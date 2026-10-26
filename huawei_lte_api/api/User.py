from __future__ import annotations

import base64
import contextlib
import hashlib
import hmac
import secrets
import time
from typing import TYPE_CHECKING

import requests

from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.enums.client import ResponseEnum
from huawei_lte_api.enums.user import LoginErrorEnum, LoginStateEnum, PasswordTypeEnum
from huawei_lte_api.exceptions import (
    LoginErrorAlreadyLoginException,
    LoginErrorPasswordWrongException,
    LoginErrorUsernamePasswordModifyException,
    LoginErrorUsernamePasswordOverrunException,
    LoginErrorUsernamePasswordWrongException,
    LoginErrorUsernameWrongException,
    ResponseErrorException,
    ResponseErrorLoginRequiredException,
    ResponseErrorNotSupportedException,
)

if TYPE_CHECKING:
    from types import TracebackType

    from huawei_lte_api.Session import GetResponseType, Session, SetResponseType

DEFAULT_USERNAME = "admin"

_LOGIN_ERROR_MESSAGES = {
    LoginErrorEnum.USERNAME_WRONG.value: "Username wrong",
    LoginErrorEnum.PASSWORD_WRONG.value: "Password wrong",
    LoginErrorEnum.ALREADY_LOGIN.value: "Already login",
    LoginErrorEnum.USERNAME_PWD_WRONG.value: "Username and Password wrong",
    LoginErrorEnum.USERNAME_PWD_OVERRUN.value: "Password overrun",
    LoginErrorEnum.USERNAME_PWD_MODIFY.value: "Password modify",
}

_LOGIN_ERROR_EXCEPTIONS = {
    LoginErrorEnum.USERNAME_WRONG.value: LoginErrorUsernameWrongException,
    LoginErrorEnum.PASSWORD_WRONG.value: LoginErrorPasswordWrongException,
    LoginErrorEnum.ALREADY_LOGIN.value: LoginErrorAlreadyLoginException,
    LoginErrorEnum.USERNAME_PWD_WRONG.value: LoginErrorUsernamePasswordWrongException,
    LoginErrorEnum.USERNAME_PWD_OVERRUN.value: LoginErrorUsernamePasswordOverrunException,
    LoginErrorEnum.USERNAME_PWD_MODIFY.value: LoginErrorUsernamePasswordModifyException,
}


def _login_error(e: ResponseErrorException) -> ResponseErrorException:
    message = _LOGIN_ERROR_MESSAGES.get(e.code, "Unknown")
    return _LOGIN_ERROR_EXCEPTIONS.get(e.code, ResponseErrorException)(f"{e.code}: {message}", e.code)


def scram_client_proof(
    password: str,
    salt: bytes,
    iterations: int,
    first_nonce: str,
    server_nonce: str,
) -> tuple[str, str]:
    """
    Client proof and expected server signature for the SCRAM login used by
    newer Huawei web UIs (user/challenge_login + user/authentication_login).

    Ported from the device's own JavaScript (CryptoJS.SCRAM in emui-jquery.js
    and the login handler in js/index.js). NOTE: it is NOT plain RFC 5802 -
    the firmware calls CryptoJS.HmacSHA256(message, key) as
    hmac(saltedPassword, "Client Key") and hmac(storedKey, authMessage), i.e.
    key and message are swapped compared to the RFC. An RFC-correct
    implementation is rejected by the device with 108006.

    :return: (client proof hex, expected server signature hex)
    """
    auth_message = f"{first_nonce},{server_nonce},{server_nonce}".encode()
    salted_password = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations, 32)
    client_key = hmac.new(b"Client Key", salted_password, hashlib.sha256).digest()
    stored_key = hashlib.sha256(client_key).digest()
    client_signature = hmac.new(auth_message, stored_key, hashlib.sha256).digest()
    client_proof = bytes(a ^ b for a, b in zip(client_key, client_signature)).hex()

    server_key = hmac.new(b"Server Key", salted_password, hashlib.sha256).digest()
    server_signature = hmac.new(auth_message, server_key, hashlib.sha256).hexdigest()
    return client_proof, server_signature


class UserSession:
    def __init__(self, session: Session, username: str = DEFAULT_USERNAME, password: str | None = None) -> None:
        self.user = User(session)
        self.user.login(username, password, force_new_login=True)

    def close(self) -> None:
        with contextlib.suppress(ResponseErrorLoginRequiredException, ResponseErrorNotSupportedException):
            self.user.logout()

    def __enter__(self) -> UserSession:
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None) -> None:
        self.close()


class User(ApiGroup):
    def state_login(self) -> GetResponseType:
        return self._session.get("user/state-login")

    def _state_login_with_retry(self) -> GetResponseType:
        tries = 5
        for i in range(tries):
            try:
                return self.state_login()
            except requests.exceptions.ConnectionError:  # noqa: PERF203
                # Some models reportedly close the connection if we attempt to access login state too soon after
                # setting up the session etc. In that case, retry a few times. The error is reported to be
                # ConnectionError: (
                #     'Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
                if i == tries - 1:
                    raise
                time.sleep((i + 1) / 10)

        raise ResponseErrorException(message="Tries exhausted", code=0)

    def _encode_password(self, username: str, password: str | None, password_type: PasswordTypeEnum = PasswordTypeEnum.BASE_64) -> bytes:
        if not password:
            return b""

        if password_type == PasswordTypeEnum.SHA256:
            concentrated = b"".join(
                [
                    username.encode("UTF-8"),
                    base64.b64encode(hashlib.sha256(password.encode("UTF-8")).hexdigest().encode("ascii")),
                    self._session.request_verification_tokens[0].encode("UTF-8"),
                ]
            )
            return base64.b64encode(hashlib.sha256(concentrated).hexdigest().encode("ascii"))

        return base64.b64encode(password.encode("UTF-8"))

    def _login(self, username: str, password: str | None, password_type: PasswordTypeEnum = PasswordTypeEnum.BASE_64) -> bool:
        password_encoded = self._encode_password(username, password, password_type)
        try:
            result = self._session.post_set(
                "user/login",
                {
                    "Username": username,
                    "Password": password_encoded.decode("UTF-8"),
                    "password_type": password_type.value,
                },
                refresh_csrf=True,
            )
        except ResponseErrorException as e:
            raise _login_error(e) from e

        return result == ResponseEnum.OK.value

    def _login_scram(self, username: str, password: str) -> bool:
        """
        SCRAM login (user/challenge_login -> user/authentication_login) used by
        newer web UIs, e.g. 5G CPE Pro H112-370 (emui webui 6.0) and reportedly
        B610h-72a (issue #228). These devices report password_type=4 but reject
        the legacy user/login SHA256 scheme with 108006.

        Raises ResponseErrorNotSupportedException if the device does not know
        the challenge endpoint; the caller then falls back to user/login. The
        challenge itself does not verify any credential, so probing it does not
        count towards the device's failed-login lockout.
        """
        first_nonce = secrets.token_hex(32)
        challenge = self._session.post_get(
            "user/challenge_login",
            {
                "username": username,
                "firstnonce": first_nonce,
                "mode": 1,
            },
            refresh_csrf=True,
        )
        # A firmware without SCRAM normally answers 100002 (raised by the
        # session); anything that is not a SCRAM challenge is treated the same.
        if not isinstance(challenge, dict) or not {"salt", "iterations", "servernonce"} <= challenge.keys():
            msg = "user/challenge_login did not return a SCRAM challenge"
            raise ResponseErrorNotSupportedException(msg, 100002)
        server_nonce = challenge["servernonce"]
        client_proof, server_signature = scram_client_proof(
            password,
            bytes.fromhex(challenge["salt"]),
            int(challenge["iterations"]),
            first_nonce,
            server_nonce,
        )

        try:
            result = self._session.post_get(
                "user/authentication_login",
                {
                    "clientproof": client_proof,
                    "finalnonce": server_nonce,
                },
                refresh_csrf=True,
            )
        except ResponseErrorException as e:
            raise _login_error(e) from e

        returned_signature = result.get("serversignature") if isinstance(result, dict) else None
        if returned_signature and not hmac.compare_digest(returned_signature, server_signature):
            msg = "Server signature mismatch"
            raise ResponseErrorException(msg, 0)
        return True

    def login(self, username: str = DEFAULT_USERNAME, password: str | None = None, force_new_login: bool = False) -> bool:
        if username == "":  # <= 1.6.4 backwards compatibility
            username = DEFAULT_USERNAME

        try:
            state_login = self._state_login_with_retry()
        except ResponseErrorNotSupportedException:
            return True

        if LoginStateEnum(int(state_login["State"])) == LoginStateEnum.LOGGED_IN and not force_new_login:
            return True

        password_type = PasswordTypeEnum(int(state_login.get("password_type", 0)))
        if password_type == PasswordTypeEnum.SHA256 and password:
            with contextlib.suppress(ResponseErrorNotSupportedException):
                return self._login_scram(username, password)

        return self._login(username, password, password_type)

    def logout(self) -> SetResponseType:
        return self._session.post_set(
            "user/logout",
            {
                "Logout": 1,
            },
        )

    def remind(self) -> GetResponseType:
        return self._session.get("user/remind")

    def password(self) -> GetResponseType:
        return self._session.get("user/password")

    def pwd(self) -> GetResponseType:
        return self._session.get("user/pwd")

    def set_pwd(self) -> SetResponseType:
        return self._session.post_set(
            "user/pwd",
            {
                "module": "wlan",
                "nonce": "aaaaaaa",
            },
        )

    def set_remind(self, remind_state: str) -> SetResponseType:
        return self._session.post_set(
            "user/remind",
            {
                "remindstate": remind_state,
            },
        )

    def authentication_login(self) -> GetResponseType:
        return self._session.get("user/authentication_login")

    def challenge_login(self) -> GetResponseType:
        return self._session.get("user/challenge_login")

    def hilink_login(self) -> GetResponseType:
        return self._session.get("user/hilink_login")

    def history_login(self) -> GetResponseType:
        return self._session.get("user/history-login")

    def heartbeat(self) -> GetResponseType:
        return self._session.get("user/heartbeat")

    def web_feature_switch(self) -> GetResponseType:
        return self._session.get("user/web-feature-switch")

    def input_event(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._session.get("user/input_event")

    def screen_state(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._session.get("user/screen_state")

    def session(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._session.get("user/session")

    def second_login(self) -> GetResponseType:
        return self._session.get("user/second_login")

    def remember_pwd(self) -> GetResponseType:
        return self._session.get("user/remember-pwd")

    def rule(self) -> GetResponseType:
        return self._session.get("user/rule")

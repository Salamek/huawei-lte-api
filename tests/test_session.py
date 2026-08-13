from __future__ import annotations

import base64
import hashlib
from typing import cast
from unittest.mock import Mock

import pytest
import requests

from huawei_lte_api.api.User import User
from huawei_lte_api.Connection import Connection
from huawei_lte_api.enums.client import ResponseCodeEnum
from huawei_lte_api.enums.user import LoginErrorEnum, PasswordTypeEnum
from huawei_lte_api.exceptions import (
    LoginErrorAlreadyLoginException,
    LoginErrorPasswordWrongException,
    LoginErrorUsernamePasswordModifyException,
    LoginErrorUsernamePasswordOverrunException,
    LoginErrorUsernamePasswordWrongException,
    LoginErrorUsernameWrongException,
    RequestFormatException,
    ResponseErrorException,
    ResponseErrorLoginCsrfException,
    ResponseErrorLoginRequiredException,
    ResponseErrorNotSupportedException,
    ResponseErrorSystemBusyException,
    ResponseErrorWrongSessionToken,
)
from huawei_lte_api.Session import Session


def make_response(
    content: bytes,
    *,
    response_headers: dict[str, str] | None = None,
    history: list[requests.Response] | None = None,
) -> requests.Response:
    response = Mock(spec=requests.Response)
    response.content = content
    response.headers = response_headers or {}
    response.history = history or []
    return cast("requests.Response", response)


def make_session() -> tuple[Session, Mock]:
    requests_session = Mock(spec=requests.Session)
    requests_session.get.return_value = make_response(b'<meta name="csrf_token" content="csrf-token">')
    session = Session("http://router", timeout=5, requests_session=cast("requests.Session", requests_session))
    return session, requests_session


def test_post_set_sends_cesu8_xml_and_updates_csrf_token() -> None:
    session, requests_session = make_session()
    requests_session.post.return_value = make_response(
        b"<response>OK</response>",
        response_headers={"__RequestVerificationToken": "next-token"},
    )

    result = session.post_set("sms/send-sms", {"Content": "A & < \U0001f600"})

    assert result == "OK"
    request = requests_session.post.call_args
    assert request.args[0] == "http://router/api/sms/send-sms"
    assert request.kwargs["headers"] == {
        "Content-Type": "application/xml",
        "__RequestVerificationToken": "csrf-token",
    }
    assert request.kwargs["timeout"] == 5
    assert b"A &amp; &lt; \xed\xa0\xbd\xed\xb8\x80" in request.kwargs["data"]
    assert session.request_verification_tokens == ["csrf-token", "next-token"]


def test_get_converts_cesu8_in_xml_response() -> None:
    session, requests_session = make_session()
    requests_session.get.return_value = make_response(
        b"<response><Message>Hello \xed\xa0\xbd\xed\xb8\x80</Message></response>",
        response_headers={"Content-Type": "application/xml; charset=UTF-8"},
    )

    result = session.get("sms/message")

    assert result == {"Message": "Hello \U0001f600"}
    request = requests_session.get.call_args
    assert request.args[0] == "http://router/api/sms/message"
    assert request.kwargs["headers"] == {"__RequestVerificationToken": "csrf-token"}


@pytest.mark.parametrize(
    ("content", "content_type"),
    [
        (b'{"response": {"State": 1}}', "application/json; charset=UTF-8"),
        (b'{"response": {"State": 1}}', "application/problem+json"),
        (b'{"response": {"State": 1}}', "text/html"),
    ],
)
def test_process_response_data_detects_json(content: bytes, content_type: str) -> None:
    response = make_response(content, response_headers={"Content-Type": content_type})

    assert Session._process_response_data(response) == {"response": {"State": 1}}  # noqa: SLF001


def test_process_response_data_handles_empty_response() -> None:
    assert Session._process_response_data(make_response(b"")) == {}  # noqa: SLF001


def test_process_response_data_maps_invalid_redirect_to_not_supported() -> None:
    redirect = make_response(b"", response_headers={"Location": "/html/home.html"})
    response = make_response(b"<html>not valid XML", history=[redirect])

    data = Session._process_response_data(response)  # noqa: SLF001

    with pytest.raises(ResponseErrorNotSupportedException):
        Session._check_response_status(data)  # noqa: SLF001


@pytest.mark.parametrize(
    ("code", "expected_exception"),
    [
        (ResponseCodeEnum.ERROR_SYSTEM_UNKNOWN, ResponseErrorException),
        (ResponseCodeEnum.ERROR_SYSTEM_NO_SUPPORT, ResponseErrorNotSupportedException),
        (ResponseCodeEnum.ERROR_SYSTEM_NO_RIGHTS, ResponseErrorLoginRequiredException),
        (ResponseCodeEnum.ERROR_SYSTEM_BUSY, ResponseErrorSystemBusyException),
        (ResponseCodeEnum.ERROR_FORMAT_ERROR, RequestFormatException),
        (ResponseCodeEnum.ERROR_SYSTEM_CSRF, ResponseErrorLoginCsrfException),
        (ResponseCodeEnum.ERROR_WRONG_SESSION_TOKEN, ResponseErrorWrongSessionToken),
    ],
)
def test_check_response_status_maps_error_codes(code: ResponseCodeEnum, expected_exception: type[ResponseErrorException]) -> None:
    with pytest.raises(expected_exception) as exc_info:
        Session._check_response_status({"error": {"code": str(code.value), "message": ""}})  # noqa: SLF001

    assert exc_info.value.code == code.value


def test_session_falls_back_to_token_endpoint() -> None:
    requests_session = Mock(spec=requests.Session)
    requests_session.get.side_effect = [
        make_response(b"<html></html>"),
        make_response(b"<response><token>fallback-token</token></response>"),
    ]

    session = Session("http://router", requests_session=cast("requests.Session", requests_session))

    assert session.request_verification_tokens == ["fallback-token"]
    assert requests_session.get.call_args_list[1].args[0] == "http://router/api/webserver/token"


def test_csrf_error_reloads_session_and_retries_once() -> None:
    requests_session = Mock(spec=requests.Session)
    requests_session.get.side_effect = [
        make_response(b'<meta name="csrf_token" content="first-token">'),
        make_response(b'<meta name="csrf_token" content="second-token">'),
    ]
    requests_session.post.side_effect = [
        make_response(b"<error><code>125002</code><message></message></error>"),
        make_response(b"<response>OK</response>"),
    ]
    session = Session("http://router", requests_session=cast("requests.Session", requests_session))

    assert session.post_set("device/control", {"Control": 1}) == "OK"
    assert requests_session.post.call_count == 2
    assert requests_session.post.call_args_list[0].kwargs["headers"]["__RequestVerificationToken"] == "first-token"
    assert requests_session.post.call_args_list[1].kwargs["headers"]["__RequestVerificationToken"] == "second-token"


@pytest.mark.parametrize(
    ("password_type", "expected_password"),
    [
        (PasswordTypeEnum.BASE_64, base64.b64encode(b"secret").decode()),
        (
            PasswordTypeEnum.SHA256,
            base64.b64encode(
                hashlib.sha256(b"admin" + base64.b64encode(hashlib.sha256(b"secret").hexdigest().encode("ascii")) + b"csrf-token").hexdigest().encode("ascii")
            ).decode(),
        ),
    ],
)
def test_user_login_encodes_password(password_type: PasswordTypeEnum, expected_password: str) -> None:
    session = Mock(spec=Session)
    session.request_verification_tokens = ["csrf-token"]
    session.get.return_value = {"State": "-1", "password_type": str(password_type.value)}
    session.post_set.return_value = "OK"

    assert User(cast("Session", session)).login("admin", "secret") is True
    session.post_set.assert_called_once_with(
        "user/login",
        {
            "Username": "admin",
            "Password": expected_password,
            "password_type": password_type.value,
        },
        refresh_csrf=True,
    )


def test_user_login_skips_request_when_already_logged_in() -> None:
    session = Mock(spec=Session)
    session.get.return_value = {"State": "0"}

    assert User(cast("Session", session)).login("admin", "secret") is True
    session.post_set.assert_not_called()


@pytest.mark.parametrize(
    ("code", "expected_exception"),
    [
        (LoginErrorEnum.USERNAME_WRONG, LoginErrorUsernameWrongException),
        (LoginErrorEnum.PASSWORD_WRONG, LoginErrorPasswordWrongException),
        (LoginErrorEnum.ALREADY_LOGIN, LoginErrorAlreadyLoginException),
        (LoginErrorEnum.USERNAME_PWD_WRONG, LoginErrorUsernamePasswordWrongException),
        (LoginErrorEnum.USERNAME_PWD_OVERRUN, LoginErrorUsernamePasswordOverrunException),
        (LoginErrorEnum.USERNAME_PWD_MODIFY, LoginErrorUsernamePasswordModifyException),
    ],
)
def test_user_login_maps_authentication_errors(code: LoginErrorEnum, expected_exception: type[ResponseErrorException]) -> None:
    session = Mock(spec=Session)
    session.request_verification_tokens = ["csrf-token"]
    session.get.return_value = {"State": "-1"}
    session.post_set.side_effect = ResponseErrorException("router error", code.value)

    with pytest.raises(expected_exception) as exc_info:
        User(cast("Session", session)).login("admin", "secret")

    assert exc_info.value.code == code.value


def test_connection_uses_url_credentials_but_removes_them_from_requests() -> None:
    requests_session = Mock(spec=requests.Session)
    requests_session.get.side_effect = [
        make_response(b'<meta name="csrf_token" content="csrf-token">'),
        make_response(b"<response><State>-1</State><password_type>0</password_type></response>"),
    ]
    requests_session.post.return_value = make_response(b"<response>OK</response>")

    Connection("http://admin:secret@router", requests_session=cast("requests.Session", requests_session))

    assert requests_session.get.call_args_list[0].args[0] == "http://router/"
    assert requests_session.get.call_args_list[1].args[0] == "http://router/api/user/state-login"
    login_request = requests_session.post.call_args
    assert login_request.args[0] == "http://router/api/user/login"
    assert b"<Username>admin</Username>" in login_request.kwargs["data"]
    assert b"<Password>c2VjcmV0</Password>" in login_request.kwargs["data"]

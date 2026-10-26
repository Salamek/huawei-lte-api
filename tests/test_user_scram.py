"""Tests for SCRAM login (user/challenge_login + user/authentication_login)."""

from __future__ import annotations

import hashlib
import hmac
from typing import Any, Callable, cast
from unittest.mock import Mock

import pytest

from huawei_lte_api.api.User import User, scram_client_proof
from huawei_lte_api.exceptions import (
    LoginErrorUsernamePasswordWrongException,
    ResponseErrorException,
    ResponseErrorNotSupportedException,
)
from huawei_lte_api.Session import Session

SALT_HEX = "6b1e6a6c3b0f4a2e9d8c7b6a5f4e3d2c1b0a99887766554433221100ffeeddcc"
ITERATIONS = 100
FIRST_NONCE = "a" * 64
SERVER_NONCE = "a" * 64 + "bcdef0123456789"

PostGet = Callable[..., dict[str, str]]


def _crypto_js_hmac(message: bytes, key: bytes) -> bytes:
    """CryptoJS.HmacSHA256(message, key) as called by the device JavaScript."""
    return hmac.new(key, message, hashlib.sha256).digest()


def _reference(password: str) -> tuple[str, str]:
    """Literal transcription of the device JavaScript, independent of the implementation under test."""
    auth = f"{FIRST_NONCE},{SERVER_NONCE},{SERVER_NONCE}".encode()
    spwd = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(SALT_HEX), ITERATIONS, 32)
    ckey = _crypto_js_hmac(spwd, b"Client Key")  # scram.clientKey(spwd)
    skey = hashlib.sha256(ckey).digest()  # scram.storedKey(ckey)
    csig = _crypto_js_hmac(skey, auth)  # scram.signature(skey, authMsg)
    proof = bytes(x ^ y for x, y in zip(ckey, csig)).hex()
    server = _crypto_js_hmac(_crypto_js_hmac(spwd, b"Server Key"), auth).hex()
    return proof, server


def _user(post_get: PostGet, pw_type: str = "4") -> tuple[User, Mock]:
    session = Mock(spec=Session)
    session.get.return_value = {"State": "-1", "password_type": pw_type}
    session.post_get.side_effect = post_get
    return User(cast("Session", session)), session


def _challenge() -> dict[str, str]:
    return {"salt": SALT_HEX, "iterations": str(ITERATIONS), "servernonce": SERVER_NONCE, "modeselected": "1"}


def test_proof_matches_device_javascript() -> None:
    assert scram_client_proof("s3cret", bytes.fromhex(SALT_HEX), ITERATIONS, FIRST_NONCE, SERVER_NONCE) == _reference("s3cret")


def test_proof_is_not_rfc5802() -> None:
    """Guard against 'fixing' the argument order back to the RFC: the device rejects it."""
    spwd = hashlib.pbkdf2_hmac("sha256", b"s3cret", bytes.fromhex(SALT_HEX), ITERATIONS, 32)
    rfc_client_key = hmac.new(spwd, b"Client Key", hashlib.sha256).digest()
    proof, _ = scram_client_proof("s3cret", bytes.fromhex(SALT_HEX), ITERATIONS, FIRST_NONCE, SERVER_NONCE)
    assert bytes.fromhex(proof) != rfc_client_key


def test_scram_login_success_verifies_server_signature() -> None:
    seen: dict[str, str] = {}

    def post_get(endpoint: str, data: dict[str, Any], **_kwargs: object) -> dict[str, str]:
        if endpoint == "user/challenge_login":
            seen["first"] = data["firstnonce"]
            return _challenge()
        _proof, server = scram_client_proof("pw", bytes.fromhex(SALT_HEX), ITERATIONS, seen["first"], SERVER_NONCE)
        return {"serversignature": server}

    user, session = _user(post_get)
    assert user.login("admin", "pw") is True
    session.post_set.assert_not_called()  # legacy user/login never attempted


def test_scram_login_rejects_forged_server_signature() -> None:
    def post_get(endpoint: str, _data: dict[str, Any], **_kwargs: object) -> dict[str, str]:
        return _challenge() if endpoint == "user/challenge_login" else {"serversignature": "00" * 32}

    user, _ = _user(post_get)
    with pytest.raises(ResponseErrorException):
        user.login("admin", "pw")


def test_scram_wrong_password_maps_to_login_error() -> None:
    def post_get(endpoint: str, _data: dict[str, Any], **_kwargs: object) -> dict[str, str]:
        if endpoint == "user/challenge_login":
            return _challenge()
        msg = "108006: Unknown"
        raise ResponseErrorException(msg, 108006)

    user, _ = _user(post_get)
    with pytest.raises(LoginErrorUsernamePasswordWrongException):
        user.login("admin", "wrong")


def test_falls_back_to_legacy_login_when_challenge_not_supported() -> None:
    def post_get(*_args: object, **_kwargs: object) -> dict[str, str]:
        msg = "100002: No support"
        raise ResponseErrorNotSupportedException(msg, 100002)

    user, session = _user(post_get)
    session.request_verification_tokens = ["token"]
    session.post_set.return_value = "OK"
    assert user.login("admin", "pw") is True
    assert session.post_set.call_args[0][0] == "user/login"


def test_no_scram_for_non_sha256_password_type() -> None:
    def post_get(*_args: object, **_kwargs: object) -> dict[str, str]:
        return _challenge()

    user, session = _user(post_get, pw_type="0")
    session.post_set.return_value = "OK"
    assert user.login("admin", "pw") is True
    session.post_get.assert_not_called()

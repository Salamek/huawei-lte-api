"""Exercise authentication through Session's real XML and CSRF handling."""

from __future__ import annotations

import base64
import hashlib
from typing import cast
from unittest.mock import Mock

import pytest
import requests
import xmltodict

from huawei_lte_api.api.User import User, scram_client_proof
from huawei_lte_api.exceptions import LoginErrorUsernamePasswordWrongException, ResponseErrorException
from huawei_lte_api.Session import Session
from tests.test_session import make_response


def make_user() -> tuple[User, Mock]:
    http = Mock(spec=requests.Session)
    http.get.side_effect = [
        make_response(b'<meta name="csrf_token" content="initial-token">'),
        make_response(b"<response><State>-1</State><password_type>4</password_type></response>"),
        make_response(b'<meta name="csrf_token" content="reloaded-token">'),
    ]
    return User(Session("http://router", requests_session=cast("requests.Session", http))), http


@pytest.mark.parametrize(
    "challenge",
    [
        b"<error><code>100002</code><message/></error>",
        b"<error><code>100003</code><message/></error>",
        b"<response/>",
        b"<response>OK</response>",
    ],
)
@pytest.mark.parametrize("rotate_token", [False, True])
def test_legacy_fallback_uses_current_csrf_token(challenge: bytes, *, rotate_token: bool) -> None:
    user, http = make_user()
    headers = {"__RequestVerificationToken": "replacement-token"} if rotate_token else {}
    http.post.side_effect = [make_response(challenge, response_headers=headers), make_response(b"<response>OK</response>")]

    assert user.login("admin", "pw") is True

    assert http.post.call_count == 2
    request = http.post.call_args_list[1]
    assert request.args[0] == "http://router/api/user/login"
    token = "replacement-token" if rotate_token else "reloaded-token"
    assert request.kwargs["headers"]["__RequestVerificationToken"] == token
    expected_password = base64.b64encode(
        hashlib.sha256(b"admin" + base64.b64encode(hashlib.sha256(b"pw").hexdigest().encode()) + token.encode()).hexdigest().encode(),
    ).decode()
    assert xmltodict.parse(request.kwargs["data"])["request"] == {
        "Username": "admin",
        "Password": expected_password,
        "password_type": "4",
    }
    assert http.get.call_count == (2 if rotate_token else 3)


@pytest.mark.parametrize(
    "reply",
    [
        b"<response/>",
        b"<response>OK</response>",
        b"<response><serversignature/></response>",
        b"<response><serversignature>forged</serversignature></response>",
    ],
)
def test_scram_requires_valid_server_signature(reply: bytes) -> None:
    user, http = make_user()
    http.post.side_effect = [
        make_response(b"<response><salt>0102</salt><iterations>100</iterations><servernonce>nonce</servernonce></response>"),
        make_response(reply),
    ]

    with pytest.raises(ResponseErrorException, match=r"[Ss]erver signature"):
        user.login("admin", "pw")

    assert http.post.call_count == 2
    assert http.post.call_args.args[0] == "http://router/api/user/authentication_login"


@pytest.mark.parametrize("code", [100002, 100003, 108006])
def test_authentication_error_never_falls_back_to_legacy(code: int) -> None:
    user, http = make_user()
    http.post.side_effect = [
        make_response(b"<response><salt>0102</salt><iterations>100</iterations><servernonce>nonce</servernonce></response>"),
        make_response(f"<error><code>{code}</code><message/></error>".encode()),
    ]
    expected_exception = LoginErrorUsernamePasswordWrongException if code == 108006 else ResponseErrorException

    with pytest.raises(expected_exception) as exc_info:
        user.login("admin", "pw")

    assert exc_info.value.code == code
    assert http.post.call_count == 2
    assert http.get.call_count == 2


def test_challenge_login_error_preserves_specialized_exception() -> None:
    user, http = make_user()
    http.post.return_value = make_response(b"<error><code>108006</code><message/></error>")

    with pytest.raises(LoginErrorUsernamePasswordWrongException):
        user.login("admin", "pw")

    assert http.post.call_count == 1


def test_scram_round_trip_sends_proof_and_rotates_tokens() -> None:
    user, http = make_user()
    first_nonce = ""

    def post(url: str, *, data: bytes, headers: dict[str, str], timeout: object) -> requests.Response:
        nonlocal first_nonce
        assert timeout is None
        payload = xmltodict.parse(data)["request"]
        if url.endswith("/challenge_login"):
            assert headers["__RequestVerificationToken"] == "initial-token"
            first_nonce = payload["firstnonce"]
            assert len(bytes.fromhex(first_nonce)) == 32
            assert payload["username"] == "admin"
            assert payload["mode"] == "1"
            return make_response(
                f"<response><salt>0102</salt><iterations>100</iterations><servernonce>{first_nonce}server</servernonce></response>".encode(),
                response_headers={"__RequestVerificationToken": "challenge-token"},
            )
        assert url == "http://router/api/user/authentication_login"
        assert headers["__RequestVerificationToken"] == "challenge-token"
        proof, signature = scram_client_proof("pw", bytes.fromhex("0102"), 100, first_nonce, first_nonce + "server")
        assert payload == {"clientproof": proof, "finalnonce": first_nonce + "server"}
        return make_response(
            f"<response><serversignature>{signature}</serversignature></response>".encode(),
            response_headers={"__RequestVerificationToken": "authenticated-token"},
        )

    http.post.side_effect = post
    assert user.login("admin", "pw") is True
    assert http.post.call_count == 2
    assert http.get.call_count == 2

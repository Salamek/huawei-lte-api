import pytest

from huawei_lte_api.Session import cesu8_encode, cesu8_fix


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", b""),
        ("ASCII", b"ASCII"),
        ("\u00e9\u20ac", b"\xc3\xa9\xe2\x82\xac"),
        ("\U00010000", b"\xed\xa0\x80\xed\xb0\x80"),
        ("\U0001f600", b"\xed\xa0\xbd\xed\xb8\x80"),
        ("\U0010ffff", b"\xed\xaf\xbf\xed\xbf\xbf"),
        ("a\U0001f600b\U00010000c", b"a\xed\xa0\xbd\xed\xb8\x80b\xed\xa0\x80\xed\xb0\x80c"),
    ],
)
def test_cesu8_encode(text: str, expected: bytes) -> None:
    assert cesu8_encode(text) == expected


@pytest.mark.parametrize(
    ("blob", "expected"),
    [
        (b"", b""),
        (b"ASCII", b"ASCII"),
        (b"\xc3\xa9\xe2\x82\xac", b"\xc3\xa9\xe2\x82\xac"),
        (b"\xed\xa0\x80\xed\xb0\x80", b"\xf0\x90\x80\x80"),
        (b"\xed\xa0\xbd\xed\xb8\x80", b"\xf0\x9f\x98\x80"),
        (b"\xed\xaf\xbf\xed\xbf\xbf", b"\xf4\x8f\xbf\xbf"),
        (
            b"a\xed\xa0\xbd\xed\xb8\x80b\xed\xa0\x80\xed\xb0\x80c",
            b"a\xf0\x9f\x98\x80b\xf0\x90\x80\x80c",
        ),
    ],
)
def test_cesu8_fix(blob: bytes, expected: bytes) -> None:
    assert cesu8_fix(blob) == expected


@pytest.mark.parametrize(
    "blob",
    [
        b"\xed\xa0\x80",
        b"\xed\xb0\x80\xed\xa0\x80",
        b"\xed\x9f\xbf\xed\xb0\x80",
        b"\xed\xa0\x80\xed\xc0\x80",
    ],
)
def test_cesu8_fix_leaves_non_surrogate_pairs_unchanged(blob: bytes) -> None:
    assert cesu8_fix(blob) == blob


@pytest.mark.parametrize(
    "text",
    [
        "plain text",
        "Za\u017c\u00f3\u0142\u0107 g\u0119\u015bl\u0105 ja\u017a\u0144",
        "minimum: \U00010000",
        "emoji: \U0001f600 \U0001f4f6",
        "maximum: \U0010ffff",
    ],
)
def test_cesu8_encode_and_fix_round_trip(text: str) -> None:
    assert cesu8_fix(cesu8_encode(text)).decode() == text

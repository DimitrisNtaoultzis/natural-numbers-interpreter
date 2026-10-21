import pytest

from src.interpreter import is_valid_greek_phone, parse_input


def test_parse_input_splits_on_spaces():
    assert parse_input("30 2 5 58") == ["30", "2", "5", "58"]


def test_parse_input_keeps_leading_zeros():
    assert parse_input("0 0 30 69") == ["0", "0", "30", "69"]


def test_parse_input_ignores_extra_whitespace():
    assert parse_input("  2 10  69 ") == ["2", "10", "69"]


@pytest.mark.parametrize(
    "text",
    [
        "",
        "  ",
        "30 abc",
        "30 -1",
        "3.5",
        "30 $%",
        "1234",
        "2²",
    ],
)
def test_parse_input_rejects_invalid_input(text):
    with pytest.raises(ValueError):
        parse_input(text)


@pytest.mark.parametrize(
    "number, expected",
    [
        # Examples from the assignment
        ("302558", False),
        ("2106930664", True),
        ("21069306604", False),
        ("00306974092252", True),
        # 10 digits
        ("6912345678", True),
        ("7106930664", False),
        ("6112345678", False),
        ("210693066", False),
        # 14 digits
        ("00302106930664", True),
        ("00301234567890", False),
        ("0030210693066", False),
        # Edge cases
        ("2", False),
        ("", False),
    ],
)
def test_is_valid_greek_phone(number, expected):
    assert is_valid_greek_phone(number) is expected

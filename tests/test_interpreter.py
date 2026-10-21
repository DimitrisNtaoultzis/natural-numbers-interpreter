import pytest

from src.interpreter import parse_input


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

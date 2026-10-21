import pytest

from src.interpreter import (
    group_value,
    interpretations,
    is_valid_greek_phone,
    parse_input,
    spoken_forms,
)


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


@pytest.mark.parametrize(
    "token, expected",
    [
        # Never split
        ("0", ["0"]),
        ("7", ["7"]),
        ("05", ["05"]),
        ("007", ["007"]),
        ("16", ["16"]),
        ("30", ["30"]),
        ("700", ["700"]),
        # Split
        ("69", ["69", "609"]),
        ("705", ["705", "7005"]),
        ("715", ["715", "70015"]),
        ("720", ["720", "70020"]),
        ("724", ["724", "70024", "700204"]),
    ],
)
def test_spoken_forms(token, expected):
    assert spoken_forms(token) == expected


@pytest.mark.parametrize(
    "tokens, expected",
    [
        # Valid groups
        (["30", "6"], "36"),
        (["700", "24"], "724"),
        (["700", "5"], "705"),
        (["700", "15"], "715"),
        (["700", "20"], "720"),
        (["700", "20", "4"], "724"),
        # Invalid groups
        (["30"], None),
        (["10", "6"], None),
        (["30", "0"], None),
        (["30", "69"], None),
        (["0", "5"], None),
        (["700", "0"], None),
        (["700", "05"], None),
        (["700", "300"], None),
        (["720", "4"], None),
        (["700", "24", "1"], None),
        (["30", "6", "1"], None),
    ],
)
def test_group_value(tokens, expected):
    assert group_value(tokens) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        # Example 1 from the assignment
        ("2 10 6 9 30 6 6 4", {"2106930664", "210693664"}),
        # Example 2 from the assignment
        (
            "2 10 69 30 6 6 4",
            {"2106930664", "210693664", "2106093664", "21060930664"},
        ),
        # Spoken as one number, so "7204" must not appear
        ("700 24", {"70024", "700204", "724"}),
    ],
)
def test_interpretation_match_all_expected(text, expected):
    results = interpretations(parse_input(text))
    assert len(results) == len(expected)
    assert set(results) == expected


def test_interpretations_example_3():
    results = interpretations(parse_input("0 0 30 69 700 24 1 3 50 2"))
    assert len(results) == 12
    for number in [
        "0030697002413502",
        "003069700241352",
        "00306972413502",
        "00306097241352",
    ]:
        assert number in results


@pytest.mark.parametrize(
    "text",
    ["30 2 5 58", "2 10 69 30 6 60 4", "0 0 30 69 700 24 1 3 50 2"],
)
def test_interpretation_literal_reading_first(text):
    tokens = parse_input(text)
    assert interpretations(tokens)[0] == "".join(tokens)

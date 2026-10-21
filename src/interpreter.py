MAX_TOKENS_DIGITS = 3


def parse_input(text: str) -> list[str]:
    """Split a space-separated sequence of numbers into tokens.
    Tokens are kept as strings so that leading zeros (e.g. "0 0 30") survive.
    Raises ValueError if the input is empty or any token is not a number of 1 to MAX_TOKEN_DIGITS ASCII digits.
    """

    tokens = text.split()

    if not tokens:
        raise ValueError("Input is empty: expected numbers separated by spaces")

    for token in tokens:
        if not (token.isascii() and token.isdigit()):
            raise ValueError(f"Invalid token '{token}': only digits 0-9 are allowed")
        if len(token) > MAX_TOKENS_DIGITS:
            raise ValueError(
                f"Invalid token '{token}': each number may have up to '{MAX_TOKENS_DIGITS}' digits "
            )

    return tokens


def is_valid_greek_phone(number: str) -> bool:
    """Valid Greek numbers: 10 digits starting with 2 or 69, or 14 digits starting with 00302 or 003069"""

    return (number.startswith(("2", "69")) and len(number) == 10) or (
        number.startswith(("00302", "003069")) and len(number) == 14
    )


def spoken_forms(token: str) -> list[str]:
    """Return every way a spoken number could have been written down

    The token itself comes first. A number like "724" (seven hundred twenty four)
    may also be written as "70024" or "700204"
    """
    if len(token) == 1 or token.startswith("0"):
        return [token]

    if len(token) == 2:
        tens, unit = token
        if tens == "1" or unit == "0":
            return [token]
        return [token, tens + "0" + unit]

    hundreds, rest = token[0], token[1:]
    if rest == "00":
        return [token]
    if rest.startswith("0"):
        return [token, hundreds + "00" + rest[1]]
    return [token] + [hundreds + "00" + form for form in spoken_forms(rest)]


def is_unit(token: str) -> bool:
    return len(token) == 1 and token != "0"


def is_round_tens(token: str) -> bool:
    return len(token) == 2 and token[0] in "23456789" and token[1] == "0"


def is_round_hundreds(token: str) -> bool:
    return len(token) == 3 and token[0] != "0" and token[1:] == "00"


def is_below_hundred(token: str) -> bool:
    return len(token) <= 2 and not token.startswith("0")


def group_value(tokens: list[str]) -> str | None:
    """Return the value of tokens that form one spoken number, else None

    Valid groups: "30 6" -> "36", "700 24" -> "724", "700 20 4" -> "724"
    """
    if len(tokens) == 2:
        first, second = tokens
        is_valid = (is_round_tens(first) and is_unit(second)) or (
            is_round_hundreds(first) and is_below_hundred(second)
        )
    elif len(tokens) == 3:
        first, second, third = tokens
        is_valid = is_round_hundreds(first) and is_round_tens(second) and is_unit(third)
    else:
        is_valid = False

    if not is_valid:
        return None
    return str(sum(int(token) for token in tokens))

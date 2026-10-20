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

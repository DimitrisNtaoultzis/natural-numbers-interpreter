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

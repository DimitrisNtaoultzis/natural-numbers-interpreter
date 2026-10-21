from src.interpreter import interpretations, is_valid_greek_phone, parse_input


def main() -> None:
    text = input("Enter numbers separated by spaces: ")

    try:
        tokens = parse_input(text)
    except ValueError as error:
        print(f"Error: {error}")
        return

    numbers = interpretations(tokens)
    width = max(len("Output"), *(len(number) for number in numbers))

    print()
    print(f"{'#':<4}{'Output':<{width}}  Phone number")
    for index, number in enumerate(numbers, start=1):
        status = "VALID" if is_valid_greek_phone(number) else "INVALID"
        print(f"{index:<4}{number:<{width}}  {status}")


if __name__ == "__main__":
    main()

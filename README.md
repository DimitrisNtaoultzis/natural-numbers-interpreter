# Natural Numbers Interpreter

A command-line application that interprets a phone number spoken as a sequence
of numbers (as a speech recognizer would transcribe it), lists every possible
interpretation of it, and checks whether each one is a valid Greek phone number.

For example, "sixty nine" may be transcribed as `69` or `60 9`, and
"thirty six" as `36` or `30 6`, so the input `2 10 69 30 6 6 4` has four
possible interpretations.

## Requirements

- Python 3.10 or newer (no third-party packages needed to run the application)
- [pytest](https://pytest.org) (only for running the tests)

## Running the application

From the project root:

```
python main.py
```

On Windows, if `python` is not on your PATH, use `py main.py` instead.

Example:

```
Enter numbers separated by spaces: 2 10 69 30 6 6 4

#   Output       Phone number
1   2106930664   VALID
2   210693664    INVALID
3   21060930664  INVALID
4   2106093664   VALID
```

Invalid input is reported without crashing:

```
Enter numbers separated by spaces: 30 abc
Error: Invalid token 'abc': only digits 0-9 are allowed
```

## Running the tests

```
python -m pip install pytest
python -m pytest
```

The tests cover every function, including all the examples from the assignment.

## Project structure

```
main.py                    Command-line interface (all input/output lives here)
src/interpreter.py         Parsing, interpretation and phone validation logic
tests/test_interpreter.py  Unit tests
```

The logic in `src/interpreter.py` does no input/output, so it can be tested
directly and reused behind a different interface.

## How it works

An interpretation is built by answering two questions:

1. **Grouping:** which consecutive tokens were spoken as a single number?
   `30 6` may be one number (36) or two (30 and 6).
2. **Writing:** in how many ways can that number be written down?
   724 may be written as `724`, `70024` (700 24) or `700204` (700 20 4).

Every combination of groupings and written forms is generated recursively,
and duplicates are removed while preserving order.

### Rules

A **group** of tokens forms one spoken number if it is:

| Group                                   | Example    | Value |
|-----------------------------------------|------------|-------|
| round tens (20-90) + digit (1-9)        | `30 6`     | 36    |
| round hundreds (100-900) + number 1-99  | `700 24`   | 724   |
| round hundreds + round tens + digit     | `700 20 4` | 724   |

A **number** can be written in these ways:

| Number                                    | Example | Written forms              |
|-------------------------------------------|---------|----------------------------|
| two digits, 21-99, not ending in 0        | `69`    | `69`, `609`                |
| hundreds with a single-digit remainder    | `705`   | `705`, `7005`              |
| hundreds with a remainder of 10-99        | `724`   | `724`, `70024`, `700204`   |
| anything else                             | `16`    | `16`                       |

### Phone number validation

A number is a valid Greek phone number if it has:

- 10 digits and starts with `2` or `69`, or
- 14 digits and starts with `00302` or `003069`.

## Assumptions and design decisions

- **Input:** numbers of 1 to 3 ASCII digits separated by whitespace. Extra
  spaces are ignored. Empty input, non-digit characters (including signs,
  decimals and characters such as `²`) and numbers longer than 3 digits are
  rejected.
- **Leading zeros** are kept (`0 0 30` gives `0030`), so tokens are handled as
  strings, never as integers. A token with a leading zero, such as `05`, has no
  natural spoken form, so it is never split or merged.
- **10-19** are spoken as a single word ("sixteen"), so `10 6` is never merged
  into `16`, and `16` is never split.
- **Only tokens that were transcribed separately are merged.** `700 24` can
  become `724`, but is never read as `720 4` (7204), because "twenty four" was
  transcribed as one token. On the other hand, `700 20 4` can also be read as
  `720` followed by `4`.
- `720 4` is not merged into `724`, since the rules above only merge round
  tens or round hundreds.
- **Order of results:** the literal reading (tokens joined as they are) is
  always listed first. The remaining interpretations may appear in a different
  order than in the assignment's examples.

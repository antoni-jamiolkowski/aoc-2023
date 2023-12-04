import argparse

import pytest


DIGITS_MAPPING: dict[str, str] = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

DIGITS: tuple[str, ...] = tuple(str(digit_int)for digit_int in range(1,10))


def main(input_file_path: str) -> int:
    with open(input_file_path, encoding="utf-8") as input_file:
        lines: list[str] = [line.strip() for line in input_file]

    first_digit = map(find_first_digit, lines)
    last_digit = map(find_last_digit, lines)
    numbers = map(lambda fd, ld: int(fd + ld), first_digit, last_digit)

    return sum(numbers)

def find_first_digit(line: str) -> str:
    for index, character in enumerate(line):
        if character.isdigit():
            return character
        for digit_name, digit in DIGITS_MAPPING.items():
            if line[index:].startswith(digit_name):
                return digit

    raise AssertionError("No digit was found.")


def find_last_digit(line: str) -> str:
    for index, character in reversed(list(enumerate(line))):
        if character.isdigit():
            return character
        for digit_name, digit in DIGITS_MAPPING.items():
            if line[:index + 1].endswith(digit_name):
                return digit

    raise AssertionError("No digit was found.")


@pytest.mark.parametrize("test_file_path, target_value", [("test_input.txt", 281)])
def test_main(test_file_path: str, target_value: int):
    assert main(test_file_path) == target_value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path", type=str)
    args = parser.parse_args()

    print(main(args.input_file_path))

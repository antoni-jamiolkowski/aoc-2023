import argparse

import pytest


def main(input_file_path: str) -> int:
    with open(input_file_path, encoding="utf-8") as input_file:
        sum_: int = 0
        for line in input_file:
            first_digit: str = None
            last_digit: str = None
            for character in line.strip():
                if character.isdigit():
                    if first_digit is None:
                        first_digit = character
                        last_digit = character
                    else:
                        last_digit = character

            if first_digit is None or last_digit is None:
                raise AssertionError

            sum_ += int(first_digit + last_digit)
    return sum_


@pytest.mark.parametrize("test_file_path, target_value", [("test_input.txt", 142)])
def test_main(test_file_path: str, target_value: int):
    assert main(test_file_path) == target_value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path", type=str)
    args = parser.parse_args()

    print(main(args.input_file_path))

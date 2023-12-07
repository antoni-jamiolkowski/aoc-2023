import argparse
from typing import NamedTuple, TypeAlias

import pytest


def main(input_file_path: str) -> int:
    sum_: int = 0
    with open(input_file_path, "r", encoding="utf-8") as input_file:
        lines: list[str] = [line.strip() for line in input_file]

    for line_id, line in enumerate(lines):
        numbers_candidates = find_numbers_candidates(line)
        valid_numbers = validate_numbers(lines, line_id, numbers_candidates)
        sum_ += sum(valid_numbers)

    return sum_


Coordinate: TypeAlias = tuple[int, ...]


class NumbersCandidates(NamedTuple):
    numbers: list[int]
    numbers_coords: list[Coordinate]


def find_numbers_candidates(line: str) -> NumbersCandidates:
    numbers: list[int] = []
    numbers_coords: list[Coordinate] = []

    number_candidate: str = ""
    candidate_coord: list[int] = []
    for char_id, char in enumerate(line):
        if char.isdigit():
            number_candidate += char
            candidate_coord.append(char_id)
        elif number_candidate:
            numbers.append(int(number_candidate))
            numbers_coords.append(tuple(candidate_coord))
            number_candidate = ""
            candidate_coord = []

    if number_candidate:
        numbers.append(int(number_candidate))
        numbers_coords.append(tuple(candidate_coord))

    return NumbersCandidates(numbers=numbers, numbers_coords=numbers_coords)


def validate_numbers(
    lines: list[str], current_line_id: int, numbers_candidates: NumbersCandidates
) -> list[int]:
    valid_numbers: list[int] = []
    investigated_lines: list[str] = [
        lines[line_id]
        for line_id in [current_line_id - 1, current_line_id, current_line_id + 1]
        if line_id >= 0 and line_id < len(lines)
    ]
    # assumption: all lines are of the same length
    line_length = len(investigated_lines[0])

    for number, number_coord in zip(*numbers_candidates):
        search_window: list[int] = _create_search_window(number_coord, line_length)
        if _is_valid_number(search_window, investigated_lines):
            valid_numbers.append(number)

    return valid_numbers


def _create_search_window(number_coord: Coordinate, line_length: int) -> list[int]:
    search_window = list(number_coord)
    if number_coord[0] - 1 >= 0:
        search_window = [number_coord[0] - 1, *search_window]
    if number_coord[-1] + 1 < line_length:
        search_window = [*search_window, number_coord[-1] + 1]
    return search_window


def _is_valid_number(search_window: list[int], investigated_lines: list[str]) -> bool:
    """Helper that goes vertically through investigated lines."""
    for investigated_id in search_window:
        if _has_adjacent_symbol(investigated_lines, investigated_id):
            return True
    return False


def _has_adjacent_symbol(lines: list[str], char_id: int) -> bool:
    """
    Return `True` when one of the lines has a \"symbol\" under specified index
    or `False` otherwise.
    """
    for line in lines:
        char = line[char_id]
        if not char.isdigit() and char != ".":
            return True
    return False


@pytest.mark.parametrize(
    "test_file_path, target_value",
    [("test_input.txt", 4361), ("test_input2.txt", 2957), ("test_input3.txt", 6079)],
)
def test_main(test_file_path: str, target_value: int):
    assert main(test_file_path) == target_value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path", type=str)
    args = parser.parse_args()

    print(main(args.input_file_path))

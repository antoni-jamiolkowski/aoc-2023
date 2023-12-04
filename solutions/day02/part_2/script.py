import argparse

import pytest
import numpy as np


def main(input_file_path: str) -> int:
    sum_: int = 0
    with open(input_file_path, "r", encoding="utf-8") as input_file:
        for line in input_file:
            line = line.strip()
            _, cubes_info = line.split(":")
            subsets = cubes_info.split(";")

            game_counts = np.array([extract_cubes_count(subset) for subset in subsets])
            required_count = game_counts.max(axis=0)
            sum_ += np.prod(required_count, dtype=int)

    return sum_


def extract_cubes_count(subset: str) -> np.ndarray:
    color_id_mapping = dict(red=0, green=1, blue=2)
    cubes_count = np.zeros(3) # the first value is for red, second for green, third for blue
    cubes = subset.split(",", maxsplit=3)
    for cube_record in cubes:
        count, color = cube_record.strip().split(" ")
        cubes_count[color_id_mapping[color]] = count

    return cubes_count


@pytest.mark.parametrize("test_file_path, target_value", [("test_input.txt", 2286)])
def test_main(test_file_path: str, target_value: int):
    assert main(test_file_path) == target_value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path", type=str)
    args = parser.parse_args()

    print(main(args.input_file_path))

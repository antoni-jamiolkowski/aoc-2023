import argparse

import numpy as np
import pytest


def main(
    input_file_path: str, red_cubes: int, green_cubes: int, blue_cubes: int
) -> int:
    puzzle_target = np.array([red_cubes, green_cubes, blue_cubes])
    sum_: int = 0
    with open(input_file_path, "r", encoding="utf-8") as input_file:
        for line in input_file:
            line = line.strip()
            game_info, cubes_info = line.split(":")
            game_id = int(game_info.lstrip("Game "))
            subsets = cubes_info.split(";")

            game_counts: list[np.ndarray] = []
            for subset in subsets:
                game_counts.append(extract_cubes_count(subset))

            game_counts = np.array(game_counts)
            if (game_counts <= puzzle_target).all().all():
                sum_ += game_id

    return sum_


def extract_cubes_count(subset: str) -> np.ndarray:
    color_id_mapping = dict(red=0, green=1, blue=2)
    cubes_count = np.zeros(
        3
    )  # the first value is for red, second for green, third for blue
    cubes = subset.split(",", maxsplit=3)
    for cube_record in cubes:
        count, color = cube_record.strip().split(" ")
        cubes_count[color_id_mapping[color]] = count

    return cubes_count


@pytest.mark.parametrize(
    "test_file_path, red_cubes, green_cubes, blue_cubes, target_value",
    [
        ("test_input.txt", 12, 13, 14, 8),
    ],
)
def test_main(
    test_file_path: str,
    red_cubes: int,
    green_cubes: int,
    blue_cubes: int,
    target_value: int,
):
    games_id_sum = main(
        test_file_path,
        red_cubes=red_cubes,
        green_cubes=green_cubes,
        blue_cubes=blue_cubes,
    )
    assert games_id_sum == target_value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path", type=str)
    parser.add_argument("red_cubes", type=int)
    parser.add_argument("green_cubes", type=int)
    parser.add_argument("blue_cubes", type=int)
    args = parser.parse_args()

    print(
        main(
            args.input_file_path,
            red_cubes=args.red_cubes,
            green_cubes=args.green_cubes,
            blue_cubes=args.blue_cubes,
        )
    )

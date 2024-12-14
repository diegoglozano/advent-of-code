from pathlib import Path
from functools import lru_cache


@lru_cache(maxsize=None)
def multiply_by_2024(stone):
    return stone * 2024


@lru_cache(maxsize=None)
def split_string(stone):
    num_str = str(stone)
    if len(num_str) % 2 != 0:
        raise ValueError("The number must have an even number of digits.")

    mid = len(num_str) // 2
    part1 = int(num_str[:mid])
    part2 = int(num_str[mid:])

    return part1, part2


@lru_cache(maxsize=None)
def is_zero():
    return 1


DATA_PATH = Path("data")

with open(DATA_PATH / "day_11.txt") as f:
    stones = list(map(int, f.read().strip().split()))


@lru_cache(maxsize=None)
def func(stone, n_blinks):
    if n_blinks == 0:
        return 1
    if stone == 0:
        return func(1, n_blinks - 1)
    if len(str(stone)) % 2 == 0:
        part1, part2 = split_string(stone)
        return func(part1, n_blinks - 1) + func(part2, n_blinks - 1)
    else:
        return func(multiply_by_2024(stone), n_blinks - 1)


print(sum([func(stone, 75) for stone in stones]))

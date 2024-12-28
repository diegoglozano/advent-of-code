from pathlib import Path
from functools import lru_cache

DATA_PATH = Path("data")

with open(DATA_PATH / "day_19.txt") as f:
    patterns, designs = f.read().split("\n\n")
    raw_patterns = tuple(patterns.split(", "))
    designs = designs.splitlines()


@lru_cache
def func(design, patterns):
    if not design:
        return True
    return any(
        [
            design[: len(pattern)] == pattern and func(design[len(pattern) :], patterns)
            for pattern in patterns
        ]
    )


@lru_cache
def func_2(design, patterns):
    if not design:
        return 1
    return sum(
        [
            design[: len(pattern)] == pattern
            and func_2(design[len(pattern) :], patterns)
            for pattern in patterns
        ]
    )


total = 0
for design in designs:
    total += func(design, raw_patterns)

total_2 = 0
for design in designs:
    temp_total = func_2(design, raw_patterns)
    total_2 += temp_total

print(total)
print(total_2)

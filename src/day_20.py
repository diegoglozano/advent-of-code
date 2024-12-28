import numpy as np
from pathlib import Path

DATA_PATH = Path("data")

with open(DATA_PATH / "day_20_toy.txt") as f:
    data = np.array([list(row) for row in f.read().strip().splitlines()])

for row in data:
    print(row)

starting_row, starting_col = (
    (data == "S").argmax(0).max(),
    (data == "S").argmax(1).max(),
)


def func(data, i, j, acc, visited):
    if (i, j) in visited:
        return float("inf")
    if data[i][j] == "E":
        return acc
    if data[i][j] == "#":
        return float("inf")
    visited.add((i, j))

    return min(
        func(data, i + 1, j, acc + 1, visited.copy()),
        func(data, i - 1, j, acc + 1, visited.copy()),
        func(data, i, j + 1, acc + 1, visited.copy()),
        func(data, i, j - 1, acc + 1, visited.copy()),
    )


original_cost = func(data, starting_row, starting_col, 0, set())
print(f"Original cost: {original_cost}")

results = []
for x in range(1, data.shape[0] - 1):
    for y in range(1, data.shape[1] - 2):
        if (
            data[x, y] == "E"
            or data[x, y + 1] == "E"
            or data[x, y] == "S"
            or data[x, y + 1] == "S"
        ):
            continue
        temp_data = data.copy()
        temp_data[x, y] = "."
        temp_data[x, y + 1] = "."
        visited = set()
        results.append(func(temp_data, starting_row, starting_col, 0, visited))

for x in range(1, data.shape[0] - 2):
    for y in range(1, data.shape[1] - 1):
        if (
            data[x, y] == "E"
            or data[x + 1, y] == "E"
            or data[x, y] == "S"
            or data[x + 1, y] == "S"
        ):
            continue
        temp_data = data.copy()
        temp_data[x, y] = "."
        temp_data[x + 1, y] = "."
        visited = set()
        results.append(func(temp_data, starting_row, starting_col, 0, visited))


print(sum(1 for result in results if result < (original_cost - 100)))

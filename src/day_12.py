import numpy as np

from pathlib import Path


DATA_PATH = Path("data")
with open(DATA_PATH / "day_12_toy.txt", "r") as f:
    data = np.array([list(row) for row in f.read().splitlines()])
    data = np.pad(data, 1, "constant", constant_values=".")

print(data)


def find_perimeter(data, i, j, perimeter, visited_nodes):
    if (i, j) in visited_nodes:
        return perimeter
    visited_nodes.add((i, j))
    current_value = data[i, j]
    print("i: ", i)
    print("j: ", j)
    print("current_value: ", current_value)
    if data[i + 1, j] != current_value and (i + 1, j) not in visited_nodes:
        perimeter += 1
    if data[i - 1, j] != current_value and (i - 1, j) not in visited_nodes:
        perimeter += 1
    if data[i, j + 1] != current_value and (i, j + 1) not in visited_nodes:
        perimeter += 1
    if data[i, j - 1] != current_value and (i, j - 1) not in visited_nodes:
        perimeter += 1

    if data[i + 1, j] == current_value:
        perimeter += find_perimeter(data, i + 1, j, perimeter, visited_nodes)
    if data[i - 1, j] == current_value:
        perimeter += find_perimeter(data, i - 1, j, perimeter, visited_nodes)
    if data[i, j + 1] == current_value:
        perimeter += find_perimeter(data, i, j + 1, perimeter, visited_nodes)
    if data[i, j - 1] == current_value:
        perimeter += find_perimeter(data, i, j - 1, perimeter, visited_nodes)
    return perimeter


n_rows = data.shape[0]
n_cols = data.shape[1]

visited_nodes = set()
for i in range(1, n_rows - 1):
    for j in range(1, n_cols - 1):
        visited_nodes = set()
        perimeter = find_perimeter(data, i, j, 0, visited_nodes)
        break

print(perimeter)

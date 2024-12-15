from pathlib import Path

DATA_PATH = Path("data")

with open(DATA_PATH / "day_10.txt") as f:
    data = [list(map(int, line)) for line in f.read().splitlines()]


def func(visited, data, i, j, previous_value, reachable):
    if (i < 0) or (i >= len(data)) or (j < 0) or (j >= len(data[0])):
        return
    current_value = data[i][j]
    if current_value != (previous_value + 1):
        return
    elif current_value == 9:
        reachable.add((i, j))
        return
    elif (i, j) not in visited:
        visited.add((i, j))
        func(visited, data, i + 1, j, current_value, reachable)
        func(visited, data, i - 1, j, current_value, reachable)
        func(visited, data, i, j + 1, current_value, reachable)
        func(visited, data, i, j - 1, current_value, reachable)


def func_2(data, i, j, previous_value):
    if (i < 0) or (i >= len(data)) or (j < 0) or (j >= len(data[0])):
        return 0

    current_value = data[i][j]
    if current_value != (previous_value + 1):
        return 0
    if current_value == 9:
        return 1
    else:
        return (
            +func_2(data, i + 1, j, current_value)
            + func_2(data, i - 1, j, current_value)
            + func_2(data, i, j + 1, current_value)
            + func_2(data, i, j - 1, current_value)
        )


total = 0
total_2 = 0
for i in range(len(data)):
    for j in range(len(data[0])):
        if data[i][j] == 0:
            # Part 1
            visited = set()
            reachable = set()
            func(visited, data, i, j, -1, reachable)
            total_reachable = len(reachable)
            total += total_reachable

            # Part 2
            total_2 += func_2(data, i, j, -1)

print(f"Total: {total}")
print(f"Total_2: {total_2}")

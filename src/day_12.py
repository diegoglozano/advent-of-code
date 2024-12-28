from pathlib import Path


DATA_PATH = Path("data")
with open(DATA_PATH / "day_12.txt", "r") as f:
    data = [list(row) for row in f.read().splitlines()]

for line in data:
    print(line)


def func(data, i, j, previous_value, visited):
    if (i < 0) or (i >= len(data)) or (j < 0) or (j >= len(data[0])):
        return 1

    current_value = data[i][j]
    if current_value != previous_value:
        return 1

    if (i, j) in visited:
        return 0
    else:
        visited.add((i, j))

    return (
        +func(data, i + 1, j, current_value, visited)
        + func(data, i - 1, j, current_value, visited)
        + func(data, i, j + 1, current_value, visited)
        + func(data, i, j - 1, current_value, visited)
    )


global_visited = set()
total = 0
for i in range(len(data)):
    for j in range(len(data[0])):
        if (i, j) not in global_visited:
            visited = set()
            perimeter = func(data, i, j, data[i][j], visited)
            area = len(visited)
            price = area * perimeter
            total += price
            global_visited.update(visited)
print(total)

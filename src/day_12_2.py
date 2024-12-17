from pathlib import Path


DATA_PATH = Path("data")
with open(DATA_PATH / "day_12_toy.txt", "r") as f:
    data = [list(row) for row in f.read().splitlines()]

for line in data:
    print(line)


def func(data, i, j, previous_value, visited: set, sides: set):
    if (i < 0) or (i >= len(data)) or (j < 0) or (j >= len(data[0])):
        sides.add((i, j))
        return

    current_value = data[i][j]
    if current_value != previous_value:
        sides.add((i, j))
        return

    if (i, j) in visited:
        return
    else:
        visited.add((i, j))

    func(data, i + 1, j, current_value, visited, sides)
    func(data, i - 1, j, current_value, visited, sides)
    func(data, i, j + 1, current_value, visited, sides)
    func(data, i, j - 1, current_value, visited, sides)


global_visited = set()
total = 0
for i in range(len(data)):
    for j in range(len(data[0])):
        if (i, j) not in global_visited:
            print(data[i][j])
            visited = set()
            sides = set()
            func(data, i, j, data[i][j], visited, sides)
            total_sides = len(set([s[0] for s in sides])) + len(
                set([s[1] for s in sides])
            )
            print(total_sides)
            area = len(visited)
            price = area * total_sides
            total += price
            global_visited.update(visited)
        break
    break
print(total)

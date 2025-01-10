import itertools as it

from pathlib import Path


DATA_PATH = Path("data")
with open(DATA_PATH / "day_12_toy.txt", "r") as f:
    data = [list(row) for row in f.read().splitlines()]

for line in data:
    print(line)


DIRECTIONS = it.cycle("ESWN")
sides = 1
visited_nodes = set()
i, j = 0, 0
current_letter = data[i][j]
current_direction = next(DIRECTIONS)

for _ in it.count():
    print(f"i, j, direction {i}, {j}, {current_direction}")
    if (i, j, current_direction) in visited_nodes:
        break
    else:
        visited_nodes.add((i, j, current_direction))
    if current_direction == "E":
        if j > len(data[0]) or data[i][j + 1] != current_letter:
            current_direction = next(DIRECTIONS)
        else:
            j += 1
    elif current_direction == "S":
        if i > len(data) or data[i + 1][j] != current_letter:
            current_direction = next(DIRECTIONS)
        else:
            i += 1
    elif current_direction == "W":
        if j < 0 or data[i][j - 1] != current_letter:
            current_direction = next(DIRECTIONS)
        else:
            j -= 1
    elif current_direction == "N":
        if i < 0 or data[i - 1][j] != current_letter:
            current_direction = next(DIRECTIONS)
        else:
            i -= 1

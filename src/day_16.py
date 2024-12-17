from pathlib import Path
from itertools import cycle

DATA_PATH = Path("data")

with open(DATA_PATH / "day_16_toy_1.txt") as f:
    data = [list(line) for line in f.read().splitlines()]

for row in data:
    print(row)

clockwise = cycle("^>v<")
anticlockwise = cycle("^<v>")

START = "S"
END = "E"

for row in data:
    if START in row:
        i, j = (data.index(row), row.index(START))
    if END in row:
        target = (data.index(row), row.index(END))

graph = {}
for i in range(len(data)):
    for j in range(len(row)):
        if data[i][j] == "#":
            continue
        graph[(i, j)] = []
        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if data[i + direction[0]][j + direction[1]] != "#":
                graph[(i, j)].append((i + direction[0], j + direction[1]))

print(graph)

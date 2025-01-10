import sys
from pathlib import Path

sys.setrecursionlimit(10**6)

DATA_PATH = Path("data")

with open(DATA_PATH / "day_16.txt") as f:
    data = [list(line) for line in f.read().splitlines()]

for row in data:
    print(row)

START = "S"
END = "E"
WALL = "#"

start_i, start_j = [
    (i, j) for i, row in enumerate(data) for j, cell in enumerate(row) if cell == START
][0]
end_i, end_j = [
    (i, j) for i, row in enumerate(data) for j, cell in enumerate(row) if cell == END
][0]


def func(data, i, j, cost, direction, visited_nodes):
    if data[i][j] == WALL:
        return float("inf")
    if data[i][j] == START:
        return float("inf")
    if data[i][j] == END:
        return cost + 1
    if (i, j) in visited_nodes:
        return float("inf")
    visited_nodes.add((i, j))

    if direction == "^":
        return min(
            func(data, i - 1, j, cost + 1, "^", visited_nodes),
            func(data, i, j + 1, cost + 1001, ">", visited_nodes),
            func(data, i, j - 1, cost + 1001, "<", visited_nodes),
        )
    if direction == ">":
        return min(
            func(data, i, j + 1, cost + 1, ">", visited_nodes),
            func(data, i - 1, j, cost + 1001, "^", visited_nodes),
            func(data, i + 1, j, cost + 1001, "v", visited_nodes),
        )
    if direction == "<":
        return min(
            func(data, i, j - 1, cost + 1, "<", visited_nodes),
            func(data, i + 1, j, cost + 1001, "v", visited_nodes),
            func(data, i - 1, j, cost + 1001, "^", visited_nodes),
        )
    if direction == "v":
        return min(
            func(data, i + 1, j, cost + 1, "v", visited_nodes),
            func(data, i, j - 1, cost + 1001, "<", visited_nodes),
            func(data, i, j + 1, cost + 1001, ">", visited_nodes),
        )


cost_routes = []
visited_nodes = set()
costs = func(data, start_i - 1, start_j, 0, ">", visited_nodes)
print(costs)

# 416364 too high

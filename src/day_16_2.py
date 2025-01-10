from pathlib import Path
from heapq import heappop, heappush


DATA_PATH = Path("data")

with open(DATA_PATH / "day_16.txt") as f:
    data = [list(line) for line in f.read().splitlines()]

for row in data:
    print(row)

START = "S"
END = "E"
WALL = "#"
INITIAL_DIRECTION = ">"
INITIAL_COST = 0

start_i, start_j = [
    (i, j) for i, row in enumerate(data) for j, cell in enumerate(row) if cell == START
][0]
end_i, end_j = [
    (i, j) for i, row in enumerate(data) for j, cell in enumerate(row) if cell == END
][0]

# A* algorithm
costs = {}
priority_queue = []
heappush(priority_queue, (INITIAL_COST, start_i, start_j, INITIAL_DIRECTION))
while priority_queue:
    cost, i, j, direction = heappop(priority_queue)
    if data[i][j] == WALL:
        continue
    if data[i][j] == END:
        print(cost)
        break
    if (i, j, direction) in costs and costs[(i, j, direction)] <= cost:
        continue
    costs[(i, j, direction)] = cost
    for new_i, new_j, new_direction in [
        (i - 1, j, "^"),
        (i, j + 1, ">"),
        (i, j - 1, "<"),
        (i + 1, j, "v"),
    ]:
        new_cost = cost + (1 if new_direction == direction else 1001)
        heappush(priority_queue, (new_cost, new_i, new_j, new_direction))

print(costs)

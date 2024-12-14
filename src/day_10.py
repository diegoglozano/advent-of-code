from pathlib import Path

DATA_PATH = Path("data")

with open(DATA_PATH / "day_10_toy.txt") as f:
    data = [list(map(int, line)) for line in f.read().splitlines()]


def reach_hike(data, i, j, num_rows, num_cols, visited_nodes):
    print(f"(i, j) = ({i}, {j})")
    print(f"Value = {data[i][j]}")
    if (i, j) in visited_nodes:
        print("Already visited")
        return 0
    else:
        visited_nodes.add((i, j))
    if data[i][j] == 9:
        return 1
    if i > 0:
        next_i = i - 1
        if data[next_i][j] != data[i][j] + 1:
            print("Reach first return 0")
            return 0
        reach_hike(data, i - 1, j, num_rows, num_cols, visited_nodes)
    if i < num_rows - 1:
        next_i = i + 1
        if data[next_i][j] != data[i][j] + 1:
            print("Reach second return 0")
            return 0
        reach_hike(data, i + 1, j, num_rows, num_cols, visited_nodes)
    if j > 0:
        next_j = j - 1
        if data[i][next_j] != data[i][j] + 1:
            print("Reach third return 0")
            return 0
        reach_hike(data, i, j - 1, num_rows, num_cols, visited_nodes)
    if j < num_cols - 1:
        next_j = j + 1
        if data[i][next_j] != data[i][j] + 1:
            print("Reach fourth return 0")
            return 0
        reach_hike(data, i, j + 1, num_rows, num_cols, visited_nodes)


num_rows = len(data)
num_cols = len(data[0])
for i, line in enumerate(data):
    for j, num in enumerate(line):
        # is trailhead
        if num == 0:
            # acc = 0
            visited_nodes = set()
            test = reach_hike(data, i, j, num_rows, num_cols, visited_nodes)

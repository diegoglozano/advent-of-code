from pathlib import Path

DATA_PATH = Path("data")
with open(DATA_PATH / "day_15_toy.txt", "r") as f:
    data = [list(row) for row in f.read().splitlines()]
    warehouse_map = data[:-2]
    movements = list(data[-1])

new_warehouse_map = warehouse_map.copy()
for i, row in enumerate(warehouse_map):
    for j, col in enumerate(row):
        if warehouse_map[i][j] == "#":
            new_warehouse_map[i].pop(j)
            new_warehouse_map[i].insert(j, "##")
        elif warehouse_map[i][j] == "O":
            new_warehouse_map[i].pop(j)
            new_warehouse_map[i].insert(j, "[]")
        elif warehouse_map[i][j] == ".":
            new_warehouse_map[i].pop(j)
            new_warehouse_map[i].insert(j, "..")
        elif warehouse_map[i][j] == "@":
            new_warehouse_map[i].pop(j)
            new_warehouse_map[i].insert(j, "@.")


for row in warehouse_map:
    print(("".join(row)))

movement = movements[0]

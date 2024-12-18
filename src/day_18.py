import networkx as nx

from pathlib import Path


DATA_PATH = Path("data")

IS_PROD = True

N_BYTES = 1024 if IS_PROD else 12
X_LEN = 71 if IS_PROD else 7
Y_LEN = 71 if IS_PROD else 7

with open(DATA_PATH / f"day_18{'' if IS_PROD else '_toy'}.txt") as f:
    raw_data = f.read().splitlines()

LEN_DATA = len(raw_data)

for i in range(2, LEN_DATA):
    data = [tuple(map(int, byte.split(","))) for byte in raw_data[:i]]
    memory = [["."] * X_LEN for _ in range(Y_LEN)]
    for x, y in data:
        memory[y][x] = "#"

    graph = {}
    for y, row in enumerate(memory):
        for x, cell in enumerate(row):
            if cell == "#":
                continue
            graph[(x, y)] = []
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                if (
                    0 <= new_x < X_LEN
                    and 0 <= new_y < Y_LEN
                    and memory[new_y][new_x] != "#"
                ):
                    graph[(x, y)].append((new_x, new_y))

    g = nx.DiGraph()
    g.add_nodes_from(graph.keys())
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            g.add_edge(node, neighbor)
    try:
        print(
            nx.shortest_path_length(g, (0, 0), (X_LEN - 1, Y_LEN - 1)),
        )
    except nx.NetworkXNoPath:
        print("Found")
        print(raw_data[i - 1])
        break

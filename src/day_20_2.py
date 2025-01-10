import networkx as nx
from pathlib import Path
from collections import Counter

DATA_PATH = Path("data")

with open(DATA_PATH / "day_20_toy.txt") as f:
    raw_data = [list(row) for row in f.read().strip().splitlines()]

for row in raw_data:
    print(row)

for i, row in enumerate(raw_data):
    for j, col in enumerate(row):
        if col == "S":
            start = (i, j, "S")
        if col == "E":
            end = (i, j, "E")

lengths = []
for disable_row in range(len(raw_data)):
    for disable_col in range(len(raw_data[0]) - 1):
        if (
            raw_data[disable_row][disable_col] == "#"
            or raw_data[disable_row][disable_col + 1] == "#"
        ):
            try:
                data = raw_data.copy()
                data[disable_row][disable_col] = "."
                data[disable_row][disable_col + 1] = "."
                graph = {}
                for i in range(len(data)):
                    for j in range(len(data[0])):
                        if data[i][j] in (".", "S", "E"):
                            graph[(i, j, data[i][j])] = []
                            if i - 1 >= 0 and data[i - 1][j] == ".":
                                graph[(i, j, data[i][j])].append(
                                    (i - 1, j, data[i - 1][j])
                                )
                            if i + 1 < len(data) and data[i + 1][j] == ".":
                                graph[(i, j, data[i][j])].append(
                                    (i + 1, j, data[i + 1][j])
                                )
                            if j - 1 >= 0 and data[i][j - 1] == ".":
                                graph[(i, j, data[i][j])].append(
                                    (i, j - 1, data[i][j - 1])
                                )
                            if j + 1 < len(data[0]) and data[i][j + 1] == ".":
                                graph[(i, j, data[i][j])].append(
                                    (i, j + 1, data[i][j + 1])
                                )

                graph = nx.Graph(graph)
                lengths.append(
                    nx.shortest_path_length(
                        graph,
                        source=start,
                        target=end,
                    )
                )
            except Exception:
                continue

for disable_row in range(len(raw_data) - 1):
    for disable_col in range(len(raw_data[0])):
        if (
            raw_data[disable_row][disable_col] == "#"
            or raw_data[disable_row + 1][disable_col] == "#"
        ):
            try:
                data = raw_data.copy()
                data[disable_row][disable_col] = "."
                data[disable_row + 1][disable_col] = "."
                graph = {}
                for i in range(len(data)):
                    for j in range(len(data[0])):
                        if data[i][j] in (".", "S", "E"):
                            graph[(i, j, data[i][j])] = []
                            if i - 1 >= 0 and data[i - 1][j] == ".":
                                graph[(i, j, data[i][j])].append(
                                    (i - 1, j, data[i - 1][j])
                                )
                            if i + 1 < len(data) and data[i + 1][j] == ".":
                                graph[(i, j, data[i][j])].append(
                                    (i + 1, j, data[i + 1][j])
                                )
                            if j - 1 >= 0 and data[i][j - 1] == ".":
                                graph[(i, j, data[i][j])].append(
                                    (i, j - 1, data[i][j - 1])
                                )
                            if j + 1 < len(data[0]) and data[i][j + 1] == ".":
                                graph[(i, j, data[i][j])].append(
                                    (i, j + 1, data[i][j + 1])
                                )

                graph = nx.Graph(graph)
                lengths.append(
                    nx.shortest_path_length(
                        graph,
                        source=start,
                        target=end,
                    )
                )
            except Exception:
                continue

print(Counter([84 - length for length in lengths]))

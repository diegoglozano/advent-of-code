import networkx as nx

from pathlib import Path

DATA_PATH = Path("data")

with open(DATA_PATH / "day_23.txt") as f:
    data = [pair.split("-") for pair in f.read().strip().split("\n")]

g = nx.Graph()
g.add_edges_from(data)

cliques = nx.enumerate_all_cliques(g)
i = 0
for clique in cliques:
    if len(clique) == 3 and any([node[0] == "t" for node in clique]):
        i += 1

while True:
    try:
        clique = next(cliques)
    except StopIteration:
        break
print(",".join(sorted(clique)))

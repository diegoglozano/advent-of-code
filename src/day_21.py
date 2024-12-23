import networkx as nx

from pathlib import Path


DATA_PATH = Path("data")


class NumericPad:
    def __init__(self, starting_node: str = "A") -> None:
        self.starting_node = starting_node
        self.g = nx.DiGraph()
        self.g.add_edges_from(
            [
                ("0", "A", {"direction": ">"}),
                ("A", "0", {"direction": "<"}),
                ("0", "2", {"direction": "^"}),
                ("2", "0", {"direction": "v"}),
                ("A", "3", {"direction": "^"}),
                ("3", "A", {"direction": "v"}),
                ("1", "4", {"direction": "^"}),
                ("4", "1", {"direction": "v"}),
                ("1", "2", {"direction": ">"}),
                ("2", "1", {"direction": "<"}),
                ("2", "5", {"direction": "^"}),
                ("5", "2", {"direction": "v"}),
                ("2", "3", {"direction": ">"}),
                ("3", "6", {"direction": "^"}),
                ("6", "3", {"direction": "v"}),
                ("4", "7", {"direction": "^"}),
                ("7", "4", {"direction": "v"}),
                ("4", "5", {"direction": ">"}),
                ("5", "4", {"direction": "<"}),
                ("5", "8", {"direction": "^"}),
                ("8", "5", {"direction": "v"}),
                ("5", "6", {"direction": ">"}),
                ("6", "5", {"direction": "<"}),
                ("6", "9", {"direction": "^"}),
                ("9", "6", {"direction": "v"}),
                ("7", "8", {"direction": ">"}),
                ("8", "7", {"direction": "<"}),
                ("8", "9", {"direction": ">"}),
                ("9", "8", {"direction": "<"}),
            ]
        )

    def shortest_path(self, start: str, end: str) -> int:
        return nx.shortest_path(self.g, start, end)


class DirectionPad:
    def __init__(self, starting_node: str = "A") -> None:
        self.starting_node = starting_node
        self.g = nx.DiGraph()
        self.g.add_edges_from(
            [
                ("<", "v", {"direction": ">"}),
                ("v", "<", {"direction": "<"}),
                ("v", "^", {"direction": "^"}),
                ("^", "v", {"direction": "v"}),
                ("v", ">", {"direction": ">"}),
                (">", "v", {"direction": "<"}),
                (">", "A", {"direction": "^"}),
                ("A", ">", {"direction": "v"}),
                ("^", "A", {"direction": ">"}),
                ("A", "^", {"direction": "<"}),
            ]
        )

    def shortest_path(self, start: str, end: str) -> int:
        return nx.shortest_path(self.g, start, end)


numeric_pad = NumericPad()
direction_pad_1 = DirectionPad()
direction_pad_2 = DirectionPad()

with open(DATA_PATH / "day_21_toy.txt") as f:
    codes = f.read().splitlines()

code = codes[0]

current_numeric_pad_node = numeric_pad.starting_node
current_direction_pad_1_node = direction_pad_1.starting_node
acc = ""

# current_node = A
# 029A
for char in code:
    # A -> 0. Path = <
    shortest_path_numeric = numeric_pad.shortest_path(current_numeric_pad_node, char)
    for numeric_pad_node in range(len(shortest_path_numeric) - 1):
        direction = numeric_pad.g.edges[
            shortest_path_numeric[numeric_pad_node],
            shortest_path_numeric[numeric_pad_node + 1],
        ]["direction"]
        shortest_path_direction_1 = direction_pad_1.shortest_path(
            current_direction_pad_1_node, direction
        )
        for direction_pad_1_node in range(len(shortest_path_direction_1) - 1):
            direction = direction_pad_1.g.edges[
                shortest_path_direction_1[direction_pad_1_node],
                shortest_path_direction_1[direction_pad_1_node + 1],
            ]["direction"]
            acc += direction
            current_direction_pad_1_node = direction
        current_numeric_pad_node = char
print(acc)

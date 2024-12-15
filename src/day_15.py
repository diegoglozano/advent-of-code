from pathlib import Path
from collections import deque

from rich.console import Console
from rich.table import Table
from rich import box


def get_rich_table(input_array, style_dict):
    table = Table(show_header=False, box=box.SIMPLE)
    for row in input_array:
        table.add_row(*map(lambda x: str(style_dict.get(x, x)), row))
    return table


def get_initial_position(data, symbol="@"):
    for i, row in enumerate(data):
        for j, col in enumerate(row):
            if col == symbol:
                return i, j


STYLE_DICT = {
    "^": "[red]▲[/red]",
    ">": "[red]▶[/red]",
    "v": "[red]▼[/red]",
    "<": "[red]◀[/red]",
    "#": "[green]█[/green]",
    ".": "",
    "O": "[blue]O[/blue]",
    "@": "[yellow]@[/yellow]",
}

console = Console()

DATA_PATH = Path("data")
with open(DATA_PATH / "day_15.txt", "r") as f:
    data = [list(row) for row in f.read().splitlines()]
    warehouse_map = data[:-2]
    movements = list(data[-1])

i, j = get_initial_position(warehouse_map, symbol="@")
print(f"Inital position: {i}, {j}")

for movement in movements:
    table = get_rich_table(warehouse_map, style_dict=STYLE_DICT)
    console.clear()
    console.print(table)

    next_i = i
    next_j = j
    if movement == "^":
        next_i -= 1
        next_j = j
    elif movement == "v":
        next_i += 1
        next_j = j
    elif movement == "<":
        next_i = i
        next_j -= 1
    elif movement == ">":
        next_i = i
        next_j += 1

    if warehouse_map[next_i][next_j] == "#":
        continue
    elif warehouse_map[next_i][next_j] == "O":
        if movement == ">":
            j_to_add = 1
            while warehouse_map[i][j + j_to_add] == "O":
                j_to_add += 1
            if warehouse_map[i][j + j_to_add] == ".":
                temp_deque = deque(warehouse_map[i][j : j + j_to_add + 1])
                temp_deque.rotate(1)
                warehouse_map[i][j : j + j_to_add + 1] = list(temp_deque)
            elif warehouse_map[i][j + j_to_add] == "#":
                continue
        elif movement == "<":
            j_to_add = 1
            while warehouse_map[i][j - j_to_add] == "O":
                j_to_add += 1
            if warehouse_map[i][j - j_to_add] == ".":
                temp_deque = deque(warehouse_map[i][j - j_to_add : j + 1])
                temp_deque.rotate(-1)
                warehouse_map[i][j - j_to_add : j + 1] = list(temp_deque)
            elif warehouse_map[i][j - j_to_add] == "#":
                continue
        elif movement == "^":
            i_to_add = 1
            while warehouse_map[i - i_to_add][j] == "O":
                i_to_add += 1
            if warehouse_map[i - i_to_add][j] == ".":
                temp_deque = deque(
                    [warehouse_map[i - x][j] for x in range(i_to_add + 1)]
                )
                temp_deque.rotate(1)
                for x in range(i_to_add + 1):
                    warehouse_map[i - x][j] = temp_deque[x]
            elif warehouse_map[i - i_to_add][j] == "#":
                continue
        elif movement == "v":
            i_to_add = 1
            while warehouse_map[i + i_to_add][j] == "O":
                i_to_add += 1
            if warehouse_map[i + i_to_add][j] == ".":
                temp_deque = deque(
                    [warehouse_map[i + x][j] for x in range(i_to_add + 1)]
                )
                temp_deque.rotate(1)
                for x in range(i_to_add + 1):
                    warehouse_map[i + x][j] = temp_deque[x]
            elif warehouse_map[i + i_to_add][j] == "#":
                continue
        i = next_i
        j = next_j
    else:
        warehouse_map[i][j] = "."
        i = next_i
        j = next_j
        warehouse_map[i][j] = "@"

total = 0
for i in range(len(warehouse_map)):
    for j in range(len(warehouse_map[0])):
        if warehouse_map[i][j] == "O":
            total += 100 * i + j
print(total)

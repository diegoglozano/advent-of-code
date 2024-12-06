import numpy as np
import time

from pathlib import Path
from itertools import cycle

from rich.console import Console
from rich.table import Table
from rich import box

def get_rich_table(input_array, style_dict):
    table = Table(show_header=False, box=box.SIMPLE)
    for row in input_array:
        table.add_row(*map(lambda x: str(style_dict.get(x, x)), row))
    return table
    
DATA_PATH = Path('data')

with open(DATA_PATH / 'day_06.txt') as f:
    input_array = []
    lines = f.read().splitlines()
    for i, line in enumerate(lines):
        input_array.append(list(line))

input_array = (
    np.array(input_array)
)
original_input_array = input_array.copy()
STYLE_DICT = {
    '^': '[red]▲[/red]',
    '>': '[red]▶[/red]',
    'v': '[red]▼[/red]',
    '<': '[red]◀[/red]',
    '#': '[green]█[/green]',
    '.': '',
}

console = Console()

possible_directions = cycle('^>v<')
current_direction = next(possible_directions)

x = int(
    (input_array == current_direction)
    .argmax(axis=0)
    .max()
)
y = int(
    (input_array == current_direction)
    .argmax(axis=1)
    .max()
)
original_x = x
original_y = y
positions = set()
while True:
    table = get_rich_table(input_array, style_dict=STYLE_DICT)
    console.clear()
    console.print(table)
    if (x, y, current_direction) in positions:
        break
    try:
        positions.add((x, y, current_direction))
        if input_array[x, y] == '^':
            x_to_check = x - 1
            y_to_check = y
        elif input_array[x, y] == '>':
            x_to_check = x
            y_to_check = y + 1
        elif input_array[x, y] == 'v':
            x_to_check = x + 1
            y_to_check = y
        elif input_array[x, y] == '<':
            x_to_check = x
            y_to_check = y - 1
        if input_array[x_to_check, y_to_check] == '#':
            current_direction = next(possible_directions)
            input_array[x, y] = current_direction
        elif input_array[x_to_check, y_to_check] == '.':
            input_array[x, y] = '.'
            x = x_to_check
            y = y_to_check
            input_array[x, y] = current_direction
    except IndexError:
        break
    time.sleep(0.05)

print(
    len(set(position[0:2] for position in positions))
)

total = 0
for i in range(input_array.shape[0]):
    for j in range(input_array.shape[1]):
        # Start cycle
        possible_directions = cycle('^>v<')
        current_direction = next(possible_directions)
        x = original_x
        y = original_y
        # Copy original input array
        temp_input_array = original_input_array.copy()
        # If empty, change it by a wall
        if temp_input_array[i, j] == '.':
            temp_input_array[i, j] = '#'
            # Start loop
            stucked = False
            positions = set()
            while not stucked:
                if (x, y, current_direction) in positions:
                    total += 1
                    stucked = True
                else:
                    try:
                        positions.add((x, y, current_direction))
                        if temp_input_array[x, y] == '^':
                            x_to_check = x - 1
                            y_to_check = y
                        elif temp_input_array[x, y] == '>':
                            x_to_check = x
                            y_to_check = y + 1
                        elif temp_input_array[x, y] == 'v':
                            x_to_check = x + 1
                            y_to_check = y
                        elif temp_input_array[x, y] == '<':
                            x_to_check = x
                            y_to_check = y - 1
                        if x_to_check < 0 or y_to_check < 0:
                            temp_input_array[i, j] = '.'
                            stucked = True
                        else:
                            if temp_input_array[x_to_check, y_to_check] == '#':
                                current_direction = next(possible_directions)
                                temp_input_array[x, y] = current_direction
                            elif temp_input_array[x_to_check, y_to_check] == '.':
                                temp_input_array[x, y] = '.'
                                x = x_to_check
                                y = y_to_check
                                temp_input_array[x, y] = current_direction
                    except IndexError:
                        temp_input_array[i, j] = '.'
                        stucked = True
print(total)
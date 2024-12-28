import re

from pathlib import Path
from itertools import combinations


def bits_to_int(s: str) -> int:
    return int(s, 2)


DATA_PATH = Path("data")

OPERATORS = {
    "AND": lambda x, y: x & y,
    "OR": lambda x, y: x | y,
    "XOR": lambda x, y: x ^ y,
}

with open(DATA_PATH / "day_24_toy_3.txt") as f:
    raw_values, connections = f.read().split("\n\n")

raw_values = raw_values.splitlines()
connections = connections.splitlines()

raw_values = {key: int(value) for key, value in (x.split(": ") for x in raw_values)}
connections = {
    tuple(re.split("\s(OR|AND|XOR|->)\s", connection)): {} for connection in connections
}

values = raw_values.copy()
while True:
    for connection, attrs in connections.items():
        first_operator, operator, second_operator, _, into = connection
        if (
            first_operator in values
            and second_operator in values
            and not attrs.get("result")
        ):
            result = OPERATORS[operator](
                values[first_operator], values[second_operator]
            )
            values[into] = result
            connections[connection]["result"] = True

    if all(attrs.get("result") for attrs in connections.values()):
        break


sorted_bits = sorted(
    [(key, value) for key, value in values.items() if key.startswith("z")], reverse=True
)
sorted_bits = "".join(str(value) for key, value in sorted_bits)
print(bits_to_int(sorted_bits))

N_SWAPS = 2

swaps = list(combinations(range(len(connections)), 2))

for i1, i2 in swaps:
    values = raw_values.copy()
    new_connections = connections.copy()
    key1 = list(new_connections.keys())[i1]
    key2 = list(new_connections.keys())[i2]
    new_connections[key1], new_connections[key2] = (
        new_connections[key2],
        new_connections[key1],
    )
    while True:
        for connection, attrs in new_connections.items():
            first_operator, operator, second_operator, _, into = connection
            if (
                first_operator in values
                and second_operator in values
                and not attrs.get("result")
            ):
                result = OPERATORS[operator](
                    values[first_operator], values[second_operator]
                )
                values[into] = result
                new_connections[connection]["result"] = True

        if all(attrs.get("result") for attrs in new_connections.values()):
            break

x_values = sorted(
    [(key, value) for key, value in values.items() if key.startswith("x")], reverse=True
)
y_values = sorted(
    [(key, value) for key, value in values.items() if key.startswith("y")], reverse=True
)
z_values = sorted(
    [(key, value) for key, value in values.items() if key.startswith("z")], reverse=True
)

x_values = "".join(str(value) for key, value in x_values)
y_values = "".join(str(value) for key, value in y_values)
z_values = "".join(str(value) for key, value in z_values)

x_values = bits_to_int(x_values)
y_values = bits_to_int(y_values)
z_values = bits_to_int(z_values)

if x_values + y_values == z_values:
    print(i1, i2)

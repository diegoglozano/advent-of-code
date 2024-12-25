import re
from pathlib import Path


def bits_to_int(s: str) -> int:
    return int(s, 2)


DATA_PATH = Path("data")

OPERATORS = {
    "AND": lambda x, y: x & y,
    "OR": lambda x, y: x | y,
    "XOR": lambda x, y: x ^ y,
}

with open(DATA_PATH / "day_24.txt") as f:
    values, connections = f.read().split("\n\n")

values = values.splitlines()
connections = connections.splitlines()

values = {key: int(value) for key, value in (x.split(": ") for x in values)}
connections = {
    tuple(re.split("\s(OR|AND|XOR|->)\s", connection)): {} for connection in connections
}

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

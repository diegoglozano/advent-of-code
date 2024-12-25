import numpy as np

from pathlib import Path
from itertools import product

DATA_PATH = Path("data")


def is_key_or_lock(schema):
    if all(cell == "#" for cell in schema[0]):
        return "lock"
    else:
        return "key"


def key_is_compatible_with_lock(key, lock):
    pass


with open(DATA_PATH / "day_25.txt") as f:
    schematics = f.read().split("\n\n")

schematics = [schematic.splitlines() for schematic in schematics]
schematics_key_lock = {i: is_key_or_lock(schema) for i, schema in enumerate(schematics)}

keys = [key for key, value in schematics_key_lock.items() if value == "key"]
locks = [lock for lock, value in schematics_key_lock.items() if value == "lock"]

schematics = np.array([[list(row) for row in group] for group in schematics])

total = 0
for key, lock in product(keys, locks):
    key_array = (schematics[key] == "#").sum(axis=0) - 1
    lock_array = (schematics[lock] == "#").sum(axis=0) - 1
    total += ((key_array + lock_array) <= 5).all()

print(total)

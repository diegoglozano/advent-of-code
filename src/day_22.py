import polars as pl

from pathlib import Path

"""
In particular, each buyer's secret number evolves into the next secret number in the sequence via the following process:

Calculate the result of multiplying the secret number by 64. Then, mix this result into the secret number. Finally, prune the secret number.
Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer. Then, mix this result into the secret number. Finally, prune the secret number.
Calculate the result of multiplying the secret number by 2048. Then, mix this result into the secret number. Finally, prune the secret number.
Each step of the above process involves mixing and pruning:

To mix a value into the secret number, calculate the bitwise XOR of the given value and the secret number. Then, the secret number becomes the result of that operation. (If the secret number is 42 and you were to mix 15 into the secret number, the secret number would become 37.)
To prune the secret number, calculate the value of the secret number modulo 16777216. Then, the secret number becomes the result of that operation. (If the secret number is 100000000 and you were to prune the secret number, the secret number would become 16113920.)
"""

DATA_PATH = Path("data")
with open(DATA_PATH / "day_22.txt") as f:
    data = [int(x) for x in f.read().strip().splitlines()]


class SecretNumber:
    def __init__(self, secret_number: int) -> None:
        self.secret_number = secret_number

    def mix(self, a: int, b: int):
        self.secret_number = a ^ b

    def prune(self):
        self.secret_number = self.secret_number % 16777216

    def evolve(self) -> int:
        self.mix(self.secret_number, self.secret_number * 64)
        self.prune()
        self.mix(self.secret_number, self.secret_number // 32)
        self.prune()
        self.mix(self.secret_number, self.secret_number * 2048)
        self.prune()


results = {}
for number in data:
    secret_number = SecretNumber(number)
    for i in range(2000):
        secret_number.evolve()
    results[number] = secret_number.secret_number

print(sum(results.values()))


results = {}
data = [123]
for number in data:
    results[str(number)] = []
    secret_number = SecretNumber(number)
    for i in range(10):
        results[str(number)].append(int(str(secret_number.secret_number)[-1]))
        secret_number.evolve()

print(pl.DataFrame(results).with_columns(pl.all().diff()))

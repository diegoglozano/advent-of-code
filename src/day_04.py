import numpy as np

from pathlib import Path


DATA_PATH = Path('data')

with open(DATA_PATH / 'day_04.txt') as f:
    input_array = []
    lines = f.read().splitlines()
    for i, line in enumerate(lines):
        input_array.append(list(line))

input_array = (
    np.array(input_array)
)
print(input_array)
n_rows = input_array.shape[0]
n_cols = input_array.shape[1]

WORD = 'XMAS'
PAD = 4
total = 0
padded_input_array = np.pad(input_array, ((PAD, PAD), (PAD, PAD)), 'constant', constant_values='.')
for i in range(PAD, n_rows + PAD):
    for j in range(PAD, n_cols + PAD):
        if padded_input_array[i, j] == WORD[0]:
            if all(padded_input_array[i-k, j] == WORD[k] for k in range(len(WORD))):
                total += 1
            if all(padded_input_array[i+k, j] == WORD[k] for k in range(len(WORD))):
                total += 1
            if all(padded_input_array[i, j-k] == WORD[k] for k in range(len(WORD))):
                total += 1
            if all(padded_input_array[i, j+k] == WORD[k] for k in range(len(WORD))):
                total += 1
            if all(padded_input_array[i-k, j-k] == WORD[k] for k in range(len(WORD))):
                total += 1
            if all(padded_input_array[i-k, j+k] == WORD[k] for k in range(len(WORD))):
                total += 1
            if all(padded_input_array[i+k, j-k] == WORD[k] for k in range(len(WORD))):
                total += 1
            if all(padded_input_array[i+k, j+k] == WORD[k] for k in range(len(WORD))):
                total += 1
print(total)

total = 0
for i in range(PAD, n_rows + PAD):
    for j in range(PAD, n_cols + PAD):
        if padded_input_array[i, j] == 'A':
            if (
                    (padded_input_array[i-1, j-1] == 'M')
                    and (padded_input_array[i+1, j-1] == 'M')
                    and (padded_input_array[i-1, j+1] == 'S')
                    and (padded_input_array[i+1, j+1] == 'S')
                ):
                total += 1
            if (
                    (padded_input_array[i-1, j-1] == 'S')
                    and (padded_input_array[i+1, j-1] == 'S')
                    and (padded_input_array[i-1, j+1] == 'M')
                    and (padded_input_array[i+1, j+1] == 'M')
                ):
                total += 1
            if (
                    (padded_input_array[i-1, j-1] == 'M')
                    and (padded_input_array[i+1, j-1] == 'S')
                    and (padded_input_array[i-1, j+1] == 'M')
                    and (padded_input_array[i+1, j+1] == 'S')
                ):
                total += 1
            if (
                    (padded_input_array[i-1, j-1] == 'S')
                    and (padded_input_array[i+1, j-1] == 'M')
                    and (padded_input_array[i-1, j+1] == 'S')
                    and (padded_input_array[i+1, j+1] == 'M')
                ):
                total += 1

print(total)
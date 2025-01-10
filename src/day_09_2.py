from pathlib import Path
from itertools import count
from pprint import pprint


# function to define if all dots in a list are at the end
def all_dots_at_end(lst):
    n_dots_in_list = sum(map(lambda x: x == ".", lst))
    return sum(map(lambda x: x == ".", lst[-n_dots_in_list:])) == n_dots_in_list


DATA_PATH = Path("data")

with open(DATA_PATH / "day_09_toy.txt") as f:
    disk = f.read()

representation = []
is_file = True
for i, digit in enumerate(disk):
    if is_file:
        representation.extend([str(i // 2)] * int(digit))
    else:
        representation.extend(["."] * int(digit))
    is_file = not is_file

len_representation = len(representation)
# print(representation)
for i in count():
    if all_dots_at_end(representation):
        break

    flag_blocks = list(map(lambda x: x != ".", representation))
    first_space = flag_blocks.index(False)
    last_file = len_representation - 1 - list(reversed(flag_blocks)).index(True)

    value_to_insert = representation.pop(last_file)
    representation.pop(first_space)
    representation.insert(first_space, value_to_insert)
    representation.insert(len_representation - 1, ".")
    if i == 1:
        break

checksum = sum(int(block) * i for i, block in enumerate(representation) if block != ".")
print(checksum)

new_disk = [
    [
        # representation
        i // 2 if i % 2 == 0 else ".",
        # number of times
        int(block),
        # flag (disk or space)
        True if i % 2 == 0 else False,
        # checked (initially False)
        False if i % 2 == 0 else True,
    ]
    for i, block in enumerate(disk)
]

pprint(new_disk)

for i in count():
    # print("".join([
    #     str(block[0]) * block[1]
    #     for block in new_disk
    # ]))
    right_index = [
        i
        for i, (representation, n_times, flag, checked) in enumerate(new_disk)
        if flag and not checked
    ]
    if len(right_index) > 0:
        right_index = right_index[-1]
        right_value = new_disk[right_index]
        # print(f"Right value {right_value} found at index {right_index}")
        temp = [
            (i, (representation, n_times, flag, checked))
            for i, (representation, n_times, flag, checked) in enumerate(new_disk)
            if not flag and n_times >= right_value[1] and i < right_index
            # if not flag and n_times >= len(str(right_value[0])) * right_value[1] and i < right_index
        ]
        # Mark as checked
        new_disk[right_index][3] = True
        if len(temp) > 0:
            left_index, left_value = temp[0]

            difference = left_value[1] - right_value[1]

            new_disk.pop(right_index)
            new_disk.insert(right_index, [".", right_value[1], False, True])
            new_disk.pop(left_index)
            new_disk.insert(left_index, [right_value[0], right_value[1], True, True])
            if difference > 0:
                new_disk.insert(left_index + 1, [".", difference, False, True])
    else:
        break

new_representation = [str(block[0]) * block[1] for block in new_disk]
print(new_representation)

checksum_2 = sum(
    int(block) * i for i, block in enumerate(new_representation) if block != "."
)

print(checksum_2)
# 89223535126 too low
# 116939635378 too low

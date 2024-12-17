import polars as pl

from pathlib import Path
from time import perf_counter


# function to define if all dots in a list are at the end
def all_dots_at_end(lst):
    n_dots_in_list = sum(map(lambda x: x == ".", lst))
    return sum(map(lambda x: x == ".", lst[-n_dots_in_list:])) == n_dots_in_list


DATA_PATH = Path("data")

start = perf_counter()
df = pl.read_csv(
    DATA_PATH / "day_09.txt",
    has_header=False,
    new_columns=["disk_map"],
    schema_overrides={
        "disk_map": pl.Utf8,
    },
)

df_blocks = (
    df.with_columns(pl.col("disk_map").cast(pl.Utf8).str.split(""))
    .explode("disk_map")
    .with_columns(
        pl.col("disk_map").cast(pl.Int64),
        pl.int_range(0, pl.len()).mod(2).alias("flag"),
    )
    .with_columns(
        pl.when(
            pl.col("flag") == 0,
        )
        .then(
            pl.lit(1),
        )
        .otherwise(None)
        .cum_sum()
        .sub(1)
        .alias("index"),
    )
    .with_columns(
        pl.when(
            pl.col("flag") == 0,
        )
        .then(pl.col("index").repeat_by(pl.col("disk_map")))
        .otherwise(pl.lit(".").repeat_by(pl.col("disk_map")))
        .alias("n"),
    )
    .explode("n")
    .filter(
        pl.col("n").is_not_null(),
    )
)

blocks = df_blocks["n"].to_list()
i = 0
while True:
    flag_blocks = list(map(lambda x: x != ".", blocks))
    len_blocks = len(blocks)
    index_to_insert = flag_blocks.index(False)
    index_to_substitute = len_blocks - 1 - (list(reversed(flag_blocks)).index(True))

    value_to_insert = blocks.pop(index_to_substitute)
    blocks.pop(index_to_insert)
    blocks.insert(index_to_insert, value_to_insert)
    blocks.insert(len_blocks - 1, ".")

    if all_dots_at_end(blocks):
        break
    i += 1
print(f"Solved in {i} iterations")

print(
    pl.DataFrame(
        {
            "blocks": blocks,
        }
    )
    .filter(
        pl.col("blocks") != ".",
    )
    .cast({"blocks": pl.Int64})
    .with_row_index()
    .select((pl.col("blocks") * pl.col("index")).alias("filesystem_checksum"))[
        "filesystem_checksum"
    ]
    .sum()
)
end = perf_counter()
print(f"Elapsed time: {end - start}")

blocks = df_blocks["n"].to_list()
flag_blocks = list(map(lambda x: x != ".", blocks))

print(blocks)
print(flag_blocks)


def find_last_dot_index(lst, start_index):
    next_value = lst[start_index]
    while next_value == ".":
        start_index += 1
        next_value = lst[start_index]
    return start_index


start_index_to_insert = blocks.index(".")
last_index_to_insert = find_last_dot_index(blocks, start_index_to_insert)
last_index_to_replace = len_blocks - 1 - list(reversed(flag_blocks)).index(True)
start_index_to_replace = blocks.index(blocks[last_index_to_replace])

print(f"Start index to insert: {start_index_to_insert}")
print(f"Last index to insert: {last_index_to_insert}")
print(f"First index to replace: {start_index_to_replace}")
print(f"Last index to replace: {last_index_to_replace}")
print(blocks[start_index_to_insert:last_index_to_insert])
print(blocks[start_index_to_replace : last_index_to_replace + 1])

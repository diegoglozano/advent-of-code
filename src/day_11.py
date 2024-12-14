import polars as pl

from tqdm import tqdm
from time import perf_counter
from pathlib import Path


DATA_PATH = Path("data")

df = (
    pl.read_csv(
        DATA_PATH / "day_11_toy.txt",
        has_header=False,
        new_columns=["stones"],
    )
    .with_columns(pl.col("stones").str.split(" "))
    .explode("stones")
    .with_columns(pl.col("stones").cast(pl.Int64))
)
print(df)

start = perf_counter()
for _ in tqdm(range(25)):
    it_start = perf_counter()
    df = (
        df.with_columns(
            pl.when(
                pl.col("stones") == 0,
            )
            .then(
                pl.lit("is_zero"),
            )
            .when(
                pl.col("stones").cast(pl.Utf8).str.len_chars().mod(2) == 0,
            )
            .then(
                pl.lit("has_even_length"),
            )
            .otherwise(
                pl.lit("other"),
            )
            .alias("flag")
        )
        .with_columns(
            pl.when(
                pl.col("flag") == "is_zero",
            )
            .then(pl.concat_list(pl.lit(1)))
            .when(
                pl.col("flag") == "has_even_length",
            )
            .then(pl.col("stones").cast(pl.Utf8).str.split(""))
            .otherwise(
                pl.concat_list(
                    pl.col("stones") * pl.lit(2024),
                ),
            )
            .alias("stones")
        )
        .with_columns(
            pl.col("stones").list.len().alias("len"),
        )
        .with_columns(
            pl.when(
                pl.col("flag") == "has_even_length",
            )
            .then(
                pl.concat_list(
                    pl.col("stones").list.slice(0, pl.col("len") / 2).list.join(""),
                    pl.col("stones")
                    .list.slice(pl.col("len") / 2, pl.col("len"))
                    .list.join(""),
                )
            )
            .otherwise(
                pl.col("stones"),
            )
            .alias("stones")
        )
        .explode("stones")
        .cast({"stones": pl.Int64})
        # .group_by('stones')
        # .agg(pl.len().alias('n'))
    )
    it_end = perf_counter()
    print(f"Iteration {_} time: {it_end - it_start}")
    print(f"- df shape: {df.shape[0]}")
    print(df)
    break

end = perf_counter()
print(df.select("n").sum().item())
print(df.shape[0])
print(f"Time: {end - start}")

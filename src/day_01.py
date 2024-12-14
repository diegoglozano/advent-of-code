import polars as pl

from pathlib import Path

DATA_PATH = Path("data")

df = (
    pl.read_csv(
        DATA_PATH / "day_01.txt",
        has_header=False,
    )
    .with_columns(pl.col("column_1").str.replace("\s+", " ").str.split(" "))
    .select(
        pl.col("column_1").list.get(0).cast(pl.Int64).alias("first"),
        pl.col("column_1").list.get(1).cast(pl.Int64).alias("second"),
    )
)

print(df.select((pl.col("first").sort() - pl.col("second").sort()).abs().sum()).item())

print(
    df.select("first")
    .join(
        df.select("second"),
        left_on="first",
        right_on="second",
        how="inner",
        coalesce=False,
    )
    .group_by("first")
    .agg(
        pl.len().alias("count"),
    )
    .select((pl.col("first") * pl.col("count")).sum())
    .item()
)

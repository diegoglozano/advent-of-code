import polars as pl

from pathlib import Path


DATA_PATH = Path("data")


print(
    pl.read_csv(
        DATA_PATH / "day_13.txt",
        has_header=False,
        separator="*",
        new_columns=["machine"],
    )
    .with_columns(
        pl.col("machine").is_null().cum_sum().alias("id_machine"),
    )
    .filter(
        pl.col("machine").is_not_null(),
    )
    .with_columns(
        pl.col("machine")
        .str.extract_groups(
            r"(?<type>Button A|Button B|Prize)\: X[\+\=](?<X>\d+), Y[\+\=](?<Y>\d+)"
        )
        .alias("values")
    )
    .unnest("values")
    .cast({"X": pl.Int64, "Y": pl.Int64})
    .pivot(
        index="id_machine",
        on="type",
        values=("X", "Y"),
    )
    # Second part
    .with_columns(
        pl.col("X_Prize") + 10000000000000,
        pl.col("Y_Prize") + 10000000000000,
    )
    .with_columns(
        (
            (
                pl.col("X_Button A") * pl.col("Y_Prize")
                - pl.col("Y_Button A") * pl.col("X_Prize")
            )
            / (
                pl.col("Y_Button B") * pl.col("X_Button A")
                - pl.col("Y_Button A") * pl.col("X_Button B")
            )
        ).alias("num_B"),
    )
    .with_columns(
        (
            (pl.col("X_Prize") - pl.col("X_Button B") * pl.col("num_B"))
            / pl.col("X_Button A")
        ).alias("num_A"),
    )
    .filter(
        pl.col("num_B") == pl.col("num_B").cast(pl.Int64),
        pl.col("num_A") == pl.col("num_A").cast(pl.Int64),
        # First part
        # pl.col("num_A") <= 100,
        # pl.col("num_B") <= 100,
    )
    .with_columns(
        (pl.col("num_A") * 3 + pl.col("num_B") * 1).alias("cost"),
    )["cost"]
    .sum()
)

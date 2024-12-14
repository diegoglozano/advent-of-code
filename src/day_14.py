import polars as pl
import matplotlib.pyplot as plt

from pathlib import Path


pl.Config(set_tbl_rows=12)
DATA_PATH = Path("data")
IMG_PATH = Path("img")

IS_SECOND_PART = False
X_LEN = 101  # 11 # wide
Y_LEN = 103  # 7 # tall

df = (
    pl.read_csv(
        DATA_PATH / "day_14.txt",
        has_header=False,
        separator=".",
        new_columns=["configurations"],
    )
    .with_columns(
        pl.col("configurations")
        .str.extract_groups(
            "p=(?<x_position>\d+),(?<y_position>\d+) v=(?<x_velocity>-?\d+),(?<y_velocity>-?\d+)",
        )
        .alias("extract")
    )
    .unnest("extract")
    .select(
        pl.all().exclude("configurations").cast(pl.Int64),
    )
)

# Change range for 2nd part
for i in range(101 * 103 if IS_SECOND_PART else 100):
    df = df.with_columns(
        (pl.col("x_position") + pl.col("x_velocity")).mod(X_LEN).alias("x_position"),
        (pl.col("y_position") + pl.col("y_velocity")).mod(Y_LEN).alias("y_position"),
    )
    if IS_SECOND_PART:
        temp = (
            df.with_columns(
                pl.lit(1).alias("representation"),
            )
            .pivot(
                index="y_position",
                on="x_position",
                values="representation",
                aggregate_function="first",
            )
            .pipe(
                lambda df_: (
                    df_.with_columns(
                        *(
                            pl.lit(None).alias(f"{i}")
                            for i in range(Y_LEN)
                            if str(i) not in df_.columns
                        )
                    )
                )
            )
            .pipe(
                lambda df_: (
                    df_.select(
                        "y_position",
                        *sorted(df_.drop("y_position").columns, key=int),
                    )
                )
            )
            .sort("y_position")
            .drop("y_position")
            .to_numpy()
        )

        fig, ax = plt.subplots()
        ax.matshow(temp)
        fig.savefig(IMG_PATH / "day_14" / f"iteration_{i}.png")

print(
    df.filter(
        pl.col("x_position") != (X_LEN // 2),
    )
    .filter(
        pl.col("y_position") != (Y_LEN // 2),
    )
    .with_columns(
        pl.when(
            pl.col("x_position") < (X_LEN // 2),
            pl.col("y_position") < (Y_LEN // 2),
        )
        .then(0)
        .when(
            pl.col("x_position") < (X_LEN // 2),
            pl.col("y_position") > (Y_LEN // 2),
        )
        .then(1)
        .when(
            pl.col("x_position") > (X_LEN // 2),
            pl.col("y_position") < (Y_LEN // 2),
        )
        .then(2)
        .otherwise(3)
        .alias("quadrant"),
    )
    .sort("y_position", "x_position")
    .with_columns(
        pl.len().over("x_position", "y_position").alias("n"),
    )
    .group_by("quadrant")
    .agg(pl.len().alias("count"))["count"]
    .cum_prod()[-1]
)

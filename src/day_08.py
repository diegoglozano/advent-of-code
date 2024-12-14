import polars as pl
import numpy as np

from rich.console import Console
from rich.table import Table

from pathlib import Path

STYLE_DICT = {
    "#": "[green]#[/green]",
    "0": "[red]0[/red]",
    "A": "[blue]A[/blue]",
}

DATA_PATH = Path("data")

antennas = (
    pl.read_csv(
        DATA_PATH / "day_08_toy.txt",
        has_header=False,
    )
    .with_row_index("row")
    .select(
        pl.col("row").cast(pl.Int64),
        pl.col("column_1").str.split("").alias("value"),
    )
    .explode("value")
    .select(
        "row",
        pl.cum_count("value").over("row").sub(1).cast(pl.Int64).alias("column"),
        "value",
    )
)
n_rows, n_cols = antennas["row"].max() + 1, antennas["column"].max() + 1

antennas = antennas.filter(
    pl.col("value") != ".",
)

print(
    antennas.join_where(
        antennas,
        pl.col("value") == pl.col("value_right"),
    )
    # Drop same antenna
    .filter(
        pl.col("row") != pl.col("row_right"),
        pl.col("column") != pl.col("column_right"),
    )
    # Only combination where left antenna is in the left
    .filter(
        pl.col("column") <= pl.col("column_right"),
    )
    .with_columns(
        pl.col("row").sub(pl.col("row_right")).alias("row_distance"),
        pl.col("column").sub(pl.col("column_right")).alias("column_distance"),
    )
    .with_columns(
        (pl.col("row") + pl.col("row_distance")).alias("antinode_1_row"),
        (pl.col("column") + pl.col("column_distance")).alias("antinode_1_column"),
        (pl.col("row_right") - pl.col("row_distance")).alias("antinode_2_row"),
        (pl.col("column_right") - pl.col("column_distance")).alias("antinode_2_column"),
    )
    .pipe(
        lambda x: (
            pl.concat(
                [
                    x.select(
                        pl.col("antinode_1_row").alias("antinode_row"),
                        pl.col("antinode_1_column").alias("antinode_column"),
                    ),
                    x.select(
                        pl.col("antinode_2_row").alias("antinode_row"),
                        pl.col("antinode_2_column").alias("antinode_column"),
                    ),
                ],
                how="vertical",
            )
        )
    )
    .filter(
        (
            pl.col("antinode_row").is_between(0, n_rows - 1)
            & pl.col("antinode_column").is_between(0, n_cols - 1)
        )
    )
    .n_unique()
)
temp = (
    antennas.join_where(
        antennas,
        pl.col("value") == pl.col("value_right"),
    )
    # Drop same antenna
    .filter(
        pl.col("row") != pl.col("row_right"),
        pl.col("column") != pl.col("column_right"),
    )
    # Only combination where left antenna is in the left
    .filter(
        pl.col("column") <= pl.col("column_right"),
    )
    .with_columns(
        pl.col("row").sub(pl.col("row_right")).alias("row_distance"),
        pl.col("column").sub(pl.col("column_right")).alias("column_distance"),
    )
    .with_columns(
        (pl.col("row") + pl.col("row_distance").mul(i)).alias(f"antinode_1{i}_row")
        for i in range(1, n_rows)
    )
    .with_columns(
        (pl.col("column") + pl.col("column_distance").mul(i)).alias(
            f"antinode_1{i}_column"
        )
        for i in range(1, n_cols)
    )
    .with_columns(
        (pl.col("row_right") - pl.col("row_distance").mul(i)).alias(
            f"antinode_2{i}_row"
        )
        for i in range(1, n_rows)
    )
    .with_columns(
        (pl.col("column_right") - pl.col("column_distance").mul(i)).alias(
            f"antinode_2{i}_column"
        )
        for i in range(1, n_cols)
    )
    .pipe(
        lambda x: (
            pl.concat(
                [
                    *[
                        x.select(
                            pl.col(f"antinode_1{i}_row").alias("antinode_row"),
                            pl.col(f"antinode_1{i}_column").alias("antinode_column"),
                        )
                        for i in range(1, n_rows)
                    ],
                    *[
                        x.select(
                            pl.col(f"antinode_2{i}_row").alias("antinode_row"),
                            pl.col(f"antinode_2{i}_column").alias("antinode_column"),
                        )
                        for i in range(1, n_rows)
                    ],
                ],
                how="vertical",
            )
        )
    )
    .filter(
        (
            pl.col("antinode_row").is_between(0, n_rows - 1)
            & pl.col("antinode_column").is_between(0, n_cols - 1)
        )
    )
)
temp = temp.with_columns(
    pl.lit("#").alias("value"),
)
print(
    pl.concat(
        [
            antennas.select("row", "column"),
            temp.select(
                pl.col("antinode_row").alias("row"),
                pl.col("antinode_column").alias("column"),
            ),
        ],
        how="vertical",
    ).n_unique()
)

# (Only for toy example!) representation in console
console = Console()
table = Table(show_header=False, show_lines=True)

rich_table = np.empty((n_rows, n_cols), dtype=str)
for values in temp.to_dicts():
    rich_table[values["antinode_row"], values["antinode_column"]] = values["value"]
for values in antennas.to_dicts():
    rich_table[values["row"], values["column"]] = values["value"]
for row in rich_table:
    table.add_row(*map(lambda x: str(STYLE_DICT.get(x, "")), row))
console.print(table)

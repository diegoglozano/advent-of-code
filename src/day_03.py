import polars as pl

from pathlib import Path

DATA_PATH = Path('data')


with open(DATA_PATH / 'day_03.txt') as f:
    lines = f.read()

df = pl.DataFrame([lines])
print(
    df
    .with_columns(
        pl
        .col('column_0')
        .str.extract_all('(mul\(\d+,\d+\))')
    )
    .explode('column_0')
    .with_columns(
        pl
        .col('column_0')
        .str.extract_groups(r'mul\((\d+),(\d+)\)')
    )
    .unnest('column_0')
    .select(
        pl
        .col('1')
        .cast(pl.Int64)
        .mul(pl.col('2').cast(pl.Int64))
    )
    .sum()
    .item()
)

print(
    df
    .with_columns(
        pl
        .col('column_0')
        .str.extract_all(
            r'''(?xi)
                (
                    do\(\)|mul\(\d+,\d+\)|don't\(\)
                )
            '''
        )
    )
    .explode('column_0')
    .with_columns(
        pl
        .when(
            pl.col('column_0') == 'do()'
        )
        .then(1)
        .when(
            pl.col('column_0') == "don't()"
        )
        .then(0)
        .otherwise(None)
        .forward_fill()
        # Implicit do at the beginning
        .fill_null(1)
        .alias('flag')
    )
    .filter(
        pl.col('column_0').is_in(['do()', "don't()"]).not_()
    )
    .with_columns(
        pl
        .col('column_0')
        .str.extract_groups(r'mul\((\d+),(\d+)\)')
    )
    .unnest('column_0')
    .select(
        pl.col('1').cast(pl.Int64)
        * pl.col('2').cast(pl.Int64)
        * pl.col('flag')
    )
    .sum()
    .item()
)
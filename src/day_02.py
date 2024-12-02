import polars as pl

from pathlib import Path

DATA_PATH = Path('data')

def compute_conditions(df: pl.DataFrame, col: str) -> pl.DataFrame:
    return (
        df
        .with_columns(
            pl
            .col(col)
            .list.diff()
            .list.eval(
                pl.element() >= 0
            )
            .list.all()
            .alias('is_monotone_asc'),
            pl
            .col(col)
            .list.diff()
            .list.eval(
                pl.element() <= 0
            )
            .list.all()
            .alias('is_monotone_desc'),
            pl
            .col(col)
            .list.diff()
            .list.eval(
                pl.element().abs().is_between(1, 3, closed='both')
            )
            .list.all()
            .alias('bounded_diff')
        )
    )

def compute_is_safe(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df
        .with_columns(
            pl
            .col('is_monotone_asc')
            .or_(
                pl.col('is_monotone_desc')
            )
            .and_(
                pl.col('bounded_diff')
            )
            .alias('is_safe'),
        )
    )

df = (
    pl
    .read_csv(
        DATA_PATH / 'day_02.txt',
        has_header=False,
    )
    .with_columns(
        pl
        .col('column_1')
        .str.split(' ')
        .cast(pl.List(pl.Int64))
    )
)

print(
    df
    .pipe(compute_conditions, col='column_1')
    .pipe(compute_is_safe)
    .select('is_safe')
    .sum()
    .item()
)

print(
    df
    .with_columns(
        pl
        .int_ranges(
            0,
            pl.col('column_1').list.len()
        )
        .alias('index_to_drop'),
    )
    .with_row_index()
    .explode('index_to_drop')
    .with_columns(
        pl
        .int_ranges(
            0,
            pl.col('column_1').list.len()
        )
        .list.set_difference(
            pl.concat_list(pl.col('index_to_drop'))
        )
        .list.sort()
        .alias('index_to_get'),
    )
    .drop('index_to_drop')
    .unique(maintain_order=True)
    .with_columns(
        pl.int_range(pl.len()).over('index').alias('index_2')
    )
    .explode('index_to_get')
    .with_columns(
        pl.col('column_1').list.get(pl.col('index_to_get')),
    )
    .group_by('index', 'index_2', maintain_order=True)
    .agg(
        pl.col('column_1'),
    )
    .pipe(compute_conditions, col='column_1')
    .pipe(compute_is_safe)
    .group_by('index')
    .agg(
        pl.col('is_safe').any(),
    )
    .select('is_safe')
    .sum()
    .item()
)

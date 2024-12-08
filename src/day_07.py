import polars as pl

from itertools import product
from operator import add, mul
from pathlib import Path

DATA_PATH = Path('data')

POSSIBLE_OPERATORS = {
    '+': add,
    '*': mul,
    '||': lambda x, y: int(f'{x}{y}'), # only for 2nd part
}

df = (
    pl
    .read_csv(
        DATA_PATH / 'day_07.txt',
        has_header=False,
        separator=':',
        new_columns=['value', 'equation'],
    )
    .with_row_index('index_equation')
    .with_columns(
        pl
        .col('equation')
        .str.replace('\s+', ' ')
        .str.strip_chars()
        .str.split(' ')
        .cast(pl.List(pl.Int64))
    )
    .with_columns(
        pl
        .col('equation')
        .list.len()
        .sub(1)
        .alias('n_combinations'),
    )
)

max_repeat = df['n_combinations'].max()
combinations = (
    pl
    .DataFrame({
        'combinations': [
            p
            for r
            in range(1, max_repeat + 1)
            for p
            in product(POSSIBLE_OPERATORS.keys(), repeat=r)
        ]
    })
    .with_columns(
        pl
        .col('combinations')
        .list.len()
        .alias('n_combinations'),
    )
    .with_columns(
        pl
        .cum_count('n_combinations')
        .over('n_combinations')
        .sub(1)
        .alias('index_combination'),
    )
)
# print(
#     df
#     .join(
#         combinations,
#         on='n_combinations',
#         how='left',
#     )
#     .filter(
#         pl.col('index_equation') == 1
#     )
#     .explode('combinations')
#     .with_columns(
#         pl
#         .cum_count('index_combination')
#         .over('index_equation', 'index_combination')
#         .sub(1)
#         .alias('index_operator'),
#     )
#     .rename({'combinations': 'operator'})
#     .with_columns(
#         pl
#         .when(
#             pl.col('operator') == '+'
#         )
#         .then(
#             pl.col('equation').list.get(pl.col('index_operator'))
#             + pl.col('equation').list.get(pl.col('index_operator') + 1)
#         )
#         .otherwise(
#             pl.col('equation').list.get(pl.col('index_operator'))
#             * pl.col('equation').list.get(pl.col('index_operator') + 1)
#         )
#         .alias('result')
#     )
# )

operations = (
    df
    .join(
        combinations,
        on='n_combinations',
        how='left',
    )
)
operations_pydict = (
    operations
    .select(
        'index_equation',
        'index_combination',
        'equation',
        pl
        .col('combinations')
        .alias('operators'),
    )
    .to_dict(as_series=False)
)

results = {}
for id_equation, id_combination, equation, operation in zip(
        operations_pydict['index_equation'],
        operations_pydict['index_combination'],
        operations_pydict['equation'],
        operations_pydict['operators'],
    ):
    acc = POSSIBLE_OPERATORS[operation[0]](equation[0], equation[1])
    # print(f'initial accumulator: {equation[0]}{operation[0]}{equation[1]}={acc}')
    for i in range(1, len(equation) - 1):
        # print(f'current iteration: {acc}{operation[i]}{equation[i + 1]}')
        acc = POSSIBLE_OPERATORS[operation[i]](acc, equation[i + 1])
        # print(f'={acc}')
    results[(id_equation,id_combination)] = acc

print(
    df
    .select(
        pl.col('index_equation').cast(pl.Int64),
        'value',
    )
    .join(
        pl
        .DataFrame({
            'indexes': results.keys(),
            'results': results.values(),
        })
        .select(
            pl.col('indexes').list.get(0).alias('index_equation'),
            pl.col('indexes').list.get(1).alias('index_combination'),
            'results',
        ),
        how='left',
        left_on='index_equation',
        right_on='index_equation',
    )
    .group_by(
        'index_equation',
    )
    .agg(
        pl.col('value').first(),
        (pl.col('value') == pl.col('results'))
        .any()
        .alias('is_valid'),
    )
    .filter(
        pl
        .col('is_valid')
    )
    ['value']
    .sum()
)
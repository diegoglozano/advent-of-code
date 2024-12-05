import polars as pl

from pathlib import Path

pl.Config(fmt_table_cell_list_len=10)
DATA_PATH = Path('data')

with open(DATA_PATH / 'day_05_toy.txt') as f:
    rules, pages = f.read().split('\n\n')

rules = (
    pl
    .DataFrame(rules.split('\n'))
    .select(
        pl
        .col('column_0')
        .str.split('|')
        .cast(pl.List(pl.Int64))
        .alias('rules')
    )
    .with_row_index('rule_index')
)

pages = (
    pl
    .DataFrame(pages.split('\n'))
    .select(
        pl
        .col('column_0')
        .str.split(',')
        .cast(pl.List(pl.Int64))
        .alias('pages')
    )
    .with_row_index('page_index')
)


print(rules)
print(pages)
correct_indexes = (
    pages
    .join(
        rules,
        how='cross',
    )
    .select(
        'page_index',
        'rule_index',
        'pages',
        'rules',
    )
    .explode('pages')
    .with_columns(
        pl
        .int_range(pl.len())
        .over('page_index', 'rule_index')
        .alias('page_index_2')
    )
    .with_columns(
        (pl.col('pages') == pl.col('rules').list.get(0))
        .alias('match_1'),
        (pl.col('pages') == pl.col('rules').list.get(1))
        .alias('match_2'),
    )
    .filter(
        pl.col('match_1') | pl.col('match_2')
    )
    .filter(
        pl
        .len()
        .over('page_index', 'rule_index')
        == 2
    )
    .group_by('page_index', 'rule_index', maintain_order=True)
    .agg(
        pl.col('pages'),
        pl.col('rules').first(),
        pl.col('match_1').first(),
        pl.col('match_2').last(),
    )
    .with_columns(
        (pl.col('match_1') & pl.col('match_2'))
        .alias('is_match')
    )
    .group_by('page_index')
    .agg(
        pl.col('is_match').all()
    )
    .filter(pl.col('is_match'))
)

print(
    pages
    .join(
        correct_indexes,
        on='page_index',
        how='inner',
    )
    .select(
        pl
        .col('pages')
        .list.get(
            pl.col('pages').list.len()
            // 2
        )
    )
    .sum()
    .item()
)

print(
    pages
    .join(
        correct_indexes,
        on='page_index',
        how='anti',
    )
    .join(
        rules,
        how='cross',
    )
    .select(
        'page_index',
        'rule_index',
        'pages',
        'rules',
    )
    .explode('pages')
    .with_columns(
        pl
        .int_range(pl.len())
        .over('page_index', 'rule_index')
        .alias('page_index_2')
    )
    .with_columns(
        (pl.col('pages') == pl.col('rules').list.get(0))
        .alias('match_1'),
        (pl.col('pages') == pl.col('rules').list.get(1))
        .alias('match_2'),
    )
        .filter(
        pl.col('match_1') | pl.col('match_2')
    )
    .filter(
        pl
        .len()
        .over('page_index', 'rule_index')
        == 2
    )
    .group_by('page_index', 'rule_index', maintain_order=True)
    .agg(
        pl.col('pages'),
        pl.col('rules').first(),
        pl.col('match_1').first(),
        pl.col('match_2').last(),
    )
    .with_columns(
        (pl.col('match_1').not_() & pl.col('match_2').not_())
        .alias('is_match')
    )
    .filter(
        pl.col('is_match'),
    )
)

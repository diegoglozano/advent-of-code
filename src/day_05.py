import polars as pl
import networkx as nx

from pathlib import Path

pl.Config(fmt_table_cell_list_len=10)
DATA_PATH = Path("data")

with open(DATA_PATH / "day_05.txt") as f:
    rules, pages = f.read().split("\n\n")

rules = (
    pl.DataFrame(rules.split("\n"))
    .select(pl.col("column_0").str.split("|").cast(pl.List(pl.Int64)).alias("rules"))
    .with_row_index("rule_index")
)

pages = (
    pl.DataFrame(pages.split("\n"))
    .select(pl.col("column_0").str.split(",").cast(pl.List(pl.Int64)).alias("pages"))
    .with_row_index("page_index")
)

correct_indexes = (
    pages.join(
        rules,
        how="cross",
    )
    .select(
        "page_index",
        "rule_index",
        "pages",
        "rules",
    )
    .explode("pages")
    .with_columns(
        pl.int_range(pl.len()).over("page_index", "rule_index").alias("page_index_2")
    )
    .with_columns(
        (pl.col("pages") == pl.col("rules").list.get(0)).alias("match_1"),
        (pl.col("pages") == pl.col("rules").list.get(1)).alias("match_2"),
    )
    .filter(pl.col("match_1") | pl.col("match_2"))
    .filter(pl.len().over("page_index", "rule_index") == 2)
    .group_by("page_index", "rule_index", maintain_order=True)
    .agg(
        pl.col("pages"),
        pl.col("rules").first(),
        pl.col("match_1").first(),
        pl.col("match_2").last(),
    )
    .with_columns((pl.col("match_1") & pl.col("match_2")).alias("is_match"))
    .group_by("page_index")
    .agg(pl.col("is_match").all())
    .filter(pl.col("is_match"))
)

print(
    pages.join(
        correct_indexes,
        on="page_index",
        how="inner",
    )
    .select(pl.col("pages").list.get(pl.col("pages").list.len() // 2))
    .sum()
    .item()
)

incorrect_pages = pages.join(
    correct_indexes,
    on="page_index",
    how="anti",
)["pages"].to_list()
corrected_pages = []
for page in incorrect_pages:
    subset_nodes = set(page)
    edges = (
        rules.explode("rules")
        .with_row_index("rule_index_2")
        .filter(pl.col("rules").is_in(subset_nodes))
        .filter(pl.len().over("rule_index") == 2)
        .group_by("rule_index")
        .agg(
            pl.col("rules").sort_by("rule_index_2"),
        )["rules"]
        .to_list()
    )
    G = nx.DiGraph()
    for src_node, dst_node in edges:
        G.add_edge(src_node, dst_node)
    sorted_rules = {value: i for i, value in enumerate(nx.topological_sort(G))}
    corrected_pages.append(
        sorted(
            page,
            key=lambda x: sorted_rules.get(x, float("inf")),
        )
    )

sorted_incorrect_pages = (
    pl.DataFrame(
        {
            "pages": corrected_pages,
        }
    )
    .select(pl.col("pages").list.get(pl.col("pages").list.len() // 2))
    .sum()
    .item()
)

print(sorted_incorrect_pages)

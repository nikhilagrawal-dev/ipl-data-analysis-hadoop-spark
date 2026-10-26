"""
Toss Analytics Module.
Analyzes the impact of coin tosses on IPL match outcomes:
- Toss decision breakdown (bat vs field) overall and by season
- Toss winner match victory rate (toss winner == match winner)
- Win rates when electing to bat first vs field first
- Denominator rule: Excludes matches with no result from win rate calculations
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    lit,
    when,
    sum as _sum,
    count as _count,
    round as _round,
)


def get_toss_decision_summary(matches_df: DataFrame) -> DataFrame:
    """
    Computes overall toss outcomes and win rates based on toss decision.

    Metrics:
    - total_tosses: Total tosses won
    - elected_field: Count of times choosing to field first
    - elected_bat: Count of times choosing to bat first
    - toss_winner_match_wins: Matches where toss winner also won the match
    - toss_winner_win_pct: (toss_winner_match_wins / matches_with_result) * 100
    - field_first_win_pct: Win rate when toss winner elects to field
    - bat_first_win_pct: Win rate when toss winner elects to bat
    """
    # Only consider matches with a declared result for percentage denominators
    decided = matches_df.filter(col("is_result_declared"))

    summary = (
        decided.agg(
            _count(lit(1)).alias("total_decided_matches"),
            _sum(when(col("toss_winner") == col("winner"), lit(1)).otherwise(lit(0))).alias("toss_winner_match_wins"),
            _sum(when(col("toss_decision") == "field", lit(1)).otherwise(lit(0))).alias("elected_field"),
            _sum(when(col("toss_decision") == "bat", lit(1)).otherwise(lit(0))).alias("elected_bat"),
            _sum(
                when((col("toss_decision") == "field") & (col("toss_winner") == col("winner")), lit(1)).otherwise(lit(0))
            ).alias("won_toss_and_fielded_won_match"),
            _sum(
                when((col("toss_decision") == "bat") & (col("toss_winner") == col("winner")), lit(1)).otherwise(lit(0))
            ).alias("won_toss_and_batted_won_match"),
        )
        .withColumn(
            "toss_winner_win_pct",
            _round((col("toss_winner_match_wins") / col("total_decided_matches")) * 100, 2),
        )
        .withColumn(
            "field_first_win_pct",
            _round((col("won_toss_and_fielded_won_match") / col("elected_field")) * 100, 2),
        )
        .withColumn(
            "bat_first_win_pct",
            _round((col("won_toss_and_batted_won_match") / col("elected_bat")) * 100, 2),
        )
    )

    return summary


def get_toss_trends_by_season(matches_df: DataFrame) -> DataFrame:
    """
    Computes toss decisions and toss-to-win conversion rates season-by-season.
    Shows the historical shift towards fielding first in T20 cricket.
    """
    decided = matches_df.filter(col("is_result_declared"))

    season_toss = (
        decided.groupBy("season_year")
        .agg(
            _count(lit(1)).alias("matches"),
            _sum(when(col("toss_decision") == "field", lit(1)).otherwise(lit(0))).alias("chose_field"),
            _sum(when(col("toss_decision") == "bat", lit(1)).otherwise(lit(0))).alias("chose_bat"),
            _sum(when(col("toss_winner") == col("winner"), lit(1)).otherwise(lit(0))).alias("toss_winner_wins"),
            _sum(
                when((col("toss_decision") == "field") & (col("toss_winner") == col("winner")), lit(1)).otherwise(lit(0))
            ).alias("chose_field_and_won"),
            _sum(
                when((col("toss_decision") == "bat") & (col("toss_winner") == col("winner")), lit(1)).otherwise(lit(0))
            ).alias("chose_bat_and_won"),
        )
        .withColumn(
            "field_preference_pct",
            _round((col("chose_field") / col("matches")) * 100, 1),
        )
        .withColumn(
            "toss_win_match_win_pct",
            _round((col("toss_winner_wins") / col("matches")) * 100, 1),
        )
        .withColumn(
            "field_win_pct",
            _round((col("chose_field_and_won") / when(col("chose_field") > 0, col("chose_field")).otherwise(lit(1))) * 100, 1),
        )
        .withColumn(
            "bat_win_pct",
            _round((col("chose_bat_and_won") / when(col("chose_bat") > 0, col("chose_bat")).otherwise(lit(1))) * 100, 1),
        )
        .orderBy("season_year")
    )

    return season_toss

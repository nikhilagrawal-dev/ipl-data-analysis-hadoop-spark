"""
Team Analytics Module.
Computes comprehensive team performance metrics using PySpark DataFrames and Spark SQL:
- Overall team records (matches played, wins, losses, ties, no-results, win percentage)
- Season-wise team performance
- Pairwise Head-to-Head records
- Win percentage correctly excluding no-results from the denominator
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    lit,
    when,
    sum as _sum,
    count as _count,
    round as _round,
    least,
    greatest,
)


def get_team_overall_performance(matches_df: DataFrame) -> DataFrame:
    """
    Computes overall team standings across all IPL matches.

    Metrics:
    - matches_played: Total matches played (as team1 or team2)
    - wins: Matches won by the team
    - losses: Matches with a declared result where the team lost
    - ties: Matches where scores tied in 20 overs (went to Super Over)
    - no_results: Matches abandoned / no result declared
    - win_percentage: (wins / (matches_played - no_results)) * 100
    """
    # Create two views: team as team1 and team as team2
    t1 = matches_df.select(
        col("team1").alias("team"),
        when(col("winner") == col("team1"), lit(1)).otherwise(lit(0)).alias("win"),
        when(
            (col("is_result_declared")) & (col("winner") != col("team1")),
            lit(1),
        ).otherwise(lit(0)).alias("loss"),
        when(col("result") == "tie", lit(1)).otherwise(lit(0)).alias("tie"),
        when(~col("is_result_declared"), lit(1)).otherwise(lit(0)).alias("no_result"),
    )

    t2 = matches_df.select(
        col("team2").alias("team"),
        when(col("winner") == col("team2"), lit(1)).otherwise(lit(0)).alias("win"),
        when(
            (col("is_result_declared")) & (col("winner") != col("team2")),
            lit(1),
        ).otherwise(lit(0)).alias("loss"),
        when(col("result") == "tie", lit(1)).otherwise(lit(0)).alias("tie"),
        when(~col("is_result_declared"), lit(1)).otherwise(lit(0)).alias("no_result"),
    )

    all_teams = t1.union(t2)

    perf = (
        all_teams.groupBy("team")
        .agg(
            _count(lit(1)).alias("matches_played"),
            _sum("win").alias("wins"),
            _sum("loss").alias("losses"),
            _sum("tie").alias("ties"),
            _sum("no_result").alias("no_results"),
        )
        .withColumn(
            "win_percentage",
            _round(
                (col("wins") / when(col("matches_played") - col("no_results") > 0, col("matches_played") - col("no_results")).otherwise(lit(1))) * 100,
                2,
            ),
        )
        .orderBy(col("wins").desc(), col("win_percentage").desc())
    )

    return perf


def get_team_season_performance(matches_df: DataFrame) -> DataFrame:
    """
    Computes season-by-season performance for each team.
    """
    t1 = matches_df.select(
        col("season_year"),
        col("team1").alias("team"),
        when(col("winner") == col("team1"), lit(1)).otherwise(lit(0)).alias("win"),
        when(
            (col("is_result_declared")) & (col("winner") != col("team1")),
            lit(1),
        ).otherwise(lit(0)).alias("loss"),
        when(~col("is_result_declared"), lit(1)).otherwise(lit(0)).alias("no_result"),
    )

    t2 = matches_df.select(
        col("season_year"),
        col("team2").alias("team"),
        when(col("winner") == col("team2"), lit(1)).otherwise(lit(0)).alias("win"),
        when(
            (col("is_result_declared")) & (col("winner") != col("team2")),
            lit(1),
        ).otherwise(lit(0)).alias("loss"),
        when(~col("is_result_declared"), lit(1)).otherwise(lit(0)).alias("no_result"),
    )

    all_season_teams = t1.union(t2)

    season_perf = (
        all_season_teams.groupBy("season_year", "team")
        .agg(
            _count(lit(1)).alias("matches_played"),
            _sum("win").alias("wins"),
            _sum("loss").alias("losses"),
            _sum("no_result").alias("no_results"),
        )
        .withColumn(
            "win_percentage",
            _round(
                (col("wins") / when(col("matches_played") - col("no_results") > 0, col("matches_played") - col("no_results")).otherwise(lit(1))) * 100,
                2,
            ),
        )
        .orderBy("season_year", col("wins").desc())
    )

    return season_perf


def get_team_head_to_head(matches_df: DataFrame) -> DataFrame:
    """
    Computes pairwise Head-to-Head records between every pair of teams.
    Canonical ordering (team_a < team_b) prevents duplicate inverse pairs.
    """
    h2h_base = matches_df.select(
        least(col("team1"), col("team2")).alias("team_a"),
        greatest(col("team1"), col("team2")).alias("team_b"),
        col("winner"),
        col("result"),
        col("is_result_declared"),
    )

    h2h = (
        h2h_base.groupBy("team_a", "team_b")
        .agg(
            _count(lit(1)).alias("matches_played"),
            _sum(when(col("winner") == col("team_a"), lit(1)).otherwise(lit(0))).alias("team_a_wins"),
            _sum(when(col("winner") == col("team_b"), lit(1)).otherwise(lit(0))).alias("team_b_wins"),
            _sum(when(col("result") == "tie", lit(1)).otherwise(lit(0))).alias("ties"),
            _sum(when(~col("is_result_declared"), lit(1)).otherwise(lit(0))).alias("no_results"),
        )
        .withColumn(
            "team_a_win_pct",
            _round((col("team_a_wins") / when(col("matches_played") - col("no_results") > 0, col("matches_played") - col("no_results")).otherwise(lit(1))) * 100, 2),
        )
        .withColumn(
            "team_b_win_pct",
            _round((col("team_b_wins") / when(col("matches_played") - col("no_results") > 0, col("matches_played") - col("no_results")).otherwise(lit(1))) * 100, 2),
        )
        .orderBy(col("matches_played").desc())
    )

    return h2h

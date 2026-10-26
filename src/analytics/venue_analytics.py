"""
Venue Analytics Module.
Computes stadium-level insights:
- Matches hosted per venue
- Average and highest 1st innings totals
- Team performance and win rates at each venue
- Sensible minimum-match thresholds for fair venue comparisons
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    lit,
    when,
    sum as _sum,
    count as _count,
    avg as _avg,
    max as _max,
    round as _round,
)


def get_venue_summary(
    matches_df: DataFrame,
    deliveries_df: DataFrame,
    min_matches: int = 5,
) -> DataFrame:
    """
    Computes venue scoring characteristics and match outcomes.

    Metrics:
    - matches_hosted: Total matches played at the venue
    - avg_first_innings_score: Average 1st innings total at the venue
    - highest_first_innings_score: Record highest 1st innings score at venue
    - chasing_wins: Matches won by the team batting second (result == 'wickets')
    - defending_wins: Matches won by the team batting first (result == 'runs')
    - chasing_win_pct: (chasing_wins / (chasing_wins + defending_wins)) * 100
    """
    # 1. First innings score per match
    first_inn = (
        deliveries_df.filter(col("inning") == 1)
        .groupBy("match_id")
        .agg(_sum("total_runs").alias("first_inn_runs"))
    )

    # Join with matches
    matches_with_score = matches_df.join(
        first_inn,
        matches_df.id == first_inn.match_id,
        how="left",
    )

    venue_stats = (
        matches_with_score.groupBy("venue", "city")
        .agg(
            _count("id").alias("matches_hosted"),
            _round(_avg("first_inn_runs"), 1).alias("avg_first_innings_score"),
            _max("first_inn_runs").alias("highest_first_innings_score"),
            _sum(when(col("result") == "wickets", lit(1)).otherwise(lit(0))).alias("chasing_wins"),
            _sum(when(col("result") == "runs", lit(1)).otherwise(lit(0))).alias("defending_wins"),
            _sum(when(col("result") == "tie", lit(1)).otherwise(lit(0))).alias("ties"),
        )
        .filter(col("matches_hosted") >= min_matches)
        .withColumn(
            "chasing_win_pct",
            _round(
                (col("chasing_wins") / when(col("chasing_wins") + col("defending_wins") > 0, col("chasing_wins") + col("defending_wins")).otherwise(lit(1))) * 100,
                2,
            ),
        )
        .orderBy(col("matches_hosted").desc())
    )

    return venue_stats


def get_team_performance_by_venue(
    matches_df: DataFrame,
    min_venue_matches: int = 5,
) -> DataFrame:
    """
    Computes team win records broken down by venue.
    Useful to identify fortress venues and venue specialists.
    """
    t1 = matches_df.select(
        col("venue"),
        col("team1").alias("team"),
        when(col("winner") == col("team1"), lit(1)).otherwise(lit(0)).alias("win"),
        when(col("is_result_declared"), lit(1)).otherwise(lit(0)).alias("decided_match"),
    )

    t2 = matches_df.select(
        col("venue"),
        col("team2").alias("team"),
        when(col("winner") == col("team2"), lit(1)).otherwise(lit(0)).alias("win"),
        when(col("is_result_declared"), lit(1)).otherwise(lit(0)).alias("decided_match"),
    )

    all_venue_teams = t1.union(t2)

    team_venue = (
        all_venue_teams.groupBy("venue", "team")
        .agg(
            _count(lit(1)).alias("matches_played"),
            _sum("win").alias("wins"),
            _sum("decided_match").alias("decided_matches"),
        )
        .filter(col("matches_played") >= min_venue_matches)
        .withColumn(
            "win_percentage",
            _round((col("wins") / when(col("decided_matches") > 0, col("decided_matches")).otherwise(lit(1))) * 100, 2),
        )
        .orderBy(col("venue"), col("wins").desc())
    )

    return team_venue

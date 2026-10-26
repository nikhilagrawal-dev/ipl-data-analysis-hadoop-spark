"""
Season and Scoring Analytics Module.
Computes season-level trends and over-phase breakdowns:
- Season summary (matches, total runs, avg/max first-innings scores, 4s, 6s, dot ball %)
- Scoring by over phase (Powerplay, Middle, Death)
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    lit,
    when,
    sum as _sum,
    count as _count,
    round as _round,
    avg as _avg,
    max as _max,
)


def get_season_summary(matches_df: DataFrame, deliveries_df: DataFrame) -> DataFrame:
    """
    Computes aggregated performance and scoring trends for each IPL season.

    Metrics:
    - total_matches: Total matches scheduled in that season
    - total_runs: Total runs scored across all innings
    - avg_first_innings_score: Average 1st innings total for the season
    - max_first_innings_score: Highest 1st innings score of the season
    - total_fours: Total 4s hit in the season
    - total_sixes: Total 6s hit in the season
    - boundary_run_pct: % of total runs coming from boundaries ((4*fours + 6*sixes)/total_runs)*100
    - dot_ball_pct: % of all deliveries resulting in dot balls
    """
    # 1. First innings match totals
    first_inn_scores = (
        deliveries_df.filter(col("inning") == 1)
        .groupBy("match_id")
        .agg(_sum("total_runs").alias("first_inn_runs"))
    )

    # Join with matches to attach season_year
    first_inn_with_season = first_inn_scores.join(
        matches_df.select("id", "season_year"),
        first_inn_scores.match_id == matches_df.id,
        how="inner",
    )

    season_first_inn = (
        first_inn_with_season.groupBy("season_year")
        .agg(
            _round(_avg("first_inn_runs"), 1).alias("avg_first_innings_score"),
            _max("first_inn_runs").alias("max_first_innings_score"),
        )
    )

    # 2. Season match counts
    season_matches = (
        matches_df.groupBy("season_year")
        .agg(_count("id").alias("total_matches"))
    )

    # 3. Deliveries joined with matches for season metrics
    deliv_with_season = deliveries_df.join(
        matches_df.select(col("id").alias("m_id"), "season_year"),
        deliveries_df.match_id == col("m_id"),
        how="inner",
    )

    season_batting = (
        deliv_with_season.groupBy("season_year")
        .agg(
            _sum("total_runs").alias("total_runs"),
            _sum("is_four").alias("total_fours"),
            _sum("is_six").alias("total_sixes"),
            _sum("is_dot_ball").alias("total_dots"),
            _count(lit(1)).alias("total_deliveries"),
        )
        .withColumn(
            "boundary_run_pct",
            _round(((col("total_fours") * 4 + col("total_sixes") * 6) / col("total_runs")) * 100, 2),
        )
        .withColumn(
            "dot_ball_pct",
            _round((col("total_dots") / col("total_deliveries")) * 100, 2),
        )
    )

    # 4. Combine all season metrics
    summary = (
        season_matches.join(season_batting, on="season_year", how="inner")
        .join(season_first_inn, on="season_year", how="left")
        .select(
            "season_year",
            "total_matches",
            "total_runs",
            "avg_first_innings_score",
            "max_first_innings_score",
            "total_fours",
            "total_sixes",
            "boundary_run_pct",
            "dot_ball_pct",
        )
        .orderBy("season_year")
    )

    return summary


def get_over_phase_analytics(deliveries_df: DataFrame) -> DataFrame:
    """
    Computes scoring and wicket trends across match phases:
    - Powerplay (overs 0-5)
    - Middle (overs 6-14)
    - Death (overs 15-19)

    Metrics:
    - total_runs: Total runs scored in phase
    - total_wickets: Wickets lost in phase
    - legal_balls: Balls bowled excluding wides/no-balls
    - run_rate: runs / (legal_balls / 6.0)
    - boundary_pct: (fours + sixes) / legal_balls * 100
    - dot_ball_pct: dot_balls / total_balls * 100
    """
    legal_cond = ~col("extras_type").isin(["wides", "noballs"])

    phase_stats = (
        deliveries_df.groupBy("over_phase")
        .agg(
            _sum("total_runs").alias("total_runs"),
            _sum("is_wicket").alias("total_wickets"),
            _sum(col("is_four")).alias("fours"),
            _sum(col("is_six")).alias("sixes"),
            _sum(col("is_dot_ball")).alias("dot_balls"),
            _count(lit(1)).alias("total_balls"),
            _sum(when(legal_cond, lit(1)).otherwise(lit(0))).alias("legal_balls"),
        )
        .withColumn(
            "run_rate",
            _round(col("total_runs") / (col("legal_balls") / 6.0), 2),
        )
        .withColumn(
            "boundary_pct",
            _round(((col("fours") + col("sixes")) / col("total_balls")) * 100, 2),
        )
        .withColumn(
            "dot_ball_pct",
            _round((col("dot_balls") / col("total_balls")) * 100, 2),
        )
        .orderBy(
            when(col("over_phase") == "Powerplay", lit(1))
            .when(col("over_phase") == "Middle", lit(2))
            .otherwise(lit(3))
        )
    )

    return phase_stats

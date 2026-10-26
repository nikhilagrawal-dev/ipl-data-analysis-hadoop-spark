"""
Player Analytics Module.
Computes batting, bowling, and Player-of-the-Match awards:
- Batting: Total runs, innings, balls faced, strike rate, batting average, 4s, 6s, 50s, 100s, highest score
- Bowling: Wickets (strictly bowler-credited), legal overs, runs conceded (excluding fielding byes/legbyes), economy, average, strike rate, dot balls
- Player of the Match awards
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    lit,
    when,
    sum as _sum,
    count as _count,
    countDistinct as _countDistinct,
    round as _round,
    max as _max,
)

# Standard bowler-credited dismissals as defined by MCC Laws & IPL records
BOWLER_CREDITED_DISMISSALS = [
    "bowled",
    "caught",
    "caught and bowled",
    "lbw",
    "stumped",
    "hit wicket",
]


def get_top_run_scorers(
    deliveries_df: DataFrame,
    min_runs: int = 1000,
    top_n: int = 20,
) -> DataFrame:
    """
    Computes top run scorers with comprehensive batting metrics.

    Metrics & Exclusions:
    - total_runs: SUM(batsman_runs)
    - balls_faced: Balls faced excluding wides (wides are not faced by the batter)
    - dismissals: Times the batter was out (excludes 'retired hurt')
    - strike_rate: (total_runs / balls_faced) * 100
    - batting_avg: total_runs / NULLIF(dismissals, 0)
    - fours: Count of 4s
    - sixes: Count of 6s
    """
    # 1. Match-level innings scores for 50s, 100s, and highest score
    match_scores = (
        deliveries_df.groupBy("batter", "match_id")
        .agg(_sum("batsman_runs").alias("match_runs"))
    )

    milestones = (
        match_scores.groupBy("batter")
        .agg(
            _max("match_runs").alias("highest_score"),
            _sum(when(col("match_runs") >= 100, lit(1)).otherwise(lit(0))).alias("hundreds"),
            _sum(when((col("match_runs") >= 50) & (col("match_runs") < 100), lit(1)).otherwise(lit(0))).alias("fifties"),
        )
    )

    # 2. Dismissals count (batter is the one dismissed, and not 'retired hurt')
    dismissals = (
        deliveries_df.filter(
            (col("player_dismissed") == col("batter"))
            & (col("dismissal_kind") != "retired hurt")
            & (col("dismissal_kind") != "none")
        )
        .groupBy("batter")
        .agg(_count(lit(1)).alias("dismissals"))
    )

    # 3. Overall aggregate stats
    batting = (
        deliveries_df.groupBy("batter")
        .agg(
            _countDistinct("match_id").alias("matches_batted"),
            _sum("batsman_runs").alias("total_runs"),
            _sum(when(col("extras_type") != "wides", lit(1)).otherwise(lit(0))).alias("balls_faced"),
            _sum(col("is_four")).alias("fours"),
            _sum(col("is_six")).alias("sixes"),
            _sum(col("is_dot_ball")).alias("dot_balls_faced"),
        )
        .filter(col("total_runs") >= min_runs)
    )

    # 4. Join milestones and dismissals
    joined = (
        batting.join(milestones, on="batter", how="left")
        .join(dismissals, on="batter", how="left")
        .fillna({"dismissals": 0, "highest_score": 0, "hundreds": 0, "fifties": 0})
    )

    result = (
        joined.withColumn(
            "batting_avg",
            _round(
                col("total_runs") / when(col("dismissals") > 0, col("dismissals")).otherwise(lit(None)),
                2,
            ),
        )
        .withColumn(
            "strike_rate",
            _round(
                (col("total_runs") / when(col("balls_faced") > 0, col("balls_faced")).otherwise(lit(1))) * 100,
                2,
            ),
        )
        .orderBy(col("total_runs").desc())
        .limit(top_n)
    )

    return result


def get_top_wicket_takers(
    deliveries_df: DataFrame,
    min_wickets: int = 50,
    top_n: int = 20,
) -> DataFrame:
    """
    Computes top wicket takers with strict bowler-wicket exclusions.

    Rules & Metric Definitions:
    - wickets: Only dismissals credited to the bowler ('bowled', 'caught', 'caught and bowled',
      'lbw', 'stumped', 'hit wicket'). Run outs and retired hurts are excluded.
    - legal_balls: Balls bowled excluding wides and no-balls.
    - overs: legal_balls / 6.0
    - runs_conceded: Bowler-charged runs (total_runs minus fielding byes and legbyes).
    - economy: runs_conceded / (legal_balls / 6.0)
    - bowling_avg: runs_conceded / wickets
    - bowling_strike_rate: legal_balls / wickets
    """
    bowler_wickets_cond = col("dismissal_kind").isin(BOWLER_CREDITED_DISMISSALS)
    legal_ball_cond = ~col("extras_type").isin(["wides", "noballs"])

    # Conceded runs excludes byes and legbyes (fielding extras)
    runs_conceded_expr = when(col("extras_type").isin(["byes", "legbyes"]), col("batsman_runs")).otherwise(col("total_runs"))

    bowling = (
        deliveries_df.groupBy("bowler")
        .agg(
            _countDistinct("match_id").alias("matches_bowled"),
            _sum(when(legal_ball_cond, lit(1)).otherwise(lit(0))).alias("legal_balls"),
            _sum(when(bowler_wickets_cond, lit(1)).otherwise(lit(0))).alias("wickets"),
            _sum(runs_conceded_expr).alias("runs_conceded"),
            _sum(when((col("batsman_runs") == 0) & (col("extras_type") == "none"), lit(1)).otherwise(lit(0))).alias("dot_balls"),
        )
        .filter(col("wickets") >= min_wickets)
    )

    result = (
        bowling.withColumn(
            "overs",
            _round(col("legal_balls") / 6.0, 1),
        )
        .withColumn(
            "economy",
            _round(
                col("runs_conceded") / when(col("legal_balls") > 0, col("legal_balls") / 6.0).otherwise(lit(1)),
                2,
            ),
        )
        .withColumn(
            "bowling_avg",
            _round(
                col("runs_conceded") / when(col("wickets") > 0, col("wickets")).otherwise(lit(None)),
                2,
            ),
        )
        .withColumn(
            "bowling_strike_rate",
            _round(
                col("legal_balls") / when(col("wickets") > 0, col("wickets")).otherwise(lit(None)),
                2,
            ),
        )
        .orderBy(col("wickets").desc(), col("bowling_avg").asc())
        .limit(top_n)
    )

    return result


def get_player_of_match_counts(
    matches_df: DataFrame,
    top_n: int = 15,
) -> DataFrame:
    """
    Computes top Player of the Match awards.
    Excludes matches with no result ('None').
    """
    potm = (
        matches_df.filter(col("player_of_match") != "None")
        .groupBy("player_of_match")
        .agg(_count(lit(1)).alias("potm_awards"))
        .orderBy(col("potm_awards").desc())
        .limit(top_n)
    )
    return potm

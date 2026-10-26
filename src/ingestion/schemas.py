"""
Explicit PySpark Schemas for IPL Raw Datasets.
Defined based on actual inspection of matches.csv and deliveries.csv.
"""

from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
    DateType,
)


def get_raw_matches_schema() -> StructType:
    """
    Returns explicit StructType schema for raw matches.csv.
    """
    return StructType([
        StructField("id", IntegerType(), nullable=False),
        StructField("season", StringType(), nullable=False),
        StructField("city", StringType(), nullable=True),
        StructField("date", DateType(), nullable=False),
        StructField("match_type", StringType(), nullable=True),
        StructField("player_of_match", StringType(), nullable=True),
        StructField("venue", StringType(), nullable=False),
        StructField("team1", StringType(), nullable=False),
        StructField("team2", StringType(), nullable=False),
        StructField("toss_winner", StringType(), nullable=False),
        StructField("toss_decision", StringType(), nullable=False),
        StructField("winner", StringType(), nullable=True),
        StructField("result", StringType(), nullable=True),
        StructField("result_margin", IntegerType(), nullable=True),
        StructField("target_runs", IntegerType(), nullable=True),
        StructField("target_overs", DoubleType(), nullable=True),
        StructField("super_over", StringType(), nullable=True),
        StructField("method", StringType(), nullable=True),
        StructField("umpire1", StringType(), nullable=True),
        StructField("umpire2", StringType(), nullable=True),
    ])


def get_raw_deliveries_schema() -> StructType:
    """
    Returns explicit StructType schema for raw deliveries.csv.
    """
    return StructType([
        StructField("match_id", IntegerType(), nullable=False),
        StructField("inning", IntegerType(), nullable=False),
        StructField("batting_team", StringType(), nullable=False),
        StructField("bowling_team", StringType(), nullable=False),
        StructField("over", IntegerType(), nullable=False),
        StructField("ball", IntegerType(), nullable=False),
        StructField("batter", StringType(), nullable=False),
        StructField("bowler", StringType(), nullable=False),
        StructField("non_striker", StringType(), nullable=False),
        StructField("batsman_runs", IntegerType(), nullable=False),
        StructField("extra_runs", IntegerType(), nullable=False),
        StructField("total_runs", IntegerType(), nullable=False),
        StructField("extras_type", StringType(), nullable=True),
        StructField("is_wicket", IntegerType(), nullable=False),
        StructField("player_dismissed", StringType(), nullable=True),
        StructField("dismissal_kind", StringType(), nullable=True),
        StructField("fielder", StringType(), nullable=True),
    ])

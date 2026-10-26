"""
Data Preprocessing and Transformation Module.
Applies transparent, documented cleaning and standardization rules:
1. Imputes missing cities using deterministic venue-to-city mapping.
2. Normalizes seasons to 4-digit integers (season_year) while preserving season_raw.
3. Standardizes franchise names to canonical team names (preserving historical names).
4. Handles match outcome nulls (e.g., method null -> 'Regular', no-result matches).
5. Standardizes extras_type, dismissal_kind, and adds analytical ball flags.
6. Deduplicates records on primary keys.
"""

from typing import Dict
from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    when,
    lit,
    coalesce,
    trim,
    regexp_replace,
    split,
)


# Canonical franchise mapping to handle historical rebrands and spelling variants
TEAM_NAME_STANDARDIZATION: Dict[str, str] = {
    "Rising Pune Supergiants": "Rising Pune Supergiant",
    "Royal Challengers Bengaluru": "Royal Challengers Bangalore",
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
}

# Deterministic venue to city mapping for the 51 matches where city is NULL
VENUE_CITY_MAPPING: Dict[str, str] = {
    "Dubai International Cricket Stadium": "Dubai",
    "Sharjah Cricket Stadium": "Sharjah",
    "Sheikh Zayed Stadium": "Abu Dhabi",
    "Zayed Cricket Stadium, Abu Dhabi": "Abu Dhabi",
}


def standardize_team_expr(column_name: str):
    """Generates a PySpark Column expression to map a team to its canonical name."""
    expr = trim(col(column_name))
    for old_name, canonical_name in TEAM_NAME_STANDARDIZATION.items():
        expr = when(expr == old_name, lit(canonical_name)).otherwise(expr)
    return expr


def impute_city_expr(venue_col: str, city_col: str):
    """Imputes missing city using venue when city is null."""
    expr = col(city_col)
    for venue_name, city_name in VENUE_CITY_MAPPING.items():
        expr = when(expr.isNull() & (col(venue_col) == venue_name), lit(city_name)).otherwise(expr)
    return expr


def parse_season_year_expr(season_col: str):
    """
    Standardizes season representations:
    '2007/08' -> 2008
    '2009/10' -> 2010
    '2020/21' -> 2020
    '2014'    -> 2014
    """
    return (
        when(col(season_col) == "2007/08", lit(2008))
        .when(col(season_col) == "2009/10", lit(2010))
        .when(col(season_col) == "2020/21", lit(2020))
        .otherwise(split(col(season_col), "/").getItem(0).cast("int"))
    )


def clean_matches(df: DataFrame) -> DataFrame:
    """
    Cleans, standardizes, and enriches the raw matches DataFrame.
    """
    # 1. Deduplicate on match ID
    cleaned = df.dropDuplicates(["id"])

    # 2. Season parsing
    cleaned = (
        cleaned.withColumnRenamed("season", "season_raw")
        .withColumn("season_year", parse_season_year_expr("season_raw"))
    )

    # 3. Impute city from venue
    cleaned = cleaned.withColumn("city", impute_city_expr("venue", "city"))

    # 4. Standardize team names into canonical columns (preserve raw names)
    cleaned = (
        cleaned.withColumn("team1_raw", col("team1"))
        .withColumn("team2_raw", col("team2"))
        .withColumn("toss_winner_raw", col("toss_winner"))
        .withColumn("winner_raw", col("winner"))
        .withColumn("team1", standardize_team_expr("team1"))
        .withColumn("team2", standardize_team_expr("team2"))
        .withColumn("toss_winner", standardize_team_expr("toss_winner"))
        .withColumn("winner", when(col("winner").isNotNull(), standardize_team_expr("winner")).otherwise(lit("No Result")))
    )

    # 5. Outcome adjustments
    cleaned = (
        cleaned.withColumn("is_result_declared", when(col("result") == "no result", lit(False)).otherwise(lit(True)))
        .withColumn("is_super_over", when(col("super_over") == "Y", lit(True)).otherwise(lit(False)))
        .withColumn("method", coalesce(col("method"), lit("Regular")))
        .withColumn("result_margin", coalesce(col("result_margin"), lit(0)))
        .withColumn("player_of_match", coalesce(col("player_of_match"), lit("None")))
    )

    return cleaned


def clean_deliveries(df: DataFrame) -> DataFrame:
    """
    Cleans, standardizes, and enriches the raw deliveries DataFrame.
    """
    # 1. Deduplicate by primary ball key
    cleaned = df.dropDuplicates(["match_id", "inning", "over", "ball"])

    # 2. Standardize team names
    cleaned = (
        cleaned.withColumn("batting_team_raw", col("batting_team"))
        .withColumn("bowling_team_raw", col("bowling_team"))
        .withColumn("batting_team", standardize_team_expr("batting_team"))
        .withColumn("bowling_team", standardize_team_expr("bowling_team"))
    )

    # 3. Standardize nullable text columns
    cleaned = (
        cleaned.withColumn("extras_type", coalesce(col("extras_type"), lit("none")))
        .withColumn("player_dismissed", coalesce(col("player_dismissed"), lit("none")))
        .withColumn("dismissal_kind", coalesce(col("dismissal_kind"), lit("none")))
        .withColumn("fielder", coalesce(col("fielder"), lit("none")))
    )

    # 4. Derived ball performance features
    cleaned = (
        cleaned.withColumn("is_dot_ball", when((col("batsman_runs") == 0) & (col("extra_runs") == 0), lit(1)).otherwise(lit(0)))
        .withColumn("is_four", when(col("batsman_runs") == 4, lit(1)).otherwise(lit(0)))
        .withColumn("is_six", when(col("batsman_runs") == 6, lit(1)).otherwise(lit(0)))
        .withColumn("is_boundary", when((col("batsman_runs") == 4) | (col("batsman_runs") == 6), lit(1)).otherwise(lit(0)))
        .withColumn(
            "over_phase",
            when(col("over") < 6, lit("Powerplay"))
            .when(col("over") < 15, lit("Middle"))
            .otherwise(lit("Death"))
        )
    )

    return cleaned

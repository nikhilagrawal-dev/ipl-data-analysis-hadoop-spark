#!/usr/bin/env python3
"""
Test Preprocessing Module:
Verifies cleaning rules:
1. Imputation of missing city values from venue
2. Parsing and normalization of seasons into 4-digit season_year
3. Canonical franchise mapping
4. Proper enrichment flags on deliveries (dots, boundaries, over phases)
5. Successful Parquet readback from HDFS
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.spark_session import get_spark_session
from src.ingestion.loader import load_raw_matches, load_raw_deliveries, get_default_hdfs_uri
from src.preprocessing.cleaner import clean_matches, clean_deliveries


def test_matches_cleaning():
    print("Testing matches preprocessing rules...")
    spark = get_spark_session("TestMatchesClean")
    raw_df = load_raw_matches(spark)
    clean_df = clean_matches(raw_df)

    # 1. Row count preserved
    assert clean_df.count() == 1095

    # 2. Zero null cities
    null_cities = clean_df.filter(clean_df.city.isNull()).count()
    assert null_cities == 0, f"Expected 0 null cities after imputation, got {null_cities}"

    # 3. Season years within valid bounds (2008 - 2024)
    min_year = clean_df.selectExpr("min(season_year)").collect()[0][0]
    max_year = clean_df.selectExpr("max(season_year)").collect()[0][0]
    assert min_year == 2008, f"Expected min season_year 2008, got {min_year}"
    assert max_year == 2024, f"Expected max season_year 2024, got {max_year}"

    # 4. Canonical team name mapping
    has_old_delhi = clean_df.filter(clean_df.team1 == "Delhi Daredevils").count()
    assert has_old_delhi == 0, "Found unmapped 'Delhi Daredevils' in canonical team1"

    has_old_punjab = clean_df.filter(clean_df.team1 == "Kings XI Punjab").count()
    assert has_old_punjab == 0, "Found unmapped 'Kings XI Punjab' in canonical team1"

    print("✅ Matches cleaning assertions passed.")


def test_deliveries_cleaning():
    print("\nTesting deliveries preprocessing rules...")
    spark = get_spark_session("TestDeliveriesClean")
    raw_df = load_raw_deliveries(spark)
    clean_df = clean_deliveries(raw_df)

    # 1. Row count preserved
    assert clean_df.count() == 260920

    # 2. No null extras_type or dismissal_kind
    null_extras = clean_df.filter(clean_df.extras_type.isNull()).count()
    assert null_extras == 0, "Null extras_type found"

    null_dismissals = clean_df.filter(clean_df.dismissal_kind.isNull()).count()
    assert null_dismissals == 0, "Null dismissal_kind found"

    # 3. Verify over phases exist
    phases = [r["over_phase"] for r in clean_df.select("over_phase").distinct().collect()]
    assert set(phases) == {"Powerplay", "Middle", "Death"}

    print("✅ Deliveries cleaning assertions passed.")


def test_hdfs_parquet_persistence():
    print("\nTesting HDFS processed Parquet persistence...")
    spark = get_spark_session("TestParquetPersistence")
    hdfs_base = get_default_hdfs_uri()

    matches_df = spark.read.parquet(f"{hdfs_base}/ipl/processed/matches")
    deliveries_df = spark.read.parquet(f"{hdfs_base}/ipl/processed/deliveries")

    assert matches_df.count() == 1095
    assert deliveries_df.count() == 260920
    assert "season_year" in matches_df.columns
    assert "is_dot_ball" in deliveries_df.columns
    print("✅ HDFS Parquet persistence assertions passed.")


if __name__ == "__main__":
    test_matches_cleaning()
    test_deliveries_cleaning()
    test_hdfs_parquet_persistence()

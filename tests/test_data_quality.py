#!/usr/bin/env python3
"""
Test Data Quality Module:
Verifies that audit checks catch anomalies, duplicates, and correct null patterns.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.spark_session import get_spark_session
from src.ingestion.loader import load_raw_matches, load_raw_deliveries
from src.validation.data_quality import validate_matches_dataset, validate_deliveries_dataset


def test_matches_quality():
    print("Testing matches data quality audit...")
    spark = get_spark_session("TestMatchesQuality")
    df = load_raw_matches(spark)
    audit = validate_matches_dataset(df)

    assert audit["row_count"] == 1095
    assert audit["col_count"] == 20
    assert audit["duplicate_rows"] == 0
    assert audit["duplicate_ids"] == 0
    assert audit["null_counts"]["city"] == 51
    assert audit["null_counts"]["winner"] == 5
    assert audit["anomalies"]["negative_margins"] == 0
    assert len(audit["distinct_seasons"]) == 17
    print("✅ Matches data quality assertions passed.")


def test_deliveries_quality():
    print("\nTesting deliveries data quality audit...")
    spark = get_spark_session("TestDeliveriesQuality")
    df = load_raw_deliveries(spark)
    audit = validate_deliveries_dataset(df)

    assert audit["row_count"] == 260920
    assert audit["col_count"] == 17
    assert audit["duplicate_rows"] == 0
    assert audit["duplicate_ball_keys"] == 0
    assert audit["anomalies"]["negative_batsman_runs"] == 0
    assert audit["anomalies"]["negative_extra_runs"] == 0
    assert audit["anomalies"]["negative_total_runs"] == 0
    assert audit["anomalies"]["invalid_overs"] == 0
    assert audit["anomalies"]["invalid_balls"] == 0
    assert audit["anomalies"]["run_discrepancies"] == 0
    print("✅ Deliveries data quality assertions passed.")


if __name__ == "__main__":
    test_matches_quality()
    test_deliveries_quality()

#!/usr/bin/env python3
"""
Test Ingestion Module:
Verifies that matches.csv and deliveries.csv are successfully read from HDFS
with the correct schemas and record counts.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.spark_session import get_spark_session
from src.ingestion.loader import load_raw_matches, load_raw_deliveries


def test_matches_ingestion():
    print("Testing matches ingestion from HDFS...")
    spark = get_spark_session("TestMatchesIngestion")
    df = load_raw_matches(spark)

    count = df.count()
    cols = df.columns

    print(f"✔ Matches loaded: {count:,} rows, {len(cols)} columns")
    assert count == 1095, f"Expected 1,095 matches, got {count}"
    assert len(cols) == 20, f"Expected 20 columns, got {len(cols)}"
    assert "id" in cols
    assert "season" in cols
    assert "winner" in cols
    print("✅ Matches ingestion test passed.")


def test_deliveries_ingestion():
    print("\nTesting deliveries ingestion from HDFS...")
    spark = get_spark_session("TestDeliveriesIngestion")
    df = load_raw_deliveries(spark)

    count = df.count()
    cols = df.columns

    print(f"✔ Deliveries loaded: {count:,} rows, {len(cols)} columns")
    assert count == 260920, f"Expected 260,920 deliveries, got {count}"
    assert len(cols) == 17, f"Expected 17 columns, got {len(cols)}"
    assert "match_id" in cols
    assert "batter" in cols
    assert "total_runs" in cols
    print("✅ Deliveries ingestion test passed.")


if __name__ == "__main__":
    test_matches_ingestion()
    test_deliveries_ingestion()

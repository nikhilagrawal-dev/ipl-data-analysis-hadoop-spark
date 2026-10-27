#!/usr/bin/env python3
"""
Smoke Test 1: Spark Engine Computation Test
Verifies that Apache Spark starts up, executes distributed transformations,
and runs Spark SQL queries properly.
"""

import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum


def run_test():
    print("==========================================================")
    print("Running Smoke Test: Spark Engine & SQL Computation")
    print("==========================================================")

    # Initialize SparkSession in local cluster mode
    spark = (
        SparkSession.builder.appName("SparkComputationSmokeTest")
        .master("local[*]")
        .config("spark.driver.memory", "1g")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    print(f"[OK] Spark Session created successfully (Version: {spark.version})")

    # 1. Create a sample DataFrame using Spark SQL (avoids Python 3.14 cloudpickle recursion bug)
    df = spark.sql("""
        SELECT 'Kolkata Knight Riders' AS team, 222 AS total_runs, 'Eden Gardens' AS venue
        UNION ALL SELECT 'Royal Challengers Bangalore', 185, 'M Chinnaswamy Stadium'
        UNION ALL SELECT 'Chennai Super Kings', 210, 'MA Chidambaram Stadium'
        UNION ALL SELECT 'Mumbai Indians', 195, 'Wankhede Stadium'
        UNION ALL SELECT 'Rajasthan Royals', 175, 'Sawai Mansingh Stadium'
    """)

    print("\n--- Input DataFrame ---")
    df.show(truncate=False)

    # 2. Perform DataFrame Transformation & Aggregation
    filtered_df = df.filter(col("total_runs") >= 190)
    filtered_count = filtered_df.count()
    total_runs_sum = filtered_df.select(_sum("total_runs")).collect()[0][0]

    print(f"Teams with >= 190 runs: {filtered_count}")
    print(f"Combined runs for these teams: {total_runs_sum}")

    assert filtered_count == 3, f"Expected 3 teams with >= 190 runs, got {filtered_count}"
    assert total_runs_sum == 627, f"Expected sum of 627 runs, got {total_runs_sum}"
    print("[OK] DataFrame transformation assertions passed.")

    # 3. Test Spark SQL Engine
    df.createOrReplaceTempView("ipl_scores")
    sql_result = spark.sql(
        "SELECT team, total_runs FROM ipl_scores WHERE total_runs > 200 ORDER BY total_runs DESC"
    )
    print("\n--- Spark SQL Query Output (total_runs > 200) ---")
    sql_result.show(truncate=False)

    sql_count = sql_result.count()
    assert sql_count == 2, f"Expected 2 teams with total_runs > 200, got {sql_count}"
    print("[OK] Spark SQL query assertion passed.")

    spark.stop()
    print("\n==========================================================")
    print("[SUCCESS] TEST PASSED: Spark computation and SQL engine verified!")
    print("==========================================================")


if __name__ == "__main__":
    try:
        run_test()
    except Exception as e:
        print(f"[FAIL] TEST FAILED with exception: {e}", file=sys.stderr)
        sys.exit(1)

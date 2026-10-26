#!/usr/bin/env python3
"""
Smoke Test 1: Spark Engine Computation Test
Verifies that Apache Spark starts up, executes distributed transformations,
and runs Spark SQL queries properly.
"""

import sys
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

    print(f"✔ Spark Session created successfully (Version: {spark.version})")

    # 1. Create a sample in-memory DataFrame
    data = [
        ("Kolkata Knight Riders", 222, "Eden Gardens"),
        ("Royal Challengers Bangalore", 185, "M Chinnaswamy Stadium"),
        ("Chennai Super Kings", 210, "MA Chidambaram Stadium"),
        ("Mumbai Indians", 195, "Wankhede Stadium"),
        ("Rajasthan Royals", 175, "Sawai Mansingh Stadium"),
    ]
    columns = ["team", "total_runs", "venue"]
    df = spark.createDataFrame(data, columns)

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
    print("✔ DataFrame transformation assertions passed.")

    # 3. Test Spark SQL Engine
    df.createOrReplaceTempView("ipl_scores")
    sql_result = spark.sql(
        "SELECT team, total_runs FROM ipl_scores WHERE total_runs > 200 ORDER BY total_runs DESC"
    )
    print("\n--- Spark SQL Query Output (total_runs > 200) ---")
    sql_result.show(truncate=False)

    sql_count = sql_result.count()
    assert sql_count == 2, f"Expected 2 teams with total_runs > 200, got {sql_count}"
    print("✔ Spark SQL query assertion passed.")

    spark.stop()
    print("\n==========================================================")
    print("✅ TEST PASSED: Spark computation and SQL engine verified!")
    print("==========================================================")


if __name__ == "__main__":
    try:
        run_test()
    except Exception as e:
        print(f"❌ TEST FAILED with exception: {e}", file=sys.stderr)
        sys.exit(1)

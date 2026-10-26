#!/usr/bin/env python3
"""
Smoke Test 2: Spark + Hadoop HDFS Integration Test
Verifies that Apache Spark successfully:
1. Connects to Hadoop HDFS NameNode
2. Reads raw CSV datasets stored on HDFS
3. Executes Spark SQL queries and aggregations on the distributed data
4. Writes processed results back to HDFS
5. Reads back the saved result to verify roundtrip integrity
"""

import sys
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, count as _count


def run_integration_test():
    print("==========================================================")
    print("Running Integration Test: Spark + Hadoop HDFS Connectivity")
    print("==========================================================")

    # Master: inside Docker it defaults to spark://spark-master:7077 or local[*]
    master = os.getenv("SPARK_MASTER", "local[*]")
    hdfs_host = os.getenv("HDFS_NAMENODE_HOST", "namenode")
    hdfs_port = os.getenv("HDFS_NAMENODE_PORT", "9000")
    hdfs_base_uri = f"hdfs://{hdfs_host}:{hdfs_port}"

    print(f"Connecting to Spark Master: {master}")
    print(f"Hadoop HDFS Base URI: {hdfs_base_uri}")

    spark = (
        SparkSession.builder.appName("HDFSSparkIntegrationTest")
        .master(master)
        .config("spark.hadoop.fs.defaultFS", hdfs_base_uri)
        .config("spark.sql.warehouse.dir", f"{hdfs_base_uri}/spark-warehouse")
        .config("spark.driver.memory", "1g")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    print("✔ SparkSession successfully established.")

    # 1. Read matches dataset from HDFS
    matches_hdfs_path = f"{hdfs_base_uri}/ipl/sample/matches.csv"
    print(f"\n📥 Reading matches from HDFS: {matches_hdfs_path}")
    matches_df = (
        spark.read.option("header", "true")
        .option("inferSchema", "true")
        .csv(matches_hdfs_path)
    )

    matches_count = matches_df.count()
    print(f"✔ Read {matches_count} match records from HDFS.")
    matches_df.printSchema()
    matches_df.select("id", "season", "city", "winner", "result").show(5, truncate=False)
    assert matches_count > 0, "Matches dataset in HDFS is empty!"

    # 2. Read deliveries dataset from HDFS
    deliveries_hdfs_path = f"{hdfs_base_uri}/ipl/sample/deliveries.csv"
    print(f"\n📥 Reading deliveries from HDFS: {deliveries_hdfs_path}")
    deliveries_df = (
        spark.read.option("header", "true")
        .option("inferSchema", "true")
        .csv(deliveries_hdfs_path)
    )

    deliveries_count = deliveries_df.count()
    print(f"✔ Read {deliveries_count} delivery records from HDFS.")
    deliveries_df.select("match_id", "inning", "batting_team", "batter", "batsman_runs").show(5, truncate=False)
    assert deliveries_count > 0, "Deliveries dataset in HDFS is empty!"

    # 3. Perform Spark SQL analytical aggregation
    matches_df.createOrReplaceTempView("matches")
    deliveries_df.createOrReplaceTempView("deliveries")

    summary_df = spark.sql("""
        SELECT 
            winner AS team,
            COUNT(id) AS matches_won
        FROM matches
        WHERE winner IS NOT NULL
        GROUP BY winner
        ORDER BY matches_won DESC
    """)

    print("\n--- Team Wins Aggregation ---")
    summary_df.show(truncate=False)

    # 4. Write processed output back to HDFS
    output_hdfs_path = f"{hdfs_base_uri}/ipl/processed/smoke_test_wins"
    print(f"📤 Writing processed output back to HDFS: {output_hdfs_path}")
    summary_df.write.mode("overwrite").parquet(output_hdfs_path)
    print("✔ Processed data written to HDFS.")

    # 5. Read back from HDFS to confirm persistence
    readback_df = spark.read.parquet(output_hdfs_path)
    readback_count = readback_df.count()
    print(f"✔ Read back {readback_count} records from HDFS output directory.")
    assert readback_count == summary_df.count(), "Readback count does not match written count!"

    spark.stop()
    print("\n==========================================================")
    print("✅ TEST PASSED: Full Spark & Hadoop HDFS Integration verified!")
    print("==========================================================")


if __name__ == "__main__":
    try:
        run_integration_test()
    except Exception as e:
        print(f"❌ TEST FAILED with exception: {e}", file=sys.stderr)
        sys.exit(1)

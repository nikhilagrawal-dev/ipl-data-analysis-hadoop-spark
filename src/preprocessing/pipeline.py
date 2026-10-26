"""
End-to-end Preprocessing and Ingestion Pipeline.
Loads raw datasets from HDFS, runs data quality validations,
cleans the datasets using documented rules, and writes
optimized Parquet datasets to HDFS under /ipl/processed/.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.utils.spark_session import get_spark_session
from src.ingestion.loader import load_raw_matches, load_raw_deliveries, get_default_hdfs_uri
from src.validation.data_quality import (
    validate_matches_dataset,
    validate_deliveries_dataset,
    generate_quality_report,
)
from src.preprocessing.cleaner import clean_matches, clean_deliveries


def run_pipeline():
    print("==========================================================")
    print("STARTING IPL BIG DATA PREPROCESSING & INGESTION PIPELINE")
    print("==========================================================")

    spark = get_spark_session("IPL_Data_Pipeline")
    hdfs_base = get_default_hdfs_uri()

    # 1. Ingestion from HDFS
    print(f"\n📥 1. Loading raw datasets from HDFS ({hdfs_base}/ipl/raw/)...")
    matches_raw = load_raw_matches(spark, f"{hdfs_base}/ipl/raw/matches.csv")
    deliveries_raw = load_raw_deliveries(spark, f"{hdfs_base}/ipl/raw/deliveries.csv")

    raw_matches_count = matches_raw.count()
    raw_deliveries_count = deliveries_raw.count()
    print(f"✔ Raw matches loaded: {raw_matches_count:,} records")
    print(f"✔ Raw deliveries loaded: {raw_deliveries_count:,} records")

    # 2. Validation & Quality Audit
    print("\n🔍 2. Running Data Quality Audits on Raw Datasets...")
    matches_audit = validate_matches_dataset(matches_raw)
    deliveries_audit = validate_deliveries_dataset(deliveries_raw)
    report_text = generate_quality_report(matches_audit, deliveries_audit)
    print(report_text)

    # 3. Preprocessing & Standardization
    print("\n🧹 3. Applying Preprocessing and Normalization Rules...")
    matches_clean = clean_matches(matches_raw)
    deliveries_clean = clean_deliveries(deliveries_raw)

    clean_matches_count = matches_clean.count()
    clean_deliveries_count = deliveries_clean.count()

    print(f"✔ Cleaned matches record count: {clean_matches_count:,}")
    print(f"✔ Cleaned deliveries record count: {clean_deliveries_count:,}")

    # Verify that remaining null count in city is 0
    remaining_null_cities = matches_clean.filter(matches_clean.city.isNull()).count()
    print(f"✔ Remaining null cities after imputation: {remaining_null_cities}")
    assert remaining_null_cities == 0, f"Expected 0 null cities, found {remaining_null_cities}"

    # 4. Save to HDFS in Parquet format
    matches_out_path = f"{hdfs_base}/ipl/processed/matches"
    deliveries_out_path = f"{hdfs_base}/ipl/processed/deliveries"

    print(f"\n📤 4. Writing processed Parquet datasets to HDFS:")
    print(f"   - Matches:    {matches_out_path}")
    print(f"   - Deliveries: {deliveries_out_path}")

    matches_clean.write.mode("overwrite").parquet(matches_out_path)
    print("✔ Matches Parquet written successfully.")

    deliveries_clean.write.mode("overwrite").parquet(deliveries_out_path)
    print("✔ Deliveries Parquet written successfully.")

    # 5. Read back from HDFS to verify roundtrip integrity
    print("\n🔄 5. Verifying Roundtrip Parquet Readback from HDFS...")
    matches_readback = spark.read.parquet(matches_out_path)
    deliveries_readback = spark.read.parquet(deliveries_out_path)

    mb_count = matches_readback.count()
    db_count = deliveries_readback.count()

    print(f"✔ Matches Parquet readback count: {mb_count:,}")
    print(f"✔ Deliveries Parquet readback count: {db_count:,}")

    assert mb_count == clean_matches_count, "Matches readback count mismatch!"
    assert db_count == clean_deliveries_count, "Deliveries readback count mismatch!"

    print("\nSample 3 Cleaned Matches:")
    matches_readback.select("id", "season_year", "city", "team1", "team2", "winner", "result").show(3, truncate=False)

    print("\nSample 3 Cleaned Deliveries:")
    deliveries_readback.select("match_id", "inning", "batting_team", "over", "ball", "batter", "batsman_runs", "is_dot_ball", "over_phase").show(3, truncate=False)

    spark.stop()
    print("==========================================================")
    print("✅ PREPROCESSING PIPELINE COMPLETED SUCCESSFULLY!")
    print("==========================================================")


if __name__ == "__main__":
    run_pipeline()

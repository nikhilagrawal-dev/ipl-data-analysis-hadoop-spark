"""
PySpark Data Ingestion Module.
Loads raw IPL datasets from Hadoop HDFS into Spark DataFrames
with explicit schemas and verified parsing options.
"""

import os
from pyspark.sql import SparkSession, DataFrame
from src.ingestion.schemas import get_raw_matches_schema, get_raw_deliveries_schema


def get_default_hdfs_uri() -> str:
    """Returns the base HDFS URI based on environment settings."""
    host = os.getenv("HDFS_NAMENODE_HOST", "namenode")
    port = os.getenv("HDFS_NAMENODE_PORT", "9000")
    return f"hdfs://{host}:{port}"


def load_raw_matches(
    spark: SparkSession,
    path: str = None,
    use_explicit_schema: bool = True,
) -> DataFrame:
    """
    Loads raw matches.csv from HDFS into a PySpark DataFrame.
    
    Args:
        spark: Active SparkSession
        path: HDFS URI or path to matches.csv (defaults to /ipl/raw/matches.csv)
        use_explicit_schema: If True, uses predefined StructType; otherwise infers schema
    """
    if path is None:
        path = f"{get_default_hdfs_uri()}/ipl/raw/matches.csv"

    reader = (
        spark.read.option("header", "true")
        .option("nullValue", "NA")
        .option("emptyValue", "")
        .option("dateFormat", "yyyy-MM-dd")
        .option("mode", "PERMISSIVE")
    )

    if use_explicit_schema:
        reader = reader.schema(get_raw_matches_schema())
    else:
        reader = reader.option("inferSchema", "true")

    df = reader.csv(path)
    return df


def load_raw_deliveries(
    spark: SparkSession,
    path: str = None,
    use_explicit_schema: bool = True,
) -> DataFrame:
    """
    Loads raw deliveries.csv from HDFS into a PySpark DataFrame.
    
    Args:
        spark: Active SparkSession
        path: HDFS URI or path to deliveries.csv (defaults to /ipl/raw/deliveries.csv)
        use_explicit_schema: If True, uses predefined StructType; otherwise infers schema
    """
    if path is None:
        path = f"{get_default_hdfs_uri()}/ipl/raw/deliveries.csv"

    reader = (
        spark.read.option("header", "true")
        .option("nullValue", "NA")
        .option("emptyValue", "")
        .option("mode", "PERMISSIVE")
    )

    if use_explicit_schema:
        reader = reader.schema(get_raw_deliveries_schema())
    else:
        reader = reader.option("inferSchema", "true")

    df = reader.csv(path)
    return df

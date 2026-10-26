"""
SparkSession factory for the IPL Big Data Analytics project.
Configures PySpark to connect to Hadoop HDFS and Spark standalone cluster.
"""

import os
from pyspark.sql import SparkSession


def get_spark_session(
    app_name: str = "IPL_Big_Data_Analytics",
    master: str = None,
    hdfs_host: str = None,
    hdfs_port: str = None,
) -> SparkSession:
    """
    Creates or retrieves a configured SparkSession.

    Environment variables:
    - SPARK_MASTER: e.g. 'spark://spark-master:7077' or 'local[*]'
    - HDFS_NAMENODE_HOST: e.g. 'namenode' (docker internal) or 'localhost' (host machine)
    - HDFS_NAMENODE_PORT: default '9000'
    """
    if master is None:
        master = os.getenv("SPARK_MASTER", "spark://spark-master:7077")

    if hdfs_host is None:
        hdfs_host = os.getenv("HDFS_NAMENODE_HOST", "namenode")

    if hdfs_port is None:
        hdfs_port = os.getenv("HDFS_NAMENODE_PORT", "9000")

    hdfs_uri = f"hdfs://{hdfs_host}:{hdfs_port}"

    builder = (
        SparkSession.builder.appName(app_name)
        .master(master)
        .config("spark.hadoop.fs.defaultFS", hdfs_uri)
        .config("spark.sql.warehouse.dir", f"{hdfs_uri}/spark-warehouse")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    )

    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark


if __name__ == "__main__":
    spark = get_spark_session("SparkSessionTest")
    print("=" * 60)
    print(f"Spark Version: {spark.version}")
    print(f"Master: {spark.sparkContext.master}")
    print(f"Hadoop fs.defaultFS: {spark.conf.get('spark.hadoop.fs.defaultFS')}")
    print("=" * 60)
    spark.stop()

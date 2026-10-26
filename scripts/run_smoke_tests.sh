#!/usr/bin/env bash
# =========================================================================
# IPL Big Data Analytics - Test Suite Runner
# Executes Phase 1 Foundation, Phase 2 Ingestion/Quality, and Phase 3 Analytics Tests
# =========================================================================

set -euo pipefail

echo "=========================================================="
echo "RUNNING COMPLETE IPL BIG DATA TEST SUITE"
echo "=========================================================="

echo -e "\n🧪 [1/6] Ingestion Test (HDFS CSV -> Spark DataFrames)..."
docker compose exec spark-master /opt/spark/bin/spark-submit /opt/spark/apps/tests/test_ingestion.py

echo -e "\n🧪 [2/6] Data Quality Audit Test..."
docker compose exec spark-master /opt/spark/bin/spark-submit /opt/spark/apps/tests/test_data_quality.py

echo -e "\n🧪 [3/6] Preprocessing & Cleaning Rules Test..."
docker compose exec spark-master /opt/spark/bin/spark-submit /opt/spark/apps/tests/test_preprocessing.py

echo -e "\n🧪 [4/6] Analytics Metrics & Calculation Rules Test..."
docker compose exec spark-master /opt/spark/bin/spark-submit /opt/spark/apps/tests/test_analytics.py

echo -e "\n🧪 [5/6] Spark Engine & SQL Computation Smoke Test..."
docker compose exec spark-master /opt/spark/bin/spark-submit /opt/spark/apps/tests/test_spark_computation.py

echo -e "\n🧪 [6/7] Spark + Hadoop HDFS Integration Smoke Test..."
docker compose exec spark-master /opt/spark/bin/spark-submit /opt/spark/apps/tests/test_hdfs_spark_integration.py

echo -e "\n🧪 [7/7] Streamlit Dashboard & Analytics Unit Tests..."
.venv/bin/pytest tests/test_dashboard.py -v

echo -e "\n=========================================================="
echo "🎉 ALL 7 TEST SUITES PASSED SUCCESSFULLY!"
echo "=========================================================="

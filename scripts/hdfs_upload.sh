#!/usr/bin/env bash
# =========================================================================
# IPL Big Data Analytics - HDFS Upload Script
# Transports datasets from local disk into Hadoop Distributed File System
# =========================================================================

set -euo pipefail

echo "=========================================================="
echo "IPL Dataset Upload to Hadoop HDFS"
echo "=========================================================="

# 1. Verify NameNode container is running
if ! docker compose ps namenode | grep -q "Up"; then
    echo "❌ Error: Hadoop NameNode is not running."
    echo "   Please start the cluster first: docker compose up -d"
    exit 1
fi

echo "✔ Hadoop NameNode is running."

# 2. Create required HDFS directory structure
echo "📁 Creating HDFS target directories (/ipl/raw, /ipl/sample, /ipl/processed)..."
docker compose exec namenode hdfs dfs -mkdir -p /ipl/raw /ipl/sample /ipl/processed /spark-warehouse
docker compose exec namenode hdfs dfs -chmod -R 777 /ipl /spark-warehouse

# 3. Upload sample datasets (always available for testing)
echo "📤 Uploading sample datasets to HDFS (/ipl/sample)..."
docker compose exec namenode hdfs dfs -put -f /opt/project_data/sample/sample_matches.csv /ipl/sample/matches.csv
docker compose exec namenode hdfs dfs -put -f /opt/project_data/sample/sample_deliveries.csv /ipl/sample/deliveries.csv

# 4. Upload full datasets if provided in data/raw/
if [ -f "data/raw/matches.csv" ] && [ -f "data/raw/deliveries.csv" ]; then
    echo "📤 Uploading full IPL datasets to HDFS (/ipl/raw)..."
    docker compose exec namenode hdfs dfs -put -f /opt/project_data/raw/matches.csv /ipl/raw/matches.csv
    docker compose exec namenode hdfs dfs -put -f /opt/project_data/raw/deliveries.csv /ipl/raw/deliveries.csv
    echo "✔ Full datasets successfully uploaded to HDFS."
else
    echo "ℹ Note: data/raw/matches.csv or data/raw/deliveries.csv not yet placed in data/raw/."
    echo "   Sample datasets in /ipl/sample/ are ready for testing and smoke verification."
fi

# 5. List current HDFS directory contents
echo "=========================================================="
echo "Current HDFS /ipl contents:"
docker compose exec namenode hdfs dfs -ls -R /ipl
echo "=========================================================="
echo "✔ HDFS upload step completed successfully!"

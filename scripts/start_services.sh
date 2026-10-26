#!/usr/bin/env bash
# =========================================================================
# IPL Big Data Analytics - Start Cluster Services
# Launches Hadoop HDFS and Apache Spark with Docker Compose
# =========================================================================

set -euo pipefail

echo "=========================================================="
echo "Starting Hadoop HDFS & Apache Spark Cluster Services"
echo "=========================================================="

docker compose up -d

echo ""
echo "Waiting for services to become healthy..."
docker compose ps

echo ""
echo "Cluster Web Interfaces:"
echo "- Hadoop HDFS NameNode: http://localhost:9870"
echo "- Hadoop HDFS DataNode: http://localhost:9864"
echo "- Apache Spark Master:  http://localhost:8080"
echo "- Apache Spark Worker:  http://localhost:8081"
echo "=========================================================="

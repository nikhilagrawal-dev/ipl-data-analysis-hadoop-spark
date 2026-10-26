#!/usr/bin/env bash
# =========================================================================
# IPL Big Data Analytics - Stop Cluster Services
# Gracefully stops Docker Compose containers without deleting data volumes
# =========================================================================

set -euo pipefail

echo "=========================================================="
echo "Stopping Hadoop HDFS & Apache Spark Cluster Services"
echo "=========================================================="

docker compose stop

echo "Cluster containers stopped. Persistent data in HDFS volumes is preserved."
echo "To restart services, run: ./scripts/start_services.sh"
echo "To completely tear down containers and delete volumes, run: docker compose down -v"
echo "=========================================================="

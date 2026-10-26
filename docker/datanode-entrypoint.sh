#!/usr/bin/env bash
set -e

# Ensure hadoop user owns the /data directory and volumes
sudo chown -R hadoop:users /data 2>/dev/null || sudo chmod -R 777 /data

echo "Starting Hadoop HDFS DataNode..."
exec /opt/starter.sh hdfs datanode

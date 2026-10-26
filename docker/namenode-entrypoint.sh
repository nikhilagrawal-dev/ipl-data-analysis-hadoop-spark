#!/usr/bin/env bash
set -e

# Ensure hadoop user owns the /data directory and volumes
sudo chown -R hadoop:users /data 2>/dev/null || sudo chmod -R 777 /data

# Check if NameNode metadata exists in the volume
if [ ! -d "/data/dfs/name/current" ]; then
    echo "=========================================================="
    echo "Formatting HDFS NameNode metadata directory: /data/dfs/name"
    echo "=========================================================="
    hdfs namenode -format -force -nonInteractive
fi

echo "Starting Hadoop HDFS NameNode..."
exec /opt/starter.sh hdfs namenode

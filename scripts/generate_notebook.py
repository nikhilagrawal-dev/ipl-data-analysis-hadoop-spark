"""
Script to generate IPL_Big_Data_Analytics.ipynb Jupyter Notebook
for presentations and code walkthroughs.
"""

import json
import os

nb = {
    "cells": [],
    "metadata": {
        "language_info": {"name": "python", "version": "3.10.0"},
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    },
    "nbformat": 4,
    "nbformat_minor": 4,
}


def add_md(text):
    nb["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip().split("\n")],
    })


def add_code(text):
    nb["cells"].append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in text.strip().split("\n")],
    })


# 1. Header & Architecture
add_md("""# 🏏 IPL Big Data Analytics Engine
### Distributed Data Processing with Hadoop HDFS, Apache Spark & Spark SQL
**Author:** Big Data Analytics Project Team  
**Tech Stack:** Python 3, PySpark 3.5, Apache Hadoop HDFS, Snappy Parquet, Streamlit

---

## 🏛️ Project Architecture & Big Data Pipeline

```
Raw CSV Datasets (1,095 Matches | 260,920 Deliveries)
                   │
                   ▼  (hdfs dfs -put)
   Distributed Hadoop HDFS Storage (/ipl/raw/)
                   │
                   ▼  (PySpark DataFrame & Spark SQL)
   Distributed In-Memory Computing Engine (Apache Spark Master/Workers)
      ├── 1. Team Performance & Head-to-Head Win Rates
      ├── 2. Player Telemetry (Strike Rate vs Average Efficiency Quadrant)
      ├── 3. Match Phase Dynamics (Powerplay vs Middle vs Death Overs)
      └── 4. Venue Fortresses & Toss Decision Impact
                   │
                   ▼  (Partitioned Columnar Export)
   HDFS Analytical Parquet Marts (/ipl/analytics/ in Snappy format)
                   │
                   ▼
   Interactive Sports Broadcast Dashboard (Streamlit & Plotly)
```

---

## 🎯 Core Big Data Concepts Explained
1. **Why Hadoop HDFS?** Provides distributed, fault-tolerant block storage (default 128MB block size) with automatic replication across data nodes.
2. **Why Apache Spark?** Replaces traditional MapReduce with in-memory Directed Acyclic Graph (DAG) execution, achieving 100x faster performance for iterative analytics.
3. **Why Snappy Parquet?** A columnar storage format enabling **projection pushdown** (reading only necessary columns) and **predicate pushdown** (filtering at storage level), reducing disk I/O by >75%.
""")

# 2. Spark Initialization
add_md("""---
## ⚡ Step 1: Initializing Apache Spark Session
We initialize a high-performance `SparkSession` with multi-core parallelism (`local[*]`) and optimized shuffle partitions.
""")

add_code("""import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, sum as _sum, avg, round as _round, 
    when, desc, asc, min as _min, max as _max, 
    row_number, concat, lit
)
from pyspark.sql.window import Window
import pandas as pd

# Initialize Apache Spark Session
spark = SparkSession.builder \\
    .appName("IPL_Big_Data_Analytics_Lecture") \\
    .master("local[*]") \\
    .config("spark.driver.memory", "2g") \\
    .config("spark.sql.shuffle.partitions", "4") \\
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print(f"✔ Apache Spark Version: {spark.version}")
print(f"✔ Spark Master: {spark.sparkContext.master}")
print(f"✔ Default Parallelism: {spark.sparkContext.defaultParallelism} Cores")
""")

# 3. Data Ingestion
add_md("""---
## 📥 Step 2: Data Ingestion from HDFS / Data Lake
We load the pre-computed analytical data marts directly into distributed PySpark DataFrames.
""")

add_code("""# Load team standings and player tables from the analytical data lake
team_standings_df = spark.read.parquet("data/analytics/team_standings")
player_batting_df = spark.read.parquet("data/analytics/player_batting")
player_bowling_df = spark.read.parquet("data/analytics/player_bowling")
phase_summary_df = spark.read.parquet("data/analytics/phase_summary")
season_summary_df = spark.read.parquet("data/analytics/season_summary")

print("--- Team Standings Schema ---")
team_standings_df.printSchema()
""")

# 4. Team Standings & Win Percentage
add_md("""---
## 📊 Step 3: Franchise Dominance & Win Rate Formulations
In Big Data analysis, defining consistent denominators is critical.
$$\\text{Win Percentage} = \\frac{\\text{Total Wins}}{\\text{Matches Played} - \\text{No Results}} \\times 100$$
""")

add_code("""# Display Top 10 Franchises sorted by Total Match Wins
top_franchises = team_standings_df.select(
    "team", "matches_played", "wins", "losses", "no_results", 
    _round("win_percentage", 2).alias("win_rate_pct")
).orderBy(desc("wins"))

top_franchises.show(10, truncate=False)
""")

add_md("""### 🏆 Head-to-Head Clash Aggregation: Mumbai Indians vs Chennai Super Kings
Aggregating match wins using Spark DataFrame `groupBy('team').sum('win')`:
""")

add_code("""# Head-to-head match wins aggregation (sum of wins per team)
h2h_clash_df = spark.sql(\"\"\"
    SELECT 'Mumbai Indians' AS team, 1 AS win
    UNION ALL SELECT 'Mumbai Indians', 1
    UNION ALL SELECT 'Mumbai Indians', 1
    UNION ALL SELECT 'Chennai Super Kings', 1
    UNION ALL SELECT 'Chennai Super Kings', 1
\"\"\")

# Group by team and calculate sum(win)
h2h_wins_table = h2h_clash_df.groupBy("team").sum("win").orderBy("sum(win)", ascending=False)
h2h_wins_table.show()
""")

# 5. Spark SQL
add_md("""---
## 🔍 Step 4: Spark SQL Distributed Query Engine
Spark SQL allows relational SQL queries directly over distributed DataFrames using registered Temporary Views.
""")

add_code("""# Register Temporary SQL View
team_standings_df.createOrReplaceTempView("franchise_standings")

# Execute Spark SQL Query
sql_query = \"\"\"
SELECT 
    team,
    matches_played,
    wins,
    win_percentage,
    CASE 
        WHEN win_percentage >= 55.0 THEN 'ELITE DYNASTY'
        WHEN win_percentage >= 50.0 THEN 'CONTENDER'
        ELSE 'REBUILDING'
    END AS tier_classification
FROM franchise_standings
ORDER BY win_percentage DESC
\"\"\"

sql_df = spark.sql(sql_query)
sql_df.show(truncate=False)
""")

# 6. Player Vanguard
add_md("""---
## ⚡ Step 5: Player Vanguard (Efficiency Quadrant Analytics)
Analyzing individual scoring efficiency and strike impact across deliveries:
- **Batting Strike Rate:** $\\frac{\\text{Total Runs}}{\\text{Balls Faced}} \\times 100$
- **Batting Average:** $\\frac{\\text{Total Runs}}{\\text{Dismissals}}$
""")

add_code("""# Top 10 Batting Powerhouses
top_batters = player_batting_df.select(
    "batter", "matches_batted", "total_runs", "balls_faced",
    _round("batting_avg", 2).alias("average"),
    _round("strike_rate", 2).alias("strike_rate"),
    "hundreds", "fifties"
).orderBy(desc("total_runs"))

top_batters.show(10, truncate=False)
""")

add_code("""# Bowling Economy & Strike Rates (Runs conceded per 6 legal balls)
top_bowlers = player_bowling_df.select(
    "bowler", "matches_bowled", "wickets", "overs",
    _round("economy", 2).alias("economy_rpo"),
    _round("bowling_avg", 2).alias("bowling_avg"),
    "dot_balls"
).orderBy(desc("wickets"))

top_bowlers.show(10, truncate=False)
""")

# 7. Match Phases Breakdown
add_md("""---
## ⏱️ Step 6: Match Phase Telemetry (Powerplay vs Middle vs Death)
T20 cricket divides innings into 3 strategic phases:
1. **Powerplay (Overs 1-6):** Mandatory field restrictions (2 fielders outside 30-yard circle).
2. **Middle Overs (Overs 7-15):** Spin and rotational strike control.
3. **Death Overs (Overs 16-20):** Maximum boundary acceleration and execution.
""")

add_code("""# Over Phase Pacing Breakdown
phase_summary_df.select(
    "over_phase", "total_runs", "total_wickets",
    _round("run_rate", 2).alias("rpo"),
    _round("boundary_pct", 2).alias("boundary_pct"),
    _round("dot_ball_pct", 2).alias("dot_ball_pct")
).show(truncate=False)
""")

# 8. Season Evolution Trends
add_md("""---
## 📈 Step 7: Multi-Season Evolution (2008–2024)
Tracking how modern T20 scoring benchmarks have escalated over 17 years.
""")

add_code("""# 17-Season Benchmark Trends
season_evolution = season_summary_df.select(
    "season_year", "total_matches", "total_runs",
    _round("avg_first_innings_score", 1).alias("avg_1st_innings"),
    "max_first_innings_score",
    "total_sixes"
).orderBy(asc("season_year"))

season_evolution.show(17, truncate=False)
""")

# 9. Clean Shutdown
add_md("""---
## 🛑 Step 8: Clean SparkSession Termination
In distributed computing, actively terminating the SparkContext frees worker memory and thread pools.
""")

add_code("""# Stop Spark Session
spark.stop()
print("✔ Apache Spark Session stopped successfully.")
""")

# Write out the notebook to notebooks/ and root
os.makedirs("notebooks", exist_ok=True)
with open("notebooks/IPL_Big_Data_Analytics.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

with open("IPL_Big_Data_Analytics.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("Notebooks successfully created at:")
print("1. IPL_Big_Data_Analytics.ipynb (Root)")
print("2. notebooks/IPL_Big_Data_Analytics.ipynb")

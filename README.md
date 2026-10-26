# IPL Data Analysis & Performance Insights
### Big Data Analytics (BDA) Project using Hadoop HDFS, Apache Spark & Streamlit

A Big Data Analytics pipeline and interactive dashboard analyzing Indian Premier League (IPL) match and ball-by-ball delivery datasets using distributed storage (**Hadoop HDFS**), distributed computing (**Apache Spark / PySpark / Spark SQL**), and web analytics (**Streamlit & Plotly**).

---

## 🏛 Architecture Overview

```
                      ┌────────────────────────────────────────┐
                      │            Raw IPL Datasets            │
                      │  (matches.csv & deliveries.csv)        │
                      └───────────────────┬────────────────────┘
                                          │  hdfs dfs -put
                                          ▼
                      ┌────────────────────────────────────────┐
                      │       Hadoop Distributed Storage       │
                      │               (HDFS)                   │
                      │  - NameNode (Port 9870 / 9000 RPC)     │
                      │  - DataNode (Port 9864)                │
                      └───────────────────┬────────────────────┘
                                          │
                      ┌───────────────────┴────────────────────┐
                      │     Apache Spark Processing Engine     │
                      │  - Spark Master (Port 8080 / 7077 RPC) │
                      │  - Spark Worker (Port 8081)            │
                      │  - PySpark DataFrame API & Spark SQL   │
                      └───────────────────┬────────────────────┘
                                          │  Processed Parquet / Analytics
                                          ▼
                      ┌────────────────────────────────────────┐
                      │    Interactive Analytics Dashboard     │
                      │     (Streamlit + Plotly Visuals)       │
                      │  - Team Performance & Venue Analysis   │
                      │  - Toss Outcomes & Player Statistics   │
                      └────────────────────────────────────────┘
```

---

## 💻 Tech Stack & Environment Compatibility

- **Host Machine**: macOS on Apple Silicon (Apple M4, ARM64 architecture).
- **Hadoop HDFS**: Apache Hadoop 3.3.6 (running seamlessly via Docker Desktop with Rosetta translation, using official Apache images with automated formatting and health monitoring).
- **Apache Spark**: Apache Spark 4.2.0 (running natively on ARM64 / Apple Silicon for peak CPU performance).
- **Python / PySpark**: Python 3.10 / PySpark 3.5+ integration.
- **Orchestration**: Docker Compose with custom bridge networking (`ipl-network`) and persistent data volumes.

---

## 📁 Project Directory Structure

```
BDA PROJECT/
├── .env                          # Local environment variable configuration
├── .env.example                  # Template configuration file
├── .gitignore                    # Git ignore file for Python, Spark, and macOS
├── README.md                     # Comprehensive project documentation
├── requirements.txt              # Python library dependencies
├── docker-compose.yml            # Multi-container orchestration (HDFS + Spark)
├── config/
│   ├── hadoop/
│   │   ├── core-site.xml         # Hadoop defaultFS and buffer configuration
│   │   └── hdfs-site.xml         # HDFS replication, name/data dir configuration
│   └── spark/
│       └── spark-defaults.conf   # Spark defaults pointing to HDFS defaultFS
├── data/
│   ├── raw/
│   │   └── README.md             # Dataset upload guidelines and expected schemas
│   └── sample/
│       ├── sample_matches.csv    # Small sample matches dataset for test verification
│       └── sample_deliveries.csv # Small sample deliveries dataset for test verification
├── docker/
│   ├── namenode-entrypoint.sh    # Resilient NameNode auto-formatter and bootstrap
│   └── datanode-entrypoint.sh    # DataNode startup permissions handler
├── scripts/
│   ├── start_services.sh         # Starts Docker containers and displays web endpoints
│   ├── stop_services.sh          # Gracefully stops containers (preserves HDFS volumes)
│   ├── hdfs_upload.sh            # Uploads local datasets into Hadoop HDFS
│   └── run_smoke_tests.sh        # Runs Spark computation and HDFS integration tests
├── src/
│   ├── __init__.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── spark_session.py      # Configured SparkSession factory with HDFS support
│   ├── analytics/                # (To be implemented) Data processing & queries
│   │   └── __init__.py
│   └── dashboard/                # (To be implemented) Streamlit interactive UI
│       └── __init__.py
└── tests/
    ├── __init__.py
    ├── test_spark_computation.py         # Smoke test 1: In-memory Spark & SQL engine
    └── test_hdfs_spark_integration.py    # Smoke test 2: Full Spark + HDFS read/write
```

---

## 🚀 Quick Start Guide

### 1. Start the Hadoop & Spark Cluster

Run the startup helper:
```bash
./scripts/start_services.sh
```
*(Or directly using Docker: `docker compose up -d`)*

### 2. Verify Container Health

Check that all four cluster containers are healthy:
```bash
docker compose ps
```

Expected output:
```text
NAME                IMAGE                 STATUS                    PORTS
ipl-hdfs-namenode   apache/hadoop:3.3.6   Up (healthy)              9000, 9870
ipl-hdfs-datanode   apache/hadoop:3.3.6   Up (healthy)              9864
ipl-spark-master    apache/spark:latest   Up (healthy)              7077, 8080
ipl-spark-worker    apache/spark:latest   Up (healthy)              8081
```

### 3. Access Web Dashboards

Open the following URLs in your web browser:
| Service | URL | Description |
| :--- | :--- | :--- |
| **Hadoop HDFS NameNode** | [http://localhost:9870](http://localhost:9870) | Browse HDFS filesystem, capacity, and DataNode status |
| **Hadoop HDFS DataNode** | [http://localhost:9864](http://localhost:9864) | DataNode volume block metrics |
| **Spark Master UI** | [http://localhost:8080](http://localhost:8080) | Live cluster status, connected workers, running apps |
| **Spark Worker UI** | [http://localhost:8081](http://localhost:8081) | Worker resource allocation and executors |

---

## 📊 Dataset Ingestion & Preprocessing Pipeline

The full IPL datasets (`matches.csv` and `deliveries.csv`) are ingested into Hadoop HDFS, validated via PySpark, preprocessed, and saved as optimized Parquet tables.

### 1. Ingest Raw Datasets to HDFS
```bash
./scripts/hdfs_upload.sh
```
This uploads the datasets to `hdfs://namenode:9000/ipl/raw/`:
- `hdfs://namenode:9000/ipl/raw/matches.csv` (1,095 matches)
- `hdfs://namenode:9000/ipl/raw/deliveries.csv` (260,920 deliveries)

### 2. Execute Data Quality Audit & Preprocessing Pipeline
```bash
docker compose exec spark-master /opt/spark/bin/spark-submit /opt/spark/apps/src/preprocessing/pipeline.py
```
This pipeline:
1. Loads the raw CSVs from HDFS with explicit PySpark schemas.
2. Performs comprehensive data quality audits (row counts, nulls, duplicates, anomalies).
3. Applies documented preprocessing rules:
   - **City Imputation**: Fills 51 missing cities from `venue` (Dubai International Stadium -> `Dubai`, Sharjah Cricket Stadium -> `Sharjah`).
   - **Season Normalization**: Standardizes multi-year season strings (`2007/08`, `2009/10`, `2020/21`) into 4-digit integers (`season_year`) while preserving `season_raw`.
   - **Canonical Franchise Mapping**: Standardizes historical rebrands (`Rising Pune Supergiants` -> `Rising Pune Supergiant`, `Royal Challengers Bengaluru` -> `Royal Challengers Bangalore`, `Delhi Daredevils` -> `Delhi Capitals`, `Kings XI Punjab` -> `Punjab Kings`) while preserving original raw team names.
   - **Outcome Adjustments**: Classifies abandoned matches as `'No Result'` with `is_result_declared=False`, replaces null `method` with `'Regular'`, and fills null `result_margin` with `0`.
   - **Delivery Features**: Standardizes null extras/dismissals to `'none'` and derives analytical flags (`is_dot_ball`, `is_boundary`, `is_four`, `is_six`, `over_phase`).
4. Writes cleaned, Snappy-compressed Parquet datasets back to HDFS:
   - `hdfs://namenode:9000/ipl/processed/matches` (38 KB Snappy Parquet, 83% compression)
   - `hdfs://namenode:9000/ipl/processed/deliveries` (1.7 MB Snappy Parquet, 93.7% compression)
5. Verifies roundtrip readback integrity.

## 🏏 Analytics Engine & Reusable Metrics (Phase 3)

The project includes a PySpark and Spark SQL analytical engine under [src/analytics/](file:///Users/nikhilagrawal/Desktop/BDA%20PROJECT/src/analytics/):

### Analytics Modules:
1. **Team Analytics** ([team_analytics.py](file:///Users/nikhilagrawal/Desktop/BDA%20PROJECT/src/analytics/team_analytics.py)):
   - Overall standings (matches played, wins, losses, ties, win % excluding no-results).
   - Season-by-season performance records.
   - Pairwise Head-to-Head records (`team_a < team_b` canonical ordering to prevent inverse duplicates).
2. **Player Analytics** ([player_analytics.py](file:///Users/nikhilagrawal/Desktop/BDA%20PROJECT/src/analytics/player_analytics.py)):
   - Batting leaderboard (runs, batting average, strike rate excluding wides from balls faced, 4s, 6s, 50s, 100s, highest scores).
   - Bowling leaderboard with **strict bowler-wicket exclusions** (`bowled`, `caught`, `caught and bowled`, `lbw`, `stumped`, `hit wicket`; excluding `run out`, `retired hurt`, `retired out`).
   - Bowling economy calculated from legal deliveries (`extras_type NOT IN ('wides', 'noballs')`) and bowler-conceded runs (fielding byes and legbyes excluded).
   - Player of the Match awards ranking.
3. **Season & Scoring Analytics** ([season_analytics.py](file:///Users/nikhilagrawal/Desktop/BDA%20PROJECT/src/analytics/season_analytics.py)):
   - Match counts, total runs, average and highest 1st innings scores by season.
   - Total 4s and 6s, boundary run percentages, and dot-ball percentages.
   - Match over-phase analysis: Powerplay (overs 0–5), Middle (6–14), and Death (15–19).
4. **Venue Analytics** ([venue_analytics.py](file:///Users/nikhilagrawal/Desktop/BDA%20PROJECT/src/analytics/venue_analytics.py)):
   - Matches hosted, average/highest 1st innings scores, chasing vs defending win percentages.
   - Team records by venue with configurable minimum-match thresholds.
5. **Toss Analytics** ([toss_analytics.py](file:///Users/nikhilagrawal/Desktop/BDA%20PROJECT/src/analytics/toss_analytics.py)):
   - Bat vs field decision distribution.
   - Toss winner match victory correlation (chasing win % vs batting first win %).
   - Historical shift towards fielding first over the seasons.

### Execute the Analytics Pipeline
```bash
docker compose exec spark-master /opt/spark/bin/spark-submit /opt/spark/apps/src/analytics/pipeline.py
```
This writes 12 reusable, Snappy-compressed Parquet tables to HDFS under `hdfs://namenode:9000/ipl/analytics/`:
- `/ipl/analytics/team_standings`
- `/ipl/analytics/team_season`
- `/ipl/analytics/team_h2h`
- `/ipl/analytics/player_batting`
- `/ipl/analytics/player_bowling`
- `/ipl/analytics/player_potm`
- `/ipl/analytics/season_summary`
- `/ipl/analytics/phase_summary`
- `/ipl/analytics/venue_summary`
- `/ipl/analytics/team_venue`
- `/ipl/analytics/toss_summary`
- `/ipl/analytics/toss_season`

---

## 🧪 Running the Complete 6-Stage Test Suite

Execute the entire test suite covering the full pipeline from raw HDFS data to analytical queries:
```bash
./scripts/run_smoke_tests.sh
```

### Test Coverage:
1. **`test_ingestion.py`**: Verifies exact record counts (1,095 matches, 260,920 deliveries) and column schemas loaded directly from HDFS.
2. **`test_data_quality.py`**: Asserts 0 duplicate match IDs, 0 duplicate delivery ball keys, 0 negative runs, and 0 invalid overs.
3. **`test_preprocessing.py`**: Verifies 0 remaining null cities, correct season year range (2008–2024), canonical team mappings, and Parquet roundtrip persistence.
4. **`test_analytics.py`**: Validates all analytical calculations, metric denominators, bowler-wicket exclusions, legal-ball definitions, and HDFS analytical table persistence.
5. **`test_spark_computation.py`**: Validates standalone PySpark distributed execution and Spark SQL temp view queries.
6. **`test_hdfs_spark_integration.py`**: Validates roundtrip distributed read/write between Spark and Hadoop HDFS.
7. **`test_dashboard.py`**: Validates all 12 analytical table loaders, KPI accuracy, win percentage rules, Plotly chart builders, filter behavior, and Streamlit execution smoke test.

---

## 🖥️ Interactive Analytics Dashboard (Phase 4)

A dark sports analytics Streamlit web application powered by **Plotly** and reading analytical tables generated by Apache Spark and Hadoop HDFS.

### 🌟 Dashboard Architecture & Pages:
1. **IPL Overview** (`/overview`):
   - Macro tournament KPIs (1,095 matches, 17 seasons, 15 franchises, total runs, bowler wickets).
   - Season matches & runs trends.
   - All-time top franchise and player spotlight.
   - Verified data coverage and no-result exclusions.
2. **Team Analytics** (`/teams`):
   - Complete franchise standings table (matches, wins, losses, ties, win %).
   - Win percentage denominator rule: `(Wins / (Matches Played - No Results)) * 100`.
   - Season-by-season franchise win-rate trajectory charts.
   - Pairwise Head-to-Head selector comparing any two teams.
3. **Player Analytics** (`/players`):
   - All-time batting leaderboard (runs, average, strike rate, 4s, 6s, 100s, 50s, HS).
   - All-time bowling leaderboard (wickets, overs, economy, bowling average, strike rate, dot balls).
   - Interactive Top-N slider (5 to 20) and player search.
   - Scatter quadrant: Batting Strike Rate vs. Batting Average.
   - Scatter quadrant: Bowling Economy Rate vs. Total Wickets.
   - Player of the Match awards leaderboard.
4. **Season & Scoring Analytics** (`/seasons`):
   - Scoring trends across all 17 editions (average & record first-innings totals).
   - Evolution of boundary contribution vs. dot-ball containment.
   - Over-Phase breakdown (Powerplay overs 0–5, Middle overs 6–14, Death overs 15–19).
   - Interactive season selector.
5. **Venue & Toss Analytics** (`/venues`):
   - Stadium match hosting leaderboard with minimum matches filter.
   - Chasing vs. defending win percentages by venue.
   - Coin toss decision breakdown (Field First 64.2% vs. Bat First 35.8%).
   - Toss winner match-win rate (50.83% across 1,090 decided matches).
   - Season evolution of fielding-first preference.
6. **Data Explorer** (`/explorer`):
   - Dropdown inspector for all 12 analytical Parquet tables.
   - Schema and data type inspector.
   - Real-time search/keyword filter across all fields.
   - One-click CSV export of filtered analytical results.

### 🚀 Starting the Dashboard Locally

Run the dashboard with the configured port (default port `8502`, or `8504` if other local projects occupy port 8502):
```bash
# Start on port 8502
./.venv/bin/streamlit run src/dashboard/app.py --server.port=8502

# Or start on port 8504 (if port 8502 is busy)
./.venv/bin/streamlit run src/dashboard/app.py --server.port=8504
```

Access the dashboard at:
👉 **[http://localhost:8502](http://localhost:8502)** (or `http://localhost:8504`)

---

## 🛑 Stopping the Services

- **To pause/stop services (preserves all data stored in HDFS)**:
  ```bash
  ./scripts/stop_services.sh
  ```
- **To completely destroy containers and remove all persistent HDFS volumes**:
  ```bash
  docker compose down -v
  ```

---

## 📌 Project Milestones Status
- [x] **Phase 1: Environment & Infrastructure Setup** (Hadoop HDFS, Spark, Docker Compose, Smoke Tests)
- [x] **Phase 2: Data Ingestion & Data Quality Audit** (CSV ingestion, schema inference, data cleaning, HDFS Parquet storage)
- [x] **Phase 3: Big Data Analytics Engine** (PySpark & Spark SQL transformations, 12 analytical tables saved to HDFS)
- [x] **Phase 4: Interactive Dashboard** (Multipage Streamlit application, Plotly visualizations, dark sports theme, tests)
- [ ] **Phase 5: Report, Presentation & Project Deliverables** *(Awaiting User Confirmation)*

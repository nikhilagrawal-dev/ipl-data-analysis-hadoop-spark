# IPL Dataset Directory (`data/raw/`)

This directory is reserved for the raw input datasets used in the Big Data Analytics pipeline:

1. **`matches.csv`**
   - Contains high-level information for each IPL match (match ID, season, teams, toss decisions, winner, venue, player of the match, umpires, etc.).
2. **`deliveries.csv`**
   - Contains ball-by-ball delivery data for every match (match ID, inning, batting/bowling team, bowler, batsman, runs, extras, wickets, etc.).

---

## Instructions for Adding Datasets

1. Download or copy your `matches.csv` and `deliveries.csv` into this folder:
   ```bash
   data/raw/matches.csv
   data/raw/deliveries.csv
   ```
2. Upload the raw datasets from your local machine into Hadoop HDFS using the helper script:
   ```bash
   ./scripts/hdfs_upload.sh
   ```
   Or manually via Docker:
   ```bash
   docker compose exec namenode hdfs dfs -mkdir -p /ipl/raw
   docker compose exec namenode hdfs dfs -put -f /opt/project_data/raw/matches.csv /ipl/raw/matches.csv
   docker compose exec namenode hdfs dfs -put -f /opt/project_data/raw/deliveries.csv /ipl/raw/deliveries.csv
   ```
3. Verify that the files exist in HDFS:
   ```bash
   docker compose exec namenode hdfs dfs -ls /ipl/raw/
   ```

---

## Expected Schemas

### `matches.csv`
- `id` (integer)
- `season` (string / integer)
- `city` (string)
- `date` (date / string: YYYY-MM-DD)
- `match_type` (string)
- `player_of_match` (string)
- `venue` (string)
- `team1` (string)
- `team2` (string)
- `toss_winner` (string)
- `toss_decision` (string: `bat` / `field`)
- `winner` (string)
- `result` (string: `runs` / `wickets` / `tie`)
- `result_margin` (integer)
- `target_runs` (integer)
- `target_overs` (integer)
- `super_over` (string / integer)
- `method` (string)
- `umpire1` (string)
- `umpire2` (string)

### `deliveries.csv`
- `match_id` (integer)
- `inning` (integer)
- `batting_team` (string)
- `bowling_team` (string)
- `over` (integer)
- `ball` (integer)
- `batter` (string)
- `bowler` (string)
- `non_striker` (string)
- `batsman_runs` (integer)
- `extra_runs` (integer)
- `total_runs` (integer)
- `is_wicket` (integer)

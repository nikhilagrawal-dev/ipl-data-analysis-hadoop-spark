"""
IPL Analytics Execution and Export Pipeline.
Executes all analytical computations across Teams, Players, Seasons, Venues, and Toss,
and writes the processed metrics to HDFS under /ipl/analytics/ in Parquet format.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.utils.spark_session import get_spark_session
from src.ingestion.loader import get_default_hdfs_uri
from src.analytics.team_analytics import (
    get_team_overall_performance,
    get_team_season_performance,
    get_team_head_to_head,
)
from src.analytics.player_analytics import (
    get_top_run_scorers,
    get_top_wicket_takers,
    get_player_of_match_counts,
)
from src.analytics.season_analytics import (
    get_season_summary,
    get_over_phase_analytics,
)
from src.analytics.venue_analytics import (
    get_venue_summary,
    get_team_performance_by_venue,
)
from src.analytics.toss_analytics import (
    get_toss_decision_summary,
    get_toss_trends_by_season,
)


def run_analytics_pipeline():
    print("==========================================================")
    print("STARTING IPL BIG DATA ANALYTICS COMPUTATION PIPELINE")
    print("==========================================================")

    spark = get_spark_session("IPL_Analytics_Engine")
    hdfs_base = get_default_hdfs_uri()

    # 1. Load Cleaned Datasets from HDFS
    print(f"\n📥 1. Loading cleaned Parquet datasets from {hdfs_base}/ipl/processed/...")
    matches_df = spark.read.parquet(f"{hdfs_base}/ipl/processed/matches")
    deliveries_df = spark.read.parquet(f"{hdfs_base}/ipl/processed/deliveries")

    print(f"✔ Matches loaded: {matches_df.count():,} rows")
    print(f"✔ Deliveries loaded: {deliveries_df.count():,} rows")

    # Register temporary views for SQL queries
    matches_df.createOrReplaceTempView("matches")
    deliveries_df.createOrReplaceTempView("deliveries")

    # 2. Compute Team Analytics
    print("\n🏏 2. Computing Team Analytics...")
    team_standings = get_team_overall_performance(matches_df)
    team_season = get_team_season_performance(matches_df)
    team_h2h = get_team_head_to_head(matches_df)

    print("--- Top 5 Teams by Wins ---")
    team_standings.show(5, truncate=False)

    # 3. Compute Player Analytics
    print("\n⭐ 3. Computing Player Analytics...")
    top_batters = get_top_run_scorers(deliveries_df, min_runs=1000, top_n=20)
    top_bowlers = get_top_wicket_takers(deliveries_df, min_wickets=50, top_n=20)
    top_potm = get_player_of_match_counts(matches_df, top_n=10)

    print("--- Top 5 Batters ---")
    top_batters.select("batter", "total_runs", "batting_avg", "strike_rate", "hundreds", "fifties").show(5, truncate=False)

    print("--- Top 5 Bowlers ---")
    top_bowlers.select("bowler", "wickets", "overs", "economy", "bowling_avg", "bowling_strike_rate").show(5, truncate=False)

    print("--- Top 5 POTM Award Winners ---")
    top_potm.show(5, truncate=False)

    # 4. Compute Season & Scoring Trends
    print("\n📅 4. Computing Season & Phase Scoring Trends...")
    season_summary = get_season_summary(matches_df, deliveries_df)
    phase_summary = get_over_phase_analytics(deliveries_df)

    print("--- Season Trends Sample ---")
    season_summary.select("season_year", "total_matches", "total_runs", "avg_first_innings_score", "boundary_run_pct").show(5, truncate=False)

    print("--- Match Phases Breakdown ---")
    phase_summary.show(truncate=False)

    # 5. Compute Venue Analytics
    print("\n🏟 5. Computing Venue Analytics...")
    venue_summary = get_venue_summary(matches_df, deliveries_df, min_matches=10)
    team_venue = get_team_performance_by_venue(matches_df, min_venue_matches=10)

    print("--- Top 5 Venues by Matches Hosted ---")
    venue_summary.select("venue", "matches_hosted", "avg_first_innings_score", "chasing_win_pct").show(5, truncate=False)

    # 6. Compute Toss Analytics
    print("\n🪙 6. Computing Toss Analytics...")
    toss_summary = get_toss_decision_summary(matches_df)
    toss_season = get_toss_trends_by_season(matches_df)

    print("--- Overall Toss Impact ---")
    toss_summary.show(truncate=False)

    # 7. Write All Analytics Outputs to HDFS (/ipl/analytics/)
    analytics_base = f"{hdfs_base}/ipl/analytics"
    print(f"\n📤 7. Writing Reusable Analytical Parquet Tables to HDFS ({analytics_base}/)...")

    outputs = {
        f"{analytics_base}/team_standings": team_standings,
        f"{analytics_base}/team_season": team_season,
        f"{analytics_base}/team_h2h": team_h2h,
        f"{analytics_base}/player_batting": top_batters,
        f"{analytics_base}/player_bowling": top_bowlers,
        f"{analytics_base}/player_potm": top_potm,
        f"{analytics_base}/season_summary": season_summary,
        f"{analytics_base}/phase_summary": phase_summary,
        f"{analytics_base}/venue_summary": venue_summary,
        f"{analytics_base}/team_venue": team_venue,
        f"{analytics_base}/toss_summary": toss_summary,
        f"{analytics_base}/toss_season": toss_season,
    }

    for path, df in outputs.items():
        table_name = path.split("/")[-1]
        df.write.mode("overwrite").parquet(path)
        print(f"✔ Saved table: {table_name}")

    # 8. Verify HDFS Readback for Saved Analytics
    print("\n🔄 8. Verifying Roundtrip Readback for All Tables in HDFS...")
    for path in outputs.keys():
        table_name = path.split("/")[-1]
        readback_df = spark.read.parquet(path)
        row_count = readback_df.count()
        assert row_count > 0, f"Table {table_name} is empty!"
        print(f"✔ Readback verified: {table_name} ({row_count} rows)")

    spark.stop()
    print("\n==========================================================")
    print("✅ IPL ANALYTICS ENGINE PIPELINE COMPLETED SUCCESSFULLY!")
    print("==========================================================")


if __name__ == "__main__":
    run_analytics_pipeline()

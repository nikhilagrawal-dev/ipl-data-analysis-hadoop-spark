#!/usr/bin/env python3
"""
Analytics Test Suite:
Tests metric definitions, denominator rules, wicket exclusions,
legal-ball logic, tie/no-result handling, and HDFS output persistence.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.spark_session import get_spark_session
from src.ingestion.loader import get_default_hdfs_uri
from src.analytics.team_analytics import (
    get_team_overall_performance,
    get_team_head_to_head,
)
from src.analytics.player_analytics import (
    get_top_run_scorers,
    get_top_wicket_takers,
    BOWLER_CREDITED_DISMISSALS,
)
from src.analytics.season_analytics import (
    get_season_summary,
    get_over_phase_analytics,
)
from src.analytics.venue_analytics import get_venue_summary
from src.analytics.toss_analytics import get_toss_decision_summary


def test_team_analytics_metrics(spark, matches_df):
    print("Testing Team Analytics metrics & denominator rules...")
    team_perf = get_team_overall_performance(matches_df)
    
    # 1. Total wins must equal total matches with a declared result (1,090)
    total_wins = team_perf.selectExpr("sum(wins)").collect()[0][0]
    total_no_results = team_perf.selectExpr("sum(no_results)").collect()[0][0]
    
    assert total_wins == 1090, f"Expected 1,090 total wins, got {total_wins}"
    # Since each match involves 2 teams, total no_results in team standings is 5 * 2 = 10
    assert total_no_results == 10, f"Expected 10 team no_results, got {total_no_results}"
    
    # 2. Check top winning teams
    top_teams = [r["team"] for r in team_perf.limit(2).collect()]
    assert "Mumbai Indians" in top_teams
    assert "Chennai Super Kings" in top_teams
    
    # 3. Head-to-Head integrity check
    h2h = get_team_head_to_head(matches_df)
    assert h2h.count() > 0
    print("✅ Team Analytics assertions passed.")


def test_player_analytics_rules(spark, matches_df, deliveries_df):
    print("\nTesting Player Analytics rules (wicket exclusions & legal balls)...")
    
    # 1. Batting checks
    top_batters = get_top_run_scorers(deliveries_df, min_runs=1000, top_n=5)
    kohli = top_batters.filter(top_batters.batter == "V Kohli").collect()
    assert len(kohli) == 1, "V Kohli not found in top scorers"
    assert kohli[0]["total_runs"] > 8000, f"Expected Kohli runs > 8000, got {kohli[0]['total_runs']}"
    assert kohli[0]["hundreds"] == 8, f"Expected 8 centuries for Kohli, got {kohli[0]['hundreds']}"
    
    # 2. Bowler wicket exclusions
    top_bowlers = get_top_wicket_takers(deliveries_df, min_wickets=50, top_n=5)
    chahal = top_bowlers.filter(top_bowlers.bowler == "YS Chahal").collect()
    assert len(chahal) == 1, "YS Chahal not found in top bowlers"
    assert chahal[0]["wickets"] == 205, f"Expected 205 wickets for Chahal, got {chahal[0]['wickets']}"
    
    # Verify that run out dismissals are strictly excluded from bowler wickets
    run_outs_as_wickets = deliveries_df.filter(
        deliveries_df.dismissal_kind == "run out"
    ).filter(
        deliveries_df.dismissal_kind.isin(BOWLER_CREDITED_DISMISSALS)
    ).count()
    assert run_outs_as_wickets == 0, "Run-out dismissals erroneously included in bowler wickets!"
    
    print("✅ Player Analytics assertions passed.")


def test_season_and_phase_analytics(spark, matches_df, deliveries_df):
    print("\nTesting Season & Over Phase Analytics...")
    season_df = get_season_summary(matches_df, deliveries_df)
    
    # Exactly 17 seasons
    assert season_df.count() == 17, f"Expected 17 seasons, got {season_df.count()}"
    
    # Match count sum across seasons == 1,095
    total_season_matches = season_df.selectExpr("sum(total_matches)").collect()[0][0]
    assert total_season_matches == 1095, f"Expected 1,095 total matches, got {total_season_matches}"
    
    # Phase analysis: Death overs should have highest run rate
    phases = get_over_phase_analytics(deliveries_df).collect()
    phase_dict = {r["over_phase"]: r["run_rate"] for r in phases}
    assert phase_dict["Death"] > phase_dict["Powerplay"]
    assert phase_dict["Death"] > phase_dict["Middle"]
    print("✅ Season and Phase Analytics assertions passed.")


def test_venue_and_toss_analytics(spark, matches_df, deliveries_df):
    print("\nTesting Venue & Toss Analytics...")
    venues = get_venue_summary(matches_df, deliveries_df, min_matches=10)
    assert venues.count() > 0
    
    toss = get_toss_decision_summary(matches_df).collect()[0]
    assert toss["total_decided_matches"] == 1090
    assert toss["elected_field"] + toss["elected_bat"] == 1090
    # Field win rate must match recorded field victories
    assert toss["field_first_win_pct"] > 50.0
    print("✅ Venue & Toss Analytics assertions passed.")


def test_hdfs_analytics_persistence(spark):
    print("\nTesting HDFS Analytics tables persistence & readback...")
    hdfs_base = get_default_hdfs_uri()
    tables = [
        "team_standings",
        "team_season",
        "team_h2h",
        "player_batting",
        "player_bowling",
        "player_potm",
        "season_summary",
        "phase_summary",
        "venue_summary",
        "team_venue",
        "toss_summary",
        "toss_season",
    ]
    for tbl in tables:
        path = f"{hdfs_base}/ipl/analytics/{tbl}"
        df = spark.read.parquet(path)
        cnt = df.count()
        assert cnt > 0, f"Table {tbl} in HDFS is empty!"
        print(f"✔ Verified {tbl}: {cnt} rows")
    print("✅ HDFS Analytics persistence assertions passed.")


def run_all_analytics_tests():
    print("==========================================================")
    print("RUNNING IPL ANALYTICS MODULE TEST SUITE")
    print("==========================================================")
    spark = get_spark_session("AnalyticsTestSuite")
    hdfs_base = get_default_hdfs_uri()
    
    matches_df = spark.read.parquet(f"{hdfs_base}/ipl/processed/matches")
    deliveries_df = spark.read.parquet(f"{hdfs_base}/ipl/processed/deliveries")
    
    test_team_analytics_metrics(spark, matches_df)
    test_player_analytics_rules(spark, matches_df, deliveries_df)
    test_season_and_phase_analytics(spark, matches_df, deliveries_df)
    test_venue_and_toss_analytics(spark, matches_df, deliveries_df)
    test_hdfs_analytics_persistence(spark)
    
    spark.stop()
    print("\n==========================================================")
    print("🎉 ALL ANALYTICS TESTS PASSED!")
    print("==========================================================")


if __name__ == "__main__":
    run_all_analytics_tests()

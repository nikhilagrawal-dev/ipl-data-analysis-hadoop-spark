"""
Automated Unit and Integration Tests for Phase 4 Streamlit Dashboard.
Verifies analytical table loading, metric formulations, chart generators,
filtering behavior, CSV export, and Streamlit AppTest execution.
"""

import os
import io
import pytest
import pandas as pd
import plotly.graph_objects as go
from streamlit.testing.v1 import AppTest

from src.dashboard.data_loader import (
    load_table,
    get_available_tables,
    get_overall_kpis,
    get_table_metadata,
    ANALYTICAL_TABLES,
)
from src.dashboard.components.chart_helpers import (
    create_horizontal_bar_chart,
    create_vertical_bar_chart,
    create_line_chart,
    create_grouped_bar_chart,
    create_donut_chart,
    create_scatter_plot,
)


class TestDataLoader:
    """Tests for cached analytical table loading and data integrity."""

    def test_all_twelve_analytical_tables_exist(self):
        tables = get_available_tables()
        assert len(tables) == 12
        assert "team_standings" in tables
        assert "player_batting" in tables
        assert "season_summary" in tables
        assert "toss_summary" in tables

    @pytest.mark.parametrize("table_name", ANALYTICAL_TABLES)
    def test_load_each_table(self, table_name):
        df = load_table(table_name)
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0, f"Table {table_name} is empty!"

    def test_invalid_table_raises_error(self):
        with pytest.raises(ValueError, match="Unknown analytical table"):
            load_table("non_existent_table_999")

    def test_table_metadata_extraction(self):
        meta = get_table_metadata("team_standings")
        assert meta["table_name"] == "team_standings"
        assert meta["row_count"] == 15
        assert "team" in meta["columns"]
        assert "wins" in meta["columns"]
        assert "win_percentage" in meta["columns"]


class TestMetricAccuracy:
    """Verifies tournament metrics, denominators, and ground truth alignment."""

    def test_tournament_kpis_accuracy(self):
        kpis = get_overall_kpis()
        assert kpis["total_matches"] == 1095
        assert kpis["total_seasons"] == 17
        assert kpis["total_teams"] == 15
        assert kpis["top_team"] == "Mumbai Indians"
        assert kpis["top_team_wins"] == 144
        assert kpis["top_run_scorer"] == "V Kohli"
        assert kpis["top_runs"] == 8014
        assert kpis["top_wicket_taker"] == "YS Chahal"
        assert kpis["top_wickets"] == 205

    def test_team_win_percentage_denominator_rule(self):
        """
        Verify that win percentage formula strictly uses:
        win_percentage == (wins / (matches_played - no_results)) * 100
        """
        df = load_table("team_standings")
        for _, row in df.iterrows():
            decided = row["matches_played"] - row["no_results"]
            if decided > 0:
                expected_pct = round((row["wins"] / decided) * 100, 2)
                actual_pct = round(row["win_percentage"], 2)
                assert abs(expected_pct - actual_pct) <= 0.05, (
                    f"Team {row['team']} win % mismatch: expected {expected_pct}, got {actual_pct}"
                )

    def test_toss_summary_decided_matches(self):
        """Verify toss summary figures: 1,090 decided matches, 554 toss-winner wins."""
        toss_df = load_table("toss_summary")
        assert len(toss_df) == 1
        row = toss_df.iloc[0]
        assert row["total_decided_matches"] == 1090
        assert row["toss_winner_match_wins"] == 554
        assert round(row["toss_winner_win_pct"], 2) == 50.83


class TestChartHelpers:
    """Verifies that all Plotly figure generators produce valid Figure objects."""

    def test_horizontal_bar_chart(self):
        df = load_table("team_standings").head(5)
        fig = create_horizontal_bar_chart(df, x_col="wins", y_col="team", title="Top Teams")
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert fig.data[0].orientation == "h"

    def test_vertical_bar_chart(self):
        df = load_table("season_summary")
        fig = create_vertical_bar_chart(df, x_col="season_year", y_col="total_matches", title="Matches/Season")
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1

    def test_line_chart(self):
        df = load_table("season_summary")
        fig = create_line_chart(df, x_col="season_year", y_col="total_runs", title="Runs Trend")
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1

    def test_grouped_bar_chart(self):
        df = load_table("phase_summary")
        fig = create_grouped_bar_chart(
            df,
            x_col="over_phase",
            y_cols=["run_rate", "boundary_pct"],
            col_names=["Run Rate", "Boundary %"],
            title="Phase Comparison",
        )
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 2

    def test_donut_chart(self):
        fig = create_donut_chart(
            labels=["Field First", "Bat First"],
            values=[700, 390],
            title="Toss Decision Breakdown",
        )
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1

    def test_scatter_plot(self):
        df = load_table("player_batting").head(10)
        fig = create_scatter_plot(
            df,
            x_col="strike_rate",
            y_col="batting_avg",
            text_col="batter",
            title="SR vs Avg",
        )
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1


class TestFilteringAndExport:
    """Verifies filter behavior, empty results, and CSV export serialization."""

    def test_player_search_and_empty_handling(self):
        df = load_table("player_batting")
        # Search for Kohli
        kohli_df = df[df["batter"].str.contains("Kohli", case=False)]
        assert len(kohli_df) == 1
        assert kohli_df.iloc[0]["batter"] == "V Kohli"

        # Search for non-existent player
        empty_df = df[df["batter"].str.contains("NonExistentPlayerXYZ123", case=False)]
        assert len(empty_df) == 0

    def test_venue_minimum_matches_filter(self):
        df = load_table("venue_summary")
        high_traffic = df[df["matches_hosted"] >= 20]
        assert len(high_traffic) > 0
        assert (high_traffic["matches_hosted"] >= 20).all()

    def test_csv_export_serialization(self):
        df = load_table("phase_summary")
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        assert len(csv_bytes) > 0
        # Re-read to confirm valid CSV
        reloaded = pd.read_csv(io.BytesIO(csv_bytes))
        assert len(reloaded) == len(df)
        assert list(reloaded.columns) == list(df.columns)


class TestStreamlitAppSmoke:
    """Smoke test for Streamlit app compilation and execution via AppTest."""

    def test_app_test_initialization(self):
        app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/dashboard/app.py"))
        at = AppTest.from_file(app_path)
        at.run(timeout=10)
        assert not at.exception, f"AppTest raised an exception: {at.exception}"

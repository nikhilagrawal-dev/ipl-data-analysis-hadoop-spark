"""
Page 4: Season & Scoring Analytics.
Scoring trends across 17 editions, first-innings benchmarks, boundary dynamics, and phase-by-phase breakdowns.
"""

import streamlit as st
import pandas as pd
from src.dashboard.data_loader import load_table
from src.dashboard.components.kpi_cards import render_kpi_card
from src.dashboard.components.chart_helpers import (
    create_line_chart,
    create_grouped_bar_chart,
)
from src.dashboard.config import THEME_COLORS


def render():
    st.title("📈 Season & Scoring Dynamics")
    st.markdown(
        "<div style='color: #526581; font-size: 0.95rem; margin-bottom: 1rem;'>"
        "Evolution of T20 batting aggression: run-rate trends, boundary frequency, first-innings scores, and phase splits."
        "</div>",
        unsafe_allow_html=True,
    )

    # Definitions Banner
    st.markdown(
        """
        <div class="info-banner">
            <b>📐 Phase & Metric Definitions:</b><br>
            • <b>Powerplay:</b> Overs 0–5 (legal balls 1–36). Fielding restrictions apply.<br>
            • <b>Middle Overs:</b> Overs 6–14 (legal balls 37–90). Consolidation and spin bowling phase.<br>
            • <b>Death Overs:</b> Overs 15–19 (legal balls 91–120). High-risk slog and bowling containment phase.<br>
            • <b>Run Rate:</b> <code>(Total Runs / Legal Balls) * 6</code> | <b>Dot Ball %:</b> <code>(Dot Balls / Legal Balls) * 100</code>
        </div>
        """,
        unsafe_allow_html=True,
    )

    season_df = load_table("season_summary").sort_values("season_year")
    phase_df = load_table("phase_summary")

    # 1. Over Phase Performance Breakdown
    st.markdown("<div class='section-title'>Tournament Phase Breakdown (All Seasons)</div>", unsafe_allow_html=True)
    phase_cols = st.columns(3)
    phases = [
        ("Powerplay", "blue"),
        ("Middle", "purple"),
        ("Death", "orange"),
    ]

    for idx, (phase_name, acc_color) in enumerate(phases):
        p_data = phase_df[phase_df["over_phase"] == phase_name].iloc[0]
        with phase_cols[idx]:
            render_kpi_card(
                f"{phase_name} Phase",
                f"{p_data['run_rate']:.2f} RPO",
                f"{p_data['boundary_pct']:.1f}% Boundaries | {p_data['dot_ball_pct']:.1f}% Dots",
                accent=acc_color,
                help_text=f"Total Runs: {int(p_data['total_runs']):,} | Wickets: {int(p_data['total_wickets']):,}",
            )

    # Phase Run Rate vs Boundary Comparison Chart
    fig_phase = create_grouped_bar_chart(
        phase_df,
        x_col="over_phase",
        y_cols=["run_rate", "boundary_pct", "dot_ball_pct"],
        col_names=["Run Rate (RPO)", "Boundary %", "Dot Ball %"],
        title="Phase Comparison: Run Rate vs. Boundary % vs. Dot Ball %",
        x_label="Over Phase",
        y_label="Metric Value",
        colors=[THEME_COLORS["accent_orange"], THEME_COLORS["accent_blue"], THEME_COLORS["accent_purple"]],
    )
    st.plotly_chart(fig_phase, use_container_width=True)

    st.markdown("---")

    # 2. First Innings Scoring Benchmarks Across Seasons
    st.markdown("<div class='section-title'>First-Innings Score Evolution</div>", unsafe_allow_html=True)
    col_bench1, col_bench2 = st.columns(2)
    with col_bench1:
        fig_avg_score = create_line_chart(
            season_df,
            x_col="season_year",
            y_col="avg_first_innings_score",
            title="Average 1st Innings Score per Season",
            x_label="Season",
            y_label="Average 1st Innings Runs",
            line_color=THEME_COLORS["accent_blue"],
        )
        st.plotly_chart(fig_avg_score, use_container_width=True)

    with col_bench2:
        fig_max_score = create_line_chart(
            season_df,
            x_col="season_year",
            y_col="max_first_innings_score",
            title="Highest 1st Innings Score per Season",
            x_label="Season",
            y_label="Highest Score Recorded",
            line_color=THEME_COLORS["accent_orange"],
        )
        st.plotly_chart(fig_max_score, use_container_width=True)

    st.markdown("---")

    # 3. Boundary & Dot Ball Trends
    st.markdown("<div class='section-title'>Boundary Aggression vs. Dot Ball Containment</div>", unsafe_allow_html=True)
    fig_boundary_dot = create_grouped_bar_chart(
        season_df,
        x_col="season_year",
        y_cols=["boundary_run_pct", "dot_ball_pct"],
        col_names=["Boundary Run % (Runs from 4s & 6s)", "Dot Ball %"],
        title="Evolution of Boundary Run Contribution vs. Dot Ball Percentage",
        x_label="Season",
        y_label="Percentage (%)",
        colors=[THEME_COLORS["accent_orange"], THEME_COLORS["accent_blue"]],
    )
    st.plotly_chart(fig_boundary_dot, use_container_width=True)

    # 4. Interactive Season Inspector
    st.markdown("<div class='section-title'>Deep-Dive: Season Scoring Card</div>", unsafe_allow_html=True)
    selected_season = st.selectbox(
        "Choose Season to Inspect:",
        options=sorted(season_df["season_year"].unique(), reverse=True),
    )

    s_row = season_df[season_df["season_year"] == selected_season].iloc[0]
    sc1, sc2, sc3, sc4, sc5 = st.columns(5)
    with sc1:
        render_kpi_card("Season Matches", str(int(s_row["total_matches"])), accent="blue")
    with sc2:
        render_kpi_card("Total Runs Scored", f"{int(s_row['total_runs']):,}", accent="orange")
    with sc3:
        render_kpi_card("Avg 1st Innings", f"{s_row['avg_first_innings_score']:.1f}", accent="purple")
    with sc4:
        render_kpi_card("Record Score", str(int(s_row["max_first_innings_score"])), accent="red")
    with sc5:
        render_kpi_card("Boundaries", f"{int(s_row['total_fours']):,} 4s | {int(s_row['total_sixes']):,} 6s", accent="green")

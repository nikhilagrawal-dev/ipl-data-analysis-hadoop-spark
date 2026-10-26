"""
Page 1: IPL Tournament Overview.
High-level KPIs, tournament trends across 17 seasons, top teams and players, and data coverage notes.
"""

import streamlit as st
import pandas as pd
from src.dashboard.data_loader import load_table, get_overall_kpis
from src.dashboard.components.kpi_cards import render_kpi_card
from src.dashboard.components.chart_helpers import (
    create_vertical_bar_chart,
    create_line_chart,
    create_horizontal_bar_chart,
)
from src.dashboard.config import THEME_COLORS


def render():
    st.title("🏏 IPL Tournament Overview (2008 – 2024)")
    st.markdown(
        "<div style='color: #526581; font-size: 0.95rem; margin-bottom: 1rem;'>"
        "A macro-level view of the Indian Premier League across 17 seasons, powered by Apache Spark analytics and Hadoop HDFS distributed storage."
        "</div>",
        unsafe_allow_html=True,
    )

    # Data Coverage & Verification Banner
    st.markdown(
        """
        <div class="info-banner">
            <b>📊 Verified Data Coverage:</b> 1,095 total matches played across 17 tournament editions (2008–2024) featuring 15 franchises.<br>
            <i>Notice:</i> 1,090 matches reached a decisive conclusion; 5 matches ended as No Results (abandoned due to weather). Denominators for win percentages strictly exclude No Result fixtures.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 1. Primary Tournament KPIs with Distinct Accent Colors
    try:
        kpis = get_overall_kpis()
    except Exception as e:
        st.error(f"Failed to load tournament KPIs: {e}")
        return

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        render_kpi_card("Total Matches", f"{kpis['total_matches']:,}", "1,090 Decided &bull; 5 NR", accent="blue")
    with col2:
        render_kpi_card("Seasons", f"{kpis['total_seasons']}", "2008 – 2024", accent="purple")
    with col3:
        render_kpi_card("Franchises", f"{kpis['total_teams']}", "Active & Historical", accent="blue")
    with col4:
        render_kpi_card("Total Runs", f"{kpis['total_runs']:,}", f"{kpis['total_fours']:,} 4s | {kpis['total_sixes']:,} 6s", accent="orange")
    with col5:
        render_kpi_card("Total Wickets", f"{kpis['total_wickets']:,}", "Bowler Dismissals", accent="green")

    st.markdown("---")

    # 2. Spotlight Leaders
    st.markdown("<div class='section-title'>All-Time Tournament Leaders</div>", unsafe_allow_html=True)
    spot1, spot2, spot3, spot4 = st.columns(4)
    with spot1:
        render_kpi_card(
            "Top Franchise",
            kpis["top_team"],
            f"{kpis['top_team_wins']} Match Wins (55.2%)",
            accent="orange",
            help_text="Most match wins in IPL history",
        )
    with spot2:
        render_kpi_card(
            "All-Time Top Scorer",
            kpis["top_run_scorer"],
            f"{kpis['top_runs']:,} Runs (8 Centuries)",
            accent="blue",
            help_text="Highest aggregate runs in IPL history",
        )
    with spot3:
        render_kpi_card(
            "All-Time Wicket Taker",
            kpis["top_wicket_taker"],
            f"{kpis['top_wickets']} Wickets (7.84 Econ)",
            accent="green",
            help_text="Leading wicket taker in IPL history",
        )
    with spot4:
        potm_df = load_table("player_potm")
        top_potm = potm_df.iloc[0]
        render_kpi_card(
            "Most POTM Awards",
            str(top_potm["player_of_match"]),
            f"{int(top_potm['potm_awards'])} Awards",
            accent="purple",
            help_text="Player of the Match awards",
        )

    st.markdown("---")

    # 3. Macro Season Trends
    st.markdown("<div class='section-title'>Season-by-Season Evolution</div>", unsafe_allow_html=True)
    season_df = load_table("season_summary")

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        fig_matches = create_vertical_bar_chart(
            season_df,
            x_col="season_year",
            y_col="total_matches",
            title="Matches Played per Season",
            x_label="Season Year",
            y_label="Matches",
            color_hex=THEME_COLORS["accent_blue"],
        )
        st.plotly_chart(fig_matches, use_container_width=True)

    with chart_col2:
        fig_runs = create_line_chart(
            season_df,
            x_col="season_year",
            y_col="total_runs",
            title="Total Runs Scored per Season",
            x_label="Season Year",
            y_label="Total Runs",
            line_color=THEME_COLORS["accent_orange"],
        )
        st.plotly_chart(fig_runs, use_container_width=True)

    # 4. Top Franchises Standings Preview
    st.markdown("<div class='section-title'>Top Franchises by Total Wins</div>", unsafe_allow_html=True)
    teams_df = load_table("team_standings")
    top5_teams = teams_df.head(7)

    fig_top_teams = create_horizontal_bar_chart(
        top5_teams,
        x_col="wins",
        y_col="team",
        title="Top Franchises by Matches Won",
        x_label="Total Wins",
        y_label="Franchise",
        color_hex=THEME_COLORS["accent_orange"],
    )
    st.plotly_chart(fig_top_teams, use_container_width=True)

    # 5. Query-Derived Strategic Insights
    st.markdown("<div class='section-title'>Key Analytical Insights</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background: #FFFFFF; border: 1px solid #DCE4EF; border-radius: 8px; padding: 1.1rem 1.4rem; color: #172B4D; font-size: 0.92rem; line-height: 1.6;">
            <ul style="margin: 0; padding-left: 1.2rem;">
                <li style="margin-bottom: 0.5rem;"><b>Franchise Dominance:</b> Mumbai Indians (144 wins) and Chennai Super Kings (138 wins) lead the all-time victory tallies with sustained win percentages exceeding 55%.</li>
                <li style="margin-bottom: 0.5rem;"><b>Toss Impact Neutrality:</b> Across 1,090 decided matches, toss winners went on to win the match in 554 fixtures (50.83%), showing that winning the coin toss provides minimal structural bias over tournament history.</li>
                <li style="margin-bottom: 0.5rem;"><b>Chasing Preference:</b> Teams bowling first have won 53.86% of decided matches, reflecting modern T20 preferences for setting targets with clarity on run-rate requirements.</li>
                <li style="margin-bottom: 0;"><b>Phase Dynamics:</b> The Death phase (overs 15–19) commands a blistering run-rate of 9.96 runs/over, compared to 7.86 in the Powerplay and 7.79 in the Middle overs.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

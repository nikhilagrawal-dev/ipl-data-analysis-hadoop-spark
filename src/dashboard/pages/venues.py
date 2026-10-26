"""
Page 5: Venue & Toss Analytics.
Ground dimensions, chasing vs. defending biases, coin toss influence, and tactical fielding preferences.
"""

import streamlit as st
import pandas as pd
from src.dashboard.data_loader import load_table
from src.dashboard.components.kpi_cards import render_kpi_card
from src.dashboard.components.chart_helpers import (
    create_horizontal_bar_chart,
    create_line_chart,
    create_donut_chart,
)
from src.dashboard.config import THEME_COLORS


def render():
    st.title("🏟️ Venue & Toss Analytics")
    st.markdown(
        "<div style='color: #526581; font-size: 0.95rem; margin-bottom: 1rem;'>"
        "Ground characteristics, pitch conditions, toss decision tactical trends, and chasing vs. defending advantages."
        "</div>",
        unsafe_allow_html=True,
    )

    # Denominator Banner
    st.markdown(
        """
        <div class="info-banner">
            <b>🪙 Toss & Venue Decision Metrics:</b> Computed across 1,090 decided fixtures (5 abandoned matches excluded).<br>
            <i>Chasing Win % Denominator:</i> <code>Chasing Wins / (Chasing Wins + Defending Wins) * 100</code>. Matches tied at 20 overs are tracked separately in the venue registry.
        </div>
        """,
        unsafe_allow_html=True,
    )

    venue_df = load_table("venue_summary")
    toss_sum_df = load_table("toss_summary")
    toss_season_df = load_table("toss_season").sort_values("season_year")

    # 1. Macro Toss Insights
    st.markdown("<div class='section-title'>Macro Coin Toss Analysis (All-Time)</div>", unsafe_allow_html=True)
    toss_row = toss_sum_df.iloc[0]

    tc1, tc2, tc3, tc4 = st.columns(4)
    with tc1:
        render_kpi_card(
            "Toss Winner Win Rate",
            f"{toss_row['toss_winner_win_pct']:.2f}%",
            f"{int(toss_row['toss_winner_match_wins'])} / {int(toss_row['total_decided_matches'])} Decided",
            accent="orange",
            help_text="Percentage of matches where the team winning the toss also won the match",
        )
    with tc2:
        render_kpi_card(
            "Field First Preference",
            f"{(toss_row['elected_field'] / (toss_row['elected_field'] + toss_row['elected_bat']) * 100):.1f}%",
            f"{int(toss_row['elected_field'])} / {int(toss_row['total_decided_matches'])} Tosses",
            accent="blue",
        )
    with tc3:
        render_kpi_card(
            "Chasing (Field 1st) Win %",
            f"{toss_row['field_first_win_pct']:.2f}%",
            "Win rate when opting to field",
            accent="green",
        )
    with tc4:
        render_kpi_card(
            "Defending (Bat 1st) Win %",
            f"{toss_row['bat_first_win_pct']:.2f}%",
            "Win rate when opting to bat",
            accent="purple",
        )

    toss_donut_col1, toss_trend_col2 = st.columns([1, 2])
    with toss_donut_col1:
        fig_toss_choice = create_donut_chart(
            labels=["Field First", "Bat First"],
            values=[int(toss_row["elected_field"]), int(toss_row["elected_bat"])],
            title="Toss Decision Breakdown",
            colors=[THEME_COLORS["accent_orange"], THEME_COLORS["accent_blue"]],
        )
        st.plotly_chart(fig_toss_choice, use_container_width=True)

    with toss_trend_col2:
        fig_pref_trend = create_line_chart(
            toss_season_df,
            x_col="season_year",
            y_col="field_preference_pct",
            title="Season Evolution: Preference for Fielding First (%)",
            x_label="Season",
            y_label="Chose Field First (%)",
            line_color=THEME_COLORS["accent_orange"],
        )
        st.plotly_chart(fig_pref_trend, use_container_width=True)

    st.markdown("---")

    # 2. Venue Leaderboard & Chasing Biases
    st.markdown("<div class='section-title'>Stadium Performance & Chasing Biases</div>", unsafe_allow_html=True)

    min_matches = st.slider("Filter Venues by Minimum Matches Hosted:", min_value=5, max_value=40, value=15, step=5)
    filtered_venues = venue_df[venue_df["matches_hosted"] >= min_matches].sort_values("matches_hosted", ascending=False)

    st.markdown(f"<span style='color: #526581;'>Displaying <b>{len(filtered_venues)}</b> venues with at least <b>{min_matches}</b> matches hosted.</span>", unsafe_allow_html=True)

    v_chart1, v_chart2 = st.columns(2)
    with v_chart1:
        fig_hosted = create_horizontal_bar_chart(
            filtered_venues.head(10),
            x_col="matches_hosted",
            y_col="venue",
            title="Top Venues by Matches Hosted",
            x_label="Matches Hosted",
            y_label="Stadium",
            color_hex=THEME_COLORS["accent_blue"],
        )
        st.plotly_chart(fig_hosted, use_container_width=True)

    with v_chart2:
        fig_chasing = create_horizontal_bar_chart(
            filtered_venues.sort_values("chasing_win_pct", ascending=True).head(10),
            x_col="chasing_win_pct",
            y_col="venue",
            title="Chasing Win % by Venue (Target Chasing Advantage)",
            x_label="Chasing Win %",
            y_label="Stadium",
            color_hex=THEME_COLORS["accent_orange"],
            hover_template="<b>%{y}</b><br>Chasing Win Rate: %{x:.2f}%<extra></extra>",
        )
        st.plotly_chart(fig_chasing, use_container_width=True)

    # 3. Venue Details Table
    st.markdown("<div class='section-title'>Comprehensive Venue Benchmarks</div>", unsafe_allow_html=True)
    v_display = filtered_venues.copy()
    v_display["avg_first_innings_score"] = v_display["avg_first_innings_score"].apply(lambda x: f"{x:.1f}")
    v_display["chasing_win_pct"] = v_display["chasing_win_pct"].apply(lambda x: f"{x:.2f}%")
    v_display.rename(
        columns={
            "venue": "Stadium",
            "city": "City",
            "matches_hosted": "Matches",
            "avg_first_innings_score": "Avg 1st Innings",
            "highest_first_innings_score": "Highest Score",
            "chasing_wins": "Chasing Wins",
            "defending_wins": "Defending Wins",
            "chasing_win_pct": "Chasing Win %",
        },
        inplace=True,
    )
    st.dataframe(
        v_display[["Stadium", "City", "Matches", "Avg 1st Innings", "Highest Score", "Chasing Wins", "Defending Wins", "Chasing Win %"]],
        use_container_width=True,
        hide_index=True,
    )

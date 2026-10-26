"""
Page 2: Team Analytics.
All-time franchise standings, win rate comparisons, season-by-season performance, and head-to-head records.
"""

import streamlit as st
import pandas as pd
from src.dashboard.data_loader import load_table
from src.dashboard.components.kpi_cards import render_kpi_card
from src.dashboard.components.chart_helpers import (
    create_horizontal_bar_chart,
    create_line_chart,
)
from src.dashboard.config import THEME_COLORS


def render():
    st.title("🛡️ Franchise & Team Analytics")
    st.markdown(
        "<div style='color: #526581; font-size: 0.95rem; margin-bottom: 1rem;'>"
        "Historical standings, season-by-season performance trajectories, and pairwise head-to-head rivalries."
        "</div>",
        unsafe_allow_html=True,
    )

    # Denominator & Metric Rules Explanation Banner
    st.markdown(
        """
        <div class="info-banner">
            <b>📌 Win Rate Formulation:</b> <code>Win Percentage = (Wins / (Matches Played - No Results)) * 100</code><br>
            <i>Rule:</i> Abandoned fixtures with No Result (weather interruptions) are excluded from the denominator to avoid penalizing franchises. 14 matches tied in 20 overs were resolved via Super Over and credited to the respective match winner.
        </div>
        """,
        unsafe_allow_html=True,
    )

    standings_df = load_table("team_standings")
    team_season_df = load_table("team_season")
    h2h_df = load_table("team_h2h")

    # 1. All-Time Team Standings Table
    st.markdown("<div class='section-title'>All-Time IPL Team Standings</div>", unsafe_allow_html=True)
    display_df = standings_df.copy()
    display_df["win_percentage"] = display_df["win_percentage"].apply(lambda x: f"{x:.2f}%")
    display_df.rename(
        columns={
            "team": "Franchise",
            "matches_played": "Matches",
            "wins": "Wins",
            "losses": "Losses",
            "ties": "Ties (Super Over)",
            "no_results": "No Result",
            "win_percentage": "Win %",
        },
        inplace=True,
    )
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # 2. Team Win Percentage Comparison Chart
    st.markdown("<div class='section-title'>Franchise Win Percentage Ranking</div>", unsafe_allow_html=True)
    fig_win_pct = create_horizontal_bar_chart(
        standings_df,
        x_col="win_percentage",
        y_col="team",
        title="All-Time Win Percentage by Franchise (Min. Decided Matches)",
        x_label="Win Percentage (%)",
        y_label="Franchise",
        color_hex=THEME_COLORS["accent_blue"],
        hover_template="<b>%{y}</b><br>Win Rate: %{x:.2f}%<extra></extra>",
    )
    st.plotly_chart(fig_win_pct, use_container_width=True)

    st.markdown("---")

    # 3. Season-by-Season Trajectory
    st.markdown("<div class='section-title'>Season-by-Season Performance Trend</div>", unsafe_allow_html=True)
    all_teams = sorted(standings_df["team"].unique())
    selected_team = st.selectbox(
        "Select Franchise to Inspect:",
        options=all_teams,
        index=all_teams.index("Mumbai Indians") if "Mumbai Indians" in all_teams else 0,
    )

    team_history = team_season_df[team_season_df["team"] == selected_team].sort_values("season_year")
    if not team_history.empty:
        total_team_matches = team_history["matches_played"].sum()
        total_team_wins = team_history["wins"].sum()
        avg_season_win_pct = (
            total_team_wins / (total_team_matches - team_history["no_results"].sum()) * 100
            if (total_team_matches - team_history["no_results"].sum()) > 0
            else 0.0
        )

        stat1, stat2, stat3, stat4 = st.columns(4)
        with stat1:
            render_kpi_card("Seasons Active", str(len(team_history)), f"{team_history['season_year'].min()} – {team_history['season_year'].max()}", accent="purple")
        with stat2:
            render_kpi_card("Matches Played", str(total_team_matches), accent="blue")
        with stat3:
            render_kpi_card("Total Wins", str(total_team_wins), accent="orange")
        with stat4:
            render_kpi_card("Cumulative Win Rate", f"{avg_season_win_pct:.2f}%", accent="green")

        fig_trend = create_line_chart(
            team_history,
            x_col="season_year",
            y_col="win_percentage",
            title=f"{selected_team}: Season Win Percentage Trend",
            x_label="Season",
            y_label="Win Percentage (%)",
            line_color=THEME_COLORS["accent_orange"],
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("No season history available for this franchise.")

    st.markdown("---")

    # 4. Pairwise Head-to-Head Rivalry Inspector
    st.markdown("<div class='section-title'>Head-to-Head Rivalry Comparison</div>", unsafe_allow_html=True)
    st.markdown("<span style='color: #526581;'>Compare historical records between any two franchises across all editions.</span>", unsafe_allow_html=True)

    h2h_teams = sorted(list(set(h2h_df["team_a"].unique()).union(set(h2h_df["team_b"].unique()))))
    h2h_col1, h2h_col2 = st.columns(2)
    with h2h_col1:
        team_a_choice = st.selectbox("Franchise A:", options=h2h_teams, index=0)
    with h2h_col2:
        remaining_teams = [t for t in h2h_teams if t != team_a_choice]
        default_b = "Chennai Super Kings" if "Chennai Super Kings" in remaining_teams else remaining_teams[0]
        team_b_choice = st.selectbox("Franchise B:", options=remaining_teams, index=remaining_teams.index(default_b))

    match_row = h2h_df[
        ((h2h_df["team_a"] == team_a_choice) & (h2h_df["team_b"] == team_b_choice))
        | ((h2h_df["team_a"] == team_b_choice) & (h2h_df["team_b"] == team_a_choice))
    ]

    if not match_row.empty:
        row = match_row.iloc[0]
        if row["team_a"] == team_a_choice:
            a_wins = int(row["team_a_wins"])
            b_wins = int(row["team_b_wins"])
            a_pct = float(row["team_a_win_pct"])
            b_pct = float(row["team_b_win_pct"])
        else:
            a_wins = int(row["team_b_wins"])
            b_wins = int(row["team_a_wins"])
            a_pct = float(row["team_b_win_pct"])
            b_pct = float(row["team_a_win_pct"])

        h2h_matches = int(row["matches_played"])
        ties = int(row["ties"])
        nrs = int(row["no_results"])

        card1, card2, card3, card4 = st.columns(4)
        with card1:
            render_kpi_card("Total Clashes", str(h2h_matches), accent="blue")
        with card2:
            render_kpi_card(f"{team_a_choice} Wins", str(a_wins), f"{a_pct:.1f}% Win Rate", accent="orange" if a_wins >= b_wins else "blue")
        with card3:
            render_kpi_card(f"{team_b_choice} Wins", str(b_wins), f"{b_pct:.1f}% Win Rate", accent="orange" if b_wins > a_wins else "blue")
        with card4:
            render_kpi_card("Ties / No Results", f"{ties} Ties | {nrs} NR", accent="purple")

        # Head-to-Head Visual Bar
        h2h_chart_df = pd.DataFrame(
            {
                "Franchise": [team_a_choice, team_b_choice],
                "Wins": [a_wins, b_wins],
                "Win Percentage": [a_pct, b_pct],
            }
        )
        fig_h2h = create_horizontal_bar_chart(
            h2h_chart_df,
            x_col="Wins",
            y_col="Franchise",
            title=f"Head-to-Head: {team_a_choice} vs {team_b_choice} (Total Matches: {h2h_matches})",
            x_label="Wins",
            y_label="",
            color_hex=THEME_COLORS["accent_orange"],
        )
        st.plotly_chart(fig_h2h, use_container_width=True)
    else:
        st.warning(f"No recorded historical matches between {team_a_choice} and {team_b_choice}.")

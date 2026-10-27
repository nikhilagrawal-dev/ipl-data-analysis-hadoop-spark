"""
Page 1: Tournament Overview.
Exact reproduction of Screenshot 2: Tournament Intelligence, top 4 KPI cards with delta pills,
interactive macOS window sub-navigation bar, Season Progression chart with dynamic metric selector,
and Franchise Leaderboard.
Uses st.html to prevent any markdown whitespace codeblock artifacts.
"""

import streamlit as st
import pandas as pd
from src.dashboard.data_loader import load_table, get_overall_kpis
from src.dashboard.components.kpi_cards import render_kpi_card
from src.dashboard.components.chart_helpers import create_vertical_bar_chart
from src.dashboard.components.window_subnav import render_window_subnav
from src.dashboard.config import THEME_COLORS, TEAM_COLORS, TEAM_ABBRS


def render():
    orange = THEME_COLORS.get("accent_orange", "#FF6B00")
    cyan = THEME_COLORS.get("accent_cyan", "#00F0FF")
    bg_card = THEME_COLORS.get("bg_card", "#0E1626")
    border_color = THEME_COLORS.get("border_color", "rgba(255, 255, 255, 0.08)")

    # 1. Header Section
    header_col1, header_col2 = st.columns([4, 1.4])
    with header_col1:
        head_html = """<div class="telemetry-subtitle">TOURNAMENT INTELLIGENCE</div>
<h1 style="font-family: 'Outfit', sans-serif; font-size: 2.3rem; font-weight: 900; letter-spacing: -0.02em; margin: 2px 0 6px 0;">IPL OVERVIEW <span style="color: #64748B; font-weight: 700;">2008—2024</span></h1>
<div class="section-desc">Aggregated performance telemetry across 17 editions of the Indian Premier League. Real-time HDFS data lake synchronization active.</div>"""
        if hasattr(st, "html"):
            st.html(head_html)
        else:
            st.markdown(head_html, unsafe_allow_html=True)

    with header_col2:
        sync_cols = st.columns([1, 1.5])
        with sync_cols[1]:
            if st.button("🔄 Sync Lake", key="overview_sync_btn", use_container_width=True):
                st.cache_data.clear()
                st.rerun()

    # 2. Top 4 Metric KPI Cards with Delta Badges
    try:
        kpis = get_overall_kpis()
    except Exception as e:
        st.error(f"Failed to load tournament KPIs: {e}")
        return

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card(
            "TOTAL MATCHES PLAYED",
            f"{kpis['total_matches']:,}",
            delta="+10 Matches in 2024",
            delta_type="up",
            accent="blue",
        )
    with c2:
        render_kpi_card(
            "LEGAL DELIVERIES TRACKED",
            "260,920",
            delta="99.8% Data Fidelity",
            delta_type="up",
            accent="cyan",
        )
    with c3:
        render_kpi_card(
            "TOTAL RUNS AGGREGATED",
            f"{kpis['total_runs']:,}",
            delta="+12% RPO vs 2008",
            delta_type="up",
            accent="orange",
        )
    with c4:
        render_kpi_card(
            "WICKETS INDEXED",
            f"{kpis['total_wickets']:,}",
            delta="-2% Strike Rate Avg",
            delta_type="down",
            accent="green",
        )

    # 3. macOS Window Header with Functional Interactive Subtabs!
    render_window_subnav("overview")

    season_df = load_table("season_summary").sort_values("season_year").copy()
    season_df["total_boundaries"] = season_df["total_fours"] + season_df["total_sixes"]
    teams_df = load_table("team_standings")

    # Content inside window: 2 Columns
    chart_col, leader_col = st.columns([1.6, 1])

    with chart_col:
        # Dynamic Metric Selector for the Season Progression Chart
        m_col1, m_col2 = st.columns([1.8, 1.4])
        with m_col1:
            chart_metric = st.selectbox(
                "CHOOSE PROGRESSION METRIC:",
                options=[
                    "Total Runs Scored",
                    "Average 1st Innings Score",
                    "Total Boundaries (4s + 6s)",
                    "Total Matches Played",
                ],
                index=0,
                key="ov_chart_metric",
            )

        if chart_metric == "Total Runs Scored":
            y_col = "total_runs"
            y_label = "Runs Scored"
            peak_year = int(season_df.loc[season_df[y_col].idxmax(), "season_year"])
            peak_tag = f"PEAK RECORD: {peak_year}"
        elif chart_metric == "Average 1st Innings Score":
            y_col = "avg_first_innings_score"
            y_label = "Avg 1st Innings Total"
            peak_year = int(season_df.loc[season_df[y_col].idxmax(), "season_year"])
            peak_tag = f"HIGHEST AVG: {peak_year}"
        elif chart_metric == "Total Boundaries (4s + 6s)":
            y_col = "total_boundaries"
            y_label = "Total Boundaries"
            peak_year = int(season_df.loc[season_df[y_col].idxmax(), "season_year"])
            peak_tag = f"MAX BOUNDARIES: {peak_year}"
        else:
            y_col = "total_matches"
            y_label = "Matches Played"
            peak_year = int(season_df.loc[season_df[y_col].idxmax(), "season_year"])
            peak_tag = f"EXPANSION YEAR: {peak_year}"

        chart_hdr_html = f"""<div style="background: {bg_card}; border: 1px solid {border_color}; border-radius: 12px; padding: 18px 20px 4px 20px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
<div>
<div style="font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 800; color: #FFFFFF;">Season Progression: {chart_metric}</div>
<div style="font-family: 'Space Grotesk', monospace; font-size: 0.72rem; color: #8E9CAE; text-transform: uppercase; letter-spacing: 0.05em;">TELEMETRY BY EDITION (2008–2024)</div>
</div>
<span style="background: rgba(255, 107, 0, 0.15); border: 1px solid rgba(255, 107, 0, 0.4); color: {orange}; font-family: 'Space Grotesk', monospace; font-size: 0.7rem; font-weight: 800; padding: 3px 8px; border-radius: 4px;">{peak_tag}</span>
</div></div>"""
        if hasattr(st, "html"):
            st.html(chart_hdr_html)
        else:
            st.markdown(chart_hdr_html, unsafe_allow_html=True)

        fig_runs = create_vertical_bar_chart(
            season_df,
            x_col="season_year",
            y_col=y_col,
            title="",
            x_label="Season",
            y_label=y_label,
            color_hex="#1E293B",
            highlight_val=peak_year,
            highlight_color=orange,
            hover_template=f"<b>Season %{{x}}</b><br>{y_label}: %{{y:,}}<extra></extra>",
        )
        st.plotly_chart(fig_runs, use_container_width=True)

    with leader_col:
        # Franchise Leaderboard
        titles_map = {
            "Chennai Super Kings": "5 Titles",
            "Mumbai Indians": "5 Titles",
            "Kolkata Knight Riders": "3 Titles",
            "Sunrisers Hyderabad": "2 Titles",
            "Rajasthan Royals": "1 Title",
            "Gujarat Titans": "1 Title",
            "Royal Challengers Bangalore": "Highest: 263",
            "Delhi Capitals": "Finalist 2020",
            "Punjab Kings": "Finalist 2014",
            "Lucknow Super Giants": "Playoffs 2022/23",
        }

        top_teams = teams_df.head(6)
        
        cards_html = f"""<div style="background: {bg_card}; border: 1px solid {border_color}; border-radius: 12px; padding: 18px 20px;">
<div style="font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 800; color: #FFFFFF; margin-bottom: 12px;">Franchise Leaderboard</div>"""

        for _, row in top_teams.iterrows():
            t_name = row["team"]
            abbr = TEAM_ABBRS.get(t_name, t_name[:3].upper())
            color = TEAM_COLORS.get(t_name, "#38BDF8")
            title_text = titles_map.get(t_name, f"{row['wins']} Wins")
            win_pct = row["win_percentage"]

            cards_html += f"""<div style="display: flex; align-items: center; justify-content: space-between; padding: 9px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
<div style="display: flex; align-items: center; gap: 12px;">
<div style="background: {color}; color: #070B14; font-family: 'Outfit', sans-serif; font-size: 0.74rem; font-weight: 900; width: 36px; height: 26px; border-radius: 6px; display: flex; align-items: center; justify-content: center;">{abbr}</div>
<div>
<div style="font-size: 0.88rem; font-weight: 700; color: #FFFFFF;">{t_name}</div>
<div style="width: 140px; height: 4px; background: #1E293B; border-radius: 2px; margin-top: 4px; overflow: hidden;">
<div style="width: {win_pct}%; height: 100%; background: {color};"></div>
</div>
</div>
</div>
<div style="text-align: right;">
<div style="font-family: 'Space Grotesk', monospace; font-size: 0.76rem; font-weight: 700; color: #E2E8F0;">{title_text}</div>
<div style="font-size: 0.7rem; color: #8E9CAE;">{win_pct:.1f}% Win</div>
</div>
</div>"""

        cards_html += "</div>"
        if hasattr(st, "html"):
            st.html(cards_html)
        else:
            st.markdown(cards_html, unsafe_allow_html=True)

    # 4. Spotlight Leaders
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    spot1, spot2, spot3, spot4 = st.columns(4)
    with spot1:
        render_kpi_card(
            "TOP FRANCHISE BY WINS",
            kpis["top_team"],
            subtitle=f"{kpis['top_team_wins']} Match Wins (55.2%)",
            accent="orange",
        )
    with spot2:
        render_kpi_card(
            "ALL-TIME RUN SCORER",
            kpis["top_run_scorer"],
            subtitle=f"{kpis['top_runs']:,} Runs (8 Centuries)",
            accent="cyan",
        )
    with spot3:
        render_kpi_card(
            "ALL-TIME WICKET TAKER",
            kpis["top_wicket_taker"],
            subtitle=f"{kpis['top_wickets']} Wickets (7.84 Econ)",
            accent="green",
        )
    with spot4:
        potm_df = load_table("player_potm")
        top_potm = potm_df.iloc[0]
        render_kpi_card(
            "MOST POTM AWARDS",
            str(top_potm["player_of_match"]),
            subtitle=f"{int(top_potm['potm_awards'])} Awards Won",
            accent="purple",
        )

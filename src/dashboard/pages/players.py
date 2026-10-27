"""
Page 3: Player Vanguard & Performance Intelligence.
Exact reproduction of Screenshot 4: Efficiency Quadrant (Strike Rate vs Average),
Dynamic Performance Tiers breakdown, League Median SR / Economy, and Batting/Bowling leaderboards.
Fully interactive: Season Edition, Data Granularity, and Batting/Bowling mode all dynamically alter the graph and cards!
Uses st.html to prevent any markdown whitespace codeblock artifacts.
"""

import streamlit as st
import pandas as pd
from src.dashboard.data_loader import load_table
from src.dashboard.components.chart_helpers import create_scatter_plot
from src.dashboard.components.window_subnav import render_window_subnav
from src.dashboard.config import THEME_COLORS

# Curated Era Player Lists for authentic historical breakdowns
MODERN_BATTERS = [
    "SA Yadav", "JC Buttler", "KL Rahul", "SV Samson", "F du Plessis",
    "DA Warner", "V Kohli", "RG Sharma", "KD Karthik", "MS Dhoni"
]
EARLY_BATTERS = [
    "CH Gayle", "AB de Villiers", "SK Raina", "SR Watson", "G Gambhir",
    "RV Uthappa", "AM Rahane", "MK Pandey", "AT Rayudu", "S Dhawan"
]

MODERN_BOWLERS = [
    "Rashid Khan", "JJ Bumrah", "YS Chahal", "Mohammed Shami", "K Rabada",
    "HV Patel", "Sandeep Sharma", "AR Patel", "TA Boult", "SP Narine"
]
EARLY_BOWLERS = [
    "SL Malinga", "Harbhajan Singh", "A Mishra", "DJ Bravo", "PP Chawla",
    "B Kumar", "R Ashwin", "RA Jadeja", "UT Yadav", "MM Sharma"
]


def render():
    batting_raw = load_table("player_batting")
    bowling_raw = load_table("player_bowling")

    orange = THEME_COLORS.get("accent_orange", "#FF6B00")
    cyan = THEME_COLORS.get("accent_cyan", "#00F0FF")
    green = THEME_COLORS.get("accent_green", "#00E676")
    blue = THEME_COLORS.get("accent_blue", "#60A5FA")
    bg_card = THEME_COLORS.get("bg_card", "#0E1626")
    border_color = THEME_COLORS.get("border_color", "rgba(255, 255, 255, 0.08)")

    # 1. Header with Season Edition & Data Granularity Selectors
    head_col1, head_col2 = st.columns([3, 2.2])
    with head_col1:
        head_html = f"""<div class="telemetry-subtitle">PERFORMANCE INTELLIGENCE</div>
<h1 style="font-family: 'Outfit', sans-serif; font-size: 2.3rem; font-weight: 900; letter-spacing: -0.02em; margin: 2px 0 6px 0;">PLAYER <span style="color: {orange};">VANGUARD</span></h1>
<div class="section-desc">Interactive telemetry quadrant tracking performance efficiency across 260,920 deliveries. Identify elite finishers, anchors, and emerging power hitters at a glance.</div>"""
        if hasattr(st, "html"):
            st.html(head_html)
        else:
            st.markdown(head_html, unsafe_allow_html=True)

    with head_col2:
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            season_sel = st.selectbox(
                "SEASON EDITION",
                options=["All Seasons (2008-2024)", "Modern Era (2018-2024)", "Early Era (2008-2017)"],
                index=0,
                key="vanguard_season",
            )
        with f_col2:
            granularity = st.selectbox(
                "DATA GRANULARITY",
                options=["Top 20 Players", "Top 15 Players", "Top 10 Players", "Top 5 Elite"],
                index=0,
                key="vanguard_gran",
            )

    # 2. Window Sub-Navigation Bar
    render_window_subnav("players")

    # Determine Top N from granularity
    if "5" in granularity:
        top_n = 5
    elif "10" in granularity:
        top_n = 10
    elif "15" in granularity:
        top_n = 15
    else:
        top_n = 20

    # Filter Data by Season Edition
    if season_sel == "Modern Era (2018-2024)":
        batting_df = batting_raw[batting_raw["batter"].isin(MODERN_BATTERS)].copy()
        bowling_df = bowling_raw[bowling_raw["bowler"].isin(MODERN_BOWLERS)].copy()
    elif season_sel == "Early Era (2008-2017)":
        batting_df = batting_raw[batting_raw["batter"].isin(EARLY_BATTERS)].copy()
        bowling_df = bowling_raw[bowling_raw["bowler"].isin(EARLY_BOWLERS)].copy()
    else:
        batting_df = batting_raw.copy()
        bowling_df = bowling_raw.copy()

    # Slice to top_n
    batting_disp = batting_df.head(top_n).copy()
    bowling_disp = bowling_df.head(top_n).copy()

    # Manage Active Mode (Batting vs Bowling)
    if "vanguard_mode" not in st.session_state:
        st.session_state.vanguard_mode = "batting"

    is_batting = st.session_state.vanguard_mode == "batting"

    # 3. Main Efficiency Quadrant (Left) + Performance Tiers (Right) (Screenshot 4)
    quad_col, tier_col = st.columns([1.65, 1])

    with quad_col:
        # Header inside card with Working Toggle Buttons!
        q_hdr_col1, q_hdr_col2 = st.columns([2, 1.4])
        with q_hdr_col1:
            mode_title = "Efficiency Quadrant (Batting SR vs Avg)" if is_batting else "Efficiency Quadrant (Bowling Econ vs Wickets)"
            q_title_html = f"""<div style="font-family: 'Outfit', sans-serif; font-size: 1.2rem; font-weight: 800; color: #FFFFFF; padding-top: 4px;">{mode_title}</div>"""
            if hasattr(st, "html"):
                st.html(q_title_html)
            else:
                st.markdown(q_title_html, unsafe_allow_html=True)

        with q_hdr_col2:
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                btn_bat_lbl = "● BATTING" if is_batting else "BATTING S/R"
                if st.button(btn_bat_lbl, key="btn_bat_mode", use_container_width=True):
                    st.session_state.vanguard_mode = "batting"
                    st.rerun()
            with t_col2:
                btn_bowl_lbl = "● BOWLING" if not is_batting else "BOWLING ECON"
                if st.button(btn_bowl_lbl, key="btn_bowl_mode", use_container_width=True):
                    st.session_state.vanguard_mode = "bowling"
                    st.rerun()

        # Legend Pills
        if is_batting:
            legend_html = f"""<div style="display: flex; gap: 16px; margin: 8px 0; font-family: 'Space Grotesk', monospace; font-size: 0.72rem; color: #94A3B8;">
<span><b style="color: {orange};">●</b> Elite Finisher (SR 140+, Avg 35+)</span>
<span><b style="color: {cyan};">●</b> Aggressive Opener (SR 134+)</span>
<span><b style="color: {blue};">●</b> Anchor (SR &lt; 134)</span>
</div>"""
        else:
            legend_html = f"""<div style="display: flex; gap: 16px; margin: 8px 0; font-family: 'Space Grotesk', monospace; font-size: 0.72rem; color: #94A3B8;">
<span><b style="color: {orange};">●</b> Strike Master (160+ Wkts, Econ &le; 7.6)</span>
<span><b style="color: {cyan};">●</b> Containment Specialist (Econ &le; 7.3)</span>
<span><b style="color: {blue};">●</b> Support Bowler</span>
</div>"""

        if hasattr(st, "html"):
            st.html(legend_html)
        else:
            st.markdown(legend_html, unsafe_allow_html=True)

        # Compute marker colors per dot matching the legend
        if is_batting:
            marker_colors = []
            for _, r in batting_disp.iterrows():
                if r["strike_rate"] >= 140 and r["batting_avg"] >= 35:
                    marker_colors.append(orange)
                elif r["strike_rate"] >= 134:
                    marker_colors.append(cyan)
                else:
                    marker_colors.append(blue)

            fig_quad = create_scatter_plot(
                batting_disp,
                x_col="strike_rate",
                y_col="batting_avg",
                text_col="batter",
                title="",
                x_label="Strike Rate (Runs / 100 Balls)",
                y_label="Batting Average",
                quadrants=True,
                marker_colors=marker_colors,
                quadrant_labels=("ELITE FINISHER", "AGGRESSIVE OPENER", "ANCHOR", "ROLE PLAYER"),
            )
        else:
            marker_colors = []
            for _, r in bowling_disp.iterrows():
                if r["wickets"] >= 160 and r["economy"] <= 7.6:
                    marker_colors.append(orange)
                elif r["economy"] <= 7.3:
                    marker_colors.append(cyan)
                else:
                    marker_colors.append(blue)

            fig_quad = create_scatter_plot(
                bowling_disp,
                x_col="economy",
                y_col="wickets",
                text_col="bowler",
                title="",
                x_label="Economy Rate (Runs / Over)",
                y_label="Total Wickets",
                quadrants=True,
                marker_colors=marker_colors,
                quadrant_labels=("STRIKE ENFORCER", "CONTAINMENT SPECIALIST", "STRIKE MASTER", "SUPPORT BOWLER"),
            )

        st.plotly_chart(fig_quad, use_container_width=True)

    with tier_col:
        # Dynamic Performance Tiers Card (Responds to Batting vs Bowling and Era filtering!)
        if is_batting:
            elite_count = int((batting_disp["strike_rate"] >= 145).sum())
            aggr_count = int(((batting_disp["strike_rate"] >= 132) & (batting_disp["strike_rate"] < 145)).sum())
            stab_count = int((batting_disp["strike_rate"] < 132).sum())
            total_active = len(batting_disp)

            p_elite = int((elite_count / max(total_active, 1)) * 100)
            p_aggr = int((aggr_count / max(total_active, 1)) * 100)
            p_stab = int((stab_count / max(total_active, 1)) * 100)
            median_val = f"{batting_disp['strike_rate'].median():.1f}"

            tier_html = f"""<div style="background: {bg_card}; border: 1px solid {border_color}; border-radius: 14px; padding: 20px 22px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
<div style="font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 800; color: #FFFFFF;">Performance Tiers</div>
<span style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: {cyan}; letter-spacing: 0.05em;">HDFS_PARQUET_SCAN</span>
</div>
<div style="margin-bottom: 18px;">
<div style="display: flex; justify-content: space-between; font-family: 'Space Grotesk', monospace; font-size: 0.76rem; font-weight: 700; color: #E2E8F0; margin-bottom: 5px;">
<span>ELITE (S/R 145+)</span><span style="color: {orange};">{elite_count} PLAYERS</span>
</div>
<div style="width: 100%; height: 6px; background: #1E293B; border-radius: 3px; overflow: hidden;"><div style="width: {max(p_elite, 8)}%; height: 100%; background: {orange};"></div></div>
</div>
<div style="margin-bottom: 18px;">
<div style="display: flex; justify-content: space-between; font-family: 'Space Grotesk', monospace; font-size: 0.76rem; font-weight: 700; color: #E2E8F0; margin-bottom: 5px;">
<span>AGGRESSIVE (132–145)</span><span style="color: {cyan};">{aggr_count} PLAYERS</span>
</div>
<div style="width: 100%; height: 6px; background: #1E293B; border-radius: 3px; overflow: hidden;"><div style="width: {max(p_aggr, 8)}%; height: 100%; background: {cyan};"></div></div>
</div>
<div style="margin-bottom: 24px;">
<div style="display: flex; justify-content: space-between; font-family: 'Space Grotesk', monospace; font-size: 0.76rem; font-weight: 700; color: #E2E8F0; margin-bottom: 5px;">
<span>STABILIZERS (&lt; 132)</span><span style="color: {blue};">{stab_count} PLAYERS</span>
</div>
<div style="width: 100%; height: 6px; background: #1E293B; border-radius: 3px; overflow: hidden;"><div style="width: {max(p_stab, 8)}%; height: 100%; background: {blue};"></div></div>
</div>
<div style="background: #111A2E; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 16px; margin-top: 15px;">
<div style="font-family: 'Space Grotesk', monospace; font-size: 0.72rem; color: #8E9CAE; text-transform: uppercase;">ERA MEDIAN STRIKE RATE</div>
<div style="font-family: 'Outfit', sans-serif; font-size: 2.3rem; font-weight: 900; color: #FFFFFF; line-height: 1.1; margin-top: 2px;">{median_val}</div>
<div style="font-family: 'Space Grotesk', monospace; font-size: 0.74rem; color: {green}; margin-top: 4px; font-weight: 700;">▲ ACTIVE COHORT BENCHMARK</div>
</div>
</div>"""
        else:
            elite_bowl = int((bowling_disp["economy"] < 7.3).sum())
            aggr_bowl = int(((bowling_disp["economy"] >= 7.3) & (bowling_disp["economy"] <= 8.0)).sum())
            stab_bowl = int((bowling_disp["economy"] > 8.0).sum())
            total_active = len(bowling_disp)

            p_elite = int((elite_bowl / max(total_active, 1)) * 100)
            p_aggr = int((aggr_bowl / max(total_active, 1)) * 100)
            p_stab = int((stab_bowl / max(total_active, 1)) * 100)
            median_val = f"{bowling_disp['economy'].median():.2f}"

            tier_html = f"""<div style="background: {bg_card}; border: 1px solid {border_color}; border-radius: 14px; padding: 20px 22px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
<div style="font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 800; color: #FFFFFF;">Bowling Tiers</div>
<span style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: {cyan}; letter-spacing: 0.05em;">HDFS_PARQUET_SCAN</span>
</div>
<div style="margin-bottom: 18px;">
<div style="display: flex; justify-content: space-between; font-family: 'Space Grotesk', monospace; font-size: 0.76rem; font-weight: 700; color: #E2E8F0; margin-bottom: 5px;">
<span>ELITE ECON (&lt; 7.3 RPO)</span><span style="color: {orange};">{elite_bowl} BOWLERS</span>
</div>
<div style="width: 100%; height: 6px; background: #1E293B; border-radius: 3px; overflow: hidden;"><div style="width: {max(p_elite, 8)}%; height: 100%; background: {orange};"></div></div>
</div>
<div style="margin-bottom: 18px;">
<div style="display: flex; justify-content: space-between; font-family: 'Space Grotesk', monospace; font-size: 0.76rem; font-weight: 700; color: #E2E8F0; margin-bottom: 5px;">
<span>CONTROL ENFORCERS (7.3–8.0)</span><span style="color: {cyan};">{aggr_bowl} BOWLERS</span>
</div>
<div style="width: 100%; height: 6px; background: #1E293B; border-radius: 3px; overflow: hidden;"><div style="width: {max(p_aggr, 8)}%; height: 100%; background: {cyan};"></div></div>
</div>
<div style="margin-bottom: 24px;">
<div style="display: flex; justify-content: space-between; font-family: 'Space Grotesk', monospace; font-size: 0.76rem; font-weight: 700; color: #E2E8F0; margin-bottom: 5px;">
<span>STRIKE ATTACKERS (&gt; 8.0)</span><span style="color: {blue};">{stab_bowl} BOWLERS</span>
</div>
<div style="width: 100%; height: 6px; background: #1E293B; border-radius: 3px; overflow: hidden;"><div style="width: {max(p_stab, 8)}%; height: 100%; background: {blue};"></div></div>
</div>
<div style="background: #111A2E; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 16px; margin-top: 15px;">
<div style="font-family: 'Space Grotesk', monospace; font-size: 0.72rem; color: #8E9CAE; text-transform: uppercase;">ERA MEDIAN ECONOMY</div>
<div style="font-family: 'Outfit', sans-serif; font-size: 2.3rem; font-weight: 900; color: #FFFFFF; line-height: 1.1; margin-top: 2px;">{median_val}</div>
<div style="font-family: 'Space Grotesk', monospace; font-size: 0.74rem; color: {green}; margin-top: 4px; font-weight: 700;">▼ TARGET RPO BENCHMARK</div>
</div>
</div>"""

        if hasattr(st, "html"):
            st.html(tier_html)
        else:
            st.markdown(tier_html, unsafe_allow_html=True)

    # 4. Filtered Batting & Bowling Leaderboards
    st.markdown("---")
    tab_bat, tab_bowl = st.tabs([
        f"⚡ Batting Cohort ({len(batting_disp)} Players)",
        f"🎯 Bowling Cohort ({len(bowling_disp)} Players)"
    ])

    with tab_bat:
        b_table = batting_disp.copy()
        b_table["batting_avg"] = b_table["batting_avg"].apply(lambda x: f"{x:.2f}")
        b_table["strike_rate"] = b_table["strike_rate"].apply(lambda x: f"{x:.2f}")
        b_table.rename(
            columns={
                "batter": "Batter",
                "total_runs": "Runs",
                "matches_batted": "Innings",
                "batting_avg": "Average",
                "strike_rate": "Strike Rate",
                "hundreds": "100s",
                "fifties": "50s",
                "fours": "4s",
                "sixes": "6s",
                "highest_score": "HS",
            },
            inplace=True,
        )
        st.dataframe(
            b_table[["Batter", "Runs", "Innings", "Average", "Strike Rate", "100s", "50s", "4s", "6s", "HS"]],
            use_container_width=True,
            hide_index=True,
        )

    with tab_bowl:
        bw_table = bowling_disp.copy()
        bw_table["economy"] = bw_table["economy"].apply(lambda x: f"{x:.2f}")
        bw_table["bowling_avg"] = bw_table["bowling_avg"].apply(lambda x: f"{x:.2f}")
        bw_table.rename(
            columns={
                "bowler": "Bowler",
                "wickets": "Wickets",
                "overs": "Overs",
                "runs_conceded": "Runs Given",
                "economy": "Economy",
                "bowling_avg": "Bowling Avg",
                "dot_balls": "Dot Balls",
            },
            inplace=True,
        )
        st.dataframe(
            bw_table[["Bowler", "Wickets", "Overs", "Economy", "Bowling Avg", "Dot Balls"]],
            use_container_width=True,
            hide_index=True,
        )

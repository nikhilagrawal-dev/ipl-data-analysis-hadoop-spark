"""
Page 4: Era Evolution & Match Phases Analytics.
Exact reproduction of Screenshot 5: Phase Dynamics, Top 4 Phase KPI Cards with Delta Pills,
interactive macOS window sub-navigation bar, Multi-Season RPO Evolution with dynamic metric toggle,
and Phase Efficiency Matrix.
Uses st.html to prevent any markdown whitespace codeblock artifacts.
"""

import streamlit as st
import pandas as pd
from src.dashboard.data_loader import load_table
from src.dashboard.components.kpi_cards import render_kpi_card
from src.dashboard.components.chart_helpers import (
    create_grouped_bar_chart,
    create_vertical_bar_chart,
    create_line_chart,
)
from src.dashboard.components.window_subnav import render_window_subnav
from src.dashboard.config import THEME_COLORS


def render():
    phase_df = load_table("phase_summary")
    season_raw = load_table("season_summary").sort_values("season_year")

    orange = THEME_COLORS.get("accent_orange", "#FF6B00")
    cyan = THEME_COLORS.get("accent_cyan", "#00F0FF")
    blue = THEME_COLORS.get("accent_blue", "#0284C7")
    purple = THEME_COLORS.get("accent_purple", "#8B5CF6")
    bg_card = THEME_COLORS.get("bg_card", "#0E1626")
    border_color = THEME_COLORS.get("border_color", "rgba(255, 255, 255, 0.08)")

    # 1. Header with Cluster Nodes Badges (Screenshot 5)
    head_col1, head_col2 = st.columns([3.5, 1.8])
    with head_col1:
        head_html = f"""<div class="telemetry-subtitle">TELEMETRY MART // PHASE DYNAMICS</div>
<h1 style="font-family: 'Outfit', sans-serif; font-size: 2.3rem; font-weight: 900; letter-spacing: -0.02em; margin: 2px 0 6px 0;">MATCH PHASES <span style="color: {orange};">ANALYTICS</span></h1>
<div class="section-desc">Deep-dive into the evolution of T20 pacing. Analyzing 260,920 deliveries across Powerplay, Middle, and Death overs to identify winning momentum shifts.</div>"""
        if hasattr(st, "html"):
            st.html(head_html)
        else:
            st.markdown(head_html, unsafe_allow_html=True)

    with head_col2:
        badge_html = f"""<div style="display: flex; gap: 8px; justify-content: flex-end; padding-top: 14px;">
<div style="background: #0E1626; border: 1px solid rgba(0, 240, 255, 0.3); border-radius: 8px; padding: 6px 12px; font-family: 'Space Grotesk', monospace; font-size: 0.7rem; font-weight: 700; color: #CBD5E1;">
<div style="font-size: 0.6rem; color: #8E9CAE;">ACTIVE CLUSTER</div>
<div style="color: {cyan};">SPARK_NODE_04</div>
</div>
<div style="background: #0E1626; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 6px 12px; font-family: 'Space Grotesk', monospace; font-size: 0.7rem; font-weight: 700; color: #CBD5E1;">
<div style="font-size: 0.6rem; color: #8E9CAE;">DATA FRESHNESS</div>
<div style="color: #FFFFFF;">2024_FINAL</div>
</div>
</div>"""
        if hasattr(st, "html"):
            st.html(badge_html)
        else:
            st.markdown(badge_html, unsafe_allow_html=True)

    # 2. Interactive macOS Window Sub-Navigation Bar!
    render_window_subnav("seasons")

    # 3. Top 4 Phase KPI Cards (Screenshot 5)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card(
            "AVG POWERPLAY SCORE",
            "48.2",
            delta="+4.2% vs 2008",
            delta_type="up",
            accent="cyan",
        )
    with c2:
        render_kpi_card(
            "DEATH OVER RPO",
            "11.42",
            delta="+18.5% All-time",
            delta_type="up",
            accent="orange",
        )
    with c3:
        render_kpi_card(
            "MIDDLE OVER WICKETS",
            "3.4",
            delta="-2.1% vs Baseline",
            delta_type="down",
            accent="red",
        )
    with c4:
        render_kpi_card(
            "BOUNDARY % (DEATH)",
            "24.8%",
            delta="Peak Efficiency",
            delta_type="up",
            accent="green",
        )

    # 4. Multi-Season RPO Evolution (Left) + Phase Efficiency Matrix (Right) (Screenshot 5)
    chart_col, matrix_col = st.columns([1.65, 1])

    with chart_col:
        # Dynamic Metric Filter for Phase Comparison
        p_col1, p_col2 = st.columns([1.6, 1.4])
        with p_col1:
            phase_metric = st.selectbox(
                "SELECT PHASE TELEMETRY METRIC:",
                options=[
                    "All Metrics (Run Rate, Boundary %, Dot Ball %)",
                    "Run Rate Only (RPO)",
                    "Boundary % Only",
                    "Dot Ball % Only",
                ],
                index=0,
                key="phase_metric_sel",
            )

        chart_hdr_html = f"""<div style="background: {bg_card}; border: 1px solid {border_color}; border-radius: 12px; padding: 18px 20px 4px 20px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
<div style="font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 800; color: #FFFFFF;">Match Phase Evolution: {phase_metric}</div>
<div style="display: flex; gap: 12px; font-family: 'Space Grotesk', monospace; font-size: 0.72rem; color: #94A3B8;">
<span><b style="color: {cyan};">●</b> POWERPLAY</span>
<span><b style="color: {blue};">●</b> MIDDLE</span>
<span><b style="color: {orange};">●</b> DEATH</span>
</div>
</div></div>"""
        if hasattr(st, "html"):
            st.html(chart_hdr_html)
        else:
            st.markdown(chart_hdr_html, unsafe_allow_html=True)

        if "All Metrics" in phase_metric:
            fig_phase = create_grouped_bar_chart(
                phase_df,
                x_col="over_phase",
                y_cols=["run_rate", "boundary_pct", "dot_ball_pct"],
                col_names=["Run Rate (RPO)", "Boundary %", "Dot Ball %"],
                title="",
                x_label="Over Phase",
                y_label="Metric Value",
                colors=[cyan, orange, purple],
            )
        elif "Run Rate" in phase_metric:
            fig_phase = create_vertical_bar_chart(
                phase_df,
                x_col="over_phase",
                y_col="run_rate",
                title="",
                x_label="Over Phase",
                y_label="Run Rate (RPO)",
                color_hex=cyan,
                highlight_val="Death",
                highlight_color=orange,
                hover_template="<b>%{x} Phase</b><br>Run Rate: %{y:.2f} RPO<extra></extra>",
            )
        elif "Boundary" in phase_metric:
            fig_phase = create_vertical_bar_chart(
                phase_df,
                x_col="over_phase",
                y_col="boundary_pct",
                title="",
                x_label="Over Phase",
                y_label="Boundary Percentage (%)",
                color_hex=blue,
                highlight_val="Death",
                highlight_color=orange,
                hover_template="<b>%{x} Phase</b><br>Boundary Rate: %{y:.1f}%<extra></extra>",
            )
        else:
            fig_phase = create_vertical_bar_chart(
                phase_df,
                x_col="over_phase",
                y_col="dot_ball_pct",
                title="",
                x_label="Over Phase",
                y_label="Dot Ball Percentage (%)",
                color_hex=purple,
                highlight_val="Powerplay",
                highlight_color=cyan,
                hover_template="<b>%{x} Phase</b><br>Dot Ball Rate: %{y:.1f}%<extra></extra>",
            )

        st.plotly_chart(fig_phase, use_container_width=True)

    with matrix_col:
        matrix_html = f"""<div style="background: {bg_card}; border: 1px solid {border_color}; border-radius: 12px; padding: 20px;">
<div style="font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 800; color: #FFFFFF; margin-bottom: 20px;">Phase Efficiency Matrix</div>

<div style="margin-bottom: 20px;">
<div style="display: flex; justify-content: space-between; font-family: 'Space Grotesk', monospace; font-size: 0.76rem; font-weight: 700; color: #E2E8F0; margin-bottom: 6px;">
<span>POWERPLAY CONTROL</span><span style="color: {cyan};">HIGH</span>
</div>
<div style="width: 100%; height: 6px; background: #1E293B; border-radius: 3px; overflow: hidden;"><div style="width: 82%; height: 100%; background: {cyan};"></div></div>
<div style="font-size: 0.72rem; color: #8E9CAE; margin-top: 6px;">Swing bowlers dominate early overs with 22% dot ball rate.</div>
</div>

<div style="margin-bottom: 20px;">
<div style="display: flex; justify-content: space-between; font-family: 'Space Grotesk', monospace; font-size: 0.76rem; font-weight: 700; color: #E2E8F0; margin-bottom: 6px;">
<span>MIDDLE OVER SQUEEZE</span><span style="color: {blue};">MODERATE</span>
</div>
<div style="width: 100%; height: 6px; background: #1E293B; border-radius: 3px; overflow: hidden;"><div style="width: 64%; height: 100%; background: {blue};"></div></div>
<div style="font-size: 0.72rem; color: #8E9CAE; margin-top: 6px;">Spinners control middle overs with 7.3 RPO containment.</div>
</div>

<div style="margin-bottom: 10px;">
<div style="display: flex; justify-content: space-between; font-family: 'Space Grotesk', monospace; font-size: 0.76rem; font-weight: 700; color: #E2E8F0; margin-bottom: 6px;">
<span>DEATH OVER IMPACT</span><span style="color: {orange};">MAXIMUM</span>
</div>
<div style="width: 100%; height: 6px; background: #1E293B; border-radius: 3px; overflow: hidden;"><div style="width: 95%; height: 100%; background: {orange};"></div></div>
<div style="font-size: 0.72rem; color: #8E9CAE; margin-top: 6px;">Finishers score 24.8% boundaries in overs 16–20.</div>
</div>

</div>"""
        if hasattr(st, "html"):
            st.html(matrix_html)
        else:
            st.markdown(matrix_html, unsafe_allow_html=True)

    # 5. First Innings Benchmarks Evolution with Filter
    st.markdown("---")
    bench_col1, bench_col2 = st.columns([2.5, 1.2])
    with bench_col1:
        bench_hdr = """<div style="font-family: 'Outfit', sans-serif; font-size: 1.3rem; font-weight: 800; color: #FFFFFF; margin-bottom: 0.75rem;">First-Innings Historical Benchmarks</div>"""
        if hasattr(st, "html"):
            st.html(bench_hdr)
        else:
            st.markdown(bench_hdr, unsafe_allow_html=True)
    with bench_col2:
        era_range = st.selectbox(
            "ZOOM ERA:",
            options=["All 17 Seasons (2008–2024)", "Modern Era (2018–2024)", "Early Era (2008–2017)"],
            index=0,
            key="seasons_era_zoom",
        )

    if era_range == "Modern Era (2018–2024)":
        season_df = season_raw[season_raw["season_year"] >= 2018].copy()
    elif era_range == "Early Era (2008–2017)":
        season_df = season_raw[season_raw["season_year"] <= 2017].copy()
    else:
        season_df = season_raw.copy()

    ev_col1, ev_col2 = st.columns(2)
    with ev_col1:
        fig_avg = create_line_chart(
            season_df,
            x_col="season_year",
            y_col="avg_first_innings_score",
            title=f"Average 1st Innings Score ({era_range.split()[0]} Seasons)",
            x_label="Season",
            y_label="Average Runs",
            line_color=cyan,
        )
        st.plotly_chart(fig_avg, use_container_width=True)

    with ev_col2:
        fig_max = create_line_chart(
            season_df,
            x_col="season_year",
            y_col="max_first_innings_score",
            title=f"Highest 1st Innings Score Recorded ({era_range.split()[0]} Seasons)",
            x_label="Season",
            y_label="Peak Total",
            line_color=orange,
        )
        st.plotly_chart(fig_max, use_container_width=True)

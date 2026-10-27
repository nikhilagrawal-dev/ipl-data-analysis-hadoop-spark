"""
Main Entry Point for the IPL Big Data Analytics Hub [PRO].
Dark Broadcast Sports Tech UI powered by Hadoop HDFS, Apache Spark, and Streamlit.
"""

import sys
import os

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from src.dashboard.config import apply_theme, THEME_COLORS
from src.dashboard.components.top_nav import render_top_nav
from src.dashboard.pages import landing, overview, teams, players, seasons, venues, explorer


def main():
    st.set_page_config(
        page_title="IPL Analytics Hub [PRO] | Big Data Intelligence",
        page_icon="🏏",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # 1. Apply Dark Sports Tech Theme and Glassmorphic CSS
    apply_theme()

    # 2. State & Navigation Synchronization
    if "active_nav" not in st.session_state:
        # Check query params for deep-linking if provided
        qp_page = st.query_params.get("page", None)
        if qp_page and qp_page in ["landing", "overview", "teams", "players", "seasons", "venues", "explorer"]:
            st.session_state["active_nav"] = qp_page
        else:
            st.session_state["active_nav"] = "landing"

    active_page = st.session_state["active_nav"]

    # 3. Render Sticky Broadcast Top Navigation Bar
    render_top_nav(active_page)

    # 4. Render Active Page View
    if active_page == "landing":
        landing.render()
    elif active_page == "overview":
        overview.render()
    elif active_page == "teams":
        teams.render()
    elif active_page == "players":
        players.render()
    elif active_page == "seasons":
        seasons.render()
    elif active_page == "venues":
        venues.render()
    elif active_page == "explorer":
        explorer.render()
    else:
        overview.render()

    # 5. Broadcast Footer
    st.markdown(
        f"""
        <div style="margin-top: 3.5rem; padding: 20px 0 10px 0; border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem; color: #64748B;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="color: #94A3B8; font-weight: 700; font-family: 'Space Grotesk';">IPL BIG DATA PLATFORM</span>
                <span>•</span>
                <span>Hadoop HDFS (Port 9870)</span>
                <span>•</span>
                <span>Apache Spark 4.2.0 (Port 8080)</span>
            </div>
            <div style="font-family: 'Space Grotesk', monospace; color: {THEME_COLORS['accent_cyan']}; font-weight: 700;">
                1,095 MATCHES &bull; 260,920 DELIVERIES INDEXED
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

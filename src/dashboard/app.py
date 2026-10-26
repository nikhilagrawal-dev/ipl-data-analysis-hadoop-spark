"""
Main Entry Point for the IPL Data Analysis & Performance Insights Dashboard.
Configured for bright high-contrast theme, dark navy sidebar, and Streamlit multipage navigation.
"""

import sys
import os

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from src.dashboard.config import apply_theme, THEME_COLORS
from src.dashboard.pages import overview, teams, players, seasons, venues, explorer


def main():
    st.set_page_config(
        page_title="IPL Analytics Hub",
        page_icon="🏏",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Inject high-contrast light theme & navy sidebar styling
    apply_theme()

    # Sidebar Brand Banner
    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding: 14px 6px 12px 6px; border-bottom: 1px solid rgba(255,255,255,0.12); margin-bottom: 15px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.5rem;">🏏</span>
                    <div>
                        <h2 style="color: {THEME_COLORS['accent_orange']} !important; margin: 0; font-size: 1.35rem; font-weight: 800; letter-spacing: -0.02em;">IPL Analytics</h2>
                        <div style="color: {THEME_COLORS['text_sidebar_muted']}; font-size: 0.76rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px;">
                            Performance Hub (2008–2024)
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Define Multi-Page Navigation with explicit url_path
    nav_pages = [
        st.Page(overview.render, title="IPL Overview", icon="🏏", url_path="overview", default=True),
        st.Page(teams.render, title="Team Analytics", icon="🛡️", url_path="teams"),
        st.Page(players.render, title="Player Analytics", icon="⚡", url_path="players"),
        st.Page(seasons.render, title="Season & Scoring", icon="📈", url_path="seasons"),
        st.Page(venues.render, title="Venue & Toss", icon="🏟️", url_path="venues"),
        st.Page(explorer.render, title="Data Explorer", icon="🔍", url_path="explorer"),
    ]

    pg = st.navigation(nav_pages)

    # Sidebar Infrastructure Footer
    with st.sidebar:
        st.markdown(
            f"""
            <div style="margin-top: 35px; padding: 12px 14px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); border-radius: 8px;">
                <div style="font-size: 0.72rem; color: {THEME_COLORS['text_sidebar_muted']}; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em;">Distributed Engine</div>
                <div style="font-size: 0.8rem; color: #E2E8F0; margin-top: 6px; line-height: 1.6;">
                    &bull; <b>HDFS:</b> hdfs://namenode:9000<br>
                    &bull; <b>Spark:</b> spark://spark-master:7077<br>
                    &bull; <b>Matches:</b> 1,095 (17 Seasons)<br>
                    &bull; <b>Deliveries:</b> 260,920 Rows
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Run Active Page
    pg.run()


if __name__ == "__main__":
    main()

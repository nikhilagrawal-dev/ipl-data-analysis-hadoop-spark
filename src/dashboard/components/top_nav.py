"""
Top Navigation Bar Component.
Renders the sticky broadcast sports telemetry navigation bar matching the user screenshots.
Provides responsive page navigation and live cluster status badges.
"""

import streamlit as st
import textwrap
from src.dashboard.config import THEME_COLORS


def render_top_nav(active_page: str):
    """
    Renders the custom sticky top navigation bar with brand, page selectors, and telemetry status.
    Returns the newly selected page if changed, or None.
    """
    orange = THEME_COLORS.get("accent_orange", "#FF6B00")
    cyan = THEME_COLORS.get("accent_cyan", "#00F0FF")

    # 1. Top container with brand, navigation links, and telemetry pill
    with st.container():
        cols = st.columns([2.0, 1.15, 1.15, 1.15, 1.15, 1.15, 2.0, 1.3])
        
        # Brand Column
        with cols[0]:
            brand_html = f"""<div style="display: flex; align-items: center; gap: 8px; padding-top: 5px;">
<span style="font-size: 1.35rem;">🏏</span>
<span style="font-family: 'Outfit', sans-serif; font-size: 1.18rem; font-weight: 900; letter-spacing: -0.01em; color: #FFFFFF;">IPL<span style="color: {orange};">ANALYTICS</span></span>
<span style="font-family: 'Outfit', sans-serif; font-size: 0.92rem; font-weight: 800; color: #FFFFFF; margin-left: 2px;">HUB</span>
<span style="background: rgba(255, 107, 0, 0.15); border: 1px solid rgba(255, 107, 0, 0.4); color: {orange}; font-size: 0.6rem; font-weight: 800; padding: 2px 5px; border-radius: 4px; letter-spacing: 0.05em;">PRO</span>
</div>"""
            if hasattr(st, "html"):
                st.html(brand_html)
            else:
                st.markdown(brand_html, unsafe_allow_html=True)

        # Nav Page 1: Overview
        with cols[1]:
            is_active = active_page == "overview"
            lbl = "● Overview" if is_active else "Overview"
            if st.button(lbl, key="nav_btn_overview", use_container_width=True):
                st.session_state["active_nav"] = "overview"
                st.rerun()

        # Nav Page 2: Franchise Wars
        with cols[2]:
            is_active = active_page == "teams"
            lbl = "● Franchises" if is_active else "Franchises"
            if st.button(lbl, key="nav_btn_teams", use_container_width=True):
                st.session_state["active_nav"] = "teams"
                st.rerun()

        # Nav Page 3: Player Vanguard
        with cols[3]:
            is_active = active_page == "players"
            lbl = "● Players" if is_active else "Players"
            if st.button(lbl, key="nav_btn_players", use_container_width=True):
                st.session_state["active_nav"] = "players"
                st.rerun()

        # Nav Page 4: Era Evolution
        with cols[4]:
            is_active = active_page == "seasons"
            lbl = "● Evolution" if is_active else "Evolution"
            if st.button(lbl, key="nav_btn_seasons", use_container_width=True):
                st.session_state["active_nav"] = "seasons"
                st.rerun()

        # Nav Page 5: HDFS Data Lake
        with cols[5]:
            is_active = active_page == "explorer"
            lbl = "● Data Lake" if is_active else "Data Lake"
            if st.button(lbl, key="nav_btn_explorer", use_container_width=True):
                st.session_state["active_nav"] = "explorer"
                st.rerun()

        # Status Pill Column
        with cols[6]:
            status_html = f"""<div style="background: #0B111E; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 5px 12px; font-family: 'Space Grotesk', monospace; font-size: 0.7rem; font-weight: 700; display: flex; align-items: center; justify-content: space-between; color: #CBD5E1; margin-top: 4px;">
<div style="display: flex; align-items: center;"><span class="pulse-dot"></span><span>SPARK MASTER</span></div>
<span style="color: rgba(255,255,255,0.2);">|</span>
<span style="color: {cyan}; font-weight: 800;">260,920 BALLS</span>
</div>"""
            if hasattr(st, "html"):
                st.html(status_html)
            else:
                st.markdown(status_html, unsafe_allow_html=True)

        # Primary Action / Launch Button Column
        with cols[7]:
            if active_page == "landing":
                if st.button("Launch Hub →", key="nav_launch_btn", use_container_width=True):
                    st.session_state["active_nav"] = "overview"
                    st.rerun()
            else:
                if st.button("🏠 Home", key="nav_home_btn", use_container_width=True):
                    st.session_state["active_nav"] = "landing"
                    st.rerun()

    # Subtle bottom border beneath top bar
    div_html = "<div style='height: 1px; background: rgba(255, 255, 255, 0.08); margin: 0.4rem 0 1.1rem 0;'></div>"
    if hasattr(st, "html"):
        st.html(div_html)
    else:
        st.markdown(div_html, unsafe_allow_html=True)

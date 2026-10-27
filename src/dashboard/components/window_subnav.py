"""
macOS Window Sub-Navigation Component.
Renders the interactive macOS window titlebar with red/yellow/green control dots,
styled active subtabs, and system telemetry badge matching Screenshots 2 & 5.
Clicking any subtab seamlessly navigates to the target page via Streamlit session state.
"""

import streamlit as st
from src.dashboard.config import THEME_COLORS


def render_window_subnav(active_tab: str = "overview"):
    """
    Renders an interactive macOS window titlebar with functional navigation tabs.
    
    active_tab options:
    - 'overview': Tournament Overview
    - 'teams': Team Analytics (Franchise Wars)
    - 'players': Player Deep-Dive (Player Vanguard)
    - 'seasons': Season Evolutions (Match Phases)
    """
    orange = THEME_COLORS.get("accent_orange", "#FF6B00")
    cyan = THEME_COLORS.get("accent_cyan", "#00F0FF")
    bg_card = THEME_COLORS.get("bg_card", "#0E1626")
    border_color = THEME_COLORS.get("border_color", "rgba(255, 255, 255, 0.08)")

    # Window Container styling wrapper
    st.markdown(
        f"""
        <style>
        div.window-subnav-container {{
            background: #090F1C;
            border: 1px solid {border_color};
            border-radius: 12px 12px 0 0;
            padding: 8px 16px;
            margin-bottom: 0px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Streamlit column layout for interactive tabs + status tag
    cols = st.columns([1.0, 1.2, 1.3, 1.4, 1.5, 2.6])

    # Col 0: macOS Window Control Dots
    with cols[0]:
        dots_html = """
        <div style="display: flex; align-items: center; gap: 7px; height: 38px;">
            <span style="display: inline-block; width: 11px; height: 11px; border-radius: 50%; background: #FF5F56; box-shadow: 0 0 6px rgba(255, 95, 86, 0.5);"></span>
            <span style="display: inline-block; width: 11px; height: 11px; border-radius: 50%; background: #FFBD2E; box-shadow: 0 0 6px rgba(255, 189, 46, 0.5);"></span>
            <span style="display: inline-block; width: 11px; height: 11px; border-radius: 50%; background: #27C93F; box-shadow: 0 0 6px rgba(39, 201, 63, 0.5);"></span>
        </div>
        """
        if hasattr(st, "html"):
            st.html(dots_html)
        else:
            st.markdown(dots_html, unsafe_allow_html=True)

    # Col 1: Overview
    with cols[1]:
        is_ov = active_tab == "overview"
        label = "● Overview" if is_ov else "Overview"
        if st.button(label, key="wsub_overview", use_container_width=True):
            st.session_state["active_nav"] = "overview"
            st.rerun()

    # Col 2: Team Analytics
    with cols[2]:
        is_tm = active_tab == "teams"
        label = "● Team Analytics" if is_tm else "Team Analytics"
        if st.button(label, key="wsub_teams", use_container_width=True):
            st.session_state["active_nav"] = "teams"
            st.rerun()

    # Col 3: Player Deep-Dive
    with cols[3]:
        is_pl = active_tab == "players"
        label = "● Player Deep-Dive" if is_pl else "Player Deep-Dive"
        if st.button(label, key="wsub_players", use_container_width=True):
            st.session_state["active_nav"] = "players"
            st.rerun()

    # Col 4: Season Evolutions
    with cols[4]:
        is_se = active_tab == "seasons"
        label = "● Season Evolutions" if is_se else "Season Evolutions"
        if st.button(label, key="wsub_seasons", use_container_width=True):
            st.session_state["active_nav"] = "seasons"
            st.rerun()

    # Col 5: Telemetry Status Tag
    with cols[5]:
        tag_html = f"""
        <div style="display: flex; justify-content: flex-end; align-items: center; height: 38px;">
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 700; color: #64748B; letter-spacing: 0.08em; background: rgba(255, 255, 255, 0.03); padding: 5px 12px; border-radius: 6px; border: 1px solid rgba(255, 255, 255, 0.06);">
                PRO_MODE_ENABLED // <span style="color: {orange};">v4.2.0</span>
            </span>
        </div>
        """
        if hasattr(st, "html"):
            st.html(tag_html)
        else:
            st.markdown(tag_html, unsafe_allow_html=True)

    # Bottom hairline border
    sep_html = "<div style='height: 1px; background: rgba(255, 255, 255, 0.08); margin: 4px 0 16px 0;'></div>"
    if hasattr(st, "html"):
        st.html(sep_html)
    else:
        st.markdown(sep_html, unsafe_allow_html=True)

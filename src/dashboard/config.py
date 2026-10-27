"""
Dashboard Styling & Configuration.
Defines the dark broadcast sports tech theme, stadium floodlight colors, custom CSS injection, and Plotly templates.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio

# Color Palette (Dark Broadcast Sports Tech Theme)
THEME_COLORS = {
    # Backgrounds
    "bg_main": "#070B14",           # Pitch black / deep stadium midnight
    "bg_card": "#0E1626",           # Dark navy glass card surface
    "bg_card_inner": "#131D31",     # Nested card container
    "sidebar_bg": "#0A0F1D",        # Dark navbar / sidebar base
    "sidebar_card": "#131D31",
    
    # Typography
    "text_primary": "#FFFFFF",      # Crisp white headings & values
    "text_secondary": "#8E9CAE",    # Slate metadata text
    "text_muted": "#526581",        # Muted subtle labels
    "text_light": "#FFFFFF",
    "text_sidebar_muted": "#8E9CAE",
    "text_cyan": "#00F0FF",         # Neon telemetry label text
    
    # Borders & Dividers
    "border_color": "rgba(255, 255, 255, 0.08)", # Subtle glass border
    "border_highlight": "rgba(0, 240, 255, 0.3)",
    "grid_color": "rgba(255, 255, 255, 0.05)",   # Subtle dark chart grid
    "sidebar_border": "rgba(255, 255, 255, 0.08)",
    
    # Sports & Telemetry Accents
    "accent_orange": "#FF6B00",     # IPL Power Orange
    "accent_orange_hover": "#FF8533",
    "accent_cyan": "#00F0FF",       # Neon telemetry cyan
    "accent_green": "#00E676",      # Victory green
    "accent_red": "#FF3366",        # Dismissal / loss crimson
    "accent_purple": "#8B5CF6",     # Strategy purple
    "accent_yellow": "#FACC15",     # CSK Gold
    "accent_blue": "#0284C7",       # MI Royal Blue
    
    # Backwards-compatibility aliases
    "bg_dark": "#070B14",
    "card_bg": "#0E1626",
    "card_border": "rgba(255, 255, 255, 0.08)",
}

# Franchise brand color mapping for badges & charts
TEAM_COLORS = {
    "Chennai Super Kings": "#FACC15",
    "Mumbai Indians": "#0284C7",
    "Kolkata Knight Riders": "#9333EA",
    "Royal Challengers Bangalore": "#EF4444",
    "Delhi Capitals": "#38BDF8",
    "Punjab Kings": "#F43F5E",
    "Rajasthan Royals": "#EC4899",
    "Sunrisers Hyderabad": "#F97316",
    "Gujarat Titans": "#14B8A6",
    "Lucknow Super Giants": "#06B6D4",
    "Rising Pune Supergiant": "#818CF8",
    "Gujarat Lions": "#D97706",
    "Kochi Tuskers Kerala": "#10B981",
    "Pune Warriors": "#0D9488",
    "Deccan Chargers": "#64748B",
}

TEAM_ABBRS = {
    "Chennai Super Kings": "CSK",
    "Mumbai Indians": "MI",
    "Kolkata Knight Riders": "KKR",
    "Royal Challengers Bangalore": "RCB",
    "Delhi Capitals": "DC",
    "Punjab Kings": "PBKS",
    "Rajasthan Royals": "RR",
    "Sunrisers Hyderabad": "SRH",
    "Gujarat Titans": "GT",
    "Lucknow Super Giants": "LSG",
    "Rising Pune Supergiant": "RPS",
    "Gujarat Lions": "GL",
    "Kochi Tuskers Kerala": "KTK",
    "Pune Warriors": "PW",
    "Deccan Chargers": "DCH",
}


def get_plotly_layout_defaults():
    """
    Returns Plotly layout defaults styled for dark broadcast sports telemetry.
    """
    return dict(
        font=dict(family="'Inter', -apple-system, BlinkMacSystemFont, sans-serif", color="#FFFFFF", size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0E1626",
        margin=dict(l=45, r=30, t=50, b=45),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            linecolor="rgba(255, 255, 255, 0.12)",
            zerolinecolor="rgba(255, 255, 255, 0.12)",
            tickfont=dict(color="#8E9CAE", size=11),
            title_font=dict(color="#FFFFFF", size=12, family="'Space Grotesk', sans-serif"),
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            linecolor="rgba(255, 255, 255, 0.12)",
            zerolinecolor="rgba(255, 255, 255, 0.12)",
            tickfont=dict(color="#8E9CAE", size=11),
            title_font=dict(color="#FFFFFF", size=12, family="'Space Grotesk', sans-serif"),
        ),
        legend=dict(
            bgcolor="rgba(14, 22, 38, 0.85)",
            bordercolor="rgba(255, 255, 255, 0.1)",
            borderwidth=1,
            font=dict(color="#FFFFFF", size=11),
        ),
        hoverlabel=dict(
            bgcolor="#070B14",
            bordercolor="#FF6B00",
            font=dict(color="#FFFFFF", family="'Space Grotesk', sans-serif", size=12),
        ),
    )


def apply_theme():
    """Injects custom CSS for broadcast sports tech aesthetics, glowing indicators, and glassmorphism."""
    bg_main = THEME_COLORS.get("bg_main", "#070B14")
    bg_card = THEME_COLORS.get("bg_card", "#0E1626")
    bg_card_inner = THEME_COLORS.get("bg_card_inner", "#131D31")
    accent_orange = THEME_COLORS.get("accent_orange", "#FF6B00")
    accent_cyan = THEME_COLORS.get("accent_cyan", "#00F0FF")
    accent_green = THEME_COLORS.get("accent_green", "#00E676")
    accent_red = THEME_COLORS.get("accent_red", "#FF3366")
    accent_purple = THEME_COLORS.get("accent_purple", "#8B5CF6")
    accent_yellow = THEME_COLORS.get("accent_yellow", "#FACC15")
    accent_blue = THEME_COLORS.get("accent_blue", "#0284C7")
    text_secondary = THEME_COLORS.get("text_secondary", "#8E9CAE")
    border_color = THEME_COLORS.get("border_color", "rgba(255, 255, 255, 0.08)")

    css = f"""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800;900&family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap');

    /* Global Root Variables */
    :root {{
        --bg-main: {bg_main};
        --bg-card: {bg_card};
        --bg-card-inner: {bg_card_inner};
        --accent-orange: {accent_orange};
        --accent-cyan: {accent_cyan};
        --accent-green: {accent_green};
        --accent-red: {accent_red};
    }}

    /* Main Application Container */
    .stApp {{
        background: #070B14 radial-gradient(circle at 50% 0%, rgba(255, 107, 0, 0.07) 0%, rgba(0, 240, 255, 0.03) 35%, transparent 70%) no-repeat !important;
        background-color: #070B14 !important;
        color: #FFFFFF !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}

    /* Hide standard sidebar and default streamlit headers */
    [data-testid="stSidebar"] {{
        display: none !important;
    }}
    header[data-testid="stHeader"] {{
        background: transparent !important;
        height: 0px !important;
        visibility: hidden !important;
    }}
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 1380px !important;
    }}

    /* Typography */
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Outfit', sans-serif !important;
        color: #FFFFFF !important;
        font-weight: 800;
        letter-spacing: -0.02em;
    }}

    h1 {{
        font-size: 2.3rem !important;
        margin-top: 0.1rem !important;
        margin-bottom: 0.35rem !important;
    }}

    h2 {{
        font-size: 1.45rem !important;
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
    }}

    p, span, div {{
        color: #FFFFFF;
    }}

    /* Neon Telemetry Subtitle */
    .telemetry-subtitle {{
        font-family: 'Space Grotesk', monospace;
        color: {accent_cyan} !important;
        font-size: 0.74rem;
        letter-spacing: 0.18em;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
        display: inline-block;
    }}

    /* Section Subtitle description */
    .section-desc {{
        color: {text_secondary};
        font-size: 0.92rem;
        margin-bottom: 1.25rem;
        line-height: 1.5;
    }}

    /* Pulse Radar Indicator */
    @keyframes pulse-radar {{
        0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 230, 118, 0.7); }}
        70% {{ transform: scale(1); box-shadow: 0 0 0 6px rgba(0, 230, 118, 0); }}
        100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 230, 118, 0); }}
    }}

    .pulse-dot {{
        width: 8px;
        height: 8px;
        background-color: {accent_green};
        border-radius: 50%;
        display: inline-block;
        animation: pulse-radar 2s infinite;
        margin-right: 6px;
    }}

    /* Top Navigation Button Overrides */
    div.stButton > button {{
        background: rgba(14, 22, 38, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        color: #CBD5E1 !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        border-radius: 8px !important;
        padding: 6px 12px !important;
        white-space: nowrap !important;
        transition: all 0.2s ease !important;
    }}

    div.stButton > button:hover {{
        background: rgba(255, 255, 255, 0.12) !important;
        color: #FFFFFF !important;
        border-color: rgba(255, 107, 0, 0.5) !important;
        transform: translateY(-1px) !important;
    }}

    /* Force dark background on any pre/code blocks to prevent white cards */
    pre, code, div[data-testid="stCodeBlock"] {{
        background: #0B111E !important;
        color: #00F0FF !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 8px !important;
    }}

    /* KPI Metric Cards */
    .metric-card {{
        background-color: {bg_card};
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        position: relative;
    }}

    .metric-card:hover {{
        border-color: rgba(0, 240, 255, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.5);
    }}

    .metric-title {{
        color: {text_secondary};
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.35rem;
    }}

    .metric-value {{
        color: #FFFFFF;
        font-family: 'Outfit', sans-serif;
        font-size: 2.1rem;
        font-weight: 900;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }}

    .metric-value.orange {{ color: {accent_orange}; }}
    .metric-value.cyan {{ color: {accent_cyan}; }}
    .metric-value.green {{ color: {accent_green}; }}
    .metric-value.purple {{ color: {accent_purple}; }}

    .metric-delta-row {{
        display: flex;
        align-items: center;
        gap: 6px;
        margin-top: 0.45rem;
    }}

    .metric-delta {{
        font-family: 'Space Grotesk', monospace;
        font-size: 0.74rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        gap: 3px;
    }}

    .metric-delta.up {{
        background: rgba(0, 230, 118, 0.12);
        color: {accent_green};
        border: 1px solid rgba(0, 230, 118, 0.25);
    }}

    .metric-delta.down {{
        background: rgba(255, 51, 102, 0.12);
        color: {accent_red};
        border: 1px solid rgba(255, 51, 102, 0.25);
    }}

    .metric-subtitle {{
        color: {text_secondary};
        font-size: 0.78rem;
    }}

    /* Mac OS Window Card Header */
    .window-card {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 14px;
        overflow: hidden;
        margin-bottom: 1.5rem;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
    }}

    .window-header {{
        background: #0B111E;
        border-bottom: 1px solid {border_color};
        padding: 10px 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}

    .window-dots {{
        display: flex;
        align-items: center;
        gap: 7px;
    }}

    .dot {{
        width: 10px;
        height: 10px;
        border-radius: 50%;
    }}

    .dot-red {{ background-color: #FF5F56; }}
    .dot-yellow {{ background-color: #FFBD2E; }}
    .dot-green {{ background-color: #27C93F; }}

    .window-tabs {{
        display: flex;
        align-items: center;
        gap: 20px;
        margin-left: 20px;
    }}

    .window-tab {{
        font-family: 'Outfit', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        color: {text_secondary};
        padding-bottom: 4px;
    }}

    .window-tab.active {{
        color: #FFFFFF;
        border-bottom: 2px solid {accent_orange};
    }}

    .window-tag {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: {text_secondary};
        letter-spacing: 0.05em;
    }}

    /* Selectboxes and Dropdowns Dark Styling */
    .stSelectbox label, .stSlider label, .stTextInput label {{
        color: #94A3B8 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.76rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
    }}

    div[data-baseweb="select"] > div {{
        background-color: #0E1626 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
    }}

    div[data-baseweb="select"] * {{
        color: #FFFFFF !important;
    }}

    /* BaseWeb Dropdown Popover & Menu Items (Fixes White Box Issue) */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    ul[data-baseweb="menu"],
    ul[role="listbox"] {{
        background-color: #0E1626 !important;
        background: #0E1626 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.75) !important;
    }}

    li[role="option"],
    li[data-baseweb="menu-item"],
    div[role="option"] {{
        background-color: #0E1626 !important;
        background: #0E1626 !important;
        color: #FFFFFF !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
        font-size: 0.88rem !important;
        padding: 9px 14px !important;
        transition: background 0.15s ease, color 0.15s ease !important;
    }}

    li[role="option"] *,
    li[data-baseweb="menu-item"] *,
    div[role="option"] * {{
        color: #FFFFFF !important;
    }}

    li[role="option"]:hover,
    li[data-baseweb="menu-item"]:hover,
    div[role="option"]:hover {{
        background-color: #1A2744 !important;
        background: #1A2744 !important;
        color: {accent_orange} !important;
    }}

    li[role="option"]:hover *,
    li[data-baseweb="menu-item"]:hover *,
    div[role="option"]:hover * {{
        color: {accent_orange} !important;
    }}

    li[role="option"][aria-selected="true"],
    li[data-baseweb="menu-item"][aria-selected="true"],
    div[role="option"][aria-selected="true"] {{
        background-color: rgba(255, 107, 0, 0.18) !important;
        background: rgba(255, 107, 0, 0.18) !important;
        color: {accent_orange} !important;
        font-weight: 700 !important;
    }}

    li[role="option"][aria-selected="true"] *,
    li[data-baseweb="menu-item"][aria-selected="true"] *,
    div[role="option"][aria-selected="true"] * {{
        color: {accent_orange} !important;
    }}

    div[data-baseweb="input"] input {{
        background-color: #0E1626 !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
    }}

    /* Plotly Containers */
    [data-testid="stPlotlyChart"] {{
        background-color: {bg_card};
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: 12px 10px 4px 10px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
        margin-bottom: 1rem;
    }}

    /* DataFrames in Dark Mode */
    .stDataFrame {{
        background-color: {bg_card} !important;
        border: 1px solid {border_color} !important;
        border-radius: 10px !important;
    }}

    /* Section Divider */
    hr {{
        border-color: rgba(255, 255, 255, 0.08) !important;
        margin: 1.5rem 0 !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

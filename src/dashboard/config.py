"""
Dashboard Styling & Configuration.
Defines the bright high-contrast sports analytics theme, colors, CSS injection, and Plotly templates.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio

# Color Palette (High-Contrast IPL Sports Theme)
THEME_COLORS = {
    # Backgrounds
    "bg_main": "#F5F7FB",           # Light grey main dashboard canvas
    "bg_card": "#FFFFFF",           # Pure white container/card
    "sidebar_bg": "#102A50",        # Deep navy sidebar
    "sidebar_card": "#163766",      # Sidebar card container
    
    # Typography
    "text_primary": "#172B4D",      # Dark navy primary text (high contrast)
    "text_secondary": "#526581",    # Slate blue-grey secondary text
    "text_light": "#FFFFFF",        # Crisp white text
    "text_sidebar_muted": "#A0B3D6",# Muted light blue for dark sidebar
    
    # Borders & Dividers
    "border_color": "#DCE4EF",      # Crisp light border
    "grid_color": "#E8EEF5",        # Subtle chart gridline
    "sidebar_border": "#24477D",    # Border inside dark sidebar
    
    # Accents
    "accent_orange": "#FF6B00",     # IPL brand orange
    "accent_blue": "#168BEB",       # Primary sports blue
    "accent_green": "#16A765",      # Positive performance green
    "accent_purple": "#7747C8",     # Analytical purple
    "accent_red": "#DC3545",        # Warning / loss red
    
    # Backwards-compatibility aliases
    "bg_dark": "#F5F7FB",
    "card_bg": "#FFFFFF",
    "card_border": "#DCE4EF",
    "text_muted": "#526581",
}


def get_plotly_layout_defaults():
    """
    Returns Plotly layout defaults styled for high-contrast light theme dashboards.
    """
    return dict(
        font=dict(family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif", color=THEME_COLORS["text_primary"], size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        margin=dict(l=45, r=30, t=55, b=45),
        xaxis=dict(
            gridcolor=THEME_COLORS["grid_color"],
            linecolor=THEME_COLORS["border_color"],
            zerolinecolor=THEME_COLORS["border_color"],
            tickfont=dict(color=THEME_COLORS["text_secondary"], size=11),
            title_font=dict(color=THEME_COLORS["text_primary"], size=12, family="Inter, sans-serif"),
        ),
        yaxis=dict(
            gridcolor=THEME_COLORS["grid_color"],
            linecolor=THEME_COLORS["border_color"],
            zerolinecolor=THEME_COLORS["border_color"],
            tickfont=dict(color=THEME_COLORS["text_secondary"], size=11),
            title_font=dict(color=THEME_COLORS["text_primary"], size=12, family="Inter, sans-serif"),
        ),
        legend=dict(
            bgcolor="rgba(255, 255, 255, 0.95)",
            bordercolor=THEME_COLORS["border_color"],
            borderwidth=1,
            font=dict(color=THEME_COLORS["text_primary"], size=11),
        ),
        hoverlabel=dict(
            bgcolor=THEME_COLORS["sidebar_bg"],
            bordercolor=THEME_COLORS["accent_orange"],
            font=dict(color="#FFFFFF", family="Inter, sans-serif", size=12),
        ),
    )


def apply_theme():
    """Injects comprehensive custom CSS for high contrast, clean typography, and polished layout."""
    css = f"""
    <style>
    /* Google Font Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Main application background and default text */
    .stApp {{
        background-color: {THEME_COLORS['bg_main']};
        color: {THEME_COLORS['text_primary']};
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    /* Global Headings */
    h1, h2, h3, h4, h5, h6 {{
        color: {THEME_COLORS['text_primary']} !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 700;
        letter-spacing: -0.015em;
    }}
    
    h1 {{
        font-size: 1.85rem !important;
        margin-top: 0.2rem !important;
        margin-bottom: 0.4rem !important;
        font-weight: 800 !important;
    }}
    
    h2 {{
        font-size: 1.35rem !important;
        margin-top: 1.4rem !important;
        margin-bottom: 0.75rem !important;
    }}
    
    h3 {{
        font-size: 1.15rem !important;
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
    }}

    p, span, div {{
        color: {THEME_COLORS['text_primary']};
    }}

    .stCaption, small {{
        color: {THEME_COLORS['text_secondary']} !important;
        font-size: 0.85rem;
    }}

    /* Section Header Decorator */
    .section-title {{
        display: flex;
        align-items: center;
        gap: 8px;
        border-left: 4px solid {THEME_COLORS['accent_orange']};
        padding-left: 10px;
        margin-top: 1.5rem;
        margin-bottom: 0.85rem;
        color: {THEME_COLORS['text_primary']};
        font-size: 1.25rem;
        font-weight: 700;
    }}

    /* Metric Card Styling */
    .metric-card {{
        background-color: {THEME_COLORS['bg_card']};
        border: 1px solid {THEME_COLORS['border_color']};
        border-radius: 10px;
        padding: 1.1rem 1.3rem;
        box-shadow: 0 2px 8px rgba(23, 43, 77, 0.05);
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        position: relative;
    }}
    
    .metric-card:hover {{
        border-color: #B4CCE8;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(23, 43, 77, 0.09);
    }}

    /* Color-coded accent tops for KPI cards */
    .metric-card.accent-orange {{ border-top: 3.5px solid {THEME_COLORS['accent_orange']}; }}
    .metric-card.accent-blue {{ border-top: 3.5px solid {THEME_COLORS['accent_blue']}; }}
    .metric-card.accent-green {{ border-top: 3.5px solid {THEME_COLORS['accent_green']}; }}
    .metric-card.accent-purple {{ border-top: 3.5px solid {THEME_COLORS['accent_purple']}; }}
    .metric-card.accent-red {{ border-top: 3.5px solid {THEME_COLORS['accent_red']}; }}

    .metric-title {{
        color: {THEME_COLORS['text_secondary']};
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.35rem;
    }}
    
    .metric-value {{
        color: {THEME_COLORS['text_primary']};
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.15;
    }}
    
    .metric-value.accent, .metric-value.orange {{ color: {THEME_COLORS['accent_orange']}; }}
    .metric-value.blue {{ color: {THEME_COLORS['accent_blue']}; }}
    .metric-value.green {{ color: {THEME_COLORS['accent_green']}; }}
    .metric-value.purple {{ color: {THEME_COLORS['accent_purple']}; }}
    .metric-value.red {{ color: {THEME_COLORS['accent_red']}; }}
    
    .metric-subtitle {{
        color: {THEME_COLORS['text_secondary']};
        font-size: 0.82rem;
        margin-top: 0.4rem;
        font-weight: 500;
    }}

    /* Sidebar Customization - High-Contrast Dark Navy */
    [data-testid="stSidebar"] {{
        background-color: {THEME_COLORS['sidebar_bg']} !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }}
    
    [data-testid="stSidebar"] * {{
        color: #E2E8F0;
    }}

    [data-testid="stSidebarNav"] a {{
        background-color: transparent !important;
        color: #D3DFEE !important;
        border-radius: 7px !important;
        margin: 2px 8px !important;
        padding: 8px 12px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }}
    
    [data-testid="stSidebarNav"] a:hover {{
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: #FFFFFF !important;
    }}

    [data-testid="stSidebarNav"] a[aria-current="page"] {{
        background-color: rgba(255, 107, 0, 0.16) !important;
        color: {THEME_COLORS['accent_orange']} !important;
        font-weight: 700 !important;
        border-left: 4px solid {THEME_COLORS['accent_orange']} !important;
    }}

    [data-testid="stSidebarNav"] a[aria-current="page"] span {{
        color: {THEME_COLORS['accent_orange']} !important;
    }}

    /* Info Banners */
    .info-banner {{
        background: #EDF4FD;
        border-left: 4px solid {THEME_COLORS['accent_blue']};
        border-top: 1px solid {THEME_COLORS['border_color']};
        border-right: 1px solid {THEME_COLORS['border_color']};
        border-bottom: 1px solid {THEME_COLORS['border_color']};
        padding: 0.85rem 1.15rem;
        border-radius: 6px;
        margin-bottom: 1.25rem;
        color: {THEME_COLORS['text_primary']};
        font-size: 0.88rem;
        line-height: 1.5;
    }}

    .info-banner b, .info-banner strong {{
        color: #0E2242;
    }}

    .info-banner code {{
        background-color: #D8E6F8;
        color: #0E2242;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.82rem;
        font-weight: 600;
    }}

    /* Selectboxes, Text Inputs, and Dropdowns */
    .stSelectbox label, .stSlider label, .stTextInput label {{
        color: {THEME_COLORS['text_primary']} !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }}

    div[data-baseweb="select"] > div {{
        background-color: #FFFFFF !important;
        border-color: {THEME_COLORS['border_color']} !important;
        color: {THEME_COLORS['text_primary']} !important;
        border-radius: 6px !important;
    }}
    
    div[data-baseweb="select"] * {{
        color: {THEME_COLORS['text_primary']} !important;
    }}

    div[data-baseweb="input"] input {{
        background-color: #FFFFFF !important;
        color: {THEME_COLORS['text_primary']} !important;
        border: 1px solid {THEME_COLORS['border_color']} !important;
        border-radius: 6px !important;
    }}

    /* Buttons & Download Action */
    .stDownloadButton button {{
        background-color: {THEME_COLORS['accent_orange']} !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.25rem !important;
        box-shadow: 0 2px 8px rgba(255, 107, 0, 0.28) !important;
        transition: all 0.2s ease !important;
    }}
    
    .stDownloadButton button:hover {{
        background-color: #E65A00 !important;
        box-shadow: 0 4px 12px rgba(255, 107, 0, 0.4) !important;
        transform: translateY(-1px) !important;
    }}

    /* Tables & DataFrames */
    .stDataFrame {{
        border: 1px solid {THEME_COLORS['border_color']} !important;
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
    }}

    /* Plotly Chart Containers */
    [data-testid="stPlotlyChart"] {{
        background-color: #FFFFFF;
        border: 1px solid {THEME_COLORS['border_color']};
        border-radius: 10px;
        padding: 10px 10px 4px 10px;
        box-shadow: 0 2px 8px rgba(23, 43, 77, 0.04);
        margin-bottom: 1rem;
    }}

    /* Dividers */
    hr {{
        border-color: {THEME_COLORS['border_color']} !important;
        margin: 1.4rem 0 !important;
        opacity: 0.8;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

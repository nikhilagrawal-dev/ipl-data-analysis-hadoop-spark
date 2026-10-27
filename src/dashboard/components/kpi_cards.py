"""
Reusable KPI Cards Component.
Renders styled, responsive HTML metric cards for dark sports broadcast analytics.
Supports delta pills (e.g. '▲ +10 Matches in 2024') exactly matching user reference designs.
Uses st.html / textwrap to eliminate any markdown code block formatting artifacts.
"""

import streamlit as st
import textwrap
from typing import Union, Optional


def render_kpi_card(
    title: str,
    value: Union[str, int, float],
    subtitle: str = "",
    accent: Union[bool, str] = False,
    help_text: str = "",
    delta: Optional[str] = None,
    delta_type: str = "up",
):
    """
    Renders a dark broadcast-grade metric card with optional delta pills and glow accents.
    """
    accent_name = ""
    if isinstance(accent, str) and accent:
        accent_name = accent.lower()
    elif accent is True:
        accent_name = "orange"

    card_accent_class = f"accent-{accent_name}" if accent_name else ""
    value_accent_class = accent_name if accent_name else ""
    help_attr = f'title="{help_text}"' if help_text else ""

    delta_html = ""
    if delta:
        arrow = "▲" if delta_type == "up" else "▼"
        delta_class = "up" if delta_type == "up" else "down"
        delta_html = f'<div class="metric-delta-row"><span class="metric-delta {delta_class}">{arrow} {delta}</span></div>'
    elif subtitle:
        delta_html = f'<div class="metric-subtitle" style="margin-top: 6px;">{subtitle}</div>'

    html = f"""<div class="metric-card {card_accent_class}" {help_attr}>
<div class="metric-title">{title}</div>
<div class="metric-value {value_accent_class}">{value}</div>
{delta_html}
</div>"""

    clean_html = textwrap.dedent(html).strip()
    if hasattr(st, "html"):
        st.html(clean_html)
    else:
        st.markdown(clean_html, unsafe_allow_html=True)

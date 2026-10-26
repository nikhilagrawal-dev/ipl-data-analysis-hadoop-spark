"""
Reusable KPI Cards Component.
Renders styled, responsive HTML metric cards for high-contrast sports analytics.
"""

import streamlit as st
from typing import Union


def render_kpi_card(
    title: str,
    value: Union[str, int, float],
    subtitle: str = "",
    accent: Union[bool, str] = False,
    help_text: str = "",
):
    """
    Renders a clean, high-contrast metric card in Streamlit with accent indicators.

    Args:
        title: Metric name / category
        value: Formatted display value (e.g. '1,095' or '55.17%')
        subtitle: Secondary insight or context
        accent: True (orange), or color name ('orange', 'blue', 'green', 'purple', 'red')
        help_text: Optional tooltip text
    """
    accent_name = ""
    if isinstance(accent, str) and accent:
        accent_name = accent.lower()
    elif accent is True:
        accent_name = "orange"

    card_accent_class = f"accent-{accent_name}" if accent_name else ""
    value_accent_class = f"accent {accent_name}" if accent_name else ""
    help_attr = f'title="{help_text}"' if help_text else ""

    html = f"""
    <div class="metric-card {card_accent_class}" {help_attr}>
        <div class="metric-title">{title}</div>
        <div class="metric-value {value_accent_class}">{value}</div>
        {f'<div class="metric-subtitle">{subtitle}</div>' if subtitle else ''}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

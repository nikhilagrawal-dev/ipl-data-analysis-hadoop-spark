"""
Plotly Chart Helpers Module.
Provides consistent, high-contrast, dark-themed interactive charts for IPL sports telemetry.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from src.dashboard.config import THEME_COLORS, get_plotly_layout_defaults


def create_horizontal_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    x_label: str = "",
    y_label: str = "",
    color_col: str = None,
    hover_template: str = None,
    color_hex: str = THEME_COLORS["accent_orange"],
) -> go.Figure:
    """
    Creates a clean, high-contrast horizontal bar chart (ideal for rankings and leaderboards).
    """
    df_sorted = df.sort_values(by=x_col, ascending=True)

    fig = go.Figure(
        go.Bar(
            x=df_sorted[x_col],
            y=df_sorted[y_col],
            orientation="h",
            marker=dict(
                color=color_hex,
                line=dict(color="rgba(255, 255, 255, 0.15)", width=1),
            ),
            hovertemplate=hover_template or f"<b>%{{y}}</b><br>{x_col}: %{{x:,}}<extra></extra>",
        )
    )

    layout = get_plotly_layout_defaults()
    layout.update(
        title=dict(text=title, font=dict(size=14, color="#FFFFFF", family="'Outfit', sans-serif")),
        xaxis=dict(**layout["xaxis"], title=x_label or x_col),
        yaxis=dict(**layout["yaxis"], title=y_label or y_col),
    )
    fig.update_layout(layout)
    return fig


def create_vertical_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    x_label: str = "",
    y_label: str = "",
    color_hex: str = THEME_COLORS["accent_blue"],
    highlight_val = None,
    highlight_color: str = THEME_COLORS["accent_orange"],
    hover_template: str = None,
) -> go.Figure:
    """
    Creates a clean vertical bar chart with optional highlight bar (e.g. peak season).
    """
    colors = []
    for val in df[x_col]:
        if highlight_val is not None and str(val) == str(highlight_val):
            colors.append(highlight_color)
        else:
            colors.append(color_hex)

    fig = go.Figure(
        go.Bar(
            x=df[x_col],
            y=df[y_col],
            marker=dict(
                color=colors,
                line=dict(color="rgba(255, 255, 255, 0.15)", width=1),
            ),
            hovertemplate=hover_template or f"<b>%{{x}}</b><br>{y_col}: %{{y:,}}<extra></extra>",
        )
    )

    layout = get_plotly_layout_defaults()
    layout.update(
        title=dict(text=title, font=dict(size=14, color="#FFFFFF", family="'Outfit', sans-serif")),
        xaxis=dict(**layout["xaxis"], title=x_label or x_col),
        yaxis=dict(**layout["yaxis"], title=y_label or y_col),
    )
    fig.update_layout(layout)
    return fig


def create_line_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    x_label: str = "",
    y_label: str = "",
    line_color: str = THEME_COLORS["accent_orange"],
    markers: bool = True,
) -> go.Figure:
    """
    Creates a dark sports line chart for season trends.
    """
    fig = go.Figure(
        go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode="lines+markers" if markers else "lines",
            line=dict(color=line_color, width=3),
            marker=dict(size=7, color=THEME_COLORS["accent_cyan"], line=dict(color="#FFFFFF", width=1.5)),
            hovertemplate=f"<b>%{{x}}</b><br>{y_label or y_col}: %{{y}}<extra></extra>",
        )
    )

    layout = get_plotly_layout_defaults()
    layout.update(
        title=dict(text=title, font=dict(size=14, color="#FFFFFF", family="'Outfit', sans-serif")),
        xaxis=dict(**layout["xaxis"], title=x_label or x_col),
        yaxis=dict(**layout["yaxis"], title=y_label or y_col),
    )
    fig.update_layout(layout)
    return fig


def create_grouped_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_cols: list,
    col_names: list,
    title: str,
    x_label: str = "",
    y_label: str = "",
    colors: list = None,
) -> go.Figure:
    """
    Creates a grouped bar chart comparing multiple series in dark broadcast mode.
    """
    if colors is None:
        colors = [THEME_COLORS["accent_cyan"], THEME_COLORS["accent_blue"], THEME_COLORS["accent_orange"], THEME_COLORS["accent_green"]]

    fig = go.Figure()
    for idx, (col_key, label) in enumerate(zip(y_cols, col_names)):
        fig.add_trace(
            go.Bar(
                name=label,
                x=df[x_col],
                y=df[col_key],
                marker_color=colors[idx % len(colors)],
                marker_line=dict(color="rgba(255, 255, 255, 0.1)", width=1),
            )
        )

    layout = get_plotly_layout_defaults()
    layout.update(
        title=dict(text=title, font=dict(size=14, color="#FFFFFF", family="'Outfit', sans-serif")),
        barmode="group",
        xaxis=dict(**layout["xaxis"], title=x_label or x_col),
        yaxis=dict(**layout["yaxis"], title=y_label or y_label),
    )
    fig.update_layout(layout)
    return fig


def create_donut_chart(
    labels: list,
    values: list,
    title: str,
    colors: list = None,
) -> go.Figure:
    """
    Creates a clean donut chart for proportional breakdowns.
    """
    if colors is None:
        colors = [THEME_COLORS["accent_cyan"], THEME_COLORS["accent_orange"], THEME_COLORS["accent_green"], THEME_COLORS["accent_purple"]]

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.6,
            marker=dict(colors=colors, line=dict(color="#070B14", width=3)),
            textinfo="percent+label",
            textposition="outside",
            hoverinfo="label+value+percent",
            textfont=dict(color="#FFFFFF", family="'Space Grotesk', sans-serif"),
        )
    )

    layout = get_plotly_layout_defaults()
    layout.update(
        title=dict(text=title, font=dict(size=14, color="#FFFFFF", family="'Outfit', sans-serif")),
        showlegend=False,
    )
    fig.update_layout(layout)
    return fig


def create_scatter_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    text_col: str,
    title: str,
    x_label: str = "",
    y_label: str = "",
    color_col: str = None,
    hover_template: str = None,
    quadrants: bool = False,
    marker_colors: list = None,
    quadrant_labels: tuple = None,
) -> go.Figure:
    """
    Creates an interactive scatter plot for player comparisons (e.g. SR vs Avg, Economy vs Wickets).
    Supports customizable marker colors per point and dynamic quadrant labels.
    """
    colors = marker_colors if marker_colors is not None else THEME_COLORS["accent_orange"]

    fig = go.Figure(
        go.Scatter(
            x=df[x_col],
            y=df[y_col],
            text=df[text_col],
            mode="markers+text" if len(df) <= 12 else "markers",
            textposition="top center",
            textfont=dict(color="#CBD5E1", size=10, family="'Inter', sans-serif"),
            marker=dict(
                size=13,
                color=colors,
                line=dict(color="#FFFFFF", width=1.5),
                opacity=0.92,
            ),
            hovertemplate=hover_template or f"<b>%{{text}}</b><br>{x_label or x_col}: %{{x}}<br>{y_label or y_col}: %{{y}}<extra></extra>",
        )
    )

    layout = get_plotly_layout_defaults()
    layout.update(
        title=dict(text=title, font=dict(size=14, color="#FFFFFF", family="'Outfit', sans-serif")),
        xaxis=dict(**layout["xaxis"], title=x_label or x_col),
        yaxis=dict(**layout["yaxis"], title=y_label or y_col),
    )

    # Optional quadrant labels for Player Vanguard
    if quadrants and not df.empty:
        x_mid = float(df[x_col].median())
        y_mid = float(df[y_col].median())
        x_min, x_max = float(df[x_col].min()), float(df[x_col].max())
        y_min, y_max = float(df[y_col].min()), float(df[y_col].max())

        # Add quadrant lines
        fig.add_shape(type="line", x0=x_mid, y0=y_min, x1=x_mid, y1=y_max,
                      line=dict(color="rgba(255,255,255,0.18)", dash="dash", width=1.2))
        fig.add_shape(type="line", x0=x_min, y0=y_mid, x1=x_max, y1=y_mid,
                      line=dict(color="rgba(255,255,255,0.18)", dash="dash", width=1.2))

        # Quadrant annotations
        top_right, bot_right, top_left, bot_left = quadrant_labels or (
            "ELITE FINISHER", "AGGRESSIVE OPENER", "ANCHOR", "ROLE PLAYER"
        )

        fig.add_annotation(x=x_max * 0.96, y=y_max * 0.98, text=top_right,
                           showarrow=False, font=dict(color=THEME_COLORS["accent_green"], size=10, family="'Space Grotesk', monospace"))
        fig.add_annotation(x=x_max * 0.96, y=y_min * 1.04, text=bot_right,
                           showarrow=False, font=dict(color=THEME_COLORS["accent_cyan"], size=10, family="'Space Grotesk', monospace"))
        fig.add_annotation(x=x_min * 1.04, y=y_max * 0.98, text=top_left,
                           showarrow=False, font=dict(color="#94A3B8", size=10, family="'Space Grotesk', monospace"))
        fig.add_annotation(x=x_min * 1.04, y=y_min * 1.04, text=bot_left,
                           showarrow=False, font=dict(color="#64748B", size=10, family="'Space Grotesk', monospace"))

    fig.update_layout(layout)
    return fig

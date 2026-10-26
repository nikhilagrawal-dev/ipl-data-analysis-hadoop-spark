"""
Plotly Chart Helpers Module.
Provides consistent, high-contrast, themed interactive charts for IPL analytics.
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
                line=dict(color="rgba(23, 43, 77, 0.08)", width=1),
            ),
            hovertemplate=hover_template or f"<b>%{{y}}</b><br>{x_col}: %{{x:,}}<extra></extra>",
        )
    )

    layout = get_plotly_layout_defaults()
    layout.update(
        title=dict(text=title, font=dict(size=15, color=THEME_COLORS["text_primary"], family="Inter, sans-serif")),
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
    hover_template: str = None,
) -> go.Figure:
    """
    Creates a clean, high-contrast vertical bar chart.
    """
    fig = go.Figure(
        go.Bar(
            x=df[x_col],
            y=df[y_col],
            marker=dict(
                color=color_hex,
                line=dict(color="rgba(23, 43, 77, 0.08)", width=1),
            ),
            hovertemplate=hover_template or f"<b>%{{x}}</b><br>{y_col}: %{{y:,}}<extra></extra>",
        )
    )

    layout = get_plotly_layout_defaults()
    layout.update(
        title=dict(text=title, font=dict(size=15, color=THEME_COLORS["text_primary"], family="Inter, sans-serif")),
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
    Creates a high-contrast line chart for season trends.
    """
    fig = go.Figure(
        go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode="lines+markers" if markers else "lines",
            line=dict(color=line_color, width=3),
            marker=dict(size=7, color=THEME_COLORS["accent_blue"], line=dict(color="#FFFFFF", width=1.5)),
            hovertemplate=f"<b>%{{x}}</b><br>{y_label or y_col}: %{{y}}<extra></extra>",
        )
    )

    layout = get_plotly_layout_defaults()
    layout.update(
        title=dict(text=title, font=dict(size=15, color=THEME_COLORS["text_primary"], family="Inter, sans-serif")),
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
    Creates a high-contrast grouped bar chart comparing multiple series.
    """
    if colors is None:
        colors = [THEME_COLORS["accent_blue"], THEME_COLORS["accent_orange"], THEME_COLORS["accent_purple"], THEME_COLORS["accent_green"]]

    fig = go.Figure()
    for idx, (col_key, label) in enumerate(zip(y_cols, col_names)):
        fig.add_trace(
            go.Bar(
                name=label,
                x=df[x_col],
                y=df[col_key],
                marker_color=colors[idx % len(colors)],
                marker_line=dict(color="rgba(23, 43, 77, 0.08)", width=1),
            )
        )

    layout = get_plotly_layout_defaults()
    layout.update(
        title=dict(text=title, font=dict(size=15, color=THEME_COLORS["text_primary"], family="Inter, sans-serif")),
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
    Creates a clean, high-contrast donut chart for proportional breakdowns.
    """
    if colors is None:
        colors = [THEME_COLORS["accent_orange"], THEME_COLORS["accent_blue"], THEME_COLORS["accent_green"], THEME_COLORS["accent_purple"]]

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.55,
            marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
            textinfo="percent+label",
            textposition="outside",
            hoverinfo="label+value+percent",
        )
    )

    layout = get_plotly_layout_defaults()
    layout.update(
        title=dict(text=title, font=dict(size=15, color=THEME_COLORS["text_primary"], family="Inter, sans-serif")),
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
) -> go.Figure:
    """
    Creates an interactive scatter plot for player comparisons (e.g. SR vs Avg, Economy vs Wickets).
    """
    fig = go.Figure(
        go.Scatter(
            x=df[x_col],
            y=df[y_col],
            text=df[text_col],
            mode="markers+text" if len(df) <= 15 else "markers",
            textposition="top center",
            textfont=dict(color=THEME_COLORS["text_secondary"], size=10, family="Inter, sans-serif"),
            marker=dict(
                size=11,
                color=THEME_COLORS["accent_orange"],
                line=dict(color="#FFFFFF", width=1.5),
                opacity=0.95,
            ),
            hovertemplate=hover_template or f"<b>%{{text}}</b><br>{x_label or x_col}: %{{x}}<br>{y_label or y_col}: %{{y}}<extra></extra>",
        )
    )

    layout = get_plotly_layout_defaults()
    layout.update(
        title=dict(text=title, font=dict(size=15, color=THEME_COLORS["text_primary"], family="Inter, sans-serif")),
        xaxis=dict(**layout["xaxis"], title=x_label or x_col),
        yaxis=dict(**layout["yaxis"], title=y_label or y_col),
    )
    fig.update_layout(layout)
    return fig

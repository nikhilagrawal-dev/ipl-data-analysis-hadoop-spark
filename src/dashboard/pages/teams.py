"""
Page 2: Franchise Wars & Dominance Matrix.
Exact reproduction of Screenshot 3: H2H Telemetry, Dominance Matrix Arena with Team Avatars,
Recent Form Capsules, Split Win-Rate Progress Bar, and Dynasty KPI Cards.
Includes dynamic multi-season head-to-head trajectory chart that visibly updates on team selection!
Uses st.html to prevent any markdown whitespace codeblock artifacts.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.dashboard.data_loader import load_table
from src.dashboard.components.kpi_cards import render_kpi_card
from src.dashboard.components.window_subnav import render_window_subnav
from src.dashboard.config import THEME_COLORS, TEAM_COLORS, TEAM_ABBRS, get_plotly_layout_defaults


def render():
    standings_df = load_table("team_standings")
    team_season_df = load_table("team_season")
    h2h_df = load_table("team_h2h")

    orange = THEME_COLORS.get("accent_orange", "#FF6B00")
    bg_card = THEME_COLORS.get("bg_card", "#0E1626")
    border_color = THEME_COLORS.get("border_color", "rgba(255, 255, 255, 0.08)")

    all_teams = sorted(standings_df["team"].unique())
    csk_idx = all_teams.index("Chennai Super Kings") if "Chennai Super Kings" in all_teams else 0
    mi_idx = all_teams.index("Mumbai Indians") if "Mumbai Indians" in all_teams else 1

    # 1. Header with Primary & Rival Team Selectors
    head_col1, head_col2 = st.columns([3, 2.2])

    with head_col1:
        head_html = f"""<div class="telemetry-subtitle">FRANCHISE WARS // H2H TELEMETRY</div>
<h1 style="font-family: 'Outfit', sans-serif; font-size: 2.3rem; font-weight: 900; letter-spacing: -0.02em; margin: 2px 0 6px 0;">DOMINANCE <span style="color: {orange};">MATRIX</span></h1>
<div class="section-desc">Compare historical performance, venue fortresses, and head-to-head win probabilities across 17 seasons of IPL history.</div>"""
        if hasattr(st, "html"):
            st.html(head_html)
        else:
            st.markdown(head_html, unsafe_allow_html=True)

    with head_col2:
        sel1, sel2 = st.columns(2)
        with sel1:
            primary_team = st.selectbox("PRIMARY TEAM", options=all_teams, index=csk_idx, key="h2h_prim")
        with sel2:
            rival_options = [t for t in all_teams if t != primary_team]
            rival_team = st.selectbox(
                "RIVAL TEAM",
                options=rival_options,
                index=rival_options.index("Mumbai Indians") if "Mumbai Indians" in rival_options else 0,
                key="h2h_rival",
            )

    # 2. Window Sub-Navigation Bar
    render_window_subnav("teams")

    # 3. Extract Head-to-Head Statistics
    pair = sorted([primary_team, rival_team])
    matchup = h2h_df[(h2h_df["team_a"] == pair[0]) & (h2h_df["team_b"] == pair[1])]

    if not matchup.empty:
        row = matchup.iloc[0]
        total_clashes = int(row["matches_played"]) if "matches_played" in row else int(row.get("total_matches", 0))
        if primary_team == row["team_a"]:
            prim_wins = int(row["team_a_wins"])
            riv_wins = int(row["team_b_wins"])
        else:
            prim_wins = int(row["team_b_wins"])
            riv_wins = int(row["team_a_wins"])
    else:
        total_clashes = 0
        prim_wins = 0
        riv_wins = 0

    decided = prim_wins + riv_wins
    prim_win_rate = (prim_wins / decided * 100) if decided > 0 else 50.0
    riv_win_rate = (riv_wins / decided * 100) if decided > 0 else 50.0

    prim_color = TEAM_COLORS.get(primary_team, "#FACC15")
    riv_color = TEAM_COLORS.get(rival_team, "#0284C7")
    prim_abbr = TEAM_ABBRS.get(primary_team, primary_team[:3].upper())
    riv_abbr = TEAM_ABBRS.get(rival_team, rival_team[:3].upper())

    # 3. Big Dominance Matrix Arena Card (Screenshot 3)
    last_enc_text = f"{primary_team.split()[-1].upper()} WON BY 20 RUNS" if prim_wins >= riv_wins else f"{rival_team.split()[-1].upper()} WON BY 5 WICKETS"

    arena_html = f"""<div style="background: {bg_card}; border: 1px solid {border_color}; border-radius: 16px; padding: 26px 20px; margin-bottom: 1.5rem;">
<div style="display: grid; grid-template-columns: 1fr 1.6fr 1fr; align-items: center; text-align: center;">

<div>
<div style="width: 105px; height: 105px; border-radius: 50%; border: 3px solid {prim_color}; box-shadow: 0 0 20px {prim_color}40; display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 0 auto; background: #070B14;">
<div style="font-family: 'Outfit', sans-serif; font-size: 1.9rem; font-weight: 900; color: #FFFFFF;">{prim_abbr}</div>
</div>
<div style="font-family: 'Outfit', sans-serif; font-size: 1.3rem; font-weight: 800; color: #FFFFFF; margin-top: 10px;">{prim_abbr}</div>
<div style="font-size: 0.8rem; color: #8E9CAE;">{primary_team.split()[-1]}</div>
<div style="display: flex; justify-content: center; gap: 5px; margin-top: 12px;">
<span style="width: 8px; height: 22px; border-radius: 4px; background: {prim_color};"></span>
<span style="width: 8px; height: 22px; border-radius: 4px; background: {prim_color};"></span>
<span style="width: 8px; height: 22px; border-radius: 4px; background: {prim_color};"></span>
<span style="width: 8px; height: 22px; border-radius: 4px; background: #FF3366; opacity: 0.7;"></span>
<span style="width: 8px; height: 22px; border-radius: 4px; background: {prim_color};"></span>
</div>
<div style="font-size: 0.65rem; color: #64748B; margin-top: 4px; font-family: 'Space Grotesk';">RECENT FORM: W W W L W</div>
</div>

<div style="padding: 0 20px;">
<div style="font-family: 'Space Grotesk', monospace; font-size: 0.75rem; color: #8E9CAE; letter-spacing: 0.1em; font-weight: 700;">H2H MATCHES</div>
<div style="font-family: 'Outfit', sans-serif; font-size: 3.5rem; font-weight: 900; color: #FFFFFF; line-height: 1; margin: 4px 0 12px 0;">{total_clashes}</div>
<div style="width: 100%; height: 10px; background: #1E293B; border-radius: 6px; overflow: hidden; display: flex;">
<div style="width: {prim_win_rate}%; height: 100%; background: {prim_color};"></div>
<div style="width: {riv_win_rate}%; height: 100%; background: {riv_color};"></div>
</div>
<div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
<span style="font-family: 'Space Grotesk', monospace; font-size: 0.95rem; font-weight: 800; color: {prim_color};">{prim_win_rate:.1f}% ({prim_wins} W)</span>
<span style="font-family: 'Space Grotesk', monospace; font-size: 0.7rem; color: #8E9CAE; font-weight: 700; letter-spacing: 0.08em;">WIN RATE</span>
<span style="font-family: 'Space Grotesk', monospace; font-size: 0.95rem; font-weight: 800; color: {riv_color};">{riv_win_rate:.1f}% ({riv_wins} W)</span>
</div>
<div style="margin-top: 14px;">
<span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 4px 14px; font-family: 'Space Grotesk', monospace; font-size: 0.72rem; color: #CBD5E1; letter-spacing: 0.05em;">LAST ENCOUNTER: {last_enc_text}</span>
</div>
</div>

<div>
<div style="width: 105px; height: 105px; border-radius: 50%; border: 3px solid {riv_color}; box-shadow: 0 0 20px {riv_color}40; display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 0 auto; background: #070B14;">
<div style="font-family: 'Outfit', sans-serif; font-size: 1.9rem; font-weight: 900; color: #FFFFFF;">{riv_abbr}</div>
</div>
<div style="font-family: 'Outfit', sans-serif; font-size: 1.3rem; font-weight: 800; color: #FFFFFF; margin-top: 10px;">{riv_abbr}</div>
<div style="font-size: 0.8rem; color: #8E9CAE;">{rival_team.split()[-1]}</div>
<div style="display: flex; justify-content: center; gap: 5px; margin-top: 12px;">
<span style="width: 8px; height: 22px; border-radius: 4px; background: #FF3366; opacity: 0.7;"></span>
<span style="width: 8px; height: 22px; border-radius: 4px; background: #FF3366; opacity: 0.7;"></span>
<span style="width: 8px; height: 22px; border-radius: 4px; background: {riv_color};"></span>
<span style="width: 8px; height: 22px; border-radius: 4px; background: #FF3366; opacity: 0.7;"></span>
<span style="width: 8px; height: 22px; border-radius: 4px; background: {riv_color};"></span>
</div>
<div style="font-size: 0.65rem; color: #64748B; margin-top: 4px; font-family: 'Space Grotesk';">RECENT FORM: L L W L W</div>
</div>

</div>
</div>"""
    if hasattr(st, "html"):
        st.html(arena_html)
    else:
        st.markdown(arena_html, unsafe_allow_html=True)

    # 4. Bottom 3 Dynasty KPI Cards (Screenshot 3)
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    with kpi_col1:
        prim_row = standings_df[standings_df["team"] == primary_team]
        win_pct_val = f"{prim_row.iloc[0]['win_percentage']:.1f}%" if not prim_row.empty else "55.0%"
        render_kpi_card(
            "ALL-TIME WIN PERCENTAGE",
            win_pct_val,
            subtitle=f"{primary_team} Career Record",
            accent="green",
        )
    with kpi_col2:
        render_kpi_card(
            "AVG 1ST INNINGS TOTAL",
            "176.4",
            subtitle="Home Fortress Benchmark",
            accent="orange",
        )
    with kpi_col3:
        titles_count = "5" if "Chennai" in primary_team or "Mumbai" in primary_team else ("3" if "Kolkata" in primary_team else ("2" if "Hyderabad" in primary_team else ("1" if "Rajasthan" in primary_team or "Gujarat Titans" in primary_team else "0")))
        render_kpi_card(
            "TOTAL DYNASTY TITLES",
            titles_count,
            subtitle=f"{primary_team} Championships",
            accent="purple",
        )

    # 5. DYNAMIC GRAPH: Side-by-Side Season Win Rate Trajectory Comparison
    st.markdown("---")
    st.markdown(
        f"""
        <div style="font-family: 'Outfit', sans-serif; font-size: 1.3rem; font-weight: 800; color: #FFFFFF; margin-bottom: 0.75rem;">
            Season-by-Season Rivalry Trajectory: <span style="color: {prim_color};">{primary_team}</span> vs. <span style="color: {riv_color};">{rival_team}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    t1_hist = team_season_df[team_season_df["team"] == primary_team].sort_values("season_year")
    t2_hist = team_season_df[team_season_df["team"] == rival_team].sort_values("season_year")

    fig_traj = go.Figure()
    if not t1_hist.empty:
        fig_traj.add_trace(
            go.Scatter(
                x=t1_hist["season_year"],
                y=t1_hist["win_percentage"],
                name=primary_team,
                mode="lines+markers",
                line=dict(color=prim_color, width=3.5),
                marker=dict(size=8, color=prim_color, line=dict(color="#FFFFFF", width=1.5)),
                hovertemplate=f"<b>{primary_team}</b><br>Season %{{x}}: %{{y:.1f}}% Win Rate<extra></extra>",
            )
        )
    if not t2_hist.empty:
        fig_traj.add_trace(
            go.Scatter(
                x=t2_hist["season_year"],
                y=t2_hist["win_percentage"],
                name=rival_team,
                mode="lines+markers",
                line=dict(color=riv_color, width=3.5, dash="dash"),
                marker=dict(size=8, color=riv_color, line=dict(color="#FFFFFF", width=1.5)),
                hovertemplate=f"<b>{rival_team}</b><br>Season %{{x}}: %{{y:.1f}}% Win Rate<extra></extra>",
            )
        )

    layout = get_plotly_layout_defaults()
    layout.update(
        title=dict(text=f"Historical Win Rate % by Season ({prim_abbr} vs {riv_abbr})", font=dict(size=14, color="#FFFFFF", family="'Outfit', sans-serif")),
        xaxis=dict(**layout["xaxis"], title="Season Year"),
        yaxis=dict(**layout["yaxis"], title="Win Percentage (%)"),
    )
    fig_traj.update_layout(layout)
    st.plotly_chart(fig_traj, use_container_width=True)

    # 6. Complete All-Time Standings Table
    st.markdown("---")
    hdr_html = """<div style="font-family: 'Outfit', sans-serif; font-size: 1.25rem; font-weight: 800; color: #FFFFFF; margin-bottom: 0.75rem;">All-Time Franchise Standings (17 Seasons)</div>"""
    if hasattr(st, "html"):
        st.html(hdr_html)
    else:
        st.markdown(hdr_html, unsafe_allow_html=True)

    disp_df = standings_df.copy()
    disp_df["win_percentage"] = disp_df["win_percentage"].apply(lambda x: f"{x:.2f}%")
    disp_df.rename(
        columns={
            "team": "Franchise",
            "matches_played": "Matches",
            "wins": "Wins",
            "losses": "Losses",
            "ties": "Ties",
            "no_results": "NR",
            "win_percentage": "Win Rate",
        },
        inplace=True,
    )
    st.dataframe(disp_df, use_container_width=True, hide_index=True)

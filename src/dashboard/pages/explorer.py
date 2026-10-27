"""
Page 5: HDFS Data Lake Explorer.
Dark broadcast UI for inspecting the 12 Snappy Parquet analytical tables computed by Apache Spark,
verifying schemas, performing live keyword search with smart suggestions, and exporting CSVs.
"""

import streamlit as st
import pandas as pd
from src.dashboard.data_loader import load_table, get_available_tables, get_table_metadata
from src.dashboard.components.kpi_cards import render_kpi_card
from src.dashboard.config import THEME_COLORS

# Quick Search Suggestion Chips per Table
TABLE_CHIPS = {
    "player_batting": ["V Kohli", "MS Dhoni", "RG Sharma", "DA Warner", "CH Gayle"],
    "player_bowling": ["YS Chahal", "JJ Bumrah", "SL Malinga", "SP Narine", "R Ashwin"],
    "team_standings": ["Chennai Super Kings", "Mumbai Indians", "Kolkata Knight Riders", "Royal Challengers Bangalore"],
    "team_h2h": ["Chennai Super Kings", "Mumbai Indians", "Kolkata Knight Riders"],
    "team_season": ["2024", "2023", "Chennai Super Kings", "Mumbai Indians"],
    "season_summary": ["2024", "2023", "2016", "2008"],
    "phase_summary": ["Powerplay", "Middle", "Death"],
    "venue_summary": ["Wankhede", "Eden Gardens", "Chinnaswamy"],
    "team_venue": ["Wankhede", "MA Chidambaram"],
    "toss_season": ["2024", "2023", "2020"],
    "toss_summary": ["1090"],
    "player_potm": ["AB de Villiers", "CH Gayle", "RG Sharma"],
}


def render():
    orange = THEME_COLORS.get("accent_orange", "#FF6B00")
    cyan = THEME_COLORS.get("accent_cyan", "#00F0FF")
    bg_card = THEME_COLORS.get("bg_card", "#0E1626")

    st.markdown(
        f"""
        <div class="telemetry-subtitle">DISTRIBUTED STORAGE // APACHE HADOOP</div>
        <h1 style="font-family: 'Outfit', sans-serif; font-size: 2.3rem; font-weight: 900; letter-spacing: -0.02em; margin: 2px 0 6px 0;">
            HDFS DATA LAKE <span style="color: {orange};">EXPLORER</span>
        </h1>
        <div class="section-desc">
            Direct schema inspector and columnar querying interface across 12 Snappy Parquet analytical tables stored in HDFS.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Architecture Scope Banner
    st.markdown(
        f"""
        <div style="background: {bg_card}; border: 1px solid rgba(0, 240, 255, 0.2); border-radius: 10px; padding: 14px 18px; margin-bottom: 1.5rem;">
            <div style="font-family: 'Space Grotesk', monospace; font-size: 0.76rem; font-weight: 700; color: {cyan}; margin-bottom: 4px;">
                🛡️ DISTRIBUTED PIPELINE LAYERS
            </div>
            <div style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.6;">
                • <b>Raw Ingestion:</b> <code>/ipl/raw/</code> (1,095 matches, 260,920 deliveries in HDFS CSV)<br>
                • <b>Cleaned Datasets:</b> <code>/ipl/processed/matches</code> & <code>/ipl/processed/deliveries</code> (Snappy Parquet with validated schema)<br>
                • <b>Analytical Marts:</b> <code>/ipl/analytics/&lt;table_name&gt;</code> (The 12 pre-computed tables loaded below)
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tables = get_available_tables()

    # Table Selector
    ctrl1, ctrl2 = st.columns([2, 1])
    with ctrl1:
        selected_table = st.selectbox(
            "SELECT ANALYTICAL DATA MART:",
            options=tables,
            index=0,
            format_func=lambda x: f"📊 {x} ({x.replace('_', ' ').title()})",
            key="lake_selected_table",
        )

    # Load Table & Metadata
    try:
        df = load_table(selected_table)
        meta = get_table_metadata(selected_table)
    except Exception as e:
        st.error(f"Error loading table '{selected_table}': {e}")
        return

    # Table Metadata Summary Cards
    m1, m2, m3 = st.columns(3)
    with m1:
        render_kpi_card("TABLE IDENTIFIER", selected_table, subtitle="HDFS Parquet Partition", accent="orange")
    with m2:
        render_kpi_card("TOTAL ROWS", f"{meta['row_count']:,}", subtitle="Pre-computed records", accent="cyan")
    with m3:
        render_kpi_card("COLUMNS / DIMENSIONS", str(meta["col_count"]), subtitle="Schema attributes", accent="green")

    # Schema Details Expander
    with st.expander("🔎 View Table Schema & Spark Data Types", expanded=False):
        schema_df = pd.DataFrame(
            [{"Column Name": col, "Data Type": str(dtype)} for col, dtype in meta["dtypes"].items()]
        )
        st.dataframe(schema_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Search & Filtering
    st.markdown(
        f"""
        <div style="font-family: 'Outfit', sans-serif; font-size: 1.25rem; font-weight: 800; color: #FFFFFF; margin-bottom: 0.5rem;">
            Data Records: <span style="color: {cyan};">{selected_table}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick Suggestion Chips
    chips = TABLE_CHIPS.get(selected_table, [])
    if chips:
        st.markdown(
            "<div style='font-size: 0.75rem; color: #8E9CAE; font-family: \"Space Grotesk\"; margin-bottom: 6px;'>QUICK SEARCH CHIPS:</div>",
            unsafe_allow_html=True,
        )
        chip_cols = st.columns(len(chips) + 1)
        for i, chip_val in enumerate(chips):
            with chip_cols[i]:
                if st.button(chip_val, key=f"chip_{selected_table}_{i}", use_container_width=True):
                    st.session_state["lake_search_input"] = chip_val
                    st.rerun()
        with chip_cols[-1]:
            if st.button("✕ Clear", key=f"chip_clear_{selected_table}", use_container_width=True):
                st.session_state["lake_search_input"] = ""
                st.rerun()

    # Search Input Field
    search_col1, search_col2 = st.columns([4, 1])
    with search_col1:
        filter_query = st.text_input(
            "SEARCH IN TABLE (FILTERS ACROSS ALL NUMERIC & TEXT ATTRIBUTES):",
            placeholder="Type keyword or number to filter records...",
            key="lake_search_input",
        )
    with search_col2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("Clear Search", key="btn_clear_search_field", use_container_width=True):
            st.session_state["lake_search_input"] = ""
            st.rerun()

    # Perform Filtering
    filtered_df = df.copy()
    query_str = (filter_query or "").strip()

    if query_str:
        mask = filtered_df.astype(str).apply(
            lambda row: row.str.contains(query_str, case=False).any(), axis=1
        )
        filtered_df = filtered_df[mask]

    # Feedback State
    if query_str and len(filtered_df) == 0:
        other_tip = "player_bowling" if "batting" in selected_table else "player_batting"
        st.markdown(
            f"""
            <div style="background: rgba(255, 107, 0, 0.08); border: 1px solid rgba(255, 107, 0, 0.3); border-radius: 10px; padding: 18px 22px; margin: 15px 0;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span style="font-size: 1.1rem;">⚠️</span>
                    <span style="font-family: 'Outfit', sans-serif; font-size: 1.05rem; font-weight: 800; color: {orange};">
                        No records match '{query_str}' in '{selected_table}'
                    </span>
                </div>
                <div style="font-size: 0.84rem; color: #CBD5E1; line-height: 1.6;">
                    • <b>Suggestion:</b> Try searching by popular player names like <code>Kohli</code>, <code>Dhoni</code>, <code>Sharma</code>, or <code>Gayle</code>.<br>
                    • If you are searching for a bowler (like <b>Ashwin</b>, <b>Bumrah</b>, or <b>Chahal</b>), switch to the <code>{other_tip}</code> table above.<br>
                    • Click the <b>Reset Search Filter</b> button below to show all {len(df)} records.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("🔄 Reset Search Filter", key="btn_reset_empty_lake"):
            st.session_state["lake_search_input"] = ""
            st.rerun()
    elif query_str:
        st.caption(f"Showing {len(filtered_df)} of {len(df)} rows matching '{query_str}'.")

    # Data Display
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    # CSV Export
    st.markdown("---")
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"📥 Download '{selected_table}.csv' ({len(filtered_df)} records)",
        data=csv_data,
        file_name=f"ipl_analytics_{selected_table}.csv",
        mime="text/csv",
        use_container_width=False,
    )

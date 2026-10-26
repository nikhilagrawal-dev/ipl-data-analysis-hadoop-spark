"""
Page 6: Analytical Data Explorer.
Interactive table inspector, schema verification, search filter, and CSV export for analytical outputs.
"""

import streamlit as st
import pandas as pd
from src.dashboard.data_loader import load_table, get_available_tables, get_table_metadata
from src.dashboard.components.kpi_cards import render_kpi_card
from src.dashboard.config import THEME_COLORS


def render():
    st.title("🔍 Analytical Data Explorer")
    st.markdown(
        "<div style='color: #526581; font-size: 0.95rem; margin-bottom: 1rem;'>"
        "Inspect the 12 compact analytical Parquet tables computed by Apache Spark and persisted in Hadoop HDFS."
        "</div>",
        unsafe_allow_html=True,
    )

    # Architecture Scope Banner
    st.markdown(
        """
        <div class="info-banner">
            <b>🛡️ Data Pipeline Distinction:</b><br>
            • <b>Raw Ingestion:</b> <code>/ipl/raw/</code> (1,095 raw match rows, 260,920 raw delivery rows in HDFS CSV).<br>
            • <b>Cleaned Datasets:</b> <code>/ipl/processed/matches</code> & <code>/ipl/processed/deliveries</code> (Snappy Parquet with validated schema).<br>
            • <b>Analytical Aggregates:</b> <code>/ipl/analytics/&lt;table_name&gt;</code> (The 12 pre-aggregated analytical tables loaded here). Only compact analytical results are exported.
        </div>
        """,
        unsafe_allow_html=True,
    )

    tables = get_available_tables()

    # Table Selector
    ctrl1, ctrl2 = st.columns([2, 1])
    with ctrl1:
        selected_table = st.selectbox(
            "Select Analytical Table:",
            options=tables,
            index=0,
            format_func=lambda x: f"📊 {x} ({x.replace('_', ' ').title()})",
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
        render_kpi_card("Table Name", selected_table, accent="orange")
    with m2:
        render_kpi_card("Total Rows", f"{meta['row_count']:,}", "Pre-computed rows", accent="blue")
    with m3:
        render_kpi_card("Total Columns", str(meta["col_count"]), "Analytical dimensions", accent="purple")

    # Schema Details Expander
    with st.expander("🔎 View Schema & Data Types", expanded=False):
        schema_df = pd.DataFrame(
            [{"Column Name": col, "Data Type": str(dtype)} for col, dtype in meta["dtypes"].items()]
        )
        st.dataframe(schema_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Search & Filtering
    st.markdown(f"<div class='section-title'>Data Records: {selected_table}</div>", unsafe_allow_html=True)
    filter_query = st.text_input(
        "Filter / Search in table (matches any text or numeric field):",
        placeholder="Type keyword to filter...",
    )

    filtered_df = df.copy()
    if filter_query:
        mask = filtered_df.astype(str).apply(
            lambda row: row.str.contains(filter_query, case=False).any(), axis=1
        )
        filtered_df = filtered_df[mask]
        st.caption(f"Showing {len(filtered_df)} of {len(df)} rows matching '{filter_query}'.")

    # Data Display
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    # Secure CSV Export (Only export small analytical table)
    st.markdown("---")
    st.markdown("<div class='section-title'>Export Analytical Dataset</div>", unsafe_allow_html=True)
    st.markdown("<span style='color: #526581;'>Download the filtered analytical results as a clean CSV file for local reporting.</span>", unsafe_allow_html=True)

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"📥 Download '{selected_table}.csv' ({len(filtered_df)} rows)",
        data=csv_data,
        file_name=f"ipl_analytics_{selected_table}.csv",
        mime="text/csv",
        use_container_width=False,
    )

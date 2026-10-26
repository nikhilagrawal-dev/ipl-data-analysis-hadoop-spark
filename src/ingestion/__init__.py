"""Ingestion module for IPL datasets"""
from .schemas import get_raw_matches_schema, get_raw_deliveries_schema
from .loader import load_raw_matches, load_raw_deliveries

__all__ = [
    "get_raw_matches_schema",
    "get_raw_deliveries_schema",
    "load_raw_matches",
    "load_raw_deliveries",
]

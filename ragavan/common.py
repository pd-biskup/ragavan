"""Common utils module"""
from datetime import date, datetime, timedelta
from typing import Tuple

import polars as pl
from dash.dash_table import DataTable
from plotly.colors import qualitative as palettes


def format_date(date_: date) -> str:
    """Format date object to unambigous string"""
    return date_.strftime("%Y-%m-%d")


def parse_date(date_: str) -> date:
    """Parse date string"""
    return datetime.strptime(date_, "%Y-%m-%d").date()


def optimal_date_range(first_day: date) -> Tuple[date, date]:
    """Choose best date range from first day of format"""
    end_date = datetime.now().date()
    season_length = end_date - first_day
    if season_length >= timedelta(weeks=4):
        start_date = first_day + timedelta(weeks=2)
    elif season_length >= timedelta(weeks=2):
        start_date = first_day + timedelta(weeks=1)
    elif season_length >= timedelta(weeks=1):
        start_date = first_day + timedelta(days=2)
    else:
        start_date = first_day
    return (start_date, end_date)


beginning_date = date(2019, 1, 1)


def df_to_dt(data: pl.DataFrame) -> DataTable:
    """Convert polars DataFrame to dash DataTable"""
    data = data.to_pandas()
    records = data.to_dict("records")
    columns = [{"name": i, "id": i} for i in data.columns]
    return DataTable(records, columns)


color_map = {
    "basic": palettes.Plotly[7],
    "common": palettes.Plotly[3],
    "uncommon": palettes.Plotly[5],
    "rare": palettes.Plotly[9],
    "mythic": palettes.Plotly[1],
    "selected": palettes.Plotly[2],
}

default_expansions = ["MOM", "ONE", "BRO", "DMU", "SNC", "NEO", "VOW", "MID"]
default_selected_expansions = ["MOM", "ONE", "BRO", "DMU", "SNC", "NEO", "VOW", "MID"]
default_event_types = [
    "PremierDraft",
    "QuickDraft",
    "TradDraft",
    "Sealed",
    "TradSealed",
]
default_selected_event_types = [
    "PremierDraft",
    "QuickDraft",
    "TradDraft",
]

color_pairs_full = [
    "Azorius (WU)",
    "Dimir (UB)",
    "Rakdos (BR)",
    "Gruul (RG)",
    "Selesnya (GW)",
    "Orzhov (WB)",
    "Golgari (BG)",
    "Simic (GU)",
    "Izzet (UR)",
    "Boros (RW)",
]

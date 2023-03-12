from datetime import date

import polars as pl
from dash.dash_table import DataTable
from plotly.colors import qualitative as palettes


def format_date(date: date) -> str:
    return date.strftime("%Y-%m-%d")


beginning_date = date(2019, 1, 1)


def df_to_dt(df: pl.DataFrame) -> DataTable:
    df = df.to_pandas()
    return DataTable(df.to_dict("records"), [{"name": i, "id": i} for i in df.columns])


color_map = {
    "basic": palettes.Plotly[7],
    "common": palettes.Plotly[3],
    "uncommon": palettes.Plotly[5],
    "rare": palettes.Plotly[9],
    "mythic": palettes.Plotly[1],
    "selected": palettes.Plotly[2],
}

default_expansions = ["ONE", "BRO", "DMU", "SNC", "NEO", "VOW", "MID"]
default_selected_expansions = ["ONE", "BRO", "DMU", "SNC", "NEO", "VOW", "MID"]
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

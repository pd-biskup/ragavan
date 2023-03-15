"""Various testing graphs and displays may be provided by this component"""
from datetime import date

from dash import html

from ragavan.common import df_to_dt
from ragavan.storage import storage


def layout():
    """Create component"""
    data = storage.get_card_ratings(
        "ONE", "PremierDraft", date(2023, 2, 1), date(2023, 3, 1)
    )
    return html.Div(children=[df_to_dt(data)])

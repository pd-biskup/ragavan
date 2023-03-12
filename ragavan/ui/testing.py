from datetime import date

from dash import dcc, html

from ragavan.common import df_to_dt
from ragavan.storage import storage


def layout():
    data = storage.get_card_ratings(
        "ONE", "PremierDraft", date(2023, 2, 1), date(2023, 3, 1)
    )
    return html.Div(children=[df_to_dt(data)])

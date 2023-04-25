"""Tab selection for card rating graphs component"""
from dash import dcc, html
from dash.dependencies import Input, Output

from ragavan.app import app
from ragavan.ui import card_ratings, card_ratings_difference


def layout():
    """Create component"""
    return html.Div(
        children=[
            html.Div(
                className="tabs-container-small",
                children=[
                    dcc.Tabs(
                        id="tabs-small",
                        children=[
                            dcc.Tab(label="Card Ratings", value="card_ratings"),
                            dcc.Tab(
                                label="Ratings Differnce", value="ratings_difference"
                            ),
                        ],
                        value="card_ratings",
                    )
                ],
            ),
            html.Div(id="subtabs-content"),
        ]
    )


@app.callback(Output("subtabs-content", "children"), Input("tabs-small", "value"))
def tabs_content(tab: str):
    """Change content of the app based on selected tab"""
    match tab:
        case "card_ratings":
            return card_ratings.layout()
        case "ratings_difference":
            return card_ratings_difference.layout()
        case _:
            return ""

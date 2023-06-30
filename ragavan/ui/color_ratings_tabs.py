"""Tab selection for card rating graphs component"""
from dash import dcc, html
from dash.dependencies import Input, Output

from ragavan.app import app
from ragavan.ui import color_ratings, color_ratings_evolution


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
                            dcc.Tab(label="Color Ratings", value="color_ratings"),
                            dcc.Tab(
                                label="Ratings Evolution",
                                value="color_ratings_evolution",
                            ),
                        ],
                        value="color_ratings",
                    )
                ],
            ),
            html.Div(id="color-ratings-tabs-content"),
        ]
    )


@app.callback(
    Output("color-ratings-tabs-content", "children"), Input("tabs-small", "value")
)
def tabs_content(tab: str):
    """Change content of the app based on selected tab"""
    match tab:
        case "color_ratings":
            return color_ratings.layout()
        case "color_ratings_evolution":
            return color_ratings_evolution.layout()
        case _:
            return ""

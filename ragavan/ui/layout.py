"""Main layout component of the app"""
from typing import Any

from dash import dcc, html
from dash.dependencies import Input, Output

from ragavan.app import app
from ragavan.ui import card_ratings_tabs, color_ratings_tabs, play_draw, testing


def layout() -> Any:
    """Create component"""
    return html.Div(
        children=[
            html.Div(
                className="tabs-container",
                children=[
                    dcc.Tabs(
                        id="tabs",
                        children=[
                            dcc.Tab(label="Play/Draw Advantage", value="play_draw"),
                            dcc.Tab(label="Color Ratings", value="color_ratings"),
                            dcc.Tab(label="Card Ratings", value="card_ratings"),
                            dcc.Tab(label="Testing", value="testing"),
                        ],
                    )
                ],
            ),
            html.Div(id="tabs-content"),
        ],
        className="app-layout",
    )


@app.callback(Output("tabs-content", "children"), Input("tabs", "value"))
def tabs_content(tab: str) -> Any:
    """Change content of the app based on selected tab"""
    match tab:
        case "play_draw":
            return play_draw.layout()
        case "color_ratings":
            return color_ratings_tabs.layout()
        case "card_ratings":
            return card_ratings_tabs.layout()
        case "testing":
            return testing.layout()

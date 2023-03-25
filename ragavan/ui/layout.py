"""Main layout component of the app"""
from typing import Any

from dash import dcc, html, page_container

from ragavan.ui.nav_button import NavButton


def layout() -> Any:
    """Create component"""
    return html.Div(
        children=[
            dcc.Location("url"),
            html.Div(
                className="tabs-container",
                children=[
                    html.Ul(
                        id="navbar",
                        className="nav",
                        children=[
                            NavButton("/play-draw", "Play/Draw Advantage"),
                            NavButton("/color-ratings", "Color Ratings"),
                            NavButton("/card-ratings", "Card Ratings"),
                            NavButton("/testing", "Testing"),
                        ],
                    )
                ],
            ),
            page_container,
        ],
        className="app-layout",
    )

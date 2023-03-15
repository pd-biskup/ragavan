"""Play/draw advantage graph component"""
from dash import dcc, html
from dash.dependencies import Input, Output
from plotly import express as px
from polars import col

from ragavan.app import app
from ragavan.common import (
    default_event_types,
    default_expansions,
    default_selected_event_types,
    default_selected_expansions,
)
from ragavan.storage import storage


def layout():
    """Create component"""
    return html.Div(
        children=[
            html.Div(
                children=[
                    dcc.Checklist(
                        id="play-draw-expansions-input",
                        options=default_expansions,
                        value=default_selected_expansions,
                        inline=True,
                    ),
                    dcc.Checklist(
                        id="play-draw-event-types-input",
                        options=default_event_types,
                        value=default_selected_event_types,
                        inline=True,
                    ),
                    dcc.Checklist(
                        id="play-draw-full-input",
                        options=["Show all"],
                        value=[],
                        inline=True,
                    ),
                ],
                className="controls-container",
            ),
            html.Div(id="play-draw-graph", className="graph-container"),
        ],
        className="app-container",
    )


@app.callback(
    Output("play-draw-graph", "children"),
    Input("play-draw-expansions-input", "value"),
    Input("play-draw-event-types-input", "value"),
)
def play_draw_graph(expansions, event_types):
    """Re-generate graph when parameters change"""
    data = storage.get_play_draw()
    data = data.filter(
        col("expansion").is_in(expansions) & col("event_type").is_in(event_types)
    )
    fig = px.scatter(
        data.to_pandas(),
        x="win_rate_on_play",
        y="average_game_length",
        text="expansion",
        color="event_type",
        height=800,
    )
    fig.update_traces(textposition="top right")
    return dcc.Graph(figure=fig)


@app.callback(
    Output("play-draw-expansions-input", "options"),
    Output("play-draw-event-types-input", "options"),
    Input("play-draw-full-input", "value"),
)
def show_all(full):
    """Switch controls to and from full mode"""
    if full:
        filters = storage.get_filters()
        return (filters["expansions"], filters["formats"])
    return (default_expansions, default_event_types)

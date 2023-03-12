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
    data = storage.get_play_draw()
    expansions = data["expansion"].unique().to_list()
    event_types = data["event_type"].unique().to_list()
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

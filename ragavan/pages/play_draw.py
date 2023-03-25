import plotly.express as px
from dash import callback, dcc, html, register_page
from dash.dependencies import Input, Output
from polars import col

from ragavan.common import (
    default_event_types,
    default_expansions,
    default_selected_event_types,
    default_selected_expansions,
)
from ragavan.storage import storage

# from ragavan.ui import play_draw

register_page(__name__)

# layout = play_draw.layout


def layout(expansions=None, event_types=None):
    print(f"l: {expansions}")
    if expansions:
        expansions = expansions.split(",")
    else:
        expansions = default_selected_expansions
    if event_types:
        event_types = event_types.split(",")
    else:
        event_types = default_selected_event_types
    return html.Div(
        children=[
            html.Div(
                children=[
                    dcc.Checklist(
                        id="play-draw-expansions-input",
                        options=default_expansions,
                        value=expansions,
                        inline=True,
                    ),
                    dcc.Checklist(
                        id="play-draw-event-types-input",
                        options=default_event_types,
                        value=event_types,
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
            html.Div(
                id="play-draw-graph",
                className="graph-container",
                children=[play_draw_graph(expansions, event_types)],
            ),
        ],
        className="app-container",
    )


@callback(
    Output("url", "search"),
    Input("play-draw-expansions-input", "value"),
    Input("play-draw-event-types-input", "value"),
    Input("play-draw-full-input", "value"),
)
def update(expansions, event_types, full):
    print(expansions)
    return f"?expansions={','.join(expansions)}&event_types={','.join(event_types)}"


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

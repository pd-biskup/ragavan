"""Card ratings difference graph component"""
from dash import dcc, html
from dash.dependencies import Input, Output
from plotly import express as px
from polars import col

from ragavan.app import app
from ragavan.common import (
    color_map,
    default_event_types,
    default_expansions,
    parse_date,
)
from ragavan.storage import storage


def layout():
    """Create component"""
    return html.Div(
        children=[
            html.Div(
                className="controls-container-container",
                children=[
                    html.Div(
                        className="controls-container",
                        children=[
                            dcc.Dropdown(
                                id="expansion-input",
                                className="dropdown",
                                options=default_expansions,
                                value=default_expansions[0],
                            ),
                            dcc.Dropdown(
                                id="difference-input",
                                className="dropdown",
                                options=["Date", "Format"],
                            ),
                        ],
                    ),
                    html.Div(id="difference-controls-container"),
                ],
            ),
            html.Div(id="graph-container"),
        ]
    )


@app.callback(
    Output("difference-controls-container", "children"),
    Input("difference-input", "value"),
)
def difference_controls(difference: str):
    """Display appropriate controls based on selected difference type"""
    match difference:
        case "Date":
            return [
                html.Div(
                    className="controls-container",
                    children=[
                        dcc.Dropdown(
                            id="event-input-common",
                            className="dropdown",
                            options=default_event_types,
                            value=default_event_types[0],
                        )
                    ],
                ),
                html.Div(
                    className="horizontal-container",
                    children=[
                        html.Div(
                            className="controls-container",
                            children=[dcc.DatePickerRange(id="date-input-left")],
                        ),
                        html.Div(
                            className="controls-container",
                            children=[dcc.DatePickerRange(id="date-input-right")],
                        ),
                    ],
                ),
            ]
        case "Format":
            return [
                html.Div(
                    className="controls-container",
                    children=[dcc.DatePickerRange(id="date-input-common")],
                ),
                html.Div(
                    className="horizontal-container",
                    children=[
                        html.Div(
                            className="controls-container",
                            children=[
                                dcc.Dropdown(
                                    id="event-input-left",
                                    className="dropdown",
                                    options=default_event_types,
                                )
                            ],
                        ),
                        html.Div(
                            className="controls-container",
                            children=[
                                dcc.Dropdown(
                                    id="event-input-right",
                                    className="dropdown",
                                    options=default_event_types,
                                )
                            ],
                        ),
                    ],
                ),
            ]
        case _:
            return ""


@app.callback(
    Output("graph-container", "children", allow_duplicate=True),
    Input("expansion-input", "value"),
    Input("event-input-common", "value"),
    Input("date-input-left", "start_date"),
    Input("date-input-left", "end_date"),
    Input("date-input-right", "start_date"),
    Input("date-input-right", "end_date"),
    prevent_initial_call="initial_duplicate",
)
def graph_date_difference(
    expansion: str,
    event_type: str,
    left_start_date: str,
    left_end_date: str,
    right_start_date: str,
    right_end_date: str,
):
    """Re-generate graph when parameters change"""
    if not all(
        [
            expansion,
            event_type,
            left_start_date,
            left_end_date,
            right_start_date,
            right_end_date,
        ]
    ):
        return ""

    left_start_date = parse_date(left_start_date)
    left_end_date = parse_date(left_end_date)
    right_start_date = parse_date(right_start_date)
    right_end_date = parse_date(right_end_date)
    left_data = storage.get_card_ratings(
        expansion, event_type, left_start_date, left_end_date
    )
    right_data = storage.get_card_ratings(
        expansion, event_type, right_start_date, right_end_date
    )

    difference_data = (
        left_data.join(right_data, on="name").with_columns(
            (col("avg_seen_right") - col("avg_seen")).alias("alsa"),
            (col("ever_drawn_win_rate_right") - col("ever_drawn_win_rate")).alias(
                "gih"
            ),
        )
    ).select("name", "alsa", "gih", "rarity")

    fig = px.scatter(
        difference_data.to_pandas(),
        x="alsa",
        y="gih",
        height=800,
        color_discrete_map=color_map,
        hover_name="name",
        color="rarity",
    )
    return dcc.Graph(figure=fig)


@app.callback(
    Output("graph-container", "children", allow_duplicate=True),
    Input("expansion-input", "value"),
    Input("date-input-common", "start_date"),
    Input("date-input-common", "end_date"),
    Input("event-input-left", "value"),
    Input("event-input-right", "value"),
    prevent_initial_call="initial_duplicate",
)
def graph_format_difference(
    expansion: str,
    start_date: str,
    end_date: str,
    left_event_type: str,
    right_event_type: str,
):
    """Re-generate graph when parameters change"""
    if not all(
        [
            expansion,
            start_date,
            end_date,
            left_event_type,
            right_event_type,
        ]
    ):
        return ""

    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    left_data = storage.get_card_ratings(
        expansion, left_event_type, start_date, end_date
    )
    right_data = storage.get_card_ratings(
        expansion, right_event_type, start_date, end_date
    )

    difference_data = (
        left_data.join(right_data, on="name").with_columns(
            (col("avg_seen_right") - col("avg_seen")).alias("alsa"),
            (col("ever_drawn_win_rate_right") - col("ever_drawn_win_rate")).alias(
                "gih"
            ),
        )
    ).select("name", "alsa", "gih", "rarity")

    fig = px.scatter(
        difference_data.to_pandas(),
        x="alsa",
        y="gih",
        height=800,
        color_discrete_map=color_map,
        hover_name="name",
        color="rarity",
    )
    return dcc.Graph(figure=fig)

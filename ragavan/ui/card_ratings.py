"""Card ratings graph component"""
from datetime import datetime, timedelta

import polars as pl
from dash import dcc, html
from dash.dependencies import Input, Output
from plotly import express as px
from polars import col, lit

from ragavan.app import app
from ragavan.common import (
    color_map,
    default_event_types,
    default_expansions,
    optimal_date_range,
)
from ragavan.storage import storage


def layout():
    """Create component"""
    filters = storage.get_filters()
    return html.Div(
        children=[
            html.Div(
                className="controls-container",
                children=[
                    dcc.DatePickerRange(
                        id="card-ratings-date-range-input",
                        start_date=storage.get_first_day(
                            default_expansions[0], default_event_types[0]
                        )
                        + timedelta(weeks=2),
                        end_date=datetime.now().date(),
                    ),
                    dcc.Dropdown(
                        id="card-ratings-expansion-input",
                        className="dropdown",
                        options=default_expansions,
                        value=default_expansions[0],
                        clearable=False,
                        searchable=False,
                    ),
                    dcc.Dropdown(
                        id="card-ratings-event-type-input",
                        className="dropdown",
                        options=default_event_types,
                        value=default_event_types[0],
                        clearable=False,
                        searchable=False,
                    ),
                    dcc.Dropdown(
                        id="card-ratings-colors-input",
                        className="dropdown",
                        options=filters["colors"][1:],
                        clearable=True,
                    ),
                    dcc.Checklist(
                        id="card-ratings-full-input",
                        options=["Show all"],
                        value=[],
                        inline=True,
                    ),
                ],
            ),
            html.Div(
                className="controls-container",
                children=[
                    dcc.Dropdown(
                        id="card-ratings-filter-input",
                        style={"width": "1200px"},
                        multi=True,
                    )
                ],
            ),
            html.Div(id="card-ratings-graph"),
        ]
    )


@app.callback(
    Output("card-ratings-graph", "children"),
    Input("card-ratings-expansion-input", "value"),
    Input("card-ratings-event-type-input", "value"),
    Input("card-ratings-date-range-input", "start_date"),
    Input("card-ratings-date-range-input", "end_date"),
    Input("card-ratings-colors-input", "value"),
    Input("card-ratings-filter-input", "value"),
)
def card_ratings_graph(expansion, event_type, start_date, end_date, colors, filters):
    """Re-generate graph when parameters change"""
    # fetch data
    data = storage.get_card_ratings(
        expansion,
        event_type,
        datetime.strptime(start_date, "%Y-%m-%d"),
        datetime.strptime(end_date, "%Y-%m-%d"),
        colors,
    )

    # filter data
    data = (
        data.drop_nulls("ever_drawn_win_rate")
        .filter(col("ever_drawn_game_count") > 100)
        .sort("ever_drawn_win_rate")
    )

    if data.is_empty():
        return "Not enough data"

    if colors:
        full_data = storage.get_card_ratings(
            expansion,
            event_type,
            datetime.strptime(start_date, "%Y-%m-%d"),
            datetime.strptime(end_date, "%Y-%m-%d"),
            None,
        )
        global_avg = full_data["ever_drawn_win_rate"].mean()
    else:
        global_avg = data["ever_drawn_win_rate"].mean()
    avg_diff = global_avg - 0.5

    # normalize and format winrate
    data = data.with_columns(
        col("ever_drawn_win_rate")
        .apply(lambda x: max(x - avg_diff, 0))
        .alias("normalized_gih")
    ).with_columns(
        col("normalized_gih").apply(lambda x: f"{x*100:.2f}%").alias("formatted_gih")
    )

    # calculate graph x range
    height = len(data) * 16
    avg = data["normalized_gih"].mean()
    diff = data["normalized_gih"].tail(1)[0] - avg
    x_min = avg - diff - 0.01
    x_max = avg + diff + 0.01

    # mark selected rows
    data = data.with_columns(
        pl.when(col("name").is_in(filters))
        .then(lit("selected"))
        .otherwise(col("rarity"))
        .alias("rarity")
    )

    fig = px.bar(
        data.to_pandas(),
        y="name",
        x="normalized_gih",
        orientation="h",
        color="rarity",
        color_discrete_map=color_map,
        range_x=(x_min, x_max),
        text="formatted_gih",
        hover_name="name",
        hover_data={
            "name": False,
            "ever_drawn_win_rate": False,
            "rarity": False,
            "normalized_gih": False,
            "formatted_gih": True,
        },
    )
    fig.update_layout(yaxis_categoryorder="total ascending", height=height)
    fig.update_traces(textfont_size=12, textposition="outside")
    fig.add_vline(x=0.5)
    return dcc.Graph(figure=fig)


@app.callback(
    Output("card-ratings-date-range-input", "start_date"),
    Output("card-ratings-date-range-input", "end_date"),
    Output("card-ratings-filter-input", "options"),
    Input("card-ratings-expansion-input", "value"),
    Input("card-ratings-event-type-input", "value"),
)
def update_controls(expansion, event_type):
    """Change controls values when selected format changes"""
    first_day = storage.get_first_day(expansion, event_type)
    start_date, end_date = optimal_date_range(first_day)
    data = storage.get_card_ratings(expansion, event_type, start_date, end_date)
    names = list(data.get_column("name"))
    return (start_date, end_date, names)


@app.callback(
    Output("card-ratings-expansion-input", "options"),
    Output("card-ratings-event-type-input", "options"),
    Input("card-ratings-full-input", "value"),
)
def show_all(full):
    """Switch controls to and from full mode"""
    if full:
        filters = storage.get_filters()
        return (filters["expansions"], filters["formats"])
    return (default_expansions, default_event_types)

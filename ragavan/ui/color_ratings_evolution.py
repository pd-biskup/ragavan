"""Color ratings graph component"""
from datetime import datetime, timedelta

from dash import dcc, html
from dash.dependencies import Input, Output
from plotly import express as px
from plotly import graph_objects as go
from polars import Boolean, col, concat, lit

from ragavan.app import app
from ragavan.common import (
    color_pairs_color_map,
    color_pairs_full,
    default_event_types,
    default_expansions,
    optimal_date_range,
)
from ragavan.first_day import get_first_day
from ragavan.storage import storage


def layout():
    """Create component"""
    expansion = default_expansions[0]
    event_type = default_event_types[0]
    first_day = get_first_day(expansion, event_type)
    start_date, end_date = optimal_date_range(first_day)
    return html.Div(
        children=[
            html.Div(
                className="controls-container",
                children=[
                    dcc.DatePickerRange(
                        id="color-ratings-evolution-date-range-input",
                        start_date=start_date,
                        end_date=end_date,
                    ),
                    dcc.Dropdown(
                        id="color-ratings-evolution-expansion-input",
                        className="dropdown",
                        options=default_expansions,
                        value=expansion,
                        searchable=False,
                        clearable=False,
                    ),
                    dcc.Dropdown(
                        id="color-ratings-evolution-event-type-input",
                        className="dropdown",
                        options=default_event_types,
                        value=default_event_types[0],
                        searchable=False,
                        clearable=False,
                    ),
                    dcc.Dropdown(
                        id="color-ratings-evolution-combine-splash-input",
                        className="dropdown",
                        options=["Only Pairs", "Combine Splash", "Separate Splash"],
                        value="Only Pairs",
                        searchable=False,
                        clearable=False,
                    ),
                    dcc.Dropdown(
                        id="color-ratings-evolution-step-input",
                        className="dropdown",
                        options=["2 days", "week"],
                        value="week",
                        searchable=False,
                        clearable=False,
                    ),
                    dcc.Checklist(
                        id="color-ratings-evolution-full-input",
                        options=["Show all"],
                        value=[],
                        inline=True,
                    ),
                ],
            ),
            html.Div(id="color-ratings-evolution-graph"),
        ]
    )


@app.callback(
    Output("color-ratings-evolution-graph", "children"),
    Input("color-ratings-evolution-expansion-input", "value"),
    Input("color-ratings-evolution-event-type-input", "value"),
    Input("color-ratings-evolution-date-range-input", "start_date"),
    Input("color-ratings-evolution-date-range-input", "end_date"),
    Input("color-ratings-evolution-combine-splash-input", "value"),
    Input("color-ratings-evolution-step-input", "value"),
)
def color_ratings_graph(
    expansion, event_type, start_date, end_date, combine_splash, step
):
    """Re-generate graph when parameters change"""
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    only_pairs = combine_splash == "Only Pairs"
    splash = combine_splash != "Separate Splash"

    data = []
    step = timedelta(days=2) if step == "2 days" else timedelta(weeks=1)
    while start_date + step < end_date:
        step_data = storage.get_color_ratings(
            expansion, event_type, start_date, start_date + step, splash
        ).with_columns(lit(start_date + step).alias("step"))
        if step_data.schema["wins"] != Boolean:
            data.append(step_data)
        start_date += step
    data = concat(data)
    if only_pairs:
        data = data.filter(col("color_name").is_in(color_pairs_full))
    data = data.with_columns((col("wins") / col("games")).alias("winrate"))
    if data.is_empty():
        return "Not enough data"
    min_y = data["winrate"].min() - 0.01
    max_y = data["winrate"].max() + 0.01
    data = data.to_pandas()

    fig = px.line(
        data,
        x="step",
        y="winrate",
        color="color_name",
        height=800,
        color_discrete_map=color_pairs_color_map,
        line_shape="spline",
        range_y=(min_y, max_y),
    )
    fig.update_layout(
        plot_bgcolor="#262321",
        yaxis={"gridcolor": "#5A5652"},
        xaxis={"gridcolor": "#5A5652"},
    )
    return dcc.Graph(figure=fig)


@app.callback(
    Output("color-ratings-evolution-date-range-input", "start_date"),
    Output("color-ratings-evolution-date-range-input", "end_date"),
    Input("color-ratings-evolution-expansion-input", "value"),
    Input("color-ratings-evolution-event-type-input", "value"),
)
def date_range(expansion, event_type):
    """Change date range control values when selected format changes"""
    first_day = get_first_day(expansion, event_type)
    start_date, end_date = optimal_date_range(first_day)
    return (start_date, end_date)


@app.callback(
    Output("color-ratings-evolution-expansion-input", "options"),
    Output("color-ratings-evolution-event-type-input", "options"),
    Input("color-ratings-evolution-full-input", "value"),
)
def show_all(full):
    """Switch controls to and from full mode"""
    if full:
        filters = storage.get_filters()
        return (filters["expansions"], filters["formats"])
    return (default_expansions, default_event_types)

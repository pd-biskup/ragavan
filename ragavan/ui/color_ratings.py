"""Color ratings graph component"""
from datetime import datetime, timedelta

from dash import dcc, html
from dash.dependencies import Input, Output
from plotly import express as px
from polars import col, concat, lit

from ragavan.app import app
from ragavan.common import color_pairs_full, default_event_types, default_expansions
from ragavan.storage import storage


def layout():
    """Create component"""
    return html.Div(
        children=[
            html.Div(
                className="controls-container",
                children=[
                    dcc.DatePickerRange(
                        id="color-ratings-date-range-input",
                        start_date=storage.get_first_day(
                            default_expansions[0], default_event_types[0]
                        )
                        + timedelta(weeks=2),
                        end_date=datetime.now().date(),
                    ),
                    dcc.Dropdown(
                        id="color-ratings-expansion-input",
                        className="dropdown",
                        options=default_expansions,
                        value=default_expansions[0],
                        searchable=False,
                        clearable=False,
                    ),
                    dcc.Checklist(
                        id="color-ratings-event-type-input",
                        options=default_event_types,
                        value=default_event_types[:1],
                        inline=True,
                    ),
                    dcc.Dropdown(
                        id="color-ratings-combine-splash-input",
                        className="dropdown",
                        options=["Only Pairs", "Combine Splash", "Separate Splash"],
                        value="Only Pairs",
                        searchable=False,
                        clearable=False,
                    ),
                    dcc.Checklist(
                        id="color-ratings-full-input",
                        options=["Show all"],
                        value=[],
                        inline=True,
                    ),
                ],
            ),
            html.Div(id="color-ratings-graph"),
        ]
    )


@app.callback(
    Output("color-ratings-graph", "children"),
    Input("color-ratings-expansion-input", "value"),
    Input("color-ratings-event-type-input", "value"),
    Input("color-ratings-date-range-input", "start_date"),
    Input("color-ratings-date-range-input", "end_date"),
    Input("color-ratings-combine-splash-input", "value"),
)
def color_ratings_graph(expansion, event_type, start_date, end_date, combine_splash):
    """Re-generate graph when parameters change"""
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    only_pairs = combine_splash == "Only Pairs"
    splash = combine_splash != "Separate Splash"
    data = [
        storage.get_color_ratings(
            expansion, event, start_date, end_date, splash
        ).with_columns(lit(event).alias("event_type"))
        for event in event_type
    ]
    data = concat(data)
    if only_pairs:
        data = data.filter(col("color_name").is_in(color_pairs_full))
    data = data.with_columns((col("wins") / col("games")).alias("winrate"))
    min_y = data["winrate"].min() - 0.01
    max_y = data["winrate"].max() + 0.01
    data = data.to_pandas()
    fig = px.bar(
        data,
        x="color_name",
        y="winrate",
        color="event_type",
        barmode="group",
        height=800,
        range_y=(min_y, max_y),
    )
    return dcc.Graph(figure=fig)


@app.callback(
    Output("color-ratings-date-range-input", "start_date"),
    Output("color-ratings-date-range-input", "end_date"),
    Input("color-ratings-expansion-input", "value"),
    Input("color-ratings-event-type-input", "value"),
)
def date_range(expansion, event_type):
    """Change date range control values when selected format changes"""
    start_date = storage.get_first_day(expansion, event_type) + timedelta(weeks=2)
    end_date = datetime.now().date()
    return (start_date, end_date)


@app.callback(
    Output("color-ratings-expansion-input", "options"),
    Output("color-ratings-event-type-input", "options"),
    Input("color-ratings-full-input", "value"),
)
def show_all(full):
    """Switch controls to and from full mode"""
    if full:
        filters = storage.get_filters()
        return (filters["expansions"], filters["formats"])
    return (default_expansions, default_event_types)

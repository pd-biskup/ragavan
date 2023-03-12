from datetime import datetime, timedelta

from dash import dcc, html
from dash.dependencies import Input, Output
from plotly import express as px
from polars import col

from ragavan.app import app
from ragavan.common import default_event_types, default_expansions
from ragavan.storage import storage


def layout():
    filters = storage.get_filters()
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
                        options=default_expansions,
                        value=default_expansions[0],
                        searchable=False,
                    ),
                    dcc.Checklist(
                        id="color-ratings-event-type-input",
                        options=default_event_types,
                        value=default_event_types[:1],
                        inline=True,
                    ),
                    dcc.Checklist(
                        id="color-ratings-combine-splash-input",
                        options=["Combine Splash"],
                        value=["Combine Splash"],
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
    if (
        expansion is None
        or event_type is None
        or start_date is None
        or end_date is None
    ):
        return ""
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        data = storage.get_color_ratings(
            expansion, event_type, start_date, end_date, combine_splash
        )
        data = data.with_columns((col("wins") / col("games")).alias("winrate"))
        min_y = data["winrate"].min() - 0.01
        max_y = data["winrate"].max() + 0.01
        data = data.to_pandas()
        fig = px.bar(data, x="color_name", y="winrate", range_y=(min_y, max_y))
        return dcc.Graph(figure=fig)

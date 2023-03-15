"""Module containing main app object"""
from dash import Dash

app = Dash(
    __name__,
    title="Ragavan",
    suppress_callback_exceptions=True,
)

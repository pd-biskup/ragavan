"""Various testing graphs and displays may be provided by this component"""
from dash import html, page_registry


def layout():
    """Create component"""
    return html.Div(children=[str(page) for page in page_registry.values()])

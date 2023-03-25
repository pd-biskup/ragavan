from dash import register_page

from ragavan.ui import color_ratings

register_page(__name__)

layout = color_ratings.layout

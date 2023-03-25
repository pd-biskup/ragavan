from dash import register_page

from ragavan.ui import card_ratings

register_page(__name__)

layout = card_ratings.layout

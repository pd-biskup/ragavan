"""17lands data fetching"""
import logging
from datetime import date
from typing import Optional

import polars as pl
import requests

from ragavan.common import format_date

log = logging.getLogger("17lands")
URL_BASE = "https://www.17lands.com"
URL_FILTERS = f"{URL_BASE}/data/filters"
URL_COLOR_RATINGS = f"{URL_BASE}/color_ratings/data"
URL_CARD_RATINGS = f"{URL_BASE}/card_ratings/data"
URL_CARD_EVALUATION_METAGAME = f"{URL_BASE}/card_evaluation_metagame/data"
URL_PLAY_DRAW = f"{URL_BASE}/data/play_draw"


def _fetch(url: str, params: dict = None) -> dict:
    log.info("fetching %s from %s", params, url)
    resp = requests.get(url, params=params, timeout=(5, 15))
    return resp.json()


def download_filters() -> dict:
    """Download and return 17lands filters"""
    data = _fetch(URL_FILTERS)
    return data


def download_color_ratings(
    expansion: str,
    event_type: str,
    start_date: date,
    end_date: date,
    combine_splash: bool,
) -> pl.DataFrame:
    """Download 17lands color ratings data, convert to polars DataFrame and return it"""
    params = {
        "expansion": expansion,
        "event_type": event_type,
        "start_date": format_date(start_date),
        "end_date": format_date(end_date),
        "combine_splash": "true" if combine_splash else "false",
    }
    data = _fetch(URL_COLOR_RATINGS, params=params)
    data = pl.DataFrame(data)
    return data


def download_card_ratings(
    expansion: str,
    event_type: str,
    start_date: date,
    end_date: date,
    colors: Optional[str] = None,
) -> pl.DataFrame:
    """Download 17lands card ratings data, convert to polars DataFrame and return it"""
    params = {
        "expansion": expansion,
        "format": event_type,
        "start_date": format_date(start_date),
        "end_date": format_date(end_date),
    }
    if colors:
        params["colors"] = colors
    data = _fetch(URL_CARD_RATINGS, params=params)
    data = pl.DataFrame(data)
    return data


# def download_card_evaluation_metagame(
#     expansion: str, event_type: str, start_date: date, end_date: date
# ) -> pl.DataFrame:
#     params = {
#         "expansion": expansion,
#         "format": event_type,
#         "start_date": format_date(start_date),
#         "end_date": format_date(end_date),
#     }
#     resp = requests.get(url_card_evaluation_metagame, params=params)
#     data = resp.json()
#     df = pl.DataFrame(data)
#     return df


def download_play_draw() -> pl.DataFrame:
    """Download 17lands play/draw advantage data, convert to polars DataFrame and return it"""
    data = _fetch(URL_PLAY_DRAW)
    data = pl.DataFrame(data)
    return data

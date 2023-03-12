import pickle
from datetime import date, timedelta
from logging import getLogger
from typing import Any, Optional

import polars as pl
from platformdirs import user_cache_path

from ragavan.common import beginning_date, format_date
from ragavan.seventeen_lands import (
    download_card_ratings,
    download_color_ratings,
    download_filters,
    download_play_draw,
)

log = getLogger("storage")


class StorageCell:
    def __init__(self, data: Any, lifetime: timedelta = timedelta(days=1)) -> None:
        self.data = data
        self.timestamp = date.today()
        self.lifetime = lifetime

    def valid(self) -> date:
        return date.today() - self.timestamp > self.lifetime


class Storage:
    path = user_cache_path("ragavan", "AcidBishop") / "storage"

    def __init__(self) -> None:
        self._filters = None
        self._play_draw = None
        self._color_ratings = {}
        self._card_ratings = {}
        self._card_evaluation_metagame = {}
        self._first_day = {}

    def save(self) -> None:
        log.info("Persisting storage")
        self.path.parent.mkdir(exist_ok=True)
        with open(self.path, "bw") as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls) -> "Storage":
        log.info("Loading storage")
        with open(cls.path, "br") as file:
            return pickle.load(file)

    def purge(self) -> None:
        if self._filters and self._filters.valid():
            self._filters = None
        if self._play_draw and self._play_draw.valid():
            self._play_draw = None
        for key in list(self._color_ratings.keys()):
            if self._color_ratings[key].valid():
                del self._color_ratings[key]
        for key in list(self._card_ratings.keys()):
            if self._card_ratings[key].valid():
                del self._card_ratings[key]
        for key in list(self._card_evaluation_metagame.keys()):
            if self._card_evaluation_metagame[key].valid():
                del self._card_evaluation_metagame[key]
        for key in list(self._first_day.keys()):
            if self._first_day[key].valid():
                del self._first_day[key]

    def get_filters(self) -> dict:
        self.purge()
        log.info("retrieving filters")
        if not self._filters:
            self._filters = StorageCell(download_filters())
            self.save()
        return self._filters.data

    def get_color_ratings(
        self,
        expansion: str,
        event_type: str,
        start_date: date,
        end_date: date,
        combine_splash: bool = False,
    ) -> pl.DataFrame:
        self.purge()
        log.info("retrieving color ratings")
        key = f"{expansion}-{event_type}-{format_date(start_date)}-{format_date(end_date)}-{combine_splash}"
        if key not in self._color_ratings:
            self._color_ratings[key] = StorageCell(
                download_color_ratings(
                    expansion, event_type, start_date, end_date, combine_splash
                )
            )
            self.save()
        return self._color_ratings[key].data

    def get_card_ratings(
        self,
        expansion: str,
        event_type: str,
        start_date: date,
        end_date: date,
        colors: Optional[str] = None,
    ) -> pl.DataFrame:
        self.purge()
        log.info("retrieving card ratings")
        key = f"{expansion}-{event_type}-{format_date(start_date)}-{format_date(end_date)}-{colors}"
        if key not in self._card_ratings:
            self._card_ratings[key] = StorageCell(
                download_card_ratings(
                    expansion, event_type, start_date, end_date, colors
                )
            )
            self.save()
        return self._card_ratings[key].data

    # def get_card_evaluation_metagame(
    #     self, expansion: str, event_type: str, start_date: date, end_date: date
    # ) -> pl.DataFrame:
    #     self.purge()
    #     key = f"{expansion}-{event_type}-{format_date(start_date)}-{format_date(end_date)}"
    #     if key not in self._card_evaluation_metagame:
    #         self._card_evaluation_metagame[key] = StorageCell(
    #             download_card_evaluation_metagame(
    #                 expansion, event_type, start_date, end_date
    #             )
    #         )
    #         self.save()
    #     return self._card_evaluation_metagame[key].data

    def get_play_draw(self) -> pl.DataFrame:
        self.purge()
        log.info("retrieving play draw advantage")
        if not self._play_draw:
            self._play_draw = StorageCell(download_play_draw())
            self.save()
        return self._play_draw.data

    def _find_first_day(self, expansion: str, event_type: str) -> Optional[date]:
        start_date = beginning_date
        end_date = start_date.replace(year=start_date.year + 1)
        ratings = storage.get_color_ratings(expansion, event_type, start_date, end_date)
        while not ratings.filter(pl.col("color_name") == "All Decks")["games"][0]:
            if end_date > date.today():
                return None
            start_date = end_date
            end_date = start_date.replace(year=start_date.year + 1)
            ratings = storage.get_color_ratings(
                expansion, event_type, start_date, end_date
            )

        end_date = start_date.replace(month=start_date.month + 1)
        ratings = storage.get_color_ratings(expansion, event_type, start_date, end_date)
        while not ratings.filter(pl.col("color_name") == "All Decks")["games"][0]:
            start_date = end_date
            end_date = start_date.replace(month=start_date.month + 1)
            ratings = storage.get_color_ratings(
                expansion, event_type, start_date, end_date
            )

        end_date = start_date.replace(day=start_date.day + 1)
        ratings = storage.get_color_ratings(expansion, event_type, start_date, end_date)
        while not ratings.filter(pl.col("color_name") == "All Decks")["games"][0]:
            start_date = end_date
            end_date = start_date.replace(day=start_date.day + 1)
            ratings = storage.get_color_ratings(
                expansion, event_type, start_date, end_date
            )
        return end_date

    def get_first_day(self, expansion: str, event_type: str) -> Optional[date]:
        self.purge()
        log.info("retriving first day")
        key = f"{expansion}-{event_type}"
        if key not in self._first_day:
            first_day = self._find_first_day(expansion, event_type)
            lifetime = timedelta(days=999) if first_day else timedelta(days=1)
            self._first_day[key] = StorageCell(first_day, lifetime)
            self.save()
        return self._first_day[key].data


try:
    storage = Storage.load()
except:
    storage = Storage()

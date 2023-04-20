"""Module with hard-coded first days of formats"""
import logging
from datetime import date
from typing import Dict, Tuple

from ragavan.common import default_event_types, default_expansions
from ragavan.storage import storage

log = logging.getLogger("first_day")

_first_days = {
    ("MOM", "PremierDraft"): date(2023, 4, 13),
    ("MOM", "QuickDraft"): date(2023, 4, 14),
    ("MOM", "TradDraft"): date(2023, 4, 18),
    ("MOM", "Sealed"): date(2023, 4, 14),
    ("MOM", "TradSealed"): date(2023, 4, 18),
    ("ONE", "PremierDraft"): date(2023, 2, 2),
    ("ONE", "QuickDraft"): date(2023, 2, 3),
    ("ONE", "TradDraft"): date(2023, 2, 7),
    ("ONE", "Sealed"): date(2023, 2, 3),
    ("ONE", "TradSealed"): date(2023, 2, 7),
    ("BRO", "PremierDraft"): date(2022, 11, 15),
    ("BRO", "QuickDraft"): date(2022, 11, 25),
    ("BRO", "TradDraft"): date(2022, 11, 15),
    ("BRO", "Sealed"): date(2022, 11, 15),
    ("BRO", "TradSealed"): date(2022, 11, 16),
    ("DMU", "PremierDraft"): date(2022, 8, 31),
    ("DMU", "QuickDraft"): date(2022, 9, 16),
    ("DMU", "TradDraft"): date(2022, 9, 1),
    ("DMU", "Sealed"): date(2022, 9, 1),
    ("DMU", "TradSealed"): date(2022, 9, 1),
    ("SNC", "PremierDraft"): date(2022, 4, 28),
    ("SNC", "QuickDraft"): date(2022, 5, 13),
    ("SNC", "TradDraft"): date(2022, 4, 28),
    ("SNC", "Sealed"): date(2022, 4, 28),
    ("SNC", "TradSealed"): date(2022, 4, 28),
    ("NEO", "PremierDraft"): date(2022, 2, 10),
    ("NEO", "QuickDraft"): date(2022, 2, 25),
    ("NEO", "TradDraft"): date(2022, 2, 10),
    ("NEO", "Sealed"): date(2022, 2, 10),
    ("NEO", "TradSealed"): date(2022, 2, 10),
    ("VOW", "PremierDraft"): date(2021, 11, 11),
    ("VOW", "QuickDraft"): date(2021, 11, 26),
    ("VOW", "TradDraft"): date(2021, 11, 11),
    ("VOW", "Sealed"): date(2021, 11, 11),
    ("VOW", "TradSealed"): date(2021, 11, 11),
    ("MID", "PremierDraft"): date(2021, 9, 16),
    ("MID", "QuickDraft"): date(2021, 10, 1),
    ("MID", "TradDraft"): date(2021, 9, 16),
    ("MID", "Sealed"): date(2021, 9, 16),
    ("MID", "TradSealed"): date(2021, 9, 16),
}


def _all_first_days() -> Dict[Tuple[str, str], date]:
    filters = storage.get_filters()
    first_days = {}
    for expansion in filters["expansions"]:
        for event_type in filters["formats"]:
            first_days[expansion, event_type] = storage.get_first_day(
                expansion, event_type
            )
    return first_days


def _selected_first_days() -> Dict[Tuple[str, str], date]:
    first_days = {}
    for expansion in default_expansions:
        for event_type in default_event_types:
            first_days[expansion, event_type] = storage.get_first_day(
                expansion, event_type
            )
    return first_days


def _generate_first_days(first_days: Dict[Tuple[str, str], date]) -> str:
    entries = []
    for (expansion, event_type), day in first_days.items():
        if day:
            entries.append(
                f'("{expansion}","{event_type}":date({day.year},{day.month},{day.day})'
            )
    return f"{{{','.join(entries)}}}"


def _print_generated():
    print(_generate_first_days(_all_first_days()))


def get_first_day(expansion: str, event_type: str) -> date | None:
    """Get hard-coded first day of format"""
    if (expansion, event_type) in _first_days:
        log.info("Using hard-coded first day for (%s, %s)", expansion, event_type)
        return _first_days[(expansion, event_type)]
    return storage.get_first_day(expansion, event_type)

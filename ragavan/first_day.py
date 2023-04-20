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
    ("SIR", "PremierDraft"): date(2023, 3, 21),
    ("SIR", "TradDraft"): date(2023, 3, 21),
    ("SIR", "Sealed"): date(2023, 3, 21),
    ("SIR", "TradSealed"): date(2023, 3, 21),
    ("SIR", "MidWeekSealed"): date(2023, 3, 28),
    ("SIR", "OpenSealed_D1_Bo1"): date(2023, 4, 1),
    ("SIR", "OpenSealed_D1_Bo3"): date(2023, 4, 1),
    ("Y23ONE", "PremierDraft"): date(2023, 2, 28),
    ("ONE", "MidWeekSealed"): date(2023, 2, 14),
    ("ONE", "OpenSealed_D1_Bo1"): date(2023, 3, 4),
    ("ONE", "OpenSealed_D1_Bo3"): date(2023, 3, 4),
    ("ONE", "OpenDraft_D2_Draft1_Bo3"): date(2023, 3, 5),
    ("ONE", "OpenDraft_D2_Draft2_Bo3"): date(2023, 3, 5),
    ("ONE", "OpenDraft_D2_Draft2B_Bo3"): date(2023, 3, 5),
    ("ONE", "QualifierPlayInSealed"): date(2023, 2, 18),
    ("ONE", "QualifierPlayInTradSealed"): date(2023, 2, 24),
    ("ONE", "Qualifier_D1_Sealed"): date(2023, 2, 25),
    ("Y23BRO", "PremierDraft"): date(2022, 12, 14),
    ("BRO", "OpenSealed_D1_Bo1"): date(2022, 11, 26),
    ("BRO", "OpenSealed_D1_Bo3"): date(2022, 11, 26),
    ("BRO", "OpenDraft_D2_Draft1_Bo3"): date(2022, 11, 27),
    ("BRO", "DecathlonTradDraft"): date(2023, 1, 7),
    ("BRO", "QualifierPlayInSealed"): date(2022, 12, 3),
    ("BRO", "QualifierPlayInTradSealed"): date(2022, 12, 9),
    ("BRO", "Qualifier_D1_Sealed"): date(2022, 12, 10),
    ("Y23DMU", "PremierDraft"): date(2022, 10, 6),
    ("DMU", "OpenSealed_D1_Bo1"): date(2022, 10, 1),
    ("DMU", "OpenSealed_D1_Bo3"): date(2022, 10, 1),
    ("DMU", "OpenDraft_D2_Draft1_Bo3"): date(2022, 10, 2),
    ("DMU", "OpenDraft_D2_Draft2_Bo3"): date(2022, 10, 2),
    ("DMU", "QualifierPlayInSealed"): date(2022, 9, 10),
    ("DMU", "QualifierPlayInTradSealed"): date(2022, 9, 16),
    ("DMU", "Qualifier_D1_Sealed"): date(2022, 9, 17),
    ("HBG", "PremierDraft"): date(2022, 7, 7),
    ("HBG", "TradDraft"): date(2022, 7, 7),
    ("HBG", "QuickDraft"): date(2022, 7, 22),
    ("HBG", "Sealed"): date(2022, 7, 7),
    ("HBG", "TradSealed"): date(2022, 7, 7),
    ("HBG", "OpenSealed_D1_Bo1"): date(2022, 7, 30),
    ("HBG", "OpenSealed_D1_Bo3"): date(2022, 7, 30),
    ("HBG", "OpenDraft_D2_Draft1_Bo3"): date(2022, 7, 31),
    ("HBG", "OpenDraft_D2_Draft2_Bo3"): date(2022, 7, 31),
    ("HBG", "QualifierPlayInSealed"): date(2022, 7, 16),
    ("HBG", "Qualifier_D1_Sealed"): date(2022, 7, 23),
    ("HBG", "Qualifier_D2_Draft"): date(2022, 7, 24),
    ("Y22SNC", "PremierDraft"): date(2022, 6, 2),
    ("SNC", "OpenSealed_D1_Bo1"): date(2022, 5, 14),
    ("SNC", "OpenSealed_D1_Bo3"): date(2022, 5, 14),
    ("SNC", "OpenDraft_D2_Bo3"): date(2022, 5, 15),
    ("SNC", "QualifierPlayInSealed"): date(2022, 5, 22),
    ("SNC", "QualifierPlayInTradSealed"): date(2022, 5, 28),
    ("SNC", "Qualifier_D1_Sealed"): date(2022, 5, 28),
    ("SNC", "Qualifier_D2_Draft"): date(2022, 5, 29),
    ("NEO", "OpenSealed_D1_Bo1"): date(2022, 2, 26),
    ("NEO", "OpenSealed_D1_Bo3"): date(2022, 2, 26),
    ("NEO", "OpenDraft_D2_Bo3"): date(2022, 2, 27),
    ("NEO", "DecathlonQuickDraft"): date(2023, 1, 10),
    ("DBL", "PremierDraft"): date(2022, 1, 28),
    ("VOW", "OpenDraft_D1_Bo1"): date(2021, 12, 4),
    ("VOW", "OpenDraft_D1_Bo3"): date(2021, 12, 4),
    ("VOW", "OpenDraft_D2_Bo3"): date(2021, 12, 5),
    ("VOW", "EsportsQualifierDraft_D1"): date(2021, 12, 18),
    ("VOW", "EsportsQualifierDraft_D2"): date(2021, 12, 19),
    ("RAVM", "PremierDraft"): date(2021, 10, 29),
    ("RAVM", "Sealed"): date(2022, 4, 8),
    ("MID", "DraftChallenge"): date(2021, 10, 22),
    ("AFR", "PremierDraft"): date(2021, 7, 15),
    ("AFR", "TradDraft"): date(2021, 7, 15),
    ("AFR", "QuickDraft"): date(2021, 7, 23),
    ("AFR", "Sealed"): date(2021, 7, 15),
    ("AFR", "TradSealed"): date(2021, 7, 15),
    ("AFR", "DraftChallenge"): date(2021, 8, 7),
    ("STX", "PremierDraft"): date(2021, 4, 15),
    ("STX", "TradDraft"): date(2021, 4, 15),
    ("STX", "QuickDraft"): date(2021, 4, 30),
    ("STX", "Sealed"): date(2021, 4, 15),
    ("STX", "TradSealed"): date(2021, 4, 15),
    ("STX", "MidWeekQuickDraft"): date(2023, 3, 14),
    ("STX", "DraftChallenge"): date(2021, 5, 22),
    ("STX", "OpenSealed_D1_Bo1"): date(2021, 5, 8),
    ("STX", "OpenSealed_D1_Bo3"): date(2021, 5, 8),
    ("STX", "OpenSealed_D2_Bo3"): date(2021, 5, 9),
    ("CORE", "PremierDraft"): date(2021, 3, 26),
    ("KHM", "PremierDraft"): date(2021, 1, 27),
    ("KHM", "TradDraft"): date(2021, 1, 28),
    ("KHM", "QuickDraft"): date(2021, 2, 12),
    ("KHM", "Sealed"): date(2021, 1, 28),
    ("KHM", "TradSealed"): date(2021, 2, 12),
    ("KHM", "MidWeekQuickDraft"): date(2023, 1, 17),
    ("KHM", "OpenSealed_D1_Bo1"): date(2021, 2, 20),
    ("KHM", "OpenSealed_D1_Bo3"): date(2021, 2, 20),
    ("KHM", "OpenSealed_D2_Bo3"): date(2021, 2, 21),
    ("KHM", "OpenDraft_D2_Draft1_Bo3"): date(2023, 1, 22),
    ("KHM", "OpenDraft_D2_Draft2B_Bo3"): date(2023, 1, 22),
    ("KLR", "PremierDraft"): date(2020, 11, 12),
    ("KLR", "TradDraft"): date(2020, 11, 12),
    ("KLR", "Sealed"): date(2020, 11, 12),
    ("KLR", "DraftChallenge"): date(2020, 11, 28),
    ("ZNR", "PremierDraft"): date(2020, 9, 16),
    ("ZNR", "TradDraft"): date(2020, 9, 17),
    ("ZNR", "QuickDraft"): date(2020, 10, 2),
    ("ZNR", "Sealed"): date(2020, 9, 17),
    ("AKR", "PremierDraft"): date(2020, 8, 13),
    ("AKR", "Sealed"): date(2020, 8, 13),
    ("M21", "PremierDraft"): date(2020, 6, 24),
    ("M21", "TradDraft"): date(2020, 6, 25),
    ("M21", "QuickDraft"): date(2020, 7, 10),
    ("M21", "Sealed"): date(2020, 6, 25),
    ("IKO", "PremierDraft"): date(2020, 4, 19),
    ("IKO", "TradDraft"): date(2020, 4, 16),
    ("IKO", "QuickDraft"): date(2020, 5, 5),
    ("IKO", "Sealed"): date(2020, 4, 17),
    ("Cube", "PremierDraft"): date(2020, 12, 13),
    ("Cube", "TradDraft"): date(2020, 12, 13),
    ("Cube", "CubeDraft"): date(2020, 6, 12),
    ("Cube", "CubeSealed"): date(2020, 4, 5),
    ("Cube", "OpenDraft_D1_Bo1"): date(2022, 12, 17),
    ("Cube", "OpenDraft_D1_Bo3"): date(2022, 12, 17),
    ("Cube", "OpenDraft_D2_Draft1_Bo3"): date(2022, 12, 18),
    ("Cube", "OpenDraft_D2_Draft2B_Bo3"): date(2022, 12, 18),
    ("THB", "PremierDraft"): date(2020, 10, 30),
    ("THB", "QuickDraft"): date(2020, 2, 4),
    ("THB", "Sealed"): date(2020, 1, 16),
    ("THB", "CompDraft"): date(2020, 1, 20),
    ("ELD", "PremierDraft"): date(2020, 7, 24),
    ("ELD", "QuickDraft"): date(2019, 12, 23),
    ("ELD", "CompDraft"): date(2019, 12, 31),
    ("M20", "QuickDraft"): date(2019, 9, 9),
    ("WAR", "PremierDraft"): date(2021, 3, 12),
    ("WAR", "QuickDraft"): date(2019, 7, 18),
    ("M19", "QuickDraft"): date(2020, 3, 29),
    ("DOM", "PremierDraft"): date(2020, 7, 31),
    ("DOM", "QuickDraft"): date(2020, 1, 3),
    ("DOM", "Sealed"): date(2022, 10, 28),
    ("DOM", "TradSealed"): date(2022, 11, 5),
    ("DOM", "OpenSealed_D1_Bo1"): date(2022, 11, 5),
    ("DOM", "OpenSealed_D1_Bo3"): date(2022, 11, 5),
    ("DOM", "OpenSealed_D2_Sealed1_Bo3"): date(2022, 11, 6),
    ("DOM", "OpenSealed_D2_Sealed2_Bo3"): date(2022, 11, 6),
    ("RIX", "QuickDraft"): date(2020, 6, 12),
    ("GRN", "PremierDraft"): date(2021, 1, 1),
    ("GRN", "QuickDraft"): date(2019, 9, 10),
    ("RNA", "PremierDraft"): date(2021, 1, 8),
    ("RNA", "QuickDraft"): date(2020, 3, 14),
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


def _update_first_days(
    first_days: Dict[Tuple[str, str], date]
) -> Dict[Tuple[str, str], date]:
    filters = storage.get_filters()
    first_days = dict(_first_days)
    for expansion in filters["expansions"]:
        for event_type in filters["formats"]:
            if (expansion, event_type) not in first_days:
                first_days[expansion, event_type] = storage.get_first_day(
                    expansion, event_type
                )
    return first_days


def _generate_first_days(first_days: Dict[Tuple[str, str], date]) -> str:
    entries = []
    for (expansion, event_type), day in first_days.items():
        if day:
            entries.append(
                f'("{expansion}","{event_type}"):date({day.year},{day.month},{day.day})'
            )
    return f"{{{','.join(entries)}}}"


def _print_generated():
    print(_generate_first_days(_update_first_days(_first_days)))


def get_first_day(expansion: str, event_type: str) -> date | None:
    """Get hard-coded first day of format"""
    if (expansion, event_type) in _first_days:
        log.info("Using hard-coded first day for (%s, %s)", expansion, event_type)
        return _first_days[(expansion, event_type)]
    return storage.get_first_day(expansion, event_type)

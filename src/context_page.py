from datetime import date, datetime, time
from typing import Dict, List, Tuple

from ics.event import Event
from ics.icalendar import Calendar
from pytz import timezone

_TIMEZONE = timezone("Europe/Vienna")

_DATE_FORMAT = "%d.%m.%Y"
_ICS_DATE_FORMAT = "%Y-%m-%d"
_NEXT_DATE_ALT_TEXT = "Wird noch Angekündigt"
_START_HOUR = 13
_END_HOUR = 20
_ASSET_PATH = "assets"
_IMG_PATH = "img"
_EVENT_IMAGES = {
    date(year=2025, month=6, day=1): (1, 10),
    date(year=2025, month=7, day=2): (1, 12),
    date(year=2025, month=8, day=5): (1, 14),
}


def _index_to_image_path(event_date, index):
    return f"/{ _IMG_PATH }/{event_date.strftime('%Y_%m_%d')}/{index:02}.jpg"


def _range_to_image_paths(event_date, indices):
    return [_index_to_image_path(event_date, i) for i in indices]


def _get_event_image_paths() -> Tuple[Dict[str, List], str]:
    paths = {
        d: _range_to_image_paths(d, range(start_index, stop_index + 1))
        for d, (start_index, stop_index) in _EVENT_IMAGES.items()
    }
    last_event_image_paths = paths.get(max(paths.keys()))
    return {
        d.strftime(_DATE_FORMAT): p for d, p in paths.items()
    }, last_event_image_paths


def _get_ics(ics_date, start_hour, end_hour):
    return Calendar(
        events=[
            Event(
                name="Brettspielsonntag",
                begin=datetime.combine(ics_date, time(hour=start_hour), _TIMEZONE),
                end=datetime.combine(ics_date, time(hour=end_hour), _TIMEZONE),
                location="Münzgrabenstrasse 10, 8010 Graz",
                url="https://brettspielsonntag.at",
            )
        ]
    )


def _get_future_dates():
    today = datetime.now().date()

    future_dates = sorted(
        d
        for d in [
            date(year=2025, month=8, day=1),
            date(year=2025, month=9, day=1),
            date(year=2025, month=10, day=1),
            date(year=2025, month=11, day=1),
            date(year=2025, month=12, day=1),
        ]
        if d >= today
    )

    next_date = future_dates[0] if future_dates else None
    next_date_ics = (
        _get_ics(next_date, start_hour=_START_HOUR, end_hour=_END_HOUR)
        if next_date
        else None
    )

    return (
        [d.strftime(_DATE_FORMAT) for d in future_dates],
        next_date.strftime(_DATE_FORMAT),
        next_date_ics,
    )


def _get_asset_path(asset):
    return f"/{ _ASSET_PATH }/{ asset }"


def _create_context():

    future_dates, next_date, next_date_ics = _get_future_dates()
    event_image_paths, last_event_image_paths = _get_event_image_paths()

    return {
        "meta_description": "Zahlreiche Brettspiele kostenlos testen",
        "meta_keywords": "Brettspiele,Graz,Münzgrabengasse 10",
        "logo_path": _get_asset_path("logo.png"),
        "future_dates": future_dates,
        "next_date": next_date,
        "time_range": f"{ _START_HOUR }:00-{ _END_HOUR }:00",
        "next_date_ics": next_date_ics.serialize(),
        "next_date_alt_text": _NEXT_DATE_ALT_TEXT,
        "event_image_paths": event_image_paths,
        "last_event_image_paths": last_event_image_paths,
    }


CONTEXT_PAGE = _create_context()

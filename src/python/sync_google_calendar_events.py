import argparse
import datetime as dt
import json
import os
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo

from ruamel.yaml import YAML

DEFAULT_CALENDAR_ID = "mcgillcsdc@gmail.com"
DEFAULT_TIMEZONE = "America/Toronto"
DEFAULT_CTA_TEXT = "View all seminars"
DEFAULT_CTA_URL = "/calendar/"
DEFAULT_BANNER_LABEL = "Featured Seminar"


def _format_date_display(start_dt: dt.datetime, all_day: bool, tz_name: str) -> str:
    local_dt = start_dt.astimezone(ZoneInfo(tz_name))
    day_name = local_dt.strftime("%A")
    month_name = local_dt.strftime("%B")
    day = str(local_dt.day)

    if all_day:
        return f"{day_name}, {month_name} {day} (All day)"

    hour_24 = local_dt.hour
    hour_12 = hour_24 % 12
    if hour_12 == 0:
        hour_12 = 12
    minute = local_dt.minute
    am_pm = "AM" if hour_24 < 12 else "PM"
    return f"{day_name}, {month_name} {day}, {hour_12}:{minute:02d} {am_pm} ET"


def _parse_start(event: Dict[str, Any], default_tz: str) -> Dict[str, Any]:
    start = event.get("start", {})

    if "dateTime" in start:
        raw = start["dateTime"].replace("Z", "+00:00")
        value = dt.datetime.fromisoformat(raw)
        if value.tzinfo is None:
            tz = start.get("timeZone", default_tz)
            value = value.replace(tzinfo=ZoneInfo(tz))
        return {"datetime": value, "all_day": False}

    if "date" in start:
        date_value = dt.date.fromisoformat(start["date"])
        value = dt.datetime.combine(date_value, dt.time.min, tzinfo=ZoneInfo(default_tz))
        return {"datetime": value, "all_day": True}

    raise ValueError("Event missing start.dateTime or start.date")


def _extract_blurb(description: str) -> str:
    for line in description.splitlines():
        cleaned = line.strip()
        if cleaned:
            if cleaned.lower().startswith("blurb:"):
                return cleaned.split(":", 1)[1].strip()
            return cleaned
    return ""


def _fetch_events(calendar_id: str, api_key: str, timezone_name: str, max_results: int) -> List[Dict[str, Any]]:
    now_utc = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    params = {
        "singleEvents": "true",
        "orderBy": "startTime",
        "timeMin": now_utc,
        "maxResults": str(max_results),
        "key": api_key,
    }

    encoded_calendar = urllib.parse.quote(calendar_id, safe="")
    url = (
        f"https://www.googleapis.com/calendar/v3/calendars/{encoded_calendar}/events?"
        + urllib.parse.urlencode(params)
    )

    payload = None
    attempts = 3

    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(url, timeout=20) as response:
                payload = json.loads(response.read().decode("utf-8"))
            break
        except Exception as exc:
            if attempt == attempts:
                raise RuntimeError(
                    f"Failed to fetch Google Calendar events after {attempts} attempts: {exc}"
                ) from exc
            time.sleep(attempt * 2)

    if payload is None:
        raise RuntimeError("Google Calendar payload is empty.")

    items = payload.get("items", [])
    events = []

    for event in items:
        try:
            start_info = _parse_start(event, timezone_name)
        except Exception:
            continue

        description = event.get("description", "")
        summary = event.get("summary", "Untitled event")

        events.append(
            {
                "title": summary,
                "start": start_info["datetime"],
                "all_day": start_info["all_day"],
                "location": event.get("location", "TBD"),
                "html_link": event.get("htmlLink", ""),
                "blurb": _extract_blurb(description),
            }
        )

    events.sort(key=lambda e: e["start"])
    return events


def _build_payload(events: List[Dict[str, Any]], calendar_id: str, timezone_name: str) -> Dict[str, Any]:
    generated_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()

    if events:
        featured = events[0]
        featured_event = {
            "banner_label": DEFAULT_BANNER_LABEL,
            "title": featured["title"],
            "date_display": _format_date_display(featured["start"], featured["all_day"], timezone_name),
            "location": featured["location"],
            "blurb": featured["blurb"],
            "cta_text": DEFAULT_CTA_TEXT,
            "cta_url": DEFAULT_CTA_URL,
            "event_url": featured["html_link"],
        }
    else:
        featured_event = {
            "banner_label": DEFAULT_BANNER_LABEL,
            "title": "No upcoming seminar scheduled.",
            "date_display": "Check back soon",
            "location": "TBD",
            "blurb": "",
            "cta_text": DEFAULT_CTA_TEXT,
            "cta_url": DEFAULT_CTA_URL,
            "event_url": "",
        }

    upcoming_events = []
    for event in events[:5]:
        upcoming_events.append(
            {
                "title": event["title"],
                "date_display": _format_date_display(event["start"], event["all_day"], timezone_name),
                "location": event["location"],
                "event_url": event["html_link"],
            }
        )

    return {
        "generated_at": generated_at,
        "source": {
            "provider": "google_calendar",
            "calendar_id": calendar_id,
            "timezone": timezone_name,
        },
        "featured_event": featured_event,
        "upcoming_events": upcoming_events,
    }


def _write_yaml_atomic(data: Dict[str, Any], output_path: Path) -> None:
    yaml = YAML()
    yaml.preserve_quotes = True
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=str(output_path.parent)) as tmp:
        yaml.dump(data, tmp)
        tmp_path = Path(tmp.name)

    tmp_path.replace(output_path)


def main(
    output_path: str = "_data/events.yml",
    calendar_id: Optional[str] = None,
    timezone_name: str = DEFAULT_TIMEZONE,
    max_results: int = 20,
) -> None:
    resolved_calendar_id = calendar_id or os.getenv("GOOGLE_CALENDAR_ID", DEFAULT_CALENDAR_ID)
    api_key = os.getenv("GOOGLE_CALENDAR_API_KEY")

    if not api_key:
        raise EnvironmentError("GOOGLE_CALENDAR_API_KEY is required.")

    events = _fetch_events(
        calendar_id=resolved_calendar_id,
        api_key=api_key,
        timezone_name=timezone_name,
        max_results=max_results,
    )
    payload = _build_payload(events, resolved_calendar_id, timezone_name)
    _write_yaml_atomic(payload, Path(output_path))

    print(
        f"Synced {len(events)} events from Google Calendar "
        f"'{resolved_calendar_id}' into {output_path}."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync Google Calendar events into Jekyll data files.")
    parser.add_argument("--output-path", default="_data/events.yml")
    parser.add_argument("--calendar-id", default=None)
    parser.add_argument("--timezone", default=DEFAULT_TIMEZONE)
    parser.add_argument("--max-results", type=int, default=20)
    args = parser.parse_args()

    main(
        output_path=args.output_path,
        calendar_id=args.calendar_id,
        timezone_name=args.timezone,
        max_results=args.max_results,
    )

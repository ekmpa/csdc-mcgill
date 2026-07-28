import argparse
import datetime as dt
import json
import os
import re
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
DEFAULT_CTA_URL = "/news/"
DEFAULT_BANNER_LABEL = "Featured Seminar"
DEFAULT_MAX_RESULTS = 20


def _format_date_display(start_dt: dt.datetime, all_day: bool, tz_name: str) -> str:
    local_dt = start_dt.astimezone(ZoneInfo(tz_name))
    day_name = local_dt.strftime("%A")
    month_name = local_dt.strftime("%B")
    day = str(local_dt.day)

    if all_day:
        return f"{day_name}, {month_name} {day} (All day)"

    hour_12 = int(local_dt.strftime("%I"))
    minute = local_dt.minute
    am_pm = "AM" if local_dt.hour < 12 else "PM"
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


def _unfold_ics_lines(ics_text: str) -> List[str]:
    raw_lines = ics_text.splitlines()
    lines: List[str] = []
    for raw in raw_lines:
        if raw.startswith((" ", "\t")) and lines:
            lines[-1] = lines[-1] + raw[1:]
        else:
            lines.append(raw)
    return lines


def _parse_property(line: str) -> tuple[str, Dict[str, str], str]:
    if ":" not in line:
        return line, {}, ""

    left, value = line.split(":", 1)
    parts = left.split(";")
    name = parts[0].upper()
    params: Dict[str, str] = {}
    for part in parts[1:]:
        if "=" in part:
            key, val = part.split("=", 1)
            params[key.upper()] = val
    return name, params, value


def _decode_ics_text(value: str) -> str:
    text = value.replace("\\n", "\n").replace("\\,", ",").replace("\\;", ";").replace("\\\\", "\\")
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def _parse_ics_datetime(raw: str, params: Dict[str, str], fallback_tz: str) -> tuple[dt.datetime, bool]:
    value_type = params.get("VALUE", "").upper()
    if value_type == "DATE" or (len(raw) == 8 and raw.isdigit()):
        date_value = dt.datetime.strptime(raw[:8], "%Y%m%d").date()
        date_dt = dt.datetime.combine(date_value, dt.time.min, tzinfo=ZoneInfo(fallback_tz))
        return date_dt, True

    if raw.endswith("Z"):
        parsed = dt.datetime.strptime(raw, "%Y%m%dT%H%M%SZ").replace(tzinfo=dt.timezone.utc)
        return parsed, False

    tz_name = params.get("TZID", fallback_tz)
    for fmt in ("%Y%m%dT%H%M%S", "%Y%m%dT%H%M"):
        try:
            parsed = dt.datetime.strptime(raw, fmt)
            return parsed.replace(tzinfo=ZoneInfo(tz_name)), False
        except ValueError:
            continue

    raise ValueError(f"Unsupported ICS datetime format: {raw}")


def _parse_rrule(rrule_value: str) -> Dict[str, str]:
    parts = [part.strip() for part in rrule_value.split(";") if part.strip()]
    parsed: Dict[str, str] = {}
    for part in parts:
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        parsed[key.upper()] = value
    return parsed


def _weekly_occurrences(
    start_dt: dt.datetime,
    now_utc: dt.datetime,
    byday_codes: List[str],
    interval: int,
    until_dt: Optional[dt.datetime],
    max_count: int,
) -> List[dt.datetime]:
    local_tz = start_dt.tzinfo or dt.timezone.utc
    now_local = now_utc.astimezone(local_tz)
    start_local = start_dt.astimezone(local_tz)

    day_code_to_weekday = {
        "MO": 0,
        "TU": 1,
        "WE": 2,
        "TH": 3,
        "FR": 4,
        "SA": 5,
        "SU": 6,
    }

    weekdays: List[int] = []
    for code in byday_codes:
        weekday = day_code_to_weekday.get(code.strip().upper())
        if weekday is not None:
            weekdays.append(weekday)

    if not weekdays:
        weekdays = [start_local.weekday()]

    start_date = start_local.date()
    candidate_date = max(start_date, now_local.date())
    horizon_date = candidate_date + dt.timedelta(days=366)

    matches: List[dt.datetime] = []

    while candidate_date <= horizon_date and len(matches) < max_count:
        days_since_start = (candidate_date - start_date).days
        if days_since_start >= 0:
            weeks_since_start = days_since_start // 7
            if weeks_since_start % max(interval, 1) == 0 and candidate_date.weekday() in weekdays:
                candidate_dt = dt.datetime.combine(
                    candidate_date,
                    start_local.timetz().replace(tzinfo=None),
                    tzinfo=local_tz,
                )

                if candidate_dt >= start_local and candidate_dt.astimezone(dt.timezone.utc) >= now_utc:
                    if until_dt is not None and candidate_dt.astimezone(dt.timezone.utc) > until_dt.astimezone(
                        dt.timezone.utc
                    ):
                        break
                    matches.append(candidate_dt)

        candidate_date += dt.timedelta(days=1)

    return matches


def _recurrence_occurrences(
    start_dt: dt.datetime,
    rrule_raw: str,
    now_utc: dt.datetime,
    max_count: int,
) -> List[dt.datetime]:
    rule = _parse_rrule(rrule_raw)
    freq = rule.get("FREQ", "").upper()
    interval = int(rule.get("INTERVAL", "1") or "1")

    until_dt: Optional[dt.datetime] = None
    until_raw = rule.get("UNTIL")
    if until_raw:
        until_dt, _ = _parse_ics_datetime(until_raw, {}, str(start_dt.tzinfo or dt.timezone.utc))

    if freq == "WEEKLY":
        byday = [part.strip() for part in rule.get("BYDAY", "").split(",") if part.strip()]
        return _weekly_occurrences(start_dt, now_utc, byday, interval, until_dt, max_count=max_count)

    if freq == "DAILY":
        step = max(interval, 1)
        candidate = start_dt
        matches: List[dt.datetime] = []
        if candidate < now_utc:
            delta_days = (now_utc.date() - candidate.date()).days
            jumps = max(delta_days // step, 0)
            candidate = candidate + dt.timedelta(days=jumps * step)
            while candidate < now_utc:
                candidate += dt.timedelta(days=step)

        for _ in range(max_count):
            if until_dt is not None and candidate.astimezone(dt.timezone.utc) > until_dt.astimezone(dt.timezone.utc):
                break
            matches.append(candidate)
            candidate += dt.timedelta(days=step)

        return matches

    return []


def _fetch_public_ics_events(calendar_id: str, timezone_name: str, max_results: int) -> List[Dict[str, Any]]:
    encoded_calendar = urllib.parse.quote(calendar_id, safe="")
    ics_url = f"https://calendar.google.com/calendar/ical/{encoded_calendar}/public/basic.ics"

    request = urllib.request.Request(
        ics_url,
        method="GET",
        headers={"User-Agent": "csdc-calendar-sync/1.0"},
    )
    with urllib.request.urlopen(request, timeout=25) as response:
        ics_text = response.read().decode("utf-8", errors="replace")

    now_utc = dt.datetime.now(dt.timezone.utc)
    lines = _unfold_ics_lines(ics_text)

    events: List[Dict[str, Any]] = []
    in_event = False
    current: Dict[str, Any] = {}

    for line in lines:
        upper = line.upper()
        if upper == "BEGIN:VEVENT":
            in_event = True
            current = {}
            continue
        if upper == "END:VEVENT":
            in_event = False
            start_dt = current.get("start")
            if isinstance(start_dt, dt.datetime):
                if start_dt >= now_utc:
                    events.append(current)
                else:
                    rrule_raw = str(current.get("rrule", "") or "")
                    if rrule_raw:
                        starts = _recurrence_occurrences(start_dt, rrule_raw, now_utc, max_count=max_results)
                        for recurrence_start in starts:
                            event_copy = dict(current)
                            event_copy["start"] = recurrence_start
                            events.append(event_copy)
            current = {}
            continue
        if not in_event:
            continue

        name, params, value = _parse_property(line)
        if name == "SUMMARY":
            current["title"] = _decode_ics_text(value) or "Untitled event"
        elif name == "DESCRIPTION":
            current["description"] = _decode_ics_text(value)
        elif name == "URL":
            current["event_url"] = value.strip()
        elif name == "RRULE":
            current["rrule"] = value.strip()
        elif name == "DTSTART":
            try:
                start_dt, all_day = _parse_ics_datetime(value.strip(), params, timezone_name)
                current["start"] = start_dt
                current["all_day"] = all_day
            except Exception:
                pass

    events.sort(key=lambda e: e.get("start", now_utc))

    parsed_events: List[Dict[str, Any]] = []
    for event in events[:max_results]:
        parsed_events.append(
            {
                "title": event.get("title", "Untitled event"),
                "start": event["start"],
                "all_day": bool(event.get("all_day", False)),
                "html_link": str(event.get("event_url", "") or ""),
                "blurb": _extract_blurb(str(event.get("description", "") or "")),
            }
        )

    return parsed_events


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
                "html_link": event.get("htmlLink", ""),
                "blurb": _extract_blurb(description),
            }
        )

    events.sort(key=lambda e: e["start"])
    return events


def _build_payload(
    events: List[Dict[str, Any]],
    calendar_id: str,
    timezone_name: str,
    source_provider: str = "google_calendar",
) -> Dict[str, Any]:
    generated_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()

    if events:
        featured = events[0]
        featured_event = {
            "banner_label": DEFAULT_BANNER_LABEL,
            "title": featured["title"],
            "date_display": _format_date_display(featured["start"], featured["all_day"], timezone_name),
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
                "event_url": event["html_link"],
            }
        )

    return {
        "generated_at": generated_at,
        "source": {
            "provider": source_provider,
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
    max_results: int = DEFAULT_MAX_RESULTS,
) -> None:
    resolved_calendar_id = calendar_id or os.getenv("GOOGLE_CALENDAR_ID", DEFAULT_CALENDAR_ID)
    api_key = os.getenv("GOOGLE_CALENDAR_API_KEY")

    source_provider = "google_calendar_public_ics"
    if api_key:
        try:
            events = _fetch_events(
                calendar_id=resolved_calendar_id,
                api_key=api_key,
                timezone_name=timezone_name,
                max_results=max_results,
            )
            source_provider = "google_calendar"
        except Exception as exc:
            print(f"Google Calendar API fetch failed ({exc}); falling back to public ICS feed.")
            events = _fetch_public_ics_events(
                calendar_id=resolved_calendar_id,
                timezone_name=timezone_name,
                max_results=max_results,
            )
    else:
        events = _fetch_public_ics_events(
            calendar_id=resolved_calendar_id,
            timezone_name=timezone_name,
            max_results=max_results,
        )

    payload = _build_payload(events, resolved_calendar_id, timezone_name, source_provider=source_provider)
    _write_yaml_atomic(payload, Path(output_path))

    print(
        f"Synced {len(events)} events from Google Calendar ({source_provider}) "
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

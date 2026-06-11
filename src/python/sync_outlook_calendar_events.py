import argparse
import datetime as dt
import os
import re
import tempfile
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

from ruamel.yaml import YAML

DEFAULT_TIMEZONE = "America/Toronto"
DEFAULT_CTA_TEXT = "View all seminars"
DEFAULT_CTA_URL = "/news/"
DEFAULT_BANNER_LABEL = "Featured Seminar"
DEFAULT_MAX_RESULTS = 20
DEFAULT_CALENDAR_HTML_URL = (
    "https://outlook.office365.com/owa/calendar/"
    "7fb5d6f8890f4776af6224301bea023b@mail.mcgill.ca/"
    "90fc976dc03e4fdcabbcdf8ce7795ea78987418656938045875/calendar.html"
)

WINDOWS_TZ_TO_IANA: Dict[str, str] = {
    "UTC": "UTC",
    "Etc/UTC": "UTC",
    "Eastern Standard Time": "America/Toronto",
    "US Eastern Standard Time": "America/Toronto",
}


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


def _map_timezone(tz_name: str, fallback_tz: str) -> str:
    if not tz_name:
        return fallback_tz
    mapped = WINDOWS_TZ_TO_IANA.get(tz_name, tz_name)
    try:
        ZoneInfo(mapped)
        return mapped
    except Exception:
        return fallback_tz


def _derive_ics_url(calendar_html_url: str) -> str:
    if calendar_html_url.endswith("calendar.html"):
        return calendar_html_url[: -len("calendar.html")] + "calendar.ics"
    if calendar_html_url.endswith(".html"):
        return calendar_html_url[: -len(".html")] + ".ics"
    if calendar_html_url.endswith(".ics"):
        return calendar_html_url
    return calendar_html_url.rstrip("/") + "/calendar.ics"


def _fetch_ics(calendar_ics_url: str) -> str:
    request = urllib.request.Request(
        calendar_ics_url,
        method="GET",
        headers={"User-Agent": "csdc-calendar-sync/1.0"},
    )
    with urllib.request.urlopen(request, timeout=25) as response:
        return response.read().decode("utf-8", errors="replace")


def _unfold_ics_lines(ics_text: str) -> List[str]:
    raw_lines = ics_text.splitlines()
    lines: List[str] = []
    for raw in raw_lines:
        if raw.startswith((" ", "\t")) and lines:
            lines[-1] = lines[-1] + raw[1:]
        else:
            lines.append(raw)
    return lines


def _parse_property(line: str) -> Tuple[str, Dict[str, str], str]:
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


def _parse_ics_datetime(raw: str, params: Dict[str, str], fallback_tz: str) -> Tuple[dt.datetime, bool]:
    value_type = params.get("VALUE", "").upper()
    if value_type == "DATE" or (len(raw) == 8 and raw.isdigit()):
        date_value = dt.datetime.strptime(raw[:8], "%Y%m%d").date()
        date_dt = dt.datetime.combine(date_value, dt.time.min, tzinfo=ZoneInfo(fallback_tz))
        return date_dt, True

    tzid = _map_timezone(params.get("TZID", ""), fallback_tz)

    if raw.endswith("Z"):
        parsed = dt.datetime.strptime(raw, "%Y%m%dT%H%M%SZ").replace(tzinfo=dt.timezone.utc)
        return parsed, False

    for fmt in ("%Y%m%dT%H%M%S", "%Y%m%dT%H%M"):
        try:
            parsed = dt.datetime.strptime(raw, fmt)
            return parsed.replace(tzinfo=ZoneInfo(tzid)), False
        except ValueError:
            continue

    raise ValueError(f"Unsupported ICS datetime format: {raw}")


def _extract_events_from_ics(ics_text: str, timezone_name: str, max_results: int) -> List[Dict[str, object]]:
    now = dt.datetime.now(dt.timezone.utc)
    lines = _unfold_ics_lines(ics_text)

    events: List[Dict[str, object]] = []
    in_event = False
    current: Dict[str, object] = {}

    for line in lines:
        upper = line.upper()
        if upper == "BEGIN:VEVENT":
            in_event = True
            current = {}
            continue
        if upper == "END:VEVENT":
            in_event = False
            start_dt = current.get("start")
            if isinstance(start_dt, dt.datetime) and start_dt >= now:
                events.append(current)
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
        elif name == "DTSTART":
            try:
                start_dt, all_day = _parse_ics_datetime(value.strip(), params, timezone_name)
                current["start"] = start_dt
                current["all_day"] = all_day
            except Exception:
                pass

    events.sort(key=lambda e: e.get("start", now))
    return events[:max_results]


def _extract_blurb(description: str) -> str:
    for line in description.splitlines():
        cleaned = line.strip()
        if cleaned:
            if cleaned.lower().startswith("blurb:"):
                return cleaned.split(":", 1)[1].strip()
            return cleaned
    return ""


def _build_payload(events: List[Dict[str, object]], source_url: str, timezone_name: str) -> Dict[str, object]:
    generated_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()

    if events:
        featured = events[0]
        featured_event = {
            "banner_label": DEFAULT_BANNER_LABEL,
            "title": str(featured.get("title", "Untitled event")),
            "date_display": _format_date_display(
                featured["start"],
                bool(featured.get("all_day", False)),
                timezone_name,
            ),
            "blurb": _extract_blurb(str(featured.get("description", ""))),
            "cta_text": DEFAULT_CTA_TEXT,
            "cta_url": DEFAULT_CTA_URL,
            "event_url": str(featured.get("event_url", "") or ""),
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
                "title": str(event.get("title", "Untitled event")),
                "date_display": _format_date_display(
                    event["start"],
                    bool(event.get("all_day", False)),
                    timezone_name,
                ),
                "event_url": str(event.get("event_url", "") or ""),
            }
        )

    return {
        "generated_at": generated_at,
        "source": {
            "provider": "outlook_published_calendar",
            "calendar_url": source_url,
            "timezone": timezone_name,
        },
        "featured_event": featured_event,
        "upcoming_events": upcoming_events,
    }


def _write_yaml_atomic(data: Dict[str, object], output_path: Path) -> None:
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=str(output_path.parent)) as tmp:
        yaml.dump(data, tmp)
        tmp_path = Path(tmp.name)

    tmp_path.replace(output_path)


def main(
    output_path: str = "_data/events.yml",
    timezone_name: str = DEFAULT_TIMEZONE,
    max_results: int = DEFAULT_MAX_RESULTS,
    calendar_html_url: Optional[str] = None,
) -> None:
    html_url = (calendar_html_url or os.getenv("OUTLOOK_CALENDAR_HTML_URL") or DEFAULT_CALENDAR_HTML_URL).strip()
    ics_url = os.getenv("OUTLOOK_CALENDAR_ICS_URL", "").strip() or _derive_ics_url(html_url)

    ics_text = _fetch_ics(ics_url)
    events = _extract_events_from_ics(ics_text, timezone_name=timezone_name, max_results=max_results)
    payload = _build_payload(events, source_url=html_url, timezone_name=timezone_name)
    _write_yaml_atomic(payload, Path(output_path))

    print(f"Synced {len(events)} events from published Outlook calendar into {output_path}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync published Outlook calendar events into Jekyll data files.")
    parser.add_argument("--output-path", default="_data/events.yml")
    parser.add_argument("--timezone", default=DEFAULT_TIMEZONE)
    parser.add_argument("--max-results", type=int, default=DEFAULT_MAX_RESULTS)
    parser.add_argument("--calendar-html-url", default=None)
    args = parser.parse_args()

    main(
        output_path=args.output_path,
        timezone_name=args.timezone,
        max_results=args.max_results,
        calendar_html_url=args.calendar_html_url,
    )
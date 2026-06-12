import datetime as dt
import os
import re
from textwrap import dedent

from . import parse_issue_body, write_content_to_file


def _is_empty(value: str) -> bool:
    if value is None:
        return True
    return str(value).strip() in ("", "_No response_", "None")


def _first_non_empty(parsed, *keys):
    for key in keys:
        value = parsed.get(key)
        if not _is_empty(value):
            return str(value).strip()
    return ""


def _normalize_summary(value: str) -> str:
    cleaned = str(value or "").strip()
    if cleaned.lower() == "x":
        return ""
    return cleaned


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "news-update"


def _build_filename(parsed):
    date_str = _first_non_empty(parsed, "date")
    dt.date.fromisoformat(date_str)
    slug = _slugify(_first_non_empty(parsed, "title"))
    return f"{date_str}-{slug}.md"


def _build_fr_filename(parsed):
    date_str = _first_non_empty(parsed, "date")
    dt.date.fromisoformat(date_str)
    fr_title = _first_non_empty(parsed, "title_fr", "title_french")
    base_title = fr_title if fr_title else _first_non_empty(parsed, "title")
    slug = _slugify(base_title)
    return f"{date_str}-{slug}.md"


def _yaml_quote(value: str) -> str:
    """Return a YAML-safe double-quoted scalar."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    escaped = escaped.replace("\n", " ").strip()
    return f'"{escaped}"'


def _build_content(parsed):
    title = _first_non_empty(parsed, "title")
    date_str = _first_non_empty(parsed, "date")
    summary = _normalize_summary(_first_non_empty(parsed, "summary"))
    title_fr = _first_non_empty(parsed, "title_fr", "title_french") or title
    summary_fr = _normalize_summary(_first_non_empty(parsed, "summary_fr", "summary_french")) or summary
    external_link = _first_non_empty(parsed, "external_link", "external_link_(optional)")

    front_matter = (
        "---\n"
        f"title: {_yaml_quote(title)}\n"
        f"title_fr: {_yaml_quote(title_fr)}\n"
        f"date: {date_str}\n"
        "categories: News\n"
        f"excerpt: {_yaml_quote(summary)}\n"
        f"excerpt_en: {_yaml_quote(summary)}\n"
        f"excerpt_fr: {_yaml_quote(summary_fr)}\n"
        "---"
    )

    body = summary
    if external_link:
        body += ("\n\n" if body else "") + f"[Read more]({external_link})"

    return front_matter + "\n" + body + "\n"


def _build_fr_content(parsed):
    title = _first_non_empty(parsed, "title")
    date_str = _first_non_empty(parsed, "date")
    summary = _normalize_summary(_first_non_empty(parsed, "summary"))
    title_fr = _first_non_empty(parsed, "title_fr", "title_french") or title
    summary_fr = _normalize_summary(_first_non_empty(parsed, "summary_fr", "summary_french")) or summary
    external_link = _first_non_empty(parsed, "external_link", "external_link_(optional)")

    front_matter = (
        "---\n"
        f"title: {_yaml_quote(title_fr)}\n"
        f"title_en: {_yaml_quote(title)}\n"
        f"date: {date_str}\n"
        "categories: [fr, news]\n"
        f"excerpt: {_yaml_quote(summary_fr)}\n"
        f"excerpt_fr: {_yaml_quote(summary_fr)}\n"
        f"excerpt_en: {_yaml_quote(summary)}\n"
        "---"
    )

    body = summary_fr
    if external_link:
        body += ("\n\n" if body else "") + f"[Lire plus]({external_link})"

    return front_matter + "\n" + body + "\n"


def main(parsed, save_dir="_posts/news"):
    formatted = {
        "filename": _build_filename(parsed),
        "content": _build_content(parsed),
    }
    write_content_to_file(formatted, save_dir)

    # Always create a French companion post; fallback to English text when FR fields are missing.
    formatted_fr = {
        "filename": _build_fr_filename(parsed),
        "content": _build_fr_content(parsed),
    }
    write_content_to_file(formatted_fr, os.path.join(save_dir, "fr"))

    return {"en": formatted, "fr": formatted_fr}


if __name__ == "__main__":
    issue_body = os.environ["ISSUE_BODY"]
    parsed = parse_issue_body(issue_body)
    main(parsed)

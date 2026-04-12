import datetime as dt
import os
import re
from textwrap import dedent

from . import parse_issue_body, write_content_to_file


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "news-update"


def _build_filename(parsed):
    date_str = parsed["date"]
    dt.date.fromisoformat(date_str)
    slug = _slugify(parsed["title"])
    return f"{date_str}-{slug}.md"


def _build_content(parsed):
    title = parsed["title"].strip()
    date_str = parsed["date"].strip()
    summary = parsed["summary"].strip()
    external_link = parsed.get("external_link", "").strip()

    front_matter = dedent(
        f"""---
        title: {title}
        date: {date_str}
        categories: News
        excerpt: {summary}
        ---
        """
    )

    body = summary
    if external_link and external_link != "_No response_":
        body += f"\n\n[Read more]({external_link})"

    return front_matter + "\n" + body + "\n"


def main(parsed, save_dir="_posts/news"):
    formatted = {
        "filename": _build_filename(parsed),
        "content": _build_content(parsed),
    }
    write_content_to_file(formatted, save_dir)
    return formatted


if __name__ == "__main__":
    issue_body = os.environ["ISSUE_BODY"]
    parsed = parse_issue_body(issue_body)
    main(parsed)

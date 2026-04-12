import datetime
import json
import os
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .add_update_publication import generate_publication_post
from . import write_content_to_file


_DOTENV_LOADED = False


def _load_dotenv_once() -> None:
    """Load key/value pairs from .env into os.environ once per process."""
    global _DOTENV_LOADED
    if _DOTENV_LOADED:
        return

    dotenv_path = Path(".env")
    if dotenv_path.exists():
        for line in dotenv_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)

    _DOTENV_LOADED = True


def _append_openalex_api_key(url: str) -> str:
    """Append OpenAlex API key if present in environment."""
    _load_dotenv_once()
    api_key = os.environ.get("OPENALEX_API_KEY", "").strip()
    if not api_key:
        return url

    separator = "&" if "?" in url else "?"
    return f"{url}{separator}api_key={api_key}"


def _request_openalex(url: str):
    """Make a request to the OpenAlex API."""
    url = _append_openalex_api_key(url)
    req = Request(url, headers={"User-Agent": "mailto:csdc-mcgill-website@github.com"})
    with urlopen(req) as response:
        return json.loads(response.read())


def _resolve_openalex_author_id(orcid: str = None, openalex_id: str = None):
    """Resolve to an OpenAlex author ID (e.g. 'A5023888391') from ORCID or a raw/URL OpenAlex ID."""
    if openalex_id:
        # Accept both bare ID and full URL
        return openalex_id.split("/")[-1]

    if orcid:
        orcid = orcid.replace("https://orcid.org/", "").strip()
        url = f"https://api.openalex.org/authors/https://orcid.org/{orcid}"
        try:
            data = _request_openalex(url)
            return data["id"].split("/")[-1]
        except Exception as exc:
            print(f"Could not resolve OpenAlex author from ORCID {orcid}: {exc}")
            return None

    return None


def _reconstruct_abstract(inverted_index):
    """Reconstruct plain-text abstract from OpenAlex inverted index format."""
    if not inverted_index:
        return "_Unavailable_"
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort()
    return " ".join(word for _, word in word_positions)


def _fetch_works(openalex_author_id: str, year_start: int, year_end: int, sleep: float = 1.0):
    """Fetch all works for an author within the given year range, handling pagination."""
    works = []
    cursor = "*"
    filter_str = f"author.id:{openalex_author_id},publication_year:{year_start}-{year_end}"

    while cursor:
        params = urlencode({
            "filter": filter_str,
            "sort": "publication_date:desc",
            "per_page": 200,
            "cursor": cursor,
            "select": "id,title,publication_year,publication_date,authorships,primary_location,ids,abstract_inverted_index,open_access",
        })
        url = f"https://api.openalex.org/works?{params}"

        try:
            data = _request_openalex(url)
        except Exception as exc:
            print(f"Error fetching OpenAlex works: {exc}")
            break

        results = data.get("results", [])
        works.extend(results)

        next_cursor = (data.get("meta") or {}).get("next_cursor")
        cursor = next_cursor if next_cursor and results else None

        if cursor and sleep > 0:
            time.sleep(sleep)

    return works


def _wrangle_work(work_json: dict) -> dict:
    """Map an OpenAlex work dict to the format expected by generate_publication_post."""
    author_names = [
        a["author"]["display_name"]
        for a in work_json.get("authorships", [])
        if (a.get("author") or {}).get("display_name")
    ]

    loc = work_json.get("primary_location") or {}
    source = loc.get("source") or {}
    venue = source.get("display_name") or ""

    pub_date = work_json.get("publication_date") or ""
    pub_year = work_json.get("publication_year") or 2000
    if pub_date:
        parts = pub_date.split("-")
        year = parts[0]
        month = parts[1] if len(parts) > 1 else "01"
        day = parts[2] if len(parts) > 2 else "01"
    else:
        year, month, day = str(pub_year), "01", "01"

    ids = work_json.get("ids") or {}
    doi = (ids.get("doi") or "").replace("https://doi.org/", "")
    arxiv_url = ids.get("arxiv") or ""
    openalex_work_id = (work_json.get("id") or "").split("/")[-1]

    if arxiv_url:
        shorthand = arxiv_url.replace("https://arxiv.org/abs/", "")
        link = arxiv_url
    elif doi:
        shorthand = doi
        link = f"https://doi.org/{doi}"
    else:
        oa_url = (work_json.get("open_access") or {}).get("oa_url") or ""
        shorthand = openalex_work_id
        link = oa_url or work_json.get("id") or ""

    title = (work_json.get("title") or "").replace("\n", " ")
    abstract = _reconstruct_abstract(work_json.get("abstract_inverted_index"))

    return {
        "title": title,
        "names": ", ".join(author_names),
        "tags": venue,
        "venue": venue,
        "shorthand": shorthand,
        "link": link,
        "year": year,
        "month": month,
        "day": day,
        "abstract": abstract,
        "_openalex_id": openalex_work_id,
    }


def main(
    orcid: str = None,
    openalex_id: str = None,
    year_start: int = None,
    year_end: int = None,
    save_dir: str = "_posts/papers",
    use_ignore_list: bool = True,
):
    if year_start is None:
        year_start = datetime.datetime.now().year
    if year_end is None:
        year_end = year_start

    ignore_list_fname = "records/semantic_paper_ids_ignored.json"
    if use_ignore_list and os.path.exists(ignore_list_fname):
        with open(ignore_list_fname) as f:
            ignored_ids = set(json.loads(f.read()))
    else:
        ignored_ids = set()

    author_id = _resolve_openalex_author_id(orcid=orcid, openalex_id=openalex_id)
    if not author_id:
        print("Could not resolve OpenAlex author ID. Skipping.")
        return {"cleaned": [], "ignored": ignored_ids}

    works = _fetch_works(author_id, year_start, year_end)
    cleaned = []

    for work in works:
        wrangled = _wrangle_work(work)
        dedup_key = wrangled.pop("_openalex_id")

        if dedup_key in ignored_ids:
            continue

        ignored_ids.add(dedup_key)
        formatted = generate_publication_post(wrangled)
        cleaned.append(formatted)
        write_content_to_file(formatted, save_dir)

    with open(ignore_list_fname, "w") as f:
        json.dump(sorted(ignored_ids), f, indent=2)

    return {"cleaned": cleaned, "ignored": ignored_ids}

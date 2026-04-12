import os
import sys
import json
import time
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

from ruamel.yaml import YAML

from . import parse_issue_body, write_content_to_file, remove_items_with_values
from .add_update_publication import generate_publication_post


def fetch_content(parsed, max_retry=3):
    method = parsed["method"]
    identifier = parsed["identifier"].strip()

    # Auto-detect: if identifier looks like a URL, always use the URL lookup method
    # so users can paste arxiv/doi/acl URLs regardless of which dropdown they chose.
    if identifier.startswith(("http://", "https://")):
        method = "URL"

    url = (
        f"https://api.semanticscholar.org/graph/v1/paper/{method}:{identifier}"
        "?fields=title,venue,year,publicationDate,authors.name,externalIds,url,abstract"
    )
    try:
        response = urlopen(url)
        data = json.loads(response.read())
    except HTTPError as e:
        if e.code == 404:
            # Fail loudly so the workflow shows an error and the user knows to resubmit.
            print(
                f"ERROR: Semantic Scholar paper not found for {method}:{identifier} (HTTP 404).\n"
                "Please verify the identifier is correct and re-submit the issue.",
                file=sys.stderr,
            )
            sys.exit(1)

        # Retry only for transient errors (rate limits / server issues).
        if max_retry > 0 and e.code in (408, 409, 425, 429, 500, 502, 503, 504):
            time.sleep(20)
            return fetch_content(parsed, max_retry - 1)
        raise
    except URLError:
        if max_retry > 0:
            time.sleep(20)
            return fetch_content(parsed, max_retry - 1)
        raise

    return data


def create_attr_to_username_map(lab_members, attribute):
    """
    Given a dictionary where key is a lab member's username, and the values are
    a dictionary containing their information (see _posts/authors.yml), create
    a dictionary mapping the value of the given attribute to the username.
    """
    return {
        member_info[attribute]: username
        for username, member_info in lab_members.items()
        if attribute in member_info
    }

def wrangle_fetched_content(parsed, paper_json):
    with open("_data/authors.yml") as f:
        yaml = YAML()
        yaml.preserve_quotes = True
        lab_members = yaml.load(f)

    parsed = remove_items_with_values(parsed, "_No response_")

    author_names = [data["name"] for data in paper_json["authors"]]
    paper_json["names"] = ", ".join(author_names)
    paper_json["tags"] = paper_json["venue"] or ""
    paper_json["shorthand"] = str(paper_json["paperId"])
    paper_json["link"] = paper_json["url"] or ""
    
    if paper_json['publicationDate']:
        year, month, day = paper_json["publicationDate"].split("-")
    else:
        year, month, day = paper_json['year'], "01", "01"
    
    paper_json["year"] = parsed.get("year", year)
    paper_json["month"] = parsed.get("month", month)
    paper_json["day"] = parsed.get("day", day)

    if "ArXiv" in paper_json["externalIds"]:
        link = f"https://arxiv.org/abs/{paper_json['externalIds']['ArXiv']}"
        paper_json["link"] = link
        paper_json["shorthand"] = paper_json["externalIds"]["ArXiv"]
    elif "DOI" in paper_json["externalIds"]:
        paper_json["link"] = f"https://doi.org/{paper_json['externalIds']['DOI']}"
        paper_json["shorthand"] = paper_json["externalIds"]["DOI"]
    elif "ACL" in paper_json["externalIds"]:
        paper_json["shorthand"] = paper_json["externalIds"]["ACL"]

    for key in ["title", "names", "tags", "venue", "shorthand", "link"]:
        paper_json[key] = (paper_json[key] or "").replace("\n", " ")

    fullname_to_username = create_attr_to_username_map(lab_members, "name")

    for author in paper_json["authors"]:
        if author["name"] in fullname_to_username:
            paper_json["author"] = fullname_to_username[author["name"]]
            break

    del (
        paper_json["externalIds"],
        paper_json["paperId"],
        paper_json["url"],
        paper_json["authors"],
        paper_json['publicationDate']
    )

    return paper_json


def main(parsed, save_dir="_posts/papers"):
    paper_json = fetch_content(parsed)
    paper_json = wrangle_fetched_content(parsed, paper_json)  # in-place
    formatted = generate_publication_post(paper_json)
    write_content_to_file(formatted, save_dir)


if __name__ == "__main__":
    issue_body = os.environ["ISSUE_BODY"]
    parsed = parse_issue_body(issue_body)
    main(parsed)

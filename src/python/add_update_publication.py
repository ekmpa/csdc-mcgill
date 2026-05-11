import argparse
import json
import os
from io import StringIO
from textwrap import dedent

from ruamel.yaml import YAML

from . import save_url_image, parse_issue_body, write_content_to_file


def _is_empty_response(value):
    if value is None:
        return True
    return str(value).strip() in ("", "_No response_", "None")


def _first_non_empty(parsed, *keys):
    for key in keys:
        value = parsed.get(key)
        if not _is_empty_response(value):
            return value
    return None

def front_matters_from_dict(d):
    # Convert to dict
    d = json.loads(json.dumps(d))

    file_object = StringIO()
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.dump(d, file_object)
    front_matter = file_object.getvalue()

    return front_matter


def front_matters_to_dict(front_matter):
    file_object = StringIO(front_matter)
    yaml = YAML()
    yaml.preserve_quotes = True
    d = yaml.load(file_object)
    return d


def get_filename(parsed):
    return "-".join([str(parsed[k]) for k in ["year", "month", "day", "shorthand"]]) + ".md"


def preprocess_parsed(parsed, keys_removed, for_update=False):
    """
    Removes any key with a value of "_No response_" or in `keys_removed`.
    """

    parsed = dict(parsed)

    # First need to add some keys
    parsed["categories"] = "Publications"

    # Normalize alternative key names from issue form labels.
    if "title_french" in parsed and "title_fr" not in parsed and not _is_empty_response(parsed.get("title_french")):
        parsed["title_fr"] = parsed.get("title_french")
    if "venue_french" in parsed and "venue_fr" not in parsed and not _is_empty_response(parsed.get("venue_french")):
        parsed["venue_fr"] = parsed.get("venue_french")
    if "abstract_french" in parsed and "abstract_fr" not in parsed and not _is_empty_response(parsed.get("abstract_french")):
        parsed["abstract_fr"] = parsed.get("abstract_french")

    if not for_update:
        # Bilingual fields: if French is missing, fall back to English.
        title_fr = _first_non_empty(parsed, "title_fr")
        parsed["title_fr"] = title_fr if title_fr is not None else parsed.get("title")

        venue_fr = _first_non_empty(parsed, "venue_fr")
        parsed["venue_fr"] = venue_fr if venue_fr is not None else parsed.get("venue")

        abstract_fr = _first_non_empty(parsed, "abstract_fr")
        parsed["abstract_fr"] = abstract_fr if abstract_fr is not None else parsed.get("abstract")

    # Sanitize some keys
    parsed["shorthand"] = parsed["shorthand"].replace("/", "-")

    # Then, modify some keys
    if parsed["tags"] != "_No response_":
        parsed["tags"] = [x.strip() for x in parsed["tags"].split(",")]

    if parsed["abstract"] == "_No response_" and not for_update:
        parsed["abstract"] = "_Unavailable_"

    if parsed.get("abstract_fr") == "_No response_" and not for_update:
        parsed["abstract_fr"] = parsed["abstract"]

    # Then, remove keys
    return {
        k: v
        for k, v in parsed.items()
        if v != "_No response_" and k not in keys_removed
    }


def generate_publication_post(parsed):
    """
    Format the parsed content into a string.
    """

    d = preprocess_parsed(
        parsed, keys_removed=["year", "month", "day", "shorthand", "abstract", "action", "title_french", "venue_french", "abstract_french"]
    )

    front_matter = front_matters_from_dict(d)
    top = dedent(f"---\n{front_matter}\n---\n")

    bottom = dedent(
        """
    *{{ page.names }}*

    {% assign current_path = page.url | default: page.permalink | default: '/' %}
    {% assign is_fr = false %}
    {% if current_path == '/fr/' or current_path contains '/fr/' %}
    {% assign is_fr = true %}
    {% endif %}

    **{% if is_fr and page.venue_fr %}{{ page.venue_fr }}{% else %}{{ page.venue }}{% endif %}**

    {% include display-publication-links.html pub=page %}

    {% if is_fr %}
    ## Resume
    {% if page.abstract_fr %}{{ page.abstract_fr }}{% else %}{{ page.abstract }}{% endif %}
    {% else %}
    ## Abstract
    {{ page.abstract }}
    {% endif %}
    
    """
    )

    try:
        content = top + bottom
    except TypeError as e:
        raise Exception(f"{e}\n{top=}\n{bottom=}\n{parsed=}") 

    return {
        "filename": get_filename(parsed),
        "content": content,
    }


def update_publication_post(parsed, load_dir="_posts/papers"):
    new_data = preprocess_parsed(
        parsed,
        keys_removed=["year", "month", "day", "shorthand", "abstract", "abstract_fr", "action", "title_french", "venue_french", "abstract_french"],
        for_update=True,
    )

    filename = get_filename(parsed)

    with open(os.path.join(load_dir, filename), "r") as f:
        lines = f.read()

    _, front_matter, bottom = lines.split("---", 2)

    old_data = front_matters_to_dict(front_matter)
    old_data.update(new_data)

    front_matter = front_matters_from_dict(old_data)
    top = f"---\n{front_matter}\n---\n"

    return {
        "filename": filename,
        "content": top + bottom,
    }

def main(parsed, save_dir="_posts/papers", image_dir="assets/images/papers"):
    img_path = save_url_image(
        fname=parsed["shorthand"],
        profile=parsed,
        key="thumbnail",
        image_dir=image_dir,
        size=(600, 600),
        crop_center=False
    )
    if img_path is not None:
        parsed["thumbnail"] = img_path

    if parsed["action"] == "Add publication":
        formatted = generate_publication_post(parsed)
    else:
        formatted = update_publication_post(parsed, load_dir=save_dir)
    write_content_to_file(formatted, save_dir)

    return formatted


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--issue_body_file", type=str)
    args = parser.parse_args()
    
    if args.issue_body_file is not None:
        with open(args.issue_body_file, "r") as f:
            issue_body = f.read()
    else:
        issue_body = os.environ["ISSUE_BODY"]
    
    parsed = parse_issue_body(issue_body)
    main(parsed)

import os
from pathlib import Path
from typing import Dict, List, Optional

from ruamel.yaml import YAML

from . import find_urls, save_url_image, parse_issue_body, remove_keys, remove_items_with_values


def _is_empty_response(value) -> bool:
    """Treat empty issue-form placeholders as missing values."""
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() in ("", "_No response_", "None")
    return False


def _normalize_avatar_value(value: str) -> str:
    """Extract the first URL from avatar input if markdown/HTML was pasted."""
    if _is_empty_response(value):
        return value

    urls = find_urls(value)
    if urls:
        return urls[0].rstrip('"\'<>')

    return value


def format_site_label(name: str) -> str:
    """Format social media site labels."""
    labels = {
        "github": "GitHub",
        "linkedin": "LinkedIn",
        "twitter": "Twitter",
        "scholar": "Scholar",
        "website": "Website"
    }
    return labels.get(name.lower(), name.title())


def format_social_media_links(parsed: Dict) -> List[Dict]:
    """Format social media links into structured format."""
    social_links = []
    for key in ["website", "twitter", "github", "scholar", "linkedin"]:
        if not _is_empty_response(parsed.get(key)):
            social_links.append({
                "label": format_site_label(key),
                "url": parsed[key]
            })
    return social_links


def process_role_data(parsed: Dict, prefix: str = "") -> Optional[Dict]:
    """Process role data from parsed content with optional prefix."""
    role_type = parsed.get(f"{prefix}type")
    if _is_empty_response(role_type):
        return None

    role = {
        "type": role_type,
        "title": parsed.get(f"{prefix}title")
    }

    # Add optional fields if they exist
    for field in ["advisor"]:
        value = parsed.get(f"{prefix}{field}")
        if not _is_empty_response(value):
            role[field] = value

    # Add new fields for affiliation and research directions
    affiliation = parsed.get(f"{prefix}affiliation")
    if not _is_empty_response(affiliation):
        role["affiliation"] = affiliation

    research_directions = parsed.get(f"{prefix}research_directions")
    if not _is_empty_response(research_directions):
        # Handle both string and list inputs for research directions
        if isinstance(research_directions, str):
            # Split by commas if it's a comma-separated string
            directions = [d.strip() for d in research_directions.split(',')]
        else:
            directions = research_directions
        role["research_directions"] = directions

    return role


def format_parsed_content(parsed: Dict) -> Dict:
    """Format the parsed content into the new structure."""
    formatted = {
        "name": parsed["name"],
    }

    # Process current role
    current_role = process_role_data(parsed, "current_role_")
    if current_role:
        formatted["current_role"] = current_role

    # Process past role if it exists (for updates)
    past_role = process_role_data(parsed, "past_role_")
    if past_role:
        formatted["past_roles"] = past_role

    # Add optional fields if they exist and aren't empty
    optional_fields = ["bio", "note", "orcid", "openalex_id", "avatar"]
    for field in optional_fields:
        if not _is_empty_response(parsed.get(field)):
            if field == "avatar":
                formatted[field] = _normalize_avatar_value(parsed[field])
            else:
                formatted[field] = parsed[field]

    # Auto-update is enabled whenever an ORCID or OpenAlex ID is present.
    formatted["auto_update_publications"] = bool(
        formatted.get("orcid") or formatted.get("openalex_id")
    )

    # Format social media links
    social_links = format_social_media_links(parsed)
    if social_links:
        formatted["social_media_links"] = social_links

    return formatted


def merge_profile_data(old_profile: Dict, new_profile: Dict) -> Dict:
    """Merge old and new profile data, preserving existing fields if not updated."""
    merged = old_profile.copy()

    # Update basic fields if provided
    for field in ["bio", "note", "orcid", "openalex_id", "avatar"]:
        if field in new_profile:
            merged[field] = new_profile[field]

    # Keep this derived from identifiers rather than user input.
    merged["auto_update_publications"] = bool(
        merged.get("orcid") or merged.get("openalex_id")
    )

    # Update current role if provided
    if "current_role" in new_profile:
        merged["current_role"] = new_profile["current_role"]
            
    # Handle past roles
    if "past_roles" in new_profile:
        existing_past_roles = merged.get("past_roles", [])
        new_past_role = new_profile["past_roles"]
        
        # Check if this past role already exists
        role_exists = False
        for role in existing_past_roles:
            if (role.get("type") == new_past_role["type"] and 
                role.get("title") == new_past_role["title"]):
                role.update(new_past_role)
                role_exists = True
                break
        
        if not role_exists:
            existing_past_roles.append(new_past_role)
            merged["past_roles"] = existing_past_roles

    # Merge social media links
    if "social_media_links" in new_profile:
        existing_links = {link["label"]: link for link in merged.get("social_media_links", [])}
        new_links = {link["label"]: link for link in new_profile["social_media_links"]}
        existing_links.update(new_links)
        merged["social_media_links"] = list(existing_links.values())

    return merged


def sort_by_lastname(authors: Dict) -> None:
    """Sort authors by last name."""
    lastname_to_user = {
        desc["name"].split()[-1] + user: user for user, desc in authors.items()
    }

    for key in sorted(lastname_to_user, reverse=True):
        user = lastname_to_user[key]
        desc = authors.pop(user)
        authors.insert(0, user, desc)


def main(parsed: Dict, action: str, site_data_dir: str = "_data/", image_dir: str = "assets/images/bio") -> Dict:
    site_data_dir = Path(site_data_dir)
    profile = format_parsed_content(parsed)

    yaml = YAML()
    yaml.preserve_quotes = True
    with open(site_data_dir / "authors.yml") as f:
        authors = yaml.load(f)
   
    if action == "Add member":
        # Handle new member addition
        if profile["name"] in authors:
            n = 2
            while (k := f'{profile["name"]} {n}') in authors:
                n += 1
            username = k
        else:
            username = profile["name"]
        authors[username] = profile
    else:
        # Handle member update
        name_to_username = {authors[username]["name"]: username for username in authors}
        if profile["name"] not in name_to_username:
            raise ValueError(f'{profile["name"]} not in authors')

        username = name_to_username[profile["name"]]
        authors[username] = merge_profile_data(authors[username], profile)

    # Handle avatar image if provided
    img_path = save_url_image(
        fname=username,
        profile=authors[username],
        key="avatar",
        image_dir=image_dir,
        crop_center=True,
        size=(300, 300),
    )

    if img_path is not None:
        authors[username]["avatar"] = img_path

    sort_by_lastname(authors)

    with open(site_data_dir / "authors.yml", "w") as f:
        yaml.dump(authors, f)

    return authors


if __name__ == "__main__":
    issue_body = os.environ["ISSUE_BODY"]
    action = os.environ["ACTION"]
    parsed = parse_issue_body(issue_body)
    main(parsed, action)
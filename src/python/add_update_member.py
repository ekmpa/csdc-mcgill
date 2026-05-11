import os
import re
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional

from ruamel.yaml import YAML

from . import find_urls, save_url_image, parse_issue_body, remove_keys, remove_items_with_values


def _normalize_heading_key(text: str) -> str:
    """Normalize issue-form headings so display-label changes don't break parsing."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def _normalize_role_type(value: str) -> str:
    """Map bilingual/variant role labels to canonical role types used by templates."""
    if _is_empty_response(value):
        return value

    norm = _normalize_heading_key(str(value))
    if "faculty" in norm or "professor" in norm or "faculte" in norm or "professeur" in norm:
        return "Faculty / Professor"
    if "staff" in norm or "personnel" in norm:
        return "Staff"
    if "postdoc" in norm or "postdoctor" in norm:
        return "Postdoc"
    if "student" in norm or "etudiant" in norm:
        return "Student"
    if "collaborator" in norm or "collaborateur" in norm:
        return "Collaborator"
    if "unaffiliated" in norm or "non_affilie" in norm:
        return "Unaffiliated"
    return value


def _normalize_role_title(value: str) -> str:
    """Normalize title variants (e.g., doctoral variants -> PhD)."""
    if _is_empty_response(value):
        return value

    cleaned = str(value).strip()
    norm = _normalize_heading_key(cleaned)

    if norm in {"phd", "ph_d", "doctorat", "doctorate", "doctoral", "doctorante", "doctoral_student", "doctoral_candidate", "doctorant"}:
        return "PhD"
    if norm in {"maitrise", "masters", "master_s", "master", "msc", "m_a", "m_a_s", "m_a_sc"}:
        return "Master's"
    return cleaned


def _translate_role_title_fr(value: str) -> str:
    """Auto-generate a French title when no explicit French title is provided."""
    if _is_empty_response(value):
        return value

    norm = _normalize_heading_key(_normalize_role_title(str(value)))
    translations = {
        "phd": "Doctorat",
        "master_s": "Maitrise",
        "professor": "Professeur",
        "associate_professor": "Professeur associe",
        "assistant_professor": "Professeur adjoint",
        "postdoc": "Postdoctorat",
        "postdoctoral_fellow": "Stagiaire postdoctoral",
        "research_assistant": "Assistant de recherche",
        "director": "Directeur",
        "student": "Etudiant",
    }
    return translations.get(norm, value)


def _canonicalize_member_parsed_input(parsed: Dict) -> Dict:
    """Map display labels to stable internal keys so form label text can evolve safely."""
    canonical = dict(parsed)
    by_norm = {_normalize_heading_key(k): v for k, v in parsed.items()}

    alias_map = {
        "name": ["name", "name_nom"],
        "alumni": ["alumni", "member_status", "status_statut"],
        "avatar": ["avatar", "profile_picture", "profile_picture_photo_de_profil"],
        "bio": ["bio", "bio_en"],
        "bio_fr": ["bio_fr", "bio_french"],
        "note": ["note"],
        "note_fr": ["note_fr", "note_french"],
        "current_role_type": ["current_role_type", "current_role_role_actuel"],
        "current_role_title": ["current_role_title"],
        "current_role_affiliation": ["current_role_affiliation", "current_affiliation_affiliation_actuelle"],
        "current_role_advisor": ["current_role_advisor", "current_role_advisor_superviseur_e_actuel_le"],
        "current_role_start_date": ["current_role_start_date", "start_date_date_de_debut"],
        "current_role_end_date": ["current_role_end_date", "end_date_alumni_only_date_de_fin_anciens_membres_seulement"],
        "orcid": ["orcid"],
        "openalex_id": ["openalex_id", "openalex_id_optional"],
        "website": ["website", "website_site_personnel"],
        "scholar": ["scholar", "google_scholar"],
        "linkedin": ["linkedin"],
        "twitter": ["twitter", "twitter_x"],
        "github": ["github"],
    }

    for target, aliases in alias_map.items():
        if _is_empty_response(canonical.get(target)):
            for alias in aliases:
                if alias in by_norm and not _is_empty_response(by_norm[alias]):
                    canonical[target] = by_norm[alias]
                    break

    return canonical


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


def _first_non_empty(parsed: Dict, *keys: str):
    """Return the first non-empty value among candidate parsed keys."""
    for key in keys:
        value = parsed.get(key)
        if not _is_empty_response(value):
            return value
    return None


def _get_avatar_input(parsed: Dict):
    """Support both the old Avatar label and the new Profile picture label."""
    avatar_value = parsed.get("avatar")
    if not _is_empty_response(avatar_value):
        return avatar_value

    return parsed.get("profile_picture")


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
    role_type = _normalize_role_type(parsed.get(f"{prefix}type"))
    if _is_empty_response(role_type):
        return None

    role_title = _first_non_empty(
        parsed,
        f"{prefix}title",
        f"{prefix}title_french",
    )
    role_title = _normalize_role_title(role_title)

    role = {
        "type": role_type,
        "title": role_title
    }

    title_fr = _first_non_empty(
        parsed,
        f"{prefix}title_fr",
        f"{prefix}title_french",
    )
    if not _is_empty_response(title_fr):
        role["title_fr"] = title_fr
    elif not _is_empty_response(role_title):
        role["title_fr"] = _translate_role_title_fr(role_title)

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
    optional_field_map = {
        "bio": ["bio"],
        "bio_fr": ["bio_fr", "bio_french"],
        "note": ["note"],
        "note_fr": ["note_fr", "note_french"],
        "orcid": ["orcid"],
        "openalex_id": ["openalex_id"],
        "avatar": ["avatar", "profile_picture"],
    }
    for field, candidates in optional_field_map.items():
        value = _get_avatar_input(parsed) if field == "avatar" else _first_non_empty(parsed, *candidates)
        if not _is_empty_response(value):
            if field == "avatar":
                formatted[field] = _normalize_avatar_value(value)
            else:
                formatted[field] = value

    # Format social media links
    social_links = format_social_media_links(parsed)
    if social_links:
        formatted["social_media_links"] = social_links

    return formatted


def merge_profile_data(old_profile: Dict, new_profile: Dict) -> Dict:
    """Merge old and new profile data, preserving existing fields if not updated."""
    merged = old_profile.copy()

    # Update basic fields if provided
    for field in ["bio", "bio_fr", "note", "note_fr", "orcid", "openalex_id", "avatar"]:
        if field in new_profile:
            merged[field] = new_profile[field]

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


def main(parsed: Dict, action: str = "", site_data_dir: str = "_data/", image_dir: str = "assets/images/bio") -> Dict:
    site_data_dir = Path(site_data_dir)
    parsed = _canonicalize_member_parsed_input(parsed)
    profile = format_parsed_content(parsed)

    yaml = YAML()
    yaml.preserve_quotes = True
    with open(site_data_dir / "authors.yml") as f:
        authors = yaml.load(f)
   
    if action not in {"Add member", "Update member"}:
        name_to_username = {authors[username]["name"]: username for username in authors}
        if profile["name"] in name_to_username:
            action = "Update member"
        else:
            action = "Add member"

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
    parsed = parse_issue_body(issue_body)

    action = os.environ.get("ACTION", "").strip()
    if not action:
        parsed_action = str(parsed.get("action", "")).strip()
        if parsed_action in {"Add member", "Update member"}:
            action = parsed_action

    main(parsed, action)
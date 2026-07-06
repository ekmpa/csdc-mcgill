import argparse
import datetime
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Set, Tuple

from ruamel.yaml import YAML


AxisId = str
Phrase = Tuple[str, str, Set[str]]  # (en_label, fr_label, signal_tokens)


@dataclass(frozen=True)
class AxisDefinition:
    axis_id: AxisId
    title_en: str
    title_fr: str
    core_tokens: Set[str]
    phrase_bank: Sequence[Phrase]


AXES: Sequence[AxisDefinition] = (
    AxisDefinition(
        axis_id="axis_1",
        title_en="Learning Democratic Citizenship in an Unequal World",
        title_fr="L'apprentissage de la citoyennete democratique",
        core_tokens={
            "citizenship",
            "learning",
            "civic",
            "education",
            "school",
            "socialization",
            "generation",
            "generational",
            "identity",
            "trust",
            "social",
            "cohesion",
            "information",
            "literacy",
            "inequality",
            "youth",
            "student",
            "community",
            "immigrant",
            "immigration",
            "integration",
            "democracy",
            "democratic",
            "backsliding",
            "tolerance",
        },
        phrase_bank=(
            ("Civic education and schools", "Education civique et ecoles", {"civic", "education", "school", "student"}),
            (
                "Political socialization across generations",
                "Socialisation politique intergenerationnelle",
                {"socialization", "generation", "youth", "learning"},
            ),
            (
                "Immigration, integration, and belonging",
                "Immigration, integration et appartenance",
                {"immigrant", "immigration", "integration", "community", "belonging"},
            ),
            (
                "Support for democracy and democratic resilience",
                "Soutien a la democratie et resilience democratique",
                {"democracy", "democratic", "support", "backsliding", "tolerance"},
            ),
            ("Political trust", "Confiance politique", {"trust", "institution", "political"}),
            ("Social cohesion", "Cohesion sociale", {"social", "cohesion", "community"}),
            ("Information literacy", "Competences informationnelles", {"information", "literacy", "media"}),
            ("Citizen identity", "Identite citoyenne", {"identity", "citizenship", "community"}),
            ("Educational inequality", "Inegalites educatives", {"education", "inequality", "student"}),
        ),
    ),
    AxisDefinition(
        axis_id="axis_2",
        title_en="The Practice of Democratic Citizenship",
        title_fr="La pratique de la citoyennete democratique",
        core_tokens={
            "participation",
            "vote",
            "voting",
            "turnout",
            "opinion",
            "information",
            "media",
            "consumption",
            "news",
            "partisan",
            "polarization",
            "engagement",
            "deliberation",
            "public",
            "electoral",
            "citizenship",
            "misinformation",
            "disinformation",
            "fact",
            "checking",
            "verification",
        },
        phrase_bank=(
            ("Media consumption", "Consommation mediatique", {"media", "consumption", "news", "information"}),
            ("Public opinion", "Opinion publique", {"public", "opinion", "attitude", "political"}),
            ("Political participation", "Participation politique", {"participation", "citizenship", "engagement"}),
            ("Voting and turnout", "Vote et participation electorale", {"vote", "voting", "turnout", "electoral"}),
            ("Partisan polarization", "Polarisation partisane", {"partisan", "polarization", "party"}),
            ("Electoral behavior", "Comportement electoral", {"electoral", "vote", "voting"}),
            ("Public deliberation", "Deliberation publique", {"public", "deliberation", "debate"}),
            (
                "Misinformation and fact-checking",
                "Desinformation et verification des faits",
                {"misinformation", "disinformation", "fact", "checking", "verification", "rumor", "rumour"},
            ),
        ),
    ),
    AxisDefinition(
        axis_id="axis_3",
        title_en="Political Representation, Institutions, and Inequality",
        title_fr="Representation, institutions et inegalites politiques",
        core_tokens={
            "representation",
            "governance",
            "institution",
            "institutions",
            "parliament",
            "legislative",
            "government",
            "responsiveness",
            "electoral",
            "system",
            "policy",
            "party",
            "trust",
            "democratic",
            "democracy",
            "inequality",
            "redistribution",
            "state",
        },
        phrase_bank=(
            ("Citizen-institution relations", "Relation citoyens-institutions", {"citizen", "institution", "trust"}),
            ("Political institutions", "Institutions politiques", {"institution", "institutions", "parliament", "legislative"}),
            ("Government responsiveness", "Reactivite des gouvernements", {"government", "responsiveness", "policy"}),
            ("Political representation", "Representation politique", {"representation", "party", "electoral"}),
            ("Democratic governance", "Gouvernance democratique", {"governance", "democratic", "government"}),
            ("Electoral systems", "Systemes electoraux", {"electoral", "system", "institution"}),
            (
                "Political inequality",
                "Inegalite politique",
                {"inequality", "political", "representation", "redistribution", "democratic"},
            ),
            (
                "Parties and political competition",
                "Partis et competition politique",
                {"party", "competition", "electoral", "representation"},
            ),
        ),
    ),
)


STOPWORDS: Set[str] = {
    "the", "a", "an", "and", "or", "for", "of", "to", "in", "on", "at", "from", "by", "with", "without",
    "we", "our", "this", "that", "these", "those", "is", "are", "was", "were", "be", "been", "being", "as",
    "it", "its", "their", "they", "them", "you", "your", "about", "across", "into", "between", "during",
    "through", "using", "use", "new", "can", "could", "would", "should", "may", "might", "also", "more",
    "most", "than", "such", "based", "within", "toward", "towards", "under", "over", "de", "la", "le", "les",
    "des", "du", "dans", "sur", "pour", "par", "avec", "sans", "entre", "chez", "nous", "vous", "ils", "elles",
    "est", "sont", "ete", "etre", "au", "aux", "ce", "cet", "cette", "ces", "une", "un", "d", "l", "et", "ou",
    "qui", "que", "dont", "mais", "plus", "moins", "tout", "tous", "toutes", "notre", "nos", "vos", "leurs",
}


NOISE_TERMS: Set[str] = {
    "supplementary", "dataset", "data", "static", "stats", "zenodo", "metric", "waveform", "inversion",
    "sensor", "branch", "synchronous", "prediction", "therapy", "antiretroviral", "software", "package",
}

FOUNDATION_YEAR = 2008


TOKEN_NORMALIZATION: Dict[str, str] = {
    "citoyennete": "citizenship",
    "citoyen": "citizen",
    "citoyens": "citizen",
    "civique": "civic",
    "gouvernance": "governance",
    "democratique": "democratic",
    "democratie": "democracy",
    "elections": "electoral",
    "electorales": "electoral",
    "electorale": "electoral",
    "institutions": "institution",
    "inegalites": "inequality",
    "inegalite": "inequality",
    "jeunes": "youth",
    "jeunesse": "youth",
    "etudiants": "student",
    "students": "student",
    "schools": "school",
    "parties": "party",
    "policies": "policy",
    "governments": "government",
    "confiance": "trust",
    "cohesion": "cohesion",
    "competences": "literacy",
    "informationnelles": "information",
    "reactivite": "responsiveness",
    "parlementaires": "parliamentary",
    "representation": "representation",
    "deepfakes": "deepfake",
    "deepfaked": "deepfake",
    "misinformations": "misinformation",
    "disinformations": "disinformation",
    "algorithms": "algorithmic",
    "algorithm": "algorithmic",
    "platforms": "platform",
    "llm": "ai",
    "llms": "ai",
    "digitales": "digital",
    "numerique": "digital",
    "numeriques": "digital",
    "online": "online",
}


AXIS_BY_ID: Dict[AxisId, AxisDefinition] = {axis.axis_id: axis for axis in AXES}

AXIS_PRIORITY_PHRASES: Dict[AxisId, Sequence[str]] = {
    "axis_1": (
        "Support for democracy and democratic resilience",
        "Political socialization across generations",
        "Immigration, integration, and belonging",
    ),
    "axis_2": (
        "Misinformation and fact-checking",
    ),
    "axis_3": (
        "Political institutions",
        "Political inequality",
    ),
}

AXIS_ALLOWED_PHRASES: Dict[AxisId, Set[str]] = {
    "axis_1": {
        "Civic education and schools",
        "Political socialization across generations",
        "Immigration, integration, and belonging",
        "Support for democracy and democratic resilience",
        "Political trust",
        "Social cohesion",
        "Information literacy",
        "Citizen identity",
        "Educational inequality",
    },
    "axis_2": {
        "Media consumption",
        "Public opinion",
        "Political participation",
        "Voting and turnout",
        "Electoral behavior",
        "Misinformation and fact-checking",
        "Partisan polarization",
        "Public deliberation",
    },
    "axis_3": {
        "Political institutions",
        "Political inequality",
        "Government responsiveness",
        "Democratic governance",
        "Electoral systems",
        "Citizen-institution relations",
        "Parties and political competition",
    },
}

TECH_ORIENTED_TOKENS: Set[str] = {
    "misinformation",
    "disinformation",
    "fact",
    "checking",
    "verification",
    "ai",
    "algorithmic",
    "deepfake",
    "synthetic",
    "generative",
    "platform",
    "regulation",
    "accountability",
    "information",
    "media",
    "literacy",
    "digital",
    "online",
}

# Extra weighting for faculty bios explicitly mapped to an axis.
MAPPED_FACULTY_BIO_WEIGHT: float = 3.0

HIGHLIGHT_TARGET_FACULTY: Set[str] = {
    "benjamin forest",
    "eran shor",
    "reihaneh rabbany",
    "eric hehman",
    "leonardo baccini",
    "nicolas ajzenman",
}

HIGHLIGHT_TARGET_FACULTY_ORDER: Sequence[str] = (
    "benjamin forest",
    "eran shor",
    "reihaneh rabbany",
    "eric hehman",
    "leonardo baccini",
    "nicolas ajzenman",
)


def normalize_person_name(name: str) -> str:
    cleaned = normalize_text(name)
    cleaned = re.sub(r"[^a-z\s,.-]", " ", cleaned)
    cleaned = cleaned.replace(".", " ")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if "," in cleaned:
        parts = [part.strip() for part in cleaned.split(",") if part.strip()]
        if len(parts) >= 2:
            cleaned = f"{parts[1]} {parts[0]}".strip()
    return cleaned


def normalize_names_blob(names_text: str) -> str:
    cleaned = normalize_text(names_text)
    cleaned = re.sub(r"[^a-z\s,.-]", " ", cleaned)
    cleaned = cleaned.replace(".", " ")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def load_faculty_name_sets(authors_path: Path) -> Tuple[Set[str], Set[str], Dict[str, str], Dict[str, List[str]], Set[str], Set[str]]:
    if not authors_path.exists():
        return set(), set(), {}, {}, set(), set()

    yaml = YAML(typ="safe")
    authors_data = yaml.load(authors_path.read_text(encoding="utf-8")) or {}

    faculty_full_names: Set[str] = set()
    faculty_last_names: Set[str] = set()
    faculty_bio_by_full_name: Dict[str, str] = {}
    faculty_bio_by_last_name: Dict[str, List[str]] = {}
    student_full_names: Set[str] = set()
    student_last_names: Set[str] = set()

    for _, profile in authors_data.items():
        if not isinstance(profile, dict):
            continue

        current_role = profile.get("current_role", {}) or {}
        role_type = normalize_text(str(current_role.get("type", "") or ""))
        name = str(profile.get("name", "") or "").strip()
        if not name:
            continue

        normalized_name = normalize_person_name(name)
        if not normalized_name:
            continue

        last_name = normalized_name.split(" ")[-1]
        is_faculty = "faculty" in role_type or "professor" in role_type
        is_student_like = any(
            marker in role_type
            for marker in ("student", "postdoc", "post-doctoral", "phd", "doctoral", "master", "msc", "ma")
        )

        if is_faculty:
            faculty_full_names.add(normalized_name)
            if len(last_name) >= 3:
                faculty_last_names.add(last_name)

            bio_value = str(profile.get("bio", "") or "").strip()
            if bio_value:
                faculty_bio_by_full_name[normalized_name] = bio_value
                if len(last_name) >= 3:
                    existing_bios = faculty_bio_by_last_name.setdefault(last_name, [])
                    if bio_value not in existing_bios:
                        existing_bios.append(bio_value)
        elif is_student_like:
            student_full_names.add(normalized_name)
            if len(last_name) >= 3:
                student_last_names.add(last_name)

    return faculty_full_names, faculty_last_names, faculty_bio_by_full_name, faculty_bio_by_last_name, student_full_names, student_last_names


def get_matching_person_names(
    names_value: str,
    full_names: Set[str],
    last_names: Set[str],
) -> List[str]:
    if not names_value:
        return []

    normalized_names_text = normalize_names_blob(names_value)
    matches: Set[str] = set()
    for full_name in full_names:
        if full_name in normalized_names_text:
            matches.add(full_name)

    word_tokens = set(re.findall(r"[a-z]{3,}", normalized_names_text))
    for full_name in full_names:
        last_name = full_name.split(" ")[-1]
        if len(last_name) >= 3 and last_name in last_names and last_name in word_tokens:
            matches.add(full_name)

    return sorted(matches)


def load_faculty_axis_map(
    mapping_path: Path,
    faculty_bio_by_full_name: Dict[str, str],
) -> Tuple[Dict[AxisId, Counter], Dict[AxisId, List[str]]]:
    axis_bio_token_boosts: Dict[AxisId, Counter] = {axis.axis_id: Counter() for axis in AXES}
    axis_faculty_names: Dict[AxisId, List[str]] = {axis.axis_id: [] for axis in AXES}

    if not mapping_path.exists():
        return axis_bio_token_boosts, axis_faculty_names

    yaml = YAML(typ="safe")
    mapping_data = yaml.load(mapping_path.read_text(encoding="utf-8")) or {}
    faculty_to_axes = mapping_data.get("faculty_to_axes", mapping_data)
    if not isinstance(faculty_to_axes, dict):
        return axis_bio_token_boosts, axis_faculty_names

    for raw_name, axes_value in faculty_to_axes.items():
        faculty_name = str(raw_name or "").strip()
        if not faculty_name:
            continue

        normalized_name = normalize_person_name(faculty_name)
        bio_text = faculty_bio_by_full_name.get(normalized_name, "")
        if not bio_text:
            continue

        axes_list = axes_value if isinstance(axes_value, list) else [axes_value]
        bio_tokens = tokenize(bio_text)
        if not bio_tokens:
            continue

        for axis_item in axes_list:
            axis_id = str(axis_item or "").strip()
            if axis_id not in AXIS_BY_ID:
                continue
            axis_bio_token_boosts[axis_id].update(bio_tokens)
            axis_faculty_names[axis_id].append(faculty_name)

    for axis_id in axis_faculty_names:
        axis_faculty_names[axis_id] = sorted(set(axis_faculty_names[axis_id]))

    return axis_bio_token_boosts, axis_faculty_names


def get_matching_faculty_bio_text(
    names_value: str,
    faculty_full_names: Set[str],
    faculty_last_names: Set[str],
    faculty_bio_by_full_name: Dict[str, str],
    faculty_bio_by_last_name: Dict[str, List[str]],
) -> str:
    if not names_value:
        return ""

    normalized_names_text = normalize_names_blob(names_value)
    matched_bios: List[str] = []
    seen_bios: Set[str] = set()

    for full_name in faculty_full_names:
        if full_name in normalized_names_text:
            bio_value = faculty_bio_by_full_name.get(full_name, "")
            if bio_value and bio_value not in seen_bios:
                matched_bios.append(bio_value)
                seen_bios.add(bio_value)

    # Fall back to surname matching for edge cases in publication author formatting.
    name_tokens = set(re.findall(r"[a-z]{3,}", normalized_names_text))
    for last_name in faculty_last_names:
        if last_name not in name_tokens:
            continue
        for bio_value in faculty_bio_by_last_name.get(last_name, []):
            if bio_value and bio_value not in seen_bios:
                matched_bios.append(bio_value)
                seen_bios.add(bio_value)

    return " ".join(matched_bios)


def parse_publication_year(path: Path, data: dict) -> Optional[int]:
    date_value = str(data.get("date", "") or "")
    match = re.search(r"(19|20)\d{2}", date_value)
    if match:
        return int(match.group(0))

    filename_match = re.match(r"(19|20)\d{2}-", path.name)
    if filename_match:
        return int(filename_match.group(0)[:4])

    return None


def publication_has_faculty_author(
    names_value: str,
    faculty_full_names: Set[str],
    faculty_last_names: Set[str],
) -> bool:
    if not names_value:
        return False

    normalized_names_text = normalize_names_blob(names_value)
    if any(full_name in normalized_names_text for full_name in faculty_full_names):
        return True

    word_tokens = set(re.findall(r"[a-z]{3,}", normalized_names_text))
    return any(last_name in word_tokens for last_name in faculty_last_names)


def normalize_text(text: str) -> str:
    lowered = text.lower()
    lowered = unicodedata.normalize("NFKD", lowered)
    lowered = "".join(ch for ch in lowered if not unicodedata.combining(ch))
    lowered = lowered.replace("\u2019", "'")
    lowered = lowered.replace("\u2018", "'")
    lowered = lowered.replace("\u2013", "-")
    lowered = lowered.replace("\u2014", "-")
    return lowered


def strip_latex_markup(text: str) -> str:
    """Strip lightweight LaTeX-like markup for clean UI display in highlights."""
    if not text:
        return ""

    cleaned = str(text)
    cleaned = re.sub(r"\$\$(.*?)\$\$", r"\1", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"\$(.*?)\$", r"\1", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"\\text(?:bf|tt|ttt|it)\s*\{([^{}]*)\}", r"\1", cleaned)
    cleaned = re.sub(r"[{}]", "", cleaned)
    cleaned = re.sub(r"\\[a-zA-Z]+", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def normalize_display_venue(text: str) -> str:
    """Normalize venue text for UI display; collapse placeholder values to empty."""
    if not text:
        return ""

    cleaned = str(text).strip()
    if not cleaned:
        return ""

    lowered = cleaned.lower()
    if lowered in {"n/a", "na", "none", "null", "_no response_", "_unavailable_"}:
        return ""
    if cleaned in {".", "-", "--", "·"}:
        return ""

    return cleaned


def tokenize(text: str) -> List[str]:
    words = re.findall(r"ai|[a-z]{3,}", normalize_text(text))
    normalized = [TOKEN_NORMALIZATION.get(word, word) for word in words]
    return [word for word in normalized if word not in STOPWORDS and word not in NOISE_TERMS]


def read_front_matter(path: Path) -> Tuple[dict, str]:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}, ""

    # Parse only YAML delimiter lines to avoid breaking on inline '---' in abstracts.
    lines = content.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, content

    closing_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            closing_idx = idx
            break

    if closing_idx is None:
        return {}, content

    yaml_text = "".join(lines[1:closing_idx])
    body_text = "".join(lines[closing_idx + 1 :])
    yaml = YAML(typ="safe")
    data = yaml.load(yaml_text) or {}
    return data, body_text


def normalize_tag(value: str) -> str:
    return re.sub(r"\s+", " ", str(value).strip())


def build_documents(
    posts_dir: Path,
    faculty_full_names: Optional[Set[str]] = None,
    faculty_last_names: Optional[Set[str]] = None,
    faculty_bio_by_full_name: Optional[Dict[str, str]] = None,
    faculty_bio_by_last_name: Optional[Dict[str, List[str]]] = None,
    student_full_names: Optional[Set[str]] = None,
    student_last_names: Optional[Set[str]] = None,
) -> List[dict]:
    documents: List[dict] = []
    faculty_full_names = faculty_full_names or set()
    faculty_last_names = faculty_last_names or set()
    faculty_bio_by_full_name = faculty_bio_by_full_name or {}
    faculty_bio_by_last_name = faculty_bio_by_last_name or {}
    student_full_names = student_full_names or set()
    student_last_names = student_last_names or set()

    for path in sorted(posts_dir.glob("*.md")):
        data, body = read_front_matter(path)

        title = strip_latex_markup(str(data.get("title", "") or ""))
        title_fr = strip_latex_markup(str(data.get("title_fr", "") or ""))
        abstract = str(data.get("abstract", "") or "")
        abstract_fr = str(data.get("abstract_fr", "") or "")

        tags = data.get("tags", []) or []
        clean_tags = [
            normalize_tag(tag)
            for tag in tags
            if normalize_tag(tag) and normalize_tag(tag) not in {"_No response_", "_Unavailable_"}
        ]
        names_value = str(data.get("names", "") or "")
        publication_year = parse_publication_year(path, data)
        if publication_year is not None and publication_year < FOUNDATION_YEAR:
            continue
        has_faculty_author = publication_has_faculty_author(
            names_value,
            faculty_full_names=faculty_full_names,
            faculty_last_names=faculty_last_names,
        )
        matched_faculty_names = get_matching_person_names(
            names_value,
            full_names=faculty_full_names,
            last_names=faculty_last_names,
        )
        matched_student_names = get_matching_person_names(
            names_value,
            full_names=student_full_names,
            last_names=student_last_names,
        )
        faculty_bio_text = get_matching_faculty_bio_text(
            names_value,
            faculty_full_names=faculty_full_names,
            faculty_last_names=faculty_last_names,
            faculty_bio_by_full_name=faculty_bio_by_full_name,
            faculty_bio_by_last_name=faculty_bio_by_last_name,
        )

        title_text = " ".join(part for part in [title, title_fr] if part)
        abstract_text = " ".join(part for part in [abstract, abstract_fr] if part)
        full_text = "\n".join(
            part for part in [title_text, abstract_text, body, " ".join(clean_tags), names_value, faculty_bio_text] if part
        )
        full_tokens = tokenize(full_text)
        faculty_bio_tokens = tokenize(faculty_bio_text)
        if faculty_bio_tokens:
            # Give faculty-only profile signal stronger influence than generic paper text.
            full_tokens.extend(faculty_bio_tokens)
            full_tokens.extend(faculty_bio_tokens)

        documents.append(
            {
                "path": str(path),
                "tokens": full_tokens,
                "title_tokens": tokenize(title_text),
                "abstract_tokens": tokenize(abstract_text),
                "faculty_bio_tokens": faculty_bio_tokens,
                "year": publication_year,
                "has_faculty_author": has_faculty_author,
                "matched_faculty_names": matched_faculty_names,
                "has_student_author": bool(matched_student_names),
                "raw_meta": {
                    "title": strip_latex_markup(str(data.get("title", "") or "")).strip(),
                    "names": str(data.get("names", "") or "").strip(),
                    "venue": normalize_display_venue(str(data.get("venue", "") or "")),
                    "link": str(data.get("link", "") or "").strip(),
                },
            }
        )

    return documents


def filter_documents(
    documents: Sequence[dict],
    recent_years: int,
    faculty_only: bool,
) -> Tuple[List[dict], Dict[str, object]]:
    current_year = datetime.date.today().year
    min_year: Optional[int] = FOUNDATION_YEAR
    if recent_years > 0:
        min_year = max(FOUNDATION_YEAR, current_year - recent_years + 1)

    filtered: List[dict] = []
    for doc in documents:
        year = doc.get("year")
        if min_year is not None and (year is None or int(year) < min_year):
            continue
        if faculty_only and not doc.get("has_faculty_author", False):
            continue
        filtered.append(doc)

    summary = {
        "recent_years": recent_years,
        "min_year": min_year,
        "faculty_only": faculty_only,
        "selected_publication_count": len(filtered),
        "available_publication_count": len(documents),
    }
    return filtered, summary


def get_axis_scores(tokens: Sequence[str]) -> Tuple[Dict[AxisId, int], Dict[AxisId, float]]:
    token_counts = Counter(tokens)
    raw_scores: Dict[AxisId, int] = {}
    for axis in AXES:
        raw_scores[axis.axis_id] = sum(token_counts.get(token, 0) for token in axis.core_tokens)

    total = sum(raw_scores.values())
    if total == 0:
        normalized = {axis.axis_id: 0.0 for axis in AXES}
    else:
        normalized = {axis_id: score / total for axis_id, score in raw_scores.items()}

    return raw_scores, normalized


def assign_documents_to_axes(
    documents: List[dict],
    min_share: float = 0.24,
    min_hits: int = 2,
) -> Tuple[Dict[AxisId, List[dict]], Dict[str, dict]]:
    axis_docs: Dict[AxisId, List[dict]] = {axis.axis_id: [] for axis in AXES}
    diagnostics: Dict[str, dict] = {}

    for doc in documents:
        raw_scores, relevance = get_axis_scores(doc["tokens"])
        doc["axis_raw_scores"] = raw_scores
        doc["axis_relevance"] = relevance

        assigned: List[AxisId] = []
        for axis in AXES:
            axis_id = axis.axis_id
            if raw_scores[axis_id] >= min_hits and relevance[axis_id] >= min_share:
                axis_docs[axis_id].append(doc)
                assigned.append(axis_id)

        if not assigned and sum(raw_scores.values()) > 0:
            best_axis = max(raw_scores, key=raw_scores.get)
            axis_docs[best_axis].append(doc)
            assigned = [best_axis]

        diagnostics[doc["path"]] = {
            "raw": raw_scores,
            "relevance": {k: round(v, 3) for k, v in relevance.items()},
            "assigned_axes": assigned,
        }

    return axis_docs, diagnostics


def score_axis_phrase_bank(
    axis: AxisDefinition,
    docs: Sequence[dict],
    axis_bio_token_boosts: Optional[Dict[AxisId, Counter]] = None,
) -> List[Tuple[str, str, float]]:
    weighted_tokens: Counter = Counter()
    weighted_title_tokens: Counter = Counter()
    current_year = datetime.date.today().year

    for doc in docs:
        axis_weight = max(0.25, doc["axis_relevance"].get(axis.axis_id, 0.0))
        year = doc.get("year")
        recency_weight = 1.0
        if isinstance(year, int):
            recency_weight += max(0.0, min(0.6, 0.08 * (year - (current_year - 6))))
        weight = axis_weight * recency_weight
        for token, freq in Counter(doc["tokens"]).items():
            weighted_tokens[token] += freq * weight
        for token, freq in Counter(doc["title_tokens"]).items():
            weighted_title_tokens[token] += freq * weight

    if axis_bio_token_boosts:
        for token, freq in axis_bio_token_boosts.get(axis.axis_id, Counter()).items():
            weighted_tokens[token] += freq * MAPPED_FACULTY_BIO_WEIGHT

    scores: List[Tuple[str, str, float]] = []
    for en_label, fr_label, signals in axis.phrase_bank:
        signal_score = sum(weighted_tokens.get(token, 0.0) for token in signals)
        title_bonus = 0.4 * sum(weighted_title_tokens.get(token, 0.0) for token in signals)
        technical_overlap = len(signals.intersection(TECH_ORIENTED_TOKENS))
        technical_bonus = 0.55 * technical_overlap
        specificity_bonus = 0.08 * len(signals)
        deterministic_tie_breaker = 1e-6 * len(en_label)
        scores.append(
            (
                en_label,
                fr_label,
                signal_score + title_bonus + technical_bonus + specificity_bonus + deterministic_tie_breaker,
            )
        )

    scores.sort(key=lambda item: item[2], reverse=True)
    return scores


def pick_axis_phrases(
    axis: AxisDefinition,
    docs: Sequence[dict],
    min_tags: int,
    max_tags: int,
    axis_bio_token_boosts: Optional[Dict[AxisId, Counter]] = None,
) -> Tuple[List[str], List[str]]:
    scored = score_axis_phrase_bank(axis, docs, axis_bio_token_boosts=axis_bio_token_boosts)
    allowed_labels = AXIS_ALLOWED_PHRASES.get(axis.axis_id)
    if allowed_labels:
        scored = [item for item in scored if item[0] in allowed_labels]
    selected: List[Tuple[str, str, float]] = list(scored[:max_tags])

    # Keep prioritized technical/specialized phrases where evidence exists.
    priority_labels = AXIS_PRIORITY_PHRASES.get(axis.axis_id, ())
    if priority_labels:
        scored_by_label = {item[0]: item for item in scored}
        selected_labels = {item[0] for item in selected}
        for label in priority_labels:
            candidate = scored_by_label.get(label)
            if candidate is None:
                continue
            if candidate[0] in selected_labels:
                continue
            if len(selected) < max_tags:
                selected.append(candidate)
                selected_labels.add(candidate[0])
                continue
            if selected:
                replacement_index = None
                for idx in range(len(selected) - 1, -1, -1):
                    if selected[idx][0] not in priority_labels:
                        replacement_index = idx
                        break
                if replacement_index is None:
                    replacement_index = len(selected) - 1
                replaced_label = selected[replacement_index][0]
                selected[replacement_index] = candidate
                selected_labels.discard(replaced_label)
                selected_labels.add(candidate[0])

    if len(selected) < min_tags:
        existing_en = {item[0] for item in selected}
        for en_label, fr_label, _ in axis.phrase_bank:
            if len(selected) >= min_tags:
                break
            if allowed_labels and en_label not in allowed_labels:
                continue
            if en_label in existing_en:
                continue
            selected.append((en_label, fr_label, 0.0))
            existing_en.add(en_label)

    selected = selected[:max_tags]
    selected.sort(key=lambda item: item[2], reverse=True)

    tags_en = [item[0] for item in selected]
    tags_fr = [item[1] for item in selected]
    return tags_en, tags_fr


def rank_axis_highlight_candidates(
    axis: AxisDefinition,
    documents: Sequence[dict],
    axis_mapped_faculty: Dict[AxisId, List[str]],
    highlight_years: int = 0,
) -> List[dict]:
    current_year = datetime.date.today().year
    min_year: Optional[int] = None
    if highlight_years > 0:
        min_year = current_year - highlight_years + 1

    mapped_faculty = {
        normalize_person_name(name)
        for name in axis_mapped_faculty.get(axis.axis_id, [])
    }
    phrase_signals = {en_label: signals for en_label, _, signals in axis.phrase_bank}

    candidates: List[dict] = []
    for doc in documents:
        year = doc.get("year")
        if min_year is not None and (year is None or int(year) < min_year):
            continue

        matched_faculty = list(doc.get("matched_faculty_names", []))
        if not matched_faculty:
            continue
        has_target_faculty = any(faculty in HIGHLIGHT_TARGET_FACULTY for faculty in matched_faculty)

        focus_tokens = list(doc.get("title_tokens", [])) + list(doc.get("abstract_tokens", []))
        if not focus_tokens:
            continue

        focus_counts = Counter(focus_tokens)
        axis_raw = sum(focus_counts.get(token, 0) for token in axis.core_tokens)
        if axis_raw < 1 and not has_target_faculty:
            continue

        other_best = max(
            (
                sum(focus_counts.get(token, 0) for token in other_axis.core_tokens)
                for other_axis in AXES
                if other_axis.axis_id != axis.axis_id
            ),
            default=0,
        )
        if axis_raw + 1 < other_best and not has_target_faculty:
            continue

        phrase_overlap = 0
        for signals in phrase_signals.values():
            phrase_overlap = max(phrase_overlap, sum(focus_counts.get(token, 0) for token in signals))

        recency_bonus = 0.0
        if isinstance(year, int):
            recency_bonus = max(0.0, min(0.5, 0.08 * (int(year) - (current_year - 6))))

        student_bonus = 0.5 if doc.get("has_student_author", False) else 0.0
        mapped_bonus = 0.45 if any(faculty in mapped_faculty for faculty in matched_faculty) else 0.0
        base_score = axis_raw + (0.45 * phrase_overlap) + recency_bonus + student_bonus + mapped_bonus

        raw_meta = doc.get("raw_meta", {})
        title = strip_latex_markup(raw_meta.get("title", "")).strip()
        if not title:
            continue

        for faculty in matched_faculty:
            target_bonus = 0.8 if faculty in HIGHLIGHT_TARGET_FACULTY else 0.0
            candidates.append(
                {
                    "score": base_score + target_bonus,
                    "axis_id": axis.axis_id,
                    "path": doc.get("path", ""),
                    "primary_faculty": faculty,
                    "all_faculty": matched_faculty,
                    "title": title,
                    "names": raw_meta.get("names", "").strip(),
                    "venue": normalize_display_venue(raw_meta.get("venue", "")),
                    "link": raw_meta.get("link", "").strip(),
                    "year": year,
                }
            )

    candidates.sort(key=lambda item: item["score"], reverse=True)
    return candidates


def select_highlights_for_all_axes(
    documents: Sequence[dict],
    axis_mapped_faculty: Dict[AxisId, List[str]],
    max_highlights: int = 3,
    min_highlights: int = 2,
    highlight_years: int = 2,
) -> Dict[AxisId, List[dict]]:
    candidates_by_axis: Dict[AxisId, List[dict]] = {
        axis.axis_id: rank_axis_highlight_candidates(
            axis,
            documents,
            axis_mapped_faculty=axis_mapped_faculty,
            highlight_years=highlight_years,
        )
        for axis in AXES
    }

    selected: Dict[AxisId, List[dict]] = {axis.axis_id: [] for axis in AXES}
    used_paths: Set[str] = set()
    used_faculty: Set[str] = set()
    used_faculty_any: Set[str] = set()

    def add_candidate(candidate: dict) -> None:
        axis_id = candidate["axis_id"]
        selected[axis_id].append(
            {
                "title": candidate["title"],
                "names": candidate["names"],
                "venue": candidate["venue"],
                "link": candidate["link"],
                "year": candidate["year"],
            }
        )
        used_paths.add(candidate["path"])
        used_faculty.add(candidate["primary_faculty"])
        for faculty_name in candidate.get("all_faculty", []):
            used_faculty_any.add(faculty_name)

    # Seed highlights with requested faculty where possible.
    for faculty_name in HIGHLIGHT_TARGET_FACULTY_ORDER:
        if faculty_name in used_faculty:
            continue
        best_candidate = None
        for axis in AXES:
            axis_id = axis.axis_id
            if len(selected[axis_id]) >= max_highlights:
                continue
            for candidate in candidates_by_axis.get(axis_id, []):
                if candidate["primary_faculty"] != faculty_name:
                    continue
                if candidate["path"] in used_paths:
                    continue
                if best_candidate is None or candidate["score"] > best_candidate["score"]:
                    best_candidate = candidate
                break
        if best_candidate is not None:
            add_candidate(best_candidate)

    def try_fill(target_count: int, enforce_unique_faculty: bool) -> bool:
        progress = False
        for axis in AXES:
            axis_id = axis.axis_id
            while len(selected[axis_id]) < target_count:
                picked = None
                for candidate in candidates_by_axis.get(axis_id, []):
                    if candidate["path"] in used_paths:
                        continue
                    if enforce_unique_faculty and candidate["primary_faculty"] in used_faculty:
                        continue
                    if enforce_unique_faculty and set(candidate.get("all_faculty", [])).intersection(used_faculty_any):
                        continue
                    picked = candidate
                    break

                if picked is None:
                    break

                add_candidate(picked)
                progress = True

        return progress

    # First pass: enforce one highlighted paper per faculty globally.
    while try_fill(min_highlights, enforce_unique_faculty=True):
        pass
    while try_fill(max_highlights, enforce_unique_faculty=True):
        pass

    # Fallback pass: if needed, allow faculty repeats before leaving empty slots.
    while try_fill(min_highlights, enforce_unique_faculty=False):
        pass
    while try_fill(max_highlights, enforce_unique_faculty=False):
        pass

    return selected


def build_output(
    documents: Sequence[dict],
    highlight_documents: Sequence[dict],
    all_documents_count: int,
    selection_summary: Dict[str, object],
    axis_docs: Dict[AxisId, List[dict]],
    diagnostics: Dict[str, dict],
    axis_bio_token_boosts: Dict[AxisId, Counter],
    axis_mapped_faculty: Dict[AxisId, List[str]],
    min_share: float,
    min_hits: int,
    min_tags: int,
    max_tags: int,
) -> dict:
    output = {
        "generated_at": datetime.date.today().isoformat(),
        "source_publication_count": all_documents_count,
        "selected_publication_count": len(documents),
        "matching": {
            "method": "weighted multi-axis relevance (recent faculty publications + faculty bios, CECD bilingual vocabulary)",
            "thresholds": {
                "min_share": min_share,
                "min_hits": min_hits,
                "min_tags": min_tags,
                "max_tags": max_tags,
            },
            "selection": selection_summary,
            "axis_mapped_faculty": axis_mapped_faculty,
            "highlight_selection": {
                "min_per_axis": 2,
                "max_per_axis": 3,
                "highlight_years": 2,
                "global_unique_faculty": True,
                "preferred_faculty": list(HIGHLIGHT_TARGET_FACULTY_ORDER),
            },
            "axis_document_counts": {axis.axis_id: len(axis_docs[axis.axis_id]) for axis in AXES},
            "sample_assignments": [],
        },
        "axes": {},
    }

    highlights_by_axis = select_highlights_for_all_axes(
        highlight_documents,
        axis_mapped_faculty=axis_mapped_faculty,
        highlight_years=2,
    )

    for axis in AXES:
        tags_en, tags_fr = pick_axis_phrases(
            axis,
            documents,
            min_tags=min_tags,
            max_tags=max_tags,
            axis_bio_token_boosts=axis_bio_token_boosts,
        )
        highlights = highlights_by_axis.get(axis.axis_id, [])
        axis_entry: dict = {
            "tags_en": tags_en,
            "tags_fr": tags_fr,
        }
        if highlights:
            axis_entry["highlight_papers"] = highlights
        output["axes"][axis.axis_id] = axis_entry

    for path in sorted(diagnostics.keys())[:6]:
        output["matching"]["sample_assignments"].append(
            {
                "path": path,
                "assigned_axes": diagnostics[path]["assigned_axes"],
                "relevance": diagnostics[path]["relevance"],
            }
        )

    return output


def write_yaml(data: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    yaml = YAML()
    yaml.default_flow_style = False
    yaml.indent(mapping=2, sequence=4, offset=2)
    with output_path.open("w", encoding="utf-8") as file_handle:
        yaml.dump(data, file_handle)


def main(
    posts_dir: str = "_posts/papers",
    authors_path: str = "_data/authors.yml",
    faculty_axis_map_path: str = "_data/faculty_axis_map.yml",
    output_path: str = "_data/research_axis_topics.yml",
    recent_years: int = 4,
    faculty_only: bool = True,
    min_share: float = 0.24,
    min_hits: int = 2,
    min_tags: int = 4,
    max_tags: int = 4,
) -> None:
    (
        faculty_full_names,
        faculty_last_names,
        faculty_bio_by_full_name,
        faculty_bio_by_last_name,
        student_full_names,
        student_last_names,
    ) = load_faculty_name_sets(Path(authors_path))
    all_docs = build_documents(
        Path(posts_dir),
        faculty_full_names=faculty_full_names,
        faculty_last_names=faculty_last_names,
        faculty_bio_by_full_name=faculty_bio_by_full_name,
        faculty_bio_by_last_name=faculty_bio_by_last_name,
        student_full_names=student_full_names,
        student_last_names=student_last_names,
    )
    docs, selection_summary = filter_documents(all_docs, recent_years=recent_years, faculty_only=faculty_only)
    axis_bio_token_boosts, axis_mapped_faculty = load_faculty_axis_map(
        Path(faculty_axis_map_path),
        faculty_bio_by_full_name=faculty_bio_by_full_name,
    )
    if not docs:
        raise RuntimeError(
            "No publications matched the topic modeling filters. "
            "Adjust --recent_years or pass --include_all_authors."
        )
    axis_docs, diagnostics = assign_documents_to_axes(docs, min_share=min_share, min_hits=min_hits)
    output = build_output(
        documents=docs,
        highlight_documents=all_docs,
        all_documents_count=len(all_docs),
        selection_summary=selection_summary,
        axis_docs=axis_docs,
        diagnostics=diagnostics,
        axis_bio_token_boosts=axis_bio_token_boosts,
        axis_mapped_faculty=axis_mapped_faculty,
        min_share=min_share,
        min_hits=min_hits,
        min_tags=min_tags,
        max_tags=max_tags,
    )
    write_yaml(output, Path(output_path))
    print(f"Wrote axis topics to {output_path} from {len(docs)} publication files.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--posts_dir", default="_posts/papers")
    parser.add_argument("--authors_path", default="_data/authors.yml")
    parser.add_argument("--faculty_axis_map_path", default="_data/faculty_axis_map.yml")
    parser.add_argument("--output_path", default="_data/research_axis_topics.yml")
    parser.add_argument("--recent_years", default=4, type=int)
    parser.add_argument("--include_all_authors", action="store_true")
    parser.add_argument("--min_share", default=0.24, type=float)
    parser.add_argument("--min_hits", default=2, type=int)
    parser.add_argument("--min_tags", default=4, type=int)
    parser.add_argument("--max_tags", default=4, type=int)
    args = parser.parse_args()
    args.faculty_only = not args.include_all_authors
    del args.include_all_authors
    main(**vars(args))

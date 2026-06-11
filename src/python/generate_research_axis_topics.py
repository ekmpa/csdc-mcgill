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
            "education",
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
            "digital",
            "online",
            "ai",
        },
        phrase_bank=(
            ("Citizen identity", "Identite citoyenne", {"identity", "citizenship", "community"}),
            ("Political trust", "Confiance politique", {"trust", "institution", "political"}),
            ("Social cohesion", "Cohesion sociale", {"social", "cohesion", "community"}),
            ("Information literacy", "Competences informationnelles", {"information", "literacy", "media"}),
            ("Civic learning", "Apprentissage civique", {"civic", "learning", "citizenship"}),
            ("Educational inequality", "Inegalites educatives", {"education", "inequality", "student"}),
            (
                "Digital civic literacy",
                "Litteratie civique numerique",
                {"digital", "media", "literacy", "information", "civic"},
            ),
            (
                "AI literacy and trust",
                "Litteratie en IA et confiance",
                {"ai", "literacy", "trust", "information", "citizenship"},
            ),
            (
                "Online political socialization",
                "Socialisation politique en ligne",
                {"online", "information", "youth", "learning", "community"},
            ),
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
            "opinion",
            "information",
            "media",
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
            "ai",
            "algorithmic",
            "deepfake",
            "synthetic",
            "generative",
            "platform",
            "perception",
        },
        phrase_bank=(
            ("Information consumption", "Consommation de l'information", {"information", "media", "news"}),
            ("Opinion formation", "Formation des opinions politiques", {"opinion", "attitude", "political"}),
            ("Citizen participation", "Participation citoyenne", {"participation", "citizenship", "engagement"}),
            ("Partisan polarization", "Polarisation partisane", {"partisan", "polarization", "party"}),
            ("Electoral behavior", "Comportement electoral", {"electoral", "vote", "voting"}),
            ("Public deliberation", "Deliberation publique", {"public", "deliberation", "debate"}),
            (
                "Misinformation and fact-checking",
                "Desinformation et verification des faits",
                {"misinformation", "disinformation", "fact", "checking", "verification", "rumor", "rumour"},
            ),
            (
                "AI and deepfake detection",
                "IA et detection des hypertrucages",
                {"ai", "deepfake", "synthetic", "generative", "detection", "media"},
            ),
            (
                "Public perceptions of AI",
                "Perceptions publiques de l'IA",
                {"public", "perception", "attitude", "ai", "algorithmic", "trust"},
            ),
        ),
    ),
    AxisDefinition(
        axis_id="axis_3",
        title_en="Citizen Representation and Governance",
        title_fr="La representation des citoyens et la gouvernance",
        core_tokens={
            "representation",
            "governance",
            "institution",
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
            "platform",
            "regulation",
            "accountability",
            "algorithmic",
            "ai",
            "digital",
        },
        phrase_bank=(
            ("Citizen-institution relations", "Relation citoyens-institutions", {"citizen", "institution", "trust"}),
            ("Parliamentary institutions", "Institutions parlementaires", {"parliament", "legislative", "institution"}),
            ("Government responsiveness", "Reactivite des gouvernements", {"government", "responsiveness", "policy"}),
            ("Political representation", "Representation politique", {"representation", "party", "electoral"}),
            ("Democratic governance", "Gouvernance democratique", {"governance", "democratic", "government"}),
            ("Electoral systems", "Systemes electoraux", {"electoral", "system", "institution"}),
            (
                "Platform governance and regulation",
                "Gouvernance et regulation des plateformes",
                {"platform", "regulation", "policy", "governance", "institution"},
            ),
            (
                "Algorithmic accountability",
                "Responsabilite algorithmique",
                {"algorithmic", "accountability", "ai", "governance", "regulation"},
            ),
            (
                "Digital platform accountability",
                "Responsabilite numerique des plateformes",
                {"digital", "platform", "accountability", "governance", "regulation"},
            ),
            (
                "AI governance and institutions",
                "Gouvernance de l'IA et institutions",
                {"ai", "governance", "institution", "regulation", "policy"},
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
    "axis_2": (
        "Misinformation and fact-checking",
        "AI and deepfake detection",
        "Public perceptions of AI",
    ),
    "axis_3": (
        "Platform governance and regulation",
        "Algorithmic accountability",
    ),
}

AXIS_ALLOWED_PHRASES: Dict[AxisId, Set[str]] = {
    "axis_1": {
        "Digital civic literacy",
        "AI literacy and trust",
        "Information literacy",
        "Online political socialization",
        "Political trust",
    },
    "axis_2": {
        "Misinformation and fact-checking",
        "AI and deepfake detection",
        "Public perceptions of AI",
        "Information consumption",
        "Opinion formation",
    },
    "axis_3": {
        "Platform governance and regulation",
        "Algorithmic accountability",
        "Digital platform accountability",
        "AI governance and institutions",
        "Democratic governance",
        "Government responsiveness",
        "Political representation",
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


def load_faculty_name_sets(authors_path: Path) -> Tuple[Set[str], Set[str]]:
    if not authors_path.exists():
        return set(), set()

    yaml = YAML(typ="safe")
    authors_data = yaml.load(authors_path.read_text(encoding="utf-8")) or {}

    faculty_full_names: Set[str] = set()
    faculty_last_names: Set[str] = set()

    for _, profile in authors_data.items():
        if not isinstance(profile, dict):
            continue

        current_role = profile.get("current_role", {}) or {}
        role_type = normalize_text(str(current_role.get("type", "") or ""))
        if "faculty" not in role_type and "professor" not in role_type:
            continue

        name = str(profile.get("name", "") or "").strip()
        if not name:
            continue

        normalized_name = normalize_person_name(name)
        if normalized_name:
            faculty_full_names.add(normalized_name)
            last_name = normalized_name.split(" ")[-1]
            if len(last_name) >= 3:
                faculty_last_names.add(last_name)

    return faculty_full_names, faculty_last_names


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

    normalized_names_text = normalize_person_name(names_value)
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
) -> List[dict]:
    documents: List[dict] = []
    faculty_full_names = faculty_full_names or set()
    faculty_last_names = faculty_last_names or set()

    for path in sorted(posts_dir.glob("*.md")):
        data, body = read_front_matter(path)

        title = str(data.get("title", "") or "")
        title_fr = str(data.get("title_fr", "") or "")
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
        has_faculty_author = publication_has_faculty_author(
            names_value,
            faculty_full_names=faculty_full_names,
            faculty_last_names=faculty_last_names,
        )

        title_text = " ".join(part for part in [title, title_fr] if part)
        abstract_text = " ".join(part for part in [abstract, abstract_fr] if part)
        full_text = "\n".join(part for part in [title_text, abstract_text, body, " ".join(clean_tags), names_value] if part)

        documents.append(
            {
                "path": str(path),
                "tokens": tokenize(full_text),
                "title_tokens": tokenize(title_text),
                "abstract_tokens": tokenize(abstract_text),
                "year": publication_year,
                "has_faculty_author": has_faculty_author,
            }
        )

    return documents


def filter_documents(
    documents: Sequence[dict],
    recent_years: int,
    faculty_only: bool,
) -> Tuple[List[dict], Dict[str, object]]:
    current_year = datetime.date.today().year
    min_year: Optional[int] = None
    if recent_years > 0:
        min_year = current_year - recent_years + 1

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


def score_axis_phrase_bank(axis: AxisDefinition, docs: Sequence[dict]) -> List[Tuple[str, str, float]]:
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
) -> Tuple[List[str], List[str]]:
    scored = score_axis_phrase_bank(axis, docs)
    phrase_signals = {en_label: signals for en_label, _, signals in axis.phrase_bank}

    allowed = AXIS_ALLOWED_PHRASES.get(axis.axis_id)
    if allowed:
        scored = [item for item in scored if item[0] in allowed]

    tech_ranked: List[Tuple[str, str, float]] = []
    general_ranked: List[Tuple[str, str, float]] = []
    for item in scored:
        label = item[0]
        signals = phrase_signals.get(label, set())
        if signals.intersection(TECH_ORIENTED_TOKENS):
            tech_ranked.append(item)
        else:
            general_ranked.append(item)

    selected: List[Tuple[str, str, float]] = []
    tech_target = max(0, max_tags - 1)
    selected.extend(tech_ranked[:tech_target])
    if len(selected) < max_tags and general_ranked:
        selected.append(general_ranked[0])
    if len(selected) < max_tags:
        for item in tech_ranked[tech_target:]:
            if len(selected) >= max_tags:
                break
            selected.append(item)

    # Keep prioritized technical/specialized phrases where evidence exists.
    priority_labels = AXIS_PRIORITY_PHRASES.get(axis.axis_id, ())
    if priority_labels:
        selected_labels = {item[0] for item in selected}
        priority_candidates: List[Tuple[str, str, float]] = []
        for item in scored:
            if item[0] in priority_labels:
                priority_candidates.append(item)

        for candidate in priority_candidates:
            if candidate[0] in selected_labels:
                continue
            if len(selected) < max_tags:
                selected.append(candidate)
                selected_labels.add(candidate[0])
                continue
            if selected:
                replacement_index = None
                for idx in range(len(selected) - 1, -1, -1):
                    sel_label = selected[idx][0]
                    sel_signals = phrase_signals.get(sel_label, set())
                    if not sel_signals.intersection(TECH_ORIENTED_TOKENS):
                        replacement_index = idx
                        break
                if replacement_index is None:
                    replacement_index = len(selected) - 1
                selected[replacement_index] = candidate
                selected_labels.add(candidate[0])

    if len(selected) < min_tags:
        existing_en = {item[0] for item in selected}
        for en_label, fr_label, _ in axis.phrase_bank:
            if len(selected) >= min_tags:
                break
            if en_label in existing_en:
                continue
            selected.append((en_label, fr_label, 0.0))
            existing_en.add(en_label)

    selected = selected[:max_tags]
    tags_en = [item[0] for item in selected]
    tags_fr = [item[1] for item in selected]
    return tags_en, tags_fr


def build_output(
    documents: Sequence[dict],
    all_documents_count: int,
    selection_summary: Dict[str, object],
    axis_docs: Dict[AxisId, List[dict]],
    diagnostics: Dict[str, dict],
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
            "method": "weighted multi-axis relevance (recent faculty-focused CECD bilingual vocabulary)",
            "thresholds": {
                "min_share": min_share,
                "min_hits": min_hits,
                "min_tags": min_tags,
                "max_tags": max_tags,
            },
            "selection": selection_summary,
            "axis_document_counts": {axis.axis_id: len(axis_docs[axis.axis_id]) for axis in AXES},
            "sample_assignments": [],
        },
        "axes": {},
    }

    for axis in AXES:
        tags_en, tags_fr = pick_axis_phrases(axis, documents, min_tags=min_tags, max_tags=max_tags)
        output["axes"][axis.axis_id] = {
            "tags_en": tags_en,
            "tags_fr": tags_fr,
        }

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
    output_path: str = "_data/research_axis_topics.yml",
    recent_years: int = 4,
    faculty_only: bool = True,
    min_share: float = 0.24,
    min_hits: int = 2,
    min_tags: int = 4,
    max_tags: int = 4,
) -> None:
    faculty_full_names, faculty_last_names = load_faculty_name_sets(Path(authors_path))
    all_docs = build_documents(
        Path(posts_dir),
        faculty_full_names=faculty_full_names,
        faculty_last_names=faculty_last_names,
    )
    docs, selection_summary = filter_documents(all_docs, recent_years=recent_years, faculty_only=faculty_only)
    if not docs:
        raise RuntimeError(
            "No publications matched the topic modeling filters. "
            "Adjust --recent_years or pass --include_all_authors."
        )
    axis_docs, diagnostics = assign_documents_to_axes(docs, min_share=min_share, min_hits=min_hits)
    output = build_output(
        documents=docs,
        all_documents_count=len(all_docs),
        selection_summary=selection_summary,
        axis_docs=axis_docs,
        diagnostics=diagnostics,
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

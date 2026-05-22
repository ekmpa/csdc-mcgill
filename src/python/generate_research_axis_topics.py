import argparse
import datetime
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Set, Tuple

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
        },
        phrase_bank=(
            ("Citizen identity", "Identite citoyenne", {"identity", "citizenship", "community"}),
            ("Political trust", "Confiance politique", {"trust", "institution", "political"}),
            ("Social cohesion", "Cohesion sociale", {"social", "cohesion", "community"}),
            ("Information literacy", "Competences informationnelles", {"information", "literacy", "media"}),
            ("Civic learning", "Apprentissage civique", {"civic", "learning", "citizenship"}),
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
        },
        phrase_bank=(
            ("Information consumption", "Consommation de l'information", {"information", "media", "news"}),
            ("Opinion formation", "Formation des opinions politiques", {"opinion", "attitude", "political"}),
            ("Citizen participation", "Participation citoyenne", {"participation", "citizenship", "engagement"}),
            ("Partisan polarization", "Polarisation partisane", {"partisan", "polarization", "party"}),
            ("Electoral behavior", "Comportement electoral", {"electoral", "vote", "voting"}),
            ("Public deliberation", "Deliberation publique", {"public", "deliberation", "debate"}),
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
        },
        phrase_bank=(
            ("Citizen-institution relations", "Relation citoyens-institutions", {"citizen", "institution", "trust"}),
            ("Parliamentary institutions", "Institutions parlementaires", {"parliament", "legislative", "institution"}),
            ("Government responsiveness", "Reactivite des gouvernements", {"government", "responsiveness", "policy"}),
            ("Political representation", "Representation politique", {"representation", "party", "electoral"}),
            ("Democratic governance", "Gouvernance democratique", {"governance", "democratic", "government"}),
            ("Electoral systems", "Systemes electoraux", {"electoral", "system", "institution"}),
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
}


AXIS_BY_ID: Dict[AxisId, AxisDefinition] = {axis.axis_id: axis for axis in AXES}


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
    words = re.findall(r"[a-z]{3,}", normalize_text(text))
    normalized = [TOKEN_NORMALIZATION.get(word, word) for word in words]
    return [word for word in normalized if word not in STOPWORDS and word not in NOISE_TERMS]


def read_front_matter(path: Path) -> Tuple[dict, str]:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}, ""

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    yaml_text = parts[1]
    body_text = parts[2]
    yaml = YAML(typ="safe")
    data = yaml.load(yaml_text) or {}
    return data, body_text


def normalize_tag(value: str) -> str:
    return re.sub(r"\s+", " ", str(value).strip())


def build_documents(posts_dir: Path) -> List[dict]:
    documents: List[dict] = []

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

        title_text = " ".join(part for part in [title, title_fr] if part)
        abstract_text = " ".join(part for part in [abstract, abstract_fr] if part)
        full_text = "\n".join(part for part in [title_text, abstract_text, body, " ".join(clean_tags)] if part)

        documents.append(
            {
                "path": str(path),
                "tokens": tokenize(full_text),
                "title_tokens": tokenize(title_text),
                "abstract_tokens": tokenize(abstract_text),
            }
        )

    return documents


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

    for doc in docs:
        weight = max(0.25, doc["axis_relevance"].get(axis.axis_id, 0.0))
        for token, freq in Counter(doc["tokens"]).items():
            weighted_tokens[token] += freq * weight
        for token, freq in Counter(doc["title_tokens"]).items():
            weighted_title_tokens[token] += freq * weight

    scores: List[Tuple[str, str, float]] = []
    for en_label, fr_label, signals in axis.phrase_bank:
        signal_score = sum(weighted_tokens.get(token, 0.0) for token in signals)
        title_bonus = 0.4 * sum(weighted_title_tokens.get(token, 0.0) for token in signals)
        deterministic_tie_breaker = 1e-6 * len(en_label)
        scores.append((en_label, fr_label, signal_score + title_bonus + deterministic_tie_breaker))

    scores.sort(key=lambda item: item[2], reverse=True)
    return scores


def pick_axis_phrases(
    axis: AxisDefinition,
    docs: Sequence[dict],
    min_tags: int,
    max_tags: int,
) -> Tuple[List[str], List[str]]:
    scored = score_axis_phrase_bank(axis, docs)
    selected = scored[:max_tags]

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
    axis_docs: Dict[AxisId, List[dict]],
    diagnostics: Dict[str, dict],
    min_share: float,
    min_hits: int,
    min_tags: int,
    max_tags: int,
) -> dict:
    output = {
        "generated_at": datetime.date.today().isoformat(),
        "source_publication_count": len(documents),
        "matching": {
            "method": "weighted multi-axis relevance (CECD-aligned bilingual vocabulary)",
            "thresholds": {
                "min_share": min_share,
                "min_hits": min_hits,
                "min_tags": min_tags,
                "max_tags": max_tags,
            },
            "axis_document_counts": {axis.axis_id: len(axis_docs[axis.axis_id]) for axis in AXES},
            "sample_assignments": [],
        },
        "axes": {},
    }

    for axis in AXES:
        tags_en, tags_fr = pick_axis_phrases(axis, axis_docs[axis.axis_id], min_tags=min_tags, max_tags=max_tags)
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
    output_path: str = "_data/research_axis_topics.yml",
    min_share: float = 0.24,
    min_hits: int = 2,
    min_tags: int = 3,
    max_tags: int = 4,
) -> None:
    docs = build_documents(Path(posts_dir))
    axis_docs, diagnostics = assign_documents_to_axes(docs, min_share=min_share, min_hits=min_hits)
    output = build_output(
        documents=docs,
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
    parser.add_argument("--output_path", default="_data/research_axis_topics.yml")
    parser.add_argument("--min_share", default=0.24, type=float)
    parser.add_argument("--min_hits", default=2, type=int)
    parser.add_argument("--min_tags", default=3, type=int)
    parser.add_argument("--max_tags", default=4, type=int)
    args = parser.parse_args()
    main(**vars(args))

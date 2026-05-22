import argparse
import datetime
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path

from ruamel.yaml import YAML


AXIS_KEYWORDS = {
    "axis_1": {
        "tokens": {
            "learning",
            "education",
            "educational",
            "school",
            "schools",
            "student",
            "students",
            "teaching",
            "classroom",
            "inequality",
            "inequalities",
            "equity",
            "social",
            "mobility",
            "youth",
            "young",
            "apprendre",
            "education",
            "ecole",
            "ecoles",
            "eleve",
            "eleves",
            "inegalite",
            "inegalites",
            "jeunesse",
            "jeunes",
        }
    },
    "axis_2": {
        "tokens": {
            "practice",
            "practices",
            "participation",
            "participatory",
            "civic",
            "citizenship",
            "engagement",
            "collective",
            "mobilization",
            "mobilisation",
            "activism",
            "protest",
            "deliberation",
            "debate",
            "public",
            "pratique",
            "participation",
            "civique",
            "citoyennete",
            "engagement",
            "mobilisation",
            "deliberation",
            "debat",
        }
    },
    "axis_3": {
        "tokens": {
            "representation",
            "representative",
            "governance",
            "government",
            "policy",
            "policies",
            "institution",
            "institutions",
            "parliament",
            "legislative",
            "election",
            "electoral",
            "party",
            "parties",
            "state",
            "trust",
            "gouvernance",
            "representation",
            "institution",
            "institutions",
            "election",
            "electoral",
            "gouvernement",
            "politique",
        }
    },
}


AXIS_DEFAULTS = {
    "axis_1": {
        "tags_en": [
            "Civic learning",
            "Social inequality",
            "Youth development",
            "Education pathways",
        ],
        "tags_fr": [
            "Apprentissage civique",
            "Inegalites sociales",
            "Developpement des jeunes",
            "Parcours educatifs",
        ],
    },
    "axis_2": {
        "tags_en": [
            "Civic participation",
            "Democratic engagement",
            "Public deliberation",
            "Collective action",
        ],
        "tags_fr": [
            "Participation civique",
            "Engagement democratique",
            "Deliberation publique",
            "Action collective",
        ],
    },
    "axis_3": {
        "tags_en": [
            "Political representation",
            "Democratic governance",
            "Electoral institutions",
            "Institutional trust",
        ],
        "tags_fr": [
            "Representation politique",
            "Gouvernance democratique",
            "Institutions electorales",
            "Confiance institutionnelle",
        ],
    },
}


AXIS_PHRASE_BANK = {
    "axis_1": [
        ("Civic learning", "Apprentissage civique", {"civic", "learning", "citizenship", "education"}),
        ("Social inequality", "Inegalites sociales", {"social", "inequality", "equity"}),
        ("Youth development", "Developpement des jeunes", {"youth", "student", "young"}),
        ("Education pathways", "Parcours educatifs", {"education", "learning", "school"}),
        ("Identity formation", "Construction identitaire", {"identity", "social", "youth"}),
        ("Community belonging", "Appartenance communautaire", {"community", "social", "citizenship"}),
    ],
    "axis_2": [
        ("Civic participation", "Participation civique", {"civic", "participation", "citizenship"}),
        ("Democratic engagement", "Engagement democratique", {"democratic", "engagement", "citizenship"}),
        ("Public deliberation", "Deliberation publique", {"public", "deliberation", "debate"}),
        ("Collective action", "Action collective", {"collective", "mobilization", "activism"}),
        ("Partisan polarization", "Polarisation partisane", {"partisan", "polarization", "party"}),
        ("Political attitudes", "Attitudes politiques", {"political", "public", "democratic"}),
    ],
    "axis_3": [
        ("Political representation", "Representation politique", {"political", "representation", "party"}),
        ("Democratic governance", "Gouvernance democratique", {"democratic", "governance", "government"}),
        ("Electoral institutions", "Institutions electorales", {"electoral", "election", "institution"}),
        ("Institutional trust", "Confiance institutionnelle", {"institution", "trust", "government"}),
        ("Election integrity", "Integrite electorale", {"election", "electoral", "democratic"}),
        ("Policy compliance", "Conformite aux politiques", {"policy", "compliance", "government"}),
    ],
}


NOISE_TERMS = {
    "supplementary",
    "dataset",
    "data",
    "static",
    "stats",
    "cgan",
    "zenodo",
    "metric",
    "waveform",
    "inversion",
    "sensor",
    "branch",
    "synchronous",
    "prediction",
    "therapy",
    "antiretroviral",
}


TOKEN_NORMALIZATION = {
    "citoyennete": "citizenship",
    "civique": "civic",
    "gouvernance": "governance",
    "democratique": "democratic",
    "elections": "election",
    "electorales": "electoral",
    "electorale": "electoral",
    "institutions": "institution",
    "inegalites": "inequality",
    "inegalite": "inequality",
    "jeunes": "youth",
    "jeunesse": "youth",
    "students": "student",
    "schools": "school",
    "parties": "party",
    "policies": "policy",
    "governments": "government",
}


WORD_TRANSLATIONS_FR = {
    "civic": "civique",
    "learning": "apprentissage",
    "social": "sociales",
    "inequality": "inegalites",
    "youth": "jeunesse",
    "development": "developpement",
    "education": "education",
    "pathways": "parcours",
    "participation": "participation",
    "democratic": "democratique",
    "engagement": "engagement",
    "public": "publique",
    "deliberation": "deliberation",
    "collective": "collective",
    "action": "action",
    "political": "politique",
    "representation": "representation",
    "governance": "gouvernance",
    "electoral": "electorales",
    "institution": "institutionnelles",
    "trust": "confiance",
    "polarization": "polarisation",
    "partisan": "partisane",
    "regional": "regionale",
    "regionalism": "regionalisme",
    "democracy": "democratie",
    "citizenship": "citoyennete",
    "backsliding": "recul",
}


STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "for",
    "of",
    "to",
    "in",
    "on",
    "at",
    "from",
    "by",
    "with",
    "without",
    "we",
    "our",
    "this",
    "that",
    "these",
    "those",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "as",
    "it",
    "its",
    "their",
    "they",
    "them",
    "you",
    "your",
    "about",
    "across",
    "into",
    "between",
    "during",
    "through",
    "using",
    "use",
    "new",
    "can",
    "could",
    "would",
    "should",
    "may",
    "might",
    "also",
    "more",
    "most",
    "than",
    "such",
    "based",
    "within",
    "toward",
    "towards",
    "under",
    "over",
    "de",
    "la",
    "le",
    "les",
    "des",
    "du",
    "dans",
    "sur",
    "pour",
    "par",
    "avec",
    "sans",
    "entre",
    "chez",
    "nous",
    "vous",
    "ils",
    "elles",
    "est",
    "sont",
    "ete",
    "etre",
    "au",
    "aux",
    "ce",
    "cet",
    "cette",
    "ces",
    "une",
    "un",
    "d",
    "l",
    "et",
    "ou",
    "qui",
    "que",
    "dont",
    "mais",
    "plus",
    "moins",
    "tout",
    "tous",
    "toutes",
    "notre",
    "nos",
    "vos",
    "leurs",
}


def normalize_text(text):
    lowered = text.lower()
    lowered = unicodedata.normalize("NFKD", lowered)
    lowered = "".join(ch for ch in lowered if not unicodedata.combining(ch))
    lowered = lowered.replace("\u2019", "'")
    lowered = lowered.replace("\u2018", "'")
    lowered = lowered.replace("\u2013", "-")
    lowered = lowered.replace("\u2014", "-")
    return lowered


def tokenize(text):
    text = normalize_text(text)
    words = re.findall(r"[a-z]{3,}", text)
    normalized = [TOKEN_NORMALIZATION.get(w, w) for w in words]
    return [w for w in normalized if w not in STOPWORDS and w not in NOISE_TERMS]


def read_front_matter(path):
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


def normalize_tag(value):
    if not value:
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def split_sentences(text):
    return [s.strip() for s in re.split(r"[.!?\n]+", normalize_text(text)) if s.strip()]


def build_documents(posts_dir):
    documents = []
    for path in sorted(posts_dir.glob("*.md")):
        data, body = read_front_matter(path)
        title = data.get("title", "")
        title_fr = data.get("title_fr", "")
        abstract = data.get("abstract", "")
        abstract_fr = data.get("abstract_fr", "")
        tags = data.get("tags", []) or []

        clean_tags = []
        for item in tags:
            tag = normalize_tag(item)
            if tag and tag not in {"_No response_", "_Unavailable_"}:
                clean_tags.append(tag)

        text_parts = [title, title_fr, abstract, abstract_fr, body, " ".join(clean_tags)]
        full_text = "\n".join([str(p) for p in text_parts if p])
        tokens = tokenize(full_text)

        title_text = " ".join([str(p) for p in [title, title_fr] if p])
        abstract_text = " ".join([str(p) for p in [abstract, abstract_fr] if p])
        title_tokens = tokenize(title_text)
        abstract_tokens = tokenize(abstract_text)
        documents.append(
            {
                "path": str(path),
                "tokens": tokens,
                "title_tokens": title_tokens,
                "abstract_tokens": abstract_tokens,
                "title_sentences": split_sentences(title_text),
                "abstract_sentences": split_sentences(abstract_text),
            }
        )

    return documents


def assign_axis(doc_tokens):
    scores = {}
    token_counter = Counter(doc_tokens)
    for axis_key, axis_data in AXIS_KEYWORDS.items():
        axis_terms = axis_data["tokens"]
        score = sum(token_counter.get(term, 0) for term in axis_terms)
        scores[axis_key] = score

    best_axis = max(scores, key=scores.get)
    if scores[best_axis] == 0:
        return None
    return best_axis


def axis_scores_for_doc(doc_tokens):
    token_counter = Counter(doc_tokens)
    raw_scores = {}
    for axis_key, axis_data in AXIS_KEYWORDS.items():
        axis_terms = axis_data["tokens"]
        raw_scores[axis_key] = sum(token_counter.get(term, 0) for term in axis_terms)

    total = sum(raw_scores.values())
    if total == 0:
        normalized = {"axis_1": 0.0, "axis_2": 0.0, "axis_3": 0.0}
    else:
        normalized = {k: raw_scores[k] / total for k in raw_scores}

    return raw_scores, normalized


def assign_axes_with_weights(documents, min_share=0.24, min_hits=2):
    axis_docs = {"axis_1": [], "axis_2": [], "axis_3": []}
    diagnostics = {}

    for doc in documents:
        raw_scores, normalized_scores = axis_scores_for_doc(doc["tokens"])
        doc["axis_raw_scores"] = raw_scores
        doc["axis_relevance"] = normalized_scores

        chosen_axes = []
        for axis_key in ("axis_1", "axis_2", "axis_3"):
            if raw_scores[axis_key] >= min_hits and normalized_scores[axis_key] >= min_share:
                axis_docs[axis_key].append(doc)
                chosen_axes.append(axis_key)

        # Fallback: if a document has axis signals but misses thresholds, still assign best axis.
        if not chosen_axes and sum(raw_scores.values()) > 0:
            best_axis = max(raw_scores, key=raw_scores.get)
            axis_docs[best_axis].append(doc)
            chosen_axes.append(best_axis)

        diagnostics[doc["path"]] = {
            "raw": raw_scores,
            "relevance": {k: round(v, 3) for k, v in normalized_scores.items()},
            "assigned_axes": chosen_axes,
        }

    return axis_docs, diagnostics


def extract_phrases_from_sentence(sentence):
    tokens = tokenize(sentence)
    phrases = []
    for size in (2, 3):
        if len(tokens) < size:
            continue
        for i in range(len(tokens) - size + 1):
            ngram = tokens[i : i + size]
            if any(token in NOISE_TERMS for token in ngram):
                continue
            if not any(len(token) > 3 for token in ngram):
                continue
            phrases.append(" ".join(ngram))
    return phrases


def phrase_matches_axis(phrase, axis_key):
    phrase_tokens = set(phrase.split())
    return len(phrase_tokens.intersection(AXIS_KEYWORDS[axis_key]["tokens"])) > 0


def score_phrases_by_axis(axis_docs, all_docs):
    phrase_df = Counter()
    doc_phrases = []

    for doc in all_docs:
        phrases = set()
        for sentence in doc["title_sentences"] + doc["abstract_sentences"]:
            for phrase in extract_phrases_from_sentence(sentence):
                phrases.add(phrase)
        doc_phrases.append(phrases)
        for phrase in phrases:
            phrase_df[phrase] += 1

    axis_scores = {"axis_1": Counter(), "axis_2": Counter(), "axis_3": Counter()}
    total_docs = max(1, len(all_docs))

    for axis_key, docs in axis_docs.items():
        if not docs:
            continue

        axis_paths = {doc["path"] for doc in docs}
        for doc, phrases in zip(all_docs, doc_phrases):
            if doc["path"] not in axis_paths:
                continue

            for phrase in phrases:
                if not phrase_matches_axis(phrase, axis_key):
                    continue

                idf = math.log((total_docs + 1) / (phrase_df[phrase] + 1)) + 1
                # Slightly boost phrases sourced from titles, which are often cleaner.
                title_boost = 1.0
                for sentence in doc["title_sentences"]:
                    if phrase in " ".join(tokenize(sentence)):
                        title_boost = 1.3
                        break
                axis_scores[axis_key][phrase] += idf * title_boost

    return axis_scores


def title_case_phrase(phrase):
    return " ".join(token.capitalize() for token in phrase.split())


def fr_label_from_en_phrase(phrase):
    translated = [WORD_TRANSLATIONS_FR.get(token, token) for token in phrase.split()]
    return " ".join(token.capitalize() for token in translated)


def dedupe_similar_phrases(candidates, max_tags):
    chosen = []
    chosen_sets = []
    for phrase in candidates:
        pset = set(phrase.split())
        if any(len(pset.intersection(other)) >= 2 for other in chosen_sets):
            continue
        chosen.append(phrase)
        chosen_sets.append(pset)
        if len(chosen) >= max_tags:
            break
    return chosen


def score_phrase_bank(axis_docs):
    bank_scores = {"axis_1": [], "axis_2": [], "axis_3": []}

    for axis_key, docs in axis_docs.items():
        weighted_tokens = Counter()
        weighted_title_tokens = Counter()
        for doc in docs:
            relevance_weight = max(0.25, doc.get("axis_relevance", {}).get(axis_key, 0.0))
            for token, freq in Counter(doc["tokens"]).items():
                weighted_tokens[token] += freq * relevance_weight
            for token, freq in Counter(doc.get("title_tokens", [])).items():
                weighted_title_tokens[token] += freq * relevance_weight

        for en_label, fr_label, signal_tokens in AXIS_PHRASE_BANK[axis_key]:
            score = 0.0
            for token in signal_tokens:
                score += weighted_tokens.get(token, 0.0)
                score += 0.4 * weighted_title_tokens.get(token, 0.0)
            # Keep deterministic output even when scores tie.
            bank_scores[axis_key].append((en_label, fr_label, score + 1e-6 * len(en_label)))

        bank_scores[axis_key] = sorted(bank_scores[axis_key], key=lambda x: x[2], reverse=True)

    return bank_scores


def pick_top_tags(axis_phrase_scores, min_tags, max_tags):
    result = {}
    for axis_key, scores in axis_phrase_scores.items():
        ordered = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        phrases = [phrase for phrase, _ in ordered]
        selected = dedupe_similar_phrases(phrases, max_tags=max_tags)

        defaults = [s.lower() for s in AXIS_DEFAULTS[axis_key]["tags_en"]]
        for phrase in defaults:
            if len(selected) >= min_tags:
                break
            if phrase not in selected:
                selected.append(phrase)

        result[axis_key] = selected[:max_tags]

    return result


def build_output(documents, tags_per_axis):
    output = {
        "generated_at": datetime.date.today().isoformat(),
        "source_publication_count": len(documents),
        "axes": {
            "axis_1": {
                "tags_en": [title_case_phrase(t) for t in tags_per_axis.get("axis_1", [])],
                "tags_fr": [fr_label_from_en_phrase(t) for t in tags_per_axis.get("axis_1", [])],
            },
            "axis_2": {
                "tags_en": [title_case_phrase(t) for t in tags_per_axis.get("axis_2", [])],
                "tags_fr": [fr_label_from_en_phrase(t) for t in tags_per_axis.get("axis_2", [])],
            },
            "axis_3": {
                "tags_en": [title_case_phrase(t) for t in tags_per_axis.get("axis_3", [])],
                "tags_fr": [fr_label_from_en_phrase(t) for t in tags_per_axis.get("axis_3", [])],
            },
        },
    }
    return output


def write_yaml(data, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    yaml = YAML()
    yaml.default_flow_style = False
    yaml.indent(mapping=2, sequence=4, offset=2)
    with output_path.open("w", encoding="utf-8") as f:
        yaml.dump(data, f)


def main(
    posts_dir="_posts/papers",
    output_path="_data/research_axis_topics.yml",
    min_tags=3,
    max_tags=4,
):
    posts_dir = Path(posts_dir)
    output_path = Path(output_path)

    documents = build_documents(posts_dir)
    axis_docs, diagnostics = assign_axes_with_weights(documents)

    bank_scores = score_phrase_bank(axis_docs)
    output = {
        "generated_at": datetime.date.today().isoformat(),
        "source_publication_count": len(documents),
        "matching": {
            "method": "weighted multi-axis relevance (bilingual normalized tokens)",
            "axis_document_counts": {
                "axis_1": len(axis_docs["axis_1"]),
                "axis_2": len(axis_docs["axis_2"]),
                "axis_3": len(axis_docs["axis_3"]),
            },
            "thresholds": {
                "min_share": 0.24,
                "min_hits": 2,
            },
        },
        "axes": {},
    }

    for axis_key in ("axis_1", "axis_2", "axis_3"):
        picks = bank_scores[axis_key][:max_tags]
        if len(picks) < min_tags:
            defaults_en = AXIS_DEFAULTS[axis_key]["tags_en"]
            defaults_fr = AXIS_DEFAULTS[axis_key]["tags_fr"]
            existing_en = {item[0] for item in picks}
            for en_tag, fr_tag in zip(defaults_en, defaults_fr):
                if len(picks) >= min_tags:
                    break
                if en_tag in existing_en:
                    continue
                picks.append((en_tag, fr_tag, 0.0))
                existing_en.add(en_tag)

        picks = picks[:max_tags]
        output["axes"][axis_key] = {
            "tags_en": [item[0] for item in picks],
            "tags_fr": [item[1] for item in picks],
        }

    # Keep a compact debug trace for spot-checking assignments.
    output["matching"]["sample_assignments"] = []
    for path in sorted(diagnostics.keys())[:5]:
        output["matching"]["sample_assignments"].append(
            {
                "path": path,
                "assigned_axes": diagnostics[path]["assigned_axes"],
                "relevance": diagnostics[path]["relevance"],
            }
        )

    write_yaml(output, output_path)

    print(f"Wrote axis topics to {output_path} from {len(documents)} publication files.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--posts_dir", default="_posts/papers")
    parser.add_argument("--output_path", default="_data/research_axis_topics.yml")
    parser.add_argument("--min_tags", default=3, type=int)
    parser.add_argument("--max_tags", default=4, type=int)
    args = parser.parse_args()
    main(**vars(args))
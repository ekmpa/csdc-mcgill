"""Keyword gate for Computer Science publication titles.

These terms are used to keep only topic-relevant publications in the
Computer Science department listing on the research pages.
"""

from __future__ import annotations

from typing import Final


CS_RELEVANT_TITLE_TERMS: Final[tuple[str, ...]] = (
    "deepfake",
    "democracy",
    "partisan",
    "polarisation",
    "election",
    "pandemic",
    "social",
    "ai-for-good",
    "responsible ai",
    "information integrity",
    "fact-checking",
    "misinformation",
    "trafficking",
    "abuse",
    "privacy",
    "sexual",
    "campaigns",
    "influence",
    "safety",
    "integrity",
    "epistemic",
    "risks",
    "disinformation",
    "political",
    "societal",
    "toxicity",
    "public",
    "discourse",
    "party",
    "tweet",
    "twitter",
    "reddit",
)


def title_matches_cs_scope(title: str) -> bool:
    """Return True when a title contains at least one CS scope keyword.

    Matching is case-insensitive and uses substring checks.
    """

    normalized = title.lower().replace("–", "-").replace("—", "-")
    return any(term in normalized for term in CS_RELEVANT_TITLE_TERMS)

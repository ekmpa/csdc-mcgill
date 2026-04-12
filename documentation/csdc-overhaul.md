# CSDC Visual + Automation Integration

This document defines how the CSDC visual overhaul is integrated with the existing root automation stack.

## Objective

Use the CSDC visual frontend style while keeping all existing member/publication automations unchanged.

## Visual Layer (safe to modify)

- `_sass/custom/csdc-theme.scss`
- `_includes/csdc-home-hero.html`
- `_includes/csdc-featured-event.html`
- `_includes/csdc-research-pillars.html`
- `_includes/csdc-cta-stats.html`
- `_pages/home.md`
- `_pages/people.md`
- `_sass/custom/people-card.scss`

These files are presentation-only and should not change automation schemas.

## Automation Layer (must remain stable)

### Trigger and workflow contract

- Issue forms are still the entry point for updates: `https://github.com/ekmpa/csdc-mcgill/issues/new/choose`
- Label-trigger routing in `.github/workflows/process-issue-forms.yml` must stay intact.
- Python module command paths in workflows must remain unchanged.

### Data contracts

- Member data source: `_data/authors.yml`
- Publication source: `_posts/papers/*.md`
- Ignore list source: `records/semantic_paper_ids_ignored.json`
- Avatar output path: `assets/images/bio/`

### Scripts that must keep current interface

- `src/python/add_update_member.py`
- `src/python/add_update_publication.py`
- `src/python/add_publication_by_id.py`
- `src/python/auto_update_publications.py`
- `src/python/__init__.py` (notably issue parsing helpers)

## Routing rules

- Keep existing page permalinks stable.
- Keep navigation data in `_data/navigation.yml` as source-of-truth for links.
- Home/People can be visually overhauled without changing update flow URLs.

## Validation checklist

1. `python -m pytest tests/`
2. `bundle exec jekyll build --strict_front_matter`
3. Confirm issue-form URL is visible and reachable from major pages.
4. Confirm member cards still render data from `_data/authors.yml`.
5. Confirm publication pages are generated and accessible after build.

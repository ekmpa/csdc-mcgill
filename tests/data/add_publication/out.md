---
title: My cool paper
author: John Doe
names: John Doe, John Doe Sr, Leland DeWitt
venue: ABC
link: https://example.com/paper
code: https://github.com/McGill-NLP
categories: Publications
title_fr: My cool paper
venue_fr: ABC
abstract_fr: _Unavailable_

---

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


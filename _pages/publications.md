---
title: Publications
layout: splash_v2
excerpt: ""
classes:
    - no-sidebar
    - wide
    - csdc-page
permalink: /publications/
taxonomy: Publications
show_view_by_venue: false
show_taxonomy_posts: false
---

<section class="csdc-section csdc-page-header">
    <div class="csdc-container">
        <h1 id="page-title" class="page__title csdc-page-title">Research</h1>
    </div>
</section>

{% include csdc-research-pillars.html show_publications_link=false show_heading=false %}

<section class="csdc-section">
    <div class="csdc-container">
        <h2>Publications</h2>
        <p class="csdc-page-subtitle">Research outputs by the team's professors and students.</p>
        {% include posts-publication.html taxonomy=page.taxonomy %}
    </div>
</section>

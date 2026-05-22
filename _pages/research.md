---
title: Our Research
layout: splash_v2
permalink: /research/
classes:
  - csdc-page
excerpt: "Research priorities and topic areas at the McGill CSDC."
show_taxonomy_posts: false
---

<div class="csdc-page csdc-research-page">
  <section class="csdc-section csdc-page-header">
    <div class="csdc-container">
      <p class="csdc-kicker"><span class="csdc-red">McGill CSDC</span></p>
      <h1 id="page-title" class="page__title csdc-page-title">Research</h1>
      <p class="csdc-page-subtitle">Our research focuses on democratic citizenship:</p>
    </div>
  </section>

  <section class="csdc-section">
    <div class="csdc-container">
      <div class="csdc-pillars csdc-pillars-two">
        <article class="csdc-card" style="border-top:4px solid #c8102e;">
          <h3 class="csdc-card-title">Learning Democratic Citizenship in an Unequal World</h3>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
        </article>
        <article class="csdc-card" style="border-top:4px solid #c8102e;">
          <h3 class="csdc-card-title">The Practice of Democratic Citizenship</h3>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
        </article>
        <article class="csdc-card" style="border-top:4px solid #c8102e;">
          <h3 class="csdc-card-title">Citizen Representation and Governance</h3>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="csdc-section">
    <div class="csdc-container">
      <h2>Publications</h2>
      <p class="csdc-page-subtitle">Research outputs by the team.</p>
      <hr class="csdc-research-divider">
      {% assign publications = site.posts | where_exp: "post", "post.path contains '_posts/papers/'" %}
      {% if publications and publications.size > 0 %}
      {% assign publication_years = '' | split: '' %}
      {% for post in publications %}
        {% assign post_year = post.date | date: "%Y" %}
        {% unless publication_years contains post_year %}
          {% assign publication_years = publication_years | push: post_year %}
        {% endunless %}
      {% endfor %}

      {% for year in publication_years %}
        {% assign year_publications = '' | split: '' %}
        {% for post in publications %}
          {% assign post_year = post.date | date: "%Y" %}
          {% if post_year == year %}
            {% assign year_publications = year_publications | push: post %}
          {% endif %}
        {% endfor %}

        <h3 class="csdc-research-year-heading">{{ year }} ({{ year_publications.size }})</h3>
        <div class="csdc-pillars csdc-pillars-two">
          {% for post in year_publications %}
          <article class="csdc-card">
            <h4 class="csdc-card-title" style="margin-bottom:0.3rem;"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h4>
            {% if post.names %}<p style="margin:0.2rem 0;">{{ post.names }}</p>{% endif %}
            {% if post.venue %}<p style="margin:0.2rem 0; color:#6b7280;">{{ post.venue }}</p>{% endif %}
            {% if post.link %}<p style="margin:0.35rem 0 0;"><a href="{{ post.link }}" target="_blank" rel="noopener noreferrer">Paper link</a></p>{% endif %}
          </article>
          {% endfor %}
        </div>
      {% endfor %}
      {% else %}
      <div class="csdc-card">
        <p style="margin:0;">No publications submitted yet. Use the footer "Add publication" form to add DOI or URL entries.</p>
      </div>
      {% endif %}
    </div>
  </section>
</div>

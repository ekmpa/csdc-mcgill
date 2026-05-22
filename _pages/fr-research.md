---
title: Recherche
layout: splash_v2
permalink: /fr/research/
classes:
  - csdc-page
excerpt: "Priorités et domaines de recherche du CÉCD McGill."
show_taxonomy_posts: false
---

<div class="csdc-page csdc-research-page">
  <section class="csdc-section csdc-page-header">
    <div class="csdc-container">
      <p class="csdc-kicker"><span class="csdc-red">CÉCD McGill</span></p>
      <h1 id="page-title" class="page__title csdc-page-title">Recherche</h1>
      <p class="csdc-page-subtitle">Nos recherches portent sur la citoyenneté démocratique :</p>
    </div>
  </section>

  <section class="csdc-section">
    <div class="csdc-container">
      <div class="csdc-pillars csdc-pillars-two">
        <article class="csdc-card" style="border-top:4px solid #c8102e;">
          <h3 class="csdc-card-title">Apprendre la citoyenneté démocratique dans un monde inégal</h3>
          <p>Travaux sur les parcours citoyens, les inégalités sociales et les conditions de formation politique.</p>
        </article>
        <article class="csdc-card" style="border-top:4px solid #c8102e;">
          <h3 class="csdc-card-title">La pratique de la citoyenneté démocratique</h3>
          <p>Études sur la participation, l'engagement civique, la délibération et les transformations de la vie démocratique.</p>
        </article>
        <article class="csdc-card" style="border-top:4px solid #c8102e;">
          <h3 class="csdc-card-title">Représentation citoyenne et gouvernance</h3>
          <p>Analyses de la représentation politique, de la confiance institutionnelle et des mécanismes de gouvernance.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="csdc-section">
    <div class="csdc-container">
      <h2>Publications</h2>
      <p class="csdc-page-subtitle">Productions scientifiques à travers le CÉCD McGill.</p>
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
            <p class="csdc-research-paper-year">{{ post.date | date: "%Y" }}</p>
            {% if post.names %}<p style="margin:0.2rem 0;">{{ post.names }}</p>{% endif %}
            {% if post.venue %}<p style="margin:0.2rem 0; color:#6b7280;">{{ post.venue }}</p>{% endif %}
            {% if post.link %}<p style="margin:0.35rem 0 0;"><a href="{{ post.link }}" target="_blank" rel="noopener noreferrer">Lien vers la publication</a></p>{% endif %}
          </article>
          {% endfor %}
        </div>
      {% endfor %}
      {% else %}
      <div class="csdc-card">
        <p style="margin:0;">Aucune publication n'a encore été soumise. Utilisez le formulaire "Ajouter ou mettre à jour une publication" du pied de page pour ajouter des entrées.</p>
      </div>
      {% endif %}
    </div>
  </section>
</div>

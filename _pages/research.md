---
title: Our Research
layout: splash_v2
permalink: /research/
classes:
  - csdc-page
excerpt: "Research priorities and topic areas at the McGill CSDC."
show_taxonomy_posts: false
---

<div class="csdc-page">
  <section class="csdc-hero">
    <div class="csdc-container">
      <p class="csdc-kicker"><span class="csdc-red">McGill Node</span></p>
      <h1 class="csdc-hero-title">Our Research</h1>
      <p class="csdc-lead">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
    </div>
  </section>

  <section class="csdc-section">
    <div class="csdc-container">
      <h2>Three CSDC Research Axes</h2>
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
      <h2>Recent Publications</h2>
      {% assign publications = site.posts | where_exp: "post", "post.path contains '_posts/papers/'" %}
      {% if publications and publications.size > 0 %}
      <div class="csdc-pillars csdc-pillars-two">
        {% for post in publications limit:8 %}
        <article class="csdc-card">
          <h3 class="csdc-card-title" style="margin-bottom:0.3rem;"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
          {% if post.names %}
          <p style="margin:0.2rem 0;">{{ post.names }}</p>
          {% endif %}
          {% if post.venue %}
          <p style="margin:0.2rem 0; color:#6b7280;">{{ post.venue }}</p>
          {% endif %}
          {% if post.link %}
          <p style="margin:0.35rem 0 0;"><a href="{{ post.link }}" target="_blank" rel="noopener noreferrer">Paper link</a></p>
          {% endif %}
        </article>
        {% endfor %}
      </div>
      <p style="margin-top:0.75rem;"><a href="{{ '/publications/' | relative_url }}">&rarr; Browse all publications</a></p>
      {% else %}
      <div class="csdc-card">
        <p style="margin:0;">No publications submitted yet. Use the footer "Add or update publication" form to add entries.</p>
      </div>
      {% endif %}
    </div>
  </section>

  <section class="csdc-section">
    <div class="csdc-container">
      <h2>Member Google Scholar Profiles</h2>
      <div class="csdc-card">
        <ul style="margin:0; padding-left:1.2rem;">
          {% assign scholar_count = 0 %}
          {% for item in site.data.authors %}
            {% assign author = item[1] %}
            {% if author.social_media_links %}
              {% for social in author.social_media_links %}
                {% if social.label == 'Scholar' and social.url and social.url != '' %}
                  {% assign scholar_count = scholar_count | plus: 1 %}
                  <li style="margin:0.25rem 0;"><a href="{{ social.url }}" target="_blank" rel="noopener noreferrer">{{ author.name }}</a></li>
                {% endif %}
              {% endfor %}
            {% endif %}
          {% endfor %}
          {% if scholar_count == 0 %}
          <li>No Google Scholar links provided yet. Members can add one through the profile form.</li>
          {% endif %}
        </ul>
      </div>
    </div>
  </section>
</div>

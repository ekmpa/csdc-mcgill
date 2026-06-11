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

  <section id="research-publications-section" class="csdc-section">
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
      <h2 id="research-publications-heading">Publications</h2>
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
      {% assign publication_years = publication_years | sort | reverse %}

      {% for year in publication_years %}
        {% assign year_publications = '' | split: '' %}
        {% for post in publications %}
          {% assign post_year = post.date | date: "%Y" %}
          {% if post_year == year %}
            {% assign year_publications = year_publications | push: post %}
          {% endif %}
        {% endfor %}

        <section id="research-year-{{ year }}" class="csdc-research-year-section">
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
        </section>
      {% endfor %}

      {% if publication_years.size > 1 %}
      <div class="csdc-year-jump-nav" data-csdc-research-year-jump>
        <button type="button" class="csdc-year-jump-btn" data-csdc-research-year-dir="up" aria-label="Jump to previous year section">
          <span class="csdc-year-jump-arrow">&uarr;</span>
          <span class="csdc-year-jump-label" data-csdc-research-year-label="up">--</span>
        </button>
        <button type="button" class="csdc-year-jump-btn" data-csdc-research-year-dir="down" aria-label="Jump to next year section">
          <span class="csdc-year-jump-arrow">&darr;</span>
          <span class="csdc-year-jump-label" data-csdc-research-year-label="down">--</span>
        </button>
      </div>

      <script>
      (function () {
        if (window.__csdcResearchYearJumpBound) {
          return;
        }
        window.__csdcResearchYearJumpBound = true;

        function extractLabel(section) {
          var heading = section.querySelector('.csdc-research-year-heading');
          if (!heading) {
            return '--';
          }
          var text = (heading.textContent || '').trim();
          var match = text.match(/^([^()]+)/);
          return (match ? match[1] : text).trim() || '--';
        }

        function init() {
          var nav = document.querySelector('[data-csdc-research-year-jump]');
          if (!nav) {
            return;
          }

          var sections = Array.prototype.slice.call(document.querySelectorAll('.csdc-research-page .csdc-research-year-section'));
          if (sections.length < 2) {
            return;
          }
          var firstYearHeading = sections[0].querySelector('.csdc-research-year-heading');
          if (!firstYearHeading) {
            return;
          }

          var upBtn = nav.querySelector('[data-csdc-research-year-dir="up"]');
          var downBtn = nav.querySelector('[data-csdc-research-year-dir="down"]');
          var upLabel = nav.querySelector('[data-csdc-research-year-label="up"]');
          var downLabel = nav.querySelector('[data-csdc-research-year-label="down"]');

          function currentIndex() {
            var pointer = window.scrollY + 170;
            var idx = 0;
            for (var i = 0; i < sections.length; i += 1) {
              if (sections[i].offsetTop <= pointer) {
                idx = i;
              }
            }
            return idx;
          }

          function computeTargets() {
            var idx = currentIndex();
            var currentHeaderTop = sections[idx].offsetTop - 92;
            var upIdx;

            if (idx === 0) {
              upIdx = 0;
            } else if (window.scrollY > currentHeaderTop + 24) {
              upIdx = idx;
            } else {
              upIdx = idx - 1;
            }

            var downIdx = Math.min(sections.length - 1, idx + 1);
            return { idx: idx, upIdx: upIdx, downIdx: downIdx, currentHeaderTop: currentHeaderTop };
          }

          function jumpTo(section) {
            var top = section.getBoundingClientRect().top + window.pageYOffset - 92;
            window.scrollTo({ top: top, behavior: 'smooth' });
          }

          function refresh() {
            var targets = computeTargets();
            var headingTop = firstYearHeading.getBoundingClientRect().top;
            var shouldShow = headingTop <= 92;
            nav.classList.toggle('is-visible', shouldShow);

            upBtn.disabled = targets.idx === 0 && window.scrollY <= targets.currentHeaderTop + 24;
            downBtn.disabled = targets.idx === sections.length - 1;

            upLabel.textContent = extractLabel(sections[targets.upIdx]);
            downLabel.textContent = extractLabel(sections[targets.downIdx]);
          }

          upBtn.addEventListener('click', function () {
            var targets = computeTargets();
            if (!upBtn.disabled) {
              jumpTo(sections[targets.upIdx]);
            }
          });

          downBtn.addEventListener('click', function () {
            var targets = computeTargets();
            if (!downBtn.disabled) {
              jumpTo(sections[targets.downIdx]);
            }
          });

          window.addEventListener('scroll', refresh, { passive: true });
          window.addEventListener('resize', refresh);
          refresh();
        }

        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', init);
        } else {
          init();
        }
      })();
      </script>
      {% endif %}
      {% else %}
      <div class="csdc-card">
        <p style="margin:0;">No publications submitted yet. Use the footer "Add publication" form to add DOI or URL entries.</p>
      </div>
      {% endif %}
    </div>
  </section>
</div>

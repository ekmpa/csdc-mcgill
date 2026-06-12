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
          <h3 class="csdc-research-year-heading">
            <span class="csdc-research-year-label">{{ year }}</span>
            (<span class="csdc-research-year-count" data-total-count="{{ year_publications.size }}">{{ year_publications.size }}</span>)
          </h3>
          <div class="csdc-pillars csdc-pillars-two">
            {% for post in year_publications %}
            <article class="csdc-card">
              <h4 class="csdc-card-title" style="margin-bottom:0.3rem;"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h4>
              {% if post.names %}<p style="margin:0.2rem 0;">{{ post.names }}</p>{% endif %}
              {% if post.venue %}<p style="margin:0.2rem 0; color:#6b7280;">{{ post.venue }}</p>{% endif %}
              {% if post.link %}<p style="margin:0.35rem 0 0;"><a href="{{ post.link }}" target="_blank" rel="noopener noreferrer">Lien vers la publication</a></p>{% endif %}
            </article>
            {% endfor %}
          </div>
        </section>
      {% endfor %}

      {% if publication_years.size > 1 %}
      <div class="csdc-year-jump-nav" data-csdc-research-year-jump>
        <button type="button" class="csdc-year-jump-btn" data-csdc-research-year-dir="up" aria-label="Aller à la section annuelle précédente">
          <span class="csdc-year-jump-arrow">&uarr;</span>
          <span class="csdc-year-jump-label" data-csdc-research-year-label="up">--</span>
        </button>
        <button type="button" class="csdc-year-jump-btn" data-csdc-research-year-dir="down" aria-label="Aller à la section annuelle suivante">
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

          var upBtn = nav.querySelector('[data-csdc-research-year-dir="up"]');
          var downBtn = nav.querySelector('[data-csdc-research-year-dir="down"]');
          var upLabel = nav.querySelector('[data-csdc-research-year-label="up"]');
          var downLabel = nav.querySelector('[data-csdc-research-year-label="down"]');

          function getVisibleSections() {
            return Array.prototype.filter.call(
              document.querySelectorAll('.csdc-research-page .csdc-research-year-section'),
              function (section) {
                return window.getComputedStyle(section).display !== 'none';
              }
            );
          }

          function getSectionTop(section) {
            var heading = section.querySelector('.csdc-research-year-heading');
            if (heading) {
              return heading.getBoundingClientRect().top + window.pageYOffset;
            }
            return section.getBoundingClientRect().top + window.pageYOffset;
          }

          function jumpTo(section) {
            var top = getSectionTop(section) - 92;
            window.scrollTo({ top: top, behavior: 'auto' });
            return top;
          }
          var activeIndex = 0;

          function computeIndexFromScroll(visibleSections, scrollYValue) {
            var idx = 0;
            for (var i = 0; i < visibleSections.length; i += 1) {
              var anchor = getSectionTop(visibleSections[i]) - 92;
              if (anchor <= scrollYValue + 1) {
                idx = i;
              } else {
                break;
              }
            }
            return idx;
          }

          function renderState(visibleSections, index, virtualScrollY) {
            if (!visibleSections.length) {
              nav.classList.remove('is-visible');
              upBtn.disabled = true;
              downBtn.disabled = true;
              upLabel.textContent = '--';
              downLabel.textContent = '--';
              return;
            }

            activeIndex = Math.max(0, Math.min(visibleSections.length - 1, index));
            var effectiveScrollY = typeof virtualScrollY === 'number' ? virtualScrollY : window.scrollY;
            var activeAnchor = getSectionTop(visibleSections[activeIndex]) - 92;
            var nextIndex = Math.min(visibleSections.length - 1, activeIndex + 1);
            upLabel.textContent = extractLabel(visibleSections[activeIndex]);
            downLabel.textContent = extractLabel(visibleSections[nextIndex]);
            upBtn.disabled = activeIndex === 0 && effectiveScrollY <= activeAnchor + 2;
            downBtn.disabled = activeIndex >= visibleSections.length - 1;

            var firstHeading = visibleSections[0].querySelector('.csdc-research-year-heading');
            if (!firstHeading) {
              nav.classList.remove('is-visible');
              return;
            }
            var shouldShow = firstHeading.getBoundingClientRect().top <= 92;
            nav.classList.toggle('is-visible', shouldShow);
          }

          function syncFromScroll() {
            var visibleSections = getVisibleSections();
            if (visibleSections.length < 2) {
              renderState(visibleSections, 0, window.scrollY);
              return;
            }
            var idx = computeIndexFromScroll(visibleSections, window.scrollY);
            renderState(visibleSections, idx, window.scrollY);
          }

          upBtn.addEventListener('click', function () {
            var visibleSections = getVisibleSections();
            if (visibleSections.length < 2) {
              return;
            }

            var currentAnchor = getSectionTop(visibleSections[activeIndex]) - 92;
            var targetIndex = activeIndex;
            if (window.scrollY > currentAnchor + 2) {
              targetIndex = activeIndex;
            } else {
              targetIndex = Math.max(0, activeIndex - 1);
            }

            var targetTop = jumpTo(visibleSections[targetIndex]);
            renderState(visibleSections, targetIndex, targetTop);
          });

          downBtn.addEventListener('click', function () {
            var visibleSections = getVisibleSections();
            if (visibleSections.length < 2) {
              return;
            }

            var targetIndex = Math.min(visibleSections.length - 1, activeIndex + 1);
            var targetTop = jumpTo(visibleSections[targetIndex]);
            renderState(visibleSections, targetIndex, targetTop);
          });

          window.addEventListener('scroll', syncFromScroll, { passive: true });
          window.addEventListener('resize', syncFromScroll);
          document.addEventListener('csdc:research-filter-changed', syncFromScroll);
          syncFromScroll();
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
        <p style="margin:0;">Aucune publication n'a encore été soumise. Utilisez le formulaire "Ajouter ou mettre à jour une publication" du pied de page pour ajouter des entrées.</p>
      </div>
      {% endif %}
    </div>
  </section>
</div>

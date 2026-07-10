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

  <section id="research-publications-section" class="csdc-section csdc-research-axes-section">
    <div class="csdc-container">
      <div class="csdc-pillars csdc-pillars-two">
        <article class="csdc-card" style="border-top:4px solid #c8102e;">
          <h3 class="csdc-card-title">1) Learning Democratic Citizenship in an Unequal World</h3>
          <p>This first axis focuses on the acquisition of values, attitudes and skills that constitute the ingredients of a healthy democracy. Democratic citizenship is based on the feeling of belonging to a political community, trust in the institutions that embody the democratic regime, social cohesion linked to the equality of citizens, as well as the information skills essential to understanding the world. However, several factors influence this learning, as research combining communication, social psychology, computer science, political science and sociology shows.</p>
        </article>
        <article class="csdc-card" style="border-top:4px solid #c8102e;">
          <h3 class="csdc-card-title">2) The Practice of Democratic Citizenship</h3>
          <p>This axis focuses on concrete elements of the practice of citizenship: the production and consumption of information on current events, the formation of opinions on political issues and actors (including partisan preferences and voting intentions), and political participation in all its forms. The research in this axis examines crucial questions about a rapidly changing media ecosystem, partisan misalignment and the polarization of opinions, and inequalities in citizen participation.</p>
        </article>
        <article class="csdc-card csdc-card--research-axis-span" style="border-top:4px solid #c8102e;">
          <h3 class="csdc-card-title">3) Citizen Representation and Governance</h3>
          <p>After learning and practicing democratic citizenship, the next critical steps are representation and governance. Democratic institutions are key elements. They shape the norms and incentives for active citizenship and they link citizens and their representatives in ways that foster accountability, legitimacy and representation. In Québec and Canada, as well as in other countries, confidence of citizens toward the institutions is low, as many dislike the way that members of parliaments behave and consider that politicians don’t honour their promises, hence various political endeavours to reform these institutions. Research on this axis will focus on the role of electoral systems, parliaments, parliamentary debates, and political parties.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="csdc-section">
    <div class="csdc-container">
      <h2 id="research-publications-heading">Publications</h2>
      <p class="csdc-page-subtitle">Research outputs by the team.</p>
      <hr class="csdc-research-divider">
      <form class="search-content__form csdc-research-search-form" role="search" onsubmit="return false;">
        <input type="search" id="research-publications-search" class="search-input csdc-research-search-input" placeholder="Search papers by title, author, venue..." autocomplete="off" aria-label="Search papers" />
      </form>
      <p class="csdc-research-no-results" id="research-publications-empty" hidden>No papers matched your search.</p>
      {% assign all_publications = site.posts | where_exp: "post", "post.path contains '_posts/papers/'" %}
      {% assign publications = '' | split: '' %}
      {% for post in all_publications %}
        {% assign post_year = post.date | date: "%Y" | plus: 0 %}
        {% if post_year >= 2008 %}
          {% assign publications = publications | push: post %}
        {% endif %}
      {% endfor %}
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
              {% assign clean_title = post.title
                | replace: '$$\\textbf{', ''
                | replace: '$$\\textttt{', ''
                | replace: '$$\\texttt{', ''
                | replace: '$$\\textit{', ''
                | replace: '$\\textbf{', ''
                | replace: '$\\textttt{', ''
                | replace: '$\\texttt{', ''
                | replace: '$\\textit{', ''
                | replace: '\\textbf{', ''
                | replace: '\\textttt{', ''
                | replace: '\\texttt{', ''
                | replace: '\\textit{', ''
                | replace: '$$', ''
                | replace: '$', ''
                | replace: '{', ''
                | replace: '}', ''
                | strip %}
              <h4 class="csdc-card-title" style="margin-bottom:0.3rem;"><a href="{{ post.url | relative_url }}">{{ clean_title }}</a></h4>
              {% if post.names %}<p style="margin:0.2rem 0;">{{ post.names }}</p>{% endif %}
              {% if post.venue %}<p style="margin:0.2rem 0; color:#6b7280;">{{ post.venue }}</p>{% endif %}
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
            // Use immediate jumps so repeated button presses always advance year-by-year.
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

      <script>
      (function () {
        if (window.__csdcResearchSearchBound) {
          return;
        }
        window.__csdcResearchSearchBound = true;

        function init() {
          var input = document.getElementById('research-publications-search');
          var emptyState = document.getElementById('research-publications-empty');
          if (!input) {
            return;
          }

          var sections = Array.prototype.slice.call(document.querySelectorAll('.csdc-research-page .csdc-research-year-section'));
          if (!sections.length) {
            return;
          }

          var yearJumpNav = document.querySelector('[data-csdc-research-year-jump]');

          function applyFilter() {
            var query = input.value.toLowerCase().trim();
            var visibleCards = 0;

            sections.forEach(function (section) {
              var cards = Array.prototype.slice.call(section.querySelectorAll('.csdc-card'));
              var visibleInSection = 0;
              var headingCount = section.querySelector('.csdc-research-year-count');

              cards.forEach(function (card) {
                var haystack = (card.textContent || '').toLowerCase();
                var isMatch = query === '' || haystack.indexOf(query) !== -1;
                card.style.display = isMatch ? '' : 'none';
                if (isMatch) {
                  visibleInSection += 1;
                  visibleCards += 1;
                }
              });

              if (headingCount) {
                if (query === '') {
                  headingCount.textContent = headingCount.getAttribute('data-total-count') || String(visibleInSection);
                } else {
                  headingCount.textContent = String(visibleInSection);
                }
              }

              section.style.display = visibleInSection > 0 ? '' : 'none';
            });

            if (yearJumpNav) {
              yearJumpNav.style.display = '';
            }

            if (emptyState) {
              emptyState.hidden = visibleCards !== 0;
            }

            document.dispatchEvent(new CustomEvent('csdc:research-filter-changed'));
          }

          input.addEventListener('input', applyFilter);
          applyFilter();
        }

        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', init);
        } else {
          init();
        }
      })();
      </script>
      {% else %}
      <div class="csdc-card">
        <p style="margin:0;">No publications submitted yet. Use the footer "Add publication" form to add DOI or URL entries.</p>
      </div>
      {% endif %}
    </div>
  </section>
</div>

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
      <h2>Publications by Member Category</h2>
      {% assign publications = site.posts | where_exp: "post", "post.path contains '_posts/papers/'" %}
      {% if publications and publications.size > 0 %}
      {% assign faculty_members = '' | split: '' %}
      {% assign professor_members = '' | split: '' %}
      {% assign student_members = '' | split: '' %}
      {% assign staff_members = '' | split: '' %}

      {% for member_hash in site.data.authors %}
      {% assign member_key = member_hash[0] %}
      {% assign member = member_hash[1] %}
      {% assign member_key_lc = member_key | default: '' | downcase %}
      {% assign member_name_lc = member.name | default: '' | downcase %}
      {% assign role_type = member.current_role.type | default: '' %}
      {% assign role_title_lc = member.current_role.title | default: '' | downcase %}

      {% if role_type == 'Faculty' %}
      {% if role_title_lc contains 'professor' %}
      {% assign professor_members = professor_members | push: member_key_lc %}
      {% assign professor_members = professor_members | push: member_name_lc %}
      {% else %}
      {% assign faculty_members = faculty_members | push: member_key_lc %}
      {% assign faculty_members = faculty_members | push: member_name_lc %}
      {% endif %}
      {% elsif role_type == 'Professor' %}
      {% assign professor_members = professor_members | push: member_key_lc %}
      {% assign professor_members = professor_members | push: member_name_lc %}
      {% elsif role_type == 'Student' %}
      {% assign student_members = student_members | push: member_name_lc %}
      {% elsif role_type == 'Staff' %}
      {% assign staff_members = staff_members | push: member_name_lc %}
      {% endif %}
      {% endfor %}

      {% assign faculty_publications = '' | split: '' %}
      {% assign professor_publications = '' | split: '' %}
      {% assign student_publications = '' | split: '' %}
      {% assign staff_publications = '' | split: '' %}
      {% assign non_affiliated_publications = '' | split: '' %}

      {% for post in publications %}
      {% assign explicit_author_lc = post.author | default: '' | downcase %}
      {% assign names_lc = post.names | default: '' | downcase %}
      {% assign match_faculty = false %}
      {% assign match_professor = false %}
      {% assign match_student = false %}
      {% assign match_staff = false %}

      {% if explicit_author_lc != '' %}
      {% for member_name in faculty_members %}
      {% if explicit_author_lc == member_name %}
      {% assign match_faculty = true %}
      {% break %}
      {% endif %}
      {% endfor %}

      {% unless match_faculty %}
      {% for member_name in professor_members %}
      {% if explicit_author_lc == member_name %}
      {% assign match_professor = true %}
      {% break %}
      {% endif %}
      {% endfor %}
      {% endunless %}

      {% unless match_faculty or match_professor %}
      {% for member_name in student_members %}
      {% if explicit_author_lc == member_name %}
      {% assign match_student = true %}
      {% break %}
      {% endif %}
      {% endfor %}
      {% endunless %}

      {% unless match_faculty or match_professor or match_student %}
      {% for member_name in staff_members %}
      {% if explicit_author_lc == member_name %}
      {% assign match_staff = true %}
      {% break %}
      {% endif %}
      {% endfor %}
      {% endunless %}
      {% else %}
      {% for member_name in student_members %}
      {% if names_lc contains member_name %}
      {% assign match_student = true %}
      {% break %}
      {% endif %}
      {% endfor %}

      {% unless match_student %}
      {% for member_name in staff_members %}
      {% if names_lc contains member_name %}
      {% assign match_staff = true %}
      {% break %}
      {% endif %}
      {% endfor %}
      {% endunless %}
      {% endif %}

      {% if match_faculty %}
      {% assign faculty_publications = faculty_publications | push: post %}
      {% elsif match_professor %}
      {% assign professor_publications = professor_publications | push: post %}
      {% elsif match_student %}
      {% assign student_publications = student_publications | push: post %}
      {% elsif match_staff %}
      {% assign staff_publications = staff_publications | push: post %}
      {% else %}
      {% assign non_affiliated_publications = non_affiliated_publications | push: post %}
      {% endif %}
      {% endfor %}

      <h3>Faculty</h3>
      {% if faculty_publications.size > 0 %}
      <div class="csdc-pillars csdc-pillars-two">
        {% for post in faculty_publications limit:8 %}
        <article class="csdc-card">
          <h4 class="csdc-card-title" style="margin-bottom:0.3rem;"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h4>
          {% if post.names %}<p style="margin:0.2rem 0;">{{ post.names }}</p>{% endif %}
          {% if post.venue %}<p style="margin:0.2rem 0; color:#6b7280;">{{ post.venue }}</p>{% endif %}
          {% if post.link %}<p style="margin:0.35rem 0 0;"><a href="{{ post.link }}" target="_blank" rel="noopener noreferrer">Paper link</a></p>{% endif %}
        </article>
        {% endfor %}
      </div>
      {% else %}
      <div class="csdc-card"><p style="margin:0;">No faculty-tagged publications found yet.</p></div>
      {% endif %}

      <h3>Professors</h3>
      {% if professor_publications.size > 0 %}
      <div class="csdc-pillars csdc-pillars-two">
        {% for post in professor_publications limit:8 %}
        <article class="csdc-card">
          <h4 class="csdc-card-title" style="margin-bottom:0.3rem;"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h4>
          {% if post.names %}<p style="margin:0.2rem 0;">{{ post.names }}</p>{% endif %}
          {% if post.venue %}<p style="margin:0.2rem 0; color:#6b7280;">{{ post.venue }}</p>{% endif %}
          {% if post.link %}<p style="margin:0.35rem 0 0;"><a href="{{ post.link }}" target="_blank" rel="noopener noreferrer">Paper link</a></p>{% endif %}
        </article>
        {% endfor %}
      </div>
      {% else %}
      <div class="csdc-card"><p style="margin:0;">No professor-tagged publications found yet.</p></div>
      {% endif %}

      <h3>Broader Research Outputs</h3>

      <h4>Students</h4>
      {% if student_publications.size > 0 %}
      <div class="csdc-pillars csdc-pillars-two">
        {% for post in student_publications limit:8 %}
        <article class="csdc-card">
          <h5 class="csdc-card-title" style="margin-bottom:0.3rem;"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h5>
          {% if post.names %}<p style="margin:0.2rem 0;">{{ post.names }}</p>{% endif %}
          {% if post.venue %}<p style="margin:0.2rem 0; color:#6b7280;">{{ post.venue }}</p>{% endif %}
          {% if post.link %}<p style="margin:0.35rem 0 0;"><a href="{{ post.link }}" target="_blank" rel="noopener noreferrer">Paper link</a></p>{% endif %}
        </article>
        {% endfor %}
      </div>
      {% else %}
      <div class="csdc-card"><p style="margin:0;">No student publications found yet.</p></div>
      {% endif %}

      <h4>Staff</h4>
      {% if staff_publications.size > 0 %}
      <div class="csdc-pillars csdc-pillars-two">
        {% for post in staff_publications limit:8 %}
        <article class="csdc-card">
          <h5 class="csdc-card-title" style="margin-bottom:0.3rem;"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h5>
          {% if post.names %}<p style="margin:0.2rem 0;">{{ post.names }}</p>{% endif %}
          {% if post.venue %}<p style="margin:0.2rem 0; color:#6b7280;">{{ post.venue }}</p>{% endif %}
          {% if post.link %}<p style="margin:0.35rem 0 0;"><a href="{{ post.link }}" target="_blank" rel="noopener noreferrer">Paper link</a></p>{% endif %}
        </article>
        {% endfor %}
      </div>
      {% else %}
      <div class="csdc-card"><p style="margin:0;">No staff publications found yet.</p></div>
      {% endif %}

      <h4>Non-affiliated Publications</h4>
      {% if non_affiliated_publications.size > 0 %}
      <div class="csdc-pillars csdc-pillars-two">
        {% for post in non_affiliated_publications limit:8 %}
        <article class="csdc-card">
          <h5 class="csdc-card-title" style="margin-bottom:0.3rem;"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h5>
          {% if post.names %}<p style="margin:0.2rem 0;">{{ post.names }}</p>{% endif %}
          {% if post.venue %}<p style="margin:0.2rem 0; color:#6b7280;">{{ post.venue }}</p>{% endif %}
          {% if post.link %}<p style="margin:0.35rem 0 0;"><a href="{{ post.link }}" target="_blank" rel="noopener noreferrer">Paper link</a></p>{% endif %}
        </article>
        {% endfor %}
      </div>
      {% else %}
      <div class="csdc-card"><p style="margin:0;">No broader research outputs found yet.</p></div>
      {% endif %}

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

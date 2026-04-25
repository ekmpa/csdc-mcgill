---
permalink: /people/
title: "People"
layout: splash_v2
search_terms: "Dietlind Stolle Anne Imouza Emma Kondrup"
classes:
    - csdc-page
---

<div class="csdc-page csdc-people-page">
<section class="csdc-section csdc-page-header">
    <div class="csdc-container">
        <h1 id="page-title" class="page__title csdc-page-title">Our Research Team</h1>
        <p class="csdc-page-subtitle">Meet the researchers and staff advancing democratic citizenship research at McGill.</p>
    </div>
</section>

<div class="csdc-container">

<h2>Faculty / Professors</h2>
{% include card-authors-with-role.html authors=site.data.authors role="Faculty / Professor" render_current_role=true %}

<h2>Staff</h2>
{% include card-authors-with-role.html authors=site.data.authors role="Staff" render_current_role=true %}

<h2>Students</h2>
{% include card-authors-with-role.html authors=site.data.authors role="Student" render_current_role=true %}

<p>
    <span class="csdc-contact-pill">Interested in joining us? <a href="mailto:anne.imouza@mail.mcgill.ca">Contact us</a></span>
</p>

</div>
</div>

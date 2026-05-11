---
permalink: /fr/people/
title: Equipe
layout: splash_v2
search_terms: "Dietlind Stolle Anne Imouza Emma Kondrup"
classes:
  - csdc-page
---

<div class="csdc-page csdc-people-page">
<section class="csdc-section csdc-page-header">
    <div class="csdc-container">
        <p class="csdc-kicker"><span class="csdc-red">Membres</span></p>
        <h1 id="page-title" class="page__title csdc-page-title">Equipe de recherche</h1>
        <p class="csdc-page-subtitle">Rencontrez les chercheur(e)s et membres du personnel qui font avancer les travaux du CÉCD a McGill.</p>
    </div>
</section>

<div class="csdc-container">

<h2>Corps professoral</h2>
{% include card-authors-with-role.html authors=site.data.authors role="Faculty / Professor" section_title="Corps professoral" render_current_role=true %}
{% include card-authors-with-role.html authors=site.data.authors role="Faculty / Professor" alumni=true %}

{% include card-authors-with-role.html authors=site.data.authors role="Staff" section_title="Personnel" render_current_role=true %}
{% include card-authors-with-role.html authors=site.data.authors role="Staff" alumni=true %}

{% include card-authors-with-role.html authors=site.data.authors role="Postdoc" section_title="Stagiaires postdoctoraux" render_current_role=true %}
{% include card-authors-with-role.html authors=site.data.authors role="Postdoc" alumni=true %}

{% include card-authors-with-role.html authors=site.data.authors role="Student" section_title="Etudiant(e)s" render_current_role=true %}
{% include card-authors-with-role.html authors=site.data.authors role="Student" alumni=true %}

<p>
    <span class="csdc-contact-pill">Vous souhaitez nous rejoindre? <a href="mailto:anne.imouza@mail.mcgill.ca">Contactez-nous</a></span>
</p>

</div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function () {
    var defaultOpen = document.querySelector('.csdc-people-page .author-card--default-open');
    if (!defaultOpen) {
        return;
    }

    var closeDefaultOpen = function (event) {
        var activeCard = event.target.closest('.author-card');
        if (!activeCard || activeCard === defaultOpen) {
            return;
        }

        defaultOpen.classList.remove('author-card--default-open');

        document.querySelectorAll('.csdc-people-page .author-card').forEach(function (card) {
            card.removeEventListener('mouseenter', closeDefaultOpen);
            card.removeEventListener('focusin', closeDefaultOpen);
        });
    };

    document.querySelectorAll('.csdc-people-page .author-card').forEach(function (card) {
        card.addEventListener('mouseenter', closeDefaultOpen);
        card.addEventListener('focusin', closeDefaultOpen);
    });
});
</script>

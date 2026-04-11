---
---
var store = [
{%- assign first_entry = true -%}

{%- for page in site.pages -%}
  {%- assign include_page = true -%}
  {%- if page.search == false -%}
    {%- assign include_page = false -%}
  {%- endif -%}
  {%- unless page.path contains '_pages/' -%}
    {%- assign include_page = false -%}
  {%- endunless -%}
  {%- if page.url == '/404.html' or page.url contains '.xml' or page.url contains '.js' -%}
    {%- assign include_page = false -%}
  {%- endif -%}
  {%- if page.url contains '/teaching/' or page.url contains '/venues/' or page.url contains '/year' or page.url contains '/tag' or page.url contains '/categor' -%}
    {%- assign include_page = false -%}
  {%- endif -%}
  {%- if include_page -%}
    {%- unless first_entry -%},{%- endunless -%}
    {
      "title": {{ page.title | default: page.url | jsonify }},
      "excerpt": {{ page.excerpt | default: page.search_terms | default: page.content | markdownify | strip_html | strip_newlines | jsonify }},
      "categories": {{ page.categories | jsonify }},
      "tags": {{ page.tags | jsonify }},
      "url": {{ page.url | relative_url | jsonify }},
      "teaser": null
    }
    {%- assign first_entry = false -%}
  {%- endif -%}
{%- endfor -%}

{%- for post in site.posts -%}
  {%- assign include_post = true -%}
  {%- if post.search == false -%}
    {%- assign include_post = false -%}
  {%- endif -%}
  {%- unless post.url contains '/news/' -%}
    {%- assign include_post = false -%}
  {%- endunless -%}
  {%- if include_post -%}
    {%- unless first_entry -%},{%- endunless -%}
    {
      "title": {{ post.title | jsonify }},
      "excerpt": {{ post.excerpt | default: post.content | markdownify | strip_html | strip_newlines | jsonify }},
      "categories": {{ post.categories | jsonify }},
      "tags": {{ post.tags | jsonify }},
      "url": {{ post.url | relative_url | jsonify }},
      "teaser": null
    }
    {%- assign first_entry = false -%}
  {%- endif -%}
{%- endfor -%}

];

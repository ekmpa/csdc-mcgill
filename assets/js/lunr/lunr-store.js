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
    {%- capture page_search_text -%}
      {{ page.excerpt | default: page.search_terms | default: page.content | markdownify | strip_html | strip_newlines }}
      {{ page.title }}
    {%- endcapture -%}
    {%- assign page_search_text_ascii = page_search_text
      | replace: 'É', 'E' | replace: 'é', 'e'
      | replace: 'È', 'E' | replace: 'è', 'e'
      | replace: 'Ê', 'E' | replace: 'ê', 'e'
      | replace: 'Ë', 'E' | replace: 'ë', 'e'
      | replace: 'À', 'A' | replace: 'à', 'a'
      | replace: 'Â', 'A' | replace: 'â', 'a'
      | replace: 'Î', 'I' | replace: 'î', 'i'
      | replace: 'Ï', 'I' | replace: 'ï', 'i'
      | replace: 'Ô', 'O' | replace: 'ô', 'o'
      | replace: 'Ö', 'O' | replace: 'ö', 'o'
      | replace: 'Ù', 'U' | replace: 'ù', 'u'
      | replace: 'Û', 'U' | replace: 'û', 'u'
      | replace: 'Ü', 'U' | replace: 'ü', 'u'
      | replace: 'Ç', 'C' | replace: 'ç', 'c'
      | replace: 'œ', 'oe' | replace: 'Œ', 'OE'
      | replace: 'æ', 'ae' | replace: 'Æ', 'AE'
      | replace: '’', "'" -%}
    {%- unless first_entry -%},{%- endunless -%}
    {
      "title": {{ page.title | default: page.url | jsonify }},
      "excerpt": {{ page_search_text | append: ' ' | append: page_search_text_ascii | strip | jsonify }},
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
    {%- unless post.path contains '_posts/papers/' -%}
      {%- assign include_post = false -%}
    {%- endunless -%}
  {%- endif -%}
  {%- if include_post -%}
    {%- capture post_search_text -%}
      {{ post.excerpt | default: post.content | markdownify | strip_html | strip_newlines }}
      {{ post.title }}
      {{ post.author }}
      {{ post.names }}
      {{ post.slug }}
    {%- endcapture -%}
    {%- assign post_search_text_ascii = post_search_text
      | replace: 'É', 'E' | replace: 'é', 'e'
      | replace: 'È', 'E' | replace: 'è', 'e'
      | replace: 'Ê', 'E' | replace: 'ê', 'e'
      | replace: 'Ë', 'E' | replace: 'ë', 'e'
      | replace: 'À', 'A' | replace: 'à', 'a'
      | replace: 'Â', 'A' | replace: 'â', 'a'
      | replace: 'Î', 'I' | replace: 'î', 'i'
      | replace: 'Ï', 'I' | replace: 'ï', 'i'
      | replace: 'Ô', 'O' | replace: 'ô', 'o'
      | replace: 'Ö', 'O' | replace: 'ö', 'o'
      | replace: 'Ù', 'U' | replace: 'ù', 'u'
      | replace: 'Û', 'U' | replace: 'û', 'u'
      | replace: 'Ü', 'U' | replace: 'ü', 'u'
      | replace: 'Ç', 'C' | replace: 'ç', 'c'
      | replace: 'œ', 'oe' | replace: 'Œ', 'OE'
      | replace: 'æ', 'ae' | replace: 'Æ', 'AE'
      | replace: '’', "'" -%}
    {%- unless first_entry -%},{%- endunless -%}
    {
      "title": {{ post.title | jsonify }},
      "excerpt": {{ post_search_text | append: ' ' | append: post_search_text_ascii | strip | jsonify }},
      "categories": {{ post.categories | jsonify }},
      "tags": {{ post.tags | jsonify }},
      "url": {{ post.url | relative_url | jsonify }},
      "teaser": null
    }
    {%- assign first_entry = false -%}
  {%- endif -%}
{%- endfor -%}

];

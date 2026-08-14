---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

[Google Scholar](https://scholar.google.com/citations?user=y9gR9AYAAAAJ) &nbsp;|&nbsp; [ORCID 0000-0002-0151-6397](https://orcid.org/0000-0002-0151-6397)

{{ site.data.pub_stats.publications }} indexed publications, {{ site.data.pub_stats.citations }} citations ({{ site.data.pub_stats.source }}, {{ site.data.pub_stats.last_updated }}), plus one patent and a doctoral thesis.

## Selected

<ul>
{%- for doi in site.data.highlights -%}
{%- assign pub = site.data.publications | where: "doi", doi | first -%}
{%- if pub %}
  <li>{{ pub.authors | replace: "Aubourg, T.", "<strong>Aubourg, T.</strong>" }} {{ pub.title }}. <em>{{ pub.venue }}</em> ({{ pub.year }}). <a href="{{ pub.url }}">doi:{{ pub.doi }}</a></li>
{%- endif -%}
{%- endfor %}
</ul>

---

## All Publications

{%- assign all = site.data.publications | concat: site.data.publications_manual | sort: "year" | reverse -%}
{%- assign years = all | map: "year" | uniq -%}
{%- for year in years %}

### {{ year }}

<ul>
{%- for pub in all -%}
{%- if pub.year == year %}
  <li>{{ pub.authors | replace: "Aubourg, T.", "<strong>Aubourg, T.</strong>" }} {{ pub.title }}. <em>{{ pub.venue }}</em>{% if pub.url %}. <a href="{{ pub.url }}">{% if pub.doi %}doi:{{ pub.doi }}{% else %}link{% endif %}</a>{% endif %}</li>
{%- endif -%}
{%- endfor %}
</ul>
{%- endfor %}

---

*This list is generated from the [Semantic Scholar](https://www.semanticscholar.org/) API and refreshed weekly. The patent and thesis are listed manually.*

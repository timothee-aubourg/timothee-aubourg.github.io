---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

[Google Scholar](https://scholar.google.com/citations?user=y9gR9AYAAAAJ) &nbsp;|&nbsp; [ORCID 0000-0002-0151-6397](https://orcid.org/0000-0002-0151-6397)

{{ site.data.scholar.citations }} citations, h-index {{ site.data.scholar.h_index }} (Google Scholar, {{ site.data.scholar.last_updated }}).

## Selected

<ul>
{%- for doi in site.data.highlights -%}
{%- assign pub = site.data.publications | where: "doi", doi | first -%}
{%- if pub %}
  <li>{{ pub.authors | replace: "Aubourg, T.", "<strong>Aubourg, T.</strong>" }} {{ pub.title }}. <em>{{ pub.venue }}</em> ({{ pub.year }}). <a href="{{ pub.url }}">doi:{{ pub.doi }}</a></li>
{%- endif -%}
{%- endfor %}
</ul>

The full list is on [Google Scholar](https://scholar.google.com/citations?user=y9gR9AYAAAAJ) and [ORCID](https://orcid.org/0000-0002-0151-6397).

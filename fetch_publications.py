"""Fetch the publication list and citation stats from the Semantic Scholar API.

Replaces the previous Google Scholar scraper, which Google blocks from CI runners.
Semantic Scholar offers a documented, key-free API that is not rate-blocked for
this volume, so the workflow can run unattended.

Writes:
  _data/publications.yml  - one entry per publication, newest first
  _data/pub_stats.yml     - citation count, h-index, publication count

Curation lives in _data/highlights.yml (a list of DOIs) and
_data/publications_manual.yml (items Semantic Scholar does not index, e.g. the
thesis and the patent). Neither is touched by this script.
"""

import re
import sys
import time
from datetime import date

import requests
import yaml

AUTHOR_ID = "1395795774"  # Semantic Scholar author id for T. Aubourg
API = "https://api.semanticscholar.org/graph/v1"
PAPER_FIELDS = "title,year,venue,externalIds,citationCount,authors"
TIMEOUT = 60

# Semantic Scholar indexes preprint deposits, errata and conference abstracts
# alongside articles. These are duplicates or non-substantive, so drop them.
TITLE_REJECT = re.compile(r"^(author correction|correction to|erratum)\b", re.I)
ABSTRACT_ID = re.compile(r"^(POS|AB|OP|SAT|THU|FRI)\d+", re.I)


def get(url, **params):
    """GET with a couple of retries; Semantic Scholar 429s under burst load."""
    for attempt in range(4):
        r = requests.get(url, params=params, timeout=TIMEOUT)
        if r.status_code == 200:
            return r.json()
        if r.status_code in (429, 503):
            time.sleep(5 * (attempt + 1))
            continue
        r.raise_for_status()
    raise RuntimeError(f"giving up on {url} after retries")


def normalise(title):
    return re.sub(r"[^a-z0-9]+", "", title.lower())


def keep(paper):
    title = paper.get("title") or ""
    doi = (paper.get("externalIds") or {}).get("DOI", "")
    if TITLE_REJECT.match(title) or ABSTRACT_ID.match(title):
        return False
    if "preprints" in doi.lower():
        return False
    if not paper.get("venue"):
        return False
    return True


def format_authors(authors):
    """'Aubourg, T., Gunter, K., Lo, C. et al.' with our name marked for bolding."""
    out = []
    for a in authors[:3]:
        parts = (a.get("name") or "").split()
        if not parts:
            continue
        family, initials = parts[-1], "".join(p[0] + "." for p in parts[:-1])
        out.append(f"{family}, {initials}" if initials else family)
    joined = ", ".join(out)
    if len(authors) > 3:
        joined += " et al."
    return joined


def crossref_year(doi):
    """Crossref is authoritative for the year of record.

    Semantic Scholar sometimes reports the earliest online-first date, which
    disagrees with the issue a paper was actually published in (e.g. JMIR
    10.2196/22339 is S2 2020, Crossref 2021). Returns None on any failure so a
    Crossref outage degrades to the S2 year rather than breaking the build.
    """
    try:
        r = requests.get(
            f"https://api.crossref.org/works/{doi}",
            params={"mailto": "timothee.aubourg@ndcn.ox.ac.uk"},
            timeout=30,
        )
        if r.status_code != 200:
            return None
        msg = r.json()["message"]
        for key in ("published-print", "published-online", "issued"):
            parts = (msg.get(key) or {}).get("date-parts") or []
            if parts and parts[0] and parts[0][0]:
                return int(parts[0][0])
    except Exception as e:  # noqa: BLE001 - enrichment must never be fatal
        print(f"  crossref lookup failed for {doi}: {e}", file=sys.stderr)
    return None


def main():
    author = get(f"{API}/author/{AUTHOR_ID}", fields="citationCount,hIndex,paperCount")
    papers = get(f"{API}/author/{AUTHOR_ID}/papers", fields=PAPER_FIELDS, limit=200)

    seen, entries = set(), []
    for p in papers.get("data", []):
        if not keep(p):
            continue
        key = normalise(p["title"])
        if key in seen:
            continue
        seen.add(key)
        doi = (p.get("externalIds") or {}).get("DOI")
        year = p.get("year")
        if doi:
            authoritative = crossref_year(doi)
            if authoritative and authoritative != year:
                print(f"  year corrected {year} -> {authoritative} for {doi}")
                year = authoritative
        entries.append(
            {
                "title": p["title"].replace("’", "'"),
                "authors": format_authors(p.get("authors") or []),
                "venue": p.get("venue"),
                "year": year,
                "doi": doi,
                "url": f"https://doi.org/{doi}" if doi else None,
                "citations": p.get("citationCount", 0),
            }
        )

    entries.sort(key=lambda e: (e["year"] or 0, e["citations"]), reverse=True)

    if len(entries) < 10:
        # A near-empty response means the API changed or the author id broke.
        # Fail loudly rather than silently truncating the publication list.
        print(f"Only {len(entries)} publications parsed; refusing to overwrite.",
              file=sys.stderr)
        sys.exit(1)

    stats = {
        "citations": author.get("citationCount", 0),
        "h_index": author.get("hIndex", 0),
        "publications": len(entries),
        "source": "Semantic Scholar",
        "last_updated": str(date.today()),
    }

    with open("_data/publications.yml", "w", encoding="utf-8") as f:
        yaml.dump(entries, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    with open("_data/pub_stats.yml", "w", encoding="utf-8") as f:
        yaml.dump(stats, f, default_flow_style=False, allow_unicode=True)

    print(f"Wrote {len(entries)} publications. {stats}")


if __name__ == "__main__":
    main()

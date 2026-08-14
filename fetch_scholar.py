"""Fetch citation count and h-index from the Google Scholar profile.

RUN THIS LOCALLY, NOT IN CI.

Google has no public API; this reads the profile page. Google blocks that read
from datacenter IPs, which is why the previous GitHub Actions workflow failed
every week from 2026-06-29 onwards. From a normal connection it works fine.

    make scholar        # fetch, then commit _data/scholar.yml

Run it occasionally, not in a loop, or Google will start showing a CAPTCHA to
your address as well.
"""

import re
import sys
from datetime import date

import requests
import yaml

SCHOLAR_URL = (
    "https://scholar.google.com/citations?user=y9gR9AYAAAAJ&hl=en"
)
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36"


def main():
    r = requests.get(SCHOLAR_URL, headers={"User-Agent": UA}, timeout=45)
    if r.status_code != 200:
        sys.exit(f"Google Scholar returned HTTP {r.status_code}.")

    if re.search(r"unusual traffic|not a robot|/sorry/", r.text, re.I):
        sys.exit(
            "Google Scholar served a CAPTCHA instead of the profile.\n"
            "This happens on datacenter IPs (CI) or after repeated requests.\n"
            "Run it later from a normal connection; _data/scholar.yml is unchanged."
        )

    # The profile stats table holds, in order:
    #   citations (all), citations (since), h-index (all), h-index (since),
    #   i10-index (all), i10-index (since)
    values = re.findall(r'gsc_rsb_std">(\d+)</td>', r.text)
    if len(values) < 3:
        sys.exit("Could not find the stats table; Scholar's markup may have changed.")

    stats = {
        "citations": int(values[0]),
        "h_index": int(values[2]),
        "last_updated": str(date.today()),
    }

    with open("_data/scholar.yml", "w", encoding="utf-8") as f:
        yaml.dump(stats, f, default_flow_style=False, allow_unicode=True)
    print(f"Updated _data/scholar.yml: {stats}")


if __name__ == "__main__":
    main()

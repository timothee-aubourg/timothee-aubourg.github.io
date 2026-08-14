.PHONY: scholar serve build

# Refresh Google Scholar citation count and h-index.
# Must run locally: Google blocks these reads from CI runners.
scholar:
	python3 fetch_scholar.py
	@git diff --stat _data/scholar.yml

# Refresh the publication list from Semantic Scholar + Crossref.
# This also runs weekly in GitHub Actions, so you rarely need it by hand.
publications:
	python3 fetch_publications.py

serve:
	bundle exec jekyll serve --livereload

build:
	bundle exec jekyll build

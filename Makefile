PYTHON ?= python3

.PHONY: wiki-ingest wiki-query wiki-lint wiki-dispatch

wiki-ingest:
	$(PYTHON) scripts/wiki_ingest.py $(SRC) --title "$(TITLE)"

wiki-query:
	$(PYTHON) scripts/wiki_query.py "$(Q)"

wiki-lint:
	$(PYTHON) scripts/wiki_lint.py

wiki-dispatch:
	$(PYTHON) scripts/wiki_dispatch.py

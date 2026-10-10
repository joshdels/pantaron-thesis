.PHONY: help scrape scrape-openalex scrape-semantic scrape-web report syntax venv uv-sync

PYTHON ?= python3
QUERY ?= Pantaron Mountain Range land and water resources management remote sensing GIS land cover forest fragmentation land capability soil erosion watershed catchment rainfall drainage surface water water quality field validation
OUTPUT ?= outputs/data/pantaron-rrl.csv
PER_TIER ?= 200
PROVIDER ?= both
MAILTO ?= deleonjoshy@gmail.com
DELAY ?= 2
SEMANTIC_API_KEY ?=
WEB_OUTPUT ?= outputs/data/pantaron-web-discovery.csv
WEB_PER_QUERY ?= 50
WEB_DELAY ?= 5

help:
	@echo 'make scrape-openalex [QUERY="..."] [OUTPUT=path] [PER_TIER=100] [PROVIDER=both] [MAILTO=email]'
	@echo 'make scrape-semantic [QUERY="..."] [OUTPUT=path] [PER_TIER=100]'
	@echo 'make venv or make uv-sync for optional uv environment setup'
	@echo 'make report [INPUT=outputs/data] [REPORT=index.html]'
	@echo 'make scrape-web [WEB_OUTPUT=outputs/data/pantaron-web-discovery.csv] [WEB_PER_QUERY=50] [WEB_DELAY=5]'

scrape:
	$(MAKE) scrape-openalex
	$(MAKE) scrape-semantic OUTPUT=outputs/data/semantic-scholar-literature.csv
	$(MAKE) scrape-web

scrape-openalex:
	$(PYTHON) scripts/openalex_scraper_lit.py \
		"$(QUERY)" \
		--output "$(OUTPUT)" \
		--per-tier "$(PER_TIER)" \
		--provider "$(PROVIDER)" \
		--delay "$(DELAY)" \
		--mailto "$(MAILTO)"

scrape-semantic:
	$(PYTHON) scripts/semantic_scholar_scraper.py \
		"$(QUERY)" \
		--output "$(OUTPUT)" \
		--per-tier "$(PER_TIER)" \
		--delay "$(DELAY)" \
		$(if $(SEMANTIC_API_KEY),--api-key "$(SEMANTIC_API_KEY)",)

scrape-web:
	$(PYTHON) scripts/pantaron_web_harvester.py \
		--output "$(WEB_OUTPUT)" \
		--per-query "$(WEB_PER_QUERY)" \
		--delay "$(WEB_DELAY)"

report:
	$(PYTHON) scripts/report_generator.py \
		--input-dir "$(or $(INPUT),outputs/data)" \
		--output "$(or $(REPORT),index.html)"

syntax:
	$(PYTHON) -m py_compile scripts/literature_scraper.py scripts/openalex_scraper_lit.py scripts/semantic_scholar_scraper.py scripts/report_generator.py scripts/pantaron_web_harvester.py

venv:
	uv venv .venv

uv-sync:
	uv venv .venv

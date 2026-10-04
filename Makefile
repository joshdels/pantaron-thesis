.PHONY: help scrape scrape-openalex scrape-semantic report syntax venv uv-sync

PYTHON ?= python3
QUERY ?= Pantaron Pantaron Mountain Range GIS remote sensing land cover land use watershed catchment hydrology hydroclimate rainfall drainage DEM terrain water resources evaluation assessment analysis
OUTPUT ?= outputs/data/pantaron-rrl.csv
PER_TIER ?= 200
PROVIDER ?= both
MAILTO ?= deleonjoshy@gmail.com
DELAY ?= 2
SEMANTIC_API_KEY ?=

help:
	@echo 'make scrape-openalex [QUERY="..."] [OUTPUT=path] [PER_TIER=100] [PROVIDER=both] [MAILTO=email]'
	@echo 'make scrape-semantic [QUERY="..."] [OUTPUT=path] [PER_TIER=100]'
	@echo 'make venv or make uv-sync for optional uv environment setup'
	@echo 'make report [INPUT=outputs/data] [REPORT=outputs/report/index.html]'

scrape:
	$(MAKE) scrape-openalex
	$(MAKE) scrape-semantic OUTPUT=outputs/data/semantic-scholar-literature.csv

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

report:
	$(PYTHON) scripts/report_generator.py \
		--input-dir "$(or $(INPUT),outputs/data)" \
		--output "$(or $(REPORT),literature-report.html)"

syntax:
	$(PYTHON) -m py_compile scripts/literature_scraper.py scripts/openalex_scraper_lit.py scripts/semantic_scholar_scraper.py scripts/report_generator.py

venv:
	uv venv .venv

uv-sync:
	uv venv .venv

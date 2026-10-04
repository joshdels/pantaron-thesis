# Script-specific instructions

These scripts harvest scholarly metadata for the Pantaron land- and water-resources RRL.

## Entry points

- `openalex_scraper_lit.py`: compatibility entry point for the OpenAlex/Crossref scraper in `literature_scraper.py`.
- `semantic_scholar_scraper.py`: Semantic Scholar Academic Graph API scraper.
- `literature_scraper.py`: shared OpenAlex/Crossref implementation; retain it until the wrapper is intentionally replaced.

## Standard workflow

Run from the repository root:

```bash
make syntax
make scrape-openalex
make scrape-semantic
make scrape
```

Override `QUERY`, `OUTPUT`, `PER_TIER`, `PROVIDER`, `DELAY`, or `MAILTO` on the command line. Generated CSVs belong in `outputs/data/`.

Semantic Scholar can rate-limit anonymous requests. Use a larger delay and, when available, an API key: `make scrape-semantic DELAY=10 SEMANTIC_API_KEY=...`. A failed Semantic Scholar tier is skipped so a temporary provider limit does not erase or invalidate the OpenAlex/Crossref result.

## Output contract

CSV exports use these columns:

`year publication`, `country`, `authors`, `title`, `abstract`, `possible methods used`, `search tier`, `source url`

`possible methods used` is a keyword-based discovery hint, not a verified method. Blank abstracts must remain blank. Country is blank when the provider does not supply affiliation-country metadata; never guess it from the title.

## Evidence and API rules

- Use official APIs and respect rate limits, delays, retries, and provider terms.
- Do not scrape Google Scholar HTML, bypass CAPTCHAs, or download paywalled full text automatically.
- Treat all records as discovery leads until the publisher, repository, or official record is checked.
- Deduplicate by DOI where available, otherwise normalized title and year.
- Do not silently merge provider records or overwrite a manually curated literature matrix.
- When adding a provider, preserve the search tier and source URL and match the output contract.

## Maintenance

Keep queries and output paths configurable. Prefer small standard-library changes. After edits, run `make syntax` and inspect the CSV header and several rows before using the records in the thesis.

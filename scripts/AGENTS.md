# Script-specific instructions

These scripts harvest scholarly metadata, discover reported Pantaron land/water problems, maintain reviewed policy records, and generate the research evidence report.

## Entry points

- `openalex_scraper_lit.py`: compatibility entry point for the OpenAlex/Crossref scraper in `literature_scraper.py`.
- `semantic_scholar_scraper.py`: Semantic Scholar Academic Graph API scraper.
- `literature_scraper.py`: shared OpenAlex/Crossref implementation; retain it until the wrapper is intentionally replaced.
- `pantaron_web_harvester.py`: RSS-based problem/news discovery plus reviewed Pantaron problem and official policy baselines.
- `report_generator.py`: reads compatible CSV exports in `outputs/data/` and generates the root `index.html` report.

## Standard workflow

Run from the repository root:

```bash
make syntax
make scrape-openalex
make scrape-semantic
make scrape
make scrape-web
make report
```

Override `QUERY`, `OUTPUT`, `PER_TIER`, `PROVIDER`, `DELAY`, or `MAILTO` on the command line. Generated CSVs belong in `outputs/data/`.

Semantic Scholar can rate-limit anonymous requests. Use a larger delay and, when available, an API key: `make scrape-semantic DELAY=10 SEMANTIC_API_KEY=...`. A failed Semantic Scholar tier is skipped so a temporary provider limit does not erase or invalidate the OpenAlex/Crossref result.

The web harvester defaults to Google News RSS with Bing fallback, uses cached responses, and retains reviewed baseline records when live discovery is unavailable. For a fresh direct run:

```bash
python3 scripts/pantaron_web_harvester.py --provider auto --refresh
```

Do not confuse `0 RSS news` with an empty output: reviewed problem and policy baselines may still populate the CSV. Live RSS records remain unverified discovery leads.

## Output contract

CSV exports use these columns:

`year publication`, `country`, `authors`, `title`, `abstract`, `possible methods used`, `search tier`, `source url`

`possible methods used` is a keyword-based discovery hint, not a verified method. Blank abstracts must remain blank. Country is blank when the provider does not supply affiliation-country metadata; never guess it from the title.

The web discovery CSV uses:

`record type`, `title`, `date published`, `source/domain`, `jurisdiction`, `legal status`, `location or scope`, `issue tags`, `summary`, `evidence status`, `search tier`, `source url`, `retrieved date`

The sanitized problem CSV uses:

`problem category`, `reported condition`, `relationship to Pantaron`, `geographic scope`, `source date`, `source`, `source type`, `summary`, `research use`, `limitations`, `evidence status`, `source url`, `retrieved date`

## Evidence and API rules

- Use official APIs and respect rate limits, delays, retries, and provider terms.
- Do not scrape Google Scholar HTML, bypass CAPTCHAs, or download paywalled full text automatically.
- Treat all records as discovery leads until the publisher, repository, or official record is checked.
- Deduplicate by DOI where available, otherwise normalized title and year.
- Do not silently merge provider records or overwrite a manually curated literature matrix.
- When adding a provider, preserve the search tier and source URL and match the output contract.
- Prefer RSS or documented provider endpoints over scraping search-result HTML.
- Keep reviewed sources separate from RSS leads. Do not silently promote an RSS record to reviewed status.
- Keep legal status precise: enacted law, bill/proposal, international convention, and declaration are not interchangeable.

## Maintenance

Keep queries and output paths configurable. Prefer small standard-library changes. After edits:

1. Run `make syntax`.
2. Run the relevant scraper with a small limit.
3. Inspect CSV headers, row counts, source links, and evidence labels.
4. Run `make report` and open `index.html`.
5. Modify `report_generator.py`, not generated `index.html`, for lasting report changes.

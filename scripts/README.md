# Literature scraper

`openalex_scraper_lit.py` creates a CSV review queue from public OpenAlex and Crossref metadata APIs. It does not download paywalled papers or decide relevance.

`semantic_scholar_scraper.py` is a separate scraper using Semantic Scholar's official Academic Graph API. Run it with `make scrape-semantic`. The combined `make scrape` target runs both scripts and writes separate CSV files so records can be merged and deduplicated in a later review step.

`report_generator.py` reads every CSV in `outputs/data/` and creates a static HTML report with counts, SVG charts, method-keyword patterns, and a record table. Run `make report`, then open `outputs/report/index.html` in a browser. The “strongest method” statement is only the most frequent `possible methods used` label in the supplied metadata; it is not a validated engineering conclusion.

To request a key, use the **Request an API Key** form on the [Semantic Scholar API page](https://www.semanticscholar.org/product/api). Store it locally in `.env` as `SEMANTIC_SCHOLAR_API_KEY=your_key` or pass it as `SEMANTIC_API_KEY=your_key` to `make`. Do not commit `.env` or paste the key into the Makefile.

Examples:

```bash
python scripts/literature_scraper.py \
  "Pantaron GIS remote sensing land water resources" \
  --output outputs/data/pantaron-rrl.csv --per-tier 40

python scripts/literature_scraper.py \
  "Sentinel-2 watershed land cover Philippines" \
  --no-tier-expansion --provider openalex \
  --output outputs/data/custom-search.csv
```

The default ordered tiers are Pantaron, Philippines, Asia, and global. The CSV preserves the search tier and source URL. API results are leads for the RRL; verify the title, abstract, methods, affiliation, and publication details against the publisher or repository before citing.

The `abstract` column contains only the abstract returned by the provider. It is cleaned for HTML and whitespace, but it is not AI-summarized or reconstructed. A blank abstract means the provider did not supply one. Authors are joined with `|` so spreadsheet programs do not split them into extra columns.

The APIs may return HTTP 429 when requests are too frequent. The script waits between requests and retries rate-limited requests with exponential backoff. If you have an email address you can identify the research client politely:

```bash
make scrape MAILTO=your.email@example.com DELAY=5
```

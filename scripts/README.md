# Pantaron harvesting and report scripts

Run commands from the repository root. Read `AGENTS.md` and `scripts/AGENTS.md` before changing source collection, evidence labels, or output schemas.

## Quick restart

```bash
make syntax
make scrape-web
make report
```

Open `index.html` after report generation. The report separates reviewed problem records, unverified RSS leads, policy/legal records, and scholarly metadata.

## Script roles

### `literature_scraper.py`

Shared OpenAlex/Crossref scholarly-metadata harvester. It creates a review queue and does not download paywalled papers or determine thesis relevance.

```bash
python3 scripts/literature_scraper.py \
  "Pantaron GIS remote sensing land water resources" \
  --output outputs/data/pantaron-rrl.csv \
  --per-tier 40
```

The default tiers are Pantaron, Philippines, Asia, and global methods. Preserve the tier because it records the search strategy, not verified geographic relevance.

### `openalex_scraper_lit.py`

Compatibility entry point for the OpenAlex/Crossref workflow. `make scrape-openalex` uses this script.

### `semantic_scholar_scraper.py`

Separate Semantic Scholar Academic Graph API harvester. Anonymous access may be rate-limited.

```bash
make scrape-semantic DELAY=10
```

When an API key is available, pass it through the environment or Make variable; do not commit it:

```bash
make scrape-semantic DELAY=10 SEMANTIC_API_KEY=your_key
```

### `pantaron_web_harvester.py`

Builds two related outputs:

- `outputs/data/pantaron-web-discovery.csv`: reviewed problem records, policy/legal records, and live RSS discoveries.
- `outputs/data/pantaron-land-water-problems.csv`: sanitized problem-focused table with scope, research use, and limitations.

The reviewed baseline ensures that an unavailable RSS provider does not produce a misleadingly empty research table. Console output such as `0 RSS news` means no live RSS items were accepted; it does not mean the baseline outputs are empty.

Default run:

```bash
make scrape-web
```

Fresh automatic provider run:

```bash
python3 scripts/pantaron_web_harvester.py --provider auto --refresh
```

Provider choices:

- `auto`: Google News RSS first, then Bing if no records are returned
- `google`: Google News RSS only
- `bing`: Bing News RSS only
- `both`: collect both and deduplicate
- `none`: write only the reviewed problem and policy baseline

The cache reduces repeated requests and rate-limit risk. `--refresh` bypasses cached feeds for one run. Use reasonable limits and delays; do not repeatedly hammer providers.

### `report_generator.py`

Reads CSV files in `outputs/data/` and generates `index.html`.

```bash
make report
```

The report:

- shows reviewed problems before RSS discovery leads;
- collapses unverified RSS rows by default;
- groups problem records into stable themes for charts;
- separates legal status and jurisdiction;
- hides literature sections when scholarly CSVs have no records.

For lasting style or layout changes, edit `report_generator.py`, not generated `index.html`.

## Output contracts

Scholarly metadata:

```text
year publication,country,authors,title,abstract,possible methods used,search tier,source url
```

Web discovery and policy records:

```text
record type,title,date published,source/domain,jurisdiction,legal status,location or scope,issue tags,summary,evidence status,search tier,source url,retrieved date
```

Sanitized problem records:

```text
problem category,reported condition,relationship to Pantaron,geographic scope,source date,source,source type,summary,research use,limitations,evidence status,source url,retrieved date
```

## Evidence rules

- Metadata, RSS titles, and RSS descriptions are discovery aids.
- Blank abstracts remain blank; never reconstruct or invent them.
- `possible methods used` is a keyword hint, not a verified method.
- Keep full-source review status explicit.
- Keep direct Pantaron evidence distinct from nearby, downstream, river-basin, and broad Mindanao context.
- Do not describe a bill as an enacted law.
- Do not infer local conditions, affiliation, methods, or findings from titles alone.
- Do not bypass CAPTCHAs, paywalls, robots rules, provider controls, or rate limits.

## Validation checklist

After changing a scraper or report schema:

```bash
make syntax
make report
```

Then check:

1. CSV headers and encoding.
2. Record counts and duplicate behavior.
3. Source URLs and retrieval dates.
4. Reviewed versus discovery evidence labels.
5. Legal status wording.
6. The generated `index.html` tables and charts.

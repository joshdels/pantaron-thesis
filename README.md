# Pantaron Range Land and Water Resources Research

A lightweight thesis workspace for assessing land and water-resource conditions in selected catchments associated with the Pantaron Range, Mindanao, Philippines. The project combines scholarly review, reported-problem and policy-source discovery, and a proposed remote-sensing/GIS assessment.

The research is being developed in a University of Southeastern Philippines (USeP) context. The exact study boundary, catchments, analysis periods, adviser requirements, and program-specific thesis format remain to be confirmed.

## Restart here after time away

1. Read `AGENTS.md` for evidence, academic-writing, remote-assessment, and harvesting rules.
2. Read `docs/research-plan.md` for the proposed objectives, scope, methods, and unresolved decisions.
3. Run `make syntax` to check the scripts.
4. Inspect the current CSV files in `outputs/data/`; do not assume every row is verified evidence.
5. Run `make report`, then open `index.html`.
6. Review the current legal status and recent problem sources before using them in thesis prose.

## Current evidence layers

The workspace deliberately separates three source types:

- **Scholarly metadata:** papers discovered through OpenAlex, Crossref, and Semantic Scholar. Metadata and abstracts are leads until the publication is appraised.
- **Reported Pantaron problems:** news, government, planning, project, and civil-society sources concerning forest, land, water, watershed, mining, drought, erosion, flooding, and governance issues.
- **Policy and law:** Pantaron-specific proposals, applicable Philippine laws, and selected international instruments. Relevance does not prove local implementation or enforcement.

The report distinguishes reviewed problem sources from unverified RSS leads. Search snippets and RSS descriptions must not be cited as if full articles were reviewed.

## Main commands

```bash
make help
make syntax
make scrape-openalex
make scrape-semantic
make scrape-web
make report
```

For a fresh web/RSS run that ignores cached responses:

```bash
python3 scripts/pantaron_web_harvester.py --provider auto --refresh
```

For a slower two-provider discovery run:

```bash
python3 scripts/pantaron_web_harvester.py \
  --provider both \
  --per-query 30 \
  --delay 10 \
  --refresh
```

## Important outputs

- `outputs/data/pantaron-land-water-problems.csv`: sanitized problem-focused table with research use and limitations.
- `outputs/data/pantaron-web-discovery.csv`: reviewed problem and policy baselines plus live RSS discoveries.
- `outputs/data/pantaron-web-sources-curated.csv`: earlier manually curated web-source export retained for traceability.
- `outputs/data/pantaron-rrl.csv`: OpenAlex/Crossref scholarly metadata output.
- `outputs/data/semantic-scholar-literature.csv`: Semantic Scholar metadata output.
- `index.html`: generated evidence report. Run `make report` to rebuild it.

Do not edit `index.html` for permanent changes. Update `scripts/report_generator.py` and regenerate the report.

## Workspace map

- `docs/`: research plan, methods, notes, and harvesting documentation
- `literature/`: literature matrix and critical-review records
- `scripts/`: harvesters and report generator; see `scripts/README.md`
- `outputs/data/`: generated CSV exports and discovery tables
- `outputs/`: generated maps, charts, and other results
- `data/`: source datasets added only when required
- `reports/`: optional thesis or submission drafts

## Evidence cautions

- Pantaron is a mountain range, not one watershed. Keep range boundaries and catchments distinct.
- A reported problem is not automatically a measured trend, proven cause, or range-wide condition.
- Remote indicators cannot by themselves establish usable water supply, groundwater yield, water quality, erosion rate, land ownership, or community preference.
- A proposed bill is not an enacted law. Recheck official legislative records before submission.
- Preserve uncertainty, source scope, date, and review status in every synthesis.

## Current research stage

The project remains at scope definition, source review, and feasibility assessment. No completed land/water analysis is claimed. The next substantive steps are to select defensible catchments and boundaries, appraise the strongest sources in full, verify candidate datasets and reference observations, and run a small terrain/land-cover/rainfall pilot.

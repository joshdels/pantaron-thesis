# Pantaron web-source harvesting

## Purpose

This collection supplements the scholarly literature matrix with news, government, planning, and legislative records that can help formulate a problem statement about land and water resources in and around the Pantaron Range. It is a discovery and scoping dataset, not a verified evidence base for final thesis claims.

## Files

- `outputs/data/pantaron-web-sources-curated.csv` contains records reviewed through the web research layer on 5 October 2026. It includes source titles, concise source-linked summaries, scope, issue tags, evidence status, search tier, and URL.
- `outputs/data/pantaron-web-discovery.csv` is the output of the automated GDELT harvester. The initial sandbox run returned zero records because DNS/network access to the GDELT API was unavailable; this is retained as an honest run artifact.
- `scripts/pantaron_web_harvester.py` queries the public GDELT 2.1 DOC API and writes discovery records. It uses metadata summaries only and does not bypass access controls.

## Interpretation cautions

The sources point to candidate problem themes: forest degradation and land conversion, mining/logging pressure, erosion and siltation, downstream flooding, dry-season/El Niño water stress, Indigenous and community governance, and unresolved protected-area legislation. These themes are not equivalent to measured rates or causal findings.

House Bill No. 7501 is recorded as referred to committee in the Senate legislative record. The dataset therefore reports a proposal and its recorded status, not a Pantaron protection law. Check the current House and Senate legislative systems again immediately before finalizing the thesis because bill status can change.

The next verification pass should inspect each source in full, retrieve the official legislative text/status, identify authoritative Pantaron boundary and hydrography data, and separate direct Pantaron observations from downstream or regional context.

## Rerun

From the repository root:

```bash
make scrape-web OUTPUT=outputs/data/pantaron-web-discovery.csv PER_QUERY=50
```

The Make target uses `WEB_OUTPUT`, `WEB_PER_QUERY`, and `WEB_DELAY`; this keeps it separate from the literature scraper's `OUTPUT` and `PER_TIER` variables. For a rate-limited run, use a smaller request and longer delay, for example:

```bash
make scrape-web WEB_OUTPUT=outputs/data/pantaron-web-discovery.csv WEB_PER_QUERY=20 WEB_DELAY=10
```

The queries are defined in `scripts/pantaron_web_harvester.py` and preserve the search tier in the output. Do not silently merge the discovery export into the curated CSV; deduplicate and review records first.

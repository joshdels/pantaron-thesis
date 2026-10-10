#!/usr/bin/env python3
"""Harvest literature metadata from the official Semantic Scholar API.

This creates a review queue. It does not download full text or decide relevance.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

FIELDS = [
    "year publication", "country", "authors", "title", "abstract",
    "possible methods used", "search tier", "source url",
]
TIERS = {
    "pantaron-local-context": "Pantaron Mountain Range land water watershed forest soil river resource management",
    "philippines-land-methods": "Philippines remote sensing GIS land cover forest fragmentation land capability soil erosion",
    "philippines-water-methods": "Philippines watershed rainfall drainage surface water water quality remote sensing GIS",
    "asia-integrated-methods": "Asia integrated land water resources management remote sensing GIS catchment validation",
    "global-validation-methods": "remote sensing GIS land water resource assessment accuracy field validation uncertainty",
}
METHODS = (
    ("remote sensing", "remote sensing"), ("gis", "GIS"), ("sentinel", "Sentinel"),
    ("landsat", "Landsat"), ("land cover", "land-cover mapping"),
    ("land use", "land-use mapping"), ("classification", "image classification"),
    ("random forest", "random forest"), ("machine learning", "machine learning"),
    ("deep learning", "deep learning"), ("weighted overlay", "weighted overlay"),
    ("analytic hierarchy", "AHP"), ("watershed", "watershed analysis"),
    ("catchment", "catchment analysis"), ("rainfall", "rainfall analysis"),
    ("precipitation", "rainfall analysis"), ("hydrologic", "hydrologic modeling"),
    ("drainage", "drainage analysis"), ("digital elevation", "DEM terrain analysis"),
    ("change detection", "change detection"),
    ("forest fragmentation", "forest-fragmentation analysis"),
    ("land capability", "land-capability evaluation"),
    ("soil erosion", "erosion-risk assessment"), ("rusle", "RUSLE erosion-risk modeling"),
    ("water quality", "water-quality assessment"),
    ("field validation", "field validation"), ("ground truth", "field validation"),
)


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def local_env(name: str) -> str:
    """Read a simple KEY=value from .env without requiring python-dotenv."""
    value = os.environ.get(name, "")
    if value:
        return value
    env_path = Path(".env")
    if not env_path.exists():
        return ""
    for line in env_path.read_text(encoding="utf-8").splitlines():
        key, separator, candidate = line.partition("=")
        if separator and key.strip() == name:
            return candidate.strip().strip('"\'')
    return ""


def methods(title: str, abstract: str) -> str:
    text = clean(f"{title} {abstract}").lower()
    found = []
    for phrase, label in METHODS:
        if phrase in text and label not in found:
            found.append(label)
    return " | ".join(found)


def request_json(url: str, api_key: str | None, retries: int) -> dict:
    headers = {"User-Agent": "pantaron-thesis-literature/1.0"}
    if api_key:
        headers["x-api-key"] = api_key
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504):
                raise
            if attempt >= retries:
                print("Warning: Semantic Scholar is still rate-limiting this request; skipping this tier.")
                return {}
            wait = 2 ** (attempt + 1)
            print(f"Semantic Scholar HTTP {exc.code}; waiting {wait}s")
            time.sleep(wait)
    return {}


def search(query: str, tier: str, limit: int, api_key: str | None, retries: int) -> list[dict]:
    fields = "title,abstract,year,authors,externalIds,url,publicationTypes"
    params = urllib.parse.urlencode({"query": query, "limit": min(limit, 100), "fields": fields})
    data = request_json(f"https://api.semanticscholar.org/graph/v1/paper/search?{params}", api_key, retries)
    rows = []
    for item in data.get("data", []):
        title = clean(item.get("title", ""))
        if not title or any(x in title.lower() for x in ("referee comment", "reviewer comment", "erratum", "correction")):
            continue
        abstract = clean(item.get("abstract", ""))
        authors = " | ".join(clean(a.get("name", "")) for a in item.get("authors", []) if a.get("name"))
        ids = item.get("externalIds") or {}
        doi = ids.get("DOI", "")
        rows.append({
            "year publication": item.get("year") or "", "country": "", "authors": authors,
            "title": title, "abstract": abstract,
            "possible methods used": methods(title, abstract), "search tier": tier,
            "source url": item.get("url") or (f"https://doi.org/{doi}" if doi else ""),
            "_dedupe": doi.lower() or f"{title.lower()}|{item.get('year') or ''}",
        })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", default="GIS remote sensing land water resources")
    parser.add_argument("--output", default="outputs/data/semantic-scholar-literature.csv")
    parser.add_argument("--per-tier", type=int, default=50)
    parser.add_argument("--api-key", help="optional Semantic Scholar API key")
    parser.add_argument("--delay", type=float, default=2.0)
    parser.add_argument("--retries", type=int, default=3)
    args = parser.parse_args()
    api_key = args.api_key or local_env("SEMANTIC_SCHOLAR_API_KEY")
    if api_key:
        print("Using Semantic Scholar API key from the command line or local environment.")
    rows = []
    for tier, extra in TIERS.items():
        rows.extend(search(f"{args.query} {extra}", tier, args.per_tier, api_key, args.retries))
        time.sleep(args.delay)
    unique = {}
    for row in rows:
        unique.setdefault(row.pop("_dedupe"), row)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(unique.values())
    print(f"Wrote {len(unique)} unique records to {output}")


if __name__ == "__main__":
    main()

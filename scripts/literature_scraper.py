#!/usr/bin/env python3
"""Harvest literature metadata for the Pantaron GIS/remote-sensing RRL.

Uses public OpenAlex and Crossref APIs. This is metadata discovery, not full-text
scraping or evidence verification. The output is a review queue in CSV format.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import time
import unicodedata
import urllib.parse
import urllib.request
import urllib.error
from datetime import date
from pathlib import Path

FIELDS = [
    "year publication",
    "country",
    "authors",
    "title",
    "abstract",
    "possible methods used",
    "search tier",
    "source url",
]
EXCLUDED_TITLE_PATTERNS = (
    r"\breferee comment\b",
    r"\breviewer comment\b",
    r"\breview comment\b",
    r"\bre[_ ]comments?\b",
    r"\bresponse to reviewers?\b",
    r"\bcorrection\b",
    r"\berratum\b",
    r"\bfront matter\b",
    r"\bback matter\b",
)

DEFAULT_QUERY = (
    "Pantaron OR Philippines GIS remote sensing land water resources "
    "catchment watershed rainfall land cover drainage"
)
TIERS = {
    "pantaron": "Pantaron",
    "philippines": "Philippines GIS remote sensing watershed rainfall land cover drainage",
    "asia": "Asia GIS remote sensing watershed rainfall land cover drainage",
    "global": "GIS remote sensing watershed rainfall land cover drainage",
}


def normalize(value: str) -> str:
    value = (
        unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode()
    )
    return re.sub(r"\W+", " ", value.lower()).strip()


def get_json(url: str, mailto: str | None = None, retries: int = 3) -> dict:
    headers = {
        "User-Agent": f"pantaron-thesis-literature/1.0 ({mailto or 'research use'})"
    }
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt >= retries:
                raise
            retry_after = exc.headers.get("Retry-After")
            wait = (
                int(retry_after)
                if retry_after and retry_after.isdigit()
                else 2 ** (attempt + 1)
            )
            print(
                f"Rate limited (429); waiting {wait}s before retry {attempt + 1}/{retries}"
            )
            time.sleep(wait)


def abstract_from_inverted_index(index: dict | None) -> str:
    if not index:
        return ""
    words = []
    for word, positions in index.items():
        for position in positions:
            words.append((position, word))
    return " ".join(word for _, word in sorted(words))


def clean_abstract(value: str) -> str:
    """Normalize provider markup without inventing or completing an abstract."""
    value = html.unescape(re.sub(r"<[^>]+>", " ", value or ""))
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r"^\s*(abstract|summary)\s*[:.]\s*", "", value, flags=re.I)
    return re.sub(r"\s+", " ", value).strip()


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def country_names(codes: set[str]) -> str:
    names = {
        "PH": "Philippines",
        "US": "United States",
        "GB": "United Kingdom",
        "AU": "Australia",
        "CA": "Canada",
        "IN": "India",
        "CN": "China",
        "JP": "Japan",
        "ID": "Indonesia",
        "MY": "Malaysia",
        "TH": "Thailand",
        "VN": "Vietnam",
        "DE": "Germany",
        "FR": "France",
        "NL": "Netherlands",
    }
    return "; ".join(sorted(names.get(code, code) for code in codes if code))


METHOD_HINTS = (
    ("remote sensing", "remote sensing"), ("gis", "GIS"),
    ("sentinel 2", "Sentinel-2"), ("sentinel-2", "Sentinel-2"),
    ("landsat", "Landsat"), ("ndvi", "NDVI"), ("land cover", "land-cover mapping"),
    ("land use", "land-use mapping"), ("classification", "image classification"),
    ("random forest", "random forest"), ("deep learning", "deep learning"),
    ("machine learning", "machine learning"), ("weighted overlay", "weighted overlay"),
    ("analytic hierarchy", "AHP"), ("ahp", "AHP"), ("dem", "DEM terrain analysis"),
    ("digital elevation", "DEM terrain analysis"), ("slope", "slope analysis"),
    ("drainage", "drainage analysis"), ("watershed", "watershed analysis"),
    ("catchment", "catchment analysis"), ("rainfall", "rainfall analysis"),
    ("precipitation", "rainfall analysis"), ("hydrologic", "hydrologic modeling"),
    ("change detection", "change detection"),
)


def possible_methods(title: str, abstract: str) -> str:
    text = normalize(f"{title} {abstract}")
    found = []
    for phrase, label in METHOD_HINTS:
        if normalize(phrase) in text and label not in found:
            found.append(label)
    return " | ".join(found)


def usable_title(title: str) -> bool:
    title = normalize(title)
    return bool(title) and not any(
        re.search(pattern, title, flags=re.I) for pattern in EXCLUDED_TITLE_PATTERNS
    )


def openalex(
    query: str, tier: str, limit: int, mailto: str | None, retries: int
) -> list[dict]:
    params = urllib.parse.urlencode({"search": query, "per-page": limit})
    url = f"https://api.openalex.org/works?{params}"
    data = get_json(url, mailto, retries)
    rows = []
    for item in data.get("results", []):
        authors = " | ".join(
            a.get("author", {}).get("display_name", "")
            for a in item.get("authorships", [])
            if a.get("author", {}).get("display_name")
        )
        countries = sorted(
            {c for a in item.get("authorships", []) for c in a.get("countries", [])}
        )
        primary = item.get("primary_location") or {}
        title = item.get("title") or ""
        if not usable_title(title):
            continue
        rows.append(
            {
                "year publication": item.get("publication_year") or "",
                "country": country_names(countries),
                "authors": authors,
                "title": clean_text(title),
                "abstract": clean_abstract(abstract_from_inverted_index(item.get("abstract_inverted_index"))),
                "possible methods used": possible_methods(title, abstract_from_inverted_index(item.get("abstract_inverted_index"))),
                "relevant": "",
                "search tier": tier,
                "doi": (item.get("doi") or "").replace("https://doi.org/", ""),
                "source url": item.get("doi") or item.get("id") or "",
            }
        )
    return rows


def crossref(
    query: str, tier: str, limit: int, mailto: str | None, retries: int
) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "query.bibliographic": query,
            "rows": limit,
            "select": "DOI,title,author,published,abstract,URL",
        }
    )
    data = get_json(f"https://api.crossref.org/works?{params}", mailto, retries)
    rows = []
    for item in data.get("message", {}).get("items", []):
        authors = " | ".join(
            " ".join(filter(None, [a.get("given"), a.get("family")]))
            for a in item.get("author", [])
            if a.get("given") or a.get("family")
        )
        date_parts = (item.get("published", {}).get("date-parts") or [[""]])[0]
        title = clean_text((item.get("title") or [""])[0])
        if not usable_title(title):
            continue
        abstract = clean_abstract(item.get("abstract", ""))
        doi = item.get("DOI", "")
        rows.append(
            {
                "year publication": date_parts[0] if date_parts else "",
                "country": "",
                "authors": authors,
                "title": title,
                "abstract": abstract,
                "possible methods used": possible_methods(title, abstract),
                "relevant": "",
                "search tier": tier,
                "doi": doi,
                "source url": item.get("URL", ""),
            }
        )
    return rows


def dedupe(rows: list[dict]) -> list[dict]:
    seen = set()
    output = []
    for row in rows:
        key = (
            f"doi:{normalize(row['doi'])}"
            if row["doi"]
            else f"title:{normalize(row['title'])}|{row['year publication']}"
        )
        if key in seen or not row["title"]:
            continue
        seen.add(key)
        output.append(row)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "query",
        nargs="?",
        default=DEFAULT_QUERY,
        help="search text; quote it as one argument",
    )
    parser.add_argument("--output", default="outputs/data/pantaron-literature.csv")
    parser.add_argument("--per-tier", type=int, default=25)
    parser.add_argument(
        "--provider", choices=("openalex", "crossref", "both"), default="both"
    )
    parser.add_argument("--mailto", help="email for polite API identification")
    parser.add_argument(
        "--delay", type=float, default=2.0, help="seconds between API requests"
    )
    parser.add_argument("--retries", type=int, default=3, help="retries after HTTP 429")
    parser.add_argument(
        "--no-tier-expansion", action="store_true", help="run only the supplied query"
    )
    args = parser.parse_args()
    tiers = (
        {"custom": args.query}
        if args.no_tier_expansion
        else {name: f"{args.query} {extra}" for name, extra in TIERS.items()}
    )
    rows = []
    for tier, query in tiers.items():
        if args.provider in ("openalex", "both"):
            try:
                rows.extend(
                    openalex(query, tier, args.per_tier, args.mailto, args.retries)
                )
            except urllib.error.URLError as exc:
                print(f"Warning: OpenAlex unavailable for tier {tier}: {exc}")
            time.sleep(args.delay)
        if args.provider in ("crossref", "both"):
            try:
                rows.extend(
                    crossref(query, tier, args.per_tier, args.mailto, args.retries)
                )
            except urllib.error.URLError as exc:
                print(f"Warning: Crossref unavailable for tier {tier}: {exc}")
            time.sleep(args.delay)
    rows = dedupe(rows)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} unique records to {output}")


if __name__ == "__main__":
    main()

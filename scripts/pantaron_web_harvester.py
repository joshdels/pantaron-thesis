#!/usr/bin/env python3
"""Harvest Pantaron land/water problem reports and relevant policy records.

Plan: use low-frequency RSS discovery instead of GDELT; add a transparent
catalogue of reviewed official policy records; clean, classify and deduplicate
the results; then write a spreadsheet-ready CSV. RSS entries remain discovery
leads, not full-text evidence. This script does not bypass access controls.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

FIELDS = [
    "record type", "title", "date published", "source/domain", "jurisdiction",
    "legal status", "location or scope", "issue tags", "summary",
    "evidence status", "search tier", "source url", "retrieved date",
]

PROBLEM_FIELDS = [
    "problem category", "reported condition", "relationship to Pantaron",
    "geographic scope", "source date", "source", "source type", "summary",
    "research use", "limitations", "evidence status", "source url",
    "retrieved date",
]

QUERIES = {
    # Keep RSS queries short. Bing in particular may return an empty feed for
    # long Boolean expressions even though ordinary search shows results.
    "pantaron-direct": '"Pantaron Mountain Range"',
    "pantaron-forest": 'Pantaron forest logging deforestation',
    "pantaron-mining-land": 'Pantaron mining land ancestral domain',
    "pantaron-water": 'Pantaron watershed river water Bukidnon',
    "pantaron-hazards": 'Pantaron drought flood erosion siltation',
    "pantaron-policy": 'Pantaron protected area national park bill',
}

ISSUE_WORDS = {
    "deforestation/forest degradation": ("deforestation", "forest loss", "forest degradation", "logging", "denuded"),
    "mining/extractive activity": ("mining", "mine", "mercury", "tailings", "extractive"),
    "land conversion/agriculture": ("land conversion", "agriculture", "plantation", "settlement"),
    "water quality/sedimentation": ("siltation", "sediment", "pollution", "water quality", "contamination"),
    "flooding/erosion": ("flood", "erosion", "landslide", "runoff"),
    "drought/water shortage": ("drought", "dry spell", "el niño", "water shortage", "below-normal rainfall"),
    "watershed/headwaters": ("watershed", "headwater", "river", "water resource"),
    "protected-area policy": ("protected area", "national park", "nipas", "bill", "law"),
    "Indigenous/community governance": ("lumad", "indigenous", "ancestral", "community", "fpic"),
    "biodiversity/wildlife": ("biodiversity", "wildlife", "endemic", "habitat"),
    "climate adaptation": ("climate", "adaptation", "el niño"),
}

# Reviewed official sources. Recheck time-sensitive bill status before thesis submission.
POLICY_RECORDS = (
    ("House Bill No. 7501: proposed Pantaron Mountain Range National Park and Watershed", "2020-08-26", "Senate Legislative Reference Bureau", "local/Pantaron; Philippines", "bill; referred to House Committee on Natural Resources on 2020-09-01; not enacted in this record", "Pantaron Mountain Range", "protected-area policy | watershed/headwaters | biodiversity/wildlife", "Proposed declaring the Pantaron Mountain Range a protected area categorized as a national park and watershed. The 18th Congress record reports information as of 20 April 2022.", "pantaron-policy", "https://issuances-library.senate.gov.ph/bills/house-bill-no-7501-18th-congress-republic"),
    ("Republic Act No. 11038: Expanded National Integrated Protected Areas System Act of 2018", "2018-06-22", "Lawphil", "national; Philippines", "enacted national law", "Philippine protected areas; Pantaron designation and boundaries require verification", "protected-area policy | biodiversity/wildlife | Indigenous/community governance", "Amends the NIPAS Act and provides a national framework for declaring and managing protected areas. It does not by itself establish that the entire Pantaron Range is protected.", "national-policy", "https://lawphil.net/statutes/repacts/ra2018/ra_11038_2018.html"),
    ("Republic Act No. 8371: Indigenous Peoples' Rights Act of 1997", "1997-10-29", "Lawphil", "national; Philippines", "enacted national law", "Indigenous communities, ancestral domains, lands and natural resources", "Indigenous/community governance | watershed/headwaters | land conversion/agriculture", "Recognizes Indigenous Peoples' rights, including ancestral-domain rights and free and prior informed consent as defined by the Act. Site-specific application requires verified tenure and project records.", "national-policy", "https://lawphil.net/statutes/repacts/ra1997/ra_8371_1997.html"),
    ("Republic Act No. 9275: Philippine Clean Water Act of 2004", "2004-03-22", "Lawphil", "national; Philippines", "enacted national law", "All Philippine water bodies; principally pollution from land-based sources", "water quality/sedimentation | watershed/headwaters", "Establishes a comprehensive water-quality management framework, including pollution prevention, discharge controls and accountability. It does not prove local Pantaron contamination.", "national-policy", "https://lawphil.net/statutes/repacts/ra2004/ra_9275_2004.html"),
    ("Republic Act No. 9147: Wildlife Resources Conservation and Protection Act", "2001-07-30", "Lawphil", "national; Philippines", "enacted national law", "Philippine wildlife and habitats", "biodiversity/wildlife | protected-area policy", "Provides for wildlife-resource conservation and protection. Pantaron-specific species, habitats and enforcement require separate evidence.", "national-policy", "https://lawphil.net/statutes/repacts/ra2001/ra_9147_2001.html"),
    ("Republic Act No. 9729: Climate Change Act of 2009", "2009-10-23", "Lawphil", "national; Philippines", "enacted national law", "National and local climate planning, including water, agriculture and forestry", "climate adaptation | drought/water shortage | flooding/erosion | watershed/headwaters", "Requires climate change to be mainstreamed into planning and identifies water resources, agriculture and forestry as climate-sensitive sectors. It is not evidence of Pantaron impacts.", "national-policy", "https://lawphil.net/statutes/repacts/ra2009/ra_9729_2009.html"),
    ("Convention on Biological Diversity: Philippines country profile", "1994-01-06", "Convention on Biological Diversity", "international; Philippines as Party", "international convention; in force for the Philippines", "National biodiversity conservation and reporting; not Pantaron-specific", "biodiversity/wildlife | protected-area policy", "The official profile records the Philippines as a Party since 6 January 1994 and links national biodiversity strategies and reports. Pantaron relevance requires national implementation evidence.", "international-policy", "https://www.cbd.int/countries?country=ph"),
    ("United Nations Declaration on the Rights of Indigenous Peoples", "2007-09-13", "United Nations", "international", "UN General Assembly declaration; not a treaty", "Global minimum standards concerning Indigenous Peoples", "Indigenous/community governance | land conversion/agriculture | watershed/headwaters", "Sets an international framework concerning Indigenous Peoples' survival, dignity, well-being, lands, territories and resources. It is not a Philippine statute or Pantaron-specific law.", "international-policy", "https://www.un.org/development/desa/indigenouspeoples/declaration-on-the-rights-of-indigenous-peoples.html"),
)

REVIEWED_PROBLEM_RECORDS = (
    ("‘Insurgent-free’ Pantaron Mountain Range eyed as protected area", "2022-05-02", "Philippine News Agency", "Pantaron in Davao del Norte and Bukidnon; reported headwater context", "watershed/headwaters | deforestation/forest degradation | protected-area policy", "Reports a proposal to pursue protected-area status and describes the range as an old-growth/residual forest and headwater source. This is reporting on an initiative, not proof of enactment.", "https://www.pna.gov.ph/articles/1183395"),
    ("Lumad, peasant groups unite to defend Pantaron Range", "2018-08-16", "Davao Today", "Pantaron across parts of six Mindanao provinces", "Indigenous/community governance | watershed/headwaters | protected-area policy", "Reports community and peasant-group advocacy concerning Pantaron and claims connections to regional watersheds. Exact catchment relationships require authoritative hydrographic verification.", "https://davaotoday.com/environment/lumad-peasant-groups-unite-to-defend-pantaron-range/"),
    ("MinDA Mindanao 2020: watershed and groundwater discussion", "2020", "Mindanao Development Authority", "Agusan and Compostela Valley downstream context associated with Pantaron", "deforestation/forest degradation | flooding/erosion | water quality/sedimentation | mining/extractive activity", "The planning document discusses forest degradation, runoff, erosion, siltation, pollution, downstream flooding and mining-related risks. These are planning-document claims requiring site-specific evaluation.", "https://minda.gov.ph/resources/Publications/Mindanao_2020/m2020_full_doc_for_web.pdf"),
    ("El Niño takes toll on Bukidnon rice farms", "2026-09-03", "Inquirer", "Banlag, Valencia City, Bukidnon; includes upland fields identified as Pantaron", "drought/water shortage | climate adaptation | land conversion/agriculture", "Reports below-normal rainfall, dried local water sources, scheduled irrigation deliveries and insufficient pumping in parts of Valencia. It documents a local episode, not a range-wide hydrologic condition.", "https://newsinfo.inquirer.net/2298487/el-nino-takes-toll-on-bukidnon-rice-farms/amp"),
    ("DavNor PENRO works for declaration of Pantaron Range as local protected area", "2023-11-30", "Philippine Information Agency", "Davao del Norte portion of Pantaron", "protected-area policy | biodiversity/wildlife | watershed/headwaters", "Reports that provincial and DENR offices were still pursuing national or local conservation status and preparing biodiversity and social documentation. This indicates an unresolved protection and management process, not degradation measurements.", "https://pia.gov.ph/news/davnor-penro-works-for-declaration-of-pantaron-range-as-local-protected-area/"),
    ("Government leaders seek support for Tagum-Libuganon river-basin protection", "2024-03-27", "Philippine Information Agency", "Pantaron-linked Tagum-Libuganon River Basin", "watershed/headwaters | climate adaptation | protected-area policy", "Reports adoption of a river-basin master-plan cooperation framework, calls to protect Pantaron headwaters, and official concern about river-basin vulnerability and a looming water crisis. It does not quantify Pantaron water supply or causation.", "https://pia.gov.ph/news/govt-leaders-seek-public-support-for-protection-of-tagum-libuganon-river-basin/"),
    ("Protecting watersheds and ancestral domain", "2015", "Foundation for the Philippine Environment", "Pantaron Range ancestral-domain and watershed project context", "Indigenous/community governance | mining/extractive activity | land conversion/agriculture | biodiversity/wildlife", "Discusses tensions between ancestral-domain governance, biodiversity conservation, mining interests, monocrop expansion and commercial operations. It is a project impact narrative rather than an independent range-wide assessment.", "https://www.fpe.ph/impact_story/protecting-watersheds-and-ancestral-domain/6"),
    ("Tokenism in environment conservation: the case of Bukidnon's major uplands", "2011-04-18", "MindaNews", "Bukidnon uplands including Pantaron", "mining/extractive activity | deforestation/forest degradation | drought/water shortage | Indigenous/community governance | land conversion/agriculture", "Reports concerns about mining exploration applications, forest conversion, uncertain Indigenous consent and competition for Sawaga River water during drought. Claims are historical reporting and require updated permits, land-cover evidence and hydrologic data.", "https://mindanews.com/special-reports/2011/04/tokenism-in-environment-conservation-the-case-of-bukidnon%E2%80%99s-major-uplands-2/"),
    ("Nature's Neighbours: sustainable coexistence in Pantaron", "", "Landscape Alliance", "Pantaron primary-forest and Tigwahanon community project area", "deforestation/forest degradation | land conversion/agriculture | Indigenous/community governance | climate adaptation", "Describes fragmented primary forests and pressures attributed to deforestation, unsustainable cultivation and changing climate conditions, alongside restoration and community co-management responses. Treat as a project description, not a measured trend report.", "https://www.landscapealliance.org/project/naturesneighbors/"),
)

PROBLEM_DETAILS = {
    "https://www.pna.gov.ph/articles/1183395": ("forest protection and watershed governance", "Remaining forest and headwater areas were reported as needing protected-area status.", "direct Pantaron report", "Use to frame protection/governance concern.", "Does not quantify forest loss or water condition; some page access may be restricted."),
    "https://davaotoday.com/environment/lumad-peasant-groups-unite-to-defend-pantaron-range/": ("Indigenous governance and watershed protection", "Community groups reported pressure on ancestral lands and advocated protection of the range and watersheds.", "direct Pantaron report", "Use for stakeholder and governance context.", "Advocacy/news source; hydrographic claims need authoritative verification."),
    "https://minda.gov.ph/resources/Publications/Mindanao_2020/m2020_full_doc_for_web.pdf": ("forest degradation, erosion, siltation and pollution", "Planning document reports degradation and mining-related risks affecting Pantaron-linked basins and downstream areas.", "Pantaron-linked basin context", "Use to identify candidate land-water pathways for testing.", "Historical planning synthesis; does not establish current site-specific rates or causality."),
    "https://newsinfo.inquirer.net/2298487/el-nino-takes-toll-on-bukidnon-rice-farms/amp": ("drought and agricultural water shortage", "Below-normal rainfall and drying local sources affected farms, including upland fields identified as Pantaron.", "local Pantaron-adjacent/direct locality report", "Use as a recent water-stress case requiring rainfall and location verification.", "Single event and locality; cannot represent the whole range."),
    "https://pia.gov.ph/news/davnor-penro-works-for-declaration-of-pantaron-range-as-local-protected-area/": ("incomplete protected-area coverage and management", "Agencies were still assembling support for national or local conservation designation.", "direct Pantaron governance report", "Use to document unresolved institutional protection as of the source date.", "A proposal/status report, not evidence of environmental condition or current 2026 legal status."),
    "https://pia.gov.ph/news/govt-leaders-seek-public-support-for-protection-of-tagum-libuganon-river-basin/": ("river-basin vulnerability and fragmented governance", "Officials linked Pantaron headwater protection to river-basin management and raised water-crisis concerns.", "Pantaron-linked river-basin context", "Use for current planning and governance rationale.", "Official statements and planning actions do not quantify hydrologic trends."),
    "https://www.fpe.ph/impact_story/protecting-watersheds-and-ancestral-domain/6": ("resource-use conflict and ancestral-domain governance", "Project narrative identifies mining and monocrop/commercial pressures as governance concerns.", "direct Pantaron project context", "Use to identify social and land-use questions for corroboration.", "Project/impact narrative; not independent impact measurement."),
    "https://mindanews.com/special-reports/2011/04/tokenism-in-environment-conservation-the-case-of-bukidnon%E2%80%99s-major-uplands-2/": ("mining, forest conversion and water-allocation conflict", "Historical reporting describes exploration interest, forest-conversion concern and drought-period competition for river water.", "Pantaron and Bukidnon upland context", "Use as historical lead for updated permit, land-cover and water-allocation review.", "Old source; all permits, projects and conditions require current verification."),
    "https://www.landscapealliance.org/project/naturesneighbors/": ("forest fragmentation and unsustainable cultivation", "Project description reports fragmented primary forest and cultivation/climate pressures.", "direct Pantaron project context", "Use to locate restoration and co-management initiatives.", "Project description; no independently verified change rate supplied."),
}


def clean(value: str) -> str:
    value = html.unescape(re.sub(r"<[^>]+>", " ", value or ""))
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", value)).strip()


def normalize(value: str) -> str:
    return re.sub(r"\W+", " ", clean(value).lower()).strip()


def classify(text: str) -> str:
    low = clean(text).lower()
    return " | ".join(label for label, words in ISSUE_WORDS.items() if any(word in low for word in words))


def fetch(url: str, cache_dir: Path, cache_hours: float, retries: int = 4) -> bytes:
    cache = cache_dir / (hashlib.sha256(url.encode()).hexdigest() + ".xml")
    if cache.exists() and time.time() - cache.stat().st_mtime <= cache_hours * 3600:
        return cache.read_bytes()
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; PantaronThesisResearch/2.0)"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = response.read()
            cache_dir.mkdir(parents=True, exist_ok=True)
            cache.write_bytes(payload)
            return payload
        except urllib.error.HTTPError as exc:
            if attempt >= retries or exc.code not in (429, 500, 502, 503, 504):
                raise
            header = exc.headers.get("Retry-After")
            wait = float(header) if header and header.isdigit() else min(60, 5 * (2 ** attempt))
            print(f"HTTP {exc.code}; waiting {wait:g}s before retry {attempt + 1}/{retries}")
            time.sleep(wait)
    raise RuntimeError("request retries exhausted")


def rss_url(provider: str, query: str) -> str:
    encoded = urllib.parse.quote_plus(query)
    if provider == "bing":
        return f"https://www.bing.com/news/search?q={encoded}&format=rss"
    return f"https://news.google.com/rss/search?q={encoded}&hl=en-PH&gl=PH&ceid=PH:en"


def child_text(item: ET.Element, name: str) -> str:
    element = item.find(name)
    return clean(element.text if element is not None and element.text else "")


def rss_records(payload: bytes, tier: str, provider: str, limit: int) -> tuple[list[dict], int]:
    root = ET.fromstring(payload)
    records = []
    items = root.findall(".//item")
    for item in items[:limit]:
        title, link = child_text(item, "title"), child_text(item, "link")
        description = child_text(item, "description")
        if not title or not link:
            continue
        records.append({
            "record type": "news/article discovery", "title": title,
            "date published": child_text(item, "pubDate"),
            "source/domain": child_text(item, "source") or urllib.parse.urlparse(link).netloc,
            "jurisdiction": "not assessed", "legal status": "not applicable",
            "location or scope": "Pantaron or nearby context; verify in linked source",
            "issue tags": classify(f"{title} {description}"),
            "summary": description or "No RSS description supplied; inspect the linked source.",
            "evidence status": f"RSS discovery lead from {provider}; full source not yet appraised",
            "search tier": tier, "source url": link, "retrieved date": date.today().isoformat(),
        })
    return records, len(items)


def policy_records() -> list[dict]:
    rows = []
    for title, published, source, jurisdiction, status, scope, tags, summary, tier, url in POLICY_RECORDS:
        rows.append({"record type": "policy/legal record", "title": title, "date published": published,
                     "source/domain": source, "jurisdiction": jurisdiction, "legal status": status,
                     "location or scope": scope, "issue tags": tags, "summary": summary,
                     "evidence status": "official source reviewed; recheck current bill status and amendments",
                     "search tier": tier, "source url": url, "retrieved date": date.today().isoformat()})
    return rows


def reviewed_problem_records() -> list[dict]:
    rows = []
    for title, published, source, scope, tags, summary, url in REVIEWED_PROBLEM_RECORDS:
        rows.append({"record type": "reviewed problem source", "title": title,
                     "date published": published, "source/domain": source,
                     "jurisdiction": "local/regional context", "legal status": "not applicable",
                     "location or scope": scope, "issue tags": tags, "summary": summary,
                     "evidence status": "reviewed source or indexed source text; consult full source before citation",
                     "search tier": "pantaron-reviewed", "source url": url,
                     "retrieved date": date.today().isoformat()})
    return rows


def dedupe(rows: list[dict]) -> list[dict]:
    seen_urls, seen_titles, output = set(), set(), []
    for row in rows:
        url_key = row["source url"].split("?")[0].rstrip("/").lower()
        title_key = normalize(row["title"])
        if (url_key and url_key in seen_urls) or title_key in seen_titles:
            continue
        seen_urls.add(url_key); seen_titles.add(title_key); output.append(row)
    return output


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)


def write_problem_csv(path: Path, rows: list[dict]) -> None:
    clean_rows = []
    for row in rows:
        if row["record type"] not in ("reviewed problem source", "news/article discovery"):
            continue
        details = PROBLEM_DETAILS.get(row["source url"])
        if details:
            category, condition, relationship, research_use, limitations = details
        else:
            category = row["issue tags"] or "unclassified; manual review needed"
            condition = row["summary"]
            relationship = "RSS discovery result; Pantaron relationship not yet verified"
            research_use = "Screen for relevance, then inspect and verify the full source."
            limitations = "Automated discovery metadata only; exclude from thesis claims until reviewed."
        clean_rows.append({
            "problem category": category, "reported condition": condition,
            "relationship to Pantaron": relationship,
            "geographic scope": row["location or scope"], "source date": row["date published"],
            "source": row["source/domain"],
            "source type": "reviewed source" if row["record type"] == "reviewed problem source" else "RSS discovery lead",
            "summary": row["summary"], "research use": research_use,
            "limitations": limitations, "evidence status": row["evidence status"],
            "source url": row["source url"], "retrieved date": row["retrieved date"],
        })
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=PROBLEM_FIELDS)
        writer.writeheader(); writer.writerows(clean_rows)
    print(f"Wrote {len(clean_rows)} sanitized problem records to {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="outputs/data/pantaron-web-discovery.csv")
    parser.add_argument("--problems-output", default="outputs/data/pantaron-land-water-problems.csv")
    parser.add_argument("--provider", choices=("auto", "bing", "google", "both", "none"), default="auto",
                        help="auto tries Google News then Bing; both collects both feeds")
    parser.add_argument("--per-query", type=int, default=20)
    parser.add_argument("--delay", type=float, default=5.0)
    parser.add_argument("--cache-dir", default="outputs/data/.web-cache")
    parser.add_argument("--cache-hours", type=float, default=24.0)
    parser.add_argument("--refresh", action="store_true", help="ignore cached RSS responses for this run")
    parser.add_argument("--no-policies", action="store_true")
    args = parser.parse_args()
    if args.refresh:
        args.cache_hours = 0
    if not 1 <= args.per_query <= 100:
        parser.error("--per-query must be between 1 and 100")

    rows = reviewed_problem_records()
    if not args.no_policies:
        rows.extend(policy_records())
    if args.provider == "none":
        providers = ()
    elif args.provider in ("auto", "both"):
        providers = ("google", "bing")
    else:
        providers = (args.provider,)
    for tier, query in QUERIES.items():
        for provider in providers:
            try:
                found, feed_items = rss_records(
                    fetch(rss_url(provider, query), Path(args.cache_dir), args.cache_hours),
                    tier, provider, args.per_query,
                )
                rows.extend(found)
                print(f"{provider}: {tier}: feed contained {feed_items} items; accepted {len(found)} records")
                if found and args.provider == "auto":
                    break
            except (urllib.error.URLError, urllib.error.HTTPError, ET.ParseError, OSError) as exc:
                print(f"Warning: {provider} RSS unavailable for {tier}: {exc}")
            time.sleep(args.delay)

    rows = dedupe(rows)
    write_csv(Path(args.output), rows)
    write_problem_csv(Path(args.problems_output), rows)
    news = sum(row["record type"] == "news/article discovery" for row in rows)
    policies = sum(row["record type"] == "policy/legal record" for row in rows)
    reviewed = sum(row["record type"] == "reviewed problem source" for row in rows)
    print(f"Wrote {len(rows)} records ({news} RSS news, {reviewed} reviewed problems, {policies} policy) to {args.output}")


if __name__ == "__main__":
    main()

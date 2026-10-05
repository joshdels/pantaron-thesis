#!/usr/bin/env python3
"""Generate the Pantaron research hub from compatible CSV exports."""

from __future__ import annotations

import argparse
import csv
import html
import re
from collections import Counter
from datetime import date
from pathlib import Path


def clean(value: object) -> str:
    return str(value or "").strip()


def esc(value: object) -> str:
    return html.escape(clean(value))


def read_rows(input_dir: Path) -> tuple[list[dict], list[str]]:
    rows, files = [], []
    for path in sorted(input_dir.glob("*.csv")):
        files.append(path.name)
        with path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                if any(clean(value) for value in row.values()):
                    row["_file"] = path.name
                    rows.append(row)
    return rows, files


def unique_literature(rows: list[dict]) -> list[dict]:
    selected: dict[tuple[str, str], dict] = {}
    for row in rows:
        if "year publication" not in row or not clean(row.get("title")):
            continue
        title = re.sub(r"[^a-z0-9]+", " ", clean(row.get("title")).lower()).strip()
        key = title, clean(row.get("year publication"))
        old = selected.get(key)
        if old is None or (not clean(old.get("abstract")) and clean(row.get("abstract"))):
            selected[key] = row
    return sorted(selected.values(), key=lambda r: (clean(r.get("search tier")), clean(r.get("title")).lower()))


def values(rows: list[dict], field: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in rows:
        for value in clean(row.get(field)).split("|"):
            if value.strip():
                counts[value.strip()] += 1
    return counts


def chart(counts: Counter[str], title: str, accent: str = "green", limit: int = 12) -> str:
    items = counts.most_common(limit)
    if not items:
        return f'<article class="chart"><h3>{html.escape(title)}</h3><p class="muted">No values available.</p></article>'
    largest = max(value for _, value in items)
    bars = "".join(
        '<div class="bar"><span title="{0}">{0}</span><i><b class="{2}" style="width:{3}%"></b></i><strong>{1}</strong></div>'.format(
            html.escape(label), value, accent, max(3, round(value / largest * 100))
        )
        for label, value in items
    )
    return f'<article class="chart"><h3>{html.escape(title)}</h3>{bars}</article>'


def problem_themes(rows: list[dict]) -> Counter[str]:
    themes = {
        "Forest loss and degradation": ("forest", "deforestation", "logging"),
        "Watershed and river governance": ("watershed", "headwater", "river basin"),
        "Indigenous and ancestral domain": ("indigenous", "ancestral", "lumad"),
        "Mining and extractive pressure": ("mining", "extractive", "tailings"),
        "Drought and water shortage": ("drought", "water shortage", "el niño"),
        "Erosion, flooding and sediment": ("erosion", "flood", "siltation", "sediment"),
        "Land conversion and agriculture": ("land conversion", "agriculture", "plantation"),
        "Water quality and pollution": ("water quality", "pollution", "contamination"),
    }
    counts: Counter[str] = Counter()
    for row in rows:
        text = " ".join(clean(row.get(k)) for k in ("problem category", "reported condition", "summary")).lower()
        for label, terms in themes.items():
            if any(term in text for term in terms):
                counts[label] += 1
    return counts


def policy_group(status: str) -> str:
    value = status.lower()
    if "bill" in value or "proposal" in value:
        return "Bill or proposal (not enacted)"
    if "enacted" in value:
        return "Enacted national law"
    if "convention" in value:
        return "International convention"
    if "declaration" in value:
        return "International declaration"
    return "Other or unspecified"


def scope(tier: str) -> str:
    value = tier.lower()
    if "pantaron" in value or "local" in value:
        return "Pantaron / local"
    if "philippine" in value or "national" in value:
        return "Philippines"
    if "asia" in value:
        return "Asia"
    if "global" in value or "international" in value:
        return "International / global"
    return "Other / unspecified"


def link(row: dict, field: str) -> str:
    label, url = esc(row.get(field)) or "Untitled", clean(row.get("source url"))
    return f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{label}</a>' if url else label


def search(table_id: str, label: str) -> str:
    return f'<div class="tools"><label for="q-{table_id}">{label}</label><input id="q-{table_id}" data-table="{table_id}" type="search" placeholder="Search this table…"><span data-count="{table_id}"></span></div>'


def card(label: str, value: int, note: str) -> str:
    return f'<article class="card"><small>{label}</small><strong>{value}</strong><span>{note}</span></article>'


def make_report(rows: list[dict], files: list[str]) -> str:
    literature = unique_literature(rows)
    problems = [r for r in rows if r.get("_file") == "pantaron-land-water-problems.csv"]
    policies = [r for r in rows if clean(r.get("record type")).lower() == "policy/legal record"]
    reviewed = [r for r in problems if clean(r.get("source type")).lower() == "reviewed source"]
    leads = [r for r in problems if r not in reviewed]
    abstracts = sum(bool(clean(r.get("abstract"))) for r in literature)

    def problem_rows(selected: list[dict]) -> str:
        return "".join(
            f'<tr><td>{n}</td><td><b>{esc(r.get("problem category"))}</b></td><td>{esc(r.get("reported condition"))}</td>'
            f'<td>{esc(r.get("relationship to Pantaron"))}</td><td>{esc(r.get("geographic scope"))}</td>'
            f'<td>{link(r,"source")}<small>{esc(r.get("source date"))}</small></td><td>{esc(r.get("research use"))}</td><td>{esc(r.get("limitations"))}</td></tr>'
            for n, r in enumerate(selected, 1)
        ) or '<tr><td colspan="8">No records found.</td></tr>'

    policy_rows = "".join(
        f'<tr><td>{n}</td><td>{link(r,"title")}</td><td>{esc(r.get("jurisdiction"))}</td>'
        f'<td><em>{html.escape(policy_group(clean(r.get("legal status"))))}</em><small>{esc(r.get("legal status"))}</small></td>'
        f'<td>{esc(r.get("summary"))}</td><td>{esc(r.get("evidence status"))}</td></tr>'
        for n, r in enumerate(policies, 1)
    ) or '<tr><td colspan="6">No policy records found.</td></tr>'

    literature_rows = "".join(
        f'<tr><td>{n}</td><td>{esc(r.get("year publication"))}</td><td>{esc(r.get("country")) or "<i>Not supplied</i>"}</td>'
        f'<td>{link(r,"title")}<small>{esc(r.get("authors"))}</small></td>'
        f'<td class="abstract">{esc(r.get("abstract")) or "<i>No abstract supplied by provider</i>"}</td>'
        f'<td>{esc(r.get("possible methods used")) or "<i>No keyword hint</i>"}</td>'
        f'<td><em>{html.escape(scope(clean(r.get("search tier"))))}</em><small>Tier: {esc(r.get("search tier"))}</small></td></tr>'
        for n, r in enumerate(literature, 1)
    ) or '<tr><td colspan="7">No literature records found.</td></tr>'

    methods = values(literature, "possible methods used")
    policy_counts = Counter(policy_group(clean(r.get("legal status"))) for r in policies)
    scope_counts = Counter(scope(clean(r.get("search tier"))) for r in literature)
    top_method = methods.most_common(1)
    method_sentence = (
        f'The most frequent metadata hint is <b>{html.escape(top_method[0][0])}</b> ({top_method[0][1]} records). '
        if top_method else "No method hints are available. "
    )
    literature_section = ""
    if literature:
        literature_section = f'''<section id="methods" class="block"><div class="heading"><span class="kicker">03 · METHODS &amp; RRL</span><h2>Methods and related literature</h2><p>{method_sentence}These are keyword-based discovery hints, not verified descriptions of study procedures. Appraise the full paper before adoption.</p></div><div class="charts">{chart(methods,"Possible methods in metadata","teal")}{chart(scope_counts,"Coverage of the search strategy","teal")}{chart(values(literature,"search tier"),"Records by search tier","teal")}{chart(Counter(clean(r.get("year publication")) or "Unknown" for r in literature),"Publication years","teal")}</div>{search("literature-table","Find a study or method")}<div class="wrap rrl"><table id="literature-table"><thead><tr><th>No.</th><th>Year</th><th>Country</th><th>Study and authors</th><th>Abstract</th><th>Possible methods</th><th>Search coverage</th></tr></thead><tbody>{literature_rows}</tbody></table></div></section>'''
    sources = "".join(f'<li><code>{html.escape(name)}</code></li>' for name in files)

    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Joshua De Leon | Pantaron Research Hub</title><style>
:root{{--ink:#17241f;--muted:#617069;--forest:#174f3b;--teal:#168797;--gold:#d5a93d;--paper:#f4f6f1;--line:#d8ded8;--pale:#eaf2ed}}*{{box-sizing:border-box}}html{{scroll-behavior:smooth;scroll-padding-top:75px}}body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.6 system-ui,sans-serif}}a{{color:#176c50;text-underline-offset:3px}}.top{{position:sticky;top:0;z-index:5;background:#103d2ff2;color:white;padding:14px max(20px,calc((100% - 1500px)/2));display:flex;justify-content:space-between;gap:20px;backdrop-filter:blur(10px)}}nav a{{color:#e6f4ed;text-decoration:none;margin-left:18px;font-size:13px}}.hero{{background:radial-gradient(circle at 85% 15%,#2c7d61 0,transparent 27%),linear-gradient(130deg,#10382b,#174f3b);color:white}}.hero>div{{max-width:1500px;margin:auto;padding:70px 40px 60px;display:grid;grid-template-columns:2fr 1fr;gap:50px;align-items:end}}.kicker{{color:#86d0b4;text-transform:uppercase;letter-spacing:.15em;font-size:12px;font-weight:800}}h1,h2{{font-family:Georgia,serif;font-weight:600;letter-spacing:-.025em}}h1{{font-size:clamp(42px,6vw,76px);line-height:1;margin:12px 0 22px}}.hero p{{color:#d7e9e1;font-size:18px;max-width:850px}}.owner{{border-left:1px solid #ffffff55;padding-left:25px}}.owner b{{display:block;font-size:20px}}main{{max-width:1500px;margin:auto;padding:32px 40px 75px}}.notice{{background:#fff8e6;border:1px solid #ead69b;border-left:5px solid var(--gold);padding:17px 20px;border-radius:10px}}.cards{{display:grid;grid-template-columns:repeat(5,1fr);gap:13px;margin:26px 0 45px}}.card,.chart{{background:white;border:1px solid var(--line);border-radius:13px;box-shadow:0 4px 15px #173d2f0a}}.card{{padding:19px}}.card small{{display:block;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);font-weight:700}}.card strong{{display:block;font:600 34px Georgia,serif;color:var(--forest);margin:6px 0}}.card span{{font-size:12px;color:var(--muted)}}section.block{{padding:45px 0 25px;border-top:1px solid var(--line)}}.heading{{display:grid;grid-template-columns:.7fr 1.3fr;gap:45px;align-items:end;margin-bottom:25px}}.heading .kicker{{grid-column:1/-1;color:#247357}}h2{{font-size:clamp(31px,3.5vw,45px);line-height:1.1;margin:0}}.heading p{{color:var(--muted);font-size:16px;margin:0}}.charts{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:20px 0 32px}}.chart{{padding:23px}}.chart h3{{margin:0 0 18px}}.bar{{display:grid;grid-template-columns:minmax(150px,1fr) minmax(100px,1.5fr) 35px;gap:11px;align-items:center;margin:11px 0;font-size:13px}}.bar i{{height:10px;background:#e4ebe6;border-radius:99px;overflow:hidden}}.bar b{{display:block;height:100%;background:linear-gradient(90deg,var(--forest),#64aa86)}}.bar b.gold{{background:linear-gradient(90deg,#a87714,var(--gold))}}.bar b.teal{{background:linear-gradient(90deg,var(--teal),#68bdbe)}}.bar strong{{text-align:right}}.tools{{display:flex;align-items:center;gap:12px;margin:12px 0}}.tools label{{font-weight:700}}.tools input{{width:min(580px,100%);padding:10px 12px;border:1px solid #bdc9c1;border-radius:8px;font:inherit}}.tools span{{color:var(--muted);font-size:13px}}.wrap{{overflow:auto;max-height:740px;border:1px solid var(--line);border-radius:11px;background:white}}.rrl{{max-height:900px}}table{{border-collapse:separate;border-spacing:0;width:100%;min-width:1280px;font-size:13.5px}}th,td{{padding:14px 15px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}th{{position:sticky;top:0;z-index:2;background:var(--pale);font-size:11px;text-transform:uppercase;letter-spacing:.05em;white-space:nowrap}}tbody tr:hover{{background:#f8fbf8}}td:first-child,th:first-child{{width:52px;text-align:center;color:var(--muted)}}td.abstract{{min-width:430px;max-width:680px}}td small{{display:block;color:var(--muted);margin-top:6px}}td em{{display:inline-block;font-style:normal;font-size:11px;font-weight:700;background:#e5f2eb;color:var(--forest);padding:3px 8px;border-radius:99px}}td i{{color:#87928d}}details{{margin-top:16px;background:white;border:1px solid var(--line);border-radius:11px}}summary{{cursor:pointer;padding:16px 19px;font-weight:700;color:var(--forest)}}details .wrap{{border:0;border-radius:0}}.sources{{padding:22px;margin-top:45px}}footer{{max-width:1500px;margin:auto;padding:0 40px 42px;color:var(--muted);font-size:13px}}code{{background:#e3e9e4;padding:2px 5px;border-radius:4px}}
@media(max-width:900px){{.hero>div,.heading{{grid-template-columns:1fr}}.cards{{grid-template-columns:repeat(2,1fr)}}.charts{{grid-template-columns:1fr}}}}@media(max-width:620px){{.top{{align-items:flex-start;flex-direction:column}}nav a{{margin:0 12px 0 0}}.hero>div,main{{padding-left:19px;padding-right:19px}}.cards{{gap:8px}}.tools{{align-items:flex-start;flex-direction:column}}.bar{{grid-template-columns:1fr 35px}}.bar>span{{grid-column:1/-1}}}}
</style></head><body><header class="top"><b>Pantaron Research Hub</b><nav><a href="#problems">Problems</a><a href="#policies">Policies</a><a href="#methods">Methods &amp; RRL</a><a href="#sources">Sources</a></nav></header>
<div class="hero"><div><div><span class="kicker">Land &amp; water resources · evidence screening</span><h1>Pantaron Research Hub</h1><p>A traceable workspace for screening reported problems, applicable policy records, and remote-sensing, GIS, and water-resource methods—from Pantaron and Philippine context toward wider methodological literature.</p></div><div class="owner"><b>Joshua De Leon</b>Thesis research workspace<br>University of Southeastern Philippines context<br><small>Generated {date.today().isoformat()}</small></div></div></div>
<main><div class="notice"><b>Screening aid, not thesis findings.</b> Reported problems, legal records, and scholarly metadata carry different evidentiary weight. Verify complete sources before citation or method adoption.</div>
<div class="cards">{card("Reviewed problems",len(reviewed),"source-level review")}{card("Discovery leads",len(leads),"still unverified")}{card("Policy records",len(policies),"statuses kept distinct")}{card("RRL records",len(literature),"unique title + year")}{card("With abstracts",abstracts,"provider supplied")}</div>
<section id="problems" class="block"><div class="heading"><span class="kicker">01 · PROBLEMS</span><h2>Reported land and water resource problems</h2><p>Geographic relationship and limitations stay attached so direct Pantaron reports are not generalized from downstream, nearby, project-specific, or historical evidence.</p></div><div class="charts">{chart(problem_themes(problems),"Problem themes in the reading list")}{chart(values(problems,"relationship to Pantaron"),"Relationship of reports to Pantaron")}</div>{search("problems-table","Find a problem or place")}<div class="wrap"><table id="problems-table"><thead><tr><th>No.</th><th>Problem</th><th>Reported condition</th><th>Relationship</th><th>Scope</th><th>Source</th><th>Research use</th><th>Limitations</th></tr></thead><tbody>{problem_rows(reviewed)}</tbody></table></div><details><summary>Show {len(leads)} unverified RSS discovery leads</summary><div class="wrap"><table><thead><tr><th>No.</th><th>Problem</th><th>Reported condition</th><th>Relationship</th><th>Scope</th><th>Source</th><th>Research use</th><th>Limitations</th></tr></thead><tbody>{problem_rows(leads)}</tbody></table></div></details></section>
<section id="policies" class="block"><div class="heading"><span class="kicker">02 · POLICIES</span><h2>Enacted laws, proposals, and policy instruments</h2><p>Status labels separate enacted Philippine laws from bills or proposals and from international conventions or declarations. Recheck time-sensitive status before thesis submission.</p></div><div class="charts">{chart(policy_counts,"Policy records by legal status","gold")}{chart(values(policies,"jurisdiction"),"Policy records by jurisdiction","gold")}</div>{search("policy-table","Find a law, bill, or instrument")}<div class="wrap"><table id="policy-table"><thead><tr><th>No.</th><th>Law or policy</th><th>Jurisdiction</th><th>Status</th><th>Relevance summary</th><th>Evidence status</th></tr></thead><tbody>{policy_rows}</tbody></table></div></section>
{literature_section}
<details id="sources" class="sources"><summary>CSV files included in this build ({len(files)})</summary><ul>{sources}</ul></details></main><footer>Generated by <code>scripts/report_generator.py</code>. Verify records against publisher, repository, legislative, or agency sources before citing them.</footer>
<script>document.querySelectorAll('.tools input').forEach(input=>{{const table=document.getElementById(input.dataset.table),rows=[...table.tBodies[0].rows],count=document.querySelector(`[data-count="${{input.dataset.table}}"]`);function update(){{const q=input.value.trim().toLowerCase();let shown=0;rows.forEach(row=>{{const yes=!q||row.textContent.toLowerCase().includes(q);row.hidden=!yes;if(yes)shown++}});count.textContent=`${{shown}} of ${{rows.length}} records`}}input.addEventListener('input',update);update()}});</script></body></html>'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default="outputs/data")
    parser.add_argument("--output", default="index.html")
    args = parser.parse_args()
    rows, files = read_rows(Path(args.input_dir))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(make_report(rows, files), encoding="utf-8")
    print(f"Read {len(rows)} records from {len(files)} CSV file(s); wrote {output}")


if __name__ == "__main__":
    main()

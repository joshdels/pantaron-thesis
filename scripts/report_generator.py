#!/usr/bin/env python3
"""Create a data-only HTML literature report from CSV exports in outputs/data."""

from __future__ import annotations

import argparse
import csv
import html
from collections import Counter
from datetime import date
from pathlib import Path


def read_rows(input_dir: Path) -> tuple[list[dict], list[str]]:
    rows: list[dict] = []
    files: list[str] = []
    for path in sorted(input_dir.glob("*.csv")):
        files.append(path.name)
        with path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                row["_file"] = path.name
                rows.append(row)
    return rows, files


def values(rows: list[dict], field: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in rows:
        for value in (row.get(field) or "").split("|"):
            value = value.strip()
            if value:
                counts[value] += 1
    return counts


def bar_chart(counts: Counter[str], title: str, limit: int = 12) -> str:
    items = counts.most_common(limit)
    if not items:
        return f'<section class="chart"><h3>{html.escape(title)}</h3><p class="muted">No values in the supplied CSV files.</p></section>'
    max_value = max(value for _, value in items)
    bars = []
    for label, value in items:
        percentage = max(3, round(100 * value / max_value))
        bars.append(
            '<div class="bar-row">'
            f'<div class="bar-label" title="{html.escape(label, quote=True)}">{html.escape(label)}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{percentage}%"></div></div>'
            f'<div class="bar-value">{value}</div></div>'
        )
    return f'<section class="chart" aria-label="{html.escape(title)}"><h3>{html.escape(title)}</h3><div class="bar-list">{"".join(bars)}</div></section>'


def problem_themes(rows: list[dict]) -> Counter[str]:
    themes = {
        "Forest loss and degradation": ("forest", "deforestation", "logging"),
        "Watershed and river governance": ("watershed", "headwater", "river-basin", "river basin"),
        "Indigenous and ancestral-domain governance": ("indigenous", "ancestral", "lumad", "community"),
        "Mining and extractive pressure": ("mining", "extractive", "tailings", "mercury"),
        "Drought and water shortage": ("drought", "water shortage", "dry", "el niño"),
        "Erosion, flooding and sedimentation": ("erosion", "flood", "siltation", "sediment"),
        "Land conversion and agriculture": ("land conversion", "agriculture", "cultivation", "plantation"),
        "Protected-area and institutional gaps": ("protected-area", "protected area", "conservation status"),
        "Water quality and pollution": ("water quality", "pollution", "contamination"),
    }
    counts: Counter[str] = Counter()
    for row in rows:
        text = " ".join((row.get("problem category", ""), row.get("reported condition", ""), row.get("summary", ""))).lower()
        for theme, words in themes.items():
            if any(word in text for word in words):
                counts[theme] += 1
    return counts


def card(label: str, value: str) -> str:
    return f'<div class="card"><div class="card-label">{html.escape(label)}</div><div class="card-value">{html.escape(value)}</div></div>'


def source_link(row: dict, label_field: str) -> str:
    label = html.escape((row.get(label_field) or "Untitled").strip())
    url = (row.get("source url") or "").strip()
    return (
        f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener">{label}</a>'
        if url
        else label
    )


def make_report(rows: list[dict], files: list[str]) -> str:
    literature_rows = [
        row
        for row in rows
        if "year publication" in row and (row.get("title") or "").strip()
    ]
    problem_rows = [
        row for row in rows if row.get("_file") == "pantaron-land-water-problems.csv"
    ]
    policy_rows = [
        row for row in rows if row.get("record type") == "policy/legal record"
    ]
    method_counts = values(literature_rows, "possible methods used")
    tier_counts = values(literature_rows, "search tier")
    year_counts = Counter(
        (row.get("year publication") or "Unknown").strip() or "Unknown"
        for row in literature_rows
    )
    reviewed_problem_rows = [row for row in problem_rows if row.get("source type") == "reviewed source"]
    discovery_problem_rows = [row for row in problem_rows if row.get("source type") != "reviewed source"]
    problem_counts = problem_themes(problem_rows)
    policy_status_counts = values(policy_rows, "legal status")
    abstract_count = sum(
        bool((row.get("abstract") or "").strip()) for row in literature_rows
    )
    strongest = method_counts.most_common(1)[0] if method_counts else None
    if strongest:
        conclusion = (
            f"Within the supplied metadata, <strong>{html.escape(strongest[0])}</strong> is the most frequently "
            f"listed possible method ({strongest[1]} record(s)). This is a keyword pattern in the exported titles/abstracts, "
            "not a verified comparison of method performance or suitability for the Pantaron Range."
        )
    else:
        conclusion = "No possible-method values were present in the supplied CSV files, so no method pattern can be reported."
    source_list = (
        "".join(f"<li>{html.escape(name)}</li>" for name in files)
        or "<li>No CSV files found</li>"
    )
    literature_html = []
    for number, row in enumerate(literature_rows[:100], start=1):
        literature_html.append(
            "<tr>"
            f"<td>{number}</td>"
            f"<td>{html.escape(row.get('year publication',''))}</td>"
            f"<td>{html.escape(row.get('country',''))}</td>"
            f"<td>{source_link(row, 'title')}</td>"
            f"<td class=\"abstract\">{html.escape(row.get('abstract',''))}</td>"
            f"<td>{html.escape(row.get('possible methods used',''))}</td>"
            "</tr>"
        )
    literature_table = (
        "".join(literature_html)
        or '<tr><td colspan="6">No literature records found.</td></tr>'
    )
    def problem_table_rows(selected_rows: list[dict]) -> str:
        rendered = []
        for number, row in enumerate(selected_rows, start=1):
            rendered.append(
                "<tr>"
                f"<td>{number}</td><td>{html.escape(row.get('problem category',''))}</td>"
                f"<td>{html.escape(row.get('reported condition',''))}</td>"
                f"<td>{html.escape(row.get('relationship to Pantaron',''))}</td>"
                f"<td>{html.escape(row.get('source date',''))}</td>"
                f"<td>{source_link(row, 'source')}</td>"
                f"<td>{html.escape(row.get('limitations',''))}</td>"
                "</tr>"
            )
        return "".join(rendered)
    problem_table = problem_table_rows(reviewed_problem_rows) or '<tr><td colspan="7">No reviewed problem records found.</td></tr>'
    discovery_problem_table = problem_table_rows(discovery_problem_rows) or '<tr><td colspan="7">No RSS discovery leads found.</td></tr>'
    policy_html = []
    for number, row in enumerate(policy_rows, start=1):
        policy_html.append(
            "<tr>"
            f"<td>{number}</td><td>{source_link(row, 'title')}</td>"
            f"<td>{html.escape(row.get('jurisdiction',''))}</td>"
            f"<td>{html.escape(row.get('legal status',''))}</td>"
            f"<td>{html.escape(row.get('summary',''))}</td>"
            f"<td>{html.escape(row.get('evidence status',''))}</td>"
            "</tr>"
        )
    policy_table = (
        "".join(policy_html) or '<tr><td colspan="6">No policy records found.</td></tr>'
    )
    literature_card = card("Literature records", str(len(literature_rows))) if literature_rows else ""
    literature_section = ""
    if literature_rows:
        literature_section = f"""
<h2>Observed literature metadata patterns</h2><p>{conclusion}</p>
<div class="charts">{bar_chart(method_counts, 'Possible methods listed in metadata')}{bar_chart(tier_counts, 'Records by search tier')}{bar_chart(year_counts, 'Publication years', 15)}</div>
<h2>Literature records</h2><p class="muted">Showing the first {min(100, len(literature_rows))} scholarly metadata records. The CSV files remain the complete data source.</p>
<div class="table-wrap"><table><thead><tr><th>No.</th><th>Year</th><th>Country</th><th>Title</th><th>Abstract</th><th>Possible methods</th></tr></thead><tbody>{literature_table}</tbody></table></div>"""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pantaron Research Evidence Report</title><style>
:root{{--ink:#18222d;--muted:#64748b;--blue:#1769aa;--pale:#eef6fb;--line:#d8e1e8;--bg:#f7fafc}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,-apple-system,Segoe UI,sans-serif}}
main{{max-width:1720px;margin:auto;padding:52px 42px 72px}}h1{{font-size:40px;line-height:1.15;margin:0 0 14px}}h2{{margin:58px 0 14px;font-size:28px;line-height:1.25}}h3{{margin:0}}.subtitle,.muted{{color:var(--muted);font-size:16px;max-width:1050px}}
.notice{{background:#fff7df;border-left:4px solid #d69e2e;padding:18px 22px;margin:28px 0;border-radius:7px;max-width:1250px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:20px;margin:34px 0 44px}}.card,.chart,.panel{{background:white;border:1px solid var(--line);border-radius:10px;padding:24px;box-shadow:0 2px 8px #0000000a}}
.card-label{{color:var(--muted);font-size:13px;text-transform:uppercase;letter-spacing:.06em}}.card-value{{font-size:34px;font-weight:700;color:var(--blue);margin-top:6px}}
.charts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(560px,1fr));gap:24px;margin:22px 0 34px}}.chart h3{{font-size:19px;margin-bottom:22px}}.bar-list{{display:grid;gap:14px}}.bar-row{{display:grid;grid-template-columns:minmax(220px,1.15fr) minmax(180px,2fr) 44px;align-items:center;gap:14px}}.bar-label{{font-size:14px;line-height:1.3;overflow-wrap:anywhere}}.bar-track{{height:14px;background:#e7eff5;border-radius:999px;overflow:hidden}}.bar-fill{{height:100%;min-width:8px;border-radius:999px;background:linear-gradient(90deg,#1769aa,#22a4c8)}}.bar-value{{font-weight:700;color:var(--blue);text-align:right;font-variant-numeric:tabular-nums}}
table{{border-collapse:separate;border-spacing:0;width:100%;min-width:1180px;background:white;font-size:14px;line-height:1.55}}th,td{{padding:16px 18px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}th{{background:var(--pale);position:sticky;top:0;z-index:1;white-space:nowrap;font-size:13px;text-transform:uppercase;letter-spacing:.035em}}tbody tr:hover{{background:#f8fbfd}}td{{min-width:130px}}td.abstract{{min-width:460px;max-width:760px;white-space:normal}}.table-wrap{{overflow:auto;max-height:780px;margin:22px 0 44px;border:1px solid var(--line);border-radius:10px;background:white;box-shadow:0 2px 8px #00000008}}.table-wrap table th:first-child,.table-wrap table td:first-child{{min-width:58px;width:58px;text-align:center}}a{{color:var(--blue);text-decoration:none;font-weight:600}}a:hover{{text-decoration:underline}}
details{{margin:24px 0 50px;border:1px solid var(--line);border-radius:10px;background:white}}summary{{cursor:pointer;padding:18px 22px;font-weight:700;color:var(--blue)}}details[open] summary{{border-bottom:1px solid var(--line)}}details .table-wrap{{margin:0;border:0;border-radius:0;box-shadow:none}}code{{background:#eef2f5;padding:2px 5px;border-radius:4px}}footer{{margin-top:32px;color:var(--muted);font-size:13px}}
@media(max-width:760px){{main{{padding:30px 18px 48px}}h1{{font-size:32px}}h2{{margin-top:44px;font-size:24px}}.charts{{grid-template-columns:1fr}}.bar-row{{grid-template-columns:1fr 48px;gap:7px 12px}}.bar-label{{grid-column:1/-1}}.card-value{{font-size:29px}}}}
</style></head><body><main>
<h1>Pantaron Research Evidence Report</h1><p class="subtitle">Generated {date.today().isoformat()} from CSV files in <code>outputs/data/</code>.</p>
<div class="notice"><strong>Evidence boundary:</strong> Literature metadata, reported problems, and legal records are separate evidence types. Reported conditions are not automatically measured trends or proven causes. Policy relevance does not establish local implementation or enforcement. Verify complete sources before thesis citation.</div>
<div class="cards">{card('Reviewed problems', str(len(reviewed_problem_rows)))}{card('RSS leads', str(len(discovery_problem_rows)))}{card('Law/policy records', str(len(policy_rows)))}{literature_card}{card('Files read', str(len(files)))}</div>
<h2>Reported land and water resource problems</h2><p class="muted">Sanitized records distinguish direct Pantaron reports from linked river-basin, downstream, project, and historical context. Limitations should remain attached to every claim.</p>
<div class="charts">{bar_chart(problem_counts, 'Problem themes across reviewed sources and discovery leads')}</div>
<h3>Reviewed sources</h3><p class="muted">These records received source-level review and are shown first. Their stated limitations still apply.</p>
<div class="table-wrap"><table><thead><tr><th>No.</th><th>Problem</th><th>Reported condition</th><th>Relationship to Pantaron</th><th>Date</th><th>Source</th><th>Limitations</th></tr></thead><tbody>{problem_table}</tbody></table></div>
<details><summary>Show {len(discovery_problem_rows)} unverified RSS discovery leads</summary><div class="table-wrap"><table><thead><tr><th>No.</th><th>Problem</th><th>Reported condition</th><th>Relationship to Pantaron</th><th>Date</th><th>Source</th><th>Limitations</th></tr></thead><tbody>{discovery_problem_table}</tbody></table></div></details>
<h2>Applicable laws and policy initiatives</h2><p class="muted">This includes enacted national laws, a Pantaron-specific bill record, and international instruments. A bill must not be described as enacted law.</p>
<div class="charts">{bar_chart(policy_status_counts, 'Policy records by legal status')}</div>
<div class="table-wrap"><table><thead><tr><th>No.</th><th>Law or policy</th><th>Jurisdiction</th><th>Status</th><th>Relevance summary</th><th>Evidence status</th></tr></thead><tbody>{policy_table}</tbody></table></div>
{literature_section}
<h2>Files included</h2><ul>{source_list}</ul>
<footer>Use this as a screening aid. Verify records against publisher or institutional sources before citing them in the thesis.</footer>
</main></body></html>"""


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

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
    width, row_height = 720, 30
    height = 55 + row_height * len(items)
    bars = [f'<text x="0" y="20" class="chart-title">{html.escape(title)}</text>']
    for index, (label, value) in enumerate(items):
        y = 40 + index * row_height
        bar_width = int(500 * value / max_value) if max_value else 0
        bars.append(f'<text x="0" y="{y + 16}" class="label">{html.escape(label[:58])}</text>')
        bars.append(f'<rect x="205" y="{y + 3}" width="{bar_width}" height="18" rx="4" />')
        bars.append(f'<text x="{215 + bar_width}" y="{y + 17}" class="value">{value}</text>')
    return f'<section class="chart"><svg viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}">{"".join(bars)}</svg></section>'


def card(label: str, value: str) -> str:
    return f'<div class="card"><div class="card-label">{html.escape(label)}</div><div class="card-value">{html.escape(value)}</div></div>'


def make_report(rows: list[dict], files: list[str]) -> str:
    method_counts = values(rows, "possible methods used")
    tier_counts = values(rows, "search tier")
    country_counts = values(rows, "country")
    year_counts = Counter((row.get("year publication") or "Unknown").strip() or "Unknown" for row in rows)
    abstract_count = sum(bool((row.get("abstract") or "").strip()) for row in rows)
    strongest = method_counts.most_common(1)[0] if method_counts else None
    if strongest:
        conclusion = (
            f"Within the supplied metadata, <strong>{html.escape(strongest[0])}</strong> is the most frequently "
            f"listed possible method ({strongest[1]} record(s)). This is a keyword pattern in the exported titles/abstracts, "
            "not a verified comparison of method performance or suitability for the Pantaron Range."
        )
    else:
        conclusion = "No possible-method values were present in the supplied CSV files, so no method pattern can be reported."
    source_list = "".join(f"<li>{html.escape(name)}</li>" for name in files) or "<li>No CSV files found</li>"
    rows_html = []
    for number, row in enumerate(rows[:100], start=1):
        url = (row.get("source url") or "").strip()
        title = html.escape(row.get("title", ""))
        linked_title = f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener">{title}</a>' if url else title
        rows_html.append(
            "<tr>"
            f"<td>{number}</td>"
            f"<td>{html.escape(row.get('year publication',''))}</td>"
            f"<td>{html.escape(row.get('country',''))}</td>"
            f"<td>{linked_title}</td>"
            f"<td class=\"abstract\">{html.escape(row.get('abstract',''))}</td>"
            f"<td>{html.escape(row.get('possible methods used',''))}</td>"
            "</tr>"
        )
    table = "".join(rows_html) or '<tr><td colspan="6">No records found.</td></tr>'
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pantaron Literature Metadata Report</title><style>
:root{{--ink:#18222d;--muted:#64748b;--blue:#1769aa;--pale:#eef6fb;--line:#d8e1e8;--bg:#f7fafc}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,-apple-system,Segoe UI,sans-serif}}
main{{max-width:1500px;margin:auto;padding:42px 30px}}h1{{font-size:38px;margin:0 0 10px}}h2{{margin-top:42px;font-size:27px}}h3{{margin:0}}.subtitle,.muted{{color:var(--muted);font-size:16px}}
.notice{{background:#fff7df;border-left:4px solid #d69e2e;padding:14px 16px;margin:22px 0;border-radius:5px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:16px;margin:28px 0}}.card,.chart,.panel{{background:white;border:1px solid var(--line);border-radius:8px;padding:20px;box-shadow:0 1px 2px #00000008}}
.card-label{{color:var(--muted);font-size:13px;text-transform:uppercase;letter-spacing:.06em}}.card-value{{font-size:34px;font-weight:700;color:var(--blue);margin-top:6px}}
.charts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(520px,1fr));gap:20px}}svg{{width:100%;height:auto;min-height:240px}}.chart-title{{font-weight:700;fill:var(--ink);font-size:16px}}.label,.value{{font-size:14px;fill:var(--ink)}}rect{{fill:var(--blue)}}
table{{border-collapse:collapse;width:100%;background:white;font-size:15px}}th,td{{padding:13px 14px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}th{{background:var(--pale);position:sticky;top:0}}td.abstract{{min-width:420px;max-width:760px;white-space:normal}}.table-wrap{{overflow:auto;max-height:720px}}a{{color:var(--blue);text-decoration:none}}a:hover{{text-decoration:underline}}
code{{background:#eef2f5;padding:2px 5px;border-radius:4px}}footer{{margin-top:32px;color:var(--muted);font-size:13px}}
</style></head><body><main>
<h1>Pantaron Literature Metadata Report</h1><p class="subtitle">Generated {date.today().isoformat()} from CSV files in <code>outputs/data/</code>.</p>
<div class="notice"><strong>Evidence boundary:</strong> This report summarizes only the supplied metadata. It does not verify full text, study quality, geographic applicability, method performance, or Pantaron affiliation. Blank abstracts remain blank.</div>
<div class="cards">{card('Records', str(len(rows)))}{card('Abstracts present', f'{abstract_count} / {len(rows)}')}{card('Files read', str(len(files)))}</div>
<h2>Observed metadata patterns</h2><p>{conclusion}</p>
<div class="charts">{bar_chart(method_counts, 'Possible methods listed in metadata')}{bar_chart(tier_counts, 'Records by search tier')}{bar_chart(year_counts, 'Publication years', 15)}</div>
<h2>Records read</h2><p class="muted">Showing the first {min(100, len(rows))} records in file order. The CSV files remain the complete data source.</p>
<div class="table-wrap"><table><thead><tr><th>No.</th><th>Year</th><th>Country</th><th>Title</th><th>Abstract</th><th>Possible methods</th></tr></thead><tbody>{table}</tbody></table></div>
<h2>Files included</h2><ul>{source_list}</ul>
<footer>Use this as a screening aid. Verify records against publisher or institutional sources before citing them in the thesis.</footer>
</main></body></html>'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default="outputs/data")
    parser.add_argument("--output", default="literature-report.html")
    args = parser.parse_args()
    rows, files = read_rows(Path(args.input_dir))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(make_report(rows, files), encoding="utf-8")
    print(f"Read {len(rows)} records from {len(files)} CSV file(s); wrote {output}")


if __name__ == "__main__":
    main()

"""Write task146/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import deliver as DL  # noqa: E402
import records as R   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    R.F_LEGACY: "Unemployment Insurance Board, Benefit Records System weekly export of initial claims by region, claims "
                "weeks of 29 December 2013 to 20 June 2021",
    R.F_CURRENT: "Unemployment Insurance Board, UI Claims System weekly initial claims by region with first-reported "
                 "counts, claims weeks of 27 June 2021 to 27 September 2026",
    R.F_RELEASE: "Unemployment Insurance Board, weekly claims release of 8 October 2026 (claims week ended 3 October 2026)",
    R.F_PROGRAM: "Unemployment Insurance Board, program statistics by region and month, January 2014 to September 2026",
    R.F_NOTES: "Unemployment Insurance Board, claims statistics technical notes, revised July 2026",
    R.F_REGIONS: "Unemployment Insurance Board, regions, territorial authorities and localities with legacy region codes",
    R.F_HOLIDAYS: "Public holidays observed, 2014 to 2027",
    R.F_PORTAL: "Unemployment Insurance Board, Employer Portal export of layoff and reduced-hours notices, 7 October 2026",
    R.F_REGISTER: "Unemployment Insurance Board, Employer Services' register of notices received by email, July 2025 to "
                  "June 2026",
    R.F_CASES: "Unemployment Insurance Board, Employer Services' case notes on notices, July to October 2026",
    R.F_CUBE: "Unemployment Insurance Board open data, initial and transitional claims by claims week, region, industry "
              "division and claim type, from January 2023",
    R.F_CODES: "Unemployment Insurance Board, industry divisions and groups used in its statistics",
    R.F_CONCORD: "Statistics Office, SIC 2006 to SIC 2023 concordance at division level, version 1.2",
    R.F_LFS: "Statistics Office, labour force survey unemployment by region and quarter, 2014 Q1 to 2026 Q2",
    R.F_ADS: "Statistics Office, experimental online job advertisements index by region and week, 2019 to 2026",
    R.F_LOG: "Rothwell Bank Economics, the desk's log of the files it holds for the preview, 8 October 2026",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".json"):
        with open(path, encoding="utf-8") as fh:
            return len(json.load(fh)["observations"])
    return None


def release_figures(target):
    """The national figures the release of 8 October states: the advance count of the week ended 3 October, the week
    before as revised and as first reported, and the same week a year earlier."""
    import csv
    import datetime as dt
    with open(os.path.join(target, R.F_CURRENT), encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    tot = {}
    for r in rows:
        d = r["claims_week_start"]
        a, b = tot.get(d, (0, 0))
        tot[d] = (a + int(r["initial_claims"]), b + int(r["first_reported_initial_claims"]))
    last = max(tot)
    prev = (dt.date.fromisoformat(last) - dt.timedelta(days=7)).isoformat()
    year = (dt.date.fromisoformat(last) - dt.timedelta(days=364)).isoformat()
    return ["{:,}".format(v) for v in (tot[last][0], tot[prev][0], tot[prev][1], tot[year][0])]


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2026-10-08",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task146",
        "title": "How many initial claims the Unemployment Insurance Board will first report for the claims week ended "
                 "10 October 2026, the first claims week of the fourth quarter",
        "domain": "Survey Research & Official Statistics",
        "client_domain": "Survey Research & Official Statistics",
        "subdomain": "seasonal-adjustment-official-time-series-production (the next value of an official weekly series "
                     "in a week carrying an administrative calendar effect: the quarter-start refiling of the closing "
                     "quarter's monetarily ineligible claimants, sized region by region and month by month of the "
                     "refusal on 50 past quarter turns)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "single figure: the national count for one claims week to the nearest thousand, with a one-page "
                        "preview charting the weekly count from April 2026 and a workbook carrying two tables (workers "
                        "under layoff notices by region and period of first layoff; the change in initial claims by "
                        "industry group, July to September 2025 to 2026)",
        "as_of": "2026-10-08",
        "deliverables": [DL.GOLD_DOC, DL.GOLD_BOOK],
        "distractor_files": list(R.DISTRACTORS),
        "stated_inputs": release_figures(target) + ["6,800"],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task146/generator/build.py (seeded, deterministic) around a "
                               "fictional country's unemployment insurance board, its claims and employer systems, its "
                               "statistics office and a bank's economics desk; no real organisation, person or system "
                               "is depicted.",
                     "date": "2026-10-08", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-16",
        "generator": "task146/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))

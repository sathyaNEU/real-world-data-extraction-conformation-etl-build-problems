"""Write task162/metadata.json from the built pack: the distractors, the portal's keys, the input gates and every
shipped file's source, date and licence."""
import json
import os

import docs as DOC
import records as R

SOURCES = {
    R.F_EXPORT: "Usva bug tracker (old tracker), saved search triage-weekly-export, reports filed 1 October 2025 to "
                "17 December 2026",
    R.F_SHARES: "Usva public data portal, daily release-channel version shares by platform",
    R.F_INSTALLS: "Usva public data portal, daily active installs by platform",
    R.F_DASH: "Usva triage dashboard, weekly new defects by product (old tracker)",
    R.F_PUBLIC: "Usva bug statistics page, monthly reports filed by platform",
    R.F_STABILITY: "Usva crash reporter, monthly stability by version and platform",
    R.F_NEWEXPORT: "Usva new tracker, REST search export of the parallel run (projects BRW and WEBC), 4 December 2026",
    R.F_GROUPS: "Usva triage team, component register of the Browser intake project (26 October 2026)",
    R.F_ROTA: "Usva triage team, rota for the parallel run and the follow-up week",
    DOC.F_THREAD: "Usva engineering, mail thread on first-quarter headcount (7 and 17 December 2026)",
    DOC.F_RUNBOOK: "Usva tracker migration, cutover runbook version 1.5 (7 December 2026)",
    DOC.F_AGREEMENT: "Usva triage team, working agreement for the new tracker (28 October 2026)",
    DOC.F_CALENDAR: "Usva release management, release calendar 2025 to 2027 (3 December 2026)",
}
DISTRACTORS = [R.F_PUBLIC, R.F_STABILITY, R.F_DASH]
TITLE = ("How many bug triagers a browser vendor needs for the first quarter of 2027, its first on a new tracker, "
         "when every one of the quarter's releases ships on Patch Tuesday and meets the Windows restart wave in its "
         "own release week")


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        n = sum(max(ws.max_row - 1, 0) for ws in wb.worksheets)
        wb.close()
        return n
    if path.endswith(".json"):
        with open(path, encoding="utf-8") as fh:
            return len(json.load(fh)["issues"])
    return None


def write(task_dir, n=None):
    target = os.path.join(task_dir, "target")
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + SOURCES[f], "date": "2026-12-18",
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task162",
        "title": TITLE,
        "domain": "Product Analytics",
        "client_domain": "Product Analytics",
        "house_domain": "product-analytics",
        "subdomain": "feature-adoption-diffusion-modeling (a desktop browser's releases reaching its installs: each "
                     "install takes an update at its next restart and most Windows installs restart in the two days "
                     "after Patch Tuesday, so a release's first-week reach and the first-use reports that follow are "
                     "set by where it sits in the monthly restart cycle)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a committed headcount (triagers, rounded up from the busiest week's forecast at 120 items per "
                        "triager-week) with the busiest week's forecast to the nearest 100, a table of the parallel "
                        "run's four weeks (triage items with no triage action within 24 hours of filing, triage items "
                        "closed by the run's end), a table of the eight component groups (triage items that arrived in "
                        "each group's components), and a chart of the weekly figures",
        "as_of": "2026-12-18",
        "deliverables": ["triage_staffing_q1_2027.xlsx", "parallel_run_triage.svg"],
        "distractor_files": DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task162/generator/build.py (seeded, deterministic) around "
                               "a fictional Tampere browser vendor, in the layouts of a Bugzilla-style CSV bug export, "
                               "a Jira-style REST search export with changelogs, a public data portal's daily series, "
                               "office workbooks and documents, a release calendar PDF and a mail thread; no real "
                               "organisation's records or person is depicted.",
                     "date": "2026-12-18", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-18",
        "generator": "task162/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta

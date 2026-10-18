"""Write task163/metadata.json from the built pack: the distractors, the portal's keys, the input gates and every
shipped file's source, date and licence."""
import json
import os

import docs as DOC
import records as R

SOURCES = {
    R.F_BFS: "constructed in the layout of a U.S. Census Bureau Business Formation Statistics API response "
             "(timeseries/eits/bfs), twelve states, October 2026 release; values simulated for this task's fictional "
             "world, not Census data",
    R.F_BFS_APR: "constructed in the layout of the Business Formation Statistics monthly download (bfs_monthly.csv), "
                 "April 2026 release; values simulated for this task, not Census data",
    R.F_NES: "constructed in the layout of a Census Bureau Nonemployer Statistics API extract, 2023, twelve states; "
             "values simulated for this task, not Census data",
    R.F_ACCOUNTS: "Kilbourne Payroll (fictional), current account system, onboarding export of the year-end planning "
                  "extract (9 January 2026)",
    R.F_WAGES: "Kilbourne Payroll, current account system, quarterly wages by account, 17 June 2024 to 31 December 2025",
    R.F_REG: "Kilbourne Payroll, current account system, state tax registrations (9 January 2026)",
    R.F_XWALK: "Kilbourne Payroll, migration load crosswalk, legacy client numbers to accounts (15 June 2024)",
    R.F_LEGACY: "Kilbourne Payroll, legacy client system quarterly wage report by pay group, to 14 June 2024",
    R.F_SUTA: "Kilbourne Payroll Payroll Tax, successor transfer register, 2022 to 2025",
    R.F_TERR: "Kilbourne Payroll Sales Operations, 2025 territory map",
    DOC.F_NOTES: "Kilbourne Payroll Sales Operations, first-time employer counting notes (3 February 2026)",
    DOC.F_STANDARD: "Kilbourne Payroll FP&A, 2027 plan sizing standard (1 September 2026)",
    DOC.F_PLAN: "Kilbourne Payroll FP&A, 2027 plan workbook with the 2025 share tab (15 October 2026)",
    DOC.F_LOG: "Kilbourne Payroll Market Research, log of state business filing changes (2023 to 2026); the filing "
               "changes are fictional",
    DOC.F_DICT: "Kilbourne Payroll FP&A, planning pack field guide (15 October 2026)",
    DOC.F_MANIFEST: "Kilbourne Payroll FP&A, planning pack manifest (15 October 2026)",
}
DISTRACTORS = [R.F_BFS_APR, R.F_NES]
TITLE = ("How many first-time employers a Columbus payroll company's 2027 plan should count on across twelve states, "
         "when three states' online formation filings started filing the IRS employer number application for "
         "businesses that tick the box")


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".json"):
        with open(path, encoding="utf-8") as fh:
            return len(json.load(fh)) - 1
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        n = sum(max(ws.max_row - 1, 0) for ws in wb.worksheets)
        wb.close()
        return n
    return None


def write(task_dir, n=None):
    target = os.path.join(task_dir, "target")
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + SOURCES[f], "date": "2026-10-15",
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task163",
        "title": TITLE,
        "domain": "Economics & Econometrics",
        "client_domain": "Economics & Econometrics",
        "house_domain": "economics-econometrics",
        "subdomain": "forecasting-forecast-evaluation (employer business formation forecast from business applications "
                     "when a filing reform changed who applies: the added applications' formation yield identified "
                     "against the states the reform did not reach, before and after)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a committed plan figure to the nearest 100, a table by sales territory of the 2024 first-time "
                        "employers (signed, still with us in the fourth quarter of 2025, gross wages in their first "
                        "quarter on payroll to the cent), a table of the 2024 first-time employers by signup channel, "
                        "and a one-page note with a chart of each territory's signed against still with us",
        "as_of": "2026-10-16",
        "deliverables": ["first_time_employer_plan_2027.xlsx", "first_time_employer_plan_2027_note.docx"],
        "distractor_files": DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task163/generator/build.py (seeded, deterministic) around "
                               "a fictional payroll services company in Columbus, Ohio, in the layouts of the Census "
                               "Bureau's Business Formation Statistics API and monthly download, the Census "
                               "Nonemployer Statistics API, a payroll platform's onboarding export, quarterly wage "
                               "files, state registrations and migration crosswalk, a legacy client system's "
                               "quarterly wage report and a payroll tax team's successor transfer register; the state "
                               "filing reforms are fictional and no real organisation's records or person is depicted.",
                     "date": "2026-10-15", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-18",
        "generator": "task163/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta

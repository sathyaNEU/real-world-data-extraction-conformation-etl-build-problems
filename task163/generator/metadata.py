"""Write task163/metadata.json from the built pack: the distractors, the portal's keys, the input gates and every
shipped file's source, date and licence."""
import json
import os

import docs as DOC
import records as R

SOURCES = {
    R.F_BFS: "Constructed in the layout of the U.S. Census Bureau's Business Formation Statistics API response "
             "(timeseries/eits/bfs, October 2026 release, twelve states, January 2021 to September 2026). Nothing in "
             "it is a Census value: every series for every state is simulated for the scenario, and the Ohio, "
             "Pennsylvania and Michigan series from 2023 carry the scenario's fictional integrated EIN filings. Only "
             "the layout (field names, series codes, FIPS codes, adjustment flags, the formation series' publication "
             "lag) follows the real release",
    R.F_BFS_APR: "Constructed in the layout of the Business Formation Statistics monthly download (bfs_monthly.csv, "
                 "April 2026 release). Every value is simulated for the scenario, the same constructed series as the "
                 "October pull at an earlier vintage; none is a Census value",
    R.F_NES: "Constructed in the layout of a Census Bureau Nonemployer Statistics API extract (2023, twelve states, "
             "NAICS sectors). Every value is simulated for the scenario; none is a Census value",
    R.F_ACCOUNTS: "Constructed: a simulated onboarding export from the current account system of Kilbourne Payroll, a "
                  "fictional company (the year-end planning extract of 9 January 2026); every client, name and EIN "
                  "in it is invented",
    R.F_WAGES: "Constructed: simulated quarterly wages by account from the fictional Kilbourne Payroll's current "
               "account system, 17 June 2024 to 31 December 2025",
    R.F_REG: "Constructed: simulated state tax registrations from the fictional Kilbourne Payroll's current account "
             "system (9 January 2026)",
    R.F_XWALK: "Constructed: the fictional Kilbourne Payroll's simulated migration load crosswalk, legacy client "
               "numbers to accounts (15 June 2024)",
    R.F_LEGACY: "Constructed: the fictional Kilbourne Payroll's simulated legacy client system quarterly wage report "
                "by pay group, to 14 June 2024",
    R.F_SUTA: "Constructed: the fictional Kilbourne Payroll payroll tax team's simulated successor transfer register, "
              "2022 to 2025; every business in it is invented",
    R.F_TERR: "Constructed: the fictional Kilbourne Payroll Sales Operations' 2025 territory map",
    DOC.F_NOTES: "Constructed: written for the scenario as the fictional Kilbourne Payroll Sales Operations' "
                 "first-time employer counting notes (3 February 2026)",
    DOC.F_STANDARD: "Constructed: written for the scenario as the fictional Kilbourne Payroll FP&A's 2027 plan "
                    "sizing standard (1 September 2026)",
    DOC.F_PLAN: "Constructed: the fictional Kilbourne Payroll FP&A's 2027 plan workbook with the 2025 share tab "
                "(15 October 2026); its formations base is summed from the constructed statistics pull",
    DOC.F_LOG: "Constructed: the fictional Kilbourne Payroll Market Research's log of state business filing changes "
               "(2023 to 2026); every change it logs, in every state, is fictional, including the integrated EIN "
               "filings",
    DOC.F_DICT: "Constructed: the fictional Kilbourne Payroll FP&A's planning pack field guide (15 October 2026)",
    DOC.F_MANIFEST: "Constructed: the fictional Kilbourne Payroll FP&A's planning pack manifest (15 October 2026)",
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
                    "source": SOURCES[f], "date": "2026-10-15",
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
                               "a fictional payroll services company in Columbus, Ohio. The three statistics files "
                               "follow the layouts of the Census Bureau's Business Formation Statistics API and "
                               "monthly download and the Census Nonemployer Statistics API, but every value in them "
                               "is simulated for the scenario and none is Census data; the integrated EIN filings in "
                               "Ohio, Pennsylvania and Michigan, and the early 2026 rise in applications, are "
                               "fictional. The company files follow the layouts of a payroll platform's onboarding "
                               "export, quarterly wage files, state registrations and migration crosswalk, a legacy "
                               "client system's quarterly wage report and a payroll tax team's successor transfer "
                               "register. No real organisation's records or person is depicted.",
                     "date": "2026-10-15", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-18",
        "generator": "task163/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta

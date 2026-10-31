"""Write task165/metadata.json from the built pack: the distractors, the input gates and every shipped file's source,
date and licence."""
import json
import os

import pack as P

ORG = "City of Quellbrook"
SOURCES = {
    P.F_LEGACY: ORG + " Roads Division, legacy AVL segment-by-shift material summaries, 1 November 2021 to 31 March 2023",
    P.F_PASSES: ORG + " Roads Division, fleet telematics platform segment passes, 1 October 2023 to 23 September 2026 (UTC)",
    P.F_XWALK: ORG + " GIS Services, segment crosswalk for the 21 August 2023 GIS release",
    P.F_REGISTER: ORG + " Roads Operations Centre, winter route register at 14 September 2026",
    P.F_REVLOG: ORG + " Roads Operations Centre, route audit revision log to 14 September 2026",
    P.F_STORM: ORG + " Roads Operations Centre, storm log and Winter Severity Index, winters 2021-22 to 2025-26",
    P.F_FLEET: ORG + " Fleet Services, winter fleet units at 24 September 2026",
    P.F_WORKORDERS: ORG + " Fleet Services, work orders on the winter fleet units, 1 July 2023 to 23 September 2026",
    P.F_QRT: "Quellbrook Regional Transit Service Planning, frequent network streets for the 30 August 2026 network",
    P.F_PELLARD: "Kettlewood Road Services, monthly material returns under contract RW-2023-07, winters 2023-24 to 2025-26",
    P.F_DOMES: ORG + " Facilities Services, salt dome register at 2 September 2026",
    P.F_SCALE: ORG + " Roads Division, yard scale house logs, 24 August to 24 September 2026",
    P.F_DISPATCH1: "Northgrit Salt Supply, October 2026 dispatch schedule for the City of Quellbrook, issued 14 September 2026",
    P.F_DISPATCH2: "Northgrit Salt Supply, October 2026 dispatch schedule for the City of Quellbrook, issued 21 September 2026",
    P.F_SURVEY: "Tessaline Geomatics, salt dome stock survey report TG-2026-0917 for the City of Quellbrook (16 September 2026)",
    P.F_PLAN: ORG + " Roads Division, winter maintenance plan 2026-27 (18 September 2026)",
    P.F_PROC: ORG + " Roads Division, road salt procurement procedure RO-PR-07, revision 3 (12 May 2025)",
    P.F_TIMESHEETS: ORG + " Payroll, yard winter timesheets, winter 2025-26",
    P.F_BRINE: ORG + " Roads Division, yard brine plant production log, 1 October 2023 to 23 September 2026",
}
DISTRACTORS = [P.F_TIMESHEETS, P.F_BRINE]
TITLE = "Seasonal rock salt commitment, winter 2026-27"


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
    if path.endswith(".parquet"):
        import pyarrow.parquet as pq
        return pq.ParquetFile(path).metadata.num_rows
    return None


def write(task_dir):
    target = os.path.join(task_dir, "target")
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + SOURCES[f], "date": "2026-09-25",
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task165",
        "title": TITLE,
        "domain": "Urban & Regional Science",
        "client_domain": "Urban & Regional Science",
        "house_domain": "urban-regional-science",
        "subdomain": "municipal service demand and resource allocation (winter road salt)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a committed seasonal tonnage, each works yard's dome stock and room before the season, each "
                        "yard's arterial rock salt by winter, and a one-page council report with a chart",
        "as_of": "2026-09-25",
        "deliverables": ["salt_commitment_2026-27.xlsx", "seasonal_salt_commitment_council_report.docx"],
        "distractor_files": DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {
            "files": len(out),
            "formats": sorted({x["format"] for x in out}),
            "largest_file": big["path"],
            "largest_file_rows": big["rows"],
        },
        "sources": [{
            "files": "all files under target/",
            "origin": "constructed for this task by task165/generator/build.py (seeded, deterministic) around a "
                      "fictional Ontario city's roads division, in the layouts of a legacy AVL's segment-by-shift "
                      "summaries and a fleet telematics platform's segment-pass export, a route register and its "
                      "revision log, a storm log, scale house logs, a supplier's dispatch schedules, a "
                      "contractor's returns, a fleet list and its work orders, a drone survey report and the "
                      "division's plan and procedure; no real "
                      "organisation's records or person is depicted.",
            "date": "2026-09-25",
            "license": "CC0-1.0 (original work)",
        }],
        "created": "2026-10-18",
        "generator": "task165/generator/build.py",
        "files": out,
    }
    json.dump(meta, open(os.path.join(task_dir, "metadata.json"), "w"), indent=2)
    return meta

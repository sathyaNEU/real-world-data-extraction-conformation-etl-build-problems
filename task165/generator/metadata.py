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
    P.F_QRT: "Quellbrook Regional Transit Service Planning, frequent network streets for the 30 August 2026 network",
    P.F_LOADING: ORG + " Roads Division, yard loader scale log, 1 November 2023 to 31 March 2026",
    P.F_PELLARD: "Kettlewood Road Services, monthly material returns under contract RW-2023-07, winters 2023-24 to 2025-26",
    P.F_DOMES: ORG + " Facilities Services, salt dome register at 2 September 2026",
    P.F_SCALE: ORG + " Roads Division, yard scale house logs, 24 August to 24 September 2026",
    P.F_DISPATCH1: "Northgrit Salt Supply, October 2026 dispatch schedule for the City of Quellbrook, issued 14 September 2026",
    P.F_DISPATCH2: "Northgrit Salt Supply, October 2026 dispatch schedule for the City of Quellbrook, issued 21 September 2026",
    P.F_SURVEY: "Tessaline Geomatics, salt dome stock survey report TG-2026-0917 for the City of Quellbrook (16 September 2026)",
    P.F_PLAN: ORG + " Roads Division, winter maintenance plan 2026-27 (18 September 2026)",
    P.F_PROC: ORG + " Roads Division, road salt procurement procedure RO-PR-07, revision 3 (12 May 2025)",
    P.F_DICT: ORG + " Roads Division fleet telematics, data dictionary for the 25 September 2026 pull",
    P.F_MANIFEST: ORG + " Roads Division fleet telematics, export manifest for the 25 September 2026 pull",
    P.F_TIMESHEETS: ORG + " Payroll, yard winter timesheets, winter 2025-26",
    P.F_BRINE: ORG + " Roads Division, yard brine plant production log, 1 October 2023 to 23 September 2026",
}
DISTRACTORS = [P.F_TIMESHEETS, P.F_BRINE]
TITLE = ("How much rock salt a lakeshore city's roads division commits above its rolled-over supply contract for the "
         "first winter after a bus network redesign moved 424 lane-km of collectors to bare-pavement service, when the "
         "collectors it moved before were streets its hazard-spot salting already covered along much of their length")


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
        "subdomain": "municipal service demand and resource allocation (a city's winter road salt for a change of "
                     "service level, forecast from the spreader records of the streets that went through the same "
                     "change before, conditioned on how much of each street the old service already salted)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a committed seasonal tonnage to the nearest 100 t, each works yard's dome stock and room on 1 "
                        "November 2026, each yard's Priority 1 arterial rock salt in each of three winters, and a "
                        "one-page memo charting the arterial figures",
        "as_of": "2026-09-25",
        "deliverables": ["salt_commitment_2026-27.xlsx", "seasonal_salt_commitment_memo.docx"],
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
                      "revision log, a storm log, scale house and loader logs, a supplier's dispatch schedules, a "
                      "contractor's returns, a drone survey report and the division's plan and procedure; no real "
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

"""Write task159/metadata.json from the built pack: the distractors, the input gates and every shipped file's source,
date and licence."""
import json
import os

import docs as DOC
import pack as PK

SOURCES = {
    PK.F_FARE: "Vellmouth Transit Commission fare back office, hourly entries by complex and payment type, 3 June 2024 to 10 January 2027 (UTC)",
    PK.F_LEGACY: "Vellmouth Transit Commission legacy fare system, four-hour register reads by station, 1 February 2022 to 30 June 2024",
    PK.F_DASH: "Vellmouth Transit Commission Ridership Data, ridership dashboard, average weekday entries by complex, 2025 and 2026 (8 January 2027)",
    PK.F_COMPLEX: "Vellmouth Transit Commission fare back office, complex table (11 January 2027)",
    PK.F_CENSUS: "Vellmouth Transit Commission count programme, station census, October 2026 (30 November 2026)",
    PK.F_COUNTS: "Vellmouth Transit Commission count programme, platform counts, autumn 2026 (4 December 2026)",
    PK.F_CAP: "Vellmouth Transit Commission Station Planning, platform capacity register (11 January 2027)",
    PK.F_TT: "Vellmouth Transit Commission Service Planning, weekday timetables for the autumn 2026 and spring 2027 picks",
    PK.F_FLEET: "Vellmouth Transit Commission Car Equipment, fleet register (11 January 2027)",
    PK.F_CHANGES: "Vellmouth Transit Commission Service Planning, service change register, 2024 to 2027",
    PK.F_INV: "Vellmouth Transit Commission Station Engineering, station elements inventory (11 January 2027)",
    PK.F_ASSET: "Vellmouth Transit Commission Elevator and Escalator Maintenance, escalator asset register (11 January 2027)",
    PK.F_CTRL: "Vellmouth Transit Commission Elevator and Escalator Maintenance, escalator controller log, September to December 2026",
    PK.F_WO: "Vellmouth Transit Commission Elevator and Escalator Maintenance, elevator work orders, September to December 2026",
    PK.F_MON: "Vellmouth Transit Commission Elevator and Escalator Maintenance, elevator remote monitoring, September to December 2026",
    PK.F_DICT: "Vellmouth Transit Commission Ridership Data, data dictionary for the 11 January 2027 pull",
    DOC.F_STANDARD: "Vellmouth Transit Commission Rail Operations, platform crowding standard, revision 4 (24 August 2026)",
    DOC.F_PLAN_AUT: "Vellmouth Transit Commission Service Planning, service plan for the autumn 2026 pick (20 July 2026)",
    DOC.F_PLAN_SPR: "Vellmouth Transit Commission Service Planning, service plan for the spring 2027 pick (14 December 2026)",
    DOC.F_MANUAL: "Vellmouth Transit Commission Station Planning, station planning manual chapter 5 (3 November 2025)",
}
DISTRACTORS = [PK.F_LEGACY, PK.F_DASH]
TITLE = ("How many weekday-morning platform conductor shifts a week a city transit commission's spring 2027 roster pick "
         "funds under its platform crowding standard, when the busiest platforms' mid-week crowds are riders left "
         "behind by trains arriving full")


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
                    "source": "Constructed: " + SOURCES[f], "date": "2027-01-11",
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task159",
        "title": TITLE,
        "domain": "Urban & Regional Science",
        "client_domain": "Urban & Regional Science",
        "house_domain": "urban-regional-science",
        "subdomain": "forecasting (a city subway's platform crowds forecast by weekday for a roster pick: the busiest "
                     "platforms' counted crowds read as a backlog behind trains that arrive carrying their branch, "
                     "built train by train from the station census and the timetable)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a committed count of weekday-morning conductor shifts a week with the count on each weekday and "
                        "the posting schedule, each watch-list complex's platform escalator capacity down to and up from "
                        "its platforms in the morning peak, each complex's elevator-hours out of service in the autumn mornings, "
                        "and a chart of the escalator figures",
        "as_of": "2027-01-11",
        "deliverables": ["spring_2027_platform_conductors.xlsx", "platform_escalators_am_peak.png"],
        "distractor_files": DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task159/generator/build.py (seeded, deterministic) around "
                               "a fictional United States city's transit commission and its six-line subway, in the "
                               "layouts of a fare back office's hourly ridership export and its legacy register reads, "
                               "a station census and platform counts, a capacity register, a scheduling system's "
                               "timetables, an engineering inventory, escalator controller logs, elevator work orders "
                               "and remote monitoring; no real organisation's records or person is depicted.",
                     "date": "2027-01-11", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-17",
        "generator": "task159/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta

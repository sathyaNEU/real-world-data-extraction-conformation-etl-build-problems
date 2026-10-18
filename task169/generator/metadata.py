"""Write task169/metadata.json from the built pack: the distractors, the input gates and every shipped file's source,
date and licence."""
import json
import os

import pack as P

ORG = "Calvermouth City Council"
F = P.F
SOURCES = {
    F["legacy"]: ORG + " Traffic Monitoring Unit, legacy logging platform archive, hourly cycle counts, 1 June to 31 August 2024",
    F["platform"]: ORG + " Traffic Monitoring Unit, counter platform hourly export, summers 2025 and 2026 (UTC)",
    F["register"]: ORG + " Traffic Monitoring Unit, cycle counter register at 2 October 2026",
    F["inventory"]: ORG + " Highways Design, Cycleway Path Inventory, segment register updated 28 April 2026",
    F["guide"]: ORG + " Highways Design, Cycle Design Guide (2023 edition, 2025 reprint), Section 4",
    F["policy"]: ORG + " Active Travel Team, Cycleway Widening Allocation Policy AT-POL-07 v1.0 (17 March 2026)",
    F["notes"]: ORG + " Traffic Monitoring Unit, cycle counter data notes for users, issue 4 (2 October 2026)",
    F["weather"]: ORG + " weather station CVM-WX1 (Civic Centre roof), daily record 1 January 2024 to 30 September 2026",
    F["terms"]: ORG + " Education Services, published school term dates 2023-24 to 2026-27 with bank holidays",
    F["log"]: ORG + " job system, counter asset maintenance jobs, January 2024 to October 2026",
    F["week"]: ORG + " Traffic Monitoring Unit, counter platform interval export for the six dashboard counters, 11 to 15 May 2026",
    F["volunteers"]: "Calvermouth Cycle Forum, May 2026 volunteer count sheets at the six dashboard counter sites",
    F["manifest"]: ORG + " Traffic Monitoring Unit, export manifest for the 9 October 2026 data request",
    F["dashboard"]: ORG + " Traffic Monitoring Unit, active travel dashboard monthly series, January 2019 to September 2026",
    F["events"]: ORG + " Events and Culture, city events programme 2024 to 2026",
    F["app"]: ORG + " Active Travel Team, activity app partner data, monthly rides by cycleway, January 2024 to September 2026",
}
TITLE = ("Which of an English city's six cycleways gets the one widening it can build before summer 2027, forecast as the "
         "cycleway crowded on the most days next summer, when its narrowest segments crowd at different hours and the "
         "trips that fill those hours grow at different rates under very different summers' weather")


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            n = sum(1 for line in fh if line.strip())
        if os.path.basename(path) in (F["legacy"], F["dashboard"]):
            return n - 2
        return n - 1
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
                    "source": "Constructed: " + SOURCES[f], "date": "2026-10-09",
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task169",
        "title": TITLE,
        "domain": "Urban & Regional Science",
        "client_domain": "Urban & Regional Science",
        "house_domain": "urban-regional-science",
        "subdomain": "forecasting (cycle demand at a segment's binding hour, by trip purpose growth with weather held "
                     "fixed, for a capacity allocation)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "the cycleway to widen with the segment and hours that crowd it, each volunteer count site's "
                        "counter riders and shortfall over the intervals both counted, each dashboard counter's 2025 "
                        "hours recording nothing and its separate stoppages, and a one-page committee note",
        "as_of": "2026-10-12",
        "deliverables": ["cycleway_widening_2027.xlsx", "widening_note_2027.pdf"],
        "distractor_files": list(P.DISTRACTORS),
        "field_terms": ["level of service", "two-way capacity", "trip purpose", "binding hour", "weather elasticity"],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}), "largest_file": big["path"],
                        "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task169/generator/build.py (seeded, deterministic) around a "
                               "fictional English city council's cycle counters, in the layouts of a legacy logger "
                               "archive, a counter platform's hourly and interval exports, a counter register, a path "
                               "inventory, a design guide section, an allocation policy, a weather station record, a "
                               "job system export and a cycle forum's count sheets; no real city's data",
                     "date": "2026-10-09", "license": "CC0-1.0 (original work, constructed for this task)"}],
        "created": "2026-10-18",
        "generator": "task169/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return meta

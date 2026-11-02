"""metadata.json beside target/: what the task is about, the deliverables, the distractors and every file's provenance.
It names the decision and the files, never the method or what the data hold."""
import json
import os

import pandas as pd
import pyarrow.parquet as pq

import pack as K

SOURCE = {
    "old": "Constructed: the old WMS's pick confirmation export, 1 January to 12 June 2026",
    "new": "Constructed: the new WMS's pick task export, 15 June to 31 December 2026",
    "exc": "Constructed: the pack-out verification stations' finding log for 2026",
    "items": "Constructed: the WMS item master as exported on 4 January 2027",
    "plan": "Constructed: the client's logistics volume plan for the first quarter of 2027",
    "deliv": "Constructed: the dispatch system's retail delivery notes for 2026",
    "colli": "Constructed: the dispatch module's container contents for retail deliveries, January to June 2026",
    "claims": "Constructed: the client's store claims register as exported on 4 January 2027",
    "lms": "Constructed: the labour management system's shift bookings for 2026",
    "users": "Constructed: the old WMS's user list with labour badges",
    "counts": "Constructed: the site's 2026 cycle counts of pick faces",
    "bms": "Constructed: the building management system's daily zone temperatures for 2026",
    "sla": "Constructed: Schedule 3 (Service Levels) of the logistics services agreement, version 2.0",
    "pcn": "Constructed: the client's packaging change notification PCN-2026-11",
    "closeout": "Constructed: the site's service close-out for December 2026",
}


def rows(path):
    if path.endswith(".csv"):
        sep = ";" if open(path, encoding="utf-8").readline().count(";") > 1 else ","
        return int(len(pd.read_csv(path, sep=sep, dtype=str)))
    if path.endswith(".parquet"):
        return int(pq.read_metadata(path).num_rows)
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        return int(sum(ws.max_row for ws in wb.worksheets))
    return None


def write(path, target):
    files = []
    for key, name in sorted(K.FILES.items(), key=lambda kv: kv[1]):
        p = os.path.join(target, name)
        files.append(dict(path=name, format=name.rsplit(".", 1)[1], bytes=os.path.getsize(p), rows=rows(p),
                          source=SOURCE[key], date="2027-01-04", license="CC0-1.0 (original work, constructed for this task)"))
    fmts = sorted({f["format"] for f in files})
    meta = {
        "task": "task277",
        "architecture": 1,
        "title": ("Whether Kroonvaart Fulfilment's Venlo site holds its client Siersma Care's 99.80 per cent pick accuracy target "
                  "in February and March 2027, with the expected failing order lines each month, and the accepted 2026 store "
                  "claims in units by customer and quarter of delivery"),
        "domain": "Business & Operations Analytics (client domain Human Factors & Ergonomics)",
        "subdomain": "service-operations-sla (client task type human-reliability-assessment)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "02: a forecast across periods (February and March 2027), with each month's failing lines, accuracy and "
                        "verdict against target, a store claims table by customer and quarter, and a chart",
        "as_of": "2027-01-04",
        "deliverables": ["venlo_accuracy_forecast_feb_mar_2027.xlsx", "siersma_pick_accuracy_q1_2027.png"],
        "distractor_files": [K.FILES["counts"], K.FILES["bms"]],
        "stated_inputs": ["February 2027", "March 2027", "99.80", "2026"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_rows": max(f["rows"] or 0 for f in files)},
        "sources": [{"files": "all files under target/",
                     "origin": ("constructed for this task by task277/generator/build.py (seeded, deterministic) in the layouts "
                                "of a warehouse management system's exports, a pack-out verification log, an item master, a "
                                "client volume plan, dispatch exports, a customer service claims register, a labour system "
                                "export and the agreement's service level schedule; the companies, customers, stores, people, "
                                "articles and codes are fictional."),
                     "date": "2027-01-04", "license": "CC0-1.0 (original work)"}],
        "created": "2027-01-04",
        "generator": "task277/generator/build.py",
        "files": files,
    }
    json.dump(meta, open(path, "w"), indent=1)
    open(path, "a").write("\n")

"""Write task164/metadata.json from the built pack: the distractors, the input gates and every shipped file's source,
date and licence."""
import json
import os

import docs as DOC
import pack as PK

SOURCES = {
    PK.F_TLM[2024]: ("Calloway Valley Power Distribution Planning, transformer load management summer peaks, 2024 season run (TLM 4.2 layout)", "2024-10-07"),
    PK.F_TLM[2025]: ("Calloway Valley Power Distribution Planning, transformer load management summer peaks, 2025 season run", "2025-10-06"),
    PK.F_TLM[2026]: ("Calloway Valley Power Distribution Planning, transformer load management summer peaks, 2026 season run", "2026-10-19"),
    PK.F_GIS: ("Calloway Valley Power GIS Records, single-phase residential service transformer locations at the pull", "2027-04-05"),
    PK.F_CHG: ("Calloway Valley Power GIS Records, unit changes posted 1 January 2024 to the pull", "2027-04-05"),
    PK.F_SP: ("Calloway Valley Power Customer Systems, residential service points and their transformers at the pull", "2027-04-05"),
    PK.F_RATE: ("Calloway Valley Power Customer Systems, rate schedule changes to R-EV2", "2027-04-05"),
    PK.F_DMV: ("Calloway Valley Power Customer Systems, DMV plug-in vehicle notification feed with the address match", "2027-04-05"),
    PK.F_LSI: ("Calloway Valley Power Load Research, 2026 EV charging load study, EVSE submeter intervals", "2026-11-16"),
    PK.F_LSP: ("Calloway Valley Power Load Research, 2026 EV charging load study participants", "2026-11-16"),
    PK.F_WX: ("Calloway Valley Power district weather stations, daily maximum temperature, summers 2024 to 2026", "2027-04-05"),
    PK.F_OMS: ("Calloway Valley Power Reliability, outage management system transformer outage lines, 16 May to 15 October 2026", "2026-10-16"),
    PK.F_WO: ("Calloway Valley Power Construction Services, 2025-26 proactive replacement pilot work orders", "2027-04-05"),
    PK.F_COST: ("Calloway Valley Power Finance, internal order 7100-PTR25 line items", "2027-04-05"),
    PK.F_DIST: ("Calloway Valley Power Distribution Planning, district codes, service centers and weather stations", "2027-04-05"),
    PK.F_IEPR: ("Calloway Valley Power Forecasting & Analytics, 2026 IEPR plug-in vehicle forecast by district", "2026-08-22"),
    PK.F_FDR: ("Calloway Valley Power Distribution Planning, feeder-head peaks from SCADA, summer 2026", "2026-10-19"),
    PK.F_MAN: ("Calloway Valley Power, export manifest for the 5 April 2027 pull", "2027-04-05"),
    DOC.F_DICT: ("Calloway Valley Power Regulatory Compliance, data dictionary for the 5 April 2027 pull", "2027-04-05"),
    DOC.F_DEC: ("Decision 26-11-019 on Application 26-03-008, excerpt (fictional proceeding)", "2026-11-12"),
    DOC.F_TAR: ("Calloway Valley Power residential rate schedules, excerpt, rates effective 1 March 2026", "2026-03-01"),
}
DISTRACTORS = [PK.F_IEPR, PK.F_FDR]
TITLE = ("How many of 400 proactive service transformer replacements each of a California utility's twelve districts "
         "gets in 2027, in proportion to its forecast transformers at risk of summer overload, when a plug-in vehicle "
         "on the default rate adds most of its charger's draw to a small transformer's recorded peak")


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
        src, date = SOURCES[f]
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + src, "date": date,
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task164",
        "title": TITLE,
        "domain": "Energy Systems & Utilities",
        "client_domain": "Energy Systems & Utilities",
        "subdomain": "load-forecasting (each service transformer's summer 2027 4 to 9 pm peak forecast from its own "
                     "recorded summer peaks and the plug-in vehicles registered at its service points on the record "
                     "date, each vehicle taken at the rise in recorded peak it brings by rate schedule)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "an allocation of 400 replacements over twelve districts with each district's forecast at-risk "
                        "count and Foothill's figure on its own, the 2025-26 pilot's replacements, kVA added and cost per "
                        "replacement in its three districts, each district's summer 2026 failure customer-hours and "
                        "customers out more than eight hours, and a chart of the customer-hours",
        "as_of": "2027-04-05",
        "deliverables": ["ptr_2027_district_allocation.xlsx", "summer_2026_transformer_failures.png"],
        "distractor_files": DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task164/generator/build.py (seeded, deterministic) around a "
                               "fictional California electric utility, in the layouts of a transformer load management "
                               "system's season runs, a GIS register and change log, a customer system's service points "
                               "and rate changes, a DMV plug-in vehicle notification feed, an EV charging load study, an "
                               "outage management system export, a work management system and a general ledger; no real "
                               "organisation's records or person is depicted.",
                     "date": "2027-04-05", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-18",
        "generator": "task164/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta

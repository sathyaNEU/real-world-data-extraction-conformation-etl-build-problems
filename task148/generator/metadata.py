"""Write task148/metadata.json from the built pack."""
import json
import os

import docs as DOC
import records as R

SOURCES = {
    R.F_LEGACY: "Tavish County Emergency Communications Agency, legacy ACD (CAMA and ALI) call detail export",
    R.F_I3: "Tavish County Emergency Communications Agency, NG911 call-handling system i3 call log export",
    R.F_ROSTER: "Tavish County Emergency Communications Agency, scheduling system floor roster",
    R.F_FORECAST: "Tri-County Regional 911 Board, hourly 911 volume forecast workbook, fiscal 2027 and 2028",
    DOC.F_SOP: "Tavish County Emergency Communications Agency, SOP 2.10 call answering and answer-time reporting",
    DOC.F_BUDGET: "Tavish County budget office, FY2028 recommended budget page for the communications floor",
    R.F_CHE: "Tavish County Emergency Communications Agency, call-handling system location records, north-east extract",
    R.F_BOUNDARY: "Tavish County GIS, Halvorsen Township boundary",
    R.F_DIRECTORY: "Tri-County ESInet PSAP directory",
    R.F_CALLBACK: "Tavish County Emergency Communications Agency, callback module task export",
    R.F_CAD: "Tavish County Emergency Communications Agency, CAD incident export",
    R.F_ADMIN: "Tavish County Emergency Communications Agency, administrative line ACD export",
    R.F_MANIFEST: "Tavish County Emergency Communications Agency, QA extract log",
    DOC.F_README: "Tavish County Emergency Communications Agency, README and field notes",
}
DISTRACTORS = [R.F_CAD, R.F_ADMIN]


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".jsonl"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh)
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        return sum(max(ws.max_row - 3, 0) for ws in wb.worksheets if ws.title != "Read me")
    return None


def write(target, out_path, files):
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + SOURCES[f], "date": "2026-10-06",
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task148",
        "title": "In which months of fiscal 2028 a county 911 center's Friday and Saturday late shift falls short of "
                 "answering 90 per cent of calls within 15 seconds with four call-takers, when its callers hang up as "
                 "they wait",
        "domain": "Urban & Regional Science",
        "client_domain": "Urban & Regional Science",
        "subdomain": "municipal-service-demand-resource-allocation (a PSAP's answer-time compliance forecast from its "
                     "ACD history and the regional board's arrival forecast, by a queue with reneging whose patience "
                     "is estimated over censored waits)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a forecast across the twelve months of fiscal 2028 (each month's expected compliance to the "
                        "whole per cent and the months below 90 per cent), a chart of the months against the standard, "
                        "and two tables (Halvorsen Township's wireless calls reaching the agency and transferred to "
                        "Wexley, by fiscal 2026 quarter; the share of abandoned calls dialled back within two minutes, "
                        "January to June 2026)",
        "as_of": "2026-10-06",
        "deliverables": ["late_shift_staffing_fy2028.xlsx", "late_shift_compliance_fy2028.png"],
        "distractor_files": DISTRACTORS,
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task148/generator/build.py (seeded, deterministic) around "
                               "a fictional county 911 agency, its regional board, a neighbouring county and a township, "
                               "in the layouts of a PSAP's ACD and NG911 i3 exports, a scheduling roster, a call-handling "
                               "system's location records, county GIS and a callback module; no real organisation's "
                               "records, person or caller is depicted, and every callback number is a pseudonym.",
                     "date": "2026-10-06", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-16",
        "generator": "task148/generator/build.py",
        "files": out,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta

"""Write task181/metadata.json from the built pack."""
import json
import os
import sys

import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    "fdps": "FDPS archive: one row per flight per elementary sector entered, 1 January 2025 to 30 September 2026",
    "occ": "Safety occurrence database export, Holmvik ACC sectors, occurrences dated 1 January 2025 to 30 September 2026",
    "codes": "Occurrence scheme AAN-OCC-01 code lists",
    "plan": "Network and Capacity Planning: planning traffic for summer 2027, issue 1 of 9 October 2026",
    "register": "Sector register: elementary sectors, traffic volumes, limits",
    "slots": "Network manager slot allocation list for regulations on Holmvik traffic volumes and arrivals, May to September 2026",
    "regs": "Network manager regulation list, May to September 2026",
    "clog": "Supervisors' sector configuration log, 30 April to 30 September 2026 (local time)",
    "ctab": "Sector configuration table as exported from the ops system on 9 October 2026",
    "plan_doc": "Unit Safety Plan 2026 to 2028 (HACC-SAF-PLN-03 edition 2.0)",
    "closeout": "Summer 2026 safety performance close-out (HACC-SAF-RPT-2026-11)",
    "om": "Operations Manual Part 3 Chapter 4, sector configuration (edition of 26 March 2026)",
    "notes": "Data and Analytics hand-off note for the extract",
    "roster": "Controller roster, June to August 2026",
    "met": "Met office convective activity summaries by sector and day, summer 2026",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        return int(pq.ParquetFile(path).metadata.num_rows)
    return None


def write(target, out_path):
    files = []
    for k, f in B.FILES.items():
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[k], "date": "2026-10-12",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    files.sort(key=lambda x: x["path"])
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task181",
        "title": "Whether any en-route sector will run over the summer 2027 tolerance of ATM-related losses of "
                 "separation, with each sector's summer 2026 delay, solo opening hours and ACAS encounters",
        "domain": "Human Factors & Ergonomics",
        "subdomain": "safety incident and error analysis (losses of separation in an area control centre's en-route "
                     "sectors against a unit safety plan's tolerance)",
        "objective": "Anomaly Detection & Diagnostics",
        "prompt_shape": "01 (each candidate in or out against a line): every sector's summer 2027 forecast against "
                        "the tolerance, with every sector's summer 2026 ATFM delay per flight, hours open on its own "
                        "and ACAS RA encounters",
        "as_of": "2026-10-12",
        "deliverables": ["summer2027_safety_forecast.pptx", "summer2026_sector_measures.csv"],
        "stated_inputs": ["40.0", "100,000", "14,957", "13.4", "32.0"],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task181/generator/build.py (seeded, deterministic) around "
                               "a fictional air navigation service provider (Aldmark Air Navigation), its area control "
                               "centre, sectors, airports and operators; external airports are real ICAO locations "
                               "used only as origins and destinations. No real person, operator, flight or occurrence "
                               "is depicted.",
                     "date": "2026-10-12", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-12",
        "generator": "task181/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))

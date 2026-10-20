"""Write task187/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    "scada": "Wind farm SCADA ten-minute export, turbines CH01 to CH10, October 2025 to September 2026",
    "mast": "Met mast M1 logger ten-minute record, October 2025 to September 2026",
    "anm": "Network operator's ANM instruction log for the farm's connection",
    "states": "Turbine controller state code table",
    "lifts": "Crane contractor's lift log for the site, 2026",
    "layout": "Site layout: pads, turbines and the met mast on the site grid",
    "register": "Turbine asset register",
    "counters": "Turbine energy meter readings by month",
    "orders": "Service contractor's work orders, October 2025 to September 2026",
    "standard": "Society O&M standard OM-07, revision 3",
    "schedule": "Turbine supply agreement, Schedule 3, warranted power curve",
    "notes": "Asset manager's extract notes, 9 October 2026",
    "meter": "Connection export meter, half-hourly settlement data",
    "prior": "Lost production report to the board, October 2024 to September 2025",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        import pyarrow.parquet as pq
        return pq.ParquetFile(path).metadata.num_rows
    return None


def write(target, out_path):
    files = []
    for k, f in B.FILES.items():
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[k], "date": "2026-10-09",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    files.sort(key=lambda x: x["path"])
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task187",
        "title": "Which of a community wind farm's ten turbines gets the summer 2027 leading-edge repair campaign, and "
                 "the energy the repaired blades recover over the twelve months after the work, with each turbine's "
                 "each turbine's metered generation and the farm's metered export over the eleven months to 31 August 2026",
        "domain": "Energy Systems & Utilities",
        "subdomain": "grid reliability and outage analysis (a wind farm's production accounting: the performance "
                     "shortfall split into blade loss and inflow, reconciled to the revenue counters and the "
                     "connection meter)",
        "objective": "Anomaly Detection & Diagnostics",
        "prompt_shape": "14 (cuts of a distribution by segment): the campaign's turbine and recovered energy; each "
                        "turbine's metered generation and the farm's metered export by month; the chart of generation by turbine",
        "as_of": "2026-10-09",
        "deliverables": ["le_repair_campaign_2027.pdf", "metered_generation_2025_26.xlsx"],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task187/generator/build.py (seeded, deterministic) around a "
                               "fictional community wind farm, its society, turbine maker, network operator and "
                               "contractors; no real organisation, site, person or record is depicted.",
                     "date": "2026-10-09", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-09",
        "generator": "task187/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))

"""Write ../metadata.json from the built target/."""
import json
import os

import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, "..", "target")
DESC = {
    "dga_main_tank_results": "Laboratory dissolved gas, water and oil temperature results for main-tank oil samples, one row per report issue, March 2021 to September 2026",
    "dga_tap_changer_compartments": "Laboratory dissolved gas results for in-oil tap-changer diverter compartments, annual March samples 2021 to 2026",
    "asset_register_zone_transformers": "Asset management system extract: the 44 zone substation transformers and the 22 substations",
    "scada_tap_counters_daily": "SCADA tap-changer operations counters at 00:00 daily, 1 January 2021 to 16 October 2026",
    "scada_top_oil_hourly": "SCADA historian export of hourly mean top-oil temperature and load per transformer, 2021 to 15 October 2026",
    "maintenance_log": "Closed work orders on zone substation plant, January 2019 to October 2026",
    "ES-DGA-02": "Network standard ES-DGA-02 rev 3, fleet DGA condition standard (governing document)",
    "oil_results_notes": "Zone substation engineering field notes for the extracts",
    "mobile_substation_bookings": "Canterbury mobile substation pool MSU-2 booking sheet, April 2027 to March 2028",
    "protection_relay_events": "Feeder and incomer protection relay operations, January 2025 to October 2026",
    "thermal_imaging_survey": "Contractor infrared survey of the 11 kV switchboards, March 2026",
    "extract_log": "Extract job log for the 16 October 2026 pull",
}
files, fmts = [], set()
for f in sorted(os.listdir(T)):
    p = os.path.join(T, f)
    ext = os.path.splitext(f)[1][1:]
    fmts.add(ext)
    e = {"path": f, "format": ext, "bytes": os.path.getsize(p)}
    if ext == "csv":
        with open(p) as fh:
            e["rows"] = sum(1 for _ in fh) - 1
    if ext == "parquet":
        e["rows"] = pq.ParquetFile(p).metadata.num_rows
    key = next(k for k in DESC if f.startswith(k))
    e.update(source="Constructed: " + DESC[key], date="2026-10-16",
             license="CC0-1.0 (original work, constructed for this task)")
    files.append(e)
big = max((x for x in files if "rows" in x), key=lambda x: x["rows"])
meta = {
    "task": "task180",
    "title": "Choosing the three zone substation transformers for the 2027/28 internal inspection outages from five years of dissolved gas analysis",
    "domain": "Energy Systems & Utilities",
    "subdomain": "asset condition and maintenance (transformer dissolved gas analysis)",
    "objective": "Anomaly Detection & Diagnostics",
    "prompt_shape": "01 ranked list under a cap: three inspection outages from 44 transformers, with a tap-changer table and a wet-transformer table",
    "as_of": "2026-10-16",
    "deliverables": ["inspection_slate_2027-28.docx", "dga_fleet_review.csv"],
    "distractor_files": [x["path"] for x in files if x["path"].startswith(("protection_relay_events", "thermal_imaging_survey"))],
    "input_gates": {"files": len(files), "formats": sorted(fmts), "largest_file": big["path"],
                    "largest_file_rows": big["rows"]},
    "sources": [{"files": "all files under target/",
                 "origin": "constructed for this task by task180/generator/build.py (seeded, deterministic) around a fictional New Zealand lines company (Ellesmere Lines) with real Canterbury place names; transformer, tap-changer and laboratory names are invented; no real asset, customer or measurement is depicted.",
                 "date": "2026-10-11", "license": "CC0-1.0 (original work)"}],
    "created": "2026-10-11",
    "generator": "task180/generator/build.py",
    "files": files,
}
with open(os.path.join(HERE, "..", "metadata.json"), "w") as fh:
    json.dump(meta, fh, indent=2)
    fh.write("\n")
print(meta["input_gates"], meta["distractor_files"])

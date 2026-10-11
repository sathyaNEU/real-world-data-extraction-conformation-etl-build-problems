"""Write ../metadata.json from the built target/."""
import json, os
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, "..", "target")
DESC = {
 "rp_mart_weekly_import": "Analytics mart rp.weekly_import: weekly metered import per metering system, w/c 2023-12-04 to w/c 2026-11-30",
 "smart_daily_reads": "Smart metering daily midnight register reads per supply number, 2024-10-01 to 2026-12-07",
 "supply_point_register": "CIS supply point register extract: supplies, meter exchanges, account history",
 "change_of_occupier": "CIS change of occupier events by UPRN",
 "heating_measures": "Energy efficiency team completions (heat pumps, storage heater replacements, insulation, solar)",
 "station_degree_days": "Daily mean temperature and 15.5 C heating degree days by weather station",
 "patch_weather_stations": "Field patch to weather station map",
 "fieldlink_visits": "Legacy FieldLink revenue protection visit jobs to 17 November 2024",
 "fieldops_visits": "FieldOps revenue protection visit jobs from 4 November 2024",
 "tamper_appeals": "Register of customer appeals against tamper findings",
 "rp_field_rota": "Field team rota for January to March 2027 with absences and the group holiday calendar",
 "RP-07": "Revenue Protection procedure RP-07 v4: referral and placement of the field team",
 "FW-3": "Field working standard FW-3, issue 6",
 "rp_extract_field_notes": "RP analytics field notes for the December extracts",
 "extract_log": "Extract log for the 7 December 2026 pull",
 "prepayment_vends": "Prepayment top-up vends, June to November 2026",
 "dno_feeder_loss": "Network operator feeder loss estimates 2025-26, shared under the data agreement",
}
files = []
fmts = set()
for f in sorted(os.listdir(T)):
    p = os.path.join(T, f); ext = os.path.splitext(f)[1][1:]
    fmts.add(ext)
    e = {"path": f, "format": ext, "bytes": os.path.getsize(p)}
    if ext == "csv":
        e["rows"] = sum(1 for _ in open(p)) - 1
    if ext == "parquet":
        e["rows"] = len(pd.read_parquet(p, columns=["read_type"]))
    key = next(k for k in DESC if f.startswith(k))
    e.update(source="Constructed: " + DESC[key], date="2026-12-07", license="CC0-1.0 (original work, constructed for this task)")
    files.append(e)
big = max((x for x in files if "rows" in x), key=lambda x: x["rows"])
meta = {
 "task": "task180",
 "title": "Placing an electricity supplier's revenue protection field team for January to March 2027 from a per-supply consumption screen",
 "domain": "Energy Systems & Utilities",
 "subdomain": "other: revenue protection (energy theft screening)",
 "objective": "Anomaly Detection & Diagnostics",
 "prompt_shape": "other: eight patches, each with its referral count, three winter-history figures and a Q1 capacity figure, plus the call, the runner-up, the gap and a named-parts chart",
 "as_of": "2026-12-07",
 "deliverables": ["field_team_q1_2027.pptx", "patch_screen_q1_2027.csv"],
 "distractor_files": [x["path"] for x in files if x["path"].startswith(("prepayment_vends", "dno_feeder_loss"))],
 "input_gates": {"files": len(files), "formats": sorted(fmts), "largest_file": big["path"], "largest_file_rows": big["rows"]},
 "sources": [{"files": "all files under target/", "origin": "constructed for this task by task180/generator/build.py (seeded, deterministic) around a fictional electricity supplier (Corran Energy) with real north of Scotland places and Met Office station names; no real customer, meter or account is depicted.", "date": "2026-10-11", "license": "CC0-1.0 (original work)"}],
 "created": "2026-10-11",
 "generator": "task180/generator/build.py",
 "files": files,
}
json.dump(meta, open(os.path.join(HERE, "..", "metadata.json"), "w"), indent=2)
print(meta["input_gates"], meta["distractor_files"])

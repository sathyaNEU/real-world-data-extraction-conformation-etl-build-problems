"""Write task153/metadata.json from the built pack."""
import json
import os

import docs as DOC
import records as R

SOURCES = {
    R.F_DAYS: "Keeble Supply Co., telematics service vehicle-day export",
    R.F_GEO: "Keeble Supply Co., telematics service geofence event export",
    R.F_DEV: "Keeble Supply Co., telematics device assignments",
    R.F_UNITS: "Keeble Supply Co., maintenance system unit list and model specifications",
    R.F_FMS: "Keeble Supply Co., fuel management system island transactions, 2025",
    R.F_WEST: "Riverbend Travel Plazas, direct-bill transaction download for Delta Paper & Chemical",
    R.F_CENTRAL: "Crossroads Fleet Card, portal transaction export for Keeble Supply Co.",
    R.F_EAST: "Smoky Mountain Petroleum Marketers, member transaction files for Holston Sanitary Supply",
    R.F_DELIV: "Overton Petroleum Co., customer portal delivery tickets, 2025",
    R.F_INV: "Overton Petroleum Co., customer portal invoice lines, 2025",
    R.F_CRED: "Overton Petroleum Co., customer portal credit memo lines, 2025",
    R.F_RACK: "Overton Petroleum Co., posted rack and TriState contract average history",
    R.F_TANKS: "Keeble Supply Co., yard tank register",
    R.F_IFTA: "Keeble Supply Co., IFTA quarterly returns for the three licences",
    DOC.F_OFFER: "Overton Petroleum Co., transport load offer of August 26, 2026",
    DOC.F_JXN25: "Overton Petroleum Co., Jackson yard tank programme letter, 2025",
    DOC.F_KNX25: "Overton Petroleum Co., Knoxville yard tank programme letter, 2025",
    DOC.F_CARDS: "Riverbend, Crossroads and SMPM pricing schedules (copies held by Keeble Supply Co.)",
    DOC.F_LAYOUT: "Smoky Mountain Petroleum Marketers, member transaction file layout v3",
    DOC.F_TW: "Overton Petroleum Co., tank wagon prices, week of August 24, 2026",
    DOC.F_NOTES: "Keeble Supply Co., fleet services yard notes, August 2026",
    DOC.F_README: "Keeble Supply Co., fleet services list of the files pulled for the fuel review",
}
DISTRACTORS = [R.F_IFTA, DOC.F_TW]
TITLE = ("How many of a fuel jobber's discounted transport loads a distributor contracts for its six yard islands over "
         "eight weeks, when only what each island will hand out is wanted and its vehicles otherwise buy on three "
         "fleet card accounts")


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".txt"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for ln in fh if ln.strip())
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        return sum(max(ws.max_row - 1, 0) for ws in wb.worksheets)
    return None


def write(target, out_path, B=None):
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + SOURCES[f], "date": "2026-08-28",
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task153",
        "title": TITLE,
        "domain": "General Statistics & Data Science",
        "client_domain": "General Statistics & Data Science",
        "house_domain": "supply-chain-logistics",
        "subdomain": "resampling-simulation-monte-carlo-methods (fleet fuel procurement: each yard island's eight-week "
                     "draw replayed from the vehicles' recent duty, stretch by stretch between yard visits, each "
                     "stretch capped at the tankful above the driver's reserve)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a committed load count with each yard's whole loads and the saving they book, a chart of each "
                        "yard's island draw against its card gallons with the loads marked, and two tables (each card "
                        "account's diesel gallons in May, June and July 2026; each month of the 2025 island "
                        "programmes' net gallons delivered and dollars billed above the posted rack)",
        "as_of": "2026-08-28",
        "deliverables": ["overton_loads_sep-nov_2026.xlsx", "yard_island_draw.png"],
        "distractor_files": DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task153/generator/build.py (seeded, deterministic) around "
                               "a fictional Tennessee wholesale distributor, its two acquired companies, a fuel jobber, "
                               "three fleet card programmes and a rack price service, in the layouts of a telematics "
                               "service's vehicle-day and geofence exports, a maintenance system's unit list, a fuel "
                               "management system's island log, three card programmes' transaction files and a "
                               "jobber's portal exports; no real organisation's records or person is depicted.",
                     "date": "2026-08-28", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-17",
        "generator": "task153/generator/build.py",
        "files": out,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta

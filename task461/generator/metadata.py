"""Write task461/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W   # noqa: E402

F = W.FILES
SOURCES = {
    F["hub"]: "the market operator's day-ahead settlement point prices for its North Hub, 2019 to 2 November 2026, "
              "appended from its yearly archive files (formats changing in 2022)",
    F["node"]: "the market operator's day-ahead settlement point prices for the battery's resource node from its first "
               "priced day, under its two names",
    F["points"]: "the market operator's settlement point list",
    F["rt"]: "the market operator's 2026 real-time settlement point prices for the North Hub, fifteen-minute",
    F["as_prices"]: "the market operator's 2026 day-ahead ancillary service clearing prices",
    F["bms"]: "the battery supplier's portal export of the battery management system's hourly records, UTC",
    F["meter"]: "the market operator's revenue meter data for the battery's settlement meter, fifteen-minute, UTC",
    F["settle"]: "the scheduling entity's extract of the battery's day-ahead settlement statement lines",
    F["policy"]: "the owner's day-ahead dispatch policy for the battery (version 2.0, 6 February 2026)",
    F["warranty"]: "an excerpt of the supply and warranty agreement (27 June 2025)",
    F["tests"]: "the battery supplier's 2026 capacity test reports",
    F["dict"]: "the asset management team's field definitions for the folder",
    F["manifest"]: "the list of the files in the folder, with source, as-of date and terms",
}
DISTRACTORS = [F[k] for k in W.DISTRACTORS]
DELIVERABLES = [W.GOLDEN["workbook"], W.GOLDEN["daily"]]


def rows_of(path):
    if path.endswith((".csv", ".txt")):
        with open(path, encoding="utf-8", errors="replace") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": W.PACK_DATE.isoformat(),
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task461",
        "architecture": 1,
        "title": "Which cycling threshold Tallgrove Storage Partners loads into its trading system for Redrock Draw "
                 "Energy Storage's 2027 contract year, the lowest setting on its menu whose expected 2027 cycling days "
                 "stay within the supply warranty's 300 full cycles, conformed from the market operator's day-ahead "
                 "price archive for the North Hub and the battery's node, the battery's BMS export, its revenue meter "
                 "data and its day-ahead settlement statements",
        "domain": "General Statistics & Data Science",
        "subdomain": "data-integration-record-linkage-entity-resolution (a short direct record of the target, the "
                     "battery node's eleven months of day-ahead prices, integrated with the long record of a correlated "
                     "source, the North Hub's eight years, through their overlap)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "04: one dial set from an allowed menu (eight threshold settings), with the expected 2027 "
                        "cycling days at each setting, the warranty's full cycles and the day-ahead net after fees in "
                        "each month of 2026 through October, the net per cycle, a cycle chart and the conformed "
                        "daily-spread file",
        "as_of": W.PACK_DATE.isoformat(),
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["2027", "2026", "300"],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task461/generator/build.py (seeded, deterministic) in the "
                               "layouts of a wholesale market operator's day-ahead and real-time price archives, "
                               "settlement point list, ancillary service prices, revenue meter data and settlement "
                               "statement lines, a battery supplier's BMS portal export and capacity test reports, and "
                               "an owner's dispatch policy and warranty excerpt; the market, its operator, the owner, "
                               "the battery, its supplier, the scheduling entity, every settlement point and the "
                               "people are fictional.",
                     "date": W.PACK_DATE.isoformat(), "license": "CC0-1.0 (original work)"}],
        "created": W.PACK_DATE.isoformat(),
        "generator": "task461/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")
    return meta

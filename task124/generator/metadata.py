"""Write task124/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    K.INVENTORY: "GIS export: the district's lead service line inventory, every service line in the fourteen zones, 8 January 2027",
    K.VERIFICATIONS: "Work management system: service line material verifications, January 2021 to December 2026 (customer system service orders before the March 2023 cut-over)",
    K.CROSSWALK: "Customer system premise numbers to GIS service line ids, built at the March 2023 migration",
    K.CODES: "Service line verification result codes on each recording route, with the inventory class each posts",
    K.PLAN: "Lead service line replacement plan, revision 2 (scope, zones and priority order, plan cost, schedule rule)",
    K.CAPITAL: "Capital improvement plan 2027 to 2037, board draft (the lead service line construction appropriation)",
    K.UNIT_COSTS: "2027 unit cost schedule by zone (engineer's estimate)",
    K.PROGRESS: "LSLR programme office 2026 progress report (counts of work done)",
    K.NOTES: "Field notes for the extract: field meanings and code routes, file by file",
    K.EXTRACT_LOG: "Extract log: each file's source system, date, row count and owner",
    K.COMPLETIONS: "Contract management export: 2026 full replacement completions with pay application amounts",
    K.CHANGE_ORDERS: "Engineering change order log, 2026 replacement contracts",
    K.CONTRACTS: "Purchasing contract register: the 2026 replacement contracts and their vendor records",
    K.AGREEMENTS: "Right-of-entry agreement forms on lines open in the plan, 2022 to January 2027",
    K.TAP_SAMPLES: "Lead and copper compliance samples at tier 1 sites, 2025 and 2026",
    K.METER_EXCHANGES: "Automated meter exchanges, April 2023 to December 2025",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2027-01-08",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task124",
        "title": "When each lead service line replacement zone is finished at the capital plan's annual appropriation",
        "domain": "Energy Systems & Utilities",
        "subdomain": "asset condition and maintenance (lead service line inventory and replacement programme at an Ohio "
                     "regional water district)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "06 (sequenced schedule under capacity): each zone's finish year, lines to replace and cost, "
                        "with the deadline call and a schedule chart",
        "as_of": "2027-01-11",
        "deliverables": list(K.DELIVERABLES),
        "distractor_files": list(K.DISTRACTORS),
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task124/generator/build.py (seeded, deterministic) around a "
                               "fictional water district (Hollins Ford Regional Water District), its fictional city, "
                               "townships, zones, contractors and people in Ohio; no real utility, person, premise or "
                               "contractor is depicted. Shaped on the public lead service line inventories Ohio "
                               "community water systems file.",
                     "date": "2027-01-08", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-12",
        "generator": "task124/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))

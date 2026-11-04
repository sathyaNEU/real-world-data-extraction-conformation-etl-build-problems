"""Write task461/metadata.json from the built pack: the decision, the deliverables, the distractors and each file's
provenance; never the method, a link or a graded figure."""
import json
import os

import world as W

F = W.FILES
SOURCES = {
    F["schedule"]: "Schedule 9 (sustainability performance targets and KPI reporting) of the facility agreement",
    F["hh"]: "the electricity supplier's half-hourly import data for the building's revenue meter, 2026",
    F["bms"]: "the building management system's export of its energy meters' cumulative registers, half-hourly",
    F["register"]: "the building's register of BMS energy meters (January 2027)",
    F["tenancy"]: "the building's tenancy schedule at 31 December 2026",
    F["dips"]: "the facilities team's weekly dips of the generator day tank",
    F["calib"]: "the generator day tank's calibration chart",
    F["dockets"]: "the fuel supplier's delivery dockets for the generator day tank, 2026",
    F["runs"]: "the standby generator controller's event log, 2026",
    F["fgas"]: "the facilities team's F-gas log for the four chillers, 2026",
    F["recovery"]: "the refrigeration contractor's refrigerant recovery record for the site, 2026",
    F["weather"]: "daily weather observations at the city's weather station, 2026",
    F["epc"]: "the building's 2024 non-domestic energy performance certificate",
}
PACK_DATE = "2027-01-15"


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8", errors="replace") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path, n=None):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": PACK_DATE,
                      "license": "CC0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task461",
        "architecture": 3,
        "title": "Whether the base building of Wexmoor Office Trust's Pellow House met its 2026 Scope 2 emissions "
                 "intensity target under the trust's sustainability-linked loan with Corvane Bank, and by how much, "
                 "with the building's Scope 1 generator and refrigerant lines",
        "domain": "Physical & Environmental Sciences",
        "subdomain": "emissions-inventory",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "other: the base building's electricity by month and for the year, its Scope 2 emissions and "
                        "intensity against the target, the generator's gas oil by quarter and each chiller's "
                        "refrigerant with their emissions, in a KPI workbook with a covering letter and chart",
        "as_of": PACK_DATE,
        "deliverables": [W.GOLDEN["report"], W.GOLDEN["letter"]],
        "distractor_files": [F[k] for k in W.DISTRACTORS],
        "stated_inputs": [W.TARGET_KG_M2, W.NLA_M2, W.FACTOR_KG_PER_KWH, W.DIESEL_KG_PER_L, W.GWP_R134A],
        "field_terms": ["generator"],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task461/generator/build.py (seeded, deterministic) in the "
                               "layouts of an electricity supplier's half-hourly data, a building management "
                               "system's meter export, meter and tenancy registers, generator dips, dockets and "
                               "controller events, an F-gas log, a refrigeration contractor's recovery record, weather "
                               "observations, a facility agreement schedule and an energy performance certificate; "
                               "the trust, the building, the bank, the occupiers, the contractors, the city and the "
                               "people are fictional.",
                     "date": PACK_DATE, "license": "CC0 (original work)"}],
        "created": PACK_DATE,
        "generator": "task461/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")
    return meta

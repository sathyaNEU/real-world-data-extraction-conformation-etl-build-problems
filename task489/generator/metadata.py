"""Write task489/metadata.json from the built pack: the decision, the deliverables, the distractors and each file's
provenance; never the method, a link or a graded figure."""
import json
import os

import world as W

F = W.FILES
SOURCES = {
    F["cycles"]: "the SCADA host's plunger lift cycle history for the operator's plunger wells, valve opens in 2026",
    F["prod"]: "production accounting's daily allocated volumes by well for the 2026 production days",
    F["ppa"]: "production accounting's volumetric adjustment journal, postings to January 2027",
    F["runs"]: "production accounting's allocation run log",
    F["register"]: "the Deep Basin equipment register (pads, wells, vessels, pneumatic devices) as exported in January 2027",
    F["analyses"]: "the contract laboratory's separator gas analyses, 2025 and 2026",
    F["counters"]: "the SCADA historian's hourly samples of the automated separators' dump counters",
    F["orders"]: "the maintenance system's 2026 work orders for the Deep Basin pads",
    F["standard"]: "the operator's methane measurement and reporting standard, revision 4",
    F["plan"]: "the operator's 2027 methane reduction plan",
    F["template"]: "the reporting standard's Annex B inventory template",
    F["survey"]: "the measurement contractor's 2026 pneumatic device survey report",
    F["sheet_corrigan"]: "a controller maker's product data sheet",
    F["sheet_aldous"]: "a controller maker's product data sheet",
    F["sheet_brannick"]: "a controller maker's product data sheet",
    F["sheet_trellick"]: "the plunger lift controller maker's specification sheet",
    F["ogi"]: "the operator's 2026 optical gas imaging leak survey results",
    F["tanks"]: "the operator's 2026 storage tank vent tests",
}
PACK_DATE = W.AS_OF.isoformat()


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
        "task": "task489",
        "architecture": 1,
        "title": "Which of Larchmere Resources' Deep Basin pads go into its 2027 zero-emission controller conversion, from "
                 "the 2026 source-level inventory of the pads' pneumatic controllers",
        "domain": "Physical & Environmental Sciences",
        "subdomain": "emissions-inventory",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "other: each pad in or out of the conversion, with each controller's and each pad's 2026 methane in "
                        "the reporting standard's inventory template, the plunger wells' cycles without an arrival and the "
                        "sales gas pressure controllers by maker and area, and a two-slide note for the order",
        "as_of": PACK_DATE,
        "deliverables": list(W.DELIVERABLES),
        "distractor_files": list(W.DISTRACTORS),
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task489/generator/build.py (seeded, deterministic) in the "
                               "layouts of a SCADA host's plunger cycle history and historian export, production "
                               "accounting's daily allocations, adjustment journal and run log, an equipment register, a "
                               "laboratory's gas analyses, a maintenance system's work orders, an operator's reporting "
                               "standard, plan and template, a measurement contractor's survey report, controller makers' "
                               "data sheets, a leak survey and tank vent tests; the operator, the contractors, the makers, "
                               "the laboratory and the people are fictional, and the pads' legal locations are used only as "
                               "names.",
                     "date": PACK_DATE, "license": "CC0 (original work)"}],
        "created": PACK_DATE,
        "generator": "task489/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")
    return meta

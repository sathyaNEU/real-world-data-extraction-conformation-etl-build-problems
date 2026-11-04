"""Write task462/metadata.json from the built pack: the decision, the deliverables, the distractors and each file's
provenance; never the method, a link or a graded figure."""
import json
import os

import world as W

F = W.FILES
SOURCES = {
    F["procedure"]: "the energy company's fuel security procedure PR-07 (the winter coal reserve), revision 4",
    F["accounting"]: "the coal yard accounting work instruction OH-12, revision 2",
    F["control"]: "the survey contractor's control report for the July 2026 handover of the yard surveys",
    F["deliveries"]: "the register of the coal yard survey deliveries, December 2025 to December 2026",
    F["areas"]: "the coal yard's pile area register (plant grid corners)",
    F["density"]: "the fuel laboratory's in-pile bulk density tests, 2025 and 2026",
    F["plan"]: "the approved first-quarter 2027 coal burn plan",
    F["berth"]: "the port's berth log for the plant quay, December 2025 to December 2026",
    F["contracts"]: "the coal purchase contract register",
    F["gu1"]: "the grab unloader GU-1's start and stop log",
    F["historian"]: "the plant historian's 15-minute export of the CV-01 and CV-21 belt scales",
    F["shiftlog"]: "the control room's shift log of the belt scale totalisers",
    F["bunkers"]: "the boiler house bunker levels at the December survey",
    F["analyses"]: "the cargo analyses of the coal received, December 2025 to December 2026",
}
for _m in range(len(W.SURVEYS)):
    SOURCES[W.survey_file(_m)] = "the %s coal yard survey delivered by %s" % (
        W.SURVEYS[_m][0], W.CONTRACTOR_A if _m < W.B_FROM else W.CONTRACTOR_B)
DISTRACTORS = [F["bunkers"], F["analyses"]]


def rows_of(path):
    if path.endswith((".csv", ".xyz")):
        with open(path, encoding="utf-8", errors="replace") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".asc"):
        with open(path) as fh:
            return sum(1 for _ in fh) - 6
    return None


def write(target, out_path, n=None):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": W.ASOF,
                      "license": "CC0 (original work)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task462",
        "architecture": 2,
        "title": "Whether Rannikon Lämpö Oy's harbour power plant went into the 2027 ice season with enough coal in its "
                 "yard to let its coal supplier's winter option cargo lapse, with the yard's receipts by coal and its "
                 "deliveries to the boiler house by quarter",
        "domain": "General Statistics & Data Science (house domain Business & Operations Analytics)",
        "subdomain": "data-integration-record-linkage-entity-resolution",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "other: each pile area's volume and tonnes at the December survey, the reserve, its days of "
                        "cover and the call in a workbook, with the yard's receipts by coal and deliveries by quarter, "
                        "and a chart of the yard's stock at every survey against the floor",
        "as_of": W.ASOF,
        "deliverables": ["coal_reserve_2026.xlsx", "coalyard_stock_2026.svg"],
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            F["bunkers"]: "coal outside the yard; PR-07 section 2 keeps the bunkers out of the reserve",
            F["analyses"]: "coal quality for invoicing and combustion; no figure asked turns on it",
        },
        "stated_inputs": [W.FLOOR_DAYS, 218740, 90],
        "field_terms": [],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task462/generator/build.py (seeded, deterministic) in the "
                               "layouts of drone survey deliveries (an ESRI ASCII grid and a semicolon XYZ text "
                               "export), a survey control report, a pile area register, laboratory density tests, a "
                               "burn plan workbook, a port berth log, a contract register, an unloader event log, a "
                               "plant historian export, a control room shift log and a fuel procedure and work "
                               "instruction; the energy company, the plant, the contractors, the suppliers, the "
                               "vessels and the people are fictional.",
                     "date": W.ASOF, "license": "CC0 (original work)"}],
        "created": W.ASOF,
        "generator": "task462/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as f:
        json.dump(meta, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return meta

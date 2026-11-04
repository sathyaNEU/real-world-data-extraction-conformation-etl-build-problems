"""Write task488/metadata.json from the built pack: the decision, the deliverables, the distractors and each file's
provenance; never the method, a link or a graded figure."""
import json
import os

import names as N

F = N.FILES
SOURCES = {
    F["scada"]: "the fuel farm pump station historian's one-minute export: flow, meter totaliser, header pressure, "
                "pumps running and the tank suction valves, 14 September to 14 October 2026",
    F["register"]: "the Operator's hydrant network register: segments, draw points, sections and the rack line",
    F["shiftlog"]: "the Operator's fuel farm shift log, 12 to 14 October 2026",
    F["maint"]: "the Operator's hydrant maintenance record for week 42: low point drains, filter vessels, pit valve tests",
    F["corbel_tickets"]: "Corbel Into-Plane Services' fuel ticket export, 12 to 14 October 2026",
    F["ng_tickets"]: "Northgarth Aviation Fuelling's ticket export, 12 to 14 October 2026",
    F["corbel_checks"]: "Corbel Into-Plane Services' daily check records, October 2026",
    F["ng_checks"]: "Northgarth Aviation Fuelling's quality control check records, October 2026",
    F["certs"]: "the Operator's register of batch receipts and certificates of quality, 2026",
    F["rack"]: "the truck rack's loading log, 12 to 14 October 2026",
    F["equipment"]: "the corporation's register of into-plane equipment authorised at Windrell",
    F["ng_vehicles"]: "Northgarth Aviation Fuelling's vehicle log, October 2026",
    F["corbel_equipment"]: "Corbel Into-Plane Services' equipment log, October 2026",
    F["recall"]: "the fuel supplier's recall notice for batch J-26-1187",
    F["qm09"]: "the corporation's quality manual procedure QM-09, product quarantine and recall",
    F["pits_q3"]: "the Operator's quarterly hydrant pit valve inspections, July to September 2026",
    F["stock"]: "the Operator's monthly stock reconciliation for September 2026",
}


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
                      "source": "Constructed: " + SOURCES[f], "date": N.AS_OF,
                      "license": "CC0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task488",
        "architecture": 2,
        "title": "Which sections of the Windrell International Airport hydrant and which refuellers held fuel from "
                 "recalled jet fuel batch J-26-1187 at the 05:30 suspension of fuelling on 14 October 2026, and "
                 "which uplifts delivered any of it, for the fuel quality committee's resumption plan and the "
                 "airlines' notices",
        "domain": "Supply Chain & Logistics (house), in General Statistics & Data Science",
        "subdomain": "transportation-network",
        "client_task_type": "data-integration-record-linkage-entity-resolution",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "07: the hydrant's sections and the refuellers, each holding the batch or clear with its "
                        "litres, the airlines' refueller litres, and one recall return row per uplift, in a CSV "
                        "return and a PDF plan with a schematic",
        "as_of": N.AS_OF,
        "deliverables": [N.GOLDEN["csv"], N.GOLDEN["pdf"]],
        "distractor_files": [F[k] for k in N.DISTRACTORS],
        "stated_inputs": ["J-26-1187", "05:30", "14 October", "15 C", "100 L", "10 L"],
        "field_terms": [],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task488/generator/build.py (seeded, deterministic) in the "
                               "layouts of a fuel farm pump station historian, an operator's hydrant network register, "
                               "shift log and maintenance record, two into-plane agents' ticket exports, check records "
                               "and vehicle logs, a truck rack loading log, a certificates register, an equipment "
                               "register, a supplier's recall notice, a quality manual procedure, pit inspections and "
                               "a stock reconciliation; the airport, the corporation, the operator, the agents, the "
                               "supplier, the airlines, the aircraft and the people are fictional.",
                     "date": N.AS_OF, "license": "CC0 (original work)"}],
        "created": N.AS_OF,
        "generator": "task488/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")
    return meta

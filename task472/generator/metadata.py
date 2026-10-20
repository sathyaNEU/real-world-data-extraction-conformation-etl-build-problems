"""metadata.json in the task folder, outside target/: the distractors by bundle path and the portal's keys."""
import json

import pack as P

DISTRACTORS = [P.FILES["ais"], P.FILES["yard"], P.FILES["windows"]]


def write(target, path, n):
    meta = {
        "task": "task472",
        "domain": "Supply Chain & Logistics (ports and container terminals)",
        "client_domain": "General Statistics & Data Science",
        "task_type": "data-integration-record-linkage-entity-resolution",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            P.FILES["ais"]: "the AIS berth stretches measure time alongside, which the program's saving and both asks "
                            "never read; the pilot station's sailings fix when each call ended",
            P.FILES["yard"]: "yard equipment orders share the maintenance system and the labor ledger but are not "
                             "ship-to-shore cranes",
            P.FILES["windows"]: "the 2027 berth windows are next year's commercial agreements, not the fiscal 2026 "
                                "record the program is placed on",
        },
        "deliverables": ["ternmouth_2027_crane_placement.xlsx", "ternmouth_fy2026_large_vessel_calls.csv"],
        "as_of": "2026-10-06",
        "files": sorted(P.FILES.values()),
        "rows": {P.FILES[k]: v for k, v in sorted(n.items())},
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task472/generator); the "
                           "port, terminals, cranes, ships, tides, people and records are fictional",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2026-10-06",
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")

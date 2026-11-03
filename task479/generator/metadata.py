"""metadata.json in the task folder, outside target/: the distractors by bundle path, provenance and the portal's keys."""
import json

import pack as P


def write(path, n):
    meta = {
        "task": "task479",
        "domain": "Physical & Environmental Sciences (emissions inventory)",
        "client_domain": "Physical & Environmental Sciences",
        "task_type": "emissions-inventory",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "distractor_reasons": {
            P.FILES["boiler"]: "boiler B-1 (EU-B1) burns natural gas through its own stack S-4; nothing it emits is an "
                               "EU-P1 vent, and the permit limits EU-P1's VOC alone",
            P.FILES["gen"]: "the emergency generator EU-G1's run hours under permit condition C.3; it has no vent on "
                            "CVS-1 and enters no EU-P1 figure",
            P.FILES["ldar"]: "Method 21 readings on equipment in VOC service (EU-F1, fugitive); leaks are a separate "
                             "emission unit with its own condition, not EU-P1's process vents",
        },
        "deliverables": ["eu_p1_2026_aq117.xlsx", "eu_p1_2026_determination.docx"],
        "as_of": "2027-01-29",
        "files": sorted(P.FILES.values()),
        "rows": {P.FILES[k]: v for k, v in sorted(n.items())},
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task479/generator) from a "
                           "simulation of the plant's 2026 operations and purchasing; the plant, the district, the "
                           "suppliers, the test contractor and the people are fictional",
            "public_specifications": "the layouts follow common batch-system step exports, a thermal oxidizer DAHS "
                                     "one-minute export, warehouse goods-receipt and accounts-payable line extracts, an "
                                     "air permit to operate and an EPA Method 25A destruction efficiency test report",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2027-01-29",
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")

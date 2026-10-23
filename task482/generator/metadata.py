"""metadata.json in the task folder, outside target/: the distractors by bundle path and the portal's keys."""
import json

import pack as P

DISTRACTORS = [P.FILES["presses"], P.FILES["ozone"]]


def write(path, n):
    meta = {
        "task": "task482",
        "domain": "Physical & Environmental Sciences (emissions inventory)",
        "client_domain": "Physical & Environmental Sciences",
        "task_type": "emissions-inventory",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            P.FILES["presses"]: "the Department's press register (type, maker, web width, rated speed, year installed "
                                "and where each press exhausts): what each plant runs, not what its presses used or "
                                "emitted in 2026",
            P.FILES["ozone"]: "the area's ozone monitors' fourth-highest eight-hour values and design values, 2024 to "
                              "2026: why the area is in nonattainment, which no plant's press VOC turns on",
        },
        "stated_inputs": ["25", "2026", "1 July 2027"],
        "deliverables": ["deq_rule18-4_applicability_2027.xlsx", "deq_printing_press_voc_2026.csv",
                         "deq_printing_press_voc_2026.svg"],
        "as_of": "2027-02-26",
        "files": sorted(P.FILES.values()),
        "rows": {P.FILES[k]: v for k, v in sorted(n.items())},
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task482/generator); the state "
                           "agency, the nonattainment area, the rule, the plants, their suppliers, vendors and testing "
                           "firms, and the people are fictional",
            "public_specifications": "the layouts follow the style of a state air agency's information-request returns: "
                                     "production press logs, oxidizer data-historian exports, EPA Method 25A test "
                                     "summaries, safety data sheet masters, hazardous waste manifests and supplier "
                                     "statements",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2027-02-26",
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")

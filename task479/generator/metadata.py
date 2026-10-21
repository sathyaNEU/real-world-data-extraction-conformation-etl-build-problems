"""metadata.json in the task folder, outside target/: the distractors by bundle path and the portal's keys."""
import json

import pack as P

DISTRACTORS = [P.FILES["state"], P.FILES["attend"]]


def write(target, path, n):
    meta = {
        "task": "task479",
        "domain": "Education & Learning Sciences (item response theory and test equating)",
        "client_domain": "Education & Learning Sciences",
        "task_type": "item-response-theory-test-equating",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            P.FILES["state"]: "the state test's 2025 results by campus, a different test, year and scale; the "
                              "designation is on the spring 2026 benchmark",
            P.FILES["attend"]: "chronic absence by campus; the designation counts students tested on the benchmark, "
                               "whatever their attendance",
        },
        "stated_inputs": ["470", "520", "35"],
        "deliverables": ["bellweather_2026-27_tutoring_designation.xlsx"],
        "as_of": "2026-10-02",
        "files": sorted(P.FILES.values()),
        "rows": {P.FILES[k]: v for k, v in sorted(n.items())},
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task479/generator); the network, "
                           "its campuses and students, the vendor and the people are fictional",
            "public_specifications": "the item bank follows the three-parameter logistic model and maximum likelihood "
                                     "scoring as published in the measurement literature",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2026-10-02",
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")

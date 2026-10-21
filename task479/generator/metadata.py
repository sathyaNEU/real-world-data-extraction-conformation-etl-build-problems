"""metadata.json in the task folder, outside target/: the distractors by bundle path and the portal's keys."""
import json

import pack as P

DISTRACTORS = [P.FILES["rates"], P.FILES["visitor"]]


def write(target, path, n):
    meta = {
        "task": "task479",
        "domain": "Survey Research & Official Statistics (seasonal adjustment and official time-series production)",
        "client_domain": "Survey Research & Official Statistics",
        "task_type": "seasonal-adjustment-official-time-series-production",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            P.FILES["rates"]: "the state and county lodging tax rates and their changes; the program qualifies a county "
                              "on its taxable receipts, which are before tax, so no rate enters the estimate",
            P.FILES["visitor"]: "the tourism bureau's visitor spending estimates, all categories of spending and only "
                                "to 2024 (preliminary); the program's basis is the Department's taxable lodging "
                                "receipts, and the estimates neither measure them nor reach 2025",
        },
        "stated_inputs": ["1,800,000"],
        "deliverables": ["tla_rising_destinations_2027.xlsx"],
        "as_of": "2026-10-02",
        "files": sorted(P.FILES.values()),
        "rows": {P.FILES[k]: v for k, v in sorted(n.items())},
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task479/generator); the state, "
                           "its Department of Revenue, the association, its counties, towns, properties, companies "
                           "and people are fictional",
            "public_specifications": "the measures follow the lodging industry's standard definitions (occupancy, "
                                     "average daily rate, revenue per available room) and the benchmark-to-indicator "
                                     "practice of official time-series production, described in no shipped file",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2026-10-02",
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")

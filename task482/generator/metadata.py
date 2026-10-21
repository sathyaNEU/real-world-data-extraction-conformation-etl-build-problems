"""metadata.json in the task folder, outside target/: the distractors by bundle path and the portal's keys."""
import json

import pack as P

DISTRACTORS = [P.FILES["costs"], P.FILES["survey"], P.FILES["returns"]]


def write(target, path, n):
    meta = {
        "task": "task482",
        "domain": "Survey Research & Official Statistics (census, register and administrative data quality)",
        "client_domain": "Survey Research & Official Statistics",
        "task_type": "census-register-administrative-data-quality",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            P.FILES["costs"]: "the re-validation's cost by region; the board chooses on the error rate alone",
            P.FILES["survey"]: "users' satisfaction with the register by user group; no region and no error rate",
            P.FILES["returns"]: "late annual returns by region in 2025; timeliness of filing, not accuracy of records",
        },
        "stated_inputs": ["4"],
        "deliverables": ["sar_register_revalidation_2027_regions.xlsx"],
        "as_of": "2026-10-08",
        "files": sorted(P.FILES.values()),
        "rows": {P.FILES[k]: v for k, v in sorted(n.items())},
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task482/generator); the nation, "
                           "the office, the registers, the businesses and the people are fictional",
            "public_specifications": "the layouts follow common business register extracts, register quality audit "
                                     "records and company notices, described in no shipped file beyond the pack's own "
                                     "dictionary",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2026-10-08",
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")

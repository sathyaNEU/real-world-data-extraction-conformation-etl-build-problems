"""metadata.json in the task folder, outside target/: the distractors by bundle path and the portal's keys."""
import json

import pack as P

DISTRACTORS = [P.FILES["staff"], P.FILES["survey"]]


def write(target, path, n):
    meta = {
        "task": "task482",
        "domain": "Survey Research & Official Statistics (census, register and administrative data quality)",
        "client_domain": "Survey Research & Official Statistics",
        "task_type": "census-register-administrative-data-quality",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            P.FILES["staff"]: "registration staff by office in September; the plans are chosen on timeliness, and "
                              "staffing is what a plan reviews afterwards",
            P.FILES["survey"]: "customer satisfaction in the first half of 2026; perceptions of an earlier period, not "
                               "the third quarter's working days",
        },
        "stated_inputs": ["20"],
        "deliverables": ["cro_timeliness_plans_q3_2026.xlsx"],
        "as_of": "2026-10-09",
        "files": sorted(P.FILES.values()),
        "rows": {P.FILES[k]: v for k, v in sorted(n.items())},
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task482/generator); the nation, "
                           "the registry, its offices, the companies and the people are fictional",
            "public_specifications": "the layouts follow common case management extracts, open caseload snapshots and "
                                     "card acquirer settlement files, described in no shipped file beyond the pack's "
                                     "own dictionary",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2026-10-09",
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")

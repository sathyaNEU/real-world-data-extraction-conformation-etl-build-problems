"""metadata.json in the task folder, outside target/: the distractors by bundle path and the portal's keys."""
import json

import pack as P

DISTRACTORS = [P.FILES["approp"], P.FILES["tuition"], P.FILES["grad"]]


def write(target, path, n):
    meta = {
        "task": "task482",
        "domain": "Survey Research & Official Statistics (census, register and administrative data quality)",
        "client_domain": "Survey Research & Official Statistics",
        "task_type": "census-register-administrative-data-quality",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            P.FILES["approp"]: "the state's fiscal 2026 appropriations by campus, made to branches directly; the grant "
                               "ranks instruction expense, which the appropriation does not measure",
            P.FILES["tuition"]: "2026-27 tuition and fees; a price, not an expense, and of the wrong year",
            P.FILES["grad"]: "graduation rates of the 2019 cohort; an outcome the grant does not rank on",
        },
        "stated_inputs": ["4.5"],
        "deliverables": ["lhecb_2027-28_instructional_investment_awards.xlsx"],
        "as_of": "2026-10-09",
        "files": sorted(P.FILES.values()),
        "rows": {P.FILES[k]: v for k, v in sorted(n.items())},
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task482/generator); the state, "
                           "the board, the campuses, their students and the people are fictional",
            "public_specifications": "the federal files follow the IPEDS directory (HD), finance (F1A, GASB) and "
                                     "12-month enrollment (E12) layouts and variable names, including the finance "
                                     "parent/child indicator PRCH_F and parent UNITID IDX_F; the state files are a "
                                     "coordinating board's own layouts, described in the pack's dictionary",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2026-10-09",
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")

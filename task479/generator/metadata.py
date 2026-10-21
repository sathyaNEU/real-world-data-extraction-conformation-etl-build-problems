"""metadata.json in the task folder, outside target/: the distractors by bundle path and the portal's keys."""
import json

import pack as P

DISTRACTORS = [P.FILES["rebates"], P.FILES["receipts"], P.FILES["survey"]]


def write(target, path, n):
    meta = {
        "task": "task479",
        "domain": "Healthcare Delivery & Health Economics (payment, claims and health plan analytics)",
        "client_domain": "Healthcare Delivery & Health Economics",
        "task_type": "payment-claims-health-plan-analytics",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            P.FILES["rebates"]: "the 2025 pharmacy rebates credited to the cooperative's reserve; the review memo "
                                "takes plan-paid claims before rebates, so no district's figure nets them",
            P.FILES["receipts"]: "the districts' fiscal 2026 contributions billed and received; the review compares "
                                 "claims with the claims component of the 2026 rate, and no receipt enters it",
            P.FILES["survey"]: "a state survey's 2025 claims cost per member per month by plan type; the review rests "
                               "on each district's own claims and no benchmark enters it",
        },
        "stated_inputs": ["125,000", "250,000", "3,000", "1,500"],
        "deliverables": ["mvshc_january_2027_contribution_review.xlsx"],
        "as_of": "2026-10-06",
        "files": sorted(P.FILES.values()),
        "rows": {P.FILES[k]: v for k, v in sorted(n.items())},
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task479/generator); the "
                           "cooperative, the districts, the administrator, the carrier, their members and the people "
                           "are fictional",
            "public_specifications": "the layouts follow common third-party administrator claims lag reports, "
                                     "eligibility files and specific stop-loss advisories (12/15 contract basis), "
                                     "described in no shipped file beyond the pack's own dictionary",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2026-10-06",
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")

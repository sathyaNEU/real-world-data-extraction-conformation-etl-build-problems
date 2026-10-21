"""metadata.json in the task folder, outside target/: the distractors by bundle path and the portal's keys."""
import json

import pack as P

DISTRACTORS = [P.FILES["rebates"], P.FILES["bench"], P.FILES["roster"]]


def write(target, path, n):
    meta = {
        "task": "task479",
        "domain": "Healthcare Delivery & Health Economics (payment, claims and health plan analytics)",
        "client_domain": "Healthcare Delivery & Health Economics",
        "task_type": "payment-claims-health-plan-analytics",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            P.FILES["rebates"]: "the 2025 pharmacy rebates credited to each employer's funding account; the "
                                "assumptions memo keeps rebates out of claims, so retained claims are gross of them",
            P.FILES["bench"]: "a regional survey's 2025 claims cost per member per month by industry; the notice rests "
                              "on each group's own experience, and no benchmark enters it",
            P.FILES["roster"]: "the groups' employers, industries and account managers; the notices are by group "
                               "number and nothing on the roster changes a group's claims",
        },
        "stated_inputs": ["250,000", "125,000", "100,000", "7.5"],
        "deliverables": ["mba_2027_funding_true_up.xlsx"],
        "as_of": "2026-10-05",
        "files": sorted(P.FILES.values()),
        "rows": {P.FILES[k]: v for k, v in sorted(n.items())},
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task479/generator); the "
                           "administrator, the carrier, the employers, their members and the people are fictional",
            "public_specifications": "the layouts follow common third-party administrator claims lag reports, "
                                     "eligibility files and specific stop-loss large claimant reports (12/15 contract "
                                     "basis), described in no shipped file beyond the pack's own dictionary",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2026-10-05",
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")

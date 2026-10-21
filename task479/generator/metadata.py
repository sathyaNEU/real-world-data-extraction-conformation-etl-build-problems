"""metadata.json in the task folder, outside target/: the distractors by bundle path and the portal's keys."""
import json

import pack as P

DISTRACTORS = [P.FILES["rebates"], P.FILES["roster"], P.FILES["survey"]]


def write(target, path, n):
    meta = {
        "task": "task479",
        "domain": "Healthcare Delivery & Health Economics (payment, claims and health plan analytics)",
        "client_domain": "Healthcare Delivery & Health Economics",
        "task_type": "payment-claims-health-plan-analytics",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            P.FILES["rebates"]: "the 2025 pharmacy rebates credited to the trust's reserve; the review memo takes "
                                "retained claims before rebates, so no employer's figure nets them",
            P.FILES["roster"]: "the member employers' names, industries, joining years and account managers; nothing "
                               "on it enters an employer's expected claims",
            P.FILES["survey"]: "a broker survey's 2025 small-group claims cost and renewal changes by group size; the "
                               "review rests on the trust's own experience and no external benchmark enters it",
        },
        "stated_inputs": ["150,000", "25,000"],
        "deliverables": ["crbht_2027_renewal_surcharges.xlsx"],
        "as_of": "2026-10-07",
        "files": sorted(P.FILES.values()),
        "rows": {P.FILES[k]: v for k, v in sorted(n.items())},
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task479/generator); the trust, "
                           "the employers, the administrator, the carrier, their members and the people are fictional",
            "public_specifications": "the layouts follow common third-party administrator claims lag reports, "
                                     "eligibility files, high-cost claimant reports and specific stop-loss "
                                     "reimbursement statements (12/15 contract basis), described in no shipped file "
                                     "beyond the pack's own dictionary",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2026-10-07",
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")

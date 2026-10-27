#!/usr/bin/env python3
"""task464: metadata.json, which sits in the task folder and never under target/."""
import json
import os

import pack
import world

FILES = [
    ("provider_directory_2027.csv", "spine",
     "The plan's own provider directory, one row per site per annual attestation cycle.",
     "Harrowgate Community Health Plan, provider data management", "2026-11-18"),
    ("state_licence_register.xlsx", "spine",
     "The state licensing authority's outpatient facility register, facility and corporate rows with the"
     " amendment history.", "State licensing authority, public register extract", "2027-02-19"),
    ("staffing_roster_2026q4.csv", "operating extract",
     "The roster of staffed treatment sessions a week by site, effective 1 October 2026.",
     "Harrowgate Community Health Plan, clinical operations", "2026-10-01"),
    ("treatment_encounters.db", "spine",
     "Four contract years of outpatient dialysis and infusion treatment encounters, in the two layouts the"
     " clearinghouse change left behind.", "Harrowgate Community Health Plan, encounter data warehouse",
     "2027-01-05"),
    ("enrolment_projection_2027.csv", "operating extract",
     "The plan's enrolment projection by service area for 2027.",
     "Harrowgate Community Health Plan, actuarial services", "2027-01-15"),
    ("network_agreement_2027_capacity_terms.pdf", "governing document",
     "Schedule 4 of the 2027 provider network agreement: capacity and service area adequacy.",
     "Harrowgate Community Health Plan, network contracting", "2026-12-10"),
    ("state_adequacy_filing_2026.xlsx", "context artifact",
     "The plan's annual network adequacy filing for the 2026 network year, position as at 1 January 2026.",
     "Harrowgate Community Health Plan, regulatory reporting", "2026-03-31"),
    ("out_of_network_payments_2026.csv", "operating extract",
     "Out-of-network outpatient dialysis and infusion claim lines adjudicated in 2026.",
     "Harrowgate Community Health Plan, claims operations", "2027-01-09"),
    ("out_of_network_payments_runout_2027q1.csv", "operating extract",
     "2026 services adjudicated after the 2026 close, to the run-out pull.",
     "Harrowgate Community Health Plan, claims operations", "2027-02-16"),
    ("out_of_network_payments_reconciliation_2026.xlsx", "control",
     "The out-of-network register's own control totals by adjudication quarter.",
     "Harrowgate Community Health Plan, claims operations", "2027-01-09"),
    ("encounter_extract_transmittal.json", "control",
     "The encounter extract's transmittal: pull date, tables and row counts by service quarter.",
     "Harrowgate Community Health Plan, encounter data warehouse", "2027-01-05"),
    ("nemt_trips_2026.csv", "distractor",
     "Non-emergency medical transport trips by service area and month, 2026.",
     "Harrowgate Community Health Plan, transportation benefit", "2027-01-07"),
    ("licence_fee_schedule_2026.pdf", "distractor",
     "The state licensing authority's annual outpatient facility fee schedule, effective 1 July 2026.",
     "State licensing authority", "2026-07-01"),
]
LICENCE = ("Compiled by Harrowgate Community Health Plan network contracting for the 2027 network year."
           " Plan records are the plan's own and are released for contracting use; the state licensing"
           " register and the fee schedule are public records of the state licensing authority, reproduced"
           " as published.")


def write(task_dir, truth):
    doc = {
        "task": "task464",
        "domain": "healthcare-delivery-health-economics",
        "subdomain": "payment-claims-health-plan-analytics",
        "objective": "etl",
        "prompt_shape": "07",
        "as_of": world.ASOF.isoformat(),
        "currency": "USD",
        "compiled_by": "Harrowgate Community Health Plan, network contracting",
        "compiled_on": pack.RUNOUT_PULL.isoformat(),
        "licence": LICENCE,
        "files": [{"path": "target/%s" % f[0], "role": f[1], "covers": f[2], "source": f[3],
                   "date": f[4], "licence": "plan record, released for contracting use"
                   if f[3].startswith("Harrowgate") else "public record of the state licensing authority"}
                  for f in FILES],
        "distractor_files": ["target/nemt_trips_2026.csv", "target/licence_fee_schedule_2026.pdf"],
        "stated_inputs": {
            "service_areas": 12,
            "contract_year_for_demand": 2026,
            "network_year": "2027",
        },
        "field_terms": ["station", "chair", "session", "position", "slot"],
        "deliverables": ["outpatient_capacity_2027.csv", "area_capacity_2027.xlsx"],
        "portal": {
            "call": "the 2027 network's weekly treatment slots and the twelve service areas against the"
                    " adequacy standard",
            "network_weekly_slots": truth["call"]["network"],
            "areas_short": len(truth["call"]["short"]),
        },
    }
    with open(os.path.join(task_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")
    return doc

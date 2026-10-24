"""metadata.json: the pairing, the files and their rows, the distractors, provenance and licence."""
import json
import os


def write(figs, names, path):
    target = os.path.join(os.path.dirname(path), "target")
    files = sorted(os.listdir(target))
    rows = {names["extract"]: figs["rows"]["extract"], names["emr"]: figs["rows"]["emr"],
            names["legacy"]: figs["rows"]["legacy"], names["claims"]: figs["rows"]["claim_lines"],
            names["remit"]: figs["rows"]["remittance"]}
    doc = {
        "task": "task482",
        "domain": "Healthcare Delivery & Health Economics (payment, claims and health plan analytics)",
        "client_domain": "Healthcare Delivery & Health Economics",
        "task_type": "payment-claims-health-plan-analytics",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": [names["quality"], names["budget"]],
        "distractor_reasons": {
            names["quality"]: "the provider numbers' 2025 and 2026 hospice quality reporting measures (care index, visits in "
                              "the last days of life, assessments, family survey); quality scores enter neither the "
                              "aggregate cap nor the inpatient cap, so no figure reads them",
            names["budget"]: "the 2027 operating budget's census, admissions and revenue by program; a plan for the next "
                             "year, while the FY2026 cap counts the days beneficiaries did and will receive",
        },
        "wrong_basis_distractors": {},
        "stated_inputs": ["31 December 2026 close", "FY2026", "eight provider numbers", "USD millions to one decimal",
                          "whole days", "percentages to one decimal"] + sorted(figs["provider_numbers"].values()) +
                         ["35,361.44", "35361.44"],
        "deliverables": ["fy2026_hospice_cap_accrual.xlsx"],
        "as_of": "2026-12-31",
        "files": files,
        "rows": rows,
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task482/generator); Wendleglen "
                           "Hospice & Palliative Care, Fallowmere Hospice, their programs and places, their staff, the "
                           "beneficiaries, identifiers, provider numbers and every record and number in the files are "
                           "fictional",
            "public_specifications": "the FY2026 hospice payment rates, labor shares and aggregate cap amount are those of "
                                     "the FY2026 Medicare hospice payment rule (CMS-1835-F, 90 FR 37404, 5 August 2025); the "
                                     "proportional method and the inpatient limit follow 42 CFR 418.309 and 418.302(f); the "
                                     "claim and remittance fields follow the institutional claim's type of bill, revenue "
                                     "code and HCPCS conventions and the 835 remittance's CLP and PLB records with claim "
                                     "adjustment reason code 253 for sequestration; the census register's discharge statuses "
                                     "are UB-04 patient status codes; diagnosis codes are ICD-10-CM",
            "licence": "CC0 1.0 (constructed data); the public rule figures are US government works",
            "date": "2026-12-31",
        },
    }
    with open(path, "w") as f:
        json.dump(doc, f, indent=1)

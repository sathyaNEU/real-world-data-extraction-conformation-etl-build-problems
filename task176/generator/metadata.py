"""task176 metadata.json: the portal's keys and the distractors, outside target/."""
from __future__ import annotations

import json
import os

import common as C


def write(root):
    m = {
        "task": "task176",
        "title": "How many of Allerton's licensed family child care homes will close during 2027, two to four years "
                 "after a start-up grant round licensed a wave of home providers",
        "domain": "Sociology & Demography",
        "client_domain": "Sociology & Demography",
        "subdomain": "event history and life course analysis (a closure hazard read on the provider's family life "
                     "course, the summer before her youngest own child starts kindergarten, from the licensing record's "
                     "home-months and the capacity worksheets' children)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "one count to the nearest 50; subsidised child-days by region and half-year; subsidy money paid "
                        "to the homes by region and quarter of the payment run",
        "as_of": C.ASSEMBLED.isoformat(),
        "deliverables": [C.DELIVERABLE],
        "distractor_files": list(C.DISTRACTORS),
        "distractors": [
            {"file": C.F_QRIS, "wrong_basis": False,
             "why_relevant": "the quality ratings of the homes, a natural covariate for which homes close",
             "why_unused": "no figure reads it; ratings carry no information on closure in this record",
             "ruled_out_by": "the call's model and every ask read other files"},
            {"file": C.F_CACFP, "wrong_basis": False,
             "why_relevant": "the food program claims of the homes, a measure of how many children each home serves",
             "why_unused": "no figure reads it; the call reads the licensing record and the asks the subsidy runs",
             "ruled_out_by": "the prompt's tables, both on the subsidy"},
            {"file": C.F_VIS, "wrong_basis": False,
             "why_relevant": "the inspectors' visits to the homes, with complaint investigations",
             "why_unused": "no figure reads it",
             "ruled_out_by": "the prompt's tables, both on the subsidy"},
            {"file": C.F_MRS, "wrong_basis": False,
             "why_relevant": "the prices homes charge by county and age group, the economics of running a home",
             "why_unused": "a 2025 survey of private prices; no figure reads it",
             "ruled_out_by": "its own header (weekly private-pay prices in spring 2025)"},
        ],
        "stated_inputs": ["2026", "2027", "31 December 2026", "50"],
        "field_terms": [],
    }
    with open(os.path.join(root, "metadata.json"), "w") as fh:
        json.dump(m, fh, indent=1)
        fh.write("\n")

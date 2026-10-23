"""task173 metadata.json: the portal's keys and the distractors, outside target/."""
from __future__ import annotations

import json
import os

import common as C


def write(root):
    m = {
        "task": "task173",
        "title": "Varner Valley Public Utility District's April to September 2027 irrigation pumping energy, the first season "
                 "the Varner River watermaster holds the riparian and pre-1914 rights to a quarter of their allotments",
        "domain": "Energy Systems & Utilities",
        "client_domain": "Energy Systems & Utilities",
        "subdomain": "load forecasting (an irrigation rate class's season energy under a change in its surface water supply, "
                     "built as acre-feet each pumping plant must move times that plant's own energy per acre-foot)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "one season energy in 5,000 MWh steps; delivery-point energy by billing month; delivery-point "
                        "demand in each monthly system peak hour; irrigation services and billed energy by delivery point",
        "as_of": C.ASOF,
        "deliverables": [C.DELIVERABLE],
        "distractor_files": list(C.DISTRACTORS),
        "distractors": [
            {"file": C.F_PTEST, "wrong_basis": False,
             "why_relevant": "the PUD's pump efficiency tests, with each tested plant's head, flow, input and "
                             "energy per acre-foot",
             "why_unused": "it covers only plants of 75 hp and more, all of them Lone Bench wells, whose 2027 energy the "
                           "2022 season already gives; no figure reads it",
             "ruled_out_by": "the dictionary (plants of 75 hp and more) and the register's plant sizes"},
            {"file": C.F_CROP, "wrong_basis": False,
             "why_relevant": "the county's 2025 harvested acreage by crop, the crops the class irrigates",
             "why_unused": "it is county-wide acreage and value, with no water or energy; no figure reads it",
             "ruled_out_by": "its own heading (all of Kestrel County) and its columns"},
        ],
        "stated_inputs": ["2027", "2026", "5,000", "1 April", "30 September"],
        "field_terms": [],
    }
    with open(os.path.join(root, "metadata.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(m, f, indent=1)
        f.write("\n")

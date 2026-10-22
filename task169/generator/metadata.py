"""task169 metadata.json: the portal's keys and the distractors, outside target/."""
from __future__ import annotations

import json
import os

import common as C


def write(root):
    m = {
        "task": "task169",
        "title": "Two-year returns of the people Pembroke expects to release to parole in 2027, the first cohort under "
                 "an act that ends recommitment for parole violations",
        "domain": "Criminology & Justice",
        "client_domain": "Criminology & Justice",
        "subdomain": "recidivism and risk assessment (a release cohort's two-year return-to-prison rate under a change "
                     "in revocation law, built from the arrest process and the courts' conversion of arrests into "
                     "prison commitments)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "one rate in five-point steps; recommitments by office and basis; parolee-days on detainer by "
                        "district and half-year; writ days by institution and half-year",
        "as_of": C.ASSEMBLED.isoformat(),
        "deliverables": ["returns_projection_2027.xlsx"],
        "distractor_files": list(C.DISTRACTORS),
        "distractors": [
            {"file": C.F_PRAT, "wrong_basis": False,
             "why_relevant": "the Department's validation of the release risk tool on the 2019 and 2020 releases, with "
                             "return shares by risk level",
             "why_unused": "it reports discrimination and returns of every kind under the old law for two early "
                           "cohorts; no figure reads it",
             "ruled_out_by": "its own data section (releases of 2019 and 2020, admissions of any kind)"},
            {"file": C.F_CASE, "wrong_basis": False,
             "why_relevant": "the Board's month-end parole caseload by office, with interstate compact cases",
             "why_unused": "it counts people under supervision on dates, not releases or returns; no figure reads it",
             "ruled_out_by": "its own header and the dictionary"},
        ],
        "stated_inputs": ["26-114", "2027", "730", "1 July 2025", "30 June 2026"],
        "field_terms": [],
    }
    with open(os.path.join(root, "metadata.json"), "w") as fh:
        json.dump(m, fh, indent=1)
        fh.write("\n")

"""task170 metadata.json: the portal's keys, the distractors and the provenance, outside target/."""
from __future__ import annotations

import json
import os

import common as C

DISTRACTORS = ["staff_benefits_survey_2025.xlsx", "sickness_absence_2025_2026.csv"]


def write(task_dir, target, rows):
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    big = max(rows, key=rows.get)
    meta = {
        "task": "task170",
        "title": "What a hospital group will pay in employer pension matching in FY2027 on the first intake enrolled "
                 "automatically, when every earlier intake had to opt in and the record shows only the hires who "
                 "chose to join",
        "domain": "Psychology & Behavioral Science",
        "client_domain": "Psychology & Behavioral Science",
        "subdomain": "decision-making and computational behavioural modelling (a default's take-up under inertia)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "the FY2027 employer match on the 2027 intake by hospital and in total, the intake contributing "
                        "on the December 2027 payroll, the match paid on the January to October 2026 payrolls and the "
                        "long-standing active members by hospital, and a one-page budget note",
        "as_of": C.PULL.isoformat(),
        "deliverables": ["vindeholm_match_forecast_2027.xlsx", "match_forecast_note_2027.docx"],
        "distractor_files": DISTRACTORS,
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big, "largest_file_rows": rows[big]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task170/generator/build.py (seeded, deterministic) around a "
                               "fictional country (Tarnland), a fictional county and its hospital group, a fictional "
                               "pension administrator and insurer, in the layouts of an HR history extract, a pension "
                               "member register, an insurer's bordereau, a payroll deduction export, a requisition "
                               "tracker, plan rules, a committee paper and a pay scale extract; no real organisation's "
                               "records or person is depicted.",
                     "date": C.PULL.isoformat(), "license": "CC0-1.0 (original work)"}],
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")

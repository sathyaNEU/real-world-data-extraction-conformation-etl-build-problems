"""metadata.json: the portal's keys and the files the solution never reads."""
import json
import os

import world as W


def write(task, g):
    out = {
        "task": "task195",
        "domain": "Biomedical and clinical research (genomics, high-dimensional association)",
        "objective": "Anomaly Detection & Diagnostics",
        "as_of": W.AS_OF.isoformat(),
        "answer": ("Replace the screen in service at the %s cutoff from 1 July 2027" % g["call"]
                   if g["call"] != "hold" else "Hold the change"),
        "distractor_files": sorted("target/" + W.FILES[k] for k in W.DISTRACTORS),
        "stated_inputs": ["2027-07-01", "2027-06-30", "2027-02", "0.030", "0.020", "0.015", "0.010",
                          "0.050"],
        "field_terms": ["panel", "plate", "well", "read", "mixture"],
        "provenance": ("Every file is constructed for this task from a simulated laboratory. No real "
                       "specimen, person or organisation is represented; the organisations, projects "
                       "and people are invented."),
        "licence": "constructed, no third-party data",
    }
    p = os.path.join(task, "metadata.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return p

"""task170 metadata.json: the portal's keys, the distractors and the provenance, outside target/."""
from __future__ import annotations

import json
import os

import common as C

DISTRACTORS = ["insecticide_susceptibility_2025.csv", "rainfall_daily_2019_2026.csv"]


def write(task_dir, target, rows):
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    big = max(rows, key=rows.get)
    meta = {
        "task": "task170",
        "title": "How many Ombeni fever cases a county-wide repellent net campaign will avert among the people sleeping "
                 "under its nets, when the county's vector bites earlier and more outdoors than at any site of the "
                 "trial that measured the nets",
        "domain": "Epidemiology & Public Health",
        "client_domain": "Epidemiology & Public Health",
        "subdomain": "health burden and impact modelling (a vector-control campaign's cases averted)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "the county's cases averted among net users with each sub-county's, the share of expected cases, "
                        "the nets to distribute and the confirmed cases reported in 2026 by sub-county, and a chart",
        "as_of": C.PULL.isoformat(),
        "deliverables": ["ruvari_cases_averted_2027.xlsx", "cases_averted_by_subcounty.png"],
        "distractor_files": DISTRACTORS,
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big, "largest_file_rows": rows[big]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task170/generator/build.py (seeded, deterministic) around a "
                               "fictional Kenyan county, its health department, an implementing non-profit, a donor, a "
                               "fictional mosquito-borne fever, its vector and a fictional trial, in the layouts of human "
                               "landing catch sheets, a behaviour survey, a campaign registration app, a KHIS export, a "
                               "master facility list, a planning baseline and a trial report; no real organisation's "
                               "records, outbreak or person is depicted.",
                     "date": C.PULL.isoformat(), "license": "CC0-1.0 (original work)"}],
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")

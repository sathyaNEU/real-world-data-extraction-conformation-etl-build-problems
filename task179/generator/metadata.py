"""metadata.json in the task folder, outside target/: the distractors by bundle path, the portal's keys and the
provenance record. The setting is fictional and every file is synthetic; this record says so, the pack stays in its
own world."""
import csv
import json
import os

import pack as P

DISTRACTORS = [P.F_LM, P.F_AD, P.F_BU]


def rows(target):
    import openpyxl
    out = {}
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        if f.endswith(".csv"):
            with open(p, newline="", encoding="utf-8-sig") as fh:
                out[f] = sum(1 for _ in csv.reader(fh)) - 1
        elif f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(p, read_only=True)
            out[f] = sum(max(0, ws.max_row - 1) for ws in wb.worksheets)
    return out


def write(target, path):
    meta = {
        "task": "task179",
        "domain": "Epidemiology & Public Health (infectious disease transmission modeling)",
        "client_domain": "Epidemiology & Public Health",
        "task_type": "infectious-disease-transmission-modeling",
        "objective": "Forecasting & Predictive Modeling",
        "setting": "fictional: the Republic of Orvanthe, its Dunmarrow Province and districts, the Dunmarrow Provincial "
                   "Health Directorate, its laboratories, Larrowmede Medical Relief, Tamberlow virus disease and every "
                   "person named are invented; no real place, agency, organisation, pathogen or outbreak is described",
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            P.F_LM: "the Kettlebank public health laboratory's results for the same weeks; the turnaround check is the "
                    "Tamberlow field laboratory's alone and no case count or interval is read from laboratory rows",
            P.F_AD: "admissions to the organisation's two treatment centres; the planning figure is every case in the seven "
                    "districts by onset, and the centres' share is applied by the desk afterwards",
            P.F_BU: "the safe burial teams' log; deaths and burials enter neither the interval, the reproduction number "
                    "nor the asks",
        },
        "stated_inputs": ["50", "92", "24", "21"],
        "deliverables": ["tvd_projection_w49-w52.xlsx", "tvd_projection_curve.svg"],
        "as_of": "2026-10-19",
        "files": sorted(os.listdir(target)),
        "rows": rows(target),
        "sources": {
            "constructed": "every file is synthetic, generated for this task by its generator (task179/generator) from a "
                           "simulated outbreak; the setting, the organisations, the pathogen and the people are fictional",
            "public_specifications": "the layouts follow common outbreak line lists, contact-tracing registries, "
                                     "transmission-link exports and laboratory analyser exports in general form; no real "
                                     "system's export, template or report is reproduced",
            "licence": "CC0 1.0 (synthetic data)",
            "date": "2026-10-19",
        },
    }
    with open(path, "w") as f:
        json.dump(meta, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return meta


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    write(os.path.join(here, "..", "target"), os.path.join(here, "..", "metadata.json"))

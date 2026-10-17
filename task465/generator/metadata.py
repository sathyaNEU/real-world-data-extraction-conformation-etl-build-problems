"""metadata.json: the task's identity, its files, the distractors, the input gates and the sources."""
import json
import os

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
F = W.FILES
DISTRACTORS = [F[k] for k in W.DISTRACTORS]
DELIVERABLES = [W.GOLDEN["workbook"], W.GOLDEN["table"]]


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path, counts=None):
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    rows = {f: rows_of(os.path.join(target, f)) for f in files}
    big = max((f for f in files if rows[f] is not None), key=lambda f: rows[f])
    meta = {
        "task": "task465",
        "architecture": 2,
        "title": "How many Home Energy Medical Assistance caseworkers each of Callowmere Electric's nine service divisions "
                 "needs for 2027 under the programme plan's caseload standard, the 2025 eligible households fused from "
                 "a state energy survey and a state health survey with the utility's screening pilot; with each "
                 "division's households on the medical baseline rate at the end of October 2026 and households given a "
                 "backup battery from January to October 2026",
        "domain": "General Statistics & Data Science",
        "subdomain": "data-integration-record-linkage-entity-resolution (two state surveys that each measured one of the "
                     "programme's two eligibility traits, fused by division and income band with the screening pilot's "
                     "within-band association, into one conformed table)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "07: a grid of nine divisions (eligible households and caseworkers), the total caseworkers, the "
                        "conformed table's eighteen division-and-band cells, two figures per division beside the "
                        "staffing and a chart of eligible households labelled with caseworkers",
        "as_of": W.AS_OF,
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["2027", "2025", "2026", "nine", "Callowmere", "25,000", "49,999", "50,000", "400"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big, "largest_file_rows": rows[big]},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task465/generator/build.py (seeded, deterministic) in the layouts "
                       "of a state energy office's survey public-use file and technical notes, a state health "
                       "department's survey household file and codebook, a state demographer's county household "
                       "estimates, and an electric utility's screening pilot records and report, division register, "
                       "programme plan, medical baseline enrolment extract and battery work orders; the state is unnamed "
                       "and its counties, agencies' figures, the utility and the people are fictional",
             "date": "2026-11-16",
             "license": "original work for this task; no third-party data"}],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta

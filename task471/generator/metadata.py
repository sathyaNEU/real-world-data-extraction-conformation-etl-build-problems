"""metadata.json: the task's identity, its files, the distractors, the input gates and the sources."""
import json
import os

import pack as P
import world as W

F = P.FILES


def write(target, out_path, deliverables, n=None):
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    rows = {P.FILES[k]: v for k, v in (n or {}).items()}
    big = max(rows, key=lambda f: rows[f]) if rows else None
    meta = {
        "task": "task471",
        "architecture": 3,
        "title": "Which of the state's sixteen counties qualify for the 2027 Well Water Assistance allocation, an "
                 "estimated 250 or more private domestic wells in the county's survey population above the nitrate "
                 "standard on the 2025-26 Private Well Nitrate Survey; with each county's wells on the survey's two "
                 "lists, its wells first tested above the standard and retested by June 30, 2026 and how many of "
                 "those retests were still above it, and a chart of the estimates against the line",
        "domain": "General Statistics & Data Science",
        "subdomain": "data-integration-record-linkage-entity-resolution (a health department links two overlapping "
                     "lists of private wells, a permit database and sixteen assessors' rolls, conforms three "
                     "laboratories' results and estimates county totals from a survey sampled from both lists)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "10: a scorecard: each of 16 counties' estimated wells above the standard against the 250-well "
                        "line, with each county's wells on the survey's lists and its retests",
        "as_of": W.AS_OF.isoformat(),
        "deliverables": deliverables,
        "distractor_files": [F[k] for k in P.DISTRACTORS],
        "stated_inputs": ["2025-26", "2027", "250", "June 30, 2026", "10 mg/L"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big,
                        "largest_file_rows": rows.get(big)},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task471/generator/build.py (seeded, deterministic) in the layouts "
                       "of a state private well program's records: a well construction permit database extract, "
                       "sixteen county assessors' residential parcel rolls compiled in their own layouts, a survey draw "
                       "manifest, three laboratories' result exports, a retest kit request log, a county code table, "
                       "a survey design and fieldwork report, an allocation standard, a household fact sheet and a "
                       "certified laboratory roster; the state is unnamed and the department, counties, towns, "
                       "laboratories, households and people are fictional",
             "date": W.AS_OF.isoformat(),
             "license": "original work for this task; no third-party data"}],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta

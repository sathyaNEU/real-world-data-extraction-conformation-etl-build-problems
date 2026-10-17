"""metadata.json: the task's identity, its files, the distractors, the input gates and the sources."""
import json
import os

import world as W

F = W.FILES
DISTRACTORS = [F[k] for k in W.DISTRACTORS]
DELIVERABLES = [W.GOLDEN["workbook"]]


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
        "task": "task469",
        "architecture": 1,
        "title": "Which of the minimum ground times the carriers filed for summer 2027 at Kelderby's E gates the "
                 "Kelderby Airport Authority should send back, and the shortest it would accept from each carrier "
                 "relationship; with the share of 2026 peak turns needing longer at each ground time in a chart, and "
                 "each relationship's turns in the summer 2027 initial submissions' peak week",
        "domain": "General Statistics & Data Science",
        "subdomain": "data-integration-record-linkage-entity-resolution (the authority's stand log linked to three "
                     "operators' flight logs, the affiliate register and the aircraft register into turns; the carriers' "
                     "SSIM submissions conformed to operating flights and turns)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "14: cuts of a distribution per segment: for each of six carrier relationships, the share of "
                        "turns needing longer than each ground time, the verdict on its filing and the shortest ground "
                        "time accepted, beside each relationship's turns and short turns in the 2027 peak week",
        "as_of": "2026-10-30",
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["2027", "12 to 18 July 2027", "2026"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big, "largest_file_rows": rows[big]},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task469/generator/build.py (seeded, deterministic) in the layouts "
                       "of an airport authority's stand log (AODB events), regional operators' flight logs, IATA "
                       "SSIM Chapter 7 schedule files, an authority's schedule facilitation guideline and file layout "
                       "note, carrier filings, affiliate and aircraft registers, a fleet plan, IATA delay codes grouped "
                       "by the authority, and a punctuality workbook and handling staffing file the review does not "
                       "use; the province is unnamed and the airport, authority, airlines, operators and people are "
                       "fictional",
             "date": "2026-10-30",
             "license": "original work for this task; no third-party data"}],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta

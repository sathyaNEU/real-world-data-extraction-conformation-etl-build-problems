"""metadata.json: the task's identity, its files, the distractors, the input gates and the sources."""
import json
import os

import world as W

F = W.FILES
DISTRACTORS = [F[k] for k in W.DISTRACTORS]
DELIVERABLES = [W.GOLDEN["memo"], W.GOLDEN["table"]]


def rows_of(path):
    if path.endswith((".csv", ".txt")):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for line in fh if not line.startswith("#")) - (2 if path.endswith(".txt") else 1)
    return None


def write(target, out_path, counts=None):
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    rows = {f: rows_of(os.path.join(target, f)) for f in files}
    big = max((f for f in files if rows[f] is not None), key=lambda f: rows[f])
    meta = {
        "task": "task466",
        "architecture": 1,
        "title": "How much firm emergency capacity the Town of Quillfield should reserve on the Castlewick interconnect "
                 "for 2027, sized to the Varrow River's 50-year 7-day low flow fitted to the gauge's record and the "
                 "water works' reports; with the drought scenarios, the recurrence interval the block covers, and the "
                 "water the town's own system drew in each declared Stage 2 period",
        "domain": "General Statistics & Data Science",
        "subdomain": "data-integration-record-linkage-entity-resolution (two records of one river kept under different "
                     "observation mechanisms, a gauge's measured years and a water works' reports, conformed into one "
                     "annual low-flow record and one maximum-likelihood fit)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "13: scenarios and the flip point: the 10-, 25-, 50- and 100-year 7-day low flows with the "
                        "permitted withdrawal and the Stage 2 shortfall at each, the block and the recurrence interval "
                        "at which it stops covering, a chart, and two figures for each declared Stage 2 period",
        "as_of": W.AS_OF,
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["2027", "2012", "1894", "2024", "10", "25", "50", "100", "7-day", "Stage 2"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big, "largest_file_rows": rows[big]},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task466/generator/build.py (seeded, deterministic) in the layouts "
                       "of a state hydrologic survey's daily-values export and station description, a historical "
                       "society's transcription of a town water works' annual reports, a state board's guidance, "
                       "permit and regional report, a town's drought plan, notices, plant historian export, wholesale "
                       "meter reads, operator round sheets and meter register, a neighbouring city's offer letter and a "
                       "cooperative weather station's record; the state is unnamed and its town, river, city, mill, "
                       "agencies and people are fictional",
             "date": W.AS_OF,
             "license": "original work for this task; no third-party data"}],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta

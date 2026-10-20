"""metadata.json: the task's identity, its files, the distractors, the input gates and the sources."""
import json
import os

import world as W

F = W.FILES
DISTRACTORS = [F[k] for k in W.DISTRACTORS]
DELIVERABLES = [W.GOLDEN["csv"], W.GOLDEN["letter"]]


def rows_of(path):
    if path.endswith(".csv") or path.endswith(".txt"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path):
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    rows = {f: rows_of(os.path.join(target, f)) for f in files}
    big = max((f for f in files if rows[f] is not None), key=lambda f: rows[f])
    meta = {
        "task": W.TASK,
        "architecture": 1,
        "title": "Which of the 14 counties are high-range for the GHSO's FY2028 impaired driving task force grants "
                 "on their 2023 to 2025 alcohol-impaired-driving fatality rate, with each county's rate and deaths, "
                 "a chart against the 0.60 line, and each county's 2025 arrest and injury crash baselines",
        "domain": "General Statistics & Data Science",
        "subdomain": "data-integration-record-linkage-entity-resolution (a fatal crash census whose surviving drivers "
                     "are tested completely at three agencies and only after an arrest at the rest, integrated with "
                     "the toxicology laboratory's specimens, the crash records system's reports and the DOT's miles)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "01 with a threshold for a cap: each of the 14 counties' 2023 to 2025 rate and deaths against "
                        "the 0.60 line, the high-range list, the chart, and each county's three 2025 baselines",
        "as_of": W.AS_OF.isoformat(),
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["2023", "2025", "FY2028"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big, "largest_file_rows": rows[big]},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task473/generator/build.py (seeded, deterministic) in the layouts "
                       "of a state fatal crash census (FARS-style crash and person files under a 2011 and a 2024 "
                       "crash report form), a state toxicology laboratory's LIMS specimen export, a state crash "
                       "records system's injury crash report extract, a state DOT's HPMS county DVMT summaries, an "
                       "agency directory, a motor vehicle division's licensed driver counts, and a highway safety "
                       "office's grant guidelines; the state is unnamed and its counties, agencies, facilities and "
                       "people are fictional",
             "date": W.AS_OF.isoformat(),
             "license": "original work for this task; no third-party data"}],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta

"""metadata.json: the task's identity, its files, the distractors, the input gates and the sources."""
import json
import os

import world as W

F = W.FILES


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".txt"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 2
    return None


def write(target, out_path, counts=None):
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    rows = {f: rows_of(os.path.join(target, f)) for f in files}
    big = max((f for f in files if rows[f] is not None), key=lambda f: rows[f])
    meta = {
        "task": "task468",
        "architecture": 4,
        "title": "How many of Halbrook Community Health Plan's 14 network hospitals lose their 2027 Hospital Quality "
                 "Bonus on fiscal 2026 risk-adjusted 30-day mortality, and which; with each hospital's bonus at stake "
                 "(2 per cent of the plan's fiscal 2026 inpatient payments), the network total and a chart of the "
                 "mortality ratios against the 1.15 line",
        "domain": "Healthcare Delivery & Health Economics",
        "subdomain": "payment-claims-health-plan-analytics (a Medicaid plan's hospital mortality measure conformed from "
                     "its claims, a delegated medical group's encounters, enrollment, service lines, risk scores and "
                     "the state vital records office's death linkage)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "10: a scorecard: each of 14 hospitals' mortality ratio against the 1.15 bonus line, with the "
                        "count and the hospitals that lose it, beside each hospital's bonus at stake",
        "as_of": W.AS_OF,
        "deliverables": [W.GOLDEN["workbook"]],
        "distractor_files": [F[k] for k in W.DISTRACTORS],
        "stated_inputs": ["fiscal 2026", "2027", "1.15", "2 per cent"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big, "largest_file_rows": rows[big]},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task468/generator/build.py (seeded, deterministic) in the layouts "
                       "of a Medicaid managed care plan's inpatient claims extract (UB-04 type of bill and patient "
                       "status codes, MS-DRGs, ICD-10-CM), a delegated medical group's encounter submission file, an "
                       "enrollment extract, a member service-line extract, a state vital records office's death "
                       "linkage return, a plan's risk model scores, a network hospital list, a measure specification, "
                       "a linkage methods note, extract notes, a file layout, a quality dashboard and hospital "
                       "profiles; the state is unnamed and the plan, group, hospitals, members and people are "
                       "fictional",
             "date": W.AS_OF,
             "license": "original work for this task; no third-party data (MS-DRG and UB-04 code values are public "
                        "code sets used as labels)"}],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta

"""metadata.json: the task's identity, its files, the distractors, the input gates and the sources."""
import json
import os

import world as W

F = W.FILES


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path):
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    rows = {f: rows_of(os.path.join(target, f)) for f in files}
    big = max((f for f in files if rows[f] is not None), key=lambda f: rows[f])
    meta = {
        "task": "task468",
        "architecture": 2,
        "title": "How many clinical pharmacists each of Merrow Health Plan's nine specialty classes gets for the program "
                 "year from July 2026, one per $1.5 million of the spend its members on therapy on June 30, 2026 will "
                 "run over the year at the 2026 schedule, from two pharmacy benefit managers' specialty claim files; "
                 "with each class's managed spend and its 2025 manufacturer rebates",
        "domain": "Healthcare Delivery & Health Economics",
        "subdomain": "payment-claims-health-plan-analytics (two PBMs' specialty claims conformed and repriced; each "
                     "class's program-year spend for its members on therapy projected by months on therapy)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "05: allocation: each of nine classes gets its pharmacists from its projected managed spend, with "
                        "each class's managed spend and rebates",
        "as_of": W.AS_OF,
        "deliverables": [W.GOLDEN["workbook"]],
        "distractor_files": [F[k] for k in W.DISTRACTORS],
        "stated_inputs": ["July 2026", "2025"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big, "largest_file_rows": rows[big]},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task468/generator/build.py (seeded, deterministic) in the layouts "
                       "of two pharmacy benefit managers' specialty claim extracts, a health plan's member crosswalk, a "
                       "PBM's specialty drug list, price schedule and rebate statement, a specialty program charter, a "
                       "formulary bulletin, PBM transition notes, a PBM trend report and a medical-benefit summary; the "
                       "state is unnamed and the plan, PBMs, drugs and people are fictional",
             "date": W.AS_OF,
             "license": "original work for this task; no third-party data"}],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta

"""metadata.json: the task's identity, its files, the distractors, the input gates and the sources. It says what the
task decides and where the files come from, never how the answer is reached."""
import json
import os

import world as W

F = W.FILES
DISTRACTORS = [F[k] for k in W.DISTRACTORS]
DELIVERABLES = [W.GOLDEN["docx"], W.GOLDEN["xlsx"]]


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        import pyarrow.parquet as pq
        return pq.ParquetFile(path).metadata.num_rows
    return None


def write(target, out_path, counts=None):
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    rows = {f: rows_of(os.path.join(target, f)) for f in files}
    big = max((f for f in files if rows[f] is not None), key=lambda f: rows[f])
    meta = {
        "task": "task470",
        "architecture": 2,
        "title": "Where the 2027 vacant dwelling activation grant goes among the municipalities of a county pilot, "
                 "with each municipality's vacant dwellings and share, and two tables for the ministry's follow-up",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "census-register-administrative-data-quality",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "01: the municipalities against the regulation's threshold, each with its vacant dwellings and "
                        "share, beside two tables by municipality",
        "as_of": "2027-01-12",
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["2026", "2027"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big, "largest_file_rows": rows[big]},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task470/generator/build.py (seeded, deterministic) in the layouts "
                       "of a Norwegian cadastre unit extract, a meter data hub's metering point register and hourly "
                       "values, a population register extract and its event log, land register titles and transfers, "
                       "business and shareholder register extracts, a power exchange's day-ahead prices, a grid "
                       "company's outage log, a ministry regulation and a ministry letter; the county, the "
                       "municipalities, the organisations, the persons and the dwellings are fictional and personal "
                       "identifiers are pseudonymised",
             "date": "2027-01-12",
             "license": "original work for this task; no third-party data"}],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return meta

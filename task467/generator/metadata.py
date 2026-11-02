"""metadata.json: the task's identity, its files, the distractors, the input gates, the sources and each shipped file's
provenance (its source, date, what it covers and its rows; no file under target/ lists or describes the others)."""
import json
import os

import pyarrow.parquet as pq

import docs as DC
import world as W

F = W.FILES
DISTRACTORS = [F[k] for k in W.DISTRACTORS]
DELIVERABLES = [W.GOLDEN["memo"], W.GOLDEN["ledger"]]


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        return pq.ParquetFile(path).metadata.num_rows
    return None


def write(target, out_path, counts=None):
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    rows = {f: rows_of(os.path.join(target, f)) for f in files}
    big = max((f for f in files if rows[f] is not None), key=lambda f: rows[f])
    meta = {
        "task": "task467",
        "architecture": 1,
        "title": "What taxi pickup fee Velmont Airport Authority should set for 2027 under its cost-recovery by-law, "
                 "with 2025's fee-liable pickups restated to the forecourt rank that returns in 2027; with the surplus "
                 "at the fee and the shortfall 25 cents below it, a chart of the monthly pickups and drop-offs, and "
                 "each brokerage's monthly pickups and fees owed from January 2025 to August 2026",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "seasonal-adjustment-official-time-series-production (an airport authority's taxi pickup counts "
                     "conformed from a city regulator's trip records to budget next year's per-trip fee)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "07: grid of cells: each brokerage's fee-liable pickups and fees owed in each month from "
                        "January 2025 to August 2026 (six brokerages by twenty months), beside the 2027 fee with the "
                        "recorded and restated base year, the rank's share, the surplus and shortfall either side of "
                        "the fee and a chart",
        "as_of": W.AS_OF,
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["2027", "2025", "2023", "2026", "25 cents", "1 January"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big, "largest_file_rows": rows[big]},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task467/generator/build.py (seeded, deterministic) in the layouts "
                       "of a municipal vehicle-for-hire regulator's taxi trip records (annual files, monthly Parquet "
                       "drops, a daily origin-destination archive, zone, brokerage and affiliation registers), an "
                       "airport authority's fees by-law, finance policy, program budget, rank notice, passenger "
                       "statistics and ground access survey, and a transit agency's service bulletin; the "
                       "province is unnamed and the city, its airport, agencies, brokerages and people are fictional",
             "date": W.AS_OF,
             "license": "original work for this task; no third-party data"}],
        "provenance": [{"file": W.FILES[k], "source": src, "date": d, "covers": desc, "rows": rows[W.FILES[k]]}
                       for k, src, d, desc in DC.PROVENANCE],
    }
    assert sorted(r["file"] for r in meta["provenance"]) == files, "every shipped file has one provenance row"
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta

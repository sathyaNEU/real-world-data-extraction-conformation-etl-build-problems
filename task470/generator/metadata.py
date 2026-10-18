"""metadata.json: the task's identity, its files, the distractors, the input gates and the sources."""
import json
import os

import world as W

F = W.FILES
DISTRACTORS = [F[k] for k in W.DISTRACTORS]
DELIVERABLES = [W.GOLDEN["csv"], W.GOLDEN["memo"]]


def rows_of(path):
    if path.endswith(".csv") or path.endswith(".txt"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path, counts=None):
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    rows = {f: rows_of(os.path.join(target, f)) for f in files}
    big = max((f for f in files if rows[f] is not None), key=lambda f: rows[f])
    meta = {
        "task": "task470",
        "architecture": 1,
        "title": "How many of the Corrisan Valley's 24 public-use airfields without a control tower qualify for the "
                 "district's 2027 Unleaded Avgas Transition Grants, and which; with each field's 2026 lead from "
                 "piston-engine aircraft, a chart against the round's threshold, and the six towered fields' 2026 "
                 "piston operations and lead",
        "domain": "Physical & Environmental Sciences",
        "subdomain": "emissions-inventory (an airport lead inventory conformed from an ADS-B receiver network's "
                     "operations, the FAA aircraft register, tower counts, commissioned counts and a state based "
                     "aircraft list)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "01: a list of candidates against a cap: each of the 24 fields' 2026 lead against the round's "
                        "threshold, the count and the qualifying fields, beside the six towered fields' operations "
                        "and lead",
        "as_of": "2027-02-12",
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "wrong_basis_distractor": {
            "file": F[W.WRONG_BASIS],
            "basis": "the airport managers' 5010 estimates of annual operations for twelve months ending 2018 to "
                     "2025, all aircraft, not the 2026 operations of piston-engine aircraft",
            "ruled_out_by": "the file's own notes (operations are the manager's estimate for the twelve months ending "
                            "on the date shown) and method CVAQD-AQ-17 section 4, which takes operations from the "
                            "network and the counts"},
        "stated_inputs": ["2026", "2027"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big, "largest_file_rows": rows[big]},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task470/generator/build.py (seeded, deterministic) in the layouts "
                       "of an ADS-B airport operations counting export, the FAA releasable aircraft database "
                       "(MASTER, DEREG, ACFTREF, ENGINE; columns as the FAA publishes them, owner names and addresses "
                       "left out), FAA ATADS-style tower daily counts, consultants' operations count reports and "
                       "workbooks, a state based aircraft validation and airport directory, FAA Form 5010 airport "
                       "master record data, ambient lead monitoring samples, and an air district's inventory method, "
                       "grant guidelines and network notes; the state is unnamed and the district, fields, firms, "
                       "aircraft and people are fictional",
             "date": "2027-02-12",
             "license": "original work for this task; no third-party data"}],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta

"""metadata.json: the task's identity, its files, the distractors, the input gates and the sources."""
import json
import os

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
F = W.FILES
DISTRACTORS = [F[k] for k in W.DISTRACTORS]
DELIVERABLES = [W.GOLDEN["workbook"], W.GOLDEN["record"]]


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
        "architecture": 1,
        "title": "Which of Quillfield Re's five 2027 area-yield drought covers on the dryland grain sorghum yields of "
                 "Ardley, Corvin, Elster, Pallard and Tresham counties the Ardley Plains Growers' Cooperative should "
                 "buy under its risk policy, each judged on its expected loss over the crop years 1991 to 2025; with "
                 "each cover's 2027 liability and premium and the cooperative's 2016 to 2020 receipts from each county "
                 "as a share of its production",
        "domain": "General Statistics & Data Science",
        "subdomain": "data-integration-record-linkage-entity-resolution (each county's dryland sorghum yield history "
                     "conformed from a statistics service's county and district estimates in two downloads, the "
                     "withheld years recovered from the district totals)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "07: a grid of five county covers (expected loss, quoted rate as a multiple of it, the rate at "
                        "which the call changes, buy or decline), with each cover's liability and premium, each "
                        "county's receipts share, a chart of quoted rates against the rates at which the calls change "
                        "and the conformed county yield record",
        "as_of": W.AS_OF,
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["five", "2027", "Ardley", "Corvin", "Elster", "Pallard", "Tresham", "2016", "2020"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big, "largest_file_rows": rows[big]},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task465/generator/build.py (seeded, deterministic) in the layouts "
                       "of a state agricultural statistics service's county estimates database export and methods note, "
                       "a reinsurer's term sheet and quote schedule, a farmers' cooperative's risk policy, member "
                       "notice, portal export, elevator scale tickets, transfer log, member roster and prior cover "
                       "statements, and the drought monitor's county statistics; the state is unnamed and its counties, "
                       "the service's figures, the cooperative, the reinsurer and the people are fictional",
             "date": "2026-11-02",
             "license": "original work for this task; no third-party data"}],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta

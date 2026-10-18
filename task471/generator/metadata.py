"""metadata.json: the task's identity, its files, the distractors, the input gates and the sources."""
import json
import os

import world as W

F = W.FILES
DISTRACTORS = [F[k] for k in W.DISTRACTORS]
DELIVERABLES = [W.GOLDEN["csv"], W.GOLDEN["brief"]]


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
        "task": "task471",
        "architecture": 1,
        "title": "Which three markets the 2027 pitch for new nonstop service from Kessick Valley Regional should carry, "
                 "with every candidate market's 2026 trips from the service area parked at Brennick International "
                 "and the passengers those trips carried, the first market left out and the gap, and a chart",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "census-register-administrative-data-quality (a parking revenue control register of entries "
                     "completed by a card survey of the parked cars, conformed with a service-area ZIP list, a "
                     "city-market table and a regional airport's schedule)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "01: a ranked list under a cap: each of the 14 candidate markets' 2026 trips and passengers, "
                        "the three pitched, the first left out and the gap",
        "as_of": "2027-01-29",
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "wrong_basis_distractor": {
            "file": F[W.WRONG_BASIS],
            "basis": "Kessick Valley Regional's own passengers (a 10 per cent sample of tickets from KVR through the "
                     "airline hubs, first to third quarter 2026), not the service area's trips parked at Brennick "
                     "International",
            "ruled_out_by": "the Air Service Pitch Standard section 2.1, which makes the basis the trips the service "
                            "area makes by car to Brennick and parks in its long-stay lots to fly"},
        "stated_inputs": ["2026", "2027"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big, "largest_file_rows": rows[big]},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task471/generator/build.py (seeded, deterministic) in the layouts "
                       "of an airport parking revenue control system's daily entry extracts, a parking card survey's "
                       "keyed data, verbatims, handout log and methods report, a state aviation bureau's service-area "
                       "ZIP list, city-market table and route pitch standard, a regional airport's published "
                       "schedule, a parking rate card, a ground access survey workbook, and US DOT DB1B market and "
                       "T-100 segment layouts; the state is unnamed and the bureau, airports, contractor, airlines "
                       "and people are fictional",
             "date": "2027-01-29",
             "license": "original work for this task; no third-party data"}],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta

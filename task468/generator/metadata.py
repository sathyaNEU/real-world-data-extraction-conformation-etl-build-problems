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


def write(target, out_path):
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    rows = {f: rows_of(os.path.join(target, f)) for f in files}
    big = max((f for f in files if rows[f] is not None), key=lambda f: rows[f])
    meta = {
        "task": "task468",
        "architecture": 1,
        "title": "Which of Larkhaven Transit's eleven candidate routes the City should nominate to the state's Frequent "
                 "Transit Corridors Program for FY2027 (at most five), on the departures its buses made from the "
                 "routes' designated stops from January to June 2026 as two AVL systems recorded them, the departures "
                 "the trip matchers tied to no trip shared out through Service Quality's review weighted by its "
                 "design; with each candidate's outbound stops that had no shelter on June 30, 2026",
        "domain": "General Statistics & Data Science",
        "subdomain": "data-integration-record-linkage-entity-resolution (two AVL vendors' stop events conformed and "
                     "linked to the timetable's trips; the links the matchers missed, which fall on the late trunk "
                     "routes, propagated into each route's departures through a clerical review that samples bus-days "
                     "and takes one event from each)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "01: ranked list under a cap: each of eleven candidate routes passes or fails the delivered "
                        "frequency standard and the five with the most weekday boardings are nominated, with each "
                        "candidate's count of outbound stops without a shelter",
        "as_of": W.AS_OF,
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["FY2027", "January to June 2026", "April 5", "June 30, 2026"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big, "largest_file_rows": rows[big]},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task468/generator/build.py (seeded, deterministic) in the layouts "
                       "of a city transit department's CAD/AVL stop-event exports from two vendors, its GTFS feeds, "
                       "a service-quality review log and memo, a fleet roster, a candidate route list, ridership and "
                       "farebox reports, a Title VI monitoring report, a bus stop amenity inventory and a shelter "
                       "work-order log, and a state department of transportation's program guidance; the "
                       "state is unnamed and the city, its transit department, vendors, routes and people are "
                       "fictional",
             "date": W.AS_OF,
             "license": "original work for this task; no third-party data"}],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta

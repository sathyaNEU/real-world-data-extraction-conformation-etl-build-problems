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


def provenance():
    """Each shipped file: who provided it, its date and what it is (dataset-generation section 9). Nothing here says
    what a column means or how the files fit together."""
    C = W.CENTER_SHORT
    D = "%s, Transportation Planning Division" % W.DOT
    M = "Department of Revenue, Motor Vehicle Division"
    items = [
        ("guidelines", W.GHSO, "2027-02-09", "FY2028 County Impaired Driving Task Force Grants, program guidelines"),
        ("manual", C, "2024-03-15", "Fatal Crash Census reference manual, 2024 edition"),
        ("crash23", C, "2025-02-27", "Fatal Crash Census, 2023 crash file as closed (2011 report form)"),
        ("person23", C, "2025-02-27", "Fatal Crash Census, 2023 person file as closed (2011 report form)"),
        ("codes2011", C, "2025-02-27", "Fatal Crash Census, the 2011 report form's code table, exported with the "
                                       "2023 files"),
        ("crash2425", C, "2027-02-25", "Fatal Crash Census, 2024 and 2025 crash file as closed (2024 report form)"),
        ("person2425", C, "2027-02-25", "Fatal Crash Census, 2024 and 2025 person file as closed (2024 report form)"),
        ("prelim26", C, "2027-03-01", "Fatal Crash Census, 2026 preliminary crash file"),
        ("agencies", C, "2027-01-04", "Agency directory of the Fatal Crash Census and the Crash Records System, "
                                      "updated 4 January 2027"),
        ("vmt", D, "2027-01-30", "County daily vehicle miles traveled by functional class, 2023 to 2025, from the "
                                 "state's HPMS submissions; 2023 and 2024 final, 2025 final as of 30 January 2027"),
        ("court", W.AOC, "2027-03-02", "Criminal traffic cases opened in the county courts, 1 January 2025 to 28 "
                                       "February 2027, with dispositions as recorded on 28 February 2027; a "
                                       "statistical extract prepared for the %s, without party identifiers" %
                                       W.CENTER_SHORT),
        ("licensed", M, "2026-01-15", "Licensed drivers by county of residence, 31 December 2025, from the driver "
                                      "license file"),
    ]
    assert sorted(k for k, _, _, _ in items) == sorted(W.FILES), "every shipped file has its provenance"
    return [{"file": W.FILES[k], "provided_by": who, "date": d, "is": what} for k, who, d, what in items]


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
                 "a chart against the 0.60 line, and each county's 2025 impaired-driving prosecution baseline",
        "domain": "General Statistics & Data Science",
        "subdomain": "data-integration-record-linkage-entity-resolution (the FY2028 high-range county designation "
                     "for the GHSO's impaired driving task force grants, and the task force applications' 2025 "
                     "baselines)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "01 with a threshold for a cap: each of the 14 counties' 2023 to 2025 rate and deaths against "
                        "the 0.60 line, the high-range list, the chart, and each county's 2025 prosecution baseline",
        "as_of": W.AS_OF.isoformat(),
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["2023", "2025", "FY2028"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big, "largest_file_rows": rows[big]},
        "provenance": provenance(),
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task473/generator/build.py (seeded, deterministic) in the layouts "
                       "of a state fatal crash census (FARS-style crash and person files under a 2011 and a 2024 "
                       "crash report form), a state DOT's HPMS county DVMT summaries, an agency directory, a state "
                       "court administrator's statistical extract of criminal traffic cases, a motor vehicle "
                       "division's licensed driver counts, and a highway safety office's grant guidelines; the state "
                       "is unnamed and its counties, agencies, courts and people are fictional",
             "date": W.AS_OF.isoformat(),
             "license": "original work for this task; no third-party data"}],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta

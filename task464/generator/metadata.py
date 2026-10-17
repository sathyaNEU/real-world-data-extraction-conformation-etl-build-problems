"""metadata.json: the task's identity, its files, the distractors, the input gates and the sources."""
import json
import os

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
F = W.FILES
DISTRACTORS = [F[k] for k in W.DISTRACTORS]
DELIVERABLES = [W.GOLDEN["workbook"], W.GOLDEN["table"]]


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
        "task": "task464",
        "architecture": 2,
        "title": "Which six of the fourteen districts that applied for the 2027 Adolescent Literacy Partnership grants "
                 "the State Board should fund, counted on the grade 9 and 10 students at Level 1 of the new state "
                 "reading test, the grade 10 students' retiring-test scores placed on the new scale through the spring "
                 "2026 bridge study; with each applicant's grade 7 students at Level 1 in spring 2026 and their share",
        "domain": "Education & Learning Sciences",
        "subdomain": "item-response-theory-test-equating (a retiring state reading test's 2025 grade 8 scores placed "
                     "on the new test's scale through a single-group bridge study, into one conformed file of grade 8 "
                     "reading levels)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "01: a ranked list under a cap: the six of fourteen applicants funded, every applicant's "
                        "students at Level 1, the first district left out and its gap, a chart, two figures per "
                        "applicant beside the call and the conformed file",
        "as_of": W.AS_OF,
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["2027", "2026", "2025", "six", "fourteen", "Level 1", "October 1"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big, "largest_file_rows": rows[big]},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task464/generator/build.py (seeded, deterministic) in the layouts "
                       "of a state department of education's records: two assessment vendors' student result files "
                       "and guides, a test-taker crosswalk, a bridge study's paired scores and memorandum, an October "
                       "enrolment collection, a district and school directory, a nonpublic schools registry, a state "
                       "board resolution, grant rules and two neighbouring state files; the state is unnamed and its "
                       "districts, schools, vendors and people are fictional",
             "date": W.AS_OF,
             "license": "original work for this task; no third-party data"}],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta

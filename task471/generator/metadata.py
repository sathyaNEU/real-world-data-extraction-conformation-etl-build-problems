"""metadata.json: the task's identity, its files, the distractors, the input gates and the sources."""
import json
import os

import pack as P
import world as W

F = P.FILES
DISTRACTORS = ["framework", "adminsum"]


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path, deliverables):
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    rows = {f: rows_of(os.path.join(target, f)) for f in files}
    big = max((f for f in files if rows[f] is not None), key=lambda f: rows[f])
    meta = {
        "task": "task471",
        "architecture": 2,
        "title": "Which of the state's sixteen educator preparation programs fall below the 70 per cent first-attempt "
                 "pass rate on the June 2026 Elementary Literacy Instruction test for their 2025-26 completers, and so "
                 "go to formal review in 2027; with the 2026 form's raw passing score, each program's completers, "
                 "first-attempt passers and rate, each program's 2024-25 completers tested by June 2025 and their "
                 "first-attempt pass rate, and a chart of the 2026 rates against the line",
        "domain": "Education & Learning Sciences",
        "subdomain": "item-response-theory-test-equating (a licensing board conforms two scoring contractors' results, "
                     "its attempt history and sixteen programs' completer lists onto the 2025 reporting scale, "
                     "equating the 2026 form to the 2025 form through a mixed-format anchor)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "10: a scorecard: each of 16 programs' first-attempt pass rate against the 70 per cent review "
                        "line, with the programs that go to review, beside each program's prior-year rate",
        "as_of": W.AS_OF.isoformat(),
        "deliverables": deliverables,
        "distractor_files": [F[k] for k in DISTRACTORS],
        "stated_inputs": ["2025-26", "2027", "70 per cent", "June 2026", "June 2025", "2024-25"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big, "largest_file_rows": rows[big]},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task471/generator/build.py (seeded, deterministic) in the layouts "
                       "of a state licensure test program's records: two scoring contractors' candidate score files, "
                       "an item response file, a constructed-response scoring read export with validity papers, a "
                       "scoring statistics workbook, item maps, a raw-to-scale conversion, a licensing system's "
                       "attempt history and registration crosswalk, a completer register, programs' Title II completer "
                       "lists, a program directory, a technical report, an assembly memo, a program review rule, a "
                       "test framework and an administration summary; the state is unnamed and the board, contractors, "
                       "programs, candidates and people are fictional",
             "date": W.AS_OF.isoformat(),
             "license": "original work for this task; no third-party data"}],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta

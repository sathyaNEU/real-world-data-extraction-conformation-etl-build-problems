"""metadata.json: the task's identity, its files, the distractors, the input gates and the sources."""
import json
import os

import pack as P
import world as W

F = P.FILES


def write(target, out_path, deliverables, n=None):
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    rows = {P.FILES[k]: v for k, v in (n or {}).items()}
    big = max(rows, key=lambda f: rows[f]) if rows else None
    meta = {
        "task": "task471",
        "architecture": 4,
        "title": "Which of the 24 municipalities whose register held 4,500 to 6,000 residents at the start of 1 January "
                 "2026 qualify for the 2027 small-municipality supplement, an adjusted resident population below "
                 "5,000 (the register count less the registered persons the Register Coverage Audit 2026 estimates "
                 "were not living there); with each municipality's departures abroad and deaths in 2025 and a chart "
                 "of the adjusted resident populations against the line",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "census-register-administrative-data-quality (a national statistics bureau applies a coverage "
                     "audit of the population register to each municipality's register count, conformed from the "
                     "register extract, its event history, the audit's sample, visits and histories and the "
                     "deregistration hub's log into the ministry's delivery file)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "10: a scorecard: each of the 24 municipalities' adjusted resident population against the "
                        "5,000 line, with each municipality's departures abroad and deaths in 2025",
        "as_of": W.AS_OF.isoformat(),
        "deliverables": deliverables,
        "distractor_files": [F[k] for k in P.DISTRACTORS],
        "stated_inputs": ["1 January 2026", "4,500", "6,000", "5,000", "2027", "2025"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big,
                        "largest_file_rows": rows.get(big)},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task471/generator/build.py (seeded, deterministic) in the layouts "
                       "of a national population register's statistical extracts: the register extract with its "
                       "trailer, the event history, a coverage audit's sample, fieldwork visits and sampled persons' "
                       "histories, the deregistration hub's 2025 log and acknowledgements, the municipalities' "
                       "non-resident records, a regulation article, the audit report, the record layouts, the "
                       "ministry's delivery specification, a municipality code workbook, a country code list, a 2024 "
                       "pilot workbook and a waste levy billing extract; the country is unnamed and the bureau, "
                       "ministry, municipalities, persons and people named are fictional",
             "date": W.AS_OF.isoformat(),
             "license": "original work for this task; no third-party data"}],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta

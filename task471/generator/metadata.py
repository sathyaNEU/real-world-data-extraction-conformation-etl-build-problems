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
        "architecture": 5,
        "title": "How many of the Electoral Commission's organisers for its 2027 enrolment campaign each region "
                 "gets, in proportion to its adults not on the roll on census day, 4 March 2025; with each "
                 "region's people added to the roll who had not been on it on census day and electors removed because "
                 "they had died, from census day to 30 June 2026, and a bar chart of the organisers",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "census-register-administrative-data-quality (the enrolment-gap file a national statistics "
                     "office prepares for its electoral commission)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "05: an allocation to a fixed total: the campaign's organisers shared among the regions, with each "
                        "region's new electors and removals because of death since census day",
        "as_of": W.AS_OF.isoformat(),
        "deliverables": deliverables,
        "distractor_files": [F[k] for k in P.DISTRACTORS],
        "wrong_basis_distractor": {
            "file": F["estimates_2024"],
            "basis": "the Office's 2018-base population estimates at 30 June 2024, eight months before census day, by "
                     "five-year-and-wider age groups that do not separate the adults",
            "ruled_out_by": "the plan's section 2.1: the adults usually resident in the region on census day, 4 March 2025"},
        "stated_inputs": ["4 March 2025", "30 June 2026", "2027"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big,
                        "largest_file_rows": rows.get(big)},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task471/generator/build.py (seeded, deterministic) in the layouts "
                       "of a national statistics office's census outputs (a workbook of usual residents by region, sex "
                       "and single year of age), its post-enumeration survey's person files, sampled meshblocks and "
                       "methods report, the vital and border series by year of birth with their notes, an electoral "
                       "commission's roll at census day by electorate, its electorate concordance, its roll at the 2023 "
                       "general election by electorate, its roll transaction "
                       "log with its code list and platform migration notes, its campaign field plan, the office's "
                       "file specification, earlier population estimates and a census field operations summary; the "
                       "country is unnamed and the office, commission, regions, electorates and people named are "
                       "fictional",
             "date": W.AS_OF.isoformat(),
             "license": "original work for this task; no third-party data"}],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta

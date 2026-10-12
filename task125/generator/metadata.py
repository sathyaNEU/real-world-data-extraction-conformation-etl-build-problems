"""Write task125/metadata.json from the built pack."""
import json
import os
import sys

import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    "person": "Household Labour Survey person-quarter analysis file, January to March 2023 to July to September 2026",
    "calls": "Call records for addresses issued for a first interview, intakes January to March 2024 to July to September 2026",
    "register": "Addresses issued for a first interview, same intakes",
    "controls": "Population controls by region and by age group and sex, 2023 to 2027",
    "release": "Release tables for April to June 2026",
    "claimants": "Jobseeker Support claimants by region and month, January 2023 to September 2026",
    "staffing": "Field interviewers by region, October 2026",
    "methods": "HLS methods note, 2025 edition",
    "fi_2026": "Field instruction FI-2026/07, first-interview visits from 1 July 2026",
    "fi_2024": "Field instruction FI-2024/03, call pattern for first interviews (superseded)",
    "dictionary": "HLS analysis files data dictionary",
    "notes": "Survey Data Office extract notes, 20 October 2026",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        return int(pq.ParquetFile(path).metadata.num_rows)
    return None


def write(target, out_path):
    files = []
    for k, f in B.FILES.items():
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[k], "date": "2026-10-20",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    files.sort(key=lambda x: x["path"])
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task125",
        "title": "How much of the July to September 2026 rise in the Household Labour Survey's unemployment rate is the "
                 "labour market, and how far the first-interview visit cap will hold the published unemployment and "
                 "employment rates off the six-visit rates in each quarter to September 2027",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "anomaly detection in official statistics (a fieldwork protocol change in a rotating-panel labour "
                     "force survey separated from the labour market)",
        "objective": "Anomaly Detection & Diagnostics",
        "prompt_shape": "02 (forecast across periods): the gap in the published unemployment and employment rates in "
                        "each quarter from July to September 2026 to July to September 2027, with the July to September "
                        "split, and three regional measures",
        "as_of": "2026-10-20",
        "deliverables": ["hls_visit_limit_note_2026q3.docx", "hls_visit_limit_path_2027.xlsx"],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task125/generator/build.py (seeded, deterministic) around a "
                               "fictional country's statistics office, its household labour survey, regions and staff; "
                               "no real survey, office, person or record is depicted.",
                     "date": "2026-10-20", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-20",
        "generator": "task125/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))

"""Write task128/metadata.json from the built pack."""
import json
import os
import sys

import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs as DC   # noqa: E402
import pack as P    # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    P.FILES["lists"]: "dialler list export, five 30-day campaigns, list days January 2025 to September 2026",
    P.FILES["calls"]: "dialler call detail, 30-day and QA campaigns, July 2025 to June 2026",
    P.FILES["history"]: "card platform delinquency history by cycle date from each 30-day entry",
    P.FILES["worklog"]: "workforce and dialler log by team and working day",
    P.FILES["arrangements"]: "arrangement system extract, arrangements set up by the 30-day teams",
    P.FILES["rates"]: "treasury daily USD/CAD booking rates",
    P.FILES["ls60"]: "60-day campaign daily list summary by centre",
    P.FILES["headcount"]: "collections workforce headcount by centre and quarter",
    DC.PROTOCOL: "early-stage collections protocol, cards, version 7.2",
    DC.POLICY: "credit policy chapter CP-14, collections resourcing",
    DC.BUDGET: "2027 collections budget request",
    DC.FIELDS: "field reference for the collections extracts",
    DC.MANIFEST: "Collections MI extract register, 9 October 2026",
}


def rows_of(path):
    if path.endswith((".csv", ".txt")):
        with open(path, encoding="utf-8", errors="replace") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        return int(pq.ParquetFile(path).metadata.num_rows)
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2026-10-09",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task128",
        "title": "Which of a Canadian bank's five early-stage collections centres, if any, gets its one new 2027 team, "
                 "sized on the rolls to 90 days past due the new team's calls would have prevented on the July 2025 to "
                 "June 2026 lists",
        "domain": "Banking, Credit & Financial Risk",
        "subdomain": "collections and recovery (capacity funding from a natural experiment in the dialler's overflow)",
        "objective": "Opportunity Sizing & Decision Support",
        "prompt_shape": "01 (ranked list under a cap): five centres sized against one funding line, none on the same footing",
        "as_of": "2026-10-09",
        "deliverables": ["centre_call_effects_2025_2026.csv", "centre_call_effects_2025_2026.png",
                         "sixth_team_decision_2027.docx"],
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task128/generator/build.py (seeded, deterministic) around "
                               "a fictional bank and its collections operation; no real bank, person or account is "
                               "depicted.",
                     "date": "2026-10-09", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-09",
        "generator": "task128/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))

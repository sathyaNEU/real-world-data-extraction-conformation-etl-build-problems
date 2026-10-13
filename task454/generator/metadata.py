"""Write task454/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W    # noqa: E402

TASK = os.path.dirname(HERE)
F = W.FILES
SOURCES = {
    F["claims"]: "the administrator's extract of the Program's fee-for-service pharmacy claims for the twelve candidate classes, fills April 2026 to March 2027, paid through 20 April 2027",
    F["aac"]: "the State AAC rates in effect from April 2026 to March 2027, as published to 1 April 2027",
    F["drugs"]: "the Department's drug file as of 15 April 2027",
    F["classes"]: "the Department's drug class list in force from 1 January 2027",
    F["summary"]: "the administrator's FY2026 generic utilization summary of 24 April 2026",
    F["terms"]: "Attachment C of the pharmacy benefit administration contract, as amended effective 1 July 2026",
    F["method"]: "the survey contractor's State AAC methodology, revised January 2026",
    F["request"]: "the Department's letter of 8 March 2027 naming the candidate classes",
    F["dict"]: "the administrator's record layout for the extract",
    F["trans"]: "the administrator's data delivery note of 21 April 2027",
    F["mco"]: "the managed care plans' pharmacy encounter summary by class and quarter",
    F["pdl"]: "the Department's preferred drug list status as of January 2027",
}


def rows_of(path):
    if path.endswith((".csv", ".txt")):
        with open(path, encoding="utf-8", errors="replace") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2027-04-21",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task454",
        "architecture": 1,
        "title": "Which drug class a state Medicaid program's pharmacy benefit administrator proposes for the State "
                 "maximum allowable cost list, ranked on each class's ingredient spread, when the State's acquisition "
                 "cost survey prices only the NDCs its sampled community pharmacies buy",
        "domain": "General Statistics & Data Science",
        "subdomain": "data-integration-record-linkage-entity-resolution (pharmacy claims integrated with an acquisition "
                     "cost survey that covers only part of the NDCs dispensed, with a drug file and a class list)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "07: a grid of the twelve candidate classes, each with its ingredient spread and, for the prior "
                        "year, its claims, units dispensed and ingredient cost paid",
        "as_of": "2027-04-21",
        "deliverables": list(W.DELIVERABLES),
        "distractor_files": [F[k] for k in W.DISTRACTORS],
        "stated_inputs": [],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task454/generator/build.py (seeded, deterministic) in the "
                               "layouts of a Medicaid fee-for-service pharmacy claims extract, a state acquisition cost "
                               "rate file, a state drug file and class list, and an administrator's utilization summary; "
                               "the state, its agencies, the administrator, the labelers, pharmacies and people are "
                               "fictional.",
                     "date": "2027-04-21", "license": "CC0-1.0 (original work)"}],
        "created": "2027-04-21",
        "generator": "task454/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))

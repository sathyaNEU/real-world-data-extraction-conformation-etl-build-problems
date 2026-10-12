"""Write task184/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    "lanes": "Lane sensor feed, eight central checkpoints, 15 June to 31 August 2026",
    "queue": "Queue-camera queue times, eight central checkpoints, 15 June to 31 August 2026",
    "roster26": "Summer 2026 roster patterns, lanes planned by 15 minutes",
    "roster27": "Summer 2027 roster pattern from the airports' rostering tool, lanes planned by 15 minutes",
    "planning": "Capacity Planning's summer 2027 planning sheet (design days)",
    "postings": "Mobile screening unit postings, summer 2026",
    "register": "Central checkpoint lane register",
    "returns": "Airport operators' monthly traffic returns, 2026",
    "hotels": "Payables lines, cost centre CC-4109, hotel invoices and credit notes, summer 2026",
    "claims": "Expense claims export, cost centre CC-4109, claims approved June to October 2026",
    "faults": "Lane fault log, 2026",
    "feedback": "Passenger feedback about security, summer 2026",
    "standard26": "Checkpoint planning standard KAS-STD-07, 2026 edition",
    "standard23": "Checkpoint planning standard KAS-STD-07, 2023 edition (superseded)",
    "policy": "Mobile screening unit deployment policy 2027",
    "notes": "Capacity Planning extract notes, 23 April 2027",
    "flags": "Throughput detector run, spring 2027",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path):
    files = []
    for k, f in B.FILES.items():
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[k], "date": "2027-04-23",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    files.sort(key=lambda x: x["path"])
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task184",
        "title": "Where the mobile screening unit should be posted for 15 June to 31 August 2027 among the eight "
                 "airports the throughput detector flagged, how many passengers it would move within the 20-minute "
                 "wait standard at each in each period, and how far the chosen airport's forecast can fall before "
                 "another posting moves more",
        "domain": "Urban & Regional Science (house domain Supply Chain & Logistics)",
        "subdomain": "aviation passenger screening operations (checkpoint capacity and the posting of a mobile "
                     "screening unit after a throughput detector's spring flags)",
        "objective": "Anomaly Detection & Diagnostics",
        "prompt_shape": "13 (scenarios and the flip point): each airport's posting in each 2027 period, the call, the "
                        "flip, and three 2026 measures per airport",
        "as_of": "2027-04-23",
        "deliverables": ["mobile_team_posting_summer_2027.pdf", "mobile_team_effect_2027.xlsx"],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task184/generator/build.py (seeded, deterministic) "
                               "around a fictional country's aviation screening agency, its airports, staff and "
                               "suppliers; no real agency, airport, hotel, person or record is depicted.",
                     "date": "2027-04-23", "license": "CC0-1.0 (original work)"}],
        "created": "2027-04-23",
        "generator": "task184/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))

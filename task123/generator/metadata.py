"""Write task123/metadata.json from the built pack."""
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
    P.FILES["kvg_bills"]: "Kestrel Valley Gas residential (RS-1) billing transactions, reads 1 October 2025 to 14 April 2026",
    P.FILES["kvg_gs"]: "Kestrel Valley Gas general service billing transactions, same reads",
    P.FILES["kvg_orders"]: "Kestrel Valley Gas residential service orders, activity 1 December 2025 to 3 February 2026",
    P.FILES["northline"]: "Northline Utility Services job report, Kestrel Valley collections batch, 5 to 16 January 2026",
    P.FILES["kvg_wcp"]: "Kestrel Valley Gas Winter Care Plan enrollments",
    P.FILES["nng_reads"]: "Northbank Natural Gas R1 bimonthly reads and billed usage (fixed width)",
    P.FILES["nng_activity"]: "Northbank Natural Gas residential field activity, December 2025 to February 2026",
    P.FILES["nng_crew"]: "Northbank Natural Gas crew completions for the field activity",
    P.FILES["nng_accounts"]: "Northbank Natural Gas R1 account history by premise",
    P.FILES["nng_flags"]: "Northbank Natural Gas HHAP premises at 31 January 2026",
    P.FILES["nng_sched"]: "Northbank Natural Gas 2026-27 meter reading schedule",
    P.FILES["phe_bills"]: "Pine Harbor Energy residential bills, cycle and calendar-month",
    P.FILES["phe_mdms"]: "Pine Harbor Energy MDMS daily reads of residential AMI meters",
    P.FILES["phe_meters"]: "Pine Harbor Energy meter and account history",
    P.FILES["phe_wo"]: "Pine Harbor Energy residential work orders, December 2025 to February 2026",
    P.FILES["phe_events"]: "Pine Harbor Energy head-end meter events, December 2025 to February 2026",
    P.FILES["phe_plans"]: "Pine Harbor Energy payment arrangements on residential accounts",
    P.FILES["service_points"]: "Service points of the three utilities in the twelve northern counties",
    DC.STANDARD: "County Energy Data Standard for Home Energy Assistance, Edition 3",
    DC.NOTES: "Ridgeline Home Energy Fund data notes on the April 2026 utility extracts",
    DC.THREAD: "Planning thread, 20 April 2026",
    DC.MANIFEST: "Export manifest, 20 April 2026",
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
                      "source": "Constructed: " + SOURCES[f], "date": "2026-04-20",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task123",
        "title": "How much of the $18,640,000 Northern Heat Assistance Grant for winter 2026-27 each of the northern "
                 "region's twelve counties should receive, in proportion to its residential natural gas use in "
                 "January 2026",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "seasonal adjustment and official time-series production (a calendar-month county series built "
                     "from billing-period returns)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "05 (allocation to a fixed total): twelve county awards, with each county's January 2026 "
                        "residential therms and two assistance indicators",
        "as_of": "2026-04-20",
        "deliverables": ["jan2026_county_gas_series.csv", "heating_grant_split_2026_27.xlsx",
                         "heating_grant_split_2026_27.png"],
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task123/generator/build.py (seeded, deterministic) around "
                               "a fictional nonprofit, three fictional gas utilities, their contractor and a fictional "
                               "twelve-county region; no real utility, agency, person or record is depicted.",
                     "date": "2026-04-20", "license": "CC0-1.0 (original work)"}],
        "created": "2026-04-20",
        "generator": "task123/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))

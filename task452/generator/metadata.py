"""Write task452/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack as P    # noqa: E402
from golden import schedule    # noqa: E402  (Schedule 1's allocations, figures the pack states as inputs)

TASK = os.path.dirname(HERE)
SOURCES = {
    P.FILES["wq"]: "the commission's water quality results export (both sampling organisations), 8 January 2027",
    P.FILES["uv"]: "the gage contractor's approved 15-minute discharge for water year 2026, delivered 14 December 2026",
    P.FILES["dv"]: "the gage contractor's approved daily mean discharge for water years 2024 and 2025",
    P.FILES["prov"]: "the gage contractor's provisional 15-minute discharge for July to September 2026, delivered 6 October 2026",
    P.FILES["register"]: "the commission's station register: compliance stations, joining streams and permitted outfalls",
    P.FILES["agreement"]: "the Brannoch Lake Phosphorus Agreement, consolidated text with Schedule 1 allocations",
    P.FILES["program"]: "the commission's description of its tributary monitoring program",
    P.FILES["transmittal"]: "the gage contractor's data transmittal of 14 December 2026",
    P.FILES["dmr"]: "the permitted facilities' discharge monitoring reports for phosphorus and flow, water year 2026",
    P.FILES["contracts"]: "the farm practice program's cover crop contracts, crop years 2024 to 2027, with amendments",
    P.FILES["fields"]: "the farm practice program's mapping of each contracted field's acres among watersheds",
    P.FILES["precip"]: "the commission's weather stations' daily precipitation, water years 2024 to 2026",
    P.FILES["lake"]: "the commission's open-water lake monitoring, May to October 2024 to 2026",
}


def rows_of(path):
    if path.endswith((".csv", ".txt")):
        with open(path, encoding="utf-8", errors="replace") as fh:
            return sum(1 for line in fh if not line.startswith("#")) - 1
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2027-01-12",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task452",
        "architecture": 1,
        "title": "Where a lake commission puts its three 2027 tributary restoration projects: each tributary's water-year "
                 "2026 total phosphorus load, estimated from monthly and storm grab samples and the 15-minute discharge "
                 "record, against its allocation",
        "domain": "Physical & Environmental Sciences",
        "subdomain": "emissions-inventory (a lake basin's waterborne phosphorus load inventory: laboratory results, "
                     "15-minute discharge and the station register conformed into each tributary's water-year load)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "01: a ranked slate of three tributaries under the fund's cap, with each tributary's load against "
                        "its allocation, its upstream permitted wastewater phosphorus and its cover crop acres",
        "as_of": "2027-01-12",
        "deliverables": ["restoration_slate_2027.docx", "tributary_loads_wy2026.csv"],
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "stated_inputs": ["{:,}".format(int(v)) for v in schedule(target).values()],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task452/generator/build.py (seeded, deterministic) in the "
                               "layouts of a water quality exchange results export, a hydrometric contractor's unit and "
                               "daily value files, NPDES discharge monitoring reports and a conservation program's "
                               "contract records; the lake, its commission, the tributaries, facilities and farms are "
                               "fictional.",
                     "date": "2027-01-12", "license": "CC0-1.0 (original work)"}],
        "created": "2027-01-12",
        "generator": "task452/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))

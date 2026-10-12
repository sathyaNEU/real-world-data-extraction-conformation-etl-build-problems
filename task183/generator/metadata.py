"""Write task183/metadata.json from the built pack."""
import json
import os
import sys

import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    "wo": "Work management system: cable fault work orders on the district's underground primary sections, January 2012 to 30 September 2026",
    "register": "GIS export: underground primary cable sections of the eight feeders, in service and retired, as of 30 September 2026",
    "codes": "Work order cause and repair codes and GIS status codes",
    "oms": "Outage management export (legacy OMS to 17 March 2026, ADMS after): one row per outage per feeder, October 2020 to September 2026",
    "steps": "Outage management restoration steps for the same outages",
    "conn": "Network connectivity model: metered points to transformers, protective devices and feeders, dated rows",
    "devices": "Network model protective device hierarchy: substations, banks, breakers, automated switches, fuses",
    "cis": "Customer information system: active service accounts at 30 September 2026",
    "med": "Published major event days, reliability years 2021 to 2025",
    "standard": "Reliability reporting standard TVE-RS-04 revision 6",
    "report": "2025 annual reliability report, section 6 (underground cable)",
    "notes": "Asset analytics hand-off note for the extract: where each file came from and what to know reading it",
    "vaults": "Manhole and vault inspection records, 2022 to 2026",
    "loading": "SCADA feeder monthly peak loading, 2021 to 2026",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="latin-1") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        return int(pq.ParquetFile(path).metadata.num_rows)
    return None


def write(target, out_path):
    files = []
    for k, f in B.FILES.items():
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[k], "date": "2026-10-06",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    files.sort(key=lambda x: x["path"])
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task183",
        "title": "The underground feeder for a 2027 cable program, with each feeder's RY2026 reliability indices",
        "domain": "Energy Systems & Utilities",
        "subdomain": "grid reliability and outage analysis (underground distribution cable failures and feeder "
                     "reliability indices at a Pennsylvania electric utility)",
        "objective": "Anomaly Detection & Diagnostics",
        "prompt_shape": "01 (ranked list under a cap): the one feeder for the 2027 program, with every feeder's "
                        "SAIFI, SAIDI and multiple-interruption count",
        "as_of": "2026-10-06",
        "deliverables": ["cable_program_2027.xlsx", "feeder_failures_2027.png"],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task183/generator/build.py (seeded, deterministic) around "
                               "a fictional electric utility (Tamsin Valley Electric), its fictional substations, "
                               "feeders, customers and places in Pennsylvania; no real utility, person, account or "
                               "asset is depicted.",
                     "date": "2026-10-06", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-11",
        "generator": "task183/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))

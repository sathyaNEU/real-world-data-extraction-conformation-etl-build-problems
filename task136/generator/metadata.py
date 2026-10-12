"""Write task136/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    K.REGISTER: "Mirrabee Energy embedded generation connection register: micro EG applications (new systems and "
                "alterations, all statuses) for NMIs on the Yarrabin feeders, received to 31 August 2026",
    K.LEGACY: "Inverters of applications migrated from the pre-July-2019 connections system",
    K.NETWORK: "Network model extract: NMIs on the eight Yarrabin 22 kV feeders at 31 August 2026",
    K.XREF: "GIS cross-reference of NMIs to Merindah City Council property numbers",
    K.RATES: "Merindah City Council 2026-27 rates roll, western rating area",
    K.PROGRAM_LOG: "Merindah City Council Solar Streets campaign summary, 2018 to 2024, with the program terms",
    K.LETTER: "Merindah City Council letter of 14 August 2026 confirming the two spring 2027 campaigns",
    K.NPP: "Mirrabee Energy Network Planning Procedure NPP-114 revision 3 (micro EG forecasting for augmentation)",
    K.HCA: "Hosting capacity assessment BPE-2026-031 for the Yarrabin 22 kV feeders",
    K.DER: "DER Register extract (AC connections and devices) for NMIs on the Yarrabin feeders, 5 September 2026",
    K.REALLOC: "NMI re-allocation log for Yarrabin premises since 1 July 2019",
    K.DICTIONARY: "Data dictionary for the extracts",
    K.MANIFEST: "Export manifest: each file's source system, date, rows, owner and scope",
    K.PEAK: "Feeder summer peak demand forecast 2027 to 2031 (Distribution Annual Planning Report working file)",
    K.REBATE: "Queensland home battery rebate approvals for Merindah addresses, FY2025-26",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2026-10-12",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task136",
        "title": "Which Yarrabin feeder gets Mirrabee Energy's FY2027-28 hosting-capacity augmentation",
        "domain": "Energy Systems & Utilities",
        "subdomain": "load-forecasting (rooftop PV forecast to an augmentation's design point, with two council "
                     "solar bulk-buy campaigns, at a Queensland distribution network)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "other: the feeder, its rooftop PV above hosting capacity, the runner-up and gap, each 2027 "
                        "bulk-buy's systems, the chart, and two per-feeder asks (a DER Register reconciliation and "
                        "battery storage)",
        "as_of": "2026-10-12",
        "deliverables": [K.GOLD_BOOK, K.GOLD_CHART],
        "distractor_files": list(K.DISTRACTORS),
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task136/generator/build.py (seeded, deterministic) around "
                               "a fictional Queensland distributor (Mirrabee Energy), council (Merindah City Council), "
                               "suburbs, consultants and people; no real organisation, person, property or meter is "
                               "depicted. Product names in the DER Register extract are generic market models.",
                     "date": "2026-10-12", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-12",
        "generator": "task136/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))

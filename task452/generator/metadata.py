"""Write task452/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack as P    # noqa: E402

TASK = os.path.dirname(HERE)
F = P.FILES
SOURCES = {
    F["main"]: "the main interpretation campaign of the 2024-2025 reference sample, February and March 2026",
    F["qc"]: "the ministry's quality-control re-interpretation of one reference point in five, March and April 2026",
    F["adj"]: "the adjudication log of the quality-control differences, April 2026",
    F["intersect"]: "each reference point's class on the final change map version 2.0",
    F["stats"]: "the class areas of the final change map version 2.0 by 2025 district",
    F["poly"]: "the deforestation polygons of the final change map version 2.0, delivered by 10 km tile",
    F["conc"]: "the district concordance between the 2019 and 2025 district layers",
    F["dict"]: "the field descriptions of the reference, map and lookup files",
    F["manifest"]: "the export manifest of 22 May 2026",
    F["design"]: "the reference sample design of 26 January 2026",
    F["erpa"]: "the emission reductions payment agreement, articles 1 to 9",
    F["plan"]: "the program's monitoring plan, sections 3 and 4",
    F["frel"]: "the forest reference level 2015-2022 summary",
    F["release"]: "the release note of the final change map version 2.0",
    F["nfi"]: "the national forest inventory's tree measurements, 2018-2022",
    F["fire"]: "the fire hotspot detections, 2024-2025",
}
DISTRACTORS = [F["nfi"], F["fire"]]
DELIVERABLES = ["er_monitoring_report_2024-2025.pdf", "reference_sample_conformed_2024-2025.xlsx"]


def rows_of(path):
    if path.endswith((".csv", ".txt")):
        with open(path, encoding="utf-8", errors="replace") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        import pyarrow.parquet as pq
        return pq.ParquetFile(path).metadata.num_rows
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2026-05-22",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task452",
        "architecture": 2,
        "title": "How many tonnes of emission reductions a lowland forest program can offer a results-based fund for "
                 "2024-2025, from a reference sample drawn on a preliminary change map that the final map revised",
        "domain": "Physical & Environmental Sciences",
        "subdomain": "emissions-inventory (the land-use sector's activity data: two interpretation campaigns conformed "
                     "into one reference dataset on the national forest definition, the reporting period's deforested "
                     "area estimated from it, and the emission reductions a payment agreement pays for)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "other: the tonnes offered and the payment, the area and its interval, each district's area, "
                        "the final map's large patches by district, a chart and the conformed reference sample",
        "as_of": "2026-05-22",
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": [],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task452/generator/build.py (seeded, deterministic) in the "
                               "layouts of a national forest monitoring system's reference sample exports, change map "
                               "deliveries and program documents; the country, its ministry, the fund, the program, "
                               "districts and people are fictional.",
                     "date": "2026-05-22", "license": "CC0-1.0 (original work)"}],
        "created": "2026-05-22",
        "generator": "task452/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=1, ensure_ascii=False)
        fh.write("\n")

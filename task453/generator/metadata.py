"""Write task453/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack as P    # noqa: E402
import world as W   # noqa: E402

TASK = os.path.dirname(HERE)
F = P.FILES
SOURCES = {
    F["old"]: "the Labour Force Survey's estimation cells from CAI 2014 (the previous questionnaire), January 2022 to November 2025",
    F["new"]: "the Labour Force Survey's estimation cells from ICS (the redesigned questionnaire), July 2025 to December 2026",
    F["release"]: "the Labour Force Survey release for December 2026 (Tables 1 to 3)",
    F["field"]: "the fieldwork system's contact outcomes, October to December 2026",
    F["psu"]: "the survey's primary sampling units and their regions, 2025 regional classification",
    F["conc"]: "the regional classification concordance, 2019 and 2025",
    F["pop"]: "the population benchmarks the survey is weighted to, 1 January 2025 to 2027",
    F["seas"]: "the projected seasonal factors for the national unemployment rate, 2027",
    F["resp"]: "Survey Operations' monthly response rates by region, 2025 and 2026",
    F["dict"]: "the field descriptions for the estimation, fieldwork and lookup files",
    F["manifest"]: "the export manifest of 25 January 2027",
    F["note"]: "the methodology note LMM 2025/04 on the redesigned questionnaire and its introduction",
    F["act"]: "the Regional Employment Support Act 2021, Part 1, consolidated to 1 July 2025",
}
DISTRACTORS = [F["pop"], F["seas"], F["resp"]]
DELIVERABLES = ["trigger_restatement_determination_2027.pdf", "regional_unemployment_redesigned_basis_2024-2026.csv"]


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
                      "source": "Constructed: " + SOURCES[f], "date": "2027-01-25",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task453",
        "architecture": 2,
        "title": "How far a statutory unemployment trigger moves when a national Labour Force Survey moves to a "
                 "redesigned questionnaire phased in through its rotation groups, and which regions the restated "
                 "trigger designates for 2027",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "seasonal-adjustment-official-time-series-production (the survey's two collection systems, one per "
                     "questionnaire, conformed into one series on the redesigned basis, and the statutory trigger "
                     "restated by the change the redesign makes to the published rate)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "other: the restated trigger, the change it rests on, the designation of nine regions, the "
                        "fourth-quarter responding dwellings by region, a chart and the regional series on the "
                        "redesigned basis",
        "as_of": "2027-01-25",
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["6.0"],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task453/generator/build.py (seeded, deterministic) in the "
                               "layouts of a national statistics office's Labour Force Survey estimation cells, "
                               "release tables, fieldwork outcomes and lookups; the country, its office, regions, "
                               "statute and people are fictional.",
                     "date": "2027-01-25", "license": "CC0-1.0 (original work)"}],
        "created": "2027-01-25",
        "generator": "task453/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))

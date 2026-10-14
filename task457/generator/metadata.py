"""Write task457/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack as P    # noqa: E402

TASK = os.path.dirname(HERE)
F = P.FILES
SOURCES = {
    F["register"]: "an academic medical center's extract of Open Payments general payments, program years 2021 to 2025, January 2027 publication, for the covered recipients matched to its clinical faculty since 2021, in the Open Payments public file layout",
    F["register_june"]: "the same office's earlier extract of program year 2025 as Open Payments first published it (June 2026)",
    F["profiles"]: "the covered-recipient profiles of every profile the extracts carry, in the Open Payments profile supplement layout",
    F["research"]: "Open Payments research payments naming a faculty member as principal investigator, in the public file layout",
    F["roster"]: "the human resources system's clinical faculty appointment terms since July 2019",
    F["depts"]: "the clinical department codes, with the Department of Medicine's divisions that became departments on 1 July 2025",
    F["entities"]: "the conflict-of-interest disclosure system's company list",
    F["export"]: "the disclosure system's export of every annual disclosure for 2021 to 2026 and every submitted version's items",
    F["history"]: "the disclosure system's submission history",
    F["nih"]: "NIH awards for fiscal year 2025 with a faculty member as contact principal investigator, in the RePORTER export layout",
    F["policy"]: "the medical center's conflict-of-interest policy for the clinical faculty (June 2024)",
    F["guide"]: "the office's guide to the 2026 edition of the annual disclosure form",
    F["dict"]: "the field descriptions of the data files",
    F["manifest"]: "the list of the export's files of 21 January 2027",
}
DISTRACTORS = [F["research"], F["nih"], F["register_june"]]
DELIVERABLES = ["coi_committee_docket_2027-02.docx", "faculty_remuneration_2026_conformed.csv"]


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8", errors="replace") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2027-01-21",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task457",
        "architecture": 1,
        "title": "Which fifteen faculty an academic medical center's conflict-of-interest office sends to its February "
                 "committee, 2026 remuneration from a single manufacturer estimated before Open Payments publishes the year",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "census-register-administrative-data-quality (the faculty's self-reported disclosures validated "
                     "against the Open Payments register on the years both cover, the amount-reporting error measured on "
                     "matched reports and credibility-weighted by the number of them, carried to the year the register "
                     "has not published)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "01: a ranked list under a cap (the committee's fifteen), with a chart, three supporting tables "
                        "and the conformed faculty-by-year file",
        "as_of": "2027-01-27",
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["15", "2026", "2027", "2025", "2021", "11:59", "1,000"],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task457/generator/build.py (seeded, deterministic) in the "
                               "public layouts of Open Payments general and research payments and its covered-recipient "
                               "profile supplement, an NIH RePORTER export, a human resources appointment extract and a "
                               "conflict-of-interest disclosure system's export; the medical center, its office, faculty, "
                               "manufacturers, companies and people are fictional.",
                     "date": "2027-01-21", "license": "CC0-1.0 (original work)"}],
        "created": "2027-01-21",
        "generator": "task457/generator/build.py",
        "files": files,
    }
    json.dump(meta, open(out_path, "w"), indent=1)
    open(out_path, "a").write("\n")
    return meta

"""Write task450/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs as DC   # noqa: E402
import pack as P    # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    P.FILES["resp26"]: "the assessment platform's export of spring 2026 grade-5 mathematics answers, one row per answer",
    P.FILES["resp25"]: "the assessment platform's export of spring 2025 grade-5 mathematics answers, one row per test",
    P.FILES["bank"]: "the district item bank's grade-5 mathematics items, release of 6 April 2026",
    P.FILES["enroll"]: "the student information system's 2025-26 grade-5 enrollment history",
    P.FILES["xwalk"]: "the assessment platform's 2026 registrations, test taker to student",
    P.FILES["merges"]: "the student information system's id merges of 2026",
    P.FILES["directory"]: "the district's campus directory for 2026-27",
    P.FILES["projection"]: "the demographer's 2026-27 grade-5 enrollment projection by campus",
    P.FILES["learning"]: "the curriculum office's log of mathematics professional learning hours, 2025-26",
    P.FILES["dictionary"]: "the assessment office's field dictionary for the extract",
    DC.REPORT: "the District Mathematics Assessment technical report, spring 2025 (excerpt)",
    DC.RULES: "the board's campus designation rules for the 2027 District Improvement Plan",
    DC.NOTICE: "the assessment office's key correction notice of 19 May 2026",
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
                      "source": "Constructed: " + SOURCES[f], "date": "2026-10-09",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task450",
        "title": "Which elementary campuses a Texas district's superintendent's cabinet places its 2027 mathematics "
                 "intervention coaches at, once the spring 2026 grade-5 results on a partly new test form are put on "
                 "the reporting scale set on the 2025 form",
        "domain": "Education & Learning Sciences",
        "subdomain": "item-response-theory-test-equating (a new form linked to the reporting scale through the items "
                     "it shares with the previous form, the two cohorts not equivalent)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "14 (cuts of a distribution): each rated campus's tested and meeting counts and share, the "
                        "designated campuses the call",
        "as_of": "2026-10-09",
        "deliverables": ["intervention_schools_2027.docx", "grade5_math_results_2026.xlsx"],
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task450/generator/build.py (seeded, deterministic) around "
                               "a fictional Texas school district, its campuses and students; no real district, "
                               "campus, person or test item is depicted.",
                     "date": "2026-10-09", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-09",
        "generator": "task450/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))

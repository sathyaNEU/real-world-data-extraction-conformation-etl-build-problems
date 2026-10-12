"""Write task180/metadata.json from the built pack."""
import json
import os
import sys

import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    "screen": "The Pharmacovigilance Unit's quarterly screen of spontaneous reports, Q3 2026, with the line listing of "
              "the quarter's reports for the three validated signals",
    "sop": "SOP-PV-14 Signal refinement in the national registries, revision 3 (effective 1 June 2026)",
    "notes": "The registry data manager's notes on registry extract PV-2026-117 (fields, coverage, record structures)",
    "rx": "Prescription registry: dispensings and returns of the six substances and of NSAIDs (M01A) for the persons in "
          "the extract, 1 January 2018 to 30 June 2026",
    "contacts": "Patient registry: every hospital record of the persons in the extract, 1 January 2018 to 30 June 2026, "
                "in both record structures (LPR2 to 3 February 2019, LPR3 from 4 February 2019)",
    "dx": "Patient registry: the diagnoses on each hospital record (action and secondary)",
    "civil": "Civil registration: birth year, sex, death, most recent emigration and immigration of every person in the "
             "extract",
    "matched": "The Agency's standard matched comparator extract: two non-users per first dispensing of tasorexant, "
               "corinurad or velaglutide, matched on birth year and sex",
    "atc": "The ATC/DDD index for the substances in the extract, with code validity dates",
    "population": "National population on 1 January by age group and sex, and national admissions under the SOP-PV-14 "
                  "case definitions, 2022 to 2025",
    "psur": "The marketing authorisation holder's PSUR summary for Somnevo (tasorexant), data lock 31 January 2026",
    "minutes": "Minutes of the Medicines Safety Committee meeting of 9 July 2026",
}
DATES = {"screen": "2026-10-07", "sop": "2026-05-20", "notes": "2026-09-04", "rx": "2026-09-04",
         "contacts": "2026-09-04", "dx": "2026-09-04", "civil": "2026-09-04", "matched": "2026-09-04",
         "atc": "2026-09-04", "population": "2026-09-04", "psur": "2026-04-08", "minutes": "2026-07-13"}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        return int(pq.ParquetFile(path).metadata.num_rows)
    return None


def write(target, out_path):
    files = []
    for k, f in B.FILES.items():
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[k], "date": DATES[k],
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    files.sort(key=lambda x: x["path"])
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task180",
        "title": "Which of three spontaneous-report signals the national registries support, for the one formal "
                 "assessment the medicines safety committee can open",
        "domain": "Pharmacology, Pharmacoepidemiology & Safety",
        "subdomain": "safety signal detection and refinement (a national medicines agency's pharmacovigilance unit "
                     "refining the quarter's signals in the national prescription and patient registries)",
        "objective": "Anomaly Detection & Diagnostics",
        "prompt_shape": "18 (hypotheses against evidence): three signals, each confirmed or refuted in the registries",
        "as_of": "2026-10-12",
        "deliverables": ["signal_refinement_note.docx", "new_users_by_year.csv"],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"],
                        "bytes_total": sum(x["bytes"] for x in files)},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task180/generator/build.py (seeded, deterministic) around a "
                               "fictional national medicines agency (the Agency) in Denmark, three fictional medicines "
                               "(tasorexant, corinurad, velaglutide) and a fictional marketing authorisation holder, "
                               "with real ATC groups, ICD-10 codes in the Danish registries' D-prefixed form and the "
                               "Danish registries' record structures; no real person, patient, report or product is "
                               "depicted.",
                     "date": "2026-09-04", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-11",
        "generator": "task180/generator/build.py",
        "files": files,
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))

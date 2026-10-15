"""Write task139/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    K.EXTRACT: "Haverline Casualty's claims listing: every claim reported January 2021 to September 2026 whose first "
               "report recorded time lost or that has paid or reserved indemnity",
    K.REGISTER: "The triage screen's assignment register of the Early Return Nursing pilot, with its notes",
    K.NURSE_LOG: "The ERN case system's export of the pilot nurses' files and reopenings",
    K.REVIEW_BOOK: "Kellerman Pryce Actuarial's verification workbook: verified ultimate indemnity on the sampled pilot "
                   "claims at 30 June 2026",
    K.REVIEW_PDF: "Kellerman Pryce Actuarial's report on the verification of the pilot claims (14 August 2026)",
    K.CHARTER: "The signed Early Return Nursing programme charter for 2027 (19 October 2026)",
    K.CHARTER_DRAFT_DOC: "Draft v3 of the 2027 programme charter (18 September 2026), superseded",
    K.PICK_MEMO: "The chief pricing actuary's memorandum on the ERN credit in the AY2027 indemnity pick (28 October 2026)",
    K.CROSSWALK: "Legacy segment codes and the 2025 codes they converted to",
    K.PAYMENTS: "Indemnity payment register lines, January to September 2026",
    K.ACH_RETURNS: "The bank's ACH return items on workers' compensation EFT payments, January to September 2026",
    K.MERGES: "Claims merged on the claims system in 2025 (each claim merged, the claim it joined, the date and unit)",
    K.DICTIONARY: "Data dictionary for the pack's claims files",
    K.MANIFEST: "Export manifest: each file, its source system, as-of date and preparer",
    K.SURVEY: "The ERN pilot's worker satisfaction survey",
    K.STAFFING: "Medical Case Management's 2027 ERN staffing plan (positions, status, salary midpoints)",
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
                      "source": "Constructed: " + SOURCES[f], "date": "2026-11-09",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task139",
        "title": "Where Haverline Casualty's seventeen Early Return Nursing teams work in 2027 and the AY2027 indemnity "
                 "they save",
        "domain": "Actuarial Science & Insurance",
        "subdomain": "claims-frequency-severity (a workers' compensation nurse programme's saving read as indemnity per "
                     "assigned intake, frequency times severity, from a randomised pilot, valued per nurse place-day)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "05: seventeen teams allocated across eight segments (teams and saving per team-year for every "
                        "segment, the AY2027 credit), the note's chart, and two per-segment asks (2025 intakes; "
                        "indemnity paid January to September 2026)",
        "as_of": "2026-11-09",
        "deliverables": [K.GOLD_BOOK, K.GOLD_NOTE],
        "distractor_files": list(K.DISTRACTORS),
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task139/generator/build.py (seeded, deterministic) around a "
                               "fictional Missouri workers' compensation carrier (Haverline Casualty Company), its "
                               "consulting actuaries (Kellerman Pryce Actuarial), claim units and people; no real "
                               "organisation, person, employer or claim is depicted. NCCI classification codes and "
                               "Missouri benefit rules are used descriptively.",
                     "date": "2026-11-09", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-12",
        "revised": "2026-10-15",
        "generator": "task139/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))

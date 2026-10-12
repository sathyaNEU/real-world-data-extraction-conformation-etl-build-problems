"""Write task449/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs as DC   # noqa: E402
import pack as P    # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    P.FILES["register"]: "the case system's matter register, every matter opened 1 October 2025 to 8 October 2026",
    P.FILES["history"]: "the case system's status history for the same matters",
    P.FILES["social"]: "the social care desk tool's export of the posts it opened matters for",
    P.FILES["meridel"]: "the payment processor's list of the payments received 8 to 10 May 2026",
    P.FILES["portfolio"]: "the card issuer's month-end open accounts",
    P.FILES["codes"]: "the issuer's complaint code list",
    P.FILES["time"]: "the outsourcer's time records for its Bellcroft site",
    P.FILES["marlowby"]: "a staffing agency's weekly timesheet exports",
    P.FILES["treadwell"]: "a staffing agency's hours report",
    P.FILES["opslog"]: "the complaint desk's operations log",
    P.FILES["ivr"]: "the complaint line's weekly call statistics",
    P.FILES["cfpb"]: "CFPB public complaint database rows for the issuer, in the CFPB layout",
    P.FILES["manifest"]: "the export manifest",
    DC.WPS: "the outsourcer's workforce planning standard",
    DC.SCHEDULE: "Schedule 7 to the issuer's ACH processing agreement",
    DC.SOW: "Exhibit B of the 2026 statement of work",
    DC.DICTIONARY: "the field dictionary",
}


def rows_of(path):
    if path.endswith((".csv", ".jsonl")):
        with open(path, encoding="utf-8", errors="replace") as fh:
            n = sum(1 for _ in fh)
        return n - (0 if path.endswith(".jsonl") else 1)
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
        "task": "task449",
        "title": "How many dedicated complaint analysts a card issuer's outsourced desk carries into 2027, sized on the "
                 "sustained weekly matters once the matters arising from its processor's payment-posting failure are "
                 "taken out, when a fifth of the matters were linked to a cardholder by a name-and-city search",
        "domain": "General Statistics & Data Science",
        "subdomain": "data-integration-record-linkage-entity-resolution (a characteristic read through uncertain links, "
                     "corrected for the false-link rate)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "other: one integer call with its base and deduction, nine month-end open counts with a chart, "
                        "nine monthly flex-hour figures",
        "as_of": "2026-10-09",
        "deliverables": ["dedicated_analysts_2027.docx", "flex_hours_2026.csv"],
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task449/generator/build.py (seeded, deterministic) around a "
                               "fictional card issuer, its complaint outsourcer, its payment processor and two staffing "
                               "agencies; no real consumer, complaint, payment or company is depicted.",
                     "date": "2026-10-09", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-09",
        "generator": "task449/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))

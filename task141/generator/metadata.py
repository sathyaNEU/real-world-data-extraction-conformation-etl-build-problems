"""Write task141/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    K.DRAFT: "Local bail policy revision for 2027, draft for consultation of 6 October 2026 (Senior Resident Superior "
             "Court Judge)",
    K.POLICY24: "Local bail policy for pretrial release, effective 1 July 2024",
    K.GUIDE: "Pretrial Assessment Scale scoring guide, version 2 (Pretrial Services)",
    K.FA_LEGACY: "Initial appearances on new charges from the clerk's legacy system, 1 October 2021 to 3 March 2024",
    K.FA_NEW: "Initial appearances on new charges from the case management system, 4 March 2024 to 30 September 2026",
    K.FA_CHARGES: "The charges at those appearances from 4 March 2024, with their case numbers",
    K.SCREENS: "Pretrial Assessment Scale screens, 1 October 2021 to 30 September 2026",
    K.JAIL: "Detention center bookings from the Sheriff's Office jail system, 1 October 2021 to 30 September 2026",
    K.ARRESTS: "State arrest repository extract for every defendant in the first-appearance exports, run 2 October 2026",
    K.CASES: "Criminal case index with dispositions, cases filed from 1 October 2021",
    K.EVENTS: "Court events, 1 October 2025 to 30 September 2026",
    K.EM: "Electronic monitoring vendor invoice lines, October 2025 to September 2026",
    K.HALSEY: "Halsey County inmate housing invoices to the Sheriff's Office, November 2025 to September 2026",
    K.CROSSWALK: "Offense code crosswalk, legacy to new system (clerk)",
    K.ROSTER: "Magistrate roster and duty shifts, 2021 to 2026 (chief magistrate)",
    K.JAIL_CODES: "Jail booking types, release types and facilities",
    K.COURT_CODES: "Court codes: conditions, dispositions and events",
    K.README: "Pretrial Services' note on the extracts",
    K.CJAC: "Criminal Justice Advisory Council jail population report for 2025",
    K.CRIME: "Reported offenses by Dorrance County agencies, 2019 to 2025",
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
                      "source": "Constructed: " + SOURCES[f], "date": "2026-10-02",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task141",
        "title": "The highest Pretrial Assessment Scale score Dorrance County's 2027 bail policy can release on a "
                 "written promise at first appearance under its 85 per cent safety floor",
        "domain": "Criminology & Justice",
        "client_domain": "Criminology & Justice",
        "subdomain": "recidivism-risk-assessment (pretrial risk assessment: each score's new-offence rate for every "
                     "eligible defendant a presumptive release tier would release, estimated past the selective "
                     "labels of the outcome record)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "04: setting one dial (the tier's top score, scores 1 to 6 the settings), with three 2025-26 "
                        "tables (bed-days in custody and monitoring days by new-criminal-activity score, missed court "
                        "dates by failure-to-appear score) and one chart",
        "as_of": "2026-10-14",
        "deliverables": [K.GOLD_MEMO, K.GOLD_BOOK, K.GOLD_CHART],
        "distractor_files": list(K.DISTRACTORS),
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task141/generator/build.py (seeded, deterministic) around "
                               "a fictional North Carolina county (Dorrance County, county seat Garrison), its courts, "
                               "magistrates, Pretrial Services, Sheriff's Office and people, and a fictional "
                               "neighbouring county (Halsey County); no real organisation, person or system is "
                               "depicted. Offense descriptions and statute citations follow the North Carolina "
                               "General Statutes in form only.",
                     "date": "2026-10-02", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-15",
        "generator": "task141/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))

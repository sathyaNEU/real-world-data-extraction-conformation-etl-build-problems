"""Write task130/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    K.REGISTER: "Risk management claims register extract: every clinician named on a claim number, valued 30 September 2026",
    K.PAYROLL: "Legacy payroll history: paid FTE by employee, month and cost centre for employed clinicians, residents, fellows and psychologists, January 2016 to December 2025",
    K.HCM: "HCM pay lines for clinicians, one row per worker, position, work month and earning code, January to September 2026",
    K.CROSSWALK: "HCM job profiles mapped to the legacy job codes they replaced",
    K.DIRECTORY: "General ledger cost centre directory: company, entity and department",
    K.PLAN: "2027 staffing plan: covered clinician FTE by entity, specialty class and month",
    K.AGREEMENT: "Corvane Professional Liability Trust Agreement as executed (extract: definitions, coverage, claims administration, Schedules A and B)",
    K.POLICY: "Trust funding policy as adopted by the Trustees",
    K.QM_SEP: "Quillan Mutual loss run for Tolliver Falls Hospital and Alderwick Medical Center, valued 30 September 2026",
    K.QM_JUN: "Quillan Mutual loss run valued 30 June 2026, revision 1 issued 9 October 2026",
    K.SC_SEP: "Stoneleigh Casualty loss run for Corvane Medical Group and Brennick Community Hospital, valued 30 September 2026",
    K.NOTICES: "Precautionary notices risk management sent to the carriers, 2012 to September 2026",
    K.SAFETY: "Patient safety event reports, January 2019 to September 2026",
    K.PREMIUMS: "Clinician professional liability premium history by entity and policy year, 2017 to 2026",
    K.DICTIONARY: "Data dictionary for the risk management extracts",
    K.EXTRACT_LOG: "Extract log: each file's system, date, row count and preparer",
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
        "task": "task130",
        "title": "The 2027 contribution to Corvane Health's new claims-made professional liability trust",
        "domain": "Actuarial Science & Insurance",
        "subdomain": "pricing-ratemaking-credibility (first-year funding of a self-insured claims-made professional "
                     "liability trust at an Oregon health system)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "other: the contribution with the expected number of claims and what each of four entities "
                        "pays toward it, the emergence chart by month and entity, and two reconciliation asks",
        "as_of": "2026-10-12",
        "deliverables": list(K.DELIVERABLES),
        "distractor_files": list(K.DISTRACTORS),
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task130/generator/build.py (seeded, deterministic) around "
                               "a fictional Oregon health system (Corvane Health), its hospitals, medical group, trust, "
                               "carriers and people; no real organisation, person, patient or claim is depicted.",
                     "date": "2026-10-12", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-12",
        "generator": "task130/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))

"""Write task453/metadata.json from the built pack. Each file's provenance (what it is, what it covers, the office that
owns it and the date it was extracted or issued) lives here, outside the pack: no file under target/ describes the
others."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W   # noqa: E402

TASK = os.path.dirname(HERE)
F = W.FILES
PROVENANCE = {
    F["permits"]: ("the Vital Statistics Agency's extract of cremation permits returned by crematoria, 1 December 2025 "
                   "to 31 January 2027", "permits returned 1 December 2025 to 31 January 2027", W.AGENCY, "2027-02-08"),
    F["register"]: ("the Crematoria Mercury Fund's register of member crematoria and the agency's facility numbers",
                    "as checked 15 January 2027", W.FUND, "2027-01-15"),
    F["s1996"]: ("report tables of the National Adult Dentition Survey, 1996 wave", "1996", W.SURVEY_BODY, "1997-06-11"),
    F["s2006"]: ("report tables of the National Adult Dentition Survey, 2006 wave", "2006", W.SURVEY_BODY, "2007-06-19"),
    F["s2016"]: ("report tables of the National Adult Dentition Survey, 2016 wave", "2016", W.SURVEY_BODY, "2017-06-14"),
    F["reg"]: ("the Crematoria Mercury Regulation (Regulation 41/2023), consolidated", "consolidated to 1 January 2025",
               "Office of Legislative Counsel", "2025-01-01"),
    F["rules"]: ("the Crematoria Mercury Fund's scheme rules for 2026", "2026 scheme year", W.FUND, "2025-11-18"),
    F["ar_halbrook"]: ("the City of Halbrook's bereavement services receivables extract (Halbrook Memorial and Ostrander "
                       "Hill crematoria)", "postings 1 December 2025 to 19 February 2027", "City of Halbrook",
                       "2027-02-26"),
    F["ar_shoreline"]: ("Shoreline Memorial Group's receivables for its four crematoria", "postings 1 December 2025 to 19 "
                        "February 2027", "Shoreline Memorial Group", "2027-02-26"),
    F["ar_members"]: ("the fee returns the independent crematoria lodge with the Fund each week", "weeks ending 7 "
                      "December 2025 to 21 February 2027", W.FUND, "2027-02-26"),
    F["cycles"]: ("cremator controller cycles at every member crematorium, 2026", "1 January to 31 December 2026",
                  W.FUND, "2027-01-29"),
    F["plant"]: ("abatement plant historian exports (events and 10-minute inlet temperatures) at the abated crematoria, "
                 "2026", "1 January (or commissioning) to 31 December 2026", W.FUND, "2027-01-29"),
    F["stack"]: ("the Air Quality Branch's summary of mercury stack tests at abated crematoria, 2019 to 2025",
                 "2019 to 2025", "Air Quality Branch", "2026-03-03"),
    F["deaths"]: ("the Vital Statistics Agency's preliminary deaths registered in 2026 by region, age group and sex",
                  "deaths registered in 2026", W.AGENCY, "2027-02-12"),
}
DISTRACTORS = [F[k] for k in W.DISTRACTORS]
DELIVERABLES = [W.GOLDEN["cert"], W.GOLDEN["book"]]


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        import pyarrow.parquet as pq
        return pq.ParquetFile(path).metadata.num_rows
    if path.endswith(".xlsx"):
        from openpyxl import load_workbook
        wb = load_workbook(path, read_only=True)
        return sum(ws.max_row for ws in wb.worksheets)
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        what, covers, owner, issued = PROVENANCE[f]
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + what, "covers": covers, "owner": owner, "extracted_or_issued": issued,
                      "date": "2027-02-26", "license": "CC0-1.0 (original work, constructed for this task)"})
    meta = {
        "task": "task453",
        "architecture": 3,
        "title": "Which crematoria a provincial crematoria mercury fund designates to fit mercury abatement after its "
                 "2026 scheme year, with each crematorium's 2026 levy and each abated crematorium's bypassed "
                 "cremations by quarter",
        "domain": "Physical & Environmental Sciences",
        "subdomain": "emissions-inventory (a provincial cremation source's 2026 abated share against a filed "
                     "threshold and the designations it triggers)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "other: the verdict on the 2026 share, the designated crematoria, a chart of each "
                        "crematorium's mercury, each crematorium's 2026 levy and each abated crematorium's bypassed "
                        "cremations by quarter",
        "as_of": "2027-02-26",
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "distractor_notes": {
            F["stack"]: "post-abatement stack concentrations at the abated crematoria; the Regulation measures the "
                        "mercury a cremation releases by the amalgam of the person cremated, so no figure uses them",
            F["deaths"]: "all deaths registered in 2026 by region of residence, every disposition; the cremations are "
                         "the permits, so no figure uses it"},
        "files": files,
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_rows": max((x["rows"] or 0) for x in files)},
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta

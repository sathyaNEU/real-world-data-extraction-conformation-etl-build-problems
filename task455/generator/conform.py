"""Read the pack the way the department's analyst does: the death file's versions as they stood on a day, the
residents' drug overdose deaths, each certificate's drug category, and the medical examiner's review by drug class.
Shared by golden.py, methods.py and checks.py; verify.py reads the pack on its own."""
import csv
import datetime as dt
import os

COUNTY = "Wendmoor"
OD_UCOD = ("X40", "X41", "X42", "X43", "X44", "X60", "X61", "X62", "X63", "X64", "X85", "Y10", "Y11", "Y12", "Y13", "Y14")
OPIOID = ("T40.0", "T40.1", "T40.2", "T40.3", "T40.4", "T40.6")
STIM = ("T40.5", "T43.6")
OPIOID_DRUGS = {"fentanyl", "heroin", "oxycodone", "hydrocodone", "morphine", "methadone", "tramadol", "opioid (unspecified)"}
STIM_DRUGS = {"methamphetamine", "amphetamine", "cocaine"}


def dotted(c):
    return c if "." in c or len(c) < 4 else c[:3] + "." + c[3:]


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def day(s):
    return dt.date.fromisoformat(s)


def versions_by_record(rows, receipts=None):
    """state file number -> its versions in order, each with the day it entered the state's file (the day the
    exchange delivered it for an out-of-state death, else the day it was registered)."""
    recv = {}
    for r in receipts or []:
        recv[(r["state_file_no"], int(r["record_version"]))] = day(r["received_date"])
    out = {}
    for r in rows:
        r = dict(r)
        r["record_version"] = int(r["record_version"])
        r["on_file"] = recv.get((r["state_file_no"], r["record_version"]), day(r["registered_date"]))
        out.setdefault(r["state_file_no"], []).append(r)
    for v in out.values():
        v.sort(key=lambda r: r["record_version"])
    return out


def as_of(recs, when=None, by="on_file"):
    """Each record's latest version on the file on day `when` (None: the latest version of all), voids applied."""
    out = []
    for sfn, vs in recs.items():
        live = [v for v in vs if when is None or day(v[by]) <= when] if by == "registered_date" else \
               [v for v in vs if when is None or v[by] <= when]
        if not live:
            continue
        v = live[-1]
        if v["record_status"] == "Void":
            continue
        out.append(v)
    return out


def is_overdose(v):
    return v["underlying_cause"][:3] in OD_UCOD


def is_resident(v):
    return v["residence_county"] == COUNTY and not v["residence_state"]


def year_of(v):
    return int(v["date_of_death"][:4])


def category(v):
    cs = [dotted(c) for c in v["record_axis"].split()]
    if any(c.startswith(OPIOID) for c in cs):
        return "OL"
    if any(c.startswith(STIM) for c in cs):
        return "SO"
    return "N"


def resident_overdoses(recs, when=None):
    return [v for v in as_of(recs, when) if is_overdose(v) and is_resident(v)]


def drug_list(s):
    return [x.strip() for x in s.split(";") if x.strip()]


def review_class(r):
    c = set(drug_list(r["drugs_caused_or_contributed"]))
    if c & OPIOID_DRUGS:
        return "O"
    if c & STIM_DRUGS:
        return "S"
    return "R"


def read_review(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb["Cases"]
    it = ws.iter_rows(values_only=True)
    head = [h for h in next(it)]
    out = []
    for row in it:
        if row[0] is None:
            continue
        out.append({h: ("" if x is None else str(x)) for h, x in zip(head, row)})
    return out


def death_keys(receipts):
    """state file number -> the death it records: a death received through the interstate exchange is the sending
    state's certificate, whatever number this office gave the copy it holds."""
    return {r["state_file_no"]: ("X", r["sending_state"], r["sending_state_file_no"]) for r in receipts}


def load(target):
    from pack import FILES as F
    rows = read_csv(os.path.join(target, F["deaths"]))
    rec = read_csv(os.path.join(target, F["receipts"]))
    return {"rows": rows, "receipts": rec, "recs": versions_by_record(rows, rec),
            "review": read_review(os.path.join(target, F["review"]))}

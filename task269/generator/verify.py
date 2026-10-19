"""task269's independent verifier: reads only the shipped pack (and, given a second folder, the goldens) and
recomputes every graded figure from the files, with no generator state.

    python3 verify.py <target> [<golden>]

The call: each examiner's station mark from the OSCE system's export (both days' formats, the withdrawn item out,
items not applicable out of the points available), the generalizability study of the 2026 marks (candidates x
stations x the station's two examiners), and the decision study for 2027's single examining in parallel circuits.
Ask A: the case bank's cases eligible for May 2027 under policy 4.4, by blueprint domain, and how many need a
simulated patient. Ask B: the examiners eligible at the December allocation (policy 5.2) who offered each site and
session in their latest response."""
import csv
import datetime as dt
import json
import os
import re
import sys
import unicodedata

import numpy as np
import openpyxl

LABEL = {"Not done": 0, "Partly done": 1, "Done well": 2, "N/A": None}
DOMAINS = ["History taking", "Physical examination", "Communication", "Procedural skills"]
SITES = {"Clinical Skills Centre, Callowfield": "CSC", "Simulation Suite, Callowfield University Hospital": "CUH",
         "Clinical Skills Unit, Fennabeg Clinical School": "FCS"}
SESS = ["d1_am", "d1_pm", "d2_am", "d2_pm"]


def rows_xlsx(path, sheet=None):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[sheet] if sheet else wb.worksheets[0]
    it = ws.iter_rows(values_only=True)
    head = next(it)
    return [dict(zip(head, r)) for r in it]


def pdf_text(path):
    from pypdf import PdfReader
    txt = "\n".join(p.extract_text() for p in PdfReader(path).pages)
    return re.sub(r"\s+", " ", txt)


def docx_text(path):
    import docx
    return re.sub(r"\s+", " ", " ".join(p.text for p in docx.Document(path).paragraphs))


def documents(t):
    """Every document the computations lean on, read through its own format's extractor, each with a positive
    control (a sentence the document carries) on the same code path as the values taken from it."""
    pol = pdf_text(os.path.join(t, "assessment_policy_v7.pdf"))
    mins = pdf_text(os.path.join(t, "board_of_examiners_minutes_2026-05-14.pdf"))
    plan = docx_text(os.path.join(t, "final_osce_2027_delivery_plan.docx"))
    for name, txt in (("policy", pol), ("minutes", mins), ("plan", plan)):
        assert len(txt) > 500, name
    assert "A candidate's total mark is the sum of their station marks" in pol
    m = re.search(r"must rank candidates with a reliability of at least (0\.\d+)", pol)
    assert m, "policy 4.3 not read"
    standard = float(m.group(1))
    assert "an item marked not applicable not being available, expressed out of 20" in pol
    assert "in the three years before the sitting" in pol and "in either of the two previous years" in pol
    assert "who have completed the examiner training or an examiner refresher in the three years before the " \
           "allocation" in pol
    m = re.search(r"item (\d+) \(", mins)
    assert m and "Station 7, item 14" in mins and "removed from every candidate's mark" in mins
    withdrawn = (7, int(m.group(1)))
    m = re.search(r"Each site has (\w+) rooms that can hold a station", plan)
    assert m and "Each station will have one examiner in each circuit" in plan
    rooms = {"eighteen": 18}[m.group(1)]
    assert "their latest response stands" in plan
    return {"standard": standard, "withdrawn": withdrawn, "rooms": rooms}


def station_marks(t, withdrawn=(7, 14)):
    st = rows_xlsx(os.path.join(t, "osce2026_station_sheet.xlsx"))
    num_of_code = {r["Case code"]: int(r["Station"]) for r in st}
    al = rows_xlsx(os.path.join(t, "osce2026_examiner_allocation.xlsx"))
    role_of_staff = {(int(r["Station"]), r["Staff no."]): 0 if r["Role"].startswith("Lead") else 1 for r in al}
    role_of_badge = {(int(r["Station"]), r["Badge"]): 0 if r["Role"].startswith("Lead") else 1 for r in al}
    pts, avail = {}, {}
    cands = set()
    with open(os.path.join(t, "osce2026_marks_export.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["item"] == "GG":
                continue
            if r["exam_day"] == "1":
                sno = int(r["station"])
                ro = role_of_badge[(sno, r["examiner"])]
                v = LABEL[r["response"]]
            else:
                sno = num_of_code[r["station"]]
                ro = role_of_staff[(sno, r["examiner"])]
                v = None if r["response"] == "NA" else int(r["response"])
            if sno == withdrawn[0] and r["item"] == str(withdrawn[1]):   # withdrawn by the board (minutes)
                continue
            key = (r["exam_no"], sno, ro)
            cands.add(r["exam_no"])
            if v is None:
                continue
            pts[key] = pts.get(key, 0) + v
            avail[key] = avail.get(key, 0) + 2
    cands = sorted(cands)
    y = np.zeros((len(cands), 12, 2))
    for i, c in enumerate(cands):
        for s in range(1, 13):
            for ro in (0, 1):
                y[i, s - 1, ro] = 20.0 * pts[(c, s, ro)] / avail[(c, s, ro)]
    return y, cands


def gstudy(y):
    n_p, n_s, n_r = y.shape
    g = y.mean()
    yp, ys, yps, yrs = y.mean(axis=(1, 2)), y.mean(axis=(0, 2)), y.mean(axis=2), y.mean(axis=0)
    ms_p = n_s * n_r * ((yp - g) ** 2).sum() / (n_p - 1)
    ms_s = n_p * n_r * ((ys - g) ** 2).sum() / (n_s - 1)
    ms_rs = n_p * ((yrs - ys[:, None]) ** 2).sum() / (n_s * (n_r - 1))
    ms_ps = n_r * ((yps - yp[:, None] - ys[None, :] + g) ** 2).sum() / ((n_p - 1) * (n_s - 1))
    res = y - yps[:, :, None] - yrs[None, :, :] + ys[None, :, None]
    ms_e = (res ** 2).sum() / ((n_p - 1) * n_s * (n_r - 1))
    return {"e": ms_e, "ps": (ms_ps - ms_e) / n_r, "p": (ms_p - ms_ps) / (n_s * n_r), "rs": (ms_rs - ms_e) / n_p,
            "s": (ms_s - ms_ps - ms_rs + ms_e) / (n_p * n_r)}


def call(t):
    doc = documents(t) if os.path.exists(os.path.join(t, "assessment_policy_v7.pdf")) else \
        {"standard": 0.80, "withdrawn": (7, 14), "rooms": 18}
    y, cands = station_marks(t, doc["withdrawn"])
    v = gstudy(y)
    rel = {n: v["p"] / (v["p"] + (v["ps"] + v["rs"] + v["e"]) / n) for n in range(12, doc["rooms"] + 1)}
    stations = min(n for n in rel if rel[n] >= doc["standard"])
    return {"components": v, "reliability": rel, "stations": stations, "candidates": len(cands)}


# ---------------------------------------------------------------------------------------------- Ask A
def bank_date(x):
    if isinstance(x, dt.datetime):
        return x.date()
    if isinstance(x, dt.date):
        return x
    d, m, y = (int(p) for p in str(x).split("/"))
    return dt.date(y, m, d)


def recreated_pairs(cases):
    """The records the November 2025 cut-over re-created (migration report, section 2): a record written in the new
    bank in 2025 (code CV-25-) whose title is a retired record's in the same domain; it carries that record's
    version forward by one and its last review date, as every re-created record does here."""
    retired = {}
    for c in cases:
        if c["Status"] == "Retired":
            retired.setdefault((c["Blueprint domain"], c["Title"]), []).append(c)
    out = {}
    for c in cases:
        if c["Case code"].startswith("CV-25-") and (c["Blueprint domain"], c["Title"]) in retired:
            old = retired[(c["Blueprint domain"], c["Title"])]
            assert len(old) == 1
            assert int(c["Version"]) == int(old[0]["Version"]) + 1
            assert bank_date(c["Last reviewed"]) == bank_date(old[0]["Last reviewed"])
            out[c["Case code"]] = old[0]["Case code"]
    return out


def ask_a(t):
    mig = pdf_text(os.path.join(t, "casebank_migration_report_2025-11.pdf"))
    assert len(mig) > 500 and "re-created as a new record under a new code" in mig, "migration report not read"
    cases = rows_xlsx(os.path.join(t, "case_bank_export_2026-11-30.xlsx"), "Cases")
    exposed = set()
    with open(os.path.join(t, "case_usage_history_2021_2026.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if int(r["sitting_date"][:4]) in (2025, 2026):
                exposed.add(r["case_code"])
    origin = recreated_pairs(cases)
    out = {}
    for d in DOMAINS:
        el = [c for c in cases if c["Blueprint domain"] == d and c["Status"] in ("Active", "Active - edits pending")
              and bank_date(c["Last reviewed"]) >= dt.date(2024, 5, 11) and c["Case code"] not in exposed
              and origin.get(c["Case code"]) not in exposed]
        out[d] = (len(el), sum(1 for c in el if c["Resources"] in ("SP", "SP and task trainer")))
    return out


# ---------------------------------------------------------------------------------------------- Ask B
def norm_name(x):
    x = re.sub(r"^(dr|prof|mr|ms|mrs)\.?\s+", "", x.strip(), flags=re.I)
    x = unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z]", "", x)


def ask_b(t):
    reg = rows_xlsx(os.path.join(t, "examiner_register_2026-11-30.xlsx"))
    by_email = {r["Email"].lower(): r["Staff no."] for r in reg}
    by_name = {}
    for r in reg:
        by_name.setdefault(norm_name("%s %s" % (r["Forename"], r["Surname"])), []).append(r["Staff no."])
    attended = {}
    with open(os.path.join(t, "examiner_training_attendance_2021_2026.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["outcome"] == "Attended":
                d = dt.date.fromisoformat(r["session_date"])
                attended[r["staff_no"]] = max(d, attended.get(r["staff_no"], d))
    elig_grades = {"Professor", "Associate Professor", "Senior Lecturer", "Lecturer", "Consultant", "GP Trainer"}
    ok = set()
    for r in reg:
        last = max(bank_date(r["Examiner training"]), attended.get(r["Staff no."], dt.date(1900, 1, 1)))
        if r["Status"] == "Active" and r["Grade"] in elig_grades and last >= dt.date(2023, 12, 7):
            ok.add(r["Staff no."])
    latest = {}
    with open(os.path.join(t, "examiner_availability_2027_responses.csv"), newline="", encoding="utf-8") as f:
        rd = csv.reader(f)
        head = next(rd)
        for r in rd:
            when = dt.datetime.strptime(r[0], "%d/%m/%Y %H:%M:%S")
            staff = by_email.get(r[1].lower())
            if staff is None:
                hits = by_name.get(norm_name(r[2]), [])
                staff = hits[0] if len(hits) == 1 else None
            if staff is None:
                continue
            if staff not in latest or when > latest[staff][0]:
                latest[staff] = (when, SITES[r[3]], {s: r[4 + k] == "Yes" for k, s in enumerate(SESS)})
    out = {}
    for site in ("CSC", "CUH", "FCS"):
        for s in SESS:
            out[(site, s)] = sum(1 for st, (_, si, ti) in latest.items() if st in ok and si == site and ti[s])
    return out


def main():
    t = sys.argv[1]
    c = call(t)
    a = ask_a(t)
    b = ask_b(t)
    print("call: %d stations; reliability %s" % (c["stations"], {n: round(r, 4) for n, r in c["reliability"].items()}))
    print("components", {k: round(x, 4) for k, x in c["components"].items()})
    print("ask A", a)
    print("ask B", b)
    if len(sys.argv) > 2:
        g = sys.argv[2]
        fig = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
        assert fig["call"]["stations"] == c["stations"], (fig["call"]["stations"], c["stations"])
        for n in range(12, 19):
            assert fig["reliability"][str(n)] == "%.3f" % c["reliability"][n], n
        for d in DOMAINS:
            assert tuple(fig["ask_a"][d]) == a[d], d
        for (site, s), v in b.items():
            assert fig["ask_b"]["%s %s" % (site, s)] == v, (site, s)
        wb = openpyxl.load_workbook(os.path.join(g, "osce2027_station_plan.xlsx"), data_only=True)
        assert wb.sheetnames == ["Stations", "Sources of variance", "Case bank", "Examiners"], wb.sheetnames
        cells = {}
        for ws in wb.worksheets:
            for row in ws.iter_rows(values_only=True):
                if row and row[0] is not None:
                    cells[(ws.title, row[0])] = row[1:]
        assert cells[("Stations", "Stations to set")][0] == c["stations"]
        for n in range(12, 19):
            assert "%.3f" % cells[("Stations", n)][0] == "%.3f" % c["reliability"][n], n
            assert cells[("Stations", n)][1] == ("Yes" if c["reliability"][n] >= 0.80 else "No"), n
        for d in DOMAINS:
            assert tuple(cells[("Case bank", d)][:2]) == a[d], d
        names = {code: name for name, code in SITES.items()}
        for (site, s_), v in b.items():
            assert cells[("Examiners", names[site])][SESS.index(s_)] == v, (site, s_)
        print("goldens agree with the pack")
    print("verify: PASS")


if __name__ == "__main__":
    main()

"""Independent verifier for task266: reads only the bundle (target/, the goldens and figures.json) on its own code
path (pandas readers, its own PDF parse of the published schedule, its own doubly truncated estimate) and recomputes
the call, every share, the members by setting and the unit's reviews by town.

    python3 verify.py <target>"""
import datetime as dt
import json
import os
import re
import sys

import numpy as np
import pandas as pd
from pypdf import PdfReader

YEAR = 365.25
START, END = pd.Timestamp("2004-07-01"), pd.Timestamp("2026-06-30")
COHORT = pd.Timestamp("1986-01-01")
TERM = pd.Timestamp("2027-07-01")
FY0, FY1 = pd.Timestamp("2025-07-01"), pd.Timestamp("2026-06-30")
SETTINGS = [40, 45, 50, 55, 60, 65, 70]
FAILS = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


def find(target, pat):
    hits = [f for f in os.listdir(target) if re.search(pat, f)]
    assert len(hits) == 1, (pat, hits)
    return os.path.join(target, hits[0])


def text(path):
    return re.sub(r"\s+", " ", " ".join(p.extract_text() or "" for p in PdfReader(path).pages))


def ep(t, u, v):
    """Doubly truncated NPMLE by the self-consistency iteration, windows as sorted-index ranges."""
    x = np.unique(t)
    n = np.bincount(np.searchsorted(x, t), minlength=len(x)).astype(float)
    lo = np.searchsorted(x, u)
    hi = np.searchsorted(x, v, side="right")
    f = n / n.sum()
    for _ in range(100000):
        c = np.r_[0.0, np.cumsum(f)]
        P = c[hi] - c[lo]
        inv = 1.0 / P
        d = np.bincount(lo, weights=inv, minlength=len(x) + 1) - np.bincount(hi, weights=inv, minlength=len(x) + 1)
        g = n / np.cumsum(d)[:len(x)]
        g /= g.sum()
        if np.abs(g - f).max() < 1e-13:
            return x, g
        f = g
    return x, f


def main(target):
    task = os.path.dirname(os.path.abspath(target))
    F = json.load(open(os.path.join(task, "generator", "figures.json")))
    # documents, with positive controls through the same extractor
    terms = text(find(target, r"review_program_terms"))
    report = text(find(target, r"annual_report"))
    sched = text(find(target, r"visit_schedule"))
    check("five-year steps from 40 to 70 years" in terms, "terms: the settings (4.1) read back")
    check("at least nine in ten of the mesotheliomas" in terms and "whenever it is diagnosed" in terms,
          "terms: the horizon's estimand (4.2) reads back")
    check("365.25 days to a year" in terms and "without assuming a shape" in terms, "terms: 4.3 and 4.4 read back")
    check("since the Fund began on 1 July 2004" in report and "every mesothelioma diagnosed to 30 June 2026" in report,
          "report: the register's start and close read back")
    # the register, both layouts
    cur = pd.read_csv(find(target, r"register_2013"), dtype=str, keep_default_na=False)
    leg = pd.read_excel(find(target, r"register_2004"), sheet_name="Register", header=3, dtype=str).fillna("")
    expo = {"OCC": "Occupational", "DOM": "Domestic", "ENV": "Environmental", "NIL": "No exposure identified"}
    reg = pd.concat([
        pd.DataFrame({"ref": cur["fund_ref"], "D": pd.to_datetime(cur["date_of_diagnosis"]), "cat": cur["exposure_category"]}),
        pd.DataFrame({"ref": leg["Ref"].str.replace("DD/", "DD", regex=False).str.replace("/", "-", regex=False),
                      "D": pd.to_datetime(leg["Date diagnosed"], format="%d-%b-%Y"), "cat": leg["Exposure"].map(expo)})])
    check(reg["D"].min() >= START and reg["D"].max() <= END, "register: every diagnosis inside the window")
    h = pd.read_csv(find(target, r"occupational_histories"), dtype=str, keep_default_na=False)
    iso = h["started"].str.match(r"^\d{4}-\d{2}-\d{2}$")
    h["start"] = pd.to_datetime(h["started"].where(iso), format="%Y-%m-%d").fillna(
        pd.to_datetime(h["started"].where(~iso), format="%d-%b-%Y"))
    ex = h[h["asbestos_exposure"].isin(["Y", "Yes"])].groupby("case_ref")["start"].min()
    reg["E"] = reg["ref"].map(ex)
    sc = reg[(reg["cat"] == "Occupational") & reg["E"].notna() & (reg["E"] < COHORT)]
    check(len(sc) == F["cases_in_estimate"], "estimate: %d cases (figures.json %d)" % (len(sc), F["cases_in_estimate"]))
    t = (sc["D"] - sc["E"]).dt.days.to_numpy(float)
    u = (START - sc["E"]).dt.days.to_numpy(float)
    v = (END - sc["E"]).dt.days.to_numpy(float)
    x, f = ep(t, u, v)
    share = {H: float(f[x <= H * YEAR].sum()) for H in SETTINGS}
    call = next(H for H in SETTINGS if share[H] >= 0.9)
    check(call == F["call"], "call: %d years (figures.json %d)" % (call, F["call"]))
    for H in SETTINGS:
        got = float("%.1f" % (round(share[H] * 1000 + 1e-9) / 10))
        check(got == F["share"][str(H)], "share within %d years %.1f (figures.json %.1f)" % (H, got, F["share"][str(H)]))
    emp = {H: float((t <= H * YEAR).mean()) for H in SETTINGS}
    check(next(H for H in SETTINGS if emp[H] >= 0.9) == 55, "rung 0: the register read as it stands files 55")
    # the program: published schedule (parsed from the PDF), appointments, members, card, QA log
    months = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                          "September", "October", "November", "December"], 1)}
    pub = {}
    for a, b, mon, yr, town in re.findall(r"(\d{1,2})-(\d{1,2}) ([A-Z][a-z]+) (\d{4}) ([A-Z][a-z]+)", sched):
        for dday in range(int(a), int(b) + 1):
            d = pd.Timestamp(dt.date(int(yr), months[mon], dday))
            if d.weekday() < 5:
                pub[d] = town
    for a, m1, b, m2, yr, town in re.findall(r"(\d{1,2}) ([A-Z][a-z]+) - (\d{1,2}) ([A-Z][a-z]+) (\d{4}) ([A-Z][a-z]+)", sched):
        d = pd.Timestamp(dt.date(int(yr) if months[m1] <= months[m2] else int(yr) - 1, months[m1], int(a)))
        e = pd.Timestamp(dt.date(int(yr), months[m2], int(b)))
        while d <= e:
            if d.weekday() < 5:
                pub[d] = town
            d += pd.Timedelta(days=1)
    ap = pd.read_csv(find(target, r"review_appointments"), dtype=str, keep_default_na=False)
    ap["date"] = pd.to_datetime(ap["appointment_date"])
    fy = ap[(ap["date"] >= FY0) & (ap["date"] <= FY1)]
    unit = fy[fy["site"] == "MRU"]
    check(set(unit["date"]) <= set(pub), "schedule: every unit working day is on the published schedule")
    card = pd.read_excel(find(target, r"card_statement"), sheet_name="Transactions", header=3, dtype=str)
    card["Date"] = pd.to_datetime(card["Date"])
    qa = []
    for sh, hd, fmt in (("Jul-Dec 2025", ["Date", "Counter start", "Counter end", "Constancy exposures"], "%d/%m/%Y"),
                        ("Jan-Jun 2026", ["Date", "Exposure count (start)", "Exposure count (end)", "QC exposures"],
                         "%Y-%m-%d")):
        q = pd.read_excel(find(target, r"xray_qa_log"), sheet_name=sh, header=2, dtype=str)[hd]
        q.columns = ["Date", "s", "e", "qc"]
        q["Date"] = pd.to_datetime(q["Date"], format=fmt)
        qa.append(q)
    qa = pd.concat(qa).set_index("Date")
    town_rev, offline = {}, set()
    for d, rows in unit.groupby("date"):
        att = int((rows["attendance"] == "Attended").sum())
        blank = int((rows["attendance"] == "").sum())
        q = qa.loc[d]
        n = (int(q["e"]) - int(q["s"]) - int(q["qc"])) / 2
        both = att + blank <= n <= (att + blank) * 1.08 + 1.5
        alone = att <= n <= att * 1.08 + 1.5
        check(both != alone, "counter %s: one reading (attended %d, blank %d, counter %.1f)" % (d.date(), att, blank, n))
        reviewed = att + (blank if both else 0)
        if both:
            offline.add(d)
        noon = card[(card["Date"] == d) & (card["Time"] >= "11:30") & (card["Time"] <= "14:00")]
        town = noon["Location"].iloc[0] if len(noon["Location"].unique()) == 1 else pub[d]
        town_rev[town] = town_rev.get(town, 0) + reviewed
    for town, n in sorted(F["reviews"].items()):
        check(town_rev.get(town, 0) == n, "unit reviews in %s: %d (figures.json %d)" % (town, town_rev.get(town, 0), n))
    mem = pd.read_csv(find(target, r"program_members"), dtype=str, keep_default_na=False).set_index("member_no")
    seen = set(fy[fy["attendance"] == "Attended"]["member_no"]) | set(
        unit[(unit["attendance"] == "") & unit["date"].isin(offline)]["member_no"])
    yrs = (TERM - pd.to_datetime(mem.loc[sorted(seen), "first_exposure"])).dt.days / YEAR
    for H in [45, 50, 55, 60, 65, 70]:
        n = int((yrs < H).sum())
        check(n == F["members"][str(H)], "members inside %d years on 1 July 2027: %d (figures.json %d)"
              % (H, n, F["members"][str(H)]))
    # the goldens read back
    gold = os.path.join(task, "golden")
    wb = pd.read_excel(os.path.join(gold, "review_horizon_workbook_2027.xlsx"), sheet_name=None, header=None)
    hz = wb["Horizon"]
    for H in SETTINGS:
        row = hz[hz[0] == H]
        check(len(row) == 1 and abs(float(row[1].iloc[0]) - F["share"][str(H)]) < 1e-9, "workbook: the %d-year share" % H)
    import docx
    para = " ".join(p.text for p in docx.Document(os.path.join(gold, "review_horizon_board_paper_2027.docx")).paragraphs)
    check("Set the horizon at %d years" % F["call"] in para, "board paper: the call reads back")
    print("verify: %d failed" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main(sys.argv[1])

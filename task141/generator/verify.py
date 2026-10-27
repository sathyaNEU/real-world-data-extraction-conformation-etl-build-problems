"""An independent path from the cut pack to the graded figures: pandas readers of its own, county time from the IANA
zone rather than the generator's offsets, completed years and calendar months from dateutil, and the deliverables read
back, every figure compared with generator/figures.json and submission.md.

    python3 task141/generator/verify.py
"""
import datetime as dt
import json
import math
import os
import re
import sys
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
sys.path.insert(0, HERE)

import common as K    # noqa: E402
import forecast as F  # noqa: E402
import golden as G    # noqa: E402

CHI = ZoneInfo("America/Chicago")
EXTRACT = dt.date(2026, 9, 30)
QUARTERS = [(dt.date(2025, 10, 1), dt.date(2025, 12, 31)), (dt.date(2026, 1, 1), dt.date(2026, 3, 31)),
            (dt.date(2026, 4, 1), dt.date(2026, 6, 30)), (dt.date(2026, 7, 1), dt.date(2026, 9, 30))]
RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append(bool(ok))
    print("%s  %-60s %s" % ("PASS" if ok else "FAIL", label, detail))


def csv(name, **kw):
    return pd.read_csv(os.path.join(TARGET, name), dtype=str, keep_default_na=False, **kw)


def local_time(s):
    if not s:
        return None
    if s.endswith("Z"):
        u = dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
        return u.astimezone(CHI).replace(tzinfo=None)
    return dt.datetime.strptime(s, "%m/%d/%Y %H:%M")


def terms():
    c1 = csv(K.CMS1)
    c1 = pd.DataFrame(dict(case=c1.CASE_NO, person=c1.APD_PERSON_NO, level=c1.LEVEL, office=c1.OFFICE.map(
        {"C": "CEN", "N": "NGT", "R": "RVS", "E": "EFD"}), sup=pd.to_datetime(c1.SUP_BEGIN, format="%m/%d/%Y"),
        months=(c1.TERM_DAYS.astype(int) / 30.4375).round().astype(int), exp=pd.to_datetime(c1.EXPIRES, format="%m/%d/%Y"),
        status="CLOSED", closed=pd.to_datetime(c1.CLOSE_DATE, format="%m/%d/%Y")))
    c2 = csv(K.CMS2)
    c2 = pd.DataFrame(dict(case=c2.case_number, person=c2.person_id, level=c2.offense_level.str[0], office=c2.office,
                           sup=pd.to_datetime(c2.supervision_begin), months=c2.term_months.astype(int),
                           exp=pd.to_datetime(c2.expiration_date), status=c2.case_status,
                           closed=pd.to_datetime(c2.closed_date.replace("", None))))
    return pd.concat([c1, c2], ignore_index=True)


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    T = terms()
    orders = csv(K.ORDERS)
    pets = csv(K.PETITIONS)
    ext = orders[orders.order_type == "EXTENSION"].groupby("case_number").months_extended.apply(
        lambda s: s.astype(int).sum())
    T["imposed"] = T.months - T.case.map(ext).fillna(0).astype(int)
    lvl = dict(zip(T.case, T.level))
    who = dict(zip(T.case, T.person))

    # ------------------------------------------------------------------ the Act on the open felony terms
    open_f = T[(T.level == "F") & (T.status == "OPEN")]
    cap = open_f.sup.apply(lambda d: (d + relativedelta(months=24)).date())
    trans = int(((open_f.exp.dt.date > dt.date(2027, 3, 31)) & (cap <= dt.date(2027, 3, 31))).sum())
    check("the Act ends this many open felony terms on 31 March 2027", trans == figs["transition_terms"],
          "%d" % trans)
    check("open felony terms at the extract", len(open_f) == figs["open_felony_terms"], "%d" % len(open_f))

    # ------------------------------------------------------------------ the trailing year's admissions
    rv = pets[(pets.disposition == "REVOKED") & (pets.case_number.map(lvl) == "F")].copy()
    rv["d"] = pd.to_datetime(rv.disposition_date).dt.date
    rv["person"] = rv.case_number.map(who)
    tr = rv[(rv.d > dt.date(2025, 9, 30)) & (rv.d <= EXTRACT)].drop_duplicates(["person", "d"])
    check("felony revocation admissions, October 2025 to September 2026", len(tr) == figs["trailing.felony_admissions"],
          "%d" % len(tr))

    # ------------------------------------------------------------------ the projection through a reader of this file's own
    R = F.Rec()
    fel = T[T.level == "F"].sort_values(["sup", "case"])
    R.cases = [dict(id=r.case, sup=K.day(r.sup.date()), score=0, term=int(r.imposed)) for r in fel.itertuples()]
    score = {}
    for r in csv(K.CMS1).itertuples():
        score[r.CASE_NO] = int(r.RISK_SCORE) // 2
    for r in csv(K.CMS2).itertuples():
        score[r.case_number] = int(r.csrs_score)
    for c in R.cases:
        c["score"] = score[c["id"]]
    R.C = {c["id"]: c for c in R.cases}
    o = orders[(orders.order_type != "EARLY TERMINATION") & orders.case_number.isin(R.C)]
    R.scheds, R.sched_now, R.close = {}, {}, {}
    first = o.groupby("case_number").expiration_before.first()
    for r in fel.itertuples():
        R.scheds[r.case] = [(-10 ** 6, K.day(dt.date.fromisoformat(first[r.case])) if r.case in first.index
                             else K.day(r.exp.date()))]
    for r in o.itertuples():
        d, v = K.day(dt.date.fromisoformat(r.order_date)), K.day(dt.date.fromisoformat(r.expiration_after))
        s = R.scheds[r.case_number]
        s[-1:] = [(d, v)] if s[-1][0] == d else [s[-1], (d, v)]
    reason = {"EXPIRED": "EXPIRED", "EXP": "EXPIRED", "REVOKED": "REVOKED", "REV": "REVOKED",
              "EARLY TERMINATION": "EARLY_TERM", "ETERM": "EARLY_TERM"}
    c1 = csv(K.CMS1)
    c2 = csv(K.CMS2)
    for r in c1.itertuples():
        if r.LEVEL == "F":
            R.close[r.CASE_NO] = (K.day(dt.datetime.strptime(r.CLOSE_DATE, "%m/%d/%Y").date()), reason[r.CLOSE_CODE])
    for r in c2.itertuples():
        if r.offense_level == "FELONY" and r.closed_date:
            R.close[r.case_number] = (K.day(dt.date.fromisoformat(r.closed_date)), reason[r.closure_reason])
    for k, s in R.scheds.items():
        R.sched_now[k] = s[-1][1]
    R.pet, R.byc = [], {}
    for r in pets[pets.case_number.isin(R.C)].itertuples():
        q = dict(case=r.case_number, file=K.day(dt.date.fromisoformat(r.filed_date)),
                 decided=K.day(dt.date.fromisoformat(r.disposition_date)) if r.disposition_date else None,
                 revoked=(r.disposition == "REVOKED") if r.disposition_date else None)
        R.pet.append(q)
        R.byc.setdefault(q["case"], []).append(q)
    F.finish(R)
    tot = F.two_clock(R, **G.GOLD)[0]
    check("the 2027 projection through this reader", abs(tot - figs["call.admissions_unrounded"]) < 0.05, "%.1f" % tot)
    check("pods by the standard (one per 220 or part)", math.ceil(tot / 220) == figs["call.pods"] == 6)
    check("the plan figure to the nearest 100", int(math.floor(tot / 100 + 0.5)) * 100 == figs["call.admissions"])

    # ------------------------------------------------------------------ Ask A, bed-days
    b = csv(K.BOOKINGS)
    xw = csv(K.PERSONS)
    so2p = dict(zip(xw.sheriff_id, xw.apd_person_id))
    b["start"] = b.booked_at.map(local_time)
    b["end"] = b.released_at.map(local_time)
    b["person"] = b.sheriff_id.map(so2p)
    rv_all = pets[pets.disposition == "REVOKED"].copy()
    rv_all["person"] = rv_all.case_number.map(who)
    rv_all["level"] = rv_all.case_number.map(lvl)
    rev = {}
    for r in rv_all.itertuples():
        rev.setdefault((r.person, r.disposition_date), set()).add(r.level)
    weekend = {}
    for r in rv_all[rv_all.served_as == "WEEKENDS"].itertuples():
        weekend.setdefault(r.person, []).append((r.disposition_date, r.level))
    tab = np.zeros((4, 2), dtype=int)
    stop = dt.datetime(2026, 10, 1)
    for person, g in b[b.classification != "PV-OOS"].groupby(b.person.fillna(b.sheriff_id)):
        g = g.sort_values("start")
        prev, prev_level = None, None
        for r in g.itertuples():
            level = None
            if r.classification in ("PV-FEL", "PV-MIS"):
                cont = prev is not None and prev.classification == r.classification and not pd.isna(prev.end) and (
                    prev.end == r.start or (prev.release_reason == "TRANSFER TO ANNEX" and
                                            0 < (r.start - prev.end).total_seconds() <= 7200))
                if cont:
                    level = prev_level
                elif r.classification == "PV-MIS":
                    level = "M"
                else:
                    day = rev.get((person, r.start.date().isoformat()))
                    if day:
                        level = "F" if "F" in day else "M"
                    else:
                        wk = [x for x in weekend.get(person, []) if x[0] < r.start.date().isoformat()]
                        level = max(wk)[1] if wk else "F"
                end = stop if pd.isna(r.end) else r.end
                midnight = dt.datetime.combine(r.start.date() + dt.timedelta(days=1), dt.time())
                while midnight < end:
                    for qi, (a, z) in enumerate(QUARTERS):
                        if a <= midnight.date() <= z:
                            tab[qi, 0 if level == "F" else 1] += 1
                    midnight += dt.timedelta(days=1)
            prev, prev_level = r, level
    ok = all(tab[i, 0] == figs["ask_a.q%d.felony" % (i + 1)] and tab[i, 1] == figs["ask_a.q%d.misdemeanor" % (i + 1)]
             for i in range(4))
    check("Ask A: violator bed-days by quarter", ok, str(tab.tolist()))

    # ------------------------------------------------------------------ Ask B, imposed terms
    def band(sup):
        s = sup.date()
        years = EXTRACT.year - s.year - ((EXTRACT.month, EXTRACT.day) < (s.month, s.day))
        return min(years, 3)
    of = open_f.copy()
    of["imposed"] = T.loc[of.index, "imposed"]
    of["band"] = of.sup.map(band)
    by_off = of.groupby("office").imposed.mean()
    by_band = of.groupby("band").imposed.mean()
    r1 = lambda v: math.floor(v * 10 + 0.5) / 10   # noqa: E731
    ok = all(r1(by_off[code]) == figs["ask_b.office.%s" % code] for code in ("CEN", "NGT", "RVS", "EFD")) and all(
        r1(by_band[k]) == figs["ask_b.band%d" % k] for k in range(4))
    check("Ask B: average term imposed by office and time on supervision", ok, " ".join(
        "%.3f" % v for v in list(by_off[["CEN", "NGT", "RVS", "EFD"]]) + list(by_band)))

    # ------------------------------------------------------------------ the deliverables
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(GOLDEN, K.GOLD_BOOK), data_only=True)
    vals = [c for ws in wb for row in ws.iter_rows(values_only=True) for c in row if c is not None]
    check("workbook: the plan figure and the pods", figs["call.admissions"] in vals and figs["call.pods"] in vals)
    ws = wb["Bed-days 2025-26"]
    rows = [r for r in ws.iter_rows(values_only=True) if r and isinstance(r[1], int)]
    check("workbook: the bed-days sheet carries Ask A", [list(r[1:3]) for r in rows[:4]] == tab.tolist())
    ws = wb["Felony supervision"]
    got = [float(r[2]) for r in ws.iter_rows(values_only=True) if r and isinstance(r[1], int) and
           isinstance(r[2], (int, float))]
    want = [figs["ask_b.office.%s" % c] for c in ("CEN", "NGT", "RVS", "EFD")] + [figs["ask_b.band%d" % k]
                                                                                  for k in range(4)]
    check("workbook: the supervision sheet carries Ask B", got[:8] == want, str(got[:8]))
    import docx
    memo = "\n".join(p.text for p in docx.Document(os.path.join(GOLDEN, K.GOLD_MEMO)).paragraphs)
    check("memo: the call and its figures", all(s in memo for s in ("six violator pods", "{:,}".format(
        figs["call.admissions"]), "{:,}".format(figs["transition_terms"]), "{:,}".format(figs["ask_a.q1.felony"]))))
    check("memo: no em or en dash", not re.search("[–—]", memo))
    check("chart: written", os.path.getsize(os.path.join(GOLDEN, K.GOLD_CHART)) > 50000)

    # ------------------------------------------------------------------ the write-up
    for key in ("transition_terms", "ask_a.q1.felony", "ask_a.q4.misdemeanor", "trailing.felony_admissions"):
        check("submission: %s stated as computed" % key, "{:,}".format(figs[key]) in sub)
    check("submission: the plan figure and pods", "carry 1,200" in sub and "staff 6 violator pods" in sub)
    print("\n%d of %d verified" % (sum(RESULTS), len(RESULTS)))
    return 0 if all(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())

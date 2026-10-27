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
    c1 = pd.DataFrame(dict(case=c1.CASE_NO, person=c1.APD_PERSON_NO, level=c1.LEVEL, klass=c1.OFF_CLASS.str.replace(
        "-", "", regex=False), officer="", office=c1.OFFICE.map(
        {"C": "CEN", "N": "NGT", "R": "RVS", "E": "EFD"}), sup=pd.to_datetime(c1.SUP_BEGIN, format="%m/%d/%Y"),
        months=(c1.TERM_DAYS.astype(int) / 30.4375).round().astype(int), exp=pd.to_datetime(c1.EXPIRES, format="%m/%d/%Y"),
        status="CLOSED", closed=pd.to_datetime(c1.CLOSE_DATE, format="%m/%d/%Y")))
    c2 = csv(K.CMS2)
    c2 = pd.DataFrame(dict(case=c2.case_number, person=c2.person_id, level=c2.offense_level.str[0],
                           klass=c2.offense_class, officer=c2.officer, office=c2.intake_office,
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
    cls = pd.read_excel(os.path.join(TARGET, K.COURT_CODES), sheet_name="Offense classes", header=2)
    cls = cls[pd.to_numeric(cls.iloc[:, 2], errors="coerce").notna()]
    cmax = dict(zip(cls.iloc[:, 0], cls.iloc[:, 2].astype(int)))
    ex = orders[orders.order_type == "EXTENSION"]
    exts = {}
    for r in ex.itertuples():
        exts.setdefault(r.case_number, []).append((K.day(dt.date.fromisoformat(r.order_date)), int(r.months_extended)))
    R.cases = [dict(id=r.case, sup=K.day(r.sup.date()), score=0, term=int(r.imposed), klass=r.klass,
                    max_m=cmax[r.klass], imposed_term=int(r.imposed), exts=sorted(exts.get(r.case, [])))
               for r in fel.itertuples()]
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
    tot = F.projection(R, **G.GOLD)[0]
    check("the 2027 projection through this reader", abs(tot - figs["call.admissions_unrounded"]) < 0.05, "%.1f" % tot)
    check("pods by the standard (one per 210 or part)", math.ceil(tot / 210) == figs["call.pods"] == 7)
    check("the projection inside seven pods' band (more than 1,260, at most 1,470)", 6 * 210 < tot <= 7 * 210)

    # ------------------------------------------------------------------ the end-of-term split, written afresh
    pf = {}
    for r in pets[pets.case_number.isin(R.C)].itertuples():
        pf.setdefault(r.case_number, []).append(dt.date.fromisoformat(r.filed_date))
    xo = {}
    for r in ex.itertuples():
        xo.setdefault(r.case_number, []).append((dt.date.fromisoformat(r.order_date), int(r.months_extended)))
    first_day = dt.date(2016, 7, 1)
    tab = {True: [0, 0, 0], False: [0, 0, 0]}
    for c in R.cases:
        sch = R.scheds[c["id"]]
        end = K.date_of(R.close[c["id"]][0]) if c["id"] in R.close else EXTRACT + dt.timedelta(days=1)
        for i, (since, s_) in enumerate(sch):
            until = sch[i + 1][0] if i + 1 < len(sch) else 10 ** 9
            exp = K.date_of(s_)
            wo = exp - dt.timedelta(days=120)
            if exp > EXTRACT - dt.timedelta(days=30) or wo < first_day or not (since <= K.day(wo) < until):
                continue
            if end <= wo or K.date_of(c["sup"]) > wo:
                continue
            term_then = c["imposed_term"] + sum(m for d, m in xo.get(c["id"], []) if d < wo)
            at_max = term_then >= c["max_m"]
            tab[at_max][0] += 1
            tab[at_max][1] += any(wo <= d < exp for d in pf.get(c["id"], []))
            tab[at_max][2] += any(wo <= d < exp for d, _ in xo.get(c["id"], []))
    check("end-of-term windows at the class maximum and their petitions", tab[True][:2] == [
        figs["rate.windows_at_max"], figs["rate.petitions_at_max"]], str(tab[True]))
    check("end-of-term windows with room, their petitions and extensions", tab[False][:2] == [
        figs["rate.windows_with_room"], figs["rate.petitions_with_room"]] and round(
        100 * tab[False][2] / tab[False][0], 1) == figs["rate.extended_with_room_pct"], str(tab[False]))

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
    rv_all["d"] = pd.to_datetime(rv_all.disposition_date).dt.date
    orders_by = {}
    for r in rv_all.itertuples():
        orders_by.setdefault(r.person, []).append((r.d, r.level, r.served_as))
    stop = dt.datetime(2026, 10, 1)
    night = {}

    def mark(person, first, end, level):
        m = dt.datetime.combine(first, dt.time())
        while m < end:
            if night.get((person, m.date())) != "F":
                night[(person, m.date())] = level
            m += dt.timedelta(days=1)
    for person, g in b[b.classification != "PV-OOS"].groupby(b.person.fillna(b.sheriff_id)):
        g = g.sort_values("start")
        od = orders_by.get(person, [])
        prev, run = None, None
        for r in g.itertuples():
            end = stop if pd.isna(r.end) else r.end
            if r.classification in ("PV-FEL", "PV-MIS"):
                cont = run is not None and prev.classification == r.classification and not pd.isna(prev.end) and (
                    prev.end == r.start or (prev.release_reason == "TRANSFER TO ANNEX" and
                                            0 < (r.start - prev.end).total_seconds() <= 7200))
                if cont:
                    mark(person, r.start.date() + dt.timedelta(days=1), end, run)
                    prev = r
                    continue
                day0 = r.start.date()
                held = prev is not None and not pd.isna(prev.end) and prev.end == r.start and \
                    prev.release_reason == "RECLASSIFIED"
                same = [o for o in od if o[0] == day0 and o[2] == "CONSECUTIVE"]
                near = [o[0] for o in od if day0 - dt.timedelta(days=8) <= o[0] < day0 and o[2] == "CONSECUTIVE"]
                order = day0 if same else (max(near) if held and near else None)
                if order is not None:
                    level = "F" if any(o[1] == "F" for o in od if o[0] == order) else "M"
                else:
                    wk = sorted(o for o in od if o[2] == "WEEKENDS" and o[0] < day0)
                    level = wk[-1][1] if wk else "F"
                if r.classification == "PV-MIS":
                    level = "M"
                first = (order if held and order is not None else day0) + dt.timedelta(days=1)
                mark(person, first, end, level)
                run = level
            else:
                run = None
                if r.classification == "PV-HOLD" and pd.isna(r.end):
                    od2 = sorted(o for o in od if o[0] >= r.start.date() and o[2] == "CONSECUTIVE")
                    if od2:
                        level = "F" if any(o[1] == "F" for o in od if o[0] == od2[-1][0]) else "M"
                        mark(person, od2[-1][0] + dt.timedelta(days=1), stop, level)
            prev = r
    tab = np.zeros((4, 2), dtype=int)
    for (person, d), level in night.items():
        for qi, (a, z) in enumerate(QUARTERS):
            if a <= d <= z:
                tab[qi, 0 if level == "F" else 1] += 1
    ok = all(tab[i, 0] == figs["ask_a.q%d.felony" % (i + 1)] and tab[i, 1] == figs["ask_a.q%d.misdemeanor" % (i + 1)]
             for i in range(4))
    check("Ask A: violator bed-days by quarter", ok, str(tab.tolist()))

    # ------------------------------------------------------------------ Ask B, probationers by supervising office
    def band(sup):
        s = sup.date()
        years = relativedelta(EXTRACT, s).years
        return min(years, 3)
    ro = csv(K.ROSTER)
    ro["a"] = pd.to_datetime(ro.assigned_from, format="%d-%b-%Y")
    ro["z"] = pd.to_datetime(ro.assigned_to.replace("", None), format="%d-%b-%Y")
    on = ro[(ro.a <= pd.Timestamp(EXTRACT)) & (ro.z.isna() | (ro.z >= pd.Timestamp(EXTRACT)))]
    office_of = dict(zip(on.badge_no, on.office_code))
    of = open_f.copy()
    of["sup_office"] = of.officer.map(office_of)
    of["band"] = of.sup.map(band)
    grid = of.groupby(["sup_office", "band"]).size()
    ok = all(int(grid.get((code, k), 0)) == figs["ask_b.%s.band%d" % (code, k)] for code in ("CEN", "NGT", "RVS", "EFD")
             for k in range(4)) and of.sup_office.notna().all()
    check("Ask B: felony probationers by supervising office and time on supervision", ok, " ".join(
        str(int(grid.get((code, k), 0))) for code in ("CEN", "NGT", "RVS", "EFD") for k in range(4)))

    # ------------------------------------------------------------------ the deliverables
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(GOLDEN, K.GOLD_BOOK), data_only=True)
    vals = [c for ws in wb for row in ws.iter_rows(values_only=True) for c in row if c is not None]
    check("workbook: the projection and the pods", figs["call.admissions_whole"] in vals and figs["call.pods"] in vals)
    ws = wb["Bed-days 2025-26"]
    rows = [r for r in ws.iter_rows(values_only=True) if r and isinstance(r[1], int)]
    check("workbook: the bed-days sheet carries Ask A", [list(r[1:3]) for r in rows[:4]] == tab.tolist())
    ws = wb["Felony supervision"]
    got = [list(r[1:5]) for r in ws.iter_rows(values_only=True) if r and isinstance(r[1], int)][:4]
    want = [[figs["ask_b.%s.band%d" % (c, k)] for k in range(4)] for c in ("CEN", "NGT", "RVS", "EFD")]
    check("workbook: the supervision sheet carries Ask B", got == want, str(got))
    ws = wb["End of term"]
    got = [list(r[1:3]) for r in ws.iter_rows(values_only=True) if r and isinstance(r[1], int) and
           isinstance(r[2], int)][:2]
    check("workbook: the end-of-term sheet carries the split", got == [
        [figs["rate.windows_at_max"], figs["rate.petitions_at_max"]],
        [figs["rate.windows_with_room"], figs["rate.petitions_with_room"]]], str(got))
    import docx
    memo = "\n".join(p.text for p in docx.Document(os.path.join(GOLDEN, K.GOLD_MEMO)).paragraphs)
    check("memo: the call and its figures", all(s in memo for s in ("seven violator pods", "{:,}".format(
        figs["call.admissions_whole"]), "{:,}".format(figs["transition_terms"]), "{:,}".format(figs["ask_a.q1.felony"]),
        "{:,}".format(figs["rate.petitions_at_max"]))))
    words = {3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}
    r10 = lambda x: "{:,}".format(int(round(x / 10.0)) * 10)
    check("memo: each wrong rung's pods under the standard", all(s in memo for s in (
        "about %s admissions and %s pods" % (r10(figs["rung.pooled"]), words[figs["rung.pooled.pods"]]),
        "about %s (%s pods)" % (r10(figs["rung.iia"]), words[figs["rung.iia.pods"]]),
        "about %s (%s)" % (r10(figs["rung.full"]), words[figs["rung.full.pods"]]))) and all(
        -(-figs["rung.%s" % k] // figs["pod_size"]) == figs["rung.%s.pods" % k] for k in ("pooled", "iia", "full")))
    check("memo: no em or en dash", not re.search("[–—]", memo))
    check("chart: written", os.path.getsize(os.path.join(GOLDEN, K.GOLD_CHART)) > 50000)

    # ------------------------------------------------------------------ the write-up
    for key in ("transition_terms", "ask_a.q1.felony", "ask_a.q4.misdemeanor", "trailing.felony_admissions",
                "ask_b.EFD.band3", "rung.pooled", "family.low", "family.high"):
        check("submission: %s stated as computed" % key, "{:,}".format(figs[key]) in sub)
    check("submission: the pods, with no plan figure rounded from the projection",
          "staff 7 violator pods" in sub and not re.search(r"(?i)nearest 100", sub))
    check("submission: the projection stated as the band seven pods cover", "more than 1,260" in sub and "1,470" in sub)
    print("\n%d of %d verified" % (sum(RESULTS), len(RESULTS)))
    return 0 if all(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())

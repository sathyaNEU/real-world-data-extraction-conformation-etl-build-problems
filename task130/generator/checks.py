"""Assertions over the built pack. Exits non-zero on any failure."""
import os
import sys

import numpy as np
import pandas as pd
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import estimators as E
from build import FILES, DISTRACTORS, TASK

N = {"n": 0}
FAIL = []


def check(cond, msg):
    N["n"] += 1
    if not cond:
        FAIL.append(msg)


def last(r):
    return tuple(int(round(r[s][-1])) for s in E.SIZES)


def cells(r):
    return [int(round(r[s][k])) for s in E.SIZES for k in range(6)]


def run(target=None):
    T = target or os.path.join(TASK, "target")
    c, pl, rv, mb, lt = E.load(T)
    hh = E.households(mb)
    P = E.plan(T)
    P0 = E.plan(T, "Original Mar 2026")
    gold = E.golden(T)
    g = last(gold)
    gt = sum(g)
    th = sorted(E.tenter_house(pl))

    # ---- input gates ----
    files = sorted(os.listdir(T))
    check(len(files) >= 10, "fewer than 10 files")
    check(len({os.path.splitext(f)[1] for f in files}) >= 3, "fewer than 3 formats")
    check(len(pl) >= 25000, "spine under 25,000 rows")
    check(len(DISTRACTORS) >= 2, "fewer than 2 distractors")
    for k in FILES:
        check(FILES[k] in files, "missing " + FILES[k])
    check(not any("distract" in f.lower() or "golden" in f.lower() for f in files), "a telling file name")

    # ---- keys and integrity ----
    check(c["case_ref"].is_unique, "case_ref repeats")
    for name, df in (("placement", pl), ("let", lt), ("review", rv), ("member", mb)):
        check(set(df["case_ref"]) <= set(c["case_ref"]), "a %s without a case" % name)
    check(lt["case_ref"].is_unique, "a case let twice")
    open_refs = set(c.loc[c["case_status"] == "Open", "case_ref"])
    check(set(mb["case_ref"]) == open_refs, "members do not cover exactly the open cases")
    first = mb[mb["member_no"] == "1"]
    check((first["relationship"] == "Applicant").all() and len(first) == len(open_refs), "member 1 is not the applicant")
    s = pl.sort_values(["case_ref", "placement_start"], kind="mergesort")
    nxt = s.groupby("case_ref")["placement_start"].shift(-1)
    check(((s["placement_end"].isna() & nxt.notna())).sum() == 0, "an open placement followed by another")
    check(((s["placement_end"] > nxt) & nxt.notna()).sum() == 0, "overlapping placements")
    u = pl[pl["accommodation_type"].isin(["Tenter House", "Private sector lease", "Nightly-paid self-contained"])]
    u = u.sort_values(["unit_ref", "placement_start"], kind="mergesort")
    nu = u.groupby("unit_ref")["placement_start"].shift(-1)
    check(((u["placement_end"].fillna(pd.Timestamp("2099-01-01")) > nu) & nu.notna()).sum() == 0, "two households in one unit")
    ci = c.set_index("case_ref")
    check(all(ci.loc[th, "decision"] == "Main duty accepted"), "an interim-duty household in Tenter House")
    check(all(ci.loc[th, "case_status"] == "Open"), "a closed case in Tenter House")
    th_starts = pl[pl["accommodation_type"] == "Tenter House"]["placement_start"]
    check((th_starts >= pd.Timestamp("2026-09-15")).sum() == 0, "a placement into Tenter House after the notice")
    # every offer is made on a round day: the third Monday of the month before the tenancy starts
    rd = lt["tenancy_start"].map(lambda t: E.round_date(t.replace(day=1)))
    check((rd == lt["offer_date"]).all(), "an offer off its round day")
    acc = lt[lt["let_status"] == "Accepted, tenancy to start"]
    check((acc["offer_date"] == pd.Timestamp("2026-09-21")).all() and (acc["tenancy_start"].dt.month == 10).all(),
          "an accepted let outside the September round")
    # the plan's April to September actuals and its October column tie to the lets log
    ws = openpyxl.load_workbook(os.path.join(T, FILES["plan"]))["Revised 14 Sep 2026"]
    st = lt[lt["let_status"] == "Tenancy started"]
    for r, sz in zip(range(5, 10), [1, 2, 3, 4, 5]):
        b = st["bedrooms"].clip(upper=5)
        for j, m in enumerate(range(4, 10)):
            n = int(((b == sz) & (st["tenancy_start"].dt.to_period("M") == pd.Period("2026-%02d" % m))).sum())
            check(ws.cell(row=r, column=2 + j).value == n, "plan actuals %d-bed month %d" % (sz, m))
        check(P[sz][0] == int((acc["bedrooms"].clip(upper=5) == sz).sum()), "plan October %d-bed is not the September round" % sz)
    check(all(v == 0 for v in P[5][1:]), "five-bedroom lets planned after October")
    check(all(sum(P[sz]) == sum(P0[sz]) for sz in (1, 2)), "rephasing moved a one- or two-bed half-year total")
    check(any(P[sz] != P0[sz] for sz in (1, 2)), "rephasing changed nothing")

    # ---- the list rule: Part 3 need on the round day, from the application ----
    h, t = E.replay(c, rv, lt, need="part3", hh=hh, since=pd.Timestamp("2026-09-01"))
    check(h == t and t > 0, "Part 3 need reproduces %d of %d September-round lets" % (h, t))
    hr, tr = E.replay(c, rv, lt, since=pd.Timestamp("2026-09-01"))
    check(hr < tr, "the case record's need reproduces every September-round let")
    hall, tall = E.replay(c, rv, lt)
    check(hall / tall < 0.9, "the case record's need reproduces %.3f of all lets" % (hall / tall))

    # ---- maturity: after day 120 of the duty a household leaves only by a let ----
    accd = c[(c["decision"] == "Main duty accepted") & (c["case_status"] == "Closed")
             & (c["closed_date"] >= pd.Timestamp("2018-04-01"))]
    late = accd[((accd["closed_date"] - accd["decision_date"]).dt.days > 120)
                & ~accd["closure_reason"].str.startswith("Settled")]
    check(len(late) == 0, "%d main-duty cases closed after day 120 other than by a let" % len(late))

    # ---- every round's cut: past day 120, and no same-day tie mixing Tenter House and other households ----
    q = E.open_main(c, E.ASOF).sort_values(["decision_date", "case_ref"], kind="mergesort")
    refs = q["case_ref"].tolist()
    dec = q["decision_date"].values
    isth = np.isin(refs, th)
    gone = np.isin(refs, list(E.accepted_october(lt)))
    for k, m in enumerate(E.TENANCY_MONTHS):
        day = E.round_date(m)
        nd = E.part3(hh, refs, day).values
        for sz in [1, 2, 3, 4, 5]:
            idx = np.flatnonzero((nd == sz) & ~gone)
            n = P[sz][k + 1]
            if n <= 0:
                continue
            took = idx[:n]
            check(((pd.Timestamp("2026-10-01") - pd.to_datetime(dec[took])).days > 120).all(),
                  "%d-bed round %s reaches a household inside its first 120 days" % (sz, day.date()))
            if n < len(idx) and dec[idx[n - 1]] == dec[idx[n]]:
                tie = idx[dec[idx] == dec[idx[n]]]
                check(isth[tie].all() or not isth[tie].any(), "%d-bed round %s: a mixed tie straddles the cut" % (sz, day.date()))
            gone[took] = True

    # ---- the devices are live ----
    p30, p1a = E.part3(hh, th, E.ASOF), E.part3(hh, th, E.UNITS_START)
    check((p30 != p1a).sum() >= 1, "no Tenter House household's need changes before 1 April")
    check((p1a >= 5).sum() >= 1, "no Tenter House household needs five or more bedrooms")
    rec = E.recorded(c, rv, E.ASOF)
    check((rec.reindex(th).values != p30.values).sum() >= 5, "the case record lags Part 3 for fewer than 5 Tenter House households")

    # ---- the ladder ----
    rungs = {
        "R0 none": E.rung_none(pl, p1a),
        "R1 rate": E.rung_rate(c, rv, pl),
        "R2 share": E.rung_share(c, rv, pl, P),
        "R3 survival": E.rung_survival(c, rv, pl),
        "R4 TA only": E.rung_dynamic(c, pl, lt, P, hh, members="ta"),
        "R5 case record": E.rung_recorded(c, rv, pl, lt, P, hh),
        "R5a case record lists, units on 1 April": E.rung_recorded(c, rv, pl, lt, P, hh, unit="part3", lump=False),
        "R6 Part 3 on 30 Sep for every round": E.rung_frozen(c, pl, lt, P, hh),
        "R6a Part 3 on 1 Apr for every round": E.rung_frozen(c, pl, lt, P, hh, day=E.UNITS_START),
        "R7 units on 30 Sep need": E.rung_dynamic(c, pl, lt, P, hh, unit_day=E.ASOF),
        "R8 four or more as one list": E.rung_dynamic(c, pl, lt, P, hh, lump=True),
        "R9 original plan": E.runoff(c, pl, lt, P0, lambda d, rf: E.part3(hh, rf, d).values, p1a),
        "R10 October counted twice": E.rung_dynamic(c, pl, lt, P, hh, october="twice"),
        "R11 TA start order": E.rung_dynamic(c, pl, lt, P, hh, order="ta_start"),
    }
    same_as = E.rung_dynamic(c, pl, lt, P, hh, october="plan")
    check(cells(same_as) == cells(gold), "the September round run from the plan disagrees with the lets log")
    seen = {g}
    for name, r in rungs.items():
        v = last(r)
        check(v not in seen, "%s repeats a call-off %s" % (name, v))
        seen.add(v)
        off = sum(a != b for a, b in zip(v, g))
        check(off >= 1, "%s lands the answer" % name)
    stump = rungs["R5 case record"]
    check(sum(a != b for a, b in zip(last(stump), g)) >= 2, "the case-record reading misses fewer than two sizes")
    check(abs(sum(last(stump)) - gt) / gt >= 0.10, "the case-record total is within 10 per cent")
    check(sum(a != b for a, b in zip(cells(stump), cells(gold))) >= 15, "the case-record reading lands too many cells")
    rr = rungs["R1 rate"]
    check(sum(a != b for a, b in zip(cells(rr), cells(gold))) >= 20, "the rate reading lands too many cells")
    for name in ("R6 Part 3 on 30 Sep for every round", "R6a Part 3 on 1 Apr for every round", "R8 four or more as one list"):
        check(sum(last(rungs[name])) != gt or last(rungs[name]) != g, "%s lands the call" % name)

    # ---- clean-data test: one row per household stay instead of placements ----
    stay = pl.sort_values("placement_start").groupby("case_ref").agg(
        placement_start=("placement_start", "min"),
        placement_end=("placement_end", lambda x: x.iloc[-1] if x.notna().all() else pd.NaT),
        accommodation_type=("accommodation_type", "last"))
    stay = stay.reset_index()
    g2 = last(E.runoff(c, stay, lt, P, lambda d, rf: E.part3(hh, rf, d).values, p1a))
    check(g2 == g, "the answer moves when placements are consolidated into stays")
    check(last(E.rung_recorded(c, rv, stay, lt, P, hh)) == last(stump), "the case-record reading moves on consolidation")

    # ---- the cost ----
    rates = E.lot3_2728(T)
    units = E.callout(gold)
    cost = E.weekly_cost(units, rates)
    check(abs(cost - round(cost)) <= 0.35, "weekly cost near a half-pound edge (%.2f)" % cost)
    import docs as D
    lot3_old = sum(units[sz] * D.LOT3_2627[sz] for sz in E.SIZES)
    lot2 = sum(units[sz] * D.LOT2_2728[sz] * 7 for sz in E.SIZES)
    check(round(lot3_old) != round(cost) and round(lot2) != round(cost), "a wrong rate basis gives the cost")

    print("checks: %d assertions, %d failed" % (N["n"], len(FAIL)))
    print("answer", g, "total", gt, "weekly cost %.2f" % cost)
    print("run-off", {sz: gold[sz] for sz in E.SIZES})
    print("Tenter House on 30 Sep by unit on 1 April", E.start_counts(pl, hh))
    print("replay: Part 3 on the September round %d of %d; case record %d of %d; case record since 2018 %d of %d"
          % (h, t, hr, tr, hall, tall))
    for name, r in rungs.items():
        v = last(r)
        print("  %-42s %s total %d, sizes off %d, cells off %d" % (
            name, v, sum(v), sum(a != b for a, b in zip(v, g)), sum(a != b for a, b in zip(cells(r), cells(gold)))))
    for f in FAIL:
        print("  FAIL", f)
    return not FAIL


if __name__ == "__main__":
    sys.exit(0 if run() else 1)

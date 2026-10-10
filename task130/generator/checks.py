"""Assertions over the built pack. Exits non-zero on any failure."""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import estimators as E
from build import FILES, DISTRACTORS, TASK, PENDING

N = {"n": 0}
FAIL = []


def check(cond, msg):
    N["n"] += 1
    if not cond:
        FAIL.append(msg)


def last(r):
    return {s: (round(v[-1]) if isinstance(v[-1], float) else v[-1]) for s, v in r.items()}


def run(target=None):
    T = target or os.path.join(TASK, "target")
    c, pl, rv, lt = E.load(T)
    P = E.plan(T)
    P0 = E.plan(T, "Original Mar 2026")
    gold = E.queue_runoff(c, rv, pl, P)
    g = last(gold)
    gt = sum(g.values())

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
    check(set(pl["case_ref"]) <= set(c["case_ref"]), "a placement without a case")
    check(set(lt["case_ref"]) <= set(c["case_ref"]), "a let without a case")
    check(set(rv["case_ref"]) <= set(c["case_ref"]), "a review without a case")
    check(lt["case_ref"].is_unique, "a case let twice")
    # no two live placements for one case on one day
    s = pl.sort_values(["case_ref", "placement_start"], kind="mergesort")
    nxt = s.groupby("case_ref")["placement_start"].shift(-1)
    check(((s["placement_end"].isna() & nxt.notna())).sum() == 0, "an open placement followed by another")
    check(((s["placement_end"] > nxt) & nxt.notna()).sum() == 0, "overlapping placements")
    # unit occupancy never overlaps
    u = pl[pl["accommodation_type"].isin(["Tenter House", "Private sector lease", "Nightly-paid self-contained"])]
    u = u.sort_values(["unit_ref", "placement_start"], kind="mergesort")
    nu = u.groupby("unit_ref")["placement_start"].shift(-1)
    check(((u["placement_end"].fillna(pd.Timestamp("2099-01-01")) > nu) & nu.notna()).sum() == 0, "two households in one unit")
    # every Tenter House household is owed the main duty and its case is open
    th = E.tenter_house(pl)
    ci = c.set_index("case_ref")
    check(all(ci.loc[list(th), "decision"] == "Main duty accepted"), "an interim-duty household in Tenter House")
    check(all(ci.loc[list(th), "case_status"] == "Open"), "a closed case in Tenter House")
    th_starts = pl[pl["accommodation_type"] == "Tenter House"]["placement_start"]
    check((th_starts >= pd.Timestamp("2026-09-15")).sum() == 0, "a placement into Tenter House after the notice")
    # plan actuals tie to the lets log
    import openpyxl
    ws = openpyxl.load_workbook(os.path.join(T, FILES["plan"]))["Revised 14 Sep 2026"]
    st = lt[lt["let_status"] == "Tenancy started"]
    for r, s in zip(range(5, 9), E.SIZES):
        for j, m in enumerate(range(4, 10)):
            n = int(((st["bedrooms"] == s) & (st["tenancy_start"].dt.to_period("M") == pd.Period("2026-%02d" % m))).sum())
            check(ws.cell(row=r, column=2 + j).value == n, "plan actuals %d-bed month %d" % (s, m))
    check(all(sum(P[s]) == sum(P0[s]) for s in (1, 2)), "rephasing moved a one- or two-bed half-year total")
    check(any(P[s] != P0[s] for s in (1, 2)), "rephasing changed nothing")

    # ---- C2: the order is the unique survivor on the lets log ----
    hit, tot = E.replay_lets(c, rv, lt)
    check(hit == tot, "duty-date order reproduces %d of %d lets" % (hit, tot))
    for kw, lim in (({"order": "ta_start", "pl": pl}, 0.2), ({"order": "application_date"}, 0.2),
                    ({"members": "ta", "pl": pl}, 0.9), ({"need": "decision"}, 0.6)):
        h, t = E.replay_lets(c, rv, lt, **kw)
        check(h / t < lim, "rival %s reproduces %.3f of lets" % (kw, h / t))

    # ---- maturity: after day 120 of the duty a household leaves only by a let ----
    acc = c[(c["decision"] == "Main duty accepted") & (c["case_status"] == "Closed")
            & (c["closed_date"] >= pd.Timestamp("2018-04-01"))]
    late = acc[((acc["closed_date"] - acc["decision_date"]).dt.days > 120)
               & ~acc["closure_reason"].str.startswith("Settled")]
    check(len(late) == 0, "%d main-duty cases closed after day 120 other than by a let" % len(late))
    q = E.open_main(c, E.ASOF).copy()
    q["need"] = E.need_at(c, rv, E.ASOF).loc[q["case_ref"]].values
    for s in E.SIZES:
        qs = q[q["need"] == s].sort_values(["decision_date", "case_ref"], kind="mergesort")
        k = sum(P[s])
        reached = qs.head(k)
        check(((pd.Timestamp("2026-10-01") - reached["decision_date"]).dt.days > 120).all(),
              "%d-bed: a household the plan reaches is inside its first 120 days" % s)
        # a duty-date tie straddling a monthly cut never mixes Tenter House and other households,
        # so every tie-break gives the same counts
        for kk in np.cumsum(P[s]):
            if 0 < kk < len(qs) and qs["decision_date"].iloc[kk - 1] == qs["decision_date"].iloc[kk]:
                grp = qs[qs["decision_date"] == qs["decision_date"].iloc[kk]]["case_ref"].isin(th)
                check(grp.all() or not grp.any(), "%d-bed: a mixed tie straddles the cut at %d" % (s, kk))
    # accepted October lets are the front of each list
    pend = lt[lt["let_status"] != "Tenancy started"]
    for s in E.SIZES:
        qs = q[q["need"] == s].sort_values(["decision_date", "case_ref"], kind="mergesort")
        front = set(qs.head(PENDING[s])["case_ref"])
        check(front == set(pend.loc[pend["bedrooms"] == s, "case_ref"]), "%d-bed: accepted lets are not the front" % s)
        check(PENDING[s] <= P[s][0], "%d-bed: accepted lets exceed October" % s)

    # ---- the ladder ----
    rungs = {
        "R0 none": E.rung_none(c, rv, pl), "R1 rate": E.rung_rate(c, rv, pl), "R2 share": E.rung_share(c, rv, pl, P),
        "R3 survival": E.rung_survival(c, rv, pl), "R4 TA only": E.queue_runoff(c, rv, pl, P, members="ta"),
        "R5 need at decision": E.queue_runoff(c, rv, pl, P, need="decision"),
        "R5' TA start": E.queue_runoff(c, rv, pl, P, order="ta_start"),
        "R6 original plan": E.queue_runoff(c, rv, pl, P0), "R6' accepted twice": E.queue_runoff(c, rv, pl, P, pending_twice=pend),
    }
    seen = {tuple(g[s] for s in E.SIZES)}
    for name, r in rungs.items():
        rl = last(r)
        key = tuple(rl[s] for s in E.SIZES)
        check(key not in seen, "%s repeats another rung's call-off %s" % (name, key))
        seen.add(key)
        same = sum(rl[s] == g[s] for s in E.SIZES)
        check(same <= 2, "%s matches the answer in %d sizes" % (name, same))
        check(abs(sum(rl.values()) - gt) / gt >= 0.12, "%s total %d within 12 per cent of %d" % (name, sum(rl.values()), gt))
    above = [n for n, r in rungs.items() if sum(last(r).values()) > gt]
    below = [n for n, r in rungs.items() if sum(last(r).values()) < gt]
    check(above and below, "every rung misses on one side")
    # monthly cells: the rate reading misses every month-end cell that is not zero
    rr = rungs["R1 rate"]
    miss = sum(round(rr[s][k]) != gold[s][k] for s in E.SIZES for k in range(6))
    check(miss >= 20, "rate reading lands %d of 24 cells" % (24 - miss))
    r6 = rungs["R6 original plan"]
    check(sum(r6[s][k] != gold[s][k] for s in E.SIZES for k in range(6)) >= 10, "the plan revision moves too few cells")

    # ---- clean-data test: one row per household stay instead of placements ----
    stay = pl.sort_values("placement_start").groupby("case_ref").agg(
        placement_start=("placement_start", "min"), placement_end=("placement_end", lambda x: x.iloc[-1] if x.notna().all() else pd.NaT),
        accommodation_type=("accommodation_type", "last"))
    stay = stay.reset_index()
    g2 = last(E.queue_runoff(c, rv, stay, P))
    check(g2 == g, "the answer moves when placements are consolidated into stays")
    check(last(E.rung_rate(c, rv, stay)) == last(rungs["R1 rate"]), "the rate reading moves on consolidation")

    # ---- the cost ----
    rates = E.lot3_2728(T)
    cost = E.weekly_cost(E.callout(gold), rates)
    check(abs(cost - round(cost)) <= 0.35, "weekly cost near a half-pound edge (%.2f)" % cost)
    import docs as D
    lot3_old = sum(E.callout(gold)[s] * D.LOT3_2627[s] for s in E.SIZES)
    lot2 = sum(E.callout(gold)[s] * D.LOT2_2728[s] * 7 for s in E.SIZES)
    check(round(lot3_old) != round(cost) and round(lot2) != round(cost), "a wrong rate basis gives the cost")

    print("checks: %d assertions, %d failed" % (N["n"], len(FAIL)))
    print("answer", g, "total", gt, "weekly cost %.2f" % cost)
    for name, r in rungs.items():
        print("  %-22s %s total %d" % (name, last(r), sum(last(r).values())))
    for f in FAIL:
        print("  FAIL", f)
    return not FAIL


if __name__ == "__main__":
    sys.exit(0 if run() else 1)

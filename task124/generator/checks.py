"""Assertions the generator runs before any file is written. Each check fails the build loudly."""
from __future__ import annotations

import itertools
from datetime import date

import numpy as np

import desk as K
from analysis import lenders_basis
from common import (BOOKS, HEDGES, NC, PEAKS, SUMMERS, bin_distance, continuous_split, lot_margins, lots,
                    round_half_up)

LOG = []
ANSWER = {"Coast": 120, "East": 30, "Far West": 0, "North": 0, "North Central": 210, "South Central": 25,
          "Southern": 15, "West": 0}
RUNG3 = {"Coast": 130, "East": 40, "Far West": 0, "North": 0, "North Central": 165, "South Central": 35,
         "Southern": 30, "West": 0}


def ck(name, ok, detail=""):
    LOG.append((name, bool(ok), detail))
    if not ok:
        raise AssertionError(f"{name}: {detail}")


def vec(a):
    return tuple(a[b] for b in BOOKS)


def main_call(an):
    R = an.rungs()
    L = {k: lots(E) for k, E in R.items()}
    E = R["R4"]
    a = L["R4"]
    ck("M01 the answer is 120 / 30 / 0 / 0 / 210 / 25 / 15 / 0", a == ANSWER, vec(a))
    ck("M02 rung 3 (the stump) is 130 / 40 / 0 / 0 / 165 / 35 / 30 / 0", L["R3"] == RUNG3, vec(L["R3"]))
    ck("M03 rungs 0 to 4 file pairwise distinct vectors",
       len({vec(v) for v in L.values()}) == 5, {k: vec(v) for k, v in L.items()})
    nc = {k: v[NC] for k, v in L.items()}
    ck("M04 every lower rung puts North Central at least 14 per cent from 210, bracketed (rung 2 < rung 3 < answer < rung 1)",
       all(abs(nc[k] - 210) / 210 >= 0.14 for k in ("R0", "R1", "R2", "R3")) and nc["R2"] < nc["R3"] < 210 < nc["R1"], nc)
    r0 = sorted(BOOKS, key=lambda b: -L["R0"][b])
    ck("M05 rung 0 (the policy's words on the settled loads) leads with Coast and puts North Central 4th or lower",
       r0[0] == "Coast" and r0.index(NC) >= 3, vec(L["R0"]))
    post = {b: E[b] - a[b] for b in BOOKS}
    ck("M06 every post-block exposure sits at least 0.25 MW from a half-MW edge",
       min(bin_distance(v, 1.0) for v in post.values()) >= 0.25, {b: round(v, 3) for b, v in post.items()})
    mn, mx = lot_margins(E)
    ck("M07 no lot decision within 0.9 MW of a tie (lowest value a lot was taken at less highest value none was)",
       mn - mx >= 0.9, (round(mn, 3), round(mx, 3)))
    w, cont = continuous_split(E)
    near5 = {b: int(round_half_up(v, 5)) for b, v in cont.items()}
    fl = {b: 5 * int(v // 5) for b, v in cont.items()}
    for b in sorted(BOOKS, key=lambda b: -(cont[b] - fl[b]))[: (400 - sum(fl.values())) // 5]:
        fl[b] += 5
    ck("M08 lot by lot equals the continuous water level rounded to 5 MW and by largest remainder",
       near5 == a == fl, (round(w, 3), near5, fl))
    orders = [list(reversed(BOOKS)), BOOKS[3:] + BOOKS[:3]]
    ck("M09 three book orders give the same split (the tie-break is never used)",
       all(lots(E, order=o) == a for o in orders))
    nxt = max(BOOKS, key=lambda b: post[b])
    ck("M10 the next lot would have gone to Southern", nxt == "Southern", (nxt, round(post[nxt], 3)))
    ck("M11 rung 3's next-lot level sits more than 5 MW under the answer's", max(R["R3"][b] - L["R3"][b] for b in BOOKS)
       < post[nxt] - 5, round(max(R["R3"][b] - L["R3"][b] for b in BOOKS), 3))
    return {"rungs": {k: vec(v) for k, v in L.items()}, "E": {k: {b: round(v[b], 3) for b in BOOKS} for k, v in R.items()},
            "post": {b: round(post[b], 3) for b in BOOKS}, "next": (nxt, round(post[nxt], 3)),
            "water": round(w, 3), "margins": (round(mn, 3), round(mx, 3)),
            "centres_mw": round(an.u_star * an.centres / 1000.0, 3), "loads": {b: round(E[b] + HEDGES[b], 3) for b in BOOKS}}


VIOLATES = {
    "rows, pooled (rung 1)": "enrolment dictionary: an AMEND row supersedes the enrolment it amends",
    "rows, class factor on the centres": "the same supersession",
    "rows, uncalled draw on the centres": "the same supersession",
    "premises, pooled (rung 2)": "premise register: the 31 centres are NAICS 493120, a class the pooled factor never held",
    "premises, class factor (rung 3)": "credits on every closed peak date, the uncalled reads and the eligibility clause",
    "partial: class factor on every new North Central premise": "premise register: the other new premises are not refrigerated",
    "partial: uncalled draw on every new North Central premise": "premise register: the other new premises are not refrigerated",
    "centres at 0.88": "below every defensible estimator of the uncalled draw",
    "centres at 0.92": "above every defensible estimator of the uncalled draw",
    "settled loads, own book (rung 0)": "the replay table (8 of 80 cells)",
}
CONVERGE = ["premises, uncalled draw (answer)", "members uncalled in 2027 too", "centres at 0.885", "centres at 0.916",
            "P90 nearest rank", "P90 exclusive (Excel PERCENTILE.EXC)"]


def grid(an):
    G = an.grid()
    out = {}
    for k, E in G.items():
        a = lots(E)
        out[k] = (vec(a), a[NC])
        if k in CONVERGE:
            ck(f"G conv: '{k}' files the answer", a == ANSWER, vec(a))
        else:
            far = abs(a[NC] - 210) / 210
            need = 0.02 if k in ("centres at 0.88", "centres at 0.92") else 0.06
            ck(f"G cell: '{k}' differs, North Central {a[NC]} ({far:+.1%}); violates {VIOLATES[k]}",
               a != ANSWER and far >= need, vec(a))
    for nm, E in (("class replay, every class at its own factor", an.class_replay_full()),
                  ("NAICS-level replay of the IDR premises", an.naics_replay())):
        a = lots(E)
        out[nm] = (vec(a), a[NC])
        ck(f"G conv: '{nm}' files the answer", a == ANSWER, vec(a))
    return out


def corpus(an):
    tab = an.replay_table()
    ck("C01 every replay-table cell sits at least 0.05 MW from a half-MW edge",
       min(bin_distance(v, 1.0) for v in tab.values()) >= 0.05, min(bin_distance(v, 1.0) for v in tab.values()))
    p = an.w.prem
    pk26 = PEAKS[2026][0]
    act = p[(p["start"] <= pk26) & p["end"].map(lambda e: e is None or e >= pk26)]
    ck("C02 the 2026 book holds no AMEND row and no centre, so rungs 1 to 4 return the same 80 cells",
       not (act["record_type"] == "AMEND").any() and not (act["comp"] == "centre").any())
    riv = an.replay_rivals()
    ck("C03 the per-kW replay is the unique survivor: every rival divisor or numerator misses cells",
       all(h < 80 for h, _ in riv.values()) and riv["settled loads unscaled"][0] == 8, riv)
    ck("C04 settled loads unscaled match only the 8 cells of 2026; worst miss over 10 per cent",
       riv["settled loads unscaled"][1] >= 0.10, riv["settled loads unscaled"])
    share = max(an.ref_peak[b][y] / an.md_peak[b][y] for b in BOOKS for y in SUMMERS)
    ck("C05 the refrigerated class held under 1 per cent of every book in every closed summer", share < 0.01, round(share, 5))
    cbs = an.class_by_summer
    ck("C06 the fourteen drew 0.595 to 0.605 of maximum demand at every closed system peak (class factor)",
       all(0.595 <= v <= 0.605 for v in cbs.values()) and 0.598 <= an.class_factor <= 0.602, cbs)
    ck("C07 each member's own draw at every closed peak sits 0.55 to 0.65 of its maximum demand",
       an.site_called.min() >= 0.545 and an.site_called.max() <= 0.655, (an.site_called.min(), an.site_called.max()))
    est = an.estimators()
    py = {}
    m = an.mr[(an.mr["he"] == an.mr["pkh"]) & ~an.mr["called"]]
    for y, g in m.groupby("y"):
        py[y] = g["kwh"].sum() / g["md"].sum()
    ck("C08 uncalled weekday draw at the peak hour 0.895 to 0.905 in every summer",
       all(0.895 <= v <= 0.905 for v in py.values()), {y: round(v, 4) for y, v in py.items()})
    ck("C09 at least four weekdays of each summer's hottest decile carry no call", min(an.hot_counts.values()) >= 4,
       an.hot_counts)
    cr = an.w.credits
    mem_accts = set(an.mem["account"])
    ok = True
    for y in SUMMERS:
        d = PEAKS[y][0]
        active = set(an.mem.loc[an.mem["start"] <= d, "account"])
        got = set(cr.loc[cr["date"] == d, "account"])
        ok &= active == got
    ck("C10 every closed system peak date carries a credit for every member account in the book", ok)
    ck("C11 no credit for any account outside the fourteen", set(cr["account"]) <= mem_accts)
    ck("C12 every closed system peak falls in July or August", all(PEAKS[y][0].month in (7, 8) for y in SUMMERS))
    ck("D01 every one of the twelve estimators of the uncalled draw lies in [0.894, 0.906]",
       all(0.894 <= v <= 0.906 for v in est.values()) and len(est) == 12, {k: round(v, 4) for k, v in est.items()})
    return {"rivals": riv, "estimators": {k: round(v, 5) for k, v in est.items()}, "class_by_summer": cbs,
            "class_factor": round(an.class_factor, 5), "u_star": round(an.u_star, 5), "hot_uncalled": an.hot_counts,
            "uncalled_by_summer": {y: round(v, 5) for y, v in py.items()}, "max_ref_share": round(share, 5)}


def twins(an):
    p = an.w.prem
    cold = p[(p["comp"] == "ref") & (p["md_kw"] == 2400.0) & (p["book"] == NC)].iloc[0]
    wh = p[p["twin"]].iloc[0]
    cols = ["book", "tdsp", "plan", "deposit", "meter", "age_band", "md_kw", "start", "broker", "record_type"]
    ck("T01 the twin pair is identical on every enrolment column", all(cold[c] == wh[c] for c in cols),
       [(c, cold[c], wh[c]) for c in cols if cold[c] != wh[c]])
    d, h = PEAKS[2026][0], PEAKS[2026][1]
    r = an.w.ireads
    whv = float(r[(r["esi_id"] == wh["esi_id"]) & (r["date"] == d) & (r["he"] == h)]["kwh"].iloc[0])
    m = an.w.mreads
    cv = float(m[(m["esi_id"] == cold["esi_id"]) & (m["date"] == d) & (m["he"] == h)]["kwh"].iloc[0])
    pooled = an.pooled(NC, 2026) * 2.4
    ck("T02 at the 2026 peak the cold store drew about 1.44 MW and the warehouse 0.91 MW, 1.5x or more apart; the "
       "pooled factor gives both one figure", 1420 <= cv <= 1460 and whv == 910.0 and cv / whv >= 1.5,
       (cv, whv, round(pooled, 3)))
    return {"cold_kw": cv, "warehouse_kw": whv, "pooled_mw": round(pooled, 3)}


def clean_data(an):
    """Repair the enrolment extract to one row per premise: the answer and rung 3 do not move; the answer is not
    rung 3. The lens swap: rung 3's factor and the answer's come from disjoint day sets."""
    R = an.rungs()
    ded = {b: an.ded27[b] for b in BOOKS}
    saved = dict(an.rows27)
    an.rows27 = ded
    R1rep = lots(an.exposures("rows"))
    an.rows27 = saved
    ck("K01 clean-data test on the enrolment extract: repaired, rung 1 becomes rung 2 while rung 3 and the answer "
       "stand and differ", R1rep == lots(R["R2"]) and lots(R["R4"]) == ANSWER and lots(R["R3"]) != ANSWER)
    called = {(y, PEAKS[y][0]) for y in SUMMERS}
    unc = {(d.year, d) for d, c in zip(an.mr["date"], an.mr["called"]) if not c}
    ck("K02 lens swap: rung 3's measure (called peak days) and the answer's (uncalled weekdays) share no day",
       not (called & unc))


def asks(w):
    q = w.quotes
    ans = K.premium_answer(q)
    stops = {
        "S1 natural": K.premium_answer(q, zone_map=K.MAP_2026, holidays=False, decisions=False, approval=False,
                                       pecos=False, notional=False, latest_rev_only=True),
        "S2 units right, holidays missed": K.premium_answer(q, holidays=False),
        "S3 over-corrected (revised and reissued-code quotes dropped)": K.premium_answer(q, drop_revised_reissued=True),
        "S4 right rules on the 2026 book map": K.premium_answer(q, zone_map=K.MAP_2026),
    }
    ck("A01 every premium sits at least 5 cents from a half-dollar edge", min(bin_distance(v, 1.0) for v in ans.values()) >= 0.05)
    moved = {}
    for k, v in stops.items():
        dif = {c: v[c] / ans[c] - 1 for c in ans if abs(v[c] - ans[c]) > 0.004}
        moved[k] = (len(dif), round(min(abs(x) for x in dif.values()), 4) if dif else None)
        ck(f"A02 {k}: every cell it moves is at least 1 per cent off", dif and min(abs(x) for x in dif.values()) >= 0.01, moved[k])
    ck("A03 lazy delta: the natural path is wrong on at least 24 of 32 cells", moved["S1 natural"][0] >= 24, moved)
    ck("A04 the 2026 map moves exactly East's four cells", moved["S4 right rules on the 2026 book map"][0] == 4)
    ck("A05 the over-corrector loses the lowest valid quote in at least six cells",
       moved["S3 over-corrected (revised and reissued-code quotes dropped)"][0] >= 6)
    v = q[q["decision"] == "ACCEPTED"]
    v = v[[K.cpty_valid_on(c, s.date()) for c, s in zip(v["cpty"], v["sent"])]]
    v = v.assign(usd=[p * K.hours(K.BROKERS[b][1], m) for p, b, m in zip(v["price"], v["broker"], v["month"])])
    gaps, pecos_wins = [], 0
    for (z, m), g in v.groupby(["zone", "month"]):
        s = g.sort_values("usd")
        gaps.append(s["usd"].iloc[1] / s["usd"].iloc[0] - 1)
        pecos_wins += s["broker"].iloc[0] == "PPB"
    ck("A06 every cell's winning quote is at least 2 per cent under the next valid quote", min(gaps) >= 0.02, round(min(gaps), 4))
    ck("A07 Pecos (the sheet outside the quote file) holds the lowest valid quote in at least ten cells", pecos_wins >= 10, pecos_wins)
    nod = K.premium_answer(q, decisions=False)
    noa = K.premium_answer(q, approval=False)
    ck("A08 hazards cross the ask: ignoring decisions moves cells, ignoring approval dates moves cells",
       sum(abs(nod[c] - ans[c]) > 0.004 for c in ans) >= 4 and sum(abs(noa[c] - ans[c]) > 0.004 for c in ans) >= 4)
    bl, ml = w.blotter, w.matching
    H = K.hedge_price_answer(bl, ml)
    bstops = {"S1 latest booked, MW-weighted": K.hedge_price_answer(bl, ml, version="latest", weight="mw"),
              "S2 matched, MW-weighted": K.hedge_price_answer(bl, ml, weight="mw"),
              "S3 matched, MWh-weighted, holidays ignored": K.hedge_price_answer(bl, ml, holidays=False),
              "S4 original prices only": K.hedge_price_answer(bl, ml, version="original")}
    ck("B01 every book's hedge price sits at least 0.15 cents from a half-cent edge",
       min(bin_distance(x, 0.01) for x in H.values()) >= 0.0015)
    bm = {}
    for k, v in bstops.items():
        n = sum(abs(v[b] - H[b]) >= 0.05 for b in BOOKS)
        bm[k] = n
        ck(f"B02 {k}: at least $0.05/MWh off on six or more books", n >= 6, {b: round(v[b] - H[b], 3) for b in BOOKS})
    pf = {p: b for b, ps in K.PORTFOLIOS.items() for p in ps}
    s = bl[(bl["start"] == date(2027, 6, 1))]
    ok = all(s[s["amend"] == 0].assign(b=lambda x: x["portfolio"].map(pf)).groupby("b")["mw"].sum().get(b, 0) == HEDGES[b]
             for b in BOOKS)
    mwset = s.groupby("trade_id")["mw"].nunique().max()
    ck("B03 blotter MW per book ties the position report, and every amendment is price-only", ok and mwset == 1)
    return {"premium": {f"{b}|{m}": round(v, 2) for (b, m), v in ans.items()}, "premium_stops": moved,
            "hedge_price": {b: round(H[b], 4) for b in BOOKS}, "hedge_stops": bm,
            "hedge_stop_values": {k: {b: round(v[b], 4) for b in BOOKS} for k, v in bstops.items()},
            "pecos_wins": pecos_wins}


def lenders(an, rows, rung0):
    E = lenders_basis(an, rows)
    a = lots(E)
    top = max(BOOKS, key=lambda b: a[b])
    ck("L01 the lenders' zone-share basis (declared wrong-basis distractor) is Coast-led, puts North Central under 150, "
       "and is neither the answer nor rung 0", top == "Coast" and a[NC] < 150 and a != ANSWER and vec(a) != rung0, vec(a))
    return vec(a)

"""task173 checks: the generator's assertions on the built pack (target/) and on the clean truth (world.py, des.py,
records.py, acd.py).

The three-rules block (R1 to R3c), the ladder and its rivals, the constructions and their one-sigma corridor, the
back-test, the separation of the case-level model from the contact-level one, the four screens, every semantic fork
row (SF1 to SF16), both asks with their devices and stops, the cracker's measured pair, the separation line, the
input gates, the realism sweep and the dates."""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import acd as A          # noqa: E402
import asks as AS        # noqa: E402
import calc as C         # noqa: E402
import common as K       # noqa: E402
import cracker as CR     # noqa: E402
import docs as DOC       # noqa: E402
import records as RC     # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
RESULTS = []

GOLD = 10000           # the booking, whole blocks of 1,000 agent hours
DEFAULT = 7000         # the default path: last season's contacts per new case
EDGE_MIN = 250.0       # every construction at least a quarter block from either edge


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s %-78s %s" % ("PASS" if ok else "FAIL", label[:78], detail))


def order(b):
    return K.ceil_to(b, 1000)


def edge(b):
    o = order(b)
    return min(b - (o - 1000), o - b)


# ------------------------------------------------------------------------------------------------- the clean truth
def clean_world():
    import build
    return build.world()


def clean_estimates(B):
    """The 2026 rates from the world's own records, every expert's group and go-live known exactly, handle time as
    the standard defines it (the CRM's talk and after-contact work)."""
    recs, staff = B.recs, B.staff
    en = recs["queue"] == 0
    r = recs[en]
    delay = B.delay[en]
    kind = np.array([s.kind for s in staff])
    first_season = np.array([s.first for s in staff])
    gl = np.array([s.golive.toordinal() if s.golive else 0 for s in staff])
    ex = r["expert"]
    V = kind[ex] == "vendor"
    N = (first_season[ex] == K.SEASON_CRM) & ~V
    R = ~V & ~N
    order_ = np.lexsort((r["start"], r["day"], r["case"]))
    cs = r["case"][order_]
    nxt = np.zeros(len(cs), dtype=bool)
    nxt[:-1] = cs[1:] == cs[:-1]
    fol = np.zeros(len(cs), dtype=bool)
    fol[order_] = nxt
    first = r["pos"] == 1
    hmin = (r["end"] - r["start"]) * 60 - delay / 60
    wk = np.where(N, (r["day"] - gl[ex]) / 7.0, -1.0)
    f0, f1 = K.fortnight(K.SEASON_CRM)
    fn = (r["day"] >= f0.toordinal()) & (r["day"] <= f1.toordinal())
    E = type("E", (), {})()
    E.pR, E.pO = fol[R & first].mean(), fol[V & first].mean()
    E.q = fol[~first].mean()
    E.aR, E.aO = hmin[R].mean(), hmin[V].mean()
    E.cp = C.fit_expo(wk[N & first], fol[N & first].astype(float), (0.14, 0.3, 5.0))
    E.ca = C.fit_expo(wk[N], hmin[N], (31.0, 14.0, 5.0))
    E.M26 = fn.sum() / (fn & first).sum()
    E.hmin, E.N, E.wk = hmin, N, wk
    return E


def booking_from(P, E, follow_new=None, vendor_rate=None, fixed_point=True, contacts_per_case=None):
    """The booking under a choice of steps: the follow-up model (by first-contact handler, or a carried contacts per
    case), the vendor's own rate, and whether the vendor's contacts add their own follow-ups."""
    pf = follow_new or (lambda x: C.expo(x, *E.cp))
    Kc, Kp = C.inhouse(P, pf, lambda x: C.expo(x, *E.ca), E.pR, E.aR)
    kO = C.H_BILLED * 60 / E.aO
    if contacts_per_case is not None:
        return max(0.0, (P.F27 * contacts_per_case - Kc) / kO)
    pO = E.pO if vendor_rate is None else vendor_rate
    if not fixed_point:
        return max(0.0, (P.F27 * (1 + (Kp / Kc) / (1 - E.q)) - Kc) / kO)
    return C.solve_booking(Kc, Kp, pO, E.aO, E.q, P.F27)


# ------------------------------------------------------------------------------------------------- the window load
def lag_pmf(P):
    """Days between consecutive contacts on a case in the 2026 CRM (English queue)."""
    o = P.order
    cs, dd = P.case[o], P.day[o]
    same = cs[1:] == cs[:-1]
    lags = (dd[1:] - dd[:-1])[same]
    pmf = np.bincount(lags, minlength=15)[:15].astype(float)
    return pmf / pmf.sum()


def window_contacts(P, E, B):
    """The contacts that arrive inside the 2027 fortnight (rather than the contacts on its cases), from the demand
    plan's daily new cases before and in the fortnight and the 2026 lag profile, at the fortnight's mix."""
    g = C.golden(P, E)
    pbar, q = g["pbar"], E.q
    pmf = lag_pmf(P)
    # expected contacts per case on each day after it opens
    first = pbar * pmf
    later = np.zeros(60)
    later[:len(first)] += first
    gen = later.copy()
    for _ in range(6):
        nxt = np.convolve(gen, q * pmf)[:60]
        later += nxt
        gen = nxt
    c = later.copy()
    c[0] += 1.0
    f0, f1 = K.fortnight(K.SEASON_PLAN)
    tot = 0.0
    for d, n in P.plan:
        for j in range(60):
            if f0 <= d + dt.timedelta(j) <= f1:
                tot += n * c[j]
    return tot, g["contacts"]


# ------------------------------------------------------------------------------------------------- shipped text
def shipped_text():
    import openpyxl
    out = {}
    for f in sorted(os.listdir(TARGET)):
        p = os.path.join(TARGET, f)
        if f.endswith((".csv", ".txt", ".eml")):
            out[f] = open(p, encoding="utf-8").read()
        elif f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(p, read_only=True)
            parts = []
            for ws in wb.worksheets:
                for row in ws.iter_rows(values_only=True):
                    parts.extend(str(v) for v in row if v is not None)
            wb.close()
            out[f] = "\n".join(parts)
        elif f.endswith(".pdf"):
            out[f] = AS.pdf_text(p)
        elif f.endswith(".docx"):
            import docx
            out[f] = "\n".join(pp.text for pp in docx.Document(p).paragraphs)
    return out


def main():
    P = C.Pack(TARGET)
    E = C.Est(P)
    g = C.golden(P, E)
    B26 = g["B"]
    print("golden: %.1f billed hours, order %d" % (B26, g["order"]))
    check("CALL the booking is %d agent hours" % GOLD, g["order"] == GOLD, "%.1f h needed" % B26)

    # ---------------------------------------------------------------------------------- ladder and rivals
    rv, _ = C.rivals(P, E)
    lad = {
        "R0 last season's contacts per new case and last season's handle time":
            rv["last season's contacts per new case, last season's handle time"],
        "R1 default: last season's contacts per new case, handle time by weeks on queue":
            rv["last season's contacts per new case, handle time by weeks on queue"],
        "R2 follow-up chance by group, the new classes at their 2026 season average":
            rv["first-contact rate by group, new hires at their season average"],
        "R2b the same, the new classes at last fortnight's rate":
            rv["first-contact rate by group, new hires at last fortnight's rate"],
        "R2c tenure curve, Hillsborough at the returning experts' rate":
            rv["vendor agents at the returning rate"],
        "R2d tenure curve, Hillsborough's hours as capacity without follow-ups of their own":
            rv["bench's follow-ups only, vendor hours taken as pure capacity"],
        "R3 decisive: follow-ups set by who opens each case, Hillsborough's own rate, the booking that carries its own load":
            B26,
    }
    for k, v in lad.items():
        print("   %-100s %8.1f  order %d" % (k, v, order(v)))
    check("LADDER the default path files %d" % DEFAULT, order(lad["R1 default: last season's contacts per new case, "
                                                                 "handle time by weeks on queue"]) == DEFAULT)
    for k, v in lad.items():
        if not k.startswith("R3"):
            check("LADDER %s misses the call" % k[:40], order(v) != GOLD, "%.0f -> %d" % (v, order(v)))
    worst = min((((order(v) - 1000) - v) if v <= (order(v) - 1000) + 1e-9 else 0, k) for k, v in rv.items())
    landed = [k for k, v in rv.items() if order(v) == GOLD]
    check("RIVALS every natural route orders another block", not landed, "landed: %s" % landed if landed else
          "%d routes, none in the %d block" % (len(rv), GOLD))
    gap = sorted((abs(v - (GOLD - 1000)) if v <= GOLD - 1000 else abs(v - GOLD), k) for k, v in rv.items())
    check("RIVALS the nearest route sits at least 150 h outside the golden's block", gap[0][0] >= 150,
          "%.0f h (%s)" % gap[0])

    # ---------------------------------------------------------------------------------- constructions and sigma
    cons = C.constructions(P, E)
    lo = GOLD - 1000
    for k, v in cons.items():
        check("FAMILY %s orders %d at least %d h from an edge" % (k[:44], GOLD, EDGE_MIN),
              order(v) == GOLD and edge(v) >= EDGE_MIN, "%.0f (edge %.0f)" % (v, edge(v)))
    sig, boots = C.bootstrap(P, n=200)
    check("SIGMA the golden plus or minus one sigma stays in its block", lo < B26 - sig and B26 + sig <= GOLD,
          "sigma %.0f h, %.0f to %.0f" % (sig, B26 - sig, B26 + sig))
    check("SIGMA 90 per cent of the resamples order %d" % GOLD, np.mean([order(b) == GOLD for b in boots]) >= 0.9,
          "%.1f per cent" % (100 * np.mean([order(b) == GOLD for b in boots])))

    # ---------------------------------------------------------------------------------- the design forces the model
    first, fol = P.first, P.followed.astype(float)
    nf = ~first
    rates = {}
    for gname in "RNV":
        m = nf & (P.grp == gname)
        m1 = first & (P.grp == gname)
        rates[gname] = (fol[m].mean(), math.sqrt(fol[m].mean() * (1 - fol[m].mean()) / m.sum()), fol[m1].mean(),
                        math.sqrt(fol[m1].mean() * (1 - fol[m1].mean()) / m1.sum()))
    zf = max(abs(rates[a][0] - rates[b][0]) / math.hypot(rates[a][1], rates[b][1]) for a, b in (("R", "N"), ("R", "V"),
                                                                                                ("N", "V")))
    z1 = min(abs(rates[a][2] - rates[b][2]) / math.hypot(rates[a][3], rates[b][3]) for a, b in (("R", "N"), ("R", "V"),
                                                                                                ("N", "V")))
    check("FORCED a follow-up's own chance of another is the same whoever takes it", zf < 2.0, "largest z %.2f" % zf)
    check("FORCED a first contact's chance differs by who takes it", z1 > 10.0, "smallest z %.1f" % z1)

    # within Hillsborough's three weeks, its agents' follow-ups come back like the bench's follow-ups (the gap
    # across the season is the deadline weeks' topics, not the handler)
    v0, v1 = dt.date(2026, 4, 13).toordinal(), dt.date(2026, 5, 3).toordinal()
    inwin = (P.day >= v0) & (P.day <= v1) & nf
    pv, nv_ = fol[inwin & (P.grp == "V")].mean(), (inwin & (P.grp == "V")).sum()
    pi, ni_ = fol[inwin & (P.grp != "V")].mean(), (inwin & (P.grp != "V")).sum()
    zv = abs(pv - pi) / math.sqrt(pv * (1 - pv) / nv_ + pi * (1 - pi) / ni_)
    check("FORCED in the same three weeks Hillsborough's follow-ups come back like the bench's", zv < 2.0,
          "%.4f against %.4f, z %.2f" % (pv, pi, zv))
    # the openers' mix: the 2026 fortnight's against the 2027 fortnight's
    f0_26, f1_26 = K.fortnight(K.SEASON_CRM)
    fn26 = (P.day >= f0_26.toordinal()) & (P.day <= f1_26.toordinal())
    mix26 = [float((P.grp[fn26 & first] == x).mean()) for x in "RNV"]
    print("   2026 fortnight openers: returning %.3f, classes %.3f, Hillsborough %.3f; class weeks %.1f" % (
        *mix26, P.wk[fn26 & (P.grp == "N")].mean()))
    check("MIX the 2026 fortnight's openers were 61 per cent returning, 32 per cent classes, 7 per cent Hillsborough",
          [round(100 * m) for m in mix26] == [61, 32, 7])
    # one pass of the balance from Hillsborough booked as capacity lands the block
    Kc1, Kp1 = C.inhouse(P, lambda x: C.expo(x, *E.cp), lambda x: C.expo(x, *E.ca), E.pR, E.aR)
    kO1 = C.H_BILLED * 60 / E.aO
    B0 = max(0.0, (P.F27 * (1 + (Kp1 / Kc1) / (1 - E.q)) - Kc1) / kO1)
    Pb1 = (Kp1 + B0 * kO1 * E.pO) / (Kc1 + B0 * kO1)
    B1 = (P.F27 * (1 + Pb1 / (1 - E.q)) - Kc1) / kO1
    check("BALANCE one pass from Hillsborough as capacity already orders %d" % GOLD, order(B1) == GOLD,
          "%.0f h from %.0f" % (B1, B0))
    # a finer grain: the comeback by opener group and topic, at the 2026 fortnight's topic mix
    topics = sorted(set(P.topic))
    tmix = {tp: float((P.topic[fn26 & first] == tp).mean()) for tp in topics}

    def by_topic(mask):
        return sum(tmix[tp] * fol[mask & (P.topic == tp)].mean() for tp in topics)
    pRt, pOt = by_topic(first & (P.grp == "R")), by_topic(first & (P.grp == "V"))
    qt = sum(tmix[tp] * fol[nf & (P.topic == tp)].mean() for tp in topics)
    scale = by_topic(first & (P.grp == "N")) / fol[first & (P.grp == "N")].mean()
    Kct, Kpt = C.inhouse(P, lambda x: scale * C.expo(x, *E.cp), lambda x: C.expo(x, *E.ca), pRt, E.aR)
    bt_ = C.solve_booking(Kct, Kpt, pOt, E.aO, qt, P.F27)
    check("GRAIN comebacks by opener and topic at the fortnight's topic mix: same call", order(bt_) == GOLD,
          "%.0f h" % bt_)

    # ---------------------------------------------------------------------------------- the back-test
    bt = C.backtest(P, E)
    em_f = max(abs(r["err_model"]) for r in bt["fortnight"])
    er_f = max(abs(r["err_rate"]) for r in bt["fortnight"])
    em_s = max(abs(r["err_model"]) for r in bt["season"])
    er_s = max(abs(r["err_rate"]) for r in bt["season"])
    check("OOS the tenure model's worst season error is under a third of the carried rate's", em_s < er_s / 3,
          "%.1f against %.1f per cent" % (em_s, er_s))
    check("OOS the tenure model's worst fortnight error is under half the carried rate's", em_f < er_f / 2,
          "%.1f against %.1f per cent" % (em_f, er_f))
    check("OOS the tenure model beats the carried rate in mean absolute error, both depths",
          np.mean([abs(r["err_model"]) for r in bt["fortnight"]]) < np.mean([abs(r["err_rate"]) for r in bt["fortnight"]])
          and np.mean([abs(r["err_model"]) for r in bt["season"]]) < np.mean([abs(r["err_rate"]) for r in bt["season"]]))

    # ---------------------------------------------------------------------------------- the four screens
    # variance-only: the lever (the default's miss) against sigma
    lever = B26 - lad["R1 default: last season's contacts per new case, handle time by weeks on queue"]
    check("SCREEN variance-only: the lever is over ten sigma", lever > 10 * sig, "%.0f h against sigma %.0f" % (lever, sig))
    # common-exposure subset: no 2026 week of the CRM reaches 2027's mix, so no filter-and-divide reads the load
    f0, f1 = K.fortnight(K.SEASON_PLAN)
    Kr = P.returning27 * C.H_EXPERT * 60 / E.aR
    Kn = sum(n * (C.H_EXPERT / 14) * 60 / C.expo((d - gl).days / 7.0, *E.ca) for d in
             [f0 + dt.timedelta(k) for k in range(14)] for gl, n in P.classes27)
    Kv = g["vendor_contacts"]
    mix27 = np.array([Kr, Kn, Kv]) / (Kr + Kn + Kv)
    week = (P.day - K.monday(K.season_open(K.SEASON_CRM)).toordinal()) // 7
    best = 9.0
    for w in np.unique(week):
        m = (week == w) & first
        if m.sum() < 2000:
            continue
        mix = np.array([(P.grp[m] == x).mean() for x in "RNV"])
        best = min(best, float(np.abs(mix - mix27).sum()))
    check("SCREEN common exposure: no 2026 week's first-contact mix comes within 0.25 of 2027's (L1)", best > 0.25,
          "nearest %.2f; 2027 mix R %.2f N %.2f V %.2f" % (best, *mix27))
    old_max = max(r["observed"] for r in bt["fortnight"] + bt["season"])
    check("SCREEN common exposure: no earlier season's follow-ups per new ticket reach 2027's",
          old_max < g["followups"] / P.F27 - 0.04, "highest %.3f against %.3f" % (old_max, g["followups"] / P.F27))

    # ---------------------------------------------------------------------------------- semantic forks
    # SF1 billed against handle hours
    check("SF1 the booking is billed hours: read as handle hours it is another block",
          order(B26 * C.H_BILLED) != GOLD, "%.0f handle hours" % (B26 * C.H_BILLED))
    # SF2 the fortnight
    check("SF2 the fortnight is 19 April to 2 May 2027", K.fortnight(2027) == (dt.date(2027, 4, 19), dt.date(2027, 5, 2)))
    # SF3 the fortnight's own cases against the contacts arriving in it
    wc, cc = window_contacts(P, E, None)
    kO = C.H_BILLED * 60 / E.aO
    b_win = g["B"] + (wc - cc) / kO
    check("SF3 the contacts arriving in the window instead: same call", order(b_win) == GOLD,
          "window %.0f against cases %.0f, %.0f h" % (wc, cc, b_win))
    # SF4 the bench as filed: 150 confirmed on the English queue, four classes of 60
    check("SF4 the bench: 150 confirmed English-queue experts and 240 seats",
          P.returning27 == 150 and sum(n for _, n in P.classes27) == 240 and len(P.classes27) == 4)
    # SF5 handle time from the CRM against the ACD's accept-to-end time: the fortnight's ACD rows give each channel's
    # gap from the accept to the CRM's start, added to every interaction of the season on that channel
    rows, crm = AS.ask_b_rows(TARGET)
    gaps = {}
    for r in rows:
        if r["CRM Interaction"]:
            gaps.setdefault(r["Channel"], []).append(
                (AS._p(crm[r["CRM Interaction"]]) - AS._p(r["Answered (UTC)"])).total_seconds() / 60)
    mean_gap = {ch: float(np.mean(v)) for ch, v in gaps.items()}
    extra = np.array([mean_gap.get(ch, 0.0) for ch in P.channel])
    hm0 = P.hmin.copy()
    P.hmin = hm0 + extra
    E3 = C.Est(P)
    b_acd = C.golden(P, E3)["B"]
    P.hmin = hm0
    check("SF5 handle time from the ACD's accept instead of the CRM's start: same call", order(b_acd) == GOLD,
          "%.0f h" % b_acd)
    # SF6 the classes take contacts from go-live
    check("SF6 every 2027 class goes live before the fortnight", all(gl < f0 for gl, _ in P.classes27))
    # SF7 capacity per expert
    check("SF7 67.32 handle hours per expert in the standard", "67.320" in " ".join(DOC.STANDARD_SENTENCES))
    # SF8 rounding up to whole blocks
    check("SF8 rounded to the nearest block instead it is another call", K.round_half_up(B26 / 1000) * 1000 != GOLD,
          "%.0f" % (K.round_half_up(B26 / 1000) * 1000))
    # SF9 the rates over the whole season against the 2026 fortnight's weeks only: a construction, same call
    check("SF9 returning rates and q from the 2026 fortnight only: same call",
          order(cons["returning rates and q from the 2026 fortnight"]) == GOLD)
    # SF10 the 12 second-season returners at their late-2026 curve rather than the returning rate: same call
    late = C.expo(16.0, *E.cp)
    Kc, Kp = C.inhouse(P, lambda x: C.expo(x, *E.cp), lambda x: C.expo(x, *E.ca), E.pR, E.aR)
    Kp2 = Kp + 12 * C.H_EXPERT * 60 / E.aR * (late - E.pR)
    b10 = C.solve_booking(Kc, Kp2, E.pO, E.aO, E.q, P.F27)
    check("SF10 the 12 second-season returners at their late-2026 curve: same call", order(b10) == GOLD, "%.0f" % b10)
    # SF11 UTC dates instead of Eastern for the 2026 records
    day_e = P.day.copy()
    P.day = np.array([t.date().toordinal() for t in P.start_utc])
    P.wk = np.where(P.grp == "N", (P.day - P.golive) / 7.0, -1.0)
    E4 = C.Est(P)
    b_utc = C.golden(P, E4)["B"]
    P.day = day_e
    P.wk = np.where(P.grp == "N", (P.day - P.golive) / 7.0, -1.0)
    check("SF11 the 2026 records on UTC dates: same call", order(b_utc) == GOLD, "%.0f" % b_utc)
    # SF12 the French queue left in by mistake: same call
    P_fr = C.Pack(TARGET, queues=("Live Experts EN", "Live Experts FR"))
    E5 = C.Est(P_fr)
    b_fr = C.golden(P_fr, E5)["B"]
    check("SF12 the French queue's interactions left in the rates: same call", order(b_fr) == GOLD, "%.0f" % b_fr)
    # SF13 the vendor's handle time and rate from its fortnight against its three weeks: it worked only those
    check("SF13 Hillsborough worked only the three weeks to 3 May 2026",
          all(P.day[i] <= dt.date(2026, 5, 3).toordinal() and P.day[i] >= dt.date(2026, 4, 13).toordinal()
              for i in np.where(P.grp == "V")[0]))
    # SF14 the demand: the plan's 14 days summed
    check("SF14 the plan's fortnight is the demand: %d new cases, %.1f per cent on 2026's %d" % (
        P.F27, 100 * (P.F27 / P.F26 - 1), P.F26), abs(P.F27 / P.F26 - 1 - K.GROWTH_2027) < 0.0005)
    # SF15 each class's seats as filled
    check("SF15 the calendar's seats are 60 a class", all(n == 60 for _, n in P.classes27))
    # SF17 the standard's 0.85 handle hours a billed hour against Hillsborough's realised 2026 occupancy
    vh = P.hmin[fn26 & (P.grp == "V")].sum() / 60
    bill26 = sum(AS.ask_a(TARGET)["daily"].values())
    real = vh / bill26
    b_real = B26 * C.H_BILLED / real
    check("SF17 the realised 2026 occupancy in place of the filed 0.85 is another call", order(b_real) != GOLD,
          "%.3f realised, %.0f h" % (real, b_real))
    # SF16 contacts per case counted at case level (each case's contacts by its opener), not by fitting rates
    cpc = {}
    oo = P.order
    cs = P.case[oo]
    starts = np.r_[0, np.where(cs[1:] != cs[:-1])[0] + 1]
    ends = np.r_[starts[1:], len(cs)]
    opener = oo[starts]
    n_contacts = ends - starts
    for gname in "RV":
        m = P.grp[opener] == gname
        cpc[gname] = n_contacts[m].mean()
    check("SF16 contacts per case by opener agree with the rates (returning, Hillsborough)",
          abs(cpc["R"] - (1 + E.pR / (1 - E.q))) < 0.01 and abs(cpc["V"] - (1 + E.pO / (1 - E.q))) < 0.02,
          "R %.4f against %.4f; V %.4f against %.4f" % (cpc["R"], 1 + E.pR / (1 - E.q), cpc["V"], 1 + E.pO / (1 - E.q)))

    # ---------------------------------------------------------------------------------- the three rules (R)
    B = clean_world()
    Ec = clean_estimates(B)
    Pc = C.Pack(TARGET)
    b_easy = booking_from(Pc, Ec, contacts_per_case=Ec.M26)
    check("R3a the easy route on the clean truth files %d" % DEFAULT, order(b_easy) == DEFAULT, "%.0f h" % b_easy)
    b_dec = booking_from(Pc, Ec)
    check("R3b the decisive step alone files %d on the clean truth" % GOLD, order(b_dec) == GOLD, "%.0f h" % b_dec)
    b_r2 = booking_from(Pc, Ec, fixed_point=False)
    check("R3b the tenure curve without the vendor's own follow-ups stays wrong", order(b_r2) != GOLD, "%.0f" % b_r2)
    b_r2c = booking_from(Pc, Ec, vendor_rate=Ec.pR)
    check("R3b the tenure curve with the vendor at the returning rate stays wrong", order(b_r2c) != GOLD, "%.0f" % b_r2c)
    head = open(os.path.join(TARGET, RC.F_CRM), encoding="utf-8").readline()
    check("R1 the CRM ships interactions with their case, handler and handle time, and no repeat or tenure column",
          all(c in head for c in ("Case Number", "Handled By", "Talk Seconds", "Interaction Type"))
          and not re.search(r"repeat|resolved on|fcr|tenure|weeks", head, re.I))
    check("R1 the decisive computation reads the case structure (each case's later interactions)",
          P.followed.sum() > 30000)
    # R2: each Layer 1 item mishandled leaves the call (UTC dates, French queue, handle time basis asserted above)
    check("R2 UTC dates, the French queue and the ACD's handle time leave the call",
          order(b_utc) == order(b_fr) == order(b_acd) == GOLD)
    # R3c: no copied block in the CRM, no decoy figure in the thread
    txt = shipped_text()
    import email
    from email import policy
    thread = email.message_from_bytes(open(os.path.join(TARGET, DOC.F_THREAD), "rb").read(),
                                      policy=policy.default).get_body(preferencelist=("plain",)).get_content()
    check("R3c control: the decoded thread carries the recall's close", "150 of last season's English" in thread)
    check("R3c the planning thread carries no booking figure", not re.search(r"\b\d{1,2},\d{3}\s*(?:agent )?hours\b",
                                                                            thread))
    crm_rows = txt[RC.F_CRM].splitlines()[1:]
    blocks = {}
    for k in range(0, len(crm_rows) - 50, 997):
        sig = tuple(r.split(",", 2)[2][:60] for r in crm_rows[k:k + 20])
        blocks[sig] = blocks.get(sig, 0) + 1
    check("R3c no repeated block of CRM rows", max(blocks.values()) == 1)

    # ---------------------------------------------------------------------------------- the asks
    a = AS.ask_a(TARGET)
    ar = AS.ask_a_routes(TARGET)
    aw = AS.ask_a_week_routes(TARGET)
    b = AS.ask_b(TARGET, rows, crm)
    br = AS.ask_b_routes(TARGET, rows, crm)
    days = AS.fortnight_days()
    for k, r in ar.items():
        moved = sum(abs(K.round_half_up(r[d], 1) - K.round_half_up(a["daily"][d], 1)) >= 0.05 for d in days)
        print("   Ask A route %-50s moves %d of 14 days" % (k, moved))
    for k in ("Duration column by row start date", "sum of billable rows split at midnight"):
        moved = sum(abs(K.round_half_up(ar[k][d], 1) - K.round_half_up(a["daily"][d], 1)) >= 0.05 for d in days)
        check("ASK A %s misses every day" % k, moved == 14, "%d of 14" % moved)
    for k in ("Duration column, every login", "summed rows, every login", "summed rows, onboarding logins only"):
        moved = sum(abs(K.round_half_up(aw[k][w], 1) - K.round_half_up(a["unsupported"][w], 1)) >= 0.05 for w in AS.weeks())
        check("ASK A weekly %s misses both weeks" % k, moved == 2, "%s" % {str(w): round(v, 1) for w, v in aw[k].items()})
    conv = aw["union, every login, totals not agent by agent"]
    check("ASK A agent by agent and week totals converge (no agent billed under its records)",
          all(abs(conv[w] - a["unsupported"][w]) < 1e-6 for w in AS.weeks()))
    for k in ("each answered row, queued to answered", "per session, first queued to the answered row that reached the CRM"):
        moved = sum(int(K.round_half_up(br[k]["daily"][d])) != int(K.round_half_up(b["daily"][d])) for d in days)
        check("ASK B %s misses every day" % k[:60], moved == 14, "%d of 14" % moved)
        moved = sum(K.round_half_up(br[k]["share"][w], 1) != K.round_half_up(b["share"][w], 1) for w in AS.weeks())
        check("ASK B %s misses both weeks" % k[:60], moved == 2)
    # the asks' graded figures are records-fixed: every licensed reading lands on the same second, so a figure's
    # distance to its rounding edge guards only the rounding itself; each clears an exact tie by 1 per cent of a bin
    worst_a = min(K.edge_share(v, 0.1) for v in list(a["daily"].values()) + list(a["unsupported"].values()))
    worst_b = min(K.edge_share(v, 1.0) for v in b["daily"].values())
    worst_s = min(K.edge_share(v, 0.1) for v in b["share"].values())
    check("BINS every Ask A figure clears its rounding tie", worst_a >= 0.01, "nearest %.3f of a bin" % worst_a)
    check("BINS every average wait clears its rounding tie", worst_b >= 0.01, "nearest %.3f of a bin" % worst_b)
    check("BINS both shares clear their rounding ties", worst_s >= 0.01, "nearest %.3f of a bin" % worst_s)
    # convergence: each agent's union over logins equals the union login by login (no agent overlaps itself across
    # two logins), the invoice weeks hold the same hours in Atlantic and Eastern time, and every session with an
    # accepted offer reached a conversation in the CRM
    per_login = {}
    for login, sid, a0, a1 in AS.state_intervals(TARGET):
        per_login.setdefault(login, []).append((a0, a1))
    tot_login = sum((b_ - a_).total_seconds() for iv in per_login.values() for a_, b_ in AS._union(iv))
    by_agent = AS.billable_by_agent(TARGET, union=True)
    tot_agent = sum((b_ - a_).total_seconds() for iv in by_agent.values() for a_, b_ in iv)
    la = AS.login_agents(TARGET)
    tot_agent_logins = sum((b_ - a_).total_seconds() for lg, iv in per_login.items() if lg in la
                           for a_, b_ in AS._union(iv))
    check("CONVERGE union by agent equals union by login (to the second)", abs(tot_agent - tot_agent_logins) < 0.5,
          "%.0f s against %.0f s" % (tot_agent, tot_agent_logins))
    check("CONVERGE every billable login in the state detail maps to an onboarded agent", tot_login == tot_agent_logins,
          "%.0f s unmapped" % (tot_login - tot_agent_logins))
    bys = {}
    for r in rows:
        bys.setdefault(r["Session ID"], []).append(r)
    orphan = sum(1 for rs in bys.values() if any(r["Result"] == "Answered" for r in rs)
                 and not any(r["CRM Interaction"] for r in rs))
    multi = sum(1 for rs in bys.values() if sum(1 for r in rs if r["CRM Interaction"]) > 1)
    check("CONVERGE every session with an accepted offer reached one conversation in the CRM", orphan == 0 and multi == 0,
          "%d without, %d with two" % (orphan, multi))
    # readings that converge on the asks: no billable time on a fortnight Sunday after 23:00 Eastern (Atlantic
    # midnight), so the invoice weeks read in Atlantic or Eastern time hold the same hours
    late_sun = 0
    for login, sid, a0, a1 in AS.state_intervals(TARGET):
        if a0.weekday() == 6 and a1 > dt.datetime.combine(a0.date(), dt.time(23, 0)):
            late_sun += 1
    check("ASK A no billable time after 23:00 Eastern on a Sunday (Atlantic and Eastern weeks agree)", late_sun == 0,
          "%d rows" % late_sun)
    # the cracker's measured pair
    out, pair, PP_ = CR.main(TARGET)
    check("PAIR the measured pair ceiling is under 40", pair < 40.0, "%.1f" % pair)
    check("PAIR the cracker misses every ask figure", out["cracker"]["hits"] == 0, "%d" % out["cracker"]["hits"])
    check("PAIR mirror leakage under 35 per cent of ask weight", out["mirror"]["ask_share"] < 35.0,
          "%.1f" % out["mirror"]["ask_share"])

    # ---------------------------------------------------------------------------------- the separation line
    # the call's rows: the CRM's English interactions, the roster, the demand plan, the calendar, the standard, the
    # old ticketing files and the history; the asks' devices sit in the ACD exports, the invoices, the onboarding
    # list and the user list
    main_files = {RC.F_CRM, RC.F_ROSTER, RC.F_HISTORY, RC.F_OLD_A, RC.F_OLD_B, RC.F_DEMAND, DOC.F_CALENDAR, DOC.F_STANDARD}
    ask_files = {A.F_STATES, A.F_CONTACTS, A.F_USERS, A.F_ONBOARD, DOC.F_INVOICES, DOC.F_SCHEDULE_B, DOC.F_GUIDE}
    check("SEPARATION no ask file is one the call reads", not (main_files & ask_files))
    # deleting every ask file leaves the call (the pack read without them)
    check("SEPARATION the call reads none of the ask files (calc.py opens only the call's files)",
          all(f not in open(os.path.join(HERE, "calc.py")).read() or f == RC.F_CRM for f in
              (A.F_STATES, A.F_CONTACTS, A.F_USERS, A.F_ONBOARD)))

    # ---------------------------------------------------------------------------------- input gates and dates
    files = sorted(os.listdir(TARGET))
    exts = {os.path.splitext(f)[1] for f in files}
    check("GATES 10 or more files", len(files) >= 10, "%d" % len(files))
    check("GATES 3 or more formats", len(exts) >= 3, " ".join(sorted(exts)))
    big = max(sum(1 for _ in open(os.path.join(TARGET, f), encoding="utf-8")) for f in files if f.endswith(".csv"))
    check("GATES one file of 25,000 rows or more", big >= 25000, "%d" % big)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("GATES two or more distractors named in metadata.json", len(meta.get("distractor_files", [])) >= 2)
    late = []
    for f, t in txt.items():
        for m in re.finditer(r"\b(2026|2027)-(\d\d)-(\d\d)\b", t):
            d = dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            if d > K.AS_OF and f not in (RC.F_DEMAND,):
                late.append((f, d))
    check("DATES no record or document dated after the as-of (forward plans excepted)", not late, str(late[:3]))
    for f, phrase in ((DOC.F_STANDARD, "Service level is the share of"), (DOC.F_SCHEDULE_B, "HCS credits the difference"),
                      (DOC.F_CALENDAR, "15 February 2027"), (DOC.F_INVOICES, "replaces invoice HCS-26-0446"),
                      (DOC.F_GUIDE, "When the agent accepted the offer."), (DOC.F_CRM_NOTES, "when the conversation began")):
        check("CONTROL %s reads back with a known sentence" % f, phrase in re.sub(r"\s+", " ", txt[f]))
    persona_last = {p.split()[-1] for p in K.PEOPLE.values()}
    names_in_docs = set()
    for f in (DOC.F_STANDARD, DOC.F_SCHEDULE_B, DOC.F_CALENDAR, DOC.F_INVOICES, DOC.F_GUIDE, DOC.F_THREAD, DOC.F_CRM_NOTES):
        names_in_docs |= set(re.findall(r"\b([A-Z][a-z]+) ([A-Z][a-z]+)\b", txt[f]))
    check("PEOPLE the documents name only the build's personas", all(
        ("%s %s" % nm) in K.PEOPLE.values() or nm[1] not in persona_last for nm in names_in_docs))
    # the realism sweep: no identical invoice lines across agents, no repeated weekly counts in the old system, no
    # round headline figures, every ghost's length its own
    inv = AS.invoices(TARGET)
    for i in inv:
        if i["no"] == "HCS-26-0446":
            continue        # billed from the schedule, which gave every agent the same week (why it was replaced)
        hrs = [h for _, h in i["lines"]]
        check("REALISM %s: agents' billed hours spread like a time clock's" % i["no"], len(set(hrs)) >= len(hrs) - 7,
              "%d lines, %d distinct" % (len(hrs), len(set(hrs))))
    check("REALISM the demand plan's fortnight is not a round figure", P.F27 % 100 != 0, "%d" % P.F27)
    check("REALISM the 2026 fortnight's new cases are not a round figure", P.F26 % 100 != 0, "%d" % P.F26)
    sessions = {}
    for r in csv.DictReader(open(os.path.join(TARGET, A.F_STATES), encoding="utf-8")):
        if r["State"] == "Logged Out" and r["Reason Code"] in ("Session timeout", "Forced"):
            sessions[(r["Agent Login"], r["Session ID"])] = r["End (UTC)"]
    lens = []
    for r in csv.DictReader(open(os.path.join(TARGET, A.F_STATES), encoding="utf-8")):
        k = (r["Agent Login"], r["Session ID"])
        if k in sessions and r["End (UTC)"] == sessions[k] and r["State"] != "Logged Out":
            lens.append(int(r["Duration (s)"]))
    check("REALISM stale sessions' last states vary in length", len(set(lens)) > 0.5 * len(lens),
          "%d sessions, %d distinct lengths" % (len(lens), len(set(lens))))
    fails = [r for r in RESULTS if not r[1]]
    print("%d checks, %d FAIL" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

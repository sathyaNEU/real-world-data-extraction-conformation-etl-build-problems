"""task482's assertions on the cut pack and the generator's clean truth: the three rules (R1, R2 by Layer 1 item,
R3a to R3c), every semantic fork row (SF1 to SF17), the ladder (R0 to R6, MA30 to MA120), the golden's standing family
and margins (G1 to G7), the asks' devices (A1 to A9, B1 to B7), the separation line (X1 to X3), the realism sweep (S1
to S4) and the input gates (I1 to I5).

    python3 task482/generator/checks.py
"""
import copy
import datetime as dt
import csv
import itertools
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import warnings
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import asks as A      # noqa: E402
import bundle as B    # noqa: E402
import pack as P      # noqa: E402
import world as W     # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLD = [103, 106, 109, 201, 206, 303]
DEFAULT = [103, 106, 108, 201, 204, 206, 207, 301, 303, 309]
RESULTS = []


def check(name, ok):
    RESULTS.append((name, bool(ok)))
    print("%s  %s" % ("PASS" if ok else "FAIL", name))


def whole(h):
    return {no: B.hround(v) for no, v in h.items()}


def count(u, y, end, y0=B.Y0, y1=B.Y1, ge=False, hold=False):
    d = np.diff(np.append(u, end)).astype(float)
    if not hold:
        d = np.minimum(d, B.STEP)
    d = np.clip(d, 0, None)
    m = (u >= y0) & (u < y1)
    hot = (y >= B.LIMIT) if ge else (y > B.LIMIT)
    return float((d * hot * m).sum()) / 60.0


def hours_v(I, tau, ge=False, y0=B.Y0, y1=B.Y1, hold=False, until_collected=False, start=None):
    """the golden's hours under one reading of a convention"""
    out = {}
    for no in I.order:
        u, x = I.rec[no]
        if start is not None:
            c = np.exp(-np.diff(u).astype(float) / tau[no])
            v = np.empty(len(x))
            v[0] = start
            v[1:] = B.ifilter(x[:-1], c, start)
            v = np.concatenate([[start], v[1:]])
        else:
            v = B.states(u, x, tau[no])
        sw = I.switch.get(no, y1)
        if until_collected and no in I.cl:
            sw = int(u[-1]) + B.STEP
        k = u < sw
        h = count(u[k], v[k], min(sw, y1), y0, y1, ge, hold)
        if no in I.cl:
            cu, cx = I.cl[no]
            j = cu >= sw
            h += count(cu[j], cx[j], y1, y0, y1, ge, hold)
        out[no] = h
    return out


def clean_truth(E):
    """the analyst test on the generator's clean truth: each store's records straight from the world (UTC minutes,
    degrees C, no duplicates, no conversions), the easy route and the decisive step alone"""
    J = type("Clean", (), {})()
    J.order = sorted(W.BY_NO)
    J.make = {no: W.MAKES[W.make_of(no)][0] for no in J.order}
    J.pilot = sorted(W.PILOT)
    J.rec, J.cl, J.switch = {}, {}, {}
    for no in J.order:
        e = E[no]
        J.rec[no] = (e["rec_t"].astype(np.int64), np.round(e["rec_x"], 1))
        if no in W.PILOT:
            J.cl[no] = (e["cl_t"].astype(np.int64), np.round(e["cl_x"], 1))
            J.switch[no] = int(e["cl_t"][0])
    return J


def truth_hours(E):
    """the vaccine itself: the carton at each logger record's time stamp, the in-carton sensor after its first reading"""
    out = {}
    for no in sorted(W.BY_NO):
        e = E[no]
        u = e["rec_t"].astype(np.int64)
        sw = int(e["cl_t"][0]) if no in W.PILOT else B.Y1
        k = u < sw
        h = count(u[k], e["carton_at"][k], min(sw, B.Y1))
        if no in W.PILOT:
            h += count(e["cl_t"], np.round(e["cl_x"], 1), B.Y1)
        out[no] = h
    return out


def subset(keys):
    d = tempfile.mkdtemp(prefix="t482_")
    for k in keys:
        shutil.copy(os.path.join(TARGET, P.FILES[k]), os.path.join(d, P.FILES[k]))
    return d


def main():
    E = W.everything()
    F = A.simulate_stock(E)
    wos = A.brannon_history()
    I = B.Inputs(TARGET)
    tau = B.taus(I)
    G = B.golden_hours(I, tau)
    gw = whole(G)
    gset = B.covered(G)

    # ---------------------------------------------------------------------------------------------- the three rules
    J = clean_truth(E)
    r0c = {no: B.store_hours(J, no, J.rec[no][1]) for no in J.order}
    tc = B.taus(J)
    gc = B.golden_hours(J, tc)
    heads = []
    for k, fn in P.FILES.items():
        path = os.path.join(TARGET, fn)
        if fn.endswith(".csv"):
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    if "," in line and not line.startswith(("Kelvra", "Exported", "All times")):
                        heads.append((fn, line.strip()))
                        break
        elif fn.endswith(".xlsx"):
            import openpyxl
            wb = openpyxl.load_workbook(path, read_only=True)
            for ws in wb.worksheets:
                for row in ws.iter_rows(max_row=4, values_only=True):
                    heads.append((fn, " ".join(str(v) for v in row if v is not None)))
    held = [h for h in heads if re.search(r"(?i)hours? (above|over|out)|excursion|time above|above 8|vaccine temp",
                                          h[1])]
    check("R1 the field's raw material ships (paired logger and in-carton readings on the overlaps) and no shipped "
          "column holds the deciding quantity %s" % held, not held and all(len(B.overlap(I, no)[0]) > 1500
                                                                           for no in I.pilot))
    check("R3a analyst test on the clean truth: the loggers' own readings file the default %s" % B.covered(r0c),
          B.covered(r0c) == DEFAULT)
    check("R3b the decisive step alone on the clean truth (the lag fitted on the overlaps) files the golden %s"
          % B.covered(gc), B.covered(gc) == GOLD)
    check("R3b the cut pack files the golden %s and the default %s" % (gset, B.covered(B.rung_hours(I, "R0"))),
          gset == GOLD and B.covered(B.rung_hours(I, "R0")) == DEFAULT)
    tr = truth_hours(E)
    check("R3b the vaccine itself (cartons at the record times, the in-carton sensor after it) puts the same stores "
          "over the line %s" % B.covered(tr), B.covered(tr) == GOLD)
    check("R3b the default and the golden read the same records over the same window: the difference is the "
          "estimator alone", all(len(I.rec[no][0]) == len(J.rec[no][0]) -
                                 int((J.rec[no][0] < B.Y0).sum() + (J.rec[no][0] >= B.Y1).sum()) for no in I.order))
    rep = 0
    for no in I.order:
        u, x = I.rec[no]
        w = 72
        seen = {}
        for i in range(0, len(x) - w, w):
            key = tuple(np.round(x[i:i + w], 1))
            if key in seen and u[i] - seen[key] > 1440:
                rep += 1
            seen.setdefault(key, u[i])
    check("R3c no plant: no twelve-hour block of any store's record repeats at another time (%d), no memo, draft or "
          "stakeholder figure ships" % rep, rep == 0)

    # ------------------------------------------------------------------------------------------- standing family
    fam = {"pooled": B.golden_hours(I, B.taus(I, "pooled")), "per store": B.golden_hours(I, B.taus(I, "store")),
           "tau-0.5": B.golden_hours(I, tau, shift=-0.5), "tau+0.5": B.golden_hours(I, tau, shift=0.5),
           "record closes its interval": B.golden_hours(I, tau, prev=True),
           "state at the interval's end": B.golden_hours(I, tau, conv="end")}
    for k, v in fam.items():
        check("G1 standing family, %s: the same stores and every store's whole hours" % k,
              B.covered(v) == GOLD and whole(v) == gw)
    mean = B.golden_hours(I, tau, conv="mean")
    moved = {no: (gw[no], B.hround(mean[no])) for no in I.order if B.hround(mean[no]) != gw[no]}
    check("SF17 the interval mean (ruled out by 7.3, a record counts by its time stamp) keeps the call; moves %s"
          % moved, B.covered(mean) == GOLD)
    edge = min((0.5 - abs(G[no] - np.floor(G[no] + 0.5)), no) for no in I.order)
    check("G2 every store's hours sit at least a third of an hour inside their whole-hour bin (tightest %.3f, store %d)"
          % edge, edge[0] >= 0.33)
    lo_in = min(G[no] for no in gset)
    hi_out = max(G[no] for no in I.order if no not in gset)
    check("G3 the line's margins: lowest replaced %.2f, highest not replaced %.2f" % (lo_in, hi_out),
          lo_in >= 27.0 and hi_out <= 21.0)
    nb = B.nearest_below(G)
    second = sorted((v for no, v in G.items() if v < B.LINE), reverse=True)[1]
    check("G4 nearest below the line: store %d at %.2f, %.2f short; the next %.2f" % (nb[0], nb[1], nb[2], second),
          nb[0] == 306 and nb[1] - second >= 1.0 and all(B.nearest_below(v)[0] == 306 and
                                                       B.hround(B.nearest_below(v)[2]) == B.hround(nb[2])
                                                       for v in fam.values()))
    rms = {mk: B.fit(I, [no for no in I.pilot if I.make[no] == mk])[1] for mk in set(I.make.values())}

    def rms_of(f):
        s, n = 0.0, 0
        for no in I.pilot:
            u, x = I.rec[no]
            y = f(u, x)
            cu, cx = B.overlap(I, no)
            k = np.searchsorted(u, cu, side="right") - 1
            s += float(((y[k] - cx) ** 2).sum())
            n += len(cx)
        return np.sqrt(s / n)
    asrec = rms_of(lambda u, x: x)
    best_ma = min((rms_of(lambda u, x, k=k: B.trailing(u, x, k)), k) for k in (30, 45, 60, 90, 120))
    check("G5 the overlaps separate the estimators: the lag fits at %s C, the readings as recorded at %.3f, the best "
          "moving average (%d minutes) at %.3f" % ({k: round(v, 3) for k, v in rms.items()}, asrec, best_ma[1],
                                                   best_ma[0]),
          max(rms.values()) < 0.1 and asrec > 0.3 and best_ma[0] > 1.4 * max(rms.values()))
    check("G6 the per-make constants: %s" % {k: round(v, 2) for k, v in tau.items() if k in (101, 201, 301)},
          all(40.0 < v < 45.0 for v in tau.values()))
    tfam = [B.golden_hours(I, tau, shift=s) for s in (-1.0, -0.75, 0.75, 1.0)]
    check("G7 the call holds a full minute either side of each make's constant", all(B.covered(v) == GOLD for v in tfam))

    # ----------------------------------------------------------------------------------------------------- ladder
    ladder = {}
    for r in ("R0", "R1a", "R1b", "R1c", "R3", "R4", "R6", "MA30", "MA45", "MA60", "MA90", "MA120"):
        h = B.rung_hours(I, r)
        ladder[r] = B.covered(h)
        check("ladder %s files %s (not the golden)" % (r, ladder[r]), ladder[r] != GOLD)

    # --------------------------------------------------------------------------------------------------- fork rows
    check("SF1 the probe read as the vaccine files the default, and the overlaps refute it (%.3f C against %.3f)"
          % (asrec, max(rms.values())), ladder["R0"] == DEFAULT and asrec > 4 * max(rms.values()))
    geq = hours_v(I, tau, ge=True)
    mv = {no: (gw[no], B.hround(geq[no])) for no in I.order if B.hround(geq[no]) != gw[no]}
    check("SF2 at or above 8.0 (ruled out by 7.3's 'above 8.0'): the same call; moves %s, only in-carton readings at "
          "exactly 8.0" % mv, B.covered(geq) == GOLD and all(no in I.cl for no in mv))
    check("SF3 above 24.0: the same call (no store within an hour of the line)",
          all(abs(v - 24.0) > 1.0 for v in G.values()))
    check("SF4 the UTC year: the same whole hours", whole(hours_v(I, tau, y0=0, y1=525600)) == gw)
    check("SF5 a record standing for the ten minutes before it: the same whole hours", whole(fam["record closes its "
                                                                                               "interval"]) == gw)
    check("SF6 the pilot loggers until collection, the in-carton sensor after: the same whole hours",
          whole(hours_v(I, tau, until_collected=True)) == gw)

    def refit_shifted(make, shift_fn):
        K = copy.copy(I)
        K.rec = dict(I.rec)
        for no in I.order:
            if I.make[no] == make:
                u, x = I.rec[no]
                K.rec[no] = (u + shift_fn(u), x)
        return B.fit(K, [no for no in K.pilot if K.make[no] == make])[1]

    dst = lambda u: np.where((u >= B.local_to_u(dt.datetime(2026, 3, 8, 3))) &
                             (u < B.local_to_u(dt.datetime(2026, 11, 1, 1))), -60, 0)
    pw_mis = refit_shifted("Brumal", dst)
    kv_mis = refit_shifted("Kelvra", lambda u: np.where(dst(u) < 0, 300, 360))
    check("SF7 a clock misread shows on the overlaps: Brumal as daylight time %.3f C, Kelvra's UTC as local %.3f C"
          % (pw_mis, kv_mis), pw_mis > 3 * rms["Brumal"] and kv_mis > 3 * rms["Kelvra"])
    kf = copy.copy(I)
    kf.rec = {no: ((u, x * 9 / 5 + 32) if I.make[no] == "Kelvra" else (u, x)) for no, (u, x) in I.rec.items()}
    kh = {no: B.store_hours(kf, no, kf.rec[no][1]) for no in I.order}
    check("SF8 Kelvra's Fahrenheit read as Celsius puts every Kelvra store far over the line (not a live reading)",
          all(kh[no] > 1000 for no in I.order if I.make[no] == "Kelvra"))
    check("SF9 the last record held through each gap: the same whole hours", whole(hours_v(I, tau, hold=True)) == gw)
    check("SF10 the lag's grouping (pooled, per make, per store): the same whole hours",
          whole(fam["pooled"]) == gw and whole(fam["per store"]) == gw)
    check("SF11 the estimate started at the 5.0 setpoint: the same whole hours", whole(hours_v(I, tau, start=5.0)) == gw)
    two = {}
    for no in W.REPLACED:
        ser = P.logger_serials(no)
        two[no] = len(ser) == 2 and all(s in I.serial for s in ser)
    check("SF12 a replaced logger's two serials are one store's record in sequence %s" % two, all(two.values()))
    ua = B.unaccounted(I)
    cal = B.unaccounted(I, cut=False)
    check("SF13 ask A's balance between the counts' own times differs from the calendar year at the 30 December "
          "stores", all(ua[no] != cal[no] for no in A.COUNT_30DEC_2025 + W.COUNT_30DEC))
    check("SF14 ask A's receipts in doses: packages times doses per package (the item master)",
          all(d % 1 == 0 for (_, _, _, d) in I.receipts) and sum(d for (_, _, _, d) in I.receipts) >
          5 * sum(1 for _ in I.receipts))
    sv = B.service(I)
    check("SF15 ask B as invoiced with tax for work completed in 2026 (devices on the ask sheet)",
          all(B.hround(sv[no]) != B.hround(B.service(I, tax=False)[no]) for no in I.order))
    check("SF16 hours rounded once from the unrounded estimate: every store's figure equals the whole of its sum",
          all(isinstance(gw[no], int) for no in I.order))

    # ------------------------------------------------------------------------------- R2, the Layer 1 items one by one
    def mishandled(fn):
        K = copy.copy(I)
        K.rec = dict(I.rec)
        for no in I.order:
            r = fn(no, *I.rec[no])
            if r is not None:
                u, x = r
                o = np.argsort(u, kind="stable")
                u, x = u[o], x[o]
                keep = np.ones(len(u), bool)
                keep[1:] = u[1:] != u[:-1]
                K.rec[no] = (u[keep], x[keep])
        t = B.taus(K)
        h = B.golden_hours(K, t)
        rr = {mk: B.fit(K, [no for no in K.pilot if K.make[no] == mk])[1] for mk in set(K.make.values())}
        return B.covered(h), rr, t
    indst = lambda u: (u >= B.local_to_u(dt.datetime(2026, 3, 8, 3))) & (u < B.local_to_u(dt.datetime(2026, 11, 1, 1)))
    for name, mk, fn in [
            ("Brumal's UTC-6 read as daylight time", "Brumal",
             lambda no, u, x: (u - 60 * indst(u), x) if I.make[no] == "Brumal" else None),
            ("Kelvra's UTC read as Central wall time", "Kelvra",
             lambda no, u, x: (u + np.where(indst(u), 300, 360), x) if I.make[no] == "Kelvra" else None),
            ("Frostline's offsets dropped", "Frostline",
             lambda no, u, x: (u - np.where(indst(u), 300, 360), x) if I.make[no] == "Frostline" else None)]:
        cov, rr, t = mishandled(fn)
        loud = rr[mk] > 3 * rms[mk] and max(v for no, v in t.items() if I.make[no] == mk) > 70
        check("R2 %s: the overlap fit fails loudly (%.3f C against %.3f, the constant at the search bound), call %s"
              % (name, rr[mk], rms[mk], "held" if cov == GOLD else "moved"), loud)
    kd = copy.copy(I)
    kd.rec = dict(I.rec)
    u, x = I.rec[204]
    day = (u >= 349920) & (u < 349920 + 1440)
    kd.rec[204] = (np.concatenate([u, u[day]]), np.concatenate([x, x[day]]))
    o = np.argsort(kd.rec[204][0], kind="stable")
    kd.rec[204] = (kd.rec[204][0][o], kd.rec[204][1][o])
    check("R2 Kelvra's repeated day kept: the call and every store's whole hours unchanged",
          whole(B.golden_hours(kd, tau)) == gw)
    for no in W.REPLACED:
        ser = P.logger_serials(no)
        a_, b_ = P.replaced_at(no)
        for keep_old in (True, False):
            kr = copy.copy(I)
            kr.rec = dict(I.rec)
            u, x = I.rec[no]
            k = u < a_ if keep_old else u >= a_
            kr.rec[no] = (u[k], x[k])
            check("R2 store %d's %s logger dropped from the roster join: the call unchanged" % (no, "new" if keep_old
                                                                                              else "old"),
                  B.covered(B.golden_hours(kr, tau)) == GOLD)
    check("R2 the battery gaps held over: the call and every store's whole hours unchanged",
          whole(hours_v(I, tau, hold=True)) == gw)
    check("R2 the ask files' items (NDC forms, packages, the Lindqvist accounts, invoice against work dates) move only "
          "the asks: the call reads none of their files (X1)", True)

    # --------------------------------------------------------------------------------------------------- ask A
    U = A.unaccounted_truth(F)
    check("A1 ask A's golden equals the world's unrecorded losses at every store", all(ua[no] == U[no] for no in I.order))
    crack = B.unaccounted(I, cut=False, vials=False, credits=True)
    check("A2 the cracker (calendar year, write-offs as logged, credits off) misses all 30 (hits %d)"
          % sum(crack[no] == ua[no] for no in I.order), all(crack[no] != ua[no] for no in I.order))
    worst = 0
    for cut, vials, cred in itertools.product([True, False], repeat=3):
        if (cut, vials, cred) == (True, True, False):
            continue
        v = B.unaccounted(I, cut=cut, vials=vials, credits=cred)
        worst = max(worst, sum(v[no] == ua[no] for no in I.order))
    check("A3 no partial handling keeps more than 14 of 30 (worst %d)" % worst, worst <= 14)
    cred = defaultdict(int)
    for (no, t, d) in I.credits:
        cred[no] += d
    vial = defaultdict(int)
    for (no, t, ndc, q, cost) in I.writeoffs:
        if I.vial[ndc] and t < B.UPDATE:
            vial[no] += q
    d8 = set(A.COUNT_30DEC_2025) | set(W.COUNT_30DEC)
    check("A4 every store carries the credit device and a vial or count device",
          all(cred[no] > 0 and (vial[no] > 0 or no in d8) for no in I.order))
    combos = [(t, B.unaccounted(I, cut=t[0], vials=t[1], credits=t[2])) for t in itertools.product([True, False],
                                                                                                    repeat=3)
              if t != (True, True, False)]
    check("A5 no mix of mishandled devices composes back to the golden at a store that carries them",
          all(x[no] != ua[no] for no in I.order for (c, v, k), x in combos
              if (not c and no in d8) or (not v and vial[no] > 0) or k))
    check("A6 the cracker's figures look like stock records (none below 5: %d)" % min(crack.values()),
          min(crack.values()) >= 5)
    wo_lot = defaultdict(int)
    for (no, t, key, lot, doses, logged, reason) in [(no,) + x for no in F for x in F[no]["writeoffs"]]:
        if reason == "EXPIRED":
            wo_lot[(no, lot)] += doses
    cr_lot = defaultdict(int)
    for no in F:
        for (key, lot, units, doses) in F[no]["credits"]:
            cr_lot[(no, lot)] += doses
    check("A7 every credited dose was first written off as expired at its store (lot by lot)",
          all(wo_lot[k] >= v for k, v in cr_lot.items()))
    rows = list(csv.DictReader(open(os.path.join(TARGET, P.FILES["writeoffs"]), encoding="utf-8")))
    pre = [r for r in rows if r["product"].endswith("MDV") and r["written_off_at"] < "2026-06-01"]
    post = [r for r in rows if r["product"].endswith("MDV") and r["written_off_at"] >= "2026-06-01"]
    check("A8 the vial write-offs before the update cost a vial each (%d rows), the ones after a dose each (%d rows)"
          % (len(pre), len(post)), pre and all(abs(float(r["cost"]) / int(r["quantity"]) - (158.40 if "25-26" in
                                                                                               r["product"] else 162.30))
                                               < 0.01 for r in pre)
          and all(abs(float(r["cost"]) / int(r["quantity"]) - (15.84 if "25-26" in r["product"] else 16.23)) < 0.01
                  for r in post))
    d31 = defaultdict(int)
    d3125 = defaultdict(int)
    for (no, t, d) in I.admin:
        if t.date() == dt.date(2026, 12, 31):
            d31[no] += d
        if t.date() == dt.date(2025, 12, 31):
            d3125[no] += d
    check("A9 the 30 December counts: at least three doses given on 31 December at each of them",
          all(d31[no] >= 3 for no in W.COUNT_30DEC) and all(d3125[no] >= 3 for no in A.COUNT_30DEC_2025))

    # --------------------------------------------------------------------------------------------------- ask B
    T = A.service_truth(wos)
    check("B1 ask B's golden equals the work orders' truth at every store", all(abs(sv[no] - T[no]) < 0.011
                                                                              for no in I.order))
    nb_ = B.service(I, tax=False)
    check("B2 the cracker (each invoice once, amounts as exported) misses all 30",
          all(B.hround(nb_[no]) != B.hround(sv[no]) for no in I.order))
    part = {"no split": B.service(I, split=False), "tax by visit date": B.service(I, by_invoice_date=False),
            "rows summed": B.service(I, dedupe=False), "visit year": B.service(I, completed=False)}
    hits = {k: sum(B.hround(v[no]) == B.hround(sv[no]) for no in I.order) for k, v in part.items()}
    check("B3 partial handlings keep %s of 30" % hits, hits["no split"] <= 12 and min(hits.values()) <= 12)
    pre_inv = defaultdict(int)
    for w in wos:
        if w["completed"].year == 2026 and w["invoice_date"] < A.PLATFORM:
            for no in set(w["stores"]):
                pre_inv[no] += 1
    check("B4 every store has an invoice from before the platform move for 2026 work",
          all(pre_inv[no] > 0 for no in I.order))
    e2 = min((0.5 - abs(sv[no] - np.floor(sv[no] + 0.5)), no) for no in I.order)
    check("B5 every store's spend sits at least 15 cents inside its whole-dollar bin (tightest %.2f, store %d)" % e2,
          e2[0] >= 0.15)
    by_inv = defaultdict(list)
    for v in I.visits:
        by_inv[v["invoice"]].append(v)
    single = [vs[0] for vs in by_inv.values() if len(vs) == 1]
    pm_rows = [r for r in single if r["amount"] in (145.0, 128.0, 152.0, 120.0, 124.0, 153.7, 135.68, 161.12, 127.2,
                                                    131.44)]
    pre_ok = all(abs(r["amount"] - I.pm_price[I.unit[r["store"]]]) < 0.005 for r in pm_rows
                 if r["invoice_date"] < B.PLATFORM)
    post_ok = all(abs(r["amount"] - round(I.pm_price[I.unit[r["store"]]] * 1.06, 2)) < 0.005 for r in pm_rows
                  if r["invoice_date"] >= B.PLATFORM)
    n_pre = sum(1 for r in pm_rows if r["invoice_date"] < B.PLATFORM)
    n_post = sum(1 for r in pm_rows if r["invoice_date"] >= B.PLATFORM)
    check("B6 the tax switch is recoverable: maintenance-only invoices at Schedule B's price before July (%d) and at "
          "that price plus 6.0 per cent after (%d)" % (n_pre, n_post), pre_ok and post_ok and n_pre >= 2 and
          n_post >= 10)
    routes = [vs for vs in by_inv.values() if len(set(v["store"] for v in vs)) > 1]
    r_ok = all(abs(vs[0]["amount"] - sum(I.pm_price[I.unit[v["store"]]] for v in vs)) < 0.005 for vs in routes)
    check("B7 each maintenance route's amount is its stores' Schedule B prices (%d routes)" % len(routes),
          r_ok and len(routes) >= 10)

    # ------------------------------------------------------------------------------------------- separation line
    d = subset(["stores", "roster", "frostline", "kelvra", "brumal", "tellvane"])
    for k in ("invoices", "admin", "writeoffs", "credits", "transfers"):
        open(os.path.join(d, P.FILES[k]), "w").write(open(os.path.join(TARGET, P.FILES[k])).readline())
    for k in ("items", "inventory", "brannon", "agreement"):
        shutil.copy(os.path.join(TARGET, P.FILES[k]), os.path.join(d, P.FILES[k]))
    try:
        K = B.Inputs(d)
        same = whole(B.golden_hours(K, B.taus(K))) == gw
    except Exception as ex:                                       # noqa: BLE001
        print("   ", ex)
        same = False
    shutil.rmtree(d)
    check("X1 the call reads no ask file: the hours with the stock files emptied are unchanged", same)
    check("X2 the asks read no temperature file (asks.py and the ask functions in bundle.py take none)",
          "rec" not in B.unaccounted.__code__.co_names and "rec" not in B.service.__code__.co_names)
    dk = tempfile.mkdtemp(prefix="t482k_")
    for k in P.FILES:
        if k != "kelvra":
            os.symlink(os.path.join(TARGET, P.FILES[k]), os.path.join(dk, P.FILES[k]))
    seen, lines = set(), []
    for line in open(os.path.join(TARGET, P.FILES["kelvra"]), encoding="utf-8"):
        if line in seen and line[:1] == "K":
            continue
        seen.add(line)
        lines.append(line)
    open(os.path.join(dk, P.FILES["kelvra"]), "w").write("".join(lines))
    K = B.Inputs(dk)
    gk = B.golden_hours(K, B.taus(K))
    rk = B.rung_hours(K, "R0")
    shutil.rmtree(dk)
    check("X3 clean-data test (Kelvra's repeated day removed): the golden and the default unchanged and still apart",
          whole(gk) == gw and B.covered(rk) == DEFAULT and B.covered(gk) != B.covered(rk))

    # ------------------------------------------------------------------------------------------- realism sweep
    adm_tot = defaultdict(int)
    for (no, t, d) in I.admin:
        adm_tot[no] += d
    reccount = [len(I.rec[no][0]) for no in I.order]
    check("S1 no identical counts across stores: administrations %d distinct of 30, logger records %d distinct"
          % (len(set(adm_tot.values())), len(set(reccount))), len(set(adm_tot.values())) == 30 and
          len(set(reccount)) >= 20)
    longest = 0
    for no in I.order:
        x = I.rec[no][1]
        x = np.round(x * 9 / 5 + 32, 1) if I.make[no] == "Kelvra" else np.round(x, 1)     # each export's own unit
        ch = np.flatnonzero(np.diff(x) != 0)
        runs = np.diff(np.concatenate([[-1], ch, [len(x) - 1]]))
        longest = max(longest, int(runs.max()))
    check("S2 no constant stream: the longest unchanged run in any logger record is %d records" % longest,
          longest <= 72)
    persons = set(re.findall(r"\b(Breanna Graham|Julia Kaufman)\b", subprocess.run(
        ["pdftotext", os.path.join(TARGET, P.FILES["pilot"]), "-"], capture_output=True, text=True).stdout))
    check("S3 every persona is the card's (%s)" % sorted(persons), persons <= {"Breanna Graham", "Julia Kaufman"})
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    roundish = [no for no, x in figs["stores"].items() if x["service_usd"] % 100 == 0 or
                (x["doses_unaccounted"] % 100 == 0 and x["doses_unaccounted"] > 0)]
    check("S4 no round ask figure (a whole hundred) %s" % roundish, len(roundish) <= 1)

    # ----------------------------------------------------------------------------------------------- input gates
    fl = sorted(os.listdir(TARGET))
    exts = sorted(set(os.path.splitext(x)[1] for x in fl))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    rowsn = meta["rows"]
    check("I1 %d files in %d formats %s" % (len(fl), len(exts), exts), len(fl) >= 10 and len(exts) >= 3)
    check("I2 a file of 25,000 rows or more (%d)" % max(rowsn.values()), max(rowsn.values()) >= 25000)
    check("I3 two distractors named in metadata.json, neither named so in a file name",
          len(meta["distractor_files"]) >= 2 and not any("distract" in x for x in fl))
    bad = []
    for x in fl:
        p = os.path.join(TARGET, x)
        if x.endswith(".pdf"):
            txt = subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True).stdout
        elif x.endswith(".xlsx"):
            import zipfile
            txt = " ".join(zipfile.ZipFile(p).read(n).decode("utf-8", "ignore") for n in zipfile.ZipFile(p).namelist())
        else:
            txt = open(p, encoding="utf-8").read()
        for word in ("—", "–", "ReportLab", "openpyxl", "matplotlib", "lag", "time constant", "parallel run",
                     "overlap"):
            if word in txt and not (word == "lag" and not re.search(r"\blag\b", txt)):
                bad.append((x, word))
    check("I4 no dash, toolchain signature or stump word in a shipped file %s" % bad, not bad)
    last = {}
    last["administrations"] = max(t for (_, t, _) in I.admin)
    last["write-offs"] = max(t for (_, t, _, _, _) in I.writeoffs)
    last["deliveries"] = max(t for (_, t, _, _) in I.receipts)
    last["credits"] = max(t for (_, t, _) in I.credits)
    last["transfers"] = max(t for (_, _, _, t, _) in I.transfers)
    last["service invoices"] = max(dt.datetime.combine(v["invoice_date"], dt.time()) for v in I.visits)
    last["records"] = max(max(int(u[-1]) for (u, x) in I.rec.values()), max(int(u[-1]) for (u, x) in I.cl.values()))
    check("I5 the extracts end where they say: %s" % {k: str(v) for k, v in last.items()},
          last["service invoices"] <= dt.datetime(2027, 1, 22) and
          all(v <= dt.datetime(2026, 12, 31, 23, 59) for k, v in last.items() if k not in ("service invoices", "records"))
          and last["records"] < B.Y1)
    n_fail = sum(1 for _, ok in RESULTS if not ok)
    print("%d checks, %d failed" % (len(RESULTS), n_fail))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())

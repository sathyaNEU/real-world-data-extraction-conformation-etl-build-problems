"""task183 checks: every fork row, every assumption of the golden's method, the back-test, the ladder, the asks'
forcing numbers, the separation line and the input gates, asserted on the shipped files in target/ (calc.py reads
only target/), with the generator's truth (sim, asks) used only where a check compares the pack against it."""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import sys
from collections import defaultdict

import numpy as np
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A           # noqa: E402
import calc as C           # noqa: E402
import pack as PK          # noqa: E402
import sim as S            # noqa: E402
import world as W          # noqa: E402

FAILS = []
N = [0]


def ok(cond, label):
    N[0] += 1
    if not cond:
        FAILS.append(label)
        print("FAIL  " + label)


def call_of(P, fam):
    """The referral list a reading of the main call files, BCR-3 4.2 applied to the till customers."""
    tf = C.till_figures(P)
    fig = {c: (tf[c] if c in P.till_cids else fam[c]) for c in P.cust}
    return sorted(c for c in fig if fig[c] > C.LINE), fig


def bin5k(x):
    return int(5000 * round(x / 5000.0))


def run(target, golden, meta_path=None):
    P = C.Pack(target)
    F = W.FOCAL_CID
    fronts = sorted([F["front_carwash"], F["front_nails"]])
    heavies = sorted([F["cafe_heavy"], F["barber_heavy"]])
    fig, referred = C.golden(P)

    # ---- the call -------------------------------------------------------------------------------------------
    ok(sorted(referred) == fronts, "G1 the golden refers the car wash and the nail bar only: %s" % referred)
    ok(bin5k(fig[F["front_carwash"]]) == 100000 and bin5k(fig[F["front_nails"]]) == 50000,
       "G2 referral cash bins 100,000 and 50,000")
    others = [fig[c] for c in P.cust if c not in fronts]
    ok(max(others) < 15000, "G3 every other customer at least 25,000 under the line (max %.0f)" % max(others))
    # submission step 4 executed literally: lodged cash less the slope times the card trade of the windows the year's
    # lodgements carry, which is the intercept times the number of lodgements
    lods0, card0 = P.lodgements(), P.card_by_day()
    for key in ("front_carwash", "front_nails"):
        cid = F[key]
        pairs = [p for p in C.windows(lods0[cid], card0[cid]) if C.in_year(p[0])]
        a0, s0, _, _ = C.fit(pairs, "ols")
        lit = sum(L["amount"] for L, _, _ in pairs) - s0 * sum(w for _, w, _ in pairs)
        ok(abs(lit - fig[cid]) < 0.01 and abs(a0 * len(pairs) - fig[cid]) < 0.01,
           "G4 step 4 read literally gives %s %.2f (intercept %.2f x %d lodgements)" % (key, lit, a0, len(pairs)))

    # ---- the estimator family the data leave standing (every member: same call, same bins) -------------------
    fam = {}
    for name, kw in [("ols", {}), ("wls", dict(kind="wls")), ("huber", dict(kind="huber")),
                     ("days", dict(kind="days")), ("all history", dict(fit_on="all")),
                     ("gross of refunds", dict(net_refunds=False))]:
        r, f = call_of(P, C.unexplained(P, **kw))
        fam[name] = f
        ok(r == fronts, "F1 %s refers the same two" % name)
        ok(bin5k(f[F["front_carwash"]]) == 100000 and bin5k(f[F["front_nails"]]) == 50000,
           "F2 %s keeps both bins (%.0f, %.0f)" % (name, f[F["front_carwash"]], f[F["front_nails"]]))
    import deliver as DL
    bound = DL.others_bound(P, referred)
    yearcard = {}
    for cid in P.cust:
        pairs = [p for p in C.windows(lods0.get(cid, []), card0.get(cid, {})) if C.in_year(p[0])]
        _, s1, _, _ = C.fit(pairs, "ols")
        yearcard[cid] = sum(L["amount"] for L, _, _ in pairs) - s1 * sum(
            v for d, v in card0.get(cid, {}).items() if C.REVIEW_START <= d <= C.REVIEW_END)
    widest = max([f[c] for f in fam.values() for c in P.cust if c not in fronts] +
                 [yearcard[c] for c in P.cust if c not in fronts and c not in P.till_cids])
    ok(widest < bound and bound - widest < 1000, "G5 every other customer under EUR %d under every reading (widest "
                                                 "%.0f)" % (bound, widest))
    cw = [f[F["front_carwash"]] for f in fam.values()]
    nb = [f[F["front_nails"]] for f in fam.values()]
    ok(min(cw) > 97500 and max(cw) < 102500 and min(nb) > 47500 and max(nb) < 52500,
       "F3 SF11 family spread inside the bins: car wash %.0f to %.0f, nail bar %.0f to %.0f" % (min(cw), max(cw), min(nb),
                                                                                          max(nb)))

    # ---- the default path and the ladder ---------------------------------------------------------------------
    for stat in ("median", "mean", "pooled"):
        dfig, dref, info = C.default_path(P, stat)
        ok(sorted(dref) == heavies, "L1 the peer %s screen refers the cafe and the barber: %s" % (stat, dref))
    dfig, dref, info = C.default_path(P, "median")
    ok(dfig[F["cafe_heavy"]] > 100000 and 45000 < dfig[F["barber_heavy"]] < 60000,
       "L2 default figures cafe %.0f barber %.0f" % (dfig[F["cafe_heavy"]], dfig[F["barber_heavy"]]))
    ok(dfig[F["front_carwash"]] < 40000 and dfig[F["front_nails"]] < 40000,
       "L3 the default leaves both fronts under the line (%.0f, %.0f)" % (dfig[F["front_carwash"]],
                                                                         dfig[F["front_nails"]]))
    r0, f0 = call_of(P, C.unexplained(P, "origin"))
    ok(r0 == [], "L4 own ratio through the origin refers no one (car wash %.0f)" % f0[F["front_carwash"]])
    # Gate F on the clean truth: the cheap routes, counted
    cheap = {"peer median": dref, "peer mean": C.default_path(P, "mean")[1], "pooled": C.default_path(P, "pooled")[1],
             "own ratio": r0}
    landing = [k for k, v in cheap.items() if sorted(v) == fronts]
    ok(len(landing) == 0, "L5 no cheap route lands the call: %s" % landing)

    # ---- the decisive step forced by the fronts' own fit (the through-origin model refuted) -------------------
    lods, card = P.lodgements(), P.card_by_day()
    for key, lo_t in (("front_carwash", 30), ("front_nails", 15), ("cafe_heavy", None), ("barber_heavy", None)):
        cid = F[key]
        pairs = [p for p in C.windows(lods[cid], card[cid]) if C.in_year(p[0])]
        y = np.array([p[0]["amount"] for p in pairs])
        x = np.array([p[1] for p in pairs])
        X = np.column_stack([np.ones_like(x), x])
        b, res, *_ = np.linalg.lstsq(X, y, rcond=None)
        s0 = (x * y).sum() / (x * x).sum()
        rss1 = ((y - X @ b) ** 2).sum()
        rss0 = ((y - s0 * x) ** 2).sum()
        se = np.sqrt(rss1 / (len(y) - 2) * np.linalg.inv(X.T @ X)[0, 0])
        tval = b[0] / se
        corr = np.corrcoef(y - s0 * x, x)[0, 1]
        if lo_t:
            ok(tval > lo_t and rss0 / rss1 > 8 and corr < -0.9,
               "D1 %s: intercept t %.1f, through-origin RSS %.1fx, residual-card corr %.3f" % (key, tval, rss0 / rss1,
                                                                                             corr))
        else:
            ok(abs(tval) < 2.5 and rss0 / rss1 < 1.1,
               "D2 %s: no fixed part (t %.1f, RSS ratio %.2f)" % (key, tval, rss0 / rss1))

    # ---- lesson 12: the back-test on the records that observe what the golden estimates ----------------------
    tc = P.till_cash()
    paid = defaultdict(lambda: defaultdict(float))
    for r in P.till:
        paid[r["customer_id"]][dt.date.fromisoformat(r["trading_date"])] += float(r["paid_outs"])
    exact, total, icepts = 0, 0, []
    for cid in sorted(P.till_cids):
        net = {d: tc[cid][d] - paid[cid][d] for d in tc[cid]}
        pairs = C.windows(lods[cid], net)
        for L, w, _ in pairs:
            total += 1
            exact += abs(L["amount"] - w) < 0.005
        own = [p for p in C.windows(lods[cid], card[cid]) if C.in_year(p[0])]
        a, _, _, _ = C.fit(own, "ols")
        icepts.append(a)
    ok(exact == total and total > 1000, "B1 till back-test: %d of %d lodgements equal the till's net cash of their "
                                        "window to the cent" % (exact, total))
    ok(max(abs(a) for a in icepts) < 25, "B2 till customers' fitted fixed part per lodgement within 25 euro (%.1f to "
                                         "%.1f)" % (min(icepts), max(icepts)))
    rel = {c: info["ratio"][c] / info["peer"][P.cust[c]["Trade"]] - 1 for c in P.till_cids}
    ok(min(rel.values()) < -0.1 and max(rel.values()) > 0.1,
       "B3 the till customers' cash sits %.0f%% to +%.0f%% off their trade median: the peer screen mis-states "
       "them" % (100 * min(rel.values()), 100 * max(rel.values())))
    # the window convention closed by the record: the own-day window does not reproduce the tills
    wrong = 0
    for cid in sorted(P.till_cids):
        net = {d: tc[cid][d] - paid[cid][d] for d in tc[cid]}
        for L, w, _ in C.windows(lods[cid], net, include_day=True):
            wrong += abs(L["amount"] - w) >= 0.005
    ok(wrong > 0.9 * total, "SF4 the own-day window misses %d of %d till lodgements" % (wrong, total))
    # every other edge convention for the window: only the day-before window reproduces the tills, so the bins it
    # moves (the judge's [previous day, own day] puts the car wash at the 95,000 bin) are closed by the back-test
    def edge(series, ls, lo_off, hi_off):
        out = []
        for a_, b_ in zip(ls, ls[1:]):
            x, d = 0.0, a_["day"] + dt.timedelta(days=lo_off)
            while d <= b_["day"] + dt.timedelta(days=hi_off):
                x += series.get(d, 0.0)
                d += dt.timedelta(days=1)
            out.append((b_, x))
        return out
    for name, lo_off, hi_off in (("previous day to own day", 0, 0), ("day after previous to own day", 1, 0),
                                 ("day after previous to day before", 1, -1)):
        miss = 0
        for cid in sorted(P.till_cids):
            net = {d: tc[cid][d] - paid[cid][d] for d in tc[cid]}
            miss += sum(abs(L["amount"] - x) >= 0.005 for L, x in edge(net, lods[cid], lo_off, hi_off))
        figs_e = {}
        for key in ("front_carwash", "front_nails"):
            prs = [(L, x) for L, x in edge(card[F[key]], lods[F[key]], lo_off, hi_off) if C.in_year(L)]
            ye = np.array([L["amount"] for L, _ in prs])
            xe = np.array([x for _, x in prs])
            se = np.polyfit(xe, ye, 1)[0]
            figs_e[key] = ye.sum() - se * xe.sum()
        ok(miss > 0.9 * total, "SF4d window %s: misses %d of %d till lodgements; car wash %.0f (bin %d), nail bar %.0f "
                               "(bin %d)" % (name, miss, total, figs_e["front_carwash"], bin5k(figs_e["front_carwash"]),
                                             figs_e["front_nails"], bin5k(figs_e["front_nails"])))
        if lo_off == 0 and hi_off == 0:
            ok(bin5k(figs_e["front_carwash"]) == 95000 and bin5k(figs_e["front_nails"]) == 50000,
               "SF4e the judge's residual window keeps the call and moves the car wash to the 95,000 bin")
    times = [L["time"] for v in lods.values() for L in v]
    ok(max(times) < "13:00", "SF4b every lodgement handed in before 13:00 (latest %s)" % max(times))

    # ---- lesson 7: the golden's assumptions against the data ---------------------------------------------------
    # a ratio stable through the year: each legitimate card customer's quarterly slopes within 6% of its yearly one
    drift = []
    for cid in P.cust:
        if cid in P.till_cids or cid in fronts:
            continue
        pairs = [p for p in C.windows(lods[cid], card[cid]) if C.in_year(p[0])]
        _, sy, _, _ = C.fit(pairs, "ols")
        for q in range(4):
            lo = dt.date(2025, 10, 1) + dt.timedelta(days=91 * q)
            sub = [p for p in pairs if lo <= p[0]["day"] < lo + dt.timedelta(days=91)]
            if len(sub) > 8:
                drift.append(abs(C.fit(sub, "origin")[1] / sy - 1))
    ok(max(drift) < 0.08, "A1 quarterly own ratios within 8%% of the year's (max %.3f)" % max(drift))
    # no background: the legitimate customers' fixed parts are noise (median |t| under 1.5)
    tv = []
    for cid in P.cust:
        if cid in fronts:
            continue
        pairs = [p for p in C.windows(lods[cid], card[cid]) if C.in_year(p[0])]
        y = np.array([p[0]["amount"] for p in pairs])
        x = np.array([p[1] for p in pairs])
        X = np.column_stack([np.ones_like(x), x])
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        rss = ((y - X @ b) ** 2).sum()
        tv.append(abs(b[0] / np.sqrt(rss / (len(y) - 2) * np.linalg.inv(X.T @ X)[0, 0])))
    ok(np.median(tv) < 1.5 and max(tv) < 3.5, "A2 no fixed part outside the fronts (median |t| %.2f, max %.2f)" % (
        np.median(tv), max(tv)))

    # ---- the fork table ------------------------------------------------------------------------------------------
    r_inc, _ = call_of(P, C.unexplained(P, include_day=True))
    ok(r_inc != fronts, "SF4c the own-day window is a different call (%s), closed by SF4 and SF4b" % r_inc)
    r_set, _ = call_of(P, C.unexplained(P, card_basis="settlement"))
    ok(len(r_set) > 10, "SF5 settlement-dated card trade refers %d, closed by trading_date" % len(r_set))
    r_pos, _ = call_of(P, C.unexplained(P, lod_by="posted"))
    ok(r_pos != fronts, "SF2 posting-dated lodgements (%d referred), closed by BCR-3 3.2" % len(r_pos))
    ok(sorted(call_of(P, C.unexplained(P, net_refunds=False))[0]) == fronts, "SF6 refunds gross or net: same call")
    raw = C._rows(os.path.join(target, C.F["acct"]))
    refs = [r["Transaction Ref"] for r in raw]
    ok(len(refs) - len(set(refs)) == P.dupes > 1000, "SF7 the re-delivered quarter repeats %d rows under their own "
                                                     "references" % P.dupes)
    two = [c for c in P.cust if P.cust[c]["Second account"]]
    cur = {c: P.cust[c]["Current account"].split()[-1] for c in P.cust}
    alt = {}
    for cid in P.cust:
        own = [L for L in lods.get(cid, []) if L["acct"] == cur[cid]]
        pairs = [p for p in C.windows(own, card[cid]) if C.in_year(p[0])]
        a_, s_, _, _ = C.fit(pairs, "ols")
        alt[cid] = sum(L["amount"] for L, _, _ in pairs) - s_ * sum(w for _, w, _ in pairs)
    r_cur, _ = call_of(P, alt)
    on_second = sum(1 for c in two for L in lods.get(c, []) if L["acct"] != cur[c])
    ok(len(two) >= 3 and r_cur == fronts,
       "SF1 %d customers hold a second account (%d lodgements on them); the current account alone gives the same "
       "call (BCR-3 3.2: all accounts)" % (len(two), on_second))
    first = min(L["day"] for v in lods.values() for L in v)
    last = max(L["day"] for v in lods.values() for L in v)
    ok(first < C.REVIEW_START and last >= dt.date(2026, 9, 29), "SF3 the export covers the review year of BCR-3 2.2 "
                                                                 "(%s to %s)" % (first, last))
    ok(all(abs(fig[c]) < 10000 for c in P.till_cids), "SF8 till customers far under the line under 4.2")
    ok(min(cw) - C.LINE > 50000 and min(nb) - C.LINE > 7000, "SF9 both referrals clear the line under every member")

    # ---- shock test: the fronts are no extreme of any shipped statistic --------------------------------------
    for key in ("front_carwash", "front_nails"):
        cid = F[key]
        tr = P.cust[cid]["Trade"]
        peers = [c for c in P.cust if P.cust[c]["Trade"] == tr]
        sh = sorted(info["ratio"][c] for c in peers)
        ok(sh[0] < info["ratio"][cid] < sh[-1], "SH1 %s cash share %.3f inside its trade's range" % (key,
                                                                                                    info["ratio"][cid]))
    cash_sorted = sorted(info["cash"].values())
    ok(info["cash"][F["front_carwash"]] < cash_sorted[-3], "SH2 the car wash is not among the three largest lodgers")

    # ---- the asks: forcing numbers, ladders, separation ---------------------------------------------------------
    rows = C.ap_rows(target)
    old_rows = [r for r in rows if A.older_platform(r["office_code"], dt.date.fromisoformat(r["counter_date"]))]
    cents = [r for r in rows if not C._five(float(r["notes_eur"]))]
    old_coin = [r for r in old_rows if float(r["coin_eur"]) > 0]
    ok({r["ap_ref"] for r in cents} == {r["ap_ref"] for r in old_coin} and len(cents) > 1000,
       "K1 notes_eur off a whole five on exactly the older platform's coin rows (%d)" % len(cents))
    ok(all(C._five(round(float(r["notes_eur"]) - float(r["coin_eur"]), 2)) for r in cents),
       "K2 on each of them notes_eur less coin_eur is a whole five")
    review_accts = {P.cust[c]["Current account"].split()[-1] for c in P.cust}
    ok(not any(r["account_no"] in review_accts for r in cents), "K3 separation: no reviewed customer's row is a "
                                                                "device row")
    per_month_old = defaultdict(int)
    for r in old_coin:
        per_month_old[r["counter_date"][:7]] += 1
    ok(min(per_month_old[m] for m in C.MONTHS) >= 20, "K4 every month carries older-platform coin rows (min %d)" %
       min(per_month_old[m] for m in C.MONTHS))
    apg = C.ap_figures(target, "golden")
    for mode in ("plain", "notes_only"):
        alt = C.ap_figures(target, mode)
        miss = sum(abs(alt[m][1] - apg[m][1]) > 0.005 for m in C.MONTHS) + sum(
            abs(alt[m][2] - apg[m][2]) > 0.005 for m in C.MONTHS)
        ok(miss == 24, "K5 the %s reading misses %d of 24 An Post figures" % (mode, miss))
    for rule, need in (("half_even", 6), ("float", 6)):
        alt = C.ap_figures(target, "golden", rule)
        moved = sum(abs(alt[m][2] - apg[m][2]) > 0.005 for m in C.MONTHS)
        ok(moved >= need, "K8 SF12 Schedule 2's half-cent-up pin is load-bearing: %s rounding moves %d of 12 monthly fees" % (
            rule, moved))
    halves = sum(1 for r in rows if (Decimal("0.00065") * Decimal("%.2f" % C.ap_cash(r))) % Decimal("0.01") ==
                 Decimal("0.005"))
    ok(halves > 20, "K9 %d lodgements carry an exact half-cent handling fee" % halves)
    raw_ap = C._rows(os.path.join(target, C.F["ap"]))
    ok(len(raw_ap) - len(rows) > 20, "K6 the re-sent day: %d rows twice under the same ap_ref" % (len(raw_ap) -
                                                                                                 len(rows)))
    # the till log
    tl = C.tlog_rows(target)
    days = C.till_days(P, tl, "golden")
    cardd = P.card_by_day()
    uniq = 0
    for r, d in days:
        uniq += abs(cardd[r["customer_id"]][d] - float(r["card_sales"])) < 0.005
    ok(uniq == len(days) and len(days) > 9000, "T1 every Z-report's card sales equal its terminal's trade on its "
                                               "trading day (%d)" % uniq)
    seen = defaultdict(int)
    for r, d in days:
        seen[(r["till_account"], d)] += 1
    ok(max(seen.values()) == 1, "T2 one Z-report a trading day a till under the golden")
    by_at = defaultdict(int)
    for r in tl:
        by_at[(r["till_account"], r["received_at"])] += 1
    batches = sum(1 for v in by_at.values() if v > 1)
    ok(batches > 200, "T3 the received-date reading puts several Z-reports on one till-day %d times" % batches)
    # uniqueness of each batch Z's match inside its window
    amb = 0
    by_t = defaultdict(list)
    for r, d in days:
        by_t[r["till_account"]].append((int(r["z_no"]), d, r))
    for t, zs in by_t.items():
        zs.sort()
        prev = None
        for z, d, r in zs:
            at = dt.datetime.strptime(r["received_at"], "%Y-%m-%d %H:%M:%S")
            hi = at.date() - dt.timedelta(days=1) if at.hour < 12 else at.date()
            lo = prev if prev is not None else hi - dt.timedelta(days=21)
            cid = r["customer_id"]
            cands = [x for x, v in cardd[cid].items() if lo < x <= hi and abs(v - float(r["card_sales"])) < 0.005]
            amb += len(cands) != 1
            prev = d
    ok(amb == 0, "T4 every Z-report matches exactly one terminal day after its till's previous Z (%d ambiguous)" % amb)
    late_rule = 0
    for r, d in days:
        at = dt.datetime.strptime(r["received_at"], "%Y-%m-%d %H:%M:%S")
        hi = at.date() - dt.timedelta(days=1) if at.hour < 12 else at.date()
        cands = [x for x, v in cardd[r["customer_id"]].items() if x <= hi and abs(v - float(r["card_sales"])) < 0.005]
        late_rule += bool(cands) and max(cands) == d
    ok(late_rule == len(days), "T7 submission step 7 read literally (the latest matching day not after the receipt) "
                               "places %d of %d Z-reports as the golden does" % (late_rule, len(days)))
    seg_tills = {"TS-%d" % (700000 + int(c.split("-")[1])) for c in P.till_cids}
    seg_batch = sum(1 for (t, at), v in by_at.items() if t in seg_tills and v > 1)
    seg_late = sum(1 for r in tl if r["till_account"] in seg_tills and int(r["received_at"][11:13]) < 12)
    ok(seg_batch == 0 and seg_late == 0, "T5 separation: the reviewed till customers send each Z the evening it closes")
    tg = C.till_figures_ask(P, target, "golden")
    for mode, need in (("received", 24), ("cracker", 24), ("terminal_count", 12)):
        alt = C.till_figures_ask(P, target, mode)
        miss = sum(abs(alt[m][i] - tg[m][i]) > 0.005 for m in C.MONTHS for i in (1, 2))
        ok(miss >= need, "T6 the %s reading misses %d of 24 till figures" % (mode, miss))
    # the reviewed customers' post office lodgements agree with the account file wherever they meet
    ap_by = defaultdict(float)
    for r in rows:
        if r["account_no"] in review_accts:
            ap_by[(r["account_no"], r["counter_date"])] += float(r["notes_eur"]) + float(r["coin_eur"])
    acc_by = defaultdict(float)
    for cid, v in lods.items():
        for L in v:
            if L["channel"] == "post" and C.in_year(L) and W.next_working(L["day"]) <= C.REVIEW_END:
                acc_by[(P.cust[cid]["Current account"].split()[-1], L["day"].isoformat())] += L["amount"]
    late = [k for k in ap_by if k not in acc_by]
    ok(all(W.next_working(dt.date.fromisoformat(k[1])) > C.REVIEW_END for k in late),
       "SF10 the reviewed customers' post office lodgements absent from the account file are the %d credited after 30 "
       "September" % len(late))
    agree = sum(abs(ap_by[k] - acc_by[k]) < 0.005 for k in ap_by if k in acc_by)
    ok(agree == len(ap_by) - len(late) and agree > 500, "K7 the reviewed customers' An Post rows equal their account "
                                                 "credits (%d of %d days)" % (agree, len(ap_by)))

    # ---- figures.json and the input gates ----------------------------------------------------------------------
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    ok([r["customer"] for r in figs["referrals"]] == referred, "R1 figures.json referrals")
    ok(all(abs(figs["an_post"][m]["cash_eur"] - apg[m][1]) < 0.005 for m in C.MONTHS), "R2 figures.json An Post")
    ok(all(abs(figs["till"][m]["cash_sales_eur"] - tg[m][1]) < 0.005 for m in C.MONTHS), "R3 figures.json till")
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "I1 %d files" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "I2 formats")
    big = max(sum(1 for _ in open(os.path.join(target, f))) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, "I3 largest file %d rows" % big)
    if meta_path and os.path.exists(meta_path):
        meta = json.load(open(meta_path))
        ok(len(meta.get("distractors", [])) >= 2, "I4 distractors named")
        ok(all(x.get("source") and x.get("date") and x.get("license") for x in meta["files"]), "I5 provenance")
        names = " ".join(files)
        ok(not any(w in names for w in ("decoy", "distractor", "trap", "fixed", "front")), "I6 no telling file name")
    print("checks: %d run, %d failed" % (N[0], len(FAILS)))
    if FAILS:
        raise SystemExit(1)


if __name__ == "__main__":
    TASK = os.path.dirname(HERE)
    run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), os.path.join(TASK, "metadata.json"))

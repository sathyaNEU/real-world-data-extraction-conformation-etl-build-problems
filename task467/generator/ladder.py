"""The rungs and the back-test, measured on target/ alone: every complete pipeline a competent solver could file for
the main call, and what the labelled records (all of 2025 and the stragglers still arriving on prepaid labels in
January 2026) say about each pairing."""
import collections
import datetime as dt

import numpy as np
import pandas as pd

import bundle as B
import golden as G
import world as W


def label_truth(target):
    """{process id: delivery time} for every opening whose record carries a prepaid label (the label is the parcel's
    goods-in barcode)."""
    p = B.processing(target)
    d = B.deliveries(target).set_index("barcode")
    lab = p[p.label != ""]
    return {pid: d.t.get(bc) for pid, bc in zip(lab.id, lab.label)}


def agreement(target, pairing, truth):
    ok = sum(1 for k, v in truth.items() if pairing.get(k) is not None and v is not None and pairing[k] == v)
    same_day = sum(1 for k, v in truth.items() if pairing.get(k) is not None and v is not None
                   and pairing[k].date() == v.date())
    return ok, same_day, len(truth)


def by_day_newest(target):
    """The date-level rung: each day's openings take the newest delivery day still holding parcels, every parcel of a
    day counted as waiting from the day's start."""
    d = B.deliveries(target)
    p = B.processing(target)
    days = collections.defaultdict(list)
    for t in d.t:
        days[t.date()].append(t)
    out = {}
    order = sorted(set(days) | set(p.t.dt.date))
    avail = []
    popen = collections.defaultdict(list)
    for pid, t in zip(p.id, p.t):
        popen[t.date()].append(pid)
    for day in order:
        if day in days:
            avail.append(day)
        for pid in popen.get(day, []):
            while avail and not days[avail[-1]]:
                avail.pop()
            out[pid] = days[avail[-1]].pop() if avail else None
    return out


def random_order(target):
    """The rung that takes every waiting parcel as equally likely to be opened: the expected composition of each
    day's openings by delivery day, carried day by day (a fluid replay)."""
    d = B.deliveries(target)
    p = B.processing(target)
    day0 = min(d.t.min().date(), p.t.min().date())
    ndays = (max(d.t.max().date(), p.t.max().date()) - day0).days + 1
    arr = np.bincount([(t.date() - day0).days for t in d.t], minlength=ndays).astype(float)
    opn = np.bincount([(t.date() - day0).days for t in p.t], minlength=ndays).astype(float)
    pool = np.zeros(ndays)
    comp = {}
    for k in range(ndays):
        pool[k] += arr[k]
        n = opn[k]
        if n <= 0:
            continue
        tot = pool[:k + 1].sum()
        share = pool[:k + 1] / tot
        comp[k] = share.copy()
        pool[:k + 1] -= share * min(n, tot)
    return comp, day0


def expected_late_random(target):
    comp, day0 = random_order(target)
    rf = B.refund_table(target, {})
    out = {}
    for (y, mo) in W.WINDOW_MONTHS:
        sel = rf[(pd.to_datetime(rf.day).dt.year == y) & (pd.to_datetime(rf.day).dt.month == mo)]
        tot = 0.0
        for opened, made in zip(sel.opened, sel.day):
            k = (opened.date() - day0).days
            c = comp[k]
            lim = (made - day0).days - W.LATE_DAY      # delivered on or before this day index -> late
            if lim >= 0:
                tot += c[:min(lim, len(c) - 1) + 1].sum()
        out["%d-%02d" % (y, mo)] = (int(len(sel)), int(round(tot)))
    return out


def carried_2025(target, truth):
    """The rung that carries each 2025 month's late share, read off the labelled 2025 refunds, to the same month of
    2026."""
    rf = B.refund_table(target, truth)
    rf = rf[pd.to_datetime(rf.day).dt.year == 2025]
    days = (pd.to_datetime(rf.day) - pd.to_datetime(rf.delivered.dt.date)).dt.days
    share = {}
    for mo in range(1, 13):
        sel = pd.to_datetime(rf.day).dt.month == mo
        share[mo] = float((days[sel] >= W.LATE_DAY).mean())
    made = B.monthly(B.refund_table(target, B.replay(target, "newest")))
    return {k: (v[0], int(round(v[0] * share[int(k[5:])]))) for k, v in made.items()}


def processing_as_delivery(target):
    p = B.processing(target)
    return dict(zip(p.id, p.t))


def back_test(target, truth):
    """2025 by month: refunds made late as the labels date them, as the newest-first replay dates them, and as
    arrival order dates them; and the mean days from delivery to opening under each (order-free)."""
    out = {}
    pairs = {"labels": truth, "newest": B.replay(target, "newest"), "arrival": B.replay(target, "oldest")}
    for name, pr in pairs.items():
        m = B.refund_table(target, pr)
        m = m[pd.to_datetime(m.day).dt.year == 2025]
        days = (pd.to_datetime(m.day) - pd.to_datetime(m.delivered.dt.date)).dt.days
        mm = pd.to_datetime(m.day).dt.month
        out[name] = {"%d" % k: int(((days >= W.LATE_DAY) & (mm == k)).sum()) for k in range(1, 13)}
        o = B.processing(target)
        o = o[(o.t >= pd.Timestamp(2025, 1, 1)) & (o.t < pd.Timestamp(2026, 1, 1))]
        w = [(t - pr[i]).total_seconds() / 86400 for i, t in zip(o.id, o.t) if pr.get(i) is not None]
        out[name + "_mean_wait_days"] = round(float(np.mean(w)), 3)
    return out


def ladder(target):
    truth = label_truth(target)
    newest = B.replay(target, "newest")
    rungs = {
        "r0_opened_as_delivered": B.monthly(B.refund_table(target, processing_as_delivery(target))),
        "r1_arrival_order": B.monthly(B.refund_table(target, B.replay(target, "oldest"))),
        "r2_2025_shares_carried": carried_2025(target, truth),
        "r3_random_order": expected_late_random(target),
        "r4_newest_from_empty_2026": B.monthly(B.refund_table(target, {**newest, **B.replay(
            target, "newest", start=pd.Timestamp(2026, 1, 1))})),
        "r5_newest_by_day": B.monthly(B.refund_table(target, by_day_newest(target))),
        "hours_reading": B.monthly(B.refund_table(target, newest), hours=True),
        "refunds_only_replay": B.monthly(B.refund_table(target, B.replay(target, "newest", refunds_only=True))),
    }
    out = {}
    for name, mon in rungs.items():
        rows, pay, breach, late = G.call_figures(mon)
        out[name] = {"payment_gbp": pay, "breach_months": breach, "late_total": late,
                     "late": {k: rows[k]["refunds_late"] for k in rows}}
    ok_n, sd_n, n_lab = agreement(target, newest, truth)
    ok_a, sd_a, _ = agreement(target, B.replay(target, "oldest"), truth)
    ok_d, sd_d, _ = agreement(target, by_day_newest(target), truth)
    ok_r, _, _ = agreement(target, B.replay(target, "newest", refunds_only=True), truth)
    lab26 = {k: v for k, v in truth.items() if v is not None and v >= pd.Timestamp(2026, 1, 1)}
    ok26, _, n26 = agreement(target, newest, lab26)
    return {"rungs": out,
            "labels": {"labelled_openings": n_lab, "newest_exact": ok_n, "arrival_exact": ok_a, "arrival_same_day": sd_a,
                       "by_day_exact": ok_d, "by_day_same_day": sd_d, "refunds_only_exact": ok_r, "labelled_2026": n26, "newest_exact_2026": ok26},
            "backtest_2025": back_test(target, truth)}

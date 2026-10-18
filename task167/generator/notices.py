"""task167 notices: the funds' cash flows as the general partners noticed them, vehicle by vehicle, in currency
units, with the netting, cancellations and the 2016 handover the two administrators' files carry."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as C
import records as R
import world as W

CALL_KINDS = ("invest", "fee", "offset", "expense", "org")
DIST_KINDS = ("roc", "gain", "income")
LINE_NAME = {"invest": "Investments", "fee": "Management fees", "offset": "Management fee offset", "expense": "Partnership expenses",
             "org": "Organisational expenses", "roc": "Return of capital", "gain": "Realised gain", "income": "Income"}
LAST_VALUE = W.AS_OF


class Notice:
    __slots__ = ("vehicle", "kind", "value_date", "notice_date", "lines", "ref", "status", "seq", "legacy_ref")

    def __init__(self, vehicle, kind, value_date, notice_date, lines):
        self.vehicle, self.kind, self.value_date, self.notice_date, self.lines = vehicle, kind, value_date, notice_date, lines
        self.ref, self.status, self.seq, self.legacy_ref = None, "Settled", 0, None

    def calls(self):
        return sum(a for k, a in self.lines.items() if k in CALL_KINDS)

    def dists(self):
        return sum(a for k, a in self.lines.items() if k in DIST_KINDS)


def _day(month, day):
    d = W.month_start(month)
    return C.roll_business(d.replace(day=min(day, 28)))


def build_notices(funds, recs, until=None):
    """every notice of every vehicle with a value date up to `until` (default the as-of date), in date order"""
    until = until or LAST_VALUE
    out = []
    for f in funds:
        rng = np.random.default_rng([W.SEED, 11, f.id])
        flows = recs[f.id][0]
        by_m = {}
        for x in flows:
            by_m.setdefault(x.month, []).append(x)
        for m in sorted(by_m):
            items = by_m[m]
            calls = [x for x in items if x.kind in CALL_KINDS]
            dists = [x for x in items if x.kind in DIST_KINDS]
            # a general partner sets a realisation against a call on one notice only late in a fund's life, and pays
            # loan income on its own notices
            age = m - W.month_index(f.first_close)
            u = rng.random()
            net = bool(calls and dists and age >= 60 and all(x.kind != "income" for x in dists) and u < 0.10)
            cday = min(x.day for x in calls) if calls else None
            dday = min(x.day for x in dists) if dists else None
            for veh in f.vehicles:
                def lines_of(xs):
                    agg = {}
                    for x in xs:
                        agg[x.kind] = agg.get(x.kind, 0.0) + x.amount
                    return {k: round(v * 1e6 * veh.share, 2) for k, v in agg.items() if abs(round(v * 1e6 * veh.share, 2)) > 0}
                if net:
                    vd = _day(m, cday)
                    ln = lines_of(calls)
                    ln.update(lines_of(dists))
                    out.append(Notice(veh, "net", vd, C.business_day_before(vd, 10), ln))
                else:
                    if calls:
                        vd = _day(m, cday)
                        out.append(Notice(veh, "call", vd, C.business_day_before(vd, 10), lines_of(calls)))
                    if dists:
                        vd = _day(m, dday)
                        out.append(Notice(veh, "dist", vd, C.business_day_before(vd, 2), lines_of(dists)))
    out = [n for n in out if n.value_date <= until and n.lines]
    out.sort(key=lambda n: (n.value_date, n.vehicle.code, n.kind))
    return out


def assign_refs(notices, cancelled):
    """the current administrator's references, in notice-date order within each year, for every notice it holds
    (value dates from 1 April 2016, the cancelled ones included), and the legacy numbers before 1 July 2016"""
    pre = {"call": "CN", "dist": "DN", "net": "CD"}
    cur = [n for n in notices if n.value_date >= W.HANDOVER_START] + list(cancelled)
    cur.sort(key=lambda n: (n.notice_date, n.vehicle.code, n.kind, n.status))
    seq = {}
    for n in cur:
        y = n.notice_date.year
        seq[y] = seq.get(y, 0) + 1
        n.ref = "%s-%d-%05d" % (pre[n.kind], y, 1000 + seq[y] * 3 + (hash_code(n.vehicle.code) % 3))
    lseq = {}
    for n in sorted([n for n in notices if n.value_date <= W.LEGACY_CUTOFF], key=lambda n: (n.notice_date, n.vehicle.code, n.kind)):
        y = n.notice_date.year
        lseq[y] = lseq.get(y, 0) + 1
        n.legacy_ref = "%02d/%04d" % (y % 100, lseq[y])
    return notices


def hash_code(s):
    h = 0
    for ch in s:
        h = (h * 131 + ord(ch)) % 1000003
    return h


def cancellations(notices):
    """twelve call notices from 2017 to 2025 that went out wrong, were cancelled and were reissued: returns the
    cancelled notices (the reissue is the settled notice already in the list)"""
    rng = np.random.default_rng([W.SEED, 13])
    pool = [n for n in notices if n.kind == "call" and dt.date(2017, 1, 1) <= n.value_date <= dt.date(2025, 12, 31)
            and "fee" in n.lines and len(n.lines) >= 2]
    pick = sorted(rng.choice(len(pool), 12, replace=False))
    out = []
    for i in pick:
        n = pool[int(i)]
        bad = dict(n.lines)
        k = "fee" if rng.random() < 0.6 else ("invest" if "invest" in bad else "fee")
        bad[k] = round(bad[k] * float(rng.choice([1.25, 0.8, 1.1, 1.5])), 2)
        c = Notice(n.vehicle, "call", n.value_date, C.business_day_before(n.notice_date, 3), bad)
        c.status = "Cancelled"
        out.append(c)
        # the reissue goes out a few days after the cancelled notice, for the same value date
        n.notice_date = C.business_day_before(n.value_date, 7)
    return out

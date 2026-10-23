"""task178 calc: every graded figure and every rung, computed from the shipped files under target/ (never from the
generator's state), so the goldens, figures.json and checks.py all read the pack as a solver would."""
from __future__ import annotations

import csv
import datetime as dt
import math
import os
from collections import defaultdict

import numpy as np
import openpyxl

import common as C


def _rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


# ------------------------------------------------------------------------------------------------ the hourly record
class Record:
    """the 2024 to 2026 hourly record as the release note defines it: reports of record, operations as dealt, local
    hours, hour marks; an hour whose closing mark is missing is joined to the next hour"""

    def __init__(self, target, fam_july="drop", resubmissions="last", clock="local", cancelled="drop"):
        self.t = target
        reg = {r["dealer_code"]: r for r in _rows(os.path.join(target, C.F_DEALERS))}
        flows = defaultdict(float)
        last = {}
        for r in _rows(os.path.join(target, C.F_FLOWS)):
            d = dt.date.fromisoformat(r["report_date"])
            to = reg[r["dealer_code"]]["of_record_to"]
            if fam_july == "drop" and to and d > dt.date.fromisoformat(to):
                continue
            key = (d, int(r["hour"][:2]), r["dealer_code"])
            if resubmissions == "last":
                if key not in last or r["received_at"] >= last[key][0]:
                    last[key] = (r["received_at"], float(r["net_customer_usd_k"]))
            elif resubmissions == "first":
                if key not in last or r["received_at"] < last[key][0]:
                    last[key] = (r["received_at"], float(r["net_customer_usd_k"]))
            elif resubmissions == "sum":
                flows[(key[0], key[1])] += float(r["net_customer_usd_k"]) / 1000.0
        if resubmissions in ("last", "first"):
            for (d, h, _), (_, v) in last.items():
                flows[(d, h)] += v / 1000.0
        ops = defaultdict(float)
        for r in _rows(os.path.join(target, C.F_OPS)):
            if cancelled == "drop" and r["status"] == "ANULADA":
                continue
            t = dt.datetime.strptime(r["dealt_at"], "%Y-%m-%d %H:%M:%S")
            if clock == "utc":
                t = C.utc_to_local(t)
            a = float(r["amount_usd_k"]) / 1000.0 * (1 if r["operation"] == "VENTA" else -1)
            ops[(t.date(), t.hour)] += a
        mids = {}
        for r in _rows(os.path.join(target, C.F_MID)):
            mids[(dt.date.fromisoformat(r["session_date"]), int(r["hour_mark"][:2]))] = float(r["mid_tqp_per_usd"])
        days = sorted({d for d, _ in mids})
        self.days = days
        r_obs, f_obs, i_obs, day_of = [], [], [], []
        self.close = {}
        self.open = {}
        for d in days:
            self.close[d] = mids[(d, C.CLOSE_H)]
            self.open[d] = mids[(d, C.OPEN_H)]
            prev_mark, fsum, isum = C.OPEN_H, 0.0, 0.0
            for hh in C.HOURS:
                fsum += flows.get((d, hh), 0.0)
                isum += ops.get((d, hh), 0.0)
                if (d, hh + 1) not in mids:
                    continue
                r_obs.append(100.0 * math.log(mids[(d, hh + 1)] / mids[(d, prev_mark)]))
                f_obs.append(fsum)
                i_obs.append(isum)
                day_of.append(d)
                prev_mark, fsum, isum = hh + 1, 0.0, 0.0
        self.r = np.array(r_obs)
        self.f = np.array(f_obs)
        self.i = np.array(i_obs)
        self.day_of = np.array([days.index(d) for d in day_of])
        self.bank_day = np.zeros(len(days))
        np.add.at(self.bank_day, self.day_of, self.i)
        cl = np.array([self.close[d] for d in days])
        self.dchg = 100.0 * np.diff(np.log(cl))          # daily closing changes, the first session has none
        self.dbank = self.bank_day[1:]
        self.year = np.array([d.year for d in days])[1:]
        self.hyear = np.array([days[k].year for k in self.day_of])

    def vol(self, lam=0.0):
        d = self.dchg + lam * self.dbank
        return math.sqrt(C.ANN * np.mean(d ** 2))


def ols_slope(y, x):
    X = np.column_stack([np.ones(len(x)), x])
    return float(np.linalg.lstsq(X, y, rcond=None)[0][1])


def ols_two(y, x1, x2):
    X = np.column_stack([np.ones(len(x1)), x1, x2])
    return np.linalg.lstsq(X, y, rcond=None)[0]


def iv_slope(y, x, z):
    y, x, z = y - y.mean(), x - x.mean(), z - z.mean()
    return float(z @ y / (z @ x))


# ------------------------------------------------------------------------------------------------ the call
def impacts(rec):
    r, f, i = rec.r, rec.f, rec.i
    out = {}
    out["ols_net"] = ols_slope(r, f - i)
    out["reduced_form"] = ols_slope(r, f)
    b = ols_two(r, f, i)
    out["two_regressor"] = -float(b[2])
    out["two_regressor_customer"] = float(b[1])
    q = i == 0
    out["no_bank_hours"] = ols_slope(r[q], f[q])
    out["iv_hourly"] = iv_slope(r, f - i, f)
    s_hat = ols_slope(i, f)
    out["absorbed_share"] = s_hat
    out["ratio"] = out["reduced_form"] / (1.0 - s_hat)
    out["iv_sign"] = iv_slope(r, f - i, np.sign(f))
    # daily grain
    nd = len(rec.days)
    R = np.zeros(nd)
    Fd = np.zeros(nd)
    Id = np.zeros(nd)
    np.add.at(R, rec.day_of, r)
    np.add.at(Fd, rec.day_of, f)
    np.add.at(Id, rec.day_of, i)
    out["iv_daily"] = iv_slope(R, Fd - Id, Fd)
    yrs = sorted(set(rec.hyear))
    out["iv_by_year"] = {y: iv_slope(r[rec.hyear == y], (f - i)[rec.hyear == y], f[rec.hyear == y]) for y in yrs}
    return out


def call(target, **kw):
    rec = Record(target, **kw)
    imp = impacts(rec)
    res = {"record_vol": rec.vol(0.0)}
    for k in ("ols_net", "reduced_form", "two_regressor", "two_regressor_customer", "no_bank_hours", "iv_hourly",
              "ratio", "iv_sign", "iv_daily"):
        res["vol_" + k] = rec.vol(imp[k])
    # one impact per year, each year's sessions put back at its own impact
    d = rec.dchg.copy()
    for y, lam in imp["iv_by_year"].items():
        d[rec.year == y] += lam * rec.dbank[rec.year == y]
    res["vol_iv_by_year"] = math.sqrt(C.ANN * np.mean(d ** 2))
    # the structural sum: impact times customer flow plus the hour's own residual, overnight kept
    lam = imp["iv_hourly"]
    resid = rec.r - lam * (rec.f - rec.i)
    hourly_free = lam * rec.f + resid
    nd = len(rec.days)
    Hd = np.zeros(nd)
    np.add.at(Hd, rec.day_of, hourly_free)
    on = np.array([100.0 * math.log(rec.open[rec.days[k]] / rec.close[rec.days[k - 1]]) for k in range(1, nd)])
    res["vol_structural"] = math.sqrt(C.ANN * np.mean((on + Hd[1:]) ** 2))
    # the variance-ratio scaling of the record by the customers' flow against the net flow, day by day
    Fd = np.zeros(nd)
    Id = np.zeros(nd)
    np.add.at(Fd, rec.day_of, rec.f)
    np.add.at(Id, rec.day_of, rec.i)
    res["vol_variance_ratio"] = res["record_vol"] * math.sqrt(np.var(Fd) / np.var(Fd - Id))
    # the record on sessions the Bank did not deal in
    res["vol_no_bank_sessions"] = math.sqrt(C.ANN * np.mean(rec.dchg[rec.dbank == 0] ** 2))
    res["impacts"] = imp
    res["n_hours"] = int(len(rec.r))
    res["n_sessions"] = int(len(rec.dchg))
    res["golden"] = res["vol_iv_hourly"]
    res["setting"] = math.ceil(res["golden"])
    return res


GOLDEN_FAMILY = ("vol_iv_hourly", "vol_ratio", "vol_iv_sign", "vol_iv_daily", "vol_iv_by_year", "vol_structural")
RIVALS = ("record_vol", "vol_ols_net", "vol_reduced_form", "vol_two_regressor", "vol_two_regressor_customer",
          "vol_no_bank_hours", "vol_variance_ratio", "vol_no_bank_sessions")


# ------------------------------------------------------------------------------------------------ ask A: hedging cost
def band_of(k_usd):
    for name, lo, hi in C.SIZE_BANDS:
        if lo <= k_usd < hi:
            return name
    raise ValueError(k_usd)


def ask_a(target, grouping="order", drop_cancelled=True):
    """dollar-weighted cost per dollar against the arrival mid, pesos, by 2026 quarter and order size band. An order
    is one arrival: one trader, one side, one millisecond stamp."""
    orders = defaultdict(list)
    for r in _rows(os.path.join(target, C.F_CONF)):
        if drop_cancelled and r["status"] == "CANCELLED":
            continue
        t = dt.datetime.strptime(r["trade_time_utc"], "%Y-%m-%dT%H:%M:%S.%fZ")
        loc = C.utc_to_local(t)
        key = (r["trader"], r["side"], r["trade_time_utc"]) if grouping == "order" else (r["confirmation_id"],)
        if grouping == "second":
            key = (r["side"], r["trade_time_utc"][:19])
        orders[key].append((loc, r["side"], float(r["usd_amount_k"]), float(r["price"]), float(r["bid_at_arrival"]),
                            float(r["ask_at_arrival"])))
    num, den = defaultdict(float), defaultdict(float)
    for key, fills in orders.items():
        loc = fills[0][0]
        size = sum(f[2] for f in fills)
        cell = (C.quarter(loc.date()), band_of(size))
        for (_, side, q, px, bid, ask) in fills:
            sgn = 1.0 if side == "BUY" else -1.0
            num[cell] += q * sgn * (px - (bid + ask) / 2.0)
            den[cell] += q
    return {cell: num[cell] / den[cell] for cell in den}, len(orders)


# ------------------------------------------------------------------------------------------------ ask B: forwards due in 2027
def read_forwards(target):
    wb = openpyxl.load_workbook(os.path.join(target, C.F_FWD), read_only=True)
    ws = wb["Deals"]
    it = ws.iter_rows(values_only=True)
    head = next(it)
    out = []
    for row in it:
        r = dict(zip(head, row))
        for k in ("Trade date", "Maturity date", "Window opens"):
            if isinstance(r[k], dt.datetime):
                r[k] = r[k].date()
        out.append(r)
    return out


def ask_b(target, net_windows=True, drop_internal=True, usd_only=True, drop_cancelled=True):
    seg = {int(r["client_no"]): r["segment"] for r in _rows(os.path.join(target, C.F_CLIENTS))}
    deals = read_forwards(target)
    if drop_cancelled:
        deals = [d for d in deals if d["Status"] != "ANULADA"]
    if usd_only:
        deals = [d for d in deals if d["Pair"] == "USD/TQP"]
    if drop_internal:
        deals = [d for d in deals if seg[int(d["Client No."])] != "TESORERIA"]
    windows = [d for d in deals if d["Product"] == "WINDOW"]
    used = defaultdict(float)
    drawdowns = set()
    if net_windows:
        for w in windows:
            for d in deals:
                if (d["Product"] == "OUTRIGHT" and d["Client No."] == w["Client No."] and d["Client USD"] == w["Client USD"]
                        and abs(d["Forward rate"] - w["Forward rate"]) < 0.005
                        and w["Window opens"] <= d["Maturity date"] <= w["Maturity date"]):
                    used[w["Deal No."]] += d["Notional"]
                    drawdowns.add(d["Deal No."])
    sell, buy, who = defaultdict(float), defaultdict(float), defaultdict(set)
    for d in deals:
        m = d["Maturity date"]
        if m.year != 2027:
            continue
        amt = d["Notional"]
        if d["Product"] == "WINDOW" and net_windows:
            amt = d["Notional"] - used[d["Deal No."]]
        if amt <= 0.5:
            continue
        q = C.quarter(m)
        s = seg[int(d["Client No."])]
        if s == "EXPORTADOR" and d["Client USD"] == "VENDE":
            sell[q] += amt
        elif s == "IMPORTADOR" and d["Client USD"] == "COMPRA":
            buy[q] += amt
        who[q].add(d["Client No."])
    return ({q: sell[q] / 1e6 for q in range(1, 5)}, {q: buy[q] / 1e6 for q in range(1, 5)},
            {q: len(who[q]) for q in range(1, 5)}, len(drawdowns))

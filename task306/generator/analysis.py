"""The golden analysis, run on the cut pack (target/) only: the desk's executions conformed and its cost curve fitted,
each candidate's twelve months of rebalances priced at GBP 400 million, the call, the routes a solver might take, and
the two asks. Every routine takes the handling it applies as an argument, so the checks and the ceiling script can
run the other readings on the same files."""
import csv
import datetime as dt
import math
import os
import re
from collections import defaultdict

import numpy as np
import openpyxl
import pyarrow.parquet as pq

AUM = 400_000_000.0
WINDOW = (dt.date(2025, 12, 1), dt.date(2026, 11, 30))
LIVE_NAMES = ["UK Equity Income", "UK Mid Cap Growth", "UK Smaller Companies", "UK Dynamic"]
F = {
    "master": "wealdmoor_security_master_2026-11-30.csv",
    "market": "lse_daily_market_data_2025-2026.parquet",
    "backtests": "research_backtests_2027_candidates.xlsx",
    "trades": "backtest_rebalance_trades_2025-2026.csv",
    "orders": "oms_orders_2025-2026.csv",
    "fills": "oms_fills_2025-2026.csv",
    "accounts": "trading_account_register.csv",
    "allocations": "oms_block_allocations_2025-2026.csv",
}


def rows(target, k):
    with open(os.path.join(target, F[k]), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def london_date(utc):
    """A UTC stamp's London trade date (BST from the last Sunday of March to the last Sunday of October)."""
    t = dt.datetime.strptime(utc, "%Y-%m-%dT%H:%M:%SZ")

    def last_sunday(y, m):
        x = dt.date(y, m, 31)
        return x - dt.timedelta(days=(x.weekday() + 1) % 7)
    d = t.date()
    bst = last_sunday(d.year, 3) <= d < last_sunday(d.year, 10)
    return (t + dt.timedelta(hours=1 if bst else 0)).date()


class Pack:
    def __init__(self, target):
        self.target = target
        self.master = {r["sedol"]: r for r in rows(target, "master")}
        self.by_isin = {r["isin"]: r["sedol"] for r in self.master.values()}
        self.tier = {s: {"FTSE 100": "L", "FTSE 250": "M", "FTSE SmallCap": "S"}[r["index_band"]]
                     for s, r in self.master.items()}
        t = pq.read_table(os.path.join(target, F["market"])).to_pydict()
        series = defaultdict(list)
        for s, d, c, v in zip(t["sedol"], t["trade_date"], t["close_gbx"], t["volume_shares"]):
            series[s].append((d, c, v))
        self.mkt = {}
        self.cons = {}
        for s, r in self.master.items():
            m = re.search(r"effective (\d\d)/(\d\d)/(\d{4})", r["corporate_action_note"])
            if m:
                self.cons[s] = dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        for s, ser in series.items():
            ser.sort()
            self.mkt[s] = ser
        self.days = sorted({d for ser in self.mkt.values() for d, _c, _v in ser})
        self.day_ix = {d: i for i, d in enumerate(self.days)}
        self._cache = {}

    def adv_vol(self, s, d, adv_n=20, vol_n=60):
        """The 20-session average daily traded value (GBP) and the 60-session daily volatility (bps) before d."""
        key = (s, d, adv_n, vol_n)
        if key in self._cache:
            return self._cache[key]
        ser = self.mkt[s]
        dates = [x[0] for x in ser]
        import bisect
        i = bisect.bisect_left(dates, d)
        lo = max(0, i - adv_n)
        vals = [ser[j][1] / 100.0 * ser[j][2] for j in range(lo, i)]
        adv = sum(vals) / len(vals)
        rets = []
        for j in range(max(1, i - vol_n), i):
            if s in self.cons and ser[j][0] == self.cons[s]:
                continue                                   # the consolidation day's tenfold price is no return
            rets.append(math.log(ser[j][1] / ser[j - 1][1]))
        vol = float(np.std(rets, ddof=1)) * 1e4
        self._cache[key] = (adv, vol)
        return adv, vol


def executions(P, dedupe=True, units=True, failover=True):
    """The desk's orders, conformed: one row per order with its account, stock, side, London trade date, arrival
    mid, filled quantity and value, average fill price and shortfall in bps."""
    orders = {r["order_id"]: r for r in rows(P.target, "orders")}
    fills = rows(P.target, "fills")
    seen = set()
    by_order = defaultdict(list)
    for f in fills:
        if dedupe:
            if f["exec_id"] in seen:
                continue
            seen.add(f["exec_id"])
        px = float(f["fill_price"])
        if units and f["price_unit"] == "GBP":
            px *= 100.0
        by_order[f["order_id"]].append((int(f["fill_qty"]), px))
    # a re-created order is the original order: the backup's order for the same account, stock and side that day,
    # carrying exactly the quantity the terminated original had left
    parent = {}
    if failover:
        term = defaultdict(list)
        for o in orders.values():
            if o["status"] == "TERMINATED":
                filled = sum(q for q, _p in by_order.get(o["order_id"], []))
                term[(o["account_code"], o["sedol"], o["side"], london_date(o["created_utc"]),
                      int(o["order_qty"]) - filled)].append(o["order_id"])
        for o in orders.values():
            if o["source"] == "BACKUP-RECOVERY":
                k = (o["account_code"], o["sedol"], o["side"], london_date(o["created_utc"]), int(o["order_qty"]))
                if len(term.get(k, [])) == 1:
                    parent[o["order_id"]] = term[k][0]
    merged = defaultdict(list)
    for oid, fl in by_order.items():
        merged[parent.get(oid, oid)].extend(fl)
    out = []
    for oid, fl in merged.items():
        o = orders[oid]
        q = sum(x for x, _p in fl)
        if q == 0:
            continue
        avg = sum(x * p for x, p in fl) / q
        arr = float(o["arrival_mid_gbx"])
        side = 1 if o["side"] == "BUY" else -1
        d = london_date(o["created_utc"])
        out.append(dict(order_id=oid, account=o["account_code"], sedol=o["sedol"], side=side, date=d,
                        arrival=arr, qty=q, value=q * arr / 100.0, avg=avg,
                        shortfall=side * (avg - arr) / arr * 1e4))
    out.sort(key=lambda x: x["order_id"])
    return out


def with_size(P, ex, adv_n=20, vol_n=60):
    for e in ex:
        adv, vol = P.adv_vol(e["sedol"], e["date"], adv_n, vol_n)
        e["part"] = e["value"] / adv
        e["vol"] = vol
        e["tier"] = P.tier[e["sedol"]]
    return ex


# ------------------------------------------------------------------------ cost models a solver might fit or take

def fit_sqrt_vol(ex):
    """The golden: shortfall = a_band + k * daily vol * sqrt(participation), least squares over the desk's orders."""
    X = np.array([[1.0 if e["tier"] == t else 0.0 for t in "LMS"] + [e["vol"] * math.sqrt(e["part"])] for e in ex])
    y = np.array([e["shortfall"] for e in ex])
    c, *_ = np.linalg.lstsq(X, y, rcond=None)
    a = dict(zip("LMS", c[:3]))
    return lambda tier, p, vol: a[tier] + c[3] * vol * math.sqrt(p)


def fit_sqrt_band(ex):
    """Per band: shortfall = a + b * sqrt(participation), no volatility term."""
    co = {}
    for t in "LMS":
        sub = [e for e in ex if e["tier"] == t]
        X = np.array([[1.0, math.sqrt(e["part"])] for e in sub])
        y = np.array([e["shortfall"] for e in sub])
        co[t], *_ = np.linalg.lstsq(X, y, rcond=None)
    return lambda tier, p, vol: co[tier][0] + co[tier][1] * math.sqrt(p)


def fit_power(ex):
    """Per band: shortfall = a + b * participation ** g, g fitted on a grid."""
    best = {}
    for t in "LMS":
        sub = [e for e in ex if e["tier"] == t]
        y = np.array([e["shortfall"] for e in sub])
        bestg = None
        for g in np.arange(0.30, 0.85, 0.025):
            X = np.array([[1.0, e["part"] ** g] for e in sub])
            c, res, *_ = np.linalg.lstsq(X, y, rcond=None)
            sse = float(((X @ c - y) ** 2).sum())
            if bestg is None or sse < bestg[0]:
                bestg = (sse, g, c)
        best[t] = bestg
    return lambda tier, p, vol: best[tier][2][0] + best[tier][2][1] * p ** best[tier][1]


def binned(ex):
    """Per band: the value-weighted shortfall of the desk's orders in participation bins, read off at each trade's
    participation (linear between bin centres in log participation)."""
    edges = [0, 0.002, 0.005, 0.01, 0.02, 0.04, 0.08, 0.15, 0.25, 1.0]
    tab = {}
    for t in "LMS":
        pts = []
        for lo, hi in zip(edges, edges[1:]):
            sub = [e for e in ex if e["tier"] == t and lo <= e["part"] < hi]
            if len(sub) < 15:
                continue
            v = sum(e["value"] for e in sub)
            pts.append((math.log(sum(e["part"] * e["value"] for e in sub) / v),
                        sum(e["shortfall"] * e["value"] for e in sub) / v))
        tab[t] = pts

    def f(tier, p, vol):
        pts = tab[tier]
        x = math.log(max(p, 1e-6))
        if x <= pts[0][0]:
            return pts[0][1]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            if x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        (x0, y0), (x1, y1) = pts[-2], pts[-1]
        return y1 + (y1 - y0) * (x - x1) / (x1 - x0)
    return f


def band_average(ex, weighted=True):
    """The easy route: the desk's average shortfall per pound (or per order) in each band, whatever the size."""
    a = {}
    for t in "LMS":
        sub = [e for e in ex if e["tier"] == t]
        if weighted:
            a[t] = sum(e["shortfall"] * e["value"] for e in sub) / sum(e["value"] for e in sub)
        else:
            a[t] = sum(e["shortfall"] for e in sub) / len(sub)
    return lambda tier, p, vol: a[tier]


def flat(bps):
    return lambda tier, p, vol: bps


# ------------------------------------------------------------------------ the candidates priced at GBP 400 million

def candidates(P):
    wb = openpyxl.load_workbook(os.path.join(P.target, F["backtests"]), read_only=True, data_only=True)
    out = {}
    for r in list(wb["Summary"].iter_rows(values_only=True))[1:]:
        out[r[0]] = dict(code=r[0], name=r[1], alpha=float(str(r[5]).rstrip("%")) / 100.0)
    trades = defaultdict(list)
    for r in rows(P.target, "trades"):
        d = dt.date.fromisoformat(r["rebalance_date"])
        if WINDOW[0] <= d <= WINDOW[1]:
            trades[r["strategy_code"]].append((d, P.by_isin[r["isin"]], float(r["traded_weight"])))
    for code in out:
        out[code]["trades"] = sorted(trades[code])
    return out


def price(P, cands, model, aum=AUM, adv_n=20, vol_n=60):
    res = {}
    for code, c in cands.items():
        cost = traded = 0.0
        parts = []
        for d, s, w in c["trades"]:
            adv, vol = P.adv_vol(s, d, adv_n, vol_n)
            v = abs(w) * aum
            p = v / adv
            parts.append(p)
            traded += v
            cost += v * model(P.tier[s], p, vol) / 1e4
        gross = c["alpha"] * aum
        res[code] = dict(name=c["name"], gross=gross, cost=cost, net=gross - cost, traded=traded,
                         rebalances=len({d for d, _s, _w in c["trades"]}), p_median=float(np.median(parts)),
                         p_max=float(max(parts)))
    return res


def call(res):
    r = sorted(res.items(), key=lambda kv: -kv[1]["net"])
    return r[0][0], r[1][0], r[0][1]["net"] - r[1][1]["net"], r


# ------------------------------------------------------------------------ the asks

def account_owner(P, account, d, dated=True):
    """The live strategy an account code belongs to on a trade date (the register is dated)."""
    reg = rows(P.target, "accounts")
    hits = []
    for r in reg:
        if r["account_code"] != account:
            continue
        if dated:
            if dt.date.fromisoformat(r["opened"]) <= d and (not r["closed"] or d <= dt.date.fromisoformat(r["closed"])):
                hits.append(r["account_name"])
        else:
            hits.append(r["account_name"])
    if not hits:
        return None
    return hits[0]


def allocated(P, ex, blocks=True):
    """The desk's orders as the portfolios own them: each block order split into its post-trade allocations (each
    at the block's arrival mid and average price); without the allocations a block stays on the block account."""
    if not blocks:
        return ex
    al = defaultdict(list)
    for r in rows(P.target, "allocations"):
        al[r["block_order_id"]].append((r["account_code"], int(r["allocated_qty"])))
    out = []
    for e in ex:
        if e["order_id"] in al:
            for acct, q in al[e["order_id"]]:
                out.append(dict(e, account=acct, qty=q, value=q * e["arrival"] / 100.0))
        else:
            out.append(e)
    return out


def ask_shortfall(P, ex, dated=True):
    """Each live strategy's value-weighted shortfall in each quarter of 2026, bps."""
    acc = defaultdict(lambda: [0.0, 0.0])
    for e in ex:
        if e["date"].year != 2026:
            continue
        who = account_owner(P, e["account"], e["date"], dated)
        if who not in LIVE_NAMES:
            continue
        q = (e["date"].month - 1) // 3 + 1
        acc[(who, q)][0] += e["shortfall"] * e["value"]
        acc[(who, q)][1] += e["value"]
    return {(n, q): acc[(n, q)][0] / acc[(n, q)][1] for n in LIVE_NAMES for q in (1, 2, 3, 4)}


def ask_traded(P, ex, dated=True):
    """Each live strategy's traded value in each half of 2026, GBP: filled quantity at the average fill price."""
    acc = defaultdict(float)
    for e in ex:
        if e["date"].year != 2026:
            continue
        who = account_owner(P, e["account"], e["date"], dated)
        if who not in LIVE_NAMES:
            continue
        h = 1 if e["date"].month <= 6 else 2
        acc[(who, h)] += e["qty"] * e["avg"] / 100.0
    return {(n, h): acc[(n, h)] for n in LIVE_NAMES for h in (1, 2)}


def run(target):
    P = Pack(target)
    ex = with_size(P, executions(P))
    cands = candidates(P)
    models = {"golden": fit_sqrt_vol(ex), "sqrt by band": fit_sqrt_band(ex), "power by band": fit_power(ex),
              "binned": binned(ex), "band average (value)": band_average(ex, True),
              "band average (orders)": band_average(ex, False), "flat 10 bps": flat(10.0)}
    priced = {k: price(P, cands, m) for k, m in models.items()}
    win, runner, gap, ranked = call(priced["golden"])
    return dict(P=P, ex=ex, cands=cands, priced=priced, call=win, runner=runner, gap=gap, ranked=ranked,
                ask_a=ask_shortfall(P, allocated(P, ex)), ask_b=ask_traded(P, allocated(P, ex)))

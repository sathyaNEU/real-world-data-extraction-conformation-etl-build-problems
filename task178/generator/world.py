"""task178 world: the clean truth before any file is written. The tamarquian peso's hourly path from January 2024 to
December 2026, the reporting dealers' customer flows, the Banco Central de Tamarquia's spot operations against each
hour's pressure, and the domestic bank's own records (its 2026 platform executions and its forward book).

Units inside this module: rates are pesos per dollar, returns are log changes in per cent, flows are US dollars in
thousands (customers' net purchases of dollars, positive when customers bought), the Bank's operations in millions
(positive when the Bank sold dollars)."""
from __future__ import annotations

import datetime as dt
import functools
import math

import numpy as np

import common as C

# ------------------------------------------------------------------------------------------------ parameters
FREE_DAILY = 10.93 / math.sqrt(C.ANN)    # per cent: the free-float daily volatility the world is drawn at
ON_SHARE = 0.12                           # share of the free daily variance that arrives overnight
FLOW_SHARE = 0.50                         # share of the in-session variance carried by customer flow
LAMBDA = 0.0055                           # per cent per USD 1 million of net flow the dealers absorb
TAU = 0.1437                              # the hour's pressure, per cent, above which the Bank operates
SMAX = 0.85                               # the share of pressure beyond TAU the Bank takes off the market at the limit
HOUR_SHAPE = np.array([1.55, 1.12, 0.92, 0.82, 0.80, 0.90, 1.08, 1.38])
OPEN_RATE = 3872.40

DEALERS = (  # code, name, share of customer flow (variance weight)
    ("BCO", "Banco Cordillera", 0.135),
    ("BSL", "Banco del Salitral", 0.150),
    ("BHV", "Banco Hacendario del Valle", 0.118),
    ("BRF", "Banco Rural de Fomento", 0.064),
    ("CLM", "Corporación Financiera Los Molles", 0.097),
    ("BIO", "Banco Interoceánico", 0.103),
    ("BQL", "Banco del Quindal", 0.071),
    ("BAM", "Banco Alameda", 0.082),
    ("FTV", "Financiera Tres Valles", 0.046),
    ("CPS", "Caja Previsora del Sur", 0.039),
    ("BVL", "Banco Valle Lindo", 0.052),
    ("CCO", "Cambios Costanera", 0.043),
)


@functools.lru_cache(maxsize=None)
def days():
    return tuple(C.trading_days())


def _t(rng, df, size):
    return rng.standard_t(df, size) / math.sqrt(df / (df - 2.0))


@functools.lru_cache(maxsize=None)
def day_scale():
    """a slowly wandering volatility level, one value per session, root mean square one"""
    rng = C.stream("day_scale")
    n = len(days())
    h = np.zeros(n)
    for i in range(1, n):
        h[i] = 0.982 * h[i - 1] + rng.normal(0, 0.095)
    s = np.exp(h)
    return s / math.sqrt(np.mean(s ** 2))


def hour_sd():
    """per-hour free in-session volatility, per cent, before the day's scale"""
    u = HOUR_SHAPE / math.sqrt(np.mean(HOUR_SHAPE ** 2))
    return FREE_DAILY * math.sqrt(1 - ON_SHARE) / math.sqrt(len(C.HOURS)) * u


@functools.lru_cache(maxsize=None)
def dealer_flows():
    """true customer net purchases by dealer and hour, USD thousands, array (dealer, day, hour). Financiera
    Tres Valles' customers are inside Banco del Salitral's figures from the merger date."""
    rng = C.stream("flows")
    n, H = len(days()), len(C.HOURS)
    sc = day_scale()
    sd_total = math.sqrt(FLOW_SHARE) * hour_sd() / LAMBDA * 1000.0     # USD thousands per hour
    shares = np.array([d[2] for d in DEALERS])
    shares = shares / shares.sum()
    out = np.zeros((len(DEALERS), n, H))
    for k in range(len(DEALERS)):
        out[k] = sc[:, None] * sd_total[None, :] * math.sqrt(shares[k]) * _t(rng, 4.5, (n, H))
    out = np.round(out)
    fam, bsa = [d[0] for d in DEALERS].index("FTV"), [d[0] for d in DEALERS].index("BSL")
    merged = np.array([d >= C.MERGER_DATE for d in days()])
    out[bsa, merged] += out[fam, merged]
    out[fam, merged] = 0.0
    return out


@functools.lru_cache(maxsize=None)
def fam_legacy():
    """what Financiera Tres Valles' own reporting system kept filing for its former customers in July 2025, after they
    had become Banco del Salitral's customers (the same trades, already inside Banco del Salitral's reports)"""
    rng = C.stream("flows")
    n, H = len(days()), len(C.HOURS)
    sc = day_scale()
    sd_total = math.sqrt(FLOW_SHARE) * hour_sd() / LAMBDA * 1000.0
    shares = np.array([d[2] for d in DEALERS])
    shares = shares / shares.sum()
    fam = [d[0] for d in DEALERS].index("FTV")
    raw = None
    for k in range(len(DEALERS)):
        x = sc[:, None] * sd_total[None, :] * math.sqrt(shares[k]) * _t(rng, 4.5, (n, H))
        if k == fam:
            raw = np.round(x)
    jul = np.array([d.year == 2025 and d.month == 7 for d in days()])
    return raw, jul


def total_flow_m():
    """the market's customer flow, USD millions, (day, hour)"""
    return dealer_flows().sum(axis=0) / 1000.0


@functools.lru_cache(maxsize=None)
def news():
    rng = C.stream("news")
    n, H = len(days()), len(C.HOURS)
    sc = day_scale()
    e = sc[:, None] * (math.sqrt(1 - FLOW_SHARE) * hour_sd())[None, :] * _t(rng, 5.0, (n, H))
    on = sc * FREE_DAILY * math.sqrt(ON_SHARE) * _t(rng, 4.0, n)
    return e, on


@functools.lru_cache(maxsize=None)
def bank():
    """the Bank's operations: per hour the pressure it saw and the tickets it dealt. Returns (pressure, I in USD
    millions by hour, tickets) where each ticket is (day index, hour index, minute, second, amount m, dealer code,
    cancelled-and-reentered flag)."""
    rng = C.stream("bank")
    F = total_flow_m()
    e, _ = news()
    P = LAMBDA * F + e
    n, H = P.shape
    I = np.zeros_like(P)
    tickets = []
    codes = [d[0] for d in DEALERS]
    for i in range(n):
        dday = days()[i]
        live = [c for c in codes if not (c == "FTV" and dday >= C.MERGER_DATE)]
        for h in range(H):
            p = P[i, h]
            if abs(p) > TAU:
                s = SMAX * (1 - TAU / abs(p)) * rng.uniform(0.92, 1.08)
            elif abs(p) > 0.6 * TAU and rng.random() < 0.06:
                s = rng.uniform(0.05, 0.15)
            else:
                continue
            target = s * p / LAMBDA                   # USD millions, positive: the Bank sells dollars
            if abs(target) < 2.0:
                continue
            left, legs = abs(target), []
            while left > 0.25:
                a = min(left, rng.uniform(4.0, 22.0))
                a = max(0.5, round(a * 2) / 2)
                if a > left + 0.25:
                    a = max(0.5, round(left * 2) / 2)
                legs.append(a)
                left -= a
            sign = 1.0 if target > 0 else -1.0
            mins = np.sort(rng.integers(3, 58, len(legs)))
            for a, m in zip(legs, mins):
                tickets.append((i, h, int(m), int(rng.integers(0, 60)), sign * a,
                                live[int(rng.integers(0, len(live)))], bool(rng.random() < 0.012)))
                I[i, h] += sign * a
    return P, I, tickets


@functools.lru_cache(maxsize=None)
def path():
    """observed hourly returns, overnight returns and the mid path (unrounded), (day, snapshot 0..8)"""
    P, I, _ = bank()
    _, on = news()
    R = P - LAMBDA * I
    n, H = R.shape
    mids = np.zeros((n, H + 1))
    last = OPEN_RATE / math.exp(on[0] / 100.0)
    for i in range(n):
        mids[i, 0] = last * math.exp(on[i] / 100.0)
        for h in range(H):
            mids[i, h + 1] = mids[i, h] * math.exp(R[i, h] / 100.0)
        last = mids[i, H]
    return R, on, mids


def free_truth():
    """the generator's own free-float volatility of daily closing changes over the record, per cent annualised"""
    P, _, _ = bank()
    _, on = news()
    d = on + P.sum(axis=1)
    return math.sqrt(C.ANN * np.mean(d ** 2))


def record_truth():
    R, on, _ = path()
    d = on + R.sum(axis=1)
    return math.sqrt(C.ANN * np.mean(d ** 2))


OUTAGES = ((dt.date(2024, 9, 18), 11), (dt.date(2025, 3, 11), 13), (dt.date(2026, 5, 27), 10))  # snapshot hour lost


# ------------------------------------------------------------------------------------------------ the desk's 2026 executions
DESK_STREAM = "desk_orders/15"
TRADERS = ("YCACERES", "EHURTADO", "LMOLANO", "GARIAS")
# the platform's 2026 liquidity: a market maker stepped back in the second quarter, a new one joined in the third and
# the year-end thinned the book
QUARTER_SPREAD = {1: 1.00, 2: 1.14, 3: 0.90, 4: 1.24}
QUARTER_DEPTH = {1: (500, 1000, 1000, 1500, 2000, 2500, 3000), 2: (500, 500, 1000, 1500, 2000),
                 3: (1000, 1500, 2000, 2500, 3000, 3000), 4: (500, 500, 1000, 1000, 1500, 2000)}
QUARTER_STEP = {1: (0.35, 0.95), 2: (0.45, 1.15), 3: (0.30, 0.80), 4: (0.50, 1.30)}


@functools.lru_cache(maxsize=None)
def desk_orders():
    """Banco Cordillera's 2026 orders on the platform, each with its fills. An order is one arrival: a trader, a side
    and one millisecond stamp; a marketable order larger than the touch takes several resting quotes and each quote
    it takes is its own execution. Returns a list of dicts."""
    rng = C.stream(DESK_STREAM)
    R, on, mids = path()
    di = [i for i, d in enumerate(days()) if d.year == C.CONF_YEAR]
    orders = []
    for k in range(1420):
        i = int(di[int(rng.integers(0, len(di)))])
        h = int(rng.integers(0, len(C.HOURS)))
        frac = rng.random()
        mid = mids[i, h] * math.exp(R[i, h] / 100.0 * frac + rng.normal(0, 0.02) / 100.0)
        q = C.quarter(days()[i])
        base_spread = ((2.6 if h == 0 else 1.9 if h in (1, 7) else 1.5) * (0.55 + 0.55 * day_scale()[i])
                       * QUARTER_SPREAD[q] * (0.85 + 0.3 * rng.random()))
        bid = math.floor((mid - base_spread / 2) * 100) / 100
        ask = math.ceil((mid + base_spread / 2) * 100) / 100
        size = float(np.exp(rng.normal(math.log(1400.0), 1.05)))               # USD thousands
        size = max(100.0, round(size / 50.0) * 50.0)
        side = "BUY" if rng.random() < 0.52 else "SELL"
        sgn = 1 if side == "BUY" else -1
        touch = (ask if sgn > 0 else bid)
        fills, left, lvl = [], size, 0
        lo_step, hi_step = QUARTER_STEP[q]
        while left > 0:
            depth = float(rng.choice(QUARTER_DEPTH[q]))
            qty = min(left, depth)
            px = touch + sgn * lvl * round(rng.uniform(lo_step, hi_step), 2)
            fills.append([round(px, 2), qty])
            left -= qty
            lvl += 1
        t = dt.datetime.combine(days()[i], dt.time(C.HOURS[h], 0)) + dt.timedelta(seconds=float(frac) * 3599.0)
        t = t.replace(microsecond=int(rng.integers(0, 1000)) * 1000)
        orders.append(dict(day=days()[i], local=t, trader=TRADERS[int(rng.integers(0, len(TRADERS)))], side=side,
                           bid=round(bid, 2), ask=round(ask, 2), size=size, fills=fills))
    for o in list(orders[:: 61]):
        twin_trader = [t for t in TRADERS if t != o["trader"]][int(rng.integers(0, len(TRADERS) - 1))]
        size = max(100.0, round(float(np.exp(rng.normal(math.log(900.0), 0.8))) / 50.0) * 50.0)
        side = o["side"] if rng.random() < 0.7 else ("SELL" if o["side"] == "BUY" else "BUY")
        sgn = 1 if side == "BUY" else -1
        t = o["local"].replace(microsecond=int(rng.integers(0, 1000)) * 1000)
        while t == o["local"]:
            t = o["local"].replace(microsecond=int(rng.integers(0, 1000)) * 1000)
        fills, left, lvl = [], size, 0
        touch = o["ask"] if sgn > 0 else o["bid"]
        while left > 0:
            q = min(left, float(rng.choice([500, 1000, 1500, 2000])))
            fills.append([round(touch + sgn * lvl * round(rng.uniform(0.35, 0.95), 2), 2), q])
            left -= q
            lvl += 1
        orders.append(dict(day=o["day"], local=t, trader=twin_trader, side=side, bid=o["bid"], ask=o["ask"], size=size,
                           fills=fills))
    orders.sort(key=lambda o: o["local"])
    return orders


# ------------------------------------------------------------------------------------------------ the forward book
FWD_STREAM = "forwards/7"
SECTORS_EXP = ("coffee", "cut flowers", "copper concentrate", "fresh fruit", "shrimp", "textiles", "cocoa", "gold")
SECTORS_IMP = ("pharmaceuticals", "machinery", "fuel distribution", "vehicles", "consumer electronics", "fertiliser",
               "grain milling", "medical devices")


@functools.lru_cache(maxsize=None)
def clients():
    rng = C.stream("clients")
    out = []
    used = set()
    for seg, n, sectors in (("EXPORTADOR", 74, SECTORS_EXP), ("IMPORTADOR", 79, SECTORS_IMP)):
        for _ in range(n):
            while True:
                no = int(rng.integers(100000, 999999))
                if no not in used:
                    used.add(no)
                    break
            out.append(dict(no=no, segment=seg, sector=sectors[int(rng.integers(0, len(sectors)))]))
    for no in (100217, 100218):
        out.append(dict(no=no, segment="TESORERIA", sector="internal"))
    return out


@functools.lru_cache(maxsize=None)
def forward_book():
    """every dollar or euro forward traded 2025-01-02 to 2026-12-29: outrights, window forwards and the drawdowns
    booked against windows. A drawdown is booked by the deal system as an outright at the window's rate; the window
    keeps its original notional."""
    rng = C.stream(FWD_STREAM)
    cl = clients()
    ext = [c for c in cl if c["segment"] != "TESORERIA"]
    start, end = dt.date(2025, 1, 2), dt.date(2026, 12, 29)
    span = (end - start).days
    deals = []
    seq = [41020]

    def nxt():
        seq[0] += int(rng.integers(1, 9))
        return seq[0]

    def biz(d):
        while d.weekday() >= 5:
            d += dt.timedelta(days=1)
        return d

    def rate_for(td, mat):
        base = 3870.0 + 45.0 * math.sin((td - start).days / 140.0)
        return round(base * (1 + 0.051 * (mat - td).days / 365.0) + rng.normal(0, 6.0), 2)

    for c in ext:
        sgn_dir = "VENDE" if c["segment"] == "EXPORTADOR" else "COMPRA"     # the client sells or buys dollars
        n_out = int(rng.integers(1, 7))
        for _ in range(n_out):
            td = biz(start + dt.timedelta(days=int(rng.integers(0, span))))
            mat = biz(td + dt.timedelta(days=int(rng.integers(30, 540))))
            amt = round(float(np.exp(rng.normal(math.log(900000.0), 0.9))) / 5000.0) * 5000.0
            pair = "EUR/TQP" if rng.random() < 0.05 else "USD/TQP"
            rate = rate_for(td, mat)
            if pair == "EUR/TQP":
                rate = round(rate * (1.0815 + 0.012 * math.sin((td - start).days / 90.0)), 2)
            deals.append(dict(no=None, client=c["no"], td=td, mat=mat, product="OUTRIGHT", window_open=None,
                              side=sgn_dir, amount=amt, rate=rate, pair=pair, cancelled=False, parent=None))
        if rng.random() < 0.46:
            for _ in range(int(rng.integers(1, 3))):
                td = biz(start + dt.timedelta(days=int(rng.integers(60, span - 15))))
                wo = biz(td + dt.timedelta(days=int(rng.integers(5, 90))))
                mat = biz(wo + dt.timedelta(days=int(rng.integers(60, 430))))
                amt = round(float(np.exp(rng.normal(math.log(2400000.0), 0.6))) / 50000.0) * 50000.0
                w = dict(no=None, client=c["no"], td=td, mat=mat, product="WINDOW", window_open=wo, side=sgn_dir,
                         amount=amt, rate=rate_for(td, mat), pair="USD/TQP", cancelled=False, parent=None)
                deals.append(w)
                full = rng.random() < 0.22
                k = int(rng.integers(1, 5))
                left = amt
                cuts = sorted(rng.uniform(0, 1, k))
                for j in range(k):
                    if j == k - 1 and full:
                        a = left
                    else:
                        a = round(amt * rng.uniform(0.08, 0.30) / 5000.0) * 5000.0
                    if a <= 0 or a > left:
                        break
                    left -= a
                    dd = biz(wo + dt.timedelta(days=int(cuts[j] * max(1, (mat - wo).days - 3))))
                    booked = max(td, dd - dt.timedelta(days=int(rng.integers(1, 4))))
                    deals.append(dict(no=None, client=c["no"], td=biz(booked), mat=dd, product="OUTRIGHT",
                                      window_open=None, side=sgn_dir, amount=a, rate=w["rate"], pair="USD/TQP",
                                      cancelled=False, parent=w))
    for no in (100217, 100218):
        for _ in range(9):
            td = biz(start + dt.timedelta(days=int(rng.integers(0, span))))
            mat = biz(td + dt.timedelta(days=int(rng.integers(30, 400))))
            deals.append(dict(no=None, client=no, td=td, mat=mat, product="OUTRIGHT", window_open=None,
                              side="COMPRA" if rng.random() < 0.5 else "VENDE",
                              amount=round(float(rng.uniform(2e6, 9e6)) / 100000.0) * 100000.0,
                              rate=rate_for(td, mat), pair="USD/TQP", cancelled=False, parent=None))
    # a few deals cancelled the day they were booked
    for d in deals:
        if d["parent"] is None and d["product"] == "OUTRIGHT" and rng.random() < 0.015:
            d["cancelled"] = True
    deals.sort(key=lambda d: (d["td"], d["client"], d["mat"]))
    for d in deals:
        d["no"] = nxt()
    return deals


@functools.lru_cache(maxsize=None)
def clients_by_no():
    return {c["no"]: c for c in clients()}

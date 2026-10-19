"""Daily prices for every security over its listed life, built in economic terms (one unit of the company as it
stood before any split) and then expressed per share as traded: the market and sector factors, each stock's own
moves and its earnings reactions, cash dividends (with the 2020 suspensions), forward splits when a price runs
high, reverse splits in distress, spin-offs, cash and stock acquisitions, a terminated deal, delisting for cause.
Then the day's open, high, low, close, closing quote, volume and shares outstanding."""
import datetime as dt
import math

import numpy as np

import universe as U
import world as W

SQ = math.sqrt(252.0)
# market episodes: start, end, total log move, volatility multiplier
EPISODES = [
    ("2018-10-03", "2018-12-24", -0.27, 1.8), ("2018-12-26", "2019-04-30", 0.20, 1.3),
    ("2020-02-21", "2020-03-18", -0.50, 3.8), ("2020-03-19", "2020-06-08", 0.42, 2.7),
    ("2020-11-04", "2021-03-12", 0.36, 1.6), ("2022-01-03", "2022-06-16", -0.30, 1.8),
    ("2022-06-17", "2022-08-16", 0.20, 1.4), ("2022-08-17", "2022-09-30", -0.17, 1.6),
    ("2023-03-08", "2023-03-17", -0.09, 2.4), ("2023-08-01", "2023-10-27", -0.19, 1.3),
    ("2023-10-30", "2023-12-29", 0.20, 1.4), ("2025-02-19", "2025-04-08", -0.24, 2.5),
    ("2025-04-09", "2025-07-31", 0.21, 1.7),
]
SECTOR_EPISODES = {
    0: [("2020-02-21", "2020-04-21", -0.35, 2.0), ("2021-01-04", "2022-06-08", 0.45, 1.2)],
    6: [("2023-03-08", "2023-05-04", -0.24, 2.2)],
    5: [("2021-02-09", "2022-06-13", -0.28, 1.3)],
    7: [("2022-01-03", "2022-10-14", -0.14, 1.2)],
    10: [("2022-01-03", "2022-10-14", -0.12, 1.2)],
}
TICK = 0.01
# each calendar year's log total return for the market factor; the episodes shape the year, these set its end
YEAR_LOG = {2018: -0.115, 2019: 0.225, 2020: 0.18, 2021: 0.135, 2022: -0.225, 2023: 0.15, 2024: 0.1, 2025: 0.095,
            2026: 0.055}


def _d(s):
    return U.day_on_or_after(dt.date.fromisoformat(s))


def factors():
    rng = U.rng_for(3)
    T = U.T
    lv = np.zeros(T)
    e = rng.normal(0, 1, T)
    for t in range(1, T):
        lv[t] = 0.98 * lv[t - 1] + 0.05 * e[t]
    drift = np.full(T, 0.052 / 252)
    vm = np.exp(lv - 0.05 ** 2 / (2 * (1 - 0.98 ** 2)))
    for a, b, move, mult in EPISODES:
        ia, ib = _d(a), _d(b)
        drift[ia:ib + 1] += move / (ib - ia + 1)
        vm[ia:ib + 1] *= mult
    m = drift + 0.14 / SQ * vm * rng.standard_t(6, T) / math.sqrt(1.5)
    years = np.array([d.year for d in U.DAYS])
    for y, target in YEAR_LOG.items():
        mk = years == y
        m[mk] += (target - m[mk].sum()) / mk.sum()
    sec = np.zeros((len(W.SECTORS), T))
    for k in range(len(W.SECTORS)):
        sd = np.full(T, 0.0)
        smult = np.ones(T)
        for a, b, move, mult in SECTOR_EPISODES.get(k, []):
            ia, ib = _d(a), _d(b)
            sd[ia:ib + 1] += move / (ib - ia + 1)
            smult[ia:ib + 1] *= mult
        sec[k] = sd + 0.09 / SQ * vm ** 0.5 * smult * rng.normal(0, 1, T)
    # sector factors are moves relative to the market: their sector-weighted mean is taken out each day
    wts = np.array(W.SECTOR_WEIGHT)[:, None]
    sec = sec - (wts * sec).sum(axis=0, keepdims=True) / wts.sum()
    return m, sec, vm


def _round_px(p):
    if p >= 1.0:
        return round(p + 1e-9, 2)
    return round(p + 1e-12, 4)


class Path:
    """One security's life in arrays over its listed days [i0, i1]."""

    def __init__(self, s):
        self.s = s
        self.i0 = s["first"]
        self.i1 = s["last"] if s["last"] is not None else U.T - 1
        n = self.i1 - self.i0 + 1
        self.n = n
        self.P = np.zeros(n)          # economic close (ex any distribution that day)
        self.S = np.ones(n)           # cumulative split factor: raw = economic / S
        self.D = np.zeros(n)          # cash dividend per raw share, on its ex-day
        self.V = np.zeros(n)          # spin-off value per raw share, on its ex-day
        self.F = np.ones(n)           # split factor on its ex-day
        self.x = np.zeros(n)          # the day's log move before distributions
        self.jump = np.zeros(n)
        self.special = np.zeros(n, dtype=bool)
        self.divs = []
        self.splits = []
        self.reaction = np.zeros(n, dtype=bool)

    def j(self, i):
        return i - self.i0


def simulate(secs, sched):
    rng = U.rng_for(4)
    m, sec, vm = factors()
    paths = {}
    order = [s for s in secs if s["kind"] == "spin"] + \
            [s for s in secs if s["kind"] != "spin" and s.get("deal", {}).get("kind") != "stock"] + \
            [s for s in secs if s.get("deal", {}).get("kind") == "stock"]
    for s in order:
        paths[s["k"]] = _one(s, sched[s["k"]], m, sec, vm, paths, secs, rng)
    return paths, (m, sec, vm)


def _one(s, sc, m, sec, vm, paths, secs, rng):
    p = Path(s)
    n, i0 = p.n, p.i0
    sd = s["ivol"] / SQ
    gam = float(rng.uniform(0.6, 1.0))
    mu = (0.55 * s["growth"] - 0.01 - s["ivol"] ** 2 / 2) / 252
    idio = sd * rng.standard_t(4, n) / math.sqrt(2.0)
    days = np.arange(i0, i0 + n)
    p.x[:] = s["beta"] * m[days] + gam * sec[s["sector"]][days] + idio + mu
    p.sd = np.sqrt((s["beta"] * 0.14 / SQ * vm[days]) ** 2 + (0.09 / SQ) ** 2 + sd ** 2)
    for r in sc["periods"]:
        if r["react"] is not None and i0 < r["react"] <= p.i1:
            jj = p.j(r["react"])
            p.jump[jj] = 0.021 * r["sue"] + rng.normal(0, 0.042)
            p.reaction[jj] = True
    p.x += p.jump

    # dividend plan (raw amounts decided on the declaration day from the price then)
    divplan = []
    if s["payer"]:
        m0 = int(rng.integers(1, 4))
        d0 = int(rng.integers(4, 24))
        yld = float(np.clip(rng.normal(0.028, 0.011), 0.008, 0.06)) * (1.4 if s["sector"] in (9, 10) else 1.0)
        covid = s["sector"] in (0, 2, 3) and rng.random() < 0.4
        for y in range(2018, 2027):
            for qq in range(4):
                mm = m0 + 3 * qq
                ex = U.day_on_or_after(dt.date(y, mm, d0))
                if ex <= i0 + 25 or ex > p.i1 or ex >= U.T:
                    continue
                if covid and U.DAYS[ex] >= dt.date(2020, 4, 1) and U.DAYS[ex] < dt.date(2021, 5, 1):
                    divplan.append((ex, "suspended"))
                    continue
                divplan.append((ex, "pay"))
        p.yld = yld
        p.covid = covid
    specials = []
    if rng.random() < 0.035:
        specials.append(int(rng.integers(i0 + 60, p.i1 - 5)) if p.i1 - 5 > i0 + 60 else None)

    deal = s.get("deal")
    dist = s.get("distress")
    spin = [e for e in s["events"] if e[0] == "spinoff"]
    spin_day = {e[1]: e[2] for e in spin}

    # walk the days
    P = p.P
    S = p.S
    if s["kind"] == "spin":
        P[0] = s["price0"]
    else:
        P[0] = s["price0"] if s["kind"] == "initial" else s["price0"] * float(np.exp(rng.normal(0.12, 0.2)))
    s["ipo_offer"] = float(max(8.0, round(s["price0"]))) if s["kind"] == "ipo" else None
    cur_div = None
    div_count = 0
    last_split = -999
    pending_split = None
    deal_K = None
    segs = _bridges(s, p, rng)
    for jj in range(1, n):
        i = i0 + jj
        S[jj] = S[jj - 1]
        # forward splits: checked at each month's last trading day, effective some weeks later
        if pending_split and pending_split[0] == i:
            p.F[jj] = pending_split[1]
            S[jj] *= pending_split[1]
            p.splits.append(dict(ex=i, F=pending_split[1], announce=pending_split[2]))
            last_split = i
            pending_split = None
            if cur_div is not None:
                cur_div = round(cur_div / p.F[jj], 3 if cur_div / p.F[jj] < 0.2 else 2)
        if dist and dist.get("rs") == i:
            raw = P[jj - 1] / S[jj - 1]
            F = 0.05 if raw < 0.4 else 0.1
            p.F[jj] = F
            S[jj] *= F
            p.splits.append(dict(ex=i, F=F, announce=i - int(rng.integers(12, 25))))
        # distributions
        dval = 0.0
        if (i, "pay") in divplan and p.F[jj] == 1.0 and not (dist and i >= dist["start"]) and \
                not (deal and deal.get("close") and i >= deal["close"] - 1):
            decl_px = P[max(0, jj - 20)] / S[max(0, jj - 20)]
            if cur_div is None:
                cur_div = max(0.01, round(p.yld / 4 * decl_px, 2 if decl_px > 8 else 3))
            elif div_count % 4 == 0:
                cur_div = round(cur_div * float(rng.uniform(1.03, 1.1)), 3 if cur_div < 0.2 else 2)
            amount = cur_div
            div_count += 1
            p.D[jj] = amount
            p.divs.append(dict(ex=i, amount=amount, kind="CASH"))
            dval += amount
        if specials and specials[0] == i:
            amt = round(float(rng.uniform(0.5, 2.5)), 2)
            p.D[jj] += amt
            p.divs.append(dict(ex=i, amount=amt, kind="SPECIAL"))
            dval += amt
        if i in spin_day:
            child = paths[spin_day[i]]
            cc = child.P[0]
            ratio = round(0.18 * (P[jj - 1] / S[jj - 1]) / cc, 4)
            p.V[jj] = ratio * cc
            p.spin_ratio = ratio
            child.parent_ratio = ratio
        # the economic close
        braw = _bridge_raw(p, segs, i, jj) if segs else None
        if braw is not None:
            P[jj] = braw * S[jj]
            p.x[jj] = math.log((P[jj] + (dval + p.V[jj]) * S[jj]) / P[jj - 1])
        elif deal and deal["announce"] <= i:
            P[jj], deal_K = _deal_price(s, p, jj, i, deal, paths, rng, deal_K)
            p.x[jj] = math.log((P[jj] + (dval + p.V[jj]) * S[jj]) / P[jj - 1])
        else:
            if P[jj - 1] / S[jj - 1] < 2.5 and not dist:
                # a listed company this cheap without a plan to reverse split or delist trades sideways
                p.x[jj] = 0.5 * p.x[jj] + 0.004
            P[jj] = P[jj - 1] * math.exp(p.x[jj]) - (dval + p.V[jj]) * S[jj]
            if P[jj] <= 0:
                P[jj] = P[jj - 1] * 0.5
        # month end: a high price brings a split announcement
        if pending_split is None and i - last_split > 500 and not deal and not dist and i + 40 < p.i1 and \
                len(p.splits) < 2 and (i + 1 < U.T and U.DAYS[i + 1].month != U.DAYS[i].month):
            raw = P[jj] / S[jj]
            if raw > 150 and rng.random() < 0.08:
                F = 3.0 if raw > 320 else 2.0
                pending_split = (i + int(rng.integers(18, 32)), F, i)
            elif raw > 90 and rng.random() < 0.012:
                pending_split = (i + int(rng.integers(18, 32)), 1.5, i)
    p.deal_K = deal_K
    p.divplan = divplan
    return p


def _bridges(s, p, rng):
    """Distress: segments of the raw price drawn as Brownian bridges to planned levels, so the stock falls below a
    dollar before its reverse split and ends near its last price before delisting. Returns [(first day, last day,
    raw target, pinned noise)]."""
    d = s.get("distress")
    if not d:
        return []
    sd = float(p.sd.mean()) * 1.35
    segs = []
    rs, end = d.get("rs"), d.get("end")
    if rs:
        segs.append((d["start"], rs - 1, float(rng.uniform(0.55, 0.9))))
        if end:
            segs.append((rs, end, d["target"] * 10 * float(rng.uniform(0.3, 0.6))))
    else:
        segs.append((d["start"], end, d["target"]))
    out = []
    for a, b, target in segs:
        n = b - a + 1
        if n < 5 or a <= p.i0:
            continue
        w = np.cumsum(rng.normal(0, sd, n))
        w = w - np.arange(1, n + 1) / n * w[-1]
        out.append((a, b, target, w))
    return out


def _bridge_raw(p, segs, i, jj):
    for a, b, target, w in segs:
        if a <= i <= b:
            if i == a:
                p._base = (p.P[jj - 1] / p.S[jj - 1]) / p.F[jj]
            k = i - a + 1
            n = b - a + 1
            l0 = math.log(p._base)
            return math.exp(l0 + (math.log(target) - l0) * k / n + w[k - 1])
    return None


def _deal_price(s, p, jj, i, deal, paths, rng, K):
    """Economic close for a target once its deal is announced."""
    S = p.S[jj]
    prev_raw = p.P[jj - 1] / p.S[jj - 1]
    a = deal["announce"]
    close = deal.get("close")
    L = (close - a) if close else 120
    if deal["kind"] in ("cash", "private", "terminated") or deal["kind"] == "pending":
        if K is None:
            K = round(prev_raw * (1 + deal["premium"]), 2)
        if deal["kind"] == "terminated":
            term = deal["terminate"]
            if i < term:
                spread = deal["spread0"] + 0.06 * (i - a) / max(1, term - a) + rng.normal(0, 0.004)
                return K * (1 - spread) * S, K
            if i == term:
                pre = p.P[p.j(a) - 1] / p.S[p.j(a) - 1]
                return pre * float(rng.uniform(0.9, 1.0)) * S, K
            return p.P[jj - 1] * math.exp(p.x[jj]), K
        frac = min(1.0, (i - a) / max(1, L - 1))
        spread = deal["spread0"] * (1 - frac) + 0.0025 + rng.normal(0, 0.0018)
        return K * (1 - max(spread, 0.0005)) * S, K
    acq = paths[deal["acquirer"]]
    if K is None:
        acq_prev = acq.P[acq.j(i - 1)] / acq.S[acq.j(i - 1)]
        K = round(prev_raw * (1 + deal["premium"]) / acq_prev, 4)
    acq_raw = acq.P[acq.j(i)] / acq.S[acq.j(i)]
    frac = min(1.0, (i - a) / max(1, L - 1))
    spread = deal["spread0"] * (1 - frac) + 0.003 + rng.normal(0, 0.0022)
    return K * acq_raw * (1 - max(spread, 0.0005)) * S, K

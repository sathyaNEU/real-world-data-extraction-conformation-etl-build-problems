"""task306 architecture 4: Wealdmoor Investment Management's systematic equity desk.

The world: a UK equity universe traded on the London market (large, mid and small caps), its daily market data,
three backtested candidate strategies whose trades the research team logged at each rebalance, and the desk's four
live strategies' orders and fills, whose cost follows a square-root impact law in each order's share of the stock's
daily traded value. Everything is drawn from fixed seeds; nothing reads the clock."""
import datetime as dt
import math

import numpy as np

SEED = 30604
AUM = 400_000_000.0                 # the new capital, GBP
K_IMPACT = 0.85                     # impact = K * daily vol * sqrt(participation)
TIERS = {
    # n, price pence (lo, hi), ADV GBP (median, log-sd), daily vol bps (centre), half-spread bps (lo, hi)
    "L": dict(n=100, px=(350, 4200), adv=(120e6, 0.50), vol=130.0, hs=(2.9, 3.1)),
    "M": dict(n=260, px=(180, 2400), adv=(22e6, 0.45), vol=175.0, hs=(8.3, 8.7)),
    "S": dict(n=320, px=(25, 620), adv=(8e6, 0.40), vol=235.0, hs=(24.5, 25.5)),
}
START, END = dt.date(2025, 1, 2), dt.date(2026, 11, 30)
BANK_HOLIDAYS = {dt.date(2025, 1, 1), dt.date(2025, 4, 18), dt.date(2025, 4, 21), dt.date(2025, 5, 5),
                 dt.date(2025, 5, 26), dt.date(2025, 8, 25), dt.date(2025, 12, 25), dt.date(2025, 12, 26),
                 dt.date(2026, 1, 1), dt.date(2026, 4, 3), dt.date(2026, 4, 6), dt.date(2026, 5, 4),
                 dt.date(2026, 5, 25), dt.date(2026, 8, 31)}
CANDIDATES = [
    # code, name, tier, holdings, rebalance ("M" monthly, "Q" quarterly), names swapped a rebalance, gross alpha
    ("SCM", "UK Smaller Companies Momentum", "S", 160, "M", 18, 0.0506),
    ("MCV", "UK Mid Cap Value", "M", 70, "Q", 10, 0.029),
    ("LCQ", "UK Large Cap Quality", "L", 45, "Q", 6, 0.018),
]
LIVE = [
    # code, name, tiers it trades, AUM GBP, orders a month (approximate)
    ("INC", "UK Equity Income", ("L",), 320e6, 120),
    ("MCG", "UK Mid Cap Growth", ("M",), 170e6, 150),
    ("SMC", "UK Smaller Companies", ("S",), 48e6, 170),
    ("DYN", "UK Dynamic", ("L", "M", "S"), 130e6, 160),
]
BROKERS = ["Orchard Lane Securities", "Calder Row Brokers", "Brightwater Execution", "Hythe Street Markets"]
GBP_BROKER = "Hythe Street Markets"            # reports fill prices in pounds; every other broker in pence
FAILOVER_DAYS = [dt.date(2026, 2, 11), dt.date(2026, 3, 19), dt.date(2026, 5, 13), dt.date(2026, 6, 24),
                 dt.date(2026, 1, 8), dt.date(2026, 2, 25), dt.date(2026, 3, 5), dt.date(2026, 4, 9),
                 dt.date(2026, 5, 27), dt.date(2026, 6, 10), dt.date(2026, 7, 29), dt.date(2026, 8, 20),
                 dt.date(2026, 9, 3), dt.date(2026, 10, 7), dt.date(2026, 10, 28), dt.date(2026, 11, 25),
                 dt.date(2026, 8, 6), dt.date(2026, 9, 16), dt.date(2026, 10, 21), dt.date(2026, 11, 18),
                 dt.date(2026, 1, 21), dt.date(2026, 4, 22), dt.date(2026, 7, 15), dt.date(2026, 11, 4)]
DYN_CODE_CHANGE = dt.date(2026, 7, 1)          # UK Dynamic moves to a new account code
DYN_OLD_REUSED = dt.date(2026, 8, 17)          # the old code is given to the transition account
RESENT_DAY = dt.date(2026, 6, 9)               # the OMS re-sent the day's fills after an outage
W_REUSE = DYN_OLD_REUSED


def rng(tag):
    h = 0
    for ch in "task306:" + tag:
        h = (h * 131 + ord(ch)) % (2 ** 32)
    return np.random.default_rng((SEED * 7919 + h) % (2 ** 32))


def trading_days():
    d, out = START, []
    while d <= END:
        if d.weekday() < 5 and d not in BANK_HOLIDAYS:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


SYL = ["ash", "brack", "cal", "der", "fen", "gar", "hal", "ingle", "kes", "lan", "mor", "nor", "oak", "pen", "quar",
       "rav", "sel", "thorn", "ul", "ver", "wey", "yar", "ald", "bel", "corr", "dun", "elm", "fal", "glen", "harl"]
END_ = ["ton", "ford", "ley", "wick", "mere", "stone", "field", "bridge", "worth", "dale", "holm", "gate", "wood",
        "brook", "more"]
KIND = {"L": ["Group", "Holdings", "plc", "International"], "M": ["Group", "Holdings", "plc", "Industries"],
        "S": ["Holdings", "plc", "Group", "Technologies", "Resources"]}
SECTORS = ["Industrials", "Financials", "Consumer Discretionary", "Consumer Staples", "Health Care", "Technology",
           "Energy", "Basic Materials", "Real Estate", "Utilities", "Telecommunications"]
SEDOL_CH = "BCDFGHJKLMNPQRSTVWXYZ0123456789"


def sedol_check(body):
    w = [1, 3, 1, 7, 3, 9]
    tot = 0
    for c, wt in zip(body, w):
        v = int(c) if c.isdigit() else ord(c) - 55
        tot += v * wt
    return str((10 - tot % 10) % 10)


def isin_for(sedol):
    body = "GB00" + sedol
    digits = "".join(str(int(c, 36)) for c in body)
    tot, dbl = 0, True
    for ch in reversed(digits):
        n = int(ch)
        if dbl:
            n *= 2
            if n > 9:
                n -= 9
        tot += n
        dbl = not dbl
    return body + str((10 - tot % 10) % 10)


def universe():
    r = rng("universe")
    out, names, sedols = [], set(), set()
    for tier, p in TIERS.items():
        for i in range(p["n"]):
            while True:
                nm = (SYL[int(r.integers(0, len(SYL)))] + END_[int(r.integers(0, len(END_)))]).capitalize()
                nm = nm + " " + KIND[tier][int(r.integers(0, len(KIND[tier])))]
                if nm not in names:
                    names.add(nm)
                    break
            while True:
                body = "B" + "".join(SEDOL_CH[int(r.integers(0, len(SEDOL_CH)))] for _ in range(5))
                sd = body + sedol_check(body)
                if sd not in sedols:
                    sedols.add(sd)
                    break
            px = float(math.exp(r.uniform(math.log(p["px"][0]), math.log(p["px"][1]))))
            adv = float(p["adv"][0] * math.exp(r.normal(0, p["adv"][1])))
            vol = float(p["vol"] * r.uniform(0.97, 1.03))
            hs = float(r.uniform(*p["hs"]))
            out.append(dict(sedol=sd, isin=isin_for(sd), name=nm, tier=tier, sector=SECTORS[int(r.integers(0, 11))],
                            px0=px, adv=adv, vol=vol, hs=hs))
    return out


def market(univ, days):
    """Daily closes (pence) and volumes (shares); a few small caps consolidate their shares ten to one."""
    r = rng("market")
    cons = {}
    smalls = [s for s in univ if s["tier"] == "S"]
    for k in r.permutation(len(smalls))[:8]:
        cons[smalls[int(k)]["sedol"]] = days[int(r.integers(60, len(days) - 60))]
    month_end = set()
    for i, d in enumerate(days):
        if i + 1 == len(days) or days[i + 1].month != d.month:
            month_end.add(d)
    rows = {}
    for s in univ:
        px = s["px0"]
        series = []
        for d in days:
            px *= math.exp(float(r.normal(-0.5 * (s["vol"] / 1e4) ** 2, s["vol"] / 1e4)))
            bump = 1.35 if d in month_end else 1.0
            value = s["adv"] * math.exp(float(r.normal(-0.5 * 0.22 ** 2, 0.22))) * bump
            shown_px = px
            if s["sedol"] in cons and d >= cons[s["sedol"]]:
                shown_px = px * 10.0
            shares = int(round(value / (shown_px / 100.0)))
            series.append((d, shown_px, shares, value))
        rows[s["sedol"]] = series
    return rows, cons, month_end


def adv20_and_vol(series, i):
    """Average daily traded value over the 20 sessions before day i, and the daily volatility over the 60."""
    lo = max(0, i - 20)
    vals = [series[j][3] for j in range(lo, i)]
    adv = sum(vals) / len(vals)
    lo = max(1, i - 60)
    rets = []
    for j in range(lo, i):
        a, b = series[j - 1][1], series[j][1]
        if abs(b / a - 10.0) < 0.5:          # a consolidation day: the price jumps tenfold, no return
            continue
        rets.append(math.log(b / a))
    vol = float(np.std(rets, ddof=1)) * 1e4 if len(rets) > 5 else None
    return adv, vol


def cost_bps(s, participation, vol_bps):
    return s["hs"] + K_IMPACT * vol_bps * math.sqrt(participation)


def candidates(univ, days, month_end):
    """Each candidate's rebalances from January 2025 to November 2026 as the backtest logged them: the weight it
    traded in each stock (buys and sells), at its own rebalance dates."""
    out = {}
    q_end = [d for d in sorted(month_end) if d.month in (3, 6, 9, 12)]
    for code, name, tier, hold, freq, swap, alpha in CANDIDATES:
        r = rng("cand-" + code)
        floor = {"S": 5e6, "M": 12e6, "L": 0.0}[tier]       # the strategy's liquidity screen
        pool = sorted([s for s in univ if s["tier"] == tier and s["adv"] >= floor], key=lambda s: s["sedol"])
        dates = sorted(month_end) if freq == "M" else q_end
        held = list(r.permutation(len(pool))[:hold])
        w = {int(k): 1.0 / hold for k in held}
        trades = []
        for d in dates:
            # drift: each holding's weight wanders between rebalances, and the rebalance trades it back
            drift = {k: v * math.exp(float(r.normal(0, 0.04 if freq == "M" else 0.06))) for k, v in w.items()}
            tot = sum(drift.values())
            drift = {k: v / tot for k, v in drift.items()}
            out_k = [int(x) for x in r.permutation(sorted(w))[:swap]]
            free = [k for k in range(len(pool)) if k not in w]
            in_k = [int(free[int(x)]) for x in r.permutation(len(free))[:swap]]
            new = {k: 1.0 / hold for k in w if k not in out_k}
            for k in in_k:
                new[k] = 1.0 / hold
            for k in sorted(set(drift) | set(new)):
                dw = new.get(k, 0.0) - drift.get(k, 0.0)
                if abs(dw) > 1e-6:
                    trades.append(dict(strategy=code, date=d, sedol=pool[k]["sedol"], isin=pool[k]["isin"],
                                       weight=round(dw, 6)))
            w = new
        out[code] = trades
    return out


def live_orders(univ, mkt, days, month_end):
    """The desk's live orders 2025 and 2026: each an order of one account in one stock on one day, its arrival mid,
    its size against the stock's 20-session traded value, and the shortfall it paid."""
    r = rng("orders")
    by_tier = {t: sorted([s for s in univ if s["tier"] == t], key=lambda s: s["sedol"]) for t in TIERS}
    idx = {d: i for i, d in enumerate(days)}
    orders = []
    oid = 4_100_000
    for code, name, tiers, aum, per_month in LIVE:
        for d in days:
            i = idx[d]
            if i < 25:
                continue
            n = int(r.poisson(1.5 * per_month / 21.0 * (3.0 if d in month_end else 1.0)))
            for _ in range(n):
                tier = tiers[int(r.integers(0, len(tiers)))]
                s = by_tier[tier][int(r.integers(0, len(by_tier[tier])))]
                adv, vol = adv20_and_vol(mkt[s["sedol"]], i)
                u = r.random()
                if u < 0.012:
                    part = float(math.exp(r.uniform(math.log(0.03), math.log(0.70))))   # block and event trades
                else:
                    part = float(math.exp(r.normal(math.log(0.005 if tier != "L" else 0.0025), 0.8)))
                part = min(part, 0.75)
                value = part * adv
                px_close_prev = mkt[s["sedol"]][i - 1][1]
                arrival = px_close_prev * math.exp(float(r.normal(0, 0.004)))
                qty = max(1, int(round(value / (arrival / 100.0))))
                value = qty * arrival / 100.0
                part = value / adv
                true_cost = cost_bps(s, part, vol)
                noise = float(r.normal(0, 0.12 * vol * (0.6 + math.sqrt(min(part, 0.6)))))
                side = 1 if r.random() < 0.5 else -1
                hh = int(r.integers(8, 15))
                mm = int(r.integers(0, 60))
                oid += int(r.integers(1, 40))
                orders.append(dict(order_id="WM%d" % oid, account=code, sedol=s["sedol"], tier=tier, date=d,
                                   hh=hh, mm=mm, side=side, qty=qty, arrival=arrival, adv=adv, vol=vol, part=part,
                                   cost=true_cost + noise, cancelled=False, filled=qty))
    # the Severnvale pension transition, run on the old UK Dynamic account code once it was free: block orders
    tr = rng("transition")
    for d in days:
        if not (W_REUSE <= d <= dt.date(2026, 11, 13)):
            continue
        i = idx[d]
        for _ in range(int(tr.poisson(9))):
            tier = ("L", "M", "S")[int(tr.integers(0, 3))]
            s = by_tier[tier][int(tr.integers(0, len(by_tier[tier])))]
            adv, vol = adv20_and_vol(mkt[s["sedol"]], i)
            part = float(math.exp(tr.uniform(math.log(0.02), math.log(0.30))))
            arrival = mkt[s["sedol"]][i - 1][1] * math.exp(float(tr.normal(0, 0.004)))
            qty = max(1, int(round(part * adv / (arrival / 100.0))))
            part = qty * arrival / 100.0 / adv
            oid += int(tr.integers(1, 40))
            orders.append(dict(order_id="WM%d" % oid, account="TRN", sedol=s["sedol"], tier=tier, date=d,
                               hh=int(tr.integers(8, 15)), mm=int(tr.integers(0, 60)),
                               side=1 if tr.random() < 0.5 else -1, qty=qty, arrival=arrival, adv=adv, vol=vol,
                               part=part, cost=cost_bps(s, part, vol) + float(tr.normal(0, 0.33 * vol)),
                               cancelled=False, filled=qty))
    # cancelled orders: a tenth of the orders stop part filled
    for o in orders:
        if r.random() < 0.06:
            o["cancelled"] = True
            o["filled"] = max(1, int(o["qty"] * r.uniform(0.25, 0.9)))
    # block orders: where UK Dynamic wants the same stock on the same side as another live book that day, the desk
    # places one order on its block account and allocates the fills after the trade
    bl = rng("blocks")
    by_tier_dyn = {t: by_tier[t] for t in TIERS}
    out = []
    for o in orders:
        if o["account"] in ("INC", "MCG", "SMC") and not o["cancelled"] and bl.random() < 0.16 \
                and o["date"] not in FAILOVER_DAYS:
            s = next(x for x in by_tier_dyn[o["tier"]] if x["sedol"] == o["sedol"])
            q2 = max(1, int(o["qty"] * bl.uniform(0.3, 0.9)))
            qty = o["qty"] + q2
            part = qty * o["arrival"] / 100.0 / o["adv"]
            oid += int(bl.integers(1, 40))
            out.append(dict(o, order_id="WM%d" % oid, account="BLOCK", qty=qty, filled=qty, part=part,
                            cost=cost_bps(s, part, o["vol"]) + float(bl.normal(0, 0.12 * o["vol"] *
                                                                                 (0.6 + math.sqrt(min(part, 0.6))))),
                            alloc=[(o["account"], o["qty"]), ("DYN", q2)]))
        else:
            out.append(o)
    out.sort(key=lambda o: (o["date"], o["hh"], o["mm"], o["order_id"]))
    return out

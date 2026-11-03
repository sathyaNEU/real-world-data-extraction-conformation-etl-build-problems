"""The Thornbury Managed Risk UK Equity Fund at each valuation point, and the accounting year replayed under a change.

`simulate()` runs the fund that existed: two sub-advised equity sleeves held security by security, the liquidity sleeve
in a money market fund, dealing through the liquidity sleeve, the share classes' charges and distributions, the
quarter-end rebalancing, and the overlay manager's futures under the drawdown rule in the prospectus.

`replay()` restates the fund for a change from the recorded series alone (sleeve returns, the money market fund, the
benchmark at the valuation point, the futures marks, dealing and distributions) with the same fund-level mechanics, so
the replay with no change reproduces the recorded B Accumulation price.
"""
import math

import numpy as np

import world as W
from world import D, DAYS, IDX

CLASSES = ["B Acc", "B Inc", "C Acc", "C Inc"]
AMC = {"B Acc": 0.0085, "B Inc": 0.0085, "C Acc": 0.0060, "C Inc": 0.0060}
INCOME = {"B Inc", "C Inc"}
XD = [(D(2025, 10, 1), D(2025, 11, 28)), (D(2026, 4, 1), D(2026, 5, 29)), (D(2026, 10, 1), D(2026, 11, 30))]
PENROSE_RESOLUTION = D(2026, 3, 23)
MULT = 10.0                 # pounds per index point
FUT_COMMISSION = 1.15       # pounds per contract per side
COMM_BP = {"V": 4.5, "G": 6.2}     # each sub-adviser's execution-only broker rate, basis points
NAV0 = 861_437_512.84
PRICE0 = {"B Acc": 171.82, "B Inc": 128.47, "C Acc": 176.30, "C Inc": 131.95}
SHARE0 = {"B Acc": 0.52, "B Inc": 0.09, "C Acc": 0.31, "C Inc": 0.08}
YEAR0 = IDX[W.YEAR_BASE]
YEAR1 = IDX[W.YEAR_END]


def last_of_quarter(d):
    i = IDX[d]
    return i + 1 < len(DAYS) and d.month in (3, 6, 9, 12) and DAYS[i + 1].month != d.month


def dealing(r):
    """net units dealt per class at each valuation point, as a fraction of the class's net assets"""
    out = {}
    for d in DAYS:
        row = {}
        for k in CLASSES:
            base = float(r.normal(-0.00011, 0.00052))
            if D(2026, 3, 23) <= d <= D(2026, 4, 30):
                base -= float(abs(r.normal(0.00080, 0.00040)))
            if D(2026, 7, 1) <= d <= D(2026, 8, 28):
                base += float(r.normal(0.00012, 0.00018))
            row[k] = base
        out[d] = row
    return out


def simulate(world):
    secs, value, growth = world["secs"], world["value"], world["growth"]
    prices, divs, ix, marks = world["prices"], world["divs"], world["ix"], world["marks"]
    secmap = {s["sid"]: s for s in secs}
    pen = [s["sid"] for s in secs if s["name"] == "Penrose Bank plc"][0]
    r = W.rng("fundloop")
    rd = W.rng("dealing")
    deal = dealing(rd)
    n = len(DAYS)
    moves = world["moves"]
    scrip = {}
    for tag, members in (("V", value), ("G", growth)):
        # each sub-adviser takes the scrip alternative on one dividend in the April to June quarter
        cands = []
        for s_ in members:
            if s_["name"] == "Penrose Bank plc" or s_["market"] == "AIM":
                continue
            for ev in divs[s_["sid"]]:
                if D(2026, 4, 13) <= ev["ex"] <= D(2026, 6, 30) and ev["pay"] <= D(2026, 9, 30):
                    cands.append((ev["ex"], s_["sid"], ev))
        cands.sort(key=lambda c: (c[0], c[1]))
        ex, sid0, ev = cands[len(cands) // 3]
        j = IDX[ex]
        ref = round(float(np.mean(prices[sid0][j:j + 5])) / 100, 4)
        scrip[(tag, sid0, ex)] = ref

    def mkt(sid, d):
        return W.market_on(secmap[sid], d, moves)

    def settle(d):
        if d == D(2026, 3, 30):
            return D(2026, 4, 7)      # in flight at the change of custodian, settled at Northcote after Easter
        if d == D(2026, 3, 31):
            return D(2026, 4, 8)
        return W.settle_date(d)

    def px(sid, i):
        if sid == pen and DAYS[i] >= W.PENROSE_SUSPENDED:
            return 0.0
        return prices[sid][i] / 100.0

    # opening sleeves
    wts = W.opening_weights(value, growth)

    def init_sleeve(members, val, tag):
        sids = [s["sid"] for s in members]
        w = [wts[tag][sid] for sid in sids]
        sh = {sid: int(math.floor(val * wt / px(sid, 0))) for sid, wt in zip(sids, w)}
        cash = val - sum(sh[sid] * px(sid, 0) for sid in sids)
        return sh, cash

    sh, cash, recv = {}, {}, {"V": {}, "G": {}}
    sh["V"], cash["V"] = init_sleeve(value, NAV0 * W.TARGET_V, "V")
    sh["G"], cash["G"] = init_sleeve(growth, NAV0 * W.TARGET_G, "G")
    C = NAV0 * W.TARGET_C
    L = 0.0
    units = {k: NAV0 * SHARE0[k] / (PRICE0[k] / 100) for k in CLASSES}
    price = dict(PRICE0)               # pence, unrounded
    nav_prev = NAV0
    ncon, code = 0, None
    active, order = False, None        # order: "on"/"off" placed at the last valuation point
    held = {"V": set(sh["V"]), "G": set(sh["G"])}
    universe_free = [s["sid"] for s in secs if s["market"] == "Main Market" and s["sid"] not in held["V"]
                     and s["sid"] not in held["G"] and s["sid"] != pen]

    rec = {k: np.zeros(n) for k in ("V", "G", "C", "L", "NAV", "TV", "TG", "TC", "fee", "flow", "futpnl", "ncon",
                                    "mark", "dd", "high", "expo", "phys", "rmmf", "dist_paid", "fut_cost")}
    rec["code"] = [None] * n
    rec["state"] = [""] * n
    rec["price"] = {k: np.zeros(n) for k in CLASSES}
    rec["units"] = {k: np.zeros(n) for k in CLASSES}
    rec["flowk"] = {k: np.zeros(n) for k in CLASSES}
    rec["dist"] = {}                   # (xd, class) -> pence per unit
    hold_log, trades, income, fut_trades, cash_log = [], [], [], [], []
    tref = 4_118_200
    pub_hist = []

    for i, d in enumerate(DAYS):
        cal = (d - DAYS[i - 1]).days if i else 0
        # corporate events: the entitlement at the ex-date, the cash at the pay date
        for tag in ("V", "G"):
            for sid in list(sh[tag]):
                for ev in divs[sid]:
                    if ev["ex"] == d and ev.get("pence", 0) > 0 and sh[tag][sid] > 0:
                        amt = round(sh[tag][sid] * ev["pence"] / 100, 2)
                        recv[tag][(sid, ev["ex"])] = (amt, ev["pay"], sh[tag][sid])
                        income.append(dict(sleeve=tag, sid=sid, ex=d, pay=ev["pay"], shares=sh[tag][sid],
                                           pence=ev["pence"], gbp=amt))
            for key, (amt, pay, q) in list(recv[tag].items()):
                if pay == d:
                    if (tag,) + key in scrip:
                        # the scrip alternative: new shares at the reference price, the fraction lapsing
                        ref = scrip[(tag,) + key]
                        newq = int(amt // ref)
                        sh[tag][key[0]] = sh[tag].get(key[0], 0) + newq
                        trades.append(dict(i=i, day=d, sleeve=tag, sid=key[0], side="SCRIP", qty=newq,
                                           price=round(ref * 100, 2), cons=0.0, comm=0.0, sdrt=0.0, kind="scrip",
                                           ref=None, settle=d))
                    else:
                        cash[tag] += amt
                    del recv[tag][key]
        # Penrose's suspension: the fair value is nil and its declared final dividend is written off
        if d == W.PENROSE_SUSPENDED:
            for key in [k for k in recv["V"] if k[0] == pen]:
                del recv["V"][key]
        # Penrose's shares are cancelled at the resolution
        if d == PENROSE_RESOLUTION and sh["V"].get(pen, 0) > 0:
            trades.append(dict(i=i, day=d, sleeve="V", sid=pen, side="X", qty=sh["V"][pen], price=0.0, cons=0.0,
                               comm=0.0, sdrt=0.0, kind="cancellation", ref=None, settle=d))
            del sh["V"][pen]
        # the money market fund and the futures since the last valuation point
        rmmf = W.mmf_rate(d) * cal / 365 if i else 0.0
        mark = marks[code][d] if (code and ncon) else 0.0
        futpnl = ncon * (marks[code][d] - marks[code][DAYS[i - 1]]) * MULT if (code and ncon and i) else 0.0
        C_pre = C * (1 + rmmf) + futpnl
        V = sum(sh["V"][sid] * px(sid, i) for sid in sh["V"]) + cash["V"] + sum(a for a, _, _ in recv["V"].values())
        G = sum(sh["G"][sid] * px(sid, i) for sid in sh["G"]) + cash["G"] + sum(a for a, _, _ in recv["G"].values())
        if i:
            g = (V + G + C_pre - L) / nav_prev - 1
        else:
            g = 0.0
        fee = 0.0
        newp = {}
        for k in CLASSES:
            f = price[k] * AMC[k] * cal / 365
            fee += units[k] * f / 100
            newp[k] = price[k] * (1 + g) - f
        # distributions to the income classes at the ex-distribution dates
        dist_add = 0.0
        for xd, pay in XD:
            if d == xd:
                for k in INCOME:
                    yld = 0.0178 if xd.month == 10 else 0.0151
                    dpu = round(newp[k] * (yld - AMC[k] / 2), 4)
                    rec["dist"][(xd, k)] = dpu
                    newp[k] -= dpu
                    dist_add += units[k] * dpu / 100
        L += dist_add
        dist_paid = 0.0
        for xd, pay in XD:
            if d == pay:
                dist_paid = L
                L = 0.0
        price = newp
        flow = 0.0
        for k in CLASSES:
            du = units[k] * deal[d][k] if i else 0.0
            units[k] += du
            fk = du * price[k] / 100
            rec["flowk"][k][i] = fk
            flow += fk
        C = C_pre + flow - fee - dist_paid
        nav = V + G + C - L
        chk = sum(units[k] * price[k] / 100 for k in CLASSES)
        assert abs(chk - nav) < 1e-3 * max(1.0, abs(nav)) * 1e-3, (d, chk, nav)
        rec["V"][i], rec["G"][i], rec["C"][i], rec["L"][i], rec["NAV"][i] = V, G, C, L, nav
        rec["fee"][i], rec["flow"][i], rec["futpnl"][i], rec["rmmf"][i] = fee, flow, futpnl, rmmf
        rec["dist_paid"][i] = dist_paid
        for k in CLASSES:
            rec["price"][k][i] = price[k]
            rec["units"][k][i] = units[k]
        # quarter-end rebalancing, after the valuation
        TV = TG = 0.0
        if last_of_quarter(d) and d > W.HIST_START:
            TV = W.TARGET_V * nav - V
            TG = W.TARGET_G * nav - G
            cash["V"] += TV
            cash["G"] += TG
            C -= TV + TG
            cash_log.append(dict(day=d, V=TV, G=TG))
        rec["TV"][i], rec["TG"][i], rec["TC"][i] = TV, TG, -(TV + TG)
        V += TV
        G += TG

        # the overlay: an order placed at the last valuation point takes effect at this one
        if order == "on":
            active = True
        elif order == "off":
            active = False
        order = None
        newcode = W.front_contract(d)[0]
        target = 0
        if active:
            m = marks[newcode][d]
            target = int(round((W.DEFENSIVE * nav - V - G) / (m * MULT)))
        fut_cost = 0.0
        if code and ncon and code != newcode:
            # roll: close the old contract and open the new one at this valuation point
            fut_trades.append(dict(day=d, code=code, qty=-ncon, price=marks[code][d], kind="roll"))
            fut_trades.append(dict(day=d, code=newcode, qty=ncon, price=marks[newcode][d], kind="roll"))
            fut_cost += 2 * abs(ncon) * FUT_COMMISSION
            code = newcode
        if target != ncon:
            c2 = newcode if target else code
            fut_trades.append(dict(day=d, code=c2, qty=target - ncon, price=marks[c2][d],
                                   kind="open" if ncon == 0 else ("close" if target == 0 else "adjust")))
            fut_cost += abs(target - ncon) * FUT_COMMISSION
            ncon = target
            code = newcode if ncon else None
        C -= fut_cost
        rec["fut_cost"][i] = fut_cost
        rec["ncon"][i] = ncon
        rec["code"][i] = code
        rec["mark"][i] = marks[code][d] if code else 0.0
        phys = (V + G) / nav
        notional = ncon * (marks[code][d] if code else 0.0) * MULT
        rec["phys"][i] = phys
        rec["expo"][i] = (V + G + notional) / nav
        # the rule, on the published B Accumulation price
        pub = round(price["B Acc"], 2)
        pub_hist.append(pub)
        hi = max(pub_hist[-W.WINDOW:])
        dd = 1 - pub / hi
        rec["dd"][i], rec["high"][i] = dd, hi
        if not active and dd > W.DD_IN:
            order = "on"
        elif active and dd <= W.DD_OUT:
            order = "off"
        rec["state"][i] = "REDUCED" if active else "FULL"

        # the sub-advisers' trading at this valuation point
        for tag in ("V", "G"):
            Vs = V if tag == "V" else G
            # an occasional exit and replacement
            if r.random() < 0.008 and len(universe_free) > 5:
                cands = [sid for sid in sh[tag] if sid != pen and px(sid, i) > 0]
                out_sid = cands[int(r.integers(len(cands)))]
                ind = secmap[out_sid]["industry"]
                pool = [sid for sid in universe_free if secmap[sid]["industry"] == ind] or universe_free
                in_sid = pool[int(r.integers(len(pool)))]
                universe_free.remove(in_sid)
                q = sh[tag][out_sid]
                p = px(out_sid, i)
                cons = round(q * p, 2)
                comm = round(cons * COMM_BP[tag] / 10_000, 2)
                tref += int(r.integers(3, 40))
                trades.append(dict(i=i, day=d, sleeve=tag, sid=out_sid, side="S", qty=q, price=prices[out_sid][i],
                                   cons=cons, comm=comm, sdrt=0.0, kind="exit", ref=tref, settle=settle(d)))
                cash[tag] += cons - comm
                del sh[tag][out_sid]
                p2 = px(in_sid, i)
                q2 = int((cons - comm) * 0.99 / p2 / (1 + W.SDRT))
                cons2 = round(q2 * p2, 2)
                comm2 = round(cons2 * COMM_BP[tag] / 10_000, 2)
                sdrt2 = round(cons2 * W.SDRT, 2) if mkt(in_sid, d) == "Main Market" else 0.0
                tref += int(r.integers(3, 40))
                trades.append(dict(i=i, day=d, sleeve=tag, sid=in_sid, side="B", qty=q2, price=prices[in_sid][i],
                                   cons=cons2, comm=comm2, sdrt=sdrt2, kind="entry", ref=tref, settle=settle(d)))
                cash[tag] -= cons2 + comm2 + sdrt2
                sh[tag][in_sid] = sh[tag].get(in_sid, 0) + q2
            if r.random() < 0.24:
                for _ in range(int(r.integers(1, 4))):
                    cands = [sid for sid in sh[tag] if px(sid, i) > 0 and sid != pen]
                    sid = cands[int(r.integers(len(cands)))]
                    p = px(sid, i)
                    val = float(r.uniform(0.0015, 0.0070)) * Vs
                    side = "B" if r.random() < 0.5 else "S"
                    q = int(val / p)
                    if side == "S":
                        q = min(q, sh[tag][sid] // 3)
                    if q <= 0:
                        continue
                    cons = round(q * p, 2)
                    comm = round(cons * COMM_BP[tag] / 10_000, 2)
                    sdrt = round(cons * W.SDRT, 2) if (side == "B" and mkt(sid, d) == "Main Market") else 0.0
                    tref += int(r.integers(3, 40))
                    if side == "B":
                        sh[tag][sid] += q
                        cash[tag] -= cons + comm + sdrt
                    else:
                        sh[tag][sid] -= q
                        cash[tag] += cons - comm
                    trades.append(dict(i=i, day=d, sleeve=tag, sid=sid, side=side, qty=q, price=prices[sid][i],
                                       cons=cons, comm=comm, sdrt=sdrt, kind="discretionary", ref=tref, settle=settle(d)))
            # the sleeve invests or raises cash beyond its working balance, across its holdings pro rata
            Vs = (V if tag == "V" else G)
            gap = cash[tag] - 0.006 * Vs
            if abs(gap) > 0.004 * Vs:
                tradable = {sid: sh[tag][sid] * px(sid, i) for sid in sh[tag] if px(sid, i) > 0}
                tot = sum(tradable.values())
                for sid in sorted(tradable):
                    amt = gap * tradable[sid] / tot
                    p = px(sid, i)
                    side = "B" if amt > 0 else "S"
                    q = int(abs(amt) / p / ((1 + W.SDRT) if side == "B" else 1))
                    if side == "S":
                        q = min(q, sh[tag][sid])
                    if q <= 0:
                        continue
                    cons = round(q * p, 2)
                    comm = round(cons * COMM_BP[tag] / 10_000, 2)
                    sdrt = round(cons * W.SDRT, 2) if (side == "B" and mkt(sid, d) == "Main Market") else 0.0
                    tref += int(r.integers(3, 40))
                    if side == "B":
                        sh[tag][sid] += q
                        cash[tag] -= cons + comm + sdrt
                    else:
                        sh[tag][sid] -= q
                        cash[tag] += cons - comm
                    trades.append(dict(i=i, day=d, sleeve=tag, sid=sid, side=side, qty=q, price=prices[sid][i],
                                       cons=cons, comm=comm, sdrt=sdrt,
                                       kind="rebalance" if (TV or TG) else "cash", ref=tref, settle=settle(d)))
        for tag in ("V", "G"):
            for sid, q in sh[tag].items():
                if q > 0:
                    hold_log.append((i, tag, sid, q))
            if pen in sh[tag] and tag == "V":
                pass
        nav_prev = nav

    return dict(rec=rec, holdings=hold_log, trades=trades, income=income, fut_trades=fut_trades,
                transfers=cash_log, pen=pen, deal=deal, scrip=scrip)


# ----------------------------------------------------------------------------------------------------------
# the replay
def recorded_inputs(world, actual):
    """The series a replay runs on, as the pack records them."""
    rec = actual["rec"]
    n = len(DAYS)
    rV = np.zeros(n); rG = np.zeros(n)
    for i in range(1, n):
        rV[i] = rec["V"][i] / (rec["V"][i - 1] + rec["TV"][i - 1]) - 1
        rG[i] = rec["G"][i] / (rec["G"][i - 1] + rec["TG"][i - 1]) - 1
    tr = world["ix"]["tr_noon"]
    rB = np.r_[0.0, tr[1:] / tr[:-1] - 1]
    return dict(rV=rV, rG=rG, rB=rB, rmmf=rec["rmmf"], marks=world["marks"], deal=actual["deal"],
                dist=rec["dist"], rec=rec)


def replay(inp, change=None, conv=None, start=None, end=None):
    """Restate the fund from `start` (the year's base valuation point) for a change in force from then.

    change: None, "A" (value sleeve tracks the benchmark), "B" (growth sleeve tracks the benchmark), "C" (trigger at
    12 per cent), "D" (restore within 6 per cent), "E" (futures equal to the liquidity sleeve).
    conv: dict of convention switches (flows, weights, lag, window, fees) for the standing-family measurement.
    """
    conv = dict(conv or {})
    rec = inp["rec"]
    i0 = YEAR0 if start is None else start
    i1 = YEAR1 if end is None else end
    dd_in = 0.12 if change == "C" else W.DD_IN
    dd_out = 0.06 if change == "D" else W.DD_OUT
    lag = conv.get("lag", 1)
    window = conv.get("window", W.WINDOW)
    # state at the base valuation point, as recorded (after that point's rebalancing and futures)
    V = rec["V"][i0] + rec["TV"][i0]
    G = rec["G"][i0] + rec["TG"][i0]
    C = rec["C"][i0] + rec["TC"][i0] - rec["fut_cost"][i0]
    L = rec["L"][i0]
    units = {k: rec["units"][k][i0] for k in CLASSES}
    price = {k: rec["price"][k][i0] for k in CLASSES}
    ncon = int(rec["ncon"][i0])
    code = rec["code"][i0]
    pub_hist = [round(rec["price"]["B Acc"][j], 2) for j in range(max(0, i0 - window + 1), i0 + 1)]
    active = rec["state"][i0] == "REDUCED"
    order_q = []
    # the rule state at the base point: replay what was pending there
    out_price = [price["B Acc"]]
    out_expo = [rec["expo"][i0]]
    out_state = [rec["state"][i0]]
    nav_prev = rec["NAV"][i0]
    for i in range(i0 + 1, i1 + 1):
        d = DAYS[i]
        cal = (d - DAYS[i - 1]).days
        rv = inp["rB"][i] if change == "A" else inp["rV"][i]
        rg = inp["rB"][i] if change == "B" else inp["rG"][i]
        V = V * (1 + rv)
        G = G * (1 + rg)
        futpnl = ncon * (inp["marks"][code][d] - inp["marks"][code][DAYS[i - 1]]) * MULT if (ncon and code) else 0.0
        C_pre = C * (1 + inp["rmmf"][i]) + futpnl
        if conv.get("weights") == "fixed":
            pass
        g = (V + G + C_pre - L) / nav_prev - 1
        fee = 0.0
        newp = {}
        for k in CLASSES:
            f = price[k] * AMC[k] * cal / 365
            fee += units[k] * f / 100
            newp[k] = price[k] * (1 + g) - f
        for xd, pay in XD:
            if d == xd:
                for k in INCOME:
                    dpu = inp["dist"][(xd, k)] if conv.get("dist", "units") == "units" else \
                        newp[k] * inp["dist"][(xd, k)] / rec["price"][k][i]
                    newp[k] -= dpu
                    L += units[k] * dpu / 100
        dist_paid = 0.0
        for xd, pay in XD:
            if d == pay:
                dist_paid = L
                L = 0.0
        price = newp
        flow = 0.0
        for k in CLASSES:
            if conv.get("flows", "fraction") == "fraction":
                du = units[k] * inp["deal"][d][k]
            elif conv["flows"] == "pounds":
                du = rec["flowk"][k][i] / (price[k] / 100)
            else:
                du = 0.0
            units[k] += du
            flow += du * price[k] / 100
        C = C_pre + flow - fee - dist_paid
        nav = V + G + C - L
        C_before = C
        if last_of_quarter(d):
            TV = W.TARGET_V * nav - V
            TG = W.TARGET_G * nav - G
            V += TV
            G += TG
            C -= TV + TG
        # the rule on this valuation point's price, then the overlay's position
        pub = round(price["B Acc"], 2)
        pub_hist.append(pub)
        hi = max(pub_hist[-window:]) if conv.get("include_day", True) else max(pub_hist[-window - 1:-1])
        dd = 1 - pub / hi
        pending = order_q[-1][1] if order_q else None
        is_on = (active if pending is None else pending == "on")
        if not is_on and dd > dd_in:
            order_q.append((i + lag, "on"))
        elif is_on and dd <= dd_out:
            order_q.append((i + lag, "off"))
        while order_q and order_q[0][0] <= i:
            active = order_q.pop(0)[1] == "on"
        newcode = W.front_contract(d)[0]
        target = 0
        if change == "E" and not active:
            m = inp["marks"][newcode][d]
            # the review terms size these futures on the liquidity sleeve after a quarter-end's transfer; the
            # "pre" switch sizes them on the value before it, the reading the terms close (SF31)
            target = int(round((C_before if conv.get("e_sizing") == "pre" else C) / (m * MULT)))
        if active:
            m = inp["marks"][newcode][d]
            target = int(round((W.DEFENSIVE * nav - V - G) / (m * MULT)))
        fut_cost = 0.0
        if code and ncon and code != newcode:
            fut_cost += 2 * abs(ncon) * FUT_COMMISSION
            code = newcode
        if target != ncon:
            fut_cost += abs(target - ncon) * FUT_COMMISSION
            ncon = target
            code = newcode if ncon else None
        C -= fut_cost if conv.get("costs", True) else 0.0
        notional = ncon * (inp["marks"][code][d] if code else 0.0) * MULT
        out_price.append(price["B Acc"])
        out_expo.append((V + G + notional) / nav)
        out_state.append("REDUCED" if active else "FULL")
        nav_prev = nav
    return dict(price=np.array(out_price), expo=np.array(out_expo), state=out_state)


def replay_held(inp, change):
    """The exposure-held restatement: the change applied with the overlay's recorded futures position kept."""
    rec = inp["rec"]
    i0, i1 = YEAR0, YEAR1
    V = rec["V"][i0] + rec["TV"][i0]
    G = rec["G"][i0] + rec["TG"][i0]
    C = rec["C"][i0] + rec["TC"][i0] - rec["fut_cost"][i0]
    L = rec["L"][i0]
    units = {k: rec["units"][k][i0] for k in CLASSES}
    price = {k: rec["price"][k][i0] for k in CLASSES}
    nav_prev = V + G + C - L
    out = [price["B Acc"]]
    for i in range(i0 + 1, i1 + 1):
        d = DAYS[i]
        cal = (d - DAYS[i - 1]).days
        rv = inp["rB"][i] if change == "A" else inp["rV"][i]
        rg = inp["rB"][i] if change == "B" else inp["rG"][i]
        V = V * (1 + rv)
        G = G * (1 + rg)
        ncon, code = int(rec["ncon"][i - 1]), rec["code"][i - 1]
        futpnl = ncon * (inp["marks"][code][d] - inp["marks"][code][DAYS[i - 1]]) * MULT if (ncon and code) else 0.0
        if change == "E":
            ncodex = W.front_contract(DAYS[i - 1])[0]
            nE = int(round(C / (inp["marks"][ncodex][DAYS[i - 1]] * MULT))) if not ncon else 0
            futpnl += nE * (inp["marks"][ncodex][d] - inp["marks"][ncodex][DAYS[i - 1]]) * MULT
        C_pre = C * (1 + inp["rmmf"][i]) + futpnl
        g = (V + G + C_pre - L) / nav_prev - 1
        fee = 0.0
        newp = {}
        for k in CLASSES:
            f = price[k] * AMC[k] * cal / 365
            fee += units[k] * f / 100
            newp[k] = price[k] * (1 + g) - f
        for xd, pay in XD:
            if d == xd:
                for k in INCOME:
                    dpu = inp["dist"][(xd, k)]
                    newp[k] -= dpu
                    L += units[k] * dpu / 100
        dist_paid = 0.0
        for xd, pay in XD:
            if d == pay:
                dist_paid = L
                L = 0.0
        price = newp
        flow = 0.0
        for k in CLASSES:
            du = units[k] * inp["deal"][d][k]
            units[k] += du
            flow += du * price[k] / 100
        C = C_pre + flow - fee - dist_paid - rec["fut_cost"][i]
        nav = V + G + C - L
        if last_of_quarter(d):
            TV = W.TARGET_V * nav - V
            TG = W.TARGET_G * nav - G
            V += TV
            G += TG
            C -= TV + TG
        out.append(price["B Acc"])
        nav_prev = nav
    return np.array(out)


def build_world():
    secs = W.securities()
    value, growth, reclass = W.assign_portfolios(secs)
    mk = W.market()
    rets = W.stock_returns(secs, value, growth, mk)
    divs = W.dividends(secs)
    prices = W.price_paths(secs, rets, divs)
    closes = W.close_prices(secs, prices, mk)
    pen = [s["sid"] for s in secs if s["name"] == "Penrose Bank plc"][0]
    pen_ret = np.r_[0.0, prices[pen][1:] / prices[pen][:-1] - 1]
    for i, d in enumerate(DAYS):
        if d >= W.PENROSE_SUSPENDED:
            pen_ret[i] = -1.0 if d == W.PENROSE_SUSPENDED else 0.0
    ix = W.index_series(mk, pen_ret)
    marks = W.futures_marks(ix)
    moves = W.listing_moves(secs, growth)
    return dict(secs=secs, value=value, growth=growth, reclass=reclass, mk=mk, rets=rets, divs=divs, prices=prices,
                closes=closes, ix=ix, marks=marks, moves=moves)

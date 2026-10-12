"""The trust's book as the custodian holds it, from the window's first valuation to the valuation date.

The Fernside mandate: tax lots of UK shares in two designations, cash, accrued income between ex and pay dates,
dividends (the REITs paying a property income distribution and an ordinary dividend on one ex-date), a 1-for-8
consolidation, a demerger whose new shares are credited the business day after the parent goes ex, a rights issue
taken up (nil-paid rights carried as their own lines), and a cash takeover. The Kestwick funds: income units in the
permanent endowment and accumulation units in the expendable endowment. Every quarter end the portfolio is
rebalanced to the policy weights at the 80 per cent growth share; the mandate side of that is a transfer of cash
into or out of the mandate, invested or raised by the manager the same day. A legacy came into the permanent
endowment's mandate account in May 2025. Fernside's fee is taken from the mandate's cash each quarter.
"""
import datetime as dt
import math

import numpy as np

import world as W
import sim as SM

RIGHTS_CODE = "BF100286R"
CASH_CODE = "GBPCASH"
QUARTER_ENDS = [dt.date(2024, 12, 31), dt.date(2025, 3, 31), dt.date(2025, 6, 30), dt.date(2025, 9, 30),
                dt.date(2025, 12, 31), dt.date(2026, 3, 31), dt.date(2026, 6, 30), dt.date(2026, 9, 30)]
FEE_RATE = 0.0045
START_TOTAL = 37_351_806.0


class Book:
    pass


def fund_codes():
    return {f: ("KWC%s%s" % (f[:2], "I"), "KWC%s%s" % (f[:2], "A")) for f in W.FUNDS}


def run(M, seed, fp, lot_mix=None, keep_rows=True, start_total=None, knobs=None):
    """knobs (income devices, none of which moves a return): nov25 scales the dividends that go ex in November 2025;
    pid_shift moves the REITs' property income distribution share of each distribution"""
    knobs = knobs or {}
    lot_mix = lot_mix or W.LOT_MIX
    rng = np.random.default_rng(seed)
    rngd = np.random.default_rng(seed + 101)
    rngl = np.random.default_rng(seed + 202)          # tax lots and their identifiers
    rngn = np.random.default_rng(seed + 303)          # narratives
    days = [d for d in M["days"] if W.WIN_START <= d <= W.VAL_DATE]
    n = len(days)
    i0 = M["days"].index(W.WIN_START)
    ukf = np.array(M["UKF"][i0:i0 + n])
    dUK = np.diff(ukf, prepend=ukf[0])
    stocks = list(W.STOCKS) + [W.DEMERGED]
    info = {s[0]: dict(name=s[1], sector=s[2], beta=s[3], iv=s[4], p0=s[5], dy=s[6] * knobs.get("dy", W.DIV_SCALE),
                       months=s[7], reit=s[8])
            for s in stocks}
    codes = [s[0] for s in stocks]
    eps = {c: rng.normal(0, info[c]["iv"], n) for c in codes}
    tk_ref, tk_code, tk_ann, tk_eff, tk_prem = W.TAKEOVER
    dm_ref, dm_code, dm_ex, dm_ratio, dm_share = W.DEMERGER
    co_ref, co_code, co_eff, co_ratio = W.CONSOLIDATION
    ri_ref, ri_code, ri_ex, ri_take, ri_ratio, ri_disc = W.RIGHTS
    dm_new = W.DEMERGED[0]
    dm_credit = W.add_bdays(dm_ex, 1)

    # ------------------------------------------------------------ dividend calendar
    events = []                 # dict(code, ref, type, ex, pay, dps)
    refno = [41270]

    def newref():
        refno[0] += int(rngd.integers(3, 29))
        return "DV%06d" % refno[0]
    for c in codes:
        lag = int(rngd.choice([33, 35, 36, 40, 42]))
        if c == tk_code:
            lag = 33
        for y in (2024, 2025, 2026):
            for k, m in enumerate(info[c]["months"]):
                ex = SM.nth_weekday(y, m, 3, 2)
                if not (days[0] < ex <= days[-1]):
                    continue
                if c == tk_code and ex >= tk_ann:
                    if ex >= tk_eff:
                        continue
                if c == dm_new and ex <= dm_credit:
                    continue
                pay = ex + dt.timedelta(days=lag)
                while not W.is_bday(pay, "UK"):
                    pay += dt.timedelta(days=1)
                nper = len(info[c]["months"])
                share = (0.38 if k == 0 else 0.62) if nper == 2 else 1.0 / nper
                events.append(dict(code=c, ex=ex, pay=pay, share=share, noise=float(rngd.normal(0, 0.04)),
                                   pid=float(rngd.uniform(0.72, 0.84))))
    ex_by = {}
    for e in events:
        ex_by.setdefault(e["ex"], []).append(e)

    # ------------------------------------------------------------ opening positions and lots
    lot_no = [int(rngl.integers(30_000_000, 31_000_000))]

    def new_lot_id():
        lot_no[0] += int(rngl.integers(1, 40))
        return "L%08d" % lot_no[0]
    subs = list(W.SUB_ACCOUNTS)
    sub_total = {s: (start_total or START_TOTAL) * W.SUB_SHARE[s] for s in subs}
    w80 = W.weights(W.SHARE_2026)
    lots = []                   # dict(sub, code, lot_id, open, qty)
    start_codes = [s[0] for s in W.STOCKS]
    wts = rng.dirichlet(np.full(len(start_codes), 5.0))
    for s in subs:
        held = [c for c in start_codes if rng.random() < 0.97]
        tot = sum(wts[start_codes.index(c)] for c in held)
        mand = sub_total[s] * w80["MAND"] * 0.985
        for c in held:
            val = mand * wts[start_codes.index(c)] / tot
            q = int(round(val / info[c]["p0"], -1))
            k = int(rngl.choice([1, 2, 3, 4], p=list(lot_mix)))
            cuts = np.sort(rngl.uniform(0.15, 0.85, k - 1)) if k > 1 else np.array([])
            qs = [int(round(q * x)) for x in cuts]
            sizes = np.diff([0] + qs + [q])
            opens = sorted(dt.date(2011, 1, 1) + dt.timedelta(days=int(x)) for x in rngl.integers(0, 4900, k))
            for size, od in zip(sizes, opens):
                while not W.is_bday(od, "UK"):
                    od += dt.timedelta(days=1)
                lots.append(dict(sub=s, code=c, lot_id=new_lot_id(), open=od, qty=int(size)))
    cash = {s: round(sub_total[s] * w80["MAND"] * 0.015, 2) for s in subs}
    fcode = fund_codes()
    fidx = {d: k for k, d in enumerate(M["days"])}

    def fprice(f, s, d):
        k = fidx[d]
        return fp[f]["inc"][k] if W.SUB_UNIT[s] == "inc" else fp[f]["acc"][k]
    units = {(s, f): round(sub_total[s] * w80[f] / fprice(f, s, days[0]), 3) for s in subs for f in W.FUNDS}
    unit_hist = {key: [(days[0] - dt.timedelta(days=1), u)] for key, u in units.items()}

    # ------------------------------------------------------------ the daily book
    price = {c: np.full(n, np.nan) for c in codes}
    for c in start_codes:
        price[c][0] = info[c]["p0"]
    rights_price = np.full(n, np.nan)
    accrued = []                # dict(sub, code, lot_id, ref, pay, amount)
    ent = []                    # entitlements: dict(sub, code, ref, type, ex, pay, amount, lots=[(lot_id, open, qty)])
    moves = []                  # (date, sub, type, amount, narrative, code)
    rows = [] if keep_rows else None
    V = np.zeros(n)
    Vsub = {s: np.zeros(n) for s in subs}
    flows = np.zeros(n)
    offer = None
    ri_sub = None
    dm_pre = None
    fee_days = {W.add_bdays(q, 8): q for q in QUARTER_ENDS}
    legacy_day, legacy_sub, legacy_amt, legacy_text = W.LEGACY
    # the legacy is sized with the portfolio, so the book is the same at any size
    legacy_amt = round(legacy_amt * (start_total or START_TOTAL) / START_TOTAL, 2)
    narrative_pool = {"buy": ["Purchase %s", "Bought %s", "Purchase of %s"], "sell": ["Sale %s", "Sold %s", "Sale of %s"]}

    def mv_mand(s, k):
        t = cash[s]
        for L in lots:
            if L["sub"] == s:
                p = rights_price[k] if L["code"] == RIGHTS_CODE else price[L["code"]][k]
                t += round(L["qty"] * p, 2)
        return t

    def buy(s, k, amount, ncount, d):
        held = sorted({L["code"] for L in lots if L["sub"] == s and L["code"] not in (RIGHTS_CODE, tk_code)})
        pool = held
        # new money is spread so that no single purchase is much over 1.5 per cent of the designation's mandate
        ncount = max(ncount, int(math.ceil(amount / (W.BUY_CAP * mv_mand(s, k)))))
        pick = list(rng.choice(pool, size=min(ncount, len(pool)), replace=False))
        spent = 0.0
        split = rng.dirichlet(np.full(len(pick), 4.0))
        for j, c in enumerate(pick):
            amt = amount * split[j]
            q = int(amt // price[c][k])
            if q <= 0:
                continue
            cost = round(q * price[c][k], 2)
            lots.append(dict(sub=s, code=c, lot_id=new_lot_id(), open=d, qty=q))
            cash[s] = round(cash[s] - cost, 2)
            spent += cost
            moves.append((d, s, "Purchase", -cost, rngn.choice(narrative_pool["buy"]) % info[c]["name"], c))
        return spent

    def sell(s, k, amount, ncount, d):
        """raise `amount` from the designation's holdings, taking at most 60 per cent of a holding's largest lot and
        moving on to the next holding for any shortfall"""
        held = sorted({L["code"] for L in lots if L["sub"] == s and L["code"] not in (RIGHTS_CODE, tk_code, dm_new)})
        order = [str(c) for c in rng.permutation(held)]
        n0 = min(ncount, len(order))
        split = rng.dirichlet(np.full(n0, 4.0))
        plan = [(c, amount * split[j]) for j, c in enumerate(order[:n0])]
        rest = order[n0:]
        got = 0.0
        while plan:
            c, need = plan.pop(0)
            mine = sorted([L for L in lots if L["sub"] == s and L["code"] == c], key=lambda L: -L["qty"])
            q = int(math.ceil(need / price[c][k]))
            q = min(q, int(mine[0]["qty"] * 0.6))
            proceeds = 0.0
            if q > 0:
                mine[0]["qty"] -= q
                proceeds = round(q * price[c][k], 2)
                cash[s] = round(cash[s] + proceeds, 2)
                got += proceeds
                moves.append((d, s, "Sale", proceeds, rngn.choice(narrative_pool["sell"]) % info[c]["name"], c))
            if need - proceeds > 1.0 and rest:
                plan.append((rest.pop(0), need - proceeds))
        return got

    for k, d in enumerate(days):
        # prices
        if k > 0:
            for c in codes:
                p = price[c][k - 1]
                if c == dm_new:
                    if d == dm_credit:
                        p = dm_pre * dm_share * dm_ratio
                    elif np.isnan(p):
                        continue
                elif np.isnan(p):
                    continue
                if c == tk_code and offer is not None:
                    if d >= tk_eff:
                        continue
                    left = max((tk_eff - d).days, 0)
                    price[c][k] = round(offer * (1 - 0.00035 * left - abs(rng.normal(0, 0.0007))), 4)
                    continue
                p = p * math.exp(info[c]["beta"] * dUK[k] + eps[c][k])
                if c == tk_code and d == tk_ann:
                    offer = round(price[c][k - 1] * tk_prem, 2)
                    p = offer * 0.976
                if c == dm_code and d == dm_ex:
                    dm_pre = p
                    p = p * (1 - dm_share)
                if c == co_code and d == co_eff:
                    p = p * co_ratio
                if c == ri_code and d == ri_ex:
                    ri_sub = round(p * ri_disc, 2)
                    p = (ri_ratio * p + ri_sub) / (ri_ratio + 1)
                for e in ex_by.get(d, []):
                    if e["code"] == c:
                        q = price[c][k - 1] * info[c]["dy"] * e["share"] * (1 + e["noise"])
                        if dt.date(2025, 11, 1) <= d <= dt.date(2025, 11, 30):
                            q *= knobs.get("nov25", 1.0)
                        q = round(q, 4)
                        e["dps"] = q
                        p -= q
                price[c][k] = round(p, 4)
        if ri_ex <= d < ri_take:
            rights_price[k] = round(max(price[ri_code][k] - ri_sub, 0.0), 4)
        # ex-dividend: the record is the holding at the previous close
        for e in ex_by.get(d, []):
            if "dps" not in e:
                continue
            c = e["code"]
            for s in subs:
                mine = [L for L in lots if L["sub"] == s and L["code"] == c and L["qty"] > 0]
                if not mine:
                    continue
                if info[c]["reit"]:
                    pid = round(e["dps"] * (e["pid"] + knobs.get("pid_shift", 0.0)), 4)
                    parts = [("PID", pid), ("DIV", round(e["dps"] - pid, 4))]
                else:
                    parts = [("DIV", e["dps"])]
                for typ, rate in parts:
                    key = (c, typ, e["ex"])
                    if key not in e.setdefault("refs", {}):
                        e["refs"][key] = newref()
                    amt = round(sum(L["qty"] for L in mine) * rate, 2)
                    ent.append(dict(sub=s, code=c, ref=e["refs"][key], type=typ, ex=e["ex"], pay=e["pay"], rate=rate,
                                    amount=amt, lots=[(L["lot_id"], L["open"], L["qty"]) for L in mine]))
                    for L in mine:
                        accrued.append(dict(sub=s, code=c, lot_id=L["lot_id"], ref=e["refs"][key], pay=e["pay"],
                                            amount=round(L["qty"] * rate, 2)))
        # income paid
        paid = [a for a in accrued if a["pay"] == d]
        if paid:
            bys = {}
            for a in paid:
                bys.setdefault((a["sub"], a["ref"], a["code"]), 0.0)
                bys[(a["sub"], a["ref"], a["code"])] += a["amount"]
            for (s, r, c), amt in sorted(bys.items()):
                cash[s] = round(cash[s] + amt, 2)
                moves.append((d, s, "Dividend received", round(amt, 2), "%s %s" % (info[c]["name"], r), c))
            accrued = [a for a in accrued if a["pay"] != d]
        # corporate actions
        if d == co_eff:
            for L in [L for L in lots if L["code"] == co_code]:
                q, frac = divmod(L["qty"], co_ratio)
                L["qty"] = q
                if frac:
                    cil = round(frac / co_ratio * price[co_code][k], 2)
                    cash[L["sub"]] = round(cash[L["sub"]] + cil, 2)
                    moves.append((d, L["sub"], "Cash in lieu", cil, "%s consolidation fractions" % info[co_code]["name"], co_code))
        if d == dm_credit:
            for L in [L for L in lots if L["code"] == dm_code]:
                q = L["qty"] // dm_ratio
                if q:
                    lots.append(dict(sub=L["sub"], code=dm_new, lot_id=new_lot_id(), open=L["open"], qty=q))
        if d == ri_ex:
            for L in [L for L in lots if L["code"] == ri_code]:
                q = L["qty"] // ri_ratio
                if q:
                    lots.append(dict(sub=L["sub"], code=RIGHTS_CODE, lot_id=new_lot_id(), open=d, qty=q))
        if d == ri_take:
            for s in subs:
                rl = [L for L in lots if L["sub"] == s and L["code"] == RIGHTS_CODE]
                q = sum(L["qty"] for L in rl)
                if q:
                    cost = round(q * ri_sub, 2)
                    cash[s] = round(cash[s] - cost, 2)
                    moves.append((d, s, "Rights subscription", -cost, "%s rights issue: %d new shares taken up" % (info[ri_code]["name"], q), ri_code))
                    lots.append(dict(sub=s, code=ri_code, lot_id=new_lot_id(), open=d, qty=q))
            lots = [L for L in lots if L["code"] != RIGHTS_CODE]
        if d == tk_eff:
            for s in subs:
                tl = [L for L in lots if L["sub"] == s and L["code"] == tk_code]
                q = sum(L["qty"] for L in tl)
                if q:
                    amt = round(q * offer, 2)
                    cash[s] = round(cash[s] + amt, 2)
                    moves.append((d, s, "Takeover consideration", amt, "%s scheme of arrangement" % info[tk_code]["name"], tk_code))
            lots = [L for L in lots if L["code"] != tk_code]
        # management fee from the mandate's cash
        if d in fee_days:
            for s in subs:
                fee = round(mv_mand(s, k) * FEE_RATE / 4, 2)
                cash[s] = round(cash[s] - fee, 2)
                moves.append((d, s, "Management fee", -fee, "Fernside Partners fee, quarter to %s" % fee_days[d].strftime("%d %B %Y").lstrip("0"), ""))
        # the legacy, held in the mandate's cash until the quarter-end rebalancing
        if d == legacy_day:
            s = legacy_sub
            cash[s] = round(cash[s] + legacy_amt, 2)
            flows[k] += legacy_amt
            moves.append((d, s, "Contribution", legacy_amt, legacy_text, ""))
        # quarter-end rebalancing to the policy weights
        if d in QUARTER_ENDS:
            for s in subs:
                fund_val = sum(round(units[(s, f)] * fprice(f, s, d), 2) for f in W.FUNDS)
                mand = mv_mand(s, k)
                total = fund_val + mand
                # the capital the trustees release from the expendable endowment for the year's grants, drawn each
                # quarter end across its holdings at the policy weights
                if s == "WRX-EX02" and d in W.RELEASES:
                    total = round(total * (1 - W.RELEASES[d]), 2)
                flow = round(total * w80["MAND"] - mand, 2)
                for f in W.FUNDS:
                    units[(s, f)] = round(total * w80[f] / fprice(f, s, d), 3)
                    unit_hist[(s, f)].append((d, units[(s, f)]))
                buffer = round(0.012 * total * w80["MAND"], 2)
                if flow >= 0:
                    cash[s] = round(cash[s] + flow, 2)
                    moves.append((d, s, "Contribution", flow, "Quarterly rebalancing transfer from the trust", ""))
                else:
                    need = -flow - (cash[s] - buffer)
                    if need > 0:
                        sell(s, k, need * 1.01, int(rng.integers(2, 4)), d)
                    cash[s] = round(cash[s] + flow, 2)
                    moves.append((d, s, "Withdrawal", flow, "Quarterly rebalancing transfer to the trust", ""))
                if cash[s] > buffer * 1.5:
                    buy(s, k, cash[s] - buffer, 1, d)
                flows[k] += flow
        # the day's valuation
        acc_by_lot = {}
        for a in accrued:
            acc_by_lot[a["lot_id"]] = acc_by_lot.get(a["lot_id"], 0.0) + a["amount"]
        for s in subs:
            tot = 0.0
            for L in lots:
                if L["sub"] != s or L["qty"] <= 0:
                    continue
                c = L["code"]
                p = rights_price[k] if c == RIGHTS_CODE else price[c][k]
                mv = round(L["qty"] * p, 2)
                ai = round(acc_by_lot.get(L["lot_id"], 0.0), 2)
                tot += mv + ai
                if keep_rows:
                    rows.append((d, s, c, L["lot_id"], L["open"], L["qty"], p, mv, ai))
            tot += cash[s]
            if keep_rows:
                rows.append((d, s, CASH_CODE, "", None, cash[s], 1.0, cash[s], 0.0))
                for f in W.FUNDS:
                    p = fprice(f, s, d)
                    code = fcode[f][0] if W.SUB_UNIT[s] == "inc" else fcode[f][1]
                    rows.append((d, s, code, "", None, units[(s, f)], p, round(units[(s, f)] * p, 2), 0.0))
            Vsub[s][k] = tot
        V[k] = sum(Vsub[s][k] for s in subs)

    B = Book()
    B.days, B.price, B.info, B.rights_price = days, price, info, rights_price
    B.events, B.ent, B.moves, B.rows, B.V, B.Vsub, B.flows = events, ent, moves, rows, V, Vsub, flows
    B.lots, B.cash, B.units, B.offer, B.ri_sub, B.dm_pre = lots, cash, units, offer, ri_sub, dm_pre
    B.fp, B.fcode, B.fprice, B.unit_hist = fp, fcode, fprice, unit_hist
    # the mandate's time-weighted daily return, the demerged shares carried on the parent's ex-date at their
    # first price
    kx = days.index(dm_ex)
    kc = days.index(dm_credit)
    newq = sum(L["qty"] for L in lots if L["code"] == dm_new and L["open"] < dm_credit)
    B.dm_adj = round(newq * price[dm_new][kc], 2)
    Vc = V.copy()
    Vc[kx] += B.dm_adj
    B.r_mand = (Vc[1:] - flows[1:]) / Vc[:-1] - 1
    B.r_raw = (V[1:] - flows[1:]) / V[:-1] - 1
    return B


def fund_returns(fp, M, days):
    """each fund's daily total return from its income units with the distribution added back"""
    fidx = {d: k for k, d in enumerate(M["days"])}
    ks = [fidx[d] for d in days]
    out = {}
    for f in W.FUNDS:
        inc, dist = fp[f]["inc"][ks], fp[f]["dist"][ks]
        out[f] = (inc[1:] + dist[1:]) / inc[:-1] - 1
    return out

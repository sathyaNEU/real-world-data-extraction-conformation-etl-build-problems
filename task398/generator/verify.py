"""Independent verifier: recompute every graded figure from the files in target/ alone, with the fund's mechanics
read from the prospectus and the review terms, and compare with figures.json. Imports no generator module."""
import csv
import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ISO = dt.date.fromisoformat
CLASSES = ["B Acc", "B Inc", "C Acc", "C Inc"]
AMC = {"B Acc": 0.0085, "B Inc": 0.0085, "C Acc": 0.0060, "C Inc": 0.0060}
UK_HOLIDAYS = {dt.date(2025, 8, 25), dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1),
               dt.date(2026, 4, 3), dt.date(2026, 4, 6), dt.date(2026, 5, 4), dt.date(2026, 5, 25),
               dt.date(2026, 8, 31)}
Y0, Y1 = dt.date(2025, 9, 30), dt.date(2026, 9, 30)


def rows(target, fn):
    with open(os.path.join(target, fn), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def dmy(s):
    d, m, y = s.split("/")
    return dt.date(int(y), int(m), int(d))


def load(target):
    val = rows(target, "thornbury_mruke_valuation_summary.csv")
    days = [ISO(r["valuation_date"]) for r in val]
    V = {ISO(r["valuation_date"]): r for r in val}
    cls = {}
    for r in rows(target, "thornbury_mruke_share_class_prices.csv"):
        cls[(ISO(r["valuation_date"]), r["share_class"])] = r
    ix = {}
    for r in rows(target, "larkspur_index_levels_2025-26.csv"):
        ix[(ISO(r["date"]), r["index_code"], r["return_type"], r["calculation"])] = float(r["level"])
    mmf = {ISO(r["date"]): float(r["one_day_yield_annualised_pct"]) / 100
           for r in rows(target, "sterling_liquidity_fund_daily_yield.csv")}
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(target, "merrow_overlay_daily_monitor_2025-26.xlsx"), read_only=True).active
    marks, held = {}, {}
    for row in ws.iter_rows(min_row=6, values_only=True):
        if row[0] is None:
            continue
        d = row[0].date() if hasattr(row[0], "date") else row[0]
        marks[(d, row[12])] = float(row[13])
        marks[(d, row[14])] = float(row[15])
        if row[7]:
            marks[(d, row[7])] = float(row[9])
        held[d] = (row[7], int(row[8] or 0))
    comm = 0.0
    for r in rows(target, "merrow_futures_blotter_2026.csv"):
        comm = float(r["commission_gbp"]) / int(r["contracts"])
    return dict(days=days, V=V, cls=cls, ix=ix, mmf=mmf, marks=marks, held=held, comm=comm)


def contracts():
    out = []
    for y in (2025, 2026, 2027):
        for m, c in ((3, "H"), (6, "M"), (9, "U"), (12, "Z")):
            d = dt.date(y, m, 1)
            while d.weekday() != 4:
                d += dt.timedelta(days=1)
            out.append(("LKX%s%s" % (c, str(y)[-1]), d + dt.timedelta(days=14)))
    return out


def replay(L, change):
    """the prospectus's fund, valuation point by valuation point, from 30 September 2025"""
    days = L["days"]
    k0, k1 = days.index(Y0), days.index(Y1)
    idx = {d: i for i, d in enumerate(days)}
    cons = contracts()

    def held_code(d):
        for code, exp in cons:
            if exp in idx and idx[exp] - idx[d] > 5:
                return code
            if exp not in idx and exp > d:
                return code

    f = lambda d, k: float(L["V"][d][k])
    d0 = days[k0]
    Vs = f(d0, "value_sleeve_gbp") + f(d0, "value_sleeve_transfer_gbp")
    Gs = f(d0, "growth_sleeve_gbp") + f(d0, "growth_sleeve_transfer_gbp")
    C = f(d0, "liquidity_sleeve_gbp") + f(d0, "liquidity_sleeve_transfer_gbp")
    Lp = f(d0, "distributions_payable_gbp")
    nav_prev = f(d0, "net_asset_value_gbp")
    units = {k: float(L["cls"][(d0, k)]["units_in_issue"]) for k in CLASSES}
    price = {k: float(L["cls"][(d0, k)]["price_gbx"]) for k in CLASSES}
    hist = [float(L["cls"][(days[j], "B Acc")]["price_gbx"]) for j in range(k0 - 62, k0 + 1)]
    trig = 0.12 if change == "C" else 0.08
    rest = 0.06 if change == "D" else 0.04
    active, order, n, code = False, None, 0, None
    path, states = [price["B Acc"]], ["FULL"]
    for j in range(k0 + 1, k1 + 1):
        d, dp = days[j], days[j - 1]
        cal = (d - dp).days
        rb = L["ix"][(d, "LKUKAS", "TR", "12:00")] / L["ix"][(dp, "LKUKAS", "TR", "12:00")] - 1
        rv = f(d, "value_sleeve_gbp") / (f(dp, "value_sleeve_gbp") + f(dp, "value_sleeve_transfer_gbp")) - 1
        rg = f(d, "growth_sleeve_gbp") / (f(dp, "growth_sleeve_gbp") + f(dp, "growth_sleeve_transfer_gbp")) - 1
        Vs *= 1 + (rb if change == "A" else rv)
        Gs *= 1 + (rb if change == "B" else rg)
        pnl = n * (L["marks"][(d, code)] - L["marks"][(dp, code)]) * 10 if n else 0.0
        Cpre = C * (1 + L["mmf"][d] * cal / 365) + pnl
        g = (Vs + Gs + Cpre - Lp) / nav_prev - 1
        fee, newp = 0.0, {}
        for k in CLASSES:
            fu = price[k] * AMC[k] * cal / 365
            fee += units[k] * fu / 100
            newp[k] = price[k] * (1 + g) - fu
            xd = L["cls"][(d, k)]["xd_distribution_gbx"]
            if xd:
                newp[k] -= float(xd)
                Lp += units[k] * float(xd) / 100
        paid = 0.0
        if d in (dt.date(2025, 11, 28), dt.date(2026, 5, 29)):
            paid, Lp = Lp, 0.0
        price = newp
        flow = 0.0
        for k in CLASSES:
            u_prev = float(L["cls"][(dp, k)]["units_in_issue"])
            du = float(L["cls"][(d, k)]["units_in_issue"]) - u_prev
            dd_ = units[k] * du / u_prev
            units[k] += dd_
            flow += dd_ * price[k] / 100
        C = Cpre + flow - fee - paid
        nav = Vs + Gs + C - Lp
        nxt = days[j + 1] if j + 1 < len(days) else None
        if d.month in (3, 6, 9, 12) and (nxt is None or nxt.month != d.month):
            tv, tg = 0.47 * nav - Vs, 0.47 * nav - Gs
            Vs, Gs, C = Vs + tv, Gs + tg, C - tv - tg
        pub = round(price["B Acc"], 2)
        hist.append(pub)
        hi = max(hist[-63:])
        if order:
            active = order == "on"
            order = None
        dd = 1 - pub / hi
        if not active and dd > trig:
            order = "on"
        elif active and dd <= rest:
            order = "off"
        newcode = held_code(d)
        target = 0
        if active:
            target = int(round((0.40 * nav - Vs - Gs) / (L["marks"][(d, newcode)] * 10)))
        elif change == "E":
            target = int(round(C / (L["marks"][(d, newcode)] * 10)))
        cost = 0.0
        if n and code != newcode:
            cost += 2 * abs(n) * L["comm"]
            code = newcode
        if target != n:
            cost += abs(target - n) * L["comm"]
            n = target
            code = newcode if n else None
        C -= cost
        path.append(price["B Acc"])
        states.append("REDUCED" if active else "FULL")
        nav_prev = nav
    return path, states


def main_side(L, figs, problems):
    days = L["days"]
    k0, k1 = days.index(Y0), days.index(Y1)
    pub = [float(L["cls"][(days[j], "B Acc")]["price_gbx"]) for j in range(k0, k1 + 1)]
    base, _ = replay(L, None)
    err = max(abs(round(a, 2) - b) for a, b in zip(base, pub))
    if err > 0.011:
        problems.append("the replay with no change misses the published B Acc price by %.3fp" % err)
    rb = pub[-1] / pub[0] - 1
    bench = L["ix"][(Y1, "LKUKAS", "TR", "12:00")] / L["ix"][(Y0, "LKUKAS", "TR", "12:00")] - 1
    r10 = lambda x: int((x / 10 + 0.5) // 1 * 10)
    got = {"short_bp": r10((bench - rb) * 1e4)}
    for ch in "ABCDE":
        p, _ = replay(L, ch)
        got["bp_" + ch] = r10((p[-1] / p[0] - 1 - rb) * 1e4)
    order = sorted("ABCDE", key=lambda c: -got["bp_" + c])
    got["call"], got["runner_up"] = order[0], order[1]
    for k, v in got.items():
        if figs[k] != v:
            problems.append("%s: verifier %s, figures.json %s" % (k, v, figs[k]))
    return got


def quarter(d):
    if dt.date(2025, 10, 1) <= d <= dt.date(2025, 12, 31):
        return "Q1"
    if dt.date(2026, 1, 1) <= d <= dt.date(2026, 3, 31):
        return "Q2"
    if dt.date(2026, 4, 1) <= d <= dt.date(2026, 6, 30):
        return "Q3"
    if dt.date(2026, 7, 1) <= d <= dt.date(2026, 9, 30):
        return "Q4"


def asks(target, figs, problems):
    master = rows(target, "thornbury_security_master_20261016.csv")
    s2i = {r["sedol"]: r["isin"] for r in master}
    seg_now = {r["isin"]: r["market_segment"] for r in master}
    acc_h = {"THB-MRUKE-ASHC": "V", "THB-MRUKE-FENN": "G"}
    acc_n = {"NDS-0447118": "V", "NDS-0447126": "G"}
    pos = {}
    for r in rows(target, "holloway_safekeeping_positions_2025-26.csv"):
        pos[(dmy(r["Position Date"]), acc_h[r["Account"]], s2i[r["SEDOL"]])] = (int(r["Settled Holding"]),
                                                                                 float(r["Market Value (GBP)"]))
    for r in rows(target, "northcote_positions_daily_2026.csv"):
        pos[(ISO(r["as_of_date"]), acc_n[r["account_id"]], r["isin"])] = (int(r["quantity_settled"]),
                                                                          float(r["market_value_gbp"]))
    # A1: every dividend in the feed on the settled holding at its record date, plus the Penrose dividend the feed
    # no longer carries; Penrose's March final was never paid
    inc = {}
    feed = rows(target, "corporate_actions_feed_20261016.csv")
    for r in feed:
        if not r["event_type"].startswith("CASH DIVIDEND"):
            continue
        ex = ISO(r["ex_date"])
        q = quarter(ex)
        if q is None:
            continue
        rd = ISO(r["record_date"])
        for tag in "VG":
            h = pos.get((rd, tag, r["isin"]))
            if h:
                inc[(tag, q)] = inc.get((tag, q), 0.0) + round(h[0] * float(r["gross_rate"]) / 100, 2)
    feed_isins = {r["isin"] for r in feed}
    for r in rows(target, "holloway_income_entitlements_2025-26.csv"):
        isin = s2i[r["SEDOL"]]
        q = quarter(dmy(r["Ex Date"]))
        if isin in feed_isins or q is None or r["Status"] != "PAID":
            continue
        inc[(acc_h[r["Account"]], q)] = inc.get((acc_h[r["Account"]], q), 0.0) + float(r["Gross Amount (GBP)"])
    for (tag, q), v in inc.items():
        if figs["inc_%s_%s" % (tag, q)] != int(round(v / 1000) * 1000):
            problems.append("income %s %s: verifier %.0f, figures.json %s" % (tag, q, v, figs["inc_%s_%s" % (tag, q)]))
    # A2: trade dates two UK dealing days before settlement; trades open at the change of custodian dated by the list
    def back(d, n=2):
        while n:
            d -= dt.timedelta(days=1)
            if d.weekday() < 5 and d not in UK_HOLIDAYS:
                n -= 1
        return d
    cost = {}
    for r in rows(target, "holloway_settled_transactions_2025-26.csv"):
        if r["Transaction Type"] not in ("PURCHASE", "SALE"):
            continue
        q = quarter(back(dmy(r["Settlement Date"])))
        if q:
            k = (acc_h[r["Account"]], q)
            cost[k] = cost.get(k, 0.0) + float(r["Commission (GBP)"]) + float(r["Stamp Duty (GBP)"])
    open_ = {}
    for r in rows(target, "holloway_open_trades_31mar2026.csv"):
        key = (acc_h[r["Account"]], s2i[r["SEDOL"]], int(r["Quantity"]), r["Consideration (GBP)"])
        open_[key] = dmy(r["Trade Date"])
    for r in rows(target, "northcote_custody_statement_2026.csv"):
        if r["transaction_type"] not in ("BUY", "SELL"):
            continue
        tag = acc_n[r["account_id"]]
        key = (tag, r["isin"], abs(int(r["quantity"])), r["gross_amount_gbp"])
        td = open_.pop(key, None) or back(ISO(r["value_date"]))
        q = quarter(td)
        if q:
            cost[(tag, q)] = cost.get((tag, q), 0.0) + float(r["commission_gbp"]) + float(r["sdrt_gbp"])
    if open_:
        problems.append("%d open trades not found at Northcote" % len(open_))
    for (tag, q), v in cost.items():
        if figs["cost_%s_%s" % (tag, q)] != int(round(v / 100) * 100):
            problems.append("costs %s %s: verifier %.0f, figures.json %s" % (tag, q, v, figs["cost_%s_%s" % (tag, q)]))
    # A3: AIM status as at each quarter-end, from today's segment and the listing transfers
    moved = {r["isin"]: ISO(r["effective_date"]) for r in feed if r["event_type"] == "LISTING TRANSFER"}
    for q, qe in (("Q1", dt.date(2025, 12, 31)), ("Q2", dt.date(2026, 3, 31)), ("Q3", dt.date(2026, 6, 30)),
                  ("Q4", dt.date(2026, 9, 30))):
        tot = aim = 0.0
        n = 0
        for (d, tag, isin), (h, mv) in pos.items():
            if d != qe or tag != "G":
                continue
            tot += mv
            seg = seg_now[isin]
            if isin in moved and qe < moved[isin]:
                seg = "AIM"
            if seg == "AIM":
                aim += mv
                n += 1
        if figs["aim_n_" + q] != n or abs(figs["aim_pct_" + q] - round(aim / tot * 100, 1)) > 1e-9:
            problems.append("AIM %s: verifier %d, %.2f%%; figures.json %s, %s" % (q, n, aim / tot * 100,
                                                                               figs["aim_n_" + q], figs["aim_pct_" + q]))


def run(target, Fg=None):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    problems = []
    L = load(target)
    main_side(L, figs, problems)
    asks(target, figs, problems)
    print("verify: %s" % ("PASS, every graded figure recomputed from target/" if not problems else "FAIL"))
    for p in problems:
        print("   ", p)
    return not problems


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    sys.exit(0 if run(t) else 1)

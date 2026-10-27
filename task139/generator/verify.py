"""An independent recomputation of every graded figure from target/ alone, written apart from golden.py and asks.py
(pandas, its own joins and its own refund and remittance logic), compared with generator/figures.json.

    python3 task139/generator/verify.py
"""
import datetime as dt
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
VAL = pd.Timestamp("2026-09-30")
RESULTS = []


def check(name, mine, theirs, tol=0.5):
    good = (mine == theirs) if isinstance(theirs, str) else abs(float(mine) - float(theirs)) <= tol
    RESULTS.append(good)
    print("%-4s %-58s %s %s" % ("OK" if good else "DIFF", name, mine, "" if good else "(figures.json %s)" % theirs))


def months_later(ts, m):
    y, mo = ts.year + (ts.month - 1 + m) // 12, (ts.month - 1 + m) % 12 + 1
    last = pd.Timestamp(y, mo, 1).days_in_month
    return pd.Timestamp(y, mo, min(ts.day, last))


def main():
    fj = json.load(open(os.path.join(HERE, "figures.json")))
    reg = pd.read_csv(os.path.join(T, "drive_plus_contract_register.csv"), dtype=str).fillna("")
    reg["sale"] = pd.to_datetime(reg["sale_date"])
    reg["o0"] = reg["odometer_at_sale"].astype(int)
    reg["price"] = reg["contract_price"].astype(float)
    xw = pd.read_csv(os.path.join(T, "contract_number_crosswalk_2024.csv"), dtype=str)
    old2new = dict(zip(xw.old_contract_number, xw.new_contract_number))
    vin2fl = dict(zip(reg.loc[reg.channel == "FARELINE", "vin"], reg.loc[reg.channel == "FARELINE", "contract_number"]))

    def resolve(s):
        return s.map(lambda x: old2new.get(x) if x.startswith("DP-") else (x if x.startswith("CV") else vin2fl.get(x)))

    cl = pd.read_csv(os.path.join(T, "claim_lines_2019-01_to_2026-09.csv"), dtype=str)
    cl["amt"] = cl.amount.astype(float)
    cl = cl[cl.line_type != "GOODWILL"]
    cl["k"] = resolve(cl.contract_number)
    claims = cl.groupby("claim_number").agg(k=("k", "first"), odo=("repair_odometer", "first"), net=("amt", "sum"))
    claims["odo"] = claims.odo.astype(int)
    rd = pd.read_csv(os.path.join(T, "odometer_readings_2019-01_to_2026-09.csv"), dtype=str)
    rd["k"] = resolve(rd.reference)
    rd = rd.dropna(subset=["k"])
    rd["d"] = pd.to_datetime(rd.reading_date)
    rd["o"] = rd.odometer.astype(int)
    rd = rd.drop_duplicates(["k", "d", "o"]).sort_values(["k", "d", "o"])
    by_k = {k: g for k, g in rd.groupby("k")}

    # miles under cover by 10,000-mile odometer band
    W = 10000
    nb = 21
    miles = np.zeros(nb)
    for r in reg.itertuples():
        end = min(months_later(r.sale, 60), VAL)
        lim = r.o0 + 75000
        g = by_k.get(r.contract_number)
        xs = [r.o0]
        if g is not None:
            gg = g[(g.d >= r.sale) & (g.d <= end)]
            xs += list(gg.o)
        xs = np.minimum(np.array(xs, float), lim)
        for a, b in zip(xs[:-1], xs[1:]):
            if b <= a:
                continue
            for j in range(int(a // W), min(int(np.ceil(b / W)), nb)):
                lo, hi = j * W, (j + 1) * W
                miles[j] += max(0.0, min(hi, b) - max(lo, a))
    cost = np.zeros(nb)
    for o, n in zip(claims.odo, claims.net):
        cost[min(o // W, nb - 1)] += n
    cpm = np.divide(cost, miles, out=np.zeros(nb), where=miles > 0)
    check("cost per 1,000 miles under 70,000 (USD)", round(cost[:7].sum() / miles[:7].sum() * 1000, 1),
          fj["cpm_per_1000.under_70000_usd"], 0.05)

    # each 2026 Fareline contract: odometer at sale, annual mileage from its feed, cover to 75,000 miles or 60 months
    fl = reg[reg.channel == "FARELINE"]
    lifes, prices, rates, o0s = [], [], [], []
    for r in fl.itertuples():
        g = by_k.get(r.contract_number)
        if g is None:
            continue
        g = g[g.d > r.sale]
        if g.empty:
            continue
        last = g.iloc[-1]
        rate = (last.o - r.o0) / (last.d - r.sale).days * 365.25
        top = r.o0 + min(75000, rate * 5)
        life = 0.0
        for j in range(nb):
            seg = max(0.0, min((j + 1) * W, top) - max(j * W, r.o0))
            life += seg * cpm[j]
        lifes.append(life)
        prices.append(r.price)
        rates.append(rate)
        o0s.append(r.o0)
    lr = 100 * np.mean(lifes) / np.mean(prices)
    r5 = lambda x: int(5 * round(x / 5.0))
    check("2026 Fareline contracts with a feed reading", len(lifes), fj["fareline.contracts_2026"], 0)
    check("lifetime loss ratio at current price, nearest 5", r5(lr), fj["lr.current_price_pct_nearest_5"], 0)
    check("lifetime loss ratio surcharged, nearest 5", r5(lr / 1.4), fj["lr.surcharged_price_pct_nearest_5"], 0)
    check("lifetime loss ratio at current price (one decimal)", round(lr, 1), fj["lr.current_price_pct"], 0.05)
    check("claims cost over the cover, nearest 100", int(round(np.mean(lifes), -2)), fj["lifetime.claims_cost_usd_nearest_100"], 0)
    check("average price, nearest 10", int(round(np.mean(prices), -1)), fj["lifetime.average_price_usd_nearest_10"], 0)
    check("annual mileage, nearest 1,000", int(round(np.mean(rates), -3)), fj["fareline.annual_miles_nearest_1000"], 0)
    check("odometer at sale, nearest 1,000", int(round(np.mean(o0s), -3)), fj["fareline.odometer_at_sale_nearest_1000"], 0)
    elect = ("renew at current rates" if lr <= 70 else
             "renew with the maximum high-use surcharge" if lr / 1.4 <= 70 else "lapse")
    check("election", elect, fj["call.election"])

    # ask A: the first request received cancels; a lienholder's request is the contract on that VIN showing it
    cr = pd.read_csv(os.path.join(T, "cancellation_requests_2025-2026.csv"), dtype=str).fillna("")
    cr["d"] = pd.to_datetime(cr.received_date)
    cr = cr.sort_values(["d", "request_id"])
    rv = reg.set_index("contract_number")
    vl = {(v, l): k for k, v, l in zip(reg.contract_number, reg.vin, reg.lienholder) if l}
    cr["k"] = [c if c else vl.get((v, l), "") for c, v, l in zip(cr.contract_number, cr.vin, cr.lienholder)]
    cr = cr[cr.k != ""]
    first = cr.drop_duplicates("k", keep="first")
    paid = claims.reset_index().merge(cl.groupby("claim_number").repair_order_date.first().reset_index(), on="claim_number")
    paid["d"] = pd.to_datetime(paid.repair_order_date)
    claim_dates = paid.groupby("k").d.min()
    out = {}
    for r in first.itertuples():
        q = "%dQ%d" % (r.d.year, (r.d.month - 1) // 3 + 1)
        c = rv.loc[r.k]
        if c.channel == "FARELINE":
            continue
        if r.odometer_stated:
            odo = int(r.odometer_stated)
        else:
            g = by_k.get(r.k)
            g = g[g.d <= r.d] if g is not None else None
            odo = int(g.o.max()) if g is not None and not g.empty else c.o0
        days = (r.d - c.sale).days
        claimed = r.k in claim_dates.index and claim_dates[r.k] <= r.d
        if days <= 30 and not claimed:
            amt = c.price
        else:
            amt = max(0.0, c.price * (1 - max(days / 1826, max(odo - c.o0, 0) / 75000)) - 50)
        o = out.setdefault(q, [0, 0.0, 0.0])
        o[0] += 1
        o[1] += amt
        o[2] += amt if c.lienholder else 0.0
    for q in ("2026Q1", "2026Q2", "2026Q3"):
        check("ask A %s contracts cancelled" % q, out[q][0], fj["askA.%s.contracts_cancelled" % q], 0)
        check("ask A %s refunds owed (USD)" % q, round(out[q][1]), fj["askA.%s.refunds_usd" % q], 0.5)
        check("ask A %s refunds to lienholders (USD)" % q, round(out[q][2]), fj["askA.%s.refunds_to_lienholders_usd" % q], 0.5)

    # ask B: premium remitted on the bordereaux, less dealer-month payments the bank returned
    xl = pd.ExcelFile(os.path.join(T, "dealer_remittance_bordereaux_2025.xlsx"))
    tr = xl.parse("Trinity Motor Group", dtype=str)
    tr = pd.DataFrame(dict(dealer=tr["Dealer"], k=tr["Contract No"], amt=tr["Remitted (USD)"].astype(float),
                           ref=tr["Payment ref"], month=pd.to_datetime(tr["Bordereau month"], format="%Y-%m")))
    bz = xl.parse("Brazos Auto Partners", dtype=str)
    bz = pd.DataFrame(dict(dealer=bz["Dealer code"], k=bz["Copperline contract"], amt=bz["Remit (cents)"].astype(int) / 100,
                           ref=bz["ACH reference"], month=pd.to_datetime(bz["Period"], format="%b %Y")))
    ind = xl.parse("Independent dealers", dtype=str)
    vs = {(v, s.strftime("%d/%m/%Y")): k for k, v, s in zip(reg.contract_number, reg.vin, reg.sale)}
    ind = pd.DataFrame(dict(dealer=ind["Dealer"], k=[vs.get((v, s)) for v, s in zip(ind["VIN"], ind["Date of sale"])],
                            amt=ind["Amount"].astype(float), ref=ind["Payment reference"],
                            month=pd.to_datetime(ind["Remittance month"], format="%m/%Y")))
    bx = pd.concat([tr, bz, ind], ignore_index=True)
    tot = bx.groupby(["dealer", "ref", "month"], as_index=False).amt.sum()
    dd = pd.read_csv(os.path.join(T, "dealer_directory.csv"), dtype=str)
    name2code = dict(zip(dd.dealer_name.str.upper(), dd.dealer_code))
    ret = pd.read_csv(os.path.join(T, "ach_returns_report_2025-2026.csv"), dtype=str)
    returned = set()
    for r in ret.itertuples():
        s = pd.Timestamp(r.settlement_date)
        m = tot[(tot.dealer == name2code[r.originator_name]) & (tot.month.dt.year == s.year) &
                (tot.month.dt.month == s.month) & ((tot.amt - float(r.amount)).abs() < 0.005)]
        returned |= set(m.ref)
    recv = bx[~bx.ref.isin(returned)].groupby("k").amt.sum()
    rt = reg[reg.channel != "FARELINE"].copy()
    rt["q"] = ["%dQ%d" % (s.year, (s.month - 1) // 3 + 1) for s in rt.sale]
    rt["recv"] = rt.contract_number.map(recv).fillna(0.0)
    for q in ("2025Q1", "2025Q2", "2025Q3", "2025Q4"):
        x = rt[rt.q == q]
        check("ask B %s premium received (USD)" % q, round(x.recv.sum()), fj["askB.%s.premium_received_usd" % q], 0.5)
        check("ask B %s premium outstanding (USD)" % q, round(x.price.sum() - x.recv.sum()),
              fj["askB.%s.premium_outstanding_usd" % q], 0.5)
    print("verify: %d of %d" % (sum(RESULTS), len(RESULTS)))
    sys.exit(0 if all(RESULTS) else 1)


if __name__ == "__main__":
    main()

"""An independent verifier: pandas over target/ only, written apart from analysis.py, recomputing the call, every
graded figure and both asks, and comparing them with figures.json.

    python3 task306/generator/verify.py
"""
import json
import math
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
BAD = []


def check(name, cond, detail=""):
    print(("ok    " if cond else "FAIL  ") + name + ("" if cond else "   " + str(detail)))
    if not cond:
        BAD.append(name)


def london(ts):
    t = pd.to_datetime(ts, utc=True)
    return t.dt.tz_convert("Europe/London").dt.date


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    master = pd.read_csv(os.path.join(T, "wealdmoor_security_master_2026-11-30.csv"), dtype=str).fillna("")
    band = dict(zip(master["sedol"], master["index_band"].map({"FTSE 100": "L", "FTSE 250": "M", "FTSE SmallCap": "S"})))
    cons = {}
    for s, note in zip(master["sedol"], master["corporate_action_note"]):
        m = re.search(r"(\d\d)/(\d\d)/(\d{4})", note)
        if m:
            cons[s] = pd.Timestamp(int(m.group(3)), int(m.group(2)), int(m.group(1))).date()
    mk = pd.read_parquet(os.path.join(T, "lse_daily_market_data_2025-2026.parquet"))
    mk["trade_date"] = pd.to_datetime(mk.trade_date).dt.date
    mk = mk.sort_values(["sedol", "trade_date"])
    mk["value"] = mk.close_gbx / 100.0 * mk.volume_shares
    mk["ret"] = np.log(mk.close_gbx / mk.groupby("sedol").close_gbx.shift(1))
    mk.loc[[cons.get(s) == d for s, d in zip(mk.sedol, mk.trade_date)], "ret"] = np.nan
    g = mk.groupby("sedol")
    mk["adv20"] = g.value.transform(lambda x: x.shift(1).rolling(20, min_periods=20).mean())
    mk["vol60"] = g.ret.transform(lambda x: x.shift(1).rolling(60, min_periods=10).std()) * 1e4
    look = mk.set_index(["sedol", "trade_date"])[["adv20", "vol60"]]

    od = pd.read_csv(os.path.join(T, "oms_orders_2025-2026.csv"), dtype={"order_id": str})
    fl = pd.read_csv(os.path.join(T, "oms_fills_2025-2026.csv"), dtype={"order_id": str})
    fl = fl.drop_duplicates("exec_id")
    fl["px"] = np.where(fl.price_unit == "GBP", fl.fill_price * 100.0, fl.fill_price)
    od["day"] = london(od.created_utc)
    filled = fl.groupby("order_id").fill_qty.sum()
    od["filled"] = od.order_id.map(filled).fillna(0).astype(int)
    term = od[od.status == "TERMINATED"].copy()
    term["left"] = term.order_qty - term.filled
    rec = od[od.source == "BACKUP-RECOVERY"]
    key = ["account_code", "sedol", "side", "day"]
    mm = rec.merge(term[key + ["left", "order_id"]].rename(columns={"order_id": "orig"}), left_on=key + ["order_qty"],
                   right_on=key + ["left"], how="left")
    parent = dict(zip(mm.order_id, mm.orig))
    fl["oid"] = [parent.get(o) if isinstance(parent.get(o), str) else o for o in fl.order_id]
    fl["pv"] = fl.fill_qty * fl.px
    agg = fl.groupby("oid").agg(q=("fill_qty", "sum"), pv=("pv", "sum")).reset_index()
    ex = agg.merge(od, left_on="oid", right_on="order_id")
    ex["avg"] = ex.pv / ex.q
    ex["sgn"] = np.where(ex.side == "BUY", 1.0, -1.0)
    ex["sf"] = ex.sgn * (ex.avg - ex.arrival_mid_gbx) / ex.arrival_mid_gbx * 1e4
    ex["value"] = ex.q * ex.arrival_mid_gbx / 100.0
    lv = look.reindex(list(zip(ex.sedol, ex.day)))
    ex["part"] = ex.value.values / lv.adv20.values
    ex["vol"] = lv.vol60.values
    ex["band"] = ex.sedol.map(band)
    X = np.column_stack([(ex.band == b).astype(float) for b in "LMS"] + [ex.vol * np.sqrt(ex.part)])
    coef, *_ = np.linalg.lstsq(X, ex.sf.values, rcond=None)
    check("the fitted impact coefficient sits near the square-root law's 0.85", 0.75 < coef[3] < 0.95, coef)

    summ = pd.read_excel(os.path.join(T, "research_backtests_2027_candidates.xlsx"), sheet_name="Summary")
    alpha = dict(zip(summ["Strategy code"], summ["Annualised gross alpha, 2015 to 2026"].astype(str).str.rstrip("%").astype(float)
                     / 100))
    tr = pd.read_csv(os.path.join(T, "backtest_rebalance_trades_2025-2026.csv"))
    tr["d"] = pd.to_datetime(tr.rebalance_date).dt.date
    tr = tr[(tr.d >= pd.Timestamp(2025, 12, 1).date()) & (tr.d <= pd.Timestamp(2026, 11, 30).date())]
    tr["sedol"] = tr["isin"].map(dict(zip(master["isin"], master["sedol"])))
    lt = look.reindex(list(zip(tr.sedol, tr.d)))
    v = tr.traded_weight.abs() * 400e6
    p = v.values / lt.adv20.values
    a = np.array([coef["LMS".index(band[s])] for s in tr.sedol])
    tr["cost"] = v.values * (a + coef[3] * lt.vol60.values * np.sqrt(p)) / 1e4
    cost = tr.groupby("strategy_code").cost.sum()
    for k in ("SCM", "MCV", "LCQ"):
        net = alpha[k] * 400e6 - cost[k]
        check("%s alpha kept GBP %dm" % (k, fig["candidates"][k]["net_gbp_m"]),
              int(round(net / 1e6)) == fig["candidates"][k]["net_gbp_m"], round(net / 1e6, 3))
        check("%s gross GBP %dm" % (k, fig["candidates"][k]["gross_gbp_m"]),
              int(round(alpha[k] * 400)) == fig["candidates"][k]["gross_gbp_m"])
    nets = {k: alpha[k] * 400e6 - cost[k] for k in ("SCM", "MCV", "LCQ")}
    order = sorted(nets, key=lambda k: -nets[k])
    check("the call and the runner-up", order[0] == fig["call"] and order[1] == fig["runner_up"], order)

    reg = pd.read_csv(os.path.join(T, "trading_account_register.csv"), dtype=str).fillna("")
    live = ["UK Equity Income", "UK Mid Cap Growth", "UK Smaller Companies", "UK Dynamic"]

    def owner(acc, d):
        for _i, r in reg[reg.account_code == acc].iterrows():
            if pd.Timestamp(r.opened).date() <= d and (r.closed == "" or d <= pd.Timestamp(r.closed).date()):
                return r.account_name
        return None
    al = pd.read_csv(os.path.join(T, "oms_block_allocations_2025-2026.csv"), dtype={"block_order_id": str})
    blk = ex[ex.order_id.isin(set(al.block_order_id))].merge(al, left_on="order_id", right_on="block_order_id")
    blk["account_code"] = blk["account_code_y"]
    blk["value"] = blk.allocated_qty * blk.arrival_mid_gbx / 100.0
    blk["pv"] = blk.allocated_qty * blk.avg
    keep = ex[~ex.order_id.isin(set(al.block_order_id))]
    ex = pd.concat([keep, blk[keep.columns]], ignore_index=True)
    e26 = ex[[d.year == 2026 for d in ex.day]].copy()
    e26["who"] = [owner(a, d) for a, d in zip(e26.account_code, e26.day)]
    e26 = e26[e26.who.isin(live)]
    e26["q"] = [(d.month - 1) // 3 + 1 for d in e26.day]
    e26["h"] = [1 if d.month <= 6 else 2 for d in e26.day]
    sf = e26.groupby(["who", "q"]).apply(lambda x: (x.sf * x.value).sum() / x.value.sum(), include_groups=False)
    tv = e26.groupby(["who", "h"]).pv.sum() / 100.0
    bad_a = [k for k in fig["ask_shortfall_bps"] if round(float(sf[(k.rsplit(" ", 1)[0], int(k[-1]))]), 1)
             != fig["ask_shortfall_bps"][k]]
    bad_b = [k for k in fig["ask_traded_gbp_m"] if int(round(tv[(k.rsplit(" ", 1)[0], int(k[-1]))] / 1e6))
             != fig["ask_traded_gbp_m"][k]]
    check("ask A: every quarter's shortfall recomputes", not bad_a, bad_a)
    check("ask B: every half's traded value recomputes", not bad_b, bad_b)
    print("verify:", "PASS" if not BAD else "FAIL (%d)" % len(BAD))
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()

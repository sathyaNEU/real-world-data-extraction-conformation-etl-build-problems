"""Independent verifier: reads only target.zip and figures.json and recomputes every graded figure its own way.

    python3 task302/generator/verify.py task302/target.zip
"""
import datetime as dt
import io
import json
import os
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BAD = []


def say(name, ok, info=""):
    print(("ok   " if ok else "FAIL ") + name + ((" :: " + info) if info else ""))
    if not ok:
        BAD.append(name)


def read(z, name, **kw):
    b = io.BytesIO(z.read(name))
    return pd.read_parquet(b) if name.endswith(".parquet") else pd.read_csv(b, **kw)


def main(zpath):
    del BAD[:]
    F = json.load(open(os.path.join(HERE, "figures.json")))
    z = zipfile.ZipFile(zpath)
    ln = read(z, "lines.csv")
    codes = read(z, "till_item_codes.csv", dtype={"item_code": str})
    sales = read(z, "pos_daily_sales_2024-07_2026-06.parquet")
    stock = read(z, "stock_positions_2024-07_2026-06.csv")
    stores = read(z, "stores.csv")
    d0, d1, base = pd.Timestamp("2024-07-01"), pd.Timestamp("2026-06-30"), pd.Timestamp("2025-07-01")
    days = pd.date_range(d0, d1)
    nd = len(days)
    a2i = {a: i for i, a in enumerate(ln.article)}
    s2i = {s: i for i, s in enumerate(stores.store_no)}
    sales["i"] = sales.item_code.map(dict(zip(codes.item_code, codes.article))).map(a2i)
    sales["s"] = sales.store_no.map(s2i)
    sales["d"] = (pd.to_datetime(sales.trade_date) - d0).dt.days
    U = np.zeros((len(stores), len(ln), nd))
    np.add.at(U, (sales.s.values, sales.i.values.astype(int), sales.d.values), sales.units.values)
    shut = np.ones((len(stores), nd), bool)
    shut[sales.s.values, sales.d.values] = False
    on = np.zeros((len(stores), len(ln), nd), int)
    on[stock.store_no.map(s2i).values, stock.article.map(a2i).values,
       (pd.to_datetime(stock.date) - d0).dt.days.values] = stock.on_hand_open.values
    out = (on == 0) & ~shut[:, None, :]
    b0 = (base - d0).days
    add = {}
    for cat in ["Bottled water", "Infant formula", "Dry pet food", "Gluten-free bakery"]:
        k = (ln.category == cat).values
        u, o = U[:, k, :], out[:, k, :]
        price = ln.shelf_price_fy2026.values[k][None, :, None]
        say("out-of-stock line-days %s" % cat, int(o[:, :, b0:].sum()) == F["oos_line_days"][cat],
            "%d" % int(o[:, :, b0:].sum()))
        # the fortnight after a restock, and days another line of the category is out
        back = np.zeros_like(o)
        ends = o[:, :, :-1] & ~o[:, :, 1:]
        for j in range(1, 15):
            back[:, :, j:] |= np.pad(ends, ((0, 0), (0, 0), (0, 1)))[:, :, :-j]
        back &= ~o
        others = (o.sum(axis=1, keepdims=True) - o) > 0
        clean = (~o & ~back & ~others & ~shut[:, None, :]).astype(float)
        lev = np.zeros_like(u)
        for half in (28, 56):
            num, den = np.zeros_like(u), np.zeros_like(u)
            for j in range(7, half + 1, 7):
                num[:, :, j:] += (u * clean)[:, :, :-j]
                den[:, :, j:] += clean[:, :, :-j]
                num[:, :, :-j] += (u * clean)[:, :, j:]
                den[:, :, :-j] += clean[:, :, j:]
            this = num / np.maximum(den, 1)
            if half == 28:
                lev, den28 = this, den
            else:
                lev = np.where(den28 < 2, this, lev)
        onshelf = ~o & ~shut[:, None, :]
        lost = (lev * o * price)[:, :, b0:].sum()
        back_sales = ((u - lev) * onshelf * (others | back) * price)[:, :, b0:].sum()
        add[cat] = 0.5 * (lost - back_sales)
    win = max(add, key=add.get)
    say("call", win == F["call_category"] and int(round(add[win] / 1e4) * 1e4) == F["call_add"],
        "%s %.0f" % (win, add[win]))
    k = (ln.category == win).values
    say("whole-shelf store-days", int(out[:, k, b0:].all(axis=1).sum()) == F["win_whole_shelf_store_days"],
        "%d" % int(out[:, k, b0:].all(axis=1).sum()))
    # ask A: the trial export's on_hand is the close from 2 February 2026
    t = read(z, "cereal_trial_stock_2025-11_2026-05.csv")
    t["date"] = pd.to_datetime(t.date)
    live = pd.Timestamp("2026-02-02")
    t = t.sort_values(["store_no", "article", "date"])
    for st, x in t.groupby("store_no"):
        rows = x.to_dict("records")
        bef = aft = 0
        prev = None
        for r_ in rows:
            if prev is not None and prev["article"] != r_["article"]:
                prev = None
            if r_["date"] < live:
                bef += r_["on_hand"] == 0
            else:
                close = prev["on_hand"] - prev["units_sold"] if prev["date"] < live else prev["on_hand"]
                aft += (close + r_["delivered"]) == 0
            prev = r_
        v = F["ask_trial"][str(st)]
        say("trial %d" % st, aft == v["after"] and round(100 * (aft / bef - 1), 1) == v["change_pct"],
            "%d after, %.1f per cent change" % (aft, 100 * (aft / bef - 1)))
    # ask B: opening at the half hour the tills' first sales start from
    s = read(z, "dc_trailer_stops_2025-26.csv")
    td = read(z, "store_trading_days_2025-26.csv")
    first = pd.to_datetime(td.trade_date + " " + td.first_sale)
    opened = dict(zip(zip(td.store_no, td.trade_date), first.dt.floor("30min")))
    s["a"] = pd.to_datetime(s.arrived)
    late = {}
    for no, a in zip(s.store_no, s.a):
        if a > opened[(no, a.strftime("%Y-%m-%d"))]:
            late[no] = late.get(no, 0) + 1
    region = dict(zip(stores.store_no, stores.island))
    by_region = {}
    for no, k in late.items():
        by_region[region[no]] = by_region.get(region[no], 0) + k
    for g, v in F["ask_late_stops"].items():
        say("late stops %s" % g, by_region.get(g, 0) == v, "%d" % by_region.get(g, 0))
    # ask C: a truck's pallets sit on every line it delivered under every dispatch advice it carried, so each dock
    # appointment counts once
    grn = read(z, "dc_goods_received_2025-26.csv")
    dock = read(z, "dc_dock_appointments_2025-26.csv")
    art_cat = dict(zip(ln.article, ln.category))
    ap = dict(zip(dock.delivery_ref, dock.appointment_no))
    tot, seen = {}, set()
    for _, r_ in grn.iterrows():
        a_ = ap[r_.delivery_ref]
        if a_ in seen:
            continue
        seen.add(a_)
        k = (art_cat[r_.article], str(r_.received)[:7])
        tot[k] = tot.get(k, 0) + int(r_.pallets)
    for c_, ms in F["ask_pallets"].items():
        for m, v in ms.items():
            say("pallets %s %s" % (c_, m), tot.get((c_, m), 0) == v, "%d" % tot.get((c_, m), 0))
    print("%d failures" % len(BAD))
    return len(BAD)


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1]) else 0)

"""Build the pack under target/: the world, Ridgeway's records, the ask files, the documents and the distractors."""
import os

import numpy as np
import pandas as pd

import asks as A
import docs as DC
import params as P
import postprocess
import records as RC
import stock
import world as WD

FILES = {
    "pos": "pos_daily_sales_2024-07_2026-06.parquet",
    "stock": "stock_positions_2024-07_2026-06.csv",
    "lines": "lines.csv",
    "codes": "till_item_codes.csv",
    "stores": "stores.csv",
    "plan": "store_ordering_2027.docx",
    "dictionary": "data_dictionary.docx",
    "trial": "cereal_trial_stock_2025-11_2026-05.csv",
    "stops": "dc_trailer_stops_2025-26.csv",
    "trading": "store_trading_days_2025-26.csv",
    "po": "dc_purchase_orders_2025-26.csv",
    "edi": "supplier_edi_messages_2025-26.csv",
    "grn": "dc_goods_received_2025-26.csv",
    "dock": "dc_dock_appointments_2025-26.csv",
    "space": "shelf_space_2026.xlsx",
    "hours": "store_ordering_hours_2025-26.csv",
}
PACK = list(FILES)
DISTRACTORS = ["space", "hours", "edi"]
CONTEXT = ["plan"]


def world():
    res, size, closed = WD.simulate(P.SEED_WORLD)
    rng = np.random.default_rng(P.SEED_STOCK + 11)
    res = RC.with_returns(res, closed, rng)
    pos = stock.positions(res, closed)
    assert stock.check(res, pos)
    ln, ch = RC.lines(np.random.default_rng(P.SEED_DOCS))
    R = dict(res=res, size=size, closed=closed, positions=pos, lines=ln, codes=ch, stores=RC.stores())
    R["pos"] = RC.pos(res, ln, ch)
    R["stock"] = RC.stock_file(pos, ln)
    # each ask file draws from its own stream; the first draw whose figures sit clear of their rounding edges, and
    # whose trial shares are nowhere near the contract's half under either reading, is the one the chain recorded
    for k in range(50):
        t = A.trial(np.random.default_rng(P.SEED_ASK + 100 + k))
        if trial_ok(t):
            R["trial"] = t
            break
    R["stops"] = A.trailer_stops(np.random.default_rng(P.SEED_ASK + 300), closed)
    R["trading"] = A.trading_days(np.random.default_rng(P.SEED_ASK + 400), closed, size)
    for k in range(50):
        po, edi, grn, dock = A.purchasing(np.random.default_rng(P.SEED_ASK + 200 + k), ln)
        if pallets_ok(po, grn, dock, ln):
            R["po"], R["edi"], R["grn"], R["dock"] = po, edi, grn, dock
            break
    assert "trial" in R and "po" in R
    return R


def edge(v, unit=0.1):
    return unit / 2 - abs(v - round(v / unit) * unit)


def trial_ok(t):
    t = t.copy()
    t["date"] = pd.to_datetime(t.date)
    b = t.date < A.TRIAL_LIVE
    for st in A.TRIAL_STORES:
        x, xb = t[t.store_no == st], b[t.store_no == st]
        gold = 100 * (1 - (x._opening[~xb] == 0).sum() / (x._opening[xb] == 0).sum())
        naive = 100 * (1 - (x.on_hand[~xb] == 0).sum() / (x.on_hand[xb] == 0).sum())
        if abs(gold - 50) < 4 or abs(naive - 50) < 4 or edge(gold) < 0.01 or abs(gold - naive) < 5:
            return False
    return True


def pallets_ok(po, grn, dock, ln):
    """Every category-month's pallets move when each dispatch advice or each receipt is taken once, and the supplier-day
    reading misses most of them: a truck carrying two orders' dispatch advices books its pallets under both."""
    cat = dict(zip(ln.article, ln.category))
    g = grn.assign(cat=grn.article.map(cat), m=pd.to_datetime(grn.received).dt.to_period("M").astype(str),
                   s=grn.po_no.map(dict(zip(po.po_no, po.supplier))),
                   ap=grn.delivery_ref.map(dict(zip(dock.delivery_ref, dock.appointment_no))))
    if g.ap.isna().any():
        return False
    gold = g.drop_duplicates("ap").groupby(["cat", "m"]).pallets.sum()
    if len(gold) != 36:
        return False
    for keys in ("delivery_ref", "grn_no"):
        if (g.drop_duplicates(keys).groupby(["cat", "m"]).pallets.sum() == gold).any():
            return False
    return int((g.drop_duplicates(["s", "received"]).groupby(["cat", "m"]).pallets.sum() == gold).sum()) <= 6


def distractors(R, rng):
    st = R["stores"]
    metres = {"Bottled water": (4.0, 8.0), "Infant formula": (1.2, 2.4), "Dry pet food": (6.0, 10.5),
              "Gluten-free bakery": (0.9, 2.1)}
    rows = []
    for no, size in zip(st.store_no, R["size"]):
        for cat, (lo, hi) in metres.items():
            m = round(float(np.clip(rng.uniform(lo, hi) * (0.8 + 0.3 * size), lo * 0.8, hi * 1.25)) * 2) / 2
            n_lines = int((R["lines"].category == cat).sum())
            rows.append((no, cat, m, int(n_lines * rng.uniform(1.6, 2.6))))
    space = pd.DataFrame(rows, columns=["store_no", "category", "shelf_metres", "facings"])
    weeks = pd.date_range("2025-07-06", "2026-06-28", freq="W-SUN")
    base = {"Bottled water": 2.4, "Infant formula": 0.3, "Dry pet food": 2.9, "Gluten-free bakery": 1.6}
    hrs = []
    for no, size in zip(st.store_no, R["size"]):
        for w in weeks:
            for cat, b in base.items():
                hrs.append((no, w.date(), cat, round(max(0.0, rng.normal(b * (0.7 + 0.4 * size), 0.35)) * 4) / 4))
    hours = pd.DataFrame(hrs, columns=["store_no", "week_ending", "category", "hours"])
    return space, hours


def build(target, R=None):
    os.makedirs(target, exist_ok=True)
    if R is None:
        R = world()
    f = lambda k: os.path.join(target, FILES[k])
    R["pos"].to_parquet(f("pos"), index=False)
    R["stock"].to_csv(f("stock"), index=False)
    R["lines"].to_csv(f("lines"), index=False)
    R["codes"].to_csv(f("codes"), index=False)
    R["stores"].to_csv(f("stores"), index=False)
    R["trial"].drop(columns=["_opening"]).to_csv(f("trial"), index=False)
    R["stops"].to_csv(f("stops"), index=False)
    R["trading"].to_csv(f("trading"), index=False)
    R["po"].to_csv(f("po"), index=False)
    R["edi"].to_csv(f("edi"), index=False)
    R["grn"].to_csv(f("grn"), index=False)
    R["dock"].to_csv(f("dock"), index=False)
    space, hours = distractors(R, np.random.default_rng(P.SEED_DOCS + 5))
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Planogram March 2026"
    ws.append(list(space.columns))
    for row in space.itertuples(index=False):
        ws.append(list(row))
    wb.properties.creator = "Space Planning"
    wb.save(f("space"))
    postprocess.scrub(f("space"), P.ORG, "2026-03-19")
    postprocess.finish_office(f("space"), "2026-03-02T21:10:00Z", "2026-03-19T03:25:00Z", P.ORG,
                              person="Space Planning")
    hours.to_csv(f("hours"), index=False)
    DC.plan(f("plan"))
    DC.dictionary(f("dictionary"))
    return R

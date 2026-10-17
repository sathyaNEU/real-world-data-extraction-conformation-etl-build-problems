"""Independent verifier for task264: reads only the shipped bundle and the golden workbook, recomputes the call, every
category's national change and format gaps, the panel's sales by format, each chain's continuous stores and each
category's promotion share on its own code path, and compares them with the golden.

    python3 task264/generator/verify.py task264/target"""
import os
import sys

import numpy as np
import pandas as pd

TOL = 1.5
FORMATS = ["supermarket", "neighbourhood", "convenience", "online"]


def load(target):
    f = lambda n: os.path.join(target, n)
    log = pd.read_csv(f("feed_delivery_log_ry2026.csv"), dtype=str)
    good = set(log.loc[log["status"] == "accepted", "load_id"])
    mv = pd.read_csv(f("gpi_movement_ry2026.csv"), dtype={"load_id": str, "store_id": str, "item_code": str,
                                                          "promo_code": str})
    mv = mv[mv["load_id"].isin(good)].copy()
    mv["item_code"] = mv["item_code"].str.zfill(14)
    items = pd.read_csv(f("gpi_item_master_2026.csv"), dtype=str)
    reg = pd.read_csv(f("panel_store_register.csv"), dtype=str)
    mv = mv.merge(items[["item_code", "category"]], on="item_code").merge(
        reg[["store_id", "chain_code", "format", "store_name", "postcode"]], on="store_id")
    start = pd.Timestamp("2025-12-06")
    mv["w"] = (pd.to_datetime(mv["week_ending"]) - start).dt.days // 7
    terms_w = {"supermarket": 59.6, "neighbourhood": 16.3, "convenience": 7.1, "online": 17.0}
    return dict(log=log, good=good, mv=mv, items=items, reg=reg, w=terms_w, target=target)


def tornqvist_geks(p, q):
    """p, q: dict product -> array of 52 (nan where unsold)."""
    keys = sorted(p)
    P = np.array([p[k] for k in keys])
    Q = np.array([q[k] for k in keys])
    n = P.shape[1]
    sold = Q > 0
    lnp = np.log(np.where(sold, P, 1.0))
    exp = np.where(sold, P * Q, 0.0)
    T = np.zeros((n, n))
    for s in range(n):
        for t in range(s + 1, n):
            both = sold[:, s] & sold[:, t]
            ws = exp[both, s] / exp[both, s].sum()
            wt = exp[both, t] / exp[both, t].sum()
            T[s, t] = np.sum((ws + wt) / 2 * (lnp[both, t] - lnp[both, s]))
            T[t, s] = -T[s, t]
    g = np.array([np.mean([T[0, s] + T[s, t] for s in range(n)]) for t in range(n)])
    idx = np.exp(g - g[0])
    return 100 * (idx[-4:].mean() / idx[:4].mean() - 1)


def changes(mv):
    out = {}
    agg = mv.groupby(["category", "format", "item_code", "chain_code", "w"])[["units", "sales_aud"]].sum()
    for (cat, fmt), d in agg.groupby(level=[0, 1]):
        p, q = {}, {}
        for (_, _, item, chain, w), r in d.iterrows():
            key = (item, chain)
            if key not in p:
                p[key] = np.full(52, np.nan)
                q[key] = np.zeros(52)
            p[key][w] = r["sales_aud"] / r["units"]
            q[key][w] = r["units"]
        out[(cat, fmt)] = tornqvist_geks(p, q)
    return out


def verdicts(ch, w):
    res = {}
    for cat in sorted({k[0] for k in ch}):
        nat = sum(w[f] * ch[(cat, f)] for f in FORMATS) / sum(w.values())
        gaps = {f: ch[(cat, f)] - nat for f in FORMATS}
        res[cat] = (nat, gaps, max(abs(g) for g in gaps.values()) <= TOL)
    return res


def takings(D):
    ss = pd.read_csv(os.path.join(D["target"], "store_weekly_sales_ry2026.csv"), dtype={"load_id": str, "store_id": str})
    ss = ss[ss["load_id"].isin(D["good"])]
    ss = ss.merge(D["reg"], on="store_id")
    d = pd.to_datetime(ss["week_ending"])
    d = d.where(d.dt.dayofweek == 5, d - pd.Timedelta(days=1))
    ss = ss.assign(we=d)
    last = pd.to_datetime(ss["last_week_ending"]).fillna(pd.Timestamp("2026-11-28"))
    ss = ss[(ss["we"] >= pd.to_datetime(ss["first_week_ending"])) & (ss["we"] <= last) &
            (ss["we"] >= pd.Timestamp("2025-12-06")) & (ss["we"] <= pd.Timestamp("2026-11-28"))]
    sw = ss.groupby(["chain_code", "format", "store_id", "we"])["sales_aud"].agg(["sum", "min", "max", "count"])
    repeated = sw.groupby(level=0).apply(lambda x: bool(((x["min"] == x["max"]) & (x["count"] > 1)).all()))
    sw["store_week"] = np.where(sw.index.get_level_values(0).map(repeated), sw["max"], sw["sum"])
    return (sw.groupby(level=1)["store_week"].sum() / 1e6).to_dict()


def continuity(D):
    mv = D["mv"]
    ch = pd.read_excel(os.path.join(D["target"], "partner_chains.xlsx"), sheet_name="Chains", dtype=str)
    start = {r.chain_code: max(0, -(-(pd.Timestamp(r.data_agreement_from) - pd.Timestamp("2025-12-06")).days // 7))
             for r in ch.itertuples()}
    site = mv["store_name"] + "/" + mv["postcode"]
    weeks = mv.assign(site=site).groupby(["chain_code", "site"])["w"].agg(lambda x: set(x))
    out = {}
    for (c, _), w in weeks.items():
        out[c] = out.get(c, 0) + int(set(range(start[c], 52)) <= w)
    return out


def promotions(D):
    mv = D["mv"]
    codes = pd.read_excel(os.path.join(D["target"], "partner_chains.xlsx"), sheet_name="Price codes", dtype=str)
    special = codes[~codes["meaning"].str.contains("clear|markdown|Clearance|override", case=False)]
    pairs = set(zip(special["chain_code"], special["code"]))
    code = mv["promo_code"].fillna("")
    on = pd.Series([(c, k) in pairs for c, k in zip(mv["chain_code"], code)], index=mv.index)
    # a code read before its listed in-use date carries no listed meaning: C2's PC rows before 2 August 2026 run at
    # every store of the chain at a cut price, the dictionary's catalogue special
    since = {(r.chain_code, r.code): pd.Timestamp(r.in_use_from) for r in codes.itertuples()}
    start = pd.to_datetime(mv["week_ending"]) - pd.Timedelta(days=6)
    early = pd.Series([start_ < since.get((c, k), pd.Timestamp("1900-01-01")) for c, k, start_ in
                       zip(mv["chain_code"], code, start)], index=mv.index)
    on = (on & ~early) | ((mv["chain_code"] == "C2") & (code == "PC") & early)
    g = mv.assign(d=mv["sales_aud"] * on).groupby("category")[["d", "sales_aud"]].sum()
    return (100 * g["d"] / g["sales_aud"]).to_dict()


def main(target):
    D = load(target)
    ch = changes(D["mv"])
    v = verdicts(ch, D["w"])
    golden = os.path.join(os.path.dirname(os.path.abspath(target)), "golden", "gpi_2027_structure.xlsx")
    gx = pd.read_excel(golden, sheet_name="Structure", header=3, nrows=18)
    gx = gx.set_index("Category")
    bad = 0
    r1 = lambda x: float("%.1f" % (x + (1e-9 if x >= 0 else -1e-9)))
    for cat, (nat, gaps, pubd) in v.items():
        row = gx.loc[cat]
        same = (row["Own sub-index in 2027"] == "Yes") == pubd and r1(nat) == row["National change (%)"] and all(
            r1(gaps[f]) == row["%s gap (pts)" % f.capitalize()] for f in FORMATS)
        bad += not same
        if not same:
            print("MISMATCH", cat, nat, gaps, pubd)
    n = sum(1 for x in v.values() if x[2])
    print("call: %d categories published" % n)
    tk = takings(D)
    pn = pd.read_excel(golden, sheet_name="Panel", header=1, nrows=4).set_index("Store format")
    for f in FORMATS:
        if r1(tk[f]) != pn.loc[f.capitalize()].iloc[0]:
            bad += 1
            print("MISMATCH takings", f, tk[f])
    cont = continuity(D)
    pc = pd.read_excel(golden, sheet_name="Panel", header=None)
    start = pc.index[pc[0] == "Chain"][0]
    for r in pc.iloc[start + 1:].itertuples(index=False):
        if cont.get(r[0]) != int(r[3]):
            bad += 1
            print("MISMATCH continuity", r[0], cont.get(r[0]), r[3])
    ps = promotions(D)
    for cat, val in ps.items():
        if r1(val) != gx.loc[cat]["Spending on promotion (%)"]:
            bad += 1
            print("MISMATCH promotion", cat, val)
    print("verify: %d mismatches" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

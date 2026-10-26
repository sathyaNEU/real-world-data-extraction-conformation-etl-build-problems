"""The independent verifier: reads only the shipped bundle (target/ and figures.json) and recomputes the call, the
critical components and every ask figure with its own code (vectorised house-years, an even-odd ray test for the
zone polygons, statsmodels' formula interface for the chosen model, pandas joins for the asks), then compares with
figures.json."""
import datetime as dt
import json
import os
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K    # noqa: E402

TOWNS = ["DOR", "BRK", "SAL"]


def half_up(x, n=0):
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP))


def inside(px, py, ring):
    ring = np.asarray(ring)
    x1, y1 = ring[:-1, 0], ring[:-1, 1]
    x2, y2 = ring[1:, 0], ring[1:, 1]
    res = np.zeros(len(px), bool)
    for a, b, c, e in zip(x1, y1, x2, y2):
        crosses = ((b > py) != (e > py))
        xint = a + (py - b) * (c - a) / np.where(e != b, e - b, 1e-12)
        res ^= crosses & (px < xint)
    return res


def run(task):
    T = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    out = []

    def ok(label, a, b):
        out.append((label, a == b, "%s | %s" % (a, b)))

    rd = lambda k: pd.read_csv(os.path.join(T, K.FILES[k]), dtype=str, keep_default_na=False)   # noqa: E731
    terms, claims, parcels, dw = rd("terms"), rd("claims"), rd("parcels"), rd("dwellings")
    # house-years, vectorised per term and year
    s = pd.to_datetime(terms["term_effective"])
    e = pd.to_datetime(terms["term_expiration"])
    cx = pd.to_datetime(terms["cancellation_effective"].where(terms["reinstatement_effective"] == ""), errors="coerce")
    e = e.where(cx.isna() | (cx > e), cx)
    rows = []
    for y in (2023, 2024, 2025):
        lo = s.clip(lower=pd.Timestamp(y, 1, 1))
        hi = e.clip(upper=pd.Timestamp(y + 1, 1, 1))
        days = (hi - lo).dt.days.clip(lower=0)
        rows.append(pd.DataFrame({"parcel_id": terms["parcel_id"], "year": y, "expo": days / (366.0 if y == 2024 else 365.0)}))
    ex = pd.concat(rows).groupby(["parcel_id", "year"], as_index=False)["expo"].sum()
    ex = ex[ex["expo"] > 0]
    wc = claims[claims["cause_code"].isin(["WTR-P", "WTR-A", "3110", "3120", "3130"]) &
                ~claims["claim_number"].str.contains(r"-R\d+$", regex=True)].copy()
    wc["year"] = wc["date_of_loss"].str[:4].astype(int)
    n = wc.groupby(["parcel_id", "year"]).size().rename("n").reset_index()
    d = ex.merge(n, on=["parcel_id", "year"], how="left").fillna({"n": 0})
    lastterm = terms.assign(tn=terms["term_number"].astype(int)).sort_values(["parcel_id", "tn"]).groupby("parcel_id").tail(1)
    found = lastterm.set_index("parcel_id")["foundation"]
    xy = parcels.set_index("parcel_id")[["x_coord_ft", "y_coord_ft"]].astype(float)
    g = json.load(open(os.path.join(T, K.FILES["zones"])))

    def zone(px, py):
        z = np.array([""] * len(px), dtype=object)
        for f in g["features"]:
            geom = f["geometry"]
            polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
            for p in polys:
                z[inside(px, py, p[0])] = f["properties"]["ZONE_ID"]
        return z
    bk = pd.DataFrame({"parcel_id": found.index})
    bk["found"] = found.values
    pxy = xy.loc[bk["parcel_id"]].values
    bk["zone"] = zone(pxy[:, 0], pxy[:, 1])
    d = d.merge(bk, on="parcel_id")
    # the townships' homes
    h = parcels[parcels["municipality_code"].isin(TOWNS) & (parcels["land_use_code"] == "R-SFD") &
                (parcels["homestead_farmstead"] == "H")]
    c1 = dw[dw["card_number"] == "1"].set_index("parcel_id")
    fmap = {"BSMT FULL": "B", "BSMT PART": "B", "SLAB": "S", "CRAWL": "C", "PIERS": "C"}
    hm = pd.DataFrame({"parcel_id": h["parcel_id"].values, "town": h["municipality_code"].values,
                       "found": [fmap[c1.loc[p, "foundation"]] for p in h["parcel_id"]]})
    hxy = h[["x_coord_ft", "y_coord_ft"]].astype(float).values
    hm["zone"] = zone(hxy[:, 0], hxy[:, 1])
    import statsmodels.api as sm
    import statsmodels.formula.api as smf

    def fitdev(formula, train, test):
        m = smf.glm(formula, data=train, family=sm.families.Poisson(), offset=np.log(train["expo"])).fit()
        mu = m.predict(test, offset=np.log(test["expo"]))
        y = test["n"].values
        t = np.where(y > 0, y * np.log(np.where(y > 0, y, 1) / mu), 0)
        return m, float(2 * np.sum(t - (y - mu)))
    tr, te = d[d["year"] < 2025], d[d["year"] == 2025]
    _, dev_z = fitdev("n ~ C(found) + C(zone)", tr, te)
    _, dev_f = fitdev("n ~ C(found)", tr, te)
    ok("deviance 2025 foundation and zone", half_up(dev_z, 1), fig["components"]["deviance_2025_chosen"])
    ok("deviance 2025 foundation alone", half_up(dev_f, 1), fig["components"]["deviance_2025_best_recorded_only"])
    m = smf.glm("n ~ C(found) + C(zone)", data=d, family=sm.families.Poisson(), offset=np.log(d["expo"])).fit()
    p = m.predict(hm, offset=np.zeros(len(hm))) * 1000
    town = p.groupby(hm["town"]).mean()
    for t in TOWNS:
        ok("frequency %s" % t, int(half_up(town[t])), fig["components"]["frequency_per_1000"][t])
        ok("Valley-zone homes %s" % t, int((hm[hm["town"] == t]["zone"] == "PZ-3").sum()),
           fig["components"]["valley_zone_homes"][t])
    best = min(TOWNS, key=lambda t: town[t])
    ok("call", best, fig["call"]["township"])
    ok("book frequency", int(half_up(1000 * d["n"].sum() / d["expo"].sum())), fig["context"]["book_frequency_per_1000"])
    # protection
    H = pd.DataFrame([dict(f["properties"], x=f["geometry"]["coordinates"][0], y=f["geometry"]["coordinates"][1])
                      for f in json.load(open(os.path.join(T, K.FILES["hydrants"])))["features"]])
    ft = rd("flowtests")
    ft["date"] = pd.to_datetime(ft["test_date"])
    old = ft[ft["date"] < pd.Timestamp(2024, 4, 1)].merge(H[H["FORMER_ID"] != ""][["FORMER_ID", "HYDRANT_ID"]],
                                                           left_on="hydrant_id", right_on="FORMER_ID")
    new = ft[ft["date"] >= pd.Timestamp(2024, 4, 1)].merge(H[["HYDRANT_ID"]], left_on="hydrant_id",
                                                            right_on="HYDRANT_ID")
    allt = pd.concat([old, new]).sort_values("date").groupby("HYDRANT_ID").tail(1)
    sp, rp, fl = allt["static_psi"].astype(float), allt["residual_psi"].astype(float), allt["flow_gpm"].astype(float)
    allt["q"] = fl * ((sp - 20) / (sp - rp)) ** 0.54
    good = H.merge(allt[["HYDRANT_ID", "q"]], on="HYDRANT_ID")
    good = good[(good["STATUS"] == "IN SERVICE") & (good["OWNER"] == "TCWA") & (good["q"] >= 500)]
    gx, gy = good["x"].values, good["y"].values

    def prot(px, py):
        res = np.zeros(len(px), bool)
        for i in range(0, len(px), 400):
            dx = px[i:i + 400, None] - gx[None, :]
            dy = py[i:i + 400, None] - gy[None, :]
            res[i:i + 400] = (dx * dx + dy * dy).min(1) <= 1000.0 ** 2
        return res
    hp = prot(hxy[:, 0], hxy[:, 1])
    for t in TOWNS:
        ok("protected %s" % t, int(hp[hm["town"].values == t].sum()), fig["asks"]["protected_homes"][t])
    # market value
    ap = rd("appeals")
    ap = ap[(ap["tax_year"] == "2026") & ap["decision"].isin(["REDUCED", "INCREASED", "SUSTAINED"])]
    val = h.set_index("parcel_id")["assessed_total"].astype(float)
    val.update(ap.set_index("parcel_id")["assessed_total_after"].astype(float))
    clr = rd("clr")
    c = float(clr[(clr["effective_from"] <= "2026-01-01") & (clr["effective_to"] >= "2026-01-01")]["common_level_ratio"].iloc[0])
    mv = (val / c).groupby(h.set_index("parcel_id")["municipality_code"]).sum()
    for t in TOWNS:
        ok("market %s" % t, half_up(mv[t] / 1e6, 1), fig["asks"]["market_value_musd"][t])
    # payments
    pm = rd("payments")
    pm["amount"] = pm["amount"].astype(float)
    pm["claim"] = pm["claim_number"].str.replace(r"-R\d+$", "", regex=True)
    base = wc.set_index("claim_number")
    pm = pm[pm["claim"].isin(base.index)]
    ind = pm[pm["transaction_type"].isin(["INDEMNITY", "VOID"])].groupby("claim")["amount"].sum()
    rec = pm[pm["transaction_type"] == "RECOVERY"].groupby("claim")["amount"].sum()
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(T, K.FILES["bordereau"]), read_only=True)
    bl = {}
    for sh in wb.sheetnames:
        for r in wb[sh].iter_rows(min_row=3, values_only=True):
            if r[0]:
                bl[r[0]] = (r[5], r[6])
    bdf = pd.DataFrame([(k, v[0], v[1]) for k, v in bl.items() if k in base.index], columns=["claim", "paid", "rec"])
    ind = ind.add(bdf.set_index("claim")["paid"], fill_value=0)
    rec = rec.add(-bdf.set_index("claim")["rec"], fill_value=0)
    net = ind.add(rec, fill_value=0)
    paid = ind[ind > 0.005]
    for y in (2023, 2024, 2025):
        ids = [k for k in paid.index if base.loc[k, "year"] == y]
        ok("payment %d" % y, int(half_up(net.loc[ids].mean())), fig["asks"]["water_payment_by_accident_year"][str(y)])
    # fire
    fc = claims[claims["cause_code"].isin(["FIR", "5110", "5120"]) & ~claims["claim_number"].str.contains(r"-R\d+$")]
    fc = fc[fc["date_of_loss"].str[:4].isin(["2023", "2024", "2025"])]
    bxy = xy.loc[bk["parcel_id"]].values
    bp = pd.Series(prot(bxy[:, 0], bxy[:, 1]), index=bk["parcel_id"].values)
    exh = d.groupby("parcel_id")["expo"].sum()
    nf = fc.groupby("parcel_id").size().reindex(exh.index).fillna(0)
    idx = bp[~bp].index.intersection(exh.index)
    ok("fire unprotected", half_up(1000 * nf.loc[idx].sum() / exh.loc[idx].sum(), 1), fig["asks"]["fire_per_1000"]["unprotected"])
    bad = [o for o in out if not o[1]]
    for label, good_, detail in out:
        print("%s  verify %s  [%s]" % ("PASS" if good_ else "FAIL", label, detail))
    print("verify: %d figures, %d differ" % (len(out), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)))

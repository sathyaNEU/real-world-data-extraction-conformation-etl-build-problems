"""Readers and the golden, run on the record tables exactly as shipped (generator side; verify.py has its own code)."""
import numpy as np
import pandas as pd
import statsmodels.api as sm
import warnings

warnings.filterwarnings("ignore")
NAME2KEY = {"Zaragoza Plaza": "ZAZ", "Ribarroja": "VLC", "Dos Hermanas": "SVQ", "San Fernando": "MAD",
            "El Prat": "BCN", "Basauri": "BIO"}
HEAVY_KG = 10.0


def dws_weight(dws, pick="first"):
    d = dws.sort_values(["barcode", "induct_local"])
    if pick == "first":
        s = d.groupby("barcode").weight_g.first()
    elif pick == "last":
        s = d.groupby("barcode").weight_g.last()
    else:
        s = d.groupby("barcode").weight_g.mean()
    return s / 1000.0


def crush_load(scans, weights, order="first"):
    """Weight scanned into each parcel's cage after it (kg), from the load scans and a per-barcode weight."""
    s = scans[scans.event == "LOAD"].sort_values("scan_utc")
    s = (s.groupby(["cage_label", "barcode"]).scan_utc.min() if order == "first"
         else s.groupby(["cage_label", "barcode"]).scan_utc.max()).reset_index()
    s["w"] = s.barcode.map(weights).fillna(0.0)
    s = s.sort_values(["cage_label", "scan_utc", "barcode"]).reset_index(drop=True)
    g = s.groupby("cage_label")
    s["load_above"] = g.w.transform("sum") - g.w.cumsum()
    s["heavy"] = (s.w >= HEAVY_KG).astype(int)
    s["heavy_above"] = g.heavy.transform("sum") - g.heavy.cumsum()
    rv = s.iloc[::-1]
    mx = rv.groupby("cage_label").w.cummax()
    s["max_above"] = (mx.groupby(rv.cage_label).shift(1)).reindex(s.index).fillna(0.0)
    n = s.groupby("cage_label").barcode.transform("size")
    s["pos"] = s.groupby("cage_label").cumcount()
    s["frac_after"] = (n - 1 - s.pos) / (n - 1).clip(lower=1)
    s["cage_kg"] = s.groupby("cage_label").w.transform("sum")
    s["cage_heavy"] = s.groupby("cage_label").heavy.transform("sum")
    return s.set_index("barcode")[["cage_label", "load_above", "heavy_above", "max_above", "frac_after", "cage_kg",
                                   "cage_heavy", "pos"]]


def base_table(rec, accounts, check_audits=False, notfound_as_ok=False, weight_pick="first", order="first"):
    a = rec["audits"]
    a = a if check_audits else a[a.audit_type == "ROUTINE"]
    ln = rec["lines"].merge(a[["audit_id", "cage_label", "hub", "build_date"]], on="audit_id")
    if notfound_as_ok:
        ln = ln.assign(condition=ln.condition.replace({"NOT FOUND": "OK"}))
    ln = ln[ln.condition.isin(["OK", "DAMAGED"])].copy()
    ln["dam"] = (ln.condition == "DAMAGED").astype(int)
    ln["hubk"] = ln.hub.map(NAME2KEY)
    wts = dws_weight(rec["dws"], weight_pick)
    dws1 = rec["dws"].drop_duplicates("barcode")[["barcode", "length_mm", "width_mm", "height_mm", "shape"]].rename(columns={"shape": "dshape"})
    ln = ln.merge(dws1, on="barcode", how="left").merge(rec["manifests"], on="barcode", how="left")
    ln["kg"] = ln.barcode.map(wts)
    acc = accounts.set_index("account")
    ln["sector"] = ln.account.map(acc.sector)
    cl = crush_load(rec["scans"], wts, order)
    ln = ln.join(cl.drop(columns=["cage_label"]), on="barcode")
    ln["lkg"] = np.log(ln.kg.clip(lower=0.05))
    ln["heavyp"] = (ln.kg >= HEAVY_KG).astype(int)
    ln["wband"] = pd.cut(ln.kg, [0, 0.5, 1, 2, 5, 10, 99], labels=False)
    return ln


def _X(t, extra=None):
    X = pd.DataFrame({"frag": (t.fragile == "Y").astype(float), "box": (t["dshape"] == "BOX").astype(float),
                      "bag": (t["dshape"] == "BAG").astype(float), "lkg": t.lkg, "nd": (t.service == "24H").astype(float),
                      "hv": t.heavyp.astype(float)})
    if extra is not None:
        for k, v in extra.items():
            X[k] = v
    return sm.add_constant(X, has_constant="add")


def oe(t, X, fam="bin"):
    f = sm.families.Binomial() if fam == "bin" else sm.families.Poisson()
    m = sm.GLM(t.dam.values, X.values.astype(float), family=f).fit()
    e = m.predict(X.values.astype(float))
    g = pd.DataFrame({"h": t.hubk.values, "o": t.dam.values, "e": e}).groupby("h").sum()
    n = t.groupby("hubk").size()
    return ((g.o - g.e) / n * 1e4), m


def cells_oe(t, keys):
    cell = t[keys].astype(str).agg("|".join, axis=1)
    r = t.groupby(cell).dam.transform("mean")
    g = pd.DataFrame({"h": t.hubk.values, "o": t.dam.values, "e": r.values}).groupby("h").sum()
    n = t.groupby("hubk").size()
    return (g.o - g.e) / n * 1e4


def readers(t, rec):
    out = {}
    out["first_look"] = t.groupby("hubk").dam.mean() * 1e4
    out["a_fields"] = cells_oe(t.assign(fr=t.fragile, sv=t.service), ["dshape", "wband", "fr", "sv"])
    out["e_literal"], _ = oe(t, _X(t))
    box = (t["dshape"] == "BOX").astype(float); bag = (t["dshape"] == "BAG").astype(float)
    ex = {"fill": t.groupby("cage_label").barcode.transform("size").astype(float), "box_lkg": box * t.lkg,
          "frag_box": (t.fragile == "Y") * box}
    ex["box_fill"] = box * ex["fill"]
    out["c_perrecord"], _ = oe(t, _X(t, ex))
    exb = dict(ex); exb.update({"fa": t.frac_after, "cw": t.cage_kg / 50, "ch": t.cage_heavy})
    exb.update({"box_fa": box * t.frac_after, "box_cw": box * t.cage_kg / 50, "box_ch": box * t.cage_heavy,
                "fa_cw": t.frac_after * t.cage_kg / 50})
    out["b_constructing"], _ = oe(t, _X(t, exb))
    pb = pd.cut(t.frac_after, [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01], labels=False)
    out["b_posbands"] = cells_oe(t.assign(pb=pb, fr=t.fragile), ["dshape", "wband", "fr", "pb"])
    top = t[(t.frac_after < 0.33) & (t.heavyp == 0)]
    out["b_topthird"] = top.groupby("hubk").dam.mean() * 1e4
    exd = {"ch": t.cage_heavy, "cw": t.cage_kg / 50, "box_ch": box * t.cage_heavy, "box_cw": box * t.cage_kg / 50,
           "bag_ch": bag * t.cage_heavy}
    out["d_mechanism"], _ = oe(t, _X(t, exd))
    # d2: names crush from stacking, orders the cage by scan, weighs with the sender's declared weight
    decl = rec["manifests"].set_index("barcode").declared_kg
    cl2 = crush_load(rec["scans"], decl, "first")
    la2 = t.barcode.map(cl2.load_above)
    out["d2_declared"], _ = oe(t, _X(t, {"f": la2 / 50, "box_f": box * la2 / 50, "bag_f": bag * la2 / 50}))
    out["d2_declared_band"] = cells_oe(t.assign(lb=pd.cut(la2, [-1, 20, 40, 60, 100, 1e4], labels=False), fr=t.fragile),
                                       ["dshape", "wband", "fr", "lb"])
    out.update(golden_family(t))
    return pd.DataFrame(out)


def golden_family(t, thresholds=(35, 45, 60, 75, 95)):
    box = (t["dshape"] == "BOX").astype(float); bag = (t["dshape"] == "BAG").astype(float); hv = t.heavyp.astype(float)
    out = {}
    for T in thresholds:
        out["g_cells_T%d" % T] = cells_oe(t.assign(ls=(t.load_above >= T).astype(int), fr=t.fragile),
                                          ["dshape", "wband", "fr", "ls"])
    ind = (t.load_above >= 60).astype(float)
    out["g_logit_ind"], _ = oe(t, _X(t, {"f": ind, "box_f": box * ind, "bag_f": bag * ind, "hv_f": hv * ind}))
    out["g_pois_ind"], _ = oe(t, _X(t, {"f": ind, "box_f": box * ind, "bag_f": bag * ind, "hv_f": hv * ind}), "pois")
    f = t.load_above / 50
    out["g_logit_lin"], _ = oe(t, _X(t, {"f": f, "box_f": box * f, "bag_f": bag * f, "hv_f": hv * f}))
    f = np.log1p(t.load_above)
    out["g_logit_log"], _ = oe(t, _X(t, {"f": f, "box_f": box * f, "bag_f": bag * f, "hv_f": hv * f}))
    f = t.heavy_above.astype(float)
    out["g_logit_cnt"], _ = oe(t, _X(t, {"f": f, "box_f": box * f, "bag_f": bag * f, "hv_f": hv * f}))
    f = t.max_above / 20
    out["g_logit_max"], _ = oe(t, _X(t, {"f": f, "box_f": box * f, "bag_f": bag * f, "hv_f": hv * f}))
    lb = pd.cut(t.load_above, [-1, 20, 40, 60, 100, 1e4], labels=False)
    out["g_cells_bands"] = cells_oe(t.assign(lb=lb, fr=t.fragile), ["dshape", "wband", "fr", "lb"])
    return out


def fits(t):
    """Deviance of each crush form, to show which the record's own fit supports."""
    box = (t["dshape"] == "BOX").astype(float); bag = (t["dshape"] == "BAG").astype(float); hv = t.heavyp.astype(float)
    res = {}
    forms = {"none": None, "ind60": (t.load_above >= 60).astype(float), "lin": t.load_above / 50,
             "log": np.log1p(t.load_above), "cnt": t.heavy_above.astype(float), "max": t.max_above / 20}
    for k, f in forms.items():
        ex = None if f is None else {"f": f, "box_f": box * f, "bag_f": bag * f, "hv_f": hv * f}
        _, m = oe(t, _X(t, ex))
        res[k] = round(float(m.deviance), 1)
    return res


def summarise(df):
    rows = []
    for c in df.columns:
        s = df[c].sort_values(ascending=False)
        lead = s.iloc[0] / s.iloc[1] if s.iloc[1] > 0 else float("inf")
        rows.append((c, s.index[0], round(float(s.iloc[0]), 1), s.index[1], round(float(s.iloc[1]), 1), round(float(lead), 2)))
    return pd.DataFrame(rows, columns=["reader", "pick", "top", "second", "second_val", "lead"])

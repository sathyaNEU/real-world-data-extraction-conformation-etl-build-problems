"""Readers and the golden family, run on the main-call record tables as shipped (generator side; verify.py has its
own code). Every figure is per 10,000 parcels inspected: observed minus expected by hub."""
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm

warnings.filterwarnings("ignore")
NAME2KEY = {"Zaragoza Plaza": "ZAZ", "Ribarroja": "VLC", "Dos Hermanas": "SVQ", "San Fernando": "MAD",
            "El Prat": "BCN", "Basauri": "BIO"}
HEAVY_KG = 10.0
BANDS = [-1, 20, 40, 60, 100, 1e5]


def dws_weight(dws, pick="first", key="exact"):
    d = dws.copy()
    if key == "norm":
        d["barcode"] = d.barcode.str.strip().str.upper()
    d = d.sort_values(["barcode", "induct_local"], kind="mergesort")
    g = d.groupby("barcode").weight_g
    s = g.first() if pick == "first" else (g.last() if pick == "last" else g.mean())
    return s / 1000.0


def crush_load(scans, weights, order="first"):
    """Weight scanned into each parcel's cage after it (kg), from the LOAD events and a per-barcode weight."""
    s = scans[scans.event == "LOAD"]
    agg = "min" if order == "first" else "max"
    s = s.groupby(["cage_label", "barcode"], sort=False).scan_utc.agg(agg).reset_index()
    s["w"] = s.barcode.map(weights).fillna(0.0).values
    s = s.sort_values(["cage_label", "scan_utc", "barcode"], kind="mergesort").reset_index(drop=True)
    g = s.groupby("cage_label", sort=False)
    s["load_above"] = g.w.transform("sum") - g.w.cumsum()
    s["heavy"] = (s.w >= HEAVY_KG).astype(int)
    s["heavy_above"] = g.heavy.transform("sum") - g.heavy.cumsum()
    rv = s.iloc[::-1]
    mx = rv.groupby("cage_label", sort=False).w.cummax()
    s["max_above"] = mx.groupby(rv.cage_label.values, sort=False).shift(1).reindex(s.index).fillna(0.0)
    n = g.barcode.transform("size")
    s["pos"] = g.cumcount()
    s["n_cage"] = n
    s["frac_after"] = (n - 1 - s.pos) / (n - 1).clip(lower=1)
    s["cage_kg"] = g.w.transform("sum")
    s["cage_heavy"] = g.heavy.transform("sum")
    return s.set_index("barcode")[["cage_label", "load_above", "heavy_above", "max_above", "frac_after", "cage_kg",
                                   "cage_heavy", "pos", "n_cage"]]


def base_table(rec, accounts, check_audits=False, notfound_as_ok=False, weight_pick="first", order="first",
               key="exact", window="build"):
    a = rec["audits"]
    a = a if check_audits else a[a.audit_type == "ROUTINE"]
    if window == "audit":
        d = a.audit_start_local.str[:10]
        a = a[(d >= "2026-07-01") & (d <= "2026-09-30")]
    ln = rec["lines"].merge(a[["audit_id", "cage_label", "hub", "build_date"]], on="audit_id")
    if notfound_as_ok:
        ln = ln.assign(condition=ln.condition.replace({"NOT FOUND": "OK"}))
    ln = ln[ln.condition.isin(["OK", "DAMAGED"])].copy()
    ln["dam"] = (ln.condition == "DAMAGED").astype(int)
    ln["hubk"] = ln.hub.map(NAME2KEY)
    wts = dws_weight(rec["dws"], weight_pick, key)
    dws1 = rec["dws"].drop_duplicates("barcode")[["barcode", "length_mm", "width_mm", "height_mm", "shape"]]
    ln = ln.merge(dws1.rename(columns={"shape": "dshape"}), on="barcode", how="left")
    ln = ln.merge(rec["manifests"], on="barcode", how="left")
    ln["kg"] = ln.barcode.map(wts).values
    ln["sector"] = ln.account.map(accounts.set_index("account").sector).values
    cl = crush_load(rec["scans"], wts, order)
    ln = ln.join(cl.drop(columns=["cage_label"]), on="barcode")
    ln["lkg"] = np.log(ln.kg.clip(lower=0.05))
    ln["heavyp"] = (ln.kg >= HEAVY_KG).astype(int)
    ln["wband"] = pd.cut(ln.kg, [0, 0.5, 1, 2, 5, 10, 99], labels=False)
    return ln.reset_index(drop=True)


def _X(t, extra=None, sector=False):
    X = pd.DataFrame({"frag": (t.fragile == "Y").astype(float), "box": (t.dshape == "BOX").astype(float),
                      "bag": (t.dshape == "BAG").astype(float), "lkg": t.lkg, "nd": (t.service == "24H").astype(float),
                      "eco": (t.service == "ECO").astype(float), "hv": t.heavyp.astype(float)})
    if sector:
        X = pd.concat([X, pd.get_dummies(t.sector, prefix="s", drop_first=True).astype(float)], axis=1)
    if extra is not None:
        for k, v in extra.items():
            X[k] = np.asarray(v, dtype=float)
    return sm.add_constant(X, has_constant="add")


def oe(t, X, fam="bin"):
    f = sm.families.Binomial() if fam == "bin" else sm.families.Poisson()
    m = sm.GLM(t.dam.values, X.values.astype(float), family=f).fit()
    e = m.predict(X.values.astype(float))
    g = pd.DataFrame({"h": t.hubk.values, "o": t.dam.values, "e": e}).groupby("h").sum()
    n = t.groupby("hubk").size()
    return (g.o - g.e) / n * 1e4, m


def cells_oe(t, keys):
    r = t.groupby(keys, dropna=False).dam.transform("mean")
    g = pd.DataFrame({"h": t.hubk.values, "o": t.dam.values, "e": r.values}).groupby("h").sum()
    n = t.groupby("hubk").size()
    return (g.o - g.e) / n * 1e4


def _crush_terms(t, f, inter=True):
    box = (t.dshape == "BOX").astype(float); bag = (t.dshape == "BAG").astype(float); hv = t.heavyp.astype(float)
    if not inter:
        return {"f": f}
    return {"f": f, "box_f": box * f, "bag_f": bag * f, "hv_f": hv * f}


def golden_family(t, thresholds=(35, 45, 60, 75, 95), quick=False):
    """Every specification that reads each parcel's load from the scan order and the DWS weights."""
    out = {}
    tf = t.assign(fr=t.fragile)
    for T in thresholds:
        out["g_cells_T%d" % T] = cells_oe(tf.assign(ls=(t.load_above >= T).astype(int)), ["dshape", "wband", "fr", "ls"])
    out["g_cells_bands"] = cells_oe(tf.assign(lb=pd.cut(t.load_above, BANDS, labels=False)), ["dshape", "wband", "fr", "lb"])
    forms = {"ind60": (t.load_above >= 60).astype(float), "lin": t.load_above / 50, "log": np.log1p(t.load_above),
             "cnt": t.heavy_above.astype(float), "max": t.max_above / 20}
    for k, f in forms.items():
        out["g_logit_" + k], _ = oe(t, _X(t, _crush_terms(t, f)))
        if not quick:
            out["g_logit_%s_noint" % k], _ = oe(t, _X(t, _crush_terms(t, f, False)))
    if not quick:
        for T in (30, 45, 80, 100):
            out["g_logit_ind%d" % T], _ = oe(t, _X(t, _crush_terms(t, (t.load_above >= T).astype(float))))
        out["g_pois_ind60"], _ = oe(t, _X(t, _crush_terms(t, forms["ind60"])), "pois")
        out["g_logit_ind60_sector"], _ = oe(t, _X(t, _crush_terms(t, forms["ind60"]), sector=True))
    return out


def supported(name):
    """The forms the record's own fit supports (the log of the load is refuted by its deviance)."""
    return not name.startswith("g_logit_log")


def readers(t, rec, quick=False):
    out = {"first_look": t.groupby("hubk").dam.mean() * 1e4}
    tf = t.assign(fr=t.fragile, sv=t.service)
    out["a_fields"] = cells_oe(tf, ["dshape", "wband", "fr", "sv"])
    out["e_literal"], _ = oe(t, _X(t))
    box = (t.dshape == "BOX").astype(float); bag = (t.dshape == "BAG").astype(float)
    fill = t.n_cage.astype(float)
    ex = {"fill": fill, "box_lkg": box * t.lkg, "frag_box": (t.fragile == "Y") * box, "box_fill": box * fill}
    out["c_perrecord"], _ = oe(t, _X(t, ex, sector=True))
    exb = dict(ex)
    exb.update({"fa": t.frac_after, "cw": t.cage_kg / 50, "ch": t.cage_heavy, "box_fa": box * t.frac_after,
                "box_cw": box * t.cage_kg / 50, "box_ch": box * t.cage_heavy, "fa_cw": t.frac_after * t.cage_kg / 50})
    out["b_constructing"], _ = oe(t, _X(t, exb))
    out["b_posbands"] = cells_oe(tf.assign(pb=pd.cut(t.frac_after, [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01], labels=False)),
                                 ["dshape", "wband", "fr", "pb"])
    top = t[(t.frac_after < 0.33) & (t.heavyp == 0)]
    out["b_topthird"] = top.groupby("hubk").dam.mean() * 1e4
    exd = {"ch": t.cage_heavy, "cw": t.cage_kg / 50, "box_ch": box * t.cage_heavy, "box_cw": box * t.cage_kg / 50,
           "bag_ch": bag * t.cage_heavy}
    out["d_mechanism"], _ = oe(t, _X(t, exd))
    decl = rec["manifests"].drop_duplicates("barcode").set_index("barcode").declared_kg
    la2 = t.barcode.map(crush_load(rec["scans"], decl).load_above)
    out["d2_declared"], _ = oe(t, _X(t, _crush_terms(t, la2 / 50)))
    out["d2_declared_ind"], _ = oe(t, _X(t, _crush_terms(t, (la2 >= 60).astype(float))))
    out["d2_declared_band"] = cells_oe(tf.assign(lb=pd.cut(la2, BANDS, labels=False)), ["dshape", "wband", "fr", "lb"])
    out.update(golden_family(t, quick=quick))
    return pd.DataFrame(out)


def wrong_reason(r):
    """A reader who sets Zaragoza aside for a reason that is not the load (an auditor, a crew) and takes the next
    hub on the attribute standardisation."""
    s = r["e_literal"].drop("ZAZ").sort_values(ascending=False)
    return s.index[0], float(s.iloc[0] / s.iloc[1]) if s.iloc[1] > 0 else float("inf")


def fits(t):
    res = {}
    forms = {"none": None, "ind60": (t.load_above >= 60).astype(float), "lin": t.load_above / 50,
             "log": np.log1p(t.load_above), "cnt": t.heavy_above.astype(float), "max": t.max_above / 20}
    for k, f in forms.items():
        _, m = oe(t, _X(t, None if f is None else _crush_terms(t, f)))
        res[k] = round(float(m.deviance), 1)
    return res


def summarise(df):
    rows = []
    for c in df.columns:
        s = df[c].sort_values(ascending=False)
        lead = s.iloc[0] / s.iloc[1] if s.iloc[1] > 0 else float("inf")
        rows.append((c, s.index[0], round(float(s.iloc[0]), 1), s.index[1], round(float(s.iloc[1]), 1), round(float(lead), 2)))
    return pd.DataFrame(rows, columns=["reader", "pick", "top", "second", "second_val", "lead"])


def fit_table(t, rec):
    """Every fitted specification a solver could compare on the quarter's audits: the rivals on file and the load
    forms, each with its deviance, parameter count, AIC, BIC and the per-hub excess it implies."""
    n = len(t)
    box = (t.dshape == "BOX").astype(float); bag = (t.dshape == "BAG").astype(float)
    fill = t.n_cage.astype(float)
    ex_c = {"fill": fill, "box_lkg": box * t.lkg, "frag_box": (t.fragile == "Y") * box, "box_fill": box * fill}
    ex_b = dict(ex_c)
    ex_b.update({"fa": t.frac_after, "cw": t.cage_kg / 50, "ch": t.cage_heavy, "box_fa": box * t.frac_after,
                 "box_cw": box * t.cage_kg / 50, "box_ch": box * t.cage_heavy, "fa_cw": t.frac_after * t.cage_kg / 50})
    ex_d = {"ch": t.cage_heavy, "cw": t.cage_kg / 50, "box_ch": box * t.cage_heavy, "box_cw": box * t.cage_kg / 50,
            "bag_ch": bag * t.cage_heavy}
    decl = rec["manifests"].drop_duplicates("barcode").set_index("barcode").declared_kg
    la2 = t.barcode.map(crush_load(rec["scans"], decl).load_above)
    specs = {"rival_attributes": (None, False), "rival_per_record": (ex_c, True), "rival_constructing": (ex_b, False),
             "rival_mechanism": (ex_d, False), "rival_declared_lin": (_crush_terms(t, la2 / 50), False),
             "rival_declared_step": (_crush_terms(t, (la2 >= 60).astype(float)), False)}
    forms = {"step30": (t.load_above >= 30).astype(float), "step35": (t.load_above >= 35).astype(float),
             "step45": (t.load_above >= 45).astype(float), "step60": (t.load_above >= 60).astype(float),
             "step80": (t.load_above >= 80).astype(float), "step100": (t.load_above >= 100).astype(float),
             "lin": t.load_above / 50, "log1p": np.log1p(t.load_above), "log": np.log(t.load_above + 0.1),
             "cnt": t.heavy_above.astype(float), "max": t.max_above / 20}
    for k, f in forms.items():
        specs["load_" + k] = (_crush_terms(t, f), False)
        specs["load_%s_noint" % k] = (_crush_terms(t, f, False), False)
    specs["load_step60_sector"] = (_crush_terms(t, forms["step60"]), True)
    rich = dict(ex_b)
    rich.update(_crush_terms(t, forms["step60"]))
    specs["load_step60_plus_constructing"] = (rich, False)
    rows = []
    for name, (ex, sector) in specs.items():
        X = _X(t, ex, sector=sector)
        r, m = oe(t, X)
        k = X.shape[1]
        rows.append(dict(spec=name, deviance=float(m.deviance), k=int(k), aic=float(m.deviance + 2 * k),
                         bic=float(m.deviance + k * np.log(n)), **{h: float(r[h]) for h in r.index}))
    return pd.DataFrame(rows).set_index("spec")

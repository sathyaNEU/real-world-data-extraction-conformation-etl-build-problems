"""The golden construction, run on the shipped files only (pandas): the eligible fleet from the registration
snapshot, each vehicle's initial-inspection reading, the cumulative miles the inspected fleet has travelled by age,
each vehicle's 2027 miles as its own level against that curve times the curve's rise over 2027, the county fill,
Table 2 and the 10-ton line. Also every rival route the ladder names and the estimator family the closure measures."""
import os
from functools import lru_cache

import numpy as np
import pandas as pd

import world as W

KM = 0.621371192


@lru_cache(maxsize=None)
def load(target):
    f = lambda k: os.path.join(target, W.FILES[k])
    reg = pd.read_csv(f("registrations"), dtype=str)
    tst = pd.read_csv(f("inspections"), dtype=str)
    body = pd.read_csv(f("body"), dtype=str).set_index("body_code")["program_class"]
    rates = pd.read_excel(f("rates"), sheet_name="Table 2").set_index("model_year")
    return reg, tst, body, rates


@lru_cache(maxsize=None)
def readings(target):
    """Each vehicle's completed initial inspection with a usable reading, in miles; age from 1 January of the model
    year; one row per test record after exact re-sent duplicates are dropped."""
    reg, tst, body, rates = load(target)
    t = tst.drop_duplicates()
    t = t[(t["test_type"] == "INITIAL") & t["result"].isin(["PASS", "FAIL"])].copy()
    t["odo"] = pd.to_numeric(t["odometer"])
    t = t[t["odo"].notna() & ~t["odo"].isin([0, 999999])].copy()
    t["miles"] = np.where(t["odometer_unit"] == "KM", t["odo"] * KM, t["odo"])
    t["when"] = pd.to_datetime(t["test_start"])
    t["my"] = t["model_year"].astype(int)
    start = pd.to_datetime(t["my"].astype(str) + "-01-01")
    t["age"] = (t["when"] - start).dt.days / 365.25
    t = t.sort_values(["when", "test_id"], kind="mergesort")
    return t


@lru_cache(maxsize=None)
def eligible(target):
    reg, tst, body, rates = load(target)
    r = reg[(reg["record_status"] == "ACTIVE") & reg["county_no"].isin(["%02d" % n for n in W.CNO.values()])].copy()
    r["my"] = r["model_year"].astype(int)
    r = r[r["my"].between(*W.ELIG_MY) & r["fuel_code"].isin(["G", "F"]) & r["gvwr_class"].isin(["1", "2a"])].copy()
    r["county"] = r["county_no"].astype(int).map(W.NAME_OF)
    r["cls"] = r["body_code"].map(body)
    r["rate"] = [rates.at[m, "passenger_car_g_per_mi" if c == "PC" else "light_truck_g_per_mi"]
                 for m, c in zip(r["my"], r["cls"])]
    return r


def match(target, vehicles):
    """Each vehicle's own reading: its VIN on a completed initial test, else the test whose plate and model year are
    the vehicle's (a VIN the inspector typed wrong), the first such test where there are two."""
    return match_on(readings(target), vehicles, set(load(target)[0]["vin"]))


def match_on(t, vehicles, regvins, fallback=True):
    first = t.drop_duplicates("vin")
    byvin = first.set_index("vin")
    out = vehicles[["vin", "plate", "my"]].copy()
    out["miles"] = out["vin"].map(byvin["miles"])
    out["age"] = out["vin"].map(byvin["age"])
    out["test_id"] = out["vin"].map(byvin["test_id"])
    if not fallback:
        return out
    orphan = t[~t["vin"].isin(regvins)].drop_duplicates(["plate", "my"])
    bp = orphan.set_index(["plate", "my"])
    miss = out["miles"].isna()
    for i in out.index[miss]:
        key = (out.at[i, "plate"], out.at[i, "my"])
        if key in bp.index:
            out.at[i, "miles"] = bp.loc[key, "miles"]
            out.at[i, "age"] = bp.loc[key, "age"]
            out.at[i, "test_id"] = bp.loc[key, "test_id"]
    return out


def quad(target):
    t = readings(target)
    p = np.polyfit(t["age"].to_numpy(), t["miles"].to_numpy(), 2)
    return lambda a: np.polyval(p, a)


def family(target):
    """The smooth fits a competent analyst would use for the cumulative curve, plus the raw one-year bins."""
    t = readings(target)
    A, O = t["age"].to_numpy(), t["miles"].to_numpy()
    fam = {}
    for d in (2, 3, 4):
        p = np.polyfit(A, O, d)
        fam["ols%d" % d] = (lambda a, p=p: np.polyval(p, a))
    edges = np.arange(0, 36, 1.0)
    idx = np.digitize(A, edges)
    pts = np.array([(A[idx == j].mean(), O[idx == j].mean(), (idx == j).sum()) for j in range(1, len(edges))
                    if (idx == j).sum() >= 30])
    for h in (4.0, 6.0):
        g = np.linspace(0, 36, 361)
        gv = []
        for x in g:
            w = np.clip(1 - (np.abs(pts[:, 0] - x) / h) ** 3, 0, None) ** 3 * pts[:, 2]
            X = np.c_[np.ones(len(pts)), pts[:, 0] - x]
            Wm = np.diag(w)
            gv.append(np.linalg.lstsq(X.T @ Wm @ X, X.T @ Wm @ pts[:, 1], rcond=None)[0][0])
        fam["ll%g" % h] = (lambda a, g=g, gv=np.array(gv): np.interp(a, g, gv))
    fam["bin1"] = (lambda a, p=pts: np.interp(a, p[:, 0], p[:, 1]))
    return fam


def family_wide(target):
    """The wider family the closure table walks: every reasonable fit of the cumulative curve, on every reasonable
    subset of the readings, each vehicle's own level kept; also the county-by-county curves."""
    t = readings(target)
    el = eligible(target).reset_index(drop=True)
    m = match(target, el)
    A, O = t["age"].to_numpy(), t["miles"].to_numpy()
    out = {k: fill_and_tons(el, own_level(el, m, f))[0] for k, f in family(target).items()}
    X = np.c_[A, A ** 2]
    b = np.linalg.lstsq(X, O, rcond=None)[0]
    out["ols2_0"] = fill_and_tons(el, own_level(el, m, lambda a: b[0] * a + b[1] * a ** 2))[0]
    for d in (1, 2):
        la = np.polyfit(A, O / A, d)
        out["lifeavg%d" % d] = fill_and_tons(el, own_level(el, m, lambda a, la=la: a * np.polyval(la, a)))[0]
    for lab, msk in (("elig", t["my"].between(*W.ELIG_MY)), ("age10", t["age"] >= 10),
                     ("my9612", t["my"].between(1996, 2012))):
        k = msk.to_numpy()
        p = np.polyfit(A[k], O[k], 2)
        out["ols2_" + lab] = fill_and_tons(el, own_level(el, m, lambda a, p=p: np.polyval(p, a)))[0]
    g = t.groupby("my").agg(a=("age", "mean"), o=("miles", "mean"), n=("age", "size"))
    g = g[g["n"] >= 30].sort_values("a")
    out["bymy"] = fill_and_tons(el, own_level(el, m, lambda a: np.interp(a, g["a"].to_numpy(), g["o"].to_numpy())))[0]
    reg = load(target)[0]
    rank = reg.assign(r=(reg["record_status"] != "ACTIVE").astype(int)).sort_values(["vin", "r", "status_date"],
                                                                                     ascending=[True, True, False])
    home = rank.drop_duplicates("vin").set_index("vin")["county_no"]
    tc = t.assign(c=t["vin"].map(home))
    miles = np.full(len(el), np.nan)
    for c in W.NAMES:
        s = tc[tc["c"] == "%02d" % W.CNO[c]]
        p = np.polyfit(s["age"].to_numpy(), s["miles"].to_numpy(), 2)
        ix = (el["county"] == c).to_numpy()
        mc = own_level(el[ix], m[ix], lambda a, p=p: np.polyval(p, a))
        miles[ix] = mc
    out["county"] = fill_and_tons(el, miles)[0]
    best = None
    for bb in np.linspace(0.005, 0.12, 231):
        X = np.c_[(1 - np.exp(-bb * A)) / bb, np.ones(len(A))]
        co = np.linalg.lstsq(X, O, rcond=None)[0]
        sse = float(((X @ co - O) ** 2).sum())
        if best is None or sse < best[0]:
            best = (sse, bb, co)
    _, bb, co = best
    out["expdecay"] = fill_and_tons(el, own_level(el, m, lambda a: co[0] * (1 - np.exp(-bb * a)) / bb + co[1]))[0]
    return out


def forms_fit(target):
    """Residual sum of squares of each functional form against the one-year means of the readings (weighted by the
    readings in each year), the quadratic's beside the forms the readings reject."""
    t = readings(target)
    A, O = t["age"].to_numpy(), t["miles"].to_numpy()
    edges = np.arange(0, 36, 1.0)
    idx = np.digitize(A, edges)
    pts = np.array([(A[idx == j].mean(), O[idx == j].mean(), (idx == j).sum(), O[idx == j].std())
                    for j in range(1, len(edges)) if (idx == j).sum() >= 30])
    def chi(f):
        return float((((pts[:, 1] - f(pts[:, 0])) / (pts[:, 3] / np.sqrt(pts[:, 2]))) ** 2).sum())
    out = {}
    p = np.polyfit(A, O, 2)
    out["quadratic"] = chi(lambda a: np.polyval(p, a))
    p1 = np.polyfit(A, O, 1)
    out["linear"] = chi(lambda a: np.polyval(p1, a))
    ok = (A > 0.5) & (O > 0)
    b1, b0 = np.polyfit(np.log(A[ok]), np.log(O[ok]), 1)
    out["power"] = chi(lambda a: np.exp(b0) * a ** b1)
    q = np.polyfit(np.log(A[ok]), np.log(O[ok]), 2)
    out["log_quadratic"] = chi(lambda a: np.exp(np.polyval(q, np.log(a))))
    best = None
    for bb in np.linspace(0.005, 0.12, 231):
        X = np.c_[(1 - np.exp(-bb * A)) / bb, np.ones(len(A))]
        co = np.linalg.lstsq(X, O, rcond=None)[0]
        sse = float(((X @ co - O) ** 2).sum())
        if best is None or sse < best[0]:
            best = (sse, bb, co)
    _, bb, co = best
    out["exponential_decay"] = chi(lambda a: co[0] * (1 - np.exp(-bb * a)) / bb + co[1])
    return out, len(pts)


def fill_and_tons(el, miles):
    e = el.assign(m27=np.asarray(miles, float))
    e["m27"] = e["m27"].fillna(e.groupby(["county", "my"])["m27"].transform("mean"))
    e["grams"] = e["m27"] * e["rate"]
    tons = e.groupby("county")["grams"].sum() / W.GRAMS_PER_TON
    return tons.reindex(W.NAMES), e


def own_level(el, m, M):
    a0, a1 = (2027 - el["my"]).to_numpy(), (2028 - el["my"]).to_numpy()
    return np.asarray(m["miles"] / M(m["age"].to_numpy()) * (M(a1) - M(a0)))


@lru_cache(maxsize=None)
def golden(target):
    el = eligible(target).reset_index(drop=True)
    m = match(target, el)
    M = quad(target)
    tons, e = fill_and_tons(el, own_level(el, m, M))
    return dict(tons=tons, frame=e, read=m["miles"].notna().groupby(el["county"]).sum().reindex(W.NAMES),
                n=el.groupby("county").size().reindex(W.NAMES), M=M)


@lru_cache(maxsize=None)
def routes(target):
    """Every route the ladder and the closure table name, each a county series of 2027 short tons."""
    el = eligible(target).reset_index(drop=True)
    m = match(target, el)
    t = readings(target)
    A, O = t["age"].to_numpy(), t["miles"].to_numpy()
    out = {}
    for nm, M in family(target).items():
        out[nm] = fill_and_tons(el, own_level(el, m, M))[0]
    a0, a1 = (2027 - el["my"]).to_numpy(), (2028 - el["my"]).to_numpy()
    at = m["age"].to_numpy()
    out["R1"] = fill_and_tons(el, np.asarray(m["miles"] / m["age"]))[0]
    la = np.polyfit(A, O / A, 2)
    L = lambda a: np.polyval(la, a)
    out["R1c"] = fill_and_tons(el, np.asarray(m["miles"] / m["age"]) * L((a0 + a1) / 2) / L(at))[0]
    tc = t.assign(county=t["vin"].map(el.set_index("vin")["county"]))
    regc = load(target)[0].drop_duplicates("vin").set_index("vin")["county_no"]
    tc["county"] = t["vin"].map(regc).astype(float).map(lambda x: W.NAME_OF.get(int(x)) if x == x else None)
    slope = {c: (tc.loc[tc["county"] == c, "age"] * tc.loc[tc["county"] == c, "miles"]).sum()
             / (tc.loc[tc["county"] == c, "age"] ** 2).sum() for c in W.NAMES}
    out["R1d"] = fill_and_tons(el, np.where(m["miles"].notna(), el["county"].map(slope), np.nan))[0]
    out["R0"] = fill_and_tons(el, np.where(m["miles"].notna(), np.nanmean(O / A), np.nan))[0]
    M = quad(target)
    out["R2"] = fill_and_tons(el, M(a1) - M(a0))[0]
    dM = lambda a: (M(a + 0.01) - M(a - 0.01)) / 0.02
    out["R3t"] = fill_and_tons(el, np.asarray(m["miles"] / M(at)) * dM(at))[0]
    out["golden"] = golden(target)["tons"]
    return out


def designated(tons):
    return [c for c in W.NAMES if tons[c] >= W.THRESHOLD_TONS]

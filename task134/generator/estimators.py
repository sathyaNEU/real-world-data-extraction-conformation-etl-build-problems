"""Every rung and the golden, computed from the shipped files alone (the generator's own reading of the pack;
verify.py reads it again on its own code path)."""
import datetime as dt
import os

import numpy as np
import openpyxl
import pandas as pd

AREA_KEYS = {"ELLERY": "Ellery", "WESTERLY": "Westerly", "HALDANE": "Haldane", "PELL ROAD": "Pell Road",
             "CALDERBROOK CENTRE": "Calderbrook Centre", "NORTH CALDER": "North Calder", "RAVENSDALE": "Ravensdale",
             "FERNLEA": "Fernlea"}
TIER_FAR = {"Within 200 m": 5.0, "200 m to 400 m": 4.0, "400 m to 800 m": 3.0}
OLD_KIND = {"000": "house", "032": "house", "034": "house", "210": "comm", "214": "comm", "220": "comm", "230": "comm",
            "260": "comm", "285": "rental"}
NEW_KIND = {"Detached house": "house", "Detached house with suite or laneway house": "house", "Commercial": "comm",
            "Purpose-built rental": "rental"}


# ------------------------------------------------------------------------------------------------ loading


def load(tdir):
    f = lambda n: os.path.join(tdir, n)
    old = pd.read_csv(f("roll_extract_2014-2018.csv"), dtype=str, keep_default_na=False)
    new = pd.read_csv(f("roll_extract_2019-2026.csv"), dtype=str, keep_default_na=False)
    o = pd.DataFrame({
        "year": old["ROLL_YEAR"].astype(int), "folio": old["FOLIO"],
        "area_name": old["NEIGHBOURHOOD"].map(AREA_KEYS), "zone": old["ZONE"],
        "use_code": old["ACTUAL_USE"].str[:3], "use": old["ACTUAL_USE"],
        "lot_area": pd.to_numeric(old["LAND_AREA"], errors="coerce"), "unit": old["AREA_UNIT"],
        "land": pd.to_numeric(old["LAND_VALUE"], errors="coerce"),
        "imp": pd.to_numeric(old["IMPROVEMENT_VALUE"], errors="coerce"), "plan": old["STRATA_PLAN"],
        "floor": pd.to_numeric(old["FINISHED_AREA"], errors="coerce")})
    o["kind"] = o["use_code"].map(OLD_KIND)
    o["units"] = np.where(o["use_code"].isin(["032", "034"]), 2, np.where(o["use_code"] == "000", 1, np.nan))
    n = pd.DataFrame({
        "year": new["roll_year"].astype(int), "folio": new["folio"], "area_name": new["neighbourhood"],
        "zone": new["zone_code"], "use_code": "", "use": new["use_group"],
        "lot_area": pd.to_numeric(new["lot_area"], errors="coerce"), "unit": new["area_unit"],
        "land": pd.to_numeric(new["assessed_land"], errors="coerce"),
        "imp": pd.to_numeric(new["assessed_improvements"], errors="coerce"), "plan": new["strata_plan"],
        "floor": pd.to_numeric(new["floor_area_sqft"], errors="coerce")})
    n["kind"] = n["use"].map(NEW_KIND)
    n["units"] = pd.to_numeric(new["dwelling_units"], errors="coerce")
    n["unit_no"] = new["unit_no"]
    n["strata_lot_count"] = pd.to_numeric(new["strata_lot_count"], errors="coerce")
    roll = pd.concat([o, n], ignore_index=True)
    roll["sqft"] = np.where(roll["unit"] == "AC", roll["lot_area"] * 43560.0, roll["lot_area"])
    roll["value"] = roll["land"] + roll["imp"]
    permits = pd.read_csv(f("building_permits_2014-2026.csv"), dtype=str, keep_default_na=False)
    permits["issued"] = pd.to_datetime(permits["issued_date"])
    permits["year"] = permits["issued"].dt.year
    for c in ("dwelling_units_created", "dwelling_units_demolished"):
        permits[c] = pd.to_numeric(permits[c])
    buildings = pd.read_csv(f("permit_buildings.csv"), dtype={"permit_no": str})
    occ = pd.read_csv(f("occupancy_permits_2018-2026.csv"), dtype={"permit_no": str, "occupancy_no": str})
    occ["issued"] = pd.to_datetime(occ["issued_date"])
    fh = pd.read_csv(f("folio_history_2014-2026.csv"), dtype=str)
    zoning = pd.read_csv(f("zoning_schedule_2014-2026.csv"), dtype=str, keep_default_na=False)
    wb = openpyxl.load_workbook(f("tod_order_schedule_a.xlsx"), read_only=True)
    rows = list(wb["Schedule A"].iter_rows(min_row=4, values_only=True))
    sched = pd.DataFrame(rows, columns=["folio", "address", "station", "band", "far_min", "storeys"])
    wb = openpyxl.load_workbook(f("housing_reference_tables_2026.xlsx"), read_only=True, data_only=True)
    bt = [r for r in wb["Building types"].iter_rows(min_row=4, max_row=7, values_only=True)]
    types = {r[0]: dict(far=r[4], eff=float(r[5]), nsf=float(r[6])) for r in bt}
    sv = [r for r in wb["Sale values"].iter_rows(min_row=4, values_only=True) if r[0]]
    values = {(int(r[0]), r[1]): dict(town=float(r[2]), wood=float(r[3]), conc=float(r[4])) for r in sv}
    cc = [r for r in wb["Construction costs"].iter_rows(min_row=4, values_only=True) if r[0]]
    costs = {int(r[0]): dict(TH3=float(r[1]), LR4=float(r[2]), MR6=float(r[3]), HR=float(r[4])) for r in cc}
    return dict(roll=roll, permits=permits, buildings=buildings, occ=occ, fh=fh, zoning=zoning, sched=sched, types=types,
                values=values, costs=costs)


# ------------------------------------------------------------------------------------------------ zoning and buildings

FORM_OF = {"Single detached house, with a secondary suite or a laneway house": "house", "Townhouses and rowhouses": "town",
           "Not permitted": "none", "Apartments to 4 storeys": "lowrise", "Apartments to 4 storeys and townhouses": "lowrise",
           "Apartments to 6 storeys, commercial at grade permitted": "midrise",
           "Apartments to 6 storeys above commercial": "midrise", "Apartments, no height limit": "tower"}


def zone_table(pack):
    z = {}
    for r in pack["zoning"].itertuples(index=False):
        z[r.zone_code] = dict(form=FORM_OF[r.residential_use], far=float(r.max_floor_area_ratio or 0))
    return z


def candidates(form, far):
    out = []
    if form in ("town", "lowrise", "midrise", "tower") and far >= 0.7:
        out.append(("TH3", min(1.2, far), "town"))
    if form in ("lowrise", "midrise", "tower") and far >= 1.5:
        out.append(("LR4", min(2.0, far), "wood"))
    if form in ("midrise", "tower") and far >= 3.0:
        out.append(("MR6", 3.0, "wood"))
    if form == "tower" and far > 3.0:
        out.append(("HR", far, "conc"))
    return out


def best(pack, sqft, area_name, form, far, y, only=None):
    """(type, FAR built, residual land value) of the best-paying permitted building"""
    bt, best_ = pack["types"], (None, 0.0, -np.inf)
    v = pack["values"][(y, area_name)]
    c = pack["costs"][y]
    for t, f, prod in candidates(form, far):
        if only and t not in only:
            continue
        r = sqft * f * (bt[t]["eff"] * v[prod] - c[t])
        if r > best_[2]:
            best_ = (t, f, r)
    return best_


def homes(pack, sqft, t, f):
    b = pack["types"][t]
    return int(np.floor(sqft * f * b["eff"] / b["nsf"] + 1e-9))


# ------------------------------------------------------------------------------------------------ the record


def events(pack):
    """each folio's rebuild year: the year its first counted permit for new construction was issued (methodology
    2.3: cancelled and expired permits out; a revision counted once, in the year of the permit it revises)"""
    p = pack["permits"]
    new = p[p["permit_type"] == "New Construction"]
    keep = new[new["status"].isin(["Issued", "Completed", "Superseded"])]
    ev = keep.groupby("folio")["year"].min()
    return ev.to_dict()


def panel(pack, zone_basis="in_force", lag_market=False, lag_roll=False):
    """one row per standing house, commercial or rental folio per year, with its best building and feasibility"""
    roll = pack["roll"]
    zt = zone_table(pack)
    ev = events(pack)
    rz = rezoning_dates(pack)
    st = roll[roll["kind"].notna()].copy()
    st["ev_year"] = st["folio"].map(ev)
    st = st[st["ev_year"].isna() | (st["year"] <= st["ev_year"])]
    prev = {}
    if lag_roll:
        prev = roll.set_index(["folio", "year"])["value"].to_dict()
    out = []
    for r in st.itertuples(index=False):
        y = r.year
        code = r.zone
        if zone_basis == "in_force":
            code = zone_in_force(r.folio, y, code, rz)
        elif zone_basis == "roll":
            code = r.zone
        z = zt[code]
        yv = y - 1 if (lag_market and y > 2014) else y
        t, f, rl = best(pack, r.sqft, r.area_name, z["form"], z["far"], yv)
        val = r.value
        if lag_roll:
            val = prev.get((r.folio, y - 1), r.value)
        R = rl / val if t else np.nan
        out.append((r.folio, y, r.kind, code, z["far"], t, R, r.ev_year == y, r.area_name, r.sqft, r.land, r.imp, z["form"]))
    return pd.DataFrame(out, columns=["folio", "year", "kind", "zone", "far", "btype", "R", "event", "area", "sqft", "land",
                                     "imp", "form"])


RENAME = {"RS-1": "R1", "RT-2": "RM1", "C-2": "C2", "RM-3": "RA1", "RM-5": "RA3", "CR-3": "MU3", "CD-CC": "CC1"}


def rezoning_dates(pack):
    """folios whose zone changed between rolls (not the 2020 renaming): the new zone and its in-force date"""
    roll = pack["roll"]
    zs = pack["zoning"].set_index("zone_code")
    out = {}
    g = roll[roll["sqft"].notna()].sort_values(["folio", "year"])
    for folio, grp in g.groupby("folio", sort=False):
        zs_ = list(zip(grp["year"], grp["zone"]))
        for (y0, z0), (y1, z1) in zip(zs_, zs_[1:]):
            if z0 != z1 and RENAME.get(z0) != z1:
                out[folio] = (dt.date.fromisoformat(zs.loc[z1, "in_force_from"]), z1)
    return out


def zone_in_force(folio, y, code, rz):
    """roll y shows the zone at 1 July of the year before; a rezoning in force by 1 July of year y governs year y"""
    if folio in rz:
        d, newcode = rz[folio]
        if d.year == y and d <= dt.date(y, 7, 1):
            return newcode
    return code


def rates(P, thr=1.0, years=None):
    sel = np.ones(len(P), bool) if years is None else P["year"].isin(years).values
    feas = (P["R"] > thr).values & sel
    out = {}
    for k in ("house", "comm", "rental"):
        m = feas & (P["kind"] == k).values
        out[k] = P["event"].values[m].sum() / m.sum()
    lo = sel & ~feas
    out["base"] = P["event"].values[lo].sum() / max(lo.sum(), 1)
    out["n"] = {k: int((feas & (P["kind"] == k).values).sum()) for k in ("house", "comm", "rental")}
    out["e"] = {k: int(P["event"].values[feas & (P["kind"] == k).values].sum()) for k in ("house", "comm", "rental")}
    return out


# ------------------------------------------------------------------------------------------------ the forward


def current_folios(pack):
    """Schedule A's folios carried to the folios they became (folio history), as at 31 December 2026"""
    fh = pack["fh"]
    nxt = {}
    for r in fh.itertuples(index=False):
        nxt.setdefault(r.retired_folio, []).append(r.new_folio)

    def walk(f, seen=0):
        if f not in nxt or seen > 6:
            return [f]
        out = []
        for g in nxt[f]:
            out += walk(g, seen + 1)
        return out
    s = pack["sched"]
    rows = []
    for r in s.itertuples(index=False):
        for f in walk(r.folio):
            rows.append((f, r.station, r.band))
    return pd.DataFrame(rows, columns=["folio", "station", "band"]).drop_duplicates("folio")


def forward(pack, only=None, allowed_type=False):
    """the order's standing lots at 2027: kind, best building under the order, feasibility, net homes"""
    roll = pack["roll"]
    zt = zone_table(pack)
    ev = events(pack)
    cur = current_folios(pack)
    r26 = roll[roll["year"] == 2026].set_index("folio")
    out = []
    for r in cur.itertuples(index=False):
        if r.folio not in r26.index:
            continue
        x = r26.loc[r.folio]
        if not isinstance(x["kind"], str) or r.folio in ev:
            continue
        z = zt[x["zone"]]
        far = max(TIER_FAR[r.band], z["far"])
        if allowed_type:
            t, f, rl = best(pack, x["sqft"], x["area_name"], "tower", far, 2026,
                            only=["HR"] if far > 3.0 else ["MR6"])
        else:
            t, f, rl = best(pack, x["sqft"], x["area_name"], "tower", far, 2026, only=only)
        R = rl / x["value"]
        u = 0 if x["kind"] == "comm" else int(x["units"])
        out.append(dict(folio=r.folio, station=r.station, band=r.band, kind=x["kind"], far=far, btype=t, far_built=f,
                        R=R, homes=homes(pack, x["sqft"], t, f), units=u, sqft=x["sqft"], land=x["land"], imp=x["imp"],
                        area=x["area_name"]))
    return pd.DataFrame(out)


def project(F, rate_of, net, thr=1.0, deplete=True):
    h = np.where(F["R"].values > thr, F["kind"].map(rate_of).values.astype(float), rate_of.get("base", 0.0))
    s = np.ones(len(F))
    out = []
    for t in range(5):
        out.append(float((s * h * net).sum()))
        if deplete:
            s = s * (1 - h)
    return np.array(out)


def golden(pack, P=None, F=None):
    P = panel(pack) if P is None else P
    F = forward(pack) if F is None else F
    r = rates(P)
    Y = project(F, r, (F["homes"] - F["units"]).values)
    return dict(yearly=Y, total=float(Y.sum()), rates=r, P=P, F=F)


def rnd(Y):
    return [int(round(y / 100.0) * 100) for y in Y], int(round(sum(Y) / 500.0) * 500)


# ------------------------------------------------------------------------------------------------ rivals

def net_permit_homes(pack, folios=None, years=None):
    """net new homes in counted permits for new construction (methodology 2.2 and 2.3), by folio set and years"""
    p = pack["permits"]
    new = p[(p["permit_type"] == "New Construction") & p["status"].isin(["Issued", "Completed", "Superseded"])]
    rows = []
    for folio, g in new.groupby("folio"):
        first = g.sort_values("issued").iloc[0]
        latest = g[g["status"] != "Superseded"].sort_values("issued")
        latest = latest.iloc[-1] if len(latest) else first
        rows.append((folio, int(first["year"]), int(latest["dwelling_units_created"]), int(latest["dwelling_units_demolished"])))
    d = pd.DataFrame(rows, columns=["folio", "year", "created", "demolished"])
    if folios is not None:
        d = d[d["folio"].isin(folios)]
    if years is not None:
        d = d[d["year"].isin(years)]
    return d


def default_path(pack, F=None, declining=False, years=range(2014, 2027), standing_only=False):
    """zoned capacity under the order at the corridors' take-up since their 2013 rezoning"""
    roll = pack["roll"]
    bt = pack["types"]["MR6"]
    r14 = roll[roll["year"] == 2014]
    corr = r14[r14["zone"] == "CR-3"]
    cap_c = (np.floor(corr["sqft"] * 3.0 * bt["eff"] / bt["nsf"] + 1e-9) - corr["units"].fillna(0)).clip(lower=0).sum()
    nh = net_permit_homes(pack, folios=set(corr["folio"]), years=list(years))
    tk = (nh["created"] - nh["demolished"]).sum() / cap_c / len(list(years))
    cur = current_folios(pack)
    r26 = roll[roll["year"] == 2026].set_index("folio")
    zt = zone_table(pack)
    cap = 0.0
    for r in cur.itertuples(index=False):
        if r.folio not in r26.index:
            continue
        x = r26.loc[r.folio]
        if not np.isfinite(x["sqft"]):
            continue
        if standing_only and not isinstance(x["kind"], str):
            continue
        far = max(TIER_FAR[r.band], zt[x["zone"]]["far"])
        c = np.floor(x["sqft"] * far * bt["eff"] / bt["nsf"] + 1e-9) - (0 if not np.isfinite(x["units"]) else x["units"])
        cap += max(c, 0)
    if declining:
        Y = np.array([cap * tk * (1 - tk) ** t for t in range(5)])
    else:
        Y = np.full(5, cap * tk)
    return dict(yearly=Y, total=float(Y.sum()), takeup=tk, capacity=cap, corridor_capacity=cap_c,
                corridor_homes=int((nh["created"] - nh["demolished"]).sum()))


def hybrid(pack, F, declining=False):
    d = default_path(pack)
    cap = float((F.loc[F["R"] > 1, "homes"] - F.loc[F["R"] > 1, "units"]).sum())
    tk = d["takeup"]
    Y = np.array([cap * tk * ((1 - tk) ** t if declining else 1) for t in range(5)])
    return dict(yearly=Y, total=float(Y.sum()))


def capacity_units(pack, F):
    bt = pack["types"]["MR6"]
    return (np.floor(F["sqft"] * F["far"] * bt["eff"] / bt["nsf"] + 1e-9) - F["units"]).values


def logit_fit(X, y, iters=60):
    """maximum likelihood logistic regression by Newton's method on standardised columns"""
    X = np.asarray(X, float)
    mu, sd = X.mean(0), X.std(0)
    sd[sd == 0] = 1.0
    Z = np.column_stack([np.ones(len(X)), (X - mu) / sd])
    b = np.zeros(Z.shape[1])
    b[0] = np.log(max(y.mean(), 1e-6) / max(1 - y.mean(), 1e-6))
    for _ in range(iters):
        p = 1 / (1 + np.exp(-(Z @ b)))
        g = Z.T @ (y - p)
        H = (Z * (p * (1 - p))[:, None]).T @ Z + 1e-9 * np.eye(Z.shape[1])
        step = np.linalg.solve(H, g)
        b = b + step
        if np.max(np.abs(step)) < 1e-10:
            break
    return dict(b=b, mu=mu, sd=sd)


def logit_pred(m, X):
    Z = np.column_stack([np.ones(len(X)), (np.asarray(X, float) - m["mu"]) / m["sd"]])
    return 1 / (1 + np.exp(-(Z @ m["b"])))


def covariate_logit(pack, P, F, far_form="level", units="allowed"):
    kd = lambda k: np.column_stack([(k == "comm"), (k == "rental")]).astype(float)
    ff = (lambda v: v) if far_form == "level" else np.log1p
    X = np.column_stack([np.log(P["sqft"]), np.log(P["land"]), np.log(P["imp"].clip(lower=1000)), ff(P["far"].values),
                         kd(P["kind"].values)])
    b = logit_fit(X, P["event"].values.astype(float))
    Xf = np.column_stack([np.log(F["sqft"]), np.log(F["land"]), np.log(F["imp"].clip(lower=1000)), ff(F["far"].values),
                          kd(F["kind"].values)])
    h = logit_pred(b, Xf)
    net = capacity_units(pack, F) if units == "allowed" else (F["homes"] - F["units"]).values
    s = np.ones(len(F))
    Y = []
    for t in range(5):
        Y.append(float((s * h * net).sum()))
        s = s * (1 - h)
    return dict(yearly=np.array(Y), total=float(sum(Y)))


def smooth_logit(pack, P, F, form="R", by_kind=False):
    ok = P["R"].notna().values
    x = P["R"].fillna(0).values
    xf = F["R"].values
    if form == "lnR":
        x = np.log(np.clip(x, 1e-3, None))
        xf = np.log(np.clip(xf, 1e-3, None))
    kd = lambda k: np.column_stack([(k == "comm"), (k == "rental")]).astype(float)
    X = np.column_stack([x, kd(P["kind"].values)]) if by_kind else x[:, None]
    b = logit_fit(X[ok], P["event"].values[ok].astype(float))
    Xf = np.column_stack([xf, kd(F["kind"].values)]) if by_kind else xf[:, None]
    h = logit_pred(b, Xf)
    net = (F["homes"] - F["units"]).values
    s = np.ones(len(F))
    Y = []
    for t in range(5):
        Y.append(float((s * h * net).sum()))
        s = s * (1 - h)
    return dict(yearly=np.array(Y), total=float(sum(Y)))


UPZONED = {"RT-2", "RM1", "CR-3", "MU3", "C-3", "CD-CC", "CC1"}


def upzoned_rates(P):
    m = P["zone"].isin(UPZONED).values
    return {k: P["event"].values[m & (P["kind"] == k).values].sum() / (m & (P["kind"] == k).values).sum()
            for k in ("house", "comm", "rental")}


def rivals(pack, P, F, G):
    r = G["rates"]
    net = (F["homes"] - F["units"]).values
    out = {}
    d = default_path(pack)
    out["R0 default: capacity at the corridors' take-up"] = d["yearly"]
    out["R0b default, declining"] = default_path(pack, declining=True)["yearly"]
    out["R0c default, take-up 2019 to 2026"] = default_path(pack, years=range(2019, 2027))["yearly"]
    out["R0d default, standing lots only"] = default_path(pack, standing_only=True)["yearly"]
    out["R0e hybrid: best-building capacity at the take-up"] = hybrid(pack, F)["yearly"]
    out["R0f hybrid, declining"] = hybrid(pack, F, declining=True)["yearly"]
    out["R1 covariate logit (FAR), homes at the allowance"] = covariate_logit(pack, P, F, "level", "allowed")["yearly"]
    out["R1b covariate logit (FAR), best building"] = covariate_logit(pack, P, F, "level", "best")["yearly"]
    out["R1c covariate logit (log FAR), homes at the allowance"] = covariate_logit(pack, P, F, "log", "allowed")["yearly"]
    out["R1d covariate logit (log FAR), best building"] = covariate_logit(pack, P, F, "log", "best")["yearly"]
    out["R1e smooth logit in the ratio"] = smooth_logit(pack, P, F, "R")["yearly"]
    out["R1f smooth logit in the log ratio"] = smooth_logit(pack, P, F, "lnR")["yearly"]
    out["R1g smooth logit in the ratio and kind"] = smooth_logit(pack, P, F, "R", True)["yearly"]
    Fa = forward(pack, allowed_type=True)
    out["R2 feasibility at the allowed type, homes at the allowance"] = project(Fa, r, capacity_units(pack, Fa))
    out["R2b feasibility at the best building, homes at the allowance"] = project(F, r, capacity_units(pack, F))
    pool = P["event"].values[(P["R"] > 1).values].mean()
    out["R2c one pooled rate"] = project(F, {"house": pool, "comm": pool, "rental": pool, "base": 0.0}, net)
    ru = upzoned_rates(P)
    out["R2d rates by kind on every upzoned lot"] = project(F.assign(R=2.0), dict(ru, base=0.0), net)
    out["R2e rates by kind on every upzoned lot, homes at the allowance"] = project(F.assign(R=2.0), dict(ru, base=0.0),
                                                                                    capacity_units(pack, F))
    out["L1 no depletion"] = project(F, r, net, deplete=False)
    out["L2 gross (no netting)"] = project(F, r, F["homes"].values.astype(float))
    cur = set(current_folios(pack)["folio"]) | set(pack["sched"]["folio"])
    nh = net_permit_homes(pack, folios=cur | ancestors(pack, cur), years=list(range(2019, 2027)))
    out["T trend of the order's lots 2019 to 2026"] = np.full(5, (nh["created"] - nh["demolished"]).sum() / 8.0)
    return out


def ancestors(pack, folios):
    fh = pack["fh"]
    prev = {}
    for r in fh.itertuples(index=False):
        prev.setdefault(r.new_folio, set()).add(r.retired_folio)
    out = set()
    stack = list(folios)
    while stack:
        f = stack.pop()
        for g in prev.get(f, ()):
            if g not in out:
                out.add(g)
                stack.append(g)
    return out


# ------------------------------------------------------------------------------------------------ the family

def family(pack, P, F, G):
    """defensible constructions of the golden: each must land on the golden's rounded figures"""
    net = (F["homes"] - F["units"]).values
    out = {}
    for thr in (1.1, 1.25):
        out["threshold %.2f" % thr] = project(F, rates(P, thr), net, thr=thr)
    out["prior year's values and costs"] = project(F, rates(panel(pack, lag_market=True)), net)
    out["prior roll's assessed values"] = project(F, rates(panel(pack, lag_roll=True)), net)
    for y0 in (2016, 2018, 2020, 2022):
        out["window %d to 2026" % y0] = project(F, rates(P, years=list(range(y0, 2027))), net)
    prox = P.assign(R=np.where(P["form"].isin(["midrise", "tower"]), 2.0, 0.0))
    out["feasible read as an apartment zone"] = project(F, rates(prox), net)
    ann = {}
    for k in ("house", "comm", "rental"):
        ys = []
        for y, g in P[(P["kind"] == k) & (P["R"] > 1)].groupby("year"):
            ys.append(g["event"].mean())
        ann[k] = float(np.mean(ys))
    ann["base"] = 0.0
    out["mean of the yearly rates"] = project(F, ann, net)
    r = G["rates"]
    cont = {k: 1 - np.exp(-(-np.log(1 - r[k]))) for k in ("house", "comm", "rental")}
    cont["base"] = 0.0
    out["continuous hazard"] = project(F, cont, net)
    out["zone as the roll records it"] = project(F, rates(panel(pack, zone_basis="roll")), net)
    bt = pack["types"]["MR6"]
    unr = F["sqft"].values * F["far_built"].values * bt["eff"] / bt["nsf"] - F["units"].values
    out["homes unrounded"] = project(F, r, unr)
    kd = lambda k: np.column_stack([(k == "comm"), (k == "rental")]).astype(float)
    fe = (P["R"] > 1).values.astype(float)
    X = np.column_stack([fe, kd(P["kind"].values), fe[:, None] * kd(P["kind"].values)])
    m = logit_fit(X, P["event"].values.astype(float))
    fef = (F["R"] > 1).values.astype(float)
    h = logit_pred(m, np.column_stack([fef, kd(F["kind"].values), fef[:, None] * kd(F["kind"].values)]))
    s = np.ones(len(F))
    Y = []
    for t in range(5):
        Y.append(float((s * h * net).sum()))
        s = s * (1 - h)
    out["logit on feasibility and kind"] = np.array(Y)
    grp = lambda a: "station" if a in STATIONS else ("centre" if a == "Calderbrook Centre" else "neighbourhood")
    fe = P[P["R"] > 1].assign(g=P["area"].map(grp))
    rt = fe.groupby(["kind", "g"])["event"].mean().to_dict()
    h = np.array([rt.get((k, grp(a)), r[k]) for k, a in zip(F["kind"], F["area"])])
    s = np.ones(len(F))
    Y = []
    for t in range(5):
        Y.append(float((s * h * net).sum()))
        s = s * (1 - h)
    out["rates by kind and location"] = np.array(Y)
    return out


# ------------------------------------------------------------------------------------------------ the asks

def station_of_folio(pack):
    """every folio in Schedule A, every folio it came from and every folio it became, to its station and band"""
    s = pack["sched"]
    st = {r.folio: (r.station, r.band) for r in s.itertuples(index=False)}
    fh = pack["fh"]
    prev, nxt = {}, {}
    for r in fh.itertuples(index=False):
        prev.setdefault(r.new_folio, set()).add(r.retired_folio)
        nxt.setdefault(r.retired_folio, set()).add(r.new_folio)
    out = dict(st)
    for f, v in st.items():
        stack = [f]
        while stack:
            g = stack.pop()
            for h in prev.get(g, ()):
                if h not in out:
                    out[h] = v
                    stack.append(h)
    for f in list(out):
        stack = [f]
        while stack:
            g = stack.pop()
            for h in nxt.get(g, ()):
                if h not in out:
                    out[h] = out[f]
                    stack.append(h)
    return out


STATIONS = ["Ellery", "Westerly", "Haldane", "Pell Road"]
BANDS = ["Within 200 m", "200 m to 400 m", "400 m to 800 m"]
ASK_YEARS = list(range(2022, 2027))


def ask_a(pack, mode="golden"):
    """homes completed on the order's lots by station area and year (first occupancy of each building)"""
    occ = pack["occ"].copy()
    p = pack["permits"].set_index("permit_no")
    occ["folio"] = occ["permit_no"].map(p["folio"])
    if mode == "direct":
        st = {r.folio: (r.station, r.band) for r in pack["sched"].itertuples(index=False)}
    else:
        st = station_of_folio(pack)
    occ["station"] = occ["folio"].map(lambda f: st.get(f, (None, None))[0])
    occ = occ[occ["station"].notna()]
    b = pack["buildings"].set_index(["permit_no", "building_no"])["dwelling_units"]
    if mode in ("direct", "all_records"):
        rows = occ.assign(year=occ["issued"].dt.year, units=occ["dwelling_units"])
    else:
        first = occ.sort_values("issued").groupby(["permit_no", "building_no"], as_index=False).first()
        first["year"] = first["issued"].dt.year
        if mode == "golden":
            first["units"] = [b[(pn, bn)] for pn, bn in zip(first["permit_no"], first["building_no"])]
        elif mode == "occupancy_units":
            first["units"] = first["dwelling_units"]
        elif mode == "permit_once":
            first = first.sort_values("issued").groupby("permit_no", as_index=False).first()
            first["year"] = first["issued"].dt.year
            first["units"] = first["dwelling_units"]
        rows = first
    rows = rows[rows["year"].isin(ASK_YEARS)]
    grid = {(s, y): 0 for s in STATIONS for y in ASK_YEARS}
    for r in rows.itertuples(index=False):
        grid[(r.station, r.year)] += int(r.units)
    return grid


def ask_b(pack, mode="golden"):
    """homes standing on the order's lots at the 2026 roll by station area and distance band"""
    roll = pack["roll"]
    r26 = roll[roll["year"] == 2026]
    s = pack["sched"]
    st = {r.folio: (r.station, r.band) for r in s.itertuples(index=False)}
    if mode == "schedule":
        on = r26[r26["folio"].isin(st)]
    else:
        anc = station_of_folio(pack)
        on = r26[r26["folio"].isin(anc)]
        st = anc
    grid = {(a, b): 0 for a in STATIONS for b in BANDS}
    for r in on.itertuples(index=False):
        a, band = st[r.folio]
        if r.use in ("Detached house", "Detached house with suite or laneway house", "Purpose-built rental"):
            h = int(r.units)
        elif r.use == "Strata residential":
            has_unit = isinstance(r.unit_no, str) and r.unit_no != ""
            has_floor = np.isfinite(r.floor)
            if mode == "every_strata":
                h = 1
            elif mode == "floor_only":
                h = 1 if has_floor else 0
            elif mode == "unit_only":
                h = 1 if has_unit else 0
            else:
                h = 1 if (has_unit or has_floor) else 0
        else:
            h = 0
        grid[(a, band)] += h
    if mode == "schedule":
        on_f = set(r26["folio"])
        for r in s.itertuples(index=False):
            if r.folio not in on_f and "-" in str(r.address).split(" ")[0]:
                grid[(r.station, r.band)] += 1
    return grid

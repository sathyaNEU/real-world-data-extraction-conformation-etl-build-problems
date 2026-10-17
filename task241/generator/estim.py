"""task241 estimators: each float's 2027 salinity offset by every route the checks run (the golden reads each
profile's salinity on potential-temperature levels against reference water at the profile's position), and the asks'
figures, all from the shipped files."""
import os

import numpy as np
import pandas as pd

import params as P

TOL = P.TOL
LAYER = P.LAYER


# ------------------------------------------------------------------ seawater: potential temperature (UNESCO 1983)
def _atg(s, t, p):
    ds = s - 35.0
    return (((-2.1687e-16 * t + 1.8676e-14) * t - 4.6206e-13) * p
            + ((2.7759e-12 * t - 1.1351e-10) * ds + ((-5.4481e-14 * t + 8.733e-12) * t - 6.7795e-10) * t
               + 1.8741e-8)) * p + (-4.2393e-8 * t + 1.8932e-6) * ds + ((6.6228e-10 * t - 6.836e-8) * t
                                                                          + 8.5258e-6) * t + 3.5803e-5


def ptmp(s, t, p, pr=0.0):
    """potential temperature (ITS-90 in and out) by the Fofonoff and Millard Runge-Kutta step"""
    s, t, p = np.asarray(s, float), np.asarray(t, float) * 1.00024, np.asarray(p, float)
    h = pr - p
    xk = h * _atg(s, t, p)
    t = t + 0.5 * xk
    q = xk
    p = p + 0.5 * h
    xk = h * _atg(s, t, p)
    t = t + 0.29289322 * (xk - q)
    q = 0.58578644 * xk + 0.121320344 * q
    xk = h * _atg(s, t, p)
    t = t + 1.707106781 * (xk - q)
    q = 3.414213562 * xk - 4.121320344 * q
    p = p + 0.5 * h
    xk = h * _atg(s, t, p)
    t = t + (xk - 2.0 * q) / 6.0
    return t / 1.00024


def pres_from_depth(z, lat):
    """pressure (dbar) from depth (m), Saunders (1981)"""
    c1 = 5.92e-3 + (np.sin(np.radians(lat))) ** 2 * 5.25e-3
    return ((1 - c1) - np.sqrt((1 - c1) ** 2 - 8.84e-6 * z)) / 4.42e-6


# ------------------------------------------------------------------ the shipped files
def load(target, F):
    rd = lambda k, **kw: pd.read_csv(os.path.join(target, F[k]), **kw)
    D = dict(reg=rd("register", dtype={"wmo": str}), prof=rd("profiles", dtype={"wmo": str}),
             lev=rd("levels"), tech=rd("technical", dtype={"wmo": str}), dlv=rd("deliveries", dtype={"wmo": str}),
             ac=rd("arch_casts"), al=rd("arch_levels"), ic=rd("intl_casts"), il=rd("intl_levels"))
    return D


def float_layer(D, dedup="version", ascending=True, good=True, layer=LAYER):
    """the array's 2027 profiles and their levels in the layer"""
    pr = D["prof"][D["prof"]["wmo"].isin(set(D["reg"]["wmo"]))].copy()
    if ascending:
        pr = pr[pr["direction"] == "A"]
    if dedup == "version":
        pr = pr.sort_values("file_version").drop_duplicates(["wmo", "cycle", "direction"], keep="last")
    lv = D["lev"].merge(pr[["profile_id", "wmo", "cycle", "juld", "latitude", "longitude"]], on="profile_id")
    if good:
        lv = lv[lv["pres_qc"].isin([1, 2]) & lv["temp_qc"].isin([1, 2]) & lv["psal_qc"].isin([1, 2])]
    lv = lv[(lv["pres"] >= layer[0]) & (lv["pres"] <= layer[1])].copy()
    lv["theta"] = ptmp(lv["psal"].values, lv["temp"].values, lv["pres"].values)
    return pr, lv


def reference(D, layer=(1300.0, 2050.0)):
    """every reference cast's levels in and around the layer, both sources, pressure in dbar, ITS-90"""
    ac = D["ac"]
    al = D["al"].merge(ac[["cast_id", "latitude", "longitude", "temp_scale", "time_utc"]], on="cast_id")
    t90 = np.where(al["temp_scale"] == "IPTS-68", al["temp"] / 1.00024, al["temp"])
    a = pd.DataFrame({"cast": al["cast_id"], "pres": al["pres"], "temp": t90, "psal": al["psal"], "lat": al["latitude"],
                      "lon": al["longitude"], "source": "archive", "when": al["time_utc"]})
    ic = D["ic"]
    il = D["il"].merge(ic[["station_id", "lat", "lon", "date"]], on="station_id")
    b = pd.DataFrame({"cast": il["station_id"], "pres": pres_from_depth(il["depth_m"].values, il["lat"].values),
                      "temp": il["temperature"], "psal": il["salinity"], "lat": il["lat"], "lon": il["lon"],
                      "source": "extract", "when": il["date"]})
    r = pd.concat([a, b], ignore_index=True)
    r = r[(r["pres"] >= layer[0]) & (r["pres"] <= layer[1])].copy()
    r["theta"] = ptmp(r["psal"].values, r["temp"].values, r["pres"].values)
    return r


def ref_model(r, position=True):
    """salinity of the reference water as a function of potential temperature and, where position is True, of the
    water's position: S = a + b th + c th^2 + (th - 3.5)(d lon + e lat)"""
    th = r["theta"].values
    cols = [np.ones_like(th), th, th ** 2]
    if position:
        cols += [(th - 3.5) * r["lon"].values, (th - 3.5) * r["lat"].values]
    beta = np.linalg.lstsq(np.column_stack(cols), r["psal"].values, rcond=None)[0]
    return beta


def ref_s(beta, th, lon, lat):
    s = beta[0] + beta[1] * th + beta[2] * th ** 2
    if len(beta) > 3:
        s = s + (th - 3.5) * (beta[3] * lon + beta[4] * lat)
    return s


def offsets(D, route="golden", **kw):
    """each float's offset: the mean over its profiles of the mean salinity difference over the profile's good layer
    levels, by route: golden (temperature levels, reference at the profile's position), theta_global (temperature
    levels, the basin's reference), p_global (pressure levels, the reference casts' mean), p_local (pressure levels,
    the nearest twelve casts), self (temperature levels at position, less the float's first profile)"""
    pr, lv = float_layer(D, **kw)
    out = {}
    if route in ("golden", "theta_global", "self"):
        r = reference(D)
        beta = ref_model(r, position=(route != "theta_global"))
        lv["ref"] = ref_s(beta, lv["theta"].values, lv["longitude"].values, lv["latitude"].values)
        lv["d"] = lv["psal"] - lv["ref"]
        per = lv.groupby(["wmo", "cycle", "juld"])["d"].mean().reset_index().sort_values(["wmo", "juld"])
        for w, g in per.groupby("wmo"):
            out[w] = float(g["d"].mean() - (g["d"].iloc[0] if route == "self" else 0.0))
        return out
    # pressure-level routes: each good value in the layer against the reference casts' salinity at the same pressure,
    # the casts on a 10 dbar grid
    grid = np.arange(1305.0, 1996.0, 10.0)
    r = reference(D, layer=(1250.0, 2050.0))
    prof = {}
    for c, g in r.groupby("cast"):
        g = g.sort_values("pres")
        if g["pres"].min() <= grid[0] and g["pres"].max() >= grid[-1]:
            prof[c] = (np.interp(grid, g["pres"].values, g["psal"].values), g["lon"].iloc[0], g["lat"].iloc[0])
    names = list(prof)
    M = np.array([prof[c][0] for c in names])
    clon = np.array([prof[c][1] for c in names])
    clat = np.array([prof[c][2] for c in names])
    clim = M.mean(axis=0)
    for (w, cyc, jd), g in lv.groupby(["wmo", "cycle", "juld"]):
        if route == "p_global":
            ref = clim
        else:
            lon, lat = g["longitude"].iloc[0], g["latitude"].iloc[0]
            dist = ((clon - lon) * np.cos(np.radians(lat))) ** 2 + (clat - lat) ** 2
            ref = M[np.argsort(dist)[:12]].mean(axis=0)
        d = g["psal"].values - np.interp(g["pres"].values, grid, ref)
        out.setdefault(w, []).append(float(np.mean(d)))
    return {w: float(np.mean(v)) for w, v in out.items()}


def adjusted(off):
    return sorted(w for w, v in off.items() if abs(v) > TOL)


# ------------------------------------------------------------------ the asks
def ref_casts_2000(D, dedup="match", convert=True, years=range(2015, 2026), split=False):
    """each year's distinct reference casts reaching 2,000 dbar. dedup: "match" (an extract cast is the archive's own
    when its time is within 15 minutes and its position within 0.02 degrees of an archive cast), "loose" (the same day
    and the same position to two decimals), None (every row counted); convert: the extract's depths taken to pressure"""
    ac = D["ac"].copy()
    ac["when"] = pd.to_datetime(ac["time_utc"])
    ac["year"] = ac["when"].dt.year
    ic = D["ic"].copy()
    ic["when"] = pd.to_datetime(ic["date"]) + pd.to_timedelta((ic["time"] * 3600).round(), unit="s")
    ic["year"] = ic["when"].dt.year
    ic["pmax"] = pres_from_depth(ic["max_depth_m"].values, ic["lat"].values) if convert else ic["max_depth_m"]
    keep = np.ones(len(ic), bool)
    if dedup == "match":
        for i, row in ic.iterrows():
            m = ((ac["when"] - row["when"]).abs() <= pd.Timedelta(minutes=15)) & \
                ((ac["latitude"] - row["lat"]).abs() <= 0.02) & ((ac["longitude"] - row["lon"]).abs() <= 0.02)
            keep[i] = not m.any()
    a = ac[ac["max_pres"] >= 2000]
    b = ic[keep & (ic["pmax"] >= 2000)]
    if dedup == "loose":
        u = pd.concat([pd.DataFrame({"day": a["when"].dt.date, "lat": a["latitude"].round(2), "lon": a["longitude"].round(2),
                                     "year": a["year"]}),
                       pd.DataFrame({"day": b["when"].dt.date, "lat": b["lat"].round(2), "lon": b["lon"].round(2),
                                     "year": b["year"]})]).drop_duplicates(["day", "lat", "lon"])
        n = u.groupby("year").size()
        return {y: int(n.get(y, 0)) for y in years}
    na, nb = a.groupby("year").size(), b.groupby("year").size()
    if split:
        return {y: int(na.get(y, 0)) for y in years}, {y: int(nb.get(y, 0)) for y in years}
    return {y: int(na.get(y, 0) + nb.get(y, 0)) for y in years}


def lisbon_to_utc(s, repeated="summer"):
    """the receipt log's Lisbon wall-clock times in UTC; a time in the hour the clocks went back (01:00 to 01:59 on
    31 October) is read as the first pass (summer time) or the second (winter time)"""
    t = pd.to_datetime(s)
    amb = np.asarray(((t >= "2027-10-31 01:00") & (t < "2027-10-31 02:00")).values)
    t = t.dt.tz_localize("Europe/Lisbon", ambiguous=amb if repeated == "summer" else ~amb & False, nonexistent="raise")
    return t.dt.tz_convert("UTC").dt.tz_localize(None)


def timely_by_month(D, anchor="ascent_end", version="complete", partners=False, descending=False, clock="lisbon",
                    hours=24.0, repeated="summer"):
    """each month's array profiles (by the month the float surfaced) whose complete file reached the data centre
    within the hours of the float surfacing. anchor: "ascent_end" (the technical file's end of ascent) or "juld" (the
    profile's own time); version: "complete" (the delivery carrying every level) or "first"; clock: "lisbon" (the
    receipt log's wall-clock time converted) or "utc" (read as UTC)"""
    pr = D["prof"].copy()
    if not descending:
        pr = pr[pr["direction"] == "A"]
    if not partners:
        pr = pr[pr["wmo"].isin(set(D["reg"]["wmo"]))]
    pr = pr.drop_duplicates(["wmo", "cycle", "direction"])
    t = D["tech"][["wmo", "cycle", "ascent_end"]].copy()
    t["surface"] = pd.to_datetime(t["ascent_end"]).dt.tz_localize(None)
    pr = pr.merge(t[["wmo", "cycle", "surface"]], on=["wmo", "cycle"], how="left")
    if anchor == "juld":
        pr["surface"] = pd.to_datetime("1950-01-01") + pd.to_timedelta((pr["juld"] * 86400).round(), unit="s")
    dl = D["dlv"].copy()
    dl["at"] = lisbon_to_utc(dl["received"], repeated) if clock == "lisbon" else pd.to_datetime(dl["received"])
    if version == "complete":
        dl = dl.sort_values("n_levels").drop_duplicates(["wmo", "cycle", "direction"], keep="last")
    else:
        dl = dl.sort_values("at").drop_duplicates(["wmo", "cycle", "direction"], keep="first")
    pr = pr.merge(dl[["wmo", "cycle", "direction", "at"]], on=["wmo", "cycle", "direction"], how="left")
    if clock == "lisbon" and repeated == "summer":
        # a receipt in the hour the clocks went back that would precede its own surfacing came in the second pass
        early = pr["at"] < pr["surface"]
        pr.loc[early, "at"] = pr.loc[early, "at"] + pd.Timedelta(hours=1)
    pr["ok"] = (pr["at"] - pr["surface"]) <= pd.Timedelta(hours=hours)
    pr = pr[pr["surface"].dt.year == P.YEAR]
    return {int(m): int(g["ok"].sum()) for m, g in pr.groupby(pr["surface"].dt.month)}


def profiles_used(D):
    """each float's 2027 ascending profiles with at least one good value in the layer"""
    pr, lv = float_layer(D)
    return {w: int(g[["cycle"]].drop_duplicates().shape[0]) for w, g in lv.groupby("wmo")}


def solve(target, F):
    D = load(target, F)
    routes = {r: offsets(D, r) for r in ("golden", "theta_global", "p_global", "p_local", "self")}
    off = routes["golden"]
    timely = timely_by_month(D)
    surfaced = timely_by_month(D, hours=24.0 * 365)
    arch, other = ref_casts_2000(D, split=True)
    return dict(D=D, routes=routes, off=off, adjusted=adjusted(off), used=profiles_used(D),
                model=dict(zip(D["reg"]["wmo"], D["reg"]["model"])), casts=ref_casts_2000(D), casts_arch=arch,
                casts_other=other, timely=timely, surfaced=surfaced, files=F)


# ------------------------------------------------------------------ other position-aware implementations (the checks)
def theta_local(D, k=None, radius=None, scale=None, insitu=False, sources=("archive", "extract"), good=True,
                dedup="version", layer=LAYER):
    """each float's offset on temperature levels against reference casts near each profile: the k nearest casts, the
    casts within radius degrees, or every cast weighted by a Gaussian of distance with the scale in degrees; each
    cast's salinity is interpolated to the profile's temperature levels within the cast's own range"""
    pr, lv = float_layer(D, dedup=dedup, good=good, layer=layer)
    r = reference(D, layer=(layer[0] - 300, layer[1] + 300))
    r = r[r["source"].isin(sources)]
    key = "temp" if insitu else "theta"
    if insitu:
        lv["theta"] = lv["temp"]
    casts = {}
    for c, g in r.groupby("cast"):
        g = g.sort_values(key)
        casts[c] = (g[key].values, g["psal"].values, g["lon"].iloc[0], g["lat"].iloc[0])
    names = list(casts)
    clon = np.array([casts[c][2] for c in names])
    clat = np.array([casts[c][3] for c in names])
    out = {}
    for (w, cyc, jd), g in lv.groupby(["wmo", "cycle", "juld"]):
        lon, lat = g["longitude"].iloc[0], g["latitude"].iloc[0]
        dist = np.sqrt(((clon - lon) * np.cos(np.radians(lat))) ** 2 + (clat - lat) ** 2)
        if k is not None:
            sel = np.argsort(dist)[:k]
            wt = np.ones(len(sel))
        elif radius is not None:
            sel = np.where(dist <= radius)[0]
            wt = np.ones(len(sel))
        else:
            sel = np.arange(len(names))
            wt = np.exp(-(dist / scale) ** 2)
        th = g["theta"].values
        num, den = np.zeros(th.size), np.zeros(th.size)
        for i, wi in zip(sel, wt):
            ct, cs, _, _ = casts[names[i]]
            ok = (th >= ct.min()) & (th <= ct.max())
            num[ok] += wi * np.interp(th[ok], ct, cs)
            den[ok] += wi
        ok = den > 0
        out.setdefault(w, []).append(np.mean(g["psal"].values[ok] - num[ok] / den[ok]))
    return {w: float(np.mean(v)) for w, v in out.items()}


def p_route(D, ref="mean", k=None, levels=None, depth_as_pressure=False, sources=("archive", "extract")):
    """each float's offset at fixed pressure: the profile's good layer values (or its salinity interpolated to standard
    levels every `levels` dbar) against the reference casts' mean or median salinity at the same pressure, or the
    nearest k casts' mean"""
    pr, lv = float_layer(D)
    r = reference(D, layer=(1250.0, 2050.0))
    if depth_as_pressure:
        il = D["il"].merge(D["ic"][["station_id", "lat", "lon"]], on="station_id")
        b = pd.DataFrame({"cast": il["station_id"], "pres": il["depth_m"].astype(float), "psal": il["salinity"],
                          "lat": il["lat"], "lon": il["lon"], "source": "extract"})
        r = pd.concat([r[r["source"] == "archive"], b[(b["pres"] >= 1250) & (b["pres"] <= 2050)]], ignore_index=True)
    r = r[r["source"].isin(sources)]
    grid = np.arange(1305.0, 1996.0, 10.0)
    prof = {}
    for c, g in r.groupby("cast"):
        g = g.sort_values("pres")
        if g["pres"].min() <= grid[0] and g["pres"].max() >= grid[-1]:
            prof[c] = (np.interp(grid, g["pres"].values, g["psal"].values), g["lon"].iloc[0], g["lat"].iloc[0])
    names = list(prof)
    M = np.array([prof[c][0] for c in names])
    clon = np.array([prof[c][1] for c in names])
    clat = np.array([prof[c][2] for c in names])
    clim = M.mean(axis=0) if ref == "mean" else np.median(M, axis=0)
    out = {}
    for (w, cyc, jd), g in lv.groupby(["wmo", "cycle", "juld"]):
        g = g.sort_values("pres")
        if k:
            lon, lat = g["longitude"].iloc[0], g["latitude"].iloc[0]
            dist = ((clon - lon) * np.cos(np.radians(lat))) ** 2 + (clat - lat) ** 2
            refp = M[np.argsort(dist)[:k]].mean(axis=0)
        else:
            refp = clim
        if levels:
            pl = np.arange(LAYER[0], LAYER[1] + 1, levels)
            d = np.interp(pl, g["pres"].values, g["psal"].values) - np.interp(pl, grid, refp)
        else:
            d = g["psal"].values - np.interp(g["pres"].values, grid, refp)
        out.setdefault(w, []).append(float(np.mean(d)))
    return {w: float(np.mean(v)) for w, v in out.items()}


P_VARIANTS = {"mean": dict(), "median": dict(ref="median"), "levels50": dict(levels=50.0), "levels10": dict(levels=10.0),
              "near5": dict(k=5), "near12": dict(k=12), "near20": dict(k=20), "near40": dict(k=40),
              "depth_as_pressure": dict(depth_as_pressure=True), "archive_only": dict(sources=("archive",))}


def theta_pooled(D, degree=2, layer=(1300.0, 2050.0), sources=("archive", "extract"), binned=False):
    """each float's offset on potential-temperature levels against the basin's pooled reference (no position)"""
    pr, lv = float_layer(D)
    r = reference(D, layer=layer)
    r = r[r["source"].isin(sources)]
    if binned:
        bins = np.arange(2.0, 10.0, 0.05)
        m = r.assign(b=np.digitize(r["theta"], bins)).groupby("b")[["theta", "psal"]].mean().sort_values("theta")
        ref = np.interp(lv["theta"].values, m["theta"].values, m["psal"].values)
    else:
        ref = np.polyval(np.polyfit(r["theta"].values, r["psal"].values, degree), lv["theta"].values)
    lv = lv.assign(d=lv["psal"].values - ref)
    per = lv.groupby(["wmo", "cycle"])["d"].mean()
    return per.groupby("wmo").mean().to_dict()


THETA_POOLED_VARIANTS = {"quadratic": dict(), "cubic": dict(degree=3), "layer_only": dict(layer=(1400.0, 1900.0)),
                         "binned": dict(binned=True), "archive_only": dict(sources=("archive",)),
                         "extract_only": dict(sources=("extract",))}

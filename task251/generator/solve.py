"""The golden and every named route, computed from the cut pack alone.

    load(target) reads the files the way a solver must: the hourly export with the renumbered stations joined back to
    their current numbers and occupancy read in per cent from both controller formats; the contractor's counts mapped
    to the stations; the register; the road network.
    call(D) is the golden: each station-direction's sensitivity from its validation day; the vehicles the TCX-2 cards miss
    on cold days, fitted on the bridges whose two approaches run different controllers (the TCX-2 side's free-flowing
    daily count against the TCX-4 side's, each on its validated sensitivity, by the airport's daily mean temperature);
    the loops' loss in queued traffic fitted on the bridges' paired approaches with the cold miss removed (the queued
    side's count against the free side's, as a function of the queued side's occupancy); and each station's 2027 error
    carried through its own hours by the controller in force."""
import os

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

import params as P

TOL = P.TOLERANCE


def load(target, FILES):
    p = lambda k: os.path.join(target, FILES[k])
    D = {}
    reg = pd.read_excel(p("register"), sheet_name="Stations")
    hist = pd.read_excel(p("register"), sheet_name="Code history")
    D["reg"], D["hist"] = reg, hist
    h = pd.read_csv(p("hourly"), dtype={"occupancy": str})
    back = dict(zip(hist["new_station"], hist["old_station"]))
    cur = {v: k for k, v in back.items()}
    h["station"] = h["station"].map(lambda s: cur.get(s, s))
    h["occ"] = h["occupancy"].astype(float)
    h["t"] = pd.to_datetime(h["local_start"] + h["utc_offset"], format="%Y-%m-%d %H:%M%z", utc=True)
    D["hourly"] = h
    v = pd.read_excel(p("validation"), sheet_name="Counts")
    site = dict(zip(reg["validation_site"], reg["station"]))
    v["station"] = v["site"].map(site).map(lambda s: cur.get(s, s))
    D["validation"] = v
    D["junctions"] = pd.read_excel(p("network"), sheet_name="Junctions")
    D["structures"] = pd.read_excel(p("network"), sheet_name="Structures")
    D["weather"] = pd.read_csv(p("weather"))
    return D


def current(code, D):
    m = dict(zip(D["hist"]["old_station"], D["hist"]["new_station"]))
    return m.get(code, code)


def bhat(D, per_direction=True):
    v = D["validation"]
    if per_direction:
        g = v.groupby(["station", "direction"])[["video", "loops"]].sum()
        return {k: r["loops"] / r["video"] - 1 for k, r in g.iterrows()}
    g = v.groupby("station")[["video", "loops"]].sum()
    out = {}
    for s, r in g.iterrows():
        for d in v.loc[v["station"] == s, "direction"].unique():
            out[(s, d)] = r["loops"] / r["video"] - 1
    return out


def validation_errors(D):
    g = D["validation"].groupby("station")[["video", "loops"]].sum()
    return {s: r["loops"] / r["video"] - 1 for s, r in g.iterrows()}


def bridges(D):
    """each bridge's two stations: the stations on the bridge's road on either side with no junction between"""
    out = []
    reg = D["reg"]
    for _, b in D["structures"][D["structures"]["type"] == "bridge"].iterrows():
        on = reg[reg["road"] == b["road"]]
        south = on[on["km"] < b["km_from"]].sort_values("km").iloc[-1]
        north = on[on["km"] > b["km_to"]].sort_values("km").iloc[0]
        j = D["junctions"]
        between = j[(j["road"] == b["road"]) & (j["km"] > south["km"]) & (j["km"] < north["km"])]
        assert between.empty
        out.append(dict(name=b["name"], south=south["station"], north=north["station"]))
    return out


def series(D):
    """each station-direction's hours as arrays aligned on UTC, with each hour's local day"""
    h = D["hourly"].sort_values("t")
    out = {}
    for (s, d), g in h.groupby(["station", "direction"]):
        g = g.set_index("t")
        out[(s, d)] = pd.DataFrame({"vehicles": g["vehicles"], "occ": g["occ"],
                                    "day": pd.to_datetime(g["local_start"].str[:10]).dt.date})
    return out


def tmean(D, which="mean"):
    """each local day's temperature at the airport (the day's mean, maximum or minimum); a day the airport's record
    misses takes the mean of the days either side"""
    w = D["weather"]
    col = {"mean": "Mean Temp (°C)", "max": "Max Temp (°C)", "min": "Min Temp (°C)"}[which]
    v = pd.to_numeric(w[col], errors="coerce").interpolate(limit_direction="both")
    return dict(zip(pd.to_datetime(w["Date/Time"]).dt.date, v))


def is_tcx2(D, station, days):
    """whether the station ran a TCX-2 on each day: the register's controller, and a TCX-2 before a replacement"""
    reg = D["reg"].set_index("station")
    h = D["hist"]
    row = h[h["new_station"] == station]
    if len(row):
        cut = pd.Timestamp(row["from_date"].iloc[0]).date()
        return np.array([d < cut for d in days])
    return np.full(len(days), reg.loc[station, "controller"] == "TCX-2")


def cold_points(D, bh, S=None, free_occ=18.0, which="mean"):
    """the bridges whose two approaches ran different controllers: each free-flowing day the TCX-2 side's count against
    the TCX-4 side's, each on its validated sensitivity, by the day's temperature"""
    S = S or series(D)
    tm = tmean(D, which)
    xs, ys = [], []
    for b in bridges(D):
        for d, up, dn in (("NB", b["south"], b["north"]), ("SB", b["north"], b["south"])):
            j = S[(up, d)].join(S[(dn, d)], lsuffix="_u", rsuffix="_d", how="inner")
            t2u, t2d = is_tcx2(D, up, j["day_u"].tolist()), is_tcx2(D, dn, j["day_u"].tolist())
            k = (j["occ_u"] < free_occ) & (j["occ_d"] < free_occ) & (t2u != t2d)
            j = j[k.to_numpy()].assign(t2u=t2u[k.to_numpy()])
            for day, g in j.groupby("day_u"):
                if len(g) < 6:
                    continue
                r = (g["vehicles_u"].sum() / (1 + bh[(up, d)])) / (g["vehicles_d"].sum() / (1 + bh[(dn, d)]))
                ys.append(1 - r if g["t2u"].iloc[0] else 1 - 1 / r)
                xs.append(tm[day])
    return np.array(xs), np.array(ys)


def cold_fit(x, y, form="knee"):
    if form == "knee":
        f = lambda t, a, k: np.clip(a * (k - t), 0, None)
        par, _ = curve_fit(f, x, y, p0=[0.004, 0.0])
        return (lambda t: f(np.asarray(t, float), *par)), par
    if form == "knee2":
        f = lambda t, a: np.clip(a * (2.0 - t), 0, None)
        par, _ = curve_fit(f, x, y, p0=[0.004])
        return (lambda t: f(np.asarray(t, float), *par)), par
    if form == "bins":
        e = np.arange(-30, 40, 2.0)
        idx = np.clip(np.digitize(x, e), 1, len(e))
        u = np.unique(idx)
        cen = np.array([e[i - 1] + 1 for i in u])
        val = np.where(cen > 8, 0.0, np.clip(np.array([np.mean(y[idx == i]) for i in u]), 0, None))
        return (lambda t: np.interp(t, cen, val)), (cen, val)
    raise ValueError(form)


COLD_FAMILY = ("knee", "knee2", "bins")


def by_day(D, cf, which="mean"):
    """a cold curve in the day's temperature as a function of the days"""
    tm = tmean(D, which)
    return lambda days: cf(np.array([tm[d] for d in days]))


ZDAY = lambda days: np.zeros(len(days))


def occ_channel(D, S=None, free_occ=12.0, smooth=7):
    """the cold miss read without the pairs: each day the TCX-2s' occupancy per counted vehicle in free-flowing hours
    against the TCX-4s', each station-direction on its own summer level; the TCX-2s' count falls short of the time their
    loops were covered by 1 - (TCX-4 / TCX-2)"""
    S = S or series(D)
    rel = {}
    for (s, d), g in S.items():
        k = (g["occ"] < free_occ) & (g["vehicles"] > 100)
        x = g[k]
        if x.empty:
            continue
        t2 = is_tcx2(D, s, x["day"].tolist())
        x = x.assign(t2=t2)
        day = x.groupby(["day", "t2"]).agg(o=("occ", "sum"), v=("vehicles", "sum"))
        opv = day["o"] / day["v"]
        summer = opv[[dd.month in (6, 7, 8, 9) for dd, _ in opv.index]]
        for t2v in (True, False):
            base = summer[[k2 == t2v for _, k2 in summer.index]]
            if base.empty:
                continue
            ref = float(base.median())
            for (dd, k2), val in opv.items():
                if k2 == t2v:
                    rel.setdefault((dd, k2), []).append(val / ref)
    days = sorted({dd for dd, _ in rel})
    g2 = pd.Series({dd: np.median(rel[(dd, True)]) for dd in days if (dd, True) in rel})
    g4 = pd.Series({dd: np.median(rel[(dd, False)]) for dd in days if (dd, False) in rel})
    c = (1 - g4 / g2).dropna()
    c = c.rolling(smooth, center=True, min_periods=1).mean().clip(lower=0)
    cmap = c.to_dict()
    return lambda ds: np.array([cmap.get(dd, 0.0) for dd in ds])


def chour(D, station, days, cday):
    return np.where(is_tcx2(D, station, days), cday(days), 0.0)


# ---- the occupancy a station reports per vehicle it counts, at matched counted flow -----------------------------
# A loop is covered by a vehicle whether or not the controller counts it, so the occupancy a station reports per
# vehicle it counts rises exactly in proportion with whatever share of vehicles the controller does not count. Read
# between two sets of months at the same counted flow, the ratio therefore moves one for one with a change in the
# station's counting and not at all with the traffic. It is the second, pair-free measurement of the cold miss, and it
# is what bounds a sensitivity that drifts, a drift common to both controller generations, and the counting of a
# window the validation programme did not film.

def matched_ratio(D, station, months, ref=(7, 8), S=None, free_occ=12.0, minv=60, nmin=50):
    """one station's occupancy per vehicle in `months` over the same in `ref`, both at the same counted flow"""
    S = S or series(D)
    vals, wts = [], []
    for (s, d), g in S.items():
        if s != station:
            continue
        x = g[(g["occ"] < free_occ) & (g["vehicles"] > minv)]
        m = np.array([dd.month for dd in x["day"]])
        a, b = x[np.isin(m, months)], x[np.isin(m, ref)]
        if len(a) < nmin or len(b) < nmin:
            continue
        lo = max(a["vehicles"].quantile(0.1), b["vehicles"].quantile(0.1))
        hi = min(a["vehicles"].quantile(0.9), b["vehicles"].quantile(0.9))
        if hi <= lo:
            continue
        mid = 0.5 * (lo + hi)
        fa = np.polyfit(a["vehicles"], a["occ"], 1)
        fb = np.polyfit(b["vehicles"], b["occ"], 1)
        vals.append(float(np.polyval(fa, mid) / np.polyval(fb, mid)))
        wts.append(len(a) + len(b))
    return float(np.average(vals, weights=wts)) if vals else float("nan")


def matched_table(D, S=None, months=(12, 1, 2), ref=(7, 8)):
    S = S or series(D)
    return {s: matched_ratio(D, s, months, ref, S) for s in D["reg"]["station"]}


MONTHS = tuple(range(1, 13))


def cold_station(D, S=None, ref=(7, 8)):
    """each station's own miss, month by month, from its occupancy per counted vehicle alone: no bridge pair, no
    register, no temperature. Returns station -> (days -> share missed)"""
    S = S or series(D)
    out = {}
    for s in D["reg"]["station"]:
        by = {}
        for m in MONTHS:
            r = matched_ratio(D, s, (m,), ref, S, nmin=30)
            by[m] = 0.0 if not np.isfinite(r) else max(0.0, 1.0 - 1.0 / r)
        out[s] = (lambda days, by=by: np.array([by[d.month] for d in days]))
    return out


def bridge_losses(D, bh, S=None, cday=None, at=40.0):
    """the loss fitted on each bridge's own pair, read at one occupancy: five sites, one function"""
    S = S or series(D)
    cday = cday or ZDAY
    out = {}
    for b in bridges(D):
        xs, ys = [], []
        for d, up, dn in (("NB", b["south"], b["north"]), ("SB", b["north"], b["south"])):
            j = S[(up, d)].join(S[(dn, d)], lsuffix="_u", rsuffix="_d", how="inner")
            j = j[(j["vehicles_u"] > 50) & (j["vehicles_d"] > 50)]
            days = j["day_u"].tolist()
            cu, cd = chour(D, up, days, cday), chour(D, dn, days, cday)
            xs.append(j["occ_u"].to_numpy())
            ys.append((1 - (j["vehicles_u"] / ((1 + bh[(up, d)]) * (1 - cu))) /
                       (j["vehicles_d"] / ((1 + bh[(dn, d)]) * (1 - cd)))).to_numpy())
        f, par = fit(np.concatenate(xs), np.concatenate(ys), "pl")
        out[b["name"]] = (float(np.ravel(f(np.array([at])))[0]), par)
    return out


def imbalance(D, bh, S=None, cday=None, free=12.0, queued=30.0):
    """what the pairs say with no loss curve at all: the upstream approach's count against the downstream one's, each
    on its filmed sensitivity, in free flow and in queued hours, with nothing joining or leaving between them"""
    x, y = pair_points(D, bh, S, cday)
    a, b = y[x < free], y[x > queued]
    return dict(free=float(a.mean()), free_se=float(a.std(ddof=1) / np.sqrt(len(a))), free_n=int(len(a)),
                queued=float(b.mean()), queued_se=float(b.std(ddof=1) / np.sqrt(len(b))), queued_n=int(len(b)))


def pair_points(D, bh, S=None, cday=None):
    S = S or series(D)
    cday = cday or ZDAY
    xs, ys = [], []
    for b in bridges(D):
        for d, up, dn in (("NB", b["south"], b["north"]), ("SB", b["north"], b["south"])):
            j = S[(up, d)].join(S[(dn, d)], lsuffix="_u", rsuffix="_d", how="inner")
            j = j[(j["vehicles_u"] > 50) & (j["vehicles_d"] > 50)]
            days = j["day_u"].tolist()
            cu, cd = chour(D, up, days, cday), chour(D, dn, days, cday)
            xs.append(j["occ_u"].to_numpy())
            ys.append((1 - (j["vehicles_u"] / ((1 + bh[(up, d)]) * (1 - cu))) /
                       (j["vehicles_d"] / ((1 + bh[(dn, d)]) * (1 - cd)))).to_numpy())
    return np.concatenate(xs), np.concatenate(ys)


def pair_points_ffnorm(D, S=None, cday=None, free_occ=12.0):
    """the pairs without the validated sensitivities: each hour's ratio against the pair's own free-flow ratio"""
    S = S or series(D)
    cday = cday or ZDAY
    xs, ys = [], []
    for b in bridges(D):
        for d, up, dn in (("NB", b["south"], b["north"]), ("SB", b["north"], b["south"])):
            j = S[(up, d)].join(S[(dn, d)], lsuffix="_u", rsuffix="_d", how="inner")
            j = j[(j["vehicles_u"] > 50) & (j["vehicles_d"] > 50)]
            days = j["day_u"].tolist()
            r = (j["vehicles_u"] / (1 - chour(D, up, days, cday))) / (j["vehicles_d"] / (1 - chour(D, dn, days, cday)))
            free = (j["occ_u"] < free_occ) & (j["occ_d"] < free_occ)
            ref = float(np.median(r[free]))
            xs.append(j["occ_u"].to_numpy())
            ys.append((1 - r / ref).to_numpy())
    return np.concatenate(xs), np.concatenate(ys)


def fit(x, y, form="pl"):
    if form == "pl":
        f = lambda o, a, k0: a * np.clip(o - k0, 0, None)
        par, _ = curve_fit(f, x, y, p0=[0.006, 20.0])
        return (lambda o: f(np.asarray(o, float), *par)), par
    if form == "power":
        f = lambda o, a, k0, p: a * np.clip(o - k0, 0, None) ** p
        par, _ = curve_fit(f, x, y, p0=[0.006, 20.0, 1.0], maxfev=40000)
        return (lambda o: f(np.asarray(o, float), *par)), par
    if form == "quad":
        k = x > 22
        c = np.polyfit(x[k], y[k], 2)
        return (lambda o: np.where(np.asarray(o) > 22, np.clip(np.polyval(c, o), 0, None), 0.0)), c
    if form == "lin22":
        k = x > 22
        c = np.polyfit(x[k], y[k], 1)
        return (lambda o: np.where(np.asarray(o) > 22, np.clip(np.polyval(c, o), 0, None), 0.0)), c
    if form == "bins":
        e = np.arange(0, 64, 2.0)
        idx = np.clip(np.digitize(x, e), 1, len(e))
        u = np.unique(idx)
        cen = np.array([e[i - 1] + 1 for i in u])
        val = np.where(cen < 21, 0, np.array([np.mean(y[idx == i]) for i in u]))
        return (lambda o: np.interp(o, cen, val)), (cen, val)
    raise ValueError(form)


FAMILY = ("pl", "power", "quad", "lin22", "bins")


def errors_g(D, bh, mfun, cfun, S=None, bfun=None):
    """the stations' errors with the loss, the cold miss and the sensitivity each given per station, so that every
    variant of the construction runs through one function"""
    S = S or series(D)
    bfun = bfun or (lambda s, d, days: 1 + bh[(s, d)])
    out = {}
    for s in D["reg"]["station"]:
        num = den = 0.0
        for (s2, d), g in S.items():
            if s2 != s:
                continue
            r = g["vehicles"].to_numpy(float)
            days = g["day"].tolist()
            num += r.sum()
            den += (r / (bfun(s, d, days) * (1 - mfun(s, g["occ"].to_numpy())) * (1 - cfun(s, days)))).sum()
        out[s] = num / den - 1
    return out


def errors(D, bh, mh, cday=None, S=None):
    cday = cday or ZDAY
    return errors_g(D, bh, lambda s, occ: mh(occ), lambda s, days: chour(D, s, days, cday), S)


def listed(e):
    return sorted(k for k, v in e.items() if abs(v) > TOL)


ZERO = lambda t: np.zeros_like(np.asarray(t, float))


def call(D, form="pl", cform="knee", S=None, per_direction=True):
    """the golden: the cold miss from the mixed pairs' free-flowing days against the day's mean temperature, the queue
    loss from the pairs with it removed, both carried through every station's hours by the controller in force"""
    S = S or series(D)
    bh = bhat(D, per_direction)
    cf, cpar = cold_fit(*cold_points(D, bh, S), cform)
    cday = by_day(D, cf)
    x, y = pair_points(D, bh, S, cday)
    mh, par = fit(x, y, form)
    e = errors(D, bh, mh, cday, S)
    return e, listed(e), (par, cpar)


def routes(D, S=None):
    """the ladder's rungs on the pack: the validation day, the queue loss alone, the cold miss alone, both"""
    S = S or series(D)
    bh = bhat(D)
    cday = by_day(D, cold_fit(*cold_points(D, bh, S), "knee")[0])
    xa, ya = pair_points(D, bh, S, ZDAY)
    A = errors(D, bh, fit(xa, ya, "pl")[0], ZDAY, S)
    B = errors(D, bh, ZERO, cday, S)
    G = call(D, S=S)[0]
    return dict(D=validation_errors(D), A=A, B=B, G=G)


def overcount_routes(D, S=None):
    """the cold effect read the other way round, as the TCX-4 counting more on cold days (the mixed pairs' TCX-4 side
    against the TCX-2 side, by the day's mean temperature), with and without the queue loss"""
    S = S or series(D)
    bh = bhat(D)
    x, y = cold_points(D, bh, S)
    xo, yo = x, 1 / (1 - y) - 1
    of = cold_fit(xo, yo, "knee")[0]
    tm = tmean(D)
    out = {}
    for name, with_loss in (("overcount", False), ("overcount_and_loss", True)):
        mh = fit(*pair_points(D, bh, S, ZDAY), "pl")[0] if with_loss else ZERO
        e = {}
        for s in D["reg"]["station"]:
            num = den = 0.0
            for (s2, d), g in S.items():
                if s2 != s:
                    continue
                r = g["vehicles"].to_numpy(float)
                days = g["day"].tolist()
                o = np.where(is_tcx2(D, s, days), 0.0, of(np.array([tm[k] for k in days])))
                num += r.sum()
                den += (r / ((1 + bh[(s, d)]) * (1 - mh(g["occ"].to_numpy())) * (1 + o))).sum()
            e[s] = num / den - 1
        out[name] = e
    return out


def pair_points_wide(D, bh, S=None, cday=None, drop_edges=False, agg=1):
    """the pairs with each queued spell's first and last hour left out, or summed over two-hour blocks, and each pair's
    vehicles as a weight"""
    S = S or series(D)
    cday = cday or ZDAY
    xs, ys, ws = [], [], []
    for b in bridges(D):
        for d, up, dn in (("NB", b["south"], b["north"]), ("SB", b["north"], b["south"])):
            j = S[(up, d)].join(S[(dn, d)], lsuffix="_u", rsuffix="_d", how="inner")
            j = j[(j["vehicles_u"] > 50) & (j["vehicles_d"] > 50)].copy()
            days = j["day_u"].tolist()
            j["vu"] = j["vehicles_u"] / (1 - chour(D, up, days, cday))
            j["vd"] = j["vehicles_d"] / (1 - chour(D, dn, days, cday))
            if drop_edges:
                hi = j["occ_u"] > 25
                step = j.index.to_series().diff().dt.total_seconds().eq(3600)
                prev = hi.shift(1, fill_value=False) & step
                nxt = hi.shift(-1, fill_value=False) & step.shift(-1, fill_value=False)
                j = j[~(hi & ~(prev & nxt))]
            if agg > 1:
                g = (j.index.to_series().diff().dt.total_seconds().ne(3600)).cumsum()
                k = j.groupby(g).cumcount() // agg
                j = j.assign(w=j["occ_u"] * j["vu"]).groupby([g, k]).agg(vu=("vu", "sum"), vd=("vd", "sum"),
                                                                        w=("w", "sum"), n=("occ_u", "size"))
                j = j[j["n"] == agg]
                j["occ_u"] = j["w"] / j["vu"]
            xs.append(j["occ_u"].to_numpy())
            ys.append((1 - (j["vu"] / (1 + bh[(up, d)])) / (j["vd"] / (1 + bh[(dn, d)]))).to_numpy())
            ws.append(j["vu"].to_numpy(float))
    return np.concatenate(xs), np.concatenate(ys), np.concatenate(ws)


def fit_weighted(x, y, w):
    f = lambda o, a, k0: a * np.clip(o - k0, 0, None)
    par, _ = curve_fit(f, x, y, p0=[0.006, 20.0], sigma=1 / np.sqrt(w))
    return (lambda o: f(np.asarray(o, float), *par)), par


def cold_variants(D, bh, S):
    """every licensed reading of the cold miss: the mixed pairs against the day's mean temperature in three curve
    forms, against its maximum or its minimum, and the occupancy channel day by day or as a curve in the mean"""
    out = {}
    xc, yc = cold_points(D, bh, S)
    for cform in COLD_FAMILY:
        out["mean_" + cform] = by_day(D, cold_fit(xc, yc, cform)[0])
    for which in ("max", "min"):
        x2, y2 = cold_points(D, bh, S, which=which)
        out[which + "_knee"] = by_day(D, cold_fit(x2, y2, "knee")[0], which)
        out[which + "_bins"] = by_day(D, cold_fit(x2, y2, "bins")[0], which)
    oc = occ_channel(D, S)
    out["occupancy_daily"] = oc
    tm = tmean(D)
    days = sorted(tm)
    vals = oc(days)
    out["occupancy_curve"] = by_day(D, cold_fit(np.array([tm[d] for d in days]), vals, "knee")[0])
    return out


def wide_family(D, S=None):
    """every licensed estimate of the stations' errors: five loss curve forms under every reading of the cold miss on
    the hourly pairs, the queued spells' edges left out, two-hour blocks, vehicle weights, the pairs on their own
    free-flow ratio, sensitivity pooled over directions"""
    S = S or series(D)
    bh = bhat(D)
    out = {}
    for cname, cday in cold_variants(D, bh, S).items():
        x, y = pair_points(D, bh, S, cday)
        for f in FAMILY:
            out[(f, cname)] = errors(D, bh, fit(x, y, f)[0], cday, S)
    cday = by_day(D, cold_fit(*cold_points(D, bh, S), "knee")[0])
    x2, y2, w2 = pair_points_wide(D, bh, S, cday, drop_edges=True)
    out[("pl_edges_out", "mean_knee")] = errors(D, bh, fit(x2, y2, "pl")[0], cday, S)
    x3, y3, w3 = pair_points_wide(D, bh, S, cday, agg=2)
    out[("pl_two_hour", "mean_knee")] = errors(D, bh, fit(x3, y3, "pl")[0], cday, S)
    out[("pl_weighted", "mean_knee")] = errors(D, bh, fit_weighted(*pair_points_wide(D, bh, S, cday))[0], cday, S)
    xf, yf = pair_points_ffnorm(D, S, cday)
    out[("pl_free_flow_ratio", "mean_knee")] = errors(D, bh, fit(xf, yf, "pl")[0], cday, S)
    bp = bhat(D, per_direction=False)
    cdp = by_day(D, cold_fit(*cold_points(D, bp, S), "knee")[0])
    xp, yp = pair_points(D, bp, S, cdp)
    out[("pl_pooled_sensitivity", "mean_knee")] = errors(D, bp, fit(xp, yp, "pl")[0], cdp, S)
    return out


# ---- the asks: the maintenance figures for the annual count report ----------------------------------------------

TZ = "America/Toronto"


def load_ops(target, FILES, D):
    p = lambda k: os.path.join(target, FILES[k])
    D["events"] = pd.read_csv(p("events"))
    D["orders"] = pd.read_excel(p("orders"), sheet_name="Orders")
    D["labour"] = pd.read_excel(p("orders"), sheet_name="Labour")
    return D


def district(D):
    return dict(zip(D["reg"]["station"], D["reg"]["district"]))


def tcx4_on(D, station, day):
    """the station's controller on a local day: the register's, and TCX-2 before a replacement"""
    h = D["hist"]
    row = h[h["new_station"] == station]
    if len(row) and day < pd.Timestamp(row["from_date"].iloc[0]).date():
        return False
    return D["reg"].set_index("station").loc[station, "controller"] == "TCX-4"


def quarter(day):
    return (day.month - 1) // 3 + 1


def _events(D, dedup=True):
    e = D["events"].copy()
    if dedup:
        e = e.drop_duplicates()
    e["station"] = e["station"].map(lambda s: current(s, D))
    e["t"] = pd.to_datetime(e["logged_utc"], utc=True)
    e = e[e["t"].dt.year == 2027]
    e["day"] = e["t"].dt.tz_convert(TZ).dt.date
    e["uday"] = e["t"].dt.date
    return e


def _labour_days(D, dedup=True):
    o = D["orders"].copy()
    o["station"] = o["stations"].str.split("; ")
    o = o.explode("station")
    o["station"] = o["station"].map(lambda s: current(s, D))
    lab = D["labour"].merge(o[["order", "station"]], on="order")
    lab["day"] = pd.to_datetime(lab["date"]).dt.date
    return lab.drop_duplicates(["station", "day"]) if dedup else lab


def _cells(pairs, D):
    dist = district(D)
    out = {(d, q): 0 for d in P.DISTRICTS for q in (1, 2, 3, 4)}
    for s, day in pairs:
        out[(dist[s], quarter(day))] += 1
    return out


def visits(D, door_days="local", span=True):
    """the maintenance visits (TDP-03 section 7): each station and local day one of the maintenance contractor's
    technicians attended it. Work the contractor carries out from its own premises is not a visit, and the TCX-4 logs
    the cabinet door switch on every opening, so a day labour was booked to a station then on a TCX-4 whose cabinet
    stayed shut is a controller reset sent over the link. A TCX-2 logs no door and has no remote reset, so the days
    labour was booked to it are the days it was attended. An attendance the door log shows running past midnight is a
    day either side of it."""
    lab = _labour_days(D)
    e = _events(D)
    doors = e[e["event"].isin(["DOOR_OPEN", "DOOR_CLOSE"])]
    key = "day" if door_days == "local" else "uday"
    opened = set(zip(doors["station"], doors[key]))
    booked = set(zip(lab["station"], lab["day"]))
    pairs = [(s, d) for s, d in zip(lab["station"], lab["day"]) if not tcx4_on(D, s, d) or (s, d) in opened]
    if span:
        held, seen = {}, set(pairs)
        dr = doors.sort_values("t")
        for s, ev, d in zip(dr["station"], dr["event"], dr[key]):
            if ev == "DOOR_OPEN":
                held[s] = d
            elif ev == "DOOR_CLOSE":
                o = held.pop(s, None)
                if o is not None and (d - o).days == 1 and (s, o) in booked and (s, d) not in seen:
                    pairs.append((s, d))
                    seen.add((s, d))
    return _cells(pairs, D)


def _missing_runs(D):
    """each station's runs of hours absent from the hourly record, as (station, first missing hour UTC, hours)"""
    h = D["hourly"]
    start = pd.Timestamp("2027-01-01 00:00", tz=TZ).tz_convert("UTC")
    end = pd.Timestamp("2028-01-01 00:00", tz=TZ).tz_convert("UTC")
    allh = pd.date_range(start, end, freq="h", inclusive="left")
    runs = []
    for s, g in h.groupby("station"):
        have = set(g["t"])
        miss = [t for t in allh if t not in have]
        k = 0
        while k < len(miss):
            j = k
            while j + 1 < len(miss) and miss[j + 1] - miss[j] == pd.Timedelta(hours=1):
                j += 1
            runs.append((s, miss[k], j - k + 1))
            k = j + 1
    return runs


def failures(D, quarter_clock="local", tcx2_only=False):
    """the power failures (TDP-03 section 7): each loss of mains power at a station's controller, counted once however
    long it lasts and a supply restored and lost again a second loss. A controller reports a loss it survives
    (MAINS_FAIL, once: the log repeats some after a lost poll). A loss it does not survive is in the station's hourly
    record instead, as the hours missing from the one the supply failed in to the one it was counting again in: a
    TCX-2 has no standby supply and stops at once, and a TCX-4 whose battery runs out stops as well and loses what it
    had logged, leaving the cold start it raises on the way back under an unset clock. A break holds as many losses as
    the station answered a poll and failed again inside it, at least one. The two controller replacements are not
    losses of supply."""
    e = _events(D)
    key = "day" if quarter_clock == "local" else "uday"
    mf = e[e["event"] == "MAINS_FAIL"]
    pairs = list(zip(mf["station"], mf[key]))
    lost = e[e["event"] == "COMMS_LOST"]
    swap = {(r["new_station"], pd.Timestamp(r["from_date"]).date()) for _, r in D["hist"].iterrows()}
    for s, t0, n in _missing_runs(D):
        day0 = t0.tz_convert(TZ).date()
        if (s, day0) in swap or (tcx2_only and tcx4_on(D, s, day0)):
            continue
        t1 = t0 + pd.Timedelta(hours=n)
        k = int(((lost["station"] == s) & (lost["t"] >= t0) & (lost["t"] < t1)).sum())
        day = day0 if quarter_clock == "local" else t0.date()
        pairs.extend([(s, day)] * max(1, k))
    return _cells(pairs, D)

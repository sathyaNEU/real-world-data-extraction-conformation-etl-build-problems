"""The golden and every named route, computed from the cut pack alone.

    load(target) reads the files the way a solver must: the hourly export with the renumbered stations joined back to
    their current numbers and occupancy read in per cent from both controller formats; the contractor's counts mapped
    to the stations; the register; the road network.
    call(D) is the golden: each station-direction's sensitivity from its validation day, the loops' loss in queued
    traffic fitted on the bridges' paired approaches (the queued side's count against the free side's, each on its
    validated sensitivity, as a function of the queued side's occupancy), and each station's 2027 error carried through
    its own hours."""
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
    """each station-direction's hours as arrays aligned on UTC"""
    h = D["hourly"].sort_values("t")
    out = {}
    for (s, d), g in h.groupby(["station", "direction"]):
        out[(s, d)] = g.set_index("t")[["vehicles", "occ"]]
    return out


def pair_points(D, bh, S=None):
    S = S or series(D)
    xs, ys = [], []
    for b in bridges(D):
        for d, up, dn in (("NB", b["south"], b["north"]), ("SB", b["north"], b["south"])):
            u, w = S[(up, d)], S[(dn, d)]
            j = u.join(w, lsuffix="_u", rsuffix="_d", how="inner")
            k = (j["vehicles_u"] > 50) & (j["vehicles_d"] > 50)
            j = j[k]
            xs.append(j["occ_u"].to_numpy())
            ys.append((1 - j["vehicles_u"] / j["vehicles_d"] * (1 + bh[(dn, d)]) / (1 + bh[(up, d)])).to_numpy())
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


def pair_points_wide(D, bh, S=None, drop_edges=False, agg=1):
    """the same pairs with each queued spell's first and last hour left out, or summed over two-hour blocks, and each
    pair's vehicles as a weight"""
    S = S or series(D)
    xs, ys, ws = [], [], []
    for b in bridges(D):
        for d, up, dn in (("NB", b["south"], b["north"]), ("SB", b["north"], b["south"])):
            j = S[(up, d)].join(S[(dn, d)], lsuffix="_u", rsuffix="_d", how="inner")
            j = j[(j["vehicles_u"] > 50) & (j["vehicles_d"] > 50)]
            if drop_edges:
                hi = j["occ_u"] > 25
                step = j.index.to_series().diff().dt.total_seconds().eq(3600)
                prev = hi.shift(1, fill_value=False) & step
                nxt = hi.shift(-1, fill_value=False) & step.shift(-1, fill_value=False)
                j = j[~(hi & ~(prev & nxt))]
            if agg > 1:
                g = (j.index.to_series().diff().dt.total_seconds().ne(3600)).cumsum()
                k = j.groupby(g).cumcount() // agg
                key = [g, k]
                j = j.assign(w=j["occ_u"] * j["vehicles_u"]).groupby(key).agg(
                    vehicles_u=("vehicles_u", "sum"), vehicles_d=("vehicles_d", "sum"), w=("w", "sum"),
                    n=("occ_u", "size"))
                j = j[j["n"] == agg]
                j["occ_u"] = j["w"] / j["vehicles_u"]
            xs.append(j["occ_u"].to_numpy())
            ys.append((1 - j["vehicles_u"] / j["vehicles_d"] * (1 + bh[(dn, d)]) / (1 + bh[(up, d)])).to_numpy())
            ws.append(j["vehicles_u"].to_numpy(float))
    return np.concatenate(xs), np.concatenate(ys), np.concatenate(ws)


def fit_weighted(x, y, w):
    f = lambda o, a, k0: a * np.clip(o - k0, 0, None)
    par, _ = curve_fit(f, x, y, p0=[0.006, 20.0], sigma=1 / np.sqrt(w))
    return (lambda o: f(np.asarray(o, float), *par)), par


def wide_family(D, S=None):
    """every licensed estimate of the stations' errors: five curve forms on the hourly pairs, the queued spells'
    edges left out, two-hour blocks, vehicle weights, sensitivity pooled over directions"""
    S = S or series(D)
    bh = bhat(D)
    x, y = pair_points(D, bh, S)
    out = {f: errors(D, bh, fit(x, y, f)[0], S) for f in FAMILY}
    x2, y2, w2 = pair_points_wide(D, bh, S, drop_edges=True)
    out["pl_edges_out"] = errors(D, bh, fit(x2, y2, "pl")[0], S)
    out["quad_edges_out"] = errors(D, bh, fit(x2, y2, "quad")[0], S)
    x3, y3, w3 = pair_points_wide(D, bh, S, agg=2)
    out["pl_two_hour"] = errors(D, bh, fit(x3, y3, "pl")[0], S)
    out["pl_weighted"] = errors(D, bh, fit_weighted(*pair_points_wide(D, bh, S))[0], S)
    bp = bhat(D, per_direction=False)
    xp, yp = pair_points(D, bp, S)
    out["pl_pooled_sensitivity"] = errors(D, bp, fit(xp, yp, "pl")[0], S)
    return out


def errors(D, bh, mh, S=None):
    S = S or series(D)
    out = {}
    for s in D["reg"]["station"]:
        num = den = 0.0
        for (s2, d), g in S.items():
            if s2 != s:
                continue
            r = g["vehicles"].to_numpy(float)
            num += r.sum()
            den += (r / ((1 + bh[(s, d)]) * (1 - mh(g["occ"].to_numpy())))).sum()
        out[s] = num / den - 1
    return out


def listed(e):
    return sorted(k for k, v in e.items() if abs(v) > TOL)


def call(D, form="pl", S=None, per_direction=True):
    S = S or series(D)
    bh = bhat(D, per_direction)
    x, y = pair_points(D, bh, S)
    mh, par = fit(x, y, form)
    e = errors(D, bh, mh, S)
    return e, listed(e), par


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


def visits(D, door_days="local"):
    """the maintenance visits: each station and day labour was booked to it, less the days at a TCX-4 station whose
    cabinet stayed shut (the controller was reset from the contractor's office)"""
    lab = _labour_days(D)
    e = _events(D)
    doors = e[e["event"].isin(["DOOR_OPEN", "DOOR_CLOSE"])]
    key = "day" if door_days == "local" else "uday"
    opened = set(zip(doors["station"], doors[key]))
    pairs = [(s, d) for s, d in zip(lab["station"], lab["day"]) if not tcx4_on(D, s, d) or (s, d) in opened]
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


def failures(D, quarter_clock="local"):
    """the power failures: each MAINS_FAIL a TCX-4 reported, once; at a TCX-2, which reports nothing and stops, each
    break in its hourly record, as many failures as polls it missed and answered again inside the break (at least
    one); not the two controller replacements"""
    e = _events(D)
    key = "day" if quarter_clock == "local" else "uday"
    mf = e[e["event"] == "MAINS_FAIL"]
    pairs = list(zip(mf["station"], mf[key]))
    lost = e[e["event"] == "COMMS_LOST"]
    swap = {(r["new_station"], pd.Timestamp(r["from_date"]).date()) for _, r in D["hist"].iterrows()}
    for s, t0, n in _missing_runs(D):
        day0 = t0.tz_convert(TZ).date()
        if (s, day0) in swap or tcx4_on(D, s, day0):
            continue
        t1 = t0 + pd.Timedelta(hours=n)
        k = int(((lost["station"] == s) & (lost["t"] >= t0) & (lost["t"] < t1)).sum())
        day = day0 if quarter_clock == "local" else t0.date()
        pairs.extend([(s, day)] * max(1, k))
    return _cells(pairs, D)

"""task241 independent verifier: reads only the shipped bundle (target/), the goldens, figures.json and submission.md,
recomputes the call by its own route (nearest reference casts on potential-temperature levels), both asks by their own
code, and requires the goldens and the write-up to carry the same figures."""
import json
import os
import re
import sys

import numpy as np
import pandas as pd
from openpyxl import load_workbook


def theta(s, t, p):
    """potential temperature at the surface, EOS-80 (Bryden's polynomial, integrated by Simpson's rule in 4 steps)"""
    def gamma(s, t, p):
        ds = s - 35.0
        return (3.5803e-5 + (8.5258e-6 + (-6.836e-8 + 6.6228e-10 * t) * t) * t + (1.8932e-6 - 4.2393e-8 * t) * ds
                + ((1.8741e-8 + (-6.7795e-10 + (8.733e-12 - 5.4481e-14 * t) * t) * t)
                   + (-1.1351e-10 + 2.7759e-12 * t) * ds) * p
                + (-4.6206e-13 + (1.8676e-14 - 2.1687e-16 * t) * t) * p * p)
    t68 = t * 1.00024
    n = 40
    h = -p / n
    th, pp = t68.copy(), p.copy()
    for _ in range(n):
        k1 = h * gamma(s, th, pp)
        k2 = h * gamma(s, th + k1 / 2, pp + h / 2)
        k3 = h * gamma(s, th + k2 / 2, pp + h / 2)
        k4 = h * gamma(s, th + k3, pp + h)
        th = th + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        pp = pp + h
    return th / 1.00024


def pressure(z, lat):
    x = np.sin(np.radians(lat)) ** 2
    c1 = 5.92e-3 + 5.25e-3 * x
    return ((1 - c1) - np.sqrt((1 - c1) ** 2 - 4 * 2.21e-6 * z)) / (2 * 2.21e-6)


def main(target, golden, figures, submission):
    fig = json.load(open(figures))
    rd = lambda f, **kw: pd.read_csv(os.path.join(target, f), **kw)
    reg = rd("ibfa_float_register.csv", dtype={"wmo": str})
    prof = rd("ibfa_profiles_2027.csv", dtype={"wmo": str})
    lev = rd("ibfa_profile_levels_2027.csv")
    # the call: nearest ten reference casts on potential-temperature levels
    prof = prof[(prof["direction"] == "A") & prof["wmo"].isin(set(reg["wmo"]))]
    prof = prof.sort_values("file_version").groupby(["wmo", "cycle"]).tail(1)
    lv = lev[lev["profile_id"].isin(set(prof["profile_id"]))]
    lv = lv[(lv[["pres_qc", "temp_qc", "psal_qc"]].isin([1, 2])).all(axis=1) & lv["pres"].between(1400, 1900)]
    lv = lv.merge(prof[["profile_id", "wmo", "cycle", "latitude", "longitude"]], on="profile_id")
    lv["th"] = theta(lv["psal"].values, lv["temp"].values, lv["pres"].values)
    st = rd("ioa_ctd_archive_stations.csv")
    al = rd("ioa_ctd_archive_levels.csv").merge(st, on="cast_id")
    al = al[al["pres"].between(1200, 2100)]
    al["t90"] = np.where(al["temp_scale"] == "IPTS-68", al["temp"] / 1.00024, al["temp"])
    al["th"] = theta(al["psal"].values, al["t90"].values, al["pres"].values)
    rs = rd("rhd_extract_iberian_basin_stations.csv")
    rl = rd("rhd_extract_iberian_basin_levels.csv").merge(rs, on="station_id")
    rl["p"] = pressure(rl["depth_m"].values, rl["lat"].values)
    rl = rl[rl["p"].between(1200, 2100)]
    rl["th"] = theta(rl["salinity"].values, rl["temperature"].values, rl["p"].values)
    casts = []
    for c, g in al.groupby("cast_id"):
        g = g.sort_values("th")
        casts.append((g["longitude"].iloc[0], g["latitude"].iloc[0], g["th"].values, g["psal"].values))
    for c, g in rl.groupby("station_id"):
        g = g.sort_values("th")
        casts.append((g["lon"].iloc[0], g["lat"].iloc[0], g["th"].values, g["salinity"].values))
    clon = np.array([c[0] for c in casts])
    clat = np.array([c[1] for c in casts])
    per = {}
    for (w, cyc), g in lv.groupby(["wmo", "cycle"]):
        lon, lat = g["longitude"].iloc[0], g["latitude"].iloc[0]
        near = np.argsort(((clon - lon) * np.cos(np.radians(lat))) ** 2 + (clat - lat) ** 2)[:10]
        th = g["th"].values
        num, den = np.zeros(th.size), np.zeros(th.size)
        for i in near:
            ct, cs = casts[i][2], casts[i][3]
            inr = (th >= ct[0]) & (th <= ct[-1])
            num[inr] += np.interp(th[inr], ct, cs)
            den[inr] += 1
        k = den > 0
        per.setdefault(w, []).append(np.mean(g["psal"].values[k] - num[k] / den[k]))
    off = {w: float(np.mean(v)) for w, v in per.items()}
    call = sorted(w for w, v in off.items() if abs(v) > 0.010)
    assert call == fig["call"]["adjusted"], ("verify: the call", call, fig["call"]["adjusted"])
    for w, v in fig["deliverables"]["offsets"].items():
        assert abs(off[w] - v) <= fig["components"]["band"], ("verify: offset outside the band", w, off[w], v)
    # ask A
    st["t"] = pd.to_datetime(st["time_utc"])
    rs["t"] = pd.to_datetime(rs["date"]) + pd.to_timedelta((rs["time"] * 3600).round(), unit="s")
    st_sorted = st.sort_values("t")
    copy = []
    for _, r in rs.iterrows():
        i = st_sorted["t"].searchsorted(r["t"])
        cand = st_sorted.iloc[max(0, i - 3):i + 3]
        copy.append(bool(((cand["t"] - r["t"]).abs().dt.total_seconds() <= 900).values.__and__(
            ((cand["latitude"] - r["lat"]).abs() <= 0.02).values & ((cand["longitude"] - r["lon"]).abs() <= 0.02).values
        ).any()))
    rs["copy"] = copy
    rs["pmax"] = pressure(rs["max_depth_m"].values, rs["lat"].values)
    a = st[st["max_pres"] >= 2000].groupby(st["t"].dt.year).size()
    b = rs[(~rs["copy"]) & (rs["pmax"] >= 2000)].groupby(rs["t"].dt.year).size()
    for y, v in fig["deliverables"]["casts_2000"].items():
        assert int(a.get(int(y), 0) + b.get(int(y), 0)) == v, ("verify: ask A", y)
    # ask B
    tech = rd("ibfa_cycle_technical_2027.csv", dtype={"wmo": str})
    tech["surf"] = pd.to_datetime(tech["ascent_end"]).dt.tz_convert(None)
    dl = rd("ioa_dac_receipt_log_2027.csv", dtype={"wmo": str})
    loc = pd.to_datetime(dl["received"])
    amb = ((loc >= "2027-10-31 01:00") & (loc < "2027-10-31 02:00")).values
    dl["utc"] = loc.dt.tz_localize("Europe/Lisbon", ambiguous=amb).dt.tz_convert(None)
    dl = dl[(dl["direction"] == "A") & dl["wmo"].isin(set(reg["wmo"]))]
    full = dl.loc[dl.groupby(["wmo", "cycle"])["n_levels"].idxmax()]
    x = full.merge(tech[["wmo", "cycle", "surf"]], on=["wmo", "cycle"])
    x["ok"] = (x["utc"] - x["surf"]) <= pd.Timedelta(hours=24)
    x = x[x["surf"].dt.year == 2027]
    got = x.groupby(x["surf"].dt.month)["ok"].sum()
    for mth, v in fig["deliverables"]["timely"].items():
        assert int(got.get(int(mth), 0)) == v, ("verify: ask B", mth)
    # the goldens carry the figures
    wb = load_workbook(os.path.join(golden, "ioa_dmqc_salinity_2027.xlsx"), data_only=True)
    ws = wb["Offsets 2027"]
    rows = [r for r in ws.iter_rows(min_row=5, values_only=True) if r[0] and str(r[0]).isdigit()]
    assert len(rows) == 24
    for r in rows:
        w = str(r[0])
        assert abs(r[3] - fig["deliverables"]["offsets"][w]) < 1e-9 and \
            (r[4] == "Adjust") == (w in fig["call"]["adjusted"]), ("verify: workbook row", w)
    ws = wb["Reference casts"]
    for r in ws.iter_rows(min_row=5, values_only=True):
        if isinstance(r[0], int):
            assert r[3] == fig["deliverables"]["casts_2000"][str(r[0])], ("verify: workbook casts", r)
    ws = wb["Delivery 2027"]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    for r in ws.iter_rows(min_row=5, values_only=True):
        if r[0] in months:
            assert r[2] == fig["deliverables"]["timely"][str(months.index(r[0]) + 1)], ("verify: workbook delivery", r)
    sub = open(submission).read()
    for w, v in fig["deliverables"]["offsets"].items():
        sv = "0.000" if v == 0 else "%+.3f" % v
        assert "%s: %s" % (w, sv) in sub, ("verify: submission offset", w)
    for y, v in fig["deliverables"]["casts_2000"].items():
        assert "%s %d" % (y, v) in sub, ("verify: submission casts", y)
    for mth, v in fig["deliverables"]["timely"].items():
        assert "%s %d" % (months[int(mth) - 1], v) in sub, ("verify: submission delivery", mth)
    print("verify: call, offsets within %.3f, both asks, workbook and write-up agree" % fig["components"]["band"])


if __name__ == "__main__":
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(os.path.join(task, "target"), os.path.join(task, "golden"),
         os.path.join(task, "generator", "figures.json"), os.path.join(task, "submission.md"))

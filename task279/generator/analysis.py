"""task279 from the pack: every route to the call and the asks, computed from the files in target/ alone.

The golden finds the peat that formed the top metre of each 1997 core again in its 2024 core as the depth that
holds the same cumulative ash per square metre, and takes the carbon lost as the 1997 top metre's carbon less the 2024
carbon above that depth. The wrong routes are the inventory's subsidence route (the surveyed lowering at the 1997
topsoil's carbon density), the cores aligned on the surveyed lowering (carbon above the 1997 core base level), equal
total soil mass, and the fixed depth."""
from __future__ import annotations

import csv
import datetime as dt
import os
import re

import numpy as np

import common as K

LINE97 = re.compile(r"^(97-0412-\d{4})\s+(VM-[A-Z]{2}-\d)\s+(\d\d-\d\d-\d{4})\s+(\d+)\s*-\s*(\d+)\s+([\d,]+)\s+"
                    r"([\d,]+)\s+([\d,]+)\s*$")


def num(s):
    return float(str(s).replace(",", "."))


def read_csv(path, delimiter=","):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=delimiter))


def half_up(x, nd=0):
    q = 10 ** nd
    return float(np.floor(abs(x) * q + 0.5) / q) * (1 if x >= 0 else -1)


def load(target):
    f = lambda k: os.path.join(target, K.FILES[k])
    pts = read_csv(f("points"))
    c97 = {}
    with open(f("core97"), encoding="latin-1") as fh:
        for ln in fh:
            m = LINE97.match(ln.rstrip("\r\n"))
            if m:
                c97.setdefault(m.group(2), []).append(dict(top=int(m.group(4)), bot=int(m.group(5)),
                                                           bd=num(m.group(6)), loi=num(m.group(7)), c=num(m.group(8)),
                                                           date=dt.datetime.strptime(m.group(3), "%d-%m-%Y").date()))
    c24 = {}
    for r in read_csv(f("core24"), ";"):
        c24.setdefault(r["point_code"], []).append(dict(top=int(r["depth_top_cm"]), bot=int(r["depth_bottom_cm"]),
                                                        bd=num(r["dry_bulk_density_kg_m3"]) / 1000.0,
                                                        loi=num(r["loi_550_pct_dm"]), c=num(r["total_c_pct_dm"]),
                                                        date=dt.date.fromisoformat(r["sampling_date"])))
    for d in (c97, c24):
        for k in d:
            d[k].sort(key=lambda s: s["top"])
    return pts, c97, c24


def profile(slices):
    """edges (cm) and per-slice dry mass, ash and carbon (kg/m2)."""
    edges = np.array([slices[0]["top"]] + [s["bot"] for s in slices], float)
    th = np.diff(edges)
    mass = np.array([s["bd"] for s in slices]) * th * 10.0
    ash = mass * (1 - np.array([s["loi"] for s in slices]) / 100.0)
    car = mass * np.array([s["c"] for s in slices]) / 100.0
    return edges, mass, ash, car


def cum(v):
    return np.concatenate([[0.0], np.cumsum(v)])


def depth_at(edges, per, target):
    c = cum(per)
    if target > c[-1] + 1e-9:
        return None
    i = int(np.clip(np.searchsorted(c, target) - 1, 0, len(per) - 1))
    return edges[i] + (target - c[i]) / (c[i + 1] - c[i]) * (edges[i + 1] - edges[i])


def amount_to(edges, per, z):
    c = cum(per)
    i = int(np.clip(np.searchsorted(edges, z) - 1, 0, len(per) - 1))
    return c[i] + (z - edges[i]) / (edges[i + 1] - edges[i]) * (c[i + 1] - c[i])


def point_routes(p, s97, s24):
    e97, m97, a97, k97 = profile(s97)
    e24, m24, a24, k24 = profile(s24)
    d97, d24 = s97[0]["date"], s24[0]["date"]
    years = (d24 - d97).days / 365.25
    f = 10.0 / years                                  # kg C/m2 over the interval -> t C/ha/yr
    C97, M97, A97 = k97.sum(), m97.sum(), a97.sum()
    low_cm = 100.0 * ((num(p["surface_level_1997_m"]) - K.DATUM_OFFSET_M) - num(p["surface_level_2024_m"]))
    za = depth_at(e24, a24, A97)
    zm = depth_at(e24, m24, M97)
    top = e97[1:] <= 30
    r = dict(years=years, low_cm=low_cm, C97=C97, A97=A97, M97=M97, z_ash=za, z_mass=zm)
    r["ash"] = (C97 - amount_to(e24, k24, za)) * f
    r["mass"] = (C97 - amount_to(e24, k24, zm)) * f if zm is not None else float("nan")
    r["level"] = (C97 - amount_to(e24, k24, K.CORE97_DEPTH - low_cm)) * f
    r["fixed"] = (C97 - amount_to(e24, k24, K.CORE97_DEPTH)) * f
    r["subsidence"] = low_cm * (m97[top].sum() / (30 * 10.0)) * 10.0 * (k97[top].sum() / m97[top].sum()) * f
    # variants the family carries
    top20 = e97[1:] <= 20
    r["subsidence_20"] = low_cm * (m97[top20].sum() / 200.0) * 10.0 * (k97[top20].sum() / m97[top20].sum()) * f
    t24 = e24[1:] <= 30
    r["subsidence_24"] = low_cm * (m24[t24].sum() / 300.0) * 10.0 * (k24[t24].sum() / m24[t24].sum()) * f
    # the ash route with slice-uniform concentrations read from the slice holding the target (same as linear) and
    # with a monotone cubic through the cumulative curves
    from scipy.interpolate import PchipInterpolator
    ca, ck = cum(a24), cum(k24)
    za_p = float(PchipInterpolator(ca, e24)(A97))
    r["ash_pchip"] = (C97 - float(PchipInterpolator(e24, ck)(za_p))) * f
    r["fixed_50"] = (k97[e97[1:] <= 50].sum() - amount_to(e24, k24, 50)) * f
    return r


def routes(target):
    pts, c97, c24 = load(target)
    per_point = {}
    for p in pts:
        per_point[p["point_1997"]] = dict(unit=p["unit_code"], **point_routes(p, c97[p["point_1997"]],
                                                                               c24[p["point_2024"]]))
    units = {}
    for code in K.UNIT_CODES:
        rs = [v for v in per_point.values() if v["unit"] == code]
        units[code] = {k: float(np.mean([r[k] for r in rs])) for k in rs[0] if k != "unit" and rs[0][k] is not None}
    return per_point, units


def ranking(units, key):
    order = sorted(units, key=lambda c: -units[c][key])
    v = [units[c][key] for c in order]
    return dict(order=order, top3=order[:3], line=v[2] / v[3] if v[3] > 0 else float("inf"))


# ------------------------------------------------------------------------------------------------ the asks
def ask_lowering(target, same_place_m=1.0, offset=K.DATUM_OFFSET_M):
    """Ask A: each unit's surface lowering, mm per year, mean over its grid points of the fall of the surface at the
    point between the 1997 levelling and the 2024 survey, the 1997 level brought to current NAP."""
    rows = read_csv(os.path.join(target, K.FILES["grid"]))
    g = {}
    for r in rows:
        g.setdefault((r["unit_code"], r["grid_point"]), {})[r["campaign"]] = r
    per = {c: [] for c in K.UNIT_CODES}
    for (code, gp), d in g.items():
        if "1997" not in d or "2024" not in d:
            continue
        a, b = d["1997"], d["2024"]
        dist = np.hypot(num(a["x_rd"]) - num(b["x_rd"]), num(a["y_rd"]) - num(b["y_rd"]))
        if same_place_m is not None and dist > same_place_m:
            continue
        yrs = (dt.date.fromisoformat(b["survey_date"]) - dt.date.fromisoformat(a["survey_date"])).days / 365.25
        fall = (num(a["level_m"]) - offset) - num(b["level_m"])
        per[code].append(1000.0 * fall / yrs)
    return {c: float(np.mean(v)) for c, v in per.items()}


def ask_glg(target, tube_history=True, hand_fill=True):
    """Ask B: each unit's GLG, cm below the surface, hydrological years 2017/18 to 2024/25."""
    meta = {r["dipwell_id"]: r for r in read_csv(os.path.join(target, K.FILES["dw_meta"]))}
    hist = {}
    for r in read_csv(os.path.join(target, K.FILES["dw_maint"])):
        if r["action"] == "tube replaced" and tube_history:
            m = re.search(r"top ([\d.]+) m above surface \(was ([\d.]+) m\)", r["note"])
            hist[r["dipwell_id"]] = (dt.date.fromisoformat(r["date"]), float(m.group(2)))
    logger, hand = {}, {}
    with open(os.path.join(target, K.FILES["dw_series"]), encoding="utf-8") as fh:
        rd = csv.DictReader(fh)
        for r in rd:
            day = r["date_time"][:10]
            if int(day[8:10]) not in (14, 28):
                continue
            if r["source"] == "logger":
                logger[(r["dipwell_id"], day)] = num(r["depth_below_tube_top_cm"])
            else:
                hand[(r["dipwell_id"], day)] = num(r["depth_below_tube_top_cm"])
    out = {}
    for dw, m in meta.items():
        top_now = num(m["tube_top_above_surface_m"])
        years = []
        for y in range(2017, 2025):
            vals = []
            day = dt.date(y, 4, 1)
            while day <= dt.date(y + 1, 3, 31):
                if day.day in (14, 28):
                    key = (dw, day.isoformat())
                    v = logger.get(key)
                    if v is None and hand_fill:
                        v = hand.get(key)
                    if v is not None:
                        top = top_now
                        if dw in hist and day < hist[dw][0]:
                            top = hist[dw][1]
                        vals.append(v - 100.0 * top)
                day += dt.timedelta(1)
            vals.sort(reverse=True)
            years.append(float(np.mean(vals[:3])))
        out[dw] = (m["unit_code"], float(np.mean(years)))
    units = {}
    for c in K.UNIT_CODES:
        units[c] = float(np.mean([v for (u, v) in out.values() if u == c]))
    return units, out


if __name__ == "__main__":
    import sys
    target = sys.argv[1]
    pp, units = routes(target)
    for key in ("ash", "ash_pchip", "subsidence", "subsidence_20", "subsidence_24", "level", "mass", "fixed",
                "fixed_50"):
        R = ranking(units, key)
        print("%-14s line %.2f | %s" % (key, R["line"], " ".join("%s:%.2f" % (K.UNIT_NAME[c][:6], units[c][key])
                                                                  for c in R["order"])))
    print("lowering A:", {K.UNIT_NAME[c][:6]: round(v, 1) for c, v in ask_lowering(target).items()})
    print("lowering mirror:", {K.UNIT_NAME[c][:6]: round(v, 1) for c, v in ask_lowering(target, None).items()})
    print("GLG:", {K.UNIT_NAME[c][:6]: round(v, 1) for c, v in ask_glg(target)[0].items()})
    print("GLG mirror:", {K.UNIT_NAME[c][:6]: round(v, 1) for c, v in ask_glg(target, False)[0].items()})

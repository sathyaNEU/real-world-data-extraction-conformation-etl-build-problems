"""An independent recomputation of the graded figures from target/ alone, by a second route: the surveys gridded onto
the plant grid (the December lattice interpolated onto contractor A's cells), the asks rebuilt from blocks of the
historian with each catch-up spread back over its outage in proportion to the shift log's readings."""
import csv
import datetime as dt
import json
import math
import os
import sys

import numpy as np
from scipy.interpolate import griddata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W   # noqa: E402

FI, UTC = W.FI, W.UTC


def read(target, name, delim=","):
    with open(os.path.join(target, name), encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=delim))


def asc(path):
    with open(path) as f:
        h = {}
        for _ in range(6):
            a, b = f.readline().split()
            h[a.lower()] = float(b)
        z = np.array([[float(v) for v in line.split()] for line in f if line.strip()])[::-1]
    z[z == h["nodata_value"]] = np.nan
    return h, z


def xyz(path):
    out = []
    with open(path, encoding="utf-8") as f:
        f.readline()
        for line in f:
            e, n, z = line.strip().split(";")
            out.append((float(e.replace(",", ".")), float(n.replace(",", ".")), float(z.replace(",", "."))))
    return np.array(out)


def main_call(target):
    reg = read(target, W.FILES["deliveries"])
    h, _ = asc(os.path.join(target, reg[0]["file"]))
    nx, ny, cs = int(h["ncols"]), int(h["nrows"]), h["cellsize"]
    gx = h["xllcorner"] + cs * (np.arange(nx) + 0.5)
    gy = h["yllcorner"] + cs * (np.arange(ny) + 0.5)
    GX, GY = np.meshgrid(gx, gy)
    a = math.radians(W.THETA_DEG)
    grids = {}
    for m, r in enumerate(reg):
        p = os.path.join(target, r["file"])
        if p.endswith(".asc"):
            grids[m] = asc(p)[1]
        else:
            pts = xyz(p)
            dE, dN = pts[:, 0] - W.E0, pts[:, 1] - W.N0
            x = W.X0 + math.cos(a) * dE + math.sin(a) * dN
            y = W.Y0 - math.sin(a) * dE + math.cos(a) * dN
            grids[m] = griddata((x, y), pts[:, 2] - W.DH, (GX, GY), method="linear")
    dec = len(reg) - 1
    areas = read(target, W.FILES["areas"])
    dens = []
    for r in read(target, W.FILES["density"]):
        v = float(r["bulk_density"])
        dens.append((r["sampled"], r["fuel_code"], v / 1000 if r["unit"] == "kg/m3" else v))
    per = {}
    for r in areas:
        xs = [float(r["x%d" % i]) for i in range(1, 5)]
        ys = [float(r["y%d" % i]) for i in range(1, 5)]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        own = (GX > x0 - 10) & (GX < x1 + 10) & (GY > y0 - 10) & (GY < y1 + 10)
        inner = (GX > x0 + 1) & (GX < x1 - 1) & (GY > y0 + 1) & (GY < y1 - 1)
        ring = own & ~((GX > x0 - 4) & (GX < x1 + 4) & (GY > y0 - 4) & (GY < y1 + 4))
        bare = [m for m in range(dec) if np.nanpercentile(grids[m][inner], 99.5) - np.nanmedian(grids[m][ring]) < 0.5]
        b = bare[-1]
        vol = float(np.nansum(np.clip(grids[dec][own] - grids[b][own], 0, None)) * cs * cs)
        rho = sorted(d for d in dens if d[1] == r["fuel_code"] and d[0] < "2026-12-16")[-1][2]
        per[r["pile_area"]] = (vol, vol * rho)
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(target, W.FILES["plan"]), data_only=True)["Coal burn Q1 2027"]
    t_sum = d_sum = 0
    for row in ws.iter_rows(min_row=5, values_only=True):
        if row[0] in ("January", "February", "March"):
            t_sum += row[5]
            d_sum += row[1]
    burn = t_sum / d_sum
    res = sum(v[1] for v in per.values())
    return per, res, res / burn


def series(target):
    v = {}
    for r in read(target, W.FILES["historian"]):
        v.setdefault(r["tag"], []).append((dt.datetime.strptime(r["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
                                           .replace(tzinfo=UTC).timestamp(), float(r["value"])))
    t = np.array([a for a, _ in v["SVL.CV01.WT15"]])
    return t, np.array([b for _, b in v["SVL.CV01.WT15"]]), np.array([b for _, b in v["SVL.CV21.WT15"]])


def run_spans(target):
    spans, on = [], None
    for r in read(target, W.FILES["gu1"]):
        ts = dt.datetime.fromisoformat(r["timestamp"]).timestamp()
        if r["event"] == "START":
            on = ts
        elif on is not None:
            spans.append((on, ts))
            on = None
    return spans


def runs_in(spans, a, b):
    return any(s < b and e > a for s, e in spans)


def spread(t, v, log_t, log_v, active=None):
    """Each impossible interval spread back over the zero run before it, shift by shift, in proportion to the
    shift log's totaliser differences; where `active` marks the intervals the belt could have carried coal in (the
    unloader running), only those receive it."""
    out = v.copy()
    for i in np.nonzero(v > 400)[0]:
        j = i
        while j > 0 and v[j - 1] == 0:
            j -= 1
        idx = list(range(j, i + 1))
        if active is not None and any(active[k] for k in idx):
            idx = [k for k in idx if active[k]]
        out[i] = 0.0
        bounds = sorted(set([t[j]] + [x for x in log_t if t[j] < x < t[i] + 900] + [t[i] + 900]))
        for c0, c1 in zip(bounds, bounds[1:]):
            s0 = max(k for k in range(len(log_t)) if log_t[k] <= c0)
            s1 = min(k for k in range(len(log_t)) if log_t[k] >= c1)
            dd = 0.0
            for k in range(s0, s1):
                d = log_v[k + 1] - log_v[k]
                dd += d if d >= 0 else log_v[k + 1]
            seg = (t >= log_t[s0]) & (t < log_t[s1])
            known = out[seg].sum()
            inside = [k for k in idx if c0 <= t[k] < c1]
            if inside:
                for k in inside:
                    out[k] += (dd - known) / len(inside)
    return out


def asks(target):
    t, v1, v21 = series(target)
    spans = run_spans(target)
    log = read(target, W.FILES["shiftlog"])
    log_t = np.array([dt.datetime.fromisoformat("%s %s" % (r["date"], r["reading_time"])).replace(tzinfo=FI)
                      .timestamp() for r in log])
    l01 = np.array([float(r["CV-01_totaliser_t"]) for r in log])
    l21 = np.array([float(r["CV-21_totaliser_t"]) for r in log])
    unl = np.array([runs_in(spans, a, a + 900) for a in t])
    f1 = spread(t, v1, log_t, l01, active=unl)
    f21 = spread(t, v21, log_t, l21)
    fuel = {r["contract"]: r["fuel_code"] for r in read(target, W.FILES["contracts"])}
    reg = read(target, W.FILES["deliveries"])
    lo = dt.datetime.fromisoformat("%s %s" % (reg[0]["survey_date"], reg[0]["flight_end"])).replace(tzinfo=FI).timestamp()
    hi = dt.datetime.fromisoformat("%s %s" % (reg[-1]["survey_date"], reg[-1]["flight_start"])).replace(
        tzinfo=FI).timestamp()
    rec = {}
    for r in read(target, W.FILES["berth"]):
        a = dt.datetime.strptime(r["commenced"], "%Y-%m-%dT%H:%MZ").replace(tzinfo=UTC).timestamp()
        b = dt.datetime.strptime(r["completed"], "%Y-%m-%dT%H:%MZ").replace(tzinfo=UTC).timestamp()
        if a < lo or b > hi:
            continue
        sel = (t + 900 > a) & (t < b) & unl
        rec[fuel[r["buyer_contract"]]] = rec.get(fuel[r["buyer_contract"]], 0.0) + float(f1[sel].sum())
    cross = (f1 > 0) & ~unl
    near = cross | np.roll(cross, 1) | np.roll(cross, -1)
    q = []
    for a, b in W.QUARTERS:
        sel = (t >= a.timestamp()) & (t < b.timestamp())
        q.append(float(f21[sel & ~near].sum()))
    return rec, q


def main(target, golden_dir=None):
    per, res, cover = main_call(target)
    rec, q = asks(target)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []
    for p in fig["piles"]:
        v, tn = per[p["area"]]
        if round(v / 1000) * 1000 != p["volume_m3"] or round(tn / 1000) * 1000 != p["tonnes"]:
            bad.append((p["area"], round(v), round(tn), p["volume_m3"], p["tonnes"]))
    if round(res / 1000) * 1000 != fig["call"]["reserve"] or round(cover) != fig["call"]["cover_days"]:
        bad.append(("reserve", round(res), round(cover, 2)))
    if (cover < W.FLOOR_DAYS) != fig["call"]["nominate"]:
        bad.append(("call", cover))
    for kk, v in fig["ask_a"].items():
        if round(rec[kk] / 1000) * 1000 != v:
            bad.append(("ask A", kk, round(rec[kk]), v))
    for i, (kk, v) in enumerate(fig["ask_b"].items()):
        if round(q[i] / 1000) * 1000 != v:
            bad.append(("ask B", kk, round(q[i]), v))
    if bad:
        raise SystemExit("verify: %s" % bad)
    print("verify: the plant-grid route reproduces every pile figure, the reserve (%.0f t, %.2f days), the call and "
          "every ask figure at the graded rounding" % (res, cover))


if __name__ == "__main__":
    main(os.path.join(os.path.dirname(HERE), "target"))

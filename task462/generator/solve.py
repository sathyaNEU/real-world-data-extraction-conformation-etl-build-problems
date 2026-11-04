"""The golden's own computation, from the shipped files only: the two contractors' surveys conformed onto the December
lattice, each pile area's December volume above the pad its own bare survey exposed, the reserve and its days of
cover; the easy routes beside it; and the two asks (receipts by coal between the surveys, deliveries by quarter)."""
import csv
import datetime as dt
import math
import os
import re

import numpy as np

import world as W

D = dt.timedelta
CT, ST = math.cos(math.radians(W.THETA_DEG)), math.sin(math.radians(W.THETA_DEG))


def P(target, key):
    return os.path.join(target, W.FILES[key])


def rows(target, key, delimiter=","):
    with open(P(target, key), encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=delimiter))


# ---------------------------------------------------------------------------------------------- readers
def read_asc(path):
    with open(path) as f:
        head = [next(f).split() for _ in range(6)]
        h = {k.lower(): float(v) for k, v in head}
        z = np.loadtxt(f)
    z = z[::-1].copy()
    z[z == h["nodata_value"]] = np.nan
    nx, ny, c = int(h["ncols"]), int(h["nrows"]), h["cellsize"]
    xs = h["xllcorner"] + c * (np.arange(nx) + 0.5) - W.X0
    ys = h["yllcorner"] + c * (np.arange(ny) + 0.5) - W.Y0
    return xs, ys, z


def read_xyz(path):
    with open(path, encoding="utf-8") as f:
        next(f)
        a = np.array([[float(v.replace(",", ".")) for v in line.strip().split(";")] for line in f if line.strip()])
    return a[:, 0], a[:, 1], a[:, 2]


def to_local(E, N):
    dE, dN = E - W.E0, N - W.N0
    return CT * dE + ST * dN, -ST * dE + CT * dN


def bilinear(xs, ys, z, x, y):
    fx = (x - xs[0]) / (xs[1] - xs[0])
    fy = (y - ys[0]) / (ys[1] - ys[0])
    i0 = np.clip(np.floor(fx).astype(int), 0, len(xs) - 2)
    j0 = np.clip(np.floor(fy).astype(int), 0, len(ys) - 2)
    tx, ty = np.clip(fx - i0, 0, 1), np.clip(fy - j0, 0, 1)
    return ((1 - tx) * (1 - ty) * z[j0, i0] + tx * (1 - ty) * z[j0, i0 + 1] + (1 - tx) * ty * z[j0 + 1, i0]
            + tx * ty * z[j0 + 1, i0 + 1])


def nearest(xs, ys, z, x, y):
    i = np.clip(np.round((x - xs[0]) / (xs[1] - xs[0])).astype(int), 0, len(xs) - 1)
    j = np.clip(np.round((y - ys[0]) / (ys[1] - ys[0])).astype(int), 0, len(ys) - 1)
    return z[j, i]


class Surveys:
    """Every survey sampled at the December survey's own points, in N60, in the plant grid's local frame."""

    def __init__(self, target, sampler=bilinear, datum=True):
        reg = rows(target, "deliveries")
        self.reg = reg
        dec = [r for r in reg if r["survey_date"].startswith("2026-12")][0]
        E, N, Z = read_xyz(os.path.join(target, dec["file"]))
        self.E, self.N = E, N
        self.x, self.y = to_local(E, N)
        self.z = {}
        key = {(round(e, 2), round(n, 2)): i for i, (e, n) in enumerate(zip(E, N))}
        for m, r in enumerate(reg):
            path = os.path.join(target, r["file"])
            if r["file"].endswith(".asc"):
                xs, ys, z = read_asc(path)
                self.z[m] = sampler(xs, ys, z, self.x, self.y)
            else:
                e, n, z = read_xyz(path)
                out = np.full(len(E), np.nan)
                for a, b, c in zip(e, n, z):
                    i = key.get((round(a, 2), round(b, 2)))
                    if i is not None:
                        out[i] = c
                self.z[m] = out - (W.DH if datum else 0.0)
        self.dec = len(reg) - 1
        self.dates = [r["survey_date"] for r in reg]


def areas(target):
    out = {}
    for r in rows(target, "areas"):
        xs = [float(r["x%d" % i]) - W.X0 for i in range(1, 5)]
        ys = [float(r["y%d" % i]) - W.Y0 for i in range(1, 5)]
        out[r["pile_area"]] = dict(coal=r["fuel_code"], x0=min(xs), x1=max(xs), y0=min(ys), y1=max(ys))
    return out


def in_area(a, x, y, pad=W.AREA_PAD):
    return (x > a["x0"] - pad) & (x < a["x1"] + pad) & (y > a["y0"] - pad) & (y < a["y1"] + pad)


def densities(target):
    out = []
    for r in rows(target, "density"):
        v = float(r["bulk_density"])
        out.append((r["sampled"], r["fuel_code"], v / 1000.0 if r["unit"].strip() == "kg/m3" else v))
    return out


def density_at(dens, coal, date):
    tests = sorted(t for t in dens if t[1] == coal and t[0] < date)
    return tests[-1][2]


def planned_burn(target):
    from openpyxl import load_workbook
    ws = load_workbook(P(target, "plan"), data_only=True)["Coal burn Q1 2027"]
    total = days = None
    for row in ws.iter_rows(min_row=5, values_only=True):
        if row[0] == "Quarter":
            days, total = row[1], row[5]
    return total / days, total, days


# ---------------------------------------------------------------------------------------------- the main call
def bare_survey(S, a, mask):
    """The latest survey before December in which the pile area held no pile (its highest point within the
    outline under half a metre above the pad around it)."""
    inner = in_area(a, S.x, S.y, pad=-1.0)
    ring = mask & ~in_area(a, S.x, S.y, pad=4.0)
    best = None
    for m in range(S.dec):
        z = S.z[m]
        ok = inner & ~np.isnan(z)
        if ok.sum() == 0:
            continue
        if np.nanmax(z[ok]) - np.nanmedian(z[ring]) < 0.5:
            best = m
    return best


def golden_volumes(S, A, base="bare"):
    out = {}
    zd = S.z[S.dec]
    allmin = np.nanmin(np.stack([S.z[m] for m in range(S.dec + 1)]), 0) if base == "min" else None
    for name, a in A.items():
        msk = in_area(a, S.x, S.y)
        m = bare_survey(S, a, msk)
        b = S.z[m] if base == "bare" else allmin
        th = zd[msk] - b[msk]
        out[name] = dict(volume=float(np.nansum(np.clip(th, 0, None)) * W.B_STEP ** 2), base=m)
    return out


def toe_volumes(S, A, kind="plane", ring=(1.6, 6.0)):
    from scipy.spatial import cKDTree
    out = {}
    zd = S.z[S.dec]
    for name, a in A.items():
        msk = in_area(a, S.x, S.y) & ~np.isnan(zd)
        xs, ys, zs = S.x[msk], S.y[msk], zd[msk]
        edge = ~in_area(a, xs, ys, pad=6.0)
        lvl = np.median(zs[edge])
        pile = zs > lvl + 0.25
        dd, _ = cKDTree(np.c_[xs[pile], ys[pile]]).query(np.c_[xs, ys])
        rg = (~pile) & (dd > ring[0]) & (dd < ring[1])
        if kind == "plane":
            c, *_ = np.linalg.lstsq(np.c_[xs[rg], ys[rg], np.ones(rg.sum())], zs[rg], rcond=None)
            basez = c[0] * xs + c[1] * ys + c[2]
        elif kind == "low":
            basez = zs[rg].min()
        elif kind == "mean":
            basez = zs[rg].mean()
        else:
            basez = W.PAD
        out[name] = dict(volume=float(np.clip(zs - basez, 0, None)[pile].sum() * W.B_STEP ** 2), base=None)
    return out


def reserve(target, vols, A=None, date=None):
    A = A or areas(target)
    dens = densities(target)
    date = date or "2026-12-16"
    per = {}
    for name, v in vols.items():
        rho = density_at(dens, A[name]["coal"], date)
        per[name] = dict(volume=v["volume"], density=rho, tonnes=v["volume"] * rho, base=v.get("base"))
    return per


def call(target, per):
    burn, total, days = planned_burn(target)
    res = sum(p["tonnes"] for p in per.values())
    cover = res / burn
    return dict(reserve=res, burn=burn, plan_total=total, plan_days=days, cover=cover,
                floor_t=W.FLOOR_DAYS * burn, margin_t=res - W.FLOOR_DAYS * burn, margin_days=cover - W.FLOOR_DAYS,
                nominate=cover < W.FLOOR_DAYS)


def monthly_stock(target, S, A):
    dens = densities(target)
    out = []
    bases = {}
    for name, a in A.items():
        msk = in_area(a, S.x, S.y)
        bases[name] = (msk, bare_survey(S, a, msk))
    for m in range(S.dec + 1):
        tot = 0.0
        for name, (msk, b) in bases.items():
            v = float(np.nansum(np.clip(S.z[m][msk] - S.z[b][msk], 0, None)) * W.B_STEP ** 2)
            tot += v * density_at(dens, A[name]["coal"], S.dates[m])
        out.append(tot)
    return out


# ---------------------------------------------------------------------------------------------- the asks
def parse_utc(s):
    return dt.datetime.strptime(s.replace("Z", ""), "%Y-%m-%dT%H:%M" if len(s) <= 17 else "%Y-%m-%dT%H:%M:%S"
                                ).replace(tzinfo=W.UTC)


def parse_local(s):
    return dt.datetime.fromisoformat(s)


def historian(target):
    h = {}
    for r in rows(target, "historian"):
        h.setdefault(r["tag"], []).append((parse_utc(r["timestamp"]), float(r["value"])))
    out = {}
    for tag, v in h.items():
        out[tag.split(".")[1]] = (np.array([t.timestamp() for t, _ in v]), np.array([x for _, x in v]))
    return out


def gu1_running(target, t_starts):
    """For each 15-minute interval start, whether GU-1 ran at any moment in it."""
    ev = [(parse_local(r["timestamp"]).timestamp(), r["event"]) for r in rows(target, "gu1")]
    run = np.zeros(len(t_starts), bool)
    on = None
    spans = []
    for t, e in ev:
        if e == "START":
            on = t
        elif on is not None:
            spans.append((on, t))
            on = None
    for a, b in spans:
        i0 = np.searchsorted(t_starts, a, side="right") - 1
        i1 = np.searchsorted(t_starts, b, side="left")
        run[max(i0, 0):i1] = True
    return run, spans


def blocks(v):
    nz = v > 0
    out, i = [], 0
    while i < len(v):
        if nz[i]:
            j = i
            while j < len(v) and nz[j]:
                j += 1
            out.append((i, j))
            i = j
        else:
            i += 1
    return out


def catchups(v, limit=400.0):
    """Intervals whose tonnage no belt can carry in a quarter hour, each with the zero run before it."""
    out = []
    for i in np.nonzero(v > limit)[0]:
        j = i
        while j > 0 and v[j - 1] == 0:
            j -= 1
        out.append((j, i))
    return out


def flights(target):
    out = []
    for r in rows(target, "deliveries"):
        a = dt.datetime.fromisoformat("%s %s" % (r["survey_date"], r["flight_start"])).replace(tzinfo=W.FI)
        b = dt.datetime.fromisoformat("%s %s" % (r["survey_date"], r["flight_end"])).replace(tzinfo=W.FI)
        out.append((a, b))
    return out


def ask_a(target, mode="golden"):
    """Receipts by coal between the December 2025 and December 2026 survey flights, as CV-01 weighed the unloader's
    coal. mode 'window' counts every CV-01 interval inside a call's berth window (the careful route)."""
    hist = historian(target)
    t, v1 = hist["CV01"]
    run, spans = gu1_running(target, t)
    contracts = {r["contract"]: r["fuel_code"] for r in rows(target, "contracts")}
    fl = flights(target)
    lo, hi = fl[0][1].timestamp(), fl[-1][0].timestamp()
    spikes = {i: j for j, i in catchups(v1)}
    out = {c: 0.0 for c in sorted(set(contracts.values()))}
    for r in rows(target, "berth"):
        a, b = parse_utc(r["commenced"]).timestamp(), parse_utc(r["completed"]).timestamp()
        if a < lo or b > hi:
            continue
        i0 = np.searchsorted(t, a, side="right") - 1
        i1 = np.searchsorted(t, b, side="left")
        tot = 0.0
        for i in range(i0, i1):
            if mode == "window" or run[i]:
                tot += v1[i]
        if mode == "golden":
            for i, j in spikes.items():
                if i0 <= j < i1 and i >= i1:      # the link fell while this call discharged and returned after it
                    tot += v1[i]
        out[contracts[r["buyer_contract"]]] += tot
    return out


def crossover_blocks(target):
    """CV-21 blocks that went to the crossover: they ran while CV-01 carried coal with the unloader stopped."""
    hist = historian(target)
    t, v1 = hist["CV01"]
    _, v21 = hist["CV21"]
    run, _ = gu1_running(target, t)
    x01 = [(a, b) for a, b in blocks(v1) if not run[a:b].any() and v1[a:b].max() < 400]
    out = []
    for a, b in blocks(v21):
        if v21[a:b].max() >= 400:
            continue
        if any(a < bb + 1 and aa < b + 1 for aa, bb in x01):
            out.append((a, b))
    return t, v21, out


def shiftlog(target):
    out = []
    for r in rows(target, "shiftlog"):
        ts = dt.datetime.fromisoformat("%s %s" % (r["date"], r["reading_time"])).replace(tzinfo=W.FI)
        out.append((ts, float(r["CV-01_totaliser_t"]), float(r["CV-21_totaliser_t"])))
    return out


def cv21_between(log, a, b):
    """CV-21's weighed tonnes between two shift readings, bridging the integrator's restart."""
    sel = [r for r in log if a <= r[0] <= b]
    tot = 0.0
    for p, q in zip(sel, sel[1:]):
        d = q[2] - p[2]
        tot += d if d >= 0 else q[2]
    return tot


def ask_b(target, mode="golden"):
    """Deliveries to the boiler house by calendar quarter of 2026 in Finnish time. mode 'shift' takes the shift
    log's CV-21 totals (the careful route, crossover moves included); 'historian' sums the historian's intervals by
    their own quarter."""
    log = shiftlog(target)
    t, v21, xb = crossover_blocks(target)
    if mode == "historian_fixed":
        v21 = respread(log, t, v21)
    out = []
    for a, b in W.QUARTERS:
        if mode in ("historian", "historian_fixed"):
            sel = (t >= a.timestamp()) & (t < b.timestamp())
            out.append(float(v21[sel].sum()))
            continue
        tot = cv21_between(log, a, b)
        if mode == "golden":
            for i, j in xb:
                if a.timestamp() <= t[i] < b.timestamp():
                    tot -= float(v21[i:j].sum())
        out.append(tot)
    return out


def respread(log, t, v21):
    """Each CV-21 catch-up returned to the shifts of its outage: each shift's totaliser difference in the shift log,
    less what the historian already holds for that shift, placed at the shift's first interval inside the outage."""
    v = v21.copy()
    lt = np.array([r[0].timestamp() for r in log])
    tot = np.array([r[2] for r in log])
    for j, i in catchups(v21):
        if i - j < 4:
            continue
        a, b = t[j], t[i] + 900.0
        p = int(np.searchsorted(lt, a, side="right") - 1)
        q = int(np.searchsorted(lt, b, side="left"))
        v[i] = 0.0
        for s in range(p, q):
            c0, c1 = lt[s], lt[s + 1]
            d = tot[s + 1] - tot[s]
            if d < 0:
                d = tot[s + 1]
            known = float(v[(t >= c0) & (t < c1)].sum())
            kk = int(np.searchsorted(t, max(c0, a)))
            v[kk] += d - known
    return v


def ask_b_window(target):
    """Deliveries to the boiler house between the two December flights, from the historian, crossover blocks out."""
    t, v21, xb = crossover_blocks(target)
    fl = flights(target)
    lo, hi = fl[0][1].timestamp(), fl[-1][0].timestamp()
    tot = float(v21[(t >= lo) & (t < hi)].sum())
    for i, j in xb:
        if lo <= t[i] < hi:
            tot -= float(v21[i:j].sum())
    return tot


def compute(target):
    A = areas(target)
    S = Surveys(target)
    g = reserve(target, golden_volumes(S, A))
    c = call(target, g)
    rungs = {}
    for k in ("plane", "low", "mean", "design"):
        rp = reserve(target, toe_volumes(S, A, kind=k))
        rungs["toe_" + k] = call(target, rp)
        rungs["toe_" + k]["per"] = rp
    gm = reserve(target, golden_volumes(S, A, base="min"))
    rungs["min_all"] = call(target, gm)
    rungs["min_all"]["per"] = gm
    return dict(per=g, call=c, rungs=rungs, S=S, A=A, monthly=monthly_stock(target, S, A),
                ask_a=ask_a(target), ask_b=ask_b(target))

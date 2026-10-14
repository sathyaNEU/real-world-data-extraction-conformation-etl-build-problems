"""The generating process: lots, the zoning each stood under, what stood on each and what it was worth, the
building that paid best each year, and the rebuilds; then every project's permits, buildings, occupancies,
strata plans and folios. Returns the clean truth as plain records (no shipped layout, no mess)."""
import datetime as dt

import numpy as np

import world as W

# ------------------------------------------------------------------------------------------------ helpers


def rng_for(*keys):
    h = W.SEED
    for k in keys:
        for ch in str(k):
            h = (h * 131 + ord(ch)) % 2147483647
    return np.random.default_rng(h)


def _nth(y, m, wd, n):
    d = dt.date(y, m, 1)
    d += dt.timedelta(days=(wd - d.weekday()) % 7)
    return d + dt.timedelta(days=7 * (n - 1))


def _easter(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    month = (h + l_ - 7 * m + 114) // 31
    day = ((h + l_ - 7 * m + 114) % 31) + 1
    return dt.date(y, month, day)


def holidays(y):
    """British Columbia statutory holidays the city's offices close for"""
    vic = dt.date(y, 5, 24)
    vic -= dt.timedelta(days=(vic.weekday() - 0) % 7)
    h = {dt.date(y, 1, 1), _easter(y) - dt.timedelta(days=2), vic, dt.date(y, 7, 1), _nth(y, 8, 0, 1), _nth(y, 9, 0, 1),
         _nth(y, 10, 0, 2), dt.date(y, 11, 11), dt.date(y, 12, 25), dt.date(y, 12, 26)}
    if y >= 2013:
        h.add(_nth(y, 2, 0, 2) if y < 2019 else _nth(y, 2, 0, 3))
    if y >= 2023:
        h.add(dt.date(y, 9, 30))
    return h


def working(d, forward=True):
    while d.weekday() >= 5 or d in holidays(d.year):
        d += dt.timedelta(days=1 if forward else -1)
    return d


def business_day(rng, y, lo=None, hi=None):
    lo = lo or dt.date(y, 1, 3)
    hi = hi or dt.date(y, 12, 22)
    span = (hi - lo).days
    return working(lo + dt.timedelta(days=int(rng.integers(0, span + 1))))


def add_months(d, m):
    return d + dt.timedelta(days=int(round(m * 30.44)))


GROUPS = {
    # group: kind, area kind of lot size, zone path (old codes by rezoning), lot size key
    "TOD_H": ("house", "house"), "TOD_C": ("comm", "comm"), "TOD_R": ("rental", "rental"),
    "CC_C": ("comm", "cc"), "CC_R": ("rental", "cc"),
    "TH": ("house", "house"), "CORR_H": ("house", "house"), "CORR_C": ("comm", "comm"), "CORR_R": ("rental", "rental"),
}


def zone_of(group, y):
    """old-scheme zone code in force for most of year y"""
    if group == "TOD_H":
        return "RS-1"
    if group in ("TOD_C", "CORR_C", "TOD_R", "CORR_R", "CORR_H"):
        return "CR-3"
    if group in ("CC_C", "CC_R"):
        return "C-3" if y < 2016 else "CD-CC"
    if group == "TH":
        return "RS-1" if y < 2019 else "RT-2"
    raise ValueError(group)


def zone_on_date(group, d):
    """old-scheme code in force on a date (the roll records the zone at its valuation date)"""
    if group == "TOD_H":
        return "RS-1"
    if group in ("TOD_C", "CORR_C", "TOD_R", "CORR_R", "CORR_H"):
        return "CR-3"
    if group in ("CC_C", "CC_R"):
        return "C-3" if d < W.REZONINGS["CC"][2] else "CD-CC"
    if group == "TH":
        return "RS-1" if d < W.REZONINGS["TH"][2] else "RT-2"
    raise ValueError(group)


def candidates(form, far):
    """(building type, FAR built) the zoning permits: wood types up to their typical FAR, towers at the maximum"""
    out = []
    if form in ("town", "apartment", "tower") and far >= 0.7:
        out.append(("TH3", min(1.2, far)))
    if form in ("apartment", "tower") and far >= 1.5:
        out.append(("LR4", min(2.0, far)))
        if far >= 3.0:
            out.append(("MR6", 3.0))
    if form == "tower" and far > 3.0:
        out.append(("HR", far))
    return out


def rlv(lot_area, area, btype, far, y):
    b = W.BTYPES[btype]
    return lot_area * far * (b["eff"] * W.value(area, b["product"], y) - W.cost(btype, y))


def homes_in(lot_area, btype, far):
    b = W.BTYPES[btype]
    return int(np.floor(lot_area * far * b["eff"] / b["nsf"] + 1e-9))


def best_building(lot_area, area, form, far, y):
    best = (None, 0.0, -np.inf)
    for t, f in candidates(form, far):
        r = rlv(lot_area, area, t, f, y)
        if r > best[2]:
            best = (t, f, r)
    return best


# ------------------------------------------------------------------------------------------------ lots


def make_lots():
    rng = rng_for("lots")
    lots = []

    def add(n, group, area, tier=0):
        kind, sizekey = GROUPS[group]
        for _ in range(int(round(n))):
            mu = W.LOT_MU[sizekey]
            a = float(np.clip(rng.lognormal(np.log(mu), 0.17), 3300, 39000))
            a = float(round(a / 5) * 5) if a < 20000 else float(round(a / 10) * 10)
            lp = W.LAND_PSF[area] * (1.04 if kind == "comm" and area != "CC" else 1.0)
            f = float(rng.lognormal(0, 0.08))
            rec = dict(group=group, kind=kind, area=area, tier=tier, a=a, lpsf=lp * f)
            if kind == "house":
                newer = rng.random() < 0.14
                rec["imp0"] = float(rng.uniform(550000, 1100000) if newer else rng.uniform(60000, 290000))
                rec["suite0"] = bool(rng.random() < 0.32)
                rec["built"] = int(rng.integers(2004, 2014) if newer else rng.integers(1948, 1996))
                rec["u0"] = 2 if rec["suite0"] else 1
            elif kind == "rental":
                fx = float(rng.uniform(1.2, 1.5))
                rec["imp0"] = float(rng.uniform(100, 140) * fx * a)
                rec["u0"] = int(a * fx * 0.80 / 760)
                rec["suite0"] = False
                rec["built"] = int(rng.integers(1962, 1986))
                rec["gfa0"] = round(a * fx)
            else:
                rec["imp0"] = float(rng.uniform(25, 105) * a)
                rec["u0"] = 0
                rec["suite0"] = False
                rec["built"] = int(rng.integers(1958, 1992))
            lots.append(rec)

    for st in W.STATIONS:
        for tier, n in W.TOD_BASE.items():
            n = n * W.TOD_SCALE
            add(n * (1 - W.TOD_SHARE["comm"] - W.TOD_SHARE["rental"]), "TOD_H", st, tier)
            add(n * W.TOD_SHARE["comm"], "TOD_C", st, tier)
            add(n * W.TOD_SHARE["rental"], "TOD_R", st, tier)
    add(W.CC_N["comm"], "CC_C", "CC")
    add(W.CC_N["rental"], "CC_R", "CC")
    for nb in W.NEIGHBOURHOODS:
        add(W.TH_N, "TH", nb)
        add(W.NB_CORR["house"], "CORR_H", nb)
        add(W.NB_CORR["comm"], "CORR_C", nb)
        add(W.NB_CORR["rental"], "CORR_R", nb)
    # a handful of large commercial sites (an acre or more) outside the station areas
    for nb, n in (("CC", 3), ("NC", 2), ("RAV", 2), ("FER", 1)):
        for _ in range(n):
            group = "CC_C" if nb == "CC" else "CORR_C"
            a = float(round(rng.uniform(44000, 96000) / 10) * 10)
            lots.append(dict(group=group, kind="comm", area=nb, tier=0, a=a,
                             lpsf=W.LAND_PSF[nb] * 0.92 * float(rng.lognormal(0, 0.06)),
                             imp0=float(rng.uniform(30, 70) * a), u0=0, suite0=False, built=int(rng.integers(1964, 1984))))
    # the station areas' remaining single-detached lots (drawn on their own stream)
    re_ = rng_for("lots-extra")
    tiers = [1] * 120 + [2] * 230 + [3] * 380
    for k in range(W.TOD_EXTRA_HOUSES):
        st = W.STATIONS[k % 4]
        tier = tiers[int(re_.integers(0, len(tiers)))]
        a = float(np.clip(re_.lognormal(np.log(W.LOT_MU["house"]), 0.17), 3300, 39000))
        a = float(round(a / 5) * 5)
        newer = re_.random() < 0.14
        suite0 = bool(re_.random() < 0.32)
        lots.append(dict(group="TOD_H", kind="house", area=st, tier=tier, a=a,
                         lpsf=W.LAND_PSF[st] * float(re_.lognormal(0, 0.08)),
                         imp0=float(re_.uniform(550000, 1100000) if newer else re_.uniform(60000, 290000)),
                         suite0=suite0, u0=2 if suite0 else 1,
                         built=int(re_.integers(2004, 2014) if newer else re_.integers(1948, 1996))))
    for i, rec in enumerate(lots):
        rec["lot_id"] = i
    ra = rng_for("additions")
    for rec in lots:
        if rec["group"] not in ("TOD_H", "TH") or rec["suite0"]:
            continue
        p_add = 0.0075 if rec["group"] == "TH" else 0.0015
        for y in W.YEARS:
            if ra.random() < p_add:
                d = business_day(ra, y)
                rec["add_year"] = y
                rec["add_date"] = d
                rec["add_kind"] = "suite" if ra.random() < 0.62 else "laneway"
                rec["add_done"] = add_months(d, float(ra.uniform(4, 9)))
                rec["add_imp"] = float(ra.uniform(55000, 90000) if rec["add_kind"] == "suite" else ra.uniform(240000, 330000))
                break
    return lots


# ------------------------------------------------------------------------------------------------ the record


def roll_values(lot, y, state):
    """assessed land and improvements on roll y (valuation 1 July y-1) for a lot still standing as it was"""
    r = rng_for("val", lot["lot_id"], y)
    up = 1.0
    g = lot["group"]
    rz = {"CC_C": "CC", "CC_R": "CC", "CORR_H": "CORR_H", "CORR_C": "CORR_C", "CORR_R": "CORR_R",
          "TOD_C": "CORR_C", "TOD_R": "CORR_R", "TH": "TH"}.get(g)
    if rz:
        eff = W.REZONINGS[rz][2]
        if dt.date(y - 1, 7, 1) >= eff:
            up = 1.12
    land = lot["a"] * lot["lpsf"] * W.LP[y] * up * (1 + r.uniform(-0.015, 0.015))
    imp = lot["imp0"] * W.IP[y] * (1 + r.uniform(-0.02, 0.02))
    if lot.get("add_done") and lot["add_done"] <= W.ROLL_CONDITION[y]:
        imp += lot["add_imp"] * W.IP[y]
    return float(round(land, -3)), float(round(imp, -3))


def units_on_roll(lot, y):
    """dwelling units standing on a house or rental lot at roll y's condition date"""
    u = lot["u0"]
    if lot.get("add_done") and lot["add_done"] <= W.ROLL_CONDITION[y]:
        u += 1
    return u


def simulate(lots):
    """the yearly record: each lot's zoning, best building, feasibility and rebuild year (permit issue year)"""
    rng = rng_for("events")
    N = len(lots)
    alive = np.ones(N, bool)
    cumN = {k: 0.0 for k in W.RATE}
    cumE = {k: 0 for k in W.RATE}
    rebuild = {}
    panel = []
    suites = {}
    for y in W.YEARS:
        feas = np.zeros(N, bool)
        rows = []
        for i, lot in enumerate(lots):
            if not alive[i]:
                continue
            code = zone_of(lot["group"], y)
            z = W.ZONES[code]
            far = z["far"](y)
            land, imp = roll_values(lot, y, None)
            t, f, r = best_building(lot["a"], lot["area"], z["form"], far, y)
            R = r / (land + imp) if t else float("nan")
            feas[i] = bool(t) and R > 1.0
            rows.append((i, code, far, t, f, r, land, imp, R))
        ev = np.zeros(N, bool)
        for k, rate in W.RATE.items():
            idx = np.array([i for i in range(N) if alive[i] and feas[i] and lots[i]["kind"] == k], int)
            cumN[k] += len(idx)
            target = int(round(rate * cumN[k] + rng.uniform(-W.JITTER, W.JITTER)))
            n = max(0, min(len(idx), target - cumE[k]))
            if n:
                pick = rng.choice(idx, n, replace=False)
                ev[pick] = True
            cumE[k] += n
        for (i, code, far, t, f, r, land, imp, R) in rows:
            panel.append(dict(lot_id=i, year=y, zone=code, far=far, btype=t, far_built=f, rlv=r, land=land, imp=imp,
                              R=R, feasible=bool(feas[i]), event=bool(ev[i])))
            if ev[i]:
                rebuild[i] = dict(year=y, btype=t, far=f, homes=homes_in(lots[i]["a"], t, f))
        alive &= ~ev
    return panel, rebuild, alive

"""task401 clean truth: Larkspur Hills Grain Ltd., west-central Saskatchewan, canola seasons 2020 to 2026.

Everything downstream (the pack, the goldens, the checks) reads this module's `build()` result. No mess is applied
here: the world before any export or document exists.

Truth, by design:
  - the new hybrid's own yield effect is nil; both hybrids reach first flower at the same heat units after seeding;
  - in 2026 the hybrid's seed reached most of the yards that ordered it late, so its fields there were seeded after it
    arrived, about ten days after the incumbent's;
  - a heat wave from 10 to 18 July 2026 harmed canola only while a field was in flower;
  - a dry June cut every field a little.
"""
import datetime as dt

import numpy as np

SEED = 401_2026
SEASONS = list(range(2020, 2027))
BASE_C = 5.0             # growing degree days, base 5 C (daily mean of max and min)
TT_FLOWER = 520.0        # heat units from seeding to first flower, both hybrids
TT_SD = 18.0             # field-to-field spread of that target
FLOWER_DAYS = 18         # days in flower from first flower
HEAT_THR = 29.5          # C, daily maximum above which flowers abort
HEAT_K = 0.018           # yield loss rate per degree day above the threshold while in flower
HYBRID_EFFECT = 0.0      # the new hybrid's own effect on yield
INCUMBENT, HYBRID = "Northline 3150", "Bracken 4720 CR"
HEAT_WAVE_START, HEAT_WAVE_DAYS = (2026, 7, 24), 9     # 24 July to 1 August 2026
# Monthly normals at mid-month for west-central Saskatchewan (daily maximum, and the day's range), C
TMAX_NORMAL = np.array([-12.0, -9.0, -2.0, 10.0, 18.5, 23.0, 25.5, 25.0, 18.5, 10.0, -1.0, -9.0])
DTR_NORMAL = np.array([11.0, 11.0, 11.0, 13.0, 14.5, 13.5, 13.5, 14.5, 14.0, 12.5, 10.0, 11.0])

ZONES = ("Dark Brown", "Black")
STATIONS = [  # name, lat, lon, zone; invented sites
    ("Larkspur Hills", 51.86, -108.42, "Dark Brown"),
    ("Tessaly", 51.42, -108.95, "Dark Brown"),
    ("Corbin Flats", 51.63, -109.41, "Dark Brown"),
    ("Vennick", 52.07, -109.12, "Dark Brown"),
    ("Ardmuir", 51.30, -107.88, "Dark Brown"),
    ("Pellatt", 52.36, -108.20, "Black"),
    ("Strand Lake", 52.58, -107.64, "Black"),
    ("Kelvey", 52.21, -107.31, "Black"),
    ("Orrin", 52.71, -108.66, "Black"),
    ("Mossbank Creek", 52.45, -106.98, "Black"),
]


def doy(y, m, d):
    return dt.date(y, m, d).timetuple().tm_yday


def _weather(r):
    """Daily Tmax, Tmin (C) and precipitation (mm) for each station and season, 1 January to 31 December."""
    out = {}
    for y in SEASONS:
        nd = 366 if y % 4 == 0 else 365
        t = np.arange(1, nd + 1)
        syn = np.zeros(nd)
        e = 0.0
        for i in range(nd):
            e = 0.78 * e + r.normal(0, 2.1)
            syn[i] = e
        spells = []
        if y == 2026:
            spells.append((doy(*HEAT_WAVE_START), HEAT_WAVE_DAYS, {"Dark Brown": 7.0, "Black": 5.6}))
        else:
            for _ in range(int(r.integers(0, 3))):
                spells.append((int(r.integers(doy(y, 6, 10), doy(y, 8, 20))), int(r.integers(3, 7)),
                               {"Dark Brown": r.uniform(3.0, 6.0), "Black": r.uniform(2.4, 5.0)}))
        june_dry = 0.55 if y == 2026 else float(np.clip(r.normal(1.0, 0.25), 0.5, 1.6))
        mid = np.array([doy(y, m, 15) for m in range(1, 13)])
        tmax_n = np.interp(t, np.r_[mid[-1] - nd, mid, mid[0] + nd], np.r_[TMAX_NORMAL[-1], TMAX_NORMAL, TMAX_NORMAL[0]])
        dtr_n = np.interp(t, np.r_[mid[-1] - nd, mid, mid[0] + nd], np.r_[DTR_NORMAL[-1], DTR_NORMAL, DTR_NORMAL[0]])
        for s, (name, lat, lon, zone) in enumerate(STATIONS):
            clim = tmax_n + (0.7 if zone == "Dark Brown" else -0.5) - 0.8 * (lat - 51.8)
            loc = np.zeros(nd)
            e = 0.0
            for i in range(nd):
                e = 0.55 * e + r.normal(0, 1.2)
                loc[i] = e
            tmax = clim + syn + loc
            for d0, ln, amp in spells:
                m = (t >= d0) & (t < d0 + ln)
                tmax[m] += amp[zone] * (1 + 0.12 * r.normal()) * np.sin(np.linspace(0.35, np.pi - 0.35, int(m.sum()))) + 1.5
            tmin = tmax - (dtr_n + r.normal(0, 1.6, nd))
            wet = r.random(nd) < np.where((t > 120) & (t < 250), 0.28, 0.18)
            pr = np.where(wet, r.gamma(0.9, 5.5, nd), 0.0)
            jun = (t >= doy(y, 6, 1)) & (t <= doy(y, 6, 30))
            pr[jun] *= june_dry * (1 + 0.15 * r.normal())
            out[(y, s)] = dict(tmax=np.round(tmax, 1), tmin=np.round(tmin, 1), precip=np.round(np.maximum(pr, 0), 1))
    return out


def gdd(w, start_doy):
    tmean = (w["tmax"] + w["tmin"]) / 2.0
    g = np.maximum(tmean - BASE_C, 0.0)
    return g, start_doy


def first_flower(w, seed_doy, target):
    """Day of year when heat units from the day after seeding reach the target."""
    tmean = (w["tmax"] + w["tmin"]) / 2.0
    g = np.maximum(tmean - BASE_C, 0.0)
    c = np.cumsum(g[seed_doy:])          # index seed_doy is the day after seeding (doy is 1-based)
    k = int(np.searchsorted(c, target))
    return seed_doy + 1 + k


def heat_in_flower(w, flower_doy, days=FLOWER_DAYS, thr=HEAT_THR):
    i0 = flower_doy - 1
    return float(np.maximum(w["tmax"][i0:i0 + days] - thr, 0.0).sum())


def _yards(r):
    yards = []
    for i in range(31):
        s = int(r.integers(0, len(STATIONS)))
        name, lat, lon, zone = STATIONS[s]
        yards.append(dict(yard=i, lat=lat + r.normal(0, 0.12), lon=lon + r.normal(0, 0.18), zone=zone))
    for y in yards:   # nearest station
        d = [((y["lat"] - st[1]) * 111.0) ** 2 + ((y["lon"] - st[2]) * 68.0) ** 2 for st in STATIONS]
        y["station"] = int(np.argmin(d))
        y["zone"] = STATIONS[y["station"]][3]
    return yards


def build(seed=SEED, heat_start=None):
    global HEAT_WAVE_START
    if heat_start is not None:
        HEAT_WAVE_START = heat_start
    r = np.random.default_rng(seed)
    W = _weather(r)
    yards = _yards(r)
    pot_zone = {"Dark Brown": 38.0, "Black": 47.0}
    fields = []
    fid = 0
    for yd in yards:
        n = int(r.integers(22, 36))
        for k in range(n):
            fields.append(dict(field=fid, yard=yd["yard"], acres=float(np.clip(r.normal(165, 55), 60, 480)),
                               pot=pot_zone[yd["zone"]] * float(np.exp(r.normal(0, 0.06))),
                               phase=int(r.integers(0, 3))))
            fid += 1
    # 2026: which yards took the hybrid, and when its seed arrived
    took = r.random(len(yards)) < 0.6
    share = np.clip(r.normal(0.62, 0.15, len(yards)), 0.25, 0.95)
    late = r.random(len(yards)) < 0.72
    arrive = {}
    for yd in yards:
        if took[yd["yard"]]:
            arrive[yd["yard"]] = doy(2026, 5, 20) + int(r.integers(0, 9)) if late[yd["yard"]] else doy(2026, 4, 9) + int(r.integers(0, 6))
    rows = []
    for y in SEASONS:
        s_year = r.normal(0, 0.05)
        s_zone = {z: r.normal(0, 0.04) for z in ZONES}
        start_shift = r.normal(0, 3.0)
        for yd in yards:
            w = W[(y, yd["station"])]
            canola = [f for f in fields if f["yard"] == yd["yard"] and (y + f["phase"]) % 3 == 0]
            if not canola:
                continue
            r.shuffle(canola)
            start = doy(y, 5, 2) + int(round(start_shift + r.normal(0, 2.0) + (2 if yd["zone"] == "Black" else 0)))
            pace = r.uniform(1.0, 1.6)          # canola fields seeded per day at this yard
            hyb = np.zeros(len(canola), dtype=int)
            if y == 2026 and took[yd["yard"]]:
                hyb[: int(round(share[yd["yard"]] * len(canola)))] = 1
                r.shuffle(hyb)
            elif y == 2025:
                hyb = (r.random(len(canola)) < 0.06).astype(int)
            order_inc = [i for i in range(len(canola)) if not hyb[i]]
            order_hyb = [i for i in range(len(canola)) if hyb[i]]
            seed_day = {}
            day = float(start)
            if y == 2026 and took[yd["yard"]] and late[yd["yard"]]:
                for i in order_inc:
                    seed_day[i] = int(day); day += 1.0 / pace
                day = max(day, arrive[yd["yard"]] + 1.0)
                for i in order_hyb:
                    seed_day[i] = int(day); day += 1.0 / pace
            else:
                for i in sorted(range(len(canola)), key=lambda _: r.random()):
                    seed_day[i] = int(day); day += 1.0 / pace
            for i, f in enumerate(canola):
                sd = seed_day[i]
                tt = TT_FLOWER + r.normal(0, TT_SD)
                fl = first_flower(w, sd, tt)
                hf = heat_in_flower(w, fl)
                heat_loss = 1.0 - np.exp(-HEAT_K * hf)
                jun = w["precip"][doy(y, 6, 1) - 1: doy(y, 6, 30)].sum()
                dry = (max(jun, 8.0) / 62.0) ** 0.12
                yld = f["pot"] * np.exp(s_year + s_zone[yd["zone"]]) * (1 - heat_loss) * dry
                yld *= (1 + HYBRID_EFFECT * hyb[i]) * float(np.exp(r.normal(0, 0.09)))
                rows.append(dict(season=y, field=f["field"], yard=yd["yard"], zone=yd["zone"], station=yd["station"],
                                 acres=f["acres"], hybrid=int(hyb[i]), variety=HYBRID if hyb[i] else INCUMBENT,
                                 seed_doy=sd, flower_doy=fl, heat_flower=hf, heat_loss=heat_loss, june_mm=jun,
                                 yield_bu=yld))
    return dict(weather=W, yards=yards, fields=fields, rows=rows, arrive=arrive, took=took, late=late)

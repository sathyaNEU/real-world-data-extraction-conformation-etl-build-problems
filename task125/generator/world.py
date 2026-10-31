"""The Umzimela catchment's 2025/26 hydrological year: rivers, gauges, monitors, mines and the water they carry.

Every quantity is generated from one process: daily rain drives each inflow's flow; each mine stream carries the
colliery's discharge and the seepage around it; sulfate is conservative, so a resource unit's water past its lower
boundary carries exactly what its inflows bring in; and a boundary monitor set within a few kilometres of a mine
stream's confluence samples water that has not mixed across the channel, the near bank carrying more of the mine
stream and the far bank more of the main river."""
import datetime as dt
import math

import numpy as np

SEED = 125_3
YEAR0 = dt.date(2025, 10, 1)          # the hydrological year, October to September
YEAR1 = dt.date(2026, 9, 30)
DAYS = [YEAR0 + dt.timedelta(days=i) for i in range((YEAR1 - YEAR0).days + 1)]
DRY0, DRY1 = dt.date(2026, 5, 1), dt.date(2026, 9, 30)
CONV = 0.0864                          # mg/L x m3/s -> tonnes per day
S_TO_SO4 = 96.06 / 32.06               # sulfate expressed as S -> as SO4


def rng(tag):
    import zlib
    return np.random.default_rng((SEED * 1_000_003 + zlib.crc32(tag.encode())) % (2 ** 32))


# ------------------------------------------------------------------ the network
# resource units, upstream to downstream; inflows are other units whose water enters at the unit's upper end
RU = [
    # code,  river,              name,                         inflows,          weir,  allocation t/d
    ("MZ1", "Mzimela River",    "Upper Mzimela",              [],                "W01", 8.0),
    ("KH1", "Khambule Stream",  "Khambule",                   [],                "W02", 16.0),
    ("MZ2", "Mzimela River",    "Mzimela at Esikhotheni",     ["MZ1", "KH1"],    "W03", 32.0),
    ("MZ3", "Mzimela River",    "Mzimela Middle",             ["MZ2"],           "W04", 32.0),
    ("SW1", "Silwane Stream",   "Silwane",                    [],                "W05", 15.0),
    ("MZ4", "Mzimela River",    "Mzimela at Ngwelezane Drift", ["MZ3", "SW1"],    "W06", 34.0),
    ("GB1", "Gubhu River",      "Gubhu",                      [],                "W07", 3.0),
    ("MZ5", "Mzimela River",    "Lower Mzimela",              ["MZ4", "GB1"],    "W08", 46.0),
    ("NY1", "Nyathi River",     "Upper Nyathi",               [],                "W09", 16.0),
    ("NT1", "Ntsheketshe Stream", "Ntsheketshe",              [],                "W10", 23.0),
    ("NY2", "Nyathi River",     "Nyathi at Mabhokweni",       ["NY1", "NT1"],    "W11", 35.0),
    ("MP1", "Mpafa Stream",     "Mpafa",                      [],                "W12", 15.0),
    ("NY3", "Nyathi River",     "Nyathi at Siphethu",         ["NY2", "MP1"],    "W13", 58.0),
    ("NY4", "Nyathi River",     "Lower Nyathi",               ["NY3"],           "W14", 58.0),
]
RU_BY = {r[0]: r for r in RU}
ORDER = [r[0] for r in RU]

# boundary monitors inside a confluence's lateral mixing zone: (bank the monitor stands on, side the mine stream
# enters, km below the confluence); every other boundary monitor stands where the river is mixed
MINE_STREAM = {"MZ2": "KH1", "MZ4": "SW1", "NY2": "NT1", "NY3": "MP1"}
MIXING = {"MZ2": ("left", "left", 2.6, 1.45), "MZ4": ("right", "left", 3.1, 0.20),
          "NY2": ("left", "right", 2.2, 0.60), "NY3": ("right", "right", 1.8, 2.60)}

# headwater and tributary units: (base dry-season flow m3/s, wet-season multiplier, sulfate at base flow mg/L,
# dilution exponent); a mine stream's sulfate falls as rain adds clean water
SOURCES = {
    "MZ1": (1.55, 3.4, 31.0, 0.15),
    "KH1": (0.105, 2.6, 2310.0, 0.62),
    "SW1": (0.100, 2.4, 1352.0, 0.55),
    "GB1": (0.82, 3.1, 14.0, 0.10),
    "NY1": (1.12, 3.2, 116.2, 0.20),
    "NT1": (0.148, 2.5, 1890.0, 0.60),
    "MP1": (0.080, 2.3, 1616.0, 0.58),
}

# mines and their licensed discharge points (each discharges into a mine stream's unit)
MINES = [
    ("Khambule Colliery (Pty) Ltd", "KHC", [("KHC-DP1", "KH1", 0.046), ("KHC-DP2", "KH1", 0.021)]),
    ("Silwane Anthracite Mine", "SAM", [("SAM-DP1", "SW1", 0.038)]),
    ("Ntsheketshe Coal Holdings", "NCH", [("NCH-DP1", "NT1", 0.071), ("NCH-DP2", "NT1", 0.034)]),
    ("Mpafa Mining Company", "MMC", [("MMC-DP1", "MP1", 0.029)]),
]
# the commercial laboratory three of the mines use reported sulfate as S from its November 2025 batches
LAB_AS_S_FROM = dt.date(2025, 11, 1)
LAB_AS_S_MINES = {"KHC", "NCH", "MMC"}
METER_SWAP = ("SAM-DP1", dt.date(2026, 2, 14))   # the flow totaliser replaced at an inspection


def rain():
    """daily rainfall (mm) at the catchment's representative gauge: summer thunderstorms, a dry winter"""
    r = rng("rain")
    out = []
    for d in DAYS:
        m = d.month
        wet = {10: 0.32, 11: 0.45, 12: 0.52, 1: 0.55, 2: 0.50, 3: 0.42, 4: 0.25, 5: 0.08, 6: 0.04, 7: 0.03,
               8: 0.05, 9: 0.10}[m]
        if r.random() < wet:
            out.append(round(float(r.gamma(0.9, 9.0 if m in (11, 12, 1, 2) else 5.5)), 1))
        else:
            out.append(0.0)
    return out


def flows(rain_mm):
    """daily mean flow of each source unit (m3/s) from a two-store response to rain"""
    out = {}
    for code, (base, wetx, c0, ex) in SOURCES.items():
        r = rng("flow-" + code)
        slow, quick = base * wetx * 0.55, 0.0
        q = []
        for i, d in enumerate(DAYS):
            p = rain_mm[i] * (0.8 + 0.4 * r.random())
            quick = quick * 0.55 + base * 0.045 * p
            # the slow store recedes towards the dry-season base through winter
            target = base * (wetx if d.month in (11, 12, 1, 2, 3) else (1.6 if d.month in (10, 4) else 1.0))
            slow = slow + 0.035 * (target - slow) + base * 0.004 * p
            q.append(max(slow + quick, base * 0.55))
        out[code] = np.array(q)
    return out


def concentrations(q):
    """daily sulfate (mg/L) of each source unit's mixed water"""
    out = {}
    for code, (base, wetx, c0, ex) in SOURCES.items():
        r = rng("conc-" + code)
        drift = np.cumsum(r.normal(0, 0.004, len(DAYS)))
        c = c0 * (base / q[code]) ** ex * np.exp(drift - drift.mean())
        out[code] = c
    return out


def simulate():
    rain_mm = rain()
    q = flows(rain_mm)
    c = concentrations(q)
    Q, C = dict(q), dict(c)
    L = {k: C[k] * Q[k] * CONV for k in SOURCES}
    gauge_noise = {}
    for code, river, name, inflows, weir, alloc in RU:
        if code in SOURCES:
            continue
        qin = sum(Q[i] for i in inflows)
        lin = sum(L[i] for i in inflows)
        Q[code] = qin
        L[code] = lin
        C[code] = lin / (qin * CONV)
    for code in ORDER:
        r = rng("gauge-" + code)
        gauge_noise[code] = 1.0 + r.normal(0, 0.0035, len(DAYS))
    return dict(rain=rain_mm, Q=Q, C=C, L=L, gauge_noise=gauge_noise)


def point_concentration(code, day_index, Q, C, run_rng):
    """the boundary monitor's sulfate on one run: the section's mixed water where the river is mixed, and within a
    confluence's mixing zone the blend of the two inflows the monitor's bank carries, the mine stream's water making
    up k times its share of the flow at the near bank and k times it at the far bank (k under 1)"""
    if code not in MIXING:
        return C[code][day_index] * (1.0 + run_rng.normal(0, 0.006))
    bank, side, km, k = MIXING[code]
    inflows = RU_BY[code][3]
    trib = MINE_STREAM[code]
    main = [i for i in inflows if i != trib][0]
    qt, qm = Q[trib][day_index], Q[main][day_index]
    f = qt / (qt + qm)
    w = min(0.97, max(0.0, f * k * (1.0 + run_rng.normal(0, 0.06))))
    return (1.0 - w) * C[main][day_index] + w * C[trib][day_index]


def runs():
    """the routine sampling runs: every second Tuesday from 7 October 2025"""
    d = dt.date(2025, 10, 7)
    out = []
    while d <= YEAR1:
        out.append(d)
        d += dt.timedelta(days=14)
    return out

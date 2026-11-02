"""task484 architecture 4: the world before any export or document is written (the clean truth).

Wrenford (a fictional unitary borough in the West Midlands): 2025 traffic on the road sections the council
counted for the noise mapping round, its permanent automatic counters and its urban traffic control (UTC)
detectors. Everything is drawn from one fixed seed; nothing here reads target/.
"""
import datetime as dt
import math

import numpy as np

SEED = 484
YEAR = 2025
DAYS = [dt.date(YEAR, 1, 1) + dt.timedelta(i) for i in range(365)]
DIDX = {d: i for i, d in enumerate(DAYS)}
THRESHOLD = 3_000_000                      # vehicle passages in the year (the round's line)

BANK_HOLIDAYS = [dt.date(2025, 1, 1), dt.date(2025, 4, 18), dt.date(2025, 4, 21), dt.date(2025, 5, 5),
                 dt.date(2025, 5, 26), dt.date(2025, 8, 25), dt.date(2025, 12, 25), dt.date(2025, 12, 26)]
SCHOOL_HOLIDAYS = [(dt.date(2025, 1, 1), dt.date(2025, 1, 3)), (dt.date(2025, 2, 17), dt.date(2025, 2, 21)),
                   (dt.date(2025, 4, 7), dt.date(2025, 4, 21)), (dt.date(2025, 5, 26), dt.date(2025, 5, 30)),
                   (dt.date(2025, 7, 23), dt.date(2025, 9, 2)), (dt.date(2025, 10, 27), dt.date(2025, 10, 31)),
                   (dt.date(2025, 12, 22), dt.date(2025, 12, 31))]
UNI_VACATIONS = [(dt.date(2025, 1, 1), dt.date(2025, 1, 12)), (dt.date(2025, 3, 29), dt.date(2025, 4, 27)),
                 (dt.date(2025, 6, 7), dt.date(2025, 9, 21)), (dt.date(2025, 12, 13), dt.date(2025, 12, 31))]
SHUTDOWNS = [(dt.date(2025, 1, 1), dt.date(2025, 1, 3)), (dt.date(2025, 8, 4), dt.date(2025, 8, 15)),
             (dt.date(2025, 12, 22), dt.date(2025, 12, 31))]
SNOW_DAYS = {dt.date(2025, 1, 9): -0.17, dt.date(2025, 1, 10): -0.11}
FIRMWARE_PUSH = dt.date(2025, 9, 8)        # the TX-200 outstations leave legacy class output on this day


def in_ranges(d, ranges):
    return any(a <= d <= b for a, b in ranges)


# ---------------------------------------------------------------------------------------------------------
# Daily rhythm of each kind of road (unnormalised multiplier) and its 07:00-19:00 share of the day.
# ---------------------------------------------------------------------------------------------------------
MONTH_COMMUTER = {1: 0.94, 2: 0.97, 3: 0.99, 4: 1.00, 5: 1.01, 6: 1.02, 7: 1.00, 8: 0.95, 9: 1.01, 10: 1.02,
                  11: 1.01, 12: 0.98}
MONTH_INTERURBAN = {1: 0.92, 2: 0.95, 3: 0.98, 4: 1.01, 5: 1.03, 6: 1.04, 7: 1.07, 8: 1.08, 9: 1.02, 10: 1.00,
                    11: 0.97, 12: 0.95}
MONTH_RETAIL = {1: 0.97, 2: 0.92, 3: 0.97, 4: 1.00, 5: 1.00, 6: 1.00, 7: 1.02, 8: 1.03, 9: 0.97, 10: 1.00,
                11: 1.10, 12: 1.30}


def rhythm(kind, d, var=None):
    """Multiplier of a road of this kind on day d; var holds a site's own small departures."""
    v = var or {}
    w, m = d.weekday(), d.month
    bh = d in BANK_HOLIDAYS
    if kind == "commuter":
        f = [1.00, 1.02, 1.03, 1.03, 1.05, 0.84 + v.get("sat", 0), 0.70 + v.get("sun", 0)][w]
        if w < 5 and in_ranges(d, SCHOOL_HOLIDAYS):
            f *= 0.93
        f *= MONTH_COMMUTER[m] + v.get("mon_" + str(m), 0)
        if bh:
            f *= 0.68
        if dt.date(2025, 12, 24) <= d <= dt.date(2025, 12, 31):
            f *= 0.80
    elif kind == "interurban":
        f = [1.00, 1.01, 1.01, 1.02, 1.08, 0.92 + v.get("sat", 0), 0.83 + v.get("sun", 0)][w]
        f *= MONTH_INTERURBAN[m]
        if bh:
            f *= 0.85
    elif kind == "retail":
        f = [0.80, 0.82, 0.84, 0.90, 1.02, 1.48, 1.18][w]
        f *= MONTH_RETAIL[m]
        if bh:
            f *= 1.25
        if d == dt.date(2025, 12, 25):
            f = 0.05
        if d == dt.date(2025, 4, 20):
            f *= 0.55
    elif kind == "industrial":
        f = [1.00, 1.02, 1.02, 1.01, 0.97, 0.36, 0.18][w]
        if in_ranges(d, SHUTDOWNS):
            f *= 0.33
        if bh:
            f *= 0.30
    elif kind == "school":
        f = [1.00, 1.00, 1.00, 1.00, 0.98, 0.50, 0.42][w]
        if w < 5 and in_ranges(d, SCHOOL_HOLIDAYS):
            f *= 0.56
        if bh:
            f *= 0.70
    elif kind == "university":
        f = [1.00, 1.00, 1.00, 0.98, 0.92, 0.55, 0.48][w]
        if w < 5 and in_ranges(d, UNI_VACATIONS):
            f *= 0.52
        if bh:
            f *= 0.80
    elif kind == "leisure":
        f = [0.82, 0.84, 0.86, 0.90, 1.05, 1.55, 1.30][w]
        if m in (7, 8):
            f *= 1.10
        if bh:
            f *= 1.30
    elif kind == "hospital":
        f = [1.00, 1.00, 1.00, 1.00, 0.99, 0.88, 0.85][w]
        if bh:
            f *= 0.86
    else:
        raise ValueError(kind)
    return f


R12 = {"commuter": 0.865, "interurban": 0.845, "retail": 0.905, "industrial": 0.745, "school": 0.900,
       "university": 0.835, "leisure": 0.715, "hospital": 0.780}


def r12(kind, d):
    base = R12[kind]
    if d.weekday() >= 5:
        base -= 0.025
    return base


# Hourly shape of each kind inside 07:00-19:00 (12 weights, hour beginning 07 to 18).
HOURLY = {
    "commuter":   [6.8, 9.6, 8.2, 7.1, 7.0, 7.3, 7.4, 7.6, 8.4, 9.9, 10.7, 10.0],
    "interurban": [7.4, 9.0, 8.0, 7.5, 7.6, 7.9, 8.0, 8.2, 8.7, 9.6, 9.9, 8.2],
    "retail":     [3.2, 5.0, 6.9, 8.6, 9.9, 10.6, 10.7, 10.2, 9.8, 9.2, 8.4, 7.5],
    "industrial": [12.9, 8.8, 6.6, 6.1, 6.0, 6.7, 11.4, 10.5, 7.1, 8.0, 9.4, 6.5],
    "school":     [6.0, 14.6, 7.2, 5.4, 5.3, 5.7, 6.1, 9.4, 12.8, 9.2, 10.3, 8.0],
    "university": [4.8, 9.4, 11.0, 8.7, 7.9, 8.6, 8.2, 7.7, 8.3, 9.4, 9.2, 6.8],
    "leisure":    [4.2, 5.6, 5.9, 6.4, 7.3, 8.0, 8.1, 8.5, 9.3, 10.6, 12.4, 13.7],
    "hospital":   [12.6, 9.8, 8.0, 7.5, 7.6, 7.7, 9.1, 8.9, 7.5, 7.8, 8.0, 5.5],
}


# ---------------------------------------------------------------------------------------------------------
# The sections counted in 2025. end_j: the signalised junction at one end (None: priority or roundabout at
# both ends). lanes: lane detectors on the section's own approach at end_j.
# ---------------------------------------------------------------------------------------------------------
SECTIONS = [
    # name, class, setting, kind, base AADF, from junction road, to junction road, length km, end_j, lanes
    ("Brookfield Way", "C", "urban", "retail", 9350, "Western Avenue", "Brookfield roundabout", 0.62, "J05", 1),
    ("Hollins Lane", "C", "urban", "leisure", 8950, "Fenwick Road", "Hollins Park", 0.81, "J11", 1),
    ("Infirmary Road", "U", "urban", "hospital", 8800, "Coventry Road", "Priory Road", 0.47, "J14", 2),
    ("Grange Road", "B", "urban", "school", 7400, "Station Street", "Sandy Lane", 0.74, "J08", 1),
    ("Castlegate Road", "C", "urban", "industrial", 7300, "Lea Road", "Castlegate", 0.95, "J16", 1),
    ("College Road", "B", "urban", "university", 6900, "Kingsway", "Oakhill Road", 0.58, "J03", 1),
    ("Station Street", "B", "urban", "commuter", 9900, "Market Way", "Birch Street", 0.52, "J09", 2),
    ("Kingsway", "B", "urban", "commuter", 11600, "Ring Road", "Rowley Street", 0.69, "J02", 1),
    ("Mill Lane", "C", "urban", "commuter", 7100, "Coventry Road", "Tanhouse Lane", 0.88, "J13", 1),
    ("Ashfield Road", "B", "urban", "commuter", 10400, "Ashby Road", "Wharf Street", 0.73, None, 0),
    ("Priory Road", "C", "urban", "commuter", 9300, "Infirmary Road", "Northgate Road", 0.66, None, 0),
    ("Wharf Street", "B", "urban", "commuter", 12700, "Ashfield Road", "Canal Street", 0.41, None, 0),
    ("Sandy Lane", "U", "urban", "commuter", 6700, "Grange Road", "Birch Street", 0.57, None, 0),
    ("Oakhill Road", "C", "urban", "commuter", 5200, "College Road", "Rowley Street", 0.79, None, 0),
    ("Tanhouse Lane", "C", "urban", "commuter", 7350, "Mill Lane", "Ashby Road", 0.84, None, 0),
    ("Lower Heath Road", "C", "rural", "interurban", 4100, "Stafford Road", "Heath End", 1.92, None, 0),
    ("Cradock Lane", "U", "rural", "interurban", 6200, "Lichgate Road", "Cradock", 1.37, None, 0),
    ("Holloway Hill", "B", "rural", "interurban", 9700, "Stafford Road", "Pelham Lane", 1.48, None, 0),
]

# Permanent automatic counters: name, road, class, setting, base AADF, installation date of the TX-200.
ATCS = [
    ("Western Avenue", "A", "urban", 24600, dt.date(2025, 3, 11)),
    ("Coventry Road", "A", "urban", 19800, dt.date(2025, 3, 12)),
    ("Ring Road North", "A", "urban", 27900, dt.date(2025, 3, 18)),
    ("Lea Road", "B", "urban", 13200, dt.date(2025, 4, 2)),
    ("Fenwick Road", "A", "urban", 17400, dt.date(2025, 4, 3)),
    ("Birmingham Road", "A", "urban", 22100, dt.date(2025, 4, 23)),
    ("Ashby Road", "B", "urban", 12100, dt.date(2025, 5, 7)),
    ("Northgate Road", "A", "urban", 15600, dt.date(2025, 5, 8)),
    ("Stafford Road", "A", "rural", 16300, dt.date(2025, 5, 20)),
    ("Lichgate Road", "B", "rural", 9800, dt.date(2025, 6, 3)),
    ("Pelham Lane", "C", "rural", 6900, dt.date(2025, 6, 4)),
]

# Signalised junctions. control: MOVA (isolated) or SCOOT (linked). arms: road, heading of the approach,
# kind, approach AADF (one direction), detected lanes. The counted sections' own arms are filled in below.
JUNCTIONS = [
    ("J02", "Kingsway / Ring Road", "MOVA", [("Ring Road", "EB", "commuter", 13800, 2), ("Ring Road", "WB", "commuter", 13100, 2)]),
    ("J03", "Kingsway / College Road", "MOVA", [("Kingsway", "NB", "commuter", 6400, 1), ("Kingsway", "SB", "commuter", 6100, 1)]),
    ("J05", "Western Avenue / Brookfield Way", "MOVA", [("Western Avenue", "NB", "commuter", 11800, 2), ("Western Avenue", "SB", "commuter", 12300, 2)]),
    ("J08", "Station Street / Grange Road", "MOVA", [("Station Street", "EB", "commuter", 5200, 1), ("Station Street", "WB", "commuter", 4900, 1)]),
    ("J09", "Station Street / Market Way", "MOVA", [("Market Way", "NB", "retail", 4300, 1), ("Market Way", "SB", "commuter", 4700, 1)]),
    ("J11", "Fenwick Road / Hollins Lane", "MOVA", [("Fenwick Road", "NB", "commuter", 8600, 2), ("Fenwick Road", "SB", "commuter", 8900, 2)]),
    ("J13", "Coventry Road / Mill Lane", "MOVA", [("Coventry Road", "EB", "commuter", 9700, 2), ("Coventry Road", "WB", "commuter", 9400, 2)]),
    ("J14", "Coventry Road / Infirmary Road", "MOVA", [("Coventry Road", "EB", "commuter", 9100, 2), ("Coventry Road", "WB", "commuter", 9900, 2)]),
    ("J16", "Lea Road / Castlegate Road", "MOVA", [("Lea Road", "NB", "commuter", 6500, 1), ("Lea Road", "SB", "commuter", 6800, 1)]),
    ("J19", "Western Avenue / Fenwick Road", "SCOOT", [("Western Avenue", "NB", "commuter", 11200, 2), ("Western Avenue", "SB", "commuter", 14300, 2), ("Fenwick Road", "EB", "commuter", 7600, 1), ("Fenwick Road", "WB", "retail", 5300, 1)]),
    ("J23", "Ring Road / Tanyard Lane", "SCOOT", [("Ring Road", "EB", "commuter", 12600, 2), ("Ring Road", "WB", "commuter", 9300, 2), ("Tanyard Lane", "NB", "leisure", 3900, 1), ("Tanyard Lane", "SB", "commuter", 4700, 1)]),
    ("J20", "Northgate Road / Station Street", "SCOOT", [("Northgate Road", "NB", "commuter", 7400, 2), ("Northgate Road", "SB", "commuter", 7700, 2), ("Station Street", "EB", "commuter", 4100, 1)]),
    ("J21", "Ring Road / Northgate Road", "SCOOT", [("Ring Road", "EB", "commuter", 13500, 2), ("Ring Road", "WB", "commuter", 12900, 2), ("Northgate Road", "NB", "commuter", 6900, 1), ("Northgate Road", "SB", "commuter", 7200, 1)]),
    ("J22", "Birmingham Road / Ashby Road", "SCOOT", [("Birmingham Road", "NB", "commuter", 10600, 2), ("Birmingham Road", "SB", "commuter", 10100, 2), ("Ashby Road", "EB", "commuter", 5600, 1), ("Ashby Road", "WB", "commuter", 5900, 1)]),
    ("J24", "Ring Road / Market Way", "SCOOT", [("Ring Road", "EB", "commuter", 14100, 2), ("Ring Road", "WB", "commuter", 13700, 2), ("Market Way", "NB", "retail", 5100, 1), ("Market Way", "SB", "retail", 4800, 1)]),
    ("J25", "Coventry Road / Ring Road", "SCOOT", [("Coventry Road", "EB", "commuter", 9800, 2), ("Coventry Road", "WB", "commuter", 10300, 2), ("Ring Road", "NB", "commuter", 12800, 2), ("Ring Road", "SB", "commuter", 12400, 2)]),
    ("J26", "Western Avenue / Lea Road", "SCOOT", [("Western Avenue", "NB", "commuter", 10900, 2), ("Western Avenue", "SB", "commuter", 11400, 2), ("Lea Road", "EB", "commuter", 5900, 1)]),
    ("J27", "Birmingham Road / Canal Street", "SCOOT", [("Birmingham Road", "NB", "commuter", 9900, 2), ("Birmingham Road", "SB", "commuter", 9600, 2), ("Canal Street", "WB", "commuter", 3300, 1)]),
    ("J28", "Fenwick Road / Market Way", "SCOOT", [("Fenwick Road", "NB", "commuter", 7100, 1), ("Fenwick Road", "SB", "commuter", 6900, 1), ("Market Way", "EB", "retail", 4600, 1), ("Market Way", "WB", "retail", 4400, 1)]),
    ("J30", "Ashby Road / Weston Road", "MOVA", [("Ashby Road", "NB", "commuter", 6000, 1), ("Ashby Road", "SB", "commuter", 6200, 1), ("Weston Road", "EB", "industrial", 3100, 1)]),
    ("J31", "Lichgate Road / Mill Street", "MOVA", [("Lichgate Road", "NB", "commuter", 5400, 1), ("Lichgate Road", "SB", "commuter", 5100, 1), ("Mill Street", "WB", "commuter", 2300, 1)]),
]
REFURBISHED = {"J19": dt.date(2025, 4, 14), "J23": dt.date(2025, 7, 21)}   # controller replaced, channels re-terminated
DARK_DAYS = 3                                                               # detectors dark during the swap


class World:
    pass


def section_heading(name):
    return {"Brookfield Way": "WB", "Hollins Lane": "NB", "Infirmary Road": "SB", "Grange Road": "NB",
            "Castlegate Road": "EB", "College Road": "WB", "Station Street": "WB", "Kingsway": "SB",
            "Mill Lane": "NB"}[name]


def build_world():
    rng = np.random.default_rng(SEED)
    W = World()
    W.days = DAYS
    # town-wide day effect (weather, events), shared by every road
    delta = rng.normal(0.0, 0.011, len(DAYS))
    for d, v in SNOW_DAYS.items():
        delta[DIDX[d]] += v
    W.delta = delta

    def series(kind, aadf, var=None, loc_sd=0.032):
        m = np.array([rhythm(kind, d, var) for d in DAYS])
        m = m / m.mean()
        e = rng.normal(0.0, loc_sd, len(DAYS))
        return aadf * m * (1.0 + delta) * (1.0 + e)

    def share12(kind, sd=0.006):
        return np.array([r12(kind, d) for d in DAYS]) * (1.0 + rng.normal(0.0, sd, len(DAYS)))

    # permanent counters
    W.atcs = []
    for name, rclass, setting, aadf, inst in ATCS:
        kind = "commuter" if setting == "urban" else "interurban"
        var = {"sat": rng.normal(0, 0.012), "sun": rng.normal(0, 0.012)}
        q = series(kind, aadf, var, loc_sd=0.018)
        s12 = share12(kind, 0.005) * (1.0 + rng.normal(0.0, 0.011))
        hgv = rng.uniform(0.042, 0.074) if rclass == "A" else rng.uniform(0.036, 0.058)
        W.atcs.append({"name": name, "road_class": rclass, "setting": setting, "kind": kind, "q24": q,
                       "q12": q * s12, "installed": inst, "hgv_share": hgv,
                       "rigid2_frac": rng.uniform(0.47, 0.56), "bus_share": rng.uniform(0.0025, 0.0065),
                       "lgv_share": rng.uniform(0.125, 0.16), "mc_share": rng.uniform(0.006, 0.011),
                       "trailer_share": rng.uniform(0.008, 0.016)})
    # counted sections (two-way daily flow)
    W.sections = []
    for (name, rclass, setting, kind, aadf, fr, to, length, end_j, lanes) in SECTIONS:
        q = series(kind, aadf)
        s12 = share12(kind) * (1.0 + rng.normal(0.0, 0.009))
        W.sections.append({"name": name, "road_class": rclass, "setting": setting, "kind": kind,
                           "base": aadf, "from": fr, "to": to, "length": length, "end_j": end_j,
                           "lanes": lanes, "q24": q, "q12": q * s12,
                           "dir_share": rng.uniform(0.47, 0.53),
                           "hgv": {"retail": 0.022, "leisure": 0.014, "hospital": 0.026, "school": 0.018,
                                   "industrial": 0.094, "university": 0.016, "commuter": 0.031,
                                   "interurban": 0.047}[kind] * rng.uniform(0.85, 1.15),
                           "bus": rng.uniform(0.004, 0.018), "lgv": rng.uniform(0.11, 0.16),
                           "mc": rng.uniform(0.005, 0.012), "cyc": rng.uniform(0.004, 0.02)})
    W.rng = rng
    return W




# ---------------------------------------------------------------------------------------------------------
# Detectors, counter channels, count days and the manual counts.
# ---------------------------------------------------------------------------------------------------------
import est  # noqa: E402

SECTION_SIDE = {"Brookfield Way": ("in", "out"), "Hollins Lane": ("in", "out"), "Infirmary Road": ("in", "out"),
                "Grange Road": ("out", "in"), "College Road": ("out", "in"), "Castlegate Road": ("out", "out"),
                "Station Street": ("in", "in"), "Kingsway": ("in", "in"), "Mill Lane": ("out", "out")}
CONTROLS = {"Station Street", "Kingsway", "Mill Lane"}


def neutral_pool():
    out = []
    for d in DAYS:
        if not (dt.date(2025, 3, 3) <= d <= dt.date(2025, 10, 23)):
            continue
        if d.weekday() > 3 or d in BANK_HOLIDAYS or in_ranges(d, SCHOOL_HOLIDAYS):
            continue
        out.append(d)
    return out


def make_detectors(W):
    rng = np.random.default_rng([SEED, 7])
    refs = {}
    used = set()
    for j in JUNCTIONS:
        while True:
            r = "%04d" % int(rng.integers(110, 990))
            if r not in used:
                used.add(r)
                refs[j[0]] = r
                break
    sec_by_j = {s["end_j"]: s for s in W.sections if s["end_j"]}
    W.junctions = []
    W.detectors = []          # one per channel
    for jid, jname, control, arms in JUNCTIONS:
        arms = list(arms)
        s = sec_by_j.get(jid)
        if s is not None:
            arms.insert(int(rng.integers(0, len(arms) + 1)), (s["name"], section_heading(s["name"]), s["kind"], None, s["lanes"]))
        chans = []
        for ai, (road, head, kind, aadf, lanes) in enumerate(arms):
            letter = "ABCD"[ai]
            if aadf is None:          # the counted section's own approach: one direction of its two-way flow
                eta = rng.normal(0.0, 0.011, len(DAYS))
                a24 = s["dir_share"] * s["q24"] * (1.0 + eta)
                a12 = s["dir_share"] * s["q12"] * (1.0 + eta + rng.normal(0.0, 0.004, len(DAYS)))
                own = s["name"]
            else:
                m = np.array([rhythm(kind, d) for d in DAYS])
                m = m / m.mean()
                e = rng.normal(0.0, 0.03, len(DAYS))
                a24 = aadf * m * (1.0 + W.delta) * (1.0 + e)
                a12 = a24 * np.array([r12(kind, d) for d in DAYS]) * (1.0 + rng.normal(0.0, 0.011)) * (1.0 + rng.normal(0.0, 0.006, len(DAYS)))
                own = None
            if lanes == 1:
                shares = [rng.uniform(0.968, 0.992)]
            else:
                l1 = rng.uniform(0.50, 0.60)
                shares = [l1, rng.uniform(0.955, 0.985) - l1]
            for li, sh in enumerate(shares):
                eps = rng.normal(0.0, 0.012 if lanes == 2 else 0.006, len(DAYS))
                d24 = sh * a24 * (1.0 + eps)
                d12 = sh * a12 * (1.0 + eps + rng.normal(0.0, 0.003, len(DAYS)))
                chans.append({"junction": jid, "arm": letter, "road": road, "heading": head, "lane": li + 1,
                              "kind": kind, "section": own, "d24": d24, "d12": d12})
        # channel numbering: current (register) order; refurbished junctions had another order before the swap
        order = list(range(len(chans)))
        rng.shuffle(order)
        for ch_no, ci in enumerate(order, start=1):
            chans[ci]["channel"] = ch_no
        if jid in REFURBISHED:
            old = list(range(1, len(chans) + 1))
            while True:
                rng.shuffle(old)
                if all(old[i] != chans[i]["channel"] for i in range(len(chans))):
                    break
            for i, c in enumerate(chans):
                c["old_channel"] = old[i]
        # availability
        for c in chans:
            av = np.full(len(DAYS), 100.0)
            if jid in REFURBISHED:
                sw = DIDX[REFURBISHED[jid]]
                av[sw - 1:sw - 1 + DARK_DAYS] = 0.0
            else:
                p_part = 0.016 if c["section"] else 0.022
                for i in range(len(DAYS)):
                    u = rng.random()
                    if u < 0.003:
                        av[i] = 0.0
                    elif u < 0.003 + p_part:
                        av[i] = float(rng.integers(58, 100))
                if c["section"] is None and rng.random() < 0.10:      # a longer loop fault on a few channels
                    st = int(rng.integers(20, 330))
                    av[st:st + int(rng.integers(9, 26))] = 0.0
            c["avail"] = av
            obs24 = np.where(av > 0, np.round(c["d24"] * av / 100.0 * (1.0 + np.where(av < 100, rng.normal(0, 0.02, len(DAYS)), 0.0))), np.nan)
            obs12 = np.where(av > 0, np.round(c["d12"] * av / 100.0 * (1.0 + np.where(av < 100, rng.normal(0, 0.02, len(DAYS)), 0.0))), np.nan)
            c["obs24"], c["obs12"] = obs24, obs12
        W.junctions.append({"id": jid, "ref": refs[jid], "name": jname, "control": control, "arms": arms})
        W.detectors.extend(chans)
    W.refs = refs


SCHEME_ARD = ["motorcycle", "car", "car_trailer", "lgv", "rigid2", "rigid3", "artic", "bus"]


def atc_site_channels(a, si, hgv_mult):
    rng = np.random.default_rng([SEED, 11, si, int(round(hgv_mult * 1000))])
    n = len(DAYS)
    tot = np.round(a["q24"]).astype(int)
    mc, bus, lgv, trl, hgv = a["mc_share"], a["bus_share"], a["lgv_share"], a["trailer_share"], a["hgv_share"] * hgv_mult
    r2 = a["rigid2_frac"]
    art = rng.uniform(0.30, 0.42)
    ch = np.zeros((n, 8), dtype=int)
    truth = np.zeros((n, 8), dtype=int)
    for i, d in enumerate(DAYS):
        wk = d.weekday()
        hf = 1.0 if wk < 5 else (0.55 if wk == 5 else 0.35)
        p_h = hgv * hf / (1.0 if wk < 5 else 0.85)
        p = np.array([mc, 0.0, trl, lgv, p_h * r2, p_h * (1 - r2 - art), p_h * art, bus])
        p = p * (1.0 + rng.normal(0.0, 0.05, 8))
        p = np.clip(p, 0.0002, None)
        p[1] = 1.0 - p.sum()
        v = rng.multinomial(int(tot[i]), p)
        truth[i] = v
        if d < FIRMWARE_PUSH:
            ch[i] = v
        else:
            l_short = int(round(v[3] * rng.uniform(0.66, 0.74)))
            a5 = int(round(v[6] * rng.uniform(0.64, 0.76)))
            ch[i] = [v[0], v[1] + l_short, v[3] - l_short, v[2], v[7], v[4], v[5] + v[6] - a5, a5]
    return truth, ch


def atc_channels(W):
    """24-hour vehicles by output channel: legacy ARD-8 classes until the firmware push, native TX-8 after.
    Each counter's heavy goods share is the tuned free parameter: the counter's 2025 heavy goods vehicles per day
    sits at least two vehicles inside its rounding bin and the install-date reading misses it by three bins."""
    # a six-day outage at one rural counter in January (rows absent from the export)
    W.atc_outage = (W.atcs[9]["name"], [DIDX[dt.date(2025, 1, 20)] + k for k in range(6)])
    for si, a in enumerate(W.atcs):
        a["obs24"] = np.round(a["q24"]).astype(float)
        a["obs12"] = np.round(a["q12"]).astype(float)
        if a["name"] == W.atc_outage[0]:
            for k in W.atc_outage[1]:
                a["obs24"][k] = np.nan
                a["obs12"][k] = np.nan
        keep = ~np.isnan(a["obs24"])
        for hm in (1.0, 1.006, 0.994, 1.012, 0.988, 1.018, 0.982, 1.024, 0.976, 1.03, 0.97):
            truth, ch = atc_site_channels(a, si, hm)
            sw = DIDX[FIRMWARE_PUSH]
            inst = DIDX[a["installed"]]
            ard = ch[:, 4] + ch[:, 5] + ch[:, 6]
            tx = ch[:, 5] + ch[:, 6] + ch[:, 7]
            gold = float(np.mean(np.concatenate([ard[:sw], tx[sw:]])[keep]))
            inst_v = float(np.mean(np.concatenate([ard[:inst], tx[inst:]])[keep]))
            if est.edge(gold, 10.0) >= 2.0 and abs(round(gold / 10) - round(inst_v / 10)) >= 3:
                break
        else:
            raise RuntimeError("counter %s not tuned" % a["name"])
        a["hgv_mult"] = hm
        a["classes_true"] = truth
        a["channels"] = ch
        a["hgv_true"] = truth[:, 4] + truth[:, 5] + truth[:, 6]


def count_rows(s, si, di, base_mult=1.0):
    """The 12-hour manual classified count on day di: rows (direction, hour, classes)."""
    rng = np.random.default_rng([SEED, 31, si, di, int(round(base_mult * 1000))])
    total = int(round(s["q12"][di] * base_mult * (1.0 + rng.normal(0.0, 0.006))))
    w = np.array(HOURLY[s["kind"]], dtype=float) * (1.0 + rng.normal(0.0, 0.05, 12))
    inbound = np.clip(0.5 + np.linspace(0.07, -0.07, 12) * (1 if s["kind"] in ("commuter", "school", "hospital", "industrial", "university") else -0.4) + rng.normal(0, 0.02, 12), 0.3, 0.7)
    cells = np.concatenate([w * inbound, w * (1 - inbound)])
    alloc = rng.multinomial(total, cells / cells.sum())
    hgv, bus, lgv, mc = s["hgv"], s["bus"], s["lgv"], s["mc"]
    hsplit = np.array([0.42, 0.10, 0.08, 0.10, 0.12, 0.18])
    rows = []
    for k, n in enumerate(alloc):
        direction = 0 if k < 12 else 1
        hour = 7 + (k % 12)
        p = np.concatenate([[mc, 0.0, bus, lgv], hgv * hsplit])
        p[1] = 1.0 - p.sum()
        v = rng.multinomial(int(n), p)
        cyc = int(rng.poisson(max(0.5, n * s["cyc"])))
        rows.append((direction, hour, cyc, v))
    return rows, total


def count_total(rows):
    return int(sum(int(v.sum()) for _, _, _, v in rows))


def lane_arrays(W, sname):
    chans = [c for c in W.detectors if c["section"] == sname]
    chans.sort(key=lambda c: c["lane"])
    return chans


def tmg_group(W, setting=None):
    return [(a["obs24"], a["obs12"]) for a in W.atcs if setting is None or a["setting"] == setting]


def families(W, s, si, di, base_mult=1.0):
    rows, _ = count_rows(s, si, di, base_mult)
    c12 = count_total(rows)
    grp = tmg_group(W, s["setting"])
    tm = {k: f(c12, di, grp) if "same-day" in k else f(c12, di, grp, BANK_HOLIDAYS) for k, f in est.TMG.items()}
    tm["T5 same-day, every counter pooled"] = est.tmg_sameday_ratio_of_sums(c12, di, tmg_group(W))
    own = {}
    if s["end_j"]:
        ch = lane_arrays(W, s["name"])
        d24 = np.nansum([c["obs24"] for c in ch], axis=0)
        d12 = np.nansum([c["obs12"] for c in ch], axis=0)
        av = np.min([c["avail"] for c in ch], axis=0)
        d24 = np.where(av > 0, d24, np.nan)
        d12 = np.where(av > 0, d12, np.nan)
        for k, f in est.OWN.items():
            own[k] = f(c12, di, d24, d12, av) if "month" not in k else f(c12, di, d24, d12, av, BANK_HOLIDAYS)
        if len(ch) == 2:
            for c in ch:
                own["G1 lane %d alone" % c["lane"]] = est.own_exact_day(c12, di, c["obs24"], c["obs12"], c["avail"])
        # the counters' 24/12 ratio is a licensed form only where the section's own 07:00-19:00 share agrees with theirs
        full = av >= 100
        own_share = float(np.nansum(d12[full]) / np.nansum(d24[full]))
        shares = [float(np.nansum(a[1]) / np.nansum(a[0])) for a in grp]
        if min(shares) - 0.01 <= own_share <= max(shares) + 0.01:
            own["G5 counters' 24/12 with the own detector's year"] = est.own_group_2412(c12, di, d24, d12, av, grp)
    return c12, tm, own


def ok_day(W, s, si, di, base_mult, strict_controls=True):
    if s["end_j"]:
        ch = lane_arrays(W, s["name"])
        if any(c["avail"][di] < 100 for c in ch):
            return False
    for a in W.atcs:
        if np.isnan(a["obs12"][di]):
            return False
    c12, tm, own = families(W, s, si, di, base_mult)
    gold_fam = own if s["end_j"] else tm
    gkey = "G1 counted day, full days" if s["end_j"] else "T1 same-day, ratio of sums"
    g = est.bin01(gold_fam[gkey])
    gb = round(g, 1)
    side_gold = "in" if g > 3.0 else "out"
    for v in gold_fam.values():
        b = est.bin01(v)
        if round(b, 1) != gb or est.edge(b) < 0.014 or abs(b - 3.0) < 0.12:
            return False
        if ("in" if b > 3.0 else "out") != side_gold:
            return False
    if s["end_j"]:
        want_g, want_d = SECTION_SIDE[s["name"]]
        if side_gold != want_g:
            return False
        for v in tm.values():
            b = est.bin01(v)
            if ("in" if b > 3.0 else "out") != want_d or abs(b - 3.0) < 0.08:
                return False
            if s["name"] in CONTROLS:
                if strict_controls and (round(b, 1) != gb or est.edge(b) < 0.01):
                    return False
            elif abs(b - g) < 0.2:
                return False
    return True


def choose_count_days(W):
    pool = neutral_pool()
    W.count_day = {}
    W.base_mult = {}
    for si, s in enumerate(W.sections):
        rng = np.random.default_rng([SEED, 53, si])
        order = list(pool)
        rng.shuffle(order)
        found = None
        for strict in (True, False):
            for bm in (1.0, 0.996, 1.004, 0.992, 1.008, 0.988, 1.012, 0.984, 1.016, 0.98, 1.02, 0.976, 1.024):
                for d in order:
                    if ok_day(W, s, si, DIDX[d], bm, strict):
                        found = (d, bm)
                        break
                if found:
                    break
            if found:
                break
        if not found:
            raise RuntimeError("no count day for %s" % s["name"])
        W.count_day[s["name"]], W.base_mult[s["name"]] = found
        rows, tot = count_rows(s, si, DIDX[found[0]], found[1])      # the count exactly as tested
        s["count_rows"], s["count_total"] = rows, count_total(rows)
        if found[1] != 1.0:          # the section's level is the tuned free parameter: rescale its flows
            s["q24"] = s["q24"] * found[1]
            s["q12"] = s["q12"] * found[1]
            for c in lane_arrays(W, s["name"]):
                for k in ("d24", "d12", "obs24", "obs12"):
                    c[k] = c[k] * found[1]
                c["obs24"] = np.round(c["obs24"])
                c["obs12"] = np.round(c["obs12"])


def build():
    W = build_world()
    make_detectors(W)
    atc_channels(W)
    choose_count_days(W)
    return W


if __name__ == "__main__":
    W = build()
    for si, s in enumerate(W.sections):
        d = W.count_day[s["name"]]
        c12, tm, own = families(W, s, si, DIDX[d], 1.0)
        g = own.get("G1 counted day, full days") or tm["T1 same-day, ratio of sums"]
        print("%-17s %s x%.3f c12 %5d true %6.0f gold %6.0f (%.2fM) tmg %6.0f (%.2fM)" % (
            s["name"], d, W.base_mult[s["name"]], c12, s["q24"].mean(), g, est.bin01(g),
            tm["T1 same-day, ratio of sums"], est.bin01(tm["T1 same-day, ratio of sums"])))

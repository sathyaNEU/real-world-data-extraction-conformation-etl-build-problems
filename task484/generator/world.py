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
    ("Brookfield Way", "C", "urban", "retail", 9350, "Western Avenue", "Brookfield Retail Park roundabout", 0.62, "J05", 1),
    ("Hollins Lane", "C", "urban", "leisure", 8950, "Fenwick Road", "Hollins Park entrance", 0.81, "J11", 1),
    ("Infirmary Road", "U", "urban", "hospital", 8800, "Coventry Road", "Priory Road", 0.47, "J14", 2),
    ("Grange Road", "B", "urban", "school", 7400, "Station Street", "Sandy Lane", 0.74, "J08", 1),
    ("Castlegate Road", "C", "urban", "industrial", 7300, "Leamore Road", "Castlegate Industrial Estate", 0.95, "J16", 1),
    ("College Road", "B", "urban", "university", 6900, "Kingsway", "Oakhill Road", 0.58, "J03", 1),
    ("Station Street", "B", "urban", "commuter", 9900, "Market Way", "Grange Road", 0.52, "J09", 2),
    ("Kingsway", "B", "urban", "commuter", 11600, "Ring Road", "College Road", 0.69, "J02", 1),
    ("Mill Lane", "C", "urban", "commuter", 7100, "Coventry Road", "Tanhouse Lane", 0.88, "J13", 1),
    ("Ashfield Road", "B", "urban", "commuter", 10400, "Darlaston Road", "Wharf Street", 0.73, None, 0),
    ("Priory Road", "C", "urban", "commuter", 9300, "Infirmary Road", "Bloxwich Road", 0.66, None, 0),
    ("Wharf Street", "B", "urban", "commuter", 12700, "Ashfield Road", "Canal Street", 0.41, None, 0),
    ("Sandy Lane", "U", "urban", "commuter", 6700, "Grange Road", "Birchills Street", 0.57, None, 0),
    ("Oakhill Road", "C", "urban", "commuter", 5200, "College Road", "Rowley Street", 0.79, None, 0),
    ("Tanhouse Lane", "C", "urban", "commuter", 7350, "Mill Lane", "Darlaston Road", 0.84, None, 0),
    ("Lower Heath Road", "C", "rural", "interurban", 4100, "Walsall Road", "Heath End", 1.92, None, 0),
    ("Cradley Lane", "U", "rural", "interurban", 6200, "Lichfield Road", "Cradley", 1.37, None, 0),
    ("Holloway Bank", "B", "rural", "interurban", 9700, "Walsall Road", "Pelsall Lane", 1.48, None, 0),
]

# Permanent automatic counters: name, road, class, setting, base AADF, installation date of the TX-200.
ATCS = [
    ("Western Avenue", "A", "urban", 24600, dt.date(2025, 3, 11)),
    ("Coventry Road", "A", "urban", 19800, dt.date(2025, 3, 12)),
    ("Ring Road North", "A", "urban", 27900, dt.date(2025, 3, 18)),
    ("Leamore Road", "B", "urban", 13200, dt.date(2025, 4, 2)),
    ("Fenwick Road", "A", "urban", 17400, dt.date(2025, 4, 3)),
    ("Birmingham Road", "A", "urban", 22100, dt.date(2025, 4, 23)),
    ("Darlaston Road", "B", "urban", 12100, dt.date(2025, 5, 7)),
    ("Bloxwich Road", "A", "urban", 15600, dt.date(2025, 5, 8)),
    ("Walsall Road", "A", "rural", 16300, dt.date(2025, 5, 20)),
    ("Lichfield Road", "B", "rural", 9800, dt.date(2025, 6, 3)),
    ("Pelsall Lane", "C", "rural", 6900, dt.date(2025, 6, 4)),
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
    ("J16", "Leamore Road / Castlegate Road", "MOVA", [("Leamore Road", "NB", "commuter", 6500, 1), ("Leamore Road", "SB", "commuter", 6800, 1)]),
    ("J19", "Western Avenue / Fenwick Road", "SCOOT", [("Western Avenue", "NB", "commuter", 11200, 2), ("Western Avenue", "SB", "commuter", 11900, 2), ("Fenwick Road", "EB", "commuter", 7600, 1), ("Fenwick Road", "WB", "retail", 5300, 1)]),
    ("J23", "Ring Road / Tanyard Lane", "SCOOT", [("Ring Road", "EB", "commuter", 12600, 2), ("Ring Road", "WB", "commuter", 13300, 2), ("Tanyard Lane", "NB", "leisure", 3900, 1), ("Tanyard Lane", "SB", "commuter", 4600, 1)]),
    ("J20", "Bloxwich Road / Station Street", "SCOOT", [("Bloxwich Road", "NB", "commuter", 7400, 2), ("Bloxwich Road", "SB", "commuter", 7700, 2), ("Station Street", "EB", "commuter", 4100, 1)]),
    ("J21", "Ring Road / Bloxwich Road", "SCOOT", [("Ring Road", "EB", "commuter", 13500, 2), ("Ring Road", "WB", "commuter", 12900, 2), ("Bloxwich Road", "NB", "commuter", 6900, 1), ("Bloxwich Road", "SB", "commuter", 7200, 1)]),
    ("J22", "Birmingham Road / Darlaston Road", "SCOOT", [("Birmingham Road", "NB", "commuter", 10600, 2), ("Birmingham Road", "SB", "commuter", 10100, 2), ("Darlaston Road", "EB", "commuter", 5600, 1), ("Darlaston Road", "WB", "commuter", 5900, 1)]),
    ("J24", "Ring Road / Market Way", "SCOOT", [("Ring Road", "EB", "commuter", 14100, 2), ("Ring Road", "WB", "commuter", 13700, 2), ("Market Way", "NB", "retail", 5100, 1), ("Market Way", "SB", "retail", 4800, 1)]),
    ("J25", "Coventry Road / Ring Road", "SCOOT", [("Coventry Road", "EB", "commuter", 9800, 2), ("Coventry Road", "WB", "commuter", 10300, 2), ("Ring Road", "NB", "commuter", 12800, 2), ("Ring Road", "SB", "commuter", 12400, 2)]),
    ("J26", "Western Avenue / Leamore Road", "SCOOT", [("Western Avenue", "NB", "commuter", 10900, 2), ("Western Avenue", "SB", "commuter", 11400, 2), ("Leamore Road", "EB", "commuter", 5900, 1)]),
    ("J27", "Birmingham Road / Canal Street", "SCOOT", [("Birmingham Road", "NB", "commuter", 9900, 2), ("Birmingham Road", "SB", "commuter", 9600, 2), ("Canal Street", "WB", "commuter", 3300, 1)]),
    ("J28", "Fenwick Road / Market Way", "SCOOT", [("Fenwick Road", "NB", "commuter", 7100, 1), ("Fenwick Road", "SB", "commuter", 6900, 1), ("Market Way", "EB", "retail", 4600, 1), ("Market Way", "WB", "retail", 4400, 1)]),
    ("J30", "Darlaston Road / Wednesbury Road", "MOVA", [("Darlaston Road", "NB", "commuter", 6000, 1), ("Darlaston Road", "SB", "commuter", 6200, 1), ("Wednesbury Road", "EB", "industrial", 3100, 1)]),
    ("J31", "Lichfield Road / Mill Street", "MOVA", [("Lichfield Road", "NB", "commuter", 5400, 1), ("Lichfield Road", "SB", "commuter", 5100, 1), ("Mill Street", "WB", "commuter", 2300, 1)]),
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
        s12 = share12(kind, 0.005)
        hgv = rng.uniform(0.038, 0.072) if rclass == "A" else rng.uniform(0.026, 0.052)
        W.atcs.append({"name": name, "road_class": rclass, "setting": setting, "kind": kind, "q24": q,
                       "q12": q * s12, "installed": inst, "hgv_share": hgv,
                       "rigid2_frac": rng.uniform(0.36, 0.46), "bus_share": rng.uniform(0.006, 0.014),
                       "lgv_share": rng.uniform(0.125, 0.16), "mc_share": rng.uniform(0.006, 0.011),
                       "trailer_share": rng.uniform(0.008, 0.016)})
    # counted sections (two-way daily flow)
    W.sections = []
    for (name, rclass, setting, kind, aadf, fr, to, length, end_j, lanes) in SECTIONS:
        q = series(kind, aadf)
        s12 = share12(kind)
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


if __name__ == "__main__":
    W = build_world()
    for s in W.sections:
        print(s["name"], round(s["q24"].mean()), s["kind"])

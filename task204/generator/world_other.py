"""Every other occurrence in the RMS extract windows, and the fare-gate counts."""
import datetime as dt

import numpy as np

import params as P
import world_net as N
from world_events import dates, to_utc

# offence code, description, weight, location types, property choices, hour profile kind
OTHER_TYPES = [
    ("THFT-SHOP", "Theft under 5000 - shoplifting", 15.0, ["COMMERCIAL"], ["MERCHANDISE"], "day"),
    ("THFT-FROMVEH", "Theft from motor vehicle", 13.0, ["STREET", "PARKING LOT", "RESIDENCE"], ["TOOLS", "BAG", "CASH", "DOCUMENTS"], "night"),
    ("THFT-VEH", "Theft of motor vehicle", 6.5, ["STREET", "PARKING LOT", "RESIDENCE"], ["VEHICLE"], "night"),
    ("BNE-RES", "Break and enter - residence", 6.0, ["RESIDENCE"], ["ELECTRONICS", "JEWELLERY", "CASH", "TOOLS"], "day"),
    ("BNE-COM", "Break and enter - business", 4.0, ["COMMERCIAL"], ["CASH", "MERCHANDISE", "TOOLS"], "night"),
    ("MSCHF", "Mischief - property damage", 11.0, ["STREET", "RESIDENCE", "COMMERCIAL", "PARKING LOT"], ["NONE"], "night"),
    ("ASLT-1", "Assault (level 1)", 9.0, ["STREET", "RESIDENCE", "COMMERCIAL", "LICENSED PREMISES"], ["NONE"], "eve"),
    ("ASLT-2", "Assault with weapon or causing bodily harm", 3.0, ["STREET", "RESIDENCE", "LICENSED PREMISES"], ["NONE"], "eve"),
    ("DIST", "Disturbance", 10.0, ["STREET", "RESIDENCE", "COMMERCIAL", "LICENSED PREMISES", "LRT PLATFORM"], ["NONE"], "eve"),
    ("FRAUD", "Fraud", 5.0, ["COMMERCIAL", "RESIDENCE", "ONLINE"], ["CASH", "DOCUMENTS"], "day"),
    ("THFT-BIKE", "Theft of bicycle", 2.5, ["STREET", "RESIDENCE", "LRT PLATFORM"], ["BICYCLE"], "day"),
    ("THFT-OTH", "Theft under 5000 - other", 7.5, ["STREET", "COMMERCIAL", "RESIDENCE", "LRT PLATFORM"], ["BAG", "WALLET", "TOOLS", "CASH"], "day"),
    ("ROB-COM", "Robbery - commercial", 0.9, ["COMMERCIAL"], ["CASH", "MERCHANDISE"], "eve"),
    ("ROB-PERS", "Robbery - person", 1.3, ["STREET", "PARKING LOT"], ["WALLET", "BAG", "CASH", "JEWELLERY"], "eve"),
    ("THFT-PERS", "Theft from person", 1.4, ["STREET", "COMMERCIAL", "LRT TRAIN"], ["WALLET", "BAG", "CASH"], "day"),
    ("DRUG-POSS", "Possession of a controlled substance", 2.0, ["STREET", "LRT PLATFORM", "PARKING LOT"], ["NONE"], "eve"),
    ("TRAF-CRIM", "Criminal traffic - impaired operation", 2.0, ["STREET"], ["NONE"], "night"),
    ("BREACH", "Fail to comply with release order", 3.0, ["STREET", "RESIDENCE"], ["NONE"], "day"),
    ("UTTER", "Uttering threats", 2.5, ["RESIDENCE", "STREET", "ONLINE"], ["NONE"], "day"),
    ("TRESP", "Trespass at night", 1.0, ["RESIDENCE", "COMMERCIAL"], ["NONE"], "night"),
]
DESC = {c: d for c, d, *_ in OTHER_TYPES}
DESC.update({"ROB-PERS": "Robbery - person", "THFT-PERS": "Theft from person"})
PROFILES = {
    "day": [0.2, 0.15, 0.1, 0.1, 0.15, 0.3, 0.6, 0.9, 1.2, 1.4, 1.5, 1.6, 1.6, 1.6, 1.6, 1.6, 1.5, 1.4, 1.2, 1.0, 0.8, 0.6, 0.4, 0.3],
    "night": [1.4, 1.5, 1.4, 1.2, 0.9, 0.6, 0.5, 0.6, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.5],
    "eve": [1.3, 1.1, 0.9, 0.5, 0.3, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.6, 1.8, 1.9, 1.9, 1.8, 1.7, 1.5],
}
DIST_WEIGHT = {"D1": 2.2, "D2": 1.3, "D3": 0.9, "D4": 1.1, "D5": 0.8, "D6": 1.0, "D7": 0.8, "D8": 0.8, "D9": 1.0, "D10": 0.7}


def make_other(rng):
    out = []
    types = OTHER_TYPES
    w = np.array([t[2] for t in types])
    w = w / w.sum()
    dists = sorted(DIST_WEIGHT)
    dw = np.array([DIST_WEIGHT[d] for d in dists])
    dw = dw / dw.sum()
    stations = sorted(N.STN)
    for (a, b) in (P.X25, P.X26):
        for d in dates(a, b):
            k = int(rng.poisson(P.OTHER_RATE * (1.08 if d.weekday() >= 4 else 0.97)))
            for _ in range(k):
                ti = int(rng.choice(len(types), p=w))
                code, desc, _, locs, props, prof = types[ti]
                loc = locs[int(rng.integers(0, len(locs)))]
                ph = np.array(PROFILES[prof], dtype=float)
                h = int(rng.choice(24, p=ph / ph.sum()))
                t = dt.datetime(d.year, d.month, d.day, h, int(rng.integers(0, 60)), int(rng.integers(0, 60)))
                if loc in ("LRT PLATFORM", "LRT TRAIN"):
                    st = stations[int(rng.integers(0, len(stations)))]
                    if st == "FG" and d < P.SPRING_CHANGE:
                        st = "MB"
                    x, y = N.STN[st]["x"] + float(rng.normal(0, 20)), N.STN[st]["y"] + float(rng.normal(0, 20))
                else:
                    st = None
                    dist = dists[int(rng.choice(len(dists), p=dw))]
                    rects = P.D26[dist]
                    areas = np.array([(x1 - x0) * (y1 - y0) for x0, y0, x1, y1 in rects], dtype=float)
                    x0, y0, x1, y1 = rects[int(rng.choice(len(rects), p=areas / areas.sum()))]
                    x, y = float(rng.uniform(x0, x1)), float(rng.uniform(y0, y1))
                prop = props[int(rng.integers(0, len(props)))]
                n_sus = int(rng.choice([0, 1, 2, 3], p=[0.35, 0.45, 0.15, 0.05]))
                out.append({"offence": code, "t_occ": t, "loc": loc, "station": st, "x": x, "y": y, "property": prop,
                            "suspects": n_sus, "weapon": "KNIFE" if (code == "ASLT-2" and rng.random() < 0.4) else "NONE"})
    return out


# ---- fare gates ---------------------------------------------------------------------------------------
HOUR_WKD = [0.2, 0.05, 0.0, 0.0, 0.0, 0.6, 3.2, 8.5, 9.0, 5.0, 4.0, 4.1, 4.6, 4.5, 4.8, 6.4, 8.4, 8.8, 6.2,
            4.2, 3.4, 2.6, 1.8, 1.0]
HOUR_WKE = [0.6, 0.2, 0.0, 0.0, 0.0, 0.0, 0.4, 1.4, 2.6, 3.8, 5.2, 6.2, 6.6, 6.6, 6.4, 6.2, 6.0, 5.6, 4.8,
            4.0, 3.4, 2.8, 2.0, 1.2]


def gate_code_on(station, entrance_i, t_local):
    ent, before, after, dev = P.GATES[station][entrance_i]
    return before if t_local.date() < P.SPRING_CHANGE else after


def make_entries(rng):
    """Hourly entries per gate code, stamped by the UTC hour (the fare system's own clock)."""
    rows = {}
    a = P.X26[0]
    b = P.X26[1]
    for d in dates(a, b):
        wd = d.weekday()
        holiday = d in P.HOLIDAYS
        prof = HOUR_WKE if (wd >= 5 or holiday) else HOUR_WKD
        dayf = 1.0 if (wd < 5 and not holiday) else (0.62 if wd == 5 else 0.46)
        tot = float(sum(prof))
        for st in sorted(P.GATES):
            if st == "FG" and d < P.SPRING_CHANGE:
                continue
            base = P.ENTRIES[st] * dayf * float(rng.normal(1.0, 0.06))
            ents = P.GATES[st]
            shares = [0.68, 0.32] if len(ents) == 2 else [1.0]
            for h in range(24):
                if prof[h] == 0:
                    continue
                t_local = dt.datetime(d.year, d.month, d.day, h)
                lam = base * prof[h] / tot
                for i, sh in enumerate(shares):
                    n = int(rng.poisson(lam * sh))
                    if n == 0:
                        continue
                    code = gate_code_on(st, i, t_local)
                    dev = P.GATES[st][i][3]
                    tu = to_utc(t_local)
                    rows[(code, dev, tu)] = rows.get((code, dev, tu), 0) + n
    return rows


def make_entries_2025(rng):
    """Daily entries per gate for the 2025 comparison weeks (the fare system's archived daily summary)."""
    rows = {}
    for d in dates(P.X25[0], P.X25[1]):
        wd = d.weekday()
        holiday = d in P.HOLIDAYS
        dayf = 1.0 if (wd < 5 and not holiday) else (0.62 if wd == 5 else 0.46)
        for st in sorted(P.GATES):
            if st == "FG":
                continue
            base = P.ENTRIES[st] * 0.94 * dayf * float(rng.normal(1.0, 0.06))
            ents = P.GATES[st]
            shares = [0.68, 0.32] if len(ents) == 2 else [1.0]
            for i, sh in enumerate(shares):
                ent, before, after, dev = ents[i]
                n = int(rng.poisson(base * sh))
                rows[(before, dev, d)] = n
    return rows

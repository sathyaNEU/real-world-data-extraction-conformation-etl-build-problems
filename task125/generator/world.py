"""task125 architecture 4: the City of Mountjoy's street segments, its two event venues and their calendars, the
founded patrol crimes on each segment by day, the 2026 calls for service (the city and the contracted Township of
Elmvale), the paid-duty bookings 2022 to 2027 and the 2026 paid-duty payroll lines.

Everything is drawn from one seed in a fixed order; nothing reads the clock. The truth objects carry the generator's
own answers (each segment's base rate and increment per event, each payroll line's booking), which analysis.py must
recover from the written files alone."""
import datetime as dt
import math

import numpy as np

SEED = 125054
AS_OF = dt.date(2027, 1, 6)
D0, D1 = dt.date(2022, 1, 1), dt.date(2026, 12, 31)
DAYS = [D0 + dt.timedelta(k) for k in range((D1 - D0).days + 1)]
DAY_INDEX = {d: k for k, d in enumerate(DAYS)}

NS = ["Ridgeway Ave", "Fairview Ave", "Kenwood Ave", "Orchard St", "Maple Ave", "Rideau St", "Cedar St", "Pine St",
      "Bay St", "Lake St", "Pier St", "Water St", "Wellington St", "Albert St", "Victoria St", "Clarence St",
      "Market St", "Brock St", "Peel St", "Ontario St", "Simcoe St", "Mill St", "Rubidge St", "Aylmer St",
      "Bethune St", "Reid St", "Park St"]
EW = ["Harbour Rd", "Front St", "King St", "Queen St", "Princess St", "Dundas St", "York St", "George St",
      "Charlotte St", "Sherbrooke St", "Hunter St", "McDonnel St", "Parkhill Rd", "Elgin St", "Durham St",
      "Murray St", "Edinburgh St", "Lansdowne St", "Romaine St", "Sophia St", "Smith St", "Wolfe St", "McKellar St",
      "Weller St", "Medina Rd", "Northgate Dr", "Burnham Line"]

GARDENS = {"name": "MEMORIAL GARDENS", "street": "Wellington St", "number": 200, "seg": ("NS", 12, 2)}
LAKESHORE = {"name": "LAKESHORE CENTRE", "street": "Harbour Rd", "number": 2015, "seg": ("EW", 0, 20)}

# Segments around each venue whose street crime rises on the venue's event nights: (orientation, street index,
# block), base founded patrol crimes a year, increment per event night.
G_ROLE = [(("EW", 2, 12), 58.0, 0.45), (("NS", 12, 2), 24.0, 0.76), (("NS", 12, 3), 22.0, 0.74),
          (("EW", 2, 11), 26.0, 0.70), (("EW", 3, 12), 23.0, 0.78), (("NS", 13, 2), 25.0, 0.72),
          (("NS", 12, 1), 12.0, 0.30)]
L_ROLE = [(("EW", 0, 20), 16.0, 1.25), (("EW", 0, 19), 17.0, 1.20), (("EW", 1, 20), 15.0, 1.30),
          (("EW", 1, 18), 18.0, 1.15), (("NS", 20, 1), 17.0, 1.30), (("EW", 2, 19), 11.0, 0.32),
          (("NS", 21, 0), 9.0, 0.30)]
# Near the Lakeshore Centre with no event-night rise (an industrial frontage and the trail access).
L_QUIET = [(("EW", 0, 21), 3.0), (("NS", 21, 1), 4.5), (("NS", 19, 0), 5.0)]
# The chronic places: bars at the east end of King St, the downtown terminal, the mall, plazas, motels, a strip.
C_ROLE = [(("EW", 2, 15), 78.0), (("EW", 2, 16), 68.0), (("EW", 7, 14), 74.0), (("EW", 25, 9), 85.0),
          (("EW", 17, 4), 64.0), (("NS", 20, 9), 63.0), (("EW", 12, 22), 66.0), (("NS", 6, 14), 62.5),
          (("EW", 5, 15), 63.5), (("NS", 16, 6), 62.0), (("EW", 21, 18), 69.0), (("NS", 24, 18), 62.0),
          (("EW", 9, 3), 64.5), (("NS", 14, 7), 72.0)]
W_ROLE = [(("EW", 13, 7), 34.0), (("NS", 9, 11), 36.0), (("EW", 19, 24), 33.0)]

PATROL = {"1610": "Robbery", "1420": "Assault level 2 (weapon or bodily harm)", "1430": "Assault level 1",
          "2120": "Break and enter", "2142": "Theft from a motor vehicle $5,000 or under", "2170": "Mischief",
          "3370": "Possession of weapons"}
OTHER = {"1371": "Sexual assault", "1627": "Uttering threats", "1625": "Criminal harassment",
         "2144": "Theft $5,000 or under", "2160": "Fraud", "3410": "Fail to comply with order",
         "4140": "Possession of a controlled substance", "2135": "Theft of a motor vehicle"}
LEGACY = [("ROB", "ROBBERY", "1610"), ("AS2", "ASSAULT LEVEL 2", "1420"), ("AWP", "ASSAULT WITH WEAPON", "1420"),
          ("AS1", "ASSAULT", "1430"), ("BEC", "B&E COMMERCIAL", "2120"), ("BER", "B&E RESIDENTIAL", "2120"),
          ("TFV", "THEFT FROM VEHICLE", "2142"), ("MIS", "MISCHIEF / DAMAGE", "2170"), ("WPN", "WEAPONS", "3370"),
          ("SXA", "SEXUAL ASSAULT", "1371"), ("THR", "THREATS", "1627"), ("HAR", "HARASSMENT", "1625"),
          ("TFO", "THEFT OTHER", "2144"), ("SHP", "SHOPLIFTING", "2144"), ("FRD", "FRAUD", "2160"),
          ("BRC", "BREACH", "3410"), ("DRG", "DRUGS POSSESSION", "4140"), ("MVT", "THEFT OF VEHICLE", "2135")]
TO_LEGACY = {}
for _l, _d, _u in LEGACY:
    TO_LEGACY.setdefault(_u, []).append(_l)
MIGRATION = dt.datetime(2023, 3, 1, 6, 0)


def rng():
    return np.random.default_rng(SEED)


# ----------------------------------------------------------------------------------------------- the street file
def streets(r):
    """The city's street segments: N-S street i between E-W streets j and j+1, E-W street j between N-S i and i+1."""
    gx = np.cumsum(np.r_[0, r.uniform(92, 148, len(NS) - 1)])
    gy = np.cumsum(np.r_[0, r.uniform(96, 152, len(EW) - 1)])
    x0, y0 = 711840.0, 4905310.0
    segs = []
    for i, name in enumerate(NS):
        for j in range(len(EW) - 1):
            segs.append({"key": ("NS", i, j), "street": name, "from": EW[j], "to": EW[j + 1],
                         "x": x0 + gx[i], "y": y0 + (gy[j] + gy[j + 1]) / 2, "len": gy[j + 1] - gy[j], "blk": j,
                         "col": i, "row": j})
    for j, name in enumerate(EW):
        for i in range(len(NS) - 1):
            segs.append({"key": ("EW", j, i), "street": name, "from": NS[i], "to": NS[i + 1],
                         "x": x0 + (gx[i] + gx[i + 1]) / 2, "y": y0 + gy[j], "len": gx[i + 1] - gx[i], "blk": i,
                         "col": i, "row": j})
    keep = {k for k, *_ in G_ROLE + L_ROLE} | {k for k, _ in L_QUIET + C_ROLE + W_ROLE}
    drop = set()
    while len(drop) < 26:
        s = segs[int(r.integers(len(segs)))]
        if s["key"] not in keep:
            drop.add(s["key"])
    segs = [s for s in segs if s["key"] not in drop]
    ids = r.choice(np.arange(100000, 200000), size=len(segs), replace=False)
    order = r.permutation(len(segs))
    for s, k in zip(segs, order):
        s["id"] = int(ids[k])
    for s in segs:
        b = s["blk"]
        lo_odd = 100 * b + 1
        hi_odd = 100 * b + 2 * int(r.integers(14, 49)) + 1
        hi_even = 100 * b + 2 * int(r.integers(14, 49))
        s["l_from"], s["l_to"], s["r_from"], s["r_to"] = lo_odd, hi_odd, 100 * b, hi_even
        c = 0 if s["col"] < 7 else (1 if s["col"] < 13 else (2 if s["col"] < 19 else 3))
        rw = 0 if s["row"] < 9 else 1
        s["ward"] = [[2, 1, 3, 4], [6, 5, 7, 8]][rw][c]
        s["x"] += float(r.normal(0, 3.0))
        s["y"] += float(r.normal(0, 3.0))
        s["len"] = round(float(s["len"]) + float(r.normal(0, 2.5)), 1)
    venue_ranges(segs)
    return segs


def venue_ranges(segs):
    for v in (GARDENS, LAKESHORE):
        s = next(x for x in segs if x["key"] == v["seg"])
        n = v["number"]
        if n % 2:
            s["l_to"] = max(s["l_to"], n + 20)
        else:
            s["r_to"] = max(s["r_to"], n + 20)


def by_key(segs):
    return {s["key"]: s for s in segs}


def base_rates(r, segs):
    """Founded patrol crimes a year from each segment's steady part, and its increment per event night."""
    bk = by_key(segs)
    base = {}
    for s in segs:
        u = r.random()
        if u < 0.58:
            v = r.gamma(0.7, 1.1)
        elif u < 0.89:
            v = r.gamma(2.2, 1.9)
        else:
            v = r.gamma(4.0, 2.9)
        base[s["id"]] = float(min(v, 23.0))
    inc_g, inc_l, role = {}, {}, {}
    for k, b, inc in G_ROLE:
        base[bk[k]["id"]] = b
        inc_g[bk[k]["id"]] = inc
        role[bk[k]["id"]] = "G"
    for k, b, inc in L_ROLE:
        base[bk[k]["id"]] = b
        inc_l[bk[k]["id"]] = inc
        role[bk[k]["id"]] = "L"
    for k, b in L_QUIET:
        base[bk[k]["id"]] = b
    for k, b in C_ROLE:
        base[bk[k]["id"]] = b
        role[bk[k]["id"]] = "C"
    for k, b in W_ROLE:
        base[bk[k]["id"]] = b
        role[bk[k]["id"]] = "W"
    return base, inc_g, inc_l, role


# ----------------------------------------------------------------------------------------------- venue calendars
def _season_dates(r, start, end, n, skip=None):
    """n home dates between start and end, weighted to Friday, Saturday and Sunday, at least two days apart."""
    pool = []
    d = start
    while d <= end:
        if not (skip and skip[0] <= d <= skip[1]):
            w = {4: 3.2, 5: 3.6, 6: 2.2, 3: 1.0, 1: 0.5, 2: 0.6, 0: 0.15}[d.weekday()]
            pool.append((d, w))
        d += dt.timedelta(1)
    chosen = []
    ds = [p[0] for p in pool]
    ws = np.array([p[1] for p in pool])
    while len(chosen) < n:
        k = int(r.choice(len(ds), p=ws / ws.sum()))
        c = ds[k]
        if all(abs((c - x).days) >= 2 for x in chosen):
            chosen.append(c)
    return sorted(chosen)


def calendars(r):
    """Each venue's event nights 2022 to 2027 with what was on. The 2027 nights are those booked by 6 January 2027."""
    ev = []   # (date, venue, kind, client, start, end, officers)
    playoffs = {2022: 2, 2023: 0, 2024: 3, 2025: 4, 2026: 2}
    for y in range(2021, 2027):
        first = dt.date(y, 9, 23)
        last = dt.date(y + 1, 3, 21)
        dates = _season_dates(r, first, last, 34, skip=(dt.date(2021, 12, 21), dt.date(2022, 1, 31)) if y == 2021
                              else (dt.date(y, 12, 24), dt.date(y + 1, 1, 7) if y == 2026 else dt.date(y, 12, 27)))
        for d in dates:
            venue = "L" if d >= dt.date(2027, 1, 1) else "G"
            if D0 <= d <= dt.date(2027, 6, 30):
                ev.append((d, venue, "hockey", "MOUNTJOY MARINERS HOCKEY CLUB",
                           "18:15" if d.weekday() == 6 else "17:30", "21:45" if d.weekday() == 6 else "22:30", 3))
        if y + 1 in playoffs and y + 1 <= 2026:
            p0 = dt.date(y + 1, 3, 25)
            taken = {e[0] for e in ev}
            k = 0
            d = p0
            while k < playoffs[y + 1]:
                if d not in taken and d.weekday() in (1, 3, 4, 5):
                    ev.append((d, "G", "hockey", "MOUNTJOY MARINERS HOCKEY CLUB", "17:30", "22:30", 3))
                    k += 1
                    d += dt.timedelta(2)
                d += dt.timedelta(1)
    promoters = ["NORTHERN STAGE PRESENTS", "LIVE NATION ONTARIO", "BAYSHORE PROMOTIONS", "MAPLE LEAF WRESTLING",
                 "KAWARTHA ENTERTAINMENT", "TRILLIUM CONCERTS"]
    taken = {e[0] for e in ev}
    for y in range(2022, 2027):
        for venue, n in (("G", int(r.integers(4, 7))), ("L", 13 if y == 2026 else int(r.integers(11, 14)))):
            k = 0
            while k < n:
                d = dt.date(y, 1, 1) + dt.timedelta(int(r.integers(0, 365)))
                if d.weekday() not in (3, 4, 5) or d in taken:
                    continue
                if venue == "G" and dt.date(y, 3, 21) >= d >= dt.date(y, 1, 1):
                    continue
                if venue == "G" and d >= dt.date(y, 9, 20):
                    continue
                taken.add(d)
                ev.append((d, venue, "concert", promoters[int(r.integers(len(promoters)))], "18:00", "23:30",
                           int(r.integers(2, 5))))
                k += 1
    # the 2027 shows already on sale at the extract: the reopened Lakeshore Centre's first season, and two at the
    # Gardens
    taken = {e[0] for e in ev}
    wanted = [(dt.date(2027, 2, 13), "G"), (dt.date(2027, 5, 8), "G")]
    while len(wanted) < 18:
        d = dt.date(2027, 1, 14) + dt.timedelta(int(r.integers(0, 164)))
        if d.weekday() in (4, 5) and d not in taken and all(d != x for x, _ in wanted):
            wanted.append((d, "L"))
    for d, venue in wanted:
        while d in taken:
            d += dt.timedelta(1)
        taken.add(d)
        ev.append((d, venue, "concert", promoters[int(r.integers(len(promoters)))], "18:00", "23:30",
                   int(r.integers(2, 5))))
    ev.sort(key=lambda e: (e[0], e[1]))
    return ev


def event_nights(ev, venue, y0=2022, y1=2026):
    return sorted({e[0] for e in ev if e[1] == venue and y0 <= e[0].year <= y1})


# ----------------------------------------------------------------------------------------------- the crimes
def season_factor(d):
    return 1.0 + 0.12 * math.cos(2 * math.pi * (d.timetuple().tm_yday - 200) / 365.25)


DOW = np.array([0.90, 0.88, 0.90, 0.95, 1.18, 1.27, 1.02])
DOW = DOW / DOW.mean()


def crimes(r, segs, base, inc_g, inc_l, ev):
    """The true founded patrol crimes: (segment id, protocol date, part) with part 'base' or the venue letter."""
    ids = np.array([s["id"] for s in segs])
    lam = np.array([base[i] for i in ids]) / 365.25
    gset = set(event_nights(ev, "G"))
    lset = set(event_nights(ev, "L"))
    gi = np.array([inc_g.get(i, 0.0) for i in ids])
    li = np.array([inc_l.get(i, 0.0) for i in ids])
    out = []
    for d in DAYS:
        f = season_factor(d) * DOW[d.weekday()]
        n = r.poisson(lam * f)
        for k in np.nonzero(n)[0]:
            out += [(int(ids[k]), d, "base")] * int(n[k])
        if d in gset:
            m = r.poisson(gi)
            for k in np.nonzero(m)[0]:
                out += [(int(ids[k]), d, "G")] * int(m[k])
        if d in lset:
            m = r.poisson(li)
            for k in np.nonzero(m)[0]:
                out += [(int(ids[k]), d, "L")] * int(m[k])
    return out


def nonpatrol_rates(r, segs, base):
    return {s["id"]: 0.55 * base[s["id"]] + float(r.gamma(1.6, 0.9)) for s in segs}


# ----------------------------------------------------------------------------------------------- Elmvale and the CAD
def township(r):
    """The Township of Elmvale's road segments in the CAD geofile (the county's numbering) and its eight patrol
    zones."""
    roads = (["Concession %d" % k for k in range(1, 13)] + ["County Rd %d" % k for k in (2, 4, 9, 12, 21, 28, 36)] +
             ["Sideroad %d" % k for k in (5, 10, 15, 20, 25, 30)] + ["Elmvale Line", "Hogs Back Rd", "Fennel Rd",
                                                                    "Station St", "Mill Pond Rd"])
    out = []
    ids = r.choice(np.arange(402000, 468000), size=440, replace=False)
    for k in range(440):
        road = roads[int(r.integers(len(roads)))]
        n0 = int(r.integers(1, 90)) * 100
        out.append({"id": int(ids[k]), "street": road, "zone": int(r.integers(1, 9)), "n0": n0})
    return out

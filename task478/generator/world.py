"""The truth behind task478's pack: the Calderwick Turnpike Authority's twelve sections, the weigh-in-motion station in
each, the five-axle tractor-semitrailers (FHWA class 9) and other trucks they weighed in 2026, the two scale houses'
static tickets, the toll system's five-axle entries and the enforcement unit's citations. Only pack.py (which writes
the files) and checks.py (which compares the cut pack with this truth) read this module.

Every truck has true axle weights; a static scale reads them as they are. A WIM station reads every axle with its own
multiplicative bias (its calibration) and a per-axle dynamic error, and sums the axles into the gross. A tractor's
steer axle carries its cab, engine and fuel: about 10,050 lb under an empty trailer, plus a share of the empty
trailer's kingpin load that depends on the trailer type, and about 11,400 lb under a loaded trailer whatever the cargo,
because a loaded tractor's fifth wheel is set to keep the steer axle near that level."""
import datetime as dt

import numpy as np

SEED = 4786
YEAR = 2026
AUTHORITY = "Calderwick Turnpike Authority"
ROAD = "Calderwick Turnpike"
PROGRAM = "Freight Compliance Program 2027"
LIMIT = 80000                       # gross vehicle weight limit, lb
LOADED_LINE = 50000                 # an empty tractor-semitrailer weighs under it, a loaded one over it
PEOPLE = {"director": "Anthony Hale", "engineer": "Anna Haynes"}

# code, name, milepost from, milepost to, technology, class 9 a weekday, loaded share, share of loaded running heavy,
# trailer mix (van, flatbed, dump, chassis, tank), station bias, mean loaded gross (lb), its spread (lb). The bulk
# haulers on Elk Ferry and Garnet Ridge load to the limit: a tight loaded gross just under 80,000 lb, no separate heavy
# traffic, the overweights the top of that band.
SECTIONS = [
    ("01", "Ashford Gap", 0.0, 21.6, "piezo", 44, .84, .030, (.60, .15, .05, .10, .10), 1.004, 70000, 5400),
    ("02", "Brannock", 21.6, 44.9, "piezo", 58, .58, .036, (.40, .08, .02, .45, .05), 1.062, 69000, 5400),
    ("03", "Cole Hollow", 44.9, 63.2, "bending", 38, .62, .160, (.40, .20, .25, .05, .10), 0.996, 70500, 5400),
    ("04", "Dunmere", 63.2, 88.7, "piezo", 53, .52, .110, (.30, .08, .02, .55, .05), 1.004, 70500, 5400),
    ("05", "Elk Ferry", 88.7, 109.4, "bending", 33, .80, .000, (.25, .15, .45, .05, .10), 0.952, 77090, 3200),
    ("06", "Foxbriar", 109.4, 131.0, "piezo", 62, .57, .035, (.45, .08, .02, .40, .05), 1.068, 68500, 5400),
    ("07", "Garnet Ridge", 131.0, 152.8, "bending", 29, .82, .000, (.25, .25, .40, .02, .08), 0.990, 77665, 3200),
    ("08", "Halbrook", 152.8, 178.3, "piezo", 47, .86, .039, (.60, .15, .08, .07, .10), 0.992, 70000, 5400),
    ("09", "Ingram Mill", 178.3, 203.5, "piezo", 55, .62, .045, (.50, .10, .03, .27, .10), 1.054, 69500, 5400),
    ("10", "Jessup Fork", 203.5, 229.0, "bending", 41, .75, .1145, (.45, .20, .15, .10, .10), 1.010, 70500, 5400),
    ("11", "Kettle Run", 229.0, 256.2, "piezo", 43, .66, .130, (.55, .20, .12, .03, .10), 0.958, 70800, 5400),
    ("12", "Lowfield", 256.2, 284.0, "bending", 36, .68, .055, (.60, .15, .08, .07, .10), 1.002, 69500, 5400),
]
CODES = [s[0] for s in SECTIONS]
NAMES = {s[0]: s[1] for s in SECTIONS}
TRAILERS = ("van", "flatbed", "dump", "chassis", "tank")
EMPTY_GROSS = {"van": 31500, "flatbed": 29000, "dump": 34000, "chassis": 27000, "tank": 32500}
# dynamic error of one axle reading (standard deviation, share of the reading)
AXLE_SD = {"piezo": 0.046, "bending": 0.033}
STEER_ERR = 0.5                     # a steer axle's single tires bounce less: its error against the other axles'
HEAVY_MEAN, HEAVY_SD = 84000, 3500
LOADED_SD = 5400
STEER_LOADED, STEER_LOADED_SD = 11400, 420
STEER_EMPTY, STEER_EMPTY_SD = 10050, 330
KINGPIN_SHARE = 0.16                # of an empty trailer's gross above 31,000 lb that reaches the steer axle
WEEKEND = 0.45                      # a weekend day's class 9 traffic against a weekday's
MONTH = [0.88, 0.90, 0.98, 1.02, 1.05, 1.06, 1.02, 1.05, 1.04, 1.06, 1.00, 0.94]
OTHER_CLASSES = {5: .10, 6: .05, 7: .03, 8: .05, 10: .06, 11: .02, 12: .01, 13: .02}   # per class 9 truck
HOLIDAYS = [dt.date(2026, 1, 1), dt.date(2026, 1, 19), dt.date(2026, 2, 16), dt.date(2026, 5, 25),
            dt.date(2026, 7, 3), dt.date(2026, 9, 7), dt.date(2026, 10, 12), dt.date(2026, 11, 11),
            dt.date(2026, 11, 26), dt.date(2026, 12, 25)]
DAYS = [dt.date(YEAR, 1, 1) + dt.timedelta(days=i) for i in range(365)]
WEEKDAYS = [d for d in DAYS if d.weekday() < 5]


def eastern_offset(d):
    """Hours behind UTC on date d, US Eastern (daylight time from the second Sunday of March to the first Sunday of
    November)."""
    m3 = dt.date(d.year, 3, 8)
    start = m3 + dt.timedelta(days=(6 - m3.weekday()) % 7)
    n1 = dt.date(d.year, 11, 1)
    end = n1 + dt.timedelta(days=(6 - n1.weekday()) % 7)
    return 4 if start <= d < end else 5


def day_factor(d):
    f = WEEKEND if d.weekday() >= 5 else 1.0
    if d in HOLIDAYS:
        f = WEEKEND
    return f * MONTH[d.month - 1]


def class9(rng, n, loaded_share, heavy_share, mix, loaded_mean, loaded_sd=None):
    """n five-axle tractor-semitrailers: trailer type, load state, true gross and the five true axle weights."""
    tt = rng.choice(len(TRAILERS), size=n, p=np.array(mix) / sum(mix))
    loaded = rng.random(n) < loaded_share
    heavy = loaded & (rng.random(n) < heavy_share)
    empty = np.array([EMPTY_GROSS[TRAILERS[k]] for k in tt]) + rng.normal(0, 1300, n)
    lw = np.clip(rng.normal(loaded_mean, loaded_sd or LOADED_SD, n), 48000, None)
    hw = rng.normal(HEAVY_MEAN, HEAVY_SD, n)
    gross = np.where(loaded, np.where(heavy, hw, lw), empty)
    steer = np.where(loaded, rng.normal(STEER_LOADED, STEER_LOADED_SD, n),
                     rng.normal(STEER_EMPTY, STEER_EMPTY_SD, n) + KINGPIN_SHARE * (empty - 31000))
    rest = gross - steer
    drive = rest * np.clip(rng.normal(np.where(loaded, 0.505, 0.47), 0.02, n), 0.4, 0.6)
    trailer = rest - drive
    s1 = rng.normal(0.5, 0.015, n)
    s2 = rng.normal(0.5, 0.02, n)
    axles = np.stack([steer, drive * s1, drive * (1 - s1), trailer * s2, trailer * (1 - s2)], axis=1)
    return dict(trailer=tt, loaded=loaded, heavy=heavy, gross=axles.sum(axis=1), axles=axles)


def outages(rng):
    """Days each station weighed nothing (controller faults, lane closures for paving)."""
    out = {}
    for code in CODES:
        k = int(rng.integers(6, 22))
        start = rng.choice(np.arange(10, 340), size=3, replace=False)
        days = set()
        for s in start:
            days.update(range(int(s), int(s) + k // 3 + 1))
        out[code] = {DAYS[i] for i in days if i < 365}
    return out


def wim(rng):
    """Every truck each station weighed in 2026, with its truth and its reading."""
    off = outages(rng)
    recs = []
    for code, name, m0, m1, tech, daily, ls, hs, mix, bias, lmean, lsd in SECTIONS:
        days = [d for d in DAYS if d not in off[code]]
        lam = np.array([daily * day_factor(d) for d in days])
        counts = rng.poisson(lam)
        n = int(counts.sum())
        t = class9(rng, n, ls, hs, mix, lmean, lsd)
        dayidx = np.repeat(np.arange(len(days)), counts)
        sd = AXLE_SD[tech]
        read = t["axles"] * bias * (1 + rng.normal(0, 1, t["axles"].shape) * sd * np.array([STEER_ERR, 1, 1, 1, 1]))
        recs.append(dict(code=code, tech=tech, bias=bias, days=days, dayidx=dayidx, cls=np.full(n, 9), **t,
                         read=read))
        # the other truck classes on the same days, read the same way
        others = []
        for cls, share in OTHER_CLASSES.items():
            m = rng.poisson(lam * share)
            others.append((cls, m))
        recs[-1]["others"] = others
    return recs, off


def tickets(rng):
    """The two scale houses' class 9 static tickets: trucks pulled in at the barrier plazas, heavy ones far more
    often, every axle weighed as it is."""
    n = 2600
    t = class9(rng, n * 5, .86, .30, (.40, .18, .22, .10, .10), 71000)
    w = np.where(t["gross"] > 76000, 1.0, np.where(t["loaded"], 0.22, 0.012))
    pick = np.flatnonzero(rng.random(len(w)) < w * 0.45)[:n]
    return {k: v[pick] for k, v in t.items()}


# toll plazas: code, name, section, milepost, five-axle entries a weekday, opened, closed (None = open)
PLAZAS = [
    ("P01", "West Barrier", "01", 0.6, 34, None, None),
    ("P03", "Ashford Gap", "01", 12.8, 22, None, None),
    ("P05", "Wendell Road", "02", 26.4, 31, None, None),
    ("P23", "Brannock Road", "02", 38.1, 27, None, dt.date(2026, 4, 30)),
    ("P41", "Brannock Road", "02", 38.1, 27, dt.date(2026, 5, 15), None),
    ("P07", "Cole Hollow", "03", 52.0, 26, None, None),
    ("P09", "Pellam Junction", "04", 70.3, 30, None, None),
    ("P10", "Dunmere", "04", 81.9, 24, None, None),
    ("P11", "Elk Ferry", "05", 97.5, 23, None, None),
    ("P13", "Foxbriar North", "06", 115.2, 33, None, None),
    ("P14", "Foxbriar South", "06", 124.0, 21, None, None),
    ("P15", "Garnet Ridge", "07", 141.6, 21, None, None),
    ("P17", "Halbrook", "08", 160.4, 25, None, None),
    ("P23", "Halbrook East", "08", 171.0, 18, dt.date(2026, 9, 1), None),
    ("P19", "Ingram Mill", "09", 186.7, 29, None, None),
    ("P20", "Route 9 Connector", "09", 197.3, 22, None, None),
    ("P25", "Jessup Fork", "10", 214.8, 27, None, None),
    ("P27", "Kettle Run", "11", 238.5, 25, None, None),
    ("P28", "Marsh Lane", "11", 249.9, 16, None, None),
    ("P30", "Lowfield", "12", 265.2, 20, None, None),
    ("P32", "East Barrier", "12", 283.4, 31, None, None),
]
SHUTTLE_SHARE = 0.05                   # entries by trucks that re-enter one plaza the same day
ENTRY_HOURS = np.array([2, 2, 2, 3, 5, 8, 10, 11, 11, 10, 10, 10, 10, 10, 10, 10, 9, 8, 6, 5, 4, 3, 3, 2], float)
ENTRY_HOURS = ENTRY_HOURS / ENTRY_HOURS.sum()    # five-axle entries by local hour of the day
# The toll back office moved to a new host plaza by plaza: each plaza's lanes went over at 02:00 local on its day, and
# the new host backfilled the plaza's last BACKFILL_DAYS of entries from the lanes' own logs. The old host stamped an
# entry when the lane's upload reached it (up to RECEIPT_MIN minutes late), in local time, to the minute; the lanes'
# logs carry local time to the second; the new host stamps its own entries in UTC.
SWITCH = {"P01": (5, 18), "P03": (6, 9), "P05": (6, 12), "P41": (6, 2), "P07": (6, 4), "P09": (5, 21), "P10": (6, 26),
          "P11": (6, 8), "P13": (5, 28), "P14": (6, 30), "P15": (6, 11), "P17": (6, 5), "P19": (5, 25), "P20": (6, 17),
          "P25": (6, 15), "P27": (6, 1), "P28": (6, 23), "P30": (6, 14), "P32": (6, 7)}
BACKFILL_DAYS = 18
RECEIPT_MIN = 15
REENTRY = 0.65                         # trucks cited for gross weight that come back through the barrier after offloading


def switch_time(code):
    """Local time the plaza's lanes moved to the new host (None: a plaza only ever on one host)."""
    if code not in SWITCH:
        return None
    m, d = SWITCH[code]
    return dt.datetime(YEAR, m, d, 2, 0)
TOL_SCALE = 500                        # citations: the enforcement unit's tolerance over 80,000 lb


def plaza_open(p, d):
    return (p[5] is None or d >= p[5]) and (p[6] is None or d <= p[6])


def toll_entries(rng):
    """Every five-axle entry in 2026, with the tags that made them. Each tag belongs to a carrier based in one section
    and makes a little over half its entries at that section's plazas, the rest anywhere on the road; a share of the
    entries are shuttle trucks' second and third entries at one plaza the same day."""
    secs = np.array([p[2] for p in PLAZAS])
    ntag = 5200
    home = rng.choice(len(CODES), size=ntag, p=np.array([s[5] for s in SECTIONS]) / sum(s[5] for s in SECTIONS))
    tagid = np.array(["%011d" % (34000000000 + 7919 * k) for k in range(ntag)])
    homed = {c: np.flatnonzero(home == j) for j, c in enumerate(CODES)}
    rows = []
    for d in DAYS:
        f = day_factor(d)
        for i, p in enumerate(PLAZAS):
            if not plaza_open(p, d):
                continue
            n = int(rng.poisson(p[4] * f))
            if n == 0:
                continue
            own = rng.random(n) < 0.55
            pool_home = homed[p[2]]
            pick = np.where(own, rng.choice(pool_home, size=n), rng.integers(0, ntag, n))
            sec = np.sort(rng.choice(24, size=n, p=ENTRY_HOURS) * 3600 + rng.integers(0, 3600, n))
            for t, s_ in zip(tagid[pick], sec):
                rows.append((d, i, str(t), int(s_)))
                if rng.random() < SHUTTLE_SHARE and s_ < 60000:
                    rows.append((d, i, str(t), int(s_ + rng.integers(7200, 21600))))
    rows.sort(key=lambda r: (r[0], r[3], r[1]))
    return rows


SCALE_HOUSES = {"W": ("West Scale House", "01", 0.6), "E": ("East Scale House", "12", 283.4)}
PAPER_UNTIL = dt.date(2026, 6, 30)     # citations written on paper and keyed later; e-citations from 1 July


def stops(rng, entries, tk):
    """Each scale-house ticket is a truck stopped on its way out at a barrier: attach it to an entry (the trip) and
    time the stop (local time) from the entry and the distance driven."""
    # a trip is an entry its tag does not follow with another for eight hours, so the stop closes that trip
    nxt = {}
    last = {}
    for k in range(len(entries) - 1, -1, -1):
        d, i, t, s_ = entries[k]
        when = (d - DAYS[0]).days * 86400 + s_
        nxt[k] = last.get(t, when + 10 ** 9) - when
        last[t] = when
    trips = [k for k, (d, i, t, s_) in enumerate(entries) if PLAZAS[i][0] not in ("P01", "P32") and nxt[k] > 28800]
    pick = rng.choice(trips, size=len(tk["gross"]), replace=False)
    out = []
    for j, k in enumerate(pick):
        d, i, tag, s_ = entries[k]
        mp = PLAZAS[i][3]
        house = "W" if mp < 142 else "E"
        miles = abs(mp - SCALE_HOUSES[house][2])
        t = dt.datetime.combine(d, dt.time()) + dt.timedelta(seconds=s_) + dt.timedelta(
            minutes=float(miles / 58.0 * 60 + rng.uniform(4, 25)))
        out.append(dict(entry=k, tag=tag, house=house, local=t))
    return out


def citations(rng, entries, tk, st):
    """The enforcement unit cites a gross over 80,000 lb beyond its scale tolerance and an overweight tandem; a paper
    citation is keyed some days after the stop, an e-citation at once, and the log's entry plaza is the truck's
    latest entry when the citation is keyed. Most trucks cited for gross weight leave through the barrier, offload
    nearby and come back onto the turnpike at that barrier a few hours later: those entries join the toll record."""
    barrier = {"W": [i for i, p in enumerate(PLAZAS) if p[0] == "P01"][0],
               "E": [i for i, p in enumerate(PLAZAS) if p[0] == "P32"][0]}
    for j, stp in enumerate(st):
        if tk["gross"][j] > LIMIT + TOL_SCALE and rng.random() < REENTRY:
            back = stp["local"] + dt.timedelta(hours=float(rng.uniform(1.5, 4.5)))
            if back.year != YEAR:
                continue
            entries.append((back.date(), barrier[stp["house"]], stp["tag"],
                            int((back - dt.datetime.combine(back.date(), dt.time())).total_seconds())))
    by_tag = {}
    for k, (d, i, tag, s_) in enumerate(entries):
        by_tag.setdefault(tag, []).append((dt.datetime.combine(d, dt.time()) + dt.timedelta(seconds=s_), k))
    for v in by_tag.values():
        v.sort()
    cites = []
    for j, stp in enumerate(st):
        g = tk["gross"][j]
        ax = tk["axles"][j]
        codes = []
        if g > LIMIT + TOL_SCALE:
            codes.append("G")
        if ax[1] + ax[2] > 34000 + TOL_SCALE or ax[3] + ax[4] > 34000 + TOL_SCALE:
            codes.append("T")
        if not codes:
            continue
        local = stp["local"]
        paper = local.date() <= PAPER_UNTIL
        keyed = local + (dt.timedelta(days=int(rng.integers(4, 14)), hours=float(rng.uniform(0, 8))) if paper
                         else dt.timedelta(minutes=float(rng.uniform(5, 40))))
        trips = by_tag[stp["tag"]]
        latest = [k for t_, k in trips if t_ <= keyed][-1]
        for c in codes:
            cites.append(dict(ticket=j, code=c, local=local, keyed=keyed, paper=paper, trip=stp["entry"],
                              logged=latest))
    return cites


def everything():
    rng = np.random.default_rng(SEED)
    recs, off = wim(rng)
    tk = tickets(rng)
    rng2 = np.random.default_rng(SEED + 1)
    entries = toll_entries(rng2)
    n0 = len(entries)
    st = stops(rng2, entries, tk)
    ci = citations(rng2, entries, tk, st)
    return dict(wim=recs, outages=off, tickets=tk, entries=entries, stops=st, citations=ci, n_entries=n0)


def section_of(entries, k):
    return PLAZAS[entries[k][1]][2]


def truth_shares(e):
    return {r["code"]: 100.0 * float(np.mean(r["gross"] > LIMIT)) for r in e["wim"]}

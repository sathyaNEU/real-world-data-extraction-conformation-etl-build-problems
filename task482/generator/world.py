"""task482 world: Penwick Pharmacy's thirty stores, each vaccine refrigerator's 2026 air, logger probe and vaccine.

Physical time is one minute per step from 2025-12-31 18:00 Central (the warm-up) to 2027-01-01 06:00 Central. The
air in each refrigerator relaxes to its target (the setpoint and its control swing, a defrost swing at the household
units, the room's air while a door stands open, the room's air slowly through an outage, a door left ajar, a failing
thermostat). The logger's probe in its 5 mL glycol bottle follows the air with TAU_P minutes; the vaccine in its
cartons follows it with TAU_V. Every logger is set, as the chain's standard requires, to record the mean of its probe
over each ten minutes, stamped at the interval's start; the pilot's in-carton sensor reads the vaccine every ten
minutes. Nothing in the pack states either constant.
"""
import datetime as dt

import numpy as np

SEED = 482
T0 = dt.datetime(2026, 1, 1)                 # local midnight, Central standard time = UTC-6
WARM = 360                                   # minutes simulated before local midnight
TAIL = 360                                   # minutes simulated after the local year
N = WARM + 525600 + TAIL
TAU_P, TAU_V, TAU_OPEN, ROOM = 3.0, 46.0, 15.0, 21.5
LIMIT, LINE = 8.0, 24.0
STEP = 10                                    # every logger and the in-carton sensor record every ten minutes
DST0 = (dt.datetime(2026, 3, 8, 2) - T0).days * 1440 + 120      # standard-time minute of the spring change
DST1 = (dt.datetime(2026, 11, 1, 1) - T0).days * 1440 + 60      # standard-time minute of the autumn change
UTC0 = dt.datetime(2026, 1, 1, 6, 0)         # local midnight in UTC
HOLIDAYS = [0, 329, 358]                     # New Year's Day, Thanksgiving, Christmas Day: pharmacies closed

PEOPLE = {"director": "Breanna Graham", "pilot": "Julia Kaufman"}
CHAINS = {"F": "Penwick Pharmacy", "K": "Vollmer Drug", "P": "Lindqvist Apothecary"}
MAKES = {"F": ("Frostline", "FL-200 Cloud"), "K": ("Kelvra", "KV-10"), "P": ("Brumal", "BR-20")}
VENDORS = {"sensor": "Tamberlane Sensing", "system": "Tellvane", "wholesaler": "Meridale Pharmaceutical Distribution",
           "service": "Brannon Refrigeration Service"}
COMPANY = "Penwick Pharmacy, Inc."


def doy(mo, d):
    return (dt.date(2026, mo, d) - dt.date(2026, 1, 1)).days


STORMS = {"S1": (doy(2, 9), 15, 40), "S2": (doy(6, 18), 17, 5), "S3": (doy(8, 3), 2, 30)}

# number, town, unit (pharma: purpose-built pharmaceutical refrigerator; household: household-style), setpoint,
# routine door openings a day, delivery-day door minutes, month-end count minutes, extras
_D = {
    101: ("Corriden", "pharma", 4.6, 22, 6, 9, {"storms": ["S1", "S3"]}),
    102: ("Dalmore", "pharma", 4.3, 12, 4, 8, {}),
    103: ("Edgecott", "pharma", 4.7, 24, 29, 9, {}),
    104: ("Farrowby", "pharma", 4.9, 40, 8, 9, {}),
    105: ("Gisborne", "household", 4.7, 20, 5, 8, {"defrost": (8.8, 46)}),
    106: ("Hatherley", "household", 5.1, 17, 6, 9, {"drift": [(doy(7, 6), 3900, 8.9)]}),
    107: ("Ilsington", "pharma", 4.5, 16, 5, 9, {}),
    108: ("Keverne", "pharma", 5.2, 46, 13, 9, {"twice": True}),
    109: ("Marcham", "pharma", 4.6, 22, 6, 9, {"propped": (33, 9, 12, 2)}),
    110: ("Oldcastle", "household", 5.0, 15, 6, 9, {"ajar": [(doy(3, 27), 650), (doy(11, 20), 440)]}),
    201: ("Thurlby", "pharma", 4.8, 21, 6, 9, {"drift": [(doy(4, 20), 2100, 9.2), (doy(12, 2), 1500, 9.0)]}),
    202: ("Ulverston", "pharma", 5.1, 42, 12, 9, {"twice": True}),
    203: ("Vexley", "pharma", 4.4, 10, 4, 8, {}),
    204: ("Wedmore", "household", 4.5, 16, 6, 8, {"defrost": (8.7, 44)}),
    205: ("Yelverton", "pharma", 4.6, 25, 7, 9, {"storms": ["S3"]}),
    206: ("Abbotsley", "pharma", 4.8, 26, 31, 9, {}),
    207: ("Braxted", "pharma", 4.7, 28, 13, 9, {"twice": True}),
    208: ("Chelwood", "pharma", 4.5, 13, 5, 8, {"propped": (38, 10, 11, 2)}),
    209: ("Embleton", "pharma", 5.0, 44, 9, 9, {}),
    210: ("Greystoke", "pharma", 4.7, 20, 6, 9, {"storms": ["S2"], "ajar": [(doy(10, 14), 600)]}),
    301: ("Haddow", "household", 4.6, 18, 5, 8, {"defrost": (8.7, 45)}),
    302: ("Inkpen", "pharma", 4.7, 19, 6, 9, {"storms": ["S2"]}),
    303: ("Lexden", "household", 5.0, 22, 27, 9, {}),
    304: ("Mowbray", "pharma", 4.2, 14, 5, 8, {}),
    305: ("Nettlecombe", "pharma", 4.8, 26, 7, 9, {"ajar": [(doy(5, 22), 400)]}),
    306: ("Padbury", "pharma", 4.7, 20, 6, 9, {"propped": (27, 9, 12, 2)}),
    307: ("Quarndon", "pharma", 4.8, 38, 9, 9, {}),
    308: ("Ruddington", "pharma", 4.5, 18, 5, 9, {"storms": ["S1", "S2", "S3"]}),
    309: ("Tilney", "household", 4.7, 22, 6, 9, {"defrost": (8.8, 45)}),
    310: ("Upwood", "pharma", 4.9, 30, 8, 9, {"storms": ["S1"]}),
}
PILOT = [105, 107, 110, 202, 206, 209, 304, 305, 308, 309]
VARIANT = {101: 1, 103: 1, 106: 4, 108: 9, 109: 55, 110: 55, 202: 2, 206: 3, 210: 1, 301: 1, 303: 1, 306: 1,
           310: 2}                            # per-store seed variants, set by tuning so every figure sits mid-bin
COUNT_30DEC = [102, 105, 110, 203, 208, 209, 306, 307]   # year-end inventory taken on 30 December
REPLACED = {302: (doy(3, 14), 13, 20, 190), 207: (doy(9, 9), 22, 40, 150)}   # day, hh, mm, gap minutes


def seed(no, k):
    return SEED * 1000 + no * 7 + k + 100003 * VARIANT.get(no, 0)


def make_of(no):
    return {1: "F", 2: "K", 3: "P"}[no // 100]


STORES = [dict(no=no, town=v[0], unit=v[1], sp=v[2], door=v[3], restock=v[4], count=v[5], ex=v[6], make=make_of(no),
               chain=CHAINS[make_of(no)]) for no, v in sorted(_D.items())]
BY_NO = {s["no"]: s for s in STORES}

# the local wall clock for every physical minute
_m = np.arange(N)
_std = _m - WARM
WALL = _std + ((_std >= DST0) & (_std < DST1)) * 60
WDAY = np.floor_divide(WALL, 1440)
WMIN = WALL - WDAY * 1440
_DATES = [dt.date(2026, 1, 1) + dt.timedelta(days=int(d)) for d in range(-1, 368)]
MONTH = np.array([d.month for d in _DATES])[np.clip(WDAY + 1, 0, 368)]
DOW = (WDAY + 3) % 7
SEASON = np.where(MONTH >= 9, 2.4, np.where(MONTH <= 2, 1.3, 1.0))
_open = (((DOW < 5) & (WMIN >= 480) & (WMIN < 1260)) | ((DOW == 5) & (WMIN >= 540) & (WMIN < 1080))
         | ((DOW == 6) & (WMIN >= 600) & (WMIN < 1080)))
OPEN = _open & ~np.isin(WDAY, HOLIDAYS) & (WDAY >= 0) & (WDAY < 365)
TOD = np.interp(WMIN, [480, 600, 720, 840, 960, 1080, 1260], [0.6, 1.0, 1.4, 1.0, 1.3, 1.5, 0.7])
WARM_SEASON = (MONTH >= 5) & (MONTH <= 9)


def at(day, hh, mm):
    """physical minute of a local wall time on a day of 2026 (0-based)"""
    w = day * 1440 + hh * 60 + mm
    s = w - (60 if (DST0 + 60 <= w < DST1 + 60) else 0)
    return s + WARM


def utc_of(m):
    return UTC0 + dt.timedelta(minutes=int(m) - WARM)


def local_of(m):
    """local wall time and its UTC offset in hours"""
    u = utc_of(m)
    std = int(m) - WARM
    off = -5 if DST0 <= std < DST1 else -6
    return u + dt.timedelta(hours=off), off


def ifilter(x, c, y0, block=800):
    """y[n] = c[n] * y[n-1] + (1 - c[n]) * x[n], y[-1] = y0"""
    x = np.asarray(x, float)
    c = np.broadcast_to(np.asarray(c, float), x.shape)
    y = np.empty_like(x)
    prev = float(y0)
    for s in range(0, len(x), block):
        xs, cs = x[s:s + block], c[s:s + block]
        p = np.cumprod(cs)
        y[s:s + block] = p * (prev + np.cumsum((1.0 - cs) * xs / p))
        prev = y[s + len(xs) - 1]
    return y


def deliveries(s):
    """(physical minute, door minutes, propped) for each delivery: Tuesdays all year, Fridays September to November
    and at the twice-weekly stores all year; the propped stores' season deliveries are unloaded with the door held"""
    r = np.random.default_rng(seed(s["no"], 1))
    out = []
    ex = s["ex"]
    for d in range(365):
        dd = _DATES[d + 1]
        if d in HOLIDAYS:
            continue
        if not (dd.weekday() == 1 or (dd.weekday() == 4 and (9 <= dd.month <= 11 or ex.get("twice")))):
            continue
        a = at(d, 10, int(r.integers(0, 110)))
        k = int(max(2, round(r.normal(s["restock"], s["restock"] * 0.15))))
        pp = ex.get("propped")
        propped = bool(pp and pp[1] <= dd.month <= pp[2] and (dd.weekday() == 1 or pp[3] == 2))
        if propped:
            k = int(max(5, round(r.normal(pp[0], 1.5))))
        out.append((a, k, propped))
    return out


def counts(s):
    """month-end cycle counts on the last business day of January to November, from about 15:00, and the year-end
    physical inventory after closing, shelf by shelf with the door shut between shelves: on 30 December at the
    stores in COUNT_30DEC, on 31 December at the rest"""
    r = np.random.default_rng(seed(s["no"], 2))
    out = []
    for mo in range(1, 12):
        last = dt.date(2026, mo + 1, 1) - dt.timedelta(days=1)
        while last.weekday() >= 5:
            last -= dt.timedelta(days=1)
        out.append((at((last - dt.date(2026, 1, 1)).days, 15, int(r.integers(0, 40))),
                    int(max(5, round(r.normal(s["count"], 1.5))))))
    day = doy(12, 30) if s["no"] in COUNT_30DEC else doy(12, 31)
    a = at(day, 21, int(r.integers(5, 25)))
    for _ in range(3):
        k = int(r.integers(3, 6))
        out.append((a, k))
        a += k + int(r.integers(4, 7))
    return out


def year_end_count(s):
    """the physical minute the year-end physical inventory closed: after the last shelf"""
    return counts(s)[-1][0] + counts(s)[-1][1] + 2


def events(s):
    """outages, doors left ajar and failing thermostats: (kind, start minute, minutes, level)"""
    r = np.random.default_rng(seed(s["no"], 3))
    out = []
    for name in s["ex"].get("storms", []):
        d, hh, mm = STORMS[name]
        out.append(("outage", at(d, hh, mm) + int(r.integers(-25, 25)), int(r.uniform(200, 560)), ROOM))
    for (d, k) in s["ex"].get("ajar", []):
        out.append(("ajar", at(d, 21, int(r.integers(5, 40))), k, 13.5))
    for (d, k, lvl) in s["ex"].get("drift", []):
        out.append(("thermostat", at(d, int(r.integers(0, 23)), 0), k, lvl))
    return out


def simulate(s):
    r = np.random.default_rng(seed(s["no"], 0))
    amp, per = (0.25, 14) if s["unit"] == "pharma" else (0.7, 36)
    target = s["sp"] + amp * np.sign(np.sin(2 * np.pi * (_m + r.integers(0, per)) / per))
    tau = np.full(N, 5.0 if s["unit"] == "pharma" else 9.0)
    lam = s["door"] / 780.0 * SEASON * TOD * OPEN
    opens = np.where(r.random(N) < lam)[0]
    for a in opens:
        target[a] = ROOM
        tau[a] = TAU_OPEN / r.uniform(0.25, 0.7)
    if "defrost" in s["ex"]:
        peak, dur = s["ex"]["defrost"]
        for k in range(0, N, 720):
            off = k + 200 + int(r.integers(-15, 15))
            lvl = (peak if WARM_SEASON[min(off, N - 1)] else peak - 1.6) + r.normal(0, 0.15)
            d = int(dur + r.normal(0, 4))
            target[off:off + d] = lvl
            tau[off:off + d] = 9.0
    for (a, k, _) in deliveries(s):
        target[a:a + k] = ROOM
        tau[a:a + k] = TAU_OPEN
    for (a, k) in counts(s):
        target[a:a + k] = ROOM
        tau[a:a + k] = TAU_OPEN
    for (kind, a, k, lvl) in events(s):
        target[a:a + k] = lvl
        tau[a:a + k] = {"outage": 210.0, "ajar": 22.0, "thermostat": 45.0}[kind]
    air = ifilter(target, np.exp(-1.0 / tau), s["sp"])
    probe = ifilter(air, np.exp(-1.0 / TAU_P), s["sp"])
    carton = ifilter(air, np.exp(-1.0 / TAU_V), s["sp"])
    return air, probe, carton, opens


def pilot_dates(no):
    """installation and logger collection (physical minutes) for a pilot store"""
    r = np.random.default_rng(seed(no, 4))
    k = PILOT.index(no)
    day = 125 + 7 * k + int(r.integers(0, 4))          # one store a week from early May
    if dt.date(2026, 1, 1).toordinal() + day and (dt.date(2026, 1, 1) + dt.timedelta(days=day)).weekday() >= 5:
        day += 2
    inst = at(day, int(r.integers(9, 15)), int(r.integers(0, 59)))
    coll = inst + int(r.integers(13, 16)) * 1440 + int(r.integers(-120, 120))
    return inst, coll


def gaps(s, rec_t):
    """record indices dropped: a logger replacement and battery changes, all in quiet hours"""
    r = np.random.default_rng(seed(s["no"], 5))
    drop = np.zeros(len(rec_t), bool)
    spans = []
    if s["no"] in REPLACED:
        d, hh, mm, g = REPLACED[s["no"]]
        a = at(d, hh, mm)
        spans.append((a, a + g, "replaced"))
    for _ in range(int(r.integers(1, 3))):
        d = int(r.integers(20, 340))
        a = at(d, 2, int(r.integers(0, 50)))
        spans.append((a, a + int(r.integers(20, 50)), "battery"))
    for a, b, _ in spans:
        drop |= (rec_t >= a) & (rec_t < b)
    return drop, spans


def everything():
    """every store's records and the truth they come from"""
    out = {}
    for s in STORES:
        air, probe, carton, opens = simulate(s)
        r = np.random.default_rng(seed(s["no"], 6))
        rec_t = np.arange(0, N - STEP + 1, STEP)
        cs = np.concatenate([[0.0], np.cumsum(probe)])
        rec_x = (cs[rec_t + STEP] - cs[rec_t]) / STEP + r.normal(0, 0.03, len(rec_t))
        e = dict(store=s, rec_t=rec_t, rec_x=rec_x, carton_at=carton[rec_t], air=None)
        drop, spans = gaps(s, rec_t)
        e["gaps"] = spans
        keep = ~drop
        if s["no"] in PILOT:
            inst, coll = pilot_dates(s["no"])
            e["inst"], e["coll"] = inst, coll
            keep &= rec_t < coll
            c0 = inst + int(r.integers(0, STEP))
            ct = np.arange(c0, N - 1, STEP)
            e["cl_t"] = ct
            e["cl_x"] = carton[ct] + r.normal(0, 0.04, len(ct))
        e["rec_t"], e["rec_x"], e["carton_at"] = rec_t[keep], rec_x[keep], e["carton_at"][keep]
        e["carton"] = carton
        e["deliveries"] = deliveries(s)
        e["counts"] = counts(s)
        e["opens"] = opens
        e["events"] = events(s)
        out[s["no"]] = e
    return out


def in_year(t):
    return (t >= WARM) & (t < WARM + 525600)

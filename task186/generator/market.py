"""The province's retail fuel market as the reporting platform saw it, 1 January 2025 to 15 November 2026.

Every urban area's pump margins cycle: stations undercut one another a little at a time for five to nine weeks and then
restore together, so an area's margin is a sawtooth of its own period, amplitude and phase. A station prices off the
latest published terminal rack price, adds the levy in force and its margin, and adds the 5 per cent sales tax. Stations
a brand prices itself (company-run sites and commission agents) change price when the brand's pricing desk pushes its
batches, at the same minutes every day; dealers change price on their own. On 1 January 2026 Tallis Petroleum's pricing
desk raised the margin on every station it prices by about 3 cents a litre beyond the levy rise, and kept it there."""
import datetime as dt
import math

import numpy as np

import world as W

N = len(W.DAYS)
CH = W.DAY_INDEX[W.CHANGE]
TALLIS_EXCESS = 3.0                   # cents a litre, before tax, from 1 January 2026 at Tallis's own-priced stations


def rng(*key):
    return np.random.default_rng([W.SEED] + [int(k) for k in key])


# ---------------------------------------------------------------- the terminal rack (dollars a litre, ex levy and tax)
def published(d):
    return d.weekday() < 5 and d not in W.HOLIDAYS


RACK_DAYS = W.days_between(dt.date(2024, 12, 2), W.LOG_END)


def rack_tables():
    """{product: {date: dollars a litre}} on publication days"""
    g = rng(1)
    n = len(RACK_DAYS)
    t = np.arange(n)
    season = 0.035 * np.sin(2 * np.pi * (t - 100) / 365.25)
    walk = np.cumsum(g.normal(0, 0.0065, n))
    walk = walk - 0.004 * np.cumsum(walk) / np.arange(1, n + 1)
    rul = 0.832 + season + walk
    pul = rul + 0.128 + 0.004 * np.sin(t / 40.0)
    dsl = 0.871 + 0.6 * season + np.cumsum(g.normal(0, 0.006, n)) * 0.9
    out = {"RUL": {}, "PUL": {}, "ULSD": {}}
    for k, d in enumerate(RACK_DAYS):
        if published(d):
            out["RUL"][d] = round(float(rul[k]), 4)
            out["PUL"][d] = round(float(pul[k]), 4)
            out["ULSD"][d] = round(float(dsl[k]), 4)
    return out


def latest(table, d):
    """the latest published price on or before d"""
    while d not in table:
        d -= dt.timedelta(days=1)
    return table[d]


# ---------------------------------------------------------------- the areas' price cycles (cents a litre of margin)
# the percentile, within the area's own 28-day changes at other dates, at which each area's change across
# 1 January 2026 falls: the two coastal areas near the top of their range, Pellow's three a little lower, the four
# areas holding Tallis's own-priced stations about the middle, the rest below
PHASE_TARGET = {"BRK": .925, "POS": .915, "KEL": .77, "TAM": .745, "LIN": .775, "TRF": .66, "QUA": .62,
                "GRY": .50, "DUN": .46, "MRB": .54, "HOL": .48, "SAL": .22, "BRC": .17, "WYN": .25, "ELV": .31,
                "REN": .14}


def _saw(t, period, amp, phase):
    return amp * (0.5 - ((t / period + phase) % 1.0))


def window_change(series, k, w=W.WINDOW):
    return float(np.mean(series[k:k + w]) - np.mean(series[k - w:k]))


def placebo_indices():
    """day indices whose windows hold no levy change"""
    out = []
    for k in range(W.WINDOW, N - W.WINDOW + 1):
        if k <= CH - W.WINDOW or k >= CH + W.WINDOW:
            out.append(k)
    return out


def area_cycles():
    g = rng(2)
    t = np.arange(N, dtype=float)
    cyc = {}
    params = {}
    pl = placebo_indices()
    for a in W.AREA_CODES:
        period = float(g.uniform(36, 62))
        amp = float(g.uniform(2.45, 3.05))
        target = PHASE_TARGET[a]
        best, best_err = 0.0, 9.0
        for ph in np.linspace(0, 1, 720, endpoint=False):
            s = _saw(t, period, amp, ph)
            d0 = window_change(s, CH)
            pct = float(np.mean([window_change(s, k) < d0 for k in pl]))
            if abs(pct - target) < best_err:
                best, best_err = float(ph), abs(pct - target)
        cyc[a] = _saw(t, period, amp, best)
        params[a] = (period, amp, best)
    return cyc, params


# ---------------------------------------------------------------- the stations
class Station:
    def __init__(self, uid, area, model, ownership):
        self.uid = uid
        self.area = area
        self.model = model                  # COCO, CODO, COMM, DODO at the start of the log
        self.ownership = ownership          # company or dealer: who owns the site
        self.brands = []                    # [(brand, from, to or None)]
        self.models = []                    # [(model, from, to or None)]
        self.opened = W.LOG_START - dt.timedelta(days=1)
        self.closed = None                  # first day closed
        self.old_id = None
        self.new_id = None
        self.street = ""
        self.size = 0.0                     # litres of regular a month at an average month
        self.base = 0.0
        self.lag = 0
        self.diff_pul = 0
        self.style = 0
        self.sfn = None
        self.frame_added = None

    def brand_on(self, d):
        for b, f, to in self.brands:
            if f <= d and (to is None or d < to):
                return b
        return None

    def model_on(self, d):
        for m, f, to in self.models:
            if f <= d and (to is None or d < to):
                return m
        return None

    def open_on(self, d):
        return self.opened <= d and (self.closed is None or d < self.closed)

    def brand_priced_on(self, d):
        return self.model_on(d) in ("COCO", "COMM") and self.brand_on(d) != W.INDEPENDENT


MIX = {  # brand: (COCO, COMM, CODO, DODO)
    "TAL": (16, 12, 10, 54), "HBL": (9, 6, 5, 32), "PEL": (7, 5, 4, 30), "WEX": (6, 4, 3, 32),
    "OXB": (5, 3, 5, 32), "STL": (4, 6, 2, 33), "GAR": (3, 2, 4, 36), "IND": (0, 0, 0, 30),
}
POSITIVE = ["BRK", "POS", "KEL", "TAM", "LIN", "TRF", "QUA"]
TALLIS_OWN = ["GRY", "DUN", "MRB", "HOL"]
NEGATIVE = ["SAL", "BRC", "WYN", "ELV", "REN"]
INDEP_FAMILY = ["Halvorsen", "Mackey", "Duchesne", "Roblin", "Kowalchuk", "Petrie", "Lindgren", "Bouchard",
                "Tremblay", "Szabo", "Gauthier", "Okafor", "Brannigan", "Featherstone", "Vasquez", "Ruddick"]
STREETS = ["Main Street", "King Street", "Harbour Road", "Mill Road", "Station Road", "Lakeshore Drive", "Highway 7",
           "Highway 12", "Highway 3", "Church Street", "Victoria Avenue", "Queen Street", "Water Street", "Bay Road",
           "Ridge Road", "Park Avenue", "Front Street", "Elm Street", "Cedar Avenue", "Maple Avenue", "Pine Street",
           "Wellington Street", "Dundas Road", "Erie Street", "Market Street", "Albert Street", "Spruce Road",
           "Ferry Road", "Quarry Road", "Orchard Lane", "Industrial Drive", "Airport Road", "College Street",
           "North Road", "South Road", "Bridge Street", "Canal Street", "Hillcrest Avenue", "Union Street",
           "Riverside Drive"]


def _area_plan(g, brand, n_priced, n_dealer):
    """areas for a brand's own-priced and dealer stations"""
    if brand == "HBL":
        pool = ["BRK"] * 24 + ["POS"] * 22 + list(g.choice(["TRF", "QUA", "KEL"], 6))
    elif brand == "PEL":
        pool = ["KEL"] * 14 + ["TAM"] * 13 + ["LIN"] * 12 + list(g.choice(["GRY", "BRC", "REN", "MRB", "HOL"], 7))
    elif brand == "TAL":
        priced = [a for a in TALLIS_OWN for _ in range(7)]
        dealers = list(g.choice(NEGATIVE, 38)) + list(g.choice(["GRY", "DUN", "MRB", "HOL"], 10)) + \
            list(g.choice(["TRF", "QUA"], 6)) + list(g.choice(["KEL", "TAM", "LIN"], 10))
        return priced, dealers[:n_dealer]
    elif brand == W.INDEPENDENT:
        pool = list(g.choice(W.AREA_CODES, n_priced + n_dealer))
    else:
        n = n_priced + n_dealer
        k = int(round(0.72 * n))
        rest = [a for a in W.AREA_CODES if a not in POSITIVE]
        pool = list(g.choice(POSITIVE, k)) + list(g.choice(rest, n - k))
    g.shuffle(pool)
    return pool[:n_priced], pool[n_priced:n_priced + n_dealer]


def roster():
    g = rng(3)
    stations = []
    uid = 0
    for brand in W.CODES + [W.INDEPENDENT]:
        coco, comm, codo, dodo = MIX[brand]
        priced_areas, dealer_areas = _area_plan(g, brand, coco + comm, codo + dodo)
        models = ["COCO"] * coco + ["COMM"] * comm
        for m, a in zip(models, priced_areas):
            stations.append((brand, a, m))
        dm = ["CODO"] * codo + ["DODO"] * dodo
        for m, a in zip(dm, dealer_areas):
            stations.append((brand, a, m))
    out = []
    used_streets = set()
    for brand, a, m in stations:
        uid += 1
        s = Station(uid, a, m, "company" if m in ("COCO", "CODO") else "dealer")
        s.size = float(np.exp(g.normal(np.log(310_000), 0.38)))
        s.base = float(g.uniform(8.2, 11.6))
        s.lag = int(g.choice([0, 0, 1, 1, 2]))
        s.diff_pul = int(g.choice([180, 190, 200, 210, 220, 230, 240]))
        s.style = int(g.integers(0, 4))
        while True:
            st = "%d %s" % (int(g.integers(1, 120)) * 10 + int(g.integers(0, 10)), str(g.choice(STREETS)))
            if (a, st) not in used_streets:
                used_streets.add((a, st))
                break
        s.street = st
        s.hist_opened = dt.date(int(g.integers(1968, 2024)), int(g.integers(1, 13)), int(g.integers(1, 29)))
        s.brands = [(brand, max(s.hist_opened, dt.date(2008, 1, 1) + dt.timedelta(days=int(g.integers(0, 5800)))),
                     None)]
        s.models = [(m, s.brands[0][1], None)]
        s.indep_name = "%s %s" % (str(g.choice(INDEP_FAMILY)), str(g.choice(["Gas Bar", "Fuels", "Service Centre",
                                                                               "Gas & Go", "Fuel Stop"])))
        out.append(s)
    _events(g, out)
    _identifiers(g, out)
    return out


REISSUE = [  # (closing dealer's brand, its closing day, brand and model of the station the reference goes to, the day
             # that station is added to the survey frame)
    ("HBL", dt.date(2026, 3, 16), "GAR", "DODO", dt.date(2026, 8, 3)),
    ("PEL", dt.date(2026, 4, 1), "TAL", "DODO", dt.date(2026, 8, 17)),
    ("WEX", dt.date(2026, 4, 20), "HBL", "COCO", dt.date(2026, 9, 1)),
    ("OXB", dt.date(2026, 5, 4), "PEL", "COCO", dt.date(2026, 9, 14)),
    ("STL", dt.date(2026, 6, 1), "WEX", "DODO", dt.date(2026, 9, 28)),
    ("GAR", dt.date(2026, 6, 22), "OXB", "DODO", dt.date(2026, 10, 5)),
    ("TAL", dt.date(2026, 7, 13), "STL", "COMM", dt.date(2026, 10, 13)),
    ("IND", dt.date(2026, 7, 27), "IND", "DODO", dt.date(2026, 10, 26)),
]


def _new_station(g, out, brand, area, model, opened):
    s = Station(max(x.uid for x in out) + 1, area, model, "company" if model in ("COCO", "CODO") else "dealer")
    s.brands = [(brand, opened, None)]
    s.models = [(model, opened, None)]
    s.opened = opened
    s.size = float(np.exp(g.normal(np.log(290_000), 0.35)))
    s.base = float(g.uniform(8.2, 11.6))
    s.lag = int(g.choice([0, 1, 2]))
    s.diff_pul = int(g.choice([190, 200, 210, 220]))
    s.style = int(g.integers(0, 4))
    s.hist_opened = opened
    s.indep_name = "%s %s" % (str(g.choice(INDEP_FAMILY)), str(g.choice(["Gas Bar", "Fuels", "Fuel Stop"])))
    taken = {(x.area, x.street) for x in out}
    while True:
        st = "%d %s" % (int(g.integers(1, 120)) * 10 + int(g.integers(0, 10)), str(g.choice(STREETS)))
        if (area, st) not in taken:
            s.street = st
            break
    out.append(s)
    return s


def _events(g, out):
    """closures, openings, rebrandings and changes of pricing over the log"""
    def pick(brand, model=None, areas=None, exclude=()):
        c = [s for s in out if s.brands[0][0] == brand and s.closed is None and s.opened <= W.LOG_START
             and (model is None or s.model == model) and (areas is None or s.area in areas) and s.uid not in exclude
             and len(s.brands) == 1]
        return c[int(g.integers(0, len(c)))]
    used = set()
    # the eight dealers whose survey references were later reissued: they close between March and July 2026
    closing = []
    for old_brand, when, new_brand, new_model, added in REISSUE:
        o = pick(old_brand, "DODO", exclude=used)
        used.add(o.uid)
        o.closed = when
        closing.append(o)
    # other closures, one before the change and three after
    for brand, when in (("WEX", dt.date(2025, 6, 2)), ("OXB", dt.date(2026, 7, 6)), ("STL", dt.date(2026, 9, 8)),
                        ("IND", dt.date(2026, 5, 11))):
        s = pick(brand, "DODO", exclude=used)
        used.add(s.uid)
        s.closed = when
    # openings: two in December 2025 (too few days before the change to be examined), three in 2026
    for brand, area, model, when in (("GAR", "TRF", "DODO", dt.date(2025, 12, 15)),
                                     ("OXB", "SAL", "DODO", dt.date(2025, 12, 19)),
                                     ("WEX", "QUA", "DODO", dt.date(2026, 3, 9)),
                                     ("PEL", "ELV", "COMM", dt.date(2026, 5, 25)),
                                     ("IND", "BRC", "DODO", dt.date(2026, 6, 29))):
        _new_station(g, out, brand, area, model, when)
    # rebrandings, effective on the first of a month
    for frm, to, area, when in (("PEL", "OXB", "KEL", dt.date(2026, 2, 1)), ("PEL", "OXB", "KEL", dt.date(2026, 2, 1)),
                                ("WEX", "GAR", None, dt.date(2026, 7, 1)), ("GAR", "TAL", None, dt.date(2026, 10, 1)),
                                ("WEX", "STL", None, dt.date(2025, 9, 1))):
        s = pick(frm, "DODO", [area] if area else None, exclude=used)
        used.add(s.uid)
        b0 = s.brands[0]
        s.brands = [(b0[0], b0[1], when), (to, when, None)]
    # pricing changes: a Tallis commission agency ends, a Strathlowe company site is leased to a dealer
    for brand, model, new_model, when in (("TAL", "COMM", "DODO", dt.date(2026, 9, 1)),
                                          ("STL", "COCO", "CODO", dt.date(2026, 10, 1))):
        s = pick(brand, model, TALLIS_OWN if brand == "TAL" else None, exclude=used)
        used.add(s.uid)
        m0 = s.models[0]
        s.models = [(m0[0], m0[1], when), (new_model, when, None)]
    # their references go to stations that had been trading for years but join the survey frame from August 2026
    h = rng(7)
    for o, (old_brand, when, new_brand, new_model, added) in zip(closing, REISSUE):
        c = [s for s in out if s.brands[0][0] == new_brand and s.model == new_model and s.closed is None and
             s.opened <= W.LOG_START and len(s.brands) == 1 and len(s.models) == 1 and s.uid not in used]
        n = c[int(h.integers(0, len(c)))]
        used.add(n.uid)
        n.reissue_of, n.frame_joined = o.uid, added
        o.reissued_to = n.uid


def _identifiers(g, out):
    """the platform's numbers: five-digit numbers to 7 June 2026, area-prefixed numbers from 8 June 2026; survey
    reference numbers from the sales survey frame"""
    olds = g.choice(np.arange(20000, 69999), size=len(out), replace=False)
    for s, o in zip(sorted(out, key=lambda s: s.uid), olds):
        if s.opened < W.RENUMBER:
            s.old_id = str(int(o))
    seq = {}
    for s in sorted(out, key=lambda s: (s.area, s.uid)):
        if s.closed is None or s.closed > W.RENUMBER:
            seq[s.area] = seq.get(s.area, 100) + int(g.integers(1, 9))
            s.new_id = "%s-%04d" % (s.area, seq[s.area])
    sfns = g.choice(np.arange(10100, 49900), size=len(out), replace=False)
    by_uid = {s.uid: s for s in out}
    for s, f in zip(sorted(out, key=lambda s: s.uid), sfns):
        if getattr(s, "reissue_of", None):
            continue
        s.sfn = "FS-%05d" % int(f)
        s.frame_added = min(dt.date(2019, 4, 1) + dt.timedelta(days=int(g.integers(0, 1500))), s.opened) \
            if s.opened <= W.LOG_START else s.opened
    for s in out:
        if getattr(s, "reissue_of", None):
            s.sfn = by_uid[s.reissue_of].sfn
            s.frame_added = s.frame_joined


def station_id_on(s, d):
    return s.new_id if (d >= W.RENUMBER and s.new_id) else s.old_id


def trading_name(s, d=None):
    b = s.brand_on(d or W.AS_OF) or s.brands[-1][0]
    if b == W.INDEPENDENT:
        return "%s %s" % (s.indep_name, W.AREA_NAME[s.area])
    return "%s %s %s" % (W.NAME[b], W.AREA_NAME[s.area], s.street)


# ---------------------------------------------------------------- prices
BATCH = {"TAL": (352, 787), "HBL": (371, 862), "PEL": (340, 805), "WEX": (390, 840), "OXB": (365, 790),
         "STL": (380, 870), "GAR": (345, 815)}


def margin_targets(stations, cyc):
    """each station's target margin (cents a litre before tax, net of levy and rack) for every day of the log"""
    g = rng(4)
    out = {}
    for s in stations:
        base = cyc[s.area]
        lagged = np.r_[np.full(s.lag, base[0]), base[:N - s.lag]] if s.lag else base
        m = s.base + lagged + g.normal(0, 0.15, N)
        if s.brands[0][0] == "TAL" and s.model in ("COCO", "COMM"):
            for k in range(CH, N):
                if s.brand_priced_on(W.DAYS[k]) and s.brand_on(W.DAYS[k]) == "TAL":
                    m[k] += TALLIS_EXCESS
        out[s.uid] = m
    return out


def simulate():
    """every station's posted regular prices: {uid: [(day index, local minute, price in tenths of a cent)]}"""
    rack = rack_tables()
    cyc, params = area_cycles()
    stations = roster()
    targets = margin_targets(stations, cyc)
    events = {}
    for s in stations:
        g = rng(5, s.uid)                 # each station its own stream, so one station's dates move no other's prices
        ev = []
        cur = None
        m = targets[s.uid]
        for k, d in enumerate(W.DAYS):
            if not s.open_on(d):
                cur = None if not s.open_on(d) else cur
                continue
            r = latest(rack["RUL"], d) * 100.0
            tgt = int(round((r + W.levy_regular(d) + m[k]) * (1 + W.SALES_TAX) * 10))
            priced = s.brand_priced_on(d)
            if cur is None:
                ev.append((k, int(g.integers(330, 420)), tgt))
                cur = tgt
                continue
            if d in (W.PREV_CHANGE, W.CHANGE):
                cur = tgt
                ev.append((k, int(g.integers(1, 31)), tgt))
                continue
            if priced:
                b = s.brand_on(d)
                t1, t2 = BATCH[b]
                if abs(tgt - cur) >= 2:
                    ev.append((k, t1, tgt))
                    cur = tgt
                adj = tgt - int(g.choice([0, 0, 1, 2]))
                if abs(adj - cur) >= 2:
                    ev.append((k, t2, adj))
                    cur = adj
            else:
                own = tgt + int(round(g.normal(0, 1.2)))
                if abs(own - cur) >= 3:
                    minute = int(g.integers(330, 1290))
                    ev.append((k, minute, own))
                    cur = own
        events[s.uid] = ev
    return {"rack": rack, "cyc": cyc, "params": params, "stations": stations, "targets": targets, "events": events}


# ---------------------------------------------------------------- the platform's outages
OUTAGES = [  # local day, start minute, end minute
    (dt.date(2025, 3, 18), 610, 830), (dt.date(2025, 7, 22), 400, 690), (dt.date(2025, 10, 9), 900, 1130),
    (dt.date(2026, 2, 24), 350, 560), (dt.date(2026, 5, 5), 700, 980), (dt.date(2026, 9, 15), 480, 735),
]


def log_rows(sim):
    """the regular price-change log as the platform holds it: one row per received submission, changes effective
    during an outage received after it ends and some received twice when the platform re-sent its queue"""
    g = rng(6)
    rows = []
    outage_by_day = {}
    for d, a, b in OUTAGES:
        outage_by_day.setdefault(d, []).append((a, b))
    stats = {i: [0, 0, set()] for i in range(len(OUTAGES))}
    for s in sim["stations"]:
        for k, minute, price in sim["events"][s.uid]:
            d = W.DAYS[k]
            eff = W.to_utc(d, minute)
            sid = station_id_on(s, d)
            rec = eff + dt.timedelta(seconds=int(g.integers(20, 240)))
            twice = False
            for i, (od, a, b) in enumerate(OUTAGES):
                if od == d and a <= minute < b:
                    rec = W.to_utc(d, b) + dt.timedelta(seconds=int(g.integers(60, 1500)))
                    stats[i][0] += 1
                    stats[i][2].add(sid)
                    if g.random() < 0.45:
                        twice = True
                        stats[i][1] += 1
            rows.append((sid, eff, price, rec))
            if twice:
                rows.append((sid, eff, price, rec + dt.timedelta(minutes=int(g.integers(7, 40)))))
    rows.sort(key=lambda r: (r[3], r[0], r[1]))
    return rows, stats

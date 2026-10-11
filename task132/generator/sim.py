"""The simulated truth: substations and their bays, the VPR-340 fleet, every PSU module fitted to it since
installation (originals and replacements), every PSU failure, and the renewal programme.

A PSU module wears out with its own age. When one fails the relay is out until the corrective work order
completes, and the module fitted then starts again at age zero. The world runs from 1992; the EAM only ever
sees January 2021 on, plus the module in each position at go-live with the fitted date the legacy system held.
"""
import datetime as dt
import functools

import numpy as np
import pandas as pd

import world as W

# station names in the Ontario mix: surnames and roads the stations were named for, English, Scottish and French
# localities, and Indigenous-derived names, all invented for Tarrock's service area
SURNAMES = ["Tamblyn", "Garrow", "Lattimer", "Brodie", "McVean", "Pennock", "Ruttan", "Sproule", "Thackery", "Stinson",
            "Kerrigan", "Dowling", "Gibbard", "Hurlbut", "Lockhart", "Marwood", "Nesbitt", "Prentice", "Quinlan",
            "Rennick", "Tolton", "Varcoe", "Whitlock", "Yeoman", "Bellamy", "Carscadden", "Doupe", "Ellerby", "Fawcett",
            "Gilchrist", "Hamill", "Jardine", "Mallory", "Oakes", "Purdy", "Rorke", "Treleaven", "Vandusen", "Wardrop",
            "Yardley", "Fairbairn", "Goodfellow", "Jessop", "Kinnear", "Lusk", "Pattinson", "Mulvihill", "Tweedie",
            "Urquhart", "Vokes", "Allingham", "Corrigan", "Grier", "Kearney", "McAlpine", "Pugsley", "Ritchie", "Wylie",
            "Hagarty", "Ostrander", "Ferrier", "Brebner"]
STREETS = [("", 0.42), (" Road", 0.16), (" Line", 0.1), (" Street", 0.07), (" Corners", 0.1), (" Mills", 0.07),
           (" Junction", 0.05), (" Sideroad", 0.03)]
ENGLISH = ["Tamarack Corners", "Sumac Heights", "Basswood Falls", "Hemlock Station", "Juniper Point", "Poplar Junction",
           "Clover Mills", "Hawthorn Ridge", "Briarcrest", "Marl Heights", "Cedarbank", "Ashlea", "Hollycrest",
           "Sprucemount", "Pinecroft", "Maplecrest", "Stonecroft", "Clayfield", "Churchview", "Northmount", "Highcroft",
           "Fairlea", "Bramblewood", "Thornbank", "Rushbrook", "Oakcrest"]
SCOTTISH = ["Glenvarra", "Dunmairn", "Kilmarra", "Balnacree", "Invercarrick", "Strathcorran", "Ardmorran", "Lochvane",
            "Torbrae", "Kinlarig", "Auchenlee", "Rossmara", "Craigellan", "Kintallan", "Glenardie", "Dunallen",
            "Balcarran", "Ardcarron", "Lochardie", "Benvarrow", "Glen Tavish"]
FRENCH = ["Beaumarais", "Bellerive", "Boisclair", "Montbrun", "Ch\u00eanevert", "Pointe-Verdure", "Lac-Brunet",
          "Rivi\u00e8re-Sauvage", "Val-Ombre", "Coteau-Vert", "Pr\u00e9-Fontaine", "Lacroix Line", "Beaucourt", "Clairval",
          "Boisjoli", "Lafreni\u00e8re Road", "Pointe-aux-Saules", "Lac-Sauv\u00e9", "Rivi\u00e8re-aux-Pins", "Belle-Prairie",
          "C\u00f4te-Rouge", "Fontbrune"]
INDIGENOUS = ["Ossawin Creek", "Wanatami Road", "Minnetaga", "Opekona Bay", "Mishawana", "Wapasaga", "Kabeshing",
              "Nibawin Point", "Kawanaki", "Waskeda", "Pemachi"]
CURRENT_REGIONS = ["North", "Central", "South"]
PLAN_LAST = dt.date(2035, 10, 1)       # last autumn outage window inside the programme period
PLAN_FIRST = dt.date(2026, 10, 1)      # first commissioning month the approved 2026 program can still plan
PLAN_25_FIRST = dt.date(2026, 4, 1)    # first month a 2025-plan scheme could be moved back to
LEGACY_REGIONS = ["Lakeshore", "Ridge", "Valley", "Harbour"]
SEASON = np.array([0.3, 0.3, 0.6, 1.4, 1.6, 1.3, 0.5, 0.5, 1.3, 1.6, 1.3, 0.3])   # outage windows, Jan..Dec


def month_add(d, n):
    y, m = d.year + (d.month - 1 + n) // 12, (d.month - 1 + n) % 12 + 1
    return dt.date(y, m, 1)


def months_between(a, b):
    """month starts from a (inclusive) to b (exclusive)"""
    out, d = [], dt.date(a.year, a.month, 1)
    while d < b:
        out.append(d)
        d = month_add(d, 1)
    return out


def mindex(d):
    return d.year * 12 + d.month - 1


def age_on(fitted, first):
    """completed years on the first day of a month"""
    return first.year - fitted.year - ((first.month, 1) < (fitted.month, fitted.day))


def first_month(d):
    """first month a module or relay placed in service on d counts: in service on the first day"""
    m = dt.date(d.year, d.month, 1)
    return m if d.day == 1 else month_add(m, 1)


def weekday(rng, d, sat=0.04):
    """the legacy draw: move a date off the weekend (a few Saturday jobs stay). The world's own stream still makes
    these draws, so the failure simulation is unchanged; the date a planned job lands on is then taken from
    bday_like, which draws it among working days directly."""
    if d.weekday() == 5 and rng.random() < sat:
        return d
    while d.weekday() >= 5:
        d = d + dt.timedelta(days=1)
    return d


# ---------------------------------------------------------------- working days (Ontario)

def _easter(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    return dt.date(y, (h + l - 7 * m + 114) // 31, (h + l - 7 * m + 114) % 31 + 1)


def _monday(y, month, n):
    d = dt.date(y, month, 1)
    return d + dt.timedelta(days=(7 - d.weekday()) % 7 + 7 * (n - 1))


@functools.lru_cache(maxsize=None)
def holidays(y):
    """Ontario statutory holidays as the utility and its suppliers observe them; one that falls at a weekend is
    taken on the next working day"""
    hs = {_easter(y) - dt.timedelta(days=2), _monday(y, 9, 1), _monday(y, 10, 2)}
    if y >= 2008:
        hs.add(_monday(y, 2, 3))
    may24 = dt.date(y, 5, 24)
    hs.add(may24 - dt.timedelta(days=may24.weekday()))
    for d in (dt.date(y, 1, 1), dt.date(y, 7, 1), dt.date(y, 12, 25), dt.date(y, 12, 26)):
        while d.weekday() >= 5 or d in hs:
            d += dt.timedelta(days=1)
        hs.add(d)
    return frozenset(hs)


def is_bday(d):
    return d.weekday() < 5 and d not in holidays(d.year)


def bdays(a, b):
    """working days from a to b inclusive"""
    out, d = [], a
    while d <= b:
        if is_bday(d):
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def add_bdays(d, n):
    """the n-th working day after d (n = 0: d itself when it is a working day, else the next one)"""
    while not is_bday(d):
        d += dt.timedelta(days=1)
    for _ in range(int(n)):
        d += dt.timedelta(days=1)
        while not is_bday(d):
            d += dt.timedelta(days=1)
    return d


def pick_bday(rng, a, b):
    """a working day drawn uniformly from a to b"""
    c = bdays(a, b)
    while not c:
        b += dt.timedelta(days=1)
        c = bdays(a, b)
    return c[int(rng.integers(len(c)))]


def bday_like(rng, d):
    """a working day counted from the same first day of a month as d, drawn across that window: the 2nd to the end
    of d's month, or for a date on the 1st the day itself (or, on a holiday, the last week of the month before).
    Every month-start count (first_month, age_on) is the same for the two dates."""
    m = dt.date(d.year, d.month, 1)
    if d.day == 1:
        return d if is_bday(d) else pick_bday(rng, m - dt.timedelta(days=7), m - dt.timedelta(days=1))
    return pick_bday(rng, dt.date(d.year, d.month, 2), month_add(m, 1) - dt.timedelta(days=1))


def station_names():
    """every station's name, from a stream of its own"""
    rn = np.random.default_rng([W.SEED, 60])
    w = np.array([p for _, p in STREETS])
    out = [s + STREETS[int(rn.choice(len(STREETS), p=w / w.sum()))][0] for s in SURNAMES]
    out += ENGLISH + SCOTTISH + FRENCH + INDIGENOUS
    assert len(out) == W.N_SUBS and len(set(out)) == len(out), (len(out), len(set(out)))
    rn.shuffle(out)
    return out


def substations(rng):
    names = station_names()
    kinds = ["TS"] * W.N_TS + ["DS"] * (W.N_SUBS - W.N_TS)
    rng.shuffle(kinds)
    rows, nts, nds = [], 0, 0
    for n, kind in zip(names, kinds):
        if kind == "TS":
            nts += 1
            code = "TS-%02d" % nts
        else:
            nds += 1
            code = "DS-%03d" % nds
        legacy = LEGACY_REGIONS[int(rng.choice(4, p=[0.27, 0.24, 0.27, 0.22]))]
        # 2024 reorganisation: Lakeshore -> North, Harbour -> South, Ridge and Valley split
        cur = {"Lakeshore": "North", "Harbour": "South"}.get(legacy) or (
            "Central" if rng.random() < 0.6 else ("North" if legacy == "Ridge" else "South"))
        ntx = int(rng.integers(2, 4)) if kind == "TS" else int(rng.integers(1, 3))
        nbus = 2 if kind == "TS" else (1 if rng.random() < 0.3 else 0)
        rows.append(dict(sub_code=code, sub_name=n, station_type=kind, region=cur, legacy_region=legacy,
                         n_tx=ntx, n_bus=nbus))
    return pd.DataFrame(rows)


def _install_day(rng, y, m):
    d = dt.date(y, m, int(rng.integers(1, 29)))
    return weekday(rng, d, sat=0.0)


def fleet(rng, subs):
    """VPR-340 relays, one per feeder bay: station campaigns 1992-2018, then feeders added later. Campaign bays are
    numbered first, added bays after them. A distribution station carries three to ten VPR-340 feeders; the
    transformer stations carry the rest."""
    yrs = np.arange(1992, 2019)
    w = 0.85 * np.exp(-0.5 * ((yrs - 2008) / 5.0) ** 2)
    w = w / w.sum() * 0.85 + (yrs <= 2000) * (0.15 / (yrs <= 2000).sum())
    w = w / w.sum()
    ts = subs[subs["station_type"] == "TS"].sample(n=W.TS_HOSTS, random_state=int(rng.integers(1e9)))
    ds = subs[subs["station_type"] == "DS"].sample(n=W.DS_HOSTS, random_state=int(rng.integers(1e9)))
    host = pd.concat([ts, ds]).sort_values("sub_code")
    is_ts = (host["station_type"] == "TS").to_numpy()
    counts = np.zeros(len(host), dtype=int)
    counts[~is_ts] = 3 + rng.binomial(7, 0.55, int((~is_ts).sum()))
    rest = W.N_RELAY - int(counts.sum()) - 14 * int(is_ts.sum())
    share = rng.gamma(6.0, 1.0, int(is_ts.sum()))
    counts[is_ts] = 14 + rng.multinomial(rest, share / share.sum())
    rows, rid = [], 0
    adj = np.random.default_rng([W.SEED, 7])
    for (_, s), c in zip(host.iterrows(), counts):
        camp = int(rng.choice(yrs, p=w))
        cm = int(rng.integers(3, 11))
        n_camp = max(2, int(round(c * (0.8 if rng.random() < 0.7 else 0.6))))
        inst = []
        for j in range(c):
            if j < n_camp:
                y, m = camp, min(12, max(1, cm + int(rng.integers(-1, 2))))
            else:
                y = int(min(2018, camp + rng.integers(1, 10)))
                m = int(rng.integers(1, 13))
            inst.append(_install_day(rng, y, m))
        inst.sort()
        # the date each relay went in, on a working day counted from the same first day of a month; the drawn date
        # (install_raw) stays behind for the world's own ordering
        moved = sorted(bday_like(adj, d) for d in inst)
        for j, (d0, d) in enumerate(zip(inst, moved)):
            rid += 1
            rows.append(dict(relay_key=rid, sub_code=s.sub_code, bay="F%02d" % (j + 1), install=d, install_raw=d0))
    return pd.DataFrame(rows)


def programme(rng, fl, subs):
    """Schemes in the approved 2026 programme for every substation still carrying VPR-340 relays (older
    stations tend to go first), schemes at stations without VPR-340, the superseded 2025 plan, and the
    stations rebuilt early (2022-2025). Large stations are replaced in two outage stages."""
    host = fl.groupby("sub_code").agg(first=("install_raw", "min"), n=("relay_key", "size")).reset_index()
    age = np.array([(W.ASOF - d).days / 365.25 for d in host["first"]])
    score = age + rng.normal(0, 13, len(host))
    order = np.argsort(np.argsort(-score))
    n = len(host)
    early = order < 6
    rest = [i for i in np.argsort(order) if not early[i]]
    unscheduled = set(rest[-9:])
    sched_idx = [i for i in rest if i not in unscheduled]
    # commissioning months: from the autumn 2026 outage window to 2035, about a dozen a year, mostly in the spring and
    # autumn windows
    months = months_between(PLAN_FIRST, dt.date(2036, 1, 1))
    mw = np.array([SEASON[m.month - 1] for m in months])
    picks = np.sort(rng.choice(len(months), len(sched_idx), replace=True, p=mw / mw.sum()))
    when = {i: months[p] for i, p in zip(sched_idx, picks)}
    rebuilt = {}
    for i in range(n):
        if early[i]:
            y = 2022 + int(order[i] % 4)
            rebuilt[i] = weekday(rng, dt.date(y, int(rng.choice([4, 5, 6, 9, 10, 11])), int(rng.integers(1, 29))), 0)
    rows = []
    for i, r in host.iterrows():
        bays = fl[fl["sub_code"] == r.sub_code]["bay"].tolist()
        rows.append(dict(sub_code=r.sub_code, n=int(r.n), first_bay=bays[0], last_bay=bays[-1],
                         plan_2026=when.get(i), unscheduled=i in unscheduled, retired_on=rebuilt.get(i)))
    prog = pd.DataFrame(rows)
    # two-stage schemes at the large stations: stage 2 one to three years after stage 1, inside the period
    prog["stage2_from"] = None
    prog["plan_2026_s2"] = None
    big = prog[(prog["n"] >= W.STAGE_MIN) & prog["plan_2026"].notna()].index.tolist()
    for i in big:
        p1 = prog.at[i, "plan_2026"]
        lag = int(rng.integers(W.STAGE_LAG[0], W.STAGE_LAG[1]))
        p2 = month_add(p1, lag)
        while SEASON[p2.month - 1] < 1.0:
            p2 = month_add(p2, 1)
        if p2 > W.PROGRAMME_END:
            continue
        k = prog.at[i, "n"] // 2 + int(rng.integers(-1, 2))
        prog.at[i, "stage2_from"] = "F%02d" % (k + 1)
        prog.at[i, "plan_2026_s2"] = p2
    # 2025 plan: one stage per scheme; 23 schemes moved by the 2026 revision (mostly deferred)
    p25 = list(prog["plan_2026"])
    movable = [i for i in range(n) if p25[i] is not None]
    for i in rng.choice(movable, 23, replace=False):
        shift = int(rng.integers(6, 31)) * (1 if rng.random() < 0.8 else -1)
        # a deferral past the period is held at the last autumn outage window inside it; the 2025 plan reached back to
        # the spring 2026 window
        p25[i] = min(PLAN_LAST, max(PLAN_25_FIRST, month_add(p25[i], -shift)))
    prog["plan_2025"] = p25
    # the first draft of the schemes at stations with no VPR-340: its draws stay in the world's stream, and the schemes
    # themselves are chosen from the register (docs.other_schemes)
    others = subs[~subs["sub_code"].isin(host["sub_code"])]
    pick = others.sample(n=17, random_state=int(rng.integers(1e9)))
    extra = []
    for _, s in pick.iterrows():
        m = months[int(rng.choice(len(months), p=mw / mw.sum()))]
        m25 = m if rng.random() < 0.8 else month_add(m, -int(rng.integers(6, 19)))
        extra.append(dict(sub_code=s.sub_code, plan_2026=m, plan_2025=max(PLAN_25_FIRST, m25)))
    return prog, pd.DataFrame(extra)


def cut_date(days, bay, nv):
    """the working day a bay is cut over in a station rebuild: transformer protection first, the VPR-340 feeders in
    bay order across the weeks of the cutover, newer feeders, bus protection, and the RTU on the last day"""
    n = len(days)
    if bay == "RTU":
        return days[-1]
    if bay.startswith("T"):
        return days[min(int(bay[1:]) - 1, n - 1)]
    if bay.startswith("B"):
        return days[max(0, n - 2)]
    j = int(bay[1:]) - 1
    if j < nv:
        return days[min(n - 1, 1 + (j * max(1, n - 3)) // nv)]
    return days[max(0, n - 3)]


def cutovers(subs, fl, prog):
    """Station rebuilds cut over bay by bay over several weeks of working days, inside the month that leaves the old
    relays in service on the first day of the rebuild month (so every month a relay is counted in is unchanged).
    Adds the working days of each rebuild to prog (cut_days) and each VPR-340's retirement to fl (retire)."""
    adj = np.random.default_rng([W.SEED, 9])
    ntx = dict(zip(subs["sub_code"], subs["n_tx"]))
    nbus = dict(zip(subs["sub_code"], subs["n_bus"]))
    prog = prog.copy()
    fl = fl.copy()
    days_of, retire = {}, {}
    for _, r in prog.iterrows():
        D = r["retired_on"]
        if D is None or isinstance(D, float):
            continue
        m = dt.date(D.year, D.month, 1)
        if D.day == 1:
            m = month_add(m, -1)
        L = bdays(dt.date(m.year, m.month, 2), month_add(m, 1) - dt.timedelta(days=1))
        mine = fl[fl["sub_code"] == r.sub_code].sort_values("bay")
        items = len(mine) + ntx[r.sub_code] + nbus[r.sub_code] + 3
        wlen = min(len(L), max(12, int(np.ceil(items / 1.5))))
        s0 = int(adj.integers(0, len(L) - wlen + 1))
        days = L[s0:s0 + wlen]
        days_of[r.sub_code] = days
        for k, bay in zip(mine["relay_key"], mine["bay"]):
            retire[k] = cut_date(days, bay, len(mine))
    prog["cut_days"] = [days_of.get(sc) for sc in prog["sub_code"]]
    fl["retire"] = [retire.get(k) for k in fl["relay_key"]]
    return fl, prog


def support_end(prog_row, bay):
    """first month a relay is no longer supported (its bay's commissioning month, or the month after the
    programme period ends)"""
    if prog_row["plan_2026"] is None or (isinstance(prog_row["plan_2026"], float)):
        return month_add(W.PROGRAMME_END, 1)
    s2 = prog_row["stage2_from"]
    if s2 is not None and isinstance(s2, str) and bay >= s2:
        return prog_row["plan_2026_s2"]
    return prog_row["plan_2026"]


class Returns:
    """Failed modules Tarrock sends to Veldtek under RMA once Veldtek's register is running, and the modules SB-15-02
    took out. A failed module waits at its store for the next shipment; two waiting at the same store within a couple
    of weeks often go in one box. Veldtek repairs a module, finds no fault or scraps it; a repaired module is back on
    the stores shelf a few days after Veldtek ships it, and the stores issue it to the next job that needs a spare.
    A box Veldtek has not received by its last save of the register before the count is still at the store."""

    def __init__(self):
        self.recs = []
        self.boxes = {}          # box number -> records
        self.open_boxes = []     # boxes not yet shipped
        self.shelf = []          # [date on the shelf, (relay_key, module)] repaired modules not yet issued
        self.made = {}           # (relay_key, module) -> build date of that module

    def _box(self, recs):
        b = len(self.boxes)
        self.boxes[b] = recs
        for r in recs:
            r["box"] = b
        self.open_boxes.append(b)

    def failed(self, rec, rr):
        """a failed module removed on rec['removed']: sent to Veldtek or not, its shipping date, its box"""
        if rr.random() > (0.5 if rec["kind"] == "LEGACY" else 0.55):
            return
        u = rr.random()
        lag = (int(rr.integers(2, 9)) if u < 0.55 else int(rr.integers(9, 19)) if u < 0.82 else
               int(rr.integers(19, 46)) if u < 0.95 else int(rr.integers(46, 111)))
        rec["ship"] = add_bdays(rec["removed"], lag)
        if rec["kind"] == "LEGACY" and rec["ship"] >= W.CUTOVER_HOLD:
            rec["ship"] = add_bdays(dt.date(2021, 1, 4), int(rr.integers(0, 9)))
        self.recs.append(rec)
        if rec["kind"] == "EAM":
            # a module still waiting at the same store and due out within two weeks of this one often goes in the same
            # box, which leaves when the later of the two would have
            for b in sorted(self.open_boxes, key=lambda b: (self.boxes[b][0]["ship"], b)):
                a = self.boxes[b]
                if (len(a) == 1 and a[0]["kind"] == "EAM" and a[0]["store"] == rec["store"]
                        and a[0]["ship"] >= rec["removed"] and abs((rec["ship"] - a[0]["ship"]).days) <= 14):
                    if rr.random() < 0.5:
                        a[0]["ship"] = rec["ship"] = max(a[0]["ship"], rec["ship"])
                        a.append(rec)
                        rec["box"] = b
                        return
                    break
        self._box([rec])

    def bulletin(self, recs, ship):
        for r in recs:
            r["ship"] = ship
            self.recs.append(r)
        if recs:
            self._box(recs)

    def ship_before(self, day):
        """every box that left before `day`: received, assessed and, if repaired, back on the shelf"""
        for b in [b for b in self.open_boxes if self.boxes[b][0]["ship"] < day]:
            self.open_boxes.remove(b)
            recs = self.boxes[b]
            rb = np.random.default_rng([W.SEED, 22, b])
            ship = max(r["ship"] for r in recs)
            lag = int(rb.integers(1, 4)) if rb.random() < 0.85 else int(rb.integers(4, 10))
            recv = add_bdays(ship, lag)
            for r in recs:
                r["ship"], r["received"] = ship, recv
                r["held"] = recv > W.REG_SAVED
                if r["held"]:
                    r["result"], r["returned"] = None, None
                    continue
                if r["kind"] == "SB":
                    r["result"], r["returned"] = "SCRAPPED (SB-15-02)", None
                    continue
                rm = np.random.default_rng([W.SEED, 23, r["relay_key"], r["module"]])
                evald = add_bdays(recv, int(rm.integers(4, 13)))
                u = rm.random()
                res = "REPAIRED" if u < 0.77 else ("NO FAULT FOUND" if u < 0.82 else "BEYOND ECONOMIC REPAIR")
                if res == "NO FAULT FOUND":
                    t = int(rm.integers(5, 19))
                else:
                    v = rm.random()
                    t = int(rm.integers(14, 33)) if v < 0.7 else int(rm.integers(32, 61)) if v < 0.92 else int(rm.integers(60, 121))
                    if recv.year >= 2026:
                        t = int(t * 1.25)
                back = None if res == "BEYOND ECONOMIC REPAIR" else add_bdays(recv, t)
                if evald > W.REG_SAVED or (back is not None and back > W.REG_SAVED):
                    res, back = "OPEN", None
                r["result"], r["returned"] = res, back
                if back is not None:
                    # Veldtek returns a module by overnight courier and the store counts it serviceable from the day it
                    # arrives; it goes out to a job one to five working days after Veldtek ships it, and a module Veldtek
                    # shipped before the count is on the shelf at the count
                    self.shelf.append([min(add_bdays(back, int(rm.integers(1, 6))), W.ASOF), (r["relay_key"], r["module"])])

    def issue(self, day, rr):
        """the module the stores issue for a job on `day`: the repaired module longest on the shelf (most jobs), or
        a module from new stock"""
        ready = sorted(s for s in self.shelf if s[0] <= day)
        if ready and rr.random() < 0.85:
            self.shelf.remove(ready[0])
            return ready[0][1]
        return None


def modules(rng, fl, prog, subs):
    """Every PSU module fitted to a VPR-340 position from installation to the extract date.

    Each month a module in service on the first day fails with the chance W.p_month gives for its age, its months in
    service and whether it came back from repair. The corrective work completes 0 to 6 days later (emergency work the
    same day), and the module fitted then is in service from the next first day of a month. Returns the module spells,
    the failures, the RMA flow, and each relay's build date."""
    keys = [int(k) for k in fl["relay_key"]]
    inst = fl["install"].tolist()
    stop = [d if isinstance(d, dt.date) else None for d in fl["retire"]]
    sub_of = fl["sub_code"].tolist()
    cur = dict(zip(subs["sub_code"], subs["region"]))
    leg = dict(zip(subs["sub_code"], subs["legacy_region"]))
    n = len(keys)
    # each relay's build date (some sat in stores a year or more before they went in) and its first module's
    relay_mfg, made = [], []
    for i in range(n):
        r = np.random.default_rng([W.SEED, 50, keys[i]])
        lag = int(r.integers(*W.HELD_LAG)) if r.random() < 0.13 else int(r.integers(*W.MFG_LAG))
        relay_mfg.append(inst[i] - dt.timedelta(days=lag))
        made.append(relay_mfg[i] - dt.timedelta(days=int(r.integers(7, 45))))
    fitted = list(inst)
    live_from = [first_month(d) for d in inst]
    serial = [0] * n
    repaired = [False] * n
    origin = [None] * n
    spells, fails = [], []
    ret = Returns()
    for i in range(n):
        ret.made[(keys[i], 0)] = made[i]

    def store(i, d):
        return W.store_for(cur[sub_of[i]], leg[sub_of[i]], d)

    def close_spell(i, removed, reason):
        spells.append(dict(relay_key=keys[i], module=serial[i], fitted=fitted[i], removed=removed, reason=reason,
                           made=made[i], repaired=repaired[i], origin=origin[i]))

    # Veldtek service bulletin SB-15-02 (2015): modules with date codes 97 and earlier replaced, station by station; the
    # station's month in the bulletin campaign is the drawn one, and the swap is dated on a working day counted from
    # the same first day of a month
    when = {}
    for s_ in sorted(set(sub_of)):
        when[s_] = weekday(rng, dt.date(2015, int(rng.integers(4, 12)), int(rng.integers(1, 29))), 0)
    adj = np.random.default_rng([W.SEED, 8])
    camp = {s_: bday_like(adj, when[s_]) for s_ in sorted(when)}
    sb_ship = {}
    for m in months_between(dt.date(1992, 1, 1), dt.date(2026, 10, 1)):
        if m.year == 2015:
            out = {}
            for i in range(n):
                c0, c = when[sub_of[i]], camp[sub_of[i]]
                if ((c0.year, c0.month) == (m.year, m.month) and live_from[i] <= m and made[i].year <= W.SB_LAST_CODE
                        and (stop[i] is None or m < first_month(stop[i]))):
                    close_spell(i, c, "CAMPAIGN")
                    rs = np.random.default_rng([W.SEED, 21, keys[i], serial[i]])
                    if rs.random() < 0.86:
                        out.setdefault(sub_of[i], []).append(dict(kind="SB", relay_key=keys[i], module=serial[i],
                                                                  removed=c, reported=c, store=store(i, c)))
                    serial[i] += 1
                    fitted[i] = c
                    live_from[i] = first_month(c)
                    made[i] = c - dt.timedelta(days=int(rs.integers(30, 160)))     # built for the bulletin
                    repaired[i], origin[i] = False, None
                    ret.made[(keys[i], serial[i])] = made[i]
            for s_ in sorted(out):
                k = sorted(when).index(s_)
                sb_ship[s_] = add_bdays(camp[s_], int(np.random.default_rng([W.SEED, 21, 9, k]).integers(12, 40)))
                ret.bulletin(out[s_], sb_ship[s_])
        idx = [i for i in range(n) if live_from[i] <= m and (stop[i] is None or m < first_month(stop[i]))]
        if not idx:
            continue
        ages = [age_on(fitted[i], m) for i in idx]
        p = np.array([W.p_month(a, mindex(m) - mindex(live_from[i]), repaired[i]) for a, i in zip(ages, idx)])
        hit = rng.random(len(idx)) < p
        month = []
        for j in np.where(hit)[0]:
            i = idx[j]
            rep = dt.date(m.year, m.month, int(rng.integers(2, 29)))
            em = rng.random() < 0.3
            eom = month_add(m, 1) - dt.timedelta(days=1)
            done = min(rep + dt.timedelta(days=0 if em else int(rng.integers(1, 7))), eom, W.ASOF)
            if stop[i] is not None and done >= stop[i]:
                continue                                   # station rebuilt before the repair: no record
            month.append((done, keys[i], i, rep, em, int(ages[j])))
        for done, _, i, rep, em, age in sorted(month):
            ret.ship_before(done)
            fails.append(dict(relay_key=keys[i], reported=rep, month=m, age=age, em=em, done=done, module=serial[i],
                              repaired=repaired[i]))
            close_spell(i, done, "FAILED")
            if done >= W.RMA_START:
                ret.failed(dict(kind="EAM" if m >= W.MIGRATION else "LEGACY", relay_key=keys[i], module=serial[i],
                                removed=done, reported=rep, store=store(i, done)),
                           np.random.default_rng([W.SEED, 21, keys[i], serial[i]]))
            rr = np.random.default_rng([W.SEED, 24, keys[i], serial[i] + 1])
            src = ret.issue(done, rr)
            serial[i] += 1
            fitted[i] = done
            live_from[i] = first_month(done)
            if src is None:
                made[i] = done - dt.timedelta(days=int(rr.integers(45, 900)))      # from new stock
                repaired[i], origin[i] = False, None
            else:
                made[i] = ret.made[src]
                repaired[i], origin[i] = True, src
            ret.made[(keys[i], serial[i])] = made[i]
    ret.ship_before(dt.date(2100, 1, 1))
    for i in range(n):
        close_spell(i, stop[i], "RETIRED" if stop[i] else None)
    f = pd.DataFrame(fails)
    sp = pd.DataFrame(spells).sort_values(["relay_key", "module"], kind="mergesort").reset_index(drop=True)
    return sp, f, ret, relay_mfg

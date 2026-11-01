"""The world: six en-route sectors' traffic for the 2026 trial, the overnight combinations, the planners' use of
PROBE-M and the short-term conflict alert's activations. Everything is drawn here, once, from params.SEED; the pack
writes it out and the figures read only the pack."""
import datetime as dt

import numpy as np

import params as P

S = P.SECTORS
IDX = {s: i for i, s in enumerate(S)}


def rng(tag):
    return np.random.default_rng([P.SEED, sum(ord(c) * (i + 1) for i, c in enumerate(tag))])


# ------------------------------------------------------------------------------------------------- calendar

def frame():
    """Local-time facts for every UTC minute of the trial (minute 0 = 2026-04-01 00:00 New Zealand time). The local
    clock steps back an hour when daylight time ends (5 April, 03:00 NZDT) and forward when it starts (27 September,
    02:00 NZST)."""
    m = np.arange(P.MINUTES)
    t1 = int((dt.datetime(2026, 4, 4, 14, 0, tzinfo=P.UTC) - P.T0).total_seconds() // 60)
    t2 = int((dt.datetime(2026, 9, 26, 14, 0, tzinfo=P.UTC) - P.T0).total_seconds() // 60)
    L = m - 60 * ((m >= t1) & (m < t2))
    day = L // 1440
    hour = (L % 1440) / 60.0
    d0 = dt.date(2026, 4, 1)
    dates = [d0 + dt.timedelta(days=int(k)) for k in range(int(day.max()) + 1)]
    wd = np.array([d.weekday() for d in dates])
    mo = np.array([d.month - 4 for d in dates])
    edges = []
    for k in range(len(dates)):
        first = int(np.argmax(day == k))
        edges.append((first, dates[k]))
    edges.append((P.MINUTES, dt.date(2026, 10, 1)))
    return {"hour": hour, "day": day, "wday": wd[day], "month": mo[day], "edges": edges, "L": L, "t1": t1, "t2": t2}


# ------------------------------------------------------------------------------------------------- traffic

# Flight chains: sectors in order with the phase in each (C climbing, D descending, L level), the mean minutes in
# each, the daily count on a weekday, and the clock the chain keeps (a hub's departure or arrival bank, or none).
CHAINS = [
    ("AKL-WLG", [("WKO", "C", 14), ("TPO", "L", 13), ("KPT", "D", 15)], 22, "AKL_DEP", ("NZAA", "NZWN")),
    ("WLG-AKL", [("KPT", "C", 14), ("TPO", "L", 13), ("WKO", "D", 15)], 22, "AKL_ARR", ("NZWN", "NZAA")),
    ("AKL-STH", [("WKO", "C", 14), ("TPO", "C", 11), ("KPT", "L", 12)], 26, "AKL_DEP", ("NZAA", "SOUTH")),
    ("STH-AKL", [("KPT", "L", 12), ("TPO", "D", 12), ("WKO", "D", 15)], 26, "AKL_ARR", ("SOUTH", "NZAA")),
    ("AKL-AUS", [("KPA", "C", 14), ("TKI", "L", 13)], 18, "AKL_DEP", ("NZAA", "AUS")),
    ("AUS-AKL", [("TKI", "L", 13), ("KPA", "D", 15)], 18, "AKL_ARR", ("AUS", "NZAA")),
    ("AKL-PAC", [("HKI", "C", 14)], 10, "AKL_DEP", ("NZAA", "PAC")),
    ("PAC-AKL", [("HKI", "D", 15)], 10, "AKL_ARR", ("PAC", "NZAA")),
    ("AKL-EST", [("HKI", "C", 12)], 14, "AKL_DEP", ("NZAA", "EAST")),
    ("EST-AKL", [("HKI", "D", 13)], 14, "AKL_ARR", ("EAST", "NZAA")),
    ("AKL-WST", [("WKO", "C", 13), ("TKI", "D", 14)], 10, "AKL_DEP", ("NZAA", "WEST")),
    ("WST-AKL", [("TKI", "C", 13), ("WKO", "D", 14)], 10, "AKL_ARR", ("WEST", "NZAA")),
    ("AKL-NTH", [("KPA", "C", 11)], 6, "AKL_DEP", ("NZAA", "NORTH")),
    ("NTH-AKL", [("KPA", "D", 11)], 6, "AKL_ARR", ("NORTH", "NZAA")),
    ("WLG-NE", [("KPT", "C", 13), ("TPO", "L", 16), ("HKI", "D", 14)], 12, "WLG_DEP", ("NZWN", "EAST")),
    ("NE-WLG", [("HKI", "C", 14), ("TPO", "L", 16), ("KPT", "D", 13)], 12, "WLG_ARR", ("EAST", "NZWN")),
    ("AUS-WLG", [("TKI", "L", 15), ("KPT", "D", 12)], 7, "WLG_ARR", ("AUS", "NZWN")),
    ("WLG-AUS", [("KPT", "C", 12), ("TKI", "L", 14)], 7, "WLG_DEP", ("NZWN", "AUS")),
    ("OVF-N", [("KPA", "L", 15), ("HKI", "L", 14)], 44, "OVF", ("AUS", "AMER")),
    ("OVF-S", [("TPO", "L", 14), ("HKI", "L", 14)], 20, "OVF", ("SOUTH", "PAC")),
    ("OVF-W", [("TKI", "L", 15), ("WKO", "L", 12), ("HKI", "L", 13)], 40, "OVF", ("AUS", "PAC")),
    ("STH-NTH", [("KPT", "L", 12), ("TPO", "L", 12), ("WKO", "L", 12)], 40, "OVF", ("SOUTH", "NORTH")),
    ("NTH-STH", [("WKO", "L", 12), ("TPO", "L", 12), ("KPT", "L", 12)], 40, "OVF", ("NORTH", "SOUTH")),
    ("OVF-E", [("HKI", "L", 14), ("KPA", "L", 14)], 22, "OVF", ("PAC", "AUS")),
    ("DOM-L", [("KPT", "L", 13), ("TPO", "L", 13)], 26, "OVF", ("SOUTH", "EAST")),
    ("TAS-X", [("KPA", "L", 14), ("TKI", "L", 14)], 30, "OVF", ("PAC", "AUS")),
]
REROUTE = {"KPA": "HKI", "HKI": "KPA", "WKO": "TKI", "TKI": "WKO", "TPO": "KPT", "KPT": "TPO"}

AERO = {
    "SOUTH": ["NZCH", "NZCH", "NZCH", "NZQN", "NZDN", "NZNS", "NZIV"],
    "AUS": ["YSSY", "YSSY", "YMML", "YBBN", "YBBN", "YBCG", "YPPH"],
    "PAC": ["NFFN", "NCRG", "NTAA", "NSFA", "NVVV", "NWWW"],
    "AMER": ["KLAX", "KSFO", "KIAH", "CYVR", "SCEL"],
    "EAST": ["NZTG", "NZGS", "NZNR", "NZRO"],
    "WEST": ["NZNP", "NZPM", "NZWU"],
    "NORTH": ["NZKK", "NZWR", "NZKT"],
}
OPERATORS = {"dom_jet": ["KRX", "SWY", "AOE"], "turbo": ["KRX", "MRV"], "intl": ["PFA", "TZA", "ZRA", "AOE", "QXW"]}
TYPES = {"dom_jet": ["A320", "A21N", "A320", "B738"], "turbo": ["AT76", "AT76", "DH8C"],
         "intl": ["B789", "A359", "B77W", "A21N", "B38M", "A333"]}


def bank_rate(clock, hour, shifts=None, day=None):
    """Relative departure or arrival intensity by local clock hour for a hub, or a flat profile for overflights.
    Each bank's centre moves from day to day with the schedule and the morning's delays (shifts, hours, per day)."""
    h = hour
    if clock == "OVF":
        return 0.25 + 0.75 * np.exp(-((h - 13.0) / 6.0) ** 2) * (h > 2) + 0.15 * ((h > 22) | (h < 4))
    centres = {"AKL_DEP": [6.8, 10.9, 13.4, 16.9, 19.8], "AKL_ARR": [8.6, 12.3, 15.2, 18.6, 21.4],
               "WLG_DEP": [7.1, 11.6, 16.3, 18.9], "WLG_ARR": [8.9, 13.1, 17.6, 20.6]}[clock]
    r = np.zeros_like(h, dtype=float)
    for j, c in enumerate(centres):
        cc = c + (shifts[day, j] if shifts is not None else 0.0)
        r += np.exp(-((h - cc) / 0.36) ** 2)
    return 0.03 + r


def flights(fr):
    """Every flight of the trial with its flown crossings and its earlier plan revisions."""
    r = rng("flights")
    hour = fr["hour"]
    nday = int(fr["day"].max()) + 1
    day_f = np.exp(r.normal(0, 0.07, nday))
    month_f = np.array([1.00, 0.97, 0.95, 1.04, 0.99, 1.02])
    wk_f = np.array([1.04, 0.98, 0.98, 1.02, 1.08, 0.86, 0.94])
    out = []
    serial = 0
    bank_shift = {c: r.normal(0, 0.55, (nday, 6)) for c in ("AKL_DEP", "AKL_ARR", "WLG_DEP", "WLG_ARR")}
    for name, legs, per_day, clock, (src, dst) in CHAINS:
        prof = bank_rate(clock, hour, bank_shift.get(clock), fr["day"])
        prof = prof / prof.reshape(-1)[:].mean()
        lam = per_day / 1440.0 * prof * day_f[fr["day"]] * month_f[fr["month"]] * wk_f[fr["wday"]]
        k = r.poisson(lam)
        mins = np.repeat(np.nonzero(k)[0], k[np.nonzero(k)[0]])
        cls = "intl" if ("AUS" in name or "PAC" in name or "OVF-N" in name or "TAS" in name or "OVF-W" in name
                         or "OVF-S" in name) else ("turbo" if name in ("AKL-EST", "EST-AKL", "AKL-WST", "WST-AKL",
                                                                           "AKL-NTH", "NTH-AKL", "WLG-NE", "NE-WLG")
                                                   else "dom_jet")
        for m0 in mins:
            serial += 1
            t = int(m0) * 60
            cross = []
            cruise = int(r.choice([300, 320, 340, 360, 380, 400])) if cls != "turbo" else int(r.choice([170, 190, 210, 230, 250]))
            for (sec, ph, mean) in legs:
                dur = max(6, int(round(r.normal(mean, 2.2)))) * 60
                if ph == "C":
                    fin = int(r.choice([150, 170, 190, 210, 230])) if cls != "turbo" else int(r.choice([110, 130, 150]))
                    fout = cruise if cruise > fin + 30 else fin + 60
                elif ph == "D":
                    fin = cruise
                    fout = int(r.choice([150, 170, 190, 210, 230])) if cls != "turbo" else int(r.choice([110, 130, 150]))
                    if fout >= fin - 30:
                        fout = fin - 80
                else:
                    fin = fout = cruise
                cross.append([sec, t, t + dur, fin, fout, ph])
                t = t + dur
            out.append({"serial": serial, "chain": name, "cls": cls, "src": src, "dst": dst, "cross": cross})
    # flow management: a flight whose crossings would take a sector past its declared capacity waits on the ground
    # a few minutes at a time until they fit
    occ = np.zeros((len(S), P.MINUTES + 600), np.int16)
    out.sort(key=lambda f: (f["cross"][0][1], f["serial"]))
    for f in out:
        for attempt in range(25):
            spans = [(IDX[c[0]], max(0, int(np.ceil((c[1] - 30) / 60.0))), int(np.ceil((c[2] - 30) / 60.0)))
                     for c in f["cross"]]
            if all(hi <= lo or occ[i, lo:hi].max() < P.CAPACITY for i, lo, hi in spans) or attempt == 24:
                break
            d = int(r.integers(2, 5)) * 60
            for c in f["cross"]:
                c[1] += d
                c[2] += d
        for i, lo, hi in spans:
            occ[i, lo:max(lo, hi)] += 1
    # re-entries: a route that leaves a sector for a neighbour and comes back into it
    for f in out:
        if r.random() < P.P_REENTRY:
            i = int(r.integers(0, len(f["cross"])))
            sec, a, b, fin, fout, ph = f["cross"][i]
            nb = P.NEXT[sec]
            if b - a < 9 * 60 or any(c[0] == nb for c in f["cross"]):
                continue
            c1 = a + int(round((b - a) / 60.0 * r.uniform(0.35, 0.55))) * 60
            c2 = c1 + int(r.integers(3, 6)) * 60
            if b - c2 < 3 * 60 or c1 - a < 3 * 60:
                continue
            mid = fin + (fout - fin) * (c1 - a) / (b - a)
            mid2 = fin + (fout - fin) * (c2 - a) / (b - a)
            m1 = int(round(mid / 10.0) * 10)
            m2 = int(round(mid2 / 10.0) * 10)
            ph1 = ph if m1 != fin else "L"
            f["cross"][i:i + 1] = [[sec, a, c1, fin, m1, ph if m1 != fin else "L"],
                                   [nb, c1, c2, m1, m2, ph if m2 != m1 else "L"],
                                   [sec, c2, b, m2, fout, ph if fout != m2 else "L"]]
            f["reentry"] = True
    # names, aerodromes, types, plan revisions
    used = set()
    for f in out:
        cls = f["cls"]
        op = str(r.choice(OPERATORS[cls]))
        while True:
            cs = "%s%d" % (op, int(r.integers(100, 1000)) if cls != "turbo" else int(r.integers(5000, 6000)))
            key = (cs, f["cross"][0][1] // 86400)
            if key not in used:
                used.add(key)
                break
        f["callsign"] = cs
        f["adep"] = str(r.choice(AERO[f["src"]])) if f["src"] in AERO else f["src"]
        f["ades"] = str(r.choice(AERO[f["dst"]])) if f["dst"] in AERO else f["dst"]
        f["type"] = str(r.choice(TYPES[cls]))
        f["ifps"] = "AA%08d" % (10000000 + f["serial"] * 37 % 89999989)
        f["revisions"] = []
        u = r.random()
        if u < P.P_REROUTE and len(f["cross"]) >= 2:
            # the first plan routed through another sector for one leg; the flight was re-planned before entering it
            i = int(r.integers(0, len(f["cross"])))
            old = [list(c) for c in f["cross"]]
            alt = REROUTE.get(old[i][0])
            if alt and all(c[0] != alt for c in old):
                old[i][0] = alt
                shift = int(r.integers(-2, 3)) * 60
                old[i][1] += shift
                old[i][2] += shift + int(r.integers(-1, 3)) * 60
                f["revisions"].append(("route", old))
        elif u < P.P_REROUTE + P.P_TIME_REVISION:
            d = int(r.integers(6, 46)) * 60
            old = [[c[0], c[1] - d, c[2] - d, c[3], c[4], c[5]] for c in f["cross"]]
            f["revisions"].append(("time", old))
            if r.random() < 0.15:
                d2 = int(r.integers(5, 25)) * 60
                older = [[c[0], c[1] - d2, c[2] - d2, c[3], c[4], c[5]] for c in old]
                f["revisions"].insert(0, ("time", older))
    return out


def occupancy(fl):
    """Aircraft in each sector at each minute's midpoint, and how many of them climb or descend through it."""
    n = np.zeros((len(S), P.MINUTES + 400), np.int32)
    T = np.zeros((len(S), P.MINUTES + 400), np.int32)
    for f in fl:
        for sec, a, b, fin, fout, ph in f["cross"]:
            i = IDX[sec]
            lo = max(0, int(np.ceil((a - 30) / 60.0)))
            hi = int(np.ceil((b - 30) / 60.0))
            if hi <= lo:
                continue
            n[i, lo:hi] += 1
            if fin != fout:
                T[i, lo:hi] += 1
    return n[:, :P.MINUTES], T[:, :P.MINUTES]


# ------------------------------------------------------------------------------------------------- configuration

def configuration(fr):
    """Each night the six sectors combine in pairs (about 23:00 to 05:30 New Zealand time)."""
    r = rng("config")
    comb = np.zeros(P.MINUTES, bool)
    changes = []
    edges = fr["edges"]
    for k, (a, dd) in enumerate(edges[:-1]):
        # local midnight minute index a; combine on the evening of dd, split on the next morning
        c_local = 23 * 60 + int(r.integers(-25, 26))
        s_local = 24 * 60 + 5 * 60 + 30 + int(r.integers(-25, 26))
        ca = a + c_local
        sb = a + s_local
        # the local clock may step at the DST changes; recompute from the next local midnight for the split
        if k + 1 < len(edges) - 1:
            nxt = edges[k + 1][0]
            sb = nxt + 5 * 60 + 30 + int(r.integers(-25, 26))
        if ca < P.MINUTES:
            comb[max(0, ca):min(P.MINUTES, sb)] = True
            changes.append((ca, "NIGHT"))
            if sb < P.MINUTES:
                changes.append((sb, "DAY"))
    # the trial opens at local midnight in the night configuration (combined since the evening of 31 March)
    first_split = edges[0][0] + 5 * 60 + 30 + int(r.integers(-25, 26))
    comb[0:first_split] = True
    changes = [(0, "NIGHT"), (first_split, "DAY")] + changes
    return comb, sorted(set(changes))


# ------------------------------------------------------------------------------------------------- the probe

def probe(fr, n, T, comb):
    """The planners' use of PROBE-M: a session runs from switch-on to switch-off at one position. Each watch has its
    own habit with the probe (unrecorded); switching on grows with the climbing and descending traffic present."""
    r = rng("probe")
    hour = fr["hour"]
    day = fr["day"]
    watch = np.where(hour < 6, 0, np.where(hour < 13.5, 1, np.where(hour < 21, 2, 3)))
    wkey = day * 4 + watch
    wkey = np.where(watch == 0, wkey - 1, wkey)   # the night watch runs across midnight
    on = np.zeros((len(S), P.MINUTES), bool)
    sessions = []
    keen = {}

    def k_of(pos, w):
        if (pos, w) not in keen:
            keen[(pos, w)] = float(np.exp(r.normal(0, P.KEEN_SD)))
        return keen[(pos, w)]

    positions = [(s,) for s in S] + list(P.PAIRS)
    # no probe use in the small hours either side of the end of daylight time (5 April), when the clock repeats
    quiet = np.zeros(P.MINUTES, bool)
    quiet[max(0, fr["t1"] - 90):fr["t1"] + 90] = True
    u = r.random((len(positions), P.MINUTES))
    for pi, pos in enumerate(positions):
        idx = [IDX[s] for s in pos]
        live = comb if len(pos) == 2 else ~comb
        nn = n[idx].sum(axis=0)
        tt = T[idx].sum(axis=0)
        state = False
        start = None
        for m in range(P.MINUTES):
            if not live[m]:
                if state:
                    sessions.append((pos, start, m))
                    state = False
                continue
            k = k_of(pos, int(wkey[m]))
            if quiet[m]:
                if state:
                    sessions.append((pos, start, m))
                    state = False
                continue
            if not state:
                hz = k * (P.PROBE_ON_BASE + P.PROBE_ON_T * max(tt[m] - 1, 0) + P.PROBE_ON_N * max(nn[m] - 4, 0))
                hz *= np.exp(-P.PROBE_BUSY * max(nn[m] - 5, 0))
                if u[pi, m] < min(hz, 0.9):
                    state = True
                    start = m
            else:
                hz = (P.PROBE_OFF_BASE + P.PROBE_OFF_T0 * (tt[m] == 0) + P.PROBE_OFF_T1 * (tt[m] == 1)) / k
                if u[pi, m] < min(hz, 0.9):
                    sessions.append((pos, start, m))
                    state = False
            if state:
                on[idx, m] = True
        if state:
            sessions.append((pos, start, P.MINUTES))
    return on, sessions


# ------------------------------------------------------------------------------------------------- activations

def intensity(n, T, on):
    """The activation intensity per minute before the sector's scale: every pair of aircraft present can raise an
    alert, and each aircraft climbing or descending through the sector multiplies the rate by exp(BETA); the probe
    multiplies it by R_TRUE at every traffic level."""
    return n * (n - 1) / 2.0 * np.exp(P.BETA * T) * np.where(on, P.R_TRUE, 1.0)   # zero below two aircraft


def activations(fl, n, T, on, comb):
    """STCA activations: each sector-minute's intensity rises with the aircraft present and, more steeply, with those
    climbing or descending; the probe's use multiplies it by R_TRUE at every traffic level."""
    r = rng("stca")
    thin = rng("stca-thin")
    present = [[] for _ in S]
    # crossing index by sector for drawing the pair
    for fi, f in enumerate(fl):
        for ci, (sec, a, b, fin, fout, ph) in enumerate(f["cross"]):
            present[IDX[sec]].append((a, b, fi, ci, fin != fout))
    for i in range(len(S)):
        present[i].sort()
    starts = [np.array([p[0] for p in present[i]]) for i in range(len(S))]
    out = []
    for i, s in enumerate(S):
        # candidates at the probe-free intensity, then the probe's minutes thinned to R_TRUE with their own draws,
        # so the probe's effect and the rest of the record are drawn apart
        base = intensity(n[i], T[i], np.zeros_like(on[i]))
        lam = P.TARGET / base.sum() * base
        k = r.poisson(lam)
        for m in np.nonzero(k)[0]:
            for _ in range(int(k[m])):
                t = int(m) * 60 + int(r.integers(0, 60))
                hi = np.searchsorted(starts[i], t, side="right")
                cand = [p for p in present[i][max(0, hi - 400):hi] if p[0] <= t < p[1]]
                if len(cand) < 2:
                    continue
                w = np.array([3.0 if c[4] else 1.0 for c in cand])
                a_i = int(r.choice(len(cand), p=w / w.sum()))
                rest = [c for j, c in enumerate(cand) if j != a_i]
                w2 = np.array([2.0 if c[4] else 1.0 for c in rest])
                b_i = int(r.choice(len(rest), p=w2 / w2.sum()))
                a, b = cand[a_i], rest[b_i]
                dur = int(r.integers(8, 75))
                inh = s in ("WKO", "KPA") and r.random() < P.P_INHIBITED
                hsep = round(float(r.uniform(0.8, 4.6)), 1)
                vsep = int(r.choice([0, 100, 200, 300, 400, 500, 600, 700, 800]))
                if on[i, m] and thin.random() >= P.R_TRUE:
                    continue
                out.append({"sector": s, "t": t, "dur": dur, "a": (a[2], a[3]), "b": (b[2], b[3]), "inhibited": inh,
                            "m": int(m), "probe": bool(on[i, m]), "comb": bool(comb[m]),
                            "hsep": hsep, "vsep": vsep})
    out.sort(key=lambda x: (x["t"], x["sector"]))
    return out


def month_edges():
    out = []
    for mo in range(4, 11):
        u = dt.datetime(2026, mo, 1, tzinfo=P.NZ).astimezone(P.UTC)
        out.append(int((u - P.T0).total_seconds()))
    return out


def cells(fl, acts):
    """The asks' exact flight hours and counted activations by sector and New Zealand month."""
    e = month_edges()
    hrs = np.zeros((len(S), 6))
    cnt = np.zeros((len(S), 6), int)
    for f in fl:
        for sec, a, b, fin, fout, ph in f["cross"]:
            for k in range(6):
                lo, hi = e[k], e[k + 1]
                ov = min(b, hi) - max(a, lo)
                if ov > 0:
                    hrs[IDX[sec], k] += ov / 3600.0
    for x in acts:
        if not x["inhibited"]:
            k = max(j for j in range(6) if x["t"] >= e[j])
            cnt[IDX[x["sector"]], k] += 1
    return hrs, cnt


def nudge(fl, acts):
    """Keep every graded ask figure clear of its rounding edge: where a sector-month's flight hours sit within two
    minutes of a half hour, or its rate within 0.004 of a half-decimal, a level overflight that opens its route in that
    sector in the small hours is entered a few minutes earlier (no alert is possible with under two aircraft present)."""
    r = rng("nudge")
    e = month_edges()
    for it in range(40):
        hrs, cnt = cells(fl, acts)
        bad = []
        for i in range(len(S)):
            for k in range(6):
                h = hrs[i, k]
                rate = 1000.0 * cnt[i, k] / h
                if abs((h % 1.0) - 0.5) < 2.0 / 60 or abs(((rate * 10) % 1.0) - 0.5) < 0.04:
                    bad.append((i, k))
        if not bad:
            return it
        for i, k in bad:
            pool = [f for f in fl if f["cross"][0][0] == S[i] and f["cross"][0][5] == "L"
                    and e[k] + 86400 < f["cross"][0][1] < e[k + 1] - 86400
                    and 1 <= ((f["cross"][0][1] // 60 + 13 * 60) // 60) % 24 <= 4]
            f = pool[int(r.integers(0, len(pool)))]
            f["cross"][0][1] -= int(r.integers(3, 8)) * 60
    raise RuntimeError("nudge did not converge")


def build():
    fr = frame()
    fl = flights(fr)
    n, T = occupancy(fl)
    comb, changes = configuration(fr)
    on, sessions = probe(fr, n, T, comb)
    acts = activations(fl, n, T, on, comb)
    nudge(fl, acts)
    n, T = occupancy(fl)
    return {"frame": fr, "flights": fl, "n": n, "T": T, "comb": comb, "changes": changes, "on": on,
            "sessions": sessions, "acts": acts}


if __name__ == "__main__":
    import time
    t0 = time.time()
    W = build()
    print("flights", len(W["flights"]), "crossings", sum(len(f["cross"]) for f in W["flights"]),
          "activations", len(W["acts"]), "sessions", len(W["sessions"]), "%.0fs" % (time.time() - t0))
    for i, s in enumerate(S):
        print(s, "mean n %.2f" % W["n"][i].mean(), "mean T %.2f" % W["T"][i].mean(),
              "T share %.2f" % (W["T"][i].sum() / max(W["n"][i].sum(), 1)), "probe %.3f" % W["on"][i].mean(),
              "acts", sum(1 for a in W["acts"] if a["sector"] == s))

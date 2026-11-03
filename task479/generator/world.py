"""The world before any export is written: Pellston Fine Chemicals' 2026 on emission unit EU-P1.

Six reactors, two fluid-bed dryers and a solvent still vent through closed-vent system CVS-1 to RTO-1, a
regenerative thermal oxidizer whose induced-draft fan draws at most 3,800 scfm. Every batch step vents at the
rate the vent calculation basis gives for its product and step; the header carries the sum of the steps in
progress, the fan draws up to its maximum, and the gas above it lifts PSV-31 at the oxidizer inlet to atmosphere.

Time is kept as whole minutes of Eastern Standard Time from 2026-01-01 00:00 EST (t = 0); the plant's local clock
is prevailing Eastern time, the DAHS keeps standard time all year, the new MES keeps UTC.
"""
import datetime as dt
import numpy as np

SEED = 47922
YEAR = 365 * 1440                      # minutes in 2026
PAD = 6 * 1440                         # simulation runs from late December 2025 to early January 2027
T0_UTC = dt.datetime(2026, 1, 1, 5, 0, tzinfo=dt.timezone.utc)
DST_START = 66 * 1440 + 120            # 2026-03-08 02:00 EST
DST_END = 304 * 1440 + 60              # 2026-11-01 01:00 EST (02:00 EDT)
CUTOVER = 181 * 1440 - 60 + 360        # 2026-07-01 06:00 EDT, Batchwise 4 to Orbitas
DOY = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]

FAN_MAX = 3800.0                       # scfm, RTO-1 induced-draft fan at its design pressure drop
DRE = 0.994                            # RTO-1 destruction efficiency certified in the May 2025 test
LIMIT_TONS = 2.5                       # EU-P1 VOC per calendar year
SCF_PER_NM3 = 35.3146667 * 293.15 / 273.15   # 68 F standard against 0 C normal
LB_PER_KG = 2.20462262
TE_REMAP = 212 * 1440 + 10 * 1440 + 9 * 60 + 5   # 2026-08-11 09:05 EST, DAHS chamber input moved to TE-101B

SOURCES = ["R-101", "R-102", "R-103", "R-104", "R-105", "R-106", "D-201", "D-202", "SR-301"]

# The vent calculation basis: (step key, basis step name, mean minutes, flow, VOC rate). US-unit products in scfm
# and lb/hr; the licensed PX line in Nm3/h and kg/h as the licensor's sheet gives them.
REACTOR = {
    "PFC-2140": ("us", [("CHG_LIQ", "Charge solvent", 42, 70, 7.1), ("CHG_SOL", "Charge solids, manway exhaust", 27, 1250, 14.2),
                        ("HEAT", "Heat to reflux", 74, 150, 8.4), ("RXN", "Reaction hold", 410, 45, 1.6),
                        ("DIST", "Atmospheric distillation", 158, 95, 4.7), ("COOL", "Cool and crystallise", 96, 30, 0.5),
                        ("XFER", "Transfer slurry to dryer", 31, 60, 2.3)]),
    "PFC-4408": ("us", [("CHG_LIQ", "Charge solvent", 38, 80, 7.7), ("CHG_SOL", "Charge solids, manway exhaust", 33, 1200, 13.6),
                        ("HEAT", "Heat to reaction temperature", 61, 165, 10.8), ("RXN", "Reaction hold", 300, 40, 1.4),
                        ("STRIP", "Solvent strip under nitrogen", 148, 120, 6.2), ("COOL", "Cool and crystallise", 84, 30, 0.5),
                        ("XFER", "Transfer slurry to dryer", 27, 60, 2.3)]),
    "PFC-2315": ("us", [("CHG_LIQ", "Charge solvent", 46, 70, 8.7), ("CHG_SOL", "Charge solids, manway exhaust", 22, 1285, 16.7),
                        ("EXTR", "Extraction and phase split", 128, 90, 6.1), ("SETL", "Settle", 92, 25, 0.6),
                        ("XFER", "Transfer slurry to dryer", 36, 60, 2.9)]),
    "PFC-3021": ("us", [("CHG_LIQ", "Charge solvent", 33, 60, 5.5), ("HEAT", "Heat to reflux", 79, 130, 6.8),
                        ("RXN", "Reaction hold", 470, 35, 1.1), ("VDIST", "Vacuum distillation", 196, 110, 5.4),
                        ("COOL", "Cool", 78, 30, 0.5), ("DRUM", "Drum off product", 44, 45, 2.0)]),
    "PX-711": ("metric", [("CHG_LIQ", "Solvent charge", 40, 105, 3.1), ("CHG_SOL", "Solids charge, manway extraction", 29, 2010, 6.6),
                          ("HEAT", "Heating", 66, 230, 4.1), ("RXN", "Reaction", 380, 64, 0.7),
                          ("DIST", "Distillation", 141, 150, 2.3), ("COOL", "Crystallisation", 101, 48, 0.2),
                          ("XFER", "Slurry transfer", 34, 95, 1.1)]),
    "PX-714": ("metric", [("CHG_LIQ", "Solvent charge", 37, 115, 3.5), ("CHG_SOL", "Solids charge, manway extraction", 31, 1955, 6.9),
                          ("RXN", "Reaction", 340, 58, 0.8), ("STRIP", "Solvent stripping", 152, 185, 3.0),
                          ("COOL", "Crystallisation", 88, 48, 0.2), ("XFER", "Slurry transfer", 30, 95, 1.1)]),
}
CLEAN = ("CIP", "Solvent wash between campaigns", 96, 120, 6.3)
HOLD = ("HOLD", "Hold for dryer", None, 30, 0.3)
# Dryer cycles by the product dried: the drying step's VOC follows the wet cake's solvent.
DRYER = {
    "PFC-2140": [("LOAD", "Load wet cake", 34, 40, 0.8), ("PRE", "Pre-dry", 29, 600, 7.9), ("DRY", "Fluid-bed drying", 138, 1420, 47.0),
                 ("COOLD", "Cool", 39, 300, 2.3), ("UNLD", "Unload", 38, 30, 0.4)],
    "PFC-4408": [("LOAD", "Load wet cake", 32, 40, 0.8), ("PRE", "Pre-dry", 27, 600, 7.4), ("DRY", "Fluid-bed drying", 121, 1390, 43.5),
                 ("COOLD", "Cool", 41, 300, 2.2), ("UNLD", "Unload", 37, 30, 0.4)],
    "PFC-2315": [("LOAD", "Load wet cake", 36, 40, 0.8), ("PRE", "Pre-dry", 31, 620, 9.2), ("DRY", "Fluid-bed drying", 149, 1450, 52.0),
                 ("COOLD", "Cool", 38, 300, 2.5), ("UNLD", "Unload", 39, 30, 0.4)],
    "PX-711": [("LOAD", "Load wet cake", 33, 40, 0.8), ("PRE", "Pre-dry", 28, 610, 7.6), ("DRY", "Fluid-bed drying", 132, 1410, 46.0),
               ("COOLD", "Cool", 40, 300, 2.3), ("UNLD", "Unload", 36, 30, 0.4)],
    "PX-714": [("LOAD", "Load wet cake", 35, 40, 0.8), ("PRE", "Pre-dry", 30, 600, 7.4), ("DRY", "Fluid-bed drying", 127, 1400, 43.0),
               ("COOLD", "Cool", 37, 300, 2.1), ("UNLD", "Unload", 38, 30, 0.4)],
}
STILL = [("FEED", "Feed and total reflux", None, 70, 0.8), ("HEADS", "Heads cut", 41, 350, 4.6)]
REACTOR_PRODUCTS = {"R-101": ["PFC-2140", "PFC-4408"], "R-102": ["PFC-4408", "PFC-2140"], "R-103": ["PFC-2315", "PFC-3021"],
                    "R-104": ["PFC-3021", "PFC-2315"], "R-105": ["PX-711", "PX-714", "PFC-2140"], "R-106": ["PX-714", "PX-711"]}


def us_rate(prod, flow, voc):
    """A basis row in scfm and lb/hr."""
    if REACTOR.get(prod, ("us",))[0] == "metric":
        return flow * SCF_PER_NM3 / 60.0, voc * LB_PER_KG
    return float(flow), float(voc)


def local_offset_min(t):
    """Minutes to add to EST to get prevailing Eastern time at EST minute t (2025 to 2027)."""
    return 60 if DST_START <= t < DST_END else 0


def month_start(m):
    """EST minute at which local month m (1..13) starts; 13 is 2027-01-01."""
    d = DOY[m - 1] * 1440
    return d - local_offset_min(d - 60) if m != 13 else YEAR


QUARTERS = [(month_start(1), month_start(4)), (month_start(4), month_start(7)), (month_start(7), month_start(10)),
            (month_start(10), YEAR)]


class World:
    pass


def _steps_for(rng, steps, us_of):
    out = []
    for key, name, mean, flow, voc in steps:
        d = int(max(5, round(rng.normal(mean, 0.13 * mean))))
        f, v = us_of(flow, voc)
        out.append((key, name, d, f, v))
    return out


def simulate():
    rng = np.random.default_rng(SEED)
    w = World()
    w.steps = []          # (source, batch, product, seq, key, name, start, end, flow, voc, parent)
    lo, hi = -PAD, YEAR + PAD
    # plant shutdowns (no production): the summer turnaround and Christmas
    # plant shutdowns: the summer turnaround (27 July to 2 August) and Christmas to the New Year, both years; and no
    # reactor batch starts in the twelve hours before the 1 July batch-system cutover
    down = [(DOY[6] * 1440 + 26 * 1440, DOY[6] * 1440 + 33 * 1440), (-9 * 1440, 1440 + 360),
            (DOY[11] * 1440 + 22 * 1440, 366 * 1440 + 360), (CUTOVER - 720, CUTOVER)]
    dryer_free = {"D-201": lo, "D-202": lo}
    dryer_jobs = []
    seq_no = {s: int(rng.integers(30, 80)) for s in SOURCES}

    def in_down(t):
        return any(a <= t < b for a, b in down)

    def skip_down(t, reactors=True):
        for a, b in (down if reactors else down[:3]):
            if a <= t < b:
                return b + int(rng.integers(120, 600))
        return t

    reactor_events = []
    for s in SOURCES[:6]:
        srng = np.random.default_rng([SEED, SOURCES.index(s)])
        t = lo + int(srng.integers(0, 2400))
        prods = REACTOR_PRODUCTS[s]
        own_down = []
        for _ in range(int(srng.integers(1, 3))):
            a = int(srng.integers(20 * 1440, YEAR - 30 * 1440))
            own_down.append((a, a + int(srng.integers(4, 11)) * 1440))
        pi = int(srng.integers(0, len(prods)))
        while t < hi:
            prod = prods[pi % len(prods)]
            pi += int(srng.integers(1, 3))
            unit, recipe = REACTOR[prod]
            ncamp = int(srng.integers(9, 26))
            for _ in range(ncamp):
                t = skip_down(t)
                for a, b in own_down:
                    if a <= t < b:
                        t = b + int(srng.integers(60, 400))
                if t >= hi:
                    break
                seq_no[s] += 1
                batch = (s, seq_no[s])
                k = 0
                for key, name, d, f, v in _steps_for(srng, recipe, lambda fl, vo: us_rate(prod, fl, vo)):
                    if key == "XFER" and prod in DRYER:
                        reactor_events.append((t, s, batch, prod, k, key, name, d, f, v))
                    w.steps.append([s, batch, prod, k, key, name, t, t + d, f, v, None])
                    t += d
                    k += 1
                t += int(srng.integers(50, 330))
            # campaign change: a solvent wash
            key, name, mean, f, v = CLEAN
            d = int(max(30, round(srng.normal(mean, 0.15 * mean))))
            seq_no[s] += 1
            w.steps.append([s, (s, seq_no[s]), "CLEAN", 0, key, name, t, t + d, float(f), float(v), None])
            t += d + int(srng.integers(600, 3600))
    # dryers: each slurry transfer starts a drying cycle on the first free dryer once the transfer ends; while both
    # dryers are busy the reactor holds its slurry (a low-flow hold step before the transfer)
    reactor_events.sort(key=lambda e: e[0])
    drng = np.random.default_rng([SEED, 99])
    holds = []
    for (t, s, batch, prod, k, key, name, d, f, v) in reactor_events:
        ready = t
        dname = min(dryer_free, key=lambda x: (max(dryer_free[x], ready), x))
        start = max(dryer_free[dname], ready + d)
        if start > ready + d:
            holds.append((s, batch, ready, start - d))
        cyc = _steps_for(drng, DRYER[prod], lambda fl, vo: (float(fl), float(vo)))
        seq_no[dname] += 1
        dbatch = (dname, seq_no[dname])
        tt = start
        for kk, (key2, name2, d2, f2, v2) in enumerate(cyc):
            w.steps.append([dname, dbatch, prod, kk, key2, name2, tt, tt + d2, f2, v2, batch])
            tt += d2
        dryer_free[dname] = tt + int(drng.integers(15, 75))
    # a hold delays the reactor's transfer and everything after it in that batch
    for s, batch, a, b in holds:
        shift = b - a
        if shift <= 0:
            continue
        for st in w.steps:
            if st[0] == s and st[1] == batch and st[4] == "XFER":
                st[6] += shift
                st[7] += shift
        w.steps.append([s, batch, None, -1, "HOLD", HOLD[1], a, b, float(HOLD[3]), float(HOLD[4]), None])
    # the still runs whenever the plant does
    srng = np.random.default_rng([SEED, 77])
    t = lo
    while t < hi:
        t = skip_down(t, reactors=False)
        seq_no["SR-301"] += 1
        b = ("SR-301", seq_no["SR-301"])
        d1 = int(srng.integers(540, 1260))
        w.steps.append(["SR-301", b, "RECOVERY", 0, "FEED", STILL[0][1], t, t + d1, 70.0, 0.8, None])
        t += d1
        d2 = int(max(15, round(srng.normal(41, 6))))
        w.steps.append(["SR-301", b, "RECOVERY", 1, "HEADS", STILL[1][1], t, t + d2, 350.0, 4.6, None])
        t += d2 + int(srng.integers(30, 240))
    # products: fill the missing product on hold steps
    byb = {}
    for st in w.steps:
        if st[2] is not None:
            byb[(st[0], st[1])] = st[2]
    for st in w.steps:
        if st[2] is None:
            st[2] = byb.get((st[0], st[1]), "PFC-2140")
    w.steps.sort(key=lambda st: (st[6], st[0], st[3]))
    w.down = down
    _rto(w)
    _purchasing(w)
    _minute_arrays(w)
    return w


def _rto(w):
    """RTO-1's status and combustion chamber temperature by EST minute over 2026."""
    rng = np.random.default_rng([SEED, 5])
    n = YEAR
    status = np.array(["RUN"] * n, dtype=object)
    trips = []
    # flame-failure trips through the winter, until the burner management system was replaced in the summer
    # turnaround
    for _ in range(7):
        a = int(rng.integers(2 * 1440, DST_START - 2 * 1440))
        off = int(rng.integers(35, 210))
        warm = int(rng.integers(55, 115))
        trips.append((a, off, warm))
    # a planned outage inside the summer turnaround
    a0 = w.down[0][0] + 2 * 1440
    trips.append((a0, 2 * 1440 + 300, 140))
    trips.sort()
    true = np.empty(n)
    base = 1561.0
    eps = rng.normal(0, 3.2, n)
    ar = np.empty(n)
    ar[0] = 0
    for i in range(1, n):
        ar[i] = 0.985 * ar[i - 1] + eps[i]
    true[:] = base + ar * 0.55
    # low excursions while running (a sticking poppet valve, a burner turndown fault)
    for _ in range(16):
        a = int(rng.integers(0, n - 400))
        d = int(rng.integers(55, 260))
        depth = float(rng.uniform(55, 115))
        shape = np.sin(np.linspace(0, np.pi, d)) ** 0.6
        true[a:a + d] -= depth * shape
    for a, off, warm in trips:
        status[a:a + off] = "OFF"
        status[a + off:a + off + warm] = "WARMUP"
        k = np.arange(off)
        true[a:a + off] = 1561 - (1561 - 900) * (1 - np.exp(-k / 140.0))
        start = true[a + off - 1]
        kw = np.arange(warm)
        true[a + off:a + off + warm] = start + (1555 - start) * (kw / max(1, warm - 1)) ** 0.8
    w.trips = trips
    w.status = status
    w.true_temp = true
    # TE-101A, the DAHS's chamber channel; TE-101B, the redundant thermocouple the controller high-selects
    a_noise = rng.normal(0, 1.6, n)
    b_noise = rng.normal(0, 1.6, n)
    te_a = true + a_noise
    te_b = true + 2.4 + b_noise
    f0 = DOY[7] * 1440 + 8 * 1440 + 14 * 60 + 20      # 2026-08-09 14:20 EST, TE-101A begins to read low
    f1 = DOY[7] * 1440 + 25 * 1440 + 10 * 60 + 40     # 2026-08-26 10:40 EST, TE-101A replaced
    k = np.arange(f1 - f0)
    te_a[f0:f1] = true[f0:f1] - (88 + 52 * (k / len(k)) ** 0.7) + rng.normal(0, 3.0, len(k))
    w.te_fail = (f0, f1)
    w.te_remap = TE_REMAP
    w.te_a = np.round(te_a, 1)
    w.te_b = np.round(te_b, 1)
    # the DAHS chamber channel: TE-101A, except while its input was moved to TE-101B pending the replacement
    w.chamber = w.te_a.copy()
    w.chamber[TE_REMAP:f1] = w.te_b[TE_REMAP:f1]


def _minute_arrays(w):
    """Header flow and VOC rate by EST minute over 2026, and the same per source."""
    n = YEAR
    flow = np.zeros(n)
    voc = np.zeros(n)
    for st in w.steps:
        a, b = max(0, st[6]), min(n, st[7])
        if a >= b:
            continue
        flow[a:b] += st[8]
        voc[a:b] += st[9] / 60.0
    w.flow = flow
    w.voc_min = voc


def emitted(w, mode="golden", bin_min=1, fan=FAN_MAX, dre=DRE, offline_counts=True):
    """EU-P1 VOC emitted in pounds by quarter and year under a route.

    golden: capture = min(1, fan / header flow) minute by minute while RTO-1 runs; the gas above the fan's draw leaves
    through PSV-31 as mixed header gas. default: every pound vented while RTO-1 runs is destroyed at the tested
    efficiency. Minutes RTO-1 is not running are uncontrolled under both (offline_counts)."""
    run = w.status == "RUN"
    flow, voc = w.flow, w.voc_min
    if mode == "golden":
        if bin_min == 1:
            f = flow
        else:
            m = len(flow) // bin_min
            f = np.repeat(flow[:m * bin_min].reshape(m, bin_min).mean(1), bin_min)
            f = np.concatenate([f, flow[m * bin_min:]])
        cap = np.where(f > fan, fan / np.maximum(f, 1e-9), 1.0)
    else:
        cap = np.ones(len(flow))
    if not offline_counts:
        run = np.ones(len(flow), bool)
    e = np.where(run, voc * ((1 - cap) + cap * (1 - dre)), voc)
    q = [float(e[a:b].sum()) for a, b in QUARTERS]
    return q, float(e.sum())


# Solvents as the plant buys them: (solvent, code, pack, lb per US gallon at 60 F for bulk)
SOLVENTS = ["methanol", "toluene", "isopropanol", "ethyl acetate", "n-heptane", "isohexane", "tetrahydrofuran"]
DENSITY_LB_GAL = {"methanol": 6.63, "toluene": 7.26, "n-heptane": 5.71}
CODE_SWITCH = DOY[5] * 1440 - 60          # 2026-06-01 00:00 EDT: SOL-07 re-pointed from n-heptane drums to isohexane


def solvent_code(solvent, t):
    if solvent == "n-heptane":
        return "SOL-07" if t < CODE_SWITCH else "SOL-12"
    return {"methanol": "SOL-01", "toluene": "SOL-03", "isopropanol": "SOL-04", "ethyl acetate": "SOL-05",
            "isohexane": "SOL-07", "tetrahydrofuran": "SOL-09"}[solvent]


def _purchasing(w):
    """Deliveries from 1 December 2025 to 10 January 2027: bulk tankers (net US gallons at 60 F) and drums or totes
    (net kilograms), with the receiving clerk's posting date and the supplier's invoice."""
    rng = np.random.default_rng([SEED, 31])
    plan = [
        ("methanol", "bulk", (8, 14), (5800, 7400), None),
        ("toluene", "bulk", (13, 23), (5200, 6900), None),
        ("isopropanol", "drum", (14, 26), (4, 12), (152.0, 158.5)),
        ("ethyl acetate", "tote", (15, 31), (2, 6), (888.0, 905.0)),
        ("n-heptane", "drum", (9, 15), (8, 16), (136.0, 141.5)),
        ("isohexane", "drum", (12, 20), (8, 16), (128.0, 133.5)),
        ("tetrahydrofuran", "drum", (10, 18), (6, 14), (170.0, 175.5)),
    ]
    start, end = -31 * 1440, YEAR + 10 * 1440
    deliveries = []
    for solvent, pack, gap, size, unit_kg in plan:
        t = start + int(rng.integers(0, 6 * 1440))
        while t < end:
            if solvent == "isohexane" and t < CODE_SWITCH:
                t = CODE_SWITCH + int(rng.integers(2, 9)) * 1440
                continue
            mode = pack
            if solvent == "n-heptane" and t >= CODE_SWITCH:
                mode = "bulk"
            day = t // 1440
            dow = (day + 3) % 7                      # 2026-01-01 is a Thursday: 0 Monday ... 6 Sunday
            if dow >= 5:
                t += (7 - dow) * 1440
                continue
            arrive = day * 1440 + int(rng.integers(6 * 60 + 30, 15 * 60))
            if mode == "bulk":
                lo, hi = (4800, 6200) if solvent == "n-heptane" else size
                gal = float(rng.integers(lo, hi)) + float(rng.integers(0, 10)) / 10.0
                deliveries.append(dict(solvent=solvent, mode="bulk", t=arrive, gal=gal, kg=None))
            else:
                n = int(rng.integers(size[0], size[1] + 1))
                kg = round(sum(float(rng.uniform(*unit_kg)) for _ in range(n)), 1)
                deliveries.append(dict(solvent=solvent, mode=mode, t=arrive, n=n, kg=kg, gal=None))
            g = gap if not (solvent == "n-heptane" and t >= CODE_SWITCH) else (20, 35)
            t = arrive + int(rng.integers(g[0], g[1] + 1)) * 1440
    # nothing is delivered while the plant is shut at Christmas; every solvent is restocked in the week before
    shut = [(-9, 1), (356, 368)]                       # day ranges: 23 Dec 2025 to 1 Jan 2026, 23 Dec 2026 to 3 Jan 2027
    deliveries = [d for d in deliveries if not any(a <= d["t"] // 1440 < b for a, b in shut)]
    for solvent, pack, gap, size, unit_kg in plan:
        for lo_day in (-15, 350):                      # 17 to 22 December
            if solvent == "isohexane" and lo_day < 0:
                continue
            if any(d["solvent"] == solvent and lo_day <= d["t"] // 1440 <= lo_day + 5 for d in deliveries):
                continue
            days = [x for x in range(lo_day, lo_day + 6) if (x + 3) % 7 < 5]
            day = days[int(rng.integers(0, len(days)))]
            arrive = day * 1440 + int(rng.integers(6 * 60 + 30, 15 * 60))
            mode = "bulk" if (pack == "bulk" or (solvent == "n-heptane" and arrive >= CODE_SWITCH)) else pack
            if mode == "bulk":
                lo, hi = (4800, 6200) if solvent == "n-heptane" else size
                gal = float(rng.integers(lo, hi)) + float(rng.integers(0, 10)) / 10.0
                deliveries.append(dict(solvent=solvent, mode="bulk", t=arrive, gal=gal, kg=None))
            else:
                n = int(rng.integers(size[0], size[1] + 1))
                kg = round(sum(float(rng.uniform(*unit_kg)) for _ in range(n)), 1)
                deliveries.append(dict(solvent=solvent, mode=mode, t=arrive, n=n, kg=kg, gal=None))
    # the 2026 year-end restock is ordered against the 2027 production plan, so it is not the size of the last one
    def lb(d):
        return d["gal"] * DENSITY_LB_GAL[d["solvent"]] if d["mode"] == "bulk" else d["kg"] * LB_PER_KG
    for solvent, pack, gap, size, unit_kg in plan:
        before = sum(lb(d) for d in deliveries if d["solvent"] == solvent and -15 <= d["t"] // 1440 <= 0)
        last = [d for d in deliveries if d["solvent"] == solvent and 350 <= d["t"] // 1440 <= 367]
        while last and abs(sum(lb(d) for d in last) - before) < 400:
            d = last[-1]
            if d["mode"] == "bulk":
                d["gal"] = round(d["gal"] + 640.0, 1)
            else:
                extra = [float(rng.uniform(*unit_kg)) for _ in range(3)]
                d["n"] += 3
                d["kg"] = round(d["kg"] + sum(extra), 1)
    deliveries.sort(key=lambda d: (d["t"], d["solvent"]))
    w.deliveries = deliveries


if __name__ == "__main__":
    import time
    t0 = time.time()
    w = simulate()
    print("simulated in %.1fs, %d steps" % (time.time() - t0, len(w.steps)))
    unc = w.voc_min.sum()
    print("uncontrolled %.1f t; minutes over fan %d; peak %.0f" % (unc / 2000, int((w.flow > FAN_MAX).sum()), w.flow.max()))
    for mode, bm, oc in (("default", 1, False), ("default", 1, True), ("golden", 60, True), ("golden", 15, True),
                         ("golden", 5, True), ("golden", 1, True)):
        q, y = emitted(w, mode, bm, offline_counts=oc)
        print("%-8s bin %3d offline %-5s: year %.3f t  quarters %s" % (mode, bm, oc, y / 2000, [round(x / 2000, 3) for x in q]))

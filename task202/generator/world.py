"""Selwith Water, October 2023 to October 2026: the clean truth every file is cut from.

The lake's daily temperature profile, the River Lenning's hourly temperature, conductivity, flow and phosphorus,
the inlet sampler's bottles, the regulator's two upstream gauges, the two works' daily effluent, the Mill Beck
outfall, the buoy's sondes, the laboratory's lake samples and the Connect Right survey.  Nothing here is written
to a file; pack.py cuts the files and golden.py computes every answer from this state.
"""
import datetime as dt
import math

import numpy as np

SEED = 202
D0 = dt.date(2023, 9, 24)
D1 = dt.date(2026, 10, 31)
NDAY = (D1 - D0).days + 1
DAYS = [D0 + dt.timedelta(i) for i in range(NDAY)]
DEPTHS = [0.5] + [float(z) for z in range(1, 26)]
SONDE_DEPTHS = [1.0, 5.0, 10.0, 15.0, 20.0]
SEASONS = (2024, 2025, 2026)
WINTERS = ((2023, 2024), (2024, 2025), (2025, 2026))
GAUGE_SWITCH = dt.date(2024, 6, 1)        # the station's own inlet gauge replaces the Lenning Bridge feed
CREDIT = {"A": 0.30, "B": 0.82, "C": 0.71, "D": 0.50}
# levels set so every graded figure prints clear of its rounding edge (checks.py asserts the clearances)
Q_SCALE = 0.996
HOL_BASE = 2620.0
OUT_DRY = 516.25
LAB_TP0 = 14.55
LAB_CHLF = 0.93
HOL_TP = 0.857


def rng(stream):
    return np.random.default_rng([SEED, stream])


def density(t):
    """Pure-water density in kg/m3 (Kell 1975 / UNESCO), t in degrees C."""
    t = np.asarray(t, dtype=float)
    num = (999.83952 + 16.945176 * t - 7.9870401e-3 * t ** 2 - 46.170461e-6 * t ** 3
           + 105.56302e-9 * t ** 4 - 280.54253e-12 * t ** 5)
    return num / (1 + 16.879850e-3 * t)


def doy(d):
    return d.timetuple().tm_yday


def is_season(d):
    return 6 <= d.month <= 9 and d.year in SEASONS


def winter_of(d):
    """(y0, y1) for 1 October y0 to 30 April y1, else None."""
    if d.month >= 10:
        k = (d.year, d.year + 1)
    elif d.month <= 4:
        k = (d.year - 1, d.year)
    else:
        return None
    return k if k in WINTERS else None


# ----------------------------------------------------------------------------------------------- the lake
def lake():
    r = rng(1)
    yoff = {2023: 0.2, 2024: 0.25, 2025: 0.85, 2026: 0.1}
    onset = {2024: 121, 2025: 116, 2026: 124}      # day of year the lake stratifies
    turn = {2023: 288, 2024: 291, 2025: 296, 2026: 289}   # day of year it overturns
    eps = 0.0
    ts = np.zeros(NDAY)
    for i, d in enumerate(DAYS):
        eps = 0.86 * eps + r.normal(0, 0.42)
        base = 11.0 + 7.6 * math.sin(2 * math.pi * (doy(d) - 115) / 365.25) + yoff[d.year]
        ts[i] = max(4.25 + 0.15 * r.random(), base + eps)
    prof = np.zeros((NDAY, len(DEPTHS)))
    strat = np.zeros(NDAY, dtype=bool)
    zt = np.full(NDAY, np.nan)
    th = np.zeros(NDAY)
    hyp = None
    for i, d in enumerate(DAYS):
        k = doy(d)
        on = onset.get(d.year)
        off = turn.get(d.year)
        s = on is not None and on <= k < off
        strat[i] = s
        if s:
            if hyp is None or (i > 0 and not strat[i - 1]):
                hyp = min(ts[i] - 0.6, 6.25 + 0.2 * r.random())
            hyp += 0.0062 + 0.0015 * r.normal()
            frac = (k - on) / (off - on)
            zt[i] = 4.7 + 6.4 * frac ** 0.78 + r.normal(0, 0.18)
            th[i] = hyp
            w = 1.05 + 0.1 * r.random()
            for j, z in enumerate(DEPTHS):
                prof[i, j] = hyp + (ts[i] - hyp) / (1 + math.exp((z - zt[i]) / w))
        else:
            hyp = None
            th[i] = ts[i]
            for j, z in enumerate(DEPTHS):
                prof[i, j] = ts[i] - 0.004 * z + r.normal(0, 0.02)
    prof += r.normal(0, 0.03, prof.shape)
    return dict(ts=ts, prof=prof, strat=strat, zt=zt, th=th, onset=onset, turn=turn)


# ----------------------------------------------------------------------------------------------- the river
def river(lk):
    """Hourly, UTC, for the River Lenning at the lake inlet, with Brankell Beck's share."""
    r = rng(2)
    nh = NDAY * 24
    t0 = dt.datetime(D0.year, D0.month, D0.day)
    hours = [t0 + dt.timedelta(hours=h) for h in range(nh)]
    q = np.zeros(nh)
    storm_flag = np.zeros(nh, dtype=bool)
    base = np.array([1.48 + 0.84 * math.cos(2 * math.pi * (doy(h.date()) - 18) / 365.25) for h in hours])
    base *= np.exp(np.convolve(r.normal(0, 0.035, nh), np.ones(240) / 240 * 24, mode="same"))
    base *= Q_SCALE
    q[:] = base
    storms = []
    h = 0
    while h < nh:
        mo = hours[h].month
        rate = 0.0052 if mo in (10, 11, 12, 1, 2, 3) else (0.0034 if mo in (4, 5) else 0.0022)
        gap = int(r.exponential(1 / rate))
        h += max(gap, 30)
        if h >= nh:
            break
        mo = hours[h].month
        wet = mo in (10, 11, 12, 1, 2, 3, 4)
        peak = Q_SCALE * float(np.exp(r.normal(math.log(5.2 if wet else 1.9), 0.55)))
        rise = int(r.integers(4, 10))
        tau = float(r.uniform(16, 34))
        storms.append((h, peak, rise, tau, wet))
        for k in range(rise + 160):
            if h + k >= nh:
                break
            add = peak * (k / rise if k < rise else math.exp(-(k - rise) / tau))
            q[h + k] += add
    brankell_share = np.clip(0.152 + 0.012 * np.sin(np.arange(nh) / 900.0) + r.normal(0, 0.004, nh), 0.12, 0.19)
    q_brankell = q * brankell_share
    q_bridge = q - q_brankell
    # temperature, degrees C
    tday = np.zeros(NDAY)
    eps = 0.0
    for i, d in enumerate(DAYS):
        eps = 0.7 * eps + r.normal(0, 0.22)
        yo = 0.2 if d.year == 2025 else 0.0
        tday[i] = 8.6 + 2.55 * math.sin(2 * math.pi * (doy(d) - 125) / 365.25) + yo + eps
    temp = np.zeros(nh)
    for hh in range(nh):
        i = hh // 24
        hod = hh % 24
        temp[hh] = tday[i] + 0.55 * math.sin(2 * math.pi * (hod - 9) / 24)
    # storm water: warmer than the springs in summer, cooler in winter
    excess = np.clip((q - base) / np.maximum(base, 0.3), 0, 6)
    summer = np.array([1.0 if 5 <= hh.month <= 9 else -0.35 for hh in hours])
    temp += 0.32 * excess * summer + r.normal(0, 0.06, nh)
    cond = 31.5 / (1 + 0.22 * excess) + r.normal(0, 0.25, nh)      # mS/m
    turb = 2.1 + 9.0 * excess ** 1.15 + np.abs(r.normal(0, 0.5, nh))
    return dict(hours=hours, q=q, q_brankell=q_brankell, q_bridge=q_bridge, base=base, temp=temp, cond=cond,
                turb=turb, storms=storms, excess=excess)


# ----------------------------------------------------------------------------------------------- the works
def works(lk):
    r = rng(3)
    out = {}
    surf = lk["prof"][:, :6].mean(axis=1)
    for name in ("Brathwick", "Hollinsby"):
        flow = np.zeros(NDAY)
        tp = np.zeros(NDAY)
        tef = np.zeros(NDAY)
        for i, d in enumerate(DAYS):
            m = d.month
            if name == "Brathwick":
                f = 636 + 18 * math.cos(2 * math.pi * (doy(d) - 20) / 365.25)
                c = 5.62 + 0.18 * math.sin(2 * math.pi * (doy(d) - 60) / 365.25)
                te = 10.9 + 3.6 * math.sin(2 * math.pi * (doy(d) - 118) / 365.25)
            else:
                tour = {6: 230, 7: 520, 8: 545, 9: 190}.get(m, 60 if m in (4, 5, 10) else 0)
                f = HOL_BASE + tour
                c = HOL_TP + 0.03 * math.sin(2 * math.pi * (doy(d) - 30) / 365.25)
                te = surf[i] + (2.1 if 6 <= m <= 9 else 2.6) + 0.15 * math.sin(i / 9.0)
            flow[i] = f * math.exp(r.normal(0, 0.05))
            tp[i] = c * math.exp(r.normal(0, 0.07))
            tef[i] = te + r.normal(0, 0.3)
        out[name] = dict(flow=flow, tp=tp, temp=tef, load=flow * tp / 1000.0)
    return out


def river_phosphorus(rv, wk):
    """Hourly total phosphorus in ug/L at the inlet: springs, Brathwick's effluent, the farms' runoff."""
    r = rng(4)
    nh = len(rv["q"])
    lb = np.repeat(wk["Brathwick"]["load"], 24)           # kg/d
    brath = lb * 11.574 / np.maximum(rv["q"], 0.05)
    wetness = np.array([1.0 if h.month in (11, 12, 1, 2, 3) else (0.7 if h.month in (10, 4) else 0.28)
                        for h in rv["hours"]])
    farm = 3.0 + 72.0 * wetness * rv["excess"] ** 0.9 + 8.0 * wetness
    spring = 11.0 + r.normal(0, 0.6, nh)
    tp = spring + brath + farm * np.exp(r.normal(0, 0.06, nh))
    srp = 6.0 + 0.82 * brath + 0.22 * farm
    return dict(tp=tp, srp=srp, brath=brath, farm=farm, spring=spring)


# ----------------------------------------------------------------------------------------------- the sampler
def sampler(rv, ph):
    """Daily 24-sub-sample composites 09:00 to 09:00 UK clock time all year; from October to April a storm
    programme fills four-hour bottles while the stage is up, and the day bottle skips those sub-samples."""
    r = rng(5)
    hours = rv["hours"]
    nh = len(hours)
    q = rv["q"]
    base = rv["base"]
    trig = np.zeros(nh, dtype=bool)
    for hh in range(nh):
        mo = hours[hh].month
        if mo in (10, 11, 12, 1, 2, 3, 4):
            trig[hh] = q[hh] > max(2.0 * base[hh], 3.2)
    # storm bottles: consecutive triggered hours cut into four-hour bottles
    storm_of = np.full(nh, -1)
    bottles = []
    hh = 0
    while hh < nh:
        if trig[hh]:
            s = hh
            while hh < nh and trig[hh]:
                hh += 1
            e = hh
            k = s
            while k < e:
                kk = min(k + 4, e)
                bid = len(bottles)
                bottles.append(dict(kind="STORM", h0=k, h1=kk))
                storm_of[k:kk] = bid
                k = kk
        else:
            hh += 1
    # day bottles: 09:00 UK clock to 09:00 next day
    day_bottles = []

    def h9(d):
        local9 = dt.datetime(d.year, d.month, d.day, 9)
        utc9 = local9 - dt.timedelta(hours=uk_offset(local9))
        return int((utc9 - hours[0]).total_seconds() // 3600)
    for i, d in enumerate(DAYS[:-1]):
        h0 = h9(d)
        h1 = h9(DAYS[i + 1])
        if h0 < 0 or h1 > nh:
            continue
        idx = [x for x in range(h0, h1) if storm_of[x] < 0]
        if idx:                      # a day the storm programme sampled throughout leaves the day bottle empty
            day_bottles.append(dict(kind="DAY", h0=h0, h1=h1, sub=idx, day=d))
    # sampler faults: a few summer days with no day bottle (none from October to April)
    drop = set()
    for b in day_bottles:
        if 5 <= b["day"].month <= 9 and r.random() < 0.012:
            drop.add(b["day"])
    day_bottles = [b for b in day_bottles if b["day"] not in drop]
    for b in bottles:
        b["sub"] = list(range(b["h0"], b["h1"]))
    allb = day_bottles + bottles
    for b in allb:
        conc = ph["tp"][b["sub"]].mean() if b["sub"] else float("nan")
        srp = ph["srp"][b["sub"]].mean() if b["sub"] else float("nan")
        b["tp"] = float(conc * math.exp(r.normal(0, 0.035)))
        b["srp"] = float(srp * math.exp(r.normal(0, 0.05)))
    return dict(day=day_bottles, storm=bottles, storm_of=storm_of)


def uk_offset(local):
    """Hours UK clock time is ahead of UTC at a local wall-clock time (BST from the last Sunday of March 01:00 UTC
    to the last Sunday of October 01:00 UTC)."""
    y = local.year

    def last_sunday(m):
        d = dt.date(y, m, 31)
        while d.weekday() != 6:
            d -= dt.timedelta(1)
        return d
    start = dt.datetime.combine(last_sunday(3), dt.time(1))
    end = dt.datetime.combine(last_sunday(10), dt.time(1))
    return 1 if start <= local < end else 0


# ----------------------------------------------------------------------------------------------- outfall
def outfall(lk):
    r = rng(6)
    vol = np.zeros(NDAY)
    tp = np.zeros(NDAY)
    wet = np.zeros(NDAY, dtype=bool)
    temp = np.zeros(NDAY)
    surf = lk["prof"][:, :6].mean(axis=1)
    for i, d in enumerate(DAYS):
        dry = OUT_DRY * math.exp(r.normal(0, 0.08))
        rain = r.random() < (0.32 if d.month in (10, 11, 12, 1, 2, 3) else 0.22)
        storm = float(np.exp(r.normal(math.log(620), 0.6))) if rain else 0.0
        vol[i] = dry + storm
        c = (dry * 1.06 + storm * 0.41) / (dry + storm)
        tp[i] = c * math.exp(r.normal(0, 0.06))
        wet[i] = rain
        temp[i] = surf[i] + 2.2 + r.normal(0, 0.5)
    return dict(vol=vol, tp=tp, wet=wet, temp=temp, load=vol * tp / 1000.0)


# ----------------------------------------------------------------------------------------------- sondes
def sondes(lk, rv):
    r = rng(7)
    n = NDAY
    cond = np.zeros((n, len(SONDE_DEPTHS)))
    do = np.zeros((n, len(SONDE_DEPTHS)))
    chl = np.zeros(n)
    lake_mean = 214.0
    plume = 0.0
    epi = lake_mean
    deep_do = 11.2
    strat_prev = False
    for i, d in enumerate(DAYS):
        s = lk["strat"][i]
        if s and not strat_prev:
            epi = lake_mean
            plume = 0.0
            deep_do = 11.0
        if s:
            qday = rv["q"][i * 24:(i + 1) * 24].mean()
            plume = plume * 0.992 + 0.55 * qday
            epi = epi - 0.035 + r.normal(0, 0.05)
            deep_do = max(0.4, deep_do - 0.071 + r.normal(0, 0.02))
            vals = [epi, epi + r.normal(0, 0.3), lake_mean + min(plume, 78), lake_mean + 0.08 * min(plume, 78),
                    lake_mean + 0.02 * min(plume, 78)]
        else:
            if strat_prev:
                lake_mean = lake_mean + 0.06 * min(plume, 78)
            lake_mean = lake_mean + 0.01 * (214 - lake_mean) + r.normal(0, 0.15)
            vals = [lake_mean] * 5
            deep_do = 11.2 + r.normal(0, 0.1)
        cond[i] = np.array(vals) + r.normal(0, 0.6, 5)
        sat = 14.6 - 0.39 * lk["prof"][i, 1] + 0.007 * lk["prof"][i, 1] ** 2
        do[i, 0] = sat * (1.02 + 0.05 * r.random())
        do[i, 1] = sat * (1.0 + 0.03 * r.random())
        do[i, 2] = (sat * 0.8 if s else sat) + r.normal(0, 0.15)
        do[i, 3] = (deep_do + 1.6 if s else sat) + r.normal(0, 0.1)
        do[i, 4] = (deep_do if s else sat) + r.normal(0, 0.08)
        bloom = 0.0
        if d.month in (6, 7, 8, 9) and d.year in SEASONS:
            ph = min(max((doy(d) - 166) / 110.0, 0.0), 1.0)
            bloom = 1.5 + 9.0 * math.sin(math.pi * ph) ** 2 * (1.3 if d.year == 2025 else 1.0)
        chl[i] = max(0.6, 2.2 + bloom + r.normal(0, 0.8))
        strat_prev = s
    return dict(cond=cond, do=np.maximum(do, 0.2), chl=chl)


# ----------------------------------------------------------------------------------------------- Connect Right
STREETS = ["Station Road", "Kirkgate", "Mill Lane", "Beck Side", "Fellview Road", "Lake Road", "Church Walk",
           "Howe Close", "Selwith Avenue", "Brackenfield", "Market Street", "Low Green", "Tarn Crescent",
           "Gill Bank", "Moss Lane", "School Brow", "Hollin Road", "Lenning Drive"]
BLOCKS = ["Beckside Court", "Fellgate House", "Mill House", "Kirkstead Court", "Lakeview Apartments",
          "Old Bank Chambers", "Howe Mews", "St Olaf's Court", "Tarnside", "The Maltings", "Station House",
          "Ghyll Court", "Brackenfield House", "Market Hall Flats"]


def survey():
    """Properties draining to the Mill Beck outfall and the trust's Connect Right visits, May 2025 to Oct 2026."""
    r = rng(8)
    props = []
    used = set()

    def uprn():
        while True:
            u = "1000" + str(int(r.integers(10000000, 99999999)))
            if u not in used:
                used.add(u)
                return u
    for s in STREETS:
        n = int(r.integers(18, 44))
        nums = sorted(set(int(x) for x in r.integers(1, 120, n)))
        for k in nums:
            props.append(dict(uprn=uprn(), parent="", addr="%d %s" % (k, s), kind="House",
                              run="SW-HB-%04d" % int(r.integers(100, 900))))
    blocks = []
    for b in BLOCKS:
        street = STREETS[int(r.integers(0, len(STREETS)))]
        num = int(r.integers(1, 90))
        pu = uprn()
        nflat = int(r.integers(4, 15))
        run = "SW-HB-%04d" % int(r.integers(100, 900))
        blocks.append(dict(uprn=pu, name=b, addr="%s, %d %s" % (b, num, street), flats=[], run=run))
        props.append(dict(uprn=pu, parent="", addr="%s, %d %s" % (b, num, street), kind="Block", run=run))
        for f in range(1, nflat + 1):
            fu = uprn()
            blocks[-1]["flats"].append(fu)
            props.append(dict(uprn=fu, parent=pu, addr="Flat %d, %s, %d %s" % (f, b, num, street), kind="Flat",
                              run=run))
    # outcomes
    start = dt.date(2025, 5, 12)
    end = dt.date(2026, 9, 30)
    close0 = dt.date(2026, 9, 14)            # the contractor's close-out round of every outstanding misconnection
    span = (end - start).days
    visits = []
    truth = dict(mis_dwell=set(), fixed_dwell=set(), closeout_fixed=set(), fixed_after=set())
    seq = [0]

    def weekday(d, back=True):
        if d.weekday() >= 5:
            d = d - dt.timedelta(d.weekday() - 4) if back else d + dt.timedelta(7 - d.weekday())
        return d

    def visit(u, day, outcome, appliance="", sync=None):
        seq[0] += 1
        if sync is None:
            lag = int(min(24, r.geometric(0.28) - 1)) if r.random() < 0.55 else 0
            sync = day + dt.timedelta(lag)
        visits.append(dict(uprn=u, day=day, sync=sync, outcome=outcome, appliance=appliance, seq=seq[0]))

    def closeout(u, fx, app, dwell):
        """The re-visit in the close-out round; the round's tablets were uploaded in October."""
        cv = weekday(close0 + dt.timedelta(int(r.integers(0, 20))))
        up = max(cv, [dt.date(2026, 10, 2), dt.date(2026, 10, 5), dt.date(2026, 10, 6)][int(r.integers(0, 3))])
        if r.random() < 0.08:
            visit(u, cv, "NO ACCESS", "", sync=up)
        elif fx is not None and fx <= cv:
            visit(u, cv, "FIX CONFIRMED", app, sync=up)
            if cv <= end:
                truth["fixed_dwell"].update(dwell)
                truth["closeout_fixed"].update(dwell)
            else:
                truth["fixed_after"].update(dwell)
        else:
            visit(u, cv, "MISCONNECTED", app, sync=up)

    def outcome_of(u, d0, app, p_fix, lo, hi, dwell):
        visit(u, d0, "MISCONNECTED", app)
        truth["mis_dwell"].update(dwell)
        fx = d0 + dt.timedelta(int(r.integers(lo, hi))) if r.random() < p_fix else None   # the day the fix is made
        conf = weekday(fx + dt.timedelta(int(r.integers(4, 75)))) if fx is not None else None   # its re-visit
        if conf is not None and conf < close0:
            visit(u, conf, "FIX CONFIRMED", app)
            truth["fixed_dwell"].update(dwell)
        else:
            closeout(u, fx, app, dwell)
    houses = [p for p in props if p["kind"] == "House"]
    for p in houses:
        d0 = weekday(start + dt.timedelta(int(r.integers(0, span - 120))))
        if r.random() < 0.09:
            visit(p["uprn"], d0, "NO ACCESS")
            d0 = weekday(d0 + dt.timedelta(int(r.integers(9, 40))), back=False)
        if r.random() < 0.118:
            app = ["washing machine", "dishwasher", "kitchen sink", "WC", "utility sink"][int(r.integers(0, 5))]
            outcome_of(p["uprn"], d0, app, 0.62, 30, 300, [p["uprn"]])
        else:
            visit(p["uprn"], d0, "CORRECTLY CONNECTED")
    for b in blocks:
        d0 = weekday(start + dt.timedelta(int(r.integers(0, span - 150))))
        if r.random() < 0.46:
            outcome_of(b["uprn"], d0, "shared soil stack", 0.6, 40, 330, b["flats"])
        else:
            visit(b["uprn"], d0, "CORRECTLY CONNECTED")
    visits.sort(key=lambda v: (v["sync"], v["seq"]))
    return dict(props=props, blocks=blocks, visits=visits, truth=truth)


# ----------------------------------------------------------------------------------------------- the laboratory
def lab(lk, sd):
    """The lake laboratory's samples: the north basin site (0 to 5 m tube and a 20 m bottle) fortnightly from
    April to October and monthly in winter; from April 2025 the Hollinsby Bay site (a 0 to 5 m tube from the boat) under the
    code the north basin site used to carry."""
    r = rng(9)
    rows = []
    for i, d in enumerate(DAYS):
        if d.weekday() != 1:
            continue
        summer = 4 <= d.month <= 10
        if not summer and d.day > 7:
            continue
        if summer and not (d.day <= 7 or 15 <= d.day <= 21):
            continue
        s = lk["strat"][i]
        chl_true = LAB_CHLF * sd["chl"][i] * math.exp(r.normal(0, 0.12))
        tp_s = LAB_TP0 + 1.9 * chl_true + r.normal(0, 1.2)
        tp_d = (tp_s + 4 + (16 if s and d.month >= 7 else 0)) * math.exp(r.normal(0, 0.06))
        rows.append(dict(day=d, site="north", depth="0-5", tp=tp_s, chl=chl_true))
        rows.append(dict(day=d, site="north", depth="20", tp=tp_d, chl=None))
        if d >= dt.date(2025, 4, 1) and summer:
            near_chl = chl_true * (1.35 + 0.25 * r.random())
            rows.append(dict(day=d, site="bay", depth="0-5", tp=tp_s * 1.3 + 3, chl=near_chl))
    return rows


# ----------------------------------------------------------------------------------------------- distractors
def bathing():
    r = rng(10)
    out = []
    for y in SEASONS:
        d = dt.date(y, 5, 15)
        while d <= dt.date(y, 9, 30):
            ec = float(np.exp(r.normal(math.log(60), 0.9)))
            ie = float(np.exp(r.normal(math.log(22), 0.9)))
            out.append(dict(day=d, ec=int(round(ec)), ie=int(round(ie))))
            d += dt.timedelta(int(r.integers(6, 9)))
    return out


def farmyards():
    r = rng(11)
    names = ["Howe Farm", "Low Brankell", "High Lenning", "Brackenhowe", "Gillside", "Raven Hill Farm",
             "Kirkgate Farm", "Thornyhow", "Lenning Hall", "Fold End", "Birkhowe", "Stangrigg", "Moss Side",
             "Hollin Bank", "Scarside", "Nether Brankell", "Tarnside Farm", "Mire End"]
    out = []
    for n in names:
        out.append(dict(holding=n, cph="08/%03d/%04d" % (int(r.integers(100, 400)), int(r.integers(1000, 9999))),
                        cattle=int(r.integers(0, 260)), sheep=int(r.integers(80, 1400)),
                        yard_m2=int(r.integers(300, 4200)), roofed_pct=int(r.integers(10, 90)),
                        slurry_months=round(float(r.uniform(1.5, 6.5)), 1),
                        sub=["Lenning", "Brankell Beck", "Lenning"][int(r.integers(0, 3))]))
    return out

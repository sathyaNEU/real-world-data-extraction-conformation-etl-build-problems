"""The world as it happened, July 2026 to December 2027: a trust's bedside glucose meters on thirteen wards of three
hospitals, the patients they tested, each meter's own systematic error, the central laboratory's two analyzers, the
scheduled pairings on the morning round and the confirmations of critical readings, the meters' dockings and the
server's receptions, the meters moved between wards and the daily quality-control runs. Nothing here is written to
the pack; records.py turns it into files.

    world(seed) -> dict

Clocks: every instant is minutes from START 00:00 UTC. The meters' own clocks run on solar time (UTC+1) all year,
the laboratory's on civil time (Europe/Rome), the data manager's server stamps receptions in UTC."""
import datetime as dt
import zoneinfo

import numpy as np

ROME = zoneinfo.ZoneInfo("Europe/Rome")
UTC = dt.timezone.utc
T0 = dt.datetime(2026, 7, 1)
START = dt.date(2026, 7, 1)
END = dt.date(2027, 12, 31)
DAYS = (END - START).days + 1
SERVICE = dt.date(2027, 1, 18)                          # the manufacturer's 2027 visit: 18 to 22 January
SWITCH = dt.date(2027, 9, 13)                           # analyzer B in service; A until the day before
PARALLEL = (dt.date(2027, 8, 30), dt.date(2027, 9, 10))
LAB_A = 0.035                                           # analyzer A against B, proportional
SA, SP = 5.0, 0.05                                      # meter random error: constant (mg/dL) and proportional
CAPVEN = 0.015                                          # capillary against venous, the minutes between them
CV_LAB, SD_LAB = 0.018, 0.8
CRIT_LO, CRIT_HI = 50.0, 400.0
LO, HI = 20.0, 600.0                                    # the meter's measuring range
CONFIRM = 0.93
ROUND = (6 * 60, 7 * 60 + 30)                           # the morning round, civil time
P_FAIL = 0.025                                          # a docking whose acknowledgement the meter never gets

# code, name, hospital, median glucose (mg/dL), log sd, patient tests per meter-day, verification weekdays,
# beds, mean stay (days), mean minutes between dockings in the day
WARDS = [
    ("TIN", "Terapia intensiva neonatale", "CM", 70.0, 0.30, 5.0, (0, 2, 4), 12, 14.0, 55),
    ("NIDO", "Nido", "CM", 60.0, 0.28, 4.0, (0, 2, 4), 16, 3.0, 70),
    ("TI", "Terapia intensiva", "CM", 165.0, 0.42, 7.0, (1, 4), 10, 8.0, 40),
    ("DIAB", "Diabetologia", "CM", 190.0, 0.42, 4.0, (1, 4), 14, 6.0, 85),
    ("PS", "Pronto soccorso", "CM", 150.0, 0.45, 3.5, (0, 3), 22, 0.6, 35),
    ("MED", "Medicina generale", "CM", 140.0, 0.33, 5.0, (2, 5), 36, 9.0, 105),
    ("CHIR", "Chirurgia generale", "CM", 128.0, 0.30, 3.5, (1, 4), 30, 6.0, 115),
    ("PED", "Pediatria", "RV", 100.0, 0.30, 2.0, (0, 3), 14, 4.0, 95),
    ("OST", "Ostetricia e ginecologia", "RV", 95.0, 0.25, 2.0, (1, 4), 18, 3.0, 105),
    ("MEDR", "Medicina", "RV", 142.0, 0.33, 4.5, (2, 5), 30, 9.0, 125),
    ("PSR", "Pronto soccorso", "RV", 148.0, 0.44, 2.5, (0, 3), 12, 0.6, 50),
    ("MEDV", "Medicina", "VD", 138.0, 0.33, 4.0, (1, 4), 24, 10.0, 190),
    ("LUN", "Lungodegenza", "VD", 132.0, 0.30, 3.0, (2, 5), 20, 25.0, 240),
]
W_ = {w[0]: w for w in WARDS}
BIAS = {
    "TIN": [-0.022, 0.006, -0.081, 0.012, -0.076],
    "NIDO": [0.084, -0.019, 0.004, 0.033],
    "TI": [0.014, -0.006, -0.083, 0.021, -0.011],
    "DIAB": [0.012, 0.088, -0.013, 0.007],
    "PS": [0.018, -0.022, 0.006, -0.009],
    "MED": [0.011, -0.016, 0.002, -0.079, 0.019, -0.004],
    "CHIR": [0.091, -0.008, 0.015, 0.003],
    "PED": [0.006, -0.019, 0.013],
    "OST": [-0.025, 0.010, 0.004],
    "MEDR": [0.016, -0.027, 0.022, -0.003],
    "PSR": [-0.014, 0.009, 0.017],
    "MEDV": [0.005, -0.021, 0.012, 0.086],
    "LUN": [-0.009, 0.015, -0.002],
}
# meters moved for good in 2027: (home ward, index, new ward, first day there)
MOVES = [("TI", 4, "PS", dt.date(2027, 2, 15)), ("MED", 5, "CHIR", dt.date(2027, 3, 8)),
         ("OST", 1, "PED", dt.date(2027, 4, 12)), ("PSR", 2, "MEDV", dt.date(2027, 5, 10)),
         ("LUN", 2, "MEDR", dt.date(2027, 6, 21)), ("DIAB", 3, "TIN", dt.date(2027, 9, 6)),
         ("NIDO", 2, "OST", dt.date(2027, 10, 4))]
PRE_BIAS_SD = 0.03
HOLIDAYS = [dt.date(2026, 8, 15), dt.date(2026, 11, 1), dt.date(2026, 12, 8), dt.date(2026, 12, 25),
            dt.date(2026, 12, 26), dt.date(2027, 1, 1), dt.date(2027, 1, 6), dt.date(2027, 3, 29),
            dt.date(2027, 4, 25), dt.date(2027, 5, 1), dt.date(2027, 6, 2), dt.date(2027, 8, 15),
            dt.date(2027, 11, 1), dt.date(2027, 12, 8), dt.date(2027, 12, 25), dt.date(2027, 12, 26)]
HSET = set(HOLIDAYS)
NEWYEAR = dt.date(2027, 1, 1)


def day(k):
    return START + dt.timedelta(days=int(k))


def civil_to_utc(d, minute):
    t = dt.datetime.combine(d, dt.time(0), tzinfo=ROME) + dt.timedelta(minutes=int(minute))
    return int((t.astimezone(UTC).replace(tzinfo=None) - T0).total_seconds() // 60)


def utc_to_civil(u):
    t = (T0 + dt.timedelta(minutes=int(u))).replace(tzinfo=UTC).astimezone(ROME).replace(tzinfo=None)
    return t


def utc_to_solar(u):
    return T0 + dt.timedelta(minutes=int(u) + 60)


def meter_sd(t):
    return np.sqrt(SA ** 2 + (SP * t) ** 2)


def ward_on(m, d):
    return m["ward2"] if (m["move"] is not None and d >= m["move"]) else m["ward"]


def plan_rows(m):
    """The meter's verification plan: (weekdays, first day, last day) per ward it sat on."""
    if m["move"] is None:
        return [(W_[m["ward"]][6], START, END)]
    return [(W_[m["ward"]][6], START, m["move"] - dt.timedelta(days=1)), (W_[m["ward2"]][6], m["move"], END)]


def planned_dates(m):
    out = set()
    for wd, a, b in plan_rows(m):
        d = a
        while d <= b:
            if d.weekday() in wd:
                x = d
                while x in HSET or x.weekday() == 6:
                    x += dt.timedelta(days=1)
                if x <= END:
                    out.add(x)
            d += dt.timedelta(days=1)
    return out


def _census(rng, code, used):
    """Each ward's patients day by day: admissions and stays; returns {date: [patient ids]}."""
    _, _, _, _, _, _, _, beds, los, _ = W_[code]
    present, out = [], {}
    for k in range(-30, DAYS):
        d = START + dt.timedelta(days=k)
        present = [(p, e) for p, e in present if e > d]
        n_new = rng.poisson(beds / los * (0.9 + 0.2 * rng.random()))
        for _ in range(n_new):
            while True:
                pid = "P%08d" % int(rng.integers(10 ** 7, 10 ** 8))
                if pid not in used:
                    used.add(pid)
                    break
            stay = max(1, int(round(rng.exponential(los)))) if los >= 1 else 1
            present.append((pid, d + dt.timedelta(days=stay)))
        if k >= 0:
            out[d] = [p for p, _ in present] or [present[-1][0] if present else "P%08d" % 0]
    return out


def world(seed):
    rng = np.random.default_rng(seed)
    meters = []
    for (code, name, hosp, mu, sd, rate, wd, beds, los, dock) in WARDS:
        for j, b in enumerate(BIAS[code]):
            mv = [x for x in MOVES if x[0] == code and x[1] == j]
            meters.append(dict(ward=code, j=j, b=b, b_pre=float(rng.normal(0, PRE_BIAS_SD)),
                               svc=SERVICE + dt.timedelta(days=int(rng.integers(0, 5))),
                               move=mv[0][3] if mv else None, ward2=mv[0][2] if mv else None,
                               q_off=float(rng.normal(0, 0.02))))
            m = meters[-1]
            while m["svc"] in planned_dates(m):           # the visit never falls on one of the meter's pairing days
                m["svc"] = SERVICE + dt.timedelta(days=(m["svc"] - SERVICE).days % 5 + 1)
                if m["svc"] > SERVICE + dt.timedelta(days=4):
                    m["svc"] = SERVICE
    used = set()
    census = {w[0]: _census(rng, w[0], used) for w in WARDS}
    plans = [planned_dates(m) for m in meters]
    tests, pairs = [], []
    for m_i, m in enumerate(meters):
        planned = plans[m_i]
        for k in range(DAYS):
            d = day(k)
            w = ward_on(m, d)
            code, name, hosp, mu, sd, rate, wd, beds, los, dock = W_[w]
            b = m["b"] if d > m["svc"] else m["b_pre"]
            n = rng.poisson(rate)
            if code in ("TIN", "NIDO"):
                slots = rng.choice(8, size=min(n, 8), replace=False)
                mins = np.sort(slots * 180 + rng.integers(-25, 26, size=slots.size)) % 1440
            else:
                centres = np.array([390, 690, 1050, 1290])
                mins = np.sort((rng.choice(centres, size=n) + rng.normal(0, 40, n)).astype(int) % 1440)
            T = np.exp(rng.normal(np.log(mu), sd, mins.size))
            M = T * (1 + b) + rng.normal(0, 1, mins.size) * meter_sd(T)
            pts = census[w][d]
            for t, mm, mi in zip(T, M, mins):
                u = civil_to_utc(d, mi)
                rec = dict(m=m_i, utc=u, T=float(t), M=float(mm), kind="P", ward=w, pid=pts[int(rng.integers(len(pts)))])
                # nobody tested in the first hour of 2027, and a meter on the night it changed ward was in the office
                skip = (d == NEWYEAR and mi < 60) or (m["move"] is not None and d == m["move"] and mi < 120)
                if not skip:
                    tests.append(rec)
                if (mm < CRIT_LO or mm > CRIT_HI) and rng.random() < CONFIRM:
                    draw = u + int(rng.integers(4, 26))
                    civ = utc_to_civil(draw)
                    cm = civ.hour * 60 + civ.minute
                    if civ.date() in planned and ROUND[0] <= cm <= ROUND[1]:
                        draw = civil_to_utc(civ.date(), ROUND[1] + 12 + int(rng.integers(3, 15)))
                    elif civ.date() in planned and ROUND[0] - 12 <= cm < ROUND[0]:
                        draw -= 12                              # a confirmation never sits at the round's edges
                    elif civ.date() in planned and ROUND[1] < cm <= ROUND[1] + 12:
                        draw += 12
                    tl = float(t * (1 + rng.normal(0, CAPVEN)))
                    shown = mm < LO or mm > HI or round(mm) < CRIT_LO or round(mm) > CRIT_HI
                    if not skip and shown:                     # the nurse acts on the number the meter shows
                        pairs.append(dict(test=len(tests) - 1, draw=draw, kind="CV", T_lab=tl))
            if d in planned:
                draw = civil_to_utc(d, int(rng.integers(ROUND[0], ROUND[1] + 1)))
                t = float(np.exp(rng.normal(np.log(mu), sd)))
                mm = float(t * (1 + b) + rng.normal() * meter_sd(t))
                tests.append(dict(m=m_i, utc=draw + int(rng.integers(-4, 7)), T=t, M=mm, kind="P", ward=w,
                                  pid=pts[int(rng.integers(len(pts)))]))
                pairs.append(dict(test=len(tests) - 1, draw=draw, kind="CP",
                                  T_lab=float(t * (1 + rng.normal(0, CAPVEN)))))
            # quality control at the start of the morning shift, two levels
            qu = civil_to_utc(d, int(rng.integers(7 * 60, 8 * 60 + 30)))
            for lev, tgt in ((1, 46.0), (2, 305.0)):
                tests.append(dict(m=m_i, utc=qu + lev, T=tgt, M=float(tgt * (1 + m["q_off"]) + rng.normal() *
                                                                       meter_sd(tgt) * 0.8),
                                  kind="Q%d" % lev, ward=w, pid=""))
    for p in pairs:
        dd = utc_to_civil(p["draw"]).date()
        a = LAB_A if dd < SWITCH else 0.0
        p["L"] = float(p["T_lab"] * (1 + a) * (1 + rng.normal(0, CV_LAB)) + rng.normal(0, SD_LAB))
        p["civil_date"] = dd
    par = []
    for _ in range(312):
        t = float(np.exp(rng.normal(np.log(120), 0.5)))
        par.append((t, t * (1 + LAB_A) * (1 + rng.normal(0, CV_LAB)) + rng.normal(0, SD_LAB),
                    t * (1 + rng.normal(0, CV_LAB)) + rng.normal(0, SD_LAB)))
    return dict(meters=meters, tests=tests, pairs=pairs, parallel=par, plans=plans, census=census)


def receptions(W, seed):
    """Each meter's dockings and the server's receptions: every test is received at the first docking after it; a
    docking whose acknowledgement the meter never gets is sent again, whole, at the next one."""
    rng = np.random.default_rng(seed + 7)
    by = {}
    for i, t in enumerate(W["tests"]):
        by.setdefault(t["m"], []).append(i)
    rec = []          # (test index, reception second from T0 in UTC, copy flag)
    end_u = civil_to_utc(END + dt.timedelta(days=1), 0)
    for m_i, idx in by.items():
        m = W["meters"][m_i]
        idx.sort(key=lambda i: W["tests"][i]["utc"])
        times = [W["tests"][i]["utc"] for i in idx]
        u, docks = -60, []
        while u < end_u + 600:
            civ = utc_to_civil(u)
            w = ward_on(m, civ.date())
            mean = W_[w][9] * (1.0 if 6 <= civ.hour < 22 else 2.5)
            u += max(4, int(rng.exponential(mean)))
            docks.append(u)
        p, unacked = 0, []
        for dk in docks:
            batch = []
            while p < len(idx) and times[p] < dk - 1:
                batch.append(idx[p])
                p += 1
            sec = dk * 60 + int(rng.integers(5, 40))
            for k, i in enumerate(unacked):
                rec.append((i, sec + (4 * k) // 10, 1))
            for k, i in enumerate(batch):
                rec.append((i, sec + (4 * (k + len(unacked))) // 10, 0))
            unacked = unacked + batch if rng.random() < P_FAIL else []
            if p >= len(idx) and not unacked:
                break
    return rec

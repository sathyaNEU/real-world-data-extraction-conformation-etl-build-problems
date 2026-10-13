"""The fixed world of task256: Tamarack Valley Regional Transit Authority, a US regional transit authority choosing the
operator workstation configuration for its 2027 bus order from the eight its builder's fit report quotes. The
Authority's standard specifies the lowest-priced configuration that fits at least 95 per cent of its bus operators;
it knows its operators' bodies only through the stature and weight recorded at their DOT medical examinations, and the
five dimensions a workstation must fit only through a reference survey of working adults. Every other module reads
its constants and its records here."""
import datetime as dt
import hashlib

import numpy as np

SEED = 256
AS_OF = dt.date(2026, 9, 30)            # the roster the standard counts, and the end of every export
AUTH = "Tamarack Valley Regional Transit Authority"
AUTH_SHORT = "Tamarack Valley Transit"
MAKER = "Halvard Coach Works"
INSTITUTE = "Brennard Institute for Workplace Design"
SURVEY = "Survey of Working Adults' Body Dimensions"
SURVEY_YEAR = 2012
SURVEY_ISSUED = dt.date(2013, 5, 20)
OLD = "Ostrander Occupational Health"
NEW = "Fernhill Occupational Medicine"
CHANGEOVER = dt.date(2021, 7, 1)        # Fernhill took over the Authority's occupational health contract
TAKEN_OVER = dt.date(2021, 1, 1)        # Fernhill's system holds Ostrander's records from this date on
STANDARD = "ES-12"
STANDARD_ADOPTED = dt.date(2024, 3, 14)
FIT_REPORT_DATE = dt.date(2026, 8, 28)
BOARD_DATE = dt.date(2026, 11, 19)      # the board adopts the FY2027 capital budget, the order included
ORDER_BUSES = 52
DIVISIONS = ("Ridgeway", "Mill Street", "Fennimore")

PEOPLE = {
    "fleet": ("Tracy Reynolds", "Vehicle Procurement Manager, Fleet Engineering"),
    "halvard": ("William Roberts", "Application Engineer"),
    "ohc": ("Kelsey Sanchez", "Occupational Health Coordinator"),
    "coo": ("Donald Mcguire", "Chief Operating Officer"),
}

IN_TO_MM = 25.4
LB_TO_KG = 0.45359237


def stream(part):
    return np.random.default_rng([SEED, sum(ord(c) * (i + 1) for i, c in enumerate(part))])


def hint(*keys):
    """A stable pseudo-random integer for small texture choices."""
    return int(hashlib.sha256("/".join(str(k) for k in keys).encode()).hexdigest()[:12], 16)


# ---------------------------------------------------------------- the reference survey
# twelve dimensions in the survey's own order; millimetres, weight in kilograms
DIMS = [
    ("S", "Stature", "mm"),
    ("W", "Weight", "kg"),
    ("SH", "Sitting height", "mm"),
    ("SEH", "Eye height, sitting", "mm"),
    ("SSH", "Shoulder height, sitting", "mm"),
    ("PH", "Popliteal height", "mm"),
    ("KH", "Knee height, sitting", "mm"),
    ("BKL", "Buttock-knee length", "mm"),
    ("BPL", "Buttock-popliteal length", "mm"),
    ("TTR", "Thumb-tip reach", "mm"),
    ("HB", "Hip breadth, sitting", "mm"),
    ("AED", "Abdominal extension depth, sitting", "mm"),
]
CODES = [d[0] for d in DIMS]
FIT_DIMS = ["PH", "BKL", "SEH", "TTR", "AED"]      # the standard's five fit dimensions
SAMPLE = {"M": 2412, "F": 1938}

# published means and standard deviations (the survey's weighted estimates)
MEANS = {
    "M": [1756.0, 86.3, 914.2, 793.6, 600.3, 441.2, 553.7, 616.4, 500.6, 801.8, 372.4, 258.7],
    "F": [1625.4, 70.6, 857.0, 742.9, 563.1, 401.5, 509.8, 590.3, 485.9, 733.5, 396.8, 236.2],
}
SDS = {
    "M": [68.9, 15.1, 35.6, 34.2, 30.4, 23.8, 27.5, 29.8, 27.4, 37.6, 28.2, 39.6],
    "F": [64.8, 14.4, 33.8, 32.5, 28.7, 21.9, 25.4, 29.1, 27.0, 35.2, 33.9, 38.3],
}
# within-sex structure: length, girth and trunk-to-limb proportion
LOADINGS = {
    "M": [[.95, .00, .10], [.45, .85, .05], [.80, .10, .50], [.76, .12, .48], [.65, .15, .45], [.80, -.06, -.35],
          [.88, .05, -.30], [.78, .40, -.25], [.75, .25, -.28], [.78, .10, -.15], [.35, .82, .00], [.12, .90, .05]],
    "F": [[.94, .00, .12], [.42, .87, .04], [.79, .12, .49], [.75, .13, .47], [.63, .17, .44], [.78, -.04, -.36],
          [.87, .06, -.31], [.74, .45, -.24], [.72, .30, -.27], [.77, .11, -.16], [.30, .86, .01], [.10, .91, .06]],
}


def survey_correlations():
    """The published within-sex correlation matrices, to two decimals."""
    out = {}
    for sx in ("M", "F"):
        lam = np.array(LOADINGS[sx])
        r = lam @ lam.T
        np.fill_diagonal(r, 1.0)
        r = np.round(r, 2)
        assert np.linalg.eigvalsh(r).min() > 0.02, sx
        out[sx] = r
    return out


CORR = survey_correlations()


def survey_params(sx, codes=None):
    """Mean vector and covariance of the published survey for a sex, over the named dimensions."""
    codes = codes or CODES
    idx = [CODES.index(c) for c in codes]
    mu = np.array([MEANS[sx][i] for i in idx])
    sd = np.array([SDS[sx][i] for i in idx])
    r = CORR[sx][np.ix_(idx, idx)]
    return mu, np.outer(sd, sd) * r


# ---------------------------------------------------------------- the builder's fit report
OPTIONS = {
    "P": "Power-adjustable pedal set",
    "R": "Extended-range seat riser",
    "T": "Tilt-telescope steering column",
    "D": "Deep-travel seat track",
    "V": "Raised header and visor",
}
OPTION_ORDER = ["P", "R", "T", "D", "V"]
BASE = {"PH": (371, 505), "BKL": (520, 680), "SEH": (680, 885), "TTR": (675, None), "AED": (None, 332)}
OPTION_EFFECT = {"P": {"PH": (-25, 0), "TTR": (-25, 0)}, "R": {"PH": (0, 25), "SEH": (-25, 0), "BKL": (0, -1)},
                 "T": {"AED": (0, 60), "TTR": (-20, 0)}, "D": {"BKL": (0, 45)}, "V": {"SEH": (0, 30)}}
CONFIGS = [  # letter, options, price per bus
    ("A", [], 0),
    ("B", ["P", "R"], 1850),
    ("C", ["T"], 2350),
    ("D", ["P", "R", "V"], 2700),
    ("E", ["T", "D"], 3300),
    ("F", ["P", "R", "T"], 3900),
    ("G", ["P", "R", "T", "D"], 4450),
    ("H", ["P", "R", "T", "D", "V"], 5900),
]
LINE = 0.95


# the fit trials' own readings: a configuration's limits are not quite the sum of its options' effects
TRIAL_TRIM = {"A": {"SEH": (0, -1)}, "C": {"SEH": (0, -1)}, "F": {"SEH": (0, -1)}, "G": {"SEH": (0, -1)},
              "H": {"BKL": (0, 1)}}


def envelope(opts, config=None):
    env = {k: list(v) for k, v in BASE.items()}
    for o in opts:
        for k, (dl, dh) in OPTION_EFFECT[o].items():
            if env[k][0] is not None:
                env[k][0] += dl
            if env[k][1] is not None:
                env[k][1] += dh
    for k, (dl, dh) in TRIAL_TRIM.get(config, {}).items():
        if env[k][0] is not None:
            env[k][0] += dl
        if env[k][1] is not None:
            env[k][1] += dh
    return {k: tuple(v) for k, v in env.items()}


ENVELOPES = {c: envelope(o, c) for c, o, _ in CONFIGS}
PRICES = {c: p for c, _, p in CONFIGS}


# ---------------------------------------------------------------- the workforce
JOBS_DOT = ("BUS OPERATOR", "OPERATOR TRAINEE", "ROAD SUPERVISOR", "INSTRUCTOR - TRANSPORTATION", "MECHANIC A",
            "MECHANIC B", "SERVICE ATTENDANT")
CURRENT_COUNTS = {"BUS OPERATOR": (1522, 588), "OPERATOR TRAINEE": (31, 15), "ROAD SUPERVISOR": (39, 15),
                  "INSTRUCTOR - TRANSPORTATION": (12, 6), "MECHANIC A": (97, 4), "MECHANIC B": (58, 5),
                  "SERVICE ATTENDANT": (36, 9)}
# the operators' build at their latest examination: stature mean and sd (mm), weight mean and sd (kg), and
# the stature-weight correlation; the other staff are drawn from a little lighter
OPERATOR_BUILD = {"M": (1762.0, 80.0, 98.0, 19.0, 0.40), "F": (1628.0, 74.0, 86.0, 19.0, 0.35)}
STAFF_BUILD = {"M": (1764.0, 76.0, 93.0, 17.0, 0.40), "F": (1630.0, 70.0, 80.0, 17.0, 0.35)}


def _build(rng, n, b):
    ms, ss, mw, sw, r = b
    z = rng.standard_normal((n, 2))
    s = ms + ss * z[:, 0]
    lsd = np.sqrt(np.log(1 + (sw / mw) ** 2))
    lmu = np.log(mw) - lsd ** 2 / 2
    w = np.exp(lmu + lsd * (r * z[:, 0] + np.sqrt(1 - r * r) * z[:, 1]))
    return s, w


def _tenure_days(rng):
    u = rng.random()
    if u < 0.36:
        return int(rng.uniform(20, 3 * 365))
    if u < 0.61:
        return int(rng.uniform(3 * 365, 8 * 365))
    if u < 0.86:
        return int(rng.uniform(8 * 365, 15 * 365))
    return int(rng.uniform(15 * 365, 31 * 365))


def employees():
    """Every employee the exports or the roster hold: those on the roster on 30 September 2026 and those who left
    since 1 January 2014. Employee numbers run in hiring order."""
    rng = stream("employees")
    people = []
    for job, (nm, nf) in CURRENT_COUNTS.items():
        for sx, n in (("M", nm), ("F", nf)):
            b = OPERATOR_BUILD[sx] if job in ("BUS OPERATOR", "OPERATOR TRAINEE") else STAFF_BUILD[sx]
            s, w = _build(rng, n, b)
            for i in range(n):
                if job == "OPERATOR TRAINEE":
                    hired = AS_OF - dt.timedelta(days=int(rng.uniform(8, 40)))
                else:
                    hired = AS_OF - dt.timedelta(days=_tenure_days(rng))
                people.append({"job": job, "sex": sx, "s": float(s[i]), "w": float(w[i]), "hired": hired,
                               "left": None})
    # former staff: operators chiefly, most of them within a few years of hire
    n_former = 2480
    s_m, w_m = _build(rng, n_former, OPERATOR_BUILD["M"])
    s_f, w_f = _build(rng, n_former, OPERATOR_BUILD["F"])
    for i in range(n_former):
        sx = "F" if rng.random() < 0.31 else "M"
        job = "BUS OPERATOR" if rng.random() < 0.86 else str(rng.choice(["MECHANIC A", "MECHANIC B",
                                                                           "SERVICE ATTENDANT", "ROAD SUPERVISOR"]))
        left = dt.date(2014, 1, 1) + dt.timedelta(days=int(rng.uniform(0, (AS_OF - dt.date(2014, 1, 1)).days - 3)))
        stay = int(rng.exponential(3.2 * 365)) + 30 if rng.random() < 0.7 else int(rng.uniform(8, 32) * 365)
        hired = left - dt.timedelta(days=stay)
        people.append({"job": job, "sex": sx, "s": float(s_m[i] if sx == "M" else s_f[i]),
                       "w": float(w_m[i] if sx == "M" else w_f[i]), "hired": hired, "left": left})
    order = sorted(range(len(people)), key=lambda i: (people[i]["hired"], hint("emp", i)))
    for rank, i in enumerate(order):
        people[i]["emp"] = 1040 + rank * 3 + hint("gap", i) % 3
    for p in people:
        p["drift"] = float(np.clip(rng.normal(0.55, 0.35), -0.4, 1.6))     # kg a year
        p["bp_risk"] = float(rng.random())
    cur = [p for p in people if p["left"] is None]
    ops = [p for p in cur if p["job"] == "BUS OPERATOR"]
    for p in cur:
        p["division"] = DIVISIONS[hint("div", p["emp"]) % 3]
        p["status"] = "ACTIVE"
    for p in ops:
        tenure = (AS_OF - p["hired"]).days / 365.25
        p["pt"] = bool(rng.random() < (0.32 if tenure < 2 else 0.07))
        u = rng.random()
        p["status"] = ("LEAVE" if u < 0.035 else "LIGHT DUTY" if u < 0.06 else "MILITARY LEAVE" if u < 0.065
                       else "ACTIVE")
    return people


def true_weight(p, d):
    """A person's weight on a date: today's build less the drift since."""
    return p["w"] - p["drift"] * (AS_OF - d).days / 365.25


# ---------------------------------------------------------------- examinations and tests
def encounters(people):
    """Every occupational health encounter of the staff in DOT-regulated jobs, 1 January 2014 to 30 September 2026:
    DOT physicals with their certificates, recertifications after a short certificate, and FTA drug and alcohol
    tests. Each physical records the measured stature and weight."""
    rng = stream("encounters")
    start = dt.date(2014, 1, 1)
    out = []
    for p in people:
        if p["job"] not in JOBS_DOT:
            continue
        end = p["left"] or AS_OF
        first = p["hired"] - dt.timedelta(days=int(rng.uniform(6, 34)))
        if first >= start:
            d, kind = first, "pre"
            out.append({"emp": p["emp"], "date": first - dt.timedelta(days=int(rng.uniform(0, 3))), "type": "DRUG-PRE"})
        else:
            d, kind = start + dt.timedelta(days=int(rng.uniform(0, 700))), "renew"
        while d <= end:
            heavy = p["w"] > (110 if p["sex"] == "M" else 98)
            u = rng.random()
            short = p["bp_risk"] > 0.985 and u < 0.5
            months = 3 if short else (12 if (p["bp_risk"] > (0.80 if heavy else 0.90) or u < 0.04) else 24)
            out.append({"emp": p["emp"], "date": d, "type": "PHYS", "months": months, "pre": kind == "pre",
                        "s_true": p["s"], "w_true": true_weight(p, d)})
            if months == 3:
                rc = d + dt.timedelta(days=int(rng.uniform(70, 88)))
                if rc <= end:
                    out.append({"emp": p["emp"], "date": rc, "type": "RECERT", "months": 9, "of": d})
                nxt = d + dt.timedelta(days=365)
            else:
                nxt = d + dt.timedelta(days=int(months * 30.44))
            d = nxt - dt.timedelta(days=int(rng.uniform(0, 45)))
            kind = "renew"
        # random tests, quarterly draws at the FTA rates
        q = dt.date(max(start, p["hired"]).year, 3 * ((max(start, p["hired"]).month - 1) // 3) + 1, 1)
        while q <= end:
            if q >= start and q >= p["hired"]:
                if rng.random() < 0.125:
                    t = q + dt.timedelta(days=int(rng.uniform(0, 88)))
                    if t <= end:
                        out.append({"emp": p["emp"], "date": t, "type": "DRUG-RAND"})
                if rng.random() < 0.025:
                    t = q + dt.timedelta(days=int(rng.uniform(0, 88)))
                    if t <= end:
                        out.append({"emp": p["emp"], "date": t, "type": "ALC-RAND"})
            q = dt.date(q.year + (q.month + 3 > 12), (q.month + 2) % 12 + 1, 1)
        if rng.random() < 0.18:
            t = p["hired"] + dt.timedelta(days=int(rng.uniform(60, max(61, (end - p["hired"]).days))))
            if start <= t <= end:
                out.append({"emp": p["emp"], "date": t, "type": "DRUG-PA"})
    out = [e for e in out if e["date"] >= start and e["date"] <= AS_OF]
    # what each physical records: stature to the provider's precision, weight in pounds
    for e in out:
        if e["type"] != "PHYS":
            continue
        s_meas = e["s_true"] + rng.normal(0, 5.0)
        w_meas = e["w_true"] + rng.normal(0, 1.0)
        e["bp"] = (int(118 + 30 * rng.random() + 8 * (e["w_true"] > 105)), int(72 + 18 * rng.random()))
        # Ostrander measured stature to the inch, Fernhill to the half inch; both weigh to the pound
        e["h_in"] = (float(round(s_meas / IN_TO_MM)) if provider_of(e["date"]) == "old"
                     else round(s_meas / IN_TO_MM * 2) / 2)
        e["w_lb"] = int(round(w_meas / LB_TO_KG))
    out.sort(key=lambda e: (e["date"], e["emp"], e["type"]))
    return out


def provider_of(d):
    return "old" if d < CHANGEOVER else "new"


# ---------------------------------------------------------------- the fleet and its operator-area maintenance
# series: model year, fleet numbers, how many, accepted (first, last), options as built, disposed (first, last)
SERIES = [
    (2009, 901, 38, (dt.date(2009, 4, 6), dt.date(2009, 6, 26)), [], (dt.date(2019, 3, 18), dt.date(2021, 8, 30))),
    (2010, 1001, 36, (dt.date(2010, 3, 1), dt.date(2010, 5, 28)), ["P"], (dt.date(2020, 6, 8), dt.date(2022, 4, 25))),
    (2011, 1101, 32, (dt.date(2011, 3, 7), dt.date(2011, 5, 20)), ["P", "R"], (dt.date(2022, 2, 14), dt.date(2023, 5, 22))),
    (2012, 1201, 28, (dt.date(2012, 4, 2), dt.date(2012, 6, 15)), ["P", "R"], (dt.date(2023, 6, 12), dt.date(2024, 9, 16))),
    (2014, 1401, 60, (dt.date(2014, 2, 10), dt.date(2014, 6, 27)), [], None),
    (2015, 1501, 45, (dt.date(2015, 3, 9), dt.date(2015, 6, 5)), [], None),
    (2016, 1601, 40, (dt.date(2016, 2, 22), dt.date(2016, 5, 13)), [], None),
    (2017, 1701, 50, (dt.date(2017, 3, 6), dt.date(2017, 7, 14)), ["P"], None),
    (2018, 1801, 40, (dt.date(2018, 2, 26), dt.date(2018, 5, 25)), ["P"], None),
    (2019, 1901, 30, (dt.date(2019, 3, 11), dt.date(2019, 5, 31)), ["P", "R"], None),
    (2020, 2001, 35, (dt.date(2020, 2, 17), dt.date(2020, 6, 26)), ["P", "R"], None),
    (2021, 2101, 30, (dt.date(2021, 3, 8), dt.date(2021, 5, 28)), ["P", "R", "T"], None),
    (2022, 2201, 40, (dt.date(2022, 2, 28), dt.date(2022, 6, 17)), ["P", "R", "T"], None),
    (2023, 2301, 30, (dt.date(2023, 3, 13), dt.date(2023, 5, 26)), ["T", "V"], None),
    (2024, 1101, 32, (dt.date(2024, 2, 5), dt.date(2024, 4, 26)), ["P", "R", "T", "D"], None),
    (2025, 1201, 28, (dt.date(2025, 1, 13), dt.date(2025, 3, 28)), ["P", "R", "T", "D", "V"], None),
]
RETROFIT = ("24-03", "P", [(2014, 24), (2015, 20)], (dt.date(2024, 4, 15), dt.date(2024, 6, 21)))
WARRANTY_DAYS = 365
COMPONENTS = {  # code: description, option or None, repairs per bus-year, part lines (min, max)
    "PDL-ADJ": ("Pedal set, power adjust", "P", 0.36, (1, 4)),
    "SEAT-RSR": ("Seat riser, extended range", "R", 0.21, (1, 3)),
    "STR-TEL": ("Steering column, tilt-telescope", "T", 0.27, (1, 4)),
    "SEAT-TRK": ("Seat track, deep travel", "D", 0.31, (1, 3)),
    "HDR-VIS": ("Header visor and roller shade, raised", "V", 0.16, (1, 3)),
    "SEAT-CUSH": ("Operator seat cushion and cover", None, 0.92, (1, 3)),
    "SEAT-SUSP": ("Operator seat suspension", None, 0.41, (1, 4)),
    "SEAT-BELT": ("Operator seat belt", None, 0.22, (1, 2)),
    "MIRR-EXT": ("Mirror, exterior", None, 1.25, (1, 3)),
    "MIRR-INT": ("Mirror, interior and convex", None, 0.18, (1, 2)),
    "DRV-FAN": ("Operator fan and defroster", None, 0.33, (1, 3)),
    "DRV-BARR": ("Operator barrier door", None, 0.29, (1, 3)),
    "STR-WHL": ("Steering wheel and horn", None, 0.12, (1, 2)),
    "PDL-FIX": ("Pedal set, fixed", None, 0.15, (1, 2)),
    "SUN-SHD": ("Roller sun shade", None, 0.25, (1, 2)),
}
COMPONENT_PARTS = {  # part number stem, description, unit cost range
    "PDL-ADJ": [("PA-1180", "Pedal actuator motor", (240, 520)), ("PA-1192", "Position sensor", (85, 160)),
                ("PA-1210", "Drive cable", (40, 95)), ("PA-1305", "Switch, pedal adjust", (32, 70))],
    "SEAT-RSR": [("SR-220", "Riser lift cylinder", (180, 390)), ("SR-231", "Riser control valve", (60, 140)),
                 ("SR-245", "Riser bushing kit", (25, 60))],
    "STR-TEL": [("ST-4410", "Telescope lock actuator", (210, 460)), ("ST-4422", "Column tilt gas spring", (70, 150)),
                ("ST-4436", "Column release valve", (55, 120)), ("ST-4450", "Column boot", (20, 45))],
    "SEAT-TRK": [("TK-310", "Seat track rail assembly", (190, 410)), ("TK-318", "Track latch", (45, 105)),
                 ("TK-326", "Track roller kit", (30, 70))],
    "HDR-VIS": [("HV-610", "Visor motor", (150, 320)), ("HV-622", "Roller shade, raised", (65, 140)),
                ("HV-630", "Header trim panel", (35, 80))],
    "SEAT-CUSH": [("SC-101", "Seat cushion", (110, 230)), ("SC-115", "Back cushion", (95, 210)),
                  ("SC-130", "Seat cover", (45, 110))],
    "SEAT-SUSP": [("SS-501", "Air spring", (120, 260)), ("SS-512", "Shock absorber", (60, 135)),
                  ("SS-520", "Height valve", (55, 120)), ("SS-534", "Suspension bushing kit", (20, 50))],
    "SEAT-BELT": [("SB-700", "Belt retractor", (60, 140)), ("SB-712", "Buckle", (25, 55))],
    "MIRR-EXT": [("ME-800", "Mirror head", (140, 330)), ("ME-812", "Mirror glass", (30, 75)),
                 ("ME-825", "Mirror arm", (85, 190))],
    "MIRR-INT": [("MI-850", "Interior mirror", (30, 70)), ("MI-860", "Convex mirror", (25, 60))],
    "DRV-FAN": [("DF-900", "Fan motor", (55, 125)), ("DF-912", "Defroster blower", (110, 240)),
                ("DF-920", "Fan switch", (15, 35))],
    "DRV-BARR": [("DB-950", "Barrier door glass", (160, 340)), ("DB-962", "Barrier hinge", (35, 80)),
                 ("DB-975", "Barrier latch", (25, 60))],
    "STR-WHL": [("SW-150", "Steering wheel", (180, 360)), ("SW-162", "Horn switch", (20, 45))],
    "PDL-FIX": [("PF-1020", "Pedal pad", (15, 40)), ("PF-1031", "Accelerator sensor", (90, 190))],
    "SUN-SHD": [("SD-040", "Roller shade", (45, 105)), ("SD-052", "Shade bracket", (12, 30))],
}
LABOR_RATE = {2019: 61.50, 2020: 63.00, 2021: 64.25, 2022: 66.75, 2023: 69.40, 2024: 71.80, 2025: 73.60, 2026: 75.10}
MAINT_START = dt.date(2019, 1, 1)
ASK_YEARS = (2021, 2025)


def fleet():
    """Every bus in the Authority's fleet since 2019: fleet number, series, accepted, disposed, options as built,
    retrofits."""
    rng = stream("fleet")
    buses = []
    for year, first_no, n, (a0, a1), opts, disp in SERIES:
        accepted = sorted(a0 + dt.timedelta(days=int(rng.uniform(0, (a1 - a0).days))) for _ in range(n))
        if disp:
            gone = sorted(disp[0] + dt.timedelta(days=int(rng.uniform(0, (disp[1] - disp[0]).days))) for _ in range(n))
            order = rng.permutation(n)
        for k in range(n):
            buses.append({"no": first_no + k, "series": year, "accepted": accepted[k],
                          "disposed": gone[order[k]] if disp else None, "built": list(opts), "retrofit": {},
                          "serial": "HV%02d-%04d" % (year % 100, 310 + 37 * (year - 2011) + k * 3 + hint("ser", year, k) % 3),
                          "division": DIVISIONS[hint("busdiv", year, k) % 3]})
    code, opt, groups, (r0, r1) = RETROFIT
    for year, n in groups:
        pool = [b for b in buses if b["series"] == year]
        pick = sorted(rng.choice(len(pool), n, replace=False))
        for i in pick:
            pool[i]["retrofit"][opt] = r0 + dt.timedelta(days=int(rng.uniform(0, (r1 - r0).days)))
    return settle_fleet(buses)


def options_on(b, d):
    """The options a bus carried on a date."""
    out = list(b["built"])
    for o, when in b["retrofit"].items():
        if when <= d and o not in out:
            out.append(o)
    return out


def in_fleet(b, d):
    return b["accepted"] <= d and (b["disposed"] is None or d < b["disposed"])


def month_starts(y0, y1):
    return [dt.date(y, m, 1) for y in range(y0, y1 + 1) for m in range(1, 13)]


def option_months(buses, opt):
    """Months of the ask's years in which a bus was in the fleet and carried the option on the month's first day."""
    return sum(1 for b in buses for d in month_starts(*ASK_YEARS) if in_fleet(b, d) and opt in options_on(b, d))


def settle_fleet(buses):
    """Keep every option's bus-years off a half-tenth: a bus-month total of 3 or 9 past a whole year would put the
    one-decimal figure on a rounding edge, so the latest acceptance in a series carrying the option moves a month."""
    for _ in range(20):
        bad = [o for o in OPTION_ORDER if option_months(buses, o) % 12 in (3, 9)]
        if not bad:
            return buses
        o = bad[0]
        cands = sorted((b for b in buses if o in b["built"] and b["accepted"].year >= ASK_YEARS[0]),
                       key=lambda b: (len(b["built"]), -b["accepted"].toordinal(), b["no"]))
        b = cands[0]
        b["accepted"] = b["accepted"] + dt.timedelta(days=31)
    raise AssertionError("bus-years still on an edge")


def work_orders(buses):
    """Operator-area work orders opened from 1 January 2019, closed by 30 September 2026: one dict per order with its
    part lines. Labour is the order's; the export prints it on every line."""
    rng = stream("workorders")
    raw = []
    day0 = MAINT_START
    for b in buses:
        start = max(b["accepted"], day0)
        stop = min(b["disposed"] or AS_OF, AS_OF)
        if stop <= start:
            continue
        for comp, (desc, opt, rate, (l0, l1)) in COMPONENTS.items():
            # step through the bus's time in thirty-day blocks so retrofits start mid-life
            d = start
            while d < stop:
                nxt = min(stop, d + dt.timedelta(days=30))
                on = options_on(b, d)
                have = ("P" not in on) if comp == "PDL-FIX" else (opt is None or opt in on)
                if have:
                    lam = rate * (nxt - d).days / 365.25 * (1.0 + 0.04 * (d.year - b["series"]) if opt else 1.0)
                    for _ in range(rng.poisson(lam)):
                        opened = d + dt.timedelta(days=int(rng.uniform(0, max(1, (nxt - d).days))))
                        raw.append((opened, b, comp))
                d = nxt
    # retrofit installation orders, charged to the capital project
    for b in buses:
        for o, when in b["retrofit"].items():
            raw.append((when - dt.timedelta(days=int(rng.uniform(1, 4))), b, "PDL-ADJ*"))
    raw.sort(key=lambda r: (r[0], r[1]["no"], r[2]))
    orders = []
    seq = {}
    for opened, b, comp in raw:
        campaign = comp.endswith("*")
        comp = comp.rstrip("*")
        desc, opt, rate, (l0, l1) = COMPONENTS[comp]
        yr = opened.year
        seq[yr] = seq.get(yr, 0) + 1
        closed = opened + dt.timedelta(days=int(rng.choice([0, 0, 0, 1, 1, 2, 3, 5, 8, 13, 21])))
        if closed > AS_OF:
            continue
        nlines = int(rng.integers(l0, l1 + 1)) if not campaign else 4
        parts = COMPONENT_PARTS[comp]
        lines = []
        for j in range(nlines):
            pn, pdesc, (c0, c1) = parts[j % len(parts)] if campaign else parts[int(rng.integers(0, len(parts)))]
            qty = 1 if rng.random() < 0.85 else 2
            unit = round(float(rng.uniform(c0, c1)) * (1 + 0.025 * (yr - 2019)), 2)
            lines.append({"part": pn, "desc": pdesc, "qty": qty, "unit": unit})
        hours = round(float(rng.uniform(0.8, 3.6)) + 0.45 * (nlines - 1), 1) if not campaign else 6.5
        if campaign:
            bill = "CAPITAL PROJ 24-03"
            reason = "CAMPAIGN"
        elif opt and (opened - b["accepted"]).days < WARRANTY_DAYS:
            bill = "HALVARD WARRANTY" if rng.random() < 0.88 else "TVRTA"
            reason = "WARRANTY" if bill != "TVRTA" else "DEFECT"
        else:
            bill = "TVRTA"
            reason = str(rng.choice(["DEFECT", "DEFECT", "DEFECT", "OPERATOR REPORT", "PM FINDING", "DAMAGE"]))
        orders.append({"wo": "%02d-%05d" % (yr % 100, seq[yr]), "bus": b, "no": b["no"], "comp": comp,
                       "opened": opened, "closed": closed, "bill": bill, "reason": reason, "lines": lines,
                       "hours": hours, "rate": LABOR_RATE[closed.year]})
    return settle_costs(orders, buses)


def settle_costs(orders, buses):
    """Each option's cost per bus-year sits a few thousandths above a whole dollar, so a twelve-year figure built from
    the dollar-rounded rates and one built from the unrounded rates agree: the unit cost on the option's last
    Authority-billed line of the ask's years moves by the few dollars that takes."""
    for o in OPTION_ORDER:
        mine = [w for w in orders if COMPONENTS[w["comp"]][1] == o and w["bill"] == "TVRTA"
                and ASK_YEARS[0] <= w["closed"].year <= ASK_YEARS[1]]
        years = option_months(buses, o) / 12.0
        cost = sum(round(ln["qty"] * ln["unit"], 2) for w in mine for ln in w["lines"]) + \
            sum(round(w["hours"] * w["rate"], 2) for w in mine)
        lines = sorted(((w, ln) for w in mine if w["closed"].year == ASK_YEARS[1] for ln in w["lines"]),
                       key=lambda t: (-t[1]["unit"], t[0]["wo"], t[1]["part"]))
        ln = lines[0][1]
        whole = int(cost / years)
        best = None
        for n in (whole, whole + 1):
            target = round((n + 0.003) * years, 2)
            unit = round(ln["unit"] + (target - cost) / ln["qty"], 2)
            if unit >= 10 and (best is None or abs(target - cost) < best[0]):
                best = (abs(target - cost), unit)
        ln["unit"] = best[1]
    return orders


def off_the_first(buses):
    """No acceptance, disposal or fitting falls on a month's first day: one recorded on the 1st is recorded on the
    last day of the month before, which the bus-month rule counts the same way (in the fleet on the 1st after an
    acceptance, out of it after a disposal, carrying a fitting), so every reading of "on the first day" agrees. Run
    after the work orders, which it leaves as they are."""
    prev = lambda d: d - dt.timedelta(days=1) if d is not None and d.day == 1 else d
    for b in buses:
        b["accepted"] = prev(b["accepted"])
        b["disposed"] = prev(b["disposed"])
        b["retrofit"] = {o: prev(w) for o, w in b["retrofit"].items()}
    return buses


# ---------------------------------------------------------------- distractors
def comfort_survey(people):
    """The 2023 operator comfort survey: anonymous responses rating today's workstations by the series driven most."""
    rng = stream("comfort")
    ops = [p for p in people if p["job"] == "BUS OPERATOR" and p["hired"] <= dt.date(2023, 4, 1)
           and (p["left"] is None or p["left"] >= dt.date(2023, 5, 1))]
    n = int(len(ops) * 0.41)
    pick = rng.choice(len(ops), n, replace=False)
    series = [s[0] for s in SERIES if s[0] <= 2023 and (s[5] is None or s[5][1].year >= 2023)]
    out = []
    for k, i in enumerate(sorted(pick)):
        p = ops[i]
        sr = int(rng.choice(series))
        base = 3.3 + 0.12 * (sr >= 2019) + 0.15 * (sr >= 2021)
        out.append({"id": "R%04d" % (k + 1), "division": p.get("division") or DIVISIONS[hint("d", p["emp"]) % 3],
                    "years": min(30, max(0, int((dt.date(2023, 5, 1) - p["hired"]).days / 365.25))),
                    "series": sr,
                    "ratings": [int(np.clip(round(rng.normal(base + d, 0.95)), 1, 5)) for d in (0.0, -0.2, -0.35, 0.1, 0.05)],
                    "date": dt.date(2023, 5, 1) + dt.timedelta(days=int(rng.uniform(0, 26)))})
    return out


def comp_claims(people):
    """Workers' compensation claims of operators and transportation staff since 2019."""
    rng = stream("claims")
    staff = [p for p in people if p["job"] in ("BUS OPERATOR", "ROAD SUPERVISOR", "INSTRUCTOR - TRANSPORTATION")]
    out = []
    parts = [("LOWER BACK", 0.24), ("SHOULDER", 0.17), ("KNEE", 0.12), ("NECK", 0.09), ("WRIST/HAND", 0.11),
             ("HIP", 0.05), ("ANKLE/FOOT", 0.07), ("MULTIPLE", 0.08), ("HEAD", 0.03), ("PSYCHOLOGICAL", 0.04)]
    causes = ["SEATING / CAB", "BOARDING ASSAULT", "SLIP OR FALL", "VEHICLE COLLISION", "LIFTING (RAMP/SECUREMENT)",
              "REPETITIVE MOTION", "STRUCK BY OBJECT"]
    d = dt.date(2019, 1, 1)
    k = 0
    while d <= AS_OF:
        for _ in range(rng.poisson(14)):
            p = staff[int(rng.integers(0, len(staff)))]
            when = d + dt.timedelta(days=int(rng.uniform(0, 28)))
            if when < p["hired"] or (p["left"] and when > p["left"]) or when > AS_OF:
                continue
            k += 1
            bp = parts[int(np.searchsorted(np.cumsum([w for _, w in parts]), rng.random()))][0]
            paid = round(float(rng.lognormal(8.1, 1.25)), 2)
            out.append({"claim": "WC%02d-%04d" % (when.year % 100, k), "emp": p["emp"], "date": when, "job": p["job"],
                        "body": bp, "cause": str(rng.choice(causes)), "lost": int(max(0, rng.normal(9, 14))),
                        "paid": paid, "status": "CLOSED" if when < dt.date(2025, 6, 1) or rng.random() < 0.4 else "OPEN"})
        d += dt.timedelta(days=28)
    return out

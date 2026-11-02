"""The clean truth of task266, drawn once from the seed: every mesothelioma case the State's pre-1986 workforce and
its later and non-occupational neighbours produce, the register's window over them, each case's working life as
its interview records it, and the review program's members, bookings and the Mobile Review Unit's year as it
happened (where the unit was each day, what its card paid for, what its X-ray counter read)."""
import datetime as dt
import math

import numpy as np

import common as K

D0 = dt.date(1900, 1, 1)


def day(x):
    return D0 + dt.timedelta(days=int(x))


def ordinal(d):
    return (d - D0).days


def frac_year_to_day(y):
    """A decimal year (1965.37) to a day number."""
    yi = int(math.floor(y))
    start = ordinal(dt.date(yi, 1, 1))
    length = ordinal(dt.date(yi + 1, 1, 1)) - start
    return start + int((y - yi) * length)


# ------------------------------------------------------------------------------------------- occupations
# real ANZSCO unit groups and occupations, the codes the online interview form uses
EXPOSED_JOBS = [("399999", "Thermal insulation installer (lagger)", 9), ("322311", "Boilermaker", 8),
                ("323211", "Fitter (General)", 10), ("341111", "Electrician (General)", 7),
                ("331212", "Carpenter", 8), ("334111", "Plumber (General)", 7), ("399112", "Shipwright", 4),
                ("821111", "Builder's Labourer", 6), ("712911", "Power Station Operator", 4),
                ("321211", "Motor Mechanic (General)", 5), ("733112", "Railway Worker (rolling stock)", 3),
                ("721911", "Waterside Worker", 3), ("711999", "Asbestos cement products machinist", 6),
                ("332211", "Painter (trade)", 2), ("821711", "Construction Rigger", 2)]
OTHER_JOBS = [("841511", "Farm Hand", 5), ("591112", "Storeperson", 4), ("531111", "General Clerk", 5),
              ("733111", "Truck Driver (General)", 5), ("621111", "Sales Assistant (General)", 4),
              ("241213", "Primary School Teacher", 2), ("851111", "Cleaner", 3), ("431511", "Waiter", 2),
              ("839411", "Factory Hand", 4), ("711311", "Paper Products Machine Operator", 2),
              ("441211", "Police Officer", 1), ("252511", "Physiotherapist", 1), ("311111", "Agricultural Technician", 1),
              ("411411", "Enrolled Nurse", 2), ("599111", "Bookkeeper", 2)]
EMPLOYERS_EXPOSED = ["Port Ellery Harbour Trust dockyard", "Hawksmere Power Station", "Lindenvale Power Station",
                     "Carrowby Asbestos Cement Works", "State Railways workshops, Port Ellery",
                     "Coastal Lagging Co.", "Allard Bros. Builders", "Murrell Heads Shipbuilding Co.",
                     "Ellery Brake & Clutch", "Dorrabee Fibro Products", "Northern Boiler Services",
                     "Harbour Engineering Pty Ltd", "Garrock Sugar Mill", "Quillerton Smelter",
                     "Public Works Department (buildings)", "Westside Plumbing & Gas", "Ellery Insulation Services",
                     "Kellowie Timber & Hardware", "State Electricity Supply, maintenance", "Bay Shipping Agencies"]
EMPLOYERS_OTHER = ["Haskins Grazing Co.", "Ellery Retail Stores", "Dept of Education", "Ostlebury Shire Council",
                   "Bayview Transport", "Riverside Hospital", "Corrin Dairy Co-op", "Tarramore Bakery",
                   "State Police", "Pellandra Freight", "Murrell Paper Mill", "Ellery Hotels",
                   "Fenalong Orchards", "State Savings Bank branch", "Linden Textiles"]


# what each employer's people did (titles from EXPOSED_JOBS and OTHER_JOBS)
POOL = {
    "Port Ellery Harbour Trust dockyard": ["Shipwright", "Boilermaker", "Fitter (General)", "Thermal insulation installer (lagger)", "Construction Rigger", "Painter (trade)"],
    "Hawksmere Power Station": ["Power Station Operator", "Fitter (General)", "Electrician (General)", "Thermal insulation installer (lagger)", "Boilermaker"],
    "Lindenvale Power Station": ["Power Station Operator", "Fitter (General)", "Electrician (General)", "Thermal insulation installer (lagger)"],
    "Carrowby Asbestos Cement Works": ["Asbestos cement products machinist", "Builder's Labourer", "Fitter (General)"],
    "Dorrabee Fibro Products": ["Asbestos cement products machinist", "Builder's Labourer"],
    "State Railways workshops, Port Ellery": ["Railway Worker (rolling stock)", "Fitter (General)", "Boilermaker", "Painter (trade)"],
    "Coastal Lagging Co.": ["Thermal insulation installer (lagger)"],
    "Ellery Insulation Services": ["Thermal insulation installer (lagger)", "Builder's Labourer"],
    "Allard Bros. Builders": ["Carpenter", "Builder's Labourer", "Plumber (General)", "Electrician (General)"],
    "Public Works Department (buildings)": ["Carpenter", "Plumber (General)", "Electrician (General)", "Builder's Labourer", "Thermal insulation installer (lagger)"],
    "Murrell Heads Shipbuilding Co.": ["Shipwright", "Boilermaker", "Fitter (General)", "Thermal insulation installer (lagger)", "Construction Rigger"],
    "Ellery Brake & Clutch": ["Motor Mechanic (General)"],
    "Northern Boiler Services": ["Boilermaker", "Thermal insulation installer (lagger)", "Fitter (General)"],
    "Harbour Engineering Pty Ltd": ["Fitter (General)", "Boilermaker"],
    "Garrock Sugar Mill": ["Fitter (General)", "Boilermaker", "Builder's Labourer"],
    "Quillerton Smelter": ["Fitter (General)", "Electrician (General)", "Builder's Labourer"],
    "Westside Plumbing & Gas": ["Plumber (General)"],
    "Kellowie Timber & Hardware": ["Carpenter", "Builder's Labourer"],
    "State Electricity Supply, maintenance": ["Electrician (General)", "Fitter (General)"],
    "Bay Shipping Agencies": ["Waterside Worker"],
    "Haskins Grazing Co.": ["Farm Hand", "Truck Driver (General)"], "Ellery Retail Stores": ["Sales Assistant (General)", "Storeperson"],
    "Dept of Education": ["Primary School Teacher"], "Ostlebury Shire Council": ["General Clerk", "Truck Driver (General)", "Cleaner"],
    "Bayview Transport": ["Truck Driver (General)", "Storeperson"], "Riverside Hospital": ["Enrolled Nurse", "Cleaner", "Physiotherapist"],
    "Corrin Dairy Co-op": ["Factory Hand", "Truck Driver (General)"], "Tarramore Bakery": ["Factory Hand", "Sales Assistant (General)"],
    "State Police": ["Police Officer"], "Pellandra Freight": ["Truck Driver (General)", "Storeperson"],
    "Murrell Paper Mill": ["Paper Products Machine Operator", "Factory Hand"], "Ellery Hotels": ["Waiter", "Cleaner"],
    "Fenalong Orchards": ["Farm Hand", "Agricultural Technician"], "State Savings Bank branch": ["General Clerk", "Bookkeeper"],
    "Linden Textiles": ["Factory Hand"]}
TITLE = {o[1]: o for o in EXPOSED_JOBS + OTHER_JOBS}


def _job(rng, exposed):
    """An employer and what the worker did there."""
    emps = EMPLOYERS_EXPOSED if exposed else EMPLOYERS_OTHER
    emp = emps[int(rng.integers(len(emps)))]
    pool = POOL[emp]
    return emp, TITLE[pool[int(rng.integers(len(pool)))]]


def _pick(rng, items):
    w = np.array([x[-1] for x in items], dtype=float)
    return items[int(rng.choice(len(items), p=w / w.sum()))]


def _workplace_code(rng, name, codes):
    if name not in codes:
        while True:
            c = "WP%04d" % int(rng.integers(1000, 9999))
            if c not in codes.values():
                codes[name] = c
                break
    return codes[name]


def _spells(rng, dob, first_exposed, last_day, exposed_case, codes):
    """A working life as the interview lists it: spells of work from leaving school to retirement or the last day
    the worker could report, with first_exposed the first day of the earliest exposed spell (None: no exposed
    spell). Returns a list of dicts in date order."""
    out = []
    leave_school = dob + int((15.2 + rng.random() * 3.5) * K.YEAR)
    retire = dob + int((58 + rng.random() * 9) * K.YEAR)
    if first_exposed is not None:
        retire = max(retire, first_exposed + 400 + int(rng.integers(0, 900)))
    stop = min(retire, last_day)
    t = leave_school
    if exposed_case:
        # spells before first exposure, none exposed
        while first_exposed - t > 400:
            dur = int(rng.uniform(0.6, 6.0) * K.YEAR)
            end = min(t + dur, first_exposed - int(rng.integers(5, 90)))
            if end - t < 120:
                break
            emp, occ = _job(rng, False)
            out.append(dict(start=t, end=end, occ=occ, employer=emp, exposed=False))
            t = end + int(rng.integers(1, 120))
        t = first_exposed
        first = True
        while t < stop - 200:
            dur = int(rng.uniform(0.8, 14.0) * K.YEAR)
            end = min(t + dur, stop)
            exp = first or rng.random() < 0.55
            emp, occ = _job(rng, exp)
            out.append(dict(start=t, end=end, occ=occ, employer=emp, exposed=exp))
            first = False
            t = end + int(rng.integers(1, 200))
        # a concurrent second job now and then (weekend work, a second employer on the same site)
        if len(out) > 1 and rng.random() < 0.12:
            base = out[int(rng.integers(len(out)))]
            if base["end"] - base["start"] > 800:
                s = base["start"] + int(rng.integers(100, base["end"] - base["start"] - 300))
                if s > first_exposed:
                    e = min(s + int(rng.integers(120, 900)), base["end"])
                    emp, occ = _job(rng, False)
                    out.append(dict(start=s, end=e, occ=occ, employer=emp, exposed=False))
    else:
        while t < stop - 200:
            dur = int(rng.uniform(0.8, 16.0) * K.YEAR)
            end = min(t + dur, stop)
            emp, occ = _job(rng, False)
            out.append(dict(start=t, end=end, occ=occ, employer=emp, exposed=False))
            t = end + int(rng.integers(1, 200))
    out.sort(key=lambda s: (s["start"], s["end"]))
    for s in out:
        s["workplace"] = s["employer"]
        s["wp_code"] = _workplace_code(rng, s["employer"], codes)
    return out


# ------------------------------------------------------------------------------------------- the cases
N_COHORT = 8600          # the pre-1986 workforce's mesotheliomas, whenever diagnosed
N_LATER = 1500           # the 1986 to 2002 workforce's, whenever diagnosed
LAT_MEDIAN, LAT_SIGMA = 44.0, 0.21


def _first_exposures(rng, n):
    """First days at exposed work for the pre-1986 workforce's mesotheliomas: a wartime and post-war group from
    1940 and the post-war boom's building, power and asbestos-cement trades peaking in the early 1970s."""
    out = []
    for _ in range(n):
        r = rng.random()
        if r < 0.012:
            y = 1940 + rng.random() * 6
        elif r < 0.14:
            y = 1946 + rng.random() * 11
        else:
            while True:
                y = 1972.0 + 6.5 * rng.standard_normal()
                if 1957.0 <= y < 1986.0:
                    break
        out.append(frac_year_to_day(y))
    return np.array(out)


def cases(seed):
    rng = np.random.default_rng([seed, 1])
    S, C = ordinal(K.REG_START), ordinal(K.REG_END)
    out = []
    E = _first_exposures(rng, N_COHORT)
    T = np.round(np.exp(np.log(LAT_MEDIAN) + LAT_SIGMA * rng.standard_normal(N_COHORT)) * K.YEAR).astype(int)
    edges = {int(H * K.YEAR) for H in K.SETTINGS if float(H * K.YEAR).is_integer()}
    T = np.array([t + 1 if t in edges else t for t in T])
    for e, t in zip(E, T):
        out.append(dict(kind="cohort", E=int(e), T=int(t), D=int(e + t), category="Occupational"))
    # the later workforce (first exposed 1986 to 2002), far fewer and far lighter
    yrs = np.arange(1986, 2003)
    w = np.exp(-(yrs - 1986) / 5.0)
    w /= w.sum()
    El = np.array([frac_year_to_day(int(rng.choice(yrs, p=w)) + rng.random()) for _ in range(N_LATER)])
    Tl = np.round(np.exp(np.log(LAT_MEDIAN) + LAT_SIGMA * rng.standard_normal(N_LATER)) * K.YEAR).astype(int)
    for e, t in zip(El, Tl):
        out.append(dict(kind="later", E=int(e), T=int(t), D=int(e + t), category="Occupational"))
    reg = [c for c in out if S <= c["D"] <= C]
    # non-occupational cases on the register: household and environmental exposure, and none identified
    n_reg = len(reg)
    for kind, cat, share in (("domestic", "Domestic", 0.052), ("environmental", "Environmental", 0.021),
                             ("none", "No exposure identified", 0.074)):
        for _ in range(int(round(n_reg * share))):
            d = int(rng.integers(S, C + 1))
            reg.append(dict(kind=kind, E=None, T=None, D=d, category=cat))
    # identities, birth dates, histories, the register's own fields
    codes = {}
    for c in reg:
        male = rng.random() < (0.93 if c["kind"] in ("cohort", "later") else 0.42)
        c["sex"] = "Male" if male else "Female"
        if c["E"] is not None:
            age_e = 15.5 + rng.gamma(2.2, 4.2)
            c["dob"] = int(c["E"] - age_e * K.YEAR)
        else:
            age_d = 52 + rng.gamma(6.0, 4.0)
            c["dob"] = int(c["D"] - age_d * K.YEAR)
        c["spells"] = _spells(rng, c["dob"], c["E"], c["D"], c["E"] is not None, codes)
        c["notified"] = c["D"] + 3 + (int(rng.integers(3, 85)) - 3) * 57 // 82      # notified within 60 days
        c["interview"] = c["notified"] + 4 + (int(rng.integers(4, 58)) - 4) * 26 // 54   # interviewed within 30 days
        c["site"] = str(rng.choice(["Pleura", "Peritoneum", "Pericardium"], p=[0.928, 0.064, 0.008]))
        c["histology"] = str(rng.choice(["Epithelioid", "Biphasic", "Sarcomatoid", "Not otherwise specified"],
                                        p=[0.58, 0.21, 0.12, 0.09]))
        c["basis"] = str(rng.choice(["Histology", "Cytology", "Clinical and imaging"], p=[0.84, 0.11, 0.05]))
        surv = int(rng.gamma(1.3, 290))
        dd = c["D"] + surv
        c["death"] = dd if dd <= ordinal(K.REG_CLOSE) else None
        c["claim"] = str(rng.choice(["Accepted", "Declined", "No claim lodged", "Withdrawn"],
                                    p=[0.71, 0.06, 0.19, 0.04] if c["kind"] in ("cohort", "later") else [0.32, 0.18, 0.46, 0.04]))
        c["hospital"] = str(rng.choice(HOSPITALS, p=HOSP_P))
    reg.sort(key=lambda c: (c["notified"], c["D"]))
    # the Fund's case references: legacy system DD/yy/nnnn with gaps, current DDyy-nnnnn
    used = set()
    for c in reg:
        nd = day(c["notified"])
        while True:
            if nd <= K.LEGACY_END:
                ref = "DD/%02d/%04d" % (nd.year % 100, int(rng.integers(1, 9999)))
            else:
                ref = "DD%02d-%05d" % (nd.year % 100, int(rng.integers(10000, 99999)))
            if ref not in used:
                used.add(ref)
                break
        c["ref"] = ref
        c["hist_ref"] = ref.replace("DD/", "DD").replace("/", "-") if "/" in ref else ref
        c["notif_no"] = "N%07d" % int(rng.integers(1000000, 9999999))
    return dict(cases=out, register=reg, workplace_codes=codes)


HOSPITALS = ["Port Ellery Hospital", "Royal Ellery Infirmary", "Hawksmere Base Hospital", "Carrowby Hospital",
             "Lindenvale Hospital", "Murrell Heads Hospital", "St Columba's Private Hospital", "Bayside Private",
             "Ellery Heart & Lung Institute"]
HOSP_P = [0.21, 0.18, 0.13, 0.08, 0.09, 0.06, 0.09, 0.07, 0.09]


# ------------------------------------------------------------------------------------------- the program
def _home_town(rng):
    r = rng.random()
    if r < 0.70:
        return str(rng.choice(list(K.CITIES), p=[0.46, 0.17, 0.13, 0.14, 0.10]))
    if r < 0.905:
        w = np.array([CIRCUIT_W[t] for t in K.CIRCUIT], dtype=float)
        return str(rng.choice(list(K.CIRCUIT), p=w / w.sum()))
    return str(rng.choice(list(K.WAYPOINTS)))


# the circuit towns differ in size, so their visits differ in bookings
CIRCUIT_W = {"Quillerton": 1.7, "Tarramore": 0.9, "Dorrabee": 1.4, "Kellowie": 1.1, "Haskesford": 0.8,
             "Brinalong": 1.5, "Lathardine": 0.7, "Wennobank": 0.6, "Corrinbar": 1.0, "Fenalong": 0.9,
             "Strathowie": 1.2, "Pellandra": 1.0, "Garrock": 0.75, "Ostlebury": 0.8}


def members(seed):
    """The program's members as at 30 June 2026: living former workers first exposed before 1986."""
    rng = np.random.default_rng([seed, 2])
    out = []
    used = set()
    n = 9860
    for i in range(n):
        while True:
            y = 1971.5 + 7.5 * rng.standard_normal()
            if 1948.0 <= y < 1986.0:
                break
        e = frac_year_to_day(y)
        if (ordinal(K.TERM_START) - e) in {int(H * K.YEAR) for H in K.ASK_SETTINGS if float(H * K.YEAR).is_integer()}:
            e -= 1
        age_e = 15.5 + rng.gamma(2.0, 3.6)
        dob = int(e - age_e * K.YEAR)
        while True:
            no = "%06d%s" % (int(rng.integers(100000, 999999)), "ABCDEFGHJKLMNPRSTUVWXY"[int(rng.integers(22))])
            if no not in used:
                used.add(no)
                break
        enrolled = max(ordinal(dt.date(2005, 3, 1)), e + int((20 + rng.random() * 25) * K.YEAR))
        enrolled = min(enrolled, ordinal(dt.date(2025, 4, 30)))
        enrolled = int(enrolled + rng.integers(0, 400))
        enrolled = min(enrolled, ordinal(dt.date(2025, 5, 30)))
        status = str(rng.choice(["Active", "Withdrawn", "Deceased", "Moved interstate"], p=[0.885, 0.04, 0.06, 0.015]))
        out.append(dict(no=no, sex="Male" if rng.random() < 0.94 else "Female", dob=dob, E=e,
                        town=_home_town(rng), enrolled=enrolled, status=status,
                        status_date=None if status == "Active" else int(rng.integers(ordinal(dt.date(2023, 7, 1)),
                                                                                    ordinal(dt.date(2026, 6, 30))))))
    return out


# the unit's visits in 2025-26 as published (first day, days, town, venue); the year as it happened swaps four
# pairs of visits and runs two stretches of days with its tablet offline
VENUES = {"Quillerton": "Quillerton Showground pavilion", "Tarramore": "Tarramore Memorial Hall car park",
          "Dorrabee": "Dorrabee Hospital car park", "Kellowie": "Kellowie Bowling Club",
          "Haskesford": "Haskesford Multi-Purpose Health Service", "Brinalong": "Brinalong Community Centre",
          "Lathardine": "Lathardine Racecourse", "Wennobank": "Wennobank Shire depot",
          "Corrinbar": "Corrinbar RSL car park", "Fenalong": "Fenalong Health Clinic",
          "Strathowie": "Strathowie Town Hall", "Pellandra": "Pellandra Medical Centre",
          "Garrock": "Garrock Sports Ground", "Ostlebury": "Ostlebury Hospital car park"}
VISITS = [("2025-07-14", 3, "Corrinbar"), ("2025-07-28", 3, "Quillerton"), ("2025-08-11", 3, "Brinalong"),
          ("2025-08-25", 3, "Tarramore"), ("2025-09-08", 3, "Haskesford"), ("2025-09-15", 2, "Wennobank"),
          ("2025-09-22", 3, "Fenalong"), ("2025-10-13", 3, "Garrock"), ("2025-10-27", 3, "Kellowie"),
          ("2025-11-10", 3, "Lathardine"), ("2025-11-24", 3, "Dorrabee"), ("2025-12-08", 2, "Ostlebury"),
          ("2026-01-19", 3, "Pellandra"), ("2026-02-02", 3, "Strathowie"), ("2026-02-16", 3, "Dorrabee"),
          ("2026-03-02", 3, "Lathardine"), ("2026-03-16", 3, "Corrinbar"), ("2026-03-30", 3, "Tarramore"),
          ("2026-04-13", 3, "Strathowie"), ("2026-04-20", 2, "Pellandra"), ("2026-04-27", 3, "Ostlebury"),
          ("2026-05-11", 3, "Kellowie"), ("2026-05-25", 3, "Garrock"), ("2026-06-08", 3, "Quillerton"),
          ("2026-06-22", 3, "Haskesford"), ("2025-10-06", 2, "Wennobank"), ("2026-01-12", 2, "Fenalong"),
          ("2026-06-15", 2, "Brinalong")]
# published visit pairs the unit swapped (the earlier visit's days went to the later visit's town and back)
SWAPS = [("2025-07-14", "2025-07-28"),   # Corrinbar and Quillerton: the Corrinbar venue double-booked
         ("2025-08-11", "2025-08-25"),   # Brinalong and Tarramore: the Brinalong centre taken for the pre-poll
         ("2025-10-13", "2025-10-27"),   # Garrock and Kellowie: the Garrock sports ground resurfaced
         ("2026-02-16", "2026-03-02")]   # Dorrabee and Lathardine: the northern road under water
OFFLINE = [(dt.date(2025, 9, 8), dt.date(2025, 9, 26)), (dt.date(2026, 4, 13), dt.date(2026, 5, 1))]


def unit_year(seed):
    """The 2025-26 visits as published and as worked: each visit's days, the town the unit stood in each day."""
    pub = []
    for first, n, town in VISITS:
        d0 = dt.date.fromisoformat(first)
        days = []
        d = d0
        while len(days) < n:
            if d.weekday() < 5:
                days.append(d)
            d += dt.timedelta(days=1)
        pub.append(dict(first=d0, days=days, town=town, venue=VENUES[town], code=None))
    pub.sort(key=lambda v: v["first"])
    by_first = {v["first"].isoformat(): v for v in pub}
    for v in pub:
        v["actual"] = v["town"]
    for a, b in SWAPS:
        va, vb = by_first[a], by_first[b]
        va["actual"], vb["actual"] = vb["town"], va["town"]
    for v in pub:
        v["offline"] = any(lo <= v["first"] <= hi for lo, hi in OFFLINE)
        v["code"] = "MRU %s %s" % (v["town"].upper()[:10], v["first"].strftime("%d%b%y").upper())
    return pub


# ------------------------------------------------------------------------------------------- bookings
def _nearest_site(town):
    """A member's review site: the fixed clinic in their city, the unit in a circuit town, else the nearer of the
    nearest clinic city and the nearest circuit town by road."""
    if town in K.CITIES:
        return [c for c, (t, _) in K.CLINIC_SITES.items() if t == town][0], town
    if town in K.CIRCUIT:
        return K.UNIT_SITE, town
    best = min(list(K.CITIES) + list(K.CIRCUIT), key=lambda t: K.road_km(town, t))
    if best in K.CITIES:
        return [c for c, (t, _) in K.CLINIC_SITES.items() if t == best][0], best
    return K.UNIT_SITE, best


def _weekdays(lo, hi):
    out, d = [], lo
    while d <= hi:
        if d.weekday() < 5:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def _earlier_unit_visits(fy_start):
    """The unit's visits in an earlier program year, the same circuit a year (or two) back."""
    shift = (K.FY_START - fy_start).days
    out = []
    for first, n, town in VISITS:
        d0 = dt.date.fromisoformat(first) - dt.timedelta(days=shift)
        while d0.weekday() != 0:
            d0 += dt.timedelta(days=1)
        days = _weekdays(d0, d0 + dt.timedelta(days=6))[:n]
        out.append(dict(first=d0, days=days, town=town, actual=town, offline=False))
    return out


SLOT_TIMES = ["08:30", "08:50", "09:10", "09:30", "09:50", "10:10", "10:30", "10:50", "11:10", "11:30", "11:50",
              "13:10", "13:30", "13:50", "14:10", "14:30", "14:50", "15:10", "15:30", "15:50", "16:10"]
CLINIC_DNA_RECORDED = {"PEH", "HWK"}       # the two clinics whose clerks close their lists with DNA


def bookings(seed, mem, unit):
    """Every booking from July 2023 to June 2026, one review a program year per active member, with the outcome
    the booking system holds."""
    rng = np.random.default_rng([seed, 3])
    rows = []
    used = set()

    def new_id():
        while True:
            a = "BK%07d" % int(rng.integers(1000000, 9999999))
            if a not in used:
                used.add(a)
                return a

    years = [(dt.date(2023, 7, 1), dt.date(2024, 6, 30)), (dt.date(2024, 7, 1), dt.date(2025, 6, 30)),
             (K.FY_START, K.FY_END)]
    for fy_lo, fy_hi in years:
        visits = unit if fy_lo == K.FY_START else _earlier_unit_visits(fy_lo)
        by_town = {}
        for v in visits:
            by_town.setdefault(v["town"], []).append(v)
        clinic_days = _weekdays(fy_lo, fy_hi)
        for m in mem:
            if ordinal(fy_hi) < m["enrolled"]:
                continue
            if m["status"] != "Active" and m["status_date"] is not None and m["status_date"] < ordinal(fy_lo):
                continue
            site, town = _nearest_site(m["town"])
            if rng.random() < 0.035:      # some members are not booked in a year (away, unwell)
                continue
            if site == K.UNIT_SITE:
                vv = by_town[town]
                v = vv[int(rng.integers(len(vv)))]
                d = v["days"][int(rng.integers(len(v["days"])))]
                visit = v
            else:
                d = clinic_days[int(rng.integers(len(clinic_days)))]
                visit = None
            if m["status_date"] is not None and m["status"] in ("Deceased", "Withdrawn", "Moved interstate") \
                    and ordinal(d) > m["status_date"]:
                continue
            slots = SLOT_TIMES
            if visit is not None and visit["first"].isoformat() in MORNING_RUN and d == visit["days"][0]:
                slots = [x for x in SLOT_TIMES if x >= MORNING_OPEN]
            t = slots[int(rng.integers(len(slots)))]
            booked_on = d - dt.timedelta(days=int(rng.integers(21, 70)))
            r = rng.random()
            outcome = "attended" if r < 0.862 else ("dna" if r < 0.952 else "cancelled")
            row = dict(id=new_id(), member=m["no"], site=site, date=d, time=t, booked=booked_on,
                       review="Chest X-ray and spirometry" if rng.random() < 0.81 else "Low-dose CT and spirometry",
                       outcome=outcome, visit=visit, town=town if site == K.UNIT_SITE else None)
            if outcome == "cancelled" and rng.random() < 0.6:
                # the member rebooked: the first booking closed as Rebooked, a later booking made
                row["outcome"] = "rebooked"
                rows.append(row)
                if site == K.UNIT_SITE:
                    later = [w for w in by_town[town] if w["first"] > d]
                    if not later:
                        continue
                    v2 = later[0]
                    d2 = v2["days"][int(rng.integers(len(v2["days"])))]
                else:
                    later = [x for x in clinic_days if x > d + dt.timedelta(days=10)]
                    if not later:
                        continue
                    d2 = later[int(rng.integers(min(len(later), 40)))]
                    v2 = None
                r2 = rng.random()
                row2 = dict(id=new_id(), member=m["no"], site=site, date=d2, time=SLOT_TIMES[int(rng.integers(len(SLOT_TIMES)))],
                            booked=d + dt.timedelta(days=int(rng.integers(-6, 0))), review=row["review"],
                            outcome="attended" if r2 < 0.9 else "dna", visit=v2, town=row["town"])
                rows.append(row2)
            else:
                rows.append(row)
    # the swapped visits: each booking on a swapped visit's days was moved, in place, to the other visit's days
    swap_of = {}
    for a, b in SWAPS:
        va = [v for v in unit if v["first"].isoformat() == a][0]
        vb = [v for v in unit if v["first"].isoformat() == b][0]
        swap_of[id(va)] = vb
        swap_of[id(vb)] = va
    for row in rows:
        v = row["visit"]
        if v is not None and id(v) in swap_of:
            other = swap_of[id(v)]
            k = v["days"].index(row["date"]) if row["date"] in v["days"] else 0
            row["date"] = other["days"][min(k, len(other["days"]) - 1)]
            row["worked_visit"] = other           # the published visit whose days it now sits on
        elif v is not None:
            row["worked_visit"] = v
    # every working day of the unit has its handful of no-shows
    per_day = {}
    for row in rows:
        if row["site"] == K.UNIT_SITE and K.FY_START <= row["date"] <= K.FY_END:
            per_day.setdefault(row["date"], []).append(row)
    for d in sorted(per_day):
        rr = per_day[d]
        dna = [x for x in rr if x["outcome"] == "dna"]
        att = [x for x in rr if x["outcome"] == "attended"]
        need = 3 + int(rng.integers(0, 2)) - len(dna)
        for x in att[:max(0, need)]:
            x["outcome"] = "dna"
    # a unit day's list runs from its first slot to its last
    for d in sorted(per_day):
        att = sorted([x for x in per_day[d] if x["outcome"] == "attended"], key=lambda x: x["time"])
        v = att[0].get("worked_visit") if att else None
        open_ = MORNING_OPEN if (v is not None and v["first"].isoformat() in MORNING_RUN and d == v["days"][0]) else "08:30"
        if len(att) >= 2:
            att[0]["time"] = open_
            att[-1]["time"] = "16:10"
    # what the booking system holds: Attended, DNA, Cancelled, Rebooked or blank
    for row in rows:
        o = row["outcome"]
        wv = row.get("worked_visit")
        offline = wv is not None and wv["offline"]
        if o == "attended":
            if offline and rng.random() < 0.74:
                row["status"] = ""              # checked in on the tablet with no signal: the replay carried no status
            else:
                row["status"] = "Attended"
        elif o == "dna":
            if row["site"] == K.UNIT_SITE:
                row["status"] = "DNA" if offline else ""
            else:
                row["status"] = "DNA" if row["site"] in CLINIC_DNA_RECORDED else ""
        elif o == "cancelled":
            row["status"] = "Cancelled"
        else:
            row["status"] = "Rebooked"
    rows.sort(key=lambda r: (r["date"], r["site"], r["time"], r["id"]))
    return rows


# ------------------------------------------------------------------------------------------- the unit's year
# each place's motels: (name, the two room rates the crew pays)
MOTEL = {"Quillerton": [("Quillerton Motor Inn", 159.0, 172.5), ("Showground Motel Quillerton", 138.0, 146.0)],
         "Tarramore": [("Tarramore Hotel", 119.0, 131.0)], "Dorrabee": [("Dorrabee Motor Lodge", 148.0, 158.9)],
         "Kellowie": [("Kellowie Country Motel", 134.5, 141.0)], "Haskesford": [("Haskesford Motel", 127.0, 136.0)],
         "Brinalong": [("Brinalong Motor Inn", 144.0, 155.0), ("Lakeside Cabins Brinalong", 112.5, 118.0)],
         "Lathardine": [("Lathardine Commercial Hotel", 115.0, 129.5)], "Wennobank": [("Wennobank Motel", 124.0, 131.0)],
         "Corrinbar": [("Corrinbar Motor Inn", 139.0, 149.5)], "Fenalong": [("Fenalong Motel", 128.0, 137.9)],
         "Strathowie": [("Strathowie Motor Lodge", 146.0, 154.0)], "Pellandra": [("Pellandra Motel", 131.5, 139.0)],
         "Garrock": [("Garrock Hotel Motel", 121.0, 129.0)], "Ostlebury": [("Ostlebury Motor Inn", 137.0, 145.5)],
         "Sallow Creek": [("Sallow Creek Roadhouse Units", 104.0, 109.5)], "Mallin Junction": [("Junction Motel", 108.0, 116.0)],
         "Ferngate Gap": [("Ferngate Gap Hotel", 99.0, 104.0)], "Bellwether Ridge": [("Bellwether Ridge Motel", 112.0, 119.5)],
         "Thornbush Flat": [("Thornbush Flat Hotel", 94.5, 99.0)], "Saltbush Flat": [("Saltbush Flat Cabins", 118.0, 126.0)],
         "Pellandra Beach": [("Beachfront Motel Pellandra", 152.0, 161.0)],
         "Kellowie Heights": [("Heights Motor Inn", 129.0, 137.0)], "Ostlebury Point": [("Point Caravan Park Cabins", 98.0, 104.5)],
         "Fenalong Bridge": [("Bridge Hotel Fenalong", 108.5, 114.0)], "Carrowby": [("Carrowby Central Motel", 141.0, 149.0)],
         "Lindenvale": [("Lindenvale Motor Lodge", 139.5, 147.0)], "Murrell Heads": [("Heads Motel", 136.0, 144.0)],
         "Port Ellery": [("Ellery City Motor Inn", 165.0, 179.0)]}
FUEL = {t: n for t, n in [("Hawksmere", "Ampol Hawksmere North"), ("Quillerton", "Quillerton Fuel Depot"),
                         ("Tarramore", "Tarramore Roadhouse"), ("Dorrabee", "BP Dorrabee"), ("Kellowie", "Kellowie Fuels"),
                         ("Haskesford", "United Haskesford"), ("Brinalong", "Brinalong Service Centre"),
                         ("Lathardine", "Lathardine Rural Supplies"), ("Wennobank", "Wennobank Truck Stop"),
                         ("Corrinbar", "Shell Corrinbar"), ("Fenalong", "Fenalong Fuel & Mechanical"),
                         ("Strathowie", "Strathowie Puma"), ("Pellandra", "Pellandra Fuel Stop"),
                         ("Garrock", "Garrock General Store & Fuel"), ("Ostlebury", "Liberty Ostlebury"),
                         ("Mallin Junction", "Mallin Junction Roadhouse"), ("Ferngate Gap", "Ferngate Gap Store"),
                         ("Thornbush Flat", "Thornbush Flat Fuel"), ("Bellwether Ridge", "Bellwether Ridge Roadhouse"),
                         ("Sallow Creek", "Sallow Creek Roadhouse"), ("Port Ellery", "Ampol Port Ellery"),
                         ("Carrowby", "BP Carrowby"), ("Lindenvale", "Shell Lindenvale"), ("Murrell Heads", "Puma Murrell Heads")]}
# where the crew buys food: (merchant, category, low, high); a town's own places and the chains every town has
FOOD = {"Quillerton": [("Main St Bakery Quillerton", "Meals", 9, 34), ("The Grain Store Cafe", "Meals", 18, 52),
                       ("Royal Hotel Quillerton", "Meals", 34, 88)],
        "Tarramore": [("Tarramore Bakehouse", "Meals", 8, 31), ("Tarramore Hotel bistro", "Meals", 31, 79)],
        "Dorrabee": [("Dorrabee Hospital Kiosk", "Meals", 7, 23), ("Bean There Dorrabee", "Meals", 14, 41)],
        "Kellowie": [("Kellowie Bowling Club Bistro", "Meals", 26, 74), ("Kellowie Bakery", "Meals", 8, 29)],
        "Haskesford": [("Haskesford Cafe", "Meals", 15, 44), ("Haskesford Hotel", "Meals", 30, 82)],
        "Brinalong": [("Brinalong Newsagency & Cafe", "Meals", 11, 36), ("Lake St Bakery", "Meals", 8, 30),
                      ("Brinalong Chinese Restaurant", "Meals", 36, 92)],
        "Lathardine": [("Lathardine Racecourse Kiosk", "Meals", 6, 21), ("Railway Hotel Lathardine", "Meals", 29, 77)],
        "Wennobank": [("Wennobank Bakery", "Meals", 9, 28), ("Wennobank Hotel", "Meals", 28, 70)],
        "Corrinbar": [("Corrinbar RSL Club", "Meals", 24, 69), ("Corrinbar Pie Shop", "Meals", 9, 27),
                      ("Thai on Main Corrinbar", "Meals", 31, 84)],
        "Fenalong": [("Fenalong Fruit Barn Cafe", "Meals", 13, 39), ("Fenalong Hotel", "Meals", 30, 76)],
        "Strathowie": [("Strathowie Hall Cafe", "Meals", 12, 38), ("Federal Hotel Strathowie", "Meals", 33, 85)],
        "Pellandra": [("Pellandra Bakery", "Meals", 8, 31), ("Pellandra Fish & Chips", "Meals", 22, 58)],
        "Garrock": [("Garrock Corner Store", "Meals", 7, 26), ("Garrock Hotel", "Meals", 27, 71)],
        "Ostlebury": [("Ostlebury Cafe", "Meals", 14, 41), ("Ostlebury Pizza", "Meals", 24, 62)]}
MORNING_WORDS = ("Bakery", "Bakehouse", "Cafe", "Kiosk", "Pie", "Bean")
EVENING_WORDS = ("Hotel", "Bistro", "Club", "Restaurant", "Pizza", "Fish", "Thai", "Chinese")


def food_places(place, when):
    """Where the crew could buy something at place at a time of day: (merchant, category, low, high)."""
    own = FOOD.get(place, [])
    if when == "morning":
        out = [f for f in own if any(w in f[0] for w in MORNING_WORDS)]
        out += [("%s Bakery" % place, "Meals", 7, 24), ("%s Newsagency" % place, "Shop", 4, 19)]
    elif when == "midday":
        out = list(own) + [("IGA %s" % place, "Shop", 9, 46), ("%s Bakery" % place, "Meals", 8, 27)]
    elif when == "afternoon":
        out = [("%s Newsagency" % place, "Shop", 4, 31), ("%s Pharmacy" % place, "Shop", 7, 48),
               ("IGA %s" % place, "Shop", 6, 52)]
    else:
        out = [f for f in own if any(w in f[0] for w in EVENING_WORDS)]
        out += [("%s Takeaway" % place, "Meals", 19, 57), ("IGA %s" % place, "Shop", 14, 96),
                ("Foodworks %s" % place, "Shop", 12, 81)]
    return out


# visits whose crew stayed out of the town (its motels full): the visit's first day -> where the crew slept
STAY_ELSEWHERE = {"2025-11-10": "Saltbush Flat", "2026-01-19": "Pellandra Beach", "2026-05-11": "Kellowie Heights",
                  "2025-12-08": "Ostlebury Point", "2026-01-12": "Fenalong Bridge"}
# visits the unit drove to on their first morning, refuelling on the way and opening late in the morning
MORNING_RUN = {"2026-03-16": "Hawksmere", "2026-06-08": "Sallow Creek", "2026-06-15": "Hawksmere",
               "2026-03-30": "Hawksmere"}
MORNING_OPEN = "11:30"


def _via(a, b):
    """The waypoint on the road from a to b that adds the least distance, or None if none is on the way."""
    best, extra = None, 1e9
    for w in K.WAYPOINTS:
        x = K.road_km(a, w) + K.road_km(w, b) - K.road_km(a, b)
        if x < extra:
            best, extra = w, x
    return best if extra < 0.18 * K.road_km(a, b) else None


def _halfway(a, b):
    """The town nearest halfway on the road from a to b, for an overnight on a long run."""
    total = K.road_km(a, b)
    cands = [p for p in list(K.CITIES) + list(K.CIRCUIT) + list(K.WAYPOINTS)
             if p not in (a, b) and K.road_km(a, p) + K.road_km(p, b) <= total * 1.04]
    return min(cands, key=lambda p: abs(K.road_km(a, p) - total / 2.0)) if cands else None


SPEED = 76.0      # the unit's average on the road, km/h
LONG_DAY = 9.5    # hours at the wheel beyond which the run is split over two days


def _hm(t):
    return "%02d:%02d" % (t // 60, t % 60)


def unit_operations(seed, unit, rows):
    """The unit's year as it happened: where it was each day, every card transaction and every QA log row."""
    rng = np.random.default_rng([seed, 4])
    food = np.random.default_rng([seed, 5])
    card, qa, where = [], [], {}
    st = dict(odo=412680 + int(rng.integers(0, 900)), tank=260.0, loc=K.UNIT_BASE)
    cap, burn = 300.0, 0.29                # litres; litres per km
    swapped = {d for a_, b_ in SWAPS for v in unit if v["first"].isoformat() in (a_, b_) for d in v["days"]}

    def buy(place, t):
        litres = round(cap - st["tank"] - float(rng.uniform(2, 9)), 2)
        price = round(float(rng.uniform(1.89, 2.21)), 3)
        card.append(dict(t=t, merchant=FUEL.get(place, place + " Fuel"), location=place, category="Fuel",
                         litres=litres, odo=st["odo"], amount=round(litres * price, 2)))
        st["tank"] = st["tank"] + litres

    def drive(to, leave, fuel_at=None):
        """Drive from where the unit is to `to`, leaving at `leave`; refuel at a waypoint on the way when low (or
        at fuel_at, a place on the way, if given). Returns the arrival time."""
        a = st["loc"]
        mid = fuel_at or _via(a, to)
        legs = [(mid, K.road_km(a, mid)), (to, K.road_km(mid, to))] if mid and mid != a else [(to, K.road_km(a, to))]
        t = leave
        if fuel_at == a:
            buy(a, t + dt.timedelta(minutes=int(rng.integers(4, 15))))
            t += dt.timedelta(minutes=25)
        for place, k in legs:
            if st["tank"] - k * burn < 0.15 * cap:
                buy(st["loc"], t + dt.timedelta(minutes=int(rng.integers(2, 9))))
                t += dt.timedelta(minutes=25)
            t += dt.timedelta(minutes=int(k / SPEED * 60))
            st["odo"] += k
            st["tank"] -= k * burn
            if place != to and (fuel_at == place or st["tank"] < 0.45 * cap):
                buy(place, t + dt.timedelta(minutes=int(rng.integers(3, 12))))
                t += dt.timedelta(minutes=25)
            st["loc"] = place
        return t

    def spend(place, day, lo, hi, when):
        """One food or shop purchase at place, at a minute between lo and hi (minutes after midnight)."""
        opts = food_places(place, when)
        name, cat, l, h = opts[int(food.integers(len(opts)))]
        t = dt.datetime.combine(day, dt.time(0, 0)) + dt.timedelta(minutes=int(food.integers(lo, hi)))
        amt = round(float(food.uniform(l, h)) * (1.0 if food.random() < 0.7 else 1.6), 2)
        card.append(dict(t=t, merchant=name, location=place, category=cat, litres=None, odo=None, amount=amt))

    def motel(place, nights, when):
        opts = MOTEL.get(place, [(place + " Motel", 118.0, 126.0)])
        name, r1, r2 = opts[0] if food.random() < 0.75 else opts[-1]
        extras = sum(round(float(food.choice([0.0, 0.0, 18.5, 24.0, 37.0, 12.0])), 2) for _ in range(nights))
        card.append(dict(t=when, merchant=name, location=place, category="Accommodation", litres=None, odo=None,
                         amount=round(nights * (r1 + r2) + extras, 2)))

    def overland(to, start_day, depart_min):
        """A long run split at the town nearest halfway, with a night there; returns the run's last day."""
        half = _halfway(st["loc"], to)
        if half is None or K.road_km(st["loc"], to) / SPEED <= LONG_DAY:
            drive(to, dt.datetime.combine(start_day, dt.time(0, 0)) + dt.timedelta(minutes=depart_min))
            return start_day
        drive(half, dt.datetime.combine(start_day, dt.time(7, 5 + int(rng.integers(0, 40)))))
        if food.random() < 0.6:
            spend(half, start_day, 18 * 60 + 5, 20 * 60 + 30, "evening")
        nxt = start_day + dt.timedelta(days=1)
        motel(half, 1, dt.datetime.combine(nxt, dt.time(6, 5 + int(food.integers(0, 30)))))
        drive(to, dt.datetime.combine(nxt, dt.time(6, 40 + int(rng.integers(0, 19)))))
        return nxt

    reviews_on = {}
    for r in rows:
        if r["site"] == K.UNIT_SITE and K.FY_START <= r["date"] <= K.FY_END:
            reviews_on.setdefault(r["date"], []).append(r)
    for v in sorted(unit, key=lambda x: x["first"]):
        town = v["actual"]
        key = v["first"].isoformat()
        stay = STAY_ELSEWHERE.get(key, town)
        first, last = v["days"][0], v["days"][-1]
        hours = K.road_km(st["loc"], stay) / SPEED
        if key in MORNING_RUN:
            drive(town, dt.datetime.combine(first, dt.time(5, 35)), fuel_at=MORNING_RUN[key])
            arrive_night = first
        else:
            eve = first - dt.timedelta(days=1)
            if hours > LONG_DAY:
                overland(stay, eve - dt.timedelta(days=1), 7 * 60)
            else:
                dep = max(6 * 60 + 20, int(18.5 * 60 - hours * 60))
                drive(stay, dt.datetime.combine(eve, dt.time(0, 0)) + dt.timedelta(minutes=dep - dep % 5))
            arrive_night = eve
            if st["tank"] < 0.55 * cap:
                buy(stay, dt.datetime.combine(eve, dt.time(18, 35 + int(rng.integers(0, 20)))))
            if food.random() < 0.5:
                spend(stay, eve, 18 * 60 + 15, 20 * 60 + 40, "evening")
        far = K.road_km(town, K.UNIT_BASE) > 320
        for i, d in enumerate(v["days"]):
            where[d] = town
            if stay != town:
                k = 2 * K.road_km(stay, town)
                st["odo"] += k
                st["tank"] -= k * burn
            st["loc"] = town
            if food.random() < 0.3:
                spend(stay, d, 6 * 60 + 40, 8 * 60 + 12, "morning")
            if d in swapped or food.random() < 0.78:
                spend(town, d, 11 * 60 + 35, 13 * 60 + 55, "midday")
            if food.random() < 0.12:
                spend(town, d, 14 * 60 + 25, 16 * 60 + 20, "afternoon")
            if i < len(v["days"]) - 1 and st["tank"] < 0.4 * cap:
                buy(town, dt.datetime.combine(d, dt.time(16, 40 + int(rng.integers(0, 15)))))
            if (i < len(v["days"]) - 1 or far) and food.random() < 0.55:
                spend(stay, d, 17 * 60 + 20, 20 * 60 + 40, "evening")
        # home after the last day: the same afternoon from a near town, the next morning from a far one
        if far:
            checkout = last + dt.timedelta(days=1)
            ck = dt.datetime.combine(checkout, dt.time(6, 2 + int(rng.integers(0, 25))))
            st["loc"] = stay
        else:
            checkout = last
            ck = dt.datetime.combine(last, dt.time(7, 2 + int(rng.integers(0, 25))))
        nights = (checkout - arrive_night).days
        if nights > 0:
            motel(stay, nights, ck)
        if far:
            overland(K.UNIT_BASE, checkout, 6 * 60 + 40)
        else:
            drive(K.UNIT_BASE, dt.datetime.combine(last, dt.time(16, 55)))
        st["loc"] = K.UNIT_BASE
        # the X-ray QA log: one row per working day
        for d in v["days"]:
            day_rows = reviews_on.get(d, [])
            reviewed = sum(1 for r in day_rows if r["outcome"] == "attended")
            retakes = int(rng.binomial(reviewed, 0.045))
            tests = 2 if rng.random() < 0.8 else 3
            start = (qa[-1]["end"] if qa else 184212) + int(rng.integers(0, 3))
            end = start + 2 * reviewed + retakes + tests
            qa.append(dict(date=d, start=start, end=end, tests=tests, reviewed=reviewed, retakes=retakes,
                           op=str(rng.choice(["JM", "RK", "JM", "TS"]))))
    for d in _weekdays(K.FY_START, K.FY_END):
        if d not in where and rng.random() < 0.05:
            card.append(dict(t=dt.datetime.combine(d, dt.time(9, 0)) + dt.timedelta(minutes=int(rng.integers(0, 420))),
                             merchant="Hawksmere Truck Wash", location="Hawksmere", category="Vehicle",
                             litres=None, odo=None, amount=round(float(rng.uniform(55, 95)), 2)))
    card.sort(key=lambda c: c["t"])
    return dict(card=card, qa=qa, where=where)


def build(seed=K.SEED):
    T = cases(seed)
    T["members"] = members(seed)
    T["unit"] = unit_year(seed)
    T["bookings"] = bookings(seed, T["members"], T["unit"])
    T.update(unit_operations(seed, T["unit"], T["bookings"]))
    return T

"""The clean truth behind task482's pack (architecture 15): Pembrook Castings Company's self-insured dental plan for
its employees and their families, administered by Ridgeline Benefit Administrators, January 2024 to September 2026.

Every person, coverage span, dental service, predetermination, adjudicated claim line, adjustment and orthodontic case
is generated forward from the parameters below with fixed seeds. A covered person's claims in a plan year are
adjudicated in the order they arrive against the plan's deductible, coinsurance and 1,500 dollar annual maximum. A
dentist sends a predetermination before most major work; a member whose estimate shows the maximum cutting the payment
puts the cut work off to the next plan year more often than not, and has it done after the January reset when they
still want it. The pack (pack.py) cuts Ridgeline's two adjudication platforms' extracts, its predetermination log,
accumulators, eligibility, crosswalk, fee schedules and orthodontic schedule from this truth; the golden (golden.py)
reads only the pack.

Money is held in integer cents throughout."""
import datetime as dt
import math
import random

SEED = 482150
D = dt.date
START = D(2024, 1, 1)
MIGRATION = D(2025, 7, 1)          # Ridgeline moves the plan from its legacy platform to the new one
SERVICE_END = D(2026, 9, 30)
EXTRACT = D(2026, 10, 9)           # both extracts carry lines adjudicated through this date
YEARS = (2024, 2025, 2026)
WARM = 2023                        # the plan year before the extracts, simulated for what it carries into 2024

MAXIMUM = 150000                   # cents, per covered person per plan year (calendar year)
DEDUCTIBLE = 5000                  # cents, per covered person per plan year, Class II and III
COINS = {1: 100, 2: 80, 3: 50}
OPTIONS = (150000, 200000, 300000)  # the current maximum, the company's counter and the union's proposal
LIMIT = 190                        # cents per covered person month, the bargaining mandate's allowance
ORTHO_LIFETIME = 150000
ORTHO_COINS = 50

COMPANY = "Pembrook Castings Company"
TPA = "Ridgeline Benefit Administrators"
PEOPLE = dict(benefits="Audrey Bautista", tpa="Marvin Jordan", finance="Barry Rowland")

# code: (description, class, 2024 network fee in dollars, tooth kind); fees rise each 1 January (FEE_STEP_RANGE)
PROCS = {
    "D0120": ("Periodic oral evaluation", 1, 44, None),
    "D0150": ("Comprehensive oral evaluation", 1, 74, None),
    "D0140": ("Limited oral evaluation, problem focused", 1, 58, None),
    "D0272": ("Bitewings, two radiographic images", 1, 41, None),
    "D0274": ("Bitewings, four radiographic images", 1, 58, None),
    "D0330": ("Panoramic radiographic image", 1, 92, None),
    "D1110": ("Prophylaxis, adult", 1, 82, None),
    "D1120": ("Prophylaxis, child", 1, 60, None),
    "D1206": ("Topical application of fluoride varnish", 1, 29, None),
    "D1351": ("Sealant, per tooth", 1, 39, "molar"),
    "D2140": ("Amalgam, one surface", 2, 102, "post"),
    "D2150": ("Amalgam, two surfaces", 2, 127, "post"),
    "D2330": ("Resin-based composite, one surface, anterior", 2, 121, "ant"),
    "D2331": ("Resin-based composite, two surfaces, anterior", 2, 146, "ant"),
    "D2391": ("Resin-based composite, one surface, posterior", 2, 132, "post"),
    "D2392": ("Resin-based composite, two surfaces, posterior", 2, 166, "post"),
    "D2393": ("Resin-based composite, three surfaces, posterior", 2, 201, "post"),
    "D7140": ("Extraction, erupted tooth", 2, 121, "any"),
    "D7210": ("Extraction, erupted tooth requiring removal of bone", 2, 205, "any"),
    "D3310": ("Endodontic therapy, anterior tooth", 2, 668, "ant"),
    "D3320": ("Endodontic therapy, premolar tooth", 2, 772, "pre"),
    "D3330": ("Endodontic therapy, molar tooth", 2, 935, "molar"),
    "D4341": ("Periodontal scaling and root planing, four or more teeth per quadrant", 2, 204, None),
    "D4910": ("Periodontal maintenance", 2, 117, None),
    "D9110": ("Palliative treatment of dental pain", 2, 83, None),
    "D2740": ("Crown, porcelain/ceramic", 3, 1032, "any"),
    "D2750": ("Crown, porcelain fused to high noble metal", 3, 985, "any"),
    "D2790": ("Crown, full cast high noble metal", 3, 1018, "post"),
    "D2950": ("Core buildup, including any pins when required", 3, 219, "any"),
    "D6240": ("Pontic, porcelain fused to high noble metal", 3, 958, "any"),
    "D6750": ("Retainer crown, porcelain fused to high noble metal", 3, 985, "any"),
    "D6010": ("Surgical placement of implant body, endosteal", 3, 1795, "any"),
    "D6057": ("Custom fabricated abutment", 3, 605, "any"),
    "D6058": ("Abutment supported porcelain/ceramic crown", 3, 1118, "any"),
    "D5110": ("Complete denture, maxillary", 3, 1415, None),
    "D5213": ("Maxillary partial denture, cast metal framework", 3, 1505, None),
}
ORTHO_CODES = {"D8080": "Comprehensive orthodontic treatment of the adolescent dentition",
               "D8670": "Periodic orthodontic treatment visit"}
FEE_STEP_RANGE = {2025: (0.022, 0.036), 2026: (0.024, 0.040), 2027: (0.028, 0.046)}
# the 2027 schedule as Ridgeline published it: the two most billed codes landed a dollar or two off their stepped fee
FEE_2027_ADJ = {"D0120": 0, "D1110": 1, "D0274": 10, "D2740": 3}

# behaviour at a cut estimate: the chance a member puts the cut work off to the next plan year, and the chance work
# put off is done after the January reset
DEFER = {"crown": 0.62, "bridge": 0.80, "implant": 0.90, "denture": 0.72, "endo": 0.12, "perio": 0.34}
PROCEED = {"crown": 0.82, "bridge": 0.76, "implant": 0.76, "denture": 0.68, "endo": 0.86, "perio": 0.62}
PREDET_SHARE = {"crown": 0.86, "bridge": 0.9, "implant": 0.92, "denture": 0.88, "endo": 0.55, "perio": 0.5}
ADJUST_SHARE = 0.026
FREQ_DENIAL_SHARE = 0.018

TEETH_ANT = [6, 7, 8, 9, 10, 11, 22, 23, 24, 25, 26, 27]
TEETH_PRE = [4, 5, 12, 13, 20, 21, 28, 29]
TEETH_MOLAR = [2, 3, 14, 15, 18, 19, 30, 31]
TEETH_POST = TEETH_PRE + TEETH_MOLAR


def rng(*k):
    return random.Random("|".join(str(x) for x in (SEED,) + k))


def month_end(d):
    nxt = D(d.year + (d.month == 12), d.month % 12 + 1, 1)
    return nxt - dt.timedelta(days=1)


def add_months(d, n):
    m = d.month - 1 + n
    y = d.year + m // 12
    m = m % 12 + 1
    return D(y, m, min(d.day, month_end(D(y, m, 1)).day))


def poisson(r, lam):
    u, acc = r.random(), 0.0
    for k in range(12):
        acc += math.exp(-lam) * lam ** k / math.factorial(k)
        if u <= acc:
            return k
    return 12


# ---------------------------------------------------------------------------------------------------------- fees
def fee_schedules():
    """{year: {code: cents}} for 2024 to 2027; every fee a whole dollar."""
    out = {2024: {c: v[2] * 100 for c, v in PROCS.items()}}
    for y in (2025, 2026, 2027):
        lo, hi = FEE_STEP_RANGE[y]
        out[y] = {}
        for c in PROCS:
            r = rng("fee", c, y)
            out[y][c] = int(round(out[y - 1][c] / 100.0 * (1 + r.uniform(lo, hi)))) * 100
    for c, adj in FEE_2027_ADJ.items():
        out[2027][c] += adj * 100
    return out


FEES = fee_schedules()


def plan_class(code):
    return PROCS[code][1]


# --------------------------------------------------------------------------------------------- business calendar
def observed(d):
    if d.weekday() == 5:
        return d - dt.timedelta(days=1)
    if d.weekday() == 6:
        return d + dt.timedelta(days=1)
    return d


def nth_weekday(y, m, wd, n):
    d = D(y, m, 1)
    while d.weekday() != wd:
        d += dt.timedelta(days=1)
    return d + dt.timedelta(days=7 * (n - 1))


def last_weekday(y, m, wd):
    d = month_end(D(y, m, 1))
    while d.weekday() != wd:
        d -= dt.timedelta(days=1)
    return d


def tpa_holidays(y):
    """Ridgeline's observed holidays (its service agreement's Schedule C): New Year's Day, Memorial Day, Independence
    Day, Labor Day, Thanksgiving and the day after, Christmas Eve and Christmas Day (weekend dates observed on the
    nearest weekday)."""
    th = nth_weekday(y, 11, 3, 4)
    days = [observed(D(y, 1, 1)), last_weekday(y, 5, 0), observed(D(y, 7, 4)), nth_weekday(y, 9, 0, 1), th,
            th + dt.timedelta(days=1)]
    xmas = D(y, 12, 25)
    if xmas.weekday() == 5:
        days += [xmas - dt.timedelta(days=2), xmas - dt.timedelta(days=1)]
    elif xmas.weekday() == 6:
        days += [xmas - dt.timedelta(days=2), xmas + dt.timedelta(days=1)]
    elif xmas.weekday() == 0:
        days += [xmas - dt.timedelta(days=3), xmas]
    else:
        days += [xmas - dt.timedelta(days=1), xmas]
    return sorted(set(days))


HOLIDAYS = sorted(set(d for y in (2023, 2024, 2025, 2026, 2027) for d in tpa_holidays(y)))
HOLIDAY_SET = set(HOLIDAYS)


def is_business(d):
    return d.weekday() < 5 and d not in HOLIDAY_SET


def next_business(d):
    while not is_business(d):
        d += dt.timedelta(days=1)
    return d


def add_business(d, n):
    d = next_business(d)
    for _ in range(n):
        d += dt.timedelta(days=1)
        d = next_business(d)
    return d


def business_between(a, b):
    """Business days after a up to and including b."""
    n, d = 0, a
    while d < b:
        d += dt.timedelta(days=1)
        if is_business(d):
            n += 1
    return n


def central_offset(t):
    """UTC offset of America/Chicago (hours) at local time t, US rules since 2007."""
    y = t.year
    start = dt.datetime.combine(nth_weekday(y, 3, 6, 2), dt.time(2, 0))
    end = dt.datetime.combine(nth_weekday(y, 11, 6, 1), dt.time(2, 0))
    return -5 if start <= t < end else -6


def to_utc(local):
    return local - dt.timedelta(hours=central_offset(local))


def receipt_day(local):
    """The service agreement's receipt rule: a request received after 5:00 p.m. Central time, or on a day that is not
    a business day, is received on the next business day."""
    d = local.date()
    if not is_business(d) or local.time() >= dt.time(17, 0):
        return next_business(d + dt.timedelta(days=1))
    return d


# ------------------------------------------------------------------------------------------------------- people
def build_people():
    """Employees with their spouses and children: identity, birth, sex and coverage spans (start, end or None)."""
    r = rng("people")
    people = []
    eno = 41000

    def add(kind, emp, dob, sex, start, end):
        people.append(dict(pid=len(people), kind=kind, emp=emp, dob=dob, sex=sex, start=start, end=end))
        return people[-1]["pid"]

    n_start = 2240
    for i in range(n_start + 690):
        eno += r.randint(1, 3)
        if i < n_start:
            cov_start = START
        else:
            hire = START + dt.timedelta(days=r.randint(0, (D(2026, 8, 31) - START).days))
            cov_start = D(hire.year + (hire.month == 12), hire.month % 12 + 1, 1)
            if cov_start > D(2026, 9, 1):
                continue
        age = r.choice([r.randint(19, 34), r.randint(28, 50), r.randint(35, 64), r.randint(22, 62)])
        dob = cov_start - dt.timedelta(days=int(age * 365.25) + r.randint(0, 364))
        sex = "M" if r.random() < 0.74 else "F"
        end = None
        if r.random() < 0.20:
            t = cov_start + dt.timedelta(days=r.randint(120, 1300))
            if t <= D(2026, 9, 30):
                end = month_end(t)
        if r.random() > 0.93:          # waives dental coverage
            continue
        add("E", eno, dob, sex, cov_start, end)
        tier = r.random()
        if tier < 0.56 and age >= 21:
            sdob = dob + dt.timedelta(days=r.randint(-2200, 1800))
            s_end = end
            if end is None and r.random() < 0.025:
                s_end = month_end(cov_start + dt.timedelta(days=r.randint(200, 900)))
                if s_end > D(2026, 9, 30):
                    s_end = None
            add("S", eno, sdob, "F" if sex == "M" else "M", cov_start, s_end)
        if tier < 0.70 and 23 <= age <= 58:
            for k in range(r.choice([1, 1, 2, 2, 2, 3, 3, 4])):
                kage = max(0, min(25, age - r.randint(22, 38)))
                kdob = cov_start - dt.timedelta(days=int(kage * 365.25) + r.randint(0, 364))
                out26 = month_end(D(kdob.year + 26, kdob.month, 1))
                k_end = end
                if out26 < (k_end or D(2099, 1, 1)):
                    if out26 < cov_start:
                        continue
                    k_end = out26
                if k_end is not None and k_end > D(2026, 9, 30):
                    k_end = None
                add("C", eno, kdob, r.choice("MF"), cov_start, k_end)
        if tier < 0.62 and 24 <= age <= 42 and r.random() < 0.10:
            b = cov_start + dt.timedelta(days=r.randint(30, 900))
            if b <= D(2026, 8, 31) and (end is None or b < end):
                add("C", eno, b, r.choice("MF"), D(b.year, b.month, 1), end)
    return people


def coverage_in_year(p, y):
    a = max(p["start"], D(y, 1, 1))
    b = min(p["end"] or D(2099, 1, 1), D(y, 12, 31), SERVICE_END)
    return (a, b) if a <= b else None


def covered(p, d):
    return p["start"] <= d and (p["end"] is None or d <= p["end"])


def member_months(p, y):
    cov = coverage_in_year(p, y)
    if not cov:
        return 0
    a, b = cov
    return (b.year - a.year) * 12 + b.month - a.month + 1


def age_on(p, d):
    return d.year - p["dob"].year - ((d.month, d.day) < (p["dob"].month, p["dob"].day))


# ------------------------------------------------------------------------------------------------------ services
def clinic_day(r, d):
    """Dental offices see patients Monday to Friday and some Saturday mornings, never on a holiday."""
    while True:
        if d.weekday() == 6 or d in HOLIDAY_SET or (d.weekday() == 5 and r.random() < 0.8):
            d += dt.timedelta(days=1)
            continue
        return d


def _day_in(r, a, b):
    d = clinic_day(r, a + dt.timedelta(days=r.randint(0, max(0, (b - a).days))))
    return d if d <= b else clinic_day(r, a)


def _pick_tooth(r, kind, used):
    pool = {"ant": TEETH_ANT, "pre": TEETH_PRE, "molar": TEETH_MOLAR, "post": TEETH_POST,
            "any": TEETH_ANT + TEETH_POST}[kind]
    free = [t for t in pool if t not in used]
    t = r.choice(free or pool)
    used.add(t)
    return t


def needs(p, y):
    """The person's dental needs in plan year y: treatments, each a dict with a date, a kind and its lines
    [(code, tooth)]; a major treatment carries its parts (a crown and its buildup, a bridge's units, an implant's
    stage)."""
    cov = coverage_in_year(p, y)
    if not cov:
        return []
    a, b = cov
    span = (b - a).days + 1
    frac = span / 365.0
    r = rng("needs", p["pid"], y)
    age = age_on(p, D(y, 7, 1))
    child = age < 19
    out = []
    used = set()

    def treat(kind, date, lines):
        out.append(dict(kind=kind, date=date, lines=lines))

    if age >= 1 and r.random() < (0.86 if child else 0.73):
        first = _day_in(r, a, min(b, a + dt.timedelta(days=max(10, span // 2))))
        dates = [first]
        if r.random() < 0.8 * min(1.0, frac * 1.15):
            second = clinic_day(r, first + dt.timedelta(days=r.randint(150, 210)))
            if second <= b:
                dates.append(second)
        new_pt = r.random() < 0.05
        for k, d in enumerate(dates):
            lines = [("D0150" if new_pt and k == 0 else "D0120", None), ("D1120" if child else "D1110", None)]
            if k == 0:
                if child and age >= 4:
                    lines.append(("D0272", None))
                elif not child and r.random() < 0.78:
                    lines.append(("D0274", None))
                if not child and r.random() < 0.16:
                    lines.append(("D0330", None))
            if child and r.random() < 0.82:
                lines.append(("D1206", None))
            if child and 6 <= age <= 14 and k == 0 and r.random() < 0.22:
                for _ in range(r.choice([2, 2, 4])):
                    lines.append(("D1351", _pick_tooth(r, "molar", used)))
            treat("prev", d, lines)
        if r.random() < FREQ_DENIAL_SHARE:
            # a third cleaning with a new dentist, past the plan's two a year
            treat("extra", _day_in(r, a, b), [("D0150", None), ("D1120" if child else "D1110", None)])
    for _ in range(poisson(r, (0.34 if child else 0.52) * frac)):
        d = _day_in(r, a, b)
        if r.random() < 0.72:
            treat("fill", d, [(r.choice(["D2391", "D2392", "D2392", "D2393", "D2140", "D2150"]),
                               _pick_tooth(r, "post", used))])
        else:
            treat("fill", d, [(r.choice(["D2330", "D2331"]), _pick_tooth(r, "ant", used))])
    if not child and r.random() < 0.05 * frac:
        treat("ext", _day_in(r, a, b), [(r.choice(["D7140", "D7140", "D7210"]), _pick_tooth(r, "any", used))])
    if r.random() < 0.025 * frac:
        treat("pall", _day_in(r, a, b), [("D9110", None)])
    if child:
        return out
    crown_teeth = []
    if r.random() < (0.030 if age < 35 else 0.050 if age < 50 else 0.065) * frac:
        tk = r.choice(["ant", "pre", "molar", "molar"])
        tooth = _pick_tooth(r, tk, used)
        d = _day_in(r, a, b)
        treat("endo", d, [({"ant": "D3310", "pre": "D3320", "molar": "D3330"}[tk], tooth)])
        if r.random() < 0.82:
            crown_teeth.append((tooth, clinic_day(r, d + dt.timedelta(days=r.randint(21, 75))), True))
    if age >= 33 and r.random() < 0.055 * frac:
        d = _day_in(r, a, b)
        treat("perio", d, [("D4341", q) for q in (1, 2, 3, 4)][:r.choice([2, 2, 3, 4, 4])])
        for k in range(r.choice([1, 2, 2])):
            dm = clinic_day(r, d + dt.timedelta(days=90 * (k + 1) + r.randint(-10, 10)))
            if dm <= b:
                treat("pmaint", dm, [("D4910", None)])
    elif age >= 40 and r.random() < 0.07 * frac:
        for k in range(r.choice([2, 3, 3, 4])):
            dm = clinic_day(r, a + dt.timedelta(days=int(span * (k + 0.5) / 4)))
            if dm <= b:
                treat("pmaint", dm, [("D4910", None)])
    nc = poisson(r, (0.08 if age < 35 else 0.18 if age < 50 else 0.30 if age < 65 else 0.38) * frac)
    if nc >= 2 and r.random() < 0.7:
        d0 = _day_in(r, a, b)
        for k in range(nc):
            crown_teeth.append((_pick_tooth(r, "any", used),
                                clinic_day(r, d0 + dt.timedelta(days=0 if k < 2 else r.randint(14, 40))), False))
    else:
        for _ in range(nc):
            crown_teeth.append((_pick_tooth(r, "any", used), _day_in(r, a, b), False))
    groups = {}
    for tooth, d, after_endo in crown_teeth:
        lines = [(r.choice(["D2740", "D2740", "D2740", "D2750", "D2750", "D2790"]), tooth)]
        if after_endo or r.random() < 0.34:
            lines.insert(0, ("D2950", tooth))
        groups.setdefault(d, []).extend(lines)
    for d in sorted(groups):
        if d <= min(b, D(y, 12, 31)):
            treat("crown", d, groups[d])
    if age >= 38 and r.random() < 0.012 * frac:
        t1 = r.choice([3, 4, 5, 12, 13, 14, 19, 20, 21, 28, 29, 30])
        treat("bridge", _day_in(r, a, b), [("D6750", t1 - 1), ("D6240", t1), ("D6750", t1 + 1)])
    if age >= 38 and r.random() < 0.060 * frac:
        tooth = _pick_tooth(r, "any", used)
        d = _day_in(r, a, b)
        treat("implant", d, [("D6010", tooth)])
        d2 = clinic_day(r, d + dt.timedelta(days=r.randint(95, 150)))
        if d2 <= min(b, D(y, 12, 31)):
            treat("implant", d2, [("D6057", tooth), ("D6058", tooth)])
    if age >= 52 and r.random() < 0.007 * frac:
        treat("denture", _day_in(r, a, b), [(r.choice(["D5110", "D5213"]), None)])
    if age >= 44 and r.random() < 0.009 * frac:
        # a restorative plan of several crowns, estimated together and placed over two or three sittings
        d0 = _day_in(r, a, b - dt.timedelta(days=min(60, span // 3)))
        teeth = [_pick_tooth(r, "any", used) for _ in range(r.choice([4, 5, 6]))]
        for k in range(0, len(teeth), 2):
            dk = clinic_day(r, d0 + dt.timedelta(days=21 * (k // 2)))
            if dk <= min(b, D(y, 12, 31)):
                part = []
                for tooth in teeth[k:k + 2]:
                    part += [("D2950", tooth), (r.choice(["D2740", "D2750"]), tooth)]
                treat("crown", dk, part)
    return out


MAJOR = ("crown", "bridge", "implant", "denture")


def predet_kind(t):
    return t["kind"] if t["kind"] in MAJOR + ("endo", "perio") else None


# ---------------------------------------------------------------------------------------------------- providers
def npi(nine):
    """An NPI with its Luhn check digit over the 80840 prefix."""
    digits = [int(c) for c in "80840" + nine]
    total = 0
    for k, dgt in enumerate(reversed(digits)):
        if k % 2 == 0:
            dgt *= 2
            if dgt > 9:
                dgt -= 9
        total += dgt
    return nine + str((10 - total % 10) % 10)


def build_providers():
    r = rng("providers")
    out = {"general": [], "endo": [], "perio": [], "surgeon": [], "ortho": [], "oon": []}
    used = set()
    for kind, n in (("general", 96), ("endo", 8), ("perio", 7), ("surgeon", 9), ("ortho", 11), ("oon", 18)):
        while len(out[kind]) < n:
            nine = "1" + "".join(str(r.randint(0, 9)) for _ in range(8))
            if nine in used:
                continue
            used.add(nine)
            out[kind].append(npi(nine))
    return out


# ----------------------------------------------------------------------------------------------------- simulate
def _lag(r):
    return dt.timedelta(days=r.choice([1, 1, 2, 2, 3, 3, 4, 5, 6, 8, 11, 15]))


def _turnaround(r, received_day, quarter_key):
    """Ridgeline's business days to answer a predetermination, slower in the quarter the platform moved."""
    slow = {"2025Q3": 0.30, "2025Q4": 0.16, "2025Q1": 0.07, "2025Q2": 0.09, "2026Q1": 0.10, "2026Q2": 0.06,
            "2026Q3": 0.08, "2024Q1": 0.08, "2024Q2": 0.07, "2024Q3": 0.09, "2024Q4": 0.10}.get(quarter_key, 0.08)
    if r.random() < slow:
        return r.choice([6, 6, 7, 7, 8, 9, 11])
    return r.choice([1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5])


def _receipt_local(r, d):
    """A request's local arrival time: mostly office hours, some evening or weekend portal uploads."""
    u = r.random()
    if u < 0.80:
        t = dt.time(r.randint(7, 16), r.randint(0, 59))
    elif u < 0.92:
        t = dt.time(r.randint(17, 21), r.randint(0, 59))
    else:
        t = dt.time(r.choice([6, 16, 16, 16, 17, 17]), r.randint(0, 59))
    if t == dt.time(17, 0):
        t = dt.time(17, 1)      # no request is stamped on the cutoff minute itself
    return dt.datetime.combine(d, t)


def simulate(people, providers):
    """Adjudicate every person's claims year by year in arrival order against the plan's rules, with the
    predeterminations sent before major work and the member's response to a cut estimate."""
    claims, predets, carry, held = [], [], {}, {}
    for base in people:
        rs, rw = rng("sim", base["pid"]), rng("warm", base["pid"])
        r = rs
        home = r.choice(providers["general"] if r.random() < 0.9 else providers["oon"])
        for y in (WARM,) + YEARS:
            # the plan has run at the same design for years: the members covered when the extracts begin bring the
            # work they put off in 2023 into January 2024, and nothing of 2023 itself is extracted
            if y == WARM and base["start"] > START:
                continue
            p = dict(base, start=D(WARM, 1, 1)) if y == WARM else base
            r = rw if y == WARM else rs
            if not coverage_in_year(p, y):
                carry.pop(p["pid"], None)
                continue
            # work put off from the year before stands in for a new need on the same tooth and procedure family
            hold = held.get((p["pid"], y), set())
            todo = [dict(t, origin="need") for t in needs(p, y)
                    if not any((c[:3], tooth) in hold for c, tooth in t["lines"])]
            for t in carry.pop(p["pid"], []):
                if covered(p, t["date"]) and t["date"] <= SERVICE_END:
                    todo.append(t)
            todo.sort(key=lambda t: (t["date"], t["kind"]))
            adjudicated = []           # (adj_date, paid) this plan year, for the remaining maximum at a given date
            ded_used = 0
            last_adj = D(y, 1, 1)
            paid_ytd_at = lambda when: sum(x for d0, x in adjudicated if d0 <= when)
            for t in todo:
                if not covered(p, t["date"]) or t["date"] > SERVICE_END or t["date"].year != y:
                    continue
                kind = predet_kind(t)
                prov = home
                if t["kind"] == "endo" and r.random() < 0.55:
                    prov = r.choice(providers["endo"])
                elif t["kind"] in ("perio",) and r.random() < 0.5:
                    prov = r.choice(providers["perio"])
                elif t["kind"] == "implant" and t["lines"][0][0] == "D6010":
                    prov = r.choice(providers["surgeon"])
                elif t["kind"] == "ext" and t["lines"][0][0] == "D7210":
                    prov = r.choice(providers["surgeon"])
                fees = FEES[max(y, START.year)]
                total_fee = sum(fees[c] for c, _ in t["lines"])
                deferred_groups = []
                if (kind and t.get("origin") == "need" and total_fee > 30000 and r.random() < PREDET_SHARE[kind]):
                    recv_day = max(D(y, 1, 2), t["date"] - dt.timedelta(days=r.randint(18, 55)), p["start"])
                    if recv_day >= t["date"]:
                        recv_day = t["date"] - dt.timedelta(days=1)
                    if recv_day.year == y:
                        local = _receipt_local(r, recv_day)
                        rday = receipt_day(local)
                        q = "%dQ%d" % (rday.year, (rday.month - 1) // 3 + 1)
                        # the estimate is issued in parts on the new platform: one record per tooth group
                        groups = []
                        for c, tooth in t["lines"]:
                            key = tooth if t["kind"] == "crown" else 0
                            if not groups or groups[-1][0] != key:
                                groups.append((key, []))
                            groups[-1][1].append((c, tooth))
                        resp_days = [_turnaround(r, rday, q) for _ in groups]
                        resp_local = []
                        for nd in resp_days:
                            rd = add_business(rday, nd)
                            resp_local.append(dt.datetime.combine(rd, dt.time(r.randint(8, 16), r.randint(0, 59))))
                        when = max(resp_local).date()
                        remaining = MAXIMUM - paid_ytd_at(when)
                        ded_met = ded_used >= DEDUCTIBLE
                        ded_left = max(0, DEDUCTIBLE - ded_used)
                        est_lines = []
                        cut_groups = set()
                        for gi, (key, glines) in enumerate(groups):
                            for c, tooth in glines:
                                allowed = fees[c]
                                ded = min(ded_left, allowed) if plan_class(c) > 1 else 0
                                ded_left -= ded
                                liab = (allowed - ded) * COINS[plan_class(c)] // 100
                                est = max(0, min(liab, remaining))
                                remaining -= est
                                if est < liab:
                                    cut_groups.add(gi)
                                est_lines.append(dict(group=gi, code=c, tooth=tooth, allowed=allowed, liab=liab,
                                                      est=est, ded=ded))
                        rec = dict(pid=p["pid"], provider=prov, received_local=local, receipt_day=rday,
                                   responded_local=resp_local, groups=[g[1] for g in groups], lines=est_lines,
                                   kind=kind, year=y, treat_date=t["date"], outcome={})
                        if y != WARM:
                            predets.append(rec)
                        for gi in sorted(cut_groups):
                            # a member who has met the year's deductible weighs the cut estimate against 1 January
                            if r.random() < DEFER[kind] and ded_met:
                                deferred_groups.append(gi)
                                held.setdefault((p["pid"], y + 1), set()).update((c[:3], tooth) for c, tooth in groups[gi][1])
                                if r.random() < PROCEED[kind] and coverage_in_year(p, y + 1):
                                    dd = clinic_day(r, D(y + 1, 1, 2) + dt.timedelta(days=min(112, int(r.gammavariate(2.0, 16)))))
                                    # done while the estimate is still good (twelve months from its issue)
                                    valid = D(when.year + 1, when.month, min(when.day, 28)) - dt.timedelta(days=3)
                                    while dd > valid:
                                        dd = clinic_day(r, D(y + 1, 1, 2) + dt.timedelta(days=r.randint(0, 20)))
                                    carry.setdefault(p["pid"], []).append(
                                        dict(kind=t["kind"], date=dd, lines=groups[gi][1], origin="deferred",
                                             provider=prov))
                                    rec["outcome"][gi] = ("deferred_done", dd)
                                else:
                                    rec["outcome"][gi] = ("deferred_dropped", None)
                            else:
                                rec["outcome"][gi] = ("cut_done", t["date"])
                        for gi in range(len(groups)):
                            rec["outcome"].setdefault(gi, ("done", t["date"]))
                        if deferred_groups:
                            keep = [ln for gi, (key, gl) in enumerate(groups) if gi not in deferred_groups for ln in gl]
                            if not keep:
                                continue
                            t = dict(t, lines=keep)
                if t.get("provider"):
                    prov = t["provider"]
                received = t["date"] + _lag(r)
                # a person's claims are adjudicated in the order they arrive, which keeps the order of service
                adj_date = max(last_adj, received + dt.timedelta(days=r.choice([0, 0, 1, 1, 2, 3, 5])))
                if adj_date > EXTRACT:
                    continue
                last_adj = adj_date
                lines = []
                for c, tooth in t["lines"]:
                    allowed = fees[c]
                    if t["kind"] == "extra":
                        lines.append(dict(code=c, tooth=tooth, allowed=0, liab=0, paid=0, reason="FRQ", ded=0))
                        continue
                    remaining = MAXIMUM - paid_ytd_at(adj_date)
                    remaining -= sum(x["paid"] for x in lines)
                    ded = min(max(0, DEDUCTIBLE - ded_used), allowed) if plan_class(c) > 1 else 0
                    ded_used += ded
                    liab = (allowed - ded) * COINS[plan_class(c)] // 100
                    paid = max(0, min(liab, remaining))
                    reason = "MAX" if paid < liab else ("DED" if ded else "")
                    lines.append(dict(code=c, tooth=tooth, allowed=allowed, liab=liab, paid=paid, reason=reason, ded=ded))
                adjudicated.append((adj_date, sum(x["paid"] for x in lines)))
                if y == WARM:
                    continue
                claims.append(dict(cid=len(claims), pid=p["pid"], provider=prov, dos=t["date"], received=received,
                                   adjudicated=adj_date, lines=lines, kind=t["kind"], origin=t.get("origin", "need"),
                                   year=y))
    return claims, predets


def adjustments(claims):
    """A small share of claims is corrected after adjudication (a coded surface count, an evaluation billed as
    periodic, a crown's material): the corrected claim replaces the original."""
    swap = {"D2391": "D2392", "D2392": "D2393", "D0120": "D0150", "D2750": "D2740", "D2140": "D2150",
            "D1110": "D4910"}
    out = {}
    for c in claims:
        r = rng("adjust", c["cid"])
        if r.random() >= ADJUST_SHARE:
            continue
        cand = [k for k, ln in enumerate(c["lines"]) if ln["code"] in swap and ln["reason"] in ("", "DED")]
        if not cand:
            continue
        k = r.choice(cand)
        old = c["lines"][k]
        new_code = swap[old["code"]]
        fees = FEES[c["dos"].year]
        allowed = fees[new_code]
        ded = old["ded"]
        liab = (allowed - ded) * COINS[plan_class(new_code)] // 100
        lines = [dict(ln) for ln in c["lines"]]
        lines[k] = dict(old, code=new_code, allowed=allowed, liab=liab, paid=liab)
        when = c["adjudicated"] + dt.timedelta(days=r.randint(12, 48))
        if when > EXTRACT:
            continue
        out[c["cid"]] = dict(date=when, lines=lines)
    return out


def ortho_cases(people, providers):
    """Comprehensive orthodontic cases for covered children: banding date, case fee, months of treatment and the
    orthodontist; a family's move hands a case to a second orthodontist, who continues it."""
    out = []
    for p in people:
        if p["kind"] != "C":
            continue
        r = rng("ortho", p["pid"])
        for y in YEARS:
            cov = coverage_in_year(p, y)
            if not cov or not (9 <= age_on(p, D(y, 7, 1)) <= 16):
                continue
            if any(c["pid"] == p["pid"] for c in out):
                break
            if r.random() < 0.045:
                band = _day_in(r, cov[0], cov[1])
                months = r.choice([18, 20, 22, 24, 24, 26, 28, 30])
                fee = r.choice([5200, 5600, 5900, 6200, 6500, 6800]) * 100
                case = dict(pid=p["pid"], band=band, months=months, fee=fee, ortho=r.choice(providers["ortho"]),
                            transfer=None)
                if r.random() < 0.08:
                    t = add_months(band, r.randint(5, months - 4))
                    case["transfer"] = dict(date=t, ortho=r.choice([o for o in providers["ortho"] if o != case["ortho"]]),
                                            fee=r.choice([2600, 3100, 3500]) * 100)
                out.append(case)
    return out


def build():
    people = build_people()
    providers = build_providers()
    claims, predets = simulate(people, providers)
    adj = adjustments(claims)
    return dict(people=people, providers=providers, claims=claims, predets=predets, adjust=adj,
                ortho=ortho_cases(people, providers))

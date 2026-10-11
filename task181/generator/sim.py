"""Simulate the unit's pertussis cases and the laboratory notifications they produce, January 2019 to
the extract at 07:00 on Monday 5 October 2026.

A case is a person's illness with its first specimen; a notification is one laboratory's report of
one specimen. Each case's specimen travels by its area's laboratory route: the hospital laboratory
in Wagga Wagga, reached by the district's daily specimen courier, or Inland Pathology, whose
collection centres send swabs on the Tuesday and Friday 10:30 runs to its Sydney laboratory (a weekly
Thursday screen, positives confirmed on the Tuesday run, keyed the next working day). What the
extract holds is every notification received by 07:00 on the extract day; the rest is the world."""
import datetime as dt

import numpy as np

import world as W

DAY = dt.timedelta(days=1)


def at(d, h, m=0):
    return dt.datetime(d.year, d.month, d.day, h, m, tzinfo=W.SYD)


def plus_minutes(d, minutes):
    return at(d, 0) + dt.timedelta(seconds=int(round(float(minutes) * 60)))


# ------------------------------------------------------------------ the private route

P_FAIL, P_RECOLLECT, P_MISS = 0.11, 0.06, 0.03
P_URGENT, P_URGENT_INFANT = 0.07, 0.5
URGENT = [None]                      # the urgent-request stream, set by simulate()


def next_courier(t):
    d = t.date()
    for k in range(0, 28):
        day = d + k * DAY
        if day.weekday() in (1, 4) and day not in W.HOLIDAYS:
            dep = at(day, 10, 30)
            if dep >= t:
                return dep
    raise RuntimeError("no courier")


def screen_after(arr):
    """The weekly Thursday screen at 10:00 takes specimens received by 08:00 that morning."""
    d = arr.date()
    for k in range(0, 28):
        day = d + k * DAY
        if day.weekday() == 3 and at(day, 8) >= arr:
            run = day
            while not W.working_day(run):
                run += DAY
            return at(run, 10)
    raise RuntimeError("no screen")


def confirm_after(screen):
    d = screen.date() + DAY
    while d.weekday() != 1:
        d += DAY
    while not W.working_day(d):
        d += DAY
    return at(d, 10)


def keyed_after(confirm, minute):
    d = confirm.date() + DAY
    while not W.working_day(d):
        d += DAY
    return plus_minutes(d, minute)


def private_received(t, urgent, u):
    """u: a dict of uniform draws (miss, fail, recollect, minute, urgent_minute)."""
    dep = next_courier(t)
    if u["miss"] < P_MISS:
        dep = next_courier(dep + dt.timedelta(minutes=1))
    arr = at(dep.date() + DAY, 7, 30)
    if urgent:
        day = arr.date()
        while day.weekday() == 6 or day in W.HOLIDAYS:
            day += DAY
        return plus_minutes(day, 12 * 60 + u["urgent_minute"] * 390)
    scr = screen_after(arr)
    if u["fail"] < P_FAIL:
        scr = screen_after(scr + DAY)
    conf = confirm_after(scr)
    if u["recollect"] < P_RECOLLECT:
        conf = confirm_after(confirm_after(conf + DAY) + DAY)
    return keyed_after(conf, 9 * 60 + u["minute"] * 450)


# ------------------------------------------------------------------ the hospital route

def hospital_received(t, area, u):
    if area == "Wagga Wagga" or area is None and u["near"] < 0.5:
        arrive = t + dt.timedelta(minutes=90) if t.hour < 16 else at(t.date() + DAY, 8)
    else:
        d = t.date()
        while True:
            dep = at(d, 14)
            if d.weekday() < 6 and d not in W.HOLIDAYS and dep >= t + dt.timedelta(minutes=15):
                break
            d += DAY
        arrive = at(d, 18)
    run = None
    d = arrive.date()
    while run is None:
        if d.weekday() < 6 and d not in W.HOLIDAYS:
            slots = (10, 15) if d.weekday() < 5 else (10,)
            for h in slots:
                if at(d, h) >= arrive + dt.timedelta(minutes=30):
                    run = at(d, h)
                    break
        d += DAY
    rel = run.date() + DAY
    while rel.weekday() == 6 or rel in W.HOLIDAYS:
        rel += DAY
    if u["fail"] < 0.07:
        rel += DAY * (1 + int(u["extra"] * 2))
    elif u["fail"] < 0.09:
        rel += DAY * (3 + int(u["extra"] * 4))
    while rel.weekday() == 6 or rel in W.HOLIDAYS:
        rel += DAY
    return plus_minutes(rel, 8 * 60 + 30 + u["minute"] * 600)


def draws(rng):
    return {k: float(rng.random()) for k in ("miss", "fail", "recollect", "minute", "urgent_minute", "extra", "near")}


def received(t, route, urgent, area, u):
    return private_received(t, urgent, u) if route == "P" else hospital_received(t, area, u)


# ------------------------------------------------------------------ the epidemic curve

RATE_KNOTS = [  # district rate per 100,000 per year
    ("2019-01-01", 45), ("2019-04-01", 38), ("2019-07-01", 44), ("2019-10-15", 72), ("2019-12-31", 62),
    ("2020-02-15", 50), ("2020-03-20", 34), ("2020-04-20", 2.2), ("2020-12-31", 1.2), ("2021-12-31", 1.0),
    ("2022-07-01", 1.6), ("2022-12-31", 2.8), ("2023-04-01", 5), ("2023-08-01", 14), ("2023-12-31", 42),
    ("2024-02-01", 70), ("2024-05-01", 150), ("2024-07-15", 260), ("2024-09-20", 340), ("2024-11-01", 320),
    ("2024-12-31", 250), ("2025-03-01", 250), ("2025-06-01", 215), ("2025-09-25", 205), ("2025-12-31", 150),
    ("2026-03-01", 120), ("2026-06-01", 105), ("2026-07-15", 100), ("2026-08-31", 150),
]
# area multipliers on the district curve, by date (the 2024 epidemic reached the areas at different times)
AREA_KNOTS = {
    "Wagga Wagga": [("2019-01-01", 1.0), ("2023-12-31", 1.0), ("2024-05-01", 1.25), ("2024-08-15", 0.6),
                    ("2024-11-01", 0.55), ("2025-04-01", 0.8), ("2025-09-25", 0.62), ("2026-01-01", 0.9),
                    ("2026-07-10", 1.0), ("2026-08-31", 2.6)],
    "Griffith": [("2019-01-01", 1.0), ("2023-12-31", 1.0), ("2024-06-01", 1.1), ("2024-09-20", 1.35),
                 ("2025-03-01", 1.2), ("2025-09-25", 1.0), ("2026-01-01", 1.25), ("2026-08-31", 1.1)],
    "Snowy Valleys": [("2019-01-01", 1.0), ("2023-12-31", 1.0), ("2024-06-01", 1.3), ("2024-09-20", 2.1),
                      ("2025-03-01", 1.9), ("2025-09-25", 2.2), ("2026-01-01", 1.1), ("2026-08-31", 1.1)],
    "Leeton": [("2019-01-01", 1.0), ("2024-09-20", 1.2), ("2025-09-25", 1.05), ("2026-08-31", 0.9)],
}


def _interp(knots, days):
    xs = np.array([(dt.date.fromisoformat(k) - W.START).days for k, _ in knots], float)
    ys = np.array([v for _, v in knots], float)
    return np.interp(days, xs, ys)


def daily_rate(area, n_days):
    days = np.arange(n_days, dtype=float)
    base = _interp(RATE_KNOTS, days)
    mult = _interp(AREA_KNOTS.get(area, [("2019-01-01", 1.0), ("2026-12-31", 1.0)]), days)
    return base * mult * W.POP[area] / 1e5 / 365.25


# ------------------------------------------------------------------ people and attributes

AGE_BANDS = [(1, 5, 0.09), (5, 10, 0.22), (10, 15, 0.21), (15, 20, 0.07), (20, 40, 0.15), (40, 60, 0.15), (60, 88, 0.11)]


class Ids:
    def __init__(self):
        r = W.stream("ids")
        self.persons = list(r.choice(np.arange(1_000_000, 9_999_999), size=9000, replace=False))
        self.mrns = list(r.choice(np.arange(210_000, 1_890_000), size=60000, replace=False))
        self.pi = 0
        self.mi = 0

    def person(self):
        self.pi += 1
        return "P%07d" % self.persons[self.pi - 1]

    def mrn(self):
        self.mi += 1
        return int(self.mrns[self.mi - 1])


def in_clean_window(d):
    """The six windows the main call reads: the fortnight and its five prior-year counterparts."""
    for y in W.PRIOR_YEARS + (2026,):
        if dt.date(y, 9, 21) <= d <= dt.date(y, 10, 4):
            return True
    return False


def near_clean_window(d, pad=95):
    for y in W.PRIOR_YEARS + (2026,):
        if dt.date(y, 9, 21) - dt.timedelta(days=pad) <= d <= dt.date(y, 10, 4) + dt.timedelta(days=pad):
            return True
    return False


def draw_age(rng, infant_share):
    if rng.random() < infant_share:
        return float(rng.uniform(0.02, 0.98))
    w = np.array([b[2] for b in AGE_BANDS])
    i = rng.choice(len(AGE_BANDS), p=w / w.sum())
    return float(rng.uniform(AGE_BANDS[i][0], AGE_BANDS[i][1]))


def dob_from_age(spec, age):
    return spec - dt.timedelta(days=int(round(age * 365.25)))


def collection_time(d, route, rng):
    if route == "P":
        if d.weekday() == 5:
            return plus_minutes(d, 8 * 60 + rng.random() * 230)
        return plus_minutes(d, 8 * 60 + rng.random() * 540)
    if d.weekday() >= 5 or d in W.HOLIDAYS:
        return plus_minutes(d, 7 * 60 + rng.random() * 900)
    return plus_minutes(d, 8 * 60 + rng.random() * 600)


def draw_postcode(area, rng, clean):
    if clean:
        opts = W.CLEAN_POSTCODES[area]
        w = np.array([dict(W.HOME_POSTCODES[area])[p] for p in opts])
        return opts[int(rng.choice(len(opts), p=w / w.sum()))]
    opts = W.HOME_POSTCODES[area]
    w = np.array([x[1] for x in opts])
    return opts[int(rng.choice(len(opts), p=w / w.sum()))][0]


def onset_for(spec, age, rng):
    p = 0.86 if age < 15 else 0.44
    if rng.random() >= p:
        return None
    return spec - dt.timedelta(days=int(np.clip(round(rng.gamma(4.0, 2.6)), 2, 35)))


def gp_day(d, rng):
    """Most people who fall ill over a Sunday or a public holiday are swabbed by their GP on the next
    working day; the rest present to an emergency department that day."""
    if (d.weekday() == 6 or d in W.HOLIDAYS) and rng.random() < 0.85:
        d += DAY
        while d.weekday() == 6 or d in W.HOLIDAYS:
            d += DAY
    return d


def make_case(ids, rng, area, d, clean, infant_share=0.05, visitor_postcode=None):
    if not clean:
        d = gp_day(d, rng)
    age = draw_age(rng, 0.0 if clean else infant_share)
    route = "P" if rng.random() < W.PRIVATE_SHARE.get(area, 0.3) else "H"
    test = "PCR"
    if not clean and age >= 15 and rng.random() < 0.13:
        test, route = "Serology", "P"
    elif not clean and route == "H" and rng.random() < 0.025:
        test = "Culture"
    if d.weekday() == 6 or d in W.HOLIDAYS:
        route = "H" if test != "Serology" else route
    if route == "P" and (d.weekday() == 6 or d in W.HOLIDAYS):
        d = d + DAY
        while d.weekday() == 6 or d in W.HOLIDAYS:
            d += DAY
    urgent = route == "P" and test == "PCR" and URGENT[0].random() < (P_URGENT_INFANT if age < 1 else P_URGENT)
    t = collection_time(d, route, rng)
    sex = "F" if rng.random() < 0.53 else "M"
    pc = visitor_postcode or draw_postcode(area, rng, clean)
    c = dict(person=ids.person(), area=area, postcode=pc, sex=sex, dob=dob_from_age(d, age), age=age,
             spec=t, route=route, urgent=urgent, test=test, onset=onset_for(d, age, rng),
             mrn=ids.mrn() if (age < 1 or rng.random() < (0.72 if route == "H" else 0.46)) else None,
             school=None, school_text=None, role=None, designed=None, visitor=visitor_postcode is not None)
    return c


def status_for(test, d):
    if test == "Serology":
        return "Probable" if d >= W.REVISION else "Confirmed"
    return "Confirmed"


def notifications_for(case, rng, allow_dup):
    """The case's notifications: its first specimen's, and sometimes a second laboratory's or a re-test."""
    out = []
    u = draws(rng)
    out.append(dict(spec=case["spec"], route=case["route"], test=case["test"], urgent=case["urgent"],
                    recv=received(case["spec"], case["route"], case["urgent"], case["area"], u)))
    p_dup = 0.38 if case["age"] < 1 else 0.07
    if allow_dup and rng.random() < p_dup:
        kind = "other" if (case["age"] < 1 or rng.random() < 0.6) else "retest"
        if kind == "other":
            d2 = case["spec"].date() + DAY * int(rng.integers(0, 5))
            route2 = "H" if case["route"] == "P" else "P"
            test2 = "PCR"
        else:
            d2 = case["spec"].date() + DAY * int(rng.integers(6, 26))
            route2, test2 = case["route"], "PCR"
        if route2 == "P":
            while d2.weekday() == 6 or d2 in W.HOLIDAYS:
                d2 += DAY
        t2 = collection_time(d2, route2, rng)
        urgent2 = route2 == "P" and case["age"] < 1
        out.append(dict(spec=t2, route=route2, test=test2, urgent=urgent2,
                        recv=received(t2, route2, urgent2, case["area"], draws(rng))))
    return out


# ------------------------------------------------------------------ history to 31 August 2026

WINDOW_TARGET = {"Wagga Wagga": 7, "Griffith": 7, "Snowy Valleys": 7, "Leeton": 3, "Narrandera": 2,
                 "Murrumbidgee": 1, "Hay": 1, "Edward River": 2, "Junee": 1, "Cootamundra-Gundagai": 3}
HIST_END = dt.date(2026, 8, 31)


def window_total(days, counts):
    tot = 0
    for y in W.PRIOR_YEARS:
        a = (dt.date(y, 9, 21) - W.START).days
        tot += int(counts[a:a + 14].sum())
    return tot


def history_counts(area):
    n = (HIST_END - W.START).days + 1
    lam = daily_rate(area, n)
    for s in range(0, 5000):
        r = W.stream("hist", area, s)
        counts = r.poisson(lam)
        if window_total(n, counts) == WINDOW_TARGET[area]:
            return counts, s
    raise RuntimeError("no history seed for %s" % area)


def simulate_history(ids):
    cases, seeds = [], {}
    n = (HIST_END - W.START).days + 1
    for area in W.AREA_NAMES:
        counts, s = history_counts(area)
        seeds[area] = s
        r = W.stream("attrs", area, s)
        for i in range(n):
            d = W.START + i * DAY
            for _ in range(int(counts[i])):
                clean = in_clean_window(d)
                c = make_case(ids, r, area, d, clean)
                c["clean"] = clean
                if dt.date(2026, 1, 1) <= d <= HIST_END and c["age"] < 0.5:
                    c["age"] = float(r.uniform(1.2, 4.5))      # infants under six months this year are designed
                    c["dob"] = dob_from_age(d, c["age"])
                cases.append(c)
    # visitors: residents of neighbouring areas notified to the unit
    vr = W.stream("visitors")
    lam = daily_rate("Wagga Wagga", n) * 0.06
    vcounts = vr.poisson(lam)
    vp = [p for p, _ in W.VISITOR_POSTCODES]
    vw = np.array([w for _, w in W.VISITOR_POSTCODES])
    for i in range(n):
        d = W.START + i * DAY
        if in_clean_window(d):
            continue
        for _ in range(int(vcounts[i])):
            pc = vp[int(vr.choice(len(vp), p=vw / vw.sum()))]
            c = make_case(ids, vr, "Wagga Wagga", d, False, visitor_postcode=pc)
            c["area"] = None
            c["clean"] = False
            cases.append(c)
    return cases, seeds


# ------------------------------------------------------------------ September 2026 and the designed infants

def _d(s):
    return dt.date.fromisoformat(s)


# area, date, hh:mm, route, urgent, test, age, sex, school, text, role, notified by the extract
SEPTEMBER = [
    # Wagga Wagga: the seasonal rise, through the hospital laboratory
    ("Wagga Wagga", "2026-09-02", "09:40", "H", False, "PCR", 34, "F", None, None, None, True),
    ("Wagga Wagga", "2026-09-03", "11:15", "H", False, "PCR", 8, "M", "fernleigh", "Fernleigh Rd PS", "Student", True),
    ("Wagga Wagga", "2026-09-07", "10:05", "H", False, "PCR", 52, "M", None, None, None, True),
    ("Wagga Wagga", "2026-09-09", "14:20", "P", False, "Serology", 15, "F", "bolton", "Bolton Park High", "Student", True),
    ("Wagga Wagga", "2026-09-10", "09:10", "H", False, "PCR", 9, "M", "wollundry", "Wollundry PS", "Student", True),
    ("Wagga Wagga", "2026-09-11", "15:30", "H", False, "PCR", 41, "F", None, None, None, True),
    ("Wagga Wagga", "2026-09-12", "10:45", "H", False, "PCR", 7, "F", "fernleigh", "Fernleigh Road Public School", "Student", True),
    ("Wagga Wagga", "2026-09-14", "08:50", "H", False, "PCR", 63, "M", None, None, None, True),
    ("Wagga Wagga", "2026-09-15", "12:10", "H", False, "PCR", 44, "F", "bolton", "Bolton Park High School", "Staff", True),
    ("Wagga Wagga", "2026-09-16", "09:25", "H", False, "PCR", 10, "F", "wollundry", "Wollundry Public School", "Student", True),
    ("Wagga Wagga", "2026-09-17", "11:00", "H", False, "PCR", 4, "M", "wollundry_pre", "Wollundry Preschool", "Student", True),
    ("Wagga Wagga", "2026-09-18", "16:40", "H", False, "PCR", 29, "M", None, None, None, True),
    ("Wagga Wagga", "2026-09-19", "13:15", "H", False, "PCR", 12, "M", None, None, None, True),
    ("Wagga Wagga", "2026-09-21", "10:20", "H", False, "PCR", 38, "F", None, None, None, True),
    ("Wagga Wagga", "2026-09-22", "09:05", "H", False, "PCR", 6, "M", None, None, None, True),
    ("Wagga Wagga", "2026-09-23", "10:35", "H", False, "PCR", 8, "F", "wollundry", "Wollundry Public", "Student", True),
    ("Wagga Wagga", "2026-09-24", "11:50", "H", False, "PCR", 16, "M", "bolton", "Bolton Park HS", "Student", True),
    ("Wagga Wagga", "2026-09-25", "09:30", "H", False, "PCR", 45, "M", None, None, None, True),
    ("Wagga Wagga", "2026-09-27", "18:20", "H", False, "PCR", 11, "F", None, None, None, True),
    ("Wagga Wagga", "2026-09-28", "10:10", "H", False, "PCR", 70, "F", None, None, None, True),
    ("Wagga Wagga", "2026-09-29", "13:40", "H", False, "PCR", 33, "M", None, None, None, True),
    ("Wagga Wagga", "2026-10-01", "09:15", "H", False, "PCR", 3, "M", None, None, None, True),
    ("Wagga Wagga", "2026-10-03", "19:30", "H", False, "PCR", 50, "F", None, None, None, False),
    ("Wagga Wagga", "2026-10-04", "11:45", "H", False, "PCR", 9, "M", None, None, None, False),
    # Griffith: the school outbreak, through Inland Pathology
    ("Griffith", "2026-09-03", "11:30", "P", False, "PCR", 47, "M", None, None, None, True),
    ("Griffith", "2026-09-18", "15:10", "P", False, "PCR", 9, "F", "banna", "Banna Ave PS", "Student", True),
    ("Griffith", "2026-09-21", "08:55", "P", False, "PCR", 10, "M", "banna", "Banna Avenue Public", "Student", True),
    ("Griffith", "2026-09-21", "11:20", "P", False, "PCR", 8, "F", "banna", "banna ave public school", "Student", True),
    ("Griffith", "2026-09-22", "09:05", "P", False, "PCR", 39, "F", "banna", "Banna Ave PS", "Parent or carer", True),
    ("Griffith", "2026-09-22", "08:40", "P", False, "PCR", 7, "F", "kooyoo", "Kooyoo St PS", "Student", True),
    ("Griffith", "2026-09-29", "08:15", "P", True, "PCR", 9, "M", "banna", "Banna Av. P.S.", "Student", True),
    ("Griffith", "2026-09-30", "19:45", "H", False, "PCR", 10, "M", "kooyoo", "Kooyoo Street Public School", "Student", True),
    ("Griffith", "2026-10-01", "09:20", "P", True, "PCR", 11, "M", "banna", "Banna Avenue Public School", "Student", True),
] + [("Griffith", d, hm, "P", False, "PCR", age, sex, None, None, None, False) for d, hm, age, sex in (
    ("2026-09-22", "11:40", 8, "M"), ("2026-09-22", "15:15", 36, "F"), ("2026-09-23", "09:20", 10, "F"),
    ("2026-09-23", "10:55", 9, "M"), ("2026-09-23", "14:30", 12, "F"), ("2026-09-24", "08:35", 7, "M"),
    ("2026-09-24", "11:10", 41, "M"), ("2026-09-24", "16:20", 11, "F"), ("2026-09-25", "09:45", 8, "F"),
    ("2026-09-25", "12:00", 10, "M"), ("2026-09-25", "15:35", 6, "F"), ("2026-09-26", "09:10", 9, "F"),
    ("2026-09-26", "10:40", 34, "M"), ("2026-09-28", "08:30", 7, "M"), ("2026-09-28", "09:50", 10, "F"),
    ("2026-09-28", "11:35", 8, "M"), ("2026-09-28", "14:05", 12, "M"), ("2026-09-28", "16:30", 44, "F"),
    ("2026-09-29", "11:15", 9, "F"), ("2026-09-29", "13:20", 11, "M"), ("2026-09-29", "15:50", 7, "F"),
    ("2026-09-29", "16:45", 38, "M"), ("2026-09-30", "08:45", 10, "F"), ("2026-09-30", "10:25", 8, "M"),
    ("2026-09-30", "13:10", 9, "M"), ("2026-09-30", "15:55", 6, "F"), ("2026-10-01", "09:35", 11, "F"),
    ("2026-10-01", "11:50", 42, "F"), ("2026-10-01", "14:40", 8, "M"), ("2026-10-02", "08:55", 10, "M"),
    ("2026-10-02", "12:25", 7, "F"), ("2026-10-02", "15:05", 9, "F"), ("2026-10-03", "10:15", 12, "M"))] + [
    ("Griffith", "2026-10-03", "20:10", "H", False, "PCR", 5, "F", None, None, None, False),
    # Snowy Valleys: a household and two classmates, through the hospital laboratory
    ("Snowy Valleys", "2026-09-05", "10:30", "H", False, "PCR", 36, "F", None, None, None, True),
    ("Snowy Valleys", "2026-09-12", "11:05", "H", False, "PCR", 13, "M", None, None, None, True),
    ("Snowy Valleys", "2026-09-21", "09:45", "H", False, "PCR", 58, "M", None, None, None, True),
    ("Snowy Valleys", "2026-09-22", "10:15", "H", False, "PCR", 7, "M", "blowering", "Blowering Rd PS", "Student", True),
    ("Snowy Valleys", "2026-09-23", "08:50", "H", False, "PCR", 31, "F", None, None, None, True),
    ("Snowy Valleys", "2026-09-25", "09:05", "H", False, "PCR", 9, "F", "blowering", "Blowering Road Public School", "Student", True),
    ("Snowy Valleys", "2026-09-26", "11:30", "H", False, "PCR", 2, "F", None, None, None, True),
    ("Snowy Valleys", "2026-09-29", "10:40", "H", False, "PCR", 66, "M", None, None, None, True),
    ("Snowy Valleys", "2026-09-30", "09:20", "H", False, "PCR", 42, "F", None, None, None, True),
    ("Snowy Valleys", "2026-10-02", "10:50", "H", False, "PCR", 25, "M", None, None, None, False),
    # Leeton
    ("Leeton", "2026-09-08", "09:00", "P", False, "PCR", 8, "M", "canal", "Canal Rd PS", "Student", True),
    ("Leeton", "2026-09-21", "10:05", "P", False, "PCR", 52, "F", None, None, None, True),
    ("Leeton", "2026-09-24", "14:15", "P", False, "PCR", 37, "M", None, None, None, False),
    ("Leeton", "2026-09-30", "10:50", "P", False, "PCR", 9, "F", None, None, None, False),
    # Cootamundra-Gundagai
    ("Cootamundra-Gundagai", "2026-09-04", "09:00", "H", False, "PCR", 10, "F", "hurley", "Hurley St Public", "Student", True),
    ("Cootamundra-Gundagai", "2026-09-22", "10:30", "H", False, "PCR", 8, "M", "hurley", "Hurley Street Public School", "Student", True),
    ("Cootamundra-Gundagai", "2026-09-26", "12:40", "H", False, "PCR", 61, "F", None, None, None, True),
    # the other areas
    ("Narrandera", "2026-09-23", "11:20", "H", False, "PCR", 12, "F", "twynam", "Twynam St PS", "Student", True),
    ("Edward River", "2026-09-28", "09:40", "H", False, "PCR", 57, "F", None, None, None, True),
    ("Junee", "2026-09-10", "10:00", "H", False, "PCR", 49, "M", None, None, None, True),
    ("Hay", "2026-09-02", "09:30", "H", False, "PCR", 71, "M", None, None, None, True),
]
# the second laboratory's notification for the Canal Road student (seen at Leeton Hospital three days on)
SEPTEMBER_SECOND = {("Leeton", "2026-09-08", "09:00"): ("2026-09-11", "14:50", "H", True)}

# Infants under six months notified January to August 2026. adm: A admitted within 14 days of the
# specimen, B an admission well away from it, None none. vacc: A dTpa at 20 to 32 weeks, B dTpa in
# the last fortnight before birth, C dTpa in an earlier pregnancy only, D influenza only, E nothing.
INFANTS = [
    # key, area, postcode, dob, specimen, route, urgent, second notification, adm, adm offset, vacc
    ("I1", "Wagga Wagga", "2650", "2025-11-02", "2026-02-10", "H", False, None, "A", 0, "A"),
    ("I2", "Wagga Wagga", "2650", "2026-03-15", "2026-06-03", "P", True, ("2026-06-05", "H"), "A", 2, "B"),
    ("I3", "Wagga Wagga", "2651", "2026-05-20", "2026-08-18", "H", False, None, "B", -90, "C"),
    ("I4", "Griffith", "2680", "2025-12-08", "2026-04-14", "P", False, None, None, None, "A"),
    ("I5", "Griffith", "2680", "2026-06-25", "2026-08-27", "H", False, None, "A", 0, "D"),
    ("I6", "Leeton", "2705", "2026-01-30", "2026-05-21", "P", True, None, "B", 50, "A"),
    ("I7", "Snowy Valleys", "2720", "2026-02-14", "2026-03-30", "H", False, None, "A", 2, "E"),
    ("I8", "Junee", "2663", "2025-10-20", "2026-01-22", "H", False, None, None, None, "A"),
    ("I9", "Edward River", "2710", "2026-04-02", "2026-07-14", "H", False, None, "A", -1, "B"),
    ("I10", "Cootamundra-Gundagai", "2727", "2026-05-05", "2026-08-27", "H", False, None, "A", -1, "A"),
    ("I11", "Wagga Wagga", "2650", "2025-08-01", "2026-03-10", "H", False, None, "A", 1, "A"),
    ("I12", "Narrandera", "2700", "2025-12-20", "2026-06-01", "H", False, None, None, None, "C"),
]


def designed_received(t, route, urgent, area, want, rng):
    for _ in range(4000):
        r = received(t, route, urgent, area, draws(rng))
        if (r <= W.EXTRACT_LOCAL) == want:
            return r
    raise RuntimeError("no draw gives %s for %s %s" % (want, area, t))


def build_september(ids):
    rng = W.stream("september")
    cases = []
    for (area, d, hm, route, urgent, test, age, sex, school, text, role, want) in SEPTEMBER:
        day = _d(d)
        h, m = (int(x) for x in hm.split(":"))
        t = at(day, h, m)
        age_f = float(age) + float(rng.uniform(0.05, 0.9))
        c = dict(person=ids.person(), area=area, postcode=draw_postcode(area, rng, True), sex=sex,
                 dob=dob_from_age(day, age_f), age=age_f, spec=t, route=route, urgent=urgent, test=test,
                 onset=onset_for(day, age_f, rng) if want else None,
                 mrn=ids.mrn() if (route == "H" or rng.random() < 0.4) else None,
                 school=school, school_text=text, role=role, designed="september", visitor=False, clean=True)
        nots = [dict(spec=t, route=route, test=test, urgent=urgent,
                     recv=designed_received(t, route, urgent, area, want, rng))]
        second = SEPTEMBER_SECOND.get((area, d, hm))
        if second:
            d2, hm2, route2, want2 = second
            h2, m2 = (int(x) for x in hm2.split(":"))
            t2 = at(_d(d2), h2, m2)
            nots.append(dict(spec=t2, route=route2, test="PCR", urgent=False,
                             recv=designed_received(t2, route2, False, area, want2, rng)))
            c["clean"] = False
        c["notifications"] = nots
        cases.append(c)
    return cases


def build_infants(ids):
    rng = W.stream("infants")
    cases = []
    for (key, area, pc, dob, spec, route, urgent, second, adm, adm_off, vacc) in INFANTS:
        day = _d(spec)
        t = collection_time(day, route, rng) if route == "P" else plus_minutes(day, 9 * 60 + rng.random() * 600)
        age = (day - _d(dob)).days / 365.25
        c = dict(person=ids.person(), area=area, postcode=pc, sex="F" if rng.random() < 0.5 else "M", dob=_d(dob),
                 age=age, spec=t, route=route, urgent=urgent, test="PCR", onset=day - DAY * int(rng.integers(4, 15)),
                 mrn=ids.mrn(), school=None, school_text=None, role=None, designed=key, visitor=False, clean=False,
                 infant=dict(key=key, adm=adm, adm_off=adm_off, vacc=vacc))
        nots = [dict(spec=t, route=route, test="PCR", urgent=urgent,
                     recv=designed_received(t, route, urgent, area, True, rng))]
        if second:
            d2, route2 = second
            t2 = plus_minutes(_d(d2), 10 * 60 + rng.random() * 360)
            nots.append(dict(spec=t2, route=route2, test="PCR", urgent=route2 == "P",
                             recv=designed_received(t2, route2, route2 == "P", area, True, rng)))
        c["notifications"] = nots
        cases.append(c)
    return cases


def reinfections(cases, ids):
    """A few people are notified again in a later, separate illness (more than 90 days on)."""
    r = W.stream("reinfect")
    early = [c for c in cases if c["area"] and not c["clean"] and c["spec"].date() < dt.date(2023, 6, 1) and c["age"] >= 15]
    late = [c for c in cases if c["area"] and not c["clean"] and dt.date(2024, 3, 1) <= c["spec"].date() <= dt.date(2026, 6, 30)
            and c["age"] >= 18 and not c.get("designed")]
    pairs = 0
    for c in late:
        cand = [e for e in early if e["area"] == c["area"] and abs(e["age"] + (c["spec"] - e["spec"]).days / 365.25 - c["age"]) < 40]
        if not cand or r.random() > 0.02:
            continue
        e = cand[int(r.integers(0, len(cand)))]
        c["person"], c["dob"], c["sex"] = e["person"], e["dob"], e["sex"]
        c["age"] = (c["spec"].date() - e["dob"]).days / 365.25
        c["mrn"] = e["mrn"] if e["mrn"] else c["mrn"]
        early.remove(e)
        pairs += 1
        if pairs >= 6:
            break
    return pairs


def simulate(urgent_seed=0):
    URGENT[0] = W.stream("urgent", urgent_seed)
    ids = Ids()
    hist, seeds = simulate_history(ids)
    nr = W.stream("notify")
    for c in hist:
        nots = notifications_for(c, nr, allow_dup=not c["clean"])
        keep = [nots[0]] + [n for n in nots[1:] if not in_clean_window(n["spec"].date())
                            and n["spec"].date() <= dt.date(2026, 8, 31)]
        c["notifications"] = keep
    npairs = reinfections(hist, ids)
    cases = hist + build_september(ids) + build_infants(ids)
    return dict(cases=cases, seeds=seeds, reinfection_pairs=npairs, ids=ids)

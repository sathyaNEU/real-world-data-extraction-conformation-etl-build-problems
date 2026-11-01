"""task145 architecture 2: the clean truth. Calendars, students, enrolment records, the absence days (scattered days
and runs), course grades, behaviour incidents and suspensions, and who leaves. Nothing here ships as it stands;
pack.py writes the network's own exports from it."""
import datetime as dt

import numpy as np

import params as P

D = dt.timedelta
YEAR_LABELS = [y[0] for y in P.YEARS]


def nth_weekday(y, m, wd, n):
    d = dt.date(y, m, 1)
    while d.weekday() != wd:
        d += D(days=1)
    return d + D(days=7 * (n - 1))


def last_weekday(y, m, wd):
    d = dt.date(y, m + 1, 1) - D(days=1)
    while d.weekday() != wd:
        d -= D(days=1)
    return d


def holidays(first, last):
    y0, y1 = first.year, last.year
    h = {nth_weekday(y0, 9, 0, 1): "Labor Day"}
    fb = nth_weekday(y0, 10, 0, 3)
    h.update({fb: "Fall break", fb + D(days=1): "Fall break"})
    tg = nth_weekday(y0, 11, 3, 4)
    h.update({tg - D(days=1): "Thanksgiving break", tg: "Thanksgiving Day", tg + D(days=1): "Thanksgiving break"})
    h[nth_weekday(y1, 1, 0, 3)] = "Martin Luther King Jr. Day"
    h[nth_weekday(y1, 2, 0, 3)] = "Presidents' Day"
    sb = nth_weekday(y1, 3, 0, 3)
    h.update({sb + D(days=i): "Spring break" for i in range(5)})
    h[last_weekday(y1, 5, 0)] = "Memorial Day"
    return h


PD = {
    "2023-24": {"CPP": ["2023-09-22", "2023-11-03", "2024-02-02", "2024-04-12"],
                "RBA": ["2023-09-29", "2023-11-10", "2024-02-09", "2024-04-19"],
                "MVH": ["2023-09-22", "2023-11-17", "2024-02-02", "2024-04-26"],
                "SHC": ["2023-10-06", "2023-11-03", "2024-02-16", "2024-04-12"]},
    "2024-25": {"CPP": ["2024-09-20", "2024-11-08", "2025-01-31", "2025-04-11"],
                "RBA": ["2024-09-27", "2024-11-01", "2025-02-07", "2025-04-18"],
                "MVH": ["2024-09-20", "2024-11-15", "2025-01-31", "2025-04-25"],
                "SHC": ["2024-10-04", "2024-11-08", "2025-02-14", "2025-04-11"]},
    "2025-26": {"CPP": ["2025-09-19", "2025-11-07", "2026-01-30", "2026-04-10"],
                "RBA": ["2025-09-26", "2025-11-14", "2026-02-06", "2026-04-17"],
                "MVH": ["2025-09-19", "2025-11-21", "2026-01-30", "2026-04-24"],
                "SHC": ["2025-10-03", "2025-11-07", "2026-02-13", "2026-04-10"]},
    "2026-27": {"CPP": ["2026-09-18", "2026-11-06", "2027-01-29", "2027-04-09"],
                "RBA": ["2026-09-25", "2026-11-13", "2027-02-05", "2027-04-16"],
                "MVH": ["2026-09-18", "2026-11-20", "2027-01-29", "2027-04-23"],
                "SHC": ["2026-10-02", "2026-11-06", "2027-02-12", "2027-04-09"]},
}
SNOW = {"2024-25": {"CPP": ["2025-02-12"], "RBA": ["2025-02-12"]},
        "2026-27": {"MVH": ["2026-10-27"], "SHC": ["2026-10-27"]}}


def calendars():
    """cal[(year, school)] = instructional dates; kinds[(year, school)][date] = the day's kind for the shipped
    calendar (instructional, a holiday, a non-student day, a weather closure)."""
    cal, kinds = {}, {}
    for label, first, fall_end, spring_start, last in P.YEARS:
        hol = holidays(first, last)
        for s in P.SCHOOLS:
            pd = {dt.date.fromisoformat(x) for x in PD[label][s]}
            snow = {dt.date.fromisoformat(x) for x in SNOW.get(label, {}).get(s, [])}
            days, k = [], {}
            d = first
            while d <= last:
                if d.weekday() < 5:
                    if fall_end < d < spring_start:
                        k[d] = "Winter break"
                    elif d in hol:
                        k[d] = hol[d]
                    elif d in pd:
                        k[d] = "Non-student day"
                    elif d in snow:
                        k[d] = "Weather closure"
                    else:
                        k[d] = "Instructional"
                        days.append(d)
                d += D(days=1)
            cal[(label, s)] = days
            kinds[(label, s)] = k
    return cal, kinds


FIRST = ["James", "Mia", "Noah", "Sofia", "Liam", "Emma", "Mateo", "Ava", "Elijah", "Isabella", "Lucas", "Camila",
         "Ethan", "Luna", "Daniel", "Aria", "Diego", "Layla", "Henry", "Valeria", "Owen", "Nora", "Gabriel", "Elena",
         "Isaac", "Ximena", "Wyatt", "Maya", "Julian", "Zoe", "Adrian", "Leah", "Andres", "Hazel", "Caleb", "Paisley",
         "Josiah", "Natalia", "Miles", "Aubrey", "Ezra", "Brooklyn", "Jayden", "Savannah", "Isaiah", "Kinsley",
         "Gianna", "Roman", "Alina", "Xavier", "Daisy", "Kai", "Esmeralda", "Jonah", "Ruby", "Elias", "Jade", "Damian",
         "Iris", "Cristian", "Lyla", "Rosalie", "Emiliano", "Talia", "Dominic", "Serenity", "Yaretzi", "Joaquin",
         "Amara", "Santiago", "Nevaeh", "Bryson", "Itzel", "Rowan", "Abril", "Tristan", "Jimena", "Uriel", "Lucia"]
LAST = ["Garcia", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Rodriguez", "Sanchez", "Ramirez", "Torres", "Rivera",
        "Gomez", "Diaz", "Cruz", "Morales", "Reyes", "Gutierrez", "Ortiz", "Chavez", "Ruiz", "Jimenez", "Mendoza",
        "Alvarez", "Castillo", "Romero", "Herrera", "Medina", "Aguilar", "Vargas", "Castro", "Johnson", "Williams",
        "Brown", "Jones", "Miller", "Davis", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
        "Lee", "Thompson", "White", "Harris", "Clark", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
        "Wright", "Scott", "Green", "Baker", "Adams", "Nelson", "Hill", "Campbell", "Mitchell", "Nguyen", "Tran",
        "Pham", "Kim", "Patel", "Yazzie", "Begay", "Archuleta", "Valdez", "Trujillo", "Montoya", "Gallegos",
        "Lucero", "Vigil", "Maestas", "Sandoval", "Salazar", "Espinoza", "Baca", "Duran", "Padilla", "Quintana"]


class Student:
    __slots__ = ("sid", "first", "last", "dob", "z", "a", "ill", "grade0", "year0")


def build(seed=None):
    rng = np.random.default_rng(P.SEED if seed is None else seed)
    cal, kinds = calendars()
    W = dict(cal=cal, kinds=kinds, students={}, years={})
    seq = [4420000117]

    def new_student(grade, label):
        s = Student()
        seq[0] += int(rng.integers(3, 41))
        s.sid = "%010d" % seq[0]
        s.first = FIRST[int(rng.integers(len(FIRST)))]
        s.last = LAST[int(rng.integers(len(LAST)))]
        by = int(label[:4]) - 14 - (grade - 9)
        s.dob = dt.date(by, 1, 1) + D(days=int(rng.integers(0, 365)) + 243 * (rng.random() < 0.5))
        s.z, s.a, s.ill = float(rng.normal()), float(rng.normal()), float(rng.gamma(P.ILL_K, 1.0 / P.ILL_K))
        s.grade0, s.year0 = grade, label
        W["students"][s.sid] = s
        return s

    roll = []
    for sc in P.SCHOOLS:
        n = int(2650 * P.SHARE[sc])
        for g in P.GRADES:
            for _ in range(int(n * {9: 0.29, 10: 0.26, 11: 0.24, 12: 0.21}[g])):
                roll.append((new_student(g, "2023-24").sid, sc, g))
    for yi, label in enumerate(YEAR_LABELS):
        if yi > 0:
            prev = W["years"][YEAR_LABELS[yi - 1]]
            nxt = []
            for sid, sc, g in roll:
                r = prev[sid]
                if r["out"] in ("grad", "left", "xfer_out"):
                    continue
                st = W["students"][sid]
                st.z = 0.8 * st.z + 0.6 * float(rng.normal())
                nxt.append((sid, r["school_end"], min(12, g + (0 if rng.random() < 0.04 else 1))))
            for sc in P.SCHOOLS:
                for _ in range(int(2650 * P.SHARE[sc] * 0.268)):
                    nxt.append((new_student(9, label).sid, sc, 9))
                for _ in range(int(2650 * P.SHARE[sc] * 0.035)):
                    g = int(rng.choice([10, 11, 12], p=[0.45, 0.35, 0.20]))
                    nxt.append((new_student(g, label).sid, sc, g))
            roll = nxt
        W["years"][label] = {}
        simulate_year(W, rng, yi, roll)
    return W


def semester(rng, st, days, texts, n_long=0):
    """{date: (portion, code)} over the student's instructional days, and the runs placed (start, length)."""
    n = len(days)
    out, runs = {}, []
    if n == 0:
        return out, runs
    p_sc = min(P.P_SC0 * np.exp(-0.45 * st.z) * st.ill * (P.TEXT_FACTOR if texts else 1.0), P.PSC_CAP)
    lam = P.LAM0 * np.exp(-0.75 * st.z)
    Ls = [(P.LONG_MIN + int(rng.geometric(P.LONG_P)) - 1, P.LONG_UX) for _ in range(n_long)]
    Ls += [(P.RUN_MIN + int(rng.geometric(P.RUN_P)) - 1, 0.72) for _ in range(int(rng.poisson(lam)))]
    for L, ux in Ls:
        if L >= n - 4:
            continue
        for _try in range(6):
            s0 = int(rng.integers(0, n - L))
            if not any(days[i] in out for i in range(max(0, s0 - 1), min(n, s0 + L + 1))):
                break
        else:
            continue
        code = "UX" if rng.random() < ux else "EX"
        for i in range(s0, s0 + L):
            out[days[i]] = ("FULL", code)
        runs.append((days[s0], L))
    i = 0
    while i < n:
        if days[i] in out or rng.random() >= p_sc:
            i += 1
            continue
        # an episode: a single day (often part of a day), or two to four whole days
        u, v = rng.random(), rng.random()
        k = 1 if u < 0.60 else (2 if u < 0.86 else (3 if u < 0.97 else 4))
        code = "EX" if v < 0.55 else ("UX" if v < 0.90 else "MED")
        for j in range(i, min(n, i + k)):
            if days[j] in out:
                break
            if k == 1:
                x = rng.random()
                por = "FULL" if x < 0.58 else ("AM" if x < 0.80 else "PM")
            else:
                por = "FULL"
            out[days[j]] = (por, code)
        i += k + 1
    return out, runs


def fails(rng, st, nruns):
    p = 1 / (1 + np.exp(-(-2.55 - 0.9 * st.a - 0.25 * st.z + 0.30 * nruns)))
    return int(rng.binomial(7, p))


def incidents(rng, st, days):
    out = []
    for _ in range(int(rng.poisson(0.33 * np.exp(-0.6 * st.z)))):
        u = rng.random()
        cons = "OSS" if u < 0.24 else ("ISS" if u < 0.55 else "DET")
        n = int(rng.choice([1, 2, 3], p=[0.45, 0.35, 0.20])) if cons == "OSS" else (1 if cons == "ISS" else 0)
        out.append((days[int(rng.integers(len(days)))], cons, n))
    return sorted(out)


def simulate_year(W, rng, yi, roll):
    label, first, fall_end, spring_start, last = P.YEARS[yi]
    cur = label == P.CUR
    cal = W["cal"]
    for sid, school, grade in roll:
        st = W["students"][sid]
        fall0 = [d for d in cal[(label, school)] if d <= fall_end]
        entry = first
        if st.year0 == label and st.grade0 != 9 and rng.random() < 0.55:
            entry = fall0[int(rng.integers(3, 40))]
        # the fall's enrolment records: (school, start, end); a move to another of the network's schools, or a
        # withdrawal and return to the same school, opens a second record
        recs = [[school, entry, None]]
        u = rng.random()
        if u < 0.014:
            ix = [i for i, d in enumerate(fall0) if d > entry]
            k = ix[int(rng.integers(15, len(ix) - 15))]
            other = [x for x in P.SCHOOLS if x != school][int(rng.integers(3))]
            nxt = next(d for d in cal[(label, other)] if d > fall0[k])
            recs = [[school, entry, fall0[k]], [other, nxt, None]]
        elif u < 0.024:
            ix = [i for i, d in enumerate(fall0) if d > entry]
            k = ix[int(rng.integers(10, len(ix) - 30))]
            back = fall0[k + int(rng.integers(9, 22))]
            recs = [[school, entry, fall0[k]], [school, back, None]]
        fall_days = []          # (date, school) the student is enrolled on, in the fall
        for sc, a, b in recs:
            for d in cal[(label, sc)]:
                if d <= fall_end and d >= a and (b is None or d <= b):
                    fall_days.append((d, sc))
        dates = [d for d, _ in fall_days]
        disp = bool(cur and rng.random() < P.DISP_SHARE * P.DISP_SCHOOL[school] * np.exp(-P.DISP_Z * st.z) /
                    np.exp(P.DISP_Z ** 2 / 2))
        ab, runs = semester(rng, st, dates, cur, 1 + int(rng.random() < P.DISP_LAM) if disp else 0)
        nf = fails(rng, st, len(runs))
        inc = incidents(rng, st, dates)
        day_absent = sum(1 for d, (por, c) in ab.items() if por != "PM")
        rate = day_absent / max(1, len(dates))
        rec = dict(school=school, grade=grade, recs=recs, fall_days=fall_days, fall_ab=ab, runs=runs, fails=nf, disp=disp,
                   inc=inc, rate=rate, out=None, exit_day=None, school_end=recs[-1][0], spring_ab={}, spring_inc=[],
                   spring_fails=0, p=None)
        # a few leave in the fall
        if rng.random() < 1 / (1 + np.exp(-(-4.9 - 0.7 * st.z))):
            rec["out"] = "left"
            ld = [d for d in dates if d > dates[0]]
            rec["exit_day"] = ld[int(rng.integers(len(ld) // 3, len(ld)))] if ld else dates[-1]
        else:
            logit = (P.B0 + P.B_RUN * min(len(runs), 1) + P.B_RUN2 * max(0, min(len(runs), 3) - 1) + 0.40 * min(nf, 4) + 0.10 * min(len(inc), 4) + 0.3 * rate
                     + {9: 0.15, 10: 0.10, 11: 0.0, 12: -0.55}[grade])
            rec["p"] = 1 / (1 + np.exp(-logit))
            if cur:
                rec["out"] = "on_roll"
            else:
                sch = rec["school_end"]
                spring = [d for d in cal[(label, sch)] if d >= spring_start]
                if rng.random() < rec["p"]:
                    rec["out"] = "left"
                    rec["exit_day"] = spring[int(rng.integers(len(spring)))]
                else:
                    rec["out"] = "grad" if grade == 12 and rng.random() < 0.985 else "stay"
                    if rec["out"] == "stay" and rng.random() < 0.035:
                        rec["out"] = "xfer_out"
                sp = [d for d in spring if rec["exit_day"] is None or d <= rec["exit_day"]]
                rec["spring_ab"], _ = semester(rng, st, sp, False)
                rec["spring_inc"] = incidents(rng, st, sp) if sp else []
                rec["spring_fails"] = fails(rng, st, 0)
                rec["spring_days"] = [(d, sch) for d in sp]
        if rec["out"] == "left" and rec["exit_day"] is not None and rec["exit_day"] <= fall_end:
            # trim the fall's records at the fall exit
            rec["recs"][-1][2] = rec["exit_day"]
        W["years"][label][sid] = rec

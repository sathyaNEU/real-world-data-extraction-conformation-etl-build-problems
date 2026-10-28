"""task270 records: the rows every shipped file carries, cut from the world.

Death registrations (the registry's extract and the other states' notifications), the 2021 census counts as a
TableBuilder export, the ABS estimated resident population by area and five-year group and the state's by single
year, the ASGS correspondence, the after-hours service's 2026 attendances, and the two published tables beside them.
Every attribute a person carries into a record is drawn once per person in a fixed order, so tuning an area's
mortality level moves which deaths fall in a year and nothing else."""
from __future__ import annotations

import datetime as dt
import hashlib
import math

import numpy as np

import common as K
import world as W

D = W.from_days

CAUSES_85 = [("F03", 13.0), ("G30", 6.0), ("I25", 10.5), ("I21", 3.5), ("I64", 5.5), ("I63", 2.0), ("I50", 4.5),
             ("J44", 4.0), ("J18", 3.2), ("C34", 2.6), ("C18", 1.8), ("C61", 2.4), ("C50", 1.2), ("E11", 2.6),
             ("N18", 2.4), ("N39", 1.4), ("I48", 2.2), ("I35", 1.4), ("G20", 1.8), ("A41", 1.5), ("K92", 0.8),
             ("I10", 1.6), ("U07", 1.4), ("W19", 2.0), ("R54", 1.5), ("C80", 1.2), ("J69", 0.9), ("I70", 0.8)]
CAUSES_60 = [("I25", 11.0), ("C34", 8.5), ("I21", 4.5), ("C18", 3.5), ("C25", 3.2), ("C50", 3.0), ("C61", 2.6),
             ("J44", 6.0), ("I64", 3.8), ("E11", 3.2), ("F03", 3.5), ("G30", 1.8), ("I50", 2.4), ("C80", 2.4),
             ("C22", 1.6), ("C71", 1.2), ("N18", 1.8), ("K70", 1.4), ("G12", 0.8), ("I48", 1.2), ("J18", 1.4),
             ("A41", 1.2), ("U07", 0.8), ("W19", 0.8), ("X70", 0.6), ("V43", 0.5), ("C92", 0.9), ("C85", 0.9)]
CAUSES_YOUNG = [("X70", 6.0), ("X42", 5.0), ("V43", 5.0), ("C50", 4.0), ("I21", 3.0), ("I25", 3.0), ("C34", 2.0),
                ("C71", 2.0), ("K70", 2.0), ("W69", 1.5), ("C18", 2.0), ("P07", 1.5), ("Q24", 1.0), ("G40", 1.2),
                ("E10", 0.8), ("X80", 0.8), ("V89", 1.5), ("I42", 0.8), ("C92", 1.0), ("R99", 1.0)]
CORONIAL = {"W19", "X70", "X42", "V43", "W69", "X80", "V89", "R99"}


def _holidays():
    """New South Wales public holidays the registry is closed on, 2015 to 2027."""
    import datetime as _dt
    easter = {2015: (4, 5), 2016: (3, 27), 2017: (4, 16), 2018: (4, 1), 2019: (4, 21), 2020: (4, 12), 2021: (4, 4),
              2022: (4, 17), 2023: (4, 9), 2024: (3, 31), 2025: (4, 20), 2026: (4, 5), 2027: (3, 28)}
    out = set()
    for y in range(2015, 2028):
        e = _dt.date(y, *easter[y])
        out |= {_dt.date(y, 1, 1), _dt.date(y, 1, 26), e - _dt.timedelta(days=2), e + _dt.timedelta(days=1),
                _dt.date(y, 4, 25), _dt.date(y, 12, 25), _dt.date(y, 12, 26)}
        jun = _dt.date(y, 6, 1)
        out.add(jun + _dt.timedelta(days=(0 - jun.weekday()) % 7 + 7))     # the King's or Queen's Birthday
        octo = _dt.date(y, 10, 1)
        out.add(octo + _dt.timedelta(days=(0 - octo.weekday()) % 7))        # Labour Day
    return out


HOLIDAYS = _holidays()


def business_day(d):
    """The registry registers on working days: a date that falls on a weekend or a public holiday moves on."""
    while d.weekday() >= 5 or d in HOLIDAYS:
        d += dt.timedelta(days=1)
    return d


def _pick(g, table, n):
    codes = [c for c, _ in table]
    w = np.array([x for _, x in table], dtype=float)
    return np.array(codes)[g.choice(len(codes), n, p=w / w.sum())]


def person_attributes(P, A):
    """Per person, drawn once in the person order: place of death, cause, coroner, registration lag, interstate
    registration, a missing date of birth, a census miss, and a uniform for the after-hours draws."""
    n = len(P["dob"])
    g = K.rng("attrs")
    P["u_place"] = g.random(n)
    P["u_cause85"] = _pick(g, CAUSES_85, n)
    P["u_cause60"] = _pick(g, CAUSES_60, n)
    P["u_lag"] = g.gamma(2.0, 1.0, n)
    P["u_lag2"] = g.random(n)
    P["u_inter"] = g.random(n)
    P["u_dobmiss"] = g.random(n)
    P["u_census"] = g.random(n)
    P["u_tod"] = g.random(n)
    P["u_seq"] = g.random(n)
    inter = np.array([a.interstate for a in A])[P["area"]]
    P["interstate"] = P["u_inter"] < inter
    return P


def death_records(P, A):
    """One record per resident's death 2016 to 30 June 2027 (persons born by 1966), with its registration."""
    out = []
    has = (P["death"] >= 0)
    for i in np.where(has)[0]:
        a = A[P["area"][i]]
        dod = D(P["death"][i])
        dob = D(P["dob"][i])
        age = K.age_on(dob, dod)
        racf = age >= P["racf_age"][i]
        cause = P["u_cause85"][i] if age >= 85 else P["u_cause60"][i]
        coronial = cause in CORONIAL or (P["u_lag2"][i] < 0.012)
        u = P["u_place"][i]
        if racf:
            place = "Residential aged care facility" if u < 0.62 else ("Hospital" if u < 0.95 else "Other")
        else:
            place = "Hospital" if u < 0.57 else ("Private dwelling" if u < 0.88 else "Other")
        if coronial:
            lag = 24 + int(P["u_lag"][i] * (30 if age >= 85 else 55))
            lag = min(lag, 150) if age >= 85 else lag
        else:
            lag = 2 + int(P["u_lag"][i] * 5.5)
        out.append(dict(person=int(i), area=a.name, sa2=a.sa2[P["sa2"][i]], sex="M" if P["sex"][i] else "F", dob=dob,
                        dod=dod, age=age, place=place, cause=cause, coronial=coronial,
                        reg=business_day(dod + dt.timedelta(days=lag)),
                        interstate=bool(P["interstate"][i]), dob_missing=bool(P["u_dobmiss"][i] < 0.0025),
                        u_seq=float(P["u_seq"][i]), u_tod=float(P["u_tod"][i])))
    return out


def young_deaths(A, Y):
    """Deaths of residents born from 1967, by area, sex, single age and year, with dates drawn in the year."""
    out = []
    for a in A:
        for sex in ("F", "M"):
            g = K.rng("ydeath", a.name, sex)
            for year in range(2016, 2028):
                pop = W.young_pop(Y, a.name, sex, min(year, 2026))
                rate = W.young_rate(np.arange(116), sex)
                frac = 0.5 if year == 2027 else 1.0
                lam = pop * rate * frac
                for age in np.where(lam > 0)[0]:
                    k = int(g.poisson(lam[age]))
                    for _ in range(k):
                        doy = int(g.integers(0, 181 if year == 2027 else 365))
                        dod = dt.date(year, 1, 1) + dt.timedelta(days=doy)
                        dob = dod - dt.timedelta(days=int(age * 365.25 + g.integers(0, 365)))
                        if dob.year < 1967:
                            dob = dt.date(1967, 1, 1) + dt.timedelta(days=int(g.integers(0, 300)))
                        agex = K.age_on(dob, dod)
                        cause = _pick(g, CAUSES_YOUNG, 1)[0]
                        coronial = cause in CORONIAL or g.random() < 0.15
                        lag = 30 + int(g.gamma(2.0, 60.0)) if coronial else 2 + int(g.gamma(2.0, 5.5))
                        u = g.random()
                        place = "Hospital" if u < 0.55 else ("Private dwelling" if u < 0.80 else "Other")
                        out.append(dict(person=-1, area=a.name, sa2=a.sa2[int(g.choice(len(a.sa2), p=a.w_young))],
                                        sex=sex, dob=dob, dod=dod, age=agex, place=place, cause=cause,
                                        coronial=coronial, reg=business_day(dod + dt.timedelta(days=lag)),
                                        interstate=bool(g.random() < a.interstate * 1.5), dob_missing=False,
                                        u_seq=float(g.random()), u_tod=float(g.random())))
    return out


def tail_2015(A, recs):
    """Deaths in November and December 2015 registered in January 2016: the extract starts at 1 January 2016
    registrations, so these come in with it."""
    out = []
    g = K.rng("tail2015")
    jan = [r for r in recs if r["dod"].year == 2016 and r["dod"].month == 1 and not r["interstate"]]
    for r in jan[: int(len(jan) * 0.42)]:
        shift = int(g.integers(5, 40))
        dod = dt.date(2015, 12, 31) - dt.timedelta(days=int(g.integers(0, 25)))
        dob = r["dob"] - dt.timedelta(days=shift)
        reg = business_day(dt.date(2016, 1, 1) + dt.timedelta(days=int(g.integers(0, 20))))
        if reg <= dod:
            continue
        out.append(dict(r, person=-2, dod=dod, dob=dob, age=K.age_on(dob, dod), reg=reg, u_seq=float(g.random())))
    return out


def lga_at_registration(area, sa2_name, reg):
    """The LGA the registry coded at registration: Thistlebank was Merriwold's until the 2023 boundary adjustment."""
    if sa2_name == K.MOVED_SA2 and reg < K.BOUNDARY_DATE:
        return K.MOVED_FROM
    return area


def reg_numbers(recs):
    """New South Wales registration numbers: the registration year and the statewide sequence in that year. The
    region registers about one death in eight of the state's, so between two of its registrations the sequence moves
    on by the state's others, in the order the registry keyed them."""
    by_year = {}
    for r in recs:
        by_year.setdefault(r["reg"].year, []).append(r)
    out = {}
    for year, regs in by_year.items():
        g = K.rng("regno", str(year))
        regs.sort(key=lambda r: (r["reg"], r["u_seq"]))
        seq = int(g.integers(1, 30))
        for r in regs:
            out[id(r)] = "%d/%06d" % (year, seq)
            seq += 1 + int(g.geometric(1 / 7.4))
    return out


def extract_rows(recs):
    """The registry's extract: registrations from 1 January 2016 to 30 June 2027 of the region's residents' deaths
    registered in New South Wales."""
    rows = []
    keep = [r for r in recs if not (r["interstate"] or r["reg"] > K.EXTRACT_TO or r["reg"] < dt.date(2016, 1, 1))]
    numbers = reg_numbers(keep)
    for r in keep:
        lga = lga_at_registration(r["area"], r["sa2"][1], r["reg"])
        rows.append((r["reg"], [numbers[id(r)], r["reg"].isoformat(), r["dod"].isoformat(),
                                "" if r["dob_missing"] else r["dob"].isoformat(), str(r["age"]), r["sex"],
                                r["sa2"][0], r["sa2"][1], K.AREA_CODE[lga], lga, r["place"],
                                "Y" if r["coronial"] else "N", r["cause"]]))
    rows.sort(key=lambda x: (x[0], x[1][0]))
    return [r for _, r in rows]


INTERSTATE_STATE = {"Windermoor": ["VIC"], "Wolfram Ranges": ["VIC"], "Coldwater Plains": ["VIC", "SA"],
                    "Merriwold": ["VIC", "ACT"], "Cobbleton": ["ACT", "VIC"], "Bannockvale": ["ACT", "QLD"],
                    "Spraymouth": ["QLD"], "Gannetmouth": ["QLD"], "Saltwick Shoals": ["QLD"], "Dunesford": ["QLD"],
                    "Kestrelmoor": ["ACT"], "Mallowmere": ["ACT"]}


def interstate_rows(recs):
    """Deaths of the region's residents registered in another state, as the ABS supplies them to the network:
    registrations to 30 June 2027."""
    rows = []
    g = K.rng("interstate")
    for r in recs:
        if not r["interstate"] or r["reg"] > K.EXTRACT_TO or r["reg"] < dt.date(2016, 1, 1):
            continue
        st = INTERSTATE_STATE[r["area"]][int(g.integers(0, len(INTERSTATE_STATE[r["area"]])))]
        width = {"VIC": 6, "QLD": 6, "SA": 5, "ACT": 4}[st]
        top = {"VIC": 42000, "QLD": 36000, "SA": 15000, "ACT": 2600}[st]
        rn = "%d/%0*d" % (r["reg"].year, width, int(g.integers(1, top)))
        rows.append((r["reg"], [st, rn, r["reg"].isoformat(), r["dod"].isoformat(), r["dob"].isoformat(), r["sex"],
                                r["age"], r["sa2"][0], r["sa2"][1]]))
    rows.sort(key=lambda x: (x[0], x[1][1]))
    return [r for _, r in rows]


# ------------------------------------------------------------------------------------------------- populations
def erp(P, A, Y):
    """Estimated resident population at 30 June 2016 to 2026 by area, sex and single age (0 to 115)."""
    out = {}
    for y in range(2016, 2027):
        day = dt.date(y, 6, 30)
        on = W.alive_on(P, day)
        ag = np.minimum(W.ages_on_fast(P, day), 115)
        for a in A:
            for s, sx in (("F", 0), ("M", 1)):
                sel = on & (P["area"] == a.i) & (P["sex"] == sx)
                v = np.bincount(ag[sel], minlength=116).astype(float)
                v += W.young_pop(Y, a.name, s, y)
                out[(y, a.name, s)] = np.round(v).astype(int)
    return out


def census_counts(P, A, Y):
    """The 2021 census counts by SA2 of usual residence, sex and single age, as TableBuilder releases them: people
    missed on census night are not in it, and every cell is randomly adjusted (small cells most)."""
    on = W.alive_on(P, K.CENSUS) & (P["u_census"] > 0.005)
    ag = np.minimum(W.ages_on_fast(P, K.CENSUS), 115)
    out = {}
    for a in A:
        for s, sx in (("F", 0), ("M", 1)):
            g = K.rng("census_young", a.name, s)
            young = W.young_pop(Y, a.name, s, 2021, on_census=True)
            ysa2 = np.zeros((len(a.sa2), 116))
            for age in range(116):
                k = int(round(young[age] * (0.975 if 15 <= age <= 34 else 0.99)))
                if k:
                    ysa2[:, age] = g.multinomial(k, a.w_young)
            for j, (code, name) in enumerate(a.sa2):
                sel = on & (P["area"] == a.i) & (P["sex"] == sx) & (P["sa2"] == j)
                v = np.bincount(ag[sel], minlength=116).astype(int) + ysa2[j].astype(int)
                out[(code, name, s)] = perturb(v, code, s)
    return out


def perturb(v, code, sex):
    """TableBuilder's cell adjustment: a small change keyed to the cell, never below zero."""
    out = v.copy()
    for age in range(len(v)):
        if v[age] == 0:
            continue
        h = int(hashlib.sha256(("%s|%s|%d|%d" % (code, sex, age, v[age])).encode()).hexdigest()[:8], 16)
        d = [-1, 0, 0, 0, 1][h % 5] if v[age] >= 3 else [-1, 0, 0, 1][h % 4]
        out[age] = max(0, v[age] + d)
    return out


def nsw_single_year():
    """New South Wales estimated resident population by single year of age (to 100 and over) and sex, 30 June 2016 to
    2026: the younger ages on the state's recent births and arrivals, the older ages on cohorts of the state's births
    surviving at its own old-age mortality."""
    out = {}
    for y in range(2016, 2027):
        for s in ("F", "M"):
            sexf = W.SEX_F[s]
            g = K.rng("nsw", y, s)
            v = np.zeros(101)
            for age in range(101):
                c = y - age
                if age < 60:
                    shape = (1.0 + 0.15 * (59 - age) / 59 + 0.08 * np.exp(-0.5 * ((age - 31) / 8.0) ** 2)
                             - 0.05 * np.exp(-0.5 * ((age - 18) / 4) ** 2))
                    v[age] = 42300 * (1.0 + 0.0085 * (y - 2016)) * shape * (1.025 if s == "M" else 0.975) \
                        * (1 + g.normal(0, 0.006))
                else:
                    v[age] = 34600 * float(W.nat_index(c)) * W.survival_hist(W.HIST_LEVEL, sexf, c, age + 0.5) \
                        * (0.99 if s == "M" else 1.01)
            tail = 0.0
            for age in range(101, 112):
                c = y - age
                tail += 34600 * float(W.nat_index(c)) * W.survival_hist(W.HIST_LEVEL, sexf, c, age + 0.5)
            v[100] += tail
            out[(y, s)] = np.round(v).astype(int)
    return out


# ------------------------------------------------------------------------------------------------- after hours
def _after_hours_time(g, day):
    """An arrival time on a day the service works out of hours: weekday evenings and nights, weekends and public
    holidays all day."""
    wk = day.weekday()
    hol = day in K.NSW_HOLIDAYS_2026
    if wk >= 5 or hol:
        hrs = np.arange(24)
        w = np.array([3, 2, 2, 1, 1, 1, 2, 3, 5, 6, 6, 6, 5, 5, 5, 5, 6, 7, 8, 8, 7, 6, 5, 4], dtype=float)
    else:
        hrs = np.array([18, 19, 20, 21, 22, 23, 0, 1, 2, 3, 4, 5, 6, 7])
        w = np.array([9, 10, 10, 9, 7, 5, 4, 3, 2, 2, 2, 2, 3, 3], dtype=float)
    h = int(hrs[g.choice(len(hrs), p=w / w.sum())])
    t = dt.datetime(day.year, day.month, day.day, h, int(g.integers(0, 60)), int(g.integers(0, 60)))
    if wk < 5 and not hol and h < 8:
        t += dt.timedelta(days=1)      # a weekday night's small hours fall on the next morning
    return t


def after_hours(P, A, recs):
    """The service's 2026 attendances: one row per clinician attending; a supervising doctor and a registrar who go
    together are two rows on one case, and a clinician who goes back to the same case later that night is a further
    row on it. On 1 July 2026 the service moved to a new clinical system: clients carried over were given new keys,
    with the old key kept in the new system's external identifier."""
    g = K.rng("afterhours")
    start, end = dt.date(2026, 1, 1), dt.date(2026, 12, 31)
    d0, d1 = W.days(start), W.days(end)
    res = (P["entry"] <= d1) & ((P["death"] < 0) | (P["death"] >= d0)) & ((P["gone"] < 0) | (P["gone"] >= d0))
    death_place = {r["person"]: r["place"] for r in recs if r["person"] >= 0}
    visits = []   # (person, arrival datetime, kind)
    for i in np.where(res)[0]:
        lo = max(d0, int(P["entry"][i]))
        hi = d1
        if P["death"][i] >= 0:
            hi = min(hi, int(P["death"][i]))
        if P["gone"][i] >= 0:
            hi = min(hi, int(P["gone"][i]))
        if hi < lo:
            continue
        gi = K.rng("ah_person", int(i))
        mid = D((lo + hi) // 2)
        age = K.age_on(D(int(P["dob"][i])), mid)
        racf = age >= P["racf_age"][i]
        if age < 75:
            lam = 0.025
        elif age < 85:
            lam = 0.30 if racf else 0.07
        elif age < 90:
            lam = 0.40 if racf else 0.16
        else:
            lam = 0.48 if racf else 0.24
        k = int(gi.poisson(lam * (hi - lo + 1) / 365.25))
        for _ in range(k):
            visits.append((int(i), _after_hours_time(gi, D(int(gi.integers(lo, hi + 1)))), "visit"))
        if P["death"][i] >= 0 and d0 <= P["death"][i] <= W.days(dt.date(2027, 2, 15)):
            dd = int(P["death"][i])
            k = int(gi.poisson(0.7))
            for _ in range(k):
                day = dd - int(gi.integers(0, 40))
                if d0 <= day <= d1 and day >= lo:
                    visits.append((int(i), _after_hours_time(gi, D(day)), "palliative"))
            if dd <= d1 and death_place.get(int(i)) in ("Residential aged care facility", "Private dwelling") \
                    and gi.random() < 0.55:
                t = _after_hours_time(gi, D(dd))
                if t.date() == D(dd) or t.date() == D(dd) + dt.timedelta(days=1):
                    visits.append((int(i), t, "verification"))
    return visits


def younger_clients(A, E):
    """Clients under 60 and visitors from outside the region: synthetic people the person file does not follow, drawn
    in proportion to each area's residents under 60 at 30 June 2026."""
    g = K.rng("ah_young")
    out = []
    under60 = np.array([sum(float(E[(2026, a.name, s)][:60].sum()) for s in ("F", "M")) for a in A])
    k = int(under60.sum() * 0.018)
    for j in range(k):
        a = A[int(g.choice(len(A), p=under60 / under60.sum()))]
        age = int(g.choice(60, p=_young_visit_age()))
        past = int(g.integers(0, 365))          # days since the last birthday on the day of the visit
        sa2 = a.sa2[int(g.choice(len(a.sa2), p=a.w_young))]
        sex = "F" if g.random() < 0.52 else "M"
        day = dt.date(2026, 1, 1) + dt.timedelta(days=int(g.integers(0, 365)))
        dob = day - dt.timedelta(days=int(age * 365.25) + past)
        out.append(dict(key=("Y", j), dob=dob, sex=sex, sa2=sa2[0], racf=False, day=day))
    return out


def _young_visit_age():
    a = np.arange(60)
    w = np.where(a < 5, 3.0, np.where(a < 15, 1.4, np.where(a < 30, 0.9, 1.1)))
    return w / w.sum()


CLINICIANS = ([("MP%04d" % (1100 + 37 * j), "General practitioner") for j in range(24)]
              + [("MP%04d" % (2100 + 41 * j), "GP registrar") for j in range(8)]
              + [("NP%04d" % (3100 + 29 * j), "Nurse practitioner") for j in range(6)])
OTHER_SA2 = ["108011131", "108021157", "108031161", "113011256", "113021261", "115011290", "115021297", "128011531",
             "128021536", "128021538", "101031015", "101021611"]


def _stamp(t):
    return t.strftime("%Y-%m-%dT%H:%M:%S") + K.offset_for(t)


def attendance_rows(P, A, visits, young):
    """The PHN's 2026 file of the service's attendances: January to June from the old system's export, July to
    December from the new system's, one row per clinician attending."""
    g = K.rng("attend")
    occ = []
    for (i, t, kind) in visits:
        dob = D(int(P["dob"][i]))
        a = A[P["area"][i]]
        age = K.age_on(dob, t.date())
        occ.append(dict(client=("P", i), dob=dob, sex="M" if P["sex"][i] else "F", sa2=a.sa2[P["sa2"][i]][0],
                        racf=age >= P["racf_age"][i], t=t, kind=kind))
    for y in young:
        occ.append(dict(client=y["key"], dob=y["dob"], sex=y["sex"], sa2=y["sa2"], racf=False,
                        t=_after_hours_time(K.rng("ah_ytime", y["key"][1]), y["day"]), kind="visit"))
    # holidaymakers and visitors on the coast, mostly in summer
    gv = K.rng("ah_visitors")
    nvis = int(len(occ) * 0.028)
    for j in range(nvis):
        month = int(gv.choice(12, p=np.array([4, 3, 2, 2, 1, 1, 1, 1, 1, 2, 2, 4], float) / 24)) + 1
        day = dt.date(2026, month, 1) + dt.timedelta(days=int(gv.integers(0, 28)))
        age = int(gv.integers(2, 92))
        dob = dt.date(2026 - age, 1, 1) + dt.timedelta(days=int(gv.integers(0, 365)))
        occ.append(dict(client=("V", j), dob=dob, sex="F" if gv.random() < 0.5 else "M",
                        sa2=OTHER_SA2[int(gv.integers(0, len(OTHER_SA2)))], racf=False,
                        t=_after_hours_time(gv, day), kind="visit"))
    occ = [o for o in occ if dt.datetime(2026, 1, 1) <= o["t"] < dt.datetime(2027, 1, 1, 8)]
    occ.sort(key=lambda o: (o["t"], str(o["client"])))
    # client keys: the old system's for anyone it ever registered, the new system's for anyone seen from July
    first_h1 = {}
    seen_h2 = {}
    for o in occ:
        if o["t"] < dt.datetime(2026, 7, 1):
            first_h1.setdefault(o["client"], o["t"])
        else:
            seen_h2.setdefault(o["client"], o["t"])
    old_key, new_key = {}, {}
    gk = K.rng("keys")
    pool = gk.choice(np.arange(10000000, 99999999), len(first_h1) + 2 * len(seen_h2) + 20, replace=False)
    olds = sorted(set(first_h1) | {c for c in seen_h2 if K.rng("prior", str(c)).random() < 0.35},
                  key=lambda c: (first_h1.get(c, dt.datetime(2026, 7, 1)), str(c)))
    for j, c in enumerate(olds):
        old_key[c] = "%08d" % pool[j]
    for j, c in enumerate(sorted(seen_h2, key=lambda c: (seen_h2[c], str(c)))):
        new_key[c] = "%08d" % pool[len(olds) + j]
    rows = []
    n_old = n_new = 0
    case_old = case_new = 0
    new_year = dt.datetime(2027, 1, 1)
    for o in occ:
        h1 = o["t"] < dt.datetime(2026, 7, 1)
        pal = o["kind"] in ("palliative", "verification")
        gs = K.rng("ah_secs", str(o["client"]), o["t"].isoformat())
        t = o["t"]
        if new_year - dt.timedelta(minutes=70) <= t < new_year:     # the year's last calls are seen and left before midnight
            t = t - dt.timedelta(minutes=70)
        req = t - dt.timedelta(minutes=int(g.integers(20, 150)), seconds=int(gs.integers(0, 60)))
        if req.year != t.year:
            req = dt.datetime(t.year, 1, 1, 0, 2) + (t - dt.datetime(t.year, 1, 1)) / 3
        dur = int(g.integers(30, 61)) if o["kind"] == "verification" else int(g.integers(20, 56))
        if h1:
            case_old += 1
            case = "THV-26-%06d" % (case_old * 3 + int(g.integers(0, 3)))
        else:
            case_new += 1
            case = "C26%07d" % (4100000 + case_new * 7 + int(g.integers(0, 7)))
        lead = CLINICIANS[int(g.integers(0, 24))] if g.random() < 0.8 else CLINICIANS[int(g.integers(24, 38))]
        atts = [(t, t + dt.timedelta(minutes=dur, seconds=int(gs.integers(-30, 30))), lead)]
        if g.random() < (0.10 if pal else 0.06):
            second = CLINICIANS[int(g.integers(24, 38))]
            a2 = t + dt.timedelta(minutes=int(g.integers(0, 5)), seconds=int(g.integers(0, 60)))
            atts.append((a2, atts[0][1] + dt.timedelta(minutes=int(g.integers(-4, 6)), seconds=int(gs.integers(0, 60))),
                         second))
        late_june = h1 and t >= dt.datetime(2026, 6, 30, 18)
        late_dec = new_year - dt.timedelta(hours=10) <= t < new_year
        if (not late_june) and (not late_dec) and g.random() < (0.15 if pal else 0.035):
            back = atts[0][1] + dt.timedelta(minutes=int(g.integers(100, 481)))
            who = lead if g.random() < 0.6 else CLINICIANS[int(g.integers(0, 24))]
            atts.append((back + dt.timedelta(seconds=int(gs.integers(0, 60))),
                         back + dt.timedelta(minutes=int(g.integers(15, 40)), seconds=int(gs.integers(0, 60))), who))
        if o["kind"] == "verification":
            outcome = "Life extinct verified"
        else:
            u = g.random()
            outcome = ("Managed at home" if u < 0.78 else "Referred to emergency department" if u < 0.86
                       else "Ambulance transfer" if u < 0.92 else "Referred to own GP")
        for (arr, dep, (cid, role)) in atts:
            age = K.age_on(o["dob"], arr.date())
            if h1:
                n_old += 1
                aid, key, ext = "A%07d" % (2604000 + n_old), old_key[o["client"]], ""
            else:
                n_new += 1
                aid = "AT%08d" % (26100000 + n_new * 3)
                key, ext = new_key[o["client"]], old_key.get(o["client"], "")
            rows.append([aid, case, key, ext, o["dob"].strftime("%Y-%m"), o["sex"], age, o["sa2"],
                         "Residential aged care" if o["racf"] else "Private residence", _stamp(req), _stamp(arr),
                         _stamp(dep), cid, role, outcome])
    rows.sort(key=lambda r: (r[10], r[0]))
    return rows


def falls_rows(A, E):
    """The state's published falls-related injury hospitalisations of people aged 65 and over by area, 2024-25: a
    table the network keeps beside its own data."""
    g = K.rng("falls")
    rows = []
    for a in sorted(A, key=lambda a: a.code):
        pop65 = sum(int(E[(2025, a.name, s)][65:].sum()) for s in ("F", "M"))
        rate = float(g.normal(2380, 260)) * (1.08 if a.type == "coast" else 1.0)
        n = int(round(pop65 * rate / 1e5))
        se = rate / max(np.sqrt(n), 1)
        rows.append([a.code, a.name, n, "%.1f" % rate, "%.1f" % (rate - 1.96 * se), "%.1f" % (rate + 1.96 * se)])
    return rows

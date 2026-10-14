"""The records the asks read, drawn from the world: the regional immunisation register's people and MMR events for
births 1993-2017 (with the GP return lines the immunisation office queried), the national notifiable disease
system's measles cases for the region since 2019 and the reference laboratory's results, and the distractors'
records (the cold-chain stock return and the European monthly counts). One generator per stream, so a change in one
stream never re-rolls another."""
import datetime as dt

import numpy as np

import callsim as CS
import world as W

D = dt.date


def _days(a, b):
    return (b - a).days


def _rand_date(rng, a, b):
    """A uniform date in [a, b]."""
    return a + dt.timedelta(days=int(rng.integers(0, _days(a, b) + 1)))


def _birthday(dob, years):
    return D(dob.year + years, dob.month, dob.day)


# =================================================================================================================
# The register
# =================================================================================================================
def _coverage(y, table):
    for r, v in table.items():
        if y in r:
            return v
    raise KeyError(y)


MMR1_UPTAKE = {1993: .84, 1994: .83, 1995: .82, 1996: .83, 1997: .85, 1998: .88, 1999: .89, 2000: .89, 2001: .90,
               2002: .90, 2003: .91, 2004: .90, 2005: .91, 2006: .92, 2007: .91, 2008: .88, 2009: .84, 2010: .81,
               2011: .82, 2012: .86, 2013: .91, 2014: .92, 2015: .93, 2016: .93, 2017: .94}
MMR2_GIVEN_MMR1 = {1993: .74, 1994: .75, 1995: .72, 1996: .74, 1997: .77, 1998: .84, 1999: .85, 2000: .86, 2001: .87,
                   2002: .87, 2003: .88, 2004: .88, 2005: .89, 2006: .89, 2007: .89, 2008: .86, 2009: .84, 2010: .83,
                   2011: .84, 2012: .86, 2013: .89, 2014: .90, 2015: .90, 2016: .91, 2017: .91}


class Person:
    __slots__ = ("pid", "dob", "sex", "lho", "lho_recorded", "registered", "practice", "born_in_region", "status",
                 "area", "dest", "postcode", "shown_practice")

    def __init__(self, **k):
        for a, b in k.items():
            setattr(self, a, b)


class Event:
    __slots__ = ("eid", "pid", "product", "date", "given_by", "source_ref", "loaded", "kind", "owner")

    def __init__(self, **k):
        for a, b in k.items():
            setattr(self, a, b)


PRODUCTS = [(D(1988, 1, 1), D(1998, 12, 31), ["MMR II", "MMR II"]),
            (D(1999, 1, 1), D(2009, 6, 30), ["MMR II", "Priorix"]),
            (D(2009, 7, 1), D(2027, 12, 31), ["M-M-RVAXPRO", "Priorix"])]


def _product(rng, d):
    for a, b, names in PRODUCTS:
        if a <= d <= b:
            return names[int(rng.random() < 0.38)]
    return "Priorix"


def _person_ids(rng, n):
    """Register numbers: 'OR' plus seven digits, the last a check digit (weights 7, 6, 5, 4, 3, 2 mod 11, 10 as 0)."""
    base = rng.choice(np.arange(200_000, 999_999), size=n, replace=False)
    out = []
    for b in base:
        s = "%06d" % b
        c = sum(int(ch) * w for ch, w in zip(s, (7, 6, 5, 4, 3, 2))) % 11 % 10
        out.append("OR%s%d" % (s, c))
    return out


def _practices(rng):
    """GP practices by area: four-digit practice numbers, weighted to the area's people."""
    areas = list(W.AREA_SHARE_OLD)
    out = {}
    nums = rng.choice(np.arange(1100, 4999), size=W.GP_PRACTICES, replace=False)
    k = 0
    for a in areas:
        n = max(3, int(round(W.GP_PRACTICES * W.AREA_SHARE_OLD[a])))
        out[a] = ["GP%04d" % x for x in nums[k:k + n]]
        k += n
    return out


def register(reg_total):
    """People born 1993-2017 with an active registration on the region's register at 30 June 2027, and their MMR
    events as loaded (GP return lines, school sessions, hospital clinics, pharmacies, records from abroad)."""
    rng = np.random.default_rng(W.SEED + 101)
    rng_dose = np.random.default_rng(W.SEED + 102)
    practices = _practices(rng)
    areas = list(W.AREA_SHARE_OLD)
    area_p = np.array([W.AREA_SHARE_OLD[a] for a in areas])
    area_p = area_p / area_p.sum()
    mover_codes = list(W.MOVER_AREA_WEIGHTS)
    mover_p = np.array([W.MOVER_AREA_WEIGHTS[c] for c in mover_codes], dtype=float)
    mover_p = mover_p / mover_p.sum()
    people = []
    for y in range(1993, 2018):
        age = 2027 - y
        proj = int(reg_total[age])
        n_res = int(round(proj * _coverage(y, W.REGISTER_COVERAGE) * rng.normal(1, 0.006)))
        n_moved = int(round(n_res * _coverage(y, W.MOVED_AWAY_SHARE) * rng.normal(1, 0.06)))
        n_port = int(rng.integers(*W.PORTLAOISE_MOVERS_PER_COHORT_YEAR))
        born_share = 0.80 if y < 2003 else 0.88
        n_trans = int(round(n_res * 0.071 * rng.normal(1, 0.05)))
        n_dead = int(rng.integers(8, 30))
        for kind, n in (("resident", n_res), ("moved", n_moved), ("portlaoise", n_port), ("transferred", n_trans),
                        ("deceased", n_dead)):
            for _ in range(n):
                while True:
                    dob = _rand_date(rng, D(y, 1, 1), D(y, 12, 31))
                    if not (dob.month == 2 and dob.day == 29):
                        break
                sex = "F" if rng.random() < 0.493 else "M"
                born_here = rng.random() < born_share
                if born_here:
                    registered = dob + dt.timedelta(days=int(rng.integers(6, 46)))
                else:
                    registered = _rand_date(rng, _birthday(dob, 1), D(2027, 6, 20))
                area = areas[int(rng.choice(len(areas), p=area_p))]
                practice = practices[area][int(rng.integers(0, len(practices[area])))]
                # the date the address (and with it the local health office) was last set
                lho_recorded = registered
                t = registered
                while True:
                    t = t + dt.timedelta(days=int(rng.exponential(365 * 9)))
                    if t > D(2027, 6, 25):
                        break
                    lho_recorded = t
                if kind == "resident":
                    status = "resident"
                elif kind == "moved":
                    status = "moved"
                    lho_recorded = _rand_date(rng, max(registered, D(2012, 1, 1)), D(2027, 6, 20))
                elif kind == "portlaoise":
                    status = "portlaoise"
                    lho_recorded = _rand_date(rng, D(2024, 7, 12), D(2027, 6, 20))
                else:
                    status = kind
                # C1: nothing recorded within a week of the revision
                if D(2024, 6, 24) <= lho_recorded <= D(2024, 7, 8):
                    lho_recorded = lho_recorded + dt.timedelta(days=15)
                if status == "resident":
                    if area == "LH27":
                        lho = "LH27" if lho_recorded < W.CUTOVER else "LH26"
                    else:
                        lho = area
                elif status == "moved":
                    c = mover_codes[int(rng.choice(len(mover_codes), p=mover_p))]
                    if c == "LH31" and lho_recorded >= W.CUTOVER and rng.random() < 0.45:
                        c = "LH27"    # the new Portlaoise area since July 2024
                        status = "portlaoise"
                    lho = c
                elif status == "portlaoise":
                    lho = "LH27"
                else:
                    lho = mover_codes[int(rng.choice(len(mover_codes), p=mover_p))] if kind == "transferred" else area
                people.append(Person(pid=None, dob=dob, sex=sex, lho=lho, lho_recorded=lho_recorded,
                                     registered=registered, practice=practice, born_in_region=born_here,
                                     status=status, area=area, dest=lho, postcode="", shown_practice=practice))
    ids = _person_ids(rng, len(people) + 9000)
    order = rng.permutation(len(people))
    for k, i in enumerate(order):
        people[i].pid = ids[k]
    spare = ids[len(people):]
    # pupils living in Northern Ireland, recorded by the school immunisation team; numbers from the end of the spare
    # block, so every other registration keeps its number
    ni = _ni_pupils(np.random.default_rng(W.SEED + 108), practices)
    for k, q in enumerate(ni):
        q.pid = spare[len(spare) - 1 - k]
    spare = spare[:len(spare) - len(ni)]
    people.extend(ni)
    _practice_shown(np.random.default_rng(W.SEED + 109), people)
    events = _doses(rng_dose, people)
    merges = _merges(np.random.default_rng(W.SEED + 106), people, events, spare)
    _postcodes(np.random.default_rng(W.SEED + 107), people)
    return people, events, practices, merges


def _ni_pupils(rng, practices):
    """Children living in Northern Ireland who go to school in the region. The school immunisation team opens a
    register record at the first session it vaccinates them, with the home address; no local health office covers a
    UK address, so the record takes the school's area, in the code scheme in force that day."""
    out = []
    areas = list(W.NI_SCHOOL_AREAS)
    ap = np.array([W.NI_SCHOOL_AREAS[a][0] for a in areas])
    for y in range(1993, 2018):
        lo, hi = next(v for r, v in W.NI_PUPILS_PER_YEAR.items() if y in r)
        for _ in range(int(rng.integers(lo, hi))):
            while True:
                dob = _rand_date(rng, D(y, 1, 1), D(y, 12, 31))
                if not (dob.month == 2 and dob.day == 29):
                    break
            sex = "F" if rng.random() < 0.493 else "M"
            area = areas[int(rng.choice(len(areas), p=ap))]
            first = _school_session_date(rng, dob, 12 if y <= 1994 else 5)
            registered = first - dt.timedelta(days=int(rng.integers(0, 9)))
            lho_recorded = registered
            t = registered
            while True:
                t = t + dt.timedelta(days=int(rng.exponential(365 * 9)))
                if t > D(2027, 6, 25):
                    break
                lho_recorded = t
            if D(2024, 6, 24) <= lho_recorded <= D(2024, 7, 8):
                lho_recorded = lho_recorded + dt.timedelta(days=15)
            if area == "LH27" and lho_recorded >= W.CUTOVER:
                lho = "LH26"
            else:
                lho = area
            district = W.NI_SCHOOL_AREAS[area][1][int(rng.integers(0, len(W.NI_SCHOOL_AREAS[area][1])))]
            pc = "%s %d%s%s" % (district, int(rng.integers(0, 10)), "ABDEFGHJLNPQRSTUWXYZ"[int(rng.integers(0, 20))],
                                "ABDEFGHJLNPQRSTUWXYZ"[int(rng.integers(0, 20))])
            practice = practices[area if area in practices else "LH26"][0]
            shown = practices[area][int(rng.integers(0, len(practices[area])))] if rng.random() < W.NI_WITH_GP else ""
            out.append(Person(pid=None, dob=dob, sex=sex, lho=lho, lho_recorded=lho_recorded, registered=registered,
                              practice=practice, born_in_region=False, status="ni", area=area, dest=lho, postcode=pc,
                              shown_practice=shown))
    return out


def _practice_shown(rng, people):
    """The practice the extract shows: cleared when the practice deregisters someone who has left it."""
    for p in people:
        if p.status in ("moved", "portlaoise") and rng.random() < 0.6:
            p.shown_practice = ""


EIRCODE_CHARS = "0123456789ACDEFHKNPRTVWXY"


def _postcodes(rng, people):
    """The address's postcode, where one was recorded: an Eircode for an address in the State recorded from July 2015,
    blank for one recorded before; a UK postcode for an address in Northern Ireland."""
    for p in sorted(people, key=lambda q: q.pid):
        if p.status == "ni":
            continue
        if p.lho_recorded < W.EIRCODE_FROM:
            p.postcode = ""
            continue
        code = p.dest
        if p.status == "resident":
            key = "LH27_old" if code == "LH27" else ("LH26_new" if (code == "LH26" and p.lho_recorded >= W.CUTOVER)
                                                     else code)
        else:
            key = code
        keys = W.ROUTING_KEYS[key]
        rk = keys[int(rng.integers(0, len(keys)))]
        p.postcode = "%s %s" % (rk, "".join(EIRCODE_CHARS[int(rng.integers(0, len(EIRCODE_CHARS)))] for _ in range(4)))


ACTIVE = ("resident", "moved", "portlaoise", "ni")


def _merges(rng, people, events, spare):
    """Duplicate registrations found and merged: a child registered a second time by the school immunisation team at
    school entry (its school doses loaded to that record), and for some a third record opened at a change of GP (its
    GP doses loaded there). The register records each merge in its merge table and leaves every event on the record it
    was loaded to. A chain merges the school record into the GP record first and the GP record into the original
    later."""
    by_pid = {}
    for e in events:
        by_pid.setdefault(e.pid, []).append(e)
    rows = []
    k = 0
    cands = [p for p in people if p.born_in_region and p.status in ACTIVE + ("transferred",)]
    pick = rng.random(len(cands)) < W.DUPLICATE_SHARE
    for p, chosen in zip(cands, pick):
        if not chosen:
            continue
        evs = by_pid.get(p.pid, [])
        school = sorted((e for e in evs if e.given_by == "School team"), key=lambda e: e.date)
        if not school:
            continue
        created = school[0].date - dt.timedelta(days=int(rng.integers(0, 20)))
        merged = created + dt.timedelta(days=int(rng.integers(200, 3200)))
        if merged > D(2027, 5, 31):
            merged = _rand_date(rng, created + dt.timedelta(days=60), D(2027, 5, 31))
        r1 = spare[k]
        k += 1
        chain = rng.random() < W.CHAIN_SHARE
        gp = sorted((e for e in evs if e.given_by == "GP" and e.date >= p.dob + dt.timedelta(days=700)), key=lambda e: e.date)
        if chain and gp:
            r2 = spare[k]
            k += 1
            g_created = gp[0].date - dt.timedelta(days=int(rng.integers(0, 30)))
            t1 = max(merged, g_created + dt.timedelta(days=30))
            t2 = t1 + dt.timedelta(days=int(rng.integers(150, 2400)))
            if t2 > D(2027, 5, 31):
                t2 = _rand_date(rng, t1 + dt.timedelta(days=20), D(2027, 6, 10))
            for e in school:
                if created <= e.date < t1:
                    e.pid = r1
            for e in gp:
                if g_created <= e.date < t2:
                    e.pid = r2
            rows.append(dict(retired=r1, surviving=r2, merged_on=t1, reason="Duplicate registration at school entry"))
            rows.append(dict(retired=r2, surviving=p.pid, merged_on=t2, reason="Duplicate registration at change of GP"))
        else:
            for e in school:
                if created <= e.date < merged:
                    e.pid = r1
            rows.append(dict(retired=r1, surviving=p.pid, merged_on=merged, reason="Duplicate registration at school entry"))
    rows.sort(key=lambda r: (r["merged_on"], r["retired"]))
    return rows


def _school_session_date(rng, dob, age_years):
    """A school session in the school year the child turns `age_years` (September to May)."""
    yr = dob.year + age_years
    start = D(yr - 1 if dob.month >= 9 else yr - 1, 9, 15)
    if dob.month >= 9:
        start = D(yr, 9, 15)
    d = _rand_date(rng, start, start + dt.timedelta(days=220))
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    return d


def _doses(rng, people):
    """True doses as the register received them, one event each, before any return-line query."""
    ev = []
    for p in people:
        if p.status == "ni":
            continue
        y = p.dob.year
        doses = []
        if p.born_in_region:
            sched = 15 if y <= 2007 else 12
            if rng.random() < MMR1_UPTAKE[y]:
                d1 = p.dob + dt.timedelta(days=int(sched * 30.4 + rng.gamma(2.0, 28)))
                doses.append((d1, "GP"))
                if rng.random() < MMR2_GIVEN_MMR1[y]:
                    if y <= 1994:
                        d2 = _school_session_date(rng, p.dob, 12)
                    else:
                        d2 = _school_session_date(rng, p.dob, 5)
                    doses.append((d2, "School team"))
            else:
                # catch-up for the scare cohorts (2013 GP catch-up) and late starters; the school team offers a dose at
                # school entry to children with none
                late = 0.30 if 2008 <= y <= 2011 else 0.12
                u = rng.random()
                if u >= late and u < late + 0.16:
                    doses.append((_school_session_date(rng, p.dob, 5 if y > 1994 else 12), "School team"))
                elif u < late:
                    if 2008 <= y <= 2011:
                        d1 = _rand_date(rng, D(2013, 2, 1), D(2013, 11, 30))
                    else:
                        d1 = p.dob + dt.timedelta(days=int(rng.integers(500, 1900)))
                    doses.append((d1, "GP"))
                    if rng.random() < 0.55:
                        doses.append((_school_session_date(rng, p.dob, 5 if y > 1994 else 12), "School team"))
        else:
            # moved in: records from abroad at registration
            if rng.random() < 0.58:
                n = 2 if rng.random() < 0.68 else 1
                d1 = p.dob + dt.timedelta(days=int(rng.integers(370, 560)))
                if d1 < p.registered:
                    doses.append((d1, "Abroad"))
                    if n == 2:
                        d2 = p.dob + dt.timedelta(days=int(rng.integers(1300, 2300)))
                        if d2 < p.registered:
                            doses.append((d2, "Abroad"))
        # adult and teenage extra doses
        if y <= 2007 and len(doses) < 2 and rng.random() < 0.10:
            d = _rand_date(rng, max(_birthday(p.dob, 18), D(2011, 1, 1)), D(2027, 6, 26))
            doses.append((d, "GP" if rng.random() < 0.6 else ("Pharmacy" if d >= D(2019, 1, 1) else "GP")))
        if y <= 2002 and rng.random() < 0.012:
            d = _rand_date(rng, max(_birthday(p.dob, 20), D(2012, 1, 1)), D(2027, 6, 26))
            doses.append((d, "Occupational health"))
        # 2019 outbreak response clinics for teenagers and young adults in the outbreak areas
        if 2003 <= y <= 2010 and p.area in ("LH21", "LH22") and len(doses) < 2 and rng.random() < 0.10:
            doses.append((_rand_date(rng, D(2019, 4, 8), D(2019, 6, 14)), "School team"))
        # 2014 outbreak response: infants aged six to eleven months in Navan and Trim-Kells
        if p.born_in_region and p.area in ("LH22", "LH24") and D(2013, 4, 15) <= p.dob <= D(2013, 10, 31) \
                and rng.random() < 0.34:
            doses.append((_rand_date(rng, D(2014, 3, 17), D(2014, 5, 16)), "Hospital"))
        fb = _birthday(p.dob, 1)
        doses.sort()
        spaced = []
        for d, by in doses:
            # C1: no two doses 20 to 36 days apart (the 28-day minimum interval never sits on an edge)
            if spaced and 20 <= (d - spaced[-1][0]).days <= 36:
                d = spaced[-1][0] + dt.timedelta(days=45 + int(rng.integers(0, 21)))
            spaced.append((d, by))
        doses = spaced
        for d, by in doses:
            if abs((d - fb).days) <= 4:
                d = fb + dt.timedelta(days=6)        # C1: no dose within four days of the first birthday
            if d > D(2027, 6, 30):
                continue
            ev.append(Event(eid=None, pid=p.pid, product=None, date=d, given_by=by, source_ref=None, loaded=None,
                            kind="dose", owner=p.pid))
    # a few doses given on 1 and 2 July 2027, loaded before the 3 July run
    adults = [p for p in people if p.dob.year <= 2009 and p.status != "ni"]
    for k in range(13):
        p = adults[int(rng.integers(0, len(adults)))]
        ev.append(Event(eid=None, pid=p.pid, product=None, date=D(2027, 7, 1 + (k % 2)),
                        given_by="Pharmacy", source_ref=None, loaded=None, kind="dose", owner=p.pid))
    # pupils living in Northern Ireland: the school team's doses only (their GP doses are given and recorded in
    # Northern Ireland)
    rng_ni = np.random.default_rng(W.SEED + 111)
    for p in people:
        if p.status != "ni":
            continue
        doses = []
        if rng_ni.random() < 0.92:
            doses.append(p.registered + dt.timedelta(days=int(rng_ni.integers(0, 9))))
        if p.dob.year >= 1995 and rng_ni.random() < 0.06:
            d2 = _school_session_date(rng_ni, p.dob, 12)
            if not doses or (d2 - doses[-1]).days > 60:
                doses.append(d2)
        for d in doses:
            if d <= D(2027, 6, 30):
                ev.append(Event(eid=None, pid=p.pid, product=None, date=d, given_by="School team", source_ref=None,
                                loaded=None, kind="dose", owner=p.pid))
    return ev


def _next_month(d):
    return D(d.year + (d.month == 12), d.month % 12 + 1, 1)


def references(rng, people, events, practices):
    """Source references and load dates: GP return lines (GPR-yyyymm-practice-line), school sessions
    (SIT-yyyy-session), hospital clinics, pharmacies and records from abroad. Returns the GP line table."""
    pmap = {p.pid: p for p in people}
    gp_lines = {}
    counters = {}
    sessions = {}
    sess_no = {}
    for e in sorted(events, key=lambda e: (e.date, e.owner)):
        p = pmap[e.owner]
        e.product = _product(rng, e.date)
        if e.given_by in ("GP",):
            # each practice returns the month's doses after the month ends; the return is labelled by that month
            ret = D(e.date.year, e.date.month, 1)
            key = (ret, p.practice)
            counters[key] = counters.get(key, 0) + 1
            e.source_ref = "GPR-%04d%02d-%s-%03d" % (ret.year, ret.month, p.practice, counters[key])
            e.loaded = _next_month(ret) + dt.timedelta(days=int(rng.integers(4, 31)))
            gp_lines[e.source_ref] = e
        elif e.given_by == "School team":
            skey = (e.date, p.area)
            if skey not in sessions:
                sess_no[e.date.year] = sess_no.get(e.date.year, 0) + 1
                sessions[skey] = "SIT-%04d-%04d" % (e.date.year, sess_no[e.date.year] + int(rng.integers(0, 3)))
                sess_no[e.date.year] += 2
            e.source_ref = sessions[skey]
            e.loaded = e.date + dt.timedelta(days=int(rng.integers(3, 21)))
        elif e.given_by == "Hospital":
            e.source_ref = "HOS-%04d-%05d" % (e.date.year, int(rng.integers(100, 99999)))
            e.loaded = e.date + dt.timedelta(days=int(rng.integers(2, 30)))
        elif e.given_by == "Pharmacy":
            e.source_ref = "PHA-%04d%02d-%05d" % (e.date.year, e.date.month, int(rng.integers(10000, 99999)))
            e.loaded = e.date + dt.timedelta(days=1 if e.date >= D(2027, 7, 1) else int(rng.integers(1, 9)))
        elif e.given_by == "Occupational health":
            e.source_ref = "OCH-%04d-%04d" % (e.date.year, int(rng.integers(1, 9999)))
            e.loaded = e.date + dt.timedelta(days=int(rng.integers(10, 60)))
        else:   # Abroad: keyed from the record at registration
            e.source_ref = "ABR-%04d-%05d" % (p.registered.year, int(rng.integers(1, 99999)))
            e.loaded = p.registered + dt.timedelta(days=int(rng.integers(0, 40)))
    # anything not loaded by the morning of the 3 July run is not in the extract
    events[:] = [e for e in events if e.loaded <= W.RUN]
    return {r: e for r, e in gp_lines.items() if e.loaded <= W.RUN}


QUERY_REASONS = {
    "sibling": "Child not registered at practice",
    "date_after": "Date of vaccination after return date",
    "date_birth": "Date of vaccination does not match child's age",
    "error": "Line sent in error",
    "duplicate": "Dose already returned",
    "batch": "Vaccine batch not recognised",
    "interval": "Dose interval shorter than schedule",
    "infant": "Child aged under 12 months at vaccination",
    "notreg": "Child not registered at practice",
}


def _chased(raised, took, least=6):
    """A query the practice had confirmed but the office had not yet closed when the 30 June extract was prepared: the
    register chased it and closed it by the as-at date. The drawn time to close is folded into the days left, never
    under the office's usual six where there is room; None when it was raised too late to close by then."""
    room = (W.AS_AT - raised).days
    if room < 1:
        return None
    lo = min(least, room)
    return raised + dt.timedelta(days=lo + (took - lo) % (room - lo + 1))


def queries(people, events, gp_lines):
    """The immunisation office's queries on GP return lines from 2005: about 1.25 per cent of lines; replaced (the
    dose keyed to a sibling, or a wrong date), withdrawn (sent in error, or a dose already returned) or confirmed as
    sent. The register loaded every line as received, so a replaced or withdrawn line is still an event; this function
    adds those events and returns the log rows."""
    rng = np.random.default_rng(W.SEED + 103)
    pmap = {p.pid: p for p in people}
    by_practice = {}
    for p in people:
        by_practice.setdefault(p.practice, []).append(p)
    lines = sorted((r for r, e in gp_lines.items() if e.date >= W.QUERY_LOG_START), key=lambda r: (gp_lines[r].date, r))
    rows = []
    new_events = []
    qn = 0
    next_line = {}
    for ref in lines:
        e = gp_lines[ref]
        p = pmap[e.owner]
        adult = (e.date - p.dob).days >= 18 * 365
        if rng.random() >= (W.QUERY_RATE_ADULT if adult else W.QUERY_RATE):
            continue
        u = rng.random()
        if u < W.QUERY_OUTCOMES["replaced"]:
            outcome = "replaced"
            sub = "sibling" if rng.random() < 0.55 else "date_after"
        elif u < W.QUERY_OUTCOMES["replaced"] + W.QUERY_OUTCOMES["withdrawn"]:
            outcome = "withdrawn"
            sub = "error" if rng.random() < 0.7 else "duplicate"
        else:
            outcome = "confirmed"
            sub = ["batch", "interval", "notreg", "date_birth"][int(rng.integers(0, 4))]
        raised = e.loaded + dt.timedelta(days=int(rng.integers(5, 40)))
        took = int(rng.integers(6, 75))
        closed = raised + dt.timedelta(days=took)
        if closed > W.AS_AT:
            # still open when the 30 June extract was prepared: the register chased it and closed it by then, or it
            # was raised too late to close and is not in the log
            closed = _chased(raised, took)
            if closed is None:
                continue
        qn += 1
        replaced_by = ""
        if outcome == "replaced":
            # the corrected line goes in the practice's next return; the original line stays loaded
            ret = D(closed.year, closed.month, 1)
            key = (ret, p.practice)
            next_line[key] = next_line.get(key, 900) + 1
            new_ref = "GPR-%04d%02d-%s-%03d" % (ret.year, ret.month, p.practice, next_line[key])
            replaced_by = new_ref
            if sub == "sibling":
                sibs = [s for s in by_practice[p.practice] if s.pid != p.pid and abs(s.dob.year - p.dob.year) <= 6
                        and s.status == p.status]
                if not sibs:
                    sub = "date_after"
                else:
                    s = sibs[int(rng.integers(0, len(sibs)))]
                    # the original line keyed to the sibling: the event moves there, the corrected line returns it
                    orig = Event(eid=None, pid=s.pid, product=e.product, date=e.date, given_by="GP", source_ref=ref,
                                 loaded=e.loaded, kind="phantom", owner=s.pid)
                    e.source_ref = new_ref
                    e.loaded = min(closed + dt.timedelta(days=int(rng.integers(10, 35))), W.RUN)
                    new_events.append(orig)
            if sub == "date_after":
                # the original line carried a mistyped date (a year or a month out); the corrected line carries the
                # date the dose was given
                shift = int(rng.choice([365, -365, 92, -61, 61]))
                wrong = e.date + dt.timedelta(days=shift)
                orig = Event(eid=None, pid=e.pid, product=e.product, date=wrong, given_by="GP", source_ref=ref,
                             loaded=e.loaded, kind="phantom", owner=p.pid)
                e.source_ref = new_ref
                e.loaded = min(closed + dt.timedelta(days=int(rng.integers(10, 35))), W.RUN)
                new_events.append(orig)
        elif outcome == "withdrawn":
            if sub == "error":
                # no dose was given: the line named a child who did not attend
                cands = [s for s in by_practice[p.practice] if s.pid != p.pid and abs(s.dob.year - p.dob.year) <= 3]
                if cands:
                    s = cands[int(rng.integers(0, len(cands)))]
                    orig = Event(eid=None, pid=s.pid, product=e.product, date=e.date, given_by="GP", source_ref=ref,
                                 loaded=e.loaded, kind="phantom", owner=s.pid)
                    # the attending child's real dose sits on another line
                    key = (D(e.date.year, e.date.month, 1), p.practice)
                    next_line[key] = next_line.get(key, 700) + 1
                    e.source_ref = "GPR-%04d%02d-%s-%03d" % (e.date.year, e.date.month, p.practice, next_line[key])
                    new_events.append(orig)
                else:
                    continue
            else:
                # the dose was already on an earlier line: a second line for the same dose, a few weeks later
                later = e.date + dt.timedelta(days=int(rng.integers(35, 120)))
                orig = Event(eid=None, pid=e.pid, product=e.product, date=later, given_by="GP", source_ref=ref,
                             loaded=e.loaded, kind="phantom", owner=p.pid)
                key = (D(e.date.year, e.date.month, 1), p.practice)
                next_line[key] = next_line.get(key, 700) + 1
                e.source_ref = "GPR-%04d%02d-%s-%03d" % (e.date.year, e.date.month, p.practice, next_line[key])
                new_events.append(orig)
        rows.append(dict(query_ref="Q%02d-%04d" % (raised.year % 100, qn), line_ref=ref, practice=p.practice,
                         raised=raised, reason=QUERY_REASONS[sub], outcome={"replaced": "Replaced by corrected line",
                         "withdrawn": "Withdrawn by practice", "confirmed": "Confirmed as sent"}[outcome],
                         replaced_by=replaced_by, closed=closed, kind=outcome,
                         chased=outcome == "confirmed" and raised + dt.timedelta(days=took) > W.AS_AT))
    events.extend(new_events)
    return rows


def other_queries(n_existing):
    """Queried lines for children born after 2017 (outside the extract), so the log covers every queried MMR line."""
    rng = np.random.default_rng(W.SEED + 104)
    rows = []
    n = int(n_existing * 0.62)
    for k in range(n):
        d = _rand_date(rng, D(2019, 2, 1), D(2027, 5, 31))
        ret = D(d.year, d.month, 1)
        practice = "GP%04d" % int(rng.integers(1100, 4999))
        ref = "GPR-%04d%02d-%s-%03d" % (ret.year, ret.month, practice, int(rng.integers(1, 140)))
        u = rng.random()
        if u < 0.41:
            out, kind = "Replaced by corrected line", "replaced"
            reason = QUERY_REASONS["sibling" if rng.random() < 0.5 else "date_after"]
        elif u < 0.55:
            out, kind = "Withdrawn by practice", "withdrawn"
            reason = QUERY_REASONS["error"]
        else:
            out, kind = "Confirmed as sent", "confirmed"
            reason = QUERY_REASONS[["batch", "interval", "infant", "date_birth"][int(rng.integers(0, 4))]]
        raised = d + dt.timedelta(days=int(rng.integers(30, 70)))
        took = int(rng.integers(6, 75))
        closed = raised + dt.timedelta(days=took)
        if raised > W.RUN:
            continue
        if closed > W.AS_AT:
            closed = _chased(raised, took)
            if closed is None:
                continue
        cl = closed or raised
        rep = ""
        if kind == "replaced":
            rr = D(cl.year, cl.month, 1)
            rep = "GPR-%04d%02d-%s-%03d" % (rr.year, rr.month, practice, 900 + int(rng.integers(1, 60)))
        rows.append(dict(query_ref=None, line_ref=ref, practice=practice, raised=raised, reason=reason, outcome=out,
                         replaced_by=rep, closed=closed, kind=kind,
                         chased=kind == "confirmed" and raised + dt.timedelta(days=took) > W.AS_AT))
    return rows


def finish_register(people, events, rows_ext, rows_other):
    """Event identifiers in load order, re-sent school batches (the same session loaded twice under fresh event
    numbers) and the query numbers in the order raised."""
    rng = np.random.default_rng(W.SEED + 105)
    # a few school sessions re-sent in 2016-17: every event of the session loaded a second time a month later
    sess = sorted({e.source_ref for e in events if e.given_by == "School team" and D(2016, 1, 1) <= e.date <= D(2017, 6, 30)})
    resent = set(rng.choice(sess, size=min(4, len(sess)), replace=False).tolist()) if sess else set()
    extra = []
    for e in events:
        if e.source_ref in resent:
            extra.append(Event(eid=None, pid=e.pid, product=e.product, date=e.date, given_by=e.given_by,
                               source_ref=e.source_ref, loaded=e.loaded + dt.timedelta(days=int(rng.integers(28, 40))),
                               kind="resent", owner=e.owner))
    events.extend(extra)
    # a school-team dose also keyed by the GP from the child's card, dated the day the card was seen
    school = [e for e in events if e.given_by == "School team" and e.kind == "dose" and e.date.year >= 2006]
    pick = rng.choice(len(school), size=min(220, len(school)), replace=False)
    pmap = {p.pid: p for p in people}
    for i in sorted(pick.tolist()):
        e = school[i]
        p = pmap[e.owner]
        d = e.date + dt.timedelta(days=int(rng.integers(3, 15)))
        if d > D(2027, 6, 30):
            continue
        events.append(Event(eid=None, pid=p.pid, product=e.product, date=d, given_by="GP", source_ref=None,
                            loaded=None, kind="card", owner=p.pid))
    events.sort(key=lambda e: (e.loaded or e.date, e.pid, e.date))
    # the GP card entries get lines of their own
    counters = {}
    for e in events:
        if e.kind == "card":
            p = pmap[e.owner]
            ret = D(e.date.year, e.date.month, 1)
            key = (ret, p.practice)
            counters[key] = counters.get(key, 500) + 1
            e.source_ref = "GPR-%04d%02d-%s-%03d" % (ret.year, ret.month, p.practice, counters[key])
            e.loaded = _next_month(ret) + dt.timedelta(days=int(rng.integers(4, 31)))
    events[:] = [e for e in events if e.loaded <= W.RUN]
    events.sort(key=lambda e: (e.loaded, e.pid, e.date))
    for k, e in enumerate(events):
        e.eid = "EV%08d" % (31_000_000 + k * 7 + int(rng.integers(0, 6)))
    log = sorted(rows_ext + rows_other, key=lambda r: (r["raised"], r["line_ref"]))
    for k, r in enumerate(log):
        r["query_ref"] = "Q%02d-%05d" % (r["raised"].year % 100, 10000 + k)
    return log


# =================================================================================================================
# The case export and the laboratory results
# =================================================================================================================
def _case(cid, onset, dob, sex, county, cls, imp, outbreak="", epi="", hosp="N", doses="0", comments="", legacy="",
          notified=None, kind="case", key=None):
    return dict(case_id=cid, legacy_ref=legacy, notified=notified or onset + dt.timedelta(days=4), onset_date=onset,
                date_of_birth=dob, sex=sex, county=county, classification=cls, importation=imp, outbreak_ref=outbreak,
                epi_link=epi, hospitalised=hosp, mmr_doses_reported=doses, comments=comments, kind=kind, key=key)


RENOTIFIED = [  # (onset, date of birth, the second notifier's note, days after the first notification, outbreak record)
    (D(2023, 7, 19), D(2017, 2, 9), "GP notification", 2, None),
    (D(2024, 2, 22), D(2011, 9, 7), "Hospital notification, Drogheda", 1, ""),
    (D(2024, 3, 6), D(2006, 2, 18), "Hospital notification, Drogheda", 2, ""),
    (D(2025, 1, 15), D(2012, 10, 11), "GP notification", 3, None),
    (D(2026, 2, 9), D(2005, 7, 27), "Hospital notification, Cavan", 1, None),
    (D(2027, 4, 2), D(1996, 5, 21), "GP notification", 2, None),
]


def cases():
    """The region's measles notifications since 2019, written case by case: the 2019 outbreak (legacy system,
    migrated in March 2021 and back-entered by the outbreak team in May 2021), sporadic imports, the 2024 outbreak
    (with a twin pair) and the April 2027 incident. Returns the export rows and the laboratory rows."""
    rng = np.random.default_rng(W.SEED + 201)
    C = []
    lab = []

    def L(cid, d, typ, test, res, geno=""):
        lab.append(dict(case_id=cid, specimen_date=d, specimen_type=typ, test=test, result=res, genotype=geno))

    # ---- 2019 outbreak (legacy MZ19 numbers), migrated records ------------------------------------------------
    # (legacy number, onset, dob, sex, county, classification, importation, doses, hosp, swap_dob, shift_onset_days)
    ob19 = [
        ("MZ19/0107", D(2019, 3, 4), D(2014, 6, 9), "M", "Louth", "Confirmed", "Imported", "0", "Y", True, 0),
        ("MZ19/0111", D(2019, 3, 14), D(1995, 4, 2), "F", "Louth", "Confirmed", "Imported", "0", "N", True, 0),
        ("MZ19/0114", D(2019, 3, 19), D(2016, 1, 23), "F", "Louth", "Confirmed", "Import-related", "0", "N", False, 6),
        ("MZ19/0118", D(2019, 3, 22), D(2010, 11, 5), "M", "Louth", "Confirmed", "Imported", "1", "N", True, 0),
        ("MZ19/0121", D(2019, 3, 27), D(2004, 3, 7), "F", "Meath", "Confirmed", "Imported", "0", "N", True, 0),
        ("MZ19/0124", D(2019, 3, 30), D(1987, 8, 19), "M", "Louth", "Confirmed", "Import-related", "0", "Y", False, 0),
        ("MZ19/0127", D(2019, 4, 3), D(2015, 2, 14), "M", "Louth", "Confirmed", "Import-related", "0", "N", False, 0),
        ("MZ19/0130", D(2019, 4, 6), D(2009, 10, 2), "F", "Meath", "Confirmed", "Import-related", "0", "N", True, 0),
        ("MZ19/0133", D(2019, 4, 9), D(2003, 5, 28), "M", "Meath", "Confirmed", "Import-related", "1", "N", False, 9),
        ("MZ19/0135", D(2019, 4, 11), D(2018, 9, 16), "F", "Louth", "Confirmed", "Import-related", "0", "Y", False, 0),
        ("MZ19/0138", D(2019, 4, 14), D(1997, 12, 21), "M", "Meath", "Confirmed", "Import-related", "0", "N", False, 8),
        ("MZ19/0140", D(2019, 4, 16), D(2016, 7, 30), "F", "Meath", "Confirmed", "Import-related", "0", "N", False, 0),
        ("MZ19/0142", D(2019, 4, 17), D(2005, 9, 13), "F", "Louth", "Probable", "Import-related", "0", "N", False, 0),
        ("MZ19/0143", D(2019, 4, 19), D(1994, 1, 26), "M", "Louth", "Confirmed", "Import-related", "1", "N", False, 0),
        ("MZ19/0146", D(2019, 4, 22), D(2011, 6, 18), "M", "Meath", "Confirmed", "Import-related", "0", "N", False, 10),
        ("MZ19/0148", D(2019, 4, 24), D(2005, 2, 27), "F", "Meath", "Confirmed", "Import-related", "0", "N", False, 0),
        ("MZ19/0149", D(2019, 4, 25), D(1999, 7, 15), "F", "Louth", "Confirmed", "Import-related", "1", "N", False, 11),
        ("MZ19/0151", D(2019, 4, 28), D(2013, 12, 3), "M", "Louth", "Probable", "Import-related", "0", "N", False, 0),
        ("MZ19/0153", D(2019, 4, 30), D(2007, 8, 22), "M", "Meath", "Confirmed", "Import-related", "0", "N", False, 0),
        ("MZ19/0156", D(2019, 5, 3), D(2001, 4, 17), "F", "Meath", "Confirmed", "Import-related", "0", "Y", False, 7),
        ("MZ19/0158", D(2019, 5, 5), D(2014, 10, 29), "F", "Louth", "Confirmed", "Import-related", "0", "N", False, 9),
        ("MZ19/0161", D(2019, 5, 8), D(1979, 3, 30), "F", "Louth", "Confirmed", "Import-related", "1", "N", False, 0),
        ("MZ19/0163", D(2019, 5, 10), D(2012, 2, 8), "M", "Meath", "Probable", "Import-related", "0", "N", False, 0),
        ("MZ19/0165", D(2019, 5, 13), D(2006, 11, 26), "M", "Louth", "Discarded", "", "2", "N", False, 0),
        ("MZ19/0168", D(2019, 5, 15), D(2003, 1, 31), "F", "Meath", "Confirmed", "Import-related", "0", "N", False, 0),
        ("MZ19/0170", D(2019, 5, 18), D(1993, 9, 24), "F", "Meath", "Confirmed", "Import-related", "0", "N", False, 8),
        ("MZ19/0173", D(2019, 5, 21), D(2019, 1, 11), "M", "Meath", "Confirmed", "Import-related", "0", "Y", False, 0),
        ("MZ19/0175", D(2019, 5, 24), D(2008, 4, 7), "F", "Louth", "Possible", "", "0", "N", False, 0),
        ("MZ19/0178", D(2019, 5, 27), D(1990, 6, 20), "M", "Meath", "Confirmed", "Import-related", "0", "N", False, 0),
        ("MZ19/0180", D(2019, 5, 30), D(2016, 5, 6), "M", "Meath", "Confirmed", "Import-related", "0", "N", True, 0),
        ("MZ19/0183", D(2019, 6, 3), D(2001, 10, 9), "M", "Louth", "Confirmed", "Import-related", "1", "N", True, 0),
        ("MZ19/0185", D(2019, 6, 6), D(2017, 3, 2), "F", "Louth", "Probable", "Import-related", "0", "N", False, 0),
        ("MZ19/0188", D(2019, 6, 10), D(1996, 2, 11), "F", "Louth", "Confirmed", "Import-related", "0", "N", True, 0),
        ("MZ19/0190", D(2019, 6, 14), D(2010, 9, 27), "F", "Meath", "Confirmed", "Import-related", "0", "N", False, 0),
    ]
    legacy_ids = {}
    k = 4400
    for row in ob19:
        ref, onset, dob, sex, county, cls, imp, doses, hosp, swap, shift = row
        k += int(rng.integers(3, 17))
        cid = "NDS-L%06d" % k
        legacy_ids[ref] = cid
        C.append(_case(cid, onset, dob, sex, county, cls, imp, doses=doses, hosp=hosp, legacy=ref,
                       comments="Migrated from legacy system 01/03/2021", key=ref, kind="legacy"))
        if cls in ("Confirmed", "Discarded"):
            if not (ref == "MZ19/0124"):     # one case confirmed by the hospital laboratory, specimen not referred
                L(cid, onset + dt.timedelta(days=int(rng.integers(2, 6))), "Serum", "Measles IgM",
                  "Positive" if cls == "Confirmed" else "Negative")
                if cls == "Confirmed" and rng.random() < 0.5:
                    L(cid, onset + dt.timedelta(days=int(rng.integers(2, 6))), "Throat swab", "Measles PCR", "Positive",
                      "D8")
    # sporadic legacy-era cases (2019 to February 2021), migrated
    spor = [
        ("MZ19/0231", D(2019, 8, 12), D(1998, 5, 3), "M", "Meath", "Confirmed", "Imported", "1", "N"),
        ("MZ19/0262", D(2019, 10, 2), D(2016, 12, 14), "F", "Cavan", "Discarded", "", "1", "N"),
        ("MZ19/0288", D(2019, 11, 21), D(1984, 7, 1), "F", "Louth", "Confirmed", "Imported", "0", "Y"),
        ("MZ20/0012", D(2020, 1, 9), D(2006, 4, 30), "M", "Cavan", "Confirmed", "Imported", "0", "N"),
        ("MZ20/0019", D(2020, 1, 28), D(2007, 1, 15), "F", "Cavan", "Confirmed", "Import-related", "0", "N"),
        ("MZ20/0047", D(2020, 2, 25), D(1991, 9, 8), "M", "Meath", "Possible", "", "Unknown", "N"),
        ("MZ20/0101", D(2020, 9, 16), D(2012, 6, 3), "F", "Monaghan", "Discarded", "", "2", "N"),
    ]
    for ref, onset, dob, sex, county, cls, imp, doses, hosp in spor:
        k += int(rng.integers(40, 160))
        cid = "NDS-L%06d" % k
        C.append(_case(cid, onset, dob, sex, county, cls, imp, doses=doses, hosp=hosp, legacy=ref,
                       comments="Migrated from legacy system 01/03/2021", key=ref, kind="legacy"))
        if cls in ("Confirmed", "Discarded"):
            L(cid, onset + dt.timedelta(days=int(rng.integers(2, 6))), "Oral fluid", "Measles IgM",
              "Positive" if cls == "Confirmed" else "Negative")
    # ---- the back-entry: the outbreak team keyed the 2019 line list into the outbreak module in May 2021 ---------
    seq = 211
    for row in ob19:
        ref, onset, dob, sex, county, cls, imp, doses, hosp, swap, shift = row
        if cls not in ("Confirmed", "Probable"):
            continue
        seq += int(rng.integers(1, 4))
        cid = "NDS-21-%06d" % (2100 + seq)
        b_dob = D(dob.year, dob.day, dob.month) if swap else dob
        b_onset = onset + dt.timedelta(days=shift)
        entered = _rand_date(rng, *W.BACK_ENTRY)
        C.append(_case(cid, b_onset, b_dob, sex, county, cls, imp, outbreak="OB-NE-2019-01", doses=doses, hosp=hosp,
                       notified=onset + dt.timedelta(days=shift + 2 if shift else 4),
                       comments="Entered from OCT line list (2019 outbreak). Legacy no. %s" % ref,
                       kind="backentry", key=ref))
    # ---- new-system cases: sporadic imports, the 2024 outbreak, the April 2027 incident ------------------------------
    new = []

    def N_(onset, dob, sex, county, cls, imp, **kw):
        new.append((onset, dob, sex, county, cls, imp, kw))
    N_(D(2021, 11, 8), D(1988, 2, 22), "M", "Meath", "Discarded", "", doses="2")
    N_(D(2022, 6, 14), D(2015, 8, 20), "F", "Louth", "Discarded", "", doses="1")
    N_(D(2023, 3, 3), D(2000, 6, 12), "F", "Meath", "Confirmed", "Imported", doses="0",
       comments="Travel to Romania, rash three days after return")
    N_(D(2023, 7, 19), D(2017, 2, 9), "M", "Louth", "Confirmed", "Imported", doses="0",
       comments="Family holiday abroad; hospital laboratory IgM positive, specimen not referred", lab=False)
    N_(D(2023, 9, 30), D(1999, 11, 4), "F", "Cavan", "Possible", "", doses="Unknown")
    N_(D(2023, 12, 11), D(1975, 5, 17), "M", "Louth", "Confirmed", "Imported", doses="Unknown")
    # the 2024 outbreak (Drogheda and Navan): entered directly by the outbreak team
    ob24 = [
        (D(2024, 2, 5), D(1994, 8, 30), "F", "Louth", "Confirmed", "Imported", "0"),
        (D(2024, 2, 18), D(2010, 4, 16), "M", "Louth", "Confirmed", "Import-related", "0"),
        (D(2024, 3, 1), D(2010, 4, 16), "F", "Louth", "Confirmed", "Import-related", "0"),   # his twin sister, epi-linked
        (D(2024, 2, 22), D(2011, 9, 7), "F", "Louth", "Confirmed", "Import-related", "0"),
        (D(2024, 2, 27), D(2012, 1, 29), "M", "Meath", "Confirmed", "Import-related", "1", False),
        (D(2024, 3, 4), D(2013, 7, 5), "F", "Louth", "Confirmed", "Import-related", "0"),
        (D(2024, 3, 6), D(2006, 2, 18), "M", "Louth", "Confirmed", "Import-related", "0"),
        (D(2024, 3, 9), D(2021, 10, 2), "F", "Louth", "Confirmed", "Import-related", "0"),
        (D(2024, 3, 11), D(2004, 12, 9), "F", "Meath", "Confirmed", "Import-related", "1"),
        (D(2024, 3, 14), D(1997, 3, 3), "M", "Meath", "Confirmed", "Import-related", "0"),
        (D(2024, 3, 15), D(2016, 11, 24), "M", "Meath", "Confirmed", "Import-related", "0"),
        (D(2024, 3, 18), D(1986, 1, 13), "F", "Louth", "Confirmed", "Import-related", "0"),
        (D(2024, 3, 20), D(2002, 5, 26), "M", "Louth", "Confirmed", "Import-related", "0", False),
        (D(2024, 3, 22), D(2023, 4, 18), "M", "Meath", "Confirmed", "Import-related", "0"),
        (D(2024, 3, 25), D(2007, 6, 1), "F", "Meath", "Confirmed", "Import-related", "0"),
        (D(2024, 3, 27), D(2009, 7, 23), "F", "Louth", "Probable", "Import-related", "0"),
        (D(2024, 3, 29), D(1996, 10, 14), "F", "Meath", "Confirmed", "Import-related", "1"),
        (D(2024, 4, 2), D(2018, 3, 27), "F", "Louth", "Confirmed", "Import-related", "0"),
        (D(2024, 4, 5), D(1992, 12, 2), "M", "Louth", "Probable", "Import-related", "0"),
        (D(2024, 4, 9), D(2014, 1, 19), "M", "Meath", "Discarded", "", "2"),
        (D(2024, 4, 12), D(2011, 3, 30), "M", "Meath", "Confirmed", "Import-related", "0"),
    ]
    for row in ob24:
        onset, dob, sex, county, cls, imp, doses = row[:7]
        if len(row) > 7:
            N_(onset, dob, sex, county, cls, imp, doses=doses, outbreak="OB-NE-2024-02", lab=False,
               comments="Reported via OCT line list 2024; hospital laboratory IgM positive, specimen not referred")
        else:
            N_(onset, dob, sex, county, cls, imp, doses=doses, outbreak="OB-NE-2024-02",
               comments="Reported via OCT line list 2024")
    N_(D(2024, 10, 21), D(2003, 9, 19), "M", "Monaghan", "Discarded", "", doses="2")
    N_(D(2025, 1, 15), D(2012, 10, 11), "F", "Meath", "Confirmed", "Imported", doses="0",
       comments="School trip abroad; IgM and PCR positive")
    N_(D(2025, 5, 2), D(1981, 4, 8), "M", "Cavan", "Confirmed", "Imported", doses="Unknown")
    N_(D(2025, 8, 26), D(2019, 6, 30), "F", "Louth", "Confirmed", "Imported", doses="0")
    N_(D(2025, 11, 3), D(2016, 3, 12), "M", "Meath", "Possible", "", doses="1")
    N_(D(2026, 2, 9), D(2005, 7, 27), "F", "Louth", "Confirmed", "Imported", doses="0", lab=False,
       comments="Returned from a festival abroad; IgM positive at the hospital laboratory, not referred")
    N_(D(2026, 4, 30), D(1989, 9, 1), "F", "Meath", "Confirmed", "Imported", doses="1")
    N_(D(2026, 6, 18), D(2024, 9, 13), "M", "Meath", "Confirmed", "Import-related", doses="0",
       comments="Household contact of NDS-26 imported case")
    N_(D(2026, 9, 7), D(2010, 2, 3), "M", "Cavan", "Discarded", "", doses="2")
    # April 2027: an imported case who attended a GP surgery and the emergency department in Navan, two adults infected
    N_(D(2027, 4, 2), D(1996, 5, 21), "M", "Meath", "Confirmed", "Imported", doses="0", hosp="Y",
       comments="Attended GP surgery and Navan ED before diagnosis", tag="index27")
    N_(D(2027, 4, 15), D(1995, 8, 6), "F", "Meath", "Confirmed", "Import-related", doses="0", tag="sec27a", lab=False)
    N_(D(2027, 4, 17), D(1992, 1, 24), "M", "Meath", "Confirmed", "Import-related", doses="Unknown", hosp="Y",
       tag="sec27b")
    N_(D(2027, 5, 29), D(2020, 8, 5), "F", "Louth", "Probable", "Import-related", doses="0")
    # a case notified twice, by the GP and by a hospital, and not linked on the system: two records, one illness
    for onset, dob, note, later, outbreak in RENOTIFIED:
        o = next(r for r in new if r[0] == onset and r[1] == dob)
        kw = dict(o[6])
        kw.pop("tag", None)
        kw.update(comments=note, lab=False, notified=onset + dt.timedelta(days=4 + later))
        if outbreak is not None:
            kw["outbreak"] = outbreak
        new.append(o[:6] + (kw,))
    new.sort(key=lambda r: (r[0], r[1]))
    cnt = {}
    tags = {}
    twin_first = None
    for onset, dob, sex, county, cls, imp, kw in new:
        yr = onset.year
        cnt[yr] = cnt.get(yr, int(rng.integers(30, 90))) + int(rng.integers(5, 60))
        cid = "NDS-%02d-%06d" % (yr % 100, cnt[yr])
        comments = kw.get("comments", "")
        epi = ""
        if dob == D(2010, 4, 16) and onset == D(2024, 2, 18):
            twin_first = cid
        if dob == D(2010, 4, 16) and onset == D(2024, 3, 1):
            epi = twin_first
            comments = "Household contact"
        if kw.get("tag") in ("sec27a", "sec27b"):
            epi = tags["index27"]
            comments = "Contact of index case in Navan ED waiting area"
        if kw.get("tag"):
            tags[kw["tag"]] = cid
        if "Household contact of NDS-26" in comments:
            prev = [c for c in C if c["onset_date"] == D(2026, 4, 30)]
            epi = prev[0]["case_id"] if prev else ""
            comments = "Household contact of imported case"
        row = _case(cid, onset, dob, sex, county, cls, imp, outbreak=kw.get("outbreak", ""), epi=epi,
                    hosp=kw.get("hosp", "N"), doses=kw.get("doses", "0"), comments=comments, kind="new",
                    notified=kw.get("notified"))
        C.append(row)
        if cls in ("Confirmed", "Discarded") and kw.get("lab", True):
            L(cid, onset + dt.timedelta(days=int(rng.integers(1, 5))), "Oral fluid" if rng.random() < 0.5 else "Serum",
              "Measles IgM", "Positive" if cls == "Confirmed" else "Negative")
            if cls == "Confirmed" and rng.random() < 0.6:
                L(cid, onset + dt.timedelta(days=int(rng.integers(1, 5))), "Throat swab", "Measles PCR", "Positive",
                  "B3" if onset.year >= 2023 else "D8")
    # epi links for the 2019 outbreak's new-system contacts: none; a 2021 discarded case links to a legacy one
    # specimen numbers in date order
    lab.sort(key=lambda r: (r["specimen_date"], r["case_id"], r["test"]))
    n = {}
    for r in lab:
        y = r["specimen_date"].year
        n[y] = n.get(y, int(rng.integers(100, 400))) + int(rng.integers(1, 30))
        r["specimen_id"] = "NMRL-%02d-%05d" % (y % 100, n[y])
    C.sort(key=lambda c: c["case_id"])
    return C, lab


# =================================================================================================================
# Distractor records
# =================================================================================================================
def _lot(prod, expiry, v):
    """A batch number in its manufacturer's lot format: MSD numbers M-M-RVAXPRO lots with a letter and six digits, GSK
    numbers Priorix lots A69C, a letter, three digits and A; the letters advance with the date of manufacture, which
    the expiry follows."""
    import hashlib
    h = int(hashlib.sha256(("%s/%d" % (prod, v)).encode()).hexdigest(), 16)
    if prod.startswith("M-M"):
        return "%s%06d" % ("X" if expiry < D(2028, 7, 1) else "Y", h % 40000)
    half = (expiry.year - 2027) * 2 + (expiry.month > 6)
    return "A69C%s%03dA" % ("ABCDE"[half], h % 1000)


def stock():
    """The cold-chain stock return at 30 June 2027: MMR doses by store, product, batch and expiry."""
    rng = np.random.default_rng(W.SEED + 301)
    stores = ["Regional vaccine store, Navan", "Hospital pharmacy, Drogheda", "Hospital pharmacy, Dundalk",
              "Hospital pharmacy, Cavan", "Community vaccine store, Monaghan", "School immunisation team store, Dundalk",
              "School immunisation team store, Navan"]
    rows = []
    for s in stores:
        for prod in ("M-M-RVAXPRO", "Priorix"):
            for b in range(int(rng.integers(1, 4))):
                exp = _rand_date(rng, D(2027, 9, 1), D(2029, 3, 31))
                batch = _lot(prod, exp, int(rng.integers(10000, 99999)))
                doses = int(rng.integers(2, 60)) * 10 if "store" in s else int(rng.integers(3, 40)) * 10
                rows.append(dict(store=s, product=prod, batch=batch, expiry=exp, doses_on_hand=doses,
                                 counted_on=D(2027, 6, 30)))
    return rows

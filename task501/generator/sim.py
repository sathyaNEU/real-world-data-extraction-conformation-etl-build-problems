"""The records the ask reads, drawn from the world: the regional immunisation register's people and MMR events for
births 1993-2017 (with the GP return lines the immunisation office queried and the registrations it merged), and the
distractor's records (the cold-chain stock return). One generator per stream, so a change in one stream never
re-rolls another."""
import datetime as dt

import numpy as np

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
                 "area", "dest", "postcode", "shown_practice", "dob_rec", "twin", "loader_twin", "cotwin")

    def __init__(self, **k):
        self.dob_rec = None       # the date of birth as the register holds it (None: as born)
        self.twin = None          # the co-twin's Person, for a twin pair
        self.loader_twin = False  # a same-sex pair whose practice returns lines without the register number
        self.cotwin = False       # the second-born of a pair, whose doses are its twin's visits
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
    _clear_tenth(people)
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
    # twins born in the region: the second registration of each pair from the end of the spare block
    twins = _twins(np.random.default_rng(W.SEED + 115), people, practices, spare)
    spare = spare[:len(spare) - len(twins)]
    _practice_shown(np.random.default_rng(W.SEED + 109), people)
    _practice_unlisted(np.random.default_rng(W.SEED + 114), people)
    for q in twins:
        p = q.twin
        if p.loader_twin:
            p.shown_practice = p.practice
        q.shown_practice = p.shown_practice
    events = _doses(rng_dose, people)
    merges = _merges(np.random.default_rng(W.SEED + 106), people, events, spare)
    _postcodes(np.random.default_rng(W.SEED + 107), people)
    for q in twins:
        q.postcode = q.twin.postcode
    return people, events, practices, merges


def _tenth(dob):
    return D(dob.year + 10, dob.month, dob.day)


def _clear_tenth(people):
    """C1 for the recorded dates of birth: no child who moved into the region is registered within 60 days after a tenth
    birthday, so a registration that close to the tenth anniversary of a recorded date of birth is a birth
    registration whose date of birth was keyed ten years early. A child registered there is given a registration day
    spread over the rest of its own span (no draw, so no other record moves), the address date kept on or after it and
    the area code read again for that date (Monaghan West recorded from 1 July 2024 is LH26)."""
    for p in people:
        if p.born_in_region:
            continue
        t = _tenth(p.dob)
        if 0 <= (p.registered - t).days <= 60:
            lo, hi = _birthday(p.dob, 1), D(2027, 6, 20)
            span = (hi - lo).days + 1 - 61
            k = (p.dob.toordinal() * 2654435761 + (p.sex == "F")) % span
            day = lo + dt.timedelta(days=k)
            p.registered = day if day < t else day + dt.timedelta(days=61)
            if p.lho_recorded < p.registered:
                p.lho_recorded = p.registered
            if D(2024, 6, 24) <= p.lho_recorded <= D(2024, 7, 8):
                p.lho_recorded = p.lho_recorded + dt.timedelta(days=15)
            if p.status == "resident" and p.area == "LH27":
                p.lho = p.dest = "LH27" if p.lho_recorded < W.CUTOVER else "LH26"


TWIN_SHARE = 0.016        # born-in-region residents with a co-twin (about one baby in thirty is a twin)
TWIN_SAME_SEX = 0.65


def loader_practices(practices):
    """The practices whose MMR returns carry no register number: the return loader matches each of their lines by
    surname, date of birth, sex and practice, and loads it to the first registration that matches."""
    allp = sorted(x for ps in practices.values() for x in ps)
    return set(allp[2::4])


def _twins(rng, people, practices, spare):
    """Twins born in the region, registered together at birth from the same birth notification, at one address and one
    practice. Twins are brought to every visit together, so each has a dose at the same GP visit and at the same school
    session. Same-sex twins at a practice whose returns carry no register number are matched by the loader to the
    first registration of the pair, so both twins' GP lines are loaded there (applied in finish_register)."""
    loader = loader_practices(practices)
    out = []
    base = [p for p in people if p.status == "resident" and p.born_in_region]
    held = {}
    for p in people:
        for k in ((p.dob, p.sex, p.practice), (p.dob, p.sex, p.registered)):
            held[k] = held.get(k, 0) + 1
    for p in sorted(base, key=lambda q: q.pid):
        if rng.random() >= TWIN_SHARE:
            continue
        same = rng.random() < TWIN_SAME_SEX
        alone = held[(p.dob, p.sex, p.practice)] == 1 and held[(p.dob, p.sex, p.registered)] == 1
        if same and p.practice in loader and not alone:
            continue          # C1: a pair the loader joins is the only registration of its birth date and sex at its
            # practice, and on its registration day, so every reading of who the co-twin is finds the same child
        sex = p.sex if same else ("M" if p.sex == "F" else "F")
        q = Person(pid=None, dob=p.dob, sex=sex, lho=p.lho, lho_recorded=p.lho_recorded, registered=p.registered,
                   practice=p.practice, born_in_region=True, status="resident", area=p.area, dest=p.dest, postcode="",
                   shown_practice=p.shown_practice)
        q.twin, p.twin, q.cotwin = p, q, True
        if same and p.practice in loader:
            p.loader_twin = q.loader_twin = True
        for k in ((q.dob, q.sex, q.practice), (q.dob, q.sex, q.registered)):
            held[k] = held.get(k, 0) + 1
        out.append(q)
    for k, q in enumerate(out):
        q.pid = spare[len(spare) - 1 - k]
    people.extend(out)
    return out


def _ni_pupils(rng, practices):
    """Children living in Northern Ireland who go to school in the region. The school immunisation team opens a
    register record at the first session it vaccinates them, with the home address; no local health office covers a
    UK address, so the register can assign the record no area and leaves its code blank (the school's area is kept
    only to place the pupil's school sessions)."""
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
            lho = ""
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


def _practice_unlisted(rng, people):
    """Residents no practice lists: an adult who has not attended a practice since the returns began, or a child whose
    practice closed its list or deregistered the family; the extract shows no practice for them."""
    for p in people:
        if p.status != "resident":
            continue
        share = 0.034 if p.dob.year <= 2004 else 0.011
        if rng.random() < share:
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


ACTIVE = ("resident", "moved", "portlaoise", "ni", "duplicate")


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
    cands = [p for p in people if p.born_in_region and p.status in ACTIVE + ("transferred",) and p.twin is None]
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
    """True doses as the register received them, one event each, before any return-line query. Each dose is a visit;
    a twin's co-twin was vaccinated at the same visits (the schedule's doses, the outbreak clinics), so its doses are
    its twin's visits and take no draws of their own, and a twin of a loader pair has no single GP visit."""
    ev = []
    joint = {}
    for p in people:
        if p.status == "ni" or p.cotwin:
            continue
        y = p.dob.year
        doses = []
        if p.born_in_region:
            sched = 15 if y <= 2007 else 12
            if rng.random() < MMR1_UPTAKE[y]:
                d1 = p.dob + dt.timedelta(days=int(sched * 30.4 + rng.gamma(2.0, 28)))
                doses.append((d1, "GP", True))
                if rng.random() < MMR2_GIVEN_MMR1[y]:
                    if y <= 1994:
                        d2 = _school_session_date(rng, p.dob, 12)
                    else:
                        d2 = _school_session_date(rng, p.dob, 5)
                    doses.append((d2, "School team", True))
            else:
                # catch-up for the scare cohorts (2013 GP catch-up) and late starters; the school team offers a dose at
                # school entry to children with none
                late = 0.30 if 2008 <= y <= 2011 else 0.12
                u = rng.random()
                if u >= late and u < late + 0.16:
                    doses.append((_school_session_date(rng, p.dob, 5 if y > 1994 else 12), "School team", True))
                elif u < late:
                    if 2008 <= y <= 2011:
                        d1 = _rand_date(rng, D(2013, 2, 1), D(2013, 11, 30))
                    else:
                        d1 = p.dob + dt.timedelta(days=int(rng.integers(500, 1900)))
                    doses.append((d1, "GP", True))
                    if rng.random() < 0.55:
                        doses.append((_school_session_date(rng, p.dob, 5 if y > 1994 else 12), "School team", True))
        else:
            # moved in: records from abroad at registration
            if rng.random() < 0.58:
                n = 2 if rng.random() < 0.68 else 1
                d1 = p.dob + dt.timedelta(days=int(rng.integers(370, 560)))
                if d1 < p.registered:
                    doses.append((d1, "Abroad", False))
                    if n == 2:
                        d2 = p.dob + dt.timedelta(days=int(rng.integers(1300, 2300)))
                        if d2 < p.registered:
                            doses.append((d2, "Abroad", False))
        # adult and teenage extra doses
        if y <= 2007 and len(doses) < 2 and rng.random() < 0.10:
            d = _rand_date(rng, max(_birthday(p.dob, 18), D(2011, 1, 1)), D(2027, 6, 26))
            doses.append((d, "GP" if rng.random() < 0.6 else ("Pharmacy" if d >= D(2019, 1, 1) else "GP"), False))
        if y <= 2002 and rng.random() < 0.012:
            d = _rand_date(rng, max(_birthday(p.dob, 20), D(2012, 1, 1)), D(2027, 6, 26))
            doses.append((d, "Occupational health", False))
        # 2019 outbreak response clinics for teenagers and young adults in the outbreak areas
        if 2003 <= y <= 2010 and p.area in ("LH21", "LH22") and len(doses) < 2 and rng.random() < 0.10:
            d = _rand_date(rng, D(2019, 4, 8), D(2019, 6, 14))
            if p.registered < d:
                doses.append((d, "School team", True))
        # 2014 outbreak response: infants aged six to eleven months in Navan and Trim-Kells
        if p.born_in_region and p.area in ("LH22", "LH24") and D(2013, 4, 15) <= p.dob <= D(2013, 10, 31) \
                and rng.random() < 0.34:
            doses.append((_rand_date(rng, D(2014, 3, 17), D(2014, 5, 16)), "Hospital", True))
        if p.loader_twin:
            doses = [x for x in doses if x[2] or x[1] != "GP"]    # no GP visit of one twin alone
        if p.twin is not None:
            doses = [x for x in doses if x[2]]                     # a twin's own extras stay its own
        fb = _birthday(p.dob, 1)
        doses.sort()
        spaced = []
        for d, by, jt in doses:
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
            joint.setdefault(p.pid, []).append((d, by))
    for q in people:
        if q.cotwin:
            for d, by in joint.get(q.twin.pid, []):
                ev.append(Event(eid=None, pid=q.pid, product=None, date=d, given_by=by, source_ref=None, loaded=None,
                                kind="dose", owner=q.pid))
    # a few doses given on 1 and 2 July 2027, loaded before the 3 July run
    adults = [p for p in people if p.dob.year <= 2009 and p.status != "ni" and p.twin is None]
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
            skey = (e.date, p.area, (e.date - p.dob).days >= 9 * 365)
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
        if p.twin is None:
            by_practice.setdefault(p.practice, []).append(p)
    lines = sorted((r for r, e in gp_lines.items() if e.date >= W.QUERY_LOG_START and pmap[e.owner].twin is None),
                   key=lambda r: (gp_lines[r].date, r))
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
    pmap = {p.pid: p for p in people}
    school = [e for e in events if e.given_by == "School team" and e.kind == "dose" and e.date.year >= 2006
              and pmap[e.owner].twin is None]
    pick = rng.choice(len(school), size=min(220, len(school)), replace=False)
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
    # same-sex twins at a practice whose returns carry no register number: the loader matched each GP line to the
    # first registration of the pair, so both twins' lines are loaded there
    for e in events:
        p = pmap.get(e.pid)
        if e.given_by == "GP" and p is not None and p.loader_twin:
            e.pid = min(p.pid, p.twin.pid)
    _typos(np.random.default_rng(W.SEED + 116), people, events, rows_ext + rows_other)
    events.sort(key=lambda e: (e.loaded, e.pid, e.date))
    for k, e in enumerate(events):
        e.eid = "EV%08d" % (31_000_000 + k * 7 + int(rng.integers(0, 6)))
    log = sorted(rows_ext + rows_other, key=lambda r: (r["raised"], r["line_ref"]))
    for k, r in enumerate(log):
        r["query_ref"] = "Q%02d-%05d" % (r["raised"].year % 100, 10000 + k)
    return log


TYPO_SHARE = 0.0016       # birth registrations whose date of birth was keyed with the decade one early


def _typos(rng, people, events, log_rows):
    """Children born in the region whose date of birth the register holds ten years early: the decade keyed one low
    when the record was keyed by hand (a later date could not stand, since the loader refuses a dose dated before the
    birth). The child's records are the child's own: registered from the birth notification, the first dose from the
    GP at the schedule's age, the school's dose with its class. Only the date of birth the extract shows moves."""
    queried = {r["line_ref"] for r in log_rows}
    by_owner = {}
    for e in events:
        by_owner.setdefault(e.owner, []).append(e)
    for p in sorted(people, key=lambda q: q.pid):
        if p.status != "resident" or not p.born_in_region or p.twin is not None or not 2003 <= p.dob.year <= 2017:
            continue
        evs = by_owner.get(p.pid, [])
        if not evs or any(e.pid != p.pid or e.kind != "dose" or e.source_ref in queried for e in evs):
            continue
        gp = sorted(e.date for e in evs if e.given_by == "GP")
        if not gp or not 365 <= (gp[0] - p.dob).days <= 365 + 150 or not 6 <= (p.registered - p.dob).days <= 45:
            continue
        if rng.random() < TYPO_SHARE:
            p.dob_rec = D(p.dob.year - 10, p.dob.month, p.dob.day)


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

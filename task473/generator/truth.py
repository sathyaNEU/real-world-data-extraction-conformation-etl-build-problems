"""The clean truth: every fatal crash in the 14 counties in 2023 to 2025, its persons, each driver's blood alcohol,
who was arrested at the scene and who was tested. The census, the laboratory extract and the crash records extract
are all cut from this; no shipped file is written here."""
import datetime as dt
import math

import numpy as np

import world as W

AGENCY_GROUPS = ("SP", "SO", "PD")
# crash types: SVK single vehicle driver killed; SVS single vehicle driver survived, passenger killed; MVK two
# vehicles, one driver killed; MVS two vehicles, both drivers survived, an occupant killed; PED a pedestrian or
# pedalcyclist killed by a vehicle whose driver survived; MCK motorcycle rider killed (single vehicle)
TYPES = ("SVK", "SVS", "MVK", "MVS", "PED", "MCK")
TYPE_MIX = {"SP": (0.34, 0.10, 0.30, 0.12, 0.08, 0.06),
            "SO": (0.47, 0.13, 0.07, 0.03, 0.13, 0.17),
            "PD": (0.25, 0.13, 0.07, 0.03, 0.41, 0.11)}
YEAR_SHARE = (0.331, 0.333, 0.336)


def rng_for(*keys):
    h = 0
    for k in keys:
        for ch in str(k):
            h = (h * 131 + ord(ch)) % (2 ** 31 - 1)
    return np.random.default_rng((W.SEED * 1000003 + h) % (2 ** 32))


def knobs(fips):
    return dict(zip(W.KNOB_FIELDS, W.KNOBS[fips]))


def _day(rng, year):
    """A crash day: more in summer and on weekends."""
    n = 366 if year % 4 == 0 else 365
    while True:
        d = int(rng.integers(0, n))
        date = dt.date(year, 1, 1) + dt.timedelta(days=d)
        season = 0.80 + 0.35 * math.sin(math.pi * (date.timetuple().tm_yday - 60) / n) ** 2
        wk = 1.25 if date.weekday() >= 4 else 0.9
        if rng.random() < season * wk / 1.6:
            return date


def _time(rng, night):
    if night:
        h = int(rng.choice([20, 21, 22, 23, 0, 1, 2, 3], p=[0.10, 0.12, 0.15, 0.16, 0.15, 0.14, 0.11, 0.07]))
    else:
        h = int(rng.choice(range(6, 20), p=np.array([3, 5, 6, 5, 5, 6, 7, 8, 9, 10, 10, 9, 9, 8]) / 100.0))
    return h, int(rng.integers(0, 60))


def avoid_edges(v):
    """No result sits exactly on .08 or .15, so 'or more' and 'more than' read alike."""
    return round(v + 0.001, 3) if v in (0.080, 0.150) else v


def _bac(rng, band):
    """A blood alcohol in g/dL, three decimals: band -1 sober, 0 from .08 to .149, 1 from .15."""
    if band < 0:
        if rng.random() < 0.86:
            return 0.0
        return round(float(rng.uniform(0.010, 0.079)), 3)
    if band == 0:
        return avoid_edges(round(float(rng.uniform(0.080, 0.1495)), 3))
    v = 0.150 + float(rng.gamma(2.2, 0.035))
    return avoid_edges(round(min(v, 0.392), 3))


def subband(b):
    for i, (lo, hi) in enumerate(W.SUBBANDS):
        if lo <= b < hi:
            return i
    return None


def band_of(b):
    if b is None or b < 0.080:
        return -1
    return 0 if b < 0.150 else 1


class Crash:
    __slots__ = ("cid", "fips", "year", "date", "hour", "minute", "group", "agency", "type", "persons", "hit_run",
                 "night", "seq", "report", "route", "light", "weather", "manner", "lat", "lon", "road_name",
                 "road_class", "municipality", "time_known", "case")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


class Person:
    __slots__ = ("unit", "pno", "role", "age", "sex", "injury", "killed", "death_days", "identified", "bac",
                 "impaired", "band", "tested", "test_type", "arrested", "atfault", "transported", "restraint",
                 "late_death", "body", "rest", "nm_tested")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))

    @property
    def is_driver(self):
        return self.role == "driver"


def _people(rng, ctype, grp):
    """The persons of one crash: drivers (unit 1 at fault), passengers, a non-motorist; who died."""
    ps = []
    def add(unit, role, killed, atfault=False):
        age = int(np.clip(rng.normal(39 if role != "pedestrian" else 46, 16), 15, 92))
        sex = "M" if rng.random() < (0.71 if role == "driver" else 0.52) else "F"
        p = Person(unit=unit, pno=len([q for q in ps if q.unit == unit]) + 1, role=role, age=age, sex=sex,
                   killed=killed, injury="K" if killed else str(rng.choice(["A", "B", "C", "O"],
                                                                         p=[0.22, 0.30, 0.26, 0.22])),
                   death_days=int(rng.choice([0, 0, 0, 0, 1, 2, 3, 5, 9, 16])) if killed else None,
                   identified=True, atfault=atfault, transported=bool(killed or rng.random() < 0.55),
                   restraint=str(rng.choice(["Lap and shoulder", "None used", "Unknown"], p=[0.70, 0.22, 0.08])))
        ps.append(p)
        return p
    if ctype == "SVK":
        add(1, "driver", True, True)
        for _ in range(int(rng.choice([0, 0, 0, 1, 1, 2]))):
            add(1, "passenger", rng.random() < 0.22)
    elif ctype == "MCK":
        add(1, "driver", True, True)
        if rng.random() < 0.15:
            add(1, "passenger", rng.random() < 0.35)
    elif ctype == "SVS":
        add(1, "driver", False, True)
        add(1, "passenger", True)
        for _ in range(int(rng.choice([0, 0, 1]))):
            add(1, "passenger", rng.random() < 0.18)
    elif ctype == "MVK":
        # which driver died: on county and city roads the driver at fault seldom does
        k = 1 if rng.random() < (0.45 if grp == "SP" else 0.15) else 2
        add(1, "driver", k == 1, True)
        add(2, "driver", k == 2, False)
        for u in (1, 2):
            for _ in range(int(rng.choice([0, 0, 0, 1, 1, 2]))):
                add(u, "passenger", rng.random() < 0.12)
    elif ctype == "MVS":
        add(1, "driver", False, True)
        add(2, "driver", False, False)
        add(2 if rng.random() < 0.6 else 1, "passenger", True)
        if rng.random() < 0.3:
            add(1, "passenger", rng.random() < 0.15)
    elif ctype == "PED":
        add(1, "driver", False, True)
        for _ in range(int(rng.choice([0, 0, 0, 1]))):
            add(1, "passenger", False)
        role = "pedestrian" if rng.random() < 0.82 else "pedalcyclist"
        add(2, role, True)
    return ps


def draw():
    """Every crash, by county, with its truth; the exact catch rates at the complete agencies imposed afterwards."""
    crashes = []
    for c in W.COUNTIES:
        f = c["fips"]
        k = knobs(f)
        rng = rng_for("crashes", f)
        n = int(k["crashes3"])
        counts = [int(v) for v in rng.multinomial(n, YEAR_SHARE)]
        seq = 0
        for y, ny in zip(W.YEARS, counts):
            for _ in range(ny):
                seq += 1
                u = rng.random()
                grp = "SP" if u < k["sp"] else ("SO" if u < k["sp"] + k["so"] else "PD")
                # the two sheriffs that follow the State Patrol's procedure patrol its kind of road
                mix = np.array(TYPE_MIX["SP" if grp == "SO" and f in W.PROTOCOL_SHERIFFS else grp])
                if grp != "SP" and k["tilt"]:
                    mix = mix * np.array([1.0, 1 + k["tilt"], 1 - k["tilt"], 1 - k["tilt"], 1 + k["tilt"], 1.0])
                mix = mix / mix.sum()
                ctype = TYPES[int(rng.choice(len(TYPES), p=mix))]
                night = rng.random() < (0.52 if ctype in ("SVK", "SVS", "MCK") else 0.36)
                date = _day(rng, y)
                hh, mm = _time(rng, night)
                ps = _people(rng, ctype, grp)
                cr = Crash(cid="%s-%d-%04d" % (f, y, seq), fips=f, year=y, date=date, hour=hh, minute=mm, group=grp,
                           type=ctype, persons=ps, hit_run=False, night=night, seq=seq)
                crashes.append(cr)
    _agencies(crashes)
    _impairment(crashes)
    _hit_and_run(crashes)
    _tests_and_arrests(crashes)
    _local_found(crashes)
    _single_deaths(crashes)
    _death_dates(crashes)
    return crashes


def _death_dates(crashes):
    """A death after the last crash day of 2025 is moved inside the year (the census is closed on 25 February 2027
    for crashes through 31 December 2025, and none of the window's last crashes' deaths falls in 2026). A few injured
    occupants of crashes in which every driver was tested and below .08 died more than 30 days after the crash; the
    census keeps the officer's injury code and records the date of death."""
    end = dt.date(2025, 12, 31)
    for cr in crashes:
        for p in cr.persons:
            p.late_death = None
            if p.killed and cr.year == 2025 and cr.date + dt.timedelta(days=p.death_days) > end:
                p.death_days = (end - cr.date).days
    cand = []
    for cr in crashes:
        ds = [p for p in cr.persons if p.is_driver]
        if not protocol(cr) or not ds or not all(p.identified and p.tested and p.bac < 0.080 for p in ds):
            continue
        hurt = [p for p in cr.persons if not p.killed and p.role == "passenger" and p.injury == "A"]
        if hurt:
            cand.append((cr, hurt[0]))
    cand.sort(key=lambda t: rng_for("late", t[0].cid).random())
    for cr, p in cand[:7]:
        p.late_death = 31 + int(rng_for("lated", cr.cid).integers(0, 40))
        if cr.year == 2025 and cr.date + dt.timedelta(days=p.late_death) > end:
            p.late_death = None


def _single_deaths(crashes):
    """In a crash at an arrest-only agency whose alcohol status rests on a surviving driver (no killed driver at
    .08 or more), one person died: the extra deaths of such crashes are rare and are kept off them."""
    for cr in crashes:
        if protocol(cr):
            continue
        survivors = [p for p in cr.persons if p.is_driver and p.identified and not p.killed]
        if not survivors:
            continue
        if any(p.is_driver and p.killed and p.impaired for p in cr.persons):
            continue
        killed = [p for p in cr.persons if p.killed]
        for p in killed[1:]:
            p.killed, p.injury, p.death_days = False, "A", None


def _agencies(crashes):
    import agencies as AG
    for cr in crashes:
        rng = rng_for("agency", cr.cid)
        if cr.group == "SP":
            cr.agency = AG.patrol_post(cr.fips)
        elif cr.group == "SO":
            cr.agency = AG.sheriff(cr.fips)
        else:
            cr.agency = AG.city_pd(cr.fips, rng)


def protocol(cr):
    return cr.group == "SP" or (cr.group == "SO" and cr.fips in W.PROTOCOL_SHERIFFS)


def _impairment(crashes):
    """Each driver's impairment and BAC. Killed drivers carry the county's level (pK, adjusted later to the target);
    surviving at-fault drivers carry pP at the complete agencies and pL elsewhere; not-at-fault survivors rarely."""
    for cr in crashes:
        k = knobs(cr.fips)
        rng = rng_for("bac", cr.cid)
        prot = protocol(cr)
        for p in cr.persons:
            if not p.is_driver:
                p.impaired, p.band = False, -1
                p.bac = _bac(rng, -1) if p.killed else None
                if p.killed and p.role in ("pedestrian", "passenger"):
                    r2 = rng_for("nmbac", cr.cid, p.unit, p.pno)
                    if r2.random() < (0.28 if p.role == "pedestrian" else 0.10):
                        p.bac = _bac(r2, 1 if r2.random() < 0.72 else 0)
                continue
            if p.killed:
                base = k["pK"] * (1.25 if cr.night else 0.78) * (1.15 if cr.type in ("SVK", "MCK") else 0.80)
                base *= 1.0 if p.atfault else 0.16
                imp = rng.random() < min(base, 0.85)
                hi = 0.70
            else:
                base = (k["pP"] if prot else k["pL"]) * (1.0 if p.atfault else 0.16)
                base *= (1.20 if cr.night else 0.82)
                imp = rng.random() < min(base, 0.85)
                hi = k["hiP"] if prot else k["hiL"]
            band = (1 if rng.random() < hi else 0) if imp else -1
            p.impaired, p.band, p.bac = imp, band, _bac(rng, band)


def _hit_and_run(crashes):
    """About one pedestrian crash in seven on county and city roads: the driver left and was never identified."""
    for cr in crashes:
        if cr.type != "PED" or cr.group == "SP":
            continue
        rng = rng_for("hr", cr.cid)
        if rng.random() < 0.14:
            cr.hit_run = True
            for p in cr.persons:
                if p.is_driver:
                    p.identified, p.age, p.sex = False, None, None
                    p.impaired, p.band, p.bac = False, -1, None
                    p.injury = "U"


def _tests_and_arrests(crashes):
    """Testing regimes. Killed drivers: the coroner or medical examiner (blood, a few vitreous). Surviving drivers:
    the State Patrol and the Corwin and Ossian sheriffs test every driver; every other agency tests a driver it
    arrests at the scene. Arrests follow the officers' catch rate by BAC band, exactly at the complete agencies."""
    for cr in crashes:
        rng = rng_for("test", cr.cid)
        prot = protocol(cr)
        for p in cr.persons:
            if not p.is_driver or not p.identified:
                p.tested, p.arrested, p.test_type = False, False, None
                continue
            if p.killed:
                p.arrested = False
                p.tested = True
                rng.random()
                p.test_type = "Blood"
                continue
            rate = W.CATCH_SOBER if p.band < 0 else W.CATCH[p.band]
            p.arrested = bool(rng.random() < rate)
            p.tested = True if prot else p.arrested
            p.test_type = "Blood" if p.tested else None
    _exact_catch(crashes)


def _agency_key(cr):
    return "SP" if cr.group == "SP" else cr.agency.aid


def _protocol_group(cr):
    """The State Patrol, or the two sheriffs that follow its procedure, taken together."""
    return "SP" if cr.group == "SP" else "SO"


def _exact_catch(crashes):
    """At the complete agencies: the State Patrol's and the two sheriffs' impaired survivors in each band are made
    a whole multiple of the band's catch denominator (seven at .08 to .149, nine at .15 or more) and the pooled
    sub-bands likewise, then exactly the band rate is arrested within each group's band and every pooled sub-band.
    At the arrest-only agencies each county's arrests in a band are the nearest whole number to the band rate."""
    surv = [(cr, p) for cr in crashes for p in cr.persons if p.is_driver and p.identified and not p.killed]
    prot = [(cr, p) for cr, p in surv if protocol(cr)]
    mult = {0: 7, 1: 9}
    agencies_ = sorted({_protocol_group(cr) for cr, p in prot})
    # 1. each agency's band counts to its target (a whole multiple of the band's denominator)
    for a in agencies_:
        for b in (0, 1):
            pool = [(cr, p) for cr, p in prot if _protocol_group(cr) == a]
            cur = [(cr, p) for cr, p in pool if p.band == b]
            tgt = W.PROTOCOL_TARGETS[a][b]
            if len(cur) > tgt:
                drop = sorted(cur, key=lambda t: rng_for("drop", a, b, t[0].cid, t[1].unit).random())
                for cr, p in drop[:len(cur) - tgt]:
                    rng = rng_for("unimp", cr.cid, p.unit)
                    p.impaired, p.band, p.bac = False, -1, _bac(rng, -1)
            elif len(cur) < tgt:
                cand = sorted([(cr, p) for cr, p in pool if p.band < 0],
                              key=lambda t: (not t[1].atfault, rng_for("add", a, b, t[0].cid, t[1].unit).random()))
                assert len(cand) >= tgt - len(cur), (a, b)
                for cr, p in cand[:tgt - len(cur)]:
                    rng = rng_for("imp", cr.cid, p.unit, b)
                    p.impaired, p.band, p.bac = True, b, _bac(rng, b)
    # 2. pooled sub-band counts to whole multiples, moving drivers between sub-bands of the same band
    for b in (0, 1):
        sbs = [i for i, (lo, hi) in enumerate(W.SUBBANDS) if (lo < 0.150) == (b == 0)]
        rows = [(cr, p) for cr, p in prot if p.band == b]
        n = len(rows)
        assert n % mult[b] == 0
        counts = {i: sum(1 for cr, p in rows if subband(p.bac) == i) for i in sbs}
        target = dict(zip(sbs, W.PROTOCOL_SUBBANDS[b]))
        assert sum(target.values()) == n, (b, n, target)
        over = [i for i in sbs if counts[i] > target[i]]
        under = [i for i in sbs if counts[i] < target[i]]
        for i in over:
            movers = sorted([(cr, p) for cr, p in rows if subband(p.bac) == i],
                            key=lambda t: rng_for("mv", t[0].cid, t[1].unit).random())[:counts[i] - target[i]]
            for cr, p in movers:
                j = next(j for j in under if sum(1 for _, q in rows if subband(q.bac) == j) < target[j])
                lo, hi = W.SUBBANDS[j]
                hi = min(hi, 0.392)
                p.bac = avoid_edges(round(float(rng_for("mvb", cr.cid, p.unit).uniform(lo, hi - 0.0005)), 3))
        for i in sbs:
            assert sum(1 for _, p in rows if subband(p.bac) == i) == target[i], (b, i)
    # 3. arrests: an integer table agency x sub-band with each agency band and each pooled sub-band exact
    for b in (0, 1):
        rate = W.CATCH[b]
        sbs = [i for i, (lo, hi) in enumerate(W.SUBBANDS) if (lo < 0.150) == (b == 0)]
        cells = {(a, i): [(cr, p) for cr, p in prot if p.band == b and _protocol_group(cr) == a and subband(p.bac) == i]
                 for a in agencies_ for i in sbs}
        row_t = {a: int(round(rate * sum(len(cells[(a, i)]) for i in sbs))) for a in agencies_}
        col_t = {i: int(round(rate * sum(len(cells[(a, i)]) for a in agencies_))) for i in sbs}
        assert sum(row_t.values()) == sum(col_t.values())
        alloc = {k: 0 for k in cells}
        # greedy by cell size, proportional first, then fix the margins
        for (a, i), v in cells.items():
            alloc[(a, i)] = min(len(v), int(math.floor(rate * len(v))))
        for _ in range(1000):
            ok = True
            for a in agencies_:
                d = row_t[a] - sum(alloc[(a, i)] for i in sbs)
                for i in sorted(sbs, key=lambda i: -(col_t[i] - sum(alloc[(x, i)] for x in agencies_))):
                    if d == 0:
                        break
                    col_gap = col_t[i] - sum(alloc[(x, i)] for x in agencies_)
                    if d > 0 and alloc[(a, i)] < len(cells[(a, i)]) and col_gap > 0:
                        alloc[(a, i)] += 1
                        d -= 1
                        ok = False
                    elif d < 0 and alloc[(a, i)] > 0 and col_gap < 0:
                        alloc[(a, i)] -= 1
                        d += 1
                        ok = False
            if ok:
                break
        for a in agencies_:
            assert sum(alloc[(a, i)] for i in sbs) == row_t[a], ("row", b, a)
        for i in sbs:
            assert sum(alloc[(a, i)] for a in agencies_) == col_t[i], ("col", b, i)
        for (a, i), v in cells.items():
            v = sorted(v, key=lambda t: rng_for("arr", t[0].cid, t[1].unit).random())
            for j, (cr, p) in enumerate(v):
                p.arrested = j < alloc[(a, i)]
    sober = sorted([(cr, p) for cr, p in prot if p.band < 0], key=lambda t: rng_for("arr0", t[0].cid, t[1].unit).random())
    k = int(round(W.CATCH_SOBER * len(sober)))
    for j, (cr, p) in enumerate(sober):
        p.arrested = j < k
    for cr, p in prot:
        p.tested, p.test_type = True, "Blood"
    # arrest-only agencies
    loc = [(cr, p) for cr, p in surv if not protocol(cr)]
    for c in W.COUNTIES:
        for b in (-1, 0, 1):
            rate = W.CATCH_SOBER if b < 0 else W.CATCH[b]
            items = sorted([t for t in loc if t[0].fips == c["fips"] and t[1].band == b],
                           key=lambda t: rng_for("arrl", t[0].cid, t[1].unit).random())
            k = int(round(rate * len(items)))
            for j, (cr, p) in enumerate(items):
                p.arrested = j < k
    for cr, p in loc:
        p.tested = p.arrested
        p.test_type = "Blood" if p.tested else None


def deaths(cr):
    return sum(1 for p in cr.persons if p.killed)


def ai(cr):
    """Truth: the crash had an identified driver at .08 or more."""
    return any(p.is_driver and p.identified and p.impaired for p in cr.persons)


def observe(crashes):
    """The observed structure the methods read (methods.py), from the truth: what a tested driver's result shows."""
    out = []
    for cr in crashes:
        ds = []
        for p in cr.persons:
            if not p.is_driver:
                continue
            ds.append(dict(killed=p.killed, identified=p.identified, tested=bool(p.tested),
                           bac=p.bac if p.tested else None, arrested=bool(p.arrested),
                           complete=(not p.killed) and protocol(cr), agency=_agency_key(cr)))
        out.append(dict(fips=cr.fips, year=cr.year, deaths=deaths(cr), drivers=ds, cid=cr.cid))
    return out


def set_levels(crashes, vmt):
    """Meet each county's target rate under the golden completion by the killed drivers of single-vehicle crashes
    (whose crash no other driver touches): impaired ones made sober or sober ones impaired, one at a time. The
    complete agencies' catch rates do not move, so each county is levelled on its own crashes."""
    import methods as M
    catch = M.catch_rates(observe(crashes))
    for c in W.COUNTIES:
        f = c["fips"]
        tgt = knobs(f)["target"] * vmt[f] / 1e8
        mine = [cr for cr in crashes if cr.fips == f]
        cand = [cr for cr in mine if cr.type in ("SVK", "MCK")]
        cand.sort(key=lambda cr: rng_for("lvl", cr.cid).random())
        for _ in range(400):
            g = M.route(observe(mine), "G", catch=catch).get(f, 0.0)
            gap = tgt - g
            if abs(gap) < 0.6:
                break
            want = gap > 0
            pick = None
            for cr in cand:
                d = next(p for p in cr.persons if p.is_driver)
                if d.impaired != want and (deaths(cr) <= abs(gap) + 0.5):
                    pick = (cr, d)
                    break
            if pick is None:
                break
            cr, d = pick
            rng = rng_for("lvlb", cr.cid)
            b = (1 if rng.random() < 0.70 else 0) if want else -1
            d.impaired, d.band, d.bac = want, b, _bac(rng, b)
            cand.remove(cr)


def _local_found(crashes):
    """The tuned counties' arrested drivers by band at the arrest-only agencies (world.LOCAL_FOUND): unarrested
    impaired drivers arrested, or arrested ones not, in a fixed random order."""
    for f, tgt in W.LOCAL_FOUND.items():
        loc = [(cr, p) for cr in crashes if cr.fips == f and not protocol(cr)
               for p in cr.persons if p.is_driver and p.identified and not p.killed]
        for b in (0, 1):
            rows = sorted([t for t in loc if t[1].band == b], key=lambda t: rng_for("lf", t[0].cid, t[1].unit).random())
            have = sum(1 for cr, p in rows if p.arrested)
            want = tgt[b]
            assert 0 <= want <= len(rows), (f, b, want, len(rows))
            if want > have:
                for cr, p in [t for t in rows if not t[1].arrested][:want - have]:
                    p.arrested = True
            elif want < have:
                for cr, p in [t for t in rows if t[1].arrested][:have - want]:
                    p.arrested = False
        for cr, p in loc:
            p.tested = p.arrested
            p.test_type = "Blood" if p.tested else None


def build():
    """The truth as every shipped file is cut from it: the crashes drawn, the tuned arrests, the levels met."""
    crashes = draw()
    set_levels(crashes, {c["fips"]: knobs(c["fips"])["vmt3"] * 1e8 for c in W.COUNTIES})
    return crashes

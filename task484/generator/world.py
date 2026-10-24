"""Selwick Basin Clean Air Agency's world: six PM2.5 maintenance areas, every wood-burning appliance in place in the
2014 base year and since, the household that burns in it (its heat status and the wood it burns), the changeout
programme of 2015 to 2024 that funded primary-heat households first, the 2024-25 household survey, and the counties'
remainder outside the areas. Everything else in the pack is written from these objects."""
import datetime as dt

import numpy as np

SEED = 4842
AGENCY = "Selwick Basin Clean Air Agency"
PEOPLE = dict(director="Kylie Maxwell", inventory="Mitchell Conway", programme="Alyssa Jacobs")
EXTRACT_2014 = dt.date(2015, 3, 31)          # the plan's registry extract for the 2014 base year
SEASON = (dt.date(2025, 10, 1), dt.date(2026, 4, 30))
SURVEY_SEASON = "2024-25"
REGISTRY_ASOF = dt.date(2026, 6, 30)
TONS_PER_CORD = 1.163
BAG_LB = 40.0

# area code, name, county, scale, changeout intensity, survey rate, commitment (per cent), the valley's burning
AREAS = [
    ("BRN", "Brannock", "Selwick", 1.00, 0.50, 0.10, 25, 1.00),
    ("IVL", "Ivelton", "Selwick", 0.70, 0.42, 0.14, 22, 1.05),
    ("QRW", "Quarrow", "Corrin", 1.30, 0.18, 0.08, 20, 0.95),
    ("SDY", "Saddeny", "Corrin", 0.50, 0.30, 0.18, 13, 1.10),
    ("WTH", "Wethermoor", "Tamsey", 0.90, 0.08, 0.11, 15, 1.00),
    ("ELK", "Ellick", "Tamsey", 0.60, 0.55, 0.15, 25, 0.92),
]
CODES = [a[0] for a in AREAS]
COUNTIES = ["Selwick", "Corrin", "Tamsey"]

# appliance classes: SCC, description, base-year count at scale 1, primary-heat share, wood burned (cords; pellets in
# tons) for a primary and a secondary household, the current factor and the 2014 tool's factor and default activity
CLASSES = {
    "UNC": ("2104008310", "Woodstove: freestanding, non-EPA certified", 2600, 0.45, 4.2, 1.1, 30.6, 30.6, 2.1),
    "CNC": ("2104008320", "Woodstove: freestanding, EPA certified, non-catalytic", 1500, 0.40, 3.8, 1.0, 14.6, 15.2, 2.1),
    "CAT": ("2104008330", "Woodstove: freestanding, EPA certified, catalytic", 300, 0.40, 3.8, 1.0, 13.0, 13.6, 2.1),
    "PEL": ("2104008400", "Woodstove: pellet-fired", 550, 0.50, 3.2, 0.9, 3.2, 3.1, 1.8),
    "FPL": ("2104008100", "Fireplace: general", 1200, 0.03, 1.0, 0.3, 23.6, 23.6, 0.4),
    "HYD": ("2104008610", "Hydronic heater: outdoor", 220, 0.80, 7.5, 3.0, 18.8, 18.8, 5.0),
}
CL = list(CLASSES)
CHANGED = ("UNC", "HYD")                     # the classes the programme replaced


def tons_of(cl, use):
    """Wood burned in tons: cords at the table's tons per cord, pellets already in tons."""
    return use if cl == "PEL" else use * TONS_PER_CORD


class Device:
    __slots__ = ("did", "area", "county", "cl", "primary", "use", "installed", "registered", "removed", "reason",
                 "parcel", "address", "programme", "replaces", "moved", "split", "late", "survey", "app", "twin")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


def build():
    r = np.random.default_rng(SEED)
    devs, apps = [], []
    nxt = [100000]

    def did():
        nxt[0] += int(r.integers(1, 9))
        return "WD-%06d" % nxt[0]

    for code, name, county, scale, prog, srate, commit, vf in AREAS:
        for cl in CL:
            scc, desc, n0, prim, cp, cs, ef, ef14, dflt = CLASSES[cl]
            n = int(round(scale * n0))
            pr = r.random(n) < prim
            base = np.where(pr, cp, cs) * vf * r.lognormal(-0.08, 0.4, n)
            for i in range(n):
                inst = int(r.integers(1978, 2015))
                reg = dt.date(2010, 6, 1) + dt.timedelta(days=int(r.integers(0, 600))) if inst < 2010 else \
                    dt.date(inst, 1, 1) + dt.timedelta(days=int(r.integers(10, 300)))
                prev = devs[-1] if devs and devs[-1].area == code and devs[-1].cl == cl else None
                if prev is not None and prev.twin is None and r.random() < (0.04 if cl == "FPL" else 0.03):
                    inst, reg = prev.installed, prev.registered          # a second appliance of the same kind
                d = Device(did=did(), area=code, county=county, cl=cl, primary=bool(pr[i]), use=float(base[i]),
                           installed=inst, registered=reg, removed=None, reason=None, programme=False, replaces=None,
                           moved=False, split=None, late=False)
                if prev is not None and inst == prev.installed and reg == prev.registered:
                    d.twin = prev
                    prev.twin = d
                devs.append(d)
            # the changeout: primary-heat households first
            if cl in CHANGED:
                for d in devs[-n:]:
                    p = min(0.95, prog * 1.8) if d.primary else prog * 0.25
                    if r.random() < p:
                        yr = int(r.integers(2015, 2025))
                        d.removed = dt.date(yr, int(r.integers(1, 13 if yr < 2024 else 10)), int(r.integers(1, 28)))
                        d.reason = "Changeout"
                        d.programme = True
            for d in devs[-n:]:
                if d.removed is None and r.random() < (0.03 if cl in CHANGED else 0.04):
                    yr = int(r.integers(2015, 2025))
                    d.removed = dt.date(yr, int(r.integers(1, 13 if yr < 2024 else 10)), int(r.integers(1, 28)))
                    d.reason = str(r.choice(["Home sale removal", "Owner removed", "Demolition"]))
        # each completed changeout: the household's new appliance (or a heat pump), burning about a tenth less
        for d in [x for x in devs if x.area == code and x.programme]:
            new = str(r.choice(["CNC", "PEL", "HP"], p=[0.5, 0.3, 0.2])) if d.cl == "UNC" else "HP"
            apps.append(dict(old=d, new=new))
            if new != "HP":
                when = d.removed + dt.timedelta(days=int(r.integers(1, 20)))
                devs.append(Device(did=did(), area=code, county=county, cl=new, primary=d.primary, use=d.use * 0.9,
                                   installed=when.year, registered=when, removed=None, reason=None, programme=False,
                                   replaces=d.did, moved=False, split=None, late=False))
        # new construction since 2015
        for cl, k in (("CNC", 380), ("PEL", 150)):
            m = int(round(scale * k))
            for i in range(m):
                p = r.random() < 0.35
                yr = int(r.integers(2015, 2026))
                when = dt.date(yr, int(r.integers(1, 13 if yr < 2025 else 7)), int(r.integers(1, 28)))
                devs.append(Device(did=did(), area=code, county=county, cl=cl, primary=bool(p),
                                   use=float((CLASSES[cl][4] if p else CLASSES[cl][5]) * vf * r.lognormal(-0.08, 0.4)),
                                   installed=yr, registered=when, removed=None, reason=None, programme=False,
                                   replaces=None, moved=False, split=None, late=False))
    # late registrations: some pre-2015 appliances first registered after the plan's extract (never changed out)
    for d in devs:
        if d.installed <= 2014 and not d.programme and d.replaces is None and d.twin is None and r.random() < 0.04:
            yl = int(r.integers(2016, 2026))
            d.registered = dt.date(yl, int(r.integers(1, 13 if yl < 2025 else 7)), int(r.integers(1, 28)))
            d.late = True
            if d.removed and d.removed < d.registered:
                d.removed = None
                d.reason = None
    # the 2020 boundary revision: a few parcels at each area's edge leave it (never a changed-out household)
    for d in devs:
        if d.replaces is None and not d.programme and d.installed <= 2014 and d.twin is None and r.random() < 0.012:
            d.moved = True
    # parcels and street addresses; a parcel split re-registers its appliance under a new id and parcel, the old
    # record closed as superseded on the split date, the install year carried over
    streets = ["Alder", "Birch", "Cedar Hollow", "Dogwood", "Elkhorn", "Fir Ridge", "Granite", "Hemlock", "Juniper",
               "Larch", "Maple Bench", "Old Mill", "Pine Flat", "Quarry", "Ridgeview", "Sawmill", "Tamarack", "Willow"]
    used, usedp = set(), set()
    for d in devs:
        k = int(r.integers(10, 9999))
        if d.twin is not None and d.twin.parcel is not None:
            d.parcel, d.address = d.twin.parcel, d.twin.address
            continue
        d.parcel = None
        while d.parcel is None or d.parcel in usedp:
            d.parcel = _parcel(r, d.county)
        usedp.add(d.parcel)
        while True:
            d.address = "%d %s %s" % (k, streets[int(r.integers(len(streets)))], str(r.choice(["Rd", "St", "Ln", "Way", "Dr"])))
            if (d.address, d.county) not in used:
                used.add((d.address, d.county))
                break
            k = int(r.integers(10, 99999))
    for d in devs:
        if d.replaces is None and d.installed <= 2014 and not d.late and not d.moved and d.twin is None and r.random() < 0.025:
            when = dt.date(int(r.integers(2016, 2025)), int(r.integers(1, 13)), int(r.integers(1, 28)))
            if d.removed is not None and d.removed <= when:
                continue
            d.split = when
    return devs, apps


def _parcel(r, county):
    if county == "Selwick":
        return "%02d-%02d-%02d-%d-%03d" % (int(r.integers(10, 30)), int(r.integers(1, 37)), int(r.integers(1, 37)),
                                           int(r.integers(1, 5)), int(r.integers(1, 999)))
    if county == "Corrin":
        return "R%06d" % int(r.integers(100000, 999999))
    return "%04d-%03d-%04d" % (int(r.integers(1, 9999)), int(r.integers(1, 999)), int(r.integers(1, 9999)))


SPLIT_SUFFIX = {"Selwick": lambda p: p[:-3] + "%03d" % ((int(p[-3:]) + 500) % 1000), "Corrin": lambda p: p + "A",
                "Tamsey": lambda p: p[:-4] + "%04d" % ((int(p[-4:]) + 5000) % 10000)}


def base_stock(devs, code, cl):
    """The plan's 2014 base year count: registered by the extract, installed by 2014, in place in 2014, on the 2014
    boundaries (a device whose parcel left the area in 2020 was still in it in 2014)."""
    return [d for d in devs if d.area == code and d.cl == cl and d.replaces is None and d.installed <= 2014
            and d.registered <= EXTRACT_2014 and not d.late]


def in_season(d):
    """In place in the 2025-26 season, on the 2020 boundaries (nothing is installed or removed between 1 July 2025 and
    the registry's extract, so a device in place at the season's start is in place all season)."""
    return (not d.moved) and d.removed is None and d.installed <= 2025


def survey(devs):
    """The 2024-25 household survey: a stratified sample of the appliances in place that season, by area and class,
    at least 30 per stratum; each respondent's weight is the stratum's appliances over its respondents."""
    r = np.random.default_rng(SEED + 7)
    srate = {a[0]: a[5] for a in AREAS}
    out = []
    for code in CODES:
        for cl in CL:
            pool = [d for d in devs if d.area == code and d.cl == cl and not d.moved and d.installed <= 2024
                    and (d.removed is None or d.removed > dt.date(2024, 10, 1)) and d.registered <= dt.date(2024, 10, 1)]
            k = min(len(pool), max(30, int(round(srate[code] * len(pool)))))
            pick = r.choice(len(pool), k, replace=False)
            for j in sorted(pick):
                d = pool[j]
                d.survey = True
                use = d.use * float(r.lognormal(0.0, 0.08))
                if cl == "PEL":
                    unit = "bags" if r.random() < 0.5 else "tons"
                    amt = round(use * 2000 / BAG_LB) if unit == "bags" else round(use * 2) / 2
                    conv = amt * BAG_LB / 2000 if unit == "bags" else amt
                else:
                    u = r.random()
                    unit = "face cords" if u < 0.35 else "pickup loads" if u < 0.5 else "cords"
                    amt = round(use * 3) if unit == "face cords" else round(use * 2) if unit == "pickup loads" else round(use * 4) / 4
                    conv = amt / 3 if unit == "face cords" else amt / 2 if unit == "pickup loads" else amt
                out.append(dict(dev=d, weight=len(pool) / k, amount=amt, unit=unit, use=float(conv)))
    return out


def remainder():
    """The counties outside the areas. The ACS tabulates 2020 block groups; the assessors' GIS still carries the 2010
    block groups, whose codes are the same where a tract kept its number but whose lines were redrawn in some tracts.
    Housing units sit in the overlaps of a 2010 and a 2020 block group; a 2010 block group's units inside an area are a
    fixed share of each of its overlaps (the plans drew the areas on 2010 lines)."""
    r = np.random.default_rng(SEED + 11)
    bg20, bg10, ov = [], [], []
    for ci, county in enumerate(COUNTIES):
        fips = ["53077", "53081", "53083"][ci]
        for t in range(18):
            tract = fips + "%06d" % (950100 + 100 * t)
            redrawn = r.random() < 0.6
            f_in = []
            for b in (1, 2, 3):
                u = r.random()
                f_in.append(1.0 if u < 0.45 else float(np.round(r.uniform(0.15, 0.85), 2)) if u < 0.65 else 0.0)
            hu = np.zeros((3, 3))
            for i10 in range(3):
                for j20 in range(3):
                    if i10 == j20:
                        hu[i10, j20] = int(r.integers(300, 1100))
                    elif redrawn and r.random() < 0.6:
                        hu[i10, j20] = int(r.integers(80, 700))
            for i10 in range(3):
                tot = hu[i10].sum()
                inside = int(round(tot * f_in[i10]))
                bg10.append(dict(geoid=tract + str(i10 + 1), county=county, hu=int(tot), inside=inside))
                for j20 in range(3):
                    if hu[i10, j20]:
                        ov.append(dict(g10=tract + str(i10 + 1), g20=tract + str(j20 + 1), hu=int(hu[i10, j20])))
            for j20 in range(3):
                tot = int(hu[:, j20].sum())
                out = sum(hu[i10, j20] * (1 - f_in[i10]) for i10 in range(3))
                wood = int(round(tot * r.uniform(0.04, 0.16)))
                drift = r.normal(1.04, 0.05)
                bg20.append(dict(geoid=tract + str(j20 + 1), county=county, hu=tot, outside=float(out / tot),
                                 acs1923=wood, moe1923=int(round(wood * r.uniform(0.25, 0.6))) + 9,
                                 acs2024=int(round(wood * drift)), moe2024=int(round(wood * r.uniform(0.25, 0.6))) + 9))
    return dict(bg20=bg20, bg10=bg10, ov=ov)

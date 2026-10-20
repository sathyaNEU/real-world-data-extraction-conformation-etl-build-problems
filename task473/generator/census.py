"""The fatal crash census as the Center keeps it: every crash on a public road in which someone died within 30 days,
each crash's persons, each driver's test and arrest. 2023 is in the 2011 report form's layout (four-digit agency
codes, codes for every field, alcohol results in thousandths); 2024 and 2025 are in the 2024 form's (the new agency
numbers, words for codes, results in g/dL). Also the 2026 preliminary crash file."""
import datetime as dt
import math

import agencies as AG
import geo as G
import truth as T
import world as W

BODY = ("PASSENGER CAR", "SPORT UTILITY VEHICLE", "PICKUP", "VAN", "TRUCK")
BODY_OLD = {"PASSENGER CAR": "01", "SPORT UTILITY VEHICLE": "02", "PICKUP": "03", "VAN": "04", "MOTORCYCLE": "05",
            "TRUCK": "06", "NON-MOTORIST": "00"}
INJ_OLD = {"O": "0", "C": "1", "B": "2", "A": "3", "K": "4", "U": "9"}
ROAD_OLD = {"INTERSTATE": "1", "US ROUTE": "2", "STATE ROUTE": "3", "COUNTY ROAD": "4", "CITY STREET": "5"}
LIGHT = ("DAYLIGHT", "DARK - NOT LIGHTED", "DARK - LIGHTED", "DAWN", "DUSK")
LIGHT_OLD = {v: str(i + 1) for i, v in enumerate(LIGHT)}
WEATHER = ("CLEAR", "RAIN", "SNOW", "FOG", "CLOUDY")
WEATHER_OLD = {v: str(i + 1) for i, v in enumerate(WEATHER)}
COLL = ("NOT A COLLISION WITH A MOTOR VEHICLE", "FRONT TO REAR", "HEAD ON", "ANGLE", "SIDESWIPE")
COLL_OLD = {v: str(i) for i, v in enumerate(COLL)}
REST = ("SHOULDER AND LAP BELT", "NONE USED", "UNKNOWN", "HELMET", "NOT APPLICABLE")
REST_OLD = {"SHOULDER AND LAP BELT": "03", "NONE USED": "20", "UNKNOWN": "99", "HELMET": "05", "NOT APPLICABLE": "00"}

CRASH23_COLS = ["CASE_NUM", "ACC_DATE", "ACC_TIME", "CNTY", "CITY_NAME", "AGCY", "RPT_NUM", "RTE_SYS", "RTE_ID", "LGT",
                "WTHR", "COLL", "VEH_CT", "FATAL_CT", "LAT", "LON"]
PERSON23_COLS = ["CASE_NUM", "VEH_NUM", "PER_NUM", "PER_TYP", "BODY", "AGE", "SEX", "INJ", "DTH_DATE", "HIT_RUN",
                 "REST", "ALC_TST", "ALC_RES", "DWI_ARR"]
CRASH25_COLS = ["crash_id", "crash_date", "crash_time", "county_fips", "municipality", "agency_id", "report_number",
                "road_class", "road_name", "light_condition", "weather", "collision_type", "motor_vehicles",
                "fatalities", "latitude", "longitude"]
PERSON25_COLS = ["crash_id", "unit", "person", "person_type", "unit_type", "age", "sex", "injury", "date_of_death",
                 "hit_and_run", "restraint", "alcohol_test", "alcohol_result", "arrested_at_scene"]
PRELIM_COLS = ["crash_id", "crash_date", "crash_time", "county_fips", "municipality", "agency_id", "report_number",
               "road_class", "road_name", "motor_vehicles", "fatalities", "alcohol_involvement", "record_status"]


def _light(cr):
    h = cr.hour
    m = cr.date.month
    rise, set_ = (7, 17) if m in (11, 12, 1, 2) else ((6, 19) if m in (3, 4, 9, 10) else (5, 20))
    if h == rise:
        return "DAWN"
    if h == set_:
        return "DUSK"
    if rise < h < set_:
        return "DAYLIGHT"
    return "DARK - LIGHTED" if cr.group == "PD" else "DARK - NOT LIGHTED"


def assign(crashes):
    """Identifiers and the crash report's descriptive fields, drawn once per crash from its own stream."""
    order = sorted(crashes, key=lambda cr: (cr.date, cr.hour if cr.hour >= 0 else 99, cr.minute, cr.cid))
    numbers = AG.Numbers()
    for cr in order:
        rng = T.rng_for("ids", cr.cid)
        cr.report = numbers.next(cr.agency, cr.date, int(rng.integers(1, 6)))
        # a county or city agency opens a death investigation when a person dies after the crash report, and
        # the census cites that number; the State Patrol keeps its crash number
        first = min((p.death_days for p in cr.persons if p.killed), default=0)
        if cr.group != "SP" and first > 0:
            cr.census_report = numbers.next(cr.agency, cr.date + dt.timedelta(days=first), 1)
        else:
            cr.census_report = cr.report
        # the road
        if cr.group == "SP":
            roads = G.state_highways(cr.fips)
            name = roads[int(rng.choice(len(roads), p=_road_weights(roads)))]
        elif cr.group == "SO":
            name = (G.COUNTY_ROADS[int(rng.integers(0, len(G.COUNTY_ROADS)))] if rng.random() < 0.7
                    else G.STATE_ROUTES[cr.fips][int(rng.integers(0, 3))])
        else:
            name = G.STREETS[int(rng.integers(0, len(G.STREETS)))]
        cr.road_name = name
        cr.road_class = ("INTERSTATE" if name.startswith("I-") else "US ROUTE" if name.startswith("US ") else
                         "STATE ROUTE" if name.startswith("SR ") else "COUNTY ROAD" if name.startswith("CR ") else
                         "CITY STREET")
        s, n, w, e = G.box(cr.fips)
        cr.lat = round(float(rng.uniform(s + 0.02, n - 0.02)), 5)
        cr.lon = round(float(rng.uniform(w + 0.02, e - 0.02)), 5)
        cr.light = _light(cr)
        cr.weather = WEATHER[int(rng.choice(5, p=[0.71, 0.13, 0.04, 0.03, 0.09]))]
        if cr.type in ("MVK", "MVS"):
            cr.manner = COLL[int(rng.choice([1, 2, 3, 4], p=[0.22, 0.27, 0.41, 0.10]))]
        else:
            cr.manner = COLL[0]
        cr.municipality = cr.agency.city if cr.group == "PD" else ""
        cr.time_known = rng.random() > 0.006
        for p in cr.persons:
            r2 = T.rng_for("unit", cr.cid, p.unit)
            if p.role in ("pedestrian", "pedalcyclist"):
                p.body = "NON-MOTORIST"
            elif cr.type == "MCK" and p.unit == 1:
                p.body = "MOTORCYCLE"
            else:
                p.body = BODY[int(r2.choice(5, p=[0.38, 0.27, 0.22, 0.06, 0.07]))]
            if p.body == "MOTORCYCLE":
                p.rest = "HELMET" if T.rng_for("helm", cr.cid, p.pno).random() < 0.55 else "NONE USED"
            elif p.body == "NON-MOTORIST":
                p.rest = "NOT APPLICABLE"
            else:
                p.rest = {"Lap and shoulder": "SHOULDER AND LAP BELT", "None used": "NONE USED",
                          "Unknown": "UNKNOWN"}[p.restraint]
        # one body type per unit
        bodies = {}
        for p in cr.persons:
            bodies.setdefault(p.unit, p.body)
            p.body = bodies[p.unit]
        # killed non-drivers are tested by the coroner in most cases, some on vitreous humor
        for p in cr.persons:
            if not p.is_driver and p.killed:
                r3 = T.rng_for("nmt", cr.cid, p.unit, p.pno)
                p.nm_tested = r3.random() < (0.86 if p.role == "pedestrian" else 0.71) or p.role == "pedalcyclist"
                p.test_type = ("Vitreous" if r3.random() < 0.12 else "Blood") if p.nm_tested else None
            elif not p.is_driver:
                p.nm_tested = False
    for i, cr in enumerate(o for o in order if o.year == 2023):
        cr.case = "23%04d" % (i + 1)
    for y in (2024, 2025):
        for i, cr in enumerate(o for o in order if o.year == y):
            cr.case = "%d-%05d" % (y, i + 1)
    return order, numbers


def _road_weights(roads):
    w = [3.0 if r.startswith("I-") else 2.0 if r.startswith("US") else 1.0 for r in roads]
    t = sum(w)
    return [x / t for x in w]


def _old_units(cr):
    """The 2011 form numbers motor vehicles 1, 2 and gives non-motorists vehicle number 0, persons numbered within."""
    out = []
    nm = 0
    for p in cr.persons:
        if p.body == "NON-MOTORIST":
            nm += 1
            out.append((0, nm, p))
        else:
            out.append((p.unit, p.pno, p))
    return out


def _new_units(cr):
    """The 2024 form gives every unit a number, a non-motorist its own unit after the vehicles."""
    nveh = max([p.unit for p in cr.persons if p.body != "NON-MOTORIST"] or [0])
    out = []
    k = nveh
    for p in cr.persons:
        if p.body == "NON-MOTORIST":
            k += 1
            out.append((k, 1, p))
        else:
            out.append((p.unit, p.pno, p))
    return out


def _death_date(cr, p):
    if p.killed:
        return cr.date + dt.timedelta(days=p.death_days)
    if p.late_death:
        return cr.date + dt.timedelta(days=p.late_death)
    return None


def _tested(p):
    if p.is_driver:
        return bool(p.tested) and p.identified
    return bool(getattr(p, "nm_tested", False))


def rows_2023(order):
    crash, person = [], []
    for cr in order:
        if cr.year != 2023:
            continue
        nveh = len({p.unit for p in cr.persons if p.body != "NON-MOTORIST"})
        crash.append([cr.case, cr.date.strftime("%m/%d/%Y"),
                      "%02d%02d" % (cr.hour, cr.minute) if cr.time_known else "9999", cr.fips, cr.municipality,
                      cr.agency.old, cr.census_report, ROAD_OLD[cr.road_class], cr.road_name, LIGHT_OLD[cr.light],
                      WEATHER_OLD[cr.weather], COLL_OLD[cr.manner], nveh, T.deaths(cr), "%.5f" % cr.lat,
                      "%.5f" % cr.lon])
        for vn, pn, p in sorted(_old_units(cr), key=lambda t: (t[0] == 0, t[0], t[1])):
            ptype = {"driver": "1", "passenger": "2", "pedestrian": "5", "pedalcyclist": "6"}[p.role]
            dd = _death_date(cr, p)
            if p.is_driver and not p.identified:
                person.append([cr.case, vn, pn, ptype, BODY_OLD[p.body], "999", "9", "9", "", "1", "99", "0", "996",
                               "0"])
                continue
            tested = _tested(p)
            if tested:
                tst = "3" if p.test_type == "Vitreous" else "1"
                res = "%03d" % int(round(p.bac * 1000))
            else:
                tst, res = "0", "996"
            inj = "4" if p.killed else INJ_OLD[p.injury]
            person.append([cr.case, vn, pn, ptype, BODY_OLD[p.body], str(p.age), "1" if p.sex == "M" else "2", inj,
                           dd.strftime("%m/%d/%Y") if dd else "", "0" if p.is_driver else "",
                           REST_OLD[p.rest], tst, res, ("1" if p.arrested else "0") if p.is_driver else ""])
    return crash, person


def rows_2425(order):
    crash, person = [], []
    for cr in order:
        if cr.year == 2023:
            continue
        nveh = len({p.unit for p in cr.persons if p.body != "NON-MOTORIST"})
        crash.append([cr.case, cr.date.isoformat(), "%02d:%02d" % (cr.hour, cr.minute) if cr.time_known else "",
                      cr.fips, cr.municipality, cr.agency.aid, cr.census_report, cr.road_class, cr.road_name, cr.light,
                      cr.weather, cr.manner, nveh, T.deaths(cr), "%.5f" % cr.lat, "%.5f" % cr.lon])
        for un, pn, p in sorted(_new_units(cr), key=lambda t: (t[0], t[1])):
            ptype = p.role.upper()
            dd = _death_date(cr, p)
            if p.is_driver and not p.identified:
                person.append([cr.case, un, pn, ptype, p.body, "", "U", "U", "", "Y", "UNKNOWN", "NOT TESTED", "",
                               "N"])
                continue
            tested = _tested(p)
            if tested:
                tst = "VITREOUS" if p.test_type == "Vitreous" else "BLOOD"
                res = "%.3f" % p.bac
            else:
                tst, res = "NOT TESTED", ""
            inj = "K" if p.killed else p.injury
            person.append([cr.case, un, pn, ptype, p.body, str(p.age), p.sex, inj, dd.isoformat() if dd else "",
                           "N" if p.is_driver else "", p.rest, tst, res,
                           ("Y" if p.arrested else "N") if p.is_driver else ""])
    return crash, person


def prelim_2026_rows():
    """The 2026 crashes reported to the census by the end of February 2027, crash level, alcohol pending."""
    rows = []
    allc = []
    for c in W.COUNTIES:
        f = c["fips"]
        k = T.knobs(f)
        rng = T.rng_for("prelim", f)
        n = int(round(k["crashes3"] / 3.0 * float(rng.uniform(0.86, 1.04))))
        for i in range(n):
            u = rng.random()
            grp = "SP" if u < k["sp"] else ("SO" if u < k["sp"] + k["so"] else "PD")
            a = AG.patrol_post(f) if grp == "SP" else AG.sheriff(f) if grp == "SO" else AG.city_pd(f, rng)
            d = T._day(rng, 2026)
            hh, mm = T._time(rng, rng.random() < 0.42)
            allc.append((d, hh, mm, f, a, grp, rng))
    allc.sort(key=lambda t: (t[0], t[1], t[2], t[3]))
    seqs = {}
    for i, (d, hh, mm, f, a, grp, rng) in enumerate(allc):
        key = a.aid
        per_year = {"State Patrol": 2600, "Sheriff": 900, "Police Department": 1500, "University Police": 140}[a.kind]
        seq = max(int(per_year * d.timetuple().tm_yday / 366.0) + 3, seqs.get(key, 0) + 1)
        seqs[key] = seq
        if grp == "SP":
            roads = G.state_highways(f)
            road = roads[int(rng.integers(0, len(roads)))]
        elif grp == "SO":
            road = G.COUNTY_ROADS[int(rng.integers(0, len(G.COUNTY_ROADS)))]
        else:
            road = G.STREETS[int(rng.integers(0, len(G.STREETS)))]
        rc = ("INTERSTATE" if road.startswith("I-") else "US ROUTE" if road.startswith("US ") else
              "STATE ROUTE" if road.startswith("SR ") else "COUNTY ROAD" if road.startswith("CR ") else "CITY STREET")
        late = d >= dt.date(2026, 11, 1)
        alc = "PENDING" if (late or rng.random() < 0.18) else ("Y" if rng.random() < 0.31 else "N")
        status = "PRELIMINARY" if not late else "PRELIMINARY - INCOMPLETE"
        rows.append(["2026-%05d" % (i + 1), d.isoformat(), "%02d:%02d" % (hh, mm), f, a.city if grp == "PD" else "",
                     a.aid, AG.case_number(a, 2026, seq), rc, road, int(rng.choice([1, 1, 1, 2, 2, 3])),
                     int(rng.choice([1] * 9 + [2])), alc, status])
    return rows

"""The crash records system's 2025 extract of crash reports with an injury or a death: every report version the
investigating agencies filed (originals and supplements), and the units on each. The census's 2025 fatal crashes are
in it as the officers reported them; some crashes were reported by two agencies."""
import datetime as dt

import agencies as AG
import geo as G
import truth as T
import world as W

REPORT_COLS = ["report_id", "version", "version_status", "submitted", "agency_id", "report_number", "crash_date",
               "crash_time", "county_fips", "municipality", "road_class", "road_name", "latitude", "longitude",
               "public_road", "severity", "motor_vehicles", "non_motorists"]
UNIT_COLS = ["report_id", "version", "unit", "unit_type", "driver_age", "driver_sex", "driver_condition",
             "unit_severity"]
CONDITIONS = ("APPARENTLY NORMAL", "HAD BEEN DRINKING", "UNDER THE INFLUENCE OF DRUGS", "ILLNESS", "FATIGUED/ASLEEP",
              "UNKNOWN")
HBD = "HAD BEEN DRINKING"
# injury crashes a year per fatal crash, and the share with a driver an officer reported had been drinking
INJURY_PER_FATAL = {"001": 18.5, "003": 21.0, "005": 17.2, "007": 22.4, "009": 23.6, "011": 21.8, "013": 27.5,
                    "015": 19.1, "017": 20.3, "019": 18.0, "021": 19.6, "023": 23.1, "025": 21.2, "027": 24.8}
HBD_SHARE = {"001": 0.052, "003": 0.061, "005": 0.066, "007": 0.047, "009": 0.043, "011": 0.058, "013": 0.041,
             "015": 0.055, "017": 0.057, "019": 0.063, "021": 0.039, "023": 0.042, "025": 0.045, "027": 0.074}


class Crash:
    __slots__ = ("fips", "date", "hour", "minute", "group", "agency", "road_name", "road_class", "lat", "lon",
                 "public", "severity", "units", "census", "dup", "versions", "key", "municipality")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


def _road(rng, fips, grp):
    if grp == "SP":
        roads = G.state_highways(fips)
        name = roads[int(rng.integers(0, len(roads)))]
    elif grp == "SO":
        name = (G.COUNTY_ROADS[int(rng.integers(0, len(G.COUNTY_ROADS)))] if rng.random() < 0.65
                else G.STATE_ROUTES[fips][int(rng.integers(0, 3))])
    else:
        name = G.STREETS[int(rng.integers(0, len(G.STREETS)))]
    rc = ("INTERSTATE" if name.startswith("I-") else "US ROUTE" if name.startswith("US ") else
          "STATE ROUTE" if name.startswith("SR ") else "COUNTY ROAD" if name.startswith("CR ") else "CITY STREET")
    return name, rc


def _driver(rng):
    return dict(age=int(min(94, max(15, rng.normal(38, 16)))), sex="M" if rng.random() < 0.62 else "F")


def universe(order):
    """Every 2025 crash with an injury or a death, as crashes (each with its true units), before any report is
    written: the census's fatal crashes and the injury crashes."""
    out = []
    fatal25 = [cr for cr in order if cr.year == 2025]
    for cr in fatal25:
        units = []
        for u in sorted({p.unit for p in cr.persons}):
            ps = [p for p in cr.persons if p.unit == u]
            nm = [p for p in ps if p.body == "NON-MOTORIST"]
            if nm:
                p = nm[0]
                units.append(dict(type="PEDESTRIAN" if p.role == "pedestrian" else "PEDALCYCLIST", age=p.age,
                                  sex=p.sex, cond=HBD if (p.bac or 0) >= 0.08 and T.rng_for("nmc", cr.cid).random() < 0.5
                                  else "APPARENTLY NORMAL",
                                  sev="K" if p.killed and p.death_days == 0 else "A" if p.killed else p.injury))
                continue
            d = next((p for p in ps if p.is_driver), None)
            rng = T.rng_for("crscond", cr.cid, u)
            if d is None or not d.identified:
                units.append(dict(type="MOTOR VEHICLE", age=None, sex=None, cond="UNKNOWN", sev="U"))
                continue
            if d.arrested:
                pr = 0.95
            elif d.killed:
                pr = 0.58 if d.impaired else 0.02
            else:
                pr = 0.27 if d.impaired else 0.015
            cond = HBD if rng.random() < pr else ("APPARENTLY NORMAL" if rng.random() < 0.88 else "UNKNOWN")
            sev = min((("K" if p.killed and p.death_days == 0 else "A" if p.killed else p.injury) for p in ps),
                      key="KABCOU".index)
            units.append(dict(type="MOTOR VEHICLE", age=d.age, sex=d.sex, cond=cond, sev=sev))
        sev = "K" if any(p.killed and p.death_days == 0 for p in cr.persons) else "A"
        out.append(Crash(fips=cr.fips, date=cr.date, hour=cr.hour, minute=cr.minute, group=cr.group,
                         agency=cr.agency, road_name=cr.road_name, road_class=cr.road_class, lat=cr.lat, lon=cr.lon,
                         public=True, severity=sev, units=units, census=cr, municipality=cr.municipality))
    for c in W.COUNTIES:
        f = c["fips"]
        k = T.knobs(f)
        rng = T.rng_for("crs", f)
        nf = sum(1 for cr in fatal25 if cr.fips == f)
        n = int(round(nf * INJURY_PER_FATAL[f]))
        for i in range(n):
            u = rng.random()
            sp = 0.55 * k["sp"]
            so = 0.75 * k["so"]
            grp = "SP" if u < sp else ("SO" if u < sp + so else "PD")
            a = AG.patrol_post(f) if grp == "SP" else AG.sheriff(f) if grp == "SO" else AG.city_pd(f, rng)
            day = T._day(rng, 2025)
            night = rng.random() < 0.28
            hh, mm = T._time(rng, night)
            name, rc = _road(rng, f, grp)
            s, nn, w, e = G.box(f)
            nveh = int(rng.choice([1, 2, 2, 2, 3], p=[0.30, 0.20, 0.20, 0.20, 0.10]))
            nonmot = (grp == "PD" and rng.random() < 0.08) or rng.random() < 0.015
            units = []
            hbd = rng.random() < HBD_SHARE[f] * (1.9 if night else 0.65)
            who = int(rng.integers(0, nveh)) if hbd else -1
            for j in range(nveh):
                d = _driver(rng)
                cond = HBD if j == who else ("APPARENTLY NORMAL" if rng.random() < 0.9 else
                                             CONDITIONS[int(rng.choice([2, 3, 4, 5], p=[0.2, 0.15, 0.25, 0.4]))])
                units.append(dict(type="MOTOR VEHICLE", age=d["age"], sex=d["sex"], cond=cond,
                                  sev=str(rng.choice(["A", "B", "C", "O"], p=[0.08, 0.25, 0.37, 0.30]))))
            if nonmot:
                d = _driver(rng)
                units.append(dict(type="PEDESTRIAN" if rng.random() < 0.7 else "PEDALCYCLIST", age=d["age"],
                                  sex=d["sex"], cond=HBD if rng.random() < 0.12 else "APPARENTLY NORMAL",
                                  sev=str(rng.choice(["A", "B", "C"], p=[0.3, 0.4, 0.3]))))
            if not any(x["sev"] in "ABC" for x in units):
                units[0]["sev"] = "C"
            sev = min((x["sev"] for x in units), key="KABCO".index)
            out.append(Crash(fips=f, date=day, hour=hh, minute=mm, group=grp, agency=a, road_name=name,
                             road_class=rc, lat=round(float(rng.uniform(s + 0.02, nn - 0.02)), 5),
                             lon=round(float(rng.uniform(w + 0.02, e - 0.02)), 5),
                             public=rng.random() > (0.035 if grp == "PD" else 0.008), severity=sev, units=units,
                             census=None, municipality=a.city if grp == "PD" else ""))
    # each county's officers noted drinking at one or more of its county and city crashes whose victim died later
    for c in W.COUNTIES:
        late = [x for x in out if x.census is not None and x.fips == c["fips"] and x.group != "SP" and
                x.severity == "A" and any(u["type"] == "MOTOR VEHICLE" and u["age"] is not None for u in x.units)]
        if late and not any(u["cond"] == HBD for x in late for u in x.units):
            x = sorted(late, key=lambda x: T.rng_for("latehbd", x.census.cid).random())[0]
            u = next(u for u in x.units if u["type"] == "MOTOR VEHICLE" and u["age"] is not None)
            u["cond"] = HBD
    out.sort(key=lambda x: (x.date, x.hour, x.minute, x.fips, x.agency.aid))
    for i, x in enumerate(out):
        x.key = i
    return out


def reports(crashes, numbers):
    """Each crash's report by its investigating agency, a second agency's report of some crashes on state roads, the
    supplements and the rejected supplements. Returns the report and unit rows and, per crash, its reports."""
    # which crashes a second agency also reported: on state highways the sheriff, on a state route in a city the
    # police; each county's drinking-driver injury crashes carry at least two such pairs
    by_county = {}
    for x in crashes:
        by_county.setdefault(x.fips, []).append(x)
    for f, xs in by_county.items():
        rng = T.rng_for("dup", f)
        cands = [x for x in xs if x.group == "SP" and x.road_class in ("US ROUTE", "STATE ROUTE", "INTERSTATE")]
        hbd_inj = [x for x in cands if x.census is None and x.public and any(u["type"] == "MOTOR VEHICLE" and
                                                                              u["cond"] == HBD for u in x.units)]
        rng.shuffle(hbd_inj)
        picked = set(id(x) for x in hbd_inj[:2 + int(rng.integers(0, 3))])
        for x in cands:
            if id(x) in picked or rng.random() < 0.035:
                x.dup = AG.sheriff(f)
        fat = [x for x in cands if x.census is not None and x.dup is None]
        if fat and rng.random() < 0.5:
            fat[int(rng.integers(0, len(fat)))].dup = AG.sheriff(f)
    # an injured person in a drinking-driver crash died more than 30 days after it: the agency's supplement records
    # the death (severity K) and the census, which counts deaths within 30 days, leaves the crash out
    late_k = {f: 1 + int(T.rng_for("latek", f).integers(0, 2)) for f in by_county}
    rep_rows, unit_rows = [], []
    rid = 0
    for x in crashes:
        rng = T.rng_for("rep", x.key)
        x.versions = []
        agencies = [(x.agency, x.census.report if x.census is not None else None)]
        if x.dup is not None:
            agencies.append((x.dup, None))
        for k, (a, number) in enumerate(agencies):
            if number is None:
                number = numbers.next(a, x.date, int(rng.integers(0, 4)))
            rid += 1
            report_id = "R25-%07d" % (1000000 + rid * 7 + int(rng.integers(0, 7)))
            hh, mm = x.hour, x.minute
            lat, lon = x.lat, x.lon
            units = [dict(u) for u in x.units]
            if k == 1:
                shift = int(rng.integers(-9, 13))
                if not 0 <= hh * 60 + mm + shift < 1440:
                    shift = -shift
                t = dt.datetime(2025, 1, 1, hh, mm) + dt.timedelta(minutes=shift)
                hh, mm = t.hour, t.minute
                lat = round(lat + float(rng.uniform(-0.0012, 0.0012)), 5)
                lon = round(lon + float(rng.uniform(-0.0012, 0.0012)), 5)
                for u in units:
                    if u["sev"] in "BC" and rng.random() < 0.3:
                        u["sev"] = "B" if u["sev"] == "C" else "C"
            sev = min((u["sev"] for u in units if u["sev"] != "U"), key="KABCO".index) if x.census is None else x.severity
            sub = x.date + dt.timedelta(days=int(rng.integers(1, 12)))
            versions = [(0, "ACCEPTED", sub, sev, units)]
            r = rng.random()
            if r < 0.07 and x.dup is not None:
                u2 = [dict(u) for u in units]
                for u in u2:
                    if u["sev"] in "BC" and rng.random() < 0.5:
                        u["sev"] = "B" if u["sev"] == "C" else "C"
                sev2 = (min((u["sev"] for u in u2 if u["sev"] != "U"), key="KABCO".index)
                        if x.census is None else sev)
                versions.append((1, "ACCEPTED", sub + dt.timedelta(days=int(rng.integers(5, 60))), sev2, u2))
            elif r < 0.07:
                u2 = [dict(u) for u in units]
                j = int(rng.integers(0, len(u2)))
                if u2[j]["type"] == "MOTOR VEHICLE" and x.census is None:
                    if u2[j]["cond"] == "UNKNOWN" and rng.random() < 0.5:
                        u2[j]["cond"] = HBD if rng.random() < 0.35 else "APPARENTLY NORMAL"
                    elif u2[j]["cond"] == HBD and rng.random() < 0.25:
                        u2[j]["cond"] = "APPARENTLY NORMAL"
                    elif u2[j]["sev"] in "BCO":
                        u2[j]["sev"] = str(rng.choice(["A", "B", "C", "O"]))
                sev2 = (min((u["sev"] for u in u2 if u["sev"] != "U"), key="KABCO".index)
                        if x.census is None else sev)
                versions.append((1, "ACCEPTED", sub + dt.timedelta(days=int(rng.integers(5, 60))), sev2, u2))
            elif r < 0.085:
                u2 = [dict(u) for u in units]
                for u in u2:
                    if u["type"] == "MOTOR VEHICLE" and u["cond"] != HBD and rng.random() < 0.5:
                        u["cond"] = HBD
                versions.append((1, "REJECTED", sub + dt.timedelta(days=int(rng.integers(3, 30))), sev, u2))
            acc = [v for v in versions if v[1] == "ACCEPTED"][-1]
            if (k == 0 and x.census is None and x.dup is None and x.public and late_k[x.fips] > 0 and
                    any(u["type"] == "MOTOR VEHICLE" and u["cond"] == HBD for u in acc[4]) and
                    any(u["sev"] == "A" for u in acc[4])):
                late_k[x.fips] -= 1
                u2 = [dict(u) for u in acc[4]]
                next(u for u in u2 if u["sev"] == "A")["sev"] = "K"
                versions.append((len(versions), "ACCEPTED", x.date + dt.timedelta(days=int(rng.integers(34, 80))),
                                 "K", u2))
            for ver, status, when, sv, us in versions:
                nveh = sum(1 for u in us if u["type"] == "MOTOR VEHICLE")
                rep_rows.append([report_id, ver, status, when.isoformat(), a.aid, number, x.date.isoformat(),
                                 "%02d:%02d" % (hh, mm), x.fips, x.municipality, x.road_class, x.road_name,
                                 "%.5f" % lat, "%.5f" % lon, "Y" if x.public else "N", sv, nveh, len(us) - nveh])
                for j, u in enumerate(us):
                    is_mv = u["type"] == "MOTOR VEHICLE"
                    unit_rows.append([report_id, ver, j + 1, u["type"], "" if u["age"] is None else u["age"],
                                      u["sex"] or "", u["cond"], u["sev"] if u["sev"] != "U" else ""])
            x.versions.append(dict(report_id=report_id, agency=a, number=number, versions=versions))
    return rep_rows, unit_rows


def ask_b(crashes):
    """Each county's 2025 crashes on public roads with an injury, no death within 30 days, and a driver an officer
    reported had been drinking (the latest accepted version of each report; a crash counts once)."""
    out = {c["fips"]: 0 for c in W.COUNTIES}
    for x in crashes:
        if x.census is not None or not x.public:
            continue
        hit = False
        for rv in x.versions:
            ver = [v for v in rv["versions"] if v[1] == "ACCEPTED"][-1]
            if ver[3] in ("A", "B", "C", "K") and any(u["type"] == "MOTOR VEHICLE" and u["cond"] == HBD for u in ver[4]):
                hit = True
        out[x.fips] += 1 if hit else 0
    return out

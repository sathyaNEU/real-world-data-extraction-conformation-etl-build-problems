"""What the offices hold, written as they export it: the state crash records extract for the region (crashes, units,
persons in injury crashes), the state's road fatality register, the linear referencing system's road inventory, the
continuous count stations and their hourly volumes, the commission's operator register, the platforms' quarterly
reports, the motor vehicle registrations, and the daily weather and work zone logs."""
import csv
import datetime as dt
import math
from zoneinfo import ZoneInfo

import numpy as np

import common as K
import events as EV
import roads as RD
import world as W

PT = ZoneInfo(K.TZ)
UTC = ZoneInfo("UTC")

BODY_V1 = {"PC": "01", "SUV": "02", "PU": "03", "VAN": "04", "CV": "05", "MB": "06", "BUS": "07", "SUT": "08",
           "TT": "09", "MC": "10", "UNK": "99"}
BODY_V2 = {"PC": "PASSENGER CAR", "SUV": "SPORT UTILITY", "PU": "PICKUP", "VAN": "VAN", "CV": "CARGO VAN",
           "MB": "MINIBUS", "BUS": "BUS", "SUT": "SINGLE-UNIT TRUCK", "TT": "TRUCK-TRACTOR", "MC": "MOTORCYCLE",
           "UNK": "UNKNOWN"}
UTYPE_V1 = {"MV": "1", "PK": "2", "PED": "3", "CYC": "4"}
UTYPE_V2 = {"MV": "MV IN TRANSPORT", "PK": "PARKED MV", "PED": "PEDESTRIAN", "CYC": "PEDALCYCLIST"}
PTYPE_V1 = {"DRIVER": "1", "PASSENGER": "2", "PED": "3", "CYC": "4"}
PTYPE_V2 = {"DRIVER": "DRIVER", "PASSENGER": "PASSENGER", "PED": "PEDESTRIAN", "CYC": "BICYCLIST"}
SEV_V1 = {"K": "1", "A": "2", "B": "3", "C": "4", "O": "5"}
FHE_V1 = {"MV": "01", "PK": "02", "PED": "03", "CYC": "04", "FIXED": "05", "OVERTURN": "06", "ANIMAL": "07",
          "OTHER": "08"}
FHE_V2 = {"MV": "MOTOR VEHICLE IN TRANSPORT", "PK": "PARKED MOTOR VEHICLE", "PED": "PEDESTRIAN",
          "CYC": "PEDALCYCLIST", "FIXED": "FIXED OBJECT", "OVERTURN": "OVERTURN/ROLLOVER", "ANIMAL": "ANIMAL",
          "OTHER": "OTHER OBJECT"}
MANNER = [("REAR END", 0.38), ("ANGLE", 0.30), ("SIDESWIPE SAME DIRECTION", 0.16), ("SIDESWIPE OPPOSITE", 0.05),
          ("HEAD ON", 0.04), ("OTHER", 0.07)]
MANNER_V1 = {"REAR END": "1", "ANGLE": "2", "SIDESWIPE SAME DIRECTION": "3", "SIDESWIPE OPPOSITE": "4",
             "HEAD ON": "5", "OTHER": "6"}
CARRIER_OTHER = {"TB": ["STONEREACH VALLEY TRANSIT", "SV TRANSIT"], "SB": ["STONEREACH SCHOOL DIST", "KELDERWICK USD"],
                 "GV": ["STONEREACH COUNTY", "CITY OF KELDERWICK", "CITY OF FAIRHOLLOW", "STATE DOT"],
                 "EM": ["KELDERWICK FIRE", "STONEREACH CO EMS", "FAIRHOLLOW FIRE"]}


def write_csv(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(head)
        w.writerows(rows)


# ---------------------------------------------------------------------------------------------------------------
# daily weather at the regional airport, and the light at a crash's hour
def weather_days(seed=K.SEED):
    rng = np.random.default_rng(seed * 1000 + 31)
    out = {}
    d = dt.date(2021, 1, 1)
    wet = False
    while d <= dt.date(2026, 9, 30):
        m = d.month
        pw = [0.62, 0.55, 0.52, 0.42, 0.32, 0.22, 0.08, 0.09, 0.18, 0.38, 0.58, 0.63][m - 1]
        p = min(0.92, pw + (0.18 if wet else -0.08))
        wet = bool(rng.random() < p)
        tmax = 46 + 32 * math.sin(math.pi * (d.timetuple().tm_yday - 105) / 365.0) ** 2 * (1 if 3 < m < 11 else 0.4)
        tmax = round(tmax + rng.normal(0, 5), 0)
        tmin = round(tmax - 14 - rng.uniform(0, 8), 0)
        prcp = round(float(rng.gamma(1.4, 0.18)), 2) if wet else 0.0
        snow = round(prcp * 9.5, 1) if (wet and tmax < 36) else 0.0
        out[d] = dict(prcp=prcp, snow=snow, tmax=tmax, tmin=tmin, awnd=round(float(rng.gamma(3.0, 2.4)), 1))
        d += dt.timedelta(days=1)
    return out


def light(day, minute, ur):
    doy = day.timetuple().tm_yday
    decl = 23.44 * math.sin(math.radians(360.0 * (284 + doy) / 365.0))
    lat = 45.6
    x = -math.tan(math.radians(lat)) * math.tan(math.radians(decl))
    half = math.degrees(math.acos(max(-1.0, min(1.0, x)))) / 15.0
    noon = 12.0 + 0.2 + (1.0 if _dst(day) else 0.0)
    rise, sett = noon - half, noon + half
    t = minute / 60.0
    if abs(t - rise) < 0.4:
        return "DAWN"
    if abs(t - sett) < 0.4:
        return "DUSK"
    if rise < t < sett:
        return "DAYLIGHT"
    return "DARK-LIGHTED" if ur == "U" else "DARK-NOT LIGHTED"


def _dst(day):
    return bool(dt.datetime(day.year, day.month, day.day, 12, tzinfo=PT).dst())


# ---------------------------------------------------------------------------------------------------------------
class Writer:
    def __init__(self, w, seed=K.SEED):
        self.w = w
        self.seed = seed
        self.rng = np.random.default_rng(seed * 1000 + 37)
        self.wx = weather_days(seed)
        self.segs = w["segs"]
        self.assign_ids()

    def assign_ids(self):
        rng = self.rng
        lag = {"SP6": (3, 12), "SCSO": (5, 30), "KPD": (2, 10), "FPD": (4, 20)}
        rec = []
        for i, cr in enumerate(self.w["crashes"]):
            lo, hi = lag[cr["agency"]]
            rec.append((cr["date"] + dt.timedelta(days=int(rng.integers(lo, hi + 1))), i))
        seq = {}
        for when, i in sorted(rec):
            cr = self.w["crashes"][i]
            y = cr["year"]
            seq[y] = seq.get(y, 0) + 1 + int(rng.random() < 0.03)
            cr["id"] = "%d-%06d" % (y, seq[y])
        aseq = {}
        for cr in self.w["crashes"]:
            k = (cr["agency"], cr["year"])
            aseq[k] = aseq.get(k, 0) + 1
            n, yy = aseq[k], cr["year"] % 100
            cr["rpt"] = {"SP6": "D6-%02d-%05d" % (yy, n), "SCSO": "SO%02d-%05d" % (yy, n),
                         "KPD": "K%02d%06d" % (yy, n), "FPD": "%02dFH%05d" % (yy, n)}[cr["agency"]]
            cr["v2"] = cr["date"] >= K.FORM_V2
            cr["time_known"] = bool(rng.random() > (0.004 if cr["agency"] in ("SCSO", "KPD") else 0.0))
            cr["manner"] = EV.pick(rng, MANNER) if cr["kind"] == "MV" else None
            if cr["kind"] == "SV":
                cr["fhe"] = EV.pick(rng, [("FIXED", 0.60), ("OVERTURN", 0.15), ("ANIMAL", 0.15 if cr["ur"] == "R"
                                                                                          else 0.04), ("OTHER", 0.10)])
            else:
                cr["fhe"] = cr["kind"]
            for v in cr["units"]:
                v["name"] = ""
                if v.get("use") in EV.OPERATORS and not v["fled"]:
                    reg = [o for o in EV.OPERATORS[v["use"]] if o[0] == v["op"]][0]
                    v["name"] = reg[1][int(rng.integers(0, len(reg[1])))]
                    if (not cr["v2"]) and rng.random() < 0.02:
                        v["name"] = ""
                elif v.get("use") == "OC" and not v["fled"]:
                    v["name"] = EV.OTHER_CARRIERS[int(rng.integers(0, len(EV.OTHER_CARRIERS)))]
                elif v.get("use") in CARRIER_OTHER and not v["fled"]:
                    v["name"] = CARRIER_OTHER[v["use"]][int(rng.integers(0, len(CARRIER_OTHER[v["use"]])))]
                if v["fault"] or v.get("fault2"):
                    v["code"] = (EV.NM_FAULT_CODES if v["type"] in ("PED", "CYC") else EV.AT_FAULT_CODES)[
                        int(rng.integers(0, 4 if v["type"] in ("PED", "CYC") else len(EV.AT_FAULT_CODES)))]

    # ---- the crash table
    def crash_rows(self):
        head = ["CRASH_ID", "FORM_VERSION", "AGENCY", "AGENCY_REPORT_NO", "CRASH_DATE", "CRASH_TIME", "TIME_ZONE",
                "ROUTE_ID", "LOC_ROUTE", "MILEPOST", "F_SYSTEM", "URBAN_RURAL", "CITY", "FIRST_HARMFUL_EVENT",
                "MANNER_OF_COLLISION", "NUM_UNITS", "AT_FAULT_UNIT", "HIT_AND_RUN", "LIGHT_CONDITION", "WEATHER",
                "ROAD_SURFACE", "CRASH_SEVERITY", "NUM_KILLED", "NUM_INJURED"]
        rows = []
        for cr in sorted(self.w["crashes"], key=lambda c: c["id"]):
            v2 = cr["v2"]
            local = dt.datetime(cr["date"].year, cr["date"].month, cr["date"].day, cr["minute"] // 60,
                                cr["minute"] % 60, tzinfo=PT)
            if cr["agency"] == "SP6":
                u = local.astimezone(UTC)
                date, time, tz = u.date().isoformat(), "%02d:%02d" % (u.hour, u.minute), "UTC"
            else:
                date, tz = cr["date"].isoformat(), "PT"
                h, mi = cr["minute"] // 60, cr["minute"] % 60
                if cr["agency"] == "SCSO":
                    time = "%02d:%02d" % (h, mi)
                elif cr["agency"] == "KPD":
                    time = "%d:%02d %s" % ((h % 12) or 12, mi, "AM" if h < 12 else "PM")
                else:
                    time = str(h * 100 + mi)
            if not cr["time_known"]:
                time = ""
            if cr["located"]:
                rid = cr["route"] if v2 else ""
                old = "" if v2 else RD.old_route_id(cr["route"])
                mp = "%.2f" % cr["mp"]
                fs, ur = (str(cr["fc"]), cr["ur"]) if v2 else ("", "")
            else:
                rid = old = mp = fs = ur = ""
            city = cr["city"].upper()
            fault_units = [v["no"] for v in cr["units"] if v["fault"]]
            if v2:
                atf = "0" if cr["undetermined"] else str(fault_units[0])
            else:
                atf = ""
            hr = "Y" if any(v["fled"] for v in cr["units"]) else "N"
            wx = self.wx[cr["date"]]
            rain = wx["prcp"] > 0.02 and self.rng.random() < 0.75
            weather = ("SNOW" if wx["snow"] > 0 else "RAIN") if rain else ("CLOUDY" if self.rng.random() < 0.35
                                                                            else "CLEAR")
            surf = ("SNOW/ICE" if wx["snow"] > 0 else "WET") if rain else "DRY"
            sev = min((p["sev"] for p in cr["persons"]), key="KABCO".index, default="O")
            nk = sum(1 for p in cr["persons"] if p["sev"] == "K")
            ni = sum(1 for p in cr["persons"] if p["sev"] in "ABC")
            fhe = (FHE_V2 if v2 else FHE_V1)[cr["fhe"]]
            manner = ""
            if cr["kind"] == "MV":
                manner = cr["manner"] if v2 else MANNER_V1[cr["manner"]]
            rows.append([cr["id"], "PTCR-23" if v2 else "PTCR-16", cr["agency"], cr["rpt"], date, time, tz, rid, old,
                         mp, fs, ur, city, fhe, manner, len(cr["units"]), atf, hr,
                         light(cr["date"], cr["minute"], cr["ur"]), weather, surf,
                         sev if v2 else SEV_V1[sev], nk, ni])
        return head, rows

    # ---- the unit table
    def unit_rows(self):
        head = ["CRASH_ID", "UNIT_NO", "UNIT_TYPE", "BODY_TYPE", "VEH_USE", "CARRIER_NAME", "CONTRIB_CODE",
                "HIT_RUN_UNIT", "OCCUPANTS", "DRIVER_AGE", "MODEL_YEAR", "STRIKING_UNIT"]
        rows = []
        for cr in sorted(self.w["crashes"], key=lambda c: c["id"]):
            v2 = cr["v2"]
            veh = [v for v in cr["units"] if v["type"] in ("MV", "PK")]
            for v in cr["units"]:
                t = v["type"]
                ut = (UTYPE_V2 if v2 else UTYPE_V1)[t]
                if t in ("PED", "CYC"):
                    body = use = name = occ = age = my = ""
                    strike = str(veh[0]["no"]) if v2 else ""
                else:
                    strike = ""
                    if v["fled"]:
                        b, u = "UNK", "UNK"
                    else:
                        b, u = v["body"], ("PV" if v["use"] == "MC" else v["use"])
                    body = (BODY_V2 if v2 else BODY_V1)[b]
                    use = (K.USE_V2 if v2 else K.USE_V1)[u]
                    name = v["name"]
                    occ = "" if v["fled"] else str(v["occ"])
                    age = "" if (v["fled"] or t == "PK") else str(v["age"])
                    my = "" if v["fled"] else str(v["vyear"])
                code = ""
                if not v2:
                    code = "00"
                    if not cr["undetermined"] and (v["fault"] or v.get("fault2")):
                        code = v["code"]
                rows.append([cr["id"], v["no"], ut, body, use, name, code, "Y" if v["fled"] else "N", occ, age, my,
                             strike])
        return head, rows

    # ---- persons in crashes with an injury on the report or a supplement
    def person_rows(self):
        head = ["CRASH_ID", "UNIT_NO", "PERSON_NO", "PERSON_TYPE", "SEAT_POSITION", "AGE", "SEX",
                "INJURY_SEVERITY"]
        rows = []
        for cr in sorted(self.w["crashes"], key=lambda c: c["id"]):
            ps = cr["persons"]
            if not any(p["sev"] != "O" or p["final"] != "O" for p in ps):
                continue
            v2 = cr["v2"]
            n = 0
            for p in ps:
                n += 1
                p["pno"] = n
                rows.append(self._prow(cr, p, n, p["sev"], v2))
            for p in ps:
                if p["supp"]:
                    n += 1
                    rows.append(self._prow(cr, p, n, p["final"], v2))
        return head, rows

    @staticmethod
    def _prow(cr, p, n, sev, v2):
        return [cr["id"], p["unit"], n, (PTYPE_V2 if v2 else PTYPE_V1)[p["role"]], p["seat"], p["age"], p["sex"],
                sev if v2 else SEV_V1[sev]]

    # ---- the state's register of road deaths within 30 days
    def fatality_rows(self):
        head = ["REGISTER_NO", "COUNTY", "AGENCY", "AGENCY_REPORT_NO", "CRASH_DATE", "DATE_OF_DEATH", "VEHICLE_NO",
                "PERSON_TYPE", "AGE", "SEX"]
        out = []
        for cr in self.w["crashes"]:
            for p in cr["persons"]:
                if p["died30"]:
                    dd = cr["date"] + dt.timedelta(days=p["death_day"])
                    out.append((dd, cr["date"], cr["agency"], cr["rpt"], p["unit"], PTYPE_V2[p["role"]], p["age"],
                                p["sex"]))
        out.sort()
        rows = []
        for i, (dd, cd, ag, rpt, unit, pt, age, sex) in enumerate(out, 1):
            rows.append(["F%d-%04d" % (dd.year, i), "STONEREACH", K.AGENCIES[ag], rpt, cd.isoformat(), dd.isoformat(),
                         unit, pt, age, sex])
        return head, rows

    # ---- weather (a distractor) and work zones (a distractor)
    def weather_rows(self):
        head = ["STATION", "NAME", "DATE", "AWND", "PRCP", "SNOW", "TMAX", "TMIN"]
        rows = []
        for d in sorted(self.wx):
            if d > dt.date(2025, 12, 31):
                continue
            x = self.wx[d]
            rows.append(["USW00094741", "KELDERWICK REGIONAL AIRPORT", d.isoformat(), "%.1f" % x["awnd"],
                         "%.2f" % x["prcp"], "%.1f" % x["snow"], "%d" % x["tmax"], "%d" % x["tmin"]])
        return head, rows

    def workzone_rows(self):
        rng = np.random.default_rng(self.seed * 1000 + 41)
        cands = [s for s in self.segs if s["fc"] <= 4]
        head = ["WZ_ID", "ROUTE_ID", "BEGIN_MP", "END_MP", "START_DATE", "END_DATE", "WORK_TYPE", "LANES_CLOSED",
                "NIGHT_ONLY"]
        rows = []
        types = ["PAVING", "BRIDGE DECK", "STRIPING", "UTILITY", "SIGNAL UPGRADE", "GUARDRAIL", "SHOULDER WORK"]
        for i in range(340):
            s = cands[int(rng.integers(0, len(cands)))]
            st = dt.date(2021, 3, 1) + dt.timedelta(days=int(rng.integers(0, 1700)))
            en = st + dt.timedelta(days=int(rng.integers(2, 120)))
            b = round(float(rng.uniform(s["b"], s["e"])), 2)
            rows.append(["WZ%05d" % (21000 + i * 3), s["route"], "%.2f" % b, "%.2f" % min(s["e"], b + rng.uniform(0.2, 2.5)),
                         st.isoformat(), en.isoformat(), types[int(rng.integers(0, len(types)))],
                         int(rng.integers(0, 3)), "Y" if rng.random() < 0.3 else "N"])
        rows.sort(key=lambda r: (r[4], r[0]))
        return head, rows


# ---------------------------------------------------------------------------------------------------------------
# continuous count stations: hourly volumes, both directions, 2025
def atr_rows(segs, sts, seed=K.SEED):
    rng = np.random.default_rng(seed * 1000 + 43)
    days = [dt.date(2025, 1, 1) + dt.timedelta(days=i) for i in range(365)]
    spring = [d for d in days if d.month == 3 and d.weekday() == 6][1]
    fall = [d for d in days if d.month == 11 and d.weekday() == 6][0]
    head = ["STATION_ID", "COUNT_DATE", "DIR"] + ["HR%02d" % h for h in range(1, 25)]
    rows = []
    for st in sts:
        g = st["group"]
        hours, wef = W.GROUP_HOURS[g]
        ur = st["ur"]
        nwd = sum(1 for d in days if d.weekday() < 5)
        nwe = 365 - nwd
        fw = 365.0 / (nwd + wef * nwe)
        mf = W.MONTH[ur]
        mean_m = sum(mf[d.month - 1] for d in days) / 365.0
        dirs = ("1", "5") if st["route"].startswith(("I-", "SR-")) and int(st["route"].split("-")[1]) % 2 == 1 \
            else ("3", "7")
        out = set()
        for _ in range(int(rng.poisson(1.6))):
            s0 = int(rng.integers(0, 360))
            for k in range(int(rng.integers(1, 10))):
                out.add((s0 + k, "both"))
        for _ in range(int(rng.poisson(1.0))):
            out.add((int(rng.integers(0, 365)), dirs[int(rng.integers(0, 2))]))
        for i, d in enumerate(days):
            if (i, "both") in out:
                continue
            dtp = "we" if d.weekday() >= 5 else "wd"
            daily = st["aadt"] * fw * (wef if dtp == "we" else 1.0) * mf[d.month - 1] / mean_m \
                * float(np.exp(rng.normal(0, 0.05)))
            prof = hours[dtp] * np.exp(rng.normal(0, 0.06, 24))
            prof = prof / prof.sum()
            vol = daily * prof
            amp = 0.10 if ur == "U" else 0.04
            share1 = 0.5 + amp * (W.bump(np.arange(24), 7.5, 1.6) - W.bump(np.arange(24), 17.0, 2.0))
            for j, dr in enumerate(dirs):
                if (i, dr) in out:
                    continue
                v = vol * (share1 if j == 0 else 1 - share1)
                cells = [str(int(round(x))) for x in v]
                if d == spring:
                    cells[2] = ""
                if d == fall:
                    cells[1] = str(int(round(v[1] * 2)))
                rows.append([st["id"], d.isoformat(), dr] + cells)
    return head, rows


def station_rows(sts, segs):
    head = ["STATION_ID", "ROUTE_ID", "MILEPOST", "F_SYSTEM", "URBAN_RURAL", "FACTOR_GROUP", "LOCATION", "DIRECTIONS"]
    gnum = {g: i + 1 for i, g in enumerate(K.GROUPS)}
    rows = []
    for st in sts:
        s = segs[st["seg"]]
        city = (s["city"] or "Stonereach County").replace("Stonereach County", "unincorporated")
        dirs = "1,5" if st["route"].startswith(("I-", "SR-")) and int(st["route"].split("-")[1]) % 2 == 1 else "3,7"
        rows.append([st["id"], st["route"], "%.2f" % st["mp"], st["fc"], st["ur"], gnum[st["group"]],
                     "%s MP %.2f (%s)" % (st["route"], st["mp"], city), dirs])
    return head, rows

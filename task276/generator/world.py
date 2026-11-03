"""The clean truth: the service's drivers and their bodies, the cab fit programme's measurements, the shortlisted cabs'
geometry, and the front-line fleet's year (vehicles, telematics units, mileage, workshop jobs, days off the road).
Everything shipped is an honest record of this world, written by pack.py through each producing system's own habits."""
import datetime as dt
import math
import random

import params as P

D = dt.timedelta


# ----------------------------------------------------------------------------------------------- geometry
def inches(v):
    return v * 25.4


def posture(stature, weight, seh, h30):
    """the service's driver posture model: hip point x, torso angle (degrees), eye point (x, z)"""
    m = P.POSTURE
    bmi = weight / (stature / 1000.0) ** 2
    xh = m["hx0"] + m["hx_s"] * (stature - m["s0"]) + m["hx_b"] * (bmi - m["b0"]) + m["hx_h"] * (h30 - m["h0"])
    th = m["t0"] + m["t_s"] * (stature - m["s0"]) + m["t_b"] * (bmi - m["b0"])
    return xh, th, xh + m["ex"], h30 + m["ez"] * seh, bmi


def backrest_corner(xh, th, h30):
    a = math.radians(th)
    L, Dd = inches(P.SEAT_IN["backrest_along"]), inches(P.SEAT_IN["backrest_behind"])
    return xh + L * math.sin(a) + Dd * math.cos(a), h30 + L * math.cos(a) - Dd * math.sin(a)


def bulkhead_x(cab, z):
    x0, x1 = cab["bulkhead"]
    return x0 + (x1 - x0) * z / P.BULKHEAD_TOP_Z


def sight(cab, xe, ze):
    ch = P.CHASSIS[cab["chassis"]]
    (xu, zu), (xd, zd) = ch["header"], ch["bonnet"]
    up = math.degrees(math.atan2(zu - ze, xe - xu))
    dn = math.degrees(math.atan2(ze - zd, xe - xd))
    return up, dn


def assess(cab, stature, weight, seh):
    """every quantity the fit standard turns on, for one driver in one cab"""
    h30 = cab["h30"]
    xh, th, xe, ze, bmi = posture(stature, weight, seh, h30)
    bx, bz = backrest_corner(xh, th, h30)
    up, dn = sight(cab, xe, ze)
    t0, t1 = cab["travel"]
    return {"xh": xh, "th": th, "xe": xe, "ze": ze, "bx": bx, "bz": bz, "bulk": bulkhead_x(cab, bz), "up": up, "dn": dn,
            "in_travel": t0 <= xh <= t1, "recline_ok": P.SEAT_IN["recline_min"] <= th <= P.SEAT_IN["recline_max"],
            "vision": up >= P.VISION["up_deg"] and dn >= P.VISION["down_deg"], "clear": bx <= bulkhead_x(cab, bz),
            "margins": (abs(xh - t0), abs(xh - t1), abs(up - P.VISION["up_deg"]), abs(dn - P.VISION["down_deg"]),
                        abs(bx - bulkhead_x(cab, bz)))}


def fits(a):
    return a["in_travel"] and a["recline_ok"] and a["vision"] and a["clear"]


# ----------------------------------------------------------------------------------------------- people
def _numbers(rnd, n, lo, hi):
    out = set()
    while len(out) < n:
        out.add(rnd.randint(lo, hi))
    v = list(out)
    rnd.shuffle(v)
    return v


def _date_between(rnd, a, b):
    return a + D(days=rnd.randint(0, (b - a).days))


def _body(rnd, sex):
    s = rnd.gauss(*P.STATURE[sex])
    bmi = min(47.0, max(18.5, rnd.lognormvariate(math.log(P.BMI[sex]), P.BMI_SPREAD)))
    seh = s * rnd.gauss(P.SEH_RATIO[sex], P.SEH_SPREAD)
    return {"stature": s, "weight": bmi * (s / 1000.0) ** 2, "seh": seh}


def _record(rnd, body, imperial):
    """one OH measurement as recorded: the instrument's error, then the form's precision"""
    s = body["stature"] + rnd.gauss(0, 3.0)
    e = body["seh"] + rnd.gauss(0, 4.0)
    w = body["weight"] + rnd.gauss(0, 0.8)
    if imperial:
        tot_in = round(s / 25.4 * 4) / 4.0
        ft = int(tot_in // 12)
        inch = tot_in - 12 * ft
        e_in = round(e / 25.4 * 4) / 4.0
        lb_tot = int(round(w / 0.45359237))
        st, lb = lb_tot // 14, lb_tot % 14
        return {"units": "imperial", "ft": ft, "in": inch, "seh_in": e_in, "st": st, "lb": lb,
                "stature": (12 * ft + inch) * 25.4, "seh": e_in * 25.4, "weight": (14 * st + lb) * 0.45359237}
    return {"units": "metric", "stature": float(int(round(s))), "seh": float(int(round(e))),
            "weight": round(w, 1)}


def _clear(rec):
    for cab in P.CABS:
        a = assess(cab, rec["stature"], rec["weight"], rec["seh"])
        m = a["margins"]
        if m[0] < P.DEAD_ZONE_MM or m[1] < P.DEAD_ZONE_MM or m[4] < P.DEAD_ZONE_MM:
            return False
        if m[2] < P.DEAD_ZONE_DEG or m[3] < P.DEAD_ZONE_DEG:
            return False
    return True


def people(rnd):
    hubs = {h[0]: h for h in P.HUBS}
    n_roster = sum(int(round(h[3] * rnd.uniform(0.985, 1.015))) for h in P.HUBS)
    n_other = 286
    service = _numbers(rnd, n_roster + n_other + 40, 20000000, 79999999)
    legacy = _numbers(rnd, 1600, 10000, 99999)
    staff = []
    k = 0
    for code, name, area, n in P.HUBS:
        n = int(round(n * rnd.uniform(0.985, 1.015)))
        for _ in range(n):
            staff.append({"service": str(service[k]), "hub": code, "area": area, "on_roster": True})
            k += 1
    for _ in range(n_other):
        code = rnd.choice(list(hubs))
        staff.append({"service": str(service[k]), "hub": code, "area": hubs[code][2], "on_roster": False})
        k += 1
    li = 0
    roles = [r for r, _ in P.ROLES]
    weights = [w for _, w in P.ROLES]
    for s in staff:
        s["sex"] = "F" if rnd.random() < P.WOMEN_SHARE else "M"
        s["role"] = rnd.choices(roles, weights)[0]
        s["contract"] = "Part time" if rnd.random() < 0.13 else "Full time"
        if rnd.random() < 0.84:
            s["joined"] = _date_between(rnd, dt.date(2004, 9, 1), dt.date(2025, 2, 28))
        else:
            s["joined"] = _date_between(rnd, dt.date(2025, 3, 3), dt.date(2026, 8, 31) if s["on_roster"]
                                        else dt.date(2026, 5, 31))
        if not s["on_roster"]:
            s["left"] = _date_between(rnd, max(s["joined"], P.PROGRAMME[0]) + D(days=30), dt.date(2026, 9, 20))
        s["legacy"] = None
        if s["area"] == "Vennerley" and s["joined"] < P.HR_MIGRATION:
            s["legacy"] = "VAS%05d" % legacy[li]
            li += 1
    return staff


def measurements(rnd, staff):
    """the programme's records; each roster driver's latest record is clear of every limit by the dead zone"""
    redraws = 0
    for s in staff:
        start = max(P.PROGRAMME[0], s["joined"])
        end = min(P.PROGRAMME[1], s.get("left", P.PROGRAMME[1]))
        while True:
            body = _body(rnd, s["sex"])
            d1 = _date_between(rnd, start, end)
            dates = [d1]
            if rnd.random() < 0.16 and (end - d1).days > 20:
                dates.append(_date_between(rnd, d1 + D(days=14), end))
            recs = []
            for d in dates:
                imperial = s["area"] == "Vennerley" and d < P.IMPERIAL_FORMS_UNTIL
                r = _record(rnd, body, imperial)
                r["date"] = d
                r["key"] = s["legacy"] if (s["legacy"] and d < P.HR_MIGRATION) else s["service"]
                recs.append(r)
            if not s["on_roster"] or _clear(recs[-1]):
                break
            redraws += 1
        s["body"] = body
        s["records"] = recs
    return redraws


# ----------------------------------------------------------------------------------------------- fleet
SEAT_JOBS = ["Driver seat slide sticking", "Driver seat recliner lever broken", "Driver seat suspension not holding",
             "Seat base bolts loose", "Driver seat cover torn", "Seat height adjuster failed", "Passenger seat belt buckle sticking",
             "Seat lumbar pump not working"]
CAB_JOBS = ["Bulkhead door catch broken", "Bulkhead window cracked", "Cab headlining loose", "Grab handle detached",
            "Cab trim panel rattling", "Bulkhead door seal perished", "Cab floor covering lifting"]
OTHER = [("B41", "Saloon cupboard door hinge"), ("E10", "Battery not charging"), ("E10", "Saloon lighting fault"),
         ("E22", "Light bar intermittent"), ("E22", "Siren amplifier fault"), ("M20", "Front brake pads worn"),
         ("M20", "Handbrake adjustment"), ("M30", "Steering pulling left"), ("M30", "Rear suspension knocking"),
         ("T10", "Tyre replacement"), ("T10", "Puncture repair"), ("S05", "Scheduled service"),
         ("S06", "Annual test preparation"), ("R01", "Stretcher mount worn"), ("R01", "Oxygen bracket loose"),
         ("R04", "Tail lift not lowering"), ("R04", "Ramp hydraulic leak")]
CODES = {"B12": "Seats", "B30": "Cab structure and trim", "B41": "Saloon body", "E10": "Electrical",
         "E22": "Emergency warning equipment", "M20": "Brakes", "M30": "Suspension and steering", "T10": "Tyres and wheels",
         "S05": "Scheduled service", "S06": "Annual test preparation", "R01": "Medical equipment mounts",
         "R04": "Tail lift and ramp"}
LEGACY_CODE = {"B12": "SEAT", "B30": "CABST", "B41": "BODY", "E10": "ELEC", "E22": "BLUE", "M20": "BRAKE", "M30": "SUSP",
               "T10": "TYRE", "S05": "SERV", "S06": "TEST", "R01": "EQPT", "R04": "LIFT"}


def fleet(rnd):
    fy0, fy1 = P.FY
    end = fy1 + D(days=1)
    vehicles = []
    hubs_n = [h[0] for h in P.HUBS if h[2] == "Strakemoor"]
    hubs_s = [h[0] for h in P.HUBS if h[2] == "Vennerley"]
    for conv, ch, n in P.FLEET:
        south_share = {"Corvane Coachworks": 1.0, "Pennick Coachbuild": 0.3, "Ostrel Vehicle Conversions": 0.45}[conv]
        for _ in range(n):
            south = rnd.random() < south_share
            vehicles.append({"converter": conv, "chassis": ch, "south": south,
                             "hub": rnd.choice(hubs_s if south else hubs_n),
                             "in_service": _date_between(rnd, dt.date(2018, 2, 1), dt.date(2024, 11, 30)), "disposed": None})
    # disposals: the oldest Corvane and Pennick FD35 vehicles, spread over the year
    old = sorted([v for v in vehicles if v["converter"] == "Corvane Coachworks" or
                  (v["converter"] == "Pennick Coachbuild" and v["chassis"] == "FD35")], key=lambda v: v["in_service"])
    pick = old[:P.DISPOSALS_IN_FY + 6]
    rnd.shuffle(pick)
    pick = pick[:P.DISPOSALS_IN_FY]
    for v in pick:
        v["disposed"] = _date_between(rnd, fy0 + D(days=20), fy1 - D(days=25))
    # new vehicles
    new = []
    for conv, ch, n in P.NEW_IN_FY:
        for _ in range(n):
            south = rnd.random() < 0.4
            ins = _date_between(rnd, fy0 + D(days=30), fy1 - D(days=40))
            if south and dt.date(2025, 6, 26) <= ins < P.WORKSHOP_CUTOVER:
                ins = P.WORKSHOP_CUTOVER + D(days=2)     # nothing entered service between the asset export and the cutover
            new.append({"converter": conv, "chassis": ch, "south": south, "hub": rnd.choice(hubs_s if south else hubs_n),
                        "in_service": ins, "disposed": None})
    # fleet numbers of six disposals go to new vehicles: the plan names the old vehicle's kind, the month it went
    # and the kind of vehicle that took its number
    plan = [(("Pennick Coachbuild", "FD35", False), dt.date(2026, 1, 9), ("Ostrel Vehicle Conversions", "FD35")),
            (("Pennick Coachbuild", "FD35", False), dt.date(2025, 10, 17), ("Ostrel Vehicle Conversions", "FD35")),
            (("Pennick Coachbuild", "FD35", False), dt.date(2026, 2, 4), ("Ostrel Vehicle Conversions", "FD35")),
            (("Pennick Coachbuild", "FD35", False), dt.date(2025, 11, 14), ("Pennick Coachbuild", "RD43")),
            (("Corvane Coachworks", "RD43", True), dt.date(2025, 12, 5), ("Ostrel Vehicle Conversions", "FD35")),
            (("Pennick Coachbuild", "FD35", False), dt.date(2026, 2, 23), ("Pennick Coachbuild", "RD43"))]
    taken_old, taken_new = set(), set()
    pairs = []
    for (conv, ch, south), month, (nconv, nch) in plan:
        cands = [v for v in vehicles if v["converter"] == conv and v["chassis"] == ch and v["south"] == south
                 and id(v) not in taken_old]
        cands.sort(key=lambda v: (v["disposed"] is None, v["in_service"]))
        o = cands[0]
        if o["disposed"] is None:
            # one of this year's disposals of another kind gives way, so the disposal count holds
            spare = [v for v in vehicles if v["disposed"] and id(v) not in taken_old and
                     not any(v is p[0] for p in pairs)]
            spare.sort(key=lambda v: v["in_service"], reverse=True)
            spare[0]["disposed"] = None
        o["disposed"] = month + D(days=rnd.randint(0, 20))
        taken_old.add(id(o))
        nv = [f for f in new if f["converter"] == nconv and f["chassis"] == nch and id(f) not in taken_new]
        f = nv[0]
        f["in_service"] = min(o["disposed"] + D(days=rnd.randint(8, 21)), fy1 - D(days=12))
        if f["south"] and dt.date(2025, 6, 26) <= f["in_service"] < P.WORKSHOP_CUTOVER:
            f["south"] = False
        taken_new.add(id(f))
        pairs.append((o, f))
    vehicles += new
    # numbering: Strakemoor vehicles and every vehicle entering service after the cutover carry HA numbers; Vennerley
    # vehicles carry legacy V numbers until the cutover and are renumbered then
    pool = _numbers(rnd, 400, 1000, 9899)
    legacy = _numbers(rnd, 200, 100, 899)
    pi = li = 0
    for v in vehicles:
        v["legacy_no"] = None
        if v["south"] and v["in_service"] < P.WORKSHOP_CUTOVER:
            v["legacy_no"] = "V%03d" % legacy[li]
            li += 1
        alive_at_cut = v["in_service"] < P.WORKSHOP_CUTOVER and (v["disposed"] is None or v["disposed"] >= P.WORKSHOP_CUTOVER)
        if (not v["south"]) or alive_at_cut or v["in_service"] >= P.WORKSHOP_CUTOVER:
            v["fleet_no"] = "HA%04d" % pool[pi]
            pi += 1
        else:
            v["fleet_no"] = None          # disposed under its legacy number before the cutover
    for o, f in pairs:
        assert o["fleet_no"] and f["in_service"] > o["disposed"], (o["fleet_no"], o["disposed"], f["in_service"])
        f["fleet_no"] = o["fleet_no"]
        f["reissue_of"] = o
        o["reissued_to"] = f
    assert len(pairs) == P.REISSUED_NUMBERS
    assert sum(1 for v in vehicles if v["disposed"]) == P.DISPOSALS_IN_FY
    for i, v in enumerate(vehicles):
        v["vid"] = i
        a = max(v["in_service"], fy0 - D(days=1))
        b = min(v["disposed"] or end, end)
        v["active"] = (a, b)
    return vehicles


def year(rnd, vehicles):
    """telematics units, daily mileage, workshop jobs and off-road spells over the financial year"""
    fy0, fy1 = P.FY
    end = fy1 + D(days=1)
    units = _numbers(rnd, 500, 0x100000, 0xFFFFFF)
    ui = 0
    jobs = []
    carried = {"Pennick Coachbuild": 0, "Ostrel Vehicle Conversions": 0}
    for v in vehicles:
        a, b = v["active"]
        # jobs and off-road spells first, mileage around them
        vor_days = set()
        day = a if a >= fy0 else fy0
        v_jobs = []
        while day < b:
            lam_seat = P.SEAT_CAB_RATE[v["converter"]] / 365.0
            lam_other = P.OTHER_JOB_RATE / 365.0
            for kind, lam in (("seatcab", lam_seat), ("other", lam_other)):
                if rnd.random() < lam:
                    v_jobs.append(_job(rnd, v, day, kind, b))
            day += D(days=1)
        # a vehicle whose number went on to a vehicle of another converter or chassis had its ordinary defects in
        # every quarter it ran, as any old vehicle does
        nxt = v.get("reissued_to")
        if nxt:
            for _, qa, qb in P.QUARTERS:
                lo, hi = max(qa, a, fy0), min(qb, b - D(days=1))
                if lo > hi:
                    continue
                if nxt["converter"] != v["converter"] and not any(j["code"] in ("B12", "B30") and lo <= j["raised"] <= hi
                                                                   for j in v_jobs):
                    v_jobs.append(_job(rnd, v, _date_between(rnd, lo, hi), "seatcab", b))
                if nxt["chassis"] != v["chassis"] and not any(j["vor"] and lo <= j["raised"] <= hi for j in v_jobs):
                    v_jobs.append(_job(rnd, v, _date_between(rnd, lo, max(lo, hi - D(days=3))), "other", b, force_vor=True))
        # seat jobs were open on some former Vennerley vehicles of each converter when the Vennerley workshop
        # system closed, as jobs are on any day
        if (v["legacy_no"] and v["in_service"] < P.WORKSHOP_CUTOVER and (v["disposed"] is None or v["disposed"] > P.WORKSHOP_CUTOVER)
                and v["converter"] in carried and carried[v["converter"]] < 2):
            d = P.WORKSHOP_CUTOVER - D(days=rnd.randint(3, 9))
            j = _job(rnd, v, d, "seatcab", b)
            if j["done"] < P.WORKSHOP_CUTOVER + D(days=2):
                j["done"] = P.WORKSHOP_CUTOVER + D(days=rnd.randint(2, 6))
                if j["vor"]:
                    j["vor_to"] = j["done"]
            v_jobs.append(j)
            carried[v["converter"]] += 1
        # visits: some off-road jobs bring further jobs raised while the vehicle is in the workshop
        extra = []
        for j in v_jobs:
            if j["vor"] and rnd.random() < 0.33:
                for _ in range(rnd.choice([1, 1, 2])):
                    d = j["raised"] + D(days=rnd.choice([0, 0, 1, 2]))
                    if d < j["vor_to"] and d < b:
                        e = _job(rnd, v, d, "seatcab" if rnd.random() < 0.18 else "other", b, force_vor=True)
                        extra.append(e)
        v_jobs += extra
        for j in v_jobs:
            if j["vor"]:
                d = j["vor_from"]
                while d < j["vor_to"]:
                    vor_days.add(d)
                    d += D(days=1)
        v["jobs"] = sorted(v_jobs, key=lambda j: (j["raised"], j["code"]))
        v["vor_days"] = vor_days
        # mileage
        miles = {}
        d = a
        odo = rnd.uniform(18000, 140000) if v["in_service"] < fy0 else rnd.uniform(40, 160)
        v["odo_start"] = odo
        while d < b:
            if d in vor_days or rnd.random() < 0.05:
                m = 0.0
            else:
                m = rnd.lognormvariate(math.log(P.DAILY_MILES[0]), P.DAILY_MILES[1])
            miles[d] = m
            d += D(days=1)
        v["miles"] = miles
        # telematics units: one from the start, possibly swapped once
        v["units"] = [{"unit": "%06X" % units[ui], "fitted": v["in_service"] if v["in_service"] >= fy0 - D(days=1)
                       else _date_between(rnd, v["in_service"], dt.date(2024, 12, 31)), "removed": None, "entered": None}]
        ui += 1
        jobs.extend((v, j) for j in v["jobs"])
    # unit swaps on vehicles in service for most of the year
    cands = [v for v in vehicles if (v["active"][1] - max(v["active"][0], fy0)).days > 120]
    rnd.shuffle(cands)
    for v in cands[:P.UNIT_SWAPS]:
        lo = max(v["active"][0], fy0) + D(days=30)
        hi = v["active"][1] - D(days=30)
        sw = _date_between(rnd, lo, hi)
        old = v["units"][0]
        old["removed"] = sw
        old["lingers"] = rnd.choice([1, 2, 2, 3, 4])     # left powered until the installer collected it
        v["units"].append({"unit": "%06X" % units[ui], "fitted": sw, "removed": None, "entered": None})
        ui += 1
    return jobs


def _job(rnd, v, day, kind, b, force_vor=False):
    if kind == "seatcab":
        if rnd.random() < 0.62:
            code, desc = "B12", rnd.choice(SEAT_JOBS)
        else:
            code, desc = "B30", rnd.choice(CAB_JOBS)
        p_vor = 0.42
    else:
        code, desc = rnd.choice(OTHER)
        p_vor = P.VOR_SHARE
    vor = force_vor or rnd.random() < p_vor
    j = {"code": code, "desc": desc, "raised": day, "vor": vor}
    if vor:
        j["vor_from"] = day
        j["vor_to"] = min(day + D(days=rnd.choice([1, 1, 1, 2, 2, 3, 4, 5, 7, 10])), b)
        if j["vor_to"] <= j["vor_from"]:
            j["vor_to"] = j["vor_from"] + D(days=1)
        j["done"] = j["vor_to"]
    else:
        j["done"] = day + D(days=rnd.choice([0, 0, 1, 1, 2, 3, 6]))
    return j


def build(seed=P.SEED, year_stream=P.YEAR_STREAM):
    rnd = random.Random(seed)
    staff = people(rnd)
    redraws = measurements(random.Random(seed + 1), staff)
    vehicles = fleet(random.Random(seed + 2))
    jobs = year(random.Random(seed + year_stream), vehicles)
    return {"staff": staff, "redraws": redraws, "vehicles": vehicles, "jobs": jobs}


# ----------------------------------------------------------------------------------------------- the truth
def truth_fit(W, which="latest"):
    """the drivers each cab fails under the standard, from the latest recorded measurement of every roster driver"""
    out = {}
    roster = [s for s in W["staff"] if s["on_roster"]]
    for cab in P.CABS:
        fail = [s for s in roster if not fits(assess(cab, *_rec_values(s, which)))]
        out[cab["id"]] = {"fail": len(fail), "women": sum(1 for s in fail if s["sex"] == "F")}
    return out


def _rec_values(s, which):
    r = s["records"][-1] if which == "latest" else s["records"][0]
    return r["stature"], r["weight"], r["seh"]


def truth_fleet(W):
    """the ask quantities from the clean truth (physical vehicles, true dates, true raise dates)"""
    fy0, fy1 = P.FY
    q = P.QUARTERS
    conv = {}
    chas = {}
    for v in W["vehicles"]:
        a, b = v["active"]
        a = max(a, fy0)
        days_in = max(0, (b - a).days)
        cv = conv.setdefault(v["converter"], {"jobs": [0, 0, 0, 0], "miles": 0.0})
        chv = chas.setdefault(v["chassis"], {"vor": [0, 0, 0, 0], "days": 0})
        chv["days"] += days_in
        for j in v["jobs"]:
            if j["code"] in ("B12", "B30") and fy0 <= j["raised"] <= fy1:
                cv["jobs"][[i for i, (_, s, e) in enumerate(q) if s <= j["raised"] <= e][0]] += 1
        for d in v["vor_days"]:
            if fy0 <= d <= fy1:
                chv["vor"][[i for i, (_, s, e) in enumerate(q) if s <= d <= e][0]] += 1
        cv["miles"] += sum(m for d, m in v["miles"].items() if fy0 <= d <= fy1)
    return conv, chas

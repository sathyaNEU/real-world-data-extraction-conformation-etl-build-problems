"""The world before any file is written: the fleet, its stations and routes, the rack postings, every vehicle's
operations day by day from September 2024 to August 2026, its fuel under the card regime and under the 2025 island
programmes, and Overton's 2025 deliveries. Nothing here is a file; records.py writes the layouts."""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

import numpy as np

import common as K

H = 3600.0


# ------------------------------------------------------------------------------------------------- stations
def _stations():
    S = []

    def add(net, code, name, city, st, lat, lon, ts):
        S.append(dict(code=code, net=net, name=name, city=city, st=st, lat=lat, lon=lon, truckstop=ts))

    # Riverbend Travel Plazas, the chain behind Delta's direct bill (West)
    for code, city, st, lat, lon, ts in [
        ("101", "Memphis", "TN", 35.0351, -89.9452, True), ("104", "Memphis", "TN", 35.0617, -89.9188, False),
        ("106", "Memphis", "TN", 35.1180, -89.8725, False), ("112", "Jackson", "TN", 35.6421, -88.8410, True),
        ("115", "Jackson", "TN", 35.6119, -88.8902, False), ("121", "Brownsville", "TN", 35.5807, -89.2456, True),
        ("124", "Lexington", "TN", 35.6701, -88.4150, True), ("127", "Dickson", "TN", 36.0582, -87.3722, True),
        ("131", "Olive Branch", "MS", 34.9512, -89.8248, True), ("134", "Tupelo", "MS", 34.2731, -88.7013, True),
        ("137", "Grenada", "MS", 33.7802, -89.8306, True), ("141", "West Memphis", "AR", 35.1495, -90.1612, True),
        ("144", "Forrest City", "AR", 35.0102, -90.7764, True), ("148", "Paducah", "KY", 37.0609, -88.6020, True),
        ("151", "Corinth", "MS", 34.9419, -88.5202, True), ("155", "Union City", "TN", 36.4276, -89.0518, True),
    ]:
        add("West", code, "Riverbend Travel Plaza #%s" % code, city, st, lat, lon, ts)
    # Crossroads Fleet Card merchants (Central)
    for code, name, city, st, lat, lon, ts in [
        ("CR40211", "Couchville Fuel Center", "Nashville", "TN", 36.1050, -86.7006, True),
        ("CR40218", "Murfreesboro Pike Fuel Stop", "Nashville", "TN", 36.1188, -86.7237, False),
        ("CR40236", "Donelson Fuel Mart", "Nashville", "TN", 36.1593, -86.6812, False),
        ("CR40252", "La Vergne Travel Center", "La Vergne", "TN", 36.0201, -86.5638, True),
        ("CR41107", "Cookeville Interstate Fuel", "Cookeville", "TN", 36.1412, -85.4750, True),
        ("CR41115", "Willow Ave Market", "Cookeville", "TN", 36.1525, -85.5055, False),
        ("CR41142", "Sparta Quick Stop", "Sparta", "TN", 35.9306, -85.4721, False),
        ("CR41160", "Crossville Highway 70 Fuel", "Crossville", "TN", 35.9561, -85.0417, False),
        ("CR42003", "Manchester I-24 Truck Stop", "Manchester", "TN", 35.4691, -86.0612, True),
        ("CR42019", "Bowling Green Travel Plaza", "Bowling Green", "KY", 36.9512, -86.4410, True),
        ("CR42033", "Cave City Fuel Stop", "Cave City", "KY", 37.1302, -85.9622, True),
        ("CR42047", "Elizabethtown Truck Plaza", "Elizabethtown", "KY", 37.6950, -85.8702, True),
        ("CR42061", "Huntsville Parkway Fuel", "Huntsville", "AL", 34.7412, -86.6012, True),
        ("CR42075", "Cullman Travel Center", "Cullman", "AL", 34.1749, -86.8436, True),
        ("CR42089", "Chattanooga Lee Hwy Fuel", "Chattanooga", "TN", 35.0612, -85.1530, True),
        ("CR42103", "Dalton Truck Stop", "Dalton", "GA", 34.7698, -84.9702, True),
        ("CR42117", "Columbia Hwy 31 Fuel", "Columbia", "TN", 35.6151, -87.0353, True),
        ("CR42131", "Clarksville Exit 4 Fuel", "Clarksville", "TN", 36.5784, -87.3519, True),
        ("CR42145", "Hopkinsville Travel Center", "Hopkinsville", "KY", 36.8656, -87.4886, True),
        ("CR42159", "Monteagle Fuel Plaza", "Monteagle", "TN", 35.2390, -85.8399, True),
        ("CR42173", "Athens I-75 Truck Stop", "Athens", "TN", 35.4426, -84.5930, True),
    ]:
        add("Central", code, name, city, st, lat, lon, ts)
    # Smoky Mountain Petroleum Marketers group merchants (East)
    for code, name, city, st, lat, lon, ts in [
        ("0417", "Middlebrook Pike Fuel", "Knoxville", "TN", 35.9734, -83.9010, True),
        ("0422", "Ebenezer Road Market", "Knoxville", "TN", 35.9105, -84.0815, False),
        ("0431", "Strawberry Plains Truck Stop", "Knoxville", "TN", 36.0365, -83.7120, True),
        ("0516", "Blountville Hwy 75 Fuel", "Blountville", "TN", 36.4720, -82.4082, True),
        ("0521", "Tri-City Airport Market", "Blountville", "TN", 36.4785, -82.3990, False),
        ("0533", "Bristol I-81 Travel Center", "Bristol", "VA", 36.6201, -82.1612, True),
        ("0602", "Wytheville Truck Plaza", "Wytheville", "VA", 36.9483, -81.0848, True),
        ("0614", "Roanoke Valley Fuel Center", "Salem", "VA", 37.2768, -80.0312, True),
        ("0627", "Harrisonburg Travel Stop", "Harrisonburg", "VA", 38.4496, -78.8689, True),
        ("0641", "Asheville I-26 Fuel", "Asheville", "NC", 35.5101, -82.5398, True),
        ("0655", "Hickory Truck Stop", "Hickory", "NC", 35.7333, -81.3412, True),
        ("0668", "Beckley Turnpike Fuel", "Beckley", "WV", 37.7782, -81.1889, True),
        ("0679", "Charleston Kanawha Fuel", "Charleston", "WV", 38.3498, -81.6326, True),
        ("0688", "London KY Travel Center", "London", "KY", 37.1290, -84.0833, True),
        ("0693", "Lexington KY Truck Plaza", "Lexington", "KY", 38.0406, -84.5037, True),
        ("0705", "Jellico Fuel Stop", "Jellico", "TN", 36.5871, -84.1272, True),
        ("0712", "Morristown I-81 Fuel", "Morristown", "TN", 36.2140, -83.2949, True),
        ("0724", "Kingsport Stone Drive Fuel", "Kingsport", "TN", 36.5484, -82.5618, False),
        ("0737", "Johnson City Market", "Johnson City", "TN", 36.3134, -82.3535, False),
        ("0748", "Sevierville Fuel Plaza", "Sevierville", "TN", 35.8681, -83.5618, True),
    ]:
        add("East", code, name, city, st, lat, lon, ts)
    return S


STATIONS = _stations()
ST = {s["code"]: s for s in STATIONS}
TERMINAL_OF_STATE = {"TN": None, "MS": "Memphis", "AR": "Memphis", "KY": "Nashville", "AL": "Nashville",
                     "GA": "Knoxville", "VA": "Knoxville", "NC": "Knoxville", "WV": "Knoxville"}


def station_terminal(code):
    s = ST[code]
    t = TERMINAL_OF_STATE[s["st"]]
    if t:
        return t
    lon = s["lon"]
    return "Memphis" if lon < -88.0 else ("Nashville" if lon < -84.9 else "Knoxville")


HOME = {"MEM": ["101", "104", "106"], "JXN": ["112", "115"], "NSH": ["CR40211", "CR40218", "CR40236"],
        "CKV": ["CR41107", "CR41115"], "SPARTA": ["CR41142"], "CROSSVILLE": ["CR41160"],
        "KNX": ["0417", "0422", "0431"], "TRI": ["0516", "0521", "0724", "0737"]}
ROUTE = {"MEM": ["131", "141", "101"], "JXN": ["121", "124", "151", "155"], "NSH": ["CR40252", "CR42117", "CR42131"],
         "CKV": ["CR41107", "CR42159"], "KNX": ["0748", "0712", "0431"], "TRI": ["0533", "0712", "0724"],
         "SPARTA": ["CR41142", "CR41107"], "CROSSVILLE": ["CR41160", "CR41107"]}
LOOP_ROUTES = {
    "JXN": [["134", "137", "151"], ["148", "155", "124"], ["144", "141", "121"]],
    "NSH": [["CR42019", "CR42047", "CR42061", "CR42075"], ["CR42089", "CR42103", "CR42145", "CR42131"],
            ["CR42033", "CR42019", "CR42173", "CR42089"], ["CR42061", "CR42075", "CR42019", "CR42047"]],
    "KNX": [["0688", "0693", "0705", "0688"], ["0641", "0655", "0641", "0748"], ["0712", "0533", "0602", "0712"]],
    "TRI": [["0602", "0614", "0627", "0602"], ["0668", "0679", "0668", "0602"], ["0641", "0655", "0641", "0533"],
            ["0693", "0688", "0705", "0712"]],
}
SHORT_ROUTES = {"KNX": ["0688", "0641", "0712", "0705"]}
CUSTOMERS = {
    "MEM": [("CUST Wolfchase Regional Hosp dock", 35.1032, -89.8689), ("CUST Getwell Schools supply ctr", 35.0821, -89.9744)],
    "JXN": [("CUST Highland Park Hospital dock", 35.6502, -88.8309)],
    "NSH": [("CUST Harding Pike Medical dock", 36.1420, -86.8001), ("CUST Cumberland City Schools whse", 36.1745, -86.7533),
            ("CUST Riverfront Convention Hotel", 36.2108, -86.6929)],
    "CKV": [("CUST Upper Cumberland College dock", 36.1751, -85.5072)],
    "KNX": [("CUST Lakeshore General Hospital dock", 35.9440, -83.9409), ("CUST East Ridge Schools whse", 35.9989, -83.9556)],
    "TRI": [("CUST Boone Lake Medical dock", 36.3082, -82.3807)],
}


# ------------------------------------------------------------------------------------------------- racks
def racks():
    """Daily postings by effective date for the three terminals: Overton's own posting and the rack service's contract
    average. A posting for effective date D is made at 6 pm on the day before."""
    out = {}
    d0 = dt.date(2024, 8, 25)
    dd = K.days(d0, K.HIST_END + dt.timedelta(days=3))
    g = K.rng("rack", "base")
    x = 2.312
    base = []
    for d in dd:
        drift = 0.0
        if dt.date(2025, 2, 10) <= d <= dt.date(2025, 4, 20):
            drift = 0.0016
        elif dt.date(2025, 6, 1) <= d <= dt.date(2025, 7, 25):
            drift = -0.0009
        elif dt.date(2026, 5, 1) <= d <= dt.date(2026, 6, 20):
            drift = 0.0011
        elif dt.date(2026, 7, 1) <= d <= dt.date(2026, 7, 31):
            drift = -0.0007
        elif dt.date(2026, 8, 1) <= d <= dt.date(2026, 8, 21):
            drift = -0.0286
        x = max(1.85, x + drift + g.normal(0.0, 0.0105))
        base.append(x)
    diff = {"Memphis": -0.0185, "Nashville": 0.0, "Knoxville": 0.0242}
    for t in ("Memphis", "Nashville", "Knoxville"):
        gt = K.rng("rack", t)
        for i, d in enumerate(dd):
            ov = base[i] + diff[t] + gt.normal(0.0, 0.0031)
            av = ov + 0.0038 + gt.normal(0.0, 0.0024)
            out[(t, d)] = (round(ov, 4), round(av, 4))
    return out


def posting_in_effect(R, terminal, t):
    """The posting in effect at a moment: Overton posts every terminal at 6 pm Central, effective the next day."""
    tc = t.astimezone(K.CENTRAL)
    d = tc.date()
    if tc.hour >= 18:
        d = d + dt.timedelta(days=1)
    return R[(terminal, d)]


# ------------------------------------------------------------------------------------------------- units
@dataclass
class Unit:
    unit: int
    yard: str
    model: str
    body: str
    cap: float
    reserve: float
    duty: str
    base: float
    mpg: float
    dom: str
    tz: object
    habit: dict
    status: str = "Active"
    sold: object = None
    card: str = ""
    driver: str = ""
    year: int = 2021
    vin8: str = ""
    in_service: dt.date = dt.date(2021, 3, 1)
    legs: list = field(default_factory=list)       # [t0, place0, t1, place1, fuel, miles, odo0]
    fills: list = field(default_factory=list)      # dict(t, kind, station, gal, odo)
    visits: list = field(default_factory=list)     # (t_enter, t_exit, place)
    cust: list = field(default_factory=list)       # (t_enter, t_exit, name)
    odo0: float = 0.0


MPG = {"van": 8.6, "box": 7.6, "daycab": 6.4, "sleeper": 6.3}
MOUNTAIN = ("KNX", "TRI")                # the East's sleepers work the Appalachian routes: loaded grades, about 5 mpg


def make_units():
    units = []
    for y in K.YARDS:
        seq = 0
        for (n, model, duty, base) in K.FLEET[y]:
            for k in range(n):
                seq += 1
                units.append(_unit(y, seq, model, duty, base, k))
        for (n, model) in K.SPARES.get(y, []):
            for k in range(n):
                seq += 1
                u = _unit(y, seq, model, "spare", 0.0, k)
                u.status = "Spare"
                units.append(u)
        for (n, model, duty, base, sold) in K.SOLD.get(y, []):
            for k in range(n):
                seq += 1
                u = _unit(y, seq, model, duty, base, k)
                u.status, u.sold = "Sold", sold
                u.year = min(u.year, 2018)
                u.in_service = dt.date(u.year, u.in_service.month, u.in_service.day)
                units.append(u)
    for u in units:
        # a unit on the road from the start of the telematics history was in service before it; the paperwork is
        # dated a working day
        d = u.in_service
        if u.status == "Active" and d > dt.date(2024, 8, 23):
            d = dt.date(2024, 1 + d.month % 8, d.day)
        while not K.working(d):
            d += dt.timedelta(days=1)
        u.in_service = d
    return units


def _unit(y, seq, model, duty, base, k):
    g = K.rng("unit", y, seq)
    name, body, cap, res = K.MODELS[model]
    unit = K.YARD[y]["branch"] * 100 + seq
    dom = "YARD"
    if duty == "sat":
        dom = "SPARTA" if k % 2 == 0 else "CROSSVILLE"
    habit = dict(
        dep=float(g.uniform(5.2, 6.7)), ret=float(g.uniform(14.6, 17.4)),
        theta=float(g.uniform(0.26, 0.40)), pref="morning" if g.random() < 0.42 else "evening",
        p_late=float(g.uniform(0.35, 0.95)), late_theta=float(g.uniform(0.50, 0.64)),
        def_every=int(g.integers(3, 6)), cust_p=float(g.uniform(0.10, 0.45)),
        reserve_mult=float(g.uniform(0.84, 1.16)), topup_floor=float(g.uniform(2.0, 4.5)),
    )
    habit["daily_top"] = False
    if duty == "dayrun":
        habit["dep"] = float(g.uniform(3.7, 4.5))
        habit["ret"] = float(g.uniform(16.9, 18.1))
        if k in (2, 6):                      # the Jackson to Paducah and Union City runs, out later and back after 7.30 pm
            habit["dep"] = float(g.uniform(5.3, 5.8))
            habit["ret"] = float(g.uniform(19.55, 20.05))
            habit["daily_top"] = True
            habit["pref"] = "evening"
    # sleeper drivers: most end their driving day early in the evening, some drive late and fuel on arrival
    late = body == "sleeper" and g.random() < 0.42
    habit["nightly"] = body == "sleeper" and y == "NSH"   # Keeble's own drivers top off at the night's stop
    habit["night_end"] = float(g.uniform(21.7, 23.0)) if late else float(g.uniform(18.6, 19.6))
    habit["start"] = 8.4 if late else 5.6
    if late:
        habit["p_late"] = float(g.uniform(0.82, 0.96))
    hs = HOME[dom if dom != "YARD" else y]
    habit["home"] = hs[int(g.integers(0, len(hs)))]
    reserve = round(res * habit["reserve_mult"], 1)
    year = int(g.integers(2018, 2025))
    u = Unit(unit=unit, yard=y, model=model, body=body, cap=cap, reserve=reserve, duty=duty,
             base=base * float(g.uniform(0.93, 1.07)) if base else 0.0,
             mpg=(5.0 if (body == "sleeper" and y in MOUNTAIN) else MPG[body]) * float(g.uniform(0.94, 1.06)),
             dom=dom, tz=K.YARD[y]["tz"], habit=habit, year=year, vin8=K.token("vin", unit, n=8).upper(),
             in_service=dt.date(year, int(g.integers(1, 13)), int(g.integers(1, 28))))
    u.card = "%05d" % int(g.integers(10000, 99999))
    u.driver = "%04d" % int(g.integers(1000, 9999))
    u.odo0 = float(g.uniform(40000, 260000)) if body != "sleeper" else float(g.uniform(180000, 620000))
    return u


# ------------------------------------------------------------------------------------------------- the week plan
def place_ll(place):
    kind, key = place
    if kind == "YARD":
        return K.YARD[key]["lat"], K.YARD[key]["lon"]
    if kind == "LOT":
        return K.LOTS[key]["lat"], K.LOTS[key]["lon"]
    s = ST[key]
    return s["lat"], s["lon"]


def week_plan(u, monday, g):
    """Legs for one unit for one week: (t0, place0, t1, place1, share of a driving day's fuel)."""
    wd = [monday + dt.timedelta(days=i) for i in range(7)]
    work = [K.working(d) for d in wd]
    tz = u.tz
    Y = ("YARD", u.yard)
    legs = []

    def T(d, h):
        return K.local_dt(d, h, tz)

    def jit(s):
        return float(g.normal(0.0, s))

    if u.duty == "spare":
        return legs
    if u.duty in ("metro", "dayrun", "sat"):
        home = Y if u.dom == "YARD" else ("LOT", u.dom)
        visit_day = next((i for i in range(5) if work[i]), None)
        for i, d in enumerate(wd[:5]):
            if not work[i]:
                continue
            dep = u.habit["dep"] + jit(0.18)
            ret = u.habit["ret"] + jit(0.35)
            if u.habit["daily_top"] and d.weekday() == 4:     # the long runs are shorter on Fridays
                ret = 17.4 + jit(0.3)
            if u.duty == "sat":
                dep = 6.05 + jit(0.15)
                ret = 16.2 + jit(0.35)
                if i == visit_day:     # the weekly yard visit for inspection and supplies
                    arr_y = dep + 0.62 + jit(0.08)
                    lv_y = arr_y + 0.95 + abs(jit(0.25))
                    legs.append((T(d, dep), home, T(d, arr_y), Y, 0.11))
                    legs.append((T(d, lv_y), Y, T(d, ret), home, 0.95))
                    continue
            if u.duty == "dayrun" and d.weekday() in (1, 3):  # Tuesday and Thursday: a midday reload
                arr_m = 11.35 + jit(0.25)
                lv_m = arr_m + 0.85 + abs(jit(0.2))
                share = (arr_m - dep) / ((arr_m - dep) + (ret - lv_m))
                legs.append((T(d, dep), Y, T(d, arr_m), Y, share))
                legs.append((T(d, lv_m), Y, T(d, ret), Y, 1.0 - share))
                continue
            legs.append((T(d, dep), home, T(d, ret), home, 1.0))
        return legs
    runs, cur = [], []
    for i in range(5):
        if work[i]:
            cur.append(i)
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    routes = LOOP_ROUTES[u.yard]
    route = routes[int(g.integers(0, len(routes)))]

    def loop(ds, stops, midday_after=None):
        n = len(ds)
        if n == 1:
            d = wd[ds[0]]
            legs.append((T(d, 5.4 + jit(0.3)), Y, T(d, 15.8 + jit(0.6)), Y, 0.86))
            return
        prev = Y
        for j, di in enumerate(ds):
            d = wd[di]
            h0 = (u.habit["start"] - 0.5 + jit(0.25)) if j == 0 else (u.habit["start"] + jit(0.35))
            t0 = T(d, h0)
            if j == n - 1:
                legs.append((t0, prev, T(d, 15.2 + jit(0.6)), Y, 0.92))
                prev = Y
                continue
            stop = ("STOP", stops[j % len(stops)])
            if midday_after is not None and j == midday_after:
                arr_m = 11.05 + jit(0.25)
                lv_m = arr_m + 1.2 + abs(jit(0.2))
                end = min(23.6, u.habit["night_end"] + jit(0.3))
                share = (arr_m - h0) / ((arr_m - h0) + (end - lv_m))
                legs.append((t0, prev, T(d, arr_m), Y, share))
                legs.append((T(d, lv_m), Y, T(d, end), stop, 1.0 - share))
                prev = stop
                continue
            legs.append((t0, prev, T(d, min(23.6, u.habit["night_end"] + jit(0.3))), stop, 1.0))
            prev = stop

    if u.duty == "loop4":
        for r in runs:
            loop(r, route)
    elif u.duty == "loop3":
        for r in runs:
            if r[:4] == [0, 1, 2, 3]:
                loop([0, 1, 2, 3], route)
            else:
                loop(r[:4], route)
    elif u.duty == "loop1x2":
        sr = SHORT_ROUTES[u.yard]
        done = set()
        for p in ([0, 1], [2, 3]):
            if all(work[i] for i in p):
                loop(p, [sr[int(g.integers(0, len(sr)))]])
                done.update(p)
        for i in range(5):
            if work[i] and i not in done:
                loop([i], [])
    elif u.duty == "dbl2":
        for r in runs:                       # the midweek reload at the yard on the third day of the week's run
            loop(r, route, midday_after=2 if len(r) >= 4 else None)
    return legs


# ------------------------------------------------------------------------------------------------- the simulation
# the days each 2025 island dispensed: the programme's delivery dates, then on until the last load was drawn down
ISLAND = {y: (a, b + dt.timedelta(days=21)) for y, (a, b) in K.PROG.items()}


def in_program(u, t_local):
    p = ISLAND.get(u.yard)
    return bool(p) and p[0] <= t_local.date() <= p[1]


class Bag:
    pass


def mondays(a, b):
    d = a - dt.timedelta(days=a.weekday())
    out = []
    while d <= b:
        out.append(d)
        d += dt.timedelta(days=7)
    return out


def simulate():
    W = Bag()
    W.R = racks()
    W.units = make_units()
    for u in W.units:
        run_unit(u)
    W.deliveries = deliveries(W)
    # each island kept dispensing after the last delivery until the tank was down to its bottom: run the yard's
    # vehicles again with the island's last day set to that day (nothing before it changes)
    for y in K.PROG:
        ISLAND[y] = (ISLAND[y][0], W.run_out[y])
        for u in W.units:
            if u.yard == y:
                run_unit(u)
    first = [(e["bol"]["bol"], e["ticket"], e["gross"]) for e in W.deliveries]
    W.deliveries = deliveries(W)
    assert first == [(e["bol"]["bol"], e["ticket"], e["gross"]) for e in W.deliveries]
    return W


def run_unit(u):
    g = K.rng("ops", u.unit)
    gf = K.rng("fuel", u.unit)
    raw = []
    for m in mondays(K.HIST_START, K.HIST_END):
        for leg in week_plan(u, m, g):
            if leg[0].date() >= K.HIST_START and leg[2].date() <= K.HIST_END and (u.sold is None or
                                                                                 leg[2].date() < u.sold):
                raw.append(leg)
    raw.sort(key=lambda x: x[0])
    legs = []
    odo = u.odo0
    for (t0, p0, t1, p1, share) in raw:
        f = u.base * K.SEASON[t0.month] * float(np.exp(gf.normal(0.0, 0.085))) * share
        f = round(f, 3)
        mi = round(f * u.mpg * float(np.exp(gf.normal(0.0, 0.03))), 1)
        legs.append([t0, p0, t1, p1, f, mi, odo])
        odo += mi
    u.legs = legs
    fuel_and_fills(u, K.rng("fills", u.unit))
    visits_of(u)
    customers_of(u)


def rem_to_yard(u, i):
    """Fuel from leg i (inclusive) to the next arrival at the unit's yard."""
    need = 0.0
    for j in range(i, len(u.legs)):
        need += u.legs[j][4]
        if u.legs[j][3] == ("YARD", u.yard):
            break
    return need


def fuel_and_fills(u, g):
    """Burn each leg's fuel in order. Card regime: drivers fill at a station when the gauge runs low (day vehicles at
    a station near home, morning or evening by habit; sleepers on the road, often at the night's stop). During a 2025
    island programme at the unit's own yard: an island fill on every yard arrival, and on the road only what gets the
    unit back to the yard on its reserve."""
    L = u.cap * 0.62
    fills = []
    legs = u.legs
    th = u.habit["theta"]
    nfuel = 0
    for i, (t0, p0, t1, p1, f, mi, odo0) in enumerate(legs):
        prog = in_program(u, t0)
        day_veh = u.duty in ("metro", "dayrun", "sat")
        # ---- at departure (card regime)
        if not prog:
            if day_veh and u.habit["pref"] == "morning" and p0[0] in ("YARD", "LOT") and L < (th + 0.12) * u.cap:
                tf = t0 + dt.timedelta(seconds=float(g.uniform(0.08, 0.26)) * H)
                fills.append(dict(t=tf, kind="card", station=u.habit["home"], gal=round(u.cap - L, 3), odo=odo0 + 1.5))
                L = u.cap
            if u.body == "sleeper" and p0 == ("YARD", u.yard) and p1[0] == "STOP" and L < 0.52 * u.cap:
                tf = t0 + dt.timedelta(seconds=float(g.uniform(0.2, 0.45)) * H)
                fills.append(dict(t=tf, kind="card", station=u.habit["home"], gal=round(u.cap - L, 3), odo=odo0 + 4.0))
                L = u.cap
        # ---- along the leg
        if prog:
            rem = rem_to_yard(u, i)
            # buy on the road only when the rest of the run cannot be made on the reserve, when the tank is low
            if L - rem < u.reserve - 0.5 and L - f < 0.30 * u.cap:
                frac = float(g.uniform(0.45, 0.85))
                lmid = L - f * frac
                buy = rem - f * frac - (lmid - u.reserve) + float(g.normal(0.0, 1.4))
                buy = max(0.0, min(buy, u.cap - lmid))
                if buy > 3.0:
                    tf = t0 + (t1 - t0) * frac
                    st = road_station(u, p0, p1, g)
                    fills.append(dict(t=tf, kind="card", station=st, gal=round(buy, 3), odo=odo0 + mi * frac))
                    L += buy
            L = max(L - f, 0.6)
        else:
            if L - f < 0.13 * u.cap:
                frac = max(0.15, min(0.85, (L - 0.16 * u.cap) / max(f, 1e-6)))
                lmid = L - f * frac
                tf = t0 + (t1 - t0) * frac
                st = road_station(u, p0, p1, g)
                fills.append(dict(t=tf, kind="card", station=st, gal=round(u.cap - lmid, 3), odo=odo0 + mi * frac))
                L = u.cap - f * (1.0 - frac)
            else:
                L -= f
                if u.body == "sleeper" and p1[0] == "STOP" and \
                        L < (0.9 if u.habit["nightly"] else u.habit["late_theta"]) * u.cap and \
                        g.random() < u.habit["p_late"]:
                    tf = t1 + dt.timedelta(seconds=float(g.uniform(0.05, 0.35)) * H)
                    fills.append(dict(t=tf, kind="card", station=p1[1], gal=round(u.cap - L, 3), odo=odo0 + mi))
                    L = u.cap
        # ---- at arrival
        prog1 = in_program(u, t1)
        if p1 == ("YARD", u.yard) and prog1:
            if u.cap - L >= u.habit["topup_floor"]:
                tf = t1 + dt.timedelta(seconds=float(g.uniform(0.05, 0.32)) * H)
                fills.append(dict(t=tf, kind="island", station=u.yard, gal=round(u.cap - L, 1), odo=odo0 + mi))
                L = u.cap
        elif not prog1:
            last_of_day = (i == len(legs) - 1) or legs[i + 1][0].date() != t1.date()
            if day_veh and u.habit["pref"] == "evening" and p1[0] in ("YARD", "LOT") and last_of_day and \
                    (L < (th + 0.05) * u.cap or (u.habit["daily_top"] and L < 0.9 * u.cap)):
                tf = t1 - dt.timedelta(seconds=float(g.uniform(0.08, 0.3)) * H)
                fills.append(dict(t=tf, kind="card", station=u.habit["home"], gal=round(u.cap - L, 3), odo=odo0 + mi - 1.2))
                L = u.cap
            if u.body == "sleeper" and p1 == ("YARD", u.yard) and L < 0.30 * u.cap:
                tf = t1 - dt.timedelta(seconds=float(g.uniform(0.15, 0.4)) * H)
                fills.append(dict(t=tf, kind="card", station=u.habit["home"], gal=round(u.cap - L, 3), odo=odo0 + mi - 3.0))
                L = u.cap
        # DEF on the cards every few fuel fills, at the same stop
        n_now = sum(1 for x in fills if x["kind"] == "card")
        if n_now > nfuel:
            if n_now % u.habit["def_every"] == 0:
                last = [x for x in fills if x["kind"] == "card"][-1]
                if u.body in ("van", "box"):
                    dgal = 2.5 * int(g.integers(1, 3))
                else:
                    dgal = round({"daycab": 11.0, "sleeper": 14.0}[u.body] * float(g.uniform(0.7, 1.3)), 3)
                fills.append(dict(t=last["t"] + dt.timedelta(minutes=int(g.integers(1, 6))), kind="def",
                                  station=last["station"], gal=dgal, odo=last["odo"]))
            nfuel = n_now
    fills.sort(key=lambda x: x["t"])
    u.fills = fills


def road_station(u, p0, p1, g):
    if p1[0] == "STOP":
        return p1[1]
    if p0[0] == "STOP":
        return p0[1]
    rs = ROUTE[u.dom if u.dom != "YARD" else u.yard]
    return rs[int(g.integers(0, len(rs)))]


def visits_of(u):
    """Yard and lot stays from the legs: entered on arrival, left on the next departure."""
    V = []
    legs = u.legs
    for i, leg in enumerate(legs):
        if leg[3][0] in ("YARD", "LOT"):
            nxt = legs[i + 1][0] if i + 1 < len(legs) else None
            V.append((leg[2], nxt, leg[3]))
    u.visits = V


def customers_of(u):
    g = K.rng("cust", u.unit)
    C = []
    custs = CUSTOMERS.get(u.yard, [])
    if custs and u.duty in ("metro", "dayrun"):
        for leg in u.legs:
            if leg[0].date() < K.GEO_START - dt.timedelta(days=3):
                continue
            if g.random() < u.habit["cust_p"]:
                name = custs[int(g.integers(0, len(custs)))][0]
                te = leg[0] + (leg[2] - leg[0]) * float(g.uniform(0.2, 0.7))
                tx = te + dt.timedelta(minutes=int(g.integers(14, 52)))
                if tx < leg[2]:
                    C.append((te, tx, name))
    u.cust = C


# ------------------------------------------------------------------------------------------------- Overton 2025
# the dispatcher's 5 pm reorder point (a load is lifted that evening for the next working morning when the tank has
# about a load's room left by then) and the daily draw it plans the programme's run-down on
REORDER = {"JXN": 11800.0, "KNX": 11000.0}
PLAN_DRAW = {"JXN": 1080.0, "KNX": 840.0}


def _last_working(d):
    nxt = d + dt.timedelta(days=1)
    while not K.working(nxt):
        nxt += dt.timedelta(days=1)
    return nxt.month != d.month


def deliveries(W):
    """Overton's 2025 programme drops. Each working day at 3 pm the dispatcher reads the tank; when it is at or below
    the reorder point and the programme's remaining draw will use a further load, a load is lifted at the terminal that
    evening for the next working morning. A drop stops at the overfill limit and the balance comes back the next working
    morning under the same terminal bill; a load due on a month's last working day is sent only if it will go in whole."""
    out = []
    for y, (a, b) in K.PROG.items():
        g = K.rng("deliv", y)
        tz = K.YARD[y]["tz"]
        term = K.YARD[y]["terminal"]
        draws = sorted((f["t"], f["gal"]) for u in W.units if u.yard == y for f in u.fills if f["kind"] == "island")
        st = dict(level=K.TANK_HEEL, di=0)

        def drain_to(t):
            while st["di"] < len(draws) and draws[st["di"]][0] <= t:
                st["level"] -= draws[st["di"]][1]
                st["di"] += 1

        bol_no = int(g.integers(4100, 4800))
        ticket = int(g.integers(51200, 53900))
        wdays = [d for d in K.days(a, b) if K.working(d)]
        lift_for = {wdays[0]: K.local_dt(wdays[0] - dt.timedelta(days=1), 19.6, tz)}
        pending = None
        for k, d in enumerate(wdays):
            t_drop = K.local_dt(d, 6.25 + float(g.uniform(0.0, 1.7)), tz)
            drain_to(t_drop)
            if pending is not None:
                bol, left = pending
                if K.TANK_FILL_LIMIT - st["level"] >= left:
                    ticket += int(g.integers(1, 4))
                    out.append(dict(bol=bol, ticket=ticket, t_drop=t_drop, gross=round(left, 1), split=True))
                    st["level"] += left
                    pending = None
            elif d in lift_for:
                t_lift = lift_for.pop(d)
                bol_no += int(g.integers(1, 9))
                temp = float(g.uniform(61.0, 69.0)) if d.month <= 5 else float(g.uniform(71.0, 83.0))
                net = float(int(g.integers(7956, 8046)))          # the terminal meters each load to its compartments
                gross = round(net * (1 + 0.00046 * (temp - 60.0)), 1)
                bol = dict(yard=y, bol="%s%06d" % ({"Memphis": "M", "Nashville": "N", "Knoxville": "K"}[term], bol_no),
                           t_lift=t_lift, net=net, gross=gross, temp=round(temp, 1), terminal=term)
                drop = min(gross, K.TANK_FILL_LIMIT - st["level"])
                ticket += int(g.integers(1, 4))
                out.append(dict(bol=bol, ticket=ticket, t_drop=t_drop, gross=round(drop, 1), split=False))
                st["level"] += drop
                if gross - drop > 0.05:
                    pending = (bol, round(gross - drop, 1))
            t_read = K.local_dt(d, 15.0, tz)
            drain_to(t_read)
            nxt = wdays[k + 1] if k + 1 < len(wdays) else None
            if nxt is None or pending is not None or lift_for:
                continue
            # the stock lasts the programme out at the draw so far: no further load
            rate = (st["di"] and sum(x[1] for x in draws[:st["di"]]) / max(1, k + 1)) or PLAN_DRAW[y]
            need = sum(1 for x in wdays if x >= nxt) * rate - (st["level"] - K.TANK_HEEL)
            point = 9900.0 if _last_working(nxt) else REORDER[y]
            if st["level"] <= point and need > 0.0:
                lift_for[nxt] = K.local_dt(nxt - dt.timedelta(days=1), 15.7 + float(g.uniform(0.0, 6.6)), tz)
        # after the last delivery the island runs the tank down to its bottom: the last fill it could make
        last = None
        while st["di"] < len(draws) and st["level"] - draws[st["di"]][1] >= K.TANK_HEEL:
            st["level"] -= draws[st["di"]][1]
            last = draws[st["di"]][0]
            st["di"] += 1
        W.run_out = getattr(W, "run_out", {})
        W.tank_end = getattr(W, "tank_end", {})
        W.run_out[y] = (last or K.local_dt(b, 12.0, tz)).date()
        W.tank_end[y] = st["level"]
        tickets_by_bol = {}
        for e in out:
            tickets_by_bol.setdefault(e["bol"]["bol"], []).append(e)
        for v in tickets_by_bol.values():
            if len(v) > 1:
                for e in v:
                    e["split"] = True
    return out

"""The truth behind task478's pack: the Tamsett Basin Air Pollution Control District's Lowry Creek corridor, its
fourteen facilities with SCR-controlled combustion units, how each unit ran from 2017 to 2026, its catalysts, its
source tests and the NOx it emitted in 2026. Only pack.py (which writes the files) and checks.py (which compares the cut
pack with this truth) read this module.

An SCR catalyst loses activity with every hour its unit fires. A unit with a continuous monitor closes its ammonia
injection on the monitor's NOx and holds its rate near a setpoint; a unit without one injects ammonia on load,
open-loop, so its NOx rate climbs from the day its catalyst is installed until the next is: the rate is the unit's own
fresh level times exp(BETA times the operating hours on the catalyst). A source test reads that rate on its day, with
the test's own scatter."""
import datetime as dt
import functools

import numpy as np

SEED = 4787
YEAR = 2026
DISTRICT = "Tamsett Basin Air Pollution Control District"
SHORT = "Tamsett Basin APCD"
PLAN = "Lowry Creek Community Emissions Reduction Plan 2027"
RULE = "Rule 4306"
PEOPLE = {"manager": "Nancy Hansen", "engineer": "Brian Daniels"}

BETA = 0.48 / 10000            # log NOx rate per operating hour on the catalyst, open-loop ammonia injection
TEST_SD = 0.065                # a source test's scatter about the day's true rate (log)
LEVEL_SD = 0.08                # a unit's fresh level about its kind's
FD_NG = 8710.0                 # Method 19 dry F-factor, natural gas (dscf/MMBtu)
FD_BIO = 9570.0                # the district's dry F-factor for landfill and digester gas (dscf/MMBtu)
HHV_NG = 1037.0                # pipeline gas higher heating value (Btu/scf)
K_NO2 = 1.194e-7               # lb/dscf per ppm NOx as NO2
START = dt.date(2017, 1, 1)
END = dt.date(2026, 12, 31)
DAYS = [START + dt.timedelta(days=i) for i in range((END - START).days + 1)]


def ppm_to_lb(ppm, o2ref, fd):
    """lb/MMBtu from ppmvd at the reference oxygen (Method 19)."""
    return ppm * K_NO2 * fd * 20.9 / (20.9 - o2ref)


def lb_to_ppm(lb, o2ref, fd):
    return lb / (K_NO2 * fd * 20.9 / (20.9 - o2ref))


# code, name, what it is
FACILITIES = [
    ("F01", "Wexley Point Energy Center", "combined-cycle power plant"),
    ("F02", "Ashgrove Refining", "petroleum refinery"),
    ("F03", "Valmora Glass Works", "container glass plant"),
    ("F04", "Sedge Hollow Landfill Gas", "landfill gas power plant"),
    ("F05", "Haskett Ridge Compressor Station", "natural gas compressor station"),
    ("F06", "St. Aldric Medical Center", "hospital central plant"),
    ("F07", "Lindqvist Paperboard", "paperboard mill"),
    ("F08", "Tamsett State University", "university central plant"),
    ("F09", "Briar Flats Water Reclamation", "wastewater treatment plant"),
    ("F10", "Merriwell Foods", "tomato cannery"),
    ("F11", "Harrow Peaking Station", "peaking power plant"),
    ("F12", "Orchard Basin Almond Growers", "almond processor"),
    ("F13", "Penrose Tire Retreading", "tire retreader"),
    ("F14", "Quarry Lane Data Center", "data center"),
]
FAC_NAME = {c: n for c, n, _ in FACILITIES}
# the district's facility numbers; Haskett Ridge changed hands in 2023 and was renumbered
FAC_NO = {"F01": "0418", "F02": "0102", "F03": "0577", "F04": "1240", "F05": "0912", "F06": "0761", "F07": "0233",
          "F08": "0350", "F09": "1102", "F10": "0645", "F11": "1318", "F12": "0880", "F13": "1027", "F14": "1455"}
RENUMBERED = ("F05", "0705", dt.date(2023, 4, 3), "Kittredge Midstream", "Haskett Ridge Pipeline LLC")

# share of a month's hours a unit fires, January to December
PROFILES = {
    "base": [.95, .94, .93, .90, .94, .95, .95, .95, .93, .90, .94, .95],
    "base2": [.86, .86, .88, .80, .84, .86, .84, .86, .84, .82, .86, .88],
    "cycle": [.62, .64, .66, .60, .66, .78, .86, .86, .76, .64, .62, .62],
    "heat": [.82, .80, .66, .44, .24, .14, .10, .10, .16, .40, .66, .80],
    "can": [0, 0, 0, 0, 0, .06, .92, .97, .96, .58, 0, 0],
    "summer": [0, 0, 0, .02, .10, .30, .46, .46, .26, .05, 0, 0],
    "peak": [.01, .01, .01, .02, .04, .08, .15, .15, .07, .02, .01, .01],
    "almond": [.12, 0, 0, 0, 0, 0, 0, .58, .88, .86, .64, .32],
    "prime": [.30, .28, .24, .20, .22, .30, .40, .42, .32, .22, .24, .30],
}
# kind: fresh level (lb/MMBtu, open-loop units), permit limit (ppmvd), reference oxygen (per cent)
KINDS = {
    "engine": (0.0195, 11.0, 15.0),
    "dgengine": (0.0196, 15.0, 15.0),
    "boiler": (0.0032, 9.0, 3.0),
    "heater": (0.0110, 7.0, 3.0),
    "turbine": (0.0074, 2.5, 15.0),
    "furnace": (0.0350, 0.0, 0.0),
}

# Units. device, facility, unit id, description, kind, MMBtu/hr, fuel, profile, monitored, load, test month, test
# cycle in years and the parity of its test years (None for monitored units), catalyst dates (the first is the SCR's
# installation for the rule's 2018 compliance date), and dated changes to the test calendar: ("defer", due, done) or
# ("extra", date).
D = dt.date
UNITS = [
    # Wexley Point: two combined-cycle turbines on monitors, an auxiliary boiler tested every year
    ("D-1101", "F01", "GT-1", "combustion turbine with duct burner, combined cycle", "turbine", 455, "ng", "base", 1, .86, None, None, None, [], []),
    ("D-1102", "F01", "GT-2", "combustion turbine with duct burner, combined cycle", "turbine", 455, "ng", "base2", 1, .84, None, None, None, [], []),
    ("D-1103", "F01", "AB-1", "auxiliary boiler", "boiler", 82, "ng", "peak", 0, .70, 6, 1, None,
     [D(2017, 5, 8)], []),
    # Ashgrove: two process heaters on monitors, two boilers tested every year
    ("D-1201", "F02", "H-101", "crude unit process heater", "heater", 228, "ng", "base", 1, .82, None, None, None, [], []),
    ("D-1202", "F02", "H-102", "reformer process heater", "heater", 214, "ng", "base", 1, .84, None, None, None, [], []),
    ("D-1203", "F02", "B-1", "steam boiler", "boiler", 124, "ng", "base2", 0, .78, 11, 1, None,
     [D(2017, 7, 10), D(2019, 9, 23), D(2021, 11, 15), D(2024, 2, 5)], []),
    ("D-1204", "F02", "B-2", "steam boiler", "boiler", 124, "ng", "base2", 0, .76, 12, 1, None,
     [D(2017, 8, 14), D(2020, 3, 2), D(2022, 6, 20), D(2024, 10, 14)], []),
    # Valmora: the glass furnace on a monitor, a process boiler
    ("D-1301", "F03", "F-1", "regenerative glass melting furnace", "furnace", 168, "ng", "base", 1, .90, None, None, None, [], []),
    ("D-1302", "F03", "B-2", "process steam boiler", "boiler", 46, "ng", "heat", 0, .74, 3, 1, None,
     [D(2017, 9, 11), D(2021, 8, 9), D(2025, 9, 15)], []),
    # Sedge Hollow: four lean-burn landfill gas engines, every two years in odd years
    ("D-1401", "F04", "E-1", "lean-burn engine generator, landfill gas", "engine", 19.4, "lfg", "base", 0, .91, 3, 2, 1,
     [D(2017, 6, 5), D(2019, 1, 21), D(2021, 2, 1), D(2023, 1, 9), D(2025, 1, 20)], []),
    ("D-1402", "F04", "E-2", "lean-burn engine generator, landfill gas", "engine", 19.4, "lfg", "base", 0, .90, 3, 2, 1,
     [D(2017, 6, 12), D(2019, 2, 4), D(2021, 2, 8), D(2023, 1, 16), D(2025, 1, 27)], []),
    ("D-1403", "F04", "E-3", "lean-burn engine generator, landfill gas", "engine", 19.4, "lfg", "base", 0, .91, 3, 2, 1,
     [D(2017, 6, 19), D(2019, 2, 11), D(2021, 2, 22), D(2023, 1, 23), D(2025, 2, 3)], []),
    ("D-1404", "F04", "E-4", "lean-burn engine generator, landfill gas", "engine", 19.4, "lfg", "base", 0, .89, 3, 2, 1,
     [D(2017, 6, 26), D(2019, 2, 18), D(2021, 3, 1), D(2023, 2, 6), D(2025, 2, 10)], []),
    # Haskett Ridge: three lean-burn compressor engines, every two years in odd years
    ("D-1501", "F05", "C-1", "lean-burn compressor engine", "engine", 24.2, "ng", "base2", 0, .92, 9, 2, 1,
     [D(2017, 4, 3), D(2019, 6, 10), D(2021, 8, 2), D(2023, 10, 9), D(2025, 12, 1)], []),
    ("D-1502", "F05", "C-2", "lean-burn compressor engine", "engine", 24.2, "ng", "base2", 0, .91, 9, 2, 1,
     [D(2017, 4, 10), D(2019, 6, 17), D(2021, 8, 9), D(2023, 10, 16), D(2025, 12, 8)], []),
    ("D-1503", "F05", "C-3", "lean-burn compressor engine", "engine", 24.2, "ng", "base2", 0, .92, 10, 2, 1,
     [D(2017, 4, 17), D(2019, 6, 24), D(2021, 8, 16), D(2023, 10, 23), D(2025, 12, 15)], []),
    # St. Aldric: two cogeneration engines tested every two years in even years, two boilers every year
    ("D-1601", "F06", "CG-1", "lean-burn cogeneration engine", "engine", 24.6, "ng", "base", 0, .93, 10, 2, 0,
     [D(2017, 3, 6), D(2018, 12, 3), D(2020, 9, 14), D(2022, 6, 6), D(2024, 9, 9)],
     [("defer", D(2026, 10, 14), D(2027, 1, 19))]),
    ("D-1602", "F06", "CG-2", "lean-burn cogeneration engine", "engine", 24.6, "ng", "base", 0, .92, 10, 2, 0,
     [D(2017, 3, 13), D(2018, 12, 10), D(2020, 9, 21), D(2022, 6, 13), D(2024, 9, 16)],
     [("defer", D(2026, 10, 21), D(2027, 1, 26))]),
    ("D-1603", "F06", "B-1", "hot water boiler", "boiler", 40, "ng", "heat", 0, .70, 1, 1, None,
     [D(2017, 10, 2), D(2022, 9, 19)], []),
    ("D-1604", "F06", "B-2", "hot water boiler", "boiler", 40, "ng", "heat", 0, .68, 1, 1, None,
     [D(2017, 10, 9), D(2023, 5, 15)], []),
    # Lindqvist: the paperboard mill's power boiler on a monitor
    ("D-1701", "F07", "PB-1", "power boiler", "boiler", 326, "ng", "base", 1, .80, None, None, None, [], []),
    # Tamsett State: the campus turbine on a monitor, a heating boiler, a summer peak-shaving engine
    ("D-1801", "F08", "GT-3", "combustion turbine, cogeneration", "turbine", 112, "ng", "base2", 1, .82, None, None, None, [], []),
    ("D-1802", "F08", "B-4", "heating boiler", "boiler", 72, "ng", "heat", 0, .72, 2, 1, None,
     [D(2017, 8, 21), D(2023, 8, 14)], []),
    ("D-1803", "F08", "E-5", "lean-burn peak-shaving engine", "engine", 31, "ng", "summer", 0, .88, 7, 1, None,
     [D(2017, 5, 15)], []),
    # Briar Flats: two digester gas engines, every two years in even years
    ("D-1901", "F09", "DG-1", "lean-burn digester gas engine", "dgengine", 12.6, "dg", "base", 0, .86, 5, 2, 0,
     [D(2017, 7, 17), D(2020, 2, 3), D(2022, 9, 12), D(2025, 4, 7)], []),
    ("D-1902", "F09", "DG-2", "lean-burn digester gas engine", "dgengine", 12.6, "dg", "base", 0, .85, 5, 2, 0,
     [D(2017, 7, 24), D(2020, 3, 9), D(2022, 10, 3), D(2025, 5, 5)], []),
    # Merriwell: three cannery boilers, every year in the season
    ("D-2001", "F10", "B-1", "process steam boiler", "boiler", 98, "ng", "can", 0, .82, 8, 1, None,
     [D(2017, 6, 12)], []),
    ("D-2002", "F10", "B-2", "process steam boiler", "boiler", 98, "ng", "can", 0, .80, 8, 1, None,
     [D(2017, 6, 19)], []),
    ("D-2003", "F10", "B-3", "process steam boiler", "boiler", 98, "ng", "can", 0, .81, 8, 1, None,
     [D(2017, 6, 26), D(2023, 6, 5)], []),
    # Harrow: two simple-cycle peakers on monitors
    ("D-2101", "F11", "GT-A", "simple-cycle combustion turbine", "turbine", 418, "ng", "peak", 1, .88, None, None, None, [], []),
    ("D-2102", "F11", "GT-B", "simple-cycle combustion turbine", "turbine", 418, "ng", "peak", 1, .88, None, None, None, [], []),
    # Orchard Basin: a dryer boiler, every year in the harvest
    ("D-2201", "F12", "B-1", "dryer steam boiler", "boiler", 80, "ng", "almond", 0, .80, 9, 1, None,
     [D(2017, 7, 31)], []),
    # Penrose: a process boiler, every two years in even years
    ("D-2301", "F13", "B-1", "process steam boiler", "boiler", 35, "ng", "base2", 0, .66, 5, 2, 0,
     [D(2017, 9, 25), D(2022, 4, 18)], []),
    # Quarry Lane: two prime-power engines, every two years in odd years
    ("D-2401", "F14", "E-6", "lean-burn prime-power engine", "engine", 19.8, "ng", "prime", 0, .84, 6, 2, 1,
     [D(2017, 11, 6), D(2022, 5, 9)], []),
    ("D-2402", "F14", "E-7", "lean-burn prime-power engine", "engine", 19.8, "ng", "prime", 0, .84, 6, 2, 1,
     [D(2017, 11, 13), D(2022, 5, 16)], []),
]
FIELDS = ("device", "facility", "unit", "desc", "kind", "rating", "fuel", "profile", "monitored", "load", "test_month",
          "cycle", "parity", "catalysts", "calendar")
UNIT = {u[0]: dict(zip(FIELDS, u)) for u in UNITS}
OPEN = [d for d, u in UNIT.items() if not u["monitored"]]
MONITORED = [d for d, u in UNIT.items() if u["monitored"]]
# monitored units' NOx setpoint (lb/MMBtu), held by closed-loop ammonia injection
SETPOINT = {"D-1101": .0070, "D-1102": .0071, "D-1201": .0104, "D-1202": .0101, "D-1301": .0335, "D-1701": .0058,
            "D-1801": .0072, "D-2101": .0083, "D-2102": .0086}
# units whose fresh level departs from their kind's (an older engine design, a leaner landfill gas burn)
LEVEL_KIND = {"D-1601": .0215, "D-1602": .0215, "D-1401": .0172, "D-1402": .0172, "D-1403": .0172, "D-1404": .0172}
# an overhaul that keeps a unit down (its catalyst runs no hours)
DOWN = {"D-1601": (D(2026, 10, 5), D(2026, 10, 24)), "D-1602": (D(2026, 10, 12), D(2026, 10, 31)),
        "D-1503": (D(2024, 4, 1), D(2024, 6, 14))}


def _rng(k):
    return np.random.default_rng([SEED, k])


def run_hours(dev):
    """The unit's operating hours each day, 2017 to 2026: its profile's share of the month, a month-to-month swing, and
    nothing before its SCR went in or while it is down."""
    u = UNIT[dev]
    rng = _rng(int(dev[2:]))
    prof = PROFILES[u["profile"]]
    swing = {(y, m): float(np.clip(rng.normal(1.0, 0.035), 0.88, 1.08)) for y in range(2017, 2027) for m in range(1, 13)}
    first = u["catalysts"][0] if u["catalysts"] else START
    down = DOWN.get(dev)
    out = {}
    for d in DAYS:
        h = 24.0 * min(1.0, prof[d.month - 1] * swing[(d.year, d.month)])
        if d < first or (down and down[0] <= d < down[1]):
            h = 0.0
        out[d] = h
    return out


def _cat_hours(cats, hours):
    out, h, k = {}, 0.0, 0
    for d in DAYS:
        while k < len(cats) and d >= cats[k]:
            h, k = 0.0, k + 1
        out[d] = h
        h += hours[d]
    return out


def catalyst_hours(dev, hours=None):
    """Operating hours on the catalyst in service at the start of each day."""
    return _cat_hours(list(schedule(dev)[0]), hours or run_hours(dev))


def level(dev):
    """The unit's own fresh-catalyst NOx rate (lb/MMBtu)."""
    u = UNIT[dev]
    base = LEVEL_KIND.get(dev, KINDS[u["kind"]][0])
    return base * float(np.exp(_rng(1000 + int(dev[2:])).normal(0, LEVEL_SD)))


def rate(dev, h):
    return level(dev) * np.exp(BETA * h)


def heat_rate(dev):
    """MMBtu an operating hour (the rating at the unit's load), and the month-to-month load swing."""
    u = UNIT[dev]
    return u["rating"] * u["load"]


def heat_input(dev, hours=None):
    hours = hours or run_hours(dev)
    hr = heat_rate(dev)
    return {d: h * hr for d, h in hours.items()}


def test_dates(dev):
    """The unit's source test dates: its month in its cycle's years from 2018, a deferred test moved to its new date."""
    u = UNIT[dev]
    if u["monitored"]:
        return []
    out = []
    for y in range(2018, 2027):
        if u["cycle"] == 2 and y % 2 != u["parity"]:
            continue
        day = 6 + (int(dev[2:]) * 7 + y) % 18
        out.append(D(y, u["test_month"], day))
    for ch in u["calendar"]:
        if ch[0] == "defer":
            out = [t for t in out if not (t.year == ch[1].year and t.month == ch[1].month)]
    return sorted(t for t in out if t <= END)


def limit_rate(dev):
    """The unit's permit limit in lb/MMBtu (None for the furnace, which has no ppm limit)."""
    u = UNIT[dev]
    ppm, o2 = KINDS[u["kind"]][1], KINDS[u["kind"]][2]
    return ppm_to_lb(ppm, o2, FD_NG if u["fuel"] == "ng" else FD_BIO) if ppm else None


@functools.lru_cache(maxsize=None)
def schedule(dev):
    """The unit's catalysts and source tests to 2026: the designed catalyst dates and routine tests and, for a test over
    the permit limit, the district's notice of violation, a retest after the catalyst due within six months of it or,
    with none due, after a corrective replacement. Returns (catalyst dates, tests), each test a dict."""
    u = UNIT[dev]
    if u["monitored"]:
        return tuple(sorted(u["catalysts"])), ()
    hrs = run_hours(dev)
    cats = sorted(u["catalysts"])
    lim = limit_rate(dev)
    rng = _rng(2000 + int(dev[2:]))
    fix = _rng(2500 + int(dev[2:]))
    queue = [(t, "routine") for t in test_dates(dev)]
    done = []
    while queue:
        queue.sort()
        t, kind = queue.pop(0)
        h = _cat_hours(cats, hrs)[t] + 6.0
        true = rate(dev, h)
        meas = true * float(np.exp(rng.normal(0, TEST_SD)))
        report = t + dt.timedelta(days=int(fix.integers(21, 36)))
        x = dict(date=t, kind=kind, cat_hours=h, true=true, measured=meas, report=report, nov=None)
        if lim and meas > lim:
            x["nov"] = report + dt.timedelta(days=int(fix.integers(3, 11)))
            due = [c for c in cats if t < c <= t + dt.timedelta(days=180)]
            c = due[0] if due else x["nov"] + dt.timedelta(days=int(fix.integers(20, 46)))
            r = c + dt.timedelta(days=int(fix.integers(28, 46)))
            if c <= END and not due:
                cats = sorted(cats + [c])
            if r <= END:
                queue.append((r, "retest"))
        done.append(x)
    return tuple(cats), tuple(done)


def tests(dev):
    """Each test: date, kind, catalyst hours, the true rate that day and the rate the test measured (lb/MMBtu), the
    report's date and any notice of violation."""
    return [dict(x) for x in schedule(dev)[1]]


def true_nox_2026(dev):
    """lb of NOx the unit emitted in 2026: each day's heat input times the day's rate at its mid-day catalyst hours."""
    if UNIT[dev]["monitored"]:
        return None
    hrs = run_hours(dev)
    cat = catalyst_hours(dev, hrs)
    hr = heat_rate(dev)
    lv = level(dev)
    tot = 0.0
    for d in DAYS:
        if d.year == YEAR and hrs[d] > 0:
            tot += hrs[d] * hr * lv * np.exp(BETA * (cat[d] + hrs[d] / 2))
    return tot


def cems_hours(dev):
    """A monitored unit's 2026 operating hours: (local standard datetime, operating time, heat input MMBtu, NOx
    lb/MMBtu, substitute flag). Startup hours run high until the catalyst reaches temperature."""
    u = UNIT[dev]
    rng = _rng(3000 + int(dev[2:]))
    prof = PROFILES[u["profile"]]
    sp = SETPOINT[dev]
    out = []
    on = False
    for d in DAYS:
        if d.year != YEAR:
            continue
        share = prof[d.month - 1] * float(np.clip(rng.normal(1, .03), .85, 1.1))
        for hr in range(24):
            if u["profile"] == "peak":
                run = rng.random() < share * (2.4 if 12 <= hr <= 20 else 0.2)
            else:
                run = rng.random() < (share if not on else min(0.995, share + 0.08))
            if not run:
                on = False
                continue
            start = not on
            on = True
            hi = u["rating"] * u["load"] * float(np.clip(rng.normal(1, .06), .55, 1.08))
            r = sp * float(np.exp(rng.normal(0, .05)))
            if start:
                r *= float(rng.uniform(2.5, 4.0))
                hi *= 0.6
            sub = rng.random() < 0.012
            if sub:
                r = sp * 1.10
            out.append((dt.datetime(d.year, d.month, d.day, hr), 1.0, hi, r, sub))
    return out


# ---------------------------------------------------------------- the gas utility's meters and bills (ask A)
UTILITY = "Tamsett Valley Gas"
CONVERSION = D(2026, 7, 1)      # the utility's new billing system: bills read on or after it carry therms
# facility: [(meter, account, pressure multiplier, read day of the month, share of the facility's gas)], the gas the
# facility burns outside the plan's units (MMBtu a day, and its winter heating swing)
METERS = {
    "F01": [("TV-40118", "7701-2251", 2.840, 4, .55), ("TV-40119", "7701-2251", 2.840, 4, .45)],
    "F02": [("TV-31502", "7702-0864", 2.480, 9, .62), ("TV-31503", "7702-0865", 2.480, 9, .38)],
    "F03": [("TV-22710", "7703-4410", 1.980, 12, 1.0)],
    "F04": [("TV-09931", "7704-1187", 1.000, 1, 1.0)],
    "F05": [("TV-51207", "7705-3302", 2.120, 6, 1.0)],
    "F06": [("TV-11846", "7706-0423", 1.420, 21, .70), ("TV-11847", "7706-0424", 1.000, 21, .30)],
    "F07": [("TV-38004", "7707-1950", 2.660, 11, .58), ("TV-38005", "7707-1950", 2.660, 11, .42)],
    "F08": [("TV-14422", "7708-6610", 1.640, 25, 1.0)],
    "F09": [("TV-07715", "7709-0332", 1.000, 18, 1.0)],
    "F10": [("TV-26651", "7710-2804", 1.760, 3, 1.0)],
    "F11": [("TV-45020", "7711-0019", 2.920, 14, 1.0)],
    "F12": [("TV-19388", "7712-5126", 1.380, 27, 1.0)],
    "F13": [("TV-19507", "7713-5130", 1.000, 27, 1.0)],
    "F14": [("TV-30876", "7714-0691", 1.520, 8, 1.0)],
}
OTHER_GAS = {"F01": (60, .2), "F02": (420, .15), "F03": (140, .25), "F04": (9, .6), "F05": (12, .5), "F06": (55, .9),
             "F07": (180, .2), "F08": (95, 1.0), "F09": (7, .6), "F10": (40, .3), "F11": (4, .5), "F12": (16, .5),
             "F13": (22, .5), "F14": (30, .3)}
EXCHANGE = ("TV-26651", D(2026, 4, 14), "TV-26690")   # Merriwell's meter exchanged mid-cycle
EVC_MULT = 1.01                # every meter delivering above the base pressure carries an electronic volume corrector


def evc_factor(meter, d):
    """A volume corrector's corrected CCF per unit of the meter's index over a period ending on d: its pressure factor
    and the gas temperature, colder (denser) gas in winter."""
    mult = {m[0]: m[2] for ms in METERS.values() for m in ms}.get(meter, 1.76)
    return mult * (1 + 0.005 * np.cos(2 * np.pi * (d.timetuple().tm_yday - 20) / 365.0)
                   + 0.0015 * _rng(int(meter[3:]) * 1000 + d.year * 13 + d.month).normal())


def btu_factor(d):
    """The utility's heat content (therms a corrected CCF) over a billing period ending on d."""
    return round(1.037 + 0.011 * np.cos(2 * np.pi * (d.timetuple().tm_yday - 30) / 365.0)
                 + 0.004 * _rng(d.year * 100 + d.month).normal(), 3)


def facility_gas(code):
    """MMBtu of utility gas the facility used each day: its plan units on pipeline gas plus everything else."""
    other, swing = OTHER_GAS[code]
    rng = _rng(4000 + int(code[1:]))
    gas = {}
    for d in (D(2025, 11, 1) + dt.timedelta(days=i) for i in range((D(2027, 3, 2) - D(2025, 11, 1)).days)):
        heat = 1 + swing * max(0.0, np.cos(2 * np.pi * (d.timetuple().tm_yday - 15) / 365.0))
        gas[d] = other * heat * float(np.clip(rng.normal(1, .08), .7, 1.3))
    for dev, u in UNIT.items():
        if u["facility"] != code or u["fuel"] != "ng":
            continue
        if u["monitored"]:
            daily = {}
            for t, _, hi, _, _ in cems_hours(dev):
                daily[t.date()] = daily.get(t.date(), 0.0) + hi
            for d in gas:
                gas[d] += daily.get(d, 0.0) if d.year == YEAR else u["rating"] * u["load"] * 24 * PROFILES[u["profile"]][d.month - 1]
        else:
            hrs = run_hours(dev)
            hr = heat_rate(dev)
            for d in gas:
                gas[d] += hrs.get(d, 24 * PROFILES[u["profile"]][d.month - 1]) * hr
    return gas


def _read_days(code, mday):
    """The meter's read dates from November 2025 to February 2027: its day each month, off weekends."""
    out = []
    for y, m in [(2025, 11), (2025, 12)] + [(2026, k) for k in range(1, 13)] + [(2027, 1), (2027, 2)]:
        d = D(y, m, min(mday, 28))
        while d.weekday() >= 5 or (d.month, d.day) in ((1, 1), (7, 3), (12, 25)):
            d += dt.timedelta(days=1)
        out.append(d)
    return out


def bills():
    """Every bill line the utility issued from the November 2025 read on: (bill id, account, meter, read from, read
    to, prior index, current index, multiplier, BTU factor, usage, estimated, facility, true therms). From the new
    system's first bills (read on or after CONVERSION) the usage column carries therms; before, corrected CCF."""
    out = []
    bid = 81320000
    for code, meters in METERS.items():
        gas = facility_gas(code)
        rng = _rng(5000 + int(code[1:]))
        for meter, acct, mult, mday, share in meters:
            days = _read_days(code, mday)
            index = float(rng.integers(20000, 900000))
            for a, b in zip(days[:-1], days[1:]):
                mmbtu = sum(gas.get(a + dt.timedelta(days=i), 0.0) for i in range((b - a).days)) * share
                btu = btu_factor(b)
                ccf = mmbtu * 10.0 / btu
                pieces = [(meter, a, b, ccf)]
                if meter == EXCHANGE[0] and a < EXCHANGE[1] < b:
                    f = (EXCHANGE[1] - a).days / (b - a).days
                    pieces = [(meter, a, EXCHANGE[1], ccf * f), (EXCHANGE[2], EXCHANGE[1], b, ccf * (1 - f))]
                for mtr, ra, rb, c in pieces:
                    if mtr == EXCHANGE[2] and ra == EXCHANGE[1]:
                        index = 0.0
                    evc = mult >= EVC_MULT
                    raw = c / (evc_factor(mtr, rb) if evc else mult)
                    prior = int(round(index))
                    current = int(round(index + raw))
                    index += raw
                    ccf = c if evc else (current - prior) * mult     # the corrector's volume, or the index corrected
                    usage = int(round(ccf * btu)) if rb >= CONVERSION else int(round(ccf))
                    therms = float(usage) if rb >= CONVERSION else usage * btu
                    bid += int(rng.integers(3, 40))
                    out.append(dict(bill=bid, account=acct, meter=mtr, read_from=ra, read_to=rb, prior=prior,
                                    current=current, mult=mult, evc=evc, btu=btu, usage=usage, est=False,
                                    facility=code, therms=therms))
                if meter == EXCHANGE[0] and b > EXCHANGE[1]:
                    meter = EXCHANGE[2]
    return out


def gas_2026(code, bl=None):
    """Ask A's truth: MMBtu delivered to the facility in 2026, each bill's therms spread over its read period by
    days."""
    bl = bl or bills()
    tot = 0.0
    for b in bl:
        if b["facility"] != code:
            continue
        n = (b["read_to"] - b["read_from"]).days
        lo, hi = max(b["read_from"], D(2026, 1, 1)), min(b["read_to"], D(2027, 1, 1))
        k = max(0, (hi - lo).days)
        tot += b["therms"] * k / n / 10.0
    return tot


# ---------------------------------------------------------------- emergency standby engines (ask B)
# tier: NOx certification (g/bhp-hr) the district's guidance applies; load factor for testing and emergency runs
TIER_NOX = {"Tier 1": 6.9, "Tier 2": 4.8, "Tier 3": 3.0, "Tier 4 Final": 0.30}
ENGINE_LF = 0.74
G_LB = 453.6                    # grams a pound, as the district's guidance writes it
# device, facility, bhp, tier, make and model, installed; a replacement in 2026: (date, old bhp, old tier, old model)
ENGINES = [
    ("D-3101", "F01", 1490, "Tier 2", "Caterpillar 3512B", D(2008, 5, 1), None),
    ("D-3201", "F02", 1110, "Tier 4 Final", "Cummins QSK38-G", D(2026, 5, 18), (D(2026, 5, 18), 1340, "Tier 1", "Caterpillar 3508")),
    ("D-3202", "F02", 755, "Tier 2", "Cummins QSX15-G9", D(2011, 9, 1), None),
    ("D-3301", "F03", 1340, "Tier 4 Final", "Caterpillar C32", D(2026, 8, 10), (D(2026, 8, 10), 1340, "Tier 2", "Caterpillar 3508B")),
    ("D-3401", "F04", 470, "Tier 3", "John Deere 6135HF485", D(2014, 3, 1), None),
    ("D-3501", "F05", 755, "Tier 4 Final", "Cummins QSX15-G", D(2026, 6, 22), (D(2026, 6, 22), 810, "Tier 1", "Detroit Series 60")),
    ("D-3601", "F06", 2220, "Tier 2", "Caterpillar 3516B", D(2009, 7, 1), None),
    ("D-3602", "F06", 2220, "Tier 4 Final", "Caterpillar 3516E", D(2026, 9, 14), (D(2026, 9, 14), 2220, "Tier 1", "Caterpillar 3516")),
    ("D-3603", "F06", 470, "Tier 2", "Cummins QSL9-G", D(2012, 4, 1), None),
    ("D-3701", "F07", 1110, "Tier 2", "Cummins KTA38-G", D(2006, 11, 1), None),
    ("D-3801", "F08", 1490, "Tier 4 Final", "MTU 16V2000", D(2026, 4, 27), (D(2026, 4, 27), 1490, "Tier 1", "Caterpillar 3512")),
    ("D-3802", "F08", 755, "Tier 2", "Cummins QSX15-G9", D(2010, 8, 1), None),
    ("D-3803", "F08", 470, "Tier 3", "Cummins QSL9-G7", D(2015, 6, 1), None),
    ("D-3901", "F09", 1110, "Tier 2", "Caterpillar 3412C", D(2007, 2, 1), None),
    ("D-4001", "F10", 470, "Tier 4 Final", "Cummins QSL9-G", D(2026, 7, 6), (D(2026, 7, 6), 470, "Tier 1", "Cummins 6CTA8.3")),
    ("D-4101", "F11", 470, "Tier 3", "Cummins QSL9-G7", D(2016, 1, 1), None),
    ("D-4201", "F12", 340, "Tier 2", "John Deere 6090HF485", D(2013, 6, 1), None),
    ("D-4301", "F13", 340, "Tier 3", "Cummins QSB7-G", D(2015, 3, 1), None),
    ("D-4401", "F14", 3000, "Tier 2", "Caterpillar 3516C", D(2017, 10, 1), None),
    ("D-4402", "F14", 3000, "Tier 2", "Caterpillar 3516C", D(2017, 10, 1), None),
    ("D-4403", "F14", 3000, "Tier 4 Final", "Caterpillar 3516E", D(2026, 10, 19), (D(2026, 10, 19), 3000, "Tier 2", "Caterpillar 3516C")),
    ("D-4404", "F14", 3000, "Tier 2", "Caterpillar 3516C", D(2017, 10, 1), None),
]
ENGINE = {e[0]: dict(zip(("device", "facility", "bhp", "tier", "model", "installed", "replaced"), e)) for e in ENGINES}
# power outages each facility's engines carried in 2026 (start, hours)
OUTAGES = {"F02": [(D(2026, 8, 19), 6.4)], "F06": [(D(2026, 1, 9), 3.1), (D(2026, 9, 2), 11.6)],
           "F08": [(D(2026, 9, 2), 9.8)], "F10": [(D(2026, 8, 19), 4.2)], "F12": [(D(2026, 9, 2), 14.5)],
           "F13": [(D(2026, 9, 2), 14.5)], "F14": [(D(2026, 3, 23), 2.2), (D(2026, 9, 2), 13.3)]}


def engine_runs(dev):
    """The engine's 2026 runs: (date, hours, purpose). A half-hour readiness run each week, an hour on load each
    month, and the facility's outages."""
    e = ENGINE[dev]
    rng = _rng(6000 + int(dev[2:]))
    out = []
    first = D(2026, 1, 1) + dt.timedelta(days=int(rng.integers(0, 7)))
    d = first
    while d.year == YEAR:
        if not (e["replaced"] and e["replaced"][0] - dt.timedelta(days=4) <= d <= e["replaced"][0]):
            out.append((d, round(float(rng.uniform(0.4, 0.6)), 1), "readiness"))
        d += dt.timedelta(days=7)
    for m in range(1, 13):
        day = D(YEAR, m, int(rng.integers(8, 23)))
        if not (e["replaced"] and e["replaced"][0] - dt.timedelta(days=4) <= day <= e["replaced"][0]):
            out.append((day, round(float(rng.uniform(0.9, 1.4)), 1), "load test"))
    for day, h in OUTAGES.get(e["facility"], []):
        out.append((day, round(h, 1), "emergency"))
    return sorted(out)


# facilities whose engine log records run time as hours and minutes (h.mm); the rest log decimal hours
HMM = ("F01", "F04", "F07", "F09", "F11", "F12", "F13")


def inspections():
    """Hour meter readings at the district's engine inspections, November 2025 to February 2027: (device, date,
    reading). The meter also runs through each start's warm-up and cool-down, which the logs leave out, and a replaced
    engine's meter starts again at its installation."""
    out = []
    for dev, e in ENGINE.items():
        rng = _rng(7000 + int(dev[2:]))
        runs = engine_runs(dev)
        extra = _rng(7500 + int(dev[2:])).uniform(0.03, 0.10, len(runs))
        runs = [(x, h + float(a), p) for (x, h, p), a in zip(runs, extra)]
        base = float(rng.uniform(300, 2600)) if not e["replaced"] else float(rng.uniform(800, 3100))
        rounds = (D(2025, 11, 3) + dt.timedelta(days=int(rng.integers(0, 20))),
                  D(2026, 11, 2) + dt.timedelta(days=int(rng.integers(0, 24))),
                  D(2027, 2, 1) + dt.timedelta(days=int(rng.integers(0, 10))))
        for d in rounds[1:] if e["replaced"] else rounds:     # an engine due for replacement skipped the 2025 round
            past = [r for r in runs if r[0] < d]
            if e["replaced"] and d >= e["replaced"][0]:
                read = 1.2 + sum(h for x, h, _ in past if x >= e["replaced"][0])
            else:
                read = base + sum(h for x, h, _ in past) + 0.0
            if d.year == 2027:
                read += float(rng.uniform(1.5, 4.0))
            out.append((dev, d, round(read, 1)))
    return out


def engine_nox_2026(code):
    """Ask B's truth: lb of NOx the facility's emergency engines emitted in 2026, each run at the engine then
    installed."""
    tot = 0.0
    for dev, e in ENGINE.items():
        if e["facility"] != code:
            continue
        for d, h, _ in engine_runs(dev):
            if e["replaced"] and d < e["replaced"][0]:
                bhp, tier = e["replaced"][1], e["replaced"][2]
            else:
                bhp, tier = e["bhp"], e["tier"]
            tot += h * bhp * ENGINE_LF * TIER_NOX[tier] / G_LB
    return tot


def everything():
    """All the truth the pack and the checks need, computed once."""
    units = {}
    for dev in UNIT:
        u = UNIT[dev]
        if u["monitored"]:
            ch = cems_hours(dev)
            units[dev] = dict(cems=ch, nox_2026=sum(round(hi * r, 2) for _, _, hi, r, _ in ch))
        else:
            hrs = run_hours(dev)
            units[dev] = dict(hours=hrs, cat=catalyst_hours(dev, hrs), tests=tests(dev), level=level(dev),
                              nox_2026=true_nox_2026(dev))
    fac = {}
    for dev, v in units.items():
        fac[UNIT[dev]["facility"]] = fac.get(UNIT[dev]["facility"], 0.0) + v["nox_2026"] / 2000.0
    bl = bills()
    return dict(units=units, facility_tons=fac, bills=bl, gas_2026={c: gas_2026(c, bl) for c in FAC_NAME},
                engine_lb={c: engine_nox_2026(c) for c in FAC_NAME}, inspections=inspections(),
                runs={dev: engine_runs(dev) for dev in ENGINE})


if __name__ == "__main__":
    e = everything()
    for c, t in sorted(e["facility_tons"].items(), key=lambda x: -x[1]):
        print("%s %-34s %7.2f  gas %10.0f MMBtu  engines %7.0f lb" % (c, FAC_NAME[c], t, e["gas_2026"][c],
                                                                    e["engine_lb"][c]))

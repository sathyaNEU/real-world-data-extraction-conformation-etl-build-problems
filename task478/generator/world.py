"""The truth behind task478's pack: the Tamsett Basin Air Pollution Control District's Lowry Creek corridor, the Rule
4306 boilers, steam generators and process heaters at its fourteen facilities, how each unit ran from 2018 to 2026, the
gas it burned, its source tests and the NOx it emitted in 2026. Only pack.py (which writes the files) and checks.py
(which compares the cut pack with this truth) read this module.

A low-NOx burner whose combustion air is set by volume at its tuning burns a richer gas hotter, so its NOx rate is its
own level times exp(K_HV times the rise of the gas's heat content over HREF, as a fraction of HREF). Tamsett Valley Gas
serves the corridor through two BTU areas: Eastside on interstate gas of steady heat content, Westside blended with the
Lowry Creek gas plant's residue gas, whose heat content follows the plant's ethane recovery from month to month. A source
test reads a burner's rate on its test month's gas, with the test's own scatter. The refinery's SCR units close their
ammonia injection on their monitors' NOx and hold their rate whatever the gas."""
import datetime as dt
import functools

import numpy as np

SEED = 4787
YEAR = 2026
DISTRICT = "Tamsett Basin Air Pollution Control District"
SHORT = "Tamsett Basin APCD"
PLAN = "Lowry Creek Community Emissions Reduction Plan 2027"
RULE = "Rule 4306"
PEOPLE = {"director": "Andrew Greene", "engineer": "Anna Haynes"}

K_HV = 6.0                      # d ln(NOx rate) / d(heat content / HREF), a low-NOx burner without oxygen trim
HREF = 1.035                    # the heat content (therms a CCF) a burner's level is quoted at
TEST_SD = 0.03                  # a source test's scatter about the day's true rate (log)
LEVEL_SD = 0.05                 # a burner's own level about its kind's (log)
FD_NG = 8710.0                  # Method 19 dry F-factor, natural gas (dscf/MMBtu)
K_NO2 = 1.194e-7                # lb/dscf per ppm NOx as NO2
START = dt.date(2018, 1, 1)
END = dt.date(2026, 12, 31)
DAYS = [START + dt.timedelta(days=i) for i in range((END - START).days + 1)]
D = dt.date


def ppm_to_lb(ppm, o2ref=3.0, fd=FD_NG):
    """lb/MMBtu from ppmvd at the reference oxygen (Method 19)."""
    return ppm * K_NO2 * fd * 20.9 / (20.9 - o2ref)


def lb_to_ppm(lb, o2ref=3.0, fd=FD_NG):
    return lb / (K_NO2 * fd * 20.9 / (20.9 - o2ref))


# code, name, what it is, BTU area
FACILITIES = [
    ("F01", "Wexley Point Energy Center", "combined-cycle power plant (auxiliary boiler)", "E"),
    ("F02", "Ashgrove Refining", "petroleum refinery", "E"),
    ("F03", "Valmora Renewable Fuels", "fuel ethanol plant", "E"),
    ("F04", "Sedge Hollow Creamery", "cheese and whey plant", "W"),
    ("F05", "Haskett Ridge Poultry", "poultry processing and rendering plant", "E"),
    ("F06", "St. Aldric Medical Center", "hospital central plant", "E"),
    ("F07", "Lindqvist Paperboard", "paperboard mill", "W"),
    ("F08", "Tamsett State University", "university central plant", "W"),
    ("F09", "Briar Flats Water Reclamation", "wastewater treatment plant", "E"),
    ("F10", "Merriwell Foods", "tomato cannery", "W"),
    ("F11", "Harrow Linen Services", "commercial laundry", "E"),
    ("F12", "Orchard Basin Almond Growers", "almond processor", "W"),
    ("F13", "Penrose Tire Retreading", "tire retreader", "W"),
    ("F14", "Quarry Lane Correctional Facility", "state correctional facility", "W"),
]
FAC_NAME = {c: n for c, n, _, _ in FACILITIES}
FAC_WHAT = {c: w for c, _, w, _ in FACILITIES}
AREA = {c: a for c, _, _, a in FACILITIES}
AREA_NAME = {"W": "Westside", "E": "Eastside"}
# the district's facility numbers; Haskett Ridge changed hands in 2023 and was renumbered
FAC_NO = {"F01": "0418", "F02": "0102", "F03": "0577", "F04": "1240", "F05": "0912", "F06": "0761", "F07": "0233",
          "F08": "0350", "F09": "1102", "F10": "0645", "F11": "1318", "F12": "0880", "F13": "1027", "F14": "1455"}
RENUMBERED = ("F05", "0705", dt.date(2023, 4, 3), "Kittredge Farms Inc.", "Haskett Ridge Poultry LLC")

# share of a month's hours a unit fires, January to December
PROFILES = {
    "base": [.95, .94, .93, .90, .94, .95, .95, .95, .93, .90, .94, .95],
    "base2": [.86, .86, .88, .80, .84, .86, .84, .86, .84, .82, .86, .88],
    "heat": [.82, .80, .66, .44, .24, .14, .10, .10, .16, .40, .66, .80],
    "can": [0, 0, 0, 0, 0, .06, .92, .97, .96, .58, 0, 0],
    "almond": [.12, 0, 0, 0, 0, 0, 0, .58, .88, .86, .64, .32],
    "peak": [.05, .04, .04, .05, .06, .10, .18, .18, .10, .05, .04, .05],
    "week": [.62, .62, .63, .62, .63, .62, .63, .63, .62, .63, .62, .62],
}

# Units. device, facility, unit id, description, rating MMBtu/hr, profile, monitored, load, control, test month, test
# cycle in years, parity of the test years on a two-year cycle, permit limit (ppmvd at 3 per cent oxygen), the kind's
# level (lb/MMBtu at HREF), and dated changes to the test calendar: ("defer", due, done).
UNITS = [
    ("D-1103", "F01", "AB-1", "auxiliary boiler", 82, "peak", 0, .70, "LNB", 6, 1, None, 9, .0072, []),
    ("D-1201", "F02", "H-101", "crude unit process heater", 452, "base", 1, .82, "SCR", None, 0, None, 5, .0061, []),
    ("D-1202", "F02", "H-102", "reformer process heater", 386, "base", 1, .84, "SCR", None, 0, None, 5, .0060, []),
    ("D-1203", "F02", "B-1", "steam boiler", 248, "base2", 1, .78, "SCR", None, 0, None, 5, .0058, []),
    ("D-1204", "F02", "H-201", "vacuum unit heater", 64, "base", 0, .72, "LNB", 3, 1, None, 9, .0072, []),
    ("D-1205", "F02", "H-202", "hydrotreater charge heater", 58, "base", 0, .70, "LNB", 3, 1, None, 9, .0072, []),
    ("D-1301", "F03", "B-1", "package steam boiler", 174, "base", 0, .74, "LNB", 3, 1, None, 9, .0075, []),
    ("D-1302", "F03", "B-2", "package steam boiler", 174, "base", 0, .72, "LNB", 4, 1, None, 9, .0075,
     [("defer", D(2026, 4, 15), D(2026, 6, 16))]),
    ("D-1401", "F04", "B-1", "process steam boiler", 108, "base", 0, .78, "LNB", 8, 1, None, 9, .0072, []),
    ("D-1402", "F04", "B-2", "process steam boiler", 108, "base", 0, .77, "LNB", 8, 1, None, 9, .0072, []),
    ("D-1403", "F04", "B-3", "process steam boiler", 108, "base", 0, .74, "LNB", 8, 1, None, 9, .0072, []),
    ("D-1501", "F05", "B-1", "process steam boiler", 140, "base2", 0, .76, "LNB", 10, 2, 1, 9, .0050, []),
    ("D-1502", "F05", "B-2", "process steam boiler", 140, "base2", 0, .74, "LNB", 10, 2, 1, 9, .0050, []),
    ("D-1601", "F06", "B-1", "hot water boiler", 66, "heat", 0, .70, "LNB", 1, 1, None, 9, .0072, []),
    ("D-1602", "F06", "B-2", "hot water boiler", 66, "heat", 0, .68, "LNB", 1, 1, None, 9, .0072, []),
    ("D-1603", "F06", "B-3", "steam boiler", 38, "base", 0, .60, "LNB", 9, 1, None, 9, .0072, []),
    ("D-1701", "F07", "PB-1", "power boiler", 300, "base", 1, .82, "LNB", None, 0, None, 9, .0072, []),
    ("D-1702", "F07", "PB-2", "package steam boiler", 96, "base2", 0, .70, "LNB", 2, 1, None, 9, .0072, []),
    ("D-1703", "F07", "PB-3", "package steam boiler", 96, "base2", 0, .68, "LNB", 2, 1, None, 9, .0072, []),
    ("D-1801", "F08", "B-1", "central plant steam boiler", 148, "heat", 0, .72, "LNB", 5, 1, None, 15, .0110, []),
    ("D-1802", "F08", "B-2", "central plant steam boiler", 148, "heat", 0, .70, "LNB", 5, 1, None, 15, .0110, []),
    ("D-1803", "F08", "B-3", "central plant steam boiler", 148, "heat", 0, .66, "LNB", 5, 1, None, 15, .0110, []),
    ("D-1901", "F09", "B-1", "digester heating boiler", 22, "base", 0, .70, "LNB", 4, 2, 0, 9, .0072, []),
    ("D-1902", "F09", "B-2", "digester heating boiler", 22, "base", 0, .66, "LNB", 4, 2, 0, 9, .0072, []),
    ("D-2001", "F10", "B-1", "process steam boiler", 152, "can", 0, .82, "LNB", 8, 2, 1, 9, .0072, []),
    ("D-2002", "F10", "B-2", "process steam boiler", 152, "can", 0, .80, "LNB", 8, 2, 1, 9, .0072, []),
    ("D-2003", "F10", "B-3", "process steam boiler", 152, "can", 0, .81, "LNB", 8, 2, 1, 9, .0072, []),
    ("D-2004", "F10", "B-4", "process steam boiler", 152, "can", 0, .79, "LNB", 8, 2, 1, 9, .0072, []),
    ("D-2005", "F10", "B-5", "process steam boiler", 152, "can", 0, .80, "LNB", 8, 2, 1, 9, .0072, []),
    ("D-2006", "F10", "B-6", "process steam boiler", 152, "can", 0, .78, "LNB", 8, 2, 1, 9, .0072, []),
    ("D-2101", "F11", "B-1", "laundry steam boiler", 34, "week", 0, .78, "LNB", 11, 1, None, 9, .0072, []),
    ("D-2102", "F11", "B-2", "laundry steam boiler", 34, "week", 0, .76, "LNB", 11, 1, None, 9, .0072, []),
    ("D-2201", "F12", "B-1", "dryer steam boiler", 60, "almond", 0, .80, "LNB", 9, 2, 1, 9, .0072, []),
    ("D-2202", "F12", "B-2", "dryer steam boiler", 60, "almond", 0, .78, "LNB", 9, 2, 1, 9, .0072, []),
    ("D-2301", "F13", "B-1", "curing steam boiler", 34, "week", 0, .74, "LNB", 3, 1, None, 9, .0072, []),
    ("D-2302", "F13", "B-2", "curing steam boiler", 34, "week", 0, .72, "LNB", 3, 1, None, 9, .0072, []),
    ("D-2401", "F14", "B-1", "heating plant boiler", 44, "heat", 0, .70, "LNB", 10, 1, None, 9, .0072, []),
    ("D-2402", "F14", "B-2", "heating plant boiler", 44, "heat", 0, .68, "LNB", 10, 1, None, 9, .0072, []),
]
FIELDS = ("device", "facility", "unit", "desc", "rating", "profile", "monitored", "load", "control", "test_month",
          "cycle", "parity", "limit", "kind_level", "calendar")
UNIT = {u[0]: dict(zip(FIELDS, u)) for u in UNITS}
OPEN = [d for d, u in UNIT.items() if not u["monitored"]]
MONITORED = [d for d, u in UNIT.items() if u["monitored"]]


def _rng(k):
    return np.random.default_rng([SEED, k])


# ---------------------------------------------------------------- the gas utility's monthly heat content
UTILITY = "Tamsett Valley Gas"
W26 = [1.031, 1.027, 1.040, 1.061, 1.071, 1.058, 1.079, 1.087, 1.083, 1.074, 1.050, 1.037]
W27 = [1.033, 1.030]
# months the Westside gas sat lean or rich, as the plant's ethane contracts ran
FORCED = {(2019, 8): 1.031, (2021, 8): 1.029, (2023, 8): 1.034, (2025, 8): 1.032,
          (2018, 5): 1.061, (2019, 5): 1.066, (2020, 5): 1.058, (2021, 5): 1.069, (2022, 5): 1.063,
          (2023, 5): 1.060, (2024, 5): 1.067, (2025, 5): 1.064,
          (2018, 10): 1.064, (2019, 10): 1.070, (2020, 10): 1.061, (2021, 10): 1.066, (2022, 10): 1.072,
          (2023, 10): 1.063, (2024, 10): 1.068, (2025, 10): 1.065}


@functools.lru_cache(maxsize=None)
def heat_content():
    """{(area, year, month): therms a CCF}, January 2018 to February 2027."""
    rng = _rng(11)
    out = {}
    x = 1.046
    for y in range(2018, 2026):
        for m in range(1, 13):
            x = 1.046 + 0.55 * (x - 1.046) + rng.normal(0, 0.016)
            v = float(min(1.090, max(1.020, x)))
            if (y, m) in FORCED:
                v = FORCED[(y, m)]
                x = v
            out[("W", y, m)] = round(v, 3)
    for m in range(1, 13):
        out[("W", 2026, m)] = W26[m - 1]
    out[("W", 2027, 1)], out[("W", 2027, 2)] = W27
    e = _rng(12)
    for y in range(2018, 2028):
        for m in range(1, 13):
            if y == 2027 and m > 2:
                break
            out[("E", y, m)] = round(HREF + float(e.normal(0, 0.0015)), 3)
    return out


def hv(area, d):
    return heat_content()[(area, d.year, d.month)]


# ---------------------------------------------------------------- operation, rates, tests and the 2026 NOx
@functools.lru_cache(maxsize=None)
def run_hours(dev):
    """The unit's operating hours each day, 2018 to 2026: its profile's share of the month and a month-to-month swing."""
    u = UNIT[dev]
    rng = _rng(int(dev[2:]))
    prof = PROFILES[u["profile"]]
    swing = {(y, m): float(np.clip(rng.normal(1.0, 0.035), 0.88, 1.08)) for y in range(2018, 2027) for m in range(1, 13)}
    return {d: 24.0 * min(1.0, prof[d.month - 1] * swing[(d.year, d.month)]) for d in DAYS}


def heat_rate(dev):
    """MMBtu an operating hour (the rating at the unit's load)."""
    return UNIT[dev]["rating"] * UNIT[dev]["load"]


@functools.lru_cache(maxsize=None)
def level(dev):
    """The unit's own NOx rate (lb/MMBtu): an SCR unit's setpoint, a burner's rate on gas at HREF."""
    u = UNIT[dev]
    return u["kind_level"] * float(np.exp(_rng(1000 + int(dev[2:])).normal(0, LEVEL_SD)))


def rate(dev, d):
    """lb/MMBtu on day d: an SCR unit holds its level; a low-NOx burner follows its BTU area's heat content."""
    u = UNIT[dev]
    if u["control"] == "SCR":
        return level(dev)
    return level(dev) * float(np.exp(K_HV * (hv(AREA[u["facility"]], d) / HREF - 1.0)))


def test_dates(dev):
    """The unit's source test dates: its month in its cycle's years from 2018, a deferred test moved to its new date."""
    u = UNIT[dev]
    if u["monitored"]:
        return []
    out = []
    for y in range(2018, 2027):
        if u["cycle"] == 2 and y % 2 != u["parity"]:
            continue
        out.append(D(y, u["test_month"], 6 + (int(dev[2:]) * 7 + y) % 18))
    for ch in u["calendar"]:
        if ch[0] == "defer":
            out = [t for t in out if not (t.year == ch[1].year and t.month == ch[1].month)] + [ch[2]]
    return sorted(out)


TEST_DRAW = {"D-1801": 15, "D-1802": 15, "D-1803": 15}  # which draw of a unit's test scatter the world uses


@functools.lru_cache(maxsize=None)
def tests(dev):
    """Each test: date, the true rate that day and the rate the test measured (lb/MMBtu), the report's date."""
    rng = _rng(2000 + int(dev[2:]) + 100 * TEST_DRAW.get(dev, 0))
    fix = _rng(2500 + int(dev[2:]))
    out = []
    for t in test_dates(dev):
        true = rate(dev, t)
        meas = true * float(np.exp(rng.normal(0, TEST_SD)))
        out.append(dict(date=t, true=true, measured=meas, report=t + dt.timedelta(days=int(fix.integers(21, 36)))))
    return tuple(out)


def true_nox_2026(dev):
    """lb of NOx the unit emitted in 2026: each day's heat input times the day's rate."""
    hrs = run_hours(dev)
    hr = heat_rate(dev)
    return sum(hrs[d] * hr * rate(dev, d) for d in DAYS if d.year == YEAR)


SETPOINT_SUB = 1.10             # a SCR unit's substitute-data rate over its setpoint
PB1_SUB = 0.0098                # the power boiler's substitute-data rate, its lookback's 90th percentile


@functools.lru_cache(maxsize=None)
def cems_hours(dev):
    """A monitored unit's 2026 operating hours: (local standard datetime, operating time, heat input MMBtu, NOx
    lb/MMBtu, substitute flag). An SCR unit's startup hours run high until its catalyst reaches temperature."""
    u = UNIT[dev]
    rng = _rng(3000 + int(dev[2:]))
    prof = PROFILES[u["profile"]]
    out = []
    on = False
    for d in DAYS:
        if d.year != YEAR:
            continue
        share = prof[d.month - 1] * float(np.clip(rng.normal(1, .03), .85, 1.1))
        for hr in range(24):
            run = rng.random() < (share if not on else min(0.997, share + 0.08))
            if not run:
                on = False
                continue
            start = not on
            on = True
            hi = u["rating"] * u["load"] * float(np.clip(rng.normal(1, .05), .6, 1.08))
            r = rate(dev, d) * float(np.exp(rng.normal(0, .04)))
            if start and u["control"] == "SCR":
                r *= float(rng.uniform(2.5, 4.0))
                hi *= 0.6
            sub = rng.random() < 0.012
            if sub:
                r = level(dev) * SETPOINT_SUB if u["control"] == "SCR" else PB1_SUB
            out.append((dt.datetime(d.year, d.month, d.day, hr), 1.0, hi, r, sub))
    return tuple(out)


def unit_month_mmbtu(dev):
    """{(year, month): MMBtu} the unit burned: the monitor's hours in 2026 for a monitored unit, else its run hours."""
    out = {}
    if UNIT[dev]["monitored"]:
        hrs = run_hours(dev)
        hr = heat_rate(dev)
        for d in DAYS:
            if d.year < YEAR:
                out[(d.year, d.month)] = out.get((d.year, d.month), 0.0) + hrs[d] * hr
        for t, _, hi, _, _ in cems_hours(dev):
            out[(t.year, t.month)] = out.get((t.year, t.month), 0.0) + hi
        return out
    hrs = run_hours(dev)
    hr = heat_rate(dev)
    for d in DAYS:
        out[(d.year, d.month)] = out.get((d.year, d.month), 0.0) + hrs[d] * hr
    return out


# ---------------------------------------------------------------- the gas utility's meters and bills (ask A)
CONVERSION = D(2026, 7, 1)      # the new billing system: bills read on or after it carry therms
EXTRACT_BILLING = D(2027, 2, 8)
# facility: [(meter, account, read day of the month, share of the facility's gas)]; meters sharing an account are on
# combined billing
METERS = {
    "F01": [("TV-40118", "7701-2251", 4, .55), ("TV-40119", "7701-2251", 4, .45)],
    "F02": [("TV-31502", "7702-0864", 9, .48), ("TV-31503", "7702-0864", 9, .30), ("TV-31504", "7702-0866", 9, .22)],
    "F03": [("TV-22710", "7703-4410", 12, 1.0)],
    "F04": [("TV-09931", "7704-1187", 1, .62), ("TV-09932", "7704-1188", 1, .38)],
    "F05": [("TV-51207", "7705-3302", 6, 1.0)],
    "F06": [("TV-11846", "7706-0423", 21, .70), ("TV-11847", "7706-0423", 21, .30)],
    "F07": [("TV-38004", "7707-1950", 11, .58), ("TV-38005", "7707-1950", 11, .42)],
    "F08": [("TV-14422", "7708-6610", 25, 1.0)],
    "F09": [("TV-07715", "7709-0332", 18, 1.0)],
    "F10": [("TV-26651", "7710-2804", 3, .64), ("TV-26652", "7710-2804", 3, .36)],
    "F11": [("TV-45020", "7711-0019", 14, 1.0)],
    "F12": [("TV-19388", "7712-5126", 26, 1.0)],
    "F13": [("TV-19507", "7713-5130", 26, 1.0)],
    "F14": [("TV-30876", "7714-0691", 8, .60), ("TV-30877", "7714-0692", 8, .40)],
}
COMBINED = sorted({a for ms in METERS.values() for (_, a, _, _) in ms
                   if sum(1 for ms2 in METERS.values() for (_, a2, _, _) in ms2 if a2 == a) > 1})
# the gas each facility burns outside the plan's units (MMBtu a day, and its winter heating swing)
OTHER_GAS = {"F01": (60, .2), "F02": (420, .15), "F03": (140, .25), "F04": (40, .3), "F05": (60, .3), "F06": (55, .9),
             "F07": (180, .2), "F08": (95, 1.0), "F09": (7, .6), "F10": (40, .3), "F11": (12, .5), "F12": (16, .5),
             "F13": (22, .5), "F14": (30, .3)}
GAS_DRAW = {"F06": 3, "F10": 1, "F12": 1, "F14": 1}  # which draw of a facility's day-to-day gas the world uses
ESTIMATED = {("TV-09931", D(2026, 2, 2)), ("TV-19388", D(2026, 1, 26)), ("TV-45020", D(2026, 12, 14)),
             ("TV-30877", D(2026, 3, 9))}


def facility_gas(code):
    """MMBtu of utility gas the facility used each day from November 2025 to February 2027: its plan units plus
    everything else."""
    other, swing = OTHER_GAS[code]
    rng = _rng(4000 + int(code[1:]) + 100 * GAS_DRAW.get(code, 0))
    gas = {}
    for d in (D(2025, 11, 1) + dt.timedelta(days=i) for i in range((D(2027, 3, 2) - D(2025, 11, 1)).days)):
        heat = 1 + swing * max(0.0, np.cos(2 * np.pi * (d.timetuple().tm_yday - 15) / 365.0))
        gas[d] = other * heat * float(np.clip(rng.normal(1, .08), .7, 1.3))
    for dev, u in UNIT.items():
        if u["facility"] != code:
            continue
        hrs = run_hours(dev)
        hr = heat_rate(dev)
        cems = {}
        if u["monitored"]:
            for t, _, hi, _, _ in cems_hours(dev):
                cems[t.date()] = cems.get(t.date(), 0.0) + hi
        for d in gas:
            if d.year == YEAR:
                gas[d] += cems.get(d, 0.0) if u["monitored"] else hrs[d] * hr
            else:
                gas[d] += u["rating"] * u["load"] * 24 * PROFILES[u["profile"]][d.month - 1]
    return gas


def _read_days(mday):
    """The meter's read dates from November 2025 to January 2027: its day each month, off weekends and holidays."""
    out = []
    for y, m in [(2025, 11), (2025, 12)] + [(2026, k) for k in range(1, 13)] + [(2027, 1)]:
        d = D(y, m, min(mday, 28))
        while d.weekday() >= 5 or (d.month, d.day) in ((1, 1), (7, 3), (12, 25)):
            d += dt.timedelta(days=1)
        out.append(d)
    return out


def btu_factor(area, read_to):
    """The heat content a bill is priced at: the month its read closes."""
    return heat_content()[(area, read_to.year, read_to.month)]


@functools.lru_cache(maxsize=None)
def bills():
    """Every meter-period the utility billed from the November 2025 read on: (bill id, account, meter, read from, read
    to, BTU factor, corrected CCF, true therms, estimated, facility). The billing extract writes these (pack.py)."""
    out = []
    bid = 81320000
    for code, meters in METERS.items():
        gas = facility_gas(code)
        rng = _rng(5000 + int(code[1:]))
        for meter, acct, mday, share in meters:
            days = _read_days(mday)
            for a, b in zip(days[:-1], days[1:]):
                mmbtu = sum(gas.get(a + dt.timedelta(days=i), 0.0) for i in range((b - a).days)) * share
                btu = btu_factor(AREA[code], b)
                ccf = mmbtu * 10.0 / btu
                bid += int(rng.integers(3, 40))
                out.append(dict(bill=bid, account=acct, meter=meter, read_from=a, read_to=b, btu=btu,
                                ccf=int(round(ccf)), est=(meter, b) in ESTIMATED, facility=code))
    # the therms each billing period's account was billed: the old system priced corrected CCF at the period's BTU
    # factor; the new one bills whole therms on the account (a combined account's meters together)
    groups = {}
    for b in out:
        groups.setdefault((b["account"], b["read_to"]), []).append(b)
    for (acct, rt), g in groups.items():
        raw = sum(x["ccf"] for x in g) * g[0]["btu"]
        billed = raw if rt < CONVERSION else int(round(raw))
        for x in g:
            x["account_therms"] = billed
            x["therms"] = billed * x["ccf"] / sum(y["ccf"] for y in g)
    return tuple(out)


def spread_2026(read_from, read_to):
    """The share of a read period inside 2026, by days (the read-to day starts the next period)."""
    n = (read_to - read_from).days
    lo, hi = max(read_from, D(2026, 1, 1)), min(read_to, D(2027, 1, 1))
    return max(0, (hi - lo).days) / n


def gas_2026(code):
    """Ask A's truth: MMBtu Tamsett Valley Gas delivered to the facility in 2026, each bill's therms spread over its
    read period by days."""
    return sum(b["therms"] * spread_2026(b["read_from"], b["read_to"]) / 10.0 for b in bills() if b["facility"] == code)


# ---------------------------------------------------------------- emergency standby engines (ask B)
TIER_NOX = {"Tier 1": 6.9, "Tier 2": 4.8, "Tier 3": 3.0, "Tier 4 Final": 0.30}
ENGINE_LF = 0.74
G_LB = 453.6                    # grams a pound, as the district's guidance writes it
# device, facility, bhp, tier, make and model, installed, the bank it runs in parallel with (or None); a replacement in
# 2026: (date, old bhp, old tier, old model)
ENGINES = [
    ("D-3101", "F01", 1490, "Tier 2", "Caterpillar 3512B", D(2008, 5, 1), None, None),
    ("D-3201", "F02", 1110, "Tier 2", "Cummins QSK38-G4", D(2011, 9, 1), "A", None),
    ("D-3202", "F02", 1110, "Tier 2", "Cummins QSK38-G4", D(2011, 9, 1), "A", None),
    ("D-3301", "F03", 1340, "Tier 4 Final", "Caterpillar C32", D(2026, 8, 10), None,
     (D(2026, 8, 10), 1340, "Tier 2", "Caterpillar 3508B")),
    ("D-3401", "F04", 470, "Tier 3", "John Deere 6135HF485", D(2014, 3, 1), None, None),
    ("D-3402", "F04", 340, "Tier 2", "John Deere 6090HF485", D(2012, 5, 1), None, None),
    ("D-3501", "F05", 755, "Tier 2", "Cummins QSX15-G9", D(2010, 6, 1), None, None),
    ("D-3601", "F06", 2220, "Tier 2", "Caterpillar 3516B", D(2009, 7, 1), "A", None),
    ("D-3602", "F06", 2220, "Tier 2", "Caterpillar 3516B", D(2009, 7, 1), "A", None),
    ("D-3603", "F06", 470, "Tier 2", "Cummins QSL9-G", D(2012, 4, 1), None, None),
    ("D-3701", "F07", 1110, "Tier 2", "Cummins KTA38-G", D(2006, 11, 1), None, None),
    ("D-3801", "F08", 1490, "Tier 2", "Caterpillar 3512C", D(2013, 6, 1), "A", None),
    ("D-3802", "F08", 1490, "Tier 2", "Caterpillar 3512C", D(2013, 6, 1), "A", None),
    ("D-3803", "F08", 470, "Tier 3", "Cummins QSL9-G7", D(2015, 6, 1), None, None),
    ("D-3901", "F09", 1110, "Tier 2", "Caterpillar 3412C", D(2007, 2, 1), None, None),
    ("D-4001", "F10", 470, "Tier 4 Final", "Cummins QSL9-G", D(2026, 7, 6), None,
     (D(2026, 7, 6), 470, "Tier 1", "Cummins 6CTA8.3")),
    ("D-4002", "F10", 755, "Tier 2", "Cummins QSX15-G9", D(2011, 3, 1), None, None),
    ("D-4101", "F11", 470, "Tier 3", "Cummins QSL9-G7", D(2016, 1, 1), None, None),
    ("D-4201", "F12", 340, "Tier 2", "John Deere 6090HF485", D(2013, 6, 1), None, None),
    ("D-4202", "F12", 470, "Tier 3", "Cummins QSL9-G7", D(2017, 2, 1), None, None),
    ("D-4301", "F13", 340, "Tier 3", "Cummins QSB7-G", D(2015, 3, 1), None, None),
    ("D-4401", "F14", 3000, "Tier 2", "Caterpillar 3516C", D(2017, 10, 1), "A", None),
    ("D-4402", "F14", 3000, "Tier 2", "Caterpillar 3516C", D(2017, 10, 1), "A", None),
    ("D-4403", "F14", 1490, "Tier 2", "Caterpillar 3512C", D(2017, 10, 1), None, None),
]
ENGINE = {e[0]: dict(zip(("device", "facility", "bhp", "tier", "model", "installed", "bank", "replaced"), e))
          for e in ENGINES}
# power outages each facility's engines carried in 2026 (date, hours)
OUTAGES = {"F02": [(D(2026, 8, 19), 6.0)], "F06": [(D(2026, 1, 9), 3.0), (D(2026, 9, 2), 11.0)],
           "F08": [(D(2026, 9, 2), 10.0)], "F10": [(D(2026, 8, 19), 4.0)], "F12": [(D(2026, 9, 2), 14.0)],
           "F13": [(D(2026, 9, 2), 14.0)], "F14": [(D(2026, 3, 23), 2.0), (D(2026, 9, 2), 11.0)]}
# every facility keeps its Rule 4702 log in the District's e-logbook (since 2025), which records run time as hours and
# minutes: 0.30 is half an hour (pack.log_rows)


@functools.lru_cache(maxsize=None)
def engine_runs(dev):
    """The engine's 2026 runs: (date, hours, purpose). A readiness run of about half an hour each week and an hour or
    so on load each month, each a whole number of three-minute steps (its decimal hours exact to the hundredth), and
    the facility's outages."""
    e = ENGINE[dev]
    rng = _rng(6000 + int(dev[2:]))
    out = []
    d = D(2026, 1, 1) + dt.timedelta(days=int(rng.integers(0, 7)))
    while d.year == YEAR:
        if not (e["replaced"] and e["replaced"][0] - dt.timedelta(days=4) <= d <= e["replaced"][0]):
            out.append((d, 3 * int(rng.integers(8, 13)) / 60.0, "readiness"))
        d += dt.timedelta(days=7)
    for m in range(1, 13):
        day = D(YEAR, m, int(rng.integers(8, 23)))
        if not (e["replaced"] and e["replaced"][0] - dt.timedelta(days=4) <= day <= e["replaced"][0]):
            out.append((day, 3 * int(rng.integers(18, 29)) / 60.0, "load test"))
    for day, h in OUTAGES.get(e["facility"], []):
        out.append((day, h, "emergency"))
    return tuple(sorted(out))


@functools.lru_cache(maxsize=None)
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
                read = base + sum(h for x, h, _ in past)
            if d.year == 2027:
                read += float(rng.uniform(1.5, 4.0))
            out.append((dev, d, round(read, 1)))
    return tuple(out)


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
        if UNIT[dev]["monitored"]:
            ch = cems_hours(dev)
            units[dev] = dict(cems=ch, nox_2026=sum(round(hi * r, 2) for _, _, hi, r, _ in ch),
                              mmbtu=unit_month_mmbtu(dev))
        else:
            units[dev] = dict(tests=tests(dev), level=level(dev), nox_2026=true_nox_2026(dev),
                              mmbtu=unit_month_mmbtu(dev))
    fac = {}
    for dev, v in units.items():
        fac[UNIT[dev]["facility"]] = fac.get(UNIT[dev]["facility"], 0.0) + v["nox_2026"] / 2000.0
    return dict(units=units, facility_tons=fac, bills=bills(), gas_2026={c: gas_2026(c) for c in FAC_NAME},
                engine_lb={c: engine_nox_2026(c) for c in FAC_NAME}, inspections=inspections(),
                runs={dev: engine_runs(dev) for dev in ENGINE}, heat_content=heat_content())


if __name__ == "__main__":
    e = everything()
    for c, t in sorted(e["facility_tons"].items(), key=lambda x: -x[1]):
        print("%s %-34s %s %7.2f  gas %10.0f MMBtu  engines %7.0f lb" % (c, FAC_NAME[c], AREA[c], t, e["gas_2026"][c],
                                                                       e["engine_lb"][c]))

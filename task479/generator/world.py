"""The world of task479 (architecture 2): the Tarrowind Lodging Association's Lodging Monitor, a fixed panel of member
properties drawn in January 2018 that report rooms and room revenue every month, and the Tarrowind Department of
Revenue's taxable lodging receipts by county, published once a year about ten months after the tax year closes.

The panel takes no property opened since it was drawn, so the Department's receipts in a county are the panel's times a
ratio that moves at the pace hotels open (or non-member lodging closes) there. The ratio is linear in the year with a
small noise; 2025's ratio is the line carried one year past the last benchmark.

    x = build()    the truth: counties, properties, monthly reports, Department receipts, the devices"""
import calendar
import datetime as dt

import numpy as np

SEED = 4792
YEARS = list(range(2018, 2026))           # 2018 to 2025 complete in the panel
BENCH = list(range(2018, 2025))           # the Department has published 2018 to 2024
LAST = (2026, 8)                          # the last month every panel property has reported by the extract
THRESHOLD = 0.06                          # the Rising Destinations growth floor, 2024 to 2025
FUND = 1_800_000

# name, county code, kind, panel properties, ratio in 2018, drift (ratio change 2024 to 2025 over 2024), panel growth
# 2023 to 2024, panel growth 2024 to 2025
COUNTIES = [
    ("Arvenne", "03", "urban", 46, 1.42, 0.005, 0.061, 0.085),
    ("Brisholt", "07", "beach", 34, 1.65, 0.010, 0.048, 0.072),
    ("Corrigan Bay", "11", "beach", 28, 2.05, -0.025, 0.092, 0.068),
    ("Delvane", "15", "mountain", 24, 1.88, -0.020, 0.071, 0.062),
    ("Elsmoor", "19", "beach", 19, 1.36, 0.065, -0.021, 0.034),
    ("Fallowmere", "23", "mountain", 14, 1.30, 0.080, 0.012, 0.026),
    ("Grindell", "27", "rural", 16, 1.74, 0.044, 0.018, 0.042),
    ("Hollin Ridge", "31", "mountain", 21, 1.95, 0.002, 0.044, 0.048),
    ("Isterhaven", "35", "urban", 38, 1.51, 0.010, 0.037, 0.040),
    ("Jorvale", "39", "rural", 12, 2.22, 0.020, 0.025, 0.010),
    ("Kestholm", "43", "urban", 31, 1.58, 0.000, 0.052, 0.040),
    ("Larrowby", "47", "rural", 13, 2.31, 0.015, 0.009, 0.024),
    ("Marrowfield", "51", "rural", 10, 2.48, 0.025, 0.014, -0.005),
    ("Nethervane", "55", "beach", 22, 1.83, -0.008, 0.066, 0.058),
    ("Orrin Falls", "59", "mountain", 15, 1.69, 0.030, 0.031, 0.008),
    ("Pellow Sound", "63", "beach", 26, 1.77, -0.002, 0.059, 0.053),
]
NAMES = [c[0] for c in COUNTIES]
CODE = {c[0]: c[1] for c in COUNTIES}

# the panel's statewide path before 2023 (2018 = 1): 2020 is the pandemic year
PATH = {2018: 1.0, 2019: 1.052, 2020: 0.61, 2021: 0.93, 2022: 1.12, 2023: 1.17}
SEASON = {   # occupancy multipliers by month
    "beach": [0.55, 0.62, 0.78, 0.86, 1.02, 1.28, 1.45, 1.42, 1.08, 0.88, 0.62, 0.58],
    "mountain": [1.12, 1.18, 0.98, 0.70, 0.74, 1.02, 1.28, 1.25, 1.06, 1.10, 0.74, 1.00],
    "urban": [0.84, 0.92, 1.02, 1.04, 1.06, 1.08, 1.02, 1.04, 1.06, 1.08, 0.96, 0.80],
    "rural": [0.78, 0.82, 0.92, 0.98, 1.06, 1.14, 1.20, 1.18, 1.06, 1.02, 0.88, 0.82],
}
COVID = {(2020, m): f for m, f in zip(range(3, 13), [0.72, 0.18, 0.28, 0.48, 0.62, 0.64, 0.58, 0.55, 0.46, 0.44])}
COVID.update({(2021, 1): 0.62, (2021, 2): 0.70, (2021, 3): 0.82, (2021, 4): 0.88})
ADR = {"beach": 168.0, "mountain": 182.0, "urban": 149.0, "rural": 112.0}

MGMT_COUNTY = "Arvenne"          # Harbor & Pine Hospitality's office county, under which its portal files from April 2026
MGMT_TAKEOVER = (2026, 4)


def months(y0=2018, m0=1, y1=LAST[0], m1=LAST[1]):
    y, m = y0, m0
    while (y, m) <= (y1, m1):
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def ratio_line(name):
    """The Department's receipts over the panel's: linear in the year, r(2018) = a, r(2025) / r(2024) = 1 + d."""
    c = COUNTIES[NAMES.index(name)]
    a, d = c[4], c[5]
    b = d * a / (1 - 6 * d)
    return a, b


def build():
    rng = np.random.default_rng(SEED)
    props = []
    pid = 0
    for name, code, kind, n, *_ in COUNTIES:
        for i in range(int(round(n * 1.55))):
            pid += 1
            rooms = int(np.clip(rng.lognormal(np.log(95 if kind != "urban" else 150), 0.55), 18, 420))
            props.append({
                "k": pid, "county": name, "kind": kind, "rooms": rooms,
                "adr": ADR[kind] * float(np.exp(rng.normal(0, 0.22))),
                "occ": float(np.clip(rng.normal(0.64, 0.07), 0.42, 0.82)),
                "close": None, "shock": rng.normal(0, 0.015, 12 * 9 + 12),
            })
    # closures: the panel loses properties through 2018 to 2022, most of them in the pandemic year
    for p in props:
        u = rng.random()
        if u < 0.015:
            p["close"] = (2018 + int(rng.integers(0, 2)), int(rng.integers(1, 13)))
        elif u < 0.085:
            p["close"] = (2020, int(rng.integers(4, 13)))
        elif u < 0.11:
            p["close"] = (2021 + int(rng.integers(0, 2)), int(rng.integers(1, 13)))
    # a few properties change their room count (renovations, a wing closed or added) after 2019
    for p in props:
        p["rooms_path"] = {}
        if rng.random() < 0.16:
            when = (int(rng.integers(2019, 2025)), int(rng.integers(1, 13)))
            p["rooms_path"] = {"from": when, "rooms": max(12, p["rooms"] + int(rng.integers(-30, 60)))}

    # the properties the 2022 crosswalk will miss: rebranded at the system change, and renovated since
    rng2 = np.random.default_rng(SEED + 5)
    gap = set()
    for c in NAMES:
        if c in ("Arvenne", "Kestholm", "Orrin Falls"):
            continue
        cand = [p for p in props if p["county"] == c and p["close"] is None]
        p = cand[int(rng2.integers(0, len(cand)))]
        p["rooms_path"] = {"from": (int(rng2.integers(2023, 2025)), int(rng2.integers(1, 13))),
                           "rooms": p["rooms"] + int(rng2.integers(18, 64))}
        gap.add(p["k"])

    # county growth: the statewide path to 2023, then each county's own 2024 and 2025 growth, 2026 flat-ish
    level = {}
    for name, code, kind, n, a, d, g24, g25 in COUNTIES:
        tilt = rng.normal(0, 0.03)
        lv = {y: PATH[y] * (1 + tilt * (y - 2018) / 5) for y in range(2018, 2024)}
        lv[2024] = lv[2023] * (1 + g24)
        lv[2025] = lv[2024] * (1 + g25)
        lv[2026] = lv[2025] * (1 + rng.normal(0.02, 0.012))
        level[name] = lv

    def active(p, y, m):
        return p["close"] is None or (y, m) < p["close"]

    def rooms_at(p, y, m):
        rp = p["rooms_path"]
        return rp["rooms"] if rp and (y, m) >= rp["from"] else p["rooms"]

    # monthly reports (truth, before any export mess); a smooth month factor interpolates the county's annual level
    rep = []
    for p in props:
        lv = level[p["county"]]
        for j, (y, m) in enumerate(months()):
            if not active(p, y, m):
                continue
            t = y + (m - 0.5) / 12
            y0 = int(np.floor(t - 0.5))
            w = t - 0.5 - y0
            g = lv.get(y0, lv[min(lv)]) * (1 - w) + lv.get(y0 + 1, lv[max(lv)]) * w if y0 >= 2018 else lv[2018]
            if y0 + 1 > 2026:
                g = lv[2026]
            cov = COVID.get((y, m), 1.0)
            days = calendar.monthrange(y, m)[1]
            rooms = rooms_at(p, y, m)
            avail = rooms * days
            occ = min(0.97, p["occ"] * SEASON[p["kind"]][m - 1] * (0.55 + 0.45 * g) * cov * np.exp(p["shock"][j]))
            sold = int(round(avail * occ))
            adr = p["adr"] * (0.6 + 0.4 * g) * (1.0 + 0.08 * (SEASON[p["kind"]][m - 1] - 1)) * (0.85 + 0.15 * cov)
            adr *= float(np.exp(rng.normal(0, 0.01)))
            rep.append({"k": p["k"], "county": p["county"], "y": y, "m": m, "avail": avail, "sold": sold,
                        "rev": round(sold * adr, 2)})
    x = {"props": props, "rep": rep, "level": level, "xwalk_gap": gap}
    _hit_growth(x)
    _benchmarks(x, rng)
    _devices(x, rng)
    return x


def panel_totals(rep):
    t = {}
    for r in rep:
        t[(r["county"], r["y"])] = t.get((r["county"], r["y"]), 0.0) + r["rev"]
    return t


def _hit_growth(x):
    """Scale each county's 2024 and 2025 months so the panel's annual growth is the designed one exactly (to a
    hundredth of a point), the months keeping their own pattern."""
    for name, code, kind, n, a, d, g24, g25 in COUNTIES:
        for y, g in ((2024, g24), (2025, g25)):
            t = panel_totals(x["rep"])
            f = t[(name, y - 1)] * (1 + g) / t[(name, y)]
            for r in x["rep"]:
                if r["county"] == name and r["y"] >= y:
                    r["rev"] = round(r["rev"] * f, 2)
    t = panel_totals(x["rep"])
    x["panel"] = t


def _benchmarks(x, rng):
    """The Department's receipts: the panel's times the county's ratio line, with a small noise; the first print
    of each year, and the revision the next year's report makes to it (amended returns, a few tenths of a per cent
    at most). 2025 is the truth the Department will first print, kept for checks only."""
    first, revised, ratio = {}, {}, {}
    for name in NAMES:
        a, b = ratio_line(name)
        for y in YEARS:
            r = a + b * (y - 2018)
            if y in BENCH:
                r *= 1 + float(rng.normal(0, 0.0006))
            ratio[(name, y)] = r
            first[(name, y)] = int(round(x["panel"][(name, y)] * r))
        for y in BENCH:
            if y + 1 in BENCH or y + 1 == 2025:
                rv = float(abs(rng.normal(0, 0.0012))) if rng.random() < 0.6 else 0.0
                revised[(name, y)] = int(round(first[(name, y)] * (1 + rv)))
    x["first"], x["revised"], x["ratio"] = first, revised, ratio


def _devices(x, rng):
    """Layer 1 mess and the asks' devices, recorded on the truth so the pack writer and the checks share them.

    renumber: the 2022 property-management-system change gave every property a new id; the crosswalk the vendor
        delivered misses some of them (the Ask B device), which the property register and the reports' own rooms
        and names tie back.
    resubmit: late and revised monthly reports, the later submission superseding the earlier.
    transfer: from April 2026 Harbor & Pine's portal account files its properties under its own office county
        (the Ask A device); the property register keeps each property's county."""
    props = x["props"]
    order = rng.permutation(len(props))
    for i, j in enumerate(order):
        props[j]["new_id"] = "P-%05d" % (30117 + 37 * i)
        props[j]["old_id"] = "L-%04d" % (1000 + int(props[j]["k"]) * 3 + int(rng.integers(0, 3)))
    live22 = [p for p in props if p["close"] is None or p["close"] > (2022, 3)]
    # Harbor & Pine: three properties in each of twelve counties besides its own, taken over in April 2026, none of
    # them closed and none a crosswalk gap
    hp = []
    for c in NAMES:
        if c in (MGMT_COUNTY, "Jorvale", "Marrowfield", "Larrowby"):
            continue
        cand = [p for p in live22 if p["county"] == c and p["k"] not in x["xwalk_gap"] and p["close"] is None]
        idx = rng.permutation(len(cand))[:3]
        hp += [cand[i]["k"] for i in idx]
    x["mgmt"] = set(hp)
    # resubmissions: about one report in forty is revised (revenue and rooms sold restated), a few sent twice
    x["resub"] = {}
    for r in x["rep"]:
        u = rng.random()
        if u < 0.022:
            x["resub"][(r["k"], r["y"], r["m"])] = ("revised", float(rng.normal(0.0, 0.06)))
        elif u < 0.030:
            x["resub"][(r["k"], r["y"], r["m"])] = ("repeat", 0.0)


def submitted_report(r, kind, f):
    """The first submission of a report later revised: what the property first sent."""
    if kind != "revised":
        return dict(r)
    s = dict(r)
    s["rev"] = round(r["rev"] / (1 + f), 2)
    s["sold"] = int(round(r["sold"] / (1 + f * 0.6)))
    s["sold"] = min(s["sold"], r["avail"])
    return s


def month_end(y, m):
    return dt.date(y, m, calendar.monthrange(y, m)[1])

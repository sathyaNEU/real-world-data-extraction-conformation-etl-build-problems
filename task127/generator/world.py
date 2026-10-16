"""The county's hospital discharges (adults aged 65 and over, December 2024 to September 2026), each pathway-1 patient's
home district and GP registration, the home-care start the council's brokerage arranged and the community equipment the
equipment service delivered; a discharge happens on the day the last of medical optimisation, equipment and home care
is in place."""
import datetime as dt
import math
import statistics

import numpy as np

import core

SEED = 127
_ND = statistics.NormalDist()


def skewed(u, median, sigma):
    """A wait drawn from a right-skewed (lognormal) distribution by its quantile at the uniform draw u, so most waits
    sit near the median and a few run to several times it."""
    u = min(max(u, 1e-6), 1 - 1e-6)
    return median * math.exp(sigma * _ND.inv_cdf(u))


def rng_for(*keys):
    return np.random.default_rng([SEED] + [abs(hash_str(k)) % (2 ** 31) for k in keys])


def hash_str(s):
    h = 2166136261
    for ch in str(s).encode():
        h = ((h ^ ch) * 16777619) % (2 ** 32)
    return h


# discharges a day, adults 65 and over, by pathway (0 home, 1 home with care, 2 rehab bed, 3 care home)
VOLUME = {"RMC01": 31.0, "RMC02": 19.0, "RSM01": 18.0, "RSM02": 14.5, "RSM03": 16.5}
P1_SHARE = {"RMC01": 0.330, "RMC02": 0.330, "RSM01": 0.370, "RSM02": 0.340, "RSM03": 0.345}
P23_SHARE = (0.075, 0.055)
# where pathway-1 patients live (district, or the neighbouring county) by hospital
HOME = {"RMC01": {"Marchford": 0.90, "Ashby": 0.06, "Teme Valley": 0.03, "Severnside": 0.01},
        "RMC02": {"Marchford": 0.58, "Ashby": 0.02, "Teme Valley": 0.38, "Severnside": 0.02},
        "RSM01": {"Marchford": 0.03, "Ashby": 0.84, "Teme Valley": 0.11, "Severnside": 0.02},
        "RSM02": {"Marchford": 0.02, "Ashby": 0.47, "Teme Valley": 0.49, "Severnside": 0.02},
        "RSM03": {"Marchford": 0.01, "Ashby": 0.02, "Teme Valley": 0.36, "Severnside": 0.61}}
# home care already in place to start on the day of optimisation (a restarted package), by district
IN_PLACE = {"Marchford": 0.47, "Ashby": 0.37, "Teme Valley": 0.41, "Severnside": 0.40}
# days from optimisation to home care starting, for those who wait, by district: the winter median and the spread of
# a right-skewed wait
CARE_WAIT = {"Marchford": (6.1, 0.45), "Ashby": (8.4, 0.42), "Teme Valley": (6.4, 0.45), "Severnside": (5.8, 0.5)}
# the north Teme Valley zone round Holmford has the council's newest block contract, so its waits are shorter
CARE_WAIT_SITE = {("RSM03", "Teme Valley"): (4.9, 0.42)}
# share of pathway-1 patients needing community equipment delivered before they can go home, by hospital
EQUIP_NEED = {"RMC01": 0.21, "RMC02": 0.65, "RSM01": 0.78, "RSM02": 0.58, "RSM03": 0.12}
# days from optimisation to the equipment's delivery, by depot: the winter median, the spread and the shortest
EQUIP_LAG = {"North": (1.3, 0.6, 0), "South": (9.6, 0.3, 3)}
RESTART_EQUIP = 0.15
WARM_UP = 75
# the week: the equipment depots run a small Saturday round and no Sunday deliveries; framework providers start
# fewer new packages at the weekend; care homes and rehabilitation units take fewer admissions then; wards send
# fewer patients home. Each pair is the chance that something that would fall on a Saturday, or a Sunday, is
# booked for another day instead.
DEPOT_WEEKEND = (0.75, 1.0)
CARE_WEEKEND = (0.55, 0.8)
BED_WEEKEND = (0.45, 0.6)
HOME_WEEKEND = (0.2, 0.3)


def rebook(day0, wait, redraw, chance, rng, tries=8):
    """The wait from day0, drawn again (from the service's own spread of waits) while it would end on a weekend day
    the service turns down; a service that is turned down every time keeps its last draw."""
    for _ in range(tries):
        wd = (day0 + dt.timedelta(wait)).weekday()
        if wd < 5 or rng.random() >= chance[wd - 5]:
            return wait
        wait = redraw(rng)
    return wait


def weekend_hold(day, chance, rng):
    """Days a patient going home waits when the ward does not send them on the weekend day."""
    wd = day.weekday()
    if wd == 5 and rng.random() < chance[0]:
        return 2 if rng.random() < 0.65 else 3
    if wd == 6 and rng.random() < chance[1]:
        return 1 if rng.random() < 0.65 else 2
    return 0


def winter_factor(d):
    """Care and equipment waits stretch in winter; volumes rise."""
    m = d.month
    return {12: 1.0, 1: 1.0, 2: 1.0, 11: 0.7, 3: 0.75}.get(m, 0.5)


def stays():
    """Every discharge of an adult aged 65 and over, with its dependencies for pathway 1."""
    out = []
    d = core.REC0 - dt.timedelta(WARM_UP)       # patients optimised before the extract who leave inside it
    while d <= core.REC1:
        for site in core.SITES:
            r = rng_for("day", site, d.isoformat())
            vol = VOLUME[site] * (1.08 if d.month in (12, 1, 2) else 1.0) * (0.86 if d.weekday() >= 5 else 1.0)
            n = int(r.poisson(vol))
            for k in range(n):
                rr = rng_for("stay", site, d.isoformat(), k)
                u = rr.random()
                pw = 1 if u < P1_SHARE[site] else (2 if u < P1_SHARE[site] + P23_SHARE[0] else
                                                  (3 if u < P1_SHARE[site] + sum(P23_SHARE) else 0))
                s = dict(site=site, mofd=d, pathway=pw, key=(site, d.isoformat(), k))
                s["age"] = int(65 + min(34, rr.gamma(2.2, 6.5)))
                s["los_pre"] = int(1 + rr.gamma(1.6, 3.2))
                if pw == 1:
                    homes = HOME[site]
                    s["home"] = list(homes)[int(rr.choice(len(homes), p=list(homes.values())))]
                    wf = winter_factor(d)
                    if rr.random() < IN_PLACE[s["home"]] + (1 - wf) * 0.25:
                        s["care_wait"] = -int(rr.integers(0, 6))          # in place: started on or before the day
                    else:
                        med, sg = CARE_WAIT_SITE.get((site, s["home"]), CARE_WAIT[s["home"]])
                        s["care_wait"] = max(1, int(round(skewed(rr.random(), med, sg) * (0.55 + 0.45 * wf))))
                    # people whose care package restarts mostly have their equipment at home already
                    if rr.random() < EQUIP_NEED[site] * (RESTART_EQUIP if s["care_wait"] <= 0 else 1.0):
                        med, sg, lo = EQUIP_LAG[core.HOSPITALS[site]["depot"]]
                        s["equip_lag"] = max(lo, int(round(skewed(rr.random(), med, sg) * (0.6 + 0.4 * wf))))
                    else:
                        s["equip_lag"] = None
                    rw = rng_for("week", *s["key"])
                    if s["care_wait"] > 0:
                        med, sg = CARE_WAIT_SITE.get((site, s["home"]), CARE_WAIT[s["home"]])
                        f = 0.55 + 0.45 * wf
                        s["care_wait"] = rebook(d, s["care_wait"], lambda g: max(1, int(round(skewed(g.random(), med, sg)
                                                                                           * f))), CARE_WEEKEND, rw)
                    if s["equip_lag"] is not None:
                        med, sg, lo = EQUIP_LAG[core.HOSPITALS[site]["depot"]]
                        f = 0.6 + 0.4 * wf
                        s["equip_lag"] = rebook(d, s["equip_lag"], lambda g: max(lo, int(round(skewed(g.random(), med, sg)
                                                                                             * f))), DEPOT_WEEKEND, rw)
                    s["delay"] = max(0, s["care_wait"], s["equip_lag"] or 0)
                elif pw in (2, 3):
                    sc = 4.0 if pw == 2 else 6.5
                    s["delay"] = rebook(d, int(rr.gamma(1.4, sc)), lambda g: int(g.gamma(1.4, sc)), BED_WEEKEND,
                                        rng_for("week", *s["key"]))
                else:
                    s["delay"] = 0 if rr.random() < 0.9 else 1
                    s["delay"] += weekend_hold(d + dt.timedelta(s["delay"]), HOME_WEEKEND, rng_for("week", *s["key"]))
                out.append(s)
        d += dt.timedelta(1)
    return out


# ----------------------------------------------------------------------------------------------------------------
# people: NHS numbers, hospital numbers, GP practices and home postcodes

PRACTICES = {  # code: (name, ICB, area)
    "M81001": ("Castle Street Surgery", "Marchshire", "Marchford"), "M81002": ("Bridge Medical Centre", "Marchshire", "Marchford"),
    "M81004": ("Riverside Health Centre", "Marchshire", "Marchford"), "M81007": ("Kingsway Medical Practice", "Marchshire", "Marchford"),
    "M81009": ("St Anne's Surgery", "Marchshire", "Marchford"), "M81012": ("Old Mill Surgery", "Marchshire", "Marchford"),
    "M81015": ("Ashby Market Surgery", "Marchshire", "Ashby"), "M81016": ("Vale View Practice", "Marchshire", "Ashby"),
    "M81018": ("Hollins Lane Surgery", "Marchshire", "Ashby"), "M81021": ("Ashby West Medical Centre", "Marchshire", "Ashby"),
    "M81023": ("Teme Bridge Surgery", "Marchshire", "Teme Valley"), "M81025": ("Clun Road Practice", "Marchshire", "Teme Valley"),
    "M81026": ("Leintwardine Surgery", "Marchshire", "Teme Valley"), "M81028": ("Holmford Medical Group", "Marchshire", "Teme Valley"),
    "N83002": ("Severn Quay Surgery", "Severnside", "Severnside"), "N83005": ("Pool Quay Medical Practice", "Severnside", "Severnside"),
    "N83006": ("Welshpool Road Surgery", "Severnside", "Severnside"), "N83009": ("Kerry Lane Practice", "Severnside", "Severnside"),
}
# practices that merged in 2025: the retired code, its name, the successor and the date of the merger
MERGED = {"M81003": ("Northgate Surgery", "M81002", dt.date(2025, 4, 1)),
          "M81019": ("Market Hall Practice", "M81018", dt.date(2025, 7, 1)),
          "M81027": ("Brampton Bryan Surgery", "M81026", dt.date(2025, 10, 1))}
ICB_NAME = {"Marchshire": "NHS Marchshire Integrated Care Board", "Severnside": "NHS Severnside Integrated Care Board"}

# postcode districts (outward codes); SV7 straddles the county line, part Teme Valley and part Severnside
OUTWARD = {"Marchford": ["MF1", "MF2", "MF3", "MF4", "MF5"], "Ashby": ["AV6", "AV7", "AV8"],
           "Teme Valley": ["TV9", "TV10", "TV11", "SV7"], "Severnside": ["SV7", "SV21", "SV22"]}
WARDS_ELECT = {"MF1": "Castle", "MF2": "Bridge", "MF3": "Northgate", "MF4": "Riverside", "MF5": "St Anne's",
               "AV6": "Ashby Market", "AV7": "Vale View", "AV8": "Hollins", "TV9": "Teme Bridge", "TV10": "Clun Road",
               "TV11": "Leintwardine", "SV7": "Bucknell and Brampton"}
_LETTERS = "ABDEFGHJLNPQRSTUWXYZ"


def postcodes():
    """Each district's unit postcodes; a cross-border outward code has its own units on each side."""
    out = {}
    for district, outs in OUTWARD.items():
        units = []
        for o in outs:
            r = rng_for("pc", district, o)
            n = 70 if o != "SV7" else 22
            seen = set()
            while len(seen) < n:
                u = "%d%s%s" % (int(r.integers(0, 10)), _LETTERS[int(r.integers(20))], _LETTERS[int(r.integers(20))])
                seen.add(u)
            units += ["%s %s" % (o, u) for u in sorted(seen)]
        out[district] = units
    # the two sides of SV7 never share a unit postcode
    a = {p for p in out["Teme Valley"] if p.startswith("SV7")}
    b = {p for p in out["Severnside"] if p.startswith("SV7")}
    out["Severnside"] = [p for p in out["Severnside"] if p not in a]
    return out


POSTCODES = postcodes()


def lookup_postcodes():
    """The council's lookup lists every unit postcode in its districts, including the many no referral or patient
    record in the pack carries; a unit on the Severnside side of SV7 is never listed."""
    taken = {p for units in POSTCODES.values() for p in units}
    out = {}
    for district in ("Marchford", "Ashby", "Teme Valley"):
        units = list(POSTCODES[district])
        for o in OUTWARD[district]:
            r = rng_for("pc-lookup", district, o)
            extra = int(r.integers(5, 64)) if o != "SV7" else int(r.integers(2, 9))
            have = {p for p in taken if p.split()[0] == o}
            add = set()
            while len(add) < extra:
                u = "%s %d%s%s" % (o, int(r.integers(0, 10)), _LETTERS[int(r.integers(20))], _LETTERS[int(r.integers(20))])
                if u not in have:
                    add.add(u)
            units += sorted(add)
        out[district] = units
    return out


def nhs_number(rng):
    """A ten-digit number that passes the Modulus 11 check."""
    while True:
        d = [int(x) for x in rng.integers(0, 10, 9)]
        d[0] = 4 + int(rng.integers(0, 3))
        tot = sum(v * (10 - i) for i, v in enumerate(d))
        chk = 11 - tot % 11
        if chk == 11:
            chk = 0
        if chk == 10:
            continue
        return "".join(map(str, d)) + str(chk)


def practice_for(home, rng):
    codes = [c for c, v in PRACTICES.items() if v[2] == home]
    c = codes[int(rng.integers(len(codes)))]
    # a few patients still carry the code of a practice that merged in 2025
    for old, (name, new, when) in MERGED.items():
        if new == c and rng.random() < 0.25:
            return old
    return c

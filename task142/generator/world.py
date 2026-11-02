"""The clean truth of the task142 world (architecture 3), before any export mess or document is written.

Veenhaven-Noord has four neighbourhoods; Molenwijk and Rietveld form the catchment of Basisschool De Kwikstaart.
Rietveld is an estate whose families moved in from 2017 to 2019: their first children entered the school from 2023 to
2025, and their second children turn four from 2027. A catchment child whose older brother or sister is on the
school's roll when the child first counts enters De Kwikstaart far more often than one without, and the share of the
coming cohorts with such a sibling is about twice the share in the last five intakes. Everything is generated forward
from a fixed seed; the only fitted parameter is the building's capacity (tune())."""
import datetime as dt
import math

import numpy as np

import params as P

D = dt.date
TD = dt.timedelta

STREETS = {
    "Molenwijk": ["Molenstraat", "Korenmolen", "Wipmolen", "Standerdmolen", "Molenwiek", "Watermolen", "Zaagmolen",
                  "Oliemolen", "Poldermolen", "Stellingmolen", "Bovenkruier", "Molensloot"],
    "Rietveld": ["Rietzoom", "Lisdodde", "Biezenweg", "Rietpluim", "Waterlelie", "Kroosweg", "Zwanebloem",
                 "Rietgors", "Oeverzegge", "Rietkraag"],
    "De Akkers": ["Akkerweg", "Tarweveld", "Gerstakker", "Haverakker", "Rogge", "Klaverakker", "Vlasakker",
                  "Akkerrand", "Bouwakker", "Esakker", "Kampweg", "Hoeveweg"],
    "Noorderpark": ["Parkweg", "Noorderhof", "Lindenpark", "Beukenlaan", "Eikenpark", "Esdoornhof", "Iepenpark",
                    "Kastanjelaan", "Platanenhof", "Wilgenpark", "Populierpark", "Elzenhof"],
}
N_HH = {"Molenwijk": (820, 2150), "Rietveld": (590, 480), "De Akkers": (1260, 2950), "Noorderpark": (1180, 3100)}
P_SIB = 0.93                       # enters when an older sibling is on the roll at the child's first count
P_NOSIB = {"Molenwijk": 0.30, "Rietveld": 0.47}
P_OUT = 0.022                      # children outside the catchment


def cohort(b):
    """The 1 October count at which a child born on b first counts (aged four on that date)."""
    y = b.year + 4
    return y if (b.month, b.day) <= (10, 1) else y + 1


def rdate(rng, y0, y1, m0=1, m1=12):
    a, b = D(y0, m0, 1).toordinal(), D(y1, m1, 28).toordinal()
    return D.fromordinal(int(rng.integers(a, b + 1)))


def population(rng):
    """Households and persons of the district with their residence periods (truth)."""
    persons, hhs = [], []
    used_addr = set()
    pid_pool = rng.choice(np.arange(10_000_000, 99_999_999), size=40000, replace=False)
    hid_pool = rng.choice(np.arange(1_000_000, 9_999_999), size=15000, replace=False)
    pi = hi = 0
    for wijk, (n_fam, n_oth) in N_HH.items():
        pc = P.WIJKEN[wijk]
        streets = STREETS[wijk]
        for k in range(n_fam + n_oth):
            fam = k < n_fam
            while True:
                st = streets[int(rng.integers(len(streets)))]
                nr = int(rng.integers(1, 180))
                add = "" if rng.random() > 0.12 else str(rng.choice(["A", "B", "C", "1", "2"]))
                if (st, nr, add) not in used_addr:
                    used_addr.add((st, nr, add))
                    break
            letters = "ABCDEFGHJKLMNPRSTVWXZ"
            postcode = "%s %s%s" % (pc, letters[(nr // 7 + len(st)) % 21], letters[(nr * 3 + len(st)) % 21])
            hid = "H%07d" % int(hid_pool[hi]); hi += 1
            if wijk == "Rietveld" and fam:
                since = rdate(rng, 2017, 2019, 3, 12)
            else:
                since = rdate(rng, 1985, 2020) if rng.random() < 0.85 else rdate(rng, 2021, 2026, 1, 6)
            leave = None
            if since < D(2025, 1, 1) and rng.random() < (0.035 if wijk != "Rietveld" else 0.02) * 6:
                leave = rdate(rng, 2021, 2026, 1, 8)
                if leave <= since:
                    leave = None
            hh = {"hid": hid, "wijk": wijk, "street": st, "nr": nr, "add": add, "postcode": postcode, "since": since,
                  "leave": leave, "members": []}
            adults = 2 if (fam and rng.random() < 0.8) or (not fam and rng.random() < 0.4) else 1
            ab = rdate(rng, 1950, 1996) if not fam else rdate(rng, 1975, 1994)
            for a in range(adults):
                b = ab + TD(days=int(rng.integers(-900, 900)))
                persons.append({"pid": "%08d" % int(pid_pool[pi]), "hh": hh, "birth": b, "sex": str(rng.choice(["M", "V"])),
                                "child": False}); pi += 1
                hh["members"].append(persons[-1])
            if fam:
                if wijk == "Rietveld":
                    r = rng.random()
                    if r < 0.64:
                        b0 = rdate(rng, 2019, 2021)
                    elif r < 0.82:
                        b0 = rdate(rng, 2013, 2018)
                    elif r < 0.90:
                        b0 = rdate(rng, 2022, 2024)
                    else:
                        b0 = None
                    kids = []
                    if b0:
                        kids.append(b0)
                        if b0.year <= 2022 and rng.random() < 0.84:
                            kids.append(b0 + TD(days=int(rng.integers(1250, 1700))))
                        if b0.year <= 2016 and rng.random() < 0.3:
                            kids.append(b0 + TD(days=int(rng.integers(700, 1500))))
                else:
                    b0 = rdate(rng, 2004, 2024)
                    n = int(rng.choice([1, 2, 3], p=[0.36, 0.47, 0.17]))
                    kids = [b0]
                    for j in range(n - 1):
                        kids.append(kids[-1] + TD(days=int(rng.integers(540, 1500))))
                for b in kids:
                    if b > D(2026, 9, 30) or (leave and b > leave):
                        continue
                    persons.append({"pid": "%08d" % int(pid_pool[pi]), "hh": hh, "birth": b,
                                    "sex": str(rng.choice(["M", "V"])), "child": True}); pi += 1
                    hh["members"].append(persons[-1])
            hhs.append(hh)
    return persons, hhs


def lives_in(p, day):
    hh = p["hh"]
    start = max(hh["since"], p["birth"])
    return start <= day and (hh["leave"] is None or day < hh["leave"])


def simulate_school(rng, persons):
    """Each child who first counts while living in the district enters De Kwikstaart or not; the roll at each
    1 October count from 2014 to 2026 follows."""
    kids = sorted([p for p in persons if p["child"]], key=lambda p: p["birth"])
    for p in kids:
        p["enrolled"] = False
        p["entry_count"] = None
    for p in kids:
        Y = cohort(p["birth"])
        if Y < 2014 or Y > 2026:
            p["sib_at_entry"] = None
            if Y < 2014:
                inside = p["hh"]["wijk"] in ("Molenwijk", "Rietveld")
                p["enrolled"] = rng.random() < (0.45 if inside else P_OUT)
                p["entry_count"] = Y if p["enrolled"] else None
            continue
        day = D(Y, 10, 1)
        if not lives_in(p, day):
            p["sib_at_entry"] = None
            continue
        sib = any(q is not p and q["child"] and q["birth"] < p["birth"] and q.get("enrolled") and
                  on_roll(q, Y) for q in p["hh"]["members"])
        p["sib_at_entry"] = sib
        if p["hh"]["wijk"] in ("Molenwijk", "Rietveld"):
            pr = P_SIB if sib else P_NOSIB[p["hh"]["wijk"]]
        else:
            pr = P_OUT * (6 if sib else 1)
        p["enrolled"] = bool(rng.random() < pr)
        p["entry_count"] = Y if p["enrolled"] else None
    return kids


def on_roll(p, Y):
    """On the roll at the 1 October count of year Y: entered, not yet past group 8, still living in the district
    (a pupil whose household left the district is off the roll from the next count)."""
    if not p.get("enrolled") or p["entry_count"] is None:
        return False
    if not (p["entry_count"] <= Y <= p["entry_count"] + 7):
        return False
    hh = p["hh"]
    return hh["leave"] is None or D(Y, 10, 1) < hh["leave"]


def roll(kids, Y):
    return [p for p in kids if on_roll(p, Y)]


def forecast(kids, persons, rates, out_avg, Y_list=P.FORECAST_YEARS, pooled=None):
    """Pupils at each forecast count: the 2026 roll still within group 8, plus every catchment child living there on
    1 October 2026 who first counts by then, at the rate for its circumstance (an older sibling on the 2026 roll who is
    still on it at the child's count), plus the out-of-catchment entrants at their five-intake average."""
    base26 = roll(kids, 2026)
    out = {}
    for Y in Y_list:
        stay = [p for p in base26 if p["entry_count"] + 7 >= Y]
        exp = 0.0
        n_sib = n_all = 0
        for p in kids:
            c = cohort(p["birth"])
            if not (2027 <= c <= Y) or p["hh"]["wijk"] not in ("Molenwijk", "Rietveld") or not lives_in(p, D(2026, 10, 1)):
                continue
            sib = any(q is not p and q["birth"] < p["birth"] and q in base26 and q["entry_count"] + 7 >= c
                      for q in p["hh"]["members"])
            n_all += 1
            n_sib += sib
            exp += (pooled if pooled is not None else (rates[True] if sib else rates[False]))
        out[Y] = {"stay": len(stay), "entrants": exp, "out": out_avg * (Y - 2026), "pupils": len(stay) + exp +
                  out_avg * (Y - 2026), "n_sib": n_sib, "n_all": n_all}
    return out


# ------------------------------------------------------------------------------------------------- the main call
def past_rates(kids):
    tot = {True: [0, 0], False: [0, 0]}
    out_n = 0
    for Y in P.INTAKE_YEARS:
        for p in kids:
            if cohort(p["birth"]) != Y or not lives_in(p, D(Y, 10, 1)):
                continue
            if p["hh"]["wijk"] in ("Molenwijk", "Rietveld"):
                tot[bool(p["sib_at_entry"])][0] += 1
                tot[bool(p["sib_at_entry"])][1] += int(p["enrolled"])
            elif p["enrolled"]:
                out_n += 1
    rates = {k: v[1] / v[0] for k, v in tot.items()}
    pooled = (tot[True][1] + tot[False][1]) / (tot[True][0] + tot[False][0])
    return rates, pooled, out_n / len(P.INTAKE_YEARS), tot


def tune(kids, persons):
    """The building's normative capacity (whole pupils, never a multiple of 5) is set so that the like-circumstance
    forecast crosses it at exactly one count with the widest margin to every other route's counts."""
    rates, pooled, out_avg, _ = past_rates(kids)
    g = forecast(kids, persons, rates, out_avg)
    pl = forecast(kids, persons, rates, out_avg, pooled=pooled)
    best = None
    for C in range(400, 800):
        if C % 5 == 0:
            continue
        gs = [g[Y]["pupils"] for Y in P.FORECAST_YEARS]
        ps = [pl[Y]["pupils"] for Y in P.FORECAST_YEARS]
        first = next((Y for Y, v in zip(P.FORECAST_YEARS, gs) if v > C), None)
        if first is None or any(v > C for v in ps):
            continue
        m = min([abs(v - C) for v in gs] + [C - max(ps)])
        if best is None or m > best[0]:
            best = (m, C, first)
    return best[1], best[2], best[0]


def build(seed=P.SEED):
    rng = np.random.default_rng(seed)
    persons, hhs = population(rng)
    kids = simulate_school(np.random.default_rng(seed + 100), persons)
    C, first, margin = tune(kids, persons)
    w = {"persons": persons, "hhs": hhs, "kids": kids, "capacity": C, "first_short": first, "margin": margin}
    gas_world(np.random.default_rng(seed + 2000), w)
    bso_world(np.random.default_rng(seed + 3000), w)
    return w


# ------------------------------------------------------------------------------------------------- ask worlds
GAS_EVENTS = {"main": [("exchange", D(2025, 3, 18))], "annex": [("exchange", D(2023, 11, 21)), ("reissue", D(2024, 9, 10))]}


def gas_world(rng, w):
    """Monthly telemetry reads (06:00 local on the 1st) of the main building's and the annex's gas meters from
    1 August 2023 to 1 August 2026, the grid operator's master data, and the true use per school year."""
    days = []
    d = D(2023, 8, 1)
    while d <= D(2026, 8, 1):
        days.append(d)
        d += TD(days=1)
    doy = np.array([x.timetuple().tm_yday for x in days])
    temp = 10.4 - 7.4 * np.cos(2 * np.pi * (doy - 22) / 365.25) + rng.normal(0, 2.6, len(days))
    reads, master, truth = [], [], {}
    for bld, annual in (("main", 23800.0), ("annex", 11900.0)):
        wts = np.maximum(0.0, 17.0 - temp) + 0.35
        wts = wts * np.exp(rng.normal(0, 0.06, len(days)))
        daily = dict(zip(days, annual * wts / wts.sum() * 3.0))
        truth[bld] = {sy: sum(v for k, v in daily.items() if D(sy, 8, 1) <= k < D(sy + 1, 8, 1)) for sy in (2023, 2024, 2025)}
        ean = "8716%014d" % int(rng.integers(10**12, 10**13 - 1))
        seg = {"ean": ean, "ser": "%s%07d" % (rng.choice(["E", "G", "K"]), int(rng.integers(1000000, 9999999))),
               "g": "G25" if bld == "main" else "G16", "from": D(2011, 5, 3) if bld == "main" else D(2014, 2, 17)}
        reg = float(int(rng.integers(90000, 900000)))
        ev = dict((e[1], e[0]) for e in GAS_EVENTS[bld])
        firsts = [D(2023, 8, 1)] + [D(2023 + (8 + k) // 12, (8 + k) % 12 + 1, 1) for k in range(36)]
        firsts = sorted(set(x for x in firsts if x <= D(2026, 8, 1)))
        x = D(2023, 8, 1)
        while x <= D(2026, 8, 1):
            if x in firsts:
                reads.append([seg["ean"], seg["ser"], dt.datetime(x.year, x.month, x.day, 6, 0), round(reg), "T"])
            if x in ev:
                part = 0.42 * daily.get(x, 0.0)
                end_reg = reg + part
                kind = ev[x]
                master.append(dict(seg, out=x, end=round(end_reg), reason=kind, bld=bld))
                if kind == "reissue":
                    reads.append([seg["ean"], seg["ser"], dt.datetime(x.year, x.month, x.day, 10, 0), round(end_reg), "E"])
                    new = {"ean": "8716%014d" % int(rng.integers(10**12, 10**13 - 1)),
                           "ser": "%s%07d" % (rng.choice(["E", "G", "K"]), int(rng.integers(1000000, 9999999))),
                           "g": "G25", "from": x, "begin": float(int(rng.integers(0, 6)))}
                    reads.append([new["ean"], new["ser"], dt.datetime(x.year, x.month, x.day, 10, 0), round(new["begin"]), "B"])
                else:
                    new = {"ean": seg["ean"], "ser": "%s%07d" % (rng.choice(["E", "G", "K"]), int(rng.integers(1000000, 9999999))),
                           "g": seg["g"], "from": x, "begin": float(int(rng.integers(0, 6)))}
                seg = new
                reg = new["begin"] + (daily.get(x, 0.0) - part)
                x += TD(days=1)
                continue
            reg += daily.get(x, 0.0)
            x += TD(days=1)
        master.append(dict(seg, out=None, end=None, reason="", bld=bld))
        w["gas_ean_current_" + bld] = seg["ean"]
    w["gas_reads"] = sorted(reads, key=lambda r: (r[2], r[0]))
    w["gas_master"] = master
    w["gas_truth"] = {sy: truth["main"][sy] + truth["annex"][sy] for sy in (2023, 2024, 2025)}


def bso_world(rng, w):
    """After-school care in the school building in October 2026: the provider books attendance per family per day
    (one row carrying the number of children), and re-coded the location on 12 October 2026 after merging it with its
    Molenwijk location."""
    kids = w["kids"]
    pupils = [p for p in roll(kids, 2026)]
    users = [p for p in pupils if rng.random() < 0.21]
    others = [{"pid": "X%05d" % i, "hh": {"hid": "XH%04d" % (i // 2)}} for i in range(40)]   # pupils of other schools
    weekdays = [D(2026, 10, d) for d in range(1, 32) if D(2026, 10, d).weekday() < 5]
    plan = {}
    for p in users + others:
        dpw = rng.choice([1, 2, 2, 3, 3, 4, 5])
        plan[p["pid"]] = set(int(x) for x in rng.choice(5, size=int(dpw), replace=False))
    rows = []
    truth = {k: [] for k in range(5)}
    fam_of = {}
    for p in users + others:
        fam_of[p["pid"]] = p["hh"]["hid"]
    for day in weekdays:
        wd = day.weekday()
        present = [p for p in users + others if wd in plan[p["pid"]] and rng.random() > 0.07]
        loc = "BSO-KWS" if day < D(2026, 10, 12) else "BSO-MLW2"
        fams = {}
        for p in present:
            fams.setdefault(fam_of[p["pid"]], []).append(p)
        for fam, ps in sorted(fams.items()):
            school_kids = [p for p in ps if not p["pid"].startswith("X")]
            rows.append([day, loc, fam, len(ps), "aanwezig"])
        truth[wd].append(sum(1 for p in present if not p["pid"].startswith("X")))
    w["bso_rows"] = rows
    w["bso_truth"] = {wd: float(np.mean(v)) for wd, v in truth.items()}
    w["bso_users"] = users
    w["bso_others"] = others


if __name__ == "__main__":
    w = build()
    kids = w["kids"]
    print("persons", len(w["persons"]), "households", len(w["hhs"]))
    for Y in range(2020, 2027):
        print(Y, "roll", len(roll(kids, Y)))
    tot = {True: [0, 0], False: [0, 0]}
    for Y in P.INTAKE_YEARS:
        ent = [p for p in kids if cohort(p["birth"]) == Y and p["hh"]["wijk"] in ("Molenwijk", "Rietveld")
               and lives_in(p, D(Y, 10, 1))]
        s = [p for p in ent if p["sib_at_entry"]]
        e = [p for p in ent if p["enrolled"]]
        for p in ent:
            tot[bool(p["sib_at_entry"])][0] += 1
            tot[bool(p["sib_at_entry"])][1] += p["enrolled"]
        print(Y, "children", len(ent), "sib", len(s), "entered", len(e))
    rates = {k: v[1] / v[0] for k, v in tot.items()}
    pooled = (tot[True][1] + tot[False][1]) / (tot[True][0] + tot[False][0])
    print("rates", {k: round(v, 3) for k, v in rates.items()}, "pooled", round(pooled, 3))
    rates, pooled, out_avg, _ = past_rates(kids)
    g = forecast(kids, w["persons"], rates, out_avg)
    pl = forecast(kids, w["persons"], rates, out_avg, pooled=pooled)
    print("capacity", w["capacity"], "first", w["first_short"], "margin", round(w["margin"], 1), "out", out_avg)
    for Y in P.FORECAST_YEARS:
        print(Y, "golden %.1f" % g[Y]["pupils"], "pooled %.1f" % pl[Y]["pupils"], "sib share %d/%d" % (g[Y]["n_sib"], g[Y]["n_all"]))



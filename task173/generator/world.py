"""The Marlstead and Fennick world: one patient-level simulation, April 2021 to March 2028.

The record ships to 31 October 2026; the months after it are the plan's truth (the expected 2027/28 line under the
capacity plan), used only by checks.py. Everything is drawn from one seeded generator, so a rebuild is byte-identical.
"""
from __future__ import annotations

import datetime as dt
import numpy as np

import os as _os
SEED = int(_os.environ.get("T173_SEED", "20"))
MIGRATION = dt.date(2023, 4, 17)          # Fennick Hospital onto the Trust EPR
RECORD_END = dt.date(2026, 10, 31)
WYECROSS = dt.date(2027, 1, 11)
M0 = dt.date(2021, 4, 1)
N_MONTHS = 84                             # April 2021 .. March 2028
REC_MONTHS = 67                           # April 2021 .. October 2026

BANDS = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59",
         "60-64", "65-69", "70-74", "75-79", "80-84", "85-89", "90+"]
DISTRICTS = ["Marlstead", "Coldvale"]
SITES = ["MGH", "FEN"]                    # Marlstead General Hospital, Fennick Hospital

# emergency first presentations with gallstone disease, per 100,000 a year, by band (female, male)
RATE_F = [0, 0, 1, 8, 28, 45, 58, 66, 74, 82, 92, 102, 112, 126, 140, 152, 160, 156, 140]
RATE_M = [0, 0, 0, 3, 9, 15, 22, 30, 40, 52, 64, 78, 92, 108, 124, 140, 150, 150, 138]
RATE_SCALE = 1.20
HAZ = 0.0215                              # emergency admission hazard per patient-month on the cholecystectomy list
P_INDEX = {"MGH": 0.34, "FEN": 0.22}      # cholecystectomy in the emergency spell
P_LIST = 0.86                             # listed for an elective cholecystectomy after a spell without one
GP_CHOLE = 74.0 * 0.76                           # GP referrals with symptomatic gallstones a month (both sites)
P_GP_LISTED = 0.80
VALID_OFF = 0.004                         # removed from a list on validation, a month
CANCEL_ON_DAY = 0.035
SCALE = 0.76                              # catchment relative to the first design (560,000)
LEAD_DAYS = 84                            # Wyecross books about twelve weeks ahead


def month_date(m: int) -> dt.date:
    y, mo = divmod(3 + m, 12)
    return dt.date(2021 + y, mo + 1, 1)


def month_end(m: int) -> dt.date:
    return month_date(m + 1) - dt.timedelta(days=1)


def season(m: int) -> float:
    moy = (3 + m) % 12                    # 0 = January
    return 1.0 + 0.06 * np.cos(2 * np.pi * (moy - 6) / 12)   # a summer peak


def mid_year(year: int) -> dt.date:
    return dt.date(year, 6, 30)


class Pop:
    """Mid-year population by district, band and sex, 2018 to 2032 (the 2022-based projection from 2023)."""

    def __init__(self, rng):
        base = {"Marlstead": int(331_000 * SCALE), "Coldvale": int(229_000 * SCALE)}
        shape = np.array([5.2, 5.6, 5.9, 5.8, 6.2, 6.4, 6.6, 6.4, 6.2, 6.1, 6.6, 6.9, 6.6, 5.9, 5.3, 4.4, 3.0, 1.8, 0.9])
        self.est, self.proj = {}, {}
        for d in DISTRICTS:
            sh = shape * (np.linspace(1.06, 0.9, 19) if d == "Marlstead" else np.linspace(0.92, 1.18, 19))
            sh = sh / sh.sum()
            for s, f in (("F", 0.507), ("M", 0.493)):
                p22 = base[d] * f * sh * (1.0 + (np.arange(19) >= 16) * (0.18 if s == "F" else -0.05))
                growth = np.where(np.arange(19) >= 13, 0.024, np.where(np.arange(19) <= 3, -0.004, 0.002))
                noise = rng.normal(0, 0.004, size=(15, 19))
                for i, yr in enumerate(range(2018, 2033)):
                    v = p22 * (1 + growth) ** (yr - 2022)
                    self.proj[(d, s, yr)] = np.round(v).astype(int)
                    if yr <= 2025:
                        self.est[(d, s, yr)] = np.round(v * (1 + noise[i])).astype(int)

    def at(self, d, s, year, kind="proj"):
        return (self.proj if kind == "proj" else self.est)[(d, s, year)]


def simulate():
    rng = np.random.default_rng(SEED)
    pop = Pop(rng)
    persons = []          # dicts: id, sex, age0 (age at 1 Apr 2021), district, site
    spells = []           # dicts with kind, site, person, admit, discharge, dx, method, procedure, pathway info
    pathways = []         # dicts: id, person, site, group, opcs, priority, added, clock, ubrn, removed, reason, prev
    referrals = []        # e-RS rows
    lists = {"chole": [], "hernia": [], "other": []}

    def new_person(sex, age, district):
        p = {"id": len(persons), "sex": sex, "age0": age, "district": district}
        persons.append(p)
        return p

    def home_site(district):
        return "MGH" if (rng.random() < (0.90 if district == "Marlstead" else 0.18)) else "FEN"

    def rand_day(m, lo=0):
        a = month_date(m)
        n = (month_date(m + 1) - a).days
        return a + dt.timedelta(days=int(rng.integers(lo, n)))

    def add_pathway(person, site, group, priority, added, clock, ubrn, prev=None, opcs=None):
        pw = {"id": len(pathways), "person": person["id"], "site": site, "group": group, "priority": priority,
              "added": added, "clock": clock, "ubrn": ubrn, "removed": None, "reason": None, "prev": prev,
              "opcs": opcs or {"chole": "J183", "hernia": rng.choice(["T202", "T204", "T241"], p=[0.62, 0.08, 0.30]),
                               "other": rng.choice(["H511", "H581", "S061", "T962", "H562"])}[group],
              "first_appt": None}
        pathways.append(pw)
        lists[group].append(pw)
        return pw

    def gp_referral(person, site, m, group):
        rdate = rand_day(m)
        wait_op = int(rng.integers(55, 130))
        appt = rdate + dt.timedelta(days=wait_op)
        ubrn = "%012d" % int(rng.integers(10 ** 11, 10 ** 12))
        referrals.append({"ubrn": ubrn, "received": rdate, "appt": appt, "site": site, "group": group,
                          "priority": "Routine" if rng.random() < 0.93 else "Urgent", "person": person["id"]})
        return ubrn, rdate, appt

    pending = []   # (month due, callable)
    capacity_hist = {"chole": {"MGH": 0, "FEN": 0}}
    target = {g: {k: int(v * SCALE) for k, v in d.items()} for g, d in {"chole": {"MGH": 640, "FEN": 660}, "hernia": {"MGH": 470, "FEN": 430}, "other": {"MGH": 340, "FEN": 280}}.items()}
    em_first = np.zeros(N_MONTHS)
    em_list = np.zeros(N_MONTHS)
    pm_chole = np.zeros(N_MONTHS)

    # seed the lists at April 2021 with patients waiting up to two years
    for g, n in (("chole", int(1260 * SCALE)), ("hernia", int(880 * SCALE)), ("other", int(600 * SCALE))):
        for site in SITES:
            for _ in range(int(n * (0.49 if site == "MGH" else 0.51))):
                age = int(np.clip(rng.normal(56 if g == "chole" else 60, 15), 19, 92))
                d = "Marlstead" if (site == "MGH") == (rng.random() < 0.88) else "Coldvale"
                p = new_person("F" if rng.random() < (0.72 if g == "chole" else 0.2) else "M", age, d)
                added = M0 - dt.timedelta(days=int(rng.integers(5, 690)))
                ubrn, rdate, appt = None, None, None
                if rng.random() < 0.82:
                    rdate = added - dt.timedelta(days=int(rng.integers(70, 170)))
                    appt = added - dt.timedelta(days=int(rng.integers(0, 40)))
                    ubrn = "%012d" % int(rng.integers(10 ** 11, 10 ** 12))
                    referrals.append({"ubrn": ubrn, "received": rdate, "appt": appt, "site": site, "group": g,
                                      "priority": "Routine", "person": p["id"]})
                pw = add_pathway(p, site, g, "P3" if rng.random() < 0.25 else "P4", added, rdate or added, ubrn)
                pw["first_appt"] = appt

    def year_frac(m):
        return 2021 + (m + 3) / 12.0

    def wyecross_capacity(m, group, site, L):
        """Elective operations a month. The Trust held its lists near their sizes until Wyecross opened."""
        base = {"chole": 34, "hernia": 31, "other": 23}[group] * SCALE
        if month_date(m) < dt.date(2027, 1, 1):
            return max(10, base + 0.09 * (L - target[group][site]))
        work = {"chole": 150, "hernia": 120, "other": 60}[group]
        if group == "chole":
            return base + 112 * SCALE
        return base + ({"hernia": 58, "other": 30}[group]) * SCALE

    for m in range(N_MONTHS):
        a, b = month_date(m), month_end(m)
        yr = a.year if a.month >= 7 else a.year - 1
        # ---- emergency first presentations from the population
        for d in DISTRICTS:
            for s, rates in (("F", RATE_F), ("M", RATE_M)):
                popv = pop.at(d, s, min(max(a.year, 2018), 2032))
                lam = popv * np.array(rates) * RATE_SCALE / 1e5 / 12 * season(m)
                counts = rng.poisson(lam)
                for bi in np.nonzero(counts)[0]:
                    for _ in range(counts[bi]):
                        lo = 0 if BANDS[bi] == "90+" else int(BANDS[bi].split("-")[0])
                        age = lo + int(rng.integers(0, 5))
                        p = new_person(s, age - int((m) / 12), d)
                        site = home_site(d)
                        pending.append(("first", m, p, site))
        if rng.random() < 1.0:   # out-of-area visitors presenting at either hospital
            for _ in range(rng.poisson(1.9 * SCALE * season(m))):
                p = new_person("F" if rng.random() < 0.6 else "M", int(rng.integers(25, 85)), "Other")
                pending.append(("first", m, p, "MGH" if rng.random() < 0.6 else "FEN"))
        # ---- conversions from the cholecystectomy list
        for pw in list(lists["chole"]):
            pm_chole[m] += 1
            if rng.random() < HAZ * season(m):
                pending.append(("conv", m, persons[pw["person"]], pw))
        # ---- resolve this month's emergency spells
        for kind, mm, p, x in [e for e in pending if e[1] == m and e[0] in ("first", "conv")]:
            if kind == "first":
                site = x
                adm = rand_day(m)
                em_first[m] += 1
                pw = None
            else:
                pw = x
                if pw["removed"] is not None:
                    continue
                site = home_site(p["district"]) if p["district"] != "Other" else pw["site"]
                adm = max(rand_day(m), pw["added"] + dt.timedelta(days=1))
                if adm > b:
                    adm = b
                em_list[m] += 1
            dxr = rng.random()
            dx = ("K80.0" if dxr < 0.30 else "K80.1" if dxr < 0.40 else "K80.2" if dxr < 0.60 else "K80.5" if dxr < 0.65
                  else "K81.0" if dxr < 0.75 else "K85.1" if dxr < 0.90 else "K83.0" if dxr < 0.95 else "K80.3")
            index = rng.random() < P_INDEX[site] * (0.4 if dx in ("K85.1", "K83.0") else 1.15)
            los = int(rng.integers(1, 4)) + (int(rng.integers(1, 6)) if index or dx in ("K85.1", "K83.0") else 0)
            spells.append({"kind": "EM_GS", "site": site, "person": p["id"], "admit": adm,
                           "discharge": adm + dt.timedelta(days=los), "dx": dx, "proc": "J183" if index else None,
                           "route": rng.choice(["AE", "GP", "AE", "AE", "SDEC"]), "spec": "301" if dx == "K85.1" and rng.random() < 0.45 else "100"})
            if index:
                if pw is not None:
                    pw["removed"], pw["reason"] = adm, "treated_emergency"
                    lists["chole"].remove(pw)
            elif pw is None and rng.random() < P_LIST:
                added = adm + dt.timedelta(days=los + int(rng.integers(20, 60)))
                lm = (added.year - 2021) * 12 + added.month - 4
                if lm < N_MONTHS:
                    pending.append(("list", lm, p, (site, "P2" if dx in ("K85.1", "K83.0") else "P3", added)))
        for kind, mm, p, x in [e for e in pending if e[1] == m and e[0] == "list"]:
            site, pri, added = x
            add_pathway(p, site, "chole", pri, added, added, None)
        pending = [e for e in pending if e[1] > m or e[0] == "gp"]
        # ---- GP referrals that reach the lists
        for g, lam in (("chole", GP_CHOLE), ("hernia", 64.0 * SCALE), ("other", 44.0 * SCALE)):
            for _ in range(rng.poisson(lam * (1 + 0.004 * (m / 12)))):
                d = "Marlstead" if rng.random() < 0.6 else "Coldvale"
                p = new_person("F" if rng.random() < (0.72 if g == "chole" else 0.22) else "M",
                               int(np.clip(rng.normal(52 if g == "chole" else 58, 15), 19, 92)), d)
                site = home_site(d)
                ubrn, rdate, appt = gp_referral(p, site, m, g)
                if rng.random() < (P_GP_LISTED if g == "chole" else 0.72):
                    added = appt + dt.timedelta(days=int(rng.integers(0, 21)))
                    lm = (added.year - 2021) * 12 + added.month - 4
                    pending.append(("gp", lm, p, (site, g, added, rdate, ubrn, appt)))
        for kind, mm, p, x in [e for e in pending if e[0] == "gp" and e[1] <= m]:
            site, g, added, rdate, ubrn, appt = x
            pw = add_pathway(p, site, g, "P3" if rng.random() < 0.28 else "P4", added, rdate, ubrn)
            pw["first_appt"] = appt
            if g == "hernia" and rng.random() < 0.05:       # an umbilical repair listed beside an inguinal one
                pw2 = add_pathway(p, site, g, pw["priority"], added, rdate, ubrn, opcs="T241" if pw["opcs"] != "T241" else "T202")
                pw2["first_appt"] = appt
            elif g == "hernia" and pw["opcs"] == "T202" and rng.random() < 0.06:   # bilateral, repaired one side at a time
                pw2 = add_pathway(p, site, g, pw["priority"], added, rdate, ubrn, opcs="T202")
                pw2["first_appt"] = appt
        pending = [e for e in pending if not (e[0] == "gp" and e[1] <= m)]
        # ---- 2025/26 list balancing: Fennick's longest hernia waiters moved to Marlstead's weekend lists
        if 48 <= m <= 58:
            fen = sorted([w for w in lists["hernia"] if w["site"] == "FEN" and w["added"] < a],
                         key=lambda w: (w["added"], w["id"]))[:int(rng.integers(9, 18))]
            for pw in fen:
                day = rand_day(m)
                pw["removed"], pw["reason"] = day, "moved"
                pw["stale_until"] = day + dt.timedelta(days=int(rng.integers(25, 100)))
                lists["hernia"].remove(pw)
                npw = add_pathway(persons[pw["person"]], "MGH", "hernia", pw["priority"], day, pw["clock"], pw["ubrn"],
                                  prev=pw["id"], opcs=pw["opcs"])
                npw["first_appt"] = pw["first_appt"]
                npw["moved_from"] = pw["id"]
        # ---- elective operations, priority then date added; validation removals
        for g in lists:
            for site in SITES:
                L = [pw for pw in lists[g] if pw["site"] == site and pw["added"] <= b]
                for pw in L:
                    if rng.random() < VALID_OFF:
                        pw["removed"], pw["reason"] = rand_day(m), "validation"
                        lists[g].remove(pw)
                L = [pw for pw in L if pw["removed"] is None]
                cap = int(round(wyecross_capacity(m, g, site, len(L)) * (1 + rng.normal(0, 0.06))))
                if month_date(m) >= dt.date(2027, 1, 1):   # Wyecross books in date order about 15 weeks ahead
                    L = [w for w in L if (b - w["added"]).days >= LEAD_DAYS or w["priority"] == "P2" and (b - w["added"]).days >= 28]
                L.sort(key=lambda w: ({"P2": 0, "P3": 1, "P4": 2}[w["priority"]], w["added"], w["id"]))
                for pw in L[:max(cap, 0)]:
                    day = rand_day(m)
                    if day <= pw["added"]:
                        day = min(pw["added"] + dt.timedelta(days=7), b)
                    p = persons[pw["person"]]
                    if rng.random() < CANCEL_ON_DAY * (1.7 if pw["site"] == "MGH" else 0.8) and day < dt.date(2027, 1, 1):
                        spells.append({"kind": "EL_CANC", "site": pw["site"], "person": p["id"], "admit": day,
                                       "discharge": day, "dx": "Z53.0" if False else {"chole": "K80.2", "hernia": "K40.9", "other": "K64.9"}[g],
                                       "proc": None, "route": "WL", "spec": "100"})
                        pw["removed"], pw["reason"] = day, "cancelled_relisted"
                        lists[g].remove(pw)
                        npw = add_pathway(p, pw["site"], g, pw["priority"], day, day, None, prev=pw["id"], opcs=pw["opcs"])
                        npw["first_appt"] = None
                        continue
                    dc = rng.random() < (0.66 if g == "chole" else 0.78)
                    spells.append({"kind": "EL_GS", "site": pw["site"], "person": p["id"], "admit": day,
                                   "discharge": day + dt.timedelta(days=0 if dc else int(rng.integers(1, 4))),
                                   "dx": {"chole": "K80.2", "hernia": "K40.9", "other": "K64.9"}[g], "proc": pw["opcs"],
                                   "route": "WL", "spec": "100", "dc": dc})
                    pw["removed"], pw["reason"] = day, "treated_elective"
                    lists[g].remove(pw)
    return {"pop": pop, "persons": persons, "spells": spells, "pathways": pathways, "referrals": referrals,
            "em_first": em_first, "em_list": em_list, "pm_chole": pm_chole}


if __name__ == "__main__":
    W = simulate()
    ef, el, pm = W["em_first"], W["em_list"], W["pm_chole"]
    for i in range(7):
        s = slice(12 * i, 12 * i + 12)
        print("FY%d/%02d first %4.0f list %4.0f total %4.0f mean list %6.0f" % (2021 + i, (22 + i) % 100, ef[s].sum(),
              el[s].sum(), ef[s].sum() + el[s].sum(), pm[s].mean()))
    print(len(W["spells"]), len(W["pathways"]), len(W["referrals"]))

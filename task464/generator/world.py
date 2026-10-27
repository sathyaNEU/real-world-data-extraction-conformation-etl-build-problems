#!/usr/bin/env python3
"""task464: the clean truth, before any mess is applied or any document written.

The plan is a nonprofit Medicaid managed care organisation contracting outpatient dialysis and infusion
capacity for its 2027 network year (1 July 2027 to 30 June 2028). Forty sites in twelve service areas.

Everything the ladder turns on is built here by construction and the seed decides texture only:

  R0  attested stations        x sessions a week x the modality figure   (the default path)
  R1  state licensed stations  x sessions a week x the modality figure
  R2  the site's busiest week over the four-year record                  (the revealed volume ceiling)
  R3  deliverable positions    x sessions a week x the modality figure   (the golden)

`conditions()` returns the whole ladder arithmetic so `checks.py` and `ladder_prototype.py` read the same
numbers.
"""
import collections
import datetime as dt
import itertools
import random

SEED = 464
CUSHION = 1.15
FLOOR = 6.0                       # per cent of an area's required figure
ASOF = dt.date(2027, 2, 19)
REC_START = dt.date(2023, 1, 2)   # the Monday the four-year record opens
REC_WEEKS = 208                   # through 2026-12-27, the last full week of the contract year
DEMAND_YEAR = 2026
WEEKS_IN_CONTRACT_YEAR = 52       # the contract's own divisor
ROSTER_CHANGE_WEEK = 118          # Monday 2025-04-07: the week the closed shifts come off the roster
SEASONAL_FILL = 0.95
PEAK_OVER_MEAN_CAP = 1.80
PEAK_OVER_ATTESTED_CAP = 1.05

# code, name, role, 2027 enrolment growth, 2026 true utilisation, busiest-week mode, sites
AREAS = [
    ("SA-01", "Ammerly",        "clear", 1.050, 0.620, "stable",   4),
    ("SA-02", "Bexhollow",      "flip",  1.110, 0.834, "stable",   3),
    ("SA-03", "Crannock",       "clear", 1.070, 0.600, "stable",   4),
    ("SA-04", "Durnsfield",     "short", 1.060, 0.915, "stable",   3),
    ("SA-05", "Eastmoor Reach", "clear", 1.040, 0.660, "seasonal", 3),
    ("SA-06", "Fallowbray",     "clear", 1.080, 0.580, "stable",   4),
    ("SA-07", "Granley",        "flip",  1.100, 0.845, "stable",   3),
    ("SA-08", "Hesper Vale",    "clear", 1.060, 0.640, "seasonal", 3),
    ("SA-09", "Innsmere",       "short", 1.090, 0.895, "stable",   4),
    ("SA-10", "Jarrowmead",     "clear", 1.050, 0.630, "stable",   3),
    ("SA-11", "Kettleby",       "flip",  1.080, 0.862, "stable",   3),
    ("SA-12", "Lowenbrook",     "short", 1.070, 0.905, "stable",   3),
]
CODES = [a[0] for a in AREAS]
AREA = {a[0]: dict(code=a[0], name=a[1], role=a[2], growth=a[3], util=a[4], mode=a[5], n=a[6])
        for a in AREAS}
CLOSED_SHIFT_AREAS = ("SA-02", "SA-07")      # every site in the area closed its third shift
EXTRA_CLOSED_AREAS = ("SA-05", "SA-08", "SA-09")   # one site each, so the closure is no marker

OPERATORS = [
    ("Marrowdale Renal Group", "chain"), ("Pelbrook Kidney Care", "chain"),
    ("Hainswell Dialysis Partners", "chain"), ("Corrindale Infusion Services", "chain"),
    ("Westmarch Community Dialysis", "independent"), ("Tolbury Renal Associates", "independent"),
    ("Needham Flats Infusion Suite", "independent"), ("Quilby Point Kidney Center", "independent"),
]
LOCALITIES = {
    "SA-01": ["Ammerly", "North Ammerly", "Pendrick", "Ammerly Heights"],
    "SA-02": ["Bexhollow", "Lower Bexhollow", "Stanmer Cross"],
    "SA-03": ["Crannock", "Crannock Mills", "Dalbury", "Sarn Hill"],
    "SA-04": ["Durnsfield", "Durnsfield West", "Oakenby"],
    "SA-05": ["Eastmoor Reach", "Harbury Point", "Melliscombe"],
    "SA-06": ["Fallowbray", "Fallowbray South", "Winderly", "Thrushmead"],
    "SA-07": ["Granley", "Granley Park", "Ovenshaw"],
    "SA-08": ["Hesper Vale", "Culvert Bridge", "Rimmerton"],
    "SA-09": ["Innsmere", "Innsmere Docks", "Falgate", "Brisley Row"],
    "SA-10": ["Jarrowmead", "Jarrowmead East", "Cawthorne Spur"],
    "SA-11": ["Kettleby", "Kettleby Green", "Marlow Dene"],
    "SA-12": ["Lowenbrook", "Lowenbrook Landing", "Arrowfield"],
}
STREETS = ["Ferrier Road", "Lanchbury Avenue", "Dunmore Street", "Kettlewell Road", "Harrowgate Lane",
           "Sedgemill Road", "Pentland Way", "Bramshaw Street", "Colverton Road", "Nettlefold Avenue",
           "Orrell Street", "Wraysbury Road", "Fenniman Lane", "Hallowgate Road", "Sturmy Avenue",
           "Peverell Street", "Caddonby Road", "Litchmere Way", "Rushbrook Street", "Ganton Road"]


def _weeks():
    return [REC_START + dt.timedelta(weeks=w) for w in range(REC_WEEKS)]


def build(seed=SEED):
    rnd = random.Random(seed)
    sites, sid = [], 0
    for code in CODES:
        a = AREA[code]
        locs = LOCALITIES[code][:]
        for k in range(a["n"]):
            sid += 1
            if a["role"] == "flip":
                mod, turns, days = "dialysis", 1, 6
                shifts = 2 if code in CLOSED_SHIFT_AREAS else 3
                ceiling = rnd.choice([8, 9, 9, 10])
            else:
                mod = "dialysis" if rnd.random() < 0.55 else "infusion"
                turns = 1 if mod == "dialysis" else 2
                days = rnd.choice([5, 6]) if mod == "dialysis" else 5
                shifts = rnd.choice([2, 3])
                ceiling = rnd.choice([7, 8, 8, 10]) if mod == "dialysis" else rnd.choice([4, 4, 5, 6])
            loc = locs[k % len(locs)]
            op = OPERATORS[(sid * 3) % len(OPERATORS)]
            name = "%s %s" % (loc, "Dialysis Center" if mod == "dialysis" else "Infusion Center")
            sites.append(dict(
                site="PS-%05d" % (10400 + sid * 37), seq=sid, area=code, modality=mod, locality=loc,
                operator=op[0], operator_kind=op[1], name=name,
                address="%d %s, %s" % (100 + (sid * 53) % 900, STREETS[(sid * 7) % len(STREETS)], loc),
                days=days, shifts=shifts, sessions=days * shifts, turns=turns, rounds=days * shifts * turns,
                ceiling=ceiling, gap=0, role=a["role"], closed_shift=False))
    by_area = collections.defaultdict(list)
    for s in sites:
        by_area[s["area"]].append(s)

    # ---------------------------------------------- 2026 volume, the area target hit exactly
    def set_volumes():
        for code in CODES:
            a, grp = AREA[code], by_area[code]
            for s in grp:
                s["R3"] = s["ceiling"] * s["sessions"] * s["turns"]
            sc = a["util"] * sum(s["R3"] for s in grp) / sum(s["u_raw"] * s["R3"] for s in grp)
            for s in grp:
                s["u"] = min(0.955, s["u_raw"] * sc)
                s["peak_fill"] = SEASONAL_FILL if a["mode"] == "seasonal" else min(0.985, s["u"] + 0.080)
                s["vol_2026"] = int(round(s["u"] * s["R3"] * WEEKS_IN_CONTRACT_YEAR))

    for s in sites:
        s["u_raw"] = AREA[s["area"]]["util"] * rnd.uniform(0.94, 1.06)
    set_volumes()

    # -------------------- the plant shortfall: searched in a flip area, drawn in a clear area, none short
    def partial_worst(code, gaps):
        grp = by_area[code]
        cc = sum(s["R3"] for s in grp)
        con = [(s, gaps[s["site"]]) for s in grp if gaps.get(s["site"])]
        ca = cc + sum(g * s["sessions"] * s["turns"] for s, g in con)
        req = int(round(CUSHION * AREA[code]["growth"] * sum(s["vol_2026"] for s in grp)
                        / WEEKS_IN_CONTRACT_YEAR))
        worst = 999.0
        for r in range(len(con) + 1):
            for sub in itertools.combinations(range(len(con)), r):
                cap = ca - sum(con[i][1] * con[i][0]["sessions"] * con[i][0]["turns"] for i in sub)
                worst = min(worst, abs(cap - req) / req * 100.0)
        return worst

    for code in CODES:
        grp, role = by_area[code], AREA[code]["role"]
        if role == "flip":
            best, tries = None, 0
            while best is None and tries < 80:
                if tries:
                    for s in grp:
                        s["ceiling"] = rnd.choice([8, 9, 9, 10])
                    set_volumes()
                tries += 1
                for vec in itertools.product(range(2, 9), repeat=len(grp)):
                    if max(s["ceiling"] + v for s, v in zip(grp, vec)) > 15:
                        continue
                    gaps = {s["site"]: v for s, v in zip(grp, vec)}
                    w = partial_worst(code, gaps)
                    if w >= FLOOR and (best is None or (sum(vec), -w) < best[0]):
                        best = ((sum(vec), -w), gaps)
            assert best, "no plant shortfall vector clears the floor in %s" % code
            for s in grp:
                s["gap"] = best[1][s["site"]]
        elif role == "clear":
            for s in rnd.sample(grp, min(rnd.choice([1, 1, 2]), len(grp))):
                s["gap"] = rnd.choice([2, 3])
    set_volumes()

    # ------------------------------------------------ the shared plant, the licence, the closed shift
    for s in sites:
        s["attested"] = s["ceiling"] + s["gap"]
        s["plant"] = ("a single reverse osmosis water loop" if s["modality"] == "dialysis"
                      else "a single compounding hood") if s["gap"] else ""
        if s["area"] == "SA-12":
            s["licensed"] = s["attested"] + 3          # chairs decommissioned, still on the licence
        elif s["role"] == "short":
            s["licensed"] = s["attested"] + rnd.choice([0, 0, 0, -1])
        else:
            r = rnd.random()
            s["licensed"] = s["attested"] + (rnd.choice([2, 3]) if r < 0.34 else (-1 if r > 0.90 else 0))
        s["R0"] = s["attested"] * s["sessions"] * s["turns"]
        s["R1"] = s["licensed"] * s["sessions"] * s["turns"]

    for code in CLOSED_SHIFT_AREAS:
        for s in by_area[code]:
            s["closed_shift"] = True
    for code in EXTRA_CLOSED_AREAS:
        grp = sorted(by_area[code], key=lambda s: s["R3"])
        (grp[0] if code == "SA-09" else grp[-1])["closed_shift"] = True
    for s in sites:
        if s["closed_shift"]:
            s["sessions_hist"] = (s["days"] * (s["shifts"] + 1) if s["area"] in CLOSED_SHIFT_AREAS
                                  else s["sessions"] + 1)
        else:
            s["sessions_hist"] = s["sessions"]
        s["rounds_hist"] = s["sessions_hist"] * s["turns"]
        s["R2"] = int(round(s["peak_fill"] * s["ceiling"] * s["sessions_hist"] * s["turns"]))
    return sites, by_area


def ladder(sites, by_area):
    rungs = ("R0", "R1", "R2", "R3")
    cap = {r: {c: sum(s[r] for s in by_area[c]) for c in CODES} for r in rungs}
    week = {c: sum(s["vol_2026"] for s in by_area[c]) / float(WEEKS_IN_CONTRACT_YEAR) for c in CODES}
    req_real = {c: CUSHION * AREA[c]["growth"] * week[c] for c in CODES}
    req = {c: int(round(req_real[c])) for c in CODES}
    short = {r: [c for c in CODES if cap[r][c] < req[c]] for r in rungs}
    tot = {r: sum(cap[r].values()) for r in rungs}
    return dict(rungs=rungs, cap=cap, week=week, req=req, req_real=req_real, short=short, tot=tot)


def conditions(sites, by_area, L=None):
    L = L or ladder(sites, by_area)
    cap, req, short, tot, rungs = L["cap"], L["req"], L["short"], L["tot"], L["rungs"]
    g = tot["R3"]
    gold = set(short["R3"])
    margins = [(c, r, (cap[r][c] - req[c]) / req[c] * 100.0) for c in CODES for r in rungs]
    pairs = [(x, y, abs(tot[x] - tot[y]) / g * 100.0)
             for i, x in enumerate(rungs) for y in rungs[i + 1:]]
    flips = [c for c in CODES if cap["R0"][c] >= req[c] > cap["R3"][c]]
    partial_worst, partial_cells, reproduce = 999.0, 0, []
    for c in CODES:
        con = [s for s in by_area[c] if s["gap"]]
        partial_cells += 1 << len(con)
        for mask in range(1 << len(con)):
            v = cap["R0"][c] - sum(con[i]["gap"] * con[i]["sessions"] * con[i]["turns"]
                                   for i in range(len(con)) if mask >> i & 1)
            partial_worst = min(partial_worst, abs(v - req[c]) / req[c] * 100.0)
            if mask != (1 << len(con)) - 1 and c in gold and (v >= req[c]) == (cap["R3"][c] >= req[c]):
                reproduce.append("%s/%d" % (c, mask))
    return dict(
        L=L, margins=margins, worst_margin=min(abs(m) for _, _, m in margins),
        pairs=pairs, closest_pair=min(p[2] for p in pairs), flips=flips,
        distinct_sets=len({tuple(short[r]) for r in rungs}), distinct_totals=len({tot[r] for r in rungs}),
        r2_misses=sorted(gold - set(short["R2"])), r2_adds=sorted(set(short["R2"]) - gold),
        partial_cells=partial_cells, partial_worst=partial_worst, partial_reproduce=reproduce,
        worth={r: (tot[r] - tot["R0"]) / float(g - tot["R0"]) for r in rungs},
        peak_over_mean=max(s["R2"] / (s["vol_2026"] / float(WEEKS_IN_CONTRACT_YEAR)) for s in sites),
        peak_over_attested=max(s["R2"] / float(s["R0"]) for s in sites),
        apparent_util=[(s["vol_2026"] / float(WEEKS_IN_CONTRACT_YEAR)) / s["R0"] for s in sites],
        nearest_half=min(0.5 - abs(L["req_real"][c] - round(L["req_real"][c])) for c in CODES),
        constrained=sum(1 for s in sites if s["gap"]),
        closed=sum(1 for s in sites if s["closed_shift"]),
    )


def verdicts(sites, by_area, L=None):
    L = L or ladder(sites, by_area)
    return {c: (L["cap"]["R3"][c] >= L["req"][c]) for c in CODES}


if __name__ == "__main__":
    sites, by_area = build()
    L = ladder(sites, by_area)
    C = conditions(sites, by_area, L)
    print("sites %d | plant constrained %d | closed a shift %d | golden network %d weekly slots"
          % (len(sites), C["constrained"], C["closed"], L["tot"]["R3"]))
    for r in L["rungs"]:
        print("  %s network %6d  %.4f x golden  short %2d/12  %s"
              % (r, L["tot"][r], L["tot"][r] / L["tot"]["R3"], len(L["short"][r]), " ".join(L["short"][r])))
    print("worst area margin %.2f%% | closest rung pair %.2f%% | distinct sets %d | distinct totals %d"
          % (C["worst_margin"], C["closest_pair"], C["distinct_sets"], C["distinct_totals"]))
    print("flip set %s | R2 misses %s | R2 adds %s" % (C["flips"], C["r2_misses"], C["r2_adds"]))
    print("partial cells %d, worst %.2f%%, reproducing %s"
          % (C["partial_cells"], C["partial_worst"], C["partial_reproduce"] or "none"))
    print("peak/mean %.2f | peak/attested %.3f | apparent util %.3f to %.3f | nearest half %.3f"
          % (C["peak_over_mean"], C["peak_over_attested"], min(C["apparent_util"]),
             max(C["apparent_util"]), C["nearest_half"]))
    print("worth " + ", ".join("%s %+0.3f" % (r, C["worth"][r]) for r in L["rungs"]))
    tre = sum(s["vol_2026"] for s in sites)
    print("2026 treatments %d | four-year estimate %d" % (tre, int(tre * 4.05)))
    print("attested/positions at the constrained sites: " +
          ", ".join("%d/%d" % (s["attested"], s["ceiling"]) for s in sites if s["gap"]))

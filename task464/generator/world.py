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
import math
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
PEAK_OVER_MEAN_CAP = 2.05
PEAK_OVER_ATTESTED_CAP = 1.05

# code, name, role, 2027 enrolment growth, 2026 true utilisation, busiest-week mode, sites
AREAS = [
    ("SA-01", "Ammerly",        "clear", 1.050, 0.620, "stable",   4),
    ("SA-02", "Bexhollow",      "flip",  1.110, 0.834, "stable",   3),
    ("SA-03", "Crannock",       "clear", 1.070, 0.600, "stable",   4),
    ("SA-04", "Durnsfield",     "short", 1.060, 0.915, "stable",   3),
    ("SA-05", "Eastmoor Reach", "clear", 1.040, 0.660, "seasonal", 3),
    ("SA-06", "Fallowbray",     "clear", 1.080, 0.580, "stable",   4),
    ("SA-07", "Granleigh",        "flip",  1.100, 0.845, "stable",   3),
    ("SA-08", "Hesper Vale",    "clear", 1.060, 0.640, "seasonal", 3),
    ("SA-09", "Innsmere",       "short", 1.090, 0.895, "stable",   4),
    ("SA-10", "Jarrowmead",     "clear", 1.050, 0.630, "stable",   3),
    ("SA-11", "Kettlebrook",       "flip",  1.080, 0.862, "stable",   3),
    ("SA-12", "Lowenbrook",     "short", 1.070, 0.905, "stable",   3),
]
CODES = [a[0] for a in AREAS]
AREA = {a[0]: dict(code=a[0], name=a[1], role=a[2], growth=a[3], util=a[4], mode=a[5], n=a[6])
        for a in AREAS}
CLOSED_SHIFT_AREAS = ("SA-02", "SA-07")      # every site in the area closed its third shift
EXTRA_CLOSED_MAX = 3      # further closures elsewhere, so the closed shift is no marker

# The operator market: a few groups with many sites, several with two or three, a handful of single-site
# independents. An operator named for one service category runs only that category; two groups carry a
# neutral name and run both. Sites are drawn from the operators that serve their own category, with these
# weights, so the column carries no order and no two operators hold the same number of sites.
OPERATORS = [
    ("Marrowdale Renal Group", "chain", ("dialysis",), 9),
    ("Pelbrook Kidney Care", "chain", ("dialysis",), 6),
    ("Hainswell Dialysis Partners", "chain", ("dialysis",), 4),
    ("Westmarch Community Dialysis", "independent", ("dialysis",), 2),
    ("Tolbury Renal Associates", "independent", ("dialysis",), 2),
    ("Quilby Point Kidney Center", "independent", ("dialysis",), 1),
    ("Corrindale Infusion Services", "chain", ("infusion",), 8),
    ("Alderwick Infusion Partners", "chain", ("infusion",), 5),
    ("Kestrel Flats Infusion Suite", "independent", ("infusion",), 2),
    ("Brinscote Infusion Care", "independent", ("infusion",), 2),
    ("Lenhardt Health Services", "chain", ("dialysis", "infusion"), 5),
    ("Varrowmere Clinical Group", "independent", ("dialysis", "infusion"), 2),
]
OPERATOR_KIND = {o[0]: o[1] for o in OPERATORS}
DIALYSIS_WORDS = ("renal", "kidney", "dialysis")
INFUSION_WORDS = ("infusion",)


def draw_operator(modality, rnd):
    pool = [(n, wt) for n, kind, cats, wt in OPERATORS if modality in cats]
    tot = sum(wt for _, wt in pool)
    x = rnd.random() * tot
    for n, wt in pool:
        x -= wt
        if x <= 0:
            return n
    return pool[-1][0]


LOCALITIES = {
    "SA-01": ["Ammerly", "North Ammerly", "Pendrick", "Ammerly Heights"],
    "SA-02": ["Bexhollow", "Lower Bexhollow", "Stanmer Cross"],
    "SA-03": ["Crannock", "Crannock Mills", "Dalbury", "Sarn Hill"],
    "SA-04": ["Durnsfield", "Durnsfield West", "Oakenby"],
    "SA-05": ["Eastmoor Reach", "Harbury Point", "Melliscombe"],
    "SA-06": ["Fallowbray", "Fallowbray South", "Winderly", "Thrushmead"],
    "SA-07": ["Granleigh", "Granleigh Park", "Ovenshaw"],
    "SA-08": ["Hesper Vale", "Culvert Bridge", "Rimmerton"],
    "SA-09": ["Innsmere", "Innsmere Docks", "Falgate", "Brisley Row"],
    "SA-10": ["Jarrowmead", "Jarrowmead East", "Cawthorne Spur"],
    "SA-11": ["Kettlebrook", "Kettlebrook Green", "Marlow Dene"],
    "SA-12": ["Lowenbrook", "Lowenbrook Landing", "Arrowfield"],
}
STREETS = ["Ferrier Road", "Lanchbury Avenue", "Dunmore Street", "Kettlewell Road", "Harbourne Lane",
           "Sedgemill Road", "Pentland Way", "Bramshaw Street", "Colverton Road", "Nettlefold Avenue",
           "Orrell Street", "Wraysbury Road", "Fenniman Lane", "Hallowgate Road", "Sturmy Avenue",
           "Peverell Street", "Caddonby Road", "Litchmere Way", "Rushbrook Street", "Ganton Road"]


def _weeks():
    return [REC_START + dt.timedelta(weeks=w) for w in range(REC_WEEKS)]


def build(seed=SEED):
    rnd = random.Random(seed)
    oprnd = random.Random(seed + 991)      # the operator market, drawn off the world's own stream
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
                shifts = rnd.choice([2, 3]) if mod == "dialysis" else rnd.choice([1, 2])
                ceiling = rnd.choice([7, 8, 8, 10]) if mod == "dialysis" else rnd.choice([4, 4, 5, 6])
            loc = locs[k % len(locs)]
            op = draw_operator(mod, oprnd)
            name = "%s %s" % (loc, "Dialysis Center" if mod == "dialysis" else "Infusion Center")
            sites.append(dict(
                site="PS-%05d" % (10400 + sid * 37), seq=sid, area=code, modality=mod, locality=loc,
                operator=op, operator_kind=OPERATOR_KIND[op], name=name,
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

    def set_history():
        for s in sites:
            s["sessions_hist"] = (s["days"] * (s["shifts"] + 1) if s["closed_shift"] else s["sessions"])
            s["rounds_hist"] = s["sessions_hist"] * s["turns"]
            s["R2"] = int(round(s["peak_fill"] * s["ceiling"] * s["sessions_hist"] * s["turns"]))

    # Every area's required figure is kept clear of the rounding boundary by moving one treatment at a
    # time onto the area's largest site, which no margin feels.
    for code in CODES:
        grp = sorted(by_area[code], key=lambda s: -s["R3"])
        for _ in range(40):
            wk = sum(s["vol_2026"] for s in grp) / float(WEEKS_IN_CONTRACT_YEAR)
            x = CUSHION * AREA[code]["growth"] * wk
            if 0.5 - abs(x - round(x)) >= 0.06:
                break
            grp[0]["vol_2026"] += 1
    set_history()
    # Further closures, searched rather than placed: a plant-constrained site in a clear area, accepted only
    # while every ladder condition still holds. Constrained, because at a site whose stations all run the
    # busiest week would then exceed the current roster's own capacity, which a solver's capacity check sees.
    cands = sorted((s for s in sites if s["gap"] and s["role"] == "clear" and not s["closed_shift"]
                    and (s["shifts"] + 1) * s["turns"] <= (3 if s["modality"] == "dialysis" else 4)),
                   key=lambda s: -s["R3"])
    taken = []
    for s in cands:
        if len(taken) >= EXTRA_CLOSED_MAX or s["area"] in {t["area"] for t in taken}:
            continue
        s["closed_shift"] = True
        set_history()
        C = conditions(sites, by_area)
        if (C["worst_margin"] >= FLOOR and C["closest_pair"] >= FLOOR and C["distinct_sets"] == 4
                and C["distinct_totals"] == 4 and len(C["r2_misses"]) >= 2 and len(C["r2_adds"]) >= 1
                and len(C["flips"]) == 3 and not C["partial_reproduce"]
                and C["partial_worst"] >= FLOOR
                and C["peak_over_mean"] <= PEAK_OVER_MEAN_CAP
                and C["peak_over_attested"] <= PEAK_OVER_ATTESTED_CAP
                and max(C["apparent_util"]) < 0.98 and C["nearest_half"] >= 0.05):
            taken.append(s)
        else:
            s["closed_shift"] = False
            set_history()
    # C1 on the nearest area: one short area is nearest the standard under the unrounded figure and under
    # every rounding of it, with two slots of daylight to the runner-up on the tightest reading. The move
    # is a treatment at a time onto a non-nearest short area's largest site, which no margin feels.
    for _ in range(600):
        L = ladder(sites, by_area)
        short = [c for c in CODES if L["cap"]["R3"][c] < L["req"][c]]
        if len(short) < 2:
            break
        hi = {c: int(math.ceil(L["req_real"][c])) - L["cap"]["R3"][c] for c in short}
        lo = {c: int(math.floor(L["req_real"][c])) - L["cap"]["R3"][c] for c in short}
        near = min(short, key=lambda c: (hi[c], c))
        tight = [c for c in short if c != near and lo[c] - hi[near] < 2]
        if not tight:
            break
        grp = sorted(by_area[min(tight, key=lambda c: lo[c])], key=lambda s: -s["R3"])
        grp[0]["vol_2026"] += 1
    # and the required figures stay clear of a half, so round and ceiling differ by a whole slot and no
    # area's verdict depends on which is taken
    for code in CODES:
        grp = sorted(by_area[code], key=lambda s: -s["R3"])
        for _ in range(60):
            wk = sum(s["vol_2026"] for s in grp) / float(WEEKS_IN_CONTRACT_YEAR)
            x = CUSHION * AREA[code]["growth"] * wk
            if 0.5 - abs(x - round(x)) >= 0.06 and abs(x - round(x)) >= 0.06:
                break
            grp[0]["vol_2026"] += 1
    return sites, by_area


def ladder(sites, by_area):
    rungs = ("R0", "R1", "R2", "R3")
    cap = {r: {c: sum(s[r] for s in by_area[c]) for c in CODES} for r in rungs}
    week = {c: sum(s["vol_2026"] for s in by_area[c]) / float(WEEKS_IN_CONTRACT_YEAR) for c in CODES}
    req_real = {c: CUSHION * AREA[c]["growth"] * week[c] for c in CODES}
    req = {c: int(math.ceil(req_real[c])) for c in CODES}
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


# ============================================================ the populations the call never reads
# The main call is the 2027 contract-intent sites' own encounters. Everything below sits outside it and
# carries the ask layer: the sites the plan is not contracting for 2027, the facilities only the state
# register holds, and the service-area boundaries the plan redrew for 2027.
DROPPED_N = 14          # in the 2026 filing and in the directory, no 2027 contract intent
NEW_N = 4               # contract intent for 2027, not in the 2026 filing
OFF_PLAN_N = 18         # licensed in the twelve areas, never in the plan's directory
REDRAWN = (("SA-03", "SA-06"), ("SA-09", "SA-10"), ("SA-01", "SA-12"),
           ("SA-05", "SA-08"))        # pairs that exchanged a locality for the 2027 network year


def extras(sites, seed=SEED + 3):
    """The non-contract sites, the register-only facilities and the 2026 area labels."""
    rnd = random.Random(seed)
    oprnd = random.Random(seed + 991)
    out = []
    sid = 1000
    for kind, n in (("dropped", DROPPED_N), ("off_plan", OFF_PLAN_N)):
        for i in range(n):
            sid += 1
            code = CODES[(i * 5 + (0 if kind == "dropped" else 2)) % 12]
            locs = LOCALITIES[code]
            loc = locs[(i * 3) % len(locs)]
            mod = "dialysis" if rnd.random() < 0.5 else "infusion"
            op = draw_operator(mod, oprnd)
            out.append(dict(
                site="PS-%05d" % (10400 + sid * 37) if kind == "dropped" else "",
                seq=sid, kind=kind, area=code, modality=mod, locality=loc, operator=op,
                operator_kind=OPERATOR_KIND[op],
                name="%s %s" % (loc, "Dialysis Center" if mod == "dialysis" else "Infusion Center"),
                address="%d %s, %s" % (100 + (sid * 71) % 900, STREETS[(sid * 11) % len(STREETS)], loc),
                licensed=rnd.choice([6, 8, 8, 10, 12]) if mod == "dialysis" else rnd.choice([4, 5, 6, 8]),
                weekly=rnd.randint(40, 190) if kind == "dropped" else 0))
    for s in sites:
        s["area_2026"] = s["area"]
        s["in_2026_filing"] = True
    news = sorted(sites, key=lambda s: s["seq"])[::7][:NEW_N]
    for s in news:
        s["in_2026_filing"] = False
    # the two redrawn pairs: a locality moved between areas, so the 2026 label differs from the 2027 one
    moved = []
    for a, b in REDRAWN:
        cand = [s for s in sites if s["area"] == b and s["in_2026_filing"]]
        if cand:
            cand[0]["area_2026"] = a
            moved.append(cand[0])
        cand2 = [s for s in out if s["kind"] == "dropped" and s["area"] == b]
        if cand2:
            cand2[0]["area_2026"] = a
            moved.append(cand2[0])
    for s in out:
        s.setdefault("area_2026", s["area"])
        s["in_2026_filing"] = (s["kind"] == "dropped")
    return out, moved

"""task464 architecture 3, the measured ladder (prototype v7, the one the design note quotes).

Every rung is built by construction and the seed decides texture only. The two searches are the
flip-area shortfall vector (so no partial application of the ceiling lands inside 6 per cent of an
area's line) and the extra dropped shifts outside the flip areas (so the dropped third shift is no
marker while every rung margin still clears 6 per cent).

Run: python3 proto7.py <seed> [--quiet]
"""
import collections
import itertools
import json
import os
import random
import zlib
import sys

SEED = int(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else 464
QUIET = "--quiet" in sys.argv
rnd = random.Random(SEED)
CUSHION, FLOOR = 1.15, 6.0
AREAS = ["A%02d" % i for i in range(1, 13)]
PER_AREA = dict(zip(AREAS, [4, 3, 4, 3, 3, 4, 3, 3, 4, 3, 3, 3]))
PLAN = {   # role, 2027 enrolment growth, area 2026 true utilisation, busiest-week fill mode
    "A01": ("clear", 1.050, 0.620, "stable"),   "A02": ("flip",  1.110, 0.834, "stable"),
    "A03": ("clear", 1.070, 0.600, "stable"),   "A04": ("short", 1.060, 0.915, "stable"),
    "A05": ("clear", 1.040, 0.660, "seasonal"), "A06": ("clear", 1.080, 0.580, "stable"),
    "A07": ("flip",  1.100, 0.845, "stable"),   "A08": ("clear", 1.060, 0.640, "seasonal"),
    "A09": ("short", 1.090, 0.895, "stable"),   "A10": ("clear", 1.050, 0.630, "stable"),
    "A11": ("flip",  1.080, 0.862, "stable"),   "A12": ("short", 1.070, 0.905, "stable"),
}
SEASONAL_FILL, PEAK_CAP = 0.95, 1.75
DROPPED_SHIFT = {"A02", "A07"}
RUNGS = [("R0 attested stations", "R0"), ("R1 licensed stations", "R1"),
         ("R2 revealed volume ceiling", "R2"), ("R3 concurrency ceiling (golden)", "R3")]

sites, sid = [], 0
for a in AREAS:
    role, g, U, fmode = PLAN[a]
    for k in range(PER_AREA[a]):
        sid += 1
        if role == "flip":
            mod, turns, days = "dialysis", 1, 6
            shifts = 2 if a in DROPPED_SHIFT else 3
            ceiling = rnd.choice([11, 12, 12, 13])
        else:
            mod = "dialysis" if rnd.random() < 0.55 else "infusion"
            turns = 1 if mod == "dialysis" else 2
            days = rnd.choice([5, 6]) if mod == "dialysis" else 5
            shifts = rnd.choice([2, 3])
            ceiling = rnd.choice([10, 12, 12, 14, 16]) if mod == "dialysis" else rnd.choice([6, 8, 8, 10])
        sites.append(dict(site="S%03d" % sid, area=a, modality=mod, days=days, shifts=shifts,
                          sessions=days * shifts, turns=turns, ceiling=ceiling, role=role, gap=0,
                          extra_dropped=False))
by_area = collections.defaultdict(list)
for s in sites:
    by_area[s["area"]].append(s)
for s in sites:
    s["R3"] = s["ceiling"] * s["sessions"] * s["turns"]

# ---------------------------------- 2026 volume per site, the area target hit exactly, and demand
for a in AREAS:
    role, g, U, fmode = PLAN[a]
    grp = by_area[a]
    for s in grp:
        s["u_raw"] = U * rnd.uniform(0.94, 1.06)
    scale = U * sum(s["R3"] for s in grp) / sum(s["u_raw"] * s["R3"] for s in grp)
    for s in grp:
        s["u"] = min(0.965, s["u_raw"] * scale)
        s["peak_fill"] = SEASONAL_FILL if fmode == "seasonal" else min(0.99, s["u"] + 0.080)
        s["vol_2026"] = int(round(s["u"] * s["R3"] * 52))
WEEK = {a: sum(s["vol_2026"] for s in by_area[a]) / 52.0 for a in AREAS}
REQ = {a: int(round(CUSHION * PLAN[a][1] * WEEK[a])) for a in AREAS}

# -------------------- the plant shortfall: searched in a flip area, drawn in a clear area, none in a short one
def partial_ok(area, gaps):
    """No partial application of the ceiling inside this area lands within the floor of its line."""
    grp = [s for s in by_area[area] if s["gap"] or True]
    con = [(s, gaps.get(s["site"], 0)) for s in by_area[area] if gaps.get(s["site"], 0)]
    cc = sum(s["R3"] for s in by_area[area])
    ca = cc + sum(gp * s["sessions"] * s["turns"] for s, gp in con)
    worst = 99.0
    for r in range(len(con) + 1):
        for sub in itertools.combinations(range(len(con)), r):
            cap = ca - sum(con[i][1] * con[i][0]["sessions"] * con[i][0]["turns"] for i in sub)
            worst = min(worst, abs(cap - REQ[area]) / REQ[area] * 100.0)
    return worst

for a in AREAS:
    grp, role = by_area[a], PLAN[a][0]
    if role == "flip":
        best, tries = None, 0
        while best is None and tries < 60:
            if tries:                                   # redraw the area's positions and search again
                for s2 in grp:
                    s2["ceiling"] = rnd.choice([11, 12, 12, 13])
                    s2["R3"] = s2["ceiling"] * s2["sessions"] * s2["turns"]
                scale = PLAN[a][2] * sum(x["R3"] for x in grp) / sum(x["u_raw"] * x["R3"] for x in grp)
                for s2 in grp:
                    s2["u"] = min(0.965, s2["u_raw"] * scale)
                    s2["peak_fill"] = SEASONAL_FILL if PLAN[a][3] == "seasonal" else min(0.99, s2["u"] + 0.080)
                    s2["vol_2026"] = int(round(s2["u"] * s2["R3"] * 52))
                WEEK[a] = sum(x["vol_2026"] for x in grp) / 52.0
                REQ[a] = int(round(CUSHION * PLAN[a][1] * WEEK[a]))
            tries += 1
            for vec in itertools.product(range(2, 10), repeat=len(grp)):
                if max(x["ceiling"] + v for x, v in zip(grp, vec)) > 20:
                    continue
                gaps = {x["site"]: v for x, v in zip(grp, vec)}
                w = partial_ok(a, gaps)
                if w >= FLOOR and (best is None or (sum(vec), -w) < best[0]):
                    best = ((sum(vec), -w), gaps, w)
        assert best, "no flip-area shortfall vector clears the floor in %s" % a
        for s2 in grp:
            s2["gap"] = best[1][s2["site"]]
    elif role == "clear":
        for s in rnd.sample(grp, min(rnd.choice([1, 1, 2]), len(grp))):
            s["gap"] = rnd.choice([2, 3])
for s in sites:
    s["attested"] = s["ceiling"] + s["gap"]
    s["plant"] = ("one water treatment loop" if s["modality"] == "dialysis" else "one compounding hood") if s["gap"] else ""
    if s["area"] == "A12":
        s["licensed"] = s["attested"] + 3
    elif s["role"] == "short":
        s["licensed"] = s["attested"] + rnd.choice([0, 0, 1, -1])
    else:
        r = rnd.random()
        s["licensed"] = s["attested"] + (rnd.choice([2, 3]) if r < 0.34 else (-1 if r > 0.90 else 0))
    s["R0"] = s["attested"] * s["sessions"] * s["turns"]
    s["R1"] = s["licensed"] * s["sessions"] * s["turns"]

# ------------------------------------- the busiest week, and the extra dropped shifts searched for
def recompute_r2():
    for s in sites:
        if s["area"] in DROPPED_SHIFT:
            s["sessions_hist"] = s["days"] * (s["shifts"] + 1)     # the third shift it has since closed
        elif s["extra_dropped"]:
            s["sessions_hist"] = (s["days"] + 1) * s["shifts"]     # the sixth day it has since dropped
        else:
            s["sessions_hist"] = s["sessions"]
        s["R2"] = int(round(s["peak_fill"] * s["ceiling"] * s["sessions_hist"] * s["turns"]))

def state():
    cap = {r: {a: sum(s[r] for s in by_area[a]) for a in AREAS} for _, r in RUNGS}
    short = {r: [a for a in AREAS if cap[r][a] < REQ[a]] for _, r in RUNGS}
    tot = {r: sum(cap[r].values()) for _, r in RUNGS}
    margins = [(a, r, (cap[r][a] - REQ[a]) / REQ[a] * 100.0) for a in AREAS for _, r in RUNGS]
    return cap, short, tot, margins

def conditions():
    cap, short, tot, margins = state()
    gold, G = set(short["R3"]), tot["R3"]
    ok = (min(abs(m) for _, _, m in margins) >= FLOOR
          and min(abs(tot[x] - tot[y]) / G for i, (_, x) in enumerate(RUNGS) for _, y in RUNGS[i + 1:]) >= FLOOR / 100.0
          and len({tuple(short[r]) for _, r in RUNGS}) == 4
          and len(gold - set(short["R2"])) >= 2 and len(set(short["R2"]) - gold) >= 1
          and max(s["R2"] / (s["vol_2026"] / 52.0) for s in sites) <= PEAK_CAP
          and max(s["R2"] / s["R0"] for s in sites) <= 1.05)
    return ok, cap, short, tot, margins

recompute_r2()
cands = sorted((s for s in sites if s["area"] not in DROPPED_SHIFT and s["days"] == 5),
               key=lambda s: -s["R3"])
chosen = []
for s in cands:
    if len(chosen) >= 3 or s["area"] in {c["area"] for c in chosen}:
        continue
    s["extra_dropped"] = True
    recompute_r2()
    if conditions()[0]:
        chosen.append(s)
    else:
        s["extra_dropped"] = False
        recompute_r2()
ok, CAP, short, TOT, margins = conditions()
G = TOT["R3"]

print("seed %d | 40 sites | plant constrained %d | network golden %d weekly slots | all conditions: %s"
      % (SEED, sum(1 for s in sites if s["gap"]), G, "PASS" if ok else "FAIL"))
print("%-34s %8s %9s %7s  %s" % ("rung", "network", "x golden", "short", "short areas"))
for name, r in RUNGS:
    print("%-34s %8d %9.4f %5d/12  %s" % (name, TOT[r], TOT[r] / G, len(short[r]), " ".join(short[r])))
if not QUIET:
    print()
    print("area  role   growth   util  demand/wk  required    R0    R1    R2    R3   R0/R1/R2/R3 verdicts      m0%     m1%     m2%     m3%")
    for a in AREAS:
        ms = [(CAP[r][a] - REQ[a]) / REQ[a] * 100.0 for _, r in RUNGS]
        print("%-5s %-6s %6.3f %6.3f %10.1f %9d %5d %5d %5d %5d   %-5s %-5s %-5s %-5s  %+7.1f %+7.1f %+7.1f %+7.1f" % (
            a, PLAN[a][0], PLAN[a][1], WEEK[a] / CAP["R3"][a], WEEK[a], REQ[a],
            CAP["R0"][a], CAP["R1"][a], CAP["R2"][a], CAP["R3"][a],
            *["ok" if CAP[r][a] >= REQ[a] else "SHORT" for _, r in RUNGS], *ms))
gold = set(short["R3"])
print()
for name, r in RUNGS[:3]:
    s = set(short[r])
    print("%-34s misses %d of the golden's %d (%s) | adds %d the golden clears (%s)"
          % (name, len(gold - s), len(gold), " ".join(sorted(gold - s)) or "-",
             len(s - gold), " ".join(sorted(s - gold)) or "-"))
print("flip set (clear on attested, short on the golden): %s" %
      " ".join(a for a in AREAS if CAP["R0"][a] >= REQ[a] > CAP["R3"][a]))
print("worst of the 48 area-rung margins: %.2f per cent of required (%s)" %
      min((abs(m), "%s %s" % (a, r)) for a, r, m in margins))
print("closest pair of rung totals: %.4f of the golden; R0 %.4f R1 %.4f R2 %.4f" % (
    min(abs(TOT[x] - TOT[y]) / G for i, (_, x) in enumerate(RUNGS) for _, y in RUNGS[i + 1:]),
    TOT["R0"] / G, TOT["R1"] / G, TOT["R2"] / G))
print("worth on the graded quantity, as a share of the correction the golden makes: " + ", ".join(
    "%s %+.3f" % (r, (TOT[r] - TOT["R0"]) / (G - TOT["R0"])) for _, r in RUNGS))
w, where, cells = 99.0, "", 0
reproduce = []
for a in AREAS:
    con = [s for s in by_area[a] if s["gap"]]
    cells += 1 << len(con)
    for mask in range(1 << len(con)):
        cap = CAP["R0"][a] - sum(con[i]["gap"] * con[i]["sessions"] * con[i]["turns"]
                                 for i in range(len(con)) if mask >> i & 1)
        m = abs(cap - REQ[a]) / REQ[a] * 100.0
        if m < w:
            w, where = m, "%s mask %d" % (a, mask)
        if mask != (1 << len(con)) - 1 and (cap >= REQ[a]) == (CAP["R3"][a] >= REQ[a]) and a in gold:
            reproduce.append("%s mask %d" % (a, mask))
print("partial applications of the ceiling: %d cells; none reproduces a golden-short area's verdict: %s;"
      " nearest cell to its area's line %.2f per cent (%s)"
      % (cells, "yes" if not reproduce else "NO " + ";".join(reproduce[:4]), w, where))

def plateau(s):
    K, d, turns = s["ceiling"], s["shifts"], s["turns"]
    dur = 240 if s["modality"] == "dialysis" else 150
    plat = 150 if s["modality"] == "dialysis" else 90
    stag = max(3, min(10, (dur - plat) // max(1, K - 1)))
    b = (d * s["u"] - 1.0) / (d - 1) if d > 1 else s["u"]
    hist, mmax, ymax, rec = collections.Counter(), [], [], 0
    r2 = random.Random(zlib.crc32(("%d-%s" % (SEED, s["site"])).encode("utf-8")))
    for month in range(48):
        mm = 0
        for _ in range(s["days"] * 4 + r2.choice([0, 1])):
            for j in range(d):
                for _t in range(turns):
                    n = K if j == 0 else max(1, min(K, int(round(b * K + r2.choice([-1, 0, 0, 1])))))
                    for lev in range(1, n):
                        hist[lev] += 2 * stag
                    hist[n] += dur - (n - 1) * stag
                    mm = max(mm, n)
        mmax.append(mm)
        if month % 12 == 11:
            ymax.append(max(mmax[-12:]))
        rec = max(rec, mm)
    tot = sum(hist.values())
    return dict(K=K, rec=rec, mmin=min(mmax), ymin=min(ymax), share=hist[K] / tot,
                cross=(tot - hist[K]) / tot, above=hist.get(K + 1, 0), plat=dur - (K - 1) * stag)

pl = [plateau(s) for s in sites]
conv = all(p["rec"] == p["K"] and p["mmin"] == p["K"] and p["ymin"] == p["K"] and p["above"] == 0 for p in pl)
sh = sorted(p["share"] for p in pl)
print()
print("ceiling convergence, 40 of 40 sites: the record maximum, every one of the 4 yearly maxima and"
      " every one of the 48 monthly maxima equal the site's positions, and one more never runs: %s" % ("yes" if conv else "NO"))
print("share of a site's treating hours at exactly the ceiling: min %.3f median %.3f max %.3f; smallest"
      " quantile returning the ceiling: worst %.3f median %.3f; a full session holds every position for"
      " at least %d minutes"
      % (sh[0], sh[20], sh[-1], max(p["cross"] for p in pl), sorted(p["cross"] for p in pl)[20],
         min(p["plat"] for p in pl)))
pk = sorted(s["R2"] / (s["vol_2026"] / 52.0) for s in sites)
print("busiest week over the site's own mean week: min %.2f median %.2f max %.2f | sites that lost a"
      " shift since 2023: %d of 40 in %d areas (%s) | required figures nearest a half treatment %.3f"
      % (pk[0], pk[20], pk[-1], sum(1 for s in sites if s["sessions_hist"] > s["sessions"]),
         len({s["area"] for s in sites if s["sessions_hist"] > s["sessions"]}),
         " ".join(sorted({s["area"] for s in sites if s["sessions_hist"] > s["sessions"]})),
         min(abs(CUSHION * PLAN[a][1] * WEEK[a] - round(CUSHION * PLAN[a][1] * WEEK[a])) for a in AREAS)))
print("attested stations over positions at each constrained site: " +
      ", ".join("%d/%d" % (s["attested"], s["ceiling"]) for s in sites if s["gap"]))
json.dump(dict(sites=sites, week=WEEK, required=REQ, totals=TOT, short=short),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ladder_prototype_%d.json" % SEED), "w"), indent=1, default=str)

# ------------------------------------------------- the readings a hygiene battery would run on the pack
app = [(s["vol_2026"] / 52.0) / s["R0"] for s in sites]
pw = [s["R2"] / s["R0"] for s in sites]
print()
print("apparent utilisation on attested stations, per site: min %.3f max %.3f (no site over 1)"
      % (min(app), max(app)))
print("busiest week over the site's CURRENT attested weekly capacity: min %.3f max %.3f (no week over 1)"
      % (min(pw), max(pw)))
cs = [(CAP["R0"][a] - CAP["R3"][a]) / CAP["R3"][a] for a in AREAS]
sz = [CAP["R3"][a] for a in AREAS]
mc, ms_ = sum(cs) / 12, sum(sz) / 12
cov = sum((x - mc) * (y - ms_) for x, y in zip(cs, sz))
den = (sum((x - mc) ** 2 for x in cs) * sum((y - ms_) ** 2 for y in sz)) ** 0.5
print("corr(the correction the ceiling makes to an area, the area's own size): %+.4f" % (cov / den))
print("areas whose verdict differs between the attested reading and the golden: %d of 12"
      % sum(1 for a in AREAS if (CAP["R0"][a] >= REQ[a]) != (CAP["R3"][a] >= REQ[a])))

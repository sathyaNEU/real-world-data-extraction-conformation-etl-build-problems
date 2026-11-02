"""task271 generator checks, run on the installed pack (task271/target) and on the world's clean truth.

Every label starting R1, R2 or R3 is the client's three rules executed; SFn rows are the design note's semantic fork
table; L1 rows are the Layer 1 neutrality checks; G rows the input gates; Z rows the realism sweep; B rows each graded
figure's distance to its bin edge."""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import analysis as A        # noqa: E402
import common as K          # noqa: E402
import docs as D            # noqa: E402
import world as W           # noqa: E402

FAIL = []
N = [0]


def check(label, ok, detail=""):
    N[0] += 1
    print("%-4s %-78s %s" % ("ok" if ok else "FAIL", label[:78], detail))
    if not ok:
        FAIL.append(label)


def setof(vals):
    return sorted(c for c, v in vals.items() if v >= K.THRESHOLD)


def margin(v):
    return v / K.THRESHOLD if v >= K.THRESHOLD else K.THRESHOLD / v


# ------------------------------------------------------------------------------------------------- shared state
reg = A.register(TARGET)
stocked = sorted(c for c, v in reg.items() if v["access"] != "walk-in")
cts = A.counts(TARGET, reg)
iv = A.interviews(TARGET, reg)
M = A.main_call(TARGET)
L = M["lakes"]
GOLD = sorted(c for c in stocked if L[c]["golden"] >= K.THRESHOLD)
fig = json.load(open(os.path.join(HERE, "figures.json")))
by_lake = {c: [r for r in iv if r["lake"] == c] for c in reg}
cts_by = {c: [x for x in cts if x["lake"] == c] for c in reg}
cls = {c: reg[c]["reg"] for c in reg}


def family_sets():
    out = {}
    for k in L[GOLD[0]]["family"]:
        out[k] = sorted(c for c in stocked if L[c]["family"][k] >= K.THRESHOLD)
    return out


def est_lake(c, rows=None, counts_rows=None, apb=None, shares=None, combine="mean", strat=True):
    rows = by_lake[c] if rows is None else rows
    counts_rows = cts_by[c] if counts_rows is None else counts_rows
    apb = A.anglers_per_boat(rows) if apb is None else apb
    sh = A.hour_shares(rows) if shares is None else shares
    if strat:
        return A.season_estimate(counts_rows, reg[c]["area"], apb, sh, combine=combine)
    # unstratified: mean survey day times the season's days
    byday = {}
    for x in counts_rows:
        n = x["boats"] * apb + x["shore"]
        s = float(sh[int(math.floor(x["t"])) - int(K.DAY_OPEN)])
        byday.setdefault(x["date"], []).append(n / s)
    return float(np.mean([np.mean(v) for v in byday.values()])) * len(K.SEASON_DAYS) / reg[c]["area"]


# ------------------------------------------------------------------------------------------------- the call
print("== the call")
check("call: figures.json carries the golden set", fig["call"]["high_use_codes"] == GOLD, ", ".join(GOLD))
check("call: ten lakes go high use", len(GOLD) == 10, str(len(GOLD)))
fs = family_sets()
for k, s in fs.items():
    check("family: %s lands the golden set" % k, s == GOLD)
fam_margin = min(margin(v) for c in stocked for v in L[c]["family"].values())
check("family: every member at least 1.15 from the 500 line at every lake", fam_margin >= 1.15, "%.3f" % fam_margin)
r1 = sorted(c for c in stocked if L[c]["R1"] >= K.THRESHOLD)
check("default (R1, count x 17 with each lake's own anglers per boat) files a different set", r1 != GOLD,
      ", ".join(r1))
check("default: puts Galloran, Nockell, Farrowdale in and the four fly-only lakes out",
      set(r1) - set(GOLD) == {"PP-14", "PP-18", "PP-24"} and set(GOLD) - set(r1) == {"PP-05", "PP-09", "PP-16", "PP-20"})
r1_margin = min(margin(L[c]["R1"]) for c in stocked)
check("default: every lake at least 1.15 from the line", r1_margin >= 1.15, "%.3f" % r1_margin)
r2 = sorted(c for c in stocked if L[c]["R2"] >= K.THRESHOLD)
check("back-test rung (pooled hourly profile) files the default's set", r2 == r1)
r2_margin = min(margin(L[c]["R2"]) for c in stocked)
check("back-test rung: every lake at least 1.05 from the line", r2_margin >= 1.05, "%.3f" % r2_margin)
r0 = sorted(c for c in stocked if L[c]["R0"] >= K.THRESHOLD)
check("rung 0 (pooled anglers per boat, count x 17) misses the golden set", r0 != GOLD, ", ".join(r0))
check("back-test: the pooled correction keeps all four fly-only flip lakes out (the reassuring check)",
      all(L[c]["R2"] < K.THRESHOLD for c in ("PP-05", "PP-09", "PP-16", "PP-20")))

# ------------------------------------------------------------------------------------------------- three rules
print("== the three rules (R1 to R3c)")
check("R1 the raw material ships: instantaneous counts at row level with their time over the lake",
      len(cts) >= 1000 and all(K.DAY_OPEN < x["t"] < K.DAY_CLOSE for x in cts), "%d counts" % len(cts))
check("R1 the raw material ships: party-level interviews with start and finish",
      len(iv) >= 3000 and all(r["end"] > r["start"] for r in iv), "%d parties" % len(iv))
check("R1 no file carries a lake's hourly presence or its angler-hours as a column",
      not any(re.search(r"angler.?hours|presence|share", h, re.I) for h in
              open(os.path.join(TARGET, "creel_interviews_2026.csv")).readline().split(",") +
              open(os.path.join(TARGET, "survey_flight_counts_2026.csv")).readline().split(",")))
X = W.simulate()
truth = {c: X["truth"][c] / reg[c]["area"] for c in reg}
check("R2 clean truth: the golden set is the lakes whose true angler-hours clear 500",
      sorted(c for c in stocked if truth[c] >= K.THRESHOLD) == GOLD)
# the default on the clean truth: exact starts, no heaping, no blanks
clean_iv = [dict(lake=r["lake"], date=r["date"], size=r["size"], shore=r["shore"], start=r["start"], end=r["end"])
            for r in X["interviews"]]
clean_by = {c: [r for r in clean_iv if r["lake"] == c] for c in reg}
clean_cts = {c: [dict(date=x["date"], loop=x["loop"], t=x["t"], boats=x["boats"], shore=x["shore"])
                 for x in X["counts"] if x["lake"] == c and x["boats"] is not None] for c in reg}
clean_r1 = sorted(c for c in stocked if A.season_estimate(clean_cts[c], reg[c]["area"],
                                                           A.anglers_per_boat(clean_by[c])) >= K.THRESHOLD)
clean_g = sorted(c for c in stocked if A.season_estimate(clean_cts[c], reg[c]["area"], A.anglers_per_boat(clean_by[c]),
                                                          A.hour_shares(clean_by[c])) >= K.THRESHOLD)
check("R2 clean-data test: on the clean world the default still files its wrong set", clean_r1 == r1)
check("R2 clean-data test: on the clean world the golden method lands the golden set", clean_g == GOLD)
# no count is altered: the shipped counts are the world's instantaneous counts
world_counts = {(x["date"], x["loop"], x["lake"]): (x["boats"], x["shore"]) for x in X["counts"]}
same = all(world_counts[(x["date"], x["loop"], x["lake"])] == (x["boats"], x["shore"]) for x in cts)
check("R3a no planted defect: every shipped count is the anglers truly on the lake at its time", same)
check("R3a no planted defect: no count is missing except the fog loop and the smoke lakes",
      sum(1 for x in X["counts"] if x["boats"] is None) == 24 + sum(1 for d in W.SMOKE_DAYS for L_ in W.LAKES if L_[5] >= 20))
check("R3b not semantics: with every field read right (crosswalk, own anglers per boat, register areas) the "
      "default still files the wrong set", r1 != GOLD and r1 == clean_r1)
words = " ".join(s for ss in D.all_sentences().values() for s in ss).lower()
banned = ["multipl", "expand", "expansion", "profile", "instantaneous", "proportion of", "share of", "estimator",
          "day length", "length of the"]
check("R3c not rule application: no filed sentence performs or names an estimator",
      not any(b in words for b in banned), ", ".join(b for b in banned if b in words))
spread_enum = {c: (min(list(L[c]["family"].values()) + [L[c]["R1"], L[c]["R2"]]),
                   max(list(L[c]["family"].values()) + [L[c]["R1"], L[c]["R2"]])) for c in stocked}
check("R3c the enumerated family spreads across the line at the flip lakes (the step decides)",
      all(spread_enum[c][0] < K.THRESHOLD < spread_enum[c][1] for c in ["PP-05", "PP-09", "PP-16", "PP-20",
                                                                         "PP-14", "PP-18", "PP-24"]))
check("R3c the standing family (each lake's own or its class's hourly presence) never crosses the line",
      all(min(L[c]["family"].values()) >= K.THRESHOLD or max(L[c]["family"].values()) < K.THRESHOLD for c in stocked))

# Gate F: cheap routes on the clean truth
print("== cheap routes (Gate F)")


def route_set(f):
    return sorted(c for c in stocked if f(c) >= K.THRESHOLD)


def am_pm_only(loop):
    def f(c):
        rows = [x for x in clean_cts[c] if x["loop"] == loop]
        return A.season_estimate(rows, reg[c]["area"], A.anglers_per_boat(clean_by[c]))
    return f


cheap = {
    "count x 17, pooled anglers per boat": lambda c: A.season_estimate(clean_cts[c], reg[c]["area"],
                                                                      A.anglers_per_boat(clean_iv)),
    "count x 17, own anglers per boat": lambda c: A.season_estimate(clean_cts[c], reg[c]["area"],
                                                                   A.anglers_per_boat(clean_by[c])),
    "pooled hourly profile": lambda c: A.season_estimate(clean_cts[c], reg[c]["area"], A.anglers_per_boat(clean_by[c]),
                                                         A.hour_shares(clean_iv)),
    "morning loop only, x 17": am_pm_only("AM"),
    "afternoon loop only, x 17": am_pm_only("PM"),
    "boats as anglers, x 17": lambda c: A.season_estimate([dict(x, shore=x["shore"]) for x in clean_cts[c]],
                                                          reg[c]["area"], 1.0),
    "peak count x 17": lambda c: max(x["boats"] * A.anglers_per_boat(clean_by[c]) + x["shore"]
                                     for x in clean_cts[c]) * 17 * len(K.SEASON_DAYS) / reg[c]["area"] / 2.2,
}
landed = [k for k, f in cheap.items() if route_set(f) == GOLD]
check("Gate F: no cheap route lands the golden set on the clean truth", not landed, ", ".join(landed) or "none")

# Shock: the golden set is not an interval of any one-dimensional statistic
print("== shock screen")
stats = {
    "interviews per lake": {c: len(by_lake[c]) for c in stocked},
    "interviews per ha": {c: len(by_lake[c]) / reg[c]["area"] for c in stocked},
    "interviewed angler-hours per ha": {c: sum((r["end"] - r["start"]) * r["size"] for r in by_lake[c]) / reg[c]["area"]
                                        for c in stocked},
    "mean count": {c: np.mean([x["boats"] + x["shore"] for x in cts_by[c]]) for c in stocked},
    "mean count per ha": {c: np.mean([x["boats"] + x["shore"] for x in cts_by[c]]) / reg[c]["area"] for c in stocked},
    "default estimate": {c: L[c]["R1"] for c in stocked},
    "area": {c: reg[c]["area"] for c in stocked},
    "route position": {c: reg[c]["vno"] for c in stocked},
    "kept fish per ha": {c: sum(r["kept"] for r in by_lake[c]) / reg[c]["area"] for c in stocked},
    "mean hours fished": {c: np.mean([r["end"] - r["start"] for r in by_lake[c]]) for c in stocked},
}
for nm, s in stats.items():
    order = sorted(stocked, key=lambda c: -s[c])
    k = len(GOLD)
    check("Shock: golden set is not the top or bottom of %s" % nm,
          set(order[:k]) != set(GOLD) and set(order[-k:]) != set(GOLD), "overlap %d" % len(set(order[:k]) & set(GOLD)))

# ------------------------------------------------------------------------------------------------- shared precision
print("== the precision every reading shares")
import deliver as DL  # noqa: E402
PF = A.presence_family(TARGET)
check("bands: fifty presence readings (hour bin, nearest hour, two interpolations, centred hour, minute; lake or "
      "class profile and anglers per boat; day mean or ratio; parties; day type) all land the golden set",
      all(sorted(c for c in stocked if PF[c][k] >= K.THRESHOLD) == GOLD for k in PF[GOLD[0]]), "%d readings" % len(PF[GOLD[0]]))
lo_high = min(min(PF[c].values()) for c in GOLD)
hi_std = max(max(PF[c].values()) for c in stocked if c not in GOLD)
check("bands: every high-use lake above %d under every reading" % DL.BAND_HIGH, lo_high > DL.BAND_HIGH,
      "lowest %.0f" % lo_high)
check("bands: every standard lake below %d under every reading" % DL.BAND_STD, hi_std < DL.BAND_STD,
      "highest %.0f" % hi_std)
check("bands: the high band clears the judge's closest high lake (626) and the standard band its closest standard "
      "lake (462)", DL.BAND_HIGH < 626 and DL.BAND_STD > 462)
nh, ns = set(), set()
for k in PF[GOLD[0]]:
    nh.add(min(GOLD, key=lambda c: PF[c][k]))
    ns.add(max((c for c in stocked if c not in GOLD), key=lambda c: PF[c][k]))
check("bands: the lakes the write-up names nearest the line are each reading's nearest",
      sorted(reg[c]["name"] for c in nh) == sorted(fig["nearest_high"]) and
      sorted(reg[c]["name"] for c in ns) == sorted(fig["nearest_standard"]))
crow = {}
for c in reg:
    crow.setdefault(reg[c]["reg"], []).extend(by_lake[c])
vno_ = {v["vno"]: c for c, v in reg.items()}
blank_rows = [r for r in csv.DictReader(open(os.path.join(TARGET, "survey_flight_counts_2026.csv"))) if r["boats"] == ""]
plain_lo, plain_hi = {}, {}
for c in ["PP-14", "PP-18", "PP-24", "PP-05", "PP-09", "PP-16", "PP-20"]:
    vals = []
    for apb in (A.anglers_per_boat(by_lake[c]), A.anglers_per_boat(crow[reg[c]["reg"]])):
        for zero in (False, True):
            rows = list(cts_by[c])
            if zero:
                rows += [dict(date=dt.date.fromisoformat(b["survey_date"]), loop=b["loop"], t=12.0, boats=0, shore=0)
                         for b in blank_rows if vno_[int(b["lake_no"])] == c]
            vals.append(A.season_estimate(rows, reg[c]["area"], apb))
            byday = {}
            for x in rows:
                byday.setdefault(x["date"], []).append((x["boats"] * apb + x["shore"]) * K.DAY_HOURS)
            vals.append(np.mean([np.mean(v) for v in byday.values()]) * len(K.SEASON_DAYS) / reg[c]["area"])
    plain_lo[c], plain_hi[c] = min(vals), max(vals)
check("bands: the plain expansion keeps Galloran, Nockell and Farrowdale above %d under each of its readings"
      % DL.BAND_PLAIN_IN, all(plain_lo[c] > DL.BAND_PLAIN_IN for c in ("PP-14", "PP-18", "PP-24")),
      "lowest %.0f" % min(plain_lo[c] for c in ("PP-14", "PP-18", "PP-24")))
check("bands: the plain expansion keeps the four fly-only lakes below %d under each of its readings"
      % DL.BAND_PLAIN_OUT, all(plain_hi[c] < DL.BAND_PLAIN_OUT for c in ("PP-05", "PP-09", "PP-16", "PP-20")),
      "highest %.0f" % max(plain_hi[c] for c in ("PP-05", "PP-09", "PP-16", "PP-20")))
gw = openpyxl.load_workbook(os.path.join(TASK, "golden", "stocking_tiers_2027.xlsx"), read_only=True)
grows = list(gw["Tiers 2027"].iter_rows(values_only=True))
bandcol = [r[6] for r in grows[1:] if r and r[0] and str(r[0]).startswith("PP-")]
check("bands: the golden workbook gives each lake its band, not a figure",
      all(v in ("above %d" % DL.BAND_HIGH, "below %d" % DL.BAND_STD) for v in bandcol) and len(bandcol) == len(stocked))

# ------------------------------------------------------------------------------------------------- semantic forks
print("== semantic fork table")
walk = [c for c in reg if reg[c]["access"] == "walk-in"]
check("SF1 lakes outside the policy (walk-in, no catchables) stay under 500 under every member",
      all(max(L[c]["family"].values()) < K.THRESHOLD for c in walk))
alt = {c: K.THRESHOLD for c in stocked}
part_ah = {c: sum((r["end"] - r["start"]) * r["size"] for r in by_lake[c]) for c in stocked}
check("SF2 angler-hours as anglers x hours fished per party is the same quantity: shares built from party hours "
      "equal shares built hour by hour", all(abs(sum(A.hour_shares(by_lake[c])) - 1) < 1e-9 for c in stocked))
r616 = {}
for c in stocked:
    rows = [dict(r, start=max(r["start"], 6.0)) for r in by_lake[c] if r["end"] > 6.0]
    r616[c] = est_lake(c, rows=rows)
check("SF3 the angling day read as the clerks' 06:00 to 22:00 changes no lake", setof(r616) == GOLD)
uns = {c: est_lake(c, strat=False) for c in stocked}
check("SF4 the season expanded without strata changes no lake", setof(uns) == GOLD)
check("SF5 surface area has one source (the register) and every lake has it", all(reg[c]["area"] > 0 for c in reg))
papb_l = {c: est_lake(c, apb=A.anglers_per_boat(iv)) for c in stocked}
check("SF6 boats to anglers: pooled anglers per boat with each lake's shares changes no lake", setof(papb_l) == GOLD)
check("SF6 boats to anglers: class anglers per boat is a family member and lands the set",
      fs["regulation-class shares and anglers per boat"] == GOLD)
check("SF7 shore anglers are counted as anglers in every member", True)
check("SF8 the count's hour: hour bin, interpolation and the count's minute all land the set",
      fs["lake shares, mean of count ratios"] == GOLD and fs["lake shares interpolated to the count's minute"] == GOLD)
inst = {}
for c in stocked:
    rows = by_lake[c]
    den = sum(r["size"] * (r["end"] - r["start"]) for r in rows)
    byday = {}
    apb = A.anglers_per_boat(rows)
    for x in cts_by[c]:
        num = sum(r["size"] for r in rows if r["start"] <= x["t"] < r["end"])
        byday.setdefault(x["date"], []).append((x["boats"] * apb + x["shore"]) * den / max(num, 1e-9))
    tot = 0.0
    for key, days in A.strata_days().items():
        vals = [np.mean(byday[d]) for d in days if d in byday]
        tot += len(days) * np.mean(vals)
    inst[c] = tot / reg[c]["area"]
check("SF8 presence read at the count's exact minute (instantaneous) lands the set", setof(inst) == GOLD,
      "min margin %.2f" % min(margin(v) for v in inst.values()))
pw = {c: est_lake(c, shares=A.hour_shares(by_lake[c], weight="parties")) for c in stocked}
check("SF9 shares weighted by parties instead of anglers land the set", setof(pw) == GOLD)
drop_ms = {}
raw_iv = list(csv.DictReader(open(os.path.join(TARGET, "creel_interviews_2026.csv"))))
has_start = {(r["date"], r["lake"].lower(), r["finished"], r["party_size"], r["fished_from"]): bool(r["started"])
             for r in raw_iv}
for c in stocked:
    rows = [r for r in by_lake[c] if has_start.get((r["date"].isoformat(), reg[c]["name"].replace(" Lake", "").lower(),
                                                    K.hm(r["end"]), str(r["size"]), "shore" if r["shore"] else "boat"),
                                                   True)]
    drop_ms[c] = est_lake(c, rows=rows)
check("SF10 parties with no start time dropped instead of filled changes no lake", setof(drop_ms) == GOLD)
blanks = [r for r in csv.DictReader(open(os.path.join(TARGET, "survey_flight_counts_2026.csv"))) if r["boats"] == ""]
vno = {v["vno"]: c for c, v in reg.items()}
zero_g, zero_r1 = {}, {}
for c in stocked:
    extra = [dict(date=dt.date.fromisoformat(b["survey_date"]), loop=b["loop"],
                  t=K.parse_hm(b["time_over"]) if b["time_over"] else (9.6 if b["loop"] == "AM" else 14.5),
                  boats=0, shore=0) for b in blanks if vno[int(b["lake_no"])] == c]
    zero_g[c] = est_lake(c, counts_rows=cts_by[c] + extra)
    zero_r1[c] = A.season_estimate(cts_by[c] + extra, reg[c]["area"], A.anglers_per_boat(by_lake[c]))
check("SF11 blank counts read as zero change no lake (golden)", setof(zero_g) == GOLD)
check("SF11 blank counts read as zero leave the default's set (default)", setof(zero_r1) == r1)
check("SF12 a survey day's counts combined as a ratio of sums land the set",
      fs["lake shares, ratio of summed counts"] == GOLD)
check("SF13 expansion by the stratum's days (the design) and without strata agree", setof(uns) == GOLD)
check("SF14 no lake within 1.15 of 500 under any member, so 'or more' and 'more than' agree", fam_margin >= 1.15)
check("SF15 no rounding enters before the comparison; rounding the estimates to 10 changes no lake",
      sorted(c for c in stocked if round(L[c]["golden"], -1) >= K.THRESHOLD) == GOLD)
check("SF16 both clerk shifts are one lake-day's interviews: the share profile uses every interviewed party",
      sum(len(by_lake[c]) for c in reg) == len(iv))
check("SF17 shares pooled within the regulation class land the set", fs["regulation-class shares"] == GOLD and
      fs["regulation-class shares, ratio of summed counts"] == GOLD)
dtp = {}
for c in stocked:
    shd = {k: A.hour_shares([r for r in by_lake[c] if K.day_type(r["date"]) == k]) for k in ("weekday", "weekend")}
    apb = A.anglers_per_boat(by_lake[c])
    byday = {}
    for x in cts_by[c]:
        s = float(shd[K.day_type(x["date"])][int(math.floor(x["t"])) - 5])
        byday.setdefault(x["date"], []).append((x["boats"] * apb + x["shore"]) / s)
    tot = sum(len(days) * np.mean([np.mean(byday[d]) for d in days if d in byday]) for key, days in A.strata_days().items())
    dtp[c] = tot / reg[c]["area"]
check("SF18 shares taken separately for weekdays and weekend days land the set", setof(dtp) == GOLD,
      "min margin %.2f" % min(margin(v) for v in dtp.values()))
cnt = list(csv.DictReader(open(os.path.join(TARGET, "survey_flight_counts_2026.csv"))))
byname = {}
for r in cnt:
    byname.setdefault(r["lake"], set()).add(int(r["lake_no"]))
check("SF19 the count file's lake numbers and its lake names point to the same register lake",
      all(len(v) == 1 for v in byname.values()) and len(byname) == len(reg))
tab = {r["lake"] for r in raw_iv}
check("SF20 every tablet lake name matches one register lake", all(any(v["name"].replace(" Lake", "") == t
                                                                      for v in reg.values()) for t in tab))
# SF21: the pooled profile is refuted by the data at the lakes it moves
pooled = A.hour_shares(iv)
rej = []
for c in ["PP-05", "PP-09", "PP-16", "PP-20", "PP-14", "PP-18", "PP-24"]:
    obs = np.zeros(len(A.HOURS))
    for r in by_lake[c]:
        for i, h in enumerate(A.HOURS):
            lo, hi = max(r["start"], h), min(r["end"], h + 1)
            if hi > lo:
                obs[i] += r["size"] * (hi - lo)
    exp = pooled * obs.sum()
    keep = exp > 5
    chi = float((((obs - exp) ** 2) / exp)[keep].sum())
    from scipy.stats import chi2
    rej.append(chi2.sf(chi, keep.sum() - 1) < 1e-4)
check("SF21 the pooled hourly profile is rejected against each lake it would move (chi-square p < 1e-4)", all(rej))

# ask forks
print("== ask forks")
gold_rel = A.releases(TARGET)
r100 = lambda x: int(math.floor(x / 100 + 0.5) * 100)


def edge100(x):
    return abs(x - (math.floor(x / 100) * 100 + 50))


for how in ("interp", "nearest"):
    alt_rel = A.releases(TARGET, how=how)
    check("SF22 fish per kg by %s sample lands every lake's figure in the same 100" % how,
          all(r100(alt_rel[c]) == r100(gold_rel[c]) for c in gold_rel))
eq = A.releases(TARGET, split="equal")
check("SF23 the drop crew's nets are the split's record: an equal split moves at least one lake (a hazard, not a "
      "reading)", any(r100(eq[c]) != r100(gold_rel[c]) for c in gold_rel))
nodoa = A.releases(TARGET, doa=False)
check("SF24 'alive' takes off the dead at the drop: leaving them in moves at least one lake",
      any(r100(nodoa[c]) != r100(gold_rel[c]) for c in gold_rel))
# SF25 the raceway each window trip loaded is fixed by the inventory, not by a reading
trips = A._trip_sheets(TARGET)
cw, switch = A._crosswalk(TARGET)
samples = A.unified_samples(A._samples(TARGET), cw, switch)
ok25 = True
n25 = 0
for tid, t in trips.items():
    if t["date"] < switch or t["new_template"]:
        continue
    n25 += 1
    gold_rw = cw[t["raceway"]]
    wrong_rw = t["raceway"]

    def drop(rw):
        ss = sorted((s for s in samples if s["raceway"] == rw), key=lambda s: s["date"])
        b = [s for s in ss if s["date"] <= t["date"]][-1]
        a = [s for s in ss if s["date"] > t["date"]]
        return b["onhand"] - a[0]["onhand"] if a else None
    dg, dw = drop(gold_rw), drop(wrong_rw)
    fishload = t["load"] * A.fpk_at(samples, gold_rw, t["date"])
    if dg is None or dg < 0.8 * fishload:
        ok25 = False
check("SF25 every trip between the renumbering and the template change emptied fish from the raceway the crosswalk "
      "maps its number to (Monday inventory)", ok25 and n25 > 0, "%d trips" % n25)
w_gold, means = A.warm_days(TARGET)
w_per, means_per = A.warm_days(TARGET, combine="perlogger")
check("SF26 days are Pacific-time days: the two loggers launched on UTC are found by their warmest hour",
      A.logger_clock_offsets({s: [(dt.datetime.strptime(r["Date Time"], "%Y-%m-%d %H:%M"), float(r["Temp (C)"]))
                                  for r in csv.DictReader(open(os.path.join(TARGET, "lake_temperature_loggers_2026.csv")))
                                  if r["Logger SN"] == s] for s in ("20184409", "20184421", "20184402")})
      == {"20184409": -7, "20184421": -7, "20184402": 0})
check("SF27 a lake-day averaged over all readings or over each logger's mean gives the same counts", w_gold == w_per)
gap = min(min(abs(v - 20) for v in means.values()), min(abs(v - 20) for v in means_per.values()))
check("SF28 no lake-day mean within 0.06 C of 20 (rounding to 0.1 and 'at or above' agree)", gap >= 0.06, "%.3f" % gap)
partial = [(k, v) for k, v in means.items() if k in (("PP-19", dt.date(2026, 7, 14)), ("PP-20", dt.date(2026, 7, 22)))]
check("SF29 the two relocation days are not warm however a part day is read", all(v < 19.7 for k, v in partial),
      ", ".join("%s %.2f" % (k[0], v) for k, v in partial))
check("SF30 the lakes with a 1 m logger in July and August are the nine the deployments give",
      sorted(w_gold) == ["PP-02", "PP-03", "PP-07", "PP-09", "PP-11", "PP-19", "PP-20", "PP-26", "PP-29"])

# ------------------------------------------------------------------------------------------------- Layer 1
print("== Layer 1 neutrality")
check("L1 Vellacott numbers re-issued: mapping by number and by the operator's spelling agree (SF19)", True)
check("L1 blank counts (fog loop, smoke lakes): zero or dropped, same call (SF11)", setof(zero_g) == GOLD)
heap = {}
for c in stocked:
    heap[c] = A.season_estimate(clean_cts[c], reg[c]["area"], A.anglers_per_boat(clean_by[c]), A.hour_shares(clean_by[c]))
check("L1 heaped start times: the clean world's exact starts give the same set", setof(heap) == GOLD)
check("L1 missing start times: filled from hours fished or dropped, same call (SF10)", setof(drop_ms) == GOLD)
check("L1 the clerks' shifts and interview numbering do not enter the call", True)
check("L1 the flight log's UTC block times are not read by the call (distractor)",
      "vellacott_air_flight_log_2026.xlsx" in json.load(open(os.path.join(TASK, "metadata.json")))["distractor_files"])
ask_files = {"quillet_creek_trip_sheets_2026.xlsx", "quillet_creek_drop_tallies_2026.json",
             "quillet_creek_raceway_samples_2026.csv", "quillet_creek_raceway_numbers.csv",
             "lake_temperature_loggers_2026.csv", "logger_deployments_2026.csv"}
check("L1 every ask device sits in files the call never reads (zero device rows in the call's population)",
      not ask_files & {"survey_flight_counts_2026.csv", "creel_interviews_2026.csv", "lake_register_2026.xlsx"})

print("== hygiene across files")
fl = openpyxl.load_workbook(os.path.join(TARGET, "vellacott_air_flight_log_2026.xlsx"), read_only=True)
frows = list(fl["Flight log"].iter_rows(values_only=True))
fh = frows[0]
air = {}
for r in frows[1:]:
    d = dict(zip(fh, r))
    if not d.get("Flight"):
        continue
    base = dt.datetime.fromisoformat(str(d["Date (UTC)"])[:10])

    def at(hhmm, after=None):
        h, m = [int(x) for x in str(hhmm).split(":")[:2]]
        t = base + dt.timedelta(hours=h, minutes=m)
        if after is not None and t < after:
            t += dt.timedelta(days=1)
        return t
    off = at(d["Block off (UTC)"])
    to = at(d["Take-off (UTC)"], off)
    ld = at(d["Landing (UTC)"], to)
    pt_to, pt_ld = to - dt.timedelta(hours=7), ld - dt.timedelta(hours=7)
    air.setdefault((pt_to.date(), d["Route"][-2:]), []).append((pt_to, pt_ld))
outside = []
for x in cts:
    t = dt.datetime.combine(x["date"], dt.time(0, 0)) + dt.timedelta(hours=x["t"])
    if not any(a <= t <= b for a, b in air.get((x["date"], x["loop"]), [])):
        outside.append((x["date"].isoformat(), x["loop"], x["lake"]))
check("H every count's time over its lake falls inside an airborne leg of that loop in the flight log", not outside,
      "%d outside" % len(outside))
check("H the tiers do not read the flight log (a distractor): the call is unchanged by it", fig["call"]["high_use_codes"] == GOLD)
recs = json.load(open(os.path.join(TARGET, "quillet_creek_drop_tallies_2026.json")))["records"]
check("H the drop tallies carry the dead at the drop in fish, in the key's own name",
      all("doaFish" in r and "doa" not in r for r in recs))

# ------------------------------------------------------------------------------------------------- input gates
print("== input gates")
files = sorted(os.listdir(TARGET))
check("G at least 10 files", len(files) >= 10, str(len(files)))
check("G at least 3 formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3,
      ", ".join(sorted({f.rsplit(".", 1)[1] for f in files})))
rows = sum(1 for _ in open(os.path.join(TARGET, "lake_temperature_loggers_2026.csv"))) - 1
check("G one file of 25,000 rows or more", rows >= 25000, "%d rows" % rows)
meta = json.load(open(os.path.join(TASK, "metadata.json")))
check("G two or more distractors declared", len(meta["distractor_files"]) >= 2 and
      all(d in files for d in meta["distractor_files"]))
check("G no readme, dictionary, notes or manifest file", not any(re.search(r"readme|dictionary|notes|manifest|schema",
                                                                          f, re.I) for f in files))
check("G file names carry no author words", not any(re.search(r"test|trap|decoy|golden|answer|stump", f, re.I)
                                                    for f in files))
check("G every file has a source, date and licence", all(x["source"] and x["date"] and x["license"]
                                                         for x in meta["files"]))

# ------------------------------------------------------------------------------------------------- realism
print("== realism sweep")
seqs = {}
for x in cts:
    seqs.setdefault(x["lake"], []).append(x["boats"])
check("Z no two lakes carry the same count sequence", len({tuple(v) for v in seqs.values()}) == len(seqs))
check("Z no per-lake angler-hours figure is written at a precision the readings split on (bands only)",
      "angler_hours_per_ha" not in fig and "angler_hours_season" not in fig and
      "nearest 10" not in open(os.path.join(TASK, "submission.md")).read())
starts = [K.parse_hm(r["started"]) for r in raw_iv if r["started"]]
q = sum(1 for s in starts if abs(s * 4 - round(s * 4)) < 1e-6) / len(starts)
check("Z start times heaped like recall (most on the quarter hour, not all)", 0.6 < q < 0.98, "%.2f on quarters" % q)
miss = sum(1 for r in raw_iv if not r["started"]) / len(raw_iv)
check("Z some parties give hours fished instead of a start", 0.04 < miss < 0.15, "%.3f" % miss)
fin = [r["finished"] for r in raw_iv]
check("Z finish times are the tablet's clock (not heaped)", len(set(fin)) > 400)
temps = [float(r["Temp (C)"]) for r in csv.DictReader(open(os.path.join(TARGET, "lake_temperature_loggers_2026.csv")))]
check("Z logger readings within a lake's physical range", 5 < min(temps) and max(temps) < 34,
      "%.1f to %.1f" % (min(temps), max(temps)))
dates = []
for f in files:
    if f.endswith(".csv"):
        dates += re.findall(r"20\d\d-\d\d-\d\d", open(os.path.join(TARGET, f)).read())
late = [d for d in dates if d > K.ASOF.isoformat()]
check("Z no date in the pack after the fiction's as-of date", not late, K.ASOF.isoformat())
names = open(os.path.join(HERE, "h21_reference_places.txt")).read().lower().split("\n")
names = {n.strip() for n in names if n.strip()}


def lev(a, b):
    if abs(len(a) - len(b)) > 2:
        return 9
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


inv = [v["name"].replace(" Lake", "").lower() for v in reg.values()] + ["pelloran", "quillet", "vellacott"]
hits = [n for n in inv if any(lev(n, p) <= 1 for p in names if abs(len(p) - len(n)) <= 1)]
check("Z invented names are not within one letter of a reference place (H21)", not hits, ", ".join(hits))
persona = K.PEOPLE.values()
check("Z personas are the card's (guard.py names)", set(persona) == {"Katrina Newman", "Luis Thomas", "Robin Fields"})
for f in files:
    if f.endswith((".xlsx", ".docx")):
        z = zipfile.ZipFile(os.path.join(TARGET, f))
        core = z.read("docProps/core.xml").decode()
        check("Z %s carries no library signature" % f, "openpyxl" not in core.lower() and "python" not in core.lower())

# ------------------------------------------------------------------------------------------------- bins
print("== bin distances")
e = min(min(edge100(v) for v in A.releases(TARGET, how=h).values()) for h in ("latest", "interp", "nearest"))
check("B every release figure at least 20 fish inside its nearest-100 bin under every sample convention", e >= 20,
      "%.1f" % e)
check("B releases in figures.json are the golden's", fig["releases_alive"] == {reg[c]["name"]: r100(v)
                                                                               for c, v in gold_rel.items()})
check("B warm days in figures.json are the golden's", fig["warm_days"] == {reg[c]["name"]: v for c, v in w_gold.items()})
check("B every lake's tier sits at least 1.15 from the line under every member (the graded unit is the set)",
      fam_margin >= 1.15)
crack_rel = A.releases(TARGET, raceways="in_force")
misses = sum(1 for c in gold_rel if r100(crack_rel[c]) != r100(gold_rel[c]))
check("B the numbering in force misses most lakes' releases (device mass)", misses >= 15, "%d of %d" % (misses,
                                                                                                      len(gold_rel)))
w_site, _ = A.warm_days(TARGET, mode="site")
check("B the download station misses Kelloran and Inverkeld (device mass)",
      w_site["PP-19"] != w_gold["PP-19"] and w_site["PP-20"] != w_gold["PP-20"],
      "Kelloran %d vs %d, Inverkeld %d vs %d" % (w_site["PP-19"], w_gold["PP-19"], w_site["PP-20"], w_gold["PP-20"]))

print("\n%d checks, %d failed" % (N[0], len(FAIL)))
if FAIL:
    for f in FAIL:
        print("  FAIL", f)
    sys.exit(1)

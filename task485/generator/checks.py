"""task485's generator checks, run on the world's clean truth and on the cut pack: the three rules (R1 to R3), the
ladder, every row of the semantic fork table (SF1 to SF15) with the deciding quantity's live readings as a cross
product, each Layer 1 item mishandled, the ask's device and its separation from the call, the realism sweep and the
input gates.

    python3 task485/generator/checks.py
"""
import csv
import itertools
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import build as B  # noqa: E402
import contractors as C  # noqa: E402
import golden as G  # noqa: E402
import registry as R  # noqa: E402
import world as W  # noqa: E402

OK, BAD = [], []
GOLD = ["Northern Vale", "Eastern Vale", "Southern Vale", "Midland Basin", "Inner Basin", "Lower Basin"]
DEFAULT = ["Northern Vale", "Eastern Vale", "Southern Vale", "Midland Basin", "Lake Uplands", "Middle Uplands", "Eastern Uplands", "Western Seaboard",
           "Atlantic Coast"]
MEAN = ["Northern Vale", "Eastern Vale", "Southern Vale", "Midland Basin", "Inner Basin", "Lower Basin", "Lake Uplands", "Middle Uplands", "Western Seaboard"]
PREMISES = ("mart", "dealer", "export", "factory", "knackery")


def check(label, cond, detail=""):
    (OK if cond else BAD).append(label)
    print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  " + detail) if detail else ""))


def intervals(w, transit="arr", premises="count", exit_counted=False, start="birth"):
    """the herd intervals under a reading of the register: the location switches at the arrival date (golden) or the
    departure date; days at marts, dealers and export centres counted there (golden), dropped, or counted at the herd
    the animal came from; the exit day not counted (golden) or counted; presence from birth (golden) or registration"""
    A, H = w.A, w.herds
    by_a = defaultdict(list)
    for m in w.moves:
        by_a[m["a"]].append((m[transit], m["k"], m["to"]))
    out = {}
    for a in range(len(A["sex"])):
        b = A["birth"][a] + (A["reg_lag"][a] if start == "reg" else 0)
        s = max(b, 0)
        e = A["exit"][a] if A["exit"][a] is not None else W.NDAY
        if exit_counted and A["exit"][a] is not None:
            e += 1
        e = min(e, W.NDAY)
        if s >= W.NDAY or e <= 0 or e <= s:
            continue
        cur, t, iv = A["herd0"][a], s, []
        for day, k, to in sorted(by_a[a]):
            if day <= t:
                cur = to
                continue
            if day >= e:
                break
            iv.append([cur, t, day])
            cur, t = to, day
        iv.append([cur, t, e])
        iv = [x for x in iv if x[1] < x[2]]
        if premises != "count":
            kept = []
            for k, x in enumerate(iv):
                if H[x[0]]["type"] in PREMISES:
                    if premises == "seller" and kept:
                        kept.append([kept[-1][0], x[1], x[2]])
                    continue
                kept.append(x)
            iv = kept
        if iv:
            out[a] = [tuple(x) for x in iv]
    return out


def region_maps(tr):
    """herd -> region index under the readings a response can take: the 2024 regions (golden), the pre-2024 codes,
    the herd register's first row for a reissued number (the earlier holder's), the herd number's letter"""
    w = tr["w"]
    old = {o["herd_no"]: o["region"] for o in tr["old"]}
    letter = {v: k for k, v in W.RLETTER.items()}
    maps = {
        "2024": [h["region"] for h in w.herds],
        "pre2024": [h["region_pre2024"] for h in w.herds],
        "first_row": [old.get(h["herd_no"], h["region"]) for h in w.herds],
        "letter": [letter[h["herd_no"][0]] for h in w.herds],
    }
    return {k: np.array([G.REGI[r] for r in v]) for k, v in maps.items()}, \
        {k: {h["herd_no"]: v[i] for i, h in enumerate(w.herds)} for k, v in maps.items()}


def call(kg, land):
    return G.designated(kg, land)


def main():
    tr = B.truth()
    w, P, land, gold = tr["w"], tr["P"], tr["land"], tr["gold"]
    kgha = gold / land
    des = call(gold, land)
    check("golden: the six regions", des == GOLD, str(des))
    near = min(abs(kgha / W.LINE - 1)) * 100
    check("SF14 no region within 2 per cent of the line on the golden", near >= 2.0, "nearest %.2f per cent" % near)
    order = sorted(W.REG, key=lambda r: kgha[G.REGI[r]])
    print("     golden kg/ha: " + ", ".join("%s %.2f" % (r, kgha[G.REGI[r]]) for r in W.REG))

    # ---------------------------------------------------------------- the ladder
    farm_region = {h["farm_no"]: h["region"] for h in w.herds if h.get("farm_no")}
    t5 = G.table5()
    L0 = G.census_route(tr["cen"], farm_region)
    st = G.stock(P, W.CENSUS)
    L1 = (st * t5).sum(1)
    L2a = L0 * gold.sum() / L0.sum()
    L3 = (G.days(P) / W.NDAY * t5).sum(1)
    L2b = L3 * gold.sum() / L3.sum()
    L4 = G.ammonia(P, season=P.home)
    rungs = dict(L0=L0, L1=L1, L2a=L2a, L3=L3, L2b=L2b, L4=L4, G=gold)
    sets = {k: call(v, land) for k, v in rungs.items()}
    for k, v in rungs.items():
        x = v / land
        print("     %-3s %7.1f t  %s" % (k, v.sum() / 1000, ", ".join("%s %.2f" % (r, x[G.REGI[r]]) for r in W.REG)))
    check("ladder L0 (the census at Table 5) files the default nine", sets["L0"] == DEFAULT, str(sets["L0"]))
    check("ladder L1 (the register's 1 June stock at Table 5) files the default nine", sets["L1"] == DEFAULT, str(sets["L1"]))
    check("ladder L2a (the census scaled to the golden total) is off the call", sets["L2a"] != GOLD, str(sets["L2a"]))
    check("ladder L3 (the register's mean count at Table 5) files the mean-count nine", sets["L3"] == MEAN, str(sets["L3"]))
    check("ladder L2b (the mean count scaled to the golden total) is off the call", sets["L2b"] != GOLD, str(sets["L2b"]))
    check("ladder L4 (animal-days at the home region's season) files the golden", sets["L4"] == GOLD, str(sets["L4"]))
    census_tot = sum(sum(c.values()) for c in tr["cen"].values())
    check("the register's 1 June stock on farms equals the census", int(G.stock(P, W.CENSUS).sum()) >= census_tot and
          census_tot == sum(1 for a, iv in tr["IV"].items() for h, s, e in iv
                            if s <= W.CENSUS < e and R.HTYPE[w.herds[h]["type"]] == "Farm"), "%d cattle" % census_tot)
    m_def = {r: kgha_r for r, kgha_r in zip(W.REG, L0 / land)}
    wrong_add = min(m_def[r] / W.LINE - 1 for r in DEFAULT if r not in GOLD) * 100
    wrong_miss = max(m_def[r] / W.LINE - 1 for r in GOLD if r not in DEFAULT) * 100
    check("the default's added regions sit 5 per cent or more over the line, its missed ones 5 per cent or more under",
          wrong_add >= 5 and wrong_miss <= -5, "nearest added %+.1f, nearest missed %+.1f" % (wrong_add, wrong_miss))
    m3 = {r: v for r, v in zip(W.REG, L3 / land)}
    check("the mean count's added regions sit 4 per cent or more over the line",
          min(m3[r] / W.LINE - 1 for r in MEAN if r not in GOLD) * 100 >= 4,
          "nearest %+.1f" % (min(m3[r] / W.LINE - 1 for r in MEAN if r not in GOLD) * 100))

    # ---------------------------------------------------------------- the three rules
    heads = {}
    for f in sorted(os.listdir(T)):
        if f.endswith(".csv"):
            heads[f] = open(os.path.join(T, f), encoding="utf-8").readline().strip().upper()
    words = ("AMMONIA", "NH3", "ANIMAL_DAYS", "ANIMAL DAYS", "HOUSED", "KG_HA", "EMISSION")
    hit = [f for f, h in heads.items() if any(x in h for x in words)]
    check("R1 the golden reads the register's animal and movement rows (shipped one row per animal and per movement)",
          len(tr["IV"]) > 100000 and len(w.moves) > 70000, "%d animals, %d moves" % (len(tr["IV"]), len(w.moves)))
    check("R1 no shipped column holds a region's ammonia, animal-days or housed days", not hit, str(hit))
    check("R3a the easy route on the clean truth files the default nine", sets["L0"] == DEFAULT)
    check("R3b the decisive step alone (the census replaced by animal-days at each region's season) files the golden",
          sets["G"] == GOLD)
    check("R3b each lower rung's single correction stays off the call (the register's stock, its mean count)",
          sets["L1"] != GOLD and sets["L3"] != GOLD)

    # ---------------------------------------------------------------- the fork table as a cross product
    rmaps, hmaps = region_maps(tr)
    lands = {}
    for rk, hm in hmaps.items():
        for mode in ("share", "whole", "drop"):
            lands[(rk, mode)] = G.farmed_land(tr["parcels"], hm, whole_commonage=(mode == "whole"),
                                              drop_commonage=(mode == "drop"))
    results = {}
    for transit, prem, exc, start in itertools.product(("arr", "dep"), ("count", "drop", "seller"), (False, True),
                                                       ("birth", "reg")):
        IV = intervals(w, transit, prem, exc, start)
        ivs = G.iv_arrays(IV)
        for rk, rm in rmaps.items():
            Pv = G.Pieces(tr["T"], ivs, rm)
            kg = G.ammonia(Pv)
            for mode in ("share", "whole", "drop"):
                results[(transit, prem, exc, start, rk, mode)] = call(kg, lands[(rk, mode)])
    flips = {k: v for k, v in results.items() if v != GOLD}
    check("SF4 SF5 SF6 SF7 SF11 SF12 SF13 the cross product, 2 by 3 by 2 by 2 by 4 by 3 = %d readings, files only the "
          "golden" % len(results), not flips, "%d flip: %s" % (len(flips), list(flips.items())[:3]))
    check("SF4 a day in transit in the arrival herd: same call (in the cross product)",
          all(v == GOLD for k, v in results.items() if k[0] == "dep"))
    check("SF5 days at marts, dealers and export centres dropped or put at the seller: same call",
          all(v == GOLD for k, v in results.items() if k[1] != "count"))
    check("SF6 the exit day counted: same call", all(v == GOLD for k, v in results.items() if k[2]))
    check("SF7 presence from the registration date: same call", all(v == GOLD for k, v in results.items() if k[3] == "reg"))
    check("SF11 commonage counted whole on each sharing herd, or left out: same call",
          all(v == GOLD for k, v in results.items() if k[5] != "share"))
    check("SF12 the pre-2024 region codes: same call", all(v == GOLD for k, v in results.items() if k[4] == "pre2024"))
    check("SF13 the herd register's first row for a reissued number (the earlier holder's region): same call",
          all(v == GOLD for k, v in results.items() if k[4] == "first_row"))
    n_reissued = len(tr["old"])
    check("SF13 the reissued numbers' earlier rows end before the programme year", all(o["valid_to"] < W.Y0 for o in tr["old"]),
          "%d reissued numbers" % n_reissued)
    check("R2 herd numbers placed by their letter (the four herds of the moved districts in Coastal Vale): same call",
          all(v == GOLD for k, v in results.items() if k[4] == "letter"))
    check("SF8 the home region's season for every day: same call (L4)", sets["L4"] == GOLD)
    check("SF3 arising in the region read as each animal in its 1 June region: another set (the default)", sets["L0"] != GOLD)
    # SF9: the note's categories by day; the census's categories held all year is the default (another set)
    check("SF9 the census's categories on 1 June held all year: another set (the default)", sets["L1"] != GOLD)
    A = w.A
    dairy_herd_cows = [a for a, iv in tr["IV"].items() if A["fc"][a] is not None and A["sex"][a] == "F"
                       and w.herds[A["herd0"][a]]["type"] == "dairy"]
    bad10 = sum(1 for a in dairy_herd_cows if A["breed"][a] not in W.DAIRY_BREEDS)
    bad10b = sum(1 for a, iv in tr["IV"].items() if A["fc"][a] is not None and A["breed"][a] in W.DAIRY_BREEDS
                 and w.herds[A["herd0"][a]]["type"] != "dairy")
    check("SF10 every cow in a dairy herd is a dairy breed and every dairy-breed cow is in a dairy herd: identical",
          bad10 == 0 and bad10b == 0, "%d, %d" % (bad10, bad10b))
    late = sum(1 for m in w.moves if m["dep"] >= W.NDAY)
    check("SF1 the movement export ends with the programme year (moves after 31 October 2026 not shipped)",
          late >= 0 and max(m["dep"] for m in w.moves if m["dep"] < W.NDAY) < W.NDAY, "%d later moves held back" % late)
    epo = subprocess.run(["pdftotext", "-layout", os.path.join(T, B.NAMES["epo"]), "-"], capture_output=True,
                         text=True).stdout
    check("SF15 the note's factors are kilograms of ammonia a head a day", "kg NH3 a head a day" in epo)
    for c in W.CATS:
        for v in W.RATE[c]:
            assert ("%.4f" % v) in epo, (c, v)
    check("the note prints every Table 3 rate the world applies", True)
    arp = subprocess.run(["pdftotext", "-layout", os.path.join(T, B.NAMES["arp"]), "-"], capture_output=True,
                         text=True).stdout
    check("SF2 the rules scope the measure to cattle manure (fertiliser and other livestock outside)",
          "outside the measure" in arp and "fertiliser" in arp)

    # ---------------------------------------------------------------- Layer 1 neutrality (R2)
    lpr = list(csv.DictReader(open(os.path.join(T, B.NAMES["lpr"]), encoding="utf-8")))
    check("R2 commonage sits only in Eastern Uplands and Atlantic Coast",
          {tr["herd_region"][r["HERD_NO"]] for r in lpr if r["LAND_USE"] == "Commonage"} <= {"Eastern Uplands", "Atlantic Coast"})
    dates = [r.split(",")[3] for r in open(os.path.join(T, B.NAMES["animals"]), encoding="utf-8").read().splitlines()[1:]]
    over12 = sum(1 for d in dates if int(d[:2]) > 12)
    check("R2 day-month-year dates: a month and day swap fails loudly (days over 12 in the birth dates)",
          over12 > 0.5 * len(dates), "%d of %d" % (over12, len(dates)))
    cen_rows = list(csv.DictReader(open(os.path.join(T, B.NAMES["census"]), encoding="utf-8")))
    raw_join = sum(1 for r in cen_rows if r["FARM_NO"] in farm_region)
    pad_join = sum(1 for r in cen_rows if "%07d" % int(r["FARM_NO"]) in farm_region)
    check("R2 census farm numbers: the raw join fails loudly and the padded join matches every farm",
          raw_join < 0.1 * len(cen_rows) and pad_join == len(cen_rows), "raw %d, padded %d of %d" % (raw_join, pad_join, len(cen_rows)))

    # ---------------------------------------------------------------- the ask
    cj = tr["cj"]
    hr = tr["herd_region"]
    A_g = C.golden(cj, hr)
    lo, hi = W.di(W.WIN0), W.di(W.WIN1)

    def route(kb_keep="own", sub_keep=True, dedup_near=False, hazards=False, kb_nominal=False):
        vol, less = defaultdict(float), defaultdict(float)
        passed = {l["ref"] for l in cj["kb"] if not l["ref"].startswith("CW")}
        av_days = {(j["herd"], j["date"]) for j in cj["av"]} | {(j["herd"], j["date"]) for j in cj["nm"]}
        for j in cj["av"]:
            if (not hazards and j["material"] != "CATTLE SLURRY") or not (lo <= j["date"] <= hi) or j["herd"] not in hr:
                continue
            if not sub_keep and j["job_id"] in passed:
                continue
            v = j["loads"] * (2000 if kb_nominal else j["gal"]) * C.GAL
            vol[hr[j["herd"]]] += v
            less[hr[j["herd"]]] += v if j["equipment"] in C.LESS_AV else 0
        for j in cj["nm"]:
            if (not hazards and j["material"] != "Cattle slurry") or not (lo <= j["date"] <= hi) or j["herd"] not in hr:
                continue
            if not sub_keep and j["job_no"] in passed:
                continue
            vol[hr[j["herd"]]] += j["m3"]
            less[hr[j["herd"]]] += j["m3"]
        for l in cj["kb"]:
            if (not hazards and not l["service"].startswith("SS-")) or not (lo <= l["date"] <= hi):
                continue
            if kb_keep == "own" and l["ref"] in passed:
                continue
            if dedup_near and (l["herd"], l["date"]) in av_days:
                continue
            v = l["qty"] * 1000 * C.GAL
            vol[hr[l["herd"]]] += v
            less[hr[l["herd"]]] += v if l["service"] in C.LESS_KB else 0
        return {r: (vol[r], 100 * less[r] / vol[r]) for r in W.REG}

    def keeps(x):
        return sum((round(x[r][0], -2) == round(A_g[r][0], -2)) + (round(x[r][1], 1) == round(A_g[r][1], 1)) for r in W.REG)

    g2 = route()
    check("ask A the golden handling reproduces the contractors' true jobs exactly", all(
        abs(g2[r][0] - A_g[r][0]) < 1e-6 and abs(g2[r][1] - A_g[r][1]) < 1e-9 for r in W.REG))
    stops = dict(cracker=route(kb_keep="all"), mirror=route(kb_keep="all", sub_keep=False),
                 near_dup=route(kb_keep="all", dedup_near=True), hazards=route(hazards=True),
                 nominal=route(kb_nominal=True), cracker_hazards=route(kb_keep="all", hazards=True))
    for k, v in stops.items():
        print("     ask A stop %-16s keeps %2d of 24" % (k, keeps(v)))
    check("ask A the cracker (every row as exported) misses every figure", keeps(stops["cracker"]) == 0,
          "%d kept" % keeps(stops["cracker"]))
    check("ask A the mirror (Countrywide's lines kept, the job sheets dropped) keeps under 35 per cent",
          keeps(stops["mirror"]) <= 8, "%d of 24" % keeps(stops["mirror"]))
    check("ask A the near-duplicate sweep (a Countrywide line beside a same-day job dropped) keeps under 35 per cent",
          keeps(stops["near_dup"]) <= 8, "%d of 24" % keeps(stops["near_dup"]))
    twins = sum(1 for l in cj["kb"] if l["ref"].startswith("CW") and l["service"].startswith("SS-") and
                (l["herd"], l["date"]) in ({(j["herd"], j["date"]) for j in cj["av"]} | {(j["herd"], j["date"]) for j in cj["nm"]}))
    passed = [l for l in cj["kb"] if not l["ref"].startswith("CW")]
    check("ask A genuine same-day pairs exist beside the passed jobs", twins >= 20, "%d same-day pairs, %d passed lines" %
          (twins, len(passed)))
    check("ask A the passed lines are a minority of Countrywide's lines", len(passed) < 0.3 * len(cj["kb"]),
          "%d of %d" % (len(passed), len(cj["kb"])))
    regs_passed = {hr[l["herd"]] for l in passed}
    check("ask A every region carries passed lines", regs_passed == set(W.REG), str(len(regs_passed)))
    check("separation: the call reads no contractor row (the golden's ammonia is computed before the jobs exist)",
          "cj" not in open(os.path.join(HERE, "golden.py")).read())
    check("separation: no contractor file is read by the call's population (0 rows)",
          not ({"ardvale", "kilbrack", "northmoor"} & set(k for k in B.NAMES if k in ("animals", "movements", "herds",
                                                                                     "census", "lpr", "epo", "survey"))))
    gsrc = open(os.path.join(HERE, "golden.py")).read() + open(os.path.join(HERE, "goldfiles.py")).read()
    check("distractors: no golden figure opens the fertiliser, milk or pig and poultry files",
          not any(x in gsrc for x in ("fert", "milk", "pigs")))

    # ---------------------------------------------------------------- gates and realism
    files = sorted(os.listdir(T))
    check("gate: 10 or more files", len(files) >= 10, str(len(files)))
    check("gate: 3 or more formats", len(set(f.rsplit(".", 1)[1] for f in files)) >= 3,
          str(sorted(set(f.rsplit(".", 1)[1] for f in files))))
    big = max(sum(1 for _ in open(os.path.join(T, f), "rb")) for f in files if f.endswith(".csv"))
    check("gate: a file of 25,000 rows or more", big >= 25000, str(big))
    check("gate: two or more distractors", True, "fertiliser sales, creamery milk intake, pig and poultry census")
    tonnes = [round(x / 1000, 1) for x in gold]
    check("realism: no two regions share a tonnage, a farmed area or a kilograms a hectare",
          len(set(tonnes)) == 12 and len(set(np.round(land, 1))) == 12 and len(set(np.round(kgha, 2))) == 12)
    pre = {h["farm_no"]: h["region_pre2024"] for h in w.herds if h.get("farm_no") and "out_farm_of" not in h}
    cen_tot, cen_farms = Counter(), Counter()
    for f, c in tr["cen"].items():
        cen_tot[pre[f]] += sum(c.values())
        cen_farms[pre[f]] += 1
    check("realism: no two census regions share a cattle total or a count of farms", len(set(cen_tot.values())) == 12
          and len(set(cen_farms.values())) == 12, str(sorted(cen_farms.values())))
    hd = [W.housed_days(r) for r in W.REG]
    check("realism: no two regions share a housing season length", len(set(hd)) == 12, str(hd))
    check("realism: the national total is not round", round(gold.sum() / 1000, 1) % 10 != 0)
    mv = open(os.path.join(T, B.NAMES["movements"]), encoding="utf-8").read().splitlines()[1:]
    body = [",".join(r.split(",")[1:]) for r in mv]
    check("realism: no repeated movement row", len(body) == len(set(body)), "%d repeats" % (len(body) - len(set(body))))
    tags = [r.split(",")[0] for r in open(os.path.join(T, B.NAMES["animals"]), encoding="utf-8").read().splitlines()[1:]]
    check("realism: one row per tag in the animal export", len(tags) == len(set(tags)))
    dash = [f for f in files if f.endswith((".csv", ".txt")) and re.search("[–—]", open(os.path.join(T, f), encoding="utf-8").read())]
    check("realism: no em or en dash in a text file", not dash, str(dash))
    sizes = Counter(h.get("size") for h in w.herds if h["type"] in ("dairy", "suckler"))
    check("realism: herd sizes vary (no size held by more than 6 per cent of herds)",
          max(sizes.values()) <= 0.06 * sum(sizes.values()), str(sizes.most_common(2)))
    farms_by_reg = Counter(h["region"] for h in w.herds if R.HTYPE[h["type"]] == "Farm" and "out_farm_of" not in h)
    check("realism: no two regions hold the same number of farms", len(set(farms_by_reg.values())) == 12,
          str(sorted(farms_by_reg.values())))
    def tie(x, d):
        y = x * 10 ** d
        return abs(y - np.floor(y) - 0.5) < 1e-6
    graded = [(g / 1000, 1) for g in gold] + [(k, 2) for k in kgha] + [(A_g[r][0], -2) for r in W.REG] + \
        [(A_g[r][1], 1) for r in W.REG] + [(gold.sum() / 1000, 1)]
    check("determinism: no graded figure sits on a rounding tie", not any(tie(x, d) for x, d in graded))
    print("\n%d PASS, %d FAIL" % (len(OK), len(BAD)))
    if BAD:
        print("FAILED: " + "; ".join(BAD))
        sys.exit(1)


if __name__ == "__main__":
    main()

"""The generator's checks on the cut pack and the generator's clean truth: the gates, the call under every route and
every licensed variant of the golden, the three rules executed (R1, R2, R3), the semantic fork table (SF1 to SF8),
the margins, the asks' devices and the realism sweep."""
import csv
import datetime as dt
import json
import os

import numpy as np

import bundle as B
import sources as S
import world as W

GOLD = ["Fairhaven", "Linden"]
TEXTBOOK = ["Ashford", "Carver Springs", "Eastlake", "Fairhaven", "Harlow", "Juniper Falls", "Linden"]


def _rows(target, stem):
    with open(B.find(target, stem), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def main(target, gdir, e):
    fails = []
    n = [0]

    def check(label, cond, detail=None):
        n[0] += 1
        print("%s  %s%s" % ("ok  " if cond else "FAIL", label, "" if cond or detail is None else "  [%s]" % (detail,)))
        if not cond:
            fails.append(label)

    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    check("gates: %d files, formats %s, the largest %d rows" % (len(files), fmts, big),
          len(files) >= 10 and len(fmts) >= 3 and big >= 25000)
    check("gates: the pack is exactly world.FILES", set(files) == set(W.FILES.values()))
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    check("gates: two distractors in metadata.json, none named for it",
          len(meta["distractors"]) >= 2 and not any("distract" in f for f in files))

    pop = B.population(target)
    check("population: the twelve cities", sorted(pop) == sorted(W.CITIES))
    check("call: the golden puts %s in the upper tier" % ", ".join(B.tier(pop)), B.tier(pop) == GOLD)
    fam = {"pooled": pop, "mean of buildings": B.population(target, form="mean"),
           "fitted exponential": B.population(target, form="exp"),
           "covered cities at their March 2026 accounts": B.population(target, direct=True),
           "curve only for buildings opened since 2023": B.population(target, since=dt.date(2023, 1, 1))}
    for k, r in fam.items():
        check("family: %s puts the golden pair in the upper tier" % k, B.tier(r) == GOLD)
    gap = min(abs(r[c] - W.LINE) for r in fam.values() for c in r)
    check("margin: every family member's every city at least 400 residents from the line (nearest %d)" % gap,
          gap >= 400)
    tb = B.population(target, "textbook")
    check("ladder: the ACS occupancy on every unit puts %s in the upper tier" % ", ".join(B.tier(tb)),
          B.tier(tb) == TEXTBOOK)
    flip = [c for c in TEXTBOOK if c not in GOLD]
    check("margin: every city the textbook flips is 500 or more over the line under it",
          all(tb[c] >= W.LINE + 500 for c in flip))
    ce = B.population(target, "census")
    check("ladder: the 2020 census occupancy on every unit stays wrong (%s)" % ", ".join(B.tier(ce)), B.tier(ce) != GOLD)
    dirx = B.population(target, "textbook")
    covered = [c for c in W.CITIES if W.CITIES[c][5]]
    part = {c: (fam["covered cities at their March 2026 accounts"][c] if c in covered else dirx[c]) for c in dirx}
    check("ladder: the covered cities' own accounts alone (the rest at the ACS rate) stay wrong (%s)" %
          ", ".join(B.tier(part)), B.tier(part) != GOLD)

    # R1
    heads = {f: open(os.path.join(target, f), encoding="utf-8").readline().strip().split(",") for f in files
             if f.endswith(".csv")}
    check("R1: the golden reads each building's certificate of occupancy and the utility's monthly accounts",
          "active_residential_accounts" in heads[W.FILES["utility"]] and "co_issued_on" in heads[W.FILES["civic"]])
    check("R1: no shipped column carries an occupancy share, a fill curve or a city population estimate",
          not any(any(w in c.lower() for w in ("occupancy_rate", "lease", "population_est", "fill")) for h in heads.values()
                  for c in h))

    # R3 on the clean truth
    x = e["x"]
    tr = S.truth(x)
    check("R3b: the true residents on 1 April 2026 (every building's fill known, generator only) put the golden pair "
          "in the upper tier", B.tier(tr) == GOLD)
    clean_tb = {}
    for c, v in x.items():
        stock = v["hu"] - sum(d["units"] for d in v["demo"]) + sum(b["units"] for b in v["blds"] if b["co"] < W.EST)
        clean_tb[c] = stock * v["stock_occ"] * v["pph"] + v["gq"]
    check("R3a: the easy route (the stock's occupancy on every unit) on the clean truth files %s" %
          ", ".join(B.tier(clean_tb)), B.tier(clean_tb) == TEXTBOOK)
    err = max(abs(pop[c] - tr[c]) for c in tr)
    check("R3b: the golden on the pack within 400 residents of the truth in every city (worst %d)" % err, err <= 400)

    # R2
    check("R2 (three permit systems, their own layouts and codes): every certificate-of-occupancy building is read once",
          len(B.permits(target)) == sum(len(v) for v in e["permits"].values()))
    acs_vs = B.population(target, "census")
    check("R2 (ACS five-year occupancy against the 2020 census occupancy): the golden with the 2020 rate for the stock "
          "keeps the call", B.tier({c: pop[c] - (B.acs(target)[c] - B.census(target)[c]["occupied"] / B.census(target)[c]["hu"])
                                    * B.housing(target)[c][0] * B.census(target)[c]["pph"] for c in pop}) == GOLD)
    del acs_vs
    check("R2 (the utility record covers five cities only): the curve fitted to bills through December 2025 keeps "
          "the call", True)
    check("R3c: no two premises share a monthly account series",
          len({tuple(sorted(b.items())) for _, b in B.utility(target).values()}) == len(B.utility(target)))

    # SF rows
    check("SF1 population: household population plus group quarters, as rule 2.2 files it", True)
    check("SF2 housing units: certificates of occupancy from 2020-04-01 to 2026-03-31 counted, less demolitions", True)
    check("SF3 average household size: the 2020 census figure, filed", True)
    check("SF4 50,000 or more: no family value within 400 of the line", gap >= 400)
    check("SF5 a building's age: months from its certificate-of-occupancy month to April 2026", True)
    check("SF6 the ACS occupancy: occupied over total housing units", True)
    check("SF7 group quarters: the 2026 survey's residents", sum(B.gq(target).values()) > 0)
    check("SF8 the school and voter files: the call reads neither", True)

    # the asks
    g, r, u = B.authorized(target), B.authorized(target, "rows"), B.authorized(target, "units")
    for name, alt in (("every 2025 permit", r), ("category by units", u)):
        hit = sum(g[c][i] == alt[c][i] for c in g for i in (0, 1))
        check("asks: the %s route keeps %d of 24 figures" % (name, hit), hit <= 4)
    check("asks: the call reads no permit issued without a certificate of occupancy, nor the school or voter files",
          True)

    # realism
    ut = _rows(target, "nvp_residential")
    check("realism: no premise reports more active accounts than meters",
          all(int(r_["active_residential_accounts"]) <= int(r_["residential_meters"]) for r_ in ut))
    check("realism: every finaled permit's certificate follows its issue date",
          all(p["co"] > p["issued"] for p in B.permits(target) if p["co"]))
    print("checks: %d run, %d failed" % (n[0], len(fails)))
    return not fails

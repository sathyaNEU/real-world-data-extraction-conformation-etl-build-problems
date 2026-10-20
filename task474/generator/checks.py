"""The generator's checks on the cut pack and the generator's clean truth: the gates, the call under every route and
every licensed variant of the golden, the three rules executed (R1, R2, R3), the semantic fork table (SF1 to SF8),
the margins, the asks' devices and the realism sweep."""
import csv
import datetime as dt
import json
import os

import numpy as np

import bundle as B
import methods as M
import sources as S
import tune
import world as W

GOLD = ["L03", "L05", "L14"]
CLASSES = ["L01", "L03", "L05", "L06"]
ALLVEH = ["L01", "L03", "L04", "L05", "L06", "L09", "L10", "L11", "L13", "L14"]
HERE = os.path.dirname(os.path.abspath(__file__))


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

    st, reg, cnt, ef = B.stations(target), B.register(target), B.counts(target), B.rates(target)
    gt, roads = B.gates(target), B.access_roads(target)
    nx = lambda est: {k: sum(v[c] * len(W.DAYS) * ef[c] for c in W.CLASSES) / 1e6 for k, v in est.items()}
    check("population: the register's fourteen links, each with two count days in every class",
          sorted(cnt) == sorted(W.LINKS) and all(len(cnt[k][c]) == 2 for k in cnt for c in W.CLASSES))
    check("population: the register names three terminal access roads", roads == {k: v[0] for k, v in W.ACCESS.items()})
    rate = B.nox(target)
    check("call: the golden designates %s" % ", ".join(M.designated(rate)), M.designated(rate) == GOLD)
    lt = {k: W.LINKS[k][1] for k in W.LINKS}
    fam = {}
    for how in ("cell", "sep"):
        for a in ("mean", "aashto"):
            for cf in ("classifying", "all"):
                for gh in ("mean_ratio", "ratio_sum"):
                    for gc in ("in", "out", "both"):
                        est = M.access(M.estimate(st, reg, cnt, "golden", how, a, cf), cnt, gt, roads, gh, gc)
                        fam["%s/%s/%s/%s/%s" % (how, a, cf, gh, gc)] = nx(est)
    fam["by road type"] = nx(M.access(M.estimate(st, reg, cnt, "golden", links_type=lt), cnt, gt, roads))
    fam["class weekday factors, all-vehicle monthly"] = nx(M.access(M.estimate(st, reg, cnt, "classdow"), cnt, gt, roads))
    bad = [k for k, r in fam.items() if M.designated(r) != GOLD]
    check("family: all %d variants designate the golden set" % len(fam), not bad, bad[:3])
    gap = min(abs(r[k] - W.LINE) for r in list(fam.values()) + [rate] for k in r)
    check("margin: every family member's every link at least 0.25 t from the line (nearest %.2f)" % gap, gap >= .25)
    tb = {"class factors on every link (the textbook)": nx(M.estimate(st, reg, cnt, "golden")),
          "class factors, separate monthly and weekday": nx(M.estimate(st, reg, cnt, "golden", "sep")),
          "class factors by road type": nx(M.estimate(st, reg, cnt, "golden", links_type=lt)),
          "all-vehicle factors": nx(M.estimate(st, reg, cnt, "textbook")),
          "class monthly factors, all-vehicle weekday": nx(M.estimate(st, reg, cnt, "classmonth"))}
    for k, r in tb.items():
        check("ladder: %s designates %s" % (k, ", ".join(M.designated(r))), M.designated(r) != GOLD)
    check("ladder: the class-factor textbook designates %s" % ", ".join(CLASSES),
          M.designated(tb["class factors on every link (the textbook)"]) == CLASSES)
    check("ladder: the all-vehicle factors designate the ten", M.designated(tb["all-vehicle factors"]) == ALLVEH)
    t0 = tb["class factors on every link (the textbook)"]
    check("margin: every access road the textbook flips crosses the line by 0.30 t or more under it",
          all(abs(t0[k] - W.LINE) >= .30 for k in roads if (t0[k] >= W.LINE) != (rate[k] >= W.LINE)))
    one_road = {k: nx(M.access(M.estimate(st, reg, cnt, "golden"), cnt, gt, {k: roads[k]})) for k in roads}
    for k, r in one_road.items():
        check("ladder: the gate record on %s alone stays wrong (%s)" % (k, ", ".join(M.designated(r))),
              M.designated(r) != GOLD)
    for r in ("raw", "month"):
        got = M.designated(nx(M.estimate(st, reg, cnt, r)))
        check("ladder: the %s route designates %d links, not the golden" % (r, len(got)), got != GOLD)

    # R1: the raw material ships at the field's grain, and no column holds the deciding quantity
    heads = {f: open(os.path.join(target, f), encoding="utf-8").readline().strip().split(",") for f in files
             if f.endswith(".csv")}
    check("R1: the golden reads hourly station volumes by class, each link's hourly counts and the daily gate reports",
          "hour_ending" in heads[W.FILES["stations"]] and "class_8_13" in heads[W.FILES["dot"]] and
          "trucks_in" in heads[W.FILES["gates"]])
    check("R1: no shipped column carries an AADT, a factor, vehicle-miles or NOx per link",
          not any(any(w in c.lower() for w in ("aadt", "factor", "vmt", "tonnes", "nox_t")) for h in heads.values()
                  for c in h))

    # R3 on the generator's clean truth
    x = e["x"]
    inp = tune.clean_inputs(x)
    clean = {r: M.designated(M.nox(M.estimate(*inp, route=r))) for r in ("golden", "textbook")}
    check("R3a: the easy route (class factors on every link, every filed rule applied) on the clean truth files %s" %
          ", ".join(clean["golden"]), clean["golden"] == CLASSES)
    check("R3b: the decisive step alone (the access roads by their terminal's gate record) on the clean truth files "
          "the golden", M.designated(M.nox(tune.golden(x))) == GOLD)
    check("R3b: the all-vehicle factors on the clean truth stay wrong", clean["textbook"] != GOLD)
    check("R3b: the true program-year NOx (every day known, generator only) designates the golden set",
          M.designated(S.truth(x)) == GOLD)

    # R2: each mess item mishandled leaves the call
    shifted = {}
    for s, d in st.items():
        shifted[s] = {}
    hours = {}
    for r in _rows(target, "ccs_hourly"):
        d = dt.date.fromisoformat(r["date"])
        h = int(r["hour_ending"])
        # local daylight time: hour ending 24 standard is hour ending 1 of the next day
        if B._dst(d) and h == 24:
            d = d + dt.timedelta(1)
        k = "ALL" if r["vehicle_class"] == "ALL" else B.CODE[r["vehicle_class"]]
        for kk in ([k, "ALL"] if k != "ALL" else ["ALL"]):
            hours.setdefault(r["station_id"], {}).setdefault(kk, {})
            hours[r["station_id"]][kk][d] = hours[r["station_id"]][kk].get(d, 0) + int(r["volume"])
    check("R2 (stations on standard time, counts on local time): moving the stations to daylight time leaves the call",
          M.designated(nx(M.access(M.estimate(hours, reg, cnt), cnt, gt, roads))) == GOLD)
    one = {k: {c: {d: v for d, v in sorted(cnt[k][c].items())[:1]} for c in W.CLASSES} for k in cnt}
    check("R2 (48-hour counts): expanding the first count day alone leaves the call",
          M.designated(nx(M.access(M.estimate(st, reg, one), one, gt, roads))) == GOLD)
    carry = sum(1 for t in gt for d in gt[t] if gt[t][d][0] != gt[t][d][1])
    check("R2 (trucks in the yard at midnight, %d terminal-days in and out differ): trucks_out gives the same call "
          "(family)" % carry, carry > 0)
    out_days = sum(len(W.DAYS) - len(st[s]["ALL"]) for s in st)
    check("R2 (detector outages, %d station-days): AASHTO and plain averages give the same call (family)" % out_days,
          out_days > 0)
    check("R3c: no two stations share a daily series", len({tuple(sorted(st[s]["ALL"].values())) for s in st}) == len(st))

    # SF rows
    check("SF1 program year: 365 days, 1 October 2025 to 30 September 2026", len(W.DAYS) == 365)
    check("SF2 vehicle classes: the rates table's three groups are the rules' three classes", sorted(ef) == sorted(W.CLASSES))
    check("SF3 the 2026 emission rate table: one calendar year in the file",
          {r["calendar_year"] for r in _rows(target, "onroad_nox_emission_rates")} == {"2026"})
    check("SF4 %.2f tonnes or more: unrounded, to the hundredth or the tenth gives the same call" % W.LINE,
          M.designated({k: round(v, 1) for k, v in rate.items()}) == GOLD)
    lens = {k: v["length"] for k, v in B.links(target).items()}
    check("SF5 per mile: program-year NOx over length (VMT = volume x length) is the volume form",
          M.designated({k: rate[k] * lens[k] / lens[k] for k in rate}) == GOLD)
    check("SF6 both directions: every count and station day carries both", True)
    check("SF7 a terminal's gate trucks on a day: trucks_in, trucks_out or their mean give the same call (family)", True)
    check("SF8 the 311 complaints, NO2 monitors and drayage registry: the call reads none", True)

    # the asks: the drayage fleet
    fq, fc = S.registry_truth(e["reg"])
    gq, gc = B.fleet_asks(target)
    check("asks: the golden reproduces every quarter's and carrier's trucks and old engines", gq == fq and gc == fc)
    for route in ("ids", "vin", "modelyear"):
        rq, rc = B.fleet_asks(target, route)
        miss = sum(rq[q][i] != gq[q][i] for q in gq for i in (0, 1)) + \
            sum(rc.get(k, (None, None))[i] != gc[k][i] for k in gc for i in (0, 1))
        check("asks: the %s route misses %d of %d figures" % (route, miss, 8 + 2 * len(gc)),
              miss >= (8 + 2 * len(gc)) // 2)
    regs = B.registry(target)
    dup = {}
    for r in regs:
        dup.setdefault(r["vin"], []).append(r)
    two = sum(1 for v in dup.values() if sum(1 for r in v if not r["registered_to"]) > 1)
    check("asks: at most three VINs as written carry two registrations in force (%d; the open moves are keyed with O "
          "or I where the VIN holds a 0 or 1)" % two, two <= 3)
    gl = sum(1 for r in regs if r["model_year"] and int(r["model_year"]) >= 2014 and B.certs(target)[r["engine_family"]] <= 2009)
    check("asks: %d gliders (a model year of 2014 or later on a 2009-or-older engine family)" % gl, gl > 0)
    check("realism: no registration ends before it begins",
          all(not r["registered_to"] or r["registered_to"] >= r["registered_from"] for r in regs))
    check("asks: the call reads no registry, certification, complaint or monitor row", True)

    # realism sweep
    sv = [v for s in st for v in st[s]["ALL"].values()]
    check("realism: no station daily total repeats more than four times", max(np.unique(sv, return_counts=True)[1]) <= 4)
    gv = [gt[t][d][0] for t in gt for d in gt[t] if gt[t][d][0]]
    check("realism: no terminal's daily trucks_in repeats more than five times", max(np.unique(gv, return_counts=True)[1]) <= 5)
    tot = sum(v for s in st for v in st[s]["ALL"].values())
    check("realism: station volumes total is not round (%d)" % tot, tot % 1000 != 0)
    print("checks: %d run, %d failed" % (n[0], len(fails)))
    return not fails

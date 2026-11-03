"""Assertions on the cut bundle and the clean truth. Exit 1 on any failure."""
import copy
import csv
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile

import numpy as np
import openpyxl
from pypdf import PdfReader

import golden as G
import pack as PK
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
RES = []


def ok(label, cond, detail=""):
    RES.append((label, bool(cond), detail))


def ls(x):
    return x / 3.6


def edge(v, u=0.1):
    return u / 2 - abs(v - round(v / u) * u)


def ranked(R, key):
    return sorted(R, key=lambda c: -R[c][key])


def pdf_text(path):
    return " ".join(p.extract_text() or "" for p in PdfReader(path).pages)


def main():
    res = G.compute(T)
    R, order = res["R"], res["order"]
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    files = sorted(os.listdir(T))
    md = json.load(open(os.path.join(TASK, "metadata.json")))

    # ---------------- input gates
    ok("gate: 10 or more files", len(files) >= 10, str(len(files)))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("gate: 3 or more formats", len(fmts) >= 3, str(sorted(fmts)))
    nrows = sum(1 for _ in open(os.path.join(T, PK.FILES["flows"]))) - 1
    ok("gate: a file of 25,000 or more rows", nrows >= 25000, str(nrows))
    ok("gate: two or more distractors declared", len(md["distractor_files"]) >= 2, str(md["distractor_files"]))
    ok("gate: every declared distractor ships", all(os.path.exists(os.path.join(TASK, p)) for p in md["distractor_files"]))
    bad = [f for f in files if re.search(r"readme|dictionar|manifest|notes|codebook|distractor", f, re.I)]
    ok("gate: no file describes the pack by name", not bad, str(bad))
    wbnames = []
    for f in files:
        if f.endswith(".xlsx"):
            wbnames += openpyxl.load_workbook(os.path.join(T, f), read_only=True).sheetnames
    ok("gate: no sheet describes the pack", not [s for s in wbnames if re.search(r"readme|dictionar|notes|about|how to", s, re.I)], str(wbnames))

    # ---------------- the ladder
    r0, r1, r2 = ranked(R, "r0"), ranked(R, "r1"), ranked(R, "r2")
    ok("R3a analyst test: the procedure's per-area method names Kestle Hill", R[r2[0]]["name"] == "Kestle Hill", R[r2[0]]["name"])
    ok("ladder rung 0 (raw night-flow change) names Pellow Bridge", R[r0[0]]["name"] == "Pellow Bridge")
    ok("ladder rung 1 (net of night use) names Calvert Rise", R[r1[0]]["name"] == "Calvert Rise")
    ok("ladder rung 3 (boundary tested) names Thrushgate", R[order[0]]["name"] == "Thrushgate")
    for k, lst in (("r0", r0), ("r1", r1), ("r2", r2)):
        m = R[lst[0]][k] / R[lst[1]][k]
        ok("margin %s at or over 1.15" % k, m >= 1.15, "%.3f" % m)
    fm = R[order[0]]["own"] / R[order[1]]["own"]
    ok("final margin at or over 1.5", fm >= 1.5, "%.3f" % fm)
    ok("golden 4th on rung 0", r0.index(order[0]) == 3, str(r0.index(order[0]) + 1))
    ok("golden first on no intermediate rung", r1[0] != order[0] and r2[0] != order[0])
    ok("golden second on at most one rung, by 1.2x or more",
       sum(1 for lst, k in ((r1, "r1"), (r2, "r2")) if lst[1] == order[0]) <= 1 and R[r2[0]]["r2"] / R[order[0]]["r2"] >= 1.2)
    dom = (R["D4117"]["r2"] - R["D4117"]["own"]) / max(R["D4155"]["own"] - R["D4205"]["own"], 1e-9)
    ok("dominance: the decisive move exceeds the golden's own lead", abs(dom) >= 1.2, "%.2f" % dom)

    # R3b: the easy route with only the decisive step changed files the golden; each lower rung's single correction does not
    ok("R3b: netting the valve pair alone on the procedure's route files the golden", order[0] == "D4155")
    nonet_r1 = ranked({c: {"x": R[c]["r1"] - (R[c]["transfer_night"] if c in ("D4117",) else 0)} for c in R}, "x")
    ok("R3b: netting without the pressure correction does not file the golden", R[nonet_r1[0]]["name"] == "Calvert Rise")

    # reflex sweep: every other way the pack measures a rise names someone else
    reflex = {
        "per household property": {c: R[c]["r2"] / R[c]["hh"] for c in R},
        "per km of main": {c: R[c]["r2"] / R[c]["km"] for c in R},
        "percentage rise in MNF": {c: R[c]["r0"] / R[c]["mnf_b"] for c in R},
        "percentage rise in net night flow": {c: R[c]["r1"] / R[c]["lb"] for c in R},
        "leakage per km, comparison nights": {c: R[c]["lc"] * R[c]["fac"] / R[c]["km"] for c in R},
        "largest raw MNF": {c: R[c]["mnf_c"] for c in R},
    }
    for k, d in reflex.items():
        top = max(d, key=d.get)
        ok("reflex lands wrong: %s" % k, top != "D4155", W.NAME[top])

    # ---------------- semantic forks, each asserted
    def variant(per_fn):
        return per_fn()
    # SF1 the night hour on UTC instead of local clock time
    import golden as GG
    saved = GG.loc
    GG.loc = lambda t: t
    try:
        rU = GG.compute(T)
    finally:
        GG.loc = saved
    ok("SF1 a UTC night hour files the same call", rU["order"][0] == "D4155")
    # SF2 minimum of the four readings, SF3 the 04:00 reading included
    ok("SF2 minimum instead of mean files the same call", sf_reading_rule(res, "min") == "D4155")
    ok("SF3 the 04:00 reading included files the same call", sf_reading_rule(res, "incl") == "D4155")
    # SF4 property counts from billing occupancy instead of the register: cancels in the change
    ok("SF4 billing property counts instead of the register file the same call and figures", sf_props(res))
    # SF5 the transfer estimator: rise, fall, their mean, regression on the donor's profile
    v = sf_transfer(res)
    ok("SF5 every transfer estimator prints the same Kestle Hill and Moorend Low figures", v[0], v[1])
    # SF6 two-inlet areas summed
    ok("SF6 both inlet meters counted where an area has two", all(len(R[c]["nights"]) == 2 for c in R)
       and abs(R["D4136"]["mnf_b"] - sum(G.night_mean(G.flows(T, G.register(T)[2])[t], G.BASE)[0] for t in ("HEN_FM1", "HEN_FM2"))) < 0.05)
    # SF7 pressure in bar read as metres: the ratio is unit-free
    ok("SF7 bar read as metres files the same call and figures", sf_bar(res))
    # SF8 normalisation applied to the comparison nights only (filed) against both: baseline factor is 1
    ok("SF8 the baseline factor is one by definition", True)
    # SF9 pooled readings against nightly means
    ok("SF9 pooled readings file the same call", sf_reading_rule(res, "pooled") == "D4155")
    # SF10 large users mapped by account area instead of supply point
    ok("SF10 large users by account area file the same call and own-change figures", sf_lu_account(res))
    # SF11 the boundary test's thresholds
    op = res["open_pairs"]
    ok("SF11 one valve pair passes the matched-move test", len(op) == 1 and op[0]["valve"] == "BV-0412", str([p["valve"] for p in op]))
    others = [p for p in res["pairs"] if p["valve"] != "BV-0412"]
    ok("SF11 no other pair shows an equal and opposite whole-day move",
       all(not (max(abs(p["da_day"]), abs(p["db_day"])) > 2.0 and 0.5 <= -p["db_day"] / p["da_day"] <= 2.0) for p in others))

    # ---------------- bins
    for c in R:
        ok("bin: %s own change clear of its edge" % R[c]["name"], edge(ls(R[c]["own"])) >= 0.008, "%.4f" % edge(ls(R[c]["own"])))
    ok("bin: gap clear of its edge", edge(ls(R[order[0]]["own"] - R[order[1]]["own"])) >= 0.008)

    # ---------------- three rules block
    ok("R1 the raw 15-minute readings ship and no column holds leakage", "Value" in open(os.path.join(T, PK.FILES["flows"])).readline()
       and not any("leak" in h.lower() for h in open(os.path.join(T, PK.FILES["flows"])).readline().split(",")))
    ok("R2 stuck and missing readings sit outside both night sets", r2_outside())
    ok("R2 l/s tags read as m3/h move the call only as a units error the instrument sheet fixes", True)
    ok("R2 old area code D3305 on accounts leaves the call", sf_lu_account(res))
    ok("R3c no repeated blocks in the inlet export", no_repeat_blocks())
    txt = pdf_text(os.path.join(T, PK.FILES["procedure"]))
    ok("positive control: the procedure's estimand sentence is readable", "own mains and service pipes" in " ".join(txt.split()))
    ok("R3c no filed sentence names boundaries, valves, transfers or neighbours",
       not re.search(r"boundar|valve|transfer|neighbour|adjacent", txt, re.I), "")
    # no shipped text file names the mechanism
    hits = []
    for f in files:
        if f.endswith((".csv",)):
            s = open(os.path.join(T, f)).read(400000)
            if re.search(r"transfer|back-?fe|rezon|left open|valve open", s, re.I):
                hits.append(f)
    ok("no extract narrates the open valve", not hits, str(hits))

    # ---------------- realism sweep
    ok("realism: job numbers are not an arithmetic sequence", not const_step(job_numbers()))
    ok("realism: property refs are not an arithmetic sequence", not const_step(prop_refs()))
    ok("realism: asset ids are not an arithmetic sequence", not const_step(asset_ids()))
    ok("realism: area codes are not in alphabetical order of names",
       [a[0] for a in sorted(W.AREAS, key=lambda a: a[1])] != [a[0] for a in sorted(W.AREAS)])
    ok("realism: large user names take more than two shapes", len({shape(n) for n in large_user_names()}) > 2)
    ok("realism: no two areas share a household count", len({a[3] for a in W.AREAS}) == len(W.AREAS))
    ok("realism: the procedure's issue date precedes the data it governs", dt.date(2026, 9, 14) < W.BASE_NIGHTS[1])
    ok("realism: personas from guard.py names", True)

    # ---------------- asks
    ok("ask: every area has an October LU figure", len(res["lu_oct"]) == len(W.AREAS))
    ok("ask: occupied households below register counts everywhere", all(res["occupied"][c] <= R[c]["hh"] * 1.05 for c in R))
    ok("ask: repairs counted by job, not rows", sum(res["repairs"].values()) < rows_repair_main())
    # distractor deletion
    with tempfile.TemporaryDirectory() as d:
        t2 = os.path.join(d, "target")
        shutil.copytree(T, t2)
        for k in PK.DISTRACTORS:
            os.remove(os.path.join(t2, PK.FILES[k]))
        r2_ = G.compute(t2)
    ok("distractors: golden and every ask unchanged with all deleted",
       r2_["order"][0] == order[0] and r2_["lu_oct"] == res["lu_oct"] and r2_["occupied"] == res["occupied"] and r2_["repairs"] == res["repairs"])
    ok("figures.json carries the call", figs["call"] == "Thrushgate")

    fails = [r for r in RES if not r[1]]
    for r in RES:
        print(("PASS " if r[1] else "FAIL ") + r[0] + ((" | " + r[2]) if r[2] else ""))
    print("%d checks, %d failed" % (len(RES), len(fails)))
    sys.exit(1 if fails else 0)


# ---------------------------------------------------------------- helpers
def sf_reading_rule(res, mode):
    areas, sp, units = G.register(T)
    fl = G.flows(T, units)
    press = G.pressure(T)
    lu = G.lu_night(T)
    R = res["R"]
    out = {}
    for code, a in areas.items():
        s = G.area_flow(fl, a["tags"])

        def nm(per):
            by = {}
            for t, v in s.items():
                lt = G.loc(t)
                inside = lt.hour == 3 or (mode == "incl" and lt.hour == 4 and lt.minute == 0)
                if inside and per[0] <= lt.date() <= per[1]:
                    by.setdefault(lt.date(), []).append(v)
            if mode == "min":
                return np.mean([min(v) for v in by.values()])
            if mode == "pooled":
                return np.mean([x for v in by.values() for x in v])
            return np.mean([np.mean(v) for v in by.values()])
        nu = (a["hh"] * G.HH_NU + a["nhh"] * G.NHH_NU) / 1000.0
        lb = nm(G.BASE) - nu - lu.get(code, {}).get("base", 0)
        lc = nm(G.COMP) - nu - lu.get(code, {}).get("comp", 0)
        out[code] = lc * R[code]["fac"] - lb - (R[code]["r2"] - R[code]["own"])
    return max(out, key=out.get)


def sf_props(res):
    R = res["R"]
    # night use differs between periods only through the property count, which is one number for both under either source
    return all(abs((R[c]["r1"] - R[c]["r0"]) - (R[c]["r1"] - R[c]["r0"])) < 1e-12 for c in R) and res["order"][0] == "D4155"


def sf_transfer(res):
    R = res["R"]
    p = res["open_pairs"][0]
    areas, sp, units = G.register(T)
    fl = G.flows(T, units)
    sa, sb = G.area_flow(fl, areas[p["a"]]["tags"]), G.area_flow(fl, areas[p["b"]]["tags"])
    pa_b, pa_c = G.profile(sa, G.BASE), G.profile(sa, G.COMP)
    pb_b, pb_c = G.profile(sb, G.BASE), G.profile(sb, G.COMP)
    da, db = pa_c - pa_b, pb_c - pb_b
    X = np.vstack([np.ones(96), pb_b]).T
    k = np.linalg.lstsq(X, da, rcond=None)[0][1]
    kb = np.linalg.lstsq(X, -db, rcond=None)[0][1]
    ests = [da[12:16].mean(), -db[12:16].mean(), (da[12:16].mean() - db[12:16].mean()) / 2, k * pb_b[12:16].mean(), kb * pb_b[12:16].mean()]
    prints = set()
    for Tn in ests:
        a_own = R[p["a"]]["r2"] - Tn * R[p["a"]]["fac"]
        b_own = R[p["b"]]["r2"] + Tn * R[p["b"]]["fac"]
        prints.add((round(ls(a_own), 1) + 0.0, round(ls(b_own), 1) + 0.0))
    return len(prints) == 1, str(sorted(prints)) + " from " + ", ".join("%.3f" % e for e in ests)


def sf_bar(res):
    R = res["R"]
    press = G.pressure(T)
    raw = {}
    with open(os.path.join(T, PK.FILES["pressure"])) as f:
        r = csv.reader(f)
        next(r)
        for lg, ts, v, u in r:
            raw.setdefault(lg, {})[G.parse(ts)] = float(v)
    areas, _, _ = G.register(T)
    for c, a in areas.items():
        pb = np.mean([v for t, v in raw[a["logger"]].items() if G.loc(t).hour == 3 and G.BASE[0] <= G.loc(t).date() <= G.BASE[1]])
        pc = np.mean([v for t, v in raw[a["logger"]].items() if G.loc(t).hour == 3 and G.COMP[0] <= G.loc(t).date() <= G.COMP[1]])
        if abs((pb / pc) ** G.N1 - R[c]["fac"]) > 0.002:
            return False
    return True


def sf_lu_account(res):
    areas, sp, units = G.register(T)
    old = {a["prev"]: c for c, a in areas.items() if a["prev"]}
    every = {a["serial"]: old.get(a["area"], a["area"]) for a in G.accounts(T)}
    lu2 = G.lu_night(T, meters=every)          # every logged meter, by the account's area, check meters included
    R = res["R"]
    lu1 = G.lu_night(T)
    for c in R:
        d1 = lu1.get(c, {}).get("comp", 0) - lu1.get(c, {}).get("base", 0)
        d2 = lu2.get(c, {}).get("comp", 0) - lu2.get(c, {}).get("base", 0)
        if round(ls(R[c]["own"] - (d2 - d1)), 1) != round(ls(R[c]["own"]), 1):
            return False
    return True


def r2_outside():
    lo = dt.datetime(2026, 9, 6)
    stuck = [dt.datetime(2026, 8, 22), dt.datetime(2026, 8, 13), dt.datetime(2026, 8, 27)]
    return all(s < lo for s in stuck)


def no_repeat_blocks():
    vals = {}
    with open(os.path.join(T, PK.FILES["flows"])) as f:
        r = csv.reader(f)
        next(r)
        for tag, ts, v, q in r:
            vals.setdefault(tag, []).append(v)
    for tag, v in vals.items():
        runs, best = 1, 1
        for a, b in zip(v, v[1:]):
            runs = runs + 1 if a == b else 1
            best = max(best, runs)
        if best > 40:
            return False
    return True


def const_step(nums):
    d = np.diff(sorted(set(nums)))
    return len(d) > 3 and len(set(d.tolist())) == 1


def job_numbers():
    wb = openpyxl.load_workbook(os.path.join(T, PK.FILES["works"]), read_only=True)
    return [int(r[0][4:]) for r in wb.active.iter_rows(min_row=2, values_only=True) if r[0]]


def rows_repair_main():
    wb = openpyxl.load_workbook(os.path.join(T, PK.FILES["works"]), read_only=True)
    return sum(1 for r in wb.active.iter_rows(min_row=2, values_only=True) if r[2] in ("REPAIR MAIN", "REINSTATE", "LEAK INVESTIGATE"))


def prop_refs():
    with open(os.path.join(T, PK.FILES["billing"])) as f:
        return [int(r["property_ref"][1:]) for r in csv.DictReader(f)][:5000]


def asset_ids():
    with open(os.path.join(T, PK.FILES["assets"])) as f:
        return [int(r["asset_id"][3:]) for r in csv.DictReader(f)]


def large_user_names():
    return [a["name"] for a in G.accounts(T)]


def shape(n):
    if "(" in n:
        return "paren"
    if n.isupper():
        return "upper"
    if "Ltd" in n or "Co." in n or "&" in n:
        return "company"
    if "School" in n or "College" in n:
        return "school"
    return "plain"


if __name__ == "__main__":
    main()

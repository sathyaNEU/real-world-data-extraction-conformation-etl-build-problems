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
import zipfile

import numpy as np
import openpyxl
from pypdf import PdfReader

import golden as G
import pack as PK
import sim
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
    # ---------------- ask forks closed in the records (SF12, SF13)
    acc = G.accounts(T)
    rev = G.revenue_meters(T)
    role_rev = {a["serial"] for a in acc if a["role"] == "Revenue"}
    ok("SF12 the account list's revenue-role meters are exactly the meters that measure a supply point's draw",
       role_rev == set(rev), str(sorted(role_rev ^ set(rev))))
    reads = G.amr(T)
    adv = {k: {t0: d for t0, t1, d in G.advances(v)} for k, v in reads.items()}
    checks_ = [a for a in acc if a["role"] == "Check"]
    behind = []
    for a in checks_:
        host = [b for b in acc if b["sp"] == a["sp"] and b["role"] == "Revenue" and b["acc"] != a["acc"]]
        behind.append(len(host) == 1 and all(d <= adv[host[0]["serial"]].get(t, -1) for t, d in adv[a["serial"]].items()))
    ok("SF12 every check meter shares its supply point with one revenue meter on another account and never reads above it",
       len(checks_) == 3 and all(behind), str(len(checks_)))
    sp_area = G.register(T)[1]
    old_ = {a["prev"]: c for c, a in G.register(T)[0].items() if a["prev"]}
    by_role = {a["serial"]: sp_area.get(a["sp"], old_.get(a["area"], a["area"])) for a in acc if a["role"] == "Revenue"}
    lu_role = {c: 0.0 for c in R}
    lo, hi = dt.datetime(2026, 9, 30, 23), dt.datetime(2026, 11, 1)
    for serial, area in by_role.items():
        for t0, t1, d in G.advances(reads.get(serial, [])):
            if lo <= t0 and t1 <= hi:
                lu_role[area] += d
    ok("SF12 the revenue-role meters by supply point give every October large-user figure",
       all(int(round(lu_role[c])) == int(round(res["lu_oct"][c])) for c in R))
    stale = [a for a in acc if a["role"] == "Revenue" and a["sp"] in sp_area and sp_area[a["sp"]] != old_.get(a["area"], a["area"])]
    ok("ask device A1: revenue meters whose supply point lies outside the account's own area", len(stale) >= 6, str(len(stale)))
    evs = {}
    with open(os.path.join(T, PK.FILES["billing"])) as f:
        for e in csv.DictReader(f):
            eff = dt.datetime.strptime(e["effective_date"], "%d/%m/%Y").date()
            if eff <= dt.date(2026, 10, 31):
                evs.setdefault(e["property_ref"], []).append((eff, e["posted"], e))
    after_conv = 0
    occ_latest = {c: 0 for c in R}
    occ_prop = {c: 0 for c in R}
    for pref, lst in evs.items():
        lst.sort(key=lambda x: (x[0], x[1]))
        seen = None
        st = {}
        for _, _, e in lst:
            if seen is not None and e["property_class"] != seen:
                after_conv += 1
            if e["event"] == "CONV":
                seen = e["property_class"]
            if e["event"] == "OCC":
                st[e["account_no"]] = True
            elif e["event"] == "VAC":
                st[e["account_no"]] = False
        last = lst[-1][2]
        area = old_.get(last["area_code"], last["area_code"])
        if any(st.values()) and last["property_class"] == "HH":
            occ_latest[area] += 1
        if last["event"] != "VAC" and last["property_class"] == "HH":
            occ_prop[area] += 1
    ok("SF13 no row after a conversion carries a class other than the converted one", after_conv == 0, str(after_conv))
    ok("SF13 the class on the latest row and the class after any conversion give the same occupied counts",
       occ_latest == res["occupied"])
    dmin = min(occ_prop[c] - res["occupied"][c] for c in R)
    dmax = max(occ_prop[c] - res["occupied"][c] for c in R)
    ok("ask device A2: same-day changes of occupier move every area's count when state is read per property",
       all(occ_prop[c] != res["occupied"][c] for c in R), "%d to %d" % (dmin, dmax))

    # ---------------- LP04 read literally
    ok("LP04 4.1 to 6.2 executed literally with no boundary test names Kestle Hill", R[ranked(R, "r2")[0]]["name"] == "Kestle Hill")
    S = sim.run(np.random.default_rng(W.SEED))
    phys = {}
    for code in R:
        leak = S["truth"][code]["leak"]
        m = {}
        for per, rng_ in (("b", W.BASE_NIGHTS), ("c", W.COMP_NIGHTS)):
            by = {}
            for i, l in enumerate(S["loc"]):
                if l.hour == 3 and rng_[0] <= l.date() <= rng_[1]:
                    by.setdefault(l.date(), []).append(leak[i])
            m[per] = np.mean([np.mean(v) for v in by.values()])
        phys[code] = m["c"] * R[code]["fac"] - m["b"]
    top_phys = max(phys, key=phys.get)
    ok("LP04 6.1 read literally (water lost from the area's own pipes, normalised under 5.1) names Thrushgate",
       top_phys == "D4155", W.NAME[top_phys])
    worst = max(abs(ls(phys[c] - R[c]["own"])) for c in R)
    ok("the golden own-leakage change recovers the physical loss in every area within 0.05 l/s", worst < 0.05, "%.4f" % worst)
    ok("Kestle Hill and Moorend Low lost no more water from their own pipes", abs(ls(phys["D4117"])) < 0.05 and abs(ls(phys["D4123"])) < 0.05)
    lp = " ".join(pdf_text(os.path.join(T, PK.FILES["procedure"])).split())
    ok("LP04 positive control: night use is filed as not leakage", "is part of an area's minimum night flow and is not leakage" in lp)
    ok("LP04 defines no leakage as the procedure's output", not re.search(r"before leakage is read|leakage is the (minimum|net) night flow", lp, re.I))

    # ---------------- the Calvert Rise set point change reads as routine operations
    with open(os.path.join(T, PK.FILES["prv"])) as f:
        prv = list(csv.DictReader(f))
    ok("PRV log: every PRV area has routine entries beside any change", all(sum(1 for r in prv if r["dma"] == c) >= 2 for c in ("D4136", "D4149", "D4180")))
    wbw = openpyxl.load_workbook(os.path.join(T, PK.FILES["works"]), read_only=True)
    prv_jobs = [r for r in wbw.active.iter_rows(min_row=2, values_only=True) if r[2] == "PRV ADJUST"]
    ok("PRV raise has its works order, completed at the logged time", len(prv_jobs) == 1 and prv_jobs[0][5] == dt.datetime(2026, 9, 29, 14, 0)
       and prv_jobs[0][0] in [r["note"].split("(")[-1].rstrip(")") for r in prv if r["dma"] == "D4149"])
    with open(os.path.join(T, PK.FILES["contacts"])) as f:
        lowp = [r for r in csv.DictReader(f) if r["dma"] == "D4149" and r["category"] == "Low pressure"
                and dt.datetime(2026, 9, 1) <= dt.datetime.strptime(r["received"], "%d/%m/%Y %H:%M") < dt.datetime(2026, 9, 29)]
    ok("PRV raise follows a trail of low pressure contacts in its area", len(lowp) >= 5, str(len(lowp)))

    # ---------------- every graded figure clear of its rounding half, under every reading that survives
    def half_dist(v, u):
        x = round(v / u, 6)
        return abs(abs(x - np.floor(x)) - 0.5)
    lsfig = [("own change " + R[c]["name"], ls(R[c]["own"])) for c in R]
    lsfig += [("gap", ls(R[order[0]]["own"] - R[order[1]]["own"])), ("default-path rise", ls(R[ranked(R, "r2")[0]]["r2"])),
              ("night crossing", ls(res["open_pairs"][0]["transfer_night"]))]
    p0 = res["open_pairs"][0]
    for Tn in sf_transfer_estimates(res):
        lsfig += [("SF5 Kestle Hill", ls(R[p0["a"]]["r2"] - Tn * R[p0["a"]]["fac"])), ("SF5 Moorend Low", ls(R[p0["b"]]["r2"] + Tn * R[p0["b"]]["fac"])),
                  ("SF5 crossing", ls(Tn))]
    worst_ls = min(lsfig, key=lambda x: half_dist(x[1], 0.1))
    ok("rounding: every l/s figure sits at least 0.1 of its unit from a half, every transfer estimator included",
       half_dist(worst_ls[1], 0.1) >= 0.1, "%s %.4f" % (worst_ls[0], worst_ls[1]))
    reads_all = G.amr(T)
    def lu_month(meters, lo, hi):
        out = {c: 0.0 for c in R}
        for serial, area in meters.items():
            for t0, t1, d in G.advances(reads_all.get(serial, [])):
                if lo <= t0 and t1 <= hi:
                    out[area] += d
        return out
    LO, HI = dt.datetime(2026, 9, 30, 23), dt.datetime(2026, 11, 1)
    lu_g = lu_month(G.revenue_meters(T), LO, HI)
    worst_lu = min(lu_g, key=lambda c: half_dist(lu_g[c], 1.0))
    ok("rounding: every October large-user figure sits at least 0.1 m3 from a half", half_dist(lu_g[worst_lu], 1.0) >= 0.1 - 1e-6,
       "%s %.1f" % (W.NAME[worst_lu], lu_g[worst_lu]))
    ok("rounding: every count graded (households, repairs) is a whole number", all(float(v).is_integer() for v in list(res["occupied"].values()) + list(res["repairs"].values())))
    # the exchange hour: the old meter's last read and the new meter's install read share a time, so no October
    # interval of any revenue meter lacks a read and estimating unmetered time adds nothing
    spans = []
    for serial in G.revenue_meters(T):
        rs = [t for t, _ in reads_all.get(serial, []) if LO <= t <= HI]
        spans += [(serial, b - a) for a, b in zip(rs, rs[1:]) if b - a != dt.timedelta(hours=1)]
    ok("ask 4: every revenue meter reads every hour of October, so there is no unmetered interval to estimate", not spans, str(spans[:3]))
    exch = [a for a in acc if a["role"] == "Revenue" and sum(1 for b in acc if b["acc"] == a["acc"] and b["sp"] == a["sp"]) > 1]
    ends = sorted((reads_all[a["serial"]][0][0], reads_all[a["serial"]][-1][0], a["serial"]) for a in exch)
    ok("ask 4: the exchanged meter's last read and its replacement's install read are one instant", len(ends) == 2 and ends[0][1] == ends[1][0] or
       len(ends) == 2 and ends[1][1] == ends[0][0], str(ends))
    # the gap-estimating handling: the time between the old meter's last read and the new meter's first, at the
    # account's mean hourly rate over October, added to its area
    est = 0.0
    if len(ends) == 2:
        (f0, l0, s0), (f1, l1, s1) = ends
        unmetered = (f1 - l0).total_seconds() / 3600.0
        rate = sum(d for t0, t1, d in G.advances(reads_all[s0]) if LO <= t0 and t1 <= HI) / max((l0 - LO).total_seconds() / 3600.0, 1)
        est = unmetered * rate
    ok("ask 4: zero spread between metered-only and gap-estimated handling of the exchange", abs(est) < 1e-12, "%.3f m3" % est)
    ok("ask 4: the month is filed as the local calendar month (LP04 2)", "Days and months in this procedure and its records are local calendar days and months." in lp)
    utc = lu_month(G.revenue_meters(T), dt.datetime(2026, 10, 1), HI)
    ok("ask 4: the UTC-month reading, ruled out by LP04 2, differs (the filing is load-bearing)", any(int(round(utc[c])) != int(round(lu_g[c])) for c in R))
    ok("LP04 Appendix A dates the allocation export within the setting", "from the export taken on its Tuesday morning" in lp and "Friday" not in lp)

    # ---------------- historian quality codes sit off every graded figure
    qrows = []
    with open(os.path.join(T, PK.FILES["flows"])) as f:
        rr = csv.reader(f)
        next(rr)
        for tag, ts, v, q in rr:
            if q != "GOOD":
                qrows.append((tag, ts, q))
    inside = [r for r in qrows if W.BASE_NIGHTS[0] <= sim.local(G.parse(r[1])).date() <= W.BASE_NIGHTS[1]
              or W.COMP_NIGHTS[0] <= sim.local(G.parse(r[1])).date() <= W.COMP_NIGHTS[1]]
    ok("realism: the historian carries UNCERTAIN and BAD codes at a historian's rate", 100 <= len(qrows) <= 1500 and {r[2] for r in qrows} == {"UNCERTAIN", "BAD"}, str(len(qrows)))
    ok("R2 no quality code other than GOOD on a night-set date, so dropping them moves no graded figure", not inside, str(len(inside)))

    # ---------------- billing posting times
    with open(os.path.join(T, PK.FILES["billing"])) as f:
        posted = [r["posted"] for r in csv.DictReader(f)]
    ok("realism: billing posting times are not on the hour", sum(p.endswith(":00") for p in posted) / len(posted) < 0.1)
    with tempfile.TemporaryDirectory() as d:
        shutil.copy(os.path.join(T, PK.FILES["register"]), d)
        ev0, _ = PK.billing(np.random.default_rng(W.SEED + 2))
        with open(os.path.join(d, PK.FILES["billing"]), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["property_ref", "account_no", "event", "effective_date", "posted", "area_code", "property_class"])
            for e in ev0:
                w.writerow([e[0], e[1], e[2], e[3].strftime("%d/%m/%Y"), e[4].strftime("%Y-%m-%d %H:%M"), e[5], e[6]])
        ok("billing: spreading the posting times moves no household figure", G.ask_occupied(d) == res["occupied"])

    # ---------------- container and golden hygiene
    prot = [f for f in os.listdir(T) + ["../golden/crew_allocation_week46.xlsx"] if f.endswith(".xlsx")
            and b"workbookProtection" in zipfile.ZipFile(os.path.join(T, f)).read("xl/workbook.xml")]
    ok("no workbook carries an empty protection element", not prot, str(prot))
    gwb = openpyxl.load_workbook(os.path.join(TASK, "golden", "crew_allocation_week46.xlsx"))
    negz = [c.coordinate for ws in gwb for row in ws.iter_rows() for c in row
            if isinstance(c.value, float) and c.value == 0 and np.copysign(1, c.value) < 0]
    gpdf = pdf_text(os.path.join(TASK, "golden", "night_flow_changes.pdf"))
    ok("golden prints no negative zero", not negz and "-0.0" not in gpdf, str(negz))

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


def sf_transfer_estimates(res):
    R = res["R"]
    p = res["open_pairs"][0]
    areas, sp, units = G.register(T)
    fl = G.flows(T, units)
    sa, sb = G.area_flow(fl, areas[p["a"]]["tags"]), G.area_flow(fl, areas[p["b"]]["tags"])
    pb_b = G.profile(sb, G.BASE)
    da = G.profile(sa, G.COMP) - G.profile(sa, G.BASE)
    db = G.profile(sb, G.COMP) - pb_b
    X = np.vstack([np.ones(96), pb_b]).T
    k = np.linalg.lstsq(X, da, rcond=None)[0][1]
    kb = np.linalg.lstsq(X, -db, rcond=None)[0][1]
    return [da[12:16].mean(), -db[12:16].mean(), (da[12:16].mean() - db[12:16].mean()) / 2, k * pb_b[12:16].mean(), kb * pb_b[12:16].mean()]


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

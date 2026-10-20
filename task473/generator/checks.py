"""task473 checks: the three rules on the clean truth (R1 to R3c), the call and the ladder read from the bundle, the
golden completion's family, the semantic fork table (SF1 to SF14), the Layer 1 items' neutrality, the asks and their
devices, every graded figure's distance to its bin edge, the input gates and distractors, the realism sweeps and the
deliverables' agreement with figures.json."""
import csv
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile

import bundle as B
import methods as M
import truth as T
import world as W

RESULTS = []
GOLD = ["Corwin", "Hatchell", "Ossian", "Tanager"]
LADDER = {"R0": ["Corwin", "Hatchell", "Ossian"], "R6": ["Corwin", "Hatchell", "Ossian", "Pruett"],
          "R2": ["Corwin", "Hatchell", "Ossian"], "R8": ["Brisbin", "Corwin", "Hatchell", "Ossian"],
          "R5": ["Corwin", "Hatchell", "Ossian", "Pruett"], "G": GOLD}


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %s%s" % ("ok  " if ok else "FAIL", label, ("  [%s]" % (detail,)) if (detail != "" and not ok) else ""))
    return ok


def pdf_text(path):
    out = subprocess.run(["pdftotext", "-raw", path, "-"], capture_output=True, text=True, check=True).stdout
    return re.sub(r"\s+", " ", out)


def xlsx_text(path):
    with zipfile.ZipFile(path) as z:
        return " ".join(z.read(n).decode("utf-8", "replace") for n in z.namelist() if n.endswith(".xml"))


def edge(v, unit):
    return unit / 2.0 - abs(v - round(v / unit) * unit)


def names(s):
    return sorted(W.NAMES[f] for f in s)


def call(rates):
    return names(f for f, v in rates.items() if v >= W.THRESHOLD)


def run(target, golden, x=None, meta_path=None, fig_path=None):
    del RESULTS[:]
    F = json.load(open(fig_path)) if fig_path else None
    files = sorted(os.listdir(target))
    dr = B.directory(target)
    cr = B.census(target, dr)
    comp = B.complete_agencies(dr)
    obs = B.observed(cr, comp)
    miles = B.vmt(target)
    g = B.golden_g(obs, miles)
    rates, deaths = g["rates"], g["deaths"]
    gold = call(rates)
    gd = {f: int(round(deaths[f])) for f in miles}
    gr = {f: "%.2f" % rates[f] for f in miles}

    # ------------------------------------------------------------------ input gates
    fmts = {f.rsplit(".", 1)[1] for f in files}
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files
              if f.endswith(".csv"))
    check("gates: %d files (10 or more), formats %s (3 or more), the largest %d rows (25,000 or more)" % (
        len(files), sorted(fmts), big), len(files) >= 10 and len(fmts) >= 3 and big >= 25000)
    check("gates: the pack is exactly the files world.FILES declares", set(files) == set(W.FILES.values()),
          sorted(set(files) ^ set(W.FILES.values())))

    # ------------------------------------------------------------------ the call
    check("call: the bundle certifies %s" % ", ".join(GOLD), gold == GOLD, gold)
    near = sorted((abs(v / W.THRESHOLD - 1), W.NAMES[f]) for f, v in rates.items())[0]
    check("call: every county at least 5 per cent from the 0.60 line (closest %s, %.1f per cent)" % (
        near[1], 100 * near[0]), near[0] >= 0.05)
    check("call: Tanager at least 9 per cent above the line (%.4f)" % rates["027"], rates["027"] >= 0.654)
    check("call: the catch rates at the agencies that test every surviving driver are %.4f and %.4f" % (
        g["catch"][0], g["catch"][1]), abs(g["catch"][0] - 2 / 7) < 1e-12 and abs(g["catch"][1] - 8 / 9) < 1e-12)

    # ------------------------------------------------------------------ R1 to R3: the three rules
    person_heads = open(os.path.join(target, W.FILES["person23"]), encoding="utf-8").readline() + \
        open(os.path.join(target, W.FILES["person2425"]), encoding="utf-8").readline()
    nd = sum(1 for c in cr for p in c["persons"] if p["role"] == "driver")
    check("R1 the field's raw material ships: %d driver rows with each driver's test, result and arrest at the scene "
          "in both layouts, and no shipped column holds a completed count, a chance or a catch rate" % nd,
          nd > 3000 and all(k in person_heads for k in ("ALC_TST", "ALC_RES", "DWI_ARR", "alcohol_test",
                                                        "alcohol_result", "arrested_at_scene")) and
          not any(re.search(r"expect|impute|probab|catch|weight|complet|ai_driving|impaired_deaths", open(
              os.path.join(target, f), encoding="utf-8").readline(), re.I) for f in files if f.endswith(".csv")))
    if x is not None:
        tobs = T.observe(x["crashes"])
        tv = x["vmt"]
        tr = {r: call(M.rate(M.route(tobs, r), tv)) for r in ("R6", "R6c", "R8", "G")}
        true = {}
        for c in x["crashes"]:
            if T.ai(c):
                true[c.fips] = true.get(c.fips, 0) + T.deaths(c)
        check("R3a analyst test on the clean truth: one share of unarrested drivers impaired, from the agencies that "
              "test everyone, every filed rule applied, certifies %s (the default path's Ends on)" % ", ".join(
                  LADDER["R6"]), tr["R6"] == LADDER["R6"], tr["R6"])
        check("R3b the decisive step alone on the clean truth (each arrested positive at one over its band's catch "
              "rate) certifies the golden four", tr["G"] == GOLD, tr["G"])
        check("R3b each lower rung's single correction stays wrong on the clean truth: each county's own share "
              "(%s), one catch rate for every BAC (%s)" % (", ".join(tr["R6c"]), ", ".join(tr["R8"])),
              tr["R6c"] != GOLD and tr["R8"] != GOLD)
        check("R3b the true alcohol-impaired-driving deaths (every driver's BAC known) certify the same four",
              call({f: true.get(f, 0) / tv[f] * 1e8 for f in tv}) == GOLD)
        check("R3 the bundle's completed deaths equal the generator's for every county",
              all(abs(deaths[f] - M.route(tobs, "G")[f]) < 1e-6 for f in miles))
    docs = {k: pdf_text(os.path.join(target, W.FILES[k])) for k in ("guidelines", "manual", "crs_notes",
                                                                       "lab_annual")}
    docs["lab_notes"] = re.sub(r"\s+", " ", open(os.path.join(target, W.FILES["lab_notes"]), encoding="utf-8").read())
    for k in ("agencies", "vmt", "licensed"):
        docs[k] = xlsx_text(os.path.join(target, W.FILES[k]))
    control = {"guidelines": "A county whose rate is 0.60 or more is high-range.",
               "manual": "the Corwin County and Ossian County sheriffs follow the same procedure",
               "crs_notes": "A report as it stands is its latest accepted version.",
               "lab_annual": "Kits received, 2025", "lab_notes": "An agency may submit a second specimen",
               "agencies": "Each State Patrol post patrols the county shown", "vmt": "Annual vehicle miles traveled",
               "licensed": "Licensed drivers"}
    check("R3c positive controls: each document's text is read through the extractor the absence checks use",
          all(control[k] in docs[k] for k in control), [k for k in control if control[k] not in docs[k]])
    banned = r"catch|detect|BAC band|bands|weight|inverse|imput|Horvitz|capture|probab|untested drivers|" \
             r"high-range counties are|notic"
    hits = {k: re.findall(banned, v, re.I) for k, v in docs.items() if k in ("guidelines", "manual", "crs_notes",
                                                                             "lab_annual", "lab_notes")}
    check("R3c no plant: no document names a catch rate, a BAC band, a weight, an imputation or an officer's "
          "noticing", not any(hits.values()), {k: v for k, v in hits.items() if v})
    county_hits = {k: [n for n in W.NAMES.values() if n in docs[k]] for k in ("guidelines", "crs_notes", "lab_annual",
                                                                               "lab_notes")}
    check("R3c no document ranks or names a county (the manual names only the two sheriffs that test everyone)",
          not any(county_hits.values()) and [n for n in W.NAMES.values() if n in docs["manual"]] == ["Corwin",
                                                                                                    "Ossian"],
          county_hits)
    check("R3c no memo, briefing, draft, earlier list or stakeholder figure ships",
          not any(re.search(r"memo|draft|briefing|list|rank", f, re.I) for f in files))

    # ------------------------------------------------------------------ the ladder, read from the bundle
    rr = {r: M.rate(M.route(obs, r), miles) for r in M.ROUTES}
    for r, want in LADDER.items():
        got = call(rr[r])
        m = min(abs(v / W.THRESHOLD - 1) for v in rr[r].values())
        check("ladder %s certifies %s (closest county %.1f per cent from the line)" % (r, ", ".join(want), 100 * m),
              got == want and m >= 0.03, got)
    for r in ("R1", "R6c", "R4", "R3"):
        got = call(rr[r])
        check("ladder %s certifies another set (%s)" % (r, ", ".join(got)), got != GOLD, got)
    check("ladder every route but the golden certifies a set with Tanager out or another county in",
          all(call(rr[r]) != GOLD for r in M.ROUTES if r != "G"))
    for r in ("R0", "R6", "R6c", "R2", "R8", "R5"):
        check("ladder %s leaves Tanager below the line (%.4f)" % (r, rr[r]["027"]), rr[r]["027"] < W.THRESHOLD - 0.01)
    if F:
        check("ladder the default path's share of unarrested drivers at .08 or more is %s per cent and one catch "
              "rate for every BAC %s per cent" % (F["share_pct"], F["one_catch_pct"]),
              6.0 < float(F["share_pct"]) < 8.0 and 50.0 < float(F["one_catch_pct"]) < 65.0)
    # the complete agencies separate the candidates: the catch rate is the same in every sub-band of a band, at the
    # State Patrol and at the two sheriffs, while one rate for every BAC is not
    sb6 = M.catch_rates(obs, subbands=M.G_FAMILY["six_subbands"]["subbands"])
    check("ladder the catch rate is the same in each sub-band of a band (%s)" % ", ".join("%.3f" % v for v in
                                                                                          sb6.values()),
          all(abs(sb6[i] - g["catch"][0]) < 1e-12 for i in (0, 1, 2)) and
          all(abs(sb6[i] - g["catch"][1]) < 1e-12 for i in (3, 4, 5)))
    sp = M.catch_rates(obs, agencies={"SP"})
    so = M.catch_rates(obs, agencies={"SO00500", "SO01900"})
    check("ladder the catch rate is the same at the State Patrol and at the two sheriffs",
          all(abs(sp[b] - g["catch"][b]) < 1e-12 and abs(so[b] - g["catch"][b]) < 1e-12 for b in (0, 1)))
    found = {}
    for c in obs:
        for d in c["drivers"]:
            if not d["killed"] and not d["complete"] and d["tested"] and d["bac"] >= 0.08:
                found.setdefault(c["fips"], [0, 0])[0 if d["bac"] < 0.15 else 1] += 1
    hi_share = {f: v[1] / float(sum(v)) for f, v in found.items() if sum(v) >= 8}
    check("ladder the arrest-only counties' positives sit at different bands (share at .15 or more %.2f to %.2f): "
          "Tanager's half below .15, Brisbin's all above" % (min(hi_share.values()), max(hi_share.values())),
          hi_share["027"] <= 0.5 and hi_share["003"] > 0.9)

    bt, e_ipw, e_pool = B.backtest(obs)
    check("ladder R6 dies to the State Patrol's own record: each post held out and completed from its arrests, the "
          "catch rates miss its unarrested drivers at .08 or more by %.2f (root mean square over %d posts), the one "
          "unarrested share by %.2f" % (e_ipw, len(bt), e_pool), len(bt) == 14 and e_pool > 2.5 * e_ipw)
    worse = sum(1 for v in bt.values() if abs(v[2] - v[0]) > abs(v[1] - v[0]))
    check("ladder the pooled share misses worse at %d of 14 posts" % worse, worse >= 9)

    # ------------------------------------------------------------------ the golden family and the fork table
    fam = M.g_family(obs)
    f365 = B.vmt(target, days={2023: 365, 2024: 365, 2025: 365})
    for k, d in fam.items():
        rt = M.rate(d, miles)
        check("SF10/SF11/SF12 the golden family's %s: the same call, every county's deaths in the same whole number "
              "and rate in the same two-decimal cell" % k, call(rt) == gold and
              all(int(round(d[f])) == gd[f] and "%.2f" % rt[f] == gr[f] for f in miles),
              [W.NAMES[f] for f in miles if int(round(d[f])) != gd[f] or "%.2f" % rt[f] != gr[f]])
    lo = {f: min(fam[k][f] for k in fam) for f in miles}
    hi = {f: max(fam[k][f] for k in fam) for f in miles}
    check("SF8 vehicle miles with 365 days in 2024: the same call and every rate in its cell under every member of "
          "the family", all("%.2f" % (hi[f] / f365[f] * 1e8) == gr[f] and "%.2f" % (lo[f] / miles[f] * 1e8) == gr[f]
                            for f in miles))
    check("SF1 'high-range' at 0.60 or more: no county within 0.005 of 0.60, so 'more than' agrees",
          min(abs(v - W.THRESHOLD) for v in rates.values()) > 0.005)
    check("SF14 high-range read on the rounded rate gives the same call", names(f for f in miles if float(gr[f]) >= 0.6)
          == gold)
    late = [p for c in cr for p in c["persons"] if p["death"] and not p["killed"]]
    in26 = [p for c in cr for p in c["persons"] if p["killed"] and p["death"] and p["death"].year > 2025]
    check("SF2 the window by crash date: no death in the window's crashes falls after 2025, so the death date "
          "selects the same deaths", not in26 and all(c["date"].year in (2023, 2024, 2025) for c in cr))
    alt = B.golden_g(B.observed(cr, comp, late_deaths=True), miles)
    check("SF3 the %d deaths recorded more than 30 days after a crash, counted: the same call and every figure "
          "(their crashes had every driver tested below .08)" % len(late),
          len(late) >= 4 and call(alt["rates"]) == gold and
          all(int(round(alt["deaths"][f])) == gd[f] for f in miles))
    alt = B.golden_g(B.observed(cr, comp, roles=("driver", "pedalcyclist")), miles)
    check("SF4 pedalcyclists read as drivers: the same call and every figure",
          call(alt["rates"]) == gold and all("%.2f" % alt["rates"][f] == gr[f] for f in miles))
    alt = B.golden_g(B.observed(cr, comp, roles=("driver", "pedestrian")), miles)
    check("SF4 pedestrians read as drivers %s; ruled out by guidelines 2.3" % (
        "keeps the call" if call(alt["rates"]) == gold else "moves the call (%s)" % ", ".join(call(alt["rates"]))),
        "pedestrians and pedalcyclists are not drivers" in docs["guidelines"])
    alt = B.golden_g(B.observed(cr, comp, unidentified=True), miles)
    check("SF4 the drivers who left the scene unidentified completed as untested drivers: the same call",
          call(alt["rates"]) == gold and "never identified is not counted as a driver" in docs["guidelines"])
    edge_bac = [p for c in cr for p in c["persons"] if p["role"] == "driver" and p["tested"] and p["bac"] in (0.08, 0.15)]
    check("SF5 no driver's result sits exactly on .08 or .15, and every result is the laboratory's whole-blood one",
          not edge_bac and "whole blood" in docs["manual"])
    vit = [p for c in cr for p in c["persons"] if p["test"] in ("3", "VITREOUS")]
    check("SF6 the %d vitreous results are all killed passengers and pedestrians, so reading vitreous as no test "
          "moves nothing" % len(vit), len(vit) > 0 and all(p["role"] != "driver" for p in vit))
    check("SF7 every census crash's investigating agency is in the crash's county (the crash county and the agency's "
          "agree)", all(str(dr["agencies"][c["agency"]]["county_fips"]) == c["fips"] for c in cr))
    by_year = {}
    for c, o in zip(cr, obs):
        by_year.setdefault(c["year"], []).append(o)
    yr_miles = {}
    sh = B.xlsx_sheets(B.find(target, "dot_county_dvmt"))
    for y in (2023, 2024, 2025):
        rows = sh["DVMT %d" % y]
        for r in rows[1:]:
            if r[0]:
                yr_miles[(str(r[0]), y)] = sum(float(v) for v in r[2:-1]) * 1000.0 * (366 if y == 2024 else 365)
    q = {f: g["missed"].get(f, 0.0) / n for f, n in g["untested"].items()}

    def yr_deaths(os_):
        out = {}
        for o in os_:
            ds = [d for d in o["drivers"] if d["identified"]]
            if any(d["tested"] and d["bac"] >= 0.08 for d in ds):
                p = 1.0
            else:
                keep = 1.0
                for d in ds:
                    if not d["tested"]:
                        keep *= 1.0 - q.get(o["fips"], 0.0)
                p = 1.0 - keep
            out[o["fips"]] = out.get(o["fips"], 0.0) + o["deaths"] * p
        return out
    yd = {y: yr_deaths(v) for y, v in by_year.items()}
    mean_rate = {f: sum(yd[y].get(f, 0.0) / yr_miles[(f, y)] * 1e8 for y in yd) / 3.0 for f in miles}
    check("SF9 the mean of the three annual rates: the same call", call(mean_rate) == gold)
    check("SF13 every killed driver was tested (none to complete)",
          all(p["tested"] for c in cr for p in c["persons"] if p["role"] == "driver" and p["killed"]))
    check("SF2/SF3/SF4 the guidelines file the population, the window, the drivers, the rate and the line",
          all(s in docs["guidelines"] for s in ("died within 30 days of a crash on a public road",
                                                 "that occurred in 2023, 2024 or 2025",
                                                 "whether or not that driver was tested",
                                                 "each crash counts its deaths times the chance",
                                                 "per 100 million vehicle miles")))

    # ------------------------------------------------------------------ Layer 1, each item read the natural wrong way
    old = {r["AGCY"] for r in B.read_csv(B.find(target, "fcc_2023_crash"))}
    by_name = {a["agency_name"]: a for a in dr["agencies"].values()}
    check("L1 the 2011 form's four-digit agency codes each map through the directory's former code to one agency "
          "(%d codes)" % len(old), all(o in dr["by_old"] for o in old))
    check("L1 the 2011 form's results in thousandths read as g/dL: every 2023 tested driver's result is under 0.4 "
          "after the division and none before it", all(p["bac"] < 0.4 for c in cr if c["year"] == 2023
                                                       for p in c["persons"] if p["tested"]))
    alt = B.golden_g(obs, f365)
    check("L1 the DOT's daily miles times 365 every year: the same call", call(alt["rates"]) == gold)
    serum = [r for r in B.lab(target) if r["specimen"] == "SER" and r["case_type"] in ("FATAL CRASH",
                                                                                       "DEATH INVESTIGATION")]
    check("L1 no census driver's result is a serum result (the laboratory's serum results are arrests away from "
          "fatal crashes)", not serum)

    # ------------------------------------------------------------------ the asks
    rows = B.lab(target)
    a = B.ask_a(rows, dr)
    crk = B.ask_a(rows, dr, merge_jail=False)
    hq = B.ask_a(rows, dr, county_of=lambda ag, case, k: str(dr["agencies"][ag]["county_fips"]))
    miss_h = [W.NAMES[f] for f in miles if hq.get(f, (0, 0))[0] == a[f][0]]
    check("ask A stop: the State Patrol's arrests at headquarters misses every county's arrests", not miss_h, miss_h)
    site = B.sites(target)
    sit = B.ask_a(rows, dr, county_of=lambda ag, case, k: site[k["site"]]["county_fips"])
    utc = B.ask_a(rows, dr, year_of=lambda k: int(k["utc"][:4]))
    miss_c = [W.NAMES[f] for f in miles if crk.get(f, (0, 0))[0] == a[f][0] or "%.1f" % crk.get(f, (0, 0))[1] ==
              "%.1f" % a[f][1]]
    check("ask A cracker (one arrest per agency case number, the State Patrol's by its post, every documented hazard "
          "repaired, the jail's second submissions kept) misses every county's arrests and per cent", not miss_c, miss_c)
    pairs = {}
    for r in rows:
        if r["case_type"] == "DUI":
            pairs.setdefault((r["collection_site"], r["collected_utc"]), set()).add((r["submitting_agency"],
                                                                                     r["agency_case_number"]))
    multi = [v for v in pairs.values() if len(v) > 1]
    check("ask A device: %d draws submitted twice, each a police department's and the sheriff's of one county jail, "
          "and no two arrests drawn at one site in one minute otherwise" % len(multi),
          len(multi) >= 28 and all(len(v) == 2 and sum(1 for ag, cs in v if ag.startswith("SO")) == 1 and
                                   sum(1 for ag, cs in v if ag.startswith("PD")) == 1 for v in multi))
    miss_s = [W.NAMES[f] for f in miles if sit.get(f, (0, 0))[0] == a[f][0] and
              "%.1f" % sit.get(f, (0, 0))[1] == "%.1f" % a[f][1]]
    same_n = [W.NAMES[f] for f in miles if sit.get(f, (0, 0))[0] == a[f][0]]
    check("ask A the collection site's county misses every county's arrests or per cent (%d counties' arrests "
          "unchanged)" % len(same_n), not miss_s and len(same_n) <= 2, (miss_s, same_n))
    moved = [W.NAMES[f] for f in miles if utc.get(f, (0, 0))[0] != a[f][0]]
    check("ask A hazard: the year read on UTC moves %d counties' arrests" % len(moved), len(moved) >= 4)
    kit_cases = {}
    for r in rows:
        if r["case_type"] == "DUI":
            kit_cases.setdefault((r["submitting_agency"], r["agency_case_number"]), set()).add(r["lab_number"])
    seconds = sum(1 for v in kit_cases.values() if len(v) > 1)
    tubes = sum(1 for r in rows if r["tube"] == "2")
    amended = sum(1 for r in rows if r["report_status"] == "AMENDED")
    check("ask A hazards present: %d arrests with a second specimen, %d second-tube rows, %d amended reports" % (
        seconds, tubes, amended), seconds > 100 and tubes > 100 and amended > 100)
    sp = [r for r in rows if r["submitting_agency"] == "SPHQ000" and r["case_type"] == "DUI"]
    check("ask A device: the State Patrol's %d DUI rows are all under SPHQ000 with a post-numbered case" % len(sp),
          sp and all(re.fullmatch(r"P\d\d-\d\d-\d{5}", r["agency_case_number"]) for r in sp) and
          not any(r["submitting_agency"].startswith("SP0") or r["submitting_agency"].startswith("SP1") for r in rows))
    reps_b, groups = B.ask_b(target, cr)
    nodup, _ = B.ask_b(target, cr, dedupe=False, link_census=False)
    miss_n = [W.NAMES[f] for f in miles if nodup.get(f, 0) == reps_b.get(f, 0)]
    check("ask B stop: every report counted on its own severity misses every county", not miss_n, miss_n)
    bynum, _ = B.ask_b(target, cr, link_near=False, late_k=False)
    miss_b = [W.NAMES[f] for f in miles if bynum.get(f, 0) == reps_b.get(f, 0)]
    check("ask B cracker (latest accepted version, two agencies' reports merged, the census linked by agency and "
          "report number, severity A to C) misses every county", not miss_b, miss_b)
    linked, _ = B.ask_b(target, cr, late_k=False)
    miss_k = [W.NAMES[f] for f in miles if linked.get(f, 0) == reps_b.get(f, 0)]
    check("ask B device: the census linked in full, a report whose supplement records a death after 30 days dropped "
          "as fatal, misses every county (the measured readers' path)", not miss_k, miss_k)
    cen25 = {(c_["agency"], c_["report"]) for c_ in cr if c_["year"] == 2025}
    late_rows = [v for g_ in groups for v in g_ if v["severity"] == "K" and
                 (v["agency_id"], v["report_number"]) not in cen25]
    check("ask B fair: each K report outside the census is a supplement submitted more than 30 days after its crash "
          "(%d reports)" % len(late_rows), late_rows and all(
              (dt.date.fromisoformat(v["submitted"]) - dt.date.fromisoformat(v["crash_date"])).days > 30
              for v in late_rows if not any((w["agency_id"], w["report_number"]) in cen25
                                            for g_ in groups if v in g_ for w in g_)))
    dups = {}
    for gr_ in groups:
        if len(gr_) > 1:
            dups[gr_[0]["county_fips"]] = dups.get(gr_[0]["county_fips"], 0) + 1
    check("ask B device: every county has crashes two agencies reported (%d to %d)" % (min(dups.values()),
                                                                                       max(dups.values())),
          len(dups) == 14 and min(dups.values()) >= 2)
    false_pairs = [gr_ for gr_ in groups if len(gr_) > 2 or (len(gr_) == 2 and gr_[0]["agency_id"] ==
                                                               gr_[1]["agency_id"])]
    check("ask B the same-crash match is unambiguous: every pair is two agencies, no group of three", not false_pairs)
    if x is not None:
        import crs as R
        tb = R.ask_b(x["crs"])
        check("ask B the bundle's counts equal the generator's", all(reps_b.get(f, 0) == tb[f] for f in miles))
        import pack as P
        ta = P.ask_a(x["arrests"])
        check("ask A the bundle's arrests and per cents equal the generator's",
              all(a[f][0] == ta[f][0] and abs(a[f][1] - ta[f][1]) < 1e-9 for f in miles))
    check("asks free of the call: the call reads no laboratory or crash records row (the bundle's completion reads "
          "the census and the miles only)", gold == GOLD)

    # ------------------------------------------------------------------ bins
    dm = min(min(fam[k][f] for k in fam) - (gd[f] - 0.5) for f in miles)
    dM = min((gd[f] + 0.5) - max(fam[k][f] for k in fam) for f in miles)
    check("bins: every county's deaths at least 0.2 inside its whole number under the whole family (%.2f, %.2f)" % (
        dm, dM), dm >= 0.2 and dM >= 0.2)
    re_ = min(min(edge(lo[f] / miles[f] * 1e8, 0.01), edge(hi[f] / f365[f] * 1e8, 0.01)) for f in miles)
    check("bins: every rate at least 0.002 inside its two-decimal cell under the family and 365 days (%.4f)" % re_,
          re_ >= 0.002)
    ea = min(edge(a[f][1], 0.1) for f in miles)
    check("bins: every per cent at .15 or more at least 0.012 inside its one-decimal cell (%.3f)" % ea, ea >= 0.012)
    check("bins: no rate prints the same as the line (0.60)", all(gr[f] != "0.60" for f in miles))

    # ------------------------------------------------------------------ distractors
    for k in W.DISTRACTORS:
        tmp = tempfile.mkdtemp()
        try:
            for f in files:
                if f != W.FILES[k]:
                    shutil.copy(os.path.join(target, f), tmp)
            d2 = B.directory(tmp)
            c2 = B.census(tmp, d2)
            g2 = B.golden_g(B.observed(c2, B.complete_agencies(d2)), B.vmt(tmp))
            a2 = B.ask_a(B.lab(tmp), d2)
            b2, _ = B.ask_b(tmp, c2)
            check("distractor %s deleted: the call and every graded figure unchanged" % W.FILES[k],
                  call(g2["rates"]) == gold and all("%.2f" % g2["rates"][f] == gr[f] for f in miles) and
                  a2 == a and b2 == reps_b)
        finally:
            shutil.rmtree(tmp)
    lic = B.xlsx_sheets(B.find(target, "dmv_licensed"))["Licensed drivers 2025"]
    check("distractor: the licensed drivers file counts drivers by county of residence (another denominator; the "
          "guidelines put the rate on vehicle miles)", len(lic) == 15 and all(isinstance(r[2], int) for r in lic[1:])
          and "vehicle miles traveled" in docs["guidelines"])
    pre = B.read_csv(B.find(target, "fcc_2026_preliminary"))
    check("distractor: the 2026 preliminary file is 2026 only and preliminary", all(r["crash_date"].startswith("2026")
                                                                                    for r in pre) and
          all(r["record_status"].startswith("PRELIMINARY") for r in pre))

    # ------------------------------------------------------------------ every PDF through three readers (H25)
    import pdfplumber
    from pypdf import PdfReader
    pdfs = [os.path.join(target, f) for f in files if f.endswith(".pdf")]
    if golden:
        pdfs += [os.path.join(golden, f) for f in os.listdir(golden) if f.endswith(".pdf")]
    bad3 = []
    for p in pdfs:
        try:
            rd = PdfReader(p, strict=True)
            t1 = re.sub(r"\s+", " ", " ".join(pg.extract_text() or "" for pg in rd.pages))
            with pdfplumber.open(p) as pl:
                t2 = re.sub(r"\s+", " ", " ".join(pg.extract_text() or "" for pg in pl.pages))
            t3 = pdf_text(p)
            words = [w for w in re.findall(r"[A-Za-z]{6,}", t3)][:40]
            if not (len(t1) > 500 and len(t2) > 500 and all(w in t1 and w in t2 for w in words)):
                bad3.append(os.path.basename(p))
        except Exception as e:
            bad3.append("%s: %s" % (os.path.basename(p), e))
    check("realism H25: every PDF (%d) opens under a strict reader and reads the same through pypdf, pdfplumber and "
          "pdftotext" % len(pdfs), not bad3, bad3)

    # ------------------------------------------------------------------ realism and consistency
    dash = []
    for f in files:
        p = os.path.join(target, f)
        txt = pdf_text(p) if f.endswith(".pdf") else (xlsx_text(p) if f.endswith(".xlsx") else
                                                       open(p, encoding="utf-8").read())
        if re.search("[–—]", txt):
            dash.append(f)
    check("realism: no en or em dash in any shipped file", not dash, dash)
    cases = [c["case"] for c in cr]
    reports = [(c["agency"], c["report"]) for c in cr]
    check("realism: census case numbers and agency report numbers unique", len(set(cases)) == len(cases) and
          len(set(reports)) == len(reports))
    lab_ids = {}
    bad = 0
    for r in rows:
        key = r["lab_number"]
        sig = (r["case_type"], r["submitting_agency"], r["agency_case_number"], r["collected_utc"])
        if lab_ids.setdefault(key, sig) != sig:
            bad += 1
    check("realism: every lab number is one kit (one case, agency and collection time)", bad == 0, bad)
    ok_dates = all(r["collected_utc"][:10] <= r["received_date"] <= r["report_date"] <= "2027-03-12" for r in rows)
    check("realism: every specimen collected before it was received and reported before the 12 March 2027 extract",
          ok_dates and min(r["received_date"] for r in rows) >= "2023-01-01" and
          max(r["received_date"] for r in rows) <= "2026-01-15")
    reps, units = B.crs(target)
    check("realism: every crash report is a 2025 crash submitted after it and before the 8 March 2027 extract",
          all(r["crash_date"].startswith("2025") and r["crash_date"] <= r["submitted"] <= "2027-03-08" for r in reps))
    linked = {(r["agency_id"], r["report_number"]) for r in reps}
    c25 = [c for c in cr if c["year"] == 2025]
    by_num = sum(1 for c in c25 if (c["agency"], c["report"]) in linked)
    check("realism: %d of the census's %d 2025 crashes carry their crash report's number, the rest the agency's "
          "death investigation number (a county or city crash whose victim died after the report)" % (by_num, len(c25)),
          0.3 * len(c25) < by_num < len(c25))
    yearly = {}
    for c in cr:
        yearly.setdefault(c["fips"], []).append(c["year"])
    ties = [W.NAMES[f] for f, v in yearly.items() if len({v.count(y) for y in (2023, 2024, 2025)}) < 3]
    check("realism sweep: the counties' fatal crashes vary year to year (equal counts in two years in %d counties, "
          "as chance gives)" % len(ties), len(ties) <= 2, ties)
    check("realism sweep: the state's totals are not round (deaths %d, 2025 arrests %d, injury crashes %d)" % (
        sum(gd.values()), sum(v[0] for v in a.values()), sum(reps_b.values())),
          sum(gd.values()) % 10 and sum(v[0] for v in a.values()) % 10 and sum(reps_b.values()) % 10)
    check("realism: the documents' dates precede what they describe (guidelines 9 February 2027, the extracts of "
          "8 and 12 March 2027, the annual report of 6 March 2027, all before the 22 March 2027 as-of)",
          "Issued 9 February 2027" in docs["guidelines"] and "8 March 2027" in docs["crs_notes"] and
          "12 March 2027" in docs["lab_notes"] and "6 March 2027" in docs["lab_annual"])
    if golden and F:
        with open(os.path.join(golden, W.GOLDEN["csv"]), encoding="utf-8") as fh:
            gcsv = list(csv.DictReader(fh))
        check("deliverables: the CSV carries each county's deaths, rate and baselines as figures.json does",
              [(r["county"], int(r["ai_driving_deaths_2023_2025"]), r["ai_driving_rate_per_100m_vmt"],
                int(r["arrests_blood_specimen_2025"]), r["pct_arrests_015_or_more_2025"],
                int(r["injury_crashes_drinking_driver_2025"])) for r in gcsv] ==
              [(r["county"], r["deaths"], r["rate"], r["arrests"], r["pct15"], r["crashes"]) for r in F["rows"]])
        check("deliverables: the CSV's figures are the bundle's",
              all(int(r["ai_driving_deaths_2023_2025"]) == gd[r["county_fips"]] and
                  r["ai_driving_rate_per_100m_vmt"] == gr[r["county_fips"]] and
                  int(r["arrests_blood_specimen_2025"]) == a[r["county_fips"]][0] and
                  r["pct_arrests_015_or_more_2025"] == "%.1f" % a[r["county_fips"]][1] and
                  int(r["injury_crashes_drinking_driver_2025"]) == reps_b[r["county_fips"]] for r in gcsv))
        lt = pdf_text(os.path.join(golden, W.GOLDEN["letter"]))
        check("deliverables: the letter certifies the four with their rates and carries every county's row",
              all(("%s (%s)" % (c, v)) in lt or ("%s (%s alcohol" % (c, v)) in lt for c, v in F["high_rates"]) and
              all(r["county"] in lt for r in F["rows"]))
        check("deliverables: the letter carries the chart (the 0.60 line and the 14 bars' labels)",
              "High-range line, 0.60" in lt and "Figure 1." in lt)
    if meta_path:
        meta = json.load(open(meta_path))
        check("metadata: the distractors are named and exist", all(f in files for f in meta["distractor_files"]) and
              len(meta["distractor_files"]) >= 2)
    n_ok = sum(ok for _, ok, _ in RESULTS)
    print("checks: %d of %d pass" % (n_ok, len(RESULTS)))
    return n_ok == len(RESULTS)


if __name__ == "__main__":
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    import pack as P
    ok = run(os.path.join(task, "target"), os.path.join(task, "golden"), x=P.everything(),
             meta_path=os.path.join(task, "metadata.json"), fig_path=os.path.join(here, "figures.json"))
    sys.exit(0 if ok else 1)

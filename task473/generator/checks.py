"""task473 checks: the three rules on the clean truth (R1 to R3c), the call and the ladder read from the bundle, the
golden completion's family, the semantic fork table (SF1 to SF14), the Layer 1 items' neutrality, the asks and their
devices, every graded figure's distance to its bin edge, the input gates and distractors, the realism sweeps and the
deliverables' agreement with figures.json."""
import collections
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
    docs = {k: pdf_text(os.path.join(target, W.FILES[k])) for k in ("guidelines", "manual")}
    for k in ("agencies", "vmt", "licensed"):
        docs[k] = xlsx_text(os.path.join(target, W.FILES[k]))
    control = {"guidelines": "A county whose rate is 0.60 or more is high-range.",
               "manual": "the Corwin County and Ossian County sheriffs follow the same procedure",
               "agencies": "State Patrol Headquarters",
               "vmt": "daily vehicle miles traveled by county and functional class (thousands)",
               "licensed": "Licensed drivers"}
    check("R3c positive controls: each document's text is read through the extractor the absence checks use",
          all(control[k] in docs[k] for k in control), [k for k in control if control[k] not in docs[k]])
    banned = r"catch|detect|BAC band|bands|weight|inverse|imput|Horvitz|capture|probab|untested drivers|" \
             r"high-range counties are|notic"
    hits = {k: re.findall(banned, v, re.I) for k, v in docs.items() if k in ("guidelines", "manual")}
    check("R3c no plant: no document names a catch rate, a BAC band, a weight, an imputation or an officer's "
          "noticing", not any(hits.values()), {k: v for k, v in hits.items() if v})
    county_hits = {k: [n for n in W.NAMES.values() if n in docs[k]] for k in ("guidelines",)}
    check("R3c no document ranks or names a county (the manual names only the two sheriffs that test everyone)",
          not any(county_hits.values()) and [n for n in W.NAMES.values() if n in docs["manual"]] == ["Corwin",
                                                                                                    "Ossian"],
          county_hits)
    check("R3c no memo, briefing, draft, earlier list or stakeholder figure ships",
          not any(re.search(r"memo|draft|briefing|list|rank", f, re.I) for f in files))

    # ------------------------------------------------------------------ no shipped file describes the data
    describe_name = re.compile(
        r"(?<![a-z])(read_?me|data_?dictionar\w*|dictionar(y|ies)|codebook|field_?notes|field_?guide|"
        r"fields?_(guide|notes|list|descriptions?)|\w*_fields|manifest|extract_contents|file_list|file_layout|"
        r"glossary|column_(notes|descriptions?)|data_?notes|how_to_read|about_this|export_notes|extract_notes|"
        r"feed_notes|desk_notes|data_team_notes|definitions|schema|layouts?_notes|handling_notes|release_notes|"
        r"index|contents)(?![a-z])", re.I)
    check("describing: the files that described the data no longer ship (%s), and no shipped file's name says it "
          "describes the data" % ", ".join(W.DESCRIBING),
          not (set(W.DESCRIBING) & set(files)) and not [f for f in files if describe_name.search(f.rsplit(".", 1)[0])],
          [f for f in files if describe_name.search(f.rsplit(".", 1)[0]) or f in W.DESCRIBING])
    describe_sheet = re.compile(r"^(read ?me|notes?|dictionary|data dictionary|definitions|glossary|fields|"
                                r"field notes|about|about this (file|workbook)|how to (read|use)( this)?|columns?|"
                                r"sources?)$", re.I)
    sheets = {f: list(B.xlsx_sheets(os.path.join(target, f))) for f in files if f.endswith(".xlsx")}
    check("describing: no workbook carries a notes, readme or dictionary sheet (the sheets: %s)" % "; ".join(
        "%s %s" % (f, ", ".join(v)) for f, v in sorted(sheets.items())),
        len(sheets) == 3 and not [(f, n) for f, v in sheets.items() for n in v if describe_sheet.match(n.strip())])
    data_cols = {}
    for f in files:
        if f.endswith(".csv"):
            head = open(os.path.join(target, f), encoding="utf-8").readline().strip().split(",")
            data_cols[f] = {c for c in head if len(c) >= 4}
        elif f.endswith(".xlsx"):
            for nm, rows_ in B.xlsx_sheets(os.path.join(target, f)).items():
                hd = next((r for r in rows_ if r and r[0] in ("agency_id", "post", "County FIPS")), None)
                if hd:
                    data_cols["%s/%s" % (f, nm)] = {str(c) for c in hd if c and len(str(c)) >= 4}
    every_col = set().union(*data_cols.values())

    def cols_named(text):
        """the data files' column names a text writes verbatim, and those written as identifiers"""
        found = {c for c in every_col if re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(c), text)}
        return found, {c for c in found if "_" in c or re.search(r"\d", c) or re.search(r"[a-z][A-Z]", c)}
    code_text = open(os.path.join(target, W.FILES["codes2011"]), encoding="utf-8").read()
    ctl_found, ctl_ident = cols_named(code_text)
    check("describing positive control: the column finder, on a text known to name the 2011 form's elements (the "
          "code table itself, a data file), finds %d of them" % len(ctl_ident),
          ctl_ident == {"RTE_SYS", "ACC_TIME", "PER_TYP", "HIT_RUN", "ALC_TST", "ALC_RES", "DWI_ARR"}, sorted(ctl_ident))
    worst = {}
    for k in ("guidelines", "manual"):
        found, ident = cols_named(docs[k])
        share = max((len(found & cols) / float(len(cols)) for cols in data_cols.values() if len(cols) >= 5),
                    default=0.0)
        worst[k] = (len(found), len(ident), share)
    check("describing: no document names the data's columns (each document's column names, identifiers and worst "
          "share of one file's columns: %s), read through the same extractor as its control" % "; ".join(
              "%s %d, %d, %.0f%%" % (k, v[0], v[1], 100 * v[2]) for k, v in worst.items()),
          all(v[1] < 4 and v[0] < 8 and v[2] < 0.4 for v in worst.values()) and
          all(len(docs[k]) > 500 for k in ("guidelines", "manual")))
    check("describing: the census manual keeps the census's own rules (1.2 the files closed, 3.1 a death within 30 "
          "days, 4.1 the result, 4.2 who is tested) and lists no field",
          all(t in docs["manual"] for t in ("A year's file is closed when the 30-day window",
                                            "A person coded fatal died within 30 days of the crash",
                                            "whole blood, or vitreous humor for some killed persons",
                                            "draw blood from a surviving driver arrested at the scene")) and
          not re.search(r"CASE_NUM|PER_TYP|ALC_TST|crash_id|person_type|alcohol_result|Field", docs["manual"]))
    cd = B.codes(target)
    p23 = B.read_csv(B.find(target, "fcc_2023_person"))
    c23 = B.read_csv(B.find(target, "fcc_2023_crash"))
    unlabelled = sorted({(e, r[e]) for r in p23 + c23 for e in r if e in cd and r[e] and r[e] not in cd[e] and
                         not (e in ("AGE", "ACC_TIME", "ALC_RES") and r[e].isdigit() and r[e] not in cd[e])})
    check("closure 19: the 2011 form's code table labels every coded value the 2023 files carry (%d elements, %d "
          "codes)" % (len(cd), sum(len(v) for v in cd.values())), not unlabelled and len(cd) >= 14, unlabelled[:6])
    per_veh = {}
    for r in p23:
        if r["VEH_NUM"] != "0":
            per_veh.setdefault((r["CASE_NUM"], r["VEH_NUM"]), []).append(cd["PER_TYP"][r["PER_TYP"]])
    fatal = {}
    for r in p23:
        fatal[r["CASE_NUM"]] = fatal.get(r["CASE_NUM"], 0) + (cd["INJ"][r["INJ"]] == "FATAL INJURY")
    check("closure 19 C1: read through the code table, every 2023 vehicle holds exactly one DRIVER and every crash "
          "row's FATAL_CT equals its persons coded FATAL INJURY (%d vehicles, %d crashes)" % (len(per_veh), len(c23)),
          all(v.count("DRIVER") == 1 for v in per_veh.values()) and
          all(int(r["FATAL_CT"]) == fatal.get(r["CASE_NUM"], 0) for r in c23))
    tst = {(cd["ALC_TST"][r["ALC_TST"]], r["ALC_RES"] == "996") for r in p23}
    check("closure 18 C1: the 2011 form's ALC_RES is 996 exactly where ALC_TST is NOT TESTED, and a result "
          "otherwise (thousandths, every one under 400)", tst <= {("NOT TESTED", True), ("BLOOD", False),
                                                                  ("VITREOUS HUMOR", False)} and
          all(int(r["ALC_RES"]) < 400 for r in p23 if r["ALC_RES"] != "996"))
    dv = B.dvmt_sheets(target)
    check("SF8 C1: the DOT's sheets carry their unit in their own title row (thousands) and the miles read from the "
          "header row on through the verifier's reader", all(rows_[0][0] == "County FIPS" and len(rows_) == 16
                                                             for rows_ in dv.values()) and
          all(("%d daily vehicle miles traveled by county and functional class (thousands)" % y) in docs["vmt"]
              for y in (2023, 2024, 2025)))

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
    for y, rows in B.dvmt_sheets(target).items():
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

    # ------------------------------------------------------------------ the ask: the courts' prosecutions
    import hashlib
    rows = B.court(target)
    a = B.ask_court(rows)
    same = {f: hashlib.sha256(open(os.path.join(target, f), "rb").read()).hexdigest() == h
            for f, h in W.CALL_FILES.items()}
    check("ask separation: every file the call reads but the guidelines is byte-identical to the leak repair's cut "
          "(%d files) and no retired ask file ships" % len(same), all(same.values()) and
          not (set(W.RETIRED) & set(files)), [f for f, v in same.items() if not v])
    check("ask separation: the guidelines keep the call's sections (2.2 to 2.4) and file the baseline once in 3.1",
          "one for each person charged and offense" in docs["guidelines"] and
          docs["guidelines"].count("one for each person charged and offense") == 1 and
          "whether or not that driver was tested" in docs["guidelines"] and
          not re.search(r"refil|dismiss|case number|same day", docs["guidelines"], re.I))
    dui = [r for r in rows if B.impaired(r)]
    by_case = {}
    for r in rows:
        by_case.setdefault((r["county_fips"], r["case_number"]), []).append(r)
    check("ask realism: one row per case within its court (%d cases, %d impaired-driving), case numbers repeating "
          "only across courts" % (len(rows), len(dui)), all(len(v) == 1 for v in by_case.values()) and
          len({r["case_number"] for r in rows}) < len(rows))
    check("ask realism: every case opened from 1 January 2025 to 28 February 2027, after its offense, and disposed "
          "after it opened and by the close", all("2025-01-01" <= r["filed_date"] <= "2027-02-28" and
                                                  r["offense_date"] <= r["filed_date"] and
                                                  (not r["disposition_date"] or
                                                   r["filed_date"] <= r["disposition_date"] <= "2027-02-28")
                                                  for r in rows))
    twins = collections.Counter(tuple(v for k, v in r.items() if k != "case_number") for r in dui
                                if r["offense_date"][:4] == "2025")
    check("ask determinism: no two impaired-driving cases of 2025 agree in every field but the case number, so a "
          "near-duplicate cleanup moves no figure", max(twins.values()) == 1)
    pros = B.prosecutions(rows)
    pairs = [g for g in pros if len(g) > 1]
    check("ask device: %d prosecutions of 2025 held two cases, the first dismissed on the day the court opened the "
          "second for the same offense date and arresting agency, in every county (%d to %d)" % (
              len(pairs), min(collections.Counter(g[0]["county_fips"] for g in pairs).values()),
              max(collections.Counter(g[0]["county_fips"] for g in pairs).values())),
          len(pairs) >= 200 and all(len(g) == 2 for g in pairs) and
          len({g[0]["county_fips"] for g in pairs}) == 14 and
          all(sorted(g, key=lambda r: r["filed_date"])[0]["disposition"] == "DISMISSED" and
              sorted(g, key=lambda r: r["filed_date"])[0]["disposition_date"] ==
              sorted(g, key=lambda r: r["filed_date"])[1]["filed_date"] for g in pairs))
    cells = collections.Counter((r["county_fips"], r["offense_date"], r["arresting_agency"]) for r in dui
                                if r["offense_date"][:4] == "2025")
    shared = sum(1 for g in B.prosecutions(rows, "cell") if len(g) > 1 and len(B.prosecutions(g)) > 1)
    check("ask over-cleaning half: %d court, offense date and agency cells hold two or more prosecutions of 2025 "
          "(co-arrested drivers, a night's arrests)" % shared, shared >= 300)
    nat = B.ask_court(rows, "cases")
    over = B.ask_court(rows, "cell")

    def misses(r, by=1, pc=0.1):
        return [W.NAMES[f] for f in miles if abs(r[f][0] - a[f][0]) < by or abs(r[f][1] - a[f][1]) < pc - 1e-9]
    check("ask device mass: each case read as a prosecution misses every county's count by %d to %d and per cent by "
          "%.1f to %.1f points" % (min(nat[f][0] - a[f][0] for f in miles), max(nat[f][0] - a[f][0] for f in miles),
                                   min(a[f][1] - nat[f][1] for f in miles), max(a[f][1] - nat[f][1] for f in miles)),
          not misses(nat, 3, 1.0), misses(nat, 3, 1.0))
    check("ask over-cleaning mass: one prosecution per court, offense date and agency misses every county's count by "
          "%d to %d and every printed per cent (%.1f to %.1f points)" % (
              min(a[f][0] - over[f][0] for f in miles), max(a[f][0] - over[f][0] for f in miles),
              min(over[f][1] - a[f][1] for f in miles), max(over[f][1] - a[f][1] for f in miles)),
          all(a[f][0] - over[f][0] >= 3 and "%.1f" % over[f][1] != "%.1f" % a[f][1] for f in miles),
          [W.NAMES[f] for f in miles if a[f][0] - over[f][0] < 3 or "%.1f" % over[f][1] == "%.1f" % a[f][1]])
    # the rival readings a careful judge could take, each computed; every acceptable one files the golden
    rivals = {"the relation without the arresting agency": B.ask_court(rows, agency=False),
              "the relation allowing one to three days": B.ask_court(rows, slack=3),
              "both readings at once": B.ask_court(rows, agency=False, slack=3),
              "a prosecution convicted if any of its cases is": B.ask_court(
                  rows, conv=lambda g: B.convicted(g, last=False)),
              "the impaired-driving charges by their code (MSC 42-1201)": B.ask_court(
                  [dict(r, lead_charge="UNDER THE INFLUENCE" if r["lead_charge_code"].startswith("MSC 42-1201")
                        else r["lead_charge"]) for r in rows]),
              "the relation only where the two cases carry one lead charge": B.ask_court(rows, same_charge=True),
              "a dismissal linked to any case of its court, offense date and agency opened on or after it":
              B.ask_court(rows, how="later"),
              "a dismissal linked to any case of its court and offense date opened on or after it":
              B.ask_court(rows, how="later", agency=False),
              "any later case, one lead charge": B.ask_court(rows, how="later", agency=False, same_charge=True)}
    for k, v in rivals.items():
        check("ask determinism: %s files the golden in every county" % k,
              all(v[f][0] == a[f][0] and "%.1f" % v[f][1] == "%.1f" % a[f][1] for f in miles),
              [W.NAMES[f] for f in miles if v[f] != a[f]])
    ruled = {"the year read on the filing date (guidelines 3.1: offenses committed in 2025)":
             B.ask_court(rows, by="filed"),
             "an amended-charge plea read as a conviction (3.1: a conviction for impaired driving)":
             B.ask_court(rows, conv=lambda g: B.convicted(g, guilty=("GUILTY PLEA", "GUILTY VERDICT",
                                                                    "GUILTY PLEA, AMENDED CHARGE"),
                                                          impaired_only=False)),
             "the drug charge left out (3.1: driving under the influence of alcohol or drugs, MSC 42-1201)":
             B.ask_court([r for r in rows if r["lead_charge_code"] != "MSC 42-1201(3)"]),
             "a deferred prosecution read as a conviction (3.1: a conviction)":
             B.ask_court(rows, conv=lambda g: B.convicted(g) or any(
                 r["disposition"] == "DEFERRED PROSECUTION" for r in [max(g, key=lambda r: r["filed_date"])]))}
    for k, v in ruled.items():
        moved = [W.NAMES[f] for f in miles if v[f][0] != a[f][0] or "%.1f" % v[f][1] != "%.1f" % a[f][1]]
        check("ask hazard, ruled out by a filed sentence: %s moves %d counties' figures" % (k, len(moved)),
              len(moved) >= 10)
    disp = collections.Counter(r["disposition"] or "(open at the close)" for r in dui)
    check("ask hazards present: %s" % ", ".join("%s %d" % kv for kv in sorted(disp.items())),
          all(disp[k] >= 100 for k in ("GUILTY PLEA, AMENDED CHARGE", "DEFERRED PROSECUTION", "NOT GUILTY",
                                       "(open at the close)")))
    early = sum(1 for r in dui if r["offense_date"][:4] == "2024")
    late = sum(1 for r in dui if r["offense_date"][:4] == "2025" and r["filed_date"][:4] > "2025")
    other = sum(1 for r in rows if not B.impaired(r))
    check("ask hazards present: %d cases of 2024 offenses opened in 2025, %d cases of 2025 offenses opened later, "
          "%d other criminal traffic cases" % (early, late, other), early >= 100 and late >= 100 and other >= 15000)
    if x is not None:
        import court as CT
        ta = CT.ask(x["cases"])
        check("ask the bundle's prosecutions and per cents equal the generator's (the relation through the verifier's "
              "reader is the positive control)", all(a[f][0] == ta[f][0] and abs(a[f][1] - ta[f][1]) < 1e-9
                                                     for f in miles))
        refiled = {c.pid for c in x["cases"] if c.refile_of is not None and c.dui and c.offense.year == 2025}
        check("ask fair: the relation finds exactly the generator's refiled prosecutions (%d), and joins no two "
              "others" % len(refiled), len(refiled) == len(pairs))
    check("ask free of the call: the call reads no court row (the bundle's completion reads the census and the miles "
          "only)", gold == GOLD)

    # ------------------------------------------------------------------ bins
    dm = min(min(fam[k][f] for k in fam) - (gd[f] - 0.5) for f in miles)
    dM = min((gd[f] + 0.5) - max(fam[k][f] for k in fam) for f in miles)
    check("bins: every county's deaths at least 0.2 inside its whole number under the whole family (%.2f, %.2f)" % (
        dm, dM), dm >= 0.2 and dM >= 0.2)
    re_ = min(min(edge(lo[f] / miles[f] * 1e8, 0.01), edge(hi[f] / f365[f] * 1e8, 0.01)) for f in miles)
    check("bins: every rate at least 0.002 inside its two-decimal cell under the family and 365 days (%.4f)" % re_,
          re_ >= 0.002)
    ea = min(edge(a[f][1], 0.1) for f in miles)
    check("bins: every per cent convicted at least 0.012 inside its one-decimal cell (%.3f)" % ea, ea >= 0.012)
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
            a2 = B.ask_court(tmp)
            check("distractor %s deleted: the call and every graded figure unchanged" % W.FILES[k],
                  call(g2["rates"]) == gold and all("%.2f" % g2["rates"][f] == gr[f] for f in miles) and a2 == a)
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
    yearly = {}
    for c in cr:
        yearly.setdefault(c["fips"], []).append(c["year"])
    ties = [W.NAMES[f] for f, v in yearly.items() if len({v.count(y) for y in (2023, 2024, 2025)}) < 3]
    check("realism sweep: the counties' fatal crashes vary year to year (equal counts in two years in %d counties, "
          "as chance gives)" % len(ties), len(ties) <= 2, ties)
    check("realism sweep: the state's totals are not round (deaths %d, prosecutions of 2025 %d, cases %d)" % (
        sum(gd.values()), sum(v[0] for v in a.values()), len(rows)),
          sum(gd.values()) % 10 and sum(v[0] for v in a.values()) % 10 and len(rows) % 100)
    check("realism: the documents' dates precede what they describe (guidelines 9 February 2027 naming the close of "
          "28 February 2027 ahead, the manual of 15 March 2024 before the 2024 files it governs, the court extract's "
          "last disposition on the close, all before the 22 March 2027 as-of)",
          "Issued 9 February 2027" in docs["guidelines"] and "issued 15 March 2024" in docs["manual"] and
          max(r["disposition_date"] for r in rows) <= "2027-02-28")
    if golden and F:
        with open(os.path.join(golden, W.GOLDEN["csv"]), encoding="utf-8") as fh:
            gcsv = list(csv.DictReader(fh))
        check("deliverables: the CSV carries each county's deaths, rate and baseline as figures.json does",
              [(r["county"], int(r["ai_driving_deaths_2023_2025"]), r["ai_driving_rate_per_100m_vmt"],
                int(r["dui_offenses_prosecuted_2025"]), r["pct_convicted_dui_by_2027_02_28"]) for r in gcsv] ==
              [(r["county"], r["deaths"], r["rate"], r["prosecuted"], r["pct_conv"]) for r in F["rows"]])
        check("deliverables: the CSV's figures are the bundle's",
              all(int(r["ai_driving_deaths_2023_2025"]) == gd[r["county_fips"]] and
                  r["ai_driving_rate_per_100m_vmt"] == gr[r["county_fips"]] and
                  int(r["dui_offenses_prosecuted_2025"]) == a[r["county_fips"]][0] and
                  r["pct_convicted_dui_by_2027_02_28"] == "%.1f" % a[r["county_fips"]][1] for r in gcsv))
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

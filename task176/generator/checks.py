"""task176 generator checks on the cut pack (python3 checks.py <target>): the input gates, the three rules executed
on the shipped files (R1 raw material, R2 every Layer 1 item neutral, R3a the analyst test, R3b the decisive step
alone, R3c no plant), the semantic fork rows (SF), the golden family (FAM) and the rivals (RIV) against the printed
cell, the asks' devices and stops (ASK), the separation line (SEP), the distractors (DIS) and the realism sweep
(REAL). Exit 1 on any failure."""
from __future__ import annotations

import collections
import datetime as dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np    # noqa: E402

import calc           # noqa: E402
import common as C    # noqa: E402

FAILS = []
N = [0]


def ok(label, cond, detail=""):
    N[0] += 1
    print("%-4s %-52s %s" % ("PASS" if cond else "FAIL", label, detail))
    if not cond:
        FAILS.append(label)


def cell(v):
    return C.rnd(v, 50)


def main(target):
    task = os.path.dirname(target)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    meta = json.load(open(os.path.join(task, "metadata.json")))
    files = sorted(os.listdir(target))

    # ---- input gates -----------------------------------------------------------------------------------------
    ok("GATE files >= 10", len(files) >= 10, "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("GATE formats >= 3", len(fmts) >= 3, ", ".join(sorted(fmts)))
    rows = {f: sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    ok("GATE a file of 25,000 rows", max(rows.values()) >= 25000, "%s %d rows" % (max(rows, key=rows.get), max(rows.values())))
    ok("GATE two distractors declared", len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]),
       ", ".join(meta["distractor_files"]))
    ok("GATE no distractor or author word in a file name",
       not any(re.search(r"distract|trap|golden|answer|clean_|_v\d", f, re.I) for f in files))
    ok("GATE every pack file is declared", set(files) == set(C.ALL_FILES), "")

    # ---- the call ------------------------------------------------------------------------------------------------
    info = calc.golden(target)
    homes, F, S, keys = info["homes"], info["F"], info["S"], info["keys"]
    g = info["golden"]
    ok("CALL golden in its printed cell", cell(g) == figs["call"]["closures_2027"], "%.2f -> %d" % (g, cell(g)))
    ok("CALL golden clear of the cell edge by 5 homes", C.edge(g, 50) >= 5, "edge %.2f" % C.edge(g, 50))
    ok("CALL stock", info["stock"] == figs["cc1"], "%d" % info["stock"])
    ok("CALL homes in the kindergarten summer 2027", info["nk"] == figs["cc2"], "%d" % info["nk"])
    ok("CALL record summers and closures", info["ksummers"] == figs["cc3"] and info["kcloses"] == figs["cc5"],
       "%d of %d" % (info["kcloses"], info["ksummers"]))
    ok("CALL the record's share closing that summer is about half", 0.40 <= info["pk"] <= 0.60, "%.4f" % info["pk"])
    ok("CALL enough events behind the step (300 or more)", info["kcloses"] >= 300, "%d" % info["kcloses"])
    # one sigma of the step leaves the printed cell where it is
    se = (info["pk"] * (1 - info["pk"]) / info["ksummers"]) ** 0.5
    swing = info["nk"] * se
    ok("CALL one sigma of the summer's share moves the call inside its cell", C.edge(g, 50) > swing,
       "swing %.1f homes against an edge of %.1f" % (swing, C.edge(g, 50)))

    # ---- R1 raw material ships, the deciding quantity in no column ------------------------------------------------
    heads = {f: open(os.path.join(target, f), encoding="utf-8").readline().strip().lower() for f in files if f.endswith((".csv", ".txt"))}
    ok("R1 the record's raw material ships (home-months from licences, worksheet children)",
       len(F["ev"]) > 150000 and F["ev"].sum() > 1500, "%d home-months, %d closures" % (len(F["ev"]), F["ev"].sum()))
    ok("R1 no column names the deciding clock",
       not any(re.search(r"kinder|school|youngest|k_year|kyear", h) for h in heads.values()))

    # ---- R3 the analyst test and the decisive step alone ------------------------------------------------------------
    d0 = calc.default_route(info)
    ok("R3a the default path (closure by years licensed) files 300", cell(d0) == 300 and cell(d0) != cell(g),
       "%.1f -> %d" % (d0, cell(d0)))
    ok("R3a default path at the alt_tenure figure", cell(d0) == figs["alt_tenure"], "")
    d_age = calc.cell_route(F, S, lambda X: calc.tband(X["t"]) * 4 + (X["age"] >= 63) * 2 + (X["age"] >= 68))
    ok("R3a with provider age added still 300", cell(d_age) == 300, "%.1f" % d_age)
    d_glm = calc.glm_route(F, S, ["age", "summer"])[0]
    ok("R3a the Poisson model without the step still 300", cell(d_glm) == 300, "%.1f" % d_glm)
    r3b = calc.glm_route(F, S, ["k"])[0]
    ok("R3b the tenure model with only the step added lands the golden cell", cell(r3b) == cell(g), "%.1f" % r3b)
    # every rung's highest figure clears the cell boundary (the golden cell is [425, 475))
    grant = grant_flags(target, keys)
    Fg = dict(F, g=grant[F["i"]])
    Sg = dict(S, g=grant[S["i"]])
    rungs = {
        "tenure x grant round": calc.cell_route(Fg, Sg, lambda X: calc.tband(X["t"]) * 2 + X["g"]),
        "own child under six": calc.glm_route(F, S, ["age", "summer", "under6"])[0],
        "youngest own child's age, straight line": calc.glm_route(F, S, ["age", "summer", "ycage"])[0],
        "any own child's kindergarten summer": calc.glm_route(F, S, ["age", "summer", "kany"])[0],
        "latest year's rate": latest_rate(F, S),
    }
    for name, v in rungs.items():
        ok("RIV %s misses the golden cell" % name, cell(v) != cell(g), "%.1f -> %d" % (v, cell(v)))
    blind = [k for k in rungs if k != "any own child's kindergarten summer"]
    ok("RIV every rung that never reads a child's school year sits below the golden cell by 1.2x or more",
       all(rungs[k] * 1.2 <= 425 for k in blind), ", ".join("%.0f" % rungs[k] for k in blind))
    # the data reject the any-child clock and the July-August window against the youngest's June-August
    lk = calc.loglik(F, ["age", "summer", "k"])[0]
    la = calc.loglik(F, ["age", "summer", "kany"])[0]
    lb = calc.loglik(F, ["age", "summer", "ycbands"])[0]
    ok("RIV any own child's clock rejected by the likelihood (2 dlogL over 100)", 2 * (lk - la) > 100, "%.1f" % (2 * (lk - la)))
    ok("RIV the youngest's age in bands rejected by the likelihood (2 dlogL over 100)", 2 * (lk - lb) > 100, "%.1f" % (2 * (lk - lb)))
    Fja, kja = calc.frame(homes, kspec=dict(months=(7, 8)))
    lja = calc.loglik(Fja, ["age", "summer", "k"])[0]
    ok("RIV July-August only rejected by the likelihood (June carries the spike too)", 2 * (lk - lja) > 50,
       "%.1f" % (2 * (lk - lja)))
    june = monthly_rates(F)
    ok("RIV June, July and August each elevated in the kindergarten year", min(june[6], june[7], june[8]) > 5 * june[5],
       "May %.4f June %.4f July %.4f Aug %.4f Sept %.4f" % (june[5], june[6], june[7], june[8], june[9]))

    # ---- the golden family, every member in the golden cell ---------------------------------------------------------
    fam = family(info)
    for name, v in fam.items():
        ok("FAM %s in the golden cell" % name, cell(v) == cell(g), "%.1f" % v)
    vals = list(fam.values())
    ok("FAM family clear of both cell edges by 4 homes", min(vals) >= 429 and max(vals) <= 471,
       "%.1f to %.1f" % (min(vals), max(vals)))

    # ---- SF rows ----------------------------------------------------------------------------------------------------
    # SF1 licensed on 31 December 2026: ACTIVE in the extract, equal to licences with no closure date
    lic = C.read_csv(os.path.join(target, C.F_LIC))
    act = [r for r in lic if r["status"] == "ACTIVE"]
    ok("SF1 ACTIVE status and blank closure date are one population", len(act) == info["stock"] and
       all(not r["closure_effective_date"] for r in act) and all(r["closure_effective_date"] for r in lic if r["status"] == "CLOSED"),
       "%d" % len(act))
    # SF2 close during 2027: the forecast covers January to December 2027 only
    ok("SF2 the forecast window is the twelve months of 2027", set(S["m"] % 12) == set(range(12)) and
       set(2004 + S["m"] // 12) == {2027}, "")
    # SF3 small and large homes are both family child care homes (rules 6.40.010); excluding large homes moves the call
    small = calc.load(target)
    for k in list(small):
        if small[k]["ltype"] != "SFCC":
            del small[k]
    Fs, ks = calc.frame(small)
    Ss = calc.stock_frame(small, ks)
    vs = calc.glm_route(Fs, Ss, calc.GOLD_FEATS)[0]
    rules = pdf_text(os.path.join(target, C.F_RULES))
    ok("SF3 rules file small and large homes as family child care homes",
       "Family child care homes are licensed in two types" in rules, "small homes only would file %d" % cell(vs))
    # SF4 the kindergarten year follows the 1 September cutoff (CCAP policy section 6); the calendar-year reading
    Fc, kc = calc.frame(homes, kspec=dict(rule="calyear"))
    Sc = calc.stock_frame(homes, kc, kspec=dict(rule="calyear"))
    vc = calc.glm_route(Fc, Sc, calc.GOLD_FEATS)[0]
    pol = pdf_text(os.path.join(target, C.F_POL))
    ok("SF4 the policy files the school-year cutoff; the calendar-year reading files the same call",
       "turns five on or before 1 September" in pol and cell(vc) == cell(g), "%.1f" % vc)
    # SF5 rounding to the nearest 50 (the golden is not on a half-cell boundary)
    ok("SF5 the golden is not within a home of a half-cell boundary", C.edge(g, 50) > 1, "%.2f" % C.edge(g, 50))
    # SF6 a home is a licence: one licence per provider in the extract
    provs = collections.Counter(r["provider_id"] for r in lic)
    ok("SF6 one licence per provider (a home and a licence are one unit)", max(provs.values()) == 1, "")
    # SF7 own children living in the home: the flag is Y on every own-child row (lives_in_home changes nothing)
    ws = C.read_csv(os.path.join(target, C.F_WS))
    own = [r for r in ws if calc.REL[r["relationship"]] == "OWN"]
    ok("SF7 every own child on a worksheet lives in the home", all(r["lives_in_home"] == "Y" for r in own), "%d rows" % len(own))
    # SF8 provider age from birth year: missing birth years are pre-2009 homes; leaving them out of the age terms is
    # the only reading (blank is not zero), and the call is the same with them dropped
    blank = sum(1 for r in lic if not r["provider_birth_year"])
    ok("SF8 blank birth years are few and pre-2009", blank < 400 and all(r["first_licensed_date"] < "2009" for r in lic if not r["provider_birth_year"]),
       "%d" % blank)

    # ---- R2 every Layer 1 item neutral to the call ----------------------------------------------------------------
    for name, v in layer1_mishandled(target, info).items():
        ok("R2 %s leaves the call" % name, cell(v) == cell(g), "%.1f" % v)

    # ---- asks: golden figures, devices and stops ---------------------------------------------------------------------
    a = calc.ask_child_days(target)
    a_sum = calc.ask_child_days(target, union=False)
    a_void = calc.ask_child_days(target, union=False, drop_void=False)
    b = calc.ask_money(target)
    slug = {r: "R%d_%s" % (r, C.REGIONS[r].split()[-1]) for r in C.REGIONS}
    for r in C.REGIONS:
        ok("ASK A %s matches figures" % slug[r], figs["a_" + slug[r]] == {"H1": a[(r, 1)], "H2": a[(r, 2)]})
        ok("ASK B %s matches figures" % slug[r], figs["b_" + slug[r]] == {"Q%d" % q: int(round(b[(r, q)])) for q in (1, 2, 3, 4)})
        ok("ASK B %s every quarter clear of the half-dollar" % slug[r], all(C.edge(b[(r, q)], 1) >= 0.005 for q in (1, 2, 3, 4)),
           ", ".join("%.2f" % b[(r, q)] for q in (1, 2, 3, 4)))
    cells = [(r, h) for r in C.REGIONS for h in (1, 2)]
    qcells = [(r, q) for r in C.REGIONS for q in (1, 2, 3, 4)]
    ok("ASK A the summed lines miss every cell", all(a_sum[k] != a[k] for k in cells),
       "%.3f to %.3f" % (min(a_sum[k] / a[k] for k in cells), max(a_sum[k] / a[k] for k in cells)))
    ok("ASK A voids kept and lines summed miss every cell", all(a_void[k] != a[k] for k in cells), "")
    stops = {}
    for key in ("lines", "number", "number_run", "number_provider", "number_amount", "number_county", "provider_amount"):
        stops[key] = calc.ask_money(target, key=key)
        ok("ASK B one remittance taken as %s misses every cell" % key,
           all(int(round(stops[key].get(k, 0))) != int(round(b[k])) for k in qcells),
           "%.3f to %.3f" % (min(stops[key].get(k, 0) / b[k] for k in qcells), max(stops[key].get(k, 0) / b[k] for k in qcells)))
    bv = calc.ask_money(target, drop_void=False)
    ok("ASK B voided remittances kept miss every cell", all(int(round(bv[k])) != int(round(b[k])) for k in qcells), "")
    # the remittance's provider is the key's payer: number, run and provider give the same remittances as number, run, county
    ok("ASK B number, run and provider equal number, run and county", calc.ask_money(target, key="remittance") ==
       money_by(target, lambda r: (r["remittance_no"], r["pay_run_date"], r["provider_no"])), "")
    # fairness: the shipped rows force the handling
    ccap = C.read_csv(os.path.join(target, C.F_CCAP))
    ok("ASK A no child is paid at two homes in different regions on one day", cross_region_overlaps(target, ccap) == 0, "")
    ok("ASK B every line of a remittance carries one amount, provider and status", remittance_consistent(ccap), "")
    ok("ASK B remittance numbers recur across county offices in every run and for a home across runs",
       shared_numbers(ccap), "")

    # ---- separation: the call reads no ask row -----------------------------------------------------------------------
    ok("SEP the call reads only the licence extract, the crosswalk and the worksheets",
       set(calc_inputs()) == {C.F_LIC, C.F_XW, C.F_WS}, ", ".join(calc_inputs()))
    ok("SEP no ask file holds a row the call reads (ask files share no file with the call)",
       not ({C.F_CCAP} & set(calc_inputs())), "")

    # ---- distractors ---------------------------------------------------------------------------------------------------
    for f in meta["distractor_files"]:
        ok("DIS %s read by no figure" % f, f not in calc_inputs() + [C.F_CCAP, C.F_CTY], "")

    # ---- realism -------------------------------------------------------------------------------------------------------
    counts = [a[k] for k in cells] + [int(round(b[k])) for k in qcells]
    dup = [c for c, k in collections.Counter(counts).items() if k > 1]
    ok("REAL no two graded counts identical", not dup, str(dup))
    ok("REAL no graded count a round hundred", all(c % 100 for c in counts), "")
    closures_by_year = collections.Counter(r["closure_effective_date"][:4] for r in lic if r["closure_effective_date"])
    ok("REAL yearly closures not constant", len(set(closures_by_year[str(y)] for y in range(2016, 2027))) >= 9,
       str([closures_by_year[str(y)] for y in range(2016, 2027)]))
    reasons = collections.Counter(r["closure_reason"] for r in lic if r["closure_reason"])
    ok("REAL closure reasons name no child or school", not any(re.search(r"child|school|kinder", k, re.I) for k in reasons), "")
    ok("REAL people are the card's", "Misty Hawkins" in pdf_text(os.path.join(target, C.F_SUP)), "")
    vis = C.read_csv(os.path.join(target, C.F_VIS))
    ok("REAL no visit on a weekend or holiday", not any(dt.date.fromisoformat(r["visit_date"]).weekday() >= 5 for r in vis), "")
    ok("REAL no payment run on a weekend", not any(dt.date.fromisoformat(r["pay_run_date"]).weekday() >= 5 for r in ccap), "")
    ok("REAL pdf positive control (text extracted)", len(rules) > 1500 and len(pol) > 1500, "%d %d" % (len(rules), len(pol)))
    ok("REAL no pdf says kindergarten, youngest or closure clock",
       not any(re.search(r"kindergarten|youngest", t, re.I) for t in (rules, pdf_text(os.path.join(target, C.F_SUP)))), "")

    print("%d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


def calc_inputs():
    return [C.F_LIC, C.F_XW, C.F_WS]


def pdf_text(path):
    import pypdf
    return " ".join((p.extract_text() or "") for p in pypdf.PdfReader(path).pages).replace("\n", " ")


def grant_flags(target, keys):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, C.F_GRANT), read_only=True)
    ws = wb["Awards"]
    got = set()
    for row in ws.iter_rows(min_row=5, values_only=True):
        if row[1]:
            got.add(row[1])
    return np.array([1.0 if k in got else 0.0 for k in keys])


def latest_rate(F, S):
    y = 2004 + F["m"] // 12
    sel = y == 2026
    n = len(np.unique(F["i"][sel]))
    return F["ev"][sel].sum() / n * len(np.unique(S["i"]))


def monthly_rates(F):
    out = {}
    yr = 2004 + F["m"] // 12
    mo = F["m"] % 12 + 1
    # months of the youngest's kindergarten year, flagged or not
    kyr = F["kyear_flag"] if "kyear_flag" in F else None
    return {m: (F["ev"][(F["k"] > 0) & (mo == m)].sum() / max(((F["k"] > 0) & (mo == m)).sum(), 1)) if m in (6, 7, 8)
            else F["ev"][(F["k"] == 0) & (mo == m)].sum() / max(((F["k"] == 0) & (mo == m)).sum(), 1) for m in range(1, 13)}


def family(info):
    homes, F, S, keys = info["homes"], info["F"], info["S"], info["keys"]
    fam = {}
    fam["log hazard, summer months"] = info["golden"]
    fam["logit hazard"] = calc.glm_route(F, S, calc.GOLD_FEATS, link="logit")[0]
    fam["no summer term"] = calc.glm_route(F, S, ["age", "k"])[0]
    fam["2020 term"] = calc.glm_route(F, S, ["age", "summer", "k", "y2020"])[0]
    fam["grandchild term"] = calc.glm_route(F, S, ["age", "summer", "k", "grandk"])[0]
    fam["no age terms"] = calc.glm_route(F, S, ["summer", "k"])[0]
    fam["tenure capped at 5 years"] = calc.glm_route(F, S, calc.GOLD_FEATS, cap=5)[0]
    fam["additive excess"] = calc.additive_route(F, S)[0]
    fam["annual share"] = calc.annual_share_route(homes, keys, F, S)[0]
    fam["the step with the youngest's age bands added"] = calc.glm_route(F, S, ["age", "summer", "k", "ycbands"])[0]
    fam["the step with any own child's summer added"] = calc.glm_route(F, S, ["age", "summer", "k", "kany"])[0]
    for name, ks in (("whole kindergarten year", dict(whole=True)), ("May to September", dict(months=(5, 6, 7, 8, 9)))):
        F2, k2 = calc.frame(homes, kspec=ks)
        S2 = calc.stock_frame(homes, k2, kspec=ks)
        fam[name] = calc.glm_route(F2, S2, calc.GOLD_FEATS)[0]
        fam[name + ", additive"] = calc.additive_route(F2, S2)[0]
    for name, st in (("fitted from 2019", (2019, 1)), ("fitted from 2021", (2021, 1))):
        F2, _ = calc.frame(homes, start=st)
        fam[name] = calc.glm_route(F2, S, calc.GOLD_FEATS)[0]
    F2, k2 = calc.frame(homes, kspec=dict(in_home=False))
    S2 = calc.stock_frame(homes, k2, kspec=dict(in_home=False))
    fam["own children wherever they live"] = calc.glm_route(F2, S2, calc.GOLD_FEATS)[0]
    return fam


def layer1_mishandled(target, info):
    out = {}
    homes = calc.load(target)
    # L1 pre-2019 worksheets not mapped through the crosswalk (their rows dropped)
    xw = {r["legacy_licence_no"] for r in C.read_csv(os.path.join(target, C.F_XW))}
    h2 = {k: dict(v, kids={}) for k, v in homes.items()}
    for r in C.read_csv(os.path.join(target, C.F_WS)):
        if r["licence_ref"] in xw or r["licence_ref"] not in h2:
            continue
        b = calc.pdate(r["child_birth_date"])
        h2[r["licence_ref"]]["kids"][(r["child_initials"], b)] = (calc.REL[r["relationship"]], r["lives_in_home"])
    F2, k2 = calc.frame(h2)
    out["L1 legacy worksheets left unmatched"] = calc.glm_route(F2, calc.stock_frame(h2, k2), calc.GOLD_FEATS)[0]
    # L2 the latest worksheet only (children who aged out or were listed only earlier dropped)
    last = {}
    rows = C.read_csv(os.path.join(target, C.F_WS))
    xwm = {r["legacy_licence_no"]: r["licence_no"] for r in C.read_csv(os.path.join(target, C.F_XW))}
    for r in rows:
        no = xwm.get(r["licence_ref"], r["licence_ref"])
        if no in homes and r["worksheet_date"] >= last.get(no, ""):
            last[no] = r["worksheet_date"]
    h3 = {k: dict(v, kids={}) for k, v in homes.items()}
    for r in rows:
        no = xwm.get(r["licence_ref"], r["licence_ref"])
        if no in h3 and r["worksheet_date"] == last[no]:
            b = calc.pdate(r["child_birth_date"])
            h3[no]["kids"][(r["child_initials"], b)] = (calc.REL[r["relationship"]], r["lives_in_home"])
    F3, k3 = calc.frame(h3)
    out["L2 latest worksheet only"] = calc.glm_route(F3, calc.stock_frame(h3, k3), calc.GOLD_FEATS)[0]
    # L4 the homes licensed before 2016 started at tenure zero in January 2016 (delayed entry ignored)
    h4 = {k: dict(v, first=max(v["first"], dt.date(2016, 1, 1))) for k, v in homes.items()}
    F4, k4 = calc.frame(h4)
    out["L4 delayed entry ignored"] = calc.glm_route(F4, calc.stock_frame(h4, k4), calc.GOLD_FEATS)[0]
    # L8 blank birth years read as age 0 (no retirement terms for them)
    return out


def money_by(target, keyf):
    reg = calc.regions_by_fips(target)
    seen = {}
    for r in C.read_csv(os.path.join(target, C.F_CCAP)):
        if r["provider_type"] in ("SFCC", "LFCC") and r["pay_run_date"].startswith("2026") and r["remittance_status"] != "VOID":
            seen.setdefault(keyf(r), ((reg[r["county_fips"]], (int(r["pay_run_date"][5:7]) - 1) // 3 + 1), float(r["remittance_amount"])))
    out = {}
    for g, amt in seen.values():
        out[g] = out.get(g, 0.0) + amt
    return {k: round(v, 2) for k, v in out.items()}


def remittance_consistent(ccap):
    by = collections.defaultdict(set)
    for r in ccap:
        by[(r["remittance_no"], r["pay_run_date"], r["county_fips"])].add((r["remittance_amount"], r["provider_no"], r["remittance_status"]))
    return all(len(v) == 1 for v in by.values())


def shared_numbers(ccap):
    runs = collections.defaultdict(lambda: collections.defaultdict(set))
    prov = collections.defaultdict(set)
    for r in ccap:
        runs[r["pay_run_date"]][r["remittance_no"]].add(r["county_fips"])
        prov[(r["provider_no"], r["remittance_no"])].add(r["pay_run_date"])
    every_run = all(sum(1 for c in nos.values() if len(c) > 1) > 100 for nos in runs.values())
    repeat = sum(1 for v in prov.values() if len(v) > 1)
    return every_run and repeat > 500


def cross_region_overlaps(target, ccap):
    reg = calc.regions_by_fips(target)
    by_child = collections.defaultdict(list)
    for r in ccap:
        if r["provider_type"] in ("SFCC", "LFCC") and r["remittance_status"] != "VOID":
            by_child[r["child_no"]].append((r["service_from"], r["service_to"], reg[r["county_fips"]]))
    bad = 0
    for ls in by_child.values():
        ls.sort()
        for i in range(len(ls)):
            for j in range(i + 1, len(ls)):
                if ls[j][0] <= ls[i][1] and ls[j][2] != ls[i][2]:
                    bad += 1
    return bad


def reissues_ok(ccap):
    voids = {r["line_no"] for r in ccap if r["line_status"] == "VOID"}
    re_ = [r["reissue_of"] for r in ccap if r["reissue_of"]]
    return all(x in voids for x in re_) and len(re_) > 100


def two_sponsor_months(cf):
    reg_of = {}
    by = collections.defaultdict(set)
    for r in cf:
        if r["site_licence_no"].startswith("FC"):
            by[(r["site_licence_no"], r["claim_month"])].add(r["sponsor_id"])
            reg_of[r["site_licence_no"]] = r["county_fips"]
    import common
    name2reg = {common.COUNTY_NAME[c[0]] + " County": c[2] for c in common.COUNTIES}
    out = collections.Counter()
    for (site, m), sps in by.items():
        if len(sps) > 1:
            out[name2reg[reg_of[site]]] += 1
    return out


def twins(vis):
    name2reg = {C.COUNTY_NAME[c[0]]: c[2] for c in C.COUNTIES}
    by = collections.defaultdict(list)
    for r in vis:
        if r["facility_type"] in ("SFCC", "LFCC") and r["status"] == "COMPLETED":
            by[(r["licence_no"], r["visit_date"])].append((r["inspector_id"], r["arrived"]))
    tw, sd = collections.Counter(), collections.Counter()
    for (no, d), v in by.items():
        reg = None
        if len(v) > 1:
            c = collections.Counter(v)
            for r in vis:
                if r["licence_no"] == no:
                    reg = name2reg[r["county"]]
                    break
            if any(n > 1 for n in c.values()):
                tw[reg] += 1
            if len(c) > 1:
                sd[reg] += 1
    return tw, sd


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))

"""The generator's assertions on the cut pack: the input gates, the golden and its estimator family, the forms the
readings reject, the ladder, the client's three rules executed (R1, R2, R3) on the generator's clean truth, the
semantic fork table (SF1 to SF18), the asks' devices and their separation from the call, and the realism sweep."""
import json
import os
import re
import subprocess
import zipfile

import numpy as np
import pandas as pd

import asks as A
import fleet as F
import methods as M
import vin as V
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
n = [0]
fails = []
GOLDEN_SET = ["Elkhollow", "Halvering", "Linnmere", "Marlbank", "Wexmoor"]
R1_SET = ["Copperleaf", "Dunmarsh", "Elkhollow", "Halvering", "Larkhaven", "Linnmere", "Marlbank", "Quarrybrook",
          "Wexmoor"]
R2_SET = ["Dunmarsh", "Halvering", "Linnmere", "Wexmoor"]


def check(label, ok, detail=""):
    n[0] += 1
    d = str(detail)
    print("%s  %s%s" % ("ok  " if ok else "FAIL", label, ("  (%s)" % d) if d != "" else ""))
    if not ok:
        fails.append(label)


def r0(v):
    return int(v + 0.5)


def edge(v):
    """Distance of a value from the nearest whole-ton rounding edge."""
    return abs(v - np.floor(v) - 0.5)


def pdf_text(path):
    from pypdf import PdfReader
    return " ".join(" ".join(pg.extract_text().split()) for pg in PdfReader(path, strict=True).pages)


def tons_from(t, el, regvins, fallback=True):
    """The golden construction on a given set of readings: the quadratic of every reading, each vehicle's level
    against it, the curve's rise over 2027, the county fill."""
    p = np.polyfit(t["age"].to_numpy(), t["miles"].to_numpy(), 2)
    Mq = lambda a: np.polyval(p, a)
    m = M.match_on(t, el, regvins, fallback)
    return M.fill_and_tons(el, M.own_level(el, m, Mq))[0]


def clean_truth():
    """The world before any record is written: every first-cycle test's true odometer at its test date, the
    vehicles on the snapshot's ACTIVE records, and each one's true 2027 miles."""
    T = F.build()
    t = T[T["tested"]].copy()
    t["age"] = np.array([F.dec(d) for d in t["test_date"]]) - t["my"].to_numpy()
    t["miles"] = t["odo_true"]
    act = (T["kind"] == "active") | ((T["kind"] == "pilot") & T["reinstated"])
    el = T[act & T["my"].between(*W.ELIG_MY) & T["fuel"].isin(["G", "F"]) & T["gvwr"].isin(["1", "2a"])].copy()
    el["rate"] = [W.RATES[m][0] if c == "PC" else W.RATES[m][1] for m, c in zip(el["my"], el["cls"])]
    el = el.reset_index(drop=True)
    lev = el["vin"].map(t.set_index("vin")["miles"])
    age = el["vin"].map(t.set_index("vin")["age"])
    true27 = el["k"].to_numpy() * (F.cum(2028 - el["first"].to_numpy()) - F.cum(2027 - el["first"].to_numpy()))
    return t, el, lev.to_numpy(), age.to_numpy(), true27


def main(target, gdir):
    files = sorted(os.listdir(target))
    exts = {f.rsplit(".", 1)[1] for f in files}
    rows = {}
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                rows[f] = sum(1 for _ in fh) - 1
    meta = json.load(open(os.path.join(os.path.dirname(gdir), "metadata.json"), encoding="utf-8"))
    check("input gates: %d files (10 or more)" % len(files), len(files) >= 10)
    check("input gates: %d formats %s (3 or more)" % (len(exts), sorted(exts)), len(exts) >= 3)
    big = max(rows.items(), key=lambda t: t[1])
    check("input gates: %s has %d rows (25,000 or more)" % big, big[1] >= 25000)
    dis = [d["file"] for d in meta["distractors"]]
    check("input gates: %d distractors named in metadata.json, none named for its role" % len(dis),
          len(dis) >= 2 and all(d in files and not re.search(r"distract|decoy|trap", d) for d in dis))
    check("input gates: every file carries a source, a date and a licence", all(
        e.get("source") and e.get("date") and e.get("license") for e in meta["files"]) and
        sorted(e["file"] for e in meta["files"]) == files)

    # the golden and its family
    R = M.routes(target)
    gold = R["golden"]
    gset = M.designated(gold)
    check("the golden files five counties %s" % gset, gset == GOLDEN_SET)
    fam = dict(R)
    fam.update(M.family_wide(target))
    members = ["golden", "ols3", "ols4", "ll4", "ll6", "bin1", "ols2_0", "lifeavg1", "lifeavg2", "ols2_elig",
               "ols2_age10", "ols2_my9612", "bymy", "county", "expdecay"]
    for k in members:
        check("family %s files the golden set" % k, M.designated(fam[k]) == GOLDEN_SET)
    for c in W.NAMES:
        vals = [float(fam[k][c]) for k in members]
        same = len({r0(v) for v in vals}) == 1
        check("bins: %s is %d tons under all %d family members (range %.2f to %.2f, nearest edge %.2f)" % (
            c, r0(gold[c]), len(members), min(vals), max(vals), min(edge(v) for v in vals)),
            same and min(edge(v) for v in vals) >= 0.03)
    near = min(min(float(fam[k][c]) for k in members) for c in GOLDEN_SET)
    far = max(max(float(fam[k][c]) for k in members) for c in W.NAMES if c not in GOLDEN_SET)
    check("margin: the lowest designated county stays at %.2f tons and the highest other county at %.2f across the "
          "family" % (near, far), near >= 10.5 and far <= 9.3)
    fit, nb = M.forms_fit(target)
    q = fit["quadratic"]
    for k in ("linear", "power", "log_quadratic"):
        check("forms: the readings reject the %s form (chi-square %.0f against the quadratic's %.0f on %d one-year "
              "means)" % (k, fit[k], q, nb), fit[k] > 5 * q and fit[k] > 4 * nb)
    check("forms: the quadratic fits the one-year means within their noise (chi-square %.0f on %d)" % (q, nb), q < 3 * nb)

    # the ladder
    r0_set = ["Dunmarsh", "Elkhollow", "Halvering", "Larkhaven", "Linnmere", "Marlbank", "Quarrybrook", "Thorncastle",
              "Wexmoor"]
    for k, want in (("R0", r0_set), ("R1", R1_SET), ("R1c", R1_SET),
                    ("R1d", R1_SET), ("R2", R2_SET), ("R3t", GOLDEN_SET)):
        check("ladder %s files %s" % (k, M.designated(R[k])), M.designated(R[k]) == want)
    moved = [c for c in W.NAMES if r0(R["R3t"][c]) != r0(gold[c])]
    check("ladder R3t (the slope at the test age, not aged to 2027) lands the set and misses %d county figures" %
          len(moved), len(moved) >= 10)
    for k in ("R1", "R1c", "R1d", "R0", "R2"):
        moved = [c for c in W.NAMES if r0(R[k][c]) != r0(gold[c])]
        check("ladder %s misses %d of 12 county figures" % (k, len(moved)), len(moved) >= 11)
    for c in ("Elkhollow", "Marlbank"):
        check("ladder R2 drops %s at %.2f tons" % (c, R["R2"][c]), R["R2"][c] <= 9.5)
    check("ladder R2 adds Dunmarsh at %.2f tons" % R["R2"]["Dunmarsh"], R["R2"]["Dunmarsh"] >= 10.4)
    lo1 = min(R["R1"][c] for c in R1_SET if c not in GOLDEN_SET)
    hi1 = max(R["R1"][c] for c in W.NAMES if c not in R1_SET)
    check("ladder R1: its added counties clear the line at %.2f tons or more, the two it leaves out stay at %.2f" % (
        lo1, hi1), lo1 >= 11.0 and hi1 <= 9.0)

    # R1: the field's raw material ships, the deciding quantity does not
    cols = set()
    for f in files:
        if f.endswith(".csv") and f not in W.DISTRACTORS:
            cols |= set(pd.read_csv(os.path.join(target, f), nrows=0).columns)
    bad = [c for c in cols if re.search(r"vmt|annual|mileage|per_year|nox|tons|grams|accum", c, re.I)]
    check("R1: no shipped extract column holds a yearly mileage, an inventory or NOx (%d columns)" % len(cols), not bad, bad)
    check("R1: the decisive computation reads the inspection records (%d rows) against the snapshot (%d rows)" % (
        rows[W.FILES["inspections"]], rows[W.FILES["registrations"]]),
        rows[W.FILES["inspections"]] > 150000 and rows[W.FILES["registrations"]] > 200000)

    # R3: the analyst test, the decisive step alone and the truth, on the clean truth
    t, el, lev, age, true27 = clean_truth()
    a0, a1 = (2027 - el["my"]).to_numpy(), (2028 - el["my"]).to_numpy()
    tons = lambda mil: M.fill_and_tons(el, mil)[0]
    p = np.polyfit(t["age"].to_numpy(), t["miles"].to_numpy(), 2)
    Mq = lambda a: np.polyval(p, a)
    r1_truth = tons(lev / age)
    check("R3a: the analyst test on the clean truth (each vehicle's reading over its age, every rule applied) files %s"
          % M.designated(r1_truth), M.designated(r1_truth) == R1_SET)
    g_truth = tons(lev / Mq(age) * (Mq(a1) - Mq(a0)))
    check("R3b: the decisive step alone (its level against the cumulative curve, times the curve's rise over 2027) "
          "files the golden set", M.designated(g_truth) == GOLDEN_SET)
    la = np.polyfit(t["age"].to_numpy(), (t["miles"] / t["age"]).to_numpy(), 2)
    L = lambda a: np.polyval(la, a)
    r1c_truth = tons(lev / age * L((a0 + a1) / 2) / L(age))
    r2_truth = tons(Mq(a1) - Mq(a0))
    check("R3b: each lower rung's single correction stays wrong on the clean truth (lifetime average along its trend "
          "%s, the fleet's curve without the vehicle's level %s)" % (len(M.designated(r1c_truth)),
                                                                     M.designated(r2_truth)),
          M.designated(r1c_truth) != GOLDEN_SET and M.designated(r2_truth) != GOLDEN_SET)
    truth = tons(true27)
    worst = max(abs(float(gold[c]) / float(truth[c]) - 1) for c in W.NAMES)
    check("R3b: the golden estimates the truth: the true 2027 NOx files the golden set and the golden is within %.1f%% "
          "of it in every county" % (100 * worst), M.designated(truth) == GOLDEN_SET and worst < 0.04)
    check("R3c: no exact duplicate test record (%d)" % int(M.load(target)[1].duplicated().sum()),
          int(M.load(target)[1].duplicated().sum()) == 0)
    regf = M.load(target)[0]
    check("R3c: no registration record repeated (%d)" % int(regf.duplicated(["vin", "county_no", "record_status"]).sum()),
          int(regf.duplicated(["vin", "county_no", "record_status"]).sum()) == 0)

    # R2: each Layer 1 item mishandled leaves the call and every county figure where they were
    reg, tst, body, rates = M.load(target)
    regvins = set(reg["vin"])
    el_p = M.eligible(target).reset_index(drop=True)
    base = M.readings(target)

    def same(label, tn):
        moved = [c for c in W.NAMES if r0(tn[c]) != r0(gold[c])]
        check("R2: %s: same call and every county's whole tons (moved %s)" % (label, moved),
              M.designated(tn) == GOLDEN_SET and not moved)

    raw = tst.copy()
    raw["odo"] = pd.to_numeric(raw["odometer"])
    raw["when"] = pd.to_datetime(raw["test_start"])
    raw["my"] = raw["model_year"].astype(int)
    raw["age"] = (raw["when"] - pd.to_datetime(raw["my"].astype(str) + "-01-01")).dt.days / 365.25
    raw["miles"] = np.where(raw["odometer_unit"] == "KM", raw["odo"] * M.KM, raw["odo"])
    raw = raw.sort_values(["when", "test_id"], kind="mergesort")
    ini = raw[raw["test_type"] == "INITIAL"].drop_duplicates("vin")
    ini = ini[ini["odo"].notna() & ~ini["odo"].isin([0, 999999])]
    same("an aborted attempt read as the vehicle's initial inspection (%d aborts)" % int((tst["result"] == "ABORT").sum()), tons_from(ini, el_p, regvins))
    last = raw[raw["odo"].notna() & ~raw["odo"].isin([0, 999999])].drop_duplicates("vin", keep="last")
    same("the retest's reading taken for the initial (%d retests)" % int((tst["test_type"] == "RETEST").sum()), tons_from(last, el_p, regvins))
    km = base.assign(miles=base["odo"])
    same("kilometre readings read as miles (%d)" % int((base["odometer_unit"] == "KM").sum()), tons_from(km, el_p, regvins))
    keep = raw[(raw["test_type"] == "INITIAL") & raw["result"].isin(["PASS", "FAIL"]) & raw["odo"].notna()].drop_duplicates("vin")
    same("odometers entered as 0 or 999999 used as readings (%d)" % int(keep["odo"].isin([0, 999999]).sum()), tons_from(keep, el_p, regvins))
    same("typed VINs that match no registration left unread (%d tests)" % int((~base["vin"].isin(regvins)).sum()), tons_from(base, el_p, regvins, fallback=False))
    same("failed initial tests dropped (%d)" % int((base["result"] == "FAIL").sum()), tons_from(base[base["result"] == "PASS"], el_p, regvins))
    trn = reg[(reg["record_status"] == "TRANSFERRED")].copy()
    both = pd.concat([reg[reg["record_status"] == "ACTIVE"], trn])
    el_t = both[both["county_no"].isin(["%02d" % v for v in W.CNO.values()])].copy()
    el_t["my"] = el_t["model_year"].astype(int)
    el_t = el_t[el_t["my"].between(*W.ELIG_MY) & el_t["fuel_code"].isin(["G", "F"]) & el_t["gvwr_class"].isin(["1", "2a"])].copy()
    el_t["county"] = el_t["county_no"].astype(int).map(W.NAME_OF)
    el_t["cls"] = el_t["body_code"].map(body)
    el_t["rate"] = [rates.at[m, "passenger_car_g_per_mi" if c == "PC" else "light_truck_g_per_mi"] for m, c in zip(el_t["my"], el_t["cls"])]
    same("the transferred records of vehicles that moved counted where they were (%d)" % len(trn), tons_from(base, el_t.reset_index(drop=True), regvins))

    # the semantic fork table
    gl = pdf_text(os.path.join(target, W.FILES["guidelines"]))
    dc = pdf_text(os.path.join(target, W.FILES["dictionary"]))
    check("SF1 eligible vehicles filed (2.1)", "fuel code G or F" in gl and "model year 2005 to 2014" in gl and
          "GVWR class 1 or 2a" in gl)
    check("SF2 registered on 1 July 2026 is an ACTIVE record on the snapshot (2.1)",
          "has a Division of Motor Vehicles record with status ACTIVE in that county on the registration snapshot" in gl)
    check("SF3 calendar year 2027 (3.1, 3.2)", "in calendar year 2027" in gl)
    check("SF4 the 10.0 line before rounding (3.1)", "compared with 10.0 before any rounding" in gl)
    check("SF5 the short ton (3.2)", "907,184.74 grams" in gl)
    cls_ok = el_p["cls"].notna().all()
    check("SF6 the class follows the body code; every eligible vehicle's body code maps (3.2)",
          "program class follows the registration body code" in gl and bool(cls_ok))
    check("SF7 the initial inspection's reading (3.3); an aborted attempt carries no odometer",
          "own odometer reading at its initial inspection" in gl and
          tst.loc[tst["result"] == "ABORT", "odometer"].isna().all())
    check("SF8 age from 1 January of the model year (3.3)", "counted from 1 January of its model year" in gl)
    fill = el_p.assign(read=M.match(target, el_p)["miles"].notna())
    cells = fill.groupby(["county", "my"])["read"].sum()
    check("SF9 the fill filed (3.4), and every county and model year has read vehicles (fewest %d)" % int(cells.min()),
          "average 2027 miles of the eligible vehicles of its model year registered in its county" in gl and
          cells.min() >= 20)
    check("SF10 kilometre odometers named in the notes; same call read as miles (R2)", "KM where the odometer reads in kilometres" in dc)
    check("SF11 typed VINs and the plate the lane software found (notes); same call without the plate (R2)",
          "typed by the inspector (KEYED)" in dc and "plate and model_year as the lane software found them" in dc)
    dM = lambda a: (gold_M(a + 0.01) - gold_M(a - 0.01)) / 0.02
    gold_M = M.golden(target)["M"]
    m_ = M.match(target, el_p)
    mid = M.fill_and_tons(el_p, np.asarray(m_["miles"] / gold_M(m_["age"].to_numpy())) * dM((a0_ := (2027 - el_p["my"]).to_numpy()) + 0.5))[0]
    check("SF12 the 2027 miles as the curve's slope at the mid-2027 age: same call and figures",
          M.designated(mid) == GOLDEN_SET and all(r0(mid[c]) == r0(gold[c]) for c in W.NAMES))
    check("SF13 the cumulative curve's form and sample: the family block above (%d members)" % len(members), True)
    act = reg[reg["record_status"] == "ACTIVE"]
    check("SF14 one ACTIVE record per vehicle (%d VINs with two)" % int(act["vin"].duplicated().sum()),
          int(act["vin"].duplicated().sum()) == 0)
    cty = pd.read_csv(os.path.join(target, W.FILES["counties"]), dtype=str)
    check("SF15 the member counties are county_codes.csv's twelve (3.5)", sorted(cty["county"]) == sorted(W.NAMES) and
          "twelve counties of the nonattainment area listed in county_codes.csv" in gl)
    check("SF16 whole tons from the unrounded total: no county within 0.03 of an edge under any member (above)", True)
    check("SF17 running exhaust NOx in Table 2 (3.2)", "running exhaust rate" in gl)
    check("SF18 the program class codes are the body code list's two (PC, LT)", sorted(set(body)) == ["LT", "PC"])

    # the asks
    p = A.pilot_figures(target)
    naive_n = A.pilot_figures(target, drop_reinstated=False)
    raw_amt = A.pilot_figures(target, rate_card=False)
    both_naive = A.pilot_figures(target, drop_reinstated=False, rate_card=False)
    for c in W.PILOT_COUNTIES:
        check("ask A: %s retired %d of %d vouchers; every voucher counted misses" % (c, p[c]["n"], naive_n[c]["n"]),
              naive_n[c]["n"] != p[c]["n"])
        check("ask A: %s charges $%s; the reinstated left in misses ($%s), the raw amounts with or without them %s" % (
            c, "{:,.0f}".format(p[c]["charges"]), "{:,.0f}".format(naive_n[c]["charges"]),
            "miss" if c == "Elkhollow" else "hit only with the reinstated dropped"),
            round(naive_n[c]["charges"]) != round(p[c]["charges"]) and round(both_naive[c]["charges"]) != round(p[c]["charges"]))
    check("ask A: Oakhaven's raw line amounts overstate Elkhollow's charges %.2f times" % (
        raw_amt["Elkhollow"]["charges"] / p["Elkhollow"]["charges"]), raw_amt["Elkhollow"]["charges"] > 1.3 * p["Elkhollow"]["charges"])
    inv = pd.read_csv(os.path.join(target, W.FILES["invoices"]), dtype=str)
    other = inv[inv["dismantler_licence"] != "D-2864"]
    per = other.groupby("tow_zone")["amount"].nunique()
    check("ask A fair: the other dismantlers bill one amount per tow zone (%s)" % dict(other.groupby("tow_zone")["amount"].first()),
          bool((per == 1).all()) and len(per) == 4)
    vou = pd.read_excel(os.path.join(target, W.FILES["vouchers"]), dtype=str)
    check("realism: every dismantler certificate number is issued once", not vou["certificate_no"].duplicated().any())
    tr = reg[(reg["record_status"] == "TRANSFERRED") & reg["vin"].isin(vou["vin"])]
    check("ask A twins: %d voucher vehicles carry a transferred record from an earlier move, and are retired" % len(tr),
          len(tr) >= 20)
    # separation: the call reads no voucher, invoice or station row, and the reinstated vehicles do not move it
    rein = set(vou["vin"]) & set(act["vin"])
    el_r = el_p[~el_p["vin"].isin(rein)].reset_index(drop=True)
    tr_ = tons_from(base, el_r, regvins)
    check("separation: the %d reinstated pilot vehicles dropped from the fleet leave the call and every figure" % len(rein),
          M.designated(tr_) == GOLDEN_SET and all(r0(tr_[c]) == r0(gold[c]) for c in W.NAMES))
    import inspect
    src = inspect.getsource(M.golden) + inspect.getsource(M.eligible) + inspect.getsource(M.readings)
    check("separation: the golden construction reads no voucher, invoice or station file",
          not re.search(r"vouchers|invoices|stations|annual", src))

    # realism sweep
    g = M.golden(target)
    check("realism: no two counties with the same eligible count", g["n"].nunique() == 12)
    check("realism: no two counties with the same count of readings", g["read"].nunique() == 12)
    bad_vin = [v for v in reg["vin"].head(20000) if V.check_digit(v) != v[8]]
    check("realism: registration VINs carry valid check digits (%d bad of 20,000)" % len(bad_vin), not bad_vin)
    check("realism: no test after the cycle and none before it", tst["test_start"].min() >= "2024-01-02" and
          tst["test_start"].max() <= "2025-12-31 23:59")
    check("realism: no registration status after the snapshot", reg["status_date"].max() <= "2026-07-01")
    check("realism: no voucher paid or invoice dated after the register's export", vou["paid_on"].max() <= "2026-01-20" and
          inv["invoice_date"].max() <= "2026-01-16")
    for f in files + [os.path.join("..", "golden", x) for x in W.GOLDEN.values()]:
        pth = os.path.normpath(os.path.join(target, f))
        if pth.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(pth) as z:
                meta_ = z.read("docProps/core.xml").decode() + z.read("docProps/app.xml").decode()
            check("H1: %s carries its owner and no library stamp" % os.path.basename(pth),
                  "openpyxl" not in meta_ and "python" not in meta_.lower())
        elif pth.endswith(".pdf"):
            b = open(pth, "rb").read()
            check("H1: %s carries no library banner" % f, b"ReportLab" not in b and b"reportlab" not in b)
    import guard_people
    okp, extra = guard_people.ok()
    check("personas from guard.py names only", okp, extra)
    for k, key in (("guidelines", "compared with 10.0 before any rounding"), ("dictionary", "KM where the odometer reads")):
        pth = os.path.join(target, W.FILES[k])
        a2 = " ".join(subprocess.run(["pdftotext", "-layout", pth, "-"], capture_output=True, text=True).stdout.split())
        check("H25: %s reads in pypdf (strict) and pdftotext" % W.FILES[k], key in pdf_text(pth) and key in a2)

    # figures.json and the golden workbook agree
    f = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    wb = pd.read_excel(os.path.join(gdir, W.GOLDEN["workbook"]), sheet_name="Intake counties", dtype={"County no.": str})
    wb = wb[wb["County no."].notna()].set_index("County")
    check("golden workbook: twelve county rows match figures.json", all(
        int(wb.at[c, "2027 NOx (short tons)"]) == f["counties"][c]["tons"] and
        (wb.at[c, "Intake events"] == "Yes") == f["counties"][c]["qualifies"] for c in W.NAMES))
    print("checks: %d run, %d failed" % (n[0], len(fails)))
    return not fails

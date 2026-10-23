"""task482's assertions on the cut pack and the generator's clean truth: the three rules (R1 to R3c), every semantic fork
row (SF1 to SF22), the ladder (R0 to R5), the golden's licensed family and margins (G1 to G5), the asks' devices
(A and B), the separation line (X1 to X4), the input gates and the realism sweep.

    python3 task482/generator/checks.py
"""
import copy
import csv
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import warnings
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import asks as A      # noqa: E402
import bundle as B    # noqa: E402
import pack as P      # noqa: E402
import world as W     # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLD = ["Ashcombe Flexible Packaging", "Carrow Gravure", "Kelvedon Laminates", "Merrion Flexibles",
        "Ravensbrook Gravure Packaging"]
DEFAULT = ["Carrow Gravure", "Merrion Flexibles", "Ravensbrook Gravure Packaging"]
RESULTS = []


def check(name, ok):
    RESULTS.append((name, bool(ok)))
    print("%s  %s" % ("PASS" if ok else "FAIL", name))


def whole(t):
    return {n: B.hround(v["emitted"] if isinstance(v, dict) else v) for n, v in t.items()}


def tenth(t):
    return {n: B.round1(v) for n, v in t.items()}


def gal(t):
    return {n: B.hround(v) for n, v in t.items()}


def moved(a, b):
    return [n for n in a if a[n] != b[n]]


def subset(keys):
    d = tempfile.mkdtemp(prefix="t482_")
    for k in keys:
        shutil.copy(os.path.join(TARGET, P.FILES[k]), os.path.join(d, P.FILES[k]))
    return d


def doc_text(key):
    return re.sub(r"\s+", " ", B.pdf_text(os.path.join(TARGET, P.FILES[key])))


def with_tests(I, fn):
    """A copy of the inputs whose test runs pass through fn(test, run) -> run."""
    J = copy.copy(I)
    J.tests = [dict(t, runs=[fn(t, dict(r)) for r in t["runs"]]) for t in I.tests]
    J.ci = np.array([r["ci"] for t in J.tests for r in t["runs"]])
    J.co = np.array([r["co"] for t in J.tests for r in t["runs"]])
    return J


def clean_truth(e):
    """The analyst test on the generator's clean truth: each plant's VOC used and captured from the world's own press
    days, each oxidizer's tests at the world's relation without run noise, every filed rule applied."""
    out = {"latest": {}, "mean": {}, "golden": {}}
    for p in W.PLANTS:
        rec = e["plants"][p["code"]]
        used = sum(rec["used"].values()) / 2000.0
        if not p["ox"]:
            for k in out:
                out[k][p["name"]] = used
            continue
        ox = p["ox"]
        cap = used * ox["CE"]
        dres = []
        for code, d, note, fac in sorted(W.TESTS, key=lambda x: x[1]):
            if code == p["code"]:
                c = W.full_inlet(p) * fac
                dres.append(1 - max(W.FLOOR, W.PASS * c) / c)
        ctl = 0.0
        for d in rec["days"]:
            h, q = rec["daily"][d]
            c = rec["used"][d] * ox["CE"] / h * ox["cf"] / (q * 60 * W.K)
            ctl += max(W.FLOOR, W.PASS * c) * q * 60 * W.K / ox["cf"] * h
        out["latest"][p["name"]] = used - cap + cap * (1 - dres[-1])
        out["mean"][p["name"]] = used - cap + cap * (1 - np.mean(dres))
        out["golden"][p["name"]] = used - cap + ctl / 2000.0
    return out


def tons_with(I, day_voc=None, flows=None, hours=None, f=None, cf=None, ce=None):
    """The golden handling with one input replaced: day_voc {plant: {day: lb}}, flows {plant: {day: scfm}}, hours
    {plant: {day: h}}, cf or ce {plant: value}."""
    f = f or B.relation(I, "golden")[0]
    out = {}
    for n in I.order:
        dv = (day_voc or {}).get(n, I.day_voc[n])
        used = sum(dv.values()) / B.TONS
        if n not in I.ox:
            out[n] = used
            continue
        ce_ = (ce or {}).get(n, I.ce[n])
        cf_ = (cf or {}).get(n, I.cf[n])
        ctl = 0.0
        for d, lb in dv.items():
            fl = I.proc[n].get(d)
            if not fl:
                continue
            h = (hours or {}).get(n, {}).get(d, float(len(fl)))
            q = (flows or {}).get(n, {}).get(d, float(np.mean(fl)))
            c = lb * ce_ / h * cf_ / (q * 60 * B.K)
            ctl += float(f(c)) * q * 60 * B.K / cf_ * h
        out[n] = used - used * ce_ + ctl / B.TONS
    return out


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    I = B.Inputs(TARGET)
    g = B.press_tons(I, "golden")
    gw = whole(g)
    cov = B.covered(g)
    fg, (F, pp) = B.relation(I, "golden")
    e = W.everything()
    press = list(csv.DictReader(open(os.path.join(TARGET, P.FILES["press"]), encoding="utf-8")))
    hist = list(csv.DictReader(open(os.path.join(TARGET, P.FILES["hist"]), encoding="utf-8")))
    ca = B.cleaning_tons(I)
    ub = B.unaccounted_gal(I)
    ca1, ub1 = tenth(ca), gal(ub)

    # ---------------------------------------------------------------- R1: the field's raw material ships
    check("R1 the press logs ship one row per press, shift or job and material (%d rows, both record bases)" %
          len(press), len(press) >= 25000 and {r["record_basis"] for r in press} == {"SHIFT", "JOB"})
    check("R1 the historians ship every hour of 2026 for the ten oxidizers (%d rows)" % len(hist),
          len(hist) == 10 * 8760 and len({r["unit_tag"] for r in hist}) == 11)
    check("R1 the test summary ships %d tests of three runs on the ten oxidizers, both firms' bases" % len(I.tests),
          len(I.tests) == 28 and {t["basis"] for t in I.tests} == {"propane", "carbon"} and
          {t["plant"] for t in I.tests} == set(I.controlled))
    heads = []
    for kk, fn in P.FILES.items():
        p_ = os.path.join(TARGET, fn)
        if fn.endswith(".csv"):
            heads += open(p_, encoding="utf-8").readline().strip().lower().split(",")
        elif fn.endswith(".xlsx"):
            import openpyxl
            for ws in openpyxl.load_workbook(p_, read_only=True).worksheets:
                for row in ws.iter_rows(min_row=1, max_row=2, values_only=True):
                    heads += [str(v).lower() for v in row if v is not None]
    bad = [h for h in heads if re.search(r"inlet|outlet|destruction efficiency|\bdre\b|floor|dilut|press voc|"
                                         r"emitted|emission|controlled|2026 total|annual", h)]
    check("R1 no shipped column holds an inlet, an outlet, a destruction efficiency for 2026, a floor, a press VOC or "
          "an emission (%s)" % bad, not bad)
    docs = " ".join(doc_text(k) for k in ("rule", "letter", "profiles")).lower()
    intro = doc_text("tests").lower().split("ashcombe flexible packaging (facility")[0]
    check("R1 the documents read back (positive control: the rule's applicability sentence, the letter's Central time, "
          "the profiles' cleaning source and the tests' basis sentence)",
          "25 tons or more" in docs and "local (central) time" in docs and "cleaning" in docs and
          "reports concentrations and mass rates as propane" in intro)
    check("R1 no document sentence says an oxidizer's destruction depends on its inlet, names a floor, a dilute inlet, "
          "part production, turndown or a fan's air, or says how a test is carried to a year",
          not re.search(r"floor|dilut|part.production|turndown|whichever|less stringent|depends on|varies with|"
                        r"low load|fan(?! speed)|airflow|represent|carried|each day|per day", docs + " " + intro))

    # ---------------------------------------------------------------- R3: the analyst test on the clean truth
    tr = clean_truth(e)
    check("R3a the easy route on the clean truth (each plant's latest test efficiency on its captured VOC, every filed "
          "rule applied) files the default path's three: %s" % B.covered(tr["latest"]), B.covered(tr["latest"]) == DEFAULT)
    check("R3a the mean of each plant's tests on the clean truth files a wrong set too: %s" % B.covered(tr["mean"]),
          B.covered(tr["mean"]) != GOLD)
    check("R3b the decisive step alone on the clean truth (each day's outlet from the relation at the day's inlet) files "
          "the golden five", B.covered(tr["golden"]) == GOLD)
    dev = max(abs(g[n]["emitted"] - tr["golden"][n]) for n in I.order)
    check("R3 every golden plant figure sits within 0.25 tons of the generator's truth (largest gap %.3f)" % dev,
          dev < 0.25 and gw == whole(tr["golden"]))
    r0 = B.rung_tons(I, "R0")
    check("R3a the default path on the cut pack files the same three", B.covered(r0) == DEFAULT)
    tk = [(t["plant"], t["date"]) for t in I.tests]
    pairs = [(r["ci"], r["co"]) for t in I.tests for r in t["runs"]]
    check("R3c no plant: no oxidizer has two tests on a day, no run repeats another's, every test passed the permit's "
          "95 per cent (least %.2f)" % min(t["dre"] for t in I.tests),
          len(set(tk)) == len(tk) and len(set(pairs)) == len(pairs) and min(t["dre"] for t in I.tests) >= 95.0)
    check("R3c no plant: every test ran at maximum production, as the permits require",
          all(t["prod"].startswith("maximum production") for t in I.tests))

    # ---------------------------------------------------------------- R2: every Layer 1 item, mishandled
    ml = whole(B.press_tons(I, "golden", misread=True))
    mlr = B.press_tons(I, "golden", misread=True)
    check("R2a the less-water-and-exempt figures read as pounds per gallon of product: the water-based plants more "
          "than double (%s move) and Garrowby reaches %.2f, a wrong set" % (moved(ml, gw), mlr["Garrowby Printing"]
                                                                            ["emitted"]),
          B.covered(ml) != GOLD and set(moved(ml, gw)) <= {"Brinsley Label Works", "Dunsford Folding Cartons",
                                                           "Garrowby Printing", "Ivers Lane Press",
                                                           "Norhaven Converting", "Pellworth Label"})
    sh = defaultdict(lambda: defaultdict(float))
    for n, rows in I.rows.items():
        for st, en, lb, d in rows:
            sh[n][d + dt.timedelta(days=1) if (st.hour == 22 and n.startswith("Merrion")) else d] += lb
    s3 = whole(tons_with(I, day_voc={"Merrion Flexibles": dict(sh["Merrion Flexibles"])}))
    check("R2b Merrion's third shift put on the day it ends: the call holds (%s move)" % moved(s3, gw),
          B.covered(s3) == GOLD)
    ut = whole(B.press_tons(I, "golden", utc=True))
    check("R2c the historians' hours joined on their UTC dates: the call holds (%s move)" % moved(ut, gw),
          B.covered(ut) == GOLD)
    rated = {n: {d: I.ox[n]["Q"] for d in I.proc[n]} for n in I.ox if not I.ox[n]["fixed"]}
    rq = whole(tons_with(I, flows=rated))
    check("R2d the variable-speed fans read at their rated airflow, not the logged speed: the call holds (%s move)" %
          moved(rq, gw), B.covered(rq) == GOLD)
    J = with_tests(I, lambda t, r: dict(r, ci=r["ci"] / 3, co=r["co"] / 3) if t["basis"] == "propane" else r)
    pr = whole(B.press_tons(J, "golden"))
    check("R2e Marlow's propane figures read as carbon: the outlet relation no longer fits one floor (rms %.3f against "
          "%.3f) and the call moves (%s)" % (B.rms_of(J, B.relation(J)[0]), B.rms_of(I, fg), B.covered(pr)),
          B.rms_of(J, B.relation(J)[0]) > 3 * B.rms_of(I, fg) and B.covered(pr) != GOLD)
    c100 = whole(tons_with(I, ce={n: 1.0 for n in I.ox}))
    check("R2f every capture taken at 100 per cent: the capture-tested plants lose their uncaptured VOC and the call "
          "moves (%s)" % B.covered(c100), B.covered(c100) != GOLD and
          set(moved(c100, gw)) <= {n for n in I.ox if I.ce[n] < 1.0})
    dv_k = defaultdict(float)
    for r in press:
        if r["facility_no"] == "0142":
            d = dt.date.fromisoformat(r["log_date"])
            code = r["material_code"]
            q = float(r["quantity"])
            gl_ = q / I.prod[code]["den"] if r["uom"] == "LB" else q
            dv_k[d] += gl_ * I.vpg(code, d)
    kk_ = tons_with(I, day_voc={"Kelvedon Laminates": dict(dv_k)})
    check("R2g Thameside Laminating's rows (facility 0117) left out: Kelvedon falls to %.1f tons and the call moves" %
          kk_["Kelvedon Laminates"], kk_["Kelvedon Laminates"] < 25 and B.covered(kk_) != GOLD)

    Jm = copy.copy(I)
    Jm.day_voc = I.day_voc_misread
    Jc = copy.copy(I)
    Jc.ce = {n: 1.0 for n in I.ce}
    l1 = {"misread": B.covered(B.rung_tons(Jm, "R0")), "capture": B.covered(B.rung_tons(Jc, "R0")),
          "propane": B.covered(B.rung_tons(J, "R0"))}
    check("R2h no Layer 1 misreading turns the default path into the golden call (%s)" % l1,
          all(v != GOLD for v in l1.values()))

    # ---------------------------------------------------------------- the ladder
    sets = {r: B.covered(B.rung_tons(I, r)) for r in ("R0", "R1", "R2", "R3", "R3m", "R4", "R4m", "R4b", "R5")}
    check("R0 each plant's latest test efficiency: the default three", sets["R0"] == DEFAULT)
    check("R1 the mean of each plant's tests: Ashcombe in, Kelvedon out (%s)" % sets["R1"],
          sets["R1"] == sorted(DEFAULT + ["Ashcombe Flexible Packaging"]))
    check("R2 the permits' 95 per cent on every oxidizer: %d plants" % len(sets["R2"]),
          len(sets["R2"]) >= 7 and set(GOLD) < set(sets["R2"]))
    check("R3 the relation at each plant's 2026 mean inlet: Kelvedon out (%s)" % sets["R3"],
          sets["R3"] == sorted(DEFAULT + ["Ashcombe Flexible Packaging"]))
    check("R3m the relation at each month's mean inlet: Kelvedon out", sets["R3m"] == sets["R3"])
    check("R4 the latest test's outlet concentration on each day's air: Larkmoor in (%s)" % sets["R4"],
          sets["R4"] == sorted(GOLD + ["Larkmoor Graphics"]))
    check("R4m the mean of the tests' outlets on each day's air: Larkmoor in", sets["R4m"] == sets["R4"])
    check("R4b the latest test's outlet rate over the year's process hours: Larkmoor in", sets["R4b"] == sets["R4"])
    check("R5 each oxidizer's own tests only (Kelvedon's all concentrated): Kelvedon out", sets["R5"] == sets["R3"])
    rk = {r: B.rung_tons(I, r) for r in ("R0", "R3", "R4")}
    check("L the rungs' margins: the default puts Ashcombe at %.1f and Kelvedon at %.1f, the year's mean inlet puts "
          "Kelvedon at %.1f, the test outlet puts Larkmoor at %.1f" % (rk["R0"]["Ashcombe Flexible Packaging"],
                                                                     rk["R0"]["Kelvedon Laminates"],
                                                                     rk["R3"]["Kelvedon Laminates"],
                                                                     rk["R4"]["Larkmoor Graphics"]),
          rk["R0"]["Ashcombe Flexible Packaging"] < 23 and rk["R0"]["Kelvedon Laminates"] < 23 and
          rk["R3"]["Kelvedon Laminates"] < 24 and rk["R4"]["Larkmoor Graphics"] > 27)

    # ---------------------------------------------------------------- the golden's licensed family
    fam = {}
    for how in ("golden", "median", "lsq", "smooth8", "smooth16", "smooth32", "interp"):
        fam[how] = B.press_tons(I, how)
    for v in sorted({o["vendor"] for o in I.ox.values()}):
        fv = B.relation(I, "golden", sel=lambda t, v=v: I.ox[t["plant"]]["vendor"] == v)[0]
        fam["vendor " + v] = {n: (B.press_tons(I, f=fv, how=None)[n] if I.ox.get(n, {}).get("vendor") == v else g[n])
                              for n in I.order}
    for firm in sorted({t["firm"] for t in I.tests}):
        fam["firm " + firm] = B.press_tons(I, f=B.relation(I, "golden", sel=lambda t, x=firm: t["firm"] == x)[0],
                                           how=None)
    fam["hour grain"] = B.press_tons(I, "golden", grain="hour")
    alt = {}
    for lo, hi in ((1500.0, 3500.0), (2200.0, 2800.0)):
        ci, co = I.ci, I.co
        Fx, px = co[ci < lo].mean(), (co[ci > hi] / ci[ci > hi]).mean()
        alt["cut %d/%d" % (lo, hi)] = B.press_tons(I, f=B.hard(Fx, px), how=None)
    fam.update(alt)
    rms = {how: B.rms_of(I, B.relation(I, how)[0]) for how in ("golden", "median", "lsq", "smooth8", "smooth16",
                                                               "smooth32", "interp", "linear")}
    check("G1 every standing member fits the runs within 1.2 times the hard floor's residual (%s); the straight line "
          "does not (%.3f)" % (", ".join("%s %.4f" % kv for kv in rms.items() if kv[0] != "linear"), rms["linear"]),
          all(v <= 1.2 * rms["golden"] for k, v in rms.items() if k != "linear") and rms["linear"] > 3 * rms["golden"])
    check("G2 every member (%d: estimators, forms, groupings by vendor and firm, the hour grain, the cut points) files "
          "the golden five and the 14 whole tons" % len(fam),
          all(B.covered(t) == GOLD and whole(t) == gw for t in fam.values()))
    lo_cov = min(g[n]["emitted"] for n in GOLD)
    hi_out = max(g[n]["emitted"] for n in I.order if n not in GOLD)
    check("G3 the lowest covered plant clears 25 by %.1f tons and the nearest below falls %.1f short" %
          (lo_cov - 25, 25 - hi_out), lo_cov - 25 >= 2.0 and 25 - hi_out >= 2.0)
    edge = min(min(abs((t[n]["emitted"] % 1.0) - 0.5) for n in I.order) for t in fam.values())
    check("G4 every member's every plant sits 0.15 tons or more from a rounding half (least %.3f)" % edge, edge >= 0.15)
    check("G5 no golden plant figure is a round figure before rounding",
          all(abs(g[n]["emitted"] - round(g[n]["emitted"])) > 0.03 for n in I.order))
    ln = whole(B.press_tons(I, "linear"))
    check("G6 even the refuted straight line files the golden five (its figures move: %s)" % moved(ln, gw),
          B.covered(ln) == GOLD)

    # ---------------------------------------------------------------- SF1 to SF22
    J = copy.copy(I)
    J.prod = copy.deepcopy(I.prod)
    for code, x in J.prod.items():
        x["exempt"] = 0.0
    sf1 = defaultdict(lambda: defaultdict(float))
    for r in press:
        n = I.fac[r["facility_no"]]
        d = dt.date.fromisoformat(r["log_date"])
        code = r["material_code"]
        q = float(r["quantity"])
        gl_ = q / I.prod[code]["den"] if r["uom"] == "LB" else q
        sf1[n][d] += gl_ * J.vpg(code, d)
    t1 = whole(tons_with(I, day_voc={n: dict(v) for n, v in sf1.items()}))
    check("SF1 acetone counted as VOC in the press washes: the call holds (%s move)" % moved(t1, gw),
          B.covered(t1) == GOLD)
    t2 = {n: g[n]["emitted"] + ca[n] for n in I.order}
    check("SF2 cleaning away from the presses added to the press VOC: the call holds (least gap below %.1f)" %
          (25 - max(v for n, v in t2.items() if n not in GOLD)), B.covered(t2) == GOLD)
    days = [dt.date.fromisoformat(r["log_date"]) for r in press]
    proc_utc = [r["hour_beginning_utc"] for r in hist if r["mode"] == "PROCESS"]
    check("SF3 2026 by local or UTC days: every press day and PROCESS hour falls inside 2026 either way",
          min(days) >= dt.date(2026, 1, 2) and max(days) <= dt.date(2026, 12, 30) and
          min(proc_utc) >= "2026-01-02" and max(proc_utc) < "2026-12-31")
    check("SF4 every capture at 100 per cent moves the call (R2f); the register's Capture sheet gives each plant's "
          "determination", B.covered(c100) != GOLD and all(n in I.ce for n in I.ox))
    check("SF5 the tested efficiencies (R0) and the permits' minimum (R2) are rungs, not readings of 'destroyed'",
          sets["R0"] == DEFAULT and sets["R2"] != GOLD)
    check("SF6 each test report states its basis, propane or carbon, and read on one basis the relation fits (R2e)",
          all(t["basis"] in ("propane", "carbon") for t in I.tests) and B.rms_of(I, fg) < 0.02)
    cf1 = whole(tons_with(I, cf={n: 0.55 for n in I.ox}))
    check("SF7 one carbon content (0.55) for every plant: the call holds (%s move)" % moved(cf1, gw),
          B.covered(cf1) == GOLD)
    check("SF8 the historians' airflow is standard (scfm), the speed-logging units at their rated airflow times speed "
          "(R2d for the rated airflow alone)", B.covered(rq) == GOLD and
          all(I.ox[n]["logs"].startswith(("Exhaust", "Fan")) for n in I.ox))
    allh = {n: {d: float(len(I.all_hours[n].get(d, []))) for d in I.proc[n]} for n in I.ox}
    t9 = tons_with(I, hours=allh)
    check("SF9 every non-OFF hour of a production day's date counted as process time: the call moves (%s), so the "
          "PROCESS mode is the oxidizer's treating time the press days fill" % B.covered(t9),
          all(len(I.proc[n][d]) <= 25 for n in I.ox for d in I.proc[n]))
    check("SF10 the relation's form: the hard floor, the smooth knees and the interpolation agree (G2)",
          all(B.covered(fam[k]) == GOLD for k in ("smooth8", "smooth16", "smooth32", "interp")))
    check("SF11 the floor pooled across the ten oxidizers, by vendor or by firm: the same call; each oxidizer's own "
          "tests leave Kelvedon's dilute days unmeasured (R5)", sets["R5"] != GOLD and
          all(B.covered(fam[k]) == GOLD for k in fam if k.startswith(("vendor", "firm"))))
    check("SF12 figures.json's tons, tenths and gallons round from the unrounded figures",
          all(f["plants"][n]["press_voc_tons"] == gw[n] and f["plants"][n]["cleaning_voc_tons"] == ca1[n] and
              f["plants"][n]["unaccounted_gal"] == ub1[n] for n in I.order))
    check("SF13 no heatset press and no retention: no shipped file names heatset, retention or a retained share",
          not re.search(r"heatset|retention|retained", " ".join(heads) + docs))
    k0117 = sum(1 for r in press if r["facility_no"] == "0117")
    check("SF14 Thameside Laminating's rows (%d) carry facility 0117 before 1 May 2026 and the register names it "
          "Kelvedon's former name (R2g)" % k0117, k0117 > 0 and all(dt.date.fromisoformat(r["log_date"]) < W.ACQUIRED
                                                                   for r in press if r["facility_no"] == "0117"))
    t15 = tenth(B.cleaning_tons(I, press_issues=True))
    check("SF15 press wash issued to the presses counted as cleaning: every ask A figure moves (%d of 14)" %
          len(moved(t15, ca1)), len(moved(t15, ca1)) == 14)
    t16 = tenth(B.cleaning_tons(I, credit=False, washers=False))
    check("SF16 the issues alone: %d of 14 ask A figures move" % len(moved(t16, ca1)), len(moved(t16, ca1)) >= 12)
    t17 = tenth(B.cleaning_tons(I, voc_pct=False))
    check("SF17 the waste's weight credited as VOC: every ask A figure moves", len(moved(t17, ca1)) == 14)
    t18 = tenth(B.cleaning_tons(I, removed=False))
    check("SF18 the washers' solvent added alone: every ask A figure moves", len(moved(t18, ca1)) == 14)
    t19 = gal(B.unaccounted_gal(I, by_ship=False))
    check("SF19 received by document date in place of ship date: %d of 14 ask B figures move" % len(moved(t19, ub1)),
          len(moved(t19, ub1)) >= 8)
    cd = {r["count_date"] for r in csv.DictReader(open(os.path.join(TARGET, P.FILES["counts"]), encoding="utf-8"))}
    check("SF20 the stock counts are the two physical counts the letter names: %s" % sorted(cd),
          cd == {"2026-01-01", "2026-12-31"})
    t21 = gal(B.unaccounted_gal(I, returns=False))
    check("SF21 returns left out: %d of 14 ask B figures move" % len(moved(t21, ub1)), len(moved(t21, ub1)) >= 5)
    t22 = gal(B.unaccounted_gal(I, lb=False))
    check("SF22 pounds read as gallons: Kelvedon's figure moves", "Kelvedon Laminates" in moved(t22, ub1))

    # ---------------------------------------------------------------- ask A devices
    truth_a = {W.BY[c]["name"]: v["tons"] for c, v in e["ask_a"]["truth"].items()}
    check("A fair: the golden handling reproduces the generator's cleaning VOC to the pound",
          max(abs(ca[n] - truth_a[n]) for n in I.order) < 1e-6)
    a_v = tenth(B.cleaning_tons(I, vintage=False))
    check("A primary (D2): HW-CS-210 on the master's current revision for every issue moves every figure (%d of 14), "
          "least move %.2f tons" % (len(moved(a_v, ca1)), min(abs(B.cleaning_tons(I, vintage=False)[n] - ca[n])
                                                               for n in I.order)), len(moved(a_v, ca1)) == 14)
    a_s = tenth(B.cleaning_tons(I, stellar=False))
    check("A hazard (D4): Ostrander's washer services left out moves the six plants that moved (%s)" % moved(a_s, ca1),
          sorted(moved(a_s, ca1)) == sorted(W.BY[c]["name"] for c in A.STELLAR))
    a_k = tenth(B.cleaning_tons(I, kg=False))
    check("A hazard (D3): the KG manifests read as pounds moves the two plants (%s)" % moved(a_k, ca1),
          sorted(moved(a_k, ca1)) == sorted(W.BY[c]["name"] for c in A.KG_PLANTS))
    a_cr = tenth(B.cleaning_tons(I, vintage=False, stellar=False))
    check("A the cracker (master revision, tickets only, every filed rule): 0 of 14", not (set(n for n in I.order if
                                                                                         a_cr[n] == ca1[n])))
    revlog = I.revs
    check("A silent: the master carries HW-CS-210's current revision only; the earlier formula sits on the revision log "
          "with its date, among %d benign revisions" % (len(W.REVISIONS) - 1),
          len(revlog) == 1 and revlog[0][0] == "HW-CS-210" and revlog[0][1] == W.REFORMULATED)
    tick = list(csv.DictReader(open(os.path.join(TARGET, P.FILES["tickets"]), encoding="utf-8")))
    last = defaultdict(str)
    for r in tick:
        last[I.fac[r["facility_no"]]] = max(last[I.fac[r["facility_no"]]], r["service_date"])
    check("A fair (D4): Wexcombe's tickets stop in June at the six plants and Ostrander's payment lines carry the gallons",
          all(last[W.BY[c]["name"]] < "2026-07-01" for c in A.STELLAR) and
          all(last[n] >= "2026-11-15" for n in I.order if n not in [W.BY[c]["name"] for c in A.STELLAR]))

    # ---------------------------------------------------------------- ask B devices
    truth_b = {W.BY[c]["name"]: v["gallons"] for c, v in e["ask_b"]["truth"].items()}
    check("B fair: the golden handling reproduces the generator's unaccounted gallons (largest gap %.4f)" %
          max(abs(ub[n] - truth_b[n]) for n in I.order), max(abs(ub[n] - truth_b[n]) for n in I.order) < 0.01)
    b_c = B.unaccounted_gal(I, chain=False)
    check("B primary (D7): Haldane's pre-April item numbers read on the current catalog move every figure (%d of 14), "
          "least move %.0f gal" % (len(moved(gal(b_c), ub1)), min(abs(b_c[n] - ub[n]) for n in I.order)),
          len(moved(gal(b_c), ub1)) == 14 and min(abs(b_c[n] - ub[n]) for n in I.order) >= 20)
    check("B silent (D7): on the current catalog the old numbers all join (no unmatched line) and every figure rises",
          all(b_c[n] > ub[n] for n in I.order))
    cat, old = B.catalog(I)
    hal = B._sheet(TARGET, "haldane", "Statement detail", header_row=2)
    items = {str(r["Item"]) for r in hal}
    check("B silent: every statement item is a catalog item number (%d items)" % len(items), items <= set(cat))
    check("B fair: each old number a current item replaces is the number the statement carried before 1 April",
          all(any(str(r["Item"]) == o and (r["Doc date"].date() if isinstance(r["Doc date"], dt.datetime) else
                                            r["Doc date"]) < B.RENUMBERED for r in hal) for o in old))
    check("B no marker: the pre-April lines carry the same columns, account numbers and description style as the rest",
          len({tuple(sorted(k for k in r if r[k] is not None)) for r in hal}) == 1)

    # ---------------------------------------------------------------- separation and distractors
    call_keys = ("register", "press", "sds", "hist", "tests")
    ask_keys = ("issues", "manifests", "profiles", "tickets", "payments", "corvane", "haldane", "catalog", "counts")
    dX = subset(call_keys)
    IX = B.Inputs(dX)
    check("X1 the call from its own five files alone: the golden five and the 14 whole tons",
          whole(B.press_tons(IX, "golden")) == gw)
    shutil.rmtree(dX)
    dA = subset(ask_keys + ("register", "sds", "press", "hist", "tests"))
    IA = B.Inputs(dA)
    check("X2 the asks from their files (with the register, the master and the press logs' gallons)",
          tenth(B.cleaning_tons(IA)) == ca1 and gal(B.unaccounted_gal(IA)) == ub1)
    shutil.rmtree(dA)
    pmat = {r["material_code"] for r in press}
    check("X3 no ask device row sits in the call's population: no press material is a cleaning material, the "
          "reformulated product is never logged on a press, and the renumbered items are cleaning and press-wash drums",
          "HW-CS-210" not in pmat and all(I.prod[m]["kind"] != "CLEANING" for m in pmat) and
          {cat[new]["code"] for new in old.values()} == {c for c, _ in A.OLD_ITEM})
    dD = subset([k for k in P.FILES if k not in ("presses", "ozone")])
    ID = B.Inputs(dD)
    check("X4 the distractors deleted: the call, the 14 whole tons and both asks unchanged",
          whole(B.press_tons(ID, "golden")) == gw and tenth(B.cleaning_tons(ID)) == ca1 and
          gal(B.unaccounted_gal(ID)) == ub1)
    shutil.rmtree(dD)

    # ---------------------------------------------------------------- input gates
    files = os.listdir(TARGET)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("I ten or more files (%d)" % len(files), len(files) >= 10)
    check("I three or more formats (%s)" % sorted({fn.rsplit(".", 1)[1] for fn in files}),
          len({fn.rsplit(".", 1)[1] for fn in files}) >= 3)
    check("I one file of 25,000 rows or more (press logs %d, historians %d)" % (len(press), len(hist)),
          len(press) >= 25000)
    check("I two distractors named in metadata.json, none in a file name",
          len(meta["distractor_files"]) >= 2 and all(d_ in files for d_ in meta["distractor_files"]) and
          not any("distract" in fn for fn in files))

    # ---------------------------------------------------------------- realism
    win = I.window
    ok = all(len(I.proc[n][d]) in (15, 16, 17, 23, 24, 25) for n in I.ox for d in I.proc[n])
    check("Z every production day's PROCESS hours are its shifts' (16 or 24, a daylight-saving hour either way)", ok)
    run_ok = all(abs(r["mi"] - r["ci"] * r["qi"] * 60 * (W.K_PROPANE if t["basis"] == "propane" else W.K))
                 <= 0.011 + 0.0006 * r["mi"] for t in I.tests for r in t["runs"])
    check("Z every test run's inlet mass rate is its concentration times its flow on its firm's basis", run_ok)
    check("Z every test's destruction is the firm's mass-rate figure, within its printed precision",
          all(abs(100 * (1 - r["mo"] / r["mi"]) - r["dre"]) < 0.02 for t in I.tests for r in t["runs"]))
    dates = [dt.date.fromisoformat(r["log_date"]) for r in press]
    check("Z no press row on a Sunday, a holiday or the year-end shutdown",
          all(d.weekday() != 6 and d not in W.HOLIDAYS for d in dates))
    ea = min(abs((ca[n] * 10) % 1.0 - 0.5) for n in I.order)
    eb = min(abs(ub[n] % 1.0 - 0.5) for n in I.order)
    check("Z every ask A figure sits 0.005 tons or more from a rounding half (least %.4f) and every ask B figure "
          "0.05 gallons or more (least %.3f)" % (ea / 10, eb), ea >= 0.05 and eb >= 0.05)
    gcsv = list(csv.DictReader(open(os.path.join(TASK, "golden", "deq_printing_press_voc_2026.csv"), encoding="utf-8")))
    check("Z the golden CSV carries the 14 whole tons in register order",
          [r["plant"] for r in gcsv] == I.order and [int(r["press_voc_2026_tons"]) for r in gcsv] ==
          [gw[n] for n in I.order])
    cnt = defaultdict(int)
    mon = defaultdict(lambda: defaultdict(float))
    for r in press:
        cnt[I.fac[r["facility_no"]]] += 1
    for n, dv in I.day_voc.items():
        for d, lb in dv.items():
            mon[n][d.month] += lb
    check("Z no two plants share a press log row count, and no plant repeats a month's VOC to the pound",
          len(set(cnt.values())) == len(cnt) and all(len({round(v) for v in m.values()}) == len(m) for m in mon.values()))
    fl = defaultdict(list)
    for r in hist:
        if r["mode"] == "PROCESS" and r["fan_speed_pct"]:
            fl[r["unit_tag"]].append(r["fan_speed_pct"])
    blocks = [tuple(v[i:i + 24]) for v in fl.values() for i in range(0, len(v) - 24, 24)]
    check("Z no 24-hour block of a speed-logging historian repeats another", len(set(blocks)) == len(blocks))
    pay_txt = [r["description"] for r in csv.DictReader(open(os.path.join(TARGET, P.FILES["payments"]),
                                                              encoding="utf-8"))]
    st_lines = [x for x in pay_txt if x.startswith("Washer")]
    check("Z every Ostrander service line is its own (washer, date, gallons), none repeated",
          len(set(st_lines)) == len(st_lines) and len(st_lines) > 0)
    inv = list(csv.DictReader(open(os.path.join(TARGET, P.FILES["corvane"]), encoding="utf-8")))
    check("Z Corvane's export carries deliveries shipped from late December 2025 and invoiced to January 2027",
          min(r["SHIP_DATE"] for r in inv) < "20260101" and max(r["INVOICE_DATE"] for r in inv) >= "20270101")

    n_fail = sum(1 for _, ok_ in RESULTS if not ok_)
    print("%s  task482 checks: %d assertions, %d failed" % ("PASS" if not n_fail else "FAIL", len(RESULTS), n_fail))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())

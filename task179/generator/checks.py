"""task179 generator checks: input gates, the three-rules block on the clean truth (the analyst test executed), the
golden family and the rivals against the bin, a one-sigma move, every semantic fork row, the ask devices on every
route, separation, documents and realism. Exit 1 on any failure.

    python3 task179/generator/checks.py [target]"""
from __future__ import annotations

import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C      # noqa: E402
import calc             # noqa: E402
import deliver          # noqa: E402
import ceiling          # noqa: E402
import docs as D        # noqa: E402

FAILS = []
N = [0]


def ok(name, cond, detail=""):
    N[0] += 1
    print("%s  %-44s %s" % ("PASS" if cond else "FAIL", name, detail))
    if not cond:
        FAILS.append(name)


def inbin(x, centre=None):
    c = deliver.r250(x) if centre is None else centre
    return deliver.r250(x) == c


def main(target):
    task = os.path.dirname(target)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    meta = json.load(open(os.path.join(task, "metadata.json")))
    files = sorted(os.listdir(target))
    # ------------------------------------------------------------------ input gates
    ok("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    fmts = sorted(set(f.rsplit(".", 1)[1] for f in files))
    ok("G2 three or more formats", len(fmts) >= 3, ", ".join(fmts))
    big = [f for f in files if f.endswith(".csv") and sum(1 for _ in open(os.path.join(target, f))) - 1 >= 25000]
    ok("G3 a file of 25,000 rows or more", bool(big), ", ".join(big))
    ok("G4 two or more distractors named", len(meta["distractor_files"]) >= 2, ", ".join(meta["distractor_files"]))
    src = open(os.path.join(HERE, "calc.py")).read()
    ok("G5 distractors unused by the golden", not any(d in src for d in ("F_HALL", "F_NSL", C.F_HALL, C.F_NSL)))
    ok("G6 every file has a source, date and licence", all(f in meta["sources"] for f in files if f != "metadata.json"))
    # ------------------------------------------------------------------ the call on the pack
    r = calc.compute(target)
    a = r["frame"]
    call = r["call"]
    ok("R1 call printed", figs["call_not_enrolled_2027"] == deliver.r250(call), "%.1f -> %d" % (call, deliver.r250(call)))
    lo, hi = figs["call_not_enrolled_2027"] - 125, figs["call_not_enrolled_2027"] + 125
    ok("R2 golden well inside its bin", lo + 40 <= call <= hi - 40, "%.1f in [%d, %d)" % (call, lo, hi))
    aic = r["aic"]
    amin = min(v[2] for v in aic.values())
    ok("B0 the filed criterion picks the golden's form", r["form"] == min(aic, key=lambda k: aic[k][2]), r["form"])
    ok("SF10 the model form, closed by SELECT_PIN: the lowest AIC prints the call", inbin(aic[r["form"]][0], figs["call_not_enrolled_2027"])
       and "Akaike" in D.SELECT_PIN, "%s %.1f" % (r["form"], aic[r["form"]][0]))
    for k, v in sorted(aic.items(), key=lambda kv: kv[1][2]):
        if v[2] - amin <= 12:
            ok("B1 form %s (within 12 AIC) prints the call" % k, inbin(v[0], figs["call_not_enrolled_2027"]),
               "%.1f (dAIC %.1f)" % (v[0], v[2] - amin))
        else:
            ok("B2 form %s (more than 12 AIC worse) recorded" % k, True,
               "%.1f (dAIC %.1f)%s" % (v[0], v[2] - amin, "" if inbin(v[0], figs["call_not_enrolled_2027"]) else ", outside the bin"))
    for k in ("none", "any", "log", "sqrt", "ge22"):
        ok("B3 rival %s refuted by the criterion" % k, aic[k][2] - amin > 15, "dAIC %.1f" % (aic[k][2] - amin))
    for yrs in ([2022, 2023, 2024, 2025], [2023, 2024, 2025]):
        v = calc.forecast(a, r["form"], yrs)[0]
        ok("B4 the golden form on intakes %d to 2025 prints the call" % yrs[0], inbin(v, figs["call_not_enrolled_2027"]), "%.1f" % v)
    rivals = {"none": aic["none"]}
    ok("L1 the exposure-free model refuted loudly", aic["none"][1] < r["ll"] - 200, "dLL %.1f" % (aic["none"][1] - r["ll"]))
    hist_rate = float(a[a["intake"] < 2026]["gone"].mean())
    last = float(a[a["intake"] == 2025]["gone"].mean()) * r["n2026"]
    ok("R3 the record's rate and last intake's rate miss", not inbin(hist_rate * r["n2026"], figs["call_not_enrolled_2027"])
       and not inbin(last, figs["call_not_enrolled_2027"]),
       "pooled %.1f, last %.1f" % (hist_rate * r["n2026"], last))
    # one-sigma move: bootstrap the record's entrants
    g = C.stream("checks/bootstrap")
    h = a[a["intake"] < 2026].reset_index(drop=True)
    f = a[a["intake"] == 2026]
    Xf = calc.design(f, r["form"])
    sims = []
    for _ in range(12):
        idx = g.integers(0, len(h), len(h))
        hb = h.iloc[idx]
        b, _ = calc.logit_fit(calc.design(hb, r["form"]), hb["gone"].values.astype(float))
        sims.append(float((1 / (1 + np.exp(-(Xf @ b)))).sum()))
    sd = float(np.std(sims, ddof=1))
    ok("R4 a one-sigma move keeps the printed call", inbin(call - sd, figs["call_not_enrolled_2027"]) and inbin(call + sd, figs["call_not_enrolled_2027"]),
       "sd %.1f (%.1f per cent)" % (sd, 100 * sd / call))
    # ------------------------------------------------------------------ three rules on the clean truth (dataset-generation 7.1)
    from world import World
    w = World()
    H = [w.cohorts[y] for y in C.INTAKES[:-1]]
    Fc = w.cohorts[C.FORWARD]
    truth = float(Fc.p.sum())

    def Xw(c, ties):
        cols = [c.ascz, c.fif, c.pt, c.mature, c.hard, c.prisk, c.lc, c.hall,
                np.array([(d - __import__("datetime").date(c.y, 1, 1)).days for d in c.accepted]) / 100.0]
        cols += [(c.fac == fc).astype(float) for fc in C.FAC_CODES[1:]]
        if ties:
            t = c.ties
            cols += [((t >= lo_) & (t < hi_)).astype(float) for lo_, hi_ in zip(calc.BANDS[:-1], calc.BANDS[1:])][1:]
        return np.column_stack([np.ones(c.n)] + cols)
    for label, ties in (("easy route", False), ("decisive step", True)):
        b, _ = calc.logit_fit(np.vstack([Xw(c, ties) for c in H]), np.concatenate([c.gone for c in H]).astype(float))
        est = float((1 / (1 + np.exp(-(Xw(Fc, ties) @ b)))).sum())
        if ties:
            ok("T2 the decisive step alone files the golden", inbin(est, figs["call_not_enrolled_2027"]), "%.1f" % est)
        else:
            ok("T1 analyst test: every rule read, the easy route", deliver.r250(est) == 2250, "%.1f -> %d" % (est, deliver.r250(est)))
    ok("T3 the clean truth sits in the golden's bin", inbin(truth, figs["call_not_enrolled_2027"]), "expected %.1f" % truth)
    ok("T4 lever 30 per cent or more", (call - aic["none"][0]) / call >= 0.30, "%.1f per cent" % (100 * (call - aic["none"][0]) / call))
    # ------------------------------------------------------------------ semantic forks on the call
    import pandas as pd
    d = r["data"]
    # SF1 leave read as enrolled
    en = calc.enrolled_sets(d)
    cz = d["census"].copy()
    cz["Y"] = cz["CENSUS_DATE"].map(calc.census_year)
    lv = {y: set(gg["STUDENT_ID"]) for y, gg in cz[cz["STATUS"].isin(["LV", "On leave"])].groupby("Y")}
    xw = dict(zip(d["xwalk"]["SIRIUS_STUDENT_NO"], d["xwalk"]["ARC_ID"]))
    a1 = a.copy()
    for i, (sid, y) in enumerate(zip(a1["sid"], a1["intake"])):
        if y < 2025 and sid in lv.get(y + 1, set()):
            a1.iloc[i, a1.columns.get_loc("gone")] = 0
        if y == 2025 and xw.get(sid) in lv.get(2026, set()):
            a1.iloc[i, a1.columns.get_loc("gone")] = 0
    v = calc.forecast(a1, r["form"])[0]
    ok("SF1 leave read as enrolled: ruled out by ENROLLED_PIN", ENROLLED_PIN_OK, "%.1f -> %d" % (v, deliver.r250(v)))
    # SF2 credit-transfer entrants kept in the intake: they have no first-year class rows and are not first-time
    adm = calc.entrants(d)
    ok("SF2 credit transfer entrants excluded (INTAKE_PIN)", "Credit transfer" not in set(adm["Entry Basis"]), "")
    # SF3 conjoint entrants counted once
    ok("SF3 conjoint entrants once", a.groupby(["sid", "intake"]).size().max() == 1, "")
    # SF4 blank week-6 ratings dropped instead of the middle value
    a4 = a.copy()
    a4["prisk"] = a4["prisk"].where(a4["prisk"] != 0.5, a4["prisk"].median())
    v = calc.forecast(a4, r["form"])[0]
    ok("SF4 blank ratings at the median: same call", inbin(v, figs["call_not_enrolled_2027"]), "%.1f" % v)
    # SF5 ASC points standardised within the intake: same call
    a5 = a.copy()
    a5["asc"] = a5.groupby("intake")["asc"].transform(lambda s: (s - s.mean()) / s.std() * 34 + 186)
    v = calc.forecast(a5, r["form"])[0]
    ok("SF5 ASC within-intake scaling: same call", inbin(v, figs["call_not_enrolled_2027"]), "%.1f" % v)
    # SF6 repeat classmates counted over the whole timetable, every student: the extracts hold entrants only
    ok("SF6 the class extracts hold first-time entrants only", set(d["acls"]["arc_student_id"]) <= set(adm["sid"]), "")
    # SF7 the forecast as the expected count against a simulated count: the conventions report a count; same call
    sims = []
    pf = 1 / (1 + np.exp(-(calc.design(f, r["form"]) @ r["coef"])))
    for _ in range(200):
        sims.append(float((g.random(len(pf)) < pf).sum()))
    ok("SF7 a simulated count's median prints the call", inbin(float(np.median(sims)), figs["call_not_enrolled_2027"]), "%.0f" % np.median(sims))
    # SF8 the age line at 21 against age as a number: same call
    a8 = a.copy()
    a8["mature"] = (a8["age"] - 18).clip(0, 30) / 10.0
    v = calc.forecast(a8, r["form"])[0]
    ok("SF8 age as a number: same call", inbin(v, figs["call_not_enrolled_2027"]), "%.1f" % v)
    # SF9 faculty from the first-listed programme against the second: conjoint entrants are few, same call
    ok("SF9 faculty of the first-listed programme", True, "admissions Faculty column, first-listed programme")
    # ------------------------------------------------------------------ the ask: devices on every route, determinacy
    akeys = [k for k in figs if k.startswith("ask_")]
    gold = ceiling.route(d, ceiling.SLOT, "golden")
    ok("A0 golden route reproduces the ask", all(gold[k] == figs[k] for k in akeys), "%d figures" % len(akeys))
    for name, (cols, rule) in ceiling.ROUTES.items():
        rr = ceiling.route(d, cols, rule)
        hits = [k for k in akeys if rr[k] == figs[k]]
        ok("A1 route %s keeps at most one cell" % name[:48], len(hits) <= 1, ", ".join(hits))
    tt = d["tt"]
    act = tt[tt["Class Status"] == "Active"]
    pair_codes = {}
    for m_, r_ in w.pairs:
        for x in (m_, r_):
            pair_codes["%s-26S1-%03d" % (x["paper"], x["k"])] = (m_, r_)
    arc_ok, sir_ok = True, True
    for m_, r_ in w.pairs:
        codes = ["%s-26S1-%03d" % (x["paper"], x["k"]) for x in (m_, r_)]
        rows_ = act[act["Class Code"].isin(codes)]
        shown = rows_.groupby("Class Code")["Enrolled at Census"].first()
        caps = rows_["Room Capacity"]
        tot = m_["enrolled"] + r_["enrolled"]
        if m_.get("combined"):
            arc_ok &= len(set(shown)) == 1 and shown.iloc[0] == tot and (2 * tot > caps).all()
        else:
            sir_ok &= sorted(shown) == sorted([m_["enrolled"], r_["enrolled"]]) and (tot <= caps).all()
    ok("A2 ARC combinations: the combination's enrolment on each class, more than the room seats added", arc_ok)
    ok("A3 classes carried from SIRIUS: own enrolments, fitting the room added", sir_ok)
    eq = sum(1 for m_, r_ in w.pairs if not m_.get("combined") and m_["enrolled"] == r_["enrolled"])
    ok("A4 SIRIUS pairs with equal enrolments in every faculty and level", eq == 10, "%d" % eq)
    multi = act.groupby(["Room", "Day", "Start", "Teaching Weeks"])["Class Code"].nunique()
    shared = set()
    for k in multi[multi > 1].index:
        cs = set(act[(act["Room"] == k[0]) & (act["Day"] == k[1]) & (act["Start"] == k[2]) & (act["Teaching Weeks"] == k[3])]["Class Code"])
        shared |= cs
    ok("A5 the only classes sharing a slot are the papers taught together", shared <= set(pair_codes), "%d classes" % len(shared))
    # separation: no device row in the call's population
    ok("S2 classes taught together are 200 level and above", all(x["level"] >= 200 for pair in w.pairs for x in pair))
    first = act[act["Level"] == 100]
    ok("S3 first-year classes meet in no shared slot", not first.duplicated(["Room", "Day", "Start", "Teaching Weeks"]).any())
    # ------------------------------------------------------------------ documents
    from pypdf import PdfReader
    conv = " ".join(p.extract_text() for p in PdfReader(os.path.join(target, C.F_CONV)).pages)
    cut = " ".join(p.extract_text() for p in PdfReader(os.path.join(target, C.F_CUT)).pages)
    flat = lambda s: re.sub(r"\s+", " ", s)
    for pin in ("ENROLLED_PIN", "INTAKE_PIN", "CALL_PIN", "SELECT_PIN", "GROUP_PIN"):
        ok("D1 %s in the conventions" % pin, flat(getattr(D, pin))[:60] in flat(conv))
    banned = re.compile(r"allocat|block|classmate|peer|cohesion|integration|learning communit|together in two|repeat",
                        re.I)
    dic = open(os.path.join(target, C.F_DICT)).read()
    for nm, txt in (("conventions", conv), ("cutover notes", cut)):
        hits = sorted(set(m.group(0).lower() for m in banned.finditer(txt)))
        ok("D2 %s carry none of the decisive step's words" % nm, not hits or hits == ["together"], ", ".join(hits))
    hits = sorted(set(m.group(0).lower() for m in banned.finditer(dic)))
    ok("D3 dictionary carries none of the decisive step's words", hits in ([], ["learning communit"]), ", ".join(hits))
    ok("D4 no em or en dash in documents", not re.search("[–—]", conv + cut + dic))
    # ------------------------------------------------------------------ realism
    sc = d["scls"]
    sizes = sc.groupby(["TERM", "CLASS_NBR"]).size()
    ok("Q1 class sizes vary (no single size dominates)", sizes.value_counts(normalize=True).max() < 0.5,
       "largest share %.2f at %d" % (sizes.value_counts(normalize=True).max(), sizes.value_counts().idxmax()))
    print("checks: %d run, %d failed%s" % (N[0], len(FAILS), (": " + ", ".join(FAILS)) if FAILS else ""))
    return 1 if FAILS else 0


ENROLLED_PIN_OK = "approved leave is not enrolled" in D.ENROLLED_PIN

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))

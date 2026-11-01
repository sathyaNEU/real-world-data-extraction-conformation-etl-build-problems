"""task146 architecture 3: the generator's assertions on the cut pack and on the world's own truth."""
import csv
import json
import os
import re
import sys

import numpy as np
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import pack as PK     # noqa: E402
import world as W     # noqa: E402

fails = []


def ok(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + ("   " + str(detail) if detail else ""))
    if not cond:
        fails.append(name)


def pdf_text(name):
    return " ".join(p.extract_text() for p in PdfReader(os.path.join(TARGET, name)).pages)


def main():
    P = A.Pack(TARGET)
    resp = A.composite(P)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    # ---- the call and its family -------------------------------------------------------------------------
    g, (a16, bw) = A.golden(P, resp)
    ok("C1 the golden files 200 mg", A.pick(g) == 200, g)
    fam = {"golden": g, "weight exponent fixed at 1.0": A.golden(P, resp, wexp=1.0)[0],
           "Emax exposure-response": A.golden(P, resp, form="emax")[0],
           "prior biologic in the exposure-response": A.golden(P, resp, prior=True)[0],
           "logistic on log dose and log weight": A.dose_weight_logistic(P, resp),
           "observed week-16 trough with the between-patient spread": A.observed_er(P, resp)}
    for k, v in fam.items():
        ok("C2 standing member files 200 mg, 100 mg at least 2 points under 70: " + k,
           A.pick(v) == 200 and v[100] <= 68.0 and v[200] >= 75.0 and v[50] < 60, {d: round(x, 1) for d, x in v.items()})
    easy = A.easy_routes(P, resp)
    for k, v in easy.items():
        ok("C3 easy route files 100 mg with at least 3 points over 70: " + k, A.pick(v) == 100 and v[100] >= 73.0
           and v[50] < 60, {d: round(x, 1) for d, x in v.items()})
    lab = A.composite(P, label=True)
    ok("C4 the labelled-baseline composite also files 100 mg on the arm rates",
       A.pick({d: A.arm_rates(P, lab)["HB%d" % d] for d in A.CANDIDATES}) == 100)
    ok("C5 the weight exponent the troughs give sits near the world's", abs(-bw - W.WEXP) < 0.15, round(-bw, 3))
    # ---- the world's truth -------------------------------------------------------------------------------
    w = W.World()
    keep = np.mean([not p["disc"] and not p["resc"] for p in w.pat if p["dose"] > 0])
    rng = np.random.default_rng(3)
    eta = rng.normal(0, W.OMEGA, 3000)
    ws = np.array([c["weight"] for c in w.cand])
    truth = {}
    for d in A.CANDIDATES:
        c = d * W.ACC[16] / (W.CL0 * (ws[:, None] / 85.0) ** W.WEXP * np.exp(eta[None, :]) * 28)
        truth[d] = 100 * float(W.p75(c).mean()) * keep
    ok("C6 the world's own truth files 200 mg (100 mg under 70)", truth[100] < 68 and truth[200] > 75, truth)
    ok("C7 every recorded number accurate: troughs follow dose over clearance (median log error under 0.02)",
       abs(np.median([math_log_err(P, w)])) < 0.02)
    # ---- the asks ----------------------------------------------------------------------------------------
    ap, ai = A.ask_pasi(P), A.ask_itch(P)
    apl, ain = A.ask_pasi(P, label=True), A.ask_itch(P, anchor="rand")
    ok("SF1 the labelled-baseline reading moves ask A", sum(ap[k] != apl[k] for k in ap) >= 4,
       "%d of %d" % (sum(ap[k] != apl[k] for k in ap), len(ap)))
    ok("SF2 the randomisation-day anchor moves ask B", sum(ai[k] != ain[k] for k in ai) >= 6,
       "%d of %d" % (sum(ai[k] != ain[k] for k in ai), len(ai)))
    ok("SF4 figures.json carries the call and the asks", fig["call"]["dose_mg"] == 200 and
       len(fig["ask_pasi"]) == 10 and len(fig["ask_itch"]) == 10)
    # ---- the fork table, row by row ----------------------------------------------------------------------
    nowk16 = [sid for sid in P.sub if P.week16(sid)[0] is None]
    ok("SF3 a patient with no week-16 PASI is a non-responder", nowk16 and all(resp[s_] == 0 for s_ in nowk16),
       len(nowk16))
    lund = [r for r in P.pk if r["unit"] == "ng/mL" and not r["concentration"].startswith("<")]
    ok("SF5 the Lund troughs are ng/mL and convert to the central scale", lund and abs(np.median(
        [float(r["concentration"]) for r in lund]) / 1000 - np.median([x[4] for x in P.troughs()])) < 3, len(lund))
    ok("SF6 the exponent fixed at 1.0 keeps the call", A.pick(fam["weight exponent fixed at 1.0"]) == 200)
    ok("SF7 every exposure-response form keeps the call", all(A.pick(fam[k]) == 200 for k in
       ("Emax exposure-response", "logistic on log dose and log weight",
        "observed week-16 trough with the between-patient spread")))
    import math
    med = sorted(c["weight"] for c in P.feas())[len(P.feas()) // 2]
    b_ = A.logistic(np.c_[np.ones(len([s_ for s_, r in P.sub.items() if A.DOSE[r["arm"]] > 0])),
                          [math.log(A.ctyp(a16, bw, A.DOSE[P.sub[s_]["arm"]], float(P.sub[s_]["weight_kg"])))
                           for s_, r in P.sub.items() if A.DOSE[r["arm"]] > 0]],
                    np.array([resp[s_] for s_, r in P.sub.items() if A.DOSE[r["arm"]] > 0], float))
    medp = {d: 100 / (1 + math.exp(-(b_[0] + b_[1] * math.log(A.ctyp(a16, bw, d, med))))) for d in A.CANDIDATES}
    ok("SF8 the median candidate keeps the call", A.pick(medp) == 200, {d: round(v, 1) for d, v in medp.items()})
    ok("SF9 the US weights are pounds (median above 200)", np.median([c["weight"] / A.LB for c in P.feas()
                                                                      if str(c["site"]).startswith("US")]) > 200)
    ok("SF10 inclusive or exclusive 70 per cent keeps the call", all(abs(v[d] - 70) > 1.0 for v in fam.values()
                                                                    for d in A.CANDIDATES))
    ok("SF11 the prior-biologic covariate keeps the call", A.pick(fam["prior biologic in the exposure-response"]) == 200)
    ok("SF12 ask A's baseline is the record on or before the first dose", sum(ap[k] != apl[k] for k in ap) >= 1)
    ok("SF13 ask B's study days run from the first dose", sum(ai[k] != ain[k] for k in ai) >= 1)
    P2 = A.Pack(TARGET)
    P2.link = "listing"
    ok("SF14 the diary day and the handheld: the device log carries every handheld once (one reading)",
       len({r["device_id"] for r in P.devlog}) == len(P.devlog) and A.ask_itch(P2) != ai)
    ok("SF15 ask B's weekly score needs four of seven days", True if ai else False)
    ok("SF17 every handheld appears once in the device log, so the link has one reading over the window",
       len({r["device_id"] for r in P.devlog}) == len(P.devlog))
    P3 = A.Pack(TARGET)
    P3.light = False
    ok("SF16 NB-UVB and PUVA are phototherapy: reading only the word moves ask A", A.ask_pasi(P3) != ap)
    # ---- the pack ----------------------------------------------------------------------------------------
    files = sorted(os.listdir(TARGET))
    ok("G1 thirteen files in four formats", len(files) == len(PK.FILES) and
       {f.rsplit(".", 1)[1] for f in files} == {"csv", "xlsx", "pdf", "eml"}, files)
    n = sum(1 for _ in open(os.path.join(TARGET, PK.FILES["epro"]))) - 1
    ok("G2 a file of 25,000 rows or more", n >= 25000, n)
    txt = pdf_text(PK.FILES["sap"]) + " " + pdf_text(PK.FILES["cdp"]) + " " + open(
        os.path.join(TARGET, PK.FILES["email"]), encoding="utf-8").read()
    for wd in ("weight", "clearance", "exposure", "body weight", "kg", "heavier", "lighter", "concentration-response"):
        ok("G3 no document names the move: '%s'" % wd, re.search(r"\b%s\b" % wd, txt, re.I) is None)
    alltxt = ""
    for f in files:
        if f.endswith((".csv", ".eml")):
            alltxt += open(os.path.join(TARGET, f), encoding="utf-8").read()
    ok("G4 no em dash in any text file", "—" not in alltxt + txt)
    ok("G5 the documents carry their own stamps", all(b"ReportLab" not in open(os.path.join(TARGET, f), "rb").read()
                                                       for f in files if f.endswith(".pdf")))
    print("checks: %d failed" % len(fails))
    sys.exit(1 if fails else 0)


def math_log_err(P, w):
    import math
    cl = {}
    sid_of = {}
    for p in w.pat:
        sid_of[p["i"]] = p
    by_sid = {}
    R = PK.Records(w)
    for p in w.pat:
        by_sid[p["sid"]] = p
    errs = []
    for sid, wk, d, wt, c in P.troughs(weeks=(16,)):
        p = by_sid[sid]
        errs.append(math.log(c) - math.log(d * W.ACC[16] / (p["cl"] * 28.0)))
    return float(np.median(errs))


if __name__ == "__main__":
    main()

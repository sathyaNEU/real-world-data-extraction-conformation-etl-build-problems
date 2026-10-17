"""task242 checks: the three rules executed on the simulator's clean truth (R1 to R3c), every semantic fork row (SF1 to
SF14), the rungs and the corridor of reasonable implementations, every Layer 1 slip against the call, the ask devices
and their stops, the separation of the call from the devices, the documents' pins, the input gates and the realism
sweep."""
import os
import re

import numpy as np
import pandas as pd

import estim as E
import params as P
import sim as S

N = [0]
GOLD = ["Melmangalam", "Vadakkupatti", "Velliyanur", "Chinnakulam", "Periyamalai", "Sengalur"]


def ok(cond, label):
    assert cond, label
    N[0] += 1


def _pdf_text(path):
    from pypdf import PdfReader
    return " ".join(" ".join(pg.extract_text().split()) for pg in PdfReader(path).pages)


def _docx_text(path):
    import docx
    d = docx.Document(path)
    return " ".join([p.text for p in d.paragraphs] + [c.text for t in d.tables for row in t.rows for c in row.cells])


def _xlsx_text(path):
    from openpyxl import load_workbook
    wb = load_workbook(path, data_only=True)
    return " ".join(str(c) for ws in wb.worksheets for row in ws.iter_rows(values_only=True) for c in row if c is not None)


def _text(path):
    if path.endswith(".pdf"):
        return _pdf_text(path)
    if path.endswith(".docx"):
        return _docx_text(path)
    if path.endswith(".xlsx"):
        return _xlsx_text(path)
    return open(path, encoding="utf-8").read()


def flags_of(out):
    return [z for z in E.ZONES if out[z]["flag"]]


# ------------------------------------------------------------------ the clean truth
def truth(W, R):
    """each zone's tested residents on the clean truth: the expected reactive share, the share infected by each
    resident's collection day, the assay's true sensitivity for those infections, and the specificity"""
    t = R.res
    out = {}
    for k, z in enumerate(E.ZONES):
        x = t[t["zone_k"] == k]
        cum = np.cumsum(W["zones"][k]["curve"])
        days = S.DAYS
        A, se = [], []
        for d in x["collected_day"].astype(int):
            w = W["zones"][k]["curve"] * (days < d)
            A.append(float(cum[d - S.LO - 1]))
            se.append(float(np.sum(w * S.se_true(d - days)) / w.sum()))
        A, se = np.array(A), np.array(se)
        p = float(np.mean(A * se + (1 - A) * (1 - P.SP)))
        out[z] = dict(p=p, A=float(A.mean()), se=float(np.sum(A * se) / A.sum()))
    return out


def panel_design_se():
    """the sensitivity a pooled panel of this design measures on the clean truth"""
    num = den = 0.0
    for day, spread, n in P.PANEL_VISITS:
        num += n * float(np.mean([float(S.se_true(day + j)[0]) for j in range(-spread, spread + 1)]))
        den += n
    return num / den


def run(target, golden, o, X, A):
    W, R = o["W"], o["R"]
    D = X["D"]
    F = {k: v for k, v in __import__("build").FILES.items()}
    g = X["golden"]
    ok(flags_of(g) == GOLD, "golden: six zones flagged (%s)" % flags_of(g))

    # ---------------------------------------------------------------- the truth behind the golden
    T = truth(W, R)
    true_flags = [z for z in E.ZONES if T[z]["A"] / T[z]["p"] > P.TOL_HIGH or T[z]["A"] / T[z]["p"] < P.TOL_LOW]
    ok(true_flags == GOLD, "truth: the six zones' expected IgM share stands for under two thirds of the share infected "
       "(%s)" % true_flags)
    ok(min(T[z]["A"] / T[z]["p"] for z in GOLD) > 1.8 and max(T[z]["A"] / T[z]["p"] for z in E.ZONES if z not in GOLD) < 1.36,
       "truth margins: flagged zones above 1.8 times, the rest under 1.36 (%.2f, %.2f)"
       % (min(T[z]["A"] / T[z]["p"] for z in GOLD), max(T[z]["A"] / T[z]["p"] for z in E.ZONES if z not in GOLD)))
    tr = {z: float(np.mean(R.res[R.res["zone_k"] == k]["infected"])) for k, z in enumerate(E.ZONES)}
    ok(all(abs(g[z]["A"] - tr[z]) < 0.06 for z in E.ZONES), "the golden estimates sit within sampling error of the share "
       "of tested residents actually infected since 1 January (max %.3f)" % max(abs(g[z]["A"] - tr[z]) for z in E.ZONES))

    # ---------------------------------------------------------------- R1: the field's raw material ships, nothing derived
    for f in os.listdir(target):
        if f.endswith(".csv"):
            cols = pd.read_csv(os.path.join(target, f), nrows=1).columns
            ok(not any(re.search(r"sensitiv|effective|attack|infected|days_since|lag|weight|window|corrected|estimate",
                                 c, re.I) for c in cols), "R1 %s carries no derived column (%s)" % (f, list(cols)))

    # ---------------------------------------------------------------- R2: the default path on the cut pack
    for r in ("pooled", "from5", "kit"):
        ok(flags_of(X[r]) == [], "R2 one sensitivity from the panel (%s) flags no zone" % r)
        ok(max(X[r][z]["ratio"] for z in E.ZONES) < 1.42, "R2 %s keeps every zone under 1.42 times (%.2f)"
           % (r, max(X[r][z]["ratio"] for z in E.ZONES)))

    # ---------------------------------------------------------------- R3: the analyst test on the clean truth
    se1 = panel_design_se()
    easy = {z: E.rogan_gladen(T[z]["p"], se1, P.SP) / T[z]["p"] for z in E.ZONES}
    ok(all(TOL_LOW_OK(v) for v in easy.values()), "R3a the easy route on the clean truth (the panel's pooled sensitivity "
       "%.3f for every zone, the true specificity) flags no zone (max %.2f)" % (se1, max(easy.values())))
    dec = {z: E.rogan_gladen(T[z]["p"], T[z]["se"], P.SP) / T[z]["p"] for z in E.ZONES}
    ok([z for z in E.ZONES if dec[z] > P.TOL_HIGH or dec[z] < P.TOL_LOW] == GOLD, "R3b the decisive step alone (each "
       "zone's sensitivity from its own epidemic timing) gives the six on the clean truth")
    kit_true = float(np.mean([float(S.se_true(d)[0]) for d in range(5, 61)]))
    ok(all(TOL_LOW_OK(E.rogan_gladen(T[z]["p"], kit_true, P.SP) / T[z]["p"]) for z in E.ZONES),
       "R3a the kit window's sensitivity on the clean truth (%.3f) flags no zone" % kit_true)

    # ---------------------------------------------------------------- R3c: no plant, no method filed
    for k in ("request", "register", "standard", "bulletin", "panelnote", "protocol", "vcsop", "readme", "dict"):
        txt = _text(os.path.join(target, F[k]))
        ok(not re.search(r"sensitivity|specificity|days since onset|epidemic curve|convol|weighted by|timing|window of",
                         txt, re.I), "R3c %s names no sensitivity, timing or method" % F[k])
        ok(not re.search(r"\b0\.\d{2,3}\b.*(?:sensitiv|specific)", txt, re.I), "R3c %s files no accuracy figure" % F[k])
    reg = _text(os.path.join(target, F["register"]))
    ok("between 1 January 2027 and the collection of their survey specimen" in reg and
       "aged one year and over" in reg, "R3c the register files SERO-D1's estimand (population, outcome, window)")
    sop = _text(os.path.join(target, F["standard"]))
    ok(re.search(r"more than one and a half times the published value or less than two thirds of it", sop) and
       "misclassification as the testing laboratory has measured it" in sop, "R3c SOP-EPI-07 files the M flag's "
       "comparison and tolerance, and the source of the test's accuracy, not a method")

    # ---------------------------------------------------------------- the rungs (each a distinct wrong set)
    for r in ("city", "peak", "median", "mean", "w60", "w90"):
        ok(flags_of(X[r]) != GOLD, "rung %s files another set (%s)" % (r, flags_of(X[r])))
    ok(set(flags_of(X["median"])) < set(GOLD) and {"Vadakkupatti", "Sengalur"} <= set(GOLD) - set(flags_of(X["median"])),
       "the median-day rung misses the two-wave zones")
    ok("Velliyanur" not in flags_of(X["w90"]), "the 90-day window misses Velliyanur's short August outbreak")
    ok("Puthanpalli" in flags_of(X["w60"]), "the 60-day window flags Puthanpalli, whose August wave sits just past it")
    ok("Kottaivayal" in flags_of(X["mean"]), "the mean-day rung flags Kottaivayal, whose January wave drags the mean")

    # ---------------------------------------------------------------- the corridor of reasonable implementations (C1, C3)
    import writeup as WU
    for n, kw in WU.LEGIT.items():
        v = E.call(D, "variant", **kw)
        ok(flags_of(v) == GOLD, "C1 %s flags the same six" % n)
        dev = max(abs(v[z]["A"] / g[z]["A"] - 1) for z in E.ZONES)
        ok(dev < WU.BAND, "C3 %s moves no estimated share by %d per cent or more (%.3f)" % (n, 100 * WU.BAND, dev))
        ok(min(v[z]["ratio"] for z in GOLD) > 1.7 and max(v[z]["ratio"] for z in E.ZONES if z not in GOLD) < 1.36,
           "C4 %s keeps the margins (flagged above 1.7, the rest under 1.36)" % n)
    for z in GOLD:
        for r in ("pooled", "from5", "kit"):
            ok(abs(X[r][z]["A"] / g[z]["A"] - 1) > WU.BAND, "the easy route's estimate for %s falls outside the band (%s)"
               % (z, r))

    # ---------------------------------------------------------------- semantic fork rows
    ok(flags_of(E.call(D, "variant", dedup=True)) == GOLD, "SF1 repeat notifications dropped or kept: same call")
    c2 = D["cases"].copy()
    official = c2["zone"].isin(E.ZONES)
    Dz = dict(D, cases=c2[official])
    ok(flags_of(E.call(Dz, "golden")) == GOLD, "SF2 only the official zone spellings kept (%d rows dropped): same call"
       % int((~official).sum()))
    ok(flags_of(E.call(D, "variant", cls="CONFIRMED")) == GOLD, "SF3 cases: confirmed only or with probable: same call")
    ok(flags_of(E.call(D, "variant", basis="notified")) == GOLD, "SF4 notification date in place of onset date: same call")
    ok(flags_of(E.call(D, "variant", timing="midpoint")) == GOLD, "SF5 each zone read at its middle fieldwork day: same "
       "call")
    r = D["results"]
    ok(int(r["age_yrs"].min()) >= 1, "SF6 residents aged one year and over: every tested resident is (converge)")
    pub = E.published(D)
    for z in E.ZONES:
        n, a = pub[z]
        p1 = round(100 * a / n, 1) / 100
        rr = E.rogan_gladen(p1, g[z]["se"], X["sp"]) / p1
        ok((rr > P.TOL_HIGH) == (z in GOLD), "SF7 %s: the bulletin's rounded share in place of reactive over tested: same "
           "flag" % z)
    ok(all(abs(g[z]["ratio"] - P.TOL_HIGH) > 0.15 and abs(g[z]["ratio"] - P.TOL_LOW) > 0.15 for z in E.ZONES),
       "SF8 more than or at least 1.5 (or two thirds): no multiple within 0.15 of either limit")
    pn = D["panel"].copy()
    first = pn.copy()
    first["result_final"] = np.where(first["reading_first"] == "REACTIVE", "REACTIVE", "NON-REACTIVE")
    ok(flags_of(E.call(dict(D, panel=first), "golden")) == GOLD, "SF9 the panel's first readings, grey zone as "
       "non-reactive: same call")
    donors = pn[(pn["arm"] == "CONFIRMED CASE") | pn["confirmed_by"].str.startswith("Blood donor")]
    ok(flags_of(E.call(dict(D, panel=donors), "golden")) == GOLD, "SF10 specificity from the blood donors alone: same call")
    febrile = pn[(pn["arm"] == "CONFIRMED CASE") | ~pn["confirmed_by"].str.startswith("Blood donor")]
    ok(flags_of(E.call(dict(D, panel=febrile), "golden")) == GOLD, "SF11 specificity from the febrile controls alone: "
       "same call")
    c3 = E.resident_cases(D)
    ok(int((c3["onset"] < E.YEAR0).sum()) > 0, "SF12 the line list carries the 2026 season's tail")
    wide = window_from_october(D, X["sp"])
    ok(flags_of(wide) != GOLD and "between 1 January 2027 and the collection of their survey specimen" in
       _text(os.path.join(target, F["register"])), "SF12 the curve opened to October 2026 estimates another quantity "
       "(%s); ruled out by the register's window" % flags_of(wide))
    ok(all(abs(g[z]["A"] * 100 - round(g[z]["A"] * 100, 1)) <= 0.05 for z in E.ZONES), "SF13 shares in per cent")
    ok(all(g[z]["A"] > 0 for z in E.ZONES), "SF14 every estimate positive (no zone's reactive share below the false "
       "positive rate)")
    no_sp = E.call(D, "golden", sp=1.0)
    ok(flags_of(no_sp) != GOLD and "misclassification as the testing laboratory has measured it" in sop and
       len(D["panel"][D["panel"]["arm"] == "NEGATIVE CONTROL"]) == 300, "SF15 sensitivity alone (specificity 1) flags "
       "another set (%s); ruled out by SOP-EPI-07, the laboratory having measured specificity on its controls"
       % flags_of(no_sp))

    # ---------------------------------------------------------------- maturity: every onset before fieldwork closed is notified
    cc = D["cases"]
    delay = (pd.to_datetime(cc["notified_on"], format="%d-%m-%Y") - pd.to_datetime(cc["onset_date"], format="%d-%m-%Y")).dt.days
    ok(int(delay.max()) < 31 and int(delay.min()) >= 1, "axis 12: notification delays run 1 to %d days, so every onset "
       "before 7 December is in the 8 January extract" % int(delay.max()))

    # ---------------------------------------------------------------- Layer 1 slips leave the call
    c4 = D["cases"].copy()
    c4["zone"] = c4["zone"].where(~c4["zone"].str.startswith("Non-resident"), "Kadalur")
    ok(flags_of(E.call(dict(D, cases=c4), "golden")) == GOLD, "L1 non-residents read as residents of one zone: same call")
    c5 = D["cases"].copy()
    c5["onset_date"] = c5["notified_on"]
    ok(flags_of(E.call(dict(D, cases=c5), "golden")) == GOLD, "L1 every onset read off the notification date: same call")

    # ---------------------------------------------------------------- separation: the ask devices sit outside the call
    Dcall = {k: D[k] for k in ("cases", "results", "panel")}
    ok(flags_of(E.call(Dcall, "golden")) == GOLD, "separation: the call reads only the line list, the results and the "
       "panel")
    ok(set(D["results"]["specimen_id"]) <= set(D["lab"][D["lab"]["condition"] == "ACCEPTED"]["barcode"]),
       "separation: every tested resident's specimen is an accepted one; no rejected specimen is a result row")
    ok(len(D["results"]) == int((D["lab"]["condition"] == "ACCEPTED").sum()), "separation: one result per accepted "
       "specimen")

    # ---------------------------------------------------------------- ask A: the Breteau index
    bi = X["breteau"]
    ok(all(abs(bi[z] - E.breteau(D, zone_from="dated")[z]) < 1e-9 for z in E.ZONES), "ask A: the ward map in force on "
       "each form's date and the premise's assessment number give the same zones")
    for zf, keep in [("ward", "inspected"), ("ward", "first"), ("ward", "last"), ("ward", "all"), ("premise", "first"),
                     ("premise", "last"), ("premise", "all"), ("dated", "first"), ("dated", "all")]:
        b = E.breteau(D, zone_from=zf, keep=keep)
        ok(all(round(b[z], 1) != round(bi[z], 1) for z in E.ZONES), "ask A stop %s/%s misses every zone (min %.2f)"
           % (zf, keep, min(abs(b[z] - bi[z]) for z in E.ZONES)))
    ins = D["insp"].drop_duplicates()
    early = ins[ins["inspected_on"] < "2027-11-16"]
    zp = early["premise_id"].str.slice(0, 2).astype(int) - 1
    wm = D["wards"]
    wz = early["ward_no"].map(dict(zip(wm["ward_no"].astype(int), wm["zone"]))).map(E.ZONES.index)
    ok(all(((zp == k) & (wz != k)).sum() > 20 for k in range(12)), "ask A: every zone has forms before 16 November "
       "whose ward number lands in another zone on the ward master")
    for k, z in enumerate(E.ZONES):
        x = ins[ins["premise_id"].str.startswith("%02d/" % (k + 1))]
        ok((x["remarks"].fillna("") == "LOCKED").sum() > 0 and x["premise_id"].duplicated().sum() > 0,
           "ask A: %s has locked calls and repeat forms" % z)
    ok(all(abs(abs(bi[z] * 10 - round(bi[z] * 10)) - 0.5) > 0.02 for z in E.ZONES), "ask A: no index within 0.002 of a rounding edge")

    # ---------------------------------------------------------------- ask B: the household response rate
    rr = X["response"]
    for num, den in [("results", "sample"), ("outcome", "sample"), ("lab", "visits"), ("results", "visits"),
                     ("outcome", "visits")]:
        b = E.response(D, numerator=num, denominator=den)
        ok(all(round(b[z], 1) != round(rr[z], 1) for z in E.ZONES), "ask B stop %s/%s misses every zone (min %.2f)"
           % (num, den, min(abs(b[z] - rr[z]) for z in E.ZONES)))
    labhh = set(D["lab"]["barcode"].str.slice(3, 9))
    reshh = set(D["results"]["household_id"])
    vv = D["visits"].drop_duplicates(["household_id", "start"]).sort_values(["household_id", "start"])
    last = vv.groupby("household_id")["visit_outcome"].last()
    for z in E.ZONES:
        hh = set(D["sample"][D["sample"]["zone"] == z]["household_id"])
        ok(len((labhh - reshh) & hh) >= 1, "ask B: %s has a household whose every specimen the laboratory rejected" % z)
        ok(len((set(last[last == 1].index) - labhh) & hh) >= 1, "ask B: %s has a completed interview with no specimen" % z)
        ok(len(hh - set(last.index)) >= 1, "ask B: %s has a sampled household never called on" % z)
    ok(all(abs(abs(rr[z] * 10 - round(rr[z] * 10)) - 0.5) > 0.02 for z in E.ZONES), "ask B: no rate within 0.002 of a rounding edge")
    ok(int(D["visits"].duplicated(subset=[c for c in D["visits"].columns if not c.startswith("_")]).sum()) > 20,
       "ask B: submissions sent twice from the tablet (hazard)")

    # ---------------------------------------------------------------- the documents' pins
    prot = _text(os.path.join(target, F["protocol"]))
    ok("the share of sampled households, other than those the field team found vacant or not a dwelling, in which at "
       "least one member gave a blood specimen" in prot, "the protocol files the household response rate")
    vc = _text(os.path.join(target, F["vcsop"]))
    ok("Positive containers per 100 houses inspected" in vc and "A locked call and a follow-up visit are not round "
       "inspections" in vc, "SOP-VC-02 files the Breteau index and what counts as the round's inspection")
    ok(not re.search(r"renumber|delimitation|16 November|former ward", vc + prot + _text(os.path.join(target, F["request"])),
                     re.I), "nothing narrates the ward renumbering on the ask's path")
    bul = _text(os.path.join(target, F["bulletin"]))
    for z in E.ZONES:
        n, a = pub[z]
        ok(re.search(r"%s %s.*?%s %d %.1f" % (E.ROMAN[E.ZONES.index(z)], z, "{:,}".format(n), a, 100.0 * a / n), bul),
           "the bulletin's Table 1 row for %s is the results file's" % z)

    # ---------------------------------------------------------------- input gates and realism
    files = sorted(os.listdir(target))
    ok(len(files) >= 10 and len({f.rsplit(".", 1)[1] for f in files}) >= 3, "input gates: files and formats")
    big = max(sum(1 for _ in open(os.path.join(target, f))) for f in files if f.endswith(".csv"))
    ok(big - 1 >= 25000, "input gates: a table of 25,000 rows or more (%d)" % (big - 1))
    import build as B
    for k in B.DISTRACTORS:
        ok(os.path.exists(os.path.join(target, B.FILES[k])), "distractor %s ships" % B.FILES[k])
    src = open(os.path.join(os.path.dirname(__file__), "estim.py")).read()
    ok(not any(B.FILES[k] in src or ('"%s"' % k) in src for k in B.DISTRACTORS), "no estimator reads a distractor")
    for f in files:
        p = os.path.join(target, f)
        txt = _text(p) if f.rsplit(".", 1)[1] in ("pdf", "docx", "xlsx") else open(p, encoding="utf-8").read()
        ok("—" not in txt and "–" not in txt, "no em or en dash in %s" % f)
        ok(not re.search(r"\b(leverage|robust|comprehensive|seamless|delve|furthermore)\b", txt, re.I),
           "no LLM tell in %s" % f)
    return N[0]


def window_from_october(D, sp):
    """the call with the curve's window opened to the line list's first day (1 October 2026)"""
    base = pd.Timestamp("2026-10-01")
    se = E.se_curve(D, "visits")
    cases = E.resident_cases(D)
    r = E.zone_results(D)
    pub = E.published(D)
    out = {}
    for z in E.ZONES:
        x = cases[cases["z"] == z]
        n = np.bincount(((x["t"] - base).dt.days).values, minlength=500).astype(float)
        days = np.arange(n.size)
        cd = ((r[r["zone"] == z]["collected"] - base).dt.days).values
        s = float(np.mean([np.sum(n * (days < d) * se(d - days)) / np.sum(n * (days < d)) for d in cd]))
        nn, a = pub[z]
        p = a / nn
        A = E.rogan_gladen(p, s, sp)
        out[z] = dict(A=A, ratio=A / p, flag=bool(A / p > P.TOL_HIGH or A / p < P.TOL_LOW))
    return out


def TOL_LOW_OK(v):
    return P.TOL_LOW <= v <= P.TOL_HIGH

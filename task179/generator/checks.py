"""The generator's assertions on the cut pack and on the clean world (dataset-generation section 7, determinism-check
section 4). Every rung, fork row, ask figure, hazard and input gate the design note names is asserted here.

    python3 task179/generator/checks.py
"""
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc                # noqa: E402
import core as C           # noqa: E402
import world as W          # noqa: E402
import records             # noqa: E402
import pack as PK          # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
LO, HI = 4500, 5500
RESULTS = []


def check(cid, ok, detail):
    RESULTS.append((cid, bool(ok), detail))
    print("%-4s  %-6s %s" % ("PASS" if ok else "FAIL", cid, detail))


def thousand(v):
    return int(round(v, -3))


def in_bin(v):
    return LO <= v < HI


def edge_gap(v):
    return min(abs(v - LO), abs(HI - v)) / v


def margin(v, unit=0.1):
    return unit / 2 - abs(v - round(v / unit) * unit)


def r1(v):
    return float("%.1f" % (v + 1e-9))


def proj_total(daily, last, R, w, by_case=False):
    if not by_case:
        x = C.project(daily, last, R, w, calc.CUT, calc.day(calc.CUT_FROM), calc.day(calc.WIN1))
    else:
        x = list(map(float, daily[:last + 1]))
        for t in range(last + 1, calc.day(calc.WIN1) + 1):
            lam = sum(w[s - 1] * R * x[t - s] for s in range(1, min(C.L, t) + 1))
            x.append(lam * (calc.CUT if t >= calc.day(calc.CUT_FROM) else 1.0))
        x = np.array(x)
    return float(x[calc.day(calc.WIN0):calc.day(calc.WIN1) + 1].sum())


def clean_truth():
    """The clean world before any Layer 1 handling: every case with its true onset and source, the links the tracing
    system holds (linked, case ill by 11 October), no duplicate numbers, no non-cases."""
    cases, _ = records.build(W.SEED)
    T = W.COMPLETE_LAST
    on = dict(zip(cases["true_id"], cases["onset"]))
    pi, pj = [], []
    for t, s, lk in zip(cases["true_id"], cases["src"], cases["linked"]):
        if lk and s in on and on[t] <= T and on[t] - on[s] >= 1:
            pi.append(on[s])
            pj.append(on[t])
    pi, pj = np.array(pi), np.array(pj)
    daily = np.bincount(cases["onset"][cases["onset"] <= T], minlength=T + 1).astype(float)
    return pi, pj, pj - pi, daily, T


def main_call_checks(F):
    g = calc.the_call()
    check("R1", thousand(g["total"]) == F["call"]["cases_w49_52"] == 5000,
          "golden %.0f cases (bin %d), R %.3f, mean interval %.2f days, %d pairs" % (g["total"], thousand(g["total"]),
                                                                                  g["R"], g["mean_si"], g["n_pairs"]))
    check("R1b", int(round(g["mean_si"])) == F["components"]["serial_interval_days"] and r1(g["R"]) == F["components"]["R"],
          "components %d days, R %.1f agree with figures.json" % (round(g["mean_si"]), r1(g["R"])))
    d = calc.the_call(gi="naive_gamma")
    e = calc.the_call(gi="naive_empirical")
    check("R2", thousand(d["total"]) == thousand(e["total"]) == F["rivals"]["register_cases_w49_52"] == 4000,
          "default path: every pair as it stands, gamma %.0f, empirical %.0f (4,000)" % (d["total"], e["total"]))
    v = calc.variant("naive_drop_last14")
    check("R2b", thousand(v[0]) == 4000, "hygiene reflex, pairs whose case fell ill in the last 14 days dropped: %.0f" % v[0])
    fam = {}
    for gi in ("trunc_weibull", "npmle", "complete_50", "complete_60"):
        fam[gi] = calc.the_call(gi=gi)["total"]
    gaps = {k: edge_gap(v) for k, v in fam.items()}
    check("G1", all(in_bin(v) for v in fam.values()) and min(gaps.values()) >= 0.05 and edge_gap(g["total"]) >= 0.05,
          "golden family in [4,500, 5,500): %s; nearest edge %.1f per cent (golden %.1f)" % (
              ", ".join("%s %.0f" % kv for kv in fam.items()), 100 * min(gaps.values()), 100 * edge_gap(g["total"])))
    return g, d


def clean_truth_checks():
    pi, pj, lags, daily, T = clean_truth()
    b0 = W.BASE_FIRST
    r = C.growth_rate(daily, b0, T)
    w_true = W.simulate(W.SEED)["w"]
    truth = proj_total(daily, T, C.R_from_growth(r, w_true), w_true)
    wn = C.empirical(lags)
    wt, _ = C.fit_lags(lags, pi, T, "gamma", True)
    keep = pj <= T - 14
    wd = C.empirical(lags[keep])
    a = proj_total(daily, T, C.R_from_growth(r, wn), wn)
    b = proj_total(daily, T, C.R_from_growth(r, wd), wd)
    c = proj_total(daily, T, C.R_from_growth(r, wt), wt)
    check("R3a", thousand(a) == 4000 and thousand(truth) == 5000,
          "clean truth: every pair as it stands %.0f (4,000) against the true interval's %.0f (5,000)" % (a, truth))
    check("R3b", thousand(b) == 4000, "clean truth: the fortnight's pairs dropped on the case's clock %.0f (4,000)" % b)
    check("R3c", thousand(c) == 5000 and abs(C.mean_of(wt) - W.SI_MEAN) < 0.6,
          "clean truth: each pair read against its source's horizon %.0f (5,000), mean %.2f against the true %.1f" % (
              c, C.mean_of(wt), W.SI_MEAN))


def fork_checks():
    ll, ch = calc.load()
    c, alias = calc.cases_table(ll)
    T = calc.day(calc.COMPLETE)
    out = {}
    v = calc.variant("no_dedup")[0]
    v2 = calc.variant("with_noncases")[0]
    check("SF1", thousand(v) == thousand(v2) == 5000 and len(alias) > 0,
          "%d case numbers duplicated by sample; both kept %.0f, Not a case kept %.0f" % (len(alias), v, v2))
    v = calc.variant("trunc_at_extract")[0]
    check("SF2", thousand(v) == 5000, "pairs and truncation at the 18 October extract %.0f" % v)
    a = calc.the_call(growth="poisson_daily")["total"]
    b = calc.the_call(growth="ols_weekly")["total"]
    check("SF3", thousand(a) == thousand(b) == 5000, "growth by Poisson regression %.0f, on weekly counts %.0f" % (a, b))
    pi, pj, lags = calc.pairs(c, ch, alias, T)
    w, _ = C.fit_lags(lags, pi, T, "gamma", True)
    daily = calc.daily_counts(c, T)
    r = C.growth_rate(daily, calc.day(calc.BASE0), T)
    Rr = C.R_renewal_ratio(daily, w, calc.day(calc.BASE0), T)
    rr = proj_total(daily, T, Rr, w)
    check("SF4", thousand(rr) != 5000 and _pdf_has(PK.F_PN, "exponential growth rate"),
          "the renewal ratio (R %.3f) gives %.0f, not the filed basis; the planning note files the growth rate" % (Rr, rr))
    bc = proj_total(daily, T, C.R_from_growth(r, w), w, by_case=True)
    check("SF5", thousand(bc) != 5000 and _pdf_has(PK.F_PN, "causes half as many new cases"),
          "halving by the case's own onset gives %.0f, not the filed scenario (every source from 2 November)" % bc)
    v = calc.variant("drop_low")[0]
    check("SF6", thousand(v) == 5000, "Low certainty links dropped %.0f" % v)
    fits = {fam: C.fit_lags(lags, pi, T, fam, True) for fam in ("gamma", "weibull", "lognorm")}
    ln = calc.the_call(gi="trunc_lognorm")["total"]
    check("SF7", thousand(ln) == 5000 and fits["lognorm"][1] - fits["gamma"][1] > 20,
          "lognormal %.0f, its negative log-likelihood %.1f worse than the gamma's; Weibull %.1f worse" % (
              ln, fits["lognorm"][1] - fits["gamma"][1], fits["weibull"][1] - fits["gamma"][1]))
    check("SF8", calc.WIN0 == dt.date(2026, 11, 30) and calc.WIN1 == dt.date(2026, 12, 27)
          and calc.WIN0.isocalendar()[1] == 49 and calc.WIN1.isocalendar()[1] == 52,
          "window 30 November to 27 December, ISO weeks 49 to 52")
    g = calc.the_call()["total"]
    check("SF9", abs(g - round(g, -3)) < 450, "unrounded %.0f rounds to %d with %.0f cases to spare" % (
        g, thousand(g), 500 - abs(g - round(g, -3))))
    E = calc.day(dt.date(2026, 10, 18))
    d2 = calc.daily_counts(c, E)
    p18 = proj_total(d2, E, C.R_from_growth(r, w), w)
    check("SF10", thousand(p18) != 5000 and _pdf_has(PK.F_PN, "onsets to Sunday 11 October are complete"),
          "onsets of 12 to 18 October read as complete give %.0f, not the filed record (complete to 11 October)" % p18)
    lag0 = int((lags < 1).sum())
    check("SF10b", lag0 == 0, "pairs with a lag under one day: %d" % lag0)
    # the data separate the readings: the mean interval by the month the source fell ill
    means = []
    for m in (8, 9, 10):
        s, e = calc.day(dt.date(2026, m, 1)), calc.day(dt.date(2026, m + 1, 1))
        k = (pi >= s) & (pi < e)
        means.append((m, int(k.sum()), float(lags[k].mean())))
    check("D1", means[0][2] > means[1][2] > means[2][2] and abs(means[0][2] - 13.5) < 0.05 and abs(means[1][2] - 11.0) < 0.05,
          "mean interval by source month: %s" % ", ".join("%d: %d pairs %.2f days" % x for x in means))
    return out


def bootstrap_check(n=60):
    ll, ch = calc.load()
    c, alias = calc.cases_table(ll)
    T = calc.day(calc.COMPLETE)
    pi, pj, lags = calc.pairs(c, ch, alias, T)
    daily = calc.daily_counts(c, T)
    r = C.growth_rate(daily, calc.day(calc.BASE0), T)
    rng = np.random.default_rng(179)
    tot = []
    for _ in range(n):
        k = rng.integers(0, len(lags), len(lags))
        w, _ = C.fit_lags(lags[k], pi[k], T, "gamma", True)
        tot.append(proj_total(daily, T, C.R_from_growth(r, w), w))
    tot = np.array(tot)
    share = float(np.mean([in_bin(v) for v in tot]))
    check("B1", share >= 0.9, "pairs bootstrap, %d draws: sd %.1f per cent of the golden, %.0f per cent in the bin" % (
        n, 100 * tot.std() / np.mean(tot), 100 * share))


def ask_checks(F):
    con = calc.ask_contacts()
    lab = calc.ask_lab()
    ok = all(F["a1_%s" % z]["people"] == n and F["a1_%s" % z]["pct_completed"] == r1(s) for z, (n, s) in con.items())
    ok = ok and all(F["a2_w%d" % w]["mean_hours"] == r1(m) and F["a2_w%d" % w]["pct_within_24h"] == r1(s)
                    for w, (m, s, n) in lab.items())
    check("A0", ok, "the sixteen ask figures recompute from target/ and agree with figures.json")
    mc = min(margin(s) for n, s in con.values())
    ml = min(min(margin(m), margin(s)) for m, s, n in lab.values())
    check("A0b", mc >= 0.02 and ml >= 0.02, "every percentage and mean a fifth of a rounding step from its edge (%.3f, %.3f)" % (mc, ml))
    routes = {"exact": calc.ask_contacts(mode="exact"), "loose": calc.ask_contacts(mode="loose"),
              "ids": calc.ask_contacts(mode="ids"), "per_listing": calc.ask_contacts(mode="exact", per_record=True)}
    sep = all(routes[k][z][0] != con[z][0] and r1(routes[k][z][1]) != r1(con[z][1]) for k in routes for z in con)
    check("A1", sep, "contacts: the exact key, the key without age, the listing id and per-listing completion each miss "
                     "every district's people and percentage")
    # completion read on any listing instead of the last-ending follow-up
    rg = calc.load_contacts()
    rg = rg.assign(pid=calc.person_ids(rg))
    diff = 0
    for z in calc.ASK_ZONES:
        sub = rg[rg["district"] == z]
        first = sub.groupby("pid")["date_listed"].min()
        ppl = first[(first >= calc.WK37) & (first <= calc.WK39_END)].index
        s2 = sub[sub["pid"].isin(set(ppl))]
        anyc = 100 * s2.groupby("pid")["status"].apply(lambda v: (v == "Follow-up completed").any()).mean()
        diff += r1(anyc) != r1(con[z][1])
    check("A2", diff >= 1 and _pdf_has(PK.F_PN, "ends last for them"),
          "completion on any listing differs in %d of 4 districts; the planning note files the last-ending follow-up" % diff)
    dup = rg[rg["follow_up_team"] == "PHD"]
    paired = sum(1 for a, b in zip(calc.person_ids(rg, "exact"), rg["pid"]) if a != b)
    check("A3", paired > 100, "%d paper listings joined to a tablet listing of the same person with the age off" % paired)
    nos = calc.ask_lab(shift_h=0.0)
    fst = calc.ask_lab(final="first")
    check("B1a", all(r1(nos[w][0]) != r1(lab[w][0]) and r1(nos[w][1]) != r1(lab[w][1]) for w in lab),
          "laboratory: the analyser clock read as local misses every week's mean and share")
    check("B2", any(r1(fst[w][0]) != r1(lab[w][0]) for w in lab), "the first result instead of the re-run moves the mean")
    df = calc.load_mobile_lab()
    run = calc.cartridge_run_minutes()
    gap = np.array([(a - b).total_seconds() / 60 for a, b in zip(df["res"], df["rec"])])
    early = float(np.mean(gap < run))
    early_shift = float(np.mean(gap + 60 < run))
    check("B3", 0.01 < early < 0.05 and early_shift == 0.0,
          "results under the %d-minute run after reception: %.1f per cent on the file's clock, %.1f once on local time" % (
              run, 100 * early, 100 * early_shift))
    ll, _ = calc.load()
    pos = df[(df["Result"] == "Positive")]
    lr = dict(zip(ll["sample_id"], ll["lab_result_date"]))
    mism = sum(1 for s, t in zip(pos["Sample no."], pos["res"]) if s in lr and lr[s] and lr[s] != t.strftime("%d/%m/%Y"))
    mism2 = sum(1 for s, t in zip(pos["Sample no."], pos["res"]) if s in lr and lr[s] and lr[s] != (t + dt.timedelta(hours=1)).strftime("%d/%m/%Y"))
    check("B4", mism > 0 and mism2 == 0, "positives whose analyser date is not the line list's result date: %d on the file's "
                                         "clock, %d on local time" % (mism, mism2))
    d = df[df["Reason"] == "Diagnostic"].copy()
    d["res"] = d["res"] + dt.timedelta(hours=1)
    g = d.sort_values(["Sample no.", "res"], kind="stable").groupby("Sample no.").tail(1)
    h = np.array([(a - b).total_seconds() / 3600 for a, b in zip(g["res"], g["coll"])])
    check("B5", _pdf_has(PK.F_PN, "no more than 24 hours"), "the 24-hour boundary is filed (%d samples at exactly 24:00)" % int(np.sum(np.abs(h - 24) < 1e-9)))


def separation_checks():
    """X1: the call reads the line list and the links only; the asks read nothing the call's construction produces."""
    import inspect
    src = inspect.getsource(calc.the_call) + inspect.getsource(calc.load) + inspect.getsource(calc.cases_table) + \
        inspect.getsource(calc.pairs)
    check("X1", PK.F_CT not in src and PK.F_LB not in src and "load_contacts" not in src and "load_mobile_lab" not in src,
          "the call's code path reads %s and %s only" % (PK.F_LL, PK.F_CH))


def _pdf_text(name):
    out = subprocess.run(["pdftotext", "-layout", os.path.join(TARGET, name), "-"], capture_output=True, text=True)
    return re.sub(r"\s+", " ", out.stdout)


def _pdf_has(name, phrase):
    return phrase in _pdf_text(name)


def pdf_checks():
    t = _pdf_text(PK.F_PN)
    pos = all(p in t for p in ("weeks 49 to 52", "half as many new cases", "onsets to Sunday 11 October are complete",
                               "no parameter comes from elsewhere", "exponential growth rate"))
    neg = "this sentence is not in the note" not in t
    check("P1", pos and neg and len(t) > 1500, "planning note reads back (%d characters; positive control and negative "
                                               "control hold)" % len(t))
    import warnings
    import pypdf
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        strict = " ".join(" ".join(pg.extract_text() for pg in pypdf.PdfReader(os.path.join(TARGET, PK.F_PN), strict=True).pages).split())
    check("P3", all(p in strict for p in ("half as many new cases", "exponential growth rate", "ends last for them")),
          "a strict second reader opens the planning note and finds the filed sentences")
    t2 = _pdf_text(PK.F_SR)
    check("P2", "week of notification" in t2 and "reproduction" not in t2.lower() and "serial" not in t2.lower(),
          "the situation report counts by notification week and carries no interval or reproduction number")


def gate_checks():
    files = sorted(os.listdir(TARGET))
    exts = {f.rsplit(".", 1)[1] for f in files}
    import metadata as MD
    rows = MD.rows(TARGET)
    check("I1", len(files) >= 10 and len(exts) >= 3 and max(rows.values()) >= 25000,
          "%d files, formats %s, largest %s with %d rows" % (len(files), sorted(exts), max(rows, key=rows.get), max(rows.values())))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    dis = meta["distractor_files"]
    check("I2", len(dis) >= 2 and all(d in files for d in dis) and not any("distract" in f.lower() for f in files)
          and "fictional" in meta["setting"] and "synthetic" in meta["sources"]["constructed"],
          "%d distractors named in metadata.json and present; the record states the setting fictional and the data synthetic" % len(dis))
    # deleting the distractors moves nothing
    tmp = tempfile.mkdtemp()
    try:
        for f in files:
            if f not in dis:
                shutil.copy2(os.path.join(TARGET, f), tmp)
        g0 = calc.the_call()["total"]
        g1 = calc.the_call(target=tmp)["total"]
        a0, a1 = calc.ask_contacts(), calc.ask_contacts(tmp)
        b0, b1 = calc.ask_lab(), calc.ask_lab(tmp)
        check("I3", g0 == g1 and a0 == a1 and b0 == b1, "the call and the asks are unchanged with the distractors deleted")
    finally:
        shutil.rmtree(tmp)
    bad = []
    words = re.compile(r"fictional|synthetic|constructed for|golden|stump|distractor|decoy|truncat|right[- ]censor|Saldan|Marrisford|Vossmarren|Orrin|" + chr(0x2014), re.I)
    for f in files:
        p = os.path.join(TARGET, f)
        if f.endswith(".pdf"):
            txt = _pdf_text(f)
        elif f.endswith(".xlsx"):
            import zipfile
            z = zipfile.ZipFile(p)
            txt = " ".join(z.read(n).decode("utf-8", "ignore") for n in z.namelist() if n.endswith(".xml"))
        else:
            txt = open(p, encoding="utf-8-sig", errors="ignore").read()
        if words.search(txt):
            bad.append("%s: %s" % (f, words.search(txt).group(0)))
    check("I4", not bad, "realism sweep: no build vocabulary, no fiction disclaimer, no retired name, no em dash in target/ %s" % (bad or ""))
    late = []
    for f in files:
        if dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(TARGET, f))) > dt.datetime(2026, 10, 19, 8, 30):
            late.append(f)
    check("I5", not late, "no file stamped after the pack's compile time")
    import csv as _csv
    import openpyxl
    man = [r["file"] for r in _csv.DictReader(open(os.path.join(TARGET, PK.F_MF), encoding="utf-8-sig"))]
    dic = [r[0] for r in openpyxl.load_workbook(os.path.join(TARGET, PK.F_DD), read_only=True)["Files"].iter_rows(min_row=2, values_only=True) if r[0]]
    check("H9", set(man) == set(files) - {PK.F_MF} and set(dic) == set(files) - {PK.F_MF, PK.F_DD},
          "the manifest names every shipped file but itself (%d), the dictionary every file but the registers (%d)" % (len(man), len(dic)))
    extract = dt.date(2026, 10, 18)
    llr = list(_csv.DictReader(open(os.path.join(TARGET, PK.F_LL), encoding="utf-8-sig")))
    rgr = list(_csv.DictReader(open(os.path.join(TARGET, PK.F_CT), encoding="utf-8-sig")))
    late = []
    for name, rows_, cols in ((PK.F_LL, llr, ("date_of_onset", "date_of_notification", "lab_result_date", "date_admitted",
                                                 "outcome_date", "date_entered")),
                              (PK.F_CT, rgr, ("date_listed", "date_last_exposure", "status_date"))):
        for col in cols:
            vals = [calc.parse_date(r[col]) for r in rows_ if r[col]]
            if vals and max(vals) > extract:
                late.append("%s %s %s" % (name, col, max(vals)))
    ends = max(calc.parse_date(r["follow_up_end"]) for r in rgr)
    check("H16", not late, "every extract date column ends on or before 18 October (follow_up_end, a planned date, runs to %s) %s" % (ends, late or ""))
    ll, ch = calc.load()
    iso = sum(1 for x in ll["date_of_onset"] if "-" in x)
    check("L1", 0 < iso < len(ll) / 5, "%d line-list onsets in ISO form beside day-first ones (Layer 1)" % iso)
    disc = sum(1 for a, b in zip(ch["Source person"], ch["Target person"])
               if b in set(ll.loc[ll["classification"] == "Not a case", "case_number"]))
    nc = calc.variant("with_noncases")[0]
    check("L2", disc > 0 and thousand(nc) == 5000,
          "%d links whose case was later found not to be a case; read with those cases kept the call is %.0f" % (disc, nc))


def run():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    main_call_checks(F)
    clean_truth_checks()
    fork_checks()
    bootstrap_check()
    ask_checks(F)
    separation_checks()
    pdf_checks()
    gate_checks()
    bad = [r for r in RESULTS if not r[1]]
    print("%s  %d checks, %d FAIL" % ("PASS" if not bad else "FAIL", len(RESULTS), len(bad)))
    return not bad


if __name__ == "__main__":
    sys.exit(0 if run() else 1)

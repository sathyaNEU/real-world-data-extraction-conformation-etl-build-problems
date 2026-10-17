"""task234 checks: the three rules executed (R1 to R3c), every semantic fork row (SF1 to SF12), the golden's margins
under every model of the testing response, the rungs, the bench, the ask devices and their stops, the separation of
the call from the devices, and the input gates."""
import os
import re

import numpy as np
import pandas as pd

import estim as E
import params as P

N = [0]
GOLD = {("L03", "Influenza"), ("L03", "RSV"), ("L03", "SARS-CoV-2"), ("L10", "Influenza"), ("L10", "RSV"),
        ("L10", "SARS-CoV-2")}
DEFAULT_WRONG = {("L01", "Influenza"), ("L01", "RSV"), ("L02", "SARS-CoV-2"), ("L04", "SARS-CoV-2"),
                 ("L05", "SARS-CoV-2"), ("L06", "SARS-CoV-2"), ("L07", "SARS-CoV-2"), ("L08", "SARS-CoV-2"),
                 ("L09", "SARS-CoV-2")}
LOGFAMILY = ("log", "logtr", "quad", "poisson", "ratio")


def ok(cond, label):
    assert cond, label
    N[0] += 1


def margin(comp):
    return min(abs(c - E.LINE) for c in comp.values())


def call_with(X, recv=None, S=None, model=E.GOLDEN_MODEL):
    recv = recv or X["recv"]
    S = S or X["S"]
    return E.escalated(E.completeness(recv, E.est_positivity(X["labels"], S, recv, *model)))


def counts(t, week=3):
    wc = E.week_counts(t, week)
    return {k: (float(wc.loc[k, "tests"]), float(wc.loc[k, "positives"])) for k in wc.index}


def alt_tests(D, mode):
    """week-3 counts under a reading the protocol rules out (or that converges)"""
    res = D["res"].copy()
    if mode == "rows":                       # every result row a test (influenza A and B two tests)
        res = res[res.result_status != "X"].copy()
        res["accession"] = res["accession"] + "|" + res["test_code"] + "|" + res["message_id"]
    elif mode == "corrections":              # a corrected result counted as another test
        res = res.copy()
        c = res.result_status == "C"
        res.loc[c, "accession"] = res.loc[c, "accession"] + "C"
    elif mode == "cancelled":                # a cancelled order counted as a test
        res = res.copy()
        res.loc[res.result_status == "X", "result_status"] = "F"
    elif mode == "inconclusive":             # inconclusive results dropped
        res = res[res.result != "INCONCLUSIVE"]
    D2 = dict(D, res=res)
    return E.conform(D2)


def run(target, golden, o, X):
    N[0] = 0
    D, S, recv, labels, tests = X["D"], X["S"], X["recv"], X["labels"], X["tests"]
    W, R = o["W"], o["R"]
    inv = {v: k for k, v in P.LAB_ID.items()}
    vn = {v: k for k, v in P.VNAME.items()}

    # ------------------------------------------------------------ R1: the field's raw material ships, no deciding column
    cols = list(D["res"].columns) + list(D["agg"].columns) + list(D["labs"].columns) + list(D["streams"].columns)
    ok(not any(re.search(r"expect|complete|baseline|flag|escalat|predict|estimat|loss|lost", c, re.I) for c in cols),
       "R1 no shipped column holds an expected count, a completeness or a flag")
    ok(len(S) == 29 and all(len(T) == len(labels) and (T > 0).all() and (Pp >= 0).all() for T, Pp in S.values()),
       "R1 every stream's tests and positives ship for every week since 2022-W40")
    ok(labels[0] == (2022, 40) and labels[-1] == (2027, 2), "R1 the reports run 2022-W40 to 2027-W02")
    ok(set(D["res"].result) == {"DETECTED", "NOT DETECTED", "INCONCLUSIVE", ""}, "R1 each result's value ships")

    # ------------------------------------------------------------ the golden, the truth and the model family
    truth = {k: float(W.T[(inv[k[0]], vn[k[1]])][W.cur]) for k in S}
    true_comp = {k: recv[k][0] / truth[k] for k in S}
    ok(X["gold"]["esc"] == GOLD, "golden: the six streams of Wexmoor and Westmarch")
    ok(E.escalated(true_comp) == GOLD, "golden equals the truth: completeness against the tests the reports will count")
    ok(margin(true_comp) >= 0.12, "the truth sits at least 0.12 from the line in every stream (%.3f)" % margin(true_comp))
    for var, r in X["variants"].items():
        thr = 0.025 if var[0] in ("lin", "lintr") else (0.025 if var[0] == "lag" else 0.05)
        ok(r["esc"] == GOLD, "model %s escalates the golden six" % (var,))
        ok(margin(r["comp"]) >= thr, "model %s nearest stream %.3f from the line" % (var, margin(r["comp"])))
    for form in ("lin", "lintr", "log", "logtr", "quad", "poisson", "ratio", "lag"):
        for w in (13, 17, 20, 26, 39, 52, 60, 80, 120, None):
            for h in (True, False):
                if form in ("quad", "poisson", "lag") and w and w < 17:
                    continue
                ok(call_with(X, model=(form, w, h)) == GOLD, "sweep %s %s %s escalates the golden six" % (form, w, h))
    gm = margin(X["gold"]["comp"])
    ok(gm >= 0.07, "golden model's nearest stream %.3f from the line" % gm)

    # ------------------------------------------------------------ R3a: the analyst test on the clean truth
    clean_recv = {}
    for code, v in P.STREAMS:
        ts = [t for t in R.week_truth[(code, 3)] if t["virus"] == v and t["in_extract"]]
        clean_recv[(P.LAB_ID[code], P.VNAME[v])] = (float(len(ts)), float(sum(t["positive"] for t in ts)))
    clean_S = {(P.LAB_ID[c], P.VNAME[v]): (W.T[(c, v)][:W.cur].astype(float), W.Pos[(c, v)][:W.cur].astype(float))
               for c, v in P.STREAMS}
    ok(clean_recv == {k: recv[k] for k in clean_recv},
       "C1 the shipped extract collapses to exactly the clean truth's week-3 tests and positives in every stream")
    acc_weeks = tests.groupby(["lab_id", "accession"]).week.nunique()
    ok((acc_weeks == 1).all(), "C1 no accession spans two weeks")
    clean_default = E.escalated(E.completeness(clean_recv, E.est_persist(labels, clean_S, clean_recv)))
    ok(clean_default == X["routes"]["persist"]["esc"], "R3a the default path on the clean truth equals the shipped default")
    ok(clean_default ^ GOLD == DEFAULT_WRONG and len(clean_default) == 15,
       "R3a the default path on the clean truth escalates 15 streams, 9 of 29 cells wrong, by name")
    # ------------------------------------------------------------ R3b: the decisive step alone
    ok(E.escalated(E.completeness(clean_recv, E.est_positivity(labels, clean_S, clean_recv, *E.GOLDEN_MODEL))) == GOLD,
       "R3b only the week's tests from the stream's own positivity: the golden on the clean truth")
    for n in ("trend", "mean3", "calendar", "peers", "peers_median", "poscount"):
        est = {"trend": E.est_trend, "mean3": E.est_mean3, "calendar": E.est_calendar, "poscount": E.est_poscount,
               "peers": E.est_peers, "peers_median": lambda l, s, r: E.est_peers(l, s, r, "median")}[n]
        ok(E.escalated(E.completeness(clean_recv, est(labels, clean_S, clean_recv))) == X["routes"][n]["esc"],
           "R3b rung %s on the clean truth equals the shipped rung" % n)

    # ------------------------------------------------------------ the default path and the rungs
    pr = X["routes"]["persist"]
    ok(pr["esc"] ^ GOLD == DEFAULT_WRONG, "default path: 9 wrong cells by name")
    ok(margin(pr["comp"]) >= 0.035, "default path: every stream at least 0.035 from the line (%.3f)" % margin(pr["comp"]))
    for n, r in X["routes"].items():
        wrong = r["esc"] ^ GOLD
        robust = [k for k in wrong if abs(r["comp"][k] - E.LINE) >= 0.03]
        ok(len(robust) >= 2, "rung %s: %d wrong, %d of them 0.03 or more from the line" % (n, len(wrong), len(robust)))
        ok(r["esc"] != GOLD, "rung %s does not land the golden" % n)
    ok(not (X["routes"]["poscount"]["esc"] & {("L03", v) for v in ("Influenza", "RSV", "SARS-CoV-2")}),
       "positives route misses every Wexmoor stream (positives are lost with the rest)")
    ok(("L01", "Influenza") in X["routes"]["peers"]["esc"] and ("L10", "SARS-CoV-2") not in X["routes"]["peers"]["esc"],
       "peers route escalates the children's hospital's influenza and misses Westmarch's SARS-CoV-2")

    # ------------------------------------------------------------ the bench: the reports separate the routes
    bt = E.backtest(labels, S)
    mv = bt["moved"]
    med = {m: 100 * float(np.median(bt[m][mv])) for m in ("persist", "trend", "positivity")}
    ok(mv.sum() >= 150 and med["positivity"] * 3 <= med["persist"] and med["positivity"] * 1.5 <= med["trend"],
       "bench: where positivity moved 3 points, the positivity fit misses %.1f%% at the median, last week %.1f%%, "
       "last week's growth %.1f%%" % (med["positivity"], med["persist"], med["trend"]))
    ok((bt["positivity"] >= 0.15).sum() <= 2 and (bt["persist"] >= 0.15).sum() >= 100 and (bt["trend"] >= 0.15).sum() >= 100,
       "bench: of %d closed stream-weeks the positivity fit misses %d by 15%% or more, last week's count %d, last "
       "week's growth %d" % (len(bt["persist"]), (bt["positivity"] >= 0.15).sum(), (bt["persist"] >= 0.15).sum(),
                             (bt["trend"] >= 0.15).sum()))

    # ------------------------------------------------------------ semantic fork table
    reg_streams = set(zip(D["streams"].lab_id, D["streams"].virus))
    ok(set(zip(tests.lab_id, tests.virus)) == reg_streams and len(reg_streams) == 29,
       "SF1 the streams in the results are the register's 29")
    t_rows = alt_tests(D, "rows")
    rows_recv = counts(t_rows)
    target_flu = {(P.LAB_ID[l[0]], "Influenza") for l in P.LABS if l[7] == "target"}
    ok(target_flu == {("L01", "Influenza"), ("L05", "Influenza"), ("L07", "Influenza")},
       "R2 influenza A and B as separate rows come from three healthy laboratories")
    ok(all(rows_recv[k][0] > 1.9 * recv[k][0] for k in target_flu) and call_with(X, rows_recv) == GOLD,
       "R2 SF2 counting result rows doubles the target-level influenza streams, same call (FCP-2 s.2 rules it out)")
    for mode, sf in (("corrections", "SF3"), ("cancelled", "SF4"), ("inconclusive", "SF11")):
        r2 = counts(alt_tests(D, mode))
        moved = max(abs(r2[k][0] / recv[k][0] - 1) for k in recv)
        ok(call_with(X, r2) == GOLD and moved < 0.02, "R2 %s %s reading: counts move under 2%%, same call" % (sf, mode))
    tu = E.conform(D)
    tu["week"] = [E.mmwr_week_2027((x + E.TZ).date()) for x in tu.first_release]
    ru = counts(tu)
    cu = E.completeness(ru, E.est_positivity(labels, S, ru, *E.GOLDEN_MODEL))
    ok(E.escalated(cu) == GOLD and max(abs(ru[k][0] / recv[k][0] - 1) for k in recv) < 0.15 and margin(cu) >= 0.1,
       "R2 SF5 the week by UTC date: counts move under 15%%, same call, nearest stream %.3f from the line" % margin(cu))
    for clock in ("switch", "utc"):
        t3 = E.conform(D, clock)
        w3 = t3[t3.week == 3]
        ok((w3.first_received <= pd.Timestamp("2027-01-25 08:00")).all(),
           "SF6 every week-3 result in the extract reached the platform by the Monday cutoff (%s clock)" % clock)
    rawrec = pd.to_datetime(D["res"].received)
    ok((rawrec - E.TZ <= pd.Timestamp("2027-01-25 08:00")).all() and (rawrec <= pd.Timestamp("2027-01-25 14:00")).all(),
       "SF6 no row of the extract after the cutoff under either clock")
    ok(X["routes"]["persist"]["esc"] != GOLD, "SF7 last week's report as the denominator is the default path")
    first = D["agg"].sort_values("version").groupby(["lab_id", "virus", "mmwr_year", "mmwr_week"]).head(1)
    ok((D["agg"].version > 1).sum() >= 50, "SF8 resubmissions exist")
    _, S1 = E.series(first)
    ok(call_with(X, S=S1) == GOLD, "R2 SF8 the first submissions instead of the latest: same call")
    ok(margin(X["gold"]["comp"]) > 0.001, "SF9 no stream on the line: below and at-or-below agree")
    fac = D["labs"].set_index("lab_id").sending_facility_ids
    ok(fac["L04"] == "05D0877219, 05D2290465" and set(D["res"].sending_facility) >= {"05D0877219", "05D2290465"},
       "SF10 the merged hospital sends under both identifiers and the register maps both to one laboratory")
    one = dict(D, labs=D["labs"].assign(sending_facility_ids=D["labs"].sending_facility_ids.str.split(",").str[0]))
    res1 = D["res"][D["res"].sending_facility != "05D2290465"]
    share = 1 - len(res1) / len(D["res"])
    r10 = counts(E.conform(dict(one, res=res1)))
    ok(0.003 < share < 0.02 and call_with(X, r10) == GOLD,
       "R2 SF10 the merged campus's identifier left unmapped drops %.1f%% of the extract, same call" % (100 * share))
    fcp = _pdf_text(os.path.join(target, "FCP-2_feed_completeness_protocol.pdf"))
    for phrase, sf in (("RV-FLUA and RV-FLUB", "SF2"), ("replaces the result it corrects", "SF3"),
                       ("is not a test", "SF4"), ("county date (America/Chicago)", "SF5"),
                       ("by 08:00 county time on the Monday after the week", "SF6"),
                       ("tests the laboratory's weekly aggregate report counts", "SF7"),
                       ("latest submission is the report of record", "SF8"), ("below 80 per cent", "SF9"),
                       ("more than one facility identifier is one laboratory", "SF10"),
                       ("inconclusive result is a test", "SF11"), ("whatever the patient's residence", "SF12"),
                       ("one collection from one patient", "ask B")):
        ok(phrase in fcp, "%s pinned in FCP-2: %s" % (sf, phrase))
    ok(not re.search(r"positivit|predict|estimat|model|baseline|last week|previous week", fcp, re.I),
       "FCP-2 names no method for the week's tests")

    # ------------------------------------------------------------ separation: the asks' columns move no escalation
    for hours in (-30, -6, 6, 48):
        D2 = dict(D, res=D["res"].assign(received=(pd.to_datetime(D["res"].received) + pd.Timedelta(hours=hours))
                                         .dt.strftime("%Y-%m-%d %H:%M:%S")))
        ok(call_with(X, counts(E.conform(D2))) == GOLD, "separation: receipt times shifted %+d h, same call" % hours)
    rng = np.random.default_rng(5)
    D3 = dict(D, res=D["res"].assign(patient_mrn=rng.permutation(D["res"].patient_mrn.values),
                                     specimen_collected=rng.permutation(D["res"].specimen_collected.values)))
    ok(call_with(X, counts(E.conform(D3))) == GOLD, "separation: patients and collection times scrambled, same call")

    # ------------------------------------------------------------ ask A: week-2 completeness and its stops
    rep = X["rep"]
    A = X["A"]
    utc = E.ask_a(E.conform(D, "utc"), rep)
    t_neg = E.conform(D, "utc")
    lag = t_neg.first_received - t_neg.first_release
    t_neg.loc[lag < pd.Timedelta(0), "first_received"] = t_neg.loc[lag < pd.Timedelta(0), "first_received"] + E.TZ
    negfix = E.ask_a(t_neg, rep)
    t_drop = E.conform(D, "utc")
    t_drop = t_drop[(t_drop.first_received - t_drop.first_release) >= pd.Timedelta(0)]
    dropped = E.ask_a(t_drop, rep)
    for k in A:
        ok(_edge(100 * A[k]) >= 0.01, "ask A %s %s mid-bin (%.3f)" % (k + (100 * A[k],)))
        ok(round(100 * utc[k], 1) - round(100 * A[k], 1) >= 0.4, "ask A stop: every receipt as UTC reads %s %s high" % k)
        ok(round(100 * negfix[k], 1) - round(100 * A[k], 1) >= 0.4, "ask A stop: negative lags only reads %s %s high" % k)
        ok(round(100 * A[k], 1) - round(100 * dropped[k], 1) >= 5, "ask A stop: negative lags dropped reads %s %s low" % k)
    ok(len(A) == 29, "ask A: 29 streams")
    raw = o["res"]
    raw = raw[(raw.week == 2) & (raw.status != "X")].copy()
    raw["virus"] = raw.code.map({"RV-FLUA": "Influenza", "RV-FLUB": "Influenza", "RV-FLU": "Influenza", "RV-RSV": "RSV",
                                 "RV-COV2": "SARS-CoV-2"})
    raw["lab_id"] = raw.lab.map(P.LAB_ID)
    first = raw.groupby(["lab_id", "virus", "accession"]).received.min()
    truth_a = first[first <= P.CUTOFF_W2_LOCAL].groupby(["lab_id", "virus"]).size()
    ok(all(X["A_counts"][k][0] == truth_a[k] for k in X["A_counts"]),
       "ask A fair: the county-time-before-the-migration reading reproduces the true receipts by the cutoff exactly")
    w2rows = D["res"][pd.to_datetime(D["res"].released) - E.TZ < pd.Timestamp("2027-01-17")]
    ok((pd.to_datetime(w2rows.received) < E.MIGRATION).all(), "ask A: every week-2 receipt precedes the broker migration")
    recd = pd.to_datetime(D["res"].received)
    ok(not ((recd >= pd.Timestamp("2027-01-19 06:00")) & (recd < pd.Timestamp("2027-01-19 12:00"))).any(),
       "ask A: the receipt clock's switch leaves a six-hour gap at the migration")

    # ------------------------------------------------------------ ask B: specimens and its stops
    B = X["B"]
    acc = E.ask_b(tests, key="accession")
    pat = E.ask_b(tests, key="patient")
    ok(len(B) == 10, "ask B: ten laboratories")
    for lab in B:
        ok(acc[lab] - B[lab] >= 50, "ask B stop: distinct accessions reads %s high (%d against %d)" % (lab, acc[lab], B[lab]))
        ok(B[lab] - pat[lab] >= 50, "ask B stop: distinct patients reads %s low (%d against %d)" % (lab, pat[lab], B[lab]))
    w3 = tests[tests.week == 3]
    for clock, shift in (("county", pd.Timedelta(0)), ("UTC", E.TZ)):
        perday = w3.assign(day=(w3.collected + shift).dt.date).groupby("lab_id").apply(
            lambda g: len(set(zip(g.patient, g.day))))
        ok(all(perday[lab] == B[lab] for lab in B),
           "C1 ask B: patient and collection date (%s) counts the same specimens as patient and collection time" % clock)
    gaps = w3.drop_duplicates(["lab_id", "patient", "collected"]).sort_values("collected").groupby(["lab_id", "patient"]).collected.diff()
    ok((gaps.dropna() >= pd.Timedelta(hours=24)).all() and gaps.notna().sum() >= 500,
       "ask B: %d patients swabbed twice in week 3, every pair of collections a day or more apart" % gaps.notna().sum())

    # ------------------------------------------------------------ R3c, input gates, dates
    files = os.listdir(target)
    ok(len(files) >= 10 and len({f.rsplit(".", 1)[1] for f in files}) >= 3, "input gates: files and formats")
    ok(max(sum(1 for _ in open(os.path.join(target, f))) for f in files if f.endswith(".csv")) >= 25001,
       "input gate: a file of 25,000 rows")
    ok(D["agg"].submitted.max() <= "2027-01-24", "no report filed after the extract")
    ok(pd.to_datetime(D["res"].released).max() - E.TZ < pd.Timestamp("2027-01-24"), "no result released after week 3")
    log = pd.read_csv(os.path.join(target, "surveillance_platform_change_log.csv"))
    ok(log.implemented_at.max() < "2027-01-25", "change log ends before the extract")
    ok(not log.change.str.contains(r"time|clock|UTC|zone|Wexmoor|Westmarch|lost|drop", case=False).any(),
       "change log says nothing of receipt clocks or of either laboratory")
    ok(D["res"].message_id.is_unique, "message ids unique")
    dic = open(os.path.join(target, "DATA_DICTIONARY.md")).read()
    rline = next(l for l in dic.splitlines() if l.startswith("| received |"))
    ok(not re.search(r"UTC|county|local|time zone|Chicago", rline), "the dictionary states no zone for the receipt time")
    for f in ("submission.md",):
        p = os.path.join(os.path.dirname(target), f)
        if os.path.exists(p):
            ok("\u2014" not in open(p).read(), "no em dash in %s" % f)
    return N[0]


def _edge(x):
    s = x * 10
    return abs((s - np.floor(s)) - 0.5) / 10


def _pdf_text(path):
    from pypdf import PdfReader
    return " ".join(" ".join(pg.extract_text().split()) for pg in PdfReader(path).pages)

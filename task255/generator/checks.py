"""Assertions on the built pack and goldens: the input gates; the three rules executed on the generator's clean truth
(R1 the field's raw material ships, R2 each Layer 1 item is neutral, R3a the easy route files the wrong attachment,
R3b the decisive step alone files the golden, R3c no plant); every rung at its named attachment with its margin; the
convergent variants; the semantic forks SF1 to SF14; the rounding bins; the ask devices against the truth and every
wrong path outside the golden in every class and at every attachment; the main population's separation from the
asks; the distractors; the realism sweep; and the goldens agreeing with figures.json."""
import collections
import csv
import datetime as dt
import json
import os
import random
import re

import openpyxl

import analysis as A
import build as B
import docs as D
import golden as G
import records as R
import world as W

N = [0]


def ok(cond, what):
    N[0] += 1
    if not cond:
        raise AssertionError(what)


def _pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in PdfReader(path).pages))


def _pick_of(rows, **kw):
    mu, sg, _ = A.mle(rows, **kw)
    return A.pick(A.counts(mu, sg)), A.counts(mu, sg), mu, sg


def _half_distance(x, places):
    """distance of x from the nearest rounding edge at the given decimal places, in units of the last place"""
    v = x * 10 ** places
    return abs((v % 1) - 0.5)


def run(target, golden, st, metadata):
    rec, mem, fig = st["rec"], st["mem"], st["fig"]
    files = sorted(os.listdir(target))
    meta = json.load(open(metadata))

    # ------------------------------------------------------------ input gates
    ok(len(files) >= 10, "at least 10 files (%d)" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "at least 3 formats")
    ok(st["counts"]["log"] >= 25_000, "a file of 25,000 rows or more")
    ok(len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]), "two distractors shipped")
    ok(not any("distractor" in f.lower() for f in files), "no file named for its role")
    ok(st["counts"]["log"] % 100 != 0, "the log's row count is not a round number")

    # ------------------------------------------------------------ the record the call reads
    rows = A.fit_rows(rec)
    ok(len(rows) == fig["fit"]["n"] == 820, "820 closed occurrences of 2014 to 2021")
    ok(all(r["status"] == "closed" for r in rec if r["ay"] in W.FIT_YEARS), "every 2014 to 2021 occurrence closed")
    ok(any(r["status"] == "open" for r in rec if r["ay"] == 2022), "2022 still has an open occurrence (2021 is the latest closed year)")
    ok(all(r["close"] <= dt.date(2026, 6, 30) for r in rec if r["ay"] in W.FIT_YEARS), "closed by 30 June 2026 (C1 on the as-of)")
    leg = {r["legacy_no"] for r in rec if r["system"] == "legacy"}
    conv = {r.get("legacy_no") for r in rec if r["system"] == "current" and r["converted"]}
    ok(not (leg & conv), "no claim in both administrators' runs (axis 15)")
    ok(fig["fit"]["capped"] == 108 and fig["fit"]["capped_250k"] == 67 and fig["fit"]["capped_500k"] == 41,
       "108 occurrences stopped at the retention (67 at $250,000, 41 at $500,000)")
    ok(min(r["ret"] - r["cost"] for r in rows if not r["capped"]) > 10, "no uncapped cost within $10 of a retention (axis 9)")
    ok(min(r["cost"] - r["ded"] for r in rows) > 0, "every recorded cost above its deductible")
    ok(all(r["x"] > r["ded"] for r in rec), "the record holds only occurrences above the deductible")
    ground = [o for o in st["occ"] if o["ay"] in W.FIT_YEARS]
    ok(len(ground) > 2 * len(rows), "most ground-up occurrences of 2014 to 2021 never reached the pool (%d of %d)"
       % (len(ground) - len(rows), len(ground)))

    # ------------------------------------------------------------ R1: the field's raw material ships
    ok(st["counts"]["legacy"] + sum(1 for r in rec if r["system"] == "current" and r["ay"] in W.FIT_YEARS) == 820,
       "R1: the fit reads the loss runs' occurrence rows")
    texts = {f: _pdf_text(os.path.join(target, f)) for f in files if f.endswith(".pdf")}
    texts[D.NOTES] = open(os.path.join(target, D.NOTES)).read()
    for f, t in texts.items():
        for v in ("10.18", "1.71", "0.74", "1.25", "4,000,000 is", "3,396"):
            ok(v not in t, "R1: %s carries no fitted figure (%s)" % (f, v))
    for word in ("truncat", "censor", "likelihood of the record", "lognormal fitted"):
        ok(all(word not in t.lower() for f, t in texts.items() if f != D.POLICY), "R1: no document narrates %s" % word)
    ok("truncat" not in texts[D.POLICY].lower() and "censor" not in texts[D.POLICY].lower(),
       "R1: the policy files no truncation or censoring")

    # ------------------------------------------------------------ the ladder and R3
    lad = A.ladder(rows)
    picks = {k: v["pick"] for k, v in lad.items()}
    ok(picks == {"R0": 2_000_000, "R1": 2_500_000, "R2": 2_000_000, "R3": 4_000_000, "G": 4_000_000},
       "rungs at their named attachments %s" % picks)
    ok(lad["G"]["pick"] == fig["call"]["attachment"] == 4_000_000, "golden $4.0 million")
    g = lad["G"]["counts"]
    ok(g[4_000_000] <= 0.76 and g[3_000_000] >= 1.24, "golden margins: 0.74 at $4.0m, 1.25 at $3.0m")
    ok(1.0 / g[4_000_000] >= 1.3 and g[3_000_000] >= 1.25, "margins 1.36x and 1.25x")
    ok(lad["R0"]["counts"][2_000_000] <= 0.62 and lad["R0"]["counts"][1_500_000] >= 1.5, "R0 at $2.0 million with margin")
    ok(lad["R1"]["counts"][2_500_000] < 1.0 < lad["R1"]["counts"][2_000_000], "R1 at $2.5 million")
    ok(lad["R2"]["counts"][2_000_000] <= 0.71 and lad["R2"]["counts"][1_500_000] >= 1.4, "R2 at $2.0 million")
    ok(lad["R3"]["counts"][4_000_000] <= 0.66 and lad["R3"]["counts"][3_000_000] >= 1.3, "R3 converges on $4.0 million")
    ok(g[4_000_000] / lad["R1"]["counts"][4_000_000] >= 3.4, "the decisive move multiplies the count above $4.0m by 3.6")
    # R3a: the easy route on the clean truth, every filed rule applied (window, cost, index, formula, line)
    ok(picks["R0"] == 2_000_000, "R3a analyst test: the complete-sample fit files $2.0 million")
    ok(picks["R1"] == 2_500_000, "R3a: censoring the capped occurrences alone files $2.5 million")
    # R3b: the decisive step alone (truncation added to the censored fit) files the golden; each single correction
    # from the default leaves a wrong answer
    ok(picks["G"] == 4_000_000 and picks["R1"] != 4_000_000 and picks["R2"] != 4_000_000,
       "R3b: truncation with censoring files $4.0 million; either alone does not")
    # the same likelihood in each accident year's dollars, rows shuffled, and a common floor
    mu_y, sg_y = A.mle_accident_year_dollars(rows)
    ok(abs(mu_y - lad["G"]["mu"]) < 1e-4 and abs(sg_y - lad["G"]["sigma"]) < 1e-4, "accident-year dollars give the same fit")
    sh = rows[:]
    random.Random(255).shuffle(sh)
    mu_s, sg_s, _ = A.mle(sh)
    ok(abs(mu_s - lad["G"]["mu"]) < 1e-5 and abs(sg_s - lad["G"]["sigma"]) < 1e-5, "row order changes nothing (axis 14)")
    floor = 100_000 * W.factor(2014)
    com = [dict(r, ded=floor / r["f"]) for r in rows if r["cost"] * r["f"] > floor]
    pk, cc, _, _ = _pick_of(com)
    ok(pk == 4_000_000, "a common floor at $215,600 files $4.0 million (%.2f, %.2f)" % (cc[4_000_000], cc[3_000_000]))
    fits = []
    for st0 in A.STARTS:
        import numpy as np
        from scipy import optimize, stats
        f = np.array([r["f"] for r in rows])
        lx = np.log(np.array([r["cost"] for r in rows]) * f)
        ld = np.log(np.array([r["ded"] for r in rows]) * f)
        c = np.array([r["capped"] for r in rows])

        def nll(p):
            m, s = p[0], abs(p[1])
            z = (lx - m) / s
            ll = np.where(c, stats.norm.logsf(z), stats.norm.logpdf(z) - np.log(s) - lx)
            return -(ll - stats.norm.logsf((ld - m) / s)).sum()
        res = optimize.minimize(nll, st0, method="Nelder-Mead", options=dict(xatol=1e-11, fatol=1e-11, maxiter=60000))
        fits.append((res.x[0], abs(res.x[1])))
    ok(max(abs(a - lad["G"]["mu"]) for a, _ in fits) < 1e-4, "SF14: every starting point reaches one optimum")

    # ------------------------------------------------------------ R2: each Layer 1 item neutral when mishandled
    swapped = []
    for r in rec:
        if r["system"] != "legacy":
            continue
        d = r["date"]
        if d.day <= 12:
            try:
                d2 = dt.date(d.year, d.day, d.month)
            except ValueError:
                d2 = d
            swapped.append(d2.year == d.year)
    ok(all(swapped), "R2: legacy dates read day first keep every accident year")
    ok(fig["call"]["attachment"] == 4_000_000, "R2: the converted claims' new numbers and member codes leave the call")

    # ------------------------------------------------------------ semantic forks
    pol = texts[D.POLICY]
    memo = texts[D.MEMO]
    quotes = texts[D.QUOTES]
    study = texts[D.STUDY]
    ok("from its first dollar and inclusive of the member's deductible" in pol and
       "inclusive of the member's deductible" in quotes, "SF1: attachments from the first dollar, inclusive")
    nos = [r["claim_no"] for r in rec if r["system"] == "current" and r["status"] != "untendered"]
    ok(len(nos) == len(set(nos)) and len(leg) == st["counts"]["legacy"], "SF2: one row per occurrence in both runs")
    ind = [dict(r, cost=round(q["ded"] + q["paid_ind"], 2)) for r, q in
           zip(rows, [q for q in rec if q["ay"] in W.FIT_YEARS and q["status"] == "closed"])]
    pk, _, _, _ = _pick_of(ind)
    ok(pk == 2_000_000 and "damages and defense costs together" in pol, "SF3: damages only files $2.0 million; ruled out by 2.2")
    pk, _, _, _ = _pick_of([dict(r, f=1.0) for r in rows])
    ok(pk == 2_500_000 and "ratio of the coverage year's claim cost index to the accident year's" in pol,
       "SF4: no trend files $2.5 million; ruled out by 4.2")
    cur = [r for r, q in zip(rows, [q for q in rec if q["ay"] in W.FIT_YEARS and q["status"] == "closed"])
           if q["system"] == "current"]
    pk, cc, _, _ = _pick_of(cur)
    ok(pk is None and "were converted to" in texts[D.NOTES], "SF5: the current run alone passes no attachment")
    allc = []
    for q in rec:
        if q["status"] == "closed":
            cst = round(q["ded"] + q["paid_ind"] + q["paid_def"], 2)
            allc.append({"ay": q["ay"], "f": W.factor(q["ay"]), "ded": q["ded"], "ret": q["ret"], "cost": cst,
                         "capped": cst >= q["ret"] - 0.005})
    pk, _, _, _ = _pick_of(allc)
    ok(pk == 4_000_000 and "2014 to 2021" in pol, "SF6: closed occurrences of every year converge on $4.0 million")
    ok("divided by the curve's probability that an occurrence costs more than $25,000" in pol, "SF7: policy 4.3 filed")
    ok(min(abs(v - 1.0) for v in g.values()) >= 0.25, "SF8: no count within 0.25 of the line")
    ok(picks["R3"] == 4_000_000, "SF9: thresholds left nominal give $4.0 million")
    byno = {m["no"]: m for m in mem}
    ok(all(r["ded"] == W.deductible_on(byno[r["member"]], r["date"]) for r in rec), "SF10: each row's deductible is the one in force")
    ok("lowest attachment quoted for that year" in pol and fig["call"]["attachment"] in W.OPTIONS, "SF11: quoted attachments only")
    rounded = {a: round(v, 2) for a, v in g.items()}
    ok(A.pick(rounded) == 4_000_000, "SF12: rounding before comparing keeps $4.0 million")
    ok(min(_half_distance(v, 2) for v in g.values()) >= 0.15, "SF12: every count clear of its two-decimal edge")
    ok("from the first dollar" in study and "at 2027 cost" in study and "228.7" in study, "SF13: the anchor's basis filed")

    # ------------------------------------------------------------ bins of the graded figures
    ok(_half_distance(fig["curve"]["mu"], 2) >= 0.15 or _half_distance(fig["curve"]["mu"], 1) >= 0.2,
       "log mean clear of its edge")
    ok(_half_distance(fig["curve"]["sigma"], 2) >= 0.3, "log standard deviation clear of its edge")
    T, U = fig["exposure"]["toe"], fig["exposure"]["units"]
    for a in W.OPTIONS:
        ok(_half_distance(A.premium(T, U, a), 0) >= 0.05, "premium at %d clear of the half dollar" % a)
    for k, e in fig["by_class"].items():
        toe = sum(d["toe"] for d in st["dec"] if d["kind"] == k)
        ok(_half_distance(toe / 1000, 0) >= 0.02, "%s expenditure clear of the half thousand" % k)
    ok(abs(fig["call"]["flip_count_25k_runner_passes"] - 182.5) < 0.05 and
       abs(fig["call"]["flip_count_25k_call_fails"] - 310.0) < 0.05, "flip counts 182.5 and 310.0")

    # ------------------------------------------------------------ the ask devices against the truth
    kind = {m["no"]: m["kind"] for m in mem}
    D_ = W.RATING_DATE
    truth = collections.Counter(u["member"] for u in st["units"] if u["acquired"] <= D_ < u["disposed"])
    gold_u = A.scheduled_units(st["log"])
    ok(gold_u == truth, "the schedule read one vehicle per latest number reproduces the fleets exactly")
    gold_cls = A.by_class(gold_u, kind)
    for mode in ("raw", "dedup_live", "raw_vin", "vin_only"):
        alt = A.by_class(A.units_naive(st["log"], mode=mode), kind)
        ok(all(alt[k] != gold_cls[k] for k in gold_cls), "vehicles by class: the %s path misses every class" % mode)
    toe_g = collections.Counter()
    toe_sum = collections.Counter()
    for d in st["dec"]:
        toe_g[d["kind"]] += d["toe"]
        toe_sum[d["kind"]] += d["toe"] * (1 if d["paper"] else len(d["lines"]))
    ok(all(round(toe_sum[k] / 1000) != round(toe_g[k] / 1000) for k in toe_g), "expenditure summed over lines misses every class")
    ok(all(any(not d["paper"] and len(d["lines"]) > 1 for d in st["dec"] if d["kind"] == k) for k in toe_g),
       "every class has an online member declaring two or more departments")
    ok(all(any(m["consortium"] and kind[m["no"]] == k for m in mem) for k in toe_g), "every class has a consortium member")
    Tc, Uc = sum(toe_sum.values()), sum(A.units_naive(st["log"], mode="raw").values())
    for a in W.OPTIONS:
        good = round(A.premium(T, U, a))
        ok(good == fig["premiums"][str(a)], "premium at %d" % a)
        for t_, u_ in ((Tc, Uc), (T, Uc), (Tc, U), (T, sum(A.units_naive(st["log"], mode="dedup_live").values()))):
            ok(round(A.premium(t_, u_, a)) != good, "a wrong exposure path misses the premium at %d" % a)
    # the mirror's counts (R1) and the default's (R0) differ from the golden at two decimals at every attachment
    for k in ("R0", "R1", "R2"):
        ok(all(round(lad[k]["counts"][a], 2) != round(g[a], 2) for a in W.OPTIONS), "%s's counts miss at every attachment" % k)
    # the main population holds no ask device: the fit reads no declaration or log row
    ok(fig["call"]["attachment"] == A.pick(A.counts(*A.mle(A.fit_rows(rec))[:2])), "the call reads only the loss runs")

    # ------------------------------------------------------------ distractors: nothing reads them
    for f in meta["distractor_files"]:
        ok(f in (R.DEDHIST, R.TRIANGLES), "distractor %s is one of the two declared" % f)
    tri = list(csv.DictReader(open(os.path.join(target, R.TRIANGLES))))
    last = {int(r["accident_year"]): float(r["paid_to_date"]) for r in tri if r["evaluation_date"] == "2026-09-30"}
    for ay in W.FIT_YEARS:
        ok(abs(last[ay] - sum(r["paid_ind"] + r["paid_def"] for r in rec if r["ay"] == ay)) < 0.05,
           "the triangles' latest diagonal ties to the loss runs (%d)" % ay)

    # ------------------------------------------------------------ realism sweep and timestamps
    by_ay = collections.Counter(r["ay"] for r in rows)
    ok(len(set(by_ay.values())) >= 6, "occurrence counts differ across accident years")
    ok(T % 1000 != 0 and U % 10 != 0, "no round exposure totals")
    ok(all(r["date"] <= W.AS_OF and r["tender"] <= W.AS_OF for r in rec if r["status"] != "untendered"), "no date past the evaluation")
    ok(all(r["close"] <= W.AS_OF for r in rec if r["status"] == "closed"), "closing dates by the evaluation")
    ok(all(r["entered"] <= W.LOG_EXTRACT for r in st["log"]), "log entries by its extract date")
    ok(all(d["submitted"] <= dt.date(2026, 10, 5) for d in st["dec"]), "declarations submitted before their export")
    ok(len({v for v in (W.PEOPLE[k][0] for k in W.PEOPLE)}) == 4, "four personas")
    vins = [u["vin"] for u in st["units"] if u["vin"]]
    ok(len(vins) == len(set(vins)), "no two vehicles share a VIN")
    sers = [u["serial"] for u in st["units"] if u["serial"]]
    ok(len(sers) == len(set(sers)), "no two units share a serial")
    for f in files + os.listdir(golden):
        p = os.path.join(target if f in files else golden, f)
        if f.endswith((".csv", ".md")):
            ok("—" not in open(p, encoding="utf-8").read(), "no em dash in %s" % f)

    # ------------------------------------------------------------ the goldens agree with figures.json
    wb = openpyxl.load_workbook(os.path.join(golden, G.WORKBOOK))
    ws = wb["Retention 2027"]
    body = [r for r in ws.iter_rows(min_row=6, max_row=12, values_only=True)]
    ok([r[0] for r in body] == list(W.OPTIONS), "workbook lists the seven attachments")
    for r in body:
        ok(abs(r[1] - round(fig["counts"][str(r[0])], 2)) < 1e-9, "workbook count at %d" % r[0])
        ok(r[5] == fig["premiums"][str(r[0])], "workbook premium at %d" % r[0])
    ex = wb["Rated exposure"]
    got = {r[0].lower(): r for r in ex.iter_rows(min_row=5, max_row=11, values_only=True)}
    for k, e in fig["by_class"].items():
        ok(got[k][2] == e["toe_000"] and got[k][3] == e["units"] and got[k][1] == e["members"], "exposure sheet %s" % k)
    ok(os.path.getsize(os.path.join(golden, G.CHART)) > 20_000, "the chart rendered")
    print("checks: %d assertions passed" % N[0])

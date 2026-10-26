"""Assertions on the built pack and goldens: the input gates; the three rules executed on the generator's clean truth
(R1 the field's raw material ships, R2 each Layer 1 item is neutral, R3a the easy route files the wrong attachment,
R3b the decisive step alone files the golden, R3c no plant); every rung at its named attachment with its margin; the
convergent variants; the semantic forks SF1 to SF16; the rounding bins; the ask devices against the truth and every
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
FAILED = []


def ok(cond, what):
    N[0] += 1
    if not cond:
        FAILED.append(what)
        print("FAIL", what)


def _pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in PdfReader(path).pages))


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
    rows, fits, curves, g = A.golden(rec)
    src = [q for q in rec if q["ay"] in W.FIT_YEARS and q["status"] != "untendered"]
    ok(len(rows) == fig["fit"]["n"] == 1071, "1,071 occurrences of 2014 to 2021 in the pool's record")
    ok(fig["fit"]["open"] == 8 and fig["fit"]["closed"] == 1063, "1,063 closed and 8 still open")
    fy_open = [r for r in src if r["status"] == "open"]
    ok(all(r["capped"] and r["part"] == "LE" and r["res_ind"] + r["res_def"] == 0 and
           abs(r["ded"] + r["paid_ind"] + r["paid_def"] - r["ret"]) < 0.006 for r in fy_open),
       "every open file of 2014 to 2021 is a law enforcement suit past the retention whose layer the pool has paid")
    ok(all(r["status"] == "closed" for r in src if not r["capped"]), "every occurrence of 2014 to 2021 below the retention is closed")
    ok(all(r["close"] <= dt.date(2026, 6, 30) for r in src if r["status"] == "closed"),
       "closed files closed by 30 June 2026 (C1 on the as-of)")
    leg = {r["legacy_no"] for r in rec if r["system"] == "legacy"}
    conv = {r.get("legacy_no") for r in rec if r["system"] == "current" and r["converted"]}
    ok(not (leg & conv), "no claim in both administrators' runs (axis 15)")
    ok(fig["fit"]["capped"] == 25 and fig["fit"]["capped_r1"] == 15 and fig["fit"]["capped_r2"] == 10,
       "25 occurrences stopped at the retention (15 at $500,000, 10 at $1,000,000)")
    ok(fig["curves"]["LE"]["n"] == 314 and fig["curves"]["LE"]["capped"] == 25 and fig["curves"]["OT"]["n"] == 757,
       "314 law enforcement occurrences (all 25 at the retention) and 757 others")
    ok(min(r["ret"] - r["cost"] for r in rows if not r["capped"]) > 10, "no uncapped cost within $10 of a retention (axis 9)")
    ok(min(r["cost"] - r["ded"] for r in rows) > 0, "every recorded cost above its deductible")
    ok(all(r["x"] > r["ded"] for r in rec), "the record holds only occurrences above the deductible")
    ground = [o for o in st["occ"] if o["ay"] in W.FIT_YEARS]
    ok(len(ground) > 2 * len(rows), "most ground-up occurrences of 2014 to 2021 never reached the pool (%d of %d)"
       % (len(ground) - len(rows), len(ground)))
    ok(len({o["date"] for o in ground}) > 2000, "loss dates spread through each year")

    # ------------------------------------------------------------ R1: the field's raw material ships
    ok(st["counts"]["legacy"] + sum(1 for r in src if r["system"] == "current") == 1071,
       "R1: the fit reads the loss runs' occurrence rows")
    texts = {f: _pdf_text(os.path.join(target, f)) for f in files if f.endswith(".pdf")}
    texts[D.NOTES] = open(os.path.join(target, D.NOTES)).read()
    banned = ["%.2f" % fig["curves"][k][x] for k in ("LE", "OT") for x in ("mu_2dp", "sigma_2dp")]
    banned += ["4,000,000 is", "{:,}".format(fig["layer_loss_100k"]["4000000"])]
    for f, t in texts.items():
        for v in banned:
            ok(v not in t, "R1: %s carries no fitted figure (%s)" % (f, v))
    for word in ("truncat", "censor", "likelihood of the record", "mixture", "separately", "each coverage part", "coverage group", "by coverage part"):
        ok(all(word not in t.lower() for t in texts.values()), "R1: no document narrates %s" % word)

    # ------------------------------------------------------------ the ladder and R3
    lad = A.ladder(rec)
    picks = {k: v["pick"] for k, v in lad.items()}
    ok(picks == {"R0": 2_000_000, "R1": 2_000_000, "R2": 2_000_000, "R3": 2_000_000, "shift": 2_500_000,
                 "G_closed": 2_500_000, "G_nominal": 5_000_000, "parts5": 4_000_000, "G": 4_000_000},
       "rungs at their named attachments %s" % picks)
    ok(lad["G"]["pick"] == fig["call"]["attachment"] == 4_000_000, "golden $4.0 million")
    ok(g[4_000_000] <= 0.83 and g[3_000_000] >= 1.18, "golden margins: 0.82 at $4.0m, 1.19 at $3.0m")
    r3 = lad["R3"]["counts"]
    ok(r3[2_000_000] <= 0.9 and r3[1_500_000] >= 1.5, "R3, the pooled curve: 0.89 at $2.0m, 1.55 at $1.5m")
    ok(lad["shift"]["counts"][2_500_000] <= 0.8 and lad["shift"]["counts"][2_000_000] >= 1.15, "one spread at $2.5m")
    ok(lad["G_closed"]["counts"][2_500_000] <= 0.99 and lad["G_closed"]["counts"][2_000_000] >= 1.3,
       "the groups on the closed files alone at $2.5m")
    # R3a: the easy route on the clean truth, every filed rule applied (window, cost, index, formula, line)
    ok(picks["R3"] == 2_000_000 and fig["pooled"]["pick"] == 2_000_000,
       "R3a analyst test: one curve over the pooled record, truncated and censored, files $2.0 million")
    # R3b: the decisive step alone (each group's tail fitted apart and weighted by its projection) files the golden
    ok(picks["G"] == 4_000_000 and picks["R3"] != 4_000_000,
       "R3b: the same likelihood by coverage group files $4.0 million; pooled it does not")
    # the record rejects the pooled curve and the one spread
    ok(fig["lr"]["pooled"] >= 100 and fig["lr"]["one_spread"] >= 20,
       "the record rejects one curve (2 dlogL %.1f on 2) and one spread (%.1f on 1)" % (fig["lr"]["pooled"],
                                                                                         fig["lr"]["one_spread"]))
    # a curve per coverage part, the other parts weighted by their share above $25,000, converges at one decimal
    ok(all(round(lad["parts5"]["counts"][a], 1) == round(g[a], 1) for a in W.OPTIONS),
       "SF18: a curve per coverage part reproduces every count at one decimal")
    lay = lad["G"]["layer"]
    ok(all(int(round(lad["parts5"]["layer"][a] / 1e5)) == int(round(lay[a] / 1e5)) for a in W.OPTIONS),
       "SF18: a curve per coverage part reproduces every layer loss to the hundred thousand")
    edge = lambda v, u: u / 2 - abs(v - round(v / u) * u)
    ok(min(min(edge(lay[a], 1e5), edge(lad["parts5"]["layer"][a], 1e5)) for a in W.OPTIONS) >= 20_000,
       "every layer loss, golden and five-part, at least $20,000 from its rounding edge")
    for k in ("R0", "R1", "R2", "R3", "shift", "G_closed", "G_nominal"):
        ok(all(round(lad[k]["layer"][a] / 1e5) != round(lay[a] / 1e5) for a in W.OPTIONS),
           "%s's layer losses miss at every attachment" % k)
    ok(all(round(fig["layer_loss"][str(a)] / 1e5) * 100_000 == fig["layer_loss_100k"][str(a)] for a in W.OPTIONS),
       "layer losses in figures.json")
    paid = A.group_fits(A.fit_rows(rec, open_at="paid"))
    ok(all(abs(paid[k][0] - curves[k][0]) < 1e-6 and abs(paid[k][1] - curves[k][1]) < 1e-6 for k in A.GROUPS),
       "SF15: an open suit read at its payments or at payments and reserves is the same record (the layer paid)")
    for k, parts in A.GROUPS.items():
        rr = [r for r in rows if r["part"] in parts]
        mu_y, sg_y = A.mle_accident_year_dollars(rr)
        ok(abs(mu_y - curves[k][0]) < 1e-4 and abs(sg_y - curves[k][1]) < 1e-4,
           "SF9: accident-year dollars with nominal thresholds give the same %s fit" % k)
        sh = rr[:]
        random.Random(255).shuffle(sh)
        mu_s, sg_s, _ = A.mle(sh)
        ok(abs(mu_s - curves[k][0]) < 1e-5 and abs(sg_s - curves[k][1]) < 1e-5, "row order changes nothing (axis 14)")
        import numpy as np
        from scipy import optimize, stats
        f = np.array([r["f"] for r in rr])
        lx = np.log(np.array([r["cost"] for r in rr]) * f)
        ld = np.log(np.array([r["ded"] for r in rr]) * f)
        c = np.array([r["capped"] for r in rr])

        def nll(p):
            m, s_ = p[0], abs(p[1])
            z = (lx - m) / s_
            ll = np.where(c, stats.norm.logsf(z), stats.norm.logpdf(z) - np.log(s_) - lx)
            return -(ll - stats.norm.logsf((ld - m) / s_)).sum()
        sols = [optimize.minimize(nll, st0, method="Nelder-Mead",
                                  options=dict(xatol=1e-11, fatol=1e-11, maxiter=60000)).x for st0 in A.STARTS]
        ok(max(abs(x[0] - curves[k][0]) for x in sols) < 1e-4, "SF14: every starting point reaches one %s optimum" % k)
    floor = 100_000 * W.factor(2014)
    com = A.group_fits([dict(r, ded=floor / r["f"]) for r in rows if r["cost"] * r["f"] > floor])
    ok(A.pick(A.counts_groups({k: com[k] for k in A.GROUPS})) == 4_000_000, "a common floor at $215,600 files $4.0 million")

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
    ok("closes the pool's file" not in memo, "the memorandum says nothing on when the pool's file closes")
    notes1 = " ".join(texts[D.NOTES].split())
    ok("A vehicle is identified by its VIN, or by its serial number where it has no VIN" in notes1 and
       "the members' earlier unit numbers for the same vehicles were left on the schedule" in notes1 and
       "deletes for those vehicles come under its asset numbers" in notes1,
       "SF16: the notes file a vehicle's identity and how the consortium's numbers relate to the earlier ones")
    ok("from its first dollar and inclusive of the member's deductible" in pol and
       "inclusive of the member's deductible" in quotes, "SF1: attachments from the first dollar, inclusive")
    nos = [r["claim_no"] for r in rec if r["system"] == "current" and r["status"] != "untendered"]
    ok(len(nos) == len(set(nos)) and len(leg) == st["counts"]["legacy"], "SF2: one row per occurrence in both runs")

    def gpick(rr):
        f_ = A.group_fits(rr)
        return A.pick(A.counts_groups({k: f_[k] for k in A.GROUPS}))
    ind = [dict(r, cost=round(q["ded"] + q["paid_ind"], 2), capped=round(q["ded"] + q["paid_ind"], 2) >= q["ret"] - 0.005)
           for r, q in zip(rows, src)]
    ok(gpick(ind) == 1_000_000 and "damages and defense costs together" in pol,
       "SF3: damages only files $1.0 million; ruled out by 2.2")
    ok(gpick([dict(r, f=1.0) for r in rows]) == 2_500_000 and
       "ratio of the coverage year's claim cost index to the accident year's" in pol, "SF4: no trend files $2.5 million")
    ok(gpick([r for r, q in zip(rows, src) if q["system"] == "current"]) is None and "were converted to" in texts[D.NOTES],
       "SF5: the current run alone passes no attachment")
    allc = []
    for q in rec:
        if q["status"] == "closed":
            cst = round(q["ded"] + q["paid_ind"] + q["paid_def"], 2)
            allc.append({"ay": q["ay"], "f": W.factor(q["ay"]), "ded": q["ded"], "ret": q["ret"], "cost": cst,
                         "capped": cst >= q["ret"] - 0.005, "open": False, "part": q["part"]})
    ok(gpick(allc) == 2_500_000 and "the accident years 2014 to 2021" in pol,
       "SF6: the closed files of every accident year file $2.5 million; ruled out by policy 4.2's years")
    ok("times the estimated probability that an occurrence of the year costing more than $25,000 costs more than "
       "the amount" in pol, "SF7: policy 4.3 filed")
    ok(min(abs(v - 1.0) for v in g.values()) >= 0.17, "SF8: no count within 0.17 of the line")
    byno = {m["no"]: m for m in mem}
    ok(all(r["ded"] == W.deductible_on(byno[r["member"]], r["date"]) for r in rec), "SF10: each row's deductible is the one in force")
    ok("lowest attachment quoted for that year" in pol and fig["call"]["attachment"] in W.OPTIONS, "SF11: quoted attachments only")
    rounded = {a: round(v, 1) for a, v in g.items()}
    ok(A.pick(rounded) == 4_000_000, "SF12: rounding before comparing keeps $4.0 million")
    ok(min(_half_distance(v, 1) for v in g.values()) >= 0.17 and
       min(_half_distance(v, 1) for v in lad["parts5"]["counts"].values()) >= 0.17,
       "SF12: every count, golden and five-part, clear of its one-decimal edge")
    ok("from the first dollar" in study and "at 2027 cost" in study and "%.1f" % W.COUNT_LE in study
       and "%.1f" % W.COUNT_OT in study and "%.1f" % W.COUNT_25K in study, "SF13: the anchors' basis filed")
    ok("Severity is modelled as lognormal" in pol and "the curve" not in pol.lower(),
       "SF17: the policy files the family, never one curve or a curve per part")

    # ------------------------------------------------------------ bins of the graded figures
    T, U = fig["exposure"]["toe"], fig["exposure"]["units"]
    for a in W.OPTIONS:
        ok(_half_distance(A.premium(T, U, a), 0) >= 0.05, "premium at %d clear of the half dollar" % a)
    for k, e in fig["by_class"].items():
        toe = sum(d["toe"] for d in st["dec"] if d["kind"] == k)
        ok(_half_distance(toe / 1000, 0) >= 0.02, "%s expenditure clear of the half thousand" % k)

    # ------------------------------------------------------------ the ask devices against the truth
    kind = {m["no"]: m["kind"] for m in mem}
    D_ = W.RATING_DATE
    leaving = {m["no"] for m in mem if m.get("withdraws")}
    ok(len(leaving) == 1 and all(m["withdraws"] == dt.date(2026, 12, 31) for m in mem if m.get("withdraws")),
       "one member declared for 2027 and leaves on 31 December 2026")
    ok(all(any(d["member"] == m for d in st["dec"]) for m in leaving), "the leaving member declared for 2027")
    owner = lambda u: u["transfer"][1] if "transfer" in u and u["transfer"][0] <= D_ else u["member"]
    truth = collections.Counter(owner(u) for u in st["units"] if u["acquired"] <= D_ < u["disposed"] and owner(u) not in leaving)
    gold_u = A.scheduled_units(st["log"], leaving=leaving)
    ok(gold_u == truth, "the schedule read one vehicle per latest number, under its latest member, reproduces the fleets")
    gold_cls = A.by_class(gold_u, kind)
    for mode in ("raw", "dedup_live", "raw_vin", "vin_only", "add_member"):
        alt = A.by_class(A.units_naive(st["log"], mode=mode), kind)
        ok(all(alt[k] != gold_cls[k] for k in gold_cls), "vehicles by class: the %s path misses every class" % mode)
    xf = collections.Counter()
    for u in st["units"]:
        if "transfer" in u and u["transfer"][0] <= D_:
            xf[kind[u["member"]]] -= 1
            xf[kind[u["transfer"][1]]] += 1
    ok(all(xf[k] != 0 for k in gold_cls), "every class gains or loses vehicles by transfer inside the pool")
    rated = W.rated(st["dec"], mem)
    toe_g = collections.Counter()
    for d in rated.values():
        toe_g[d["kind"]] += d["toe"]

    def toe_path(pick, drop_leaver=False):
        by = {}
        for d in st["dec"]:
            if drop_leaver and d["member"] in leaving:
                continue
            by.setdefault(d["member"], []).append(d)
        out = collections.Counter()
        for m_, ds in by.items():
            out[kind[m_]] += pick(ds)
        return out
    paths = {"max per member": lambda ds: max(d["toe"] for d in ds),
             "first declaration": lambda ds: min(ds, key=lambda d: d["submitted"])["toe"],
             "every declaration": lambda ds: sum(d["toe"] for d in ds),
             "every line": lambda ds: sum(d["toe"] * (1 if d["paper"] else len(d["lines"])) for d in ds)}
    for nm, f in paths.items():
        for dl in (False, True):
            alt = toe_path(f, dl)
            ok(all(round(alt[k] / 1000) != round(toe_g[k] / 1000) for k in toe_g),
               "expenditure by class: the %s path misses every class (leaver dropped %s)" % (nm, dl))
    late = toe_path(lambda ds: max(ds, key=lambda d: d["submitted"])["toe"])
    ok(late[kind[min(leaving)]] != toe_g[kind[min(leaving)]] and sum(late.values()) != sum(toe_g.values()),
       "the last declaration with the leaver kept misses its class and the total")
    ok(all(any(d["seq"] == 2 and d["toe"] < min(x["toe"] for x in st["dec"] if x["member"] == d["member"] and x["seq"] == 1)
               for d in st["dec"] if d["kind"] == k) for k in toe_g), "every class has a member whose adopted budget was cut")
    ok(all(any(not d["paper"] and len(d["lines"]) > 1 for d in st["dec"] if d["kind"] == k) for k in toe_g),
       "every class has an online member declaring two or more departments")
    T, U = fig["exposure"]["toe"], fig["exposure"]["units"]
    ok(T == sum(toe_g.values()) and U == sum(gold_u.values()), "the rated totals are the classes' sums")
    wrong_T = [sum(toe_path(f, dl).values()) for f in paths.values() for dl in (False, True)] + [sum(late.values())]
    wrong_U = [sum(A.units_naive(st["log"], mode=m_).values()) for m_ in ("raw", "dedup_live", "add_member")]
    for a in W.OPTIONS:
        good = round(A.premium(T, U, a))
        ok(good == fig["premiums"][str(a)], "premium at %d" % a)
        for t_ in wrong_T:
            ok(round(A.premium(t_, U, a)) != good, "a wrong expenditure path misses the premium at %d" % a)
        for u_ in wrong_U:
            ok(round(A.premium(T, u_, a)) != good, "a wrong vehicle path misses the premium at %d" % a)
    # every wrong route's counts differ from the golden at one decimal at every attachment
    for k in ("R0", "R1", "R2", "R3", "shift", "G_closed", "G_nominal"):
        ok(all(round(lad[k]["counts"][a], 1) != round(g[a], 1) for a in W.OPTIONS), "%s's counts miss at every attachment" % k)
    # the main population holds no ask device: the fit reads no declaration or log row
    ok(fig["call"]["attachment"] == A.pick(A.golden(rec)[3]), "the call reads only the loss runs")

    # ------------------------------------------------------------ distractors: nothing reads them
    for f in meta["distractor_files"]:
        ok(f in (R.DEDHIST, R.TRIANGLES, R.DECL, R.LOG), "distractor %s is one of the four declared" % f)
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
        ok(abs(r[1] - round(fig["counts"][str(r[0])], 1)) < 1e-9, "workbook count at %d" % r[0])
        ok(r[3] == fig["layer_loss_100k"][str(r[0])], "workbook layer loss at %d" % r[0])
    ok(wb.sheetnames == ["Retention 2027", "Notes"], "the workbook's sheets")
    ok(os.path.getsize(os.path.join(golden, G.CHART)) > 20_000, "the chart rendered")
    print("checks: %d assertions, %d failed" % (N[0], len(FAILED)))
    if FAILED:
        raise AssertionError("; ".join(FAILED))

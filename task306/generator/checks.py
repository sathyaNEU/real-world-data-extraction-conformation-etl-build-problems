"""task306's generator checks, run on the cut pack (target/) and the clean truth.

    python3 task306/generator/checks.py
"""
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import pack as PK     # noqa: E402
import world as W     # noqa: E402

FAILS = []
N = [0]


def ok(name, cond, detail=""):
    N[0] += 1
    print(("PASS  " if cond else "FAIL  ") + name + ("" if cond else "   " + str(detail)))
    if not cond:
        FAILS.append(name)


def rounded(res):
    return {c: int(round(res[c]["net"] / 1e6)) for c in res}


def pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join((p.extract_text() or "") for p in PdfReader(path).pages))


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    R = A.run(TARGET)
    P, pr = R["P"], R["priced"]
    gold = rounded(pr["golden"])

    # ------------------------------------------------ input gates
    files = sorted(os.listdir(TARGET))
    ok("gate: 10 or more files", len(files) >= 10, len(files))
    ok("gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    ok("gate: a file of 25,000 rows or more", meta["largest_file"]["rows"] >= 25000, meta["largest_file"])
    ok("gate: two or more distractors named in metadata.json, none named as one in its file name",
       len(meta["distractors"]) >= 2 and not any(re.search("distract|decoy|unused", f) for f in files))
    ok("gate: every file carries a source, a date and a licence",
       all({"source", "date", "license"} <= set(v) for v in meta["files"].values()))

    # ------------------------------------------------ the call and the routes
    ok("C1 the golden gives the GBP 400m to UK Mid Cap Value, runner-up UK Large Cap Quality",
       R["call"] == "MCV" and R["runner"] == "LCQ", (R["call"], R["runner"]))
    gap_m = gold[R["call"]] - gold[R["runner"]]
    size_routes = ["golden", "pooled with band terms", "sqrt by band", "power by band", "binned"]
    for k in size_routes:
        win, run, gap, _r = A.call(pr[k])
        ok("C2 every size-dependent cost curve files the same call and runner-up (%s)" % k,
           win == "MCV" and run == "LCQ" and gap > 1.2e6, (win, run, round(gap / 1e6, 2)))
        ok("C3 every size-dependent cost curve rounds each candidate's alpha kept to the golden's whole million (%s)"
           % k, rounded(pr[k]) == gold, (rounded(pr[k]), gold))
    for k in ["band average (value)", "band average (orders)", "flat 10 bps"]:
        win, run, gap, _r = A.call(pr[k])
        ok("R0 the size-blind route %s files small-cap momentum" % k, win == "SCM" and gap > 1.5e6,
           (win, round(gap / 1e6, 2)))
    net = {c: pr["golden"][c]["net"] / 1e6 for c in pr["golden"]}
    ok("C4 each golden alpha kept sits at least 0.15 from its rounding edge",
       min(abs(v % 1 - 0.5) for v in net.values()) >= 0.15, net)
    gross = {c: pr["golden"][c]["gross"] / 1e6 for c in pr["golden"]}
    ok("C5 the gross alphas are the workbook's own figures times GBP 400m",
       {c: round(v, 2) for c, v in gross.items()} == {"SCM": 20.2, "MCV": 12.08, "LCQ": 7.36}, gross)

    # ------------------------------------------------ the fit family: every defensible curve, weighting and data reading
    ex = R["ex"]
    fam = {}
    for g in (0.4, 0.45, 0.5, 0.55, 0.6, 0.7):
        fam["band by band, participation to the %.2f" % g] = (ex, A.fit_curve(ex, g=g), "skip", R["cands"])
        fam["band by band, no volatility term, %.2f" % g] = (ex, A.fit_curve(ex, g=g, vol=False), "skip", R["cands"])
    for g in (0.4, 0.5, 0.6, 0.7):
        fam["band by band, value-weighted, %.2f" % g] = (ex, A.fit_curve(ex, g=g, weight=True), "skip", R["cands"])
        fam["pooled with band terms, %.2f" % g] = (ex, A.fit_curve(ex, g=g, pooled=True), "skip", R["cands"])
        fam["pooled with band terms, value-weighted, %.2f" % g] = (ex, A.fit_curve(ex, g=g, pooled=True, weight=True),
                                                                   "skip", R["cands"])
    fam["band by band, value-weighted, no volatility term"] = (ex, A.fit_curve(ex, vol=False, weight=True), "skip",
                                                              R["cands"])
    trn = [e for e in ex if not (e["account"] == "WM-DYN-01" and e["date"] >= dt.date(2026, 8, 17))]
    fam["SF15 without the Severnvale transition's orders"] = (trn, A.fit_sqrt_vol(trn), "skip", R["cands"])
    nob = [e for e in trn if e["account"] != "WM-BLOCK-01"]
    fam["SF15 without the transition or the block account"] = (nob, A.fit_sqrt_vol(nob), "skip", R["cands"])
    noc = [e for e in ex if e["status"] != "CANCELLED"]
    fam["SF16 without the orders cancelled part filled"] = (noc, A.fit_sqrt_vol(noc), "skip", R["cands"])
    for mode in ("adjust", "raw"):
        exm = A.with_size(P, A.executions(P), cons=mode)
        fam["SF12 the consolidation day %s" % {"adjust": "with the history before it adjusted",
                                                "raw": "left as a return"}[mode]] = (exm, A.fit_sqrt_vol(exm), mode,
                                                                                    R["cands"])
    import csv
    esg_rows = list(csv.DictReader(open(os.path.join(TARGET, PK.FILES["esg"]), encoding="utf-8")))
    esg = {r["isin"] for r in esg_rows}
    no_esg = {k: dict(c, trades=[t for t in c["trades"] if P.master[t[1]]["isin"] not in esg])
              for k, c in R["cands"].items()}
    fam["SF14 the ESG-listed names dropped from the rebalances"] = (ex, A.fit_sqrt_vol(ex), "skip", no_esg)
    lo, hi, bad = {c: 99.0 for c in gold}, {c: -99.0 for c in gold}, []
    blo, bhi = dict(lo), dict(hi)
    for label, (rows_, model, mode, cands) in fam.items():
        res = A.price(P, cands, model, cons=mode)
        win, run, gap, _r = A.call(res)
        for c in gold:
            v = res[c]["net"] / 1e6
            lo[c], hi[c] = min(lo[c], v), max(hi[c], v)
            if "pooled" not in label:                     # band by band: the population IC-07 files
                blo[c], bhi[c] = min(blo[c], v), max(bhi[c], v)
        if not (rounded(res) == gold and (win, run) == (R["call"], R["runner"]) and round(gap / 1e6) == gap_m):
            bad.append((label, {c: round(res[c]["net"] / 1e6, 2) for c in res}))
    ok("C7 every member of the fit family (%d: exponents 0.4 to 0.7 with and without the volatility term, band by "
       "band and pooled with band terms, unweighted and value-weighted, without the transition, the block account or "
       "the cancelled orders, either consolidation reading, the ESG names dropped) files the golden's call, runner-up, "
       "gap and every rounded figure" % len(fam), not bad, bad)
    bspan = {c: (round(float(blo[c]), 2), round(float(bhi[c]), 2)) for c in gold}
    span = {c: (round(float(lo[c]), 2), round(float(hi[c]), 2)) for c in gold}
    ok("C8 band by band (IC-07's population) each alpha kept stays at least 0.25 inside the golden's whole million: "
       "%s" % bspan, all(blo[c] - (gold[c] - 0.5) >= 0.25 and (gold[c] + 0.5) - bhi[c] >= 0.25 for c in gold), bspan)
    ok("C8 with the pooled fits too, at least 0.2 inside: %s" % span,
       all(lo[c] - (gold[c] - 0.5) >= 0.2 and (gold[c] + 0.5) - hi[c] >= 0.2 for c in gold), span)
    ok("SF14 the ESG list is inert: every exclusion took effect before the rebalance log and the desk's orders begin, "
       "and no rebalance trade is in an excluded name",
       all(r["effective"] < "2025-01-02" for r in esg_rows)
       and not any(r["isin"] in esg for r in A.rows(TARGET, "trades")), len(esg_rows))
    first = min(e["date"] for e in ex)
    ok("SF13 every order has the full 60 sessions of history the TCA standard measures on",
       P.day_ix[first] >= 60 and min(P.day_ix[t[0]] for c in R["cands"].values() for t in c["trades"]) >= 60,
       (first, P.day_ix[first]))

    # the clean truth: the world's own impact law on the same trades
    univ = {s["sedol"]: s for s in W.universe()}
    tr = {}
    for code, c in R["cands"].items():
        cost = 0.0
        for d, s, w in c["trades"]:
            adv, vol = P.adv_vol(s, d)
            v = abs(w) * A.AUM
            cost += v * W.cost_bps(univ[s], v / adv, vol) / 1e4
        tr[code] = c["alpha"] * A.AUM - cost
    ok("C6 on the clean truth (the world's impact law) the call and every rounded figure are the golden's",
       {c: int(round(v / 1e6)) for c, v in tr.items()} == gold, {c: round(v / 1e6, 2) for c, v in tr.items()})

    # ------------------------------------------------ the fork rows
    alt = {}
    for label, kw in (("SF1 participation on 60 sessions' traded value", dict(adv_n=60)),
                      ("SF2 volatility over 250 sessions", dict(vol_n=250))):
        ex2 = A.with_size(P, A.executions(P), **kw)
        m2 = A.fit_sqrt_vol(ex2)
        alt[label] = A.price(P, R["cands"], m2, **kw)
        ok(label + ": same call and rounded figures", rounded(alt[label]) == gold, rounded(alt[label]))
    vw = A.price(P, R["cands"], A.fit_curve(ex, weight=True))
    ok("SF3 the curve fitted value-weighted, band by band: same call and rounded figures (the whole family is C7)",
       rounded(vw) == gold, rounded(vw))
    one = A.price(P, R["cands"], A.fit_curve(ex, pooled=True))
    ok("SF11 one curve pooled over the bands with an intercept per band: same call and rounded figures",
       rounded(one) == gold, rounded(one))
    for label, kw in (("SF4 the fit without merging the failover orders", dict(failover=False)),
                      ("SF5 the fit with the re-sent fills kept twice", dict(dedupe=False))):
        exk = A.with_size(P, A.executions(P, **kw))
        pk = A.price(P, R["cands"], A.fit_sqrt_vol(exk))
        ok(label + ": same call and rounded figures", rounded(pk) == gold, rounded(pk))
    exu = A.with_size(P, A.executions(P, units=False))
    bad = sum(1 for e in exu if abs(e["shortfall"]) > 5000)
    ok("SF6 a pounds fill read as pence shows at once (shortfalls near minus 10,000 bps)", bad > 100, bad)
    wb = __import__("openpyxl").load_workbook(os.path.join(TARGET, PK.FILES["backtests"]), read_only=True)
    ann = list(wb["Annual alpha"].iter_rows(values_only=True))[1:]
    geo = {}
    for j, code in enumerate(["SCM", "MCV", "LCQ"]):
        xs = [float(str(r[j + 1]).rstrip("%")) / 100 for r in ann]
        geo[code] = math.prod(1 + x for x in xs) ** (1 / len(xs)) - 1
    ok("SF7 the annual alphas compound to the Summary's annualised gross alpha (no second reading of 'expected "
       "gross alpha')", all(abs(geo[k] - R["cands"][k]["alpha"]) < 0.0006 for k in geo), geo)
    cal = A.WINDOW
    ok("SF8 the twelve months to 30 November 2026 hold every candidate's rebalances, twelve monthly and four "
       "quarterly", [pr["golden"][k]["rebalances"] for k in ("SCM", "MCV", "LCQ")] == [12, 4, 4],
       [pr["golden"][k]["rebalances"] for k in ("SCM", "MCV", "LCQ")])
    pol = pdf_text(os.path.join(TARGET, PK.FILES["policy"]))
    tca = pdf_text(os.path.join(TARGET, PK.FILES["tca"]))
    ok("SF9 IC-07 files the estimand: gross alpha less the shortfall of the twelve months' rebalances at the size "
       "allocated, traded in full on the day, estimated on the desk's executions in the candidate's index band (SF11), "
       "commissions and the launch build outside",
       all(s in pol for s in ("annualised gross alpha", "twelve months to 30 November 2026",
                              "traded in full on the rebalance day", "estimated from the desk's own executions",
                              "in stocks of the index band the candidate trades",
                              "Commissions are paid from the research budget", "outside it")), pol[:200])
    ok("SF10 the TCA standard files shortfall, value, participation, the failover rule, the dated register, the "
       "consolidation day (SF12) and the 60-session history (SF13)",
       all(s in tca for s in ("signed so that a cost is positive", "filled quantity at its arrival mid",
                              "over the 20 sessions before its trade date", "is the original order",
                              "account codes the trading account register gives it on the trade date",
                              "consolidation or split takes effect gives no return",
                              "60 sessions of history before its trade date")))
    plant = re.compile(r"square root|sqrt|impact|capacity|scal(es|ing) with|rises with|larger orders|size of the "
                       r"order", re.I)
    ok("R1 no document names how cost grows with size", not plant.findall(pol + " " + tca), plant.findall(pol + tca))

    # ------------------------------------------------ the asks
    ga, gb = R["ask_a"], R["ask_b"]
    nf = A.allocated(P, A.with_size(P, A.executions(P, failover=False)))
    a_nf = A.ask_shortfall(P, nf)
    moved = sum(round(a_nf[k], 1) != round(ga[k], 1) for k in ga)
    ok("ask A: the failover orders left unmerged move at least 12 of the 16 shortfall cells", moved >= 12, moved)
    alx = A.allocated(P, R["ex"])
    a_ud, b_ud = A.ask_shortfall(P, alx, dated=False), A.ask_traded(P, alx, dated=False)
    a_nb, b_nb = A.ask_shortfall(P, R["ex"]), A.ask_traded(P, R["ex"])
    ok("ask A/B: the block orders left unallocated move every traded cell and most shortfall cells",
       sum(round(b_nb[k] / 1e6) != round(gb[k] / 1e6) for k in gb) == 8
       and sum(round(a_nb[k], 1) != round(ga[k], 1) for k in ga) >= 12,
       (sum(round(b_nb[k] / 1e6) != round(gb[k] / 1e6) for k in gb), sum(round(a_nb[k], 1) != round(ga[k], 1)
                                                                        for k in ga)))
    ok("ask A/B: the register read undated moves UK Dynamic's second-half cells",
       round(a_ud[("UK Dynamic", 4)], 1) != round(ga[("UK Dynamic", 4)], 1)
       and round(b_ud[("UK Dynamic", 2)] / 1e6) != round(gb[("UK Dynamic", 2)] / 1e6))
    ok("ask A: every shortfall cell clear of its rounding edge by 0.005 of a tenth",
       min(abs((v * 10) % 1 - 0.5) for v in ga.values()) >= 0.005)
    ok("ask B: every traded cell clear of its rounding edge by 0.005 of a million",
       min(abs((v / 1e6) % 1 - 0.5) for v in gb.values()) >= 0.005)
    ok("figures.json matches the golden run", fig["call"] == R["call"] and
       {k: v["net_gbp_m"] for k, v in fig["candidates"].items()} == gold)
    zp = os.path.join(TASK, "target.zip")
    if os.path.exists(zp):
        ok("target.zip holds exactly the pack's files", sorted(zipfile.ZipFile(zp).namelist()) == files)
    print("%d checks, %d failed" % (N[0], len(FAILS)))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()

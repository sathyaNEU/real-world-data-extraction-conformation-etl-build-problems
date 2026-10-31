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
    size_routes = ["golden", "sqrt by band", "power by band", "binned"]
    for k in size_routes:
        win, run, gap, _r = A.call(pr[k])
        ok("C2 every size-dependent cost curve files the same call and runner-up (%s)" % k,
           win == "MCV" and run == "LCQ" and gap > 1.2e6, (win, run, round(gap / 1e6, 2)))
        if k != "binned":
            ok("C3 every parametric cost curve rounds each candidate's alpha kept to the golden's whole million (%s)" % k,
               rounded(pr[k]) == gold, (rounded(pr[k]), gold))
    for k in ["band average (value)", "band average (orders)", "flat 10 bps"]:
        win, run, gap, _r = A.call(pr[k])
        ok("R0 the size-blind route %s files small-cap momentum" % k, win == "SCM" and gap > 1.5e6,
           (win, round(gap / 1e6, 2)))
    net = {c: pr["golden"][c]["net"] / 1e6 for c in pr["golden"]}
    ok("C4 each golden alpha kept sits at least 0.15 from its rounding edge",
       min(abs(v % 1 - 0.5) for v in net.values()) >= 0.15, net)
    gross = {c: pr["golden"][c]["gross"] / 1e6 for c in pr["golden"]}
    ok("C5 the gross alphas are the workbook's own figures times GBP 400m",
       {c: round(v, 2) for c, v in gross.items()} == {"SCM": 20.24, "MCV": 11.6, "LCQ": 7.2}, gross)

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
    ex = R["ex"]
    import numpy as np
    X = np.array([[1.0 if e["tier"] == t else 0.0 for t in "LMS"] + [e["vol"] * math.sqrt(e["part"])] for e in ex])
    y = np.array([e["shortfall"] for e in ex])
    wv = np.sqrt(np.array([e["value"] for e in ex]))
    c, *_ = np.linalg.lstsq(X * wv[:, None], y * wv, rcond=None)
    aa = dict(zip("LMS", c[:3]))
    vw = A.price(P, R["cands"], lambda t, p, v: aa[t] + c[3] * v * math.sqrt(p))
    ok("SF3 the curve fitted value-weighted: same call and rounded figures", rounded(vw) == gold, rounded(vw))
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
       "allocated, traded in full on the day, commissions and the launch build outside",
       all(s in pol for s in ("annualised gross alpha", "twelve months to 30 November 2026",
                              "traded in full on the rebalance day", "estimated from the desk's own executions",
                              "Commissions are paid from the research budget", "outside it")), pol[:200])
    ok("SF10 the TCA standard files shortfall, value, participation, the failover rule and the dated register",
       all(s in tca for s in ("signed so that a cost is positive", "filled quantity at its arrival mid",
                              "over the 20 sessions before its trade date", "is the original order",
                              "account codes the trading account register gives it on the trade date")))
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

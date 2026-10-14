"""Every assertion the design note's Build record asks for, on the shipped bundle (target/) and the generator's world.

    python3 task134/generator/checks.py
"""
import datetime as dt
import itertools
import json
import os
import re
import subprocess
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import askcalc as AC
import asktune as AT
import estimators as E
import golden as G
import readpack as RP
import sim
import tune
import world as W

TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
N = [0]
FAILS = []


def ok(cond, msg):
    N[0] += 1
    if not cond:
        FAILS.append(msg)
        print("FAIL  " + msg)
    else:
        print("ok    " + msg)


def r10(x):
    return np.floor(np.asarray(x) / 10.0 + 0.5) * 10


def same_bin(a, b):
    return bool(np.all(r10(a) == r10(b)))


def edge_dist(x):
    x = np.asarray(x)
    return np.abs(x - (np.floor(x / 10.0 + 0.5) * 10)) * -1 + 5


def doc_text():
    """the text of every document and workbook in the pack"""
    from pypdf import PdfReader
    import docx
    import openpyxl
    out = {}
    for f in sorted(os.listdir(TGT)):
        p = os.path.join(TGT, f)
        if f.endswith(".docx"):
            out[f] = "\n".join(x.text for x in docx.Document(p).paragraphs)
        elif f.endswith(".pdf"):
            out[f] = "\n".join(pg.extract_text() for pg in PdfReader(p).pages)
        elif f.endswith(".txt"):
            out[f] = open(p, encoding="utf-8").read()
        elif f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(p, read_only=True)
            out[f] = "\n".join(" ".join(str(v) for v in r if v is not None) for ws in wb.worksheets
                               for r in ws.iter_rows(values_only=True))
    return out


def three_rules(T, I, g, rungs, tot, figs):
    """R1 the field's raw material ships; R2 every mess item is neutral to the call; R3a the easy route with every filed
    rule executed files the named wrong answer; R3b changing only the decisive step files the answer; R3c nothing planted"""
    files = sorted(os.listdir(TGT))
    hdr = []
    for f in files:
        if f.endswith((".csv", ".tsv")):
            hdr += list(pd.read_csv(os.path.join(TGT, f), nrows=0, sep="\t" if f.endswith(".tsv") else ",").columns)
    ok(not any(re.search(r"capital|drawdown|hazard|forecast|conversion|census|weeks|probab|expected", c.lower()) for c in hdr),
       "R1: no shipped column holds a capital, a drawdown, a hazard, a conversion count or a forecast")
    li = T["li"]
    ok({"admitted", "award_start", "award_end", "end_reason"} <= set(li.columns) and len(li["debtor_ref"].unique()) >= 2000,
       "R1: the payment lines carry each of %d self-funders' admission and award end with its reason (censored durations)"
       % len(li["debtor_ref"].unique()))
    m = g["measure"]
    n52 = int(round(m["flow"] * 52))
    ok(m["on_day"] >= 6 and n52 >= 70, "R1: the stage-1 response is read from %d conversions on 6 April 2026 against %d in the "
       "52 weeks before" % (m["on_day"], n52))
    Tn = dict(T)
    Tn["li"] = T["li"].iloc[:0]
    In, _, _ = RP.inputs(Tn["pl"], Tn["li"], Tn["cw"], Tn["dl"])
    ok(len(In["sf_admit"]) == 0, "R1: without the payment lines there is no self-funding pool to forecast from")
    # R2: the Layer 1 items, each mishandled in the natural way, leave the call where it was
    Tx = dict(T)
    Tx["dl"] = T["dl"][T["dl"]["match_status"] == "EXACT"]
    Ix, _, _ = RP.inputs(Tx["pl"], Tx["li"], Tx["cw"], Tx["dl"])
    ok(np.allclose(E.golden(Ix)["total"], tot, atol=1e-9), "R2: deaths matched EXACT only keep the call")
    Tl = dict(T)
    Tl["li"] = T["li"][T["li"]["line_type"].isin(["FPC", "FNC"])]
    Il, _, _ = RP.inputs(Tl["pl"], Tl["li"], Tl["cw"], Tl["dl"])
    ok(np.allclose(E.golden(Il)["total"], tot, atol=1e-9), "R2: the adjustment and hospital-reduction lines dropped keep the call")
    Tsv = dict(T)
    Tsv["pl"] = T["pl"].copy()
    Tsv["pl"]["service_no"] = "CS0000000000"
    Isv, _, _ = RP.inputs(Tsv["pl"], Tsv["li"], Tsv["cw"], Tsv["dl"])
    ok(np.allclose(E.golden(Isv)["total"], tot, atol=1e-9), "R2: the re-registered homes' service numbers (every service number blanked) keep the call")
    Tp = dict(T)
    Tp["li"] = T["li"].copy()
    Tp["li"]["period"] = "P"
    Ip, _, _ = RP.inputs(Tp["pl"], Tp["li"], Tp["cw"], Tp["dl"])
    ok(np.allclose(E.golden(Ip)["total"], tot, atol=1e-9), "R2: the four-weekly payment calendar keeps the call")
    # R3a: the easy route, every filed rule executed (the definitions' population and dates, the limits read but the history's
    # hazard projected as fitted), files the default
    ok(np.all(r10(rungs["R5"]) != r10(tot)) and np.all(tot - rungs["R5"] >= 15),
       "R3a: the easy route with every filed rule executed files %s against %s"
       % (r10(rungs["R5"]).astype(int).tolist(), r10(tot).astype(int).tolist()))
    # R3b: the same pipeline with only the decisive step changed files the answer; each half-step leaves it off
    r5b = E.golden(I, w1=0.0, apply1=False)["total"]
    ok(np.abs(r5b - rungs["R5"]).max() < 0.05, "R3b: the canonical pipeline with no capital-limit step is the default (%.3f)" % np.abs(r5b - rungs["R5"]).max())
    for k, lab in (("R6", "the day's count repeated"), ("R7", "the day's count scaled by the rise"), ("R9", "the clocks moved on, nobody converting that day")):
        ok(np.all(r10(rungs[k]) != r10(tot)), "R3b: %s (%s) alone leaves the easy route off the answer" % (k, lab))
    # R3c: nothing planted
    ok(not any(re.search(r"memo|draft_budget|briefing|forecast|census|prior|outturn", f.lower()) for f in files),
       "R3c: no memo, briefing, prior forecast or census in the pack")
    texts = doc_text()
    allt = " ".join(texts.values())
    for q in W.QLABEL:
        v = str(figs["call"][q]["stated"])
        ok(re.search(r"(?<![\d.,£])%s\s+(council|residents|people|placements|funded)" % v, allt) is None,
           "R3c: no document states %s residents" % v)
    pl = T["pl"].drop(columns=["placement_id", "client_id"])
    ok(pl.duplicated().sum() <= 0.003 * len(pl), "R3c: the placements repeat no block of rows (%d coincident episodes)" % pl.duplicated().sum())
    l2 = T["li"].drop(columns=["debtor_ref"])
    ok(l2.duplicated().sum() <= 0.01 * len(l2), "R3c: the payment lines repeat no block of rows (%d coincident lines)" % l2.duplicated().sum())


def main():
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    T, I, g, rungs, ask, counts, stops = G.compute(TGT)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    tot = g["total"]
    golden = tot

    # ---------------------------------------------------------------- input gates
    files = sorted(os.listdir(TGT))
    ok(len(files) == 14, "input gate: 14 files (%d)" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(fmts) >= 3, "input gate: %d formats %s" % (len(fmts), sorted(fmts)))
    nl = len(T["li"])
    ok(nl >= 25000, "input gate: the spine fpnc_payment_lines has %d rows (25,000 or more)" % nl)
    ok(len(meta["distractors"]) >= 2 and all(d in files for d in meta["distractors"]),
       "input gate: %d distractors named in metadata.json and present" % len(meta["distractors"]))
    ok(not any("distractor" in f.lower() for f in files), "no file name says distractor")
    ok(set(meta["deliverables"]) == {G.XLSX, G.PNG}, "metadata names the two deliverables")
    # distractors unused: the golden and the ask recompute with them deleted
    import shutil
    import tempfile
    tmp = tempfile.mkdtemp()
    for f in files:
        if f not in meta["distractors"]:
            shutil.copy(os.path.join(TGT, f), tmp)
    T2, I2, g2, _, ask2, _, _ = G.compute(tmp)
    shutil.rmtree(tmp)
    ok(np.allclose(g2["total"], tot) and np.allclose(AC.vec(ask2), AC.vec(ask)),
       "distractors deleted: the call and the 20 ask figures unchanged")
    offer_txt = doc_text()["nchc_draft_offer_2027-28.pdf"]
    ok("has not been agreed" in offer_txt, "the draft offer says it is not agreed (wrong-basis distractor ruled out)")
    draft_net = []
    for loc in W.LOCS:
        for ct, k in (("Residential", 0), ("Nursing", 1)):
            draft_net.append(ask[(loc, ct)][1] + W.NCHC_DRAFT_2027[k] - W.NCHC[2026][k])
    ok(np.all(np.abs(np.array(draft_net) - AC.vec(ask)[1::2]) >= 1.5), "the draft-offer read moves every net cell by 1.5 or more")

    # ---------------------------------------------------------------- the golden
    stated = np.array([figs["call"][q]["stated"] for q in W.QLABEL])
    ok(np.all(stated == r10(tot)), "figures.json carries the call as computed: %s" % stated.tolist())
    ok(np.all(edge_dist(tot) >= 2.0), "every golden figure at least 2.0 from a bin edge: %s" % np.round(edge_dist(tot), 2).tolist())
    ok(np.all(np.abs(tot - np.round(tot)) > 0.01), "no golden figure is a whole number before rounding %s" % np.round(tot, 2).tolist())
    ok(np.all(np.diff(tot) > 0), "the forecast rises through the year")
    m = g["measure"]
    ok(m["on_day"] == figs["stage_1"]["conversions_that_day"] and abs(g["w1"] - figs["stage_1"]["weeks"]) < 0.006
       and abs(g["w2"] - figs["stage_2"]["weeks"]) < 0.006,
       "the 6 April 2026 rise: %d conversions that day against %.3f a week, %.2f weeks; 5 April 2027 %.2f weeks"
       % (m["on_day"], m["flow"], g["w1"], g["w2"]))

    # ---------------------------------------------------------------- three rules
    three_rules(T, I, g, rungs, tot, figs)

    # ---------------------------------------------------------------- the ladder
    names = ("R0", "R1", "R1b", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10")
    for k in names:
        ok(not np.allclose(rungs[k], tot, atol=0.5), "rung %s on its own vector %s" % (k, np.round(rungs[k], 1).tolist()))
    for k in ("R0", "R1", "R1b", "R2", "R3"):
        ok(tot[3] - rungs[k][3] >= 25, "rung %s at least 25 below at 31 March 2028 (%.1f)" % (k, tot[3] - rungs[k][3]))
        ok(np.all(r10(rungs[k]) != r10(tot)), "rung %s outside the golden's bin at every quarter end" % k)
    ok(np.all(r10(rungs["R5"]) != r10(tot)) and np.all(tot - rungs["R5"] >= 15),
       "the default R5 (the hazard by months since admission as fitted) at least 15 below and outside the golden's bin at "
       "every quarter end %s (thinnest %.1f)" % (np.round(rungs["R5"], 1).tolist(), (tot - rungs["R5"]).min()))
    ok(np.all(np.abs(r10(rungs["R5"]) - r10(tot)) >= 20), "the default files a different figure at every quarter end, two bins or more from the golden's")
    for k in ("R6", "R7", "R9"):
        ok(np.all(r10(rungs[k]) != r10(tot)) and np.all(rungs[k] < tot),
           "rung %s below the golden and outside its bin at every quarter end %s" % (k, np.round(rungs[k], 1).tolist()))
    ok(np.sum(r10(rungs["R8"]) != r10(tot)) >= 3, "rung R8 (the jump with no clock moved on) outside the golden's bin at 3 or more quarter ends")
    ok(np.sum(r10(rungs["R4"]) != r10(tot)) >= 3 and rungs["R4"][3] - tot[3] >= 15,
       "rung R4 (exits censored) outside the golden's bin at 3 or more quarter ends and 15 or more above at 31 March 2028 (%.1f)"
       % (rungs["R4"][3] - tot[3]))
    ok(np.all(rungs["R10"] < tot), "rung R10 (the 2027 jump alone) below the golden at every quarter end %s" % np.round(rungs["R10"] - tot, 1).tolist())
    vecs = [tuple(r10(rungs[k])) for k in names]
    ok(tuple(r10(tot)) not in vecs, "no rung lands on the golden's four stated figures")
    cy = figs["conversions_by_year"]
    vals = [cy[str(y)] for y in range(2021, 2027)]
    ok(len(set(vals)) == len(vals), "conversions by year not identical %s" % vals)

    # ---------------------------------------------------------------- the golden family
    fam = [dict(lo=W.dn(dt.date(2022, 4, 1))), dict(lo=W.dn(dt.date(2023, 4, 1))), dict(lo=W.dn(dt.date(2022, 1, 1))),
           dict(lo=W.dn(dt.date(2023, 1, 1))), dict(band=3.0), dict(band=6.0), dict(step=0.25), dict(exits="care"),
           dict(clock="cal"), dict(sf_clock="award"), dict(post_asof_sf=True), dict(adm_window=(2021, 2026)),
           dict(adm_window=(2026, 2026)), dict(adm_window=(2022, 2026)), dict(cf_clock="entry"),
           dict(band=3.0, exits="care"), dict(step=0.25, clock="cal"), dict(drift=W.SF_FEE_GROWTH), dict(fit_on="capital"),
           dict(how="model"), dict(how="year"), dict(how="after", weeks=26), dict(how="around", weeks=26)]
    fam += [dict(weeks=k) for k in (4, 8, 12, 13, 26)]
    fam += [dict(w1=g["measure"]["on_day"] / g["measure"]["flow"])]       # the day's count over a week, no day subtracted
    worst = 0
    for kw in fam:
        v = E.golden(I, **kw)["total"]
        worst = max(worst, np.abs(v - tot).max())
        ok(same_bin(v, tot) and np.all(edge_dist(v) >= 0.3),
           "golden family %s in the bin at every date %s" % (kw, np.round(v, 1).tolist()))
    print("      golden family: widest move %.2f" % worst)
    pa = E.golden(I, post_asof_sf=True)["total"]
    ok(abs(pa[3] - tot[3]) < 1.5, "self-funders admitted after the as-of date move 31 March 2028 by under 1.5 (%.2f)" % (pa[3] - tot[3]))
    # the simulated world and the stock
    S = sim.simulate(W.SEED)
    rec = json.load(open(os.path.join(HERE, "build_record.json")))
    tune.apply_flow(S, [tuple(m) for m in rec["flow_moves"]])
    tune.apply(S, [tuple(m) for m in rec["centring_moves"]])
    import observe as OB
    lag0 = OB.ask_attributes(S, None, np.random.default_rng(W.SEED + 404)).lag0
    unrec = int(((S.conv <= W.ASOF) & (S.conv + lag0 > W.EXTRACT) & (S.exit > W.ASOF)).sum())
    ok(int(sim.cf_on(S, W.ASOF).sum()) - unrec == g["n_cf"],
       "the as-of stock read from the files (%d) is the timeline's less the %d conversions not yet recorded" % (g["n_cf"], unrec))
    outcome = np.array([int(sim.cf_on(S, q).sum()) for q in W.QEND])
    ok(np.all(np.abs(outcome - tot) < np.abs(outcome - rungs["R5"])),
       "the simulated outcome %s sits nearer the golden than the default at every quarter end" % outcome.tolist())
    conv27 = int(((S.conv >= W.dn(dt.date(2027, 1, 1))) & (S.conv < W.dn(dt.date(2028, 1, 1)))).sum())
    on27 = int((S.conv == W.STAGE2).sum())
    print("      simulated conversions in 2027: %d, %d on 5 April 2027 (the register's 2024 to 2026: %s)"
          % (conv27, on27, [figs["conversions_by_year"][str(y)] for y in (2024, 2025, 2026)]))
    # the ordinary week: every natural window gives the stage-1 response within 0.45 of a week
    fr_ = E.fit(I)
    ws_ = [E.measure(I, k, "before")["w1"] for k in (4, 8, 12, 13, 26, 52)] + [E.measure(I, k, "after")["w1"] for k in (8, 12, 26)]
    ws_ += [E.measure(I, 0, "year")["w1"], E.measure(I, 0, "model", fr_)["w1"]]
    ok(max(ws_) - min(ws_) <= 0.65, "the stage-1 response from every natural ordinary-week window: %.2f to %.2f weeks" % (min(ws_), max(ws_)))
    # every earlier first Monday of April is an ordinary day: the limits were frozen
    cd = E.conv_days(I)
    others = [int((cd == W.uprate_day(y)).sum()) for y in range(2021, 2026)]
    ok(max(others) <= 2, "the first Mondays in April 2021 to 2025 are ordinary days %s" % others)

    # ---------------------------------------------------------------- semantic forks
    defs = doc_text()["care_home_budget_definitions_2027-28.docx"]
    quotes = {
        "SF1": "Self-funding residents who receive free personal care or free nursing care payments are not council-funded residents",
        "SF2": "Respite, short-break and interim placements are excluded",
        "SF3": "in place at the end of that day",
        "SF4": "including residents temporarily in hospital and residents placed in care homes outside Strathallan",
        "SF5": "including residents temporarily in hospital",
        "SF7": "a decision recorded after a date but effective on or before it counts on that date",
        "SF8": "counted once",
        "SF12": "whenever they were admitted",
    }
    for k, q in quotes.items():
        ok(q in defs, "%s: the ruling sentence is in the budget definitions" % k)
    alt = {}
    # SF1: self-funders on free personal and nursing care counted as council-funded
    on = E.pool(I)
    o, HX, HC, HS = g["o"], g["HX"], g["HC"], g["HS"]
    d0 = E.months(I["sf_admit"][on], np.full(on.sum(), W.ASOF))
    qm = E.qmonths("days")
    sf_surv = np.array([np.exp(-(HX[0].H(d0 + q) - HX[0].H(d0))).sum() for q in qm])
    alt["SF1"] = tot + sf_surv
    # SF2: interim and respite placements kept
    I2, st2, _ = RP.inputs(T["pl"], T["li"], T["cw"], T["dl"], types=("PERM", "INT", "RESP"))
    I2["cf_route"] = np.where(I2["cf_route"] == "", "DIRECT", I2["cf_route"])
    alt["SF2"] = E.golden(I2)["total"]
    # SF3: anyone placed at any time in the quarter
    q0 = W.dn(dt.date(2026, 10, 1))
    e, x = I["cf_entry"], I["cf_exit"]
    extra = ((e <= W.ASOF) & (x > q0 - 1)).sum() - ((e <= W.ASOF) & (x > W.ASOF)).sum()
    alt["SF3"] = tot + extra
    # SF4: homes in Strathallan only
    regs = set(T["reg"]["service_no"])
    st = RP.stays(T["pl"], T["cw"], T["dl"])
    ooa = np.array([s["rows"][-1].service_no not in regs for s in st])
    I4 = {k: (v[~ooa] if k.startswith("cf_") else v) for k, v in I.items()}
    alt["SF4"] = E.golden(I4)["total"]
    # SF7: a conversion counted from the date it was recorded
    _, deb = RP.resolver(T["cw"])
    a = T["ass"]
    late = set()
    for r in a.itertuples(index=False):
        if r.outcome in ("ASSESSED", "NIL") and RP.day(r.completed) > W.ASOF and RP.day(r.effective_from) <= W.ASOF:
            late.add((deb.get(r.debtor_ref), RP.day(r.effective_from)))
    lateconv = np.array([(s["cl"], s["entry"]) in late and s["route"] == "CONV" for s in st])
    ok(lateconv.sum() >= 1, "SF7: %d conversions effective in December 2026 were recorded in January 2027" % lateconv.sum())
    I7 = {k: (v[~lateconv] if k.startswith("cf_") else v) for k, v in I.items()}
    v7 = E.golden(I7)["total"]
    ok(np.abs(v7 - tot).max() <= 5, "SF7: counting them from the recorded date gives %s (%s, under 5 at every date); refused by definitions 1.2"
       % (np.round(v7, 1).tolist(), "same call" if same_bin(v7, tot) else "another call"))
    # SF12: today's residents and their survival only
    alt["SF12"] = g["survivors"]
    for k, v in alt.items():
        ok(not same_bin(v, tot), "%s: the alternative reading lands elsewhere %s and is refused by the quoted sentence" % (k, np.round(v, 1).tolist()))
    # SF5, SF6, SF8, SF9, SF10, SF11: the same call
    ok(set(T["pl"]["end_reason"]) <= {"", "FEE", "MOVE", "SVC", "DIED", "DISCH", "ENDED"}, "SF5: the register carries no absence episodes")
    perm = T["pl"][T["pl"]["placement_type"] == "PERM"]
    ok(set(perm["route"]) == {"DIRECT", "CONV"}, "SF6: every long-stay placement is one Strathallan funds (route DIRECT or CONV)")
    overl = 0
    by = {}
    for s in RP.stays(T["pl"], T["cw"], T["dl"], types=("PERM", "INT", "RESP")):
        by.setdefault(s["cl"], []).append((s["entry"], s["exit"]))
    for cl, ivs in by.items():
        ivs.sort()
        for (a1, b1), (a2, b2) in zip(ivs, ivs[1:]):
            if a2 < b1:
                overl += 1
    ok(overl == 0, "SF8: no person has two placements in place at the end of any day")
    ok([W.dd(q).isoformat() for q in W.QEND] == ["2027-06-30", "2027-09-30", "2027-12-31", "2028-03-31"], "SF9: the four dates")
    cut = "2026-12-31"
    late_dates = 0
    for col in ("admitted", "start_date", "end_date"):
        late_dates += (T["pl"][col] > cut).sum()
    for col in ("admitted", "award_start", "period_start", "period_end", "award_end"):
        late_dates += (T["li"][col] > cut).sum()
    late_dates += (T["dl"]["date_of_death"] > cut).sum()
    ok(late_dates == 0, "SF10: no admission, placement date, payment period or death after 31 December 2026")
    comp = np.array([[figs["components"][q][k] for k in ("today_residents", "direct_admissions", "conversions")] for q in W.QLABEL])
    ok(same_bin(np.round(comp).sum(axis=1), tot), "SF11: components rounded to whole residents first land in the same bins")
    texts_ = doc_text()
    pol = " ".join(texts_["charging_policy_2026-27.pdf"].split())
    ok("from 5 April 2027 the limits will be £25,000 and £40,750" in pol and "Capital limits from 6 April 2026" in pol,
       "SF13: the 5 April 2027 limits are a record before the cut, in the charging policy of April 2026 (3.2); "
       "leaving them out is the default R5, outside the bin")
    from pypdf import PdfReader
    pdate = str(PdfReader(os.path.join(TGT, "charging_policy_2026-27.pdf")).metadata.get("/CreationDate", ""))
    ok(pdate.startswith("D:2026"), "SF13: the charging policy is dated %s, before the records' cut" % pdate[:10])
    cv = [s for s in st if s["route"] == "CONV" and s["entry"] == W.STAGE1]
    aw_end = {deb.get(r): RP.day(row["award_end"]) for r, row in T["li"].groupby("debtor_ref").first().iterrows()
              if row["end_reason"] == "CF"}
    ok(len(cv) == m["on_day"] and all(aw_end.get(s["cl"]) == W.STAGE1 - 1 for s in cv),
       "SF14: the %d conversions of 6 April 2026 start that day in the register and end their awards the day before; "
       "every quarter end falls after 5 April 2027, so the day a rise's conversions count from moves no figure" % len(cv))
    ok("3.2 Weekly fee: the weekly fee payable under the placement's contract" in " ".join(defs.split()),
       "SF15: the fee is the one payable under the placement's contract (definitions 3.2)")
    rt_ = texts_["nchc_rates_2021-22_to_2026-27.xlsx"]
    ok("Agreed nationally 06/11/2026" in rt_ and "Interim, 1.5% on 2025-26, pending national agreement" in rt_,
       "SF15: the contract rate table holds the 2026-27 rate agreed on 6 November 2026 beside the interim rate")
    notes_ = texts_["extract_notes_2027-01-18.txt"]
    ok("the locality team whose caseload the resident is on" in notes_,
       "SF16: the placement's locality is filed as the team holding the case; the ask names the localities' care homes")

    # ---------------------------------------------------------------- C1 convergences
    evd = 0
    for col in ("start_date", "end_date", "admitted"):
        evd += (perm[col] == cut).sum()
    evd += ((T["li"]["award_end"] == cut)).sum()
    ok(evd == 0, "C1: nothing starts, ends or converts on 31 December 2026")
    li = T["li"]
    refs_per_client = {}
    for ref in li["debtor_ref"].unique():
        refs_per_client.setdefault(deb.get(ref, ref), set()).add(ref)
    ok(all(len(v) == 1 for v in refs_per_client.values()), "C1: one payment-line history per person (one pool member per person)")
    aw = li.groupby("debtor_ref").first()
    cf_end = {deb.get(r): RP.day(row["award_end"]) + 1 for r, row in aw.iterrows() if row["end_reason"] == "CF"}
    conv_st = [s for s in st if s["route"] == "CONV" and s["entry"] >= W.HIST_START + 120]
    linked = sum(1 for s in conv_st if cf_end.get(s["cl"]) == s["entry"])
    ok(linked == len(conv_st), "C1: every conversion since August 2021 links to one award ended for council funding (%d of %d)" % (linked, len(conv_st)))
    # no later-completed assessment takes effect before an earlier one, per person
    a = T["ass"][T["ass"]["outcome"] != "SELF"].copy()
    a["cl"] = [deb.get(r) for r in a["debtor_ref"]]
    bad = 0
    for cl, gg in a.groupby("cl"):
        gg = gg.sort_values("completed", kind="stable")
        e_ = list(gg["effective_from"])
        bad += sum(1 for p, q in zip(e_, e_[1:]) if q < p)
    ok(bad == 0, "C1, SF17: no later-completed assessment takes effect before an earlier one, so the contribution in force on "
       "31 December 2026 is one row")
    # every ask resident has exactly one in-force assessment row selected
    con = AC.contributions(T["ass"], T["cw"])
    res = AC.residents(T["pl"], T["cw"], T["dl"])
    ok(all(r["cl"] in con for r in res), "every council-funded resident on 31 December 2026 has an assessment in force")
    # death match status: the PROBABLE matches close no open stay or award, so EXACT only reads the same
    Tx = dict(T)
    Tx["dl"] = T["dl"][T["dl"]["match_status"] == "EXACT"]
    Ix, _, _ = RP.inputs(Tx["pl"], Tx["li"], Tx["cw"], Tx["dl"])
    gx = E.golden(Ix)
    ok(np.allclose(gx["total"], tot, atol=1e-9) and gx["n_cf"] == g["n_cf"] and gx["n_sf"] == g["n_sf"]
       and np.allclose(AC.vec(AC.compute(Tx)), AC.vec(ask), atol=1e-9),
       "C1: deaths matched EXACT only give the same stock, pool, call and 20 ask figures (%d PROBABLE matches)"
       % int((T["dl"]["match_status"] == "PROBABLE").sum()))
    # the write-up's extra figure: the pool admitted from 1 January 2025
    adm = I["sf_admit"][E.pool(I)]
    ok(int((adm >= W.dn(dt.date(2025, 1, 1))).sum()) == figs["pool_admitted_since"]["1 January 2025"],
       "the pool admitted from 1 January 2025 is %d, as figures.json and the write-up state" % figs["pool_admitted_since"]["1 January 2025"])

    # ---------------------------------------------------------------- Layer 1 slips priced on both paths
    slips = {
        "interim and respite kept": dict(types=("PERM", "INT", "RESP")),
        "stays not stitched": dict(stitch=False),
        "crosswalk not used": dict(use_crosswalk=False),
        "death linkage unread": dict(use_deaths=False),
    }
    for name, kw in slips.items():
        Is, sts, _ = RP.inputs(T["pl"], T["li"], T["cw"], T["dl"], **kw)
        Is["cf_route"] = np.where(Is["cf_route"] == "", "DIRECT", Is["cf_route"])
        rs = E.rungs(Is, RP.census(sts, RP.month_ends()))
        ok(np.all(r10(rs["R5"]) != r10(tot)), "R2 slip '%s': the default %s stays outside the golden's bin" % (name, np.round(rs["R5"], 1).tolist()))
        print("      slip '%s': golden path %s" % (name, np.round(rs["golden"], 1).tolist()))
    for name, Ix in (("out-of-area dropped", I4), ("January-recorded conversions dropped", I7)):
        rs = E.rungs(Ix)
        ok(np.all(r10(rs["R5"]) != r10(tot)), "R2 slip '%s': the default %s stays outside the golden's bin" % (name, np.round(rs["R5"], 1).tolist()))

    # ---------------------------------------------------------------- clean-data and lens-swap tests
    It = sim.truth_inputs(S)
    rt = E.rungs(It)
    ok(np.all(rt["golden"] - rt["R5"] >= 15), "clean-data test: on the true timeline with every Layer 1 device repaired the default %s and the golden %s stay apart" % (np.round(rt["R5"], 1).tolist(), np.round(rt["golden"], 1).tolist()))
    ok(np.abs(rt["golden"] - tot).max() < 3, "clean-data test: the golden moves under 3 (%.2f)" % np.abs(rt["golden"] - tot).max())
    o_, HX_, _, _ = E.fit(I)
    A_, _ = E.survivors(I, o_, HX_)
    ok(np.allclose(A_.sum(axis=1), g["survivors"]), "lens swap: the default and the golden carry the same residents on the same dates; they differ only in the conversions")

    # ---------------------------------------------------------------- separation: the ask's columns and files never move the call
    Ts = {k: v.copy() for k, v in T.items()}
    rng = np.random.default_rng(5)
    Ts["pl"]["locality"] = rng.permutation(Ts["pl"]["locality"].values)
    Ts["pl"]["weekly_fee"] = rng.permutation(Ts["pl"]["weekly_fee"].values)
    Is, _, _ = RP.inputs(Ts["pl"], Ts["li"], Ts["cw"], Ts["dl"])
    ok(np.allclose(E.golden(Is)["total"], tot, atol=1e-9), "separation: scrambling the locality and fee columns leaves the call unchanged at full precision")
    mcw = Ts["cw"].copy()
    mcw.loc[mcw["merged_into"] != "", "debtor_ref"] = "399999999"
    Is, _, _ = RP.inputs(Ts["pl"], Ts["li"], mcw, Ts["dl"])
    ok(np.allclose(E.golden(Is)["total"], tot, atol=1e-9), "separation: the merged records' second debtor references do not move the call")
    # the ask does not read the payment lines (mirror sheet identical on the ask)
    Ta = {k: v for k, v in T.items()}
    Ta["li"] = T["li"].iloc[:0]
    ok(np.allclose(AC.vec(AC.compute(Ta)), AC.vec(ask)), "mirror: the ask is computed without the payment lines, so the default and the golden answer it alike")
    nproc = sum(1 for s in st if s["entry"] <= W.ASOF < s["exit"])
    ok(sum(counts.values()) <= nproc, "separation: the ask's %d residents are rows the call already reads (%d in place)" % (sum(counts.values()), nproc))

    # ---------------------------------------------------------------- the ask: golden, stops, cracker sheet
    gv = AC.vec(ask)
    fr = np.abs(gv - np.round(gv))
    ok(np.all(fr <= 0.2), "every ask figure within 0.2 of its whole pound (mid-bin): worst %.2f" % fr.max())
    ok(figs["chart"]["order"] == list(W.LOCS), "chart: the localities in their listed order (the prompt sets none)")
    s1 = AC.vec(AC.compute(T, **AC.STOPS["s1"]))
    ok(np.all(np.abs(s1 - gv) >= 1.5), "cracker (s1, the fee on the episode): all 20 figures off by 1.5 or more (least %.2f)" % np.abs(s1 - gv).min())
    ok(np.all(np.round(s1[1::2]) != np.round(gv[1::2])), "cracker (s1): every chart value label differs")
    for k, t in (("s2", 1.2), ("o1", 1.2), ("lazy", 2.0), ("s5", 1.5), ("s6", 1.5)):
        v = AC.vec(AC.compute(T, **AC.STOPS[k]))
        ok(np.all(np.abs(v - gv) >= t), "stop %s: all 20 off by %.1f or more (least %.2f)" % (k, t, np.abs(v - gv).min()))
    v = AC.vec(AC.compute(T, **AC.STOPS["s3"]))
    ok(np.all(np.abs(v - gv)[1::2] >= 1.2) and np.allclose(v[0::2], gv[0::2]),
       "stop s3 (the latest completed contribution): every net figure off by 1.2 or more, no fee moves")
    v = AC.vec(AC.compute(T, **AC.STOPS["s4"]))
    d4 = np.abs(v - gv)
    idx = [W.LOCS.index(l) * 4 + j for l in ("Braeburn", "Dunmorrow") for j in range(4)]
    ok((d4[idx] >= 1.0).sum() >= 4 and np.allclose(np.delete(d4, idx), 0), "stop s4 (active registrations only): %d of the re-registered homes' locality cells off, no other cell moves" % (d4[idx] >= 1.0).sum())
    draft_fee = np.array([ask[(loc, ct)][0] + W.NCHC_DRAFT_2027[k] - W.NCHC[2026][k] for loc in W.LOCS
                          for ct, k in (("Residential", 0), ("Nursing", 1))])
    ok(np.all(np.abs(draft_fee - gv[0::2]) >= 1.5), "the draft-offer read moves every fee figure by 1.5 or more")
    # necessity matrix
    need = {"placements_fee_as_entered": 20, "placements_locality": 20, "assessments_latest": 10, "crosswalk_one_ref": 4,
            "register_active_only": 4, "lookup_unread": 20, "rates_unread": 20, "deaths_unread": 0,
            "definitions_interim_kept": 10, "codes_unread": 10}
    for k, n in need.items():
        v = AC.vec(AC.compute(T, **AC.NECESSITY[k]))
        moved = int((np.round(v) != np.round(gv)).sum())
        ok(moved >= n, "necessity: %s moves %d of 20 (target %d)" % (k, moved, n))
    # composed mishandlings: none that includes the fee on the episode or the team's locality keeps a figure
    FT = AT.Fast(AC.table(T))
    for k in ("s1", "s2", "s3"):
        ok(np.allclose(FT.stop(**AC.STOPS[k]), AC.vec(AC.compute(T, **AC.STOPS[k])), atol=1e-9),
           "the fast table reproduces stop %s exactly" % k)
    ok(np.allclose(FT.stop(), gv, atol=1e-9), "the fast table reproduces the golden ask exactly")
    worst_p = 0
    for sub in AT.SUBSETS:
        if "primary" in sub or "second" in sub:
            v = FT.stop(**AT.composite(sub))
            worst_p = max(worst_p, AC.kept(v, gv))
    ok(worst_p == 0, "composed: no mishandling that includes the fee on the episode or the team's locality keeps a figure")
    # the pair ceiling at planning weights 38 / 7 / 55: the call's four figures and its sentence (5 criteria); instruction
    # following, the two files, the rounding and the chart's layout; the ask's 20 figures and the chart's value labels (21).
    # The cracker lands the call and misses every ask criterion; the mirror (the default R5) keeps about 5 of the
    # recommendation weight and no call figure
    call_crit, ask_crit = 5, 21
    labels_off = np.all(np.round(s1[1::2]) != np.round(gv[1::2]))
    ask_kept = int(np.sum(np.round(s1) == np.round(gv))) + (0 if labels_off else 1)
    mirror_call = sum(1 for k in range(4) if r10(rungs["R5"][k]) == r10(tot[k])) / call_crit
    cracker = 38 + 7 + 55 * ask_kept / ask_crit
    mirror = max(5.0, 38 * mirror_call) + 7 + 55 * ask_kept / ask_crit
    pair = (cracker + mirror) / 2
    ok(pair <= 40, "pair ceiling %.1f at or under 40 (cracker %.1f, mirror %.1f)" % (pair, cracker, mirror))
    ok(cracker < 50, "both top responses on the call and no ask criterion: %.1f each, under 50" % cracker)
    r10_call = sum(1 for k in range(4) if r10(rungs["R10"][k]) == r10(tot[k])) / call_crit
    ok((cracker + 38 * r10_call + 7 + 55 * ask_kept / ask_crit) / 2 <= 40,
       "pair ceiling with the mirror at R10 (the 2027 jump alone, %d of 4 dates): %.1f"
       % (round(r10_call * call_crit), (cracker + 38 * r10_call + 7 + 55 * ask_kept / ask_crit) / 2))

    # ---------------------------------------------------------------- silence and realism
    texts = doc_text()
    banned = ["months since admission", "hazard", "competing", "cohort", "survival", "run rate", "depletion", "deplete",
              "kaplan", "aalen", "johansen", "cumulative incidence", "forecast", "distractor", "projection", "drawdown",
              "draw down", "bring forward", "brought forward", "sooner", "natural experiment", "excess", "weeks of conversions",
              "weeks of drawdown", "weeks' worth"]
    for f, t in texts.items():
        low = t.lower()
        hits = [b for b in banned if b in low]
        ok(not hits, "silence: %s carries none of the method words %s" % (f, hits))
    allt = "\n".join(texts.values())
    for f in files:
        if f.endswith((".csv", ".tsv", ".txt")):
            allt += open(os.path.join(TGT, f), encoding="utf-8").read()
    ok("—" not in allt and "–" not in allt, "no em or en dashes anywhere in the pack")
    # no file carries a forecast, a conversion count by year or a census
    hdrs = " ".join(pd.read_csv(os.path.join(TGT, f), nrows=0, sep="\t" if f.endswith(".tsv") else ",").columns.str.lower()
                    .str.cat(sep=" ") for f in files if f.endswith((".csv", ".tsv")))
    ok(not re.search(r"forecast|census|conversion", hdrs), "no column carries a forecast, a census or a conversion count")
    # realism: yearly flows are not identical, monthly streams not constant, headline totals not round
    pl = T["pl"]
    d_adm = pl[(pl["placement_type"] == "PERM") & (pl["route"] == "DIRECT")].drop_duplicates("admitted")
    st_ = [s for s in st if s["route"] == "DIRECT"]
    by_y = {}
    by_m = {}
    for s in st_:
        d = W.dd(s["entry"])
        if 2021 <= d.year <= 2026:
            by_y[d.year] = by_y.get(d.year, 0) + 1
            by_m[(d.year, d.month)] = by_m.get((d.year, d.month), 0) + 1
    yv = [by_y[y] for y in range(2022, 2027)]
    ok(len(set(yv)) == len(yv), "realism: direct admissions differ year to year %s" % yv)
    ok(len(set(by_m.values())) >= 8, "realism: monthly direct admissions vary (%d distinct counts)" % len(set(by_m.values())))
    ok(g["n_cf"] % 10 != 0 and g["n_sf"] % 10 != 0, "realism: the as-of stock (%d) and pool (%d) are not round" % (g["n_cf"], g["n_sf"]))
    ok(np.all(np.abs(gv - np.round(gv)) > 0.001), "realism: no ask average is a whole pound exactly")
    li_types = T["li"]["line_type"].value_counts()
    ok(set(li_types.index) == {"FPC", "FNC", "ADJ", "HOSP"}, "payment lines carry every line type %s" % dict(li_types))
    # the payment calendar: each financial year numbers its four-weekly periods from P01, whose middle day falls in
    # April of that year, and no year runs past P13
    per = T["li"][["period", "period_start"]].drop_duplicates()
    bad_p = 0
    for r in per.itertuples(index=False):
        y, n = int(r.period[:4]), int(r.period[-2:])
        mid = dt.date.fromisoformat(r.period_start) + dt.timedelta(days=13)
        fy_mid = mid.year if mid.month >= 4 else mid.year - 1
        bad_p += (fy_mid != y) or n > 13 or (n == 1 and mid.month != 4)
    ok(bad_p == 0, "payment calendar: %d periods, each numbered in the financial year of its middle day, P01 to P13" % len(per))
    # the extract notes name every other file in the pack (H9)
    notes = open(os.path.join(TGT, "extract_notes_2027-01-18.txt"), encoding="utf-8").read()
    unnamed = [f for f in files if f != "extract_notes_2027-01-18.txt" and f not in notes]
    ok(not unnamed, "the extract notes name every other file in the pack %s" % unnamed)
    # containers: the fiction's authors and dates
    people = set(W.PEOPLE.values())
    card = json.load(open(os.path.join(TASK, "..", ".claude", "skills", "fingerprint", "cards", "task134.json")))
    ok(people <= set(card["world"]["people"]), "every persona is on the card (drawn with guard.py names)")
    for f in files:
        p = os.path.join(TGT, f)
        if f.endswith((".docx", ".xlsx")):
            core = zipfile.ZipFile(p).read("docProps/core.xml").decode()
            who = re.findall(r"<dc:creator>([^<]*)</dc:creator>", core) + re.findall(r"<cp:lastModifiedBy>([^<]*)</cp:lastModifiedBy>", core)
            ok(all(w in people for w in who), "%s: authors %s are the fiction's" % (f, who))
            stamps = re.findall(r"<dcterms:(?:created|modified)[^>]*>([^<]*)<", core)
            ok(all("2021" <= x[:10] <= "2027-01-18" for x in stamps), "%s: dates inside the fiction %s" % (f, stamps))
        if f.endswith(".pdf"):
            from pypdf import PdfReader
            m = PdfReader(p).metadata
            ok(m.get("/Author") in people and str(m.get("/CreationDate", "")).startswith("D:2026"), "%s: author %s and date %s" % (f, m.get("/Author"), m.get("/CreationDate")))
        mt = dt.datetime.fromtimestamp(os.path.getmtime(p), W.LON)
        ok(dt.datetime(2026, 4, 1, tzinfo=W.LON) <= mt <= dt.datetime(2027, 1, 19, tzinfo=W.LON), "%s: saved %s" % (f, mt.date()))

    print("\n%d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())

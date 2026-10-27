"""The generator's assertions on the cut pack and the clean truth: the input gates, the call against the world's truth,
the ladder and the standing family, the three rules (R1 to R3), the Layer 1 items, the semantic fork rows (SF1 to
SF12), both asks and their devices, the context report's recomputation and the realism sweep.

    python3 task141/generator/checks.py
"""
import collections
import datetime as dt
import json
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import numpy as np    # noqa: E402

import asks as AS     # noqa: E402
import ceiling as C   # noqa: E402
import common as K    # noqa: E402
import docs as DOC    # noqa: E402
import forecast as F  # noqa: E402
import golden as G    # noqa: E402
import metadata as MD  # noqa: E402
import pack as PK     # noqa: E402
import pack_read as PR  # noqa: E402
import world as WD    # noqa: E402

RESULTS = []
FLOOR = 1.15                       # every wrong rung sits at least this far below the golden's lower pod edge


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %-62s %s" % ("PASS" if ok else "FAIL", label, detail))


def in_bin(v):
    return 1150 <= v < 1250 and K.pods(v) == 6


def pdf_text(name):
    return subprocess.run(["pdftotext", "-layout", os.path.join(TARGET, name), "-"], capture_output=True,
                          text=True).stdout


def rec_copy(R):
    S = F.Rec()
    S.__dict__.update({k: v for k, v in R.__dict__.items() if k != "cache"})
    S.cases = [dict(c) for c in R.cases]
    S.C = {c["id"]: c for c in S.cases}
    F.finish(S)
    return S


def main():
    files = sorted(os.listdir(TARGET))
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    P = PR.read()
    R = PR.record(P)
    T = PR.terms(P)

    # ------------------------------------------------------------------ input gates
    fmts = {os.path.splitext(f)[1] for f in files}
    rows = {f: sum(1 for _ in open(os.path.join(TARGET, f), "rb")) - 1 for f in files if f.endswith(".csv")}
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("input: 10 or more files", len(files) >= 10, "%d files" % len(files))
    check("input: 3 or more formats", len(fmts) >= 3, " ".join(sorted(fmts)))
    check("input: a file of 25,000 rows or more", max(rows.values()) >= 25000, "%s %d rows" % (max(rows, key=rows.get),
                                                                                             max(rows.values())))
    check("input: two or more distractors named in metadata.json", len(meta["distractor_files"]) >= 2,
          ", ".join(meta["distractor_files"]))
    check("input: every file has a source, date and licence", set(MD.SOURCES) == set(files))
    check("input: no file name names the stump", not any(re.search(r"review|window|tolling|expir|clock|trap|issue", f)
                                                         for f in files))

    # ------------------------------------------------------------------ the call
    W = WD.simulate()
    PK.assign_ids(W)
    Bw = PK.bookings(W)
    Rw = F.record_from_world(W)
    g, parts, est = F.two_clock(R, **G.GOLD)
    gw = F.two_clock(Rw, **G.GOLD)[0]
    check("call: golden from the pack equals the golden on the world record", abs(g - gw) < 1e-6, "%.4f %.4f" % (g, gw))
    check("call: six pods, 1,200 to the nearest 100", K.pods(g) == 6 and K.round_to(g, 100) == 1200, "%.1f" % g)
    check("call: figures.json carries the call", figs["call.pods"] == 6 and figs["call.admissions"] == 1200
          and abs(figs["call.admissions_unrounded"] - round(g, 1)) < 0.05)
    tr, sd = WD.truth(W, reps=8)
    check("call: the world's truth sits in the golden's bin", in_bin(tr), "truth %.0f (sd %.0f over 8 runs)" % (tr, sd))
    check("call: golden within 4 per cent of the truth", abs(g - tr) / tr < 0.04, "%.1f per cent" % (100 * (g - tr) / tr))

    # ------------------------------------------------------------------ the ladder
    rg, fam = G.rungs(R)
    floor = 1100 / FLOOR
    for k in ("persistence", "rate_on_exposure", "one_clock_by_term", "one_clock", "two_clock_no_transition"):
        check("ladder: %s files fewer pods, under the rung floor" % k, K.pods(rg[k]) < 6 and rg[k] <= floor,
              "%.0f, %d pods (floor %.0f)" % (rg[k], K.pods(rg[k]), floor))
    check("ladder: the default path files three pods", K.pods(rg["one_clock"]) == 3, "%.0f" % rg["one_clock"])
    check("ladder: persistence files five pods", K.pods(rg["persistence"]) == 5, "%.0f" % rg["persistence"])
    for k, v in fam.items():
        check("family: %s" % k, in_bin(v), "%.0f" % v)
    lo = F.two_clock(R, window=150, clip_act=False, score_adjust=True)[0]
    hi = F.two_clock(R, window=150, conv_pooled=True, pwin_free=True, mean_lag=True, score_adjust=False)[0]
    check("family: the extreme combinations of the six choices stay in the bin", in_bin(lo) and in_bin(hi),
          "%.0f and %.0f" % (lo, hi))
    tx = F.to_expiry(R)
    check("family: every petition on the expiry clock alone still files six pods", K.pods(tx) == 6, "%.0f" % tx)
    fs = rg["two_clock_from_supervision_start"]
    check("ladder: the two clocks without delayed entry fall short of the golden", fs < g - 50 and K.pods(fs) <= 6,
          "%.0f, %d pods" % (fs, K.pods(fs)))

    # ------------------------------------------------------------------ R1: the field's raw material ships
    heads = {f: open(os.path.join(TARGET, f), encoding="utf-8").readline().strip().lower() for f in files
             if f.endswith(".csv")}
    bad = [f for f, h in heads.items() if re.search(r"review|window|days_to_(exp|end)|end_of_term|kind|clock", h)]
    check("R1: petitions, terms and orders ship at the record's grain", all(
        x in heads[K.PETITIONS] for x in ("filed_date", "disposition_date")) and "supervision_begin" in heads[K.CMS2]
          and "expiration_after" in heads[K.ORDERS])
    check("R1: no column holds a petition's clock or kind", not bad, ", ".join(bad))
    kinds = collections.defaultdict(collections.Counter)
    for lg in W.log.values():
        for e in lg:
            if K.RECORD_START <= e["file"] <= K.EXTRACT and e["kind"] in ("ORDINARY", "REVIEW"):
                for a in e["alleg"]:
                    kinds[e["kind"]][a] += 1
    sh = {k: {a: v / sum(c.values()) for a, v in c.items()} for k, c in kinds.items()}
    gap = max(abs(sh["ORDINARY"].get(a, 0) - sh["REVIEW"].get(a, 0)) for a in set(sh["ORDINARY"]) | set(sh["REVIEW"]))
    check("R1: end-of-term petitions carry the ordinary petitions' allegations", gap < 0.03, "largest gap %.3f" % gap)
    check("R1: the decisive computation reads petitions on the expiration in force", est["wpet"] > 1000 and
          est["reach"] > 5000, "%d of %d windows" % (est["wpet"], est["reach"]))

    # ------------------------------------------------------------------ R2: each mess item mishandled leaves the call
    raw = {r["CASE_NO"]: int(r["RISK_SCORE"]) for r in P["cms1"]}
    S = rec_copy(R)
    for c in S.cases:
        if c["id"] in raw:
            c["score"] = raw[c["id"]]
    v = F.two_clock(S, **G.GOLD)[0]
    va = F.two_clock(S)[0]
    check("R2: CaseTrak 1 risk scores left on the version 1 scale", in_bin(v) and K.pods(va) == 6,
          "%.0f (the score-adjusted member %.0f)" % (v, va))
    S = rec_copy(R)
    for c in S.cases:
        S.scheds[c["id"]] = [(-10 ** 6, T[c["id"]]["exp"])]
    v = F.two_clock(S, **G.GOLD)[0]
    check("R2: every scheduled expiration read as it now stands", in_bin(v), "%.0f" % v)
    v = F.two_clock(R, ns_months=6, **G.GOLD)[0]
    check("R2: new supervision starts at the trailing six months' rate", in_bin(v), "%.0f" % v)

    # ------------------------------------------------------------------ R3: the analyst test, the decisive step alone
    check("R3a: the easy route with every filed rule applied files three pods", K.pods(rg["one_clock"]) == 3)
    check("R3b: the easy route with only the clock changed files the golden", K.pods(g) == 6 and
          K.pods(rg["one_clock"]) != 6)
    check("R3b: each lower rung's single correction stays on a wrong answer",
          all(K.pods(rg[k]) != 6 for k in ("one_clock_by_term", "rate_on_exposure", "persistence",
                                            "two_clock_no_transition")))
    rpt = pdf_text(K.REPORT)
    F_ = DOC.report_figures(P["cms1"], P["cms2"], P["pets"])
    nums = [F_["began"]["F"], F_["began"]["M"], F_["filed"]["F"], F_["filed"]["M"], F_["disp"][("F", "REVOKED")]]
    check("R3c: the annual report recomputes from the shipped rows", all("{:,}".format(x) in rpt for x in nums))
    check("R3c: no shipped document forecasts 2027 or names the end-of-term petitions",
          not re.search(r"(?i)projection|forecast|tolling petition|end of (the )?term|second clock", rpt +
                        pdf_text(K.ACT_PDF)))

    # ------------------------------------------------------------------ semantic forks
    revf = collections.Counter()
    for p in P["pets"]:
        if p["disposition"] == "REVOKED" and T[p["case_number"]]["lvl"] == "F":
            revf[(T[p["case_number"]]["person"], p["disposition_date"])] += 1
    check("SF1: one felony revocation a person and day (admission = revoked felony petition)", max(revf.values()) == 1)
    check("SF2: felony commitments begin at the hearing (none served on weekends)", all(
        p["served_as"] == "CONSECUTIVE" for p in P["pets"] if p["disposition"] == "REVOKED" and "-CF-" in p["case_number"]))
    links = G.commitment_levels(P)
    fel_days = {(T[p["case_number"]]["person"], p["disposition_date"]) for p in P["pets"]
                if p["disposition"] == "REVOKED" and "-CF-" in p["case_number"]}
    so2p = PR.sheriff_to_person(P)
    start_f = [b for b in links if b["lvl"] == "F" and b["first"] and b["start"].date() >= dt.date(2019, 2, 1)]
    ok3 = sum((so2p.get(b["so"]), b["start"].date().isoformat()) in fel_days for b in start_f)
    check("SF3: felony commitments in the jail begin on a court revocation day (county time)",
          ok3 == len(start_f), "%d of %d commitments" % (ok3, len(start_f)))
    plan = pdf_text(K.PLAN_PDF)
    act = pdf_text(K.ACT_PDF)
    norm = re.sub(r"\s+", " ", plan)
    check("SF4: terms beginning supervision after the extract are filed in, and decide the call",
          "whose supervision begins after the extract" in norm and K.pods(g - parts["new"]) < 6,
          "%.0f without them" % (g - parts["new"]))
    cal = sum(1 for c in R.active if R.sched_now[c["id"]] > K.TRANS and c["sup"] <= K.day("2025-03-31"))
    check("SF5: 24 months as calendar months or as 730 days: the same 31 March terms", cal == figs["transition_terms"],
          "%d and %d" % (cal, figs["transition_terms"]))
    check("SF6: no term ends under section 4 before 31 March 2027", all(
        F.act_end(R, c) >= min(R.sched_now[c["id"]], K.TRANS) for c in R.active))
    check("SF7: section 6 keeps pending proceedings, and it decides the call", "Proceedings pending on the day a term "
          "ends under section 4 continue" in re.sub(r"\s+", " ", act) and K.pods(g - est["trans"]["window"]) < 6,
          "%.0f without them" % (g - est["trans"]["window"]))
    pend = sum(1 for p in R.pet if p["decided"] is None)
    check("SF8: petitions pending at the extract carried as pending", pend > 100 and parts["pending"] > 0, "%d" % pend)
    check("SF9: or part of 220 is a ceiling: six pods", "or part of 220" in re.sub(r"\s+", " ", plan) and
          math.ceil(g / 220) == 6 and round(g / 220) == 5, "%.2f" % (g / 220))
    check("SF10: pods from the unrounded projection and from the plan figure agree", K.pods(g) == K.pods(1200))
    g1 = sum(1 for c in W.commitments if c["lvl"] == "M" and c["cls"] == "PV-FEL" and
             K.EXTRACT - 365 < c["day"] <= K.EXTRACT)
    check("SF11: misdemeanor commitments of felony probationers added: same call", in_bin(g + g1), "%d a year" % g1)
    check("SF12: the end-of-term window and the other standing choices: same call", all(in_bin(v) for v in fam.values())
          and in_bin(lo) and in_bin(hi))

    # ------------------------------------------------------------------ the asks
    A = G.bed_days(P)
    At = AS.bed_days_truth(Bw)
    check("Ask A: bed-days from the pack equal the world's", (A == At).all(), str(A.tolist()))
    ga, gb, ka, kb = C.measure(P)
    check("Ask A: the bookings' classification keeps none of the 8", ka["classification"] == 0)
    check("Ask A: misdemeanor commitments of felony probationers in every quarter", all(
        sum(1 for c in W.commitments if c["lvl"] == "M" and c["cls"] == "PV-FEL" and AS.quarter_of(c["day"]) == q) > 0
        for q in range(4)))
    offs, sups, _, _ = G.imposed_terms(P)
    wt = AS.ask_b_truth(W)
    check("Ask B: imposed terms from the pack equal the world's", np.allclose(offs + sups, list(wt[0]) + list(wt[1])))
    check("Ask B: term_months as it stands keeps none of the 8", kb["term_months as it stands"] == 0)
    dist = min(abs(v * 10 - math.floor(v * 10) - 0.5) / 10 for v in offs + sups)
    check("Ask B: every figure at least 0.02 from a rounding edge", dist >= 0.02, "%.3f" % dist)
    edge = [t for t in T.values() if t["lvl"] == "F" and (t["open"] or (t["closed"] and t["closed"][0] == K.EXTRACT))]
    by = collections.defaultdict(list)
    for t in edge:
        by[G.sup_band(t["sup"])].append(t["imposed"])
    check("Ask B: terms closed on the extract day leave every band's figure", all(
        K.round1(np.mean(by[k])) == K.round1(sups[k]) for k in range(4)))
    check("Ask B: the device moves every band and office", all(
        K.round1(a) != K.round1(b) for a, b in zip(offs + sups, list(G.imposed_terms(P, "as_it_stands")[0]) +
                                                   list(G.imposed_terms(P, "as_it_stands")[1]))))
    check("asks: the call reads no booking and no term length", True, "two_clock reads terms' dates, scores and petitions")

    # ------------------------------------------------------------------ realism sweep
    bnos = [r["booking_number"] for r in P["book"]]
    check("realism: booking numbers unique", len(bnos) == len(set(bnos)))
    pnos = [r["petition_no"] for r in P["pets"]]
    check("realism: petition numbers unique", len(pnos) == len(set(pnos)))
    cases = [r["CASE_NO"] for r in P["cms1"]] + [r["case_number"] for r in P["cms2"]]
    check("realism: each term in one register", len(cases) == len(set(cases)))
    late = [p for p in P["pets"] if p["filed_date"] > "2026-09-30" or (p["disposition_date"] or "") > "2026-09-30"]
    late += [o for o in P["orders"] if o["order_date"] > "2026-09-30"]
    check("realism: nothing dated after the extract", not late, "%d" % len(late))
    B = PR.bookings(P)
    neg = [b for b in B if b["end"] is not None and b["end"] <= b["start"]]
    check("realism: every closed booking released after it was booked", not neg, "%d" % len(neg))
    byp = collections.defaultdict(list)
    for b in B:
        if b["cls"] != "PV-OOS":
            byp[so2p.get(b["so"], b["so"])].append(b)
    over = 0
    for lst in byp.values():
        lst.sort(key=lambda b: b["start"])
        over += sum(1 for a, b in zip(lst, lst[1:]) if a["end"] is None or b["start"] < a["end"])
    check("realism: one booking at a time per person", over == 0, "%d overlaps" % over)
    unmapped = sum(1 for b in B if b["cls"] not in ("PV-OOS", "PROB-COND") and b["so"] not in so2p)
    cond = sum(1 for b in B if b["cls"] == "PROB-COND" and b["so"] not in so2p)
    check("realism: every hold and commitment's Sheriff's number is in the crosswalk", unmapped == 0,
          "%d (%d confinement bookings of terms not yet supervised)" % (unmapped, cond))
    mon = [v for _, v in G.history(P)]
    check("realism: monthly admissions vary like counts", np.std(mon) > 5 and len(set(mon)) > 20,
          "sd %.1f, %d distinct" % (np.std(mon), len(set(mon))))
    yr = collections.Counter()
    for (y, m), v in G.history(P):
        yr[y] += v
    check("realism: no trend in the yearly admissions 2019 to 2025", max(yr[y] for y in range(2019, 2026)) /
          min(yr[y] for y in range(2019, 2026)) < 1.2, str({y: yr[y] for y in range(2019, 2026)}))
    dash = [f for f in files if f.endswith((".csv", ".txt")) and re.search("[\u2013\u2014]", open(
        os.path.join(TARGET, f), encoding="utf-8").read())]
    dash += [f for f in files if f.endswith(".pdf") and re.search("[\u2013\u2014]", pdf_text(f))]
    check("realism: no em or en dash in any shipped text", not dash, ", ".join(dash))
    persons = set(K.PEOPLE.values())
    text = plan + act + rpt + open(os.path.join(TARGET, K.README), encoding="utf-8").read()
    check("realism: no placeholder identity", not re.search(r"John Doe|Jane Doe|Acme|Company A|Lorem", text))
    check("realism: personas from guard.py names only", all(n in persons for n in re.findall(
        r"Gina Yoder|Larry Pugh|Colleen Cameron|Donald Russo|Megan Chambers|Gloria Lynch", text)))
    conv = [r for r in P["book"] if r["release_reason"] == "CONVERTED TO NEW JMS"]
    check("realism: the jail system's replacement closes and reopens the spells open at it", len(conv) > 200 and all(
        r["released_at"] == "02/04/2025 03:10" for r in conv), "%d spells" % len(conv))

    fails = [r for r in RESULTS if not r[1]]
    print("\n%d checks, %d failed" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

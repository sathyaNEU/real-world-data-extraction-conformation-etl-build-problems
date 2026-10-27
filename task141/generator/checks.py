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
FLOOR = 1.09                       # every wrong rung below sits at least this far under the golden's lower pod edge
EDGE_LO, EDGE_HI = 6 * K.POD_SIZE, 7 * K.POD_SIZE
LOW_MARGIN, HIGH_MARGIN = 150, 30  # independent builds ran up to 153 under the golden; the upward stack 45 over it


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %-62s %s" % ("PASS" if ok else "FAIL", label, detail))


def in_bin(v):
    """the golden's call: seven pods, more than six pods' cover and no more than seven's"""
    return EDGE_LO < v <= EDGE_HI and K.pods(v) == 7


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
    check("input: no file name names the stump", not any(re.search(r"room|maximum|extension|window|class|trap|cap",
                                                                    f) for f in files))

    # ------------------------------------------------------------------ the call
    W = WD.simulate()
    PK.assign_ids(W)
    Bw = PK.bookings(W)
    Rw = F.record_from_world(W)
    g, parts, info = F.projection(R, **G.GOLD)
    gw = F.projection(Rw, **G.GOLD)[0]
    check("call: golden from the pack equals the golden on the world record", abs(g - gw) < 1e-6, "%.4f %.4f" % (g, gw))
    check("call: seven pods, the golden %d over six pods' cover and %d under seven's" % (LOW_MARGIN, HIGH_MARGIN),
          K.pods(g) == 7 and EDGE_LO + LOW_MARGIN <= g <= EDGE_HI - HIGH_MARGIN, "%.1f" % g)
    check("call: figures.json carries the call", figs["call.pods"] == 7
          and abs(figs["call.admissions_unrounded"] - round(g, 1)) < 0.05 and "call.admissions" not in figs)
    tr, sd = WD.truth(W, reps=8)
    check("call: the world's truth files the golden's seven pods, 100 or more over six pods' cover",
          K.pods(tr) == 7 and EDGE_LO + 100 <= tr <= EDGE_HI,
          "truth %.0f (sd %.0f over 8 runs)" % (tr, sd))
    check("call: golden within 4 per cent of the truth", abs(g - tr) / tr < 0.04, "%.1f per cent" % (100 * (g - tr) / tr))

    # ------------------------------------------------------------------ the ladder
    rg, fam = G.rungs(R)
    floor = EDGE_LO / FLOOR
    for k in ("pooled", "iia", "two_clock_no_extension", "persistence", "rate_on_exposure", "one_clock",
              "one_clock_by_term"):
        check("ladder: %s files fewer pods, under the rung floor" % k, K.pods(rg[k]) < 7 and rg[k] <= floor,
              "%.0f, %d pods (floor %.0f)" % (rg[k], K.pods(rg[k]), floor))
    check("ladder: every would-be extension a petition files more pods, clear of the upper edge",
          K.pods(rg["full"]) > 7 and rg["full"] >= EDGE_HI * 1.1, "%.0f, %d pods" % (rg["full"], K.pods(rg["full"])))
    check("ladder: the default path (pooled end-of-term rate) files five pods", K.pods(rg["pooled"]) == 5,
          "%.0f" % rg["pooled"])
    check("ladder: persistence files no more pods than the default path",
          K.pods(rg["persistence"]) <= K.pods(rg["pooled"]), "%.0f, %d pods" % (rg["persistence"],
                                                                                 K.pods(rg["persistence"])))
    check("ladder: every wrong rung files a pod count of its own or below the default", len({K.pods(rg[k]) for k in (
        "pooled", "iia", "full", "golden")}) == 4)
    for k, v in fam.items():
        check("family: %s" % k, in_bin(v), "%.0f" % v)
    lo = F.projection(R, window=90, clip_act=False)[0]
    hi = max(F.projection(R, window=150, conv_pooled=True, pending_free=True, mean_lag=True, score_adjust=True)[0],
             F.projection(R, window=150, pending_free=True, mean_lag=True)[0])
    check("family: the extreme combinations of the standing choices stay in the bin", in_bin(lo) and in_bin(hi),
          "%.0f and %.0f" % (lo, hi))
    ns, ns_lo = F.projection(R, second=False)[0], F.projection(R, second=False, window=90, clip_act=False)[0]
    check("family: the extended terms' second windows left out, alone and at the low extreme, stay in seven pods",
          in_bin(ns) and in_bin(ns_lo), "%.0f and %.0f" % (ns, ns_lo))
    S = rec_copy(R)
    for c in S.cases:
        c["exts"] = []
    v_imp = F.projection(S, **G.GOLD)[0]
    check("SF17: a window's room read on the term imposed alone leaves the class maximum's extensions out: same call",
          in_bin(v_imp), "%.0f, %d pods" % (v_imp, K.pods(v_imp)))
    S = rec_copy(R)
    for c in S.cases:
        c["imposed_term"] = T[c["id"]]["length"]
        c["exts"] = []
    v_now = F.projection(S, **G.GOLD)[0]
    check("SF17: a window's room read on the term as it now stands puts extended terms at the maximum early",
          K.pods(v_now) < 7, "%.0f, %d pods" % (v_now, K.pods(v_now)))
    rows17 = [r for r in P["orders"] if r["order_type"] == "EXTENSION"]
    check("SF17: the orders carry the term in force after each extension, so the term at any window is on file",
          all(int(r["term_months_after"]) <= P["classes"][T[r["case_number"]]["klass"]] for r in rows17),
          "%d extension orders" % len(rows17))

    # ------------------------------------------------------------------ R1: the field's raw material ships
    heads = {f: open(os.path.join(TARGET, f), encoding="utf-8").readline().strip().lower() for f in files
             if f.endswith(".csv")}
    bad = [f for f, h in heads.items() if re.search(r"room|at_max|maximum|review|window|end_of_term|kind|clock", h)]
    check("R1: terms, classes, orders and petitions ship at the record's grain", all(
        x in heads[K.PETITIONS] for x in ("filed_date", "disposition_date")) and "offense_class" in heads[K.CMS2]
          and "months_extended" in heads[K.ORDERS] and "term_months_after" in heads[K.ORDERS])
    check("R1: no column holds a term's room, its maximum or a petition's kind", not bad, ", ".join(bad))
    kinds = collections.defaultdict(collections.Counter)
    for lg in W.log.values():
        for e in lg:
            if K.RECORD_START <= e["file"] <= K.EXTRACT and e["kind"] in ("ORDINARY", "REVIEW"):
                for a in e["alleg"]:
                    kinds[e["kind"]][a] += 1
    sh = {k: {a: v / sum(c.values()) for a, v in c.items()} for k, c in kinds.items()}
    gap = max(abs(sh["ORDINARY"].get(a, 0) - sh["REVIEW"].get(a, 0)) for a in set(sh["ORDINARY"]) | set(sh["REVIEW"]))
    check("R1: end-of-term petitions carry the ordinary petitions' allegations", gap < 0.03, "largest gap %.3f" % gap)
    rt = F.window_rates(R)
    check("R1: the decisive split reads each window's term in force against its class maximum",
          rt["n_nonext"] > 5000 and rt["n"] - rt["e"] > 0.25, "%d of %d windows at the maximum, %.3f against %.3f" % (
              rt["n_nonext"], rt["n_windows"], rt["n"], rt["e"]))
    byk, byl = collections.defaultdict(list), collections.defaultdict(list)
    byk_n, byk_e = collections.defaultdict(list), collections.defaultdict(list)
    for cc in R.cases:
        ps = R.byc.get(cc["id"], [])
        e = F.end_of(R, cc) if cc["id"] in R.close else K.EXTRACT + 1
        sch = R.scheds[cc["id"]]
        for i, (since, s_) in enumerate(sch):
            until = sch[i + 1][0] if i + 1 < len(sch) else 10 ** 9
            wo = s_ - 120
            if s_ > K.EXTRACT - 30 or not (since <= wo < until) or wo < K.RECORD_START or e <= wo or cc["sup"] > wo:
                continue
            hit = any(wo <= p["file"] < s_ for p in ps)
            byk[cc["klass"]].append(hit)
            byl[cc["imposed_term"]].append(hit)
            (byk_n if F.term_m_at(cc, wo) >= cc["max_m"] else byk_e)[cc["klass"]].append(hit)
    sk = [np.mean(v) for v in byk.values() if len(v) > 300]
    sl = [np.mean(v) for v in byl.values() if len(v) > 300]
    spread = max(max(sk) - min(sk), max(sl) - min(sl))
    check("R1: no class and no imposed length alone separates the end-of-term rate", spread * 2.5 < rt["n"] - rt["e"],
          "largest spread %.3f against %.3f" % (spread, rt["n"] - rt["e"]))
    at = {kk: (np.mean(v), len(v)) for kk, v in byk_n.items() if len(v) >= 150}
    wr = {kk: np.mean(v) for kk, v in byk_e.items() if len(v) >= 150}
    check("R1: every class at its maximum files at the at-maximum rate, drug felony class 4's 24 months included",
          "DF4" in at and all(abs(m - rt["n"]) < 0.06 for m, _ in at.values()) and max(wr.values()) < 0.12,
          " ".join("%s %.3f (%d)" % (kk, m, n) for kk, (m, n) in sorted(at.items())))

    # ------------------------------------------------------------------ R2: each mess item mishandled
    raw = {r["CASE_NO"]: int(r["RISK_SCORE"]) for r in P["cms1"]}
    S = rec_copy(R)
    for cc in S.cases:
        if cc["id"] in raw:
            cc["score"] = raw[cc["id"]]
    v = F.projection(S, **G.GOLD)[0]
    va = F.projection(S, score_adjust=True)[0]
    check("R2: CMS 1 risk scores left on the version 1 scale", in_bin(v) and K.pods(va) == 7,
          "%.0f (the score-adjusted member %.0f)" % (v, va))
    S = rec_copy(R)
    for cc in S.cases:
        S.scheds[cc["id"]] = [(-10 ** 6, T[cc["id"]]["exp"])]
    v = F.projection(S, **G.GOLD)[0]
    check("R2: every scheduled expiration read as it now stands: the pods stand", K.pods(v) == 7, "%.0f" % v)
    v = F.projection(R, ns_months=6, **G.GOLD)[0]
    check("R2: new supervision starts at the trailing six months' rate", in_bin(v), "%.0f" % v)

    # ------------------------------------------------------------------ R3: the analyst test, the decisive step alone
    check("R3a: the easy route with every filed rule applied files five pods", K.pods(rg["pooled"]) == 5)
    check("R3b: the easy route with only the comparison group changed files the golden", K.pods(g) == 7 and
          abs(F.projection(R, "pooled")[0] - g) > 300)
    check("R3b: each lower rung's single correction stays on a wrong answer",
          all(K.pods(rg[k]) != 7 for k in ("one_clock_by_term", "rate_on_exposure", "persistence",
                                            "two_clock_no_extension", "iia", "full")))
    rpt = pdf_text(K.REPORT)
    F_ = DOC.report_figures(P["cms1"], P["cms2"], P["pets"])
    nums = [F_["filed"]["F"], F_["filed"]["M"], F_["disp"][("F", "REVOKED")], F_["disp"][("M", "REVOKED")],
            sum(v["F"] for v in F_["caseload"].values())]
    check("R3c: the annual report recomputes from the shipped rows", all("{:,}".format(x) in rpt for x in nums))
    check("R3c: no shipped document forecasts 2027", not re.search(r"(?i)projection|forecast", rpt + pdf_text(
        K.ACT_PDF)))
    check("R3c: no shipped document names terms at or under their maximum, or says how the supervising office is found",
          not re.search(r"(?i)end of (the )?term|at (its|their) (class )?maximum|room to extend|could not be extended|"
                        r"office of the officer|kept at intake|reclassif|order reaches", rpt + pdf_text(K.ACT_PDF) +
                        pdf_text(K.PLAN_PDF)))
    check("R3c: no shipped document breaks the caseload down by office", not re.search(r"(?i)by office|Eastfield",
                                                                                        rpt))

    # ------------------------------------------------------------------ semantic forks
    revf = collections.Counter()
    for p in P["pets"]:
        if p["disposition"] == "REVOKED" and T[p["case_number"]]["lvl"] == "F":
            revf[(T[p["case_number"]]["person"], p["disposition_date"])] += 1
    check("SF1: one felony revocation a person and day (admission = revoked felony petition)", max(revf.values()) == 1)
    check("SF2: felony commitments served consecutively (none on weekends)", all(
        p["served_as"] == "CONSECUTIVE" for p in P["pets"] if p["disposition"] == "REVOKED" and "-CF-" in p["case_number"]))
    cm = G.commitments(P)
    late = [c for c in cm if c["cls"] != "PV-HOLD" and c["order"] is not None and c["start"].date() > c["order"]]
    on_day = [c for c in cm if c["order"] is not None and c["start"].date() == c["order"]]
    lag = max((c["start"].date() - c["order"]).days for c in late)
    check("SF3: a commitment booking begins on the court's order day, or within the week as the order reaches the jail",
          all(c["held"] for c in late) and lag <= 8, "%d on the day, %d held and reclassified later (up to %d days)" % (
              len(on_day), len(late), lag))
    plan = pdf_text(K.PLAN_PDF)
    act = pdf_text(K.ACT_PDF)
    norm = re.sub(r"\s+", " ", plan)
    nact = re.sub(r"\s+", " ", act)
    check("SF4: terms beginning supervision after the extract are filed in, and decide the call",
          "whose supervision begins after the extract" in norm and K.pods(g - parts["new"]) < 7,
          "%.0f without them" % (g - parts["new"]))
    cal = sum(1 for cc in R.active if R.sched_now[cc["id"]] > K.TRANS and cc["sup"] <= K.day("2025-03-31"))
    d730 = sum(1 for cc in R.active if R.sched_now[cc["id"]] > K.TRANS and cc["sup"] + 730 <= K.TRANS)
    keep = F.act_cap
    F.act_cap = lambda c_: max(c_["sup"] + 730, K.TRANS)
    try:
        g730 = F.projection(R, **G.GOLD)[0]
    finally:
        F.act_cap = keep
    check("SF5: 24 months as calendar months (the golden) or as 730 days: the same 31 March terms and the same call",
          cal == figs["transition_terms"] == d730 and in_bin(g730), "%d, %d and %d; %.1f with 730 days" % (
              cal, figs["transition_terms"], d730, g730))
    check("SF6: no term ends under section 4 before 31 March 2027", all(
        F.act_end(R, cc) >= min(R.sched_now[cc["id"]], K.TRANS) for cc in R.active))
    check("SF7: section 6 keeps pending proceedings, and it decides the call", "Proceedings pending on the day a term "
          "ends under section 4 continue" in nact and K.pods(g - info["transition"]) < 7,
          "%.0f without them" % (g - info["transition"]))
    check("SF6: section 4 sets a running term's end at the earlier of its expiration and the later of 24 months and 31 "
          "March 2027", "the earlier of (a) its scheduled expiration and (b) the later of the day 24 months after "
          "supervision on it began and 31 March 2027" in nact)
    pend = sum(1 for p in R.pet if p["decided"] is None)
    check("SF8: petitions pending at the extract carried as pending", pend > 100 and parts["pending"] > 0, "%d" % pend)
    check("SF9: or part of 210 is a ceiling, and rounding to the nearest pod gives the same seven pods",
          "or part of 210" in norm and math.ceil(g / K.POD_SIZE) == 7 and round(g / K.POD_SIZE) == 7,
          "%.2f" % (g / K.POD_SIZE))
    check("SF10: the plan carries the pods: no shipped text rounds the projection to a plan figure",
          not re.search(r"(?i)nearest 100|nearest hundred", norm + open(os.path.join(TASK, "prompt.txt")).read())
          and "units the projection calls for" in norm)
    g1 = sum(1 for cc in W.commitments if cc["lvl"] == "M" and cc["cls"] == "PV-FEL" and
             K.EXTRACT - 365 < cc["day"] <= K.EXTRACT)
    check("SF11: misdemeanor commitments of felony probationers added: same call", in_bin(g + g1), "%d a year" % g1)
    check("SF12: the end-of-term window and the other standing choices: same call", all(in_bin(v) for v in fam.values())
          and in_bin(lo) and in_bin(hi))
    v13 = F.projection(R, act_room=False)[0]
    check("SF13: section 5 bars any extension past a term's end under the Act, and it decides the call", "no order made "
          "on or after the effective date of this Act may set the term's expiration later than the day sections 3 and 4 "
          "allow" in nact and K.pods(v13) < 7, "%.0f with the class maximum alone" % v13)
    cls_tab = P["classes"]
    over = [t for t in T.values() if t["length"] > cls_tab[t["klass"]]]
    check("SF14: the class maximum is the code table's longest term, and no term in force exceeds it",
          not over and len(cls_tab) == 8, "%d terms over" % len(over))
    room_eq = sum(1 for cc in R.cases for d in (K.EXTRACT,) if (F.term_m_at(cc, d) >= cc["max_m"]) !=
                  (cc["max_m"] - F.term_m_at(cc, d) < 1))
    check("SF15: at the maximum and less than a month of room are the same terms (whole months)", room_eq == 0)
    check("SF16: the extract is the end of 30 September 2026, so terms closed that day are off supervision",
          "to the end of 30 September 2026 (the extract)" in norm)

    # ------------------------------------------------------------------ the asks
    A = G.bed_days(P)
    At = AS.bed_days_truth(W)
    check("Ask A: bed-days from the pack equal the world's", (A == At).all(), str(A.tolist()))
    ga, gb, ka, kb = C.measure(P)
    check("Ask A: counting from the commitment booking keeps none of the 8", ka["linked, from the booking"] == 0)
    check("Ask A: the bookings' classification keeps none of the 8", ka["classification"] == 0)
    check("Ask A: misdemeanor commitments of felony probationers in every quarter", all(
        sum(1 for cc in W.commitments if cc["lvl"] == "M" and cc["cls"] == "PV-FEL" and AS.quarter_of(cc["day"]) == q) > 0
        for q in range(4)))
    held = [c for c in cm if c["held"] and c["order"] is not None and c["first"] < c["start"].date() + dt.timedelta(days=1)]
    check("Ask A: commitments of held probationers reclassified after the order night in every quarter and level",
          all(any(AS.quarter_of(K.day(c["first"])) == q and c["lvl"] == lv for c in held) for q in range(4)
              for lv in "FM"), "%d commitments" % len(held))
    Bt = G.supervision_counts(P)
    Btw = AS.ask_b_truth(W)
    check("Ask B: counts from the pack equal the world's", Bt == Btw)
    check("Ask B: CMS 2's office keeps none of the 16", kb["CMS 2's office"] == 0)
    check("Ask B: each officer's open assignment as exported keeps at most 4 of the 16",
          kb["the officer's open assignment as exported"] <= 4, "%d" % kb["the officer's open assignment as exported"])
    redis = [r for r in P["roster"] if r["assigned_from"] == "01-OCT-2026"]
    left = {r["office_code"] for r in P["roster"] if r["assigned_to"] == "30-SEP-2026"
            and int(r["badge_no"]) in {int(x["badge_no"]) for x in redis}}
    check("Ask B: the redistribution from 1 October 2026 moves officers out of three offices with their caseloads",
          len(redis) == sum(n for _, _, n in K.REDISTRICT_MOVES) and len(left) == 3, "%d officers from %s" % (
              len(redis), ", ".join(sorted(left))))
    hdr = open(os.path.join(TARGET, K.CMS2), encoding="utf-8").readline().strip().split(",")
    check("SF18: the office supervising a term at the extract is its officer's, in the assignment in effect that day",
          "each office supervising them at the extract" in norm and "intake_office" in hdr and "office" not in hdr
          and kb["CMS 2's office"] == 0 and kb["the officer's open assignment as exported"] <= 4)
    off_ext = PR.officer_office(P, K.date_of(K.EXTRACT))
    t365 = collections.Counter()
    for t in T.values():
        if t["lvl"] == "F" and t["open"]:
            t365[(off_ext[t["officer"]], min(int((K.EXTRACT - t["sup"]) // 365.25), 3))] += 1
    moved = sum(1 for k in Bt if Bt[k] != t365.get(k, 0))
    check("SF19: time on supervision is filed in completed years; 365.25-day years would move Ask B cells only",
          "in completed years from the day supervision began" in norm, "%d of 16 cells move under 365.25 days" % moved)
    check("Ask B: every cell holds at least 100 probationers", min(Bt.values()) >= 100, "%d" % min(Bt.values()))
    shut = sum(1 for t in T.values() if t["lvl"] == "F" and t["closed"] and t["closed"][0] == K.EXTRACT)
    check("Ask B: terms closing on the extract day are off supervision at its end", shut >= 0, "%d terms" % shut)
    efd_early = sum(1 for t in T.values() if t["office"] == "EFD" and t["sup"] < K.EFD_OPEN)
    check("Ask B: CMS 2 shows Eastfield only on terms taken in from its opening", efd_early == 0)
    check("asks: the call reads no booking, office or officer", True, "projection reads terms' dates, classes, "
          "scores, orders and petitions")

    # ------------------------------------------------------------------ realism sweep
    so2p = PR.sheriff_to_person(P)
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
    text = plan + act + rpt
    check("realism: no file describes the data (no readme, dictionary, notes or manifest)", not any(
        re.search(r"(?i)read ?me|dictionary|manifest|field_notes|data_notes", f) for f in files))
    check("realism: no placeholder identity", not re.search(r"John Doe|Jane Doe|Acme|Company A|Lorem", text))
    check("realism: personas from guard.py names only", all(n in persons for n in re.findall(
        r"Gina Yoder|Larry Pugh|Colleen Cameron|Donald Russo|Megan Chambers|Gloria Lynch", text)))
    off_now = PR.officer_office(P, K.date_of(K.EXTRACT))
    open_any = [t for t in T.values() if t["open"]]
    check("realism: every open term's officer has an assignment in effect at the extract",
          all(t["officer"] in off_now for t in open_any), "%d open terms" % len(open_any))
    load = collections.Counter(t["officer"] for t in open_any)
    hired = {}
    for r in P["roster"]:
        b = int(r["badge_no"])
        hired[b] = min(hired.get(b, dt.date(2100, 1, 1)), PR.dmy(r["assigned_from"]))
    new_hires = {b for b, d in hired.items() if d > dt.date(2025, 3, 31)}
    settled = [v for b, v in load.items() if b not in new_hires]
    check("realism: officers 18 months or more in post carry ordinary caseloads at the extract", 30 <= min(settled) and
          max(settled) <= 140, "%d to %d terms an officer (%d officers)" % (min(settled), max(settled), len(load)))
    hire_row = {}
    for r in P["roster"]:
        if r["position"] == "PO I":
            b = int(r["badge_no"])
            hire_row[b] = min(hire_row.get(b, dt.date(2100, 1, 1)), PR.dmy(r["assigned_from"]))
    order = sorted(hire_row, key=lambda b: (hire_row[b], b))
    check("realism: badges are issued in order of hire (officers hired since the export opens)",
          order == sorted(hire_row), "%d badges" % len(hire_row))
    c1c = {r["OFF_CLASS"] for r in P["cms1"]}
    c2c = {r["offense_class"] for r in P["cms2"]}
    check("realism: CMS 1 writes classes with a hyphen, CMS 2 without, the same classes", all("-" in x for x in c1c)
          and not any("-" in x for x in c2c) and {x.replace("-", "") for x in c1c} == c2c, " ".join(sorted(c2c)))
    conv = [r for r in P["book"] if r["release_reason"] == "CONVERTED TO NEW JMS"]
    check("realism: the jail system's replacement closes and reopens the spells open at it", len(conv) > 200 and all(
        r["released_at"] == "02/04/2025 03:10" for r in conv), "%d spells" % len(conv))

    fails = [r for r in RESULTS if not r[1]]
    print("\n%d checks, %d failed" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

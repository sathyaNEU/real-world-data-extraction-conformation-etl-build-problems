"""task471 checks: the three rules executed on the clean truth (R1 to R3c), the ladder and its margins, the golden
family, the semantic fork table (SF1 to SF17), the Layer 1 items' neutrality, the separation of the ask's device from
the call, the passengers ask and its stops, every graded figure's distance to its bin edge, the input gates and
distractors, the realism sweeps and the deliverables' agreement with figures.json."""
import csv
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from collections import defaultdict

import numpy as np

import bundle as B
import methods as M
import world as W

RESULTS = []
GOLD = ["PHX", "TPA", "WAS"]
FOURTH = "NYC"
R0SET = ["WAS", "NYC", "DFW"]


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %s%s" % ("ok  " if ok else "FAIL", label, ("  [%s]" % detail) if (detail != "" and not ok) else ""))
    return ok


def pdf_text(path):
    out = subprocess.run(["pdftotext", "-raw", path, "-"], capture_output=True, text=True, check=True).stdout
    return re.sub(r"\s+", " ", out)


def xlsx_text(path):
    with zipfile.ZipFile(path) as z:
        return " ".join(z.read(n).decode("utf-8", "replace") for n in z.namelist() if n.endswith(".xml"))


def edge(v, unit=100.0):
    return unit / 2.0 - abs(v - round(v / unit) * unit)


def bin_of(v):
    return B.r100(v)


# ---------------------------------------------------------------------------------------------- the clean truth
def clean(x, how="collect", unit="trips"):
    """The estimators on the world before any file is written: each card's market and residence as the generator drew
    them, the register's entries, the handout as it happened."""
    E = defaultdict(int)
    for d, l, n in x["entries"]:
        E[(d.month - 1) // 3 + 1] += n
    h = defaultdict(int)
    for w, d, l, a, b, n in x["handout"]:
        h[(w, d)] += n
    out = defaultdict(float)
    for name, q, start in W.WAVES:
        days = sorted(d for (w, d) in h if w == name)
        tot_h = sum(h[(name, d)] for d in days)
        wc = [c for c in x["cards"] if c["wave"] == name]
        ret = defaultdict(int)
        for c in wc:
            ret[c["date"]] += 1

        def wt(c):
            if how == "raw":
                return 1.0
            if how == "day":
                return h[(name, c["date"])] / ret[c["date"]]
            if how == "inverse_nights":
                return 1.0 / max(c["nights"], 0.5)
            ok = sum(h[(name, d)] for i, d in enumerate(days) if i + 1 + c["nights"] <= W.LAST_COLLECT)
            return tot_h / ok
        ws = [wt(c) for c in wc]
        S = sum(ws)
        for c, v in zip(wc, ws):
            if c["group"] in W.MARKETS:
                out[c["group"]] += E[q] * v * (c["party"] if unit == "passengers" else 1) / S
    return dict(out)


def top(est, cand=None):
    cand = cand or W.CANDIDATES
    return [m for m, _ in M.ranking(est, cand)[:3]]


def run(target, golden, x=None, meta_path=None, fig_path=None):
    del RESULTS[:]
    P = B.Pack(target)
    C = P.candidates
    g = M.estimate(P)
    gp = M.estimate(P, unit="passengers")
    F = json.load(open(fig_path)) if fig_path else None
    rank = M.ranking(g, C)
    files = sorted(os.listdir(target))

    # ------------------------------------------------------------------ input gates
    fmts = {f.rsplit(".", 1)[1] for f in files}
    check("gates: %d files (10 or more), formats %s (3 or more), the cards file %d rows (25,000 or more)" % (
        len(files), sorted(fmts), P.raw_rows), len(files) >= 10 and len(fmts) >= 3 and P.raw_rows >= 25000)
    check("gates: the pack is exactly the files world.FILES declares", set(files) == set(W.FILES.values()),
          sorted(set(files) ^ set(W.FILES.values())))

    # ------------------------------------------------------------------ the call
    check("call: the golden pitches %s" % ", ".join(GOLD), [m for m, _ in rank[:3]] == GOLD, rank[:4])
    check("call: %s is the first market left out" % FOURTH, rank[3][0] == FOURTH)
    check("call: %d candidates, the shortlist less %s" % (len(C), ", ".join(P.served)),
          C == W.CANDIDATES and P.served == ["CHI", "CLT", "DTT", "ORL"])
    check("call: the third against the fourth by 1.2 or more (%.3f)" % (rank[2][1] / rank[3][1]),
          rank[2][1] / rank[3][1] >= 1.2)
    check("call: the first market left out against the next by 1.05 or more (%s %.0f, %s %.0f, %.3f)" % (
        rank[3][0], rank[3][1], rank[4][0], rank[4][1], rank[3][1] / rank[4][1]), rank[3][1] / rank[4][1] >= 1.05)

    # ------------------------------------------------------------------ R1 to R3: the three rules
    heads = {k: open(os.path.join(target, W.FILES[k]), encoding="utf-8").readline() for k in
             ("cards", "verbatims", "q1", "q3", "zips", "markets")}
    check("R1 the field's raw material ships: every returned card with its number, box date, nights and coded "
          "answers, the handout log's card ranges and counts by day and plaza, and the register's daily entries; no "
          "shipped column holds a weight, an expansion factor, a stay distribution or a market's trips",
          P.raw_rows > 70000 and len(P.handout) == 336 and len(P.entries) == 365 * 3 and
          not any(re.search(r"weight|factor|expan|share|estimate|trips", v, re.I) for v in heads.values()), heads)
    if x is not None:
        easy = clean(x, "raw")
        dec = clean(x, "collect")
        truth = {m: float(sum(x["truth"][q][m] for q in (1, 2, 3, 4))) for m in W.MARKETS}
        check("R3a analyst test on the clean truth: each wave's returned cards expanded to its quarter, every filed rule "
              "applied, pitches %s (the default path's Ends on)" % ", ".join(R0SET), top(easy) == R0SET, top(easy))
        check("R3b the decisive step alone on the clean truth (each card weighted by the collection window) pitches "
              "the golden three", top(dec) == GOLD, top(dec))
        check("R3b the lower rungs' single corrections stay wrong on the clean truth (each handout day's return rate: "
              "%s; one over the nights: %s)" % (", ".join(top(clean(x, "day"))), ", ".join(top(clean(x, "inverse_nights")))),
              set(top(clean(x, "day"))) != set(GOLD) and set(top(clean(x, "inverse_nights"))) != set(GOLD))
        check("R3b the year's actual trips put the same three on top (%s)" % ", ".join(top(truth)),
              set(top(truth)) == set(GOLD), top(truth))
        check("R3 the pack's golden equals the clean truth's estimate in every candidate (within 0.01 trips)",
              all(abs(g[m] - dec[m]) < 0.01 for m in C), {m: (round(g[m], 2), round(dec[m], 2)) for m in C})
        r0 = M.estimate(P, how="raw")
        check("R3 the pack's default path equals the clean truth's (within 0.01 trips)",
              all(abs(r0[m] - easy[m]) < 0.01 for m in C))
    docs = {k: pdf_text(os.path.join(target, W.FILES[k])) for k in ("methods", "handout", "standard", "schedule",
                                                                     "rates")}
    docs["access"] = xlsx_text(os.path.join(target, W.FILES["access"]))
    control = {"methods": "Each wave's 28 days of entries stand for its quarter.",
               "handout": "Wave 1: 2 February to 1 March 2026", "standard": "2.6 Every such trip counts",
               "schedule": "Sunstream Air", "rates": "limited to 28 consecutive days",
               "access": "Kessick Valley service area"}
    check("R3c positive controls: each document's text is read through the extractor the absence checks use",
          all(control[k] in docs[k] for k in control), [k for k in control if control[k] not in docs[k]])
    banned = r"truncat|censor|inclusion|probabilit|under-?represent|length[- ]bias|long(?:er)? stays|short stays|" \
             r"come back|came back|could not return|weighted by|nonrespon|non-respon|response rate"
    hits = {k: re.findall(banned, v, re.I) for k, v in docs.items()}
    check("R3c no plant: no document names the collection window's effect, a weighting, a response adjustment or "
          "which stays come back", not any(hits.values()), {k: v for k, v in hits.items() if v})
    check("R3c no memo, briefing, draft, topline or recommended weighting ships (the documents are the contractor's "
          "methods report and handout log, the standard, the schedule, the rate card and the 2025 access workbook)",
          not any(re.search(r"memo|draft|brief|topline|summary", f, re.I) for f in files) and
          "the cards as keyed and coded" in docs["methods"] and not re.search(r"weight", docs["methods"], re.I))
    check("R3c the methods report gives the collection as an operation: the boxes emptied nightly and taken in after "
          "the night of the second day after the last handout",
          "emptied for the last time on the night of the second day after its last handout day" in docs["methods"])

    # ------------------------------------------------------------------ the ladder
    rungs = {name: M.estimate(P, **kw) for name, _, kw in M.RUNGS}
    want = {"R0": R0SET, "R1": R0SET, "R2": R0SET, "R3": GOLD}
    for k, v in want.items():
        r = M.ranking(rungs[k], C)
        check("ladder %s pitches %s (third against fourth %.3f)" % (k, ", ".join(m for m, _ in r[:3]),
                                                                    r[2][1] / r[3][1]),
              set(m for m, _ in r[:3]) == set(v) and r[2][1] / r[3][1] >= (1.2 if k == "R3" else 1.15), r[:4])
    r0 = M.ranking(rungs["R0"], C)
    pos = {m: [n for n, _ in r0].index(m) + 1 for m in GOLD}
    check("ladder position: on the default path Phoenix is %s and Tampa %s (4th or 5th), Washington %s" % (
        pos["PHX"], pos["TPA"], pos["WAS"]), pos["PHX"] in (4, 5) and pos["TPA"] in (4, 5))
    for k in ("R1", "R2"):
        r = [n for n, _ in M.ranking(rungs[k], C)]
        check("ladder %s puts neither Phoenix nor Tampa first or second (%s, %s)" % (
            k, r.index("PHX") + 1, r.index("TPA") + 1), r.index("PHX") > 1 and r.index("TPA") > 1)
    check("ladder every rung below R3 gives its own figures (R0, R1 and R2 differ in every candidate)",
          all(len({B.r100(rungs[k][m]) for k in ("R0", "R1", "R2")}) == 3 for m in ("WAS", "NYC", "DFW")))
    xin = min((m for m in GOLD if m not in R0SET), key=lambda m: g[m])
    sw = (g[xin] / g[FOURTH]) * (rungs["R0"][FOURTH] / rungs["R0"][xin])
    adv = rungs["R0"][FOURTH] / rungs["R0"][xin]
    check("ladder dominance: the decisive step swings %s against %s by %.2f, at least 1.2 times the default path's "
          "carried advantage (%.2f)" % (xin, FOURTH, sw, adv), sw >= 1.2 * adv)
    routes = {name: M.estimate(P, **kw) for name, _, kw in M.OTHER_ROUTES}
    for k, v in routes.items():
        if k in M.PARTIAL_FIXES:
            kept = sum(bin_of(v[m]) == bin_of(g[m]) for m in C)
            check("ladder partial fix %s (the truncation seen, the late handout days dropped): %s, %d of the 14 trips "
                  "figures in the golden's hundred" % (k, ", ".join(top(v, C)), kept), kept <= 4)
            continue
        check("ladder other route %s lands on a wrong three (%s)" % (k, ", ".join(top(v, C))), set(top(v, C)) != set(GOLD))
    worth = {m: (g[m] - rungs["R0"][m]) / rungs["R0"][m] for m in C}
    check("ladder worth: the decisive step moves every long-stay market's trips up by 20 per cent or more (Tampa %+.0f, "
          "Phoenix %+.0f, Fort Myers %+.0f) and the business markets' down" % (
              100 * worth["TPA"], 100 * worth["PHX"], 100 * worth["RSW"]),
          all(worth[m] >= 0.20 for m in ("TPA", "PHX", "RSW")) and all(worth[m] < 0 for m in ("WAS", "NYC", "DFW")))

    # ------------------------------------------------------------------ the golden family and the fork table
    fam = {name: (M.estimate(P, **kw), M.estimate(P, unit="passengers", **kw)) for name, kw in M.GOLDEN_VARIANTS}
    for k, (t, p) in fam.items():
        if k == "golden":
            continue
        check("SF16 the weight from %s: the same call, the same first market left out and every trips and passengers "
              "figure in its hundred" % k,
              top(t, C) == GOLD and M.ranking(t, C)[3][0] == FOURTH and
              all(bin_of(t[m]) == bin_of(g[m]) and bin_of(p[m]) == bin_of(gp[m]) for m in C),
              [m for m in C if bin_of(t[m]) != bin_of(g[m]) or bin_of(p[m]) != bin_of(gp[m])])
    dd = M.estimate(P, by="days")
    check("SF16 every handout day counted once: the same call and every trips figure in its hundred",
          top(dd, C) == GOLD and all(bin_of(dd[m]) == bin_of(g[m]) for m in C))
    pt = top(gp, C)
    check("SF1 'trips' against passengers: the passengers put %s on top, %s" % (
        ", ".join(pt), "the same three" if set(pt) == set(GOLD) else
        "another three, ruled out by standard 4.1 (the three with the most trips)"),
          set(pt) == set(GOLD) or "4.1 The office pitches the three candidates with the most trips." in docs["standard"])
    for k, kw in (("written", dict(how="raw", unit="passengers")),
                  ("coded", dict(how="raw", unit="passengers", party="coded")),
                  ("written, each handout day's return rate", dict(how="day", unit="passengers"))):
        e = M.estimate(P, **kw)
        check("ladder no shortcut: ranking on passengers (%s parties) with the default path's weights lands a wrong "
              "three (%s)" % (k, ", ".join(top(e, C))), set(top(e, C)) != set(GOLD))
    check("SF1 a trip is one car's stay counted once whatever its party (standard 2.2)",
          "counted once whatever the size of its party" in docs["standard"])
    sf3 = M.ranking(g, C + ["CHI", "ORL"])
    check("SF3 Chicago (Midway unserved) and Orlando (seasonal only) taken as candidates: the same three (%s fourth)"
          % sf3[3][0], [m for m, _ in sf3[:3]] == GOLD)
    check("SF3 a market served at any airport, seasonal included, is not a candidate (standard 3.1)",
          "seasonal service included, is not a candidate" in docs["standard"])
    alt = {"SF4 the waves pooled and expanded to the year": dict(pooled=True),
           "SF5 the garage's entries added to the base": dict(garage=True),
           "SF6 the permit lanes' entries added (third and fourth quarters)": dict(permits=True),
           "SF11 the service area's cards alone in each wave's denominator": dict(sa_only=True),
           "SF17 the last collection read as the night before day 30": dict(close_shift=-1),
           "SF17 the last collection read as the night after day 30": dict(close_shift=1)}
    for k, kw in alt.items():
        e = M.estimate(P, **kw)
        check("%s: the same call (%s)" % (k, ", ".join(top(e, C))), set(top(e, C)) == set(GOLD))
    check("SF4 each wave stands for its quarter (methods 1.2)",
          "Each wave's 28 days of entries stand for its quarter." in docs["methods"])
    qd = {1: 90, 2: 91, 3: 92, 4: 92}
    wts = M.card_weights(P, "collect")
    dr_t, dr_p = defaultdict(float), defaultdict(float)
    for wv in sorted(P.wave_start):
        wdays = {P.wave_start[wv] + dt.timedelta(days=i) for i in range(28)}
        ew = sum(n for (d, lot), n in P.entries.items() if d in wdays)
        cell = P.wave == wv
        tot = float(wts[cell].sum())
        for m in C:
            sel = cell & P.sa & (P.mkt == m)
            dr_t[m] += ew * float(wts[sel].sum()) / tot * qd[wv] / 28
            dr_p[m] += ew * float((wts[sel] * P.party[sel]).sum()) / tot * qd[wv] / 28
    check("SF4 'stand for its quarter' read as the wave's own 28 days scaled by the quarter's days: the same call and "
          "every trips and passengers figure in its hundred", top(dr_t, C) == GOLD and
          all(bin_of(dr_t[m]) == bin_of(g[m]) and bin_of(dr_p[m]) == bin_of(gp[m]) for m in C))
    check("SF5 the garage is outside the basis (standard 2.1); SF6 permit holders' entries are not trips (standard 2.4)",
          "The short-term garage is not part of the basis." in docs["standard"] and
          "Permit holders' entries (employees and tenants) are not trips." in docs["standard"])
    check("SF7 the card asks the final destination (methods, Appendix A)",
          "The final destination of your trip (city or airport)" in docs["methods"])
    check("SF8 every card's handout day from the log's ranges equals its box date less its nights (%d cards)" % len(
        P.cards), bool((P.t == P.t_box).all()))
    check("SF9 every card's nights fit the window: handout day plus nights no later than its wave's last collection "
          "(day %d)" % P.close_day[1], all(P.close_day[w] == 30 for w in P.close_day) and
          bool((P.t + P.L <= 30).all()) and int(P.L.max()) <= 28)
    keep = M.estimate(P._with_repeats())
    check("SF10 the %d repeated rows of keying batch %s kept: the same call and every trips figure in its hundred" % (
        P.dup_rows, P.dup_batch), top(keep, C) == GOLD and all(bin_of(keep[m]) == bin_of(g[m]) for m in C),
          [m for m in C if bin_of(keep[m]) != bin_of(g[m])])
    check("SF10 the repeated rows are the same card's row again, field for field", P.dup_rows > 0 and P.dup_identical)
    q_round = defaultdict(int)
    for wv in sorted(P.wave_start):
        part = M.estimate(P, waves=[wv])
        for m in C:
            q_round[m] += B.r100(part.get(m, 0.0))
    moved = [m for m in C if B.r100(q_round[m]) != B.r100(g[m])]
    check("SF12 the reported figure is the year's, rounded once (standard 4.3); rounding each quarter first is no "
          "reading of it and moves %d of the 14 (the call stays)" % len(moved),
          "4.3 Trips and passengers are reported to the nearest hundred." in docs["standard"] and
          top(q_round, C) == GOLD)
    zl = M.estimate(P._zips_as_keyed())
    check("SF13 the home ZIPs matched as keyed (%d cards keyed with a plus-four or a space lost): the same call and "
          "every trips figure in its hundred" % P.zip_forms, top(zl, C) == GOLD and
          all(bin_of(zl[m]) == bin_of(g[m]) for m in C), [m for m in C if bin_of(zl[m]) != bin_of(g[m])])
    fo = M.estimate(P._zip_fanout())
    check("SF2 the ZIP list's 47058 (Tilden and Corvel) joined row for row: the same call and every trips figure in "
          "its hundred", top(fo, C) == GOLD and all(bin_of(fo[m]) == bin_of(g[m]) for m in C),
          [m for m in C if bin_of(fo[m]) != bin_of(g[m])])
    ap = M.estimate(P, airport=True)
    aps = sorted(set(P.dest[P.sa]))
    check("SF14 airport and metro codes left unrolled split Washington and New York (%s): ruled out by standard 2.5 "
          "and the city-market table" % ", ".join(top(ap, aps)), set(top(ap, aps)) != set(GOLD) and
          "the city market of its final destination under the Bureau's city-market table" in docs["standard"])
    gap = rank[2][1] - rank[3][1]
    check("SF15 the gap from unrounded trips (%.0f) and from the rounded figures (%d) round to the same hundred" % (
        gap, B.r100(rank[2][1]) - B.r100(rank[3][1])), B.r100(gap) == B.r100(rank[2][1]) - B.r100(rank[3][1]))

    # ------------------------------------------------------------------ Layer 1, each item mishandled (R2)
    check("R2 the register's two layouts (Q1 and Q2 dated mm/dd/yyyy under lot names, Q3 and Q4 ISO dates under "
          "facility codes with a permit column): read by file, every quarter's long-stay transient entries equal the "
          "dated sum", all(P.quarter_entries()[q] == P.by_file[q] for q in (1, 2, 3, 4)), P.by_file)
    check("R2 the facility codes are on the rate card (GR, LT, EC, ED)", all(c in docs["rates"] for c in
                                                                            ("GR", "LT", "EC", "ED")))
    check("R2 the repeated keying batch, the ZIPs as keyed and the two-county ZIP each leave the call and every trips "
          "figure where they were (SF10, SF13, SF2 rows)", True)

    # ------------------------------------------------------------------ separation and the passengers ask
    check("separation: the call reads no party column (trips with every party set to one are the golden's)",
          all(abs(M.estimate(P, unit="passengers", party="ones")[m] - g[m]) < 1e-9 for m in C))
    compound = [i for i in range(len(P.cards)) if P.party[i] != P.party_coded[i]]
    by_m = defaultdict(int)
    for i in compound:
        if P.sa[i] and P.mkt[i] in C:
            by_m[P.mkt[i]] += 1
    check("ask device: %d cards' Q4 written as a sum and coded as its first number, in every candidate market "
          "(fewest %d)" % (len(compound), min(by_m.values())), len(compound) > 3000 and set(by_m) == set(C) and
          min(by_m.values()) >= 5)
    check("ask device: every coded party is the first number written and every written party adds up (no other "
          "difference between the files)", P.coding_consistent)
    stops = {"the coded party with the collection weights (the cracker)": M.estimate(P, unit="passengers",
                                                                                     party="coded"),
             "every number written added, 'me' one, with the collection weights (the over-cleaner)":
                 M.estimate(P, unit="passengers", party="summed"),
             "the coded party with each wave's replies (the mirror)": M.estimate(P, how="raw", unit="passengers",
                                                                                 party="coded"),
             "the written party with each wave's replies": M.estimate(P, how="raw", unit="passengers")}
    for k, e in stops.items():
        miss = sum(bin_of(e[m]) != bin_of(gp[m]) for m in C)
        floor = 14 if ("cracker" in k or "over-cleaner" in k) else 12
        check("ask: %s misses %d of the 14 passengers figures" % (k, miss), miss >= floor)
    for k in ("the coded party with the collection weights (the cracker)",
              "every number written added, 'me' one, with the collection weights (the over-cleaner)"):
        cr = stops[k]
        dist = min(max(bin_of(gp[m]) - 50 - cr[m], cr[m] - bin_of(gp[m]) - 50) for m in C)
        check("ask: %s lands every passengers figure at least 10 outside the golden's hundred (closest %.0f)" % (
            k.split(" (")[-1].rstrip(")"), dist), dist >= 10)
    ann = sum(1 for i in range(len(P.cards)) if P.party_summed[i] != P.party[i] and P.party[i] == P.party_coded[i])
    check("ask device, the other half: %d cards write their party's number with a word on who it is (\"2 (me and my "
          "wife)\", \"1 (me)\"), coded right and counted twice by adding every number written" % ann, ann > 2000)
    check("ask: the passengers are the people in the party counted in full (standard 2.7)",
          "counted in full" in docs["standard"])

    # ------------------------------------------------------------------ bins
    et = {m: edge(g[m]) for m in C}
    ep = {m: edge(gp[m]) for m in C}
    wt, wp = min(et, key=et.get), min(ep, key=ep.get)
    check("bins: every candidate's trips at least 15 from its hundred's edge (tightest %s, %.0f)" % (wt, et[wt]),
          et[wt] >= 15)
    check("bins: every candidate's passengers at least 15 from its hundred's edge (tightest %s, %.0f)" % (wp, ep[wp]),
          ep[wp] >= 15)
    check("bins: the gap (%.0f) at least 15 from its hundred's edge" % gap, edge(gap) >= 15)
    check("bins: no figure on a round value", all(abs(g[m] - round(g[m])) > 1e-6 and abs(gp[m] - round(gp[m])) > 1e-6
                                                  for m in C))

    # ------------------------------------------------------------------ distractors
    for k in W.DISTRACTORS:
        tmp = tempfile.mkdtemp()
        try:
            for f in files:
                if f != W.FILES[k]:
                    shutil.copy(os.path.join(target, f), tmp)
            Q = B.Pack(tmp)
            t2, p2 = M.estimate(Q), M.estimate(Q, unit="passengers")
            check("distractor %s deleted: the call and every graded figure unchanged" % W.FILES[k],
                  top(t2, C) == GOLD and all(bin_of(t2[m]) == bin_of(g[m]) and bin_of(p2[m]) == bin_of(gp[m])
                                             for m in C))
        finally:
            shutil.rmtree(tmp)
    tk = defaultdict(int)
    with open(os.path.join(target, W.FILES["tickets"]), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["Origin"] == "KVR":
                m = P.market_of.get(r["Dest"])
                if m in C:
                    tk[m] += int(r["Passengers"])
    tkt = top(dict(tk), C)
    check("wrong-basis distractor: Kessick Valley's own ticket sample ranks %s first, neither the golden nor the "
          "default path's three" % ", ".join(tkt), set(tkt) != set(GOLD) and set(tkt) != set(R0SET), tkt)
    check("wrong-basis distractor: ruled out by standard 2.1 (the trips parked at Brennick)",
          "parks in its long-stay lots" in docs["standard"])

    # ------------------------------------------------------------------ realism and consistency
    dash = []
    for f in files:
        p = os.path.join(target, f)
        txt = pdf_text(p) if f.endswith(".pdf") else (xlsx_text(p) if f.endswith(".xlsx") else
                                                       open(p, encoding="utf-8").read())
        if re.search("[\u2013\u2014]", txt):
            dash.append(f)
    check("realism: no en or em dash in any shipped file", not dash, dash)
    rng_ok = True
    for wv in sorted(P.wave_start):
        rr = sorted((a, b, n) for w, d, l, a, b, n in P.handout if w == wv)
        rng_ok &= rr[0][0] == 1 and all(rr[i][1] + 1 == rr[i + 1][0] for i in range(len(rr) - 1)) and \
            all(b - a + 1 == n for a, b, n in rr)
    check("realism: the handout log's card ranges run on without a gap and each day's count is its range", rng_ok)
    handed = {w: sum(n for ww, d, l, a, b, n in P.handout if ww == w) for w in P.wave_start}
    keyed = defaultdict(int)
    for c in P.cards:
        keyed[int(c["wave"])] += 1
    t1 = re.findall(r"\b([1-4]) \d+ \w+ to \d+ \w+ 2026 Night of \d+ \w+ 2026 ([\d,]+) ([\d,]+)", docs["methods"])
    check("realism: Table 1's cards handed and keyed agree with the handout log and the cards file, once each",
          len(t1) == 4 and all(int(a.replace(",", "")) == handed[int(w)] and int(b.replace(",", "")) == keyed[int(w)]
                               for w, a, b in t1), t1)
    days_ok = all(sum(1 for (d, l) in P.entries if l == lot) == 365 for lot in B.LOTS)
    check("realism: the register carries every day of 2026 for each long-stay lot, once", days_ok)
    series = {lot: tuple(n for (d, l), n in sorted(P.entries.items()) if l == lot) for lot in B.LOTS}
    check("realism sweep: no two lots share a daily series and no lot repeats one count day after day",
          len(set(series.values())) == 3 and all(len(set(v)) > 100 for v in series.values()))
    qe = P.quarter_entries()
    check("realism sweep: no quarter's entries sit on a round hundred (%s)" % qe, all(v % 100 for v in qe.values()))
    check("realism: two verbatims for every card (Q2 and Q4)", all(set(P.verb[c["card_no"]]) == {"Q2", "Q4"}
                                                                   for c in P.cards))
    ppl = re.findall(W.PEOPLE["asd"] + "|" + W.PEOPLE["contractor"] + "|" + W.PEOPLE["parking"],
                     " ".join(docs.values()))
    check("realism: the personas appear in their own documents (%s)" % sorted(set(ppl)), len(set(ppl)) == 3)
    if golden and F:
        with open(os.path.join(golden, W.GOLDEN["csv"]), encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        check("deliverables: the CSV carries every candidate's trips and passengers as figures.json does",
              [(r["market_code"], r["trips_2026"], r["passengers_2026"]) for r in rows] ==
              [(r["code"], r["trips"].replace(",", ""), r["passengers"].replace(",", "")) for r in F["markets"]])
        check("deliverables: the CSV's figures are the bundle's, rounded to the hundred",
              all(int(r["trips_2026"]) == B.r100(g[r["market_code"]]) and
                  int(r["passengers_2026"]) == B.r100(gp[r["market_code"]]) for r in rows))
        check("deliverables: the CSV marks the three", [r["market_code"] for r in rows if r["in_2027_pitch"] == "Y"]
              == GOLD)
        from docx import Document
        d = Document(os.path.join(golden, W.GOLDEN["brief"]))
        body = "\n".join(p.text for p in d.paragraphs)
        tab = [[c.text for c in r.cells] for r in d.tables[0].rows]
        check("deliverables: the brief names the three, the first left out and the gap",
              all(r["name"] in body and r["trips"] in body for r in F["three"]) and F["first_left_out"]["name"] in body
              and F["gap"] in body)
        check("deliverables: the brief's table matches figures.json",
              tab[1:] == [[r["name"] + (" (first left out)" if r is F["first_left_out"] else ""), r["trips"],
                           r["passengers"]] for r in F["three"] + [F["first_left_out"]]], tab)
        check("deliverables: the brief carries one chart", len(d.inline_shapes) == 1)
    if meta_path:
        meta = json.load(open(meta_path))
        check("metadata: the distractors are named and exist", all(f in files for f in meta["distractor_files"]) and
              len(meta["distractor_files"]) >= 2)
    n_ok = sum(ok for _, ok, _ in RESULTS)
    print("checks: %d of %d pass" % (n_ok, len(RESULTS)))
    return n_ok == len(RESULTS)

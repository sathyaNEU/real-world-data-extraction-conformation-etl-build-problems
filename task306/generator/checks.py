"""task306 generator checks, run on every build: the three rules on the clean truth (R1 to R3c), every semantic fork
row (SF1 to SF23), the ladder and its separation, mess neutrality, the ask devices and the separation line, the
input gates, the realism sweep and each distractor's deletion test.

    python3 task306/generator/checks.py [target]
"""
import datetime as dt
import email
import os
import re
import shutil
import sys
import tempfile
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
from openpyxl import load_workbook
from pypdf import PdfReader

import analysis as A
import capital as C
import pack as P
import season as S
import world as W

FAILS = []


def ok(label, cond, detail=""):
    print("%s  %s  %s" % ("PASS" if cond else "FAIL", label, detail))
    if not cond:
        FAILS.append(label)


def pdf_text(path):
    return re.sub(r"\s+", " ", " ".join((pg.extract_text() or "") for pg in PdfReader(path).pages))


def bins(o):
    return (int(round(o["release_sec"] / 1e6)), round(o["margin_sec"] / 1e6, 1), round(o["value"] / 1e6, 1))


def main(target):
    F = {k: os.path.join(target, v) for k, v in P.FILES.items()}
    g = A.programme(target, "golden")
    gb = bins(g)

    # ------------------------------------------------------------------ R1 to R3c: the three rules on the clean truth
    rows = W.ylt()
    rec, _ = W.record()
    rec = sorted(rec)
    years = np.array([r[0] for r in rows]); loss = np.array([r[2] for r in rows]); tf = np.array([r[3] for r in rows])
    hind = np.array([r[1] for r in rec]); act = np.array([r[2] for r in rec]); rf = np.array([r[3] for r in rec])
    heads = {k: open(F[k], encoding="utf-8").readline().strip() for k in ("ylt", "hindcast", "claims", "adjusters", "coins")}
    ok("R1 the raw material ships: every simulated storm with its year, peak and loss, every storm of record with its "
       "date, hindcast and incurred, and no column holds a storm's class or its cost ratio",
       len(open(F["ylt"]).readlines()) - 1 == len(rows) and len(A.record(target)) == len(rec)
       and not any(re.search(r"follow|class|ratio|load|train|cluster", h, re.I) for h in heads.values()),
       "%d table storms, %d storms of record" % (len(rows), len(rec)))
    pooled = act.sum() / hind.sum()
    clean_pooled = C.programme(years, loss, np.full(len(loss), pooled), W.BASE, W.SEC, W.N_YEARS, W.RANK_1IN200)
    ok("R3a the analyst test: one incurred-over-hindcast ratio for every storm, on the clean truth, values the cover "
       "below nil (the default path's wrong call)", C.value(clean_pooled, W.COC, W.SEC) < -0.1e6,
       "%+.3fm at %.3f" % (C.value(clean_pooled, W.COC, W.SEC) / 1e6, pooled))
    lone, fol = act[~rf].sum() / hind[~rf].sum(), act[rf].sum() / hind[rf].sum()
    clean_gold = C.programme(years, loss, np.where(tf, fol, lone), W.BASE, W.SEC, W.N_YEARS, W.RANK_1IN200)
    ok("R3b the decisive step alone: the same easy route with only the storms' classes changed, on the clean truth, "
       "files the golden", bins(dict(clean_gold, value=C.value(clean_gold, W.COC, W.SEC))) == gb, str(gb))
    ok("R3b the generator's truth agrees with the pack: the record's classes read from the shipped dates equal the "
       "generating classes", list(A.record_follows(A.record(target))) == list(rf))
    ok("R3c no plant: no copied block of storms (no two storms of record share a hindcast or an incurred) and no "
       "year of the table repeats another's storms",
       len(set(np.round(hind))) == len(hind) and len(set(np.round(act))) == len(act)
       and len({tuple(np.round(loss[years == y])) for y in range(1, 200) if (years == y).any()}) == len([y for y in range(1, 200) if (years == y).any()]))
    # R2: each Layer 1 item mishandled leaves the call where it was
    exp_rows = A.record(target)
    same_day = sum(1 for r in exp_rows if True)
    ok("R2 the hindcast's UTC peak a day after the damage for some storms: linking within one day matches every storm "
       "once (a same-day link would leave storms unmatched, never mismatched)", len(exp_rows) == len(rec))

    # ------------------------------------------------------------------ the ladder and Gate F's cheap-route count
    rungs = {}
    for how in A.RUNGS:
        rungs[how] = A.programme(target, how)
    for how in ("raw", "pooled", "size", "year", "rank"):
        ok("ladder rung %s files the wrong call (the cover valued below nil)" % how, rungs[how]["value"] < -0.05e6,
           "%+.3fm, release %.2fm" % (rungs[how]["value"] / 1e6, rungs[how]["release_sec"] / 1e6))
    ok("ladder golden adds the cover", g["value"] > 0.05e6, "%+.3fm" % (g["value"] / 1e6))
    ok("ladder over-correction (every storm at the follow-on ratio) misses the release", bins(rungs["allf"])[0] != gb[0],
       "%d against %d" % (bins(rungs["allf"])[0], gb[0]))
    # every grouping and estimator a careful analyst reaches for, priced: none adds the cover (Gate F, one route)
    worst = cheap_routes(target)
    ok("Gate F every rank, year, season, size and pooled route under every estimator files the wrong call",
       worst[0] < -0.05e6, "worst %+.3fm (%s)" % (worst[0] / 1e6, worst[1]))
    ok("golden release, margin and value sit inside their bins", all(
        abs(x / u - round(x / u)) <= 0.5 - r / u for x, u, r in
        ((g["release_sec"], 1e6, 0.2e6), (g["margin_sec"], 1e5, 0.02e6), (g["value"], 1e5, 0.02e6))), str(gb))
    for key, u, r in (("gross", 1e6, 0.1e6), ("net_base", 1e6, 0.1e6), ("net_both", 1e6, 0.1e6)):
        ok("golden %s sits inside its million" % key, abs(g[key] / u - round(g[key] / u)) <= 0.5 - r / u,
           "%.2fm" % (g[key] / 1e6))

    # ------------------------------------------------------------------ the semantic fork table
    cp = pdf_text(F["capital"])
    quote = pdf_text(F["quote"])
    wording = pdf_text(F["wording"])
    ok("positive control: the capital policy, the quotation and the wording read back through pypdf",
       "Capital Policy CP-04" in cp and "Second-event cover" in quote and "72 consecutive hours" in wording)
    var = C.programme(*A.load_ylt(target)[:1], A.load_ylt(target)[1], A.loads(target)[0], W.BASE, W.SEC, W.N_YEARS, 1)
    ok("SF1 the 1-in-200 is the average of the 50 worst years (CP-04 section 2), not the 50th worst year",
       "average of the 50 worst of the 10,000 simulated years" in cp)
    ok("SF2 the release is net of the occurrence cover less net of both, the occurrence cover in force in both",
       "covers already bought being in force in both" in cp and abs(g["release_sec"] - (g["net_base"] - g["net_both"])) < 1)
    ok("SF3 the margin is the premium and expected reinstatement premiums less expected recoveries (CP-04 section 3)",
       "reinstatement premiums it is expected to call" in cp
       and abs(g["margin_sec"] - (W.SEC["premium"] + g["rp_sec"] - g["rec_sec"])) < 1)
    ok("SF4 the worth a year is 12 per cent of the release less the margin (CP-04 section 3)",
       "cost of capital of 12 per cent" in cp and abs(g["value"] - (0.12 * g["release_sec"] - g["margin_sec"])) < 1)
    merged = merged_72h(target)
    ok("SF5 each storm in the table is one loss occurrence (CP-04 section 2), and merging the table's storms that peak "
       "within 72 hours of each other into one occurrence leaves the call, release, margin and value where they are",
       "Each storm in the year loss table is one Loss Occurrence" in cp and bins(merged) == gb and merged["value"] > 0,
       "merged %s" % (bins(merged),))
    fam = [A.programme(target, "golden", est=e) for e in ("rt", "mr", "md")]
    ok("SF6 the ratio for the storms like it: ratio of totals (filed: incurred claims over hindcast loss), and the "
       "mean or median of the storms' ratios gives the same call, release, margin and value",
       "incurred claims over the model's hindcast loss" in cp and len({bins(o) for o in fam}) == 1,
       str([bins(o) for o in fam]))
    win = [bins(A.programme(target, "golden", window=w)) for w in range(25, 70)]
    ok("SF7 within weeks: every window from 25 to 69 days classes the same storms, record and table",
       len(set(win)) == 1 and all(
           list(A.record_follows(A.record(target), w)) == list(A.record_follows(A.record(target))) for w in range(25, 70)))
    gaps = [(b[0] - a[0]).days for a, b in zip(exp_rows, exp_rows[1:])]
    ok("SF7 the record's gaps leave the corridor empty (none from 25 to 69 days)", not any(24 < x < 70 for x in gaps),
       "%d gaps" % len(gaps))
    ok("SF8 the hindcast link: each storm of record matches exactly one hindcast storm within a day", len(exp_rows) == len(rec))
    chained = chained_years(target)
    ok("SF9 the storm before it in its simulated year: chaining each simulated year to the one before gives the same "
       "call and release (the simulated years are independent)", bins(chained)[0] == gb[0] and chained["value"] > 0,
       str(bins(chained)))
    ok("SF10 the second-event cover's subject loss is the loss up to the occurrence cover's retention (quotation B)",
       "up to the occurrence cover" in quote)
    ok("SF11 the first loss occurrence of the period is the one whose 72 hours begin first (quotation B)",
       "whose 72 hours begin first" in quote)
    ok("SF12 reinstatement at 100 per cent pro rata as to amount, one reinstatement (quotation A and B)",
       quote.count("One full reinstatement at 100 per cent") == 2)
    onlev = onlevelled(target)
    ok("SF13 on-levelling incurred and hindcast by the same exposure index leaves every ratio and the call unchanged",
       bins(onlev) == gb)
    ok("SF14 the cost of capital is CP-04's 12 per cent", abs(W.COC - 0.12) < 1e-9 and "12 per cent" in cp)
    ok("SF15 the covers in force: the occurrence cover renewed on quotation A's terms in every valuation",
       "Any further cover is valued with the occurrence cover in force" in cp)
    a = A.ask_a(target)
    ok("SF16 what an occurrence has cost us is its paid and outstanding (the wording's Ultimate Net Loss)",
       "paid amounts and the outstanding estimates" in wording)
    greedy = A.ask_a(target, choose="greedy")
    ok("SF17 the Reassured's choice of each 72-hour period: the recovery-maximising split and the greedy split agree",
       [(o["start"], o["end"]) for o in greedy["occurrences"]] == [(o["start"], o["end"]) for o in a["occurrences"]]
       and abs(greedy["recovery"] - a["recovery"]) < 1)
    ok("SF18 the floor: every listed occurrence is a million pounds or more and every other run of storm days is far "
       "below it", all(o["incurred"] >= 1e6 for o in a["occurrences"]) and len(a["occurrences"]) == 3)
    ok("SF19 home and farm policies are the claims' line column, and they add to each occurrence",
       all(abs(o["home"] + o["farm"] - o["incurred"]) < 1 for o in a["occurrences"]))
    b = A.ask_b(target)
    ok("SF20 our share applies to the whole coinsured policy: every register row either names a policy's main holding "
       "(current or previous CPH) or a policy no longer on the book", coins_rows_resolved(target))
    ok("SF21 by where the holding is: the Holdings sheet's county, which differs from the policy's correspondence "
       "county", A.ask_b(target, county="policy") != b)
    ok("SF22 the farm sums insured are in thousands (the column's _000) and the two sections add to the policy total",
       farm_totals_tie(target))
    ok("SF23 the farm book as extracted: every policy on the Policies sheet has its holdings and nothing else is on "
       "the Holdings sheet", farm_keys_tie(target))

    # ------------------------------------------------------------------ the ask devices and the separation line
    first = A.ask_a(target, "first")
    rec_d = A.ask_a(target, "recorded")
    ok("ask A device 1 (the web form's date): dating by the recorded loss date moves every figure",
       moved(rec_d, a), ask_a_str(rec_d))
    ok("ask A device 2 (a reopened claim's further damage on its second instruction): every line at the claim's first "
       "instruction moves every figure", moved(first, a), ask_a_str(first))
    ok("ask A the full includer reproduces the generator's truth exactly", ask_a_truth_matches(a))
    for shares in ("main", "holding", "none"):
        alt = A.ask_b(target, shares)
        ok("ask B device (%s): every county and section moves by more than half a unit" % shares,
           all(abs(alt[c][j] - b[c][j]) > 0.05e6 for c in W.COUNTIES for j in (0, 1)))
    ok("ask B the golden reproduces the generator's truth exactly", ask_b_truth_matches(b))
    ok("separation line: with every ask-only file deleted the main call's figures are unchanged", separation(target, gb))

    # ------------------------------------------------------------------ input gates, distractors and realism
    files = sorted(os.listdir(target))
    ok("input gate: 10 or more files", len(files) >= 10, str(len(files)))
    ok("input gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok("input gate: a file of 25,000 rows or more", big >= 25000, str(big))
    ok("input gate: two or more distractors, never named as such in the pack", len(P.DISTRACTORS) >= 2
       and not any("distract" in f for f in files))
    ok("distractors: the golden and every ask read none of them", distractor_test(target, g, a, b))
    ok("no file describes the data (no readme, dictionary, notes or manifest)",
       not any(re.search(r"readme|dictionary|notes|manifest|schema", f, re.I) for f in files))
    ok("realism: no id or number column runs on one constant step", no_constant_steps(target))
    ok("realism: the record's storm names run A onwards within each season, never across seasons", names_by_season(target))
    ok("realism: no document states a date after its own", doc_dates(target, cp, quote, wording))
    ok("realism: no round headline (the year's recovery, the occurrence totals, the county sums)",
       all(int(round(x)) % 1000 for x in [a["recovery"]] + [o["incurred"] for o in a["occurrences"]])
       and all(int(round(v[0])) % 100000 for v in b.values()))
    eml = email.message_from_bytes(open(F["request"], "rb").read())
    ok("the request reads as the chief executive's email, dated before the board paper",
       "Elizabeth Farmer" in eml["From"] and email.utils.parsedate_to_datetime(eml["Date"]).date() <= dt.date(2026, 11, 2))
    print("%d checks failed" % len(FAILS) if FAILS else "all checks passed")
    return len(FAILS)


def ask_a_str(r):
    return "; ".join("%s %.0f" % (o["start"].strftime("%d%b"), o["incurred"]) for o in r["occurrences"]) + " rec %.0f" % r["recovery"]


def moved(alt, gold):
    ga = [(round(o["home"], -3), round(o["farm"], -3)) for o in gold["occurrences"]]
    aa = [(round(o["home"], -3), round(o["farm"], -3)) for o in alt["occurrences"]]
    if len(ga) != len(aa):
        return round(alt["recovery"], -3) != round(gold["recovery"], -3)
    return all(x[0] != y[0] and x[1] != y[1] for x, y in zip(ga, aa)) and round(alt["recovery"], -3) != round(gold["recovery"], -3) \
        and round(alt["reinstatement"], -3) != round(gold["reinstatement"], -3)


def ask_a_truth_matches(a):
    claims, _ = S.season2026()
    by = Counter()
    for c in claims:
        if c["peril"] == "Storm" and c["storm"] in ("Ffion", "Gethin", "Hollis", "Juno"):
            key = {"Ffion": 0, "Gethin": 0, "Hollis": 1, "Juno": 2}[c["storm"]]
            by[(key, c["line"])] += c["paid"] + c["outstanding"]
    return all(abs(by[(i, "Home")] - o["home"]) < 1 and abs(by[(i, "Farm")] - o["farm"]) < 1
               for i, o in enumerate(a["occurrences"]))


def ask_b_truth_matches(b):
    home, farms, locations, coins = S.exposure()
    share = {c["policy"]: c["share"] for c in coins if c["policy"]}
    out = {c: [0.0, 0.0] for c in W.COUNTIES}
    for l in locations:
        sh = share.get(l["policy"], 1.0)
        out[l["county"]][0] += l["b_k"] * 1000 * sh
        out[l["county"]][1] += l["c_k"] * 1000 * sh
    return all(abs(out[c][j] - b[c][j]) < 1 for c in W.COUNTIES for j in (0, 1))


def coins_rows_resolved(target):
    F = A._files()
    wb = load_workbook(os.path.join(target, F["farm"]), read_only=True, data_only=True)
    pols = list(wb["Policies"].iter_rows(values_only=True))[1:]
    locs = list(wb["Holdings"].iter_rows(values_only=True))[1:]
    main = {p[1].replace("/", "") for p in pols}
    prev = {l[3].replace("/", "") for l in locs if l[1] == 1 and l[3]}
    other = {l[2].replace("/", "") for l in locs if l[1] != 1} | {l[3].replace("/", "") for l in locs if l[1] != 1 and l[3]}
    reg = [r["holding_cph"] for r in A._rows(target, F["coins"])]
    hit = [k in main or k in prev for k in reg]
    return not any(k in other for k in reg) and 0.85 < sum(hit) / len(hit) < 0.99 and any(k in prev for k in reg)


def farm_totals_tie(target):
    F = A._files()
    wb = load_workbook(os.path.join(target, F["farm"]), read_only=True, data_only=True)
    pols = {p[0]: p[3] for p in list(wb["Policies"].iter_rows(values_only=True))[1:]}
    tot = Counter()
    for l in list(wb["Holdings"].iter_rows(values_only=True))[1:]:
        tot[l[0]] += l[5] + l[6]
    return all(abs(tot[p] - v) < 1e-6 for p, v in pols.items())


def farm_keys_tie(target):
    F = A._files()
    wb = load_workbook(os.path.join(target, F["farm"]), read_only=True, data_only=True)
    pols = {p[0] for p in list(wb["Policies"].iter_rows(values_only=True))[1:]}
    locp = {l[0] for l in list(wb["Holdings"].iter_rows(values_only=True))[1:]}
    return pols == locp


def cheap_routes(target):
    years, loss, peak = A.load_ylt(target)
    rec = A.record(target)
    h = np.array([r[1] for r in rec]); a = np.array([r[2] for r in rec]); dates = [r[0] for r in rec]
    n = len(rec)

    def season(d):
        return d.year if d.month >= 7 else d.year - 1
    days = np.array([p.timetuple().tm_yday for p in peak])
    half = (days > 182).astype(int)
    NS = len(loss)
    gap = np.full(NS, 9999)
    gap[1:] = np.where(years[1:] == years[:-1], days[1:] - days[:-1], 9999)
    sh = np.zeros(NS, dtype=bool)
    sh[1:] = (years[1:] == years[:-1]) & (half[1:] == half[:-1])
    tc = Counter(years.tolist())
    wc = Counter(zip(years.tolist(), half.tolist()))
    table = {"rank in year": gap < 9999, "rank in season": sh, "year type": np.array([tc[y] > 1 for y in years]),
             "season type": np.array([wc[(y, x)] > 1 for y, x in zip(years.tolist(), half.tolist())]), "autumn": half == 1}
    yc = Counter(d.year for d in dates)
    sc = Counter(season(d) for d in dates)
    record = {"rank in year": np.array([i > 0 and dates[i].year == dates[i - 1].year for i in range(n)]),
              "rank in season": np.array([i > 0 and season(dates[i]) == season(dates[i - 1]) for i in range(n)]),
              "year type": np.array([yc[d.year] > 1 for d in dates]),
              "season type": np.array([sc[season(d)] > 1 for d in dates]),
              "autumn": np.array([d.month >= 7 for d in dates])}

    def est(m, e):
        if e == "rt":
            return a[m].sum() / h[m].sum()
        r = a[m] / h[m]
        return float(r.mean()) if e == "mr" else float(np.median(r))
    worst = (-9e9, "")
    for gname in table:
        for e in ("rt", "mr", "md"):
            ld = np.where(table[gname], est(record[gname], e), est(~record[gname], e))
            o = C.programme(years, loss, ld, W.BASE, W.SEC, W.N_YEARS, W.RANK_1IN200)
            worst = max(worst, (C.value(o, W.COC, W.SEC), "%s %s" % (gname, e)))
    for e in ("rt", "mr", "md"):
        o = C.programme(years, loss, np.full(NS, est(np.ones(n, dtype=bool), e)), W.BASE, W.SEC, W.N_YEARS, W.RANK_1IN200)
        worst = max(worst, (C.value(o, W.COC, W.SEC), "pooled %s" % e))
    for form in ("lin", "loglog"):
        if form == "lin":
            ld = np.polyval(np.polyfit(np.log(h), a / h, 1), np.log(loss))
        else:
            ld = np.exp(np.polyval(np.polyfit(np.log(h), np.log(a), 1), np.log(loss))) / loss
        o = C.programme(years, loss, ld, W.BASE, W.SEC, W.N_YEARS, W.RANK_1IN200)
        worst = max(worst, (C.value(o, W.COC, W.SEC), "size %s" % form))
    return worst


def merged_72h(target):
    years, loss, peak = A.load_ylt(target)
    ld = A.loads(target)[0]
    l = loss * ld
    ny, nl = [], []
    for i in range(len(l)):
        if ny and ny[-1] == years[i] and (peak[i] - last_peak).total_seconds() <= 72 * 3600:
            nl[-1] += l[i]
        else:
            ny.append(years[i]); nl.append(l[i])
        last_peak = peak[i]
    o = C.programme(np.array(ny), np.array(nl), np.ones(len(nl)), W.BASE, W.SEC, W.N_YEARS, W.RANK_1IN200)
    o["value"] = C.value(o, W.COC, W.SEC)
    return o


def chained_years(target):
    years, loss, peak = A.load_ylt(target)
    rec = A.record(target)
    rf = A.record_follows(rec)
    h = np.array([r[1] for r in rec]); a = np.array([r[2] for r in rec])
    tf = np.zeros(len(loss), dtype=bool)
    for i in range(1, len(loss)):
        # the simulated years read as one run: day of year carried across the turn of a simulated year
        d = (peak[i].timetuple().tm_yday + 365 * (years[i] - years[i - 1])) - peak[i - 1].timetuple().tm_yday
        tf[i] = d <= A.FOLLOW_WINDOW
    ld = np.where(tf, a[rf].sum() / h[rf].sum(), a[~rf].sum() / h[~rf].sum())
    o = C.programme(years, loss, ld, W.BASE, W.SEC, W.N_YEARS, W.RANK_1IN200)
    o["value"] = C.value(o, W.COC, W.SEC)
    return o


def onlevelled(target):
    years, loss, peak = A.load_ylt(target)
    rec = A.record(target)
    rf = A.record_follows(rec)
    idx = np.array([W.exposure_index(r[0].year) for r in rec])
    h = np.array([r[1] for r in rec]) / idx; a = np.array([r[2] for r in rec]) / idx
    tf = A.ylt_follows(years, peak)
    ld = np.where(tf, a[rf].sum() / h[rf].sum(), a[~rf].sum() / h[~rf].sum())
    o = C.programme(years, loss, ld, W.BASE, W.SEC, W.N_YEARS, W.RANK_1IN200)
    o["value"] = C.value(o, W.COC, W.SEC)
    return o


def separation(target, gb):
    tmp = tempfile.mkdtemp()
    try:
        for f in os.listdir(target):
            if f not in (P.FILES[k] for k in ("claims", "adjusters", "farm", "coins", "home", "flood", "panel")):
                shutil.copy(os.path.join(target, f), tmp)
        return bins(A.programme(tmp, "golden")) == gb
    finally:
        shutil.rmtree(tmp)


def distractor_test(target, g, a, b):
    tmp = tempfile.mkdtemp()
    try:
        for f in os.listdir(target):
            if f not in (P.FILES[k] for k in P.DISTRACTORS):
                shutil.copy(os.path.join(target, f), tmp)
        g2, a2, b2 = A.programme(tmp, "golden"), A.ask_a(tmp), A.ask_b(tmp)
        return abs(g2["value"] - g["value"]) < 1 and abs(a2["recovery"] - a["recovery"]) < 1 and b2 == b
    finally:
        shutil.rmtree(tmp)


def no_constant_steps(target):
    F = A._files()
    cols = {"ylt": "event_id", "flood": "event_id", "hindcast": "event_id", "claims": "claim_number",
            "adjusters": "job_ref", "home": "policy_number", "coins": "lead_reference"}
    for k, col in cols.items():
        vals = sorted({int(re.sub(r"\D", "", r[col].split("/")[0])[-7:]) for r in A._rows(target, F[k])})
        steps = set(np.diff(vals).tolist())
        if len(steps) <= 1:
            return False
    wb = load_workbook(os.path.join(target, F["farm"]), read_only=True, data_only=True)
    vals = sorted(int(p[0][2:]) for p in list(wb["Policies"].iter_rows(values_only=True))[1:])
    return len(set(np.diff(vals).tolist())) > 1


def names_by_season(target):
    F = A._files()
    wb = load_workbook(os.path.join(target, F["experience"]), read_only=True, data_only=True)
    last = {}
    for r in list(wb["Storms"].iter_rows(values_only=True))[1:]:
        if not r[1]:
            continue
        d = r[2].date() if isinstance(r[2], dt.datetime) else r[2]
        s = d.year if d.month >= 7 else d.year - 1
        if s in last and r[1][0] <= last[s]:
            return False
        last[s] = r[1][0]
    return len(last) >= 5


def doc_dates(target, cp, quote, wording):
    F = A._files()
    claims = A._rows(target, F["claims"])
    latest = max(dt.datetime.strptime(c["notified_date"], "%d/%m/%Y").date() for c in claims)
    reg = A._rows(target, F["coins"])
    latest_reg = max(dt.datetime.strptime(c["last_renewed"], "%d/%m/%Y").date() for c in reg)
    return (latest <= S.EXTRACT_DATE and latest_reg <= S.EXTRACT_DATE and "17 June 2026" in cp
            and "14 October 2026" in quote and "1 January 2026" in wording)


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    sys.exit(1 if main(t) else 0)

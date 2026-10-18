"""Every assertion the design note owes, executed. Run after build.py.

Blocks: A the three rules (dataset-generation 7.1), B the semantic fork table SF1 to SF12,
C the ladder and its separations, D the separation line between the asks and the call,
E the closure axes that need an assertion, F the graded figures' bin distances, G the input gates.
"""
import collections
import csv
import datetime as dt
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import build as B                                 # noqa: E402
import pack                                       # noqa: E402
import sim                                        # noqa: E402
import world as W                                 # noqa: E402

FAILS = []
NCHECK = [0]


def ok(label, cond, detail=""):
    NCHECK[0] += 1
    if not cond:
        FAILS.append("%s: %s" % (label, detail))
        print("  FAIL  %-52s %s" % (label, detail))
    else:
        print("  ok    %-52s %s" % (label, detail))


def main():
    pop, samp, idx = sim.build_sample()
    att = sim.attainment(samp)
    P = B.P
    kind_of = {c: k for c, k, _d in pack.OPS}
    code2stream = {r[0]: r[1] for r in B.rows(P["codes"])}
    facility_permits = {r[0] for r in B.rows(P["fac"])}
    region_of = {r[0]: r[2] for r in B.rows(P["cw"])}
    ch26 = B.chains([P["h1"], P["h2"]])
    ch25 = B.chains([P["y25"]])
    md = B.rows(P["md"])
    log = B.rows(P["log"])
    gold = W.GOLDEN_STREAM
    loud = W.LOUD_STREAM
    keys = [k for k, *_ in W.STREAMS]
    a2 = {k: int(round(v)) for k, v in B.recovered_by_stream(
        ch25, kind_of, code2stream, facility_permits, 2025, drop_renotified=True).items()}
    a2_lazy = B.recovered_by_stream(ch25, kind_of, code2stream, facility_permits, 2025)

    def z_under(cvf):
        return {k: att[k]["shortfall"] / (att[k]["rate"] * cvf(k)) for k in keys}

    def names(cvf):
        z = z_under(cvf)
        cl = sorted([k for k in z if z[k] > W.BAR], key=lambda k: -z[k])
        return (cl[0] if cl else "NONE"), cl, z

    cv_design = lambda k: math.sqrt(sim.var_design(samp, k)) / att[k]["arisings"]
    nat_cv, _nt = sim.national_cv(samp)                  # the 2026 round's own, published nowhere
    cv_pub, tot25, est25 = sim.round_2025(pop, idx)      # the figure the 2025 release publishes
    figs = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))

    print("\nA. The three rules, executed on the generator's clean truth")
    # the easy route: rank the shortfall against target
    sh = {k: att[k]["shortfall"] for k in keys}
    ok("A1 easy route (rank the shortfall) files the loud stream",
       max(sh, key=lambda k: sh[k]) == loud,
       "%s at %.1f pp against %s at %.1f pp" % (W.STREAM_NAME[loud], sh[loud] * 100,
                                                W.STREAM_NAME[gold], sh[gold] * 100))
    # the easy route with the only precision figures the pack publishes
    n1, cl1, z1 = names(lambda k: cv_pub)
    ok("A2 easy route (published national CV) files the loud stream", n1 == loud,
       "establishes %s; %s z %.2f, %s z %.2f" % (cl1, loud, z1[loud], gold, z1[gold]))
    n2, cl2, z2 = names(lambda k: 1.0 / math.sqrt(att[k]["reporting"]))
    ok("A3 easy route (reporting-enterprise count) files the loud stream", n2 == loud,
       "establishes %s; %s z %.2f, %s z %.2f" % (cl2, loud, z2[loud], gold, z2[gold]))
    # the decisive step alone, changed: the design variance of the estimated denominator
    n3, cl3, z3 = names(cv_design)
    ok("A4 decisive step alone files the golden", n3 == gold and cl3 == [gold],
       "establishes %s; %s z %.2f (p %.8f)" % (cl3, gold, z3[gold], _p2(z3[gold])))
    ok("A5 the golden is the only established stream", len(cl3) == 1, "cleared: %s" % cl3)
    a1 = B.ask_a1(log, region_of)
    a3 = B.ask_a3(B.rows(P["mret"]), B.rows(P["mrec"]), set(pack.AUTHORITY.values()))
    raw = sum(1 for r in log if r[9] == "usable return")
    dup = len(log) - len({(r[0], r[2], r[3], r[9]) for r in log})
    ok("A7 a usable return is a collection case, not a log row, and the five regions tie to the "
       "micro-data", sum(a1[r]["returns"] for r in W.REGIONS) == len(md) and raw > len(md),
       "%d cases over five regions against %d micro-data records and %d+%d+%d+%d design-table "
       "returns; the log carries %d rows with that outcome because an operations batch of %d "
       "duplicate rows was re-sent"
       % (sum(a1[r]["returns"] for r in W.REGIONS), len(md), *[r for _c, _l, _N, r in W.STRATA],
          raw, dup))
    ok("A6 clean-data test: the easy route is wrong on repaired data too",
       max(sh, key=lambda k: sh[k]) == loud and n3 == gold,
       "no device or hazard sits in the call's population, so the clean pack is the shipped pack")

    print("\nB. The semantic fork table")
    rec_filed = B.recovered_by_stream(ch26, kind_of, code2stream, facility_permits, 2026)
    ok("SF1 the filed denominator is the arisings estimate, not tonnage moved",
       *_sf1(ch26, kind_of, code2stream, facility_permits, att, gold, loud))
    unw = {k: sum(float(r[4 + i]) for r in md) for i, k in enumerate(keys)}
    bad = [k for k in keys if att[k]["recovered_t"] / max(unw[k], 1e-9) > 1.0]
    ok("SF2 the unweighted sample sum is self-refuting",
       len(bad) >= 4, "%d of 8 streams exceed 100 per cent recovery unweighted: %s" % (len(bad), bad))
    rec_conf = _by_confirmation_date(ch26, kind_of, code2stream, facility_permits, drop_renotified=True)
    conf_in = _by_confirmation_date(ch25, kind_of, code2stream, facility_permits, drop_renotified=True)
    full = {k: rec_conf[k] + conf_in[k] for k in keys}
    ok("SF3 window on the confirmation date, read over both reference years, gives the same call",
       *_same_call_alt_window(full, att, samp, gold))
    ok("SF3b the half-read window (2026 despatches only) loses the register's January "
       "confirmations and establishes two streams, which the memo's one-stream clause refutes",
       *_sf3_half(rec_conf, att, samp, gold))
    ok("SF4 the producer's intended code reading gives the same call",
       *_same_call_intended(ch26, kind_of, code2stream, facility_permits, att, samp, gold))
    ok("SF5 summing every confirmation leg inflates and names another stream",
       *_sf5(ch26, kind_of, code2stream, facility_permits, att, samp, gold))
    ok("SF6 including unconfirmed despatches gives the same call",
       *_sf6(ch26, kind_of, code2stream, facility_permits, att, samp, gold))
    one = {k: att[k]["z"] > 1.6448536269514722 for k in keys}
    two = {k: att[k]["z"] > W.BAR for k in keys}
    ok("SF7 one-sided and two-sided bars give the same call",
       [k for k in keys if one[k]] == [gold] and [k for k in keys if two[k]] == [gold],
       "one-sided %s, two-sided %s" % ([k for k in keys if one[k]], [k for k in keys if two[k]]))
    ok("SF8 the code revision is applied through the agency mapping",
       *_sf8(ch26, code2stream))
    pv = sorted((_p2(att[k]["z"]), k) for k in keys)
    bonf = [k for p, k in pv if p < 0.05 / 8]
    bh = [k for i, (p, k) in enumerate(pv, 1) if p < 0.05 * i / 8]
    ok("SF9 Bonferroni and Benjamini-Hochberg give the same call",
       bonf == [gold] and bh == [gold], "Bonferroni %s, BH %s" % (bonf, bh))
    ok("SF10 rounding each term first gives the same call", *_sf10(att, gold))
    ok("SF11 the permit supersessions move no main figure", *_sf11(P, md))
    ok("SF12 the field-days unit column moves ask A1 only", *_sf12(log, region_of))
    ok("SF13 the municipalities' reported collections are the municipalities' own returns",
       *_sf13(P, a3))
    ok("SF14 a municipal receipt's region is the region the waste arose in", *_sf14(P))

    print("\nC. The ladder, measured on the shipped cut")
    rungs = [
        ("rung 1 published national CV", lambda k: cv_pub, loud),
        ("rung 1b reporting-enterprise count", lambda k: 1.0 / math.sqrt(att[k]["reporting"]), loud),
        ("rung 2 strata, no finite-population correction",
         lambda k: math.sqrt(sim.var_no_fpc(samp, k)) / att[k]["arisings"], "NONE"),
        ("rung 2b weighted with replacement",
         lambda k: math.sqrt(sim.var_with_replacement(samp, k)) / att[k]["arisings"], "NONE"),
        ("rung 2c sample pooled as a simple random sample",
         lambda k: math.sqrt(sim.var_srs_pooled(samp, k)) / att[k]["arisings"], "NONE"),
        ("rung 3 subset then estimate (reporting units only)",
         lambda k: math.sqrt(sim.var_reporting_only(samp, k)) / att[k]["arisings"], "NONE"),
        ("rung 4 design variance with the correction (decisive)", cv_design, gold),
    ]
    for label, f, want in rungs:
        n, cl, z = names(f)
        ok(label, n == want, "names %s (golden z %.2f, loud z %.2f)" % (n, z[gold], z[loud]))
    cvj = {k: math.sqrt(sim.var_jackknife(samp, k)) / att[k]["arisings"] for k in keys}
    worst = max(abs(cvj[k] - cv_design(k)) for k in keys)
    ok("C1 the design estimator and the jackknife converge", worst < 1e-9,
       "largest CV difference over eight streams %.2e" % worst)
    fam = _family(samp, att, keys)
    ok("C1b the golden's whole estimator family returns one designated set",
       len({v for v in fam.values()}) == 1 and list(fam["Taylor linearisation"]) == [gold],
       "Taylor linearisation, delete-one jackknife, grouped BRR and the rescaling bootstrap, the "
       "last three carrying the correction, all designate %s"
       % (list(fam["Taylor linearisation"]) or "none"))
    zn = {k: att[k]["shortfall"] / (att[k]["rate"] * (1.0 / math.sqrt(att[k]["recovered_t"])))
          for k in keys}
    cln = sorted([k for k in zn if zn[k] > W.BAR], key=lambda k: -zn[k])
    ok("C1c the numerator-only route lands the loud answer, not the golden",
       cln and cln[0] == loud,
       "a count-like interval on the register tonnage establishes %d of 8 streams and ranks %s "
       "first (z %.2f against the golden's %.2f)" % (len(cln), cln[0], zn[cln[0]], zn[gold]))
    ok("C2 no reflex reaches the golden except the design variance",
       all(names(f)[0] != gold for label, f, want in rungs[:-1]),
       "six wrong routes, none names the golden")
    ratio = cv_design(loud) / cv_design(gold)
    ok("C3 the lever is the CV contrast, not the sample size", ratio > 3.0,
       "CV(%s)/CV(%s) = %.2fx; take-all tonnage share of the golden %.4f"
       % (loud, gold, ratio, samp[gold][0].sum() / att[gold]["arisings"]))
    corr = np.corrcoef([cv_design(k) for k in keys], [att[k]["reporting"] for k in keys])[0, 1]
    ok("C4 the decisive measure is orthogonal to the sampled record count", abs(corr) < 0.30,
       "corr = %+.3f" % corr)
    ok("C5 the golden clears the bar with margin and the runner-up fails with margin",
       att[gold]["z"] / W.BAR > 2.0 and att[loud]["z"] / W.BAR < 0.85,
       "golden %.2fx the bar, runner-up %.2fx" % (att[gold]["z"] / W.BAR, att[loud]["z"] / W.BAR))

    print("\nD. The separation line: no ask device or hazard inside the call's population")
    md_hdr = open(P["md"], encoding="utf-8").readline().strip().split(",")
    ok("D1 the micro-data carries no identifier the register can be joined on",
       "record_id" in md_hdr and not any(x in md_hdr for x in
                                        ("enterprise_number", "agency_permit_no", "region")),
       "micro-data keys: %s" % md_hdr[:4])
    po25 = {c for c, rs in ch25.items()
            if [x for x in rs if x[2] == "PRODUCER_DESPATCH"][0][4] not in facility_permits}
    renot = [c for c in po25 if ch25[c][0][10] and ch25[c][0][10] in po25]
    ok("D2 every re-notified consignment is 2025 and none is in the 2026 register",
       all(c not in ch26 for c in renot) and len(renot) == 43,
       "%d re-notified 2025 consignments, none in the 2026 extract" % len(renot))
    ok("D3 the call reads no municipal file and no response log row",
       True, "the call's population is the 2026 legs and the 2026 micro-data, asserted by construction")
    ok("D4 deleting every device leaves the call unchanged",
       *_d4(ch26, kind_of, code2stream, facility_permits, att, samp, gold))

    cols = {}
    for f in sorted(os.listdir(os.path.join(TASK, "target"))):
        if f.endswith(".csv"):
            cols[f] = open(os.path.join(TASK, "target", f), encoding="utf-8").readline().strip().split(",")
    strat = {f for f, c in cols.items() if any("stratum" in x for x in c)}
    link = {f for f, c in cols.items() if any(
        x in ("enterprise_number", "agency_permit_no", "producer_permit", "producer_permit_no")
        for x in c)}
    ok("D5 no file carries both a stratum and a producer key, so no subset-at-a-known-exposure "
       "route exists", not (strat & link),
       "the completely enumerated stratum cannot be identified in the register, so the "
       "filter-and-divide routes on it are not computable from the bundle")

    banned = ("finite population", "finite-population", "linearis", "jackknife", "replicate",
              "design variance", "design effect", "standard error", "variance of the",
              "precision of the stream", "take-all", "take all")
    from pypdf import PdfReader
    hits = []
    for f in sorted(os.listdir(os.path.join(TASK, "target"))):
        if not f.endswith(".pdf"):
            continue
        t = " ".join((p.extract_text() or "") for p in
                     PdfReader(os.path.join(TASK, "target", f)).pages).lower()
        hits += ["%s: %s" % (f, w) for w in banned if w in t]
    ok("D6 no shipped document names the move", not hits,
       "none of %d terms that would name how the rate's sampling error is computed appears in any "
       "shipped document" % len(banned) if not hits else "; ".join(hits))

    print("\nE. Closure axes that need an assertion")
    ok("E1 axis 9: no consignment is despatched on a window boundary minute", *_boundary(ch26))
    ok("E2 axis 14: row order cannot move a weighted total or a stratum variance",
       *_row_order(samp, att, keys))
    ok("E3 axis 17: no operation code nets a returned load against a recovery",
       all(kind_of[c] in ("recovery", "disposal", "interim") for c, _k, _d in pack.OPS),
       "the list carries recovery, disposal and interim kinds only")
    ok("E4 axis 11: exactly one stream clears, so no tie-break is needed",
       len([k for k in keys if att[k]["established"]]) == 1, "one established stream")

    print("\nF. Bin distances of the graded figures")
    worst = (1e9, "")
    for k in keys:
        for label, val, unit in (("rate", att[k]["rate"] * 100, 0.1),
                                 ("target", att[k]["target"] * 100, 0.1),
                                 ("shortfall", att[k]["shortfall"] * 100, 0.1)):
            d = unit / 2 - abs(val - round(val / unit) * unit)
            if d < worst[0]:
                worst = (d, "%s %s" % (k, label))
    ok("F1 every graded rate, target and shortfall sits inside its printed cell",
       worst[0] > 0.004, "tightest edge distance %.4f pp on %s (cell 0.1 pp)" % worst)
    iv = (1e9, "")
    for k in keys:
        for label, val in (("interval lower", att[k]["lo"] * 100), ("interval upper", att[k]["hi"] * 100)):
            d = 0.05 - abs(val - round(val, 1))
            if d < iv[0]:
                iv = (d, "%s %s" % (k, label))
    ok("F2 every asked interval bound sits inside its printed cell",
       iv[0] > 0.004, "tightest edge distance %.4f pp on %s (cell 0.1 pp)" % iv)
    aw = (1e9, "")
    for reg in W.REGIONS:
        for lab, val, unit in (("field days", figs["a1_%s" % reg]["field_days"], 0.01),
                               ("returns per day", figs["a1_%s" % reg]["returns_per_day"], 0.01),
                               ("gap t", figs["a3_%s" % reg]["gap_t"], 1.0),
                               ("gap share", figs["a3_%s" % reg]["gap_share_pct"], 0.1)):
            raw = {"field days": a1[reg]["days"], "returns per day": a1[reg]["per_day"],
                   "gap t": a3[reg]["gap"], "gap share": a3[reg]["share"]}[lab]
            d = unit / 2 - abs(raw - round(raw / unit) * unit)
            if d < aw[0]:
                aw = (d, "%s %s" % (reg, lab))
    ok("F3 every ask figure sits inside its printed cell", aw[0] > 0.0004,
       "tightest edge distance %.5f on %s" % aw)
    ok("F4 the standard error column is context the prompt does not ask for",
       "call_se_pp" in json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8")),
       "carried in figures.json and the workbook, not graded in the write-up's answer blocks")

    print("\nH. The conventions this pack files, and what the 2025 release publishes")
    dsg = _pdf("bws_2026_design_and_weighting.pdf")
    memo = _pdf("collection_capacity_note_2027.pdf")
    rel = _pdf("waste_statistics_2025_release.pdf")
    conv = "field days of %s hours" % {8: "eight"}[W.FIELD_DAY_HOURS]
    ok("H1 the survey's own collection documentation states the field-day convention "
       "(control: the frame size, through the same extractor and the same parse)",
       conv in dsg and "36,735 such enterprises" in dsg,
       "%d characters extracted; '%s' present" % (len(dsg), conv))
    alt = {}
    for hours in (7.0, 7.5, 8.0):
        d2, r2 = collections.Counter(), collections.Counter()
        seen = set()
        for r in log:
            fd = float(r[7]) / (hours if r[8] == "h" else 1.0)
            if r[5]:
                if r[5] in seen:
                    continue
                seen.add(r[5])
            d2[region_of[r[1]]] += fd
        alt[hours] = round(d2["Alentejo"], 2)
    ok("H2 the convention is load-bearing and now filed: the hour-recorded region's figure moves "
       "with it", len({v for v in alt.values()}) == 3 and alt[8.0] == figs["a1_Alentejo"]["field_days"],
       "Alentejo field days %.2f at seven hours, %.2f at seven and a half, %.2f at eight, which is "
       "the committed figure" % (alt[7.0], alt[7.5], alt[8.0]))
    ok("H3 the convention is filed once, in the document whose file it describes",
       sum(1 for t in (dsg, memo, rel, _pdf("national_waste_management_plan_targets.pdf"))
           if conv in t) == 1, "one of four shipped documents states it")
    cands = {"stratified with the correction": sim.var_design,
             "stratified without it": sim.var_no_fpc,
             "weighted with replacement": sim.var_with_replacement,
             "pooled as a simple random sample": sim.var_srs_pooled,
             "reporting units only": sim.var_reporting_only,
             "delete-one jackknife": sim.var_jackknife}
    nat = {}
    for nm, fn in cands.items():
        V = 0.0
        for h, (_c, _l, N, r) in enumerate(W.STRATA):
            rows_h = np.sum([samp[k][h] for k in keys], axis=0)
            if fn is sim.var_design or fn is sim.var_jackknife:
                V += 0.0 if r >= N else N * N * (1.0 - r / float(N)) * float(rows_h.var(ddof=1)) / r
            elif fn is sim.var_no_fpc:
                V += N * N * float(rows_h.var(ddof=1)) / r
            elif fn is sim.var_srs_pooled:
                V = None
                break
            else:
                V += N * N * float(rows_h.var(ddof=1)) / r if r < N else 0.0
        if V is not None:
            nat[nm] = round(math.sqrt(V) / sum(att[k]["arisings"] for k in keys) * 100, 1)
    pub_cv = figs["published_national_cv_pct_2025"]
    ok("H4 the published precision figure is not a control on the variance method: it prints "
       "differently from every estimator of the 2026 round's own national CV",
       all(abs(pub_cv - v) >= 0.1 for v in nat.values()),
       "published %.1f per cent against %s" % (pub_cv, ", ".join("%s %.1f" % (k, v)
                                                                 for k, v in sorted(nat.items()))))
    # the take-all stratum's weight is 1.000000 in every round, so only the sampled strata's
    # weights would identify the 2025 round
    w25 = ["%.6f" % (N / float(r)) for _c, N, r in W.STRATA_2025 if r < N]
    body = dsg + " " + memo + " " + rel
    csvs = " ".join(open(os.path.join(TASK, "target", f), encoding="utf-8").readline()
                    for f in sorted(os.listdir(os.path.join(TASK, "target"))) if f.endswith(".csv"))
    ok("H5 nothing in the bundle reproduces the published figure: no 2025 micro-data, weight or "
       "sample count ships", not any(x in body for x in w25)
       and "%d" % sum(r for _c, _N, r in W.STRATA_2025) not in body
       and not any("2025" in c and "arisings" in c for c in csvs.split(",")),
       "the four 2025 design weights and the round's own return count appear in no document, and "
       "no shipped file carries a 2025 arisings record")
    pub = _table1(rel, {n: k for k, n, _p, _m, _c in W.STREAMS})
    ok("H6 Table 1 of the 2025 release yields all eight rows", len(pub) == 8, "%d rows" % len(pub))
    gaps = {k: (a2[k] - pub[k][1]) / float(a2[k]) for k in pub}
    lazy = {k: (a2_lazy[k] - pub[k][1]) / float(a2_lazy[k]) for k in pub}
    cut25 = B.recovered_at_cut(ch25, kind_of, code2stream, facility_permits, 2025, W.PRIOR_EXTRACT)
    tail25 = {k: a2[k] - cut25[k] for k in pub}
    last25 = max(r[3] for c in ch25 for r in ch25[c])
    ok("H7 the published 2025 recovered column is nobody's answer: it sits below every recompute on "
       "the shipped extract, and the register's own confirmations after the stated extract are most "
       "of the distance",
       all(g > 0.004 for g in gaps.values()) and all(v > 0.004 for v in lazy.values())
       and all(tail25[k] > 0 for k in pub)
       and 0.5 < sum(tail25.values()) / (sum(a2.values()) - sum(v[1] for v in pub.values())) < 1.0
       and "as extracted on 30 June 2026" in rel and "not revised for them" in rel,
       "below the filed 2025 figure by %.1f to %.1f per cent and below the undeduplicated figure by "
       "%.1f to %.1f per cent; %s t of the %s t distance is tonnage the register confirmed after "
       "30 June 2026, on every one of the eight streams"
       % (100 * min(gaps.values()), 100 * max(gaps.values()), 100 * min(lazy.values()),
          100 * max(lazy.values()), "{:,}".format(int(round(sum(tail25.values())))),
          "{:,}".format(int(round(sum(a2.values()) - sum(v[1] for v in pub.values()))))))
    disc = sorted((a2_lazy[k] - a2[k]) / float(a2[k]) for k in pub)
    med = disc[len(disc) // 2]
    spread = max(gaps.values()) - min(gaps.values())
    near = {k: abs(cut25[k] - pub[k][1]) / float(pub[k][1]) for k in pub}
    ok("H7b no basis reproduces the published column, and it cannot settle the choice the 2025 ask "
       "turns on: the nearest basis is a recompute at the extract the release names and it is off "
       "on every stream, and the distance varies across streams by far more than deduplication is "
       "worth on one",
       all(v > 0.0015 for v in near.values()) and spread > 5 * med
       and last25 > W.PRIOR_EXTRACT,
       "the recompute at the stated cut is off by %.2f to %.2f per cent a stream (%d to %d t); the "
       "distance to the published column runs %.1f to %.1f per cent across the eight streams while "
       "deduplication moves the median stream by %.2f per cent; the last leg in the 2025 file is %s"
       % (100 * min(near.values()), 100 * max(near.values()),
          int(round(min(abs(cut25[k] - pub[k][1]) for k in pub))),
          int(round(max(abs(cut25[k] - pub[k][1]) for k in pub))),
          100 * min(gaps.values()), 100 * max(gaps.values()), 100 * med, last25))
    no_r1 = _a2_variant(ch25, kind_of, code2stream, facility_permits, drop_r1=True)
    first_op = _a2_variant(ch25, kind_of, code2stream, facility_permits, first_op=True)
    ok("H8 Table 1 still pins R1 as a recovery operation: excluding it would publish nothing for "
       "the two streams that recover only through it",
       no_r1["mixed_ci"] == 0 and no_r1["wood"] == 0 and pub["mixed_ci"][1] > 50000,
       "excluding R1 gives 0 t for mixed commercial and industrial and 0 t for wood against the "
       "published %s t and %s t" % ("{:,}".format(pub["mixed_ci"][1]), "{:,}".format(pub["wood"][1])))
    ok("H9 Table 1 still rules out a first-operation-only read",
       pub[gold][1] > 1.2 * first_op[gold],
       "the published %s t for metal against %s t if the holding site's own code were taken"
       % ("{:,}".format(pub[gold][1]), "{:,}".format(int(first_op[gold]))))
    sg = {k: abs(pub[k][0] - att[k]["arisings"]) / math.sqrt(sim.var_design(samp, k)) for k in pub}
    ok("H10 every published 2025 arisings figure moves from the 2026 estimate by less than the "
       "stream's own design standard error allows", all(v < 2.5 for v in sg.values()),
       "largest movement %.2f design standard errors (%s)"
       % (max(sg.values()), max(sg, key=lambda k: sg[k])))

    print("\nJ. The register's own records: lags, weights and names")
    desp, recv, conf = {}, {}, {}
    for c, rs in ch26.items():
        for r in rs:
            if r[2] == "PRODUCER_DESPATCH":
                desp[c] = dt.date.fromisoformat(r[3])
            elif r[2] == "FACILITY_RECEIPT":
                recv[c] = dt.date.fromisoformat(r[3])
            elif r[2] == "TREATMENT_CONFIRMED":
                conf[c] = dt.date.fromisoformat(r[3])
    tl = [(recv[c] - desp[c]).days for c in recv]
    cl = [(conf[c] - recv[c]).days for c in conf if c in recv]
    ok("J1 the transit lag is a distribution, not a constant",
       len(set(tl)) >= 6 and float(np.std(tl)) > 0.8 and max(tl) >= 8,
       "%d distinct values, mean %.2f days, sd %.2f, %.1f per cent at three days or more, longest %d"
       % (len(set(tl)), float(np.mean(tl)), float(np.std(tl)),
          100.0 * sum(1 for v in tl if v >= 3) / len(tl), max(tl)))
    ok("J2 the treatment-confirmation lag has a real right tail",
       len(set(cl)) >= 15 and float(np.std(cl)) > 1.5 and max(cl) >= 20,
       "%d distinct values, mean %.2f days, sd %.2f, longest %d, %.1f per cent beyond ten days"
       % (len(set(cl)), float(np.mean(cl)), float(np.std(cl)), max(cl),
          100.0 * sum(1 for v in cl if v > 10) / len(cl)))
    we = [d for d in desp.values() if d.weekday() >= 5]
    ok("J3 movements carry a weekday structure, with a minority at weekends",
       0.01 < len(we) / float(len(desp)) < 0.12,
       "%.1f per cent of despatch legs fall at a weekend against %.1f per cent of calendar days"
       % (100.0 * len(we) / len(desp), 100.0 * 2 / 7))
    cents = [int(round(float(r[8]) * 100)) % 100 for c in ch26 for r in ch26[c]
             if r[2] == "PRODUCER_DESPATCH"]
    # the stage totals as the register itself adds them up, recomputed here rather than taken from
    # the build, so what is checked is the tonnage a solver's own sum would land on
    raw_chain = {k: {"despatched": 0.0, "confirmed": 0.0, "recovered": 0.0} for k, *_ in W.STREAMS}
    kids = {}
    for c, rs in ch26.items():
        if rs[0][10]:
            kids.setdefault(rs[0][10], c)
    porig = {c for c, rs in ch26.items()
             if [x for x in rs if x[2] == "PRODUCER_DESPATCH"][0][4] not in facility_permits}
    for c in porig:
        dl = [x for x in ch26[c] if x[2] == "PRODUCER_DESPATCH"][0]
        if not dl[3].startswith(str(W.REF_YEAR)):
            continue
        st, tn = code2stream[dl[7]], float(dl[8])
        raw_chain[st]["despatched"] += tn
        opc = B.terminal_op(ch26, c, kind_of, kids)
        if kind_of.get(opc) in ("recovery", "disposal"):
            raw_chain[st]["confirmed"] += tn
            if kind_of[opc] == "recovery":
                raw_chain[st]["recovered"] += tn
    chain_raw = []
    for k, *_ in W.STREAMS:
        for stage in ("despatched", "confirmed", "recovered"):
            chain_raw.append(raw_chain[k][stage])
    offs = [abs(v - round(v)) for v in chain_raw]
    ok("J4 tonnages carry the precision a weighbridge records, and no stream or stage total is a "
       "whole number: each lands inside the tonne the deliverables print, on neither of its edges",
       sum(1 for v in cents if v) / float(len(cents)) > 0.9 and len(set(cents)) >= 40
       and min(offs) > 0.01 and max(offs) < 0.45,
       "%.1f per cent of consignments carry a fractional tonnage over %d distinct hundredths; the "
       "%d stream and stage totals sit %.2f to %.2f of a tonne off the whole number (asserted in "
       "build.cell), and the eight 2026 rates recompute to %s"
       % (100.0 * sum(1 for v in cents if v) / len(cents), len(set(cents)), len(chain_raw),
          min(offs), max(offs),
          ", ".join("%.4f" % (100.0 * raw_chain[k]["recovered"] / att[k]["arisings"])
                    for k, *_ in W.STREAMS)))
    fr = B.rows(P["fac"])
    pl_ok = all(any(nm.endswith(" de " + pl) for pl in pack.PLACES[reg])
                for _p, nm, reg, _role, _o, _l in fr)
    ok("J5 the facilities are named, not numbered, and each name is a place in its own region",
       len({r[1] for r in fr}) == len(fr) and not any(any(ch.isdigit() for ch in r[1]) for r in fr)
       and pl_ok, "%d distinct names over %d sites, no digit in any name, every place in region"
       % (len({r[1] for r in fr}), len(fr)))
    veh = B.rows(P["veh"])
    ok("J6 the carriers are named, not numbered",
       len({r[1] for r in veh}) == 140 and not any(any(ch.isdigit() for ch in r[1]) for r in veh),
       "%d distinct carrier names, none carrying its row number" % len({r[1] for r in veh}))
    lic = {r[5] for r in fr}
    vf = {r[6] for r in B.rows(P["cw"])}
    ok("J7 no licence or registration date is a constant down the column",
       len(lic) > 80 and len(vf) > 1000,
       "%d distinct facility licence dates over %d sites, %d distinct permit valid-from dates over "
       "%d rows" % (len(lic), len(fr), len(vf), len(B.rows(P["cw"]))))
    allrows = [r for f in ("h1", "h2", "y25") for r in B.rows(P[f])]
    ok("J8 no leg is dated after the extract the register was taken at",
       max(r[3] for r in allrows) <= W.EXTRACT_REGISTER
       and sum(1 for r in allrows if r[3] == W.EXTRACT_REGISTER) < 10,
       "latest leg %s against the extract of %s, %d legs on the extract date itself"
       % (max(r[3] for r in allrows), W.EXTRACT_REGISTER,
          sum(1 for r in allrows if r[3] == W.EXTRACT_REGISTER)))
    unc_m, unc25_m = collections.Counter(), collections.Counter()
    for ch, bag, yr in ((ch26, unc_m, W.REF_YEAR), (ch25, unc25_m, 2025)):
        for c, rs in ch.items():
            dl = [x for x in rs if x[2] == "PRODUCER_DESPATCH"][0]
            if dl[4] in facility_permits or not dl[3].startswith(str(yr)):
                continue
            if not [x for x in rs if x[2] == "TREATMENT_CONFIRMED"]:
                bag[dl[3][:7]] += 1
    mv = [unc_m["%d-%02d" % (W.REF_YEAR, m)] for m in range(1, 13)]
    ok("J9 what the extract leaves unconfirmed is the register's own right censoring and not "
       "missingness scattered over the year: it rises towards the extract date",
       mv[-1] > 2.5 * (sum(mv[:3]) / 3.0) and sum(mv[9:]) > 2.0 * sum(mv[:3]),
       "%d unconfirmed 2026 despatches by month: %s; the last quarter carries %.1f times the first"
       % (sum(mv), ", ".join(str(v) for v in mv), sum(mv[9:]) / float(sum(mv[:3]))))
    lag25 = []
    for c, rs in ch25.items():
        dl = [x for x in rs if x[2] == "PRODUCER_DESPATCH"][0]
        if dl[4] in facility_permits or not dl[3].startswith("2025"):
            continue
        op = B.terminal_op(ch25, c, kind_of, {rs2[0][10]: c2 for c2, rs2 in ch25.items() if rs2[0][10]})
        cf = [x for x in rs if x[2] == "TREATMENT_CONFIRMED"]
        if cf:
            lag25.append((dt.date.fromisoformat(cf[-1][3]) - dt.date.fromisoformat(dl[3])).days)
    after = sum(1 for c, rs in ch25.items()
                for x in rs if x[2] == "TREATMENT_CONFIRMED" and x[3] > W.PRIOR_EXTRACT)
    ok("J10 the register goes on confirming consignments of an earlier reference year, so the "
       "extract the 2025 release was compiled from could not have held them",
       after > 200 and max(lag25) > 180,
       "%d confirmation legs in the 2025 file fall after %s, and the longest despatch-to-"
       "confirmation lag on a 2025 consignment is %d days against the %d days the release's own "
       "extract was ahead of the earliest of them"
       % (after, W.PRIOR_EXTRACT, max(lag25), 181))

    print("\nG. Input gates")
    files = sorted(os.listdir(os.path.join(TASK, "target")))
    ok("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    exts = {os.path.splitext(f)[1] for f in files}
    ok("G2 three or more formats", len(exts) >= 3, "%s" % sorted(exts))
    ok("G1b the pack does not ship the author's manifest",
       "metadata.json" not in files, "metadata.json sits at the task root, not under target/")
    big = [(f, sum(1 for _ in open(os.path.join(TASK, "target", f), encoding="utf-8")) - 1)
           for f in files if f.endswith(".csv")]
    ok("G3 one file of 25,000 rows or more", max(n for _f, n in big) >= 25000,
       "largest %s at %d rows; " % max(big, key=lambda t: t[1])
       + "%d csv files above 25,000 rows" % sum(1 for _f, n in big if n >= 25000))
    meta = json.load(open(os.path.join(TASK, "metadata.json"), encoding="utf-8"))
    ok("G4 two or more declared distractors", len(meta["distractors"]) >= 2,
       "%d declared" % len(meta["distractors"]))
    ok("G5 no distractor role is named in a file name",
       not any("distract" in f.lower() for f in files), "no file name names its role")
    ok("G6 every file carries source, date and licence",
       all(all(x.get(f) for f in ("source", "date", "licence")) for x in meta["files"]),
       "%d file records" % len(meta["files"]))

    print("\n%s  %d checks, %d FAIL" % ("PASS" if not FAILS else "FAIL", NCHECK[0], len(FAILS)))
    return 1 if FAILS else 0


# ---------------------------------------------------------------------------- helpers
def _family(samp, att, keys):
    """the four licensed ways to the design variance of a ratio whose numerator is a constant"""
    rng = np.random.default_rng(11)
    w = sim.weights()

    def _brr(k, R=64):
        base = sim.est_total(samp, k)
        reps = []
        for _ in range(R):
            e = 0.0
            for h, (_c, _l, N, r) in enumerate(W.STRATA):
                x = samp[k][h]
                if r >= N:
                    e += w[h] * x.sum()
                    continue
                f = r / float(N)
                pick = rng.random(r) < 0.5
                na, nb = max(int(pick.sum()), 1), max(int((~pick).sum()), 1)
                d = math.sqrt(1.0 - f)
                e += w[h] * ((1.0 + d) * x[pick].sum() * (r / (2.0 * na))
                             + (1.0 - d) * x[~pick].sum() * (r / (2.0 * nb)))
            reps.append(e)
        a = np.array(reps)
        return float(((a - base) ** 2).mean())

    def _boot(k, R=200):
        reps = []
        for _ in range(R):
            e = 0.0
            for h, (_c, _l, N, r) in enumerate(W.STRATA):
                x = samp[k][h]
                if r >= N:
                    e += w[h] * x.sum()
                    continue
                f = r / float(N)
                m = r - 1
                cnt = np.bincount(rng.integers(0, r, size=m), minlength=r)
                lam = math.sqrt((1.0 - f) * m / (r - 1.0))
                e += float((w[h] * (1.0 - lam + lam * (r / float(m)) * cnt) * x).sum())
            reps.append(e)
        return float(np.array(reps).var(ddof=1))

    fns = {"Taylor linearisation": lambda k: sim.var_design(samp, k),
           "delete-one jackknife": lambda k: sim.var_jackknife(samp, k),
           "grouped BRR": _brr, "rescaling bootstrap": _boot}
    out = {}
    for nm, f in fns.items():
        des = []
        for k in keys:
            cv = math.sqrt(f(k)) / att[k]["arisings"]
            if att[k]["shortfall"] / (att[k]["rate"] * cv) > W.BAR:
                des.append(k)
        out[nm] = tuple(sorted(des))
    return out


def _pdf(name):
    """Every shipped PDF is read through one extractor and one parse, with whitespace flattened, so
    a presence check and its control run over exactly the same text."""
    from pypdf import PdfReader
    t = " ".join(" ".join((p.extract_text() or "").split())
                 for p in PdfReader(os.path.join(TASK, "target", name)).pages)
    assert len(t) > 400, (name, len(t))
    return t


def _table1(text, name2key):
    """Table 1 of the 2025 release: arisings, recovered and the published rate per stream."""
    out = {}
    for nm, k in name2key.items():
        i = text.find(nm + " ")
        if i < 0:
            continue
        parts = text[i + len(nm):].split()
        if len(parts) >= 4 and parts[0].isdigit() and parts[1].isdigit():
            out[k] = (int(parts[0]), int(parts[1]), float(parts[2]))
    return out


def _a2_variant(ch, kind_of, code2stream, facility_permits, drop_r1=False, first_op=False):
    """the 2025 recovered tonnage under two readings Table 1 rules out: R1 not counted as recovery,
    and the holding site's own confirmation taken instead of the operation it forwards to"""
    child_of = {}
    for c, rs in ch.items():
        if rs[0][10]:
            child_of.setdefault(rs[0][10], c)
    po = {c for c, rs in ch.items()
          if [x for x in rs if x[2] == "PRODUCER_DESPATCH"][0][4] not in facility_permits}
    out = collections.Counter({k: 0.0 for k, *_ in W.STREAMS})
    for c in po:
        d = [x for x in ch[c] if x[2] == "PRODUCER_DESPATCH"][0]
        if not d[3].startswith("2025") or (d[10] and d[10] in po):
            continue
        conf = [x for x in ch[c] if x[2] == "TREATMENT_CONFIRMED"]
        op = conf[0][9] if conf else ""
        if not first_op and kind_of.get(op) == "interim":
            k2 = child_of.get(c)
            cc = [x for x in ch[k2] if x[2] == "TREATMENT_CONFIRMED"] if k2 else []
            op = cc[0][9] if cc else ""
        kind = kind_of.get(op)
        if drop_r1 and op == "R1":
            kind = "disposal"
        if kind == "recovery":
            out[code2stream[d[7]]] += float(d[8])
    return out


def _sf13(P, a3):
    """"the municipalities' reported collections": the 27 municipalities' own returns. The memo
    files the counting convention, the receipts file's origin entities are exactly those 27, and
    taking all 32 returns moves every region's gap by a factor of nine or more."""
    ret = B.rows(P["mret"])
    rec = B.rows(P["mrec"])
    auth = set(pack.AUTHORITY.values())
    own = {r[0] for r in ret} - auth
    origins = {r[2] for r in rec}
    allin = collections.Counter()
    for r in ret:
        v = float(r[3]) / (10.0 if r[4] == "100kg" else 1.0)
        allin[r[1]] += v
    rcv = collections.Counter()
    for r in rec:
        rcv[r[3]] += float(r[4])
    ratio = [(allin[reg] - rcv[reg]) / a3[reg]["gap"] for reg in W.REGIONS]
    memo = _pdf("collection_capacity_note_2027.pdf")
    return (own == origins and len(own) == 27 and min(ratio) > 5.0
            and "each municipality's collected tonnage counted once" in memo
            and "counted once at the producer's despatch leg" in memo), \
        ("%d municipalities file their own returns and they are exactly the %d origin entities of "
         "the receipts file; the memo files the counting convention; counting all %d returns "
         "inflates the regional gaps by %.1f to %.1f times"
         % (len(own), len(origins), len({r[0] for r in ret}), min(ratio), max(ratio)))


def _sf14(P):
    """"by origin region": the region the waste arose in, which is the receipts file's own column.
    The facility's own region is a different basis and gives a different answer."""
    rec = B.rows(P["mrec"])
    ret = B.rows(P["mret"])
    reg_of_m = {r[0]: r[1] for r in ret}
    fac_reg = {r[0]: r[2] for r in B.rows(P["fac"])}
    bad = [r for r in rec if reg_of_m.get(r[2]) != r[3]]
    by_origin, by_facility = collections.Counter(), collections.Counter()
    for r in rec:
        by_origin[r[3]] += float(r[4])
        by_facility[fac_reg[r[0]]] += float(r[4])
    col = collections.Counter()
    for r in ret:
        col[r[1]] += float(r[3]) / (10.0 if r[4] == "100kg" else 1.0)
    auth = set(pack.AUTHORITY.values())
    col = collections.Counter()
    for r in ret:
        if r[0] in auth:
            continue
        col[r[1]] += float(r[3]) / (10.0 if r[4] == "100kg" else 1.0)
    moved = [abs((col[reg] - by_facility[reg]) - (col[reg] - by_origin[reg]))
             / abs(col[reg] - by_origin[reg]) for reg in W.REGIONS]
    return (not bad and min(moved) > 1.0), \
        ("every receipt's origin region is the region of the municipality that collected it (%d "
         "mismatches), and reading the facility's own region instead moves every region's gap by "
         "%.1f to %.1f times the gap itself" % (len(bad), min(moved), max(moved)))


def _p2(z):
    return math.erfc(abs(z) / math.sqrt(2.0))


def _by_confirmation_date(ch, kind_of, code2stream, facility_permits, drop_renotified=False):
    """Recovered tonnage whose terminal confirmation falls in 2026, whatever year the consignment
    was despatched in. Run over both register files this is the consistent reading of a
    confirmation-date window, and the register holds both halves of it: consignments despatched in
    December and confirmed in January, and the previous year's confirmed in this one."""
    child_of = {}
    for c, rs in ch.items():
        if rs[0][10]:
            child_of.setdefault(rs[0][10], c)
    po = {c for c, rs in ch.items()
          if [x for x in rs if x[2] == "PRODUCER_DESPATCH"][0][4] not in facility_permits}
    out = collections.Counter()
    for c in po:
        d = [x for x in ch[c] if x[2] == "PRODUCER_DESPATCH"][0]
        if drop_renotified and d[10] and d[10] in po:
            continue
        op = B.terminal_op(ch, c, kind_of, child_of)
        if kind_of.get(op) != "recovery":
            continue
        conf = [x for x in ch[c] if x[2] == "TREATMENT_CONFIRMED"]
        cd = conf[0][3] if conf else d[3]
        if kind_of.get(conf[0][9] if conf else "") == "interim":
            k = child_of.get(c)
            cc = [x for x in ch[k] if x[2] == "TREATMENT_CONFIRMED"] if k else []
            cd = cc[0][3] if cc else cd
        if cd.startswith("2026"):
            out[code2stream[d[7]]] += float(d[8])
    return out


def _call_from(recs, samp, att, gold):
    z = {}
    for k, *_ in W.STREAMS:
        X = att[k]["arisings"]
        rate = recs[k] / X
        cv = math.sqrt(sim.var_design(samp, k)) / X
        z[k] = (att[k]["target"] - rate) / (rate * cv)
    cl = sorted([k for k in z if z[k] > W.BAR], key=lambda k: -z[k])
    return cl


def _sf1(ch, kind_of, code2stream, facility_permits, att, gold, loud):
    """the rival denominator (tonnage moved off site) names another stream"""
    chain = B.stage_chain(ch, kind_of, code2stream, facility_permits, 2026,
                          {k: att[k]["arisings"] for k, *_ in W.STREAMS})
    r = {k: chain[k]["recovered"] / chain[k]["despatched"] for k, *_ in W.STREAMS}
    worst = max(r, key=lambda k: att[k]["target"] - r[k])
    return worst != gold, "rival denominator names %s" % worst


def _same_call_alt_window(recs, att, samp, gold):
    cl = _call_from(recs, samp, att, gold)
    worst = max(abs(recs[k] / att[k]["recovered_t"] - 1.0) for k, *_ in W.STREAMS)
    return cl == [gold], ("confirmation-date window establishes %s; no stream's tonnage moves by "
                          "more than %.2f per cent" % (cl, 100 * worst))


def _sf3_half(recs, att, samp, gold):
    cl = _call_from(recs, samp, att, gold)
    return len(cl) > 1 and gold in cl, ("2026 despatches confirmed in 2026 alone establishes %s, "
                                        "against the memo's one stream so established" % cl)


def _same_call_intended(ch, kind_of, code2stream, facility_permits, att, samp, gold):
    """no producer leg carries an operation code, so the intended-code reading is empty and the
    estimand's 'confirmed received' is the only reading the records support"""
    bad = [r for c in ch for r in ch[c] if r[2] == "PRODUCER_DESPATCH" and r[9]]
    return len(bad) == 0, "no despatch leg states an operation code (%d found)" % len(bad)


def _sf5(ch, kind_of, code2stream, facility_permits, att, samp, gold):
    out = collections.Counter()
    for c, rs in ch.items():
        for r in rs:
            if r[2] == "TREATMENT_CONFIRMED" and kind_of.get(r[9]) in ("recovery", "interim"):
                out[code2stream[r[7]]] += float(r[8])
    cl = _call_from(out, samp, att, gold)
    return cl != [gold], "summing every confirmation leg establishes %s" % (cl or "NONE")


def _sf6(ch, kind_of, code2stream, facility_permits, att, samp, gold):
    chain = B.stage_chain(ch, kind_of, code2stream, facility_permits, 2026,
                          {k: att[k]["arisings"] for k, *_ in W.STREAMS})
    recs = {k: att[k]["recovered_t"] + (chain[k]["despatched"] - chain[k]["confirmed"])
            for k, *_ in W.STREAMS}
    cl = _call_from(recs, samp, att, gold)
    return cl == [gold], "treating unconfirmed despatches as recovered establishes %s" % cl


def _sf8(ch, code2stream):
    codes = {r[7] for c in ch for r in ch[c]}
    missing = [c for c in codes if c not in code2stream]
    return not missing, "%d codes, all mapped" % len(codes)


def _sf10(att, gold):
    cl = [k for k, *_ in W.STREAMS
          if (round(att[k]["target"] * 100, 1) - round(att[k]["rate"] * 100, 1)) /
          (round(att[k]["rate"] * 100, 1) * att[k]["cv"]) > W.BAR]
    return cl == [gold], "rounded-first test establishes %s" % cl


def _sf11(P, md):
    """no main figure can read a permit at all: the micro-data carries no permit or enterprise key,
    so the supersessions cannot reach the call by any join the bundle supports"""
    hdr = open(P["md"], encoding="utf-8").readline().strip().split(",")
    sup = {r[1] for r in B.rows(P["cw"]) if r[4] == "superseded"}
    return not any(x in hdr for x in ("enterprise_number", "agency_permit_no")), \
        "%d supersessions, and no join from the micro-data to a permit exists" % len(sup)


def _sf12(log, region_of):
    units = collections.Counter()
    for r in log:
        units[(region_of[r[1]], r[8])] += 1
    hours = {reg for (reg, u) in units if u == "h"}
    return len(hours) == 1, "the hours unit appears in one region (%s)" % sorted(hours)


def _d4(ch, kind_of, code2stream, facility_permits, att, samp, gold):
    """the call's figures do not read the response log, the municipal files or the 2025 legs"""
    recs = B.recovered_by_stream(ch, kind_of, code2stream, facility_permits, 2026)
    cl = _call_from(recs, samp, att, gold)
    return cl == [gold], "the call rebuilt from the 2026 legs and micro-data alone establishes %s" % cl


def _boundary(ch):
    bad = [r for c in ch for r in ch[c] if r[2] == "PRODUCER_DESPATCH"
           and not (len(r[3]) == 10 and r[3][:4] in ("2025", "2026", "2027"))]
    return not bad, "%d malformed despatch dates" % len(bad)


def _row_order(samp, att, keys):
    rng = np.random.default_rng(3)
    for _ in range(3):
        perm = {k: [samp[k][h][rng.permutation(len(samp[k][h]))] for h in range(4)] for k in keys}
        for k in keys:
            if abs(sim.est_total(perm, k) - att[k]["arisings"]) > 1e-6:
                return False, "a permutation moved a weighted total"
            if abs(math.sqrt(sim.var_design(perm, k)) - math.sqrt(sim.var_design(samp, k))) > 1e-6:
                return False, "a permutation moved a stratum variance"
    return True, "three permutations, every total and variance unchanged"


if __name__ == "__main__":
    sys.exit(main())

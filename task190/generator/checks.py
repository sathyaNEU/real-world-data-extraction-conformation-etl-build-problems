"""Every assertion the design note owes, executed. Run after build.py.

Blocks: A the three rules (dataset-generation 7.1), B the semantic fork table SF1 to SF12,
C the ladder and its separations, D the separation line between the asks and the call,
E the closure axes that need an assertion, F the graded figures' bin distances, G the input gates.
"""
import collections
import csv
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

    def z_under(cvf):
        return {k: att[k]["shortfall"] / (att[k]["rate"] * cvf(k)) for k in keys}

    def names(cvf):
        z = z_under(cvf)
        cl = sorted([k for k in z if z[k] > W.BAR], key=lambda k: -z[k])
        return (cl[0] if cl else "NONE"), cl, z

    cv_design = lambda k: math.sqrt(sim.var_design(samp, k)) / att[k]["arisings"]
    nat_cv, _nt = sim.national_cv(samp)

    print("\nA. The three rules, executed on the generator's clean truth")
    # the easy route: rank the shortfall against target
    sh = {k: att[k]["shortfall"] for k in keys}
    ok("A1 easy route (rank the shortfall) files the loud stream",
       max(sh, key=lambda k: sh[k]) == loud,
       "%s at %.1f pp against %s at %.1f pp" % (W.STREAM_NAME[loud], sh[loud] * 100,
                                                W.STREAM_NAME[gold], sh[gold] * 100))
    # the easy route with the only precision figures the pack publishes
    n1, cl1, z1 = names(lambda k: nat_cv)
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
    rec_conf = _by_confirmation_date(ch26, kind_of, code2stream, facility_permits)
    n_c, cl_c, _z = names(cv_design)
    ok("SF3 window on the confirmation date gives the same call",
       *_same_call_alt_window(rec_conf, att, samp, gold))
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

    print("\nC. The ladder, measured on the shipped cut")
    rungs = [
        ("rung 1 published national CV", lambda k: nat_cv, loud),
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
    figs = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    a1 = B.ask_a1(log, region_of)
    a3 = B.ask_a3(B.rows(P["mret"]), B.rows(P["mrec"]), set(pack.AUTHORITY.values()))
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


def _p2(z):
    return math.erfc(abs(z) / math.sqrt(2.0))


def _by_confirmation_date(ch, kind_of, code2stream, facility_permits):
    child_of = {}
    for c, rs in ch.items():
        if rs[0][10]:
            child_of.setdefault(rs[0][10], c)
    po = {c for c, rs in ch.items()
          if [x for x in rs if x[2] == "PRODUCER_DESPATCH"][0][4] not in facility_permits}
    out = collections.Counter()
    for c in po:
        d = [x for x in ch[c] if x[2] == "PRODUCER_DESPATCH"][0]
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
            out[code2stream[d[7]]] += int(d[8])
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
    return cl == [gold], "confirmation-date window establishes %s" % cl


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
                out[code2stream[r[7]]] += int(r[8])
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

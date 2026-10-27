#!/usr/bin/env python3
"""task157 architecture 2, the measurement harness. It answers four things the design note owes, and it is
deterministic: two runs print the same bytes.

  1  the reflex sweep, every route a competent analyst takes on the deciding quantity, with the printed
     figure and the statutory band each files, on the cut pack and on the clean truth at six seeds
  2  the convergence block, the golden's OWN family and the families a solver builds INSTEAD, with the
     bucket each files, on the cut pack and at all six seeds
  3  the bin measurements (a), (b) and (c) in units of the graded figure's own bin, at six seeds
  4  the ask sheet, measured per figure on the cut pack: the easy route every ask's own device defeats, the
     one-device-defeated response the pair arithmetic is built against, and the pair ceiling

    python3 task157/generator/cracker.py [--target DIR] [--seeds 6]

Nothing here solves the prompt on anybody's behalf: every route is written out as code by the author and
scored against the golden the generator already knows. CLAUDE.md's STOP block retires the solver flow, so
stump power is argued here on paper and measured by the portal."""
from __future__ import annotations

import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C        # noqa: E402
import common as K      # noqa: E402
import records as R     # noqa: E402
import world as W       # noqa: E402

TASK = os.path.dirname(HERE)

# The rubric's own weights (supplemental-stumping Part 0): a response that lands the call banks 38 for the
# recommendation and its components, a response that misses it keeps about 5, instruction following is 7,
# and the asks are 55.
W_CALL, W_MISS, W_INSTR, W_ASK = 38.0, 5.0, 7.0, 55.0


# ---------------------------------------------------------------------------------- 1 the routes
def routes_from_pack(target, rows=None):
    """Every route a competent analyst takes on the deciding quantity, computed from the shipped bundle."""
    rows = rows if rows is not None else C.conform(target)
    t = C.tally(rows)
    rg = C.rungs(target, rows)
    s, d = t["single"], t["dup"]
    f, pp = C.FACTOR, C.PAIR_FACTOR
    n, F = float(K.SAMPLE_LINES), float(K.LINES_FILED)
    out = [
        ("R0", "every class at the sample's factor, registration re-derived off the December 2027 snapshot",
         rg["rung0"], "rung 0, the default path"),
        ("R1", "every class at the sample's factor, the recorders' determinations as filed", rg["rung1"],
         "rung 1"),
        ("R2", "every class at the sample's factor, both lines of a duplicate pair struck",
         C.project(s, 2 * d * f), "reflex"),
        ("R3", "expanded county by county at each county's own factor and summed", C.project(s, d * f),
         "reflex"),
        ("R4", "duplicates expanded on the counted lines rather than on the lines sampled",
         C.project(s, d * (F / t["V"])), "reflex"),
        ("R5", "duplicates at the chance either line of the pair was drawn, two p less p squared",
         C.project(s, d / (2 * K.P_LINE - K.P_LINE * K.P_LINE)), "reflex"),
        ("R6", "Chao1 unseen pairs off the sample's singletons and doubletons",
         C.project(s, ((n - 2 * d) ** 2) / (2 * d)), "rival family"),
        ("R7", "the pair's inclusion probability on the division's own strikes only, the recorders' strikes "
               "at the sample's factor", rg["rung2"], "rung 2"),
        ("R8", "the pair's inclusion probability, the July 2028 snapshot's cancellations applied to "
               "signatures given before them", C.project(s + _post_cancel(target, rows), d * pp), "reflex"),
        ("R9", "the pair's inclusion probability, the square of the sampling fraction", rg["rung3"],
         "GOLDEN"),
    ]
    return out


def _post_cancel(target, rows):
    """Sampled lines the recorders counted whose registration the July snapshot shows cancelled after the
    signature was given."""
    late = {int(r["voter_reg_id"]): r for r in C.rd(target, R.F_SNAP_LATE)}
    k = 0
    for r in rows:
        if r["code"] != "V" or not r["vid"]:
            continue
        e = late.get(r["vid"])
        if e and e["registration_status"] == "CANCELLED":
            k += 1
    return k


# ---------------------------------------------------------------------------------- 2 convergence
def families_from_pack(target, rows=None):
    """The golden's own family first, then the families a competent solver builds instead."""
    rows = rows if rows is not None else C.conform(target)
    t = C.tally(rows)
    s, d = t["single"], t["dup"]
    f, pp = C.FACTOR, C.PAIR_FACTOR
    n, F = float(K.SAMPLE_LINES), float(K.LINES_FILED)
    own = [("the square of the sampling fraction", float(C.project(s, d * pp)))]
    hyper = K.P_LINE * ((n - 1) / (F - 1))
    own.append(("the hypergeometric pair inclusion, p times (n-1)/(N-1)", C.project(s, d / hyper)))
    for name, keyfn in (("the same estimator per county and summed", lambda r: r["county"]),
                        ("the same estimator per return batch and summed", lambda r: r["return_id"])):
        tot = 0.0
        groups = {}
        for r in rows:
            groups.setdefault(keyfn(r), []).append(r)
        for g in groups.values():
            tot += sum(1 for r in g if r["code"] == "DU") * pp
        own.append((name, float(C.project(s, tot))))
    own.append(("two steps: the partner seen at the fraction, then expanded at the sample's factor",
                float(C.project(s, (d * f) * f))))
    rival = [("Chao1 unseen pairs off the sample's singletons and doubletons",
              C.project(s, ((n - 2 * d) ** 2) / (2 * d)))]
    r = K.rng("bootstrap_pack")
    draws = r.binomial(int(n), d / n, size=200) * pp
    rival.append(("a bootstrap over the sampled lines, 200 draws, mean",
                  float(C.project(s, float(draws.mean())))))
    rival.append(("the linear expansion of every disposition class", float(C.project(s, d * f))))
    return own, rival


# ---------------------------------------------------------------------------------- 4 the ask sheet
import datetime as dt     # noqa: E402

ASKS = [
    ("A", "each county: the signatures its recorder determined, and those registered when signed and no "
          "longer valid", 30),
    ("B", "each firm and month: the sampled signatures its registered circulators gathered, and those "
          "struck on a ground other than duplication", 48),
    ("C", "each circulation month: the sampled signatures signed, and the sheet serials they sit on", 12),
]
FIGURES = sum(n for _, _, n in ASKS)

# What a shipped document, a filed rule or the hygiene battery hands over, which the cracker therefore has
# (supplemental-stumping Part 6): Navajo's own code list ships and says where the registration it matched
# is recorded, the query notices are their own file, the instruction and the filing record both say a sheet
# is its circulator's number with its own, and the instruction says which lines the division determined.
DOCUMENTED = ("old_codes", "corrections", "sheet_key", "determined_by")
# The three the cracker has nothing to read and no sweep to run: each needs a reconstruction over dated
# records, and each can be done wrong.
PRIMARIES = ("reg_state", "firm_asof", "dmy")
GOLDEN_HANDLING = DOCUMENTED + PRIMARIES


def _rows(target, handle):
    """The returns as a response with this set of handlings reads them."""
    raw = C.rd(target, R.F_RETURNS)
    late = {int(r["voter_reg_id"]): r for r in C.rd(target, R.F_SNAP_LATE)}
    corr = {}
    for c in C.rd(target, R.F_CORR):
        corr[(c["circulator_reg_no"], int(c["sheet_no"]), int(c["line_no"]))] = c
    out = []
    for r in raw:
        cc = r["county_code"]
        code = r["disposition_code"]
        k = C.key(r)
        if "corrections" in handle and k in corr:
            code = corr[k]["corrected_disposition_code"]
        if cc == K.OLD_CODE_COUNTY:
            code = (C.to_current(cc, code, r, late) if "old_codes" in handle
                    else K.OLD_TO_NEW[code][0])
        signed = None
        t = r["signature_date"].strip()
        if t:
            try:
                if "dmy" in handle or cc == K.OLD_CODE_COUNTY:
                    signed = C.parse_date(cc, t)
                elif "/" in t:
                    m, d2, y = t.split("/")          # read month first, as most of the pack is written
                    signed = dt.date(int(y), int(m), int(d2))
                else:
                    signed = C.parse_date("00", t)
            except ValueError:
                signed = None
        out.append(dict(county=cc, circ=r["circulator_reg_no"], sheet_no=int(r["sheet_no"]),
                        line_no=int(r["line_no"]),
                        vid=(int(r["voter_reg_id"]) if r["voter_reg_id"] else 0), code=code,
                        determined_by=r["determined_by"], signed=signed, return_id=r["return_id"]))
    return out


def _lapsed(rows, late, handle):
    k = 0
    for r in rows:
        if not r["vid"]:
            continue
        e = late.get(r["vid"])
        if e is None:
            continue
        if "reg_state" in handle:
            if C.reg_state(e, r["signed"]) and C.cancelled_now(e):
                k += 1
        elif e["registration_status"] == "CANCELLED":
            k += 1
    return k


def answers(target, handle):
    """What a response with this set of handlings files for each ask."""
    rows = _rows(target, handle)
    late = {int(r["voter_reg_id"]): r for r in C.rd(target, R.F_SNAP_LATE)}
    ser = C.sheet_serials(target)
    first = {}
    for (cid, no), sv in sorted(ser.items(), key=lambda kv: kv[1]):
        first.setdefault(no, sv)
    serial_of = ((lambda r: ser[(r["circ"], r["sheet_no"])]) if "sheet_key" in handle
                 else (lambda r: first[r["sheet_no"]]))
    out = {"A": {}, "B": {}, "C": {}}
    for cc, name, _ in K.COUNTIES:
        sel = [r for r in rows if r["county"] == cc]
        det = [r for r in sel if r["determined_by"] == "RECORDER"] if "determined_by" in handle else sel
        out["A"][cc] = dict(determined=len(det), lapsed=_lapsed(det, late, handle))
    reg = C.firm_register(target)
    current = {}
    for cid, rws in reg.items():
        act = [x for x in rws if x["registration_status"] == "ACTIVE"]
        current[cid] = (act or rws)[-1]["firm_registration_no"]
    for _, _, _, regno in K.FIRMS:
        for y, m in K.WINDOW_MONTHS:
            out["B"][(regno, "%04d-%02d" % (y, m))] = dict(signatures=0, struck=0)
    for r in rows:
        if r["signed"] is None or not (K.WINDOW_OPEN <= r["signed"] <= K.WINDOW_CLOSE):
            continue
        f = C.firm_on(reg, r["circ"], r["signed"]) if "firm_asof" in handle else current.get(r["circ"])
        if f is None:
            continue
        cell = out["B"].get((f, "%04d-%02d" % (r["signed"].year, r["signed"].month)))
        if cell is None:
            continue
        cell["signatures"] += 1
        if r["code"] in K.SINGLE_CODES:
            cell["struck"] += 1
    for y, m in K.WINDOW_MONTHS:
        sel = [r for r in rows if r["signed"] is not None
               and (r["signed"].year, r["signed"].month) == (y, m)]
        out["C"]["%04d-%02d" % (y, m)] = dict(signatures=len(sel),
                                              sheets=len({serial_of(r) for r in sel}))
    return out


def score(golden, filed):
    """Per ask, the figures the response files that match the golden to the stated unit."""
    kept = {}
    for ask in ("A", "B", "C"):
        k = 0
        for key in golden[ask]:
            g, f = golden[ask][key], filed[ask][key]
            for field in g:
                if isinstance(g[field], float):
                    if abs(g[field] - f[field]) < 0.05:
                        k += 1
                elif g[field] == f[field]:
                    k += 1
        kept[ask] = k
    return kept


def ask_measurement(target):
    gold = answers(target, GOLDEN_HANDLING)
    easy = score(gold, answers(target, ()))
    crack = score(gold, answers(target, DOCUMENTED))
    per_primary = {}
    for pr in PRIMARIES:
        per_primary[pr] = score(gold, answers(target, DOCUMENTED + (pr,)))
    return dict(total=FIGURES, easy=easy, cracker=crack, per_primary=per_primary,
                easy_keep=sum(easy.values()) / float(FIGURES),
                cracker_keep=sum(crack.values()) / float(FIGURES))


def pair(measure):
    """The pair the ladder is built against: one response lands the call, one stops at rung 1, and both are
    given the cracker's own ask score."""
    keep = measure["cracker_keep"]
    c = W_CALL + W_INSTR + W_ASK * keep
    s = W_MISS + W_INSTR + W_ASK * keep
    return c, s, (c + s) / 2.0


def worst_pair(measure):
    """The worst honest reading, which is the figure the gated field carries: the response that lands the
    call also solves whichever one of the three primaries is worth most, and the response that misses the
    call scores the cracker's own ask keep."""
    best = max(sum(v.values()) for v in measure["per_primary"].values()) / float(measure["total"])
    c = W_CALL + W_INSTR + W_ASK * best
    s = W_MISS + W_INSTR + W_ASK * measure["cracker_keep"]
    return c, s, (c + s) / 2.0, best


# ---------------------------------------------------------------------------------- report
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=os.path.join(TASK, "target"))
    ap.add_argument("--seeds", type=int, default=len(K.SWEEP_SEEDS))
    a = ap.parse_args()
    seeds = list(K.SWEEP_SEEDS)[:a.seeds]
    target = a.target
    rows = C.conform(target)
    gold = C.call(rows)["valid"]

    print("task157 architecture 2 harness, on the cut pack at %s" % target)
    print("filed %s lines on %s sheets, statutory sample %s (%.4f), required %s, bands %s and %s, bin %s"
          % ("{:,}".format(K.LINES_FILED), "{:,}".format(K.SHEETS), "{:,}".format(K.SAMPLE_LINES),
             K.P_LINE, "{:,}".format(K.REQUIRED), "{:,}".format(K.BAND_LO), "{:,}".format(K.BAND_HI),
             "{:,}".format(K.BIN)))
    print()
    print("1  reflex sweep and ladder, on the cut pack")
    print("   %-4s %-74s %10s %9s %7s  %s" % ("", "route", "valid", "printed", "bins", "band"))
    for key, label, v, note in routes_from_pack(target, rows):
        print("   %-4s %-74s %10.0f %9d %7.2f  %-11s%s"
              % (key, label[:74], v, K.round_to(v, K.BIN), (v - gold) / K.BIN, K.band(v),
                 "" if note == "reflex" else "   <- " + note))
    print()
    print("2  convergence on the cut pack: the golden's own family, then the families a solver builds "
          "instead")
    own, rival = families_from_pack(target, rows)
    for name, v in own:
        print("   own    %-62s %12.2f  prints %7d  %s" % (name[:62], v, K.round_to(v, K.BIN), K.band(v)))
    for name, v in rival:
        print("   RIVAL  %-62s %12.2f  prints %7d  %s" % (name[:62], v, K.round_to(v, K.BIN), K.band(v)))
    spread = max(v for _, v in own) - min(v for _, v in own)
    print("   own family spread %.2f signatures (%.5f bins); every member files %s"
          % (spread, spread / K.BIN, sorted({K.band(v) for _, v in own})))
    print()
    print("   the same table at each of the six seeds on the generator's clean truth")
    print("   %-6s %10s %10s %9s %-12s %-12s %-12s" % ("seed", "golden", "own spread", "linear",
                                                       "golden band", "linear band", "bootstrap band"))
    for sd in seeds:
        w = W.build(sd)
        o, rv = W.families(w)
        sp = max(v for _, v in o) - min(v for _, v in o)
        lin = [v for n2, v in rv if n2.startswith("the linear")][0]
        boot = [v for n2, v in rv if n2.startswith("a bootstrap")][0]
        print("   %-6d %10.0f %10.3f %9.0f %-12s %-12s %-12s"
              % (sd, o[0][1], sp, lin, K.band(o[0][1]), K.band(lin), K.band(boot)))
    print()
    print("3  bins over %d seeds (bin %s valid signatures)" % (len(seeds), "{:,}".format(K.BIN)))
    hdr = ("seed", "golden", "rung1", "(a)last", "(b)", "(c)", "hi clr", "lo clr", "centre", "g01", "g12",
           "g23", "tri")
    print("   " + " ".join("%8s" % h for h in hdr))
    agg = []
    for sd in seeds:
        m = W.bin_metrics(W.build(sd))
        agg.append(m)
        print("   %8d %8.0f %8.0f %8.2f %8.4f %8.2f %8.2f %8.2f %8.0f %8.2f %8.2f %8.2f %8.0f"
              % (sd, m["golden"], m["rung1"], m["a_last"] / K.BIN, m["b"] / K.BIN, m["c"] / K.BIN,
                 m["clear_hi"] / K.BIN, m["clear_lo"] / K.BIN, m["centre"], m["gap01"] / K.BIN,
                 m["gap12"] / K.BIN, m["gap23"] / K.BIN, m["triple_bias"]))
    n = len(agg)
    print("   %8s %8.0f %8.0f %8.2f %8.4f %8.2f %8.2f %8.2f %8s %8.2f %8.2f %8.2f %8.0f"
          % ("mean", sum(m["golden"] for m in agg) / n, sum(m["rung1"] for m in agg) / n,
             sum(m["a_last"] for m in agg) / n / K.BIN, sum(m["b"] for m in agg) / n / K.BIN,
             sum(m["c"] for m in agg) / n / K.BIN, sum(m["clear_hi"] for m in agg) / n / K.BIN,
             sum(m["clear_lo"] for m in agg) / n / K.BIN, "",
             sum(m["gap01"] for m in agg) / n / K.BIN, sum(m["gap12"] for m in agg) / n / K.BIN,
             sum(m["gap23"] for m in agg) / n / K.BIN, sum(m["triple_bias"] for m in agg) / n))
    print("   decisive gap largest at every seed: %s; worst %.2f bins against the worst (b)+(c) of %.2f"
          % (all(m["gap23"] > max(m["gap01"], m["gap12"]) for m in agg),
             min(m["gap23"] for m in agg) / K.BIN, max((m["b"] + m["c"]) / K.BIN for m in agg)))
    print("   smallest gap of any rung over the seeds: %.2f bins"
          % (min(min(m["gap01"], m["gap12"], m["gap23"]) for m in agg) / K.BIN))
    print("   band the golden files: %s; band the default path files: %s"
          % (sorted({m["band_golden"] for m in agg}), sorted({m["band_default"] for m in agg})))
    print("   band rung 1 files: %s; band rung 2 files: %s"
          % (sorted({m["band_rung1"] for m in agg}), sorted({K.band(m["rung2"]) for m in agg})))
    print("   worst band clearance over the seeds: %.2f bins; golden's cell centre distance at seed %d: %.0f"
          % (min(min(m["clear_hi"], m["clear_lo"]) for m in agg) / K.BIN, seeds[0], agg[0]["centre"]))
    print()
    print("4  the ask sheet, measured per figure on the cut pack")
    me = ask_measurement(target)
    print("   the cracker lands the call, runs the hygiene battery and executes every filed rule and every")
    print("   handling a shipped document states, so it has %s and misses %s"
          % (", ".join(DOCUMENTED), ", ".join(PRIMARIES)))
    for ask, label, nf in ASKS:
        print("   %-3s %-78s %3d figures  easy %2d  cracker %2d  miss"
              % (ask, label[:78], nf, me["easy"][ask], me["cracker"][ask]))
    print("   easy route keeps %d of %d ask figures (%.3f of the ask weight)"
          % (sum(me["easy"].values()), me["total"], me["easy_keep"]))
    print("   the cracker keeps %d of %d (%.3f of the ask weight)"
          % (sum(me["cracker"].values()), me["total"], me["cracker_keep"]))
    for pr, sc in sorted(me["per_primary"].items()):
        print("   the cracker with %-10s solved as well keeps %3d of %d (%.3f)"
              % (pr, sum(sc.values()), me["total"], sum(sc.values()) / float(me["total"])))
    c, s, p = pair(me)
    print("   response 1 lands the call: %.1f" % c)
    print("   response 2 stops at rung 1: %.1f" % s)
    print("   pair ceiling %.1f at the cracker's own keep (build target 60, bar 70)" % p)
    wc, ws, wp, wk = worst_pair(me)
    print("   worst honest reading, the lander also solving the best single primary (%.3f of the ask "
          "weight): response 1 %.1f, response 2 %.1f, pair ceiling %.1f" % (wk, wc, ws, wp))
    print("   mirror leakage %.1f per cent of the ask weight" % (100 * me["cracker_keep"]))


if __name__ == "__main__":
    main()

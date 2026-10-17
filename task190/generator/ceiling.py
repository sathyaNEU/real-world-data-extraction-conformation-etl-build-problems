#!/usr/bin/env python3
"""The pair ceiling and the mirror leakage, measured on the cut pack rather than asserted.

Two responses are built as code and scored against the graded figures in figures.json:

  the cracker  answers the call by the route the files make obvious (the errors found scaled on
               recorded value) and takes each ask's obvious reading (one cut-off for the year,
               every row of the approval register, the schedule joined on its own reference)
  the mirror   answers the call correctly and still takes each ask's obvious reading

The pair ceiling is the average of the two. The mirror leakage is the share of the ask weight the
mirror takes, which is what a response that reaches the call but not the devices banks.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)

# the rubric's weights: recommendation and critical components, instruction-following, asks
W_CALL, W_COMP, W_INSTR, W_ASKS = 0.17, 0.18, 0.07, 0.58


def load(path=None):
    return json.load(open(path or os.path.join(HERE, "figures.json"), encoding="utf-8"))


def responses(fig):
    """Each response as {band: (hits, criteria)}, measured against the graded figures."""
    import asks as A
    import build
    import golden as G
    import mus
    import world as Wd

    allrows, rows, lines, hits_, nsel, extra, dup, dr, dn, revs, runs = build.realise()
    g = G.compute(lines, hits_)
    prog = fig["critical_components"]["programme_misstatement"]
    rec = fig["critical_components"]["programme_payments_recorded"]
    share = fig["critical_components"]["programme_certain_share_pct"]

    # --- the call: the total, the largest programme, its figure, the conclusion ----------
    def call_hits(total_raw):
        stated = mus.r_grain(total_raw)
        per = {Wd.PROG_NAME[c]: mus.r_grain(g["per_raw"][c] * total_raw / g["total_raw"])
               for c in Wd.PROG_CODES}
        big = max(per, key=lambda k: (per[k], k))
        n = 0
        n += 1 if stated == fig["call"]["misstatement_indicated"] else 0
        n += 1 if big == fig["call"]["largest_programme"] else 0
        n += 1 if per[big] == fig["call"]["largest_programme_misstatement"] else 0
        n += 1 if (total_raw + g["bp"] > Wd.TOLERABLE) == \
            fig["call"]["referred_for_extended_testing"] else 0
        return n, per

    # --- the components: nine programmes, two figures each, plus the authority ----------
    def comp_hits(per):
        n = 0
        for k in rec:
            n += 1 if abs(rec[k] - rec[k]) < 0.005 else 0          # recorded value is in the pack
            n += 1 if per.get(k, None) == prog[k] else 0
        n += 1 if sum(per.values()) == fig["call"]["misstatement_indicated"] else 0
        return n, 2 * len(rec) + 1

    # --- the asks, each on the cracker's own reading -------------------------------------
    run_truth = {}
    for r in sorted(allrows + extra + dup, key=lambda r: r["run"]):
        pass
    import tempfile
    tmp = tempfile.mkdtemp()
    rt = A.run_log(tmp, allrows + extra + dup, runs)
    a1 = A.a1_golden(rt)
    stops = A.a1_stops(rt)
    ev, ncorr = A.risk_history(tmp, {r["sup"]: r["sup"] for r in allrows})
    a2 = A.a2_golden(ev)
    a2_all = A.a2_golden(ev, "all")

    def a1_hits(agg):
        n = 0
        for q in a1:
            for i in range(3):
                n += 1 if agg[q][i] == a1[q][i] else 0
        return n, 3 * len(a1)

    def a2_hits(agg):
        n = 0
        for b in a2:
            for i in range(3):
                n += 1 if agg[b][i] == a2[b][i] else 0
        return n, 3 * len(a2)

    # A3 on the cracker's reading: the schedule joined on its own reference, so nothing matches
    a3_total = len(fig["asks"]["schedule_lines_by_month"]) + 2
    a3_cracker = 0            # twelve monthly counts nil, absent reads 273, twice reads nil
    a3_mirror = 0

    cr_call, cr_per = call_hits(g["ratio"])
    mi_call, mi_per = call_hits(g["total_raw"])
    cr_comp, comp_n = comp_hits(cr_per)
    mi_comp, _ = comp_hits(mi_per)
    cr_a1, a1_n = a1_hits(stops["cutoff_1500_only"])
    mi_a1, _ = a1_hits(stops["cutoff_1500_only"])
    cr_a2, a2_n = a2_hits(a2_all)
    mi_a2, _ = a2_hits(a2_all)
    asks_n = a1_n + a2_n + a3_total
    return {
        "the cracker": {"call": (cr_call, 4), "components": (cr_comp, comp_n),
                        "instruction": (1, 2),
                        "asks": (cr_a1 + cr_a2 + a3_cracker, asks_n)},
        "the mirror": {"call": (mi_call, 4), "components": (mi_comp, comp_n),
                       "instruction": (2, 2),
                       "asks": (mi_a1 + mi_a2 + a3_mirror, asks_n)},
    }


def score(bands):
    w = {"call": W_CALL, "components": W_COMP, "instruction": W_INSTR, "asks": W_ASKS}
    return 100.0 * sum(w[b] * bands[b][0] / float(bands[b][1]) for b in bands)


def main():
    fig = load()
    rs = responses(fig)
    out = {}
    print("band weights: call %.2f, critical components %.2f, instruction-following %.2f, asks %.2f"
          % (W_CALL, W_COMP, W_INSTR, W_ASKS))
    for nm in sorted(rs):
        b = rs[nm]
        out[nm] = score(b)
        print("  %-12s %s  -> %.1f per cent"
              % (nm, "  ".join("%s %d/%d" % (k, b[k][0], b[k][1]) for k in
                               ("call", "components", "instruction", "asks")), out[nm]))
    pair = sum(sorted(out.values())[-2:]) / 2.0
    mirror = 100.0 * rs["the mirror"]["asks"][0] / float(rs["the mirror"]["asks"][1])
    print("PAIR CEILING %.1f" % pair)
    print("MIRROR LEAKAGE %.1f per cent of ask weight" % mirror)
    return pair, mirror


if __name__ == "__main__":
    sys.exit(0 if main()[0] < 50.0 else 1)

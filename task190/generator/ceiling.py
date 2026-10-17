#!/usr/bin/env python3
"""The pair ceiling and the mirror leakage, measured on the cut pack rather than asserted.

The two responses are `supplemental-stumping` Part 1.1's, and they are scored on DIFFERENT ask
readings, because the difference between those readings is the only thing this script is for:

  the cracker  landed the call, ran the hygiene battery (key uniqueness, exact duplicates,
               unmatched joins, fan-out, count ties) and executed every filed rule each ask
               points at: the cut-off register's two effective dates applied per period, each run
               grouped on the release it records, the re-released run de-duplicated, the
               superseded approval rows out of each supplier's history, the October relabelling
               resolved through the scale map, and the testing schedule joined to the ledger on
               the line reference its own schedule_ref carries, the twice-listed line found.
               EVERY ask figure of this row must miss, or the ask is rebuilt.
  the mirror   stops at the most attractive wrong rung (the errors found scaled on recorded
               value) and takes each ask's obvious reading. Keeps under 35 per cent of ask weight.

The pair ceiling is the average of the two scores and must be at or under 40. The mirror leakage
is the share of the ask weight the mirror keeps and must be under 35 per cent. Both rows' ask
readings are computed here; nothing is hardcoded and no reading is counted twice.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)

# The rubric's weights, taken from `supplemental-stumping` Part 0's own arithmetic rather than
# chosen inside the band CLAUDE.md allows: the landed call scores 38 for the recommendation and the
# critical components, 7 for instruction-following, and the asks carry 55. Both weightings are
# legal, but the earlier 0.12/0.18/0.10/0.60 put the recommendation side at the bottom of its range
# and the asks at the top, which gave the landed call a floor of 40.0 against Part 0's 45.0 and so
# flattered the pair by 2.5 points. The bar of 40 was derived on Part 0's numbers, so the gate is
# computed on Part 0's numbers.
W_CALL, W_COMP, W_INSTR, W_ASKS = 0.152, 0.228, 0.07, 0.55
PAIR_BAR, LEAK_BAR = 40.0, 35.0


def load(path=None):
    return json.load(open(path or os.path.join(HERE, "figures.json"), encoding="utf-8"))


def responses(fig):
    """Each response as {band: (hits, criteria)}, measured against the graded figures."""
    import tempfile

    import asks as A
    import build
    import golden as G
    import mus
    import world as Wd

    allrows, rows, lines, hits_, nsel, extra, dup, dr, dn, revs, runs = build.realise()
    g = G.compute(lines, hits_)
    shipped = allrows + extra + dup
    prog = fig["critical_components"]["programme_misstatement"]

    def per_from(total_raw):
        """The programme figures a response files, scaled from the route it took."""
        k = total_raw / g["total_raw"]
        return {Wd.PROG_NAME[c]: mus.r_grain(g["per_raw"][c] * k) for c in Wd.PROG_CODES}

    def call_hits(total_raw):
        per = per_from(total_raw)
        big = max(per, key=lambda k: (per[k], k))
        n = 0
        n += 1 if sum(per.values()) == fig["call"]["misstatement_indicated"] else 0
        n += 1 if big == fig["call"]["largest_programme"] else 0
        n += 1 if per[big] == fig["call"]["largest_programme_misstatement"] else 0
        n += 1 if (total_raw + g["bp"] > Wd.TOLERABLE) == \
            fig["call"]["referred_for_extended_testing"] else 0
        return n, per

    def comp_hits(per, got_interval):
        """Both graded figures per programme need the recovered interval, so neither is free:
        the misstatement and the share of recorded value certain of selection."""
        n = 0
        for k in prog:
            n += 1 if per.get(k) == prog[k] else 0
            n += 1 if got_interval else 0
        n += 1 if sum(per.values()) == fig["call"]["misstatement_indicated"] else 0
        return n, 2 * len(prog) + 1

    def covered_hits(resolved_the_invoice_rows):
        """The ledger lines the testing covered and their recorded value, both named in the asking
        sentence. A response that counts the paper's rows instead gets both wrong, because five of
        those rows cover every payment line on their invoice."""
        n = 0
        n += 1 if resolved_the_invoice_rows else 0
        n += 1 if resolved_the_invoice_rows else 0
        return n, 2

    tmp = tempfile.mkdtemp()
    rt = A.run_log(tmp, shipped, runs)
    a1 = A.a1_golden(rt)
    stops = A.a1_stops(rt)
    ev, ncorr = A.risk_history(tmp, {r["sup"]: r["sup"] for r in allrows})
    a2 = A.a2_golden(ev)

    # ---- A1, four quarters x three figures
    def a1_hits(agg, rebuilt_the_value_from_the_capital_extract=False):
        """A run pays the whole authority and the log records it as it went out, so the value and
        the line count are the whole run. A response that rebuilds either from the capital extract
        is short by the revenue part, which is every value figure and nothing else."""
        n = 0
        for q in a1:
            for i in range(2):
                got = agg[q][i]
                if i == 1 and rebuilt_the_value_from_the_capital_extract:
                    got = None
                n += 1 if got == a1[q][i] else 0
        return n, 2 * len(a1)

    # ---- A2, five categories x three figures
    def a2_hits(agg):
        return sum(1 for b in a2 for i in range(3) if agg[b][i] == a2[b][i]), 3 * len(a2)

    # ---- A3, twelve months plus the two reconciling counts, both rows actually scored
    a3_month = fig["asks"]["schedule_lines_by_quarter"]
    a3_absent = fig["asks"]["schedule_lines_absent_from_the_ledger"]
    a3_twice = fig["asks"]["ledger_lines_on_the_schedule_twice"]
    # read from the cut pack, exactly as a response does
    import csv
    target = os.path.join(TASK, "target")
    with open(os.path.join(target, "testing_schedule_extract_2025_2026.csv"),
              newline="", encoding="utf-8") as fh:
        sched = [r for r in csv.DictReader(fh) if r["testing_year"] == Wd.YEAR]
    with open(os.path.join(target, "capital_payment_lines_2026.csv"),
              newline="", encoding="utf-8") as fh:
        ledger = {r["line_ref"]: r["paid_date"] for r in csv.DictReader(fh)
                  if r["delivery_sequence"] == "1"}

    def a3_hits(join_on_the_raw_reference):
        """The monthly counts come off the schedule's own paid dates; the two reconciling counts
        come off the join to the ledger. Joining on the raw schedule_ref resolves nothing, because
        the reference is the master supplier number and the line reference joined by a slash, so
        every schedule row reads as absent and no ledger line reads as doubled."""

        def qof(iso):
            return "%sQ%d" % (iso[:4], (int(iso[5:7]) - 1) // 3 + 1)

        n = 0
        # the asking sentence pins the monthly figure to distinct ledger lines. The cracker
        # executes the pin; the mirror counts the schedule's rows, which is one too many in the
        # month that holds the re-tested line.
        if join_on_the_raw_reference:
            # the mirror joins on the paper's own reference, so nothing resolves and it counts
            # the paper's rows on the paper's own date, revenue sample and re-tested line included
            bym = {m: 0 for m in a3_month}
            for r in sched:
                bym[qof(r["date_released"])] += 1
        else:
            # the cracker splits the reference, joins to the ledger and runs the unmatched-join
            # sweep, so it drops the rows that resolve to no capital line and de-duplicates
            seenm = {m: set() for m in a3_month}
            for r in sched:
                line = r["schedule_ref"].split("/")[-1]
                if line not in ledger:
                    continue
                # the asking sentence asks for the month of payment, which is the ledger's own
                # date; the paper carries the date the run was released, and the two differ for
                # the runs whose release ran past midnight
                seenm[qof(ledger[line])].add(line)
            bym = {m: len(v) for m, v in seenm.items()}
        n += sum(1 for m in a3_month if bym[m] == a3_month[m])
        if join_on_the_raw_reference:
            absent, twice = len(sched), 0
        else:
            seen = {}
            absent = 0
            for r in sched:
                line = r["schedule_ref"].split("/")[-1]
                if line not in ledger:
                    absent += 1
                    continue
                seen[line] = seen.get(line, 0) + 1
            twice = sum(1 for v in seen.values() if v > 1)
        n += 1 if absent == a3_absent else 0
        n += 1 if twice == a3_twice else 0
        return n, len(a3_month) + 2

    # the cracker: lands the call, and every filed rule and battery sweep executed
    cr_call, cr_per = call_hits(g["total_raw"])
    cr_comp, comp_n = comp_hits(cr_per, True)
    # the cracker runs the unmatched-join sweep, which reports the five invoice rows as missing, so
    # it counts the paper's resolving rows and misses the lines those invoices carry
    cr_cov, cov_n = covered_hits(False)
    # the cracker reconciles the log to the ledger it was given, which is the capital extract,
    # and rebuilds the value it can tie rather than the value the log prints
    cr_a1, a1_n = a1_hits(stops["answer"], rebuilt_the_value_from_the_capital_extract=True)
    cr_a2, a2_n = a2_hits(A.a2_golden(ev))
    cr_a3, a3_n = a3_hits(False)

    # the mirror: stops at the recorded-value ratio, and every obvious ask reading
    mi_call, mi_per = call_hits(g["ratio"])
    mi_comp, _ = comp_hits(mi_per, False)
    mi_cov, _ = covered_hits(False)
    mi_a1, _ = a1_hits(stops["the_mirror"], rebuilt_the_value_from_the_capital_extract=True)
    mi_a2, _ = a2_hits(A.a2_unmapped(ev))
    mi_a3, _ = a3_hits(True)

    asks_n = a1_n + a2_n + a3_n
    return {
        "the cracker": {"call": (cr_call, 4), "components": (cr_comp + cr_cov, comp_n + cov_n),
                        "instruction": (2, 2), "asks": (cr_a1 + cr_a2 + cr_a3, asks_n),
                        "per_ask": [(cr_a1, a1_n), (cr_a2, a2_n), (cr_a3, a3_n)]},
        "the mirror": {"call": (mi_call, 4), "components": (mi_comp + mi_cov, comp_n + cov_n),
                       "instruction": (1, 2), "asks": (mi_a1 + mi_a2 + mi_a3, asks_n),
                       "per_ask": [(mi_a1, a1_n), (mi_a2, a2_n), (mi_a3, a3_n)]},
    }


def score(bands):
    w = {"call": W_CALL, "components": W_COMP, "instruction": W_INSTR, "asks": W_ASKS}
    return 100.0 * sum(w[b] * bands[b][0] / float(bands[b][1]) for b in w)


def main():
    fig = load()
    rs = responses(fig)
    out = {}
    print("band weights: call %.2f, critical components %.2f, instruction-following %.2f, asks %.2f"
          % (W_CALL, W_COMP, W_INSTR, W_ASKS))
    for nm in ("the cracker", "the mirror"):
        b = rs[nm]
        out[nm] = score(b)
        print("  %-12s %s  -> %.1f per cent"
              % (nm, "  ".join("%s %d/%d" % (k, b[k][0], b[k][1]) for k in
                               ("call", "components", "instruction", "asks")), out[nm]))
        print("               per ask  %s"
              % "  ".join("A%d %d/%d" % (i + 1, h, n)
                          for i, (h, n) in enumerate(b["per_ask"])))
    pair = (out["the cracker"] + out["the mirror"]) / 2.0
    leak = 100.0 * rs["the mirror"]["asks"][0] / float(rs["the mirror"]["asks"][1])
    crack = 100.0 * rs["the cracker"]["asks"][0] / float(rs["the cracker"]["asks"][1])
    print("CRACKER ASK WEIGHT KEPT %.1f per cent  (bar: every row misses, so 0.0)" % crack)
    print("MIRROR LEAKAGE %.1f per cent of ask weight  (bar: under %.0f)" % (leak, LEAK_BAR))
    print("PAIR CEILING %.1f  (bar: at or under %.0f)" % (pair, PAIR_BAR))
    bad = [n for n, ok in (("cracker keeps ask figures", crack == 0.0),
                           ("mirror leakage", leak < LEAK_BAR),
                           ("pair ceiling", pair <= PAIR_BAR)) if not ok]
    if bad:
        print("FAIL: %s" % ", ".join(bad))
    return pair, leak, crack


if __name__ == "__main__":
    p, l, c = main()
    sys.exit(0 if (p <= PAIR_BAR and l < LEAK_BAR and c == 0.0) else 1)

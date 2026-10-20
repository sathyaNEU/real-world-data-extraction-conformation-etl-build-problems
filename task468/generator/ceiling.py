"""The pair ceiling, measured on the cut pack (supplemental-stumping Part 0). The cracker lands the call, runs the hygiene
battery (claim numbers unique, every replacement and void points at a bill in the extract, every NPI maps through the
network list, no exact duplicate rows) and executes every handling the files document: each bill as the system that
paid it recorded it (a CPS replacement's change added to its original, a platform replacement in its original's place,
a voided bill nothing; the extract notes file both), Carrisford's stays are not Halbrook's payments, the stays are those
discharged in fiscal 2026, both of Mercy Valley's NPIs map, and the dispute log's additional payments made on those
stays are added. The mirror stops on the best-scoring wrong rung of the ladder and builds the payments the same way.
Weights 38 / 7 / 55: the main block's 38 as the call (the count and the set) 10 and each hospital's verdict 2; the 55
over the fifteen bonus figures (each hospital's and the total).

    python3 task468/generator/ceiling.py [target]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B      # noqa: E402
import numpy as np      # noqa: E402
import world as W       # noqa: E402

TASK = os.path.dirname(HERE)


def r100(v):
    return int(round(v / 100.0)) * 100


def main(target):
    P = B.Pack(target)
    f = P.frame()
    gold = P.determination(frame=f)["losers"]
    gb = {h: r100(v) for h, v in P.bonus().items()}
    gt = r100(sum(P.bonus().values()))

    def main_score(losers):
        call = losers == gold
        hits = sum((h in losers) == (h in gold) for h in W.CANDIDATES)
        return 10 * call + 2 * hits, call, hits

    def ask_score(b):
        hits = sum(r100(b[h]) == gb[h] for h in W.CANDIDATES) + (r100(sum(b.values())) == gt)
        return 55 * hits / 15.0, hits

    crack_b = P.bonus(awards="paid")
    m, _, _ = main_score(gold)
    a, ah = ask_score(crack_b)
    C = m + 7 + a
    print("cracker: call landed, main %.1f + instructions 7 + ask %.1f (%d of 15 figures) = %.1f" % (m, a, ah, C))
    rungs = {
        "R0 the links as deaths": P.determination(how="naive", frame=f)["losers"],
        "R1 plus the deaths later bills record": P.determination(how="union", frame=f)["losers"],
        "R2 less the links later claims contradict (the default path)": P.determination(how="reflex", frame=f)["losers"],
        "R3a the false links removed alone": P.determination(how="fp_only", frame=f)["losers"],
        "R3b the missed deaths added alone": P.determination(how="recall_only", frame=f)["losers"],
        "R4a both corrected at one network rate": P.determination(by="all", frame=f)["losers"],
        "R4b both corrected by number on file": P.determination(by="pass", frame=f)["losers"],
        "R4c both corrected at each hospital's own rates": P.determination(by="all", frame=f,
                                                                           mkw=dict(hosp_rates=True))["losers"],
    }
    best = None
    for k, losers in rungs.items():
        mm, call, hits = main_score(losers)
        S = mm + 7 + a
        print("mirror on %-62s main %.1f (call %s, %2d of 14 verdicts) + 7 + ask %.1f (%d of 15) = %.1f" % (
            k, mm, call, hits, a, ah, S))
        if best is None or S > best[0]:
            best = (S, k)
    pair = (C + best[0]) / 2
    print("Pair ceiling: %.1f (cracker %.1f, best mirror %.1f on %s)" % (pair, C, best[0], best[1]))
    print("Mirror leakage: %.1f per cent of ask weight (%d of 15 figures)" % (100.0 * ah / 15, ah))
    for k, kw in (("every paid award added (the cracker)", dict(awards="paid")),
                  ("the dispute log left out", dict(awards="none")),
                  ("every award decided, paid or not", dict(awards="decided")),
                  ("the amount disputed", dict(awards="disputed")),
                  ("awards by the day they were paid", dict(award_basis="payment")),
                  ("a replacement in its original's place", dict(how="standard")),
                  ("every line summed", dict(how="sum")), ("every replacement added", dict(how="net")),
                  ("admission date as the basis", dict(basis="admission")),
                  ("Carrisford's payments added", dict(with_cmg=True)),
                  ("awards a bill already paid left out (golden)", dict())):
        print("ask stop %-52s %d of 15" % (k, ask_score(P.bonus(**kw))[1]))
    print("The asks read no row or column the call reads: the call is unchanged with every paid amount blanked "
          "(checks.py S1), so the two responses' ask rows are scored on the same payments path by construction.")
    return pair


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target"))

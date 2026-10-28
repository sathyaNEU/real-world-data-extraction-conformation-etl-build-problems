"""The ask sheet, measured on the cut pack. The cracker lands the call, runs the hygiene battery (exact duplicate rows
dropped, UTC converted to UK dates, imports left out, the duty repeated on a declaration's item rows priced item by
item as litres times the rate) and executes every filed rule (CE14: a correction replaces the declaration it names, in
the period the release was first accepted; nothing for a cancellation; repayments when accepted; removals to premises
not approved that day at that day's rate), reading the correction rule the natural way: the declaration a correction
names is taken as the release. Each other careful reading of the corrections is scored beside it, and so is the route
that follows every chain to its first release. The mirror stops on the most attractive wrong rung of the call (cider,
the cut's own triangle) and does the asks as the cracker does, since the asks read no file the call reads
(checks.py, separation). Weights 38 / 7 / 55 (supplemental-stumping Part 0), a hit within half a unit of the rounding.

    python3 task118/generator/pair.py"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P  # noqa: E402
import solve as SV  # noqa: E402

CAREFUL = [
    ("one_hop", "litres x rate with the battery; a correction dated and priced by the declaration it names"),
    ("one_hop_duty", "the same, priced at the release's own rates (the declaration duty split by item)"),
    ("one_hop_header_once", "the same, the repeated declaration duty kept once on the first item"),
    ("own_quarter", "each correction in the quarter of its own acceptance"),
    ("latest_per_named", "the latest correction of each named declaration kept"),
    ("every_declaration", "every release declaration counted, corrections too"),
    ("named_by_any", "the chain followed, but a release a repayment names also dropped"),
]
FOUND = [
    ("first_own_rate", "the chain followed to the first release, each correction priced on its own day"),
    ("golden", "the chain followed to the first release, priced on that day"),
]


def rounded(X):
    return {c: {q: SV.thousand(X[c][q]) for q in P.ASK_QUARTERS} for c in X}


def keep(X, G):
    return sum(X[c][q] == G[c][q] for c in G for q in P.ASK_QUARTERS)


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    zp = os.path.join(os.path.dirname(target), "target.zip")
    stamp = hashlib.sha256(open(zp, "rb").read()).hexdigest()[:8] if os.path.exists(zp) else "unzipped"
    G = rounded(SV.asks(target))
    cr = rounded(SV.asks(target, "one_hop"))
    n = 20
    print("pack: target.zip sha256 %s" % stamp)
    print("%-30s %12s %12s %12s %s" % ("criterion (GBP thousand)", "golden", "cracker", "mirror", "cracker verdict"))
    for c, *_ in P.DUTIES:
        for q in P.ASK_QUARTERS:
            print("%-30s %12.1f %12.1f %12.1f %s" % ("%s %s" % (c, q), G[c][q], cr[c][q], cr[c][q],
                                                     "HIT" if cr[c][q] == G[c][q] else "miss"))
    print("\ncareful paths (the battery and CE14 executed), cells kept of %d:" % n)
    worst = 0
    for m, label in CAREFUL:
        k = keep(rounded(SV.asks(target, m)), G)
        worst = max(worst, k)
        print("  %2d  %-20s %s" % (k, m, label))
    print("paths that find the device:")
    for m, label in FOUND:
        print("  %2d  %-20s %s" % (keep(rounded(SV.asks(target, m)), G), m, label))
    kc = keep(cr, G) / n
    km = kc
    c_score = 38 + 7 + 55 * kc
    m_score = 5 + 7 + 55 * km
    print("\ncracker keeps %d of %d (%.3f); mirror %d (%.3f), the same path: the asks read no file the call reads"
          % (round(kc * n), n, kc, round(km * n), km))
    print("honest max over the careful paths: %d of %d" % (worst, n))
    print("cracker %.1f  mirror %.1f  pair ceiling %.1f  mirror leakage %.1f per cent"
          % (c_score, m_score, (c_score + m_score) / 2, 100 * km))
    wc = 38 + 7 + 55 * worst / n
    wm = 5 + 7 + 55 * worst / n
    print("at the honest max on both rows: pair %.1f; if both responses follow every chain: pair %.1f"
          % ((wc + wm) / 2, (100 + 67) / 2))
    return (c_score + m_score) / 2, 100 * km, worst


if __name__ == "__main__":
    main()

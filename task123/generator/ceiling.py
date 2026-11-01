"""Scores the cracker and the mirror on the cut pack (target/), figure by figure, and prints the pair ceiling.

The cracker lands the call and runs the hygiene battery on every ask: the last submission of each code, the
crosswalk from CIR to the register, the last filing of each declaration, every dated register variation applied
from its date. The mirror stops at the most attractive wrong rung on the call (the filled August returns
benchmarked to the declared quarter) and works the asks the same careful way. A figure is kept when it equals the
golden at the asked rounding."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402

T = os.path.join(os.path.dirname(HERE), "target")


def r100(v):
    return int(round(v / 100.0)) * 100


def main():
    p = A.load(T)
    res = A.main_call(p)
    gold_ja = A.ask_jan_apr(p)
    gold_occ = A.ask_oct_occupancy(p)
    gold_tax = A.ask_tax_2025(p)
    careful_ja = A.ask_jan_apr(p, via="reg", dedupe=False)
    careful_occ = A.ask_oct_occupancy(p, corrections=False)
    careful_tax = A.ask_tax_2025(p, "latest")
    asks = [("A1 January to April 2026 guest nights by member comune", len(gold_ja),
             sum(r100(careful_ja[c]) == r100(gold_ja[c]) for c in gold_ja)),
            ("A2 2025 tourist tax due by quarter", 4, sum(r100(careful_tax[q]) == r100(gold_tax[q]) for q in gold_tax)),
            ("A3 October 2025 net bed-place occupancy by type", len(gold_occ),
             sum(round(careful_occ[t], 1) == round(gold_occ[t], 1) for t in gold_occ))]
    n_fig = sum(a[1] for a in asks)
    kept = sum(a[2] for a in asks)
    Lc = kept / n_fig
    Ls = Lc
    C = 38 + 7 + 55 * Lc
    S = 5 + 7 + 55 * Ls
    print("| Ask | Figures | Cracker keeps | Verdict |")
    print("|---|---|---|---|")
    for name, n, k in asks:
        print("| %s | %d | %d | %s |" % (name, n, k, "miss" if k < n else "HIT"))
    gold = A.designation(res, "golden")
    mirror = A.designation(res, "R2_ct")
    print("call: golden %s; mirror %s" % ([res[c]["name"] for c in gold], [res[c]["name"] for c in mirror]))
    print("ask figures %d, cracker keeps %d (%.1f per cent); mirror keeps %.1f per cent" % (n_fig, kept, 100 * Lc, 100 * Ls))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f" % (C, S, (C + S) / 2))


if __name__ == "__main__":
    main()

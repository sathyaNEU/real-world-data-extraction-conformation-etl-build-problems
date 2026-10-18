"""Solve the pair ceiling: both responses rescored on Part 0's weights, both columns printed.

Stage 2: solves on the generator's clean truth in core.py. At stage 3 the figure lookups are
re-pointed through verify.py's own bundle pipeline so the ceiling is measured on what ships.
Exits 1 unless the pair is at or under 40 and the mirror leakage under 35.
"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core

W_REC, W_INSTR, W_ASKS = 38.0, 7.0, 55.0
BAR_PAIR, BAR_LEAK = 40.0, 35.0

def inventory():
    """One row per graded ask figure, with who can recover it and why."""
    inv = [("ask1_national_change", "free")]
    for q in ("2026Q1", "2026Q2", "2026Q3", "2026Q4"):
        inv.append(("ask2_covered_interviews_%s" % q, "schedule"))
    for c in core.codes:
        kind = "blank" if c == core.BLANK else "grouped"
        inv.append(("ask3_%s_benchmark" % c, kind))
        inv.append(("ask3_%s_rate" % c, kind))
    return inv

def keeps(resp, inv):
    out = []
    for name, kind in inv:
        if kind == "free":
            out.append(name)            # the call's own population: no device may sit here
        elif kind == "blank":
            out.append(name)            # the blank sends any reader to the published table
        elif kind == "schedule" and resp == "cracker":
            out.append(name)            # executes the filed per-interview rate
    return out

def forcing():
    """Each device's forcing gap, measured on the truth, against its asking sentence's rounding."""
    lines = collections.Counter()
    for r in core.CL:
        lines[r["q"]] += 1
    g2 = {q: core.PERQ[q] for q in ("2026Q1", "2026Q2", "2026Q3", "2026Q4")}
    smallest = min(abs(g2[q] - lines[q]) for q in g2)
    gaps = [abs(core.G3[(c, "rate")] - core.N3[(c, "rate")])
            for c in core.codes if core.N3[(c, "rate")] is not None]
    return g2, lines, smallest, (min(gaps), max(gaps))

def main():
    inv = inventory()
    g2, lines, smallest, (lo, hi) = forcing()
    print("ask device forcing, measured on the truth")
    for q in g2:
        print("  ask2 %s golden %5d | claim lines read as interviews %5d | gap %5d"
              % (q, g2[q], lines[q], g2[q] - lines[q]))
    print("  ask2 smallest quarterly gap %d interviews, figures stated in whole interviews" % smallest)
    print("  ask3 grouped-area rate gap %.1f to %.1f per 1,000 against a 0.05 bin half-width" % (lo, hi))
    print("  ask3 %s carries no benchmark at all" % core.BLANK)
    print()
    rows = []
    for resp, rec in (("cracker", W_REC), ("mirror", 5.0)):
        k = keeps(resp, inv)
        frac = len(k) / float(len(inv))
        rows.append((resp, rec, len(k), frac, rec + W_INSTR + W_ASKS * frac))
    print("pair ceiling on Part 0 weights %g / %g / %g" % (W_REC, W_INSTR, W_ASKS))
    print("  response   rec   kept      fraction   score")
    for resp, rec, nk, frac, sc in rows:
        print("  %-9s %5.1f  %2d of %2d   %.4f     %5.1f" % (resp, rec, nk, len(inv), frac, sc))
    pair = sum(r[4] for r in rows) / 2.0
    leak = 100.0 * rows[1][3]
    print("  PAIR CEILING   = %.1f  (bar 50, build to 40)" % pair)
    print("  MIRROR LEAKAGE = %.1f per cent of ask weight" % leak)
    print("  ask figures     = %d" % len(inv))
    if pair > BAR_PAIR or leak > BAR_LEAK:
        print("FAIL: pair %.1f or leakage %.1f outside the bars" % (pair, leak))
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())

"""The pair ceiling on the cut pack: the cracker lands the call and takes the careful route through every ask;
the mirror stops at the balanced default (rung 0) and, the asks being decoupled from the call, takes the same
careful route through them.  C = 38 + 7 + 55 Lc, S = 5 + 7 + 55 Ls, pair = (C + S) / 2."""
import os, sys
import analysis as A
import routes as R

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASKS = [("A July use by riser (MWh, 2 dp)", "july_mwh", 0.01, R.a_cracker),
        ("B charger requests by riser", "requests", 1.0, R.b_cracker),
        ("C time outside the limits by riser (%, 2 dp)", "voltage_pct", 0.01, R.c_cracker)]


def binv(v, u):
    return round(round(v / u) * u, 6)


def main(target):
    E = A.everything(target)
    D, U = E["D"], E["units"]
    rows, kept, total = [], 0, 0
    for name, key, u, fn in ASKS:
        g = E[key]
        r = fn(D, U)
        k = sum(1 for x in g if binv(r[x], u) == binv(g[x], u))
        rows.append((name, len(g), k, k))
        kept += k
        total += len(g)
    Lc = kept / total
    Ls = Lc
    C = 38 + 7 + 55 * Lc
    S = 5 + 7 + 55 * Ls
    pair = (C + S) / 2
    print("| Ask | Figures | Cracker keeps | Mirror keeps | Verdict |")
    print("|---|---|---|---|---|")
    for name, n, k, m in rows:
        print("| %s | %d | %d | %d | %s |" % (name, n, k, m, "miss" if k < n else "keep"))
    print("\nLc = %.3f, Ls = %.3f, C = %.1f, S = %.1f, pair ceiling = %.1f, mirror leakage = %.1f per cent of ask weight"
          % (Lc, Ls, C, S, pair, 100 * Ls))
    return pair, 100 * Ls


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target"))

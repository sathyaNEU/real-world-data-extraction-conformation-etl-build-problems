"""The ask sheet as code on the cut pack: the cracker, the full includer, the no-repair reader and the mirror, each
scored figure by figure against the golden (a hit is within half a unit of the stated rounding).

    python3 ceiling.py            prints the sheet and the pair ceiling; exit 1 if the ceiling is over 60
The cracker landed the call, ran the hygiene battery (latest correction, rejected entries out, five-minute sequences,
lockouts read from each device's final state, local quarters, holiday rate) and reads each ask the careful way it
reads it; the full includer also counts each member once across devices and each employee's chained jobs as one
callout; the mirror is the best response off the call, handling the asks as the cracker does (the asks do not turn on
the call)."""
import hashlib, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden

T = os.path.join(os.path.dirname(HERE), "target")


def score(P):
    gA = golden.maifi_files(P, "golden")
    gh, gp = golden.callouts_files(P, "golden")
    rows = {}
    for route in ("cracker", "full", "norepair"):
        A = golden.maifi_files(P, route)
        h, p = golden.callouts_files(P, route)
        ha = sum(1 for k in gA if abs(round(A[k], 2) - round(gA[k], 2)) < 0.005)
        hb = sum(1 for i in range(12) if abs(round(h[i]) - round(gh[i])) < 0.5) + sum(1 for i in range(12) if abs(round(p[i]) - round(gp[i])) < 0.5)
        rows[route] = (ha, hb)
    rows["mirror"] = rows["cracker"]
    return rows


def main():
    P = golden.load(T)
    rows = score(P)
    digest = hashlib.sha256(open(os.path.join(os.path.dirname(HERE), "target.zip"), "rb").read()).hexdigest()[:12]
    nA, nB = 16, 24
    print("pack digest %s" % digest)
    print("%-10s %12s %12s %10s" % ("route", "A kept", "B kept", "share"))
    for r, (a, b) in rows.items():
        print("%-10s %8d/%-3d %8d/%-3d %9.1f%%" % (r, a, nA, b, nB, 100.0 * (a + b) / (nA + nB)))
    Lc = (rows["cracker"][0] + rows["cracker"][1]) / float(nA + nB)
    Lm = (rows["mirror"][0] + rows["mirror"][1]) / float(nA + nB)
    C = 38 + 7 + 55 * Lc
    S = 5 + 7 + 55 * Lm
    pc = (C + S) / 2
    print("cracker on the call %.1f, mirror off it %.1f: pair ceiling %.1f; mirror leakage %.1f per cent" % (C, S, pc, 100 * Lm))
    for ask, i, n in (("A", 0, nA), ("B", 1, nB)):
        print("cracker row %s: %s" % (ask, "miss" if rows["cracker"][i] <= n // 3 else "KEEPS"))
        print("full includer row %s: %s" % (ask, "misses a block" if rows["full"][i] < n else "KEEPS ALL"))
    return 0 if pc <= 60 else 1


if __name__ == "__main__":
    sys.exit(main())

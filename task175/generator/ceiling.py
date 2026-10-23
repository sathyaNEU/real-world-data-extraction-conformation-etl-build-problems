"""The pair ceiling, run on the cut pack, on every verbatim reader path the stage 4 rounds recorded, the cracker and the
stored phase. The asks are the four phase totals of fiscal 2026 new connections and the twenty phase and quarter cells
of fiscal 2026 capacity fees.

  cracker   counts every fiscal 2026 install and sums every receipt line
  reader A  round 1: drops installs at premises whose first account predates the install, plat-unit phases
  reader B  round 1: drops installs at premises whose first account started more than 1,000 days before the install
  reader D  round 2: a premise's first install, at a premise with no account opened before it, plat-unit phases
  reader E  round 3: one per premise at first install (reader D's count), and the same at ACTIVE premises only
  reader F  round 3: one connection per normalised service address at its first install, prior accounts excluded
  reader G  round 4: a lot's first install (parcel, else address), replacements and re-installs excluded: the golden
            count on connections
  reader H  round 4: the CIS phase codes, stubs kept (the stored-phase route)
  stored    reader A with the premise's stored UEP_PHASE

Every reader so far summed the fees by receipt date; each route is priced on the fee handling that keeps the most
cells among every line, one amount per receipt number (first or last line), per receipt number and amount, and per
receipt number and date. Reader C's path was not recorded beyond its score. Weights 38, 7, 55 (supplemental-stumping
Part 0); a hit only when exact at the stated rounding; the call is landed on every route (worst case).

    python3 ceiling.py <target>"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc                 # noqa: E402

PHASES = ["Core", "1", "2", "3", "4"]
CELLS = [(ph, q) for ph in PHASES for q in (1, 2, 3, 4)]


def main(target):
    P = calc.Pack(target)
    r = calc.connections_fy26(target, P)
    fees, lines, by_no, fx = calc.fees_fy26(target, P, extra=True)
    tot = lambda rt: [sum(r[rt][(ph, q)] for q in (1, 2, 3, 4)) for ph in PHASES[1:]]
    golden = tot("golden") + [round(fees[c]) for c in CELLS]
    fee_ways = {"lines": lines, "number": by_no, **fx}
    conn_routes = {"cracker": "cracker", "reader A": "reader_a", "reader B": "reader_b", "reader D": "reader_d",
                   "reader E": "reader_d", "reader E (ACTIVE)": "reader_e", "reader F": "reader_f", "reader G": "golden",
                   "reader H": "stored_phase", "stored": "stored_phase"}
    n = len(golden)
    keep, worst_way = {}, {}
    for k, rt in conn_routes.items():
        best = -1
        for way, fw in fee_ways.items():
            if k == "cracker" and way != "lines":
                continue
            v = tot(rt) + [round(fw[c]) for c in CELLS]
            hit = sum(1 for a, b in zip(golden, v) if a == b)
            if hit > best:
                best, worst_way[k] = hit, way
        keep[k] = best
    for k, v in keep.items():
        print("%-18s keeps %2d of %d ask figures (fees priced on %s)" % (k, v, n, worst_way[k]))
    print("connections, phase totals: golden %s; reader D %s; reader F %s; stored %s" % (tot("golden"), tot("reader_d"),
                                                                                          tot("reader_f"), tot("stored_phase")))
    worst = max(keep.values())
    L = worst / n
    C_score = 38 + 7 + 55 * L
    S_score = 5 + 7 + 55 * L
    pair = (C_score + S_score) / 2
    print("worst route keeps %d of %d: cracker %.1f, mirror %.1f, pair ceiling %.1f, leakage %.1f per cent of ask weight"
          % (worst, n, C_score, S_score, pair, 100.0 * L))
    return pair


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))

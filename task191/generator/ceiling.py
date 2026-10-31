"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task191/generator/ceiling.py

Rows: the cracker lands the call, runs the battery (repeated rows out, the October bordereau as the latest
snapshot, the metres on the new module's lines converted, the registration history joined) and executes every
filed rule (lines 000 and ESC out of hours on service, a session in the week it starts, depots by HR on the start
date, codes A and C at fault, each depot's kilometres for the lines it operates), but sums each log-on session as
written and on the wall clock (ask A), counts every incident report and every claim number's latest paid to date
(ask B), and takes the return's kilometres as filed (ask C); the mirror stops at rung 0 on the call and handles the
asks the same way, since they carry nothing from the call; the full includer also ends a session at the driver's
next log-on, adds the hour when clocks go back, counts one incident per pair of reports, one paid amount per
reopened chain and applies the diversions (a stress row, not the gate). The chart's structure is banked by every
response that draws it."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import estim as E   # noqa: E402

BANKED = 1          # the chart's structure


def figures(D, a_kw, b_kw, c_kw):
    a, _ = E.ask_a(D, **a_kw)
    cnt, paid, _ = E.ask_b(D, **b_kw)
    km, _ = E.ask_c(D, **c_kw)
    flat = []
    for d in E.DEPOT_ORDER:
        flat += [("A", d, i, a[d][i]) for i in range(4)]
        flat += [("B count", d, 0, cnt[d]), ("B paid", d, 0, paid[d])]
        flat += [("C", d, i, km[d][i]) for i in range(4)]
    return flat


def kept(resp, gold):
    return sum(1 for x, y in zip(resp, gold) if x[3] == y[3])


def main():
    D = E.load()
    gold = figures(D, {}, {}, {})
    n = len(gold) + BANKED
    crack_f = figures(D, dict(dst=False, overlap=False), dict(dedupe=False, chains=False), dict(diversions=False))
    crack = kept(crack_f, gold) + BANKED
    full = kept(figures(D, {}, {}, {}), gold) + BANKED
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc          # the mirror's ask handling is the cracker's: the asks carry nothing from the call
    by_ask = {}
    for x, y in zip(crack_f, gold):
        by_ask.setdefault(x[0][0], [0, 0])
        by_ask[x[0][0]][0] += x[3] == y[3]
        by_ask[x[0][0]][1] += 1
    print("cracker (lands the call, battery, filed rules; sessions as written on the wall clock, every report and "
          "claim number, the return's kilometres as filed): keeps %d of %d ask criteria (%s), response %.1f"
          % (crack, n, ", ".join("%s %d of %d" % (k, v[0], v[1]) for k, v in sorted(by_ask.items())), c))
    print("mirror (rung 0 on the call, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("full includer (every device resolved, stress row): keeps %d of %d, response %.1f"
          % (full, n, 38 + 7 + 55 * full / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))


if __name__ == "__main__":
    main()

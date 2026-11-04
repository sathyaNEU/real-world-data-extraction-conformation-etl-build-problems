"""The pair ceiling on the cut pack. The cracker lands the call, runs the battery and executes every filed rule it
points at; on the asks it compensates the absolute loggers with the barologger reading of the same clock face, reads
the register's logger serials as they stand, and prices every interval on the register's schedule. The mirror stops at
the default path (each unmetered well at its test's kWh per acre-foot) and handles the asks as the cracker does.
Weights 38 / 7 / 55: the main block (purchase 12, ranch total 4 as a 0.5 per cent band, the fifteen wells' water year
volumes 22 as 1 per cent bands), the instructions 7, the asks (Ask A 14, the construction layer's static depths 10,
Ask D 31)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import golden as G   # noqa: E402

W_PUR, W_TOT, W_WELLS, W_INSTR = 12.0, 4.0, 22.0, 7.0
W_A, W_CONS, W_D = 14.0, 10.0, 31.0


def main(target=None, quiet=False):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    d = G.load(target)
    gold = G.extraction(d)
    mirror = G.extraction(d, route="R0")
    wells = sorted(d["reg"])
    # the wells and the ranch are graded as bands (1 and 0.5 per cent), the precision the pairing conventions leave
    keep_m = sum(1 for w in wells if abs(mirror["reported"][w] / gold["reported"][w] - 1) <= 0.01)
    main_c = W_PUR + W_TOT + W_WELLS
    main_m = (W_PUR if mirror["purchase"] == gold["purchase"] else 0) + \
        (W_TOT if abs(mirror["total"] / gold["total"] - 1) <= 0.005 else 0) + W_WELLS * keep_m / len(wells)
    absolute = [w for w in wells if "absolute" in str(d["reg"][w]["Level logger"])]
    vented = [w for w in wells if w not in absolute]
    gs = {w: G.static_depths(d, w) for w in wells}
    cs = {w: G.static_depths(d, w, baro_shift=-8, swap_aware=False) for w in absolute}
    a_hit = sum(1 for w in absolute for k in ("spring", "fall") if round(cs[w][k][1], 1) == round(gs[w][k][1], 1))
    a_n = 2 * len(absolute)
    cons_hit = 2 * len(vented)
    gc = G.energy_charges(d)
    cc = G.energy_charges(d, schedule="register")
    d_hit = sum(1 for w in wells if round(cc[w]) == round(gc[w]))
    ask = W_A * a_hit / a_n + W_CONS * cons_hit / (2 * len(vented)) + W_D * d_hit / len(wells)
    cracker = main_c + W_INSTR + ask
    mir = main_m + W_INSTR + ask
    ceiling = (cracker + mir) / 2
    if not quiet:
        print("golden purchase %d, ranch %d against %.1f; mirror purchase %d, ranch %d" % (
            gold["purchase"], gold["total"], gold["available"], mirror["purchase"], mirror["total"]))
        print("mirror keeps %d of %d well volumes; the cracker keeps %d of %d absolute-logger depths, every vented "
              "depth, %d of %d energy charges" % (keep_m, len(wells), a_hit, a_n, d_hit, len(wells)))
        print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight" % (
            cracker, mir, ceiling, 100.0 * ask / (W_A + W_CONS + W_D)))
    return ceiling


if __name__ == "__main__":
    sys.exit(0 if main() <= 60.0 else 1)

"""The ask sheet's arithmetic, run on the cut pack rather than written in prose.

    python3 task125/generator/pair.py [target]

Loads target/, computes each ask three ways (the golden, the cracker's path and the over-correction), counts the
figures each path would be graded right, and prints the pair arithmetic the design note's Ask sheet states:
the cracker (a response that lands the main call and runs the hygiene battery), the mirror (the best response
that stops at rung 0 of the ladder), the pair ceiling and the mirror's leakage of the ask weight."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import deliver as DL   # noqa: E402
import world as W      # noqa: E402

W_REC, W_IF, W_ASK = 38.0, 7.0, 55.0     # the rubric's weights (guide-to-prompt: 30 to 40, 5 to 10, 55 to 60)
N_ASK = 18                                # separately gradable ask figures: 6 regions x 3 asks
REC_MIRROR = 6.0                          # of W_REC, what a response stopped at rung 0 still banks
METHOD_CREDIT = 0.08                      # of the ask weight, credit for a right method with every figure wrong


def counts(target):
    c = DL.compute(target)
    a = c["asks"]
    out = {}
    out["visits"] = {k: sum(1 for g in W.RCODES if a["visits"][k][g] == a["visits"]["golden"][g])
                     for k in ("golden", "rows", "serial_day")}
    out["flows"] = {k: sum(1 for g in W.RCODES if "%.2f" % a["flows"][k][g] == "%.2f" % a["flows"]["golden"][g])
                    for k in ("golden", "person_no", "serial_only")}
    out["hours"] = {k: sum(1 for g in W.RCODES if "%.1f" % a["hours"][k][g] == "%.1f" % a["hours"]["golden"][g])
                    for k in ("golden", "raw", "all_converted")}
    return out


def main(target):
    c = counts(target)
    cracker = c["visits"]["rows"] + c["flows"]["person_no"] + c["hours"]["raw"]
    over = c["visits"]["serial_day"] + c["flows"]["serial_only"] + c["hours"]["all_converted"]
    ask_kept = max(cracker, over) / N_ASK + METHOD_CREDIT * (1 if max(cracker, over) < N_ASK else 0)
    ask_pts = W_ASK * ask_kept
    C = W_REC + W_IF + ask_pts
    S = REC_MIRROR + W_IF + ask_pts
    print("ask figures the cracker's path is graded right: %d of %d (visits %d, flows %d, hours %d)"
          % (cracker, N_ASK, c["visits"]["rows"], c["flows"]["person_no"], c["hours"]["raw"]))
    print("ask figures the over-correction is graded right: %d of %d" % (over, N_ASK))
    print("ask weight kept by either: %.1f per cent (%.1f of %.0f points)" % (100 * ask_kept, ask_pts, W_ASK))
    print("cracker C = %.0f + %.0f + %.1f = %.1f" % (W_REC, W_IF, ask_pts, C))
    print("mirror  S = %.0f + %.0f + %.1f = %.1f" % (REC_MIRROR, W_IF, ask_pts, S))
    print("Pair ceiling: %.1f" % ((C + S) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * ask_kept))
    return (C + S) / 2


if __name__ == "__main__":
    task = os.path.dirname(HERE)
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(task, "target"))

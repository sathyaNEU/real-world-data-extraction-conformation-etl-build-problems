"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task281/generator/ceiling.py

Rows. The cracker lands the call and runs the battery: it pairs a re-photographed referral's two cases under their
referral order and closes the referral on its last grade, moves the reading center's UTC stamps to the Pacific
calendar, and counts a fault's lost days as the days carrying an equipment cancellation at the clinic
up to the camera that replaced it; it reads every case in the reading center log as an AI referral. The mirror
stops at the pooled rung on the call and handles the asks the same way, since nothing in them comes from the call.
The full includer also keeps only REF7734 referral orders and drops the fault day, which still had screenings (a
stress row, not the gate)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
from deliver import rnd  # noqa: E402


def figures(P, scope, route):
    oc, oq = A.ask_overreads(P, scope=scope, pair=True, clock="local")
    dt_ = A.ask_downtime(P, route=route)
    f = {}
    for c, (n, s) in oc.items():
        f["reads " + c] = n
        f["confirmed " + c] = rnd(100 * s)
    for q, v in oq.items():
        f["days " + q] = rnd(v, 1)
    for k, v in dt_.items():
        f["lost days " + k] = v["days"]
    return f


def kept(resp, gold):
    return sum(resp[k] == v for k, v in gold.items())


def main(target=TARGET):
    P = A.Pack(target)
    gold = figures(P, "ai", "history")
    n = len(gold)
    crack = kept(figures(P, "all", "cancel_days"), gold)
    full = kept(figures(P, "ai", "history"), gold)
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call, battery, every log case an AI referral, lost days by equipment cancellations): "
          "keeps %d of %d ask criteria, response %.1f" % (crack, n, c))
    print("mirror (the pooled rung, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("full includer (REF7734 referrals only, the fault day kept out, stress row): keeps %d of %d, response %.1f"
          % (full, n, 38 + 7 + 55 * full / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc


if __name__ == "__main__":
    main()

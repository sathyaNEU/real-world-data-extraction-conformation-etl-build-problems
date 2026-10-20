"""The pair ceiling on the cut pack. The cracker lands the call and reads the asks the careful way (accepted messages,
the 2025 departure or death date, the country's time, persons who left twice counted twice, former residents out) and
meets no rule or sweep that sends it to the persons' histories; the mirror stops at the rung that keeps the most
qualifications and reads the asks the same way. Weights 38 / 7 / 55: the call 8, each of the 24 qualifications 1.25,
each of the 48 ask figures 55/48.

    python3 task471/generator/ceiling.py     exit 0 at 40 or under
"""
import itertools
import os
import sys

import bundle as B
import methods as M

W_CALL, W_QUAL, W_INSTR, W_ASK = 8.0, 1.25, 7.0, 55.0
HERE = os.path.dirname(os.path.abspath(__file__))


def hits(a, b, codes):
    return sum(1 for m in codes if a[m] == b[m])


def main(target=None, quiet=False):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    pk = B.Pack(target)
    gold = set(pk.qualifying())
    gd, gt = pk.departures(), pk.deaths()
    n = len(pk.codes)
    ask_cracker = hits(pk.departures(void="keep"), gd, pk.codes) + hits(pk.deaths(void="keep"), gt, pk.codes)
    best, best_keep = None, -1
    for name in M.RUNGS:
        s = set(pk.qualifying(name))
        if s == gold:
            continue
        keep = sum(1 for m in pk.codes if (m in s) == (m in gold))
        if keep > best_keep:
            best, best_keep = name, keep
    cracker = W_CALL + W_QUAL * n + W_INSTR + W_ASK * ask_cracker / (2.0 * n)
    mirror = W_QUAL * best_keep + W_INSTR + W_ASK * ask_cracker / (2.0 * n)
    # the strongest single reading of either ask a careful response could take, device by device
    strongest = 0
    for clock, void in itertools.product(("local", "utc"), ("exclude", "keep", "drop_registered")):
        if (clock, void) != ("local", "exclude"):
            strongest = max(strongest, hits(pk.departures(clock=clock, void=void), gd, pk.codes))
    for clock, res, void in itertools.product(("local", "utc"), ("registered", "none"), ("exclude", "keep")):
        if (clock, res, void) != ("local", "registered", "exclude"):
            strongest = max(strongest, hits(pk.deaths(clock=clock, residency=res, void=void), gt, pk.codes))
    pair = (cracker + mirror) / 2
    if not quiet:
        print("golden: %d municipalities; best mirror %s keeps %d of %d qualifications" % (len(gold), best, best_keep, n))
        print("the cracker's ask reading keeps %d of %d ask figures; the strongest single mishandled reading keeps %d "
              "of %d" % (ask_cracker, 2 * n, strongest, n))
        print("cracker %.2f, mirror %.2f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight" % (
            cracker, mirror, pair, 100.0 * ask_cracker / (2 * n)))
    return pair


if __name__ == "__main__":
    sys.exit(0 if main() <= 40.0 else 1)

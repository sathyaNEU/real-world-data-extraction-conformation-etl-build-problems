"""The ask layer measured on the cut pack: violator bed-days by quarter and level (Ask A, 8 figures) and the felony
probationers on supervision by supervising office and time on supervision (Ask B, 16 figures) under the golden's
handling and the handlings a response is likely to take, scored figure by figure (a hit is the exact whole number),
and the pair ceiling those keeps imply.

    python3 task141/generator/ceiling.py

The cracker links each commitment booking to the court's revocation for its level, reads the new jail system's UTC
times in county time and chains annex moves and reclassifications, but counts a commitment from its commitment
booking; it takes each officer's open assignment on the roster as the supervising office. The mirror, off the call,
handles the asks the same way."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import common as K  # noqa: E402
import golden as G  # noqa: E402
import pack_read as PR  # noqa: E402

A_HANDLINGS = (("linked, from the booking", dict(how="booking_start")),
               ("classification", dict(how="classification")),
               ("classification, UTC read as local", dict(how="classification_utc")),
               ("linked, UTC read as local", dict(how="utc_as_local")),
               ("classification with holds counted", dict(how="classification", holds=True)))
B_HANDLINGS = (("CMS 2's office", "cms_office"), ("the officer's first office", "first_assignment"),
               ("the officer's office when supervision began", "office_at_start"),
               ("the officer's open assignment as exported", "current_assignment"))
CRACKER = ("linked, from the booking", "the officer's open assignment as exported")


def figures_a(tab):
    return [int(tab[i, j]) for i in range(4) for j in range(2)]


def figures_b(tab):
    return [tab[(o[0], k)] for o in K.OFFICES for k in range(4)]


def measure(P=None):
    P = P or PR.read()
    ga = figures_a(G.bed_days(P))
    gb = figures_b(G.supervision_counts(P))
    keep_a = {name: sum(a == b for a, b in zip(figures_a(G.bed_days(P, **kw)), ga)) for name, kw in A_HANDLINGS}
    keep_b = {name: sum(a == b for a, b in zip(figures_b(G.supervision_counts(P, how)), gb)) for name, how in B_HANDLINGS}
    return ga, gb, keep_a, keep_b


def pair(keep_c, keep_m, total, call=45.0, miss=12.0):
    """the pair ceiling: the cracker on the call, the mirror off it, each keeping its share of 55 ask points"""
    return ((call + 55.0 * keep_c / total) + (miss + 55.0 * keep_m / total)) / 2


if __name__ == "__main__":
    ga, gb, keep_a, keep_b = measure()
    n = len(ga) + len(gb)
    print("graded ask figures: %d (Ask A %d, Ask B %d)" % (n, len(ga), len(gb)))
    for k, v in keep_a.items():
        print("  Ask A  %-46s keeps %d of %d" % (k, v, len(ga)))
    for k, v in keep_b.items():
        print("  Ask B  %-46s keeps %d of %d" % (k, v, len(gb)))
    kc = keep_a[CRACKER[0]] + keep_b[CRACKER[1]]
    print("cracker keeps %d of %d (%.1f per cent of ask weight); mirror the same; pair ceiling %.1f" % (
        kc, n, 100.0 * kc / n, pair(kc, kc, n)))
    best = max(keep_a.values()) + max(keep_b.values())
    print("the best non-golden handling of each ask keeps %d of %d together (%.1f per cent)" % (best, n, 100.0 * best / n))
    print("a reader who cracks Ask A alone keeps %d of %d (%.1f per cent); Ask B alone %d (%.1f per cent)" % (
        len(ga) + keep_b[CRACKER[1]], n, 100.0 * (len(ga) + keep_b[CRACKER[1]]) / n, len(gb) + keep_a[CRACKER[0]],
        100.0 * (len(gb) + keep_a[CRACKER[0]]) / n))

"""The ask layer measured on the cut pack: violator bed-days by quarter (Ask A, 8 figures) and the average imposed term
of the felony probationers on supervision (Ask B, 8 figures) under the golden's handling and the handlings a response is
likely to take, scored figure by figure (a hit is the exact whole day, or the month to one decimal), and the pair
ceiling those keeps imply.

    python3 task141/generator/ceiling.py

The cracker reads the bookings' classification as the level (PV-FEL felony, PV-MIS misdemeanor), with the new jail
system's UTC times in county time and annex moves and reclassifications chained, and takes CMS 2's term_months as
the term imposed. The mirror, off the call, handles the asks the same way."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import common as K  # noqa: E402
import golden as G  # noqa: E402
import pack_read as PR  # noqa: E402

A_HANDLINGS = (("classification", dict(how="classification")),
               ("classification, UTC read as local", dict(how="classification_utc")),
               ("linked, UTC read as local", dict(how="utc_as_local")),
               ("linked, current Sheriff's numbers only", dict(how="current_ids")),
               ("classification with holds counted", dict(how="classification", holds=True)))
B_HANDLINGS = (("term_months as it stands", "as_it_stands"), ("expiration less supervision begin", "from_dates"),
               ("open terms past expiration left out", "not_past_expiration"))
CRACKER = ("classification", "term_months as it stands")


def figures_a(tab):
    return [int(tab[i, j]) for i in range(4) for j in range(2)]


def figures_b(res):
    offs, sups = res[0], res[1]
    return [K.round1(v) for v in list(offs) + list(sups)]


def measure(P=None):
    P = P or PR.read()
    ga = figures_a(G.bed_days(P))
    gb = figures_b(G.imposed_terms(P))
    keep_a = {name: sum(a == b for a, b in zip(figures_a(G.bed_days(P, **kw)), ga)) for name, kw in A_HANDLINGS}
    keep_b = {name: sum(a == b for a, b in zip(figures_b(G.imposed_terms(P, how)), gb)) for name, how in B_HANDLINGS}
    return ga, gb, keep_a, keep_b


def pair(keep_c, keep_m, total, call=45.0, miss=12.0):
    """the pair ceiling: the cracker on the call, the mirror off it, each keeping its share of 55 ask points"""
    return ((call + 55.0 * keep_c / total) + (miss + 55.0 * keep_m / total)) / 2


if __name__ == "__main__":
    ga, gb, keep_a, keep_b = measure()
    n = len(ga) + len(gb)
    print("graded ask figures: %d (Ask A %d, Ask B %d)" % (n, len(ga), len(gb)))
    for k, v in keep_a.items():
        print("  Ask A  %-42s keeps %d of %d" % (k, v, len(ga)))
    for k, v in keep_b.items():
        print("  Ask B  %-42s keeps %d of %d" % (k, v, len(gb)))
    kc = keep_a[CRACKER[0]] + keep_b[CRACKER[1]]
    print("cracker keeps %d of %d (%.1f per cent of ask weight); mirror the same; pair ceiling %.1f" % (
        kc, n, 100.0 * kc / n, pair(kc, kc, n)))
    best = max(keep_a.values()) + max(keep_b.values())
    print("the best non-golden handling of each ask keeps %d of %d together (%.1f per cent)" % (best, n, 100.0 * best / n))

"""The ask layer measured on the cut pack: the back series (arrivals registered for work and long-term immigration by
sector, five years) under the golden's handling and under the handlings a response is likely to take, scored figure by
figure against the golden (a hit is the exact whole-person count), and the pair ceiling those keeps imply.

    python3 task485/generator/ceiling.py

Every handling reads the legacy archive's day-first dates, maps the 2014 activity codes to the 2026 sectors and counts
a stay by its arrival date; they differ in how they take the stays open at the 2023 move and whether they count once a
stay the legacy register held twice. The golden takes the archive's records, each one open at the move with the
leaving date of its TRANSFER record, and counts once the records identical in every declared particular whose stays
ended on one day on notices received the same day. The cracker builds the series the same way from the archive and
the TRANSFER records' leaving dates and counts every record."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import golden as G  # noqa: E402

HANDLINGS = [("cracker", "archive_stitched"), ("current_records_as_they_are", "current_transfer"),
             ("current_records_twins_once", "current_transfer_twins"),
             ("stitched_current_activity", "stitch_current_activity"), ("stitched_current_date", "stitch_current_date"),
             ("declared_fields_deduplicated", "declared_dedupe"), ("both_systems_counted", "both")]


def figures(AB, P):
    A, B = AB
    f = {"arrivals.%d.%s" % (y, s): A[y][s] for y in G.BACK_YEARS for s in P.sectors}
    f.update({"long.%d.%s" % (y, s): B[y][s] for y in G.BACK_YEARS for s in P.sectors})
    return f


def measure(P=None):
    P = P or G.Pack()
    gold = figures(G.back_series(P), P)
    keeps = {}
    for name, how in HANDLINGS:
        f = figures(G.back_series(P, how), P)
        keeps[name] = sum(1 for k in gold if f[k] == gold[k])
    return gold, keeps


def pair(keep_c, keep_m, total, call=45.0, miss=12.0):
    """the pair ceiling: the cracker on the call, the mirror off it, each keeping its share of 55 ask points"""
    return ((call + 55.0 * keep_c / total) + (miss + 55.0 * keep_m / total)) / 2


if __name__ == "__main__":
    gold, keeps = measure()
    n = len(gold)
    print("graded ask figures:", n)
    for k, v in keeps.items():
        print("  %-30s keeps %2d of %d" % (k, v, n))
    kc = keeps["cracker"]
    print("cracker keeps %.1f per cent of ask weight; mirror the same; pair ceiling %.1f" % (100.0 * kc / n, pair(kc, kc, n)))
    worst = max(keeps.values())
    print("the best non-golden handling keeps %d of %d (%.1f per cent)" % (worst, n, 100.0 * worst / n))

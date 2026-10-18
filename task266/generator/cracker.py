"""The cracker's and the mirror's paths, run on the cut pack.

The cracker landed the call, ran the hygiene battery, executed every rule the asking sentences point at and matched
every control. For each ask this module computes what that path returns and scores it against the golden within half
a unit of the stated rounding (FTE to one decimal, whole classes). The mirror stops at the default path on the call
and takes the natural read of every ask. It is measurement, not argument.

    python3 task266/generator/cracker.py [target]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402

CHART = 3              # the chart's form criteria, kept by any response that draws one


def cracker(target):
    """Each ask as the cracker reads it. A: Policy 4.1 and 4.3 executed, the credit hours registered at the census
    (registrations in place on the census date, later withdrawals kept) by the program of record in effect for fall
    2026 in the history, each registration at the credit hours its row carries. B: Policy 4.2's sections scheduled to
    meet together taken as sections sharing an instructor, days, begin time and the schedule's start and end dates
    (online sections apart), so the eight-week halves stay apart; census registrations as in A."""
    return dict(A=A.ask_a(target, credits="row"), B=A.ask_b(target, group="exact"))


def without_dates(target):
    """The same cracker with the meeting key that leaves the section dates out (instructor, days and begin time)."""
    return dict(A=A.ask_a(target, credits="row"), B=A.ask_b(target, group="meeting"))


def mirror(target):
    """The natural reads: the registration rows' credit hours by the extract's program, every RE, RW and WC row; the
    schedule's enrolment under ten, section by section."""
    return dict(A=A.ask_a(target, credits="row", program="row", census="status"),
                B=A.ask_b(target, enrol="export", group="none"))


def score(target, got):
    ga, gb = A.ask_a(target), A.ask_b(target)
    progs = sorted(ga)
    return [("A", len(progs), sum(abs(round(got["A"][p], 1) - round(ga[p], 1)) < .05 for p in progs)),
            ("B", len(progs), sum(got["B"][p] == gb[p] for p in progs))]


def ceiling(cr, mi):
    """supplemental-stumping Part 0: C = 38 + 7 + 55 Lc, S = r + 7 + 55 Ls with r about 5, the chart's form to both."""
    total = sum(n for _a, n, _h in cr)
    lc = sum(h for _a, _n, h in cr) / float(total)
    ls = sum(h for _a, _n, h in mi) / float(total)
    return total, lc, ls, ((38 + 7 + CHART + 55 * lc) + (5 + 7 + CHART + 55 * ls)) / 2.0


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    cr, mi = score(tgt, cracker(tgt)), score(tgt, mirror(tgt))
    for (ask, n, h), (_a, _n, m) in zip(cr, mi):
        print("%s: %d figures, cracker keeps %d, mirror keeps %d" % (ask, n, h, m))
    total, lc, ls, pair = ceiling(cr, mi)
    print("total %d figures, cracker keeps %.1f per cent, mirror leakage %.1f per cent, pair ceiling %.1f"
          % (total, 100 * lc, 100 * ls, pair))
    print("without the dates in the meeting key: Ask B %d of %d" % score(tgt, without_dates(tgt))[1][2:0:-1])

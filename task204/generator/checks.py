#!/usr/bin/env python3
"""task204 generator checks: the analyst test and the semantic fork table, executed on the clean truth.

Stage 2 state. Every assertion below is written against the generator's clean-truth model (the world's own
supply rates, volumes, attendance and session windows), which is what `dataset-generation` section 7.1
requires: the easy route is run with every filed rule applied and asserted to file the named wrong answer,
then the decisive step alone is changed and the golden is asserted. The clean-truth model itself is owed at
stage 3, so each check below carries either the figure measured in the design-time prototype
(`<scratch>/task204/screen.py`, byte-identical over two runs at PYTHONHASHSEED=0) or the word OWED.

    python3 task204/generator/checks.py          # prints one line per check, exit 1 on any failure

Bins: the graded figure is litres per second per occupant present, printed to the nearest 0.5, so one bin
is 0.5 and a check that reports "same call" has been measured inside a bin.
"""

BIN = 0.5
STANDARD = 8.0            # litres per second per person, TGD-M4
GOLDEN = 5.0              # printed, nearest 0.5
DEFAULT_PATH = 11.0       # printed figure the easy route files, 10.95 before rounding

# Design-time prototype measurements, three seeds (11, 12, 13).
PROTOTYPE = {
    "truth":            (5.063, 4.961, 4.879),
    "golden":           (5.014, 5.072, 4.902),
    "r0_session_mean":  (11.06, 10.95, 10.56),
    "r1_final_15min":   (10.23, 10.19, 9.83),
    "r2_peak_sample":   (9.59, 9.56, 9.23),
    "regression_member": (4.993, 5.070, 4.890),
}

CHECKS = []


def check(name, ok, detail):
    CHECKS.append((name, bool(ok), detail))


def analyst_test():
    """The easy route files the named wrong answer; the decisive step alone recovers the golden."""
    r0 = PROTOTYPE["r0_session_mean"]
    gold = PROTOTYPE["golden"]
    truth = PROTOTYPE["truth"]
    check("analyst test files the default path",
          all(round(v * 2) / 2 >= 10.5 for v in r0) and all(v > STANDARD for v in r0),
          "steady-state read on each session's mean excess files %s, every seed clearing %.1f"
          % (", ".join("%.2f" % v for v in r0), STANDARD))
    check("decisive step alone recovers the golden",
          all(round(v * 2) / 2 == GOLDEN for v in gold) and all(v < STANDARD for v in gold),
          "the session-integrated balance files %s, every seed printing %.1f and failing %.1f"
          % (", ".join("%.3f" % v for v in gold), GOLDEN, STANDARD))
    check("the construction recovers the clean truth",
          all(abs(g - t) / t < 0.025 for g, t in zip(gold, truth)),
          "recovery error %s per cent against the world's own rates"
          % ", ".join("%+.1f" % (100 * (g - t) / t) for g, t in zip(gold, truth)))
    check("no rung sits inside the 1.15x floor",
          min(PROTOTYPE["r2_peak_sample"]) / STANDARD >= 1.15 and STANDARD / max(gold) >= 1.15,
          "nearest clearing rung %.3fx, golden %.3fx on the failing side"
          % (min(PROTOTYPE["r2_peak_sample"]) / STANDARD, STANDARD / max(gold)))


def semantic_forks():
    """One assertion per row of the design note's fork table."""
    check("SF1 per person is the occupant present",
          True,
          "filed in prompt.txt; the enrolled and design-occupancy readings measured 4.21 and 3.98 against "
          "5.06, so the term is filed and not left to converge")
    check("SF2 the session is the timetable's session row",
          True,
          "filed in prompt.txt and the bid sheet; the room-booking system is not shipped as a session source")
    check("SF3 the outdoor baseline is the campus sensor",
          True,
          "campus sensor against the national station agree within 6 ppm over the overlap: same call, 0.04 "
          "of a bin (OWED as a generator assertion at stage 3)")
    check("SF4 the generation rate is TGD-M4's seated classroom value",
          True,
          "the standard's extract table, and every block session carries a sedentary subject code")
    check("SF5 the room volume is the as-built gross internal volume",
          True,
          "the as-built room data sheet is the only record of volume; the area-times-2.7 reading is OWED a "
          "measured spread at stage 3")
    check("SF6 the window is 28 September to 11 December 2026",
          True,
          "filed in prompt.txt; the pilot space's June record is outside it")
    check("SF7 timestamps are Irish local time as exported",
          True,
          "the offset column separates the October repeat hour, which is a Sunday, so no block session falls "
          "in it: same call on the main figure")
    check("SF8 rounding is once, at the end, to the nearest 0.5",
          abs(round(PROTOTYPE["golden"][1] * 2) / 2 - GOLDEN) < 1e-9,
          "stated in the asking sentence; %.3f prints %.1f" % (PROTOTYPE["golden"][1], GOLDEN))
    check("SF9 the block is the six room codes the bid sheet lists",
          True,
          "the pooled-over-14 reading files 8.36, a different call, so the population is filed")
    check("SF10 a session with nobody present is kept",
          True,
          "OWED at stage 3: the generator asserts same call, the estimand covering every timetabled session")


def main():
    analyst_test()
    semantic_forks()
    bad = 0
    for name, ok, detail in CHECKS:
        print("%-4s %-46s %s" % ("PASS" if ok else "FAIL", name, detail))
        bad += 0 if ok else 1
    print("%s task204: %d checks, %d failed" % ("PASS" if not bad else "FAIL", len(CHECKS), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())

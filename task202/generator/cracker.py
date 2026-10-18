"""The cracker and mirror sheets, measured on the cut pack rather than argued on paper.

The cracker is the response that LANDS the call, runs the hygiene battery (key uniqueness, exact
duplicates, unmatched joins, fan-out, count ties) and executes every filed rule it points at; the
mirror is the best response that stops at a wrong rung of the call. Each ask figure is scored a hit
when it falls within half a unit of the rounding the asking sentence states.

Where the criteria sit, because the previous pass's measurement turned on exactly this. The six band
ceilings, the twelve referred shares and the six scale factors are the recommendation's own schedule:
they are generated from the committed ceiling by schedule B over the population clause 9 declares, so
a response that lands the call has them all, and they are scored in the recommendation and critical
components block that Part 0 prices at 38. The ask band is the closed-period annex, whose figures are
computed from two files the ceiling never reads, over claim months that closed before its window
opened. The audit line at the foot prints what the pair would be if the schedule were scored as asks
instead, which is the accounting that measured 65.5 and the reason the ask layer was re-sited.

    python3 task202/generator/cracker.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build as B
import params as P
import writeup as WU

W_REC, W_INSTR, W_ASK, R_KEEP = 38.0, 7.0, 55.0, 5.0
TARGET = os.path.join(os.path.dirname(HERE), "target")

# the asking sentence's own rounding: the annex amounts to the nearest peso, the claim-months whole
UNIT = {"A": 1.0, "B": 1.0, "C": 1.0}
ASKS = [("A the pesos the payment runs transferred, by scheme quarter", "A", 1),
        ("B the pesos the claim checks held back, by scheme quarter", "B", 1),
        ("C the claim-months with a hold, by reason", "C", 1)]
# what the cracker's path files on each ask: it sums the column as the export states it and groups
# by the column the ask names, which is stop 1 of each ladder (stop 2 of C, which reports the blanks
# rather than dropping them, is the kinder reading and is scored too)
CRACKER_STOP = {"A": 0, "B": 0, "C": 1}
SCHEDULE_CRITERIA = 24          # six ceilings, six referred shares, six value shares, six factors

# The reader-calibrated response, which is the measurement that matters. The cracker's stops are the
# author's guesses at the opponent's routes, and the stage 4 reader beat all three of them: it kept
# 0 of 6 on A, 6 of 6 on B and 6 of 6 on C where the cracker said nought of eighteen. So this row is
# not a guess. It is the stop each ask's ladder reaches for a response that
#   * reads the data dictionary and applies every convention filed in it,
#   * reconciles each closed-period file against the claim returns, which is what found the
#     register's running totals, and
#   * takes the ordinary hygiene moves (key uniqueness, folding a free-text field onto its list,
#     cross-tabulating a blank against the movement that produced it).
# A is at its answer because the re-issue convention is now filed, which is what makes the device
# fair and is what it costs. B is at the scheme-year stop, because the year the return workbooks
# label is the year such a response assumes and the accreditation year is in no sentence. C is at its
# answer, because the blank-reason device is the one the reader cracked and the rewording did not
# replace it.
READER_STOP = {"A": "A5", "B": "B3", "C": "C4"}


def rows_of(group, stops, gold, keys):
    labels = list(stops[group])
    out = []
    for i, label in enumerate(labels):
        vals = stops[group][label]
        hits = sum(1 for k, g in zip(keys, gold) if abs(vals[k] - g) <= UNIT[group] / 2.0)
        out.append((label, hits, len(keys)))
    return out


def main():
    fig = WU.figures(TARGET, B.FILES)
    a = fig["asks"]
    stops = WU.ask_stops(TARGET, B.FILES)
    keys = {"A": a["quarters"], "B": a["quarters"], "C": WU.REASONS}
    gold = {"A": [a["transferred"][q] for q in a["quarters"]],
            "B": [a["held"][q] for q in a["quarters"]],
            "C": [a["holds_by_reason"][r] for r in WU.REASONS]}
    print("golden call PHP %s; the annex covers claim months %s to %s"
          % ("{:,}".format(fig["call"]), "2024-07", "2025-12"))

    print("\nCRACKER: lands the call, runs the battery, executes clause 4.2, 9.2, 9.3 and schedule B")
    print("   recommendation and critical components: lands the call and generates all %d schedule"
          % SCHEDULE_CRITERIA)
    print("   figures from it, so it banks the whole %.0f-point block before any ask" % W_REC)
    crows, n_ask = [], 0
    for label, grp, _ in ASKS:
        ladder = rows_of(grp, stops, gold[grp], keys[grp])
        pick = ladder[CRACKER_STOP[grp]]
        crows.append((label, pick[1], pick[2]))
        n_ask += pick[2]
        print("   %-58s keeps %d of %d   (%s)" % (label, pick[1], pick[2], pick[0][:46]))
    kept = sum(h for _, h, _ in crows)
    print("   every other stop measured on this pack, for the record:")
    for label, grp, _ in ASKS:
        for lab, h, n in rows_of(grp, stops, gold[grp], keys[grp]):
            print("      %-66s %d of %d" % (lab[:66], h, n))

    print("\nMIRROR: stops at a wrong rung of the call (rung 1 to 5 of the ladder)")
    print("   the annex asks consume nothing the call's construction produces, so the mirror's ask")
    print("   row is the cracker's row figure for figure. The separation is asserted, not asserted")
    print("   by assumption: checks.py separation.ceiling_without_either_ask_file recomputes the")
    print("   ceiling from a folder holding only the four files the call reads and gets PHP 7,800,")
    print("   separation.checks_rows_in_the_window and separation.archive_rows_in_the_window are 0,")
    print("   and separation.device_partner_months_in_the_window is 0. Printing a second scored row")
    print("   would be comparing a list with itself, so the mirror's ask weight is the cracker's.")

    print("\nREADER-CALIBRATED: applies every filed convention and the ordinary hygiene moves")
    rkept = 0
    for label, grp, _ in ASKS:
        ladder = rows_of(grp, stops, gold[grp], keys[grp])
        pick = next(r for r in ladder if r[0].startswith(READER_STOP[grp]))
        rkept += pick[1]
        print("   %-58s keeps %d of %d   (%s)" % (label, pick[1], pick[2], pick[0][:46]))
    Lr = rkept / float(n_ask)
    rpair = (W_REC + R_KEEP) / 2.0 + W_INSTR + W_ASK * Lr
    print("   keeps %d of %d ask figures, %.3f of the ask weight" % (rkept, n_ask, Lr))
    print("   PAIR AT THE READER'S KEEP %.1f   (bar 50, build to 40)" % rpair)
    if rpair > 50:
        print("   OVER THE BAR. The ask band cannot absorb a fair Ask A at %d graded figures: filing"
              % n_ask)
        print("   the re-issue convention hands back 6 of %d, and Ask C's blank-reason device is the"
              % n_ask)
        print("   one the reader already cracked. Holding the pair under 50 at this keep rate needs")
        print("   more graded figures, which needs prompt room, which is a rubric pass and not a")
        print("   determinism one. Reported rather than papered over.")

    Lc = kept / float(n_ask)
    Lm = Lc
    Cs = W_REC + W_INSTR + W_ASK * Lc
    Ss = R_KEEP + W_INSTR + W_ASK * Lm
    pair = (Cs + Ss) / 2.0
    print("\nPAIR on Part 0's weights (%.0f recommendation and components, %.0f instruction, %.0f asks,"
          " r = %.0f)" % (W_REC, W_INSTR, W_ASK, R_KEEP))
    print("   cracker keeps %d of %d ask figures, %.3f of the ask weight -> %.1f" % (kept, n_ask, Lc, Cs))
    print("   mirror  keeps %d of %d ask figures, %.3f of the ask weight -> %.1f" % (kept, n_ask, Lm, Ss))
    print("   PAIR CEILING %.1f   (bar 50, build to 40)" % pair)
    print("   MIRROR LEAKAGE %.1f per cent of ask weight (bar under 35)" % (100 * Lm))

    print("\nwhat the pair would be at each keep count, the asks being decoupled so both rows move:")
    for k in range(0, n_ask + 1, 2):
        p = (W_REC + R_KEEP) / 2.0 + W_INSTR + W_ASK * k / n_ask
        print("   both responses keep %2d of %d -> pair %.1f%s"
              % (k, n_ask, p, "   <= 40" if p <= 40 else ""))
    hold = max(k for k in range(n_ask + 1)
               if (W_REC + R_KEEP) / 2.0 + W_INSTR + W_ASK * k / n_ask <= 40)
    print("   so the asks have to hold both responses to %d of %d or fewer, which is the fifth each"
          % (hold, n_ask))
    print("   that Part 0 prices; the deepest stop measured keeps 5 of %d (C3, the response that"
          % n_ask)
    print("   differences the register and folds the free text but drops the blank reasons), and a")
    print("   response that cracks one whole ask would keep 6 of %d for a pair of %.1f" %
          (n_ask, (W_REC + R_KEEP) / 2.0 + W_INSTR + W_ASK * 6 / n_ask))

    alt = n_ask + SCHEDULE_CRITERIA
    altC = W_REC + W_INSTR + W_ASK * (kept + SCHEDULE_CRITERIA) / alt
    altS = R_KEEP + W_INSTR + W_ASK * (kept + 8) / alt
    print("\naudit line, the accounting the previous pass used: scoring the schedule's %d figures in"
          % SCHEDULE_CRITERIA)
    print("   the ask band instead puts the pair at %.1f (cracker %.1f, a mirror keeping the six"
          % ((altC + altS) / 2.0, altC))
    print("   factors and two content criteria %.1f). The gate takes the figure above, because the"
          % altS)
    print("   schedule is the recommendation's own components over the call's own population and")
    print("   Part 1.2 ban 4 forbids counting it as an ask at all.")
    return pair, 100 * Lm


if __name__ == "__main__":
    main()

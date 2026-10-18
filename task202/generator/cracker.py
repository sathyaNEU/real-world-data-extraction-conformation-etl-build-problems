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

# the asking sentence's own rounding: the annex amounts to the nearest peso, the instruction and
# claim-month counts whole
UNIT = {"A": 1.0, "B": 1.0, "C": 1.0}
ASKS = [("A of each quarter's claims, the pesos settled and the instructions", "A", 1),
        ("B the pesos the claim checks passed and the pesos they held back", "B", 1),
        ("C the partner claim-months a hold was recorded in, by reason", "C", 1)]
# what the cracker's path files on each ask: it sums the column as the export states it and groups
# by the column the ask names, which is stop 1 of each ladder (stop 2 of C, which reports the blanks
# rather than dropping them, is the kinder reading and is scored too)
CRACKER_STOP = {"A": 0, "B": 0, "C": 1}
SCHEDULE_CRITERIA = 24          # six ceilings, six referred shares, six value shares, six factors

# The reader-calibrated response, which is the measurement that matters, and each row's provenance.
# The stage 4 reader (a medium thread holding only the pack and prompt.txt) beat all three cracker
# stops on the previous cut: it kept 0 of 6 on A, 6 of 6 on B and 6 of 6 on C. This row is that
# reader's stop on each ask, re-scored on this cut:
#   A  MEASURED 0 of 6. The reader summed the run lines as the archive states them and was high on
#      every quarter. The previous pass then filed the re-issue convention in the data dictionary
#      to make the device fair, which handed the ask back in one step; that sentence is gone and the
#      asking sentence now closes the reading instead ("of those claims the pesos settled": run
#      lines summing above what the partner claimed cannot answer it). So the measured stop stands.
#   B  MEASURED 0 of 6. The reader found the register's running totals and assumed the scheme year;
#      the series turns over on the partner's own accreditation anniversary (stop B3).
#   C  MEASURED 6 of 6, and NOT REPAIRED. The reader cross-tabulated the increments against the
#      reason column and read the blank both ways. Its primary reaches one figure of six (stop C3
#      keeps five), so Ask C has no effective device mass, and Part 6's free-figure rule is why it
#      was not widened with the other two: widening an ungated ask hands figures away.
READER_STOP = {"A": "A1", "B": "B3", "C": "C4"}
READER_NOTE = {"A": "MEASURED by the stage 4 reader, pin removed since",
               "B": "MEASURED by the stage 4 reader",
               "C": "MEASURED by the stage 4 reader, primary NOT replaced"}


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
    QA = a["quarters"]
    keys = {"A": QA + ["n " + q for q in QA], "B": QA + ["passed " + q for q in QA],
            "C": list(WU.REASONS)}
    gold = {"A": [a["transferred"][q] for q in QA] + [a["instructions"][q] for q in QA],
            "B": [a["held"][q] for q in QA] + [a["passed"][q] for q in QA],
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
    print("   ceiling from a folder holding only the four files the call reads and gets PHP 8,000,")
    print("   separation.checks_rows_in_the_window and separation.archive_rows_in_the_window are 0,")
    print("   and separation.device_partner_months_in_the_window is 0. Printing a second scored row")
    print("   would be comparing a list with itself, so the mirror's ask weight is the cracker's.")

    print("\nREADER-CALIBRATED: the stop an isolated reader at medium effort actually reached")
    rkept, per = 0, {}
    for label, grp, _ in ASKS:
        ladder = rows_of(grp, stops, gold[grp], keys[grp])
        pick = next(r for r in ladder if r[0].startswith(READER_STOP[grp]))
        rkept += pick[1]
        per[grp] = pick
        print("   %-58s keeps %2d of %2d" % (label, pick[1], pick[2]))
        print("      %-55s %s" % (pick[0][:55], READER_NOTE[grp]))
    Lr = rkept / float(n_ask)
    rpair = (W_REC + R_KEEP) / 2.0 + W_INSTR + W_ASK * Lr
    print("   keeps %d of %d ask figures, %.3f of the ask weight" % (rkept, n_ask, Lr))
    print("   PAIR AT THE READER'S KEEP %.1f   (bar 50, build to 40)" % rpair)
    print("   sensitivity, one whole ask lost to a reader this row does not model:")
    for label, grp, _ in ASKS:
        n_i = len(keys[grp])
        alt = rkept - per[grp][1] + n_i
        print("      %-56s %2d of %2d -> pair %.1f" % ("all of " + label[:48], alt, n_ask,
              (W_REC + R_KEEP) / 2.0 + W_INSTR + W_ASK * alt / n_ask))

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
    print("   that Part 0 prices. The reader-calibrated row above sits at %d of %d." % (rkept, n_ask))

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

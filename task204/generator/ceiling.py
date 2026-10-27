#!/usr/bin/env python3
"""The ask sheet's pair arithmetic for task204.

Stage 2: a design-time model. The weights are the rubric's, the per-ask shares are what each ask's device
is designed to leave a careful response, and the two responses are both off the main call because the
ladder is built to take them to the default path's 10.9 litres per second per occupant present. Stage 3
re-runs this file against the cut pack with the shares measured instead of modelled, and the design note's
two figures move to whatever it prints then.

    python3 task204/generator/ceiling.py
"""

# Rubric weights, per cent of the whole response (CLAUDE.md, Current spec).
W_RECOMMENDATION = 36.0        # recommendation and critical components
W_INSTRUCTION = 7.0            # instruction-following
W_ASKS = 57.0                  # the asks

# What a response banks on the recommendation side (stumping Part 0): about 45 on the call, about 12 off it.
ON_CALL = 45.0
OFF_CALL = 12.0

# The asks, their graded figure counts and the share of each the device is designed to leave.
# share_a: the stronger cold response. share_b: the second.
ASKS = [
    # ask, figures, share_a, share_b, the device that sets the share
    ("A occupied hours above 1,500 ppm, space x month", 56, 0.34, 0.29,
     "plant occupied state against timetabled sessions, and 25 local hours on 25 October"),
    ("B share of expected readings received, per space", 14, 0.50, 0.43,
     "the expected base counts teaching days only"),
    ("C mean occupants present per session, six spaces", 6, 0.50, 0.33,
     "the enrolment group size against the attendance register"),
    ("D the four largest single-session rises", 8, 0.25, 0.25,
     "the largest raw rises straddle the lunch setback"),
]


def main():
    figures = sum(a[1] for a in ASKS)
    per_figure = W_ASKS / figures
    ask_a = sum(a[1] * a[2] for a in ASKS) * per_figure
    ask_b = sum(a[1] * a[3] for a in ASKS) * per_figure
    # Instruction-following: both responses follow the prompt's shape, so both keep most of it.
    ins_a, ins_b = 0.85 * W_INSTRUCTION, 0.80 * W_INSTRUCTION
    total_a = OFF_CALL + ask_a + ins_a
    total_b = OFF_CALL + ask_b + ins_b
    pair = (total_a + total_b) / 2.0
    mirror = 100.0 * ask_a / W_ASKS

    print("task204 ask sheet, design-time model (stage 3 re-measures on the cut pack)")
    print("  graded ask figures            %d over %d asks" % (figures, len(ASKS)))
    print("  weight per ask figure         %.4f per cent" % per_figure)
    for name, n, sa, sb, dev in ASKS:
        print("  %-48s %3d figures  a %.2f  b %.2f   %s" % (name, n, sa, sb, dev))
    print("  response A, off the call      %.1f = %.1f recommendation + %.1f asks + %.1f instruction"
          % (total_a, OFF_CALL, ask_a, ins_a))
    print("  response B, off the call      %.1f = %.1f recommendation + %.1f asks + %.1f instruction"
          % (total_b, OFF_CALL, ask_b, ins_b))
    print("  PAIR CEILING                  %.1f per cent (built to 60, bar 70)" % pair)
    print("  MIRROR LEAKAGE                %.1f per cent of ask weight (ceiling 50)" % mirror)
    print("  on-call reference             a response that landed 5.0 would bank %.1f on the "
          "recommendation side" % ON_CALL)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

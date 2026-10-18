# task197 determinism review (isolated judge thread)

**Order kept.** I derived from the prompt and the pack first and wrote the derivation to disk (task197_derivation.md) before opening task197_graded_blocks.md. I did not open any forbidden path, run no git command and spawned nothing.
**Disclosure.** The scratchpad folder `w/` already held many working files from earlier passes. I listed it once by accident (ls) and opened none of them, but my first script was written to `w/ep.py` and `w/eps.pkl` and overwrote two earlier files of those names (an earlier pass's scratch only, not part of the task folder). All later work is in my own folder `j197/`. Nothing from an earlier pass was used.

**Verdict:** DETERMINISTIC
**Disposition:** APPROVE (advisories below, none needs a rerun)

## Why
Every committed figure reproduced from the shipped files with an independent rebuild: Kampvliet 72 per cent over 134 episodes, Reiderland 83 per cent, gap 11 points, three sites outside tolerance, all nine under and eight over-frequency gains, the six capacity-hour blocks and the nine-site energy table. The call is forced because the baseline is identified by the data (the quiet-minute power follows a per-site traverse, the step and undisturbed-level baselines do not), and the gap to the runner-up is 10.7 points.

## Gate table
| Gate | Result | Line |
|---|---|---|
| A correct | PASS | All load-bearing and supplementary figures recompute; 911 pairs, 134 episodes, spans 90 s (KPV) and 300 s (TRB) all reproduce |
| B facts in files | PASS | Everything is in the pack. The old OOS meter code is not in the register but is the only unmatched meter, ends where the new one starts and matches event 4112 |
| C uniquely forced | PASS with advisories | Main call forced (see recomputations). Forks that exist: step vs ramp programme energy (literal text gives step), face-value vs UTC clock on 9 withdrawal events (logged_utc forces UTC), cancelled events (stated). None moves the main call |
| D hard for right reason | PASS | Splits come from the counterfactual baseline, not from wording |
| E prompt unambiguous | PASS | One site, one gain, one runner-up, units and rounding in the sentence |
| F stump power | PASS, strong | Step setpoint files RDL 57 per cent, undisturbed level files ZWT 72 per cent, ramp files KPV 72 per cent |
| G stumping type | PASS | line below |
| H three rules | PASS | line below |

**Gate G:** `mechanism: other (counterfactual baseline identification, with a binding tolerance rule)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported figure is wrong: the programme, frequency and power are all correct as published, and the difficulty is estimating the output the site would have produced, which survives on perfectly clean data.

**Gate H:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Swap test: the deciding quantity is a primary-response gain measured against the characteristic of a frequency reserve standard, which no other field estimates in this form. Layer 1: end-stamped meters with a misleading period column, kWh at one meter, a meter replaced mid window, UTC clock written as local on 9 log events, duplicate recording, corrections that cancel log entries. Layer 2: the counterfactual output (traverse recovered at uncommitted boundaries). Easy route for an analyst who read everything right: take the period setpoint as the undisturbed output (RDL 57 per cent, files Reiderland) or the last pre-deviation power (ZWT 72 per cent, files Zwartewater).

## Recomputation 1: traverse span
Fitted at boundaries where the site held no commitment, measured samples, linear ramp from previous to new setpoint, start at the boundary:
DLK 100 s, HGZ 185, KPV 90, MPD 200, NWV 95, OOS 85, RDL 190, TRB 300, ZWT 80. Unique to about 1 s: a span 1 s away has an error only 3 to 37 per cent larger; 5 s away it is 2.0x (OOS, KPV) to 10x (TRB) larger, so the runner-up on the 5 s grid is the neighbour (KPV 85 or 95 s). Fractional fit lands on the same integers (KPV 90.0 to 90.25). Competing readings of the criterion (new period uncommitted, both periods, previous period, either, all boundaries, with or without a quiet-frequency filter) all give the same nine spans. The one reading that differs is boundaries where the site WAS committed: the archive has no samples in the first two minutes after those boundaries for DLK, KPV and ZWT, so the fit collapses to 1 s (unidentified); for the other six it agrees. The criterion therefore recovers each span uniquely and is the only one that identifies KPV.

## Recomputation 2: realised gain and counterfactual baselines (under-frequency, per cent)
Ramp with fitted span (answer): DLK 93.1, HGZ 88.0, KPV 72.1, MPD 97.1, NWV 90.9, OOS 94.8, RDL 82.8, TRB 101.1, ZWT 98.8. Below 90: KPV, RDL, HGZ.
| baseline left open by the text | furthest below |
|---|---|
| ramp, fitted span | KPV 72.1 |
| period setpoint (step) | RDL 57.4 (below: RDL, KPV, HGZ, TRB 76.8, MPD 78.7) |
| previous setpoint or last pre-deviation power | ZWT 71.7 (below: ZWT, OOS 80.7, NWV 87.6) |
| common span 120 s | RDL 72.1 |
| common span 300 s | ZWT 79.3 |
Only the ramp reproduces quiet-minute power to the noise floor (residual sd 0.013 MW). The other baselines leave several MW of residual after every boundary, so exactly one is defensible once the power is compared with it. Almost every extreme second falls 60 to 100 s after a boundary, so the baseline decides every gain. Margin KPV to RDL 10.7 points; plus or minus 5 s on every span moves KPV 70.6 to 73.5 and RDL 82.3 to 83.3, ranking unchanged.

## Recomputation 3: counts and missing recordings
Contracted pairs 1383 (935 under, 448 over). Valid withdrawals remove 5 over-frequency pairs, leaving 1378 (935 under, 443 over). Archive carries a recording of the extreme second for 911 of the 935 under-frequency pairs (the write-up's 911), 431 of 443 over-frequency, 1342 of 1378 in total (1346 of 1383 before withdrawals). Missing pairs are all obliged by construction (24 under, 13 over before withdrawals): HGZ 7, TRB 7, RDL 6, ZWT 6, KPV 3, MPD 3, NWV 3, DLK 1, OOS 1. The pattern is the reverse of "only unobliged missing": the archive holds 97 per cent of obliged pairs but only about 7 per cent (228 of 3252) of unobliged ones. Missing pairs are scattered over days and blocks, with the same deviation depth as recorded ones (median 0.082 against 0.086 Hz); two are a recording that ends seconds before the extreme second. Nothing in the pattern tells a solver the direction of a gain.

## Recomputation 4: distance from rounding edge
Under-frequency gains, in whole per cent from the nearest x.5 edge: DLK 0.403, HGZ 0.470, KPV 0.417, MPD 0.446, NWV 0.381, OOS 0.283, RDL 0.277, TRB 0.434, ZWT 0.349. Over-frequency: DLK 0.499, HGZ 0.353, KPV 0.462, NWV 0.466, OOS 0.342, RDL 0.350, TRB 0.486, ZWT 0.326. Capacity hours are exact at one decimal (18.0, 17.0, 20.9, 7.1, 26.5, 7.8; no rounding at all). Energy (step programme, units of 0.1 MWh): closest are RDL above 0.303, KPV above 0.311, KPV below 0.337, ZWT below 0.391, all others 0.36 to 0.49. No figure prints on a tie; nothing prints within 0.27 of a unit of its edge. The 90 per cent line is cleared by NWV under-frequency at 90.88 (0.88 above) and HGZ at 88.03 (1.97 below).

## Figures that did not reproduce
None. Every graded figure in the three blocks reproduced to its stated rounding. The one difference is not a failing: my first energy reading used the ramp for programme energy (portfolio 80.5 above, 216.4 below), the submission uses the period setpoint (114.4, 242.6), and the step figures reproduce exactly.

## Advisories (none needs a rerun)
1. Energy against programme: the standard says programme energy is "the setpoint the control platform held for that period", and clause 6 settles against the nominated programme, so the step is the literal reading, but a solver who has just found the traverse could carry it into this ask and file 80.5 / 216.4 (site rows move by 3 to 7 MWh). Closing it would need a pin in the standard or the prompt, which changes what solvers see.
2. Nine log events have start_local written in UTC clock time under a +02:00 label (logged_utc minus the label is 7290 s instead of 90 s). Read at face value, no over-frequency pair is withdrawn: OOS over-frequency becomes 89.9 per cent (below tolerance instead of 96), KPV 69.5, ZWT 92.5, HGZ 86.3, and the capacity shortfalls become 10.5, 14.2, 17.5, 4.7, 18.8, 6.5. The UTC reading is forced (an event cannot be logged two hours before it starts; every event then lies in a block the site holds; four recorded seconds show no response). Main call and under-frequency table are unaffected.
3. Settled-statement files, the group availability statement, auction and price files are unused and are fair distractors.

## Hygiene
18 files, formats csv, sqlite, pdf, xlsx (4); one sqlite of 1,194,352 power rows and 4,617 recordings; no authoring language seen in the files read. PASS. Not a cross-batch check (no other task folder may be read).

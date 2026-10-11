# task180 design note: Corran Energy, the field team's patch for January to March 2027

Seed AD03 (revenue-protection crew, register grain). Re-rooted under the two-layer standard: the seed's
calibration corpus, twin pair, licensed wrong basis and withheld rule are not used. The procedure the
organisation would have in writing (RP-07) is filed in full, and the difficulty is the construction it
demands on data whose convenient series is at the wrong grain.

## DRAW

```
Card filed with guard.py register before the ladder was written? yes (WARN, answered below)
Shape: other (8 patches x {referrals, 3 winter-history figures, Q1 capacity} + call, runner-up, gap, chart)
Gate G mechanism: decomposition_attribution
Gap: population (decisive), rule        Pattern: D, two grains both flawless (G2 grain mismatch)
Domain: energy-systems-utilities (client domain)   Subdomain: other (revenue protection)   Objective: anomaly-detection
Pairing repeated from last build? no (energy x anomaly never built)
Stakeholder role: revenue protection manager (field_unit_lead)   Context artifact: monitoring_export (the mart)
Calibration form: none   Decision type: pick_one_of_n   Decisive mechanism: screen per metered supply, count per patch
Stump strategy: grain_or_unit   Decisive rule filed? yes (RP-07 sections 2 to 7)   Official decoy filed? no
Forum: operations_desk (the December planning meeting)   Forcing event: season_or_peak   Org family: utility_or_infrastructure
People (guard.py names, en_GB, seed 180): Gareth Francis (RP manager, RP-07 approver), Judith Jones (field side, prompt
  belief), Christopher Horton (RP analytics, extract owner), Matthew Gill (senior field officer); field officers in the
  visit logs and rota: Alan Khan, Aaron O'Connor, Jonathan Gibson, Debra Martin, Chloe Lewis
```

**Data-native sentence.** In the north of Scotland storage-heated homes carry a second, heating-only supply number
(a related metering point on its own meter), so a bypass of the heating meter takes 36.2 to 57.9 per cent off that supply
while the metering system's weekly total in the analytics mart, keyed by the primary supply number, falls by 6.5
to 23.9 per cent, below the 30 per cent referral band.

**Layer 1 (realistic mess and the system that produces it).** Cumulative midnight register reads from the smart
metering data service with comms gaps and meter exchanges (bridged by the exchange reads in the CIS register); primary
supply numbers to premises through a four-sheet CIS workbook whose related metering points (the heating-only supply
numbers) sit on their own sheet; a weekly analytics-mart table at metering-system grain keyed by the primary supply
number; degree days by station with a patch map in JSON; a field-visit system migration (FieldLink to
FieldOps, re-keyed jobs carrying the legacy number) and an appeals register keyed to whichever system raised the
finding; a group HR holiday calendar that lists both the England and Wales and the Scottish holidays.

**Layer 2 (the analytical shortcut).** Screening the ready-made weekly series. The mart's weekly series, keyed by a supply number, is
the natural input for a supply-level anomaly test, and every count, join and total ties on it; an expert screens each metered
supply against its own history, because an anomaly confined to one component of an additive total is diluted below
any sensible referral band in the total.

**Similarity claim.** No prior build turns on an anomaly test whose filed unit is a metered component while the
convenient series sums the components; the guard's structural near-neighbours (task72, task103, task81, task86, task90)
are attribution, fan-out, identity and chaining moves, differentiated on the card.

**WARN answers.** driver.near task131 (0.15) and task52 (0.14): both read; task131 is interference between sibling
units in a randomised test, task52 a minimum over sub-units, neither is dilution of a component anomaly in a sum.
repeat.decision pick_one_of_n after task131: the decision is genuinely one patch for one team; the answer type is a
named option carrying a count. Deliverable format set moved off docx+png and pptx+xlsx to pptx+csv.

## GATE G

- **Litmus.** No reported number is overturned: the mart's weekly totals are exactly the metering system's import, primary
  plus related supplies (the verifier rebuilds them), every register read, degree day, occupier event and visit record is correct,
  and the difficulty is which series the filed screen runs on.
- **Primary mechanism:** decomposition_attribution (the anomaly lives in one metered component of an additive total).
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`
- **Deletion test.** Delete Judith's belief, both distractors and the history and capacity files: the RP-07 screen run
  on the mart still names Elgin and Lossiemouth and run per supply still names Caithness.
- **Clean-data and instrument test.** The suspect files are the reads (comms gaps) and the mart (coarse grain). Gap
  handling converges: linear interpolation, booking a gap to the later week, and spreading it evenly over its days
  (the verifier's route) give identical referral counts in every patch. The mart is complete at its grain; the
  instrument that observes the decision's own quantity, consumption per supply number, already ships (the reads), and
  the difficulty is choosing it over the metering-system total, not repairing either.
- **Lens swap.** Not one population under two lenses: the rung's unit is a metering system (2,960, keyed by the primary
  supply number), the answer's is a supply number (3,659, 699 of them related heating-only supplies), and a supply-level series has to be built
  from cumulative reads before it can be screened.
- No shipped artifact ranks the patches on referrals. The distractors answer nothing on the decision.

## STUMP SENTENCE

A competent solver runs the filed RP-07 screen (own 104-week degree-day line, 30 per cent over eight weeks, every week
below expected, occupier and heating changes excluded) on the analytics mart's weekly import, keyed by supply number,
and places the team in Elgin and Lossiemouth with 35 referrals; the step that lands it there is taking the mart row
for the supply the procedure screens, when it is a metering system's total, when 42 storage-heated premises in Caithness carry a bypassed heating-only supply
whose 36.2 to 57.9 per cent shortfall moves the metering system total by 6.5 to 23.9 per cent.

## ENTITY AND UNIT OF VALUE

Corran Energy's revenue protection team places one field team per quarter and is judged by referrals worked; RP-07
places it in the patch with the most referred supplies. Two series both look like a supply's "consumption": the mart's weekly
import keyed by the primary supply number, and each supply number's weekly import (reads). They rank the patches differently because only some
patches' premises hold two supplies, and only there does a single-supply anomaly dilute.

## LADDER

| Rung | Construction | Names | Why a careful analyst stops | Killed by |
|---|---|---|---|---|
| belief | best confirmation rate over three winters | Lochaber, 68.2% (15 of 22) | the field side's own outcome record, computed properly (dedupe, appeals) | RP-07 section 7 places on referrals; Lochaber has the fewest (8) |
| 0 | RP-07 screen on the mart's weekly import (keyed by primary supply number), or on the Supplies sheet's supply numbers from the reads | Elgin and Lossiemouth, 35 | the filed method run on a series keyed by supply number, every exclusion applied; every key matches the Supplies sheet and every total ties | RP-07 section 6 glossary (a supply is a supply number and its meter) and the register's Related metering points sheet (699 heating-only supply numbers, each with its own meter) |
| grid | RP-07 per supply, heating changes not excluded | Strathspey, 73 | the decisive grain found, one exclusion missed | RP-07 section 5 and the completions file (heat pumps commissioned June to September 2026) |
| 1 (decisive) | RP-07 per supply number from the reads, exclusions by premises | **Caithness, 54** | | |

Position: Caithness ranks 5th on rung 0 (12, behind Elgin 35, Inverness City 19, Nairn 14, Skye 13), last-but-two on
the belief rung (41.5%), and leads only the decisive rung. Rung margins: belief 68.2 against 57.9 (1.18x, a past
rate, not a referral rung), rung 0 35 against 19 (1.84x), decisive 54 against 35 (1.54x).

**Discriminator dominance.** Elgin carries 35 against Caithness's 12 into the decisive rung (2.92x). The grain move
multiplies Caithness by 4.50 (12 to 54) and Elgin by 1.00: edge 4.50 against the required 1.2 x 2.92 = 3.50, 1.29x
headroom.

**A solver who does everything right up to rung 0 commits to Elgin and Lossiemouth.** Summing each premises' supplies
from the reads and screening the sum (the "build the premises unit" correction) returns exactly the rung-0 counts,
asserted: aggregating before detecting is the same mistake whichever file it starts from.

## GRID (asserted in checks.py, cell by cell)

| Cell | Names | Rule violated |
|---|---|---|
| supply, heating changes kept | Strathspey 73 (1.28x over Caithness 57) | RP-07 s5 |
| supply, occupier changes kept | Inverness City 91 (1.52x over 60) | RP-07 s5 |
| supply, neither exclusion | Inverness City 91 (two violations) | RP-07 s5 twice |
| mart (metering system), occupier changes kept | Inverness City 91 (2.17x over Elgin 42) | RP-07 s5 and s2/s6 |
| mart (metering system), heating changes kept | Elgin 35 | RP-07 s2/s6 |
| Supplies-sheet supply numbers only, from the reads | Elgin 35 (same counts as the mart) | RP-07 s6 and the related sheet |
| premises sum from reads | Elgin 35 | RP-07 s2/s6 |
| supply, no weather adjustment (same weeks a year earlier) | Caithness | RP-07 s3; recorded as a rule violation that happens to land on the answer |

Convergent (identical counts in all eight patches, asserted): degree-day base 14 and 16.5 C, gap booked to the later
week or spread evenly, total-only against every-week test, threshold 25 and 33 per cent, counting premises against
supplies, prepayment supplies left in.

## CLOSURE (the 22 axes)

1 Population: credit accounts, filed (RP-07 s1); prepayment converges (no prepayment supply clears the band). 2 Unit
of account: supply number, filed (s2, s6), and premises against supply counting converges. 3 Attribution window:
weeks Monday to Monday local, filed (s2). 4 As-of dating: register on the run date; patch is a premises attribute, no
moves. 5 Version basis: one register extract; appeals register is the record of decision (s8). 6 Divisor: rate is
over visits with access (s8). 7 Weighting: none in the call; counts. 8 Window length: 104 + 8 weeks, filed (s2).
9 Boundary inclusivity: 30 per cent band sits in an empty gap (ordinary supplies at most 12.4 per cent, diverted at
least 36.2 per cent), C1. 10 Rounding path: counts only in the call; rates rounded once from integer counts, mid-bin
asserted. 11 Tie-break: filed (s7), not reached (no level patches). 12 Maturity: assessment weeks complete; no read
missing on any Monday from 28 September or at the window edges. 13 Order of operations: detect then count is the
decisive move; aggregate-then-detect is the rung. 14 Row order: irrelevant. 15 Duplicate resolution: re-keyed visits
by `legacy_job_no` (field notes), ask layer only. 16 Identity normalisation: MPAN cores are text throughout.
17 Netting: not applicable. 18 Units: kWh throughout. 19 Code semantics: heating change defined in s5 (heat pumps,
new heating system, change of fuel; not insulation or solar); FW-3 codes for field days. 20 Integerisation: whole
visits per day, filed (FW-3 s2), no boundary values. 21 Scope of a clause: s5 exclusions apply to the premises, all its
supplies. 22 Forward window contents: the call is the referrals on the Monday 7 December run (s7), the quarter's
capacity never binds (at least 3x referrals in every patch).

## ASK SHEET

Both asks are decoupled from the screen (the screen never reads the visit logs, appeals register, rota or FW-3,
asserted) and enter the call as the belief's audit trail (history) and the capacity qualifier (can the team work its
referrals).

| Ask | Figures | Primary devices | Stops (asserted to move figures) |
|---|---|---|---|
| Winter history by patch | 8 x (visits with access, confirmed, rate) = 24 | D1 re-keyed migration jobs (FieldLink 4 to 17 Nov 2024 re-created in FieldOps), with genuine revisits after no access as the over-cleaning half; D2/D7 appeals keyed to the raising system's job number, overturned findings count as no fault | no dedupe (8 patches move), no appeals (8), all visits as denominator (8), both (8) |
| Q1 visit capacity by patch | 8 | D8 group HR calendar lists England and Wales and Scotland (FW-3 s3 names Scotland; leave booked on 4 January and 29 March makes the calendars differ by 2 officer-days); D5 third officer's field start 15 February; standby counts as a field day | E&W calendar 136 days, officer counted all quarter 167, standby as leave 137, against 138 |

Pair arithmetic (planning weights): the call block (patch, count, runner-up, gap, eight referral counts, chart parts)
is the 38-point recommendation and critical block and is inherited by a solver on the right grain; the 32 ask figures
are device-carried. A cracker that handles neither device class keeps the capacity figures only if it reads FW-3 s3
and the rota start dates; a mirror sheet (rung 0) keeps the same ask figures as the cracker. Estimated pair:
cracker about 45 + 0.4 x 55, mirror about 7 + 0.4 x 55, mean about 48 at 40 per cent ask leakage, about 41 at 25 per
cent. The ask layer is the weaker half of this build; the solver round reads it.

## PINS

Filed: RP-07 v4 (governing, level 1): scope, screening unit, method, referral test, exclusions, glossary, placement,
reporting. FW-3 (level 1): field day, visit standard, holiday calendar, start dates. Field notes (level 4): field
semantics only (mart grain, read semantics, re-keyed jobs). No counter-pins: no file states that a metering system is screened.

## PACK GATES

17 files, 8 formats (csv, docx, json, md, parquet, pdf, txt, xlsx), largest `smart_daily_reads_*.parquet` at
2,891,687 rows; distractors `prepayment_vends_*.csv` (prepayment is out of RP-07 scope) and
`dno_feeder_loss_estimates_2025-26.xlsx` (all-supplier technical and non-technical losses by feeder), named in
metadata.json.

## SIX-POINT CHECK

1. The inputs take real work (cumulative reads with gaps and exchanges, three-sheet register, occupier and heating
   events by UPRN, migrated visit logs), none of it planted. 2. The flip is a methodological choice: the grain at
   which a filed anomaly test runs. 3. RP-07 defines the population, outcome, window, unit and comparison. 4. No decoy
   memo or staff draft; Judith's belief is a true statement about the past. 5. The method is stated, not recovered
   from certified figures. 6. No earlier task teaches dilution of a component anomaly in an additive total.

## STOPPING RULE

Two solver rounds that land Caithness by reading the RP-07 glossary first file this architecture as at-ceiling for the
main call; a round where the miss lands anywhere other than Elgin and Lossiemouth or Strathspey is read for a fork
before any hardening.

## Tried and rejected

- Seed AD03 as written (register split by each meter's switching regime, recovered from an operator acknowledgement
  corpus): the decisive rule withheld and recovered from a closed corpus is the capped Pattern B pin, and the
  acknowledgement file would refute the whole-house screen case by case (an alarm, not a stump).
- Register split from half-hourly data by time-of-use regime: if daily register reads ship the split is a lookup, and
  if they do not, the realistic route is the separate heating supply, which is how north-of-Scotland storage heating
  is actually metered, so the build uses related supply numbers.
- Account-level shortfall of heating diversions above 25 per cent (first parameter pass, heating 0.62 to 0.86 kWh per
  degree day): too close to the 30 per cent band for convergence across weather readings; heating sensitivity cut to
  0.42 to 0.62.
- Strathspey at 9 heating diversions tied Inverness City at 19 referrals, an ordering fork in the ranked chart; cut to 6.
- First cut of the pack (mart keyed by billing account and described as "the account's metered import", heating-only
  supply numbers listed inline on the Supplies sheet with a `related_mpan` column): the solver's-eye leak reader's plan
  of attack, before any solve, was "screen each MPAN separately, including the related heating-only ones" and "use the
  mart only as a sanity check, since it is per account". The decisive grain was announced by the file layout. The mart
  is now the metering-system table it would be at a supplier, keyed by the primary supply number, and the related
  metering points sit on their own CIS sheet, so the natural pipeline (Supplies sheet plus mart, or plus the reads) is
  keyed by supply number and silent everywhere. The same reader flagged RP-07's revision table (its two lines named the
  own-history degree days and the occupier window) and the DNO loss file ranking Lochaber top, echoing the belief; both
  rewritten.

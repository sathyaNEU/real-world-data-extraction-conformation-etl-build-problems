# Determinism check report, task182 ARCHITECTURE 2 (archived evidence)

**This is architecture 2's verdict, and architecture 2 is spent.** The judge ran on the bundle whose tree
digest was `ab3198a15c906f7b`, cut 2026-10-17, and the build was re-rooted at architecture 3 the same day.
That bundle is superseded: it is still on disk while architecture 3 is designed, because architecture 3
keeps as much of the generator as its new decisive step allows, and it is rebuilt or removed at stage 3.
Nothing below describes architecture 3, whose decisive step is different. The report is kept so that the
next person to read the folder can see why architecture 2 died without taking anyone's word for it.

**What it settles.** The verdict is DETERMINISTIC with a cosmetic SOLUTION_WRONG, and the call was
derived from the 13 files alone: the same five dwellings, the same fourteen levels at one decimal, the
same per-position and per-week plant figures, the same longest runs and the same tone. Gate F was read
LOW to MODERATE with too-easy risk named on the main call. Together with the stage 4 reader, which also
landed the call and both device asks, that is two independent cold threads on the same decisive step, so
architecture 2 is spent: the step the filed clause demands and the data supplies in one move is readable.

**What binds architecture 3, from this report.** Three things, two of which would have shipped.
1. Section 3's rounding finding: the weekly air printed whole where the prompt's rounding sentence asks
   for one decimal, eighteen asked figures wrong on the face of the submission with every gate green,
   because `figures_check.py` asks only whether the block's number is in `figures.json` and both carried
   the same coarse value. Architecture 3 lists the figures the prompt's rounding sentence governs and
   checks each printed precision against it in the verifier.
2. Section 3's unreproduced recommendation sentence: a clause naming what a rejected method would give is
   itself graded. Architecture 3 either recomputes each rejected route the write-up names and names
   exactly the candidates it yields, or writes the sentence without the candidate list.
3. Section 0's residual table is the raw material for architecture 3's decisive step, and section 7's
   ruling that plan 3.1's "in dB LAeq" textually bars an LA90 proxy is the sentence to re-examine: a
   textual bar on the wrong route is the bar doing the analytical work.

---

# Task 182 determinism review (Drumlorne noise, mitigation slot)

Verdict: DETERMINISTIC, SOLUTION_WRONG (cosmetic, three items)
Disposition: FIX_NOW (edit the write-up; no change to prompt or files; no model rerun)

## 0. Answer I derived before checking the graded blocks (disclosure and enumeration)

Disclosure: the brief quoted the graded blocks in the same file, so I had read them before computing. The derivation below was run
from the 13 files only, and every figure was recomputed rather than copied.

Path from prompt plus bundle: pair 28 deployments to positions (meter_deployments); dedupe the repeated download (120 rows, SLM-22043,
NSL09); convert UTC to Europe/Dublin (IST); correct deployments with |mean check - 94.0| > 0.3 by SUBTRACTING the deviation (11 deployments);
drop minutes whose 10-min weather bin (UTC, floor to 10 min) has rain tips > 0 or wind > 5 m/s (km/h / 3.6 from 20 Sep) and minutes at the
-120.2 no-measurement sentinel; weekday 07:00 to 19:00 local; energy-average; residual; energy subtraction; rank.

Options for the one unstated step (how the residual is obtained). Plan 3.1 says only "sound from sources other than the plant ... in dB LAeq":

| Residual option | Top five | 5th minus 6th |
|---|---|---|
| A. LAeq of valid minutes inside the equipment-log windows where BL-01/02/03, CF-01/02 and CHP-01 are all down (six weekly stops, 120 min each, 240 min per position) | NSL04, 11, 07, 02, 13 (6th NSL06) | 1.29 dB |
| B. none (rank on measured level) | 04, 11, 07, 02, 06 (6th NSL13) | 0.48 |
| C. energetic LA90, assessment period | 04, 06, 11, 03, 13 (6th NSL12) | 1.22 |
| D. median LA90, assessment period | 04, 06, 11, 13, 03 | 1.01 |
| E. 10th-percentile LAeq | 04, 11, 06, 07, 02 | 0.75 |
| F. 24 h LA90 variants | 04, 11, 06 plus 13/03/07/02 mixes | 0.01 to 0.76 |
| G. LAeq at night or at weekends | 04, 02/11, 06, 13 ... | various |

My answer is option A: NSL04, NSL11, NSL07, NSL02, NSL13 at 53.0, 49.9, 47.8, 47.3, 46.0 dB, with NSL06 sixth at 44.7 (1.3 behind).
Why A is the only one the shipped text licenses: 3.1 makes the residual an LAeq of non-plant sound. LA90 is not an LAeq, and any
LAeq from a time the plant runs contains the plant. Only the equipment log supplies times when it does not. No stop falls inside
the 07:00 to 19:00 window (the stops end at 06:30 to 07:00), so the residual has to come from outside the assessment period.

## 1. Gate table

| Gate | Result | Line |
|---|---|---|
| A, correct from files | PASS (SOLUTION_WRONG items below) | All four critical components and all 14 levels reproduce. Plant figures reproduce under the stated readings. |
| B, facts in files | PASS | Every decisive input is in a shipped file. The residual method is not written down but is forced by the 3.1 definition plus the equipment log. "Blowers" air needs a counter pair (see C). |
| C, uniquely forced | PASS for the main call; PASS with two flagged inference debts on asks | Main call survives every Layer-1 variant (below). Flags: blower-air counter choice; "no reading of its own" in the weekly counts. |
| D, hardness not semantics | PASS (borderline) | The residual step is method choice pinned by the definition and the log, not a vocabulary lottery. |
| E, prompt pins the decision | PASS | Five dwellings, sixth with margin, tone, six weeks. Units pinned in the sentence. |
| F, stump power | LOW to MODERATE (too_easy risk on the main call) | See section 4. |
| G, stumping type | PASS | method_or_model_selection, FINE numbers. See the line below. |
| H, three rules | PASS, one borderline caveat | See the line below. |

## 2. Reproduction (what I got)

Critical components: NSL04 measured 53.222 (golden 53.2) over 6,130 valid minutes (6,130 reproduces); residual 40.527 over 240 minutes
(40.5); specific 52.982 (53.0); fifth minus sixth 45.969 - 44.682 = 1.287 (1.3). All reproduce.

14 specific levels (mine vs golden): NSL01 43.92/43.9, 02 47.27/47.3, 03 43.64/43.6, 04 52.98/53.0, 05 38.73/38.7, 06 44.68/44.7,
07 47.78/47.8, 08 41.43/41.4, 09 44.03/44.0, 10 37.42/37.4, 11 49.87/49.9, 12 43.32/43.3, 13 45.97/46.0, 14 42.02/42.0. All 14 match.
None sits within 0.01 of a rounding edge; including the 19:00 minute moves nothing at one decimal.

Calibration: 11 deployments corrected (D02, D04, D07, D09, D12, D16, D18, D21, D23, D26, D28). No deployment breaks the 1.0 dB
check-pair limit (max 0.8), so that clause is unused.

Blower air per position: mine 520.5 (NSL01, 02, 04, 05), 506.3 (03), 498.0 (06, 07, 08), 505.7 (09, 10), 511.0 (11, 12), 503.3 (13), 517.5 (14).
All match. Method: for each weekday of the position's two deployment weeks, counter(19:00) - counter(07:00), aeration_header_total_knm3 +
bl03_discharge_total_knm3. Every boundary stamp exists.
Weekly air from plan 5.1 (Monday 00:00 to next Monday 00:00): 689.2, 675.9, 684.7, 687.2, 653.8, 674.9, matching 689, 676, 685, 687, 654, 675.
No counter roll-over affects these counters.

Quarter hours with no own reading, per position: NSL01/02/04/05 20 (run 14); 03 27 (14); 06/07/08 24 (13); 09/10 27 (16); 11/12 24 (16); 13 21 (13);
14 14 (8). All match.
Weekly: 20/14, 16/11, 12/8, 92/86, 18/13, 21/16. All match, but only if the zero-flow repeats inside the six weekly stops are NOT counted
as stale (see fork 2).

Tone (plan 4.3, assessment period, both deployments together, unweighted): 400 Hz excess is NSL02 12.6, NSL03 6.7, NSL04 15.7, NSL07 11.2,
NSL09 9.4, NSL11 13.0. Not prominent: NSL01 3.5, NSL06 1.7, NSL12 3.1, NSL13 2.5. No other band reaches 5 dB. The set is unchanged with or
without the field correction, and under quarter-hour validity screening of any kind. Reproduces.

## 3. Forks enumerated, and figures I could not reproduce

Main call robustness. The top-five set is identical under: no weather screen, rain-only screen, wind >= vs >, no field correction, wind
km/h misread as m/s, 19:00 inclusive. Only the 5th/6th gap moves (0.91 to 1.29). The call turns solely on the residual (table in section 0).

Fork 1, residual method (main call). The shipped text does not say "measure it with the plant off". It is closed by "residual ... in dB LAeq"
(rules out LA90 and percentile proxies) and by the plant-off windows in the equipment log. Any proxy gives a different set (table). I count it
closed by the literal definition, but it is the one inference a hostile portal reader would attack.

Fork 2, "no reading of its own" in the six weekly counts. Naive "row identical to the previous row" also flags the 7 zero-flow rows in each
weekly stop (05:00 to 06:30 etc.). Counts would then be 27/23/18/99/25/28 instead of 20/16/12/92/18/21 (runs unchanged). Counting missing rows
only gives 11/7/5/80/9/13 with runs 11/7/5/80/9/13. The golden excludes stop-window repeats, since zeros against a logged stop are real readings, and
counts repeats of non-zero values after a gap as copies, as the survey notes describe. The per-position figures are unaffected because the stops
end before 07:00. A careful solver reaches the golden by crossing the equipment log, but nothing in the text says to.

Fork 3, "the air the blowers delivered". aeration_header_total_knm3 alone gives weekly 469.8/446.3/452.7/455.4/422.7/443.5 and per-position
about 332 to 357. The golden adds bl03_discharge_total_knm3. File evidence for the sum: on 10/09 and 8/10 BL-01/02 are isolated, the header reads 0
while BL-03's counter keeps advancing, so the header excludes BL-03. No file says so in words. I count it closed by file evidence, flagged as the
weakest link (it moves 20 asked figures by about 40 percent).

Not reproduced or inconsistent:
- Recommendation block: "a background taken from the position's own record ... puts NSL03 and NSL12 in". Under none of my background proxies is
  NSL12 in the five (best case sixth). NSL03 enters under several; NSL06 enters under most and the sentence omits it. The sentence is narrative, not
  graded, but it is unreproduced.
- Deliverable block 4, weekly blower air is given in whole units (689, 676 ...). The prompt says "levels, the margin and air to one decimal", so
  these should be 689.2, 675.9, 684.7, 687.2, 653.8, 674.9. Rounding mismatch with the prompt (solution_wrong, cosmetic).
- Deliverable block 3, "a tone is prominent at 6 of the fourteen positions". Only ten positions have band data (three meters carry the module;
  NSL05, 08, 10, 14 have none, and NSL04 and NSL13 have one deployment each). Should read "6 of the 10 positions with band data".

Other checks that passed: complaints register is correctly demoted by plan 6.1; effluent file and lab as-found values are unused distractors; plan 5.2
(centrifuge runs) and the roll-over clause in 5.1 are unused by this prompt.

## 4. Gate F, stump power

All Layer-1 mess (UTC, duplicates, calibration drift, wind unit change, rain, historian dropouts) can be botched without changing the five. The
main call is decided by one step, getting a residual from the plant-off windows rather than from LA90 or by skipping it. A strong model that
reads plan 3.1 and sees "weekly MCC inspection" stops in the log will likely find it. Expect the main call to be cleared by most strong runs,
with some LA90 or skip-residual failures; the weight sits on the asks (14 exact levels, 6x3 plant figures, tone), where Layer-1 slips and the stale
and BL-03 readings bite. The natural lever, if wanted, is a harder separation of the 5th/6th pair, not more mess.

## 5. Hygiene

PASS. 13 members, formats csv, parquet (281,918 rows), xlsx, pdf, md. Two distractors (complaints, effluent). Manifest row counts match files (258, 7,267,
6,912, 12,047, 28). Dates coherent (plan effective 01/06, PDF created 29 May; survey 31 Aug to 12 Oct, extracts 13 to 16 Oct). No authoring or benchmark
language, no README. Minor: effluent notes repeat two stock phrases; xlsx core properties name a creator (fictional). Not exclusion-level.
No public-data contamination.

## 6. Gate G line

mechanism: method_or_model_selection (residual estimation by plant-off measurement on honest data), with etl_conformance in the asks;
stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no.
No reported number is wrong: measured levels are correct, and the plan and the prompt themselves name the specific-level lens. The complaints
ranking is a declared non-measurement. On perfectly clean data the call would still need the residual step. Borderline note: the flip from measured
to specific ranking could be read as a lens swap, but the prompt ("how much of the sound ... is the plant's") and plan 3.1/7.1 state the lens, so it
does not count as surface-read rejection.

## 7. Gate H line

domain: pass; layers: pass (Layer 1: UTC to local, duplicated download, calibration deviation, wind unit change after 20 Sep, rain and wind screening,
historian dropouts and stale repeats, counter roll-over; Layer 2: residual by plant-off measurement, then energy subtraction to the specific sound
level, ranked for the slot); decisive_step: analytical (borderline-rule_application caveat).
Swap test: replace "dB LAeq / residual / plant-off" with another field's nouns and the task no longer reads the same, so the domain is not a backdrop.
Decisive step: estimating the residual sound with the plant genuinely off. The easy route a strong analyst who read the plan might take is LA90 or a
quiet-period LAeq as "background", or ranking on the measured level; those give NSL06 in and NSL13 out (or NSL03 in), a wrong set.
Caveat: because 3.1 states "less the residual sound", ranking by measured level is a rule-reading failure, and the residual method is left to the
solver. I judge it analytical because the plan fixes the estimand (an LAeq of non-plant sound) and the data supports exactly one way to obtain it,
but a reviewer could call the unstated plant-off method a withheld rule. Not a planted defect: no decoy decides the call.

## 8. Fix

Location: solution (write-up only).
1. Weekly blower air in block 4 to one decimal: 689.2, 675.9, 684.7, 687.2, 653.8, 674.9.
2. Replace "which puts NSL03 and NSL12 in" with a claim that reproduces, or drop it.
3. "6 of the fourteen" to "6 of the 10 positions with band data".
Optional, would need a rerun: file in the prompt that blower air means all three blowers (header plus BL-03 counters), and that a repeated value
is not a reading.

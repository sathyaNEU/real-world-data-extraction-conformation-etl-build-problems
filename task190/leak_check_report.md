# leak check, task190

**Verdict: REVIEW.** 17 files read, 135 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: design, variance, stratum, sample, decisive, asserted, published, correction, register, national, release, sampled, estimand, method, estimate, denominator, estimator, population, finite-population, consignment, enterprise, reference, sentence, strata, survey

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `collection_capacity_note_2027.pdf`: carries 11 of 15 distinctive words of the committed call: 'The 2027 supplementary collection module goes to Metal and metal-bearing wastes, the only stream whose 2026 recovery rat'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `bws_2026_design_and_weighting.pdf`: 10 of 25 stump-paragraph terms appear (design, stratum, sample, register, national, release); read whether the document names the move
- **REVIEW** `collection_capacity_note_2027.pdf`: 10 of 25 stump-paragraph terms appear (sample, register, national, release, sampled, estimate); read whether the document names the move
- **REVIEW** `waste_statistics_2025_release.pdf`: 9 of 25 stump-paragraph terms appear (published, register, national, release, method, estimate); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

One isolated reader, Sonnet at medium effort, on a fresh unzip of the pack and the prompt alone, 2026-10-18.

# task190 reader answers

1. Decisive step stated? Partly. collection_capacity_note_2027.pdf s3: "A stream is established below target where its 2026 recovery rate is below its National Waste Management Plan 2024-2030 target at the 95 per cent level. The module goes to the one stream so established." It states the test, not the variance method.
2. Ranks/scores candidates: none. waste_statistics_2025_release.pdf ranks 2025 rates, a prior year and not the 2026 question.
3. Exists only to help the analyst: treatment_operation_codes.xlsx (operation_kind recovery/interim/disposal, "An interim operation is storage pending a later operation; the later operation is confirmed on the consignment the holding site forwards."), and waste_code_crosswalk.csv. Distractor-like: carrier_permit_vehicle_log_2026.csv, hazardous_export_notifications_2026.csv, bws_2026_response_log.csv (only for asks).
4. Reads as the answer: none by name. Closest: the capacity note's "committed to the one stream where the 2026 attainment figures establish a shortfall", which says exactly one stream qualifies.
5. Filed sentence fixing the figure: collection_capacity_note_2027.pdf s3: "the tonnage of that stream despatched by its producer during the 2026 calendar year and confirmed received at a recovery operation, counted once at the producer's despatch leg, over the total tonnage of that stream arising during 2026 at every enterprise in the Business Waste Survey frame whether sampled or not, as estimated from the 2026 survey." Literal result for metal: 70,384 t / 124,354 t = 56.6%. Target 59.5, shortfall 2.9 points.
6. Decider: an analytical choice, plus following the stated definition. The definition fixes the numerator and denominator. What flips the call is the interval: the stratified, finite-population-corrected standard error of the weighted survey total for each stream, with the register tonnage treated as a census. The pack's only precision figure, in waste_statistics_2025_release.pdf ("coefficient of variation of the estimated national total of business waste arising is 3.9 per cent"), is for the total and not for the stream. Applying it to a stream would make metal non-significant. Sentence: bws_2026_design_and_weighting.pdf s2 (E1 completely enumerated, weight 1.0), which makes metal's interval narrow. Also needed: following R13 interim to the forwarded consignment (xlsx notes), and ignoring the stream-level point-estimate ranking (mixed C&I is 4.9 below target but z about -1.45, not established).

## Solver route and answer
Answer: Metal and metal-bearing wastes. 2026 rate 56.6% (SE about 0.63 pts, 95% interval about 55.4 to 57.8) against 59.5%, shortfall 2.9 points. The module goes to metal. Confidence about 75%.
Route:
- Stacked the three legs into one table. The h2 file has renamed columns, handled positionally; no consignment overlaps between files, and the 2025 file holds early-2026 despatches, so I filtered on leg_date.
- Mapped waste codes via the crosswalk, which covers the 2026-07-01 starred codes.
- Took enterprise-origin despatches (producer APA-3...) dated in 2026 and dropped any with a parent (re-submissions of the same load; none in 2026).
- Recovery means R1/R3/R4/R5 on the treatment-confirmed leg. R13 follows the forwarded consignment (parent_consignment, producer APA-F...) to its later operation. 730 despatches have no confirmation and count as not recovered.
- Denominator: stratified weighted survey totals. Variance uses (1-f) and s^2 within stratum, with the register numerator treated as fixed.
- Metal: recovered 70,384 t of 124,354 t arisings. Mixed C&I 59.6 vs 64.5, z -1.45. Paper, wood, C&D, glass, plastic and textile are all insignificant. Only metal is below target at 95%.
- Naive route (not following R13 chains) gives rates around 40% for metal, so every stream looks short. Mixed C&I then looks worst, which is the wrong answer.
- Uncertainty: the variance method, whether nonresponse (E2 206 eligible vs 195 usable) is adjusted, and the one-sided versus two-sided test. Metal is z -4.6, so it is robust to those.
Asks not worked fully. Visible hazards: the response log mixes d and h units (7.76 h in 71 rows), the municipal returns mix t and 100kg, and the 2025 tonnage needs dedup of the 43 re-submissions plus chain-following.

## Exercise-feel
- collection_capacity_note_2027.pdf s2: "it is committed to the one stream where the 2026 attainment figures establish a shortfall" and s3 "The module goes to the one stream so established." The document announces a single answer and defines the quantity line by line, more like a spec than a memo. s3 is a one-sentence estimand, which reads as written for the task.
- Same note s5: "The core-round figures are the 2027 plan, not the 2026 outturn; the 2026 outturn is in the collection operations log." This is a warning planted for the field-days ask.
- bws_2026_design_and_weighting.pdf s2: "the 2026 round closed with a return from each of them." and s4 "no region", which pre-empts questions the analyst would ask.
- waste_statistics_2025_release.pdf: the CV of the national total (3.9 per cent) next to "the statistical stream breakdown is published without them" reads as a bait for the wrong interval.
- Facility names such as "Unidade 1 de Norte", carrier "Transportes 1" and facility permits APA-F70001... are sequential and synthetic.
- Movement data: every chain has the same 1-day receipt and 2-3 day confirmation lag (std 0), and all legs have integer tonnes, which is too regular for a register.

### The main thread's ruling, line by line

- **Question 1, no leak.** The capacity note's bar fixes the test and the reader says so explicitly: it does not
  fix how the interval is built. The method is not named anywhere in the pack.
- **Question 2 and 3.** No file ranks the streams on the 2026 question. The crosswalk and the operation-code
  notes are the resolution chain the estimand needs, not help: without them the numerator cannot be built at
  all. The two files the reader calls distractor-like are the two declared distractors.
- **Question 5, the quoted sentence executes to the golden.** 70,384 over 124,354 is 56.6 per cent, which is the
  committed figure, so the literal reading is the golden and not the easy answer.
- **Question 6 and the solver answer: this is the finding, and it is Gate F rather than a leak.** The reader
  reached rung 4 directly, with the finite-population correction and the register numerator held fixed, and
  named the golden at about 75 per cent confidence. Rungs 1 to 3 were skipped. Computing a design-based
  variance is the opponent's reflex for a survey quantity, and the frame and strata have to ship because the
  estimand names them, so the architecture cannot be hardened by withholding them.
- **The hardening route is the reader's own residual**: the E2 stratum's nonresponse, 206 eligible against 195
  usable. If reweighting inside the stratum moves the estimate and its variance enough to change which stream
  is established, the decisive step sits one level below the reader's route and rung 4 becomes a rung.
- **Realism, all four to be fixed in the generator in the same pass:** receipt always exactly one day after
  despatch and confirmation two to three days after; every tonnage an integer; facility and carrier names
  running sequentially; and the capacity note reading as a specification rather than as a memo.

### What the repair pass of 2026-10-18 changed under this report

The four realism defects are repaired in the generator and asserted in `checks.py` block J. The reader's
quotations of the 2025 release's "3.9 per cent" and of the capacity note's numbered sections describe the
judged pack: the release now publishes the 2025 round's own coefficient of variation (3.4 per cent), which no
estimator of the 2026 round reproduces, and the capacity note is a memo. The reader's route, its 75 per cent
confidence and the Gate F question above are unchanged and still open: a fresh reader after this pass is the
test the orchestrator is holding it for.

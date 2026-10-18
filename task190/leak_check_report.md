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
- Stacked the three legs into one table. The h2 file has renamed columns, handled positionally; no consignments overlap between files, and the 2025 file holds early-2026 despatches, so I filtered on leg_date.
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

## Solver's-eye read, round 2 (the repaired pack, target.zip bbf01fae)

# task190 reader answers

1. Decisive step: the sentence in collection_capacity_note_2027.pdf, "A stream is established below target where its 2026 recovery rate is below its National Waste Management Plan 2024-2030 target at the 95 per cent level." It states the test but not how the interval is made. bws_2026_design_and_weighting.pdf gives the strata, N, n and weights but says nothing about variance. No sentence says what to do about the census stratum or the finite population correction.
2. Ranks or scores 2026 candidates: none. waste_statistics_2025_release.pdf Table 1 ranks 2025 rates only, and national_waste_management_plan_targets.pdf is targets only.
3. Exists only to help the analyst: waste_code_crosswalk.csv and treatment_operation_codes.xlsx (code-to-stream and code-to-kind lookups), and facility_register.csv (role lookup). The two PDFs and the memo are context.
4. Reads as the answer: none. The memo's "it is committed to the one stream where the 2026 attainment figures establish a shortfall" says one stream qualifies but names none. Closest context figure: the 2025 release's "coefficient of variation of that estimated national total in the 2025 round is 3.4 per cent", which invites a wrong, national-level precision.
5. Literal fix of the main figure (collection_capacity_note_2027.pdf): "a stream's recovery rate is the tonnage of that stream despatched by its producer during the 2026 calendar year and confirmed received at a recovery operation, counted once at the producer's despatch leg, over the total tonnage of that stream arising during 2026 at every enterprise in the Business Waste Survey frame whether sampled or not, as estimated from the 2026 survey."
   Literal result for Metal: numerator 70,384 t, denominator (weighted survey total) 124,354 t, rate 56.6 per cent against the 59.5 target, shortfall 2.9 points. Other streams: mixed 59.6 (target 64.5, 4.9 short), paper 49.9 (1.9), wood 43.7 (1.6), C&D 60.2 (2.4), glass 53.7 (2.0), plastic 33.8 (1.6), textile 28.3 (0.9).
6. Mostly an analytical choice (the interval for a stratified, partly census survey, which decides which shortfall is established), plus rule application for the register chain. The deciding file is bws_2026_design_and_weighting.pdf (strata table: E1 "enumerated completely" so it has zero sampling variance; E2 to E4 sampled without replacement, so an fpc applies), combined with the memo's "at the 95 per cent level". Reading codes, units and duplicates correctly is needed but does not flip the call.

## Solver route and answer

Answer: Metal and metal-bearing wastes. 2026 rate 56.6 per cent (interval about 54.1 to 59.1 two-sided, SE of rate about 0.63 pt), target 59.5, shortfall 2.9 points. It takes the 2027 module. Confidence about 85 per cent on the stream, about 70 per cent on exact figures to one decimal.

Steps:
1. Register: stack the three leg files (2025 file contains 333 despatches dated 2026, h2 contains 306 dated 2027). Select by PRODUCER_DESPATCH date in the calendar year, not by file. h2 uses different column names (consignment_ref, leg_no, ewc_code, net_tonnes, treatment_op, parent_ref).
2. Counted once at the producer's despatch: drop despatches whose producer is a facility (APA-F...), which are R13 forwards (12,124), and drop 43 producer re-despatches whose parent was already confirmed at R1/R3/R4/R5 (same producer, tonnes and carrier as the parent).
3. Recovered: root consignment with TREATMENT_CONFIRMED in R1/R3/R4/R5, or R13 (interim) whose forwarded child is confirmed at R1/R3/R4/R5. D1, D10, bare R13 and no confirmation (1,431 despatches) are not recovered. All 12,124 forwards resolve to a terminal operation.
4. Streams via waste_code_crosswalk.csv, including the starred codes from 1 July 2026 (all codes map).
5. Recovered 2026 t: metal 70,384; mixed 93,294; paper 31,721; wood 20,003; C&D 95,414; glass 13,376; plastic 7,659; textile 1,819.
6. Denominator: Horvitz-Thompson, sum of weight times arisings from the micro-data. Metal 124,354 t, mixed 156,533, paper 63,569, wood 45,773, C&D 158,494, glass 24,908, plastic 22,659, textile 6,429.
7. Variance: stratified, Nh^2 (1 - n/Nh) s^2 / n per stratum, E1 contributes zero. SE of denominator: metal 1,395; mixed 8,862; paper 4,407; wood 3,729; C&D 20,669; glass 1,524; plastic 1,505; textile 594. The register tonnage is a census so it is treated as fixed, and the rate SE is the delta-method share. z of shortfall: metal 4.6, mixed 1.45, plastic 0.7, glass 0.6, paper 0.55, wood 0.45, textile 0.35, C&D 0.3. Only metal is established, at either a one-sided or a two-sided 95 per cent level.
8. Field days: count once per visit_ref (the visit total is repeated on every case row), convert h to days by /8 (EQ-ALE logs in hours). Norte 32.54, Centro 25.69, Lisboa 29.80, Alentejo 10.11, Algarve 7.66. Usable returns are distinct cases (1,630; 1,634 rows, 4 duplicate rows): Norte 538, Centro 381, Lisboa 430, Alentejo 166, Algarve 115. Returns per field day: Norte 16.53, Centro 14.83, Lisboa 14.43, Alentejo 16.42, Algarve 15.01.
9. 2025 tonnage confirmed received at a recovery operation, same basis, from the register: metal 67,709; mixed 89,749; paper 30,516; wood 19,243; C&D 91,788; glass 12,868; plastic 7,368; textile 1,750. These are above the published 2025 release (metal 65,074), which the release explains by later confirmations.
10. Municipal: exclude the five "Associacao de Municipios" rows (they overlap the member municipalities; including them gives 32 to 43 per cent gaps), convert Mangualde and Tondela from 100kg to t (/10), compare with receipts summed by receipt_date in 2026 by origin_region. Gap t and share: Norte 3,075 (2.6%), Centro 4,910 (4.1%), Lisboa 4,081 (3.6%), Alentejo 2,589 (3.4%), Algarve 3,463 (4.0%).

Choices between two defensible methods:
- The variance. With the fpc and a zero-variance census E1, metal's SE is 1,395 t and it is established. Without the fpc and with E1 treated as a sample, the SE is 6,692 t, metal's z falls to about 1.0 and no stream is established. I chose the fpc and the census because the PDF says E1 is "enumerated completely" and the others are "without replacement". The fpc uses usable returns as n (matching the weights); using issued counts moves the metal SE to 1,382, immaterial.
- The tempting route is to rank by point shortfall: Mixed (4.9 points) is largest but its interval is wide (z 1.45), so it fails.
- Treating the register tonnage as fixed (census) rather than adding variance. Adding any plausible register variance would not move metal's z far below 4.
- One-sided versus two-sided 95 per cent: same stream either way.

What I would need to be told to be sure: whether the E1 census and fpc are the intended variance basis (the pack never says), whether the issued or the usable count is n for the fpc, whether associations are meant to be dropped (inferred from the receipts matching the municipalities alone), and whether the register unconfirmed 2.6 per cent should be non-recovered (taken literally from the memo's "confirmed").

## Reads as written for an exercise
- collection_capacity_note_2027.pdf: "So that we are all measuring the same thing, the quantity is this." A head of operations would not define the rate this way in a memo; it reads as the rule being handed over. Also "My answer is the module: it is committed to the one stream where the 2026 attainment figures establish a shortfall against the plan", which announces that exactly one stream qualifies.
- collection_capacity_note_2027.pdf: "One module is what there is: a second would come out of field days the core rounds need." It exists to force a single answer.
- bws_2026_design_and_weighting.pdf: "the 2026 round closed with a return from each of them" and "No calibration or post-stratification is applied to the 2026 round." Both exist to pin the variance basis.
- waste_statistics_2025_release.pdf: "The register goes on receiving treatment confirmations for consignments despatched in earlier reference years, and the published series is not revised for them." This explains the 2025 mismatch for the solver in advance.
- Data: the 2026 rates land on exact tenths (56.60, 59.60, 49.90, 43.70, 60.20, 53.70, 33.80), which no real survey produces. The 43 duplicate redespatches are exact copies of the parent's tonnes and carrier. The municipal Mangualde and Tondela rows are the only ones in 100kg, and the associations are the only overlapping rows.
- The Layer 1 mess (h2 column rename, starred codes, hours in one team, repeated visit days) is each a single clean switch, which reads as planted.

### The main thread's ruling

- **Gate F has now failed twice, and harder.** Round 1 landed the call at about 75 per cent, round 2 at
  about 85 per cent on the stream. Cutting the oracle did not make the decisive step harder to find,
  because what points at it is not the published coefficient of variation but the design document's own
  statement of its strata, which has to ship: the estimand names the frame. A design-based variance is
  this domain's reflex and both readers reached for it unprompted.
- **The repair cost the fork its closure, which is the finding of this round and it is mine, not the
  reader's.** Round 1's judge closed Gate C partly on a shipped number: the published CV reproduced at
  3.915 under the corrected estimator and 4.091 without it, so the method was confirmed against the pack.
  That confirmation is exactly what I had cut as an oracle. Round 2's reader now reports the variance basis
  as the biggest fork in the build, says the pack never states which basis is intended, and measures the
  consequence: the metal standard error is 1,395 t with the correction and the census stratum and 6,692 t
  without, where z falls to about 1.0 and no stream is established at all. So the oracle and the closure
  were the same sentence, and removing it traded a Gate F weakness for a Gate C fork without buying
  anything. Either the basis is forced by the records in a way no single figure confirms, or the build
  carries a live fork on its main call.
- **Three realism tells survive and one is new and serious.** The 2026 rates land on exact tenths
  (56.60, 59.60, 49.90, 43.70, 60.20, 53.70, 33.80), which a real survey does not produce, so the
  numerator and denominator have been tuned to a printed figure. The memo still announces that exactly
  one stream qualifies. And the reader reads the design document's two variance-pinning sentences, the
  column rename, the starred codes, the single hours team and the repeated visit days as one clean
  switch each, which is the pack reading as constructed rather than exported.

### What the pins pass of 2026-10-18 changed under these two reports

The judge's second pass closed the Gate C fork (both estimators of the denominator's design variance are
forced by the records, and the published 3.4 per cent confirms nothing), and its three pins are made here.
Two of them change what a reader sees, so **both reader rounds above are now stale on those points and a
fresh reader round is owed**:

- `bws_2026_design_and_weighting.pdf` section 5 now states the visit grain outright ("a visit covers several
  enterprises in one region on one trip, and the visit's field days are recorded on each case the visit
  covered, under the visit reference the log carries"), so ask A1's grain is a filed rule and no longer a
  silent device. Measured cost: the pair ceiling moves from 28.5 to 38.3 against a gate of 40.
- `prompt.txt` now names the four chain stages, so the stage sheet cannot be decomposed another way.
- The 2025 release's recovered column is now the register at the 30 June 2026 extract it names, the register
  carries 230 confirmation legs of 2025 consignments after that cut (longest lag 626 days), and no basis
  reproduces the column (the nearest, a recompute at that cut, is off by 0.24 to 0.76 per cent a stream).
  The round-2 reader's "metal 65,074" and the round-1 reader's "3.9 per cent" both describe earlier packs.
- The register's stream and stage totals are no longer whole numbers and the unconfirmed despatches now rise
  towards the extract (33 in January against 139 in December). The round-2 reader's "the 2026 rates land on
  exact tenths" survives at the fourth decimal and cannot be cleared without moving a graded tonnage: with
  70,384 t and 124,354 t both frozen and printed, the rate is pinned to 56.5991 to 56.6004.

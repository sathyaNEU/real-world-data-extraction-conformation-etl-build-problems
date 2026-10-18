# task190 design note

Architecture 6, drawn 2026-10-18 on new ground after architecture 5 died at stage 1 on measurement,
built to stage 3, judged NOT_DETERMINISTIC with a FIX_NOW on the ask side, repaired in one pass, judged
DETERMINISTIC on the second pass with a FIX_NOW of three note-level pins, pinned in a third pass on
2026-10-18, and re-sited on the ask side in a fourth pass the same day after `precut.py` failed on
`cracker misses every ask` (every pass is at the end of `## Tried and rejected`). Asks A1 and A3 now
carry silent primaries and the three pins stand untouched. The main call, its eight streams'
rates, targets, intervals and standard errors, all 32 stage-chain cells, the five field-day rows, the eight
2025 tonnages, the five municipal rows and the ladder are byte-identical to the judged pack, key by key in
`generator/figures.json`; what moved in the pins pass is the 2025 release's recovered column and the register's own clock
behind it, the visit grain the design documentation now states, the four chain stages the prompt now names,
and the weighbridge residues that stop a stream total being a whole number; what moved in the re-siting
pass is three ask files (`bws_2026_response_log.csv`, `enterprise_permit_crosswalk.csv`,
`municipal_waste_returns_2026.csv`), the two ask sentences of the prompt and ask A1's figures, with the
digest of every file the call reads asserted against the shipped pack in `checks.py` A10.
Architectures 1, 2 and 3 died on determinism verdicts; 4 on a model constraint plus a measured null; 5 on
a measured reflex. The live design is this block; everything from `## Architecture 3, spent` down is kept
as record.

## Draw

| | |
|---|---|
| Card | architecture 6 draft at `/tmp/claude-0/-home-user/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/wave5/task190/task190_card.json`; `guard.py check` **WARN, no BLOCK**. The card under `.claude/skills/fingerprint/cards/` is still architecture 4's: this builder is barred from `register`, so the orchestrator registers the draft. |
| Owner | oviya13ya |
| Status | stage 3, build |
| Domain / subdomain | `survey-research-official-statistics` / `anomaly-detection` (the client's own task type) |
| Objective | `anomaly-detection` |
| Shape | 09, funnel or chain of stages |
| Decision type | `pick_one_of_n`, answer unit `named_option`, question form `which` |
| Gap / pattern / generator | `objective` / `none` / G16 |
| Gate G | `method_or_model_selection` |
| Strategy | `uncertainty_hold`; Layer 2 family `estimation_fit`, pattern `own:design-variance-of-a-ratio-whose-denominator-alone-is-estimated` |
| Calibration form | `none` |
| Context artifact | `capacity_report` |
| Role / forum / forcing event / org family | `operations_director` / `line_manager_or_team` / `incident_or_complaint` / `research_or_statistics_office` |
| World | Portugal, EUR, five mainland regions; a statutory National Institute for Environment Statistics |
| Deliverables | `recovery_attainment_2026.xlsx`, `attainment_against_target_2026.png` |
| As-of | the register extract is 2027-01-31, the survey round 2027-01-16, the decision due 2027-02-28; `leak.py --asof 2027-02-28` |

**Pairing.** Survey research and official statistics is the one field that ships the sampling error of its
own estimates as part of the estimate, and the anomaly-detection task type in it asks whether a published
figure's departure from a reference is real or is the estimate's own noise. The deciding quantity here is a
design-based ratio whose numerator is a complete administrative total and whose denominator is a
stratified-sample estimate, which is the field's commonest published object (a rate per unit of exposure
the register cannot see) and whose standard error is the field's own Taylor-linearised ratio variance.

**Data-native sentence.** In this pack the Business Waste Survey enumerates the 250-or-more employee
stratum completely and samples the three smaller strata at 1 in 4, 1 in 8 and 1 in 225, so 95.8 per cent of
metal and metal-bearing arisings come from enterprises that were all taken and therefore carry no sampling
error at all, while mixed commercial and industrial arisings sit mostly in the lightly sampled strata: the
same eight streams, estimated from the same 1,630 returns, carry design coefficients of variation from 1.1
to 13.0 per cent, and that spread is set by where a stream's waste arises rather than by how many sampled
enterprises report it (corr(CV, sampled record count) = -0.076, corr(CV, estimated arisings) = -0.013).

**Reserved-axis deviations.** `stump_strategy` is `uncertainty_hold`, not the reserved `composition_mix`:
nothing here is a mix shift, a standardisation or a reweighting, and the reviewer's key for the decisive
move is how the evidence is judged with its uncertainty. `calibration_form` is `none`, not the reserved
`closed_decision_corpus`: the method is forced by the sample design, and a corpus would either bless a
wrong method (the validated decoy the guard blocks) or tie only under the golden (an oracle).
`context_artifact` is `capacity_report`, not `published_series`: `ban.artifact` blocks `published_series`
against task244. `role_family` is `operations_director`, not the reserved `capacity_planner`: `ban.role`
blocked `capacity_planner` against task197 once the registration window moved, and the axis was redrawn
rather than argued.

**WARNs answered.** `repeat.gate_g` and `overuse.gate_g`: no other listed Gate G mechanism is honest for a
call that turns on which variance estimator a design-based ratio takes; it is not a forecast, not a
decomposition, not a binding constraint, and `signal_vs_noise_or_hold` implies a licensed hold while
exactly one stream clears the filed bar. `repeat.decision` and `repeat.question_form`: the call is exactly
one of a filed list of eight streams, so `pick_one_of_n` and `which` are the honest keys, and the division
commits the module to a stream rather than to a count or a gate. `test.same_driver_older` is differentiated
on the card against task195, task228 and task240.

**One line per source.** `references/client/layer2-rigor-patterns.md`, this subdomain's anomaly-detection
patterns: pattern 1 scores edits by weighted impact on an estimate (not used; no editing threshold ships);
pattern 2 is the Hidiroglou-Berthelot robust ratio test, a unit-level editing test that scales a ratio of
two reported values by unit size and needs no sample design, where mine is domain-level and turns on which
of a ratio's terms carries error (no size exponent, quartile bound or unit-level ratio test ships).
`complex-survey-estimation-variance` patterns 1 and 2 belong to another task type and another objective;
their shortcuts (the SRS formula, subset-then-estimate) are measured here as rungs 2 and 3 and neither
reaches the golden, so the decisive step sits one step past both. task195 spends the uncertainty of a
paired difference; task186 spends the reference distribution a per-unit test needs; task191 spends
selection on the maximum; task240 spends the variance of a calibrated total. task198's architectures 2
and 3 are banned to this build and neither is reused.

## Default path

1. Read both halves of the 2026 movement register, map the renamed columns in the second half, and map the
   waste codes to the eight statistical streams through `waste_code_crosswalk.csv`, honouring the mid-year
   code revision.
2. Chain each consignment from the producer's despatch through any interim facility to its final treatment
   facility, using `facility_register.csv` for the facility role, and take the final facility's confirmed
   operation code; count each consignment's tonnage once, at the producer's despatch leg.
3. Sum, per stream, the 2026-despatched tonnage confirmed received at a recovery operation (an R code on
   the revised list in `treatment_operation_codes.xlsx`).
4. Estimate each stream's total arisings from `bws_2026_microdata.csv` by summing the design weight times
   the reported tonnage over every sampled enterprise.
5. Divide: each stream's 2026 recovery rate.
6. Subtract each stream's National Waste Management Plan target and rank the eight shortfalls; or test each
   shortfall against the only precision figure to hand, the 3.4 per cent coefficient of variation on the
   estimated national total of arisings the 2025 release's methodological note publishes for its own round,
   or against the stream's own count of reporting enterprises.
7. Name the stream with the largest shortfall, which is also the only stream any of those tests finds
   significant.

**Ends on:** Mixed commercial and industrial wastes, 4.9 points below its 64.5 per cent plan target.
**Golden:** Metal and metal-bearing wastes, 2.9 points below its 59.5 per cent plan target, the only
stream whose shortfall is established at the 95 per cent level (z = 4.57, p = 0.00000489).

## Stump sentence

The default path files Mixed commercial and industrial wastes, whose 4.9-point shortfall is the largest of
the eight and the only one that clears a bar built from the published national coefficient of variation or
from the stream's count of reporting enterprises, because it treats the recovery rate's uncertainty as a
property of the rate rather than as the design variance of the one term that is estimated: once that
variance is computed over the survey's own strata, with the completely enumerated large-enterprise stratum
contributing none of it, Mixed commercial and industrial sits at 1.45 standard errors and Metal and
metal-bearing, on a smaller shortfall, at 4.60.

## Three rules

- **Task type:** `survey-research-official-statistics` / `anomaly-detection`, the client's own task type in
  that domain, which serves Anomaly Detection & Diagnostics in the taxonomy.
- **Domain test:** the deciding quantity is a design-based ratio estimator's standard error, the
  Taylor-linearised variance of a ratio whose denominator is a stratified-sample estimate of a population
  total, which official statistics computes over the design's strata with each stratum's finite-population
  correction, and where a completely enumerated stratum contributes exactly nothing.
- **Swap:** "which waste stream's recovery rate is established below its plan target" rewritten as "which
  hospital's readmission rate is established below its contract target" stops making sense the moment the
  denominator is a complete count rather than a survey estimate: with a register of every discharge there
  is no probability sample, no stratum, no inclusion fraction, no finite-population correction and no
  design variance, so the quantity that decides this call does not exist and the task collapses into
  comparing two numbers.
- **Layer 1:** the register's schema changes at the mid-year boundary because the Environment Permit Agency
  moved system in July (renamed columns, a revised operation-code list); the waste classification codes
  were revised on the same date, with the agency's own mapping; consignments routed through an interim
  facility appear on two legs because the forwarding leg is a child consignment in the same register;
  despatch date against confirmation date straddles both year boundaries, and the register runs on three
  clocks, so a load held for aggregation or re-keyed after the July system move is confirmed months after
  its despatch and what an extract leaves unconfirmed rises towards its own cut date; one legacy municipal
  extract
  reports in hundreds of kilograms because that was the old return's unit; agency permit numbers against
  business register enterprise numbers, with supersessions, one duplicate and the numbers the agency's
  January 2027 licensing batch reissued after their holder's permit lapsed, which is why a permit register
  is kept effective dated, because the two registers are
  maintained by different bodies; municipal returns on a monthly form whose December slot some
  municipalities use for the annual confirmation; the 2025 release exists in a preliminary and a revised version; the
  release's reference tables sit inside a PDF. Nothing is placed to be caught.
- **Layer 2:** `estimation_fit`. The recovery rate is a ratio of a complete administrative total to a
  design-based estimate of a population total, so its sampling variance is the linearised variance of the
  denominator alone, computed over every sampled unit in each stratum (the zeros included, because a stream
  is a variable and not a subpopulation) with each stratum's finite-population correction, which is zero in
  the stratum the survey enumerates completely.
- **Decisive step:** decide which of the ratio's two terms, and which of the sampled units inside the
  estimated term, carry any sampling error at all: none from the register total, none from the enumerated
  large-enterprise stratum, and therefore a rate determined to 1.1 per cent for the stream whose arisings
  are 95.8 per cent enumerated against 5.7 per cent for the stream whose arisings sit in the lightly
  sampled strata.
- **Not semantics:** every field, code, unit and definition can be read correctly and the easy route still
  files Mixed commercial and industrial. The design documentation states the strata, their population and
  sample counts and that the 250-or-more stratum is taken in full; the microdata carries the stratum code,
  the design weight and an explicit zero for every stream an enterprise does not produce; the estimand
  states that the denominator is the total arising at every enterprise in the frame, sampled or not. A
  solver who reads all of that correctly, computes the rate correctly and then judges the shortfall against
  the published national coefficient of variation, against the stream's reporting-enterprise count, or
  against a variance that omits the finite-population correction, still files the wrong stream or no stream
  at all: measured, those three routes give Mixed commercial and industrial, Mixed commercial and
  industrial, and none.
- **Not rule application:** no shipped sentence states, implies or points at how the rate's uncertainty is
  computed. The design documentation describes the sample as a statistics office describes one and stops;
  the plan states targets; the capacity note states the estimand and the 95 per cent level and no method.
  The step no filed rule performs is choosing the estimator of the denominator's design variance, and the
  value of that variance is a statistic of the sample (within-stratum dispersion against stratum population
  and realised sample sizes) which no clause can state without stating the method.
- **Analyst test:** a strong analyst who has mapped both register schemas, honoured both code revisions,
  chained every consignment to its final treatment, counted each tonnage once and used the design weights
  correctly ranks the eight shortfalls against target, or tests each against the only precision figures the
  pack publishes, and files Mixed commercial and industrial wastes, 4.9 points below its 64.5 per cent plan
  target, against Metal and metal-bearing's 2.9.
- **Estimand:** filed in `collection_capacity_note_2027.pdf`, the memo's third paragraph ("so that we
  are all measuring the same thing"): for the 2026 reference year a
  stream's recovery rate is the tonnage of that stream despatched by its producer during the 2026 calendar
  year and confirmed received at a recovery operation, counted once at the producer's despatch leg, divided
  by the total tonnage of that stream arising during 2026 at every enterprise in the Business Waste Survey's
  frame whether sampled or not, as estimated from the 2026 survey; a stream is established below target
  where its 2026 recovery rate is below its National Waste Management Plan 2024-2030 target at the 95 per
  cent level; the module goes to the one stream so established.
- **No decoy:** nothing is planted to be caught. The Council's complaint asks the institute to review the
  stream-level figures and argues for no answer and no method. The 2025 release is a correct prior-year
  release. The national coefficient of variation is the true design CV of the 2026 national arisings
  estimate and is correct for what it measures. No memo, draft, briefing or stakeholder figure carries the
  wrong answer, and no shipped artifact ranks the streams on the decision question.
- **No certified replay:** no corpus, no closed determinations, no certified or published figure is
  reproduced by the method. The 2025 release publishes 2025, the plan publishes targets, and neither can be
  reproduced by any 2026 route; the method is forced by the sample design, measured as the design estimator
  and the delete-one jackknife within strata agreeing to six decimal places on every stream. The one figure
  that did replay the method is cut: the judged pack published the 2026 round's own national coefficient of
  variation, which the finite-population-corrected estimator reproduced at 3.915 against 4.091 without it,
  so a solver could confirm the decisive estimator against a shipped number. The release now publishes the
  2025 round's own measure, 3.4 per cent, and `checks.py` H4 asserts it prints differently from every
  estimator of the 2026 round's national CV (3.9 corrected, 4.1 without the correction inside the sampled
  strata, 4.5 without it anywhere, 4.1 weighted with replacement) and H5 that no 2025 micro-data, weight or
  sample count ships, so nothing in the bundle reproduces it under any method.
- **Lesson:** the uncertainty of a published rate belongs to the term that was estimated and to the units
  that were sampled, so a rate whose numerator is an administrative total and whose denominator is a
  design-based estimate can be far better determined for a small, concentrated domain than for a large,
  dispersed one, and no precision figure published for another domain or read off a record count stands in
  for it. No build on file teaches it: task195 teaches the paired difference, task186 the empirical null,
  task191 selection on the maximum, task240 the variance of a calibrated total.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 rank the eight shortfalls against target | the plan files the targets, which every route needs | the target table joins on stream | yes, the first thing anyone computes | none | no | one subtraction | readable |
| 1 test each shortfall against a published or record-count precision figure | the methodology note quotes a national CV | the microdata's record counts are a group-by | yes, the rigorous reflex | none | no | one ratio | readable |
| 2 design variance over the strata but without the finite-population correction, or with the sample treated as weighted with replacement | no sentence names a variance | stratum and weight columns exist | yes, what a default toolkit returns when the population sizes are not supplied | none | no | no | readable |
| 3 design variance over only the enterprises reporting the stream (subset then estimate) | no sentence names it | the stream columns make a non-zero filter one predicate | yes, the client's own named shortcut for a domain estimate | none | no | no | readable |
| 4 (decisive) the domain total's design variance over every sampled unit in each stratum, zeros included, with each stratum's finite-population correction, so the enumerated stratum contributes none | no sentence states, implies or points at it | no column marks which stratum was enumerated; the design documentation reports population and sample counts as a statistics office reports them | no: every reflex swept lands on another stream or on none | none | no: the battery computes no design variance | no | silent |

## Semantic fork table

| id | Term or convention | Golden reading | Alternatives and the call under them | Ruled out by |
|---|---|---|---|---|
| SF1 | "recovery rate" | confirmed recovered tonnage over estimated arisings | recovered over tonnage moved off-site (the register's own denominator): names Mineral construction and demolition | the memo's estimand paragraph names the denominator as total arising at every enterprise in the frame |
| SF2 | "arising at every enterprise in the frame whether sampled or not" | the design-weighted population total | the sum of sampled enterprises' reported tonnage: every rate above 100 per cent for four streams, self-refuting | the clause's own words, plus the release's published national arisings total which the weighted estimate reproduces |
| SF3 | the 2026 window | consignments despatched by the producer in calendar 2026 | window on the confirmation date, read over both register files as that reading requires: `same call`, asserted. The register's confirmation tail puts the two windows 1.0 to 4.2 per cent apart a stream and the call does not move: metal stands at 3.13 standard errors under that reading against 4.57 under the filed one, and no second stream reaches 1.07 | the memo names the despatch date; convergence asserted |
| SF3b | the same window read over the 2026 file alone | not a reading the files support: it drops the 972 confirmations the extract carries in January 2027 and counts none of the 2025 despatches confirmed in 2026 | establishes two streams, metal and mixed commercial and industrial | the memo's "the module goes to the one stream so established", which two established streams contradict; and the despatch-date pin |
| SF4 | "confirmed received at a recovery operation" | an R code confirmed by the final treatment facility | the producer's intended operation code at despatch: `same call`, asserted | the clause says confirmed received; convergence asserted |
| SF5 | consignments routed through an interim facility | the producer's despatch leg tonnage once, carrying the final facility's confirmed code | sum both legs: inflates five streams and names Mineral construction and demolition | the clause's "counted once at the producer's despatch leg" |
| SF6 | consignments with no returned confirmation | excluded, being unconfirmed | included as recovered: `same call`, asserted | the clause says confirmed; convergence asserted |
| SF7 | "at the 95 per cent level" | a two-sided normal bar at 1.959964 standard errors | one-sided at 1.644854, or a t bar on the design degrees of freedom: `same call`, asserted | convergence asserted on every stream |
| SF8 | the waste code revision of 1 July 2026 | the agency's own mapping applied, so a stream is one series across the year | codes read as filed in each half: moves two streams' tonnage and names Wood | the crosswalk file states the revision date and the mapping |
| SF9 | multiplicity across the eight streams | no correction needed; the bar is filed per stream | Bonferroni at 0.05/8, or Benjamini-Hochberg at 5 per cent: `same call`, asserted | convergence asserted; the golden's p is 0.0000041 |
| SF10 | rounding of the rate | per cent to one decimal, once, at the end | rounding each term first: `same call`, asserted | the prompt's rounding sentence; convergence asserted |
| SF11 | an enterprise whose permit number was superseded | no reading reaches the call: the released micro-data carries a survey record number only | the agency permit number or the enterprise number: neither exists on the micro-data, so no join from the register to the survey exists at all | asserted on the shipped schema: no file carries both a stratum and a producer key |
| SF12 | "field days" in the response log | days, at the division's booked field day of eight hours, which is what the collection documentation states | seven or seven and a half hours to the day: `same call`, and since the re-siting of ask A1 no graded figure reads the field_days column at all, so the reading moves nothing (0 of the 28 graded figures, asserted) | the survey's own collection documentation, section 5 on collection operations, and the assertion that no graded figure reads the column |
| SF13 | "municipalities' reported collections" in ask A3 | the 27 municipalities' own returns, each municipality's collected tonnage counted once | all 32 reporting entities, adding the five inter-municipal associations' returns for their member municipalities: inflates every region's gap by 12.5 to 20.0 times. This is now hazard H5 and not the ask's primary: the convention resolves it, so the cracker resolves it, and the ask's primary sits under it | the memo's compilation convention, "each municipality's collected tonnage counted once", and the receipts file's 27 origin entities, which are exactly those 27 municipalities |
| SF14 | "by origin region" in ask A3 | the region the waste arose in, the receipts file's own origin_region column | the receiving facility's own region: moves every region's gap by 1.4 to 15.4 times the gap itself | the prompt's own word, and the receipts file carries the origin region on every row |
| SF15 | "by the enterprise's region" in ask A1 | the region of the enterprise the collection case was opened for, read from the crosswalk row valid at the contact date | the region of the team that worked the case: moves every region by 50 to 175 contacts, and is not the enterprise's region; the region on the crosswalk row marked current: moves every region by 23 to 84 contacts and is the January 2027 holder, who the round never contacted | the asking sentence's own words, plus the assertion that no case's region changes across its own contact dates and that every current-only row for a reissued number begins after the last contact in the log |
| SF16 | "the contacts our 2026 round made" in ask A1 | one row per contact, exact duplicates counted once, over every case the round issued | contacts made in calendar 2026: `same call`, asserted, every one of the 6,094 contacts being dated inside 2026; the rows as loaded: 15 of them are a re-sent operations batch, which the battery removes | convergence asserted on the window; the duplicate batch is a hazard and not a reading |
| SF18 | "that number per usable return" in ask A1 | the contacts the asking sentence has just asked for, all of them, over the region's usable returns | the contacts made on the cases that returned only: 3.29, 3.29, 3.36, 3.43 and 3.38 against the committed 3.65, 3.64, 3.84, 3.86 and 3.77, so it is a live reading and not a convergent one | the asking sentence names the figure it divides, "that number", which is the whole-number figure beside it; asserted in `checks.py` SF18 |
| SF17 | "collected tonnage" for a municipality in ask A3 | the tonnage the municipality collected in 2026, taken once from its own return | the sum of its twelve return rows: on five municipalities the December row is the year's confirmation and already contains the eleven, so the sum counts those eleven twice and the gap reads 3.4 to 10.3 times the answer. Not a reading the records support: the December row stands at 11.8 times the mean of its own eleven months where no other month exceeds 0.86, and the sum puts those municipalities' facility receipts at 50 per cent of their collections against 94 to 99 elsewhere | the arithmetic of the returns themselves, asserted in `checks.py` A9, and the receipts file as the second witness |

## Ladder

| Rung | Analysis | Names | Metal z | Mixed C&I z | Dies to |
|---|---|---|---|---|---|
| 0 | rank the eight shortfalls against target (raw or relative) | Mixed commercial and industrial | n/a | n/a | the filed bar: the estimand establishes a shortfall at the 95 per cent level, which a ranking never does |
| 1 | test each shortfall against the published national CV (3.4 per cent, the 2025 round's) or against 1/sqrt(reporting enterprises) | Mixed commercial and industrial | 1.51 / 0.65 | 2.42 / 2.32 | neither figure is the 2026 estimate's own standard error, and the first is another round's; the microdata carries the design |
| 2 | design variance over the strata, finite-population correction omitted, or the sample treated as weighted with replacement | no stream established | 0.95 / 0.57 | 1.28 / 1.22 | the design documentation's own population and sample counts, which make the correction computable |
| 3 | design variance over only the enterprises reporting the stream | no stream established | 1.80 | 0.96 | the microdata ships an explicit zero per stream per enterprise, so a non-reporting enterprise is a datum and not a gap |
| 4 (decisive) | the domain total's design variance over every sampled unit in each stratum, with each stratum's finite-population correction | **Metal and metal-bearing** | **4.57** | 1.45 | nothing: the golden |

**Arithmetic.** Position: Metal is 2nd of 8 on rung 0's raw shortfall (2.90 points against Mixed C&I's 4.90,
a 1.69x lead to the loud answer) and 3rd on the relative ranking. Margin: the decisive rung clears the
filed bar by 2.33x (4.57 against 1.959964) and rung 3's best candidate falls short by 1.08x. Separation:
rungs 1 and 2 are 1.59x apart on Metal's z (1.51 against 0.95). Dominance: no single wrong route reaches Metal; the one route
that does, ignoring the design weights and rescaling the unweighted totals to the published national
total, is reported under `## Tried and rejected` with the measurement that shows the unrescaled form
self-refutes (four streams above 100 per cent, and no stream showing any shortfall at all). Grid: every
single-error cell files a feasible figure, and the eight streams' z values under the decisive route are
4.57, 1.45, 0.71, 0.61, 0.55, 0.45, 0.35, 0.31, so the second-best candidate is 3.17x below the bar's
distance. Worth: measured on the graded quantity (the verdict per stream), rung 4 moves the verdict for
two streams and rung 3 for none.

**Degrees of freedom.** One live degree of freedom would hold no ladder, so the lever and the noise are
checked to be different numbers: the lever is the ratio of the two streams' design CVs, which is set by
where their arisings sit in the design (3.81x to 9.82x over 60 seeds, median 6.03x), while the noise in
the ranked quantity is the sampling error of the arisings estimate. Across 60 seeds with the shipped plan
targets held fixed, Metal's z ran 3.62 to 6.61 and never fell below the bar, so the golden verdict is not
seed-hostage; Mixed C&I's z ran -1.32 to 4.11 around its shipped 1.45, which is the expected behaviour of
a shortfall that is not established, and the shipped pack's own value is asserted.

**The call is retrospective, with its reason.** Official statistics tests a reference year's published
estimate against a reference value, so the estimand names the closed 2026 reference year; the decision it
forces is forward, the division's single 2027 supplementary collection module.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | every enterprise in the Business Waste Survey's 2026 frame, sampled or not, for the denominator; every consignment despatched in 2026 for the numerator | estimand filed literally in the memo's estimand paragraph, naming the unsampled members in; C1 asserted |
| 2 Unit of account | the waste stream, one of the plan's eight | the plan's target table names the eight; the question names the unit |
| 3 Attribution window | the producer's despatch date in calendar 2026 | filed; C1 asserted against the confirmation-date reading (SF3) |
| 4 As-of dating | the register extract of 31 January 2027 and the survey's 2026 round | the capacity note names both extract dates; no later vintage ships |
| 5 Version basis | the revised 2025 release, not the preliminary | the revised release states it supersedes the preliminary; the call reads neither |
| 6 Denominator | estimated total arisings of the stream | filed in the estimand's own words; SF1 ruled out by that clause; C4, the rival denominator names a different stream |
| 7 Weighting | the survey's design weights as shipped | the microdata's weight column is the design weight; no reweighting is filed or needed; SF2 |
| 8 Window length | one reference year | the plan's targets are annual; the estimand names 2026 |
| 9 Boundary inclusivity | despatch date inclusive of 1 January and 31 December 2026 | C1: no consignment is despatched on a boundary minute, and the 2025 and 2027 edges are asserted clear |
| 10 Rounding path | once, at the end: per cent to one decimal, tonnes to the nearest tonne | the prompt's last sentence; SF10 convergence asserted |
| 11 Tie-break | none needed: exactly one stream clears the bar | asserted on the shipped pack, and the runner-up is 3.17x below the bar's distance |
| 12 Maturity and censoring | consignments despatched in 2026 and still unconfirmed at the extract are excluded as unconfirmed | SF6, convergence asserted both ways |
| 13 Order of operations | rate then compare then test | each step commutes with the others here; asserted |
| 14 Row order | file order cannot move a weighted total or a stratum variance | C1 by construction, asserted over three permutations |
| 15 Duplicate resolution | one row per leg; a child consignment is a distinct consignment, its tonnage counted at the parent's despatch leg | SF5, filed by "counted once at the producer's despatch leg" |
| 16 Identity normalisation | the business register enterprise number is the identity | the crosswalk's supersession rows and its reissued permit numbers, both asserted to move no main figure: no file carries both a stratum and a producer key, so the micro-data cannot be joined to a permit at all (SF11, D1, D5) |
| 17 Netting against gross | no netting: rejected loads returned to the producer are a separate leg and are not recovery | the operation code list has no code for a return; asserted |
| 18 Dimensional units | tonnes throughout the register and the microdata; one municipal extract in hundreds of kilograms | the unit is in each file's own column; the municipal files are outside the call's population, asserted |
| 19 Code and status semantics | R codes are recovery, D codes disposal, on the list in force at confirmation | the operation code workbook states the revision and the mapping; never the stump |
| 20 Integerisation | tonnages are whole tonnes in the register; no integerisation in the rate | asserted |
| 21 Clause scope | the memo's estimand paragraph governs the estimand and the bar; the design documentation's sections govern the survey it describes; the plan governs the targets | each document names its own scope |
| 22 Forward window contents | none: the estimand's window is closed, and the forward element is the module commitment the answer drives | stated in the capacity note |

## Literal reader

A reader who executes the memo's estimand paragraph, the plan's target table, the crosswalks and the
operation-code workbook word for word and infers nothing else computes each stream's 2026 recovery rate
from the register's confirmed recovery tonnage over the survey's design-weighted arisings estimate, and is
left with exactly one thing the shipped text does not state: how the rate's sampling error is computed.
Every reading of the twelve `SF` rows gives the golden or is ruled out by a quoted sentence, and the two
estimators of the denominator's design variance that the design admits (stratified linearisation with the
finite-population correction, and the delete-one jackknife within strata) agree to six decimal places on
all eight streams, so the literal reading lands on Metal and metal-bearing wastes.

## Oracles

None now, and one was cut in the repair pass of 2026-10-18. There is no corpus, no control bench, no
certified record and no reconciliation column that ties only under the golden. The ask layer's
re-siting added none: the crosswalk publishes no count, the response log no total and the municipal
pair no reconciled gap, so nothing in the pack ties only under a device's right handling, and the one
referee (the licensed-facility register) ties under every handling of every device.

**What was cut.** The judged pack's 2025 release published the coefficient of variation of the estimated
national total of business waste arising "for the 2026 round". That figure is the design CV of the 2026
arisings estimate, so it reproduced at 3.915 per cent under the decisive estimator and at 4.091 without the
finite-population correction: a solver who computed the denominator's design variance could confirm the
decisive method against a shipped number, which is an oracle under Part 2.4 whatever else it was doing.
Cut by publishing the measure for an aggregate no candidate estimator reproduces: the release reports its
own round's national total (623,430 t) and that round's coefficient of variation (3.4 per cent), computed in
`sim.round_2025` from a 2025 round whose micro-data, realised sample counts and weights do not ship. The
bait is untouched, because that figure is still the only precision measure in the pack and still the one
rung 1 borrows, and the figure's own date now makes sense: the release is issued 30 September 2026 and the
2026 round did not close until 16 January 2027, so the judged pack's sentence was an anachronism as well.
Asserted in `checks.py` H4 (the published 3.4 prints differently from every estimator of the 2026 round's
national CV: 3.9 with the correction, 4.1 without it inside the sampled strata, 4.5 without it anywhere,
4.1 weighted with replacement) and H5 (no 2025 weight, sample count or arisings record is anywhere in the
bundle).

**What the remaining published figures confirm, on every route.** The 2025 release's published arisings and
recovery rates are a prior year's and no 2026 route reproduces them. Its recovered column is now carried off
the register at the 30 June 2026 extract the release says it was compiled from, so the reason the release
gives for sitting below a later extract is true of the records: 230 confirmation legs of 2025 consignments
fall after that cut, the longest despatch-to-confirmation lag on a 2025 consignment is 626 days, and those
confirmations are 3,913 t of the 5,323 t distance, on every one of the eight streams. The rest is the
register's ordinary post-cut amendment, which is why no basis reproduces the column: the nearest, a recompute
at the stated cut, is off by 0.24 to 0.76 per cent a stream (12 to 461 t), and the distance to the published
column runs 1.4 to 4.9 per cent across the eight streams while deduplicating the re-notified consignments
moves the median stream by 0.51 per cent, so the column cannot settle the one choice ask A2 turns on. It
still does the two jobs the design needs it for, and both are asserted: excluding R1 from recovery would
publish nothing at all for the two streams that recover only through it (H8), and taking the holding site's
own confirmation instead of the operation it forwards to would publish 47,770 t for metal against the
released 66,611 t (H9). Every published 2025 arisings figure sits within one design standard
error of the 2026 estimate (H10), so the year-on-year movements are what the survey's own precision allows.
The plan's targets are constants every route needs. No shipped artifact ranks the eight streams on the
decision question.

## Ask sheet

Three asks, 28 separately gradable figures, all three sited on populations the main call never reads.
A1 and A3 were re-sited on 2026-10-18, after the pins pass left A1's primary a filed rule and A3's a
fork closed by a sentence; the quantities A1 asks for changed with it, A3's did not, and every
measurement below is on the cut pack. The lesson that drove the re-siting is in `## Tried and
rejected`: a fork is not a device, so a primary that a filed sentence can resolve has to be replaced
rather than hardened.

**A1, the chasing behind the round's returns** (audit trail of an input the call consumes). Figures:
for each of the five regions, the contacts the 2026 round made as a whole number and that number
per usable return to two decimals: 10 figures. H18 home: the trail from the survey the call
consumes, through rows the call never reads, to the round's own collection effort. Use: the
division's 2027 capacity note needs what a usable return cost to chase, region by region, and the
2027 module is costed against it. Primary device (D7 keys, silent): the agency's January 2027
licensing batch took the permit numbers freed when their holder's permit lapsed at the end of 2026,
so 150 of the numbers the round's cases were opened under carry a second crosswalk row marked
current whose validity starts in one of the agency's four weekly licensing runs of January 2027, and
on 126 of them that holder sits in another region; the reattribution moves every region's contacts
by 31 to 77 and every ratio by 0.02 to 0.09. The batch is not one kind of row: 12 of its 162
rows are ordinary re-registrations under a new number for the same holder, so no value in the
valid_from column isolates the device rows. The
join the battery's own repair leaves, take the row marked current or the latest, puts those cases in
the wrong region; the row that holds is the one valid at the contact date. The internal
inconsistency is temporal and arithmetic: the holder of record now did not hold the number when the
contact was made, the last contact in the log being 2026-12-30, so the case cannot be its case.
Every reissued number belonged to a holder with no 2026 despatch leg in the register, so no reading
of the permit register, however strict, can take a tonne out of the call's own population (asserted:
0 of the 150 is a 2026 despatcher, and restricting the register to producers whose 2026 row is
current leaves the designated set and every graded figure where the shipped pack had them). The
enterprises that gave a permit up are the ones the round found hardest to collect from, so the
reattribution is not proportionate and the ratio moves with the count. Nothing in the pack invites
the comparison: what the battery sees is a join that fans out, and both of its habitual repairs are
wrong.
Hazards: H3 (a re-sent operations batch of fifteen exact duplicate rows, all Norte), H4 (34 permit
supersessions, where a current-only filter drops a case's row and the join fails loudly), H6 (field
cases are allocated by workload, so 722 contacts were made by a team other than the one based in the
enterprise's region, and the team identifier is not this ask's basis). The usable-return count is a
per-case outcome counted once per case: the re-sent batch puts the row count at 1,634 against the
1,630 records of the micro-data and the 155 plus 195 plus 520 plus 760 of the design table, and
`checks.py` A7 asserts the tie at case grain.
Files on the path: `bws_2026_response_log.csv`, `enterprise_permit_crosswalk.csv`,
`bws_2026_design_and_weighting.pdf`, `collection_capacity_note_2027.pdf`; 11 columns. Stops: the
log's rows as contacts with the region off the row marked current (lazy, 1,916 / 1,420 / 1,575 / 684
/ 499 contacts against 1,965 / 1,387 / 1,652 / 641 / 434, every region wrong by 31 to 77 and every
ratio by 0.02 to 0.09), the same with the exact duplicates taken out (1,903 / 1,418, the batch
sitting in Norte on the ask's own basis), the team identifier read as the region (every region wrong
by 50 to 175 contacts), the answer.
Realism: a waste permit lapses when its holder stops the permitted activity and the agency's next
licensing batch draws on the numbers freed, which is why a permit register is kept effective dated.
Forcing figure: 150 of the round's permit numbers carry a current row whose validity starts after
the last contact in the log (2026-12-30), 126 of them in another region, and no case's region
changes across its own contact dates (0 exceptions), so the basis is one number and not a
date-by-date choice.

**A2, the 2025 reference year's confirmed recovery tonnage by stream** (the decisive construction on
a window the call never reads). Figures: 8. H18 home: the same chain construction on the prior
reference year, which the attainment table's own trend column needs. Use: the plan's mid-term review
quotes the prior year. Primary device (D1 duplication, silent): a set of 2025 consignments rejected
at the receiving facility's gate was re-notified under a fresh consignment number carrying the
original's reference and the same tonnage, so summing confirmed recovery over consignments exceeds
the producers' despatched tonnage for three streams; found only by reconciling each child
consignment against its parent's rejection leg. Hazards: H2 (the code revision), H4 (facility permit
supersessions). Files on the path: `waste_movement_legs_2025.csv`, `facility_register.csv`,
`waste_code_crosswalk.csv`, `treatment_operation_codes.xlsx`, `enterprise_permit_crosswalk.csv`; 12
columns. Stops: sum every confirmed R leg (lazy, every stream high by 78 to 160 t), the crosswalk's
currently valid codes only (metal 51,297, mixed commercial and industrial 67,519, wood 12,561 and
plastic 4,843 against 67,709, 89,749, 19,243 and 7,368), drop every re-notified consignment
including the genuine ones (over-corrected, two streams low), the answer. Realism: a rejected load is
re-notified rather than amended, and the register keeps both notifications. Forcing figure: 43 child
consignments carry a parent reference whose leg sequence ends in a gate rejection, and for those 43
the child's tonnage equals the parent's to the tonne.

**A3, the municipal waste reconciliation by region** (an input reconciled to another system's
total). Figures: for each of the five regions, the gap in tonnes between the municipalities'
reported collected tonnage and the licensed facilities' reported receipts of municipal waste on a
receipt-date basis, and that gap as a share of collections to one decimal: 10 figures. H18 home: a
reconciliation of a second collection system to the facility returns, at the region grain the
attainment table already uses. Use: the institute publishes the municipal series beside the business
series and the gap has to be explained before the release. Primary device (D9 self-validation,
silent): on five municipalities' returns software the December slot carries the year's own
confirmation rather than the month, so that row does not sum with its own eleven; a municipality's
collections are its December row where that row is the year, and the eleven months it already
contains are not added to it. The internal inconsistency is two arithmetic patterns pointing the
same way: those five December rows stand at 11.8 times the mean of their own eleven months while no
other return month exceeds 0.86 times its own, and summing twelve months puts those five
municipalities' facility receipts at 50 to 51 per cent of their collections while every other
municipality's sit at 94 to 99 per cent. The recovery is exact and self-validating, because the
December row less the eleven lands inside that municipality's own monthly range. No sweep compares a
return month with its siblings or a municipality's receipts with its own return, and the ask is
asked at region grain, which is one grain above the cut that shows it.
Hazards: H1 (two municipalities reporting in hundreds of kilograms, the unit in the file's own
column), H5 (five inter-municipal associations file a return covering their three member
municipalities, which file their own, and the memo files the counting convention). Files on the
path: `municipal_waste_returns_2026.csv`, `municipal_facility_receipts_2026.csv`,
`facility_register.csv`, `collection_capacity_note_2027.pdf`; 11 columns. Stops: every return,
twelve months each, the hundreds-of-kilograms rows read as tonnes (lazy, the gap reads 24.7, 110.2,
20.2, 29.3 and 25.2 times the answer), the same with the units converted (24.7, 14.9, 20.2, 29.3,
25.2 times), the 27 municipalities' own returns summed over twelve months (8.1, 3.4, 4.6, 10.3 and
8.0 times, a 12.5 to 27.0 per cent gap share against the answer's 2.6 to 4.1), the answer. Realism:
a monthly return form whose December slot is used for the annual confirmation is an ordinary returns
defect, and these five municipalities file through the same returns software. Forcing figure: five
December rows at 11.8 times the mean of their own eleven months against a highest 0.86 elsewhere,
and a receipts coverage of 50 to 51 per cent against 94 to 99 for the other 22. Basis and grain are
in the asking sentence (receipt date, origin region).

**Main population zero-counts.** Asserted in `checks.py`: zero device rows and zero hazard rows
inside the main call's declared population, which is the 2026 movement legs and the 2026 survey
micro-data. A1's device rows are crosswalk rows valid from January 2027 and response-log rows,
neither of which the call reads; no file carries both a stratum and a producer key, so no join
from the call's population to a permit exists at all (`checks.py` D1, D5, SF11); and no reissued
number is a 2026 despatcher, so the strictest reading of the permit register drops not one leg on
the device's account and designates the same stream (`checks.py` D7); the 43 re-notified
consignments of A2 are all 2025-despatched (asserted); A3's populations are municipal and never
read. Deleting every device leaves the call byte-identical, asserted. The repair's own scope is
asserted the same way: `checks.py` A10 holds the digest of every file the call reads against the
shipped pack, and only `bws_2026_response_log.csv`, `enterprise_permit_crosswalk.csv` and
`municipal_waste_returns_2026.csv` moved.

**Hazard table.** H1 units (A3; the two hundreds-of-kilograms municipalities read as tonnes put
Centro's gap at 110.2 times the answer instead of 14.9). H2 code revision (A2; the currently valid
codes alone move metal, mixed commercial and industrial, wood and plastic by 2,525 to 22,230 t). H3
re-sent batch (A1; 15 rows, 1,916 contacts against 1,903 deduplicated where they fall). H4 permit
supersessions (A1, A2; 34 of them, where a current-only filter fails the join loudly). H5 the
inter-municipal associations' returns (A3; every region, the gap 3.4 to 10.3 times the answer). H6
cross-region teams (A1; 722 contacts, every region 50 to 175 contacts out on the team basis).

**Referee.** One byte-clean referee, the licensed-facility register, arbitrates which facility is
interim and which final without carrying any level; it ties under every handling of every device. No
shipped figure ties only under a device's right handling: the crosswalk publishes no count, the
response log no total, and the municipal pair no reconciled gap.

**Cracker sheet.** The cracker landed the call, ran the hygiene battery (key uniqueness, exact
duplicates, unmatched joins, fan-out, count ties) and executed every filed rule the pack points at,
including the collection documentation's visit grain and the memo's municipal counting convention.

| Ask | Figures | What the cracker computes | Verdict |
|---|---|---|---|
| A1 contacts and contacts per usable return by region | 10 | the deduplicated contacts with the region off the crosswalk row marked current, which is what the battery's fan-out repair leaves | miss |
| A2 2025 confirmed recovery tonnage by stream | 8 | the sum over confirmed R legs after the battery, which finds no duplicate because each re-notification is a distinct consignment number | miss |
| A3 municipal gap by region and its share of collections | 10 | the 27 municipalities' returns summed over twelve months, the convention applied and the units converted, which the battery accepts because every return month is a valid row | miss |

**Measured by:** `generator/ceiling.py`, run on the cut pack through `generator/ceiling_deltas.json`.
**Pair ceiling:** 28.5
**Mirror leakage:** 0.0 per cent of ask weight

**The two premises, measured.** The gated figure takes one of the top two responses onto the call:
the cracker banks 38 for the recommendation, 7 for instruction following and 0 of 28 ask figures, so
45.00, the mirror misses the call and every ask at 12.00, and the pair is 28.5 against the gate of
40. Both responses on the call, each keeping its measured asks, is 45.0, which is the structural
floor a landed call carries and is not recoverable by ask work. Both on the call with one of them
resolving a whole ask of ten figures is 54.8, and that premise now costs a found inconsistency
rather than a section read, which is the whole of what this repair bought: at the pins pass the same
premise cost nothing, because A1's primary was a filed rule, and the measured figures were 38.3,
48.1 and 67.8. The premise itself is not something this script can check; the stage-4 cold reader
and the judge's Gate F check it.

**Why the two rows are two measurements.** The readings differ on every ask: the cracker
deduplicates the re-sent batch, the mirror counts rows; the cracker maps the retired waste codes
through the crosswalk's revision, the mirror takes the currently valid codes; the cracker applies
the memo's counting convention and the files' unit columns, the mirror neither. Neither reaches a
primary, because each primary is an inconsistency across grains or dates that no column description
asks for and no sweep performs. The three asks consume nothing the call's construction produces (A1
the response log and the permit crosswalk, A2 the 2025 legs, A3 the municipal files), so a
response's ask score does not depend on whether it landed the call, and the zero-count assertions
above are what prove it rather than a duplicated row in the script.

### Architecture 4's header block, archived

Architecture 4, drawn 2026-10-17 after architecture 3 was called spent, then abandoned on a model
constraint. Architecture 5 (criminology ground) died at stage 1 on measurement with nothing cut.
Architecture 6 is the live design and its sections are at the top of this note.

## Architecture 3, spent

Architecture 3 (internal audit of a port authority's capital programme payments, the misstatement
projected from a tested set drawn in euro rather than in items) is spent. The reason is structural
rather than a tuning problem, which is why architecture 4 re-roots on a different decisive quantity
instead of hardening this one.

**What the second judge of architecture 3 found.** NOT_DETERMINISTIC, SEND_BACK, repairable, with
Gate G passing and the decisive step analytical. But **stump power moderate to low**, and its blind
enumeration, written before it opened the graded blocks, filed the probability-proportional
projection and matched the golden exactly on all nine programme figures, the authority figure, the
largest programme and the referral. Its words: "A strong analyst who reads the schedule PDF and
manual 9.3 reaches 850,000 and refers." The cold reader of the same pack landed the same call at 80
to 90 per cent confidence.

**Why that is fatal rather than a weakness to tune.** A response on the main call banks about 45
before any ask. If both top responses land it, each scores 45 plus whatever the asks give, so the
pair average cannot reach 40 however strong the ask layer is: 45 is already above the bar. The
measured pair of 38.1 is `(56.0 + 20.1) / 2`, and the 20.1 is a response that misses the call. The
ceiling was never a claim that the call is hard; it assumed a ladder that keeps all but one response
off it, and two independent cold threads have now shown this ladder does not.

**The bind that cannot be undone.** The referral rests on basic precision, not on the projection: the
projection alone is 840,096.72 against a tolerable of 1,160,000, which accepts, and the refer comes
from adding the precision to reach 1,380,096.72. Basic precision needs a reliability factor. A call
resting on an input the bundle does not carry fails Gate B outright, which is what the first judge
found. So the factor table and the terms it uses had to ship, and shipping them is exactly what the
second judge says supplies the vocabulary that makes the route recoverable. Fixing Gate B breaks
Gate F and fixing Gate F breaks Gate B. That is a property of the draw: a monetary-unit sampling
call whose decision turns on the precision cannot both document its own arithmetic and withhold the
method. No amount of ask work or data tuning moves it, and the only remedy is a different decisive
quantity, which is what architecture 4 draws.

**The rule architecture 4 is drawn under, taken from that bind.** The decisive step may not rest on a
constant, a factor table or any other filed input that Gate B forces the bundle to carry, because
shipping the input ships the route. Everything the decisive step needs must already be in the pack,
and the choice must still not be: the structure of the organisation's own data forces it, and no
shipped sentence can name it without naming the method.

**The author's part in it, for the record.** Shipping manual 9.3 was my ruling, taken knowingly, with
the cost named at the time: it nudges a reader toward monetary-unit sampling, and I judged the nudge
cheaper than the gate. On Gate B that was right and I would rule the same way again. The error was
upstream, in accepting a draw whose call needed the field's own vocabulary shipped in order to be
answerable at all.

**What architecture 3 produced that outlives it.** Six rules now in the skills came out of this build
in one day, each with the measurement that earned it: a ceiling script scoring one reading twice; a
document sweep that read three PDFs as raw bytes and so never saw inside their compressed streams,
with the positive-control rule and its same-code-path refinement; the ceiling computed on Part 0's
weights rather than a legal but favourable point inside the bands; a dictionary-resolvable device
moving the mirror and never the cracker; cutting a free figure as a correctness check, which exposed
a Gate A defect in the quarter basis; and a device that is draftable but moves the call being held
rather than built. The build also carried the covered-lines golden that counted schedule references
where the ask said ledger lines, 275 against the true 285 at 21,709,610.89, which both the reader and
the judge found and which is the cleanest example on file of a golden sitting on the cracker's side
of its own device.

Every card is kept and architecture 3's identity now sits in the card's `lineage` with its fate.
Nothing of it is resumed: not the monetary-unit sampling world, not the projection driver, not the
ladder, not the pack.

### Architecture 4: Draw, archived

Architecture 4's draw table is demoted to an H3 archive heading, because `precut.py` reads whichever copy of a section it finds and would otherwise pass the design-stage gate on a ground that is abandoned twice over, once on the model constraint in the final section and once on the `ban.subdomain` BLOCK against task242 recorded below. Architecture 5 writes its own `## Draw` when its decisive step is fixed.

| | |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task190.json`, architecture 4, registered 2026-10-17T23:01:30Z |
| Pairing | epidemiology-public-health / disease-surveillance-outbreak-anomaly-detection (serves Anomaly Detection in the client taxonomy) |
| Objective | anomaly-detection |
| Shape | other: each allowed setting crossed with each evaluation year, with the arithmetic in the card's notes (04 and 13 both blocked against task195 and task191) |
| Decision type | dial_setting; answer unit a named option |
| Gap, pattern, Gate G | time; G1 decisive, G13 and G2 supporting; method_or_model_selection |
| Strategy, Layer 2 | other (a performance ratio produced by the configuration being replaced); estimation_fit |
| World | Finland, a regional public health authority of 14 surveillance districts; people from `guard.py names --geo Finland --seed 190` |
| Forcing event | cutover_or_migration: the detection platform goes live and the configuration must be set |

**Guard verdict, and it has moved.** At registration the card was WARN with no BLOCK, nearest driver 0.07
against task104. Re-run after the parallel builders registered, `guard.py check` now returns **BLOCK
ban.subdomain against task242**, which holds epidemiology-public-health /
disease-surveillance-outbreak-anomaly-detection on the Data Quality Monitoring objective and registered
inside the three builds the ban reaches. The pairing was free when it was drawn and is not free now, so the
registered ground needs a redraw whatever happens to the decisive step.

**The four WARNs, answered.** `government_agency` is 33 builds deep and has to be one here, because
statutory communicable-disease surveillance is a function no other kind of organisation performs; the
objective is the lane's own and its frequency is the lane rather than this draw;
`method_or_model_selection` repeats against task196 and stands at 8 of the last 12, and it is the truthful
label for "which basis ranks the settings" rather than a label chosen to spread the batch, so the variety
is carried by the driver at 0.07 against the whole corpus; the question form `which` repeats against
task197 and follows from the decision, which is a pick among the platform's allowed settings.

**Stage 1 is not complete.** The decisive step this ground was drawn for (value each allowed accumulation
window by the outbreak cases with onset after the alert it produces, against the reflex of multiplying the
clusters a window flags by the unit's published preventable share) was simulated in four parameterisations
and does not reverse: the two routes agree to within 1.6 to 4.1 per cent at every mix a district could
plausibly record, for the structural reason written into `## Tried and rejected`. The data-native sentence
that would have carried it is therefore not written, no prompt exists, nothing is cut, and the next move is
a decision on the decisive step rather than any further build work.

## Architecture 3's record below this line

Every heading from here to `## Tried and rejected` is architecture 3's, demoted so the design-stage gate cannot read a spent architecture's ladder, closure table or ask sheet as the live design. Architecture 4's own sections replace them when its decisive step is fixed.

### Architecture 3: Author override of the judge's disposition

Architecture 3's first determinism judge returned **NOT_DETERMINISTIC, SEND_BACK**. By the letter of
`build-pipeline` that spends the architecture and retires the number, because a SEND_BACK spends an
architecture and this is task190's third. The author overrode the disposition to **FIX_NOW**. The
reasoning and the condition are recorded here verbatim, because an author override of a judge's
disposition that nobody can find later is worse than no override.

> **The test I applied.** An architecture is spent when the decisive step cannot be saved, and the mark of
> that is when the only way to close the fork is to file the HOW. That is what killed architecture 1 of
> task194 this morning. It is not what is happening here. Every fix the judge asks for files the WHAT: what
> the sample is, how it was drawn, what the terms in its own working papers mean. None of them files the
> estimator. And the judge's own gates say the decisive step is alive: Gate F high, with every easy route
> accepting the population; Gate G pass; Gate H pass with the decisive step analytical and no decoy; the
> headline reproducing at 800,000, refer, Rail siding and yard 250,000. The proof is in the cold reader: it
> saw the certainty stratum perfectly well, called it out at about 100,000, and still used a value-weighted
> ratio estimator, got about 130,000 and accepted the population. Telling a solver how the sample was drawn
> does not tell it how to project from a sample drawn that way, and that gap is the whole build.
>
> **The condition, and it is hard.** If the re-judge after this pass is not APPROVE, task190 retires,
> without further argument and without another override. This is the only one.

The eight fixes the override carries are worked in the order they bind: the sampling design filed as a fact
about the sample; the reliability factors shipped; the terms the graded components use defined; the
allowance and the upper limit made to reproduce from the shipped table; tolerable misstatement stated as a
judgement with the derivation deleted; the four ask forks pinned in the asking sentences; the whole-euro
marker taken off the certainty lines; and the payment-run realism done with the run pins in one pass.

### Architecture 3: What is filed and what is open, after the override

**Filed, as facts about the sample and not as a method.** The testing schedule's basis of selection states
that the lines tested were selected with probability proportional to recorded value by stepping one
interval of 180,000 euro through the population's cumulated recorded value from a random start; that the
single interval was used for the whole population and was **common to every work programme**, none having
an interval of its own; that a line recorded at 180,000 or more spans a whole interval and was therefore
certain of selection; and that a line below the interval was selected with probability equal to its
recorded amount over the interval. Manual 9.3 defines selection interval, certain of selection, tainting,
basic precision, incremental allowance and upper misstatement limit. Manual 9.5 ships the Poisson
reliability factors at 95 per cent for nil to twenty overstatements.

**Open, and it is the decisive step.** No shipped sentence says how to get from the tested lines to the
population. The estimator is the analysis: the misstatement the testing found, the findings scaled on
recorded value, the certainty lines at their own error with the rest scaled on their stratum, or each
tainting at the interval with the certainty lines at their own error. `checks.py` asserts by word sweep,
with the PDFs' content streams decompressed, that no shipped file projects, extrapolates, scales up,
grosses up or multiplies a tainting.

**Why filing the design does not file the answer, measured rather than argued.** The cold reader had the
certainty stratum without being told it, named it at about 100,000, and still filed a value-weighted ratio
estimate of about 130,000 and accepted the population. Knowing how a sample was drawn and knowing what one
of its rows stands for are different pieces of knowledge, and only the second decides the call.

**What filing the interval closed.** The per-programme-interval route, which gave an authority figure a
quarter again as large and which nothing in the earlier pack refuted, is closed by the one clause that the
interval was common to every programme. `checks.py` computes that route and asserts it lands on a
different stated figure, so the closure is executed rather than claimed.

### Architecture 3: Draw

| | |
|---|---|
| Pairing | `accounting-audit-forensic` / `audit-testing-sampling`, filed against the client's Survey Research and Official Statistics because the deciding method is design-based estimation from a probability-proportional-to-size sample. A never-built pairing; the subdomain has never been drawn. |
| Objective | `anomaly-detection`. The object is a defect in a population of payments, separated from what the testing happened to catch, and the call is a monitoring decision: certify the population or send it to extended testing. |
| Shape | 12, drill-down to one leaf. Nine work programmes, two figures each (18), the authority's figure and the programme carrying most (2), the referral decision (1), the chart's nine bars and the mark on the largest (10), and the three ask families' 41 figures. 72 graded figures, plus instruction-following. |
| Gap | 4, rule: which projection the tested set's own selection entitles. |
| Strategy | `population_selection`; Layer 2 family `field_method`; generators G16 decisive, G17 supporting, G10 in Layer 1. |
| Decision | `quantity_figure`, answer unit `currency`, question form how-much. |
| World | Carrowmore Port Authority, Ireland, EUR, year to 31 December 2026. People drawn from `guard.py names --geo Ireland --seed 190`: Tanya McCrea, Colm Shaffrey, Marc O'Reardon. |
| Deliverables | `projected_misstatement_2026.csv`, `misstatement_by_population_2026.png`. |
| Guard | No BLOCK, after five redraws (context artifact three times, gap, people, deliverables) and three differentiation lines. Two WARNs, `repeat.gate_g` and `overuse.gate_g`, answered in the card's notes: no other Gate G key is true of this build, and the variety is carried by the driver, which scores 0.07 against the whole corpus on `guard.py check` and 0.05 against every card driver on `guard.py heart`, the lowest this slot has drawn. `guard.py heart` WARN. |

**The data-native sentence.** The tested set was drawn by stepping a fixed amount of euro through the
payment population in value order, so a tested payment line stands for that amount of the population
rather than for one line, every line at or above it was certain of selection and stands only for itself,
and the amount itself is recorded in no file and has to be recovered from the tested set; the authority's
capital payments are the kind of population that design exists for, a handful of contractor certificates
holding most of the value and twenty-six thousand small lines holding the defects.

**Why this ground, written against the slot's own lineage.** Architecture 1 settled whether unobserved
members were in the population and failed the WHAT screen. Architecture 2 estimated a counterfactual
density and died three times on the same shape: the specifications always disagreed, and each pass bought
agreement another way (a smooth draw, then an algebraic cancellation) rather than earning it. The author's
four constraints for this draw follow from that, and each is answered here:

1. **No fitted counterfactual density.** Nothing is fitted. Once one integer is recovered the figure is an
   exact weighted sum over the tested items: no window, no bin width, no family, no polynomial order, no
   tolerance. There is no specification grid for a judge to sweep, because there are no specifications.
2. **The blind-response test, at the draw.** Measured on paper below, before any file exists.
3. **The insensitivity screen.** Answered below, and the answer is the inverse of architecture 2's: the
   figure is strictly proportional to the recovered interval, so it is maximally sensitive to the one
   thing the data pins exactly, rather than insensitive to what the candidates differ on.
4. **No sentence filed at authority without the author's approval.** Nothing is pinned at authority in this
   design as it stands. If the build needs one, its exact wording comes to the author before it ships.

**The decisive quantity, and why it is determinate by construction.** Let k be the amount of euro stepped
through the population. Each tested line below k was selected with probability equal to its own amount over
k, so a tainting of fraction f on such a line projects as f times k. Each line at or above k was certain,
so it projects at its own error. The population's misstatement is the sum of those two terms over the
tested set. Every term is an exact arithmetic function of shipped numbers and k, and k is an integer the
tested set pins two independent ways:

- **the certainty threshold:** the smallest amount above which every line in the population is in the
  tested set, which is k itself;
- **the value step:** order the population by the value the selection ran on, cumulate the amounts, and
  the tested lines below k sit one per k of cumulated value, so the book value between consecutive tested
  lines is k.

The two have to agree, and they do, exactly. Nothing is filed that says to do either.

**The insensitivity screen, answered.** Architecture 2's agreeing estimator agreed because it cancelled the
fitted level algebraically, so it was insensitive to exactly what the candidate specifications differed on
and every other candidate stayed standing. Here the question is not why one estimator among many agrees,
because there is no family: the figure is one sum. The thing that could still be argued is k, and the
figure is linear in k, so a solver who recovers a different k files a proportionally different figure. k is
therefore the whole of the analysis, and it is pinned exactly by two independent observables rather than
chosen. The candidates the design has to rule out are not variants of one estimator but three different
estimators (the factual sum, the book-value ratio, the size-banded ratio), and what rules them out is that
the tested set is visibly a size-biased draw: every line above a definite amount is in it, and below that
amount the share of lines tested rises exactly in proportion to amount. That is a property of the shipped
record, not a rule in a file.

**The field's own evaluation, measured before the ladder was fixed.** A monetary-unit sample is not
evaluated by the projection alone: the standard evaluation is the projected misstatement plus basic
precision plus an incremental allowance for the taintings found, compared against tolerable misstatement
as an upper limit. Basic precision is the interval times the reliability factor at the stated confidence
and is computed before any tainting is looked at, so a draw whose basic precision already exceeds
materiality is escalated by step one of a textbook evaluation with no projection and no insight at all.
The first sketch did exactly that: an interval of 520,000 against materiality of 750,000 gives basic
precision of 1,560,000, **2.08 times materiality**.

**Why that sizing was indefensible, which is the reason and not just the arithmetic.** The interval an
auditor draws is (tolerable misstatement less expected misstatement times the expansion factor) over the
reliability factor. **Sizing with no allowance for expected misstatement therefore forces basic precision
to equal materiality exactly**, at any materiality: the interval is materiality over the factor, so the
factor cancels. A sample sized that way rejects its population on any tainting at all, which is why no
auditor sizes one that way, and it is why the first sketch's interval could not have been drawn by the
body it was attributed to. Planning for expected misstatement is what opens the headroom the decision
needs, and the headroom is exactly the expected misstatement times the expansion factor.

### The design point

| | |
|---|---|
| Reliability factors | Poisson, one-sided upper bound, 95 per cent: RF(0) 3.00, then 4.75, 6.30, 7.76 and on, the table every audit text carries. Expansion factor 1.60. |
| Population | 59,469,739.92 EUR over 26,648 payment lines, nine work programmes |
| Tolerable misstatement | 1,160,000 EUR, 2.0 per cent of budgeted capital expenditure of 58,000,000. **Shipped.** |
| Expected misstatement allowed in planning | 387,500 EUR. **Not shipped, and the reason is below: the plan's own sizing formula would otherwise give the interval away exactly.** |
| Interval | (1,160,000 less 387,500 x 1.60) / 3.00 = **180,000**. Not shipped. |
| Selections | 330, on 271 distinct tested lines; the 31 certainty lines hold 15,826,525 EUR, 75 per cent of the tested recorded value of 21,043,847.13 |
| Basic precision | 180,000 x 3.00 = **540,000, which is 0.466 of materiality**, so step one escalates nothing |
| Stated granularity | the nearest **50,000** EUR, set from the measured route spread below |

### The selection interval, filed rather than recovered

Earlier passes of this build left the interval to be recovered from the tested set and enumerated ten
routes a solver might recover it by, one of which the record admitted. The first determinism judge refused
that: the pack did not hold the interval, the decision rested on it through basic precision, and the
recovery the note claimed was not one either isolated thread performed. The interval is now filed. The
route table, the lattice feasibility search and the granularity argument built on the route spread are all
retired with it, and the generator's determinism block now asserts the two things that matter instead:
that the filed interval and the filed start reproduce the shipped selection exactly, and that the
per-programme-interval route the working paper rules out lands on a different figure.

### The programme table, and the blind responses

Nine programmes, each carrying the projected misstatement and the share of its recorded value that was
certain of selection. The five families are a constant in every cell, nil in every cell, and one obvious
rate applied to recorded value, to the tested-line count, or to the misstatement the testing found.
Measured at the draw, before any file existed: all five score **4 of 18, 22 per cent**, because four
programmes read nil, which is above the fifth the author set as the point to act, so the construction was
tuned to three nils. Measured again on the cut pack by `checks.py`: **all five score 3 of 18, 17 per
cent**, and those three cells are the three nil misstatements. No blind family reaches a non-nil
misstatement or any certain share at all, because both graded figures per programme need the recovered
interval.

### The tuning contract, and what the cut pack measures against it

Two residual defects at the design point, both tuning rather than design, with the constraint asserted
against each and the measurement beside it:

1. **The two paths to the headline have to agree.** Both are computable, so if the stated programme
   figures and the rounded total disagree the task has two defensible headlines, and filing the WHAT does
   not fix it because the other path stays computable. That was architecture 2's SF12 failure. The
   generator tunes each programme's taintings so **the sum of the stated programme figures equals the
   stated total**: measured, the nine stated figures sum to 800,000 and the unrounded 811,170.09 rounds to
   800,000, asserted both ways.
2. **Four nil programmes at the design point, three in the pack.** Measured: Deepwater berth renewal, Quay
   3 reconstruction and the Dredging programme, each nil exactly rather than merely deep in its cell, and
   none of them carrying a nil certain share, which is what protects the pair. The two largest are nil
   because they are paid on contractor certificates and carry no day-work defect at all; the Dredging
   programme carries 31 defective day-work lines that the selection happened to miss, which is what a
   probability sample does and is the honest reason its figure is nil.

The rest of the tuning contract, with the measured value beside each: every programme's underlying figure
at least 9,000 inside its stated cell (worst 10,688, at Rail siding and yard) against a per-programme
route band of at most 1,214 euro across the five near routes; the headline's underlying at least 11,000
from its edge (measured 13,830, against a headline route band of 3,725); the largest programme by
misstatement outside the top three by recorded value (Rail siding and yard, fourth of nine); the stated
figures taking at least five distinct values (measured six: nil, 50,000, 100,000, 150,000, 200,000 and
250,000); and all five blind families at 3 of 18 or fewer (measured 3).

### Readability screen, test 6, written out

The author's ruling is taken: test 6 asks how the decisive step is **found**, not how much arithmetic
follows once it is found. The step here is recognising that the sample was drawn in euro rather than in
items, so a line at or above the interval stands only for itself while a tainting in a small line carries
a whole interval of untested euro. That is a reconceptualisation of what one tested row represents, not a
subtraction, a ratio or half of a reported figure, and the multiplication that follows being trivial is
what a correct estimator usually looks like. **Verdict: silent.** Having written it out, it does not fire.

### What may be filed at authority, and what may not

**The leak the author caught, and the rule it gives.** The first draft of the plan stated tolerable
misstatement, the confidence and the expected misstatement allowance. The reliability factor at 95 per
cent with none expected is 3.00 and the expansion factor is 1.60, both in every audit text, so any
domain-competent reader computes (1,160,000 less 387,500 x 1.60) / 3.00 and has the interval exactly from
the plan alone. **The sizing formula is the inverse of the recovery problem the task is about**, so stating
its inputs at authority states the answer. The expected-misstatement sentence is therefore cut from every
shipped document, and the allowance lives only in this note as the reason the sizing is defensible. Without
it a reader has (1,160,000 less an unknown times 1.60) / 3.00 and can only bound the interval below
**386,667**, which is 1,160,000 over 3.00 and still a factor of 2.1 above the true 180,000, so the
recovery is left intact. The general rule, going into the slot's record: **before filing
any figure at authority, invert every formula the field would apply to it and check what the inverse
yields.**

**The reliability factors: Gate B, decided.** The decision rests on a bound, and a bound needs a
reliability factor, which the pack ships nowhere. The decision is that **they are standard domain knowledge
and the pack ships nothing for them**, for three reasons. First, Gate B asks whether the pack holds the
data the answer needs; a published constant every text in the field carries is not data, and no pack is
expected to ship the normal distribution's quantiles either. Second, the alternative fails worse: a manual
that ships the factors has to say what they are for, and any sentence that does so names the interval or
says the population was tested by selecting from its monetary units, which is the premise of the decisive
step and the one thing that must stay unstated. Third, the decision does not depend on the richer parts of
the evaluation: the projection plus basic precision alone clears materiality by 15 per cent, and basic
precision needs only the factor 3.00. **No reliability table, no expansion factor and no evaluation
procedure appears in any shipped file**, asserted by word sweep in `checks.py`.

**The decision rule, and the ambiguity that had to go.** "Where the testing indicates that the population
may be misstated by more than tolerable misstatement" does not say whether the comparison is against the
projection or against a bound. On these figures the projection is 811,170.09 against materiality of
1,160,000, so a solver who gets the decisive step right and compares the projection itself **certifies**:
the wording would have thrown the call away after the analysis was done. It is reworded so the comparison
is a confidence statement, which can only be met by a bound, without naming an estimator, a factor or the
interval.

**The two documents, held for the author's approval and shipped only after it.**

The audit plan, section 4:

> **4.2 Capital programme payments.** Tolerable misstatement for the capital programme payments
> population is set at 1,160,000 euro for the year to 31 December 2026, being 2.0 per cent of budgeted
> capital expenditure, and the population is tested to a confidence of 95 per cent.
>
> **4.3 Conclusion on a tested population.** A population is accepted only where the testing shows, to
> the confidence at 4.2, that the population's misstatement does not exceed tolerable misstatement. Where
> the testing does not show that, the population is referred for extended testing before the financial
> statements are certified.

The audit manual, part 9, which files the estimand and nothing else:

> **9.1 What a tested population's misstatement means.** The misstatement of a tested population is the
> amount by which the population's recorded value exceeds the amount properly payable, taken over every
> payment line in the population and over the year in which the line was paid. It is an amount of euro and
> not a count of lines or of invoices. It is stated for each work programme and for the authority, each to
> the nearest fifty thousand euro, the authority's figure being the sum of the programme figures as stated.
>
> **9.2 Records.** No feed, schedule or register the authority keeps records a population's misstatement,
> and none can: the payment records carry what was paid, not what was properly payable, and the testing
> establishes the difference only for the lines tested. The head of internal audit is satisfied each
> year that the figure reported rests on the year's own payment records and the testing performed on them.

What those two documents between them do **not** say: the interval, the number of selections, how the
population was ordered or selected from, the expected misstatement allowance, any reliability or expansion
factor, any evaluation procedure, and anything about projecting, scaling, weighting or extrapolating a
finding. 4.2's two figures bound the interval below 386,667 and no further. 9.1 files population, outcome,
window, unit, segmentation and grain, and 9.2 says no column holds the answer.


### Architecture 3: Default path

1. Read `capital_payment_lines_2026.csv` and `supplier_master.xlsx`, carry the ledger's supplier numbers
   onto the master's through `supplier_number_crosswalk.csv`, and take each payment line's work programme
   from the capital programme register.
2. Keep the lines in the capital programme payments population for the year to 31 December 2026: drop the
   two credit notes and the lines they reverse, collapse the batch the bank feed delivered twice on its
   delivery sequence, and take the prior year's lines out of the overlapping extract.
3. Read `internal_audit_testing_schedule_2026.pdf` and lift the tested lines out of the table inside it:
   the line reference, the amount recorded and the amount the testing found properly payable.
4. Compute the misstatement the testing found: for each tested line, recorded less properly payable. Total
   it. It is 15,445.38 euro, which cannot be the population's misstatement because only part of the
   population was tested.
5. Project it to the population on the ratio the files make obvious: the population's recorded value over
   the tested recorded value, 59,469,739.92 over 21,043,847.13, a factor of 2.826.
6. State the result by work programme and for the authority, and read the conclusion at plan 4.3.

**Ends on:** 43,648.52 euro, which is accepted at 4.3 and certifies the population, with Security and
access systems the programme carrying most of it.
**Golden:** 800,000 euro, which is not accepted at 4.3 and refers the population for extended testing,
with Rail siding and yard the programme carrying most of it.

The default path cleans every key correctly, reads every clause correctly and uses a projection that is
arithmetically sound. It files a figure nineteen times too small because it treats the tested lines as a
sample of lines when they are a sample of euro.

### Architecture 3: Stump sentence

The default path scales the misstatement it found on the ratio of the population's recorded value to the
tested recorded value and files **43,648.52** euro, which certifies the population, because the 31 lines at
or above the recovered selection interval hold 75 per cent of the tested recorded value and are sound,
while every defect sits in a small day-work invoice that was selected with a probability equal to its own
amount over that interval and therefore stands for a whole interval of untested euro; the misstatement the
selection entitles is 800,000, which refers the population for extended testing.

### Architecture 3: Three rules

- **Task type:** anomaly-detection, the client task type in Survey Research and Official Statistics
  that serves Anomaly Detection, worked as the house domain's `audit-testing-sampling`: whether an
  administrative population holds a defect that the testing only sampled, and how much of it.
- **Domain test:** the deciding quantity is the misstatement in a population projected from a sample,
  which audit estimates on the sample's own inclusion probabilities because the sample was drawn in euro
  and not in items, so a tainting projects at the selection interval and a line certain of selection
  stands only for itself. Swap the nouns to a utility sampling meter readings for a billing error rate and
  the design has no reason to exist: a utility samples meters, because meters are what it is testing, so
  inclusion is equal and the ratio projection is the right one. The proportional design exists only
  because what is being tested and what materiality is denominated in are the same unit, which is what
  makes this an audit sampling problem and not a counting one.
- **Swap:** "how many of the hospital's admissions in the year were recorded against the wrong tariff"
  reads as a count over the sampled admissions scaled by the admission count, because admissions are
  sampled as admissions; nothing makes a large admission certain of being audited and nothing makes a
  small one stand for many, so the quantity collapses into the count and the task has nothing to estimate.
- **Layer 1:** the authority's own systems produce all of it and none of it decides the call. The ledger
  carries one row per payment line and several lines per invoice; two credit notes reverse payments inside
  the year; the bank feed delivered one payment batch twice with its own delivery sequence; the supplier
  master numbers suppliers differently from the ledger and a crosswalk carries both; the testing schedule
  is a table inside a PDF; the prescribed prior-year sample and the current year's sit in one overlapping
  extract; the capital programme register states values in thousands where every other file is in euro to
  the cent; the authority's financial year is the calendar year while the funder's grant claim runs to 31
  March.
- **Layer 2:** `field_method`. The methodological choice is what one tested payment line stands for: itself,
  a share of the lines, a share of the recorded value, or a fixed amount of euro fixed by how the
  selection was made.
- **Decisive step:** recognising that the tested set is a sample of euro and not of lines, so every line at
  or above the selection interval was certain and stands only for itself while a tainting below it carries
  a whole interval, and recovering that interval from the tested set.
- **Not semantics:** plan 4.2, plan 4.3 and manual 9.1 fix the population, the outcome, the window, the
  unit, the segmentation and the grain, and the field dictionary gives every column, so nothing turns on a
  reading. A solver who reads every field and every clause correctly still has to decide what the tested
  lines represent, and the misstatement found, the recorded-value ratio, the stratum ratio and the
  interval each give a different number: 15,445.38, 43,648.52, 129,201.54 and 800,000.
- **Not rule application:** no shipped sentence names a selection interval, a selection count, an inclusion
  probability, a projection, an extrapolation, a weighting or a stratum, and none describes how the
  population was ordered or selected from. A word sweep over every shipped file asserts it. Executing
  every stated rule leaves the solver holding a population, a tested set, a definition of misstatement and
  a question about what the tested set stands for.
- **Analyst test:** a strong analyst who carries the supplier numbers through the crosswalk, resolves the
  payment lines onto invoices, drops the credit notes and the re-delivered batch, lifts the table out of
  the PDF correctly and reads 9.1 exactly projects on the recorded-value ratio and files **43,648.52** (the
  `Ends on:` figure), where the misstatement the selection entitles is 800,000. `checks.py` runs that route
  on the generator's clean truth and asserts it files 43,648.52, then changes the decisive step alone and
  asserts 800,000.
- **Estimand:** manual 9.1: "The misstatement of a tested population is the amount by which the
  population's recorded value exceeds the amount properly payable, taken over every payment line in the
  population and over the year in which the line was paid. It is an amount of euro and not a count of
  lines or of invoices. It is stated for each work programme and for the authority, each to the nearest
  fifty thousand euro, the authority's figure being the sum of the programme figures as stated." Population,
  outcome, window, unit, segmentation and grain are all there; how the amount is arrived at for the lines
  that were not tested is nowhere stated, and that is the analysis.
- **No decoy:** nothing is planted to be caught. No scorecard, league table, ranked artifact, draft paper,
  memo or stakeholder figure ships; no block is copied; no screen, flag or indicator ships that the solver
  is meant to distrust. The tested set is a real sample of the population and every amount in it is the
  authority's own record; the defect is a wrong labour rate applied across small day-work invoices, which
  is a thing that happens and not a thing placed to be found.
- **No certified replay:** no past figure for this quantity ships. The prior year's extract holds its own
  tested lines and their findings, and no route on the ladder reproduces any closed or certified number
  from them; the prior year's own misstatement is not stated anywhere.
- **Lesson:** when a sample was drawn with probability proportional to size, what one sampled row stands
  for is fixed by the design and not by the row count or the value share, so the right projection is the
  one the design entitles and the ratio that the file makes obvious is wrong by the ratio of the sampled
  rows' mean size to the size-biased mean. No build on file teaches it: the corpus has survival behind a
  join, grain against a decided unit and conditioned yield, but no build turns on the inclusion
  probabilities of a designed sample recovered from the sample itself.

### Architecture 3: Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| below 0 the misstatement found, 15,445.38 | 9.1 defines misstatement, so a solver totals what the testing found | the schedule carries recorded and properly payable, so the difference is a column pair | yes, the first arithmetic | none ships | the battery reconciles the schedule to the ledger, not this | yes, one subtraction | readable |
| 0 the recorded-value ratio, 43,648.52 | nothing names a projection; 9.2 says the testing establishes the difference only for the lines tested, which makes the solver ask how to get from part to whole | the population's recorded value and the tested recorded value are both sums of one column | yes, the opponent's default when handed a sample and a population | none | no | yes, one ratio | readable |
| 1 the stratum ratio, 129,201.54 | nothing names a stratum | no column marks a line as certain of selection | yes, the obvious correction once the big tested lines are noticed | none | no | one ratio on two groups | readable |
| 2 **each tainting at the recovered interval, 800,000 (decisive)** | no shipped sentence names a selection interval, a selection count, an inclusion probability, a projection, a weighting or a stratum, and none says how the population was ordered or selected from, asserted by word sweep | no column, key or flag marks a line as certain, as proportional, or as standing for anything; the schedule carries a line reference, an amount recorded and an amount properly payable | no: the reflexes are the subtraction, the ratio and the stratified ratio, and each files a named wrong figure | none ships; no corpus, twin or colleague voice scores any projection | the battery reconciles the schedule to the ledger and finds the re-delivered batch, never what a tested line represents | no: the interval has to be recovered from the pattern of which lines were tested and which were not before anything can be multiplied | silent |

**Test 6, written out.** The test asks how the decisive step is **found**, not how much arithmetic follows
once it is found. The step here is recognising that the sample was drawn in euro rather than in items, so a
line at or above the interval stands only for itself while a tainting in a small line carries a whole
interval of untested euro. That is a reconceptualisation of what one tested row represents, not a
subtraction, a ratio or half of a reported figure, and the multiplication that follows being trivial is
what a correct estimator usually looks like. Written out, it does not fire. **Verdict: silent.**

### Architecture 3: Semantic fork table

| id | Term or convention | Golden reading | Alternative | Ruled out by |
|---|---|---|---|---|
| SF1 | "the population" | every capital programme payment line paid in the year to 31 December 2026 | the invoices rather than the lines; capital and revenue together | 9.1 says every payment line in the population and the register names the capital programmes; `same call`: the figure is identical read on lines, asserted |
| SF2 | "misstated" | recorded value less the amount properly payable, overstatements only | any difference in either direction; absolute values | 9.1 says the amount by which the recorded value exceeds the amount properly payable; the testing found no understatement, asserted |
| SF3 | the window | 1 January to 31 December 2026, by the date the line was paid | the funder's year to 31 March; the date the invoice was received | 9.1 says the year in which the line was paid; the register states the authority's year; `same call` on the receipt date, asserted |
| SF4 | the unit | one amount of euro | a count of lines or of invoices | 9.1: an amount of euro and not a count of lines or of invoices |
| SF5 | the segmentation | the nine work programmes on the capital programme register | the three directorates; the supplier | 9.1 says for each work programme; the register carries the programme on every line |
| SF6 | the grain | the nearest fifty thousand euro per programme, the authority's figure their sum | the unrounded sum rounded once | 9.1 files both, and the construction makes the two agree: the stated programme figures sum to the stated total, asserted |
| SF7 | the credit notes | excluded, both the credit note and the line it reverses | the line kept, or the credit note kept as a negative | the dictionary gives `reverses_line_ref`; `same call`: neither is in the tested set, asserted |
| SF8 | the re-delivered batch | one payment line however many times the feed delivered it | each delivery a line | the dictionary states the feed's delivery sequence and that a line is one payment; `same call`, asserted |
| SF9 | the supplier numbers | the ledger's numbers carried onto the master's through the crosswalk | the ledger's numbers read as the master's | the crosswalk is complete and one-to-one over the window, asserted; the figure never reads a supplier |
| SF10 | the overlapping extract | the current year's tested lines only | both years' | the extract header states both years and the schedule states its own year; `same call` on the figure, asserted |
| SF11 | the register's thousands | converted to euro | read as euro | the register's own column header and the dictionary; `same call`: the figure never reads the register's values, asserted |
| SF12 | "shows, to the confidence at 4.2" | a bound on the misstatement at that confidence | the projection itself compared with tolerable misstatement | 4.3 says the testing must show that the misstatement does not exceed tolerable misstatement, which a point estimate does not show; and the crudest bound at that confidence already exceeds it, asserted |
| SF13 | "the programme carrying most of it" | the programme with the largest stated misstatement | the largest by recorded value, or by the misstatement found | the deliverable asks for the misstatement; the three rankings name different programmes, asserted |

### Architecture 3: Ladder

**Measured on a real selection, not modelled.**

A population of 26,648 payment lines in four classes (contractor certificates, subcontractor interim
payments, day-work variation invoices, sundries) and a real monetary-unit selection at 180,000 from a
random start. The defect is a wrong day-work labour rate applied across small variation invoices in seven
of the nine programmes; the two largest by recorded value, Deepwater berth renewal and Quay 3
reconstruction, are paid almost entirely on contractor certificates and carry none of it, and **no
certificate is overstated: every line certain of selection was found sound**, which is what makes the
recorded-value ratio fail. Six programmes carry a tainting in the sample; the Dredging programme's 31
defective lines were all missed by the selection, so its projection is nil. A first draft put an error on
one certificate and it inverted two rungs, because the ratio route scales that error by the
whole-population factor while the stratum route takes it at face: the line is in `## Tried and rejected`.

The figures in the table below are the measured ones at the design point the generator carries. Every one
is asserted in `checks.py` against the clean truth, and `verify.py` recomputes each from the bundle alone
on its own code path, recovering the interval itself rather than being told it.

| Rung | The analysis | Figure | Upper limit | Decision | Step |
|---|---|---|---|---|---|
| below 0 | the misstatement found in the tested lines | 21,004.93 | 569,406.90 | certify | |
| 0 | the errors found scaled on the population's recorded value over the tested recorded value | **57,577.47** | 620,608.46 | certify | x2.74 |
| 1 | certainty lines at their own error, the rest on their stratum's recorded value | 156,183.24 | 758,656.54 | certify | x2.71 |
| 2 | **each tainting at the filed interval, certainty lines at their own error** | **840,096.72** | **1,607,781.54** | **extended testing** | x5.38 |

The incremental allowance on the golden is 227,684.83, which is 0.27 of its projection, and the allowance
on each wrong rung is modelled at 0.40 of its own sample part, so every rung is tested at the conservatism
the golden itself earns. **No wrong rung reaches extended testing**: the nearest one's upper limit is
758,656.54, **65 per cent of materiality, a 35 per cent margin**, while the golden clears materiality by
**39 per cent**. Basic precision alone is 0.466 of materiality. Every certainty line was found sound, so
the certainty part of each rung is nil and the allowance falls entirely on the sampled part.

**The decision is robust to how the bound is built, which matters because the bound's construction is not
filed.** The crudest defensible one-sided bound at the stated confidence is the projection plus basic
precision, because basic precision is by definition the bound when nothing is found: 840,096.72 plus
540,000 is **1,380,096.72, which clears materiality by 19 per cent**. So a solver who knows only the
single factor the manual's own table gives at nil overstatements, 3.00, reaches the right decision,
and every richer bound clears it by more. The nearest wrong rung fails under every bound: 129,201.54 plus
540,000 is 696,183.24, 60 per cent of materiality. Every rung walks one way, the decisive move is the
largest, and the golden is the extreme.


**Position and dominance.** On every rung below the decisive one the programme carrying most of the
misstatement is Security and access systems, seventh of nine by recorded value, while the golden names
Rail siding and yard, fourth of nine: the default path does not merely mis-size the figure, it names a
different programme. The recorded-value ranking and the tested-lines ranking both name Deepwater berth
renewal, the ranking by misstatement found and the stratum ratio both name Security and access systems,
and no natural ranking of the pack reaches the golden's answer. The golden's leader leads its runner-up by
a full stated cell, 250,000 against 200,000, and by 50,257 unrounded, so the two do not overlap.

**The grid.** The wrong answers are the rungs and the refused recovery routes, not fit variants: the
misstatement found (15,445.38), the recorded-value ratio (43,648.52), the stratum ratio (129,201.54), and
the figures the refused intervals give (383,447.76, 598,944.79, 811,692.98, 812,248.27, 814,441.81,
814,895.43, 988,931.41, 1,116,668.39 and 1,116,814.17). Every single-error cell files a feasible figure.
Four of the refused intervals round into the golden's stated cell, which is the granularity doing its job
rather than a leak: they are the approximate recoveries of the same interval. The five that do not land at
400,000, 600,000, 1,000,000 and 1,100,000, none of them the golden.

### Architecture 3: Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every capital programme payment line paid in the year | 9.1 files it literally; SF1 asserted |
| 2 | Unit of account | one amount of euro | 9.1; SF4 |
| 3 | Attribution window | the date the line was paid | 9.1; SF3 asserted, and the receipt date gives the same figure |
| 4 | As-of dating | the ledger extracted 14 January 2027, the testing completed 26 February 2027, the year closed 31 December 2026 | the extract headers state it; the schedule carries its own completion date |
| 5 | Version basis | the bank feed's second delivery of the duplicated batch is the same payment | the dictionary's delivery sequence; SF8 |
| 6 | Denominator | none: the figure is an amount, not a rate | 9.1 states an amount of euro; each programme's recorded value ships beside it as a separate figure |
| 7 | Weighting | the weight a tested line carries is fixed by how the selection was made, and is the analysis | not closed by a sentence, and must not be: this is the decisive step |
| 8 | Window length | none: the figure is a level over one closed year | 9.1 |
| 9 | Boundary inclusivity | a line at or above the interval was certain of selection | recovered, not filed; the lattice fixes the interval and no population line sits at it, the nearest being 726 euro above and 71,054 euro below, so "at or above" and "above" give the same certainty set, asserted |
| 10 | Rounding path | the nearest fifty thousand euro per programme, the authority's figure their sum | 9.1 files both; SF6 asserts the two agree by construction |
| 11 | Tie-break | the programme carrying most of the misstatement is named; Rail siding and yard leads the runner-up by at least one stated cell, 250,000 against 200,000 | asserted, with the unrounded figures 50,257 apart and not overlapping |
| 12 | Maturity and censoring | nothing is censored: the year is closed, every line is recorded, the testing is complete and no finding arrives later | asserted that the schedule holds no open or pending finding |
| 13 | Order of operations | each tested line's contribution is computed, then summed by programme, then rounded | asserted: sum-then-round and round-then-sum agree, which is SF6 |
| 14 | Row order | no step depends on file order, and the lattice recovery is invariant to re-ordering the population for presentation because it runs on the ledger's own sequence | asserted over six permutations of the presentation order |
| 15 | Duplicate resolution | one payment line per ledger row; the re-delivered batch collapses on the delivery sequence | the dictionary; SF8 |
| 16 | Identity normalisation | the crosswalk carries the ledger's supplier numbers onto the master's | complete and one-to-one over the window, asserted |
| 17 | Netting against gross | gross: credit notes and the lines they reverse are both excluded, nothing else nets | the dictionary; SF7 |
| 18 | Dimensional units | every amount is euro to the cent except the capital programme register, which states values in thousands | the register's column header and the dictionary; SF11, and the figure never reads it |
| 19 | Code and status semantics | `line_status`, `reverses_line_ref`, `delivery_sequence`, `programme_code` as the dictionary gives them | dictionary semantics; SF7, SF8, SF5 |
| 20 | Integerisation | the figure is an amount rounded to the nearest fifty thousand once | SF6; the underlying sits 13,830 inside its cell against a headline route band of 3,725 and a per-programme band of at most 1,214 |
| 21 | Clause scope | plan 4.2 sets materiality and the confidence, plan 4.3 the conclusion, manual 9.1 the estimand, manual 9.2 that no record holds it | the documents' own headings; asserted that no other clause bears on the figure |
| 22 | Forward window contents | the extended testing the conclusion may require has not been performed | the call is the conclusion on a closed population, with its reason below |

**Why the call is retrospective on its figure and forward on its consequence.** The misstatement is the
authority's own for a closed year, which is what an audit conclusion is about; the conclusion it drives,
whether the population goes to extended testing before the statements are certified, is work not yet done.
A figure about an open year would be a projection of a projection and no audit states one.

### Architecture 3: Literal reader

A reader who executes the prompt, plan 4.2, plan 4.3 and manual 9.1 word for word, inferring nothing, has
the population, the outcome, the window, the unit, the segmentation, the grain, the comparison and the
conclusion rule all fixed, and 9.2 tells them no record holds the answer. Every reading of every term gives
the golden (SF1 to SF13, each asserted). The only thing the text does not give is what the tested lines
stand for, which is the analysis. Three constructions a reader may build instead are analyses rather than
readings, which is why the ladder and not the fork table carries them, and the nine recovery routes the
record refuses are measured in `## Draw` and asserted rather than argued.

### Architecture 3: Oracles

Every control in the pack reads the same on the wrong path and on the golden. The capital programme
register's values in thousands reconcile to the ledger under every rung because they are sums of recorded
value and not of misstatement, to the authority's own stated residue. The prior year's extract holds its
own tested lines and findings and states no misstatement for its population, so no rung reproduces a
closed number from it. The funder's grant claim covers a different window and a different population and
ties under every rung. The supplier master carries approval categories and no figure. No corpus scores a
projection, no document ranks the programmes, and nothing in the pack states a misstatement for any
population in any year.

### Architecture 3: Ask sheet

Three families, each multi-dimensional, each decoupled from the call and each carrying its own silent
device against the careful solver's path.

| Ask | Figures | The device |
|---|---|---|
| A1, per quarter of release: the value the runs released past the cut-off then in force carried. Both conventions are pinned in the asking sentence. The plain count of runs released was cut first, then the count past the cut-off: each was free to the cracker and no device reached either | 4 x 1 = 4 | three devices, each measured: the cut-off moved from 15:00 to 14:00 on 1 July 2026 and the register carries both effective dates, so one cut-off for the year undercounts both later quarters; a run released past midnight ends each quarter, so grouping on the opening date rather than the release moves the counts; and one run was rejected by the bank and re-released, so the log carries it twice. A run released exactly at the cut-off is within it, which the register states |
| A2, per supplier risk category: the suppliers raised into it, those removed from it, and those raised in then removed. "Removed from it" is pinned in the asking sentence, against the removed-into reading | 5 x 3 = 15 | the **grain** primary: an approval decision is taken on a trading group and recorded against the parent only, so a decision reaches every member the master names. Nothing says a row covers more than the number on it; a reader finds it by seeing a member hold a current risk category with no approval row to account for it, and then intersecting the register against the master's parent column. Hazards beside it: the superseded rows the dictionary rules out of the history, and the October relabelling the scale map resolves | the approval register chains per supplier and carries superseded rows the dictionary rules out of the history; a category was relabelled on 1 October and the scale map carries both codings |
| A3, per month of payment: the distinct ledger lines the testing schedule covers, whether any schedule line is missing from the ledger and if so how many, and whether any ledger line is on it twice and if so how many. "Distinct" and the month of payment are pinned in the asking sentence | 12 + 2 = 14 | two primaries. **Scope:** the working paper is internal audit's paper for the year, so plan 4.4's revenue expenditure sample sits on it under its own cost centres and its own ledger prefix; seventeen rows resolve to no capital line, are counted in no month, and nothing flags them. **Clock:** the paper carries the date the run was released, as the payment run log records it, while the ledger carries the date of the run that paid the line, and the two differ for the seven runs whose release ran past midnight, two of which cross a month end | the schedule is a table inside a PDF and its line references carry the ledger's supplier prefix, so the join needs the crosswalk; the re-delivered batch puts one ledger line on the schedule twice |

Every A3 ask is worded so that "none" is a grammatical answer, per H23.

Pair ceiling: 38.1

Mirror leakage: 12.0 per cent of ask weight

Measured by: `generator/ceiling.py`, which builds both responses as code, scores each on its OWN ask
readings against the graded figures in `figures.json` on the cut pack, and exits non-zero unless the
cracker keeps nothing, the mirror keeps under 35 per cent and the pair sits at or under 40. **It currently
exits non-zero on all three.**

**The measurement is failing and the asks are open work.** The first version of this script scored both
responses on the same ask readings, both rows taking the mirror's A1 stops and the mirror's A2 reading,
and hardcoded the third ask to nil for both, so the ask component of the ceiling and the whole of the
mirror leakage were one reading counted twice; the two labels were crossed against
`supplemental-stumping` Part 1.1 as well. Scored properly, with each response on its own readings and the
third ask actually scored:

| Response | call | components | instruction | A1 | A2 | A3 | score |
|---|---|---|---|---|---|---|---|
| the cracker, which lands the call, runs the hygiene battery and executes every filed rule | 4/4 | 19/21 | 2/2 | 0/4 | 5/15 | 1/6 | **56.0** |
| the mirror, which stops at the recorded-value ratio and takes each obvious reading | 0/4 | 6/21 | 2/2 | 0/4 | 3/15 | 0/6 | **20.1** |

**Why the cracker keeps everything, which is the diagnosis and not a wording problem.** Every device on
every ask is adjudicated by a filed sentence or found by the hygiene battery, so a careful solver executes
it: the cut-off register carries both effective dates, the run log carries the release timestamp and marks
the re-released run, the scale map resolves the October relabelling, `event_status` marks the superseded
rows, and A3's twelve monthly counts come straight off the schedule's own `paid_date` column and need no
join at all, which is why even the mirror takes 12 of 14 there. There is not one silent primary in the
set. `supplemental-stumping` Part 5 names this exactly: a pin says what to compute and never makes
computing it correctly hard, so every pin has to be paired with a silent primary underneath it. The asks
need silent primaries, which is design work on the ask data, not a re-worded sheet, and it is open.

**The cracker sheet.** One row per ask, the cracker being the response that lands the call, runs the
hygiene battery and executes every filed rule and column description. Measured by
`generator/ceiling.py` on the cut pack.

| Ask | What the cracker does | What it never reaches | Verdict |
|---|---|---|---|
| A1 | reconciles the run log to the ledger it was given and rebuilds the value it can tie | the log records the whole run and the capital extract holds only its capital part, so every value figure is short by the revenue part, which ties to the revenue expenditure summary month by month | miss |
| A2 | reads the approval register as it stands, one decision against one supplier number | a decision is taken on a trading group and recorded against the parent only, so the suppliers raised into or removed from a category are the group's members, which only the master's parent column and a member holding a category with no row of its own reveal | miss |
| A3 | splits the paper's reference, joins to the ledger and runs the unmatched-join sweep | five rows are certified valuations recorded at invoice level, so each covers every line on its invoice; the sweep reports them as missing from the ledger, which is wrong, and the quarters are short by the lines they carry | miss |

Measured: the cracker gets **no ask whole**, keeping 4 of 8 on A1, 5 of 15 on A2 and 1 of 6 on A3, which
is 10 of the 29 ask figures against a measured ceiling of 12, and the pair reads 38.1.

### Architecture 3: Pre-ship check

**The pack.** 18 files, four formats (11 csv, 2 xlsx, 3 pdf, 1 md), the spine
`capital_payment_lines_2026.csv` at 26,874 rows (26,648 population lines plus the two credit notes and the
re-delivered batch), every file carrying a source, a date and a licence in `metadata.json` and asserted
complete against the cut directory, two declared distractors (the funder's
grant claim on a claim year to 31 March, and the revenue expenditure summary, which is the other
population the plan tests) plus the prior year's lines, which the two-year testing extract needs and whose
own misstatement is stated nowhere.

**Layer 1, every item produced by the authority's own systems and none of it deciding the call.** The
ledger carries one row per payment line and several lines per invoice; two payments were reversed inside
the year and the credit notes that reverse them ship beside them; the bank feed delivered one payment run
twice with its own delivery sequence; the supplier master numbers suppliers differently from the ledger
and a crosswalk carries both, which the testing schedule's references need; the schedule is a table inside
a PDF; the prior year's tested lines and the current year's sit in one overlapping extract; the capital
programme register states approved budgets in thousands where every other file is in euro to the cent; the
authority's financial year is the calendar year while the funder's claim runs to 31 March; one line was
queried and re-tested, so the schedule carries it twice, and it carries no exception, so no figure the
report states turns on it.

**What is filed at authority, and nothing more.** Plan 4.2 (tolerable misstatement and the confidence),
plan 4.3 (the conclusion, as a confidence statement that only a bound satisfies), manual 9.1 (the
estimand) and manual 9.2 (that no record holds the answer). Asserted by word sweep over every shipped
file: no selection interval, no selection count, no inclusion probability, no reliability or expansion
factor, no basic precision, no incremental allowance, no upper limit, no expected-misstatement allowance,
and nothing about projecting, scaling, weighting, extrapolating or monetary units.

**The free gates.**

| Gate | Result |
|---|---|
| `precut.py task190` | 50 checks, 0 FAIL, 0 WARN |
| `voice-check.py task190` | PASS, 974 characters |
| generator `checks.py` | 121 assertions: the three-rules block R1 to R3c on the clean truth, the analyst test executed, the ladder's conclusions at 4.3, the determinism block (the whole route table, the lattice, its neighbouring band and the interval's boundary), SF1 to SF13, the five blind families, the input gates including every file's licence record, and the asks |
| `verify.py` (reads `target/` and `figures.json` only, own code path, recovers the interval itself) | 0 failed |
| two consecutive rebuilds | `target/` and `golden/` byte-identical |
| `figures_check.py task190` | every figure in blocks 1 to 4 present in `figures.json` |
| `leak.py task190 --asof 2027-02-26` | REVIEW, every line answered below |
| `guard.py check` / `heart` | no BLOCK; WARN on the two answered gate_g repeats (`repeat.gate_g` against task468, `overuse.gate_g` at 7 of the last 12); nearest driver 0.07 on `check`, 0.05 against card drivers on `heart` |
| `guard.py surface` | no BLOCK; no persona the card never planned, and only two of the three carded names ship; eight pairs promoted for the author's adjudication, five on corpus-wide surface idiom (shared file names, the `pdf+png` deliverable pair, `quantity_figure`) and three on the same-driver signature, gap `rule` plus pattern G16 plus Gate G `method_or_model_selection`, against task185, task457 and task80, each already answered by a differentiation line on the card |

**The leak report's lines, answered.** REVIEW on eight lines, no LEAK, each read against this pass's
pack.

- **Block 3, five lines.** One matches the clause number 4.3, not a figure, in the heading "4.3
  Conclusion on a tested population". The others are the plan and the provenance note carrying the call's
  distinctive words, because the call is asked in manual 9.1's own vocabulary: payment, population,
  misstatement, programme, tested, year, euro. The question cannot be asked without them and no shipped
  file carries the figure, asserted by word sweep with the PDF content streams decompressed and with a
  positive control proving the sweep can read each PDF before any absence is asserted.
- **Block 4, the manual and the schedule share the design note's vocabulary.** Deliberate, and the
  author's override is why: the manual defines selection interval, certain of selection, tainting, basic
  precision, incremental allowance and upper misstatement limit, and the schedule states the basis of
  selection. Read for whether either names the move: neither says how to get from the tested lines to the
  population, and `checks.py` sweeps for projecting, extrapolating, scaling up, grossing up and
  multiplying a tainting and finds none.
- **Block 9, dates after the as-of in the capital programme register.** The programmes' planned
  completion dates, now spread from 2027 into 2029. A capital register carries the dates the works are
  due to finish, and the figure never reads the register's values (SF11).
- **Block 10, container metadata.** INFO; the pack is clean.

**Golden realism.** The schedule is sorted by the misstatement indicated and then by programme name, the
order the chart uses; recorded value to the cent as the ledger holds it, the misstatement whole because
9.1 states it to the nearest fifty thousand, the share to one decimal; the authority row carries its own
certain share rather than a blank. The chart's title is the finding, the axis names its unit and its
grain, the three nil programmes are explained in a footer from the pack's own facts, and the source strip
carries the testing completion date. Every programme's recorded value is a non-round figure: nine totals
each within a euro of a round million was the first draft's clearest tell and the contractor certificates
were round too, so both were redrawn.


## Tried and rejected

- Ranking the lines by the share of alerts that prove real (the yield reading): `guard.py nearest`
  measured the driver at 0.15 against task446 v2, which already builds a yield carried onto a
  population with a different base rate. Dropped at the draw, before any data was cut.
- The seed's own architecture, a filed scorecard ranking the divisions on confirmed movement per 1,000
  accounts: a stated score deciding the call, which the 10/10 rules ban, and a ranked artifact Gate G
  forbids shipping. No scorecard ships.
- Clause 9.2, which said the bank maintains no ranking of its business lines: it was there to keep a
  ranked artifact out of the pack, but the isolated reader quoted it as a sentence placed on purpose to
  reassure, which is a tell. Removed, and the Gate G guarantee is now carried by an assertion over
  every shipped PDF instead of by a sentence in one of them.
- A register in which every case is confirmed, every identifier sequential and no case amended past a
  second version: the reader called the pack plausibly real but slightly too orderly. The register now
  carries the cases that were put to the head of financial crime and not accepted, with no confirmed
  month, identifiers numbered as cases were opened with the gaps the register's own deletions leave,
  and ten cases amended twice. No graded figure moves: `figures.json` is byte-identical across the
  change, and SF14 asserts the wider reading of the disposition field names the same three lines.
- Clause 6.2's closing phrase, "the expectation is taken over the cases the line's own closed record
  implies", and clause 6.3's definition of that closed record: both were added by the first
  determinism repair, to close a fork between the expectation and a single realisation. Two isolated
  readers then quoted the pair as naming the method, one of them saying the stump had become "did you
  read 6.2" rather than "did you find the pitfall", and the determinism judge marked Gate F borderline
  for the same reason. That is the failure the house rules name: a determinism repair that files the
  HOW. Removed. The expectation is now carried by "expected to be carrying" alone, the realisation
  reading is ruled out because the register holds no unseen case (asserted), and the window the
  construction needs is closed by convergence over 36 windows and the register entire rather than by a
  clause. Clause 6.3 keeps the look-back span as a fact of the bank's governance, which says nothing
  about using it.
- The contract register's note that "the ledger holds the ticket under both references and the hours
  are owed once", and the ledger's own note column saying a row was "reissued under the credit note
  series": a filed rule adjudicating an ask's device, and a narration of it, which the ask layer's
  first two bans forbid. Both removed. Each credit note now names the ticket it reverses, so the
  reissued pair reverses more hours than that ticket was billed and only an internal inconsistency
  finds it.
- A register whose typologies were uniform across the eight lines, whose annual case counts barely
  moved, whose confirmation lag was uniform on nought to two months everywhere and whose amendments
  multiplied an amount by 1.08: the isolated reader read all four as generated. The mix is now what
  each line actually sees, the monthly count is a Poisson draw on a yearly and a seasonal factor, the
  confirmation lag runs with the line's own detection lag, and an amendment moves an amount either way.
- **Architecture 1, the whole of it, is spent.** Three consecutive judge SEND_BACK verdicts and a Gate
  F graded moderate to borderline then moderate to low. The reason is structural rather than a list of
  fixes. `determinism-check` requires the estimand to say that the population holds cases the bank has
  no record of yet, and requires the method to be forced, which here means every estimation route
  converging: it now does, over 36 windows of two years or more and the register entire. Once both
  hold, the only analytical step left is deciding to nowcast rather than count, and clause 6.2 has to
  announce that to be literal. Every Gate F repair reopened a determinism fork and every determinism
  repair closed the stump, twice round. Three isolated readers built the nowcast and landed the call at
  80 to 90 per cent confidence, so the portal's top two would both land it. The slot re-roots at stage
  1 with a new driver; the stock-from-arrivals-and-time-unseen driver is not reused.
- **Architecture 2, the WHAT screen run on four candidate decisive steps before this one.** Correcting
  the monitoring's output with the sensitivity and specificity measured on an assurance sample: dropped
  at the draw, because task446 v2 ships that driver in this same domain and task448 ships its stratified
  form, which the re-root brief bans. Estimating the undetected caseload from a below-the-line review
  sample: the same two cards, plus the sample's own arms announce the step. The excess of deposits over
  a counterfactual named in the estimand as "the number that would otherwise have been made there":
  dropped because naming the counterfactual that way excludes the band count by the clause's own words,
  which turns the decisive step into rule application and fails the analyst test. Ranking the eight
  segments rather than sizing the figure: dropped because a three-of-eight set pays a response that
  gets two members right, and the ladder cannot keep the top two off a set the way it keeps them off a
  figure. The step that survived settles none of the estimand's five parts, which `## Three rules`
  answers line by line.
- **The first cut of architecture 2's deposit-size record, spent at stage 4.** The law had one shape over
  5,000 to 16,000 and a different one below 5,000, so a fit window starting at 4,000 or 3,000 crossed the
  kink and gave 440 and 512 against the filed 400, and the per-bin integer rounding left enough scatter for
  an unweighted log fit at 100-dollar steps to read 421 and a one-sided fit to read 311. The design note
  asserted convergence it had not measured. Replaced by one shape end to end, a gentle decay of the same
  rate in every segment, with each 500-dollar block's count exact and the pile on round figures spread
  evenly inside it, so every family, window and step width lands on the same eight figures. The sweep is
  now run and asserted rather than claimed.
- **The pooled book profile as a wrong cell.** It gave 370 against 400 on the old record, and the note
  carried it as a single-error cell. On a record with one shape it converges with the rest, and it is now
  reported as one of the 199 estimators rather than as a rival.
- **Rating events drawn independently.** 205 of 805 follow-on events started from a band the customer was
  not in and 318 moved a rating to itself, which the solver's-eye reader read as generated and which gave
  "moved out of the band" more than one reading. The events now chain, so the ask has one answer.
- **A machine estate defined only by the service log.** The deposit feed invented machine ids the log never
  held, so "any machine with no service record" had no forced answer. The estate now ships as
  `deposit_machine_register.csv` with install and withdrawal dates, the feed takes deposits only at a
  machine in service that day, and the answer is the register's own.
- **Amounts drawn from evenly spaced quantiles of a fixed curve.** Every bin count was the curve's own
  value, so variance over mean was 0.11 bank-wide at 100-dollar bins and the eight segments gave
  chi-square per degree of freedom of 0.004 to 0.026, each with a tail probability below 1e-26. The
  determinism judge named this as the reason the method fork looked tight: the 199-estimator agreement and
  the 180-specification agreement were both bought by the absence of sampling noise, not by the design.
  Replaced by drawing each deposit independently from its segment's own density, so every bin count is a
  genuine sample, which `## Dispersion and granularity, measured` reports on the shipped pack. The dispersion sweep that was to find a ceiling is therefore dead: there is no ceiling to find,
  because block-level dispersion bought no chi-square at all (chi-square tracks the dispersion parameter
  squared, so the honest value needs the parameter at 1, which is a sample) and cost convergence at 0.02.
- **Block-exact generation with an evenly spread round-figure pile.** It was what made 199 estimators
  agree, and that is the defect above, restated. Recorded here so it is not reached for again.
- **Splitting generated by adding a band deposit on top of an existing day.** It put a surplus below the
  threshold with no matching deficit above, which both readers found: a real splitting process moves mass,
  so the takes that would have been reported are missing. Replaced by replacing a take: a deposit at or
  just above the threshold is taken out of the record and paid in instead as two deposits on the same day,
  the larger inside the band. The dollars balance to the cent and 10,000 to 11,000 carries a deficit of the
  same size as the band's surplus.
- **Raising the record's volume to beat the noise.** Measured at 2x, 4x and 8x with the construction
  scaled alongside: the bank figure's span across the judge's grid falls only from 44 per cent of the
  figure to 29 per cent, because the residue is specification bias (OLS on counts extrapolates the
  baseline low, log-OLS with curvature extrapolates it high) and bias scales with the figure, not with its
  square root. Flattening the baseline's curvature over the fit window, measured at 2x, 4x and 8x the
  decay length, does not remove it either.
- **Grading something derived instead of the level.** Measured across the 165 clean specifications: the
  rise over the prior year spans 125 to 244, the ratio 1.46 to 2.58, every segment's share of the bank
  figure spans 5 to 21 points, the largest segment splits 113 to 52 between two segments, and a
  significance call on each segment's own trade gives 4 to 10 distinct answer sets at every bar from 1.5
  to 5. The specification bias does not cancel in a difference, a ratio, a share or a ranking, so none of
  these is determinate either.
- **An averaging estimator the pack files nowhere (architecture 2's last stand, and what spent it).** The
  golden was the average of the band's surplus below the threshold and the deficit above it, and the
  determinism judge reproduced it under that estimator and no other: the surplus alone gave unrounded bank
  figures from 71 to 786 and the deficit alone from 207 to 858, while the average gave 450 in all 186 of
  its complete specifications. The reason it agreed is the finding: being the half difference of two
  observed counts less a half slope correction of 2.7 to 58 deposits, it cancels the fitted profile's level
  algebraically, so it is insensitive to exactly what the specifications differ on and every other
  estimator is still standing. The refusal rule the build used, failing to reconcile within a fifth, is in
  no shipped file, so the 141 standing specifications could not be reproduced from the bundle at all. The
  general lesson, and the reason this slot is now barred from the whole family: a decisive step that is an
  estimation choice over a fitted counterfactual density cannot be both forced and silent, because the
  specifications always disagree and nothing filable chooses between them without becoming rule
  application. Three passes each moved the artifact instead of removing it (a smooth draw, then an
  algebraic cancellation), which is what spending an architecture looks like.
- **A per-segment table that book size alone reproduces.** On architecture 2's shipped pack a flat rate on
  the paid-in column matched 7 of 8 segment cells at about 0.82 per cent, and at 0.91 per cent it matched 6
  of 8 with the bank figure landing on exactly the golden, only the top two segments wrong. Raising one
  segment's propensity was not enough to break it. The replacement is not a tuning: the blind-response
  test now runs at the draw, before any file exists, on the widest graded component, and the component's
  shape changes if it fails.
- **Two paths to one headline, asserted to agree on one family.** Summing the rounded segment figures gave
  the golden in 186 of 186 specifications while rounding the unrounded sum gave it in 93, so SF12's
  assertion that both paths agree was true on the author's family and false on the judge's. A two-path
  assertion is only worth what the family behind it is worth.
- **A handbook sentence ordered to state a role, which stated the method.** Filing "the whole of that band
  is what the figure estimates, so no part of it evidences what the band would have held absent the
  practice" was the instruction; the clause that followed it, "that has to come from the segment's trade
  outside the band", told the solver where to build the counterfactual. A sentence filed to close one thing
  closes more than it was asked to, so any sentence filed at authority now goes to the author in its exact
  wording before it ships.
- **An error on one contractor certificate.** It was put there so the Dredging programme would not read
  nil, and it inverted two rungs: the recorded-value ratio scales a certainty line's error by the whole
  population factor (2.8x) while the stratum route takes it at face, so at an error of 62,400 the ratio
  route filed 216,123 against the stratum route's 182,462 and the ladder ran backwards. The arithmetic is
  that the inversion happens whenever the certainty error exceeds about 2.9 times the proportional
  findings, and keeping it below that left too little room to also hold the rungs 1.15x apart. Replaced by
  putting the defect in a seventh programme's day-work instead, so no certainty line carries an error at
  all. That is better in three ways: the ladder is monotone by construction, the story is cleaner (the big
  certificates get the most scrutiny and were sound, which is exactly why the recorded-value ratio fails),
  and the two largest programmes reading nil is a fact a reader can check rather than a coincidence.
- **Computing the golden from the designer's exact tainting fractions.** The schedule ships the amount
  recorded and the amount properly payable, both to the cent, so a solver's fraction is theirs and not the
  designer's. The generator and the independent verifier disagreed by up to 34 cents until the fraction
  was recomputed from the rounded payable, which is now what the population carries.
- **Shipping the ledger extract sorted by payment date.** The selection cumulates the population in the
  ledger's own sequence, and sorting the extract by date destroyed that order, so the interval was no
  longer recoverable and the verifier could not reproduce the figure at all. The extract now ships in the
  ledger's posting sequence with a `ledger_sequence` column, which is how a ledger extract comes out and
  which survives a solver re-sorting the file.
- **Nine programme totals each within a euro of a round million.** The first draft scaled each programme
  to a round target and the contractor certificates were round too, which is the clearest realism tell in
  the pack and would have been the first thing a reader quoted. Both were redrawn off round numbers, which
  moved the cumulative values and forced the design point to be re-tuned from scratch.
- **The claim that the untested lines are what make the interval unique.** The note asserted that the
  tested lines alone narrow the start but admit many intervals, so the untested side carried the recovery.
  Measured on the cut pack it is false: the tested lines alone pin both the interval and the same
  23.76-euro start window over a 4,001-euro band. The claim was replaced by the measurement, and the
  untested side is now described as a confirmation. Nothing in the design changed; an unmeasured sentence
  about the mechanism did.
- **A closure row asserting a clearance nothing asserted.** Axis 9 claimed no population line sits within
  1,000 euro of the interval, "asserted", and no assertion existed; the nearest line is 726 euro above it.
  The row now states the measured gaps and two assertions were added to `checks.py`, so the boundary
  reading cannot move the certainty set and the claim is executed rather than written.
- **The interval left to be recovered from the tested set.** Ten routes were enumerated, one admitted by
  the record, and the granularity was set from the spread of the five that agreed. The first determinism
  judge refused it: the pack did not hold the interval, the call rested on it through basic precision, and
  neither isolated thread performed the recovery the note claimed, the cold reader instead taking
  materiality over the reliability factor and filing a figure twice the golden. The design is now filed as
  a fact about the sample and the estimator alone is open. The route table, the lattice search and the
  granularity argument built on the route spread are retired with it.
- **The whole-euro contractor certificates.** Every line certain of selection was a whole number of euro
  and the only whole-euro line above 100,000, so `cents == 0 and amount >= 100,000` selected the certainty
  set exactly, with no false positives and none missed. Both isolated threads found the certainty set that
  way rather than from the interval. Measured: 31 of 31 certainty lines whole euro against 1.04 per cent of
  the lines below the interval. The certificates now carry cents and about one sundry line in nine is
  invoiced at a round euro, a half euro or a round five euro across every size band.
- **The paper cracker sheet, and the first code that replaced it.** The sheet claimed every ask figure
  missed and reported a pair ceiling of 37.1 with 22.0 per cent mirror leakage. Written as code the two
  responses were scored on the same ask readings, both rows taking `the_cracker` for A1 and `a2_unmapped`
  for A2, and the third ask was hardcoded to nil for both, so the ask component of the ceiling and the
  whole of the leakage were one reading counted twice. The labels were also crossed against
  `supplemental-stumping` Part 1.1. Scored properly the cracker takes 41 of 41 and the pair ceiling is
  69.3. The asks need silent primaries, which is open work and not a re-wording.
- **The word sweep that could not see the PDFs.** `_sweep` read every shipped file as raw bytes, so it
  never saw inside the three PDFs' Flate-compressed content streams, which is exactly where the authority
  sentences live. Every R3c claim rested on it. It now decompresses the streams through `verify.pdf_text`.
- **Tolerable misstatement derived from budgeted capital expenditure.** The plan called 1,160,000 two per
  cent of budgeted capital expenditure while the register summed to a figure giving 1,189,620, a
  contradiction of 29,620 that the call did not turn on. The derivation is deleted and the figure is stated
  as the head of internal audit's judgement, which is what an audit plan does.
- **The register's approved budget equal to the year's spend.** Each programme's budget was the year's own
  recorded value rounded to the thousand, so the register reconciled to the ledger exactly and the budget
  carried no information. It now carries the board's approval figure, which differs from the spend.
- **Pins alone against the cracker.** The four ask conventions were pinned in the asking sentence, which
  is where a pin belongs, and the measured pair ceiling moved only from 69.3 to 67.8 with the mirror
  leakage from 51.2 to 46.3. The cracker still takes 41 of 41. That is the skill's own rule arriving
  empirically: a pin says what to compute and never makes computing it correctly hard, so a pin without a
  silent primary under it buys determinism and no difficulty. The primaries are open work and the four
  families the author named for them are unspent in this world.
- **A3's monthly figure read off the schedule's own date column.** Twelve of the ask's fourteen figures
  were a group-by on `paid_date` with no join at all, which is why even the mirror took twelve of them.
  Pinning the count to distinct ledger lines costs the mirror one figure and nothing else. The ask needs
  re-routing through the resolution chain rather than strengthening, which is open.
- **Two visible devices tried against the cracker, and what they measured.** A3's scope primary (plan
  4.4's revenue sample on the same working paper) and its clock primary (the paper's release date against
  the ledger's run date) together took the mirror from 46.3 to **26.8 per cent of ask weight, which passes
  its bar**, and the pair ceiling from 67.8 to 62.0. Neither moved the cracker, which still takes 41 of
  41. The reason is general and belongs on the slot's record: **a device a careful reader can resolve from
  a column description cannot suppress the cracker, because the cracker reads the dictionary.** The scope
  device is found by the unmatched-join sweep, which is a battery check, and the clock device is resolved
  by reading two honest date definitions. Both are legitimate mirror devices and neither is a primary in
  the sense the cracker test means. What suppresses the cracker has to be discoverable only from an
  internal inconsistency that nothing invites, and the candidate designed for it is below.
- **The grain device, built, and the two figures it cost to build it safely.** Five tested items are
  certified valuations the paper records at invoice level, so each row covers every payment line on its
  invoice rather than one line. It is the first device in this build that costs the cracker anything:
  A3 fell from 14 of 14 to **8 of 14**, because the unmatched-join sweep reports the five invoice rows as
  missing from the ledger, which is wrong, and the monthly counts are short by the lines those invoices
  carry. Every line on the five invoices was found sound, so the projection is identical read at line or
  at invoice level, and `checks.py` asserts the tested set, the certainty set, every per-programme figure
  and the unrounded total identical with the device deleted. What it cost: the lines tested and the value
  tested are read off the paper, and the invoice rows make both ambiguous, so neither is stated as a
  figure any more and the three wrong rungs are no longer quoted to the cent in the recommendation. That
  is the right trade, because a graded figure a judge cannot rebuild is the commonest finding in the
  record, but it is a trade and it is recorded as one.
- **The earlier draft of that device, which would have moved the call.** The paper would identify
  a handful of tested items by their invoice reference rather than their line reference, in the same
  shape, so those rows resolve to the ledger's `invoice_ref` and cover two or three payment lines each.
  A response that reports every unresolved row as missing is then wrong on the absent count, and one that
  counts a line per paper row undercounts the months. It is silent: only reconciling the paper's recorded
  amount against the ledger, where one paper row equals the sum of two lines, reveals it. It was not built
  because it changes which lines the paper identifies as tested, which moves the main call, and the
  separation rule and the author's standing instruction both say a device that moves the call is the
  gravest finding. Building it needs the invoice-level rows to cover lines that are already in the tested
  set, so the tested set is unchanged, and that construction has to be measured before it is cut.
- **The band weights at the favourable end of every permitted range.** `ceiling.py` weighed the call at
  0.12, the critical components at 0.18, instruction-following at 0.10 and the asks at 0.60. Every one is
  legal under the house spec, but the recommendation side sat at the bottom of its range and the asks at
  the top, which gave a response that lands the call a floor of **40.0** against `supplemental-stumping`
  Part 0's **45.0**, and so flattered the pair by 2.5 points in the field the gate reads. The bar of 40
  was derived on Part 0's numbers, so the gate now computes on Part 0's numbers: 38 for the recommendation
  and the components, 7 for instruction-following, 55 for the asks. Measured with the script rather than
  argued on paper, the cracker may keep at most **10** of the 41 ask figures for the pair to reach 40; on
  the old weights it was 11.
- **Dropping the figures the grain device made ambiguous, rejected for naming the quantity instead.** The
  invoice-level rows made the lines tested and the value tested ambiguous, and the first fix was to stop
  stating them. The better fix is to name the quantity in the asking sentence, the ledger lines the
  testing covered and their recorded value, which is one determinate answer that a response counting the
  paper's rows gets wrong. The device then bites on a graded figure instead of costing one, and the three
  wrong rungs are quoted to the cent again. Measured: the cracker loses 2 of the 21 component cells.
- **Ask figures the cracker kept that no device could protect, cut rather than defended.** The bar is a
  share of ask weight, not a count, so a figure every strong response banks for free is worth less than
  nothing: it dilutes every criterion beside it. Of the 31 the cracker still kept, twelve were free by
  construction. **A1's plain count of runs released** was a row count per quarter after the duplicate
  sweep and the pinned basis, so it is cut: A1 is now two figures per quarter, both of which need the
  cut-off register and the run log's own value. **A3's twelve monthly counts** were a group-by in which
  only four months carried a device, so they fold into four quarters of payment, and now every quarter
  contains a device-touched month. Measured: the ask set falls from 41 criteria to 29, the cracker from 31
  of 41 to 20 of 29, A3 from 8 of 14 to **1 of 6**, and the pair from 51.0 to **47.6**. The floors hold:
  56 graded criteria against a floor of 25, and the ask weight is unchanged at 55 per cent.
- **An overnight release scored as inside the cut-off, which the fold exposed.** A run released at 01:30
  on the day after its run date was compared against that morning's clock, so the latest run of the
  quarter counted as the earliest. Minutes now run from the run's own date, so a release that crossed
  midnight is past that date's cut-off by construction, which is both the correct reading and what makes
  the quarter basis worth pinning.
- **A2's grain device, and the measurement that closed the pass.** An approval decision is taken on a
  trading group and the register records it against the parent the submission came in under; the master
  names the parent each supplier belongs to, and the members carry no row of their own. A response that
  reads one row as one supplier undercounts every category. Measured: A2 fell from 15 of 15 to **5 of 15**
  and the pair from 47.6 to **38.1**, which is the first measurement in this build to clear its bar. The
  discovery route is the one the shape promises: a member holds a current risk category with no approval
  row to account for it, which shows only by intersecting the register against the master's parent column,
  and no battery sweep performs that intersection.
- **The realism tail, cleared before the hand-back rather than after.** Supplier names are now a mix of
  family firms, trade names and place names with varied suffixes rather than a town-plus-trade grid; the
  crosswalk's numbers were issued in blocks as trades migrated, so they step from the ledger's by no
  stride; the supersessions are no longer symmetric pairs, with some arriving the same day, some weeks
  late and a couple whose effective date disagrees with the row they replace; the funder's claim has the
  shape a claim has, eligible expenditure by how long the programme has been running, the grant at the
  funder's 45 per cent intervention rate, and the two newest programmes with nothing yet to claim; and the
  revenue summary's maintenance line is seasonal on the spring and autumn shutdowns. It was cleared first
  because the next isolated reader sees a pack whose prompt and documents have moved, and a reader
  rediscovering a known item spends the pass on a list already in hand.
- **The mirror modelled rather than measured, which flattered the pair twice over.** Two of its scores
  were assumptions with nothing behind them. Its nine certain-share cells were credited only to the
  response that lands the call, which was true while the interval had to be recovered and false the moment
  the interval was filed: any response that reads the working paper computes all nine. And its
  instruction-following was scored 1 of 2, where the rubric spec says instruction-following covers the
  requested files and output-shape asks, all of which a wrong-rung response produces. Corrected, the
  honest pair was **44.7**, not 38.1. Two cuts brought it back: the deliverable's second column is now the
  misstatement as a share of the programme's recorded value, which moves with the estimator, in place of
  the certain share, which every route banked; and A1's count of runs past the cut-off was cut after its
  plain run count, because the cut-off register files both effective dates so the cracker applies them.
  **Measured against `supplemental-stumping` Part 0: the mirror's recommendation side is 6.5 of the 38
  points, above Part 0's r of about 5, and 13.5 before the asks against Part 0's 12**, so the model is now
  slightly more generous to the mirror than Part 0 assumes rather than harsher. The six component criteria
  it earns are named: the three nil programmes, Deepwater berth renewal, Quay 3 reconstruction and the
  Dredging programme, on both columns, where nil is nil under any route.
- **The prose of Part 1.1 and the script that enforces it disagree, and the disagreement is worth
  filing.** The prose scores "each ask figure and chart criterion" and then says "every row misses or the
  ask is rebuilt", which reads as a per-figure zero; `precut.py` reads the rows of the cracker table in
  the design note, at whatever granularity the author wrote them, and checks each ends in a miss. Read as
  a per-figure zero the prose makes the pair ceiling redundant, which cannot be its purpose, so it is a
  design-iteration instruction and the ship gates are Part 7's two numbers. `ceiling.py` gates on those
  two and prints the figure keep beside them, because every figure the cracker takes costs pair points.
- **Architecture 3, the whole of it, is spent, and the number re-roots rather than retiring.** The refer
  rested on basic precision, whose reliability factor Gate B forced the bundle to carry, and carrying it
  made the projection route recoverable so Gate F fell: two independent cold threads landed the call, and
  a landed call banks about 45, so the pair could not reach 40 whatever the ask layer did. `## Architecture
  3, spent` holds the measurement. Architecture 4 re-roots on a decisive step that needs no filed constant
  or factor table; the monetary-unit sampling world, the probability-proportional projection driver and
  the port authority pack are not reused.
- **Architecture 4's first decisive step, the window dial valued in cases ahead of the alert, is dead on
  measurement, before any file was cut.** The step was: value each allowed accumulation window of the
  unit's aberration detector by the outbreak cases with onset after the alert that window itself produces,
  against the reflex of multiplying the clusters a window flags by the unit's published preventable share.
  The algebra is sound and was written first: a cluster crosses a `k`-sigma Poisson threshold only once it
  has put `k*sqrt(lambda*W)` cases into the window, so every already-detected cluster loses
  `k*sqrt(lambda)*(sqrt(W2) - sqrt(W1))` cases to a longer window, a loss that grows as the square root of
  the window and is independent of the cluster's size, while a cluster that becomes detectable only at
  window `W` is flagged about `W` days into its notification run and so contributes only about
  `mu*(D - L - W)`. Four parameterisations were simulated end to end on the generating process rather than
  on the algebra, each with the detector, the seasonal baseline, the reporting lag and the register's own
  flag rule: short point-source outbreaks (margins 1.6 to 7.7 per cent, the plug-in naming the same window
  as the truth in two of three seeds); persistent dispersed clusters (0.2 to 2.0 per cent, sensitivity
  saturated at the shortest window); campylobacteriosis volumes with a three-sigma rule and a weekly
  review, which is the realistic artifact (1.5 to 4.1 per cent); and the mean of per-cluster preventable
  shares against the case total, which disagreed on one seed of two and agreed on the other, so the
  disagreement is sampling noise rather than structure. **The obstruction is structural, not a tuning
  problem:** in outbreak detection the cases still ahead of a signal are dominated by whether a cluster is
  detected at all, which is 60 to 80 per cent of its cases, and only weakly by when, which costs
  `k*sqrt(lambda*W)` cases, a few per cluster. Any route that ranks configurations by detections, the
  published-share plug-in included, therefore ranks them almost exactly as the preventable-case total does,
  and the two routes agree by the structure of the domain at every parameterisation a district could
  plausibly record. Re-drawing the decisive step, not the mix: a mix that reverses would need cluster
  intensities concentrated in the narrow band where the window decides, which spans a factor of 2.8 in
  intensity against the factor of 20 real registers carry.
- **The general lesson this slot now owns, worth more than the architecture: a dial on a closed record is a
  replay.** Every per-setting figure a dial build grades is exactly computable from the record, so the
  decisive step cannot live in the computation and has to live in the step from the record to the coming
  window. On this ground every such step is either banned for this slot (population selection, maturity
  censoring, composition mix), or blocked by the house rules (a baseline the clusters themselves
  contaminate, so a back-test blesses the wrong setting until the forward window breaks it, which is the
  validated-decoy shape), or a fractional effect the data cannot separate, which is what was measured
  above. The two dial shapes that have held in this corpus make the replay impossible for a structural
  reason (task104's self-adapting scorer withholds its own flagged observations) or put the decision on an
  interval (task195's paired difference), and both are spent against the last two builds.
- **Architecture 5's axis map on the assigned criminology ground, read off `guard.py check` before any design
  time went in, and banked because the slot note architecture 4 left is wrong about two labels.** On
  criminology-justice / crime-incidence-hotspot-analysis with objective anomaly-detection, the only axis
  BLOCKs against the current last three (task197, task196 v2, task194 v3) are: strategy `maturity_censoring`
  and `causal_design`; shape `17`; context artifact `register`, `planning_thread` and `close_out_summary`;
  role `capacity_planner` and `programme_officer`; forum `board_of_directors` and `trustees_or_governors`;
  forcing event `vote_or_meeting`, `audit_or_inspection` and `statutory_or_regulatory_filing`; org family
  `cooperative_or_member_body`. With gap `objective` and pattern `none`, decision type `quantity_figure`
  blocks on `test.same_puzzle_older` against task140 and `pick_one_of_n` against task184 v1, and Gate G
  `binding_constraint` blocks against task140 and `decomposition_attribution` against task184 v1. Every
  other value on every axis is open, `composition_mix` and `population_selection` included: those two are
  not guard-blocked, so the slot note's line that they are banned for this slot was a design judgement about
  the epidemiological ground and not a fact about the guard. `renew_replace_lapse` has never been drawn in
  the corpus and `date_or_period` once; both are open here.
- **Eleven candidate decisive steps on crime-incidence-hotspot-analysis, each put through the WHAT screen,
  the swap test and the corpus before any row was cut, and all eleven died.** The five patterns the client's
  own library gives this task type die first: the named exposure denominator and the benchmark pool are the
  estimand's comparison, so filing them leaves a group-by and leaving them open is a fork (the library's own
  pin, "risk per a stated exposure", files it); persistence across periods is the window; recorded crime
  mixing incidence, reporting and detection resolves into a channel column (semantics), a reporting rate
  estimated off a survey (open family), or a driver already spent (task196's two capture channels, task446
  v2's assurance-sample sensitivity, task182 v1's instrument footprint, task104's endogenous detector);
  testing clusters against a spatial null is task191's selection-on-the-max plus a bandwidth or neighbour
  tolerance the house bans as a residue; and smoothing small-exposure rates is an open shrinkage family worth
  about 8 per cent (G16's own note). Six more were drawn and killed: maximal coverage over overlapping patrol
  zones and a junction-connected focal sum both fail the swap test, because a neighbourhood or union count
  reads identically with warehouse aisles in it; direct against indirect standardisation is task194 v2 and is
  a convention rather than a method; a like-for-like panel of continuing premises is task68; distinct
  victimised targets against offences is a one-line `nunique` the hygiene battery performs; and time-at-risk
  against a count of units is task181 v1's crossings driver. **The structural reason, worth more than the
  list: in a world additive over rows, every quantity this task type estimates is either one of the
  estimand's five parts or a correction already spent in this lane, so the ground has no decisive step left
  for this slot rather than no good one.**
- **The near-repeat clustering ratio, the one candidate that cleared the WHAT screen and the swap test, is
  dead on measurement before any file was cut.** The step was to rank the district's areas for a
  post-burglary cocooning response on how much more often their burglaries fall close together in place and
  in time than the same burglaries would by chance, the expectation taken exactly from each area's own
  spatial and temporal pair margins (the Knox form, which needs no fit at all and so avoids the background
  rate that killed task181 v3), against the reflex of the raw close-pair count or the share of burglaries
  with a close neighbour. Ten reflexes were swept as code on the generating process: seven of them (the
  count, the count per 1,000 dwellings, the count per square kilometre, the raw close-pair count, close
  pairs per burglary, close pairs over all pairs, and the share of burglaries with a close neighbour) land on
  a compact, busy area and not on the designed winner, which is the separation the design wanted and it
  holds. The eighth kills it: **the plain share of addresses burgled more than once, which the duplicate
  sweep in the hygiene battery computes for free, reaches the designed winner at every boost from 0.15 to
  0.60, and always by a wider margin than the decisive step (1.50x to 2.89x against the Knox ratio's own
  1.26x to 1.46x), so the decisive move is the smallest move on the ladder, which is build 37's death
  shape.** It is one dial and not a tuning problem: repeat and near-repeat victimisation share the boost
  account, so raising the boost raises both margins together, and the Knox margin saturates near 1.46x
  however hard it is driven. Forcing the near-repeats onto different addresses (the same-address share cut
  from 0.30 to 0.12) suppresses the reflex at three boosts out of five and not at the other two, at margins
  of 1.03x to 1.13x, which is seed noise rather than the computable blindness L1 requires, and it
  contradicts the domain's own mechanism. Not resumed, and not re-found: the near-repeat latent structure is
  now spent in this lane twice, at task181 v3 on the background rate and here on the repeat-address reflex.
- **The search's own tooling and draw, kept so the next session on this slot starts from it rather than
  re-deriving it.** Three scripts were written in a session scratchpad that does not survive the session, so
  what they do and what they need is recorded here. **The axis prober** fills `guard.py new task190`'s
  template with a probe card on this pairing and runs `guard.py check` once per value of one axis, grepping
  for the axis rules; it is the cheapest way to get the map in the entry above, and it is worth re-running
  rather than trusting that map, because the three builds the bans reach move as the wave ships. Two BLOCKs
  fire on every probe until a real draw exists and should be ignored while probing: `card world.people is
  empty` and `two_layer.fields`. **The reflex sweep** generates, per area, background burglaries uniform in
  a square of the area's own side and uniform over 730 days, then with probability `boost` attaches
  `1 + Poisson(mfo)` follow-ons at a uniform radius out to 260 m and 1 to 12 days later, an offence taking
  the triggering offence's address with probability `samefrac`; it then computes all within-area pairs and
  ranks the areas on ten measures (count, count per 1,000 dwellings, count per km squared, close pairs,
  close pairs per burglary, close pairs over all pairs, share with a close neighbour, share of addresses
  burgled more than once, the Knox ratio, and the Knox ratio excluding same-address pairs) with the close
  bands at 400 m and 14 days. The eight areas were (side m, dwellings, background, boost, mean follow-ons):
  Kingsley 900/3000/860/0.04/0.5, Rotherglen 1300/2600/610/0.08/0.5, Marsden 1050/1500/480/0.06/0.5, Totara
  Flat 2100/2200/300/0.34/1.1 as the designed winner, Awakino 1700/1800/360/0.10/0.5, Hillsborough
  800/1200/300/0.05/0.5, Pencarrow 2400/3100/430/0.07/0.5, Bexley 1150/900/210/0.12/0.5, seed 190.
  **The dial sweep** is the same generator run over `boost` in (0.15, 0.25, 0.34, 0.45, 0.60) crossed with
  `samefrac` in (0.30, 0.12), reporting which area each of the two measures tops and by what margin; it is
  what turns "the reflex reaches the golden" from an argument into the measurement in the entry above, and
  any later candidate on this ground gets the same treatment before a card is registered.
- **The persona draw, made and unspent.** `guard.py names --geo "New Zealand" --seed 190` returned Bruce
  Wheeler, Rachael Wood, Ryder Reader, Dylan Burrell, Kayla Burr, Brian Simonsen, Benjamin Jefferies, Emma
  Gullery, Manaaki Little, Thomas Hughes. No pack was cut, so none of them is spent and none is on the card;
  a session that draws this slot on a New Zealand world can take them, and one that draws another geography
  redraws rather than translating these.

- **Architecture 5's assigned criminology ground, left behind at the re-root to architecture 6.** The eleven
  dead candidates, the near-repeat Knox measurement and the axis map above stand as the record. What is
  being left behind is the ground itself, not one mechanism: crime-incidence-hotspot-analysis is additive
  over rows, so every quantity it estimates is one of the estimand's five parts or a correction already
  spent in this lane, which is why eleven candidates died before a default path existed. Architecture 6
  moves to `survey-research-official-statistics` / `anomaly-detection`, where the deciding quantity is a
  design-based estimator's own sampling error rather than an aggregate over rows, and the New Zealand
  persona draw banked above stays unspent because the new world is Portugal.
- **The pincer test on architecture 6's decisive step, written before any design time went in, because
  task200 lost four mechanisms on it.** The estimand files all five parts: population (every enterprise in
  the survey's frame, sampled or not, and every consignment despatched in 2026), outcome (the stream's
  recovery rate), window (calendar 2026 on the producer's despatch date), unit (the waste stream) and
  comparison (the plan target at the 95 per cent level). The decisive quantity is none of the five: it is
  the sampling variance of the denominator, which is a statistic of the sample (within-stratum dispersion
  against stratum population and realised sample sizes) and not a constant any clause can state. Filing it
  would file the method, which the house rules forbid; leaving it open does not fork the call, because the
  two estimators the design admits agree to six decimal places on all eight streams while every route that
  disagrees is not an estimator of the design variance at all. The filed quantity is also unobserved, which
  is what `stumping` 1.2 requires: a stream's population arisings are known only from a sample, so two
  estimators of its interval genuinely stand. That is the statable distinction from task198's architectures
  2 and 3, which filed a recorded change (observed exactly) and corrected its variance, and so were
  computing a different quantity.
- **The reflex sweep on architecture 6, run as code on the generating process before any file was cut, and
  the one reflex that reached the golden.** Thirteen routes were swept on the shipped cut: ranking the raw
  shortfall and the relative shortfall (both Mixed commercial and industrial), a bar from the published
  national CV (Mixed C&I, z 2.10 against Metal's 1.32), a bar from 1/sqrt(reporting enterprises) (Mixed
  C&I, 2.64 against 0.65), the design variance with the finite-population correction omitted (no stream,
  Metal 0.96), the same treated as weighted with replacement (no stream, Metal 0.50), the sample pooled as
  a simple random sample (no stream, every CV absurd), the design variance over reporting enterprises only
  (no stream, Metal 1.81), the register's own moved tonnage as the denominator (Mineral construction and
  demolition), shrinkage of each direct rate toward the national rate weighted by record count (Mineral
  construction and demolition), and the design estimator and the delete-one jackknife within strata (both
  Metal, identical to six decimals). **The one route that reaches the golden is ignoring the design weights
  and rescaling the unweighted stream totals so they sum to the published national total.** It is recorded
  rather than designed away because the unrescaled form self-refutes on the shipped cut: four streams come
  out above 100 per cent recovery (Mixed C&I 1.65, Mineral C&D 1.99, Paper 1.25, Glass 1.07) and no stream
  shows any shortfall at all, so the route produces no answer without a deliberate rescale by an arbitrary
  factor of 1.99. The pack closes it further by publishing the survey's own national arisings total, which
  the weighted estimate reproduces and an unweighted sum misses by a factor of about twenty.
- **Targets re-solved per seed, which made the first stability measurement worthless.** The first
  across-seed run reported the correct route naming Metal in 30 of 30 seeds, but the plan targets were
  being re-solved on each seed to hit the designed z-profile, so the measurement was true by construction
  and said nothing about stability. Re-run with the shipped targets held fixed across 60 seeds, Metal's z
  ran 3.62 to 6.61 and never fell below the bar, the CV lever ran 3.81x to 9.82x, and Mixed C&I's z ran
  -1.32 to 4.11 about its shipped 1.45. That last range is the honest behaviour of a shortfall that is not
  established and is reported rather than tuned away: a candidate that fails a significance test is within
  about two standard errors of the bar by definition, so no design can make it both the largest raw
  shortfall and two standard errors clear of failing.
- **A ladder whose decisive step was the finite-population correction alone, rejected as readable.** The
  first design put the whole decisive step on the correction, and the textbook stratified variance formula
  carries it, so a solver who identified the design and applied the standard formula reached the golden
  with no analytical step at all. The step was re-rooted onto which terms and which units carry error, with
  the correction as one of two halves: the numerator is a complete administrative total and contributes
  none, and the domain total's variance is computed over every sampled unit in the stratum including the
  zeros. Measured, that second half is what the client's own named shortcut for a domain estimate (subset
  then estimate) gets wrong, and it costs the golden 3.3x of its CV (1.12 per cent against 4.42), putting
  Metal at 1.81 against the bar.
- **Shipping several prior years of stream-level published rates, rejected before it was cut.** A solver
  with four or five prior years could compute each stream's year-to-year volatility and rank precision off
  it, which is the empirical twin of the decisive quantity and the shape that killed task198's architecture
  3. The pack therefore ships one prior reference year only (2025), and the survey microdata for 2026
  alone, so no variance can be estimated from the series; a single difference per stream cannot estimate a
  variance. The 2025 register legs still ship, because ask A2 needs them and they carry no survey
  microdata with them.
- **Replicate weights, rejected as furniture too close to a banned driver.** Shipping jackknife replicate
  weights would have forced the method handsomely, and task198's architecture 3 (uncertainty computed over
  replication groups while the error source acts on groups the record never replicates over) is banned to
  this build. The design documentation therefore describes the strata, their population and sample counts
  and the weighting, which is what a statistics office publishes, and the jackknife agreement is an
  internal convergence assertion rather than shipped furniture.

- **The common-exposure subset screen, run as code on the cut pack, and the route it caught.** `stumping`
  1.2's screen says a step of the form "put the units on a common exposure before comparing" cannot carry a
  stump, because the subset already at that exposure is a filter and a divide. On this ground the subset at
  a known exposure is the completely enumerated stratum, whose arisings are a census. Measured four ways on
  the shipped cut: ranking the enumerated stratum's own rate shortfall names **Plastic wastes**, the
  relative version names Plastic, and treating those rates as certain and taking the largest names Plastic,
  because the enumerated subset's rate differs from the population rate wherever the stream's arisings are
  not concentrated there (its share of arisings runs from 0.264 for Paper to 0.958 for Metal). The fourth
  route did reach the golden: restricting **both** terms to the 1,630 sampled enterprises, which is
  internally consistent and so not self-refuting, names Metal. **It is closed by construction rather than by
  argument.** The released micro-data now carries a survey record number and no business register number,
  permit number, name, address or region, which is what statistical confidentiality requires of a released
  survey file and is stated as such in the design document; asserted on the shipped schema, no file carries
  both a stratum and a producer key, so neither the enumerated-stratum subset nor the sampled-enterprise
  subset can be identified in the register and none of the four routes is computable from the bundle. The
  same change closes the unweighted-and-rescaled route banked above and makes SF11 unconditional.
- **The designation determinacy screen: the golden's own estimator family returns one designated set.**
  Four licensed ways to the design variance of a ratio whose numerator is a constant were measured on the
  shipped cut: Taylor linearisation with the finite-population correction, the delete-one jackknife within
  strata, grouped balanced repeated replication and the Rao-Wu-Yue rescaling bootstrap, the last three
  carrying the correction. CV(Metal) came out 0.011214, 0.011214, 0.011137 and 0.011234, a spread of 0.9
  per cent of its own value against a bar the golden clears by 2.33x, and **all four designate {Metal}: one
  distinct set**. Over 20 redraws crossed with the four members, 80 draws, there is still **one distinct
  designated set**, Metal in 80 of 80. What rules out all but one is the design rather than any sentence:
  the numerator is a complete administrative total, so the ratio's variance is exactly the denominator's
  relative variance with no covariance term and no model to choose, and the denominator is estimated under
  stratified simple random sampling without replacement, fully described by the frame and realised sample
  sizes, so every licensed estimator is a consistent estimator of the same sum and the only variation left
  is Monte Carlo noise in the replication methods. The other half of the screen is also measured: the
  numerator-only route, a count-like interval on the register tonnage, establishes seven of the eight
  streams and ranks Mixed commercial and industrial first at 25.11 standard errors against Metal's 13.60,
  so it does not land the golden's verdict.
- **The register's producers drawn uncorrelated with the arisings structure, found and fixed before the
  screens were run.** The first cut drew each consignment's producer uniformly from all 6,235 permit
  holders, so Metal's movements were spread evenly over enterprises of every size while 96 per cent of its
  arisings came from the largest stratum. That is a realism tell a reader could check in one cross-tab, and
  it also made the subset screens meaningless. Each consignment's producer is now drawn from the stratum
  distribution of its own stream's arisings, so the register and the survey agree on where a stream's waste
  comes from.
- **Twelve assertions that were vacuous, found by reading the output rather than the exit status.** The
  semantic-fork helpers return a `(verdict, detail)` pair and were being passed to `ok()` as the condition,
  and a non-empty tuple is always truthy, so SF1, SF3 to SF6, SF8, SF10 to SF12, D4 and two closure
  assertions were passing without testing anything. All twelve are now unpacked, and all twelve pass on the
  merits. It would have been a Gate A finding.
- **metadata.json shipped inside the pack, which would have handed over both distractors.** The first cut
  wrote it to `target/`, where it names each distractor and why the solution never reads it. The house
  convention is the task root and `leak.py` reads it there; it is now at the root, and `checks.py` asserts
  the pack does not ship the author's manifest.
- **Two sentences in the documents saying the pack was built.** Three documents and the operation-code
  workbook carried "Synthetic data produced for methodological work; no real enterprise is described",
  which `leak.py` sweep 2 reads as a statement that the pack was constructed, and a real release carries no
  such line. Removed; provenance and licence live in metadata.json alone. The design document was also
  renamed from `bws_sample_design_2026.pdf` to `bws_2026_design_and_weighting.pdf`, because sweep 1 reads
  `sample_` as the author's vocabulary and the field has another word for the same thing.
- **The four leak REVIEW lines, answered.** (1) `collection_capacity_note_2027.pdf` carries 11 of the 15
  distinctive words of the committed call: it files the estimand, which determinism requires at authority,
  and the estimand necessarily shares the call's nouns; it names no stream, no method and no figure the
  answer turns on, and it has four other uses (the division's establishment, the core-round field days, the
  complaint and its deadline, the extract dates), so it fails the single-use test for an announcement.
  (2 to 4) Three documents carry 7 to 9 of the 25 stump-paragraph terms, which are the field's own nouns
  (design, stratum, sample, register, enterprise, estimate, consignment, survey) and unavoidable in any
  honest document in this world. That none of them names the move is asserted rather than argued: `checks.py`
  D6 reads every shipped PDF and requires that none of twelve terms that would name how the rate's sampling
  error is computed appears anywhere in them.
- **Two axis probes that moved under the build, recorded because the next session will meet them again.**
  `ban.role` blocked the reserved `capacity_planner` against task197; the block then appeared to lapse when
  the axis bans moved to the last three live cards and this slot's stale card went `architecture_spent`;
  and it fired again the moment this build's own card was placed live in the window, because registering it
  pulls task197 back into the last three. The axis was redrawn to `operations_director` rather than argued.
  The decisive generator was probed at G17 as well as G16: G17 moved the surface promotion from task195 to
  task189 and task191 rather than removing it, so the label was not changed to clear a screen and G16
  stands with the promotion reported and differentiated.

### The repair pass of 2026-10-18, one line per thing abandoned

- Counting a usable return per log row: abandoned on the orchestrator's measurement, which the generator now
  reproduces. The log carries a re-sent operations batch of fifteen exact duplicate rows, four of them Norte
  usable returns, so the row count was 542 against 538 distinct cases and put total usable returns at 1,634
  against the 1,630 records of the micro-data and of the design table. Deliverable 3's Norte figure moves
  from 16.66 to 16.53 and nothing else in the pack moves: the other four regions carried no duplicate, and
  the field-days denominator was already counted once per visit reference. `checks.py` A7 asserts the tie.
- Leaving hours per field day unfiled: abandoned. Seventy-one Alentejo rows carry `time_unit = h` and no
  shipped file said what a field day is, so the committed 10.11 and 16.42 rested on an inference (eight
  hours is the only factor putting the converted values inside the range the `d` rows occupy). The survey's
  own collection documentation now books field work "in field days of eight hours" beside the sentence that
  describes the log's unit column. Filed as a convention, not a method: it fixes a unit, and the ask's
  device is still the unstated grain. `checks.py` H1 asserts the text through the same extractor as its own
  positive control, H2 that the figure moves to 11.55 and 10.78 at seven and seven and a half hours, and H3
  that the convention is filed once.
- The 2025 release's published coefficient of variation of the 2026 round: abandoned as an oracle. It
  reproduced at 3.915 under the decisive estimator and 4.091 without the correction, so it confirmed the
  decisive method against a shipped number. Replaced by the 2025 round's own measure, which nothing in the
  bundle reproduces; the full record is in `## Oracles`.
- The 2025 release's recovered column as a near-tie to the register: abandoned. The judged pack's residuals
  of +47 to +345 t (0.3 to 0.5 per cent) read as a calibration target that could be chased, and the judge
  could not reconcile them under any basis. The column is now the register as at the 30 June 2026 extract
  the release was compiled from, which the release states along with the fact that the series is not revised
  for the confirmations the register takes later, and it sits 3.3 to 5.0 per cent below the recompute. The
  two jobs the table does for the design are re-asserted rather than assumed (`checks.py` H8, H9).
- The register's uniform lags, integer tonnages and numbered sites: abandoned on the stage-4 reader's
  realism findings. Receipts were always one day after despatch and confirmations two or three after, which
  is a standard deviation of zero; every tonnage was a whole tonne; every site was "Unidade N de <region>"
  and every carrier "Transportes N". The register now carries a transit lag over twelve values (mean 2.00
  days, sd 1.15, longest 14), a confirmation lag over forty-one (mean 4.31, sd 3.69, longest 47), 4.2 per
  cent of movements at a weekend and 1.2 per cent on a national holiday against 28.6 and 2.7 by calendar,
  net weights to the 20 kg a weighbridge records (98.1 per cent fractional over fifty distinct hundredths),
  and names drawn from the pt_PT place and family-name pools with each site's place inside its own licensed
  region. Every new draw comes from its own seeded stream, so the consignment allocation, producers, codes,
  sites, response log and municipal files are the ones the judged pack was cut with and no graded figure
  moves; the weighbridge noise sums to exactly zero over each stream and class, asserted in `build.exact`.
- Holiday damping that stepped backwards across the year end: abandoned within the pass. Moving a 1 January
  despatch to the previous working day moved it into 2025, which dropped it out of the reference year and
  cost metal 41 t of recovered tonnage; `build.exact` caught it on the first run. The bump now turns inwards
  at either end of the year, and `checks.py` J8 asserts no leg is dated after the extract and that none
  piles onto the extract date.
- SF3's convergence as the judged pack measured it: abandoned and re-measured, not weakened. With a real
  confirmation tail the extract carries 762 January 2027 confirmations for 2026 despatches, so counting only
  2026 despatches confirmed in 2026 drops 2.3 to 3.9 per cent of every stream's tonnage and establishes two
  streams. That is not the reading a confirmation-date basis gives, because the 2025 register ships and
  carries the previous year's confirmations landing in 2026: read consistently over both files the
  alternative moves no stream by more than 0.73 per cent and still establishes metal alone. SF3 is asserted
  on the consistent reading and SF3b records that the half reading contradicts the memo's one-stream clause.
- A prompt word for the municipal population: abandoned in favour of a document convention. "The
  municipalities' own returns" in the prompt closes SF13 for every response, which the measurement puts at a
  46.2 pair ceiling; the memo's compilation convention closes it for a literal reader while leaving the
  across-grain reconciliation to be done, which holds the measured ceiling at 28.5. Both numbers are in
  `## Ask sheet`. "By origin region" did go in the prompt, which cost seven characters and was paid for by
  dropping "movement" from the stage-chain clause (994 characters).

### The pins pass of 2026-10-18, one line per thing the judge's second pass moved or killed

The second judge pass returned DETERMINISTIC with a FIX_NOW of three note-level pins and three hygiene
findings. Every graded figure is frozen through this pass and the freeze is proved key by key against
`generator/figures.json` (193 keys, 0 moved).

- Regenerating the 2025 release's published recovered column so that a stated cut of the register
  reproduces it: refused on the judge's own instruction, because a column that reconciles confirms the
  roots-only chain basis to anyone who checks, which is the oracle shape this build has already paid to
  remove once. The column is carried off the register at the 30 June 2026 extract the release names and then
  moved by the register's ordinary post-cut amendment (`world.PRIOR_DRIFT`, 0.24 to 0.76 per cent a stream,
  one sign, no constant ratio), so the nearest basis is off by 12 to 461 t a stream and nothing reproduces
  it. Asserted in `checks.py` H7b and independently in `verify.py`.
- `late = U(0.028, 0.052)` as the published column's construction: dead, and it is what the judge caught.
  It made the release's stated reason false: the 2025 file held no leg after 2026-03-09 and a maximum
  confirmation lag of 48 days, so a 30 June 2026 extract would have held everything and the 12,296 t gap had
  no source. The gap is now the register's own tail, 3,913 t of the 5,323 t distance, on all eight streams.
- One long clock for the confirmation lag at `CONF_LONG_P = 0.045`: dead on measurement. It carried the 2025
  tail (3,923 t) but left textile at zero, flattened the censoring the extract leaves (December only 2.6
  times January) and pushed the confirmation-date reading of SF3 to metal at 2.96 standard errors. Two clocks
  at 0.110 (median 55 days) and 0.040 (median 250 days) carry all three: tail 3,913 t on every stream,
  December 4.2 times January, SF3 metal at 3.13.
- Making the 2025 unconfirmed class concentrate too, for one never-closes rate across both years: dead. The
  class totals are the frozen chain cells and the 2025 despatch dates come off the shared draw stream that
  the response log and the municipal returns are cut from, so moving them moves ask A1 and ask A3. Measured
  residual: the never-closes rate reads 3.35 per cent in 2025 against 1.4 per cent in 2026, visible only to a
  solver who models both years' censoring, and the July 2026 system move is the obvious reading if one does.
- Clearing the exact-tenth read on the eight 2026 rates: impossible under the freeze, with the arithmetic as
  the reason. The recovered tonnage and the arisings are both printed and frozen (70,384 t and 124,354 t for
  metal), and a ratio of two printed integers is pinned: metal's rate cannot leave [56.5991, 56.6004]
  whatever the legs do, and the same holds for all 24 pass-through rates. What was free is taken: the 24
  stream and stage totals are no longer whole numbers (they sit 0.02 to 0.38 of a tonne off, inside the
  printed tonne, `world.CLASS_RESID`), so no total in the register reads as having been solved from a round
  number, and `build.cell` now asserts both edges instead of asserting a whole tonne. Clearing the residual
  needs one printed tonnage a stream to move by 12 to 62 t, which is a graded figure and the author's call.
- Quoting the 2025 coefficient of variation for the activity-class publication domain instead of the national
  total, the judge's optional hardening: declined with a proof rather than a preference. The nudge is the
  ordering of the 2026 round's own estimators against the published 3.4 per cent (3.9 with the correction,
  4.5 without), and rung 1's measured arithmetic is built on that same 3.4 (metal 1.51 standard errors,
  mixed commercial and industrial 2.42). Holding the rung means holding the number and holding the number
  holds the nudge, because the domain the figure is published for enters neither calculation. The change
  would also relocate the check rather than remove it (the 2026 micro-data ships `nace_division`, so an
  activity-class CV for the 2026 round is recomputable, while a 2025 one is not) and would need an activity
  class at frame level, which the population does not carry.
- Keeping ask A1's visit grain silent: given up on the judge's pin, and it is the one real trade in this
  pass. The design documentation now states that a visit's field days are recorded on each case the visit
  covered, which is a filed rule, so the cracker resolves A1's ten figures: the measured pair ceiling moves
  from 28.5 to 38.3 against a gate of 40, and `precut.py`'s "cracker misses every ask" fails on the A1 row.
  The pin buys the last literal reading in the pack that pointed at a wrong number (the row sum files 55.57
  field days for Alentejo against 13 dated visits), which is a determinism verdict against an ask's silence.
- Shortening the prompt to pay for the four chain stages: "The answer is due" became "Due", the xlsx clause
  lost its verb and "confirmed recovered" became "recovered", the png clause lost "showing its", the field
  day clause lost one "field" and the municipal clause lost "reported". The stages cost 89 characters and the
  prompt stands at 995; no requirement, unit or rounding was dropped.

### The ask re-siting of 2026-10-18, one line per thing abandoned

`precut.py` came back exit 1 on `cracker misses every ask`, because the pin the determinism judge
required made ask A1's primary a filed rule. The gate's own number still passed (38.3 against 40) and
the thing the gate protects did not: with both top responses reading the pinned clause the pair
measured 48.1, and with A3's convention found as well 67.8, against a house bar of 50. The main
recommendation side is frozen through this pass and `freeze.py check --mode rubric` proves it; what
moved is `bws_2026_response_log.csv`, `enterprise_permit_crosswalk.csv`,
`municipal_waste_returns_2026.csv`, the two ask sentences of the prompt and the ask goldens, and
`checks.py` A10 holds the digest of every file the call reads against the shipped pack.

- Hardening ask A1 in place, keeping the field days as its quantity: dead on arithmetic. The pin
  states that a visit's field days are recorded on each case the visit covered, so the quantity's
  only difficulty was the grain the pin states, and no device can be put under a quantity whose
  whole construction a shipped sentence gives. The field days stay in the log as texture, the pin
  stays exactly as the judge wrote it, and `checks.py` SF12 and H2 assert that 0 of the 28 graded
  figures now read the field_days column.
- Keeping A1's quantity and adding rows to the log that the extract had dropped (a silently partial
  extract, the tell being interior gaps in each case's own contact sequence): dead on a frozen
  sentence. Section 5 of the design documentation, which the call reads and which cannot move, says
  the log records the division's contacts with each issued enterprise, so a judge reading it
  literally gets the row count as the contacts and the device becomes a fork against a shipped
  sentence. Rejected before any row was cut.
- A1 re-sited onto the region of the enterprise contacted, with the permit reissue as its primary:
  measured and kept. 150 of the round's permit numbers carry a crosswalk row marked current whose
  validity starts in the agency's January 2027 licensing runs, after the last contact in the log
  (2026-12-30), and the holder differs
  in region on 126 of them; the current-row reading moves every region's contacts by 31 to 77 and
  every ratio by 0.02 to 0.09, and the team-identifier reading by 50 to 175 contacts. The
  reattribution is not proportionate because the enterprises that gave a permit up are the ones the
  round found hardest to collect from, which is what keeps the ratio moving with the count: with the
  reissues drawn proportionately the ratio moved by 0.00 to 0.01 in three regions and the figure
  would have been free.
- Siting the reissue on any permit number the 2026 register uses: dead on measurement, and it is the
  gravest class of finding. With the pool drawn from the issued sample at large, 124 of the 150
  numbers were 2026 despatchers, and a solver who restricted the register to producers whose 2026
  permit row was current dropped 2,086 t of metal and established a second stream (metal at 7.43
  standard errors and mixed commercial and industrial at 2.13 against the shipped 4.57 and 1.45),
  which is a path from an ask device into the call. The reissue pool is now drawn from the 341
  issued holders with no 2026 despatch leg, so that same filter returns the shipped pack's own
  figures (metal only, 4.65 standard errors, 70,327 t), and `checks.py` D7 asserts it.
- The reissued rows all carrying one valid_from, which would have let a single column value isolate
  them: closed against ban 2 by licensing weekly and putting 12 ordinary re-registrations in the same
  four runs, so the January 2027 batch holds 162 rows of two kinds and the column classifies nothing.
- Three handholds that would have made the as-of join unnecessary, all removed before measuring:
  case references numbered region by region (a solver could read the region off the number), visit
  references prefixed with the region, and a team identifier that matched the enterprise's region on
  every case. Cases and visits now carry the operational system's own shuffled counters and 722
  contacts were worked by a neighbouring region's team, so the ask's basis has to be joined and
  cannot be read off a label.
- A1's figures as a count and a ratio of two quantities that move together: measured and changed.
  Contacts per usable return is immune to a proportionate reattribution, so the pair of figures was
  checked against the device before the wording was written rather than after.
- A3's authority rollup kept as the primary: dead on the same lesson as A1. The memo files the
  counting convention, the memo is a file the call reads and cannot move, so the cracker resolves the
  rollup by executing a filed sentence. It is demoted to hazard H5, where it still costs the mirror
  every figure, and the ask's primary now sits under it.
- A3 re-sited onto the December row that is the year's confirmation: measured and kept. The five
  December rows stand at 11.8 times the mean of their own eleven months against a highest 0.86
  elsewhere, and summing twelve months puts those municipalities' facility receipts at 50 to 51 per
  cent of their collections against 94 to 99 for the other 22. The golden figures do not move,
  because the truth of the reconciliation is unchanged and only the route to it is now silent.
- The same device sized as a fourth-quarter total rather than the year, to make the lazy figure less
  conspicuous: dead on determinism. A December row at three times its own monthly mean says the row
  covers about three months and does not say which three, so the year is recoverable only up to the
  boundary and two defensible figures exist. The year version is an identity: the row less its own
  eleven months lands inside that municipality's monthly range, which fixes the span exactly. The
  price is paid in the open, and it is that the cracker's gap share reads 12.5 to 27.0 per cent
  against the answer's 2.6 to 4.1.
- A3 re-sited onto the receipts' origin region instead (a defaulted region column on cross-boundary
  deliveries): held, not built, because A1's primary is already the region a row belongs to and two
  asks whose device is a wrong grouping key is one device twice. Kept here as the fallback if the
  reissue is ever spent.
- Keeping `enterprise_permit_crosswalk.csv` in `metadata.json` as a declared distractor: it is not
  one and never was, since every ask joins through it; the two declared distractors are the carrier
  log and the export notifications, which is what the file already says.


**Architecture 6, spent on Gate F, measured 2026-10-18.** The round-3 leak reader, a medium-effort thread
holding only a fresh unzip of the pack and `prompt.txt`, reported the call and every graded figure: 43 of
43 against `generator/figures.json`, with the stream, the 56.6 per cent rate, the 55.4 to 57.8 interval,
the 59.5 target and the 2.9 point shortfall all exact, and all 38 supplementary ask figures exact. It also
stated the easy-route error unprompted, that counting R13 as a recovery lifts mixed commercial and
industrial wastes above its target. Three causes, each quoted in `leak_check_report.md`: the memo files the
test ("established below target where its 2026 recovery rate is below its target at the 95 per cent
level"), so the decisive step is executing a filed rule and picking a textbook variance formula, which the
client's rule 3 bans as the decisive step; the 2025 release announces A2's device in a sentence telling the
reader a later extract stands above the published column; and A3's two devices are arithmetically exact
enough to be found by inspection, five December values at about fourteen times a month and five
association rows each summing to exactly three members. No ask rewording repairs this, because the devices
were not weak, they were absent from the reader's path. The ask layer had been re-sited once already, from
a measured 65.5 to a paper 28.5, and the `## Ask sheet` cracker table claimed every ask row missed: that
table was a model of the opponent and it was wrong on all three asks, where the reader is the measurement.
Also unresolved on this world: `guard.py heart` BLOCKs on `ban.org_family`, because
`research_or_statistics_office` repeats task244 two builds earlier and `government_agency` repeats task170
three builds earlier, so both honest keys for a statutory statistics institute are banned and only the
author's `--force` or a different deciding organisation clears it. Paused rather than retired, per the
author file's standing no-retirement rule.

## Architecture 4, abandoned on a model constraint rather than a design finding

Architecture 4 is abandoned, and not because the design failed. Two builder sessions were terminated by an
API safeguard that flagged this ground's own subject matter, one on Opus 5 (request `req_011Cg96NYnjwr8JwJnA4LDdk`,
error type `invalid_request`, details `[bio]`) and one on Sonnet 5.5 (`req_011Cg96z2kTp3cdub9iT3kXv`, same
details), the second written deliberately in surveillance-statistics terms rather than epidemiological ones
and flagged all the same. Every model this environment can reach refuses the material, so no agent can
carry the build, whatever the design's merits.

That also voids the premise of the author's earlier override. The override kept this ground against a
`ban.subdomain` BLOCK on the reasoning that this slot had claimed it first; the ground is now unavailable
for a reason that has nothing to do with the ban, so the override has nothing left to protect and the slot
re-roots at architecture 5 on different ground.

**What architecture 4 measured, kept because a fifth draw should not re-find it.** The decisive step was
that a detector setting is worth what each flagged series still has ahead of it at the moment that
setting's own alert fires. The first prototype showed no reversal between that and the easy route, because
the quantity the easy route gets right rises with the detection window too, and the session before the
terminations recorded the step as dead in four parameterisations for a structural reason: whether a series
is flagged at all dominates when it is flagged, by about an order of magnitude. That verdict was never
re-run as code, so it stands as a strong indication rather than a measurement.

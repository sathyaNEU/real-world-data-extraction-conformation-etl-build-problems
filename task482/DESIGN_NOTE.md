# task482 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 10, drawn 2026-10-24 after architectures 1
to 9 were spent at stage 4: a fresh world and pack in the ETL objective, a nonprofit hospice organisation's FY2026
Medicare aggregate cap repayments, accrued provider number by provider number at the December 2026 close, each
beneficiary counted under the proportional method on the hospice days they will receive in every hospice and year.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task482.json` (architecture v10, lineage v1 to v9 spent), checked
  2026-10-24 after a fetch of main: WARN, no BLOCK. The first draft carried G13 (horizon mismatch) as its decisive
  generator and BLOCKed on `test.same_puzzle` against task171 v4 (time, G13, quantity_figure) and on the older
  same-puzzle and same-driver signatures of five builds each; the decisive generator is G12 (absence of record against
  record of absence: a beneficiary discharged alive who has no later election is not a beneficiary who will have none),
  which is the honest one for the step that decides, with G13 (the days recorded to the close against the days in every
  year) as the frame. Against G12 the older task157, task192 v2, task201 v2 and task445 v1 repeat gap, pattern and
  decision type or Gate G and are differentiated on the card: task157 forecasts a lapsed group's returns inside a window
  from earlier waves' calendar; task192 v2 counts a cohort's events before a terminal end; task201 v2 recovers each
  event's unrecorded opening interval; task445 v1 completes a still-open period's total. Here every day given is
  recorded and nothing is completed: each member's later days enter the denominator of a share.
- **WARNs answered.** `repeat.question_form` (how much, against task486 v2): the decision is an amount for each provider
  number, so the question asks how much. People drawn with `guard.py names --geo us --seed 482` and checked against
  every card: Breanna Graham (the organisation's controller, the requester), Jeremy Cortez (its chief financial
  officer) and John Huang (its reimbursement director); none appears in the pack. Lawrence Hughes and Audrey Bautista,
  drawn for architecture 9 from the same seed, are not reused.
- **Pairing:** Healthcare Delivery & Health Economics, task type `payment-claims-health-plan-analytics`, which serves
  ETL: the organisation's two EMR election exports, its levels-of-care and remittance lines, and the Medicare
  contractor's beneficiary days reports conformed into the cap schedule the year-end accrual reads, one row per FY2026
  beneficiary per provider number with the days in the cap year, the days in every hospice and year, the share and the
  cap they carry.
- **The decision and the quantity:** Elderglen Hospice & Palliative Care, a nonprofit in central and southeastern Ohio,
  holds eight Medicare hospice provider numbers: seven of its own and Fallowmere Hospice, bought under a change of
  ownership on 1 March 2025. Medicare pays each provider number at most its aggregate cap for a cap year (1 October to
  30 September): the FY2026 per-beneficiary cap amount times the number of beneficiaries counted under the proportional
  method of 42 CFR 418.309, each beneficiary counted as their FY2026 days at the provider number over their total days
  of hospice care in all hospices and all years. Payments above the cap are repaid when the contractor determines the
  cap. Elderglen accrues each provider number's FY2026 repayment at its 31 December 2026 close; the external auditors
  test the estimate. Forward facing: the determination counts days not yet given.
- **Shape:** `07`, a grid read provider number by provider number: each provider number's FY2026 payments, counted
  beneficiaries, cap and accrued repayment (eight provider numbers, four figures each), the total accrual, the provider
  numbers owing; asks of one figure per provider number on files the call reads only for days (levels-of-care days and
  payment detail); the workbook's sheets and the deliverable. About 75 criteria on structure.
- **Strategy:** `maturity_censoring` (each beneficiary's hospice days are recorded only to the close, and the days
  still to come are estimated from the beneficiary's state at the close); Gate G `method_or_model_selection` (how the
  remaining days are projected, the data ruling out the easy routes); gap `time` (the days recorded to the close are
  backward, the determination counts every later year); pattern none; generators G12 (decisive) and G13. Layer 2 family
  `field_method`, pattern `own:a capped credit shared on each member's lifetime days, projected from the member's state
  at the close (an open stay by its length so far, a live discharge by its time out)`. Calibration organ:
  `existing_book_actuals`, Elderglen's own elections since October 2016 and the contractor's reports on its earlier
  cohorts. Context artifact `capacity_report` (the monthly census report with each program's average length of stay by
  diagnosis).
- **World:** Ohio, USD; the organisation's seven programs in Brackwater, Corrinbrook, Dunsmere, Lindmoor, Pennacott,
  Sallowfield and Wexmoor, and Fallowmere Hospice; invented names screened against real places (a register of US,
  Canadian and UK places, every one more than two edits away) and against real organisations and products by search
  before any reader sees the pack (H21).
- **Forcing fact:** the organisation closes its 2026 books on 31 December 2026, and the cap repayment for FY2026 is
  accrued at that close from the records as they stand.
- **Forum and forcing event:** auditor (the external auditors test the accrual), period_close. Organisation
  hospital_or_health_provider; role finance_controller.
- **The physics:** a beneficiary elects hospice and stays until death, a revocation or a discharge because they are no
  longer terminally ill; about one election in six ends alive, one in three for dementia. A beneficiary discharged
  alive can elect hospice again at any time, at Elderglen or at any other hospice, and many do, most in the first
  months out; the chance that one who has been out longer comes back falls the longer they stay out. A stay that has
  already run long is a stay of the kind that runs long: its expected remainder grows with its length so far.
- **Data-native sentence:** in the elections a beneficiary discharged alive often comes back months later under a new
  election, and a third of Fallowmere's returns appear only in the contractor's reports, at hospices outside the
  organisation; the FY2026 cohort holds stays still open at the close and live discharges whose days to come no record
  holds.
- **Default path and golden, indicative:** on the feasibility harness (eight provider numbers, ten years of elections)
  the cap ratio of a dementia-heavy provider number with many live discharges moves from 0.98 on the days to the close
  to 1.06 with its open stays run conditionally and its live discharges' returns counted in every hospice, while the
  open stays alone take it to 0.99; the stage 2 generator fixes the set: Brackwater, Lindmoor and Wexmoor owe on the
  default path, and Fallowmere owes too once each live discharge carries its expected returns.
- **The WHAT screen.** Population: Medicare beneficiaries with hospice days at the provider number in FY2026 (418.309,
  the policy). Outcome: the provider number's FY2026 repayment on the contractor's determination. Unit: dollars.
  Window: the FY2026 cap year, with every later day of each beneficiary's hospice care counted. Comparison: payments
  against the cap. The decisive step settles none of them: it is how many days each beneficiary will still receive,
  which no record or filed rule states.
- **Sources, one line each:**
  - 42 CFR 418.309 and the hospice payment final rules: the aggregate cap, the cap year, the proportional method;
  - hospice operations: election, revocation, discharge as no longer terminally ill, transfer, re-election, levels of
    care (routine home care in two tiers, continuous home care in hours, inpatient respite, general inpatient);
  - provider practice: the cap liability accrued with the patients still on service and the patients who may return.
- **Same-puzzle and same-driver tests:** (time, G12, quantity_figure) and (time, G12, method_or_model_selection)
  against the last twelve builds, lineage included: no match; the older matches are differentiated on the card.
- **Abstraction test:** the nearest drivers stripped of nouns: task266 v1 counts the units whose spell ends one way
  within a fixed time; task271 v2 reads a latent state from call records; task244 corrects moves between two states for
  misclassification; task143 takes a joint chance over a shared error. Here no spell is counted and no state is
  misread: each member's total is the recorded part plus the remainder its state implies, and the total divides a
  share.

## Default path

1. Read 42 CFR 418.309 and the accrual policy: each FY2026 beneficiary counts as their FY2026 days at the provider
   number over their total hospice days in all hospices and years; the cap is the count times the FY2026 cap amount;
   the repayment is the FY2026 payments above the cap.
2. Built each FY2026 beneficiary's days at each provider number in the cap year from the two EMR exports and the
   levels-of-care lines, and each one's days in every hospice to date from the elections and the contractor's current
   report.
3. Ran each stay still open at the close to its expected end, from Elderglen's closed stays of the same diagnosis
   group, conditional on how long it had run.
4. Took each beneficiary discharged alive as finished: no later election is on file.
5. Summed the shares, applied the cap amount and set the repayment against each provider number's FY2026 payments.

Ends on: repayments at Brackwater, Lindmoor and Wexmoor; none at Fallowmere.

Golden: repayments at Brackwater, Lindmoor, Wexmoor and Fallowmere.

## Stump sentence

The default path runs every stay still open at the close to its expected end and treats each beneficiary discharged
alive as finished, and accrues repayments at Brackwater, Lindmoor and Wexmoor only; a beneficiary discharged alive
often elects hospice again, the chance falling the longer they have been out, and a third of Fallowmere's returns go
to hospices outside the organisation that only the contractor's reports hold, so each live discharge's share is read
on the days the history of beneficiaries out as long shows to come, in every hospice, and Fallowmere owes too.

## Three rules

Task type: payment-claims-health-plan-analytics (Healthcare Delivery & Health Economics), a task type serving Data
Extraction & Conformation (ETL): the EMR elections, levels-of-care lines, remittances and the contractor's beneficiary
days reports conformed into the FY2026 cap schedule, one row per beneficiary per provider number, that the year-end
accrual reads.

Domain test: the quantity that decides is each FY2026 beneficiary's hospice days in all hospices and years under the
proportional method, which hospice finance estimates for the cap liability from each beneficiary's state at the close
(a stay still open and how long it has run, a live discharge and how long ago, a death) out of the provider's own
history of elections; the field's estimator is the expected remainder for each state, read from the beneficiaries who
were once in it.

Swap: "which schools owe a refund because each pupil counts as their days at the school over their days in every school
and every year" stops making sense: no other field shares out a capped amount on its members' lifetime days, and the
states that decide the remainder (an open election, a live discharge that can be followed by a new election) are the
hospice benefit's own.

Layer 1: two EMR election exports with different layouts, one of them Fallowmere's seller's system for its elections
before 1 March 2025; the contractor's beneficiary days reports in fixed width, one per cohort, with each beneficiary's
days at every provider number by cap year as of the report's date; remittance lines with reversals, adjustments and the
2 per cent sequestration; beneficiary identifiers moving from the HICN to the MBI in 2018 to 2020; continuous home care
billed in hours; the cap year (October to September) against the December close. Each is produced by the systems that
hold it; nothing is placed to be caught.

Layer 2: field_method; the cap liability estimated the way the field estimates it, each beneficiary's remaining
lifetime hospice days projected from their state at the close, and the methodological choice that flips the call is
treating a beneficiary discharged alive as a beneficiary still accruing days, with the chance of a return read on how
long they have been out and counted in every hospice.

Decisive step: projecting each FY2026 beneficiary discharged alive and not yet back to the hospice days the history of
beneficiaries out as long shows still to come, in Elderglen's programs and in hospices outside it, rather than taking
the days on file as their total.

Not semantics: every field can be read correctly (the discharge reasons, the contractor's report columns, the cap
year, the levels of care) and the default path still treats a live discharge as finished, because no field says
whether a beneficiary will elect hospice again; the reading of "all hospices and all years" is necessary and leaves
the projection undone.

Not rule application: 418.309 and the policy define the count and the cap, and no filed rule or procedure says how
many days a beneficiary will still receive or how to estimate them; executing every stated rule on the days on file,
or with open stays run to their ends, files the default path's set. The family the rules leave open, and its spread,
is measured at stage 2: the enumerated family (days to the close; open stays by average length less time so far;
open stays conditionally; returns at the history's unconditional rate; returns conditional on time out, in Elderglen's
programs only; returns conditional on time out in every hospice), the standing family (the constructions that condition
on time out and diagnosis and count every hospice: nonparametric, parametric and empirical-analog versions), and the
loudness of what rules the others out.

Analyst test: with every file read and the proportional method applied, the easy route runs each open stay to its
expected end and treats each beneficiary discharged alive as finished, and accrues repayments at Brackwater, Lindmoor
and Wexmoor only (the default path's Ends on), missing Fallowmere.

Estimand: Elderglen's cap liability policy, section 2: each provider number's FY2026 repayment is its FY2026 Medicare
payments less its aggregate cap, the cap counting each FY2026 beneficiary as their FY2026 days at the provider number
over the hospice days the beneficiary is expected to receive in every hospice and year, the days on file to the close
plus the days expected after it given what Elderglen knows of the beneficiary at the close (the file:
`elderglen_cap_liability_policy.docx`).

No decoy: nothing is planted to be caught; no memo, draft, briefing or stakeholder figure carries the default path's
answer, and no provisional FY2026 determination ships. The census report's average lengths of stay are the programs'
own operating report and rank nothing on the decision.

No certified replay: the method is not hidden and recovered by reproducing certified or published figures; the
contractor's reports on earlier cohorts hold days, not the method, and the policy files the estimand.

Lesson: a share whose denominator is a member's lifetime total counts every later spell, and a member who left alive
is not finished; the remainder for each state is read from the members who were once in that state, at the same time
since entering it.

## Architecture 9 record (spent 2026-10-23)

Architecture 9 read each station's Schedule C availability from the bikes in working order docked, each bike's spells
rebuilt from the trips and fleet moves and a bike counted out of working order from the end of the ride that left it
when renters passed it over and a van then took it to the depot for a day or more, against the status feed's available
count (W-02, W-12, W-16 and W-19 against W-16 alone). At stage 4 (zip 14ceb178) both scored readers missed the call:
reader A subtracted the reported bikes and the bikes mechanics took in without a report, inside the inspection windows
(W-16 and W-19); reader B subtracted the reported bikes only (W-16). Both kept nearly every ask figure (65 and 64 of 74,
exit 1): the sales export's present-location column undone through the work orders' terminal replacements, and the
alarms ended at restarts once the clear pairing ran to hundreds of hours with sales inside them. The isolated judge
thread returned NOT_DETERMINISTIC, SEND_BACK, competing_defensible_answer (Gates B, C and E): no shipped file says that
unreported broken bikes exist or how to find them, so the records read literally (the feed, or the rebuild with the
reported bikes out) file W-16 alone, and the depot-stay cut and the pass test sit only in the solution's steps (at 36
and 48 hours W-17 and W-19 move by a point); Gate G `planted_defect_flip`, `surface_read_rejection`,
`surface_read_dependency: yes`, `sole_data_defect: yes`; Gate H `decisive_step: planted`.

## Architecture 8 record (spent 2026-10-23)

Architecture 8 carried each store's data logger record through the vaccine's thermal lag, a first-order response
fitted per logger make on the two weeks each pilot store's old logger kept recording beside its new in-carton sensor
(42.2, 42.2 and 41.9 minutes), against the loggers' readings taken as the vaccine's temperature (six stores against
ten). At stage 4 (zip ad958ec9) reader B set the pilot stores' loggers beside their in-carton sensors over the overlap
unprompted, fitted the lag as a first-order filter (0.21 of the gap closed per ten minutes, about 42 minutes) and
landed the six stores and every store's whole hours, answering question 6 "an analytical choice" on standard 7.2; it
kept every ask figure too (122 of 122 graded figures, exit 1): the counts' own closing times, the credits found when
per-item balances went negative, the vial write-offs by cost over the per-dose cost, the tax switch by the
maintenance-only invoices at Schedule B's prices, and the two-store routes split by Schedule B. Reader A and the judge
thread were stopped at the spend.

## Architecture 7 record (spent 2026-10-23)

Architecture 7 read each production day's oxidizer outlet from the relation the ten oxidizers' tests trace (a floor of
about 45 ppmv as carbon, 1.8 per cent of the inlet above about 2,500) at the inlet the day's captured VOC and airflow
imply, against each plant's latest test efficiency (Ashcombe 21 and Kelvedon 20 against 29 and 28). At stage 4 (zip
5ab18e48) reader A read the floor straight off the test tables (Ashcombe's 2018 two-press test holds the same 45 ppmv
at half the inlet), rebuilt each hour's outlet as the greater of the floor and 1.8 per cent of the inlet and landed the
five and all 14 whole tons, Part 2 question 1 "none" and question 6 "an analytical choice"; reader B carried each
fixed-fan unit's test outlet to the year through the register's fan-drive column (R4, six plants). Both readers kept
all 28 ask figures: the revision log read, the payment lines parsed, Haldane matched on description. The judge thread
was stopped at the spend.

## Architecture 6 record (spent 2026-10-22)

Architecture 6 set Form 27A's placement scores from the bank difficulties carried from the old platform's field-test
section (positions 61 to 70) to the positions 21 to 70 the unique items take on Northgate Assess, by the position term
the 2026 attempts measure, against the default path's difficulties as filed (29 and 18 against 30 and 19). At stage 4
reader A rebuilt every response at its delivered position, fitted the Rasch model with the anchor block fixed, found
items harder later in the test on both platforms and landed 30 and 19 exactly (29.48 and 18.50), Part 2 question 1
"none" and question 6 "an analytical choice"; it kept 13 of 62 ask figures (the system totals and some twice counts).
Reader B and the judge thread were stopped at the spend.

## Architecture 5 record (spent 2026-10-22)

Architecture 5 designated rapid price growth areas on each dwelling type's own year effect weighted by the census
stock's value, with a pooled hedonic year term as the default path. At stage 4 both readers and the judge's own
derivation took the type-by-stock aggregation by reflex (type medians or type year effects weighted by the census
stock) and missed the call only on the location control (electoral division), which the judge read as unfiled; filing
it hands all three the call, so the decisive step as designed does not stump and the one that held is a fork.

## Tried and rejected
- Architecture 6, item position effects in pre-equating (2026-10-22, spent at stage 4): reader A fitted a Rasch model
  with a position term to the rebuilt attempts and carried the field-test difficulties to Form 27A's positions,
  unprompted by any sentence. The calibration context has to be recoverable for the truth to be fair (the report's
  delivery section and both exports' positions), and once it is, an analyst who knows the field checks the effect the
  context invites; a context effect measured by an obvious model term is a reflex for the field's own analysts.
- Architecture 6 draw (2026-10-22): re-rooted on the author's standing rule (no retirement) with a fresh world. Screened
  before it and dead: a CEMS gap fill on load (guard BLOCK on pattern G12 and strategy population_selection against
  task273, same-puzzle and same-driver spent in five to seven builds, the statutory filing against task249);
  multiplicative against additive seasonality (task146, task147); a moving holiday (task162, task467, task135);
  Denton benchmarking (this slot, below); retroactive eligibility as a denominator still developing (the completion
  driver of task451 and task479 v5); Fellegi-Sunter frequency weights (set aside at task486's draw against task468's
  linker error); the oldest old by extinct generations (task228); non-detects under several limits (task189).
- Architecture 5, the stock's price change as each dwelling type's own year effect weighted by the census stock's
  value (2026-10-22, spent at stage 4): both readers and the judge's first derivation weighted dwelling types by the
  census stock by reflex (the note's "dwellings the 2022 census counts" and the census workbook by type invite it) and
  missed only on the electoral-division control, which the judge read as unfiled (r5a); filing it hands them the call.
  A stock aggregation over a tabulated type mix is a reflex once the stock is the filed population.
- Architecture 5 draw (2026-10-22): re-rooted on the author's standing rule (no retirement); the world and pack of architecture 4 kept, the decisive step moved from the constant-quality regression its reader 9 found to the aggregation that regression skips (each type's own year effect over the stock's value), with the pooled regression now the default path. At registration the v4 identity BLOCKed on own_lineage, gap population on same-puzzle and same-driver (task251 v5), shape 10 and the statutory filing (task249 v6) and filed_standard (task478 v4); redrawn as recorded in the Draw, the circular changed to settle the 2027 fund allocations.
- Ask B's reissued student ids as a 7-digit id equal to the old one plus a campus constant, linked by birth date, sex and ZIP (2026-10-21, stage 4 round 1): both readers resolved it on the person columns and kept all six headcounts (score_reader 50 per cent); re-sited so the new ids share the old form with no arithmetic tie, birth date, sex and ZIP are shared by different students, and the movers' majors are recoded, so only the four-field key resolves it.
- Architecture 1, a coordinating board's instructional grant with four parents' consolidated returns apportioned by a cost model (2026-10-21, spent at stage 4): round 1's two readers split by FTE or total credit hours and missed; both round 2 readers fitted instruction expense on credit hours by level across the standalone campuses, split each parent's return by the modelled cost and landed the call (exit 1). Pricing activity by level from the units that report alone is a strong reader's reflex once the activity file by level ships beside the combined return.
- Architecture 2, regional register error rates from an audit drawn unequally by a risk screen (2026-10-21, spent at stage 4): both readers checked the audit's composition against the register (35 per cent referred against 8), weighted each stratum to the 30 April register and landed the call; both also read the UTC times into local time and dropped the restored companies (asks 28 of 28). A sample whose composition differs from its frame on a shipped flag is reweighted by a strong reader; a stated clock and a restoration notice are seen devices.
- Architecture 3, registration offices put on a timeliness plan from a quarter's median working days with part of the quarter still open at the extract (2026-10-21, spent at stage 4): both readers censored the open applications at their age, took the Kaplan-Meier median and landed the call, and dated payments by the batch terminal day (asks 28 of 28). An open caseload shipped beside a duration cohort, with a paper saying the open ones count, is read as right-censored by a strong reader; a settlement batch file carrying the terminal day is a seen device.
- Architecture 4, areas' house price change for the rapid price growth designation read from a shifting sample of the stock (2026-10-21, spent at stage 4): reader 9 fitted log price on type, floor area, age, newness and the address point file's electoral division with a year term and landed the call; reader 10 left location out and missed; the block purchases' one consideration on every line held both readers (0 ask totals of 32). A constant-quality index is a strong reader's reflex once the note cites the handbook and the attributes ship; location one join away is not a hidden dimension.
- A district's register error rise tested with the spread of the audit's sampled blocks (2026-10-21, screened at the draw): the guard put it beside task261 (subgroup statistics from one clustered sample, their difference's error from the clusters), the same driver.
- Regional quarterly output benchmarked to annual totals by Denton against pro-rata (2026-10-21, screened): Denton's extrapolation holds the end-of-year ratio, which sits within a few tenths of a point of pro-rata's annual ratio, while a trending ratio puts the truth far from both; the separation is too small and the truth not recoverable without forecasting the ratio.
- Architecture 7 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world.
  Screened before it and dead: gross labour-force flows corrected for reinterview misclassification (task244's
  driver); speededness on a timed form (task249's screen); a winner's curse in form assembly (task471's shrinkage
  coin flip); generic price erosion by entrant count (task484 v1's ramp, screened at task478's draw); percent-of-charges
  hospital contracts carried to each hospital's current chargemaster (the swap test reads it as any list-price
  contract); laboratory results harmonised by proficiency-test bias (the reported result is the measurement, so the
  correction is a fork); a cancer registry's completeness by the flow method (task249's screen); common-stack
  apportionment from single-unit hours (task263's unmixing); a concentration-discharge load (task452 v1, task135);
  change of support for block grades (task270, task254, task273 screens); linkage on an address the outcome changes
  (task468's linker error); calculator-type DIF and released-item drift on the item bank (architecture 6's lesson: a
  context an obvious model term measures).
- v7 stage 3, 2026-10-23: the first tuning let each oxidizer's test outlet carried to the year (its concentration on
  each day's air, or its rate over the year's hours) file the golden five, because a fixed-fan plant at the floor emits
  the same rate every day; Larkmoor Graphics was made a concentrated-test, mostly-dilute plant under 25 tons so those
  routes file six (R4, R4m, R4b).
- v7 stage 3, 2026-10-23: press VOC to one decimal: the standing family spreads up to 0.37 tons on a plant, so the
  figure is graded in whole tons, every member 0.19 tons or more from a half (G4); the CSV's used and captured
  columns went with it (free to both top responses), the CSV now the press VOC and coverage.
- v7 stage 3, 2026-10-23: the tuned plants landed on whole tons (29.00, 37.00); moved to ordinary offsets (G5). Days
  below the tests' lowest inlet at three plants opened an extrapolation fork (interpolated efficiency against the
  floor); the low days were raised inside the tested range.
- Architecture 7, 2026-10-23: spent at stage 4. The decisive relation was visible inside one oxidizer's own tests (the
  same outlet at two inlets) and in the register's fan-drive column, and a regenerative oxidizer's outlet floor is
  field knowledge both readers carried; the asks' devices each sat one file away from a careful reader's path (the
  master's revision log in the same workbook, the washer gallons in readable payment text, descriptions beside the
  renumbered items). Next architecture: a decisive step no table displays as a pattern and no column labels.
- Architecture 8 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world, aimed
  at architecture 7's lesson (no table displays the decisive relation, no column labels it). Screened before it and
  dead: vessel propulsion from AIS speed over ground carried to speed through the water by an estuary's tidal streams
  (a port world beside task472 and task474, and a tidal stream table has no other use in an emissions pack, so its
  presence announces the correction); container ships' at-berth auxiliary load by the reefers on board, calibrated on
  shore power meters (a port world, and a reader calibrating on the meters sees the per-call spread with reefers its
  first explanation); a tanker's boiler load at berth by its own steam cargo pumps on discharge (the at-berth tanker
  rules' own reasoning, a reflex once the transfer log is joined); dairy lagoon methane through the lagoon's
  temperature lag behind the air (the rate model is a filed procedure, and four inspection readings a year cannot fix
  the lag deterministically); switcher locomotives' idling through the start-stop system's restart temperature (a
  rate carried across a weather covariate, task478 v7's driver); crematory mercury by the decedents' dental cohort (a
  composition mix one survey table hands over); breaker SF6 leak rates from temperature-uncompensated pressures (the
  gas temperature at each reading is not recoverable). A cold-chain prototype (thirty-six refrigerators, probe 6 minutes,
  carton 48) put the logger's own hours at two to ten times the vaccine's, the default qualifying 29 against 12, with
  a 45-minute lag fitted on ten fourteen-day overlaps at 0.04 degrees C reproducing the carton's set exactly, while 30
  and 60 minute duration filters (17 and 6) and a 45-minute moving average (20) fell elsewhere and a 90-minute moving
  average missed by one refrigerator: the stage 2 world keeps the default's count plausible and every store clear of the
  line under the standing family.
- v8 stage 3, 2026-10-23: standard 7.1 first read "the records of each store's device of record are its vaccine
  temperature records", which a literal reader takes as the logger's readings being the vaccine's temperature (an
  official decoy for the default path); it became a records-custody clause.
- v8 stage 3, 2026-10-23: under the interval-mean reading of a record's vaccine temperature five stores' whole hours
  moved by one while the call held; 7.3 now files the counting (a record counts its ten minutes by the vaccine's
  temperature at its time stamp), WHAT and not HOW (SF17).
- v8 stage 3, 2026-10-23: return credits from both manufacturers put the cracker's balance below zero at eleven
  stores, a loud failure that points at the double count; only Halvorsen's standard-dose products are returnable, the
  leftovers leaner and the unrecorded losses scaled to each store's volume (cracker 15 doses or more, A6).
- v8 stage 3, 2026-10-23: maintenance-only invoices at one price per unit type tied ten stores' service figures (a
  constant response would have kept them); per-model prices and add-on parts at some visits, every store's figure now
  distinct (B5). With the tax switch as ask B's only silent device a reader who found it kept 23 to 30 of 30; the
  pre-move two-store maintenance routes on one invoice were added, so the tax switch alone keeps 10.
- v8 stage 3, 2026-10-23: the first names sat on real organisations, products or places in or near the field (H21):
  Coldline (a refrigeration manufacturer), Polarwatch (an ocean-data programme), Vaxtor, Homeline, Arctis, Glacier
  Medical, and the acquired chains Rookwood Drug and Saltash Apothecary; renamed Tellvane, Brumal, Stellane, Keswell,
  Brannon, Pendry Medical, Vollmer Drug and Lindqvist Apothecary before any reader saw the pack.
- Architecture 8, 2026-10-23: spent at stage 4. Two instruments recording one unit side by side are compared by a
  strong reader on reflex: the pilot stores' logger and in-carton series parted at every restock and defrost swing, so
  reader B fitted a first-order lag on the overlap with no sentence asking for it. Every ask device had one natural
  check that exposed it (per-item balances, cost per unit, a list price met exactly, one invoice on two sites).
  Next architecture: a decisive step whose evidence no single side-by-side comparison shows, and ask devices that no
  per-item reconciliation or unit-price check reveals.
- Architecture 9 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world. Screened before it and set aside: phantom shelf inventory under a vendor-managed availability guarantee (on-shelf availability is an industry term that names its own correction); a plan directory's ghost providers read from claims (the directory and the claims sit side by side, architecture 8's reflex); a starting dose as the mark of a true initiator in an outcomes contract (population_selection, in the window against task275); rectifying inspection's over-weighted rejected lots (population_selection again); left truncation of a fleet's lifetimes (task133's delayed entry for a taken-over book); GPS chord distance by terrain for fuel-tax jurisdiction miles (the call would sit on a few per cent of one state's miles); meter error read off a system balance (the instrument-bias family task478 v5 and task480 v1 lost to readers); charger uptime from failed sessions (the failure is written in the session record itself). The bike-share draw keeps the listed count correct for what the operator knew and puts the difference in renters' choices, which no record states.
- v9 stage 2, 2026-10-23: the fleet's clock ran four hours off Eastern time after the move to absolute instants (its
  local minute of the day counted from midnight UTC), so the pack showed the morning rush at noon; the window's start was
  re-anchored to 20:00 on 23 September so the fleet's own clock is Eastern time, the trajectory byte for byte the same
  (46,883 trips), the station move and the dock expansions read at 23:00, and Schedule C's minutes taken from Eastern
  time itself; the designations held (W-16 alone against W-02, W-12, W-16, W-19).
- v9 stage 2, 2026-10-23: each station's three months to one decimal put nine of 72 cells within two minutes of a
  printed edge and W-12's lowest month (87.652) within a minute; graded at each station's lowest month in whole per cent
  instead (the tightest ten minutes clear, M1), the margin to one decimal (0.684, eleven minutes), the monthly figures
  kept in the workbook as context.
- v9 stage 2, 2026-10-23: ask B's hours to one decimal put W-18 within a second of an edge; graded in whole hours, each
  pay station's alarm stream chosen so its figure sits 0.08 hours or more inside its bin (M3).
- v9 stage 2, 2026-10-23: the union of overlapping alarms as ask B's device: at whole hours the summed and merged
  spans print alike at every station; kept as texture (B3), the restarts carrying the device.
- v9 stage 2, 2026-10-23: with only the alarms and restarts in the log, ending an open alarm at the pay station's next
  event of any kind kept 15 of 24 hours figures (the restart was nearly always the next event), an honest pair of 45.7;
  the cabinet heater's events on cold days and the service door at reader repairs added, the shortcut keeps 4 (33.1).
- v9 stage 2, 2026-10-23: invented names screened by web search (Wellhaven, Northlane Mobility, Corlund Kiosk
  Systems): no organisation, product or place on any of them in or near the field; Welland, Ontario is three edits away.
- Architecture 9, 2026-10-23: spent at stage 4 on the judge's SEND_BACK. A count the operator's system publishes as
  available, read against a state no record holds (a bike's working order inferred from what renters and the vans did
  with it), is a surface read rejected however the evidence is gathered: on clean data the feed would be right, so the
  judge files Gate G surface_read_rejection and Gate H planted, and with nothing filed saying unreported faults exist
  the records read literally give the feed's answer (competing_defensible_answer). The readers missed the call for the
  same reason the judge refused it. Both ask devices were found: a column filled from a present-day register is undone
  by a work-order log that lists every swap, and a pairing that runs alarms to hundreds of hours with sales inside them
  announces its own repair. Next architecture: a quantity every file visibly lacks (so no surface read stands in for it),
  estimated by a method the data forces, and ask devices whose wrong reading is plausible rather than absurd and whose
  evidence no log lists outright.
- Architecture 10 draw (2026-10-23), no card filed. The guard's window closes survey research for ETL (ban.pairing and
  ban.subdomain against task483, so census-register and seasonal adjustment are both out) and the strategies grain_or_unit,
  population_selection and composition_mix (task483, task275, task179); payment claims, emissions, IRT equating and data
  integration clear it. Screened on those four and dead on file or on measurement: competing exits against censoring
  (task169, task266; the competing exit is a reflex, task133); pooled-test infection rates (task188); age-length keys
  (post-stratification, a reflex once the aged subsample's design ships); a pooled tail share from parts' means and spreads
  (task483's lesson); a population's share past a cut from short matrix-sampled booklets (task464's shrinkage lesson);
  direct against indirect adjustment of a net series (task453 v2's fork); time-series consistency by splicing (task123's
  screen); chance agreement on name and birth date in a voter roll (task468's common-identifier lesson); credibility for
  site emission factors (the regulatory standard takes the site's own tests, a fork); tracer flux ratios (the integrated
  ratio is the method's own definition, so the default is the golden); flows traced through intermediaries to end markets
  (task451 v1's swap failure); uncompensated gas meters (a unit read, data semantics); correlated systematic errors in an
  activity-data uncertainty (the call is a monitoring decision, Data Quality); cohort waits from cumulative counts under
  first-in-first-out (generic queueing, the swap reads the same); a pick log matched to put-aways by each lane's access
  order (drive-in lanes are last-in-first-out, field knowledge a strong reader carries, architecture 7's death).
- Architecture 10 draw (2026-10-24): drawn on the hospice cap after a second screen of the four open ETL task types (survey research still closed by task483). Screened and dead: TRI range codes valued at the exact filings inside each range (the midpoint is the programme's own convention, a competing defensible answer, and the exact filings are one group-by away); charge compression in cost-plus repricing (the implant invoices put the cost-to-charge ratio against the charge in plain view, and the functional form forks); a stopped turbine's nacelle anemometer read through the running transfer function (readers impute from neighbours by habit, and Gate G reads an instrument bias as planted); unconstrained demand on sell-out days (the product-limit estimator is a reflex and converges with the intraday route); time-of-observation bias in daily maxima (the calendar-day maximum is not recoverable from a 5 p.m. reset and the nearest hourly station); trend uncertainty with shared emission factors (propagating through the difference carries the shared factor by construction, so the easy route is right); items dropped from scoring rescored through the test characteristic curve (the published conversion table replays the method); best-of-k seed reports deflated by each recipe's seed spread (the client's GSDS Layer 1 list names best seed against mean as harmonisation); inverter clipping, demand ratchets and dead-time counting losses (each leaves a flat top or a ceiling in the records that announces its correction); unit value against a fixed-basket price index for provider unit cost (composition_mix, banned against task179 for this registration); DIF purification, testing-window instruction time and single-group order effects in equating (field reflexes, or no bias in the equating); register status nowcast by a Markov chain (forecasting, and architecture 9's surface-read refusal); interpolation along a process curve between sparse readings (task478 v6's and task480's degradation and life-cycle families). The first card draft BLOCKed on test.same_puzzle against task171 v4 with G13 decisive; G12 is the honest decisive generator for the step that decides.

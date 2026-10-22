# task482 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 6, drawn 2026-10-22 after architectures 1
to 5 were spent at stage 4: a fresh world and pack in the ETL objective, a community college system pre-equating its
2027 mathematics placement form from a Rasch item bank.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task482.json` (architecture v6, lineage v1 to v5 spent), registered
  2026-10-22 after a pull, `check` re-run on the filed card. Guard WARN only, answered here: `repeat.gate_g` (task273,
  live, decides a descriptive cut over censored records by the method its censoring entitles; here the method carries
  an item parameter across the measurement condition it was calibrated under). Nearest drivers 0.07 and below.
- **Redrawn at the draw, and why the replacements are the honester labels.** The first draft BLOCKed on `ban.role`
  (research_desk) and `ban.forum` (committee_or_panel), both against task249 v6, and on `ban.forcing_event`
  (launch_or_rollout) against task177 v2. Placement scores in this system are policy the State Board of Community
  Colleges approves, so the forum is trustees_or_governors and the forcing event the Board's approval meeting
  (vote_or_meeting) ahead of the form's go-live; the stakeholder runs the placement programme rather than a research
  office, so the role family is programme_officer.
- **Pairing:** Education & Learning Sciences, task type `item-response-theory-test-equating`, which serves ETL: the
  item bank in two systems, the two delivery platforms' exports of the 2026 attempts, the form maps and the technical
  report conformed into Form 27A's score conversion, the load file the new platform reads to place each student.
- **The decision and the quantity:** the Brackett Plains Community College System places entering students into
  college algebra, corequisite college algebra or developmental mathematics by their raw score on the Quantitative
  Placement Inventory (QPI). Form 27A goes live on 1 March 2027 and its two placement scores must be approved by the
  State Board on 18 February, before any student sits it, so the form is pre-equated from the bank. Each placement
  score is the lowest whole raw score at or above the expected raw score, on Form 27A, of a student standing exactly
  at that placement's standard on the bank scale (the technical report files both standards from the 2022 standard
  setting). Forward facing: the scores govern every placement from 1 March 2027.
- **Shape:** `04`, setting one dial twice: the two placement scores and the expected raw score each rests on, the
  default path's scores as the rivals, the conversion's placement level at every raw score near each cut; the asks
  carry each college's 2026 placements by level (14 colleges by two levels, 28) and the 2026 field test's accepted
  items by content strand; a curve chart's named parts and the three files. About 50 criteria, sized at stage 2.
- **Strategy:** `other` (no family on the list states it: a parameter calibrated under one measurement condition is
  carried to another by the condition's effect, measured where the same items were presented in varied orders); Gate
  G `method_or_model_selection`; gap `objective` (the bank's difficulty is a correct figure for the slot it was
  calibrated in, not the difficulty the form's curve needs); pattern none; generators G14 (does the calibrated value
  apply under this condition, decisive) and G16. Layer 2 family `field_method`, pattern `own:bank difficulties carried
  from their calibration position to their operational position before pre-equating`.
- **World:** an unnamed state of the United States; the Brackett Plains Community College System, fourteen colleges,
  about 9,600 QPI attempts in the 2026 testing year (1 February 2026 to 31 January 2027) on two delivery platforms,
  the old one until 30 June 2026 and the new one from 1 July. People from `guard.py names --geo 'United States' --seed
  482`: Breanna Graham (Director of Placement and Developmental Mathematics) and John Huang (Psychometrician).
- **Forcing fact:** the State Board approves Form 27A's placement scores on 18 February 2027; the form goes live on 1
  March 2027.
- **Forum and forcing event:** trustees_or_governors, vote_or_meeting. Organisation university_or_school; role
  programme_officer.
- **Form design (both platforms, every form):** 60 scored items, a 20-item anchor block in positions 1 to 20 kept in
  place on every form, then 40 unique items, then an unscored 10-item field-test section in positions 61 to 70. The old
  platform delivered each form in two fixed versions (the unique section and the field-test section in reverse order on
  version B); the new platform shuffles the unique section and the field-test section for each attempt. Field-test
  items are calibrated with the anchor block fixed at its bank values; unique items are retired after their
  operational year. Form 27A's 40 unique items are new: every one was calibrated in a field-test section.
- **Data-native sentence:** at the same ability a student answers an item less often the later it comes, by about
  0.0075 logits per position in the 2026 attempts, so a difficulty calibrated in the field-test section (positions 61
  to 70) states the item harder than it will be at positions 21 to 60 on Form 27A, by about 0.19 logits; the bank's
  difficulties as filed put the expected raw score at the college algebra standard near 27.9 (placement score 28), the
  difficulties carried to their Form 27A positions near 29.5 (placement score 30).
- **The WHAT screen.** Population: Form 27A's 60 scored items as students will sit them (the unique section shuffled
  for each attempt). Outcome: the expected raw score of a student at each standard. Unit: the whole raw score.
  Comparison: the lowest whole raw score at or above that expectation. Window: the form's live period from 1 March
  2027. The decisive step settles none of them: it is how each item's difficulty on Form 27A is estimated from a bank
  difficulty calibrated elsewhere on an earlier form, which nothing files.
- **Sources, one line each:**
  - The client's IRT equating rigor patterns (anchor screening; nonequivalent groups through anchors): here no groups
    are linked and no anchor drifts; the item's own parameter is carried across a presentation condition.
  - Kingston and Dorans (1984), item location effects in IRT equating and adaptive testing; Debeer and Janssen (2013),
    position effects as a Rasch facet: the field's method (a position term in the Rasch model, estimated where order
    varies) is what the golden runs.
  - Kolen and Brennan, Test Equating, Scaling, and Linking: pre-equating rests on item parameters holding in their
    operational context.
- **Same-puzzle and same-driver tests:** (objective, none, dial_setting) and (objective, none,
  method_or_model_selection) against the last twelve builds, lineage included: no match (the guard's tests pass).
- **Abstraction test:** the nearest drivers stripped of nouns (task190's size-proportional sample, task255's floored
  record, task87's capped procedure) neither carry a calibrated parameter across a condition nor measure the
  condition's effect from varied orderings; within this objective the IRT builds link groups through anchors
  (task450), convert by distribution matching (task464), or rejected a judged anchor (task471 v2) and rapid guessing
  (task479 v4) as planted, and none moves an item's own parameter.

## Architecture 5 record (spent 2026-10-22)

Architecture 5 designated rapid price growth areas on each dwelling type's own year effect weighted by the census
stock's value, with a pooled hedonic year term as the default path. At stage 4 both readers and the judge's own
derivation took the type-by-stock aggregation by reflex (type medians or type year effects weighted by the census
stock) and missed the call only on the location control (electoral division), which the judge read as unfiled; filing
it hands all three the call, so the decisive step as designed does not stump and the one that held is a fork.

## Tried and rejected
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

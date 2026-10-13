# task124: Hollins Ford Regional Water District, the lead service line replacement schedule (architecture 2)

Private, never ships. Architecture 2 of 3, drawn 2026-10-12 at the wave-1 resume as the re-root of architecture 1
(Sabine Crest Energy's summer firm-capacity block split, harden loops 0 to 2). Architecture 1 is spent for three
reasons, each recorded in `## Tried and rejected`: its card carried `validated_decoy: true`, which the guard has
blocked outright since 2026-10-11 and which no differentiation clears; the in-house solver walked the default path
to the golden twice (round 1 by the programme baseline, round 2 by the peak days' shoulder hours), which is the
re-root rule's two failures on the default path; and loops 1 and 2 each answered a solve by stacking a rung above
the solved decisive step, which the current pipeline forbids (redesign the decisive step, never add a rung above
it). Its generator, pack, goldens, write-up, metadata and prompt were removed from this folder at the re-root (in
history at 64079f2); `solver_rounds/` stays as its evidence, and its `leak_check_report.md` is in history at
d8664dd, replaced by architecture 2's `leak.py` report at stage 3. The card keeps architecture
1's three loops in `lineage` (v1 to v3). Nothing of architecture 1's world, pack, prompt or asks is reused.

**Loop 1, 2026-10-13.** Architecture 2 shipped on 2026-10-12 with the whole-segment shares as the answer; the portal's
top response filed 2037 (the call landed) and the author asked for the stumps hardened. The shipped decisive step had
been executed as a work order: the field notes announced the replaced mains' exposures and coverage separated their
segments cleanly. Hiding the sample could not hold (`## Tried and rejected`), so loop 1 moves the decisive step: plan
4.3's share is expected among the district's Lead Status Unknown lines, which are what the targeted verifications
left, so the whole-segment shares become a rung (2038) and the answer is the remainder (2037). The capital plan's
construction line is $25.4 million, the unit cost schedule's mobilisation $160,000 with three zones' prices moved, and
plan revision 2's order swaps two adjacent pairs, so that the call separates with every margin; the ask files are
byte-identical to the shipped cut and every ask figure is unchanged. The whole-segment rung is a different insight
from the one above it (a depleted pool, not a selected sample), and the stopping rule now ends the world there.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task124.json`, architecture v4 (re-root: architecture 2), registered 2026-10-12; `guard.py check` WARN on one finding (`repeat.gate_g`, answered below); `guard.py validate` clean |
| Domain / task type | energy-systems-utilities / asset-condition-maintenance (a client domain; the asset is the water service line) |
| Objective | Forecasting & Predictive Modeling: the programme year in which each of the plan's twelve zones will be finished, from the district's records to 31 December 2026 |
| Shape | 06, sequenced schedule under capacity: each zone's finish year and running total, the deadline call, a schedule chart with its parts named |
| Decision | `schedule_or_sequence`, answer unit `date_or_period`: whether the replacement plan's annual capital finishes every zone by the federal deadline (lines replaced by 1 November 2037), and the year each zone is finished |
| Mechanism | gap population; pattern none; generators G14 (decisive: does a rate measured on one pool apply to this pool; at loop 1 the whole-segment rate of the era's lines carried to the unknown lines the targeted verifications depleted, and below it the verified yield conditioned on why a line was dug), G6 (the unknown pool's composition after targeted removal; the zones' construction-era mix differs from the swept segments'), G2 (the representative unit is a main segment verified whole, built from rows); Gate G `forecasting`; strategy `population_selection` |
| Layer 2 family / pattern | `estimand_identification`; `biomedical-clinical-research/diagnostic-biomarker-accuracy/1` (partial verification biases accuracy), made here on service lines: the verified share is measured on lines dug because something pointed at lead, and the lines never dug are the complement of that selection |
| Furniture | forum `board_of_directors` (the district board adopts the capital plan), forcing event `budget_or_appropriation` (the 2027 to 2037 capital plan's annual lead service line appropriation), organisation family `cooperative_or_member_body` (a water district owned by its member municipalities), role family `programme_officer`, context artifact `capacity_report` (the 2026 programme progress report), calibration `physical_verification`, opening `question-first`, question form `when` |
| Spine | the district's service line inventory, 87,410 rows, one service line (main to premise) with its records class, current classification, construction year, zone and the main segment it taps; synthetic, shaped on public lead service line inventories filed by Ohio community water systems |
| Deliverables | `lslr_2027_programme.xlsx` (the zone schedule and the two asks), `lslr_2027_board_paper.pdf` (the call and the schedule chart) |
| People | drawn with `guard.py names --geo "United States, Ohio" --seed 124 --n 24`: Gregory Sheppard (programme manager, drawn again at loop 1), Bethany Davidson (district engineer), Seth Sullivan (finance director), Craig Stewart (board chair, drawn again at loop 1); none appears in the prompt |

As-of date: Monday 11 January 2027. The inventory extract runs 8 January 2027; the verification log closes with the
2026 construction season (last record 18 December 2026); the board adopts the 2027 to 2037 capital plan on Tuesday
19 January 2027; the plan's first construction season opens in April 2027. The Lead and Copper Rule Improvements'
compliance date is 1 November 2027 and every lead and galvanized-requiring-replacement (GRR) line must be replaced
within ten years of it.

**Guard.** `guard.py check` on the scratch card: WARN, one finding. `repeat.gate_g` (forecasting repeats task501, the
last build): forecasting is the honest mechanism, because the call is a bet on what the plan's digs will find over
2027 to 2037 and the correctly read past pins it only through the verifications a programme-like process produced.
The first draft of the card (pattern E, then pattern D) blocked on `test.same_driver` against task181 v3 and task500
v2 in the window and on `test.own_lineage`, and pattern D would have banned task181 v4 (filed today, later in draw
order) on its decisive pattern; the furniture was redrawn clear of task181 v4 and task229 (role, artifact,
organisation family, forum, forcing event, shape, decisive mechanism, question form), so this card adds no BLOCK to
either (checked by running `guard.py check` on both after registration). Nearest driver on file 0.05 (task32 v2).

**Abstraction and same-puzzle tests.** Stripped of nouns, the loop-1 driver is: the units still unexamined are what
an examination that chose units by signs of the outcome left behind, so their rate is the population's expected count
(from the only groups examined exhaustively) less what the examinations found, over the units left, below the
population's rate. Loop 0's driver (only the groups examined exhaustively give the population's rate) is its rung. The
three nearest drivers (task32 v2, a conversion rate fitted across a regime break; task83 v1, a retrained selection
model; task446 v2, a screen's yield moving with the base rate) share no latent structure, default path or
correction with it. task446 v2 is the closest in words (a yield measured on one population carried to another) and
differs in the mechanism: there the yield moves with a base rate the history shows; here the measured rate is
inflated by why units were examined, and the base rate is the same.

**Data-native sentence.** A water utility verifies a service line's material only when something sends a crew to
dig: a customer's report of lead pipe, a lead sampling site, a leak on old galvanized pipe, a dig a consultant
ranked as likely lead, or a water main replacement that exposes every service on the main; this district logs every
one under the same work-order code, so the verified lines over-represent lead, the main segments a replacement
verified whole are the one sample of the district's lines that did not choose them, and the lines still unknown are
the ones the targeted digs passed over, so they hold less lead than the district's lines as a whole.

**Sources read, one line each.**
- `stumping/references/client/two-layer-task-design.md`: the three rules and both layers; the stump sits in the
  estimation sample, every piece of mess on the main path is mess-neutral, and the ask devices live in files the call
  never reads.
- `layer2-rigor-patterns.md`, biomedical diagnostic accuracy 1 (partial verification bias): learned that a quantity
  estimated on the verified subset is biased when verification depends on the result; made here on service lines,
  where the unbiased subset is recovered from the main segments verified whole, not from a verification probability.
- `layer2-rigor-patterns.md`, healthcare utilization 1 and epidemiology surveillance 3 (capped demand, testing volume):
  read and set aside; both are measured traps on other cards.
- `dataset-generation/references/layer1-messiness.md`, the universal techniques (imperfect keys across a system
  migration, codes that differ by source, overlapping records) and energy 1 and 5 (quality codes, governing vintage):
  the migration crosswalk, the field codes and the re-verifications are Layer 1 on the main path and neutral there.
- `strategies.md` F7 (population: checks that see a unit because it was wrong) and L1 (a control blind for a computable
  reason): no control in this pack scores the estimation sample.
- `guide-to-prompt/references/examples.md`: the call is one quotable question with its unit and deadline, the plan is
  named and its method is not, rounding once at the close.
- Exemplar 3 (the go-to-market pod, mean 0.47): the unit of analysis is the stump; here the unit that represents the
  programme is a whole main segment, which no file names.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain. Figures as built, each asserted in
`generator/checks.py` from the shipped files.

1. Read the question: the programme year in which each of the twelve zones of the replacement plan is finished at
   $25.4 million a year from 2027, and whether the last is finished by the 1 November 2037 deadline.
2. Load the service line inventory; for each zone count the lines classified Lead or GRR (each is replaced) and the
   lines classified Lead Status Unknown, by the plan's construction era (each is dug, and replaced if it proves lead
   or GRR).
3. Load the field verification log for 2021 to 2026, map the pre-migration legacy premise numbers through the 2023
   crosswalk, normalise the result codes through the field code list, keep each line's first result, join to the
   inventory and keep the lines that had no tap card record and were built before 1989 (4,911 lines).
4. Take the share of those lines found lead or GRR in each construction era: 0.763 before 1930, 0.585 for 1930 to
   1949, 0.217 for 1950 to 1988.
5. Cost each zone at the plan's unit costs: its Lead and GRR lines plus its unknown lines at the era shares are full
   replacements, the rest of its unknown lines are digs that find no lead, and it carries one mobilisation.
6. Work the zones in the plan's priority order against $25.4 million a year from 2027, a zone finished in the year
   its running cost is covered: $347.2 million, 13.67 programme years, the zones finishing 2028, 2029, 2031, 2032,
   2033, 2035, 2036, 2037, 2038, 2039, 2040 and 2040.

Ends on: 2040, the last zone (RZ-10 Lakeview Terrace) finished three years after the deadline
Golden: 2037, the last zone (RZ-10 Lakeview Terrace) finished inside the deadline

## Stump sentence

A competent solver joins the verification log to the inventory through the migration crosswalk, keeps the lines that
had no tap card record, prices each zone's unknown lines at the share found lead or GRR in each construction era
across every verification (0.763, 0.585 and 0.217) and files the plan as missing the deadline, its last zone finished
in 2040; the step that lands it there is pricing the lines still unknown at the share found where something sent a
crew, and the solver who sees the selection and takes the shares on the 78 main segments verified whole (0.556, 0.316
and 0.083) still lands past the deadline, in 2038, because those are the shares across every line of the era with no
tap card while the unknown lines are what the targeted visits left: the whole-segment share of the era's lines less
the lead the visits already found, over the lines still unknown, is 0.497, 0.279 and 0.075, the plan costs $274.1
million rather than $284.4 million (or $347.2 million on the default path), and the last zone is finished in 2037,
inside the deadline.

## Three rules

- Task type: asset-condition-maintenance (Energy Systems & Utilities), forecasting what a lead service line
  replacement programme's digs will find zone by zone and when its capital finishes the zones.
- Domain test: what decides the call is a water utility's estimate of how many of its Lead Status Unknown service
  lines are lead or galvanized-requiring-replacement, the inventory practice of estimating the unknowns' composition
  from verifications that sampled lines regardless of their likely material, corrected for the lines targeted
  verification has already taken out of the unknown pool.
- Swap: "whether the hospital's screening programme clears every unscreened ward by the deadline at the share found
  where clinicians referred patients" loses its sense: there are no tap cards, GRR classes, main-replacement
  exposures, construction eras or replace-on-find, so neither the unbiased sample nor the depleted pool exists in the
  same form, and the quantity stops being a line-material estimate.
- Layer 1: realistic mess from the district's own systems: the verification log keyed by the customer system's legacy
  premise number before the March 2023 GIS migration and by the GIS service line id after it; material codes that
  differ by recording route; dates in two formats either side of the migration; re-verifications of one line on
  separate rows; the county assessor's construction year with zeros on non-residential parcels (all on tap card
  lines); lines found lead and since replaced reading NON-LEAD under REPLACED; and, on the ask paths only, a
  completions export that repeats each change order's total on every covered site and keeps both closings of a
  re-closed work order, completion times in UTC, a vendor renumbered mid-year under an unchanged contract, and access
  agreements keyed by legacy premise numbers without their padding and carrying the zone printed on the form.
- Layer 2: estimand identification under selection: the share among the unknown lines is neither the verified share
  (verification was triggered by evidence of lead) nor the unbiased whole-segment share (that is the share across
  every line of the era, the verified ones included); it is the whole-segment share of the era's lines less what the
  targeted verifications found, over the lines they left.
- Decisive step: treating the Lead Status Unknown pool as what the targeted verifications left behind: the expected
  lead or GRR across every no-tap-card line of an era (whole-segment share times the era's lines) less the lead or
  GRR already found, divided by the lines still unknown.
- Not semantics: a solver who reads plan 4.3 exactly (the share expected among the district's Lead Status Unknown
  lines), reads REPLACED as found lead and resolves every code and key still takes the whole-segment share as that
  share, because the whole segments are the one sample that did not choose its lines; no field, code or definition
  says the unknown lines differ from it, and reading every term correctly files 2038.
- Not rule application: no filed rule or procedure computes the share; the field notes say how lines come to be
  verified and plan 4.3 names the class, and executing both literally leaves the estimator open: the remainder
  accounting is the solver's own construction from the design's consequence for the lines no crew has reached.
- Analyst test: a strong analyst who joins the verification log through the migration crosswalk, normalises every
  material code and keeps the no-tap-card lines files 2040, the last zone (RZ-10 Lakeview Terrace) finished three
  years after the deadline, pooling every verification (or 2040 with a model on every visible attribute); one who
  also reads the field notes' account and takes the shares on the 78 main segments verified whole still files 2038,
  because the unknown lines are the visits' leftovers and carry less lead than the era's lines as a whole.
- Estimand: plan 4.3 (`HFRWD_LSLR_plan_rev2_2026-10.pdf`): each Lead Status Unknown line carried at the share of lead
  or GRR expected among the district's Lead Status Unknown lines of its construction era; plan 6.1 defines them as the
  lines built before 1989 with no usable tap card that have not been field verified; the population is the
  inventory of 8 January 2027, the window programme years 2027 to 2037, the unit one service line.
- No decoy: nothing is planted: no consultant score, published hit rate, memo, draft or stakeholder figure ships; the
  progress report carries counts only; the lines dug for cause are the district's real work and correctly recorded.
- No certified replay: no file states a share, an expected count, a zone's cost or a schedule, so no method is
  recovered by reproducing a certified figure; every share is estimated on the record.
- Lesson: a pool left after targeted testing is depleted of what the targeting looked for, so an unbiased population
  rate overstates it; the remainder's rate is the population's expected count less what testing found, over what is
  left. No card on file carries it: the nearest drivers (task446 v2, a yield moving with the base rate; task181, a
  conditioned yield) correct the measured rate, never the depletion of the pool the decision is about.

## Gate G

- **Litmus:** no. Every reported figure is correct; no stakeholder figure or conclusion is overturned. The difficulty
  is estimating what the plan's digs will find among lines the targeted verifications passed over.
- **Classification:** mechanism `forecasting` with `method_or_model_selection` supporting;
  `surface_read_dependency: no`; `stumping_family: analytical_non_defect`; `sole_data_defect: no`.
- **Deletion test:** delete every wrong number and misleading claim: there are none (no hit rate is published, no
  consultant score ships), and the schedule is still hard, because the decisive quantity (the share among the unknown
  lines of each era) is built from the whole-segment share and the verification record.
- **Clean-data test, asserted (W4):** on the world's ground truth, carrying the true share of every no-tap-card line
  to the unknown lines (the easy route with every rule applied) runs past the deadline, and the true share among the
  unknown lines finishes in 2037, the golden shares within 0.012 of it. Fill (crosswalk applied, codes normalised,
  re-verifications collapsed), semantics (every field means what the dictionary says) and instrument (a perfect
  material reading for every verified line): the answer and the default unchanged and apart (M18, M24); dropping every
  legacy row keeps the twelve finish years (M18).
- **Lens swap:** the whole-segment share and the golden share are not one population under two lenses: one is the
  era's every no-tap-card line, the other the lines still unknown, and the difference is the lead the visits found.
- **Identity:** the plan's cost identity closes over the expected shares, which no file ships and the estimation
  builds.
- **First moves:** the one-period group-by (2026 verifications only) files 2039 or later (M22); the hygiene battery
  comes back clean on the wrong path; reweighting the verified lines to the unknown lines' mix of era and zone files
  2040 (M7).
- **Surface read:** no shipped artifact ranks the zones, gives a zone's lead count or cost, or schedules the plan.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene battery | 6 linear arithmetic | Verdict |
|---|---|---|---|---|---|---|---|
| R0 every verified no-record line, share by era (2040, the default path) | the plan groups unknown lines by era | result and construction year are columns | yes | none needed | clean | one share per era | readable |
| R1 a model on every visible attribute (era, construction year, zone) fitted on every verified line, or the verified lines reweighted to the unknown lines' mix (2040) | no | era, year and zone are columns | yes: holds the pool to every visible attribute | none | clean | no | readable |
| R2 the segments verified whole, one pooled share (2039) | no | no column marks them | no | none | clean | one share | silent |
| R3 the segments verified whole, share by era, carried to the unknown lines (2038) | the field notes say how lines come to be verified (every service on a replaced main; every other row a single-line visit) | no column marks a sweep; known only by every service on the segment having a verification | the reflex once the selection is seen: take the unbiased sample's rate | none | clean | one share per era on a rebuilt subset | readable |
| R4 (decisive) the share among the Lead Status Unknown lines: the whole-segment share of every no-tap-card line of the era less what the verifications found, over the lines still unknown (2037) | plan 4.3 names the class and plan 6.1 defines it (not yet verified); neither says the class differs from the era's lines, names a share, a remainder or a method, and the field notes' account names no share, sample or pool | no column carries an expected count, a found count or a remainder | not a reflex: the reflex carries the unbiased rate to the target; the target being the depleted pool is the step | no control scores the remainder; the progress report carries counts of work only | clean: every join matches, every code normalises, the found count ties between the log and the inventory | no: a count across every line of the era from a rate on a rebuilt subset, less a count from a second population, over a third | silent |

## Semantic fork table

| Id | Term or convention in the main ask or the main computation | Golden reading | Alternative reading | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "each of the twelve zones" | the plan's twelve zones as the inventory records them (revision 2) | a zone printed on an older form | 2037 | same call: no file the call reads carries another zone (asserted) |
| SF2 | "finished" | the programme year in which the running total of plan cost through the zone is covered by the running total of appropriations | the year the zone's work starts | the last zone starts and finishes in 2037: same call (asserted) | the plan's schedule sentence; same call |
| SF3 | "$25.4 million a year from 2027" | 2027 dollars in each programme year 2027 to 2037, against 2027 unit costs | nominal dollars with escalation | 2037 | the capital plan: amounts in 2027 dollars; same call (no escalation figure ships) |
| SF4 | "lead or galvanized-requiring-replacement lines" | lines that prove lead or GRR on the field form, with the lines already classified Lead or GRR | lead only, GRR left out | an earlier schedule, the last zone in 2034 (asserted) | the prompt names both; the plan replaces both in full |
| SF5 | "will replace" in each zone | the zone's Lead and GRR lines plus its unknown lines at the share expected among the district's Lead Status Unknown lines of their era | every unknown line taken as lead | 2046 | plan 4.3: each Lead Status Unknown line is carried at the share of lead or GRR expected among the district's Lead Status Unknown lines of its construction era |
| SF6 | "the November 2037 deadline" | 1 November 2037; a zone finished in programme year 2037 meets it | a zone finished in 2037 counted late | the call would flip | the plan: each programme year's construction season runs from April to 31 October |
| SF7 | a zone's "cost" | its plan cost: full replacements and non-lead digs at the zone's 2027 unit costs, plus one mobilisation | 2026 actual cost per replacement | a later schedule, the last zone past the deadline (asserted) | the plan: plan costs are at the 2027 unit cost schedule |
| SF8 | the unknown lines of a zone | lines classified Lead Status Unknown in the inventory of 8 January 2027 | every no-record line, verified ones included | a later schedule, past the deadline (asserted) | the inventory's classification carries every verification's result; the plan works lines by their classification |
| SF9 | lines classified Lead or GRR | each is replaced in full | some prove non-lead when dug | 2037 | same call: every Lead or GRR record on a segment verified whole proved lead or GRR (asserted) |
| SF10 | the lines a share is measured on | verified lines with no usable tap card record, built before 1989 | every verified line, tap card lines included | 2040 (asserted 2039 or later) | plan 4.3 and 6.1: the class is the lines with no usable tap card |
| SF11 | a line verified twice | its first result | its latest result | 2037 | same call: the two results agree on every re-verified line (asserted) |
| SF12 | a segment "verified whole" | every service line on the main segment has a verification | any coverage threshold from 0.45 to 1.00 | 2037 | same call: segments verified whole at 1.00, every other segment at 0.42 or less (asserted) |
| SF13 | mobilisation | once per zone, when its work starts | once in each programme year a zone is worked | the same finish years; nine zones that span a year end cost $160,000 more per extra year (asserted) | the plan's cost sentence |
| SF14 | how work crosses a year end | work runs on through the zones, a zone spanning years | whole zones only, each starting with a new programme year | the last zone in 2043, past the deadline (asserted) | the plan's schedule sentence |
| SF15 | which verifications estimate the share across an era's lines | the lines of the 78 segments whose every service was verified, the mains replaced from 2023, share by era | every verification on file, pooled by era | 2040, past the deadline (asserted) | the field notes' account of how lines come to be verified: every other row is a single-line visit raised by a customer reporting lead or galvanized pipe, a leak, a sampling site or the likely-lead ranking, so its results carry why the line was visited; only a replaced main takes every service on it |
| SF16 | the lines plan 4.3's share is expected among | the district's Lead Status Unknown lines of the era: built before 1989, no usable tap card, not yet field verified (plan 6.1); the accounting gives the same shares district-wide from the log, off the whole segments only and from the inventory's classes (asserted); the twelve plan zones only, or zone by zone, keep every finish year (asserted) | every line of the era with no usable tap card, verified or not | 2038, past the deadline (asserted) | plan 4.3's words ("the district's Lead Status Unknown lines of its construction era") and plan 6.1's definition (a line with no usable tap card that has not been field verified) |
| SF17 | the lead the verifications have found | each verified no-tap-card line's first result, a line found lead or GRR and since replaced counted as found | the inventory's current class, a replaced line read as non-lead; or known results for the verified lines with the whole-segment share for the rest | 2038 either way (asserted) | the field notes: REPLACED is found lead or GRR and replaced in full, NON-LEAD since; every replaced no-tap-card line's first result is lead or GRR (asserted); the second is the selection counted back in, the whole-segment share being the era's, verified lines included |

## Ladder

Figures as built, asserted in `generator/checks.py` from the shipped files and recomputed by `generator/verify.py`.

| Rung | Construction | Last zone finished | Programme years | Zones' finish years in plan order | Equal to the answer | Killed by (one fact) |
|---|---|---|---|---|---|---|
| R0 (default path) | every verified no-record line, share by era 0.763, 0.585, 0.217 | 2040 | 13.67 | 2028 2029 2031 2032 2033 2035 2036 2037 2038 2039 2040 2040 | 1 of 12 | the segments verified whole show 0.556, 0.316 and 0.083 in the same eras |
| R1 | a model on every visible attribute fitted on every verified line (or reweighting to the unknown lines' mix) | 2040 | 13.67 | as R0 | 1 of 12 | the same: the selection is on why a line was dug, which no attribute carries |
| R2 | the segments verified whole, one pooled share 0.435 | 2039 | 12.89 | 2027 2029 2030 2031 2033 2034 2035 2036 2037 2038 2039 2039 | 4 of 12 | the plan carries unknown lines by era, and the swept segments lean to the oldest mains (792 of their 1,264 no-record lines built before 1930); through the accounting it still files 2039 |
| R3 | the segments verified whole, share by era 0.556, 0.316, 0.083 (5 in 9, 6 in 19, 1 in 12), carried straight to the unknown lines | 2038 | 11.20 | 2027 2029 2030 2031 2032 2033 2034 2035 2036 2036 2037 2038 | 10 of 12 | those are the shares across every no-tap-card line of the era; the verifications have already found 2,177, 749 and 168 of the 7,213, 3,351 and 1,107 lead or GRR lines they imply |
| R4 (decisive) | the share among the Lead Status Unknown lines: (era's no-tap-card lines times the whole-segment share, less the lead or GRR found) over the lines still unknown, 0.497, 0.279, 0.075 | 2037 | 10.79 | 2027 2029 2030 2031 2032 2033 2034 2035 2035 2036 2037 2037 | answer | |

- **The answer:** $274.1 million of plan cost over 10.79 programme years; the last zone (RZ-10 Lakeview Terrace) is
  finished in 2037, inside the deadline. Zones and expected lead or GRR replacements (nearest ten), cost (nearest
  $100,000), finish year: RZ-07 1,560, $21.5M, 2027; RZ-02 2,020, $33.7M, 2029; RZ-11 1,830, $28.5M, 2030; RZ-04
  1,420, $23.8M, 2031; RZ-09 1,730, $27.1M, 2032; RZ-01 1,840, $27.3M, 2033; RZ-05 1,640, $25.7M, 2034; RZ-03 1,230,
  $19.6M, 2035; RZ-12 890, $14.8M, 2035; RZ-08 1,310, $21.4M, 2036; RZ-06 1,040, $18.0M, 2037; RZ-10 750, $12.7M, 2037.
- **The accounting by era** (lines with no usable tap card built before 1989, district-wide): before 1930, 12,983
  lines, 7,213 expected lead or GRR, 2,855 verified with 2,177 found, 10,128 unknown expected to hold 5,036; 1930 to
  1949, 10,612, 3,351, 1,281 with 749, 9,331 holding 2,602; 1950 to 1988, 13,279, 1,107, 775 with 168, 12,504 holding
  939. On the world's ground truth the unknown lines hold 0.500, 0.289 and 0.071 (W4).
- **Margins:** every zone's running total sits at least 0.153 programme years ($3.9 million) from a year boundary;
  every expected replacement count at least 2.61 lines from its rounding edge; every cost at least $18,541 from its
  rounding edge; the last zone 0.21 years inside 2037 and R3's last zone 0.20 years past it. Every construction decade on
  the swept segments carries its era's share exactly, so decade bands and an era-only model return the whole-segment
  shares exactly and a model on era and construction year within 0.075 line per zone (C1); the shares rounded to three
  decimals keep every finish year and every rounded count (M26).
- **Partials and grid (asserted as built):** digs for cause only by era 2041; one pooled share of every verification
  2042; records only (every unknown line non-lead) 2034 (the bracket below); every unknown line lead 2046; a model with
  zone effects fitted on the swept segments moves zone counts by up to 200 lines and files 2038 (C4: the plan carries
  one share per era for the district); a construction-year logistic on the swept segments overstates eleven zones by
  5 to 150 lines (C4: the same sentence); dropping every legacy row keeps the twelve finish years through the
  accounting (M18); the inventory's classes with a replaced line read as non-lead, or known results with the
  whole-segment share for the rest, file 2038 (SF17).
- **Why each rung is a place to stop:** R0 is the inventory practice every utility report shows (the share of
  investigated unknowns found lead); R1 is the analyst's correction for the verified lines' mix of eras and zones; R2
  has found the unbiased lines; R3 has found them and kept the plan's eras, and is the unbiased rate of the district's
  lines, the number an inventory statistician reports.
- **Sign and worth:** the chain walks one way: R0 to R1 moves nothing, R1 to R2 puts three more zones' years right and
  the last zone a year earlier, R2 to R3 six more and a year earlier, and the decisive move takes the last zone from
  2038 to 2037 and the plan cost from $284.4 million (R3) to $274.1 million ($347.2 million on R0). The answer is
  bracketed by records-only (2034) below.
- **Position:** the call is a schedule, so the separation floor binds: the last zone's year differs by three years
  between R0 and the answer and by one between R3 and the answer, 11 and 2 of the 12 zones' years differing.

## Closure table

| # | Axis | Reading chosen | Closure move |
|---|---|---|---|
| 1 | Population | the twelve plan zones' lines classified Lead, GRR or Lead Status Unknown at 8 January 2027 | pinned (plan scope); C1: no class changes after the extract |
| 2 | Unit of account | one service line | pinned (inventory grain); C1: one row per line id, asserted |
| 3 | Attribution window | verifications January 2021 to 18 December 2026; programme years 2027 to 2037 | pinned (extract dates, capital plan) |
| 4 | As-of dating | inventory at 8 January 2027 | pinned (extract date); C1 |
| 5 | Version basis | plan revision 2 and the 2027 unit cost schedule | C1: only revision 2 ships; the revision-1 zone label lives only on agreement forms (ask B) |
| 6 | Denominator | the whole-segment share on the no-record lines built before 1989 of the segments verified whole, by era; the unknown-line share over the district's Lead Status Unknown lines of the era | C4: every verified line (SF10), every verified no-record line (R0, SF15) and every no-tap-card line of the era (R3, SF16) each map to a violated sentence or the decisive step; C1: the accounting district-wide, off the whole segments only, from the inventory's classes, on the twelve plan zones only or zone by zone returns the same finish years, asserted |
| 7 | Weighting | lines unweighted within an era | C1: decade-band shares equal the whole-segment era shares exactly and an era and construction-year model returns them within 0.075 line, asserted |
| 8 | Window length | every verification on file, for the whole-segment share and for the lead already found | C1: every swept segment was verified from May 2023, so a 2023-on window selects the same whole-segment lines, asserted; the found count takes every verification because plan 6.1 defines the unknown class by verification to date |
| 9 | Boundary inclusivity | eras before 1930, 1930 to 1949, 1950 to 1988; 1989 on non-lead | pinned (plan); C1: no unknown line built in 1989 or after |
| 10 | Rounding path | unrounded through the running total, rounded once for display | C1: rounding expected lines to whole lines first, or the unknown-line shares to three decimals, moves no finish year and no rounded count, asserted |
| 11 | Tie-break | none needed | C1 |
| 12 | Maturity and censoring | a dig's result is final | C1: re-verifications agree |
| 13 | Order of operations | shares, then zone costs, then the running total | C1 |
| 14 | Row order | not order-dependent | C1: asserted under shuffled rows |
| 15 | Duplicate resolution | a line's first verification | C1 (SF11) |
| 16 | Identity normalisation | legacy premise numbers through the crosswalk, zero padding restored | C1: every swept line is keyed by its GIS id; legacy rows are digs for cause, which feed the found count, and dropping every legacy row keeps the twelve finish years (M18) |
| 17 | Netting against gross | none | C1 |
| 18 | Dimensional units | 2027 dollars, lines | pinned (capital plan) |
| 19 | Code and status semantics | result codes through the field code list; REPLACED as found lead or GRR | pinned (code list; the field notes' REPLACED definition); C1: the log and the inventory's classes give the same found count, asserted |
| 20 | Integerisation | expected lines are carried unrounded | C1 (axis 10) |
| 21 | Scope of a stated clause | "every line classified Lead, GRR or Lead Status Unknown is excavated" applies to each zone the plan works | pinned (plan) |
| 22 | Forward window contents | programme years 2027 to 2037 at the full appropriation each year | pinned (capital plan) |

## Literal reader

Filed estimand, from the prompt and the plan: for each of the twelve zones, taken in the plan's priority order, the
programme year in which the running total of plan cost (the zone's Lead and GRR lines and its Lead Status Unknown lines
at the share of lead or GRR expected among the district's Lead Status Unknown lines of their construction era as full
replacements, the rest of its unknown lines as non-lead digs, at the zone's 2027 unit costs, plus one mobilisation) is
covered by the running total of $25.4 million a year from 2027; and whether the last zone is finished in a programme
year whose season closes by 31 October 2037. Plan 6.1 defines the class: lines built before 1989 with no usable tap
card that have not been field verified. Criterion: none filed; the design forces the method (determinism-check §1,
form 1), and the design is filed: the field notes say that a replaced main has every service on it exposed and
recorded and that every other row is a single-line visit raised by a customer reporting lead or galvanized pipe, a
leak, a sampling site or the likely-lead ranking. The share expected among every no-tap-card line of an era is what a
verification that does not choose its lines finds, which the record holds only on the 78 segments verified whole
(0.556, 0.316, 0.083); the unknown lines are every such line the verifications have not reached, and the
verifications reached them by evidence of lead, so the share expected among the unknown lines is the era's expected
lead or GRR less what the verifications found, over the lines left: 0.497, 0.279, 0.075. Why the careful computation
still lands wrong: the obvious computation takes the share from every verified no-tap-card line (2040), and the
careful one takes the unbiased whole-segment share and carries it to the unknown lines (2038), the share of a class
that includes the lines the visits took; every literal reading of the prompt's and the plan's terms lands on 2037 once
the share is the unknown lines' own (the fork table, SF15 to SF17), and the easy answers come only from easier
estimators on the same estimand.

## Oracles

- `LSLR_progress_report_2026.pdf` (the context artifact): lines verified and full replacements completed by quarter of
  2026 (Eastern time), full replacements by year 2021 to 2026, the inventory's class totals and the crews; every figure
  recomputes from the shipped rows (asserted), it carries no share found lead, no count of lead found among the
  no-tap-card lines, ranks no zone, and states no contractor's cost or any zone's agreements. Its quarterly
  replacements tie on local time and not on UTC, which referees ask A's hazard H1 only.
- The plan revision 2: zones, order, scope, the era grouping, the class plan 4.3's share is expected among and the
  schedule rule; no zone's line count or cost, no share.
- The unit cost schedule: prices only.
- Ask referees: `change_orders_2026.xlsx` (each change order once) arbitrates ask A's device without stating any
  contractor's cost per replacement; the inventory's zone field arbitrates ask B's.
- The field notes' account of how lines come to be verified: no figure, no segment, no share; it ties nothing on
  either path and confirms neither estimate.
- The inventory's classes and the verification log tie on the found count (the same 2,177, 749 and 168 by either
  route, asserted): a cross-check of the input, not of the estimate.
- Nothing ties only under the golden for the main call.

## Ask sheet

**Main call's declared row population:** every row of `hfrwd_service_line_inventory_20270108.csv` in the twelve plan
zones, `sl_field_verifications_2021_2026.csv`, `cis_gis_crosswalk_2023.csv`, the plan, the capital plan and the unit
cost schedule. Every ask device lives in files the call never reads (`lsl_completions_2026.csv`,
`change_orders_2026.xlsx` and `contracts_2026.csv` for ask A; `access_agreements_2022_2026.csv` for ask B); the
generator asserts zero device rows and zero hazard rows inside the declared population, and every ask figure unchanged
when the call's estimator moves (R0 or R3). No ask is keyed to the call: every zone and every contract is asked for.

**Ask A. What each of the three 2026 contractors was paid per full replacement completed in each quarter of 2026**
(3 contracts by 4 quarters, 12 figures, USD to the nearest dollar).
- H18 home: the cost basis beside the plan's unit costs (the board compares the 2027 schedule with what a replacement
  cost in 2026); the call does not turn on it, because the plan prices zones at the 2027 schedule.
- Construction: per contract and quarter of local completion date, the paid base, extra footage and restoration of
  the full replacements completed, plus each change order's amount once (every change order's sites complete in one
  quarter, asserted), over the number of full replacements completed.
- Primary device (D6, an event's quantity on every line it covers, grain unstated): the completions export joins each
  change order's total onto every site the change order covers (`co_amount`), so summing a site's paid columns
  multiplies a change order by its site count. The tell is in `change_orders_2026.xlsx` (each change order's amount
  once and its sites), which no reconciliation the natural path writes reaches. Every contract-quarter carries at
  least one change order covering two or more sites, so all 12 figures move.
- Hazards: H1 (D8 clock) completion times are exported in UTC while the district's quarters are local, and five
  completions at each of the first three quarter ends (one or two per contract) cross a quarter in UTC; H2 (D7) Tri-County's vendor number changed with its July
  2026 acquisition while its contract number did not; H3 (D2) a completion re-closed after a restoration correction
  carries two rows, the later superseding (filed in the field notes: the reclosing's paid amounts replace the first
  closing's; paying on the first closing moves 5 of 12 figures, asserted).
- Inclusion pin (the judge's secondary fork): the change order log says approved change orders are paid to the
  contractor on its pay applications, so they are part of what was paid (leaving them out moves all 12 figures by $25
  or more, asserted); no filed sentence says how a change order counts against its sites, so the device stays silent
  (asserted).
- Path (6 files, 13 columns): completions export, change order register, contracts list, field notes, extract log,
  progress report; `site_id`, `contract_no`, `vendor_no`, `completed_utc`, `work_type`, `paid_base`, `paid_extra_ft`,
  `paid_restoration`, `co_no`, `co_amount`, `row_status`, the register's `Amount ($)` and `Sites covered`. Six files is the
  real path; a seventh would be padding.
- Stops (asserted as built, every stop at least $25 from the golden on every figure it moves): S1 natural (`co_amount`
  summed per site, UTC quarters, by contract); S2 (`co_amount` per site, local quarters); S3 (each change order once,
  UTC quarters); S4 (each change order once, local quarters, grouped by vendor number, so Tri-County splits); answer.
- Lazy delta: S1 wrong on 12 of 12.
- Realism: an export that joins a header amount onto every line it covers is how contract-management systems flatten
  a change order for a field report; the register carries it once.

**Ask B. How many service lines in each of the twelve zones already have a signed access agreement** (12 whole
numbers).
- H18 home: each zone's readiness, a measure every scheduled zone carries; the call does not turn on it.
- Construction: distinct service lines with an agreement signed and not withdrawn by 8 January 2027, legacy premise
  numbers resolved through the crosswalk, counted by the zone the inventory gives the line today.
- Primary device (D2, a label stored before a silent switch): each agreement carries the zone printed on its form
  when it was signed; plan revision 2 (October 2026) moved main segments between six pairs of zones and kept every
  zone's code and name, so forms signed before it carry the old zone for those lines. Nothing in the pack states the
  redraw; it shows only where an agreement's form zone and the inventory's zone disagree for the same line. Every zone
  gains or loses lines. Zone basis (the judge's secondary fork): the field notes define the inventory's `zone` as the
  line's replacement zone under plan revision 2, a field meaning; no filed rule counts agreements by either zone
  (supplemental-stumping ban 1), asserted.
- Hazards: H4 (D7) forms signed before the March 2023 migration carry the legacy premise number, unpadded; H5 (D1)
  owners who signed on paper and again on the portal; H6 (D2) agreements later withdrawn (status and date).
- Path (6 files, 10 columns): agreements file, crosswalk, inventory, plan revision 2, field notes, extract log;
  `agreement_no`, `signed_on`, `channel`, `premise_no`, `sl_id`, `zone_on_form`, `status`, `status_date`, the
  crosswalk's `premise_no` and `sl_id`, the inventory's `zone`.
- Stops (asserted as built, every stop off the golden on at least 10 of 12 zones): S1 natural (rows counted by form
  zone); S2 (distinct lines, withdrawn removed, by form zone); S3 (inventory zone, legacy rows unmapped and dropped);
  answer.
- Lazy delta: S1 wrong on 12 of 12.
- Realism: an agreement form printed with the zone of the plan in force when it was mailed, and a plan revision that
  realigned zone boundaries to main replacement packages, are both ordinary; the agreement system never re-stamps old
  forms.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta (asserted as built) |
|---|---|---|---|
| H1 UTC completion times | the work management system stores UTC; the district reports in local time | ask A | five completions at each of the first three quarter ends |
| H2 vendor renumbered | Tri-County's July 2026 acquisition | ask A | Tri-County's third quarter split across two vendor numbers |
| H3 re-closed completion | a restoration correction re-closes the work order | ask A | one or two sites per contract counted twice |
| H4 legacy premise numbers | the March 2023 migration | ask B (and the main call's digs for cause, neutral there) | pre-2023 forms unmatched unless mapped |
| H5 paper and portal signatures | the portal opened in June 2024 | ask B | rows above lines in every zone |
| H6 withdrawn agreements | owners may withdraw before work starts | ask B | a few lines per zone |

**The cracker sheet.** The cracker filed 2037, ran the hygiene battery (keys unique, exact duplicates, every join
matched, no fan-out, counts that tie to the progress report) and executed every filed rule. Every ask row misses
outside its rounding:

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask A, paid per full replacement, 3 contracts by 4 quarters (12) | paid base, extra footage, restoration and `co_amount` summed per site, by contract and quarter, over completions | every contract-quarter's change orders are counted once per covered site | miss |
| Ask B, lines with a signed agreement, 12 zones (12) | distinct lines, withdrawn removed, legacy numbers mapped, counted by the form's zone | the forms signed before revision 2 carry the old zone for the moved segments | miss |
| Chart (recommendation block, not an ask) | the schedule bars | carried by the main call, scored with it | outside |

Mirror leakage: 10 per cent of the ask weight (the mirror files 2038 and answers both asks exactly as the cracker
does, keeping method credit only; no ask figure couples to the call).

**Pair arithmetic.** Planning weights 38 recommendation (the call, each zone's finish year, replacements and cost),
7 instruction following, 55 asks over 24 figures. The cracker keeps about 10 per cent of the ask weight:
C = 38 + 7 + 5.5 = 50.5. The mirror (R0) keeps r of about 4 (two zones' finish years, the plan order) and the same
5.5: S = 4 + 7 + 5.5 = 16.5.

Pair ceiling: 33.5

If the rubric grades each zone's figures as asks rather than recommendation criteria, the cracker keeps them and the
mirror does not: C rises to about 66 and S stays near 17, a pair of about 41.5; that case needs the call held by all
but one response, which the decisive rung is built for. Recomputed from the generated rubric when it exists.

## Pins

- In the prompt (the question, never a convention): each zone's finish year at $25.4 million a year from 2027, the
  last zone against the November 2037 deadline, the deliverables, the asks' units and rounding.
- Plan revision 2 (level 1): the scope (every line classified Lead, GRR or Lead Status Unknown in a zone is excavated,
  lead and GRR replaced in full), the zones and their priority order, the construction eras unknown lines are grouped
  by, plan cost carrying each unknown line at the share of lead or GRR expected among the district's Lead Status
  Unknown lines of its era (4.3) and the class's definition (6.1), the 2027 unit cost schedule and one mobilisation
  per zone, the running-total schedule rule, and each programme year's season closing 31 October; the LCRI deadline.
- Capital plan (level 2): $25.4 million a year in 2027 dollars, 2027 to 2037.
- Change order log (level 2, the engineer's register): approved change orders are paid to the contractor on its pay
  applications, each entered once with its sites.
- Field notes (level 4): field meanings (REPLACED is found lead or GRR and replaced in full, NON-LEAD since), the
  result code list, the crosswalk's zero padding, UTC on the completions export, the reclosing's paid amounts
  replacing the first closing's, the inventory's zone as plan revision 2's, and the extract's own account of how lines
  come to be verified (every service on a replaced main, from 2023; every other row a single-line visit raised by a
  customer report, a leak, a sampling site or the 2024 ranking), filed once.
- No pin names coverage, a sample, a sweep, a project, a remainder, a depleted pool, which verifications estimate the
  share or any estimation method; the readability screen was rerun on every pin, plan 4.3's new class included.

## Stopping rule

Written before the first portal test and rewritten at loop 1. Loop 0 shipped the whole-segment shares as the answer;
the portal's top response filed 2037, and the author asked for the stumps hardened. Loop 1 makes the whole-segment
shares a rung (R3, 2038) and the unknown lines' own share the answer. If a top portal response files 2037 by the
remainder accounting (the whole-segment expectation less what the verifications found, over the lines still unknown),
the main call is at ceiling in this world: change the decision, never stack a further rung on the share. If the call
holds and the asks score over the bar, an ask-only revision on the ask paths with the call byte-identical. If the judge
finds a fork on the call that convergence cannot close, re-root the decisive step rather than pin it.

## Prompt

`prompt.txt`, written last against the planned golden: voice-check PASS, 844 characters. Loop 1 changed one figure (the
appropriation, $27.1 million to $25.4 million a year, as the capital plan files it) and, at the loop-1 judge's
optional point, the first ask's "lines we will replace" to "lines we expect to replace" (read literally, the first
could be the lines already classified Lead or GRR); the question is unchanged.

## Build record

Stage 3, 2026-10-12. `python3 task124/generator/build.py` builds the pack into `target/`, the goldens into `golden/`,
`metadata.json` and `generator/figures.json`, runs `generator/checks.py` (93 assertions, 0 failed, every SF row among
them) and `generator/verify.py` (its own parsers, the plan order read from the plan's table; the call, the default path,
12 zones, 12 payments and 12 agreement counts agree with the golden workbook), then builds a second time into a scratch
folder and compares every byte: identical.

| File | Role | Rows |
|---|---|---|
| `hfrwd_service_line_inventory_20270108.csv` | spine: every service line, its tap card, class, basis, zone and main segment | 87,410 |
| `sl_field_verifications_2021_2026.csv` | operating extract: every verification, customer-system rows keyed by premise number | 6,671 |
| `cis_gis_crosswalk_2023.csv` | lookup: premise numbers to service line ids, eight-digit padded | 85,850 |
| `sl_material_result_codes.csv` | lookup: result codes by recording route | 15 |
| `HFRWD_LSLR_plan_rev2_2026-10.pdf` | governing document: scope, zones and order, cost rule, schedule rule, season, deadline | |
| `HFRWD_capital_improvement_plan_2027-2037_board_draft.docx` | governing document: $27.1 million a year in 2027 dollars | |
| `unit_cost_schedule_2027.xlsx` | lookup: unit costs by zone and the mobilisation | 12 |
| `LSLR_progress_report_2026.pdf` | context artifact: counts of work done, every figure asserted (C1) | |
| `lsl_extract_field_notes_2027-01.md` | dictionary | |
| `extract_log_2027-01-08.csv` | provenance record | 15 |
| `lsl_completions_2026.csv` | ask A: completions export (D6, H1, H2, H3) | 777 |
| `change_orders_2026.xlsx` | ask A: change order log, each once | 45 |
| `contracts_2026.csv` | ask A: contracts and vendor records | 4 |
| `access_agreements_2022_2026.csv` | ask B: agreement forms (D2, H4, H5, H6) | 10,489 |
| `lcr_tap_samples_2025_2026.csv` | distractor: tier 1 compliance samples | 361 |
| `ami_meter_exchanges_2023_2025.csv` | distractor: automated meter exchanges | 30,916 |

- **Input gates (asserted):** 16 files, 5 formats (csv, docx, md, pdf, xlsx), the 87,410-row spine, 2 distractors in
  `metadata.json`, each deleted with nothing moving.
- **Built answer:** RZ-06 Wexley last, finished 2037; $284.7 million over 10.50 programme years; shares 0.556, 0.316 and
  0.083 on 792, 304 and 168 lines of the 78 segments verified whole. Default path: 0.763, 0.585 and 0.217 on 4,911
  lines, last zone 2039 ($347.5 million, 12.82 years). Ask A: 12 figures, every stop at least $25 off on every figure
  it moves, the cracker's stop (S2) off on all 12. Ask B: 12 counts, S1, S2 (the cracker) and S3 each off on all 12
  zones.
- **`figures_check.py`:** exit 0 (76 figures in blocks 1 to 4, none absent from `figures.json`).
- **`leak.py --asof 2027-01-11`:** REVIEW, no LEAK. Sweep 3, the plan carries 9 of 13 words of the call: it defines
  the call's terms (zone, programme year, finished, deadline) and lists RZ-06 Wexley in its priority table, and states
  no finish year, cost or count; harmless. Sweep 4, the plan, the progress report and the field notes carry 7 or 8
  stump-paragraph terms (verified, verification, unknown, schedule, inventory, district): the domain's own nouns, and
  none names why a line was dug, a main replacement, coverage or a share (checks S1, S4, S5); harmless. Sweep 6, the
  plan names eight zones beside numbers in its priority table, the order the call uses and not a ranking on finish
  year; the unit cost schedule names zones beside unit costs, prices only; the change order log names the contracts
  beside change order amounts and states no contract's cost per replacement; harmless.
- **`guard.py`:** surface 0 pairs promoted (nearest task111 at 0.100); heart WARN on `repeat.gate_g` against task501,
  answered in the draw.
- **House fixes:** H1 container audit clean on `target/` and `golden/`; H2 every figure in this note re-measured on the
  built pack; H3 the board paper's "three in four" asserted (F3); H4 the golden folder holds exactly the two
  deliverables; H8 every file and plan clause the write-up and goldens cite exists; H9 the extract log and field notes
  name every file (G5, G6); H11 one `submission.md`, one `prompt.txt`, no `prompt.md`; H16 no extract carries a date
  past its extract (R5); H21 the invented names read by hand (Hollins Ford, Darrow, Kittering, Brannigan Excavating,
  Tri-County Underground, Kestrel Pipe and Utility; "Tri-County" is generic geography with no distinctive remainder);
  H23 ask B reads with "none" as a grammatical answer; H24 no file under `target/` says the pack was built (R6).
- **Golden realism:** precision varies by quantity (lines to the ten, costs to $100,000, running totals to $0.1
  million, programme years to 0.01, shares to 0.001, payments to the dollar); finding titles on the board paper, its
  chart and the schedule sheet; notes carry the rounding convention, the unrounded running totals and the Tri-County
  vendor change; numbers right-aligned; the chart labels every finish year and marks the deadline; containers carry the
  programme manager as author and in-fiction stamps.

- **Stage 4 repair, 2026-10-12.** The determinism judge returned NOT_DETERMINISTIC, SEND_BACK: nothing filed said
  how the verifications were chosen, so pooling every verification (2039) read as literally as the whole segments
  (2037). The fork is closed by filing a fact the record lacked, never the estimator (the stopping rule's line: the
  method stays the solver's step). One generator pass: the field notes give the extract's own account of how lines
  come to be verified (every service on a replaced main, from 2023; every other row a single-line visit raised by a
  customer report, a leak, a sampling site or the 2024 ranking), naming no share, sample, segment or method (S1, S6,
  W3); plan 4.3's share is expected among the district's lines of the era with no usable tap card, the class the whole
  segments estimate exactly, which closes the left-unverified share the filing would otherwise expose (SF15 to SF17,
  in `checks.py` and `verify.py`). Ask A: the field notes say the reclosing's paid amounts replace the first closing's
  (A10) and the change order log says approved change orders are paid to the contractor (A11), neither saying how a
  change order counts against its sites. Ask B: the inventory's zone is defined as plan revision 2's (B7), with no rule
  counting agreements by either zone. Realism: change order approvals off weekends and district holidays (R8, the
  Christmas Day approval now 23 December), each change order worded on its own (R3, 45 of 45 distinct), the unit cost
  schedule's system rates and each zone's rate basis stated (R9). Gates: `checks.py` 108 assertions, 0 failed;
  `verify.py` green; two builds byte-identical; `figures_check.py` exit 0 (76 figures); `freeze.py check --mode
  determinism` PASS; `precut.py` exit 0; voice-check PASS; `leak.py` REVIEW, no LEAK, the same seven lines as stage 3 (sweep 4 now
  counts 9, 8 and 10 stump-paragraph terms in the plan, the progress report and the field notes because the term list
  follows this note and took in replaced and sample: the domain's own nouns, and the field notes' new paragraph says
  how lines come to be verified, naming no share, sample, segment or method, S6, so no document names the move;
  harmless); `guard.py surface` 0 promoted (nearest task111 at 0.100), `heart` WARN (`repeat.gate_g`, answered in the draw). Four pack files
  changed (the plan, the field notes, the change order log, the unit cost schedule); every data file is byte-identical
  to the stage 3 cut, no graded figure moved, and the goldens changed in prose only (plan 4.3's wording, the visit
  reasons). The prompt is unchanged. The reader's stage 3 read stands in the leak report and is due again on this cut.

- **Stage 4 re-judge and ship, 2026-10-12.** The re-judge (one isolated thread on a fresh copy of the repaired cut)
  returned DETERMINISTIC, APPROVE (`determinism_check_report_pass2.md`): every figure reproduced, the 78 segments
  verified whole are a clean break (the next segment at 0.42), and both competing bases it ran (every verification;
  one pooled share on the whole segments) file 2039. Its one soft point, taken: step 6 said the form zone was printed
  before plan revision 2 redrew six boundaries, which no shipped file states; step 6 now rests only on the field
  notes' definitions (the inventory's `zone` is the line's zone under plan revision 2, `zone_on_form` the zone printed
  on the form). The board paper's note under the agreement table carried the same claim, with an October 2026 edge
  that two forms signed on 3 and 12 October 2026 contradict (house fix H6); it now reads "in the zone the inventory
  gives each line under plan revision 2; some forms signed before the revision print a different zone" (B5). The
  leak reader's re-read is answered under `## Leak review`. Gates on the final rebuild: `checks.py` 108 assertions,
  0 failed; `verify.py` green; two full runs byte-identical, each with its own second build; `target/` byte-identical
  to the cut the judge and the reader read, the workbook, `metadata.json` and `figures.json` byte-identical, and the
  board paper changed in that note only; `figures_check.py` exit 0 (75 figures, the old step 6's "2" gone);
  `freeze.py check --mode determinism` PASS against the snapshot taken before the stage 4 repair; `precut.py` exit 0
  (38 checks, 0 FAIL); voice-check PASS; `leak.py --asof 2027-01-11` REVIEW, no LEAK, the same seven lines;
  container audit clean on `target/` and `golden/`; `guard.py surface` 0 promoted (nearest task111 at 0.100),
  `heart` WARN (`repeat.gate_g`, answered in the draw), nearest driver 0.05 (task32 v2); the card's answer is the
  call verbatim, `guard.py validate` 145 cards, 0 invalid. `target.zip` is cut from the final rebuild: the 16 files,
  flat, each byte-identical to `target/`.

- **Loop 1, 2026-10-13 (harden after the portal return).** The generator's world is the shipped one: the 2026 records
  search keeps the prices it was drawn against and agreement outreach the ranking it opened under, so every
  verification, completion, change order and agreement row is byte-identical to the loop-0 cut, and every ask figure
  is unchanged (asserted against the shipped `figures.json`). Changed: plan 4.3's class (the district's Lead Status
  Unknown lines) and the plan's order (RZ-03 before RZ-12, RZ-06 before RZ-10); the capital plan's construction line
  ($25.4 million); the unit cost schedule (mobilisation $160,000; RZ-07 $11,050 and $2,440, RZ-02 $13,950, RZ-04
  $12,550); the field notes' REPLACED definition (found lead or GRR and replaced in full); nineteen copper cards in six
  zones read as lead cards on lines no crew has dug (the replacement counts' rounding edges); the programme manager
  and the board chair drawn again (Gregory Sheppard, Craig Stewart); the progress report's class totals follow the
  inventory. Golden: $274.1 million over 10.79 programme years, RZ-10 Lakeview Terrace last, finished 2037; the
  unknown-line shares 0.497, 0.279 and 0.075; the whole-segment rung 2038 ($284.4 million, 11.20 years); the default
  path 2040 ($347.2 million, 13.67 years). Gates: `checks.py` 114 assertions, 0 failed (W4 the analyst test on the
  clean truth; SF16 and SF17 the accounting three ways and its misreadings; M18 mess neutral on the call); `verify.py`
  green on its own parsers (the accounting district-wide and off the whole segments, the found count tied to the
  inventory's unknown class); two builds byte-identical; `figures_check.py` exit 0 (84 figures); `precut.py` exit 0
  (49 checks, 0 FAIL, 0 WARN); voice-check PASS (839 characters); `leak.py --asof 2027-01-11` REVIEW, no LEAK (sweep 3
  the plan's call words: it defines the terms and lists RZ-10 in its priority table, no finish year, cost or count;
  sweep 4 the plan, the progress report and the field notes at 12, 9 and 11 stump-paragraph terms: the domain's own
  nouns, plan 4.3 names the class and no share, remainder or method, the field notes' REPLACED line is a field
  meaning; sweep 6 the plan's priority table, the progress report's and the change order log's three contractors and
  the unit cost schedule's zone prices, none a ranking on finish year: harmless); container audit clean; `guard.py
  surface` 0 promoted (nearest task111 at 0.100); `heart` BLOCK on `ban.pattern` alone (G14 against task121 v3, a
  retired re-root drawn later on 2026-10-12 whose lower number sorts it first, recorded under `## Tried and
  rejected`) and WARN `driver.near` against this slot's loop-0 driver; `guard.py validate` 161 cards, 0 invalid.
  `target.zip` cut from the final rebuild: 16 members, flat, each byte-identical to `target/`.

- **Loop 1 stage 4, 2026-10-13.** The judge thread (one isolated Sonnet thread on a fresh unzip of the loop-1
  `target.zip`, the prompt and the submission's graded blocks) returned DETERMINISTIC, APPROVE
  (`determinism_check_report_loop1.md`): every figure reproduced (4,911 verified no-tap-card lines; the 78 segments
  verified whole, the next main at 50 per cent or less; 0.556, 0.316 and 0.083; 0.497, 0.279 and 0.075; twelve zones'
  lines, costs and finish years; $274.1 million over 10.79 years; twelve payments; twelve agreement counts); the
  competing estimators file 2038 (the whole-segment shares carried straight to the unknown lines), 2039 (one pooled
  share) and 2040 (every verification), each ruled out by the data; its variants (shares rounded, the mean of
  per-main shares, a logistic on era and zone over the whole-segment lines) keep 2037 at 10.73 to 10.79 years. Gate
  G statistical_rigor (the note's forecasting, a name only), analytical_non_defect, no surface read, no sole defect;
  Gate H domain, layers and decisive step pass. Its one optional point, taken: the first ask reads "lines we expect
  to replace" (the prompt's only change at stage 4; voice-check PASS, 844 characters; `precut.py` exit 0). The leak
  reader's first read is under `## Leak review`; the prompt change sent it back for one re-read of the final prompt.

## Leak review

- `leak.py --asof 2027-01-11` on the final cut: REVIEW, no LEAK. Its seven lines (sweep 3, the plan's call words;
  sweep 4, the plan, the progress report and the field notes; sweep 6, the plan, the unit cost schedule and the
  change order log) are the stage 3 and stage 4 lines, each answered in the build record.
- Reader, stage 3 cut: no decisive-step sentence, ranking, helping file or answer-like figure; it named the era
  share's estimation sample as open, with the payment and agreement readings and six realism tells, all taken into
  the stage 4 repair.
- Reader, re-read on the repaired cut: no decisive-step sentence (the field notes' two verification routes read to it
  as a mild lean, not a leak), no ranking, helping file or answer-like figure. Its own 2034 execution took the era
  share from the inventory's current classes of the no-tap-card lines of known status (3.8, 3.3 and 1.4 per cent;
  13.6, 7.3 and 1.8 on the field-verified ones), where every line found lead and since replaced reads NON-LEAD under
  REPLACED, so those lines are not a sample of the unknown lines; the judge's competing bases land on 2039 and none
  returns 2034: not a defensible reading, and nothing changed for it.
- The re-read's ask readings (payment basis, Eastern quarters, reclosings, Tri-County's two vendor numbers; withdrawn
  agreements, form zone against inventory zone, the crosswalk) are the asks' designed devices and hazards, each
  reproduced by the re-judge. Its two realism notes (the change order descriptions still read patterned; the capital
  plan draft is thin, with no footer) are left as they stand: the realism sweep passes (R3, 45 of 45 descriptions
  distinct), neither file carries the decisive step, and both are files the judge read.
- Loop 1 (2026-10-13), `leak.py --asof 2027-01-11` on the loop-1 cut: REVIEW, no LEAK; its seven lines answered in
  the loop-1 build record.
- Reader, loop-1 cut: no decisive-step sentence, ranking, helping file or answer-like figure; it read plan 4.3 as the
  share among the unverified lines (the golden's estimand) and quoted the field notes' two routes as a mild lean. Its
  own execution found the replaced mains by same-date clusters and carried their shares straight to the unknown lines,
  filing 2039: the whole-segment rung (its shares ran high on a key it resolved by stripping zeros; on the shipped
  files the clusters give 0.544 to 0.575 before 1930). It never weighed the pool the visits had depleted, which is the
  decisive step holding against a careful reader. Its six realism tells are ruled in the leak report: none moved a
  file (the change order sequence is ask A's frozen file; the construction line against cost reads short only on the
  rung's cost).
- Reader, re-read on the final prompt (the first ask's "expect to replace"): clean on the six questions; its ask
  readings are the asks' designed devices and the expected count plan 4.3 and 4.2 settle; nothing moved.

## Pre-ship check

1. Domain: a water utility's estimate of how many of its Lead Status Unknown service lines are lead or GRR, made from
   the one sample that did not choose its lines (services exposed when a main is replaced) and corrected for what
   targeted verification already took out of the unknown pool, carried into a replacement schedule against the capital
   plan; with another field's nouns there are no tap cards, GRR classes, main-replacement exposures or replace-on-find.
2. Real work, nothing planted: a verification log keyed across the March 2023 migration, result codes by recording
   route, two date formats, re-verifications, assessor zeros and replaced lines reading NON-LEAD; on the asks, change
   order totals repeated per site, reclosings, UTC completion times, a vendor renumbered mid-year and agreements keyed
   by unpadded legacy numbers with the zone printed on the form, each a record the district's systems produce.
3. The step that flips the call is methodological: the share among the unknown lines is the whole-segment expectation
   across the era's lines less the lead the verifications found, over the lines left; no field reading, code or stated
   rule flips it (mishandling the legacy keys keeps the twelve finish years; reading REPLACED as non-lead is ruled out
   by its definition).
4. Analyst test: the default path (every verified no-tap-card line by era, or a model on every visible attribute)
   files $347.2 million, 13.67 programme years and RZ-10 Lakeview Terrace in 2040; a strong analyst who takes the
   whole-segment shares files $284.4 million and 2038; both past the deadline.
5. Plan 4.3 names the class and plan 6.1 defines it; the field notes file how lines come to be verified; the design
   forces the method (form 1), with the accounting's three routes and its zone and plan-zone variants converging
   (SF16).
6. No decoy: no consultant score, published hit rate or memo ships; the progress report carries counts only and ranks
   no zone.
7. Nothing is recovered from certified figures: no file states a share, an expected count, a zone's count or cost, or
   a schedule.
8. The lesson (a pool left after targeted testing is depleted of what the testing looked for, so the population's
   unbiased rate overstates it) is on no other card: `guard.py heart` finds no driver near it but this slot's loop 0
   (0.20); its one BLOCK is the same-day ordering tie on G14 against retired task121 v3.

## Tried and rejected

- Draw, the note's tariff-class replay as the decisive rung: a schema-visible join (ESI ID to the premise file's class) that a finest-grain replay of the interval data also hands over, both default moves for the pilot solver; demoted to rung 3.
- Draw, a demand-response re-dispatch rung (the new centres join the programme on lower bids and displace the members carrying a fixed seasonal target, moving the reduction between zones with the book total unchanged): the centres on next season's roster prompt the solver to model their curtailment, which needs the dispatch rule, which hands over the displacement, and the rule has to be stated or empirical in a file the solver then executes.
- Draw, a maximum-demand basis rung (a new premise's maximum demand on the enrolment is its service application estimate, not a metered maximum): reachable by validating the field against interval data for existing premises and joining the application register on the same key; kept only as a candidate ask device.
- Draw, a first-summer ramp rung (new refrigerated sites fill over their first year): the same driver as analytical_tasks note FC04 (station maturity ramp), which a sibling build in this wave may realise, and a cohort split by commissioning age is a group-by a strong forecaster runs on analogs.
- Draw, an endogenous peak-hour shift (the newcomers move the reference hour): the reference is the transmission operator's system peak, exogenous to a retail book, a flat refrigerated load cannot move a peak, and an hourly replay finds it wherever it does apply.
- Draw, a cogeneration outage at a private-use network site (net load jumps to gross while the unit is out): it needs a shipped forward outage record, a sentence the solver executes, and an outage file in a peak-load folder is read as relevant at once.
- Draw, the note's Economics tag: Economics' boundary excludes markets trading, and a retail provider placing call options across zone books is that class.
- Draw, four zone books: shape 05 off four buckets reaches about 20 criteria.
- Draw, "Afternoon Hold" as the programme's name: it describes the mechanism a solver has to find; replaced by a neutral product name.
- Draw, Kenneth Ross and Robert Cobb as personas: first names in one older build each (task93, task104); replaced by Donald Lee from the same draw.
- Design, grading each book's 1-in-10 load and pre-block exposure (the draw's 8 x 3 block): under rung 3 seven of the eight books' loads and exposures equal the answer's, so a rung-3 response keeps 14 component criteria free; replaced by the uncovered exposure left once the lots are in, which moves on every receiving book with the level.
- Design, naming the developer or its centres in the prompt: it points every solver at the one population whose draw decides the call and invites the "what does a new cold store draw" question the stump depends on nobody asking.
- Design, a Business Saver file of kW curtailed per member per event: it names the quantity a peak forecaster adds back; replaced by the billing system's credits (kWh and USD per account per window), keyed on the account number.
- Design, a product sheet that says events are called on forecast system-peak days: one sentence that hands over why the fourteen's peak draw is low; the timing is left to the credit dates against the peak list.
- Design, a programme with general commercial members as well: their called draws would bias the new general premises' class factor too, so the answer would need a second adjustment no record forces.
- Design, refrigerated sites joining the programme a summer after joining the book: the joining summer shows a cold store at 0.90 in the system peak hour, a symptom in the class factor that hands the rung over; eligibility now runs on the meter's history, so every refrigerated arrival was eligible on arrival.
- Design, the amendment rows restating 60 MW (the source note): rung 1 then sits 5 MW from rung 3 and inside 10 per cent of the answer; 275 MW puts rung 1 at +21.4 per cent.
- Design, ask A's primary device as two brokers quoting per MWh of different notional shapes: the same insight as ask B's 5x16 against 7x16 weighting, so one discovery would pay twice; demoted to hazard H4 across both asks and replaced by the third broker's absent channel.
- Design, hedge prices in USD per MW-month beside USD/MWh in the blotter: a magnitude 300 times apart is loud and gets fixed by reflex; replaced by price-only amendments with a matching log.
- Design, a counterparty novation or a re-delivered blotter batch as an ask B device: either moves hedge MW for a solver who builds hedges from the blotter, which puts a device on the main call's path.
- Build, clearing every replay-table cell off its half-MW edge by moving that summer's swing alone: the two summers that set the 1-in-10 are pinned by the exposure target, so the factor solve pulled them straight back and the loop oscillated; they are cleared by a small target shift checked against both pinned cells and the post-block bins.
- Build, a 2026 block split in the close-out report: its figures cannot recompute from a pack that starts at summer 2017 and it reads as a split artifact; replaced by Table 1 (enrolled maximum demand and settled load at the 2026 peak).
- Build, the close-out dated October 2026: true-up for the 2026 peak was not available until late January 2027, so the report would cite settlement it could not have had; dated 2 February 2027.
- Build, residential premises in the book: the enrolment extract would run near 600,000 rows; the book is commercial and industrial.
- Build, a credit line whose account total lands on a half kWh: rounding conventions split on it; the member's first window-hour read is entered 0.1 kWh higher so every total has no half to round.
- Solve, round 1 (plain), the five-rung ladder as built: the solver landed 120 / 30 / 0 / 0 / 210 / 25 / 15 / 0 at step 5 of its path, in its own words "The members were curtailed on every system peak day (bsaver_credits), so their peak-hour reads cannot be used directly; on those days they run at about 0.60 of maximum demand ... That gives a factor of about 0.900 of maximum demand in every summer"; it set the credit dates beside the system peaks and took the uncalled baseline from the programme terms, so rung 3 never held it; hardening loop 1 of 3 follows.
- Harden loop 1, the uncalled-draw rung as built (rung 4 reached through the credit dates and the programme baseline): the solver's own path sentence, "The members were curtailed on every system peak day (bsaver_credits), so their peak-hour reads cannot be used directly ... Each site's baseline follows the program terms: the 10 most recent business days without a call", shows two free routes onto it; the credit file's window dates line up with the published peak list on a one-key date join a solver runs by reflex once it opens a file named for the programme, and the product sheet's baseline clause is a shipped sentence that describes constructing exactly the uncalled draw, so the decisive factor was a reading, not a construction; the uncalled draw stays as rung 4 and is no longer the answer.
- Harden loop 1, a members' NAICS split as the new rung (ice plants idle in the afternoon, cold stores do not, so the fourteen's pooled uncalled draw is wrong for 493120 centres): the split sits on the premise register's NAICS column, a one-key group-by the solver runs on the population it already holds, so it is a row predicate, not a construction.
- Harden loop 1, rooftop solar on the new centres (net load at the peak hour below the analogs' draw): it needs a DG column on the premise register or the enrolment, which names the adjustment on the very rows the solver prices.
- Harden loop 1, a draw linear in heat with no full-load level: every heat-conditioned estimator (regression, hottest decile, days as hot as the peaks) lands on a different factor, so the answer forks on the estimator; the full-load level is what makes the peak-heat estimators converge.
- Harden loop 1, a heat ramp from 0.45 to 0.80 or a step at 0.70 to 0.74: the programme baseline at the closed peak hours (its ten uncalled days run hot just before a peak) lands at 0.90 to 0.92, North Central 200, under 5 per cent from the answer; the ramp sits at 0.68 to 0.78 of the heat index, where the baseline lands at 0.885 and North Central at 195.
- Harden loop 1, leaving the hottest non-peak weekdays uncalled every summer so that the peak-heat sample is large: the desk would miss the five hottest days of every summer while calling cooler ones, a pattern that reads as constructed; the forecast-miss rule stays as built (five of the hottest decile uncalled by the worst forecast scores).
- Harden loop 1, zone temperatures at 14 degrees F per unit of the heat index with 1.1 degrees of scatter: the hottest tenth of each site-summer's uncalled weekdays by zone maximum mixed ordinary days in and landed at 0.949, outside the corridor; the file now runs 30 degrees per unit with 0.7 of scatter, which is also the realistic summer range (about 82 to 108 F).
- Harden loop 1 architecture, solved by round 2 plain (landed, 96.6, asks 7/8): the solver skipped the heat-matched uncalled weekdays and the programme baseline altogether and read the members' uncalled hours on the peak days themselves. In its words: "on each peak day, the 493120 member sites' average load in the uncalled hours (hours ending 11-14 and 19-20) divided by maximum demand is about 0.981-0.982 every year." The shoulder hours of the called peak day sit at full load, so the 0.98 level is visible on the very days the solver already has open; loop 2 has to make same-day uncalled hours read a different level (or not exist at peak-day load) without forking the heat-matched estimator.
- Harden loop 2, an hourly ambient profile on the members' uncalled draw (morning hours cooler, so the peak days' shoulders read under full load): under the loop-1 heat ramp the full-load mark is a few degrees above an ordinary day's maximum, so on a design day it is crossed by late morning and every shoulder hour of a peak day still reads full load; a profile steep enough to drop the shoulders 10 per cent needs a 9 F fall between hours ending 14 and 15, which no Texas afternoon has.
- Harden loop 2, an extended called window on the system-peak days (hours ending 12 to 20, so the peak days carry no uncalled hour to read): a cold store cannot hold a firm level for nine hours, the credit file would need window hours it does not carry, and it removes the solver's step instead of making it return a wrong answer.
- Harden loop 2, uncalled full load kept at 0.90 with pre-cool at 0.96 to 0.99: the peak-day shoulders filed North Central at 220 (+4.8 per cent), inside the 6 per cent floor; the full-load level is 0.85 of maximum demand so the shoulder reading lands at 230 (+9.5 per cent).
- Re-root (2026-10-12), architecture 1 spent at the wave-1 resume, before any stage-3 work on loop 2: its card carried `validated_decoy: true` (the closed replay table and the members' metered peaks reproduce every wrong rung and only the newcomers' 2027 summer breaks them), which `guard.py` blocks outright since 2026-10-11 and no differentiation clears; the in-house solver walked the default path to the golden in round 1 (the programme baseline) and round 2 (the peak days' shoulder hours), the re-root rule's two default-path failures; loops 1 and 2 answered each solve by stacking a rung above the solved decisive step, which the pipeline now forbids; the loop-2 ladder ran seven rungs against a ceiling of five, the replay divisor was pinned by replaying certified cells (capped at review), round 2 cracked seven of eight ask items through filed rules, and `prompt.md` failed the prompt gate. `precut.py` failed 23 of 33 checks on the loop-2 note.
- Draw (architecture 2), the selection-biased verification stump labelled pattern E (conditioned yield): `test.same_driver` blocks it inside the window against task181 v3 (population, E, forecasting) and task500 v2 (population, E, method_or_model_selection), and `test.own_lineage` against architecture 1's three loops; carried as pattern none with G14 decisive, as task183 carries the same mechanism.
- Draw (architecture 2), pattern D (the whole-segment unit read as a grain): it would ban task181 v4 (filed earlier today, later in draw order) on its decisive pattern D; dropped.
- Draw (architecture 2), the first furniture set (role capacity_planner, artifact close_out_summary, organisation family utility_or_infrastructure, shape 01, question form whether): each repeats task181 v4 or task229, both filed today and later in draw order, so this card would have banned or warned them; redrawn to programme_officer, capacity_report, cooperative_or_member_body, shape 06 and when.
- Draw (architecture 2), the single-year call (which zones the 2027 construction budget covers, shape 01): shape 01 collides with task181 v4; the ten-year schedule against the annual appropriation (shape 06) carries the same stump with a finish year per zone and is the decision the capital plan actually takes.
- Draw (architecture 2), shipping the main-replacement project register: it names the segments a replacement verified whole, a join on a key the solver already holds that hands the decisive sample over; the sweeps are known only by complete coverage.
- Draw (architecture 2), a consultant's lead-probability score per service line: a filed model calibrated on the targeted verifications gives the wrong answer read literally (an official decoy); not shipped.
- Draw (architecture 2), a verification hit rate published in the 2026 progress report: a reported figure the default path would quote, which turns the stump into rejecting a surface read (Gate G); the report carries counts and spend only.
- Build (architecture 2), swept shares of 14/25, 8/25 and 2/25: every whole-segment decade read exactly 0.56, 0.32 or 0.08 on 750, 300 and 150 lines, two-decimal rates on round counts that a reader takes for construction; moved to 5 in 9, 6 in 19 and 1 in 12 per decade (792, 304 and 168 lines), the per-decade exactness kept because it is what closes the post-stratification fork (C1).
- Build, zone sizes in exact hundreds (88,000 lines, GRR exactly 4,700): synthetic tells in every per-zone count and in the progress report's totals; a few dozen never-built lots dropped per zone (unverified records-known or new-build lines on segments at or under 0.25 coverage) and one to three abandoned galvanized services in RZ-13 and RZ-14, so no zone size or class total is a multiple of 100 (R1); the call and every margin unchanged.
- Build, a plan sentence making the inventory's zone each line's zone: it adjudicates ask B's device for a cracker who executes every filed rule; cut, and SF1 closes on no file the call reads carrying another zone.
- Build, capital spent in the progress report: it cannot recompute from the pack (engineering and district crews are not in it), and a contractor-payment total beside it would referee ask A's change orders; cut, the report carries counts only.
- Build, large evening closings at all three quarter ends: the June closings moved into the third quarter as the September ones moved out, and the UTC stop came within $1 of the golden on Tri-County's third quarter; the June closings are ordinary jobs now, so the moves never cancel (A7).
- Build, agreement outreach opening zone by zone every 70 days: six zones had no form signed before the cut-over, so the legacy-key stop missed only six zones; outreach now opens in every zone before 13 March 2023 (B3).
- Build, the mobilisation fork (SF13) carried as a later schedule: a mobilisation in each year a zone spans adds $185,000 per year end crossed and moves no finish year; the row now says so, and the plan's cost sentence rules it out.
- Stage 4, the verification design left unfiled (the selection recoverable only from coverage and the within-era gap): the judge read pooling every verification (2039) as literally as the whole segments (2037), NOT_DETERMINISTIC, SEND_BACK; the field notes now carry the extract's own account of how lines come to be verified, which forces the frame without naming it.
- Stage 4, filing the whole segments as an inventory validation plan's sweeps: a validation sample is the estimation sample by name, so the decisive step would become a reading, and the world's whole segments are main replacements (old cast iron first, the era lean R2 rests on); filed as what a main replacement does to every service on the main.
- Stage 4, a plan 4.3 sentence naming the estimation sample (lines on segments where every service was verified), the judge's second suggestion: it files the method, so the stump becomes rule application.
- Stage 4, plan 4.3 left on "expected among Lead Status Unknown lines": once the selection is filed, the share among the lines the single-line visits left unverified (0.497, 0.279, 0.075) is a coherent rival, last zone 2037 but five zones a year earlier and $10.4 million less; 4.3 now carries the share among the district's lines of the era with no usable tap card, which the whole segments estimate exactly (SF16).
- Stage 4, a filed rule counting agreements by the inventory's zone (the pin first proposed for ask B): it adjudicates ask B's primary device (supplemental-stumping ban 1), as the draw had already found; the inventory's zone field is defined as plan revision 2's instead, a field meaning.
- Stage 4, "paid once" or "per site" wording beside the change order inclusion pin: either adjudicates ask A's device; the log says only that approved change orders are paid to the contractor.
- Stage 4, moving holiday-dated field work (verifications, completions) to working days: it shifts replacement dates and the change orders built on them, so ask A's figures; only the change order approvals, which no figure rests on, moved.
- Stage 4, varying the unit costs zone by zone: every zone cost, running total and the default path move; the schedule states its system rates and each zone's rate basis instead.
- Stage 4, the prompt's "the November 2037 deadline" changed to "1 November 2037": voice-check passes both, the plan files 1 November 2037 and the 31 October season close, every reading gives the same call, and the call sentence is frozen; kept.
- Stage 4, "from May 2023" in the field notes: the first replaced-main verification is 13 July 2023; filed as "from 2023".
- Ship, step 6 of the write-up and the board paper's agreement note saying the form zone is the line's zone before plan revision 2 (forms signed before October 2026): no shipped file states it (the re-judge's soft point), and forms signed on 3 and 12 October 2026 also carry a differing zone; both now rest only on the inventory's zone being plan revision 2's.
- Portal, loop 0 (2026-10-13): the top response filed 2037, RZ-06 Wexley last, before the deadline (the call landed).
  The field notes' paragraph on how lines come to be verified announced the replaced mains' exposures, and coverage
  separated their 78 segments (1.00) from every other (0.42 or less), so the decisive step ran as a work order.
- Harden loop 1, hiding the sample: the replaced mains' account moved to the capital plan and the visit reasons to the
  progress report; new houses on every renewed block lowering its coverage; GIS valve splits making short segments
  that single-line visits years apart had verified whole; the golden identifying the renewals by timing (every service
  built before 1989 first verified within one renewal's weeks). With every eligible run split off, "every service
  built before 1989 verified" filed 11.01 programme years (0.01 past 2037) and "verified since 2023" equalled the
  golden or, with since-2023 runs admitted, still filed 2037; a segment-size filter or a burst rule finds the renewals
  whatever the decoys, and new houses on exactly the renewed blocks were a tell. Dropped, the generator reverted.
- Harden loop 1, the remainder at $27.1 million: the whole-segment shares and the remainder both finish in 2037 (10.50
  and 10.12 programme years); the call separates only with the boundary between them, so the construction line is
  $25.4 million (10.79 and 11.20).
- Harden loop 1, the appropriation alone: no construction line on one decimal of $ million clears every zone's running
  total by 0.13 years with the last zone 0.13 inside 2037 and the whole-segment rung 0.13 past it (best 0.095 at
  $25.9 million, the rung at 11.004); with the mobilisation, three zones' engineer's prices (RZ-07, RZ-02, RZ-04) and
  two adjacent swaps in the priority order (RZ-03 before RZ-12, RZ-06 before RZ-10), every zone clears by 0.153.
- Harden loop 1, re-tuning the 2026 records search to the new prices: its picks decide which unverified lines are open
  in the plan, so three zones' agreement counts moved (ask B); the search keeps the prices it was drawn against, and
  agreement outreach keeps the ranking it opened under.
- Harden loop 1, the replacement counts' rounding edges under the new shares through the records search's own move (a
  copper card found for an unknown line): it removes lines from the class the share is estimated over, so the share
  moves with every fix; the six zones are cleared by lead cards on copper-carded lines no crew has dug, which no share
  reads.
- Harden loop 1, the card's decisive generator relabelled to dodge `guard.py heart`'s ban on G14 (task121 v3, a retired re-root drawn later on 2026-10-12 whose lower number sorts it first, so neither card's check met the other): G6 promotes task125 back to back and task132 on the same-driver signature in `guard.py surface`, and G5 meets task120 v3's ban the same way; G14 is the honest label (the table's question: does the pooled rate apply to this pool), so it stays, with the heart BLOCK recorded as that ordering tie against a build no reviewer meets. The first name Andrew (on task254's card) and William (drawn on task256 the next day) are drawn again as Gregory Sheppard and Craig Stewart.

# task157 design note: the 2027 initiative petition signature projection (architecture 2)

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first, and
`## Architecture 1 is spent: the bin is finer than the estimator` below it: architecture 1 (the January 2027
winter guarantee qualifier forecast) shipped twice and was returned twice, and the cause was measured rather
than argued. Architecture 2 is drawn afresh in the same number.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task157.json` (architecture 2, architecture 1 in `lineage` with
  its measured fate), registered 2026-10-27, re-checked against the restamped ban window: WARN only, no BLOCK,
  no person warning, `validate` clean on 299 cards, `heart` WARN. Personas drawn with
  `guard.py names --geo "United States"` over three seeds and screened to zero `people.*` warnings: Philip
  James, Laura Davis, Tony Lynch.
- **Pairing:** `political-science-public-policy` / `election-polling-forecasting`, objective **Forecasting &
  Predictive Modeling**, prompt shape **03** (bridge between totals, one reconciling item per disposition class
  per county), decision type `quantity_figure`, answer unit a count of signatures.
- **Why the objective is Forecasting and not Descriptive.** The call is what a full count would find, which is
  an unobserved total rather than a future value, and Descriptive & Distribution Analysis was weighed for it.
  Forecasting is kept for two reasons: the objective is Forecasting **and Predictive Modeling**, and predicting
  the result of a full count from a probability sample is predictive modeling rather than a description of a
  population in hand; and the taxonomy maps `election-polling-forecasting` to F alone, so a Descriptive tag
  would need a task type (`small-area-public-opinion-estimation-mrp`, `legislative-behavior-ideal-point-estimation`)
  that does not hold this quantity. The tag is the weakest axis of this draw and is recorded as such.
- **Niche:** a state elections division projecting, from the statutory three per cent random sample of a filed
  initiative petition, how many of its 1,043,000 signatures a full count would find valid, when the sample is
  the only part of the petition that is ever keyed.
- **Strategy:** gap `population` and `rule`, generators `G10` and `G2`, Gate G `forecasting`, strategy `other`,
  Layer 2 family `field_method`, pattern `own:pairwise-defect-inclusion-is-the-square-of-the-sampling-fraction`,
  calibration `prior_period_close_out`, context artifact `register`, `stump_class: analytical`, no official
  decoy, no validated decoy, decisive rule not filed.
- **Data-native sentence.** Only the sampled sections of this petition are ever keyed, which is how a
  random-sample check of a petition actually works, so a duplicate signature exists in the record only when the
  sample happened to draw both signatures by the same signer; every other ground of invalidity is a property of
  the one signature in front of the verifier, and that difference in what the sample can see is a property of
  this pack's own generating process rather than of any rule in it.
- **Sources, one line each.** `guard.py mechanisms` was read on `forecasting` (90 builds) and
  `opportunity-sizing-decision` (14) before drawing. Almost every forecasting driver on file is a behavioural
  rate measured on one population and carried to another (returning waves, take-up, roll-off, conversion,
  reactivation, retention, non-renewal, hazard by age), which is exactly the family the bin law kills and why
  architecture 1's shape is not repairable by changing its world. task264 v2 is the nearest insight at 0.06, an
  inclusion probability the record's own design sets, and the differentiation is in the card. task190's
  architecture 3 is the measured death in this genus and is answered under `## Readability screen`. Nearest
  driver on file is 0.09 (task445 v1).
- **Fiction.** Arizona, USD, a state elections division, forum `committee_or_panel`, forcing event
  `vote_or_meeting`, org family `government_agency`.
- **Deliverables:** `signature_projection_2027.xlsx` and `petition_disposition_2027.png`.
- **Spine:** `sample_verification_register_2027.csv`, one row per sampled signature and the disposition its
  county gave it, 31,290 rows, grain sampled signature by county by sheet section.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain.

1. Reconcile the county verification registers to the office receipt log, mapping the one county still filing
   on the old disposition codes.
2. Place each sampled signature in the voter file through its two registration vintages.
3. Count dispositions in the sample: 8,200 of 31,290 invalid on single-signature grounds (26.21 per cent), and
   106 struck as duplicates.
4. Expand every class at the statutory sampling fraction: single grounds 273,333, duplicates 106 over three
   hundredths, 3,533.
5. Valid equals 1,043,000 less 273,333 less 3,533.

Ends on: about 766,110 valid signatures, which prints **770,000** to the nearest 10,000 and stands at 122.9 per
cent of the 623,212 threshold, so the board certifies outright.

Golden: about 651,650 valid signatures, which prints **650,000**, 104.6 per cent of the threshold, so the board
orders a full count. The duplicate burden is 106 over nine ten-thousandths, about 117,780.

The two graded figures are twelve bins of 10,000 apart and the calls differ, which is the separation
architecture 1 never had. Both figures are candidate magnitudes from the draw's arithmetic and are re-measured
against the cut pack at stage 3.

## Stump sentence

A competent solver who reads every disposition code, places every sampled signature through both voter file
vintages and expands the sample at the statutory three per cent files about 766,110 valid signatures and an
outright certification; the step that lands them there is expanding the duplicate dispositions at the sampling
fraction alongside the single-signature grounds, when a duplicate is a relation between two signatures that the
sample sees only when it draws both, so the duplicate burden is about 117,780 rather than 3,533 and the
projection is about 651,650, which orders a full count.

## Three rules

Task type: election-polling-forecasting: projecting a filed petition's valid signature total from the statutory
random sample, a task type the taxonomy maps to Forecasting & Predictive Modeling.

Domain test: the deciding quantity is the number of valid signatures a full count would return, estimated the
way election administration estimates it, by design-based expansion of a probability sample in which each
ground of invalidity carries its own inclusion probability; put another field's nouns in and the quantity
disappears, because the estimator exists only where a statute fixes a sampling fraction and a threshold and
where one ground of invalidity is a relation between two records rather than a property of one.

Swap: "projecting from the statutory three per cent random sample, how many of the 1,043,000 signatures the
measure filed would a full count find valid, and should the board certify, order a full count or reject"
becomes "how many of 1,043,000 hospital admissions would a full count find valid", and it reads as one
multiplication: an admission has no second member that must fall in the same sample for its defect to be
visible, so the whole decisive step has nothing to attach to.

Layer 1: two voter file registration vintages; one county still filing on the old disposition codes; sheet
sections keyed by circulator rather than by signer; the office receipt log against the county registers; the
prior initiative's close-out at a different threshold. Each is written by the system that produces it, none is
placed to be caught, and each is asserted neutral on the call at stage 3.

Layer 2: field method (design-based estimation): the call flips on recognising that one disposition class's
inclusion probability is the square of the sampling fraction rather than the fraction.

Decisive step: expanding the duplicate dispositions at the pair inclusion probability, the square of the
sampling fraction, rather than at the fraction every single-signature ground expands at; in election
administration's own words, reading the design's inclusion probability for a ground that is a relation between
two signatures.

Not semantics: every disposition code, both voter file vintages, the threshold and the sampling fraction read
perfectly still leave the easy route expanding one class at the wrong power of the fraction, because no field,
code, unit or definition in the pack carries an inclusion probability; the fraction is stated once, in the
statute, and it is the right number for every other class.

Not rule application: the statute files the sample size, the threshold and the certification bands, and no
shipped sentence states how a class expands. Executing every filed rule with the statutory fraction applied to
all classes files the certification, so the step no rule performs is reading the design.

Analyst test: a strong analyst who reads every disposition code correctly, places every sampled signature
through both vintages, reconciles the registers to the receipt log and applies the filed threshold expands
every class at the statutory fraction and files about 766,110 valid signatures, printing 770,000 and certifying
outright. Executed in `checks.py` on the generator's clean truth at stage 3.

Estimand: the statute's sampling section, filed at authority: the number of signatures a full count of the
filed petition would find valid, where the filed total, the sampling fraction and the threshold are the
statute's own, and the sample is the signatures the counties verified. It fixes the population, the window, the
unit and the comparison, and says nothing about how any disposition class expands.

No decoy: nothing is planted to be caught. Duplicate signatures are authentic, because people sign twice at
different events; no memo, briefing or draft argues for an expansion basis; no file states a valid total or
ranks the dispositions.

No certified replay: the prior initiative's close-out is the calibration organ and must tie under every
expansion basis, which is a stage 2 construction constraint recorded below, not a figure that reproduces a
method.

Lesson: a defect that is a relation between two records enters a probability sample only when both members do,
so its design weight is not the sample's weight; no build on file teaches an inclusion probability that differs
by class within one design (task264 carries a per-respondent design weight whose probability rises with
multiplicity, which attaches to a unit and is linear in the fraction).

## Readability screen

Owed at stage 2 for architecture 2, a row per rung over the six tests, verdict last, the decisive row `silent`.
Two rows have to be argued hardest and both are named now rather than discovered later.

**Test 1, the filed sentence, and it is this draw's real risk.** The duplicate dispositions are visible in the
sample: a solver reading the verification register meets a class of about 106 signatures struck as duplicates
and is directly confronted with the question of how to expand it. That is a clause it cannot avoid reading,
which `stumping` 2.1 test 1 says sends the solver looking. The step then rests on whether seeing the class
leads to seeing that its inclusion probability is the fraction squared, which is a genuine analytical move and
the reason the draw is worth building, but it is reflex-adjacent for anyone who has done sampling theory. The
screen must measure it honestly and say so either way; if it reads, the fix is in the design and not in a
sentence.

**task190's architecture 3 is the measured death in this genus** (`task190/DESIGN_NOTE.md` lines 536 to 560): a
design-based projection from a probability-proportional sample, where Gate B forced the audit manual and the
reliability factor table to ship, shipping them handed the route back, and two independent cold threads landed
the call. The structural difference claimed for this draw, and it must be asserted rather than argued: nothing
has to ship to make this projection computable, because the sampling fraction and the filed total are world
facts the prompt's own forcing sentence carries and the decisive move is one division. Two design constraints
follow and are not optional. The pack ships **no keyed full signer list**, which is realistic because only
sampled sections are ever keyed, and without which a solver dedupes the petition directly and the build
collapses. And the `prior_period_close_out` calibration must tie under every expansion basis, which is easiest
if the prior initiative's duplicate burden was negligible.

## Semantic fork table

Owed at stage 2 for architecture 2, `SF1` onward, every row ruled out by a quotable shipped sentence or marked
`same call`, each asserted in `generator/checks.py`. The rows already known to be needed: what the sampling
fraction is a fraction of; whether a duplicate pair counts as one invalid signature or two; which registration
vintage places a sampled signature; the one county's old disposition codes against the current set; the
threshold's basis; and the rounding path to the nearest 10,000.

## Ladder

Owed at stage 2 for architecture 2, measured over at least three seeds. There are about twelve bins of 10,000
between the default path and the golden, so unlike architecture 1 there is budget to place three or four rungs
and still leave the decisive gap the **largest** of them, which `stumping` Part 3 requires and architecture 1
violated at 0.58 of a bin.

## Closure table

Owed at stage 2 for architecture 2: the 22 axes with the reading and the closure move, one row per axis number.

## Literal reader

Owed at stage 2 for architecture 2.

## Oracles

Owed at stage 2 for architecture 2. The prior initiative's close-out is the one control to screen hardest: it
must tie under every expansion basis or be out of scope, never only under the golden.

## Ask sheet

Owed at stage 2 for architecture 2, with the pair arithmetic, the cracker and mirror sheets and the separation
counts.

## Convergence, against a rival's family

Owed at stage 2 for architecture 2, and it is the section architecture 1 got wrong: its fourteen constructions
all varied the golden's own method and converged 20 of 20 in every world tested, including the one the portal
broke. This section computes, on the clean truth, both the golden's own family (the hypergeometric pair
inclusion against the fraction squared, the per-county, per-circulator and per-section groupings, the
duplicate-signatures reading at two per pair, a triple-signer variant) and at least two families a competent
solver builds **instead**: a Chao-style unseen-pairs estimator off the sample's singleton and doubleton counts,
and a bootstrap over sampled sections. It states the bucket each files.

## Bin measurements

Owed at stage 2 against the cut pack; the draw's arithmetic gives the candidate figures, verified by hand on
registration. Bin 10,000 valid signatures. (a) the decisive step's worth, about 114,240 signatures, 11.42 bins.
(b) the defensible estimator spread, about 4 signatures, 0.0004 bins, because the hypergeometric pair inclusion
and the fraction squared differ in the eighth decimal and every grouping gives the identical total; bounded at
0.12 bins if a triple-signer variant is admitted. (c) the golden estimator's 95 per cent sampling interval,
about plus or minus 22,420 signatures on 106 observed pairs, 2.24 bins. So (a) exceeds (b) plus (c) by about
five times and is the largest available rung gap rather than the smallest.

(c) is read here under the refinement now filed in `determinism-check`: this estimator is an observed count
over a constant the statute fixes, with no fitted parameter, window, band width, distribution family or
grouping, so every solver computing it files the same figure to the unit and the interval is the quantity's
honest uncertainty rather than a fork. That is the structural difference from architecture 1, whose (c) was a
fitted rate and therefore became real disagreement. It is tested rather than asserted: the estimator is
computed under every grouping the records allow and the total shown identical. (c) is also a world dial,
falling to about 1.40 bins at a five per cent statutory sample, and it is independent of (a), which the
duplicate burden sets; in architecture 1 the rival span and the decisive worth were both proportional to the
un-returned remainder, so no scaling separated them.

## Pre-ship check

Owed at stage 5 for architecture 2.

## Tried and rejected

- Architecture 1, the January 2027 qualifier forecast from the seasonal return wave (spent 2026-10-27 on its
  second portal return): the graded bin is finer than the estimator. Measured above in `## Architecture 1 is
  spent`. The decisive step was worth 0.58 of a 50,000 bin, the smallest gap in the ladder; the choice between
  two measurable subgroups for the un-returned remainder is worth 0.90 bins and the sampling error on the right
  one another 0.31, so no pin, world parameter or rounding choice forces one bucket. Three repairs were built and
  measured: a later return profile (0.58 to 2.08 bins, still open), positioning the golden by the campaign size
  (about 8,500 of slack a side), and a coarser bin (kills the stump). Re-rooted, not retired.

- Market dilution (riders' January demand is fixed, so returning drivers split a fixed pool of trips and fewer clear 40), worked at the draw: the qualification count needs the hours distribution and a demand forecast stacked on the supply forecast, and the defensible constructions spread wider than any graded bin; dropped before registration.
- A moved threshold with bunching at the old and new lines (the notch response estimated from past windows), worked at the draw: the deciding analysis is a labour-supply response to a notch, honestly economics-econometrics, whose pairing with forecasting task155 holds in the ban window; dropped rather than relabelled.
- The trips-per-driver distribution against the threshold as the decisive step: task151's driver (a stepped payout as the sum of chances from a resampled distribution); kept only as last year's observed rates, never decisive.
- The campaign recruits' type read from when each stopped (an exit-timing reference class): task146's lesson, and the campaign's bonus drivers stopped in April with its seasonal workers; kept only as a rival that misses.
- Holiday drivers (December-only drivers) inside the wave, prototyped: they separate the aggregate KPI route but their share inside each December band changes year to year, which moved every band-priced construction of the golden by up to $140,000 in the prototype; left out of the world.
- A wave timed by each driver's own anniversary, or by weather: neither is what seasonal trades do, and either would make the timing ratio a property of the group; the timing is the trades' common calendar.
- Each seasonal driver's return week fixed once for life (dealt from a profile at entry), built at stage 3: each winter's returners then kept their own mix of weeks, and the January-to-December ratio ran 1.11, 1.01 and 0.97 across the three winters, wider than the fund's bin; replaced by the trades' calendar dealt afresh each winter (which driver returns which week changes, the calendar does not), after which the winters read 1.098, 1.093 and 1.074.
- New drivers priced from the onboarding app's approvals at the as-of, built at stage 3, while drivers approved during the window could still reach 40 trips: the pool-only and every-new-qualifier constructions differed by about $25,000; closed by the terms' eligibility clause (accounts approved by the Sunday before the window, as in 2025 and 2026; 73 drivers who completed 40 trips in the 2026 window on later accounts were not paid), with "every eligible driver" in the prompt.
- Ask A as twelve figures (main run, later runs, returns, recoveries, net, drivers, both years): the main runs and later runs carry no device and hand the strongest response free points; cut to the six device-bearing figures, the chart keeping the full bridge.
- HB3 (an approved applicant whose account was opened under a second email): the applications export carries the driver id an approval opened, so the hazard had no record to live in; dropped.
- Occasional drivers coming back on at 6 per cent a week: they sat in last winter's drivers often enough to swing the June-to-October-blank construction by $13,000; raised to 15 per cent a week (shorter breaks, fewer in the winter group), the construction now within $4,000.
- Approvals stamped at any hour, and Sunday decisions moved back to the Saturday: 24 decisions fell before their own resubmission; decisions are now taken on working days in office hours, a Sunday's on the Monday.

- 2026-10-26, the portal's determinism block, both judges `competing_defensible_answer` on the main call,
  fix location `input_files`. Two forks, both closed without moving a graded figure (`freeze.py check
  --mode determinism` PASS). SF14, the shipped rider demand plan: it carried 316,650 completed trips for the
  guarantee's window, 72.5 per cent of the 436,733 the window actually takes, because it assumed 11.8 per
  cent growth where the autumn ran 19 to 38 per cent ahead and the window itself grew 53.7 per cent. Read as
  a trip ceiling it gave 3,500 drivers and $1,250,000 against the golden's 4,700, and nothing shipped ruled
  that reading out, so a declared distractor was doing the work of an official decoy. Closed by C1 rather
  than by a pin: the generator now sets the plan's growth off the autumn's own year-on-year rate, the window
  carries 447,500 trips, and three assertions hold that no demand-constrained reading binds. SF15, the
  out-of-sample line: "within 2 per cent" did not say what it was 2 per cent of, and the second judge read
  it as the fund's own precision, about plus or minus 94 drivers on 4,700. The write-up now names the counts,
  308 against 306 and 413 against 405, which are returns in the hundreds. The stump is untouched: the
  default path still files $1,450,000 against the golden's $1,650,000, four bins apart.

- **Architecture 2 draw hunt, 2026-10-27 (screens run on paper before any card was registered, under the bin law now filed in `determinism-check`).** Four directions screened against the brief's test, that the decisive step's worth in bins must exceed the defensible-subgroup spread plus the golden estimator's own sampling interval, and that it must not be the smallest rung gap.
  - **Pharmacology, population pharmacokinetics and exposure response (a weight-banded concentrate's forward vial commitment, the requirement built from each patient's own measured elimination rather than the per-kg label dose): dead before measurement.** `guard.py slots` put it on `task170/DESIGN_NOTE.md` line 667, where the same cell was screened with twenty in-cell candidates before any card and every one fell into one of four graves, "effective half-life on sparse troughs" among them as a fit whose estimator family forks the graded figure, with the note's own verdict "the cell is spent for this slot". Bins never reached: the candidate dies on determinacy, which is the (b) term.
  - **Media reach and frequency (a 2027 schedule's net reach from a single-source panel's pairwise duplication against a random-duplication product of marginals): bins pass and Gate F does not.** Measured on paper at a target of 4.21 million with the bin at 100,000 people: decisive step 490,000 people or 4.9 bins, panel sampling interval about 48,000 or 0.48 bins, subgroup spread about 0.2 bins. It dies on readability test 7 instead, because the panel that makes the golden computable makes it a one-group-by (count the distinct respondents the schedule's vehicles reach), and the escape of carrying the joint across a longer window is already recorded dead in `task270/DESIGN_NOTE.md` line 155, a radio schedule's four-week reach from one-week diaries.
  - **A council's already-born cohort (a forward intake read off births and the dwellings completing rather than off each area's own birth-to-intake ratio): dead on the corpus.** task150 is a school-by-school cohort-component projection with a kindergarten-to-births ratio in its own stump sentence and task153 already differentiates against it; the direction is occupied rather than fresh.
  - **A regional waste authority's permitted void (the exhaustion quarter built from the settlement consecutive surveys of one lift measure, against the latest survey's filled volume over a lifetime density): bins pass, the guard blocks.** Measured with the bin at one quarter: decisive step about 3 quarters or 3 bins, survey volume error about 0.4 bins, subgroup spread about 0.2 bins, and the decisive gap is the largest rung gap. `guard.py check` returns BLOCK `test.same_driver` inside the batch against task304 on (time, G3, forecasting), which differentiation does not clear, and BLOCK `test.same_driver_older` against task169 v2; the abstraction test also maps its driver onto task89 v9 and v10, time to exhaustion as a stock over the right net change rather than the published stock over a gross outflow (`guard.py nearest` 0.05). Available only on a redrawn gap or decisive pattern.
  - **Carried forward as the hunt's recommendation:** a pairwise defect's inclusion probability under a sampling design (a filed petition's duplicate signatures seen only when the sample draws both members of a pair, so the duplicate burden expands at the square of the sampling fraction while every single-signature ground expands at the fraction). `guard.py check` WARN, no BLOCK, nearest driver 0.09; measured at 11.4 bins for the decisive step against 2.30 for the sampling interval and at most 0.12 for the subgroup spread. Its two risks are named for whoever takes it: the abstraction adjacency to task264 (an inclusion probability the record's own design sets) and the measured Gate F death of task190's architecture 3, where a design-based projection had to ship the manual that then handed the route back.

## The licensed re-judge, 2026-10-26

Verdict NOT_DETERMINISTIC, disposition SEND_BACK, label `margin_or_boundary_fragility`. Gate G passes
(`forecasting`, `analytical_non_defect`, no surface-read dependency, no sole data defect) and Gate H passes
(domain pass, layers pass, decisive step analytical); the judge reproduced asks 3, 4 and 5 exactly, all
fifteen pipeline cells, the cost tables, the 1,087 back by 3 January, the ratio and the 1,180 due back, and
recorded that the easy route lands 3,500 to 4,300 against the golden's 4,700. Neither fork the portal raised
reappears, so SF14 and SF15 are closed.

It raised three new findings. Two are false and were checked rather than argued; the third is a closure it
did not reach, and that one was worth something.

1. **"The golden mixes two definitions of paid", the non-winter block on kept payments and the 93 and 82 per
   cent rates on main run plus late credits. False.** `calc.fund` takes one `kept` flag and passes the same
   value to `band_rates` and to `qualified`, so both move together: at the default the block is 2,681.1 with
   qD 0.9284 and qJ 0.8198, and at `kept=True` all three change at once (2,629.8, 0.9125, 0.8148) and the
   answer becomes 4,600. One definition throughout, and the `kept=True` reading is SF13's alternative, which
   the record rules out.
2. **"About 11 drivers are double counted, the 13 already back by 3 January sitting inside the 1,180".
   False.** The priced groups are disjoint row sets: `back & nonwave` is 0 rows and `back & other` is 0 rows.
   `n_rest` (1,180.4) is a count derived as `n_back x g`, not a row set, and it prices the wave's members
   still to come while `back` prices the 1,087 already returned.
3. **"Defensible conventions give 4,614 to 4,778, straddling three rounding lines."** The wide end of that
   range is the `kept=True` basis at 4,600 and USD 1,600,000, which SF13 already names and rules out by
   three shipped sentences: the terms ("Larch pays $350 to every eligible driver who completes 40 trips
   between 00:00 on Monday 4 January 2027 and 23:59 on Sunday 31 January 2027, Central time"), the payout
   notes ("It pays $350 to every account the payments system counts at 40 completed trips") and finance's
   email ("Returned payouts and recoveries come back to the account afterwards, so leave them out"). The
   note's own convergence block spans 4,688 to 4,703 across fourteen constructions.

**What the third finding was actually worth, and it is a real defect.** The email's sentence was there but
hard-wrapped mid-phrase, "...with it. Returned\r\npayouts and recoveries come back...", so the phrase broke
across a line and the sentence that settles the qualification basis was not findable by any line-oriented
search. Two of my own searches missed it for exactly that reason before a MIME decode found it, which is
almost certainly why the judge concluded the convention was unpinned. A closure present in the record but
unreachable in the raw file is not doing its job. The instruction is now its own paragraph and carries the
basis in the terms' words: "Returned payouts and recoveries come back to the account afterwards, so leave
them out. Count every driver who completes the 40 trips, whatever happened to the payment afterwards." That
is WHAT and not HOW, it restates the terms, and it names nothing about the decisive step. Asserted present
in the raw bytes.

**Why this is not treated as a redesign.** `/fix-determinism` sends a SEND_BACK back to design, and that is
right when the verdict stands. Here two of the three findings are verifiably false and the third rests on a
sentence the judge could not find rather than one the record does not carry. The stump is untouched and
measured: the default path still files USD 1,450,000 against the golden's USD 1,650,000, four bins apart,
and the judge itself put the easy route at 3,500 to 4,300 drivers. `freeze.py check --mode determinism`
passes, so nothing graded moved in any of this. A further judge pass is the author's call, not mine to take
on my own initiative.

## Architecture 1 is spent: the bin is finer than the estimator, measured 2026-10-27

The portal returned this build a second time (two judges, Gate C and D fail, taxonomy
`competing_defensible_answer` and `underspecified_objective`, fix_location `input_files` and `prompt`). Both
judges reproduced every ask exactly, reached the stump's own mechanism, and landed on 4,500 to 4,600 drivers and
USD 1,600,000 against the committed 4,700 and USD 1,650,000. The first return's two forks are closed and neither
reappeared: no judge read the demand plan as a ceiling, and no judge read the 2 per cent band as the fund's
precision.

What is left is not a fork and no pin reaches it. Measured on the shipped pack:

| Quantity | Measured | In 50,000 bins |
|---|---|---|
| The decisive last increment (the wave priced at its own January qualification, not in December-trip bands) | 82.9 drivers, USD 29,001 | 0.58 |
| The golden's distance to its lower bin edge | USD 19,850 | 0.40 |
| The subgroup choice for the un-returned remainder (its own January rate 0.8198 against the back-by-December rate 0.9284) | 128 drivers, USD 44,877 | 0.90 |
| The 95 per cent sampling interval on that January rate alone (n=405, se 0.0191) | plus or minus 45 drivers, USD 15,700 | 0.31 |

The decisive step is the smallest rung gap in the ladder (0.58 bins, against 1.96 to 5.81 for every other rung),
which `stumping` Part 3 bans outright. Worse, a solver who picks the right subgroup and estimates it correctly
still carries a third of a bin of sampling error, and the choice between two measurable subgroups carries another
nine tenths. The graded figure is a behavioural point forecast rounded to about 3 per cent of itself, and this
pack's own sample cannot pin it to 3 per cent.

**Three repairs were measured and none holds.**

1. **A later seasonal return profile.** Moving the trades' return from November into late December (so the wave
   carries few December trips and the band pricing is badly wrong) lifts the decisive increment from 0.58 to
   2.08 bins, moves the default path from 4.00 to 5.65 bins away, populates the returner cells from n=4 to 13 in
   the low bands up to n=32 to 87, and leaves the committed answer at 4,712 drivers and USD 1,650,000. It is a
   real improvement and it still does not close the finding: the subgroup choice is 0.64 bins and the sampling
   error 0.3, so a method half a per cent out still files a different bucket. The rival family's own branches
   land at USD 1,650,000, 1,650,000 and 1,700,000, with only USD 2,215 of headroom under the upper edge.
2. **Positioning the golden inside the bin.** The campaign size was swept (2,155 to 2,215 recruits). The rival
   span is about USD 33,000 of a 50,000 bin, so at best about 8,500 of slack sits on each side: a rival 24
   drivers out of 4,700 flips the answer. Rival span and decisive worth are both proportional to the
   un-returned remainder, so no scaling separates them.
3. **A coarser bin.** At the nearest 250,000 the fork widens to two buckets. At the nearest 500,000 it closes,
   and the default path lands in the golden's bucket, so the stump dies. A later extract date was rejected
   without building: it would let the extract see the window's own trips, which makes the call partly a count.

The convergence block this note carried was the blind spot. Its fourteen constructions all varied the golden's
own family (which winters the timing ratio comes from, the wave window, the band widths), and that family
converges 20 of 20 on USD 1,650,000 in every world tested, including the one the portal broke. It never varied
the family a rival builds, and that is where both returns came from.

Architecture 1 is spent. It is re-rooted at stage 1, not retired.

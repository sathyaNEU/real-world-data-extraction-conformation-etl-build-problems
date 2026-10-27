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
- **Niche:** a state elections division projecting, from the statutory five per cent random sample of a filed
  initiative petition, how many of its 540,000 signatures a full count would find valid, when the sample is
  the only part of the petition that is ever keyed.
- **The world's figures were corrected at stage 2, and this is the correction the author has to read first.**
  The draw's candidate magnitudes (1,043,000 signatures filed, a three per cent sample, a 623,212 threshold and
  95 and 110 per cent bands) are California's statute, attached to an Arizona card: 623,212 is California's own
  statutory initiative requirement for the 2019 to 2022 cycle, its sample is three per cent of sections and its
  bands are 95 and 110. Arizona's own statute, which the card's geography names, samples **five per cent of the
  signatures filed** and sets the bands at **95 and 105 per cent** of the required number. The world is
  therefore rebuilt on Arizona's statute: 540,000 signature lines on 36,000 sheets of 15 lines, a 27,000 line
  sample, a required number of 384,924 (15 per cent of the 2,566,154 votes cast for Governor in 2026), and
  bands at 365,678 and 404,170. Nothing about the decisive step moves: the sample is of signature lines, so a
  pair's inclusion probability is the square of the sampling fraction exactly, which is the registered driver
  and which the three per cent reading would not have been, because a sample drawn by whole sections makes a
  same-section pair's inclusion the fraction itself. **The card's `answer`, `niche` and `spine.rows` are stale
  against this note and are the author's to update; the driver, the stump, the strategy and every axis stand.**
  Two consequences the card also carries: its Layer 1 item "the sample drawn by sheet sections, so the keyed
  rows are sections rather than signatures" is withdrawn, because under Arizona's statute the sample is drawn
  line by line, and the spine is 27,000 rows rather than 31,290.
- **The six guard WARNs, one line each.** `overuse.org_family`, government_agency in 40 builds: the deciding
  body is a state elections division and no other organisation family can hold a statutory sample projection,
  so the variety is carried by the driver, which scores 0.09 against the whole corpus. `repeat.gate_g` and
  `overuse.gate_g`, forecasting in 5 of the last 12: no other Gate G key is true of this build, since the
  quantity is unobserved and the correctly read sample does not pin it linearly; the lane is a forecasting lane
  and the honest key is the repeated one. `repeat.decision`, quantity_figure against task464: the call is a
  count of signatures and a band, and task464's shared key is its only similarity, its gap, pattern, Gate G and
  driver all differing. `repeat.deliverables`, png and xlsx against task144: the shape is a bridge between
  totals, which a workbook holds and a chart reads at a glance, and no third format would be a real analyst's
  output here. `repeat.question_form`, how-many against task464: the decision is a count, and
  `guide-to-prompt` takes the question's form from the decision.
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
  county gave it, 27,000 rows, grain sampled signature by county by sheet section.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain.

1. Reconcile the fifteen county verification registers to the office receipt log, mapping the one county still
   filing on the pre-2024 disposition codes.
2. Validate the counties' registration determinations against the statewide voter extract, taking the extract
   whose run date precedes the signing window because the statute asks for registration at the time of
   signing; that extract still shows 400 sampled signers registered who were cancelled in the list-maintenance
   run inside the window and signed afterwards, so those 400 are not struck.
3. Count dispositions in the sample: 5,337 invalid on single-signature grounds and 92 struck as duplicates, of
   27,000 sampled lines.
4. Expand every class at the sample's own factor of 20: single grounds 106,740, duplicates 92 times 20, 1,840.
5. Valid equals 540,000 less 106,740 less 1,840.

Ends on: 431,420 valid signatures, which prints **430,000** to the nearest 5,000 and stands at 112.1 per cent of
the required 384,924, above the statute's 105 per cent line, so the measure is sufficient and goes on the
ballot.

Golden: 388,460 valid signatures, which prints **390,000**, 100.9 per cent of the required number and inside
the 95 to 105 per cent band, so a full count is ordered. The duplicate burden is 92 over nine ten-thousandths,
36,800, and the single-ground burden is the counties' 5,737 strikes expanded at 20, 114,740.

The two graded figures are 8.59 bins of 5,000 apart and the statutory calls differ, which is the separation
architecture 1 never had: there the two figures were four bins apart and the decisive step was worth 0.58 of
one. Figures are at design seed 157 on the generator's clean truth and are re-measured against the cut pack at
stage 3.

## Stump sentence

A competent solver who reads every disposition code, validates the counties' registration determinations
against the voter extract whose run date precedes the signing window and expands every class at the sample's
own factor of 20 files 431,420 valid signatures and a sufficient measure that goes on the ballot; the step that
lands them there is expanding the duplicate dispositions at the sampling fraction alongside the
single-signature grounds, when a duplicate is a relation between two signatures that the sample sees only when
it draws both, so the duplicate burden is 36,800 rather than 1,840 and the projection is 388,460, which orders
a full count.

## Three rules

Task type: election-polling-forecasting: projecting a filed petition's valid signature total from the statutory
random sample, a task type the taxonomy maps to Forecasting & Predictive Modeling.

Domain test: the deciding quantity is the number of valid signatures a full count would return, estimated the
way election administration estimates it, by design-based expansion of a probability sample in which each
ground of invalidity carries its own inclusion probability; put another field's nouns in and the quantity
disappears, because the estimator exists only where a statute fixes a sampling fraction and a threshold and
where one ground of invalidity is a relation between two records rather than a property of one.

Swap: "projecting from the statutory five per cent random sample, how many of the 540,000 signatures the
measure filed would a full count find valid, and does the measure qualify, go to a full count or fail" becomes
"how many of 540,000 hospital admissions would a full count find valid", and it reads as one multiplication: an admission has no second member that must fall in the same sample for its defect to be
visible, so the whole decisive step has nothing to attach to.

Layer 1: two statewide voter extracts with their own run dates either side of a list-maintenance run inside
the circulation window; one county still filing on the pre-2024 disposition codes, which merge two grounds;
two counties that filed their register twice, the correction superseding row by row; 240 sheets filed twice by
two circulator firms and struck at receipt, so the receipt log and the counties' reported sheet counts differ;
extract timestamps in UTC against local signing dates; the prior measure's full-count close-out under the old
code set. Each is written by the system that produces it, none is
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

Analyst test: a strong analyst who reads every disposition code correctly, validates the counties'
determinations against the voter extract that precedes the signing window, reconciles the registers to the
receipt log and applies the required number expands every class at the sample's own factor and files 431,420
valid signatures, printing 430,000 and a sufficient measure. Executed in `checks.py` on the generator's clean truth at stage 3.

Estimand: the statute's sampling section, filed at authority: the number of signatures a full count of the
filed petition would find valid, where the filed total (540,000 lines on the office receipt log), the sampling
fraction (five per cent of the signatures filed) and the required number (384,924) are the statute's own, and
the sample is the 27,000 signatures the counties verified. It fixes the population, the window, the
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

Measured, not argued: `generator/cracker.py` enumerates the reflex row from election administration's and
sampling's own vocabulary for a sample projection and computes every route on the clean truth over six seeds.
Nine routes were run. **Not one route outside the pair-inclusion family reaches the golden's printed cell or
its statutory band**: the linear family lands 6.62 to 8.59 bins away and files `sufficient` at every seed, the
signer-base and the two-p corrections land 6.99 and 7.18 bins away, and the capture-recapture reflex
self-destructs at minus 3,482,881 valid signatures. So the duplicate class being visible in the sample takes a
solver to rung 1 and rung 1 is seven bins wrong in the band that certifies the measure.

| rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | 7 organ | verdict |
|---|---|---|---|---|---|---|---|---|
| 0 registration re-derived off the pre-run extract, every class at the sample's factor (431,420) | the extracts carry their own run dates | two extracts in the pack | yes, the opponent validates the counties' work | none | the battery finds the date overlap | yes, one join | no organ | readable |
| 1 the counties' dispositions as filed, every class at the sample's factor (423,420) | the statute names the sample and the threshold | the disposition column | yes, the opponent's default projection | none | no | yes, one ratio | no organ | readable |
| 2 pair inclusion on the cross-county strikes only, county strikes at the sample's factor (410,120) | no | the register names which body struck each duplicate | partly, a solver that senses the pair problem | none | no | no | no organ | readable |
| 3 (decisive) every duplicate strike at the pair's own inclusion probability (388,460) | no shipped sentence names a pair, an inclusion probability, a squared fraction or a count of signers | no column pairs two lines and no match key ships | no: 9 of 9 enumerated routes land 4.33 to 8.59 bins away, measured | no control scores the expansion bases | the battery reaches the extracts and the merged code, not the expansion | no: it is a different power of a number the statute states once, and every route that takes the obvious ratios is measured wrong | every file is one the office keeps for its own reasons and the pack ships no reliability factor, manual or allowance | silent |

**Test 1 and this draw's exposure, answered.** The duplicate class is unavoidable and has to be, or there is no
decisive step and Gate B fails. What test 1 asks is whether a clause names the decisive quantity, and the
decisive quantity is the duplicate burden in the whole petition, which no clause names: the statute names the
sampling fraction once, and that fraction is the right number for every other class. The sweep is the evidence
and it is the honest kind: a route that meets the class and asks how to expand it lands on rung 1. The limit of
the measurement is stated plainly: it scores the routes enumerated here, computed as code, and nothing
beyond it is owed. CLAUDE.md's STOP block of 2026-10-27 retires the solver flow outright, so there is no
scored or blind reader at stage 4 or anywhere else; stump power is argued on paper here and measured by the
portal alone. The nine-route sweep IS the paper argument, and the only readers that still run are the
isolated leak reader, which reads the pack for leaks and never solves it, and the determinism judge.

**task190's architecture 3, asserted rather than argued.** That build died because Gate B forced its audit
manual and reliability factor table into the pack and shipping them handed the route back. Here nothing has to
ship to make the projection computable: the filed total, the sampling fraction and the threshold are the
statute's, and the decisive move is one division. Two constraints are therefore load-bearing and are asserted
in the generator at stage 3. **No keyed full signer list ships**, because only sampled sections are ever keyed,
and the pack's own extent carries that fact (no file holds a line outside the sampled sections) rather than any
sentence stating it. And **no reliability factor, projection manual, settlement allowance or duplicate
allowance ships in any form**.

## Semantic fork table

Every row closed by a quotable shipped sentence, by C1 convergence, or marked `same call` with the measured
distance. Each id is asserted in `generator/checks.py` at stage 3; the ids and their closures are fixed now.

| id | the term or convention | the readings | ruled out by |
|---|---|---|---|
| SF1 | what the five per cent is five per cent of | the signatures filed, or the sheets filed | the statute's sampling section names the signatures filed; the office sample receipt states 27,000 of 540,000; C1, the sample is drawn line by line so both readings give the same factor of 20 |
| SF2 | a duplicate pair is one invalid signature or two | strike the later line, or strike both | the statute: a signature shall not be counted more than once, so one line of the pair stands; measured, the both-lines reading lands 6.62 bins away and is a named wrong cell in the grid rather than a live reading |
| SF3 | which registration extract places a sampled signature | the extract current when circulation opened, or the one current at verification | the statute's "registered at the time of signing" plus each extract's own run date; C4, the pre-run reading is rung 0 and is measured 1.60 bins away from rung 1 |
| SF4 | the one county's pre-2024 merged disposition code | duplicates folded into the general class, or unfolded | C1 in the world: that county's sampled lines were gathered by one firm in one week and carry no duplicate strike at all, so the fold cannot move any figure. Measured first at a 9.2 per cent share, where unfolding moved the golden 0.61 bins while four of six seeds sat 0.03 to 0.19 bins from a cell edge, so it was load-bearing and had to be closed in the world rather than by a sentence |
| SF5 | the filed total | the office receipt log, or the counties' reported sheet counts | the statute files the projection on the signatures filed and the receipt log is the statutory record of filing; measured at 390,803 against the golden's 388,460, `same call` and the same printed cell, asserted convergent on the shipped pack |
| SF6 | the order the grounds are applied in | not registered before duplicate, or duplicate first | the counties' verification instruction states the order; a signature carries exactly one disposition, asserted as a partition of the sampled lines |
| SF7 | the rounding path | once on the projected valid total, or per disposition line then summed | the asking sentence rounds the projected valid total to the nearest 5,000 and every other projected figure to the nearest 100, so the total is rounded once from the unrounded projection |
| SF8 | the band the projection falls in | at or above 105 per cent, or above it | the statute's own words, strict above; C1, the golden sits 3.14 bins inside the band at the design seed and no seed puts it on a boundary |

## Ladder

Four rungs, each a defensible analysis climbed by refusing it, measured by `generator/cracker.py` on the clean
truth over six seeds (157 to 162). Figures at seed 157; the per-seed table is in `## Bin measurements`.

| rung | the analysis | valid | printed | band | gap to the next rung | dies to |
|---|---|---|---|---|---|---|
| 0 | registration re-derived off the extract current when circulation opened, every disposition class expanded at the sample's own factor | 431,420 | 430,000 | sufficient | 1.60 bins | each extract's own run date against the signing dates, and the list-maintenance run inside the circulation window |
| 1 | the counties' own determinations taken as the statute assigns them, every class still expanded at the sample's factor | 423,420 | 425,000 | sufficient | 2.66 bins | the pack holds no keyed line outside the sampled sections, so a duplicate exists in the record only where both of a signer's lines were drawn |
| 2 | the pair inclusion applied to the cross-county strikes only, on the view that a county checked its own whole batch | 410,120 | 410,000 | sufficient | **4.33 bins** | the same shipped fact: no county keyed a line outside its own sampled sections, so no full-batch check was possible |
| 3 (decisive) | every duplicate strike at the pair's own inclusion probability, the square of the sampling fraction | 388,460 | 390,000 | **full count** | | |

**Worth.** Computed on the graded quantity, never an intermediate. Gaps over six seeds: rung 0 to 1 is 1.60
bins at every seed, rung 1 to 2 runs 2.66 to 3.57 (mean 3.27), rung 2 to 3 runs 4.33 to 5.78 (mean 5.31). **The
decisive gap is the largest at every one of the six seeds**, and its worst value, 4.33 bins, is 2.4 times the
largest measured sum of (b) and (c). Architecture 1's decisive gap was 0.58 of a bin and the smallest in its
ladder; this is the number that changed.

**Position and dominance.** The decision is a figure and a statutory band, so position is read on the band: the
golden files `full count` at all six seeds and every one of the nine enumerated routes outside the
pair-inclusion family files `sufficient`, so no rung shares the golden's call. Dominance: the golden's distance
to the nearest band boundary is 3.14 bins at the design seed (4.49 bins mean above, 3.21 mean below), against
(b) plus (c) of at most 1.82 bins.

**The grid.** Every cell a partial application reaches is a named wrong answer: the pre-run extract alone
(430,000), the counties' dispositions alone (425,000), both lines of a pair struck (420,000), the signer-base
expansion (425,000), the two-p correction (425,000), the cross-county split (410,000), and the
capture-recapture reflex (a negative total that refutes itself). Single-error cells all file feasible figures
in the `sufficient` band; none files the golden's cell.

**Margins.** No gap under 1.15 times the printed cell: the smallest, 1.60 bins, is 1.60 times it. Each rung's
printed figure sits in its own cell at the design seed, with measured cell-edge distances of 1,080 for rung 0,
920 for rung 1, 2,380 for rung 2 and 960 for the golden. Rung 1 at 920 and the golden at 960 are the two that
the stage 3 parameter pin has to move out to 1,500 or more; the targets are in `## Bin measurements`.

## Closure table

The 22 axes of `determinism-check` section 3, each with the reading it admits and the move that closes it.

| axis | the axis | the reading here | closure |
|---|---|---|---|
| 1 | Population | the signatures filed for this measure | the statute's sampling section files the filed total; the office receipt log is the record of filing; C1 with SF5 |
| 2 | Unit of account | the signature line, not the sheet or the signer | the asking sentence counts signatures; SF1 closes the fraction's base and C1 makes both readings one factor |
| 3 | Attribution window | which month a signature was signed in | the signing date on the line; the circulation window is fixed by the statute's own filing deadline |
| 4 | As-of dating | registration status as at signing | the statute's "registered at the time of signing"; SF3, each extract carries its run date |
| 5 | Version basis | the county register as filed or as corrected | the correction supersedes row by row and carries its own date; asserted on the shipped pack |
| 6 | Denominator | the sampled lines, per county and per class | the office sample receipt states the sampled count; every rate is over the sampled lines of its own cell |
| 7 | Weighting | pooled or per county | C1, the estimator is a count over a constant the statute fixes, so every grouping gives the identical total; measured at (b) equals 0.000 bins over six seeds |
| 8 | Window length | none: no rate is measured over a look-back | not applicable today, recorded as such |
| 9 | Boundary inclusivity | the 95 and 105 per cent band edges | the statute's own words; SF8, and no seed puts the golden within 1.91 bins of a boundary |
| 10 | Rounding path | once at the end or per line | SF7, the asking sentence rounds the valid total once and the line figures to the nearest 100 |
| 11 | Tie-break | none: one figure and three bands | no tie is reachable, recorded as such |
| 12 | Maturity and censoring | the unsampled sections are never keyed | the pack's own extent: no file holds a line outside the sampled sections, which is what fixes the duplicate class's inclusion probability |
| 13 | Order of operations | grounds applied in order, then expansion | SF6, the counties' verification instruction states the order; the expansion is per class after the partition |
| 14 | Row order | file order of the register | C1, every figure is a count or a sum; asserted invariant over row permutations |
| 15 | Duplicate resolution | which line of a pair stands | SF2, the statute's "not counted more than once"; the later line is struck |
| 16 | Identity normalisation | a signer across two extracts and fifteen registers | the state's own registration identifier carried on both extracts; no fuzzy matching anywhere, and no match key between two signature lines ships |
| 17 | Netting against gross | none: strikes do not offset | each line carries one disposition, asserted as a partition |
| 18 | Dimensional units | signatures, sheets and lines | the receipt log states lines per sheet; SF5 closes the only place the two could be confused |
| 19 | Code and status semantics | the disposition codes, including the pre-2024 merged code | the counties' own code crosswalk ships; SF4 closes the merged code by C1 so no reading of it moves a figure, and it is never the stump |
| 20 | Integerisation | signatures are whole | every projection is rounded as the asking sentence states; no remainder is allocated |
| 21 | Clause scope | the statute's sampling section applies to this filing | the section's own words; one measure, one filing, one sample |
| 22 | Forward window contents | what the full count would find | the committed quantity is the full count's own result, and the sample is the only evidence of it; no driver file is needed because nothing arrives after the sample |

## Literal reader

A reader who executes the shipped sentences word for word and infers nothing the files do not carry reaches the
golden. The statute files the filed total, the five per cent sample, the required number and the three bands;
the office receipt log files 540,000 lines on 36,000 sheets; the counties' registers file one disposition per
sampled line under a crosswalk that ships; and the pack holds no keyed line outside the sampled sections. A
literal reader therefore has exactly one basis on which a duplicate strike could have been found, both lines of
the signer drawn, and that fixes the expansion for that class and for no other class. Nothing in the pack
states the expansion, and nothing states a different one.

## Oracles

| control | what it confirms on the wrong path | verdict |
|---|---|---|
| the prior measure's close-out (`prior_period_close_out`) | nothing about any expansion basis | kept, re-specified at stage 2, see below |
| the office receipt log | sheets and lines received, and the 240 sheets struck at receipt | ties under every basis, reconciles SF5 |
| the two voter-file extracts | registrations and their run dates | ties under every basis; they carry no validity determination |
| the counties' registers | one disposition per sampled line | the evidence itself, not a control |
| the counties' reported sheet counts | the filed total before the receipt strike | ties under every basis, measured `same call` at SF5 |

**The calibration organ was re-specified at stage 2, and this is the one design change the measurement forced
beyond the figures.** The organ the draw implied, a prior measure projected from its own statutory sample and
then fully counted, is rejected in both of its only two directions. If the linear expansion reproduces that
measure's full count, the record blesses the naive method and is broken only by this petition's own duplicate
burden, which is the validated decoy the guard blocks and the "wrong now" violation of `stumping` Part 6. If it
fails to reproduce it, the record refutes the naive read, which is readability test 4 and makes the decisive
rung readable. There is no third position. **What ships instead:** the prior measure fell under the sampling
threshold and was verified by full count only, under the pre-2024 code set that folded duplicates into the
general class, so it carries the office's disposition vocabulary and realistic single-ground rates and carries
no projection, no expansion and no duplicate figure. It ties under every expansion basis because it contains no
expansion. `official_decoy` false, `validated_decoy` false, and no shipped artifact ranks the three statutory
dispositions.

## Ask sheet

Four asks, 91 separately gradable figures, 55 per cent of the rubric. Each is a component, qualifier or audit
trail of the call, each is multi-dimensional, and each carries its own silent device against the careful
solver's path. Unit and rounding sit inside the asking sentence.

| ask | the asking sentence's object | figures | weight | the silent device |
|---|---|---|---|---|
| A | each disposition the counties used, the sampled signatures and the projected statewide figure to the nearest 100 | 22 | 0.26 | the pre-2024 merged code has to be unfolded before any class is projected, and the grounds apply in order, so a sampled line sits in exactly one class |
| B | each county's sheets filed, sampled signatures and invalid rate other than duplication to one decimal | 45 | 0.28 | two counties filed their register twice and the correction supersedes row by row, so a wholesale replacement loses the rows the correction does not carry |
| C | each circulator firm's sheets filed, sampled signatures and invalid rate other than duplication to one decimal | 12 | 0.30 | 240 sheets were filed twice by two firms and struck at receipt, so a firm's sheets filed is the receipt log's count and not the counties' reported count |
| D | for each month of circulation, the sampled signatures and how many match a registration the later extract has cancelled, to the unit | 12 | 0.16 | the extract timestamps are UTC against local signing dates, so a month boundary moves 17 hours of signatures |

Cracker sheet: the careful solver that takes rung 1 on the call and each ask's easy route.

| ask | the cracker's route | the figures it would take | cracker |
|---|---|---|---|
| A | project every class at the sample's own factor without unfolding the merged code | the eight classes the fold does not touch | miss |
| B | replace each county's first register wholesale with its correction | the thirteen counties that filed once | miss |
| C | take each firm's sheets filed from the counties' reported counts | the two firms with no twice-filed sheets | miss |
| D | bucket signing dates on the extract's own timestamps | the four months with no boundary crossing | miss |

Pair ceiling: 50.5 (response 1 lands the call, 69.2; response 2 takes rung 1, 31.9; build target 60, bar 70).

Mirror leakage: 30.7 per cent of the ask weight, the share the best response off the call keeps, against a bar
of 50 and a target of two fifths.

Measured by: generator/cracker.py, section 4, run on the generator's clean truth.

**Two things this sheet owes, written as owed rather than claimed.** The per-ask shares are a declared model of
each device's reach, not a scored response, so they are re-measured against the cut pack at stage 3 and the
figures here are the design's targets. And **the binding risk is response 1 at 69.2**: the pair is 50.5 against
a build target of 60, but a single response that lands the call and keeps 0.367 of the ask weight sits 0.8
inside the bar on its own. Stage 3 holds the lander nearer a third of the ask weight, by hardening ask C's
device (the receipt strike has to be found in the receipt log rather than inferred from a round number) and
ask A's (the merged code's crosswalk ships as the county's own code list, not as a mapping table).

**One ask was folded at stage 2, for a reason worth keeping.** A separate reconciliation ask (the receipt log
against each county's reported sheet count) was folded into asks B and C, where the twice-filed sheets bite
directly. It was folded rather than deleted for two reasons: the prompt's 1,000 characters cannot carry five
multi-dimensional asks and a chart's named parts, and a separate reconciliation line would have been the fifth
place the receipt strike is named. The fold raised the figure count from 92 to 91 at four asks rather than
five, and moved the pair from 51.1 to 50.5.

## Convergence, against a rival's family

Computed on the clean truth by `generator/cracker.py`, seed 157, with the bucket each construction files. The
golden's own family is first and is **not** the evidence; the families a competent solver builds instead are.

| family | construction | valid | prints | band |
|---|---|---|---|---|
| own | the pair inclusion at the square of the sampling fraction | 388,460 | 390,000 | full count |
| own | the hypergeometric pair inclusion, five per cent times (n-1) over (N-1) | 388,459 | 390,000 | full count |
| own | the same estimator computed per county and summed | 388,460 | 390,000 | full count |
| own | the same estimator computed per circulator firm and summed | 388,460 | 390,000 | full count |
| own | two steps: the partner seen at the fraction, then expanded at the sample's factor | 388,460 | 390,000 | full count |
| **rival** | Chao1 unseen pairs off the sample's singletons and doubletons | -3,482,881 | -3,485,000 | insufficient, self-refuting |
| **rival** | a bootstrap over the sampled lines, 200 draws, mean | 388,536 | 390,000 | full count |
| **rival** | the linear expansion of every disposition class | 423,420 | 425,000 | sufficient |

**What this says and what it does not.** The golden's own family is unanimous to the unit, which is (b) equals
0.000 bins; that is the measurement architecture 1 mistook for determinism. The rival families are the point.
One of the two a competent solver reaches, the bootstrap, files the golden's own cell and call, so resampling
does not open a second answer. The other, the capture-recapture reflex, returns a negative valid total and
refutes itself on sight rather than standing as a competing defensible answer. The third rival, the linear
expansion, does file a different bucket: that is the stump, and it is wrong because the pack holds no keyed line
outside the sampled sections. Owed at stage 3: the same table on the cut pack, plus the two rival families run
over all six seeds rather than at the design seed alone.

## Bin measurements

Measured by `generator/cracker.py` on the clean truth over six seeds, bin 5,000 valid signatures (the asking
sentence's rounding). Two runs of the harness are byte-identical.

| seed | golden | rung 1 | (a) | (b) | (c) | band clear above | band clear below | cell edge | gap 0 to 1 | gap 1 to 2 | gap 2 to 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 157 | 388,460 | 423,420 | 6.99 | 0.000 | 1.59 | 3.14 | 4.56 | 960 | 1.60 | 2.66 | 4.33 |
| 158 | 383,260 | 426,200 | 8.59 | 0.000 | 1.75 | 4.18 | 3.52 | 760 | 1.60 | 3.27 | 5.32 |
| 159 | 378,080 | 424,060 | 9.20 | 0.000 | 1.80 | 5.22 | 2.48 | 580 | 1.60 | 3.50 | 5.70 |
| 160 | 383,060 | 425,620 | 8.51 | 0.000 | 1.74 | 4.22 | 3.48 | 560 | 1.60 | 3.27 | 5.24 |
| 161 | 382,340 | 426,420 | 8.82 | 0.000 | 1.77 | 4.37 | 3.33 | 160 | 1.60 | 3.34 | 5.47 |
| 162 | 375,220 | 421,960 | 9.35 | 0.000 | 1.82 | 5.79 | 1.91 | 2,280 | 1.60 | 3.57 | 5.78 |
| mean | 381,737 | 424,613 | 8.58 | 0.000 | 1.74 | 4.49 | 3.21 | | 1.60 | 3.27 | 5.31 |

**(a), two readings, both reported.** The decisive step's full worth, the distance from the route that takes
every other step right to the golden, is 6.99 to 9.35 bins, mean 8.58. Its worth at the last rung, the distance
from rung 2 to the golden, is 4.33 to 5.78 bins, mean 5.31. The conservative reading is the second, and it is
the one the law should be read against: **4.33 bins at worst against (b) plus (c) of at most 1.82, a factor of
2.4**, and the largest gap in the ladder at every seed.

**(b) equals 0.000 bins at every seed, and it is tested rather than asserted.** Five constructions of the
estimator, the squared fraction, the hypergeometric pair inclusion, the per-county grouping, the per-firm
grouping and the two-step reading, are unanimous to the unit, because the estimator is an observed count over a
constant the statute fixes: there is no fitted parameter, no window, no band width, no distribution family and
no grouping for a solver to choose. The hypergeometric construction differs from the squared fraction by one
signature. The one thing that could open this family is signers who signed three or more times, because the
all-doubles expansion then overstates: **measured at 117 signatures, 0.0233 bins**, with 150 triple signers
against 60,000 double signers. That bound is a construction constraint, not an observation: swept to a five per
cent triple share among multi-signers the all-doubles estimator is biased 0.59 bins and the multiplicity mix is
not identified from the sample at all, which would be a Gate B failure. The generator therefore draws
multiplicity near binary and asserts the bias under 0.05 bins.

**(c) is 1.59 to 1.82 bins, mean 1.74**, read under the refinement now filed in `determinism-check`: the
estimator has no free parameter, so every solver computing it files the same figure to the unit and the
interval is the quantity's honest uncertainty rather than a fork. (c) is also a world dial independent of (a),
which the duplicate burden sets.

**The one thin number, recorded as owed.** The band clearance below the golden falls to 1.91 bins at seed 162
against (c) of 1.82, because the duplicate burden is a draw and the golden drifts 375,220 to 388,460 across
seeds. Stage 3 therefore pins the campaign's own parameters rather than taking the burden from a free draw, to
targets asserted in the generator: the golden within 1,500 of a cell centre, both band clearances at or above
2.5 bins, and rung 2's figure at or above 500 from its own cell edge (it is 120 at seed 157). Seed 157 is the
best balanced of the six and meets two of the three.

## Pre-ship check

Owed at stage 5 for architecture 2.

## Tried and rejected

- The blind-reader evidence this screen first recorded as owed at stage 4 is withdrawn, not deferred.
  CLAUDE.md gained a STOP block on 2026-10-27 retiring the solver flow under every name (no scored reader, no
  cold or blind reader, no call-only or draw probe, no isolated thread that answers the task), leaving stump
  power to the paper argument and the portal. The nine-route sweep computed on the clean truth stands as that
  argument. The isolated leak reader and the determinism judge are unaffected and remain stage 4.

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

- **Stage 2 of architecture 2, 2026-10-27. Four things died or were re-specified under measurement, each with
  the number that killed it (`generator/cracker.py`, six seeds, byte-identical over two runs).**
  - **The draw's own figures.** 1,043,000 filed, a three per cent sample, a 623,212 threshold and 95 and 110
    per cent bands are California's statute on an Arizona card. Rebuilt on Arizona's: 540,000 lines, five per
    cent of the signatures filed, 384,924 required, bands at 95 and 105. The decisive step is unmoved and in
    fact only exact under the new world, because Arizona samples signature lines, so a pair's inclusion is the
    square of the fraction; a three per cent sample of whole sections would have made a same-section pair's
    inclusion the fraction itself and the registered driver wrong as written.
  - **The merged disposition code as neutral Layer 1: rejected.** At a 9.2 per cent share of the sampled
    duplicate strikes, unfolding it moved the golden 0.61 bins while four of six seeds sat 0.03 to 0.19 bins
    from a cell edge, so it was load-bearing on the graded figure and therefore a fork. Closed by C1 in the
    world (SF4): the old-code county's sampled lines carry no duplicate strike at all.
  - **The calibration organ as drawn: rejected in both of its only two directions.** A prior measure projected
    from its own sample and then fully counted either reproduces its full count under the linear expansion,
    which blesses the naive method and is the validated decoy the guard blocks, or fails to, which refutes the
    naive read and is readability test 4 on the decisive rung. Replaced by a prior measure that fell under the
    sampling threshold and was verified by full count only, carrying no projection and no duplicate figure.
  - **A world with a five per cent triple-signer share: rejected.** The all-doubles expansion is then biased
    0.59 bins and the multiplicity mix is not identified from the sample at all, which is a Gate B failure
    rather than a tuning problem. The world draws multiplicity near binary (150 triple signers against 60,000
    double signers) and the bias is measured at 117 signatures, 0.0233 bins, and asserted under 0.05.
  - **Chao1 on the sample's singletons and doubletons, screened as the rival a solver reaches for:** it returns
    minus 3,482,881 valid signatures, so it refutes itself rather than standing as a competing defensible
    answer, and it is recorded in `## Convergence` rather than used as a rung.

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

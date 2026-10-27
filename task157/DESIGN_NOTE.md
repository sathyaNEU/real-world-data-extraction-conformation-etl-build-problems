# task157 design note: the 2028 initiative petition signature projection (architecture 2)

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first, and
`## Architecture 1 is spent: the bin is finer than the estimator` below it: architecture 1 (the January
2027 winter guarantee qualifier forecast) shipped twice and was returned twice, and the cause was
measured rather than argued. Architecture 2 is drawn afresh in the same number, and every figure in the
live sections below is measured on the cut pack by `generator/cracker.py` and asserted in
`generator/checks.py`.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task157.json` (architecture 2, architecture 1 in `lineage` with
  its measured fate), registered 2026-10-27, re-checked against the restamped ban window: WARN only, no BLOCK,
  `validate` clean on 299 cards, `heart` WARN. Personas drawn with `guard.py names --geo "United States"
  --seed 157` and screened to zero `people.*` warnings: Philip James (State Elections Director), Laura Davis
  (the division's data unit), Tony Lynch (Navajo County Recorder).
- **Pairing:** `political-science-public-policy` / `election-polling-forecasting`, objective **Forecasting &
  Predictive Modeling**, prompt shape **03** (bridge between totals, one reconciling item per disposition
  class), decision type `quantity_figure`, answer unit a count of signatures.
- **Why the objective is Forecasting and not Descriptive.** The call is what a full count would find, which is
  an unobserved total rather than a future value, and Descriptive & Distribution Analysis was weighed for it.
  Forecasting is kept for two reasons: the objective is Forecasting **and Predictive Modeling**, and
  predicting the result of a full count from a probability sample is predictive modeling rather than a
  description of a population in hand; and the taxonomy maps `election-polling-forecasting` to F alone, so a
  Descriptive tag would need a task type (`small-area-public-opinion-estimation-mrp`,
  `legislative-behavior-ideal-point-estimation`) that does not hold this quantity. The tag is the weakest axis
  of this draw and is recorded as such.
- **Niche:** a state elections division projecting, from the statutory five per cent random sample of a filed
  initiative petition, how many of its 540,000 signature lines a full count would find valid, when the sample
  is the only part of the petition that is ever keyed.
- **As-of:** **4 August 2028**, the Friday the division pulls every file and the projection is due. The
  petition was filed 6 July 2028, the sample drawn 11 July, the recorders' returns closed 2 August and the
  division's consolidation check 3 August. The certification deadline for the 7 November 2028 ballot is
  8 September 2028, so the window the call is about has not closed.
- **The world's figures are Arizona's own statute, and this is the correction the author has to read first.**
  The draw's candidate magnitudes (1,043,000 signatures filed, a three per cent sample, a 623,212 threshold
  and 95 and 110 per cent bands) are California's statute, attached to an Arizona card. Arizona samples
  **five per cent of the signatures filed** and sets the bands at **95 and 105 per cent** of the required
  number. The world is therefore built on Arizona's: 44,120 receipted sheets carrying **540,000 signature
  lines**, a **27,000** line sample, a required number of **384,924** (fifteen per cent of the 2,566,154 votes
  cast for Governor in 2026), and bands at **365,678** and **404,170**. Nothing about the decisive step moves:
  the sample is of signature lines, so a pair's inclusion probability is the square of the sampling fraction
  exactly, which is the registered driver and which the three per cent reading would not have been, because a
  sample drawn by whole sections makes a same-section pair's inclusion the fraction itself.
- **What the card still owes.** Its `answer`, `niche` and `spine.rows` are the author's to bring to the
  figures below, and three strings the cut pack introduces are the author's to add to `world.people` so
  `guard.py surface` stops reading them as personas: **Santa Cruz** (one of Arizona's fifteen counties, which
  `surface` BLOCKs against task243's persona of that name), **Arizona Secretary** (the office) and the firm
  names. Santa Cruz is a real county on a real statutory list of fifteen and cannot be renamed.
- **Strategy:** gap `population` and `rule`, generators `G10` and `G2`, Gate G `forecasting`, strategy
  `other`, Layer 2 family `field_method`, pattern
  `own:pairwise-defect-inclusion-is-the-square-of-the-sampling-fraction`, calibration
  `prior_period_close_out`, context artifact `register`, `stump_class: analytical`, no official decoy, no
  validated decoy, decisive rule not filed.
- **Data-native sentence.** Only the sampled lines of this petition are ever keyed, which is how a
  random-sample check of a petition actually works, so a duplicate signature exists in the record only where
  the sample happened to draw both lines of one signer; every other ground of invalidity is a property of the
  one signature in front of the recorder, and that difference in what the sample can see is a property of
  this pack's own generating process rather than of any rule in it.
- **Sources, one line each.** `guard.py mechanisms` was read on `forecasting` (90 builds) and
  `opportunity-sizing-decision` (14) before drawing. Almost every forecasting driver on file is a behavioural
  rate measured on one population and carried to another, which is the family the bin law kills and why
  architecture 1's shape is not repairable by changing its world. task264 v2 is the nearest insight at 0.06,
  an inclusion probability the record's own design sets, and the differentiation is in the card. task190's
  architecture 3 is the measured death in this genus and is answered under `## Readability screen`. Nearest
  driver on file is 0.09 (task445 v1).
- **Fiction.** Arizona, a state elections division, forum `regulator_or_inspector`, forcing event
  `vote_or_meeting`, org family `government_agency`.
- **Deliverables:** `signature_projection_2028.xlsx` and `petition_disposition_2028.png`.
- **Spine:** `county_verification_returns_2028.csv`, one row per sampled signature line and the disposition
  its recorder or the division gave it, **27,000 rows**, grain sampled signature line by county by sheet.
  Beside it the office's own sheet register, `petition_sheet_index_2028.csv`, 44,120 rows.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain.

1. Reconcile the fifteen recorders' returns to the office's own record of the sample: 27,000 lines, one
   disposition each.
2. Put Navajo County's returns on the current code set from that recorder's own 2019 list, splitting its
   merged code 02 by the registration the recorder matched, and apply the division's query notices, which
   supersede the disposition first returned for the line they name.
3. Re-derive the registration grounds from the statewide snapshot current when circulation opened, because
   the statute asks for registration at the time of signing; that snapshot still shows 364 sampled signers
   as active who were cancelled in the list-maintenance run of 14 March 2028 and signed afterwards, so those
   364 are not struck.
4. Count the dispositions in the sample: 5,913 invalid on single-signature grounds and 61 struck as
   duplicates, of 27,000 sampled lines.
5. Expand every class at the sample's own factor of twenty: single grounds 118,260, duplicates 61 times
   twenty, 1,220.
6. Valid equals 540,000 less 118,260 less 1,220.

Ends on: **420,520** valid signatures, which prints **420,000** to the nearest 5,000 and stands at 109.2 per
cent of the required 384,924, above the statute's 105 per cent line, so the petition is sufficient and goes on
the ballot.

Golden: **390,060** valid signatures, which prints **390,000**, 101.3 per cent of the required number and
inside the 95 to 105 per cent band, so the examination of all 540,000 signature lines is ordered. The
duplicate burden is 61 over one four-hundredth, **24,400**, and the single-ground burden is the recorders'
6,277 strikes expanded at twenty, **125,540**.

The two graded figures are 6.09 bins of 5,000 apart and the statutory calls differ, which is the separation
architecture 1 never had: there the two figures were four bins apart and the decisive step was worth 0.58 of
one. Every figure here is measured on the cut pack by `generator/cracker.py` and asserted in
`generator/checks.py`.

## Stump sentence

A competent solver who reads every disposition code, puts Navajo County's own codes on the current set,
applies the division's query notices, validates the recorders' registration determinations against the
snapshot whose run date precedes the signing window and expands every class at the sample's own factor of
twenty files 420,520 valid signatures and a sufficient petition that goes on the ballot; the step that lands
them there is expanding the duplicate dispositions at the sampling fraction alongside the single-signature
grounds, when a duplicate is a relation between two signature lines that the sample sees only where it draws
both, so the duplicate burden is 24,400 rather than 1,220 and the projection is 390,060, which orders the
examination of all 540,000 lines filed.

## Three rules

Task type: election-polling-forecasting: projecting a filed petition's valid signature total from the
statutory random sample, a task type the taxonomy maps to Forecasting & Predictive Modeling.

Domain test: the deciding quantity is the number of valid signatures a full count would return, estimated the
way election administration estimates it, by design-based expansion of a probability sample in which each
ground of invalidity carries its own inclusion probability; put another field's nouns in and the quantity
disappears, because the estimator exists only where a statute fixes a sampling fraction and a threshold and
where one ground of invalidity is a relation between two records rather than a property of one.

Swap: "projecting from the statutory five per cent random sample, how many of the 540,000 signature lines
filed would a full count find valid, and does the petition qualify, go to a full count or fail" becomes "how
many of 540,000 hospital admissions would a full count find valid", and it reads as one multiplication: an
admission has no second member that must fall in the same sample for its defect to be visible, so the whole
decisive step has nothing to attach to.

Layer 1: Navajo County's recorder still files on its own 2019 disposition code list, whose code 02 covers two
grounds the current set keeps apart; Mohave County's return writes signature dates day first and Navajo's
writes them in its system's own month-abbreviated form; the division's query notices supersede single
determinations line by line after the returns closed; sheet numbers are each firm's own series, so a sheet is
identified by its circulator's registration number with its number; 182 sampled lines were determined by the
division rather than by a recorder; 240 sheets two firms had already filed were struck at receipt and sit in
their own manifests but not in the office's sheet register; one firm changed its trading name in April and
kept its registration number, so one number carries two trading names; twenty-two circulators left one firm
for another inside the window and carry two registration rows handed over on one day; registrations cancelled
and restored carry a cancellation date against an
active registration; lines struck for a missing or out-of-window date carry no usable date; the returns carry
UTC load stamps against local signing dates; two files are written with CRLF line endings. Each is written by
the system that produces it, none is placed to be caught, and each is asserted neutral on the call in
`checks.py` under R2. **The two statewide snapshots either side of the March list-maintenance run are not in
this list**: they are rung 0's own lever and belong to the ladder, not to neutral mess.

Layer 2: field method (design-based estimation): the call flips on recognising that one disposition class's
inclusion probability is the square of the sampling fraction rather than the fraction.

Decisive step: expanding the duplicate dispositions at the pair's inclusion probability, the square of the
sampling fraction, rather than at the fraction every single-signature ground expands at; in election
administration's own words, reading the design's inclusion probability for a ground that is a relation
between two signature lines.

Not semantics: every disposition code, both snapshot vintages, the threshold and the sampling fraction read
perfectly still leave the easy route expanding one class at the wrong power of the fraction, because no
field, code, unit or definition in the pack carries an inclusion probability; the fraction is stated once, in
the office's own record of the sample, and it is the right number for every other class.

Not rule application: the filing record files the sample size, the number required and the three statutory
outcomes, and no shipped sentence states how a class expands. Executing every filed rule with the statutory
fraction applied to all classes files the sufficient determination, so the step no rule performs is reading
the design.

Analyst test: a strong analyst who reads every disposition code correctly, puts Navajo's own codes on the
current set, applies the query notices, validates the recorders' determinations against the snapshot that
precedes the signing window and applies the required number expands every class at the sample's own factor
and files **420,520 valid signatures, which prints 420,000 to the nearest 5,000 and stands at 109.2 per cent
of the required 384,924, above the statute's 105 per cent line, so the petition is sufficient**. Executed in
`checks.py` under R3a, on the bundle and again on the generator's clean truth.

Estimand: filed at authority in the office's own filing and selection record: the number of signatures a full
count of the filed petition would find valid, where the filed total (540,000 lines on the 44,120 sheets
receipted), the sampling fraction (five per cent of the signature lines filed) and the number required
(384,924) are the statute's own, and the sample is the 27,000 lines the recorders verified. It fixes the
population, the window, the unit and the comparison, and says nothing about how any disposition class
expands.

No decoy: nothing is planted to be caught. Duplicate signatures are authentic, because people sign twice at
different events; no memo, briefing or draft argues for an expansion basis; no shipped file states a valid
total or ranks the three statutory outcomes.

No certified replay: the 2024 full count's close-out is the calibration organ and carries no projection, no
expansion and no duplicate figure at all, because that petition was never sampled: a court ordered every
signature examined. It therefore ties under every expansion basis, and `checks.py` asserts that its header
carries no projection, expansion, duplicate or sample row.

Lesson: a defect that is a relation between two records enters a probability sample only when both members
do, so its design weight is not the sample's weight; no build on file teaches an inclusion probability that
differs by class within one design (task264 carries a per-respondent design weight whose probability rises
with multiplicity, which attaches to a unit and is linear in the fraction).

## Readability screen

Measured, not argued: `generator/cracker.py` enumerates the reflex row from election administration's and
sampling's own vocabulary for a sample projection and computes every route **on the cut pack**. Ten routes
were run. **Every route that expands the duplicate class at the sampling fraction files `sufficient`**: the
linear family lands 4.39 to 6.09 bins away, the counted-line base 4.56 and the either-line correction 4.75,
and the capture-recapture reflex self-destructs at minus 5,507,072 valid signatures. The only two routes that
reach the statutory band both apply the pair's own inclusion probability, and the one that also re-derives
registration from the July snapshot prints two cells below the golden. So the duplicate class being visible
in the sample takes a solver to rung 1, and rung 1 is 4.64 bins wrong in the band that certifies the
petition.

| rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | 7 organ | verdict |
|---|---|---|---|---|---|---|---|---|
| 0 registration re-derived off the December 2027 snapshot, every class at the sample's factor (420,520) | each snapshot carries its own date | two snapshots in the pack | yes, the opponent validates the recorders' work | none | the battery finds the date overlap | yes, one join | no organ | readable |
| 1 the recorders' dispositions as filed, every class at the sample's factor (413,240) | the record names the sample and the number required | the disposition column | yes, the opponent's default projection | none | no | yes, one ratio | no organ | readable |
| 2 pair inclusion on the division's own strikes only, the recorders' strikes at the sample's factor (404,880) | no | the returns name who determined each line | partly, a solver that senses the pair problem | none | no | no | no organ | readable |
| 3 (decisive) every duplicate strike at the pair's own inclusion probability (390,060) | no shipped sentence names a pair, an inclusion probability, a squared fraction or a count of signers | no column pairs two lines except the registration identifier the recorder matched, which is also what the recorder found the duplicate with | no: the nine enumerated routes beside the golden land 2.02 to 6.09 bins from it, measured on the cut pack | no control scores the expansion bases | the battery reaches the snapshots and the merged code, not the expansion | no: it is a different power of a number the record states once, and every route that takes the obvious ratios is measured wrong | every file is one the office keeps for its own reasons and the pack ships no reliability factor, manual or allowance | silent |

**Test 1 and this draw's exposure, answered.** The duplicate class is unavoidable and has to be, or there is
no decisive step and Gate B fails. What test 1 asks is whether a clause names the decisive quantity, and the
decisive quantity is the duplicate burden in the whole petition, which no clause names: the record names the
sampling fraction once, and that fraction is the right number for every other class. The sweep is the
evidence and it is the honest kind: a route that meets the class and asks how to expand it lands on rung 1.
The limit of the measurement is stated plainly: it scores the routes enumerated here, computed as code on the
shipped bundle, and nothing beyond it is owed. CLAUDE.md's STOP block of 2026-10-27 retires the solver flow
outright, so there is no scored or blind reader at stage 4 or anywhere else; stump power is argued on paper
here and measured by the portal alone. The ten-route sweep IS the paper argument, and the only readers that
still run are the isolated leak reader, which reads the pack for leaks and never solves it, and the
determinism judge.

**task190's architecture 3, asserted rather than argued.** That build died because Gate B forced its audit
manual and reliability factor table into the pack and shipping them handed the route back. Here nothing has
to ship to make the projection computable: the filed total, the sampling fraction and the number required are
the statute's, and the decisive move is one division. Two constraints are therefore load-bearing and are
asserted in `checks.py`. **No keyed signature line outside the sample ships**, because only the sampled lines
are ever keyed, and the pack's own extent carries that fact (the returns are the only file at the signature
line's grain, asserted on the shipped columns) rather than any sentence stating it. And **no reliability
factor, projection manual, settlement allowance or duplicate allowance ships in any form**, asserted by a
sweep over every shipped document for the words expand, project, multiply, factor and inclusion probability.

## Semantic fork table

Every row closed by a quotable shipped sentence, by C1 convergence, or marked `same call` with the measured
distance. Every id is asserted in `generator/checks.py`, and every document assertion there reads the text
with its line breaks collapsed, because a closure sentence hard-wrapped mid-phrase is present in the record
and unreachable by a line-oriented search, which is how one of this build's own determinism findings
happened.

| id | the term or convention | the readings | ruled out by |
|---|---|---|---|
| SF1 | what the five per cent is five per cent of | the signature lines filed, or the sheets filed | the filing record: "a random sample of five per cent of the signature lines filed, 27,000 of the 540,000 lines receipted"; and the shipped sample is 27,000 signature lines rather than 2,206 sheets, so the sheets reading is refuted by the pack's own extent |
| SF2 | a duplicate pair is one invalid signature or two | strike the later line, or strike both | the verification instruction: "A signature shall not be counted more than once. Where an elector's signature appears on more than one of the lines before you, count the earliest by the date signed and give each later line code DU"; measured, the both-lines reading files 412,020, a named wrong cell 4.39 bins away, and `sufficient` |
| SF3 | which registration record places a sampled signature | the recorders' own determinations, or the snapshot current when circulation opened | the instruction: verify "against your county's registration records as they stood on the date written on the line"; C4, the December 2027 reading is rung 0, measured 1.46 bins from rung 1 and filing `sufficient` |
| SF4 | Navajo County's merged code 02 | folded into one ground, or split between not registered and registration cancelled | both readings are single-signature grounds that carry at the same factor, so no reading of the fold moves any projected class total or the call; asserted equal to the signature on the cut pack, and the split itself is forced by the registration the recorder matched, asserted row by row |
| SF5 | the filed total | the 540,000 lines the office receipted, or the 542,931 the firms' own manifests claim | the filing record: "240 of those sheets were sheets already filed with this office under the same serial number and were struck at receipt; they are not part of the filing"; measured, the manifest reading projects 392,044, which prints the golden's own cell and files the same band |
| SF6 | the order the grounds are applied in | the instruction's order, or any other | the instruction: "Work down the table and record the first code that applies", and a sampled line carries exactly one disposition, asserted as a partition of the 27,000 lines |
| SF7 | the rounding path | once on the projected valid total, or per disposition class then summed | the asking sentence rounds the projection to the nearest 5,000 and every other figure as a whole number; C1, both classes project to whole numbers of lines, so summing the classes and rounding the total once give the identical 390,060, asserted |
| SF8 | the band the projection falls in | at or above 105 per cent, or above it | the filing record's own words, "more than one hundred and five per cent" and "less than ninety-five per cent", both strict; C1, the projection sits 2.82 bins inside the band at the shipped seed and no seed puts it within 2.82 bins of a boundary |

## Ladder

Four rungs, each a defensible analysis climbed by refusing it, measured by `generator/cracker.py` on the cut
pack and on the clean truth over six seeds (157 to 162). Figures are the shipped pack's; the per-seed table is
in `## Bin measurements`.

| rung | the analysis | valid | printed | band | gap to the next rung | dies to |
|---|---|---|---|---|---|---|
| 0 | registration re-derived off the snapshot current when circulation opened, every disposition class expanded at the sample's own factor | 420,520 | 420,000 | sufficient | 1.46 bins | each snapshot's own run date against the signing dates, and the list-maintenance run of 14 March inside the circulation window |
| 1 | the recorders' own determinations taken as the instruction assigns them, every class still expanded at the sample's factor | 413,240 | 415,000 | sufficient | 1.67 bins | the returns are the only file at the signature line's grain, so a duplicate exists in the record only where both of a signer's lines were drawn |
| 2 | the pair inclusion applied to the division's own strikes only, on the view that a recorder checked its whole county's share of the petition | 404,880 | 405,000 | sufficient | **2.96 bins** | the same shipped fact: no recorder was sent a line outside the sample, so no full-batch check was possible |
| 3 (decisive) | every duplicate strike at the pair's own inclusion probability, the square of the sampling fraction | 390,060 | 390,000 | **full count** | | |

**Worth.** Computed on the graded quantity, never an intermediate. Gaps over the six seeds: rung 0 to 1 runs
1.37 to 1.49 bins (mean 1.44), rung 1 to 2 runs 1.22 to 1.98 (mean 1.58), rung 2 to 3 runs 2.58 to 3.80 (mean
3.07). **The decisive gap is the largest at every one of the six seeds**, and its worst value, 2.58 bins, is
1.80 times the largest measured sum of (b) and (c). Architecture 1's decisive gap was 0.58 of a bin and the
smallest in its ladder; this is the number that changed.

**Position and dominance, measured and not rounded up.** The decision is a figure and a statutory band. On the
figure, every rung prints its own cell and the nearest rung is three cells from the golden, so no rung files
the golden's figure at any seed. On the band, all three rungs file `sufficient` at the shipped seed and rungs
0 and 1 file `sufficient` at every one of the six seeds; **rung 2 files `sufficient` at the shipped seed with
710 signatures to spare and falls inside the band at the other five seeds**, which is the one position claim
this architecture cannot make at every seed, because the golden has to sit 2.5 bins clear of both boundaries
and rung 2 is only 2.96 bins above it. It costs nothing on the figure (rung 2 prints 405,000, three cells
out) and it is recorded here rather than smoothed. Dominance: the golden's distance to the nearest band
boundary is 2.82 bins at the shipped seed (3.50 mean above, 4.20 mean below), against (b) plus (c) of at most
1.43 bins.

**The grid.** Every cell a partial application reaches is a named wrong answer: the December snapshot alone
(420,000), the recorders' dispositions alone (415,000), both lines of a pair struck (410,000), the
counted-line base (415,000), the either-line correction (415,000), the division-strikes-only split (405,000),
and the capture-recapture reflex (a negative total that refutes itself). Single-error cells all file feasible
figures in the `sufficient` band; none files the golden's cell.

**Margins.** No gap under 1.15 times the printed cell at any seed: the smallest measured, 1.22 bins, is 1.22
times it. Each rung's printed figure sits in its own cell at the shipped seed, with measured cell-edge
distances of 1,980 for rung 0, 740 for rung 1, 2,380 for rung 2 and 2,440 for the golden. The author's stage 3
targets were the golden within 1,500 of its cell's centre (measured **60**) and every rung at least 500 from
its own edge (measured, worst 740, rung 1); the note's earlier wish for 1,500 on rung 1 is not reachable
without moving the golden off its centre, because rung 1 is the golden plus 380 times the duplicate count and
both cannot be centred at once.

## Closure table

The 22 axes of `determinism-check` section 3, each with the reading it admits and the move that closes it.

| axis | the axis | the reading here | closure |
|---|---|---|---|
| 1 | Population | the signature lines filed for this petition | the filing record files the filed total and the sample; the receipt log is the record of filing; C4 with SF5 |
| 2 | Unit of account | the signature line, not the sheet or the signer | the asking sentence counts signature lines; SF1 closes the fraction's base and the shipped sample settles it |
| 3 | Attribution window | which month a signature was signed in | the signing date written on the line; the circulation window runs from the serial's issue to the filing |
| 4 | As-of dating | registration status as at signing | the instruction's "as they stood on the date written on the line"; SF3, each snapshot carries its own date |
| 5 | Version basis | the disposition as first returned or as corrected | the query notices carry the prior and the corrected code and their own date, and supersede the named line only; asserted applied row by row |
| 6 | Denominator | the sampled lines, per county and per class | the filing record states the sampled count; every rate is over the sampled lines of its own cell |
| 7 | Weighting | pooled or per county | C1, the estimator is a count over a constant the statute fixes, so every grouping gives the identical total; measured at (b) of 0.86 signatures on the cut pack and under 0.0003 bins at every seed |
| 8 | Window length | none: no rate is measured over a look-back | not applicable today, recorded as such |
| 9 | Boundary inclusivity | the 95 and 105 per cent band edges | the filing record's own strict words; SF8, and no seed puts the golden within 2.82 bins of a boundary |
| 10 | Rounding path | once at the end or per class | SF7, the asking sentence rounds the projection once and every other figure as a whole number; both paths measured identical |
| 11 | Tie-break | none: one figure and three bands | no tie is reachable, recorded as such |
| 12 | Maturity and censoring | the unsampled lines are never keyed | the pack's own extent: the returns are the only file carrying a line number, asserted on the shipped columns, which is what fixes the duplicate class's inclusion probability |
| 13 | Order of operations | grounds applied in order, then expansion | SF6, the instruction states the order; the expansion is per class after the partition |
| 14 | Row order | file order of the returns | C1, every figure is a count or a sum; asserted invariant under row reversal |
| 15 | Duplicate resolution | which line of a pair stands | SF2, the instruction's "count the earliest by the date signed"; the later line is struck |
| 16 | Identity normalisation | a signer across two snapshots and fifteen returns | the state's own registration identifier, carried on the returns and on both snapshots and nowhere else, which is also the key the recorder matched a line to and therefore the only thing that pairs two sampled lines; no fuzzy matching anywhere, and no key pairs a sampled line with an unsampled one because no unsampled line is keyed in any file |
| 17 | Netting against gross | none: strikes do not offset | each line carries one disposition, asserted as a partition |
| 18 | Dimensional units | signatures, sheets and lines | the sheet register carries the lines each sheet bears and they sum to the filed total, asserted; SF5 closes the only place the two could be confused |
| 19 | Code and status semantics | the disposition codes, including Navajo's merged code | the recorders' current code table ships in the instruction and Navajo's own 2019 list ships as that recorder's list; SF4 closes the merged code because both of its grounds carry at the same factor, so no reading of it moves a figure, and it is never the stump |
| 20 | Integerisation | signatures are whole | both class burdens are whole numbers by construction, asserted; the projection is rounded as the asking sentence states |
| 21 | Clause scope | the filing record applies to this serial | the record names serial I-18-2028 throughout; one petition, one filing, one sample |
| 22 | Forward window contents | what the full count would find | the committed quantity is the full count's own result, and the sample is the only evidence of it; no driver file is needed because nothing arrives after the sample |

## Literal reader

A reader who executes the shipped sentences word for word and infers nothing the files do not carry reaches
the golden. The filing record files the filed total, the five per cent sample, the number required and the
three outcomes; it files 540,000 lines on the 44,120 sheets receipted and the 240 sheets struck at receipt as
outside the filing; the recorders' returns file one disposition per sampled line under a code table that
ships; and no file in the pack carries a signature line outside the sample. A literal reader therefore has
exactly one basis on which a duplicate strike could have been found, both lines of the signer drawn, and that
fixes the expansion for that class and for no other class. Nothing in the pack states the expansion, and
nothing states a different one.

## Oracles

| control | what it confirms on the wrong path | verdict |
|---|---|---|
| the 2024 full count's close-out (`prior_period_close_out`) | nothing about any expansion basis: that petition was never sampled | kept, and it is the only settled measure the office holds of what examining a petition line by line takes, which is what makes the band's own remedy actionable |
| the office's receipt log | bundles received, sheets accepted and the 240 struck at receipt | ties under every basis, reconciles SF5 |
| the two statewide snapshots | registrations and their own run dates | they carry no validity determination; they are rung 0's lever, not a control |
| the recorders' returns | one disposition per sampled line | the evidence itself, not a control |
| the firms' own delivery manifests | the sheets and lines each firm handed over | ties under every basis, measured one cell and the same band at SF5 |
| the circulator registration extract | which firm had a circulator registered on a date | ask B's own path; it carries no validity determination and no figure the call reads |

**The calibration organ was re-specified at stage 2, and this is the one design change the measurement
forced beyond the figures.** The organ the draw implied, a prior petition projected from its own statutory
sample and then fully counted, is rejected in both of its only two directions. If the linear expansion
reproduces that petition's full count, the record blesses the naive method and is broken only by this
petition's own duplicate burden, which is the validated decoy the guard blocks and the "wrong now" violation
of `stumping` Part 6. If it fails to reproduce it, the record refutes the naive read, which is readability
test 4 and makes the decisive rung readable. There is no third position. **What ships instead:** the 2024
petition was never sampled at all, because a court ordered the examination of every signature in a challenge,
so its close-out carries the office's own examination rate, its county figures and its determination, and no
projection, expansion or duplicate figure. It ties under every expansion basis because it contains no
expansion. `official_decoy` false, `validated_decoy` false, and no shipped artifact ranks the three statutory
outcomes.

## Ask sheet

Three asks, 75 separately gradable figures, 55 per cent of the rubric. Each is a component, qualifier or audit
trail of the call, each is multi-dimensional, and each carries its own **primary** device, which is a
reconstruction over dated records that no shipped sentence states and no sweep of the hygiene battery
performs. Unit and rounding sit inside the asking sentence: every figure is a whole number.

| ask | the asking sentence's object | figures | primary device | shared hazards |
|---|---|---|---|---|
| A | each of the fifteen counties: how many of the sampled signatures its recorder determined carry a registration in force on the day signed and cancelled in the 10 July 2028 snapshot | 15 | **the registration state at the day signed**, rebuilt from the registration date and the cancellation date the July snapshot carries, so a registration re-established after a cancellation stands, one cancelled after the signature was given stands too, and the status column rather than the presence of a cancellation date decides what is lost now | the 182 lines the division determined rather than a recorder; the day-first signature dates |
| B | each of the four circulator firms and each month from January to June 2028: the sampled signatures gathered by circulators that firm had registered on the day the signature was given, and how many were struck on a ground other than duplication | 48 | **the firm as at the day signed**, rebuilt from the circulator registration extract, where twenty-two circulators registered again under another firm inside the window and a registration number therefore carries two rows with their own dates | the day-first signature dates; the firm that changed its trading name on one registration number; the firms' manifests, which count what they delivered rather than what was sampled |
| C | each of those months: the signatures signed in it, and how many carry such a registration | 12 | **the day-first signature dates**, which Mohave County's return writes as the recorder's system does, so a month-first parse silently moves signatures across every month boundary | the registration state at the day signed again, which the second figure shares with ask A, so a response that reconstructs neither loses both figures of every month |

**The two ask-side forks the stage 4 judge raised are closed by the filing record's own sentences**, which is
the sanctioned device on this side of the build: rule 3 binds the main call's decisive step and the asks are
free of it, so an ask may turn on a filed rule. The record's `Circulator registrations` section states that a
circulator who moves firm is withdrawn as of the day the new registration takes effect and that sheets
gathered on that day are gathered under the new registration, which fixes the 17 sampled lines signed on a
handover day; and that a firm which changes its trading name keeps its registration number, which fixes the
five trading names over four registration numbers at four firms and matches the asking sentence's "four
circulator firms". Both are asserted in `checks.py` against the extract's own rows rather than against a
sentence alone, and the extract hands every mover over on one day with no gap and no overlap.

**The cracker sheet**, measured by code on the cut pack. The cracker lands the call, runs the hygiene battery
(key uniqueness, exact duplicates, unmatched joins, fan-out, count ties), executes every filed rule it points
at and applies every handling a shipped document states, so it has Navajo's code list, the query notices, the
sheet key and the division's own determinations, and it meets the three primaries with nothing to read.

| ask | the cracker's route | figures it keeps of its own ask | cracker |
|---|---|---|---|
| A | the recorder column taken as filed and a registration counted lost wherever the snapshot's status says cancelled | 1 of 15 | miss |
| B | the firm taken from the circulator's current registration row | 2 of 48 | miss |
| C | every slash-separated signature date read month first | 0 of 12 | miss |

**Both numbers, labelled, because the gate carries the worse one.**

| reading | what the response that lands the call also does | its ask keep | response 1 | response 2 | pair |
|---|---|---|---|---|---|
| the cracker's own keep | nothing beyond the battery and the filed rules | 3 of 75, 0.040 | 47.2 | 14.2 | 30.7 |
| **the worst honest reading, and the gated figure** | also solves whichever single primary is worth most, the registration state at the day signed | 18 of 75, 0.240 | **58.2** | 14.2 | 36.2 |

Pair ceiling: 36.2

Pair ceiling on the cracker's own keep for both responses: 30.7

The worse figure is in the gated field on purpose, because a green gate bought with the favourable of two
numbers is the defect the gate exists to catch. **The single-response figure the coordinator asked about is
58.2, under 60, and it got there without touching the main call**: what moved it was cutting ask A's count of
each recorder's own determinations, 15 figures the cracker kept 15 of, because the verification instruction
tells a reader how to filter them. Cutting them took the cracker's keep from 0.178 of the ask weight to
0.040 and the worst single response from 66.4 to 58.2. Ask A keeps a population only inside its own asking
sentence, where it is not separately graded.

Easy route, which also takes the documented handlings wrong: 3 of 75. Each of the three primaries is
load-bearing and `checks.py` asserts it: a response that solves the other two without it still misses, at 16,
29 and 55 of 75, and no single primary solved alone reaches a third of the ask weight (0.120, 0.013, 0.240).

Mirror leakage: 4.0 per cent of the ask weight, the share the best response off the call keeps, against a bar
of 50 and a target of two fifths.

Measured by: generator/cracker.py, section 4, run on the cut pack.

**What was cut, and the measurement that cut it.** The ask sheet carried a fourth ask, the sampled signatures
and sheet serials of each of the eleven disposition codes, 22 figures, and the cracker kept 22 of 22: Navajo's
code list, the query notices and the sheet key are all documented or battery-visible, so nothing on that ask's
path cost a careful response anything. It was cut at stage 3 and the conformation work it asked for is still
in the pack and still on the call's own path, where `checks.py` asserts it neutral. Ask A's determination
count went the same way at this pass and for the same reason, measured rather than argued.
## Convergence, on the cut pack and against a rival's family

Computed by `generator/cracker.py` on the shipped bundle, with the bucket each construction files. The
golden's own family is first and is **not** the evidence; the families a competent solver builds instead are.

| family | construction | valid | prints | band |
|---|---|---|---|---|
| own | the pair inclusion at the square of the sampling fraction | 390,060 | 390,000 | full count |
| own | the hypergeometric pair inclusion, p times (n-1)/(N-1) | 390,059 | 390,000 | full count |
| own | the same estimator computed per county and summed | 390,060 | 390,000 | full count |
| own | the same estimator computed per return batch and summed | 390,060 | 390,000 | full count |
| own | two steps: the partner seen at the fraction, then expanded at the sample's factor | 390,060 | 390,000 | full count |
| **rival** | Chao1 unseen pairs off the sample's singletons and doubletons | -5,507,072 | -5,505,000 | insufficient, self-refuting |
| **rival** | a bootstrap over the sampled lines, 200 draws, mean | 389,930 | 390,000 | full count |
| **rival** | the linear expansion of every disposition class | 413,240 | 415,000 | sufficient |

**The same table at every one of the six seeds**, on the generator's clean truth, asserted in `checks.py`:
the own family's spread is 0.73 to 1.00 signatures, the bootstrap files the golden's band at all six seeds
and the linear expansion files `sufficient` at all six.

**What this says and what it does not.** The golden's own family is unanimous to the unit, which is (b) of
0.86 signatures or 0.0002 bins; that is the measurement architecture 1 mistook for determinism. The rival
families are the point. One of the two a competent solver reaches, the bootstrap, files the golden's own cell
and call, so resampling does not open a second answer. The other, the capture-recapture reflex, returns a
negative valid total and refutes itself on sight rather than standing as a competing defensible answer. The
third rival, the linear expansion, does file a different bucket: that is the stump, and it is wrong because no
file in the pack carries a signature line outside the sample.

## Bin measurements

Measured by `generator/cracker.py`, bin 5,000 valid signatures (the asking sentence's rounding). Seed 157 is
the shipped pack; 158 to 162 are the same world drawn again, and every row is the generator's clean truth.
Two runs of the harness are byte-identical.

| seed | golden | rung 1 | (a) last | (b) | (c) | band clear above | band clear below | cell centre | gap 0 to 1 | gap 1 to 2 | gap 2 to 3 | all-doubles bias |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 157 | 390,060 | 413,240 | 2.96 | 0.0002 | 1.34 | 2.82 | 4.88 | 60 | 1.46 | 1.67 | 2.96 | 118 |
| 158 | 383,540 | 408,620 | 3.80 | 0.0002 | 1.39 | 4.13 | 3.57 | 1,460 | 1.41 | 1.22 | 3.80 | 106 |
| 159 | 388,240 | 409,140 | 2.58 | 0.0002 | 1.29 | 3.19 | 4.51 | 1,760 | 1.37 | 1.60 | 2.58 | 108 |
| 160 | 389,740 | 409,500 | 2.58 | 0.0001 | 1.26 | 2.89 | 4.81 | 260 | 1.49 | 1.37 | 2.58 | 108 |
| 161 | 381,840 | 408,820 | 3.72 | 0.0002 | 1.43 | 4.47 | 3.23 | 1,840 | 1.49 | 1.67 | 3.72 | 114 |
| 162 | 386,600 | 410,160 | 2.74 | 0.0002 | 1.35 | 3.51 | 4.18 | 1,600 | 1.41 | 1.98 | 2.74 | 106 |
| mean | 386,670 | 409,913 | 3.07 | 0.0002 | 1.34 | 3.50 | 4.20 | | 1.44 | 1.58 | 3.07 | 110 |

**(a), two readings, both reported.** The decisive step's full worth, the distance from the route that takes
every other step right to the golden, is 4.64 bins on the shipped pack and 4.65 at the mean. Its worth at the
last rung, the distance from rung 2 to the golden, is 2.58 to 3.80 bins, mean 3.07. The conservative reading
is the second, and it is the one the law is read against: **2.58 bins at worst against (b) plus (c) of at most
1.43, a factor of 1.80**, and the largest gap in the ladder at every seed.

**(b) is 0.0002 bins at every seed, and it is tested rather than asserted.** Five constructions of the
estimator, the squared fraction, the hypergeometric pair inclusion, the per-county grouping, the per-batch
grouping and the two-step reading, are unanimous to the unit, because the estimator is an observed count over
a constant the statute fixes: there is no fitted parameter, no window, no band width, no distribution family
and no grouping for a solver to choose. The hypergeometric construction differs from the squared fraction by
one signature. The one thing that could open this family is signers who signed three or more times, because
the all-doubles expansion then overstates by one minus the sampling fraction per registered triple signer:
**measured at 106 to 118 signatures, 0.021 to 0.024 bins, at every seed**, against 150 triple signers and
34,000 double signers. That bound is a construction constraint, not an observation: swept to a five per cent
triple share among multi-signers the all-doubles estimator is biased 0.59 bins and the multiplicity mix is
not identified from the sample at all, which would be a Gate B failure. The generator therefore draws
multiplicity near binary and `checks.py` asserts the bias under 0.05 bins at every seed.

**(c) is 1.26 to 1.43 bins, mean 1.34**, read under the refinement filed in `determinism-check`: the
estimator has no free parameter, so every solver computing it files the same figure to the unit and the
interval is the quantity's honest uncertainty rather than a fork. It is reported because it sets how much of
the bin the ladder may not use.

**The stage 3 pin, and what it cost.** The author's three targets are met and measured: the golden sits
**60** signatures from its cell's centre at the shipped seed (target 1,500), and **both band clearances are
at or above 2.5 bins at every one of the six seeds**, the worst being 2.82 (target 2.5), where the design
stage measured 1.91 at seed 162 against a sampling interval of 1.82. The pin is the campaign's own
parameters, not a wider bin: the double-signer count, the single-ground rates and the share of the March
cancellations that fall after their signers' signing dates. What it cost is the decisive step's absolute
worth, which fell from a design-stage 6.99 bins to a measured 4.64 on the shipped pack, because centring the
golden inside a band 7.70 bins wide with 5.0 of it reserved for clearance caps the duplicate burden the world
can carry. The law still holds at every seed with a factor of 1.80, and the decisive gap is still the largest
in the ladder at every seed.

**What the arithmetic will not give, recorded rather than smoothed.** Rung 2 cannot be held outside the
statutory band at all six seeds while the golden is held 2.5 bins clear of both boundaries: rung 2 is the
golden plus 0.64 of the duplicate burden, so pushing it past the upper line needs a burden the position target
forbids. Sixty parameter sets were measured over the six seeds and none met both. The shipped seed keeps rung
2 outside the band by 710 signatures; the other five put it inside, with its figure three cells from the
golden's at every seed. The author's stated targets were taken as primary and this is the claim that gave
way.

## Pre-ship check

Every gate below was re-run on the final build of 2026-10-27, after the stage 4 return was answered in one
generator pass.

- Generator checks: **146 run, 0 failed**, exit 0. Independent verifier (pandas, bundle only, no generator
  import): **29 run, 0 failed**, exit 0.
- Two consecutive builds byte-identical on `target/`, `golden/`, `figures.json` and `submission.md`;
  `target.zip` sha256 `03a605c6acdecb39d97d465b28399eeb013be957155e0dff9aa8b7b4b9901d93` on both.
- `figures_check.py`: **96 figures in blocks 1 to 4, 0 absent** from `figures.json`, exit 0.
- `precut.py`: **52 checks, 0 FAIL, 0 WARN**, exit 0. `voice-check.py`: PASS, 970 characters, exit 0.
- `leak.py --asof 2028-08-04`: **REVIEW, no LEAK**, exit 1 (the REVIEW verdict's own code). Seven REVIEW
  lines, each answered here. The Navajo code list is that recorder's own code table, which maps codes and
  says nothing about them, so it is data rather than a file that describes the pack. The filing record
  carries the seven words of the committed call because the statute's third outcome is the examination of
  all signature lines filed, stated beside the other two outcomes and with no figure of the projection
  anywhere in it. The three documents carry four to seven of the stump paragraph's twenty-five terms, every
  one of them a generic institutional noun (division, record, disposition, arizona, sheets, office,
  recorders, instruction, duplicate, filing) and not one of them a pair, an inclusion probability, a squared
  fraction or a count of signers. The circulator extract and the firms' manifests name the four firms beside
  registration numbers and sheet counts, and neither carries a validity determination or any figure the call
  reads. The statutory figures the filing record must state are declared under `stated_inputs` and the
  statute's own nouns under `field_terms` in `metadata.json`.
- `guard.py surface`: **exit 0, no BLOCK**. The persona BLOCK the screen raised on the earlier build is gone:
  the receiving staff and the firms' contacts are drawn afresh, and the four personas the pack now carries
  (Arizona Secretary, Philip James, Tony Lynch, Verde Petition) raise one NOTE, that `Arizona Secretary` and
  `Verde Petition` are not on the card's `world.people`, which is the author's field to extend. The clone
  screen's own half promotes eight pairs holding task157, six of them on surface alone at 0.101 to 0.104
  where the corpus's 99th percentile is 0.100, one back-to-back pair with task156 on two card axes (gap
  population, decision quantity_figure) and one with task98 v7 on gap, pattern, Gate G and calibration form,
  which `heart` already records as differentiated and which `guard.py check` cleared at the draw. The screen
  still reads this build as delivered on 10-17, which is architecture 1's record in `pipeline.json`, so its
  severities are read one level high.
- `guard.py heart`: exit 0, **WARN, no BLOCK**, nearest driver 0.09 (task445 v1), three WARNs
  (`overuse.org_family` government_agency, `repeat.deliverables` png and xlsx against task144,
  `repeat.question_form` how-many against task464) and two older-build NOTEs, each answered in `## Draw`.
  Both are corpus-comparing gates and were read on 2026-10-27; `reduce-house-fixes` H31 asks for them again
  after the final pull and before the push.
- `scrub_producer_metadata.py`: `target/` and `golden/` both clean, no producer signature and no
  out-of-band timestamp.
- Input gates: **15 files, 4 formats** (11 csv, 2 pdf, 1 xlsx, 1 txt), largest **44,120 rows**
  (`petition_sheet_index_2028.csv`), two declared distractors in `metadata.json` and named nowhere else,
  every file with source, date and licence.

## Clone adjudication, the promoted surface pairs, 2026-10-27

`guard.py surface` screened 298 builds and 297 pairs and promoted ten holding task157, with no BLOCK.
Eight are surface similarity alone at 0.101 to 0.104 against a corpus 99th percentile of 0.100 (task134,
task448, task470, task179, task150, task281, task143, task170): a margin of three thousandths on a lexical
measure, every one of them a petition, register or return world sharing institutional nouns, and none
sharing a driver. The two promoted on mechanism are adjudicated here because a promotion on mechanism is
the finding the screen exists for.

- **task156 vs task157, flagged back to back because two of three mechanism axes collide.** The colliding
  values are `gate_g: forecasting`, `decision_type: quantity_figure` and the `population` member of the
  gap, and the third axis, `pattern`, reads `none` on both, which is an absence rather than a collision.
  Those three are among the most common values in the corpus, so what collided is labels. The mechanisms
  do not: task156 rides heterogeneous hazards, where the fast leavers go first so a pool's observed
  leaving rate falls as its members age, and this build rides the inclusion probability of a property that
  belongs to a PAIR of records, so a five per cent sample reveals it with probability one in four hundred
  rather than one in twenty. No shared latent structure, no shared default path, no shared correction, and
  the two reflexes a solver brings are opposite (fit a curve to an ageing pool against scale a count by the
  sampling fraction). No axis ban fires either: the pairing, the subdomain, the strategy
  (`other` against `forecast_method_backtest`) and the calibration form (`prior_period_close_out` against
  `none`) all differ, `guard.py check` cleared the draw and `heart` returns WARN with no BLOCK.
- **task98 vs task157, flagged because gap, pattern and decision family all collide with no surface
  overlap**, at 0.084 and only the 65th percentile. Same reading: the shared values are the `population`
  gap, a `none` pattern and `quantity_figure`, plus a genuinely shared organ in
  `calibration_form: prior_period_close_out`. The driver is not shared: task98 resolves identity across two
  dated schedules held under different keys where a subset of members stands in both, which is a join
  problem; this build's decisive step is an inclusion probability, which is a sampling problem. A shared
  calibration organ is reuse of a proven component, which `clone-check` holds legitimate; what may not be
  reused is the thing that drives the stump, and that is not shared. task98 is not within the three builds
  `ban.calibration` reaches.

The screen reads this build as delivered 10-17, which is architecture 1's record in `pipeline.json`, so
every severity above reads one level higher than it should.

## The standing design risk, stated rather than discovered later

Arizona's real statute prescribes a proportional projection of a signature sample, which is this ladder's
rung 1 and files 413,240, printing 415,000, and reads sufficient. Nothing in the pack ships that formula:
the filing record states the sample's size, the number required and the three outcomes, and never an
expansion, which both the leak reader and the judge's thread confirmed clause by clause. The asking
sentence asks what a full count would find rather than what the statutory projection gives, and that is
what keeps the decisive step analytical rather than rule application. The exposure is a domain expert on
the portal who reaches for the statute's own method from memory rather than from the pack. That is a real
risk and it is not closable from inside the build without either shipping the formula, which makes the step
rule application, or asking a different question, which is a redesign. It is recorded here, and if the
portal returns on it the repair is at stage 2 and not a sentence.

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

- **Stage 3 of architecture 2, 2026-10-27. What the build measured and what it moved.**
  - **Architecture 1's `generator/checks.py`, `verify.py`, `calc.py` and `ops.py`: replaced or deleted.**
    The old checks asserted SF1 to SF15 for forks this architecture does not have, which is the FAIL
    `precut.py` was fixed to catch. The new `checks.py` asserts this build's own eight rows and runs 134
    checks; `ops.py` and the old `calc.py` were architecture 1's fund arithmetic and are gone (138 checks
    after the house-fix pass added a second PDF extractor, the citation resolution and the denominator
    refusal).
  - **The design-stage figures: superseded by the pin.** The note carried a golden of 388,460 against a
    default path of 431,420 at a slip of 400 and a duplicate count of 92. The stage 3 pin (the
    double-signer count, the single-ground rates and the share of the March cancellations falling after
    their signers' dates) moves them to 390,200 against 420,520, which is what the band and cell targets
    cost: the decisive step's full worth falls from 6.99 bins to 4.64 and its worth at the last rung from
    4.33 to 2.96, against (b) plus (c) of at most 1.44.
  - **Rung 2 outside the statutory band at all six seeds: not reachable, and recorded rather than
    smoothed.** Sixty parameter sets were measured over the six seeds against the author's two position
    targets and the rung-2 band together, and none met both, because rung 2 is the golden plus 0.62 of the
    duplicate burden while the golden must sit 2.5 bins clear of both boundaries. The shipped seed keeps
    rung 2 outside the band by 850 signatures and the other five put it inside with its figure three cells
    from the golden's.
  - **SF4's duplicate fold: re-rooted into two single-signature grounds.** The design stage had Navajo's
    merged code covering duplicates and the general class, closed by that county carrying no duplicate
    strike. A wrong split of 34 lines would then have moved the call by 12,920 signatures, 2.6 bins, so the
    fold was a live fork on the main call. The merged code now covers two grounds that both carry at the
    sample's factor (not registered, and registration cancelled), the split is forced by the registration
    the recorder matched, and `checks.py` asserts the projection identical under either reading.
  - **The ask layer: rebuilt on three primaries after the first one measured 0.495 of the ask weight.**
    The design-stage sheet's four devices were a code fold, a correction file, a sheet key and a
    determined-by filter, every one of them documented in a shipped file or found by the hygiene battery,
    so the cracker kept 45 of 91 ask figures and a single response scored 72.0. Rebuilt on three
    reconstructions over dated records (the registration state at the day signed, the firm as at the day
    signed, the day-first dates), with the free per-code ask cut, the cracker keeps 16 of 90 and the worst
    honest reading is 66.4 for a single response and 44.1 for the pair.
  - **SF5 closed by a filed sentence rather than by convergence.** The firms' manifests claim 543,380
    lines against the office's 540,000, which at the design stage was asserted convergent. Measured, the
    manifest basis projects 392,488, which does print the golden's own cell, but the margin is a draw, so
    the filing record now states flatly that the 240 sheets presented in duplicate were struck at receipt
    and are not part of the filing, and the row is closed by that sentence with the convergence reported
    beside it.
  - **Every sheet exactly full: dropped.** 540,000 lines on 36,000 sheets of fifteen makes the sheet
    register a constant column, which the realism sweep reads as a generator's arithmetic. The office now
    receipts 38,080 sheets carrying 5 to 15 lines each and summing to the statutory 540,000, asserted.
  - **The circulator register without the firm on the sheet index: the only way ask B's primary is not a
    fork.** With a firm column on the sheet index or the receipt log there are two defensible firm
    attributions and the ask is forked rather than deviced; both columns are gone and the circulator
    registration extract is the single source, so the as-of join is the work and not a choice.
  - **Floating point in the two expansion factors: removed.** The sample's factor and the pair's
    denominator are computed as integers (twenty and four hundred) because `61 / (0.05 * 0.05)` is
    24,399.999999999996 and cost a signature to rounding in the first write-up.
  - **The global sheet sequence: dead, and the assertion that passed over it with it.** The instruction and
    the filing record both file that a sheet number is the circulator's own series running from one, which
    is what makes the line key need the circulator's registration number as well. The generator numbered
    sheets 1 to 15,044 in one global sequence across all 329 circulators, so no circulator had a series of
    its own and the key claim was false in the data while `checks.py` passed on it: the assertion tested
    that some number repeated across circulators, which a global sequence satisfies by coincidence because
    the returns carry the same number under different circulators only by accident of the draw. Each
    circulator is now numbered from one over its own sheets in receipt order, 412 distinct numbers over
    44,120 sheets, and the assertion tests the claim instead: every circulator's own series is one to n and
    contiguous, and a number is shared by two circulators under different serials.
  - **Ask A's count of each recorder's own determinations: cut, measured.** It was 15 of the sheet's 90
    figures and the cracker kept all 15, because the verification instruction tells a reader how to filter
    the division's lines. Cutting it took the cracker's keep from 0.178 of the ask weight to 0.040 and the
    worst honest single response from 66.4 to 58.2, under the build target of 60, with the main call and
    the projection untouched. The population it supplied now lives inside ask A's own asking sentence,
    where it is not separately graded.
  - **The per-code ask kept in the prompt after its table was cut: a prompt that asked for a deliverable
    the pack's goldens did not carry.** The asks were restructured at stage 3 and `prompt.txt` was not
    rewritten with them, so the shipped prompt asked for a per-disposition-code figure with no table behind
    it and gave the per-month ask the sheet serials instead of the figure the workbook holds. The prompt is
    now written from the three asks the goldens carry, and the month range is pinned in the asking sentence
    (January to June 2028) rather than left to the data.
  - **Two ask-side forks closed by the filing record's own sentences rather than by a convention in the
    code.** A circulator who moves firm is withdrawn on the day its new registration takes effect, so 17
    sampled lines sit on a handover day and the firm they belong to was a convention; and one firm's two
    trading names on one registration number split 141 lines into a fifth firm against an asking sentence
    that names four. Clearing the handover days in the generator was tried first and cannot work: the
    circulators who move are the busiest, so there is no day inside the window on which they gathered
    nothing. The filing record now carries a `Circulator registrations` section stating both conventions,
    which is legitimate on this side of the build because rule 3 binds the main call's decisive step and
    the asks are free of it, and `checks.py` asserts both against the extract's own rows.
  - **The primary-cost assertion rewritten to test its claim.** It asserted that each primary solved on its
    own lifts the cracker's total, which is false once two primaries compose: solving the firm as at the day
    signed while still reading dates month first scores two figures below the cracker's baseline, because
    the right firm with the wrong month moves cells that had matched by accident. It now asserts what is
    actually claimed, that every primary is load-bearing (a response solving the other two without it keeps
    16, 29 and 55 of 75) and that no primary solved alone reaches a third of the ask weight.
  - **Seventy-three per cent of sheets at exactly fifteen lines, consecutive bundle ids and round-robin
    receiver ids: all three dropped as procedural shapes.** The weighted draw over 4 to 15 lines now leaves
    a 27.6 per cent mode at the pad's full fifteen, bundle ids step by one to four, and the six receiving
    staff ids carry an uneven load (274, 228, 174, 94, 82, 53) instead of cycling. The two statewide
    snapshots no longer carry the same row count or a monotonic identifier column, status_changed_utc
    equals the registration date only for the quarter of rows never touched since registration, the query
    notices are spread over ten dates after each line's own return rather than all on one day, and the
    instruction PDF's creation and modification stamps differ.
  - **The 2024 close-out as a pointer: re-subjected rather than cut.** It read as a file placed to be
    compared with this filing. Its county table is now subjected on the examination itself (lines examined,
    examiner days, examination closed) and its header states that every signature line filed was examined
    and no sample was drawn, so it carries its own subject and still ties under every expansion basis.

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

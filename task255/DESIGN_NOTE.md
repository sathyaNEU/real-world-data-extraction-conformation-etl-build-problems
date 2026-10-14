# task255 design note

## Draw

- **Card:** `cards/task255.json`, registered 2026-10-13. Actuarial Science & Insurance, task type
  claims-frequency-severity, objective Descriptive & Distribution Analysis; shape 04 (setting one dial: each quoted
  attachment); decision dial_setting; gap population; G12 then G16; Gate G method_or_model_selection; strategy
  maturity_censoring (here limit censoring at the pool's retention with deductible truncation, no maturity element).
- **World:** Fallowmere Intergovernmental Risk Pool, a Washington pool of 62 cities and special districts. The pool
  shares its members' liability occurrences above each member's deductible ($10,000, $25,000, $50,000 or $100,000,
  elected yearly) up to its per-occurrence retention, inclusive of the deductible ($250,000 for occurrences in 2014
  to 2017, $500,000 from 2018); its excess insurer pays above the retention, outside the pool's claims system. For
  1 January 2027 the broker gathered indications at seven attachments from $1.0 million to $5.0 million, and the
  trustees' risk financing policy keeps every layer the pool expects to be reached more than once a year. The
  trustees set the 2027 retention at their meeting of 18 November 2026 (forcing event vote_or_meeting).
- **People** (guard.py names --geo US --seed 255): Laura Williams, finance director; Larry Hodge, consulting actuary;
  Matthew Klein, the broker's account executive; Caleb Payne, claims manager.
- **Data-native sentence:** a pool's claims record is a window on its members' losses: an occurrence enters it only
  once its member has paid the deductible in force that year, and stops at the pool's retention, beyond which the
  excess insurer pays and the pool records nothing; both thresholds were fixed in each year's dollars, so at 2027
  cost every occurrence carries its own floor and its own ceiling; and the occurrences that pierced the retention are
  suits the excess insurer goes on defending for years after the pool has paid its layer, so the pool's files on
  exactly those occurrences stay open long after the small ones close (20 of the 108 from 2014 to 2021 are open).
- **Loop 1 (2026-10-13, the author's request for a second layer of stumping):** the world no longer forces every
  occurrence of 2014 to 2021 closed; an occurrence past the retention runs a suit about three years longer (the excess
  insurer's defence), and once it has used the pool's layer the pool's file stays open until the excess insurer
  closes its own. Twenty such suits of 2014 to 2021 are open at 30 September 2026, every one with the layer paid in
  full and nothing reserved. The policy's window is now named without closure ("the eight accident years before the
  latest five"), so the record of those years holds open files. The golden is unchanged ($4.0 million, 0.74 and
  1.25): the loop-0 construction on every file. The loop-0 construction on the closed files alone, the natural way
  to fit severity to final costs, drops a fifth of the occurrences that reached the retention and files $3.0
  million. No file, column or sentence was added; the strategy stays maturity_censoring (open files of the window,
  beside the retention's censoring), the second layer a selection by settlement.
- **Guard:** WARN repeat.gate_g and overuse.gate_g (method_or_model_selection after task450 and task501): the
  mechanism here is a loss model's observation process, deductible truncation and retention censoring in the
  likelihood, against task450's emissions grain and task501's transmission model; the vocabulary's nearest honest key.
  Question form how-much: the attachment is the amount of each occurrence the pool keeps.
- **Pairing and shape:** the field's own analysis decides (a loss distribution fitted to data observed through
  deductibles and a retention), the objective is the shape of that distribution's tail, and the call is a dial over
  seven quoted attachments (shape 04). Criteria: seven attachments, each with its expected 2027 count above it and its
  2027 premium (14); the call, the runner-up ($3.0 million), the gap and the flip (4); the rated exposure by member
  class, operating expenditure and vehicles for seven classes (14); the chart's named parts (5); two files (2). 39.
- **Sources, one line each.** `guard.py mechanisms --objective descriptive-distribution` (26 builds): none fits a
  size distribution through an observation process; task254 v2 (spent at stage 2) cut a time-to-event distribution
  censored by a lock date, differentiated on the card; task139 (the other actuarial claims-frequency-severity card in
  the last twelve) read a nurse intervention per assigned intake, a causal design; task185 converted a station's
  instrument change for a heat cover. `layer2-rigor-patterns.md` has no actuarial patterns, so the family comes from
  `two-layer-task-design.md` ("the data's real structure such as censoring"); the pattern is this build's own. The
  seed DA05 gave the number only.
- **Forward facing:** the call is the 2027 retention, a window not yet open; the curve is fitted to closed years and
  brought to 2027 cost with the actuary's projected index.

## Default path

1. Read the current administrator's loss run (csv) and the legacy administrator's closed-claim archive (xlsx, one
   sheet per accident year) and keep the closed liability occurrences of accident years 2014 to 2021, the ones whose
   costs are final: 800 (the 20 open files set aside).
2. Take each occurrence's ground-up cost as its member's deductible plus the pool's payments (damages and defence)
   and bring it to 2027 cost with the claim cost index (the 2027 index over the accident year's).
3. Fit the policy's lognormal by maximum likelihood to the 800 costs at 2027 cost, the mean and standard deviation of
   their logs: log mean 12.04, log standard deviation 0.85.
4. Expected 2027 occurrences above each quoted attachment: the actuary's 228.7 above $25,000 times the fitted
   probability of exceeding the attachment over that of exceeding $25,000.
5. Take the lowest quoted attachment where that is one or fewer.

Ends on: $2.0 million
Golden: $4.0 million

## Stump sentence

The default path fits the policy's lognormal to the 800 closed occurrences' recorded ground-up costs as if they were
the whole curve and ends on $2.0 million (0.43 expected 2027 occurrences above it), because the pool's record holds
only occurrences that exhausted their member's deductible and stops at the retention; censoring the 88 closed ones
that reached the retention still ends on $2.5 million; carrying each deductible as truncation as well, both thresholds
at 2027 cost, ends on $3.0 million (0.70) while the 20 open suits stay set aside, because the occurrences that pierced
the retention are the ones still open; only the same fit on every file of 2014 to 2021, the open suits censored at
the retention their paid layer reached, files $4.0 million (1.25 occurrences above $3.0 million, 0.74 above $4.0
million).

## Three rules

- **Task type:** claims-frequency-severity in Actuarial Science & Insurance, serving Descriptive & Distribution
  Analysis: the call reads the tail of the ground-up severity distribution at each quoted attachment.
- **Domain test:** the deciding quantity is the ground-up severity tail at each attachment, fitted the way loss models
  are fitted to insurance data observed through deductibles and limits (a truncated and censored likelihood with each
  observation's own thresholds at the fitted cost level) and turned into an expected excess count from the actuary's
  frequency above $25,000; that is the claims-frequency-severity task type's own construction.
- **Swap:** with a hospital's nouns ("how much of each patient's stay the ward funds before the regional fund pays, from
  the stays the ward recorded") there is no deductible below which stays never reach the record, no retention at
  which the record stops, and no quoted attachment to choose, so the estimator and the decision stop making sense.
- **Layer 1:** the legacy administrator's closed-claim archive (one sheet per accident year, title blocks, dates as
  text, currency formats) written by the system the pool left on 1 July 2020; the current administrator's loss run,
  claims open at the conversion carried under new numbers with the legacy number kept; member codes in the archive
  against member numbers elsewhere; occurrence costs in each year's own dollars beside the actuary's index; for the
  asks, the vehicle schedule kept as a log since its opening load and a consortium's bulk load, and declarations taken
  online and on paper. Nothing is placed to be caught; every main-path item leaves the call and the components where
  they are when mishandled (asserted).
- **Layer 2:** estimation_fit: the likelihood of the record the pool actually holds, each occurrence left-truncated at
  its member's deductible and right-censored at the retention when it reached it, both at 2027 cost, instead of a
  complete-sample fit of the recorded costs, on every file of the window rather than the closed ones, whose closure
  is selected on size (the suits past the retention run on under the excess insurer's defence); the open suits lift
  the expected count above $4.0 million from 0.38 to 0.74 and move the call from $3.0 million to $4.0 million.
- **Decisive step:** fitting the ground-up severity with the record's own observation process in the likelihood,
  truncation at each member's deductible and censoring at the pool's retention, at the cost level of the fit, over
  every file of the window: an open suit whose layer is paid is a complete censored observation, and leaving the open
  files out selects the record on settlement, which here is selection on size.
- **Not semantics:** every field reads plainly (the deductible, the pool's payments and reserves, the status, the
  retention in the coverage memorandum), and a solver who reads them all and knows the capped occurrences stopped at
  the retention still files $2.5 million when it fits without the deductible's truncation, and $3.0 million when it
  fits only the files whose costs are final: no field, code or definition says how the record's floor enters an
  estimate or whether an open file belongs in it.
- **Not rule application:** the policy files the family (lognormal), the estimator (maximum likelihood), the record,
  the window, the cost level, the count formula and the line; it files no likelihood and nothing on open files, and
  executing every filed rule on the recorded costs files $2.0 million; writing the likelihood of a
  deductible-truncated, retention-censored record, with the open suits in it as the censored observations they are,
  is the step no rule performs.
- **Analyst test:** a strong analyst who cleans both loss runs, reads every field and rule, brings the costs to 2027
  cost and fits the lognormal by maximum likelihood to the 800 closed files' recorded ground-up costs files $2.0
  million (the default path's Ends on: $2.0 million), with the 88 closed capped occurrences censored files $2.5
  million, and with truncation and censoring at 2027 cost on the closed files still files $3.0 million.
- **Estimand:** the trustees' risk financing policy fixes the curve as the distribution of what a member's liability
  occurrence costs from its first dollar, damages and defence together, at 2027 cost, over all the members' liability
  occurrences, estimated by maximum likelihood from the pool's claims record for accident years 2014 to 2021 (the
  eight before the latest five), and the retention as the lowest quoted attachment whose expected 2027 count above
  it is one or fewer (risk_financing_policy_2026.pdf).
- **No decoy:** nothing is planted: no memo, draft, briefing or stakeholder figure states an attachment, a fit or a
  count; the loss runs are the administrators' own records and every row is a real occurrence.
- **No certified replay:** no certified or published figure is reproduced by the method: the actuary's exhibits file
  the index and the count above $25,000 and no severity parameter, count above any other amount or layer cost.
- **Lesson:** a loss distribution fitted to what a pool records is fitted to a window, floored at each member's
  deductible and cut at the retention, and the files still open are not a random few: the largest losses settle
  last; reading the window as the whole curve, or its closed files as the whole window, thins the tail exactly where
  an excess attachment sits. No build on file fits a size distribution through truncation, censoring and
  settlement.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R1, the closed files' 88 occurrences at the retention censored ($2.5m) | the memorandum says the excess insurer pays above the retention, outside the pool's system | 88 closed costs sit exactly at $250,000 or $500,000 | a solver used to limited losses censors them | none | no | no | readable |
| R2, each deductible as truncation, the capped costs read as exact ($2.0m) | the memorandum's tender sentence says how an occurrence reaches the pool, naming no truncation | the deductible is an ordinary loss-run column, no row predicate | not a default | none | no | no | silent |
| R3, truncation and censoring at 2027 cost on the closed files ($3.0m) | no sentence names a truncation, a censoring or a likelihood | no flag; the floor differs by member and year | the opponent fits severity to final costs: closed files only | none | no | a likelihood | silent |
| G (decisive), the same likelihood on every file of 2014 to 2021, the open suits censored at the retention their paid layer reached ($4.0m) | no sentence names a truncation, a censoring, a likelihood or open files; the policy names the record of the years, the notes say the current run holds open and closed files | the status column reads Open on 20 rows whose payments reach the retention, nothing marks them as belonging to a fit | not a reflex: the reflexes fit the recorded costs, censor only the visible caps, or keep the closed files for their final costs | nothing scores a fit: no severity parameter, no count above any amount, no excess-layer experience ships | the battery sees no floor and treats open files as unfinished | a likelihood, no ratio or subtraction | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | attachment | from the first dollar, inclusive of the member's deductible | excess of the member's deductible | each count read above attachment plus deductible | policy 5.2 and the indications: attachments are stated from the first dollar of an occurrence, inclusive of the member's deductible |
| SF2 | occurrence | one row of either loss run | one claimant | same call | same call: both loss runs are one row per occurrence |
| SF3 | cost | the deductible plus the pool's paid damages and defence | damages only ($2.0m) | $2.0 million | policy 4.1: damages and defence costs together |
| SF4 | 2027 cost | the 2027 index over the accident year's | no trend ($2.5m) | $2.5 million | policy 4.2 names the index and the ratio |
| SF5 | the record | the legacy archive and the current run together | the current run alone (no attachment passes) | none | the extract notes: the archive holds the claims the legacy administrator closed before 1 July 2020, the current run every claim handled since |
| SF6 | the record of 2014 to 2021 | the 820 files of those years, open and closed | the closed files of every accident year ($2.5m) | $2.5 million | policy 4.2 names the years |
| SF7 | expected number above an attachment | 228.7 times the fitted tail ratio to $25,000 | counts read off the record | not a count of 2027 occurrences | policy 4.3 |
| SF8 | one or fewer | at most 1.0, inclusive | strictly under 1.0 | same call: 1.25 and 0.74 at $3.0m and $4.0m | same call |
| SF9 | thresholds' cost level | each deductible and retention at 2027 cost with the occurrence | left in each year's dollars | same call ($4.0m, 0.65 and 1.31) | same call |
| SF10 | the deductible of an occurrence | the one on the loss-run row, in force on the date of loss | the member's current deductible | not on any row | the memorandum: the deductible in force on the date of the occurrence applies; the loss runs carry it |
| SF11 | the quoted attachments | the seven in the broker's indications | an interpolated attachment | not quoted | policy 5.1: the lowest attachment quoted for the year |
| SF12 | rounding | counts unrounded until compared, shown to two decimals; premiums rounded once at the total | rounded before comparing | same call | same call |
| SF13 | the anchor amount | $25,000 from the first dollar at 2027 cost | at each year's cost | not the actuary's figure | the actuary's exhibit states its count at 2027 cost from the first dollar |
| SF14 | maximum likelihood | the maximum over the lognormal's two parameters, one optimum | a local optimum | same call | same call: five starting points reach one optimum (asserted) |
| SF15 | an open file's recorded cost | the deductible plus what the pool has paid and still reserves | the deductible plus payments to date | same record (asserted): every open file of 2014 to 2021 has its layer paid in full and nothing reserved | same call and same counts |
| SF16 | a vehicle on the schedule (the asks) | one vehicle by its VIN, or its serial without a VIN, on the schedule at 30 September 2026 by effective date, a consortium vehicle by its FMC- record | the last row across every number the vehicle holds, any of its numbers in force (6,387), every unit number in force (8,233) | other premiums and class vehicles | the extract notes: a vehicle is identified by its VIN or serial; the members' earlier numbers were left on the schedule and still take the revaluations; since 4 March 2024 the consortium's adds, changes and deletes come under its asset numbers (filed after loop 1's judge pass 1) |

## Ladder

| Rung | Likelihood | Log mean, log SD | Expected 2027 occurrences above $3.0m and $4.0m | Call |
|---|---|---|---|---|
| R0 | the closed files' recorded costs as a complete sample (800) | 12.04, 0.85 | 0.08, 0.02 | $2.0 million (0.43 above it, 1.20 above $1.5m) |
| R1 | the closed files, the 88 capped censored, no truncation | 12.10, 0.94 | 0.30, 0.11 | $2.5 million (0.56 above it, 1.16 above $2.0m) |
| R2 | the closed files, each deductible as truncation, caps read as exact | 11.05, 1.18 | 0.16, 0.07 | $2.0 million (0.50 above it) |
| R3 | the closed files, truncation and censoring at 2027 cost (the loop-0 construction) | 10.45, 1.53 | 0.70, 0.38 | $3.0 million (1.02 above $2.5m) |
| G | every file of 2014 to 2021, truncation and censoring at 2027 cost, the 20 open suits censored at the retention | 10.18, 1.71 | 1.25, 0.74 | $4.0 million |

- **Position:** the golden is the sixth of seven attachments; rung 0 takes the third. Every correction walks one way
  (up the attachments); only the decisive move (the open suits kept, at the retention their paid layer reached)
  reaches $4.0 million.
- **Margins:** at $4.0 million 0.74 (1.36x under the line); at $3.0 million, the runner-up, 1.25 (1.25x over it).
  R3's own pick is thin (1.02 at $2.5m): a variant of it lands on $2.5 million, either wrong.
- **Worth:** the decisive move (R3 to G) nearly doubles the expected count above $4.0 million (0.38 to 0.74) and
  moves the call one attachment; R1 to G multiplies it by 7.0.
- **Every single correction with the open suits kept** (asserted): the complete sample $2.0 million, censoring alone
  $2.5 million, truncation alone $2.0 million; thresholds left nominal with the open suits in $4.0 million (0.65 and
  1.31, other counts: a rung on the asks), on the closed files $3.0 million.
- **Convergence asserted:** the same likelihood in each accident year's dollars gives 10.18 and 1.71; a fit truncated
  at one common floor ($215,600) gives $4.0 million; an open suit read at its payments or at payments and reserves is
  the same record.
- **Flip:** $3.0 million would pass if the actuary's count above $25,000 were 182.5 or lower; $4.0 million fails
  only above 310.0.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the curve's population is every members' liability occurrence; the fit's is the record of the closed 2014 to 2021 occurrences | filed literally, policy 4.1 and 4.2 |
| 2 | Unit of account | the occurrence | policy and indications per occurrence; one loss-run row each (SF2) |
| 3 | Attribution window | accident year by date of occurrence | the memorandum's occurrence basis; dates on every row |
| 4 | As-of dating | the loss runs at 30 September 2026 | C1: every fit occurrence closed by 30 June 2026 |
| 5 | Version basis | the record as it stands at the evaluation | C1: closed values are final; the archive was cut at conversion |
| 6 | Denominator | the tail ratio's denominator, the probability above $25,000 | policy 4.3 |
| 7 | Weighting | one observation per occurrence | maximum likelihood filed (policy 4.2) |
| 8 | Window length | eight accident years, 2014 to 2021 | policy 4.2 |
| 9 | Boundary inclusivity | "one or fewer" inclusive; a cost at the retention reached it | C1: no count within 0.25 of 1.0; no uncapped cost within $15 of a retention |
| 10 | Rounding path | counts unrounded until compared; premiums once at the total | SF12, same call |
| 11 | Tie-break | none: one lowest passing attachment | by construction |
| 12 | Maturity and censoring | no maturity (every fit occurrence closed); censoring at the retention is the record's structure | the memorandum's facts; the decisive step, not a convention |
| 13 | Order of operations | thresholds and costs at one cost level before the fit | C1: the accident-year-dollar likelihood gives the same fit (asserted) |
| 14 | Row order | none | C1: the fit is the same under shuffled rows (asserted) |
| 15 | Duplicate resolution | a converted claim appears once, in the current run, its legacy number kept | C1: no claim number in both runs (asserted) |
| 16 | Identity normalisation | member codes against numbers (not needed for the call); VINs and serials for the asks | the roster maps codes; ask device D7 |
| 17 | Netting against gross | no recovery on any fit occurrence | C1: asserted none |
| 18 | Dimensional units | dollars; the index a ratio | the actuary's exhibit (2014 = 100.0) |
| 19 | Code and status semantics | "CL" in the archive, "Closed" in the current run; five liability coverage parts | the extract notes; every row is a liability occurrence |
| 20 | Integerisation | none; vehicles are whole units | by construction |
| 21 | Clause scope | 4.2's window for the curve, 4.3's anchor for frequency, 5.1 for the attachment | filed per clause |
| 22 | Forward window contents | 2027's count above $25,000 and its index value | the actuary's exhibits file both |

## Literal reader

Executed word for word, the policy fixes the curve as the distribution of all the members' liability occurrences from
the first dollar at 2027 cost (4.1), estimated by maximum likelihood from the pool's claims record for accident years
2014 to 2021 (4.2); the record of those years holds 820 files, 800 closed and 20 open, every open one a suit whose
payments have reached the retention; the coverage memorandum files how that record came to exist (an occurrence
reaches the pool when its member's payments exhaust the deductible in force, and the pool records nothing above its
retention), so the likelihood of the record is the truncated and censored one over every file, and its literal
execution gives a log mean of 10.18, a log standard deviation of 1.71 and $4.0 million. Every row of the fork table
violates a quoted sentence or converges on $4.0 million; the easy answers ($2.0 million, $2.5 million, $3.0 million)
come from an easier likelihood or from setting files of the named years aside, not from another reading.

## Oracles

- The actuary's 228.7 occurrences above $25,000: an input of every rung; it ties to nothing.
- The claim cost index: an input; it ties to nothing.
- The liability triangles (distractor): the pool's paid and incurred, net of deductibles and limited to its
  retention, by accident year and evaluation, with the counts tendered and closed; the latest diagonal ties to the
  loss runs under every handling, its closed counts show the twenty open files of 2014 to 2021 as the loss run does,
  and it carries no ground-up cost, no count above any amount and no severity parameter.
- The member deductible history (distractor): agrees with the deductible on every loss-run row; it scores no fit.
- The open accident years 2022 to 2026 in the current run: outside the policy's window and immature; the pack carries
  no development pattern to bring their counts to ultimate, so they score no fit (their counts at the retention are
  set beside each rung's expectation in `checks.py`).
- The ask layer: the declarations' department payroll is the benign twin of the repeated expenditure and ties to
  nothing; no 2026 rated exposure, premium or expiring programme ships (Tried and rejected).

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (lazy delta) | Realism |
|---|---|---|---|---|---|---|---|---|
| A, the 2027 premium of each quoted attachment | 7 | a measure every candidate carries that the call does not turn on | the trustees see each attachment's cost beside the policy's test | D6: an online declaration repeats the member's total operating expenditure, a member-level figure, on every department line (a paper declaration keyed by staff carries it on its first line only) | D1 (the consortium replay moves the vehicles in every premium); D8 (log rows effective after 30 September) | declarations (member, department, expenditure), schedule log (member, unit, type, effective date, VIN, serial), indications (two rates per attachment), roster (class), extract notes; 5 files, 12 columns | expenditure summed over lines and units counted raw: 3.41 to 3.45 times the golden across the attachments; expenditure once, units raw: 10 to 11 per cent high; expenditure summed, units right: 3.29 to 3.34 times; expenditure once, units deduplicated among those in force: 3.0 to 3.2 per cent high; the answer | a member portal flattens a header field onto each detail line; paper forms are keyed line by line |
| B, the rated exposure by member class | 14 (expenditure and vehicles, seven classes) | the audit trail of the premium's exposure | the board confirms the exposure the market rated | D1: on 4 March 2024 the fleet consortium's lists re-added sixteen members' fleets (the largest in each class) under the consortium's asset numbers; the pool's numbers were never deleted, and the consortium's later disposals reach the pool on its numbers only | D6 (expenditure); D7 (VINs keyed in lower case or with a space or dash; trailers and equipment with "NONE", "N/A", "UNKNOWN", "SEE SERIAL" or a blank VIN and a serial) | schedule log, roster, declarations, extract notes; 4 files, 9 columns | in-force unit numbers 8,233 (every class high); in-force units deduplicated by normalised VIN 6,387; raw-VIN dedup 6,563; VIN-only dedup (placeholders collapsed) 6,045; the answer 5,649 | a bulk load from a member's own system adds what it duplicates without closing the old records |
| C, the policy's test per attachment and the chart | 7 counts (in the call's question) and 5 chart parts | the construction | the call's own table | none | none | the golden fit | R0, R1 and R3 values (R3: 5.50, 2.71, 1.58, 1.02, 0.70, 0.38, 0.23) | the actuary's exhibit layout |

- **Main population zero-counts:** no row of the declarations or the schedule log sits in the loss runs, the policy,
  the memorandum, the actuary's exhibits or the attachments the call reads; the call and every component are unchanged
  with both ask files deleted (asserted).
- **Hazard table:** D6 moves every premium (A) and every class's expenditure (B); D1 moves every premium (A) and every
  class's vehicles (B); D7 moves the deduplicating paths (B); D8 moves any path that takes rows effective after the
  rating date.
- **Referee:** none; the roster maps classes and the extract notes describe the formats, and neither adjudicates a
  device.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A premiums at seven attachments | expenditure summed over department lines, units counted by in-force unit number | 3.41 to 3.45 times the golden | miss |
| B expenditure by class | summed over department lines | high in every class | miss |
| B vehicles by class | in-force unit numbers | high in every class | miss |
| C counts and chart | the golden's construction | right | outside |

Mirror leakage: about 8 per cent of the ask weight (the chart's two presence parts of 26 ask criteria; the mirror's
counts and chart values are R1's or R3's, each missing every count at two decimals, asserted).
Pair ceiling: 36 (the cracker at about 56 with the call and its counts, the mirror at about 15; if the rubric grades
the seven counts as asks the pair is about 40).

## Build record

- Generator: `world.py`, `analysis.py`, `records.py`, `docs.py`, `golden.py`, `checks.py`, `verify.py`, `build.py`,
  `postprocess.py`; `python3 task255/generator/build.py` builds the pack, the goldens, `metadata.json` and
  `generator/figures.json`, runs the checks and the independent verifier, rebuilds into scratch for the byte
  comparison and cuts `target.zip`.
- Pack: 12 files in 4 formats; the vehicle schedule log 43,855 rows; the legacy archive 467 occurrences in six
  accident-year sheets; the current loss run with 353 occurrences in the fit's years among all its open and closed
  occurrences; distractors the member deductible history and the actuary's triangles.
- Gates: 196 assertions with the three-rules block and SF1 to SF14; the verifier recomputes the fit (log mean 10.1769,
  log standard deviation 1.7102), the call, every count, the premiums and the class exposure from `target/` alone with
  its own parser and optimiser; two builds byte-identical; figures_check 88 figures; precut 49 checks; voice-check
  PASS; scrub audit clean on target and golden; leak.py REVIEW (no LEAK: the quoted attachments are declared stated
  inputs; the policy's own vocabulary; 26 schedule changes keyed before they take effect, allow-listed); guard
  surface 0 promoted; heart WARN (Gate G overuse, answered in the Draw).

## Judge record

- Pass 1 (stage 4): DETERMINISTIC, APPROVE. The isolated thread recomputed the record (820 occurrences, 108 at the
  retention), the fit (10.1769, 1.7102), the seven counts and premiums and the class exposure from the bundle alone,
  and tested the competing estimators: censoring without truncation ($2.5 million) and truncation without censoring
  ($2.0 million) each conflict with a memorandum sentence (2.3, 3.2); thresholds left nominal with costs trended
  still give $4.0 million; an untrended fit is inconsistent with the policy's record brought to 2027 cost. Ask-only
  fork: vehicles keyed on entered_date (5,602 on the judged pack) against effective_date, closed by the extract
  notes' definition. Gate G statistical_rigor, analytical_non_defect, no surface read, no sole data defect; Gate H
  domain pass, layers pass, decisive step analytical. Cosmetic: the class rows rounded one by one foot to a thousand
  above the total (the golden's notes say so; the write-up's total line now says it is rounded from the exact sum).
- After the judge: the leak reader's realism tells were fixed in the generator (member numbers in joining order, each
  unit's own depreciation with some values held, slower closings for claims tendered in 2019 to 2022, a market's
  uneven rate ladder, the log note's entry date; the consortium is now the largest fleets in each class, loaded
  4 March 2024). A second read's tells were fixed in the same way: a member admitted in 2024 had schedule rows dated
  from 2022 (now from its admission), unit numbers ran in member blocks (now in the order units were keyed),
  revaluations followed one formula (now the class's depreciation, steeper in a unit's first years, held at some
  renewals, an appraisal at a few, keyed in one batch per member), the rate ladder was one smooth curve (the auto
  rate now stops at the market's minimum above $3.5 million) and the triangles closed at the same pace every year
  (each accident year now has its own pace). The fit, the call and every count are the judged ones to the last
  digit; the ask figures and the archive split (467 and 353) moved and were rechecked by the 196 assertions and the
  independent verifier. No re-judge: the disposition was APPROVE and no estimand, rule or sentence the call reads
  changed.

- Loop 1 (2026-10-13, the author's request for a second layer). Stage 3: the world lets an occurrence past the
  retention run a suit about three years longer, the pool's layer paid by about three and a half years after tender
  and its file left open until the excess insurer closes its own; no clamp closes those suits by mid-2026, the
  uncapped files of 2014 to 2021 still close by then. 20 open suits in the window (8 converted from the legacy
  administrator, 18 from 2019 to 2021), every one with the layer paid and nothing reserved; the legacy archive now
  421 occurrences, the current run 399 of the window's. Policy 4.2 names the window without closure. The golden fit,
  call, counts, premiums and class exposure are the loop-0 values to the last digit; the closed files alone file $3.0
  million. 202 assertions (the analyst test now runs the closed-file construction on the clean truth, R3 at $3.0
  million, and the golden only with the open suits in); the verifier reads open files at payments and reserves and
  finds the twenty; two builds byte-identical; figures_check 93 figures.

- Loop 1, stage 4. Leak reader, first read: no decisive-step sentence; it quoted the memorandum's "once the pool's
  share is paid, the pool's administrator closes the pool's file on the occurrence", which the twenty open suits
  contradict: the clause is cut (the memorandum now says only that the excess insurer's payments are not entered),
  and the extract notes' "The documents beside them are as issued" reads "Filed with them as issued". Second read: no
  decisive-step sentence, no contradiction, nothing names the open suits. Judge pass 1 (one isolated thread):
  NOT_DETERMINISTIC on the asks only, the main call forced and reproduced (820 files, 20 open, 108 at the retention,
  10.18 and 1.71, $4.0 million; closed files alone $3.0 million): the vehicle count behind the premiums and the class
  vehicles turned on a rule no file stated (the consortium's FMC- numbers against the members' earlier numbers, which
  still take the revaluations). Fixed in the generator: the extract notes file a vehicle's identity (its VIN, or its
  serial without one) and how the consortium's numbers relate to the earlier ones (SF16, asserted); no figure moved.
  Third read (on the fix): no decisive-step sentence; it asked whether the unit count is by effective or entered
  date, which the notes file (effective_date is when the change applies to coverage). Judge pass 2 (the one re-judge):
  DETERMINISTIC, APPROVE; every figure reproduced, the premiums and the class figures included; the competing fits
  (closed files alone, the open suits read as exact, no truncation, censoring alone, no trend) all miss; entered dates
  for the vehicles would move each premium by about $825, against the notes' effective-date definition; Gate G
  analytical, Gate H domain, layers and decisive step pass.

## Leak record

- leak.py REVIEW, no LEAK: the policy carries the call's own nouns (retention, attachment, occurrence), harmless; four
  documents use ordinary domain words (record, deductible, likelihood, closed), none names a truncation or a
  censoring (asserted); 25 schedule changes keyed before they take effect, allow-listed in metadata.json.
- Reader 1 (fresh copy of prompt.txt and target/): no decisive-step sentence (the memorandum's tender and excess
  sentences make the structure discoverable, neither says to adjust for it); no ranking file; no analyst-only file;
  no answer-like figure. Question 5: it read policy 4.2 as leaving the likelihood open and computed the three
  likelihoods to the golden's own figures ($2.0 million, $2.5 million, $4.0 million); ruled: the curve of 4.1 is over
  all occurrences at their full cost and the memorandum files how the record arises, so the record's likelihood is
  the truncated and censored one (the judge reached the same reading on its own). Question 6: an analytical choice.
- Reader 2 (after the realism repairs, fresh copy): no decisive-step sentence; the extract notes describe files and
  name no pitfall. Its tells were repaired as the judge record says; two did not hold on checking (every cleaned VIN
  is free of I, O and Q and carries its model year in the tenth place) and three are the record as such a pool keeps
  it (the pool's share stopping at the retention less the deductible, a member's deductible changing often, a bulk
  load keyed on one day).

## Pre-ship check

- Call: keep the first $4,000,000 of each 2027 liability occurrence (the $4.0 million quoted attachment), 0.74
  expected 2027 occurrences above it and 1.25 above $3.0 million; curve log mean 10.18, log standard deviation 1.71
  on the 820 files of 2014 to 2021 (800 closed, 20 open suits with the layer paid), 108 stopped at the retention.
- Default path: the complete-sample fit to the closed files files $2.0 million; censoring alone $2.5 million;
  truncation alone $2.0 million; truncation and censoring at 2027 cost on the closed files $3.0 million; thresholds
  left nominal $4.0 million (convergent call); a common floor at $215,600 $4.0 million.
- 10/10 rules re-read against the built pack: the deciding quantity is the ground-up severity tail fitted through the
  record's own observation process (the field's construction); the mess (two administrators, converted numbers,
  member codes, text dates, the schedule's bulk load, the declarations' repeated totals) leaves the call and the
  components where they are when mishandled (asserted); the decisive step is analytical (the likelihood of a
  truncated, censored record over every file, the open suits being the censored observations a closed-file fit
  drops); no planted figure, no withheld rule, nothing flips on reading a field.
- Gates: 204 assertions with the three-rules block and SF1 to SF16; the independent verifier from target/ alone; two
  builds byte-identical; figures_check 93 figures; precut 49 checks; voice-check PASS; leak.py REVIEW (no LEAK); guard
  heart BLOCK in task-number order on task229 v3 and task231, both registered after this build's draw (06:41 and 17:18
  against 00:38 on 13 October), WARN in registration order (Gate G overuse, answered in the Draw).
- Deliverables: retention_2027.xlsx (the test and premium at seven attachments, the rated exposure by class, notes)
  and attachment_test_2027.png; target.zip from the final rebuild, 12 files.
- Card current: answer, spine rows, stump and driver at the built values.

## Tried and rejected

- DA05's seed world (a hospital trust's weekend day-surgery team and 52-week waits): no Descriptive task type in the
  client taxonomy fits that world's decision, so the number was redrawn inside Descriptive with a new world.
- A competing-risk design (time to resolution with withdrawals as non-returners): task134 v1 spent Kaplan-Meier with
  competing exits as the golden; rejected at the draw.
- High member deductibles across the board: the complete-sample fit and the truncated fit cancelled toward one
  attachment; rejected in the feasibility search.
- A $500,000 then $1,000,000 retention history: fewer capped occurrences and a better-seen tail, but the complete
  fit and the censoring-only fit crossed the line too close to the golden to sit on other attachments; the $250,000
  then $500,000 history kept (feasibility search, not rebuilt).
- A line of two expected occurrences a year: the censoring-only fit crossed close to the golden and shared its
  attachment in the search; one a year kept.
- An actuary's count anchored above $100,000 or $250,000 (inside the observed range): the tail's sampling error
  barely moved in the search and the nominal-threshold fit split from the golden onto $3.0 million; $25,000 kept.
- A ten-year window (2012 to 2021): the tail's sampling error fell only a little in the search; eight years kept.
- The legacy archive without the deductible, joined from the effective-dated history: the natural mishandling (the
  member's current deductible) moved the log mean by more than three in the search, not mess-neutral; both loss runs
  carry the deductible on each row and the history ships as a distractor.
- An ask on the open years' large occurrences (the underwriters' large-loss listing): immature counts set beside a
  fitted tail can bless the thinner curves, a validated decoy; dropped.
- Members declaring in thousands of dollars as the expenditure device: a thousandfold value shows on any sort;
  dropped for the repeated member figure.
- The expiring 2026 programme summary as a distractor: its premium and rated exposure would refute the repeated
  expenditure at a glance (an oracle for the ask); not shipped.
- The loop-0 design as the final rung: every occurrence of 2014 to 2021 forced closed by mid-2026 (the window named
  "the latest eight accident years in which every occurrence has closed"), so the likelihood of the record decided
  alone; at the author's request for a second layer the clamp was lifted for the suits past the retention, which
  the excess insurer goes on defending, and the closed-file construction became R3 ($3.0 million).
- Open suits carrying a case reserve to the rest of the pool's layer: reading them at payments to date as exact costs
  files $3.0 million, but censoring them at their payments (the ultimate is at least what is paid) gives the golden
  call with other counts at two decimals, a fork on the seven graded counts; the window's open suits have their
  layer paid in full (a suit past the retention has used the layer within about three and a half years of tender),
  so every reading of an open file is the same record.
- A window extended to the open years 2022 and 2023 with their reserves developed: the development of individual
  large files from aggregate triangles is the actuary's judgment, several defensible factors and several counts;
  the window kept at 2014 to 2021, where the only open files are the paid-up suits.

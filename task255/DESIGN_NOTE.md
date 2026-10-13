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
  cost every occurrence carries its own floor and its own ceiling.
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
   sheet per accident year) and keep the liability occurrences of accident years 2014 to 2021: 820, every one closed.
2. Take each occurrence's ground-up cost as its member's deductible plus the pool's payments (damages and defence)
   and bring it to 2027 cost with the claim cost index (the 2027 index over the accident year's).
3. Fit the policy's lognormal by maximum likelihood to the 820 costs at 2027 cost, the mean and standard deviation of
   their logs: log mean 12.08, log standard deviation 0.87.
4. Expected 2027 occurrences above each quoted attachment: the actuary's 228.7 above $25,000 times the fitted
   probability of exceeding the attachment over that of exceeding $25,000.
5. Take the lowest quoted attachment where that is one or fewer.

Ends on: $2.0 million
Golden: $4.0 million

## Stump sentence

The default path fits the policy's lognormal to the 820 recorded ground-up costs as if they were the whole curve and
ends on $2.0 million (0.60 expected 2027 occurrences above it), because the pool's record holds only occurrences that
exhausted their member's deductible and stops at the retention; censoring the 108 occurrences that reached the
retention still ends on $2.5 million, and only the fit carrying each deductible as truncation as well, both thresholds
at 2027 cost, files $4.0 million (1.25 occurrences above $3.0 million, 0.74 above $4.0 million).

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
  complete-sample fit of the recorded costs; it raises the expected count above $4.0 million from 0.21 to 0.74 and
  moves the call from $2.0 million (or $2.5 million) to $4.0 million.
- **Decisive step:** fitting the ground-up severity with the record's own observation process in the likelihood,
  truncation at each member's deductible and censoring at the pool's retention, at the cost level of the fit.
- **Not semantics:** every field reads plainly (the deductible, the pool's payments, the retention in the coverage
  memorandum), and a solver who reads them all and knows the capped occurrences stopped at the retention still files
  $2.5 million when it fits without the deductible's truncation: no field, code or definition says how the record's
  floor enters an estimate.
- **Not rule application:** the policy files the family (lognormal), the estimator (maximum likelihood), the record,
  the window, the cost level, the count formula and the line; it files no likelihood, and executing every filed rule
  on the recorded costs files $2.0 million; writing the likelihood of a deductible-truncated, retention-censored
  record is the step no rule performs.
- **Analyst test:** a strong analyst who cleans both loss runs, reads every field and rule, brings the costs to 2027
  cost and fits the lognormal by maximum likelihood to the 820 recorded ground-up costs files $2.0 million, and with
  the 108 capped occurrences censored files $2.5 million (the default path's Ends on: $2.0 million).
- **Estimand:** the trustees' risk financing policy fixes the curve as the distribution of what a member's liability
  occurrence costs from its first dollar, damages and defence together, at 2027 cost, over all the members' liability
  occurrences, estimated by maximum likelihood from the pool's record of the closed occurrences of accident years
  2014 to 2021, and the retention as the lowest quoted attachment whose expected 2027 count above it is one or fewer
  (risk_financing_policy_2026.pdf).
- **No decoy:** nothing is planted: no memo, draft, briefing or stakeholder figure states an attachment, a fit or a
  count; the loss runs are the administrators' own records and every row is a real occurrence.
- **No certified replay:** no certified or published figure is reproduced by the method: the actuary's exhibits file
  the index and the count above $25,000 and no severity parameter, count above any other amount or layer cost.
- **Lesson:** a loss distribution fitted to what a pool records is fitted to a window, floored at each member's
  deductible and cut at the retention; reading the window as the whole curve thins the tail exactly where an excess
  attachment sits. No build on file fits a size distribution through truncation and censoring.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R1, the 108 occurrences at the retention censored ($2.5m) | the memorandum says the excess insurer pays above the retention, outside the pool's system | 108 costs sit exactly at $250,000 or $500,000 | a solver used to limited losses censors them | none | no | no | readable |
| R2, each deductible as truncation, the capped costs read as exact ($2.0m) | the memorandum's tender sentence says how an occurrence reaches the pool, naming no truncation | the deductible is an ordinary loss-run column, no row predicate | not a default | none | no | no | silent |
| G (decisive), truncation at each deductible with censoring at the retention, both at 2027 cost ($4.0m) | no sentence names a truncation, a censoring or a likelihood; the policy says all occurrences, the memorandum how one reaches the pool | no flag or marker; the floor differs by member and year | the opponent's default fits the recorded costs, or censors only the visible caps | nothing scores a fit: no severity parameter, no count above any amount, no excess-layer experience ships | the battery sees no floor | a likelihood, no ratio or subtraction | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | attachment | from the first dollar, inclusive of the member's deductible | excess of the member's deductible | each count read above attachment plus deductible | policy 5.2 and the indications: attachments are stated from the first dollar of an occurrence, inclusive of the member's deductible |
| SF2 | occurrence | one row of either loss run | one claimant | same call | same call: both loss runs are one row per occurrence |
| SF3 | cost | the deductible plus the pool's paid damages and defence | damages only ($2.0m) | $2.0 million | policy 4.1: damages and defence costs together |
| SF4 | 2027 cost | the 2027 index over the accident year's | no trend ($2.5m) | $2.5 million | policy 4.2 names the index and the ratio |
| SF5 | the record | the legacy archive and the current run together | the current run alone (no attachment passes) | none | the extract notes: the archive holds the claims the legacy administrator closed before 1 July 2020, the current run every claim handled since |
| SF6 | closed occurrences of 2014 to 2021 | the 820, every one closed at 30 September 2026 | closed occurrences of every year ($4.0m) | same call | policy 4.2 names the years; convergent besides |
| SF7 | expected number above an attachment | 228.7 times the fitted tail ratio to $25,000 | counts read off the record | not a count of 2027 occurrences | policy 4.3 |
| SF8 | one or fewer | at most 1.0, inclusive | strictly under 1.0 | same call: 1.25 and 0.74 at $3.0m and $4.0m | same call |
| SF9 | thresholds' cost level | each deductible and retention at 2027 cost with the occurrence | left in each year's dollars | same call ($4.0m, 0.65 and 1.31) | same call |
| SF10 | the deductible of an occurrence | the one on the loss-run row, in force on the date of loss | the member's current deductible | not on any row | the memorandum: the deductible in force on the date of the occurrence applies; the loss runs carry it |
| SF11 | the quoted attachments | the seven in the broker's indications | an interpolated attachment | not quoted | policy 5.1: the lowest attachment quoted for the year |
| SF12 | rounding | counts unrounded until compared, shown to two decimals; premiums rounded once at the total | rounded before comparing | same call | same call |
| SF13 | the anchor amount | $25,000 from the first dollar at 2027 cost | at each year's cost | not the actuary's figure | the actuary's exhibit states its count at 2027 cost from the first dollar |
| SF14 | maximum likelihood | the maximum over the lognormal's two parameters, one optimum | a local optimum | same call | same call: five starting points reach one optimum (asserted) |

## Ladder

| Rung | Likelihood | Log mean, log SD | Expected 2027 occurrences above $3.0m and $4.0m | Call |
|---|---|---|---|---|
| R0 | the recorded costs as a complete sample | 12.08, 0.87 | 0.13, 0.04 | $2.0 million (0.60 above it, 1.59 above $1.5m) |
| R1 | the capped occurrences censored, no truncation | 12.14, 0.98 | 0.54, 0.21 | $2.5 million (0.95 above it, 1.82 above $2.0m) |
| R2 | each deductible as truncation, caps read as exact | 11.07, 1.22 | 0.24, 0.10 | $2.0 million (0.70 above it) |
| R3 | truncation and censoring, thresholds left nominal | 11.76, 1.23 | 1.31, 0.65 | $4.0 million (same call) |
| G | truncation and censoring at 2027 cost | 10.18, 1.71 | 1.25, 0.74 | $4.0 million |

- **Position:** the golden is the sixth of seven attachments; rung 0 takes the third. Every correction walks one way
  (up the attachments); only the decisive move reaches $4.0 million.
- **Margins:** at $4.0 million 0.74 (1.36x under the line); at $3.0 million, the runner-up, 1.25 (1.25x over it).
  R1's own pick is thin (0.95 at $2.5m; $3.0m under small variations): either is wrong.
- **Worth:** the decisive move (R1 to G) multiplies the expected count above $4.0 million by 3.6 and above $3.0 million
  by 2.3; the obvious correction (R0 to R1) moves the call one attachment.
- **Grid:** the four single-error cells (R0, R1, R2, R3) each file a quoted attachment: $2.0m, $2.5m, $2.0m, $4.0m.
- **Convergence asserted:** the same likelihood in each accident year's dollars (the curve's log mean moving with the
  index) gives 10.18 and 1.71; a fit truncated at one common floor ($215,600, the $100,000 deductible at 2014's
  factor) gives $4.0 million (0.90, 1.47); thresholds left nominal give $4.0 million.
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
the first dollar at 2027 cost (4.1), estimated by maximum likelihood from the pool's record of the closed occurrences
of 2014 to 2021 (4.2); the coverage memorandum files how that record came to exist (an occurrence reaches the pool when
its member's payments exhaust the deductible in force, and the pool records nothing above its retention), so the
likelihood of the record is the truncated and censored one, and its literal execution gives a log mean of 10.18, a log
standard deviation of 1.71 and $4.0 million. Every row of the fork table violates a quoted sentence or converges on
$4.0 million; the easy answers ($2.0 million, $2.5 million) come from an easier likelihood on the same estimand, not
from another reading.

## Oracles

- The actuary's 228.7 occurrences above $25,000: an input of every rung; it ties to nothing.
- The claim cost index: an input; it ties to nothing.
- The liability triangles (distractor): the pool's paid and incurred, net of deductibles and limited to its
  retention, by accident year and evaluation; the latest diagonal ties to the loss runs under every handling, and
  it carries no ground-up cost, no count above any amount and no severity parameter.
- The member deductible history (distractor): agrees with the deductible on every loss-run row; it scores no fit.
- The open accident years 2022 to 2026 in the current run: outside the policy's window and immature; the pack carries
  no development pattern to bring their counts to ultimate, so they score no fit (their counts at the retention are
  set beside each rung's expectation in `checks.py`).
- The ask layer: the declarations' department payroll is the benign twin of the repeated expenditure and ties to
  nothing; no 2026 rated exposure, premium or expiring programme ships (Tried and rejected).

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (lazy delta) | Realism |
|---|---|---|---|---|---|---|---|---|
| A, the 2027 premium of each quoted attachment | 7 | a measure every candidate carries that the call does not turn on | the trustees see each attachment's cost beside the policy's test | D6: an online declaration repeats the member's total operating expenditure, a member-level figure, on every department line (a paper declaration keyed by staff carries it on its first line only) | D1 (the consortium replay moves the vehicles in every premium); D8 (log rows effective after 30 September) | declarations (member, department, expenditure), schedule log (member, unit, type, effective date, VIN, serial), indications (two rates per attachment), roster (class), extract notes; 5 files, 12 columns | expenditure summed over lines and units counted raw: 3.43 times the golden at every attachment; expenditure once, units raw: 6.3 per cent high; expenditure summed, units right: 3.36 times; expenditure once, units deduplicated among those in force: 0.8 per cent high; the answer | a member portal flattens a header field onto each detail line; paper forms are keyed line by line |
| B, the rated exposure by member class | 14 (expenditure and vehicles, seven classes) | the audit trail of the premium's exposure | the board confirms the exposure the market rated | D1: on 3 March 2025 the fleet consortium's lists re-added sixteen members' fleets under the consortium's asset numbers; the pool's numbers were never deleted, and the consortium's later disposals reach the pool on its numbers only | D6 (expenditure); D7 (VINs keyed in lower case or with a space or dash; trailers and equipment with "NONE", "N/A", "UNKNOWN", "SEE SERIAL" or a blank VIN and a serial) | schedule log, roster, declarations, extract notes; 4 files, 9 columns | in-force unit numbers 7,104 (every class high); in-force units deduplicated by normalised VIN 5,818; raw-VIN dedup 5,889; VIN-only dedup (placeholders collapsed) 5,526; the answer 5,629 | a bulk load from a member's own system adds what it duplicates without closing the old records |
| C, the policy's test per attachment and the chart | 7 counts (in the call's question) and 5 chart parts | the construction | the call's own table | none | none | the golden fit | R0 and R1 values | the actuary's exhibit layout |

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
| A premiums at seven attachments | expenditure summed over department lines, units counted by in-force unit number | 3.43 times the golden | miss |
| B expenditure by class | summed over department lines | high in every class | miss |
| B vehicles by class | in-force unit numbers | high in every class | miss |
| C counts and chart | the golden's construction | right | outside |

Mirror leakage: about 8 per cent of the ask weight (the chart's two presence parts of 26 ask criteria; the mirror's
counts and chart values are R1's).
Pair ceiling: 36 (the cracker at about 56 with the call and its counts, the mirror at about 15; if the rubric grades
the seven counts as asks the pair is about 40).

## Build record

- Generator: `world.py`, `analysis.py`, `records.py`, `docs.py`, `golden.py`, `checks.py`, `verify.py`, `build.py`,
  `postprocess.py`; `python3 task255/generator/build.py` builds the pack, the goldens, `metadata.json` and
  `generator/figures.json`, runs the checks and the independent verifier, rebuilds into scratch for the byte
  comparison and cuts `target.zip`.
- Pack: 12 files in 4 formats; the vehicle schedule log 39,109 rows; the legacy archive 477 occurrences in six
  accident-year sheets; the current loss run 990 occurrences (343 of them in the fit's years); distractors the member
  deductible history and the actuary's triangles.
- Gates: 196 assertions with the three-rules block and SF1 to SF14; the verifier recomputes the fit (log mean 10.1769,
  log standard deviation 1.7102), the call, every count, the premiums and the class exposure from `target/` alone with
  its own parser and optimiser; two builds byte-identical; figures_check 88 figures; precut 49 checks; voice-check
  PASS; scrub audit clean on target and golden; leak.py REVIEW (no LEAK: the quoted attachments are declared stated
  inputs; the policy's own vocabulary; 26 schedule changes keyed before they take effect, allow-listed); guard
  surface 0 promoted; heart WARN (Gate G overuse, answered in the Draw).

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

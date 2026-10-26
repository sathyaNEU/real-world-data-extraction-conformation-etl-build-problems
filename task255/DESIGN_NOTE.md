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
- **Loop 2 (2026-10-26, after the portal's FAILED_TO_STUMP):** both portal responses filed the loop 1 golden, so the deductible-truncated, retention-censored likelihood is now the reflex rung. The world keeps its pool, files and asks; its liability occurrences now come from two severities, law enforcement liability (police civil-rights and use-of-force suits, a far longer tail) and the other four coverage parts, and the actuary's Exhibit 6 projects 2027 frequency above $25,000 on each group's own exposure (police department payroll 85.5, all other payroll 364.3). The retention history is $500,000 for 2014 to 2017 and $1,000,000 from 2018. The policy files the estimand (expected 2027 occurrences above each attachment from the actuary's expected number above $25,000 and the estimated probability) and the family (lognormal, maximum likelihood, the record of 2014 to 2021 at 2027 cost), never a single curve or a curve per part. One curve over the pooled record, the route both portal responses and both call-only probes took (p255a, p255b, 2026-10-26), files $2.0 million (0.92); a curve per group weighted by the two projections files $4.0 million (1.20 above $3.0 million, 0.83 above $4.0 million). The record rejects the pooled curve (likelihood ratio 158 on 2 degrees of freedom) and a common spread with a shifted log mean (29 on 1; it files $2.5 million). The executive director now sets the retention in the 2027 budget under the trustees' delegated authority (card: executive_team, budget_or_appropriation, local_government; the old forum, event and family were blocked by drift in the guard window). Heart WARN: the people's first names, Gate G, decision type and deliverable set repeat older builds, answered here: the people stay (no full name is reused), the Gate G and dial are this slot's own and the two files are what a retention decision produces.
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
   sheet per accident year) and keep every liability occurrence of accident years 2014 to 2021: 1,071 (8 still open).
2. Take each occurrence's ground-up cost as its member's deductible plus the pool's payments and reserves (damages and
   defence) and bring cost, deductible and retention to 2027 cost with the claim cost index.
3. Fit the lognormal by maximum likelihood to the 1,071 costs at 2027 cost, each truncated at its deductible and the
   25 at the retention censored there: log mean 8.09, log standard deviation 1.86.
4. Expected 2027 occurrences above each quoted attachment: the actuary's 432.7 above $25,000 (Exhibit 6's total)
   times the fitted probability of exceeding the attachment over that of exceeding $25,000.
5. Take the lowest quoted attachment where that is one or fewer.

Ends on: $2.0 million
Golden: $4.0 million

## Stump sentence

The default path fits one lognormal, deductible-truncated and retention-censored at 2027 cost, to all 1,071
occurrences of 2014 to 2021 and carries Exhibit 6's 432.7 occurrences above $25,000 by that curve, which ends on $2.0
million (0.9 expected 2027 occurrences above it), because law enforcement liability, under a third of the record and
every one of the 25 occurrences that reached the retention, runs a far longer tail than the other four coverage parts
and one curve takes its shape from the 757 others; giving law enforcement its own log mean but one spread still ends
on $2.5 million; fitting the two groups apart and carrying the actuary's 85.1 law enforcement and 347.6 other
occurrences by their own curves files $4.0 million (1.2 above $3.0 million, 0.8 above $4.0 million).

## Three rules

- **Task type:** claims-frequency-severity in Actuarial Science & Insurance, serving Descriptive & Distribution
  Analysis: the call reads the tail of the ground-up severity distribution at each quoted attachment.
- **Domain test:** the deciding quantity is the ground-up severity tail at each attachment, priced the way excess
  layers are priced: a severity per coverage whose losses differ in kind (law enforcement civil-rights and use-of-force
  suits against general, auto, public officials' and employment practices claims), each fitted through the record's
  deductible floor and retention ceiling and weighted by the actuary's frequency for that coverage on its own exposure.
- **Swap:** with a hospital's nouns ("how much of each patient's stay the ward funds before the regional fund pays")
  there is no coverage whose verdicts run a longer tail, no deductible floor, no retention ceiling and no quoted
  attachment to choose, so the estimator and the decision stop making sense.
- **Layer 1:** the legacy administrator's closed-claim archive (one sheet per accident year, title blocks, dates as
  text, currency formats) written by the system the pool left on 1 July 2020; the current administrator's loss run,
  claims open at the conversion carried under new numbers with the legacy number kept; coverage codes in two
  vocabularies (GL, AL, LEL, POL, EPL against GENL, AUTO, LAWE, PUBO, EMPL); member codes against member numbers;
  costs in each year's own dollars beside the actuary's index; for the asks, the vehicle schedule kept as a log since
  its opening load and a consortium's bulk load, and declarations taken online and on paper. Nothing is placed to be
  caught; every main-path item leaves the call and the components where they are when mishandled (asserted).
- **Layer 2:** estimation_fit: the severity of a pool whose occurrences come from two coverage kinds with different
  tails is a mixture, and one lognormal fitted through the record's truncation and censoring is shaped by the
  short-tailed majority; the record rejects one curve (twice the log likelihood difference 158.2 on two degrees of
  freedom) and one spread (28.8 on one); each group fitted apart and carried by the actuary's own projection for it
  moves the expected count above $4.0 million from 0.2 to 0.8 and the call from $2.0 million to $4.0 million.
- **Decisive step:** fitting the law enforcement occurrences and the other parts' occurrences apart through the
  record's own observation process and adding each group's projected 2027 occurrences above $25,000 carried by its
  own tail ratio, rather than one curve over the pooled record carried by the total.
- **Not semantics:** every field reads plainly (the coverage code, the deductible, the pool's payments and reserves,
  the status, the retention in the memorandum, the two projections in Exhibit 6), and a solver who reads them all,
  censors the capped occurrences and truncates at each deductible still files $2.0 million with one curve: no field,
  code or definition says whether the coverages share a severity.
- **Not rule application:** the policy files the family (lognormal), the estimator (maximum likelihood), the record,
  the window, the cost level, the expected-number formula from the actuary's count above $25,000, and the line; it
  files no curve count, no grouping and no likelihood, and executing every filed rule with one curve files $2.0
  million; testing whether the coverages share a severity and carrying each group's frequency by its own tail is the
  step no rule performs.
- **Analyst test:** a strong analyst who cleans both loss runs, reads every field and rule, brings the record to 2027
  cost and fits the lognormal by maximum likelihood with each deductible as truncation and the capped occurrences
  censored at the retention, then carries Exhibit 6's 432.7 by that one curve, files $2.0 million (0.9 above it);
  both portal responses to loop 1 and both call-only probes on this pack (p255a, p255b) took that route.
- **Estimand:** the trustees' risk financing policy fixes severity as the distribution of what a member's liability
  occurrence of the coverage year costs from its first dollar, damages and defence together, at 2027 cost, over all
  the members' liability occurrences, estimated by maximum likelihood from the pool's claims record for accident
  years 2014 to 2021, and the expected number above an attachment as the actuary's expected number above $25,000 times
  the estimated probability that an occurrence above $25,000 costs more than the attachment; the retention is the
  lowest quoted attachment whose expected 2027 number above it is one or fewer (risk_financing_policy_2026.pdf).
- **No decoy:** nothing is planted: no memo, draft, briefing or stakeholder figure states an attachment, a fit or a
  count; the loss runs are the administrators' own records and every row is a real occurrence; the actuary's
  exhibit projects frequency by coverage group because law enforcement exposure is police payroll, the way such
  studies are laid out, and states no severity.
- **No certified replay:** no certified or published figure is reproduced by any method: the actuary's exhibits file
  the index and the counts above $25,000 and no severity parameter, count above any other amount or layer cost.
- **Lesson:** a pool's liability severity is two curves, not one: the coverage whose suits run longest is a minority
  of the record and the whole of the tail, and one curve fitted through the record's floor and ceiling is shaped by
  the many short claims, thinning the tail exactly where an excess attachment sits.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 to R2, one curve without the full observation process ($2.0m) | the memorandum's tender and excess sentences | capped costs sit at $500,000 or $1,000,000 | the textbook truncated and censored fit fixes these | none | no | no | readable |
| R3, one curve, truncated and censored ($2.0m) | none names a curve count | the coverage column sits on every row | the reflex itself: both portal responses and both probes stop here | none | no | a likelihood | readable |
| Shift, own log mean, one spread ($2.5m) | none | the coverage column | a regression reflex once coverage is seen to matter | none | no | no | silent |
| G (decisive), the groups fitted apart, each carried by its own projection ($4.0m) | no sentence names a grouping, a mixture or separate curves; policy 3.1 says the actuary projects the two groups on their own exposures, which is how frequency studies are laid out | Exhibit 6 has two rows and a total; the loss runs carry a coverage code | not a reflex: the reflexes fit one curve to the record and carry the total | nothing scores a fit: no severity parameter, no count above any amount, no excess experience ships | the battery sees no defect | a likelihood per group and a weighted sum | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | attachment | from the first dollar, inclusive of the member's deductible | excess of the member's deductible | each count read above attachment plus deductible | policy 2.3 and the indications: attachments are from the first dollar, inclusive of the member's deductible |
| SF2 | occurrence | one row of either loss run | one claimant | same call | same call: both loss runs are one row per occurrence |
| SF3 | cost | the deductible plus the pool's paid and reserved damages and defence | damages only ($1.0m) | $1.0 million | policy 2.2: damages and defence costs together |
| SF4 | 2027 cost | the 2027 index over the accident year's | no trend ($2.5m) | $2.5 million | policy 4.2 names the index and the ratio |
| SF5 | the record | the legacy archive and the current run together | the current run alone (no attachment passes) | none | the extract notes: the archive holds the claims closed before 1 July 2020, the current run every claim handled since |
| SF6 | the record of 2014 to 2021 | the 1,071 files of those years, open and closed | the closed files of every accident year ($2.5m) | $2.5 million | policy 4.2 names the years |
| SF7 | expected number above an attachment | Exhibit 6's expected number above $25,000 times the estimated probability that an occurrence above $25,000 exceeds the attachment | counts read off the record | not a count of 2027 occurrences | policy 4.3 |
| SF8 | one or fewer | at most 1.0, inclusive | strictly under 1.0 | same call: 1.20 and 0.82 at $3.0m and $4.0m | same call |
| SF9 | thresholds' cost level | each deductible and retention at 2027 cost with the occurrence | the likelihood in each year's own dollars, the log mean moving with the index | same fit to the fourth decimal in both groups (asserted) | same call; thresholds left nominal against trended costs mixes two cost levels in one likelihood (a rung, $5.0m) |
| SF10 | the deductible of an occurrence | the one on the loss-run row, in force on the date of loss | the member's current deductible | not on any row | the memorandum: the deductible in force on the date of the occurrence applies; the loss runs carry it |
| SF11 | the quoted attachments | the seven in the broker's indications | an interpolated attachment | not quoted | policy 5.1: the lowest attachment quoted for the year |
| SF12 | rounding | counts unrounded until compared, shown to one decimal; premiums rounded once at the total | rounded before comparing | same call; every count, golden and five-part, at least 0.2 of the last place from its edge; every layer loss at least $20,000 from its edge | same call |
| SF13 | the anchors | Exhibit 6's 85.1 and 347.6 above $25,000 from the first dollar at 2027 cost, total 432.7 | at each year's cost | not the actuary's figures | Exhibit 6 states its counts at 2027 cost from the first dollar |
| SF14 | maximum likelihood | the maximum over each lognormal's two parameters, one optimum | a local optimum | same call | same call: five starting points reach one optimum in each group (asserted) |
| SF15 | an open file's recorded cost | the deductible plus what the pool has paid and still reserves | the deductible plus payments to date | same record (asserted): every open file of 2014 to 2021 is a law enforcement suit with its layer paid and nothing reserved | same call and same counts |
| SF16 | a vehicle on the schedule (the asks) | one vehicle by its VIN, or its serial without a VIN, on the schedule at 30 September 2026 by effective date, a consortium vehicle by its FMC- record | the last row across every number the vehicle holds, any number in force (6,387), every unit number in force (8,233) | other premiums and class vehicles | the extract notes file a vehicle's identity and how the consortium's numbers relate to the earlier ones |
| SF17 | "severity is modelled as lognormal" | a lognormal for each group the record separates | one lognormal for every occurrence ($2.0m) | $2.0 million | the record: one curve is rejected at twice the log likelihood difference 158.2 on two degrees of freedom and one spread at 28.8 on one (asserted, the design forcing the method); the policy files the family, never one curve (4.2, asserted) |
| SF18 | the groups | law enforcement liability and the other four parts, Exhibit 6's two projections | a curve per coverage part, the other four weighted by their share of the record above $25,000 | same call, the same seven counts at one decimal and the same seven layer losses to the hundred thousand (asserted) | same call |

## Ladder

| Rung | Likelihood | Expected 2027 occurrences above $3.0m and $4.0m | Call |
|---|---|---|---|
| R0 | one curve, the recorded costs as a complete sample | 0.15, 0.05 | $2.0 million (0.67) |
| R1 | one curve, the capped censored, no truncation | 0.20, 0.07 | $2.0 million (0.84) |
| R2 | one curve, each deductible as truncation, caps read as exact | 0.24, 0.12 | $2.0 million (0.61) |
| R3 | one curve, truncation and censoring at 2027 cost (the reflex, both portal responses, both probes) | 0.39, 0.21 | $2.0 million (0.89) |
| Shift | law enforcement's own log mean, one spread | 0.56, 0.31 | $2.5 million (0.79) |
| G_closed | the groups apart, the 8 open suits set aside | 0.75, 0.48 | $2.5 million (0.99) |
| G | the groups apart on every file, each carried by its own projection | 1.20, 0.82 | $4.0 million |

- **Position:** the golden is the sixth of seven attachments; the reflex takes the third. Every correction short of the
  decisive one stays at or below $2.5 million.
- **Margins:** at $4.0 million 0.82 (1.22x under the line); at $3.0 million, the runner-up, 1.20 (1.20x over it).
- **Worth:** the decisive move (R3 to G) multiplies the expected count above $4.0 million by 3.8 (0.22 to 0.82) and
  moves the call two attachments.
- **Convergence asserted:** the same likelihoods in each accident year's dollars give the same two fits; a curve per
  coverage part with the other parts weighted by their share above $25,000 gives every count at one decimal; a
  common floor at $215,600 files $4.0 million; an open suit read at its payments or at payments and reserves is the
  same record.
- **Flip:** with the other parts' projection held, $3.0 million would pass if Exhibit 6's law enforcement count were
  71.0 or lower; $4.0 million fails only above 103.2.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | severity over every members' liability occurrence; the fit's population the record of the 2014 to 2021 occurrences | filed literally, policy 4.1 and 4.2 |
| 2 | Unit of account | the occurrence | policy and indications per occurrence; one loss-run row each (SF2) |
| 3 | Attribution window | accident year by date of occurrence | the memorandum's occurrence basis; dates on every row |
| 4 | As-of dating | the loss runs at 30 September 2026 | C1: every uncapped fit occurrence closed by 30 June 2026; the 8 open suits have the layer paid (SF15) |
| 5 | Version basis | the record as it stands at the evaluation | C1: closed values are final; the archive was cut at conversion |
| 6 | Denominator | the probability above $25,000 in each group | policy 4.3 and Exhibit 6 |
| 7 | Weighting | one observation per occurrence; groups weighted by Exhibit 6 | maximum likelihood filed (policy 4.2); Exhibit 6 |
| 8 | Window length | eight accident years, 2014 to 2021 | policy 4.2 |
| 9 | Boundary inclusivity | "one or fewer" inclusive; a cost at the retention reached it | C1: no count within 0.18 of 1.0; no uncapped cost within $10 of a retention |
| 10 | Rounding path | counts unrounded until compared; premiums once at the total | SF12, same call |
| 11 | Tie-break | none: one lowest passing attachment | by construction |
| 12 | Maturity and censoring | censoring at the retention is the record's structure; the 8 open suits with the layer paid are censored there | the memorandum's facts |
| 13 | Order of operations | thresholds and costs at one cost level before the fit | C1: the accident-year-dollar likelihood gives the same fits (asserted) |
| 14 | Row order | none | C1: each fit is the same under shuffled rows (asserted) |
| 15 | Duplicate resolution | a converted claim appears once, in the current run, its legacy number kept | C1: no claim number in both runs (asserted) |
| 16 | Identity normalisation | member codes against numbers (not needed for the call); coverage codes in two vocabularies (the notes map them); VINs and serials for the asks | the extract notes; ask device D7 |
| 17 | Netting against gross | no recovery on any fit occurrence | C1: asserted none |
| 18 | Dimensional units | dollars; the index a ratio | the actuary's exhibit (2014 = 100.0) |
| 19 | Code and status semantics | "CL" in the archive, "Closed" or "Open" in the current run; five coverage parts, law enforcement one of them | the extract notes |
| 20 | Integerisation | none; vehicles are whole units | by construction |
| 21 | Clause scope | 4.2's window for severity, 4.3's anchor for frequency, 5.1 for the attachment | filed per clause |
| 22 | Forward window contents | 2027's counts above $25,000 and its index value | the actuary's exhibits file both |

## Literal reader

Executed word for word, the policy fixes severity as the distribution of all the members' liability occurrences from
the first dollar at 2027 cost (4.1), modelled as lognormal and estimated by maximum likelihood from the pool's claims
record for accident years 2014 to 2021 (4.2), and the expected number above an attachment as the actuary's expected
number above $25,000 times the estimated probability that an occurrence above $25,000 exceeds it (4.3); Exhibit 6
gives that expected number as 85.1 law enforcement and 347.6 other occurrences, 432.7 in all. The record of those
years holds 1,071 files, 8 of them open law enforcement suits whose payments have reached the retention; the
memorandum files how the record came to exist (truncation at the deductible in force, nothing above the retention).
The text files the family and the estimator and is silent on whether one lognormal or one per coverage group; the
record separates the readings (one curve rejected at 158.2 on two degrees of freedom, one spread at 28.8 on one), so
the design forces the groups, and their literal execution gives $4.0 million. Every other row of the fork table
violates a quoted sentence or converges on $4.0 million; the easy answers ($2.0 million, $2.5 million) come from a
model the record rejects, not from another reading.

## Oracles

- The actuary's 85.1 and 347.6 occurrences above $25,000: inputs of every rung (the reflex uses their total); they tie
  to nothing.
- The claim cost index: an input; it ties to nothing.
- The liability triangles (distractor): the pool's paid and incurred, net of deductibles and limited to its
  retention, by accident year and evaluation, with the counts tendered and closed; they carry no coverage split, no
  ground-up cost, no count above any amount and no severity parameter.
- The member deductible history (distractor): agrees with the deductible on every loss-run row; it scores no fit.
- The open accident years 2022 to 2026 in the current run: outside the policy's window and immature; the pack carries
  no development pattern to bring them to ultimate, so they score no fit.
- The ask layer: the declarations' department payroll is the benign twin of the repeated expenditure; the police
  department payroll in Exhibit 6 ties to the declarations' Police lines; no 2026 rated exposure, premium or
  expiring programme ships (Tried and rejected).

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (lazy delta) | Realism |
|---|---|---|---|---|---|---|---|---|
| A, each quoted layer's expected 2027 losses | 7 | the cost side of each attachment the call chooses among | the board sets each layer's expected losses beside its quote | the construction: each layer's expected losses carry each group's projection by its own severity between the attachment and the attachment plus the $10,000,000 limit | the limit (an unlimited excess cost is ruled out by the indications' limit) | the golden fit, the indications' limit | the pooled curve 3.3, 2.1, 1.5, 1.1, 0.8, 0.6, 0.4 million; the one spread and the groups on the closed files lower at every attachment; the answer | an excess layer's expected losses set beside its quote |
| C, the policy's test per attachment and the chart | 7 counts (in the call's question) and 5 chart parts | the construction | the call's own table | none | none | the golden fit | R3's values (3.3, 1.6, 0.9, 0.6, 0.4, 0.2, 0.1) and the one spread's (3.9, 2.0, 1.2, 0.8, 0.6, 0.3, 0.2) | the actuary's exhibit layout |

- **Loop 2 ask history:** the exposure asks (premiums by attachment, expenditure and vehicles by class) were solved to
  the dollar by both loop 1 portal responses and, after their devices were re-sited (D9 a member leaving on 31
  December 2026, D10 re-declarations on adopted budgets, D11 vehicles moved between members), by both loop 2 readers
  (21 of 21 figures each, 75 per cent of the ask figures). Exposure arithmetic does not hold against a careful
  reader, so the graded asks follow the severity construction (the ledger's lesson that decoupled asks pay only
  while their leakage is under a half). The declarations and the schedule log ship as distractors with D9 to D11 in
  them; the actuary's payroll ties to the 2027 members' last declarations.
- **Main population zero-counts:** no ask reads a file the call does not.
- **Hazard table:** the limit moves every layer loss; nothing else.
- **Referee:** none; the indications state the limit.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A layer losses at seven attachments | the golden's construction when the call lands | right | outside |
| C counts and chart | the golden's construction when the call lands | right | outside |
| A layer losses (mirror) | the pooled curve | 3.3 million against 8.3 at $1.0 million, off at every attachment | miss |
| C counts (mirror) | the pooled curve | off at every attachment | miss |

Measured by: task255/generator/pair.py (the readers' measured path, off the call, run on the built records).
Mirror leakage: 0 per cent of the ask weight (every layer loss and count of the pooled curve and the one spread
misses at the graded rounding, asserted).
Pair ceiling: 56.0 (the cracker at 100.0 on the call and every ask, the mirror at 12.0).

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

- Loop 2 (2026-10-26, after the portal's FAILED_TO_STUMP). World: each occurrence draws its coverage part first and
  its cost from that part's severity (law enforcement lognormal 8.6 and 2.45 at 2027 cost, the other parts 9.2 and
  1.35), 2,000 ground-up occurrences a year at the 2027 membership, the retention $500,000 for 2014 to 2017 and
  $1,000,000 from 2018; Exhibit 6 projects 85.0 law enforcement and 375.0 other occurrences above $25,000 on police and
  other payroll. Record: 1,071 occurrences (610 legacy, 461 current), 314 law enforcement with all 25 capped and the 8
  open suits, 757 others. Asks re-sited: D9 (a water-sewer district declared and then gave notice to leave on 31
  December 2026), D10 (eleven re-declarations on adopted budgets, the first in every class a cut), D11 (eight vehicles
  sold between members inside the pool, keyed as a change of member). Counts graded to one decimal (a curve per
  coverage part reproduces every count there; at two decimals it parted at $1.0 million). 281 assertions; the
  independent verifier fits both groups from target/ alone (8.5158 and 2.3713; 9.8851 and 1.1352) and reprices the
  exposure; two builds byte-identical; figures_check 93; precut 51; leak.py REVIEW; heart WARN; surface PASS;
  pair.py ceiling 35.4. Then, after stage 4's readers solved every exposure figure, the anchors moved to 85.1 and
  347.6, the premium ask gave way to each quoted layer's expected losses (a downstream ask), the quotes were
  rescaled by one market factor, same-day occurrences were separated; 282 assertions, pair.py ceiling 56.0.

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
- Loop 1 as shipped (portal 2026-10-26, FAILED_TO_STUMP): both responses filed USD 4,000,000 with 0.74 above it and
  the premium to the dollar. The deductible-truncated, retention-censored likelihood is the field's textbook reflex
  for a pool's loss run (readability test 3 fires on R2, R3 and G, recorded silent), and an open suit whose layer is
  paid reads as a censored observation to anyone who has already censored the caps, so the settlement selection
  added no rung. The observation-process likelihood is demoted below the new decisive step.
- Loop 2 prototype with five distinct coverage severities: the per-part fits were unstable (the truncated lognormal
  with a hundred or two rows a part ran its log mean far below the deductibles) and the groupings disagreed on the
  call; rejected for two severity groups, law enforcement against the rest, with the record grown to 2,000 ground-up
  occurrences a year.
- The $250,000 then $500,000 retention history under loop 2: a common spread with a shifted log mean was not rejected
  by the record (twice the log likelihood difference 2 to 14 on one degree of freedom across seeds) and filed another
  call, an open fork; the history raised to $500,000 and $1,000,000 and the record enlarged until it is rejected at
  28.8.
- The prototype anchors 85.5 and 364.3: the counts above $2.5 million and $5.0 million sat within a hundredth of a
  rounding edge; 84.7 and 364.7 kept the call and cleared every count's edge.
- Counts at two decimals under loop 2: a curve per coverage part, the other four weighted by their share of the record
  above $25,000, matched the golden at six attachments and parted at $1.0 million (4.59 against 4.57); counts graded
  to one decimal, the precision the record carries.
- The prototype's loss dates: every occurrence of an accident year drew the same day (a probe noticed it); fixed, no
  fit moved.
- Loop 1's ask layer under loop 2: both portal responses reproduced the $4.0 million premium to the dollar, so the
  repeated-total and consortium devices were solved; re-sited with D9, D10 and D11.
- The anchors 84.7 and 364.7 under the layer-loss ask: the golden and the five-part fit put the $1.0 million layer's
  expected losses either side of a $100,000 edge (8.24 and 8.25 million); 85.0 and 375.0 keep the call, the counts
  and every layer loss in one cell for both, at least 0.23 of the last place from each edge.
- The premium ask beside the layer-loss ask: a careful reader prices the exposure right, so a reader who lands the
  call keeps every ask and the pair ceiling sits at 65; dropped from the prompt, the quotes kept as the layers' terms.
- The loop 1 rate ladder at loop 2's severities: premiums a fifth of the layers' expected losses, a ratio no market
  quotes; one market factor of 7.3 on the ladder puts the expected losses at 58 to 64 per cent of each premium.
- Two same-member, same-day occurrences in the record (thirteen pairs before the fix): a careful reader merges them
  under the memorandum's one-occurrence clause; each member's second occurrence of a day is now dated the next free
  day, no fit moved.
- The anchors 85.0 and 375.0: a stage 4 reader read the two round projections as reverse-engineered; 85.1 and
  347.6 keep the call, every count and every layer loss in its cell (at least 0.2 of the last place from each edge).
- The same unit rate at $4.0 million and $5.0 million (a market minimum): flagged by two readers; the $5.0 million rate
  is now $222.50.

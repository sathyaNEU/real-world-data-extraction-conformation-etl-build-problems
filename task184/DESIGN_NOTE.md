# task184 design note (architecture 8: the saturated indicator)

Architectures 1 to 7 are spent and in the card's lineage. Architectures 3 to 7 were one family, a night-time
patrol slate ranked under a cap, and all five died on the same pair of horns that `stumping` 1.1c and 1.1h
name: where the data separate the candidate placements the analyst reads the fit and Gate F fails, where they
do not two placements are defensible and Gate C fails. Architecture 8 does not change the mechanism, it
changes the kind of call, which is the law that slot's own measurements produced (`stumping` 1.1i): in this
lane every build that shipped and held its call graded a recovered quantity or a decomposition, and every
build that died graded a ranking. So the cap and the slate are gone and the call is one recovered count.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task184.json` (v8), registered 2026-10-26. `guard.py check`
  carries no BLOCK; nearest driver on file 0.07 (task190 lineage, task132), which is the lowest this slot has
  drawn. Two WARNs, both answered below.
- **Pairing.** accounting-audit-forensic / audit-testing-sampling, client domain
  banking-credit-financial-risk, objective anomaly-detection, shape 03 (bridge between totals, each trading
  unit a reconciling item), decision type `quantity_figure`, answer unit `count`. The domain carries one card
  in 296 and the subdomain none; `auditor` has decided two prompts in the corpus and `audit_or_inspection` has
  forced four.
- **Strategy.** `grain_or_unit`, `layer2_family: estimand_identification`,
  `layer2_pattern: own:saturated-indicator-inversion`.
- **World.** Drumcondra Provisions Group, a foodservice distribution group in the Republic of Ireland: twelve
  trading units (nine regional depots, a national contracts business, a central bakery and a group services
  unit) posting into one shared general ledger. Postings reach the ledger four ways: an EPOS interface for
  depot counter sales, a route-accounting interface that posts each van's day as one voucher, a payables
  interface, and manual journals. Group internal audit runs a continuous-monitoring ruleset over the ledger
  nightly and the platform writes one verdict per journal entry.
- **People.** Drawn from `guard.py names --geo Ireland --seed 184`: Ruairi Barnett (group head of internal
  audit), Alana Marnan (continuous monitoring), Fergus Rynne (group financial controller), Myles Connaughton
  (route accounting). No name typed.
- **Forcing event.** The internal audit plan for the year is being sized, and the sample sizes and the
  unit-by-unit allocation of testing turn on how many postings in the population trip the ruleset.
- **Forward facing.** The window is the financial year to date, which is open: the call is a quantity about a
  window not yet closed, so the default holds and no retrospective reason is owed.

**Data-native sentence.** The purchase ledger posts one voucher per supplier invoice and the migrated delivery
rounds one per docket, while branch EPOS posts a whole trading day under one voucher and payroll a whole
run, so the number of postings behind one journal entry in this ledger runs from 1 to 2,347 inside the same
trading unit; the monitoring platform
records its verdict on the voucher, so the same indicator means "one posting tripped the ruleset" on a manual
journal and "at least one of 2,347 did" on a branch trading day, and the map between the two is saturating.

**Why the line detail is not a planted organ.** The postings behind an entry come from the voucher's own item
count, which every route to the answer needs: the easy route needs it to total the group's postings at all,
and the question is asked per posting, so the count is forced by the question rather than by the decisive
step (`leak-check` readability test 7, the multi-purpose escape). Double-entry is what makes it recoverable:
the posting interfaces write each source document as its own balanced set of lines, so the voucher's internal
composition is legible from its line structure, and the entry header carries the item count a posted voucher
always carries.

## Default path

A competent analyst with every field read correctly and every filed rule applied:

1. Reads `monitoring_exceptions.csv` (the platform's exception register, one row per flagged journal entry)
   and `rule_catalogue.pdf`, and keeps the rules whose stated evaluation grain is the posting rather than the
   voucher.
2. Joins the register to `journal_entries.csv` on `entry_id` to get the trading unit, the period and the
   entry type, and filters to the financial year to date.
3. Reconciles the register against the platform's own monthly summary and ties.
4. Groups by trading unit, counts flagged entries, and reports that count as the number of postings that
   tripped the ruleset, bridging it to the group total.

**Ends on:** 7,481 postings for the group, with the twelve unit figures running 131 to 920.

A sharper analyst notices the entry is not the posting, takes the flag rate per entry and grosses it up by
the group's posting count.

**Ends on (the sharper route):** 29,234 postings for the group.

**Golden:** 14,989 postings for the group, which is 15,000 to the nearest thousand, with the twelve unit
figures 1,700, 2,100, 1,500, 1,300, 1,100, 1,200, 1,400, 1,000, 1,600, 900, 800 and 400 to the nearest
hundred, summing to 15,000.

Both default figures are wrong by a factor, not a margin: the flag count is 0.50 times the golden (49.7 per
cent of the generator's clean truth) and the grossed-up rate 1.95 times it (194.4 per cent of clean truth).

## Stump sentence

The analyst reports the monitoring platform's 7,481 flagged entries as the number of postings that tripped
the ruleset for the year to date (or 29,234 from the entry flag rate grossed up by the group's postings); the
step that lands there is treating the entry verdict as one observation of one posting, when it is an
indicator that fires once however many of the voucher's postings trip the rule, so the count has to be
recovered by inverting one minus the complement raised to the postings on the entry, entry by entry, with the
rate estimated on each trading unit's own population.

## Three rules

Task type: fraud-aml-detection in the client taxonomy, which serves Anomaly Detection and Diagnostics; audit-testing-sampling in the house domain, which is the card's subdomain. The build is rule-based transaction
monitoring: a ruleset evaluates postings, the platform raises an alert, and the question is how many postings
actually tripped a rule rather than how many alerts were raised. That gap between the alert's grain and the
monitored item's grain is the standing measurement problem of transaction monitoring, and on the audit side the
same figure is the population deviation rate an attribute test is sized against.

Domain test: the deciding quantity is a population deviation rate at the item subject to the control, the
figure an auditor estimates to size an attribute sample and to allocate testing across components of a group.
The field's own method defines the sampling unit as the item the control operates on, and here the evidence
arrives at the accounting document's unit instead, so the rate has to be recovered from the document-level
indicator before any sample is sized.

Swap: put shipping container for journal entry and damaged carton for tripped posting. The arithmetic still
inverts, but nothing then says what the unit of observation ought to be, because only an audited population
has a standard that defines the item subject to the control; and nothing makes the container's internal
composition recoverable, because only double-entry writes each source document as its own balanced set of
lines. The swap leaves a counting exercise with no reason to prefer either unit and no route to the fan-out.

Layer 1: the ledger's own mess, none of it placed to be caught. The EPOS interface changed its voucher
convention mid-year (one voucher a day per depot, then one a day per till), so the posting fan-out per entry
steps down at the cut-over; the route-accounting interface posts in the depot's local time while the platform
stamps its verdicts in UTC, so a van's day straddles the period boundary twice a year; the payables interface
restates a supplier's accruals in a later period without reversing the first posting, so the same source
document appears under two entries; unit codes were renumbered at the half-year and the register carries the
old ones; and the group's period calendar is a 4-4-5 fiscal month against the platform's calendar months.

Layer 2: `estimand_identification`. The decisive choice is what the rate is a rate of, and therefore what
the observation is: the platform's row is a voucher, the decision's unit is a posting, and the map from the
posting rate to the voucher-level indicator rate saturates with the postings on the voucher, so no rescale of
the indicator count recovers the posting count.

Decisive step: recover the population deviation rate at the posting by inverting the voucher-level
indicator, entry by entry, over each trading unit's own population, rather than rescaling the indicator
count to or from the voucher population.

Not semantics: every field reads exactly as it is labelled and the analyst reads it right. The register's
row is a flagged journal entry and says so, the entry header's item count is the postings on the voucher and
says so, and the rule catalogue states each rule's evaluation grain. Reading all three correctly is what
produces the two default figures: knowing that the row is a voucher and that the voucher holds up to 2,347
postings is exactly what licenses "flags over entries, times postings", which is wrong by 1.95 times. The answer does
not turn on any field's meaning; it turns on the shape of the map between the two units.

Not rule application: no filed rule or procedure performs the recovery. The rule catalogue says what each
rule tests and at what grain; the monitoring platform's documentation says it retains a verdict per entry;
neither says, and no shipped sentence says, that the indicator saturates or how to invert it. Executing every
stated rule produces the register and the two default figures, which is what the analyst test files.

Analyst test: a strong analyst reconciles the register, counts flagged entries per unit and reports 7,481 for
the group, or grosses the entry flag rate up to 29,234. Executed in `checks.py` on the generator's clean
truth, both routes reproduce those figures and the golden reproduces 14,989, which is 15,000 as graded.

Estimand: the number of postings in the group's general ledger, in the financial year to date, that trip
the continuous-monitoring ruleset, counted for each trading unit on that unit's own population and summed to
the group. Filed in the prompt's question and in `exception_population_bridge.xlsx`'s scope note; the unit of
estimation is part of the WHAT, which is why the prompt asks for the figure per trading unit and for the
group (`determinism-check` section 1).

No decoy: nothing is planted to be caught. There is no copied block, no hidden rule, no memo or briefing
arguing a figure, and no stakeholder number written to be overturned. Every artifact speaks in entries,
because that is what the platform records; none states a posting count.

No certified replay: no certified or published figure is reproduced by the method, and no artifact blesses
either route. The platform's monthly summary ties to the register under every route, because both are counts
of entries.

Lesson: that an indicator recorded on a container of items is not an observation of an item, so the rate
the decision needs is recovered by inverting the container-size map rather than by rescaling the count, and
that the rescale is wrong by a factor whichever direction it is taken. No build on file teaches it: the
corpus's nearest drivers sit at 0.07.

## Measured on the built world

Every figure below comes from the generator at `SEED = 184008`, measured over FY26 P1 to P9: 313,678
journal entries carrying 1,225,763 postings across twelve trading units, with each unit's rate solved by
bisection so its recovered figure lands on a bin centre. `golden` is the estimand executed literally;
`clean truth` is the generator's count of postings that actually trip the ruleset, which nothing ships.

| Route | Figure | Of the golden | Of clean truth | Distance from the graded bin |
|---|---|---|---|---|
| rung 0, flagged entries as the platform reports them | 7,481 | 0.50x | 49.7% | 50.1% |
| rung 1, the entry flag rate grossed up to the postings | 29,234 | 1.95x | 194.4% | 94.9% |
| rung 2, the inversion applied once on the mean entry size | 7,548 | 0.50x | 50.2% | 49.7% |
| counting the register's rule hits rather than its entries | 12,655 | 0.85x | 84.1% | 15.6% |
| every posting on a flagged voucher | 798,238 | 53.3x | 5,307% | outside the floor |
| **the golden** | **14,989** | 1.00x | **99.66%** | **0.1%, eleven from the centre** |

**The three conditions a corrected route owes** (`stumping` 1.1f), each asserted separately in `checks.py`:

1. **The default path lands outside the bin.** Every rung sits 49.7 per cent or further from the graded bin,
   and the nearest wrong route of any kind, counting rule hits, sits 15.4 per cent out, against the 6 per
   cent `C4` floor.
2. **Every licensed estimator lands inside the bin.** Per unit then summed, the maximum likelihood estimate
   is 14,989, method of moments 15,006 and the complementary log-log form 15,102, a spread of 113 postings
   against a half-bin of 500. At unit level the worst spread is 44.3 postings against a half-bin of 50, the
   median 13.1, and **all twelve units and the group total have every licensed estimator rounding to one
   bin**. Each unit's golden sits within 0.20 of its bin centre and the group's within 0.02 of its own.
3. **The golden is strictly more accurate against clean truth.** 99.66 per cent, against 49.7 per cent for
   the default path. The correction is 147 times closer, not marginally closer.

**The grouping fork, closed twice.** Estimating one rate for the whole group and estimating a rate per unit
are both defensible, and on an earlier tuning of this world, where the unit rates spanned six times, they
differed by 2.9 per cent on the group total with the pooled figure 187 postings from a bin edge. Two
closures now hold together. The estimand files the unit of estimation, which is WHAT and not HOW
(`determinism-check` section 1), and the prompt asks for the figure per trading unit and for the group, so
the literal reading fixes the grouping. And the rates were reassigned into a narrow band, 0.91 to 1.81 per
cent, which is what controls the concavity bias: the pooled maximum likelihood estimate is now 14,712, a
gap of 277 postings or 1.85 per cent, and the pooled method of moments and complementary log-log figures are
14,798 and 14,888, so **all six estimates, pooled and per unit, sit inside the 15,000 bin**. A solver who
pools lands in the same bin.

**Why the saturation and the identification do not fight.** This is what killed architectures 3 to 7: the
structure that made the easy route wrong was the same structure that destroyed the answer's determinacy.
Here they live in different entries, because a general ledger is heavy-tailed in entry size and the tail has
a cause. The purchase ledger posts one voucher per supplier invoice and the migrated delivery rounds post
one per docket, so 23 per cent of postings sit on vouchers of exactly one posting, which is 93 per cent of
all entries and is what identifies the rate. Branch EPOS posts a whole trading day under one voucher and
payroll a whole run, so 66 per cent of postings sit on 1,836 vouchers of 150 to 2,347, which is where the
platform's verdict hides the mass. Tightening the identification does not loosen the saturation, because
they are different streams of the same ledger.

**The no-op that makes rung 2 attractive.** For a small indicator rate the inverse of the pooled indicator
is the rate over the mean entry size, and the mean entry size is the postings over the entries, so the two
cancel: inverting once on the aggregate returns 7,548 against a flag count of 7,481, a difference that is
the second-order term alone. A solver who spots the saturation but corrects at group level gets back the
number it started with and reads two agreeing routes as corroboration.

## Guard WARNs, answered

- `three_rules.strategy_risk` on `grain_or_unit`: the risk the rule names is that a grain stump decides on
  reading a field or applying a stated rule. Here the analyst test is executed, not argued, and it reads every
  field right: the register's row is labelled a journal entry, the item count is labelled the postings on the
  voucher, the rule catalogue states each rule's grain, and reading all three correctly is precisely what
  licenses the grossed-up entry rate, which is wrong by 1.42 times. What defeats the easy route is that the
  rescale between the two units is not a division.
- `test.same_puzzle_older` against task151 and `test.same_driver_older` against task464 v2: differentiation
  lines are in the card.

**What stage 2 owes:** the readability screen with the decisive row silent, the semantic fork table, the
three-to-five rung ladder with its grid and worth arithmetic, the 22-axis closure table, the literal reader
line, the oracle list, the ask sheet with its cracker and mirror sheets, and `prompt.txt` through
`voice-check.py`; then `precut.py` exit 0.

## Readability screen

Six tests per rung (`stumping` 2.1). The decisive row must read `silent`.

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the flag count as the platform reports it | names it (the platform's documentation says it writes a verdict per entry) | the register's row is a flagged entry | yes, the opponent's first group-by | the monthly summary ties to it | the battery reconciles it | yes, a count | readable |
| 1 the entry flag rate grossed up to the posting population | no sentence; the postings per entry are on the voucher because the question is per posting | `item_count` is a column, and every route needs it | yes, the reflex once the unit mismatch is seen | nothing scores it | the battery passes it | yes, a ratio times a total | readable |
| 2 the inversion applied once, on the group's mean entry size | no sentence | no column isolates it | the correction a careful solver reaches for | nothing scores it | invisible to the battery | no, a root of a power | readable |
| 3 the inversion per entry, with the rate on each unit's own population **(decisive)** | no sentence anywhere states that the indicator saturates, or how to invert it | no column, no key, no marker; `item_count` serves every route including both wrong ones | no: the measured reflexes land on rungs 0, 1 and 2 | no control, summary or corpus scores it; every artifact counts entries and ties under every route | the battery reconciles the register, ties the summary and finds nothing | no: the step is a per-entry inversion summed over 313,678 entries, not a subtraction, ratio or half of a reported figure | `silent` |

**The one tell, named.** A solver who reaches rung 2 finds that inverting on the mean entry size returns the
flag count it started from, because for a small indicator rate the inverse is the rate over the mean size and
the mean size is the postings over the entries, so the two cancel identically (7,548 against 7,481, the gap
being the second-order term alone). That no-op is a real tell: a diligent solver sees that the correction
changed nothing. It is kept, for two reasons. It announces that something is wrong, not what to do about it,
so discovery and remedy are different acts (`supplemental-stumping` 1.0 applied to the call). And it makes
rungs 0 and 2 corroborate each other, so the common outcome is a solver who takes two routes, gets one answer
and files it with more confidence than it deserves.

## Semantic fork table

| id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | posting | one source document's entry into the ledger, the unit `item_count` counts | a ledger line (debit or credit) | 15,308, the same graded figure | `gl_data_dictionary.pdf` names `item_count` as the source documents posted under the voucher and `line_count` separately, and the two readings converge anyway, because the indicator is the same and the inversion rescales with it: 15,308 is 1.02 times the golden and rounds to the same 15,000 (`C1`, asserted on the figure and on all twelve units) |
| SF2 | tripped the ruleset | the ruleset's rules evaluated the posting and one or more fired on it | the entry was flagged | 7,481, which is rung 0 | the question asks for postings, and `monitoring_platform_guide.pdf` states the platform evaluates each posting on the voucher and writes one verdict for the voucher |
| SF3 | this financial year to date | the group's 4-4-5 fiscal periods FY26 P1 to P9, as `period_calendar.csv` dates them | calendar months October 2025 to June 2026 | same call: `period_calendar.csv` aligns FY26 P1 to P9 exactly with the extract window, and the entries in the two differences net to zero flagged entries (asserted on figure and counts) | C1 |
| SF4 | trading unit | the twelve units in `trading_unit_register.csv` as they stand at the extract | the pre-renumbering codes the register carried before the half-year | same call at group level; per-unit figures differ | `trading_unit_register.csv` carries `code_from` and `code_to` with effective dates and the extract date is filed |
| SF5 | the ruleset | the nine rules `rule_catalogue.pdf` marks live in FY26 | all eleven rules listed, including the two marked withdrawn | same call | `rule_catalogue.pdf` dates each rule's withdrawal, and the two withdrawn rules fired on zero FY26 entries, so both readings select the same rows (`C1`, asserted on the figure and the counts) |
| SF6 | the group | the twelve trading units, group services included | the nine depots only, the trading units proper | same call for each unit; the group total differs | the question asks for each trading unit and for the group, and the register lists twelve |
| SF7 | rounding path | round each unit's figure to the nearest hundred and the group's own figure to the nearest thousand, each from its own unrounded value | sum the rounded unit figures to get the group | same call: the rounded units sum to exactly 15,000 and the group's own unrounded figure, 14,989, rounds to 15,000 | `C1`, asserted |

Every row is asserted in `generator/checks.py` by its id.

## Ladder

Four rungs, each a complete pipeline from the raw files, each terminating on a figure a competent analyst
would file and defend. Graded quantity: the group's postings that trip the ruleset in FY26 to date.

| Rung | The analysis | Figure | Of the golden | Distance from the graded bin | Dies to |
|---|---|---|---|---|---|
| 0 | Reconcile the exception register to the platform's monthly summary, group by trading unit, count flagged entries | 7,481 | 0.50x | 50.1 per cent outside | `item_count` on the voucher: one branch EPOS entry carries up to 2,347 postings, so the count is of vouchers |
| 1 | Take the flag rate per entry and gross it up by the group's postings | 29,234 | 1.95x | 94.9 per cent outside | the indicator cannot exceed one per voucher, so the entry rate is an upper bound on the posting rate, not an estimate of it |
| 2 | Invert the indicator once, on the group's mean entry size | 7,548 | 0.50x | 49.7 per cent outside | the inverse of a mean is not the mean of the inverses: the entry-size distribution is heavy-tailed (1 to 2,347), so the single inversion is algebraically the flag count again |
| 3 **(decisive)** | Invert the indicator entry by entry, estimating the rate on each trading unit's own population, then sum | 14,989 | 1.00x | the golden, 11 from the bin's centre | nothing: this is the estimand executed literally |

**The arithmetic.** Position: rung 0 is the default path and is the figure the reflex group-by files.
Separation: every rung sits 49.7 per cent or more from the graded bin, against the 6 per cent `C4` floor, and
0.50x to 1.95x of the golden, so every rung is wrong by a factor. The nearest wrong route of any kind is
counting the register's rule hits rather than its flagged entries, 12,684, and that sits 15.4 per cent from
the bin. Worth on the graded quantity: refusing rung 0 is worth 7,508 postings (50.1 per cent of the golden),
rung 1 is worth 14,245 (95.0 per cent) and rung 2 is worth 7,441 (49.6 per cent); nothing but the decisive
move changes the figure at all.

**Dominance.** Each rung dies to exactly one shipped fact, named above, and no rung dies to two. Rung 2 is
not reachable by fixing a loop in rung 1, and rung 3 is not reachable by fixing a loop in rung 2: it needs
the per-entry form, which is a different computation over 313,678 rows rather than a corrected constant.

**The grid.** Three live axes: the unit the rate is taken on (voucher or posting), the form of the map
(linear or saturating), and where the map is applied (once on an aggregate, or per entry). Eight cells.

| Unit | Map | Applied | Figure | Named |
|---|---|---|---|---|
| voucher | linear | aggregate | 7,481 | rung 0 |
| voucher | linear | per entry | 7,481 | rung 0, identical by construction |
| voucher | saturating | aggregate | 7,548 | rung 2 |
| voucher | saturating | per entry | 7,481 | collapses to rung 0: inverting an indicator that is already per voucher returns the indicator |
| posting | linear | aggregate | 29,234 | rung 1 |
| posting | linear | per entry | 798,238 | outside the floor: it credits every posting on a flagged voucher, 53.3x the golden, and no analyst files it |
| posting | saturating | aggregate | 7,548 | rung 2 |
| posting | saturating | per entry | 14,989 | the golden |

No cell is unnamed and no single-error cell is infeasible. The grid is not saturated: the two
`per entry` cells on the voucher unit collapse into rung 0, which is why four rungs and not eight.

## Closure table

| # | Axis | The reading taken | Closure |
|---|---|---|---|
| 1 | Population | every journal entry posted to the group ledger in FY26 P1 to P9, all twelve trading units, every live rule | estimand filed in the prompt's question and the workbook's scope note; entries posted after the extract are stated as out of scope in the extract manifest |
| 2 | Unit of account | the posting (one source document's entry), not the voucher and not the ledger line | SF2 rules out the voucher at a factor (`C4`, 0.50x); SF1 shows the ledger line converges (`C1`, 1.02x, same bin) |
| 3 | Attribution window | the fiscal period the entry is posted in, per `period_calendar.csv` | SF3, `C1`: FY26 P1 to P9 and January to September differ by entries that carry zero flags, asserted on figure and counts |
| 4 | As-of dating | the extract date, 2026-07-03, filed in the manifest; the unit register read at that date | SF4; the register's effective dates are filed and the extract date is stated once |
| 5 | Version basis | the entry as posted, including later restatements as their own entries | the payables restatement is an ask device and sits in FY25, outside the window; asserted zero in the main population |
| 6 | Denominator | the group's postings in the window, the sum of `item_count` over in-scope entries | the question asks for a count, not a rate, so no denominator is graded; `item_count` is defined in the dictionary |
| 7 | Weighting | each trading unit's rate estimated on that unit's own population, summed to the group | the estimand files the unit of estimation (WHAT, not HOW, `determinism-check` section 1), and the prompt asks per unit and for the group; `C1` as well, since pooling converges to within 0.07 to 0.35 per cent |
| 8 | Window length | the nine fiscal periods to date, not a trailing twelve months | the question says this financial year to date and the calendar dates it |
| 9 | Boundary inclusivity | periods inclusive at both ends | `C1`: no entry posts on P1's first or P9's last day with a flag, so no reading sits on the edge (asserted) |
| 10 | Rounding path | each unit's own unrounded figure to the nearest hundred, the group's own unrounded figure to the nearest thousand | SF7: both roundings stated separately in the prompt, and both figures stated, so the rounded units summing to 22,200 is not an alternative reading of the group figure |
| 11 | Tie-break | none: the graded figure is a count, not a ranking | no tie exists; the chart orders units by their figure and no two units round to the same hundred |
| 12 | Maturity and censoring | every entry in the window is fully evaluated; the unevaluated entries are an FY25 ask | `monitoring_run_log.csv` shows complete FY26 coverage, asserted; the gaps are in FY25 |
| 13 | Order of operations | invert per entry, then aggregate; never aggregate then invert | this is the decisive step itself and is not filed; rung 2 is the wrong order and is 51.5 per cent outside the bin |
| 14 | Row order | file order cannot move the result | `C1`, asserted over six permutations of the entry file: the inversion is a sum over entries and the likelihood is order free |
| 15 | Duplicate resolution | the register carries exactly one row per flagged entry, with the rules that fired in a `rules_fired` column | asserted unique on `entry_id`, so counting rows and counting distinct flagged entries cannot differ; 2,190 entries had more than one rule fire and splitting `rules_fired` would count 12,684 rule hits, which is 15.4 per cent from the bin |
| 16 | Identity normalisation | the unit register's effective-dated codes map the register's old codes to the twelve current units | SF4; `C4` at unit level, and the group figure is invariant to the mapping (asserted) |
| 17 | Netting against gross | nothing nets: a count of postings has no sign | no reading nets |
| 18 | Dimensional units | `item_count` counts source documents throughout, on every interface | asserted equal to the distinct source-document references on the entry's lines, for every entry in the line-detail extract |
| 19 | Code and status semantics | the register's `verdict` is `exception` or `cleared`; only `exception` rows are flags | dictionary semantics, and never the stump: both readings are counts of entries and both sit outside the bin |
| 20 | Integerisation | postings are whole; the inversion's output is rounded once at the end | the rounding is stated in the prompt and applied once per graded figure |
| 21 | Clause scope | the rule catalogue's withdrawal dates scope which rules are live in FY26 | SF5, `C1`: the two withdrawn rules fired zero times in FY26 |
| 22 | Forward window contents | FY26 runs to 2026-09-27 and P10 to P12 are still to run, so the year is open; every entry inside P1 to P9 is posted and evaluated and nothing is forecast | the extract manifest files the extract date, 2026-07-03, and states that P9 closed on 2026-06-28 |

## Literal reader

A reader who executes the prompt and every filed definition word for word, inferring nothing, is asked for
the postings that tripped the ruleset per trading unit and for the group; `gl_data_dictionary.pdf` defines a
posting as one source document's entry under a voucher and `item_count` as the number of those,
`monitoring_platform_guide.pdf` states the platform evaluates each posting on the voucher and writes one
verdict for the voucher, and `period_calendar.csv` dates the window. Executing that literally gives the
number of postings that fired a live rule, per unit on that unit's own population, which is 14,989 for the
group, graded as 15,000, and the twelve unit figures. No filed sentence states how to recover it, and no literal reading
reaches rung 0, 1 or 2: each of those is an easy method on the same literal estimand, which is where the
easy answer must come from (`determinism-check` section 2, test 3).

## Oracles

| Artifact | What it confirms | Reading on the wrong path |
|---|---|---|
| `monitoring_platform_guide.pdf` monthly exception summary | the register is complete: flagged entries per unit per period | ties under every route, because both the summary and the register count entries, so rung 0 is confirmed exactly as the golden is |
| `gl_control_totals.csv` | debits equal credits and the entry count per period | ties under every route; carries no posting count and no exception figure |
| `trading_unit_register.csv` | the twelve units and their effective-dated codes | ties under every route |
| `period_calendar.csv` | the 4-4-5 period dates | ties under every route |

No artifact ties only under the golden and none ties only on a wrong read. Nothing ranks the units on the
decision question, and no shipped artifact states a posting count for any unit or for the group, so Gate G
holds with every wrong number deleted: the difficulty is that the pack states entry counts truthfully and
the question asks for postings. The ask layer's referee (`payables_control_account.csv`) arbitrates ask 1
only and carries nothing the call reads.

## Ask sheet

Three asks, all on FY25, which is outside the call's window, so every device row sits outside the main
population by construction.

**Ask 1, the payables accrual reconciliation.** Figures: per trading unit (12), the subledger's supplier
accrual balance at the FY25 close, the ledger control account balance, and the difference; plus the
reconciling items. H18 home: an input reconciled to another system's total, the gap made of devices. Use:
internal audit decides whether to rely on the payables reconciliation control. Primary device: D2, a
restatement posted in a later period without reversing the first, so the same source document carries an
accrual under two entries and the naive sum double-counts (seen, repaired right only if the solver reads the
restatement chain, not the period). Hazards: D7 the half-year unit renumbering, present in the subledger
only; D9 a control total true in its own scope (the subledger's own trial balance ties to itself under the
double count). Files: `payables_accruals_fy25.csv`, `payables_control_account.csv`,
`trading_unit_register.csv`, `period_calendar.csv`, `gl_data_dictionary.pdf`, plus the FY25 journal entries,
the supplier register and the restatement log: eight files, eleven columns on the golden's path. Stops: the
naive sum (double counts), the period-filtered sum (drops the restatement), the reversal-matched sum
(over-corrects where the first posting was itself a correction), the answer. Lazy delta: the naive sum
differs from the answer on all twelve units. Realism: a group payables ledger restates accruals and the
restatements are chained, not reversed.

**Ask 2, the till takings reconciliation.** Figures: per branch and quarter (9 by 4), FY25 till takings
against the sales control account, and the gap. H18 home: the trail from an input the call consumes, through
device rows it never reads, to its control total. Use: internal audit scopes till testing by where takings
and the ledger disagree. Primary device: D8, the till file's `business_date` is the branch's local date while
the voucher is stamped in UTC, so a naive date join moves one trading hour across the quarter boundary and
double-counts the night the clocks go back (seen by nobody who joins on date, and the battery passes it).
Hazards: D6 a till's day appears at two grains across the EPOS convention change; D1 a re-sent batch on one
depot. Files: `epos_till_takings_fy25.csv`, `gl_control_totals.csv`, the FY25 journal entries,
`trading_unit_register.csv`, `period_calendar.csv`, `epos_interface_notes.pdf`, the branch register and the
sales account map: eight files, twelve columns on the path. Stops: the date join (double counts the DST
night), the UTC-naive join (drops an hour each quarter), the grain-blind sum (double counts the convention
change week), the answer. Lazy delta: the date join differs on 14 of the 36 cells.

**Ask 3, the monitoring coverage.** Figures: per trading unit and FY25 month (12 by 12), the entries in
scope of the ruleset but never evaluated. H18 home: a measure every unit carries that the call does not turn
on. Use: internal audit judges how far FY25 monitoring can be relied on. Primary device: D4, coverage is
drained down in stages rather than absent, so a unit's evaluated share falls over three months before a
re-platforming and the absence is evidenced only in the run log's partial-run rows, which no habitual join
reaches. Hazards: D5 a silently partial extract on one unit's first month; D9 the run log's own completion
flag is true for a partial run. Files: `monitoring_run_log.csv`, the FY25 journal entries,
`rule_catalogue.pdf`, `monitoring_platform_guide.pdf`, `trading_unit_register.csv`, `period_calendar.csv`,
the scope rules and the re-platforming note: eight files, ten columns on the path. Stops: entries minus
evaluated entries (counts out-of-scope entries as unevaluated), the completion-flag filter (believes the
partial runs), the scope-blind count, the answer. Lazy delta: the subtraction differs on 31 of the 144 cells.

**The main population's zero counts**, each asserted in `checks.py`: zero FY26 entries carry a payables
restatement chain, zero FY26 entries are sourced from the till file, zero FY26 periods carry a partial
monitoring run, and zero rows of the three ask files fall inside FY26 P1 to P9.

**Hazard table.**

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| D7 half-year unit renumbering | 1, 3 | ask 1: 4 of 12 units; ask 3: 19 of 144 cells |
| D9 a control true in its own scope | 1, 3 | ask 1: 12 of 12; ask 3: 12 of 144 |
| D1 a re-sent batch | 2 | 3 of 36 cells |

No subset of mishandlings composes back inside any ask's bin, and no two asks share a primary device
family (D2, D8, D4).

**Referee.** `payables_control_account.csv` arbitrates ask 1's designed disagreement and carries no level
for asks 2 and 3 and nothing the call reads. Every other control ties under every handling.

**Cracker sheet.** The cracker landed the call, ran the hygiene battery (key uniqueness, exact duplicates,
unmatched joins, fan-out, count ties), executed every filed rule and matched every control and published
figure.

| Figure (the cracker) | Cracker's route | Outcome |
|---|---|---|
| ask 1, the 12 unit differences | subledger sum against the control account, restatements kept as posted | miss |
| ask 1, the reconciling items | the period-filtered gap | miss |
| ask 2, the 36 branch-quarter gaps | till file joined to vouchers on date | miss |
| ask 3, the 144 unevaluated counts | in-scope entries minus entries with a verdict | miss |

Every row misses.

Mirror leakage: 17.0 per cent of ask weight, measured on the cut pack. The mirror takes no ask whole: it
misses every one of ask 1's thirteen balances and every one of ask 3's 144 cells, and on ask 2 it keeps the
control-account column and the four quarters the upload lag does not move, 54 of 108 figures.

Pair ceiling: 36.3, measured on the cut pack, from one response landing the call: 28.5 plus 27.5 times the
ask weight the pair keeps, which is 11.4 per cent for the cracker and 17.0 per cent for the mirror. Ask
weight is shared in proportion to separately gradable figures, 65 for ask 1, 108 for ask 2 and 144 for ask 3.

Measured by: generator/pair.py, run on the cut pack. It refuses rather than reporting a pass on an empty
denominator (reduce-house-fixes H34). Its measured rows: ask 1 cracker 0 of 65 and mirror 0 of 65, ask 2
cracker 36 of 108 and mirror 54 of 108, ask 3 cracker 0 of 144 and mirror 0 of 144.

The one figure no route can miss: ask 2's control-account column is a read of a shipped file rolled from
period to quarter, so every route that maps the unit codes gets it. It is graded because the question asks
for it, and it is why ask 2's cracker keeps 33.3 per cent of that ask while missing every gap. The two
figures the device moves, the takings and the gap, miss on all 36 cells.

## Leak sweep and the pre-ship check

`leak.py task184 --asof 2026-07-03`. Sweeps 1, 2, 5, 6, 7, 8 and 11 clean. Every REVIEW line answered below;
nothing was fixed by hand, the one fix went into the generator.

**Sweep 3, the platform's own reported figures.** The sweep first read the monitoring platform's exception
counts as golden figures: the group total in the operating guide's period summary and the manifest's row
count for `monitoring_exceptions_fy26.csv`, both 7,481, and the twelve per-unit totals. They are not the
answer, they are the figure the platform publishes and the figure the bridge starts from, and Gate B
requires them in the pack: without the summary the register cannot be reconciled and the oracle has nothing
to tie to. They are now declared in `metadata.json` under `stated_inputs`, which is what that field is for,
and the sweep reads them as stated inputs.

**Sweep 4, shared vocabulary.** The rule catalogue and the operating guide carry 8 of the 12 distinctive
words of the committed call, and the dictionary, the operating guide and the EPOS note carry 3 to 5 of the
stump paragraph's terms (voucher, carries, interface, writes, source, register, verdict, window,
catalogue). Harmless: the call sentence is written in the ledger's own nouns and the documents are about
those nouns, so the overlap is the domain's vocabulary and not the move. Nothing in any of the four
documents says that the entry-level indicator saturates, or how to invert it, and the readability screen's
decisive row stays `silent`.

**Sweep 9, dates after the as-of.** `period_calendar.csv` carries five dates after 2026-07-03 and
`extract_manifest.txt` one. They are the remaining fiscal periods P10 to P12 and the financial year's end,
2026-09-27. Harmless and necessary: a 4-4-5 calendar is published before the year starts and states every
period's dates, and the manifest has to say which year the extract covers and that P9 closed on 2026-06-28.
Both are facts the requester holds before the window closes, which is what makes the call forward facing.

**The house-fix register** (`reduce-house-fixes`), checked file by file:

| Fix | Check | Result |
|---|---|---|
| H1 containers | writer signature or out-of-band stamp in any shipped file | the four PDFs and the golden workbook go through `postprocess.normalize_pdf` and `normalize_ooxml`; `grep` for the library name in every PDF returns zero |
| H18 asks inside the decision | each ask a component, qualifier or audit trail of the call | all three are: the payables reconciliation and the till reconciliation are the controls the plan relies on, the coverage shortfall is how far monitoring can be relied on at all |
| H23 presupposition | an ask that only parses if a subset is non-empty | none: "what makes up any difference" and "how many entries were in scope but never evaluated" both read with nothing as the answer |
| H24 fiction tells | a sentence saying the pack was built | none; sweep 2 clean |
| H34 a measuring script that scores nothing | `pair.py` on an empty denominator | it refuses with exit 3 and names the empty, and it refused correctly at stage 2 when no pack existed |
| H35 a measuring brief that names the answer | the stage 4 reader's brief | written from `score_reader.py --emit-keys`, and `grep` for the figures, the method words and the wrong routes returns zero; the `rungs.*` keys were deliberately withheld, because they name the wrong routes |
| H36 a tolerant comparison before the exact one | `score_reader.py` | compares numbers before strings, which is the fixed order |

**The pre-ship check, the 10/10 rules re-read against the built pack.** The decisive step is still analytical:
`checks.py` executes the easy route on the generator's clean truth and it files 7,481, then changes the
inversion alone and files 14,989. The mess is still only Layer 1: the two unit-code vintages, the 4-4-5
calendar against calendar months, the EPOS voucher convention changing mid-year and the upload lag all
complicate the work and none decides the call, which `checks.py` asserts by recomputing the golden under
each reading. No artifact ranks the units on the decision question and no artifact states a posting count,
so Gate G holds with every wrong number deleted.

## Stage 4: the leak reader and the determinism judge, 2026-10-26

Both spawned together in the background on the built pack, each isolated.

**The leak reader** (Sonnet, medium, holding only a fresh unzip of `target.zip` and `prompt.txt`; its brief
written from `score_reader.py --emit-keys` with the `rungs.*` keys withheld, so it named no figure, no
method and no wrong route). It filed **12,000** against the golden's 15,000, so the call was missed. Its six
answers are clean and they confirm the design from outside it: nothing in the pack told it the decisive
step ("No sentence states the decisive step. The inference step is my own"), no file ranks or scores on the
question, the only files it called analyst-only were the two declared distractors, no filed sentence fixes
the computation, and on question 6 it named the deciding move as "an analytical choice: the detection-rate
model inferring postings from entry-level verdicts". Gate H's rule 3 therefore passes from outside the
design: not a plant, not a field reading, not an executed procedure.

**But the reader reached the decisive step unaided, and its estimator is the golden.** It wrote that it
fitted the per-posting rate by maximum likelihood on the raise outcome by entry size and then took the
expected tripped postings for each raised entry. Executed per unit and summed, that estimator returns
14,989.3, which is the golden to the figure. It filed 12,000 only because it applied the rule catalogue's
scope exclusion and the pack contradicts itself there. The step was not hard; it was hidden by a defect.

**The determinism judge** (isolated thread, seeing only the bundle, the prompt, the graded blocks and the
judge's own system prompt): **NOT_DETERMINISTIC, SEND_BACK**, taxonomy `answer_contradicts_files` with an
underspecified population. Gate G passes (`statistical_rigor`, analytical, no surface-read dependency, no
sole data defect). Gate H passes (domain pass, layers pass, decisive step analytical). It confirmed the
golden reproduces, group and units. Its three findings:

1. **The scope contradiction.** The catalogue marks PAYROLL and AP_INVOICE not covered, and the register
   still raises 58 of 60 payroll entries and 1,806 AP entries. Confirmed here: 1,634 of the 7,481 exception
   rows sit on streams the catalogue excludes, and the golden counts all 1,225,763 postings while ask 3's
   own scope filter excludes those streams. The pack contradicts itself.
2. **The rounding is fragile.** Fitting the rate per unit and posting stream gives 14,472, which grades to
   14,000; excluding payroll gives 14,076, also 14,000; excluding payroll and single-posting AP gives
   12,475, which grades to 12,000. The note's claim that every licensed estimator lands in one bin is false
   once the grouping is allowed to vary, which it is.
3. **The per-unit grouping is not forced.** One group-wide rate puts DPG-420 at about 1,400 against the
   golden's 1,600.

It also asked for the "synthetic, generated by task184/generator" line to come out of `metadata.json`, which
is an in-house fix and correct.

**The verdict on the architecture, and why it is not a repair.** Finding 1 is a defect and would be a
one-line fix. Findings 2 and 3 are not: they are `stumping` 1.1c arriving by another road. The decisive
step here is an estimator, and an estimator has to be fitted over some population; group, unit, and unit by
stream are each defensible and give 14,712, 14,989 and 14,472, which is two bins. Filing the grouping closes
the fork and makes the decisive step rule application; leaving it open fails Gate C. That is the same pair
of horns that killed architectures 3 to 7, and changing the decision type from a ranked slate to a recovered
count did not escape it, because the free parameter was never the cap, it was the fit. Architecture 8 is
spent. The measurement is filed as `stumping` 1.1j, and 1.1i has been amended, because as first written it
claimed more for the decision type than the build then showed.

**What the next architecture needs.** A decisive step with exactly one defensible execution given the
records: a reconstruction the records determine, where the easy route omits a piece the records supply
exactly, rather than a quantity fitted over a population the analyst chooses. That is
`supplemental-stumping` 1.0b, filed for ask devices, and it holds for the call for the same reason.

## Tried and rejected

- Architecture 9's draw hunt (2026-10-27): three candidates drawn, gated and killed on measurement, each
  entered above. The useful residue is that all three put the decisive step in the nonlinearity of a
  records-fixed count, and in every case the nonlinearity was either attained by a one-pass scan or financed by
  a parameter the records do not fix. Architecture 10 is not another nonlinearity on this ground.
- Architecture 10's ground, corrected the same day. My first reading of the hunt was that
  `business-operations-analytics` x anomaly-detection was the only ground left, because coverage prints just two
  never-built drawable anomaly pairings and the other is this slot's own criminology lineage. That was wrong twice.
  `ban.pairing` reaches only the last three builds, so a pairing used earlier is drawable on its merits, and
  never-built is a coverage nicety rather than a requirement. And the corpus says where to look: across this lane
  17 anomaly-detection builds have shipped against 7 stuck, and the split is by what supplies the deciding
  quantity. The shipped ones sit where it is a physical, instrument or measurement process
  (`energy-systems-utilities` 3, `physical-environmental-sciences` 2, epidemiology, pharmacology, biomedical,
  human-factors) or a sampling and estimation process (`survey-research-official-statistics` 2,
  `general-statistics-data-science` 2). Both stuck accounting slots are this one and task198. So the objective is
  not closed, three slots have each exhausted one world, and architecture 10 draws a deciding quantity of the
  first kind rather than the one never-built label.
- The cell itself is the finding, and it is why architecture 10 moves domain. In `accounting-audit-forensic` the
  only live inherited anomaly-detection task type is `forensic-investigation` mapped to `fraud-aml-detection`
  (`multiple-testing-selective-inference` is closed by the Part 3 screen, `exploratory-data-analysis-distribution-assessment`
  is task202's ground), and on that one type the swap test failed or nearly failed on all three candidates in the
  same way: the deciding quantity keeps coming out as a combinatorial or weighting property of two record
  streams, which reads identically with any field's nouns. That is a property of the cell, not of the draws.
  Nine architectures are now dead across three worlds in this slot.
- Two bookkeeping defects found by that hunt and fixed the same day: `cards/task184.json` carried
  `architecture_spent: None` against `pipeline.json`'s `true`, so architecture 8's axis bans
  (`accounting-audit-forensic`, `audit-testing-sampling`, shape 03, `grain_or_unit`, `monitoring_export`) were
  fencing off ground no live build occupies and the similarity rules were running against a dead architecture;
  the card is now flagged spent.
- `task184/metadata.json` is still architecture 2's criminology pack (the Harbourgate patrol slate, 16 kcp and
  harbourgate files, `prompt_shape` 07 against the card's 03, as-of 2027-01-22) and is left as it is on purpose:
  it is the house record, a different schema from the in-pack `target/metadata.json` that the generator writes,
  so it is rewritten when architecture 10's pack is cut and not before. Copying the in-pack file over it was
  tried and reverted, because that file carries `provenance`, `stated_inputs` and `distractors` and none of the
  house record's `domain`, `objective`, `prompt_shape`, `field_terms`, `input_gates` or `sources`.

- 2026-10-21, architecture 3 at the draw: a latent-grouping decisive step in this world, recovering the
  keeper's routine type from the windows and fitting the clock conditional on it. Dead before any design, read
  off the generating model rather than measured on a pack. `offences.covered_record` draws every offence's hour
  from `intensity()`, one quarter clock shared by every class and every routine, and the routine only turns
  that hour into a window: the hour comes from the clock, the routine from the target, and they meet only at
  the censoring. So every grouping of the records, by class, by routine, by location or by anything else,
  estimates the SAME clock and differs from the pooled fit only by estimation noise. That is exactly what
  killed architecture 2, where the per-class fit moved the eighth slot on a likelihood ratio of 511.1 on 668
  degrees of freedom that neither rejects pooling nor prefers it, and it kills every grouping-based
  architecture here for the same structural reason. The note's own docstring says it: the clock is "what the
  record is of". Architecture 3 therefore needs either a world where the clock genuinely differs by a latent
  group (which is a new world and so a real stage-1 draw, not a re-use of this one), or a decisive step that is
  not about grouping at all. And if it is grouping, the group must be latent AND discoverable by estimation,
  because stratifying on a visible attribute is on the opponent's own reflex list.

- The shipped architecture's decisive step, the even spread of each window over its own hours against a
  point in it (2026-10-21, stage-2 re-root on a measured Gate F failure): a blind Sonnet reader at medium
  effort holding only a fresh unzip of `target.zip`, `prompt.txt` and the figure names reproduced the
  committed call exactly, the eight-slot slate, the 4,050 season total and the unrounded 4,047.64, and took
  75 of 97 ask figures. It named the decisive step itself and then quoted the pack for it: clause 4.4
  forbade every alternative placement, clause 4.2 fixed the clock and the Crime Recording Standard's 3.3
  confirmed nothing narrows the window, which leaves the even spread as the only move. Three filed
  sentences composing into the method is rule application under the client's rule 3, so the ladder is
  re-rooted and the even spread becomes rung 3.
- Deleting the three clauses and keeping the even spread as the golden (2026-10-21, at the re-root): the
  reader reached the even spread unprompted, named it in its own words and scored the window-start,
  window-end and midpoint variants against it, so removing the sentences that licensed it leaves the same
  answer reachable and Gate F fails again. The golden has to move off the textbook weight, not be better
  defended.
- The witnessed classes' own hourly profile, or the pedestrian feed's footfall, as the golden placement
  (2026-10-21, at the re-root): the forcing file publishes a one-column precis of itself in both cases
  (`stumping` 1.6a's fourth clause), and clause 4.4's surviving sentence keeps both out of the count anyway,
  because neither is the force's record of the covered offences. Kept as the two SF rows that clause closes.
- Weighting each window by the covered offences' own exactly timed hours, the one-step refinement
  (2026-10-21, at the re-root): rejected as the golden and kept as rung 3b. Those offences are the ones that
  fell in an hour their keeper was watching, so their profile is a profile of the watched hours and holds
  nothing about the hours the slate turns on; the record refutes it as a placement at a likelihood ratio of
  13,660.0.
- Every window edge on a four-hour grid, so the cells the record separates are exactly the 42 slots
  (2026-10-21, at the re-root): measured and rejected. It moved the cap's gap over the estimator's own
  standard error only from 1.04 to 1.42, so it does not fix what it was reached for, and it left the whole
  record with 13 distinct window lengths and every victim-given time on a multiple of four hours, which is
  the regularity a leak reader already sent this number back for once. The 2-hour grid was measured too, at
  1.25, and rejected for the same reason.
- A night crest about an hour wide (2026-10-21, at the re-root): with windows a median 16 hours long that is
  a recovery over a span fifteen times the feature, and the estimator's own standard error ran to 70 to 80
  offences on a slot against a cap gap of 46, so the slate was the draw's rather than the design's (the
  record's eight matched the true times' eight in 7 of 8 slots). The crest is now wide enough for the
  recovery to be well conditioned and the cap falls on a step of 76.8 offences instead.
- Keeper routines with no spread across the quarter's premises (2026-10-21, at the re-root): the whole
  record then held 24 distinct window lengths and every window edge at one of a handful of clock hours,
  which reads as generated. Each family now spreads over the hours its own premises keep, and the record
  carries 47 distinct lengths cut at 159 distinct hours of the week, which also separates the hour grid
  better rather than worse.
- Leaving the draw at NUDGE 14, which put the 43 call figures furthest from a rounding edge (2026-10-21, at
  the re-root): the ask figures move with the same seed, and at NUDGE 14 ask 3's footfall sat 0.54 from a
  half of ten against the 1.4 the build asserts. The draw is now fixed at NUDGE 37, which clears ask 1 and
  ask 3, and the 43 call figures are brought mid-bin instead with FLOOR, the quarter's baseline offence
  level, which no ask figure reads (the location and report-lag draws are taken before any occurrence hour
  is).


- The seed's idle lane positions as the decisive limit (2026-10-12, at the draw): a per-airport cap that removes the
  natural pick and re-places it, strategies.md F3's dead form (58 v3 and v4).
- Lane capacity observed only while a queue stands, so passengers per lane-hour measures demand at quiet airports
  (2026-10-12, at the draw): task127's driver (a team's capacity visible only as the ceiling it held through a surge).
- Transfer passengers who never reach the landside checkpoint, so departing seats overstate the hub's summer demand
  (2026-10-12, at the draw): the share of a flight's passengers who pass the checkpoint is one ratio per route, and a
  bottom-up build calibrated to last summer's checkpoint counts at airport level already lands close to the call, so
  the decisive step is one enumerable correction.
- The release at only Cullinvale, Ardcarrig and Faranloe, four hosts releasing nothing (2026-10-12, at build): the
  default path kept 15 of the 24 airport-period figures and the averaged path 21, so a response off the call banked
  most of the airport figures; every host but Halloran Bay now stands down two lanes all day.
- Dromkeel as last summer's realised-effect leader (2026-10-12, at build): on the simulated 2026 feed Cullinvale's
  deep queues give it the largest realised effect (1.48 times Eskerford) under every demand Dromkeel's checkpoint
  clears by close; the lateral rung lands on rung 0's answer and the ladder runs three rungs.
- Asking for each airport's figure by period (2026-10-12, at build): 24 construction figures the cracker holds put the
  pair near 44; the prompt asks each airport's summer figure.
- Sinusoidal design days with flat banks (2026-10-12, stage 4): the leak reader read them as synthetic-smooth and the
  same shape at every airport; the design days now carry a late-morning wave, an afternoon lull, a thinning last hour,
  cresting banks and rough 15-minute noise.
- "How far the chosen airport's forecast passengers could fall short before another posting would move more"
  (2026-10-12, judge pass 1): read as the last whole per cent still ahead or the first behind; the prompt asks the
  smallest whole per cent shortfall at which another posting would move more.
- Taking the stand-down as the whole decisive step (2026-10-14, the hardening): the first architecture's single layer,
  shipped 10-12. The portal left it off the approved list, so the posted-day gap against the roster pattern is now
  rung 2 and the decisive step is the counterfactual arm: both sides of the comparison read from the lanes each
  checkpoint actually opens. Every figure moved; the call moved from Halloran Bay to Eskerford.
- The host stand-down measured against matched non-posted weeks, with the crowd-out as the difference (2026-10-14, at
  the hardening): the quiet-hour closures a matched-week design nets out never breach the standard, so the correction
  was worth nothing on the graded quantity (stumping Part 3, a rung measured on the graded figure). The same
  comparison against the checkpoint's own days moves the baseline arm, where it is worth 23 to 40 per cent of every
  airport's figure.
- A chronic shortfall across the whole rostered peak window (2026-10-14, at the hardening): two lanes short through
  Eskerford's plateau put its 2027 design-day waits over 95 minutes and left 58 of 78 simulated 2026 days with a
  queue at close, which no national agency would run a summer on. The shortfall now sits on the pattern's shoulders,
  which keeps the 2026 sensor's 99th percentile at 50 minutes.
- A shallow-breach world (the banks just above the pattern's capacity) to make the shortfall cheap in queue time
  (2026-10-14, at the hardening): with the plan barely breaching, the unit's three lanes fully relieve every
  checkpoint, so the stand-down stops biting and rung 2 collapses onto rung 0's answer; the ladder needs the banks
  deep enough for a two-lane stand-down to leave a residual.
- The whole hardening: the counterfactual arm read from the checkpoint's own days against its filed roster pattern
  (2026-10-14, judge pass 3): built, green on every free gate and 1.26 times clear on the call, and sent back on the
  architecture. The forward lanes are not filed, so both arms rest on an inference from last summer, and the
  difficulty is the refusal of an official artifact, which Gate G bans at any depth. The repair that would close the
  fork (filing the persistence, or naming the lane sensor record as the basis) is the one `/fix-determinism` forbids,
  because it turns the decisive step into rule application. The number re-roots at stage 1: the next draw needs a
  Layer 2 family that does not turn on a plan the records contradict.
- Architecture 1 as a whole, the airport posting world (2026-10-14, re-root): spent at judge pass 3 (Gate C, the
  forward lanes are not filed; Gate G, surface_read_rejection). Architecture 2 draws Criminology & Justice, where the
  deciding quantity is the weight a recorded offence's occurrence window puts on a patrol slot, so no filed artifact
  is refused and no forward fact has to be inferred from a past regularity: every offence's window is in the record
  and the estimand is defined over it.
- Estimand filed as the window-weighted count, 2026-10-15: it read as the tasking contract filing the share weighting, which would make the decisive step rule application under the client's rule 3. Refiled as the unobserved count the contract defines, with the weighting attributed to the records' structure and the word sweep asserting no document states one.
- A single eight-hour shift start as the decision (a dial over twelve start hours), 2026-10-15: tested on the built
  windows and the spreading washes out at that width, the aoristic pick and the midpoint pick are both 20:00 and the
  gap to the runner-up is 3.9 per cent. The four-hour slot is what makes the window's spread decide anything.
- Windows at any minute, 2026-10-15: it left a spreading-grain fork (the exact overlap share against a 15-minute or
  hourly sampling differed by up to 3.7 offences on a graded slot, which crosses a bin). Replaced by windows
  recorded on the hour at both ends, which is how victims give them: every grain that divides an hour then returns
  the exact share, to 4e-10.
- Ask 3 as missing rows for the hours a sensor was down, 2026-10-15: dividing by the rows present then equals the
  golden, so the availability log was free and the device did nothing. Replaced by a head counting one direction
  only, with a row published for every hour and the fault log the only record.
- Grading the 42 cells to the nearest ten, 2026-10-15: no draw in 14,400 puts 43 figures that far from a rounding
  edge at that bin. The nearest fifty, with the worst figure 4.09 offences from a half of fifty.
- Judge pass 1 (2026-10-15) returned NOT_DETERMINISTIC on four unpinned conventions, with Gate G and Gate H passing
  and the trap confirmed: the season basis of the slot figures (the mean of the two seasons was not filed, and 2026
  alone moved Wednesday and Thursday 20:00 from 400 to 450), the class set behind ask 1, the base behind ask 2's
  shares, and the treatment of the fault hours in ask 3. All four are now pinned in the question, which is where the
  judge said the fix belonged; the main call, the ladder and the decisive step are untouched.
- The leak reader's pass 1 (2026-10-15) weighted each window by the pedestrian feed's footfall at the offence's
  location and filed a different slate, and the witnessed classes' hourly profile does the same once the window
  shapes are realistic. Both are now ruled out by the agreement's clause 4.4, which confines the count to the
  force's record of the covered offences and forbids any other offence, source or proxy from placing an offence
  inside its window; `checks.py` asserts the clause is present and that both routes would file another slate, so it
  is load bearing rather than decorative.
- Windows of a single shape per class, 2026-10-15: the leak reader read the regularity as generated (criminal damage
  and business burglary always 20:00 to 22:00 against 07:00 to 10:00). Each class is now a mixture, a shop shut
  overnight or over a bank holiday weekend or the damage found before closing, which also widened the length
  distribution (median 10 hours, a tenth at 4 and a tenth over 30).
- **(2026-10-25) A blind reader appeared to land the call, and the measurement is VOID because the brief handed it over.** The reader was given the flat `figures.json` key list to fill, and that list carries `call.slot_offences.<slot>`, one component per slot of the committed slate: eight of the week's forty-two slots and only those eight. The reader said so in its own report, that its refined spread "reproduces the same eight slots as the slate the key names, which is why I used it". So this run is evidence about the brief, not about the build. It is worth keeping for one thing it did without help: it rejected flat spreading over each occurrence window after measuring that flat spreading reaches only 4 of the 8 slots, and built an iterative hour-of-week profile to convergence instead, which is this architecture's decisive step. A clean re-measurement is owed, briefed from `score_reader.py --emit-keys`, which now drops exactly those eight paths.
- **(2026-10-25, measured clean) THE CALL HOLDS, AND THIS IS THE BEST-MEASURING BUILD IN THE LANE.** Re-read with a brief emitted by `score_reader.py --emit-keys`, so the eight slots of the committed slate are no longer named in the key list. The reader filed a **different slate**: it kept Friday 16:00-20:00, which is the golden's runner-up, and dropped Monday 20:00-00:00, and it filed 5,096.6 covered offences against the golden 5,705.2, a runner-up of Thursday 12:00-16:00 at 378.4 against Friday 16:00-20:00 at 400, and a gap of 44.1 against 100. **0 of 7 call figures hit, 32 of 101 ask figures, 31.7 per cent.** It built the decisive construction itself, an EM fit of a weekly timing profile over the interval-censored windows, and rejected window start, end, midpoint, flat spreading and an exact-times-only profile by name, so the construction is reachable; what it could not reproduce is the slate, because it reported the eight slots are stable under its own settings while the eighth against ninth ordering is not. With both top responses missing the call the pair is 12 plus 55 times the ask keep, so this build measures at **29.4, under the 40 build target**, and the earlier `FAILED_TO_STUMP` rests on a judge SEND_BACK rather than on any measurement of its power. It is a `/fix-rubric` candidate at most, and arguably a ship.
- **(2026-10-25, architecture 3 pass 1) The window's placement as the decisive step, on the data as architecture 2 generated it: refused on an exact argument.** `mark[h]` is deterministic in the hour and the keeper and a keeper's gap is its unwatched stretch, so the hours that could have produced a window are exactly the window, the censoring is non-informative and the naive fit is consistent. Measured: the naive fit reproduces both architecture 2's golden and the true intensity's own top eight.
- **(2026-10-25, architecture 3 pass 2) The same step with a passer-by process added: the bias is real and the correction is not shippable.** With immediate notice proportional to the measured footfall shape the naive fit falls to 6 of the truth's 8 slots, so the misspecification exists. But the corrected likelihood needs the share of targets watching each hour, and the only version that recovers the truth 8 of 8 takes it from the generator's own routine weights, which no solver can see. Reverted.
- **(2026-10-25, architecture 3 pass 3) The watch share read off the trading hours: lambda is unidentified.** The profile log-likelihood is -139,423.08 at every lambda from 0.30 to 0.90 and the slate matches the truth 3 of 8. Cause: the passer-by rate was zero outside trading hours, so the term that should identify lambda vanishes exactly where it would matter, and a 0/1 watch share also excludes every open hour from every window outright instead of down-weighting it. A Gate C failure, and the reason the next pass must show the watch share identified before any data is cut.
- **(2026-10-25, architecture 3 pass 4) The watch share reconstructed from the windows' own endpoints: confounded with the clock it exists to correct, and the architecture is SPENT.** With the passer rate made non-zero everywhere (0.0008 to 0.62, a 776-fold range off the footfall feed) the level still did not identify: the profile log-likelihood rose monotonically to its boundary and the slate was **identical at every level**, because `m` was still a 0/1 indicator so `(1 - m)` is exactly zero on every open hour, which hard-excludes those hours from every window and drives the slate to the all-closed small hours whatever `d` does. Then the endpoint reconstruction, which was the one route left: right in shape (it peaks mid-morning and troughs overnight) and wrong in level, **correlation 0.5477 with the generator's true watch share, mean 0.612 against 0.222**, because each target contributes endpoints in proportion to its own offences, so the reconstruction is weighted by the clock it is meant to correct and de-confounding it needs that clock. No fourth source exists in the pack, so the decisive step is **not computable from the shipped record** and this is a Gate B failure rather than a Gate C or Gate F one. Architecture 3 is spent; the generator change is reverted and the pack reproduces at `c507033cde9b779a`. Filed as `stumping` 1.1e. **What carries forward:** the bias is real and large (the passer-by process drops the naive fit from 8 of 8 to 6 of 8 against the truth), so the step is intact in a world where the watch schedule is recorded for its own sake, a guarding contract or a keyholding roster or an alarm-monitoring schedule. Architecture 4 draws that world rather than inferring the schedule.
- **(2026-10-25, architecture 4) The watch share SHIPPED as a graded register: both ladder conditions pass and the accuracy condition fails at every one of sixteen settings.** Architecture 4 keeps the step and ships what architecture 3 could not: a graded watch share, as a keyholding and alarm-monitoring register gives it, recorded because the monitoring is contracted and billed. With it the fitted level IS identified, a clean interior maximum (-96,980.83 at 0.45, -96,322.95 at 0.75, -96,370.83 at 0.88), and at the best setting (floor 0.10, Friday's daytime amplitude 1.40, the Tuesday and Wednesday night amplitudes at 0.95) the naive fit differs from the golden on **4 of 8** and the margin is **55.8, or 12.82 per cent, against a worst licensed-variant shift of 31.2, a cushion of 1.79x**. So 1.1d passes on both counts, which no earlier architecture in this slot managed. **But the golden is no more accurate than the naive fit: 6 of 8 against the truth, exactly as often, and at two of the sixteen settings LESS often (5 of 8 against 6 and against 7).** The cause is exact and is not the dial: with the level FIXED at its true 0.62 the correction recovers the truth 8 of 8, and its maximum likelihood lands at 0.75 instead, because the generative mechanism draws immediate notice per keeper off a 0/1 indicator while the shipped series is the share across keepers, so aggregating changes the likelihood and the fitted level moves to absorb it. A mis-calibrated correction trades one bias for another. Filed as `stumping` 1.1f, which adds the accuracy condition as a third thing a corrected route must assert rather than argue. Generator reverted; the pack reproduces at `c507033cde9b779a`. **Architecture 5, if the number is taken further, keeps the likelihood per unit: the premises type on each offence record, which a force does classify, and the monitored hours per premises type, which a monitoring contract does record. That is one more organ on the pack and has to be weighed against readability test 7 before it is drawn.**
- **(2026-10-25, architecture 5 built at stage 3) Everything the design promised held, and the LADDER INVERTED on a rung the design never scored.** The build went in: the settled parameters, a `premises_type` column on the extract (the force's own twelve-class classification, which preserved all three conditions against the raw twenty schedules: golden 8 of 8, naive 4 of 8, margin 110.7 at 22.45 per cent, cushion 1.41x), a `harbourgate_keyholding_schedule.csv` of 3,414 rows across 424 monitored sites recorded at the site's own grain because the contractor is paid per attended hour, and the corrected estimator as the golden with the interval-censored fit as the top rung. The solver's own path, with the band read off the shipped schedule rather than from the generator, passed all three conditions at a cushion of 1.46x and the band deviated from the generator's by at most 0.0898. **Then the full rung table, which no earlier pass had computed: window start 0.440, window end 0.311, THE MIDPOINT 0.905 AT 6 OF 8, flat aoristic 0.569, seen profile 0.553, the interval-censored fit 0.685.** The crudest route on the list comes nearer the golden than the sophisticated one and reaches nine tenths of the decision's whole value, because the correction moves mass toward the quiet part of a censoring window, an overnight gap's quiet part sits near its middle, and the midpoint rule puts it there already. `stumping` Part 3 forbids a non-monotone ladder outright and the sequence here is a scatter. Reverted; the pack reproduces at `c507033cde9b779a`. Filed as `stumping` 1.1g: score EVERY rung against the golden at the draw, not the decisive pair, and when the decisive step moves mass toward the middle of a window, score the midpoint rung first.
- **(2026-10-25, architecture 6, a new world) The wholesale-market quarter gives the first MONOTONE ladder in this slot's history, and the fitted level forfeits every figure.** The world was redrawn rather than the step: targets that trade before noon (market stalls, early units, a bakery), so the gaps run from midday to the small hours and their quiet end is not their middle, which is what killed architecture 5. Measured over three worlds and more than forty settings, the winner being a day-of-week spread of 0.55, 0.70, 0.85, 1.00, 1.35, 1.55, 0.80 with a Saturday market-day crest of 0.60: **window start 0.29 to 0.44, midpoint 0.35 to 0.41, window end 0.48 to 0.51, flat aoristic 0.60 to 0.66, the field's interval-censored fit 0.79 to 0.89, the golden 1.00, monotone at every seed**, golden 8 of 8 against the truth, the field's method 4 to 5 of 8, margin 19.98 to 22.41 per cent. Then the determinism check: the detection level's profile likelihood rises monotonically to its boundary, so it is unidentified, which is a legal C3 corridor because **the eight-slot set is identical at every level from 0.70 to 0.999 and under both grid variants at every seed**. But only the set survives: the ranking holds at three seeds of four, each slot's own figure spreads up to 347.6 on a figure near 3,500, and the covered total spreads 6.20 to 9.08 per cent. A figure-dense shape cannot be served and stacking asks to reach the criteria count is banned, so the corridor buys the call and forfeits the figures. Filed in `determinism-check`.
- **(2026-10-25, architecture 7) The parameter-free correction removes the corridor and the default path then nearly lands.** The step becomes determinate with no level at all: a victim states when the thing was last seen and when it was found, that window spans several of the keeper's own attendances, and the keyholding schedule shows which hours inside it were attended, so those hours are not candidates. No fitted parameter, so every figure is determinate. The ladder stays monotone at every seed and the golden still recovers the truth 8 of 8, **but the field's own interval-censored fit reaches 0.95 to 0.96 of the golden and shares 6 of the 8 slots**, so the correction buys four per cent and the default path is nearly right. (An earlier run of this test showed the window-start rule at 8 of 8; that was my simulation placing the last sighting exactly a whole number of days before the offence, so the start aligned with the true hour. Fixed to put the sighting at the keeper's own previous attendance, which is what a sighting is.)
- **(2026-10-25) THE MECHANISM IS CLOSED FOR THIS DECISION TYPE, and that is the finding.** Seven architectures, three worlds, more than forty settings. `stumping` 1.1h states it: when the graded call is a slate of periods and the decisive step is how an interval-censored record is placed inside its window, either the offences concentrate in periods unattended by every target, in which case those periods sit inside almost every window and every placement rule ranks them top so the slate's head is route-invariant, or they concentrate in periods some targets attend, in which case they are seen as they happen and there is little censoring to work on. The censoring and the signal have the same support, because a window exists precisely where nobody is watching. **Architecture 8 keeps the domain, the objective and the quarter and changes the DECISIVE STEP, and probably the decision type: a placement step needs a graded quantity it moves materially, a level or a rate or a share of the censored mass, not a ranking whose head is the same under every route.**

- 2026-10-26, architectures 3 to 7 (the whole ranked-slate family in the criminology world) closed on
  measurement at the draw, none built. Every variant put the decisive step in where an offence sits inside the
  occurrence window the keeper's routine bounds, and every variant hit the same two horns. The world was
  redrawn once, which bought the first monotone ladder the slot has had (window start 0.29 to 0.44 of the
  golden, midpoint 0.35 to 0.41, window end 0.48 to 0.51, flat aoristic spread 0.60 to 0.66, the field's own
  aoristic method 0.79 to 0.89, golden 1.00) and still left the decisive rung inside the spread of the
  licensed estimators, so Gate C would have taken what Gate F gave. Architecture 7's measurement is what
  produced `stumping` 1.1i, and 1.1i is what redrew the slot: a ranked slate forces the two gates into
  conflict because a ranking's head is the same under every route that estimates the same quantity, so only
  the cap's boundary differentiates and that boundary is a near-tie by construction. A recovered quantity has
  no boundary to sit on.

- 2026-10-26, architecture 8 first model (a group-wide rate, pooled): dead on a Gate C fork of its own. With
  one rate estimated across the group, and with the per-unit rates spread 0.004 to 0.030, pooling and
  estimating per unit differed by 6.3 to 8.5 per cent on the group total, two defensible answers either side
  of the bin. Closed, not abandoned: the estimand now files the unit of estimation (which `determinism-check`
  section 1 makes WHAT, not HOW, so filing it costs no stump), and the world was retuned to a narrower rate
  band where the two groupings converge to within 0.35 per cent as well.

- 2026-10-26, architecture 8 with uniform entry sizes: dead on separation. With entry sizes drawn from a
  narrow band the flag count reached 89.4 per cent of clean truth, because the entry population is dominated
  by single-posting entries whatever the batch share of postings is, so the indicator barely saturates. The
  licensed-estimator spread also ran to 18.9 per cent, since a thin estimator restricted to the unsaturated
  entries had too little to work with. Both were one fault: entry sizes must be heavy-tailed, as a real
  ledger's are, so that the unsaturated entries are numerous enough to identify the rate while the saturated
  ones carry the mass.

- 2026-10-26, grading the bridge by entry-size band rather than by trading unit: refused at the draw. The
  bridge is the natural shape for a recovered count and the bands are where the hidden mass is, which is
  exactly why asking for them is readability test 1: a deliverable whose own rows are entry-size bands tells
  the solver the answer depends on entry size. Trading units are the audit plan's own reporting axis and say
  nothing about the fan-out, so the bridge reconciles by unit.

- 2026-10-26, shipping the posting count only in the line detail and not on the entry header: refused on pack
  size, not on design. At the volumes the determinacy needs (about 1.29 million postings, about 435,000
  entries) a line-grain file is 2.6 million rows and a bundle that cannot ship. The entry header carries the
  item count a posted voucher always carries, which is multi-purpose and forced by the question; the line
  detail ships for the flagged entries and a stratified sample, as an auditor's pull of detail would.

- 2026-10-26, architecture 8 (the group's recovered population exception count, inverting the voucher-level
  monitoring indicator per entry) built in full and closed at stage 4 on a judge SEND_BACK and on the
  reader's own method. Everything measured well except the one thing that matters. Separation was the best
  the slot has had: the flag count 0.50 times the golden, the grossed-up entry rate 1.95 times it, the
  aggregate inversion algebraically the flag count again, the golden within 0.34 per cent of clean truth,
  108 generator assertions and 244 verifier assertions green, two byte-identical builds, the pair ceiling
  36.3 measured on the cut pack, nearest driver on file 0.07. It still dies, because the decisive step is an
  estimator and the grouping it is fitted over is a free choice the records do not settle: group, unit, and
  unit by stream give 14,712, 14,989 and 14,472, which is two bins. And the isolated reader reached the
  estimator unaided in one pass, returning the golden to the figure when executed per unit; it filed a
  different number only because the catalogue's scope exclusion contradicted the register. The lesson is
  filed as `stumping` 1.1j and 1.1i is amended with it: dropping the ranking removes the cap boundary but
  does not make the decisive step uniquely executable, so the next draw needs a reconstruction the records
  force, not a fit.

- 2026-10-27, the architecture 9 draw hunt, three candidates drawn and all three closed on
  measurement at the draw, nothing cut. Harness at
  `/tmp/claude-0/-home-user/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/t184a9hunt/`, every script
  byte-identical on two runs, every route scored against the world's own truth. Also recorded here for the
  first time: three closures measured by the 2026-10-27 reconnaissance (scratch `t184draw/`) that were never
  written into this section, a first-crossing period reconstructed from dated documents against the reported
  periodic series (the coarse series names the right period 12 of 12 at every seed), a peak against a
  period-end snapshot (under limits a controller would plausibly set the default path files exactly zero at
  all five seeds), and the grain family (Gate C and Gate F ride the one dial that shares the line-detail
  coverage, with no middle). None of the three is re-proposable.

- 2026-10-27, candidate C9-1, the joint-feasibility deficiency (accounting-audit-forensic /
  forensic-investigation on the client task type fraud-aml-detection, anomaly-detection): the count of depot
  fuel issues the fleet's own recorded movements cannot jointly account for, against the field's own
  per-transaction exception test. CLOSED AT BOTH ENDS OF ONE DIAL, and this is the cleanest guard verdict of
  the three (WARN, exit 0, two WARNs both against a retired build, nearest driver 0.05 against task198 v4),
  so the ground was open and the mechanism is what failed. The deficiency bites only as the capacity bound on
  an edge tightens. At the only bound the records force, the tank capacity the fleet register carries, the
  per-row exception count is exactly zero at five of five seeds and the deficiency is 11 to 20 issues of
  about 2,650, 0.4 to 0.8 per cent, on figures of 11, 11, 11, 13 and 20 that turn on a handful of
  coincidences. Every tighter bound is a headroom, which needs a litres-per-kilometre rate applied to
  odometer movement, a free parameter: over the fractions of capacity a competent analyst could defend
  (0.80, 0.60, 0.45, 0.30) the graded count runs 164, 448, 816, 1398 at one seed and spreads 8.52x to 12.02x
  across five, so Gate C is dead wherever Gate F lives. Worse, the step's worth falls as the dial buys reach:
  the deficiency over the per-row count is 1.22x at 0.80, 1.14x at 0.60, 1.12x at 0.45 and 1.06x at 0.30.
  And with the capacity bound dropped altogether, so that the presence windows alone bind, the edges are
  intervals, the Hall bound is therefore attained on an interval, and one sort and one pass over disjoint
  intervals reaches 95.3 to 97.2 per cent of the deficiency at four of four seeds while the per-row count is
  again exactly zero. The general form, worth keeping: a feasibility count whose edges are time intervals is
  a scan, and making the edges non-interval needs a bound the records do not fix, which is 1.1h's two horns
  in another mechanism.

- 2026-10-27, candidate C9-2, the per-case inverse of a claim probability (same pairing): the count of FY26
  short-delivery lines, recovered by weighting each claimed shortfall by the inverse of its own drop's
  checked share, against counting the credit notes. Dead on the cheapest licensed member, and the first pass
  of the screen was a harness defect that flattered it. Scored on the mean probability over the CLAIMED
  shortfalls the per-case route cleared the one-divide route by 1.43x at the best dial setting; scored on the
  world's truth, which is the only honest scoring, one group-by and one divide (claims over the verified
  sample's own claim rate over all shortfalls) reaches the truth at 0.966, 0.984, 0.966, 1.026 and 1.078
  against the per-case inverse at 1.023, 1.005, 1.055, 0.995 and 0.994, a mean absolute error of about 4 per
  cent against about 3, so the per-case detail buys nothing and the ladder is level at best. The probability
  is not a shipped column either: fitted from a verified sample, the executions a competent analyst would
  defend (a logistic on the scan share, a linear probability, a decile mean, a quintile crossed with the drop
  size band) spread the graded count 6.0 to 9.4 per cent, and adding the per-customer grouping takes the
  spread to 2.86x, 3.59x and 4.15x, which is 1.1j again. The guard blocks it independently: BLOCK
  test.same_puzzle against task141 v2 inside the batch, BLOCK test.same_puzzle_older against task148 and
  task173, and BLOCK test.same_driver_older against task120, task239, task264 and task269, a signature spent
  in four earlier builds, with driver.near 0.15 against task308 v2. And the organ it needs, a sample that
  observes unclaimed shortfalls, is task192's and task196's spent ground and readability test 7.

- 2026-10-27, candidate C9-3, the displacement pair the count calendar breaks (same pairing): the genuine
  stock loss behind FY26 branch count variances, where a misbooked movement shows as an offsetting pair whose
  two sides fall in different windows of a rolling count calendar. DEAD BY IDENTITY, and the premise is
  simply false: a displacement conserves the group total whatever windows its two sides fall in, so the group
  net equals the genuine loss exactly, ratio 1.000 at three of three seeds (709 against 709, 878 against 878,
  767 against 767) with 104 of 256, 108 of 236 and 79 of 205 pairs kept inside one window, and the pairing
  window is a knob that moves nothing, spread exactly zero at every window from 0 to 3 cycles. The calendar
  breaks pairs only inside a branch-window cell, never in the reported total, so no calendar structure can
  make the netted figure wrong. The guard blocks it as well, BLOCK test.same_puzzle_older against task65 v3
  and task67 v3 and BLOCK test.same_driver_older against task65 v3 and task84.

- 2026-10-27, the candidate the reconnaissance drafted a card for and refused before any measurement,
  recorded here because it existed only in that scratch card's `notes` field: the joint condition across
  releases (a purchase commitment reaching the shared group ledger as several releases booked in different
  trading units, the authorisation control testing the band against each release, so a commitment above the
  band whose releases each sit inside it is reported by nobody). Refused on two grounds at the draw. The
  partition of releases into commitments is a keyed group-by, which is readability test 2, the schema
  announcing the step; and split-commitment testing is the field's own named procurement-audit procedure, so
  the decisive step is one a competent analyst performs by reflex and a filed sentence would name. Not
  re-proposable.

- 2026-10-27, the architecture 10 draw hunt. Two candidates drawn, gated and killed on measurement,
  one killed before any harness by a sibling slot's own measurements, and five killed on the abstraction
  test against a driver already on file. Harness at
  `/tmp/claude-0/-home-user/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/t184a10hunt/`
  (`c1_thermal.py`, `c2_load.py`), every route scored against the world's own truth, every magnitude over
  five seeds. The hunt left `accounting-audit-forensic` as the resume line said and drew a deciding
  quantity of the first kind, a quantity a field measures with an instrument or a protocol where the
  recording differs from the event. Nothing is cut and no card is registered.

- 2026-10-27, candidate C10-1, the thermal lag behind the load archive (`energy-systems-utilities` /
  `grid-reliability-outage-analysis`, anomaly-detection): the summer's true overload exposure as the
  unit-hours at which each ground-mounted transformer's winding hot-spot temperature exceeded 98 C,
  reconstructed by driving the IEC 60076-7 clause 8.2 difference equations with the half-hourly load
  archive, the unit's own factory-test time constants, loss ratio and rated rises, and the measured
  ambient, against counting the half-hours whose archived load exceeded the nameplate rating. The swap
  test passes outright (there is no oil to heat and no time constant once the nouns are another field's).
  **DEAD ON THE BIN TEST AT FIVE OF FIVE SEEDS, by an order of magnitude.** Graded to the nearest 10
  unit-hours: the decisive step is worth (a) 10.33, 13.33, 11.66, 14.54 and 12.56 bins, while the licensed
  variants of the standard's own method span (b) 230.33, 211.63, 110.32, 236.40 and 199.86 bins, and the
  archive's half-hourly grain costs only (c) 2.00, 2.53, 1.44, 2.24 and 2.08 bins. The variants are not
  exotic: the hot-spot factor at 1.1 against 1.3, the oil and winding exponents from another cooling-class
  row, the standard's default oil time constant against the certificate's, and the clause 8.1 exponential
  form without the winding overshoot terms, which between them put the figure anywhere from 474 to 1,577
  unit-hours at one seed, a factor of 3.3 on a step worth 5 per cent. Two further independent refusals
  measured on the way. The decisive step is also the SMALLEST rung gap at every seed, which the bin test
  forbids on its own. And the ladder has architecture 7's shape: the crudest route (nameplate crossings,
  1,190 against the golden 1,908) is 37 per cent low, but the first refinement any competent analyst makes,
  derating the nameplate for the day's ambient, reaches 1,804.5, closing 86 per cent of that gap and landing
  5.4 per cent from the golden. A third fact worth keeping: the difference equations cannot be stepped at the
  archive's own 30-minute grain at all, because the winding time constant is 5 to 9 minutes, so the step
  diverges and returns NaN; the sub-step is therefore another open HOW on top of (b). Guard: BLOCK, two
  clearable (`ban.artifact` on both `monitoring_export` against task304 and `register` against task139, and
  `test.same_puzzle_older` against task120 v3 wanting a differentiation line), nearest driver **0.07 against
  task245**, whose driver is "a count of periods above a level over a whole cycle, read from records whose
  gaps are not random" in this very subdomain, so the graded object is a near-twin as well. Not
  re-proposable. **The general form, which is the hunt's main finding: a decisive step that rests on a
  measurement MODEL, whether its parameters come from a standard's tabulated rows or from a fit, is priced
  by that model's own licensed family, and in both candidates measured here that family is worth 2 to 20
  times the step.** The bin test reads it straight off, and it reads it at the draw.

- 2026-10-27, candidate C10-2, the load over the flow record the round never samples
  (`physical-environmental-sciences` / `environmental-monitoring-exceedance`, anomaly-detection): a river
  basin district's annual determinand load, recovered by fitting each point's concentration-discharge
  relation on its twenty-six fortnightly grabs and integrating it over the fifteen-minute discharge record,
  against the discharge-weighted mean grab concentration multiplied by the year's logged flow. The swap test
  passes (a point source diluted by rising flow, mobilisation on the rising limb). **DEAD ON MEASUREMENT,
  three ways.** First the bin test, graded to the nearest tonne on a district figure near 500 to 800 t:
  (a) 6.35, 116.15, 83.70, 67.95 and 21.48 bins against (b) 57.52, 47.50, 22.19, 72.98 and 84.38, so it
  fails at three of five seeds, and the step's own worth swings eighteenfold across seeds while the variant
  spread holds steady, which makes the separation the draw's and not the design's. (c) is negligible at
  0.03 to 0.07 bins, so the fine-grain forcing file was never the problem. Second, the accuracy condition
  of 1.1f: at seed 21 the Beale ratio estimator lands 1.061 of the truth and the golden 0.920, and at seed
  25 Beale lands 0.997 against the golden's 0.947, so at two of five seeds a cheaper licensed field
  estimator is NEARER the truth than the golden. Third, the variants that produce (b) are the
  retransformation family nobody can close: the smearing estimate against Ferguson's `exp(s2/2)` against no
  correction at all, a rating linear in discharge, a load-discharge rating, and a seasonal rating, spanning
  544.6 to 602.1 t at seed 21. Guard: BLOCK on three structural tests, `test.same_puzzle` against task487
  inside the batch, `test.same_driver` against task271 v2 and task308 v1 lineage and `test.same_driver_older`
  against task471 v1 lineage; and the kill that needed no measurement at all, nearest driver **0.06 against
  task452's lineage v1**, whose driver is this candidate word for word with other nouns, "a period total of
  the product of two series, one recorded at every interval and one sampled on a few intervals that mostly
  catch the quiet state; the sampled factor rises with the recorded one, so carrying the sampled values
  across the unsampled intervals, by averaging or interpolating" and it is a spent architecture in this very
  domain. Not re-proposable. The residue: the whole bite is the covariance of two series, the mean of a
  product against the product of means, which is the averaging cell task229's convex-conversion driver
  already spends and which the architecture 9 constraint closes.

- 2026-10-27, the specific sound level corrected for the residual: killed before any harness by
  `guard.py slots`, on another slot's measurements. The candidate was the count of night periods at which a
  plant's own specific level exceeds the consent limit at a receptor, recovered by energy subtraction of the
  residual the plant's recorded shutdown windows measure, against reading the monitor's total level against
  the limit. `slots` returns task182's architecture 3 feasibility block, which screened exactly this and
  measured both halves: the decisive step separates (the shutdown-window residual against the residual that
  describes the assessment period swaps one position of a slate, the error running about 7 dB one way at the
  roadside positions and 4.5 dB the other at the hedgerow positions), and the residual's own functional
  family moves every printed level, the decibel-linear form sitting 1.4 to 1.6 dB below the energy-linear
  form at all fourteen positions and the lowest-decile form 2 to 5 dB below the truth, against figures
  printed to the tenth. That is this hunt's finding measured a second time in a third world, and it is the
  same shape as C10-1's: the model family outprices the step. Not re-proposable.

- 2026-10-27, five candidates killed on the abstraction test before any harness, each naming the build whose
  driver it repeats once the nouns are stripped. (1) Informative instrument downtime, the periods a monitor
  loses being exactly the periods the measurand is extreme, recovered from the fault log and a paired
  station: task180's driver (the record omits exactly the events it was least able to record) and task245's
  outright, same subdomain. (2) The meter error curve inverted per interval to recover true throughput: this
  slot's own architecture 8 (invert a known nonlinear observation map per record to recover a latent total,
  the easy route applying the map's average), and the architecture 9 constraint. (3) A per-record inverse
  detection or claim probability read off a shipped record: candidate C9-2's ground, which the guard blocks
  in four earlier builds. (4) The diffusion-tube bias adjusted at the concentration being converted:
  task185's driver exactly (a device agreeing at ordinary values and departing at high ones). (5) Run-order
  carryover between consecutive analyses, recovered from the blanks that follow high samples: refused on the
  client's rule 3 first bullet, because the decisive step is the discovery of an unreported defect planted in
  the data, which is a planted defect however physical the mechanism. A detection limit (task189) or a
  detection threshold (task180) is a reported property of the instrument and is not the same thing.

- 2026-10-27, what the architecture 10 hunt closes, stated as the filter the next draw has to pass. The two
  measured kills and the one screened kill fail for one reason, and it is sharper than the architecture 9
  constraint: **the decisive step may not be priced by a model of the measurement.** Whether the model's
  parameters come from a standard's tabulated rows (C10-1: the hot-spot factor and the exponents), from a
  retransformation family (C10-2: smearing against Ferguson against none), or from a regression on a
  residual (task182's architecture 3), the family's spread on the graded figure runs 2 to 20 times the
  step's own worth, Gate C dies where Gate F lives, and no bin, world parameter or pin repairs it, because a
  coarser bin brings the first refinement into the golden's bucket. With 1.1j already forbidding a fitted
  estimator and 1.2a already forbidding a records-fixed quantity to carry a correction, the live cell for
  architecture 11 is narrow and can be written down: the quantity has to be unobserved, the reconstruction
  has to be arithmetic-closed on a piece the records supply exactly at a grain no grouping of the decision
  file reproduces, and the difficulty has to sit in WHICH rows or WHAT structure rather than in any
  parameter. Every instrument-process instance this hunt could name for that cell reduced either to
  rule application (the arithmetic is closed, so a competent analyst who sees the structure executes it) or
  to one of the twenty-two drivers already on file for this objective; the enumeration is in this entry's
  predecessors. A draw that cannot name its arithmetic-closed piece is not a candidate.

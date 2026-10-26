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

**Data-native sentence.** A single route-accounting voucher carries a whole van round, a day of counter sales
posts as one EPOS voucher and a manual journal carries one posting, so the number of postings behind one
journal entry in this ledger runs from 1 to about 1,400 inside the same trading unit; the monitoring platform
records its verdict on the voucher, so the same indicator means "one posting tripped the ruleset" on a manual
journal and "at least one of 1,400 did" on a van-sales batch, and the map between the two is saturating.

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

**Ends on:** 10,587 postings for the group, with the twelve unit figures running 579 to 1,316.

A sharper analyst notices the entry is not the posting, takes the flag rate per entry and grosses it up by
the group's posting count.

**Ends on (the sharper route):** 31,282 postings for the group.

**Golden:** 22,195 postings for the group, to the nearest thousand, with each unit's figure to the nearest
hundred.

Both default figures are wrong by a factor, not a margin: the flag count is 47.9 per cent of the golden's
basis and the grossed-up rate 141.6 per cent of it.

## Stump sentence

The analyst reports the monitoring platform's 10,587 flagged entries as the number of postings that tripped
the ruleset for the year to date (or 31,282 from the entry flag rate grossed up by the group's postings); the
step that lands there is treating the entry verdict as one observation of one posting, when it is an
indicator that fires once however many of the voucher's postings trip the rule, so the count has to be
recovered by inverting one minus the complement raised to the postings on the entry, entry by entry, with the
rate estimated on each trading unit's own population.

## Three rules

`Task type:` audit-testing-sampling. The task sizes an attribute test: it estimates the deviation rate in a
population at the unit the control applies to, which is what the task type exists for and what the objective
anomaly-detection needs here (the real deviation count separated from the artifact the platform's reporting
grain produces).

`Domain test:` the deciding quantity is a population deviation rate at the item subject to the control, the
figure an auditor estimates to size an attribute sample and to allocate testing across components of a group.
The field's own method defines the sampling unit as the item the control operates on, and here the evidence
arrives at the accounting document's unit instead, so the rate has to be recovered from the document-level
indicator before any sample is sized.

`Swap:` put shipping container for journal entry and damaged carton for tripped posting. The arithmetic still
inverts, but nothing then says what the unit of observation ought to be, because only an audited population
has a standard that defines the item subject to the control; and nothing makes the container's internal
composition recoverable, because only double-entry writes each source document as its own balanced set of
lines. The swap leaves a counting exercise with no reason to prefer either unit and no route to the fan-out.

`Layer 1:` the ledger's own mess, none of it placed to be caught. The EPOS interface changed its voucher
convention mid-year (one voucher a day per depot, then one a day per till), so the posting fan-out per entry
steps down at the cut-over; the route-accounting interface posts in the depot's local time while the platform
stamps its verdicts in UTC, so a van's day straddles the period boundary twice a year; the payables interface
restates a supplier's accruals in a later period without reversing the first posting, so the same source
document appears under two entries; unit codes were renumbered at the half-year and the register carries the
old ones; and the group's period calendar is a 4-4-5 fiscal month against the platform's calendar months.

`Layer 2:` `estimand_identification`. The decisive choice is what the rate is a rate of, and therefore what
the observation is: the platform's row is a voucher, the decision's unit is a posting, and the map from the
posting rate to the voucher-level indicator rate saturates with the postings on the voucher, so no rescale of
the indicator count recovers the posting count.

`Decisive step:` recover the population deviation rate at the posting by inverting the voucher-level
indicator, entry by entry, over each trading unit's own population, rather than rescaling the indicator
count to or from the voucher population.

`Not semantics:` every field reads exactly as it is labelled and the analyst reads it right. The register's
row is a flagged journal entry and says so, the entry header's item count is the postings on the voucher and
says so, and the rule catalogue states each rule's evaluation grain. Reading all three correctly is what
produces the two default figures: knowing that the row is a voucher and that the voucher holds 1,400 postings
is exactly what licenses "flags over entries, times postings", which is wrong by 1.42 times. The answer does
not turn on any field's meaning; it turns on the shape of the map between the two units.

`Not rule application:` no filed rule or procedure performs the recovery. The rule catalogue says what each
rule tests and at what grain; the monitoring platform's documentation says it retains a verdict per entry;
neither says, and no shipped sentence says, that the indicator saturates or how to invert it. Executing every
stated rule produces the register and the two default figures, which is what the analyst test files.

`Analyst test:` a strong analyst keeps the posting-grain rules, counts flagged entries per unit and reports
10,587 for the group, or grosses the entry flag rate up to 31,282. Executed in `checks.py` on the
generator's clean truth, both routes reproduce those figures and the golden reproduces 22,195.

`Estimand:` the number of postings in the group's general ledger, in the financial year to date, that trip
the continuous-monitoring ruleset, counted for each trading unit on that unit's own population and summed to
the group. Filed in the prompt's question and in `exception_population_bridge.xlsx`'s scope note; the unit of
estimation is part of the WHAT, which is why the prompt asks for the figure per trading unit and for the
group (`determinism-check` section 1).

`No decoy:` nothing is planted to be caught. There is no copied block, no hidden rule, no memo or briefing
arguing a figure, and no stakeholder number written to be overturned. Every artifact speaks in entries,
because that is what the platform records; none states a posting count.

`No certified replay:` no certified or published figure is reproduced by the method, and no artifact blesses
either route. The platform's monthly summary ties to the register under every route, because both are counts
of entries.

`Lesson:` that an indicator recorded on a container of items is not an observation of an item, so the rate
the decision needs is recovered by inverting the container-size map rather than by rescaling the count, and
that the rescale is wrong by a factor whichever direction it is taken. No build on file teaches it: the
corpus's nearest drivers sit at 0.07.

## Measured at the draw

Six independent seeds of the generating model, each with the twelve units' goldens placed mid-bin by the
generator's own per-unit search. `golden` is the estimand executed literally; `clean truth` is the
generator's count of postings that actually trip the ruleset, which nothing ships.

| seed | golden | clean truth | golden / truth | flag count | as % of truth | entry rate grossed up | as % of truth |
|---|---|---|---|---|---|---|---|
| 3  | 22,195 | 22,098 | 100.44% | 10,587 | 47.9% | 31,282 | 141.6% |
| 11 | 22,697 | 22,573 | 100.55% | 10,491 | 46.5% | 30,846 | 136.6% |
| 19 | 22,510 | 22,570 |  99.73% | 10,432 | 46.2% | 30,892 | 136.9% |
| 27 | 26,114 | 26,099 | 100.06% | 12,166 | 46.6% | 36,064 | 138.2% |
| 41 | 26,096 | 26,169 |  99.72% | 12,035 | 46.0% | 35,531 | 135.8% |
| 55 | 25,702 | 25,512 | 100.74% | 12,203 | 47.8% | 34,949 | 137.0% |

**The three conditions a corrected route owes** (`stumping` 1.1f), each asserted separately in `checks.py`:

1. **The default path lands outside the bin.** The flag count is 46.0 to 47.9 per cent of clean truth and the
   grossed-up entry rate 135.8 to 141.6 per cent of it, against a graded bin of plus or minus 2.3 per cent on
   the group figure. The nearest wrong route sits 36 per cent away, against the 6 per cent `C4` floor.
2. **Every licensed estimator lands inside the bin.** Method of moments on the total, the full per-entry
   maximum likelihood and the complementary log-log form, each run on each unit's own population and summed,
   span 0.95 to 1.08 per cent of the group figure and 0.92 to 1.13 per cent (median) at unit level, worst unit
   1.29 to 1.81 per cent. At every one of the six seeds all twelve units and the group total round to one bin.
   Each golden sits within a tenth of a bin of its centre.
3. **The golden is strictly more accurate against clean truth.** 99.72 to 100.74 per cent, against 46.0 to
   47.9 per cent for the default. The correction is 30 times closer, not marginally closer.

**The grouping fork, closed twice.** Estimating one rate for the whole group and estimating a rate per unit
are both defensible, and on an earlier tuning of this world they differed by 6 to 8 per cent on the group
total, which would have been an open Gate C cell on the call itself. Two closures now hold together: the
estimand files the unit of estimation, which is WHAT and not HOW, and the prompt asks for the figure per
trading unit and for the group, so the literal reading fixes the grouping; and on the shipped tuning the two
groupings converge anyway, to within 0.07 to 0.35 per cent of the group figure at every seed, well inside the
bin. A solver who pools lands in the same bin.

**Why the saturation and the identification do not fight.** This is what killed architectures 3 to 7: the
structure that made the easy route wrong was the same structure that destroyed the answer's determinacy. Here
they live in different entries. A real general ledger is heavy-tailed in entry size, so the manual journals
and single-document postings (about 30 per cent of postings, about 95 per cent of entries) are nearly
unsaturated and identify the rate precisely, while the interface batches (about 55 per cent of postings, a
few thousand entries) are heavily saturated and carry the hidden mass. The information for the rate and the
mass the correction moves come from different parts of the same file, so tightening one does not loosen the
other.

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

## Tried and rejected

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

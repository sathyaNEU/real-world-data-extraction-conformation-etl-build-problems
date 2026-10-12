# task124: Hollins Ford Regional Water District, the lead service line replacement schedule (architecture 2)

Private, never ships. Architecture 2 of 3, drawn 2026-10-12 at the wave-1 resume as the re-root of architecture 1
(Sabine Crest Energy's summer firm-capacity block split, harden loops 0 to 2). Architecture 1 is spent for three
reasons, each recorded in `## Tried and rejected`: its card carried `validated_decoy: true`, which the guard has
blocked outright since 2026-10-11 and which no differentiation clears; the in-house solver walked the default path
to the golden twice (round 1 by the programme baseline, round 2 by the peak days' shoulder hours), which is the
re-root rule's two failures on the default path; and loops 1 and 2 each answered a solve by stacking a rung above
the solved decisive step, which the current pipeline forbids (redesign the decisive step, never add a rung above
it). Its generator, pack, goldens, write-up, metadata and prompt were removed from this folder at the re-root (in
history at 64079f2); `solver_rounds/` and `leak_check_report.md` stay as its evidence. The card keeps architecture
1's three loops in `lineage` (v1 to v3). Nothing of architecture 1's world, pack, prompt or asks is reused.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task124.json`, architecture v4 (re-root: architecture 2), registered 2026-10-12; `guard.py check` WARN on one finding (`repeat.gate_g`, answered below); `guard.py validate` clean |
| Domain / task type | energy-systems-utilities / asset-condition-maintenance (a client domain; the asset is the water service line) |
| Objective | Forecasting & Predictive Modeling: the programme year in which each of the plan's twelve zones will be finished, from the district's records to 31 December 2026 |
| Shape | 06, sequenced schedule under capacity: each zone's finish year and running total, the deadline call, a schedule chart with its parts named |
| Decision | `schedule_or_sequence`, answer unit `date_or_period`: whether the replacement plan's annual capital finishes every zone by the federal deadline (lines replaced by 1 November 2037), and the year each zone is finished |
| Mechanism | gap population; pattern none; generators G14 (decisive: the verified yield, conditioned on why a line was dug, does not apply to a programme that digs every line), G6 (the zones' construction-era mix differs from the swept segments'), G2 (the representative unit is a main segment verified whole, built from rows); Gate G `forecasting`; strategy `population_selection` |
| Layer 2 family / pattern | `estimand_identification`; `biomedical-clinical-research/diagnostic-biomarker-accuracy/1` (partial verification biases accuracy), made here on service lines: the verified share is measured on lines dug because something pointed at lead |
| Furniture | forum `board_of_directors` (the district board adopts the capital plan), forcing event `budget_or_appropriation` (the 2027 to 2037 capital plan's annual lead service line appropriation), organisation family `cooperative_or_member_body` (a water district owned by its member municipalities), role family `programme_officer`, context artifact `capacity_report` (the 2026 programme progress report), calibration `physical_verification`, opening `question-first`, question form `when` |
| Spine | the district's service line inventory, about 88,000 rows, one service line (main to premise) with its records class, current classification, construction year, zone and the main segment it taps; synthetic, shaped on public lead service line inventories filed by Ohio community water systems |
| Deliverables | `lslr_2027_programme.xlsx` (the zone schedule and the two asks), `lslr_2027_board_paper.pdf` (the call and the schedule chart) |
| People | drawn with `guard.py names --geo "United States, Ohio" --seed 124 --n 24`: Andrew Wells (programme manager), Bethany Davidson (district engineer), Seth Sullivan (finance director), William Bates (board chair); none appears in the prompt |

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

**Abstraction and same-puzzle tests.** Stripped of nouns, the driver is: a rate measured on units examined because
they showed signs of the outcome is carried to a population every unit of which will be examined, and only the groups
examined exhaustively, recognisable by complete coverage rather than by any code, give the population's rate. The
three nearest drivers (task32 v2, a conversion rate fitted across a regime break; task83 v1, a retrained selection
model; task446 v2, a screen's yield moving with the base rate) share no latent structure, default path or
correction with it. task446 v2 is the closest in words (a yield measured on one population carried to another) and
differs in the mechanism: there the yield moves with a base rate the history shows; here the measured rate is
inflated by why units were examined, and the base rate is the same.

**Data-native sentence.** A water utility verifies a service line's material only when something sends a crew to
dig: a customer's report of lead pipe, a lead sampling site, a leak on old galvanized pipe, a dig a consultant
ranked as likely lead, or a water main replacement that exposes every service on the main; this district logs every
one under the same work-order code, so the verified lines over-represent lead, and only the main segments a
replacement verified whole are a sample of what a programme that digs every unknown line will find.

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

The pipeline a competent analyst builds from the prompt's words and the files' grain (provisional figures from the
draw-stage paper model; stage 2 re-solves every figure on the prototype):

1. Read the question: the programme year in which each of the twelve zones in the replacement plan is finished at the
   capital plan's annual appropriation, and whether the last is finished by the deadline.
2. Load the service line inventory and, for each zone, count the lines classified Lead or GRR (each is replaced) and
   the lines classified Lead Status Unknown (each is dug, and replaced if found lead or GRR).
3. Load the field verification log for 2021 to 2026, map the pre-migration legacy premise numbers through the 2023
   migration crosswalk, normalise the material codes through the field code list, join to the inventory and keep the
   verifications of lines whose records class was unknown (no usable material record, built before 1989).
4. Take the share of those verifications found lead or GRR in each construction era of the plan (before 1930, 1930
   to 1949, 1950 to 1988): about 0.78, 0.58 and 0.24.
5. Price each zone at the plan's unit costs: expected replacements are its Lead and GRR lines plus its unknown lines
   at the era shares, the rest of its unknown lines are digs that find no lead, and each zone carries its
   mobilisation.
6. Work the zones in the plan's priority order against the annual appropriation from 2027 on, a zone finished in the
   year its running cost is covered.

Ends on: 2038, the last zone finished a year after the deadline
Golden: 2036, the last zone finished inside the deadline

## Stump sentence

A competent solver joins the verification log to the inventory through the migration crosswalk, keeps the lines that
had no material record, prices each zone's unknown lines at the share found lead or GRR in each construction era
across every verification (about 0.78, 0.58 and 0.24) and files the last zone finished in 2038, a year after the
deadline; the step that lands it there is treating verifications prompted by evidence of lead as a sample of the
lines a systematic programme digs, when on the main segments a water main replacement verified whole the shares are
about 0.56, 0.31 and 0.07, every zone's cost falls by a fifth or more, and the last zone is finished in 2036.

## Three rules

- **Litmus:** no reported number is wrong and nothing overturns one. The inventory, the verification log, the
  crosswalk, the plan, the unit costs and the capital plan are all correct; the difficulty is estimating what the
  plan's digs will find from verifications whose selection the log does not record.
- Domain test: what decides the call is a water utility's estimate of how many of its unknown-material service lines
  are lead or galvanized-requiring-replacement, which inventory practice has to make from verifications that sampled
  lines regardless of their likely material, since a dig prompted by a customer's report, a sampling site or a leak
  on galvanized pipe finds lead far more often than a systematic dig; with another field's nouns there are no tap
  cards, goosenecks, GRR classifications or main-replacement sweeps, and the task does not read the same.
- Analyst test: a strong analyst who joins the verification log through the migration crosswalk, normalises every
  material code, keeps the lines that had no material record and reads the inventory, the plan, the unit costs and
  the capital plan correctly still estimates each era's lead and GRR share from every verification on file (pooled,
  by era, or with a model on every visible attribute) and finds the plan misses the deadline, because nearly every
  verification was prompted by evidence of lead and only the segments a main replacement verified whole show what a
  programme that digs every unknown line will find.
- Layer 1: realistic mess from the district's own systems: the verification log keyed by the customer system's legacy
  premise number before the March 2023 GIS migration and by the GIS service line id after it; material codes that
  differ by crew and contractor form; re-verifications of one line dated in two formats either side of the migration;
  the county assessor's construction year with zeros on non-residential parcels; and, on the ask paths only, a
  pay-application export that repeats each change order's total on every covered site's line, revised and resubmitted
  pay applications with the engineer's decisions in a separate log, and access agreements keyed by legacy premise
  numbers and carrying the zone named on the form when signed.
- Layer 2: the share of unknown lines that prove lead or GRR is not the verified share: verification was triggered by
  evidence of lead, so the verified lines are a selected sample, and the only unselected sample is the set of main
  segments whose every service was verified when the main was replaced, which no code marks and which is recovered by
  grouping the verifications by segment against the inventory (the partial verification pattern, made on service
  lines).
- **Stump class:** analytical. Rule 3 is cleared: no planted defect or decoy decides it (the verifications are real
  and correctly recorded), no field reading flips it (every code is read the same on both paths) and no stated rule
  produces it (nothing in the pack says how to estimate the unknown lines).

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

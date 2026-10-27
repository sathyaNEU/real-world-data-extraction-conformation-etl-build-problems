# task139: Copperline Vehicle Protection, whether the Fareline rideshare channel renews in 2027 at its price, at the high-use surcharge, or lapses (architecture 3)

Private, never ships. Re-rooted on 2026-10-27 for the second time. Architecture 1 (where Haverline's nurse teams work, read
per claim against per intake) was solved by both portal responses; architecture 2 (the same world, the opening call both
pilot arms received) was spent at stage 2 before any pack was cut (`## Architecture 2 record`). At the author's
instruction nothing is kept: a new world, a new task type, a new decision and a new mechanism.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task139.json`, architecture v3, registered 2026-10-27; architectures 1 and 2 in `lineage` with their fates |
| Domain / task type | actuarial-science-insurance / pricing-ratemaking-credibility (serves Forecasting): the deciding quantity is the expected claims cost of a vehicle service contract over its cover, the service-contract actuary's frequency and severity per mile of exposure by odometer, carried along each contract's mileage path to its mileage or time limit |
| Objective | Forecasting & Predictive Modeling: the lifetime loss ratio of the contracts the rideshare channel will sell in 2027, none of which exists yet, forecast from the channel's six months and the retail book's seven years |
| Shape | 04 (setting one dial: each allowed setting): the three renewal settings each carry a forecast loss ratio, with the asks' grids supplying most of the criteria (arithmetic under `## Ask sheet` at stage 2) |
| Decision | `renew_replace_lapse`, answer unit `named_option` (renew at current rates, renew with the maximum high-use surcharge, or let the channel lapse) |
| Mechanism | gap objective (the channel's cost per month of cover is correct and is not what the cover costs) then time (its six months have seen only the start of a cover that runs twenty); pattern none, generators G1 (the unit of exposure: a mile at the odometer, not a contract-month) then G13 (the horizon the channel's history covers against the horizon the cover runs); Gate G `forecasting`; strategy `grain_or_unit` |
| Layer 2 family / pattern | `field_method` (the exposure base done right); `own:exposure-on-the-odometer-not-the-contract-clock` |
| Furniture | forum `executive_team` (Copperline's executive product committee elects the renewal), forcing event `purchase_order_or_contract` (the Fareline agreement's election notice is due by 1 December 2026 for the 1 January 2027 renewal), organisation family `professional_services` (a service-contract obligor and administrator, its contracts backed by Tarrant Mutual Casualty's contractual liability policy), role family `product_manager` (the head of the rideshare and fleet programme), context artifact `register` (the contract register), calibration `existing_book_actuals` (the retail book's seven years of contracts, readings and claims), opening `question-first`, question form `which` |
| Spine | `odometer_readings_2019-01_to_2026-09.csv`, the administrator's odometer history: one reading on one contracted vehicle from a repair order, a maintenance-proof upload or the platform's weekly mileage feed; constructed |
| Deliverables | `fareline_channel_renewal_2027.pptx` (the committee deck: the election, the forecast and the chart it rests on), `rideshare_contract_experience_2027.xlsx` (the forecast's working and the asks) |
| People | drawn with `guard.py names --geo us --seed 1393` and `--seed 1397`: Nicholas Reed (head of the rideshare and fleet programme, the requester), Emily Willis (pricing actuary), Jason Livingston (claims director), Kirsten Weaver (administration systems), Philip Butler (Fareline's driver-benefits lead), Nicole Monroe (Tarrant Mutual's programme underwriter); none in the prompt |

**Guard.** `guard.py check` on the draft BLOCKed `ban.forum` (committee_or_panel) and `ban.org_family`
(financial_institution) against task304 in the window; the forum is honestly the executive team (the product committee
of a company this size is its executives), and the organisation is honestly a service-contract obligor and
administrator, a professional-services firm whose insurance sits with the contractual liability insurer, not a
financial institution. Registered at WARN: `three_rules.strategy_risk` (grain_or_unit), answered in `## Three rules`
(the unit is an exposure basis the analysis chooses, no field or rule names it); `people.first` on Kirsten (task457) and
Nicole (task243), older builds; `repeat.gate_g` (forecasting, beside task171 v5), the lane's own mechanism;
`repeat.question_form` (which, beside task270), the decision is a pick of one of three settings.

**Same-puzzle and same-driver tests.** Gap objective, decisive G1, `renew_replace_lapse`, Gate G `forecasting`: no
structural block in the last twelve or older.

**Abstraction test.** Stripped of nouns: a unit's events accrue with its accumulated use and climb steeply with it, and
the record's dominant population accumulates use slowly from a low start; a new population that accumulates four times
faster from a higher start reaches the steep part within months while its own short history shows only its beginning,
so the cost of its whole cover is read per unit of use at the same accumulated use from the slow population, not per
month of cover from either. Nearest drivers on `check` (0.06 and under): task170 v5 (a per-attempt failure probability
falling with each operator's own count), task161 (stock ahead of a cost step), task130 v4's lineage (a cover paying only
for events reported inside its own window): none reads a cover's cost on an exposure scale other than the cover's own
clock. `guard.py slots` on the mechanism's words (usage scale, per-mile hazard, mileage limit, odometer, telematics) and
the setting's (vehicle service contract, rideshare drivers, premium deficiency) returns no earlier screen of it.

**Data-native sentence.** Copperline's repair claims accrue with the miles a car is driven and climb with its odometer,
both in how often a covered part fails and in what the repair costs; a rideshare driver puts about 44,000 miles a year
on a car bought at 50,000 to 100,000 miles, so the 75,000 covered miles run out within two years at odometers the retail
book reaches only in its last years, and the channel's own six months have seen only the start of the cover.

**World.** Copperline Vehicle Protection (Fort Worth, Texas) has sold Copperline Drive Plus vehicle service contracts
through about 340 franchised and independent dealers in Texas and Oklahoma since 2019, administering its own claims; a
contractual liability policy from Tarrant Mutual Casualty insures its obligations. Drive Plus covers the powertrain and
major systems of a used car under ten model years old and under 100,000 miles at sale, for 60 months or 75,000 miles
from the sale date and odometer, whichever comes first, with a 100 dollar deductible a repair visit; the price is set
by vehicle class from the rate manual. In April 2026 Copperline opened a channel with Fareline, a rideshare platform,
selling Drive Plus to its drivers at the class price with a 20 per cent commercial-use loading. The agreement renews on
1 January 2027 and Copperline elects, by 1 December 2026, to renew at current rates, to renew with the rate manual's
maximum high-use surcharge of 40 per cent on the class price, or to let the channel lapse. The rate manual's channel
review standard: a channel renews at current rates if the forecast lifetime loss ratio of its next year's sales is 70
per cent or less, with the surcharge if the surcharged loss ratio is 70 per cent or less, and otherwise lapses. The
records run to 30 September 2026; the request is made in October 2026 by the head of the rideshare and fleet programme
for the committee's November meeting.

**On paper, before any data** (`generator/paper/` prototypes, 14,000 retail and 2,500 rideshare contracts a world; repair
claims per mile and their cost flat to 70,000 miles and climbing past it, rideshare sales from April 2026 at 50,000 to
100,000 miles and 44,000 miles a year), every route scaled to the golden at 84 per cent of the price:

| Route | Lifetime loss ratio | Election |
|---|---|---|
| the channel's own cost per contract-month over the months its drivers take to use the cover | 39 | renew |
| the same, with the cost per month's trend in contract age carried forward | 50 | renew |
| the retail book's cost by contract age, with the 20 per cent loading | 47 | renew |
| the retail book's cost by contract age on a clock sped up by the mileage ratio | 52 | renew |
| the book's pooled cost per mile, over the 75,000 covered miles | 42 | renew |
| claim frequency per mile by odometer band, at the book's average claim | 56 | renew |
| the channel's own cost per contract-month over the full 60 months (the mileage limit dropped) | 110 | lapse |
| golden: cost per mile at each odometer from the whole book, along each contract's mileage path to its limit | 84 | renew with the surcharge (60 surcharged) |

The nearest route sits 14 points under the renewal line and the golden 14 points inside each edge of its band; the build
measures both on the pack before stage 3.

## Three rules

- **Task type:** actuarial-science-insurance, pricing-ratemaking-credibility (serves Forecasting): the lifetime loss
  ratio of next year's rideshare sales, forecast from the exposure each contract will run before its limit.
- **Domain test:** the deciding quantity is the expected claims cost of a contract over its cover, which the service-contract
  actuary builds as frequency and severity per mile of exposure by odometer band, the exposure base the cover's wear
  generates, carried over each contract's mileage path to the earlier of its mileage and time limits; the 70 per cent
  standard reads that cost against the price.
- **Swap:** "should a hospital renew its agency-nurse contract at the current rate, with a surcharge, or not, from the
  agency's first six months" has no dual mileage-or-time limit, no covered parts that wear with use, no repair cost that
  climbs with an odometer and no earned exposure base for a cover; the quantity the call turns on, cost per mile at the
  odometer, has nothing to be, and the task stops reading the same.
- **Layer 1:** odometer readings from three sources (repair orders, maintenance-proof uploads and the platform's weekly
  feed) at different grains, with typed and rolled values; contract numbers re-keyed when the administration system
  moved in 2024, joined through a crosswalk; claims at repair-order line grain with authorised, paid and reversed lines
  and goodwill payments; cancellations refunded pro rata by days or miles with dealer chargebacks; dealer-remitted
  premium bordereaux in each dealer's layout; vehicles by VIN with make and model-year normalisation. Each is what these
  systems write; none is placed to be caught, and none carries the call.
- **Layer 2:** `field_method`, the exposure base done right: the cover's cost accrues per mile driven at each odometer,
  so it is read per mile at the odometer from the population that has driven every band and integrated along the new
  contracts' faster mileage paths to their limits.
- **Decisive step:** cost the cover per mile at the odometer rather than per month of cover, reading each odometer
  band's frequency and claim cost from the retail book and running every 2027 rideshare contract's mileage path through
  them to the earlier of its 75,000-mile and 60-month limits.
- **Not semantics:** every field, code and unit read correctly (the terms, the readings, the claim lines, the
  deductible, the loading) still leaves the easy route on the channel's own cost per contract-month: nothing in the pack
  marks the odometer as the clock, the channel's months are real, correctly priced experience, and the step is an
  exposure choice the analyst makes.
- **Not rule application:** the terms file the cover (60 months or 75,000 miles) and the standard files the 70 per cent
  line and the population (next year's sales, like this year's); no rule names an exposure base, a band or a curve.
  Enumerated family on paper: eight constructions spread the lifetime loss ratio from 39 to 110 per cent (71 points,
  three elections); the standing family (cost per mile at the odometer from the whole book, by 5,000-, 10,000- or
  20,000-mile bands or a fitted curve, frequency and severity separately or together) is measured on the pack at stage 2
  and must file one election; what rules the per-month routes out is one cross-section nothing invites: the retail
  book's cost per mile by odometer band, flat to 70,000 miles and nearly ten times as high by 160,000.
- **Analyst test:** a strong analyst who reads the terms, the readings, the claims and the standard correctly takes the
  channel's own cost per contract-month over the months its drivers need to use 75,000 miles (or the retail book's cost
  by contract age with the loading, or a pooled cost per mile), forecasts a lifetime loss ratio between 39 and 56 per
  cent and renews the channel unchanged; only the cost per mile at the odometer files the golden (asserted in
  `checks.py` on the generator's clean truth).
- **Estimand:** the rate manual's channel review section (`drive_plus_rate_manual_2026.pdf`): the lifetime loss ratio of
  the contracts the channel will sell in its next year, the claims Copperline pays over each contract's cover (covered
  repairs net of the deductible, at 2026 repair costs, no trend) over the contract price, for contracts like those the
  channel sold in its first year (vehicle, odometer at sale, driving); renew at current rates at 70 per cent or less,
  with the 40 per cent surcharge if that brings it to 70 or less, otherwise lapse. Population, outcome, window, unit and
  comparison are filed; the exposure base is not.
- **No decoy:** no memo, briefing, prior review or stakeholder figure states a cost, a loss ratio or an election; the
  20 per cent loading is the price Copperline actually charged, a fact of the contracts, never argued as adequate; the
  dealer bordereaux and the cancellation file are declared distractors that rank nothing.
- **No certified replay:** no published loss ratio, prior channel review or certified figure ships, so the exposure
  base cannot be recovered by matching certified numbers; the retail book's experience is raw records every route uses.
- **Lesson:** a cover's cost accrues on the scale its wear runs on, and a population that runs that scale four times
  faster from further along it is costed per unit of use at the same accumulated use, from whoever has driven that far,
  never per month of cover from its own short start. No build on file reads a cover's cost on an exposure scale other
  than the cover's own clock (task130 v4's lineage reads a reporting window, task170 v5 an operator's own attempt count).

## Default path

1. Read the terms (60 months or 75,000 miles from sale, 100 dollar deductible) and the channel review standard (renew at
   70 per cent or less; with the 40 per cent surcharge if that reaches 70; otherwise lapse).
2. Build the rideshare contracts from the register (sold since April 2026) and their claims from the repair-order lines
   (paid net of reversals, the deductible taken off).
3. The channel's cost per contract-month: its claims cost over its contract-months in force to 30 September 2026.
4. The months of cover a 2027 contract runs: 75,000 miles over the channel's average driving (from the platform feed),
   about 20 months, under the 60-month limit.
5. A 2027 contract's lifetime cost is step 3 times step 4; over the average 2026 price, the lifetime loss ratio.
6. Apply the standard.

Ends on: renew the channel at current rates (a lifetime loss ratio of about 39 per cent on paper).
Golden: renew with the maximum high-use surcharge (about 84 per cent at current rates and 60 per cent surcharged).

## Stump sentence

A competent solver costs a 2027 rideshare contract by its months of cover, the channel's own claims cost per
contract-month run over the months a rideshare driver takes to use the 75,000 covered miles (or the retail book's cost by
contract age with the loading, or the book's pooled cost per mile), forecasts a lifetime loss ratio between 39 and 56 per
cent and files renew the channel at current rates (Ends on); the step that lands it there is costing the cover by its
months, when repair claims accrue per mile and both their frequency and their cost climb with the odometer past 70,000
miles, and a rideshare cover runs from 50,000 to 100,000 miles at sale through 75,000 miles more in under two years, past
anything the channel's six months have reached: read per mile at each odometer from the retail book and stopped at each
contract's limit, the cover costs about 84 per cent of the price, so the channel renews only with the maximum high-use
surcharge, at about 60 per cent.

## Architecture 2 record (spent 2026-10-27)

Haverline Workers' Compensation Trust, the same seventeen Early Return Nursing teams as architecture 1, re-rooted on the
opening call both pilot arms had received before the file was randomised (the default path read the usual-handling arm
as a unit with no team; the golden read the call's saving from the intakes the triage screen never drew). Registered
2026-10-26 and spent the next day at stage 2 before any pack was cut: the decisive step rested on one sentence of the
pilot protocol, which a careful reader meets first, inside the world the portal had already solved.

## Architecture 1 record (spent 2026-10-26)

Haverline Casualty Company, a stock carrier writing Missouri employers; drawn 2026-10-12, shipped 2026-10-15 (commit
1384f0e9, `target.zip` sha256 da3c19bf42dff8ef; checks.py 343 assertions, verify.py, byte-identical rebuilds,
figures_check 67, precut 49 with 0 FAIL, voice-check PASS, leak.py REVIEW answered, guard heart PASS, surface exit 0).
Stage 4: the leak reader found no leak (Q6 analytical); the judge returned NOT_DETERMINISTIC on supplementary 3 only,
FIX_NOW applied (the intake filed as a WHAT in the dictionary, Ask 1's silent device redrawn as EDI resends merged into
their claims), and the re-judge DETERMINISTIC and APPROVE, stump power moderate (`determinism_check_report.md`,
`determinism_check_report_pass2.md`).

**The design.** The pilot's nurses kept a fifth to a quarter of the strain intakes from ever paying indemnity, and the
review verified 100 indemnity claims a unit and group, so ERN's verified claims were the costlier remainder. The default
path compared the two groups' mean verified claim and valued a team per place-day of an indemnity claim; the decisive
step read the pilot per assigned intake (each group's share paying indemnity times its own verified severity) over an
ERN intake's place-days. The ladder: per verified claim 0 3 0 3 2 3 3 3 at 2,048,524 (booked 2,000,000); the per-claim
family 2.0 to 2.2 million; per assigned intake without the place-day 3,793,208, with an indemnity claim's place-days
3,398,667, without the fill check 4,200,799; the golden 3 3 2 0 3 3 0 3 at 4,105,562 (booked 4,100,000), RW-SS held to
the two teams its 944 intakes keep in use (teams listed HC-SS, HC-OT, RW-SS, RW-OT, MF-SS, MF-OT, CN-SS, CN-OT).

**Portal result, 2026-10-26.** Both responses placed three teams each in HC-SS, MF-SS, MF-OT, CN-OT and HC-OT, two in
RW-SS and none in RW-OT or CN-SS, and booked the 4.1 million dollar credit, with the workbook and the note: the golden
exactly.

**Why it was reachable, and it is not a near miss.** Reading a randomised pilot per assigned intake is the textbook
reading, analyse as randomised, which this note quoted as the client's pin, so readability test 3 fired on the decisive
rung where the screen had recorded it silent; the default path it overturned conditions on a status the treatment
moves, which a strong analyst refuses by reflex. And the whole ladder sat inside the register's two arms: once a reader
read the arms per intake, nothing in the pack was left to find.

**The constraint it leaves.** Inside the two arms the per-intake contrast is unbiased and the design forces it, so any
further step there is a stratification of it (the triage tier, the office), the opponent's first group-by, or a
transport of its average onto the intakes the 2027 teams reach, which is task177 v2's driver and needs that population
filed. Architecture 2 finds what the two arms share that the counterfactual lacks: the opening call.

## Tried and rejected

- The seed's light-duty conditioned yield (the saving exists only at employers with a record of temporary-partial
  payments, carried onto segments whose mix of such employers differs from the pilot's): a conditioned yield under a
  composition shift, pattern E and `composition_mix`, both spent on task137 inside the ban window; dropped at the draw.
- The saving per place-day alone (Little's law on the pilot's files, the teams valued per place-day rather than per
  claim): a strong solver computes a capacity-bound team's yearly throughput by segment by reflex once the charter
  states twenty places; kept as a rung, never the decisive step.
- An Erlang loss model on the triage stream (intakes lost when every place is taken): the effect is under a sixth of a
  team's value at matched load, it never moves a whole team, and a replay or a monthly fluid model files a different
  figure from the formula; rejected on determinism.
- A transient count of 2027 intakes from empty teams on 4 January (the first twenty in each team): the answer turns on
  the whole duration distribution and a reading of the AY window, `time_semantics` is spent on task138; closed instead by
  the pick memo's run-rate convention.
- A twelve-month pilot drawing one in three intakes with 40 to 50 verified claims a stratum (2026-10-15): a segment's
  realised saving per team-year had a standard deviation of 120,000 to 300,000 dollars across draws against values of
  120,000 to 330,000, so the segment ranking was noise; the pilot runs 24 months and the review verifies 100 a stratum.
- The review as a census of every pilot indemnity claim (2026-10-15): it would cut the noise further, but the join of the
  review to the register would then show 451 usual-handling claims against 338 ERN claims in healthcare strains, the
  frequency effect on the surface of the file the default path reads; the review samples a fixed 100 a stratum.
- A check run sent twice with its cancellation only in a treasury register (Ask 2's first device, 2026-10-15): the
  register would have been a single-purpose file announcing the device, and a duplicate run whose checks are voided after
  the pull leaves "paid" indeterminate; replaced by the line grain and the bank's returns.
- The draft charter's "units with the most intakes would be considered first" (stage 3, 2026-10-15): a staff draft
  stating a placement basis reads as a decoy draft (R3c); the draft now leaves the basis to be settled with Pricing.
- Ask 1's two devices left silent (stage 4, 2026-10-15): the judge's literal reader took `time_off_at_report` as the
  dictionary then defined it and counted both listings of a parallel-run claim, so the golden held only under the
  author's reading (NOT_DETERMINISTIC, FIX_NOW); a silent label switch and an unkeyed double listing cannot be both
  silent and forced, so both are filed and the ask's silence is gone.
- Ask 1 regenerated to the flag as filed (stage 4, 2026-10-15): it would count later indemnity conversions and the
  parallel run's second listings as intakes against charter 4.1, mark the careful count wrong and leave the ask with no
  device; the organisation's definition is filed instead.
- The parallel-run note without its fields (stage 4, 2026-10-15): matched on office, segment, class, injury and report
  dates without `disability_began`, one converted claim listed once pairs a new-number claim; the note names all six.
- Memo paragraph 2's restated comparison (stage 4, 2026-10-15): "what those intakes would pay with their adjusters
  alone, less what they pay with a team" restated the credit as a subtraction over the intakes, which the judge read as
  the estimand stated nearly literally; the credit is stated once and the counterfactual left to charter 4.2.
- A second form for the review's control digit (stage 4 realism, 2026-10-15): the digit sits on the call's join of the
  review to the register, so a second form would be a main-path mess item; the references and remarks vary instead.
- The FIX_NOW pass's Ask 1 (stage 4, 2026-10-15): both devices filed for determinism and nothing silent left, the cracker
  landing all eight figures and a pair of 58.2; redrawn with the merge file.
- A state FROI filing log carrying the cancels of claims filed in error (Ask 1 redraw, 2026-10-15): a second source of
  reported lost-time claims in the state's voice, its originals counting later conversions as reports and a cancel for a
  wrong-carrier report not plainly outside "intakes"; the claims system's own merge file instead.
- A closed-outcome field on the extract (Ask 1 redraw, 2026-10-15): a value naming the device rows in the habitual file
  is a marker, and its denied or withdrawn outcomes in the call's window would move the fill count when mishandled.
- Legacy claims parked as unassigned (G9) and converted to GN-AL (Ask 1 redraw, 2026-10-15): the injury class cannot be
  recovered from the class code, so the true segment would be a guess.
- 2026-10-26, architecture 1's decisive step (the pilot read per assigned intake, each group's own indemnity-claim rate
  times its own verified severity, instead of per verified indemnity claim), after both portal responses landed the
  placement and the 4.1 million credit. Spent, not repairable: analysing a randomised pilot as randomised is the
  domain's own reflex, so readability test 3 fires on the decisive rung, and the whole ladder sat inside the register's
  two arms, so a reader who reads the arms per intake has nothing left to find. Every further step inside those arms is
  a stratification of the contrast or a transport of its average, both spent or filed. The re-root is recorded in
  `## Portal result and the stage 2 diagnosis`.
- 2026-10-26, at the architecture 2 draw: the triage tier as the decisive step (2027 teams take intakes highest
  predicted lost time first, so a unit's teams reach the top of its tier distribution, where the file saves least in the
  strain units and most in the other-injury units). Measured on paper (200,000 intakes a unit, five tiers): the golden
  4.28 million against the pilot average's placement at 4.16 million, both booking 4.3 million, so the credit did not
  separate; the stratification by tier is the opponent's first group-by, the teams' population has to be filed, and the
  driver is task177 v2's (a randomised average carried to the part of the population the deployment reaches).
- 2026-10-26, at the draw: employer spillover (a nurse's suitable-duty work at an employer also helping its
  usual-handling claimants), the randomised contrast understating the at-scale effect: the interference family of
  task131 v1 and task249, a parent unit's shared resource; dropped unmeasured.
- 2026-10-26, at the draw: the file's effect falling with the team's load (the pilot ran below the full load 2027
  teams will carry), a dose-response read from the pilot's daily open-file counts: a fitted curve with a free form,
  and a randomised average carried to one covariate value again; dropped.
- 2026-10-26, at the draw: the pilot's claims developed to ultimate arm by arm (a file closing claims sooner, so one
  set of book factors overstates ERN's ultimates): the chain-ladder variants a reader would defend fork the graded
  figures (stumping 1.6a's task194 death), and the review already projects the open claims; dropped.
- 2026-10-26, at the draw: segment savings blended by credibility before placing: shrinkage is the opponent's reflex,
  and the credibility standard would have to be filed, which is the method; dropped.
- 2026-10-27, architecture 2 spent at stage 2 before any pack was cut (the opening call both pilot arms received): the decisive
  step rests on one sentence of the pilot protocol, which a careful reader meets first, and the world is the one the portal
  already solved; re-rooted at the author's instruction for a fully fresh architecture.
- 2026-10-27, architecture 3 draw screens, each dead before a card: a larger die's yield read through the wafer-level
  spread of defect density (task143's driver, a joint chance under a shared group effect, in new nouns); regression
  dilution corrected with replicate readings (task166 and task178: the probe's reflex); delayed entry for a taken-over
  book (task133); hearing-loss claims filed after separation (task166's lineage, the probe sliced claimants by status);
  non-synchronous covariances (task135); a first claims-made year's cost from the report-lag pattern (task130 v4's
  lineage, and the same-calendar-year claims give it in one filter); long-term disability reserves without the coming
  Social Security offsets (the field's standard assumption, so a reflex); second deaths after a bereavement (last year's
  claims rate lands it); a miners' trust's amount-weighted release (task171's screen: last year's release lands it).
- 2026-10-27, the rideshare channel opened in January 2025 or 2026: with nine or more months of its own experience, the
  channel's cost per contract-month by contract age, its trend carried forward, landed inside the golden's band; opened
  in April 2026, its six months stay on the flat part of the wear curve and the trend files renew.
- 2026-10-27, a retail book sold across 20,000 to 100,000 miles: its cost by contract age with the loading reached 72 to
  81 per cent, inside the band; the retail book is now mostly sold at 15,000 to 55,000 miles, with a fifth at 60,000 to
  115,000, which drives every odometer band the rideshare cover reaches.
- 2026-10-27, cost per mile rising as a power of the odometer from zero: the channel's own six months saw the rise and
  its trend landed; claims are flat to 70,000 miles and climb past it, as major components start to fail.

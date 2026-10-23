# task171 design note

**Status: PAUSED, architecture 4 spent at Gate F at stage 4 on 9451b6bd (2026-10-23); the number stays open and the next cell comes from the main session.**
The cell is economics-econometrics / forecasting-forecast-evaluation; the draw is a turnpike authority's first
all-electronic tolling year and the toll it will collect on what it bills by mail. Architectures 1 to 3 are kept under
`## Earlier screens`.

## Draw

- **Cell, and why this one.** The coordinator left the cell to this build on four conditions: the forward window
  changes the process in a way no file states, the decisive step is not the textbook set-up of the obvious
  calibration, no ask device is visible hygiene, and no cell named in this note or a sibling's `## Rebuild` is reused.
  Client domain Economics & Econometrics (a public authority's revenue forecast is a fiscal read), task type
  `forecasting-forecast-evaluation` (serves Forecasting). The healthcare utilization cell was screened first and died
  on code (`## Tried and rejected`), and `urban-regional-science` with Forecasting is banned by `ban.pairing` against
  task175, which is where a toll road would otherwise sit. In 2027 the Authority removes its cash booths: every vehicle
  without a transponder is billed by mail. How much of that toll is eventually collected is not on file; it is
  measured on the overnight hours since 3 March 2025, when the booths have been closed and the cash lanes' users
  billed by mail. The textbook calibration matures those invoices by their own age (six months, a year). The
  enforcement cycle does not: an in-state plate's invoice unpaid at 60 days is collected at the plate's next two-year
  registration renewal, so in a twenty-month record most in-state invoices are still waiting, and the matured share is
  read on the invoices whose plate has passed its renewal since the hold.
- **World.** The Marrowfield Turnpike Authority, a fictional public authority running a fictional 48-mile toll road
  with three mainline barrier plazas in an unnamed US state (people, systems and records fictional; the field's method
  real). Its toll-by-mail back office invoices each plate monthly; the state Motor Vehicle Division places a
  registration hold on in-state plates; a collection agency works out-of-state plates and returns what it cannot
  collect. The AET programme manager files the first AET year's toll-by-mail revenue in the revenue certificate to the
  bond trustee. Records to 31 October 2026.
- **Card.** `domain` economics-econometrics, `subdomain` forecasting-forecast-evaluation, `objective` forecasting,
  `shape` single-figure, `decision_type` quantity_figure, `answer_unit` currency, `gap` [time, population], `pattern`
  [none, E], `generators` [G13, G14, G7], `gate_g` forecasting, `calibration_form` existing_book_actuals,
  `stump_strategy` maturity_censoring, `context_artifact` planning_thread, `role_family` programme_officer, `forum`
  customer_or_counterparty, `forcing_event` cutover_or_migration, `org_family` government_agency; `stump_class`
  analytical; `layer2_family` estimation_fit; `layer2_pattern`
  own:toll-by-mail-ultimate-collection-matured-on-each-plates-registration-renewal. People from `guard.py names --geo
  us --seed 171`: Brittany Moon (AET programme manager), Zachary Mcneil (toll-by-mail back office).
- **Axes, and why each value is the honest one.** The last three live cards (task170, task274, task175) hold
  committee_or_panel, board_of_directors and executive_team; budget_or_appropriation, audit_or_inspection and
  statutory_or_regulatory_filing; hospital_or_health_provider, cooperative_or_member_body and utility_or_infrastructure;
  strategies other, population_selection and composition_mix; roles other, operations_director and finance_controller.
  The forecast goes into the annual revenue certificate the trust agreement requires the Authority to deliver to the
  bond trustee before the AET year, so `customer_or_counterparty` is the forum; the forcing event is the cutover
  itself; a public authority is a `government_agency`; the requester runs the AET conversion programme
  (`programme_officer`); the decisive move is a censoring construction on a clock each payer carries
  (`maturity_censoring`); the population step (the cash lanes' own users, not the violators) is the supporting E.
- **Pattern labels.** The stage-3 relabel (decisive pattern E, generators reordered) was reverted to the draw's labels, pattern [none, E] and generators [G13, G14, G7], which pass `guard.py check` with WARN only.
- **Stage 3 record (2026-10-23).** `generator/build.py`: checks 69 of 69, verify 0 problems, two byte-identical
  rebuilds, target.zip 9451b6bdf0182a8eff3f67f3dc4e30d6; figures_check 43 of 43; precut 51 checks, 0 FAIL;
  voice-check PASS (967 characters). `leak.py` REVIEW, four lines answered: the plan and the policy share the call's
  plain words (toll, billed by mail, revenue certificate) and print no figure of it; the policy's registration and
  renewal sentences (4.1, 4.2) are the enforcement rule the record runs on and say nothing about when a book has
  finished collecting. `guard.py surface`: no persona pair; ten promoted pairs on axis collisions (task169, task172,
  task170, task167, task460, task129, task230, task162, task130, task102) for the author's adjudicated read if wanted.
  `guard.py heart` WARN only. Pair ceiling 28.5 by `generator/cracker.py`.
- **Data-native sentence.** In-state toll-by-mail invoices are collected when the plate next renews its two-year
  registration, and the booths have been closing at night for only twenty months, so the overnight book's
  collected share is censored by each plate's own expiry date, not by the invoice's age.
- **WARN answers.** `people.first` Zachary appears once in an older build (task141), a different surname and world.
  `overuse.org_family` government_agency is honest for a public authority. `repeat.gate_g`, `overuse.gate_g` and
  `repeat.decision` follow from a forecast quantity in the Forecasting lane. `repeat.deliverables` (one workbook) is the
  product a revenue certificate's back-up is. The older same-puzzle and same-driver signatures are differentiated on the
  card line by line (task102, task130, task134, task162, task178, task501, and this slot's architecture 3).

## Default path

The strong analyst's route, every field read and every filed rule applied (the field's textbook for a toll-by-mail
leakage estimate: the collected share of the existing toll-by-mail book, read on invoices old enough to have run their
collection cycle, applied to the billed toll):

1. Reads programme note PN-14 for the 2027 toll billed by mail to today's cash-lane users, $11,908,500 on in-state
   plates and $4,292,700 out-of-state, after image review, and the basis (toll only, collected however long the hold
   or the agency takes).
2. Takes the TOLL-BY-MAIL invoices (the overnight booth-lane crossings) from the invoices file and their payments
   posted to 31 October 2026 from the payments file, nets returned payments and applies each payment toll first
   (policy 3.3).
3. Matures the book by age: an invoice is done once the reminder, the hold or agency referral and the agency's
   270 days have run, a year after issue, so it reads the collected share of the invoices issued a year or more
   before 31 October 2026: 80.1 per cent in-state, 60.0 per cent out-of-state.
4. Applies the shares to the billed toll: $12,116,763.

**Ends on:** $12.00 million (in-state 80 per cent, out-of-state 60 per cent).
**Golden:** $13.75 million (in-state 94 per cent, out-of-state 60 per cent; $13,743,858 unrounded).

## Stump sentence

A competent solver matures the overnight toll-by-mail invoices by their age, reads the collected share of those
issued a year or more before 31 October 2026 (80 per cent in-state, 60 per cent out-of-state), applies it to the
plan's 2027 billed toll and files $12.00 million; the step that lands it there is maturing in-state invoices by age
when an invoice unpaid at 60 days is collected only at its plate's next two-year registration renewal, so in a
twenty-month record most held invoices are still waiting on a renewal, and read on the held invoices whose
registration on file has since expired the in-state share is 94 per cent and the call $13.75 million.

## Three rules

- Task type: forecasting-forecast-evaluation (Economics & Econometrics; serves Forecasting & Predictive Modeling).
- Domain test: the deciding quantity is the ultimate collection rate of video-billed tolls for the vehicles that pay cash today, the revenue leakage a traffic-and-revenue forecast carries into an all-electronic conversion year, estimated on the toll-by-mail book of the cash lanes' own users and matured on the enforcement cycle that collects it (the registration hold paid at each plate's two-year renewal, the agency's 270 days); remove the maturity construction and the forecast is the book's young collected share, so the call moves by $1.75 million.
- Swap: put a hospital's self-pay bills or a utility's arrears in place of the turnpike's invoices and there is no registration renewal clock that collects a held balance and no booth closure that billed the cash lanes' users by mail, so the construction has nothing to run on and the task does not read the same.
- Layer 1: the back office's export writes one line per billed crossing and one invoice per plate and month, issued on the eighth or the next weekday, carries returned payments as negative REVERSAL rows and postings after the records date to the export run, the Division writes the registration on file as MM/YYYY, the toll schedule changed on 1 January 2026, an express-lane vehicle passing between the two lanes is read twice, and the lane classifier sometimes counts a truck's trailer as a second vehicle; each is what the systems write, and none moves the call (`checks.py` R2).
- Layer 2: estimation_fit, own pattern: the ultimate collected share of a young billed book is censored by a clock each payer carries (the plate's next registration expiry after the hold), so it is read on the payers whose clock has run, not on the bills old enough by their own age.
- Decisive step: for the in-state toll unpaid at 60 days, read the collected share on the held invoices whose registration on file (reg_expires) had expired by 31 October 2026, combine it with the share paid inside 60 days and the agency's share on invoices with no Division record, and carry the in-state and out-of-state shares to the plan's billed toll.
- Not semantics: every field, code, date and status read correctly, including the policy's hold and renewal sentences, still leaves the analyst choosing when a toll-by-mail invoice has finished collecting, and maturing it by its own age (the reminder, the referral and the agency's 270 days, a year) files $12.00 million; no field states an invoice's outcome is final.
- Not rule application: executing the policy's sentences (invoice cycle, late fee, hold at 60 days, renewal window, agency at 90 days and its 270 days, toll-first application) and the plan's basis gives the bills and their payments but not the share a young book will finally collect; that is an estimate from the record, and the standard route (a year-old cohort) is a valid-looking estimate that lands a wrong figure.
- Analyst test: a strong analyst who cleans the book and reads every rule correctly, then matures the overnight invoices by age and reads the share of those a year old, files $12.00 million against the golden's $13.75 million; read on invoices 15 months old, $12.50 million; on every invoice as it stands, $10.50 million.
- Estimand: PN-14 files the population (the toll billed by mail in 2027 to the vehicles that pay cash at the booths today, $11,908,500 in-state and $4,292,700 out-of-state, after image review), the outcome (the toll collected on those invoices however long the hold or the agency takes), the unit (toll dollars; fees left out) and the window (calendar 2027 crossings); the prompt sets the rounding.
- No decoy: nothing is planted; no memo, draft, briefing or stakeholder figure carries a collection rate, a leakage share or a forecast; the held invoices waiting on renewals are what a two-year registration and a 60-day hold produce and are never stated as such.
- No certified replay: no published or certified figure is reproduced to recover a method; no shipped file prints a collected share, a leakage rate or a forecast, and the image review and traffic files answer other questions.
- Lesson: a young book's collected share is censored by whatever clock collects it, and here the clock is each payer's own renewal date, not the bill's age; read the share where that clock has run. No build on file matures a billed book on a renewal each payer carries.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 no leakage, the billed toll collected in full ($16.25 million) | no | no | yes | no | no | yes | readable |
| 1 every toll-by-mail invoice's collected share as it stands ($10.50 million) | no | no | yes | no | no | yes | readable |
| 2 invoices matured by age, 180 days ($11.50 million), a year ($12.00 million), 15 months ($12.50 million) | no | no | yes | no | no | yes | readable |
| 3 the renewal construction run on the toll-by-mail and violation invoices pooled ($13.00 million) | no | no | no | no | no | no | readable |
| 4 (decisive) in-state held invoices read where the plate's registration on file has expired, the cash lanes' own invoices ($13.75 million) | no: no sentence says when an invoice's collection is complete or that held invoices are still waiting | no: the hold returns carry every invoice's expiry alike, no final flag | no: the reflex is a cohort old enough by age | no: no shipped figure ties only under the golden | no: no repair of a defect reaches it | no: the share is a decomposition read on a subset set by another file's dates | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | toll billed by mail in 2027 to today's cash-lane users | PN-14's $11,908,500 and $4,292,700 | rebuilt from the traffic counts | not built from the pack | PN-14 states the figures and their basis |
| SF2 | collected | toll collected however long the hold or agency takes | collected within 2027 | a different quantity | PN-14: "however long the registration hold or the agency takes" |
| SF3 | toll, not fees | toll only, payments applied toll first | fees counted | none (fees excluded) | PN-14 and policy 3.3 |
| SF4 | in-state | plate_state HM | plates of nearby states | same call (HM only) | the dictionary: HM is this state |
| SF5 | records date | payments posted to 31 October 2026 | to the export run | same call (asserted) | the invoices' status date and PN-14 |
| SF6 | returned payments | netted | gross | same call (asserted) | the dictionary's REVERSAL rows |
| SF7 | an expired registration on file | reg_expires month end on or before 31 October 2026 | strictly before | same call (asserted) | records converge (SF7 asserted) |
| SF8 | agency-matured invoices | issued a year or more before 31 October 2026 (placement at 90 days, return at 270) | 400 days | same call (asserted) | policy 4.3 |
| SF9 | the cash lanes' users' book | TOLL-BY-MAIL invoices | every billed-by-mail invoice | $13.00 million | PN-14: the vehicles that pay cash at the booths today; policy 2.2 |
| SF10 | rounding | nearest $0.25 million, shares to whole per cent | finer | n/a | the prompt |

## Ladder

| Rung | Route | In-state | Out-of-state | Collected | Printed | Dies to |
|---|---|---|---|---|---|---|
| 0 | no leakage | 100.0 | 100.0 | $16,201,200 | $16.25 million | the book collects far less than it bills |
| 1 | every invoice as it stands | 69.9 | 51.5 | $10,530,742 | $10.50 million | young invoices are still collecting |
| 2a | invoices 180 days old | 76.0 | 56.9 | $11,495,557 | $11.50 million | the agency's 270 days and the renewals still to come |
| 2b | invoices a year old (default path) | 80.1 | 60.0 | $12,116,763 | $12.00 million | in-state invoices wait on a renewal up to two years after the hold |
| 2c | invoices 15 months old | 82.4 | 61.2 | $12,436,584 | $12.50 million | the same; most renewals have not come |
| 3 | renewal construction, violations pooled in | 88.0 | 56.6 | $12,912,749 | $13.00 million | the violators are not today's cash-lane users |
| 4 | renewal construction on the cash lanes' own invoices (golden) | 93.8 | 60.0 | $13,743,858 | $13.75 million | |

Margins: the golden family (registration on file expired on or before, or strictly before, the records date; the
agency read on invoices issued 365 to 400 days before; returned payments netted or not; payments to the records date
or the export run) sits in one printed cell, the call $13,743,395 to $13,761,443 against the $13.625 to $13.875
million cell, in-state 93.78 to 93.90 and out-of-state 60.00 to 60.31; every rival misses by at least three cells.
The in-state share's parts: 61.0 per cent of the toll paid within 60 days; of the unpaid toll, 96.8 per cent put on a
hold and 86.1 per cent of the held toll collected where the registration on file has expired (7,214 invoices); the
agency's share on the 279 invoices with no Division record, 23.0 per cent.

## Closure table

| Axis | Name | Reading | Closure |
|---|---|---|---|
| 1 | Population | the 2027 toll billed by mail to today's cash-lane users | filed in PN-14 with its two figures |
| 2 | Unit of account | toll dollars | PN-14; fees left out |
| 3 | Attribution window | calendar 2027 crossings, collected however long it takes | filed |
| 4 | As-of dating | payments posted to 31 October 2026; invoice status at that date | SF5 asserted |
| 5 | Version basis | the 2026 rates, unchanged for 2027 | the schedule |
| 6 | Denominator | toll billed on the invoices read | C1 |
| 7 | Weighting | toll-weighted shares | the call is toll dollars |
| 8 | Window length | invoices issued April 2025 to October 2026 | the record |
| 9 | Boundary inclusivity | expiry on or before the records date | SF7 asserted |
| 10 | Rounding path | shares and toll unrounded, round once | the prompt |
| 11 | Tie-break | none needed | C1 |
| 12 | Maturity and censoring | in-state held invoices matured on the registration on file; agency invoices at a year | the decisive step; family converges |
| 13 | Order of operations | payments to toll first, then shares, then the plan's toll | policy 3.3 |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | express-lane double reads occur only on violation lines | SEP asserted |
| 16 | Identity normalisation | invoice number joins every file | dictionary |
| 17 | Netting against gross | returned payments netted | SF6 asserted |
| 18 | Dimensional units | dollars | dictionary |
| 19 | Code and status semantics | TOLL-BY-MAIL and VIOLATION; HOLD PLACED and NO RECORD | dictionary and policy 4.1, 4.3 |
| 20 | Integerisation | none before rounding | C1 |
| 21 | Clause scope | PN-14's first figure is the call, the second the Enforcement tables | PN-14's paragraphs |
| 22 | Forward window contents | every crossing without a MarrowPass billed by mail from 4 January 2027, on today's cycle | policy 2.3 and PN-14 |

## Literal reader

Executed word for word, PN-14's basis and figures and the policy's sentences fix every input of the golden's quantity
(the billed toll by plate state, toll only, collected however long it takes), and every literal reading of them (SF1 to
SF10) lands the same call or is ruled out by a quoted sentence; the easy answer comes from the easy method (a
year-old cohort) on the same literal estimand, never from another reading.

## Oracles

None tie only under the golden. The invoices' status column is the back office's own as at 31 October and agrees with
the payments under every reading; the image review summary and the plaza traffic counts are the systems' own totals
and no graded figure reads them; no shipped figure prints a collected share, a leakage rate or a forecast.

## Ask sheet

**Main call's declared row population:** the TOLL-BY-MAIL invoices issued April 2025 to October 2026, their lines (booth
lanes, 11 p.m. to 5 a.m.), their payments posted to 31 October 2026, their Division hold returns and agency placements
(Corrigan Mott Recovery), and PN-14's two billed-toll figures. Device and hazard rows in it: 0 (`checks.py` SEP: no
express-lane line on a toll-by-mail invoice, so no double read or classifier split; every toll-by-mail agency
remittance names its own invoice and covers only it; the call never reads the commercial postings).

**Ask A. For each month January to September 2026, the violation crossings and the toll they owe** (18 figures,
crossings whole, toll to the cent). H18 home: the violation part of the certificate's toll-by-mail line, which
Enforcement forecasts from it, beside the programme's figure. Path: the invoice lines, the commercial MarrowPass
postings, the lane table, the policy (four files, eight columns).
- A1 (classifier splits; silent primary): a five- or six-axle truck with a MarrowPass sometimes passes the express-lane
  classifier as a three-axle tractor posted to its account and a second, tagless vehicle a tenth to three tenths of a
  second behind it in the same lane, read on the trailer's (or a towed car's) own plate and billed as a violation. It
  is not a violation (policy 2.1: the vehicle had a valid MarrowPass), and only the commercial postings place it:
  2,611 lines over the nine months, every month moves (by 254 to 319 crossings and $553.70 to $707.20).
- A2 (straddles; seen, repaired right): an express-lane vehicle passing between E1 and E2 is read in both, a fraction of
  a second apart on one plate, 2,961 lines; the battery counts it once.
- Stops (asserted): every line (all 18 miss), straddles dropped (all 18 miss), a window of 2.5 seconds behind a posting
  that also drops the violators following trucks a second or two behind (all 18 miss).

**Ask B. For the out-of-state violation invoices issued in each quarter April 2025 to March 2026, the share of the toll
owed collected by 31 October 2026** (4 figures, whole per cent). H18 home: the collection record of the violation
book that becomes toll-by-mail at the cutover, the certificate's companion figure. Path: the invoices, the payments,
the agency placements, the lines and the postings (five files, ten columns).
- B1 (whole-account remittances; silent primary): Benbow Associates works a plate's whole violation account, so one
  remittance names the oldest invoice it holds for the plate and covers every invoice it closed as collected that
  day; the payment joins its invoice, exceeds that invoice's balance, and the other invoices show no payment. Applied
  oldest first (policy 3.3) the quarters read 44, 48, 41 and 40 per cent; applied to the named invoice only, 42, 42, 34
  and 34 (283 of the 812 violation remittances cover more than the invoice they name).
- B2 (classifier splits; shared hazard): the phantom violations of 2026 owe nothing; left in, the January to March 2026
  quarter moves.
- Stops (asserted): every payment on the invoice it names (all 4 miss); the phantoms left in owed (the 2026 quarter).

**Hazard table.**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| H1 classifier splits | the express-lane classifier on tractor-trailers and tows | A, B | A every cell; B the 2026 quarter |
| H2 straddles | lane change through the express lanes | A | every cell, before the battery |
| H3 whole-account remittances | the violation agency's contract | B | every quarter, 3 to 6 points |
| H4 returned payments, postings to the export run | the back office | call (neutral), B | under 0.1 point |

**Referee.** A1: a tagless read in the same lane a tenth to three tenths of a second behind a commercial posting (two
vehicles cannot pass one lane that close; ordinary followers are 0.9 seconds and more behind); B1: a remittance above
its invoice's balance and the agency file's other invoices for the plate collected that day. Each is countable from
shipped rows.

**Cracker sheet** (`generator/cracker.py` on the cut pack: the call landed, returned payments netted, straddles
counted once, each payment applied to the invoice it names toll first, payments to 31 October)

| Ask row | Figures | Cracker's path | Device that holds | Verdict |
|---|---|---|---|---|
| Ask A, violation crossings and toll owed by month | 18 | straddles counted once, every other line kept | A1 | miss |
| Ask B, out-of-state violation collections by quarter | 4 | each payment on the invoice it names | B1 | miss |

Measured by: `generator/cracker.py` (Part 0's weights: the call and its components 38, the instructions 7, the asks
55 over the 22 ask figures; a response off the call keeps 5).

Mirror leakage: 0.0 per cent of ask weight (the mirror keeps none of the 22).

Pair ceiling: 28.5 measured on the cut pack (the cracker 45.0, the mirror 12.0). The honest risk: A1 falls to a
reader who pairs every violation read with the commercial postings by lane and time, which lifts the cracker by 45
points of ask weight on 18 figures; B1 falls to one who checks each remittance against its invoice's balance.

## Earlier screens (architectures 1 to 3, kept as history)

**Architecture 3 (2026-10-23, spent at Gate F on ce04ed65).** Sablewood Electric Cooperative's optional overnight
rate R-ON for 2027, its members and shortfall priced on each R-1 member's own bill saving through the first-year
take-up of the March 2024 evening-peak rate R-TOU, read on the use of the year before that rate was offered because
its takers moved use out of 4 to 9 p.m. after joining (golden 2,250 services and $200,000 against the default path's
1,000 and $100,000). Stage 3 was green (checks 76 of 76, verify, byte-identical rebuilds, figures_check 41 of 41,
precut 51 checks, voice-check PASS) and scored reader B landed the call and all 20 ask figures, calibrating the launch
cohort on its pre-launch use by default; its card moved into `lineage` with that fate and its generator was replaced
by architecture 4's. The death line is in `## Tried and rejected`.


**The 2026-10-19 status: PAUSED at stage 1, no card registered, nothing cut.** The receiving-desk architecture was
re-rooted on the coordinator's call, and the re-draw screened the actuarial mortality-longevity cell on code
(three designs, prototypes a1 to a7 and b1) and the human-reliability cell on code (h1, h2). A second screen
took the coordinator's two candidates on code (screenA: event prediction in an outcomes trial, then fatigue
under a longer-shift roster), and neither held on measurement. A third and final screen (screenC) took the
coordinator's read-across candidates on code, F (a first annual renewal in a second market, measured in full
in an earlier market) and G (a new meter batch's failures, read from an older batch of the same design), with
the four stumping 1.2 screens of eda6c8c run first, and neither held. A fourth screen, the author's redraw in a
new world, took the political-science-public-policy cell (election-polling-forecasting) on code under the
round's bans (scratch r171/proto: seats_sim.py, tactical_sim.py), with stumping 1.3's library test applied, and
nothing held; a fifth took the scaling-laws cell the same way, and nothing held there either. No architecture
is live. This note holds the screen record only; it carries none of the `precut.py` sections, because no
design exists.

**The election cell, in one sentence.** The quantities with enough rows to price at the bar (seats from
constituency results, turnout from registers, ballots from tracking files) have textbook routes a back-test
settles, and the judgments beyond them are composition-type (who is in the electorate, which ballots remain,
which seats declared first, out this round), or carry levers under 20 per cent because the last result already
embeds the structure, or rest on an election-level behaviour estimated from a handful of past elections;
poll-based shares and margins fail on arithmetic before any of that.

**The scaling-laws cell, in one sentence.** A fifth screen took general-statistics-data-science (scaling-laws, the
subdomain never drawn) on code (scratch r171/proto: cbs_sim.py, dir_sim.py), with the client's three cards as the
default path: every judgment beyond the cards puts runs on a common exposure (batch-efficient tokens, the value of a
repeated token, a completed-schedule equivalent), so where some runs attain the plan's condition the effect is a filter
and a divide on them, and where none does its dependence is extrapolated by forms the runs cannot tell apart, while the
graded figures that can carry a 30 per cent lever (token and compute budgets) carry inversion noise of 10 to 50 per cent.

**The structural sentence, and the first thing to read.** A near-term mortality quantity of a population the
record observes every year is reproduced by carrying the last period's amount-weighted rate onto the current
roll, because next year's population is this year's population one year older; every analytical correction
the field owns (the amounts gradient, credibility, improvement, banding, a covariate model) corrects a
quantity the persistence route already measures in the right units, so the decisive step has to act on a
period the record never contained (the client's "a known schedule change makes the next period genuinely
differ"), and in mortality the scheduled changes are premium steps, which live on thin life-insurance deaths,
and benefit changes, which only move weights the persistence route can re-weight. The second screen met the
same wall from the other side: where the coming window differs from the record only in cells the record has
not yet filled (durations the late, lower-risk entrants have not reached; hours on duty most of a workforce
has never worked), either the field's standard forms disagree in those cells by more than any rival misses
by, or a straight line carried through the filled cells lands, so a draw here needs a coming-window
difference that the record measures in full somewhere else in itself. The third screen built exactly that and
found the read-across is the common-exposure subset screen's completion branch: no unit of the target has
reached the exposure, so the step aligns its units with a population that has, at a common point (the same
month of the term, the same age), and that alignment is itself a filter and a divide on the attaining
population, while every partial alignment (an earlier common point, a ratio of a related rate, a band at the
wrong point, a haircut) lands inside the bin the full alignment's own family needs, because the family spreads
as the target moves away from the attaining population, so the gap that moves the rivals out widens the bin
with them.

## Tried and rejected

- **Architecture 1, a regional grocery network's receiving desks (supply chain, never registered).** The 90th-percentile tractor count a DC closure needs was meant to turn on queueing at the receiving desks, but a flat 20 to 30 minute dwell uplift reproduces the queue's effect on that statistic within a tractor, and in the overload regime the stump needs the standard congestion constructions disagree (the M/D/1 desk is undefined there, the fluid queue runs 3 tractors under the discrete-event replay, the empirical wait curve 9 under, the hourly M/D/1 23 over or 3 under), so neither strength nor determinism held (prototypes p1 to p27, p27 the coordinator's four-construction and flat-uplift test).
- **Levers rejected inside architecture 1.** Drive-time calibration (another scalar correction a flat uplift absorbs); reverse congestion at a slow Northgate desk (about one response in three lands it); roster-capped demand rebuilt from release times (task168's driver, and the release times would have to be named in the estimand); dispatch re-timing (it works only with a filed or withheld dispatch rule).
- **A miners' pension trust's 2027 pension release, where larger pensions die sooner (actuarial mortality-longevity, prototypes a2 to a7).** A flat dollar rate per year of credited service makes the pension track years underground, so the amount-weighted experience ratio runs 11.6 to 13.0 per cent above the head-count ratio and every textbook factor (amounts lighter than lives) points the wrong way; on a cohort-built fund (miners only, 2023 to 2026 experience) the head-count route misses by 10.4 to 11.5 per cent, the head-count ratio times 0.95 by 14.9 to 15.9, times 0.90 by 19.4 to 20.3, the table at face value by 26.7 to 28.7, and the head-count route fails the 2026 hold-out by 3.3 to 5.6 standard deviations. It died because the release is observed every year: last year's release rate on the December roll lands 3.1 to 5.8 per cent from the golden even in a closed, ageing fund (the four-year crude rate 6.5), inside any bin that holds the twelve golden-family estimators (range 1.2 per cent) and one sigma (1.0 per cent), so the plainest rule of thumb lands, and a solver who weights by amounts lands too (the step is a coin flip).
- **The same trust's liability for the miners' pensions.** No persistence route exists, but on the same fund at 6 per cent the head-count multiplier moves the present value only 4.1 per cent against the generator's member-level model while a single amount-weighted multiplier lands 1.0 per cent under it (the service GLM 0.2 under, the table at face value 13.0 over), so no bin separates the rival while holding the estimators, and the decisive step reduces to the weighting a literate solver takes by reflex.
- **A term insurer's ten-year level-premium step (series A through its step in 2022 to 2024, series B stepping in 2027, healthy lives leaving at the step; prototype b1).** It died on determinism: series A's 27,332 persisters carry 117 deaths in their first post-step year and series B's forecast year 32, so face-weighted rates by jump band carry 10 to 20 per cent sampling error, and the band-matched golden route moved minus 13 and plus 33 per cent against the simulated claims across two seeds. A step at an anniversary is also task107's driver.
- **Screeners' threat-image detection under a summer roster with 30-minute X-ray stints and a large new-hire cohort (human-reliability-assessment, prototypes h1 and h2).** Persistence, tenure-only and minutes-only routes sit 1.5 to 4.3 points above a golden family that spreads 0.34 to 0.38 points within a seed, but the learning curve's form alone (exponential against logarithmic in experience) moves the figure 0.34 to 0.38 points, so whole-percent grading has no quarter-bin margin; both moves are visible attributes (stint length on the roster, tenure from the hire date), which is the reflex death task202 recorded for time on task and task182 for experience composition. The stronger variant, vigilance restored only by a break and not by a rotation, repeats task132's reset clock.
- **Paper screens, not coded.** A pandemic-contaminated window (the fund's level against contemporaneous population mortality): excluding 2020 and 2021 is the field's reflex and lands within 2 per cent, and the as-of would sit in early 2023, where a solver's own knowledge of 2023 mortality is an outside fork. Experience-rated employer groups chosen for the worst ratio: credibility toward the manual rate is the field's reflex and lands. Election polling: every vote-share family (house effects, likely-voter turnout, undecided allocation) spreads wider than the margin any rival misses by. Population pharmacokinetics: the decisive structures (renal covariate, accumulation to steady state, Michaelis-Menten elimination, unbound fraction) are filed formulas (rule application) or tail counts whose method families spread.
- **Event prediction in a blinded event-driven outcomes trial whose protocol amendment opened enrolment to lower-risk patients (biomedical-clinical-research, survival-time-to-event-analysis, the forecasting task type, since clinical-trial-design-analysis serves only experiment-causal; prototypes in screenA).** The count of first adjudicated primary events over the next 3 to 12 months, forecast from blinded pooled data, was to turn on the hazard by time since randomisation within entry cohort, because a hazard pooled over every entrant lends the late, lower-risk entrants the early entrants' hazard at the durations they are about to reach. It died on measurement in every layout tried. On a frailty-and-mixture truth (12,000 patients, Weibull shape 0.6, gamma frailty 0.5, the post-amendment cohort at about 0.6 of the earlier risk, 9 and 12 months ahead) the standard cohort-aware forms spread from 13 to 25 per cent under to 4 to 10 per cent over their median (log-normal 11 to 13 under, Cox 5 to 11 under, the stratified piecewise model 13 to 25 under, the Weibull 3 to 7 over), sigma 9 to 16 events on medians of 185 to 263, while the pooled Weibull sits only 15 to 18 per cent over the median and the pooled log-logistic 13 to 15. On a clean proportional-hazards Weibull truth (6,500 to 11,000 patients, cohort hazard ratio 0.4 to 0.5, 12 months ahead) the family spread 58 to 157 events on medians of 289 to 572 with a patient-bootstrap sigma of 16 to 22, so a bin holding it needs 197 to 396 events, against a nearest rival (the pooled log-logistic, or the last three months' events per patient-month) 25 to 85 off. On the most favourable layouts (a small early cohort with a long low-risk enrolment, or a late amendment, 3 to 12 months ahead) the three core forms alone (Weibull, Cox with its baseline carried on, piecewise exponential, each with the cohort term) spread 20 to 45 events on about 230 at nine months, sigma 3 to 15, bins needed 45 to 204, nearest rival 9 to 62 off, and even with no family spread the pooled log-logistic sits under four sigma of the golden in two of three seeds. The dial: the cohort effect bites only at durations the late entrants have not reached, so the golden itself carries a hazard into unobserved cells (proportional hazards borrowed from the early cohort, or the late cohort's own shape extrapolated), and that carry is what spreads the family; shortening the horizon to stay inside observed durations hands the call to the last months' events per patient-month, 12 to 30 per cent over at 9 to 12 months and 9 to 12 events off on about 100 at 3 months. The amendment notice the pack would carry also makes the decisive rung readable, and the duration piece without the cohort is task134 v2 round 1's driver (guard 0.18, the nearest).
- **Dispensing errors in a hospital pharmacy moving from 8-hour to 12-hour shifts, with hours 9 to 12 worked only on overtime extensions taken by staff whose own error rate is low (human-factors-ergonomics; the forecast would sit in human-reliability-assessment, since workload-fatigue-shift-analysis serves only root-cause; prototype simB).** On 70 staff over two years (about 32,000 shifts, 7,500 to 8,000 errors, volunteers selected two standard deviations on the logit of the person effect) the right family (person fixed effects with hourly or grouped duty-hour categories, a two-slope spline, with or without time of day) agrees within 1.0 per cent and a within-person shift bootstrap puts sigma at 2.2 to 2.3 per cent, so a bin holding it needs about 11 per cent of the forecast (440 to 470 errors); the pooled duty-hour model misses by 15 to 19 per cent and the flat rate per item by 13 to 15, but the gradient over hours 1 to 8 carried in a straight line to hour 12 lands 0.4 to 9.2 per cent from the golden (0.8 to 9.3 pooled), and the published 27.5 per cent excess for 12-hour shifts 8 to 11 per cent over, both inside the bin. The decisive step itself (the gradient read within each person rather than across people, applied to a forward plan that lengthens every shift) is task149's driver by the abstraction test (guard 0.15, the nearest), in the human-reliability cell where this slot's screener design already died.
- **A first annual renewal in a second market, read across from a first market whose annual cohorts have renewed in full (product-analytics, retention-cohort-lifetime-value-modeling; prototypes simF, runF, sweepF and screensF in screenC).** Market B's annual terms, six to eleven months run at the as-of, renew inside the window; market A's 29,900 complete first terms carry the only renewals on file; the golden reads each open B term from the state it has reached (auto-renew status, engagement) through A's renewals at the same month of the term. The eda6c8c screens, as code: dispersion and truncation do not apply (a level, no suppressing threshold); variance-only passes (the step moves the point estimate, lever over noise 9 to 45); the common-exposure subset screen fires, because no B term attains month 12 (0 of about 10,600), so the escape is completion from an attaining population that differs from B (B's engagement 0.34 to 0.50 sd lower at the same month), and the golden is itself a filter and a divide on A (banded same-month rates within 1.4 to 2.1 per cent of the logistic) while the attaining population's plain filter and divide (A's raw rate) misses by 16 to 28 per cent. Separation fails as well: across 36 runs (market gaps of 0.25 to 0.8 sd of habit, three persistence settings, three seeds) the family (two logistics, banded rates, a forest, a tree, engagement only, every month observed, a second-order chain) spreads 1.0 to 6.0 per cent with sigma 0.74 to 1.27, so the bin needs 5.3 to 16.1 per cent, and 6 to 11 routes land inside it in every run: A's renewal by month-1 engagement band in all 36 (0.25 to 0.92 bins), the end-of-term engagement band scored on present engagement (0.18 to 1.02), trial-day bands (0.40 to 1.17), the memoryless chain (0.46 to 1.10), the engagement-ratio and monthly-plan-ratio adjustments at the smaller gaps, a 10 to 30 per cent haircut and a textbook 30 to 35 per cent renewal rate at every gap. The bin widens with the gap because the family spreads as B moves away from A (a single dial), and the A-trained family itself runs up to 6 per cent above the truth on B's prior shift. guard.py slots found no earlier screen of the mechanism.
- **A new smart-meter batch's failures in its third year, read from an older batch of the same design observed to age ten (energy-systems-utilities, asset-condition-maintenance; prototypes simG, simG2 and sweepG in screenC; task164's peak-coincidence driver untouched).** 600,000 new meters at ages 2.0 to 2.5 and 900,000 old ones at 8 to 10, about 9,800 new-batch failures, a bathtub hazard (early-life decay, a constant, a wear-out onset); the golden is the old batch's age-specific rate at the window's ages scaled by the new batch's level against the old at the ages both have reached. The common-exposure subset screen fires: no new meter attains ages 2.5 to 3.5, the attaining old batch's own filter and divide misses by -23 to -27 per cent, and the golden is two filters and a divide (the new-to-old ratio over ages 1 to 2.5 times the old forward rate lands -0.2 to +3.2 per cent from it), the batch comparison at common ages any reliability analyst makes first. Under a proportional-hazards truth (five seeds) the family spreads 1.2 to 8.6 per cent with sigma 2.6 per cent, so the bin needs 13 to 27 per cent, and the accelerated-time form (+18 to +22), the new batch's cumulative rate carried (-13 to -17) and its last six months' rate (-15 to -23) sit inside it in most seeds, the new batch's 2026 rate (-20 to -26) and the old batch raw at about one bin. And the form that carries the batch difference into the ages the new batch has not reached decides the figure: under an accelerated-time truth, or a difference in the early-life mode only, the proportional-hazards family runs 16 to 27 per cent off the truth, told apart only by a likelihood ratio on the early ages (+17 to +63 units under the proportional truth, -29 to -55 under the accelerated one), which is the structural sentence's first horn again. A Weibull fitted to the old batch, the field's first form, runs +67 to +74 per cent.
- **Election polling, the swing scale (the redraw's lead; political-science-public-policy, election-polling-forecasting; seats_sim.py).** A seat projection under a filed national scenario (600 seats, six past elections, a third party C rising 15 to 20 per cent, the governing party falling 36 to 33) was to turn on the scale of the change across seats, uniform swing being the default. It died on stumping 1.3's library test, measured: under a logit truth the back-test of uniform, proportional and logit swing on the five past pairs picked logit in 4 of 4 seeds and landed within 0 to 5 seats of the truth's 64 to 72 C seats, proportional swing alone within 0 to 3, while uniform swing missed by 17 to 22 seats; under a uniform truth the back-test picked uniform in 3 of 3. The scale is a debate between textbook routes that a careful reader back-tests both sides of.
- **Election polling, a realignment that keeps moving (seats_sim.py, truth realign).** Each seat's lean drifting along a factor recovered from the history of seat-level changes (step 0.10 to 0.50 logits per election, transient noise 0.10 to 0.18) was meant to be the judgment beyond the swing scale. It died on lever: the logit swing the back-test picks lands within 0 to 6 seats of the truth's 83 to 101 C seats at every setting, because the last result already carries five steps of the realignment and one more adds under 6 per cent; the per-seat trend, factor, pooled AR and last-plus-mean-change routes all land inside the same few seats.
- **Election polling, tactical switching when a seat's configuration changes (tactical_sim.py).** The third party's voters moving to the close challenger where the governing party leads (rate 0.25 to 0.60, window 12 to 20 points), so seats entering that configuration gain beyond the swing. Truth 58 to 79 C seats; uniform swing 32 to 48 per cent under, but the logit swing the back-test picks only 5 to 13 seats (9 to 17 per cent) under, a swing stratified by the last result's winner and runner-up no closer, and the true model's own hard count up to 8 seats from its expected count, so the estimand's hard-or-expected choice forks by as much as the lever and the tactical form (window, decay, who switches) is a free specification.
- **Election polling, paper screens across the cell.** Poll-based vote shares and margins fail on arithmetic (a share cannot move 30 per cent; a margin's sampling sigma is about a point on 10,000 to 100,000 respondents). Turnout after a surge election: the comparable-election reflex lands, and with surge registrants it is composition, out this round. Election-day turnout from the remaining pool after early voting: the timing-against-turnout split rests on an assumption the data cannot force. The late count completed stream by stream: a few hundredths of a point on the margin, and task181's driver. Mail-ballot returns by time since each ballot was mailed: the mailing delay is a stated break, the realigned curve is the subset route, and the driver is task134 v2's and this slot's own screenA death. Expected seats of a party near a threshold: card 1's simulation lands. Phantom swing as a hold: a margin's sigma. Notional results on new boundaries from ward local results: a single-purpose file and the textbook allocation. The local-election swing pattern carried into a general election: a fitted regression on the obvious covariate. Ballot cure deadlines (task172), a holiday in the count's development (task162-like, small), a ranking cap in ranked-choice counts (task168-like), signature-sample duplicates and betting longshot bias (the swap test fails), seat quantile calibration (a variance lever on a few cycles).
- **Scaling laws, the critical batch (general-statistics-data-science, scaling-laws; cbs_sim.py).** A planned 1.5B run forced to an 8M-token batch by a new pod, graded on the tokens to first reach a target validation loss, the judgment beyond the three cards being that tokens stop being the exposure once the batch passes the critical batch, which grows as the loss falls (the steps-against-tokens tradeoff, the critical batch read from the batch sweeps). Truth 383B tokens; the golden (critical batch a power law in the loss) -4 to +4 per cent; the cards' pooled fit +27 to +43, the standard-batch grid -19 to -45, a batch covariate +36 to +41, one pooled critical batch +13 to +17. It died on determinism: the critical batch as a power law in the reducible loss fits the sweeps as well (residual sd 0.046 to 0.070 against 0.039 to 0.066) and lands +73 to +99 per cent (+99 to +230 in a fixed-recipe variant with the plan near its own critical batch, where the cards miss by -42 to -53), and as a power law in data size it runs wild; with the target inside the sweeps' losses the batch factor at the target is a filter and a divide on the largest sweep. The single dial is the target's distance below the sweeps.
- **Scaling laws, card 3's holdout direction against an overtrained plan (dir_sim.py).** A 1B model trained to about 250 tokens per parameter, the judgment being that the form is validated along the plan's tokens-per-parameter axis rather than on the largest compute. It died twice: where the forms differ enough to matter (a coupled truth against the additive form, RMSE 3.6 against 39 to 62 thousandths of a nat) every holdout and the in-sample fit pick the right form, so the card lands; and a token budget near the size's own loss limit swings -22 to +96 per cent across seeds under the true form itself.
- **Scaling laws, paper screens.** Repeated data (the value of an epoch at the plan's count is measured by small multi-epoch runs, a filter and a divide, unless its dependence on model size is extrapolated, which spreads); learning-rate drift with scale (the same dilemma); downstream accuracy read through the loss (the external models nearest the predicted loss are the forecast); continued pretraining from a cooled checkpoint (matched continuation pairs measure the penalty); interval calibration by back-test distance (a handful of origins); best-of-attempts selection at the largest scale (a lever of a few thousandths of a nat); compute accounting from configs, rolled-back tokens and eval-set drift (rule application or Layer 1).
- **Rebuild 2026-10-23, the discrete-choice cell, paper screens before any harness.** The client's three cards (willingness to pay as a ratio, IIA against nesting, scale across samples) are the default path, and each judgment drawn beyond them died on paper: congestion feedback when a toll moves trips onto a crossing that slows with its own volume (task253's and task228's fixed point); a randomised savings-plan invitation whose comparison arm is reached through co-workers (task131 architecture 1's household interference read where a group drew one arm); diversion after a product is withdrawn read from each buyer's browse log (the set a buyer would consider once the product is gone is not the viewed set less the product, and with stockout episodes the diversion is a filter and a divide); logit curvature at each unit's own propensity (task165's own-baseline gain); attenuation from skimmed travel times corrected on a GPS sub-study (skims are zone averages, so the error is Berkson and barely attenuates, and the sub-study sees only the chosen mode's time); a nesting dimension no category names (a likelihood back-test picks it, the election cell's death); choice-based sampling (calibrating constants to counts is the reflex); crop rotation after a price spike (the lagged crop is the obvious covariate); travel-time reliability (mean delay proxies its spread across routes and hours); a customer switching away from a plan whose provider fails (task169's two routes, one closed).
- **Rebuild 2026-10-23, departure-time choice under a 2027 peak surcharge (scratch `b171n/proto/dt1.py`).** A bridge's commuters choosing 15-minute slots under a scheduling-model truth (preferred arrival times, early and late penalties, a lateness step), with an early-bird discount and planned roadworks in the record to calibrate on. Over 18 settings the peak window lost 24 to 46 per cent of its share; a multinomial logit with slot constants and its toll and time coefficients calibrated on the early bird and the roadworks overstated the drop by -1 to +40 per cent (median about +20), and the early bird's slot shifts scaled to the surcharge understated it by 28 to 72. It died three ways: the textbook route sits 15 to 25 per cent of the drop off in most settings, under the 30 per cent lever the held builds carried, and straddles zero in one; the golden is a structural scheduling model over a latent preferred-arrival distribution, so its outsider family is a set of specifications (preferred time from habit or fitted, linear or stepped lateness) rather than one construction; and a peak surcharge names peak spreading, so the adjacent-slot step is the question's own reflex.

- **Rebuild 2026-10-23, measured inside architecture 3 before the pack was frozen.** (1) A take-up truth with one decision and a fixed launch-response curve put the textbook discrete-time hazard 10 to 15 per cent under the 12-month logit on the shortfall, so the truth is the monthly logit hazard the field writes, and the 12-month logit, probit and saving bins sit within 4.8 per cent of it on services. (2) With the overnight rate's customer charge above R-1's, the overnight savings sat left of the evening rate's and every form extrapolated in the lower tail; equal customer charges and the overnight rate's top savers kept inside the evening rate's range removed it. (3) A forecast population with part-year services forked on annualising their saving (2,298 services and $206,671 against 2,216 and $201,673); the paper now files the population as the services billed in all twelve test-year months, and annualising the cohort's part-year savings is rejected by 235 log-likelihood units. (4) Ask B by district and month left 3 to 7 of 15 cells unmoved by the first-service keying, so it is graded by district, with the two-service members' homes in town and their farm dwellings out of town. (5) A re-issue of every R-TOU row at one date put every tenure cell at zero under the in-effect row's start, a loud failure; the re-writes now follow account maintenance after the June 2025 upgrade (42 per cent of spells). (6) Districts named Coldwater and Velma were renamed (Brisco Bend, Tamsey) for real places with utilities, and Arden Flats (Sedge Flats) for reading as a person's name.
- **Architecture 3 (optional-rate take-up, Sablewood Electric Cooperative) spent at Gate F on ce04ed65, 2026-10-23.** Scored reader B filed 2,250 services and $200,000 and all 20 ask figures. Its path: "Cohort = R-1 services at launch, billed 12 months pre-launch, open through 2025-02-28; outcome = on R-TOU 12 months after launch. Logistic on annual dollar saving (R-1 minus R-TOU, 2024 rates, pre-launch use) fits best"; for the asks, "consecutive R-TOU rows (1-day gap) merged into spells ... after dropping the EST row of each EST/ACT duplicate" and "CRM times UTC converted to local ... 'Closed - duplicate' rows dropped". A careful reader calibrating take-up on a launch cohort reads the cohort's pre-launch covariates by default, because that is the textbook way to set up a launch cohort, so the decisive step was the default; and every ask device (spell gaps, estimate and actual duplicates, UTC, duplicate-closed rows) was visible hygiene the battery executes.
- **Rebuild 2026-10-23, after architecture 3: a regional hospital emergency department's low-acuity walk-ins deterred by its posted wait, a 2027 fast-track holding that wait at 45 minutes (healthcare-delivery utilization-access-demand-forecasting; scratch `b171n/proto2/ed2.py`, `screen3.py`, `screen4.py`).** A slotted priority-queue ED with a queue-based hourly posted wait, deterrence exp(-beta x posted) on CTAS 4 and 5 walk-ins, unfilled physician shifts as the exogenous shifter. The lever is 15 to 25 per cent of the CTAS 4 and 5 count, and the naive Poisson with hour-of-week effects is biased by the shared demand shocks (beta 0.05 to 0.10 against 0.13 to 0.18). It died on the family: with the truth at beta 0.18 the deterrence-aware estimators split, Poisson with day effects 0.205 to 0.214, day-demeaned log OLS 0.123 to 0.174, the Wald ratio on the shortfall 0.135 to 0.151, 2SLS on logs 0.152 to 0.182, the control function 0.150 to 0.166, forecasts about 6 per cent either side, so no rounding holds the golden; and the decisive insight (patients answer the posted wait) is the one a reader reaches from the feed the plan's own target names.
- **Rebuild 2026-10-23, paper and arithmetic screens beside it.** An index provider's 2027 watch list making every addition anticipated, the event desk's capture read on the rule-mandated additions (quantitative-finance strategy-backtesting-evaluation): a hedged five-day capture carries about 4.5 per cent of noise against a mean near 0.7, so 600 anticipated additions give a standard error of 27 per cent of the figure and 2 per cent would need about 37,000 events; the short-notice variant (off-cycle additions already at a one-day notice) is the very subset the rule change names. Cross-border fuel excise after a unilateral rate rise (time-series-macro): the neighbour's price survey on the textbook path names the mechanism and the one tax holiday in the record sizes it from a single episode. A kindergarten entry cut-off moved from 31 December to 1 September, delayed entry by relative age read from a second board already on 1 September (sociology population projection, spent by task176 besides): relative-age redshirting is common knowledge and the second board's pattern is the analogue a reader takes. A five-year mortgage reset's defaults on its payment shock (credit-scoring-pd): the payment shock is the covariate every reader fits. Bunching at a tax kink moved forward: the counterfactual density is a polynomial knob. Forestalling before a tax rise and a toll bridge's commuters were not taken further (the second is this note's dt1 world).
- **Architecture 4 at design, 2026-10-23: agency settlements as Ask B's device, replaced before the pack was frozen.** A violation account settled at 65 per cent in one payment with no invoice number, its invoices listed in the reference and applied oldest first, toll before fees: the unmatched join the hygiene battery runs surfaces the payment and a policy sentence then hands the allocation over (a filed rule adjudicating the device), so the device became the violation agency's whole-account remittance named on the oldest invoice.
- **Architecture 4 (the Marrowfield Turnpike's toll-by-mail collection, matured on each in-state plate's registration renewal) spent at Gate F on 9451b6bd, 2026-10-23.** Blind reader B landed $13.75 million: "used toll-by-mail (closed booth) invoices, not violation invoices, as the comparison group. Out-of-state: ultimate toll-weighted collection of matured cohorts issued Apr-Oct 2025 (agency window closed) = 0.600. In-state: share paid before DMV referral 0.610, DMV holds 0.378 (converting at 0.862 at renewal, measured on holds whose registration expiry has passed, right-censoring handled) ... In-state ultimate about 0.938." Lessons: a collection channel the policy states (the hold paid at renewal, 4.1 and 4.2) with its clock on file (reg_expires) is measured on sight, the law that killed task177 v3; both ask devices held, 0 of 22 (the classifier-split phantoms found only by same-lane sub-second timing against the commercial postings, and the whole-account agency remittance named on the oldest invoice), so neither sat on the reader's path; and "the in-state and out-of-state shares behind it" forked, read as the collected toll's composition (81 and 19 per cent) rather than the collection rates (94 and 60), so a share in a prompt names its numerator and denominator.
- **Rebuild 2026-10-23, fifth cell (chosen shape first): biomedical-clinical-research / dose-response-pk-pd-modeling, a phase 3's week-12 target-lesion response read lesion by lesion (scratch `b171s/proto/l1.py`, `l1b.py`, `l2.py`).** The structure looked right: the response is a threshold on the size-weighted sum of a patient's target-lesion changes, the lesions share a patient effect and vary within it, and a forward population whose sums are dominated by one large lesion averages less than a record of evenly sized metastases, so the record's patient-level rate does not transfer; the concentration (the effective number of lesions) is built from lesion rows and named nowhere, and the count and baseline-sum reflexes move the wrong way. It died on lever and on sigma, measured: over sixteen settings (median lesion ratio 0.70 to 0.90, within-patient correlation 0.10 to 0.50) the forward rate sits only +1.7 to +18.7 per cent from the record's at correlations of 0.23 to 0.50, the published range for lesion response, and reaches +22 to +29 only at a correlation of 0.10 with median shrinkage of 10 to 16 per cent; on 640 patients at the dose the lesion-level mixed model's own figure moves 0.239 to 0.278 across seeds on a truth of 0.265, about 6 per cent, because a trial's patient count cannot carry a sigma near 1 per cent; and the shared patient effect with members summed is task143's insight one step removed. The cell's other structures are named by the field (dose intensity and reductions, cumulative-dose toxicity, schedule, tolerance, the PK-PD index, hysteresis, exposure confounded by clearance) or sit in population PK, which died for task178 and task179.
- **Fifth cell, the paper half: physical-environmental-sciences / hydrology-flood-frequency, screened beside it (scratch `b171s/proto/h1.py`).** Flood frequency is one weather-driven system per site, so no forward quantity rests on enough events: on a 45-year record the mean annual count of flood-stage days carries a 15 per cent sigma, the 10-year flood about 9 per cent and the 100-year flood about 22 (16th to 84th percentile over 400 records), against the 1 per cent the holds this round had. Every structural break the cell offers is a channel its standard names (regulation and naturalised flows, mixed rain and snowmelt populations, historical floods and perception thresholds, low outliers, urbanisation, non-contributing area, permeable-catchment growth curves, rating extrapolation, compound river and surge flooding), and a hindcast of a forward scheme over the recorded flows is a filed operating rule replayed on the record. A many-unit version (culverts, crossings) reads its catchment property off a map layer, a column.
- **Fifth cell, while choosing, the grey cells on paper (each died in another number's note this round, so not drawn):** a land-retirement programme's 2017 contracts expiring together, read on the share of each owner's holding enrolled (built from a contract file and an ownership file with no shared key), holds the street-grain shape but is `composition_mix`, banned by task179 in the window, and sits in task175's own task type; lease banks rationed per solar developer read through project-company names is builder absorption in another field (task175's world) and fails the swap test; patients with one or more admissions under a therapy that halves each person's rate is a fitted nonlinearity whose lever is its own sensitivity; habit, default, inertia and reference-point choice structures are named in decision-making (task170 v4's ground); media reach, reserving, ratemaking and model diagnostics carry task174's findings.

## Retired

task171 retired on 2026-10-19 under the author's rule for this round (a number that dies in its second new cell retires);
no card was ever registered. The seed's receiving-desk architecture died at the draw, and the redraw round's two cells
died on code: political-science-public-policy / election-polling-forecasting (e27c16f: the swing scale is settled by a
back-test a careful reader runs, and the realignment and tactical layers sit under the bar or fork on hard against
expected seats) and general-statistics-data-science / scaling-laws (96b18ed: every judgment beyond the three client
cards is a common exposure the sweeps either measure, so a filter and a divide lands it, or cannot pin, so the family
spreads past any rival). The lesson: in a field whose standard is a back-tested model choice, the back-test is the
textbook route and it lands.

## Rebuild (2026-10-23)

Reopened under the author's rule that no number stays retired; rebuilt from scratch in economics-econometrics / discrete-choice-limited-dependent-variable-modeling as architecture 3 (`## Draw`), the receiving-desk seed and both redraw cells left spent.

Architecture 3 was spent at Gate F at stage 4 the same day (the scored reader calibrated take-up on the launch cohort's pre-launch use by default); the coordinator left the next cell to this build, the healthcare utilization cell died on code, and architecture 4 was drawn in economics-econometrics / forecasting-forecast-evaluation: the Marrowfield Turnpike Authority's first all-electronic tolling year (`## Draw`). Stage 3 went green the same day and the build is parked at stage 4 for the readers and the judge.

Architecture 4 was spent at Gate F at stage 4 the same day (a blind reader measured the renewal-hold channel the policy states); the number is PAUSED for the main session's next cell.

The fifth rebuild cell was left to this build, shape first: biomedical-clinical-research / dose-response-pk-pd-modeling was taken to code (the lesion-level response, dead on lever and sigma) and physical-environmental-sciences / hydrology-flood-frequency screened beside it (dead on sigma and named channels), with the grey cells read on paper (`## Tried and rejected`, last three lines). No card registered past v4, which stays the card's identity marked spent; PAUSED at stage 1 for the main session's next cell. The number is never retired.

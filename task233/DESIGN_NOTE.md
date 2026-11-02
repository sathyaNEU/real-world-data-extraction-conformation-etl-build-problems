# task233 design note

Architecture 3 (re-rooted 2026-11-01 at the Batch 3 queue reset). Data Quality Monitoring & Alerting, Survey Research
& Official Statistics, nonresponse, calibration and measurement-error adjustment. The school-leaver survey world of
architectures 1 and 2 is closed (their records are at the end of this note). A fictional English-speaking country's
national statistics office (NSO) contracts its consumer price index field collection to Tallis Field Research Ltd. Each
quarter the Head of Prices assesses the contractor's collection in each of fourteen collection regions under the Price
Collection Quality Standard (PCQS v3.0, new from 1 July 2026): compliant, corrective action (accompanied collection next
quarter) or a service credit, on each region's collection accuracy, the share of recorded prices that were the price on
offer when the collector recorded them. The Field Quality Team (FQT) estimates it by re-collecting the prices at a
monthly sample of outlets, on a fixed regional circuit: within a day of collection in the capital, four to six days
after it in the far regions.

## Draw

Card `.claude/skills/fingerprint/cards/task233.json` (architecture v3, registered 2026-11-01T23:41:28Z), guard PASS at
draft and again on the registered card; one NOTE, `test.same_puzzle_older` against task270's v9 lineage, differentiated
on the card (a dispersion read at a chosen lag from ratings at other lags, against an error share at delay zero split
from genuine change). Axes redrawn during the draw because the window moved under parallel builds: shape 07 to 10
(task304 v4 and task475 v2 registered shapes 14 and 07 an hour before), context artifact filed_standard to
close_out_summary (task475 v2 filed_standard), question form what to where (task475's prompt), personas redrawn to
clear two first-name WARNs. The honest labels: the call is a scorecard of one metric against two thresholds per region
(shape 10), and the stakeholder's file beside the standard is the contractor's quarterly close-out return.

- **Pairing.** survey-research-official-statistics / nonresponse-calibration-measurement-error-adjustment (DD, DQ):
  the object is the measurement error in the CPI's field-collected prices, the call each region's monitoring outcome.
  Not retaggable: no real-world event is detected (not AD) and nothing is predicted (not Forecasting).
- **The call.** For each region: Compliant, Corrective action or Service credit; and the quarter's total credit.
- **Shape 10 arithmetic.** 14 outcomes + 1 credit + chart parts (about 5) + 14 timeliness + 14 missed visits + 14
  replacement acceptance + 2 files = about 64 criteria.
- **Strategy and labels.** decomposition_attribution (each disagreement split between the collector's error and a
  genuine price change), Gate G decomposition_attribution, gap objective then time (the agreement metric is correct and
  is not what the standard scores), generators G13 (the check's moment is not the recording's), G3, G16; calibration
  gold_standard_subsample (the back-checks); layer 2 estimand_identification; forum customer_or_counterparty (the
  contractor receives the assessment and the credit), forcing event period_close (the quarterly assessment), org
  research_or_statistics_office, role statistical_office_head.
- **World.** A fictional country of about 5.1 million, its NSO, contractor, regions, outlets and people invented;
  personas from `guard.py names --locale en_NZ --seed 233`: Joanne MacDonald (Head of Prices, signs the letter), Lucia
  Morrison (the contractor's contract manager), Steven Rowe (FQT lead, initials only in the register).
- **Sources.** A fully constructed operating layer: the NSO's price database extract, outlet register, item list, code
  list, collection calendar, back-check register, decisions log, standard and fee schedule; the contractor's visit
  log, schedule, quarterly return and roster; the published regional indices. Every file is declared synthetic in
  `metadata.json`.
- **Data-native sentence.** The FQT drives a fixed circuit, re-collecting in the three Halbrook regions within a day of
  collection and in the far regions four to six days after it, while the price database shows every item class's shelf
  prices moving in 3.5 to 19 per cent of months: the back-check's delay is a property of this team's operating calendar
  that no column states, and it is what turns a correctly recorded price into a disagreement.
- **Abstraction sentence.** Against the nearest approved builds a reviewer would say "a capture share read against an
  independent fixed-protocol index" (task236) and "a validation figure carried to each site through a latent device
  mix" (task281); this build's sentence, "a check made later than the reading measures error plus genuine change, so
  the error share nets each check's own chance of change over its delay", is neither, and no card on file carries it
  (`guard.py slots` on the mechanism and the setting nouns returned no screened ground).
- **Candidates written before choosing** (each dropped one has a line in `## Tried and rejected`): (1) this back-check
  delay; (2) a seismic catalogue's completeness under station outages; (3) a land-cover map's accuracy with the
  reference sample stratified on the previous edition; (4) a survey's response rate with the unresolved addresses'
  eligibility to estimate; (5) blood-pressure digit preference under a device-resolution mix; (6) a retailer's
  inventory record accuracy against counts taken mid-trading; (7) calibration intervals under a renew-if-failed policy.

## Survivor anatomy

- Actor: the deciding property is whether each back-checked item's shelf price changed between the collector's visit and the officer's re-collection, and no file has a column for it: the back-check register holds two prices and a re-collection date, the visit log visit times, the price database monthly prices.
- Link: the signal is read through a comparison no key offers and no sentence invites: each back-check's own delay (its re-collection date against the visit date in the contractor's visit log, crosswalked from NSO outlet code to contractor outlet number through the register) set against its item class's month-on-month frequency of price change in the price database, a different file, grain and system.
- Reflex: the field's QA measure for collection accuracy, the share of back-checked prices that agree with the re-collection, sits at rung 0 and files ten regions wrong (seven compliant regions under corrective action, three corrective regions on credits, a $7,049 credit).
- Back-test: the textbook route validates: in the three Halbrook regions the officers re-collect within a day (mean delay 0.6 to 1.1 days), so agreement and accuracy agree there; each region's agreement is steady across the three months; and nothing in the pack reports an accuracy that could contradict it.
- Second use: every file the decisive step reads has its own job: the visit log carries the timeliness ask, the price database the index and the replacement ask, the register the crosswalk and the outlet types, the back-check register the accuracy measure itself; delete the decisive step and every file stays in the pack.
- Shock: the movement reads as ordinary: the far regions' collectors look about one and a half points less accurate than the capital's, a familiar rural pattern; sorted on agreement, delay, back-check count or region size the flagged set is not an interval (on agreement Wexcombe Plains, compliant, sits between the four lowest and Halbrook North, asserted C13).
- Pins: PCQS v3.0 files the WHAT in the division's own genre (the quarter, every price recorded at the region's outlets, the price on offer at the time the collector recorded it, items not found left out, the bands unrounded, the credit on Schedule 4's fee); no filed sentence names a delay, a re-collection date, a price change, a frequency or a hazard; deleting 3.1's time clause unfixes the estimand, it never hands over the step.

## Default path

1. Read pcqs_price_collection_quality_standard_v3.pdf: accuracy is the share of recorded prices that were the price on
   offer when recorded, estimated from the FQT's back-checks; Compliant at 98.0 or more, Corrective action below 98.0
   and at least 95.5, Service credit below 95.5 with 4 per cent of the region's Schedule 4 fee.
2. Read the three monthly sheets of fqt_backcheck_register_2026q3.xlsx (header block, July dates typed as text,
   September columns reordered) and keep the 6,125 prices the officer found.
3. Take the field's QA measure of collection accuracy, the share of each region's back-checked prices whose collector
   price equals the FQT price: Halbrook Central 98.92, Halbrook North 97.18, Halbrook South 98.78, Eastwick Coast 97.52,
   Belmont Valley 92.84, Wexcombe Plains 97.14, Tamsin Bay 95.09, Greywater 97.37, Ardmore Uplands 97.35, Fenwick 94.90,
   Corran Peninsula 97.32, Westholm 94.95, Rookby Downs 97.49, Northreach 97.23.
4. Apply section 4 and pcsa_schedule4_collection_fees.pdf.

Ends on: corrective action for Halbrook North, Eastwick Coast, Wexcombe Plains, Greywater, Ardmore Uplands, Corran Peninsula, Rookby Downs and Northreach; service credit for Belmont Valley, Tamsin Bay, Fenwick and Westholm; a $7,049 credit.

Golden: corrective action for Halbrook North, Tamsin Bay, Fenwick and Westholm; service credit for Belmont Valley; the other nine compliant; a $1,775 credit.

## Stump sentence

A competent solver takes each region's accuracy as the share of its back-checked prices that agree with the officer's
re-collection and files corrective action for Eastwick Coast, Wexcombe Plains, Greywater, Ardmore Uplands, Corran
Peninsula, Rookby Downs and Northreach and service credits for Tamsin Bay, Fenwick and Westholm, a $7,049 credit; the
step that lands it there is counting every disagreement as a collector's error when the officers re-collected the far
regions' prices four to six days after the visits and a share of those prices, set by each item's frequency of price
change and each re-collection's delay, had genuinely changed in between.

## Three rules

- Task type: survey-research-official-statistics / nonresponse-calibration-measurement-error-adjustment, which serves Data Quality Monitoring & Alerting: the object is the measurement error in the CPI's field-collected prices and the call is each region's monitoring outcome under the quality standard.
- Domain test: the deciding quantity is each region's price-collection accuracy at the moment of recording, the error rate of a survey's field measurement estimated from a re-measurement sample, read in price statistics, where the measured price is itself a quantity that moves at each item's own frequency of change.
- Swap: "which hospital wards code accurately, judged on coding audits done a week later" keeps the arithmetic, but a diagnosis code does not move between the coding and the audit, so the step that clears ten regions here has nothing to act on.
- Layer 1: re-sent uploads in the price database (the handheld retries a failed upload; same rows, a later load batch); letter status codes replaced by numeric codes from August (the handheld software update, mapped by the code list); NSO outlet codes in the price database and back-check register against contractor outlet numbers in the visit log and schedule (crosswalked by the register); the back-check register's monthly sheets with a header block, July dates typed as text and September's columns reordered (the team's new form); visit stamps carrying the +12:00 offset; contractor area names against NSO region names; split and late visits; items the officer could not find; each produced by the system named, none placed to be caught.
- Layer 2: estimand identification, the right counterfactual: accuracy is about the price on offer at the moment of recording, so a later re-collection is evidence about that price only net of the chance the price moved over the delay; estimating accuracy net of genuine change, not as raw agreement, flips ten regions.
- Decisive step: recognising that a re-collection made days after the visit disagrees with a correctly recorded price whenever the outlet changed that price in between, and netting each back-check's chance of such a change, from its delay and its item class's daily hazard of a price change read off the price database's month-on-month changes, before setting accuracy against the bands.
- Not semantics: every field read correctly (both prices, the re-collection date, the found flag, the visit times, the status codes, the crosswalk) still leaves the easy route on the raw agreement, and on the clean truth's records the agreement files the same ten regions wrong (R3a).
- Not rule application: no filed rule says how the price at the time of recording is estimated from a later re-collection, and executing PCQS 3.1 to section 4 on the agreement files the default; the enumerated family (raw agreement, agreement with fruit and vegetables set aside, quote-by-quote persistence in four readings, netting by class, item, outlet type, region or pooled frequency, exponential or linear in the delay, three frequency windows, visit-day or index-day delays, calendar or consistent working days, expected changes subtracted from the disagreements, a common daily rate fitted to agreement against delay, a frequency netted of the collectors' own errors) spans outcome vectors from ten regions wrong to none; the standing family (every netting member) spreads zero on the outcomes and the credit, its nearest figure 0.46 points from a band edge against the golden's 0.61; the ruling-out is quiet, reached only by reading the visit log and the price database against the register.
- Analyst test: a strong analyst who reads the standard and every file correctly takes each region's accuracy as the share of its back-checked prices that agree with the officer's re-collection and files ten regions wrong: Eastwick Coast, Wexcombe Plains, Greywater, Ardmore Uplands, Corran Peninsula, Rookby Downs and Northreach under corrective action, Tamsin Bay, Fenwick and Westholm on service credits, a $7,049 credit.
- Estimand: PCQS v3.0 sections 3.1, 3.3 and 4 (pcqs_price_collection_quality_standard_v3.pdf): the population is every price recorded by the contractor's collectors at the region's outlets in July to September 2026, the outcome whether it was the price on offer at the time the collector recorded it, estimated from the back-checks (3.2) with items not found left out, compared unrounded with 98.0 and 95.5, the credit 4 per cent of the region's Schedule 4 fee.
- No decoy: nothing is planted: no memo, earlier assessment, draft or stakeholder figure states an accuracy or an outcome; the contractor's return reports activity counts only; the back-check register is the team's own record, with no block copied or withheld.
- No certified replay: no published or certified accuracy, outcome or credit exists in the pack to reproduce; the method is not hidden behind a figure the solver backs out.
- Lesson: a check made after a reading measures the reading's error plus whatever the measured thing did in between, so before charging a disagreement to the recorder, net the chance the quantity moved over the check's own delay, read from the quantity's own record of change; no build on file teaches a re-measurement whose delay lets the truth move.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 raw agreement | fires: 3.2 points at the back-checks | fires: collector and FQT price side by side | fires: the field's QA measure | no | no | fires: one ratio | no | readable |
| R1 fruit and vegetables set aside | no | fires: the class column | fires: a common QA exclusion of volatile items | no | no | fires | no | readable |
| R2 persistence read quote by quote | no | fires: next and previous month's prices in the database | no | no | no | no | no | readable |
| R3 net each back-check's chance of a genuine change over its delay (decisive) | silent: 3.1 names the moment of recording, no delay, change or frequency | silent: no column holds a delay, a visit date beside a back-check or a change frequency | silent: the field's measure is agreement | silent: no control scores accuracy | silent: no hygiene item finds it | silent: a per-back-check product across two files and a crosswalk | silent: every file it reads has its own job | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the prices recorded | every back-checked price found, both outlet types, all three months | one stratum or one month | different | PCQS 3.1 "the prices recorded ... during the quarter"; asserted |
| SF2 | at the time the collector recorded it | the visit date from the visit log | the index day | same call | asserted (index-day delays converge, nearest edge 0.46) |
| SF3 | a replacement variety's price | a recorded price | dropped | same call | PCQS 3.1 last sentence; asserted |
| SF4 | items the officer cannot find | left out | counted as disagreements | different | PCQS 3.2; asserted |
| SF5 | compared with the bands | unrounded | rounded to one decimal | same call | PCQS 3.3; asserted |
| SF6 | a price in the register | once | twice | same call | the register holds each price once; asserted |
| SF7 | a re-sent upload | one row per quote and month | both rows | same call | asserted |
| SF8 | status 30 | a replacement variety's price | a same-variety price | same call | handheld_status_codes.csv; asserted |
| SF9 | days of delay | calendar days (shops trade every day) | working days over a working month | same call | asserted |
| SF10 | the visit date | the local date of the +12:00 stamp | the UTC date | same call | asserted (S4 and R2) |
| SF11 | the change frequency's grouping and form | COICOP class by outlet type, exponential, twelve months | item, type, region, pooled; linear; other windows; expected changes subtracted; a rate fitted to the back-checks; error-netted | same call | asserted (C5, C6b) |
| SF12 | the credit | 4 per cent of each credit region's fee, summed, rounded once to the dollar | rounded per region | same call | Schedule 4 and PCQS section 4; asserted (C10) |
| SF13 | a region's prices | the outlet's region in the register | the collector's contractor area | same call | the back-check register's region equals the register's; asserted |

## Ladder

| Rung | Construction | Outcome vector (CR01 to CR14: C compliant, A corrective, S credit) | Credit | Wrong | Dies to |
|---|---|---|---|---|---|
| R0 | raw agreement (default path) | CACASASAASASAA | $7,049 | 10 | the visit log's dates against the back-check dates, and the price database's monthly changes |
| R1 | agreement with fruit and vegetables set aside | CCCCSCSCASAACA | $5,334 | 6 | PCQS 3.1's population (every price recorded); every other class also moves |
| R2 | a disagreement read as genuine where the collector's price is the previous month's and the FQT's the next month's | CCCCACACCACACC | $0 | 2 | a kept pre-filled price looks the same quote by quote (the next month confirms the officer's price), and September has no next month; its other three readings file two to four regions wrong and never a credit (C4b) |
| R3 | each back-check's chance of no change, (1 minus its class frequency) to the power delay/30.4, divided into agreement (golden) | CACCSCACCACACC | $1,775 | 0 | none |

- Margins: the golden's nearest band edge 0.61 points (Halbrook North 97.39); the default's 0.41 (Tamsin Bay
  95.09); every standing-family member at least 0.46 (index-day delays, Halbrook North 97.54); a frequency netted of
  the collectors' own errors names the same set, 0.20 from an edge (C6b). The decisive step's worth on the flipped
  regions is 1.54 to 2.14 points (golden minus agreement), against a standing-family spread of at most 1.06 on any
  region (C12).
- Golden estimates: Halbrook Central 99.18, Halbrook North 97.39, Halbrook South 99.18, Eastwick Coast 99.29, Belmont
  Valley 94.33, Wexcombe Plains 99.28, Tamsin Bay 96.68, Greywater 99.49, Ardmore Uplands 99.11, Fenwick 96.56, Corran
  Peninsula 99.39, Westholm 96.49, Rookby Downs 99.18, Northreach 99.33; the generator's truth over every price
  recorded in the quarter names the same outcomes (C11).
- Pricing sequence. (1) The residue the filed WHAT leaves is a method (how a later re-collection estimates the price at
  recording), not a knob. (2) The move: netting lifts the far regions by 1.5 to 2.1 points against a corrective band
  2.5 points wide, and crosses a band in ten of the fourteen regions. (3) The one-group-by route is the default and lands wrong; a one-line lag route
  (agreement among back-checks within a day of the visit) exists only in the capital, since the far regions' delays are
  at least three days. (4) The estimate's own sampling error is about 0.5 to 1.2 points per region; the standard rules on the
  estimate as it stands (3.3) and every licensed construction prints the same outcomes. (5) Not a ranking: banded
  verdicts, each at least 0.61 from its edge. (6) Not a change call. (7) The capital's same-day back-checks print
  accuracy directly, and exist nowhere else. (8) Every reflex is run as code in `generator/checks.py`.
- Free parameter at the naive value: a pooled frequency (all items and outlets) names the golden set, as do the item,
  outlet-type, class and region groupings, linear and exponential forms and three windows (C5).

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | every price recorded at the region's outlets in the quarter, estimated from the back-checks | PCQS 3.1, 3.2; C1 over strata, months and replacements (SF1, SF3) |
| 2 Unit of account | the recorded price; the outcome per region | PCQS 3.1 and section 4 |
| 3 Attribution window | July to September 2026 by reference month | the register's monthly sheets; C1 |
| 4 As-of dating | the visit's local date, the re-collection's date | the visit log and register; SF2, SF10 converge |
| 5 Version basis | PCQS v3.0, Schedule 4 variation 3, the price database pulled 14 October 2026 | filed in each document |
| 6 Denominator | back-checked prices the officer found | PCQS 3.2 (SF4) |
| 7 Weighting | an unweighted share of prices | PCQS 3.1 "the share of the prices"; C1 |
| 8 Window length | the frequency's window | C1 over twelve months, the quarter and January to September (SF11) |
| 9 Boundary inclusivity | 98.0 or more, below 95.5 | section 4; no standing member within 0.46 of an edge (C6) |
| 10 Rounding path | accuracy unrounded; the credit rounded once to the dollar | PCQS 3.3; SF12 |
| 11 Tie-break | none arises | outcomes are banded |
| 12 Maturity and censoring | September's prices complete in the 14 October extract | the extract date; only the persistence rung lacks a next month |
| 13 Order of operations | estimate, band, credit | section 4 order |
| 14 Row order | no result depends on file order | sums and shares only |
| 15 Duplicate resolution | one row per quote and month; each back-check once | SF6, SF7 converge |
| 16 Identity normalisation | NSO outlet code to contractor outlet number | the register's crosswalk; S4 asserts one visit per back-check |
| 17 Netting against gross | not applicable | shares of prices |
| 18 Dimensional units | dollars; delays in calendar days; a month of 30.4 days | SF9 converges |
| 19 Code and status semantics | P and 10 priced, R and 30 replacements, U and 20 not available | the code list (SF8 converges) |
| 20 Integerisation | the credit to the nearest dollar | 1,775.20 clears its edge by 0.3 (C10) |
| 21 Clause scope | section 4's bands apply to accuracy; timeliness and acceptance are reported (section 7) | PCQS sections 4 and 7 |
| 22 Forward window contents | corrective action applies next quarter; nothing forecast | section 4 |

## Literal reader

Executing PCQS 3.1 to section 4 word for word: the population is every price recorded at the region's outlets in July
to September, the outcome whether it was the price on offer at the time the collector recorded it, estimated from the
back-checks with items not found left out, compared unrounded with 98.0 and 95.5. The back-check register's dates
follow the visit log's visit dates by 0 to 7 days and the price database shows each item class's shelf prices moving
in 3.5 to 19 per cent of months, so the re-collected price is the price on the re-collection day, and a literal reader
cannot take it for the price at recording without allowing for the chance it moved; every allowance the records
license names CACCSCACCACACC and $1,775 (SF2, SF9, SF11 converge), while the raw agreement executes a different quantity
and is not compliant with 3.1 read literally.

## Oracles

None ties only under the golden. The contractor's quarterly return reports activity counts and no accuracy; the two
distractors carry no accuracy; the capital's same-day back-checks agree with both routes because their delays are near
zero; no published or earlier assessment ships.

## Ask sheet

The asks sit on the contractor's schedule and visit log and on the commodity team's decisions log, quantities the main
call's files cannot compute (no schedule or decision in them). Ask 1: by region, timeliness (PCQS 5.2) and missed visits
(28 figures). Ask 2: by region, replacement acceptance (PCQS 6.1, 14 figures). H18 home: measures every region carries
in the quarterly assessment (PCQS section 7) that the accuracy call does not turn on.

- Pair ceiling: 32.4 (cracker 46.3 on the call with 1 of 42 ask figures, mirror 18.4 with 1 of 42).
- Mirror leakage: 2.4 per cent of the ask weight (nothing in the asks comes from the call).
- Measured by: generator/ceiling.py on the cut pack.

| Ask | Primary device | Hazards | Cracker's handling | Cracker |
|---|---|---|---|---|
| Ask 1 timeliness | Lifeline Chemists' branches sold to CareMed Pharmacy on 1 August: the schedule agreed on 26 June lists the Lifeline outlet numbers for August and September, the visit log records the visits under CareMed's new numbers, and the link is the shared address in the register or the quote numbers that continue at the new outlet code in the price database (one branch per region, every figure moves 1.5 to 6.1 points) | the August window runs to 18 August (17 August a holiday); a supermarket collected over two days with the second row after the window; the +12:00 stamps read in UTC | the schedule against the visit log by outlet number with the holiday-aware window and every visit row | miss |
| Ask 1 missed visits | the same sale: each sold branch's August and September schedule rows find no visit under the old number (every figure moves by two) | the same | the same | miss |
| Ask 2 replacement acceptance | the decisions log keys a decision by quote only, and one quote per region was replaced twice in the quarter with opposite decisions, so a decision belongs to the latest replacement of its quote visited before it was decided (13 regions move when decisions are read per quote) | queries to the contractor ahead of a decision; senior re-checks dated after a first decision; September replacements decided in October; June replacements decided in July | the quarter's replacement rows in the price database with the latest decision per quote | miss |

The full includer (the sale followed, each decision dated to its replacement) keeps 42 of 42 (stress row). Zero device
rows sit in the main call's population: no back-check at a sold branch or its successor, at an outlet carrying a
repeated replacement, or at a split, late or missed visit (S1 to S3).

## Pre-ship check

Stage 3 gates on the final cut are recorded in `pipeline.json`. The three rules re-read against the built pack: the
deciding quantity is still each region's accuracy net of genuine change; the mess is Layer 1 only and every item is
asserted neutral (R2); the decisive step reads the visit log and the price database against the register (R1).

`leak.py --asof 2026-10-16` on the final cut: REVIEW, no LEAK; each REVIEW line ruled here.
- PCQS v3.0 (sweep 4): its matches are its own nouns ("the Agreement" is the services contract; back-check, recorded,
  collector and outlet file the WHAT); no sentence names a delay, a change, a frequency or the index day's distance
  from the visit, so the move is not named. Harmless.
- Schedule 4 fees (sweep 4): the contract's name, outlet and a region name in the fee table. Harmless.
- Outlet register (sweep 6): regions beside outlet codes, addresses and dates in sample; nothing scores or orders the
  regions on accuracy. Harmless.
- Collection calendar (sweep 9): the 2026 calendar is published for the year, so its October to December index days
  and holidays postdate the letter, as the real calendar's do. Harmless.
- The visit log's handheld column, first named `device` (sweep 8), renamed `handheld_id` as the export names it. Fixed.

## Architecture 2 record

Architecture 2 (2026-10-16, shipped 2026-10-16, no portal result): a university social survey unit's quality flags on
an island state's school-leaver destinations release under QS-4 v2.0, each district's NEET and higher-education entry
rates flagged on their shift under a missing-not-at-random departure measured by a 2025 nonresponse follow-up across
the island's range and carried nonrespondent by nonrespondent on the odds scale; the default carried the pooled points
gap and filed 11 of 24 flags wrong. Re-rooted 2026-11-01 at the Batch 3 queue reset; reports kept as
`determinism_check_report_arch2.md` and `leak_check_report_arch2.md`.

## Architecture 1 record

Architecture 1 (2026-10-16): the same world with the follow-up in the five middle and deprived districts; judge
SEND_BACK (underspecified_objective), report `determinism_check_report_arch1.md`.

## Tried and rejected

- QS-4 s.3 saying the sensitivity rate is worked "from that nonrespondent's own allocation" (stage 4, reader Q5):
  read as leaning toward a per-leaver odds or ratio form; cut, the per-nonrespondent grain kept.
- Architecture 1, follow-up in the five middle and deprived districts (built and judged 2026-10-16): SEND_BACK. Inside
  each attainment band its allocations barely varied, so a points gap or a ratio per band fitted the follow-up within
  1 to 4 log-likelihood units of one odds ratio while giving other flags, and the prompt's "rate the release will
  publish" was open for the four suppressed statistics. Re-rooted as architecture 2: the follow-up spans the island's
  range so the data reject every band-level and pooled points or ratio departure, and the headline rate is defined
  whatever the flag.
- Traced districts spanning the whole range in the first prototype (2026-10-16): borrowing the nearest followed-up
  district's band gaps landed 23 of 24 flags; with the affluent extremes left uncovered and every untraced district
  matched by leaver-level allocations, the borrowed gaps now agree with the golden and are an allocation-conditioned
  route to it, not a rung.
- Flags required to agree under a probit or complementary log-log shift (prototype, 2026-10-16): the follow-up
  cannot separate the links in the low-allocation tail and the logit delta is the field's standard for a binary
  outcome; in architecture 2 the probit shift agrees anyway and is asserted.
- Released rates and the follow-up's odds ratios and gaps on a rounding edge (stage 3, 2026-10-16): one or two
  recorded destinations changed between a graded and an ungraded destination (the generator's mid-bin step),
  leaving every shift and flag where it was.
- Architecture 2, the school-leaver destinations world (shipped 2026-10-16, no portal result): re-rooted 2026-11-01 at
  the Batch 3 queue reset; one architecture per world, so the survey world is closed.
- 2026-11-01 draw, candidate: a seismic network's catalogue completeness under station outages (Physical &
  Environmental Sciences): the DQ task types there are exceedance and sensor calibration, neither a catalogue's
  detection threshold, and the completeness estimators (maximum curvature, goodness of fit, entire-range) spread 0.2
  to 0.4 magnitude units on the graded figure.
- 2026-11-01 draw, candidate: a land-cover map's accuracy with the reference sample stratified on the previous edition:
  the sampling design document names the strata, so the design-based estimator is a reflex once read, and Gate H reads
  analyse-as-designed as rule application.
- 2026-11-01 draw, candidate: a survey's response rate with the unresolved addresses' eligibility to estimate:
  proportional allocation, survival extrapolation and covariate models each defensible (Gate C), and a second source
  listing occupancy turns the estimate into a join (task445 v2).
- 2026-11-01 draw, candidate: blood-pressure digit preference under a mix of 2 mmHg and 1 mmHg devices: the device's
  scale resolution is a reading of a unit (data semantics) and the swap reads the same for any instrument.
- 2026-11-01 draw, candidate: a retailer's inventory record accuracy against cycle counts taken during trading: the
  same mechanism as the chosen draw in a house domain whose deciding quantity is less native than a price's frequency
  of change.
- 2026-11-01 draw, candidate: calibration intervals under a renew-if-failed policy: the age that drives drift restarts
  only at some recorded events, the abstraction of task132's approved replacement that restarts the wear curve.
- 2026-11-01 prototype: far-region delays of seven to nine days at monthly change frequencies near 0.3 put the far
  regions' agreement at 89 to 94 per cent, the pack's largest anomaly, and the golden's sampling noise past a point;
  delays cut to four to six days and frequencies to realistic CPI levels (6 to 21 per cent a month).
- 2026-11-01 prototype: index-day delays a knife-edge from the golden (Westholm 98.02 under a 98.0 edge) with bands at
  98.0 and 96.5; the corrective band widened to 96.0 and visits front-loaded so every licensed netting names the same
  set with 0.41 points to spare.
- 2026-11-01 build: a form keyed twice in the back-check register (a copied block a reader can take for a plant) cut;
  the price database's re-sent uploads, which differ in their load batch, kept and asserted neutral.
- 2026-11-01 build: two regions with identical back-check counts (a realism tell) cleared by the FQT sample draw's
  candidate count (23), every outcome and margin unchanged or wider.
- 2026-11-02 build: collector errors carried mostly by keying slips and wrong varieties (Belmont Valley 5.6 per cent)
  added about twice each region's own slip rate to its recorded month-on-month changes, so a change frequency taken
  region by region lifted Belmont Valley to corrective action and cleared the credit; the regions' differences moved to
  kept pre-filled prices (which shift a recorded change by a month and add none), keying and variety slips held low and
  near-uniform, and the region groupings asserted (C5). Its cost: quote-by-quote persistence reads a kept price as a
  change, so rung 2 files two regions wrong instead of five, and never a credit (C4b).
- 2026-11-02 build: the corrective band at 96.0 left a frequency netted of the collectors' own errors 0.04 above it
  (Fenwick); the band moved to 95.5 with Schedule 4's credit unchanged, every standing member at least 0.46 from an
  edge and the error-netted reading 0.20.
- 2026-11-02 build: with the errors re-cut, the five non-compliant regions were the five lowest on raw agreement (an
  interval, the Shock test failed); Halbrook North's kept-price rate lowered one step so Wexcombe Plains sits between.
- 2026-11-02 build: accuracy stated to the whole per cent in the write-up (Westholm 96.49, its standing family 96.06 to
  97.03 across the 96.5 rounding line): the components now state band membership, the unit the decision is made in.

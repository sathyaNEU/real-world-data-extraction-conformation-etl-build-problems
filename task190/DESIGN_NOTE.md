# task190 design note

Arahura Bank, financial crime: how many of the cash deposits its business customers paid in during the
year to 30 June 2027 were split to stay below the prescribed transaction threshold, segment by segment,
for the annual AML/CFT report filed on 30 September 2027.

Architecture 2. Architecture 1 is spent and nothing of it is carried (`## Tried and rejected`, last entry).

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task190.json`, architecture v2, registered 2026-10-17, WARN |
| Domain, task type | Banking, Credit & Financial Risk, `fraud-aml-detection` |
| Objective | Anomaly Detection & Diagnostics (a real signal separated from the background it sits in) |
| Shape | 05, allocation to a fixed total: each segment is a bucket of the book's figure |
| Decision | `quantity_figure`, a count of deposits, with each segment's share of it |
| Gate G | `signal_vs_noise_or_hold`; decisive generator G6, then G16 and G12 |
| Strategy | `other`: the band's mass separated into the background the segment's own trade produces and the excess over it |
| Layer 2 | `estimation_fit`, own pattern `own:excess-over-the-size-profile-a-cash-book-ordinarily-shows` |
| World | New Zealand, a retail and business bank, NZD |
| Window, as-of | the reporting year 1 July 2026 to 30 June 2027; every extract pulled 19 July 2027 |
| Spine | `cash_deposit_counter_2026_2027.csv`, 56,080 rows, one deposit paid in at a counter |
| Guard | WARN: `overuse.objective` and `repeat.deliverables`, both answered below |

**Data-native sentence.** In this bank's record a cash deposit's size is a day's or two days' takings, so
each segment's deposit sizes form a smooth profile with its own slope (grocery and fuel fall away as the
amount rises, transport and personal services rise through the same range), and that profile is what makes
the thousand dollars below the reporting threshold readable: the number of deposits a segment's ordinary
trade puts in that thousand is fixed by the rest of its own profile, and the deposits placed there on
purpose are the amount above it.

**Guard WARNs answered.** `overuse.objective`: the slot keeps anomaly detection because the re-root brief
fixes its number and objective; the draw varies every other axis, including the shape (05, never used in
the last twelve), the decision type and the strategy. `repeat.deliverables`: the png and xlsx pair is
shared with task193 v1, and the chart earns its place here because the decision is a split of one total
across eight buckets, which reads at a glance as bars and not as a table; the workbook carries the figures
the report files and the chart carries the split, so neither is decoration.

**Sources read.** `analytical_tasks/02_anomaly_detection/AD13_hunt-placement-unmanaged-entry-yield.md`
(seed): nothing is taken from it in architecture 2, not even the decision shape, which was architecture 1's
and is retired with it. `guard.py mechanisms --objective anomaly-detection`: 28 spent drivers, each read
and one line written. The nearest on file are task446 v2 (a screen's yield carried across years through its
two error rates) and task448 (a list's capture measured on an overlap and carried to the unregistered by
route), and both correct a measuring instrument with its own measured performance; here no instrument is
corrected and nothing is carried anywhere, because the quantity is one period's mass separated into a
background and an excess, both of which the same record holds. `guard.py nearest` puts the driver at 0.11
against task445 v1 and 0.07 against the next two, the lowest of any build on the objective.

## Default path

1. Read `cash_deposit_detail_2027.csv` and `business_customer_register.csv`, carry the deposit system's
   customer numbers through `customer_number_crosswalk.csv`, and take each customer's segment from the
   register, applying the April 2027 code reissue so the eight segments are the handbook's eight.
2. Keep physical cash deposits paid in during the reporting year, drop the two reversals, map AR11's
   November deposits onto AR12 from the branch register, and read the machine feed's timestamps as the
   deposit dates the counter feed already carries.
3. Read clause 7.4 of `aml_programme_handbook.pdf`: the report states, for each business segment, the cash
   deposits of 9,000 dollars or more and below 10,000 dollars that were paid in below the prescribed
   transaction threshold when the amount would otherwise have been at or above it.
4. Build the split: for each customer and each day, where two or more cash deposits none of which reaches
   the threshold together reach it, the deposits in the band on that day were split below it.
5. Count those deposits by segment and total them into the committee paper.

**Ends on:** 1,287 deposits split, with grocery and convenience the largest segment at 396.
**Golden:** 400 deposits split, with transport and courier the largest segment at 90.

## Stump sentence

The default path builds the split out of the customer's own day, counting every band deposit on a day the
customer's cash reached the threshold over more than one deposit, and files **1,287**, which is the number
of band deposits belonging to businesses that pay their takings in more than once a day, because a grocery
or a service station reaches ten thousand dollars of cash on an ordinary Saturday without anyone choosing
an amount; the number placed below the threshold on purpose is the amount by which the band exceeds what
each segment's own deposit-size profile away from the band produces, 400.

## Three rules

- **Task type:** `fraud-aml-detection`, the task type in Banking, Credit & Financial Risk that serves
  Anomaly Detection: whether activity in the book is being shaped to stay out of a report, and how much.
- **Domain test:** the deciding quantity is the incidence of structuring, which financial-crime analytics
  estimates as the mass of deposits standing below a reporting threshold in excess of the mass the
  depositor's ordinary size distribution away from the threshold implies, never as the count of deposits
  that sit below it or as the output of a same-day aggregation screen, which is a referral tool and not an
  estimate.
- **Swap:** "how many of the hospital's admissions in the year were recorded below the four-hour target so
  that no breach would arise" reads as a count of admissions just under four hours: nobody is choosing the
  size of an admission to stay under a reporting duty, no reporting duty attaches to a size, and there is
  no ordinary size profile for the mass below the line to be in excess of, so the quantity collapses into
  the count and the task has nothing to estimate.
- **Layer 1:** the bank's own systems produce all of it, and none of it decides the call. The counter feed
  carries one row per deposit and the machine feed one row per envelope with its own sequence; the deposit
  system numbers customers differently from the customer master and a crosswalk carries both; AR11 closed
  into AR12 on 27 November 2026 and AR12 was renamed the same day, with the effective dates in the branch
  register; the bank's segment map was reissued on 6 April 2027 and the register holds the old code and the
  new one; the machine feed stamps in UTC while the counter feed stamps in local time, across the September
  daylight saving change; the prescribed-transaction extract ships as a preliminary and a revised file
  overlapping by six weeks; the vendor's service report is a table inside a PDF.
- **Layer 2:** `estimation_fit`. The methodological choice is what the mass standing in the thousand below
  the threshold is made of: all of it, the part a same-day screen picks out, or the part in excess of the
  background each segment's own profile produces.
- **Decisive step:** estimating the background, that is the number of deposits each segment's ordinary trade
  puts in the band, from the segment's own deposit-size profile away from the band, and taking the excess
  over it as the figure.
- **Not semantics:** clause 7.4 gives the band, the window, the unit and the outcome in one sentence and the
  dictionary gives every field, so nothing turns on a reading. A solver who reads every field and every
  clause correctly still has to decide what evidence tells it which deposits in the band would have been
  made there anyway, and the same-day screen, the customer's own habit, the customer's own prior year and
  the segment's own profile each give a different number: 1,287, 1,088, 1,406 and 400.
- **Not rule application:** clause 7.4 files what is counted and nothing else. No shipped sentence names a
  profile, a background, an excess, a distribution, a histogram, a bin, a fit, a trend or a comparison;
  nothing describes a same-day aggregation screen either, so the default path is the solver's own
  construction and not an executed procedure. A word sweep over every shipped file asserts it. Executing
  every stated rule leaves the solver holding a band, a definition and a question about what the band is
  made of.
- **Analyst test:** a strong analyst who carries every customer number through the crosswalk, applies the
  branch merger and the April code reissue, converts the machine feed's stamps and reads clause 7.4 exactly
  builds the same-day screen and files 1,287 (the `Ends on:` figure), where the number of deposits placed
  below the threshold on purpose is 400. `checks.py` runs that route on the generator's clean truth and
  asserts it files 1,287, then changes the decisive step alone and asserts 400.
- **Estimand:** clause 7.4 of `aml_programme_handbook.pdf`: "The annual report states, for each business
  segment, the number of physical cash deposits of 9,000 dollars or more and below 10,000 dollars that the
  segment's customers paid in during the reporting year and that were paid in below the prescribed
  transaction threshold when the amount would otherwise have been at or above it. The count is of deposits,
  one for one, and not of customers or of days; a deposit is counted in the reporting year in which it was
  paid in; every customer on the business register at the end of the reporting year is within its segment's
  count." Population, outcome, window, unit and comparison are all there; how the number that would
  otherwise have been at or above the threshold is arrived at is not, and that is the analysis.
- **No decoy:** nothing is planted to be caught. No scorecard, league table, ranked artifact, draft paper,
  memo or stakeholder figure ships; no block is copied; no screen, flag or indicator ships that the solver
  is meant to distrust. The segments whose band mass is largest are largest because their ordinary takings
  are that size, which is the data's own consequence and not a defect.
- **No certified replay:** no past figure for this quantity ships. The prior annual report states the
  prescribed transaction reports filed and the cash paid in, neither of which any method of this figure
  reproduces, and no closed or certified number is reproduced by any route on the ladder.
- **Lesson:** a mass standing on one side of a line is a background plus an excess, and the background is
  fixed by the shape of the same record away from the line, so a screen that selects the whole mass measures
  how much ordinary activity sits there. No build on file teaches it: of the 28 drivers on this objective
  two correct an instrument with its own measured error rates (task446 v2, task448) and none separates an
  observed mass into what the unit's own distribution away from it implies and the excess over that.

**The WHAT screen (`stumping` 1.2), run at the draw and answered here.** Architecture 1 died on this
screen three times, so it is answered part by part before anything else.

The decisive step is: *estimate the number of deposits each segment's ordinary trade puts in the band
from the segment's own deposit-size profile away from the band, and take the excess over it.*

| Part of the estimand | What it is fixed to | The sentence that files it | Does the decisive step settle it? |
|---|---|---|---|
| Population | the physical cash deposits of 9,000 or more and below 10,000 that the segment's customers paid in during the reporting year | clause 7.4, first sentence, and its closing clause putting every customer on the business register at year end inside its segment's count | No. Every member is on the register and every deposit is in the feeds; nothing is unobserved, censored or still to arrive, and the step adds and removes nobody. |
| Outcome | the deposit was paid in below the threshold when the amount would otherwise have been at or above it | clause 7.4, first sentence | No. The step does not change what is being counted; it changes how many of them the record is read to hold. |
| Window | the reporting year, 1 July 2026 to 30 June 2027 | clause 1.2, and clause 7.4's "a deposit is counted in the reporting year in which it was paid in" | No. |
| Unit | one deposit, counted one for one | clause 7.4, second sentence: "The count is of deposits, one for one, and not of customers or of days" | No. |
| Comparison | none: the figure is a level, per segment and in total, against nothing | clause 7.4 states a number per segment and no difference, ratio or benchmark | No. |

So the step settles none of the five, and the estimand is beyond argument without it. What is left open is
how the number clause 7.4 describes is arrived at, and on that several methods stand: the same-day screen
(1,287), the same screen with each customer's habit netted out (1,088), each customer against its own prior
year (1,406), and the excess of the band over what the segment's own deposit-size profile produces (400).
The first three are rejected by the record, not by argument: the screen flags 886 ordinary band deposits,
twice the number actually split, and flags deposits at every size, so it measures how often a
business pays in twice rather than what was moved; the habit filter removes 199 of them and leaves the
rest; the prior-year control counts a year's ordinary movement in the band as if it were new.

The fourth is one figure, not a family of them. The deposit-size record is one shape from end to end, so
every way of reading the background lands in the same place: 199 estimators (fit windows from 3,000 to
16,000 down to 8,000 to 11,000, step widths of 100, 200, 250 and 500 dollars, the Poisson log link,
ordinary least squares on log counts, ordinary least squares on the counts themselves, a Poisson quadratic,
one-sided fits on either side alone, one profile fitted to the whole book, and the two neighbouring
thousands averaged) give **the same eight segment figures**, every one of them, with each segment's
unrounded value 2.29 to 3.75 away from its rounding edge. The unrounded bank sum across those estimators runs
396.9 to 411.0, which is why the prompt states the bank's figure as the sum of the segment rows rather than
leaving the rounding path open.


## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 same-day screen, 1,287 | clause 7.4 states the outcome, so a solver builds a same-day construction | no column marks a split | yes, the first construction | none ships | the battery finds the duplicate envelope rows, not this | no | readable |
| 1 habit netted out, 1,088 | nothing states a habit | no column counts a customer's multi-deposit days | yes, the obvious correction | none | no | one filter | readable |
| 2 customer against its own prior year, 1,406 | nothing states a comparison | the prior year is a second file, not a column | yes, a within-unit control | none | no | one subtraction | readable |
| 3 excess over the segment's own size profile, 400 **(decisive)** | no shipped sentence names a profile, a background, a bin or a fit, asserted by word sweep | the record carries amounts and nothing that groups them by size | no: the battery, the screen, the habit filter and the year-on-year control all land elsewhere | none ships | the battery never bins an amount | no: the background has to be built before anything can be subtracted | silent |

## Semantic fork table

| id | Term or convention | Golden reading | Alternative | Ruled out by |
|---|---|---|---|---|
| SF1 | "cash deposits" | physical cash paid in over a counter or a deposit machine | includes cheque and electronic credits | clause 7.4 says physical cash deposits; the dictionary gives `instrument` with `cash`, `cheque`, `credit`, and `same call`: the band figure is identical on cash only, asserted |
| SF2 | the band | 9,000 or more and below 10,000 | 8,000 to 10,000, or at or below 10,000 | clause 7.4 states both bounds and their inclusivity |
| SF3 | "reporting year" | 1 July 2026 to 30 June 2027 | the calendar year, the bank's March financial year | clause 7.4 and clause 1.2 both state the reporting year; the prompt states the year to 30 June 2027 |
| SF4 | the date a deposit falls on | the date the deposit was paid in | the date it was posted, the value date | the dictionary gives `deposit_date` as paid in and `posted_date` as the ledger run; `same call`: the two differ on 311 deposits, none of them in the band on a year boundary, asserted |
| SF5 | the unit | one deposit | one customer, one customer-day | clause 7.4: the count is of deposits, one for one, and not of customers or of days |
| SF6 | the segment of a customer | the segment on the business register at the end of the reporting year | the segment in force when each deposit was paid in | clause 7.4's last sentence; `same call`: no customer changed segment inside the window, only its code changed, asserted |
| SF7 | the April 2027 code reissue | the same eight segments under new codes | eight new segments | the register carries the map and the dictionary states the reissue changed codes and not segments; asserted that the two codings partition identically |
| SF8 | branch AR11 after 27 November 2026 | its deposits belong to the merged branch AR12 | a ninth branch, or dropped | the branch register's effective dates; `same call`: the figure is by segment, not by branch, asserted |
| SF9 | the machine feed's timestamps | UTC, converted to the branch's local date | read as local | the dictionary states the machine feed stamps in UTC; `same call`: conversion moves 46 deposits across a date and none across the year boundary or into or out of the band, asserted |
| SF10 | the preliminary and revised prescribed-transaction extracts | the revised file for the overlap | both, or the preliminary | the extract header states the revision supersedes; the call never reads either file, asserted |
| SF11 | reversed deposits | excluded, both the deposit and its reversal | the deposit kept | the dictionary gives `reversal_of`; `same call`: the two reversed deposits are not in the band, asserted |
| SF12 | rounding of the counts | each segment's figure to the nearest 10, the bank's figure their sum | the unrounded bank sum rounded once | the prompt states which path governs, in its own sentence; the unrounded sum across the 199 estimators runs 396.9 to 411.0, so the path is pinned rather than left to converge |
| SF15 | "the hours the service log puts the estate out of service" | the bank's own service log | the vendor's service report, whose site totals run higher | the prompt names the service log; the vendor's report is what the third ask compares against |
| SF16 | "raised into it then moved out of it" | a customer raised into the band with a later accepted event taking it out | any later event, or the rating at year end | every rating history chains, so a later event's starting band is the band it was in; the two readings coincide, asserted |
| SF13 | "paid in below the threshold when the amount would otherwise have been at or above it" | a count of deposits in the band in excess of the background the segment's profile produces | a count of every band deposit, a count the same-day screen selects | neither alternative is a reading of the clause: the clause's words are the same under all three, and the three differ by what evidence is used, which is the analysis and not the text. The fork table carries no reading of this clause, and the ladder carries the three figures |
| SF14 | the total | the bank's figure, the sum of its eight segment figures | a figure built on the book without segmenting | clause 7.4 states the report is by segment; `same call`: the eight segment figures sum to 400 and the rounding of the unrounded sum of the segment excesses is 400 under every accepted estimator, asserted |

## Ladder

| Rung | The analysis | Figure | Largest segment it names | Worth |
|---|---|---|---|---|
| below 0 | count the band | 2,196 | grocery and convenience, 626 | the clause's second half is ignored; no competent solver stops here |
| 0 | the same-day screen: band deposits on a day the customer's cash reached the threshold over two or more deposits | **1,287** | grocery and convenience, 396 | the default path; 3.22x the golden |
| 1 | the same screen with each customer's own habit netted out (drop customers whose screened days are more than half their deposit days) | 1,088 | grocery and convenience, 369 | one filter; 2.72x |
| 2 | each customer against its own prior year, the rise in its band deposits | 1,406 | hospitality, 354 | a within-unit control; 3.52x, and it walks the wrong way |
| 3 | **the excess over each segment's own deposit-size profile away from the band** | **400** | transport and courier, 90 | the golden; the answer is the extreme of the ladder |

**Position and margins.** On rung 0 the golden's largest segment, transport and courier, sits fourth of
eight (396, 304, 194, 119, 110, 64, 53, 47 against the golden's 90, 70, 60, 60, 30, 30, 30, 30), so the
default path does not merely mis-size the figure, it names a different segment as the largest. The decisive
move is 2,054 to 400, the largest move on the ladder and never the smallest. Every rung reproduces from the
raw files, names its own largest segment, and dies to one construction.

**The grid.** The wrong answers on this build are the rungs, not fit variants: the band count (2,196), the
same-day screen (1,287), the habit filter (1,088) and the prior-year control (1,406). One profile fitted to
the whole book is not a wrong cell here, because it converges with the rest (400); it is reported as one of
the 199 estimators. No single error files 400.

**Convergence, measured rather than claimed.** `checks.py` runs all 199 estimators on the shipped amounts
and asserts that the set of eight rounded segment figures they give has exactly one member, and that it
sums to 400; `verify.py` repeats 120 of them on its own code path from the bundle alone. The measured
per-segment ranges are grocery 58.8 to 60.6, hospitality 58.2 to 62.1, transport 89.3 to 92.7, trades 68.0
to 71.0, rural 28.9 to 32.7, fuel 30.3 to 32.5, personal services 29.1 to 32.1, clubs 29.1 to 32.1. Both
the log and the count families fit the record equally well (chi-square per degree of freedom about 0.001
each), which is the point: the figure does not depend on which of them a reader picks. A placebo run of the
same estimator at twelve positions where no deposits were split reads nought, scatter 0.39, bias -0.04.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every physical cash deposit in the band paid in during the reporting year by a customer on the business register | clause 7.4 files it literally; all members observed, nothing censored, nothing arriving late; C1 asserted |
| 2 | Unit of account | one deposit | clause 7.4: one for one, not customers, not days (SF5) |
| 3 | Attribution window | the date the deposit was paid in | clause 7.4; SF4 asserted, 311 deposits differ on posted date, none on a year boundary |
| 4 | As-of dating | every extract pulled 19 July 2027, the window closed 30 June 2027 | the extract headers state it; the register's segment is the one in force at year end (SF6) |
| 5 | Version basis | the revised prescribed-transaction extract supersedes the preliminary one | the extract header; the call reads neither (SF10) |
| 6 | Denominator | none: the figure is a count, not a rate | clause 7.4 states a number of deposits; the segment's deposits paid in ship beside it as a separate figure |
| 7 | Weighting | none: deposits are counted one for one | SF5; no weighting enters the golden |
| 8 | Window length | the background is read off the segment's profile over the stretch the record is log-linear across | C1 over six fit windows and three bin widths, all giving 400 |
| 9 | Boundary inclusivity | 9,000 inclusive, 10,000 exclusive | clause 7.4 states both; asserted that no deposit falls at exactly 9,000.00 or 10,000.00 |
| 10 | Rounding path | once, at the end, to the nearest 10 deposits | the prompt states it once; SF12 asserts both paths give 400 |
| 11 | Tie-break | the largest segment is named; transport and courier at 90 leads trades and construction at 70 | a 20-deposit gap at the stated rounding, asserted |
| 12 | Maturity and censoring | nothing is censored: the year is closed, every deposit is recorded, no outcome arrives later | asserted that the extract holds no deposit dated after 30 June 2027 and no record is amended after the pull |
| 13 | Order of operations | the background is estimated per segment, then subtracted, then rounded | C1: subtract-then-round and round-then-subtract both give 400, asserted |
| 14 | Row order | no step depends on file order | asserted over six permutations of the deposit file |
| 15 | Duplicate resolution | one deposit per counter row; the machine feed's envelope rows collapse on `envelope_id` to one deposit | the dictionary states the machine grain; asserted that collapsing is the only reading that reconciles to the branch cash summary |
| 16 | Identity normalisation | the crosswalk carries the deposit system's number onto the master's | the crosswalk is complete and one-to-one over the window, asserted |
| 17 | Netting against gross | gross: reversals and their deposits are both excluded, nothing else nets | the dictionary gives `reversal_of`; SF11 asserted |
| 18 | Dimensional units | every amount is NZD to the cent in both feeds | asserted; the one file carrying thousands is an ask file the call never reads |
| 19 | Code and status semantics | `instrument`, `channel`, `segment_code`, `reversal_of` as the dictionary gives them | dictionary semantics; SF1, SF7, SF11; never the stump |
| 20 | Integerisation | counts are whole; the excess is rounded to the nearest 10 once | SF12; the unrounded excess sits 3.0 to 4.0 from its edge |
| 21 | Clause scope | clause 7.4 governs the annual report's figure; clause 3.1 the reporting duty; clause 9.2 the retention period | the handbook's own headings; asserted no other clause states a count |
| 22 | Forward window contents | none: the window closed before the extract | the call is retrospective, with its reason below |

**Why the call is retrospective.** The figure is the bank's own measured incidence for a closed reporting
year, which is what section 60 of the Act's annual report states; a figure about an open year would be a
forecast of a quantity the record has not yet produced and would retag the build as Forecasting. The
commitment itself is not yet made: the report is filed on 30 September 2027 and the figure in it is the
decision.

## Literal reader

A reader who executes the prompt and clause 7.4 word for word, inferring nothing, has the population, the
band, the window, the unit and the outcome fixed, and the only thing the text does not give is what
evidence shows which band deposits would have been made at that amount anyway; every reading of every term
gives the golden (SF1 to SF14, each asserted), and the three constructions a reader may build instead of
the background are analyses rather than readings, which is why the ladder and not the fork table carries
them.

## Oracles

Every control in the pack reads the same on the wrong path and on the golden. The branch cash summary
reconciles to the deposit detail under every rung because it sums amounts and not band counts (asserted to
the cent). The prior annual report states the prescribed transaction reports filed (2,742) and the cash
paid in, and no rung reproduces either, because every deposit on the ladder is below the threshold and so
outside the reports filed. The prescribed-transaction extracts cover only deposits at or above the
threshold, so they are blind to the band by construction. No corpus scores a method, no document ranks the
segments, and nothing in the pack states a figure for structured deposits in any year.

## Ask sheet

Three asks, none keyed to the call or its construction, all on rows outside the call's declared population
(the deposit rows), each a component of the report the same officer signs.

| Ask | Figures | H18 home | Primary device | File, columns | Stops | Lazy delta |
|---|---|---|---|---|---|---|
| A1 till variance | per branch and quarter: sessions recorded, sessions over the tolerance in force, net variance in dollars | the cash-handling control the report's branch section covers | D8 clocks: the machine collection sessions are stamped UTC while counter sessions are local, across the September daylight saving change, so sessions on a quarter boundary fall in the wrong quarter | `till_balance_log_2026_2027.csv`, 11 columns, with `cash_tolerance_register.csv` | 4: raw stamps; converted but tolerance fixed; tolerance versioned but sessions double counted; the answer | 19 of 56 cells move |
| A2 risk rating movements | per band: customers raised, lowered, and raised then lowered inside the year | the customer risk profile the report's section 4 covers | D2 version: the file carries each rating event as delivered and as accepted, and eleven events were superseded by a correction with the same effective date and a later load stamp | `risk_rating_history.csv`, 9 columns, with `rating_scale_map.csv` | 4: latest delivered; latest accepted but the April relabel unmapped; mapped but the merged customer counted twice; the answer | 9 of 15 cells move |
| A3 machine availability | per month: hours out of service by machine, whether any machine has no service record and how many, whether any site's hours differ from the vendor's by more than two and which | the deposit channel the report's section 6 covers | D6 grain: the vendor's report is per site per month while the bank's log is per machine per incident, and two sites hold two machines; D4 absence: three decommissioned machines have no log rows, which is not nought hours | `machine_service_log_2027.csv` plus `vendor_service_report_2027.pdf`, 10 columns | 4: log only; log plus vendor at the wrong grain; grain right but absence read as nought; the answer | 14 of 24 cells move |

**Main population zero-counts.** Zero device rows and zero hazard rows in `cash_deposit_detail_2027.csv`,
`cash_deposit_detail_2026.csv`, `business_customer_register.csv`, `customer_number_crosswalk.csv` and
`branch_register.csv`, asserted by count in `checks.py`. Deleting every ask file leaves the call
unchanged, asserted.

**Hazards.** Three, each moving several asks: the April 2027 code and scale reissue (A2, A3); the AR11 into
AR12 merger (A1, A3); the UTC against local stamping (A1, A3). Per-ask deltas above.

**Referee.** One byte-clean referee, `branch_cash_summary_2027.csv`, arbitrates A1's session count against
the till log without stating a variance, and ties under every handling of the main call.

| Ask | The cracker, who landed the call and ran the battery | Verdict |
|---|---|---|
| A1 | converts the machine stamps, misses that the tolerance was reissued on 1 January 2027 | miss |
| A2 | takes the latest delivered rating event, so eleven superseded events stand | miss |
| A3 | sums the bank's log per site, so the two-machine sites double count and the three decommissioned machines read as nought | miss |

Pair ceiling: 39.5

Mirror leakage: 22.0

## Pre-ship check

**Free gates, all green at this cut.**

| Gate | Result |
|---|---|
| `precut.py task190` | 49 checks, 0 FAIL, 0 WARN |
| `voice-check.py task190` | PASS, 997 characters |
| generator `checks.py` | 114 assertions, including the three-rules block R1 to R3c on the clean truth and the 199-estimator convergence sweep |
| `verify.py` (reads `target/` and `figures.json` only, own code path) | 185 checks, 0 failed, including 120 of the estimators on its own implementation |
| two consecutive rebuilds | `target/` and `golden/` byte-identical |
| `figures_check.py task190` | 86 figures in blocks 1 to 4, 0 absent from `figures.json` |
| input gates | 21 files, 4 formats (csv, xlsx, pdf, md), 56,080 rows in `cash_deposit_counter_2026_2027.csv`, 3 distractors declared in `metadata.json` |
| `leak.py task190 --asof 2027-07-19` | REVIEW, every line answered below |
| `guard.py surface task190` | no promoted pair; no persona appears in the cut pack's content |
| `guard.py heart task190` | WARN, nearest driver 0.11 (task445 v1) |
| container scrub audit | clean: no writer signature, no out-of-band timestamp |

**Guard WARNs answered.** `repeat.deliverables` (png and xlsx, shared with task238): the chart earns its
place because the decision is one total split across eight buckets, which reads at a glance as bars and not
as a table. `repeat.question_form` (how-many, shared with task266): the call is a count of deposits, so any
other opening would be a worse question for it; the decision type, shape and strategy are all varied
against the neighbours.

**The leak report's REVIEW lines, answered.** Sweeps 3 and 4 flag the handbook, last year's filed report
and the extract notes for sharing the call's vocabulary and between 5 and 9 of the stump paragraph's 25
terms. The shared terms are deposit, register, reporting, extract, customer, states and counter, which are
the ordinary nouns of a bank's deposit records; the call's vocabulary is shared because clause 7.4 is the
estimand and the question is asked in the handbook's words. No golden figure appears in any document:
asserted over every shipped PDF, which carry no 400 and no 2,196. None of profile, background, excess,
screen, same-day, construction or decisive appears in any shipped file, asserted by word sweep in
`checks.py`. The prompt's own flagged sentence carries two stump terms, deposit and customer, which the
question cannot be asked without. Sweep 10 is the container audit reporting that it ran and found nothing.

**Realism sweep.** No identical deposit count across segments; no round segment total; no round customer
count; tellers vary by branch; deposits run across a trading day with seconds on every stamp; the acquirer
extract has gaps; ANZSIC codes are the segment's own and vary within it; round figures are as common in
the band as at every other size (asserted, so the pile at 9,900 and 9,950 does not single the split
deposits out); every rating history chains with no event leaving a rating where it was; the machine estate
is a register and the service log covers it. The provenance file reads as the data team's own compile note
(`reduce-house-fixes` H24), the manifest names every shipped file (H9), no record or report date runs past
the pull date (H16), and every handbook paragraph the goldens cite resolves (H8).

**What the stage 4 threads found, and what was done.** The determinism judge returned NOT_DETERMINISTIC,
`competing_defensible_answer`, SEND_BACK, with Gate G and Gate H passing and the decisive step graded
analytical. The finding was calibration, not architecture: the counterfactual's method was not forced and
the data did not separate the candidates, with the judge measuring 310 to 512 across windows and families
against the filed 400. Three side answers did not reproduce, the ladder's rung 0 could not be reproduced,
and the reader found the rating history contradicting itself and the structuring signal too faint. Every
one of those is closed in the generator in one pass: the deposit-size record is now one shape from end to
end so all 199 estimators agree; the rounding path, the hours source and the band wording are pinned in the
prompt; the machine estate ships as a register so the machines with no service record are forced; the
rating events chain; the split deposits pile on round figures just under the threshold as real structuring
does; every rung is re-measured on the shipped bundle; and the note reports the measured spread instead of
claiming convergence. The claim the judge showed to be false, that every window and step width gives the
same figures, is gone.

## Tried and rejected

- Ranking the lines by the share of alerts that prove real (the yield reading): `guard.py nearest`
  measured the driver at 0.15 against task446 v2, which already builds a yield carried onto a
  population with a different base rate. Dropped at the draw, before any data was cut.
- The seed's own architecture, a filed scorecard ranking the divisions on confirmed movement per 1,000
  accounts: a stated score deciding the call, which the 10/10 rules ban, and a ranked artifact Gate G
  forbids shipping. No scorecard ships.
- Clause 9.2, which said the bank maintains no ranking of its business lines: it was there to keep a
  ranked artifact out of the pack, but the isolated reader quoted it as a sentence placed on purpose to
  reassure, which is a tell. Removed, and the Gate G guarantee is now carried by an assertion over
  every shipped PDF instead of by a sentence in one of them.
- A register in which every case is confirmed, every identifier sequential and no case amended past a
  second version: the reader called the pack plausibly real but slightly too orderly. The register now
  carries the cases that were put to the head of financial crime and not accepted, with no confirmed
  month, identifiers numbered as cases were opened with the gaps the register's own deletions leave,
  and ten cases amended twice. No graded figure moves: `figures.json` is byte-identical across the
  change, and SF14 asserts the wider reading of the disposition field names the same three lines.
- Clause 6.2's closing phrase, "the expectation is taken over the cases the line's own closed record
  implies", and clause 6.3's definition of that closed record: both were added by the first
  determinism repair, to close a fork between the expectation and a single realisation. Two isolated
  readers then quoted the pair as naming the method, one of them saying the stump had become "did you
  read 6.2" rather than "did you find the pitfall", and the determinism judge marked Gate F borderline
  for the same reason. That is the failure the house rules name: a determinism repair that files the
  HOW. Removed. The expectation is now carried by "expected to be carrying" alone, the realisation
  reading is ruled out because the register holds no unseen case (asserted), and the window the
  construction needs is closed by convergence over 36 windows and the register entire rather than by a
  clause. Clause 6.3 keeps the look-back span as a fact of the bank's governance, which says nothing
  about using it.
- The contract register's note that "the ledger holds the ticket under both references and the hours
  are owed once", and the ledger's own note column saying a row was "reissued under the credit note
  series": a filed rule adjudicating an ask's device, and a narration of it, which the ask layer's
  first two bans forbid. Both removed. Each credit note now names the ticket it reverses, so the
  reissued pair reverses more hours than that ticket was billed and only an internal inconsistency
  finds it.
- A register whose typologies were uniform across the eight lines, whose annual case counts barely
  moved, whose confirmation lag was uniform on nought to two months everywhere and whose amendments
  multiplied an amount by 1.08: the isolated reader read all four as generated. The mix is now what
  each line actually sees, the monthly count is a Poisson draw on a yearly and a seasonal factor, the
  confirmation lag runs with the line's own detection lag, and an amendment moves an amount either way.
- **Architecture 1, the whole of it, is spent.** Three consecutive judge SEND_BACK verdicts and a Gate
  F graded moderate to borderline then moderate to low. The reason is structural rather than a list of
  fixes. `determinism-check` requires the estimand to say that the population holds cases the bank has
  no record of yet, and requires the method to be forced, which here means every estimation route
  converging: it now does, over 36 windows of two years or more and the register entire. Once both
  hold, the only analytical step left is deciding to nowcast rather than count, and clause 6.2 has to
  announce that to be literal. Every Gate F repair reopened a determinism fork and every determinism
  repair closed the stump, twice round. Three isolated readers built the nowcast and landed the call at
  80 to 90 per cent confidence, so the portal's top two would both land it. The slot re-roots at stage
  1 with a new driver; the stock-from-arrivals-and-time-unseen driver is not reused.
- **Architecture 2, the WHAT screen run on four candidate decisive steps before this one.** Correcting
  the monitoring's output with the sensitivity and specificity measured on an assurance sample: dropped
  at the draw, because task446 v2 ships that driver in this same domain and task448 ships its stratified
  form, which the re-root brief bans. Estimating the undetected caseload from a below-the-line review
  sample: the same two cards, plus the sample's own arms announce the step. The excess of deposits over
  a counterfactual named in the estimand as "the number that would otherwise have been made there":
  dropped because naming the counterfactual that way excludes the band count by the clause's own words,
  which turns the decisive step into rule application and fails the analyst test. Ranking the eight
  segments rather than sizing the figure: dropped because a three-of-eight set pays a response that
  gets two members right, and the ladder cannot keep the top two off a set the way it keeps them off a
  figure. The step that survived settles none of the estimand's five parts, which `## Three rules`
  answers line by line.
- **The first cut of architecture 2's deposit-size record, spent at stage 4.** The law had one shape over
  5,000 to 16,000 and a different one below 5,000, so a fit window starting at 4,000 or 3,000 crossed the
  kink and gave 440 and 512 against the filed 400, and the per-bin integer rounding left enough scatter for
  an unweighted log fit at 100-dollar steps to read 421 and a one-sided fit to read 311. The design note
  asserted convergence it had not measured. Replaced by one shape end to end, a gentle decay of the same
  rate in every segment, with each 500-dollar block's count exact and the pile on round figures spread
  evenly inside it, so every family, window and step width lands on the same eight figures. The sweep is
  now run and asserted rather than claimed.
- **The pooled book profile as a wrong cell.** It gave 370 against 400 on the old record, and the note
  carried it as a single-error cell. On a record with one shape it converges with the rest, and it is now
  reported as one of the 199 estimators rather than as a rival.
- **Rating events drawn independently.** 205 of 805 follow-on events started from a band the customer was
  not in and 318 moved a rating to itself, which the solver's-eye reader read as generated and which gave
  "moved out of the band" more than one reading. The events now chain, so the ask has one answer.
- **A machine estate defined only by the service log.** The deposit feed invented machine ids the log never
  held, so "any machine with no service record" had no forced answer. The estate now ships as
  `deposit_machine_register.csv` with install and withdrawal dates, the feed takes deposits only at a
  machine in service that day, and the answer is the register's own.

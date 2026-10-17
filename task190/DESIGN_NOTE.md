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
| Spine | `cash_deposit_detail_2027.csv`, 45,304 rows, one physical cash deposit |
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

**Ends on:** 1,223 deposits split, with grocery and convenience the largest segment at 356.
**Golden:** 400 deposits split, with transport and courier the largest segment at 90.

## Stump sentence

The default path builds the split out of the customer's own day, counting every band deposit on a day the
customer's cash reached the threshold over more than one deposit, and files **1,223**, which is the number
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
  the segment's own profile each give a different number: 1,223, 1,077, 2,054 and 400.
- **Not rule application:** clause 7.4 files what is counted and nothing else. No shipped sentence names a
  profile, a background, an excess, a distribution, a histogram, a bin, a fit, a trend or a comparison;
  nothing describes a same-day aggregation screen either, so the default path is the solver's own
  construction and not an executed procedure. A word sweep over every shipped file asserts it. Executing
  every stated rule leaves the solver holding a band, a definition and a question about what the band is
  made of.
- **Analyst test:** a strong analyst who carries every customer number through the crosswalk, applies the
  branch merger and the April code reissue, converts the machine feed's stamps and reads clause 7.4 exactly
  builds the same-day screen and files 1,223 (the `Ends on:` figure), where the number of deposits placed
  below the threshold on purpose is 400. `checks.py` runs that route on the generator's clean truth and
  asserts it files 1,223, then changes the decisive step alone and asserts 400.
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
how the number clause 7.4 describes is arrived at, and on that two or more methods stand: the same-day
screen (1,223), the same screen with each customer's habit netted out (1,077), each customer against its
own prior year (2,054), and the excess over the segment's own profile (400). The data's own structure
rules out the first three and selects the fourth: each segment's deposit-size profile is log-linear across
the stretch either side of the band, with residuals 0.0005 to 0.0029 of the mean, so the number the band
would hold without the splitting is fixed by the record; the book's pooled profile is not log-linear
(residuals 0.0088), which is why one fit for the whole book is rejected by its own residuals; and every
window and bin width inside the stretch gives the same eight figures. Filing none of that in the pack is
what keeps the step analysis rather than rule application: no shipped sentence names a profile, a
background, an excess, a bin or a fit.


## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 same-day screen, 1,223 | clause 7.4 states the outcome, so a solver builds a same-day construction | no column marks a split | yes, the first construction | none ships | the battery finds the duplicate envelope rows, not this | no | readable |
| 1 habit netted out, 1,077 | nothing states a habit | no column counts a customer's multi-deposit days | yes, the obvious correction | none | no | one filter | readable |
| 2 customer against its own prior year, 2,054 | nothing states a comparison | the prior year is a second file, not a column | yes, a within-unit control | none | no | one subtraction | readable |
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
| SF12 | rounding of the counts | to the nearest 10 deposits, once, at the end | per segment then summed, or unrounded | the prompt states the rounding once; `same call`: the sum of the rounded segment figures and the rounding of the unrounded sum are both 400, asserted over all eleven estimators |
| SF13 | "paid in below the threshold when the amount would otherwise have been at or above it" | a count of deposits in the band in excess of the background the segment's profile produces | a count of every band deposit, a count the same-day screen selects | neither alternative is a reading of the clause: the clause's words are the same under all three, and the three differ by what evidence is used, which is the analysis and not the text. The fork table carries no reading of this clause, and the ladder carries the three figures |
| SF14 | the total | the bank's figure, the sum of its eight segment figures | a figure built on the book without segmenting | clause 7.4 states the report is by segment; `same call`: the eight segment figures sum to 400 and the rounding of the unrounded sum of the segment excesses is 400 under every accepted estimator, asserted |

## Ladder

| Rung | The analysis | Figure | Largest segment it names | Worth |
|---|---|---|---|---|
| below 0 | count the band | 3,520 | grocery and convenience, 897 | the clause's second half is ignored; no competent solver stops here |
| 0 | the same-day screen: band deposits on a day the customer's cash reached the threshold over two or more deposits | **1,223** | grocery and convenience, 356 | the default path; 3.06x the golden |
| 1 | the same screen with each customer's own habit netted out (drop customers whose screened days are more than half their deposit days) | 1,077 | grocery and convenience, 346 | one filter; 2.69x |
| 2 | each customer against its own prior year, the rise in its band deposits | 2,054 | hospitality, 485 | a within-unit control; 5.14x, and it walks the wrong way |
| 3 | **the excess over each segment's own deposit-size profile away from the band** | **400** | transport and courier, 90 | the golden; the answer is the extreme of the ladder |

**Position and margins.** On rung 0 the golden's largest segment, transport and courier, sits fourth of
eight (356, 268, 170, 133, 117, 64, 60, 55 against the golden's 90, 70, 60, 60, 30, 30, 30, 30), so the
default path does not merely mis-size the figure, it names a different segment as the largest. The decisive
move is 2,054 to 400, the largest move on the ladder and never the smallest. Every rung reproduces from the
raw files, names its own largest segment, and dies to one construction.

**The grid.** Single-error cells, each a named wrong figure: one profile fitted to the whole book rather
than to each segment, 370 (7.5 per cent from the golden, and the book's own residuals away from the band
are 0.0088 of the mean against 0.0005 to 0.0029 for each segment, so the record rejects it); the band read
over the prior year, 289; the profile fitted over a window reaching outside the stretch the record is
log-linear over, residuals 0.23 to 1.01 of the mean, rejected by the record; a two-bin local average in
place of a fit, whose placebo scatter at twenty positions where the excess is nought is more than five
times the fitted estimator's. No cell files 400 by a single error.

**Convergence.** Eleven estimators of the background (fit windows from 5,000 to 16,000, 5,500 to 15,000,
6,000 to 14,000, 5,000 to 15,000, 5,000 to 14,000 and 6,000 to 16,000; bin widths 200, 250 and 500; and
three local-average forms) give the same eight segment figures and the same total of 400, with every
segment's unrounded excess 3.0 to 4.0 away from its rounding edge. Asserted in `checks.py` and in
`verify.py`.

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
| `voice-check.py task190` | PASS, 998 characters |
| generator `checks.py` | 205 assertions, including the three-rules block R1 to R3c on the clean truth |
| `verify.py` (reads `target/` and `figures.json` only, own code path) | 112 checks, 0 failed |
| two consecutive rebuilds | `target/` and `golden/` byte-identical |
| `figures_check.py task190` | 86 figures in blocks 1 to 4, 0 absent from `figures.json` |
| input gates | 20 files, 4 formats (csv, xlsx, pdf, md), 56,325 rows in `cash_deposit_counter_2026_2027.csv`, 3 distractors declared in `metadata.json` |
| `leak.py task190 --asof 2027-07-19` | REVIEW, every line answered below |
| `guard.py surface task190` | no promoted pair; no persona appears in the cut pack's content |
| `guard.py heart task190` | WARN, nearest driver 0.11 (task445 v1) |
| container scrub audit | clean: no writer signature, no out-of-band timestamp |

**The leak report's REVIEW lines, answered.**

- Sweep 3, `aml_programme_handbook.pdf`, 10 of 12 words of the committed call: the call is quoted in the
  handbook's own vocabulary because clause 7.4 is the estimand, and the prompt asks the question in the
  handbook's words. No golden figure appears: the documents carry no 400, no 3,520 and no segment figure,
  asserted by extraction over every shipped PDF.
- Sweep 3, `annual_report_extract_2026.pdf`, 8 of 12: the prior year's report names the same quantity it
  does not state, and says so ("was first stated for the year ended 30 June 2027 and is not given here").
  It carries last year's prescribed transaction count and cash paid in, neither of which any rung
  reproduces.
- Sweep 3, `provenance.md`, 8 of 12: the extract notes name the deposits and the reporting year, which is
  what they are notes about. No figure in them is on any rung.
- Sweep 4, the same three documents, 4 to 8 of 25 stump terms: the terms are deposit, register, reporting,
  extract, customer, closed and states, which are the ordinary nouns of a bank's deposit records. None of
  profile, background, excess, screen, same-day, construction or decisive appears in any shipped file,
  asserted by word sweep in `checks.py`.
- Sweep 4, the prompt sentence carrying two stump terms: the two are "deposit" and "customer". The
  question cannot be asked without them.
- Sweep 10, INFO: the container audit ran and found nothing, which is the result wanted.

**Realism sweep.** No identical deposit count across segments; no round segment total; round amounts under
4 per cent of deposits; the drawn personas only; no placeholder identity; the monthly counts per segment
carry no repeated block. The provenance file reads as the data team's own compile note (`reduce-house-fixes`
H24), the manifest names every shipped file (H9), no record or report date runs past the pull date (H16),
and every handbook paragraph the goldens cite resolves (H8).

**What stage 4 still owes.** The isolated leak reader and the determinism judge have not run: this session
has no `Agent` tool. Both briefs are staged with their own isolated inputs, and the verdicts come back
through the orchestrator.

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

# DS10 — How many promotional emails to commit for December, when every retry counts against the quota that the retries themselves exhaust

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Product Analytics · CRM and lifecycle messaging |
| Mirrors | Committing volume against a shared quota whose retries consume the quota they are caused by (AWS and Google Cloud API rate limits with client retries, SMS aggregator throughput caps, Meta and Google push-notification budgets) |
| Decision shape | One figure committed at a date: next billing month's promotional send volume, booked on the 25th |
| Committed call | Promotional first attempts for December, in millions to one decimal |
| Gap · Pattern | Gap 1 (time) over Gap 3 (objective) · measured #22's architecture (a self-referencing load whose ceiling binds only after the fixed-point solve), with a latent attribution marker (#17) at rung 1 |
| Gate G mechanism | binding_constraint, with forecasting |
| Measured traps engaged | #22 solves a self-referencing rule in one pass · #17 guesses an attribution the data can settle · #13 validates on one population, applies to another · #10 notes a binding limit as a risk |
| Calibration form | Retry or revision log: the email service's retry log, thirteen months of attempts by mailbox provider and hour, with deferral codes and retry numbers |
| Driving force | Every attempt counts against the 60M quota, retries included. A mailbox provider defers everything above its hourly acceptance ceiling, so retries are part of the load that creates them. A constant retry rate is exact for every closed month, last December's 4.5% included, because every closed holiday week ran four-hour batches. This December's calendar sends doorbusters in two hours: deferrals from 08:00 land at 09:00, which is already over the ceiling, and the load compounds. Only an hourly fixed point, with the ceilings recovered from the log's provider-hours, finds the 29.7M that fit. |

## 1. Situation

A retailer's CRM team commits next month's promotional email volume on the 25th, and merchandising books revenue against it. The email
service contract gives a 60M-attempt monthly quota and stops sending when it is reached. Transactional mail shares the quota and goes
first. Deferred messages are retried at one, four and twelve hours. December's calendar puts 40% of promotional volume into the holiday
week, as doorbuster batches at 08:00 and 09:00. Last month the team sent 32.0M promotional, 7.5M order and 8.5M account emails. The CRM
lead is confident last December is a safe guide.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. The log's attempts and retries, last month's 0.30%
  and last December's 4.5% retry rates, and the order plan are all right. The difficulty is that the retry load is a function of the hourly
  volume it adds to, and this December's volume has a shape no closed month had.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the CRM lead's view. Quota less forecast transactional mail, divided by the seasonal retry rate, still commits
  37.8M, and every closed month reconciles.
* **Instrument repair.** Log every attempt perfectly. Each closed month still reproduces under its own constant rate, and the two-hour batch
  is still in the future.
* **Lens swap.** The naive figure treats retries as a fixed share of first attempts. The answer is built from the hours in which a
  provider's queue overflows, a population of deferred attempts that exists only under next month's schedule.

## 3. The driving force

A strong solver reserves the quota for transactional mail, types each transactional message by its sending subdomain so that order mail
scales with December's order plan and account mail does not, and swaps November's 0.30% retry rate for last December's 4.5%. Each step is
competent, and every closed month reproduces. But deferrals are not a rate. In the log's provider-hours, a provider accepts everything up to
its hourly ceiling (300k, 100k, 75k and 65k for the four providers) and defers the whole excess, with a 0.3% background either way.
December's doorbuster hours put 229k an hour at the strict provider. The 08:00 excess is retried at 09:00, which is over the ceiling, so it
defers again and returns at 13:00 and 21:00. Retries are part of their own base. Solving the month hour by hour, 50.2M first attempts
generate 9.8M retries, and only 29.7M of the first attempts can be promotional.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Quota less last month's transactional attempts, divided by 1 + last month's pooled retry rate (0.30%) | 43.9M (+48%) | The contract, last month's actuals and a measured rate | The sending subdomains: order mail scales with December's order plan (+60%) and account mail does not |
| 1 | Transactional typed by sending subdomain (#17): order mail 12.0M, account mail 8.5M | 39.4M (+33%) | A forecast built from the order plan | The retry log: last December's retry rate was 4.5%, fifteen times November's |
| 2 | Last December's pooled retry rate | 37.8M (+27%) | The right season and the right type split | The log at provider-hour grain: deferrals are 0.3% at or below each ceiling and the whole excess above it, and December's calendar halves the batch window |
| 3 | **Decisive:** hourly fixed point. Each hour's load is first attempts plus retries due, the excess over each ceiling is deferred to +1, +4 and +12 h with transactional first, and the largest promotional volume whose attempts total 60.0M is taken | **29.7M** | — | — |

* **Figure shape.** Every correction walks the figure down, and the answer is the minimum of the rung cells. Offsets from the answer: +48%,
  +33%, +27%.
* **Partial correction priced (L3).** Running the hourly fixed point with last December's four-hour batches, ignoring the calendar's
  doorbusters, commits 35.1M (+18%). Running it with transactional mail unscaled commits 33.3M (+12%). Scaling all transactional mail with
  orders, account mail included, over-reserves and commits 26.7M (−10%).
* **Grid.** Transactional (unscaled, by subdomain, all scaled) × retries (November rate, December rate, hourly fixed point) × batch window
  (calendar, four hours) gives 12 feasible cells, since the window only matters to the fixed point. The nearest wrong cells sit 10.0% below
  (one error: account mail scaled with orders) and 12.3% above (one error: no type split).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The contract says attempts count and states the retry schedule. No document gives a provider's ceiling or says that
   retries land in already-full hours.
2. **No sweepable corpus nominates it.** *In every closed month the holiday and sale batches ran four hours, because doorbuster sends are
   new on this year's calendar.* So every month's retries reproduce exactly under its own constant rate. The ceilings appear only in the
   log's 41 over-ceiling provider-hours (last December's mornings at the strict provider, and a March reactivation blast at all four).
3. **No arithmetic symptom.** First attempts, retries and quota usage reconcile in every closed month, under every rate.
4. **Not a row predicate.** It needs provider-hour aggregation, a ceiling recovered from the absolute split, and a forward recursion in
   which each hour's deferrals feed later hours. The quota condition is then solved for the promotional volume.
5. **The enumeration is arithmetic.** Which attempts are retries next month is computed from the schedule. No column forecasts it.
6. **No cutover date.** The ceilings are constant across the log, and the doorbuster calendar is a planned shape, not an event in an outcome
   series.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The retry log: thirteen months of attempts by mailbox provider and hour, each with its stream, sending subdomain, deferral code
  and retry number.
* **What it pins.** The ceilings, absolutely. In every provider-hour, accepted volume equals the lesser of arrivals and the ceiling, with a
  0.3% background, and no hour accepts between 97% and 100% of its ceiling. It also pins the subdomain typing: order mail scaled by last
  December's order count (+45%) reproduces December's transactional attempts exactly, and a pooled scaling misses by 1.1M.
* **What it is blind to.** A two-hour batch (above).
* **Twin pair.** Two December Tuesdays at the strict provider are identical on every daily column: 0.70M promotional, 0.12M transactional,
  the same campaign type. Their retries are 61k and 122k (2.0×). One day's batch went through a send-time test that compressed it into a
  single hour, and only the hourly ceiling model reproduces both.
* **Every rule exercised.** March's blast crossed all four ceilings, and one December morning had transactional mail alone near the ceiling,
  which tests the priority rule.
* **Resemblance points at the decoy.** This December's month totals look most like last December's, whose 4.5% is the rate a lookup would
  carry.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The contract: every send attempt, retries included, counts against the 60M monthly quota, and sending stops at the quota.
  The contract's delivery schedule: retries at one, four and twelve hours, then the message is dropped. The platform policy: transactional
  mail is delivered first. One sentence each.
* **Empirical pins.** The provider ceilings and the subdomain typing, from the log.
* **Voices.** The CRM lead: "Last December is the right guide; same season, same customers." The merchandising director: "Every email we
  don't commit is revenue we can't book." The deliverability engineer: "Retries are noise, under one per cent."
* **Licensed wrong basis.** The planning manual records that the finance review checks send commitments against the prior year's same-month
  retry rate and will see that basis.

## 8. Determinism by construction

* **Ceilings.** The absolute split leaves no hour between 97% and 100% of a ceiling, so ceiling estimates converge across fitting
  conventions.
* **Hours.** Batches start on the hour, and the contract's retry offsets are whole hours, so the recursion has no sub-hour fork.
* **Priority and drops.** Both are filed. A message deferred four times is dropped, and drops count as attempts already made.
* **Solve.** Attempts rise monotonically with promotional volume, so bisection to 0.1M is unique.

## 9. Prompt sketch and deliverables

> Merchandising books revenue against the promotional email volume I commit on the 25th, and the email service stops sending the moment we
> hit our 60 million quota. Our CRM lead is confident last December is a safe guide. Tell me how many promotional emails we can commit to
> next month, in millions to one decimal, as one line for the calendar. Send `send_commit.xlsx`, a chart `hourly_load.png`, and a one-page
> `commit_note.pdf`.

* `send_commit.xlsx` — the commitment build, the unsubscribe sheet (ask A), the attribution sheet (ask B) and the log sheet (ask C).
* `hourly_load.png` — one holiday-week day at the strict provider: first attempts and retries due as stacked bars by hour, the ceiling as a
  labelled reference line, deferrals cascading from 08:00 annotated, and last December's matching day as a ghost series.
* `commit_note.pdf` — the committed figure, and why last December's rate does not carry.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of six customer value tiers, last quarter's unsubscribe and complaint rates per 1,000
  promotional emails delivered. *Device:* one-click unsubscribes and complaints arrive through providers' feedback loops keyed by envelope
  ID, which the envelope map resolves to customers. Dropping unmapped events understates the two tiers most active at the strict provider by
  a third.
* **Ask B (device-carried).** For each week of last quarter, promotional revenue per 1,000 delivered under 7-day click attribution.
  *Device:* app orders after an email click carry the tracking parameter only through a deep link, and the session-stitch table links the
  rest by device. Skipping it understates mobile-heavy weeks by 15–20%.
* **Ask C (validity).** The four provider ceilings, last December's retries under the constant-rate and ceiling models, and the commitment
  under each rung.
* **Decoupling.** Clearing the hourly fixed point changes no figure in asks A or B. Feedback events and app sessions never enter quota
  arithmetic.

## 11. Rubric arithmetic

6 tiers × 2 rates (ask A) + 13 weeks (ask B) + 4 ceilings + 2 December reproductions + 4 rung commitments (ask C) + the committed figure,
next month's total retries and the binding provider-hours + 5 named chart parts + 3 files ≈ 52 criteria.

## 12. World-building constraints

* Ceilings (per hour): 300k, 100k, 75k, 65k, for providers holding 46%, 27%, 15% and 12% of recipients. Background deferral 0.3%.
* November: 48.0M first attempts, retry rate 0.30%. Last December: 54.4M first attempts with four-hour holiday batches, 56.8M attempts, rate
  4.5%. December plan: order mail 12.0M, account mail 8.5M, 40% of promotional volume in the holiday week at 08:00–10:00.
* Answer 29.7M promotional, so 50.2M first attempts and 9.8M retries, with 56 provider-hours over ceiling on first attempts alone. Rung
  figures 43.9 / 39.4 / 37.8. Partials 35.1, 33.3 and 26.7.
* The twin days are identical on every daily column. Feedback-loop events and app sessions never touch attempts, retries or ceilings.

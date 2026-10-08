# FC08 — How many agent-hours to book for next quarter's deposit campaign, when a client is finished only once every callable number is

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Economics · retail banking operations |
| Mirrors | Booking outreach capacity when the work in a case is set by every reachable channel rather than the channels on file (Amazon customer-service callback queues, Uber driver re-activation across phone, SMS and email, account-verification outreach at Meta and Google) |
| Decision shape | One figure committed at a date: the agent-hours booked with the outsourced contact centre at the booking deadline |
| Committed call | Agent-hours for next quarter's maturity campaign (18,400 clients), to the nearest 100, booked take-or-pay by the deadline |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · S1, the unit that closes a case is a minimum over sub-units the file does not count, with Pattern B for the closing rule |
| Gate G mechanism | method_or_model_selection, with forecasting support |
| Measured traps engaged | #18 joins only on the visible key · #3 stops at a close but inexact match · #13 validates on one population, applies to another |
| Calibration form | Counterparty acknowledgement file: the vendor's case acknowledgements for last campaign, with every attempt, the number dialled, the outcome and each case's closure |
| Driving force | A case closes on a contact or when every callable number has had six unanswered attempts. Last campaign's young list had almost no uncallable numbers, so "six per number on file" fitted 97.5% of closures. Next quarter's list is the maturity segment: three numbers on file for 75% of clients, but 22% of the list's numbers are carrier-dead or on the do-not-call register and are never dialled. Callable count lives behind two number-level joins and is in no column, and work per client follows it, not the count on file. |

## 1. Situation

A retail bank's term-deposit campaigns are dialled by an outsourced contact centre that the bank books in agent-hours, take-or-pay, a
quarter ahead. Next quarter's list is fixed: 18,400 clients whose deposits mature, selected by the filed score cut-off. The vendor
contract fixes handling times (1.5 minutes per unanswered attempt, 8 minutes per contact) and says each case is worked until a contact or
until it is exhausted under the vendor's standard dialling rules. The rules themselves are not in the contract.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the vendor's acknowledgement file, the list files, the CRM's phone numbers, the do-not-call
  register, the carrier validation file and the contract. No one's claim about their own numbers is overturned. The difficulty is what a
  unit of work is on a list that does not look like the last one.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and procurement's sizing. Per-number work rates from last campaign, applied to next quarter's
  numbers on file, are still the careful build, and still 20% high.
* **Instrument repair.** Log every attempt perfectly; they already are. Next quarter's numbers have not been dialled, and which of them
  will be is a property of numbers no past attempt touched.
* **Lens swap.** The naive read and the answer are different populations: last quarter's young clients, whose numbers on file were
  callable, against a maturity list whose numbers on file mostly are not.

## 3. The driving force

A strong solver links every attempt to its client, then sees that work per client rises with the numbers a client has. It fits a
per-number law: six unanswered attempts on each number, then the case closes. That law reproduces 97.5% of last campaign's closures, and the
2.5% it misses look like vendor noise. They are clients with a number the vendor never dialled: carrier-dead or registered on the
do-not-call list. The closing rule is a minimum over callable numbers. A case is exhausted when each callable number has six unanswered
attempts, and uncallable numbers do not count. Last campaign hardly exercised the distinction. Next quarter does: 75% of the maturity list
has three numbers on file, but only 35% has three callable. Callable status needs each number joined to the register snapshot and to the
carrier file, then a count per client, and work follows that count.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Last campaign's hours per client, attempts joined to clients on the list file's case ID, × 18,400 | 2,940 h, −41% | The vendor's own record of work, per client, scaled to the new list | **E20 (an implicit join):** the vendor's carry-forward table, which its practice note documents; 30% of clients were worked under their wave-one case IDs |
| 1 | The same with carry-forward cases linked | 4,200 h, −16% | Every attempt now belongs to a client, and hours tie to the vendor's invoice | The acknowledgement file: attempts to closure rise with a client's numbers, and the new list has far more numbers per client |
| 2 | Work per client by numbers on file (six unanswered attempts per number), at next quarter's on-file mix | 6,000 h, +20% | A closing law that reproduces 97.5% of closures, applied to the list's actual structure | The do-not-call register and the carrier file: every miss is a client with an undialled number, and 22% of the new list's numbers are undialable |
| 3 | **Decisive:** closure when every callable number has six unanswered attempts; callable count per client from both number-level joins; expected work at next quarter's callable mix | **5,021 h → 5,000** | — | — |

* **Figure shape.** Two corrections walk the figure up (−41%, −16%), the per-number law overshoots (+20%), and the decisive rung brings it
  back. A solver who stops short is wrong in a known direction at each rung.
* **Partial correction priced (L3).** A solver who learns that undialled numbers matter but keeps the minimum over numbers on file finds
  that those clients can never be exhausted. Run to the 21-day campaign window, they lift the figure to 6,600 hours (+31%), further away
  than rung 2.
* **Grid.** Link (explicit key, carry-forward) × closing law (per client, per number on file, per callable number) gives 6 cells: −41%,
  −16%, +20%, −16%, −30% and the answer. The nearest wrong cells sit 16% away, each one omission from the answer.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The contract says "exhausted under the vendor's standard dialling rules". The practice note covers case IDs, not
   closing. No document says uncallable numbers are skipped or how exhaustion is counted.
2. **The reproduction numbers.** The callable minimum reproduces 22,000 of 22,000 closures (contacted at the logged attempt, or exhausted
   at exactly six per callable number). Six per number on file reproduces 21,450 (97.5%), and every miss is a client it predicts never
   closes. Any single total-attempts threshold reproduces at most 59% of exhaustions. The rule is a construction: a count per client of
   numbers that pass two joins, then a minimum. It is not a setting a sweep finds.
3. **No arithmetic symptom.** Once carry-forward cases are linked, attempts tie to the invoice, contacts to the deposit system and
   numbers to the CRM under every rung.
4. **Not a row predicate.** Callable status is a property of a phone number (two joins), the closing rule is a minimum over a client's
   callable numbers, and the forward work is an expectation over that count.
5. **The enumeration is arithmetic.** Which clients close at six, twelve or eighteen attempts is computed. No column holds callable
   counts.
6. **No cutover date.** Nothing changed between the campaigns except the list, and the list is a different segment, not a later one.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The vendor's acknowledgement file for last campaign: 22,000 cases, every attempt with the number dialled, timestamp and
  outcome, and each case's closure (contacted or exhausted).
* **What it pins (Pattern B).** The closing rule (above), and the contact rate per attempt by number type: 9% on mobiles and 4% on
  landlines, stable across the campaign's weeks.
* **Twin pair.** Clients C-44017 and C-58210 are identical on every CRM column: three numbers on file, age band, segment, score band and
  region. They were exhausted after 12 and 6 attempts (2.0×), because C-58210's landline is carrier-dead and its work number is on the
  register. Only the callable minimum reproduces both.
* **Resemblance points at the decoy.** Next quarter's clients resemble last campaign's three-number clients on every CRM column. Those
  clients took the most work, because their numbers were callable.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The contract: handling times of 1.5 and 8 minutes, cases worked until contact or exhaustion, a 21-day campaign window
  and one attempt per number per day. The list file: next quarter's 18,400 clients. The practice note: clients carried between waves keep
  their first case ID in the carry-forward table.
* **Empirical pins.** The closing rule and the contact rates, from the acknowledgement file. Callable status, from the register snapshot
  dated the week before the campaign and the carrier validation run on the list.
* **Voices.** The contact-centre manager: "List size drives the booking; every client is about the same work." The vendor's account lead:
  "Older clients have more numbers on file, so they take more dialling."
* **Licensed wrong basis.** The booking procedure records that procurement sizes bookings on the vendor's quoted hours per thousand list
  records and will present that sizing at the approval meeting.

## 8. Determinism by construction

* **Threshold.** Six attempts per callable number is unique: five or seven reproduce no exhaustion in the file.
* **Window.** At most three callable numbers per client, one attempt per number per day, so every case closes inside 21 days and no
  forward case is cut off by the window.
* **Snapshots.** The register snapshot and the carrier run both predate the campaign and are the vendor's own pre-dial inputs, so no
  number's status changes mid-campaign.
* **Expectation.** Contact rates are fixed by number type, and the first callable number dialled is the mobile where one exists, as the
  file shows for every case.
* **Rounding.** The unrounded 5,021 hours rounds to 5,000, with the nearest wrong cell more than 800 hours away.

## 9. Prompt sketch and deliverables

> Bookings with our contact centre close on Friday, and whatever I book is paid for, so I need one figure: the agent-hours for next
> quarter's maturity campaign, to the nearest hundred. Our contact-centre manager thinks list size is all that matters. Send me
> `campaign_booking.xlsx`, a chart `case_work_by_callable.png`, and a one-page `booking_note.pdf` that commits to the hours.

* `campaign_booking.xlsx` — the hours build by client structure, the funding sheet (ask A) and the handling-time sheet (ask B).
* `case_work_by_callable.png` — attempts to closure by callable-number count in last campaign (bars with the 6/12/18 steps marked),
  next quarter's on-file and callable mixes as paired bars, the booked hours as a labelled line, and the twin clients annotated.
* `booking_note.pdf` — the committed hours, forward attempts and contacts, and the sizing procurement will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 regions, the share of last campaign's subscriptions funded within 10 days and
  the median funded amount. *Device:* a deposit funded by two transfers posts two credit rows under one deposit ID, as the deposit
  system's dictionary documents. Per-row figures understate the median in every region and misdate completion for a fifth of deposits.
* **Ask B (device-carried).** For each of the vendor's 9 agent teams, the mean handling time per contact and per unanswered attempt last
  campaign. *Device:* after-call work is logged as a separate wrap-up record carrying the call's ID, and the vendor's time standard counts
  it. Talk time alone understates contact handling by about a quarter in every team. The booking uses the contract's filed times.
* **Ask C (validity).** Hours under each of the four rung constructions, with each construction's reproduction of the 22,000 closures.
* **Decoupling.** Replacing callable counts with on-file counts changes no figure in asks A or B.

## 11. Rubric arithmetic

12 regions × 2 (ask A) + 9 teams × 2 (ask B) + 4 constructions × 2 (ask C) + the committed hours, forward attempts and forward contacts
+ 5 named chart parts + 3 files ≈ 61 criteria.

## 12. World-building constraints

* Last campaign: 22,000 clients; on-file mix 50/35/15% (one/two/three numbers), callable mix 51.5/34.5/14%. 30% of clients carried
  forward under wave-one IDs.
* Next quarter: 18,400 clients; on-file mix 5/20/75%, callable mix 25/40/35%.
* Contact rate per attempt 9% (mobile) and 4% (landline); the first number dialled is the mobile.
* Rung figures 2,940 / 4,200 / 6,000 / 5,021 hours; the capped on-file-minimum cell is 6,600. No non-answer cell is within 16%.
* Split funding transfers and wrap-up records never touch attempts, numbers or the register.

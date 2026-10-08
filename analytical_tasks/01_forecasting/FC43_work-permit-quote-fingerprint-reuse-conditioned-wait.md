# FC43 — What wait to quote next quarter's work-permit renewals, when a case's speed depends on whether USCIS still holds the filer's fingerprints and next quarter's filers mostly do not

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Policy & Education · public case-processing administration (employer immigration and mobility planning) |
| Mirrors | Quoting service times when a queue's speed depends on a hidden prerequisite carried over from earlier cases (tech-industry work-permit and visa planning, marketplace seller verification that reuses an earlier identity check, enterprise access reviews that reuse a prior approval) |
| Decision shape | One figure committed at a date: the wait quoted in the benefits portal for renewals filed from January to March |
| Committed call | The wait within which four in five of next quarter's filers will have their decision, to the nearest half month |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · Pattern E (conditioned yield, S8: decisions split absolutely on whether USCIS holds fingerprints from the previous 15 months), with a past statement read as a forward one (E08) at rung 2 |
| Gate G mechanism | forecasting, with decomposition_attribution |
| Measured traps engaged | #13 validates on one population, applies to another · #6 treats a mixed segment all one way · #7 uses the ready-made measure |
| Calibration form | Existing-book actuals: every work-permit case the company has filed since January 2024, with receipt and decision dates, joined to the immigration case register's appointment notices |
| Driving force | A case's wait splits absolutely on whether USCIS already holds the filer's fingerprints from the previous 15 months, across all of that person's cases: with them, decisions come in 2.6–3.4 months; without, the filer waits for a new appointment and decisions take 5.9–6.9. In the book four in five cases had recent fingerprints, because every renewal was of a one-year card filed within a year of its last appointment. Next quarter's filers are mostly spouses renewing the two-year cards issued in early 2025, whose fingerprints are over two years old, so the book's renewals, its fastest group and its busiest office all point the wrong way. |

## 1. Situation

A technology company's mobility team files work-permit renewals for employees on student extensions and for the spouses of sponsored
employees. It quotes each filer a wait in the benefits portal, and people plan leave, travel and job starts on it. The mobility policy
quotes the wait within which four in five of a quarter's filers will have their decision. About 900 renewals fall due from January to
March. The pack holds the company's case book since January 2024, the immigration case register with every receipt and appointment
notice, the dependants table, USCIS's quarterly receipts, completions and pending counts for the form, the posted USCIS processing time
and the team's dashboard. The quote goes live on 15 December.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: receipts, decisions, appointment notices, USCIS's quarterly counts, the posted processing time and
  the dashboard. No stakeholder's reading of their own numbers is overturned; renewals really were the company's fastest cases. The
  difficulty is that the speed belonged to a property the past renewals happened to share and next quarter's mostly lack.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of mobility's view and every voice. The book's renewals are still the obvious reference for a
  quarter of renewals, and their 80th percentile, shifted for the growing queue, still lands at 5.0 months.
* **Instrument repair.** Imagine USCIS publishing every case's appointment and decision dates. The past would be clearer, but which of
  next quarter's filers need a new appointment is still decided by each person's own appointment history, joined across their cases.
* **Lens swap.** The naive read and the answer weigh different populations: renewals whose fingerprints were a year old, against renewals
  whose fingerprints are two years old, which the book's renewals never included.

## 3. The driving force

A strong solver starts from the team's own record rather than the national posting, measures each case from the receipt USCIS accepted,
shifts the distribution by the growth in the queue ahead (USCIS's pending count for the form is up 52% on flat completions), and
conditions on the visible fact that next quarter's filers are all renewals. The book's renewals were its fastest cases, so the quote
comes out at 5.0 months. Every step is correct. But the book's waits split on something no column names: whether USCIS already held
fingerprints taken in the 15 months before filing, from any of the person's cases, including a spouse's extension of stay. With them, a
case went straight to adjudication; without them, it waited for a new appointment. Every renewal in the book was of a one-year card, so
its fingerprints were recent. Next quarter 630 of the 900 filers renew two-year cards issued in early 2025 on fingerprints taken in late
2024. Joined to the register and mixed at next quarter's proportions, with the queue shift applied to both groups, four in five decisions
arrive within 8.0 months.

## 4. The ladder

| Rung | Construction | Lands on (months, to the half month) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The team's dashboard: 80th-percentile wait of the book's decided cases, measured from first receipt | 4.5 (−44%) | The company's own record, not the national posting | The case register: 6% of cases carry a rejected first receipt (fee or signature) and an accepted refiling, and USCIS's clock starts at the accepted one |
| 1 | Hygiene: every case measured from its accepted receipt | 3.5 (−56%) | Clean, reconciled to the register, and it matches the posted national time | USCIS's quarterly counts: pending for the form is up 52% on flat completions, and the dashboard is labelled as a statement about cases decided in the last twelve months |
| 2 | The book's renewals, shifted by the growth in the wait ahead (pending ÷ completion rate, 2.9 to 4.4 months) | 5.0 (−37.5%) | Forward-looking, and conditioned on the visible fact that next quarter's filers are renewals | The case register's appointment notices: every case decided in under 3.5 months had fingerprints from the previous 15 months on file, every slower case attended a new appointment, and 630 of next quarter's 900 filers last gave fingerprints in late 2024 |
| 3 | **Decisive:** each filer classed by the latest appointment across all their cases as of filing, the book's two absolute groups shifted by the queue and mixed at next quarter's 270 / 630 | **8.0** | — | — |

* **Figure shape.** The rungs move 4.5, 3.5, 5.0 and the decisive rung lands at 8.0, the extreme cell: no other construction comes within
  18% of it, and every one sits below it, so a solver who stops anywhere short under-quotes.
* **Partial correction priced (L3).** A solver who finds the fingerprint split but weights it at the book's own mix (83 / 17) lands at
  5.0 (−37.5%), because the 80th percentile stays inside the fast group. One who conditions on the visible card length instead finds no
  two-year renewal in the book to learn from and also lands at 5.0. One who classes and mixes correctly but leaves out the queue shift
  lands at 6.5 (−19%).
* **Grid.** Receipt basis (first, accepted) × queue (as posted, shifted) × grouping (pooled, by type, by fingerprints at the book's mix,
  by fingerprints at next quarter's mix) = 16 cells. Only the two cells with next quarter's mix and the queue shift reach 8.0 (the receipt
  basis does not move it, because every refiled case had recent fingerprints); the nearest wrong cell is 6.5, 19% below.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** USCIS's posting and quarterly counts say nothing about fingerprints; the register files appointment notices as
   correspondence. No document says a recent appointment is reused or how old is too old.
2. **Corpus blind to the mix.** *In every closed quarter about four in five of the company's filers held fingerprints from the previous
   15 months, because every renewal in the book was of a one-year card filed within a year of its last appointment; so the pooled, by-type
   and by-office distributions reproduced each quarter's 80th percentile within 0.2 months.* The book certifies the visible grouping
   exactly where it cannot fail.
3. **No arithmetic symptom.** Receipts, decisions and notices reconcile; USCIS's counts satisfy the stock-flow identity; every rung's
   figure is internally consistent.
4. **Not a row predicate.** Whether USCIS holds a filer's fingerprints depends on the latest appointment across all of that person's cases
   (their own permits, extensions of stay and residence applications), linked by A-number through the dependants table, as of the filing
   date: an as-of join across case types before any count.
5. **The enumeration is arithmetic.** No column says "fingerprints on file"; each filer's status is computed from dated notices.
6. **No cutover date.** No outcome series steps; the two-year cards simply reach renewal for the first time next quarter.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The company's case book since January 2024 (2,600 cases with receipt and decision dates), the immigration case register's
  appointment notices across every case type, and USCIS's quarterly counts for the form.
* **What it certifies.** The hygiene rule (USCIS's clock starts at the accepted receipt) and the queue shift: a case's wait moved with
  pending ÷ completion rate in every closed quarter.
* **What it pins.** The absolute split: decisions in 2.6–3.4 months for every case with fingerprints at most 14 months old, 5.9–6.9 for
  every case with fingerprints at least 16 months old, and no case in between.
* **Twin pair.** Two spouse renewals filed from Seattle in March 2026 are identical on every case-table column: category, office, filing
  month, card length and type. They were decided in 3.0 and 6.4 months (2.1× apart), because one filer's last appointment was 11 months
  before filing and the other's, after a slow previous case, 17 months. Type, office and card length predict them equal; only the
  appointment join separates them.
* **Resemblance points at the decoy.** By category, office and type, next quarter's filers most resemble the book's renewals, its fastest
  group, and Seattle, which files most of next quarter's cases, had the fastest record in the company.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The mobility policy: the quote is the wait within which four in five of the quarter's filers will have their decision,
  rounded to the half month. USCIS's quarterly counts for the form. The renewal calendar: who files next quarter and when.
* **Empirical pins.** The two groups' wait ranges and the 15-month line, from the book joined to the register. The queue shift, from
  USCIS's pending and completions.
* **Voices.** The head of mobility: "Renewals are the easy ones; they always come back in about three months." Immigration counsel:
  "The posted USCIS time is the only number we can defend to employees." The Seattle HR partner: "Seattle's cases have always been the
  fastest in the company."
* **Licensed wrong basis.** The mobility policy records that the employee-relations team benchmarks every quote against the posted USCIS
  processing time and will compare the team's quote with it.

## 8. Determinism by construction

* **The 15-month line.** No case in the book and no filer next quarter has fingerprints between 14 and 16 months old, so the line's
  exact placement moves nobody.
* **Queue shift.** Pending ÷ completion rate computed monthly or quarterly gives 1.5 months ± 0.05, and the shift applies alike to both
  groups because both wait in the same adjudication queue.
* **Maturity.** Every case received before January 2026 is decided; the two groups' ranges are read from those, and the 2026 cases still
  open sit inside the same ranges at their current age.
* **Filing dates.** The renewal calendar files each case 120 days before card expiry, so every filer's as-of date is fixed.
* **Rounding.** The mix gives 8.11 months, inside the 8.0 bin and clear of both edges; percentile conventions move it by under 0.02.

## 9. Prompt sketch and deliverables

> Next quarter about 900 of our people and their spouses file work-permit renewals, and they will plan leave, travel and job starts
> around what we tell them. Our head of mobility says renewals are the easy ones and always come back in about three months. Give me the
> wait to quote, to the nearest half month, in one sentence for the benefits portal, and send `quote_build.xlsx` with the build and the
> sheets below, a chart `wait_split.png`, and a one-page `quote_note.docx`.

* `quote_build.xlsx` — the quote under each construction, next quarter's filers by fingerprint status and office, the relocation sheet
  (ask A) and the leavers sheet (ask B).
* `wait_split.png` — the book's waits as a strip plot in two bands (fingerprints on file, new appointment) with the empty gap between them
  shaded, next quarter's filers as a stacked bar beside it, the posted USCIS time and the queue-shifted line marked, and the 8.0-month
  quote annotated.
* `quote_note.docx` — the quote, why renewals are not fast this time, and which filers to warn first.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six offices and each month of last quarter, the median days from offer acceptance
  to start date for relocating hires. *Device:* a start date the hire defers is written as a new entry in the onboarding changes table,
  while the hire table keeps the original date, as the HR data guide documents; reading the hire table understates relocation time in
  four offices. Relocations enter no part of the quote.
* **Ask B (device-carried).** For each office and each quarter of last year, the sponsored employees who left the company. *Device:* an
  employee who resigns and is rehired within 90 days keeps the same ID, with the rehire in the employment-events table, as the HR data
  guide documents; counting termination records alone counts them as leavers. No leaver or rehire is among next quarter's filers.
* **Ask C (validity).** The quote under each of the four rung constructions, and next quarter's filers by office split by fingerprint
  status.
* **Decoupling.** Clearing the fingerprint classification changes no figure in asks A or B.

## 11. Rubric arithmetic

6 offices × 3 months (ask A) + 6 offices × 4 quarters (ask B) + 4 constructions + 6 offices × 2 (ask C) + the committed quote and the
630 filers needing appointments + 5 named chart parts + 3 files ≈ 68 criteria.

## 12. World-building constraints

* Book: 2,600 cases; fingerprints at most 14 months old decide in 2.6–3.4 months, at least 16 months in 5.9–6.9; 83% / 17% overall;
  6% refiled after a rejected first receipt, all with recent fingerprints, each 1.5 months longer from first receipt.
* USCIS: pending ÷ completion rate rises from 2.9 to 4.4 months (pending +52%, completions flat).
* Next quarter: 900 renewals; 630 last gave fingerprints in late 2024; 270 have fingerprints from the previous 15 months (one-year cards,
  and spouses with an extension-of-stay appointment this autumn).
* Quotes by rung: 4.5 / 3.5 / 5.0 / 8.0 (8.11 unrounded); without the queue shift 6.5; at the book's mix 5.0.
* The twin renewals are identical on every case-table column; 3.0 and 6.4 months.
* Onboarding changes and rehires touch no case, notice or USCIS count used in the quote.

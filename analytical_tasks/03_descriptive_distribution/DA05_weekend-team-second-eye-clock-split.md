# DA05 — Which specialty gets the weekend day-surgery team, when half the longest-looking cataract waits are second eyes on a new clock

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · health-system administration and elective waiting lists |
| Mirrors | Sending one surge team to the queue with the most SLA breaches when part of that queue's age is an inherited start date rather than a running clock (support follow-ups logged under the original ticket's open date at Apple and Amazon, the second unit on a warranty claim aged from the first, app-review resubmissions aged from first submission) |
| Decision shape | Which of N gets one scarce thing: 26 weeks of weekend day-surgery lists for one of six specialties |
| Committed call | The specialty, and the 52-week waits the team prevents there by 31 March 2027 |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · E29, a uniformly labelled segment split by a clause through a join (second-eye listings), with E16 (finer controls in the settled ledger) below it and a ledger blind to the split (L1) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #6 treats a mixed segment all one way · #12 stops at the first control that passes · #5 takes the population a flag or filter suggests · #15 follows the requester's hunch over the rule |
| Calibration form | Settled-transaction ledger: the commissioner's 24 months of settled elective episodes at the trust and its partner site, with pathway, procedure, site and dates |
| Driving force | Ophthalmology's at-risk list is more than half second-eye cataract listings, and every row carries the original referral date as its wait start. The access policy's clock annex starts a second procedure's clock when the first is done, and the first eye's date sits only in the treatment history, found by grouping each patient's procedures by family and ordering them by date. Re-clocked, 60% of Ophthalmology's apparent 52-week risk is months short of 52 weeks, and the team prevents the most waits in Urology. |

## 1. Situation

A hospital trust has funding for one surgical team to run weekend lists in its day-surgery unit for 26 weeks from October. The
elective recovery plan sends the team to the specialty in which it prevents the most 52-week waits by 31 March 2027. The unit's weekend
template gives 640 day-case slots over the period. The candidates are Orthopaedics, General Surgery, Ophthalmology, Urology,
Gynaecology and ENT. The pack holds the waiting-list snapshot for 30 September 2026, the PAS theatre log, the commissioner's settled
ledger, the treatment history, the access policy with its clock annex, the national waiting-time returns for the closed year and the
unit's operating documents. The board decides on 15 October.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the snapshot's referral dates, the theatre log, the settled ledger and the returns. Nobody's
  reading of their own numbers is overturned, and Ophthalmology's long list is real. The difficulty is which of its patients are
  actually near 52 weeks on the clock the plan scores.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the COO's and the clinical director's views and the commissioner's licensed basis. The snapshot still
  gives every patient a referral date and a procedure, and projecting waits from it is still the competent first build.
* **Instrument repair.** Make the snapshot and the ledger perfect; they already are. A second-eye listing's clock is set by an event on
  another record, the first eye's treatment, so no better list instrument carries it.
* **Lens swap.** The two reads cover different populations: 470 Ophthalmology day cases that look at risk on weeks since referral,
  against the 188 of them whose clock, started at referral or at the first eye, actually reaches 52 weeks by 31 March.

## 3. The driving force

A strong solver projects each specialty's list forward: patients reach 52 weeks in clock order unless existing lists treat them first.
It measures existing throughput from the settled ledger at both sites, checks the projection against the closed year's per-specialty
waits, keeps only patients the weekend unit can take as day cases, and caps at the 640 slots. That puts Ophthalmology first by 1.49×,
which matches the clinical director's belief and the length of the cataract list. But the list dates every row from its referral. A
patient listed for the second eye after the first was done has the original referral on the row, often 50 to 70 weeks old. The clock
annex says a second procedure on a paired organ starts its own clock when the first is done. The first eye's date is not on the list.
It sits in the treatment history, reached by grouping each patient's procedures by family and ordering them by date. Re-clocked,
Ophthalmology keeps 40% of its apparent risk, and Urology, with almost no staged procedures, leads by 1.46×.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Projection with the PAS theatre log as existing throughput, all intended managements, capped at 640 slots | A, Orthopaedics (640, 1.23× General Surgery) | The trust's own throughput log; the projection reproduces the closed year's trust-wide breach count within 1% | The ledger's per-specialty breach and wait-at-treatment controls: the theatre log misses partner-site joints and counts endoscopy surveillance as throughput |
| 1 | Existing throughput from settled RTT treatments at both sites, linked to list pathways (E16) | B, General Surgery (640, 1.36× Ophthalmology) | Reproduces all six specialties' closed-year breach counts and median waits at treatment | The unit's operating document: weekend lists are day cases, and 73% of General Surgery's at-risk patients are listed as inpatients |
| 2 | Same, keeping only patients listed as day cases | C, Ophthalmology (470, 1.49× Urology) | The team's real casemix, cleanly applied | The clock annex, read through the treatment history: 60% of Ophthalmology's at-risk day cases are second-eye listings on a clock that started at the first eye |
| 3 | **Decisive:** second-procedure clocks re-started at the first procedure's treatment, found by patient × procedure family in the treatment history | **D, Urology (309, 1.46× Gynaecology)** (5th of 6 on rung 0) | — | — |

* **Position table.** Urology ranks 5th on rung 0, 4th on rung 1 and 2nd on rung 2 (1.49× behind Ophthalmology), and leads only rung 3.
  Each rung's leader beats its runner-up by at least 1.23×.
* **Discriminator dominance.** Ophthalmology carries 1.49× (470 against 315) into rung 3. On the decisive axis, the share of apparent
  risk that survives re-clocking, Urology keeps 0.98 and Ophthalmology 0.40, an edge of 2.45×. That is 1.37 times the required
  1.2 × 1.49 = 1.79. The final margin over Ophthalmology is 309 against 188 (1.64×).
* **Partial correction priced (L3).** A solver who re-clocks only second eyes whose first eye was done at the trust's own site misses the
  partner site, where two-thirds of the first eyes were done. Ophthalmology then keeps 374 (0.80 of its risk) and still leads Urology by
  1.21×: the half insight names the decoy. A solver who re-clocks but keeps the theatre-log throughput names Orthopaedics (472 against
  Urology's 304, 1.55×).
* **Grid.** Throughput (theatre log or ledger) × casemix (all or day case) × clocks (referral or re-started) gives 8 cells. Every
  non-answer cell names Orthopaedics, General Surgery or Ophthalmology, and only the ledger, day cases and re-started clocks together name
  Urology.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The clock annex states a general rule for paired organs among a dozen clock rules. Nothing says the snapshot's
   referral date is not the clock, and the list carries no laterality, sequence or "second procedure" field.
2. **Corpus blind for a computable reason.** *In every settled cataract episode of the closed 24 months, the wait since referral and the
   wait since the first eye fell on the same side of 52 weeks (none over 49 weeks on either clock), because the second-eye queue only
   lengthened past 30 weeks this year.* The ledger's back-tested breach counts are therefore identical under both clocks, and it certifies
   rung 2 exactly.
3. **No arithmetic symptom.** Snapshot counts tie to the national return, ledger episodes tie to the commissioner's payments, and every
   pathway on the list resolves.
4. **Not a row predicate.** A second-eye listing is found by grouping a patient's treatment history by procedure family, ranking by
   date and comparing to the listing date, then re-clocking from the first treatment. No list column flags it.
5. **The enumeration is arithmetic.** 282 of 470 at-risk Ophthalmology day cases are re-clocked by the join alone, and 6 Urology
   listings (staged ureteroscopies) by the same rule.
6. **No cutover date.** The second-eye queue lengthened gradually, the clock annex dates from years earlier, and no breach series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the snapshot still invites weeks since referral.

## 6. The calibration corpus

* **Form.** The commissioner's settled ledger: 24 months of paid elective episodes at the trust and its partner site, each with pathway
  ID, specialty, procedure, site and admission and discharge dates. The national returns supply the closed year's per-specialty 52-week
  breaches and median waits at treatment.
* **What it certifies (E16).** Existing throughput. The salient control, the closed year's trust-wide breach count (1,412), is reproduced
  within 1% by both the theatre-log and the ledger projections, because Orthopaedics' over-projection and General Surgery's
  under-projection offset. The twelve finer controls (per-specialty breach counts and median waits at treatment) pass only the ledger's
  pathway-linked treatments at both sites. The theatre log misses Orthopaedics' breaches by +47% and General Surgery's by −35%.
* **What it is blind to.** The second-procedure clock (above).
* **Twin pair.** Patients 7731 and 7748 on the Ophthalmology list are identical on every snapshot column: referral date (58 weeks
  before the snapshot), listing date, procedure, priority, age band and site. Their clocks stand at 58 and 29 weeks (2.0×), because
  7748's first eye was treated 29 weeks ago at the partner site. One breaches before 31 March and the other does not, and only the
  treatment history separates them.
* **Resemblance points at the decoy.** This year's Ophthalmology list most resembles last year's by size and age profile, and in last
  year's list every at-risk cataract patient was a first-eye listing.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The elective recovery plan: "The weekend team goes to the specialty in which it prevents the most 52-week waits by
  31 March 2027." The unit's operating document: "Weekend lists take day cases only, 640 slots across the 26 weeks." The access policy:
  "Patients are treated in clock order within clinical priority." The clock annex, among its rules: "A second procedure on a paired organ,
  listed after the first is done, starts its own clock at the first procedure."
* **Empirical pins.** Existing throughput comes from the ledger's per-specialty controls.
* **Voices.** The chief operating officer: "Our 52-week risk sits in orthopaedics; it always has." The ophthalmology clinical director:
  "Cataracts are where the long waits are. Give us the weekends and we'll fill every list."
* **Licensed wrong basis.** The plan records that the commissioner monitors 52-week risk on weeks since referral and will review the
  allocation on that basis.

## 8. Determinism by construction

* **Horizon.** No at-risk patient's 52-week date falls within three days of 31 March, under either clock.
* **Throughput window.** The ledger's last 26, 39 and 52 weeks give the same weekly rates to within 2% for every specialty, so the
  projection picks the same patients.
* **Procedure families.** The treatment history codes procedures to the national classification's family level. Each second-eye
  listing has exactly one earlier same-family treatment, at least 6 weeks before listing.
* **Capacity.** Only the rung-0 and rung-1 leaders exceed 640 slots. At rung 3 every pool is under 640, so the cap decides nothing.

## 9. Prompt sketch and deliverables

> I have to tell the elective board on 15 October which specialty gets the weekend day-surgery team for the next 26 weeks. Our COO is
> sure the risk sits in orthopaedics. Name the specialty and the number of 52-week waits it will prevent by 31 March, as one sentence for
> the board paper, and send `weekend_team_case.xlsx` with the sheets below, plus `breach_runway.png`.

* `weekend_team_case.xlsx` — the projection, the six specialties under the four rung constructions (ask C), the cancer-referral sheet
  (ask A) and the cancellation sheet (ask B).
* `breach_runway.png` — for each specialty, at-risk day cases by the week they reach 52 weeks, as stacked bars split into first and
  second procedures; the 640-slot line; the chosen specialty marked; and the twin patients annotated.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six specialties, the share of urgent suspected-cancer referrals seen within 14
  days in each quarter of the last year. *Device:* a referral the consultant downgrades after triage leaves the urgent pathway on its
  downgrade date, posted as a separate event, as the cancer waiting-times guide documents. Counting downgraded referrals as urgent
  misstates 15 of the 24 quarterly shares.
* **Ask B (device-carried).** The day-surgery unit's same-day cancellations in the last year, per specialty, by reason (patient, clinical,
  hospital). *Device:* a patient moved to another list on the same day is logged as a cancellation plus a new booking, with a "moved"
  flag in the booking audit. Counting moves as hospital cancellations overstates them by 18% to 40%.
* **Ask C (validity).** Waits prevented for each specialty under each of the four rung constructions.
* **Decoupling.** The cancer pathway file and the booking audit share no row with the elective snapshot or the treatment history.
  Clearing the re-clocking changes no figure in asks A or B.

## 11. Rubric arithmetic

6 specialties × 4 quarters (ask A) + 6 × 3 reasons (ask B) + 6 specialties × 4 constructions (ask C) + the committed specialty, its
waits prevented and its margin + 4 named chart parts + 2 files ≈ 75 criteria.

## 12. World-building constraints

* Waits prevented by rung (Orthopaedics, General Surgery, Ophthalmology, Urology, Gynaecology, ENT): rung 0 640 (1,180 at risk) / 520 /
  450 / 345 / 360 / 280; rung 1 380 / 640 (760 at risk) / 470 / 350 / 320 / 285; rung 2 152 / 205 / 470 / 315 / 211 / 205; rung 3 152
  / 205 / 188 / 309 / 211 / 205.
* Day-case shares of at-risk patients: Orthopaedics 0.40, General Surgery 0.27, Ophthalmology 1.00, Urology 0.90, Gynaecology 0.66,
  ENT 0.72. Shares surviving re-clocking: Ophthalmology 0.40, Urology 0.98, all others 1.00.
* The theatre-log projection reproduces the closed year's trust-wide breach count within 1% and misses the per-specialty controls. The
  ledger projection reproduces all twelve.
* No settled cataract episode in the closed 24 months waited over 49 weeks on either clock. Patients 7731 and 7748 are identical on every
  snapshot column.
* The cancer pathway file and the booking audit touch no elective pathway.

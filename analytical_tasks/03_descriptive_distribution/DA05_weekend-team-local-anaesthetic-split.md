# DA05 — Which specialty gets the weekend day-surgery team, when no anaesthetist works weekends and the longest-looking cataract waits are second eyes

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · health-system administration and elective waiting lists |
| Mirrors | Sending one surge team to the queue with the most SLA breaches when the team can only work part of each queue (weekend support shifts that cannot take tickets needing a specialist's sign-off, weekend warehouse crews without licensed forklift drivers, app-review surge teams limited to non-sensitive categories), where every queue's backlog is real but the team's reach inside it differs |
| Decision shape | Which of N gets one scarce thing: 26 weeks of weekend day-surgery lists for one of six specialties |
| Committed call | The specialty, and the 52-week waits the team prevents there by 31 March 2027 |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · E29, each specialty's day-case list split by the absence of weekend anaesthetic cover through the pre-assessment record, with E16 (the ledger's per-procedure waits, which pin re-started clocks for second procedures) below it and a ledger blind to weekend lists (L1) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #6 treats a mixed segment all one way · #12 stops at the first control that passes · #10 notes a binding limit as a risk · #15 follows the requester's hunch over the rule |
| Calibration form | Settled-transaction ledger: the commissioner's 24 months of settled elective episodes at the trust and its partner site, with pathway, procedure, site and dates |
| Driving force | The weekend rota has a surgeon, scrub nurses and a recovery nurse, and no anaesthetist, so the team can treat only patients whose pre-assessment plans a local anaesthetic. Every list the trust keeps is labelled by specialty and day case, and every past list ran with an anaesthetist, so nothing in the ledger separates the two. Most of Urology's at-risk day cases are planned under general anaesthesia, frail men with bleeding risk, while seven in ten of Gynaecology's are hysteroscopies and loop excisions under local. Split on the pre-assessment record, Gynaecology prevents the most waits, after re-clocking second eyes has already moved the lead from Ophthalmology to Urology. |

## 1. Situation

A hospital trust has funding for one surgical team to run weekend lists in its day-surgery unit for 26 weeks from October. The elective
recovery plan sends the team to the specialty in which it prevents the most 52-week waits by 31 March 2027. The unit's weekend template
gives 640 day-case slots over the period, and the weekend rota is a surgeon, two scrub nurses and a recovery nurse. The candidates are
Orthopaedics, General Surgery, Ophthalmology, Urology, Gynaecology and ENT. The pack holds the waiting-list snapshot for 30 September
2026, the pre-assessment record, the commissioner's settled ledger, the treatment history, the access policy with its clock annex, the
national waiting-time returns for the closed year, and the unit's operating document and rota. The board decides on 15 October.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the snapshot, the pre-assessment plans, the ledger and the returns. Each specialty's at-risk day
  cases are real, and nobody's reading of their own numbers is overturned. The difficulty is which of them a team without an
  anaesthetist can treat.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the COO's and the clinical director's views and the commissioner's licensed basis. Every list is still
  labelled by specialty and day case, and the projection still ranks Urology first once clocks are right.
* **Instrument repair.** Clean-data test. The suspect file is the waiting-list snapshot, whose wait start for a second procedure on a
  paired organ is the original referral, not the clock the annex sets. Repair it (each listing carries its re-started clock): rung 1 then
  names Urology, as rung 2 does by direct read, and rung 0 still names General Surgery. The answer is unchanged, and the split by
  anaesthetic plan is still needed. No other file is suspect: every listed patient has a pre-assessment plan, and the ledger, rota and
  operating document are complete.
* **Lens swap.** The two reads cover different populations: 309 Urology day cases at risk on their true clocks, against the 86 of them
  planned under local anaesthetic, and Gynaecology's 150.

## 3. The driving force

A strong solver projects each specialty's list forward: patients reach 52 weeks in clock order unless existing lists treat them first,
with existing throughput from the commissioner's ledger. It keeps the day cases, because the weekend unit has no beds, and Ophthalmology
leads. It then re-clocks second-eye cataracts from the first eye, as the clock annex requires and the ledger's per-procedure waits
confirm, and Urology leads by 1.37×. That is a complete, back-tested projection. But the weekend rota has no anaesthetist. Without one,
a list can take only patients whose pre-assessment plans a local anaesthetic, and the plan sits on the pre-assessment record, not the
list. Urology's at-risk day cases are mostly older men with bleeding risk, planned under general anaesthesia; 28% are planned under
local. Gynaecology's are hysteroscopies and loop excisions, 71% under local. Every list the ledger settled had an anaesthetist, so it
cannot tell the two apart.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Projection with the ledger's existing throughput, all intended managements, capped at 640 slots | A, General Surgery (640, 1.23× Orthopaedics) | Reproduces the closed year's per-specialty breach counts | The operating document: weekend lists take day cases only, and 73% of General Surgery's at-risk patients are inpatients |
| 1 | Same, day cases only | B, Ophthalmology (470, 1.49× Urology) | The unit's casemix, cleanly applied | The ledger's finer controls: second-eye cataracts' waits at treatment reproduce only from the first eye, as the clock annex rules |
| 2 | Second procedures re-clocked from the first, found by patient and procedure family in the treatment history (E16) | C, Urology (309, 1.37× General Surgery) | Every per-procedure control in the ledger reproduces | The weekend rota has no anaesthetist, and the pre-assessment record plans 72% of Urology's at-risk day cases under general anaesthesia |
| 3 | **Decisive:** only day cases planned under local anaesthetic, read from the pre-assessment record (E29) | **D, Gynaecology (150, 1.34× Ophthalmology)** (5th of 6 on rung 0) | — | — |

* **Position table.** Gynaecology ranks 5th on rung 0, 4th on rung 1 and 3rd on rung 2, and leads only rung 3. Each rung's leader beats
  its runner-up by at least 1.23×.
* **Discriminator dominance.** Urology carries 1.46× (309 against 211) into rung 3. On the decisive axis, the share of at-risk day cases
  planned under local anaesthetic, Gynaecology holds 0.71 and Urology 0.28, an edge of 2.54×. That is 1.45 times the required 1.2 × 1.46
  = 1.75. The final margin over Urology is 150 against 86 (1.74×).
* **Partial correction priced (L3).** Every half-applied construction names a wrong specialty. Splitting by anaesthetic plan without
  re-clocking names Ophthalmology (447 against 155, 2.89×). Re-clocking only second eyes whose first eye was done at the trust's own site
  and then splitting names Ophthalmology too (335 against 153, 2.19×). Taking each procedure code's usual anaesthetic from the procedure
  catalogue instead of each patient's plan names Urology (170 against 127, 1.34×).
* **Grid.** Managements (all or day case) × clocks (referral or re-started) × anaesthetic (any or local) gives 8 cells. Every non-answer
  cell names General Surgery, Ophthalmology or Urology; all managements with re-started clocks and local plans names Urology (196 against
  160, 1.23×), because its frail inpatients under local count there. Only day cases, re-started clocks and local plans name Gynaecology.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The rota lists who works the weekend. The operating document says day cases only. The pre-assessment record
   carries each patient's planned anaesthetic. No document says that a list without an anaesthetist takes only local-anaesthetic cases,
   or joins the rota to the pre-assessment record.
2. **Corpus blind to the anaesthetic.** The ledger certifies throughput and clocks exactly. *In every settled episode of the closed 24
   months an anaesthetist was on the list, because neither site has ever run one without, so local and general plans were treated alike.*
   Run over the ledger, the split changes no back-tested breach or wait.
3. **No arithmetic symptom.** Snapshot counts tie to the national return, the ledger ties to the commissioner's payments, and every
   listed pathway has one pre-assessment.
4. **Not a row predicate.** Eligibility is a plan on another system's record, reached by pathway, and the waits prevented are a
   projection over the eligible pool in clock order against existing throughput.
5. **The enumeration is arithmetic.** 1,132 at-risk day cases are split by plan across six specialties, and 523 are planned under local.
6. **No cutover date.** Weekend lists are new, but nothing steps in any series the solver reads; the rota simply has no anaesthetist.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the lists are still labelled only by specialty and day case.

## 6. The calibration corpus

* **Form.** The commissioner's settled ledger: 24 months of paid elective episodes at the trust and its partner site, each with pathway
  ID, specialty, procedure, site and admission and discharge dates. The national returns supply the closed year's per-specialty 52-week
  breaches and median waits at treatment by procedure.
* **What it certifies (E16).** Existing throughput and the clock. The salient control, the trust-wide breach count (1,412), passes
  several throughput and clock constructions. The finer controls, per-specialty breaches and per-procedure waits at treatment, pass only
  the ledger's pathway-linked throughput with second procedures re-clocked from the first: second-eye cataracts' recorded waits run from
  the first eye.
* **What it is blind to.** The anaesthetic (above).
* **Twin pair.** Mr Ashdown's and Ms Tey's urology day-case lists are identical on every list column: 60 at-risk patients each, the same
  procedure mix, referral dates and priorities. The pre-assessment record plans local anaesthesia for 41 of Ashdown's and 20 of Tey's
  (2.05×), because Tey's patients are older and more often anticoagulated. Every list-based rule treats them alike.
* **Resemblance points at the decoy.** By procedure mix and age, Urology's at-risk list most resembles the partner site's weekday
  day-case lists, which the ledger shows clearing fastest.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The elective recovery plan: "The weekend team goes to the specialty in which it prevents the most 52-week waits by
  31 March 2027." The operating document: "Weekend lists take day cases only, 640 slots across the 26 weeks." The weekend rota: "Surgeon,
  two scrub nurses, one recovery nurse." The access policy: "Patients are treated in clock order within clinical priority." The clock
  annex, among its rules: "A second procedure on a paired organ, listed after the first is done, starts its own clock at the first
  procedure."
* **Empirical pins.** Existing throughput and re-started clocks, from the ledger's finer controls.
* **Voices.** The chief operating officer: "Our 52-week risk sits in general surgery and orthopaedics; it always has." The ophthalmology
  clinical director: "Cataracts are where the long waits are. Give us the weekends and we'll fill every list."
* **Licensed wrong basis.** The plan records that the commissioner monitors 52-week risk on weeks since referral and will review the
  allocation on that basis.

## 8. Determinism by construction

* **Horizon.** No at-risk patient's 52-week date falls within three days of 31 March, under either clock.
* **Throughput window.** The ledger's last 26, 39 and 52 weeks give the same weekly rates to within 2% for every specialty.
* **Plans.** Every listed patient is pre-assessed at listing, and plans are local, local with sedation, or general. Sedation needs an
  anaesthetist at this trust, so only "local" is eligible.
* **Procedure families.** Each second-procedure listing has exactly one earlier same-family treatment, at least 6 weeks before listing.
* **Capacity.** Only rung 0's leader exceeds 640 slots; at rung 3 every pool is under 640, so the cap decides nothing.

## 9. Prompt sketch and deliverables

> I have to tell the elective board on 15 October which specialty gets the weekend day-surgery team for the next 26 weeks. Our COO is
> sure the risk sits in general surgery and orthopaedics. Name the specialty and the number of 52-week waits it will prevent by 31 March,
> as one sentence for the board paper, and send `weekend_team_case.xlsx` with the sheets below, plus `breach_runway.png`.

* `weekend_team_case.xlsx` — the projection, the six specialties under the four rung constructions (ask C), the cancer-referral sheet
  (ask A) and the cancellation sheet (ask B).
* `breach_runway.png` — for each specialty, at-risk day cases by the week they reach 52 weeks, stacked by anaesthetic plan; the 640-slot
  line; the chosen specialty marked; and Ashdown's and Tey's lists annotated.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six specialties, the share of urgent suspected-cancer referrals seen within 14
  days in each quarter of the last year. *Device:* a referral the consultant downgrades after triage leaves the urgent pathway on its
  downgrade date, posted as a separate event, as the cancer waiting-times guide documents. Counting downgraded referrals as urgent
  misstates 15 of the 24 quarterly shares.
* **Ask B (device-carried).** The day-surgery unit's same-day cancellations in the last year, per specialty, by reason (patient, clinical,
  hospital). *Device:* a patient moved to another list on the same day is logged as a cancellation plus a new booking, with a "moved"
  flag in the booking audit. Counting moves as hospital cancellations overstates them by 18% to 40%.
* **Ask C (validity).** Waits prevented for each specialty under each of the four rung constructions.
* **Decoupling.** The cancer pathway file and the booking audit share no row with the elective snapshot, the pre-assessment record or the
  treatment history. Clearing the anaesthetic split changes no figure in asks A or B.

## 11. Rubric arithmetic

6 specialties × 4 quarters (ask A) + 6 × 3 reasons (ask B) + 6 specialties × 4 constructions (ask C) + the committed specialty, its
waits prevented and its margin + 4 named chart parts + 2 files ≈ 75 criteria.

## 12. World-building constraints

* At risk on the ledger projection, all managements, referral clocks (Orthopaedics, General Surgery, Ophthalmology, Urology,
  Gynaecology, ENT): 520 / 880 / 480 / 450 / 330 / 300. Day-case shares 0.35 / 0.27 / 0.98 / 0.70 / 0.66 / 0.40. Shares surviving
  re-clocking 0.85 / 0.95 / 0.25 / 0.98 / 0.97 / 0.95. Local-anaesthetic shares of re-clocked day cases 0.40 / 0.45 / 0.95 / 0.28 / 0.71
  / 0.10.
* Waits prevented by rung: rung 0 520 / 640 / 480 / 450 / 330 / 300; rung 1 182 / 238 / 470 / 315 / 218 / 120; rung 2 155 / 226 / 118 /
  309 / 211 / 114; rung 3 62 / 102 / 112 / 86 / 150 / 11.
* Ashdown's and Tey's lists are identical on every list column; 41 and 20 local plans.
* No settled episode ran without an anaesthetist. The cancer pathway file and the booking audit touch no elective pathway.

# AD05 — How many high-dose patients the referral letter puts on one prescriber, when the dose that defines them is a daily dose built from overlapping fills

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Policy & Education · public health-insurance programme integrity |
| Mirrors | Measuring a per-day intensity from records that arrive as overlapping batches (concurrent cloud reservations summed per hour at AWS and Google Cloud, overlapping ad flights summed per day at Meta, stacked subscriptions per account-day at app stores) |
| Decision shape | One figure committed at a date: the high-dose patient count stated in the referral letter sent to the medical board on 20 November 2026 |
| Committed call | Members for whom the referred prescriber wrote high-dose opioid therapy in Q2 2026, as a whole number |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · a non-commuting construction (E04): a daily dose summed across concurrent prescriptions, with an early refill's supply started when the previous supply runs out, pinned by the board's reviewer determinations; the writer attribution and a quiet second contamination behind a loud one (E15) at the lower rungs |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #7 uses the ready-made measure · #11 beats the headline trap, misses the quiet one · #17 guesses an attribution the data can settle |
| Calibration form | Gold-standard verification subsample: the board's reviewer determinations for 300 members of its last six referrals, each with the member's daily-dose timeline, and the unit's 400 original prescriptions with the clinician who signed |
| Driving force | The standard counts members on a daily dose of 90 MME or more, and the programme's conversion table invites a quarterly total over 91 days. A daily dose is built: each fill's supply laid on the calendar, concurrent prescriptions summed, and an early refill's supply started when the previous one runs out, as the board's reviewers do. That construction adds 80 members whose high-dose courses were too short to reach the quarterly total and drops 30 whose totals reached it only because early refills were stockpiled; on the writer-attributed fills it lands at 280, where every quarterly reading stops at 230 or above 330. |

## 1. Situation

A state health-insurance programme's integrity unit has already decided to refer Dr. Szabo to the medical board, and the letter that goes
on 20 November must state how many of his patients were on high-dose opioid therapy in the second quarter. The referral standard defines
the figure. The pack carries the practice's pharmacy claims (fill date, drug, strength, quantity and days' supply) and medical claims, the
member file, the programme's conversion table, the claims guide, the quarterly paid-claims reconciliation, the unit's verification sample
of 400 original prescriptions, and the board's closed reviewer files from its last six referrals.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each claim's prescriber field records the account the prescription was sent under, as the claims
  guide defines it, and every fill, days' supply, visit and conversion factor is right. No stakeholder figure is overturned; the
  difficulty is how fills make a daily dose.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the investigators' method. A careful quarterly count of his members, with reversals,
  adjustment chains and the writer handled, still lands 17.9% low at 230.
* **Instrument repair.** Suspect files: the claims' prescriber field (the account, not the writer) and the reversed and adjusted claims
  (superseded rows). Repaired, every claim names its writer and carries only its final link: rungs 0 to 3 all return 230, and the daily-dose
  construction is still needed to reach 280. Fill dates, days' supply and the conversion table are complete, and a claim that recorded its
  writer still records one fill, not a day's dose.
* **Lens swap.** The naive read sums a quarter's fills per member; the answer reads each member's dose day by day, a different population
  of member-days in which short high-dose courses count and stockpiled supply does not.

## 3. The driving force

A strong solver pulls every pharmacy claim under Dr. Szabo's number, drops reversed claims, collapses adjustment chains to their final
link and ties the paid total, then learns from the verification sample that the nurse practitioner sends his renewals under Dr. Szabo's
account while Dr. Szabo writes under Dr. Okonjo's at the satellite clinic, and re-attributes every fill to the clinician of the member's
latest visit. It converts by the programme's table and counts members at 8,190 MME, ninety days at the line, and lands at 230. Every step
is right except the last. The standard's unit is a daily dose. A member on two concurrent prescriptions of 60 MME a day is on 120 for as
long as they overlap, and a five-week course at 120 never reaches the quarterly total; a member who refills a 30-day supply every 24 days
reaches the total without ever taking 90 in a day. The board's reviewers build the day: each fill's supply laid on the calendar from its
fill date, an early refill of the same drug and strength starting when the previous supply runs out, and concurrent prescriptions summed.
That construction adds 80 short-course members, drops 30 stockpilers, and gives 280.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Every pharmacy claim under his prescriber number, converted by the programme's table, members at or over 8,190 MME in the quarter | 380, +35.7% | The prescriber field is the prescriber, and ninety days at the line is the standard's dose over the quarter | The claims guide: a reversed claim stays on file with status R and was never dispensed |
| 1 | Hygiene: reversed claims removed | 350, +25.0% | The obvious contamination is gone and the count has moved | The paid-claims reconciliation: the quarter's paid total ties only when each adjustment chain is collapsed to its final link |
| 2 | Hygiene: adjustment chains collapsed, paid total tied | 330, +17.9% | Every claim is accounted for and the control total ties to the cent | The verification sample: 148 of the 400 signed prescriptions were written by someone other than the account on the claim |
| 3 | Each fill attributed to the clinician of the member's latest visit at the practice on or before the fill date | 230, −17.9% | The writer settled fill by fill and reproduced on all 400 signed prescriptions | The reviewer determinations: the quarterly total reproduces 236 of 300, missing every member on a short high-dose course and every stockpiler |
| 4 | **Decisive:** each member's daily dose from his fills, supply laid from the fill date, an early refill of the same drug and strength starting when the previous supply runs out, concurrent prescriptions summed; members reaching 90 MME on any day | **280** | — | — |

* **Figure shape.** The hygiene and attribution corrections walk the figure down; the decisive move reverses them. Per-rung offsets are
  +35.7%, +25.0%, +17.9% and −17.9%.
* **Partial correction priced (L3).** A solver who sums concurrent prescriptions by calendar day but lets early refills overlap lands at
  310 (+10.7%), counting 30 stockpilers whose overlapping supply looks like a double dose. A solver who builds the daily dose but keeps the
  account on the claim lands at 352 (+25.7%). A solver who reads the daily dose of each fill on its own, without summing concurrent
  prescriptions, lands at 230 (−17.9%), losing the 50 members whose high dose comes from two drugs at once.
* **Grid.** Reversals (kept or removed) × adjustment chains (summed or collapsed) × attribution (account or latest visit) × dose (quarterly
  total, per fill, concurrent without shift, concurrent with shift) gives 32 cells. The nearest wrong cells are concurrent without shift at
  310 (+10.7%), the full construction with reversals kept at 314 (+12.1%) and with chains summed at 318 (+13.6%); every other cell sits at
  least 17.9% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard says a daily dose of 90 MME or more; the conversion table gives MME per unit. Nothing says how fills
   combine into a day, and the reviewers' timelines sit in closed referral files.
2. **The corpus pins a construction, not a menu.** Concurrent daily doses with shifted early refills reproduce all 300 reviewer
   determinations; the quarterly total reproduces 236, the per-fill dose 251 and concurrent doses without the shift 271. The quarterly
   total errs both ways and the other two each in one direction, so none reproduces the sample's count either. The construction is a
   timeline per member, built from dates and supplies, and no column holds a daily dose.
3. **No arithmetic symptom.** Every fill's MME ties to the table, the paid total ties, and quarterly sums are exact under every reading.
4. **Not a row predicate.** It needs each member's fills laid on a calendar, early refills shifted within drug and strength, concurrent
   doses summed by day, and a maximum taken per member.
5. **The enumeration is arithmetic.** Who reaches 90 MME on some day is computed member by member; the count then follows exactly.
6. **No cutover date.** Courses start and stop throughout the quarter, and the nurse practitioner's and the satellite's arrangements
   predate it; no series steps.
7. **Survives deletion.** With every voice and the investigators' method removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The board's closed reviewer files from its last six referrals of other prescribers: 300 members, each with the reviewer's
  day-by-day dose timeline and determination. Beside them, the unit's 400 original Schedule II prescriptions from Q4 2025 and Q1 2026,
  each recording the clinician who signed.
* **What it pins.** The daily-dose construction, 300 of 300; the latest-visit attribution, 400 of 400 signed writers against 252 for the
  account on the claim.
* **Twin pair.** Members 40711 and 52390 in the reviewers' sample are identical on every claims total: the same two drugs, strengths,
  quantities, days' supply, fill count and quarterly MME (4,200). The reviewers set their maximum daily doses at 120 and 60 MME (2×): 40711's
  two prescriptions ran concurrently for 35 days and 52390's one after the other.
* **Every rule exercised.** The sample holds early refills of the same drug (shifted), switches of drug mid-supply (not shifted), members
  with three concurrent prescriptions, and supplies crossing the quarter's end.
* **Resemblance points at the decoy.** By quarterly totals his members most resemble the referrals whose counts the investigators'
  quarterly method matched exactly.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The referral standard: the figure counts members for whom the referred prescriber wrote opioid therapy at a daily dose of
  90 MME or more in the quarter, at the programme's conversion table. The claims guide's definitions of reversed and adjusted claims.
* **Empirical pins.** The daily-dose construction, from the reviewer determinations; the latest-visit attribution, from the verification
  sample.
* **Voices.** The unit's clinical pharmacist: "The prescriber field is the prescriber, and that's how the board will read it." The unit's
  data lead: "Reversals are the only thing in pharmacy claims that ever trips us up."
* **Licensed wrong basis.** The referral procedure records that the board's investigators count members at 8,190 MME over the quarter on
  fills under the prescriber's own account and will check the letter against that count.

## 8. Determinism by construction

* **Shift.** Early refills shift within the same drug and strength only; a change of drug or strength starts its supply on its fill date.
  No member's maximum daily dose sits within 3% of 90 MME.
* **Attribution.** Every fill has a practice visit within 21 days before it, and no member saw two clinicians between a visit and the next
  fill, so latest-visit rules with 30- or 60-day limits assign identically.
* **Maturity.** Adjustments post up to 90 days after the fill; the extract is taken 120 days after the quarter closed, so every chain is
  final.
* **Supply.** Every fill carries days' supply between 7 and 30; supplies crossing the quarter's end count only on the quarter's days.

## 9. Prompt sketch and deliverables

> The letter referring Dr. Szabo to the medical board goes out on 20 November and has to state how many of his patients were on high-dose
> opioid therapy in the second quarter. Our clinical pharmacist reads the prescriber field as the prescriber. Give me the number as one
> sentence for the letter, with `referral_evidence.xlsx` holding the sheets below, a chart `daily_dose_timeline.png`, and a one-page
> `referral_figure.html` I can attach.

* `referral_evidence.xlsx` — the member-level build with each member's maximum daily dose, the naloxone sheet (ask A), the drug-screen sheet
  (ask B) and the construction back-test (ask C).
* `daily_dose_timeline.png` — the twin members and three of his members as calendar strips, each fill's supply laid from its fill date with
  early refills shifted, the summed daily dose against the 90 MME line, and an inset of the count under each dose construction.
* `referral_figure.html` — the committed figure, the members gained and lost at the decisive step, and the readings the investigators
  will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 14 pharmacies, Q2 naloxone dispensings to the practice's members and the share of
  those members' opioid fills they accompany. *Device:* naloxone under the state's standing order is billed under the pharmacist's own
  number, with the standing-order prescriber in a separate field, as the standing-order notice says. Matching naloxone to the practice
  through the prescriber field finds almost none; it has to be matched by member and date. The main figure never reads naloxone claims.
* **Ask B (device-carried).** For each month of Q2, the practice's urine drug screens and the share confirmed by a definitive test.
  *Device:* a definitive test ordered after a presumptive positive carries the same order number under a different code family, per the
  lab billing guide. Counting codes as screens double-counts every confirmed screen.
* **Ask C (validity).** For each of the four dose constructions, the reviewer determinations it reproduces out of 300, and the figure under
  each of the five rung bases.
* **Decoupling.** Clearing the daily-dose construction changes no figure in asks A or B.

## 11. Rubric arithmetic

14 pharmacies × 2 (ask A) + 3 months × 2 (ask B) + 4 constructions and 5 rung figures (ask C) + the committed figure, the members gained
and the members lost at the decisive step + 5 named chart parts + 3 files ≈ 54 criteria.

## 12. World-building constraints

* Rung figures are 380 / 350 / 330 / 230 / 280. Every grid cell sits at least 10.7% from the answer.
* Reversals add 30 members at rung 0 and adjustment chains 20; attribution removes 128 members and adds 28.
* On his written fills: 150 members at or over 90 MME every day, 50 reaching it only on concurrent prescriptions, 80 on courses too short
  for the quarterly total, and 30 stockpilers whose totals pass 8,190 with no day at 90.
* The verification sample holds 400 signed fills, 148 written by someone other than the account holder; the reviewers' sample holds 300
  members, and members 40711 and 52390 are identical on every claims total.
* Naloxone standing-order claims and lab claims never touch the opioid fills, the visits or the reviewer files.

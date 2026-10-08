# AD05 — How many high-dose patients the referral letter puts on one prescriber, when the claims carry the account a prescription was sent under and not the clinician who wrote it

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Policy & Education · public health-insurance programme integrity |
| Mirrors | Attributing actions to the person who took them when the system logs the account they were taken under (shared admin credentials in AWS and Google Cloud audit logs, delegated posting on Meta business pages, sales credited to the account owner rather than the rep who closed) |
| Decision shape | One figure committed at a date: the high-dose patient count stated in the referral letter sent to the medical board on 20 November 2026 |
| Committed call | Patients for whom the referred prescriber wrote high-dose opioid therapy in Q2 2026, as a whole number |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · a latent attribution marker recovered against a verification sample (E19, Pattern B), with a quiet second contamination behind a loud one (E15) |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #17 guesses an attribution the data can settle · #11 beats the headline trap, misses the quiet one · #18 joins only on the visible key |
| Calibration form | Gold-standard verification subsample: 400 original prescriptions pulled from pharmacies, each with the clinician who signed it |
| Driving force | Pharmacy claims carry the prescriber an e-prescribing account is registered to. The nurse practitioner's renewals go out under Dr. Halvorsen's number, and his own prescriptions at the satellite clinic go out under the satellite's registered prescriber. The writer is recoverable exactly as the clinician of the member's latest visit at the practice on or before the fill, a ranked join into the medical claims, and it moves patients both off and onto his count. |

## 1. Situation

A state health-insurance programme's integrity unit has already decided to refer Dr. Halvorsen to the medical board, and the letter that
goes on 20 November must state how many of his patients were on high-dose opioid therapy in the second quarter. The referral standard
defines the figure. The pack carries the practice's pharmacy claims and medical claims, the member file, the programme's conversion table,
the claims guide, the quarterly paid-claims reconciliation, and the unit's verification sample of 400 original prescriptions.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each claim's prescriber field records the account the prescription was sent under, exactly as the
  claims guide defines it, and every fill, visit and conversion factor is right. No stakeholder figure is overturned. The difficulty is an
  attribution the claims never carry and the medical claims settle.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the board's counting practice. A careful count of the claims under his number, with reversals
  and adjustment chains handled, still lands 36.7% low.
* **Instrument repair.** Make every claim perfect; the prescriber field is already correct for what it records. An instrument that
  recorded the account more carefully would still record the account, not the hand that signed.
* **Lens swap.** The naive read counts members with fills under his account. The answer counts members whose fills he wrote, which adds
  members recorded under another account and removes members whose fills the nurse practitioner wrote: a different population of fills.

## 3. The driving force

A strong solver pulls every pharmacy claim under Dr. Halvorsen's number, drops reversed claims, notices that adjusted claims chain to their
originals and keeps only the final link, reconciles to the paid-claims control, converts to morphine milligram equivalents and counts
members over the line. Every step is right, and the count is wrong by more than a third. The practice runs one e-prescribing account per
registered prescriber per site. The nurse practitioner, who writes most routine renewals at the main site, sends them under his account;
at the satellite clinic, where he covers three sessions a week, everything goes out under Dr. Okonjo's account. No claim field carries
the writer. The verification sample shows who signed, and the signal that reproduces it is in a different file: the rendering clinician
of the member's most recent visit at the practice on or before the fill date. That is a ranked join from each fill into the medical claims
on member and date, and applying it removes 29 members from his count and adds 117.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Every pharmacy claim under his prescriber number, converted by the programme's table, members at or over 8,190 MME in the quarter | 212, −11.7% | The prescriber field is the prescriber, and the standard's line is applied exactly | The claims guide: a reversed claim stays on file with status R and was never dispensed |
| 1 | Hygiene: reversed claims removed | 186, −22.5% | The obvious contamination is gone and the count has moved | The paid-claims reconciliation: the quarter's paid total ties only when each adjustment chain is collapsed to its final link, because an adjustment is a new claim pointing at the one it replaces |
| 2 | Hygiene: adjustment chains collapsed, paid total tied | 152, −36.7% | Every claim is accounted for and the control total ties to the cent | The verification sample: 148 of the 400 signed prescriptions were written by someone other than the account on the claim |
| 3 | **Decisive:** each fill attributed to the rendering clinician of the member's latest visit at the practice on or before the fill date, across every account the practice holds | **240** | — | — |

* **Figure shape.** The two hygiene corrections walk the figure down; the decisive move reverses them and lands above rung 0. Per-rung
  offsets are −11.7%, −22.5% and −36.7%.
* **Partial correction priced (L3).** A solver who learns from the sample that the nurse practitioner writes under his account, and removes
  those fills without asking whether he writes under anyone else's, lands at 123, 48.8% low and further away than any rung.
* **Grid.** Reversals (kept or removed) × adjustment chains (summed or collapsed) × attribution (account, removals only, or latest visit)
  gives twelve cells. The nearest wrong cell is the full attribution with reversals left in, at 266 (+10.8%), which keeps rows the claims
  guide marks as never dispensed; the attribution with adjustment chains summed (the quiet trap missed) lands at 274 (+14.2%). Every other
  cell sits at least 11.7% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The claims guide defines the prescriber field as the account the prescription was sent under. No document says
   who uses which account, that the satellite has its own registered prescriber, or that visits identify the writer.
2. **The corpus pins a construction, not a menu.** The latest-visit rule reproduces 400 of 400 signed writers; the account on the claim
   reproduces 252, a site default 318, and a same-day-visit rule covers only 61% of fills. The reproducing rule is a construction: each
   fill must be ranked against the member's visits by date in another file, and no column in either file holds the result.
3. **No arithmetic symptom.** Paid claims tie to the reconciliation, visits tie to the medical claims control, and every member's fills sum
   the same under every attribution; only who owns them changes.
4. **Not a row predicate.** It needs a join from each fill to the member's visits, a rank by date within member to the latest visit on or
   before the fill, and the rendering clinician of that visit.
5. **The enumeration is arithmetic.** Which fills are his is computed fill by fill, and the patient count is then a threshold on a sum
   over his fills per member.
6. **No cutover date.** The nurse practitioner and the satellite sessions predate the window and run through it; no series steps.
7. **Survives deletion.** With every voice and the board's practice removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The verification sample: 400 Schedule II prescriptions filled in Q4 2025 and Q1 2026 at the practice's two sites, pulled as
  originals from 14 pharmacies, each recording the clinician who signed.
* **What it pins.** The latest-visit rule reproduces all 400; the claim's account 252; a site default 318. The account rule's 148 misses run
  both ways (96 nurse-practitioner fills under his account, 52 of his fills under Dr. Okonjo's), so the sample refutes it fill by fill and
  in each direction's total.
* **Twin pair.** Members 40711 and 52390 have identical claims rows: six fills each under his account, the same oxycodone strengths and
  quantities, the same pharmacy and the same fill days. The sample's signed writers are him for all six of 40711's fills and for three of
  52390's, so his MME is 9,180 against 4,590, one above the line and one below.
* **Every rule exercised.** The sample holds fills written at a visit one to 21 days earlier, members seen by two clinicians in the
  quarter (the latest visit decides), and satellite fills he signed under Dr. Okonjo's account.
* **Resemblance points at the decoy.** His main-site claims most resemble those of the practice's other physicians, whose sampled fills
  matched their accounts 97% of the time, so transferring their match rate keeps the account rule.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The referral standard: the figure counts members for whom the referred prescriber wrote opioid prescriptions totalling
  at least 8,190 MME by fill date in the quarter, at the programme's conversion table. The claims guide's definitions of reversed and
  adjusted claims.
* **Empirical pins.** The latest-visit attribution, from the verification sample.
* **Voices.** The unit's clinical pharmacist: "The prescriber field is the prescriber, and that's how the board will read it." The unit's
  data lead: "Reversals are the only thing in pharmacy claims that ever trips us up."
* **Licensed wrong basis.** The referral procedure records that the board's investigators count fills under the prescriber's own account
  and will check the letter against that count.

## 8. Determinism by construction

* **Attribution.** Every fill has a practice visit within 21 days before it, and no member saw two clinicians between a visit and the next
  fill, so latest-visit, latest-visit-within-30-days and latest-visit-within-60-days rules assign identically.
* **Maturity.** Adjustments post up to 90 days after the fill; the extract is taken 120 days after the quarter closed, so every chain is
  final.
* **Threshold.** No member sits within 3% of 8,190 MME under the answer's attribution, so conversion rounding cannot move the count.
* **Dates.** The standard counts by fill date; written dates are not in the claims, so no second convention exists.

## 9. Prompt sketch and deliverables

> The letter referring Dr. Halvorsen to the medical board goes out on 20 November and has to state how many of his patients were on
> high-dose opioid therapy in the second quarter. Our clinical pharmacist reads the prescriber field as the prescriber. Give me the number
> as one sentence for the letter, with `referral_evidence.xlsx` holding the sheets below, a chart `writer_attribution.png`, and a one-page
> `referral_figure.html` I can attach.

* `referral_evidence.xlsx` — the member-level build, the naloxone sheet (ask A), the drug-screen sheet (ask B) and the attribution
  back-test (ask C).
* `writer_attribution.png` — a flow from the two accounts on the claims to the three writers who signed, in fills and in members over the
  line, with the 29 members leaving his count and the 117 joining it labelled, and the twin members marked.
* `referral_figure.html` — the committed figure and the readings the board's investigators will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 14 pharmacies, Q2 naloxone dispensings to the practice's members and the share of
  those members' opioid fills they accompany. *Device:* naloxone under the state's standing order is billed under the pharmacist's own
  number, with the standing-order prescriber in a separate field, as the standing-order notice says. Matching naloxone to the practice
  through the prescriber field finds almost none; it has to be matched by member and date. The main figure never reads naloxone claims.
* **Ask B (device-carried).** For each month of Q2, the practice's urine drug screens and the share confirmed by a definitive test.
  *Device:* a definitive test ordered after a presumptive positive carries the same order number under a different code family, per the
  lab billing guide. Counting codes as screens double-counts every confirmed screen.
* **Ask C (validity).** For each of the four attribution rules (account, site default, same-day visit, latest visit), the signed writers it
  reproduces out of 400, and the figure under each of the four rung bases.
* **Decoupling.** Clearing the attribution changes no figure in asks A or B.

## 11. Rubric arithmetic

14 pharmacies × 2 (ask A) + 3 months × 2 (ask B) + 4 rules and 4 bases (ask C) + the committed figure, the members leaving and the members
joining + 5 named chart parts + 3 files ≈ 53 criteria.

## 12. World-building constraints

* Rung figures are 212 / 186 / 152 / 240. Every grid cell sits at least 10.8% from the answer; the removals-only partial lands at 123.
* Reversals add 26 members at rung 0 and adjustment chains 34; attribution removes 29 members and adds 117.
* The nurse practitioner writes 38% of the fills under his account; he writes 44% of the fills under Dr. Okonjo's satellite account.
* The sample holds 400 signed fills, 148 written by someone other than the account holder; members 40711 and 52390 are identical on every
  claims column.
* Every fill has a practice visit within 21 days before it. No member sits within 3% of the line.
* Naloxone standing-order claims and lab claims never touch the opioid fills or the visits.

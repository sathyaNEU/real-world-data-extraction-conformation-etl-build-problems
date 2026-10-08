# AD13 — Which university division gets the two-week threat hunt, when the division with the most confirmed lateral movement is printed only as "<5"

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Policy & Education · university information security |
| Mirrors | Deciding where to look when the most sensitive units' incident counts reach you only through suppressed aggregate reports (privacy-restricted incident reporting in Google and Microsoft enterprise tenants, regulated subsidiaries in bank security operations, HR-system incidents at large employers) |
| Decision shape | Which of N gets one scarce thing: the external hunt team's single two-week engagement next term |
| Committed call | The one division the hunt team works in, and its confirmed lateral-movement rate per 1,000 accounts over the last two quarters |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · a suppressed cell bounded from published margins (E25), the margins found through division groups and inverted at a convention the line-level acknowledgements pin, with a saturated tie at the lower rung (E21) |
| Gate G mechanism | method_or_model_selection, with binding_constraint support |
| Measured traps engaged | #24 treats an unpublished figure as unknown · #19 breaks a big tie instead of questioning it · #7 uses the ready-made measure |
| Calibration form | Counterparty acknowledgement file: the incident-response provider's line-level acknowledgements for five divisions and its quarterly matrix of confirmed rates for all eight, privacy-restricted cells under 5 printed as "<5" |
| Driving force | The incident-response provider confirms lateral movement case by case, but for the three privacy-restricted divisions it reports only quarterly rates, printing any cell under five cases as "<5". Treasury's two cells are both "<5", so every natural reading drops it, imputes it or caps it. Each suppressed cell sits inside a published group rate whose other members are printed, and inverting the matrix's own convention (cases over accounts at quarter start, rounded to 0.1) recovers Treasury's counts exactly: 7 cases on 1,100 accounts, the highest rate in the university. |

## 1. Situation

A university's central security office can bring an external threat-hunting team in for two weeks next term, and the team works in one
division. The security policy says the hunt goes where confirmed lateral movement has been heaviest per 1,000 accounts over the last two
quarters. The SOC's detector raises alerts; escalated alerts go to the outsourced incident-response provider, which confirms or closes them.
For five divisions it acknowledges line by line. For the three privacy-restricted divisions (Treasury, Human Resources, Legal and
Compliance) it publishes only a quarterly matrix of confirmed rates by division and by division group. The pack carries the alerts, the
SOC's triage log and queue log, the identity directory's account counts, and the provider's file.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the alerts, the SOC's triage outcomes, every acknowledgement line and every printed cell of the matrix.
  The suppression is the provider's documented privacy rule. Nothing reported is overturned; the difficulty is that an unprinted figure is
  determined by printed ones.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the SOC lead's view. Ranking the printed confirmed rates, with "<5" cells left out, imputed or capped, still
  names C or F.
* **Instrument repair.** Make every alert and acknowledgement perfect; they already are. A provider that printed every cell would remove
  the puzzle, and a better SOC detector would still not know what the provider confirmed.
* **Lens swap.** The naive set ranks the divisions whose cells are printed; the answer's set includes the restricted divisions whose cells
  are recovered, a different population of divisions, and Treasury enters it at the top.

## 3. The driving force

A strong solver distrusts raw alert volume, turns to the SOC's triage outcomes, finds four divisions at a 100% true-positive share,
applies the policy's tie-break, then sees that the triage queue left most alerts untriaged and switches to the provider's confirmations,
which are the policy's basis. It ranks the printed rates and names C. The restricted divisions are blanks, and every natural way of
filling a blank misleads: leaving them out keeps C; the suppression midpoint or ceiling puts Human Resources, with 400 accounts, absurdly
on top. The matrix also prints each division group's rate, and Treasury shares a group with two printed divisions, Human Resources with
two others. Converting printed rates back to cases needs the matrix's convention, cases over accounts at quarter start rounded to 0.1 per
1,000, which only reproducing the five line-level divisions' printed cells reveals. Subtracting within each group then recovers every
suppressed cell to a unique integer: Treasury had 4 and 3 cases, 6.4 per 1,000 accounts.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Lateral-movement alerts per 1,000 accounts, last two quarters | A, Research Computing (61) | The SOC's detector, normalised for size | The provider's acknowledgements: 71% of A's escalations were closed as administrator activity |
| 1 | SOC triage true-positive share; four divisions at 100%; the policy's tie-break (criticality tier, then accounts) | B, Estates (tier 1, 6,200 accounts against F's 400) | An outcome measure, the policy's documented tie-break applied | The triage queue log: the SOC triages at most 50 alerts a day, and under the policy's rule that shares count every alert raised, B's 11 of 11 is 11 of 38 |
| 2 | The provider's confirmed rate per 1,000 accounts, printed cells, "<5" cells left out | C, Admissions (5.1) | The policy's own basis, from the counterparty's record, with nothing invented for the blanks | The matrix's group rates: every "<5" cell sits in a printed group whose other members are printed |
| 3 | **Decisive:** the matrix's convention recovered from the five line-level divisions, then each suppressed cell solved from its group, cases over start-of-quarter accounts | **E, Treasury (6.4)** (5th of 8 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0 (31), 8th on rung 1 (67%) and is absent from rung 2, and leads only rung 3, 1.24× C. Intermediate
  leaders hold margins of 1.24×, the tie-break's tier and accounts, and 1.37×.
* **Discriminator dominance.** At rung 2 the natural fill for Treasury is the midpoint, 4.5 per 1,000, so C carries 1.13× into rung 3.
  Recovery lifts Treasury by 1.40× to 6.4, against the 1.2 × 1.13 = 1.36 required; E leads C by 1.24×.
* **Partial correction priced (L3).** Midpoint imputation (2.5 cases a cell) and ceiling imputation (4) both name F, Human Resources, at 12.5
  and 20 per 1,000, because 400 accounts magnify any guess; its recovered cells are 1 and 1, 5.0 per 1,000. Recovering cells with average
  accounts instead of start-of-quarter accounts gives the same integers, so that slip costs nothing.
* **Grid.** Fill (omit, zero, midpoint, ceiling, recover) × denominator (start or average accounts) gives ten cells: omit and zero name C,
  midpoint and ceiling name F, recovery names E under either denominator. The nearest wrong name, C, needs the group margins ignored.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The provider's note says cells under five are printed as "<5" for privacy. Nothing says the group rates determine
   them or gives the rate convention.
2. **The corpus pins a construction, not a menu.** Start-of-quarter accounts rounded to 0.1 reproduce all 10 printed cells of the five
   line-level divisions; average accounts reproduce 7 and unrounded rates none. The recovery is a construction: it needs that convention,
   the group each suppressed cell belongs to, and a subtraction of printed members, with no column holding a recovered count.
3. **No arithmetic symptom.** Every printed cell is consistent with every other; the blanks look like the privacy rule working as written.
4. **Not a row predicate.** It needs rates turned back into cases at the right denominator, group totals less printed members, and a
   rounding band resolved to an integer for each blank.
5. **The enumeration is arithmetic.** Each recovered count is the only integer inside its rounding band; no field carries it.
6. **No cutover date.** Treasury's cases are spread across both quarters; no series steps.
7. **Survives deletion.** With every voice removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The provider's file: line-level acknowledgements for the five unrestricted divisions (every escalation with its outcome), and the
  quarterly matrix for all eight divisions and three division groups, with "<5" for any cell under five cases.
* **What it pins.** The rate convention, from reproducing the 10 printed cells the line-level divisions also report. Recovered counts:
  Treasury 4 and 3, Human Resources 1 and 1, Legal and Compliance 4 and 2.
* **Twin pair.** Treasury's Q3 cell and Legal and Compliance's Q4 cell are both printed "<5", both in restricted divisions, with identical
  alerts per 1,000 accounts (14.8) and triage shares that quarter. They recover to 4 and 2 cases (2×).
* **Every rule exercised.** One group holds two suppressed cells in one quarter, so the group with a second printed margin is needed; one
  division's accounts changed by 2% within a quarter, so the start-of-quarter denominator is tested.
* **Resemblance points at the decoy.** On every SOC-side column Treasury most resembles Legal and Compliance, whose recovered rate is the
  university's lowest.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The security policy: the hunt goes where confirmed lateral movement has been heaviest per 1,000 accounts over the last two
  quarters; shares count every alert raised; ties go to the higher criticality tier, then to more accounts. The identity directory's
  accounts at each quarter start.
* **Empirical pins.** The matrix's rate convention, from the line-level divisions.
* **Voices.** The SOC lead: "The detector knows where the movement is; send the hunt where it fires hardest." The provider's account
  manager: "Restricted divisions are too small to matter, which is why their cells are suppressed."
* **Licensed wrong basis.** The policy records that the university's insurer scores divisions on printed confirmed rates and will see the
  placement on that basis.

## 8. Determinism by construction

* **Integers.** Every recovered count is the unique integer within its rounding band, and both denominators give the same integers.
* **Window.** The two quarters are filed; Treasury leads on either quarter alone.
* **Groups.** Every suppressed cell sits in exactly one group, and where a group holds two blanks in a quarter its other quarter and the
  division's other group margin settle them.
* **Accounts.** The directory's start-of-quarter counts are filed and never revised.

## 9. Prompt sketch and deliverables

> We can bring the external hunt team in for two weeks next term, and it works in one division. The SOC lead would send it wherever the
> lateral-movement detector fires hardest. Tell me the division and its confirmed rate, in a line for the security committee, with
> `hunt_placement.xlsx` holding the sheets below, the chart `confirmed_rates.png`, and a one-page `committee_note.pdf`.

* `hunt_placement.xlsx` — the division build with every recovered cell and the margin it came from, the MFA sheet (ask A), the phishing sheet
  (ask B) and the convention test (ask C).
* `confirmed_rates.png` — the eight divisions' confirmed rates per 1,000 accounts as bars, recovered cells hatched with their rounding bands as
  error bars, the midpoint and ceiling imputations marked as ghosts for the restricted divisions, and the chosen division highlighted.
* `committee_note.pdf` — the committed division and why the printed ranking and the imputations are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each division, privileged accounts without multi-factor enrolment at quarter end, as a count
  and as a share of its people with privileged access. *Device:* the directory lists a person's standard and administrative accounts
  separately, linked by an owner ID, as its schema documents. Counting accounts as people overstates the share in the three divisions where
  administrators hold several accounts. The hunt placement uses account counts only as the matrix's denominators.
* **Ask B (device-carried).** For each month of the two quarters, phishing emails staff reported and the share the mail team confirmed
  malicious. *Device:* the report button files one report per recipient, and the mail team's log groups a campaign's reports under one
  campaign ID. Counting reports as emails overstates every month with a large campaign.
* **Ask C (validity).** For each of three rate conventions (start-of-quarter accounts, average accounts, unrounded), the printed cells it
  reproduces out of 10.
* **Decoupling.** Clearing the recovery changes no figure in asks A or B.

## 11. Rubric arithmetic

8 divisions × 2 (ask A) + 6 months × 2 (ask B) + 3 conventions (ask C) + the committed division, its rate and the six recovered cells + 5
named chart parts + 3 files ≈ 47 criteria.

## 12. World-building constraints

* Accounts: A 9,800, B 6,200, C 3,900, D 2,400, E 1,100, F 400, G 2,700, H 1,600. Half-year confirmed cases: 31, 22, 20, 6, 7, 2, 9, 6.
* Treasury (E) 4 and 3 cases, Human Resources (F) 1 and 1, Legal and Compliance (D) 4 and 2, all printed "<5".
* Rung leaders are A, B, C, E; E leads rung 3 by 1.24× over C; midpoint and ceiling fills name F.
* Four divisions show 100% triage shares; the SOC triages at most 50 alerts a day.
* Treasury's Q3 and Legal and Compliance's Q4 cells are identical on every SOC-side column.
* Owner-linked accounts and campaign-grouped phishing reports never touch the provider's matrix or the alerts.

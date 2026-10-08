# AD13 — Which university division gets the two-week threat hunt, when the division with the most confirmed lateral movement is printed only as "<5"

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Policy & Education · university information security |
| Mirrors | Deciding where to look when the most sensitive units' incident counts reach you only through suppressed aggregate reports (privacy-restricted incident reporting in Google and Microsoft enterprise tenants, regulated subsidiaries in bank security operations, HR-system incidents at large employers) |
| Decision shape | Which of N gets one scarce thing: the external hunt team's single two-week engagement next term |
| Committed call | The one division the hunt team works in, and its confirmed lateral-movement rate per 1,000 accounts over the last two quarters |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · a suppressed cell bounded from published margins (E25), solved from the one margin family in which each restricted division stands alone, at a rate convention the line-level acknowledgements pin; a tie the scorecard's rounding saturates at the lower rung (E21) |
| Gate G mechanism | method_or_model_selection, with binding_constraint support |
| Measured traps engaged | #24 treats an unpublished figure as unknown · #19 breaks a big tie instead of questioning it · #7 uses the ready-made measure |
| Calibration form | Counterparty acknowledgement file: the incident-response provider's line-level acknowledgements for six divisions and its quarterly matrix of confirmed rates for all eight, by division, functional group and campus, cells of one to four cases printed as "<5" |
| Driving force | The incident-response provider confirms lateral movement case by case, but for the two privacy-restricted divisions it reports only quarterly rates, printing any cell of one to four cases as "<5". All four of their cells are "<5", so every natural reading drops them, imputes them or caps them, and any guess puts Human Resources, with 400 accounts, on top. Both sit in one functional group, whose margin gives only their sum; but each is the only blank on its campus, and inverting the matrix's convention (cases over start-of-quarter accounts, to two decimals) recovers every cell exactly: Treasury had 8 cases on 900 accounts, the highest rate in the university. |

## 1. Situation

A university's central security office can bring an external threat-hunting team in for two weeks next term, and the team works in one
division. The security policy says the hunt goes where confirmed lateral movement has been heaviest per 1,000 accounts over the last two
quarters. The SOC's detector raises alerts; escalated alerts go to the outsourced incident-response provider, which confirms or closes them.
For six divisions it acknowledges line by line. For the two privacy-restricted divisions, Treasury and Human Resources, it publishes only a
quarterly matrix of confirmed rates by division, by functional group and by campus. The pack carries the alerts, the SOC's monthly
scorecard and triage log, the identity directory's account counts, the criticality register and the provider's file.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the alerts, the scorecard, the triage outcomes, every acknowledgement line and every printed cell of
  the matrix. The suppression is the provider's documented privacy rule. Nothing reported is overturned; the difficulty is that an
  unprinted figure is determined by printed ones.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the SOC lead's view. Ranking the confirmed rates with the restricted cells left out, imputed or capped, still
  names C or F.
* **Instrument repair.** Make every alert and acknowledgement perfect; they already are. A provider that printed every cell would remove
  the puzzle, and a better SOC detector would still not know what the provider confirmed.
* **Lens swap.** The naive set ranks the divisions whose cases are acknowledged; the answer's set includes the restricted divisions whose
  cells are recovered, a different population of divisions, and Treasury enters it at the top.

## 3. The driving force

A strong solver distrusts raw alert volume and turns to the SOC's triage outcomes, where four divisions print at 100%. It reads the triage
log's exact counts rather than the scorecard's rounding, sees that triage shares are not confirmations anyway, and moves to the provider's
acknowledgements, the policy's basis. Ranking the six acknowledged divisions names C. The restricted divisions are blanks, and every
natural way of filling one misleads: leaving them out keeps C, and the midpoint or the ceiling puts Human Resources, with 400 accounts, on
top. The matrix also prints each functional group's rate, and Treasury and Human Resources share one, Corporate Services, so its margin
gives only their sum, and any split of that pair still puts Human Resources first. The campus rates separate them: each restricted
division is the only blank on its campus. Converting a printed rate back to cases needs the matrix's convention, cases over accounts at
quarter start to two decimals per 1,000, which only reproducing the acknowledged divisions' printed figures reveals. Subtracting the
acknowledged counts from each campus then recovers every blank exactly: Treasury had 4 and 4 cases, 8.89 per 1,000 accounts.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Lateral-movement alerts per 1,000 accounts, last two quarters | A, Research Computing (70.0) | The SOC's detector, normalised for size | The provider's acknowledgements: 71% of A's escalations were closed as administrator activity |
| 1 | The scorecard's triage true-positive share, printed to the whole percent; four divisions at 100%; the policy's tie-break (criticality tier, then accounts) | B, Estates (tier 1, 6,200 accounts against F's 400) | An outcome measure, the policy's documented tie-break applied | The triage log: under the policy's rule that a figure is the lowest value consistent with every file of record, B's printed 100% is 199 of 200, and only F's 16 of 16 is exact, so the tie breaks |
| 2 | The provider's confirmed rate per 1,000 accounts from its line-level acknowledgements, the restricted divisions' blanks left out | C, Admissions (5.13) | The policy's own basis, from the counterparty's record, with nothing invented for the blanks | The matrix's campus rates: each restricted division is the only blank on its campus |
| 3 | **Decisive:** the matrix's convention recovered from the acknowledged divisions, then each restricted cell solved from its campus margin, cases over start-of-quarter accounts | **E, Treasury (8.89)** (5th of 8 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0 (41.1), 8th on rung 1 (67%) and is a blank on rung 2, and leads only rung 3, 1.19× F (7.50)
  and 1.73× C. Intermediate leaders hold margins of 1.33×, the tie-break's tier and accounts, and 1.37×.
* **Discriminator dominance.** Treasury is a blank at rung 2; read at the floor its print allows (one case a cell, 2.22 per 1,000), it
  trails C by 2.31×. Recovery multiplies Treasury's figure by 4.00 and leaves C's unchanged: an edge of 4.00 against the 1.2 × 2.31 = 2.77
  required, 1.44× headroom.
* **Partial correction priced (L3).** Filling the restricted blanks instead of solving them names F, because 400 accounts magnify any
  guess: at the midpoint (2.5 cases a cell) 12.5 per 1,000 against Treasury's 5.56, at the ceiling (4) 20.0 against 8.89, 2.25× both
  times. Solving from the functional groups alone leaves the Corporate Services pair: an even split names F (13.8 against 6.1, 2.25×), and
  a split by accounts gives both 8.46, where the tie-break names F (tier 1 against Treasury's tier 2). Applying the policy's rule to the
  scorecard but staying on triage shares names F as well, the only exact 100%. No half lands on E.
* **Grid.** Treatment of the restricted cells (omit, zero, midpoint, ceiling, functional pair split, campus recovery) × denominator (start
  or average accounts) gives twelve cells: omit and zero name C; midpoint, ceiling and both pair splits name F; campus recovery names E
  under either denominator, which give the same integers. The nearest wrong name, F, needs only the campus margins left unread.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The provider's note says cells of one to four cases print as "<5" for privacy. Nothing says the group or campus
   rates determine them, and nothing gives the rate convention.
2. **The corpus pins a construction, not a menu.** Cases over start-of-quarter accounts to two decimals reproduce all 13 printed figures
   built only from acknowledged divisions (7 division cells, 6 margins); average and end-of-quarter accounts reproduce 10 each, all three
   misses on Admissions' third quarter. The recovery is a construction: it needs that convention, the campus each restricted division sits
   alone in, and a subtraction of acknowledged counts, with no column holding a recovered count.
3. **No arithmetic symptom.** Every printed figure is consistent with every other; the blanks look like the privacy rule working as written.
4. **Not a row predicate.** It needs rates turned back into cases at the right denominator, campus totals less acknowledged members, and a
   rounding band resolved to an integer for each blank.
5. **The enumeration is arithmetic.** Each recovered count is the only integer inside a rounding band at most 0.15 cases wide; no field
   carries it.
6. **No cutover date.** Treasury's cases are spread across both quarters; no series steps.
7. **Survives deletion.** With every voice removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The provider's file: line-level acknowledgements for the six unrestricted divisions (every escalation with its outcome), and
  the quarterly matrix for all eight divisions, three functional groups and three campuses, with "<5" for any cell of one to four cases.
* **What it pins.** The rate convention, from reproducing the 13 printed figures the acknowledged divisions alone determine. Recovered
  counts: Treasury 4 and 4, Human Resources 2 and 1.
* **Twin pair.** Human Resources' third- and fourth-quarter cells are both printed "<5", with identical alerts (8), triage outcomes (8 of 8
  true positive) and accounts (400). They recover to 2 and 1 cases (2×).
* **Every rule exercised.** Corporate Services holds both restricted divisions, so its margin leaves a pair and the campus margins are
  needed; Admissions' accounts grew 2% within the third quarter, so the start-of-quarter denominator is tested on its printed figures.
* **Resemblance points at the decoy.** On every SOC-side column Treasury most resembles Legal and Compliance, whose acknowledged rate (2.5
  per 1,000) is the university's lowest.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The security policy: the hunt goes where confirmed lateral movement has been heaviest per 1,000 accounts over the last two
  quarters; a figure is the lowest value consistent with every file of record; ties go to the higher criticality tier, then to more
  accounts. The criticality register's tiers. The identity directory's accounts at each quarter start.
* **Empirical pins.** The matrix's rate convention, from the acknowledged divisions.
* **Voices.** The SOC lead: "The detector knows where the movement is; send the hunt where it fires hardest." The provider's account
  manager: "Restricted divisions are too small to matter, which is why their cells are suppressed."
* **Licensed wrong basis.** The policy records that the university's insurer scores divisions on acknowledged confirmed rates and will see
  the placement on that basis.

## 8. Determinism by construction

* **Integers.** Every recovered count is the unique integer within its rounding band under start-of-quarter or average accounts alike: the
  only division whose accounts moved within a quarter, Admissions, shares no campus with a restricted division.
* **Window.** The two quarters are filed, and Treasury's and Human Resources' accounts are the same at both quarter starts.
* **Margins.** Each restricted division is the only blank on its campus in both quarters, so no campus needs a second margin.
* **Accounts.** The directory's start-of-quarter counts are filed and never revised.

## 9. Prompt sketch and deliverables

> We can bring the external hunt team in for two weeks next term, and it works in one division. The SOC lead would send it wherever the
> lateral-movement detector fires hardest. Tell me the division and its confirmed rate, in a line for the security committee, with
> `hunt_placement.xlsx` holding the sheets below, the chart `confirmed_rates.png`, and a one-page `committee_note.pdf`.

* `hunt_placement.xlsx` — the division build with every recovered cell and the margin it came from, the MFA sheet (ask A), the phishing sheet
  (ask B) and the convention test (ask C).
* `confirmed_rates.png` — the eight divisions' confirmed rates per 1,000 accounts as bars, recovered cells hatched with their rounding bands as
  error bars, the midpoint and ceiling imputations marked as ghosts for the restricted divisions, and the chosen division highlighted.
* `committee_note.pdf` — the committed division and why the acknowledged ranking and the imputations are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each division, privileged accounts without multi-factor enrolment at quarter end, as a count
  and as a share of its people with privileged access. *Device:* the directory lists a person's standard and administrative accounts
  separately, linked by an owner ID, as its schema documents. Counting accounts as people overstates the share in the three divisions where
  administrators hold several accounts. The hunt placement uses account counts only as the matrix's denominators.
* **Ask B (device-carried).** For each month of the two quarters, phishing emails staff reported and the share the mail team confirmed
  malicious. *Device:* the report button files one report per recipient, and the mail team's log groups a campaign's reports under one
  campaign ID. Counting reports as emails overstates every month with a large campaign.
* **Ask C (validity).** For each of three rate conventions (start-of-quarter, average and end-of-quarter accounts), the printed figures it
  reproduces out of 13.
* **Decoupling.** Clearing the recovery changes no figure in asks A or B.

## 11. Rubric arithmetic

8 divisions × 2 (ask A) + 6 months × 2 (ask B) + 3 conventions (ask C) + the committed division, its rate and the four recovered cells + 5
named chart parts + 3 files ≈ 45 criteria.

## 12. World-building constraints

* Accounts: A 9,800, B 6,200, C 3,900 (3,980 from the fourth quarter), D 2,400, E 900, F 400, G 2,700, H 1,600. Half-year confirmed
  cases: 31, 22, 20, 6, 8, 3, 9, 6.
* Treasury (E) 4 and 4 cases, Human Resources (F) 2 and 1, all printed "<5". Campuses: City A and E; Park B, F and G; Riverside C, D and H.
  Corporate Services holds B, E and F.
* Rung leaders are A, B, C, E; E leads rung 3 by 1.19× over F and 1.73× over C; every fill and every pair split names F.
* Scorecard: A 300 of 301, B 199 of 200, C 200 of 201 and F 16 of 16 print 100%; B and F are tier 1, A, C and E tier 2.
* Human Resources' two quarterly cells are identical on every SOC-side column.
* Owner-linked accounts and campaign-grouped phishing reports never touch the provider's matrix or the alerts.

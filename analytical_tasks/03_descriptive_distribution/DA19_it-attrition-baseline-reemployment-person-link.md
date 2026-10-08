# DA19 — The attrition baseline a civil service files for its IT retention pilot, when moving between pay systems is booked as resigning

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · civil-service workforce planning |
| Mirrors | Attrition measured per legal employer when people move inside the group (Google, Amazon and Meta staff moving between subsidiaries with separate payrolls, contractors converted to employees under new IDs, bank and consulting staff re-hired across entities), where the HR system books an internal move as a leaver plus a new hire |
| Decision shape | One figure filed at a date: the FY2026 attrition rate of IT specialists, filed on 15 December 2026 in the retention-bonus pilot's charter as its baseline |
| Committed call | The rate, as a percentage to one decimal |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · E01, a reproduction-gated control set (the dashboard pilot's 15 published rates) whose only reproducing construction removes leavers back on another agency's rolls, found through the pension identity table, with E07 (the month-end rolls rebuilt from the action feed, against the September snapshots) below it |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #3 stops at a close but inexact match · #8 papers over a failed reproduction · #18 joins only on the visible key |
| Calibration form | Pilot log: the FY2025 release of the new attrition dashboard's pilot, 15 published rates (12 agencies and 3 occupational families) to two decimals, produced by a method no document spells out |
| Driving force | The standard counts losses to the civil service, and only one construction reproduces the pilot release. When a specialist moves between the four security agencies, which run their own pay system, and the rest of the service, the move is processed as a resignation and a new appointment under a new employee number. The separation file calls it a resignation, and the receiving agency books a new hire. Only the pension identity table, which carries each person's single civil-service number on every appointment, shows the same person back on the rolls days later. 692 of IT's 2,451 coded losses in FY2026 are such moves. The obvious construction reproduces 10 of the 15 published rates, and every miss is too high. |

## 1. Situation

A national civil service will pay retention bonuses to IT specialists in a pilot starting in January 2027. The pilot's charter files a
baseline attrition rate for FY2026 (October 2025 to September 2026), and the bonus fund is sized on it. The workforce office's
statistical standard says a published rate counts losses to the civil service over the year, divided by the average of the thirteen
month-end rolls, and may be published only by a method that reproduces every rate in the FY2025 pilot release. The pack holds the
separation file, the personnel-action feed (every appointment, move and separation, to 30 November 2026), the 30 September snapshots for
2025 and 2026, the pension identity table, the pilot release, the standard and the dashboard's own rates.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: separations and their codes, the action feed, the snapshots, the identity table and the pilot
  release. A cross-system move really is a resignation in the sending agency's books, and the dashboard's rates are right on its own
  convention. Nobody's reading of their own numbers is overturned. The difficulty is what a loss to the civil service is.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the CIO's view, the head of analytics' view and the budget office's basis. The separation file still codes
  692 moves as resignations, and the obvious construction still reproduces 10 of the 15 published rates.
* **Instrument repair.** Perfect the separation file and the moves are still resignations, because two pay systems cannot transfer a
  person between them. The person is joined across appointments only by the pension identity table.
* **Lens swap.** The two reads count different populations: 2,451 people who left an agency against 1,759 who left the civil service.

## 3. The driving force

A strong solver reads the standard and builds it faithfully. It counts resignations, retirements, dismissals and other losses,
excluding the codes for transfers, deaths and expired fixed-term appointments. It rebuilds the thirteen month-end rolls from the action
feed instead of averaging the two September snapshots, which matters because the Tax Agency carries 4,800 fixed-term IT staff from January
to August. Then it checks the pilot release and reproduces ten rates to the hundredth. The five misses (the four security agencies, the
Digital Services Office and the IT family) are all too high, by 0.6 to 3.1 points, and the head of analytics calls them rounding. They
are not. A move across the pay-system boundary cannot be booked as a transfer, so it is a resignation followed by a new appointment, with
a new employee number. The identity table gives every appointment the person's civil-service number. Joined through it, 692 of IT's
FY2026 leavers were back on another agency's rolls within nine days. They were never lost.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The dashboard: resignations, retirements, dismissals and transfers out, over the 30 September 2026 headcount | 15.8% (+97.5%) | The office's own published convention, on its own snapshot | The standard: transfers between agencies are not losses, and the denominator is the year's average roll |
| 1 | Coded losses (transfers, deaths and expiries excluded) over the average of the two September snapshots | 12.9% (+61.3%) | The standard's loss codes and an average headcount | The pilot release: the snapshot average reproduces 4 of 15 rates, missing every agency with fixed-term seasonal staff |
| 2 | Coded losses over the average of the thirteen month-end rolls rebuilt from the action feed (E07) | 11.1% (+38.8%) | Reproduces 10 of the 15 published rates to the hundredth | The identity table: 692 IT leavers coded as resigning reappear on another agency's rolls under the same civil-service number within nine days |
| 3 | **Decisive:** coded losses less leavers back on any agency's rolls (identity table), over the month-end average (E01) | **8.0%** | — | — |

* **Figure shape.** Every correction lowers the figure, and the answer is the minimum cell. A charter filed at any lower rung sizes the
  bonus fund on losses that never left the service, and judges the pilot against a baseline it can only appear to beat.
* **Partial correction priced (L3).** A solver who removes the moves but keeps the snapshot average lands at 9.3% (+16.3%). One who uses
  the 30 September 2026 headcount lands at 9.0% (+12.5%). One who looks for moves in the receiving agency's accession codes finds none,
  because the receiving agency books a new appointment, and stays at 11.1%. The separation file carries no names or birth dates, so
  there is no fuzzy route to the moves.
* **Grid.** Denominator (September headcount, snapshot average, month-end average) × numerator (dashboard codes, loss codes, loss codes
  less moves) gives 9 cells, from 8.0% to 16.3%. The nearest wrong cell is 9.0% (+12.5%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard defines losses to the civil service through the separation codes and excludes the transfer code.
   The HR manual says employee numbers are issued per appointment. No document says that a move across pay systems is booked as a
   resignation, and none connects the identity table to attrition.
2. **Reproduction, and why it is a construction.** Removing the moves reproduces all 15 published rates. The month-end construction
   reproduces 10, the snapshot average 4 and the dashboard none. Every rival miss is too high, so no rival reconciles on the families'
   totals either. The reproducing rule is a join from each leaver's employee number to the person's civil-service number and on to any
   later appointment. No code, threshold or parameter reaches it.
3. **No arithmetic symptom.** Separations reconcile to the action feed, the rebuilt rolls tie to both snapshots, and every employee
   number is unique. The moves look like a resignation in one agency and an ordinary hire in another.
4. **Not a row predicate.** Whether a leaver was lost depends on another agency's later appointment, reached through a third table.
5. **The enumeration is arithmetic.** 692 IT moves in FY2026 and 2,310 across the service are found by the join. No field marks them.
6. **No cutover date.** Moves across the pay-system boundary happen in every month, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the obvious construction still reproduces ten rates.

## 6. The calibration corpus

* **Form.** The pilot release: the dashboard pilot's FY2025 attrition rates for the 12 agencies and the IT, finance and general
  administrative families, to two decimals. The standard makes reproducing all 15 the condition of publishing any rate.
* **What it pins.** The month-end denominator, through the agencies with seasonal staff, and the removal of moves, through the four
  security agencies, the Digital Services Office and the IT family. Each rule has cells that break without it.
* **Twin pair.** The Land Registry and the Digital Services Office are identical on every column of the separation file, the action feed
  and the snapshots: a month-end average of 2,400 and 236 coded losses each. Their published rates are 9.83% and 4.92% (2.0×), because
  118 of the Digital Services Office's leavers were back in a security agency within nine days. Every rival construction gives both
  9.83%.
* **Resemblance points at the decoy.** On every personnel column, the IT family most resembles the general administrative family, whose
  published rate the month-end construction reproduces exactly.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The standard: "A published attrition rate counts losses to the civil service over the year, divided by the average of
  the thirteen month-end rolls from 30 September to 30 September. Transfers between agencies, deaths and the expiry of fixed-term
  appointments are not losses. A rate may be published only by a method that reproduces every rate in the FY2025 pilot release." The
  charter fixes the IT family by occupational series.
* **Empirical pins.** The removal of moves, from the pilot release.
* **Voices.** The CIO: "We lose our best IT people to industry every year." The head of workforce analytics: "Our dashboard has counted
  resignations faithfully for years; the pilot's figures only round differently."
* **Licensed wrong basis.** The standard records that the budget office sizes retention funds on the dashboard's separation rate and will
  compare the charter's baseline with it.

## 8. Determinism by construction

* **Window.** Every move puts the person on another agency's rolls 2 to 9 days after the resignation, and no FY2026 leaver reappears
  between day 10 and the end of the feed, so any window from 9 days to 60 gives the same 692.
* **Censoring.** The feed runs to 30 November 2026, so the 60 days after every FY2026 separation are observed.
* **Appointments.** No IT specialist holds two appointments at once, and no retiree is re-employed within the feed, so the rolls count
  people and no other re-entry exists.
* **Denominator.** The thirteen month-ends are pinned by the standard, and the rebuilt rolls tie to both snapshots.
* **Family.** The charter's occupational series fix the IT family, and no person changes series during the year.

## 9. Prompt sketch and deliverables

> The IT retention-bonus pilot starts in January, and its charter needs a baseline: our IT specialists' attrition rate for FY2026, which
> also sizes the bonus fund. The CIO is convinced we lose our best IT people to industry every year. Give me the rate as a percentage to
> one decimal, in a sentence for the charter, and send `attrition_baseline.xlsx` with the sheets below and a chart
> `it_rolls_and_losses.png`.

* `attrition_baseline.xlsx` — the IT rate under each rung's construction with its losses and denominator, the pilot release
  reproduction for each construction (ask C), the sick-leave sheet (ask A) and the training sheet (ask B).
* `it_rolls_and_losses.png` — IT's thirteen month-end rolls against the two September snapshots, monthly coded losses with the moves
  stacked in a separate colour, the committed rate, and the Land Registry's and the Digital Services Office's published rates against
  each construction.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Sick-leave days by agency and quarter of FY2026. *Device:* an absence spanning a quarter end is
  one record with start and end dates, as the leave guide documents. Booking it in its start quarter misplaces 8% of days and moves 21 of
  the 48 cells.
* **Ask B (device-carried).** Course completions by agency and quarter of FY2026. *Device:* a blended course completes only when both its
  online module and its classroom day are recorded, and each part writes its own record, as the learning-system guide documents.
  Counting records as completions overstates 26 of the 48 cells, by up to double.
* **Ask C (validity).** The IT rate under each of the four rung constructions, each construction's reproduction count on the pilot
  release, and the Land Registry's and the Digital Services Office's rates under the decisive construction.
* **Decoupling.** Leave and training records share no row with the separation file, the action feed or the identity table. Clearing the
  removal of moves changes no figure in asks A or B.

## 11. Rubric arithmetic

12 agencies × 4 quarters (ask A) + 12 agencies × 4 quarters (ask B) + 4 rung rates, 4 reproduction counts and 2 twin rates (ask C) + the
committed rate, its losses and its denominator + 4 named chart parts + 2 files ≈ 115 criteria.

## 12. World-building constraints

* IT, FY2026: 2,451 coded losses, 640 coded transfers out, 692 moves among the coded losses; snapshots 18,400 (2025) and 19,600 (2026);
  month-end average 22,000 with the Tax Agency's 4,800 fixed-term staff on the rolls January to August.
* Rates: 15.8 / 12.9 / 11.1 / 8.0%; other grid cells 12.5, 16.3, 14.0, 9.3 and 9.0%.
* Pilot release: the decisive construction 15 of 15, month-end 10, snapshot average 4, dashboard 0; every miss too high.
* The Land Registry and the Digital Services Office are identical on every personnel column (2,400 average, 236 coded losses); 118 of
  the latter's are moves.
* Every move reappears in 2 to 9 days. No names or birth dates ship on separations.
* Leave and training records touch no personnel action.

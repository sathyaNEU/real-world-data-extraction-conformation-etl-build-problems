# DA19 — The attrition baseline a civil service files for its IT retention pilot, when fixed-term specialists leave for the mandatory break and come back

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · civil-service workforce planning |
| Mirrors | Attrition counted per worker record when tenure caps force a break between assignments (Microsoft's and Google's vendor and temporary staff capped at 18 to 24 months with a mandatory gap, Amazon's seasonal re-hires, gig platforms' deactivated and reactivated couriers), where every assignment end reads as a leaver and the return as a new hire under a new worker ID |
| Decision shape | One figure filed at a date: the FY2026 attrition rate of IT specialists, filed on 15 December 2026 in the retention-bonus pilot's charter as its baseline |
| Committed call | The rate, as a percentage to one decimal |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · E01, a reproduction-gated control set (the dashboard pilot's 15 published rates) whose only reproducing construction treats a fixed-term expiry as no loss when the same person is re-appointed after the employment code's mandatory break, the person linked across appointment numbers only through the pension identity table, with E07 (the average roll at month-end grain rebuilt from the action feed, against the September snapshots) below it |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #3 stops at a close but inexact match · #8 papers over a failed reproduction · #18 joins only on the visible key |
| Calibration form | Pilot log: the FY2025 release of the new attrition dashboard's pilot, 15 published rates (12 agencies and 3 occupational families) to two decimals, produced by a method no document spells out |
| Driving force | The standard counts losses to the civil service, and only one construction reproduces the pilot release: an expiry is no loss when the same person comes back after the break. The employment code forbids renewing a fixed-term appointment in place. A specialist whose appointment ends must stay off every roll for at least 30 days, and a re-appointment then opens under a new appointment number. The separation file truthfully records an expiry, and the action feed truthfully records a new appointment. Only the pension identity table, which carries one civil-service number across appointments, links the two. 830 of IT's 1,130 FY2026 expiries are such chains. The obvious construction reproduces 10 of the 15 published rates, and every miss is too high. |

## 1. Situation

A national civil service will pay retention bonuses to IT specialists in a pilot starting in January 2027. The pilot's charter files a
baseline attrition rate for FY2026 (October 2025 to September 2026), and the bonus fund is sized on it. The workforce office's
statistical standard says a published rate counts the year's losses to the civil service against the year's average roll, and may be
published only by a method that reproduces every rate in the FY2025 pilot release. The pack holds the separation file, the
personnel-action feed (every appointment, series change and separation, to 30 November 2026), the 30 September snapshots for 2025 and
2026, the pension identity table, the employment code, the pilot release, the standard and the dashboard's own rates. Each summer the
Tax Agency moves 4,800 contact-centre staff into the IT service-desk series for the lodgement season, July to October.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: separations and their codes, the action feed, the snapshots, the identity table and the pilot
  release. An expiry really ends an appointment and the person really leaves the rolls, and the dashboard's rates are right on its own
  convention. Nobody's reading of their own numbers is overturned. The difficulty is what a loss to the civil service is.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the CIO's view, the head of analytics' view and the budget office's basis. The 830 expiries are still
  expiries, and the obvious construction still reproduces 10 of the 15 published rates.
* **Instrument repair.** Clean-data test. The suspect file is the personnel-action feed, which is delta-shaped: eleven of the thirteen
  month-end rolls exist only as rebuilt from it, and the 30 September snapshots cover the other two. Repair it by shipping all thirteen
  month-end snapshots. Rung 1 moves to 12.9%, rung 2's figure. Rung 0 stays at 10.3% and rung 2 at 12.9%. No other file is suspect.
  Every separation code records what happened: each of the 830 expiries ended a real appointment, and the person was off every roll for
  31 to 45 days. Even a leaver register that recorded directly who left the civil service would list all 830 and leave rung 2 at 12.9%.
  The answer stays 8.5%, and the chain of spells through the identity table is still needed, because whether a leaver comes back is a
  fact about a later appointment, not about the separation.
* **Lens swap.** The two reads count different populations: 2,451 appointments that ended in a loss code against 1,621 people the
  service lost. The 830 people who left for the break and came back are in one count and not the other.

## 3. The driving force

A strong solver reads the standard and builds it faithfully. It counts resignations, retirements, dismissals and expiries, excluding
transfers and deaths. It sees that the September snapshots catch the lodgement-season reassignment, and it rebuilds the thirteen
month-end rolls from the action feed instead of averaging the two snapshots. Then it checks the pilot release and reproduces ten rates
to the hundredth. The five misses (the Digital Services Office, the Statistics Office, the Courts Service, the Health Department and
the IT family) are all too high, by 0.7 to 4.9 points, and the head of analytics calls them rounding. They are not. These four
agencies staff their IT projects on fixed-term appointments, and the employment code forbids renewing one in place. When a project
runs on, the appointment expires, the specialist stays off every roll for at least 30 days, and a new appointment opens under a new
appointment number. Joined through the identity table, which gives every appointment the person's civil-service number, 830 of IT's
FY2026 expiries were followed by a re-appointment of the same person 31 to 45 days later. The service never lost them.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The dashboard: resignations, retirements, dismissals and transfers out, over the 30 September 2026 headcount | 10.3% (+20.4%) | The office's own published convention, on its own snapshot | The standard: an expiry is a way of leaving and a transfer is not, and the denominator is the year's average roll |
| 1 | Coded losses (expiries in; transfers and deaths out) over the average of the two September snapshots | 11.1% (+30.6%) | The standard's losses over the textbook average roll, opening and closing headcount | The pilot release: the snapshot average reproduces 4 of 15 rates, missing the IT and general administration families, whose rolls swing with the lodgement season |
| 2 | Coded losses over the average of the thirteen month-end rolls rebuilt from the action feed (E07) | 12.9% (+51.2%) | Reproduces 10 of the 15 published rates to the hundredth | The identity table: 830 IT expiries were followed, 31 to 45 days later, by a new appointment under the same civil-service number |
| 3 | **Decisive:** coded losses less expiries whose person is re-appointed after the break (identity table), over the month-end average (E01) | **8.5%** | — | — |

* **Figure shape.** The corrections walk the figure up, from 10.3% to 12.9%, and the decisive move reverses them to 8.5%, below every
  rung. A charter filed at rung 2 sizes the bonus fund on 830 specialists who were back within six weeks, and judges the pilot against a
  baseline it can only appear to beat.
* **Partial correction priced (L3).** Removing the chains over the snapshot average lands at 7.4% (−13.6%), and over the September
  headcount at 7.2% (−15.9%). Linking expiries to new appointments through the post number finds only the 210 re-appointments made to the
  old post, and lands at 11.8% (+38.2%). Dropping every expiry, as many dashboards do and the standard forbids, lands at 7.0% (−18.5%).
  Looking for returns in the action feed's hire codes finds none, because a re-appointment is booked as a new appointment, and stays at
  12.9%. The separation file carries no names or birth dates, so there is no fuzzy route to the chains.
* **Grid.** Numerator (dashboard codes, loss codes, loss codes less chains, loss codes less every expiry) × denominator (September
  headcount, snapshot average, month-end average) gives 12 cells, from 5.9% to 12.9%. The nearest wrong cell is 7.4% (−13.6%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard lists the ways of leaving and excludes transfers and deaths. The employment code sets the 30-day
   break for an operational reason, to stop fixed-term staff accruing a claim to permanence. The HR manual says appointment numbers are
   issued per appointment. No document connects the break or the identity table to attrition, or says a re-appointed person was not lost.
2. **Reproduction, and why it is a construction.** Removing the chains reproduces all 15 published rates. The month-end construction
   reproduces 10, the snapshot average 4 and the dashboard none. Every miss of the month-end construction is too high, so it cannot
   reconcile on the families' totals either. The reproducing rule is a join from each expiry's appointment number to the person's
   civil-service number and on to any later appointment of that person. No code, threshold or parameter reaches it.
3. **No arithmetic symptom.** Separations reconcile to the action feed, the rebuilt rolls tie to both snapshots, and every appointment
   number is unique. A chain looks like an ordinary expiry in one month and an ordinary new appointment six weeks later.
4. **Not a row predicate.** Whether an expiry was a loss depends on a later appointment of the same person, reached through a third
   table, in any agency.
5. **The enumeration is arithmetic.** 830 IT chains in FY2026 and 2,940 across the service are found by the join. No field marks them.
6. **No cutover date.** Fixed-term appointments end every March and June, the break rule has stood for twenty years, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the obvious construction still reproduces ten rates.

## 6. The calibration corpus

* **Form.** The pilot release: the dashboard pilot's FY2025 attrition rates for the 12 agencies and the IT, finance and general
  administration families, to two decimals. The standard makes reproducing all 15 the condition of publishing any rate.
* **What it pins.** The month-end average roll, through the two families whose rolls swing with the lodgement season, and the removal of
  chains, through the four agencies that staff IT projects on fixed-term appointments and the IT family. Each rule has cells that break
  without it.
* **Twin pair.** The Land Registry and the Statistics Office are identical on every column of the separation file, the action feed and
  the snapshots: a month-end average of 2,400, 236 coded losses including 130 expiries, and 130 new appointments each. Their published
  rates are 9.83% and 4.92% (2.0×). 118 of the Statistics Office's new appointments re-appointed its own expired specialists after the
  break, while the Land Registry's were outside recruits and its expired staff left. Every rival construction gives both 9.83%.
* **Resemblance points at the decoy.** On every personnel column, the IT family most resembles the finance family, which has no
  fixed-term chains and whose published rate the month-end construction reproduces exactly.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The standard: "A published attrition rate counts the year's losses to the civil service against the year's average
  roll. Resignation, retirement, dismissal and the end of a fixed-term appointment are ways of leaving; a transfer between agencies and a
  death in service are not losses. A rate may be published only by a method that reproduces every rate in the FY2025 pilot release." The
  employment code: "A fixed-term appointment may not be renewed. Its holder may be appointed again after a break of at least 30 days."
  The charter fixes the IT family by occupational series.
* **Empirical pins.** The month-end average and the removal of chains, from the pilot release.
* **Voices.** The CIO: "We lose our best IT people to industry every year." The head of workforce analytics: "Our dashboard has counted
  separations faithfully for years; the pilot's figures only round differently."
* **Licensed wrong basis.** The standard records that the budget office sizes retention funds on the dashboard's separation rate and
  will compare the charter's baseline with it.

## 8. Determinism by construction

* **Window.** Every re-appointment comes 31 to 45 days after the expiry, and no FY2026 leaver of any kind is appointed again between day
  46 and the end of the feed, so any window from 45 days to the feed's end gives the same 830.
* **Censoring.** IT fixed-term appointments end on 31 March or 30 June, so every FY2026 expiry's following 45 days fall inside the year
  and inside the feed.
* **Other returns.** No resignation, retirement or dismissal is followed by an appointment of the same person within the feed, and no IT
  specialist holds two appointments at once.
* **Denominator.** The rebuilt month-end rolls tie to both snapshots. People on a break are off the rolls in every construction. The
  reassigned Tax Agency staff count while they are in the IT series, and none of them separates while there.
* **Family.** The charter's occupational series fix the IT family at each month-end, and every re-appointed specialist returns to an IT
  series.

## 9. Prompt sketch and deliverables

> The IT retention-bonus pilot starts in January, and its charter needs a baseline: our IT specialists' attrition rate for FY2026, which
> also sizes the bonus fund. The CIO is convinced we lose our best IT people to industry every year. Give me the rate as a percentage to
> one decimal, in a sentence for the charter, and send `attrition_baseline.xlsx` with the sheets below and a chart
> `it_rolls_and_losses.png`.

* `attrition_baseline.xlsx` — the IT rate under each rung's construction with its losses and denominator, the pilot release
  reproduction for each construction (ask C), the sick-leave sheet (ask A) and the training sheet (ask B).
* `it_rolls_and_losses.png` — IT's thirteen month-end rolls against the two September snapshots with the lodgement season shaded,
  monthly coded losses with the expiries that came back stacked in a separate colour, the committed rate, and the Land Registry's and
  the Statistics Office's published rates against each construction.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Sick-leave days by agency and quarter of FY2026. *Device:* an absence spanning a quarter end is
  one record with start and end dates, as the leave guide documents. Booking it in its start quarter misplaces 8% of days and moves 21 of
  the 48 cells.
* **Ask B (device-carried).** Course completions by agency and quarter of FY2026. *Device:* a blended course completes only when both its
  online module and its classroom day are recorded, and each part writes its own record, as the learning-system guide documents.
  Counting records as completions overstates 26 of the 48 cells, by up to double.
* **Ask C (validity).** The IT rate under each of the four rung constructions, each construction's reproduction count on the pilot
  release, and the Land Registry's and the Statistics Office's rates under the decisive construction.
* **Decoupling.** Leave and training records share no row with the separation file, the action feed or the identity table. Clearing the
  removal of chains changes no figure in asks A or B.

## 11. Rubric arithmetic

12 agencies × 4 quarters (ask A) + 12 agencies × 4 quarters (ask B) + 4 rung rates, 4 reproduction counts and 2 twin rates (ask C) + the
committed rate, its losses and its denominator + 4 named chart parts + 2 files ≈ 115 criteria.

## 12. World-building constraints

* IT, FY2026: 920 resignations, 360 retirements, 41 dismissals, 1,130 expiries (830 followed by re-appointment of the same person), 1,000
  transfers out and 19 deaths. Coded losses 2,451; people lost 1,621.
* Rolls: September headcount 21,400 (2025) and 22,600 (2026), both with the 4,800 reassigned staff; month-end average 19,000, with the
  reassigned staff in the IT series at 5 of the 13 month-ends.
* Rates: 10.3 / 11.1 / 12.9 / 8.5%; other grid cells 5.9, 6.0, 7.0, 7.2, 7.4, 10.6, 10.8 and 12.2%; post-number partial 11.8%.
* Pilot release: the decisive construction 15 of 15, month-end 10, snapshot average 4, dashboard 0; every month-end miss too high.
* The Land Registry and the Statistics Office are identical on every personnel column (2,400 average, 236 coded losses, 130 expiries,
  130 new appointments); 118 of the latter's new appointments are re-appointments after the break.
* Every re-appointment falls 31 to 45 days after its expiry. No names or birth dates ship on separations.
* Leave and training records touch no personnel action.

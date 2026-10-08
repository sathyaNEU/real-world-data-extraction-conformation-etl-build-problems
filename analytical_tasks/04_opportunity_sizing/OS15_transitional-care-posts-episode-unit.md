# OS15 — How to place 30 transitional-care nurses across five hospitals, when much of the worst readmission rate is patients sent across town the next day

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Policy & Education · health-system administration |
| Mirrors | Allocating a follow-up or retention team across business units when the unit the programme serves is a journey that crosses units (support cases transferred between Amazon or Apple teams, Google Cloud incidents handed between on-call rotations, Meta integrity cases escalated across queues), and row-level counts score each handoff as a failure |
| Decision shape | An allocation under a cap: 30 funded nurse posts placed across five hospitals in whole posts |
| Committed call | The posts each hospital receives, and the readmissions a year the programme avoids, to the nearest five |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · S1, the unit the programme serves is not stored (#2), pinned by the counterparty's episode numbers, with finer published controls (#12) separating effect-transport constructions below it |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #2 counts file rows instead of the real unit · #12 stops at the first control that passes · #13 validates on one population, applies to another |
| Calibration form | Counterparty acknowledgement file: the Medicaid managed-care plan's acknowledgements for every stay it paid, each carrying the plan's episode number |
| Driving force | The programme serves index discharges, the moment a patient goes home at the end of an acute episode, and the discharge file holds stays. When St Anne's or Lakeview sends a patient across town the next day, the file shows a discharge and a 30-day readmission, though the patient went home from Central. Chained by patient across the system's hospitals with a one-day gap, which the plan's episode numbers confirm 6,412 of 6,412 times, the community hospitals' readmission rates fall by half or more and Central holds the highest-risk episodes. |

## 1. Situation

A five-hospital system has funded 30 transitional-care nurse posts for next year: Riverside, St Anne's and Lakeview are community
hospitals, while Northgate and Central are tertiary centres. The programme charter allocates posts in proportion to each hospital's
expected avoidable readmissions, in whole posts, and says the programme serves index discharges. Last year's pilot at Harbour General
cut 30-day readmissions from 24.0% to 19.8%, and its report also gives results by risk tier. The discharge file holds every stay with a
risk tier and the system-wide patient number. The Medicaid managed-care plan acknowledges each stay it pays with its own episode number.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the stays, the readmission flags, the pilot's results, the tier labels and the plan's episode
  numbers. St Anne's really does have the highest stay-level readmission rate. No stakeholder read is overturned. The difficulty is the
  unit the programme serves, which no file stores.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete every voice. The stay-level file and the pilot's by-tier effects still produce a confident split with
  Lakeview on top.
* **Instrument repair.** Code every stay's disposition perfectly. A patient sent home and admitted elsewhere the next day is still two
  stays; only chaining by patient makes them one episode.
* **Lens swap.** The naive read counts stays; the answer counts episodes ending at each hospital, a different population built by
  linking stays across hospitals.

## 3. The driving force

A strong solver rejects the planning team's flat 4.2 points: the pilot's result is relative, and its report shows the effect is strong
for high-risk patients (36.0% to 27.2%) and nil for low-risk ones. It applies those tier effects to each hospital's stays by tier, and
Lakeview, with the most high-risk readmissions, leads. But the charter's unit is the index discharge. The community hospitals send
patients to the tertiary centres for procedures, often coded as discharges home and admitted at Central the next morning, so the stay
file scores each transfer as a readmission. Chained by patient with a one-day gap, Riverside's readmission rate falls from 34% to 16%
and St Anne's from 55% to 18%. Central, where those episodes end, holds the highest-risk index discharges in the system.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Stays × the pilot's 4.2-point reduction | Riverside leads (8 posts); 1,021 avoided (+63%) | The planning team's method on the discharge file | The pilot report: the effect is relative (24.0% to 19.8%), so it scales with each hospital's own rate |
| 1 | Stays × each hospital's readmission rate × the pilot's relative reduction | St Anne's leads (9, 1.26× over Riverside); 1,606 (+157%) | Reproduces the pilot's headline result and uses each hospital's own rate | The pilot report's by-tier results: 36.0% to 27.2% high-risk, 20.0% to 18.4% medium, 8.0% unchanged low |
| 2 | Stays by tier × tier readmission rates × the tier effects | Lakeview leads (9, 1.61× over St Anne's); 1,201 (+92%) | Reproduces the pilot's headline and all three tier results | The charter's unit, with the plan's episode numbers: stays chained by patient with a gap of a day or less form one episode, 6,412 of 6,412 |
| 3 | **Decisive:** index episodes by tier (stays chained by patient across hospitals, a readmission being a new episode within 30 days) × tier effects | **Riverside 4 · St Anne's 3 · Lakeview 7 · Northgate 5 · Central 11; 625 avoided** | — | — |

* **Position table.** Central ranks 5th on rung 0, 4th on rung 1 and 3rd on rung 2, and leads only rung 3 (1.42× over Lakeview).
* **Discriminator dominance.** Lakeview carries a 1.61× advantage into rung 3 (379 against 235 avoidable at stay grain). Chaining keeps
  0.96 of Central's figure and 0.42 of Lakeview's, an edge of 2.30×, above the 1.93× floor. Product: 2.30 / 1.61 = 1.42.
* **Partial correction priced (L3).** A solver who builds episodes but keeps the pilot's single relative reduction lands at 693 avoided
  (+10.6%) and misplaces 4 posts. One who links stays only through the transfer disposition code reproduces 5,010 of the plan's 6,412 episodes
  and still scores every home-coded next-day admission as a readmission. One who builds episodes with the flat 4.2 points names Riverside.
* **Grid.** Unit (stays, episodes) × effect (absolute, relative, by tier) gives 6 cells: Riverside, St Anne's and Lakeview at stay grain;
  Riverside, Central (+10.6%, 4 posts misplaced) and the answer at episode grain. Every leader is at least 1.26× clear.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The charter says the programme serves index discharges and that stays linked by a transfer form one episode.
   It does not say what links them, and the disposition code is the obvious reading.
2. **Reproduction, not a menu.** Chaining by patient with a gap of a day or less reproduces 6,412 of the plan's 6,412 episode groupings.
   Disposition-code linking reproduces 5,010, and every miss is a stay coded home and followed by an admission elsewhere the next day. The
   rule is a construction: stays ordered within each patient across five hospitals, gaps measured, chains cut, readmissions attributed to
   the chain's final hospital. No column holds the episode.
3. **No arithmetic symptom.** Stays reconcile to each hospital's census, readmission flags to the quality dashboard, and the pilot's results
   reproduce under rungs 1 to 3.
4. **Not a row predicate.** An episode needs a group per patient, an order within it, a gap rule, and a reassignment of every readmission
   to the hospital where the episode ended.
5. **The enumeration is arithmetic.** Episodes are built for 24,310 stays; nothing flags a stay as a transfer when it was coded home.
6. **No cutover date.** Transfer patterns are stable across the year, and no series steps.
7. **Survives deletion.** Removing every voice leaves the stay file and the pilot certifying rung 2.

## 6. The calibration corpus

* **Form.** The plan's acknowledgement file: every Medicaid stay it paid last year (30% of all stays), each with the plan's episode number.
* **What it pins.** The chaining rule (above), 6,412 of 6,412. The rule is then applied to every payer's stays through the system-wide
  patient number.
* **The pilot report's finer controls.** The headline (24.0% to 19.8%) is reproduced by the absolute, relative and by-tier constructions;
  only by-tier effects reproduce the three tier results.
* **Twin pair.** Riverside's and St Anne's cardiology services are identical on stays (1,200), tier mix and stay-level readmission rate
  (39.7%). Riverside's 476 readmissions include 120 next-day transfers; St Anne's include 300. The programme would avoid 87 a year at
  Riverside and 43 at St Anne's, 2.0× apart, separated only by chaining.
* **Resemblance points at the decoy.** By tier mix and stay-level rate, Lakeview most resembles Harbour General, the pilot hospital.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The charter: the programme serves index discharges; stays linked by a transfer form one episode; a readmission is a new
  episode within 30 days of an index discharge; posts are allocated in proportion to each hospital's expected avoidable readmissions, in
  whole posts by largest remainder. The pilot report, with its headline and tier results.
* **Empirical pins.** The chaining rule, from the plan's episode numbers. Tier effects, from the pilot report.
* **Voices.** The chief medical officer: "Riverside discharges more patients than anyone, so that is where the nurses go." The quality
  lead: "St Anne's has the worst readmission rate in the system."
* **Licensed wrong basis.** The charter records that the state hospital association benchmarks transitional-care staffing on discharges
  and will present that split to the board.

## 8. Determinism by construction

* **Gap rule.** No two stays of one patient are separated by two or three days, so gap thresholds of one, two or three days build the same
  chains.
* **Tiers.** Every stay in a chain carries the same risk tier, so an episode's tier does not depend on which stay supplies it.
* **Linkage.** The system-wide patient number is on every stay, and the plan's episode numbers cover every Medicaid stay.
* **Planned admissions.** Planned readmissions carry a filed flag and are excluded under every construction.
* **Rounding.** The answer is 626 avoided readmissions, mid-bin at the nearest five, and no hospital's post quota sits within 0.03 of a
  remainder tie.

## 9. Prompt sketch and deliverables

> We've funded 30 transitional-care nurse posts for next year, and I have to place them across our five hospitals. Our chief medical
> officer's view is that they belong where we discharge the most patients. Tell me how many posts each hospital gets and how many
> readmissions a year the programme should avoid, to the nearest five, in a form I can put to the board. Send `nurse_posts.xlsx`, a chart
> `avoidable_by_hospital.png`, and a short `board_paper.docx`.

* `nurse_posts.xlsx` — each hospital's stays, episodes, readmission rates and avoidable readmissions by tier on four bases, the vacancy
  sheet (ask A) and the referral sheet (ask B).
* `avoidable_by_hospital.png` — a script-rendered paired bar chart: each hospital's avoidable readmissions at stay grain and at episode
  grain, split by tier, with the post allocation printed above each pair and next-day transfers shaded within the stay-grain bars.
* `board_paper.docx` — the committed posts, the avoided-readmissions figure, and why each hospital's share moves.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each hospital, last year's median days to fill a nursing vacancy and the share open over 90
  days. *Device:* a requisition reposted after a failed hire keeps its number with a new posting date, and the recruitment guide times a
  fill from the original posting. Timing from the latest posting understates days to fill at three hospitals.
* **Ask B (device-carried).** For each of the six home-health agencies, the share of referrals accepted within 48 hours. *Device:* a
  referral re-sent after a decline is logged as a new referral carrying `original_referral_id`, and the referral guide scores the original.
  Counting re-sends as new referrals overstates acceptance at the two agencies that decline most.
* **Ask C (validity).** Each hospital's avoidable readmissions and posts under each of the four rung bases, and the plan's episodes
  reproduced under patient chaining, disposition linking and same-hospital linking.
* **Decoupling.** Counting stays instead of episodes changes no figure in asks A or B. Requisitions and home-health referrals touch neither
  the stay file nor the plan's acknowledgements.

## 11. Rubric arithmetic

5 hospitals × 2 (ask A) + 6 agencies × 2 (ask B) + 5 hospitals × 4 bases × 2 figures and 3 reproduction counts (ask C) + the post vector
(5) and the avoided figure + 5 named chart parts + 3 files ≈ 79 criteria.

## 12. World-building constraints

* Episodes ending at each hospital by tier (high, medium, low): Riverside 500 / 2,080 / 2,620; St Anne's 450 / 1,200 / 1,200; Lakeview
  1,600 / 1,100 / 700; Northgate 900 / 1,600 / 1,300; Central 2,400 / 900 / 500. Next-day transfers out: Riverside 400 / 700 / 400; St
  Anne's 200 / 1,600 / 600; Lakeview 800 / 300 / 100; Northgate 50 / 40 / 10; Central 30 / 20 / 10.
* Episode readmission rates by tier 36%, 20%, 8%; tier effects 0.755, 0.92, 1.00 (the pilot's 24.0% to 19.8% at a 40 / 40 / 20 mix).
* Rung leaders Riverside, St Anne's, Lakeview, Central at 1.28×, 1.26×, 1.61×, 1.42×; posts by rung as in the ladder.
* The two cardiology services match on every stay-level column.
* Requisitions and home-health referrals never touch stays, episodes or acknowledgements.

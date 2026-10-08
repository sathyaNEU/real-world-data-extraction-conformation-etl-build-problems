# OS36 — Where 1,200 discharge-to-assess packages go this winter, when most "delayed" patients already had their care arranged

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Policy & Education · health and social-care administration |
| Mirrors | Capacity a fast-track route frees when much of the queue was about to clear anyway (right-sizing tools credited with savings the autoscaler would have made, expedited shipping that only beats goods already dispatched, priority support that closes tickets an existing fix was about to resolve) |
| Decision shape | An allocation under a cap: 1,200 council-funded packages across six hospitals |
| Committed call | Packages per hospital, and the occupied bed-days freed from December to February |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · S10 (the governing verb is causal: a package frees only the days a patient was still waiting for care, and the providers' acknowledgements supply the baseline), with E07 below it (delays on the weekly census against the same delays per patient episode) |
| Gate G mechanism | decomposition_attribution, with binding_constraint |
| Measured traps engaged | #7 uses the ready-made measure · #2 counts file rows instead of the real unit · #13 validates on one population, applies to another |
| Calibration form | Counterparty acknowledgement file: home-care providers' acknowledgements (offered start date or decline) of every pathway-1 discharge referral at the six hospitals last winter, including 640 referrals in a two-site pilot |
| Driving force | A discharge-to-assess package sends a patient home before their regular care starts, so it frees only the days they were still waiting for that care. In the providers' acknowledgements, 58% of Ardmore's delayed patients already had a start date on or before the day they were medically optimised. Their "delay" is transport, medicines and paperwork, which D2A patients wait for too. The national return and the trust's delay file fuse package wait and process days into one number; only the join to the brokerage feed separates them. |

## 1. Situation

A county council will fund 1,200 discharge-to-assess (D2A) packages this winter for patients ready to go home with care (pathway 1). The
system board wants them where they free the most hospital bed-days. Each of the six hospitals' delays is in the national weekly return
and in the trust's discharge records. The council's brokerage portal holds every provider acknowledgement of a discharge referral. The
director of adult services believes the scheme halves delays wherever it runs.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the weekly return, the discharge records, the acknowledgements and the pilot timelines. The patients
  really were delayed for those days. Nothing reported is overturned. The difficulty is how many of those days a package removes, which is a
  counterfactual.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's belief and every voice. Delay per pathway-1 patient still ranks Calder first, and no document
  separates waiting for care from waiting to leave.
* **Instrument repair.** Record every delay to the minute. The delay is already exact. A package still frees only the part spent waiting
  for care, and that is defined by another party's commitment.
* **Lens swap.** The answer counts days that would not have happened anyway, a different population of bed-days from the delays recorded.

## 3. The driving force

A strong solver distrusts the weekly census's average delay because a snapshot over-samples long stayers, rebuilds delay per patient
episode, and keeps the pathway-1 patients the scheme serves. That gives a clean delay per eligible patient and names Calder. But the
scheme's verb is "frees": a package removes the days a patient would otherwise have spent waiting for regular care to start, nothing more.
The trust's delay runs from medically optimised to discharge and includes days spent waiting for transport, medicines and paperwork after
care was arranged. A D2A patient waits those days too, as the pilot shows. The brokerage feed records, for each referral, the start date a
provider had already offered. Freed days are max(0, offered start − optimised date − 1). Where providers are scarce (Eskvale, a rural
community hospital), that is most of the delay. Where care is usually arranged before optimisation (Ardmore, a teaching hospital), it is a
fifth of it.

## 4. The ladder

| Rung | Construction (days freed per package; fill 1,200 by value, each hospital up to its pathway-1 referrals) | Names (ranked first) and winter bed-days | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The weekly return's average delay per delayed patient on census days | A, Ardmore, 21.0 (1.27× Bridgend); 20,470 bed-days, +329% | The national measure every business case uses | A package serves one patient discharge, and the census over-samples long stays: Ardmore's episodes average 9.0 days, not 21.0 |
| 1 | Delay per patient episode from the trust's discharge records | B, Bridgend, 11.2 (1.18× Calder); 11,538, +142% | The right grain for a per-patient package | The scheme's specification serves pathway 1 only, and pathway-3 waits for care homes dominate Bridgend's delays |
| 2 | Delay per pathway-1 episode | C, Calder, 9.8 (1.23× Bridgend); 9,832, +106% | The eligible population at the right grain | The acknowledgements: 212 pilot patients whose care had a start date on or before optimisation left no earlier with D2A |
| 3 | **Decisive:** days freed = max(0, offered start − optimised date − 1) per pathway-1 episode, from the delay file joined to the brokerage feed | **E, Eskvale, 6.15 (1.48× Fernlea)**; **4,770 bed-days** (4th of 6 on rung 0) | — | — |

* **The answer.** Eskvale 280, Fernlea 240, Dunford 320, Bridgend 300 and Calder 60 packages, freeing 4,770 occupied bed-days over the
  winter.
* **Position table.** Eskvale ranks 4th on rungs 0 and 1 and 3rd on rung 2, and leads only rung 3. It is never 2nd.
* **Discriminator dominance.** Calder carries a 1.26× lead into rung 3 (9.8 days against 7.8). Its package wait is 0.25 of its delay and
  Eskvale's 0.79, an edge of 3.2×, above 1.2 × 1.26 = 1.51.
* **Sign discipline.** Every correction walks the figure down, and the answer is the minimum cell. A solver who stops anywhere promises the
  board at least twice the beds.
* **Partial correction priced (L3).** A solver who takes the pilot's pooled freed days (2.2 per package) and applies them everywhere files
  2,640 bed-days (−45%), with the largest hospitals filled first and Ardmore at the top. A solver who measures package wait on the weekly
  census instead of per episode over-samples Dunford's long waits for double-handed care and names Dunford at 7,410 bed-days (+55%).
* **Grid.** Census or episode grain × all pathways or pathway 1 × full delay or package wait = 8 cells. Every non-answer cell names Ardmore,
  Bridgend, Calder or Dunford and sits at least 25% from the answer.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The specification says packages "free beds". No document says which days, and the brokerage feed is an operational
   record between the council and providers.
2. **The corpus pins the counterfactual only through a join.** Delays sit in the trust's records and offered starts in the brokerage feed,
   joined by referral number. Every group-by on either file alone shows one fused delay. In the pilot the absolute split appears only after
   the join: 212 of 212 D2A patients whose care was already arranged left no earlier than matched patients without D2A.
3. **No arithmetic symptom.** Episodes reconcile to the weekly return, referrals to acknowledgements, and packages to the council's budget.
4. **Not a row predicate.** Freed days need a second party's offer, dated against the patient's optimisation, for every episode, before
   the per-hospital means.
5. **The enumeration is arithmetic.** No column holds freed days or flags care as already arranged.
6. **No cutover date.** The pilot ran all winter at two hospitals, and no series steps; the split is a property of each referral.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** Every provider acknowledgement of a pathway-1 referral at the six hospitals last winter (offered start date or decline,
  timestamped), with the 640 pilot referrals' D2A discharge dates.
* **What it certifies.** Process days are the same with and without D2A at each hospital (2.1–2.6 days), and the episode grain reproduces
  the weekly return's patient counts.
* **The absolute split (O2).** Pilot patients whose care was offered to start on or before optimisation: 0 days freed (212 of 212).
  Patients without such an offer: freed days equal offered start − optimised − 1 to the day (428 of 428).
* **Twin pair.** Pilot wards Heron and Linnet are identical on every column of the delay file: pathway-1 episodes (160 each), mean delay
  (8.1 days), age mix and reasons coded. D2A freed 2.0× as many bed-days on Linnet (604 against 302), because Heron's patients had care
  arranged earlier. No delay-based rule reproduces both.
* **Resemblance points at the decoy.** Calder resembles the pilot's best ward on delay length, age mix and pathway share.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The council's specification funds 1,200 packages for pathway-1 patients, one package per discharge, and starts each
  within 24 hours. The system board scores the scheme on occupied bed-days freed from December to February. The council's planning
  assumption takes each hospital's pathway-1 referrals at last winter's level.
* **Empirical pins.** The freed-days rule and unchanged process days come from the pilot through the brokerage join.
* **Voices.** The director of adult services: "D2A halves delays wherever we run it." Calder's discharge lead: "Our patients wait longest
  for everything."
* **Licensed wrong basis.** The specification records that NHS England's regional team counts beds freed as delayed days avoided, on the
  weekly return, and will review the plan on that basis.

## 8. Determinism by construction

* **One offer per referral.** The portal took one acknowledgement per referral last winter, so no revision rule is needed.
* **Optimised date.** Each episode carries one medically-optimised timestamp, and no offer falls on the same calendar day as optimisation
  at a different hour.
* **Winter window.** 1 December to 28 February (90 days); episodes optimised inside it.
* **Fill ties.** Freed days per package differ between every pair of hospitals by at least 0.1 day.
* **Rounding.** The answer, 4,769.6 bed-days, sits 4.6 from the nearest ten-day rounding boundary.

## 9. Prompt sketch and deliverables

> The council is funding 1,200 discharge-to-assess packages this winter, and the trusts need to know where they go and how many bed-days
> they free. Our director of adult services believes the scheme halves delays wherever it runs. Give me the split across the six hospitals
> and the occupied bed-days freed from December to February, to the nearest 10, in a sentence for the system board. Send
> `d2a_allocation.xlsx`, a chart `days_freed.png`, and a one-page `system_board_note.pdf`.

* `d2a_allocation.xlsx`: the six hospitals under the four rung bases, the episode-level build, the care-home sheet (ask A) and the
  transport sheet (ask B).
* `days_freed.png`: for each hospital, mean pathway-1 delay split into package wait and process days as stacked bars, with packages
  allocated printed on each bar, hospitals sorted by package wait, and the census average marked as a dot.
* `system_board_note.pdf`: the committed split, the bed-days, and the deciding comparison for Calder and Eskvale.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each hospital, the mean and 90th-percentile days from discharge-ready to discharge for
  pathway-3 (care home) patients last winter. *Device:* care-home placements are acknowledged twice, a provisional date and a confirmed
  one under the same referral, and the confirmed date governs, per the brokerage guide. Taking the first row understates waits by 3 days
  at four hospitals. Pathway-3 rows never enter the main call.
* **Ask B (device-carried).** For each hospital, the median hours from transport request to pickup and the share of discharges that missed
  their booked slot. *Device:* an amended transport booking gets a new reference that carries the original in a linked field. Counting
  amendments as new bookings halves the miss rate at the two hospitals with a shared ambulance contract.
* **Ask C (validity).** The split and bed-days under each of the four rung bases, and the pilot reproduction (the freed-days rule matches
  640 of 640 pilot patients, while full delay overstates the pilot's freed days by 2.3×).
* **Decoupling.** Clearing the brokerage join changes no figure in asks A or B.

## 11. Rubric arithmetic

6 hospitals × 2 (ask A) + 6 × 2 (ask B) + 4 bases × 2 + 1 reproduction figure (ask C) + 6 package counts, the bed-days, the margin and the
two deciding comparisons + 5 named chart parts + 3 files ≈ 51 criteria.

## 12. World-building constraints

* Days per eligible patient (census delay / episode delay / pathway-1 delay / package wait): Ardmore 21.0 / 9.0 / 7.5 / 1.89, Bridgend
  16.5 / 11.2 / 8.0 / 2.53, Calder 15.0 / 9.5 / 9.8 / 2.41, Dunford 13.0 / 8.0 / 6.5 / 3.58, Eskvale 14.0 / 8.8 / 7.8 / 6.15, Fernlea
  11.0 / 7.0 / 6.0 / 4.16.
* Pathway-1 winter referrals: Ardmore 380, Bridgend 300, Calder 260, Dunford 320, Eskvale 280, Fernlea 240 (1,780 against 1,200
  packages).
* Rung figures 20,470 / 11,538 / 9,832 / 4,770 bed-days. The census-grain package-wait cell is +55% and names Dunford, and no cell is
  within 25%.
* Pilot: 640 D2A patients, 212 with care arranged by optimisation and 0 days freed, 428 freed exactly offered start − optimised − 1.
  Heron and Linnet are identical on every delay-file column.
* Care-home double acknowledgements and transport amendments never touch pathway-1 episodes or offers.

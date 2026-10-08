# DS32 — The firm winter-evening wind contribution a data centre files, when its new ridge farm ices in cloud

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Supply Chain & Logistics · power procurement for data centres |
| Mirrors | Reliability commitments from a portfolio whose new member sits on a regime the validated model never saw (hyperscaler wind and solar PPAs for 24/7 matching at Google and Microsoft, cloud regions adding a site in a colder climate, supplier portfolios adding a plant on a different failure regime) |
| Decision shape | One figure committed at a date: the portfolio's firm winter-evening contribution, filed with the utility by 1 October |
| Committed call | The firm contribution in whole megawatts |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · E17, a model validated on one population (four coastal farms) applied to another (a ridge farm that ices in cloud), with the icing-episode rule recovered from published aggregates (Pattern B) and a binding limit (E14) at rung 2 |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #13 validates on one population, applies to another · #10 notes a binding limit as a risk · #4 never tests its reading against the control |
| Calibration form | Counterparty acknowledgement file: the utility's hourly acknowledgements of energy delivered by the four operating farms over four winters |
| Driving force | The power model reproduces every acknowledged hour of the four operating farms, which sit on the coastal plain where winter cloud never reaches the rotors. The new farm stands on a 640 m ridge. On cold winter evenings it is in cloud, and once rime forms a turbine stays down until four warm hours have passed: an episode, not an hour. The portfolio's winter-evening tail is made of those evenings. |

## 1. Situation

A data-centre operator buys wind through PPAs with four operating coastal farms (A–D, 420 MW) and a fifth, the ridge farm E (150 MW),
which comes online in November. By 1 October it must file with its utility the portfolio's firm winter-evening contribution, which offsets
the data centre's capacity charge and is penalised if the portfolio falls short. The filing rule defines the figure over ten reference
winters, in December to February from 17:00 to 21:00. Procurement believes a fifth site in a new region can only steady the portfolio.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the acknowledgements, the reanalysis weather, the power curves, the accreditation register and the
  system operator's published icing losses. No stakeholder read is overturned. A new region does diversify the wind, and the model is
  excellent on the farms it was built on. The difficulty is that the new farm is a different population.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete procurement's view and the utility's desk check. The five-farm model on the reference winters still files at
  the accreditation ceiling of 158 MW.
* **Instrument repair.** Give every farm a perfect meter and the ridge a perfect weather mast. The coastal farms still never ice, the
  ridge still ices in episodes, and the ridge's output on future evenings is still unmetered. A better instrument of the past adds nothing.
* **Lens swap.** The naive read and the answer differ in population: the farms the model was validated on against a farm whose winter
  regime none of them shares, at a moment (next winter) none of them has metered.

## 3. The driving force

A strong solver models each farm's hourly output from the reference winters' weather, confirms the model against four winters of the
utility's acknowledgements (it matches every hour within 1.5%), adds the ridge farm, takes the portfolio's 10th percentile in the
critical hours, and caps the result at the farms' summed accreditations. Every step is correct. The model has never seen icing, because
the coastal farms never ice: winter cloud there sits above the rotors. The ridge farm's hub height at 640 m puts it inside the cloud base on
cold, humid evenings. The system operator publishes daily icing losses for three other ridge farms in the zone, and those losses follow one
rule exactly: an episode starts after three consecutive in-cloud hours at or below −1 °C, and the turbines stay down until four
consecutive hours above +1 °C. It is a state carried across hours, not a condition on any one of them. On the reference winters that rule
takes the ridge farm out on 19% of critical evenings, and those evenings are the portfolio's tail.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The four farms' acknowledged 10th percentile over four winters, scaled by capacity to 570 MW | 142 MW (+10.9%) | The portfolio's own metered record, the utility's own numbers | The filing rule: the figure is defined on the ten reference winters, with each farm's output modelled from their weather |
| 1 | Power model for all five farms over the reference winters; portfolio 10th percentile in the critical hours | 171 MW (+33.6%) | The filing rule's own definition, a model certified hour by hour, and the diversification procurement expected | The accreditation register: the filing cannot exceed the farms' summed winter accreditations, 158 MW |
| 2 | The same, capped at the register's ceiling | 158 MW (+23.4%) | The constraint applied in the figure, not noted as a risk | The system operator's published icing losses for the zone's ridge farms, which the model cannot reproduce |
| 3 | **Decisive:** ridge-farm output removed through icing episodes (three in-cloud cold hours start one, four warm hours end it), the rule that reproduces every published farm-day, applied to the reference winters | **128 MW** | — | — |

* **Figure shape.** The answer is the minimum cell of the grid. Every partial treatment of icing, and every stop above it, overstates the
  filing; the ceiling no longer binds at the answer, so applying or omitting it there changes nothing.
* **Partial correction priced (L3).** Treating icing as an hour-by-hour condition, with turbines back the moment the cloud lifts, files
  146 MW (+14.1%). An episode that ends at the first hour above 0 °C files 141 MW (+10.2%). The rival start rules, two and four in-cloud
  hours, file 117 and 139 MW (−8.6%, +8.6%), and each misses at least 23 of the 90 published farm-days.
* **Grid.** Base (scaled history, five-farm model) × ceiling (off, on) × icing (none, hourly, episode) = 12 cells, of which the scaled
  history cannot carry icing. The episode cells with the model give 128 MW with or without the ceiling; every other cell sits at least
  10.9% above it, the nearest being the scaled history at 142 MW.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The site register gives the ridge farm's elevation; the published aggregates give daily losses at other farms.
   No document says the new farm ices, or how an icing episode starts and ends.
2. **Corpus blind for a computable reason.** *In every acknowledged hour the four operating farms stood below 200 m on the coastal plain,
   where winter cloud never held three hours at rotor height, so no icing rule could change any acknowledged hour.* The model reproduces
   all of them with or without icing logic.
3. **No arithmetic symptom.** Acknowledged energy reconciles to the model, the register to the ceiling, and the reference winters to the
   filing rule's hour count.
4. **Not a row predicate.** An episode is a state that starts after a run of hours and ends after another run, so a turbine can be down in
   an hour that, alone, meets no icing condition.
5. **The enumeration is arithmetic.** Which critical hours are iced is computed by the state machine over each reference winter.
6. **No cutover date.** Episodes are scattered weather states, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice the model still files at the ceiling.

## 6. The calibration corpus

* **Form.** The utility's acknowledgements: hourly delivered energy from farms A–D at their connection points over four winters, as the
  utility settled them.
* **What it certifies.** Rungs 1 and 2: the farm power curves, shear exponents and 97% availability reproduce every acknowledged hour
  within 1.5%.
* **What it is blind to.** Icing (above).
* **The second control.** The system operator's published daily icing losses at three ridge farms, 90 farm-days, with their hourly
  weather. The episode rule reproduces 90 of 90 within 1%; the hourly-condition reading reproduces 41.
* **Twin pair.** Two farm-days at one of those farms are identical on daily mean temperature (−3.1 °C), humidity (96%), wind (9.4 m/s) and
  nine in-cloud hours. Their published losses were 410 and 205 MWh (2.0×): the first day's in-cloud hours came in one run of nine, the
  second's in three runs of three with warm spells between. No daily-mean rule reproduces both; only the episode state does.
* **Resemblance points at the decoy.** By capacity, turbine model and hub height, the ridge farm most resembles farm B, the steadiest of
  the four in the acknowledgements.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The filing rule: the firm contribution is the 10th percentile of the portfolio's hourly output over the critical hours
  of the ten reference winters, filed in whole megawatts, and may not exceed the farms' summed winter accreditations. The PPAs: delivery at
  each farm's connection point, as generated, with 97% availability guaranteed. The reference-winter list. One sentence each.
* **Empirical pins.** The power model, from the acknowledgements. The episode rule, from the published farm-days.
* **Voices.** Procurement lead: "A fifth site in a new region can only steady the portfolio." The utility account manager: "The register
  is your ceiling; everything under it is yours to claim." The developer: "Our ridge has the best wind in the province."
* **Licensed wrong basis.** The filing rule records that the utility's adequacy desk checks every filing against the farms' mean winter
  capacity factor and will query a figure well below it.

## 8. Determinism by construction

* **Percentile.** The filing rule's nearest-rank percentile over 3,600 critical hours; interpolated readings differ by under 1 MW, and the
  answer is 128.4.
* **Clock.** Critical hours are local time, the reanalysis is in UTC, every farm is in one zone, and no clock change falls in December to
  February.
* **Episode rule.** Start and end runs are pinned by the published farm-days; temperature and humidity at hub height come from the same
  reanalysis the losses were published against, so no lapse-rate convention enters.
* **Shear and availability.** Each farm's shear exponent is in the PPA annex, and availability outside icing is the guaranteed 97%, which
  the acknowledgements confirm.

## 9. Prompt sketch and deliverables

> By 1 October we file our wind portfolio's firm winter-evening contribution with the utility, and the ridge farm comes online in
> November. Procurement believes a fifth site in a new region can only steady the portfolio. Give me the figure we file, in whole
> megawatts, as the line for the utility's form. Send `firm_contribution.xlsx`, a chart `winter_evening_tail.png`, and a one-page
> `filing_note.pdf`.

* `firm_contribution.xlsx` — the filing under each rung construction (ask C), the curtailment sheet (ask A) and the consumption sheet
  (ask B).
* `winter_evening_tail.png` — the distribution of the portfolio's critical-hour output over the reference winters with and without the
  ridge farm's icing episodes, the 10th percentile marked on each, the 158 MW ceiling drawn, and the iced share of the tail annotated.
* `filing_note.pdf` — the committed figure and why the diversified model overstates it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the four operating farms, last year's curtailment ordered by the transmission
  operator, in MWh and hours. *Device:* a new dispatch instruction supersedes the one before it from its own start time, as the operator's
  instruction log documents. Summing every instruction's full span double-counts overlaps at three farms.
* **Ask B (device-carried).** For each month of last year, the data centre's consumption in the critical hours and its peak 15-minute
  demand. *Device:* the meter was replaced in March, and the metering register records that the new meter applies its 40:1 transformer
  multiplier while the old one did not. Summing raw readings mixes scales across the replacement.
* **Ask C (validity).** The filing under each of the four rung constructions, and the share of critical evenings the ridge farm is iced
  in each reference winter.
* **Decoupling.** Clearing the icing episodes changes no figure in asks A or B. Dispatch instructions and the data centre's meter touch no
  acknowledgement, reanalysis or icing record.

## 11. Rubric arithmetic

4 farms × 2 (ask A) + 12 months × 2 (ask B) + 4 rung figures + 10 reference winters (ask C) + the committed figure, the ridge farm's
contribution to the tail and the margin under the ceiling + 5 named chart parts + 3 files ≈ 57 criteria.

## 12. World-building constraints

* Rung figures 142 / 171 / 158 / 128 MW (+10.9%, +33.6%, +23.4%, answer). Partial cells 146, 141, 117 and 139 MW.
* The four coastal farms never meet three in-cloud cold hours at rotor height in any acknowledged or reference winter. The ridge farm meets
  the episode rule on 19% of critical evenings across the reference winters.
* Published icing: 90 farm-days at three ridge farms, all reproduced by the three-hour start and four-warm-hour end; the twin farm-days
  match on every daily mean.
* Dispatch instructions and meter multipliers are independent of every main-call record.

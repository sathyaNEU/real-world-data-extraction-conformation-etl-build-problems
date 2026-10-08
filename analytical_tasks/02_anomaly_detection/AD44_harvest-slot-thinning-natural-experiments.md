# AD44 — Which salmon site gets the plant's one emergency harvest week, when thinning a pen also saves the fish left in it

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Supply Chain & Logistics · aquaculture operations |
| Mirrors | Spending one emergency capacity slot during a stress event when past interventions show a second-order benefit the plan ignores (data-centre load shedding in heatwaves at Google and Meta, where moving one workload also cools the racks left behind; fulfilment decongestion at Amazon peaks, where pulling some orders speeds the rest) |
| Decision shape | Which of N gets one scarce thing: the processing plant's single emergency harvest week during the current heatwave goes to one of five farm sites |
| Committed call | The site harvested in the emergency week, and the thermal mortality the harvest avoids over the rest of the event, in tonnes |
| Gap · Pattern | Gap 3 (objective: mortality avoided, not mortality at risk) over Gap 2 (population) · change-log natural experiments measuring what thinning does for the fish left behind, with the site's own heatwave category (a fine segment against the regional bulletin) below it |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection support |
| Measured traps engaged | #25 assumes an effect the log could measure · #14 coarsens the segment it was asked about · #7 uses the ready-made measure |
| Calibration form | Counterparty acknowledgement file: the insurer's acknowledgements of every thermal-mortality claim in the 2014, 2018, 2019 and 2022 heatwaves, with accepted tonnes per pen |
| Driving force | An emergency harvest saves the fish it takes out, and the plan counts only that. The farm's own change log holds eleven partial harvests that happened during past heatwaves; in the seven that took a pen from above 20 kg per cubic metre to below it, the fish left behind died at about half the rate, and in the four that did not, nothing changed. That effect is measurable only by reading the log as natural experiments and joining each pen to its volume. E's pens run at 25 kg per cubic metre, so its harvest week saves twice what the plan credits; C's run at 14, so it saves nothing more. |

## 1. Situation

A marine heatwave began on the coast two weeks ago, and the regional bulletin calls it category II. A salmon producer has five farm sites
on the coast, and the processing plant can give it one emergency harvest week before the event peaks: up to 600 tonnes of market-size fish
from one site. The emergency plan sends the week where it avoids the most thermal mortality over the rest of the event, takes heatwave
categories at each site's own grid cell, and harvests the densest pens first. The producer holds daily sea temperature by grid cell, the pen
register (volumes and biomass), the farm system's change log with daily pen mortality, the insurer's acknowledgement file and the bulletin.
The fish-health vet wants the hottest site.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: temperatures, the bulletin, biomass, the insurer's accepted tonnes and the logged harvests and
  deaths. The vet is right that site A's water is the warmest in absolute terms. Nothing is overturned; the difficulty is an effect of the
  intervention that the plan assumes away and the log can measure.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the bulletin. Site-level categories with the insurer's mortality rates, applied to the fish the
  week harvests, still name C.
* **Instrument repair.** Suspect file: the insurer's acknowledgement file, which holds no thinned pen because thinning voids the cover. Add
  the thinned pens' mortality: no category rate moves by 0.1 points, so rung 0 still names A, rung 1 B and rung 2 C. The survivor effect is
  still needed, measurable only by reading the change log's harvests as natural experiments; temperatures, the pen register and the change
  log are complete.
* **Lens swap.** The naive population is the fish harvested; the answer adds the fish left behind in thinned pens, a different population
  whose mortality changes only after the intervention.

## 3. The driving force

A strong solver drops the annual-percentile flags, rebuilds each site's heatwave category from its own grid cell (the bulletin's regional
mean hides a fjord site at category III and an exposed site at category I), takes mortality rates per category from the insurer's
acknowledged claims, and values the harvest week as the fish it removes times their site's rate. Every step is correct, and every step
assumes the remaining fish are unaffected. The insurer cannot see otherwise: its policy voids thermal cover on any pen harvested mid-event,
so thinned pens never reach the claims file. The farm system's change log records eleven partial harvests that market timing put inside past
heatwaves, with daily deaths per pen before and after. Joined to the pen register, they split absolutely on density: where the harvest took
a pen from above 20 kg per cubic metre to below it, the survivors' mortality fell 52–58%; where the pen stayed below 20 throughout, it did
not move. E's densest pens drop from 25 to 16 kg per cubic metre under its 420-tonne harvest.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Days above the annual 90th percentile of temperature × standing biomass (scaled to tonnes at risk): A 31, B 26, C 22, D 19, E 16 | A | The analyst's flags and the vet's instinct | The day-of-year climatology: A's water is warm every summer, and against its own seasonal threshold it is barely in a heatwave |
| 1 | The bulletin's regional category II for every site, rate 1.6%, × harvest-ready tonnes: B 9.6, C 8.3, A 8.0, E 6.7, D 6.1 | B | The official bulletin, applied to what the week can harvest | The plan takes the category at the site's own grid cell, and the cells run from category I to category III |
| 2 | Each site's own category, the insurer's rate for it (I 0.4%, II 1.6%, III 4.1%), × harvest-ready tonnes: C 21.3, E 17.2, B 9.6, D 6.1, A 2.0 | C | Site-correct, calibrated on acknowledged claims | The change log: seven past partial harvests that crossed 20 kg per cubic metre halved the survivors' mortality |
| 3 | **Decisive:** add the survivors in thinned pens × the site's rate × 0.55 where the harvest takes a pen across 20 kg per cubic metre: E 34.8, C 21.3, B 17.5, D 6.1, A 2.4 | **E** (5th of 5 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0, 4th on rung 1 and 2nd on rung 2 (C leads it by 1.24×), and leads only rung 3. Rung leaders beat
  their runners-up by 1.19×, 1.16×, 1.24× and 1.63×.
* **Discriminator dominance.** C carries a 1.24× advantage into rung 3, so the required edge is 1.2 × 1.24 = 1.49×. E's value doubles (17.2
  to 34.8, 2.02×) when survivors are counted, because its two densest pens fall from 25 to 16 kg per cubic metre and keep 780 tonnes; C's
  pens sit at 14 and gain nothing. The edge is 1.36× the requirement, and the net is 2.02 / 1.24 = 1.63×.
* **Partial correction priced (L3).** A solver who reads the log but averages all eleven harvests applies a 35% survivor effect everywhere
  and credits C's thinned pens too, naming C, 35.5 against E's 28.3 (1.25×): rung 2's answer again. A solver who models density as a smooth
  elasticity per tonne removed credits large sites and names B, 33.4 against E's 27.1 (1.23×).
* **Grid.** Category grain (annual percentile, regional, site) × survivor effect (none, pooled, density-conditioned) = 9 cells. Percentile
  cells name A without a survivor effect and B with either (B's thinned pens keep the most tonnes); regional cells name B, 17.5 against E's
  13.6 with the density-conditioned effect; site cells name C under no or pooled effect; only site categories with the density-conditioned
  effect name E.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The plan says the week avoids mortality; it says nothing about survivors. The change log records harvests and daily
   deaths for operations, and nothing reports an effect.
2. **Corpus blind for a computable reason.** *Every acknowledged claim is for a pen that was not harvested during its event, because the
   insurer's policy voids thermal cover on any pen harvested mid-event.* The file certifies the site-category rates (rung 2) to within 0.2
   points in all four events and cannot contain a thinned pen.
3. **No arithmetic symptom.** Pen biomass ties to the register, claims tie to the insurer's totals, and the plan's harvest arithmetic is
   exact.
4. **Not a row predicate.** Each logged harvest's effect is a before-and-after comparison of a pen's daily deaths within one event, against
   the same site's unharvested pens, then joined to the pen register to place the pen above or below 20 kg per cubic metre.
5. **The enumeration is arithmetic.** Which of E's pens cross the line under the harvest rule is computed; no column carries it.
6. **No cutover date.** The decision turns on an effect measured across eleven harvests in four events; no site's series steps.
7. **Survives deletion.** Remove both voices and the bulletin: the site-category build is still the natural one.

## 6. The calibration corpus

* **Form.** The insurer's acknowledgement file for the 2014, 2018, 2019 and 2022 heatwaves: every thermal-mortality claim with the pen, the
  event and the accepted tonnes.
* **What it certifies.** Mortality by site-level category (0.4%, 1.6%, 4.1%), which the regional bulletin cannot reproduce (it misses every
  fjord-site claim by half), so a back-tester is confirmed at rung 2.
* **What it is blind to.** Thinned pens (above). The refusal sits in the less inviting record: the change log's eleven partial harvests,
  seven crossing 20 kg per cubic metre (survivor mortality −52% to −58%) and four staying below it (−2% to +3%), with no harvest ending
  between 19 and 21.
* **Twin pair.** Pens F-07 (2019) and H-03 (2022) are identical on every log column: site category III, 600 tonnes, 200 tonnes removed, the
  event's third week. F-07 went from 24 to 16 kg per cubic metre and its survivors died at 1.9%; H-03 went from 15 to 10 and its survivors
  died at 4.0%, 2.1× apart, separated only by the pen-volume join.
* **Resemblance points at the decoy.** By biomass and exposure, E resembles past claims at sites with low acknowledged mortality.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The emergency plan: the week goes where it avoids the most thermal mortality over the rest of the event; categories are
  taken at each site's own grid cell; the densest pens are harvested first, market-size fish only. The pen register. One sentence each.
* **Empirical pins.** Category mortality rates, from the acknowledgement file; the survivor effect and its 20 kg per cubic metre line, from
  the change log.
* **Voices.** The fish-health vet: "Hot water kills; go where it is hottest." The regional manager: "The bulletin says category II
  everywhere, so take the biggest harvest."
* **Licensed wrong basis.** The plan records that the plant's planners allocate emergency weeks by harvest-ready tonnage and will present
  that allocation on the call.

## 8. Determinism by construction

* **Categories.** No site's current category lies within 0.1 of a boundary at its grid cell.
* **Survivor effect.** The seven crossing harvests fall in 52–58%, so 0.55 or any value in the range names E with the same order; no logged
  harvest ended near the line.
* **Harvest plan.** Densest pens first and market-size fish only are filed, so which of E's pens are thinned is fixed (its two 25 kg per
  cubic metre pens).
* **Rounding.** The committed figure is given to the nearest tonne; E's 34.8 sits clear of a boundary.

## 9. Prompt sketch and deliverables

> The plant can give us one emergency harvest week before this heatwave peaks, and all five sites want it. The vet says go where the water
> is hottest. Tell me which site gets the week and how many tonnes of fish it should keep alive over the rest of the event, to the nearest
> tonne, in a line for the operations call. Send `harvest_case.xlsx`, a chart `thinning_effect.png`, and a one-page `allocation_note.pdf`.

* `harvest_case.xlsx` — the five sites under each rung's basis (ask C), the feed sheet (ask A) and the treatment sheet (ask B).
* `thinning_effect.png` — the eleven logged harvests as before-and-after survivor mortality pairs, coloured by whether the pen crossed 20 kg
  per cubic metre, the line labelled, and each site's avoided mortality as a stacked bar (harvested fish and survivors).
* `allocation_note.pdf` — the committed site and figure, and why each other site falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each site, the last twelve months' feed conversion ratio. *Device:* month-end biomass comes
  from counter-and-weigh samples that the husbandry guide adjusts for fish removed as mortality during the month; dividing feed by
  unadjusted biomass gain misstates three sites. The allocation never uses feed records.
* **Ask B (device-carried).** For each site, sea-lice treatments last year and the median days between them. *Device:* a bath treatment is
  logged per pen per day, and the health guide counts one treatment per site campaign; counting log rows multiplies treatments at four
  sites.
* **Ask C (validity).** Each site's avoided mortality under each of the four rung bases.
* **Decoupling.** Clearing the survivor effect and the site-level categories changes no figure in asks A or B.

## 11. Rubric arithmetic

5 sites × 2 (ask A) + 5 × 2 (ask B) + 5 × 4 bases (ask C) + the committed site, its avoided mortality, the runner-up and the margin + 5
named chart parts + 3 files ≈ 52 criteria.

## 12. World-building constraints

* Rung figures as in the ladder; E is 5th, 4th, 2nd (1.24× behind C) and 1st.
* Harvest-ready tonnes: A 500, B 600, C 520, D 380, E 420. E's two densest pens hold 600 tonnes each at 25 kg per cubic metre; C's pens all
  sit at 14; B's thinned pens cross 20 kg per cubic metre and keep 900 tonnes. The pooled build gives C 35.5 and E 28.3; the elasticity
  build B 33.4 and E 27.1.
* Change log: seven crossing harvests (−52% to −58%), four non-crossing (−2% to +3%), none ending between 19 and 21 kg per cubic metre.
* F-07 and H-03 are identical on every change-log column.
* Feed records and treatment logs never touch temperatures, the pen register, the change log or the claims.
* Thinned pens hold under 3% of past heatwave biomass, so adding them to the claims moves no category rate by 0.1 points.

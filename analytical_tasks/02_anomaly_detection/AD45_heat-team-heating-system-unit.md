# AD45 — Which district gets this week's extra heat inspection team, when one boiler can serve twenty buildings on separate lots

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Demographic & Social Science · urban housing conditions |
| Mirrors | Support-ticket storms where one failure files tickets across many accounts that share one upstream component (cloud region incidents at AWS and Azure, a shared network controller behind many Cisco customer sites, a campus Wi-Fi outage filed by every building), counted by the component that failed rather than by who called |
| Decision shape | Which of N gets one scarce thing: the single extra inspection team goes to one of the city's community districts for the cold-snap week |
| Committed call | The district that gets the team, and its excess of heating systems without heat over the week, weather-adjusted |
| Gap · Pattern | Gap 2 (population: the heating system, not the call or the lot) over Gap 4 (rule) · the unit the decision funds is not stored (heating systems built through the boiler register's served-lots link), with finer controls separating expectation models below it |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #2 counts file rows instead of the real unit · #12 stops at the first control that passes · #4 never tests its reading against the control |
| Calibration form | Prior-period close-out: last heating season's close-out summary, with each district's complaints, distinct building-days, heating systems inspected and the published weather-adjusted expectations by borough |
| Driving force | An inspection covers one heating system, and a heating system can serve one walk-up or twenty buildings on separate tax lots. Every complaint is keyed on the building's lot, so counting distinct buildings without heat counts a campus outage twenty times. The boiler register's served-lots table links each lot to its plant, and grouping building-days into heating-system days reproduces every district's published inspection count from last season. District E is walk-ups with their own boilers, where a building is a system; B and C are campuses, where it is not. |

## 1. Situation

A cold snap pushed heat and hot-water complaints in the city up 70% this week. The housing agency can send one extra inspection team to one
community district. Its inspection manual says an inspection covers one heating system, the boiler or plant and every building it serves, and
its deployment rule sends the extra team where the weather-adjusted excess of heating systems without heat is largest. The agency holds the
311 complaints (with each building's lot number), daily temperatures, the lot register, the boiler register with its served-lots table and
last season's close-out summary. The dashboard points at district A, which has had the most heat calls for three winters running.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: complaint counts, building-days, temperatures, the boiler register and the close-out. The dashboard is
  right that A has the most calls. Nothing reported is overturned; the difficulty is building the unit the inspection covers, which no file
  is keyed on.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the dashboard and both voices. A weather-adjusted count of distinct buildings without heat, with the expectation
  model that reproduces the close-out, still names C.
* **Instrument repair.** Make every complaint perfectly geocoded and every lot correct: they are. A lot is still a lot, and a campus plant
  still serves twenty of them.
* **Lens swap.** The naive population is buildings (lots) without heat; the answer's is heating systems, a different population that merges
  campus lots and leaves walk-ups unchanged, and it names a different district.

## 3. The driving force

A strong solver discards call counts (one building's tenants call dozens of times), collapses to distinct building-days, fits a negative
binomial expectation on heating degree days from two prior seasons, picks the model form that reproduces the close-out's borough
expectations rather than only the citywide one, and names C. Every step is correct, and every step counts lots. The manual's unit is the
heating system. Public-housing campuses and co-op villages run one plant for many buildings on separate tax lots, so one plant failure files
complaints from every lot it serves. The boiler register's served-lots table links lots to plants; a heating-system day is a plant with at
least one complaint from any lot it serves. B and C are campus districts, averaging 2.7 and 2.2 lots per system among complaining lots; E's
complaining buildings are walk-ups, where nearly every lot has its own boiler. Last season's close-out counts inspections per heating system, and only the plant link
reproduces it.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Complaints in the week: A 1,240, B 980, C 860, D 760, E 690 | A | The dashboard and the council's own measure | The complaint file: A's calls come from 31 lots, six of them carrying 40% of the calls |
| 1 | Excess distinct building-days over a heating-degree-day expectation that reproduces the citywide published figure: B 310, A 240, C 220, E 190, D 150 | B | The memo's unit and weather adjustment, passing the citywide control | The close-out's borough expectations: this model misses four of five boroughs by 9–16% |
| 2 | Excess building-days over the model with district-specific degree-day slopes, which reproduces all five borough expectations: C 260, E 205, B 190, A 140, D 120 | C | Passes the salient control and every finer one | The close-out's inspection counts: last season's heating systems inspected match building-days in only 18 of 59 districts |
| 3 | **Decisive:** link lots to plants through the served-lots table, count heating-system days, same expectation model at that grain: E 199, A 129, C 117, D 114, B 70 | **E** (5th of 5 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0, 4th on rung 1 and 2nd on rung 2 (C leads it by 1.27×), and leads only rung 3. Rung leaders beat
  their runners-up by 1.27×, 1.29×, 1.27× and 1.54×.
* **Discriminator dominance.** C carries a 1.27× advantage into rung 3, so the required edge is 1.2 × 1.27 = 1.52×. E keeps 0.97
  heating-system days per building-day against C's 0.45 (2.16×), 1.42× the requirement, so the net is 2.16 / 1.27 = 1.70×.
* **Partial correction priced (L3).** A solver who merges lots by owner instead of by plant treats every walk-up in a landlord's portfolio as one
  system; E's walk-ups sit in three large portfolios with separate boilers, so E collapses to 72 and C leads again, 112 against A's 91
  (1.23×). A solver who divides building-days by each district's average lots per plant, instead of linking complaining lots, names D: E's
  average is inflated by a co-op village whose plants never failed, so E falls to 85, while D keeps 114 against A's and C's 93 (1.23×).
* **Grid.** Unit (calls, lots, owners, plants) × expectation (citywide slope or district slopes) = 8 cells. Call cells name A; lot cells name
  B (citywide) or C (district); owner cells name A (156 against D's 113) or C (112 against A's 91); plants with the citywide slope name A,
  221 against E's 184 (1.20×), because A's walk-ups keep their rung-1 lead at plant grain; only plants with district slopes name E.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The manual defines the inspection's unit; nothing says how lots relate to plants or that complaint files count lots.
   The boiler register is filed for permit renewals.
2. **The corpus pins a construction, not a menu (Pattern B).** Plant-linked heating-system days reproduce last season's published
   inspection counts in all 59 districts. Building-days reproduce 18, owner groups 27; both over-count in every campus district, so both miss
   the citywide total by more than 25%. The unit is a join from lot to plant and a group by plant and day, not a setting.
3. **No arithmetic symptom.** Complaints geocode to lots, lots tie to the lot register, building-days reconcile, and the expectation models
   reproduce their controls.
4. **Not a row predicate.** It needs every complaining lot joined to its plant, plant-days formed across lots, and the expectation refitted at
   plant grain.
5. **The enumeration is arithmetic.** Heating systems without heat are computed; no field carries a plant on a complaint.
6. **No cutover date.** The campus structure is permanent; nothing steps.
7. **Survives deletion.** Remove both voices and the dashboard: the building-day build is still the natural one.

## 6. The calibration corpus

* **Form.** Last heating season's close-out summary: for each district, complaints, distinct building-days, heating systems inspected, and
  the published weather-adjusted expectation for each borough.
* **What it pins.** The district-slope expectation, through the borough figures (the finer controls), and the heating-system unit, through the
  inspection counts (above).
* **Every rule exercised.** Districts with campuses, with walk-ups and with mixed stock all appear, so each construction is tested where it
  differs.
* **Twin pair.** Last season, districts 7 and 12 had identical complaints, building-days, buildings, units and degree-day exposure. The
  agency inspected 41 heating systems in district 7 and 82 in district 12, 2.0× apart, because district 7's complaining lots sat on campus
  plants serving two lots each. Only the plant link separates them.
* **Resemblance points at the decoy.** E's call and building-day profile resembles districts whose close-out shows modest inspection counts.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The inspection manual: an inspection covers one heating system, the boiler or plant and every building it serves. The
  deployment rule: the extra team goes where the weather-adjusted excess of heating systems without heat is largest this week. The boiler
  register as the agency's registration record. One sentence each.
* **Empirical pins.** The expectation form, from the borough figures; the unit, from the inspection counts.
* **Voices.** The dashboard owner: "District A has had the most heat calls for three winters running." The borough inspection chief:
  "Distinct buildings is how we count; calls are noise."
* **Licensed wrong basis.** The manual records that the council's housing committee tracks districts by heat complaints per thousand units and
  will review the deployment on that basis.

## 8. Determinism by construction

* **Plant links.** Every lot in the contending districts maps to exactly one active plant for the season; split systems are registered as one
  plant.
* **Plant-day.** A plant counts on a day when any lot it serves files at least one complaint; first-complaint and any-complaint definitions
  agree because no plant's complaints straddle midnight in the week.
* **Model.** District-slope models with or without a squared degree-day term reproduce the borough figures equally and name the same district.
* **Rounding.** The committed excess is given to the nearest whole heating system; E's 199 sits clear of a boundary.

## 9. Prompt sketch and deliverables

> We can put one extra inspection team into one district for the cold snap, and the dashboard is pointing at A again. Tell me which district
> gets the team and how many heating systems there are out above what this weather would explain, as one line for the operations call. Send
> `team_case.xlsx`, a chart `plant_excess.png`, and a one-page `deployment_note.pdf`.

* `team_case.xlsx` — the contending districts under each rung's basis (ask C), the inspection-timing sheet (ask A) and the violations sheet
  (ask B).
* `plant_excess.png` — each contending district's excess as paired bars (building-days and heating-system days), lots per plant labelled
  above each pair, the chosen district highlighted, and the borough expectations from the close-out in a side panel.
* `deployment_note.pdf` — the committed district and figure, and why each other district falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each borough, last season's median days from complaint to completed inspection. *Device:* an
  attempt where the inspector was refused entry is logged and re-attempted, and the manual dates the inspection at the first completed
  attempt; dating from the first attempt understates the delay in three boroughs. The deployment never uses inspection timing.
* **Ask B (device-carried).** For each contending district, open heat violations at the end of last season and their median age. *Device:* the
  violation history holds one row per status change, and the dictionary takes a violation's status at a date from its latest row on or before
  that date; counting rows ever marked open overstates four districts.
* **Ask C (validity).** Each contending district's figure under each of the four rung bases.
* **Decoupling.** Clearing the plant link and the district slopes changes no figure in asks A or B.

## 11. Rubric arithmetic

5 boroughs × 2 (ask A) + 5 districts × 2 (ask B) + 5 districts × 4 bases (ask C) + the committed district, its excess, the runner-up and the
margin + 5 named chart parts + 3 files ≈ 52 criteria.

## 12. World-building constraints

* Rung figures as in the ladder; E is 5th, 4th, 2nd (1.27× behind C) and 1st (1.70× ahead of C, 1.54× ahead of A).
* Lots per plant among complaining lots: A 1.09, B 2.7, C 2.2, D 1.05, E 1.03. District-wide averages over all plants: A 1.5, B 2.9, C 2.8,
  D 1.05, E 2.4 (E's co-op village never failed). Owner-days per building-day: A 0.65, B 0.35, C 0.43, D 0.75, E 0.35.
* The close-out: plant-linked counts match all 59 districts; building-days 18; owner groups 27.
* Districts 7 and 12 are identical on every complaint, lot and weather column.
* Inspection attempts and violation histories never touch complaints, the boiler register or temperatures.

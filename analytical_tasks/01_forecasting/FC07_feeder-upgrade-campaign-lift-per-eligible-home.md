# FC07 — Which feeder gets the one accelerated solar upgrade, when next spring's neighbourhood campaigns have a lift the log can measure

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Demographic & Social Science · household technology adoption |
| Mirrors | Forecasting adoption when a scheduled campaign's lift must be measured per reachable household rather than assumed (incremental adoption per eligible audience in Meta and Google campaigns, Apple feature adoption after onboarding pushes, cloud-migration programmes measured per eligible workload) |
| Decision shape | Which of N gets one scarce thing: the single accelerated feeder upgrade in next year's capital plan, among eight feeders |
| Committed call | The feeder that receives the upgrade, with its forecast 2029 rooftop solar above hosting capacity, in MW to one decimal |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · a scheduled intervention whose effect is recovered from in-log natural experiments, stable only per eligible household (a join the per-feeder event study never makes) |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #25 assumes an effect the log could measure · #24 treats an unpublished figure as unknown · #4 never tests its reading against the control |
| Calibration form | Published control set with a reproduction clause: the utility's filed 2024 adoption-forecast vintage (40 feeder-year cells), which the forecasting standard requires a method to reproduce |
| Driving force | Next spring the city runs neighbourhood solar campaigns on two feeders. The change log holds seven earlier campaigns; measured per feeder their lifts swing from 1.3× to 3.4×, but measured per not-yet-adopted eligible household every one converted 4.1% within a year, as a permanent step. Eligible households live in the parcel register, not in the log. Feeder D's newer suburb has 9,800 of them and few installs so far, so its campaign adds 2.8 MW, which a trend, a vendor target or a per-feeder multiplier all miss. |

## 1. Situation

A distribution utility can fund one accelerated feeder upgrade next year for rooftop solar beyond hosting capacity, among eight feeders
(A–H). The capital plan sends it to the feeder with the most forecast solar above hosting capacity in 2029, the upgrade's design year. The
commission's forecasting standard says a feeder forecast may be used in a capital decision only if its method reproduces every cell of the
utility's filed 2024 forecast vintage. The city's sustainability plan schedules neighbourhood campaigns on feeders D and G next spring.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the published hosting-capacity report, interconnection history, the filed vintage, the parcel
  register, the change log and the city's plan. No one's claim about their own figures is overturned. The difficulty is sizing an effect
  that has not happened yet from instances that have.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the vendor's proposal. The standard-compliant forecast still names C, and campaigns are
  still sized by whatever multiplier a solver assumes or reads off per-feeder installs.
* **Instrument repair.** Record every install perfectly. The campaigns are next spring's, and their size depends on households that have
  not adopted yet; no better record of the past observes it.
* **Lens swap.** The naive read and the answer differ in moment and population: feeder D's adoption path without a campaign against its
  eligible households under one.

## 3. The driving force

A strong solver reads the suppressed cells off their published totals, builds the eligible-household diffusion model that reproduces the
filed vintage, and then sees the campaign schedule. It does the event study the change log invites, aligning seven past campaigns on their
start dates. Per feeder, the lift is all over the place (1.3× to 3.4× a year's installs), so a careful analyst falls back on the vendor's
stated target or the average multiplier. Both scale feeder D's small trend and leave D third. The instability is in the unit. A campaign
reaches households that could adopt and have not: owner-occupied single-family parcels with a suitable roof and no system yet. That count
comes from the parcel register joined to interconnection history. Per such household, every past campaign converted 4.1% within twelve
months, and the step stayed. D's suburb is young: 9,800 eligible households, few systems yet, so its campaign adds 402 systems and 2.8 MW.

## 4. The ladder

| Rung | Construction | Names (2029 MW above hosting capacity) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Each feeder's install CAGR on the published report's installed base, suppressed commercial cells read as zero | A (3.1 against 2.4) | The utility's own growth rates on the utility's own published base | **E25 (a suppressed cell, bounded):** B's published feeder total minus its residential cell fixes its suppressed commercial cell at 1.5–1.6 MW |
| 1 | The same with B's commercial base bounded from the published total | B (3.9 against 3.1) | Every published figure used, the unpublished one bounded, nothing guessed | The reproduction clause: CAGR reproduces 9 of the filed vintage's 40 cells |
| 2 | Diffusion per feeder with market size set by eligible households from the parcel register, which reproduces 40 of 40 filed cells | C (3.2 against 2.6) | The method the standard requires, proven on every filed cell | The city's campaign schedule, sized by the change log's seven campaigns per eligible household |
| 3 | **Decisive:** rung 2 plus each scheduled campaign's permanent step of 4.1% of the feeder's not-yet-adopted eligible households | **D (4.8 against 3.2)** | — | — |

* **Position table.** D is 5th on rung 0 (1.2), 5th on rung 1 and 3rd on rung 2 (2.0), and leads only rung 3. Leaders beat runners-up by
  1.29×, 1.26×, 1.23× and 1.50×.
* **Discriminator dominance.** C carries a 1.60× advantage into rung 3 (3.2 against 2.0). D's campaign edge is 2.40× (4.8 against 2.0),
  above the required 1.2 × 1.60 = 1.92, for a final margin of 1.50×.
* **Partial correction priced (L3).** The vendor's target of +60% installs in the campaign year puts D at 2.25 MW. The per-feeder event
  study's average multiplier (2.1× a year's installs) puts it at 2.46 MW. Both leave D third behind C and B, where rung 2 left it.
* **Grid.** Base (suppressed as zero, bounded) × model (CAGR, eligible-household diffusion) × campaign (none, vendor target, per-feeder
  multiplier, per eligible household) gives 16 cells. The name is A, B or C everywhere except diffusion with per-household campaigns,
  and the nearest wrong cell (the per-feeder multiplier) still has C ahead by 1.30×.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The change log records campaigns and dates, and the city's plan names the neighbourhoods. No document says what
   a campaign converts or of whom.
2. **Corpus blind for a computable reason.** *In every one of the filed vintage's 40 cells no campaign ran on the feeder within the
   forecast window, because the programme paused in 2019 and the vintage was filed in 2024.* The eligible-household diffusion model
   reproduces 40 of 40 without any campaign term.
3. **No arithmetic symptom.** Feeder totals tie to the published report, systems to interconnections, and eligible households to the
   parcel register, under every rung.
4. **Not a row predicate.** The campaign effect is a rate per not-yet-adopted eligible household, which is a parcel-register class minus
   households already holding a system, recovered from seven aligned instances.
5. **The enumeration is arithmetic.** Each feeder's remaining eligible pool is a count built from two files. No column holds it.
6. **No cutover date carries the answer.** Past campaigns step their feeders' series, and aligning them gives the unstable per-feeder
   multipliers, which are the decoy. The answer needs the pool those steps were drawn from.
7. **Survives deletion.** No wrong number exists to delete. Without the vendor's proposal a solver still has to choose a size, and the
   event study still gives the wrong one.

## 6. The calibration corpus

* **Form.** The filed 2024 vintage: forecast systems and MW for each of eight feeders over 2024–2028, filed with the commission. The
  standard's clause makes reproducing it, from the data available at filing, the condition of using a method.
* **What it certifies.** The eligible-household diffusion model reproduces 40 of 40 cells. CAGR reproduces 9 and freely fitted diffusion
  23. Both miss on the high side for saturating feeders and fail on the total by 14% and 6%. A back-tester is confirmed at rung 2.
* **What it is blind to.** Campaigns (above). The change log is the second, less inviting record: seven campaigns from 2014–2018, each
  with dates, sign-ups and its feeder's monthly installs.
* **Twin pair.** Campaigns 2016-03 and 2017-02 are identical on every column the change log carries: 48 installs on the feeder in the
  prior year, the same budget, sign-ups, vendor and duration. Their twelve-month lifts are 226 and 107 systems (2.1×), because their
  feeders held 5,510 and 2,610 not-yet-adopted eligible households. Per such household both are 4.1%; no per-feeder multiplier reproduces
  both.
* **Resemblance points at the decoy.** D's campaign neighbourhood matches 2017-02 on every log column, the campaign with the smaller lift.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The capital plan: the upgrade goes to the feeder with the most forecast solar above hosting capacity in 2029. The
  forecasting standard: a method is usable only if it reproduces every filed vintage cell. The sustainability plan: campaigns on feeders D
  and G next spring. The hosting-capacity report: suppressed cells are those with fewer than three commercial customers.
* **Empirical pins.** Market size per feeder, from the parcel register (through the filed vintage). The campaign step, 4.1% of
  not-yet-adopted eligible households, from the change log. System size for campaign installs, 7.0 kW, from the log.
* **Voices.** The planning engineer: "Growth rates have tracked every feeder we have." The customer-programmes manager: "Campaigns move
  timing more than totals."
* **Licensed wrong basis.** The capital plan records that the commission's staff screen feeders on the published report's current
  utilisation (installed solar over hosting capacity) and will present that screen at the review.

## 8. Determinism by construction

* **Step, not pulse.** In all seven campaigns the 24 months after the campaign year follow the pre-campaign diffusion path within 1%,
  so a step and a step-plus-decay reading coincide; there is no pull-forward to net.
* **Eligibility.** The parcel register flags owner occupancy, dwelling type and roof suitability; the filed vintage reproduces only with
  all three, so the class is pinned by the control set.
* **Suppressed cell.** Published totals and residential cells are in kW, so B's commercial cell is fixed within 0.1 MW, and no reading
  of it moves B's position.
* **Campaign timing.** Both campaigns finish in 2026, so their steps sit fully inside the 2029 horizon under any monthly convention.
* **Ties.** No two feeders sit within 0.3 MW at any rung's top two.

## 9. Prompt sketch and deliverables

> The capital plan has room for one accelerated feeder upgrade next year, and I need to name the feeder at the planning committee on
> the 12th, with how far over hosting capacity it will be in 2029. Our planning engineer would rather stay with the growth rates that
> have served us for years. Send me `feeder_upgrade_case.xlsx`, a chart `feeder_2029_path.png`, and a one-page `upgrade_choice.pdf`.

* `feeder_upgrade_case.xlsx` — the forecast for all eight feeders, the complaint sheet (ask A) and the transformer sheet (ask B).
* `feeder_2029_path.png` — installed solar against hosting capacity for the top four feeders, 2018–2029: history, the diffusion path,
  the campaign step on D and G as a shaded band, and the 2029 exceedance labelled.
* `upgrade_choice.pdf` — the committed feeder and its 2029 exceedance, the runner-up, and why the vendor's target does not size the
  campaign.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each feeder, last year's voltage complaints and the share resolved within 30 days. *Device:*
  a complaint reopened after closure posts as a new ticket carrying its parent's number, and the service manual measures resolution on
  the parent. Counting tickets inflates three feeders' complaints and understates their resolution rate.
* **Ask B (device-carried).** For each feeder, the number of service transformers at or above nameplate during last summer's peak week.
  *Device:* a three-phase bank of single-phase units carries one asset ID with a phase suffix, and its nameplate is the bank's. Comparing
  each unit's load with the bank's nameplate misses every overloaded bank on two feeders.
* **Ask C (validity).** Each feeder's 2029 exceedance under each of the four rung constructions, with each construction's hits on the 40
  filed cells.
* **Decoupling.** Removing the campaign step changes no figure in asks A or B.

## 11. Rubric arithmetic

8 feeders × 2 (ask A) + 8 feeders × 2 (ask B) + 8 feeders × 4 constructions (ask C) + the committed feeder, its exceedance, the
runner-up and the margin + 5 named chart parts + 3 files ≈ 76 criteria.

## 12. World-building constraints

* 2029 exceedance (MW) by rung: A 3.1/3.1/1.9/1.9, B 2.4/3.9/2.6/2.6, C 2.0/2.0/3.2/3.2, D 1.2/1.2/2.0/4.8, G 0.6/0.6/0.5/1.5.
* Feeder D: 9,800 not-yet-adopted eligible households, 60 installs a year on trend, campaign step 402 systems × 7.0 kW.
* Seven past campaigns, each a 4.1% step (±0.3 point) per not-yet-adopted eligible household; per-feeder lifts span 1.3×–3.4×.
* The filed vintage's 40 cells: 40 / 23 / 9 reproduced by the three model families. No vintage window contains a campaign.
* Reopened complaints and transformer banks never touch installs, parcels or the change log.

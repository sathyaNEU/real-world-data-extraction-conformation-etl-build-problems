# AD46 — How many restaurants the hygiene grant reaches, when the qualifying small segments have their rates withheld

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Nonprofit & Grant-making · grant-funded food-safety programmes |
| Mirrors | Programme sizing from an agency's published statistics where small cells are withheld (community grants targeted on census tables with suppressed tracts, seller-education programmes on marketplaces sized from published category statistics, outreach funded by foundations and targeted from health-department tables) |
| Decision shape | One figure committed at a date: the number of restaurants the campaign will reach, written into the grant work plan |
| Committed call | The campaign's reach, to the nearest ten restaurants, in the work plan due to the foundation on 1 March |
| Gap · Pattern | Gap 2 (population: the eligible segments) over Gap 3 (objective: reach under capacity) · a withheld cell bounded from published totals and its other components, with a per-borough trainer cap applied in the figure below it |
| Gate G mechanism | decomposition_attribution, with binding_constraint support |
| Measured traps engaged | #24 treats an unpublished figure as unknown · #10 notes a binding limit as a risk · #21 adds exclusions the rules do not ask for |
| Calibration form | Gold-standard verification subsample: the health department's re-inspection of 1,100 randomly drawn restaurants by senior inspectors, published by segment for segments at or above the publication floor |
| Driving force | The grant funds training in segments whose published initial-inspection critical rate is at least five points above the city's, and the department withholds the critical count of every segment under 40 restaurants. Withheld is not unknown: each neighbourhood's critical total is published, and so is every other cuisine's count in it, so where two cuisines are withheld their critical counts sum to a known figure and each is bounded. Six withheld segments clear the line even at the low end of their bounds, and all six sit in boroughs where trainer capacity is still free. |

## 1. Situation

A food-safety nonprofit holds a foundation grant to train kitchen staff in restaurant segments (cuisine × neighbourhood) with high
critical-violation rates; the grant pays per restaurant trained, so the work plan must commit the reach. The grant terms make a segment
eligible when the health department's published figures show its initial-inspection critical rate at least five points above the citywide
rate, and cap reach in each borough at what its trainers can deliver in the grant year (90 restaurants each; three trainers work in
Brooklyn, Queens and Staten Island, five in the Bronx and Manhattan). The department publishes, by segment and by neighbourhood, restaurants and restaurants with a critical violation on their first cycle inspection, withholding segment critical counts under
40 restaurants. The nonprofit holds those tables, the department's quality-assurance re-inspection results and last year's all-inspection
pilot. The department's liaison says a withheld rate is a rate nobody has.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the published counts and rates, the withheld markers, the neighbourhood totals, the trainer table and
  the re-inspection results. The liaison is right that the department has not published those rates. Nothing is overturned; the difficulty is
  that the published table already settles them.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the liaison's view and the pilot. Published eligible segments under the borough cap still give 1,170, and still
  leave out six segments the table proves eligible.
* **Instrument repair.** Publish every cell the rule allows: the withheld cells stay withheld by rule. A better table of the same design still
  needs the bound.
* **Lens swap.** The naive population is published segments; the answer adds withheld segments proved eligible by arithmetic on other cells,
  a different set of restaurants in different boroughs.

## 3. The driving force

A strong solver discards the pilot's all-inspection rates (follow-up visits are sent where a restaurant already failed), takes the
department's first-cycle figures, finds 22 published segments over the line, applies the per-borough cap that binds in Brooklyn and Queens,
and commits 1,170. Every step is correct, and every withheld segment has been dropped as unknown. The neighbourhood rows are published in
full, and so is every cuisine above the floor. In a neighbourhood with one withheld cuisine, its critical count is the neighbourhood total
less the published cuisines, exactly. Where two cuisines are withheld, their counts sum to a known figure and each lies between that sum less
the other's restaurant count and the smaller of the sum and its own count. Fourteen segments are withheld; six are over the line at the bottom
of their bounds, three straddle it, and five are below it at the top. The six hold 220 restaurants, all in the Bronx, Manhattan and Staten
Island, where trainers still have room.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Every inspection row in the pilot, 40 segments over the line, no cap | 2,600, +87% | Last year's pilot and the owners' own complaints | The re-inspection subsample: all-inspection rates run 9 points above the senior inspectors' verified rates, first-cycle rates within 1 |
| 1 | Published first-cycle rates: 22 eligible segments, no cap | 1,560, +12% | The department's own published basis | The trainer table: Brooklyn's 520 and Queens's 410 eligible restaurants exceed the 270 that each borough's three trainers can deliver |
| 2 | Published eligible segments under the per-borough cap | 1,170, −16% | Basis and capacity both respected | The neighbourhood totals: six withheld segments are bounded above the line |
| 3 | **Decisive:** bound every withheld segment from its neighbourhood total and the published cuisines, add those over the line at the low end of their bound, apply the cap | **1,390** | — | — |

* **Figure shape.** Rungs 0 to 2 walk the reach down (−40%, then −25%), and the decisive move turns it back up by 19%.
* **Partial correction priced (L3).** A solver who bounds the withheld segments but tests each at the midpoint of its bound admits the three
  straddling segments too, all in uncapped boroughs, and commits 1,540: 11% above the answer and further from it than rung 2.
* **Grid.** Basis (all inspections or first cycle) × withheld segments (dropped, midpoint, bounded) × cap (noted or applied) = 12 cells. The
  first-cycle cells run 1,560 / 1,930 / 1,780 uncapped and 1,170 / 1,540 / 1,390 capped. The pilot rated every segment, so the six
  all-inspection cells give 2,600 uncapped and 1,580 capped whatever is done with withheld segments. The nearest wrong cell is the midpoint
  partial's 1,540, 11% above; every other cell is at least 12% away.
* **Cap interaction.** The six bounded segments fall where the cap is slack, so the cap and the bound do not cancel; had they fallen in
  Brooklyn, the decisive move would have changed nothing, which is why the world puts them elsewhere.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The publication note says small segments are withheld for privacy; no document says the neighbourhood rows bound
   them, and the grant terms speak only of what the published figures show.
2. **Corpus blind for a computable reason.** *Every segment in the re-inspection subsample has a published rate, because the department draws
   that sample only from segments at or above the 40-restaurant floor.* It certifies the first-cycle basis (rung 1 over rung 0) and cannot
   speak to a withheld segment.
3. **No arithmetic symptom.** Every published cell sums to its neighbourhood and borough totals, and the withheld markers sit exactly where the
   floor puts them.
4. **Not a row predicate.** Each bound comes from subtracting a neighbourhood's published cuisines from its total and splitting the remainder
   between withheld cuisines by their restaurant counts.
5. **The enumeration is arithmetic.** Which withheld segments are proved eligible is computed from other cells.
6. **No cutover date.** Nothing in the decision depends on a date.
7. **Survives deletion.** Remove the liaison and the pilot, and dropping withheld segments is still the natural build.

## 6. The calibration corpus

* **Form.** The department's quality-assurance subsample: 1,100 restaurants drawn at random from published segments and re-inspected within
  48 hours by senior inspectors, with verified critical findings published by segment.
* **What it certifies.** First-cycle rates match the verified rates within one point in every sampled segment; all-inspection rates run 9
  points high, because follow-up visits target restaurants that already failed. A back-tester is confirmed at rung 1.
* **What it is blind to.** Withheld segments (above).
* **Twin pair.** Withheld segments West African × Concourse (the Bronx) and West African × Inwood (Manhattan) both hold 34 restaurants, both
  sit in boroughs with trainer places to spare and both show only the withheld marker. Concourse's bound puts its critical rate at 31% or
  more and Inwood's at 15% or less, about 2× apart, which only the neighbourhood arithmetic reveals.
* **Resemblance points at the decoy.** Withheld segments look like the smallest published segments, most of which fall below the line.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The grant terms: a segment is eligible when the department's published figures show its first-cycle critical rate at least
  five points above the citywide rate, and reach in each borough may not exceed its trainers' capacity. The trainer table (two per borough,
  150 restaurants each). The department's publication rule. One sentence each.
* **Empirical pins.** The first-cycle basis, from the re-inspection subsample.
* **Voices.** The programme director: "The pilot's forty segments are the ones owners know need help." The department liaison: "If we
  withhold it, there is no rate; leave it out."
* **Licensed wrong basis.** The grant terms record that the city council's food-safety committee measures need on all inspection results and
  will review the work plan on that basis.

## 8. Determinism by construction

* **What "show" means.** A withheld segment counts only when the published figures show it over the line at every value in its bound; three
  straddling segments are not shown and stay out, and no other segment lies within one point of the line at either end.
* **Neighbourhood structure.** No neighbourhood withholds more than two cuisines, so every bound is a single subtraction and split.
* **Capacity.** Trainer capacity is filed per borough. The six added segments sit in the Bronx, Manhattan and Staten Island, which keep at
  least 160 places spare after rung 2 and room for the three straddling segments as well, so on every first-cycle cell the cap binds only in
  Brooklyn and Queens.
* **Rounding.** Reach is committed to the nearest ten; 1,390 is exact.

## 9. Prompt sketch and deliverables

> The work plan goes to the foundation on 1 March and it has to say how many restaurants we will reach, because that is what they pay on. The
> department's liaison tells us a withheld segment is one nobody has a number for. Give me the reach, to the nearest ten, in a line for the
> plan, and send `reach_build.xlsx`, a chart `segment_bounds.png`, and a one-page `work_plan_note.pdf`.

* `reach_build.xlsx` — eligible segments and reach under each rung's construction (ask C), the openings sheet (ask A) and the grades sheet
  (ask B).
* `segment_bounds.png` — each segment near the line as a point (published) or an interval (withheld bound), the citywide-plus-five line drawn
  and labelled, the six proved segments highlighted, and a borough strip showing reach against each borough's cap.
* `work_plan_note.pdf` — the committed reach and the alternatives a reviewer will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each borough, restaurants that opened in the last twelve months. *Device:* an ownership change
  issues a new permit number at the same address and name, and the permit guide says a permit is not a restaurant; counting new permit numbers
  as openings overstates every borough, three by more than a third. The reach uses the published segment tables only.
* **Ask B (device-carried).** For each of the 22 published eligible segments, the share of restaurants holding an A grade. *Device:* the grade
  field also carries codes for grade pending and pending re-opening, which the dictionary says are not grades; counting them as non-A
  understates eleven segments.
* **Ask C (validity).** Reach under each of the four rung constructions, with each segment's eligibility under each.
* **Decoupling.** Clearing the bounds and the cap changes no figure in asks A or B.

## 11. Rubric arithmetic

5 boroughs × 2 (ask A: openings and permit changes) + 22 segments (ask B) + 4 constructions × 2 (ask C) + the committed reach, the six proved
segments, the capped boroughs and the citywide rate + 5 named chart parts + 3 files ≈ 52 criteria.

## 12. World-building constraints

* Rung figures 2,600 / 1,560 / 1,170 / 1,390; the midpoint partial 1,540.
* 14 withheld segments: six over the line at their lower bound (220 restaurants, outside Brooklyn and Queens), three straddling (150), five
  below at their upper bound.
* Published-eligible restaurants by borough: Brooklyn 520 and Queens 410 against caps of 270, the Bronx 250 and Manhattan 290 against 450,
  Staten Island 90 against 270. The six proved segments add 100 / 60 / 60 in the Bronx, Manhattan and Staten Island; the three straddling
  segments add 90 and 60 in the Bronx and Staten Island. The pilot's 2,600 splits 820 / 640 / 520 / 480 / 140 in the same borough order.
* The Concourse and Inwood West African segments are identical on every column of their own; Concourse is one of the six, Inwood one of
  the five below the line.
* Permit records and grades never touch the published segment and neighbourhood tables.

# AD46 — How many restaurants the hygiene grant reaches, when franchise outlets almost never take the training and last year's pilot was full of them

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Nonprofit & Grant-making · grant-funded food-safety programmes |
| Mirrors | Programme sizing where uptake splits on an attribute that last year's pilot over-represented (seller-education programmes on marketplaces where franchised sellers follow their brand's own training, foundation-funded outreach sized from a pilot in a different district mix, employer upskilling grants where franchisees decline because the franchisor runs its own course) |
| Decision shape | One figure committed at a date: the number of restaurants that will complete training, written into the grant work plan |
| Committed call | The campaign's reach, to the nearest ten restaurants, in the work plan due to the foundation on 1 March |
| Gap · Pattern | Gap 2 (population: who will take the training) over Gap 3 (objective: reach under capacity) · conditioned yield (the pilot's enrolment splits absolutely on franchise status, reached through the state franchise registry), with a per-borough trainer cap on visits applied in the figure below it |
| Gate G mechanism | decomposition_attribution, with binding_constraint support |
| Measured traps engaged | #13 validates on one population, applies to another · #10 notes a binding limit as a risk · #7 uses the ready-made measure |
| Calibration form | Gold-standard verification subsample: the health department's re-inspection of 1,100 randomly drawn restaurants by senior inspectors, published by segment |
| Driving force | The grant pays per restaurant that completes training, and a trainer's year holds 90 visits whether or not the owner signs up. Last year's pilot enrolled 48% of the restaurants it visited, and that rate belongs to nobody: independents enrolled at 0.86 and franchise outlets at 0.04, because their franchisors require their own food-safety programme. The pilot visited segments flagged on all inspections, fast-food heavy and 46% franchise; this year's eligible segments, flagged on first-cycle rates, are 20% franchise. Franchise status is on no inspection table; it comes from each permit's trade name joined to the state franchise registry. Conditioned on it, the 1,390 capped visits yield 990 trained restaurants, where the pilot's pooled rate says 670. |

## 1. Situation

A food-safety nonprofit holds a foundation grant to train kitchen staff in restaurant segments (cuisine × neighbourhood) with high
critical-violation rates; the grant pays per restaurant that completes training, so the work plan must commit the reach. The grant terms make
a segment eligible when the health department's published figures show its initial-inspection critical rate at least five points above the
citywide rate, and cap the work in each borough at what its trainers can visit (90 visits a trainer, training given on the visit; three
trainers work in Brooklyn, Queens and Staten Island, five in the Bronx and Manhattan). Trainers visit eligible restaurants in the order the
department's next inspection cycle reaches them. The department publishes, by segment, restaurants and restaurants with a critical
violation on their first cycle inspection. The nonprofit holds those tables, the department's quality-assurance re-inspection results, the
permit register, the state franchise registry and last year's pilot, with every visit and whether the owner enrolled. The outreach lead says
about half the owners they visit sign up.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the published counts and rates, the trainer table, the permit register, the registry and the pilot's
  enrolment records. The outreach lead is right that the pilot enrolled about half the restaurants it visited. Nothing is overturned; the
  difficulty is that the pilot's rate is a mix this year's segments do not share.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the outreach lead's view and the pilot's summary. Published eligible segments under the cap, valued at the
  pilot's enrolment, still give 670.
* **Instrument repair.** Suspect files: the permit register's chain flag, which marks only brands with 15 or more city locations (a narrower
  record of franchise status), and the re-inspection subsample (1,100 restaurants). Flagging every franchise outlet and re-inspecting every
  restaurant leaves rungs 0–2 at 1,360, 850 and 670, because none of them conditions enrolment, and the conditioned enrolment is still needed
  to reach 990; no instrument can record which owners will enrol this year.
* **Lens swap.** The naive yield is the pilot's 48%, true of no restaurant; the answer's is each visited restaurant's own status rate, a
  different population of likely trainees that moves the figure up by half.

## 3. The driving force

A strong solver discards the pilot's all-inspection flags (follow-up visits are sent where a restaurant already failed), takes the
department's first-cycle figures, finds 28 segments over the line, applies the per-borough cap that binds in Brooklyn and Queens, and values
the 1,390 visits at the pilot's measured enrolment: 670. Every step is correct, and the yield is a mix. Read visit by visit, the pilot's
enrolment splits without overlap: 203 of 236 independents enrolled and 8 of 204 franchise outlets, whose franchisors require their own
food-safety programme. The pilot's segments were the fast-food-heavy ones that all-inspection rates flag, 46% franchise; this year's
first-cycle segments are 20% franchise, and only 7% in the Bronx. No inspection table carries franchise status: each permit's trade name
has to be matched to the state franchise registry. Valued at each borough's own mix, Brooklyn's 270 visits yield 177 trainees, Queens's
166, the Bronx's 350 visits 281, Manhattan's 244 and Staten Island's 122: 990 in all.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Last year's pilot basis: 40 segments flagged on all-inspection rates, every restaurant at the pilot's enrolment rate (0.48), no cap | 1,360, +37% | The pilot's own segments and its own yield | The re-inspection subsample: all-inspection rates run 9 points above the senior inspectors' verified rates, first-cycle rates within 1 |
| 1 | Published first-cycle rates: 28 segments, 1,780 restaurants at 0.48, no cap | 850, −14% | The department's own published basis | The trainer table: Brooklyn's 520 and Queens's 410 eligible restaurants exceed the 270 visits each borough's three trainers can make |
| 2 | The same under the per-borough trainer cap: 1,390 visits at 0.48 | 670, −32% | Basis and capacity both respected, on the programme's own measured yield | The pilot's enrolment records: franchise outlets enrolled at 0.04 and independents at 0.86 with nothing between, and the pilot's segments were 46% franchise |
| 3 | **Decisive:** each borough's visits at its own franchise mix, status from each permit's trade name joined to the state franchise registry, independents at 0.86 and franchise outlets at 0.04 | **990** | — | — |

* **Figure shape.** Rungs 0 to 2 walk the reach down (−37%, then −21%), and the decisive move turns it back up by 48%.
* **Partial correction priced (L3).** A solver who conditions enrolment on the permit register's chain flag, which marks only brands with 15
  or more city locations, counts half the franchise outlets as independents and commits 1,090, 10% above the answer. A solver who conditions
  enrolment but values every eligible restaurant, ignoring the visits the cap allows, commits 1,240, 25% above.
* **Grid.** Basis (all inspections or first cycle) × cap (noted or applied) × enrolment (pilot pooled or status-conditioned) = 8 cells:
  1,360 / 740 / 1,370 / 870 on all inspections (uncapped pooled, capped pooled, uncapped conditioned, capped conditioned) and 850 / 670 /
  1,240 / 990 on first cycle. The nearest wrong cell is 870, 12% below; every other is at least 14% away.
* **Cap interaction.** The cap fixes Brooklyn's and Queens's visits at 270 each; conditioning changes how many of those visits enrol (177
  and 166), not how many are made, so cap and conditioning compose and neither alone reaches 990.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The pilot report gives one enrolment rate; no document links enrolment to franchise status or says franchisors run
   their own programmes, and the grant terms speak only of restaurants trained.
2. **Corpus blind for a computable reason.** *Every restaurant in the re-inspection subsample was inspected, not offered training, because
   the department draws that sample for verification.* It certifies the first-cycle basis (rung 1 over rung 0) and cannot see who enrols.
   The refusal sits in the less inviting record: the pilot's visit-level enrolment, with no segment's franchise outlets above 0.06 or its
   independents below 0.82.
3. **No arithmetic symptom.** Published cells sum to their neighbourhood and borough totals, the pilot's enrolments sum to its 0.48, and
   visits tie to the trainer table.
4. **Not a row predicate.** Each eligible restaurant's status needs its trade name matched to the registry's brands, then each borough's
   visited mix, then the status rates applied under the cap.
5. **The enumeration is arithmetic.** Expected trainees are computed; no column carries franchise status or an enrolment probability.
6. **No cutover date.** Nothing in the decision depends on a date.
7. **Survives deletion.** Remove the outreach lead and the pilot's summary, and the pooled-yield build is still the natural one.

## 6. The calibration corpus

* **Form.** The department's quality-assurance subsample: 1,100 restaurants drawn at random from published segments and re-inspected within
  48 hours by senior inspectors, with verified critical findings published by segment.
* **What it certifies.** First-cycle rates match the verified rates within one point in every sampled segment; all-inspection rates run 9
  points high, because follow-up visits target restaurants that already failed. A back-tester is confirmed at rung 1.
* **What it is blind to.** Enrolment (above).
* **Twin pair.** Pilot segments Fried Chicken × Flatbush and Fried Chicken × Jamaica each had 60 restaurants visited, with identical
  all-inspection rates, visit weeks and trainers. 52 Flatbush restaurants enrolled and 27 in Jamaica, 1.9× apart, because half of Jamaica's
  are outlets of two national franchise brands; only the registry join separates them.
* **Resemblance points at the decoy.** By cuisine and critical rate, this year's eligible segments resemble the pilot's, so a lookup carries
  the pilot's 0.48 forward.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The grant terms: a segment is eligible when the department's published figures show its first-cycle critical rate at
  least five points above the citywide rate; reach counts restaurants that complete training; work in each borough may not exceed its
  trainers' visits. The trainer table (90 visits a trainer, training given on the visit). The work plan's visiting order (the department's
  next inspection cycle). One sentence each.
* **Empirical pins.** The first-cycle basis, from the re-inspection subsample; enrolment by franchise status, from the pilot.
* **Voices.** The programme director: "The pilot's forty segments are the ones owners know need help." The outreach lead: "About half the
  owners we visit sign up; plan on that."
* **Licensed wrong basis.** The grant terms record that the city council's food-safety committee measures need on all inspection results and
  will review the work plan on that basis.

## 8. Determinism by construction

* **Enrolment rates.** The pilot is the only enrolment record: 203 of 236 independents (0.860) and 8 of 204 franchise outlets (0.039). Only
  eight eligible segments were in the pilot, and their own rates sit within 0.02 of these, so status rates are the only reading.
* **Franchise status.** Every eligible restaurant's trade name either matches a registry brand exactly or matches none, and no permit has
  changed brand since the pilot.
* **Visiting order.** The department has not yet published its next cycle, so each borough's visits carry its eligible mix.
* **Rounding.** Reach is committed to the nearest ten; the conditioned figure is 989.2.

## 9. Prompt sketch and deliverables

> The work plan goes to the foundation on 1 March and it has to say how many restaurants will complete training, because that is what they
> pay on. Our outreach lead says about half the owners we visit sign up. Give me the reach, to the nearest ten, in a line for the plan, and
> send `reach_build.xlsx`, a chart `enrolment_by_status.png`, and a one-page `work_plan_note.pdf`.

* `reach_build.xlsx` — eligible segments, visits and expected trainees under each rung's construction (ask C), the certificates sheet
  (ask A) and the grades sheet (ask B).
* `enrolment_by_status.png` — the pilot's enrolment rate by segment as points coloured by franchise status, the pooled 0.48 drawn as a
  labelled line, the two status rates labelled, and a borough strip of visits and expected trainees against each cap.
* `work_plan_note.pdf` — the committed reach and the alternatives a reviewer will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each borough, food-handler certificates issued last year and the share renewed on time.
  *Device:* a replacement for a lost card is issued under the same certificate number with a reissue suffix, and the certification guide
  counts one certificate per number; counting rows inflates every borough, three by more than 10%. The reach never uses certificates.
* **Ask B (device-carried).** For each of the 28 eligible segments, the share of restaurants holding an A grade. *Device:* the grade field
  also carries codes for grade pending and pending re-opening, which the dictionary says are not grades; counting them as non-A understates
  eleven segments.
* **Ask C (validity).** Reach under each of the four rung constructions, with each borough's visits and expected trainees under each.
* **Decoupling.** Clearing the franchise conditioning and the cap changes no figure in asks A or B.

## 11. Rubric arithmetic

5 boroughs × 2 (ask A) + 28 segments (ask B) + 4 constructions × 2 (ask C) + the committed reach, the two status rates, the capped boroughs
and the citywide rate + 5 named chart parts + 3 files ≈ 58 criteria.

## 12. World-building constraints

* Rung figures 1,360 / 850 / 670 / 990; the chain-flag partial 1,090; the nearest grid cell 870.
* 28 published-eligible segments, 1,780 restaurants: Brooklyn 520, Queens 410, the Bronx 350, Manhattan 350, Staten Island 150; franchise
  outlets 130, 123, 25, 70 and 8 (20% overall). The all-inspection basis adds 12 segments and 1,060 restaurants (Brooklyn 500, Queens 400,
  the Bronx 100, Manhattan 60), 90% franchise.
* Trainers: three each in Brooklyn, Queens and Staten Island, five each in the Bronx and Manhattan, 90 visits each.
* Pilot: 440 restaurants visited, 46% franchise; independents 203 of 236 enrolled, franchise outlets 8 of 204. Half of all franchise outlets
  belong to brands with fewer than 15 city locations.
* The Flatbush and Jamaica fried-chicken pilot segments are identical on every column but brand.
* Certificates and grades never touch the segment tables, the permit register, the registry or the pilot's enrolment records.

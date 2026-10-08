# DA27 — The change in concentration a Medicare Advantage acquisition files for its most affected county, when a retiree block is about to change hands

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Economics · market concentration and merger screening |
| Mirrors | Competition screens in markets where large customer blocks are re-awarded on a contract calendar (enterprise cloud and SaaS reseller books, freight carrier contracts, group insurance at large employers), so the share a firm holds at close is not the share the last report shows |
| Decision shape | One figure committed at a date: the ΔHHI stated in the pre-acquisition notification filed on 30 October |
| Committed call | The change in the Herfindahl–Hirschman Index in Tamsin County from Corvane Health acquiring Halvard Senior Plans, in points to the nearest 10 |
| Gap · Pattern | Gap 4 (rule) over Gap 1 (time) · Pattern B (the department's market book pins the attribution through its finer controls), with a suppressed cell recovered from a published total at rung 2 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #12 stops at the first control that passes · #24 treats an unpublished figure as unknown · #4 never tests its reading against the control |
| Calibration form | Existing-book actuals: the department's market book for last year, 62 county markets with enrolment, concentration band, firm count and leading-firm share |
| Driving force | The department counts each employer-group retiree block under the insurer that holds the employer's contract for the coming plan year. Last year's book reproduces its totals and bands under any attribution, and only its leading-firm shares and firm counts pin the rule. In Tamsin the Harrow Foundry retirees, invisible in the release because their cell is suppressed, move to the target on 1 January. |

## 1. Situation

Corvane Health is acquiring Halvard Senior Plans and files the state's pre-acquisition notification on 30 October. The notification states
the change in concentration for the county where the parties overlap most, Tamsin County, on the department's market basis. The pack holds
the latest monthly enrolment release, the release notes, the department's market book for last year, the employer group contract register
with its award history and retiree census, and the deal documents. Halvard closes on 1 January.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the release, the book, the register and the census. No stakeholder computes a concentration figure
  and nothing reported is overturned. The difficulty is which holder the department's basis assigns a retiree block to.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the target's counsel's note. The latest release still yields a clean ΔHHI near 380 to 560, and
  no sentence says which holder a block belongs to.
* **Instrument repair.** Suspect: the enrolment release, with one suppressed cell and crosswalk-month duplicates. Repaired, Harrow's cell
  published and the duplicates removed, rungs 0, 1 and 2 all return 384, each enrollee under the plan serving them this month, which is
  correct. The department's basis assigns each employer block to its coming-year contract holder, an employer-level award recorded in the
  register that no enrolment field claims to record, so the answer stays 1,200 and the attribution is still needed.
* **Lens swap.** The naive market holds the blocks with their current insurers; the answer's market holds them with the coming-year
  insurers. Same enrollees, different holders at a different moment.

## 3. The driving force

A strong solver builds the post-merger market from the latest release, removes the crosswalk-month duplicates the release notes describe,
recovers the suppressed Harrow cell from Brackwater Mutual's statewide group total, and back-tests against the book. County totals tie and
every concentration band matches, so the method looks certified. But the book's leading-firm shares and firm counts miss in 18 of 62
counties, and they all sit where an employer contract changed holder at the year boundary. The department's figures follow the coming-year
award in the register. The Harrow Foundry retiree trust awarded its contract to Halvard from 1 January. Under that attribution the
target's Tamsin share rises from 8% to 25%, and the ΔHHI triples.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Latest release as filed; the suppressed Harrow cell dropped | 606, −50% | The official monthly release, read straight | The penetration file's individual total (7,200) sits 540 below the release's individual rows |
| 1 | Hygiene: crosswalk-month duplicates removed (the release notes list them under both contract IDs) | 557, −54% | Clean, deduplicated and tied to the published individual total | Brackwater's statewide group total minus its 34 other counties leaves 1,530 retirees in Tamsin |
| 2 | Suppressed Harrow block recovered from that published total and held by its current insurer | 384, −68% | Complete market, every total tied, and the book's totals and bands reproduce | The book's leading-firm shares and firm counts miss in 18 counties, all where a contract changed holder |
| 3 | **Decisive:** every group block held by its coming-year contract holder from the register, Harrow's 1,530 retirees with Halvard | **1,200** | — | — |

* **Figure shape.** Rungs 0 to 2 walk the figure down (−8.0%, then −31.1%), and the decisive move reverses them (+212%). A solver who stops
  anywhere short understates the change by half or more.
* **Partial correction priced (L3).** A solver who adopts coming-year holders but only for the blocks the release shows lands on 384,
  rung 2's figure, because Tamsin's only switching block is the suppressed one. Recovering the block without coming-year holders also lands
  on 384. Each half of the insight is worth nothing alone.
* **Grid.** Duplicates (kept or removed) × Harrow block (dropped, current holder, coming-year holder) = 6 cells: 606, 557, 427, 384,
  1,335 and 1,200. The nearest wrong cell is 1,335 (+11.2%): the decisive construction with the documented duplicates left in.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The notification rule says the figure is stated on the latest monthly release on the department's market basis.
   The book's method note says firms are "as the department identifies them". No sentence mentions award years.
2. **Pattern B, pinned by finer controls.** Current-holder attribution reproduces 62 of 62 county totals and 62 of 62 bands, but 44 of 62
   leading-firm shares and 51 of 62 firm counts. Coming-year attribution reproduces 62 of 62 on all four. It is a construction, not a
   menu: it needs the register's award history joined to each employer's retiree census by county, and no release column carries a holder
   for next year.
3. **No arithmetic symptom.** Re-attributing blocks between insurers partitions the same enrollees, so every total ties under both
   readings.
4. **Not a row predicate.** It needs the award effective for the coming plan year per employer, the employer's retirees by county, and a
   re-aggregation of blocks by holder before shares are squared.
5. **The enumeration is arithmetic.** Which insurer holds a block next year is computed from the register; no column states it.
6. **No cutover date.** The rule is an attribution convention, not an event. The award the answer turns on takes effect after the filing,
   and no closed series in the pack steps on it.
7. **Survives deletion.** With every voice removed, the natural pipeline still stops at 384 to 606.

## 6. The calibration corpus

* **Form.** The department's market book for last year, published each autumn: 62 county markets with total enrolment, concentration band,
  number of firms and leading-firm share to 0.1%.
* **What it certifies.** The market basis (individual and group enrolment together) and the release month, through the totals and bands,
  which every attribution reproduces.
* **What pins the rule.** The 18 counties touched by the 9 employer contracts that changed holder at the last year boundary. Their
  leading-firm shares and firm counts reproduce only with the blocks under the holders awarded for the following year.
* **Twin pair.** Wexley and Orrin are identical on every release column for the book month: individual shares by insurer, group block
  sizes by current holder and totals. Their published leading-firm shares are 41.0% and 20.5% (2.0×). Wexley's largest block moved to
  its leading insurer for the following year, and Orrin's did not.
* **Resemblance points at the decoy.** Tamsin's release profile most resembles book counties with no award change, where current-holder
  attribution reproduces every control.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The notification rule: concentration is stated for the county of greatest overlap, on the latest monthly release, with
  individual and group enrolment in one market. The department's guideline excerpt (shipped as background) fixes HHI in percentage
  points.
* **Empirical pins.** The attribution, from the book's finer controls.
* **Voices.** The deal lead: "Regulators read the same monthly release we do; current enrolment is the market." The outside economist:
  "Retiree groups aren't where insurers compete."
* **Licensed wrong basis.** The notification rule records that the target's counsel states shares on the latest release as published and
  will present them at the pre-filing conference.

## 8. Determinism by construction

* **Awards.** Every coming-year award in the register is effective 1 January and was filed by 1 August, so no award is pending at the
  filing date.
* **Suppression.** Tamsin is the only suppressed cell of Brackwater's group contract, so its statewide total less 34 published counties
  recovers 1,530 exactly. The retiree census gives the same 1,530.
* **Duplicates.** Keeping the successor ID or the closing ID gives the same totals; the release notes name both.
* **Arithmetic.** Post-merger HHI minus pre-merger HHI equals 2 × s(Corvane) × s(Halvard), and the answer, 1,200, is exact.

## 9. Prompt sketch and deliverables

> We file the Halvard notification on 30 October, and it has to state the change in concentration in Tamsin County, where we overlap
> most. Our deal lead believes the monthly release is the market as the department sees it. Give me the figure in points to the nearest
> 10, as one sentence for the filing, with `tamsin_screen.xlsx`, a chart `tamsin_shares.png`, and a one-page `filing_note.pdf`.

* `tamsin_screen.xlsx` — the market build, the plan-offer sheet (ask A), the ratings sheet (ask B) and the book reproduction table
  (ask C).
* `tamsin_shares.png` — stacked bars of Tamsin's shares by insurer under the four rung constructions, the Harrow block in its own colour,
  each construction's ΔHHI annotated, and the committed figure marked.
* `filing_note.pdf` — the committed ΔHHI, the post-merger HHI, and the constructions a reviewer will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 34 overlap counties, the number of plans the combined firm offers for the coming
  year and their median monthly premium. *Device:* the landscape file lists a segmented plan once per segment under one plan ID with a
  segment suffix, as its layout note says; counting rows overstates plans in 9 counties and shifts four medians.
* **Ask B (device-carried).** The enrolment-weighted star rating of each of the combined firm's 10 contracts for the coming year.
  *Device:* the ratings technical notes assign a consolidated contract the surviving contract's rating, so weighting with the closing
  contracts' ratings misstates two contracts.
* **Ask C (validity).** For each of the three block attributions, the book's reproduction count on each of its four controls, and Tamsin's
  ΔHHI and post-merger HHI under each rung.
* **Decoupling.** Clearing the coming-year attribution changes no figure in asks A or B.

## 11. Rubric arithmetic

34 counties × 2 (ask A) + 10 contracts (ask B) + 3 × 4 reproduction counts and 4 × 2 rung figures (ask C) + the committed ΔHHI, the
post-merger HHI and the Harrow block + 5 named chart parts + 3 files ≈ 109 criteria.

## 12. World-building constraints

* Tamsin individual enrolment (deduplicated): Corvane 2,160, Halvard 720, Brackwater 2,520, Silverleaf 1,080, Northgate 720 (7,200). The
  release rows carry 540 crosswalk duplicates on Corvane.
* Group blocks: Harrow Foundry 1,530 (Brackwater now, Halvard from 1 January; suppressed); state retirees 270 (Northgate both years).
* Rung ΔHHI: 606 / 557 / 384 / 1,200; other cells 427 and 1,335. Post-merger HHI at the answer 3,450 (49 / 28 / 12 / 11).
* Book: 62 counties; 9 contracts changed holder at the last boundary, touching 18 counties. Wexley and Orrin identical on every release
  column, leading-firm shares 41.0% and 20.5%.
* Segment rows and rating consolidations never touch Tamsin's enrolment or any group block.

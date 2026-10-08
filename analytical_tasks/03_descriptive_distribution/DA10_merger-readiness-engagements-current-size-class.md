# DA10 — How a credit-union association shares 60 merger-readiness engagements among its leagues, when the small credit unions that will exit were mid-sized when the panel first saw them

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Economics · cooperative financial institutions and industry structure |
| Mirrors | Allocating retention or migration support across regions by projected churn when accounts move between tiers over their life (cloud customers that shrink from enterprise to SMB plans, marketplace sellers that fall into a smaller fee tier, subscriptions downgraded over time), where the tier at signup is not the tier now |
| Decision shape | An allocation under a cap: 60 engagements shared in proportion to projected small credit-union exits in 2027–2029, with a guaranteed 10 for any league whose last-window small exit rate beat the national rate |
| Committed call | Engagements per league in whole numbers summing to 60, headed by Lakes' share |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · E16, finer class-by-window controls in the revision log that only the current size class reproduces, with E25 (Mountain's withheld rate fixed by the national total) and delayed entry below it |
| Gate G mechanism | method_or_model_selection, with binding_constraint |
| Measured traps engaged | #12 stops at the first control that passes · #24 treats an unpublished figure as unknown · #13 validates on one population, applies to another · #1 reports a failed back-test, ships anyway |
| Calibration form | Retry or revision log: the association's exit-outlook revision log, each vintage's projections with realised exits by window, league and size class |
| Driving force | The research memo classes a credit union by its assets when the panel first sees it, and the revision log tabulates realised exits by class at the start of each window. Over thirty years, 438 credit unions that entered as mid-sized have shrunk under $50 million, most in Lakes, and they merge at old, small credit unions' rates. Class at entry reproduces every national and league control, because both are complete partitions, and misses 7 of the 12 class-by-window cells. Only the current class reproduces all of them, and it moves Lakes from 13 engagements to 19. |

## 1. Situation

A national credit-union association funds 60 merger-readiness engagements in 2027 (succession planning, partner search, member
communication) for small credit unions, those under $50 million in assets in 2020 dollars. The programme rule shares them among five
regional leagues in proportion to projected small credit-union exits in 2027–2029. It guarantees 10 to any league whose small
credit-union exit rate in 2022–2024 exceeded the national rate. The pack holds the quarterly call-report panel since 1994, the
institution profiles, the merger and liquidation file, the CPI deflator, the research memo (a delayed-entry Kaplan–Meier by size class)
and the association's exit-outlook revision log. The board votes on 11 February.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the call reports, the exits, the revision log's realised counts and its withheld cell, which is
  withheld by rule, not lost. Nobody's reading of their own numbers is overturned. The difficulty is which credit unions are "small" for
  a projection of the next three years, and one rate the log does not print.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the research director's view, the Mountain president's view and the regulator's licensed basis. The memo's
  estimator still classes by entry assets, and that construction still passes every national and league control.
* **Instrument repair.** Clean-data test. Two files are suspect. The revision log withholds Mountain's 2022–2024 small-exit cell, and the
  call-report panel starts in 1994, so credit unions that exited earlier are missing from it. Repair both (publish the cell; carry every
  credit union's history back to its charter, classed as the memo classes it): survival from charter loses the bias that kills rung 0, so
  rung 0 falls in with rung 1, and with Mountain's guarantee applied both give Lakes 13, rung 2's figure; rung 2 stays at 13. No other file
  is suspect: every quarter's assets are reported exactly, and class at first observed quarter is a true label of that quarter's size, not
  a field claiming current size. The answer stays 19, and classing each credit union by its assets at the start of each quarter is still
  needed.
* **Lens swap.** The two reads cover different populations: 2,961 open credit unions that were small at entry, against 3,373 small now:
  438 were mid-sized when the panel began, and 26 have grown out of the class.

## 3. The driving force

A strong solver builds spells from 1994, enters each credit union into the risk set at its age in its first observed quarter, and
estimates hazards by size class. That is the memo's estimator, and it fixes the immortal-time error a naive survival curve makes. It
back-tests on the revision log's four closed windows and matches the national exits within 1%, and every league's exits within 2%. A
careful solver also recovers Mountain's withheld rate from the national figure, which triggers Mountain's guarantee. Nothing fails a
check it would write. But size class at entry is not size class now. A credit union that entered at $120 million and shrank to $35
million is old, small and merging at the old small credit unions' rate. The memo's construction keeps it in the mid class, where its
exit dilutes the mid-class hazard and never reaches a small-exit projection. The revision log's class-by-window cells, tabulated by
class at each window's start, show it, but only to a solver who tests the finer controls after the coarse ones passed.

## 4. The ladder

| Rung | Construction | Lands on (Lakes) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Survival from charter date, class at entry, Mountain's rate treated as unknown | 12 (−36.8%) | Lifetimes from charter for every credit union in the panel | The revision log's national control: survival from charter projects every closed window 28% low, because the panel cannot see credit unions that exited before 1994 |
| 1 | Delayed-entry Kaplan–Meier by class at entry (the memo's estimator), no guarantee | 15 (−21.1%) | Reproduces all 4 national and all 20 league cells of the log | The log's withheld cell is fixed by its national total: Mountain lost 5 of 28 small credit unions (17.9%, against 8.40% nationally) |
| 2 | Same, with Mountain's guarantee of 10 (E25) | 13 (−31.6%) | Every published and recoverable control met, the rule applied in full | The log's class-by-window cells: class at entry misses 7 of 12 |
| 3 | **Decisive:** size class taken at the start of each quarter, projection from the current class (E16) | **19** | — | — |

* **Figure shape.** The answer is bracketed. Current classes without Mountain's guarantee give Lakes 22 (+15.8%), and every class-at-entry
  construction gives 11 to 15 (−21% to −42%). Full answer: Northern Plains 9, Lakes 19, Delta 10, Coastal 12, Mountain 10.
* **Partial correction priced (L3).** A solver who takes the current class but keeps survival from charter lands at 17 without the
  guarantee and 15 with it, because the shrunk-in credit unions are old and the charter-based curve understates old-age hazard most.
* **Grid.** Entry (charter or delayed) × class (entry or current) × guarantee (off or on) gives 8 cells. The nearest non-answer cell is
  17 (−10.5%), and it needs two errors: no delayed entry and no guarantee.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The memo says "size class: total assets at first observed quarter, deflated to 2020 dollars". The programme rule
   says "small credit unions". The log's footnote says its class cells use "class at the start of the window". No sentence sets the three
   side by side.
2. **The salient control certifies the wrong construction.** National and league cells are complete partitions of the same exits, so
   class at entry passes all 24 of them, while only the 12 class-by-window cells tell the constructions apart. Current class reproduces
   12 of 12, class at entry 5 of 12, and every miss is in the same direction: too few small exits, too many mid.
3. **No arithmetic symptom.** Spells, exits and assets reconcile to the panel. Totals tie under both classings, and no credit union is
   lost or duplicated.
4. **Not a row predicate.** Current class is a property of each quarter's deflated assets along a spell. Projected small exits sum
   hazards by class and age over the credit unions small today, through the time-varying class.
5. **The enumeration is arithmetic.** 464 credit unions change class (438 shrink in, 26 grow out), found only by following each
   spell's deflated assets.
6. **No cutover date.** Credit unions shrink gradually over decades, and no exit series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the memo's own definition still fixes class at entry.

## 6. The calibration corpus

* **Form.** The association's exit-outlook revision log: for each closed window (2013–15, 2016–18, 2019–21, 2022–24), the outlook
  published at its start and the realised exits nationally (4 cells), by league (20 cells) and by size class at the window's start (12
  cells). Small exit rates by league carry their at-risk counts, withheld where fewer than 30 were at risk.
* **What it pins (E16).** The current class, uniquely among constructions that pass the coarse controls: 12 of 12 class cells against
  5 of 12. Survival from charter fails even the national cells.
* **The withheld cell (E25).** Mountain's 2022–24 small exit rate is withheld (28 at risk). The national small exits (412 of 4,904,
  8.40%) less the four published leagues leave 5, so Mountain's rate is 17.9%, and the guarantee applies.
* **Twin pair.** States L-3 (in Lakes) and C-2 (in Coastal) are identical on every class-at-entry column: credit unions by entry class,
  ages, field of membership and total exits in every window. Their realised small exits in 2022–24 are 61 and 30 (2.03×), because 46 of
  L-3's mid-at-entry credit unions had shrunk below $50 million. Only the current class separates them.
* **Resemblance points at the decoy.** Lakes' class-at-entry profile most resembles Coastal's, whose projection barely moves between the
  two classings.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The programme rule: "The 60 engagements are shared among the leagues in proportion to their projected small credit-union
  exits in 2027–2029, in whole engagements by largest remainder; a league whose small credit-union exit rate in 2022–2024 exceeded the
  national rate receives at least 10." The rule defines small as under $50 million in 2020 dollars. The memo fixes the delayed-entry
  estimator, exits dated at the merger's effective date, and censoring at 2026Q2.
* **Empirical pins.** The current class, from the log's class cells. Mountain's rate, from the log's national total.
* **Voices.** The research director: "We've classed credit unions by their size when the panel first sees them since the outlook began,
  and it has never missed a national figure." The Mountain league president: "Our numbers are hidden every year; nobody can say we're
  above the national rate."
* **Licensed wrong basis.** The rule records that the regulator's small credit-union office projects exits by size at charter and will
  present its own split to the board.

## 8. Determinism by construction

* **Deflation.** Assets are deflated by annual CPI to 2020 dollars. No credit union sits within 1% of $50 million in 2026Q2, so monthly
  and annual deflators give the same current classes.
* **Hazard grain.** Hazards by class and five-year age band, and by class and single year of age, give the same rounded allocation.
* **Guarantee.** Mountain's recovered rate (17.9%) sits far above 8.40%, so the test is not close under any rounding of the published
  rates.
* **Rounding.** Largest remainder, with no tied remainders under any construction.

## 9. Prompt sketch and deliverables

> The board votes on 11 February on how our 60 merger-readiness engagements are shared among the five leagues. Our research director
> trusts the outlook method we've always used. Give me each league's engagements in whole numbers summing to 60, as the table the board
> votes on, and send `engagement_split.xlsx` with the sheets below, plus `small_exit_projection.png`.

* `engagement_split.xlsx` — the spell build and projections, the four rung constructions' allocations with their control hit counts
  (ask C), the branch sheet (ask A) and the complaints sheet (ask B).
* `small_exit_projection.png` — projected 2027–29 small exits by league under class at entry and current class as paired bars, the
  national 8.40% rate and Mountain's recovered 17.9% marked, the 438 shrunk-in credit unions shaded within each bar, and the L-3 and C-2
  twins annotated.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Branch openings and closures in each league in each year from 2023 to 2025. *Device:* a
  relocation is filed as a closure and an opening on the same date, carrying a relocation flag, as the branch-file guide documents.
  Counting relocations overstates openings and closures by 9% to 27% in 26 of the 30 cells.
* **Ask B (device-carried).** Member complaints per 10,000 members in 2025 for each league, across four product lines. *Device:* a
  complaint referred between the federal and state regulators appears in both extracts under one referral ID. Counting both double-counts
  a fifth of the complaints in the three leagues with state-chartered majorities.
* **Ask C (validity).** Each league's allocation under the four rung constructions, with each construction's hit counts on the log's
  national, league and class cells.
* **Decoupling.** The branch file and the complaint extracts share no row with the call-report panel or the exits. Clearing the
  current-class construction changes no figure in asks A or B.

## 11. Rubric arithmetic

5 leagues × 3 years × 2 (ask A) + 5 leagues × 4 product lines (ask B) + 5 leagues × 4 constructions and the hit counts (ask C) + the
five committed allocations and Mountain's recovered rate + 5 named chart parts + 2 files ≈ 87 criteria.

## 12. World-building constraints

* Projected 2027–29 small exits (Northern Plains, Lakes, Delta, Coastal, Mountain): from charter 62 / 60 / 66 / 84 / 14; delayed entry
  with class at entry 80 / 110 / 100 / 120 / 25; delayed entry with current class 85 / 176 / 98 / 108 / 27; from charter with current
  class 66 / 85 / 64 / 76 / 16.
* Lakes lands at 12 / 15 / 13 / 19 by rung. The other cells are 11, 22, 17 and 15, and none lies within 10% of 19.
* 438 credit unions shrank from mid to small, 61% of them in Lakes, and 26 grew out of small. Class at entry misses 7 of 12 class cells, all in 2016–24.
* National small exits in 2022–24 are 412 of 4,904. Mountain's are 5 of 28, the only withheld rate.
* L-3 and C-2 are identical on every class-at-entry column.
* The branch file and the complaint extracts touch no call-report row.

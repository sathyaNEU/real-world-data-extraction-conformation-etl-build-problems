# RC15 — Which cause the spring ammonia enforcement initiative targets, when a violation is counted once however long it lasts

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Policy & Education · environmental compliance regulation |
| Mirrors | Enforcement and SLA programmes that count incidents by a unit the logs do not store (content-policy strikes counted per continuing violation at Google and Meta, SLA credits per incident rather than per alarm at cloud providers, seller defect episodes at marketplaces) |
| Decision shape | Which of N root causes gets the fix: the state's one enforcement and assistance initiative this year |
| Committed call | The cause the initiative targets, and the spring violation episodes it accounts for |
| Gap · Pattern | Gap 2 (population) · S1 (the unit the decision funds is not stored: an episode is a run of consecutive non-compliant months at one outfall for one parameter), with E29 (a mixed segment split through a join: plants under compliance schedules) at rung 1 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #2 counts file rows instead of the real unit · #6 treats a mixed segment all one way · #4 never tests its reading against the control |
| Calibration form | Counterparty acknowledgement file: permittees' acknowledgements of the notices of violation issued in the last two springs |
| Driving force | The discharge-monitoring file holds one row per limit type per month, and the enforcement guide counts one violation for each continuing failure to meet a limit, however long it continues. Cold-water nitrification losses and the wet spring run for consecutive months at the same plants and collapse into a few episodes. Hauled-waste slugs at plants that take septage break the limit for one month at a time, at many plants, and each is an episode. Only the run-length construction the permittees' acknowledged notices reproduce reveals that. |

## 1. Situation

Ammonia limit exceedances at the state's municipal treatment plants roughly doubled this spring. The utility association blames the wettest spring in
decades; the permits chief points to new seasonal limits written into permits reissued last year; the commissioner believes cold water stalled
nitrification. The water-quality regulator has one initiative this year and will aim it at one cause: inflow and infiltration enforcement (A),
nitrification upgrade grants (B), compliance assistance on the new seasonal limits (C), hauled-waste and septage controls (D) or aeration equipment
grants (E). The enforcement guide says how violations are counted, and every notice of violation issued is answered by the permittee.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the monitoring rows, each exceedance's cause code in the permittee's noncompliance report, the permits
  and their compliance schedules, and the acknowledged notices. The association, the permits chief and the commissioner each describe a real
  cause. Nothing reported is overturned; the decision turns on a unit no file stores.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the three voices and the licensed basis. Counting violation months by cause, the natural careful build, still names
  cold water.
* **Instrument repair.** A perfect monitoring system still reports one row per limit type per month, as the permit requires; the episode is an
  enforcement unit, built from a sequence of correct rows.
* **Lens swap.** The naive build counts months of noncompliance; the answer counts continuing failures, which group the months into a
  different population of events.

## 3. The driving force

A strong solver counts violations, not rows: it groups the monthly, weekly and daily limit rows into one violation per outfall-month. It splits
out plants whose reissued permits carry compliance schedules, because interim limits govern there until the schedule ends, so exceeding the final
limit is not a violation. On violation-months cold water leads clearly. The enforcement guide counts "one violation for each continuing failure
to meet a limit, however long it continues", and the permittees' acknowledged notices show what that means in practice: one notice per run of
consecutive non-compliant months at one outfall for one parameter, ended by any compliant month. Cold-water losses at a plant run January to
April and are one episode. The wet spring ran March to May at the same plants. Hauled-waste slugs strike plants that accept septage for a single
month, then pass. Counted as the guide counts, the slugs lead.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Exceedance rows (each limit type each month) by the noncompliance report's cause code | C, new seasonal limits (412 rows) | The monitoring file's own exceedance flags, coded by the permittees themselves | The permits' compliance schedules: 302 of C's rows are at plants where interim limits still govern |
| 1 | Rows with compliance-schedule plants' final-limit exceedances removed | A, wet weather (330 rows) | Only true violations remain, each coded to a cause | The enforcement guide counts violations, not limit types: A's months breach the weekly and daily limits too, 2.4 rows a month |
| 2 | Violations as outfall-months, limit types grouped | B, cold water (230 months) | One violation per outfall per month, every limit type counted once | The acknowledged notices: month counting reproduces 140 of 418 permittee-spring counts; one notice covers each run of consecutive months |
| 3 | **Decisive:** episodes, runs of consecutive non-compliant months at one outfall for one parameter, ended by a compliant month | **D, hauled-waste loading (104 episodes)** (5th of 5 on rung 0) | — | — |

* **Position table.** D ranks 5th on rung 0, 4th on rung 1 and 3rd on rung 2, and leads only rung 3. Rung leaders beat their runners-up by
  1.25×, 1.27×, 1.64× and 1.49× (104 against aeration's 70).
* **Discriminator dominance.** Cold water carries a 2.09× lead into rung 3 (230 months against 110). Months per episode are 3.7 for cold water
  and 1.06 for hauled waste, an edge of 3.51×, above the required 1.2 × 2.09 = 2.51; the net margin is 1.68×.
* **Partial correction priced (L3).** A solver who builds runs per plant rather than per outfall and parameter merges a plant's separate
  outfalls. The slugs reach both outfalls at the six septage-receiving plants that have two, so hauled waste halves to 52 episodes and cold
  water leads at 62, rung 2's answer.
* **Grid.** Unit (rows, months, episodes) × schedule split (off, on) × run key (plant, outfall and parameter) gives eight feasible builds. Row
  builds name C or A, month builds B, plant-keyed episodes B, and only outfall-and-parameter episodes with the schedule split name D. Without
  the split D still leads at 104 but C rises to 88, so the margin falls to 1.18×.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The guide's sentence says a continuing failure is one violation; it does not say what continues, what key a run
   follows or what ends it. The acknowledgements pin all three.
2. **The acknowledgements pin a construction, not a menu.** Outfall-and-parameter runs ended by one compliant month reproduce 418 of 418
   acknowledged permittee-spring notice counts; plant-keyed runs 301, two-month gaps 266, months 140, rows 31. Every rival overcounts or
   undercounts in one direction for its whole class of permittee, so none reconciles on the two springs' totals. A run is built by ordering each
   outfall-parameter's months and cutting at compliant ones; there is no parameter to scan.
3. **No arithmetic symptom.** Rows, months and episodes reconcile to the same exceedance records; every cause code is filed.
4. **Not a row predicate.** Whether a month starts a new episode depends on the month before it at the same outfall for the same parameter.
5. **The enumeration is arithmetic.** No column carries an episode id; 326 episodes are built from 960 violation rows.
6. **No cutover date.** The slugs strike at different plants in different months; the dated events (the permit reissue, the March storms)
   step the series for C and A and are the decoys.
7. **Survives deletion.** With every voice gone, violation-months still name cold water.

## 6. The calibration corpus

* **Form.** The acknowledgement file: every notice of violation issued for ammonia in the last two springs, each permittee's response
  (acknowledged, contested and upheld, contested and withdrawn), and the monitoring rows of those springs.
* **What it pins.** The episode construction (above), and that withdrawn notices were all at compliance-schedule plants, which certifies the
  schedule split.
* **Twin pair.** Permittees P-118 and P-140 had identical spring rows, violation-months (eight each), cause mixes, plant sizes and outfall
  counts. They acknowledged 8 and 4 notices (2.0×): P-118's months were scattered, P-140's ran in two blocks. Only the run construction
  reproduces both.
* **Resemblance points at the decoy.** This spring's mix of cause codes matches two springs ago, the wet one, when wet-weather notices were the
  largest group.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The regulator's planning rule: the initiative targets the cause behind the most violations this spring, counted as the
  enforcement guide counts them. The guide's sentence on continuing failures. The reissued permits' compliance schedules.
* **Empirical pins.** The run key and the end-of-run rule, from the acknowledgements.
* **Voices.** The utility association's director: "It was the wettest spring in thirty years; every plant was under water." The permits chief:
  "The new seasonal limits are why the numbers jumped."
* **Licensed wrong basis.** The guide records that the federal regional office tallies noncompliance in violation-months and will present
  that tally at the initiative briefing.

## 8. Determinism by construction

* **Cause.** Each violation month carries one cause code in its noncompliance report; an episode takes the code of its months, and no run
  mixes codes.
* **Runs.** Months are calendar monitoring periods; a run ends at the first compliant month at that outfall for that parameter.
* **Schedules.** A plant is under a schedule when its permit's schedule end date falls after the month; no end date falls inside the spring.
* **Window.** March to May, with runs that began in January or February counted once, in the spring, as the guide counts continuing failures.
* **Rounding.** Episodes are whole counts.

## 9. Prompt sketch and deliverables

> Ammonia violations at our plants doubled this spring and we have one initiative to aim at one cause. The commissioner is sure cold water did
> it. Tell me which cause we target and how many of this spring's violations it accounts for, counted the way we enforce, as the sentence for the
> initiative briefing. Send `ammonia_initiative.xlsx` and a chart `violations_by_cause.png`.

* `ammonia_initiative.xlsx` — the five causes under each construction, the overflow sheet (ask A), the biosolids sheet (ask B) and the
  acknowledgement reproduction (ask C).
* `violations_by_cause.png` — for each cause, a strip of plants by month showing non-compliant months, with episodes outlined as bars, the
  month and episode counts printed at the right, and the targeted cause highlighted.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine river basins, spring precipitation against normal and combined-sewer overflow
  events. *Device:* each outfall reports its own overflows, and the overflow rule counts one event per storm per sewer system, as the reporting
  guidance documents; counting outfall reports triples events in the three basins with multi-outfall systems.
* **Ask B (device-carried).** For each of the 40 largest permittees, biosolids applied to land last year. *Device:* permittees report wet or
  dry tonnes with a basis field, as the biosolids form documents; summing without converting overstates the eleven wet-basis reporters about
  fivefold.
* **Ask C (validity).** For each permittee and each of the two closed springs, acknowledged notices and the count each of the five rules
  returns; and each cause's count under each rung construction.
* **Decoupling.** Clearing the run construction and the schedule split changes no figure in asks A or B.

## 11. Rubric arithmetic

9 basins × 2 figures (ask A) + 40 permittees (ask B) + 30 permittees × 2 springs × 5 rules + 5 causes × 4 constructions (ask C) + the targeted
cause, its episodes and the runner-up's + 5 named chart parts + 2 files ≈ 395 criteria.

## 12. World-building constraints

* Rows by cause (A / B / C / D / E): 330 / 260 / 412 / 120 / 140; after the schedule split 330 / 260 / 110 / 120 / 140; violation-months 140
  / 230 / 90 / 110 / 100; episodes 60 / 62 / 30 / 104 / 70.
* Acknowledgements: 418 permittee-spring counts; outfall-parameter runs 418/418, plant runs 301, two-month gaps 266, months 140, rows 31.
* P-118 and P-140 identical on every row, month, cause and plant column.
* Overflow reports and biosolids tonnage touch no ammonia monitoring row.

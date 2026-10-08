# DS13 — Which 180 bridges get the 12-month inspection cycle, when the inventory repeats a bridge's ratings in every year nobody looked at it

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Policy & Education · infrastructure inspection programmes |
| Mirrors | Risk-based inspection or audit frequency set from a register that carries the last observation forward between checks (Google and Meta fleet health scores refreshed only on probe, Amazon supplier audits, cloud configuration-drift scans on rotating schedules) |
| Decision shape | An allocation under a cap: 45 in-depth 12-month slots for each of four district crews, 180 in all |
| Committed call | The 180 bridges by crew, and how many of them come out of the 48-month cycle |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · measured #11's architecture (the loud condition-only decoy beaten, the quiet carried-forward contamination missed), with a latent crew-attribution marker (#17) at rung 2 |
| Gate G mechanism | decomposition_attribution, with forecasting |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #17 guesses an attribution the data can settle · #2 counts file rows instead of the real unit · #13 validates on one population, applies to another |
| Calibration form | Prior-period close-out: the last cycle's inspection close-out (every inspection performed, with date, crew and findings) |
| Driving force | The annual inventory file has a record for every bridge every year. Under the coding guide, a bridge not inspected that year repeats its last ratings. A transition matrix built from consecutive annual records counts those repeats as observed stability, so a bridge on a 48-month cycle shows change in at most one year-pair in four. Old steel girders on busy routes, all on the 48-month cycle, look four times more stable than they are. Only transitions measured between actual inspections, dated by the inventory's unchanging inspection-date field and confirmed by the close-out, put 38 of them into the 12-month tier. |

## 1. Situation

A state DOT must decide which bridges go on the 12-month in-depth inspection cycle next cycle. Each of its four district crews can take 45.
The inspection policy ranks bridges on risk: the probability that a component falls to rating 4 or below within 24 months, times the
consequence (traffic times detour length). The DOT holds eleven years of the annual inventory file (component ratings, inspection date,
structure type, age, traffic, detour), the maintenance-agreement table, and the last cycle's close-out. The chief bridge engineer wants the
slots on every bridge rated 5 or worse.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. The inventory's ratings are exactly what the coding
  guide prescribes, and the close-out, the agreements and the traffic counts are all right. The difficulty is that a carried-forward rating
  is a correct record of the last inspection, not an observation of the bridge that year, and a transition count cannot tell the two
  apart.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chief engineer's view. Risk from consecutive-year transitions, with crews attributed correctly, still puts
  only 12 bridges from the 48-month cycle into the tier, and every count reconciles.
* **Instrument repair.** Inspect every bridge every year from now on. The past decade still holds four-year gaps, and the forward risk still
  has to be estimated from them.
* **Lens swap.** The naive read estimates deterioration over bridge-years in the file. The answer estimates it over inspection intervals
  (a different population of observations, at the elapsed time each actually spans).

## 3. The driving force

A strong solver rejects condition-only tiering, because the policy ranks on risk. It builds transition matrices by material, age and
traffic band from consecutive annual records, and it assigns bridges to crews through the maintenance-agreement table, because the close-out
shows a freeway corridor in District 3 inspected by District 2's crew. Each step is competent, and only 12 bridges move up from the 48-month
cycle. But the annual file repeats a bridge's ratings in every year it was not inspected, and its inspection-date field stays the same in
those years. For a 48-month bridge, three year-pairs in four are carried forward and read as "no change". Measured between actual
inspections, and annualised over the years each one spans, the 64 old steel girders on busy routes have a 24-month decline probability of
0.121, not 0.031. Thirty-eight of them displace prestressed bridges rated 5, whose risk barely changes.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Any component rated 5 or worse, worst first, crews by inventory district code | 0 bridges from the 48-month cycle | The draft policy, and the measure the federal review reads | The policy: tiers go on 24-month decline probability × consequence |
| 1 | Risk from consecutive-year transition matrices, crews by district code | 7 | A full risk model on eleven years of data | The close-out: District 2's crew inspected 31 District 3 bridges on a freeway corridor, under the agreement table |
| 2 | Crews attributed through the maintenance-agreement table (#17) | 12 | The caps now bind on the crews that actually do the work | The close-out's inspection dates: 48-month bridges were inspected in 26% of years, and the inventory repeats their ratings in the rest |
| 3 | **Decisive:** transitions measured between actual inspections (carried-forward years identified by the unchanged inspection date), annualised over each interval's elapsed years | **38** (D1 4, D2 9, D3 21, D4 4) | — | — |

* **Figure shape.** The count rises at every rung (0, 7, 12, 38), and the answer is the extreme cell. Expected declines covered move the
  same way: 24.9, 27.4, 28.1 and 41.3.
* **Partial correction priced (L3).** Dropping the carried-forward years but treating every remaining pair as one year apart overstates
  long-interval deterioration and moves 61 (+61%). Estimating transitions only from bridges already on the 12-month cycle moves 22 (−42%),
  because those bridges are low-rated concrete, not old steel. The decisive construction with crews by district code moves 33 (−13%).
* **Grid.** Ranking (condition, risk) × crews (district code, agreement) × transitions (annual pairs, inspection intervals, unannualised
  intervals) gives 8 feasible cells, since condition ranking uses no transitions. The nearest wrong count is 33 (−13%), one omission away:
  the agreement table.
* **Why the cohort flips.** At rung 2 the marginal prestressed bridge carries a 2.1× risk advantage over the best old steel girder. The
  decisive rung raises the steel cohort's decline probability 3.9× and the prestressed cohort's 1.1×, a 3.5× relative swing, which leaves the
  steel girder 1.67× ahead.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The coding guide says ratings are carried forward between inspections. No document says a transition count
   inherits that, or that long-interval bridges are diluted most.
2. **No sweepable corpus nominates it.** *In every annual record between inspections the ratings are identical to the last inspection's,
   because the coding guide carries them forward.* Every consecutive-year transition count reconciles, and the file cannot show how fast an
   uninspected bridge deteriorates. Only the close-out's dates separate observed stability from carried stability.
3. **No arithmetic symptom.** Bridges, records, ratings and inspections reconcile under every rung, and no rating is wrong.
4. **Not a row predicate.** It needs each bridge's records grouped by unchanged inspection date, transitions taken between inspections,
   annualised by elapsed years, pooled by material × age × traffic band, and then a capped allocation per crew.
5. **The enumeration is arithmetic.** No column flags a record as carried forward. The inspection-date field merely stays the same.
6. **No cutover date.** The cycle lengths are long-standing, and nothing steps in any series.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The last cycle's close-out: every in-depth and routine inspection performed, with date, crew, bridge and findings, against the
  inventory's eleven years.
* **What it certifies.** Two things the shallow rungs need. Crew workloads are reproduced only by agreement-based attribution (four of four
  crew totals, against one of four by district code). The findings are reproduced only by interval-based deterioration: 14% of
  48-month bridges showed a component drop since their previous inspection, against the 3.6% the annual-pair matrices predict.
* **What it is blind to on its own.** It holds one cycle, so it cannot by itself give 24-month probabilities by band. It has to be married
  to the inventory's intervals.
* **Twin pair.** Two cohorts are identical on every inventory column: steel girders built 1966–70, 25,000–35,000 vehicles a day, all
  components rated 6, District 3. One is on the 24-month cycle and the other on the 48-month. Their naive annual decline rates are 4.2% and
  1.9% (2.2×), and their interval-based rates are 4.2% and 4.4%. Only the interval construction reproduces both.
* **Every rule exercised.** Some bridges moved between cycle lengths mid-decade, so intervals of two, three and four years all occur. Some
  received an unscheduled damage inspection, so the inspection-date marker changes mid-cycle.
* **Resemblance points at the decoy.** The steel cohort's record (rated 6, years of unchanged ratings) looks like the bridges the draft
  policy rightly leaves alone.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The inspection policy: the 12-month tier goes to the highest-risk bridges, risk being the 24-month probability of a
  component at 4 or below times traffic × detour, within each crew's 45 slots. The coding guide: ratings are carried forward in years
  without an inspection. The maintenance-agreement table: which crew inspects each route segment. One sentence each.
* **Empirical pins.** Interval-based transitions, from the inventory and the close-out.
* **Voices.** The chief bridge engineer: "The bridges rated 5 are where the risk is." The District 3 engineer: "Our crew knows our bridges;
  the district is the unit." The asset analyst: "Year-on-year changes in the inventory are the cleanest deterioration data we have."
* **Licensed wrong basis.** The policy records that the federal division office reviews tier assignments on condition ratings and will see
  that basis.

## 8. Determinism by construction

* **Carried-forward marker.** A record is carried forward exactly when its inspection date equals the previous year's. The close-out
  confirms every case, with no ambiguous dates.
* **Annualising.** A multi-year transition is converted to annual steps by matrix root within each band. Root and per-year-hazard
  conventions select the same 38 bridges, because no bridge sits within 4% of the cut.
* **Bands and consequence.** Material, age and traffic bands, the consequence formula and the 24-month horizon are filed in the policy.
* **Caps.** 45 per crew, with ties at the cut broken by bridge number, as the policy states. No tie occurs at any crew's cut.

## 9. Prompt sketch and deliverables

> Next cycle each of our four district crews can take 45 bridges on the 12-month in-depth cycle. The chief bridge engineer wants the slots
> on everything rated 5 or worse. Give me the 180 bridges by crew, and how many of them come out of the 48-month cycle, as the table for the
> inspection plan. Send `tier_plan.xlsx`, a chart `risk_by_cohort.png`, and a one-page `inspection_note.pdf`.

* `tier_plan.xlsx` — the 180 bridges by crew under each construction, the field-hours sheet (ask A), the posting sheet (ask B) and the
  transitions sheet (ask C).
* `risk_by_cohort.png` — decline probability by cohort under annual-pair and interval transitions as paired bars, each crew's cut-off risk
  as a labelled marker, the steel cohort annotated, and a panel of one 48-month bridge's annual records with the carried-forward years
  shaded.
* `inspection_note.pdf` — the plan, the count from the 48-month cycle, and why the rated-5 bridges give way.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each crew and structure type, last cycle's mean field hours per in-depth inspection.
  *Device:* an inspection spanning two days is logged as two timesheet rows under one inspection ID, as the timesheet dictionary documents.
  Averaging by row halves the steel-truss figures.
* **Ask B (device-carried).** For each district, the deck area of bridges load-posted on 1 October. *Device:* postings are effective-dated,
  and a posting lifted and reinstated appears twice. Reading the table as of the date, not by counting rows, avoids overstating two districts
  by 12–18%.
* **Ask C (validity).** Each cohort's 24-month decline probability under annual-pair and interval transitions, and the four crews' close-out
  workloads under district-code and agreement attribution.
* **Decoupling.** Clearing the interval construction changes no figure in asks A or B. Timesheets and postings never enter a transition or
  a risk.

## 11. Rubric arithmetic

4 crews × 3 structure types (ask A) + 4 districts (ask B) + 6 cohorts × 2 methods + 4 crews × 2 attributions (ask C) + the movers by crew
(4), the total and the expected declines covered + 6 named chart parts + 3 files ≈ 57 criteria.

## 12. World-building constraints

* 64 old steel girders on busy routes, all on the 48-month cycle. Their 24-month decline probability is 0.031 from annual pairs and 0.121
  from intervals. Prestressed bridges rated 5 on the 24-month cycle: 0.14 and 0.155.
* 48-month bridges inspected in 26% of years. The close-out finds 14% of them with a component drop, against 3.6% predicted from annual
  pairs. 31 District 3 freeway bridges are inspected by District 2's crew.
* Movers 0 / 7 / 12 / 38. The partials give 61, 22 and 33. Expected declines covered: 24.9 / 27.4 / 28.1 / 41.3.
* The twin cohorts are identical on every inventory column. Timesheets and postings never touch ratings, dates, crews or traffic.

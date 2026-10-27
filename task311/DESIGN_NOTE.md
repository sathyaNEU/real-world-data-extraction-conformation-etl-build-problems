# task311: which health region the foundation's 2027 boost of 1,200 interviews goes to

Wave 7, Opportunity Sizing & Decision Support. Architecture 1, drawn 2026-10-27. Seed OS13 (a public charging
coverage figure) was read for its world only: its mechanism is a site-unit reading (data semantics) and its state
energy office repeats task310's organisation family, so the number moves to Survey Research & Official Statistics,
never built against Opportunity Sizing. No probe, reader or solver is run (the STOP rule); the stump is argued on
paper here and measured on the generator's clean truth.

## Draw

| Axis | Value |
|---|---|
| Domain / task type | survey-research-official-statistics / sample-design-allocation-weighting (serves Opportunity Sizing) |
| Objective | Opportunity Sizing & Decision Support: the headline is the precision the boost buys in each region, sized from the pool (1,200 nominal interviews) to the realisable (the standard error they take off the region's 2027 estimate, equivalently the effective interviews they add), and the sizes decide the region |
| Decision / answer unit / question form | pick_one_of_n / named_option (one of five health regions) with each region's projected 2027 standard error / where |
| Shape | 01, five candidates each with its projected error and error reduction, the call, the runner-up and the gap, plus three asks |
| Gap / pattern / generators | objective (the 2025 error is correct and is not what the boost is scored on), time / none / G2 (interviews against areas), G17 |
| Gate G / strategy | binding_constraint (the between-area variance the fixed areas carry is a floor no added interview moves) / grain_or_unit |
| Layer 2 | estimation_fit, own:boost-precision-from-variance-components-not-scaled-error |
| Forum / forcing event / org family | funder_or_donor (the foundation's grant committee releases the boost on the centre's placement) / purchase_order_or_contract (the 2027 fieldwork contract is let on the placement) / research_or_statistics_office |
| Stakeholder | the survey director of a university survey research centre (statistical_office_head); the prompt carries no persona |
| People (guard.py names --geo CA --seed 311) | Kristin Schmidt, survey director; Jeremy Morris, the foundation's programme director; Jason Clarke, the centre's sampling statistician |
| World | a provincial health survey run by a university survey research centre for the province's health ministry since 2019, two-stage (sampled areas, then dwellings), three waves 2023 to 2025 in five health regions; a foundation funds 1,200 extra interviews in one region in the 2027 wave, taken in that region's 2025 sampled areas |
| Deliverables | boost_region_2027.xlsx (the placement workbook), boost_memo_2027.docx (the memo to the foundation) |
| Guard | WARN only: three_rules.strategy_risk (grain_or_unit, answered by the analyst test below), overuse.objective (the lane's), repeat.gate_g (binding_constraint after task310: here the binding quantity is a variance component, not an export limit) |

**The data-native sentence:** the survey's interviews are taken twenty or so to a sampled area, and in the North the
outcome clusters by area (whole communities share one pharmacy and its prices), so most of the North's sampling
error sits between areas; the boost adds interviews inside the same areas, which shrinks only the within-area part,
and a region whose error looks widest gains least.

## Default path

1. Read the foundation's terms: the boost goes to the region where it most reduces the standard error of the
   region's 2027 estimate of adults who did not fill a prescription because of its cost.
2. Join the two fieldwork contractors' interview files, recode the 2024 boundary change, drop partial interviews
   below the filed completeness, compute each region's 2025 prevalence and its design-based standard error with
   sampled areas as clusters (the centre's technical report method).
3. Project each region's 2027 error by scaling its 2025 error by the square root of its interviews before over
   after the boost (the design effect held at its published value).
4. Fund the region with the largest fall.

**Ends on:** the North, whose 2025 error is the widest and whose scaled fall is the largest.

**Golden (to be fixed on the generator's truth):** projected from each region's between-area and within-area variance
components with the boost spread over its existing areas, the North's error barely moves and a low-clustering region
(Central Valley in the prototype) gains most, by about 1.6 times the next region.

## Stump sentence

A competent analyst computes each region's 2025 standard error correctly with the sampled areas as clusters, scales it
by the square root of the region's interviews before and after the boost and funds the North, where the error is
widest; but the boost's interviews go into the North's existing areas, most of whose error is the difference
between areas, so projected from the variance components the boost barely moves the North and belongs to a region
whose prevalence hardly clusters.

## Three rules

- **Task type:** survey-research-official-statistics / sample-design-allocation-weighting, which serves Opportunity
  Sizing: the boost is sample allocated to one region and sized by the precision it buys.
- **Domain test:** the deciding quantity is the standard error a two-stage clustered sample gives a regional
  estimate, which survey sampling projects under a changed design from its between-area and within-area variance
  components (the cluster take enters the design effect).
- **Swap:** "put the 1,200 extra interviews in Central Valley, where the prevalence hardly clusters by area" becomes
  "put the 1,200 extra hospital beds in Central Valley"; beds have no sampling error, no areas within which they are
  drawn and no variance components, so the projection has nothing to act on.
- **Layer 1:** two contractors' interview files with different code frames and date formats (each contractor's
  CAPI export); a 2024 health-region boundary change recoding some areas (the ministry's reorganisation); partial
  and proxy interviews with outcome codes; reissued cases under new case numbers; the weights file keyed on the
  pre-2024 area codes. Nothing placed to be caught; each mishandling is asserted to leave the call.
- **Layer 2:** estimation_fit: the design's variance splits between and within areas, and the choice that flips the
  call is projecting the boosted error from those components instead of scaling the present error by the count.
- **Decisive step:** recognising that interviews added inside fixed areas reduce only the within-area variance, and
  projecting each region's 2027 error from its estimated variance components (its intraclass correlation and the
  boosted cluster take).
- **Not semantics:** every field read correctly (the contractors' codes, the boundary recode, the outcome codes, the
  completeness rule) still leaves the analyst with the correct 2025 error, and scaling a correct error by the count
  is the natural projection; no field or definition says how the error splits between areas.
- **Not rule application:** no filed rule projects an error under a new design; the terms file the objective (the
  fall in the 2027 standard error) and the boost's placement (inside the 2025 areas), and executing them with the
  present error scaled by the count funds the North. Spread: to be measured on the generator's clean truth (the
  enumerated family, SRS, scaled design error, published design effect held, components by ANOVA, by random-effects
  fit, pooled over waves or 2025 only; the standing family the component projections), with the ruling-out read
  from the data, not from a filed clause.
- **Analyst test:** a strong analyst who joins both contractors' files, applies the boundary recode and computes
  each region's 2025 design-based error scales it by the square root of the interviews before and after the boost
  and funds the North, where the extra interviews in the same few areas buy almost nothing.
- **Estimand:** the foundation's terms (section 2) file the region as the one whose 2027 estimate's standard error the
  boost reduces most, the error computed as the centre computes every regional error (technical report section 4),
  the 2027 wave keeping the 2025 design with the boost's interviews taken in the funded region's 2025 areas.
- **No decoy:** nothing is planted: the published design effects are the technical report's ordinary table, and no
  memo, draft or stakeholder figure names a region.
- **No certified replay:** the method is not recovered by reproducing a certified figure; no file states a 2027 error.
- **Lesson:** precision bought by added sample is set by where the variance sits, not by the size of the present
  error; no build on file teaches projecting a clustered design's error under a changed cluster take.

## Tried and rejected

- Seed OS13's co-located charging sites as one site: the call turns on reading the federal site definition (data
  semantics); its state energy office repeats task310's organisation family; set aside.

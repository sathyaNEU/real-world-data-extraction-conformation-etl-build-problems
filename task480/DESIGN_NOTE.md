# task480 design note: the 2026 municipal population estimates and the road aid formula's urban tier

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

Architecture 3, drawn 2026-10-31 after architecture 2 (the vehicle retirement program's NOx counties) was spent at
stage 4 of its 10-30 reship (judge pass 2 SEND_BACK). Card `.claude/skills/fingerprint/cards/task480.json` (v3),
registered 2026-10-31T19:27:22Z; guard check WARN only.

- **Pairing.** Survey Research & Official Statistics / census-register-administrative-data-quality (client domain
  survey-research-official-statistics), objective Data Extraction & Conformation (ETL): a state data center conforms
  the county address points, the certificates of occupancy and demolition permits, the group quarters list and the
  2020 census block groups into the 1 July 2026 municipal population estimates it certifies to the state.
- **Shape 10, a scorecard against a threshold.** Each municipality's estimated residents on 1 July 2026 against the
  10,000 that the state's municipal road aid formula moves to its urban tier; the call is the set of municipalities at
  or over the line.
- **Decision.** designation_set, answer unit set_of_items, question form what; forum the Secretary of Community and
  Economic Development, who signs the aid determination (minister_or_cabinet), forcing event the statutory
  certification of the estimates by 15 December 2026 (statutory_or_regulatory_filing), org family
  research_or_statistics_office, stakeholder the state demographer (statistical_office_head).
- **Strategy.** composition_mix, decisive generator G13 (horizon mismatch): persons per occupied dwelling, measured on
  the 2020 stock, is applied to the 2026 stock it no longer describes; Gate G method_or_model_selection; Layer 2 family
  estimation_fit, pattern own:persons-per-dwelling-by-dwelling-age-in-the-housing-unit-method.
- **Data-native sentence.** A dwelling's household fills when the dwelling is new and thins as it ages: young families
  buy into new subdivisions and their children leave a decade or two later, so persons per occupied dwelling is a
  property of the dwelling's age, not of the place; a municipality's 2020 census average holds the age mix its stock
  had then, and the subdivisions built since 2020 sit in a few municipalities while others' stock has aged.
- **Sources.** The housing unit method (occupied dwellings times persons per occupied dwelling, plus group quarters)
  is the official subcounty estimator and this build's default path; the decisive step is the precondition it takes
  for granted, one persons-per-dwelling figure for a place's whole stock (`stumping` 1.3 and 1.4). Set aside earlier
  on file: the housing unit method as a golden (task176, the textbook at the bottom of the ladder) and dwelling
  completions lagging consents (task174); here the method is the default and its precondition the step.
- **WARNs answered.** shell.repeat reads architecture 2's prompt until this architecture's prompt is written.
- **Differentiation** (card): task229, task242, task476, task174, task461 and task501 share the structural triple
  (time, G13, method_or_model_selection) on cards, each with one line naming how its driver differs.
- **Personas** (`guard.py names --geo "United States" --seed 480`): Laura Rubio, Chad Neal.

## Tried and rejected

- 2026-10-20, at the draw: the seed's own quantity, each NUTS 2 region's GDP per head in PPS against 75 and 100 per
  cent of the EU-27 average: every input (regional GDP, average population, national PPPs, the EU average) is a
  published aggregate, so the categorisation is arithmetic once the NUTS version, the average and the vintage are
  read; the seed's three moves are data semantics and rule application by construction.
- 2026-10-20, at the draw: putting an estimate into the seed's quantity: rebuilding regions across a NUTS boundary
  that splits a NUTS 3 unit is task474 v1's and task476 v1's spent split driver; a nowcast of the latest year's
  regional GDP is Forecasting with an open estimator family; carrying the national statistics institute's coming
  benchmark revision into the regional figures through the overlap years recovers the institute's method from its
  own published vintages (a certified replay); a register's population over-coverage is the census-register ground
  task471, task448 and task455 have spent.
- 2026-10-20, at the draw: other worlds screened before this one: attendance rebuilt from tickets by a show-up rate
  conditioned on booking lead time (composition_mix sat in the ban window behind task481, and a yield conditioned
  on a per-case property and measured where the record is complete is task473's driver); length of stay from
  stock over entries by Little's law (one divide, readable); weekly overtime from biweekly totals (the after-migration
  ratio per site lands the golden); direct-store-delivery shortages against theft (the warehouse-supplied categories
  are an unaffected subset that ranks stores with no model); a pooled percentile from published percentiles (the
  "never average percentiles" reflex reaches the mixture).
- 2026-10-20, stage 2: the under-registration rising with meter age, fitted by age: linear, quadratic and banded fits
  of a slope of 0.3 points a year moved the town-centre zones' indices by 0.05 to 0.1 across forms, so the graded
  indices forked; the meters' error is now one level for the mechanical fleet, varying meter to meter.
- 2026-10-20, stage 2: the town-centre flats exchanged last and the suburbs first with only a class-level summer:
  every pooled control landed within 0.5 points of the golden by composition (already-exchanged suburbs match the
  exchanged suburbs), so the first reflex reached the call; the rollout now opens and closes on town-centre zones and
  2024 was a normal year, so every pooled and tariff route over-corrects.
- 2026-10-20, stage 2: route reads spread nine days either side of the quarter end with estimated reads at 4 per
  cent: the smeared mechanical quarters put the per-meter averages 0.4 to 1.0 points under the volume share and pulled
  the tariff route's per-meter median onto the golden; reads now fall within three days of the quarter end and 1.5
  per cent are estimated.
- 2026-10-20, stage 2, asks: contracts in force at the end of 2025 (no device a reader would not adjudicate from the
  status and date columns); mains failures across a work-management cutover (migration duplicates are executed by
  the hygiene battery, proven-in-production Part 2); asbestos-cement length across a material-code renumbering (the
  old code book is nowhere in the pack, so the device is not fair).
- 2026-10-21, architecture 1 spent at stage 4 (the water utility's zone leakage index, the old meters'
  under-registration read across the staggered smart-meter exchange against same-type premises whose meters did not
  change): scored leak reader 2 landed the call, eight zones at 4.3 per cent, by netting each exchanged meter's step
  against unchanged premises of the same type and checking it with a placebo, and reader 1 filed seven with type
  controls stratified by consumption band, so the matched comparison is a medium reader's reflex once a staggered
  rollout is visible; both readers kept all 32 ask figures (the SCADA UTC stamps fell to the daylight-saving shift of
  the night profile, the GIS 2008 install-year placeholder to its spike and the works register); the judge returned
  DETERMINISTIC with FIX_NOW on the 4.3 per cent figure, whose estimator family spans 3.5 to 4.5 per cent against a
  printed unit of 0.1. Re-rooted fresh by the author's rule: no staggered rollout or treated-against-untreated
  comparison in the new world, every graded figure printed at the precision its estimator family supports, and no ask
  device a clock profile or a value spike can find.
- 2026-10-21, stage 2: the 2027 program's model years 2001 to 2010: their 2027 ages, 17 to 27, sit at the thin old end
  of the readings, where an exponential decay of yearly miles fits the one-year means as well as the quadratic
  (chi-square 33 against 33 on 27) and puts every county 4 to 5 per cent higher, so the whole tons forked across
  forms the record cannot separate; the program now takes model years 2005 to 2014, whose 2027 ages lie inside the
  bulk of the readings, and the fifteen-member family agrees in every county.
- 2026-10-21, stage 2: first sales centred three months before the model year began: the cumulative curve then has an
  intercept, and fits through the origin or of the lifetime average moved every county by 4 to 7 per cent; first
  sales now centre on 1 January of the model year.
- 2026-10-21, stage 2: county-by-county curves on the counties' first random draws spread up to 9 per cent around the
  pooled curve; each county's draw is now the one whose own curve agrees with the pooled one, and its intensity sets
  its level mid-bin.
- 2026-10-21, stage 2, asks: station numbers given again only between counties whose drivers do not cross left three
  counties' counts unchanged under the current licence; each reissued pair now shares a commuting corridor.
- 2026-10-21, stage 2: a lane computer's re-sent March 2025 rows (exact repeats at one station): a copied block is a
  plant kind even when the call ignores it; removed.
- 2026-10-21, stage 4 round 1, ask B: the station register's licensed_since column: both scored readers compared each
  test date with it, took the 2024 report's county before it, and kept all twelve station figures (score_reader 20 of
  44 each, call missed by both on the default path); the register now carries no licence date, so the reissue is a
  cross-file conflict and the hand-over is the pause in the number's own tests.
- 2026-10-21, stage 4 round 2, ask B: with no licence date on the register, reader C still split each reused number
  at the pause in its tests and kept all twelve station figures, and reader D kept seven from the 2024 report's
  closure dates; a station number reused across counties is a map every careful reader reconciles, so the station
  ask is retired, the register stays as a declared distractor, and the ask layer is the pilot (0 of 8 for all four
  readers).
- 2026-10-31, architecture 2 spent at stage 4 of its 10-30 reship (judge pass 2, `determinism_check_report_pass2.md`):
  NOT_DETERMINISTIC and SEND_BACK. Guidelines 3.3 file the reading as the evidence and no criterion selects the
  cumulative curve's form: a linear cumulative fit files six counties (Dunmarsh at 10.29 tons) against the golden's five,
  though the readings reject it (chi-square 5,820 against 30), and the pilot ask's "retired" (679 against 741) rests on
  a code meaning. The first judge (10-21) had approved with both as watch items. The sentence that would close the first
  fork names the decisive step (a fitted mileage curve), so the fork is the stump and the slot re-roots.

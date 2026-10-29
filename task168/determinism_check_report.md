# determinism-check report, task168, 2026-10-28

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting (secondary: method_or_model_selection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The fork the portal's second judge pass found — a refusal's route and direction attributed by the record's own `orig, dest` (giving a 47,484 turnaway total) versus by its `flight_no, dep_date` looked up against `rm_booking_build_s25.csv` (giving the committed 50,632) — is closed by the single-sentence repair to `data_dictionary_rev5.pdf`: the refusals table's `orig, dest` now reads "IATA airport codes of the journey requested," standing beside the pre-existing "flight_no, dep_date: the departure requested." The isolated judge thread independently verified that every one of the 9,040 network-wide rows (3,853 on the nine Linate routes) where a refusal's own `orig,dest` disagrees with the operating leg's is a GDS connecting-itinerary record (e.g. event 51000150, flight 2106/2025-03-30, CTA→LIN operating leg but CTA→LHR on the refusal's own fields); reading `orig,dest` directly would silently drop genuinely-refused Linate demand rather than reassign it to a different one of the nine routes, which the prompt's "turned away from summer 2025 departures... because the flight was full" (a specific operated leg) does not license. The main recommendation (175,000) and both critical components (1,044,148 passengers carried; 6,418/7,560 sold-out departures) reproduce exactly from the shipped files, and nothing else in the pack changed except the SQLite container's library version (confirmed byte-identical content).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Summer 2025 passengers carried, nine routes | 1,044,148 | 1,044,148 (dcs_flight_close_s25.csv, pax_flown) | yes |
| Summer 2025 sold-out departures, nine routes | 6,418 of 7,560 | 6,418 of 7,560 (rm_booking_build_s25.csv, sold_out_utc populated) | yes |
| Seats added by gauge change | 620,224 | 620,224 (summer2026_capacity_plan_v3.xlsx, "Gauge changes" sheet) | yes |
| Turnaway total, committed method (flight_no/dep_date) | 50,632 | 50,632, all 18 route-direction figures exact | yes |
| Turnaway total, orig/dest-direct alternative | — (not committed) | 47,484 | yes — a real, quantified fork, closed by the dictionary text, not by data incapability |
| Main call, 175,000 (censored own-month demand build, Solution Steps 3-6) | 174,865 → 175,000 | spot-checked for internal consistency/plausibility only, not independently re-derived step-by-step | not fully re-derived (scope note, not a finding) |

## Competing answers that survived
None, for either committed answer. The orig/dest vs flight_no/dep_date fork on the 18 turnaway figures (SF11 in the design note, the finding behind the portal's second judge pass) is the only candidate fork identified, and it is closed: the judge thread confirmed the dictionary's two now-distinct field definitions, together with the prompt's "departures... because the flight was full" framing, leave only the flight_no/dep_date reading defensible. The main recommendation's censored-demand construction was not independently re-derived line by line this pass (see ledger above), so residual risk there is a scope limitation of this review, not a surviving fork — the design note's ladder (167,917–184,813 family spanning two-thirds of the 25,000 bin) and its holdout-separated method table were not re-litigated by the isolated thread.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | ≥10 | 14 | pass |
| Format mix | ≥3 | 4 (csv, pdf, sqlite, xlsx) | pass |
| Large file | ≥25,000 rows or large DB | booking_engine_refusals_s25.csv 142,969 rows; ym3_leg_history_s24.sqlite 740,880 rows across 3 tables | pass |
| Distractors named, not in filenames | ≥2, named in metadata.json, unused | fare_report_IS25.xlsx, competitor_seats_IS25_IS26.csv — generic names, neither in Solution Steps, judge confirmed unreferenced | pass |
| Distractor relevant enough to weigh / arithmetic rule-out | each distractor unused yet weigh-worthy | fare_report_IS25.xlsx (fare families) and competitor_seats_IS25_IS26.csv (rival capacity) both plausibly relevant to an upgauge-demand forecast; design note does not record a specific arithmetic-reproduction/rule-out line for either, so this sub-gate is unverified rather than failed | not fully verified |
| Deliverables | 1-3, present in golden, no format family required | 2 (summer2026_upgauge_forecast.xlsx, summer2025_turnaways.pptx), both present in golden/ | pass |
| Asks multi-dimensional with unit/rounding in sentence | required | 18 route-direction turnaway counts, each whole-number, plus the main figure to the nearest 25,000, both stated in prompt.txt's own sentence | pass |
| Prompt shape / rubric ≥25 criteria | required | design note's Shape line: 25 criteria (1 call, 2 critical components, 18 route-direction counts, 2 slide/label criteria, 2 file criteria) | pass |
| LLM-generated tells | none | judge's hygiene pass: dated revision/issue headers, named owners, migration cutover, mixed snapshot cadences, realistic noise; no boilerplate or tidy-uniformity tells | pass |

## Gate G reconciliation
Judge's Gate G/H line: `mechanism: forecasting` (secondary `method_or_model_selection`), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`; Gate H `domain: pass`, `layers: pass`, `decisive_step: analytical`. This matches the design note's card (`stump_class: analytical`, with `analyst_test` and `domain_test` sections present) and its `## Three rules` section (domain test on censored-demand projection detruncation, swap test against hospital wards failing, Layer 1 = RM-system migration/DCS lap-infant split/refusal-log channel split, Layer 2 = estimation_fit censoring/truncation, "No decoy", "Not semantics", "Not rule application" each present and argued). No mismatch: the judge did not name either declared distractor (fare_report_IS25.xlsx, competitor_seats_IS25_IS26.csv) as the surface read carrying the task — it confirmed both are unused and non-load-bearing, consistent with the card. The judge separately and correctly noted that the supplementary turnaway ask's own difficulty is data-semantics (reading flight_no/dep_date vs orig/dest), which the project's rules explicitly permit on asks (Rule 3 binds only the main call's decisive step). This is a landable call under `stumping` 1.3 (library methods — censored/truncated demand completion via projection detruncation — are a textbook route a strong RM analyst takes; a strong model still has to find the right reference population, not just know the method exists), consistent with the design note's method table (projection/month-build vs pooled, EM, Tobit, additive-pickup alternatives all separated by holdouts). No Gate G/H finding; no send-back predicted from this axis.

## Stump power (Gate F)
Judge: the main call's trap is demand-forecasting/method-selection on honest numbers — naive extrapolation of the 2025 gauge-change uplift ratio (~500,000) or a pooled/coarse-period booking-curve build (~230,000–270,000) is the natural wrong turn for a capable analyst, because July/August departures sell out far earlier and deeper than the shoulder-season departures that dominate a pooled or coarse build. This matches the design note's P(one) ≈ 0.14 estimate and its method table's holdout-separated wrong rungs (0.80-ratio at 500,000; pooled build at 225,000; EM/Tobit variants at 100,000–200,000). The judge did not independently re-derive the censored-demand construction (Solution Steps 3-6) step by step, so its stump-power read rests on the design note's documented holdouts plus plausibility, not a full re-litigation — flagged above as a scope note, not a finding.

## Findings, ranked
None. The single open item from the prior portal round (the orig/dest vs flight_no/dep_date attribution fork) is closed by the data-dictionary edit, verified independently by the isolated judge thread with its own quantification of the fork's size (50,632 vs 47,484) and its own trace of every mismatching row to GDS connecting itineraries. No other gate failure, hygiene issue, or Gate G/H mismatch was found.

## Next action for the author
None required — ship as-is. If a further pass is ever warranted, the only item not independently re-derived this round was the full censored own-month demand build behind the 175,000 main figure (Solution Steps 3-6); re-derivation would increase confidence but nothing in this pass or the design note's own ladder/holdout evidence suggests it would change the call.

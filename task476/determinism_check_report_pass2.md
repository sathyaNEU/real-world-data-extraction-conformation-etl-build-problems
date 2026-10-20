# determinism-check report, task476, 2026-10-20 (architecture 2, pass 1)

## Verdict
DETERMINISTIC (SOLUTION_WRONG, minor: a component's window label)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor (the card files method_or_model_selection: the decisive step is the choice among start estimates, forced by the call log), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Fixes applied
The pack now starts in 2016, so the 2016 to 2026 profile is the file's own (62.6 per cent December to March); guidelines 3.1 says a customer is a meter; guidelines 2.2 names Central time. Re-judged once (pass 2).

## Thread verdict (verbatim)

# Verdict, task476, run r2

- **Verdict:** DETERMINISTIC (SOLUTION_WRONG, minor: Critical Component 1 mislabels its window)
- **Disposition:** FIX_NOW. Restate Critical Component 1 as 62.3% of the 2015 to 2026 confirmed-call starts (62.6% for 2016 to 2026 as written), or change the figure to match the window. The prompt and files are unchanged, so no model rerun is needed.

## Why
The shipped files force one set, Brennan Hill, Elmwood, Fenwick, Harlow and Ivers. The guidelines fix the rates, the end of the emission window, the numerator and the denominator. The only open step is the start date of a survey-found leak. The one start-date record in the package is the odor-call log, where the guidelines treat the call as the start, and it is strongly seasonal (Dec to Mar is 62.3 to 62.6%). Every seasonal weighting I tried gives the same five districts, with margin: the lowest designated district is Harlow at 3.69 and the highest non-designated is Juniper at 2.95, against a line of 3.30.

## Evidence (recomputed from target/)
| Item | Result |
|---|---|
| Leaks found in 2026 on cast-iron and bare-steel mains (613 survey finds + 278 confirmed calls) | 891, matching the district counts in the golden (72, 78, 68, 49, 114, ...) |
| Methane per mile, seasonal expected start (month-share and per-day weighting; local offsets of 4 to 8 h; profile 2016 to 2025, 2023 to 2026, two-level) | The five districts at or above 3.30 every time. Brennan Hill 3.78, Elmwood 3.76 to 3.78, Fenwick 3.76, Harlow 3.69 to 3.76, Ivers 3.73. Non-designated: Juniper 2.95 to 3.13, Dorrance 2.9, Calder 2.8, Ashby 2.7 to 2.8, Lockwood 2.7 to 2.8, Kessel 2.5, Glenmora 2.3. |
| Start fork (survey leaks) | Find date: no district reaches the line (max 1.49). Midpoint between surveys: Ashby 3.39, Elmwood 4.59, Ivers 3.47 designate (3 districts, a different set). Seasonal profile: the 5-district set. |
| Cost, 2026 less 2025, by the leak's own district, cost-to-date semantics | Reproduces all 12 district figures exactly (Ashby 391,294 ... Elmwood 617,746). The semantics are confirmed by 1,231 of 1,231 closeout totals equalling the sum of each type's last line. |
| Interruptions, one per (leak, address), meters from meter_premises | Reproduces all 12 figures exactly (Ashby 94, Calder 144, Elmwood 184, Fenwick 40, ...). |
| Critical Component 1 | Calls 2016 to 2026 give 62.6% (n=2,944). The stated 62.3% only reproduces for 2015 to 2026 (62.26%, n=3,188). Labeling error only, no effect on any answer. |
| Local-time zone | Not filed, but call-versus-repair ordering shows the offset is at least 4 h, and no call falls near a year boundary (only L25-09531 and L26-10422 are close), so the choice cannot move any figure. |

Residual forks, none of which flip the committed answer under the filed text:
1. The start estimator for survey leaks is not named in the prompt or guidelines. The midpoint is a defensible-looking easy route that files three districts. I rate the seasonal route as forced because the call log is the only start evidence and is overwhelmingly seasonal, but a literal reader could still file the midpoint. This is the main determinism risk. The cleanest repair would file the estimand ("each surveyed leak's start taken as expected from when leaks begin, per the shipped call history") without naming the weighting.
2. "Customer" in the interruptions ask is read as meters. The alternative, counting service addresses, gives different figures (Ashby 47 and so on). meter_premises is the only customer-count source for the premises, so I judge the meter reading as intended, but the unit is not stated in the prompt.

## Files/Hygiene
PASS. 13 files in 4 formats (csv x9, pdf x2, xlsx, txt). One file is over 25,000 rows (meter_premises, 71,543). Distractors: LAUF report, district_customer_counts_2026.xlsx. The extract notes read as a data-extract description and do not hand over the method. The cost-to-date semantics are not documented in the shipped notes, which keeps that ask's device live. No authoring or benchmark disclosure, and dates are consistent (extract 15 March 2027, memo due 20 April 2027). There is no public-data contamination signal. Not exclusion-level.

## Stump power
Good. The easy route is the midpoint start (or the find date), and it files Ashby, Elmwood and Ivers, a wrong three-district set. A capable analyst who cleaned the data and read every rule would likely take it. The hard step is noticing that the call log is seasonal and uses it to weight the unobserved starts. The asks add independent traps: cost lines are cumulative to date, the cost center is not the leak's district, ticket duplicates, and meters per premise.

## Stumping type
`mechanism: statistical_rigor`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The difficulty is estimating interval-censored leak starts from the seasonal start profile. No reported figure is misleading, and on clean data the task still stumps. The decision depends on an estimand-level choice, not on catching a planted defect.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. The field's own work, estimating methane emissions from leak inventories with interval-censored start dates and seasonal start timing, decides the call. The easy route, a midpoint or find-date start, gives 3 districts (Ashby, Elmwood, Ivers) or none. Layer 1 is UTC against local time, grade codes A/B/C against 1/2/3, duplicate tickets, cumulative cost lines and change-over of survey cycles. Layer 2 is the seasonal-start estimator.

## Fix
- **solution:** correct the Critical Component 1 window label (62.3% is 2015 to 2026; 62.6% is 2016 to 2026).
- **prompt (optional hardening, not required):** state "customer" as meters, and file that survey-found leaks are dated from when leaks begin, to close the two residual forks without naming the weighting.

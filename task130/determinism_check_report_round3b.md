# Verdict, task130 (fresh pass)

**Verdict:** DETERMINISTIC (minor SOLUTION_WRONG wording in SOLUTION_STEPS step 4, see Evidence).

**Disposition:** APPROVE. No rerun needed. Optional in-house clean-up: reword step 4 ("some in every year to 2024" is false for Brennick in 2020). The main call's one soft spot (below) is a prompt/policy wording choice for the author, not a required repair.

**Why:** The $1,250,000 is the expected cost of Claims first made in 2027 from incidents on or after each entity's Transition Date (Agreement 1.3, 2.1, 2.2; Policy 3.1 to 3.4). That figure is forced by the files once the report-lag structure is read from the register. The register shows zero Claims made within 30 days for any 2016 to 2018 incident, and a steady cluster (about 14% of claims, bimodal at under 30 days) for every incident year from 2019. Incidents from 2025 to 2026, outside the experience, keep showing the cluster (9 to 26 per quarter), so the 2016 to 2018 delays do not predict 2027. The supplementary answers all reproduce. Governing taxonomy label: none. Residual risk: Policy 3.3 literally names 2016 to 2024 as the experience, so an "all years" lag run is a licensed-looking alternative that gives $1.0M. See the fork table.

## Evidence (recomputed from the bundle)

| Item | Result | Source |
|---|---|---|
| Experience Claims, 2016 to 2024, Covered Clinicians (Schedule B job in incident month, both code sets), merged per incident_no, earliest claim_made | 3,320 (reproduced) | rm_claims_register + clinician_fte |
| Covered paid FTE-years, 2016 to 2024 | 13,747.07 (reproduced) | clinician_fte (cls via Schedule B) |
| Claims made within 30 days, by incident year | 2016 to 2018: 0. 2019: 45, 2020: 49, 2021: 40, 2022: 64, 2023: 47, 2024: 50 | register |
| First fast Claim by entity | AMC 2019-01, TFH 2019-04, CMG 2019-05, BCH 2019-07 | register |
| BCH fast Claims by year | 2019: 3, 2020: 0, 2021: 4, 2022: 1, 2023: 5, 2024: 4 | register |
| Contribution, delay-aware, each entity's experience from its first fast Claim (my own day-level build: Claims at trended cost, counted per 2027 plan FTE-year with delay <= days left to 31 Dec) | entity-only 1,259,592; pooled by class with each entity's own start 1,281,536; pooled by class with common start 1,253,730 | staffing plan, Policy 3.4 at 5.0% from incident year |
| Same, any common start from 2019-01 to 2024-01 | 1.23M to 1.32M, all round to $1,250,000 | |
| Same on whole 2016 to 2024 experience | 937,175 to 961,261, rounds to $1,000,000 (matches the golden's foil) | |
| No lag awareness (frequency x average trended cost x plan FTE-years) | $16.8M (whole) / $13.2M (2019+) | easy-route wrong answer |
| Largest valued Claim vs the $2M limit | one trended 2.5M, a late claim, no effect on a within-year cost | |

**Supplementary reproduction**

- Ask 2 (missing open Claims). I used incident-level open status, excluded CONTRACT-line defendants, took incidents on or after the leaving carrier's first term (premium history), and matched by CL- reference, RMN- reference via notices, and suits via prior_claim_no, against the 09/30 loss runs. Results: TFH 1 / $1,465,000; AMC 3 / $7,000; CMG 4 / $54,000; BCH 0. All reproduce. Pre-term misses (TFH 4 / $1.44M under Halberd, BCH 1 / $1.676M under Tallis, AMC 6, CMG 11) are correctly excluded because those incidents sit with earlier carriers.
- Ask 3 (July to September 2026 FTE). Hours on lines whose profile maps through the crosswalk to a Schedule B PHY- or APC- code, over 173.33, by cost-centre entity, excluding residents' and fellows' additional positions. TFH 188.6/187.1/188.0, AMC 464.5/463.6/465.4, CMG 1,037.1/1,036.8/1,040.6, BCH 105.5/106.7/108.2. All reproduce. Summing the `fte` column by line instead would double count.
- Step 7 and step 8 values match the above. Step 4's "some in every year to 2024" fails for BCH 2020 (zero). The 30-day count is correct; this is a wording defect only and does not move any figure.

## Competing answers and forks

| Fork | Answers | Judgement |
|---|---|---|
| Lag from all 2016 to 2024 experience (Policy 3.3 read literally) vs post-2019 regime | $1.0M vs $1.25M | Data separates them: 0 of 960 claims in 2016 to 2018 vs about 14% fast after, persisting in 2025 to 2026 incidents. Weakest point of the build; a rigorous solver who tests lag stability lands on $1.25M, one who does not lands on $1.0M or $16.8M. |
| Start month: entity-own vs common vs 2022 | 1.23M to 1.32M | All round to $1.25M. Not a fork at the filed rounding. |
| Pooled vs entity-only class rates (BCH Primary Care has plan FTE from Oct 2027 but no BCH experience) | 1.26M vs 1.28M | Same rounded answer. |
| Resident or fellow moonlighting positions (83 GME workers, 1.2 to 3.6 FTE a month in total) | excluded (golden) vs included (+0.6 to +1.2 FTE per entity) | Agreement 1.5 says residents and fellows are not Covered Clinicians; exclusion is the better reading, but "while so employed" gives a small opening. Affects ask 3 at one decimal. |
| "Latest" loss run: Quillan 09/30 (run 10/06) vs 06/30 rev1 (run 10/09) | TFH 1 / AMC 3 vs TFH 5 / AMC 13 | Valuation date is the natural reading; the rev1 header states it replaces the 07/08 run valued 06/30. Low risk. |
| Open Claims counted with CONTRACT lines | adds 1 (TFH), 8 or 9 (AMC), 1 (BCH) zero-reserve | Excluded: ask says "under its policies", and the dictionary says CONTRACT is insured by the clinician's own group. |

No competing answer survives on the main call at the filed $250,000 rounding, other than the whole-experience $1.0M, which the files themselves disprove (back-test on 2025 to 2026 incidents).

## Files/Hygiene: PASS
17 files; formats: PDF (2), XLSX (3), CSV (10 plus), MD (1); the CSVs are the 224,767-row payroll history, 69,064-row safety events and 30,764-row HCM lines. Distractors available: patient_safety_events, defense_panel_invoices, QMPL 06/30 rev1 loss run, extract log. Provenance and temporal checks: nothing authored-looking in PDF or XLSX metadata (QMPL, Derek White, Nancy Holland creators), no "synthetic"/"benchmark" strings, dates coherent with an October 2026 setting (loss run valuation 09/30, plan 09/29, policy 09/22). Layer 1 mess is genuine (job code sets change 1 July 2020, HCM replaces payroll, carrier-specific reference formats CL2026xxxx and RMN26xxxx, two-cost-centre FTE splits, closed cost centres). Nothing exclusion-level. The cross-batch fingerprint check was not run (outside the readable directory).

## Stump power
Strong. Easy routes: (a) frequency x average cost x plan FTE-years = $16.8M, ignoring that a first claims-made year catches only claims reported within the year; (b) delay-aware but on the whole 2016 to 2024 experience = $1.0M (one rounding step off). Only a solver who tests the delay structure for stability and sees the 2019 regime shift lands on $1.25M. Asks add independent traps (CONTRACT lines, pre-term carriers, RMN and prior_claim_no matching, resident positions, `fte` double count). Estimate: a capable solver commits one of the two wrong answers for an analytical reason.

## Stumping type
`mechanism: forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported figures are all fine. The difficulty is a forward projection (claims made within the plan year, with a regime change in report lag that the pooled history mispredicts). On clean data the task would still stump.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: self-insured trust funding on a claims-made basis, i.e. reporting-lag and exposure-based loss costing (an actuary's own work); swap test fails to preserve meaning ("megawatt-hours" has no Transition Date or claim-made trigger). Layer 1: two job code sets, legacy vs HCM payroll, three carrier layouts and reference formats, revised vs latest loss run. Layer 2: lag-aware first-year claims-made costing with the post-2019 regime. Easy route a strong analyst would take after reading everything correctly: full-history exposure rating ($16.8M) or full-history lag ($1.0M).

## Fix
none required. Optional (prompt or policy 3.1, input_files unaffected): closing the one soft fork by adding to the prompt that the cost is on the claims process the System has today; this would change what solvers see and need a rerun, so it is not recommended unless the portal finds the 1.0M answer common among stumped runs. Solution: correct step 4 to say Brennick had no fast Claim from a 2020 incident.

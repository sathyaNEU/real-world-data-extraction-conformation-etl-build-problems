# Verdict: task130 round 2

**Verdict:** NOT_DETERMINISTIC (the golden's arithmetic reproduces fully; the failure is in what the filed text forces).

**Disposition:** SEND_BACK. The policy or prompt must pin the experience population and the entity-split basis (and the FTE entity attribution), which changes what solvers see, so a rerun is required.

**Why:** CPLT funding policy 3.2 defines the experience as "the System's own claims experience: the Claims arising from Medical Incidents from 1 January 2017 to 31 December 2024 against Covered Clinicians", with the exposure being "the Covered Clinicians' paid FTE in the System's payroll for the same years". There is no entity filter, and 3.4 ("rates its Participating Entities alike") points to a pooled rate. Executed word for word, with the lag-to-first-making window the golden also uses, this gives $312k (5.65 claims). The golden's $587k (10.2 claims) needs an unfiled extra step: restrict the experience to Tolliver Falls and Alderwick because the Early Resolution Program (ERP) reaches every entity from its Transition Date (Agreement 5.2). That is an inference from the data dictionary and the Agreement, not an instruction in the policy. Gate C/E fails on the main recommendation, with a second fork on supplementary 3 and a third on supplementary 5. Governing label: underspecified_objective (competing_defensible_answer for the pooled $312k).

## Evidence (recomputed from target/; all reproduced)

| Item | Golden | Recomputed | Source |
|---|---|---|---|
| Covered incident-merged Claims, 2017-2024 | 192 | 192 | register, 2 Oct extract, joined to the legacy payroll by employee and incident month; job code mapped through Schedule B |
| TFH+AMC Claims | 123 | 123 | same |
| TFH+AMC covered FTE-years 2017-2024 | 2,655.2 | 2,655.18 (TFH 749.48, AMC 1,905.70) | clinician_fte_by_month |
| Claims made within 120 days of the incident | 62, all at TFH/AMC | 62 (TFH 18, AMC 44; CMG 0, BCH 0) | register |
| 2027 exposure | 599.9 FTE-years | 599.92 (day-level, from each Transition Date) | staffing plan |
| Expected claims, ERP-hospital experience | 10.2 | 10.23 | day-by-day lag cut at 31 Dec 2027 |
| Contribution, ERP-hospital experience | $587,000 | $587,072 | same |
| Contribution, pooled System experience | $312,000 (the golden's own rejected alternative) | $311,825 (5.65 claims) | same |
| Split by exposure share | 111 / 201 / 260 / 15 thousand | 110,931 / 201,141 / 259,750 / 15,250 | policy 2 |
| Missing from carrier run | AMC 1 ($7,000); CMG 1 ($20,000); TFH and BCH none | same | AMC CL-2026-0049 (IR-2026-00725): reserves 5,000+2,000. CMG CL-2026-0093 (IR-2026-01310): reserves 0+20,000. TFH CL-2025-0092 is carried under prior CL-2024-0064 (Q24-02241). Matching needs the dash-less Stoneleigh refs, the RMN notice map, and the notice entity/date/category fallback. |
| September 2026 covered FTE by cost-centre entity | 106.9 / 271.5 / 525.0 / 53.9 | same (total 957.3) | HCM pay lines, crosswalk, cost-centre directory |

Class assignment (first-named clinician) was tested three ways. The result is identical in all three and the 26 two-class incidents do not move it. The $587k rounding is robust to this.

### Forks that survive

1. **Main call, experience population (Gate C/E).** Literal policy 3.2 is all System claims, which gives $312k. The golden's TFH/AMC-only experience gives $587k. A third defensible expert method keeps pooled frequency and severity but takes the lag pattern from the ERP hospitals; I computed about $820k. The package shows the lag split clearly: the ERP hospitals have median lag 120 days and 82% of claims made within a year, against median 556 days and 22% for the other entities. But no filed sentence says "cost the 2027 claims on the ERP hospitals' experience". The estimand is meant to be filed so its literal execution is the golden, and here it is not. This is the decisive step. Deciding it by inference is a Gate C failure, and solvers who miss it follow the filed policy.
2. **Supplementary 3, what each entity pays (Gate C).** The golden uses the exposure-FTE share ($111k, $201k, $260k, $15k), taken from policy 2, which is written for the quarterly instalments. The alternative is each entity's own expected cost, which is what slide 2 charts: TFH $183k, AMC $250k, CMG $149k, BCH $4k (ERP experience). CMG differs by $111k. The slide-1 payments then fail to match the slide-2 cost totals for each entity, and nothing in the files says which basis is intended. The word "pays" is not defined as exposure share.
3. **Supplementary 5, September 2026 FTE (Gate C).** The golden attributes FTE by the pay line's cost-centre entity, giving 106.9 / 271.5 / 525.0 / 53.9. The HCM `home_entity` field gives 105.7 / 269.9 / 527.2 / 54.5. Agreement 1.5 says "employed by a Participating Entity", which could be read as the home entity. Only the experience side of the golden (legacy `entity_code` is "of the cost centre") supports the cost-centre choice, and it is not filed for this question.
4. **Supplementary 4.** The golden excludes the 9 open CONTRACT-line claims (blank reserves). That follows from the data dictionary (CONTRACT is insured by the clinician's own group), so it is forced enough. Not a fork.

Smaller points that do not move the answer: policy 3.5 ("no development") sits uneasily with the lag-emergence step, but 2.4 and 3.1 require the window cut, and 3.5 only bars loss development, tail and distribution fitting, so it holds. Right-censoring of 2023-24 incidents is left as filed by 3.5.

## Files/Hygiene: PASS

16 files: csv x9, xlsx x4, pdf x2, md x1. Formats are csv, xlsx, pdf and md. Largest files are 121k rows (payroll) and 35k rows (safety events). Distractors: the 30 June revised loss run, premium history, patient safety events and carrier notices. The operational layer reads as real system output (carrier layouts differ, dash-less refs, a revised run, extract log). No benchmark or authoring language and no temporal contradiction was found (the staffing plan dates 29 Sep 2026, extracts 2 Oct, runs 5 to 9 Oct). No exclusion-level finding.

## Stump power (Gate F)

Real. The natural literal results are $312k (pooled), $3,617k (no claims-made window) and $966k (average severity), all rejected by the golden. Reaching $587k needs the ERP lag structure and the window cut together. A strong model could plausibly land on the filed pooled rate, and for that route the divergence is a fork, not an analytical error. Any stump credit depends on Fork 1 being closed in the filed text.

## Stumping type

`mechanism: method_or_model_selection (experience selection plus lag emergence under a claims-made window)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no` (borderline: the solver must override the filed all-System experience, which is a stated method rather than a misleading reported figure), `sole_data_defect: no` (clean data would still need the lag-window and experience-relevance judgement).

## Three rules

`domain: pass`, `layers: pass`, `decisive_step: analytical` (borderline, because it rests on an inferred rule not filed in the policy).

Domain: actuarial claims-made funding of a self-insured trust (frequency and severity by class, trend, reporting-lag emergence). It fails the swap test for non-insurance nouns. Layer 1 is the messy payroll, the register, the carrier run reference formats and the HCM and payroll switch. Layer 2 is the experience relevance and reporting-lag window. The easy route (the filed pooled rate with the lag cut) gives $312k.

## Fix

Location: input_files (funding policy) and prompt.
- Pin the experience in policy 3.2 or the prompt to the entities whose patients have the ERP, or state that the rate is to reflect the ERP, so that executing it literally gives the golden.
- State in 2 or the prompt that each entity pays its share of the exposure (or its own expected cost), and that the chart is on the other basis.
- State whether employment is by cost-centre entity or home entity for the FTE ask.

Rerun required.

# Determinism verdict, task253 (Reading Partnership 2027)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. Nothing to repair in the prompt or the files; no rerun needed. Optional note: the prompt's phrase "underlying average ... over many years" tells solvers the target is a latent quantity (see Stump power).

**Why:** Every committed answer recomputes from the shipped files. The count is the expected number of schools below 480 under LT-AS-04 (REML, fitted values per 3.4): 41.95, so 42. The Poisson-binomial mean (41.95), median (42) and mode (42) of the school count all agree on 42, so no differently-licensed summary of the count gives another number. The other counts (28 BLUP averages below 480, 56 raw averages below 480) are rejected by the prompt's own definition of "underlying average". Regional shares, students and kilometres follow from the same per-school chances plus two filed bridges (census Years 2 to 5 rolled to 2027 Years 3 to 6; the Nov 2026 hub plan over the stale Feb 2026 directory, guidelines section 4's "and back for every visit").

**Evidence (literal reading first)**
- Prompt, guidelines s2 and s3, LT-AS-04 s3.1 to 3.5: Year 5 reading only, random effects for school and year group within school, REML, fitted values, every school in whatever its size. Partner schools are not known until Term 1 2027 reviews (guidelines s3), so the count and the downstream figures can only be expectations. The prompt, "how many places", is the number of schools below 480, which the data can only give in expectation.
- Where the text is silent: (a) how to turn probabilities into a count: sum, median and mode all give 42; "top-N" or ">0.5" selection (28) contradicts "underlying" plus guidelines s3; (b) students: 2027 Years 3 to 6 = census Years 2 to 5 (roll-forward, no mobility) gives 7,072; the un-rolled Years 3 to 6 headcount gives 6,946 (regions 1,503/3,379/373/458/809/425). This is the one inference not stated in a file. It is the natural reading of "the students the places will serve in 2027" with an August 2026 census, but a literal reader could stop at current Years 3 to 6. Flagged as a minor fork, not disqualifying, because the prompt says "in 2027" and census day is the only enrolment source; (c) km: round trip (2x one-way) per school per fortnight, weighted by chance, each school once per fortnight per the plan (Week A or B); guidelines s4 states "and back for every visit".
- Hub assignment: using the Feb 2026 facilities directory instead of the Nov 2026 plan gives Haskwick South 31 students and 24 km, Kirkanby 6,728 km, so a different chart title. The directory is dated before Haskwick South opened (July 2026, Hubs sheet remark), and the plan is the 2027 servicing plan, so the plan governs; the files make this forced.

**Recomputation ledger**

| Value | Claimed | Recomputed | Source and field |
|---|---|---|---|
| Participating Y5 reading results | 30,956 | 30,956 (10,232 + 10,400 + 10,324) | legacy CSV YR_LVL=05, TEST_CD=RD, PART_CD=P; portal xlsx Year 5 sheet header row 5, Domain=Reading, Participation=P; 2026 CSV Year 5 reading participated; all rows join to the 264 register primaries, no duplicates |
| Grand mean | 496.5 | 496.48 | REML (own nested-model implementation, 3 year groups x 264 schools) |
| School SD | 16.5 | 16.47 | same |
| Year-group SD | 9.3 | 9.28 | same |
| Student SD | 69.9 | 69.86 | same |
| Sum of chances below 480 | 41.95 | 41.947 | posterior of school effect given 3 year-group means, fitted values |
| Schools with model average below 480 | 28 | 28 | posterior mean |
| Schools with raw 2024-26 average below 480 | 56 | 56 | pooled mean |
| Region shares (%) | MN 15.5, MS 25.6, N 12.2, W 16.7, S 14.1, C 15.9 | identical; sum 100.0 | register Region x chances |
| Students by region | 1,578; 3,530; 356; 768; 431; 409; total 7,072 | identical (7,072.2) | census_aug2026 Years 2 to 5, codes zero-padded to 4, x chance |
| Hub students | 3,068; 2,243; 725; 671; 365 (7,072) | identical | plan matched to register on name and locality (264 of 264, unique codes) |
| Hub km | 813; 1,957; 1,826; 1,593; 2,138 (8,327) | identical | 2 x road_km (hub_school_road_distances.csv) x chance; every assigned hub-school pair exists in the distance file |
| Chart claims | Haskwick South longest at 2,138 km | consistent with the ledger | (PNG not read, outside the permitted folder; values follow from the above) |

**Files/Hygiene:** PASS. 13 input files in 5 formats (csv x5, xlsx x6, pdf, docx, txt); largest tables ~108k and ~110k rows. Realistic mess: three different layouts and score precisions across sittings, title block above the header, zero-stripped census codes, abbreviated and variant school names and localities in the hub plan ("Nth", "Upr", "Hts", "Saint"), directory refresh predating a new hub. Distractors: literacy_PL_register_2026.csv, literacy_specialist_rates_2027.xlsx, facilities directory (stale) and the Year 3 and non-reading data. No authoring or provenance disclosure seen in the files read. The PDF standard and the docx guidelines state no answer figure. No exclusion-level finding.

**Stump power:** The wrong answers are real and tempting: 56 (raw three-year average below 480) and 28 (the model's shrunken school averages below 480, the standard output of the filed model), each a competent-looking count. The right one requires seeing that shrinkage compresses the spread, so the tail count must be built from probabilities. A strong solver who reads "underlying average" may reach 42; the 28 route is the natural LT-AS-04 output, so I expect most solvers on the main call to miss. The downstream asks add the ETL layer (name and locality matching, zero-padding, stale directory). Moderate difficulty, correct reason.

**Stumping type:** `mechanism: statistical_rigor / method_or_model_selection` `stumping_family: analytical_non_defect` `surface_read_dependency: no` `sole_data_defect: no`. The reported numbers (raw averages, fitted model averages) are all correct; the difficulty is choosing the right estimand (expected tail count of latent school means) and it persists on perfectly clean data.

**Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Education measurement: hierarchical (random-effects) estimation of latent school performance and a tail-count estimand is what the field itself does, and the swap test changes the task. Layer 1 is the messy joins and layouts across three sittings and hubs; Layer 2 is the shrinkage-aware tail count. The easy route a careful analyst takes is to fit LT-AS-04 and count model averages below 480 (28 places), or count the raw three-year averages (56).

**Fix:** none. Optional (does not affect determinism): state in the prompt or the guidelines that a 2027 Year 3 to 6 cohort is the August 2026 Year 2 to 5 cohort, to remove the single un-filed bridge; this changes what solvers see and would need a rerun, so it is not recommended unless the portal shows a split on ask 3.

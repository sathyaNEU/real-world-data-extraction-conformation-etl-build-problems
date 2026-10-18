# Determinism check report, task198 ARCHITECTURE 1

**Verdict NOT_DETERMINISTIC, disposition SEND_BACK**, on the 19-member bundle whose zip md5 was
2d0a08cf33b050578a0d0beefdafb64d, cut 2026-10-18. The architecture is spent and the number re-roots at
architecture 2; this report is the evidence for why, and it describes a pack that is being replaced.

**The finding, which the isolated reader reached independently.** Framework clause 4.2 files the
comparison, a queue's share against its own earlier quarters "which carried the same offered load", and
nothing fixes how closely "the same" must match. Three queues win across licensed readings: Contribution
queries under the nearest one to four quarters pooled, a load band of 0.05 to 0.2 or load read to one
decimal; Investment switches, which is also the plain highest-share answer, under a band of 0.22 to 0.3 or
load rounded to whole positions-equivalents; Member data corrections under five or more nearest quarters
pooled, or load divided by rostered positions, or no matching at all. Gates C and E fail on that, and Gate
H reads the decisive step as rule application, because executing the clause correctly is all the answer
needs.

**Why a pin does not save it.** Pinning the tolerance closes Gates C and E and finishes Gate F: with the
comparison filed and the tolerance filed, nothing analytical is left. That is the bind, and the rule it
earned is now in `determinism-check` section 1: what is left open after the WHAT is filed must be a method
with a defensible alternative, not a knob.

# Task 198 determinism review

**Verdict:** NOT_DETERMINISTIC (governing label: underspecified_objective, Gate C). Every supporting figure reproduces; the main call is forced only under one of several unfiled readings of "the same offered load".
**Disposition:** SEND_BACK. The framework text (an input file) or the prompt must pin how "same offered load" is matched; that changes what solvers see, so a rerun is needed.

## Enumeration written before reading the graded blocks (honest caveat)
The brief inlines the graded blocks, so I had seen them. I derived the answer from the files independently, listing every option first.
- Cases: stack Gemini and Orbit and resolve the 506 legacy_case_ref rows (all received Feb to Mar 2024, so FY2024). Convert Orbit received_utc to Irish time (standard 2.1). Count working days after receipt (3.1, 3.3 with the holiday file), subtract clock_stop_days (3.4), and compare with the target using strict ">" (3.2, 3.6).
- Framework 4.2 options for "same offered load" (load = cases x standard minutes / (420 x 0.88 x working days in the quarter)). Each is a plausible reading:
  - (a) the k nearest-load historical quarters, k = 1 to 6
  - (b) a tolerance band on load, narrow or wide
  - (c) load rounded to 1 decimal
  - (d) load rounded to whole positions-equivalents
  - (e) load divided by rostered positions (utilisation)
  - (f) no matching, all 12 history quarters
  - each pooled (cases summed) or as a mean of quarterly shares
- Prior of the winner: CQ if load is matched finely; IS (the plain highest share) or DC if matching is coarse or ignored.

## Recomputed figures
| Item | Golden | Mine | Status |
|---|---|---|---|
| FY2026 cases received | 19,222 | 19,222 | reproduces |
| FY2026 answered later than target | 1,799 | 1,799 | reproduces; the 30 Apr inclusion and the UTC vs local answer stamp make no difference |
| CQ cases / breach share | 6,480 / 12.4 | 6,480 (804 late) / 12.41 | reproduces |
| IS / DC / TI shares | 29.8 / 25.8 / 13.4 | 29.84 / 25.77 / 13.35 | reproduces |
| CQ load vs positions | 15.0 vs 16 | 15.01 to 15.03 vs 16 | reproduces |
| DC load | 4.7 on 5 (FY2026), 13.0 on 14 (FY2025) | 4.65 on 5; 12.87 to 13.16 on 14 | reproduces |
| TI worst on elapsed days before clock exclusions | stated | 46.9% late with exclusions ignored | reproduces |
| Chargeable cases Q1 to Q4 | 1,593 / 1,967 / 1,920 / 1,811 | same | reproduces |
| Chargeable cases total | 7,291 on 4,364 lines | same | reproduces |
| Top-10 schemes, members and rates | RMT-000 41,789, 125.4 and so on | identical for all ten | reproduces |

- **Charging extract:** it holds 4,557 lines, 7,583 cases, to 30 Apr 2026. Excluding the April 2026 (FY2027) lines gives 7,291 on 4,364 lines.
- **Rate labels:** every line is an exact multiple of its rate under the file's R1/R2 label, which always agrees with the charge date.
- **Members:** the trustee report's contributing plus suspended is the figure that governs. The register's active_members is the sponsor-level return and repeats across schemes. The trustee report's own wording settles this.
- **Figures that did not reproduce as written:**
  - Step 5 and the Final Recommendation say Contribution queries is furthest above "under every number of matched quarters". Using the k nearest quarters by load and pooled cases, k = 5 puts Member data corrections at 12.0 points above CQ at 10.6, and k = 6 puts DC at 15.7. The claim holds for k = 1 to 4 pooled, and for k = 1 to 6 if quarterly shares are averaged.
  - Critical component 1 says the 506 cutover cases are "counted once" in FY2026. They are FY2024 receipts and affect no FY2026 figure.

## The fork: what "the same offered load" means (framework 4.2, not defined in any file)
Gap = FY2026 share minus the matched-quarter share, in points.

| Reading | CQ | IS | DC | TI | Winner |
|---|---|---|---|---|---|
| k = 1 to 4 nearest load, pooled | 10.2 to 10.4 | -2.0 to 2.1 | 0.4 to 2.9 | 1.6 to 3.7 | CQ |
| load band +-0.05 to +-0.2, or load to 1 decimal | 10.2 to 10.6 | -1.0 to 8.6 | 2.9 | 2.5 to 5.9 | CQ |
| load band +-0.22 to +-0.3, or load rounded to whole positions-equivalents | 10.6 to 11.0 | 11.7 | 2.9 | 4.0 to 6.9 | **IS** |
| k = 5 or more, pooled | 10.6 | 4.0 to 4.6 | 12.0 to 15.7 | 3.6 to 4.0 | **DC** |
| load / rostered positions, k = 2 or more or any band | about 10.4 | -2.0 to 4.6 | 17.8 to 22.0 | 1.6 to 4.0 | **DC** |
| no matching, all 12 quarters | 11.0 | 11.7 | 20.5 | 6.9 | **DC** |

- **Nothing in the shipped text pins** the tolerance, k, pooled against mean, or load against utilisation.
- **The strict reading is the natural one.** The CQ, IS and DC Q4 quarters cluster tightly (15.02 to 15.03 against a next group at 14.87), and the data is plainly built for it.
- **Whole positions-equivalents is not an unreasonable rounding.** Positions are whole numbers, and the framework gives no precision. It returns IS, the answer a plain ranking gives, by 0.7 points over CQ.
- **Under the instruction that a fork closed only by inference counts as open:** it counts as open, and the answer flips.
- **Margin:** under the strict reading it is large (about 6 points over the next queue), so margin fragility is not the issue. The issue is an unfiled definition.
- **Not a competing queue on the data:** IS under strict matching is at or below its baseline, because its Q4-load quarters ran 29 to 32 per cent late.

## Gates
| Gate | Result |
|---|---|
| Cross-batch | not run; the brief limited me to the pack |
| A | Pass on every graded figure. Two claims fail to reproduce as written (k = 5 pooled; "counted once" in FY2026), both repairable in the solution blocks. |
| B | Pass. Every decisive fact is in a shipped file. The vocabulary check (positions-equivalents, offered load, clock exclusions) is satisfied by the framework, the work measurement standard and the service standard. |
| C | **Fail.** The matching of "same offered load" is unfiled and the winner flips as shown. The asks (1,799; the quarterly chargeable cases; the top-10 table) are closed. |
| D | Borderline. A split among careful solvers would trace to the matching reading and the pooled-or-mean choice, not to the data. |
| E | **Fail with C.** The decisive term "same offered load" has no precision. The prompt defers the method to the framework, which defers it to the reader. |
| F | Moderate to too easy once the framework is read (see below). |
| G | Passes on the shape (see line below), with a borderline note. |
| H | Borderline fail on H3 (see line below). |

## Files / Hygiene
**PASS.**
- **Count and formats:** 19 files in 7 formats (csv, json, pdf, xlsx and so on). Two files exceed 25,000 rows (Gemini 40,060; Orbit 42,481).
- **Distractors:** telephony, satisfaction survey, service_monitoring_export (calendar-quarter, with the clock exclusions ignored), and the register's sponsor-level members. No file names a trap.
- **Provenance and dates:** export dates agree with the 30 April 2026 extract. The charging extract carries April 2026 lines beyond FY2026, which is realistic mess. No authoring language was found.
- **LLM-generation tells:** none beyond uniformly clean, round-valued rosters. Not exclusion-level.

## Stump power (Gate F)
- **What would fail a strong model:** ranking by the largest share answered late (IS, 29.8, which sets the cleaner story), or comparing each queue with all of its own history (DC wins on that basis, 20.5 points, because the remediation years at 14 positions are included).
- **What 4.2 does:** it states the matched-load method, so a solver who reads clause 4.2 and computes load gets CQ. That is documented-method execution rather than discovery.
- **Lever, if a rebuild is wanted:** file the estimand and let the data separate the candidates, for example by validating a seasonal or load-adjusted baseline out of sample.

## Stumping type (Gate G)
`mechanism: statistical_rigor (confounding of a share by offered load and season; borderline single_conceptual_flip), stumping_family: analytical_non_defect, surface_read_dependency: no (borderline), sole_data_defect: no`
- The reported shares are all correct and nothing in the pack is a planted defect. On clean data the load-matched comparison would still separate CQ from IS.
- The lens swap (absolute share to excess over a like-for-like baseline) is stated by framework 4.2 rather than discovered, so route to live testing if the type is in doubt.

## Three rules (Gate H)
`domain: pass, layers: pass, decisive_step: rule_application (borderline analytical)`
- **Domain:** operations resourcing. Workload in positions-equivalents on standard minutes against rostered capacity is the field's own estimate; the swap test fails to rename it (hospital visits do not have a work measurement standard).
- **Layer 1:** a platform cutover with 506 overlapping cases, UTC against Irish time, a monthly-hours to FTE basis change, a renamed queue, sponsor-level against per-scheme membership, an extract with April 2026 charges.
- **Layer 2:** a like-for-like comparison against a load-matched baseline.
- **Decisive step:** the framework hands over the comparison and its unit, so executing it correctly gives the answer, which is rule application. What a strong analyst can still get wrong is the matching tolerance, which is an unfiled convention, not analysis.
- **Easy route and its answer:** rank by share answered late and file Investment switches (29.8), or compare with all own history and file Member data corrections.

## Fix
- **Where:** input_files (framework clause 4.2) or prompt.
- **What:** pin the matching without filing the method. For example, "quarters whose offered load, in positions-equivalents to one decimal place, equals the FY2026 quarter's" or an explicit tolerance, and say cases are pooled.
- **Solution blocks:** correct step 5 (k = 5 only with mean quarterly shares) and the "counted once in FY2026" wording of critical component 1 (the 506 are FY2024 cases).

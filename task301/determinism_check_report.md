# task301 determinism check (architecture 3)

2 isolated judge pass(es), each a Sonnet thread at medium effort that saw only a fresh unzip of target.zip, the prompt and the judge's system prompt, and opened the graded blocks only after its own derivation was on disk.

| Round | Pack | Verdict | Disposition | Action |
|---|---|---|---|---|
| 1 | ae2a4182 | NOT_DETERMINISTIC on the main call (underspecified_objective, Gates A, B, C; order kept; G PASS; H PASS) | SEND_BACK as labelled; a C repair by the gate table | guidance 3.9 files that only payments received in 2027 count, a claimed measure paying a newly entitled family once its claim is decided; the 2024 widening cohort re-cut so every claim-pace estimator puts A ahead by 1.39 or more; 'newly within the limit', the annex rules (award to the month the last child turns 18, suspended months lifted within three months) and the fieldwork reissue key filed |
| 2 | 3ab80e13 | DETERMINISTIC (order kept; F good; G PASS, forecasting / analytical_non_defect; H PASS) | APPROVE | none |

Architecture 2's record is in determinism_check_report_arch2.md.

---

# Determinism check, round 1 (2026-11-02): NOT_DETERMINISTIC on the main call (underspecified_objective, Gates A, B, C; order kept; G PASS; H PASS), SEND_BACK as labelled; a C repair by the gate table

Isolated thread, Sonnet at medium effort, on target.zip ae2a4182.

# Verdict: task 301 (a3r1)

Order kept: yes. derivation.md was written to disk before graded_blocks.md was opened. After opening it I corrected one bug of my own (open-ended awards) and re-ran the annex; the corrected run is compared below.

- **Verdict:** NOT_DETERMINISTIC (the annex and response-rate figures are SOLUTION-reproducible under the golden's readings; the main call is not forced).
- **Disposition:** SEND_BACK. The appraisal guidance has to file the estimand for "payments the household receives during 2027" (who claims, from when). The dwelling-key rule and the zero-children rule must be pinned. This changes what solvers see, so a rerun is required.
- **Why:** The golden funds A only through a claim-pace model that no shipped text files: solution steps 3 to 5 apply a "chance of crossing over claim month and decision lag" built from the April 2024 rise cohort in the register, plus 71.8 per cent coverage. Read literally, the guidance (3.3 to 3.7, plus the proposals text) has every household that meets the test paid, and that gives C (19,652 full year; 17,691 with a one-month lag; 12,700 to 14,100 at any flat take-up of 64.5 to 71.8 per cent) far above A (3,695). The call flips on a quantity, the monthly claim hazard, that has several valid estimates straddling the deciding line. Gates failed: A, B, C (taxonomy: underspecified_objective, with margin_or_boundary_fragility behind it). It is not a fabricated fact: the register carries the pace data, but the method for using it is unfiled.

## Evidence (recomputed from target/)
| Item | Golden | My value | Reproduces? |
|---|---|---|---|
| A, full year and 2027 (automatic, filed return, gross income under 28,000) | 3,700 (1,100 / 1,400 / 1,200) | 3,695 (1,094 / 1,424 / 1,178) | yes, from ecvv2026_households/persons (irpf_return_2025, irpf_gross_income_2025) |
| E | 300 | 320 | yes (nearest hundred) |
| C full year | 18,400 | 19,652 on the filed test (8,400 to under 10,800 computable income per equivalent adult); 18,439 only if households with complemento_familiar_now = 1 are also dropped | only under a convention the files do not state ("newly within the limit" is not defined at household level) |
| B, C, D "under 3,000" in 2027 | each under 3,000 | full year: B 7,785, D 6,658, C 19,652. With a flat monthly claim hazard h, C = 1,746 (h 2%), 2,775 (3.3%), 4,006 (5%), 6,987 (10%). C passes A (3,700) at h of about 4%. | no without the unfiled hazard model; the register band flow (about 300 initial grants a month, 9,093 since April 2024) over a band stock of about 9,000 households gives 3.3%, but dividing by unclaimed households (about 3,500) gives 8%, so C could exceed A |
| True CF coverage Dec 2025 | uses the department's 71.8% | register paid 15.1k to 17.0k over ECVV entitled households 23.4k gives 64.5% to 72.5% depending on the annex reading | the dept figure and the rebuilt figure differ, so even the take-up input is a fork |
| Annex, Mar 2025 (families, Valmesura / Las Cuencas / Sierra del Alba) | 5,622 / 5,055 / 3,797 | 5,605 / 5,037 / 3,783 (applying the zero-children rule); 5,622 / 5,055 / 3,797 without it | yes without the rule |
| Jun | 6,031 / 5,412 / 4,123 | 5,984 / 5,362 / 4,095; without the rule 6,031 / 5,412 / 4,124 | yes |
| Sep | 6,363 / 5,683 / 4,381 | 6,301 / 5,614 / 4,345; without the rule 6,363 / 5,684 / 4,385 | yes within 4 |
| Dec | 6,668 / 5,939 / 4,583 | 6,590 / 5,859 / 4,541; without the rule 6,670 / 5,939 / 4,586 | yes within 3 |
| Response rate | 7,132 / 5,172 / 72.5; 5,317 / 3,961 / 74.5; 3,672 / 2,834 / 77.2 | 7,185 / 5,172 / 72.0; 5,354 / 3,961 / 74.0; 3,700 / 2,834 / 76.6 on the dwelling code as filed. Merging reissues by municipality plus serial (118 dwellings whose census section changed) gives the golden's figures exactly | only with an undocumented key rule |

Forks the shipped text leaves open (answers shown):
1. Claim behaviour of B, C, D in 2027 (the decisive one): all eligible paid from February (C 18,845 to 19,652, the call is C) against a register-pace ramp (C under 3,000, the call is A) against flat 64.5 to 77.5 per cent take-up (C 12,700 to 15,200, the call is C). Literal execution of the guidance gives C.
2. "Newly within the limit": include or exclude households already receiving CF (C 19,652 or 18,439).
3. Annex: a family whose children under 18 net to zero through the 'Child reached 18' incidents (rules 2.1, 4, 8) is dropped (-17 to -80 per province-month, totals 14,425 / 15,441 / 16,260 / 16,990) or kept (golden, 14,442 / 15,490 / 16,333 / 17,190). The incident file is itself inconsistent (Q1 incidents dated on cases claimed in November; 1-child families with 'Child reached 18' who renew with 1 child).
4. Annex: suspended months paid in arrears count as paid (golden; rule 7.2) or not (about 250 fewer families a month).
5. Dwelling identity in the fieldwork file (code as filed against municipality plus serial after the April 2026 section change).
Competing answer for the main call: C, with 12,700 to 19,700 children (provinces about 5,800 to 9,000 / 3,900 to 6,000 / 3,000 to 4,600).

## Files/Hygiene: PASS
13 files: pdf x4, docx, xlsx x2, csv x6 (pipe, semicolon and comma layouts; mixed date and decimal formats in the register). Register 63,433 rows (25,000-row gate met). Distractors present: municipal_poverty_estimates_2024.xlsx, ecvv2025_households.csv, the coverage report. No authoring or generation tells found; dates coherent (proposals 28 Oct 2026, register extract 2 Nov 2026). No exclusion-level finding. The 71.8 per cent coverage figure in the department's report is a wrong-basis input that the golden itself uses, which is a Gate A concern, not a hygiene one.

## Stump power (Gate F)
Plausible: a strong model that reads the guidance literally, or applies the 71.8 per cent coverage as a flat take-up, picks C and is wrong against the golden, and the department's cost column invites the full-year view. But the failure is only "valid" if the claim-pace method is forced, and it is not (see forks 1 and 2); the A over C margin sits inside the range of valid hazard estimates.

## Stumping type (Gate G)
`mechanism: forecasting` (take-up and timing projection of a policy), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported numbers are fine; the difficulty is projecting who is actually paid in 2027. This shape passes Gate G.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: policy appraisal and take-up modelling for a benefit measure. Layer 1: mixed date and decimal layouts, retro revocations, suspensions, address moves, the census-section re-key. Layer 2: projecting claim behaviour. Easy route: count every eligible household as paid all year (or at a flat coverage rate), which gives C, 19,700 to 12,700 children, against the golden A, 3,700. The step is analytical in kind but, as filed, its method is not literal.

## Fix: prompt and input_files (the appraisal guidance), plus solution
- File the WHAT of 3.5 in the guidance: which households receive claim-based payments in 2027 (the population and window), without filing the computation. If the pace-from-register approach is the intended path, file a selection criterion the data separates (for example the stated denominator and the cohort the pace is measured on), and make the margin between A and the best claim-based measure clear of the plausible hazard range.
- File the "newly within the limit" convention for C, the dwelling key rule for reissues, and whether a family with no child under 18 stays in the annex count; or remove those incidents from the file.
- Rewrite CRITICAL_COMPONENTS 2 and 3 once the estimand is filed, and align steps 3 to 5 with it (the 71.8 per cent coverage conflicts with the rebuilt register coverage).

---

# Determinism check, round 2 (2026-11-02): DETERMINISTIC (order kept; F good; G PASS, forecasting / analytical_non_defect; H PASS), APPROVE

Isolated thread, Sonnet at medium effort, on target.zip 3ab80e13.

# Verdict (task 301, a3r2)

Order kept: derivation.md was written to disk before graded_blocks.md was opened.

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE (no rerun). Optional hardening: none required; residual risks below are low.
- **Why:** The recommended measure's figures (A: 3,700 = 1,100 / 1,400 / 1,200) and both annex tables reproduce exactly from the shipped files, and A is the only measure whose 2027 figure involves no unfiled modelling. Guidance 3.9 makes the claim-based measures (B, C, D) pay only after claim and decision, and the register's own claim history (April 2024 rise, October 2022 launch, claim-to-first-payment lag of about two months) separates A from B, C and D with a clear lead under every register-based model I ran. Governing taxonomy label: none.
- **Evidence (recomputed, all from the bundle):**
  - Eligibility populations reproduce the department's costs exactly (A 96,315 children = 32.4M; B 96,883 = 41.9M; D 62,126 = 38.8M; C 39,484 = 47.4M; E 30,033 = 12.6M), so who each measure covers is closed.
  - Full-year ceiling: A 3,695; B 7,785; D 6,658; C 18,439; E 320. A by province 1,093.6 / 1,424.0 / 1,177.6, region 3,695.3, which rounds to 1,100 / 1,400 / 1,200 / 3,700 (matches golden).
  - With 3.9 applied via the register: C about 1,600 (hazard of about 2.2 percent of the band a month, 27.9 percent by month 12 as the golden uses); B 2,386, D 2,213 (October 2022 launch curve, about 58 to 62 percent by month 12); B with a curve 35 percent faster still 3,221, and B needs about 1.55 times the observed pace to pass A. Golden's "B, C, D under 3,000, E 300" reproduces.
  - Annex 1 reproduces cell for cell (14,008 / 14,718 / 15,196 / 15,425 total; province split identical to golden) using decision_date <= 31 Dec 2025, row-wise appeal re-decisions, 2026 revocations ignored, province from territorial_codes (the register province column is wrong on 520 rows), address moves from the month after the report. Annex 2 reproduces (7,132 / 5,172 / 72.5; 5,317 / 3,961 / 74.5; 3,672 / 2,834 / 77.2); complete interviews tie to ecvv2026_households (5,172 / 3,961 / 2,834).
  - Surviving forks (all low): (1) take-up read as the 64.4 percent coverage rate with payments from March gives B 3,856 against A 3,695 and C 9,766; this ignores the register's claim timing, which 3.9 makes the governing evidence, so it is the wrong-method route the task is built to catch, not a licensed alternative. (2) Applying "Child reached 18" incidents dated before an award's first payment moves the annex by 1 to 5 families per cell; the register decision (granted) is the decision as it stood, so this is not a reasonable reading. (3) Keying dwellings on the string instead of reissue_of gives 7,185 / 5,354 / 3,700 eligible; reissue_of resolves it. No filed sentence names the claim-arrival model for B/D/C, which is why the margin to B (about 1,300 children) is the thing to watch.
- **Files/Hygiene:** PASS. 13 files; formats csv (7), pdf (4), xlsx (2), docx (1); register has 61,235 rows. Mixed date layouts, decimal commas, appeal duplicate rows, renumbered dwelling sections and a wrong province column read as system mess. Distractors present (municipal_poverty_estimates_2024.xlsx, ecvv2025_households.csv, coverage report, main-results PDF). Dates coherent with a 2 Nov 2026 setting. No authoring disclosures; no exclusion-level finding.
- **Stump power:** Good. The easy routes are the full-year ceiling (picks C at 18,400, the department's own costing logic) and a flat coverage-rate take-up (picks C 9,766 or B 3,856); both file a wrong answer. A strong model that reads 3.9 still has to build claim-arrival and lag curves from a 61k-row register with two date layouts and a wrong province column, and then notice A has no claim step. Likely to stump on the call and heavily on the annex whole numbers.
- **Stumping type:** `mechanism: forecasting` (take-up and timing projection, with etl_conformance in the annex), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Reported costs are correct; the difficulty is projecting which payments are actually received in 2027, and it survives clean data.
- **Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Swap test fails to transfer (take-up, claim lag and income-per-equivalent-adult poverty crossing are the field's own microsimulation work). Layer 1: mixed date formats, comma decimals, appeal re-rows, wrong province column, renumbered dwelling keys. Layer 2: claim-timing-adjusted poverty-reduction estimate. Easy route: rank on the full-year ceiling and recommend C (18,400, versus A 3,700) or apply a flat 64.4 percent take-up and recommend C or B.
- **Fix:** none (location: none). Watch item only: the claim-arrival evidence is in the register but no sentence names it; if the portal flags a fork, pin it by filing the claim population and window (what), not the curve (how).

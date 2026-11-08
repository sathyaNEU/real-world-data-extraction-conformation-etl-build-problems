# Determinism verdict, task306 (architecture 5, pass 2, the re-judge)

Judged cut: target.zip sha256 ea8155d76c3f5fbd4270d584eb3afe13fc41515101cce3b96f9025ed7394a0c7, 2026-11-08, after the fix of pass 1 (determinism_check_report_arch5.md). One isolated judge thread (Sonnet, medium effort) reading only the unzipped bundle and the graded blocks. The shipped cut a915483e differs from this one only in the ePACT2 summary's BNF label for the gabapentinoid line, a declared distractor no figure reads.

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. Every committed answer reproduced from the shipped files. Two advisory forks (below) do not move the main call or any graded cell beyond what the data themselves resolve; no rerun needed.

## Why
The call is forced by the programme specification section 3 (scope on 31 Dec 2026, chance of being off at six months times the table 1 harm rate at age on 31 Dec 2026, summed) once the pilot off-rate is conditioned on who started the medicine. That split is the only heterogeneity in the pilot (practice-started 63/136, 68/276, 65/192 off; specialist-started 1/24, 1/24, 2/48) and the 2027 population's specialist-started share is 86%, 6%, 44% against the pilot's 15%, 8%, 20%. Applying the pooled close-out rates (40.0%, 23.0%, 27.9%) instead gives review A 24.1 harms, B 11.8, C 10.8, i.e. a different winner, and that route is demonstrably biased by the data. Every other covariate I tested (age band, sex, practice, pharmacist) shows no heterogeneity (chi-squared p from 0.32 to 1.0), so the stratifier is separated by the data and no second defensible answer survives.

## Evidence (all recomputed from target/)
| Item | Golden | Recomputed | Source |
|---|---|---|---|
| In scope A / B / C | 612 / 1,239 / 1,636 | 612 / 1,239 / 1,636 | registrations (active on 31 Dec, outside Clun Valley, age = 2026 minus birth year), prescribing_issues (1 Jul to 31 Dec), problem list exclusions, palliative register |
| Specialist-started share | 86% / 6% / 44% | 525/612 = 85.8%; 76/1239 = 6.1%; 718/1636 = 43.9% | courses + letters feed (+ lookup) |
| Pilot six-month rows, practice | 63/136, 68/276, 65/192 | same | outcome log (follow-up rows) + same flag |
| Pilot six-month rows, specialist | 1/24, 1/24, 2/48 | same | same |
| Patients off | 60 / 290 / 340 | 62.2 / 289.7 / 340.7 | spec 3.3 |
| Harms a year | 6 / 12 / 8 | 6.15 / 11.99 / 8.10 | table 1 by age on 31 Dec |
| Gap | 4 | 3.89, rounds to 4 (12 minus 8 on whole numbers) | |
| Letters per 1,000 (5 networks, 2 halves) | as golden | all 10 cells identical | workflow + feed + list sizes (1 Jan, 1 Jul) |
| Consultations per 1,000 (5 networks, 4 quarters) | as golden | all 20 cells identical | hub (UTC to London), clinical system, group register, registrations, list sizes |

Robustness of the specialist flag: the lag from letter to first issue falls only in 1 to 30 days; nothing between 31 and 4,000 days, so any window from 30 to 365 days gives the same 525 / 76 / 718. Start-only letters, encounter date instead of letter date, and unresolved-pseudonym letters give identical flags (any-course instead of earliest-course moves B by 3 patients, 11.97 vs 11.99). Using a reviewed-patients denominator (including the 10 who died) gives 60.7 / 286.6 / 337.5 off and 6.0 / 11.9 / 8.0 harms: same rounded answers. A pooled specialist rate (4/96 = 4.2%, identical to each review's own) changes nothing.

Competing answers tested:
- Pooled pilot rates: A wins (24 harms). Not defensible once the 1/24 vs 63/136 split is seen.
- Flag "any letter naming the class, any date" (ignores that Continue/Review/Stop letters do not show who started the medicine): A 15.8, B 12.0, C 9.2, so A wins. This operationalisation does not separate the pilot outcomes as sharply (flagged rate 23% vs 47% in A) and is not a reading of "started by"; the clean flag separates 4% vs 25 to 46%. Advisory fork, resolved by the data.

Letters (ask 7) sensitivity: dropping the 152 reissued MMH twins of 7 April moves cells by up to 0.8 (spec 4.3 "a letter counts once" forces the dedupe); the GP Connect receipt match is invariant to window 14 to 28 days (21 as filed), 60 days moves one cell by 0.1, 7 days breaks it; document-type filter, twin key subsets and tie-order change nothing. Receipts occur only 07:00 to 18:59, so no half-boundary timezone issue. Closed practices carry no receipts or list sizes.
Consultations (ask 8) sensitivity: without the hub/clinical-system de-duplication cells inflate by up to 2.8 (spec 4.1 "one patient consultation" forces it); matching on any hub outcome is identical; Friday hub appointments are recorded the following Monday (119 cases), so calendar-next-day instead of next working day shifts a cell by 0.2; dropping group sessions shifts 0.5. Residual advisory fork: 151 same-patient same-day repeat contacts in the clinical system (distinct consultation ids and times) are counted as separate consultations in the golden; collapsing them to one per patient per day lowers every cell by 0.1 to 0.3. The distinct ids, times and consultation types make row counting the natural reading.

Gates: A pass (all reproduced, blocks agree). B pass (every fact in a shipped file; the specialist split and dedupe rules are discoverable from the letters feed, courses file and workflow data, not external). C pass with the advisory forks above; the main margin (B 12.0 vs C 8.1) is not near any estimation line under the variants tested. D pass. E pass (single committed call plus bounded asks with unit and rounding stated).

## Files/Hygiene: PASS
18 files; formats csv, parquet, xlsx, pdf (four); one file of 176,956 rows (letters feed); distractors available (pilot close-out pooled rates, falls admissions csv, ePACT2 xlsx). Dates consistent with a 6 January 2027 snapshot; no authoring or benchmark language found in the three PDFs. Mixed date formats (MMH dd/mm/yyyy, WTH ISO), differing reference schemes and reissued letters read as real-system mess. Nothing exclusion-level.

## Stump power
Strong. The pilot report is correct and its no-heterogeneity statement (practice, age, sex) is true, so a strong analyst trusting the pooled rates files A with about 245 off and 24 harms; the winner only changes after the starter split is found in the 30 MB letters feed and the pilot is re-weighted to the 2027 mix. The ask layer adds long ETL chains (reissued letters, GP Connect receipt matching, hub vs clinical double counting) that are laborious to land cell by cell.

## Stumping type
`mechanism: decomposition_attribution (effect modification and transport of a correctly reported pilot rate to a different population mix)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported pilot numbers are correct; the difficulty is reweighting by a covariate the report does not show. On perfectly clean data the task still stumps.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: programme evaluation in medicines optimisation, transporting trial (pilot) effectiveness to the target population and multiplying by attributable harm rates; swapping nouns breaks it. Layer 1: layout and date-format changes between trusts, hospital-number lookup, reissued letters, GP Connect references, UTC hub times, practice merger codes. Layer 2: heterogeneous response by who started the medicine plus covariate shift between pilot and programme population. Easy route: pooled close-out off rates, which gives review A (about 24 harms) and not B.

## Fix
none. Optional, only if the author chooses to reopen: one clause in programme specification 4.1 stating that each consultation record is one patient consultation (closes the same-day repeat fork); would require a rerun, so not recommended.

# task255 determinism check (architecture 3)

Two isolated judge passes, each a Sonnet thread at medium effort that saw only a fresh unzip of target.zip, the prompt and the judge's system prompt, and opened the graded blocks only after its own derivation was on disk.

| Round | Pack | Verdict | Disposition | Action |
|---|---|---|---|---|
| 1 | eb685de6 | NOT_DETERMINISTIC on supplementary ask 4 only (order kept; main call and asks 1 to 3 forced; G PASS; H PASS) | SEND_BACK as labelled, an ask-layer repair by the gate table | programme 3.3 counts each person once however the register numbers them, the link shipped in a register person table; ask 3 moved to per-quarter entitlements with later cancellations; the cancellations dated before the programme's adoption; the regional series given a seasonal shape; the documents headed as the region's English working versions |
| 2 | ccc93a03 | DETERMINISTIC (order kept; F moderate to good; G PASS; H PASS) | APPROVE | none |

The round-1 leak reader's question 6 (rule application with a reconstruction step) against the judge's Gate H (analytical) is resolved by the measurement: one tablet a day files nine practices and a DDD-based dose two, the patient's own dose from the refills the six; the round-2 reader also read the deciding step as analytical.

---

# Determinism check, architecture 3 round 1 (2026-11-01): NOT_DETERMINISTIC on supplementary ask 4 only, SEND_BACK as labelled; order kept; main call and asks 1 to 3 forced; Gate G PASS; Gate H PASS (analytical)

Read against the gate table: a Gate C failure confined to a supplementary ask with the main call forced and G and H passing is an ask-layer repair that spends no architecture. The leak reader's question 6 (rule application with a reconstruction step) against the judge's Gate H (analytical) is resolved by the measurement: one tablet a day files nine practices and a DDD-implied dose another set, the patient's own dose from the refills the six; the decisive step is analytical. Isolated thread, Sonnet at medium effort, on target.zip eb685de6.

# Verdict, task255 round 3

**Order kept:** yes. derivation.md was written to disk first (it holds my own persistence, entitlement and continuing-user figures); graded_blocks.md was opened only afterwards.

- **Verdict:** NOT_DETERMINISTIC (supplementary ask 4 only; the main call, asks 1 to 3 and the PDF are forced).
- **Disposition:** SEND_BACK. Closing the fork changes what solvers see (a filed person-key rule or crosswalk for the 35 replaced pseudonyms), so prior runs are invalidated and a rerun is required. The main call, persistence figures, and entitlement figures need no change.
- **Failure type / gates:** competing_defensible_answer (sub-label: unfiled identity link). Fails Gate C and Gate B/E for supplementary ask 4 ("each practice's continuing statin users of 2026 as a count"). Gates A, D pass. Gate A: every golden figure reproduced (see Evidence), but ask 4 reproduces only under the unfiled link.

## Why
Programme 3.3 counts "persons ... each person counted once" and the only person key in the data is `personal_number_pseudonym`. Thirty-five persons carry two pseudonyms (the first ends, the second begins between 2026-04-16 and 2026-07-29, same sex and birth date, same product line, same practice, a 48 to 115 day gap). No shipped file (no dictionary, note, programme clause, README) says personal numbers were replaced in 2026, nor which fields identify the same person. A literal reader who counts a person as one pseudonym files 2116 continuing users (132, 127, 65, 119, 150, 116, 124, 247, 77, 120, 214, 107, 148, 82, 175, 113 by practice, in register order); the golden files 2151 (135, 129, 67, 121, 152, 119, 127, 249, 79, 121, 215, 110, 151, 84, 176, 116). All 16 practice counts differ, by 1 to 3. The matching key is also not forced by the text: matching on sex plus birth date alone yields 1,849 candidate rows (825 coincidental pairs), so the correct link needs same product line, same practice and non-overlap, a rule the files never state.

## Evidence (recomputed from the bundle)
| Item | Source | Reproduced |
|---|---|---|
| Dates: dd-mm-yyyy for Jan to Jun 2024 rows, ISO afterwards | statin_dispensings csv | yes, unambiguous |
| New users 1,485 (first statin 2025-07-01..12-31, none in 365 days before; nearest prior gap 42 to 225 days, nothing near 365); none hospital-first | dispensings | yes |
| Daily dose is not filed; patient-specific 0.5, 1 or 2 tablets/day (not fixed by strength). Inferred from refill cadence (median, mean, first-interval, first-365-day variants agree for every patient, none in an ambiguous zone) | dispensings, products | yes |
| 287 single-dispensing new users hold one pack of 98 to 100 tablets, non-persistent at any dose | dispensings | yes |
| Persistence per practice, whole per cent: 68, 48, 66, 53, 48, 73, 67, 48, 76, 68, 54, 71, 53, 75, 71, 65 (041207..041358; counts 70/103, 40/84, 37/56, 30/57, 51/107, 75/103, 69/103, 55/115, 61/80, 65/96, 45/83, 59/83, 62/117, 65/87, 72/101, 72/110) | derived | matches golden exactly; stable under window 364/365/366, tolerance 29/30/31, ">=30", no carry-over |
| Join set (below 60): 041219, 041236, 041248, 041275, 041307, 041322; nearest from above 041358 at 65.5 | derived | matches golden |
| Pharmacy rates (annex is not shipped) recovered from the statements: amount over conversations held or not yet cancelled on the statement date gives one integer rate per pharmacy across all four quarters: A102 213, A107 196, A114 238, A121 187, A126 249, A133 222, A139 204, A145 261. The held-final-status reading gives a drifting non-integer rate, so the as-of reading is the only consistent one | statements pdf, conversations xlsx | yes |
| Entitlement 2026 = rate x conversations with status afholdt (final, cancellations dated to 2027-02-08 included): 63,474; 43,708; 41,174; 26,928; 29,133; 36,408; 28,152; 49,590 | derived | matches golden |
| Continuing users with the 35-pair link: total 2151, per practice equals golden exactly; without the link 2116 | derived | reproduces only with the unfiled link |

Competing answers: (a) persistence under 1 tablet/day gives 9 joiners (adds 041224, 041251, 041282, 041334, flips 041275 in at 55.7 and 041307 out at 61.4 etc.); under a DDD-implied dose it gives yet another set. Both are cleanly ruled out by the filed words "the daily dose they take" plus the refill evidence, so they are the stump's wrong routes, not forks. (b) Ask 4 unlinked 2116 is the surviving fork described above. (c) "Entitled" read as the sum of statements paid is ruled out by agreement 2.1 (a cancelled conversation is not paid); the sum of statements exceeds entitlement only through later cancellations. Wording of ask 3 ("entitled to for 2026") is read as total, not balance owed; I regard this as forced.

## Files/Hygiene
PASS, with notes. 12 files; formats csv (3), xlsx (5), pdf (4 incl. none-decisive national report), so three formats; one 61,788-row CSV (3.3 MB). Distractors present and not file-named for their role: national_persistence_report_2025.pdf (180-day definition, wrong definition and wrong cohort), regional_statin_use_ddd_2025.xlsx, patient_survey_general_practice_2026.xlsx, atc_ddd_2026.xlsx. Layer 1 mess is realistic (mixed date formats, hospital prescribers, cancelled-after-statement, absent rate annex). Temporal: the dispensing extract carries cancellations dated up to 2027-02-08, later than the programme adoption date 26 Jan 2027; minor, non-decisive, a later extract of the same log is plausible. No authoring or benchmark disclosure seen. Nothing exclusion-level.

## Stump power (Gate F)
Moderate. The trap that does the work is that no file gives the daily dose: a solver that times each dispensing at one tablet a day (or at the DDD) reads 0.5 and 2 tablets/day patients wrongly and files a different join set (9 practices under 1 tablet/day, against 6). The programme sentence "at the daily dose they take" and the carry-over rule point toward the right method, so a strong model is plausibly able to infer dose from refills; the pharmacy-rate recovery (annex absent) and the 35 replaced pseudonyms add ask-level difficulty, though the latter is the indeterminate part. Lever if easier than wanted: none needed for determinism.

## Stumping type (Gate G)
`mechanism: etl_conformance / exposure estimation (method)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Reported numbers are not overturned (the national report 64 per cent and DDD index are unused distractors with other definitions); the difficulty is estimating latent dose and exposure from refill cadence on clean-enough data, which survives the clean-data test.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: pharmacoepidemiology (supply-based persistence from dispensing registers, cohort of new users); swap test fails to read the same with other nouns. Layer 1: mixed date formats, product join, hospital prescribers, quarter statements against later cancellations. Layer 2: estimating each patient's exposure (dose from their own refills, carry-over) before applying the 60 per cent line. Easy route: one tablet/day (or DDD), which a strong analyst who cleaned the data and read every rule would still file, giving 9 joiners (or another set) instead of 6. Mild caution: the filed sentence "at the daily dose they take" names the quantity but not how to get it; I class this as analysis (estimating an unobserved exposure), not semantics.

## Fix
input_files (and a matching one-line filed definition): state in a shipped file that personal numbers of some persons were replaced during 2026 and give the key that identifies one person (a crosswalk of the 35 pseudonym pairs, or a programme 3.3 sentence naming the identifying fields: sex, birth date, product line, practice, non-overlapping dispensing spans), and close it in the fork table; alternatively drop ask 4 or restate it per pseudonym. Persistence, join set, entitlement figures and the main call stay frozen.


---

# Determinism check, architecture 3 round 2 (2026-11-01): DETERMINISTIC, APPROVE; order kept; Gate F moderate to good; Gate G PASS; Gate H PASS

The re-judge after round 1's ask-4 repair, on target.zip ccc93a03. Isolated thread, Sonnet at medium effort.

# Verdict, task255 r4

- **Verdict:** DETERMINISTIC (no SOLUTION_WRONG; every graded figure reproduced exactly).
- **Disposition:** APPROVE. No repair needed; no rerun.
- **Order kept:** yes. derivation.md was written to disk before graded_blocks.md was opened.

## Why
The main call (send 041219, 041236, 041248, 041275, 041307, 041322) is forced by statin_followup_programme_2027.pdf 2.1 and 3.1-3.2 read literally on the dispensing file. The nearest practice to the line is 54 on the low side and 65 on the high side, so no margin is thin. Every unfiled convention I could vary gives identical whole-per-cent values: grace 29/30/31, window 364/365/366, carry-forward on/off, dose as snapped class vs continuous median vs first interval vs in-window intervals only. The one open term, the patient's daily dose (3.2), is not filed. It is recoverable from each patient's own refills, which cluster cleanly at 0.5, 1 and 2 tablets a day, and the 287 single-dispensing patients cannot reach 335 days of cover at any dose. All four supplementary blocks match my values.

## Evidence (recomputed, all reproduced)
| Figure | Source and field | Mine | Golden |
|---|---|---|---|
| New users | dispensings (dd-mm-yyyy to Jun 2024, ISO after), 365-day lookback, first dispensing in H2 2025 | 1,485 | 1,485 |
| Persistence % by practice (16) | prescriber_id; refill-derived dose | 68/48/66/53/48/73/67/48/76/68/54/71/53/75/71/65 | identical, including numerators (70/103, 40/84, 37/56, 30/57, 51/107, 75/103, 69/103, 55/115, 61/80, 65/96, 45/83, 59/83, 62/117, 65/87, 72/101, 72/110) |
| Below 60 | | 6 practices | same 6 |
| Pilot rates | pilot_statements_2026.pdf amount / conversations not cancelled by the statement date | 213, 196, 238, 187, 249, 222, 204, 261, an exact integer and the same in all four quarters for every pharmacy | same |
| Entitlement, 32 cells | rate x conversations with status afholdt, by conversation_date quarter | e.g. A102 14,271/16,401/17,253/15,123; A145 10,440/10,179/16,704/10,440 | identical |
| Continuing users (16) | 4 quarters of 2026, ids merged through cpr_persons previous number, last-2026 prescriber | 135/129/67/121/152/119/127/249/79/121/215/110/151/84/176/116 (2,151) | identical |

- **Rate fork closed by the data.** The statements carry quarter totals only. The held-only or all-rows readings give non-integer, unstable rates. Only the reading "not cancelled as at the statement date" gives an integer rate that is constant across the four quarters. That makes the rate recoverable and the entitlement unique. Late cancellations (64 rows cancelled after the quarter end) are correctly not paid under agreement 2.1.
- **Wrong routes, each of which changes the answer.**
  - 1 tablet a day for everyone flags 041219, 041224, 041236, 041248, 041251, 041275, 041282, 041322 and 041334, and misses 041307 (61 per cent).
  - DDD-based dose (atc_ddd_2026.xlsx) flags only 041236 and 041263.
  - Not merging ids gives 2,116 continuing users.
  - Using the statements as the entitlement (or any reading that counts late-cancelled rows) gives wrong cells.
- **Semantic forks.** None left open that changes a graded figure. Hospital attribution (SGH-*) never arises: no cohort first dispensing is hospital-prescribed, and no continuing user's last 2026 dispensing is hospital-prescribed.

## Gate-by-gate
- Gate A pass. Gate B pass: the rate annex is not shipped, but the statements and the log fix the rate, and the dose is recovered from the dispensing file. Gate C pass. Gate D pass. Gate E pass: the prompt's terms (programme line, persistence, continuing users, entitled) are all defined in the shipped programme and agreement texts.
- Residual notes, not findings: "daily dose they take" and "the agreed rate" are never stated as numbers, so a solver must infer both. The data separates the candidates cleanly, so this is an analysis step rather than a fork.

## Files/Hygiene: PASS
13 files, formats csv, xlsx and pdf (3 formats). Rows: dispensings 61,788 (above the 25,000 floor), persons 8,538, conversations 1,560.
- The relevant files are practice_register, statin_products, cpr_persons, dispensings, conversations, programme pdf, agreement pdf and statements pdf.
- Distractors used by no solution: national_persistence_report_2025.pdf (180-day rule, 2023 cohort), regional_statin_use_ddd_2025.xlsx, patient_survey_general_practice_2026.xlsx, atc_ddd_2026.xlsx.
- Layer-1 mess is authentic: date-format switch, pack sizes 30/98/100, brand variants, pseudonym changes, cancellations after the statement date.
- Temporal coherence holds: the programme was adopted 26 Jan 2027 and the data end 31 Dec 2026.
- No authoring or benchmark language found. No exclusion-level finding.
- Minor realism note only: the repeated "English working version kept by the medicines unit" line across the PDFs reads slightly templated; it is non-decisive.

## Stump power (Gate F)
Moderate to good. The decisive trap is the unfiled daily dose. The naive 1-tablet-a-day or DDD routes give a wrong set of practices (see above), and the 3.2 text points at it without giving the number. The other lines are a pharmacy rate that must be backed out of the statements and ids that must be merged, and these add ask-level difficulty. Risk: a strong analyst who checks refill intervals finds the 0.5/1/2 clusters quickly, and 3.2 does tell the solver to use the patient's dose, so the main call may be reached by careful runs. The portal measures this.

## Stumping type (Gate G)
`mechanism: etl_conformance / method_or_model_selection (dose-adjusted persistence estimand)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
No reported number is wrong or misleading, and on perfectly clean data the persistence estimand still requires the refill-derived dose. Not a banned scaffold.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`
- **Domain.** Persistence on treatment from dispensing data is core pharmacoepidemiology (the swap test fails if you change the nouns).
- **Layer 1.** Mixed date formats, pack sizes, product variants, pseudonym changes, cancellations after the statement date.
- **Layer 2.** Measuring persistence as supply coverage at each patient's own estimated daily dose, with carry-forward.
- **Easy route.** A strong analyst who read every rule and cleaned the data could still take one tablet a day, or the DDD, and flag nine practices that miss 041307 (naive) or only two (DDD).
- **Why not rule application.** The rule is stated, but its decisive input is estimated from the data rather than executed from stated numbers.

## Fix
none.


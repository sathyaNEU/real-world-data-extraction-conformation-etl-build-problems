# task452 determinism check (architecture 3)

Two isolated judge passes, each a Sonnet thread at medium effort that saw only a fresh unzip of target.zip, the prompt and the judge's system prompt, and opened the graded blocks only after its own derivation was on disk.

| Round | Pack (sha256) | Verdict | Disposition | Action |
|---|---|---|---|---|
| 1 | 3c2e3b88 | DETERMINISTIC (order kept; F moderate; G PASS; H PASS) | APPROVE as labelled; two forks settled only by the thread's reading treated as a FIX_NOW | licence definition 1.8 files hours as summed elapsed time; the supplier certificates built from the same fuel the as-fired composites describe, so every source rounds alike (68, 83, 151, 66 over); the quarterly hours made the reported basis |
| 2 | 3b551682 | NOT_DETERMINISTIC on supplementary 4 only (order kept; main call and hours reproduced; G PASS; H PASS) | FIX_NOW | the 21 per cent ambient oxygen basis filed beside the reference conditions in licence 1.6, the wording the judge itself asked for; NOx holds at 931.90 and 605.00 t under both overlap choices; the quarry file declared a distractor with its reason in metadata.json; figures.json and submission.md byte-identical, no graded figure moved (target.zip d46d00ed) |

---

# Determinism check, round 1 (2026-11-01): DETERMINISTIC, APPROVE as labelled; order kept; Gate F moderate; Gate G PASS (method_or_model_selection); Gate H PASS

Two advisory forks were settled by the thread only by the literal reading or the better-supported source (the duration reading of hours; the lab composites against the supplier certificates for the kg figures), so under 'our judge is the floor' they are treated as a FIX_NOW and closed before the one re-judge. Isolated thread, Sonnet at medium effort, on target.zip sha256 3c2e3b88.

# Determinism verdict, task 452 (round 1)

ORDER: kept. derivation.md was written to disk before graded_blocks.md was opened. Cross-batch check: no earlier verdicts or delivered packages were supplied in the allowed folder, so not run (no hit reported).

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. No repair is needed and no rerun is required. Two advisory notes under Evidence (hours convention, quarterly vs annual rounding) are not blocking.
- **Why:** The call is forced by the shipped files. Condition 5.6 counts every firing hour in compound and in direct operation. All six stack tests (stack_tests_Hg_2024-2026.pdf) were run with the raw mill in operation, so no file measures direct-operation mercury. The only closed route is the annual mercury balance, ledger tonnes times QC_lab_composites Hg, less clinker and, for kiln 1, bled filter dust. I got 67.93 + 83.19 = 151.12 kg, which is 68 / 83 / 151 and 66 kg over, so carbon injection is needed. Every variant I tried stays over the load (lowest 62 kg over). The easy route (tests x firing hours, about 70.5 kg, "14 kg under") is the wrong answer, and its coverage gap is stated in the files. Every committed answer reproduced. Gates A to E pass.

## Evidence (recomputed from the bundle; all reproduced)
| Item | Mine | Golden | Source |
|---|---|---|---|
| Hg kiln 1 | 67.93 kg (in 80.82, out 12.90) | 68 | production_ledger H1/H2 x QC_lab_composites (LS, SH, SA, FE, SL, CO, RF, CK1, FD1) |
| Hg kiln 2 | 83.19 kg (in 84.10, clinker 0.90) | 83 | same, PFA 43.07 kg is the largest term |
| Works / margin | 151.12 kg, 66 kg over | 151 / 66 | |
| On feed K1 quarters | 1542.01, 2106.70, 2115.61, 2175.75 | 1,542 / 2,107 / 2,116 / 2,176 | DCS journal, seconds, DST-aware, trip stops feed |
| On feed K2 quarters | 1636.99, 2168.12, 2125.61, 2105.82 | 1,637 / 2,168 / 2,126 / 2,106 | |
| Direct K1 quarters | 287.95, 345.22, 378.97, 379.74 | 288 / 345 / 379 / 380 | on feed and raw mill stopped |
| Direct K2 quarters | 352.21, 451.85, 469.36, 457.72 | 352 / 452 / 469 / 458 | |
| NOx K1 / K2 | 931.90 / 605.00 t | 932 / 605 | historian REF10 x (21-O2)/11 x dry flow x 0.5 h, 9-day hole filled from CEMS |

- **Cross-check on the balance.** Compound hours x tested rate leave a direct-operation residual of about 42 kg (kiln 1) and 54 kg (kiln 2). That is about 30 g/h per direct hour in both kilns, so the two kilns are consistent with each other.
- **Competing routes tried against the main call.**
  - Tests x all firing hours: about 70.5 kg, which would say "under by 14 kg". It is not licensed, because cl. 5.6 and 1.4/1.5 require direct operation and every test shows "Raw mill: in operation".
  - Tests for compound hours plus the 50 ug/Nm3 ELV for direct hours: about 95 to 100 kg. The ELV is not an emission estimate, and the call direction is the same as the golden.
  - Supplier-certificate Hg for coal and SRF (fuel_receipts) instead of the lab: kiln 1 about 65, kiln 2 about 82, works about 147, 62 over. The call is unchanged. The lab composite is the as-fired basis that matches the ledger. It also contradicts the cargo-4 certificate (47 vs lab about 90 ug/kg). Using the certificates would need an unpinned rule for which cargo is burned when, so they are a weaker, not an equal, reading. Advisory: no filed hierarchy names the lab as the source of truth, so a grader should hold the call and not penalise the kg figures too hard.
  - Ledger dust 9,924 t vs weighbridge after removing 2 duplicated tickets and 3 VOIDs (9,930 t): under 0.01 kg. Raw-meal stock change (no opening stock): under 0.5 kg. Annual-mean Hg instead of monthly: 68 / 83, same.
- **Hours advisory (asks only, no effect on the call).** "Hours" is read as summed durations. A clock-hour grid (cond. 6.4 "every hour") would give different whole numbers for kiln 1 / kiln 2 direct hours:
  - summed durations: 1,392 / 1,731 (golden)
  - majority-of-hour: 1,396 / 1,729
  - any minute: 1,509 / 1,863
  - whole hours only: 1,223 / 1,551
  The condition's own words ("hours in which a kiln is producing clinker and its raw mill is stopped") and the prompt's "whole hours" make the duration sum the literal reading. The other grids are unlicensed rounding schemes, so I do not fail the gate on this.
- **Other forks closed by the files.**
  - On feed: the journal never logs FEED OFF at a burner TRIP. Counting the tag as ON through trips adds roughly 190 h per kiln. The historian feed rate is 0 over those periods and the later FEED ON line shows a restart, so feed stopped at the trip. Five or fewer half-hours disagree between historian and journal.
  - DST and the repeated hour: the 25 Oct RM1 STOP at 01:05:42 and START at 01:50:58 are placed by file order around the clock-change line, a 1 h 45 min stop. The journal order and the historian agree.
  - The 9-day historian hole (11 May 06:00 to 20 May 05:30 UTC) is covered by the CEMS file. Its timestamp is local IST and labels the interval end (UTC start = local - 1.5 h). Flow matches the historian exactly on 384 overlapping rows.
  - NOx conversion: naive REF10 x dry flow gives 825 / 549 t. Leaving the gap unfilled gives 903 / 587 t. Feed-hours-only gives 930 / 604 t, a 2 t / 1 t fork that cl. 6.4 "every hour of the year" closes toward 932 / 605.
- **Rounding.** Kiln 1 on-feed quarters sum to 7,941 against an annual 7,940.07. This is a presentation point only. The workbook should show quarters only, or say that rounded quarters need not sum.

- **Files/Hygiene:** PASS. 11 files, 4 formats (csv x4, xlsx x3, pdf x2, txt journal x1, plus the semicolon CSV logger). One file has 34,176 rows (historian). Distractors are present and unused: quarry_extraction_2026.csv (wet haul tonnes), weighbridge_byproducts_2026.csv (only dust tickets matter, and only as a cross-check), the fuel-receipt certificates, the cement-mill events and the 2024 and 2025 test reports.
  - Files read as operational artefacts: mixed date formats (DD/MM/YYYY, ISO), semicolon CSV, duplicate and VOID tickets, H1/H2 ledger sheets with different layouts, a journal export with a repeated clock hour, UTC vs local.
  - No README, authoring or benchmark language. Dates are coherent (journal exported 4 Jan 2027, licence amended 30 Jun 2026, last cargo 9 Dec 2026).
  - Minor: the stack-test reports share identical boilerplate ("Signed for the laboratory: technical manager"). That is cosmetic, in-house only and not exclusion-level. Licence/source/date records live outside the bundle (metadata.json is not in my universe) and could not be checked. Real-data contamination: none apparent, the data is fictional (Kilcarrow Works).
- **Stump power (Gate F):** Moderate. The trap is applying the tested compound-operation rate to every firing hour (about 70 kg, a "keeps under" answer). It is genuine because the test tables are correct and complete for the mode they cover, and the closed route needs about 60 ledger x lab cells across two sheet layouts. Easy-signal risk: cl. 5.6 and the 1.4/1.5 definitions state the two modes, and QC_lab_composites ships Hg for clinker and for filter dust, so a strong model may reach the balance. Even a model that only flags "direct mode unmeasured" and uses a proxy may get the direction ("injection needed") but not the 151 / 66 figures. The asks (DST-aware journal rebuild, O2 restatement, CEMS gap fill) carry additional difficulty. The portal measures the rest. No lever needed.
- **Stumping type (Gate G):** mechanism: method_or_model_selection; stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no. The tests are accurate for compound operation and nothing is "misleading". The difficulty is choosing an estimand and method that cover the unmeasured mode, and on clean data the balance would still be needed. No shipped artifact ranks the decision wrongly. The nearest thing is the "compliant" test result against the 50 ug/Nm3 ELV, which is a different quantity (concentration vs annual mass). Gate G passes.
- **Three rules (Gate H):** domain: pass, layers: pass, decisive_step: analytical.
  - Domain: an industrial-emissions compliance load estimate, where the quantity that decides is an annual stack mercury mass closed by a material balance. This is what the field does, and the swap test fails to hold under "hospital" or "visits".
  - Layer 1: DST and a repeated hour, UTC vs local, a 9-day historian gap filled from a CEMS file at actual O2 and interval-end labels, H1/H2 layouts, duplicate and VOID tickets.
  - Layer 2: a mercury balance by line with the direct-operation release as the unmeasured remainder.
  - Easy route: a strong analyst who cleaned everything and read every rule correctly could still multiply the tested rate by 7,940 / 8,037 firing hours and file about 70 kg, "14 kg under, no injection". Reading cl. 5.6 correctly does not by itself produce the balance, so this is analysis and not rule application. It is not a planted decoy or a withheld rule. The coverage gap is stated in the files (cl. 5.6 modes; "Raw mill: in operation" in every test).
- **Fix:** none (APPROVE). Optional, in-house: show only quarterly on-feed hours in the workbook, or note that rounded quarters need not sum to the annual figure.


---

# Determinism check, round 2 (2026-11-01): NOT_DETERMINISTIC confined to supplementary 4 (NOx), FIX_NOW; order kept; main call forced; Gate G PASS; Gate H PASS

The re-judge after round 1's two forks were closed (hours as elapsed durations; certificates agreeing with the lab composites), both reproduced exactly. Its one finding (the unfiled ambient-oxygen constant behind the NOx restatement) is closed by the wording the judge itself asked for (21 per cent filed beside the reference conditions), which moves no graded figure. Isolated thread, Sonnet at medium effort, on target.zip sha256 3b551682.

# Verdict, task 452 r2 (Kilcarrow Works mercury load, kiln hours, NOx)

Order kept: yes. derivation.md was written to disk, with my own figures for every ask, before graded_blocks.md was opened. Cross-batch fingerprinting against delivered tasks was not possible (only this folder is readable) and is not reported.

- **Verdict:** NOT_DETERMINISTIC, confined to one supplementary answer (NOx, kiln_emissions_2026.xlsx item 4). The main call, the per-kiln mercury figures, and the feed and direct hours are all forced and reproduce. Gate A passes (blocks are correct and consistent).
- **Disposition:** FIX_NOW. File the oxygen-correction convention (ambient O2 constant of 21 %) in the licence's reference-conditions clause or the historian's tag note. This pins what the correct tonnage is, leaves the analytic surface unchanged, and needs no rerun of the main call. If the pin cannot be filed, round NOx to tens of tonnes or pin the constant in the ask.
- **Why:** NOx mass needs the historian's 10 % O2 concentration restated to measured oxygen, and no shipped file gives the ambient-oxygen constant. The historian itself shows 20.90 for cold air, so 20.9 is a licensed reading, while the golden (932 / 605) only reproduces with 21.0. At 20.9 I get K1 932.85 t (933) and K2 605.503 t (606, or 605 if the CEMS file is preferred in the overlap, 605.496), a rounding knife-edge. At 21.0: 931.90 / 605.00. Gate C/E on supplementary 4; taxonomy label underspecified_objective (convention unpinned, with a margin_or_boundary_fragility element for K2).

## Evidence (all recomputed from target/)
| Figure | My value | Golden | Source |
|---|---|---|---|
| Hg K1 | 67.93 kg (ledger dust) / 67.84 (weighbridge dust) = 68 | 68 | production_ledger x QC composites, less clinker and S7 dust |
| Hg K2 | 83.19 kg = 83 (dust recycled, site_register) | 83 | same |
| Works / margin | 151.1 kg, over by 66 | 151 / 66 | limit 85 (cond 5.6) |
| Hours on feed K1 | 1542.01 / 2106.70 / 2115.61 / 2175.76 | 1542 / 2107 / 2116 / 2176 | DCS journal, feed ON/OFF plus burner TRIP, local quarters |
| Hours on feed K2 | 1636.99 / 2168.12 / 2125.61 / 2105.82 | 1637 / 2168 / 2126 / 2106 | same |
| Direct K1 | 287.95 / 345.22 / 378.97 / 379.74 | 288 / 345 / 379 / 380 | feed on and raw mill stopped |
| Direct K2 | 352.21 / 451.86 / 469.36 / 457.73 | 352 / 452 / 469 / 458 | same |
| NOx K1, K2 | 932.85, 605.50 (20.9) or 931.90, 605.00 (21.0) | 932, 605 | historian plus CEMS May file for the 9 day hole |

All Hg and hours figures reproduced exactly. The nearest rounding boundary is 0.11 h (K1 Q3 feed 2115.61, K2 Q3 feed 2125.61), and journal times are second-accurate (historian May-30 and Jun-20 partial-interval feed values confirm them), so those are safe.

Competing answers tested:
- Stack-test rate x hours on feed: 31.7 + 38.8 = 70.5 kg (71.2 with three-year means), "under by 14 kg, no injection". It is refuted by the shipped files: cond 5.6 counts direct operation, 1.5 defines it, all six test reports show the raw mill "in operation", and the balance implies about 30 g/h in direct operation on both kilns (K1 30.0, K2 30.5) against 4 to 5 g/h in compound. No defensible alternative survives for the main call.
- Balance variants: the margin stays over by 64 to 67 kg and K1 stays 68 and K2 83 under dust from ledger or weighbridge, lab or supplier-certificate coal and SRF Hg (about -0.3 kg), and the unknown opening raw-meal stock (about 0.1 kg). Omitting the clinker sink would give 153 kg, but the clinker composites are shipped, so that is a solver error, not a fork.
- quarry_extraction_2026.csv (1.69 Mt limestone, 0.24 Mt shale hauled) does not reconcile to ledger consumption (2.15 Mt, 0.37 Mt) and is not per kiln. If used it lowers the total by about 26 kg (to about 125) and the call still stands. It is a declared-distractor candidate whose conflict with the ledger is not explained anywhere; the ledger is the only per-kiln consumption source, so the figures are still forced.
- Hours traps are closed by shipped text: cond 1.8 (elapsed, not clock hours), 1.7 (Irish local time), journal clock-change rows. The historian has a 9 day hole (11 May 05:30 to 20 May 06:00 UTC, 432 rows per line), so counting historian rows gives wrong hours (for example K1 Q2 feed 1891.5, direct Q1 293.5 versus 287.95). The journal fixes this.
- Small residual wording gap (not a fork): the prompt says "on feed", the licence defines hours of operation as "producing clinker". The data never separates them.

## Files/Hygiene
PASS. 11 files; formats csv (5), txt, pdf (2), xlsx (3); PI historian is 34,176 rows. Operational-looking artifacts with real irregularity (DST journal, two ledger layouts, historian hole, local-time CEMS with interval-end stamps). No authoring or benchmark disclosure found, no temporal contradictions (journal exported 4 Jan 2027, tests to Oct 2026). Distractors present: quarry_extraction, fuel_receipts supplier certificates, weighbridge (an alternative dust source), stack tests (lure). Not exclusion-level. Note the unexplained quarry versus ledger gap above.

## Stump power
Moderate to good. The decisive lure is the stack-test g/h x hours route (70.5 kg, under), which is attractive because the tests are the only measured Hg. A strong model that reads the "raw mill in operation" column and cond 5.6 will turn to the mass balance, and then the exact figures (68 / 83 / 66) fall to the S7 dust sink, the PFA inputs, the clinker sink and per-kiln allocation. The hours and NOx asks add independent traps (historian hole, clock changes, O2 restatement). Risk: the direction (over 85) survives a sloppy balance, so the main call may be solved while the graded numbers are missed; the licence sentence in 5.6 also nearly announces the trap. Lever if too easy: none required.

## Stumping type
mechanism: method_or_model_selection (annual mass-balance closure versus extrapolating a periodic measurement that never sampled direct operation), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no. The stack-test results are correct for compound operation and are not overturned as wrong; the difficulty is that they do not cover the estimand. On clean data the task would still stump. Passes Gate G.

## Three rules
domain: pass, layers: pass, decisive_step: analytical. Swap test fails to transplant (annual Hg emission inventory, mass balance versus periodic stack monitoring, compound versus direct raw-mill operation is the field's own estimation problem). Layer 1: DST journal, 9 day historian hole, two ledger layouts, interval-end local-time CEMS, 10 % O2 restated concentrations. Layer 2: closing the release by mass balance because tests cover only compound mode. Easy route: stack-test rate x hours = 70.5 kg, under by 14 kg, no injection; correct answer 151 kg, over by 66 kg.

## Fix
Fix location: input_files (pin) or prompt. File the ambient-oxygen constant (21 %) next to the reference conditions (cond 1.6) or in the ask; then K1 932 t and K2 605 t hold under either overlap choice (931.90 / 605.00 at 21.0). Optional: add one line explaining the quarry versus ledger difference (stockpile reclaim) or drop the quarry file from the apparent consumption evidence. No other change needed.


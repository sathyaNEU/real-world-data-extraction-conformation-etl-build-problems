# determinism-check report, task119, 2026-10-10 (pass 2)

**Run note.**
- **Licence:** `/build` stage 6.
- **No spawned thread:** the workflow exposes no `Agent` tool, so the judge ran inside the orchestrator under the same allow-list a spawned thread would have had.
- **What the judge saw:** a fresh copy of `target/` at `/tmp/determinism-check-task119-20261010T031031Z/target/`, `prompt.md`, the four graded blocks of `submission.md`, and `guidelines/determinism_judge_system_prompt.md` (v3), read in full.
- **Sequencing:** the judge's `verdict.md` (same scratch folder) was written before `metadata.json`, `DESIGN_NOTE.md`, `golden/`, the pass 1 report, `leak_check_report.md` or `pipeline.json` were opened.
- **Opened after the verdict:** `pipeline.json` was opened afterwards, while checking the leak-check record. Nothing in it is used here.
- **Never opened:** the generator and `solver_rounds/`.
- **Not run:** the cross-batch reference check, because other task folders are outside the allow-list. `/clone-check` owns that question.

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The terms of reference (`review_terms_of_reference_2027-28.docx`, WRHB/26/097) set the objective:
- **s.3:** the engagement is judged on deaths confirmed avoidable "because of problems in the reviewed trust's own care".
- **s.4:** a trust's decisions about the use of its own beds and staff are part of that care.
- **s.5:** placement rests on the latest four complete quarters, July 2025 to June 2026.

Recomputed from the shipped files:
- **Stennock:** all 27 of its long-wait deaths in that year happened while its unit held one or two beds assigned to its own planned surgical patients. Those beds were physically empty, because `left_recovery_at` in `rds_theatre_cases_2023-2026.parquet` falls after the waiting patient's decision.
- **Prideswick:** its 15 happened beside unassigned staffed beds.
- **Ristenholm, Brackenford, Prideswick:** every bed that went to someone else during their waits was a network bed bureau allocation. All 43 are in `interhospital_transfer_audit_202307_202606.csv`, with `bed_confirmed_at` equal to the stay start.

Stennock is forced at 27 against 15. The gap is 12, and no estimate is involved. Gates A to E pass, and there is no taxonomy failure.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Main call | Stennock | Stennock, 27 against Prideswick 15 | yes |
| docx 1: trust | Stennock (STN) | Stennock | yes |
| docx 2: deaths a year of review could confirm | 27 | 27 | yes |
| docx 3: runner-up | Prideswick (PRW), 15 | Prideswick, 15 | yes |
| docx 4: gap | 12 | 12 | yes |
| CC1: Lathingbury placement-year remit deaths, no level 3 beds | 56, none | 56; `acc_unit_register.csv` LAT-HDU care_level 2 | yes |
| CC2: Stennock deaths all after held-bed waits | 27 of 27 | 27 of 27. 1 or 2 held beds at each decision: SDU-referred type 03 stays from Stennock Treatment Centre (provider STN, no audit row), assigned 08:31 to 12:11 the same day, `left_recovery_at` after the decision. Long waits fall on weekdays only, 10:00 to 13:59 | yes |
| CC3: Prideswick deaths beside own empty staffed bed | 15 | 15 (free bed for 254 to 361 minutes of each wait; weekends and two May bank holidays) | yes |
| CC4: Stennock lead | 12 | 12 | yes |
| Steps 1-2: placement-year remit deaths | 213 | 213 = 193 admitted + 20 died before admission more than 4 h after the decision | yes, but only with the died-before-admission inclusion, which step 1 does not state |
| Step 4: Ristenholm own-care deaths | 2 | 2 (Saturday and Sunday free beds, 334 and 326 min) | yes |
| Step 5: admissions to own unit during waits | all other-trust, bureau | 43 of 43: RIS 35 type 03 from LAT/TAN/ELL/PEL theatre recovery, BRK 6 and PRW 2 type 02; every one in the audit | yes |
| BRK full through every wait | yes | min census 16 of 16 open in all 35 waits; all began 18:00 to 23:59 | yes |
| png 1: deaths in remit, STN PRW RIS LAT BRK ELL TAN PEL | 27, 21, 44, 56, 35, 13, 10, 7 | same | yes |
| png 2: confirmable part | 27, 15, 2, five at 0 | same | yes |
| png 3: order | STN, PRW, RIS, then five at 0 | same; the order inside the five-way tie is unpinned (the golden sorts them by deaths) | yes |
| png 4: gap marked | 12 | 12 | yes |
| png 5: title names Stennock | yes | golden title "Stennock: 27 deaths a year of review could confirm, 12 more than Prideswick" | yes |
| xlsx Brackenford | 351 / 104 / 5 | 351 / 104 / 5 | yes |
| xlsx Ellerdyke | 140 / 40 / 6 | 140 / 40 / 6 (level 3 until 2024-03-31) | yes |
| xlsx Lathingbury | 559 / 165 / 0 | 559 / 165 / 0 | yes |
| xlsx Pellowham | 75 / 22 / 3 | 75 / 22 / 3 (PEL-W3 winter beds, Dec 2023) | yes |
| xlsx Prideswick | 221 / 63 / 46 | 221 / 63 / 46 | yes |
| xlsx Ristenholm | 438 / 126 / 8 | 438 / 126 / 8 | yes |
| xlsx Stennock | 275 / 80 / 80 | 275 / 80 / 80 (60 held-bed, 20 own-given in the CCRS era) | yes |
| xlsx Tannerby | 104 / 29 / 0 | 104 / 29 / 0 | yes |
| xlsx totals | 2,163 / 629 / 148 | 2,163 / 629 / 148 | yes |

The workbook reproduces only with the full conformance applied. Each skipped device moves the totals by a known amount:

| Device skipped | Totals become |
|---|---|
| CCRS times left in UTC | 2,197 / 659 |
| CCRS transfers timed at placement | 2,191 / 650 |
| Local clock across the March changes | 20 more referrals, 17 of them deaths |
| No spell death for the 10 unresolved temporary keys | 619 deaths |
| Requested level instead of decided level | 2,179 / 645 |
| Raw-feed census | 183 confirmable |
| Current register in place of the dated register | 139 confirmable |
| Own-given placements not counted | 121 confirmable |

Convergences checked:
- The 274 pilot-ward duplicate pairs agree on remit membership both ways.
- No wait falls between 232 and 249 minutes.
- No long-wait death falls between day 25 and day 35.
- The placement year carries none of the CCRS conformance devices.

## Competing answers that survived
None. The nearest forks, with the shipped fact that closes each:

- **Bureau allocations read as the receiving trust's decision.** Ristenholm 37, Stennock 27, Prideswick 17, Brackenford 6, so the call flips to Ristenholm. This is the closest fork. Closed by:
  - the field guide (`bed_confirmed_at` is when "the network bed bureau allocated the bed at the receiving unit");
  - ACCN/23/41 s.3 ("agreed through the network's bed bureau");
  - ToR s.2 (transfers reviewed with the referring trust);
  - Maria Reynolds' "their unit's rule, not a network one".

  The only text pulling the other way is her opinion that Brackenford "could take more of its own patients if it held on to those beds".
- **Assigned-but-empty beds read as occupied.** Stennock 0, so the call flips to Prideswick at 15. Closed by ToR s.4 and the theatre join. This is the stump, not a licensed reading.
- **Most deaths waiting (Norman Scott).** Points to Lathingbury, 56. Closed by ToR s.3 and the register (no level 3 unit).
- **"Reviews confirm every long-wait death", generalised from the NRR log.** Points to Ristenholm, 44. Closed because all 34 NRR reviews had every long wait beside an empty staffed bed, so the corpus cannot separate the readings and ToR s.3 governs.
- **Died before admission excluded.** STN and PRW bars are unchanged, but RIS 41, LAT 46, BRK 33, ELL 11, TAN 8, PEL 6, and the workbook becomes 2,113 / 579. Closed by the remit's natural reading (patients who "die waiting"), but `submission.md` step 1 should say so (Finding 1).
- **Three-year average in place of the placement year.** 26.7 and 15.3 round to 27 and 15, but the gap would be 11. Closed by ToR s.5.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10 or more | 20 | yes |
| Distinct formats | 3 or more | 8 (csv, parquet, pdf, xlsx, sqlite, txt, eml, docx) | yes |
| Largest table or database | 25,000 rows, or a large database | apc parquet 88,202 rows; ambulance csv 70,072; `nrr_review_records.sqlite` 12.7 MB (48,755-row referrals table) | yes |
| Distractors declared | 2 or more in `metadata.json`, none labelled in a file name | 5 (level 2 returns, ambulance handovers, capacity report, NRR log, NRR database); names are in-fiction | yes |
| Distractors relevant and unused | same world, off the solution path | all five off the path, all about the same trusts, beds or reviews | yes |
| Distractors that answer a graded or decision quantity reproduce and are ruled out | arithmetic plus a shipped fact | Capacity report waits from receipt: 216 of 216 month-trust cells and the level 3 counts reproduce from the referral record. NRR log: 34 of 34 reviews reproduce from the database. Ruled out by ToR s.2 (wait from the decision to admit), s.3 and s.5 | yes |
| Deliverables | 1 to 3 | 3 (docx, xlsx, png) | yes |
| Format family | none required | Text, Data, Visual | n/a |
| Multi-dimensional asks | no stacked lookups | 8 by 3 grid with totals; 8 stacked bars with shading, order, gap and title; docx keyed to the call | yes |
| Golden deliverables present | every one named | 3 of 3. Every shared figure agrees with `submission.md` (27, 15, 12, 213, 44, 2,163 / 629 / 148, the per-year 25/28/27 and 14/17/15 in the memo, all recomputed) | yes |
| Units and rounding | stated for every ask | units in each ask (deaths, patients); "whole numbers throughout" closes the prompt | yes |
| Prompt shape and criteria | identifiable, 25 or more | `metadata.json` shape 07 (grid of cells), 36 criteria by the design note's arithmetic | yes |
| Realism | nothing reads as generated | Generator tells remain: 345 admitted waits at exactly 225 minutes and an empty 232-249 band; constant `beds_open`; RIS and STN at 100 per cent on every one of 1,126 mornings; board-paper PDF dated before the meeting its text records; CCRS levels file name says 202604. The goldens read as a board paper, workbook and chart; the workbook totals are typed values | warn |

## Gate G reconciliation
| | Judge | Design note (lines 16, 134, 361) |
|---|---|---|
| mechanism | decomposition_attribution | decomposition_attribution |
| stumping_family | analytical_non_defect | analytical_non_defect |
| surface_read_dependency | no | no |
| sole_data_defect | no | no |

The two sides agree on all four flags:
- The design note's stump sentence lands the solver on Prideswick at 15, which is the judge's expected wrong commit.
- The design note's lens-swap grid names Ristenholm 37 under the bed-only lens, which is the judge's nearest fork.
- The judge did not name any declared distractor as the surface read carrying the task. The first rung is Norman's attributed metric. The capacity report and the NRR files recompute exactly and sit off the path.

No mismatch, so this axis gives no send-back signal.

## Stump power (Gate F)
Moderate to good.
- **Expected wrong commit, Prideswick:** a solver rebuilds each census from the unit feed and sees Stennock's beds assigned through every long wait. Those beds are coded "03 planned transfer in", which looks like bureau traffic. The solver then names Prideswick on the weekend empty beds that Maria's email flags.
- **Secondary wrong commits:** Ristenholm (counting bureau allocations) and Lathingbury (Norman's metric).
- **Too-easy signal:** Maria's line "Stennock's unit is full every morning" points a careful solver at the right unit, although it reads as capacity.
- **Ask layer:** the workbook layer is dense with conformance traps (the ledger's table of skipped devices), so it should hold even a response that lands the call.

## Findings, ranked
1. **Step 1 of `submission.md` does not state the died-before-admission inclusion or the ward/ED filter (Gate A, wording).**
   - As written ("waited more than four hours from `dta_at` to the bed's assignment"), the step produces 193 placement-year deaths, not 213. It also moves six PNG bars and 50 workbook patients and deaths.
   - Reword step 1 to the golden Notes sheet's definition: level 3 referrals from a ward or the emergency department whose elapsed wait to a bed, or to death before a bed was assigned, exceeded four hours. Name the 20 died-before-admission deaths in step 2.
   - Figures unchanged, no rerun.
2. **The 225-minute clamp in `critical_care_referrals_202307_202606.csv` reads as generated (hygiene).**
   - 345 admitted waits sit at exactly 225 minutes (247 at level 3), and no wait falls between 232 and 249.
   - Any reviewer who checks the four-hour boundary will plot exactly this distribution.
   - In `generator/`, spread the clamped waits across a band below 232 minutes, then assert 213 / 2,163 / 629 / 148 / 27 / 15 / 12 and every grid cell unchanged.
   - Remit membership does not move, so the surface stays equivalent.
3. **The board-paper PDF dates itself before its own approval.** `accn_board_paper_2023-11-21_level3_capacity.pdf` has CreationDate 14 Nov 2023, but its last line reads "Approved at the meeting on 21 November 2023". The design note's "circulated before its meeting" defence does not cover a paper that records its own approval. Either set the date on or after 21 Nov 2023, or end the paper with "The board is asked to approve both changes."
4. **A file name contradicts its coverage.**
   - `ccrs_referral_levels_202307_202604.csv` is described as "exported at switch-off", and its entries end on 2024-04-01, but the name says April 2026.
   - Rename it to `..._202307_202404.csv` in the generator, the field guide's file list and `metadata.json`.
5. **The bureau fork is closed, but only by a definition plus an opinion (optional pin).**
   - One field-guide sentence in s.6 would remove the Ristenholm 37 reading, for example: "The bureau allocates the bed; the receiving unit does not choose which patient takes it."
   - Trade-off: it also disarms the Ristenholm lure, so add it only if the author wants that belt-and-braces over the secondary stump.
6. **The PNG tie order is unpinned.** The prompt orders trusts by the confirmable part, which leaves a five-way tie at 0. Make sure the generated rubric accepts any order inside that tie, because the golden's secondary sort by deaths is not asked for.
7. **Realism debts carried from pass 1:** constant `beds_open`, RIS and STN full on every recorded morning, and typed workbook totals. These are recorded in the design note as debts. They stay a residual "reads as generated" risk rather than a blocker.

Status of the pass 1 items:
- CCU is now defined as a ward in the field guide.
- Trust names now match the files.
- Five distractors are declared.
- `prompt_shape` is recorded as 07.
- The lens swap was re-run.
- Typed totals were kept, by choice.

`leak_check_report.md` is present (REVIEW, no LEAK), and the design note records the reduce-house-fixes audit. Both belong to the BUILD stage before this pass, and both need re-running after the rebuild below.

## Next action for the author
Make one generator-and-write-up pass:
1. Reword `submission.md` step 1 as in Finding 1.
2. In `generator/`, spread the 225-minute clamp below 232 minutes, correct the board-paper PDF date, and rename the CCRS levels file.
3. Rebuild, and assert every graded figure unchanged.
4. Re-run `leak.py` and reduce-house-fixes on the rebuilt pack.
5. Re-judge as pass 3.

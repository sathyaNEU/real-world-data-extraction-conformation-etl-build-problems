# Verdict (task139b, fresh re-judge)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE (optional in-house FIX_NOW: file-metadata dates, see Hygiene). No model rerun required.

**Why:** The pick memo (ay2027_indemnity_pick_ern_credit.pdf items 2 to 5) files the estimand literally: the credit is the ultimate indemnity the teams' *intakes* will not pay because the teams took them, at verified TTD+TPD+PPD, run rate of 20 places x 365 days, credited per segment from the pilot. The signed charter files the 3-team cap (3.2), the fill rule (3.3), the both-days and reopening place-day rules (5.2, 5.3) and the 17 teams (2.1). Executed word for word these give exactly the golden placement and $4.1M for the main call and for every ask. The main-call figures all recompute from the shipped files, and the only near-tie that decides a place (RW-SS third team versus HC-OT third team) is a rule threshold (2.44 against 3.0) that holds under every intake window I tried.

## Evidence (recomputed from the bundle; all reproduced)

| Item | Source files / fields | Recomputed | Golden |
|---|---|---|---|
| Pilot intakes, paid | assignments xlsx (5,227; 2,613 ERN, 2,614 UH) joined on legacy_claim_no to claims extract claim_type=IND; segment via crosswalk (0 mismatches vs extract) | 4,339 paid | 4,339 |
| Paid share ERN / UH: HC-SS, RW-SS, MF-SS | same | 64.9/86.6, 57.5/83.9, 68.1/86.7 % | same |
| Verified means (100 per group and segment, control digit dropped, all 1,600 matched, total $9,747,283.11) | KPA workbook | sheet total ties to the KPA report 5.1 | ok |
| Saving per intake (U share x U mean - E share x E mean) HC-SS, RW-SS, MF-SS | | $857, $741, $889 | same |
| Place-days per ERN intake (case log; claim_ref normalised for case, separators, zero padding, all 2,647 rows matched to ERN intakes, none to UH; both days counted, 34 reopenings added) HC-SS, RW-SS, MF-SS | ern_case_log | 21.40, 18.85, 23.03 | same |
| Team saving, all 8 segments | x 7,300 | 292,364 / 286,892 / 281,996 / 212,070 / 199,174 / 191,656 / 130,715 / 118,890 -> 290k, 290k, 280k, 210k, 200k, 190k, 130k, 120k (HC-SS, RW-SS, MF-SS, MF-OT, CN-OT, HC-OT, RW-OT, CN-SS) | same |
| Fill, intakes reported Oct 2025 to Sep 2026 (time_off_at_report Y, all new-system) x place-days/7,300 | claims extract | RW-SS 944 -> 2.44; others 4.1 to 5.3 | same |
| Total | 3 each HC-SS, MF-SS, MF-OT, CN-OT, HC-OT + 2 RW-SS | $4,105,562 -> $4.1M (also 4.1M from rounded team savings) | $4,100,000 |
| 2025 intakes (legacy LOST_TIME recomputed as disability_began <= report_date, parallel-run 29 May to 1 Jun 2025 duplicates removed, 2025 merged-away claims removed) | extract, dictionary, claim_merges | 1537, 822, 939, 708, 1356, 770, 1109, 666 | same |
| Indemnity paid Jan to Sep 2026 (one amount per payment_no, drop VOID checks, drop the 275 ACH-returned EFTs by trace, segment by claim) | payments, ach_returns | 3,724,903 / 4,652,050 / 1,805,107 / 3,992,890 / 4,276,854 / 5,232,875 / 4,999,081 / 7,281,913 -> rounds to golden in all 8 | same |

Literal-reading forks checked (each answer shown):
- **Per verified claim instead of per intake** (the KPA frame is paid-only, so U-E per sampled claim is the easy route): team savings 188k CN-OT, 174k MF-OT, 159k HC-OT, 111k RW-OT, 73k MF-SS, 68k CN-SS, 45k HC-SS, 42k RW-SS. That leaves HC-SS, RW-SS and MF-SS without good teams, a different placement. The memo's "intakes ... will not pay because the teams took them" and "A segment without teams carries no credit" rule it out literally, and the pilot was randomised by intake, so the paid share is an outcome. Forced.
- **No fill cap**: RW-SS 3 and HC-OT 2, total $4.20M. Charter 3.3 forbids it. Forced.
- **Intake window for the fill**: Oct 2025 to Sep 2026 gives 2.44; CY2025 corrected 2.42; CY2024 2.65; raw uncorrected 2.59; all rows 2.72; 2026 annualised 2.34. All under 3, so RW-SS = 2 on every window. Every other funded unit is 4.4 or more.
- **Place-day convention**: dropping reopenings gives 18.72; exclusive-day count gives 17.83. Both are filed (5.2, 5.3), not open. Rounded team savings change only for the excluded reading.
- **Voids and ACH returns**: 271 of the 275 returned EFTs and all 85 voided payment_nos have a reissued payment for the same claim, benefit and weeks, so counting them double counts. Netting is forced by the files (issued-only without netting gives HC-SS 3,747,560, outside the rounding).
- **Merged claims in the 2025 intake count**: not excluding gives HC-SS 1,554 against 1,537. The dictionary describes merged claims as rows merged into another claim, so counting both is a double count. Mild fork on an ask only (see Fix).
- **Trend factors**: memo item 4 says the credit is un-trended and Exhibit 4 is not shipped. The un-trended $4.1M is the only computable answer. Not a gap.
- **Sampling noise**: a bootstrap of the 100-claim samples puts the SD of a team saving at roughly 90k to 180k, so unit ranks near the cut are not statistically separable. Memo item 5 ("credited with what the pilot measured in that segment") files the point estimates as the basis and every solver gets the same sample means, so the call is forced, not contested. Noted, not a fail.

Provenance: the 5,227-intake register, the case log, the verification workbook and the memo agree on every segment and ID I traced. No misattribution; no figure from outside the package.

## Files/Hygiene
PASS. 16 files; formats csv, xlsx, pdf, docx; two large extracts (59,876-row claims, 63,135-row payments); distractors present and unused by the golden (draft_v3 charter, staffing plan, worker survey, the $47.4M pick base, ACH detail beyond trace match). Layer 1 mess is system-native (legacy and new claim numbers, control digits, nurse-typed claim_ref, parallel-run duplicates, legacy LOST_TIME flag, void and returned payments, amount repeated per line). No author or benchmark language inside files; no hidden sheets or comments. Minor, not stump-affecting, FIX_NOW at most: claims_data_dictionary.xlsx core.xml created 2025-05-19 although it documents the 2025-06 upgrade and a 2026-10-02 date; assignments xlsx created 2023-02-21 but prepared 2025-03-07. Not exclusion-level. Cross-batch check not done (other task folders are forbidden to me).

## Stump power (Gate F)
Moderate. The trap is the estimand: the KPA workbook and report invite a claim-level comparison of verified amounts, which leaves the strain units unfunded; a solver who treats paid-ness as an outcome of the randomised assignment places the teams in the strain units. The fill cap and the Layer 1 mess in the two asks (intake dedup and legacy flag, payments net of voids and returns) add independent failure points that I expect to cost most careful solvers some of the ask weight. The memo wording "intakes ... will not pay because the teams took them" is a partial cue, so a strong run may land the ITT, in which case the asks do the work. I cannot judge the empirical bar without model runs.

## Stumping type (Gate G)
`mechanism: decomposition_attribution / statistical_rigor (unit of analysis under randomisation) with binding_constraint (fill rule)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Reported figures (KPA verified amounts, paid shares) are correct; the difficulty is which estimand the randomised pilot supports. On clean data the task would still stump on the claim-level versus intake-level comparison.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Domain: the deciding quantity is the ultimate indemnity avoided by a randomised pilot, converted to a per-team-year credit for an actuarial pick; swapping in another field's nouns breaks it.
- Layer 1: legacy versus 2025 claim systems and codes, noisy nurse-keyed claim refs, parallel-run duplicates, merges, voided and returned payments. Layer 2: the intake-level (ITT) estimand with place-day conversion and the capacity fill cap.
- Easy route: a strong analyst who read every rule correctly compares verified ERN against UH amounts per paid claim (the sampled population), ranks on that, and files CN-OT, MF-OT, HC-OT, RW-OT, MF-SS, CN-SS units with small credit and no HC-SS, RW-SS team; the correct answer funds HC-SS, MF-SS and RW-SS first. This is a choice of estimand, so it counts as analysis. The fill rule alone is rule application but does not decide the main call's core.

## Fix
none (fix location: none). Optional, in-house: align docProps dates on the data dictionary and register workbooks; optionally state in the prompt or dictionary that merged-away claims are not counted as separate intakes (ask 3 only; it is already derivable from the merges file and dictionary).

## Disposition

APPROVE, and the build ships on the judged pack with no change to it (the final rebuild is byte-identical to the
commit the judge read). This is the one re-judge after the stage 4 FIX_NOW pass (`determinism_check_report.md`, kept
as it was).

- **The merged-claim reading in supplementary 3, the judge's mild fork.** SF28 asserts both readings in `checks.py`
  and `verify.py` reproduces the golden on its own path: counted once with the claim it was merged into (the golden,
  1,537/822/939/708/1,356/770/1,109/666, the dictionary and the merge file executed literally), and both claims
  counted (every segment 4 to 17 high: HC-SS 1,554 as the judge found), with both claims dropped (4 to 17 low) and a
  dedup on the first-report fields across the year (23 to 186 low) asserted beside them. The optional sentence in the
  prompt or the dictionary that a merged-away claim is no separate intake is not added: the judge finds the exclusion
  derivable from the merge file and the dictionary already, and a filed rule would adjudicate the ask's one silent
  device.
- **The optional file-metadata dates.** Left as they are, the pack unchanged: a workbook kept in use keeps its creation
  date. The data dictionary was set up on 19 May 2025, before the upgrade it documents, and last saved on 2 October
  2026; the assignment register was set up on 21 February 2023, before the pilot's first triage date of 1 March 2023,
  and last saved on 7 March 2025, the date its Notes sheet carries. Both sit inside the pack's band.
- **Sampling noise.** Noted, no change: memo paragraph 5 files each segment's credit at what the pilot measured there,
  so every solver reads the same sample means and the call is forced.
- **Gates F, G, H.** Stump power moderate; Gate G analytical, not a defect; Gate H domain and layers pass, the decisive
  step analytical. No re-judge owed.

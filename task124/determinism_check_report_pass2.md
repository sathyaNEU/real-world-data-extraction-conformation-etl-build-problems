# Determinism check, task124 (pass 2)

Stage 4 re-judge, 2026-10-12: one isolated judge thread on a fresh copy of the repaired cut (the 16 files under
`target/`, byte-identical to those in the shipped `target.zip`), the prompt, the submission's graded blocks as they
stood at the PAUSED commit 5974390 (key assumptions empty) and the judge's system prompt, verbatim. It opened no design
note, generator, golden, metadata, earlier report or other task. Its verdict follows verbatim, between the rules; the
disposition after it records what the main session did with it. Pass 1 (NOT_DETERMINISTIC, SEND_BACK, on the stage 3
cut) is `determinism_check_report.md`.

---

# Verdict, task124 (re-judge)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair needed; optional wording tightening on two minor forks (below) would not change the golden and needs no rerun.

**Why:** Every committed answer reproduces from the shipped files. The main call turns on the plan's section 4.3 share "among the district's lines of its construction era that have no usable tap card", estimated from the 78 main segments whose every service line was verified (the replaced mains named in lsl_extract_field_notes_2027-01.md), not from the selection-driven single-line visits. The notes say how each verification arises, the 78-segment census is a clean break (next segment 0.42), and the plan's schedule rule (5.3) and cost rule (4.2, 4.3) are literal.

**Evidence (recomputed, all reproduced):**
- Verifications joined to inventory (CIS premise zero-padded to 8 digits via crosswalk, 0 unmapped; unpadded maps 0 of 1,569 agreement premises, so the padding is derivable from the crosswalk and notes): 4,911 distinct no-tap-card, pre-1989 verified lines (5,136 rows pre-1989 no tap card). No line has conflicting results across visits.
- Segment coverage: exactly 78 segments with 100% of lines verified, next highest 0.421. Shares on those segments' no-tap-card lines, by latest result: 440/792 = 0.5556, 96/304 = 0.3158, 14/168 = 0.0833. Matches 0.556 / 0.316 / 0.083.
- All-verification shares: 0.7625 / 0.5847 / 0.2168, matches the stated wrong basis.
- Zone costing (lead+GRR + share x unknown at replacement unit cost, rest at dig cost, + $185k): RZ-07 23.07M (1,672 lines, 2027), RZ-02 34.83M (2,141, 2029), RZ-11 29.79M (1,960, 2030), RZ-04 24.41M (1,482, 2031), RZ-09 28.13M (1,830, 2032), RZ-01 28.63M (1,971, 2033), RZ-05 26.80M (1,752, 2034), RZ-12 15.21M (932, 2034), RZ-03 20.28M (1,292, 2035), RZ-08 22.12M (1,382, 2036), RZ-10 12.97M (772, 2036), RZ-06 18.43M (1,078, 2037). All match the golden at the stated rounding. Total 284.671M, 10.504 programme years, last zone 2037, inside 31 Oct 2037. The boundary margins (nearest: RZ-10 at 9.82 yr, RZ-02 at 2.14 yr) are clean and not estimation-sensitive. No unknown line has year_built 0.
- Competing bases: all-verification shares give 347.5M, 12.82 yr, RZ-06 in 2039; one pooled share on the whole-segment lines (0.435) gives 327.6M, 12.09 yr, 2039. Both flip the call (No instead of Yes), as the FINAL_RECOMMENDATION states.
- Ask 2 (payments): latest closing per site (5 RECLOSED replace the first), completed_utc converted to Eastern, change orders added once per CO (all 45 reconcile to the xlsx log; every CO's sites fall in one quarter, so no allocation fork), divided by distinct sites, by contract_no. All 12 cells reproduce to the dollar (13,890 / 13,494 / 13,416 / 13,673; 14,509 / 13,937 / 13,903 / 13,568; 14,488 / 14,459 / 15,008 / 14,784). Eastern quarters give 135/195/315/127, matching LSLR_progress_report_2026.pdf, which is what pins the time zone.
- Ask 3 (agreements): distinct lines with SIGNED forms (545 lines have two signed forms; no line is both signed and withdrawn), premise mapped via padded crosswalk, zone from inventory: 975/1,217/1,118/954/1,017/857/889/518/626/663/368/539. All reproduce.
- Chart/paper ask: finish years and deadline are determined by the above.

**Literal-reading forks (answers each gives):**
1. Share estimator: literal text of 4.3 does not name the verification subset. Using all verifications (0.763/0.585/0.217) gives 2039, "No". The notes (verification routes, "every service on the replaced main is exposed"; other rows "raised by a customer reporting lead... a leak... the 2024 consultant ranking of services likely to be lead") make the whole-segment census the only unbiased basis, so a rigorous expert is forced to it. This is the intended analysis, not a semantic gap. Not a fork I would fail.
2. Ask 3 zone attribute: zone_on_form differs from the inventory zone on 171 signed lines (six zone pairs; mismatches persist to Oct 2026 forms; 2027 forms have 0). Counting by zone_on_form gives different counts (e.g. RZ-07 1,008 vs 975, RZ-11 1,140 vs 1,118). No shipped file states that the form zone is the pre-revision-2 zone (the SOLUTION_STEPS sentence "printed before plan revision 2 redrew six boundaries" is not in any file; the notes only say "the replacement zone printed on the form", and the inventory zone is stated to be "under plan revision 2"). The ask is "service lines in each zone" of the plan, whose zones the inventory defines, so the inventory zone is the better literal reading, but this is the softest point in the package. Minor residual risk; optionally the SOLUTION_STEPS claim about redrawn boundaries should be reworded as "the inventory zone is the plan's zone" (solution-block edit only).
3. Ask 2 quarter basis: closed_on instead of completed_utc moves 1 site (Brannigan Q2 13,513 vs 13,494; Q3 13,406 vs 13,416); UTC instead of Eastern moves 13 sites. The prompt says "completed", the notes name completed_utc as the completion time, and the progress report states Eastern quarters, so the golden reading is the literal one.
4. Chart: bar start positions (continuous running-cost start) are not specified by the prompt; graded content (finish-year labels, deadline) is determined.

**Files/Hygiene:** PASS. 16 files; formats: csv (9), xlsx (2), pdf (2), docx (1), md (1). One file of 87,410 rows (inventory), 5 other extracts 6k to 85k rows. Distractors present and unused: lcr_tap_samples_2025_2026.csv, ami_meter_exchanges_2023_2025.csv. Provenance in extract_log and field notes is in-fiction (GIS and Asset Records), no authoring or benchmark language, no solver-facing hints. Dates are coherent (extract 8 Jan 2027; plan 20 Oct 2026; CIP draft 14 Dec 2026; progress report 6 Jan 2027). Real-looking operational noise present (two date formats, vendor number change, reclosings, CO repeats). Nothing exclusion-level.

**Stump power:** Good, with the main call binary (Yes/2037 vs No/2039). Strong models are likely to take the all-verifications share or a pooled/regression share, since the verification file is the only direct evidence and the 78-segment census must be found by a coverage analysis the prompt never mentions; the field notes' description of verification routes is a pre-disarming signal (too-easy risk: partial), but identifying the census and computing the era shares still takes real work. The asks add independent traps (CO repeat, UTC to Eastern, reclosed rows, vendor change, zero-padding, zone attribute) that stack on top.

**Stumping type:** mechanism: statistical_rigor (selection bias in the estimand's sample, method/estimator choice on honest data), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no. No reported figure is wrong; the difficulty is choosing the unbiased sample for the unknown-line share, and it would persist on perfectly clean data.

**Three rules:** domain: pass, layers: pass, decisive_step: analytical. The field's own work is estimating the lead/GRR prevalence among unknown-status lines for an LCRI inventory plan from a representative verification sample and costing the schedule from it; the easy route (use every field verification, 0.763/0.585/0.217, as the expected share) is what a strong analyst who read every field and rule correctly would take, and it gives $347.5M, 12.8 years and "No, RZ-06 finishes in 2039". Layer 1: CIS/WMS code and ID migration, zero-padded premises, UTC vs Eastern, vendor re-registration, reclosings, repeated CO totals. Layer 2: selection bias in who gets verified.

**Fix:** none required (solution: optionally reword the Step 6 statement about redrawn boundaries so it relies only on the inventory zone being the revision 2 zone, since no shipped file says the form zone predates revision 2).

---

## Disposition

APPROVE, shipped. No figure, no file under `target/` and no main-call sentence moved.

1. **Fork 1, the share estimator.** No action. The judge reads the whole-segment census as forced by the field
   notes' account of how lines come to be verified (the intended analysis, not a semantic gap), and both competing
   bases it ran (every verification; one pooled share on the whole segments) file 2039.
2. **Fork 2, ask 3's zone attribute: the optional fix, taken.** Step 6 of the write-up no longer says the form zone
   was printed before plan revision 2 redrew six boundaries, which no shipped file states. It now reads: "For the
   agreements, counted distinct service lines with a SIGNED form in access_agreements_2022_2026.csv, premise numbers
   mapped through the crosswalk, in the zone the inventory gives each line, its replacement zone under plan revision 2
   (lsl_extract_field_notes_2027-01.md), rather than zone_on_form, the zone printed on the form." It rests only on the
   field notes' definitions of `zone` and `zone_on_form`. The board paper's note under the agreement table carried the
   same claim ("forms signed before October 2026 print the zone the line was in before plan revision 2"), with an edge
   that two forms signed on 3 and 12 October 2026 contradict; it now reads "in the zone the inventory gives each line
   under plan revision 2; some forms signed before the revision print a different zone", which `checks.py` B5 asserts
   (every signed form whose zone differs from the inventory's was signed before 20 October 2026). No filed rule counts
   agreements by either zone, so the ask's device stays silent (B7).
3. **Fork 3, ask 2's quarter basis.** No action: the golden reading is the literal one (the completion time, in the
   Eastern quarters the progress report ties).
4. **Fork 4, the chart's bar starts.** No action: the graded content (finish-year labels, the deadline) is determined.

**Scope.** Wording only. `target/` is byte-identical to the cut the judge and the leak reader read; the workbook,
`metadata.json` and `generator/figures.json` are byte-identical; the board paper changed in that one note.
`freeze.py check --mode determinism` passes against the snapshot taken before the stage 4 repair.

**Gates on the final rebuild.** `checks.py` 108 assertions, 0 failed; `verify.py` green; two full runs
byte-identical, each with its own second build; `figures_check.py` exit 0 (75 figures); `precut.py` exit 0 (38
checks, 0 FAIL); voice-check PASS; `leak.py --asof 2027-01-11` REVIEW, no LEAK (the same seven lines); `guard.py
surface` 0 promoted, `heart` WARN (`repeat.gate_g`, answered in the draw).

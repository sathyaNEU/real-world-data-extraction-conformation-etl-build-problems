# determinism-check report, task154 (architecture 2), 2026-11-02

Judge thread: one pass, sonnet, medium. Scratch: /tmp/determinism-check-task154-1793602500/ (verdict.md there). target.zip md5 b6d0643e186cb81b4a18410542f71b99.

## Verdict
NOT_DETERMINISTIC on the field-check ask only (second sheet); the main call and the dig-plan sheet are forced. No SOLUTION_WRONG.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The register ships its own "Field Depth (%)" column against its own "Nominal WT". For 12 of 59 digs that wall (0.250 in) disagrees with the wall of the upstream joint in the tally (0.188 in). No sentence in the prompt or any file says which governs. The golden bands hold only under the tally wall (87.5 / 94.1 / 77.8 / 100.0 / 85.7 per cent within 10 points); the register's own column gives 68.8 / 82.4 / 66.7 / 80.0 / 57.1. "Largest inspection minus field" is also unpinned (signed maximum vs largest magnitude). Gates C and E fail for the second sheet; governing label underspecified_objective. The main recommendation passes A to E.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Ext. corrosion anomalies at 60 or deeper (dug) | 59 | 59 (register 60 rows, re-excavation 028R) | yes |
| R-7 failure | 12 Aug 2019 | 12 Aug 2019 (prior day 93 per cent of design, run day 14) | yes |
| R-5 failure | 9 Jul 2016 | 9 Jul 2016 (prior day 98, run day 15) | yes |
| R-3 failure | 12 Jul 2011 | 12 Jul 2011 (first "U" inspection) | yes |
| Days failure to run | R-7 2,102; R-5 3,231 | 2,102; 3,231 (14 May); 2,101 / 3,230 if 13 May | yes |
| R-7 / R-3 restoration | 10 Jun 2030 / 16 Oct 2028 | same; R-5 bed on Deferred sheet (2032 to 2036) | yes |
| R-3 anomalies reach 80 before restoration | none | earliest 24 Mar 2031 | yes |
| Digs by year | 4, 9, 11, 6, 4 = 34 | same (R-7: 4,7,6,3,0; R-5: 0,2,5,3,4) | yes |
| Funded | 4,5,5,5,5 = 24 | same | yes |
| 34 mileposts and depths | listed | all reproduce to 2 decimals | yes |
| Band table (tally wall) | as filed | as filed, n 16/17/9/10/7 | yes |

## Competing answers that survived
Main call (digs 2027/28/29/30/31, total), second readings tested:
- Run end 13 May, per-anomaly pass day, 365 vs 365.25, failure date from the inspection call-out, R-3 failure 2008 to 2011, failure threshold 30 to 90 per cent, raw odometer/5280 zones, 31 December boundary (closest crossing 28 days): all identical to the golden. No fork.
- Failure date set to last "normal" inspection: 3,9,12,5,4 = 33 (outlying; the RMU gives the exact day).
- No stop at restoration (R-3 and R-7): 4,9,11,6,20 = 50; R-3 only 35; R-7 only 47. R-7 restoration read as start of 2030: 4,9,11,3,4 = 31.
- Full-life rate since 8 Oct 1974: 0,0,0,0,0 = 0 ("yes, 24 suffice").
- Unfiled but forced: growth basis (Section 6.4 gives no rate; nothing states the whole depth accrued between the zone's failure and the run) and growth stopping at restoration. The golden basis is the only one built from the shipped CP records. The judge finds no surviving defensible alternative, but the estimand is inferred, not filed.
- Mileposts: raw odometer/5280 is off by +0.03 to +0.06 mile for all 34, but the ILI summary says the marker survey ties the run to the line; counted wrong, not a fork.

Field-check ask (FORK SURVIVES):
| Band | Golden: tally wall (within 10 %, mean, largest signed) | Register Field Depth column | Golden, largest by magnitude |
|---|---|---|---|
| 60 to 64.9 (n16) | 87.5, 1.2, 10.9 | 68.8, 5.2, 21.3 | 12.4 |
| 65 to 69.9 (n17) | 94.1, -0.4, 9.4 | 82.4, 1.5, 23.6 | 12.0 |
| 70 to 74.9 (n9) | 77.8, 2.7, 11.8 | 66.7, 6.3, 26.9 | 11.8 |
| 75 to 79.9 (n10) | 100.0, 1.9, 8.6 | 80.0, 5.9, 18.3 | 8.6 |
| 80 to 84.9 (n7) | 85.7, 5.1, 12.6 | 57.1, 10.4, 26.0 | 12.6 |
- Wall fork rows: D25-005, 007, 012, 013, 020, 025 (Prairie) and 039, 040, 045, 046, 052, 058 (Kaw Valley); register 0.250 vs tally 0.188. The tally wall is better supported (ILI summary: depth is "a percentage of the joint's nominal wall"; differences stay inside the tool's plus or minus 10 spec, against up to 26 on the register wall) but no file says it governs.
- Cut-outs: D25-005 76.6 (tally wall) vs 57.6 (register wall); D25-007 72.3 vs 54.4; the other five cut-outs have equal walls.
- Counting the re-excavation twice moves only the 65 band (94.4, -0.1, 9.4). Treating the 7 cut-outs as blank deletes the 80 to 84.9 band.
- No fork: 59 sites counted once; Kaw Valley mils as inches single reading; band edges and inclusive vs exclusive "within 10" identical.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | csv (8), pdf (4), xlsx (2) | yes |
| Large file | 25,000 rows or more | tally 36,009; RMU readings 31,283 | yes |
| Distractors | 2 or more named, none labelled by file name | metadata.json names soil resistivity, one-call tickets, class location study (judge also saw crossings, annual CP survey as unused) | yes |
| Distractor weight | unused, relevant, ruled out by a shipped fact | not separately tested by the thread; judge found them unused by the solution; arithmetic route to a graded figure not seen | yes (unconfirmed on "ruled out") |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), golden/ holds both | yes |
| Asks | multi-dimensional, unit and rounding stated | dig schedule, banded field check; mileposts two decimals, rest one decimal | yes |
| Prompt shape / 25 criteria | identifiable, 25 or more | shape identifiable; rubric count not checkable here (generated at portal) | not verified |
| Reads as real | no LLM tells | judge saw none in pdf text, csv headers, xlsx cells | yes |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical; design note stump sentence: the full-life rate files 0 digs, the real driver is exposure time since a zone's rectifier failed. Match. The thread names the full-life rate as the easy route, not a declared distractor; the declared distractors are soil, one-call and class location, none the surface read. Design note's `## Three rules` has No decoy, Not semantics, Not rule application lines. Note: the note claims "nothing filed says how a growth rate is estimated" (Not rule application), consistent with the judge's "unfiled" growth basis; the judge accepts it as forced but inferred. The field-check ask rests on a data defect (register wall) and is semantics; allowed for an ask.

## Gate H
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1: RMU readings in UTC, odometer vs marker-tied milepost, two contractor register layouts, mils vs inches. Layer 2: growth by exposure time since protection loss, stopped at restoration. Easy route: depth over full life gives 0 digs ("yes, 24 suffice"); the thread says a strong analyst who cleaned everything can still land there.

## Stump power (Gate F)
Plausibly strong on the main call: the easy age-based rate answers 0 digs; the right route needs the failure day from about 31k daily RMU readings (R-3 only from the inspection log), restoration dates from Projects vs Deferred, and a crossing-year count. The thread did not classify the decisive step as landable-by-standard-method. Risk: a response lands the call but misses exact counts through one zone's date; the field check adds ask-level difficulty (wall choice).

## Findings, ranked
1. Field-check ask: wall thickness for field depth is unfiled (register 0.250 vs tally 0.188 on 12 digs); bands differ materially (e.g. 85.7 vs 57.1). FIX_NOW.
2. "Largest inspection minus field" unpinned (signed max vs magnitude; band 60 to 64.9: 10.9 vs 12.4).
3. Main call growth basis is an inferred estimand, not filed (accepted as forced; record in the design note).
4. Distractor ruling-out and the 25-criteria rubric were not verified by the thread.

## Next action for the author
Add to the second-sheet clause of prompt.txt, as a WHAT only: field depth as a per cent of the wall thickness the inspection tally gives for the anomaly's joint, and the largest as the largest signed inspection minus field difference; the analytic surface and stump stay unchanged and goldens need no figure change. Alternative: correct the register's nominal wall so both walls agree. Record the inferred growth basis in the design note; if a pin is wanted, file only the population (anomalies in zones whose protection was lost) and the window, not the rate formula. Re-judge once after the fix.

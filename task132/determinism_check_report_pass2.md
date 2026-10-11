# determinism-check report, task132, 2026-10-11 (pass 2)

**Run note.** This is the single re-judge after pass 1's FIX_NOW. The `Agent` tool was not available in this harness, so the judge pass ran in the orchestrator's own context rather than in a spawned thread. Isolation came from ordering. A fresh copy of `target/` went to `/tmp/determinism-check-task132-pass2-20261011T094456Z/target/` (sha256-identical to the source). The spawn prompt was assembled with the judge system prompt inlined verbatim (byte-checked) and saved as `spawn_prompt.md` beside it. Nothing outside that path, apart from `prompt.md`, `submission.md` and the system prompt needed to build the brief, was read until `verdict.md` was written there. The design note, card and `metadata.json` were opened only afterwards, for the checks below. Pass 1's report was not read. The one leak from the brief: the invocation named pass 1's fix items (the step 4 wording and the memo phrase), which concern write-up wording, not any figure.

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
**Three rules (Gate H):** domain: pass, layers: pass, decisive_step: analytical

## Why
The 13-lot call is forced. AM-PC-014 rev 4 pins every step:
- the failure definition (5.1);
- module age from the rotating-item fitted date (3, 5.2);
- exposure over the work-order history's own period (5.3);
- support by bay and stage from the Approved 2026 sheet, up to but not including the commissioning month, and through December 2035 where no scheme falls in the period (4.1, 4.2);
- available stock (7);
- the 95 per cent Poisson cover (8).

The survival-weighted monthly recursion gives 298.6 expected failures, and 13 lots holds for any mean in (287.3, 311.2]. Every procedure-compliant variant falls in 297.7 to 299.2, and every route to another lot count breaks a shipped rule. All supplementary answers reproduce exactly at the stated rounding.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Failures per 5.1 (VPR-340, CM/EM, PSU, COMP/CLOSE) | 210 (implied) | 210, one to one with the FAILED removals by `removal_wo` | yes |
| Band rate 0-9 | 0.0052 | 0.005162 (15 failures / 34,870 module-months) | yes |
| Band rate 10-14 | 0.0233 | 0.023284 (49 / 25,253) | yes |
| Band rate 15-19 | 0.0508 | 0.050844 (68 / 16,049) | yes |
| Band rate 20-24 | 0.1186 | 0.118634 (66 / 6,676) | yes |
| Band rate 25+ | 0.2945 | 0.294479 (12 / 489) | yes |
| Expected failures to end of support | 298.6 | 298.606 | yes |
| Modules available | 15 | 12 serviceable + 3 at repair (= 3 OPEN RMAs); 7 quarantine excluded | yes |
| Main call: lots / modules / cost | 13 / 325 / CAD 638,625 | 13 / 325 / 638,625 | yes |
| Cover, 8 lots | 0.0%, CAD 393,000 | 0.0%, 393,000 | yes |
| Cover, 9 lots | 0.0%, CAD 442,125 | 0.0%, 442,125 | yes |
| Cover, 10 lots | 2.6%, CAD 491,250 | 2.6%, 491,250 | yes |
| Cover, 11 lots | 32.2%, CAD 540,375 | 32.2%, 540,375 | yes |
| Cover, 12 lots | 83.6%, CAD 589,500 | 83.60%, 589,500 | yes |
| Cover, 13 lots | 99.1%, CAD 638,625 | 99.13%, 638,625 | yes |
| Cover, 14 to 22 lots | 100.0%, CAD 687,750 to 1,080,750 in steps of 49,125 | 100.0% each, the same nine costs | yes |
| Expected failures Oct to Dec 2026 | 11.6 | 11.6 | yes |
| 2027: failures / relays on 1 Jan | 45.1 / 1,163 | 45.1 / 1,163 | yes |
| 2028 | 44.7 / 1,094 | 44.7 / 1,094 | yes |
| 2029 | 42.9 / 973 | 42.9 / 973 | yes |
| 2030 | 40.6 / 884 | 40.6 / 884 | yes |
| 2031 | 36.1 / 783 | 36.1 / 783 | yes |
| 2032 | 30.0 / 695 | 30.0 / 695 | yes |
| 2033 | 23.9 / 564 | 23.9 / 564 | yes |
| 2034 | 16.0 / 373 | 16.0 / 373 | yes |
| 2035 | 7.8 / 201 | 7.8 / 201 | yes |
| Region North | 117.5 | 117.5 (current region from `substations.csv`, which agrees with the program sheet) | yes |
| Region Central | 54.7 | 54.7 | yes |
| Region South | 126.4 | 126.4 | yes |
| Memo ask 1 (opens on 13 lots, 99.1% cover) | as stated | consistent with the workbook | yes |
| Memo ask 2 (chart of the ten period values) | as stated | consistent with the workbook | yes |
| Golden workbook extras (expected module-years by band 2,206.2 / 1,466.2 / 1,704.6 / 868.9 / 215.1; failures by band 11.4 / 34.1 / 86.7 / 103.1 / 63.3) | in `golden/vpr340_psu_final_buy.xlsx` | identical | yes |

## Competing answers that survived
None. Closed routes, for reference (full table in the scratch `verdict.md`):

| Route | Mean, lots | Closed by |
|---|---|---|
| No renewal (the stump) | 431.4, 19 | 1, 3, 6.1, 6.2 |
| Relay-age rates | 223.7 to 249.9, 10 to 11 | 3, 5.2 |
| Staged scheme at first / last stage | 273.7 / 324.6, 12 / 14 | 4.1 and the program Notes |
| Superseded 2025 sheet | 262.4, 11 | 4.1 and the sheet's own title |
| Commissioning month counted | 303.2, 13 | 4.1; the cover cells would move |
| Continuous-time hazard | 297.7, 13 | 3 and 6.1; P(11) would move 1.8 points |
| Quarantine plus the 5 returns-shelf modules counted | 12 | 7 and the dictionary |

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10+ | 12 | yes |
| Distinct formats | 3+ | 5 (csv x6, xlsx x3, docx, pdf, txt) | yes |
| Large file | 25,000+ rows or a large DB | `eam_work_orders_protection_2021-01_2026-09.csv`, 32,569 rows | yes |
| Distractors declared | 2+ in `metadata.json`, none labelled in a name or file | 3 (`veldtek_rma_log_vpr340_psu.xlsx`, `feeder_relay_operations_2025.csv`, `pc_relay_maintenance_compliance_2025.xlsx`); no label anywhere under `target/` (grep clean, XML included) | yes |
| Distractors relevant and unused | same world, weighable, not used by the solution | all three are same-fleet artifacts the solution does not use. The RMA log corroborates the stock file (3 OPEN = 3 AT REPAIR) and does not contradict it | yes |
| Wrong-basis distractor reproduces and is ruled out | if any answers a graded quantity | none of the three answers the decision or a graded quantity. The superseded 2025 sheet (inside a used file, undeclared) does give 11 lots and is ruled out by 4.1 and its title | n/a |
| Deliverables | 1 to 3 | 2 (xlsx, docx) | yes |
| Format family | none required | n/a | yes |
| Multi-dimensional asks | not stacked lookups | 15-order cover and cost curve, 10-period forecast with 9 relay counts, 3 regions | yes |
| Golden deliverables present | every named file | `golden/vpr340_psu_final_buy.xlsx`, `golden/psu_last_time_buy_memo.docx` | yes |
| Units and rounding stated | every ask | all stated, with one soft spot: "what that order costs" inherits "in dollars to the nearest dollar" from the previous sentence (all costs are whole-dollar multiples of 49,125, so rounding cannot bite) | yes, with note |
| Prompt shape and 25 criteria | shape identifiable, 25+ | shape 04 (dial setting over a period forecast); prompt arithmetic gives about 58 (3 + 30 + 10 + 9 + 3 + memo 3). The generated rubric itself was not inspected | yes |
| Pack realism | nothing reads as LLM generated | judge hygiene PASS: varied crew text, cancelled duplicates, legacy regions, MMS 1 July dates, superseded sheet, in-fiction docProps | yes |
| Golden realism | real work products | the memo renders to one page (LibreOffice), opens on the order and the cover, and has a labelled bar chart, a 12/13/14 table and a sign-off line. The workbook is plain, with Buy, Lot settings, Outlook by year, By region, Failure rates and Notes sheets, and one-decimal number formats. One small tell: the chart caption says "(one decimal)" | yes, with note |
| No em dashes | none | 0 in `prompt.md`, `submission.md`, the memo XML and the workbook strings | yes |
| Pass 1 fix landed | memo and step 4 restate the survival-weighted recursion | memo: "each month the old module's rate is weighted by the chance it is still fitted and the 0-9 rate by the chance it has already been replaced"; step 4 cites 1, 3, 6.1 and 6.2; the band rates are in Critical Components | yes |

## Gate G reconciliation
| | Judge (this pass) | Design note and card |
|---|---|---|
| mechanism | forecasting | forecasting (`gate_g: forecasting`) |
| stumping_family | analytical_non_defect | analytical_non_defect |
| surface_read_dependency | no | no |
| sole_data_defect | no | no |
| Gate H | domain pass, layers pass, decisive_step analytical; easy route 431.4 failures, 19 lots | `stump_class: analytical`; `analyst_test`: 431.4 failures, 19 lots instead of 13; `domain_test`: utility asset-condition and spares work |

Full match on every field, and the easy route agrees to the decimal. The build reads the same shape from outside as from inside. The judge named no surface read at all, so no declared distractor was cast as the surface read carrying the task. The judge's bin for 13 lots (287.3 to 311.2) also matches the design note's asserted bin.

## Stump power (Gate F)
The renewal step carries the stump. A strong model that cleans everything and reads every rule can still apply 6.2 to the present module's own module-months as it ages, which gives 431.4 expected failures and 19 lots (CAD 933,375). Relay-age, staging and superseded-plan slips give 10 to 14 lots.

Too-easy signals the judge named: AM-PC-014 and the program Notes state module age, staging, the outage-from-the-1st pin and the stock rule outright. Those lower rungs are therefore documentation-disarmed, and the renewal is effectively the single lever. Because it is a computation rather than rule-discovery, it is plausible against strong solvers.

## Findings, ranked
1. **Residual reviewer risk on the decisive step (no change advised).** The design note records that round 2's two solvers named the renewal reading and declined it because the procedure does not spell it out. A reviewer holding contrasting responses could try the "reached the insight and still disagreed" rule on it.
   - The judge ruled it forced before seeing that record. 6.1 binds the rate to "a module in service", and 3 defines the module in service after a failure as the replacement, fitted that month and aged from its own fitted date. Applying the old module's rate in a month it is no longer fitted therefore breaks 6.1, which makes the no-renewal route an error, not a licensed reading.
   - Step 4 already cites 1, 3, 6.1 and 6.2, which is the right defence.
   - Writing the recursion into AM-PC-014 would hand out the stump (a Gate F too-easy signal), so don't.
2. **Optional, `submission.md` Final Recommendation.** "13 lots cover every expected failure to the end of support with a 99.1 per cent chance" should read "cover all failures to the end of support with a 99.1 per cent chance". The cover is over realised demand, not over the expected count.
3. **Optional, `submission.md` Deliverable Answers, memo.** Ask 1 adds "against 83.6 per cent for 12 lots", and ask 2 specifies "bar chart" with "each bar labelled to one decimal". The prompt pins only "opens with the lot count and the cover it gives" and "shows the expected failures by year as a chart". Keep the golden as it is, but word the graded answers to what the prompt pins, so that a correct line chart or an unlabelled chart is not marked down.
4. **Optional, `submission.md` step 4.** State the survival update ("the chance it is still fitted falls each month by its band rate over twelve"). This makes the 6.1 pin explicit against the continuous-hazard variant, which moves P(11 lots) from 32.2 to 34.0 and several period cells by 0.1 to 0.4.
5. **Note, `prompt.md`, no change now.** "and what that order costs" does not restate its unit and rounding inside its own sentence. It is harmless because every cost is a whole-dollar multiple of 49,125, and a prompt edit would change what solvers saw.
6. **Optional, golden realism.** Drop "(one decimal)" from the memo's chart caption in `golden/psu_last_time_buy_memo.docx`. It reads as an echo of the spec, not as a caption a planner would write.
7. **Bookkeeping, never ships.** The card's `driver_concrete` (`.claude/skills/fingerprint/cards/task132.json`) still says "applies only while it is likely to survive". Pass 1 retired that phrase from the memo because it read as a cutoff (328.8, 14 lots).
8. **Outside this pass's scope, for the author to confirm.** The design note's repair-3 entry says "Solver round 2 measured the seed-150 world; no round has been run on this one", and its SOLVER ROUNDS section lists only rounds 1 and 2. If that is current rather than stale, the stage-6 worth-it gate has not been measured on the seed-1215 world being shipped.

## Next action for the author
Advance task132 to SHIP (stage 8) on this APPROVE. Findings 2 to 4 and 6 are wording-only, move no figure and need no re-judge, so they can be folded into `submission.md` and the memo caption before hand-over or left as they are.

# determinism-check report, task188, 2026-10-13 (pass 3)

Record note: pass 3 is the recorded pass. Pass 1 (FIX_NOW on one write-up count) and pass 2 (DETERMINISTIC, APPROVE, before the data recut) came back as messages, not files. This pass verifies the recut: the second load of 22 June now brings back only the June Tuesday nights, and no copy lands on a night its site ran. The judge thread was spawned by the main session from /tmp/determinism-check-task188-pass3/judge_brief.md (no Agent tool in my runtime). Its verdict is /tmp/determinism-check-task188-pass3/verdict.md.

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: method_selection, stumping_family: method_selection, surface_read_dependency: no, sole_data_defect: no

## Why
Every committed answer reproduced from the bundle alone: Westbrook 2.3 against South Prairie 1.8, break-even 18 per 1,000, and the per-zone case, trap-night run and trap-night lost counts. The 22 June soft spot is closed. The 206 records (tn_id 7231 to 7436, 103 sites on 3 June and 103 on 10 June, both Wednesdays) collide with no (site, set_date) in the table. They are exact catch copies of the preceding Tuesday nights (572 of 572 and 589 of 589 species-sex rows match). The shipped text excludes them as runs:
- Protocol 3.3 sets traps Monday and Tuesday only.
- Protocol 3.5 allows Wednesday and Thursday nights only at CO2 sites after a zone's first positive pool. The copies include gravid traps, all eight zones and 3 June, before any positive pool.
- Protocol 4.1 pools every trap-night's Culex females, yet 185 copy nights with Culex females have no pools.
- Protocol 6.2 and the dictionary's `entered` line record the June reload of 22 June.

One reading is forced. The as-entered count is the only rival, and it contradicts 3.3, 3.5, 4.1 and 6.2. Drop-the-load and keep-first-or-last on the catch signature both give the golden. A key-based dedupe on (site, set_date) removes nothing and gives the as-entered column. The load does not touch the main call (week of 10 and 11 August only).

Residual softness, accepted: no document says outright that the reload repeats nights. Identifying the echo takes a content comparison plus the schedule rules, which is the intended Layer 1 mess and is not a fork. A second, lesser risk: the bundle never names the estimator. "Estimated", the 50 against 10 pooling and 42 of 70 positive pools carry the case for maximum likelihood. A solver who reads the minimum infection rate as "the usual index" is a defensible but not airtight residual. Filing the HOW to close it would turn the decisive step into rule application, so it is not recommended.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Westbrook Culex females per CO2 trap-night, week 32 | 99.0 | 99.03 (CXTA 2,857 + CXPI 114 over 30 OK trap-nights), sqlite catches/trap_nights | yes |
| South Prairie same | 143.0 | 143.04 (24 trap-nights) | yes |
| Westbrook CXTA pools positive | 42 of 70, 23.7 per 1,000 (MIR 14.7) | 42 of 70, 23.7 | yes |
| Westbrook estimate | 2.3 | 2.3275 | yes |
| South Prairie estimate | 1.8 | 1.8112 | yes |
| Break-even rate | 18 per 1,000 | 18.3 (current Westbrook 23.5) | yes |
| Robustness (single Culex rate; Firth) | same figures | 2.31/1.81; 2.26/1.79 | yes |
| Human cases NB/MR/WB/OT/RS/SP/CH/AE | 3/2/2/2/3/4/7/2 | same (register Zone sections sheet; 8 of 37 log rows stale) | yes |
| CO2 trap-nights run, same zone order | 256/252/319/215/211/251/188/186 | same, count once | yes |
| CO2 trap-nights lost, same zone order | 6/5/9/3/6/11/7/10 | same (FAN, CO2, BAT, STOLEN; NS excluded) | yes |
| County PDF pools | 1,155 | 1,155, zero mismatches to the database; 4 Table 2 retests override | yes |

## Competing answers that survived
None on the main call. Competing readings of the main call are closed by the filing ("per CO2 trap-night", protocol 3.2 and 4.1) and are reproduced as the stump's wrong answers: positive pools over mosquitoes tested across all pools gives Riverside South, the likelihood estimate across all pools gives Old Town, and positive pools over mosquitoes tested across CO2 pools gives South Prairie (1.70 against 1.47). The only trap-night alternative is the as-entered column (NB 279/7, MR 270/7, WB 348/10, OT 234/4, RS 229/8, SP 273/13, CH 205/8, AE 203/11), which the schedule rules 3.3 and 3.5 exclude.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 6 (sqlite, pdf, xlsx, csv, geojson, txt) | yes |
| Large file | 25,000 rows or a large database | sqlite, 5.3 MB, catches 57,074 and pools 35,573 | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | 3 named (weather, dead birds, aerial applications); no file name labels one | yes |
| Distractors relevant but unused | unused by the solution, weigh, ruled out by a shipped fact | none feeds a graded figure. The thread did not name any as carrying the call. I did not test whether each distractor could answer a graded quantity. | yes (see Findings 3) |
| Deliverables | 1 to 3, all in the golden, no format family required | 3 (pdf, xlsx, png), all present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 8 zones per ask; whole counts, one decimal and nearest whole number stated in the prompt | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 01; the design note counts 36. I did not generate the rubric. | yes (design note) |
| Reads as real | no LLM tells; goldens read as work products | thread's hygiene review found no authoring or provenance leakage. I did not review the golden files' look. | yes |

## Gate G reconciliation
Thread: mechanism method_selection, stumping_family method_selection, surface_read_dependency no, sole_data_defect no. Card: gate_g `method_or_model_selection`, stump_strategy `composition_mix`, layer2_family `estimation_fit`, stump_class `analytical`. Design note: the default path ends on Riverside South and the golden is Westbrook through maximum likelihood on CO2 pools only. These match. The declared distractors (weather, dead birds, aerial history) were not named as the surface read carrying the task, and no shipped artifact ranks the zones on the decision question wrongly. Gate G: pass, no finding.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical. Card analyst_test and domain_test, and the design note's `## Three rules` (No decoy, Not semantics, Not rule application): the analyst who reads every field correctly files Riverside South (maximum likelihood alone Old Town, CO2 pools alone South Prairie, both together Westbrook). They agree. The 22 June load, the stale zone column, the unkeyed county PDF and pools of 50 against 10 sit in Layer 1 and do not decide the call.

## Stump power (Gate F)
Moderate to high. The common minimum infection rate on CO2 pools files South Prairie, and on all pools files Riverside South. Only the pool-size-aware likelihood on CO2 pools gives Westbrook. The asks (cases by corrected zone, trap-nights by status with the copies counted once) carry their own devices.

## Findings, ranked
1. None blocking.
2. Minor, design note only: its fork table cites protocol "3.2" for the trap-night definition (SF3) and "5.3" for the retest rule (SF4). The shipped protocol numbers are 3.4 and 4.3, which the submission cites correctly. Correct in the next edit of the note; no effect on the pack.
3. Optional: the estimator is unnamed in the shipped text (see Why). I did not test each declared distractor against the graded quantities, so rely on the thread's no-finding.

## Next action for the author
Nothing for determinism: proceed to `/approve task188`. Optionally fix the two protocol section numbers in DESIGN_NOTE.md SF3 and SF4.

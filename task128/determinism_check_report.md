# determinism-check report, task128, 2026-10-12

Scope: the thread judged the build whose CP-14 line was 700 rolls ($1,183,000 over $1,690). The verdict below is recorded as given on that build. Later fixes are listed under "Next action for the author".

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (no change required by the judge; its two optional notes were applied afterwards)
**Stumping type:** mechanism: method_or_model_selection (causal identification from an unfinished-list natural experiment) with binding_constraint (400 dials a day), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every committed answer reproduced from the shipped files. On the 24 unfinished lists per centre (cycles 04 and 13), the roll-rate difference between unreached and reached records, scaled by the diallable share, gives an effect per dial. CP-14 6.4 and budget line C-01 cap the new team at 400 dials a day. The result is 500 / 200 / 200 / 100 / 100 rolls (London, Kingston, Winnipeg, Sudbury, Thunder Bay) against the policy line. Six estimator variants all round to the same hundreds. The only routes that fund London are called against uncalled, pooled, skipped-records-set-aside, and uncapped dials, and the files rule each out. No gate failed.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| London rolls | 500 | 494.7 (5.15 per 100 dials, 9,600 dials) | yes |
| Kingston rolls | 200 | 203.8 | yes |
| Winnipeg rolls | 200 | 204.0 | yes |
| Sudbury rolls | 100 | 103.2 | yes |
| Thunder Bay rolls | 100 | 98.6 | yes |
| London dials | 9,600 (cap binds on all 24 days) | 689 to 1,096 diallable left per day | yes |
| Contacts per 100 dialled (LON/KGN/WPG/SUD/TBY) | 49.3 / 57.2 / 52.8 / 54.6 / 50.4 | same | yes |
| Promises per 100 contacts | 37.6 / 39.1 / 40.3 / 36.4 / 41.2 | same | yes |
| Arrangement balances, CAD | 15.5M / 14.3M / 16.0M / 10.1M / 7.0M | same | yes |
| Below the line, London 200 short | yes | yes | yes (the line figure moved after the pass, see Next action) |

## Competing answers that survived
None survived for any committed answer. The judge listed these wrong-method routes, and the files rule out each:

| Route | London rolls | Closed by |
|---|---|---|
| Called against uncalled | about 2,470 | holds, skips and campaign days in the uncalled; protocol and result codes |
| Pooled year | about 2,150 | campaign cycles' records against other days |
| Skipped set aside | about 990 | undiallable share left unmarked below the line |
| Uncapped dials | 1,114 | CP-14 6.4 and C-01 (400 a day) |

Two further traps, both closed by the files:
- No availability limit would put Kingston at 533, above London.
- Counting undiallable records as dials would put Winnipeg at 254, rounding to 300. The protocol says DNC and NDN records are not dialled.

The window in CP-14 6.2 (Aug 2025 to Jul 2026) differs from the prompt's window, but every rounded figure is identical under it.

The code-table risk on the contacts and promises columns is the Ask A device. The Field Reference lists AR as an answering machine, and a hyper-literal reader gets London 46.0 and 40.3. Call detail and DIALLER_VER settle it, so it is discoverable and not an open fork.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | csv, parquet, xlsx, docx, pdf (5 distinct; metadata.json lists these five) | yes |
| Largest file | 25,000 or more rows | 1,063,574 rows (card delinquency parquet); dialler list csv 362,358 | yes |
| Distractors | 2 or more, in metadata.json, none named in a file | LS60_DAILY_LIST_SUMMARY and Collections_Workforce_Headcount; neither is labelled in any file name; judge found both relevant and unused | yes |
| Distractor does not answer the question | not the stump | the judge did not name either as the surface read (surface_read_dependency: no) | yes |
| Deliverables | 1 to 3 | 3 (csv, png, docx) | yes |
| Deliverables present | all named | the three goldens are in the submission's Deliverable Answers; files not opened by me | yes (by submission) |
| Multi-dimensional asks | yes | five centres by five figures, chart, decision with gap | yes |
| Units and rounding in the asking sentence | stated | nearest 100, one decimal, nearest $100,000, Canadian dollars | yes |
| Prompt | one paragraph, under 1,000 characters | 852 characters, question first | yes |
| Prompt shape and 25 criteria | shape identifiable, 25 or more | shape 01 (ranked list under a cap); 25 gradable figures (5 centres by 5 columns) plus the chart and the decision, so the floor is plausibly met. The rubric is generated downstream, so I cannot count it here. | yes (unverified count) |
| Realism | nothing LLM generated | judge saw no tool banners, authoring language or tracked changes; plausible metadata; pod merge and code changes read as real | yes |

## Gate G reconciliation
- **Judge:** method_or_model_selection with binding_constraint, analytical_non_defect, surface_read_dependency no, sole_data_defect no. On clean data the task still needs the load-order identification and the capacity cap, so it passes Gate G.
- **Card and design note:** stump_strategy causal_design, `layer2_family` estimand_identification, `gate_g` signal_vs_noise_or_hold, `stump_class` analytical, `decisive_rule_filed` false, `official_decoy` false. The design note names the decisive rung as keeping the skipped records on the reached side, the same list day, and the 400-dial cap.
- **Result:** the labels differ but the substance agrees. Both name an analytical identification step plus a capacity cap, with no planted defect, decoy or filed rule. No mismatch predicting a send-back.
- **Ladder:** the judge's wrong routes track the design note's ladder.

| Route | Judge | Design note |
|---|---|---|
| Called against uncalled | about 2,470 | R0 2,315 |
| Skipped set aside | about 990 | R2 981 |
| Uncapped | 1,114 | R4 1,114 |
| Pooled | about 2,150 | R3 1,830 (a differently defined pooled form) |

Both agree every wrong route funds London.

## Gate H reconciliation
- **Judge:** domain pass, layers pass, decisive_step analytical.
- **Card:** `domain_test` is collections strategy judged on incremental cures against a counterfactual. `analyst_test` is that a strong analyst who found the overflow and set the skipped records aside still gets about 981.
- **Result:** match. The judge's easy route (called against uncalled) is the design's R0, and the design's analyst-test failure (R2 at 981) is a failure the judge also confirmed. No distractor carries the task.

## Stump power (Gate F)
Good per the judge. Four routes fund London at 1.4 times the line or more. Only the load-order natural experiment, the diallable-share scaling and the 400-a-day sizing return C-01. The AR code change and VUSD conversion add independent traps on the asks. Sampling noise on London is about 75 rolls, but rounded figures are stable across estimators, so the margin is not fragile. The gap of 200 against estimator spread of about 30 is wide. Too-easy signals named: none.

## Findings, ranked
1. None blocking.
2. Ask A code-table risk (AR in the Field Reference): intended D2 device, discoverable from call detail and DIALLER_VER. It is a data_semantics device on an ask, which the spec permits. Optional hint: listing AM in the Field Reference's code table.
3. Temporal coherence (judge note, since fixed): the CP-14 date preceded the 2027 budget filing, and the budget note's Kingston pilot date conflicted with the dialler log.
4. Sampling noise on London (about 75 rolls) is a point estimate, not margin fragility.

## Next action for the author
One step: make sure `submission.md` and the goldens agree with the post-judge pack. The judge saw the 700-roll line; the pack now says 694.

Applied after the thread was spawned (not judged):
- Loss per roll is now $1,705 and the CP-14 line 694 rolls (693.8 rounded up). No centre's rounded rolls or gap moved.
- The field reference no longer lists CAMPAIGN_ID under the list export.
- The register's history scope note was reworded.
- The CP-14 footer and register now date the 2027 line in 6.5 to 6 October 2026, after the 30 September budget filing.
- The budget note now reads "Kingston's CX2.1 pacing study in March 2026".

What to check:
- `submission.md` now reads 694 throughout (confirmed on disk). Confirm the other goldens (the PNG line label and the docx) also read 694, and that "200 short" still holds at the nearest 100 (500 against 694).
- Rebuild once and confirm the bundle and `target.zip` match the fixed pack.
- No re-judge is needed unless a rounded figure moved. The coordinator reports that none did.

# determinism-check report, task155 (pass 3), 2026-10-31

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Isolated thread run once from /tmp/determinism-check-task155-pass3/judge_brief.md (spawned by the main session); verdict at /tmp/determinism-check-task155-pass3/verdict.md. Inputs: prompt.txt (not legacy), target.zip, submission.md.

## Why
Crew hours reproduce exactly (Camberwell open lines 215, 1,092.5 paid hours, rounds to 1,090). The placement follows from the placement standard s3/s4 run through wp05_casual_callin_procedure.pdf with the acceptance model the offer log supports (carry-on term plus own/sister-store term). Surface read (most open hours) and a no-carry-on model give Werribee; the full model gives Camberwell. Both tables reproduce exactly. The reship (describing files removed, rules moved into the procedure) left every graded figure intact.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Open paid hours W / BH / Alt / Cam | 3,250 / 2,600 / 1,770 / 1,090 | 3,254 / 2,602 / 1,770 / 1,092.5 | yes (rounded) |
| Table 1 put out, covered, uncovered (24 cells) | per submission | identical, all 8 stores | yes, exact |
| Table 2 (16 cells) | per submission | identical | yes, exact |
| CC1 carry-on offers accepted | 32% (2,241) vs 4% (153,829) | 31.8% (2,190) vs 3.9% (153,880); 29.4% (2,480) if bookings counted | approximate, not decision-relevant |
| CC2 carry-on share of open shifts | W 100, BH 96, Alt 79, Cam 0 | plain adjacency W 100, BH 100, Alt 85, Cam 12.6 | not exact (needs the eligibility checks); not decision-relevant |
| Forecast order | Camberwell first | Cam 515-525 vs Sunshine 419-441 vs Werribee 118-160 (full model) | yes |

## Competing answers that survived
- Sunshine, if the own-versus-sister-store acceptance term is omitted (carry-on only: 322 vs 357). The data separates it (about 4% own vs 1.4% sister, n=16,314), so the full model is the forced one, but it is a method-selection dependence, not a pinned rule.
- Werribee, if carry-on is omitted or a flat fill rate is used (the intended easy route).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000 rows | 14 / 4 (csv, json, xlsx, pdf) / 156,070 rows | yes |
| Distractors in metadata.json, none named by file | 2+ | trading plan, school terms and holidays; names unlabelled | yes |
| Distractors unused yet weighable | yes | neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (pdf, xlsx), both present | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 24 + 16 cells, prompt states rounding | yes |
| Prompt shape, rubric 25+ | yes | shape 09 funnel; 40 table cells plus call and chart | yes |
| Prompt | one paragraph, under 1,000 chars | 890 chars | yes |
| No LLM tell, goldens real | yes | thread found none; golden-realism done at build | yes |

## Gate G reconciliation
Thread: mechanism forecasting, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: gap time with population, pattern E, Gate G forecasting, stump_class analytical, the default path ends on Werribee. Match. The declared distractors (trading plan, school terms) are not the surface read; the surface read is the open-hours ranking, which is the default path, not a shipped wrong ranking.
Gate H: domain pass, layers pass, decisive_step analytical (a fitted discrete-choice model simulated through the call-in procedure). Matches the note's Three rules (field_method, labour-supply choice with a fixed trip cost; not semantics; not rule application).

## Stump power (Gate F)
Good. Flat fill rate or most open hours gives Werribee; carry-on only gives Sunshine; only the full fitted model through the procedure gives Camberwell. Not a standard-method landable call. The Camberwell margin over Sunshine is about 16% in the judge's replication, thinner than the note's golden (630 vs 440).

## Findings, ranked
1. Watch: Camberwell vs Sunshine depends on including the own/sister-store term; margin about 85 hours in the judge's replication.
2. Minor: Critical components 1 and 2 do not reproduce exactly (2,241/153,829 counts; 96%/79%/0% rely on the procedure's eligibility checks). Submission step 2 and CC2 still say "the module's checks" while the module notes file is gone; re-word to the procedure and give the definition used. Does not affect any graded figure.
3. Minor: the note's Default path still cites the retired module notes; no ship impact.

## Next action for the author
Proceed to ship. Optionally re-word CC1 and CC2 in submission.md with exact counts and the procedure's eligibility definition (no rebuild needed).

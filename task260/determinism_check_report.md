# determinism-check report, task260, 2026-11-02

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (MRMC random-effects inference), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The protocol (ai_evaluation_protocol_v2.pdf, s3 and s4) fixes the gain as the panel's mean empirical AUC, tool minus unaided, and the qualifying test as a two-sided 95 per cent interval wholly above zero for the service's film readers reading its screening examinations. With readers and examinations both random, Halvic Breast is the only qualifier, under every estimator tried (OR with jackknife or DeLong covariances, DBM, stratified and unstratified two-way bootstrap). Quotes, RIS, mobile-visit and HR files force the numeric asks. The judge thread's verdict is at /tmp/determinism-check-task260-r1/verdict.md (one pass, one thread, sonnet, medium).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Gain Lumidra | 0.047 | 0.0472, interval [-0.0148, 0.1092] | yes |
| Gain Ondrix | 0.042 | 0.0420, [-0.0129, 0.0969]; 3 of 10 readers worse | yes |
| Gain Halvic | 0.026 | 0.0259, [0.0136, 0.0383] | yes |
| Sites CRB / WDL / CPL / TLW | 11,569 / 7,298 / 13,253 / 13,758 | same (45,878 total) | yes |
| Film readers 1 Apr 2027 | 27 | 28 rows less one duplicated registration = 27 | yes |
| Lumidra cost | 110,745 | 44,262 x 2.08 + 27 x 340 + 9,500 = 110,744.96 | yes |
| Ondrix cost | 89,122 | 45,878 x 1.62 + 14,800 = 89,122.36 | yes |
| Halvic cost | 101,750 | 27 x 2,450 + 4 x 5,900 + 12,000 | yes |

## Competing answers that survived
None changes the main call; each is data-supported toward the golden.
1. Legacy-record dedup (MW/LR, offset 0 or 60 min, 24 Mar to 15 May 2026): rule not stated in a document, inferred from a clean 639 of 639 one-to-one match with a BST signature. A cruder one-per-woman-site-code-day rule gives 45,252 and other site totals. Layer 1.
2. Lumidra episodes: 124 women with two MAMS 4 to 28 days apart; one per woman gives 44,262, a patient-day count gives 44,386 (cost 111,003). Round length is only implicitly supported (protocol 36-month interval). Affects the Lumidra cost only.
3. Roberts starts 1 April 2027: counted in (27); excluded gives 26. Reader-seat wording supports inclusion.
4. Mobile host: screening_locations.json host_site at export gives the wrong split (CRB 6,417, WDL 12,450); the dated visit ranges close it.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000 rows | 17 / 4 (csv, xlsx, pdf, json) / RIS 55,920 rows | yes |
| Distractors | 2+ in metadata.json, none labelled by file name | 3 named (vendor summaries, KPI xlsx, self-assessment csv) | yes |
| Distractor unused, weighs, ruled out by a shipped fact | yes | vendor standalone AUC (Halvic lowest) is declared wrong-basis, ruled out by protocol 3.1 and 3.2 | yes |
| Deliverables | 1 to 3, all in golden | 3 (pdf, xlsx, png), all present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per-tool gain/gate/why/cost, four sites, reader count; units and rounding in the prompt | yes |
| Prompt shape, 25+ criteria | shape identifiable | shape 01 per design note; criteria count taken from the design note, not recounted here | yes (note) |
| Not LLM-reading, goldens business-real | yes | judge found plausible operational artifacts, no authoring disclosures | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: the stump is the interval built with both readers and examinations random; default path is the fixed-panel case bootstrap (files Ondrix) or reader paired t-test (files Lumidra); declared distractor is the vendor standalone-AUC summary. Match. The thread did not name the distractor as the surface read carrying the task (the largest raw gain, Lumidra, is the naive pick, not the distractor). Gate G: pass.

## Gate H
domain: pass, layers: pass (Layer 1: ReadPoint layout change and last-submission rule, legacy vs new RIS with BST offset, mobile host change in year, HR registration formats; Layer 2: MRMC OR/DBM inference), decisive_step: analytical. Matches the design note's `## Three rules` (No decoy, Not semantics, Not rule application).

## Stump power (Gate F)
Moderate to high. MRMC OR/DBM is the field's standard route, so a strong solver who reads protocol 4.1's population sentence takes it on sight; the design note itself names this loudness as the risk (the ruling-out is one sentence). The thread's own account is that the easy routes (largest gain, reader-only paired test, fixed-reader or fixed-case interval) file Lumidra or Ondrix, so the call is not landed by reading alone. The main thread should weigh this against the ladder (textbook method, `stumping` 1.3). The asks carry independent stumps (mobile host by date, legacy dedup, episode definition, registration dedup).

## Findings, ranked
1. Fork 2 (Lumidra episode count) rests on an implicit round length; affects one cost figure only. Optional: file the round length in the quote or protocol (changes the pack, so a rebuild).
2. Fork 1 (legacy dedup rule unstated but inferable): Layer 1, closed by the data.
3. Stump loudness of protocol 4.1 (design-note risk, not a determinism defect).

## Next action for the author
None required for determinism; proceed to ship. Optionally close fork 2 by filing the screening round length.

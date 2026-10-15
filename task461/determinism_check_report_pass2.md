# determinism-check report (pass 2), task461, 2026-10-15

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The call is the lowest menu setting whose expected 2027 cycling days stay within 300. The node's 11 months of own prices are a windy, low-spread stretch; its daily spread tracks the 8-year hub record at a stable ratio (2.21). Extending the node over the hub's 2,863 days gives 275 days at $20 and 323 at $15. Every pooled estimator tried gives $20; only the node's own single year moves the call ($15). The pass-1 rounding fork is closed: the net per cycle is $31,342 on every path ($31,341.80 unrounded, $31,342 from rounded inputs).
Verdict file: /tmp/determinism-check-task461-1792076016/verdict.md (one isolated sonnet thread, medium effort, scratch folder only).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Hub days / node days | 2,863 / 336 | 2,863 / 336 | yes |
| Hub-priced first node days | 13 | 13 (max diff 0.0) | yes |
| Ratio over 323 days | 2.21 | 2.2097 | yes |
| Expected days $5..$40 | 365/355/323/275/224/176/138/113 | same | yes |
| Full Cycles Jan..Oct | 7.95, 2.98, 4.98, 5.99, 9.01, 11.03, 18.05, 14.02, 11.01, 2.99; 88.00 | 88.0006 total, months match | yes |
| Monthly net $k | 268.9 ... 63.5; 2,758.1 | 2,758.096 | yes |
| Net per cycle | $31,342 | $31,341.80 unrounded | yes |
| CSV rows | 3,199 | 3,199 | yes |

## Competing answers that survived
- Fork 1 (optional pin): the prompt says only "expected 2027 cycling days" and does not file the population (the price years in the extracts). Reading it as "2027 repeats the node's own 2026" gives $15 (270 days). The judge does not credit it as defensible: 2026 is an outlier among eight hub years (209 days at $20 against 222 to 300) and the node record is 11 months. Closing sentence is the design note's SF3 (365 times the share of the record's days at or above the setting) and the stump itself, so this is the intended stump, not a defect; note that CLAUDE.md files the WHAT (population) and not the HOW, and the prompt could add "expected over the price years in our extracts" if the author wants it closed. Not required.
- Minor, none decisive: node label in the CSV (old name separate gives the same 3,199 rows); chart reference line (flat 300 or pace line); operating month versus statement month for nets.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 13 | yes |
| Formats | 3+ | csv, pdf, xlsx | yes |
| Large file | 25,000+ rows | 68,712 (hub), others over 25,000 | yes |
| Distractors named in metadata.json | 2+, no file name labels one | RTM hub prices, ancillary clearing prices; names are neutral | yes |
| Distractors unused yet weighable | yes | unused by solution, relevant (judge confirmed) | yes |
| Deliverables | 1 to 3 | 2 | yes |
| Asks with unit and rounding | yes | stated in the prompt for each | yes |
| Prompt shape, 25+ criteria | identifiable, 25+ | shape 04; asks give 8 + 10 + 10 + net + chart + CSV, reaches 25+ by count | yes (portal rubric not seen) |
| Not LLM-reading | yes | judge found no authoring language | yes |

## Gate G reconciliation
Thread: mechanism forecasting, family analytical_non_defect, surface_read no, sole_data_defect no. Design note and card (read after the thread returned): the stump is the extension of the short node record through the overlap, with the node's own record giving $15, the hub's alone $10 and the hub plus premium $30; the declared distractors are the RTM and ancillary files and the thread names neither as carrying the call. Matches; no mismatch finding.
Gate H: domain pass, layers pass, decisive_step analytical (data-integration estimate of the short record over the long one; not plant, not semantics, not rule application). Matches the note's `## Three rules`.

## Stump power (Gate F)
Plausibly stumps a strong model: the cleaned-but-naive routes file $15 (node's own days) or $10 (raw hub). No document announces the extension. Weaker point: the back-test advantage of the pooled estimator is slim (RMSE 36.0 against 43.8 at $20), margins are 25 and 23 days with a pooled standard error near 11 days. Empirical rate is for the portal.

## Findings, ranked
1. Optional: population of "expected 2027 cycling days" is not filed in the prompt (fork 1); needs a rerun if pinned.
2. Minor presentation forks (CSV label, chart reference line, month keying); not gradable or not decisive.

## Next action for the author
Proceed to ship; optionally pin the population in the prompt only if you accept a rerun.

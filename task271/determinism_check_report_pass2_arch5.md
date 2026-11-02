# determinism-check report, task271, pass 2, 2026-10-27

Pack judged: target.zip d6135883 (the unzip the thread read). The main session then fixed two realism items a leak reader found (trading calendar closing Friday 1 January 2027; the dealing plan's cut-off table moved under its section 2). Neither enters a graded computation; the current target.zip is 7718f1c7 and was not re-judged. Verdict recorded on d6135883.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_selection (which fills represent the platform's orders; own-impact contamination of the 60 s mid), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The thread reproduced every graded figure from the bundle. Four venues are above 1.5 bp on the 69,118 fills with no other desk execution in the same share in the following 60 s: Delvenne lit 2.18, Ardenwick mid 3.01, Thursgate mid 1.89, Quintrell SI 2.23. Every clean-forward-window variant it tried (same-order only, any desk fill, plus or minus 60 s, 30 s, 120 s, 300 s, share-weighted) returns the same list. The pass 1 FIX_NOW is closed: "by trade date" in the prompt makes the order-level, part-level, first-date and last-date readings of Ask A, and the trade-month reading of Ask B, give identical results at the stated rounding.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Fills after dedup, busts, auction out | 171,750 | 171,750 (172,417 rows, 444 busts, 223 auction) | yes |
| Isolated fills | 69,118 | 69,118 (69,116 if busted neighbours ignored, same list) | yes |
| Wexcombe / Ardenwick lit / Delvenne lit / Ardenwick mid | 0 / 1 / 2 / 3 | 0.079 / 0.922 / 2.184 / 3.012 | yes |
| Delvenne Midpoint / Thursgate mid / Brindock SI / Quintrell SI | 1 / 2 / 0 / 2 | 0.956 / 1.889 / 0.225 / 2.234 | yes |
| Ask 4 09:30 / 12:00 / 14:30 | 0.169 / 0.119 / 0.112 | 0.1689 / 0.1185 / 0.1118 | yes |
| Ask 5 Jan to Oct | 4.72, 4.40, 5.05, 3.71, 4.31, 3.13, 4.65, 4.23, 3.18, 3.87 | 4.716, 4.399, 5.046, 3.706, 4.315, 3.129, 4.648, 4.228, 3.182, 3.874 | yes |
| Naive all-fills route | two venues | DLVL 1.67, QTSI 1.73 only | yes |

## Competing answers that survived
- Last fill of each order only (4,894 fills): adds Delvenne Midpoint at 1.62 (n=211, SE 0.39) and moves Delvenne lit to 3. Thread rates it weak: a 7 percent subset with an error band straddling the line, and it discards clean fills the 60 s policy horizon admits. Residual risk, not disqualifying.
- London-time reading of `placed_at` (Ask 4 becomes 0.172, 0.115, 0.109): rejected by two data signals (Gresmere's cut-off boundaries in the notes shift with the clock change; order-arrival hours shift after March), but not documented anywhere. Data-pinned, and an ask-side device by design.
- Two items from the design note the thread did not list: Gresmere's ten-minutes-before-a-point cut-off in its trade times gives 12:00 = 0.117 if read from the notes rather than the plan's 15-minute cut-offs; the plan's stated cut-offs are the literal rule, so this is not an open fork.
- Consideration-based Ask 5, cancelled notes kept, June reissues kept: all rejected by shipped text or fields.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | csv, pdf, xlsx, json | yes |
| Large file | 25,000 rows or more | 172,960 (also 106,299, 104,523, 90,015, 82,846, 25,320) | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | wexcombe_closing_auction_statistics_2026.csv, venue_volume_report_2025.pdf; no file name says distractor | yes |
| Distractor relevance | unused, weighable, ruled out by shipped fact | auction stats and 2025 volume report; neither answers a graded quantity (volume shares, no adverse moves) | yes |
| Deliverables | 1 to 3, all in golden | 2 (PDF board paper, xlsx workbook); both answered in submission.md | yes |
| Asks | multi-dimensional, unit and rounding stated | 8 venues, 3 points, 10 months; whole bp, three decimals per cent, GBP million two decimals in the prompt | yes |
| Prompt | one paragraph, under 1,000 chars | 978 chars | yes |
| Rubric 25 or more criteria | 25 | not countable from the pack; 4 components + 21 ask figures + 3 chart/list items reach it on the shape (8-venue scorecard, 3 sizes, 10 months) | yes (inferred) |
| LLM-generated tells | none | thread found none; names and tickers were replaced for realism since pass 1 | yes |

## Gate G reconciliation
Thread: method_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: decomposition_attribution under causal_design, analytical, wrong basis is the desk's own following trades; Gate G exception only the declared distractors. The labels differ in wording but name the same step (which fills represent the platform's orders). The thread did not name a declared distractor as the surface read; the distractors are not load-bearing. No mismatch.

Gate H: thread domain pass, layers pass, decisive_step analytical. Design note `## Three rules` agrees (decisive step: lone-fill read net of the desk's own following trades). The thread did not class the step analytical merely because the golden is a field-standard method; it cited the all-fills route a capable model takes returning two venues.

## Stump power (Gate F)
Strong on paper. The easy route (average every 2026 fill) names two venues and passes both midpoint books (0.48, -0.44); other routes (1 s, 5 s markouts, DMA single orders, parent fixed effects) name 0 to 2 venues. The correct filter comes from policy 4.3's counterfactual wording and the plan's one-execution statement, not a filed rule. Asks run through silent devices (UTC clock, ADV consolidation, stamp duty in consideration), so a careful solver misses the same figures. Measured stump power is the portal's.

## Findings, ranked
1. (Low) `placed_at` carries no time-zone label; data-pinned to UTC. Design keeps it as a silent ask device; the thread advises against labelling it.
2. (Low) Last-fill-only fork puts Delvenne Midpoint at 1.62 on 211 fills; recorded in the design note's RECORD rows, not built for.
3. (Info) The two post-judge realism edits (calendar New Year's Day, cut-off table placement) are outside the graded computations; the thread did not see them.

## Next action for the author
Ship. The determinism judge returns APPROVE; carry on to stage 5 with target.zip 7718f1c7 and the free gates already re-run green.

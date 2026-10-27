# determinism-check report, task271, 2026-10-27

Pack read by the thread: target.zip 93bbb64c. Since then the main session replaced the securities master's share names and tickers (a realism fix, no figure moved) and is pinning the trade date in the prompt per the FIX_NOW. This verdict is on the pack the thread read. The thread's raw verdict is /tmp/determinism-check-task271-r1/verdict.md.

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (prompt pin only; no re-judge of the stump needed, main call and graded figures unchanged)
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The deciding fact is dealing plan 4 ("each is filled in one execution"), read with policy 4.3 (the fills the flow's orders would receive) and 4.4 (busts and the closing auction out). Every defensible way of keeping fills with no own follow-on desk execution in the share within 60 s gives the same four venues off: Delvenne lit, Ardenwick mid, Thursgate mid, Quintrell SI (1.88 to 3.01 bp against 1.5; the four kept on are at or below 0.96 bp). Thresholds from 30 s to 300 s, value weighting, any month, broker, side or time slice, and the added "none in the prior minute" filter all agree. All 34 graded figures reproduce. The only open point is the prompt's silence on which date defines "dealt in 2026" and the months (trade vs settlement).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Fills after dedupe, busts, auction out | 171,750 | 171,750 | yes |
| Fills with no later desk execution within 60 s | 69,118 | 69,118 (69,237 if busted prints are not counted as executions) | yes; rounded venue figures identical either way |
| Wexcombe / Ardenwick lit / Delvenne lit / Ardenwick mid | 0 / 1 / 2 / 3 | 0.079 / 0.922 / 2.184 / 3.012 | yes |
| Delvenne Midpoint / Thursgate mid / Brindock / Quintrell | 1 / 2 / 0 / 2 | 0.956 / 1.889 / 0.225 / 2.234 | yes |
| Mean market-order size 09:30 / 12:00 / 14:30 | 0.169 / 0.119 / 0.112 | 0.16887 / 0.11854 / 0.11157 | yes (12:00 is 0.00004 above the rounding line, stable under every dedupe variant) |
| Market-order counts | 18,135 / 9,949 / 8,924 | same | yes |
| Net purchases Jan to Oct, GBP m | 4.72, 4.40, 5.05, 3.71, 4.31, 3.13, 4.65, 4.23, 3.18, 3.87 | 4.7164, 4.3986, 5.0464, 3.7057, 4.3145, 3.1288, 4.6485, 4.2278, 3.1824, 3.8735 | yes, all ten |

## Competing answers that survived
- Settlement-month reading of ask 5 (4.57, 4.11, 4.94, 4.15, 4.07, 3.21, 4.75, 4.04, 3.38, 3.96, plus 0.21 from December trades); including 30 and 31 Dec 2025 trades moves the 12:00 mean to 0.118. The notes file name says "settling", the prompt does not pin the date. Closing rule: none shipped; prompt pin required (trade date, 1 Jan to 30 Oct).
- Main call: none survived. Last-fill-of-each-order-only (4,894 fills) adds Delvenne Midpoint at 1.616 (n=211, se 0.39); the thread judged it unreasonable (discards 93% of the equally clean fills) and did not accept it as a surviving answer. Noted as the one reading to watch.
- Not forks: all-fills average (DLVL 1.67, QTSI 1.73 only) is the intended trap; the 2026 single orders only reading cannot answer all eight venues (no single order used the midpoint books).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | 4 (csv 8, pdf 4, xlsx 2, json 1) | yes |
| Large file | 25,000 rows or more | hessenby 172,960 (also ashlowe, pemberwick, gresmere notes, client orders, closing auction above 25,000) | yes |
| Distractors | 2 or more in metadata.json, none named by file name | wexcombe_closing_auction_statistics_2026.csv, venue_volume_report_2025.pdf; neither name labels a distractor | yes |
| Distractors relevant, unused, ruled out | one answering a graded quantity must reproduce arithmetically | the volume report gives volume shares only, the auction file is used only for the ADV unit check; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden, no format family | 2 (PDF, XLSX), both in task271/golden | yes |
| Asks | multi-dimensional, unit and rounding stated | 3 dealing points and 10 months; bp, per cent to 3 dp, GBP m to 2 dp all stated | yes (the date basis is not, see Findings 1) |
| Prompt shape, rubric 25 or more | identifiable shape and 25 criteria | shape 10 scorecard (metadata); eight venues, 3 points, 10 months, recommendation and components give well over 25 gradable items; the rubric itself is generated and not inspected here | yes (inferred) |
| Not LLM generated, goldens read real | no tells | thread found no authoring language in the PDFs; the leak reader's note on synthetic share names in the securities master has since been fixed by the main session (not re-read by me) | yes, pending the fixed master |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no.
Design note: Gate G strategy `decomposition_attribution`/`causal_design`, decisive step the counterparty part of each fill's markout net of the desk's own following trades; stump sentence names the same pooled-average route (Delvenne lit and Quintrell SI only) and the same fill population for the golden. Card: stump_class analytical, and its analyst_test names the same easy route and its 0.48 and -0.44 figures, which the thread reproduced exactly as AWKM 0.48 and THG -0.44.
Match. The thread did not name the declared distractors (2025 volume report, closing auction statistics) as the surface read carrying the task; the easy route is the solver's own pooled average of clean fills. The note's "Not semantics" and "Not rule application" lines agree with the thread's finding that no file names the method and the policy is silent on the desk's own trades.
Gate H: thread `domain: pass`, `layers: pass`, `decisive_step: analytical`. It matches the card's domain_test (markout/adverse selection separated from the desk's own impact) and the note's Layer 1/Layer 2 split.

## Stump power (Gate F)
Moderate to good, on paper. The pooled average misses Ardenwick mid and Thursgate mid by wide margins (0.48 and -0.44 against 3.01 and 1.89) and keeps off two venues, so a strong analyst who cleans correctly and reads every rule still files a wrong call by the easy route. Counterweight for the main thread: the pointers to the right population are the prompt phrase "as the platform's orders would meet it" and dealing plan 4 (platform orders filled in one execution); a strong solver reading the policy's 4.3 literally (the fills the platform's orders would receive) can land on the golden, as the leak reader did, and the thread judged the follow-on-contamination filter forced once that is read. The thread did not class the decisive step analytical on the grounds of a standard textbook method. The asks add real hazards (UTC to BST, cut-offs and calendar, consolidation by ten, system-migration twins, split parts, value basis). The main thread weighs this against the design note's ladder.

## Findings, ranked
1. Prompt (FIX_NOW, low): the workbook sentence does not say months and "dealt in 2026" run by Gresmere trade date, 1 January to 30 October. A settlement-month reader gets different figures for ask 5 (and 0.118 at 12:00 if December trades are included). The main session is already pinning the trade date; no stump or figure change.
2. Solution wording (cosmetic): step 4 should say the new system's twins of 29 and 30 June trades are matched by order and trade date, not by order (order WO20063619 has a genuine second part on 1 July; dropping by order wrongly gives July 4.66 and 14:30 0.111). Keep the parts that have no twin.
3. Solution wording (cosmetic): step 2 counts busted prints as "desk executions", as 69,118 requires; either state that or accept 69,237. No venue figure moves.
4. Watch item (no action): last-fill-of-each-order-only puts Delvenne Midpoint at 1.616 bp with se 0.39; not a reasonable reading but it is the one alternative that moves the list.

## Next action for the author
Pin the date basis in prompt.txt (gresmere trade date, 1 January to 30 October 2026) and tighten steps 2 and 4 of submission.md as above, rebuild once, then proceed to ship; no judge rerun is needed since the main call, the pack's figures and every graded value stay byte-identical.

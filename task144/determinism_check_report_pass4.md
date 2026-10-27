# determinism-check report, task144, 2026-10-27 (pass 4, run r4, pack 9126d810)

## Verdict
DETERMINISTIC (judged on Ask A; Ask B and the main call spot-checked only, no fork seen). No SOLUTION_WRONG.
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Run note: no Agent tool in the runtime, so the brief was written to /tmp/determinism-check-task144-r4/judge_brief.md and the main session spawned the one sonnet thread. Its verdict is /tmp/determinism-check-task144-r4/verdict.md. This report only records it.

## Why
The partial-gateway change is closed by the data. In Postwerk (April) 4,926 subscribers click all 9 links and 2,887 click exactly the 8 non-unsubscribe links; nobody sits in between, so both groups are fetches. In Relaymark the per-subscriber maximum of clicks in any 2 s window is 0 to 3 for humans and 9 to 11 for gateways, nothing in 4 to 8, so a 9-link burst without the unsubscribe link is as forced a fetch as a 10-link one. Reading the unsubscribe-spared subscribers as genuine clickers roughly doubles every count (April 9,482, 2.42%) and is not defensible. All six Ask A counts and shares reproduce.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Apr clickers / share | 6,699 / 1.71% (of 391,299) | same | yes |
| May | 7,031 / 1.76% (of 399,160) | same | yes |
| Jun | 7,169 / 1.76% (of 406,891) | same | yes |
| Jul | 7,395 / 1.72% (of 429,444) | same | yes |
| Aug | 7,090 / 1.65% (of 429,291) | same | yes |
| Sep | 7,317 / 1.70% (of 429,949) | same | yes |
| Ask B kilnkit, tracewire, shiftgres, ferrolog | 22/27, 43/47, 28/31, 30/37 | same (81.48, 91.49, 90.32, 81.08) | yes |
| Ask B hullcheck | 23 of 26 (88.46%) | judge's rough pass gave 12 of 14 without applying the imagelint alias | not reproduced by the thread; incomplete, not a disagreement |
| Main call (12,000 / 9,000 / slidewell 10,000) | spot-check not run | not rechecked | not tested this pass |

## Competing answers that survived
1. Residual, minor: fetch-affected subscribers who also made their own later or duplicate click on the spotlight link (104 in April, 108 in May in Postwerk; about 100 to 120 a month in Relaymark). Golden keeps them (leave out the fetch, keep the subscriber's own click). An analyst who drops the whole gateway subscriber files about 1.6 per cent lower (April 6,595, June 7,052). The golden is the literal reading of step 7 ("leaving out mail gateways' fetches") and of "subscribers who clicked through". The design note lists this route as a known wrong route (gateways' subscribers dropped, 0 of 12). It is still a reading the files only imply.
2. Minor: a 3-link threshold changes Jun to Sep by 1 to 4 each (7,168 / 7,392 / 7,087 / 7,313). Humans with exactly 3 links in 2 s exist (about 5 a month). 3 sits on the human side of the gap, so it is not a reasonable choice. The thresholds 4 to 9 give identical results.
3. Inferred, not read: the Thursday resend to non-openers is a subset of the list, so the denominator is the Tuesday delivered sum. The prompt's "delivered to" and the campaign files support it.
Closed: window edge (inclusive or strict, no change), id-form addresses (needed, Jun 6,248 without), seed/test sends ("[TEST]" label and seeds list), the Relaymark "spotlight" tag (points at the previous month's repository, the URL decides), denominator 394,936 vs Tuesday delivered, no fetch filtering (April 14,408).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | 5 (csv, json, parquet, pdf, xlsx) | yes |
| Large file | 25,000 or more rows | relaymark_link_clicks 489,415 rows | yes |
| Distractors | 2 or more in metadata.json, none named in a file name | repository_traffic and trending_daily; names are plain exports | yes |
| Distractors unused, relevant | weighable, ruled out by a shipped fact | rank nothing on stars; design note and judge found them unused by the solution | yes |
| Deliverables | 1 to 3, all in golden | xlsx and png, both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | issue sheet by 6 issues x count and share; nominator sheet by 5 repositories; unit and rounding in the prompt | yes |
| Prompt shape and rubric | identifiable, 25 or more criteria | shape `other`, design note counts about 39 criteria (3+7+5+22+2) | yes (by design note count) |
| Reads as real | no LLM tells | thread found none; exports read as system output | yes |
| Prompt length | under 1,000 characters | 996 | yes |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: gap-time mechanism on a forecast (rate window against the cascade window, backtested on the lottery), stump_class analytical. They agree. The thread did not name the declared distractors (traffic, trending) as the surface read carrying the task, so there is no too-load-bearing finding. The thread's picks for the easy routes (whole-life rate files slidewell at 14,000; lottery average lift files tracewire) match the note's analyst test.

## Stump power (Gate F)
Weighed on paper against the design note's ladder only (STOP block: no solver, reader or probe). The thread did not rerun the main call. Gate H line: domain pass, layers pass, decisive_step analytical (a per-view rate read from the 8th day public, chosen by out-of-sample reproduction of the 19 closed lottery spotlights). The note's `## Three rules` carries No decoy, Not semantics and Not rule application lines. The partial-gateway change touches only the ask path: the decisive step is not a standard textbook method applied without judgment, since the window has to be chosen against the lottery. Ask A devices (unsubscribe-spared fetches, id-form links, test sends) are ask-side, allowed to turn on semantics, and about 2x overcount if missed. The thread found them reachable from the data.

## Findings, ranked
1. Minor, optional: the surplus-click fork (competing answer 1). Not a FIX_NOW. The thread suggests an optional population phrase in Ask A ("excluding gateway fetches but keeping any further click of the subscriber's own"). This files the WHAT, not the HOW, and it must not state the 4-link threshold. It would change the prompt and so is the author's call; it needs a /fix-determinism pass if taken.
2. Minor: hullcheck Ask B not reproduced by the thread (incomplete, alias not applied). Not a finding against the golden.
3. Pass noted: the unsubscribe-spared reading is forced by two separated clusters in both platforms.

## Next action for the author
No FIX_NOW. Proceed to ship pack 9126d810. Optionally close finding 1 by one sentence in the Ask A wording via /fix-determinism, with the call, stump and graded figures frozen.

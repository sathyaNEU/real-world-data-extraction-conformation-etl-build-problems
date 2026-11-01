# determinism-check report, task197, 2026-11-01 (pass 2, reship after leak-gate repair)

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW as the thread wrote it; this report rules both conventions closed by convergence (C1), so the repair is optional and, for the meter stamps, barred by the reship brief. Net: no rerun and no filing required, residual reviewer risk recorded below.
**Stumping type:** mechanism: method_or_model_selection (counterfactual baseline estimation), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
Judge thread verdict: /tmp/determinism-check-task197-1793556507/verdict.md (one thread, one pass, brief at judge_brief.md in the same folder). Pack md5 aa74426a897dc2ec22ea9c3eb0fab3a3, 17 files, no data_dictionary.csv.

## Why
Applying the standard's definition with the programme baseline moving over a fixed per-site traverse reproduces Kampvliet 72 per cent (134 episodes), Reiderland 83 per cent, gap 11 points (10.7 unrounded), 3 sites under 90, and scorecard ask 1 in full. The setpoint baseline names Reiderland (57) and the undisturbed level names Zwartewater (76); the data (per-site traverse fits, spread within 2 s) choose the baseline. The two repair-side changes (no dictionary, no Notes sheet, E flag unwritten on two samples) move nothing graded: the thread reproduced 911 pairs and 134 and 152 counts with no extreme-second sample flagged E.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Kampvliet gain / episodes | 72 / 134 | 72.1 / 134 | yes |
| Reiderland gain, gap | 83, 11 | 82.8, 10.7 | yes |
| Sites under 90 | 3 | 3 | yes |
| Traverse KPV / TRB | 90 s / 300 s | 90 / 300 (archive DPDT at uncommitted boundaries) | yes |
| Site-episode pairs with extreme second | 911 | 911 | yes |
| Ask 1 all nine gains and counts | as submission | match | yes |
| Ask 2 over-frequency gains and counts | as submission | match only with event-log start_local read as UTC clock | yes under C1 |
| Ask 3 six blocks held/shortfall | 542.0/18.0 ... 244.2/7.8 | match under same reading; literal gives shortfalls 10.5, 14.2, 17.5, 4.7, 18.8, 6.5 | yes under C1 |
| Ask 4 portfolio 114.4 / 242.6 and nine rows | as submission | match with interval-ending stamps; as-given stamps give 944.5 / 1054.0 | yes under C1 |

## Competing answers that survived
1. Event-log start_local read at its written +02:00 (asks 2 and 3): over-frequency HGZ 86 (151), KPV 70 (21), OOS 90 (16), ZWT 93 (70); block shortfalls above. Closed by C1 (ruling A).
2. Meter stamps as given (ask 4): 944.5 / 1054.0. Closed by C1 (ruling B).
3. "Every unit below 90 per cent is withdrawn" (technical conditions clause 3): not a second figure (ruling C).
No competing answer survives on the main call or ask 1.

## Rulings requested
**A. Event-log start_local (asks 2, 3): C1, closed by convergence in the data, with residual risk.** Four witnesses converge on one reading: logged_utc less start_local is 1.5 min on 18 rows and 121.5 min on 9 when read at the stated offset, and 1.5 min on all 27 when the nine are read as the UTC clock; the archive's ALARM recordings (Terborgh 10-09, Kampvliet 10-03) sit at the clock-as-UTC times; the zero-response over-frequency episodes sit in those windows; and a 121.5 min logging lag is a value no producing system writes beside a 1.5 min one. The literal reading is contradicted by the file's own columns, so it is not a second supported figure. Weakness stated plainly: the design note's SF10 row says the event log's start field is a local column, so the label points the other way for those nine rows and no sentence resolves it. The closure is a cross-column cut (what D8 declares it to be), not a stated rule. A reviewer executing the label literally lands on the second figure set; I judge that reading unsupported, not a fork, but it is the item most likely to draw a Gate C comment. No filing is needed; none is advised.

**B. Meter stamps interval-ending (ask 4): C1.** The file itself carries the evidence: first ts 00:15 (labelled period 2), last 10-12 00:00, no 09-21 00:00 row (21 days x 96 rows are all present only if stamps close their interval), correlation with programme energy 0.9995 shifted against 0.96 unshifted. Only one reading uses every row of the file. This is an ask device (D6) and the reship brief forbids filing an ask's device in a document, so the optional clause the thread proposed is not to be added; convergence closes it. Same residual-risk note as A, smaller: a literal reader who never pairs the rows against the programme gets 944.5 / 1054.0.

**C. "Every unit below 90 per cent is withdrawn" against the standard's single withdrawal: not a fork.** Technical conditions clause 3 binds the provider to withdraw a unit found under 90 per cent but, in the same clause, allows one re-prequalification test a month and has a second unit carried at zero until a slot is free, so it already contemplates one slot. The desk standard (clause 3, effective 2026-07-01) says the desk withdraws the one site furthest below contract and carries the other tolerance failures at contracted capacity. The prompt asks "which ... site", a runner-up and a gap, which only a single-site, ranked reading supports. The two documents differ on how the other two sites are treated, never on which site comes out and its gain; design note SF8 records the same: Kampvliet is named first under both. Ruled closed, same call; no filing.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 17 / csv, sqlite, pdf, xlsx | yes |
| Large file | 25,000 rows or large database | 111,454-row frequency CSV, 1.19M-row sqlite | yes |
| Distractors | 2+ in metadata.json, none labelled by file name | 3 declared (imbalance prices, auction results, prequalification records), none named by file name | yes |
| Distractor weighs but unused | arithmetic reproduces, shipped fact rules out | prequalification measured/contracted puts Reiderland at 98.5 and none under tolerance, ruled out by standard clauses 2 and 3 | yes |
| Deliverables | 1 to 3, all in golden, no format family | 2 (md, xlsx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | four scorecard blocks plus chart; per cent whole, MWh one decimal, counts whole | yes |
| Prompt shape, rubric 25+ | identifiable, 25+ criteria | 992 chars, one paragraph; 9+9+9+9+12+18+... graded cells exceed 50 figures per the note | yes (rubric count not generated here) |
| Not LLM-looking, goldens realistic | no authoring language | thread found no README/dictionary/authoring language; golden realism not re-read here | yes, not independently re-verified |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical; analyst_test files Zwartewater/ramping-site by the undisturbed level or block setpoint; driver is the unit's response measured while its own scheduled trajectory runs. Match: the thread names the undisturbed level (ZWT 76) and the setpoint (RDL 57) as the easy routes, the design note's analyst test names the undisturbed level to Zwartewater. The declared distractor (prequalification records) is not named by the thread as carrying the task, so it is not too load-bearing. Gate H: thread domain pass, layers pass, decisive_step analytical; the design note's Three rules agree (no decoy, not semantics, not rule application, no shipped sentence states the traverse). No mismatch.

## Stump power (Gate F)
Thread: good; the undisturbed-level and period-setpoint routes are plausible to a strong solver who does not fit the controller traverse from the DPDT recordings, episodes sit 67 to 100 s from a boundary so the ramp matters. The decisive step is a method choice the data separate (traverse fits sharp), not a standard's textbook route filed in the pack, so it is not the landable-call case in my contract. The main thread weighs it against the ladder.

## Findings, ranked
1. Event-log start_local label (+02:00, local) is contradicted by the nine rows' own logged_utc; closed by convergence, labelled risk (ruling A). Note the design note's SF10 wording ("the event log's start field" local) does not mention the nine exceptions and reads as a stated closure the data do not bear out.
2. Meter stamps interval-ending: closed by file evidence, barred from filing (ruling B).
3. Technical conditions vs standard on withdrawal count: no figure moves (ruling C).
4. Rubric count and golden realism not independently regenerated in this pass.

## Next action for the author
None required to ship on determinism. If a Gate C comment on the start_local label is unacceptable, the only change is to the SF10 row of the design note so it records the nine-row exception, not a clause in any shipped document.

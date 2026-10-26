# determinism-check report, task137 (architecture 3), 2026-10-26

## Verdict
DETERMINISTIC on every committed figure. Main call not forced by analysis: Gate H3 fails.
**Disposition:** SEND_BACK
**Stumping type:** mechanism: single_conceptual_flip, stumping_family: surface_read_rejection, surface_read_dependency: yes, sole_data_defect: yes

## Why
Every graded figure recomputes from the bundle (run 1792999105, one sonnet thread). The call turns on one move: the arrests file holds only Calderwick officers' arrests (brief) and allocation note 2 books every detainee at the ward's suite whichever agency arrests them, so BTP's station arrests are added. The size of the addition is immaterial: any BTP figure from 121 to 371 rounds to 4,000, and the forecast method is immaterial too (model v2 3,754, flat 3,732, 5-year trend about 3,833 all give 4,000 once BTP is added). Skipping BTP gives 3,750. That is coverage reading plus rule application, with the forecast pinned by a supplied, validated model.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Six wards' arrests FY21-22..25-26 | 3,472/3,734/3,615/3,680/3,732 | same | yes |
| Model v2 2027-28 | 3,754 | 3,754.4 (no ward at cap) | yes |
| PDF validation table, four suites | as printed | exact | yes |
| BTP crimes in six wards | 1,702 (1,600 + 102) | 1,702 | yes |
| BTP arrests | 281 | 262.1 to 267.4 by type ratios; 275 to 282 with 5.0 to 5.3 pct warrant share | only under one unfiled convention |
| Planning figure | 4,000 | 4,000 under every variant | yes |
| Ask 3 remand (cell hours / over 24h) | N 4,487/183, E 2,811/109, S 7,767/296, W 5,595/240 | identical, 1,206 defendants | yes |
| Ask 4 assessments (day/night) | N 1,178/1,470, E 526/670, S 1,571/2,078, W 1,115/1,515 | identical, 10,123 | yes (under the golden's reading) |

## Competing answers that survived
All on supplementary asks; none moves the main call.
1. Ask 4, 19:00 boundary: 9 first assessments start at exactly 19:00; prompt silent on whether 19:00 is day. Day-inclusive gives N 1,180/1,468, S 1,576/2,073, W 1,117/1,513.
2. Ask 4, suite attribution: the csv "suite" is the clinician team's suite. Literal no-relocation counts: N 1,146/1,426, E 558/714, S 1,217/1,619, W 1,469/1,974. Relocation is deducible only from gaps in the arrests file; no file says the teams moved.
3. Ask 4, unit: 323 return-from-hospital second initial assessments; episodes (9,800) vs lines (10,123).
4. Ask 3, unit: "defendants" vs file "one row per case file"; 76 co-arrestee holds are missed by a file-only count.
5. Main call, BTP 281: needs the type-ratio-plus-warrant convention, not filed; the rounded 4,000 is unaffected, the quoted 281 is not forced.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 12 | yes |
| Formats | 3+ | 5 (csv, xlsx, pdf, docx, json) | yes |
| Large file | 25,000+ rows | 127,845 and 158,906 rows | yes |
| Distractors named, none labelled in a file name | 2+ | 4 in metadata.json (estate register, ward population, late-night licences, bank holidays); no name labels one | yes |
| Distractors unused yet weighable, none answers a graded quantity | yes | none answers a graded quantity; all wrong_basis false; none is a Gate G wrong-basis case | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | multi-cut; nearest 250 and nearest hour stated; counts have no rounding sentence; 19:00 boundary and assessment unit unstated | partial |
| Prompt shape identifiable, rubric 25+ criteria | yes | shape identifiable; rubric not generated here, not verifiable | not checked |
| Not LLM-generated, goldens realistic | yes | PDF header reads "HARROWDOWN POLICE" (leftover, confirmed by pdftotext); no other leakage found | FAIL (hygiene) |

## Gate G reconciliation
Thread: single_conceptual_flip / surface_read_rejection / surface_read_dependency yes / sole_data_defect yes. Design note and card: stump_strategy population_selection, layer2 field_method, gap population, gate_g forecasting; the note's own driver is "taking the force's arrest records as everyone the hub will book". The note and the thread agree on the mechanism itself (an absent second population). They disagree on its class. The note calls it field_method and gate_g forecasting, and the thread calls it a single coverage flip with a sole data defect. The declared distractors are not the surface read (the surface read is model v2 on the arrests file). No distractor is too load-bearing. Mismatch on classification is the predictive finding.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step data_semantics. Note's `## Three rules` claims Not semantics and Not rule application. The note's own evidence (nine own-arrest constructions all print 3,750; twenty BTP constructions all print 4,000, with the whole spread 3,933 to 4,045) supports the thread, not the note: the BTP piece is a presence/absence flip whose sizing never matters, and note 2 plus the brief's "one row per arrest by a Calderwick Police officer" state the coverage and the routing in shipped text. The domain test is reasonable (custody demand counted by arresting agency, with a two-force arrangement), so H1 passes. The card's analyst_test is satisfied only in the sense that a model-only analyst files 3,750; whether strong analysts skip note 2 is the scored readers' question, and the card records two Opus probes that did (4,500 vs 4,750 on the earlier probe pack).

## Stump power (Gate F)
Weak on the main call by the thread's read: a solver who reads the brief and note 2 adds BTP and cannot go wrong on size or method. Per the standing guidance, the scored readers' result decides; the card's probe misses (p137i, p137j) are the counter-evidence and the main thread should weigh them. The remaining difficulty is in the asks (shift-split lines, co-arrestee holds, team relocation), which are semantics-heavy and, as above, partly under-specified.

## Findings, ranked
1. Gate H3 / Gate G: decisive step reads as data semantics plus rule application; answer insensitive to both BTP size and forecast method (4,000 across every variant). SEND_BACK per judge. Lever: make the call turn on a forecast the supplied model does not pin, with a filed back-test choosing between methods, answer clear of the 250 boundary by more than the method spread.
2. Ask 4 forks: 19:00 boundary, suite attribution (team vs place, relocation inferred only from arrest gaps) and assessment unit are open; pin in the prompt (WHAT, not HOW).
3. Ask 3 unit: say defendants are counted from the arrest records.
4. 281 is not forced by a filed convention; rounding hides it on the main call, but critical component 3 and the ask 2 figure are gradeable and open. File the population and window or quote a range.
5. Hygiene FIX_NOW: custody_demand_model_v2.pdf header "HARROWDOWN POLICE" should read Calderwick Police. Stump-neutral.

## Next action for the author
Decide, with the scored readers' result, whether the main call stands on the card's probe evidence or is re-rooted so the forecast method is chosen by a filed back-test; either way fix the PDF header and pin the ask 4 and ask 3 wording in prompt.txt in one generator pass.

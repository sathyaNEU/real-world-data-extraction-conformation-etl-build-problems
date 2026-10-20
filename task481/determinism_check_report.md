# determinism-check report, task481, 2026-10-20

## Verdict
DETERMINISTIC, plus SOLUTION_WRONG (minor: SOLUTION_STEPS step 6 misdescribes the township-block flag; no graded figure changes).
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection (etl_conformance in the shootings ask), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The shipped files force 2025 = 5,254 (methods docx s.2: 13A victims, local report month, deleted incidents excluded) and 2024 restated = 5,193, about 5,200, +1 per cent. October to December 2024 is the only period with both bases, and the DVU log reproduces the extract's Q4 domestic 4E count exactly (1,642), which validates it as the Jan-Sep domestic split. Q4's domestic share of 4E (35.8 per cent) differs from Jan-Sep (29.1 per cent), so the unstratified Q4 line rate (5,419, -3 per cent) is biased and not an equally licensed reading. One residual fork remains in ask 2 (township blocks, below), which is why the disposition is FIX_NOW and not APPROVE.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 2024 Return A 4a-4d actual | 4,829 | 4,829 (return_a_2024.xlsx col 4; also Table 8) | yes |
| 2025 13A, local report month | 5,254 | 5,254 (UTC month 5,264; incident year 5,247; state repository 5,320) | yes |
| Q4 2024 13A | 1,204 | 1,204 (Oct 413, Nov 357, Dec 434), equals certification letter | yes |
| Q4 shares | 100.0 / 32.4 / 21.2 / 0.31 | 4A-4C 100.0; 4D 135/417 = 32.4; 4E domestic 348/1,642 = 21.2; 4E other 9/2,948 = 0.31 | yes |
| Domestic share of 4E | 35.8 / 29.1 (4,756 of 16,321) | Q4 1,642/4,590 = 35.8; Jan-Sep 4,756/16,321 = 29.1 | yes |
| Bridge | 4,829 + 202 + 1,400 - 1,238 = 5,193 | reproduced to the unit | yes |
| Change | +1 per cent | 5,254/5,193 - 1 = +1.17 | yes |
| Shootings, 12 quarters (victims / shootings) | 110/105 ... 126/115 | all 24 values match | yes |

## Competing answers that survived
- Township blocks (ask 2, quarters before Oct 2024 only). The log marks 30 early rows of the township blocks Y under the bare block name; the same blocks carry the suffixed names "(NORTH ELLSMERE TWP)" / "(CASSEL)" flagged N later, plus 26 early N rows. A solver dropping only inside_city = N rows gets 1,686 victims over 2023-2025 against the golden 1,657. The golden requires matching the block by physical name. The docx limits counts to the City and the same block is N later, so the golden is the better reading, but nothing states it, and step 6 describes it wrongly. This is an open fork on a graded ask.
- Closed: unstratified Q4 rate (5,400, -3) is closed by the DVU composition; ignoring hierarchy-hidden victims (about 5,000, +4); counting UNFOUNDED DVU rows (about 5,235, 0) is closed by the docx "deleted incidents not counted", Return A col 3 and the Q4 1,642 match; stratifying 4D by domestic moves the total by about 3 (no effect). Shooting conventions (no ME match 1,693; no dedup 1,682) are pinned by the docx and the prompt's "non-fatal".
- Margins: 43 victims from the nearest-hundred boundary; the percent sits 17 victims from the 1.5 line but is a definitive computation.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 16 (metadata.json; the thread's count of 13 was a miscount) | yes |
| Formats | 3+ | 5 (csv, xlsx, pdf, docx, txt) | yes |
| Large file | 25,000+ rows | 119,713 (NIBRS extract) | yes |
| Distractors | 2+ named, none labelled in a file name | 3 in metadata.json (census, CAD calls, state repository download); file names carry no label | yes |
| Distractor weight | unused, relevant, ruled out by a shipped fact | state repository 5,320 (incident-year basis at freeze) reproduces as an alternative 2025 count and is ruled out by the docx month-reported rule; census and CAD unused | yes |
| Deliverables | 1 to 3, all in golden | 1 (ellsmere_aggravated_assault.xlsx) | yes |
| Asks | multi-dimensional, unit and rounding stated | restated total to the hundred, counts whole, change whole percent; 12 quarters x 2 counts | yes |
| Prompt shape and rubric | shape identifiable, 25+ criteria | shape 07 (grid of cells), 29 graded items per design note | yes |
| Reads as real | no LLM tells | thread found real-looking operational artifacts, no authoring leakage | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: strategy composition_mix, Gate G etl_conformance, Layer 2 estimation_fit (conversion rates applied where stable, each period at its own composition). These agree: the thread names the same stratified-versus-pooled Q4 rate choice as the decisive step and the same easy route (5,400, -3). The declared distractors (census, CAD calls, state repository) are not named by the thread as the surface read carrying the task; the state repository's 5,320 is a wrong-basis alternate for 2025 only and is closed by the docx. No finding of an over-loaded distractor.

Gate H line: domain: pass, layers: pass, decisive_step: analytical. Field analysis: restating a summary-basis count to the incident basis with conversion rates whose composition is held to the population restated (crime-statistics bridge study). Layer 1: UTC/local month, renumbered ids, deleted incidents, township-block renaming. Layer 2: standardising the Q4 conversion for domestic mix. The design note's Three rules lines (No decoy, Not semantics, Not rule application) are consistent with the thread's reading.

## Stump power (Gate F)
Strong. The certification letter and `ucr_summary_class` invite a line-by-line Q4 restatement (5,400, -3 per cent, sign flips). The domestic composition shift is visible only by joining the DVU log. The decisive step is a judgment the data settle (is the line's rate stable across the year), not a textbook method applied without a data-settled choice, so the standard-method caveat does not apply. Hierarchy-hidden (NS) victims are a second step. The main call is bounded by a 1 per cent versus -3 per cent split, and ask 2 adds a conformation layer.

## Findings, ranked
1. Ask 2 township-block fork (pre-Oct 2024 quarters): 1,686 versus 1,657 victims depending on whether early Y-flagged rows of the township blocks are matched by physical name. Not stated anywhere; step 6 misdescribes it.
2. SOLUTION_STEPS step 6 wording: it says the log marks the township blocks N in any row and Y before October 2024; the data show bare-name rows flagged Y early, suffixed-name rows flagged N later, plus 26 early N rows.
3. Minor: no other exclusion-level finding; hygiene passes.

## Next action for the author
Correct step 6 in submission.md to describe the township blocks as the thread found them, and add one sentence to scorecard_crime_chapter_methods_2026.docx (generator) stating that the North Ellsmere Township and Cassel blocks are outside the City whatever the log's flag. File the WHAT (population), not the HOW, so the main call's decisive step stays unfiled. Rebuild, then re-judge once under /fix-determinism or stage 4.

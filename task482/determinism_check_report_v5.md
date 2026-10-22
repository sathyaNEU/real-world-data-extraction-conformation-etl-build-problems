# determinism-check report, task482 (pass v5, run r5a), 2026-10-22

## Verdict
NOT_DETERMINISTIC (competing_defensible_answer / underspecified_objective on supplementary asks 3 and 4; the designated set reproduces but rests on a location control no filed sentence requires). No SOLUTION_WRONG: every golden figure reproduced under the golden's own conventions.
**Disposition:** SEND_BACK (the repair files text solvers read, so prior runs are invalidated).
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
1. Ask 4 counts: the golden counts each housing-body block as one purchase, but circular s.2 asks for "the number of dwellings sold" and the block lines are 4 to 20 apartments in the valuation register. Counting each apartment as a dwelling gives larger counts in all 16 areas (Annaghvale 2,201 vs 2,164; Kilbrannagh 3,254 vs 3,229). Totals paid agree in both readings.
2. Ask 3 one-decimal changes come from an unfiled specification (log hedonic, electoral-division dummies, new-dwelling dummy, log floor area, type-specific year effects, weights = census count x first-year mean price). The note files only the estimand. Location-constant variants move individual areas 0.2 to 1.1 points (Dunmarra 10.2 vs 10.8, Ardcullen 10.1 vs 9.2, Drumshallon 5.6 vs 6.6 to 6.9, Innishrue 4.8 vs 5.7 under count weights).
3. The designated set is stable across all location-constant variants (same seven, smallest margin Ardcullen 8.8) but changes if location is not held constant (Ballymarne and Rathgowan replace Ardcullen and Dunmarra). No filed sentence says to hold location constant; the address point file is the only hint.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 16 area changes | per submission (Glenaskin 12.0 ... Knockfeerin 3.4) | identical under the golden's specification | yes, all 16 |
| Designated set | AC, AV, CV, DM, GS, KB, MR | identical | yes |
| Total paid incl. VAT, block paid once | per submission | identical (e.g. KB 1,425,305,000; DM 1,181,753,500) | yes, all 16 |
| Purchases, block = 1 | per submission | identical | yes (golden convention) |
| Purchases, each apartment a dwelling | not claimed | AC 2,465; AV 2,201; BM 2,400; CL 1,465; CT 1,543; CV 2,698; DM 2,982; DS 1,999; GS 1,889; IR 2,084; KB 3,254; KF 1,791; LF 1,963; MR 2,313; RG 2,784; TV 1,675 | fork |
Pipeline: old rows joined by eircode (34,471) else address plus area (3,061); old new-dwelling prices x1.135; 1,024 overlap properties deduped by property_number; 28 block groups, 362 apartment lines, all not full market price.

## Competing answers that survived
| Fork | Answers |
|---|---|
| Purchase count unit | block as 1 purchase (golden) vs each apartment a dwelling (circular wording); differs in all 16 areas |
| Location not held constant, type-stratified, census-weighted | designates AV, BM, CV, GS, KB, MR, RG |
| Pooled hedonic, one year effect | designates AV, BM, DS, GS, IR, KB, RG |
| One-decimal values under location-constant variants | differ from golden by up to 1.1 points in Dunmarra, Ardcullen, Drumshallon, Innishrue |
Closed by filed text (Layer 1): VAT gross-up, NFMP exclusion, date-of-sale windows, overlap dedup.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000+ rows | 12 / csv, pdf, xlsx / 75,141 rows (valuation register, address points) | yes |
| Distractors in metadata, unlabelled in names | 2+ | rta_registered_rents (xlsx), mortgage_drawdowns (csv); neither named as distractor in a file name | yes |
| Distractors unused yet weighable; one answering a graded quantity is ruled out by a shipped fact | | rents and loans are different markets; neither reproduces a graded quantity | yes (not arithmetically tested beyond the thread's run) |
| Deliverables | 1 to 3, all in golden | 1 xlsx, present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | | 16-area change (per cent, 1 dp), counts and totals (whole euro) | yes on form; asks 3 and 4 fail determinism |
| Prompt shape, rubric 25+ | | design note counts 69 criteria | yes |
| Not LLM-generated, goldens realistic | | no authoring leakage seen by the thread; golden realism not assessed by me | yes (thread) |

## Gate G reconciliation
Thread: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: Layer 2 estimand identification (type-own year effects, stock-value weights); decisive step the same; default path (pooled year term, Annaghvale, Ardcullen, Dunmarra, Drumshallon, Glenaskin, Innishrue, Kilbrannagh) matches the thread's pooled fork. No mismatch. The declared distractors (rents, mortgages) are not the surface read carrying the task. Passes Gate G.
Gate H: `domain: pass`, `layers: pass`, `decisive_step: analytical`. Field work is a constant-quality, stock-weighted price index; the easy route (type-stratified means or medians, or a pooled hedonic) gives Ballymarne and Rathgowan or Drumshallon and Innishrue in place of the golden's areas.

## Stump power (Gate F)
Easy routes diverge from the golden by two to four areas, so the trap can work. Caveat for the main thread: the thread's own first pass (type-stratified, no location) landed five of seven areas and the design note records that a constant-quality index with location one join away is a strong reader's reflex. The decisive method is the field's standard (Handbook) approach, which blind readers measure as landable; weigh this with the scored readers' result. The unfiled location control also means a stumped solver may hold a defensible reading rather than an analytical error.

## Findings, ranked
1. Ask 4 count unit conflicts with the circular's "number of dwellings sold" (all 16 areas).
2. Ask 3 one-decimal values not forced by the filed estimand; spread up to 1.1 points.
3. Designated set depends on an unfiled location control (file the WHAT, not the HOW).
4. Block-paid-once total is inferred from data, stated nowhere.

## Next action for the author
Run /fix-determinism with the main call frozen. File in the WHAT: the estimand with size, newness and electoral division held constant and the types weighted by stock value at prior-year prices (without naming the regression), and the unit of a purchase (block as one purchase and paid once, or dwellings, with the golden changed to match). Then re-judge once.

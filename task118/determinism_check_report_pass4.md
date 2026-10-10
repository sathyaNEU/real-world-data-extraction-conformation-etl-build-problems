# determinism-check report, task118, 2026-10-09 (pass 4)

**Pass note.** No Agent tool was available in this workflow context, so no isolated judge thread was spawned. The judge pass ran in the orchestrator's thread under the judge allow-list, enforced by reading order:
- Before `verdict.md` was written, the judge read only `guidelines/determinism_judge_system_prompt.md` (v3, verbatim), the prompt with the extracted blocks (`judge_inputs.md`), and a fresh copy of the bundle at `/tmp/determinism-check-task118-20261009T221229Z-19697/target/`.
- There is no `target.zip` in the folder, so the fresh copy was made from `target/`.
- `DESIGN_NOTE.md` (Gate G and the adjacent ladder lines), `metadata.json`, the goldens and the pass 3 report were opened only after the verdict was fixed. `solver_rounds/` and `pipeline.json` were never opened.
- Two deviations remain. First, the orchestrator read the whole `submission.md`, Tags block included, to extract the blocks. Second, the cross-batch check was not run, because it is outside the thread's allow-list and `/clone-check` covers it.

For the strict isolated-thread rehearsal, re-invoke where the Agent tool is available. Judge verdict file: `/tmp/determinism-check-task118-20261009T221229Z-19697/verdict.md`.

## Verdict
DETERMINISTIC, SOLUTION_WRONG (minor: the label on critical component 2)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main call is forced. The construction is shrunk winning lift (test-level empirical Bayes, one normal prior fitted by maximum likelihood on all 10,111 variant packages) times each desk's 2027 clicks on surfaces that render the live headline, on articles its own desk does not already test. That gives Culture·national 1,252,299 (1,250,000) against Local·metro's 808,110 (800,000).

Each step is pinned by a shipped fact:
- **Method:** `headline_squad_change_log.xlsx`, where shrunk lift reproduces 7 of 7 realised embeddings within 2% and raw lift gets 0 of 7.
- **Surfaces:** `canonical_headline` in `audience_warehouse_field_reference.md`.
- **Desk-test net:** `owner_staff_id` joined to `newsroom_staff_list_2026-10-12.xlsx`, with the plan note that new initiatives are "planned on top of these figures".

Every supplementary cell reproduces. The single defect is wording (Gate A, solution_incorrect, label only). Critical component 2 says "50.2% of Culture·national's 2027 clicks start on Bightline's own surfaces". The field reference lists newsletters and alerts as Bightline surfaces, and counting them gives 50.9%. 50.2% is the share on surfaces that show the live headline.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Main call | Culture·national | Culture·national, 1.55x over the runner-up | yes |
| Extra clicks 2027, Culture·national | 1,250,000 | 1,252,299 | yes |
| Runner-up | Local·metro, 800,000 | Local·metro, 808,110 | yes |
| Gap to runner-up | 450,000 | 444,189 unrounded; 450,000 from the rounded figures | yes |
| CC1 shrunk lift, Culture·national | 1.78% | 1.781% (prior mean -1.038%, sd 4.533%) | yes |
| CC2 share "on Bightline's own surfaces" | 50.2% | 50.16% on live-headline surfaces; 50.85% if newsletters and alerts count as own | value yes, label no |
| CC3 desk-test coverage of platform clicks | 8.6% CUL-N, 71.1% LOC-M | 8.585%, 71.066% | yes |
| CC4 Culture·national platform clicks on untested headlines | 70,300,000 | 70,314,857 | yes |
| Back-test, shrunk lift | 7 of 7 within 2% | 7 of 7, errors -0.85% to +1.16% | yes |
| Back-test, raw lift | 0 of 7 | 0 of 7; raw over-predicts 1.30x to 3.85x (the judge file rounds the low end to 32%) | yes |
| xlsx extra clicks (CUL-N / LOC-M / BUS-N / SPT-N / POL-N / SPT-M) | 1,250,000 / 800,000 / 700,000 / 650,000 / 550,000 / 100,000 | 1,252,299 / 808,110 / 697,594 / 648,293 / 552,392 / 100,400 | yes, all six |
| xlsx average monthly readers | 1,412,000 / 617,000 / 1,760,000 / 2,931,000 / 3,180,000 / 470,000 | 1,412,240 / 616,760 / 1,760,310 / 2,930,720 / 3,180,260 / 470,290 | yes, all six |
| xlsx extra clicks per reader | 0.9 / 1.3 / 0.4 / 0.2 / 0.2 / 0.2 | 0.885 / 1.297 / 0.398 / 0.222 / 0.173 / 0.213 (unrounded inputs give the same one-decimal values) | yes, all six |
| xlsx headline corrections | 14 / 34 / 39 / 42 / 47 / 18 | 14 / 34 / 39 / 42 / 47 / 18 | yes, all six |
| xlsx corrections per 1,000 articles | 3.6 / 4.9 / 4.9 / 3.8 / 5.2 / 7.3 | 3.605 / 4.898 / 4.914 / 3.803 / 5.218 / 7.308 on 3,883 / 6,941 / 7,937 / 11,043 / 9,007 / 2,463 articles | yes, all six |
| xlsx median minutes to first headline correction | 119 / 102 / 89 / 47 / 86 / 55 | 119 / 102 / 89 / 47 / 86 / 55 | yes, all six |
| xlsx back-test line | 7 of 7 | 7 of 7 | yes |
| docx chart | walk, order by extra clicks, chosen and runner-up marked, gap labelled, titled | the golden chart carries all five | yes |
| Control: dashboard by vertical (declared distractor) | not claimed | Politics 4.69, Local 3.44, Sport 3.02, Business 2.34, Culture 2.22, exact from the archive | yes |
| Control: plan vs parquet | not claimed | all 11 desks tie to the click | yes |
| Control: article denominators vs parquet | step 7 | tie exactly at all seven web desks | yes |
| Control: March 2026 corrections | not claimed | 11 headline and 22 text corrections, exactly the figures in `standards_bulletin_2026-04.docx` | yes |

## Competing answers that survived
None. Every fork tried was closed, and all but one by a shipped rule:

- **Main call, by skipped rung:**
  - Dashboard vertical lift x plan names Politics·national. Closed by the change log (raw 0 of 7) and the brief's desk grain.
  - Raw desk lift names Sport·metro. Closed by the change log.
  - Shrunk lift x all clicks, or x untested clicks on all surfaces, names Business·national. Closed by `canonical_headline`.
  - Shrunk lift x live-headline clicks with no desk-test net names Local·metro at 2.79M. Closed by the owner join and the plan note.
  - A desk-test net by article count rather than clicks still names Local·metro. Closed because lift multiplies clicks.
- **Estimator:** ML pooled, ML on web variants only and DerSimonian-Laird all pass 7 of 7 and give identical 50,000-rounded figures for all six desks. Log-scale, naive moments, per-desk priors, a zero-mean prior, a shipped-variants-only prior, an app-only prior and raw lift all fail the back-test.
- **Surfaces:** dropping related links (Culture 1,050,000) or counting newsletters and alerts (Business 750,000, Sport·national 700,000, Politics·national 600,000) are both ruled out by the field reference's closed list of stored-headline surfaces.
- **Panel:** taking the latest release regardless of the log, reading R26-04H by period, or ignoring R26-04H each changes the readers figures. Each is ruled out by a release-log note.
- **Correction counting:**
  - A note-text search gives 11 / 20 / 24 / 23 / 24 / 11, and only 3 in March against the bulletin's 11.
  - Matching the headline change at any save drops LOC-M, POL-N and SPT-M by one or two, and those four notes name the headline.
  - Timing at the note rather than at the publishing revision moves four medians, and editorial standards 7.4 pins the publishing revision.
- **Closed by data only:** a scheduled article whose next save is a draft (2,439 documents). Read as a cancelled schedule, these give Politics·national 82 and Sport·metro 43, not 86 and 55. The data refute that reading:
  - no draft save ever precedes `publish_at`;
  - draft-then-live saves on live documents are routine (10,294, median gap 3 minutes);
  - the time from `publish_at` to the first save matches documents the CMS plainly published (quartiles 80/180/418 vs 72/171/408 minutes).

  No shipped sentence states this rule, which is finding 2.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files in pack | 10 or more | 19 | PASS |
| Distinct formats | 3 or more | 8: csv, xlsx, pdf, docx, eml, md, txt, parquet | PASS |
| Large file | a file of 25,000+ rows, or a large database | parquet 2,324,291 rows (CMS csv 266,630) | PASS |
| Distractors declared | 2 or more in `metadata.json`, none labelled in a file name or file | 3 declared (Newsfold agreement, newsletter performance, dashboard export); "distractor" appears nowhere in the pack | PASS |
| Distractors unused yet relevant | same world as the decision, weighed by a solver | partner-app surface terms, newsletter clicks, lift by vertical: all unused by the solution, all about where clicks and lift come from | PASS |
| Decision-answering distractor reproduces and is ruled out | arithmetic plus a shipped fact | dashboard reproduces to the last digit; the change log (raw lift 0 of 7) and the brief's "counted at the owning desk" rule its basis out | PASS |
| Deliverables | 1 to 3 | 2 (docx, xlsx) | PASS |
| Format family | none required | not assessed by design | n/a |
| Asks multi-dimensional | not stacked lookups | six desks x six measures, each on its own pipeline (release log, CMS revision rules, click chain), plus the chart walk | PASS |
| Goldens present | every named deliverable | `golden/squad_placement_2027.docx`, `golden/squad_placement_2027.xlsx` | PASS |
| Units and rounding | stated for every ask | all stated; the docx gap, xlsx extra clicks, counts and minutes take theirs from the following sentence ("throughout"), not the asking sentence | PASS (placement carried from pass 3) |
| Prompt shape and 25-criteria floor | identifiable shape, 25+ | grid (36 cells) plus call, number, runner-up, gap, five chart elements and the back-test line, about 50 | PASS |
| Realism | nothing reads LLM-generated; goldens edited | pass 3 tells are fixed (staff names, file times, PDF producers, export log scope, authorial lines); export notes are slightly explanatory; goldens read as edited work products | PASS (minor) |

## Gate G reconciliation
| | mechanism | stumping_family | surface_read_dependency | sole_data_defect |
|---|---|---|---|---|
| Judge, pass 4 | method_or_model_selection (binding-constraint layers) | analytical_non_defect | no | no |
| Design note | decomposition_attribution (method_or_model_selection at rung 2) | analytical_non_defect | no | no |

The family and all three flags match, so no send-back is predicted. Only the mechanism label differs, and both labels are FINE-numbers shapes that pass Gate G.

Across four passes the outside readings are binding_constraint, method_or_model_selection, binding_constraint (method second), and now method_or_model_selection (binding layers). None has ever said decomposition_attribution. The build reads the same type from inside and outside but under a different name. A reviewer will write binding_constraint or method_or_model_selection.

The judge's predicted stump matches the design note's stump sentence: Local·metro, reached by never asking who ran the tests.

`metadata.json` was read after the verdict. The judge did not name a declared distractor as the surface read carrying the task. It raised the dashboard export as an official artifact that ranks the candidates (Politics first) and is wrong for the decision, but explicitly not the primary stump. The dashboard is declared as a wrong-basis distractor, it reproduces, and the change log rules its basis out. That is the house rule's one exception, so this is not a finding.

## Stump power (Gate F)
Plausible. The judge named the desk-test net as the decisive rung: a solver who shrinks and restricts to live-headline surfaces but never asks who ran the tests files Local·metro. Test-level shrinkage is the second rung, where a raw or calibration-ratio solver files Sport·metro.

Too-easy signals named:
- In `squad_placement_thread.eml`, Jason's "A small desk like Culture would waste the year" names the golden desk as the one to avoid, so a reflex-contrarian solver can land the call without the analysis.
- Nina's "Every winner the squad ships clears 95 per cent" cues winner's curse.
- The prompt's back-test line signals that a validation exists.

The most natural lever is to drop or redirect the Culture mention in Jason's line, which needs a rerun. This is the roll-call lever from pass 3, now with a sharper reason.

## Findings, ranked
1. **`submission.md` critical component 2 mislabels its figure.** "50.2% of Culture·national's 2027 clicks start on Bightline's own surfaces" is 50.9% if read literally, because the field reference lists newsletters and alerts as Bightline surfaces.
   - Restate it as "50.2% of Culture·national's 2027 clicks start on surfaces that show the live headline (web home and section fronts, the app feed and section tabs, related links)".
   - The golden docx defines "our own surfaces" in the sentence before, and the workbook's Click chain note lists them, so only the bare component needs the edit.
   - FIX_NOW, no rerun.
2. **The go-live rule for scheduled articles is pinned by data, not by a sentence.** A reviewer who reads a draft save after scheduling as a cancelled schedule recomputes Politics·national at 82 minutes and Sport·metro at 43, not 86 and 55, and would call SOLUTION_WRONG.
   - In the same `submission.md` edit, add the basis to step 7: no draft save precedes `publish_at`, and a draft save on a live article is followed by a live save within minutes, so the CMS published those articles at `publish_at`.
   - FIX_NOW, no rerun, and the ask layer stays as hard as it is.
   - A clause in `cms_revisions_export_fields.txt` would also close it, but it changes what solvers see and softens the device.
3. **`headline_tests_archive_2019-2026.csv` has 22 squad tests outside their logged embedding windows.** 20 start after the change log's end date, some on 25 December, and 2 start before the 2022 start. The log's `tests_run` reconciles only to the calendar year, so the back-test is pinned, but a reviewer filtering on started/ended gets 3 of 7, not 7 of 7.
   - Add to step 2 of `submission.md` that an embedding's tests are its desk's app tests in that calendar year, matching the log's `tests_run`. FIX_NOW.
   - Drawing those tests inside the logged window in the generator is cleaner, but the archive changes and a rerun follows.
4. **Gate F lever (carried from pass 3).** Jason's Culture line in `squad_placement_thread.eml` points a reflex solver at the answer. Redirect his caution to a desk that genuinely ranks low (Sport·metro), or cut it. Optional; rerun required.
5. **Prompt scope wording.** "gives each desk a row" and "walks every desk" never say "shortlisted"; the six-row scope is inferred from the shortlist sentence. Low risk. Say "each shortlisted desk" if the prompt is touched again (rerun).
6. **Prompt rounding placement (carried from pass 3).** The docx gap, xlsx extra clicks, counts and minutes take their rounding from the sentence after the ask. Move it inline if the prompt is touched again.
7. **Domain roster (carried).** `guidelines/scope_of_project.md` still says six domains. `CLAUDE.md` and `guide-to-prompt` accept Marketing & Consumer Research, and the skills win. Confirm with the client before delivery.
8. **Bookkeeping only, nothing shipped.** `DESIGN_NOTE.md` carries figures stale against the pack:
   - Politics vertical 4.02% (pack 4.69%);
   - Politics·metro 130 tests at 8.3% (pack 210 at 7.85%);
   - rung 0 at 16.87M (pack 17.65M), rung 2 at 6.12M (pack 6.18M), rung 3 at 2.82M (pack 2.79M);
   - tested shares 8.3% and 71.4% (pack 8.6% and 71.1%);
   - raw overstatement up to 3.57x (pack 3.85x).

   Correct them so a later iteration does not inherit them. Separately, the card's mechanism label could note binding_constraint as the expected reviewer label.

## Next action for the author
Invoke `submission-writeup` and make one edit to `submission.md`:
- Restate critical component 2 as "50.2% of Culture·national's 2027 clicks start on surfaces that show the live headline (web home and section fronts, the app feed and section tabs, related links)".
- Add the two basis sentences from findings 2 and 3 to steps 7 and 2.

None of this changes what solvers see.

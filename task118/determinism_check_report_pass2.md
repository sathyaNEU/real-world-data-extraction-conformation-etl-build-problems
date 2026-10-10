# determinism-check report, task118, 2026-10-09 (pass 2)

## Verdict
DETERMINISTIC, SOLUTION_WRONG
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

**Run note.** This runtime exposes no Agent tool, so the one judge pass ran in the orchestrator's own context. Isolation was enforced by hand, the same evidence class as pass 1. Before `verdict.md` was written to `/tmp/determinism-check-task118-pass2-20261009T184005Z-14523/`, the only things read were:
- a fresh copy of `target/` (no `target.zip` in the folder; the copy was checked byte-identical by SHA-256)
- `prompt.md`
- the four graded blocks of `submission.md`, saved as `judge_inputs.md` with Tags excluded
- `guidelines/determinism_judge_system_prompt.md` (v3)

DESIGN_NOTE.md, metadata.json, golden/, the pass-1 report and the state line of pipeline.json were opened only after the verdict was written. pipeline.json played no part. generator/, solver_rounds/ and leak_check_report.md were not opened. The cross-batch fingerprint check was not run, because it falls outside the isolation scope.

## Why
The call for Culture·national is forced by three rungs, each grounded in a shipped file:
1. **Shrunk lift beats raw lift.** It is validated by `headline_squad_change_log.xlsx`: 7 of 7 embeddings within 2 per cent, against 0 of 7 for raw lift.
2. **Only clicks on Bightline's own surfaces can move.** `canonical_headline` in the field reference sends search, social, partner feeds, newsletters and alerts the stored headline.
3. **Headlines the desk already tests are netted out.** The plan holds 2027 at the trailing year, so those gains are already in it.

That gives 1,252,299 extra clicks against Local·metro's 808,110, and no single alternative tested moves the call. Every committed figure recomputes. The defects are in the write-up:
- Step 7's going-live clause, followed as written, gives different medians at three desks.
- The Final Recommendation says Politics·national leads "only" on the dashboard.
- Step 1 does not name the one estimator form that reproduces 7 of 7.

Two ask-layer rules rest on inference rather than a filed sentence. They are the put-back note, which the pass-1 pin has made more exposed, and Discover's headline source.

## Recomputation ledger
Supplementary rows list the six desks in this order: Culture·national, Local·metro, Business·national, Sport·national, Politics·national, Sport·metro.

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Culture·national shrunk winning lift | 1.78% | 1.781%. One normal prior by maximum likelihood on all 10,111 variant packages (mu -1.04%, tau 4.53%); lift is the CTR ratio minus one; delta-method variance; a kept control counts as zero | Yes |
| Back-test, shrunk lift x planned clicks | 7 of 7 within 2% | 7 of 7 (errors +1.16% to -0.85%) | Yes |
| Back-test, raw lift | 0 of 7 | 0 of 7 (+30% to +285%) | Yes |
| Culture·national clicks starting on Bightline's own surfaces | 50.2% | 50.16% (76,918,315 of 153,340,236; home_web, section_web, feed_app, section_app, related_links) | Yes |
| Desk-run test coverage of platform clicks, Culture·national / Local·metro | 8.6% / 71.1% | 8.585% / 71.066%. All 3,515 web tests are owned by the desk's own staff; all app tests by the squad | Yes |
| Culture·national platform clicks on untested headlines | 70,300,000 | 70,314,857 | Yes |
| Parquet tie-out to the 2027 plan | ties | exact for all 11 desks (1,628,687,392 in total) | Yes |
| Extra article clicks 2027, six desks | 1,250,000; 800,000; 700,000; 650,000; 550,000; 100,000 | 1,252,299; 808,110; 697,594; 648,293; 552,392; 100,400 | Yes |
| Gap to runner-up | 450,000 | 444,189 (450,000 on unrounded or rounded figures) | Yes |
| Average monthly readers, six desks | 1,412,000; 617,000; 1,760,000; 2,931,000; 3,180,000; 470,000 | 1,412,240; 616,760; 1,760,310; 2,930,720; 3,180,260; 470,290 (release-log rule, R26-08's April to June rows set aside) | Yes |
| Extra clicks per reader, six desks | 0.9; 1.3; 0.4; 0.2; 0.2; 0.2 | 0.887; 1.310; 0.396; 0.221; 0.174; 0.213, the same on rounded inputs | Yes |
| Headline corrections, six desks | 14; 34; 39; 42; 47; 18 | same | Yes |
| Bulletin control, March 2026, seven desks | 11 headline, 22 text | 11 and 22 | Yes. Every edge-case variant gives the same pair (see Competing answers) |
| Corrections per 1,000 articles, six desks | 3.6; 4.9; 4.9; 3.8; 5.2; 7.3 | same, on 3,883; 6,941; 7,937; 11,043; 9,007; 2,463 articles, which equal the parquet's in-window article count at every desk | Yes |
| Median minutes to first headline correction, six desks | 119; 102; 89; 47; 86; 55 | same, when going live is the earlier of `publish_at` and the first live save, a restored copy uses its original, and the correction is timed at the save that publishes the corrected headline | Yes, but not under step 7 as written (finding 1) |
| Embeddings within 2 per cent | 7 of 7 | 7 of 7 | Yes |
| Dashboard export (declared distractor) | n/a | every vertical reproduces exactly from the archive (Politics 4.69, Local 3.44, Sport 3.02, Business 2.34, Culture 2.22) | Yes |

## Competing answers that survived
None overturns the main call. Two forks survive on supplementary answers under readings the files support less well than the golden's but do not rule out.

| Fork | Golden answer | Rival answer | Shipped rule meant to close it |
|---|---|---|---|
| **Put-back notes.** 11 stories lose a text-correction note on one save and get the same note back on a later save that also changes the headline | Not a new correction: 14 / 34 / 39 / 42 / 47 / 18 corrections, 3.6 / 4.9 / 4.9 / 3.8 / 5.2 / 7.3 per 1,000, medians 119 / 102 / 89 / 47 / 86 / 55 | A fix and its note on one save: 15 / 36 / 41 / 44 / 49 / 19, 3.9 / 5.2 / 5.2 / 4.0 / 5.4 / 7.7, medians 132.5 / 121 / 90 / 51 / 93 / 62.5. Two of these land on half-minutes | 7.3, the copy-forward line, and the note's earlier appearance. The stage-6 pin ("A fix and its note go on the same save, or on two saves within ten minutes of each other") literally describes the rival's restoring save. The March totals are 11 and 22 either way |
| **`discover` as an own surface** | 1,250,000; runner-up Local·metro 800,000; gap 450,000 | 1,400,000; runner-up Sport·national 1,000,000; gap 350,000 to 400,000 | Only by inference. The field reference's `canonical_headline` list names feeds, search and social metadata, newsletters and alerts, not Discover. The golden paper says Discover carries the stored headline, but the solver never sees that |

Forks tested and closed:

| Fork | Answer it produces | Closed by |
|---|---|---|
| Dashboard vertical lift, or readers | Politics·national | Brief: judged on incremental clicks at the owning desk; the prompt pins the metric |
| Raw lift | Sport·metro (2.76M) | Change log, 0 of 7 |
| Shrunk lift x all clicks | Business·national (3.59M) | `canonical_headline` |
| No netting of desk-tested headlines | Local·metro (2.79M), the stump | Plan Notes: trailing year carried forward, initiatives on top |
| Netting by article count | Local·metro (2.23M) | The gain is in clicks; tested articles carry the clicks |
| Log-scale shrinkage, or no ratio-squared variance term | Culture·national at 1,300,000; back-test 0 of 7 | Change log (0 of 7; 2 of 7 at 5%). Closed, but step 1 does not say so (finding 4) |
| The squad's own pooled lift (1.76%) for every desk | runner-up Sport·national 850,000 | The verdict listed this without a closure. The change log closes it: one pooled lift misses all seven embeddings (-31% to +153%), so the back-test certifies a desk-specific lift |
| `related_links` as a stored-headline surface | 1,050,000 | Not on the canonical list; a Bightline-rendered surface |
| Corrections by note wording only | March = 2, not 11 | Bulletin control |
| Panel by latest release ignoring logged months | every desk 1.7 to 1.9 per cent low | Release log's months and the R26-07B note |
| Panel codes mapped by period date | Business·national 2,820,000 and others | R26-04 and R26-04H notes (2026 taxonomy) |
| Going live at `publish_at` for every scheduled article | Business·national 80, Politics·national 68, Sport·metro 43, five negative durations | Data sanity; the golden's own Notes sheet states the right rule (finding 1) |

The bulletin's March totals do not discriminate the edge-case rules. Dropping entries, same save only, a 5-minute window, counting put-backs and all-revision pairing all give 11 and 22. The design note records that this is deliberate (a "false clean"). The edge-case rules therefore stand on text alone: the ten minutes, §7.4 and §7.5 are explicit, and the put-back rule is inferred.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10 or more | 19 | Yes |
| Distinct formats | 3 or more | 8 (csv, xlsx, pdf, md, txt, parquet, eml, docx) | Yes |
| Large file | 25,000+ rows or a large database | parquet 2,324,291 rows; CMS csv 266,630 rows | Yes |
| Distractors declared | 2 or more in metadata.json, none labelled in a name or file | 3: `newsfold_syndication_agreement.pdf`, `newsletter_performance_2026-07_2026-09.csv`, `experimentation_dashboard_export_2026-10-01.csv`. No shipped file or name says distractor | Yes |
| Distractors unused yet relevant | same world, something to weigh | partner-app syndication of the same articles; a stored-headline surface's clicks; the room's lift view. None enters the computation | Yes |
| Wrong-basis distractor reproduces and is ruled out | arithmetic plus a shipped fact | The dashboard reproduces exactly from the archive. It is ruled out by the brief's desk grain and by the change log (raw 0 of 7). The judge did not name it as the read carrying the task | Yes |
| Deliverable count | 1 to 3 | 2 (docx, xlsx) | Yes |
| Format family | none required | n/a | Yes |
| Asks multi-dimensional | not stacked lookups | one row per desk x six measures, each with its own ETL; a five-part chart; a back-test count | Yes |
| Golden deliverables present | every file the prompt names | `golden/squad_placement_2027.docx` (chart embedded) and `.xlsx`. Every figure matches the submission; the chart meets every named part (walk, order, both marks, gap label, title) | Yes |
| Units and rounding stated | inside the asking sentence | Main ask, readers, per-reader and rate are inline. The docx gap and the xlsx clicks, counts and minutes take their rounding from the following sentence | Yes, with note (finding 8) |
| Prompt shape, 25 criteria | identifiable shape, 25+ | shape 09, a funnel or chain of stages over a six-desk grid; about 47 gradable items off the prompt | Yes |
| Realism | nothing reads as LLM-generated; goldens read as real work | The goldens read as a real paper and workbook. The pack has minor tells (finding 9) | Yes, with notes |
| Domain tag | an accepted domain | Marketing & Consumer Research is on the on-disk CLAUDE.md nine-domain roster (commit 3745d56, 9 October) and the skills. `guidelines/scope_of_project.md` still says six | Yes, on the working standard (finding 7) |
| Objective tag | one of eight, earned | Opportunity Sizing & Decision Support: the figure is built from planned clicks down to the clicks a new headline can still move, and that sizing drives the call | Yes |
| Em dashes | none | 0 in the prompt, the submission and the golden paper | Yes |

## Gate G reconciliation
| | Mechanism | Family | surface_read_dependency | sole_data_defect |
|---|---|---|---|---|
| Judge, pass 2 (outside) | method_or_model_selection | analytical_non_defect | no | no |
| Design note (inside) | decomposition_attribution ("G5 netting over a G8 reachable base"), method_or_model_selection at rung 2 | analytical_non_defect | no | no |
| Judge, pass 1 | binding_constraint | analytical_non_defect | no | no |

Family and all three flags match across both passes and the note. Only the mechanism label moves. It has now read three ways, depending on which rung the reader treats as primary. Pass 2's own Gate F names the desk-tested netting as the trap doing the work, which is the note's decisive rung. All three labels are FINE-numbers shapes, so the mismatch does not predict a send-back.

The more useful outside signal is the borderline note in the verdict. The two sizing rungs (own-surface rather than all clicks; untested rather than all own-surface clicks) can read as lens swaps on honest data. A strict reader of v3's single_conceptual_flip could file them under rejection. The design note answers this with its lens-swap test (a strict subset reached through a two-entity join, not one population under two lenses), but that argument lives only in the note. The reviewer sees the submission.

The declared distractors were not named as the surface read carrying the task. The dashboard appears only as rung 0's rejected read, and the note asserts that the task stays hard with it deleted.

## Stump power (Gate F)
Moderate to good, and it agrees with the note's stump sentence. A strong model that shrinks correctly and keeps to own surfaces, but never asks who ran the tests, files Local·metro at about 2.8M. That is a provable error: it counts again gains the desk's own tests already put in the plan. The secondary traps are raw lift (Sport·metro), all surfaces (Business·national), and the dashboard and readers (Politics·national).

Too-easy signals:
- The field reference hands out the stored-headline rung.
- The prompt's back-test line points at out-of-sample validation.
- The plan Notes say initiatives sit "on top of these figures".
- The thread names three wrong paths (readers, "a winner is a winner", big samples).

One harsh edge: the 2% back-test band separates variance formulas, not modelling approaches. A sound solver who picks log-scale shrinkage gets 0 of 7 and 1,300,000.

## Findings, ranked
1. **`submission.md` step 7 still misstates the going-live rule (SOLUTION_WRONG).** "publish_at for a scheduled article" ignores the 4,021 scheduled articles published by hand before their `publish_at`. Followed as written, it gives five negative durations, and Business·national 80, Politics·national 68 and Sport·metro 43 instead of 89, 86 and 55. The golden workbook's Notes sheet and docx footnote 3 already state the right rule ("its publish time when the CMS published a scheduled article, otherwise its first live save"); copy it into step 7. This was inherited from pass 1's own recommendation, which said "go-live at publish_at for scheduled articles".
2. **The put-back rule is the ask layer's most exposed determinism point, and the stage-6 pin made it more so.**
   - All 11 put-backs sit on the same save as a headline change. The new field-notes line describes that save literally as a fix and its note.
   - The March control is the same either way.
   - Counting them changes all 18 corrections values, and two medians land on half-minutes.
   - Recommended: add one line under `correction_note` in `cms_revisions_export_fields.txt`, such as "A note put back after a save that left it off is the same notice, not a new correction". This is a data-dictionary pin, so FIX_NOW.
   - By the note's own pair arithmetic it costs little stump power: N-first still holds the counts, rates and medians, and the pair stays at 40.6. It does change a file the asks read, so ask-layer round results no longer carry over strictly.
3. **The Final Recommendation over-claims (SOLUTION_WRONG).** "Not Politics·national, which leads only on the dashboard's vertical lift" is untrue: Politics·national also leads the shortlist on readers (3,180,000) and on 2027 clicks (376M). Use the golden paper's line instead: it leads on the dashboard's Politics figure (4.69%), but that average is pulled up by Politics·metro's small tests, and its own tests shrink to 1.28%.
4. **Step 1 does not name the estimator form.** Only a ratio-scale lift with delta-method variance (or a web-only prior) reproduces 7 of 7 and 1.78%. Log-scale, or dropping the ratio-squared term, gives 0 of 7 and 1,300,000. The shipped back-test does exclude them, so the figure is forced. But a reviewer who reaches for log-scale will fail to reproduce both claims unless step 1 says "lift as the CTR ratio minus one, delta-method variance, one prior over every variant package of both engines". Add log-scale to the design note's fork grid too.
5. **Optional: pin Discover's headline source.** Add "Discover-style cards" to the `canonical_headline` row of `audience_warehouse_field_reference.md`. Without it, Discover-as-own keeps the call but moves the figure to 1,400,000 and the runner-up to Sport·national. It is a FIX_NOW-class dictionary pin, but it touches a main-path file, so the main path the rounds solved is no longer byte-identical. It does not touch the decisive rung.
6. **The change log fits the golden estimator too tightly to read as measured.** Its realised figures sit within 1.2% of one shrinkage formula in all seven years; difference-in-differences estimates would not. No determinism change is needed, but a reviewer may read the file as generated to one formula. The prompt and data are unchanged unless this is reopened.
7. **Domain roster: confirm with the client before delivery.** The on-disk CLAUDE.md and the skills now list nine domains, including Marketing & Consumer Research. `guidelines/scope_of_project.md` still says six, and so did the copy of CLAUDE.md loaded into this session. Pass 1's finding 6 is resolved on the repo side only.
8. **Prompt rounding placement (carried from pass 1).** The docx gap and the xlsx clicks, counts and minutes take their rounding from the next sentence. Rubric risk is low; move the rounding inline if the prompt is touched again.
9. **Realism tells (carried, partly fixed).**
   - All three PDFs give "Bightline News" as Producer and Creator.
   - Every file in `target/` has the same mtime.
   - The xlsx files are created equal to modified, with creator "Bightline News".
   - `audience_data_export_log.csv` still reads as a package manifest, logging the thread and the contract as extracts.
   - A few authorial lines remain: "Describes those tests."; "It is the view the room will have in front of it."
10. **Gate G label (no action required).** Three labels across two passes and the note; family and flags agree.

From pass 1, findings 2, 3, 4 and 5 are fixed and finding 6 is fixed on the repo side. Finding 1 is fixed except the going-live clause (finding 1 above). Findings 7 and 8 carry over.

## Next action for the author
Invoke `submission-writeup` and make one edit pass on `submission.md`:
- Replace step 7's going-live clause with the golden Notes wording ("its publish time when the CMS published a scheduled article, otherwise its first live save").
- Name the estimator form in step 1.
- Reword the Politics·national line in the Final Recommendation to the paper's.

No shipped file changes, so no rerun is needed.

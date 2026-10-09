# determinism-check report, task118, 2026-10-09

## Verdict
DETERMINISTIC, SOLUTION_WRONG
**Disposition:** FIX_NOW
**Stumping type:** mechanism: binding_constraint, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

**Run note.** This runtime exposes no Agent tool, so the one judge pass ran in the orchestrator's own context. Isolation was enforced by hand. Before `verdict.md` was written to `/tmp/determinism-check-task118-20261009T164438-15580/`, the only things read were:
- a fresh copy of `target/` (there is no `target.zip` in the folder)
- `prompt.md`
- the submission blocks
- `guidelines/determinism_judge_system_prompt.md` (v3)

DESIGN_NOTE.md, metadata.json, golden/, generator/, solver_rounds/, pipeline.json and leak_check_report.md were opened only after the verdict was written. The cross-batch fingerprint check was not run, because it falls outside the isolation scope.

## Why
The call for Culture·national is forced by three rungs, each grounded in a shipped fact:
1. **Shrunk lift beats raw lift.** One normal prior, fitted by maximum likelihood on all 10,111 variant packages in `headline_tests_archive_2019-2026.csv`, puts 7 of 7 closed embeddings within 2 per cent on `headline_squad_change_log.xlsx`. Raw lift gets 0 of 7.
2. **Only clicks on Bightline's own surfaces can move.** `audience_warehouse_field_reference.md` says the stored headline is the one carried in feeds, search and social metadata, newsletters and alerts.
3. **Headlines the desk already tests are netted out.** `audience_plan_2027.xlsx` holds 2027 at the trailing year and plans new initiatives "on top of these figures".

Every committed figure recomputes. The defect is in the solution blocks. Step 7 states the panel rule ("on the section list it was issued on") and the correction rule ("on the save before or on the save after") in words that, applied literally, produce different readers and corrections figures. It also omits the restored-copy and scheduled go-live rules that the medians depend on. The fix is to regenerate the block. Nothing a solver sees has to change.

## Recomputation ledger
Supplementary rows list the six desks in this order: Culture·national, Local·metro, Business·national, Sport·national, Politics·national, Sport·metro.

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Culture·national shrunk winning lift | 1.78% | 1.781% (prior mu -1.04%, tau 4.53%, delta-method variance) | Yes |
| Back-test, shrunk lift x planned clicks | 7 of 7 within 2% | 7 of 7, largest error 1.16% (tests by calendar year, counts match the change log) | Yes |
| Back-test, raw lift | 0 of 7 | 0 of 7 (errors +32% to +261%) | Yes |
| Culture·national clicks on Bightline surfaces | 50.2% | 50.16% (home_web, section_web, feed_app, section_app, related_links) | Yes |
| Desk-run test coverage of platform clicks, CUL / LOC | 8.6% / 71.1% | 8.585% / 71.066% (all 3,515 web tests owned by the desk's own staff) | Yes |
| Culture·national platform clicks on untested headlines | 70,300,000 | 70,314,857 | Yes |
| Parquet tie-out to the 2027 plan | ties | exact for all 11 desks | Yes |
| Extra article clicks 2027, six desks | 1,250,000; 800,000; 700,000; 650,000; 550,000; 100,000 | 1,252,299; 808,110; 697,594; 648,293; 552,392; 100,400 | Yes |
| Gap to runner-up | 450,000 | 450,000 (unrounded 444,189) | Yes |
| Average monthly readers, six desks | 1,412,000; 617,000; 1,760,000; 2,931,000; 3,180,000; 470,000 | 1,412,240; 616,760; 1,760,310; 2,930,720; 3,180,260; 470,290 | Yes (see finding 1a) |
| Extra clicks per reader, six desks | 0.9; 1.3; 0.4; 0.2; 0.2; 0.2 | same, on rounded or unrounded inputs | Yes |
| Headline corrections, six desks | 14; 34; 39; 42; 47; 18 | same (same-session pairing, entry fixed before the blog note; March across seven desks = 11, matching the bulletin) | Yes (see finding 1b) |
| Corrections per 1,000 articles, six desks | 3.6; 4.9; 4.9; 3.8; 5.2; 7.3 | same, on 3,883; 6,941; 7,937; 11,043; 9,007; 2,463 articles (equals the parquet count of articles published in the window) | Yes |
| Median minutes to first headline correction, six desks | 119; 102; 89; 47; 86; 55 | same (go-live is the earlier of publish_at and the first live save; a restored copy uses its original's go-live; the blog is the article for entry corrections) | Yes (see finding 1c) |
| Embeddings within 2 per cent | 7 of 7 | 7 of 7 | Yes |
| Dashboard export (not a solution input) | n/a | every vertical reproduces exactly from the archive (Politics 4.69, Local 3.44, Sport 3.02, Business 2.34, Culture 2.22) | Yes |

## Competing answers that survived
No fork survived for the main call or for any supplementary answer under a careful reading. These are the forks tested, with the shipped fact that closes each:

| Fork | Answer it produces | Closed by |
|---|---|---|
| Readers, Kayla's view | Politics·national (3.18m readers) | The prompt pins the metric to extra clicks |
| Raw lift x plan clicks, or raw lift x the movable base | Sport·metro (11.3m, 2.76m) | Change-log back-test, 0 of 7 |
| Shrunk lift x all clicks, or x all untested clicks | Business·national (6.18m, 3.59m) | Canonical-headline surfaces, field reference |
| Shrunk lift x platform clicks, no desk-test netting | Local·metro (2.79m), which is the stump | Plan Notes: trailing year carried forward, initiatives on top |
| Net out only articles with a shipped variant | Local·metro (1.55m vs 1.30m) | Selection error: the desk average already prices kept controls at zero |
| Squad's pooled history lift (1.80%) for every desk | Culture 1,250,000, but runner-up Sport·national (900,000) | Pooled lift x planned clicks fails the back-test (0 of 7) |
| Shrinkage variants | A pooled-p variance passes 7 of 7 with the same figures. A per-desk prior (1,200,000), mu fixed at 0 (1,300,000), a per-engine prior and a shipped-only prior all fail the back-test | Back-test |
| Drop related_links, or add discover, to platform surfaces | 1,050,000, or 1,400,000 with Sport·national runner-up | Field reference's canonical-headline list |
| Panel R26-03 read on the 2026 list by issue date | BUS 1,824,000, SPT-N 2,830,000, LOC 634,000, SPT-M 463,000 | Release log ("R26-04: first release on the 2026 content taxonomy") and the February discontinuities |
| Corrections counted by note wording only | CUL 8, LOC 25, BUS 26, SPT-N 28, POL-N 24, SPT-M 12 | Standards bulletin control total (March = 11 under the structural rule) |
| Corrections with literal save adjacency and no session limit | CUL 18, LOC 42, BUS 48, SPT-N 52, POL-N 62, SPT-M 24 | Not closed by any shipped rule. Unreasonable, because it pairs body-worded notes with headline updates hours apart |

Residual risk, closed only by reading 7.5 as fix-then-note. A symmetric 30 to 60 minute pairing window gives SPT-N 43 and POL-N 48. The cause is two blog notes whose entry headline changed 21 and 22 minutes after the note (`6LU3SH4UEH`, `N3YWU62GU5`). With the entry-before-note order, the golden counts hold for every window from 10 to 60 minutes. Neither cell is the recommended desk's.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10 or more | 19 | Yes |
| Distinct formats | 3 or more | 8 (csv, xlsx, pdf, md, txt, parquet, eml, docx) | Yes |
| Large file | 25,000+ rows or a large database | parquet 2,324,291 rows; CMS csv 266,630 rows | Yes |
| Distractors declared | 2 or more in metadata.json, none labelled in a name | 2 (newsfold_syndication_agreement.pdf, newsletter_performance_2026-07_2026-09.csv); file names neutral | Yes |
| Distractors unused yet relevant | same world, something to weigh | both are click surfaces in the Bightline world; neither is used by the solution | Yes |
| Wrong-basis artifacts declared | any file that ranks the candidates on the decision and gets it wrong must be a declared distractor | experimentation_dashboard_export_2026-10-01.csv ranks verticals for placement (the brief names it the room's view), reproduces exactly, is ruled out by the back-test, and is NOT in distractor_files | No (finding 3) |
| Deliverable count | 1 to 3 | 2 (docx, xlsx) | Yes |
| Format family | none required | n/a | Yes |
| Asks multi-dimensional | not stacked lookups | six-desk grid of six measures, each needing its own ETL, plus chart and back-test line | Yes |
| Golden deliverables present | every file the prompt names | golden/squad_placement_2027.docx and .xlsx present; figures match the submission; chart meets every named part | Yes |
| Units and rounding stated | inside the asking sentence | Main ask, readers, per-reader and rate are inline. The docx gap and the xlsx clicks, corrections and minutes take their rounding from the following sentence | Yes, with note (finding 7) |
| Prompt shape, 25 criteria | identifiable shape, 25+ | funnel or chain of stages (shape 09) over a desk grid; about 45 gradable items from the prompt | Yes |
| Realism | nothing reads LLM-generated; goldens read as real work | Goldens read as a real paper and workbook. The pack has minor tells (finding 8) | Yes, with notes |
| Domain tag | an accepted domain | "Marketing & Consumer Research" is on guide-to-prompt Step 1's nine-domain list. It is not on CLAUDE.md's, stumping SKILL.md's or guidelines/scope_of_project.md's six-domain list | Unresolved (finding 6) |

## Gate G reconciliation
- **Judge (outside):** mechanism binding_constraint, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no.
- **Design note (inside):** decomposition_attribution ("G5 netting over a G8 reachable base") with method_or_model_selection at rung 2, analytical_non_defect, surface_read_dependency no, sole_data_defect no.

Family and all three flags match. Only the mechanism label differs. From outside, the decisive step (netting desk-tested headlines out of the clicks the squad can move) reads as an eligibility limit on honest data. It does not read as splitting a movement into mix, rate and volume, which is how v3 defines decomposition_attribution. Both labels are FINE-numbers shapes that pass Gate G, so this mismatch does not predict a send-back.

The two declared distractors were not named as the surface read carrying the task. The design note's own stump sentence (a solver lands on Local·metro by never asking who ran the tests) is the trap the outside pass also found decisive. The one Gate G gap is the undeclared dashboard export (finding 3). It is a licensed wrong basis that is not filed as one, but it is not the stump: the task stays hard with it deleted.

## Stump power (Gate F)
Moderate and plausible. The trap doing the work is the desk-tested netting. A strong model that shrinks the lift and keeps only platform clicks, but never joins test owners to the staff list, files Local·metro at about 2.8m. The platform cut is the second trap; missing it gives Business·national. Too-easy signals:
- The prompt's back-test line telegraphs the method-validation step.
- The field reference states the canonical-headline fact plainly.
- The plan Notes say initiatives are "planned on top of these figures".
- `squad_placement_thread.eml` gives three opinions (readers, the dashboard, big samples), each of which pre-flags a wrong path.

The supplementary ETL is heavy (release restatements, the taxonomy cutover, put-back notes, live-blog entries, restored and migrated documents, scheduled go-live) and should hold the asks. If the solver rounds show the main call too easy, the most natural lever is to drop the explicit "within 2 per cent" framing from the prompt and keep the back-test as an unprompted check.

## Findings, ranked
1. **submission.md Step 7 misstates the rules behind the supplementary figures (SOLUTION_WRONG).**
   - (a) "Read each release on the section list it was issued on", taken as the list in force on the issue date, puts R26-03 (issued 10 March 2026) on the 2026 list. That gives BUS 1,824,000, SPT-N 2,830,000, LOC 634,000 and SPT-M 463,000. State the release-log rule instead: R26-03 and earlier on the 2025 list; R26-04, R26-04H and later on the 2026 list; R26-08's April to June rows set aside; R26-07B replaces R26-05 to R26-07.
   - (b) "On the save before or on the save after" with no session limit gives CUL 18, LOC 42, BUS 48, SPT-N 52, POL-N 62, SPT-M 24. State the same-session pairing and the live-blog order the way the golden workbook's Notes sheet does ("a few minutes apart", "the entry fixed in the minutes before it"). In that Notes sheet and in docx footnote 3, replace "the note saying the headline was corrected" with wording that does not invite a text-only count, which gives CUL 8.
   - (c) Add the two omitted rules. A restored copy continues its original: LOC-M's median is 102 only if `YJZKD97TGJ` is timed from `JNPKCW55H4`'s go-live on 2 November 2025, and is 72 without it. A scheduled article goes live at publish_at: Culture's median is 119 with it and 100 on the first live save.
2. **headline_squad_change_log.xlsx predates one of its own rows.** The export log and workbook properties date the snapshot 6 February 2026, but embedding 7's closed_on is 10 February 2026. Set the change log's extracted_on and created date to 11 February 2026 or later in the generator, both in `audience_data_export_log.csv` and in the workbook properties.
3. **The dashboard is an undeclared wrong-basis artifact.** Add `experimentation_dashboard_export_2026-10-01.csv` to `distractor_files` in metadata.json. It already meets the bar: it reproduces exactly, the back-test rules raw lift out, and it is not the stump.
4. **Optional determinism hardening.** No shipped file says how a correction note pairs with the corrected headline. One line under correction_note in `cms_revisions_export_fields.txt` would close the residual 30 to 60 minute fork on SPT-N and POL-N. It changes a shipped file, so the in-house rounds' supplementary results would no longer carry over strictly.
5. **Temporal slip in the thread.** `squad_placement_thread.eml` has the exports in the folder at 16:05 on 15 October, but `audience_data_export_log.csv` and `cms_revisions_export_fields.txt` date them 16 October. Align the dates in the generator.
6. **Domain roster conflict.** Confirm which roster is current before delivery. On the six-domain roster, the tag alone gets the task rejected.
7. **Prompt rounding placement.** For the docx gap and the xlsx extra clicks, corrections and minutes, the rounding sits in the sentence after the ask. Rubric risk is low; move it inline if the prompt is touched again.
8. **Realism tells.**
   - `audience_data_export_log.csv` reads as a package manifest: it logs the mail thread and the contract as extracts.
   - `standards_bulletin_2026-04.docx` and the golden docx carry python-docx template residue (Words 0, default thumbnail).
   - Every file in `target/` has an identical mtime.
   - The PDF producer is "Bightline News".
9. **Gate G label (no action required).** Optionally align the design note's mechanism label to binding_constraint.

## Next action for the author
Rewrite Step 7 of `submission.md` to state the rules that actually produce its numbers: the release-log taxonomy rule for the panel, same-session pairing with the entry fixed before the blog note, the restored copy continuing its original, and go-live at publish_at for scheduled articles. Use the golden workbook's Notes sheet as the base wording, and carry the same correction into that sheet and into docx footnote 3.

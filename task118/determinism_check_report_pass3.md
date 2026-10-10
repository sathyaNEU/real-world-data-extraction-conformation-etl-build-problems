# determinism-check report, task118, 2026-10-09 (pass 3)

**Pass note.** This workflow context had no Agent tool, so no isolated judge thread was spawned. The judge pass ran in the orchestrator's thread under the same isolation rules. It read only:
- the fresh copy of the bundle at `/tmp/determinism-check-task118-20261009T202126Z/target/`;
- the extracted blocks in `judge_inputs.md`;
- `guidelines/determinism_judge_system_prompt.md` (v3).

No design note, generator, `metadata.json`, golden, earlier report, solver round or `pipeline.json` was opened until `/tmp/determinism-check-task118-20261009T202126Z/verdict.md` was written. One deviation remains: the judge had read the whole `submission.md`, including the Tags block, not only the extracted blocks. For the strict isolated-thread rehearsal, re-invoke where the Agent tool is available.

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW
**Stumping type:** mechanism: binding_constraint (method_or_model_selection as the second layer), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Culture·national is forced, and three shipped facts pin it:
- The change-log back-test pins the lift estimator. Only one pooled normal prior on the lift scale, fitted by maximum likelihood (REML and DerSimonian-Laird agree), gets 7 of 7 embeddings within 2 per cent.
- The `canonical_headline` row of the field reference pins which clicks a winning headline can reach.
- Joining the archive's test owners to the staff list shows every web-desk test was desk-run, so that gain already sits in the plan, which holds 2027 at the trailing year.

Culture·national leads 1,252,299 to Local·metro's 808,110 (1.55x). It wins under every shrinkage variant tried, and each other desk falls to a shipped fact. All 41 committed values reproduce from the files. The one defect is in the write-up: step 7 never states the article denominator behind its six "per 1,000 articles" figures.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Desk for the squad | Culture·national | Culture·national (1,252,299 vs 808,110) | Yes |
| Extra clicks there, 2027 | 1,250,000 | 1,252,299 | Yes |
| Runner-up | Local·metro | Local·metro | Yes |
| Runner-up's extra clicks | 800,000 | 808,110 | Yes |
| Gap | 450,000 | 444,189 (1,250,000 less 800,000 also gives 450,000) | Yes |
| CC1: Culture·national shrunk winning lift | 1.78% | 1.781% (prior on all 10,111 packages: mu -1.038%, tau 4.533%) | Yes |
| CC2: Culture·national clicks starting on own surfaces | 50.2% | 50.16% (parquet ties to the plan to the click, every desk) | Yes |
| CC3: desk-tested share of own-surface clicks, Culture·national | 8.6% | 8.59% | Yes |
| CC3: desk-tested share of own-surface clicks, Local·metro | 71.1% | 71.07% (all 3,515 web tests are run by the desk's own staff) | Yes |
| CC4: Culture·national own-surface clicks on untested headlines | 70,300,000 | 70,314,857 | Yes |
| Back-test, shrunk lift (xlsx ask 2) | 7 of 7 | 7 of 7, errors -0.85% to +1.16% | Yes |
| Back-test, raw lift | 0 of 7 | 0 of 7, errors +30% to +285% | Yes |
| Extra clicks, Culture·national | 1,250,000 | 1,252,299 | Yes |
| Extra clicks, Local·metro | 800,000 | 808,110 | Yes |
| Extra clicks, Business·national | 700,000 | 697,594 | Yes |
| Extra clicks, Sport·national | 650,000 | 648,293 | Yes |
| Extra clicks, Politics·national | 550,000 | 552,392 | Yes |
| Extra clicks, Sport·metro | 100,000 | 100,400 | Yes |
| Monthly readers, Culture·national | 1,412,000 | 1,412,240 | Yes |
| Monthly readers, Local·metro | 617,000 | 616,760 | Yes |
| Monthly readers, Business·national | 1,760,000 | 1,760,310 | Yes |
| Monthly readers, Sport·national | 2,931,000 | 2,930,720 | Yes |
| Monthly readers, Politics·national | 3,180,000 | 3,180,260 | Yes |
| Monthly readers, Sport·metro | 470,000 | 470,290 | Yes |
| Extra per reader, Culture·national | 0.9 | 0.887 (0.885 on rounded inputs) | Yes |
| Extra per reader, Local·metro | 1.3 | 1.310 (1.297) | Yes |
| Extra per reader, Business·national | 0.4 | 0.396 (0.398) | Yes |
| Extra per reader, Sport·national | 0.2 | 0.221 (0.222) | Yes |
| Extra per reader, Politics·national | 0.2 | 0.174 (0.173) | Yes |
| Extra per reader, Sport·metro | 0.2 | 0.213 (0.213) | Yes |
| Headline corrections, Culture·national | 14 | 14 | Yes |
| Headline corrections, Local·metro | 34 | 34 | Yes |
| Headline corrections, Business·national | 39 | 39 | Yes |
| Headline corrections, Sport·national | 42 | 42 | Yes |
| Headline corrections, Politics·national | 47 | 47 | Yes |
| Headline corrections, Sport·metro | 18 | 18 | Yes |
| Rate per 1,000 articles, Culture·national | 3.6 | 3.605 (14 / 3,883) | Yes |
| Rate per 1,000 articles, Local·metro | 4.9 | 4.898 (34 / 6,941) | Yes |
| Rate per 1,000 articles, Business·national | 4.9 | 4.914 (39 / 7,937) | Yes |
| Rate per 1,000 articles, Sport·national | 3.8 | 3.803 (42 / 11,043) | Yes |
| Rate per 1,000 articles, Politics·national | 5.2 | 5.218 (47 / 9,007) | Yes |
| Rate per 1,000 articles, Sport·metro | 7.3 | 7.308 (18 / 2,463) | Yes |
| Median minutes to first headline correction, Culture·national | 119 | 119 (13 corrected articles) | Yes |
| Median minutes, Local·metro | 102 | 102 (72 if the restored copy keeps its own go-live) | Yes |
| Median minutes, Business·national | 89 | 89 | Yes |
| Median minutes, Sport·national | 47 | 47 | Yes |
| Median minutes, Politics·national | 86 | 86 | Yes |
| Median minutes, Sport·metro | 55 | 55 | Yes |
| Chart (docx ask 3) | four-stage walk, ordered, two desks marked, gap labelled, titled | derivable from the chain above; the golden chart meets every part (orchestrator check) | Yes |
| Control total, March 2026 headline and text corrections | (bulletin: 11 and 22) | 11 and 22 | Yes |
| Dashboard, all seven verticals | (reported) | exact, kept controls as zero, window on concluded date AEST | Yes |

## Competing answers that survived
None. The forks below were each built at their strongest. All are closed by a shipped rule, and the Pass column says whether the golden holds against each.

| Fork | What it produces | Shipped rule that closes it | Pass |
|---|---|---|---|
| Shrinkage form: per-engine prior, shipped-only prior, zero-mean prior, log scale, best posterior variant | Culture·national still wins; figure 1,250,000 to 1,600,000 | change log: each gets 0 or 1 of 7 within 2% | Yes |
| Netting only articles where a variant shipped | Local·metro 1,550,000 over Culture·national 1,300,000 | a desk tests before it knows the result, and the shrunk average already scores kept controls as zero. No file states this (the design note leaves it unfiled on purpose), so it rests on analysis, which is the right place for it | Yes |
| Squad-wide pooled lift (1.80%) for every desk | Culture·national 1,250,000; runner-up Sport·national 900,000 | change log: realised lift varies 0.69% to 2.57% by desk and year, so the desk's own evidence governs | Yes |
| Related links read as a stored-headline surface | Culture·national 1,050,000 | `canonical_headline` row lists the stored-headline surfaces, and related links are not among them | Yes |
| Rate denominator including the 1,704 migrated documents | 3.5, 4.7, 4.7, 3.7, 5.0, 7.0 | `migrated_from` ("moved from the previous CMS"). After the verdict I cross-checked the parquet: its count of articles published in the window equals the golden denominator at every desk (3,883; 6,941; 7,937; 11,043; 9,007; 2,463). Two files pin it | Yes |
| Go-live at the first live save for every article | medians 100, 67, 83, 41, 61, 40 | `publish_at` semantics: no CMS row is ever written at publish_at, and 4,021 articles were published by hand early | Yes |
| R26-04H read as voiding November to February wholesale | Business·national, Sport·national and every Brisbane desk on 8 months | "over the twelve months to September" | Yes |
| Put-backs counted, same-save pairing only, 5-minute window, live-blog entries ignored | 8 to 49 corrections per desk, varying by rule (the March total is 11 under each, so it cannot discriminate) | `cms_revisions_export_fields.txt` (put-back line; "within ten minutes") and standards 7.4 and 7.5 | Yes |

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10 or more | 19 | Yes |
| Distinct formats | 3 or more | 8: csv x7, xlsx x4, pdf x3, md, txt, parquet, eml, docx | Yes |
| Largest row count | a 25,000+ row file or a large database | parquet, 2,324,291 rows (CMS csv 266,630) | Yes |
| Distractors declared | 2 or more in `metadata.json`, none labelled in `target/` | 3: newsfold_syndication_agreement.pdf, newsletter_performance_2026-07_2026-09.csv, experimentation_dashboard_export_2026-10-01.csv. No file name or content labels them | Yes |
| Distractors relevant and unused | same world, something a solver has to weigh | partner-app feed terms (the stored-headline surface Local·metro lacks), a stored-headline surface's performance, and the room's own basis. All unused by the solution | Yes |
| Decision-answering distractor | reproduces, and a shipped fact rules it out | dashboard reproduces to the last digit. Raw winning lift fails the back-test 0 of 7, and the brief counts clicks at the owning desk (Politics pools Politics·metro, which is not shortlisted) | Yes |
| Deliverable count | 1 to 3 | 2 (docx, xlsx) | Yes |
| Format family | none required | Text and Data | n/a |
| Asks multi-dimensional | not stacked lookups | 6 desks x 6 measures, each a construction (sizing chain, release-log reading, corrections pipeline), plus the runner-up and gap, the chart and the back-test | Yes |
| Golden deliverables present | every file the prompt names | `golden/squad_placement_2027.docx` (with chart), `golden/squad_placement_2027.xlsx` (Desks, Click chain, Back-test, Notes). All 41 values match the submission | Yes |
| Units and rounding stated | every ask | all stated. For the docx gap and the xlsx clicks, counts and minutes, the rounding sits in a later sentence (finding 4) | Yes, placement aside |
| Prompt shape and criteria | identifiable shape, 25 or more | shape 09, chain of stages. About 46 criteria from the 36-cell grid plus call, figure, runner-up, gap, 5 chart parts and the back-test, before instruction-following | Yes |
| Tags | accepted domain, one of eight objectives | Marketing & Consumer Research (nine-domain roster, commit 3745d56), Opportunity Sizing & Decision Support | Yes (finding 7) |
| Realism | nothing reads as generated; goldens read as real work | the goldens read as a real paper and workbook. The pack carries generator tells (findings 2 and 3) | Fix in house |

## Gate G reconciliation

| Reading | mechanism | stumping_family | surface_read_dependency | sole_data_defect |
|---|---|---|---|---|
| Judge, pass 3 | binding_constraint, with method_or_model_selection second | analytical_non_defect | no | no |
| Design note's Gate G line | decomposition_attribution (G5 netting over a G8 reachable base), with method_or_model_selection at rung 2 | analytical_non_defect | no | no |
| Pass 1 | binding_constraint | analytical_non_defect | no | no |
| Pass 2 | method_or_model_selection | analytical_non_defect | no | no |

Family and all three flags agree in every reading. Only the mechanism label moves, and every label it has taken is a FINE-numbers shape that passes Gate G. No send-back is predicted.

The judge's predicted stump matches the design note's stump sentence exactly. A solver who shrinks the lift and builds the own-surface base, but never asks who ran the tests, files Local·metro.

`metadata.json` declares three distractors, and the judge named none of them as the read carrying the task. It read the dashboard as a ranking on the decision question that reproduces exactly and is ruled out by the back-test and the desk grain. That is the declared wrong-basis exception working as intended.

What the label drift implies: two of three outside readings call the netting an eligibility limit (binding_constraint) rather than a decomposition. The card's label is defensible, but binding_constraint is the label a reviewer is likely to write.

## Stump power (Gate F)
Moderate. The thread named three signposted rungs:
- the field reference spells out the stored-headline surfaces (rule discovery);
- the prompt's back-test line shows raw lift failing 0 of 7, which invites shrinkage;
- `squad_placement_thread.eml` is a roll call (Kayla on readers, Nina's "a winner is a winner", Jason on Business) that hands the solver three rungs to refute.

The trap most likely to beat a strong model is the netting rung. It needs the incrementality insight that a desk's own tests already sit in the held-flat plan, reached through a join (`owner_staff_id` to the staff list) that nothing signposts. A model that misses it files Local·metro, and one that skips the stored-headline rule files Business·national.

The supplementary devices should hold ask weight even for models that land the call. They are the release-log restatements, the stale R26-08 rows, the taxonomy remap, put-back notes, ten-minute pairing, live-blog entries, restored copies and scheduled go-live.

Most natural lever without breaking determinism: cut the thread's opinion roll call to logistics. That changes a solver-visible file, so it needs a rerun.

## Findings, ranked
1. **`submission.md` step 7 never states the article denominator.** The six "per 1,000 articles" cells reproduce only when the denominator excludes migrated documents and restored copies. Including migrated documents gives 3.5, 4.7, 4.7, 3.7, 5.0 and 7.0.
   - Add to step 7: "rates per 1,000 stories and live blogs first published October 2025 to September 2026; live-blog entries, copies restored after 14 November 2025 and documents carried across at the 1 October 2025 migration are not separate articles (the same count as the warehouse's articles published in the window)".
   - The golden workbook's Notes "Articles" row already says this. Add the same clause to footnote 3 of `golden/squad_placement_2027.docx`.
   - FIX_NOW, no rerun.
2. **`target/newsroom_staff_list_2026-10-12.xlsx` carries generator tells, and no earlier pass caught them.**
   - "Ronald Mcdonald" (BN12604) is a generator default name.
   - Every Mc surname is lowercased: Mcdonald x2, Mckay, Mccall, Mccormick, Mccarty, Mcgee.
   - The surname mix is US-skewed (Smith x12, Perez, Melendez, Carrillo, Molina) for a Sydney, Brisbane, Melbourne and Canberra newsroom.
   - Redraw the 207 names in the generator with `guard.py names --geo Australia` and recase Mc and Mac.
   - The join reads only staff_id and team_code, so this is non-decisional. FIX_NOW.
3. **Realism tells carried from passes 1 and 2.** All FIX_NOW in the generator or container.
   - `audience_data_export_log.csv` still reads as a package manifest: it logs the mail thread, the contract and the bulletin as extracts. Keep it to warehouse extracts.
   - All 19 files share the mtime 2026-10-15 23:00:00 UTC. Stagger them to each source's extraction time.
   - All three PDFs give "Bightline News" as Producer and Creator. Use real producer strings.
   - Every xlsx has created equal to modified.
   - Two authorial lines remain: "Describes those tests." (dashboard) and "It is the view the room will have in front of it." (brief).
   - The change log's realised clicks sit within 1.2% of one formula in all seven years. A reviewer may read that as fitted, though the 2% back-test needs it.
4. **Prompt rounding placement (carried).** The docx gap and the xlsx clicks, counts and minutes take their rounding from a later sentence, while the spec wants it inside the asking sentence. Rubric risk is low. Move it inline if the prompt is touched again, which needs a rerun.
5. **Optional hardening (changes solver-visible files, so a rerun follows).**
   - One clause under `migrated_from` in `cms_revisions_export_fields.txt` saying migrated documents first went live in the previous CMS. The parquet count already pins this, so it is optional.
   - Cutting the thread's roll call, which is the Gate F lever.
6. **`DESIGN_NOTE.md` line 220 (Position table, "Rung 4 order") lists Sport·metro at 0.602M, ahead of Politics·national.** The pack gives 100,400 (graded 100,000, last), as the note's own world-building item 20 records. Correct the line so a later iteration does not inherit it. This is bookkeeping and touches nothing shipped.
7. **Domain roster (carried).** `guidelines/scope_of_project.md` still says six domains, while CLAUDE.md and `guide-to-prompt` accept Marketing & Consumer Research. Confirm with the client before delivery. Nothing changes in the task.
8. **Chart readability (minor).** The golden chart draws its four stages in four close shades of blue, and on the Culture·national and Local·metro rows the stage dots overlap at log scale. Distinct hues or direct stage labels would read faster. This is a `golden-realism` item.

## Next action for the author
Invoke `submission-writeup` and add the article-denominator clause to step 7 of `submission.md`: stories and live blogs first published in the window, with entries, restored copies and migrated documents not separate articles. Carry the same clause into footnote 3 of the golden docx in that edit.

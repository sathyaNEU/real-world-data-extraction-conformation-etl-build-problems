# determinism-check report, task126, 2026-10-10

Pass 1, run because `/build` reached stage 6. The judge saw three things:

- `prompt.md`;
- a fresh copy of the bundle at `/tmp/determinism-check-task126-20261010T035555Z-29782/target/`. The folder ships an unzipped `target/` and no `target.zip`, so the bundle was copied rather than unzipped;
- the four graded blocks, inlined from `submission.md`. KEY_ASSUMPTIONS was left empty.

The standard was `guidelines/determinism_judge_system_prompt.md` (v3), read in full and applied verbatim. The judge's own record is `/tmp/determinism-check-task126-20261010T035555Z-29782/verdict.md`.

**Process deviation.** This workflow gave the orchestrator no `Agent` tool, so no separate judge thread could be spawned. The judge pass ran in the orchestrator's own context, under the thread's allow-list: the scratch path plus the inlined blocks, local tools only, no web, no server tools. `verdict.md` was written before `DESIGN_NOTE.md`, `metadata.json` or `golden/` was opened. Nothing else in the task folder was read: no generator, no answer key, no solver rounds, no `pipeline.json`, no leak report. If the author wants a separate thread, as the definition specifies, re-invoke from a context that has `Agent`.

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW. The judge pass returned APPROVE. After the verdict was fixed, the Gate G reconciliation and a read of the goldens added two write-up repairs (findings 1 and 2). Neither moves a figure, touches the prompt or the bundle, or needs a model rerun.
**Stumping type:** mechanism: etl_conformance, stumping_family: mixed, surface_read_dependency: no, sole_data_defect: no

## Why
`performance_reporting_charter.pdf` s.2 fixes the headline:

- it runs from an application's filing date to the office's final decision;
- an application still undecided at the extract counts as waiting;
- a month is 30.4375 days;
- a benefit claim does not move the filing date.

The codebook, the production standard and the production ledger then decide which docket chains are one application. Under the standard, 1N is "credited once per application" and 1R comes "after a refusal is set aside on a request for re-examination". Rebuilding applications on that rule gives 66,186 FY2022 filings and a Kaplan-Meier median of 880 days, which is 28.9 months. All 24 group cells and the 10.6% undecided share reproduce exactly. Every competing operationalisation the judge built is closed by a shipped sentence. Every undecided application has waited at least 1,461 days, so censoring cannot move any graded quantile. No gate failed; taxonomy: none.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| FY2022 filings (applications) | 66,186 | 66,186 (dockets with `docketed_on` 2021-10-01 to 2022-09-30) | yes |
| of which dockets not opened on a transferred file (no link, CN, DV) | 57,418 | 54,481 + 1,770 + 1,167 = 57,418 (`docket_links.csv` link_type) | yes |
| of which CX successors whose first action on the merits is credited 1N | 8,768 | 8,768. The first EXR by `served_on`, then `action_id`, is joined to the ledger `credit_class`; the other 24,698 FY2022 CX successors are 1R | yes |
| Undecided at the 30 Sep 2026 extract | 10.6% | 6,994 / 66,186 = 10.567% | yes |
| Shortest wait among the undecided | 1,461 d (48.0 mo) | 1,461 d | yes |
| Headline median (final recommendation) | 880 d, 28.9 mo | 880 d = 28.912 mo. KM and every numpy quantile rule agree | yes |
| 1600 lower quartile | 16.2 | 493 d = 16.197 | yes |
| 1600 median | 23.4 | 712 d = 23.392 | yes |
| 1600 decided within 36 months | 79.6% | 79.620% | yes |
| 1700 lower quartile | 17.5 | 534 d = 17.544 | yes |
| 1700 median | 25.7 | 782 d = 25.692 | yes |
| 1700 decided within 36 months | 74.1% | 74.083% | yes |
| 2100 lower quartile | 18.4 | 560 d = 18.398 | yes |
| 2100 median | 26.8 | 815 d = 26.776 | yes |
| 2100 decided within 36 months | 71.6% | 71.593% | yes |
| 2400 lower quartile | 19.8 | 604 d = 19.844 | yes |
| 2400 median | 28.6 | 870 d = 28.583 | yes |
| 2400 decided within 36 months | 66.1% | 66.103% | yes |
| 2600 lower quartile | 20.6 | 626 d = 20.567 | yes |
| 2600 median | 30.0 | 913 d = 29.996 | yes |
| 2600 decided within 36 months | 63.0% | 63.028% | yes |
| 2800 lower quartile | 21.0 | 638 d = 20.961 | yes |
| 2800 median | 30.6 | 932 d = 30.620 | yes |
| 2800 decided within 36 months | 62.5% | 62.527% | yes |
| 3600 lower quartile | 21.8 | 665 d = 21.848 | yes |
| 3600 median | 31.9 | 970 d = 31.869 | yes |
| 3600 decided within 36 months | 58.6% | 58.637% | yes |
| 3700 lower quartile | 24.0 | 731 d = 24.016 | yes |
| 3700 median | 35.2 | 1,070 d = 35.154 | yes |
| 3700 decided within 36 months | 51.6% | 51.578% | yes |
| docx ask 1, headline sentence | 28.9 months | 28.9 | yes |
| docx ask 3, undecided share | 10.6% | 10.567% | yes |
| svg asks 1, 4 and 5 (title, median label, undecided annotation) | 28.9 / 10.6% | 28.9 / 10.6% (curve ends at 89.4% decided) | yes |
| svg asks 2 and 3 (step curve with every filing in the denominator, 50% line) | presentational | consistent with report table notes ("counts every application ... in its denominator") | yes |
| Golden docx "All FY2022 filings" row (not in the submission blocks; checked after the verdict) | 19.7 / 28.9 / 65.6 | 600 d = 19.713 / 28.912 / 65.62% | yes |

Group membership: each application's docketing art unit is the `from_au` of its `docket_transfers.csv` row, else `art_unit`. That art unit is mapped to the `art_unit_groups.csv` row with a blank `valid_to`. Group sizes sum to 66,186.

Structural facts checked:

- Every docket carries at most one of NOA, REF or ABN.
- The first EXR is the only credited EXR on all 965,388 dockets that have one.
- Every CX parent has exactly one CX child, opened 5 to 62 days after the refusal.
- ALW dockets close on GRT, at a median of 139 days after the NOA.
- Last year's tables tie to this extract: P1 medians FY2016 to FY2020, P1 closed shares FY2016 to FY2025, and P2 counts FY2021 to FY2025.
- The Saravel file ties to the notice date on all 5,921 decided rows and to no grant date. Its 16 quarterly medians reproduce exactly from its own rows.

## Competing answers that survived
None.

The closest call is excluding continuations and divisionals, which gives 878 d and 28.8. The charter's "A priority or benefit claim does not move it" closes it, as do the codebook's CN and DV glosses: both are applications filed in FY2022. Excluding CN alone or DV alone still files 28.9.

The forks tested and closed:

| Fork | Answer it produces | What closes it |
|---|---|---|
| Docket pendency, P1 basis | 23.1 | charter s.2 and s.4; the P1 header "describes dockets, not applications" |
| Each FY2022 docket ended at its own notice | 20.8 | codebook CX gloss; standard 1R |
| Applications ended at their first docket's notice / close | 23.5, 25.0 / 27.1 | same |
| CX successors censored at the transfer | 27.8 | the re-examined application's decision is in the extract |
| Allowed applications ended at the grant | 32.0 | codebook ALW line; standard lists NOA as the disposal; the Saravel decision dates are NOA dates |
| Every CX chained into its parent (the decoy) | 34.0 (37.5 if ended at the grant) | 1N "credited once per application" plus the ledger |
| 1N successors dated to the parent's filing | 32.7 | charter benefit-claim sentence |
| 1N successors left out of the cohort | 30.9 | they are applications filed in FY2022 |
| Abandonment not a decision / abandoned excluded | 31.1 / 29.6 | standard lists the abandonment notice as a disposal; Saravel acknowledges abandonment as a final decision |
| Groups by recorded `tg` / by art unit at close | cells differ in every row | report table notes: restated groups, "the art unit that docketed it at filing" |
| Unclassified successor, quantile convention, 1,095 vs 1,096-day cut, month divisor | no change | no FY2022 chain reaches an unclassified successor; every convention rounds the same |

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10 or more | 16 | yes |
| Distinct formats | 3 or more | 7: parquet, csv, xlsx, md, pdf, docx, eml | yes |
| Largest row count | a file of 25,000+ rows or a large database | `office_actions_FY2016_FY2026.parquet` has 3,580,785 rows; the ledger 1,819,133; the dockets 1,020,138 | yes |
| Declared distractors | 2 or more in `metadata.json`, none labelled in a file name or a file | `examiner_roster_2026-09-30.csv` and `international_pendency_comparison_2025.xlsx`. No label anywhere under `target/` | yes |
| Distractors unused yet relevant | each unused, same world, weighable | Roster: unused. Its `tg` is the restated group of each examiner's home unit (100% consistent), which is a weighable wrong way to group applications. It is the weaker of the two. Comparison: unused. Its bases ("to grant or final refusal", "excludes divisional applications") tempt two forks the charter closes | yes |
| Distractor answering a graded quantity | must reproduce, and a shipped fact must rule it out | neither files an MPO FY2022 figure | n/a |
| Deliverable count | 1 to 3 | 2 (`.docx`, `.svg`) | yes |
| Format family | none required | Text plus Visual | not gated |
| Multi-dimensional asks | not stacked lookups | 8 groups x 3 cuts on the main construction, plus the headline, the undecided share and 5 chart parts. A wrong construction fails all of them at once | yes |
| Goldens present | every golden the prompt names | both in `golden/`. Shared figures agree across the two files and the submission: 28.9, 10.6%, 89.4% | yes |
| Units and rounding stated | every ask | The main ask and the docx asks state both. The svg sentence inherits them for the median label and the undecided annotation | yes (minor) |
| Prompt shape and 25-criteria floor | an identifiable shape and 25+ criteria | shape 14, cuts of a distribution: 24 group cells + headline + undecided share + 5 chart parts + 2 files, about 33 | yes |
| Realism | nothing LLM-generated; goldens read as real work products | Content reads as office artefacts. The goldens are edited: headed draft, footnotes, source line, sign-off footer, no em dashes. Container fingerprints and generator regularities are noted under findings 6 and 7 | yes (minor) |

## Gate G reconciliation
| | mechanism | stumping_family | surface_read_dependency | sole_data_defect |
|---|---|---|---|---|
| Judge (outside) | etl_conformance | mixed | no | no |
| Design note, Stage 2 "Gate G" (inside) | method_or_model_selection, decomposition_attribution supporting | analytical_non_defect | no | no |

**Where they agree.** Both readings agree on the two flags that drive a ban. Both also put the stump in the same place. The judge found, without the design note, the same decisive rung (split CX successors by the ledger's 1N/1R class) and the same decoy (chain every CX, 34.0 against the note's model 33.9). It also found the same reason the Saravel control cannot catch the decoy: no programme file has a 1N successor, so chain-all passes it. Neither declared distractor was named as the surface read carrying the task, so there is no distractor finding.

**Where they differ.** Two points:

1. *Mechanism label.* etl_conformance and method_or_model_selection both pass Gate G, so the label difference has no consequence. The outside reading saw no decomposition, so the note's "decomposition_attribution supporting" is not visible to a reviewer.
2. *Family: mixed against analytical_non_defect.* This is the real mismatch.
   - The judge counted Thomas Kennedy's docket-series belief as a rejection layer. The prompt names that belief, and the Final Recommendation overturns it in its first rejection: "Not examiner docket pendency".
   - The design note discounts it: "the deputy commissioner's belief is a belief". The note's deletion test does hold from the outside, since every other wrong landing survives deleting Thomas, P1 and the thread. So the judge kept the primary on the construction, and the build still passes Gate G.
   - What the mismatch predicts: the build reads as pure construction from the inside, and as a construction with a lens-flip layer in front of it from the outside.
   - The write-up makes the layer prominent. The committed call is explained by four "Not X" rejections before it is explained by what it is. A reviewer who stops there can file the build as `single_conceptual_flip`, and that is a SEND_BACK.

**What the note concedes.** The note's own line, "Every input ships except the membership of 'application', which no file states", matches the judge's "most contestable link". Inside and outside agree that the decisive fact is an inference from the production standard, not a sentence. The judge ruled it forced, because a second 1N in one chain would breach "credited once per application".

## Stump power (Gate F)
The decoy carries the stump. A solver that rebuilds applications by chaining every CX docket files 34.0, and two things push it there:

- Lauren Mendoza's "the same file" note.
- Cristina Turner's Saravel check. The programme subset runs about 33 months on honest numbers for a different population, and it agrees with chain-all exactly as well as with the golden.

Only the shielded join, from the production standard to the ledger's credit class on each CX successor's first action, reaches 28.9.

Secondary landings: 32.0 (grant end), 27.8 (censoring at the transfer), and 20.8 to 27.1 (docket-based readings). In the group table, art unit at close instead of the docketing art unit costs cells in most rows.

Too-easy signals named:

- The docket-versus-application rung is pre-disarmed by charter s.2 and s.4 and by the P1 header.
- The notice-versus-grant rung is pre-disarmed by the codebook's ALW line.

So stump power rests on one rung. A model that finds the 1N/1R split probably lands the headline and most cells together. The judge recommends no lever inside determinism. The solver round and the portal decide this one.

## Findings, ranked
1. **Gate G framing, `submission.md` section 1 (Final Recommendation).** The block explains 28.9 through four rejections, led by "Not examiner docket pendency". That shows an outside reader a lens-flip layer the design note says is not the stump. Change: open the block on the construction:
   - FY2022 applications rebuilt from dockets;
   - a 1R successor continues the same application;
   - a 1N successor is a new application filed on its docketing date, and its parent was decided at the refusal;
   - each application ends at its decision notice, with undecided applications waiting at the extract.

   Move the rejected bases into the Step-by-Step Solution. Write-up only, no rerun.
2. **Step 4 is silent on a successor with no first action yet, `submission.md` section 3.** Read literally ("follow CX edges while the successor is credited 1R and take the last docket's decision notice"), it ends such a chain at the refusal. That makes 4 programme files decided where Saravel lists them Open: 19-187170, 20-155620, 21-140669, 21-179413. The golden docx says the decision dates agree with Saravel "for every work-sharing application ... open cases included", which is false under the step as written. No FY2022 chain reaches such a successor, so no graded figure moves. Change: add "a successor with no first action at the extract leaves the application waiting".
3. **The decisive fact is an inference, `submission.md` Step 2.** No file says a CX docket can carry a new application. The judge ruled it forced, but this is the link a strict reviewer would attack as underspecified (Gate C/D). Do not pin it in a shipped file: that would disarm the stump. Change, in Step 2: spell out the forcing argument, "a second 1N inside one CX chain would breach 'credited once per application', so the 1N successor is a second application and the parent's refusal was never set aside".
4. **Thin but clean rounding margins (watch, no change).** The headline sits 1.9 days above the 28.85 boundary. Several group cells sit closer to theirs:
   - 3600 lower quartile, 0.06 d;
   - 3700 median, 0.12 d;
   - 1700 and 2400 lower quartiles, 0.18 d;
   - 3600 share decided within 36 months, about 2 applications from 58.7.

   All are forced under the charter. If the generator is ever re-seeded, extend the headline's mid-bin assertion to the 24 group cells.
5. **Vocabulary, `submission.md` section 1 and the golden docx.** No shipped file contains "continuing application". Keep the files' observable beside it ("whose first action on the merits is credited 1N") wherever the phrase appears, so a rubric line built from it stays earnable.
6. **Container fingerprints (low).**
   - `performance_reporting_charter.pdf` and `examiner_production_standard_2019.pdf` are reportlab-structured, with the header comment and Producer rewritten to a unit name.
   - `report_table_notes.docx` is the python-docx default package: customXml, thumbnail.jpeg, stylesWithEffects, and an app.xml with Words=0, Characters=0, TotalTime=0.
   - `golden/fy2022_pendency_headline.docx` carries the same python-docx parts, with TotalTime 0.

   Re-save through a real template, or make app.xml coherent. Metadata only.
7. **Generator regularities a cross-year profile exposes (low, optional, a regeneration would change what solvers see).**
   - FY2022 roots have zero unclassified CX successors, against 80 on FY2021 roots and 472 on FY2023 roots.
   - None of the 6,300 programme files has a 1N successor, against about 12% of FY2022 applications. This is by design, and the reason is deliberately unshipped.
   - 1N and 1R successors are identical on gap, examiner and art unit.

   None hands out the answer.
8. **Design note bookkeeping (low).** The Stage 2 "Gate G" section quotes model figures: 5,358 of 5,358 Saravel decisions, rung 3 at 33.9, and 60,266 applications. The pack realises 5,921 decided acknowledgements, 34.0 and 66,186. Restate them after the build is delivered, if the Build record has not already done so.

## Next action for the author
Edit `submission.md` through the `submission-writeup` skill. Open the Final Recommendation on the application construction and move the four rejected bases into the steps. In the same edit, add the Step 4 waiting clause and the Step 2 forcing clause (findings 1 to 3). No figure, prompt byte or bundle byte changes. Then re-invoke the rehearsal as pass 2, which writes `determinism_check_report_pass2.md`.

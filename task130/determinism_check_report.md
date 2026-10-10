# determinism-check report, task130, 2026-10-10

Run note. This workflow context has no `Agent` tool, so the judge pass could not be spawned as a separate thread. It ran in the orchestrator's own context under the same allow-list instead. That context saw a fresh copy of `target/` at `/tmp/determinism-check-task130-20261010T040957Z-13140/target/`, the inlined submission blocks and the v3 judge system prompt, read in full. `DESIGN_NOTE.md`, `metadata.json`, `golden/`, `generator/`, `solver_rounds/`, `pipeline.json` and `leak_check_report.md` stayed unopened until `verdict.md` had been written to the scratch path. The isolation was therefore procedural, not structural. No retry or second pass was run.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The call is forced. Article 4 of `ordre_designacio_seccions_grans_tenidors.pdf` designates on holdings at 1 January 2027, Article 2.4 defines holdings by deeds executed up to that day, and Article 2.1 counts only inscribed holders and excludes public bodies. Each rung of the 30 June to 1 January projection is pinned by a shipped file. The conformed 30 June base ties to `butlleti_parc_residencial_2026T2.pdf` in 14 of 14 sections. All 27 settled first-offer purchases were executed exactly 120 days after their PPO phase D line and never on the notified date. All 112 declared July to September sales executed as declared. The line is decided by 0301402014 at 25.70% (155/603) and 4625001012 at 24.17% (183/757). Both gaps are definitive, and the list does not move under any later agency commitment.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 30 June LH dwellings, 14 sections (step 1) | tie to bulletin 2026/2 | 162, 165, 114, 156, 93, 263, 205, 205, 187, 188, 316, 169, 126, 151, equal to the bulletin in every section | yes |
| Settled first-offer purchases, lag (CC 1) | 120 days, 27 purchases | 27 of 27 at D+120, 0 on the notified date, 4 executed before it | yes |
| Habitatges Cornisa SL in 4625011016 (CC 2) | 18 | 18 (deeds Jan 2025 to Jun 2026; inscribed 2026-09-17; no return) | yes |
| Pòrtic Residencial SL (step 4) | 5 in 4625001005, 6 in 4625013021 | 5 and 6 | yes |
| 4625011016 on 1 Jan 2027 (CC 3) | 168, 26.2% | 168, 26.21% | yes |
| 4625001012 on 1 Jan 2027 (CC 4) | 183, 24.2% | 183, 24.17% | yes |
| 0301402014 on 1 Jan 2027 (CC 5) | 155, 25.7% | 155, 25.70% | yes |
| 0301402014 December sales kept (step 3) | complete 13 to 22 January | 14 sales by B28984920, D+120 from 2027-01-13 to 2027-01-22 | yes |
| Main call | 0301401008, 0301402014, 4625001005, 4625002007, 4625011004, 4625011016, 4625012009 | same seven | yes |
| designation_brief_2027.pdf: ask 1 | the seven sections | same | yes |
| designation_brief_2027.pdf: ask 2 | 7 | 7 | yes |
| designation_brief_2027.pdf: ask 3 | 0301402014, 25.7%, 0.7 pp above | 25.70%, +0.70 pp | yes |
| designation_brief_2027.pdf: ask 4 | 4625001012, 24.2%, 0.8 pp below | 24.17%, -0.83 pp (0.8 from the rounded or unrounded share) | yes |
| designation_annex_2027.csv: 0301401008 | 157, 28.0%, Grup Cantonera, 43, 8 | same | yes |
| designation_annex_2027.csv: 0301402014 | 155, 25.7%, Grup Barana, 38, 9 | same | yes |
| designation_annex_2027.csv: 0301405003 | 109, 17.8%, Grup Cantonera, 28, 5 | same | yes |
| designation_annex_2027.csv: 1204001006 | 154, 22.4%, Grup Porxo, 40, 9 | same | yes |
| designation_annex_2027.csv: 1204003011 | 92, 17.8%, Grup Arcada, 25, 6 | same | yes |
| designation_annex_2027.csv: 4625001005 | 260, 32.0%, Grup Barana, 89, 14 | same | yes |
| designation_annex_2027.csv: 4625001012 | 183, 24.2%, Grup Xamfrà, 75, 11 | same | yes |
| designation_annex_2027.csv: 4625002007 | 202, 29.3%, Grup Finestral, 73, 9 | same | yes |
| designation_annex_2027.csv: 4625002019 | 163, 22.6%, Grup Finestral, 50, 12 | same | yes |
| designation_annex_2027.csv: 4625005013 | 183, 20.8%, Grup Escaire, 47, 10 | same | yes |
| designation_annex_2027.csv: 4625011004 | 310, 33.3%, Grup Barana, 108, 17 | same | yes |
| designation_annex_2027.csv: 4625011016 | 168, 26.2%, Grup Mitgera, 48, 7 | same | yes |
| designation_annex_2027.csv: 4625012009 | 141, 26.2%, Grup Ràfec, 54, 13 | same | yes |
| designation_annex_2027.csv: 4625013021 | 155, 20.7%, Grup Andana, 48, 6 | same | yes |
| section_bridge_2027.png: 4625001012 | 205; -1, 0, 0, -1, -20, 0; 183; line 189.25 | same (the November -20 is the agency completing on 2026-11-06 a February 2027 sale to 44516779A) | yes |
| section_bridge_2027.png: 0301402014 | 165; -2, -2, -2, 0, 0, -4; 155; line 150.75 | same | yes |
| section_bridge_2027.png: title | 7 | 7 | yes |

The golden files in `golden/` carry the same figures. The annex CSV matches cell for cell. The brief opens on the seven-section list, and the chart title reads "7 sections designated".

## Competing answers that survived
None. These forks were tested and each one is closed by a shipped fact:

| Path | Answer it produces | Closed by |
|---|---|---|
| 30 June bulletin list | 8 sections (adds 4625001012, 4625002019; drops 4625012009) | Art. 4, holdings on 1 January |
| Last year's method (notified date and buyer), with or without the new holders | 7, with 4625001012 in (26.8%) and 0301402014 out (23.4%) | 27/27 agency deeds at D+120; Art. 2.1 excludes the agency |
| Agency completing on the notified date | same swap | the same 27/27 history; the 4 completions before the notified date also kill max(notified, D+120) |
| Returns-only roll with the agency rung | 6, drops 4625011016 (150, 23.4%) | Art. 2.1 + 2.4: Cornisa is inscribed and owns 18 by deed on 1 January |
| Deeds to 30 September, no projection | 8, adds 4625001012 | 112/112 declared July to September sales executed as declared |
| OP/RS rows kept as holdings | 1204001006 inflated | guide s.7; the bulletin control total breaks |
| Group membership at 1 Oct, at 30 Jun, or from the return's codi_grup | 4 to 13 group cells change | Art. 5 frames the annex at 1 January; Vinculacions carries pre-annotated effect dates |
| Lapse reference date for the padró (delivery day, 1 Oct, 13 Nov, 1 Jan) | no count changes | robust; no registration sits on the two-year boundary |

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10 or more | 19 | PASS |
| Distinct formats | 3 or more | 6 (csv, pdf, xlsx, docx, eml, txt) | PASS |
| Largest row count | 25,000+ rows or a large DB | `declaracions_grans_tenidors_2024T3_2026T2.csv`, 45,070 rows | PASS |
| Distractors declared | 2 or more in metadata.json, none labelled in the pack | 3 (`butlleti_parc_residencial_2026T1.pdf`, `fiances_lloguer_seccions_2025.csv`, `inspeccions_habitatge_buit_2025.csv`); file names and the expedient index describe them neutrally | PASS |
| Distractors relevant and unused | same world, weighed, not used | all three cover the watch-list sections; none is used by the solution | PASS |
| Distractor answering a graded quantity | reproduces and is ruled out by a shipped fact | the March bulletin reproduces 14/14 from returns lodged by 31 May and is ruled out by Art. 4; the deposit shares are ruled out by Art. 2.3/4; the inspection vacancies by Art. 5c | PASS |
| Deliverable count | 1 to 3 | 3 | PASS |
| Format family | none required | n/a | PASS |
| Multi-dimensional asks | not stacked lookups | 14 x 5 annex grid, two six-month bridges, list plus the nearest pair | PASS |
| Deliverables present | every named golden | 3 of 3 in `golden/` | PASS |
| Units and rounding stated | every ask | stated throughout; the chart's line value "at its value in dwellings" has no precision (189.25, 150.75) | PASS (note) |
| Prompt shape, 25-criteria floor | identifiable, 25+ | bridge between two totals plus the annex grid; about 100 separately gradable figures | PASS |
| Realism | nothing reads LLM generated; goldens are real work products | pack and goldens read as real artifacts; three data or metadata tells and one layout nit, listed under Findings | PASS (notes) |

## Gate G reconciliation
The judge's classification is `forecasting` / `analytical_non_defect` / `surface_read_dependency: no` / `sole_data_defect: no`. DESIGN_NOTE.md (header and Stage 2 Gate G block) records `etl_conformance`, framed by `forecasting` (pattern A), with the same family and both flags `no`.

The family and both flags agree. The mechanism label differs only in which of two passing FINE-numbers shapes comes first, so no Gate G send-back is predicted. The outside read also agrees with the note's litmus. The 30 June bulletin ties exactly, the 2026 annex agrees with the March bulletin's 31 December 2025 back-cast, and Celestina's back-test passes again in 2026, so no correct number is read the wrong way. The thread did not name any declared distractor as a surface read carrying the task.

One implication is worth knowing. From outside, the decisive rung is a projection on a clock recovered from 27 settled cases. The note's own wording does not quite fit that: it says "every transfer it counts is known at the extract, so nothing is estimated and the tag stays ETL". If a reviewer questions the ETL tag, the defence is the conformance load the annex carries: versioned returns, the April unit change, reference repair, group-code reuse with dated links, and the per-district padró deliveries. Do not retag.

## Stump power (Gate F)
Good. The decisive rung is the agency's first-offer programme. Commitments rose from 27 (January to May) to 119 (July to September) after the 30 June budget supplement. 100 of the 146 sit on sales declared in the 30 June returns, and they complete on a 120-day clock that only the join of the budget ledger to the deed extract shows. Celestina's check ("every declared sale dated before 30 September executed on date and buyer") passes again in 2026, because every pre-empted sale is dated after 30 September. A model that verifies her method is therefore reassured. If it does find the agency, the D line hands it the notified date as the natural completion date, and both routes commit to the same wrong list (4625001012 in, 0301402014 out). The new-holder rung independently costs 4625011016.

The too-easy signals named are mild. The prompt's "sees no reason to build this one any differently" is a light reflex cue. The register Diccionari (code reuse, pre-annotated links) and the padró note (lapse rule) document the ask-level traps, but they are needed for determinism, and the main rung is documented nowhere. No lever is needed.

## Findings, ranked
None of these blocks the ship, and none touches a decisive figure.
1. `target/padro_lliurament_2026-09.csv` (realism, low to medium). Against the June delivery for the same districts, the September file has no `data_alta` after 2026-04-20 and no renewal after 2026-05-18, which are the June maxima. It has zero changed renewals, and 419 registrations appear with alta dates years in the past. Diffed, it reads as a second independent draw. The change belongs in the generator at the next regeneration: carry June forward and add dated June to August altas, bajas and renewals while holding each section's no-registrant count. This changes solver-visible data, so only do it if the pack is being regenerated anyway.
2. `target/notes_annex_2026_CGallart.docx` (metadata, low). `docProps/app.xml` reports Words, Characters, Paragraphs and TotalTime as 0 on the stock python-docx template. Write the real statistics (about 250 words) in the generator's docx writer. This is a metadata-only edit, with no rerun.
3. `prompt.md` (Gate E, low). "The designation line drawn at its value in dwellings" is the one ask without a precision; the values are 189.25 and 150.75. If the prompt is ever reopened, add "to two decimals". Not worth a rerun on its own.
4. `target/fiances_lloguer_seccions_2025.csv` (realism, low, distractor only). `import_fiances_eur` equals exactly 1.0 or 2.0 times `contractes_dipositats` x `renda_mitjana_eur` in all 54 rows, and a section aggregate rarely lands on an integer multiple. At the next regeneration, draw per-contract multiples.
5. `golden/designation_brief_2027.pdf` (cosmetic). The "The annex" heading is orphaned at the foot of page 1, with its paragraph and table on page 2. Set keep-with-next in the golden writer. Figures are unaffected.
6. `DESIGN_NOTE.md` (bookkeeping). The stage 3b build record says the golden asserts "the 23 settled cases at 120 days", but the pack has 27 (the clock-closure loop added four). The Stage 2 deletion test also names an "income atlas" that the pack does not ship. Correct both lines, and confirm the generator's assertion counts 27.

## Next action for the author
Ship task130 to the official portal as built and report the result.

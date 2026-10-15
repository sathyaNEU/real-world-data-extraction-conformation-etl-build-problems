# determinism-check report, task260, 2026-10-15

## Verdict
DETERMINISTIC (re-judge after the FIX_NOW pass; run 043008, one thread)
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Protocol section 4.1 files the estimand: the interval is for the service's film readers reading the service's screening examinations, so readers and examinations are both random. The thread recomputed every load-bearing value from a fresh unzip of target.zip. Only Halvic Breast's interval lies wholly above zero. The earlier finding (Ask B's Lumidra episode count unfiled) is closed: 44,262 episodes reproduce as distinct women with a routine study, as quote_lumidra_detect_2027.pdf defines them. No competing answer survives. After the verdict the author pinned the site-count ask in prompt.txt ("how many routine and technical-repeat screening studies each of the four sites..."). That closes the thread's one minor fork (MAMS only against MAMS plus MAMT). No figure, no file in target/ and no golden moved, so no rerun is needed.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Gain, Lumidra Detect | 0.047 | 0.0472 | yes |
| Gain, Ondrix Mammo | 0.042 | 0.0420 | yes |
| Gain, Halvic Breast | 0.026 | 0.0259 | yes |
| 95% interval, readers and cases random (OR, jackknife, Hillis df) | Halvic only above zero | Lumidra [-0.0148, 0.1092]; Ondrix [-0.0129, 0.0969]; Halvic [0.0136, 0.0383]. A two-way bootstrap gives the same classification. | yes |
| Ondrix readers reading worse with the tool | 3 of 10 | 3 of 10 | yes |
| Site counts | CRB 11,569; WDL 7,298; CPL 13,253; TLW 13,758 (45,878) | same | yes |
| Film readers on 1 April 2027 | 27 | 27 (28 rows, Johnson duplicated by registration) | yes |
| Screening episodes | 44,262 | 44,262 | yes |
| Cost, Lumidra | £110,745 | 44,262 x 2.08 + 27 x 340 + 9,500 = 110,744.96 | yes |
| Cost, Ondrix | £89,122 | 45,878 x 1.62 + 14,800 = 89,122.36, above the 60,000 minimum | yes |
| Cost, Halvic | £101,750 | 27 x 2,450 + 4 x 5,900 + 12,000 | yes |

## Competing answers that survived
None. Residual forks, all closed by shipped text:
- MAMS only against MAMS plus MAMT (CRB 11,351, WDL 7,163, CPL 13,003, TLW 13,495 under MAMS only). Closed by the codes file, the Ondrix quote and now the pinned ask wording.
- Implant-displaced "-ID" second studies count as separate accessions, and the Lumidra episode count collapses them.
- First against last submission would move Lumidra to 0.048. The field guide files the last as the reading of record.
- The interval construction (OR, DBM, two-way bootstrap, z against t) is open. Every construction gives the same classification, and the closest margin (Ondrix bootstrap lower bound -0.006) still crosses zero.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, json) | yes |
| Large file | 25,000 or more rows | ris_mammography_studies: 55,920 rows | yes |
| Distractors | 2 or more named in metadata.json, no file name labels one | 3 named (vendor_product_summaries_2026.pdf, screening_kpis_2023-24_to_2025-26.xlsx, reader_self_assessment_2025.csv); no file name labels one | yes |
| Distractor behaviour | unused, relevant, ruled out by a shipped fact | the vendor standalone AUCs rank Lumidra first; protocol 3.1 and 3.2 rule them out; they decide nothing | yes |
| Deliverables | 1 to 3, all in the golden | 3 (pdf, xlsx, png), all present in golden/ | yes |
| Asks | multi-dimensional; unit and rounding stated | gains to three decimals and costs in whole pounds are stated; the counts are whole numbers; the four-site, three-tool and cost cuts are multi-dimensional | yes |
| Prompt | one plain paragraph, under 1,000 characters | 930 characters after the pin, one plain paragraph | yes |
| Rubric of 25 or more criteria | 25 or more | not measured here; the design note lists the criteria (call, 3 gains and verdicts, reasons, 4 site counts, readers, 3 costs, chart parts), which count about 25 | not independently verified |
| Reads as real work, not LLM generated | yes | the thread found no authoring disclosure; the pdf and xlsx metadata read as in-fiction authors; the export, RIS and HR artifacts are realistic | yes |

## Gate G reconciliation
The thread's Gate G reading matches the design note and the card (stump_class analytical; strategy uncertainty_hold; signal_vs_noise_or_hold).
- **Mechanism:** the thread says statistical_rigor and the note says field_method (Obuchowski-Rockette or DBM, readers and examinations both random). Same stump.
- **Stumping family:** the thread says analytical_non_defect and the note says nothing is planted.
- **Easy routes:** the thread's routes match the note's. A case bootstrap with the readers fixed files Ondrix, and a reader-level test files Lumidra.
- **Surface read:** the declared wrong-basis distractor (vendor standalone areas) is not the surface read that carries the task, and the thread did not name it as one. The difficulty survives deleting every wrong number from the pack. surface_read_dependency is no.
- **Sole data defect:** no.
- **Mismatch:** none.

Gate G: PASS (statistical_rigor on honest data).

## Stump power (Gate F)
Moderate to good. The easy route of a reader-level paired test, or a DeLong or case-bootstrap interval with the ten readers fixed, qualifies all three tools and files Ondrix or Lumidra. The protocol hints at the target population but names no method and does not say which tool fails. A model that knows MRMC (OR or DBM) gets it right, so the stump rests on reaching for crossed random factors.

## Findings, ranked
1. No blocking finding. The previously open Lumidra episode count now reproduces.
2. Minor, closed: the site-count ask now pins routine and technical-repeat studies.
3. Not independently counted: the rubric's 25-criterion floor. The leak and portal stages cover it.

## Next action for the author
prompt.txt measures 930 characters after the pin. Run voice-check.py on it once, since the thread did not rerun the voice gate, then ship.

Gate H: PASS (domain: pass, layers: pass, decisive_step: analytical). The deciding quantity is MRMC inference on a fully crossed reader study, and the swap test fails to relabel it. Layer 1 is the v4.1 to v4.2 export change, resubmissions, a legacy RIS overlapping the new one with an hour shift, a mobile unit re-hosted, and duplicate HR registrations. Layer 2 is the reader-and-examination-random interval.

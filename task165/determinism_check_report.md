# determinism-check report, task165, 2026-10-31

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (the minor Gate C residual below is being closed in the generator by the main session; no rerun requested)
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One judge thread (sonnet, medium) saw only a fresh unzip of target.zip and the five blocks. The call of 2,200 t reproduced from the files, and every estimator in the family it tried (weighted and unweighted linear, quadratic, cubic, log-log) lands in 2,158 to 2,209 t, all rounding to 2,200. The tempting routes land clearly elsewhere (2,570 to 2,660 t on the Priority 1 level less own salt, about 1,505 t on the average gain). The dome and arterial figures reproduce to the stated rounding. Gates A to E pass. The one soft spot was the dome figures' dependence on counting five double-weighed loads once (Gate C, below).

Note: the thread was not run by me (my runtime had no Agent tool); the main session spawned it from the brief I wrote and handed back verdict.md at /tmp/determinism-check-task165-1793463743/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| New segments moved 2026-08-30 | 216 segments, 424.0 lane-km | 216, 424.0 (matches QRT street list) | yes |
| Earlier P2 to P1 moves | 377 | 377 (136, 69, 119, 53) | yes |
| WSI by winter | 61.7 planning point | 63.4, 50.1, 38.9, 67.2, 58.4 | yes |
| New segments' own P2 salt | about 700 t, under 2 t/lane-km | 665 t, 1.57 t/lane-km | approximately (loose "about") |
| Gain vs own P2 salt, 377 | falls with own P2 salt | corr -0.95; fit gain = 0.1009 - 0.657 x pre | yes |
| Seasonal tonnage | 2,200 t | 2,203.7 t (bootstrap SD 15 t, 95% 2,173 to 2,232) | yes |
| Dome 1 Nov, Kelvin Road / room | 7,843.2 / 1,356.8 t | same | yes |
| Mapleford | 7,142.4 / 1,257.6 | same | yes |
| Ridge | 8,447.4 / 2,352.6 | same | yes |
| Lakeshore | 6,279.6 / 1,320.4 | same | yes |
| Arterial Kelvin Road, 3 winters | 5,100 / 10,000 / 8,200 | 5,105.9 / 10,007.1 / 8,200.9 | yes |
| Mapleford | 7,000 / 13,700 / 11,300 | 6,997.4 / 13,695.3 / 11,300.4 | yes |
| Ridge | 6,650 / 13,200 / 10,700 | 6,645.7 / 13,196.8 / 10,695.1 | yes |
| Lakeshore | 2,750 / 5,400 / 4,500 | 2,747.7 / 5,394.9 / 4,496.6 | yes |

## Competing answers that survived
- Procedure 4.1 read as total need less 39,100 t (about 46,000 to 48,600 t): does not survive, since 4.2 and the prompt pin the commitment to the change's additional salt. Mild latent tension only.
- Gate C residual (minor, being fixed): no file states trucks are weighed at two scales. Five pairs share vehicle and gross within 20 kg, 0.58 to 0.97 h apart. Three carry a destination remark on the first ticket; two (KLV-041051 / MPF-042539 and RDG-044077 / LKS-045505) do not, so counting at the later yard was an inference. Each moves a dome figure by about 44 t (without dedup: KLV 7,887.6, MPF 7,185.6, RDG 8,491.6, LKS 6,367.1; unremarked pairs kept at the first yard: MPF 7,098.2, LKS 6,235.6). The coordinator reports the generator is being changed so every double-weighed pair carries its destination remark. That change is not in the pack the thread judged and is not verified here; the dome figures must be re-checked on the rebuilt pack.
- Brine deduction alternatives (water only, 23%, none) move cells across a 25 t boundary; the literal reading (total less litres at 1.18 kg, both stated in the plan) is the golden.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 19 in target.zip and target/ (the thread's hygiene line said 20; the count is 19) | yes |
| Formats | 3+ | csv, pdf, xlsx, parquet (4) | yes |
| Large file | 25,000+ rows | telematics parquet 344,770 rows, AVL csv 164,095 | yes |
| Distractors | 2+, named, not in file names | metadata.json names yard_timesheets_2025-26.csv and brine_production_log_2023-10_to_2026-09.csv; file names do not label them | yes |
| Distractor behaviour | unused, weighable, ruled out by a shipped fact | thread found none used by the solution; neither answers a graded quantity (not independently tested by me) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 8 dome figures, 12 arterial figures; unit and rounding in the prompt | yes |
| Prompt shape / 25 criteria | identifiable, 25+ | single-figure with decoupled asks; 21 graded figures plus call and chart. The 25-criterion count is the design note's, not recomputed | yes (per note) |
| Reads as real, not LLM generated | | thread found no provenance leakage; golden realism not re-judged here | yes |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: stump is an estimation_fit (gain conditioned on each street's own Priority 2 salt), rivals are the pooled gain and the pooled Priority 1 level, no planted defect. Match. Declared distractors (timesheets, brine log) are not named as the surface read carrying the task; the surface reads the thread names are the P1-level-less-own-salt and average-gain routes, which are the design note's declared rivals and sit in no shipped artifact as a ranked answer. Gate G: pass, analytical, no surface-read dependency.

Gate H: thread says domain pass, layers pass, decisive_step analytical. Design note's Three rules lines (Not semantics, Not rule application, No decoy, Domain, Layers, Analyst test) agree: decisive step is carrying the earlier moves' gain conditioned on own P2 salt; layer 1 is AVL/GIS/UTC/kg/M410/double-weighing mess. Match, no mismatch finding.

## Stump power (Gate F)
Strong per the thread: the naive routes land at 1,500 and 2,600 to 2,700 t, 400 to 500 t or more away from the golden; a strong analyst who cleans everything and reads every rule can still file them. The conditioned-gain method is an estimation choice the data separate (corr -0.95), not a textbook route the thread flagged as landable by default. The main thread weighs it against the design note's ladder.

## Findings, ranked
1. Gate C, minor: two unremarked double-weighed pairs make the dome figures rest on an inference. Coordinator is adding the destination remark to every pair; re-verify the four dome figures after the rebuild.
2. Cosmetic: the golden's "about 700 t" for the new streets' own P2 salt is 665 t on recompute (still under 2 t/lane-km); consider "about 650 t" or the exact figure.
3. Latent: procedure 4.1 wording versus 4.2 does not survive but is a reading a careless reviewer could raise.

## Next action for the author
After the generator change, rebuild twice byte-identical, recompute the four dome stock/room pairs and confirm they still equal 7,843.2 / 7,142.4 / 8,447.4 / 6,279.6 t, then update the "about 700 t" figure in submission.md section 2 if you want it to match the 665 t recompute.

## Author's note on the Gate C residual (main thread, 2026-10-31)

The residual is kept, not closed: the two unremarked pairs are Ask A's device A4. Remarks on them would move A4's
double count onto Lakeshore and Mapleford and hand back Ridge's and Kelvin Road's four dome figures on every careful
path. The yard is forced without a remark: the later ticket carries the same gross, so the load was still on the truck
when it reached the receiving yard's scale, and only that ticket shows the 14 to 31 minutes of a load tipped. No file
changed; target.zip d9c24521 is the pack judged.

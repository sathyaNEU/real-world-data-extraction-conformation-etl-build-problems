# determinism-check report, task119, 2026-10-10

Pass 3, run at `/build` stage 6. The judge's own verdict is at `/tmp/determinism-check-task119-20261010T042012Z-16099/verdict.md`. The scratch copy of `target/` is in the same folder and is byte-identical to `task119/target/` by md5.

How this pass ran: this workflow gave the orchestrator no `Agent` tool, so no separate judge thread could be spawned. The judge phase ran inline, and the isolation was kept by ordering instead.
- **Before `verdict.md` was written**, only the judge system prompt (v3, read in full), `prompt.md`, the submission blocks and the scratch copy of the bundle were read.
- **After it was written**, `metadata.json`, `golden/` and the design note's Gate G, stump and ship-log sections were read, for the spec gates and the reconciliation below.
- **Never opened:** the generator, the answer key, the solver rounds, the earlier reports and the leak report.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: decomposition_attribution, stumping_family: mixed, surface_read_dependency: no, sole_data_defect: no

## Why
The terms of reference pin every decisive term:
- **Remit (section 2):** level 3 referrals from a ward or the ED, more than four hours from the decision to admit to the bed's assignment, death within 30 days.
- **Objective (section 3):** deaths confirmed avoidable because of the reviewed trust's own care.
- **Methodology note (section 4):** "A trust's decisions about the use of its own beds and staff are part of its own care."
- **Basis (section 5):** July 2025 to June 2026.

On that basis, all 27 of Stennock's remit deaths followed waits during which STN-ACC held one or two beds for its own Stennock Treatment Centre electives, who were still in theatre or recovery at the waiting patient's decision. Prideswick's 15 followed waits beside an empty staffed bed. Every other long wait was either a full unit or a bureau allocation (`bed_confirmed_at`). So Stennock, 27, runner-up Prideswick at 15, gap 12, is forced, and every supplementary figure reproduces. No gate failed and no taxonomy label applies.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Main call (docx ask 1) | Stennock (STN) | Stennock | yes |
| Stennock confirmable, placement year (docx ask 2, CC 2) | 27 | 27; all 27 waits had 1 or 2 held beds at the decision (39 holds), and no free-bed minute | yes |
| Runner-up (docx ask 3, CC 3) | Prideswick, 15 | Prideswick, 15; free staffed bed for 254 to 361 min, the whole wait | yes |
| Gap (docx ask 4, CC 4, png ask 4) | 12 | 12 | yes |
| Ristenholm confirmable | 2 | 2; the other 35 death-waits saw 35 admissions, all other trusts' elective transfers in the audit | yes |
| Brackenford confirmable | 0 | 0; no free minute in any of 118 long waits, and 23 admissions, all bureau | yes |
| Lathingbury, Tannerby, Ellerdyke, Pellowham confirmable | 0 each | 0 each; no level 3 unit on the decision date | yes |
| Placement-year remit deaths (step 2) | 213, 20 before a bed | 213, 20 | yes |
| Lathingbury remit deaths, no level 3 beds (CC 1) | 56 | 56 | yes |
| png bar Stennock | 27 | 27 | yes |
| png bar Prideswick | 21 | 21 | yes |
| png bar Ristenholm | 44 | 44 | yes |
| png bar Lathingbury | 56 | 56 | yes |
| png bar Brackenford | 35 | 35 | yes |
| png bar Ellerdyke | 13 | 13 | yes |
| png bar Tannerby | 10 | 10 | yes |
| png bar Pellowham | 7 | 7 | yes |
| png shaded part (ask 2) | 27, 15, 2, then 0 for five | 27, 15, 2, then 0 for five | yes |
| png order (ask 3) | STN, PRW, RIS, then the five in any order | same | yes |
| png title (ask 5) | names Stennock | presentation item, golden title names Stennock | yes |
| xlsx Brackenford (patients / deaths / confirmable) | 351 / 104 / 5 | 351 / 104 / 5 | yes |
| xlsx Ellerdyke | 140 / 40 / 6 | 140 / 40 / 6 | yes |
| xlsx Lathingbury | 559 / 165 / 0 | 559 / 165 / 0 | yes |
| xlsx Pellowham | 75 / 22 / 3 | 75 / 22 / 3 | yes |
| xlsx Prideswick | 221 / 63 / 46 | 221 / 63 / 46 | yes |
| xlsx Ristenholm | 438 / 126 / 8 | 438 / 126 / 8 | yes |
| xlsx Stennock | 275 / 80 / 80 | 275 / 80 / 80 | yes |
| xlsx Tannerby | 104 / 29 / 0 | 104 / 29 / 0 | yes |
| xlsx totals | 2,163 / 629 / 148 | 2,163 / 629 / 148 | yes |

**Sources:**
- `critical_care_referrals_202307_202606.csv`: `dta_at`, `outcome_at`, `level_of_care`, `referred_from`, `referring_trust`.
- `ccrs_referral_levels_202307_202404.csv`: the DECISION entry.
- `acc_unit_stays_202306_202606.parquet`: `admitted_at` (bed assigned), `discharged_at`, `admission_type`.
- `acc_bed_return_0800_202306_202606.csv`: `beds_open`.
- `acc_unit_register.csv`: `care_level`, `valid_from`, `valid_to`.
- `interhospital_transfer_audit_202307_202606.csv`: `bed_confirmed_at`, `arrived_at`.
- `rds_theatre_cases_2023-2026.parquet`: `left_recovery_at`, `site_name`.
- `apc_episodes_referred_patients_2022-2026.parquet`: `date_of_death`, and `discharge_method` 4 for unresolved keys.
- `pas_patient_key_links_2023-2026.csv`.

**Each conformance step is load-bearing in the workbook, and each is pinned by a shipped statement:**
- No UTC conversion gives 2,183 / 645 / 172.
- The form level instead of the decision level gives 2,179 / 645 / 152.
- No `bed_confirmed_at` shift gives 183 confirmable. The legacy feed codes 916 of 977 inter-trust transfers as 01.
- No bed-row merge gives 156.
- No spell-ending-in-death fallback gives 619 deaths.
- Naive clock arithmetic adds 20 waits on the 2024 and 2025 spring-forward nights.
- The pilot double entry is neutral (CC or R row, no change).

## Competing answers that survived
None. Each fork the judge built, with the answer it gives and the shipped fact that closes it:
- **Lathingbury 56** (the Chair's "most patients die waiting"; also first on the receipt-clock screen at 243). Closed by ToR s.3 and s.2; Lathingbury runs no level 3 unit.
- **Brackenford 34** (the 08:00 return shows a free bed on 34 of 35 death dates, and the network manager's email says the same). Closed by the minute census: full through all 118 long waits.
- **Prideswick 15** (empty unassigned beds only, which is also what the NRR corpus literally shows, since no NRR case has a held bed). Closed by ToR s.4 together with the field guide's "the minute the bed was assigned" and the theatre `left_recovery_at`.
- **Ristenholm 37** (the bureau's holds counted as Ristenholm's decisions). Closed by the field guide's `bed_confirmed_at` ("the network bed bureau allocated the bed") and ACCN/23/41 s.3.
- **Ristenholm 38** (beds occupied by its own electives counted as own care) and **Ristenholm 44** (every remit death confirmable). Unreasonable or contrary to s.3.
- **Workbook level after a later LEVEL CHANGE** (4 patients, 2 deaths). Closed by timing: every change was recorded 43 to 66 hours after the bed was assigned.

The margin is definitive. No remit death falls on days 24 to 35, no wait sits at exactly 4 hours, and the placement year has no clock-change or stood-down effects.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files in the pack | 10 or more | 20 | yes |
| Distinct formats | 3 or more | 8 (csv, parquet, pdf, xlsx, docx, sqlite, txt, eml) | yes |
| Large file | 25,000+ rows in any format, or a large database | APC parquet 88,145 rows; ambulance csv 70,072; NRR sqlite 12.7 MB (48,755 referral rows) | yes |
| Distractors declared, none labelled | 2+ in `metadata.json`; no file name or content marks one | 5 declared; no file name or text labels one | yes |
| Distractors relevant and off the path | unused by the solution, same world | none of the 5 is used by the reproduction; all are the same world (level 2 beds, ED handovers, network capacity, the review programme) | yes |
| Distractor figures reproduce, and a shipped fact rules them out | arithmetic plus a clause | capacity report: 108/108 occupancy cells, 216/216 receipt-clock wait cells. NRR log: 34/34 rows on every column. Ruled out by ToR s.2 (decision clock), s.3 (objective) and the register (level 2 units cannot give level 3 care) | yes |
| Deliverables | 1 to 3 | 3 (docx, xlsx, png) | yes |
| Format family | none required | not assessed | yes |
| Multi-dimensional asks | no stacked lookups | an 8 x 3 grid with totals; an 8-bar chart with shaded part, order, gap and title; a four-part call | yes |
| Golden deliverables present | every file the prompt names | 3 of 3 in `golden/` | yes |
| Units and rounding | stated for every ask | each ask names its unit (deaths, patients). Rounding is one global sentence ("whole numbers throughout") rather than inside each ask sentence | yes |
| Prompt shape and criteria floor | identifiable, 25 or more | shape 07, grid of cells: 24 cells + 3 totals + 4 docx figures + 5 chart parts = 36 | yes |
| Realism, pack | nothing reads as LLM generated | reads as system exports, specs, papers and mail. No authoring or tool leakage: the only scan hits were the PDF /Trapped key and Word style XML. Known debts in finding 4 | yes |
| Realism, goldens | real work products, not an unedited draft | the board paper (with table and footnote), the workings (with notes sheet) and the chart all read as real. Two wording nits (finding 3); typed totals | yes |

## Gate G reconciliation
| Field | Judge | Design note (`### Gate G`, and the draw at lines 132 to 136) | Match |
|---|---|---|---|
| mechanism | decomposition_attribution | decomposition_attribution | yes |
| stumping_family | mixed | analytical_non_defect | no |
| surface_read_dependency | no | no | yes |
| sole_data_defect | no | no | yes |

**The one mismatch is the family label, and it does not change the outcome.** Both labels pass Gate G, because the primary layer is the same on both readings. That layer is the held-bed attribution against Prideswick's empty beds, on correct numbers.

**Why the judge said mixed.** The judge counted the ladder's lower rungs as a rejection layer under v3's own definitions:
- The Chair's deaths-waiting lens, which names Lathingbury. The note itself calls Lathingbury "the naive leader" that "the natural pipeline still counts first".
- The Brackenford morning-return rung.

v3 classes a lens swap on correct numbers as `single_conceptual_flip`, which is in the surface-read family. "Mixed" is v3's label for an independent FINE-numbers layer that stumps on its own plus such a layer.

**Why the note says analytical_non_defect.** Its litmus is narrower: "no voice's claim about its own numbers is overturned".

**What this predicts.** A portal reviewer is more likely to reach mixed than banned_stumping_type, so the send-back risk is low.

**Distractor and corpus checks:**
- The judge did not name a declared distractor as the surface read carrying the task.
- The judge found that the NRR corpus cannot tell "free bed" from "held bed" (every NRR remit death sat beside a free bed). That matches the note's L1 "corpus blind for a computable reason", so it is a designed property, not a load-bearing distractor.
- The two wrong answers the judge built independently (Prideswick 15 and Ristenholm 37) are exactly the two the note's stump sentence names. The build reads the same from the outside as from the inside.
- The note's ship log records that passes 1 and 2 matched it on all four fields.

## Stump power (Gate F)
Moderate to good. The trap that does the work is Prideswick: a strong model that rebuilds the minute census correctly finds Stennock full through every wait, files it as capacity, and commits to Prideswick at 15. Stennock's holds show only through a join the prompt never mentions: STN 03 "planned transfer in" stays matched to Stennock Treatment Centre theatre cases, with `left_recovery_at` against the waiting patient's decision. The lower rungs (Lathingbury, the Brackenford 08:00 read, and Ristenholm via bureau holds) catch weaker paths.

Too-easy signals named:
- ToR s.4 states the principle outright.
- The network manager's email points at all three units, including "Stennock's unit is full every morning".

Optional lever, which costs a rerun and is not needed on present evidence: drop that Stennock sentence from `review_placement_correspondence.eml`.

## Findings, ranked
1. **Process (affects this pass, not the task).**
   - The workflow gave no `Agent` tool, so the judge ran inline, isolated by ordering rather than by a separate thread. If a thread-isolated record is wanted, re-invoke in a runtime that grants `Agent`.
   - Separately, the session scratchpad is shared with concurrent runs. Another task's determinism run (task128) overwrote the shared `scratch_path.txt` mid-pass. This pass verified its copy by md5 and re-ran the affected step, so no figure here is affected.
   - The shared directory listing exposed file names from earlier passes. Only names were seen, and they carried nothing beyond the submission blocks.
   - Fix: give each workflow run its own scratch subfolder.
2. **Gate G family label** (mixed against analytical_non_defect, both passing). No pack change. In `DESIGN_NOTE.md` `### Gate G`, either adopt "mixed", or add one line saying why the Chair's deaths-waiting rung (Lathingbury) is not a v3 `single_conceptual_flip` layer.
3. **Golden board paper wording** (`golden/external_review_placement_2027-28.docx`, "Why Stennock" paragraph). Optional; golden-only, no figure moves and no rerun.
   - "admitted nobody while they lasted" fails in 5 of 92 Stennock waits, including 2 of the 27 deaths (R2601-01348, R2604-00884). In each, a bed went to a Stennock elective in the same minute as the waiting patient's decision. Delete that clause.
   - "assigned that morning" covers 14 of 133 holds that were made between 12:00 and 12:52. Change it to "assigned earlier that day".
4. **Known realism debts** (already listed in the note; none affects determinism). Optional lever, which costs a regenerate and a rerun: narrow the death-day hole to days 29 to 31, which still closes the 30-day fork.
   - **The death-day hole is the debt most visible to a reviewer.** No remit death falls on days 24 to 35 after the decision across 2,163 patients (10 on day 23, 4 on day 36). A reviewer probing the 30-day boundary sees it first.
   - **Other debts:**
     - `beds_open` is constant for three years.
     - Ristenholm and Stennock show 100 per cent at 08:00 on all 1,126 days.
     - Long waits sit in fixed clock windows: Brackenford 18:00 to 23:59; Stennock decisions 10:00 to 13:59 on weekdays.
     - Workbook totals are typed values, not `=SUM()`.

## Next action for the author
Take task119 to the portal test as it stands: the pass is APPROVE and no rerun is needed.

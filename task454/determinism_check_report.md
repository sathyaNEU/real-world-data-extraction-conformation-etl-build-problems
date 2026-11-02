# determinism-check report, task454, 2026-11-02

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: single_conceptual_flip (borderline, leans method on honest data), stumping_family: analytical_non_defect (borderline), surface_read_dependency: no, sole_data_defect: no

## Why
The isolated thread (one pass, sonnet, medium) recomputed every graded figure from a fresh unzip and reproduced all of them. The main call (five funded regions; Yallambee Valley fifth at $4,150, Pelican Coast $3,205, $945 short) follows from guidelines section 4 (IRTS visitor, in person, Australian cards, selection-weighted, ERP 30 Jun 2026 over Schedule 1 with shared SA2 shares). The card-region pairs split into two classes with an empty gap (trip: at most 3 months and 21 days; routine: 8+ months and 59+ days; none at 4 to 7 months), so every usual-environment threshold in the gap gives the same classes. The asks (remaining balance, unspent returned, grant) each have one reading once transfers and receipts are unbundled, which the amounts force (one subset per transfer, one component set per receipt).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cards / rows | 12,201 / 148,555 | 12,201 / 148,555, weights 1:1 | yes |
| Per resident JAB, LYR, SPX, TNG, YAL, PEL, GID, CAR, WOL, MUL, KEL | 10,149; 5,894; 5,197; 4,272; 4,150; 3,205; 2,657; 2,547; 1,521; 1,387; 1,167 | identical | yes |
| Quarterly and annual spend | golden csv | match to $1,000 (rounded once from raw; sums of rounded quarters differ by 1,000 for CAR, LYR, YAL, settled by "each rounded once") | yes |
| Shortfall | 945 | 945 | yes |
| Remaining at 31 Dec 2026, by region | JAB 506,601 ... KEL 283,900 | identical; total 3,852,428.51 (golden 3,852,430 = sum of rounded regional figures) | yes |
| Unspent returned, by region | JAB 76,015 ... KEL 25,754 | identical; total 709,968.77 (golden 709,970) | yes |
| Grant | 1,771,508 | 8,857,540.26 / 5 = 1,771,508.05 | yes, on exact or rounded inputs |

## Competing answers that survived
None on the main call or the asks. Second readings, all ruled out by shipped facts:
- Count every non-Westhaven spend as visitor: LYR, JAB, CAR, GID, SPX funded (about $13,000 to $18,000 per resident). Ruled out by the IRTS visitor definition in section 4.
- Residents by statement SA2 (the address route): JAB 10,149, LYR 6,363, GID 5,410, SPX 5,197, CAR 5,027, then TNG 4,268, YAL 4,250, PEL 3,966. Funds GID and CAR in place of TNG and YAL. Ruled out by the data: GID and CAR cards sit there 8 to 12 months on 59+ days, and the statement SA2 matches the routine region in only 73 to 82 percent of cases.
- Scaling by apn_regional_totals (about 0.905 to 0.916 of the weighted sample): ranking unchanged.
- Quoted-agreement attribution of transfers (no unbundling): remaining total 3,787,913 (PEL, KEL, SPX move). Counting the 20 March repeats as paid: PEL 562,016, KEL 249,963, SPX 211,545. Counting all receipts as unspent: 957,487. The grant moves with these totals (about 1.77M at golden, more under the naive readings). The unbundling is load-bearing for the grant but forced by the data (unique subsets; refunds equal the repeats; closure paragraph 4 says repeats are not unspent money).

Residual risk the thread flagged: the IRTS definition is named in the pack but not quoted, and the bundling of claims into one transfer and the 20 March duplicates are inferred, not stated. Both are recoverable from the amounts.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 11 | yes |
| Formats | 3 or more | csv, xlsx, pdf | yes |
| Large file | 25,000 rows or more | 148,555 rows | yes |
| Distractors | 2 or more in metadata.json, no file name labels one | apn_regional_totals_2026.csv, erp_sa2_30jun2025_revised.xlsx; neither name labels it | yes |
| Distractors relevant and ruled out | unused by the solution, a shipped fact rules each out | totals cover all card products and overseas cards (about 0.91 of sample, ranking unchanged); 2025 ERP is superseded by the 2026 denominator the guidelines file | yes |
| Deliverables | 1 to 3, all in golden | 2 (csv, docx), both in golden | yes |
| Asks multi-dimensional, unit and rounding stated | yes | quarters x regions, per-resident, program figures, grant; unit and rounding in the prompt | yes |
| Prompt shape and 25+ criteria | yes | Design note states above 60 criteria before any ask; I did not run the rubric generator | yes (per note) |
| Reads as real, not LLM generated | yes | thread found no authoring leakage; dates coherent; mixed date formats and duplicate run give realistic mess; golden realism not re-judged here | yes |

## Gate G reconciliation
Thread: mechanism single_conceptual_flip (borderline), stumping_family analytical_non_defect (borderline), surface_read_dependency no, sole_data_defect no. Card: stump_class analytical; the analyst test (address route files GID $5,410 and CAR $5,027 among the five, replacing TNG and YAL) and the design note's ladder agree with the thread's easy route and figures exactly. The card carries no mechanism or stumping_family fields to compare. The thread does not name the declared distractors as the surface read carrying the task; the easy route is the statement-address residence proxy, not a distractor. No mismatch.

## Gate H
domain: pass. layers: pass (Layer 1: nested keys, preliminary vs revised ERP, shared SA2 shares, bundled transfers, duplicate payment run; Layer 2: usual-environment classification and weighted per-capita ranking). decisive_step: analytical. The design note's Three rules lines (No decoy, Not semantics, Not rule application) agree. The thread's caveat is that the decisive step leans on the IRTS usual-environment concept, which the pack names but does not quote; the data separate the classes with an empty gap.

## Stump power (Gate F)
Moderate on the main call: a strong model that reads the IRTS reference and the month counts will likely find the usual-environment classification. The asks (unbundling consolidated transfers, dropping the 20 March repeats, separating repeat from unspent money) are where strong models most likely slip, since no file states the bundling. The thread did not class the decisive step as analytical because it is a textbook method; it reached the golden by classifying cards, which is judgment the data had to settle. The main thread should weigh this against the design note's ladder (the note reports a 1.295 rung 2 figure).

## Findings, ranked
1. No blocking finding.
2. Low: the IRTS definition is not quoted in the pack (section 4 cites it by name only).
3. Low: the bundling and duplicate-run inferences rest on amounts alone (unique subset per transfer and per receipt).
4. Note: the golden totals (3,852,430; 709,970) are sums of rounded regional figures; the exact totals are 3,852,428.51 and 709,968.77. The grant agrees on either basis.

## Next action for the author
Proceed to ship; no repair needed. Optionally weigh the stump power point above against the design note's ladder.

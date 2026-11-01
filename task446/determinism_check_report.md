# determinism-check report, task446, 2026-11-01

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting / method_or_model_selection (mix shift validated out of sample), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

One isolated sonnet thread (run 20261101T163955), fresh unzip of target.zip at /tmp/determinism-check-task446-20261101T163955/target/ (16 files). Thread verdict: /tmp/determinism-check-task446-20261101T163955/verdict.md. This overwrites the earlier report as the author directed.

## Why
Every graded figure rebuilds from the shipped files using only CRM-07 definitions (4.1, 4.2, 5.1 to 5.3, 6.1, 6.2). The main call is 78 (77.97). The back-test that 5.2 invites picks the split by the member that raised the flag: leave-one-cohort-out largest miss 3.9% for the split, 14.4% for one flagged rate. Alternative splits that validate (customer vs other, RED, multi-member, score band) land on 77.5 to 78.2. The easy route (pooled 4.3 hit and false-alarm rates) gives 64.05, and a single all-groups rate gives 47.1.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Book at 30 Sep 2026 | 913 | 913 | yes |
| Flagged / on a customer | 165 / 127 | 165 / 127 | yes |
| Customer-flag cohorts | 120/240 = 50.0% | same | yes |
| Other-member-flag cohorts | 11/176 = 6.25% | same | yes |
| Not-flagged cohorts | 50/3,092 = 1.62% | same | yes |
| Expected arrivals | 78.0 | 77.97 | yes |
| LOCO largest miss, split / one rate | 3.9% / 14.4% | 3.9% / 14.4% | yes |
| Bands, groups | 201/304/248/120/40 | same | yes |
| Bands, arrivals | 16.2/25.8/21.9/9.0/5.1 | same | yes |
| Bands, arriving exposure GBP m | 38.5/257.1/596.8/576.3/826.8 | same | yes |
| Total committed / arriving exposure GBP m | 25,663.4 / 2,295.5 | same | yes |
| Flagged per band | 34/54/46/20/11 | same | yes |

## Competing answers that survived
- Main call: none. The pooled-rate 64 is the intended wrong route, closed by the back-test that 5.2 invites (implicit rather than spelled out, the main residual risk and also the stump).
- Asks only (band cells, Gate C/E): 6.1 counts "facilities" and the 22 undrawn ledger twins are not filed as excluded. A literal reader who keeps them gets bands 199/302/250/118/44 and total 25,943.2. The data separates the cases (identical limit history to the preceding facility, undrawn). Other readings: UTC cut-off gives 197/298/254/114/50; dropping the GLEIF cross-group placement gives 203/312/243/120/35. The main call is unaffected.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | 6 (csv, xlsx, json, pdf, txt, docx) | yes |
| Large file | 25,000 rows | 125,975 rows (ews signals) | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | 2 named (rating master scale, Group Economics outlook); file names do not label them | yes |
| Distractor behaviour | unused, relevant, ruled out by a shipped fact | not used by the solution; thread found neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | band table across 5 bands by 5 measures; whole number, one decimal, GBP m one decimal stated | yes |
| Prompt shape / rubric | identifiable; 25+ criteria | shape 05 (allocation to a fixed total); every band cell gradable, 25+ plausible by construction (rubric not shipped, not counted here) | yes |
| Not LLM-reading | clean | no authoring disclosures seen by the thread; prompt 798 characters, one paragraph | yes |

## Gate G reconciliation
Thread: mechanism forecasting (method_or_model_selection), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: Gate G mechanism forecasting, stump_class analytical, strategy composition_mix, no decoy. Match. The declared distractors (rating master scale, Group Economics outlook) are not named by the thread as the surface read, so they are not too load-bearing. No shipped artifact ranks the call wrongly.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. Matches the design note's Three rules (PD-style segmentation of the flagged population by raising member; Layer 1 key, GLEIF, UK-time and ledger-twin mess; Layer 2 stratified rate validated on closed cohorts).

## Stump power (Gate F)
Good on paper: customer flags rise to 77% of this September's flags against 48 to 69% in the cohorts, so the pooled rate files 64 against 78. Caveat for the main thread: the judge calls the back-test implicit in 5.2, and the design note itself records that earlier stage 4 readers filed 64 without building it. A strong solver who segments flags by raising member (the standard PD-style route) lands 78, so the ladder should be weighed against that. The decisive step is not classed analytical merely because it is a textbook method: the judge found the split needed a join from signals to the obligor master that 3.2 never invites.

## Findings, ranked
1. Optional, asks only: the 22 twin facilities are not filed as counted once. Adding a WHAT sentence (a facility the ledger booked twice counts once) would remove the band-cell fork. Do not file the method.
2. Main residual risk: the back-test is implicit in 5.2, and is also the intended stump. No change required.

## Next action for the author
None required to ship on determinism. Optionally file, as a WHAT, that a facility booked twice in the ledger counts once, then rebuild twice byte-identical and rerun figures_check.

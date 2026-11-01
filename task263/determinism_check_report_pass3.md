# determinism-check report, task263, 2026-11-01 (pass 3)

Final cut judged: target.zip md5 c38b70927ef7065db923fe1d22411dca (fresh unzip at /tmp/determinism-check-task263-r3c/target/, byte-identical to the zip's contents). Thread output: /tmp/determinism-check-task263-r3c/verdict.md. The earlier thread on the 81d61969 cut was stopped before writing and is not used.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main call reproduces from the shipped files: 23 of 53 active wells over 4.0 ng/L, 16 of 20 systems funded, Torvik through Valdahl, Nordvold (691,200) the first not reached, 451,200 left. It holds under non-detects at 0, half or full reporting limit, revision 1 or 2, equal or capacity weights, 2024, 2025 or both years, with or without confirmation samples. The nearest well under the line is 2.4 to 3.3 ng/L and the nearest over is 7.1 to 7.3, so there is no near-tie. The three rival easy routes (7, 8 and 11 systems) reproduce and are each ruled out by s.6.3 "a well's own water is the water the well itself pumps". The pump fact now sits in the inventory `pump` column (constant speed on all 220 wells with a value), so capacity-proportional mixing is derivable from the files, and flow over summed rated capacity is 0.95 to 1.06 on all 393 samples that name sources.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Samples, listed systems, 2024-25, RT/CO | 302 at 24 entry points | 302 / 24 | yes (results csv + collection records) |
| Wells over 4.0 | 23 of 53 | 23 of 53 | yes |
| Grants (20) | per golden, e.g. Torvik 1,728,000, Halvorsen 6,000,000 cap, Nordvold 691,200 | identical | yes (inventory rated_capacity_gpm x 1,440 / 1e6 x 2.4M) |
| Funded / spent / left | 16 / 35,548,800 / 451,200 | same | yes |
| County water, Mgal 2025 | 1,342.9 / 1,318.4 / 913.5 / 714.6 | same | yes (operating reports, meter register, inventory facility_type) |
| County people | 30,167 / 29,442 / 21,518 / 17,614 | same | yes (register, wholesale connections) |
| Chart | 53 wells, 23 over | 53, 23 | yes |

## Competing answers that survived
None on the main call or on any ask. The two low-risk readings the thread named are ruled below.
- **Kesselring emergency Well 3 in the county water (Hedstrom 913.5 vs 912.7): CLOSED, one figure.** The ask is "the listed systems' wells", with no status filter; "active" appears only in the chart sentence and in s.6.3 (which governs grants, not the water ask). Executed literally, the emergency well is a listed system's well that pumped (799,270 gal in July 2025), so 913.5. The 912.7 figure needs an unstated "active only" restriction; it is a wrong reading of the text, not a second literal answer. Residual risk is a solver importing the chart sentence's "active" into the water ask; the design note already carries this as H3 with 912.7 as the named wrong route, and the main call is unaffected.
- **Inactive buyer ids in the county population: CLOSED, one figure.** The ask is people living in the county who get their water from those wells, which is a current-state question. The register holds each of the four renumbered buyers (Fjelstad Junction 942, Halvorsen Township 1,436, Torvik East 1,130, Wikstrom Heights 318) twice, under the old inactive id at stale population and under the active id of the same name and county, and the connections still carry the old id. The active row is the current record, and the same name and county is in the register itself. Using the stale rows (21,221 / 29,231 / 29,988 / 17,563) counts a population the register itself marks inactive. This is the design's D7 silent device on an ask, which the asks may carry. Other forks are closed by files: Hagestad Corners ended 2025-06-30 (excluded); emergency ties are not Full purchase.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 12 | yes |
| Formats | 3+ | 3 (csv, pdf, xlsx) | yes |
| Large file | 25,000+ rows | pfas_entry_point_results 36,414 | yes |
| Distractors | 2+ in metadata.json, none named in a file | national_pfas_survey_2023.csv, private_well_pfas_2024-2026.csv; file names do not label them | yes |
| Distractor behaviour | unused, weighable, not answering a graded quantity | thread: weighable, unused; neither yields a graded figure | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | grants to the dollar, Mgal one decimal, people whole, per county and per system | yes |
| Prompt shape / rubric 25+ | identifiable, 25+ criteria | per-system grants (20) plus counts, county cells and chart give well over 25 gradable items; the generated rubric itself is not in the folder, so the count is by item inventory, not verified | yes (by inventory) |
| Not LLM generated / realistic goldens | | thread: files read as agency artifacts, no toolchain tells | yes |

## Gate G reconciliation
Thread: mechanism decomposition_attribution, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note (## Three rules): "decomposition and attribution family", the decisive step is inverting the mixtures against the per-well average, flow-share average and solo-run average, with Layer 1 being the free-text sources, revisions, blanks and duplicates. These match. The declared distractors (national survey, private wells) were not named by the thread as the surface read carrying the task; the surface read it names is the per-well average, a method route and not a shipped wrong ranking. No sole data defect, and the thread found no artifact ranking the candidates wrongly. I did not find a mismatch on `stump_class`, `analyst_test` or `domain_test` (no card file was located under the paths I checked; I compared against the design note's Three rules only).

## Gate H line
domain: pass; layers: pass (L1 free-text sources, revision overlap, shared header meters, meter swap, renumbered ids; L2 source apportionment of each well's own PFAS from commingled samples); decisive_step: analytical. This agrees with the note's "Not semantics" and decisive-step lines.

## Stump power (Gate F)
Moderate to good. Mass-balance unmixing is the field's recognised method, and the plan's "own water" definition and the guide's sources-in-service field point toward it, so a strong solver who unmixes lands 16. The thread did not class this as a landable textbook call by itself: it requires parsing about 40 free-text source strings across 24 entry points, and three plausible averaging routes give 7, 8 or 11. The main thread should weigh the ladder against the note: this is not a case where the golden is reached by applying a standard method with no judgment, since the choice of estimand (own water against mixture) is the analysis. The asks add independent layers (shared header meters, renumbered ids, ended connection, cross-county buyers).

## Findings, ranked
1. None blocking.
2. Low: the Kesselring emergency-well reading on the water ask is closed only by the literal text ("the listed systems' wells"); a solver could import "active" from the chart sentence. One county cell (Hedstrom, 0.8 Mgal) is exposed; no change needed.
3. Note: the 2023 national survey and non-detect convention (half the reporting limit) are not stated in any shipped file; tested at 0, half and full limit, none moves the flagged set, any grant or the remainder.
4. Reship check: with the covering note and inventory Notes sheet gone, and the pump fact moved to the inventory `pump` column, nothing the main call needs became undefined. Capacity weighting is derivable from flow against rated capacity, and equal weights give the same 23 wells.

## Next action for the author
Proceed to ship the c38b7092 cut; no determinism repair is needed. Optionally re-run the leak check on this final cut (the `pump` column is new).

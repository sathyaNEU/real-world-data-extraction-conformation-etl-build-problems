# determinism-check report, task131, 2026-10-13

## Verdict
NOT_DETERMINISTIC (one supplementary figure, xlsx ask 3). The main recommendation and every other committed answer reproduce.
**Disposition:** SEND_BACK per the judge (the repair is a one-phrase prompt pin plus a data tweak, so FIX_NOW through /fix-determinism is the practical route).
**Stumping type:** mechanism: statistical_rigor (judge; design note says forecasting), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The ask says "the share of those answering the March 2026 survey who said they were likely or very likely to stay". The golden divides by households whose first submitted response has Q4 answered (231/244/233) and gives 55.4/45.9/60.1. A literal reader divides by everyone whose first response counts (238/253/241) and gets 53.8/44.3/58.1. I confirmed in the bundle that 24 of the 732 first submitted responses have a blank q4_stay, and the survey PDF never says a blank Q4 is dropped. The design note's Tried-and-rejected line says this was closed by making Q4 mandatory on submission, but the shipped CSV still carries 25 submitted responses with blank Q4. The fix did not reach the data.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Hot workdays | 7, 43.7 to 45.3 C | same (IDCJAC0010) | yes |
| Design A / B / C change to 214.6 MW | +5 / +20 / -11 | +5.095 / +20.045 / -10.991 | yes |
| Peak half-hour | B, C 8 pm; A 9 pm | same | yes |
| Table 1 (still on / back at request / left) | A 370;22;7 B 361;29;9 C 374;18;6 | same | yes |
| Table 2 (charged more; mean diff) | 123, -19.64; 45, -42.86; 52, -31.61 | same, to the cent | yes |
| Table 3 (share likely to stay) | 55.4 / 45.9 / 60.1 | 55.4 / 45.9 / 60.1 with Q4-answered denominator; 53.8 / 44.3 / 58.1 with all respondents | only under an unstated denominator |

## Competing answers that survived
1. Survey denominator: Q4-answered (55.4/45.9/60.1) against all first responses (53.8/44.3/58.1). Shipped rule meant to close it: Q4 mandatory on submission, which is not in the data.
2. Minor, not disqualifying: sign of the mean difference (the golden states "a negative difference a saving"); mean over all 400 households versus only those charged more. The design note says the prompt was changed to "per trial household", but prompt.txt still reads "per household". Check the note and prompt agree.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 | yes |
| Formats | 3 or more | csv, xlsx, pdf, NEM12, BoM csv | yes |
| Large file | 25,000 rows or more | NEM12 about 336k 300-records | yes |
| Distractors named in metadata.json, none in a file name | 2 or more | 3 (zone_substation_loads, rooftop_pv_connections, generation_availability), unused by the solution | yes (arithmetic check that one answers a graded quantity not rerun by me) |
| Deliverables | 1 to 3, all in golden | 2, both in golden/ | yes |
| Asks unit and rounding | stated | closing sentence states MW, dollars, percentages | yes |
| Rubric 25 or more criteria | 25 | not verifiable here; asks plus 3 critical components plus tables give plenty of gradable cells | not checked |
| Licence/provenance | recorded | metadata.json sources: synthetic, no licence restriction (the judge saw no licence field in the shipped file list) | yes in metadata |
| Reads as LLM generated | no | judge found no authoring leakage | yes |

## Gate G reconciliation
Judge: mechanism statistical_rigor, family analytical_non_defect, no surface-read dependency, no sole data defect. Design note: Gate G mechanism "forecasting", stump strategy "other" (non-linear planning maximum). The two agree on substance (heat-matched effect carried to the design day, maximum moving to a different half-hour); only the mechanism label differs, which is a label mismatch and not a build finding. The judge did not name any declared distractor as the surface read carrying the task. The easy route (all trial workdays) gives A -13.1, B -3.3, C -10.3, i.e. the wrong design A, matching the note's stump sentence in direction.

## Stump power (Gate F)
Strong. The pooled-days route files Design A (or B in-window only) and misses that the pull-down after the window raises the maximum under A and B. C is the only design that lowers it; the bootstrap 95% intervals are A [0.5, 10.0], B [14.8, 25.3], C [-14.9, -7.2]. Gate H: domain pass, layers pass, decisive_step analytical, consistent with the card and note's `## Three rules`.

## Findings, ranked
1. Survey denominator fork on xlsx ask 3 (fails Gate C/E); the note's fix is not in the shipped survey CSV.
2. prompt.txt and the design note disagree on "per household" against "per trial household"; pin the mean-difference population and sign.
3. Judge saw no licence field in the shipped file list; metadata.json carries it, so a pointer only.

## Next action for the author
Run /fix-determinism: either make Q4 present on every submitted response in the generator (as the note claims) or file the denominator in the prompt ("of those who answered that question"), keep 55.4/45.9/60.1 if the pin matches, rebuild twice byte-identical and re-judge once.

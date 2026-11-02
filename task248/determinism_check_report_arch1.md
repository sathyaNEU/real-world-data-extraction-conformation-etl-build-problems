# determinism-check report, task248, 2026-10-18

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated judge thread (sonnet, medium, scratch /tmp/determinism-check-task248-r1/, verdict.md there) recomputed every load-bearing figure from the bundle and reproduced all of them. The main call is 26 alert episodes on the shed load against 30 published (ADS, ADE, TRN, CLF, SLT -1; ADW +1). The only fork, whether the decay rate varies with temperature, is settled by the paired study (adding the temperature term cuts the residual sum of squares from 7.57 to 1.02, F = 637; pH and conductivity are inert). Every temperature-dependent route tried gives the same 26 and the same six moves. The constant-rate route gives 30.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Published episodes (dashboard basis) | 30 | 30; matches the 30 rows of the export's episode sheet | Yes |
| Shed-load episodes and moves | 26; ADS, ADE, TRN, CLF, SLT -1, ADW +1 | same | Yes |
| Decay fit (101 visits) | k20 0.050/h, theta 1.09 (restated after the run from 0.0503 and 1.088) | k20 0.05030, theta 1.0875 | Yes (see finding 2) |
| Seasonal losses (CLF, ADS) | CLF 0.69 / 0.31 log10, ADS 0.52 / 0.24 | consistent with the fit and the travel times | Yes |
| Constant-rate route | 30 | 30 (pooled k 0.0408/h, year-mean temperature) | Yes |
| Ask 3, 24 plants' hours without a valid inlet flow | e.g. ASD 60, ADS 13, PLH 70, UWD 52 | all 24 match | Yes |
| Ask 4, 24 plants' failing composites (total 71) | per submission | all 24 match | Yes |

## Competing answers that survived
None on the main call or the asks. Robustness the thread tried:
- theta 1.07 to 1.10, k scaled 0.5x to 2x, linear-in-temperature rate, plant-only or upstream-only temperature, monthly temperature, historian flow in place of the form's: all 26.
- Ask 4 is unchanged under valid-hour mean x 24, valid-hour sum, a 364 to 366 day window, and an inclusive window end.
- Ask 4 changes only if the contract-laboratory composites are dropped or the unit is misread by 10x, both closed by shipped text.
- Ask 3 has a minor wall-clock reindex fork (finding 1).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 (metadata.json and the unzip; the thread miscounted 15) | Yes |
| Formats | 3 or more | 5 (csv, eml, md, pdf, xlsx) | Yes |
| Large file | 25,000 rows or more | historian 475,268 rows | Yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | rain gauges, EQA returns; neutral file names | Yes |
| Distractor weight | unused by the solution, relevant enough to weigh, ruled out by a shipped fact | unused (confirmed by the thread); relevance is weak, since neither could answer a graded quantity | Pass, weak (finding 4) |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, docx), both in the golden; no format family required | Yes |
| Asks | multi-dimensional, unit and rounding stated | 24-row per-plant cuts; "whole numbers" in the prompt; the unit is in each asking phrase | Yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 03; 24 + 24 per-plant figures, totals and moves give well over 25 | Yes |
| Not LLM-looking, goldens realistic | | thread found no authoring disclosure; layer 1 mess is organic; golden realism not reassessed here | Yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no.
Design note and card: stump_class analytical, layer2_family field_method, decisive step "fit k(T) = k20 theta^(T-20) and restore each composite at its own inlet temperature over the travel time", easy route 30, no decoy, `official_decoy` false, `decisive_rule_filed` false.
These agree. The thread named no declared distractor as the surface read. Rain and EQA are unused, and the thread's easy route is the constant-rate answer, which equals the published count. No shipped artifact counts episodes on the shed load, since the dashboard export is the declared context artifact on its own basis. Gate G is clean.

**Gate H line (thread):** domain: pass, layers: pass, decisive_step: analytical.
The design note's `## Three rules` agrees (swap test fails to transplant, Layer 1 is the run, flow, unit and clock mess, Layer 2 is the temperature-dependent decay). The card's analyst_test and domain_test agree.

## Stump power (Gate F)
The thread rates it moderate to high. The constant-rate and PMMoV-ratio routes land on 30 with no plant moving, and the seasonal fit step carries the call. Asks 3 and 4 add independent hazards (DST and held runs; the contract-laboratory unit and window).

## Findings, ranked
1. Minor, ask 3: a solver who reindexes to 8,784 wall-clock slots counts the non-existent 02:00 on 26 Sep 2027 and gets +1 at all 24 plants. The golden counts real hours. The historian note never mentions the skip. The prompt now carries the real-hours definition only in the golden's step 7, so the optional pin is "real local hours". It is not blocking, since it is Layer 1 and the repeated 02:00 on 4 Apr 2027 shows the clock.
2. Informational: theta is 1.0875, on the 1.087/1.088 edge. The write-up was restated after the thread at the precision every fitting route prints (0.050 an hour at 20 degrees, about 9 per cent a degree, theta 1.09). I confirmed `submission.md` lines 18 and 26 carry this. No graded figure, file or answer changed, and `target.zip` sha256 is still 4733488b15715caba85a8fe2484b813a5ec40d8874094c9de18dbe9ba20ca0b4. The restatement came after the judged text, so the critical component the thread saw read 0.0503 and 1.088.
3. Informational: the temperature dependence of the decay is not named in the methods note, and the data force it (F = 637). This is analysis, not a hidden rule. Ask 4's reliance on the contract-laboratory unit is data semantics at the ask level, which the spec allows.
4. Minor: the distractors are relevant to the sewer's season (rain) and the laboratory's quality (EQA) but neither could produce a wrong graded figure, so they weigh weakly.

## Next action for the author
None required to ship. Optionally add "real local hours" to the ask 3 wording of `prompt.txt` (needs the prompt length and voice-check re-run, so only if you accept the churn).

# determinism-check report, task246

# Pass 1, 2026-10-18 (first cut; superseded by pass 2 for the shipped bundle)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (etl_conformance supporting), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Gate G: pass (no shipped artifact ranks the zones on the note; the June bulletin, market prices and rainfall are the declared distractors, none answers a graded quantity). Gate H: domain: pass, layers: pass, decisive_step: analytical.

## Why
One isolated judge thread (sonnet, medium) saw only a fresh unzip of target.zip and the inlined blocks. Every committed answer reproduced from the bundle: seven noted zones, all 12 zones' figures, response rates, crude and under-five death rates. Count of 7 holds under every standard variant that removes the anthropometrists' random error (smallest noted gap 2.7 to 2.8, largest un-noted gap 1.4, East Riverine). Thread: /tmp/determinism-check-task246-r1/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Offsets, 13 anthropometrists (mm) | -2.5 ... +3.9 | within 0.1 (teams workbook, standardisation files) | yes |
| Departure SDs about offset | 2.1 to 5.7 | same with n-1 form; repeat SDs 1.06, 1.51, 0.88 | yes |
| Readings' figure, 12 zones | 4.8 to 17.6 | matches | yes |
| Children's own figure, 12 zones | 4.4 to 14.6 | matches within accepted ranges; Central Pastoral 10.5 (n) or 10.6 (n-1) | yes |
| Note differences | +4.7, +2.8, -3.4, +4.4, +5.6, +3.0, +2.9 | -3.3 or -3.4 for Central Pastoral, rest as claimed | yes |
| Household response, 12 zones | 94.8 to 97.9 | all 12 | yes |
| Crude death rate, 12 zones | 0.40 to 0.84 | all 12 (cluster 202 de-duplicated on cluster/hh/line) | yes |
| Under-five death rate, 12 zones | 0.50 to 2.11 | all 12 | yes |

## Competing answers that survived
- Offset only, or repeat-error (TEM) as the random error: 4 zones (North Pastoral, Central Pastoral, Laga Town, East Pastoral). The protocol (section 7) says the children's-own figure is taken "at the round's standard" and files no way of estimating random error. The thread judged the data forces the golden (the standard is defined as departure from the supervisor, and three anthropometrists repeat within 1.5 mm yet depart by about 5.5 mm), and found no defensible case for 4. Residual wording exposure only (Gate C/E, minor).
- Mean squared departure (counts the offset twice): 8 zones, adds East Riverine. Wrong by construction.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | csv, xlsx, pdf, eml, md | yes |
| Large file | 25,000 rows or more | lr2027_household_members.csv, 26,198 rows | yes |
| Distractors | 2 or more, in metadata.json, none labelled by file name | 3 named (June bulletin, market prices, rainfall); file names neutral | yes |
| Distractor weight | unused by solution, weighs, ruled out by a shipped fact | bulletin gives community screening shares and says they are not comparable with the round; none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 4 asks over 12 zones, units and rounding in the prompt | yes |
| Prompt | one paragraph, under 1,000 chars | prompt.txt 739 bytes, one paragraph, question first | yes |
| Rubric size | 25 or more criteria | about 36 graded figures plus the count, zones and chart (design note) | yes |
| Reads as real | no LLM tells, goldens real | thread found no authoring leakage; golden realism not re-judged here | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: declared decisive step is the error taken as the variance of single readings' departures from the supervisor about the offset, rather than repeat TEM (4 zones) or no random error; the note's analyst test (offset out, TEM squared out, 4 zones) matches the thread's rivals. No mismatch. No distractor carries the task; the thread named none as the surface read.

## Gate H (three rules)
domain: pass, layers: pass, decisive_step: analytical. The design note's Not rule application line says the protocol files the estimand and the reference but no way of estimating a measurer's error; the thread agrees the method is not stated and finds the data, not a filed rule, separates it.

## Stump power (Gate F)
Good. A strong analyst who cleans everything and applies offsets lands on 4 (missing North Lakeshore, West Pastoral, West Riverine) or 8 with the squared shortcut. No signal in the protocol or bulletin names the variance construction.

## Findings, ranked
1. Gate C/E, minor: the protocol never says the children's-own figure is net of random error as well as offset, so a literal offset-only solver files 4. The data separates the candidates, so this is wording exposure, not a fork the data leaves open. Optional one-clause pin in protocol section 7 (WHAT, not HOW, is borderline: say "net of the measurers' error against the supervisor", not the formula).
2. Optional: state or keep the accepted range for the SD convention (Central Pastoral 10.5 or 10.6).

## Next action for the author
Proceed to ship. Optionally decide on the finding 1 clause; if added, rebuild twice byte-identical and do not re-judge unless the design changes.


---

# Pass 2, 2026-10-18 (final rebuild after the stage 4 realism repair)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Gate G: pass. Gate H: domain: pass, layers: pass, decisive_step: analytical.

## Why
One isolated judge thread (sonnet, medium) saw only a fresh unzip of the final target.zip and the inlined blocks. Thread: /tmp/determinism-check-task246-r2/verdict.md. It recomputed the call and every graded figure from the bundle: seven noted zones (North Pastoral +4.0, North Lakeshore +4.1, Central Pastoral -3.8, Laga Town +5.2, East Pastoral +5.1, West Pastoral +2.9, West Riverine +4.5); the largest un-noted gap is East Riverine at 1.5. Margins to the 2.0 threshold are 0.9 on the noted side and 0.5 on the un-noted side. The repair moved the figures but not the structure.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Readings' figure, 12 zones (after team 2 duplicate drop, 75 to 220 mm rule, PRK cm to mm) | 5.2 to 18.2 | all 12 exact | yes |
| Offsets, 13 anthropometrists | -4.0 to +3.7 | match (Titus -2.15, Sharon -4.0, Albert +3.7) | yes |
| Departure SDs about offset | Steve 5.8, Joan 5.1, Cosmas 6.3, rest 1.9 to 2.9 | match (n-1) | yes |
| TEM of the scattered three | 1.7, 1.2, 1.0 | 1.73, 1.22, 1.02 | yes |
| Children's own figure, 12 zones | 4.5 to 14.5 | all 12 match golden centres, inside accepted ranges | yes |
| Household response, 12 zones | 94.8 to 97.9 | all 12 | yes |
| Crude death rate, 12 zones | 0.40 to 0.84 | all 12 (cluster 202 deduplicated, 3/4 swap before 21 June, births-module deaths) | yes |
| Under-five death rate, 12 zones | 0.50 to 2.11 | all 12 under the literal mid-point formula | yes |

## Competing answers that survived
- Offset only, or TEM as the random error: 4 zones (North Pastoral, Central Pastoral, Laga Town, East Pastoral). The data separates it (the scattered three repeat within about 1.7 mm but depart from the supervisor by 5.1 to 6.3 mm), so it is the stump, not an open fork.
- Mean squared departure: 8 zones, adds East Riverine. Wrong by construction (counts the offset twice).
- Departure variance with n or n-1: the same seven.
- Residual, low severity: (1) the estimator of the children's own figure is unfiled, which moves some figures by 0.1 to 1.0 point and is covered by the accepted ranges; the note decision does not move. (2) The U5 treatment of 19 born-and-died newborns shifts 5 of 12 U5 figures by 0.01 under a death-only reading (Central Pastoral 1.84 against 1.85, East Agro-pastoral 1.89, North Agro-pastoral 2.10, Laga Town 1.10, West Riverine 1.69); the literal section 9 text gives the golden.

## Spec gates (checked by me on the unzipped bundle and the folder)
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | csv, xlsx, pdf, eml, md | yes |
| Large file | 25,000 rows or more | lr2027_household_members.csv, 26,198 rows (wc confirms 26,199 lines with header) | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | 3 named (June bulletin, market prices, rainfall); names neutral | yes |
| Distractor weight | unused, weighs, ruled out by a shipped fact | bulletin gives CHV screening shares and says they are not comparable with the round; none answers a graded quantity; the thread named none as the surface read | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 4 asks over 12 zones; the prompt gives units and rounding (the wasting and response figures in per cent to one decimal, the death rates per 10,000 a day to two) | yes |
| Prompt | one paragraph, under 1,000 chars | prompt.txt 739 bytes, question first | yes |
| Rubric | 25 or more criteria | 36 household and wasting figures plus count, zones and chart (design note) | yes |
| Reads as real | no LLM tells | thread found no authoring disclosures; README is a file index; golden realism not re-judged here | yes |

## Gate G reconciliation
Thread: statistical_rigor, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: decisive step is the variance of single readings' departures from the supervisor about the offset, against TEM (4 zones) or no random error; metadata.json's distractors are the bulletin, prices and rainfall. They agree, and no distractor carries the task. No mismatch.

## Gate H (three rules)
Thread: domain pass, layers pass, decisive_step analytical. The design note's Domain test, Layer 1, Layer 2, Not semantics and Not rule application lines match: Layer 1 is the partners' unit and age encodings, the duplicate send, the form-code swap and the anthropometrist change; Layer 2 is the measurement-error correction against the reference. No mismatch.

## Stump power (Gate F)
Good. A strong analyst who cleans correctly and reads every rule takes the offset out and the TEM squared out, and files 4 zones (misses North Lakeshore, West Pastoral and West Riverine); the squared-departure shortcut files 8.

## Findings, ranked
1. Low, stale design note: the Analyst test line still quotes the first cut's gaps for the four-zone route (3.3, -4.2, 4.6, 4.7). The shipped bundle's four-zone route gives different gaps, and the call is unchanged. Refresh the numbers from checks.py; no data change and no rejudge.
2. Low, unchanged from pass 1: the estimator of the children's own figure is unfiled. The data separates the candidates and the accepted ranges cover the spread. Keep the ranges in the rubric.
3. Low: accept 0.01 slack on the five U5 figures for the born-and-died convention (optional).

## Next action for the author
Ship. Optionally refresh the stale gaps in the design note's Analyst test line; no rebuild and no re-judge are needed.

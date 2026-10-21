# determinism-check report, task252 (architecture 2), 2026-10-21

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: other (latent measurement-error identification: lagged-regression carryover, zero/span split, flush event-study, with ETL-conformance asks), stumping_family: analytical_non_defect (borderline), surface_read_dependency: no (borderline), sole_data_defect: no (borderline)

The judge ran as one isolated sonnet thread on the prepared brief. Its verdict is at /tmp/claude-0/-home-user/ae71c25a-4beb-538a-9fe7-971dc23fc641/scratchpad/t252a2s4/judge/verdict.md. This report replaces the architecture 1 report.

## Why
Every committed figure reproduced from the shipped bundle alone. The six flagged channels are BRN-FW1, CAL-FI1, DUN-FW1, ELS-FW1, GAR-FI1 and GAR-FW1. They come from three separable instrument effects: port carryover, the zero or span calibration error, and the filtered sample-line loss that regrows after each monthly flush. Every flagged channel is 0.009 or more off, and every other channel is within 0.004 of zero, so the 0.005 line sits in a gap. Asks 2 and 3 reproduce for all eight plants. Each rests on one inference the files force (see the forks below).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Carryover share BRN / DUN / ELS / GAR / HOL (1 and 2 slots back) | about 7% and 2% | .072/.019, .079/.020, .076/.021, .066/.019, .070/.020 | yes |
| Carryover share ASH / CAL / FEN | under 1% | .006/-.001, .003/.002, .004/-.001 | yes |
| Carryover offset BRN-FW1 / DUN-FW1 / ELS-FW1 / GAR-FI1 / GAR-FW1 | each 0.006 or more | +0.0115 / +0.0123 / +0.0091 / +0.0266 / +0.0112 | yes |
| Carryover offset HOL-FI1 / HOL-FW1 | cancelled by line loss / zero error | +0.0254 / +0.0077 | yes |
| Holmedale zero error | 0.008 low at every level | check mean 0.0920; raw lab minus online -0.0071 (a span error would predict -0.029) | yes |
| Calderwood span error | about 8% low | check mean 0.0916 (-8.4%); raw difference -0.052 (span predicts -0.042, zero error -0.008) | yes |
| Other six analysers' check means | within 0.002 of 0.100 | .0996, .1011, .0993, .1002, .0996, .1008 | yes |
| CAL-FI1 / HOL-FI1 rise at flush | 0.009 to 0.011 / 0.018 to 0.020 | +0.0102 / +0.0195 | yes |
| Other channels' flush rise | none | at noise | yes |
| Regrowth time | 2.0 days | grid fit 2.00 for both | yes |
| Line loss over quarter CAL / HOL | 0.010 / 0.019 | 0.0104 / 0.0192 | yes |
| CAL-FI1 total | 0.007 or more below | -0.0104 | yes |
| HOL-FI1 total | within 0.004 | -0.0018 | yes |
| Other unflagged totals | within 0.004 | ASH-FI1 -0.0005, ASH-FW1 +0.0010, BRN-FI1 +0.0003, CAL-FW1 -0.0008, DUN-FI1 -0.0002, ELS-FI1 -0.0002, FEN-FI1 -0.0005, FEN-FW1 +0.0006, HOL-FW1 -0.0003 | yes |
| Flagged list (six) | as above | same six: +0.0116, -0.0104, +0.0122, +0.0091, +0.0268, +0.0113 | yes |
| Ask 2, lab holding time over 24 h (Ash, Bra, Cal, Dun, Els, Fen, Gar, Hol) | 14, 9, 8, 12, 11, 13, 14, 11 | same | yes (needs the +1 h shift on `analysed` and de-duplication) |
| Ask 3, fixed-dose hours (same order) | 31.2, 27.8, 35.8, 32.2, 26.7, 34.8, 31.3, 29.3 | same | yes |
| Ask 4 PNG | six marked | not checked by the judge (golden outside its access) | n/a |

## Competing answers that survived
No fork survives that moves the main call. Two soft forks sit on the asks, and the shipped data closes both.
- **Ask 2, clock of `analysed`.** The dictionary says "NZ time" for collected, received and released but is silent on `analysed`. Read with no shift, the total is 69 instead of 92. The files force a shift of 53 to 64 minutes: 16 rows have `analysed` before `received`, and no result is released within 64 minutes of its stamp. Every shift in that window gives the golden counts. The 7 December duplicate rows must be dropped, otherwise each plant is 2 higher. A solver who takes the stamp at face value files wrong counts. This is a Layer 1 clock issue on an ask, not the stump. The judge would not send it back and offers an optional pin: state `analysed` as "laboratory run record, instrument clock".
- **Ask 3, availability rule.** The PLC reads the analyser directly and the historian is downstream. A historian-only reading gives 38.2, 34.8, 42.3, 38.7, 32.7, 40.8, 38.3, 36.3. Counting every F row as unavailable gives 34.2, 30.8, 38.3, 34.7, 28.7, 36.8, 32.8, 32.8. Only the golden fits the process summary's telemetry description and the dictionary's fill and missing-slot notes. Counting the check slots as available changes no plant.
- Wrong lists on the main call all fail:
  - Raw historian plus PASS checks flags HOL-FI1, HOL-FW1 and CAL-FI1 and misses the five carryover channels.
  - Correct carryover without line loss wrongly flags HOL-FI1 and drops CAL-FI1.
  - Mixing up zero and span error wrongly flags HOL-FW1 or CAL-FW1.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 10 | yes |
| Formats | 3 or more | 5 (csv, xlsx, pdf, eml, md) | yes |
| Large file | 25,000 or more rows | nh3_online_readings 106,100 rows | yes |
| Distractors | 2 or more, named in metadata.json, no file name labels one | plant_daily_output_2027Q4.csv and catchment_rainfall_daily_2027Q4.csv named in metadata.json; neither file name labels it | yes |
| Distractors unused and relevant | unused by solution, relevant enough to weigh, a ruling-out fact shipped | both are unused by any answer; the judge found no sign that either reproduces a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png) | yes |
| Asks | multi-dimensional, unit and rounding stated | 16 channels, 8 plants by 2 items; hours to one decimal; counts are whole numbers | yes |
| Prompt shape and rubric of 25 or more | identifiable shape, 25 or more criteria | shape 07 per metadata; 16 channel flags plus 16 per-plant values plus chart items exceed 25 | yes (criteria count inferred, not generated here) |
| Not LLM generated, goldens real | no authoring language | judge found none; real-looking noise throughout | yes |

## Gate G reconciliation
Judge: mechanism other (latent measurement-error identification), stumping_family analytical_non_defect (borderline), surface_read_dependency no (borderline), sole_data_defect no (borderline).

Card and design note: `stump_class: analytical`. The easy path is carryover plus zero and span, flagging HOL-FI1 and leaving CAL-FI1 at about +0.001. The stump is the filtered-line loss read from the recovery after each monthly flush. The judge independently reached the same easy-route result: correct carryover without line loss flags HOL-FI1 wrongly and drops CAL-FI1.

The two readings match. The PASS checks are named as the misleading surface read, but they do not carry the task. Neither declared distractor (plant output, rainfall) carries any weight. No finding of a too-load-bearing distractor. The "borderline" labels stem from the judge's worry that three stacked corrections can look like a defect chain. The design note's reply is that nothing is planted and the maintenance log records visits only, so I read it as an estimation task and not a send-back risk.

## Gate H line
`domain: pass`, `layers: pass`, `decisive_step: analytical`

This agrees with the card's `analyst_test` and `domain_test` and the design note's `## Three rules`. The decisive step is not a field reading or an executed rule. A strong analyst who cleans the data and reads every document still files the wrong list unless they join the maintenance log to the readings.

## Stump power (Gate F)
High. Three independent chances to err sit on the main call: the PASS checks, the missing line loss, and zero versus span. Asks 2 and 3 add two more (the clock shift with de-duplication, and the PLC-versus-historian availability reasoning). The data dictionary documents the fill and missing-slot rules, and the log says "sample lines flushed", but neither names the effect. The line-loss method is not filed, which is consistent with the rule of filing the WHAT and not the HOW. The textbook-route caveat does not apply: the judge reached the golden by identification from the data, not by applying a standard method with no judgment.

## Findings, ranked
1. Ask 2: the `analysed` clock is unstated. The files force the answer (53 to 64 min), but a literal reading gives 69, not 92. The judge classed it determinate by evidence and not a send-back. The optional pin in the dictionary is cheap and does not move the stump.
2. Ask 3: the availability rule rests on inference from the process summary. Determinate, and the golden is the only consistent reading.
3. Minor hygiene: the dictionary is "revised 3 November" yet describes a December export.
4. Not verified by the judge: Ask 4 (the PNG), the metadata.json distractor naming (checked by me: present), and the cross-batch comparison.

## Next action for the author
No repair is needed. Optionally add the one-line clock note for `analysed` to water_services_data_dictionary.md, and if so rebuild and re-run the free gates. Otherwise proceed to ship.

# determinism-check report, task461 architecture 3, 2026-11-04

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (one prompt precision fix, no redesign; the judge thread said APPROVE)
**Stumping type:** mechanism: etl_conformance (metering hierarchy), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no (borderline)

## Why
The thread recomputed every load-bearing value from the unzipped bundle: import 3,477.30 MWh, tenancy supplies 1,562.35, base building 1,914.95 (1,915), Scope 2 396.49 t (396.5), KPI 18.476 (18.5), miss 0.9. It also reproduced the quarterly gas oil (570, 317, 318, 448 L) and the four chiller releases. No competing answer survived. The only wrong route that flips the call is subtracting all 13 tenancy-labelled meters (15.9, "met"). The thread's source for the nesting is the half-hourly registers: 0 exceedances of a parent in 17,596 intervals, and zeros matching the 13 June isolations.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Import 2026 | 3,477 MWh | 3,477.30 | yes |
| Tenancy supplies (9) | 1,562 MWh | 1,562.35 | yes |
| Base building | 1,915 MWh | 1,914.95 | yes |
| Months | 158 ... 154 | 158.2, 144.5, 156.2, 141.2, 150.1, 175.8, 189.7, 174.3, 166.2, 153.2, 151.8, 153.8 | yes |
| Scope 2 | 396.5 t | 396.49 | yes |
| KPI | 18.5, 0.9 over | 18.476, 0.876 | yes (0.9 equals 18.5 minus 17.6) |
| Gas oil Q1 to Q4 | 570 / 317 / 318 / 448 L | same | yes |
| Refrigerant CH-1 to CH-4 | 10.8 / 20.7 / 14.8 / 20.5 kg | same | yes |

## Competing answers that survived
None on the call. Two presentation notes:
- The twelve rounded months sum to 1,914 against the 1,915 annual. The design note's SF16 closes this (annual from unrounded months).
- Prompt rounding gap for Scope 2 (see Spec gates and Fix).

## Spec gates (checked by me against the bundle)
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / size | 10+ files, 3+ formats, 25,000+ rows | 13 files; csv, xlsx, pdf; BMS CSV 281,585 rows | yes |
| Distractors | 2+ in `metadata.json`, none labelled by file name | met_wexmoor_daily_2026.csv and pellow_house_epc_2024.pdf; neither name labels it | yes |
| Distractors unused yet weighable | yes | The EPC's 27,940 m2 would give a different KPI but is ruled out by schedule 1.5 (21,460). Weather is unused. | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, pdf), both in golden/ | yes |
| Asks multidimensional, unit and rounding stated | every ask | Scope 2 "in tonnes" has no decimal places; every other ask is pinned | NO |
| Prompt shape and 25+ criteria | identifiable, 25+ | shape "other", but the card gives 16 ask figures plus the call and components; I cannot count the generated rubric. Author to confirm at least 25. | unverified |
| Prompt form | under 1,000 chars, one paragraph, no counts | 986 chars; no counts | yes |
| No LLM tell, no em dashes | | none found in prompt or submission | yes |

## Gate G reconciliation
- Thread: etl_conformance, analytical_non_defect, no surface-read dependency, sole_data_defect no.
- Card: `gate_g` etl_conformance, `stump_class` analytical, `official_decoy` false.
- These match. The thread does not name either declared distractor (weather, EPC) as carrying the task. The EPC area is a possible wrong-denominator route, but it still files a miss and is closed by SF3.

Gate H line from the thread: domain pass, layers pass, decisive_step analytical. The card agrees (`layer2_family` estimand_identification).

**The semantics question, answered plainly.** The card's `analyst_test` and the note's `Not semantics` line do not fully answer it. They are weaker than they read, for three reasons:
1. `analyst_test` says "nothing asks whether one tenancy meter sits inside another". Schedule 1.4 does ask the question: it subtracts the electricity supplied to the Tenancies "as metered at each Tenancy's supply". The tenancy schedule lists nine occupied or licensed tenancies, and the meter register carries the same occupier on EM-101 and EM-102, EM-104 and EM-105, EM-107 and EM-108.
2. The register names the supply and the room separately: "L1-L2 tenancy supply" against "L2 comms room". A reader of the labels alone can reach the nine supplies. Both sentences in the note ("no field, code, unit or label records the hierarchy"; "the names mislead both ways") are too strong. The labels do not mislead on the three nested rooms. They mislead only on the roof licensee's EM-114, which is rung 1.
3. What the data adds is confirmation of the nesting, and EM-114's independence. That is a real analytical step: containment and zero-with-parent. But it checks an inference the filed text and labels already point to.

So a reviewer could class the nesting as data semantics or rule application ("one supply per Tenancy"). The thread judged it analytical because the register cannot tell you, only the counters. I would not call it decisively either way.

Mitigating points. A strong analyst who skims the labels does land on the 15.9 route, and the card says rung 0 is the field's reflex. The note's case for the data-derived hierarchy is genuine. My recommendation is not to redesign, but to be ready for a rule-application finding at the portal. The wording to tighten is "nothing asks" in the card and the "no label records" claim in the note, to state what is true: the labels name the rooms, but only the counters show containment and EM-114's independence.

## Stump power (Gate F)
Moderate. The call flips only on the nesting. A careful solver who counts nine tenancies against nine "tenancy supply" labels may land the call without testing increments, which weakens the stump. EM-114 (the roof licensee) is the part that needs the data. The thread's note that the nesting is real topology, not a planted defect, holds. The main thread should weigh this against the note's ladder.

## Findings, ranked
1. Prompt: Scope 2 "in tonnes" has no decimals, yet the golden is 396.5 t and 396 would be a tolerable literal reading. Pin it. The prompt is 986 of 1,000 characters, so trim words elsewhere to fit "to one decimal" (about 15 characters).
2. Card `analyst_test` and note `Not semantics`: overstated, as above. Reword.
3. Rubric count: confirm 25 or more criteria.
4. Optional: footnote in the workbook that the annual is rounded from unrounded months (1,914 vs 1,915).

## Next action for the author
Change the prompt to "Scope 2 emissions in tonnes to one decimal", stay under 1,000 characters, and run `voice-check.py`. Then rebuild twice for byte-identical output and re-run figures_check. No other golden figure moves. A second judge pass is not needed unless you change more than the rounding words.

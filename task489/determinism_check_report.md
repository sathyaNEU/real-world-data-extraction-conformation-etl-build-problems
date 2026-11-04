# determinism-check report, task489, 2026-11-04

## Verdict
NOT_DETERMINISTIC
**Disposition:** SEND_BACK (the thread's label; read against the gate table below, this is a main-call repair in the data, not a spent architecture)
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread order: kept (derivation.md on disk before graded_blocks.md was opened). Its derivation differed from the submission on one point only, the plunger-well separators (11 pads against 8). Everything else matched exactly.

## Why
The main call turns on one modelling step no shipped file states: how an uncounted plunger-well separator dumps when a slug exceeds its level band. The golden says one dump per slug at or above the band, with smaller slugs accumulating to the band. The literal reading, liquid over band (the method the five SCADA counters validate), puts Elmworth 12-15, Elmworth 5-3 and Kakwa 8-10 at 0.57, 0.64 and 0.70 t, so 11 pads convert instead of 8. All five counted separators are flowing wells, so nothing in the bundle calibrates a plunger-well separator. MRS-03 2.4 defines a dump cycle only as one opening and closing of the dump valve. "Slug" and "surge" appear in no file. The shipped dump-valve capacities (1.8 to 7.9 m3/h) and the logged afterflow_min (about 5 to 45 min) point toward several dumps per slug, the liquid-over-band answer. Only an instantaneous-surge assumption from outside the package supports one dump per slug. The design note's own Three rules line says "The ruling-out is silent", which is the Gate B/C failure stated as intended.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Counted cycles (5 counters, 16-bit wrap at 65,536) | per submission | K5-1 #1 19584, K6-27 #1 51914, E6-17 21178, K11-22 58697, K16-23 47178 | yes |
| Flowing-well controller kg (e.g. 662, 863, 952, 618, 412) | per submission | same | yes |
| Pad tonnes, K3-9, K11-22, K14-16, K6-27, K16-23, K1-14, E14-24 | per submission | same | yes |
| Plunger no-arrival cycles, 25 wells | per submission | same, from counter deltas per controller segment (total 17,211) | yes |
| Sales gas PC by maker and area: 518 / 256 / 380 / 427 kg | per submission | same | yes |
| E12-15, E5-3, K8-10 pad t | 0.37 / 0.40 / 0.24 | 0.57 / 0.64 / 0.70 under liquid over band; 0.37 / 0.40 / 0.24 only under one dump per slug | NO (fork) |
| Pads converted | 8 | 11 (liquid over band); 8 (slug reading); 14 pads change under one dump per arrival | NO (fork) |
| E10-11, E7-2 pad t | 0.71, 0.64 | 0.79, 0.78 under liquid over band (still in the set either way) | fork, call-neutral |

## Competing answers that survived
- **Plunger-well separator dump rule.** Liquid over band: 11 pads. Slug-sized replay (golden): 8 pads. One dump per arrival everywhere: also differs (K16-23 0.84, K13-22 0.65, E4-27 0.63, E9-34 0.61 go over). No shipped file rules out the first; the valve capacities and afterflow data favour it.
- Readings ruled out by shipped words: survey rate times hours (MRS-03 4.2 and 4.3), naive counter end minus start (negative for K11-22 and K16-23, wrap evident), condensate-only (contradicted by the counters, about 40 percent off), host NO ARRIVAL rows for ask 3 (11,574 against 17,211; PCX-300 sheet says counters are not reset and cycle_count steps by 2).

## Spec gates
Checked against the unzip at /tmp/determinism-check-task489-810032/target/, with the thread's file hygiene pass and metadata.json read after it returned.
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, docx) | yes |
| Large file | 25,000 or more rows | plunger_cycles_2026.csv, 240,855 rows | yes |
| Distractors | 2 or more, named in metadata, none labelled in a file name | 4 named (ogi_leak_survey, tank_vent_measurements, volumetric_adjustments, allocation_runs); gas-only, so unused by the liquid solution; no file name labels one | yes |
| Distractor relevance | weighs, reproduces, ruled out by a shipped fact | pneumatic-adjacent but outside MRS-03 4.5 or gas-only; none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pptx), both in submission | yes |
| Asks | multi-dimensional, unit and rounding stated | 4 asks (51 controllers, 26 pads, 25 wells, 4 maker-area cells), units and rounding in the prompt | yes |
| Shape and rubric | identifiable, 25 or more criteria | shape other; 26 pads + 51 controllers + 25 wells + 4 cells + deck | yes |
| Reads as real | no LLM tells, goldens realistic | thread found no authoring leakage; golden realism not re-judged here | yes |
Gates B and C (main call) fail; they are not spec gates and are in the Why.

## Gate G reconciliation
Thread: mechanism method_or_model_selection; family analytical_non_defect; surface_read_dependency no; sole_data_defect no. Card: stump_class analytical, layer2_family field_method, official_decoy false, validated_decoy false. Match. The thread names no declared distractor as the surface read, so no too-load-bearing finding. Gate G passes: deleting every wrong number leaves the same slug-against-band problem.

Where thread and design differ is not the family but the evidence. The card's analyst test says the five counters confirm liquid over band to within 1.8 percent and that a slug "empties the band in one dump". The thread agrees on the 2 percent, but treats the counters as supporting the default path on the plunger wells too, and finds the valve and afterflow data point the same way. The design's "snap-acting, one dump per slug" is physics from outside the bundle.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. Matches the card (analyst_test, domain_test) and the note's Three rules. The step is analytical in kind (slug against band is what an emissions engineer estimates) but unpinned.

## Stump power (Gate F)
The thread says a strong model would plausibly take the liquid-over-band route. That is the intended wrong route, but because it is itself defensible the miss would not be a clean analytical error. The Layer 1 mess (host label lag, re-sends, rollover, renumbered tags) is cleared by careful reading and carries no stump. The thread does not class the decisive step analytical because the golden is the field's standard method; here the golden is not a standard route the files confirm, so no landable-call discount applies. The main thread should weigh Gate F again after the data repair.

## Findings, ranked
1. Gate B and C, main call: plunger-well dump rule unfiled and uncalibrated, 11 pads against 8. Blocks the ship.
2. Contrary shipped evidence: dump-valve capacities and afterflow_min favour multiple dumps per slug; the repaired generator must make the new counters consistent with them.
3. Near-tie on rounding: Kakwa 12-36 #2 sits 0.029 kg below the 5.5 kg line (5.471 kg). Kakwa 13-22 #3 is 6.449. A solver who rounds the band volume or a constant can flip a controller kg. The pad lines are clean (Elmworth 14-24 is 0.088 t under, Kakwa 1-14 is 0.12 t over). On liquid over band, E5-3 #3 (186.516) is 0.016 kg above its line. Ask 3 boundary counts may move by one if a row is lost at a boundary.
4. Cross-batch duplicate check not possible from inside the allowed path; not reported.

## Disposition read against the gate table (determinism-check section 6)
- Failed gates: B (missing input: the decisive fact, how a plunger slug loads a separator, is not shipped) and C (underspecified_objective). Gates A (figures recompute), D, E and the spec gates pass; G and H pass; F is reopened by the repair.
- Architecture: not spent. The table sends back on G and H, the two that say the build is the wrong build; neither failed, and the thread's own Gate H says analytical.
- This is a main-call repair in the data (thread fix class input_files), not an ask-layer wording fix, because the failure sits on the recommendation's decisive step. It moves the pad set's evidence, so the judge's pack-scope rule applies: the repaired pack needs the one re-judge. Asks 3 and 4 need no change.

## Weighing the thread's fix
Fix: ship SCADA dump counters on two plunger-well separators, one with slugs above its band and one with slugs well below it.
- **Stays analytical.** Yes, if shipped as data and not as a rule. A counter file is a calibration organ (physical_verification), like the existing five. The solver must still relate each well's slug (day's liquid over arrivals) to its separator's band, build the count per separator, and extend it to the uncounted plunger separators. Nothing files the HOW. A strong analyst who cleaned the data and read every rule could still file 11 by validating only on flowing wells.
- **What a solver who validates liquid over band against all seven counters sees.** Five flowing counters agree within about 2 percent. On the big-slug separator, the counter reads near the arrival count and liquid over band overcounts it by roughly the slug-to-band ratio (about 2 to 3.5 times). On the small-slug separator, the counter agrees with liquid over band and one dump per arrival overcounts it by a large factor. So the first counter breaks rung 1 and the second breaks rung 1b, and together they pin the slug replay. That closes Gates B and C, as the fix intends. Cost: the step becomes discoverable, so the ladder and Gate F must be argued again for a solver who does validate on all seven. A solver who skips validation still files 11.
- **Design cautions.** Put the two counters on separators whose pads do not decide the call, otherwise those pads become counted by SF7 and the decisive step shrinks; and keep valve capacity and afterflow consistent with the new counters.
- **Filing the slug behaviour in MRS-03 or a data sheet.** The thread is right that it turns the step into rule application, and it files the HOW (the counting method) rather than the WHAT, which the 10/10 rules ban as the decisive step. Reject that option and use the data route.

## Next action for the author
Add counted dump-counter series for two plunger-well separators (one big-slug, one small-slug) in scada_dump_counters_2026.csv, on pads that do not decide the call and with the register's SCADA flag and generator physics consistent, rebuild twice byte-identically, move Kakwa 12-36 #2 off its rounding line if a constant allows, re-argue the ladder and Gate F on paper, then re-judge once.

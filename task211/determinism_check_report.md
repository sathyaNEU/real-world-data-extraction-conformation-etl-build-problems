# determinism-check report, task211, 2026-11-07

## Verdict
DETERMINISTIC. A SOLUTION_WRONG wording defect sits in FINAL_RECOMMENDATION (see Findings 1).
**Disposition:** FIX_NOW (solution-block wording only; pack, prompt and shipped files unchanged). Three optional closures below would change what solvers see and need a rerun and a re-judge.
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one judge, sonnet, medium, brief at /tmp/determinism-check-task211-078575/judge_brief.md, bundle freshly unzipped (sha256 of target.zip 4c5bcbb4...e06b3). Order kept: derivation.md written before graded_blocks.md was opened; every graded figure matched the derivation.

## Why
Read literally, the bundle gives one answer. Of 224 investigation-level periods (reference level plus 30 nSv/h, from the alarm config), 11 are flat plateaus that end in one ten-minute step back to baseline, at MV334 and MV129. Every other increase decays smoothly: the largest one-step fall in the excess over a centred 48-hour median is 41 per cent, against 85 per cent or more on the 11. Rain at the nearest gauge, neighbours and time of day each give a wrong list. All 24 source-check results, 24 timeliness figures and 39 gross beta concentrations reproduced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Detection days, MV334 | 6 (08/07, 17/07, 20/07, 22/07, 07/08, 13/08) | same | yes (dose-rate csv, shape of ends) |
| Detection days, MV129 | 5 (24/08, 28/08, 13/09, 14/09, 17/09) | same | yes |
| Highest ten-minute values | 155 and 164 nSv/h | same | yes (per-day 144/139/134/143/141/155; 164/154/154/133/150) |
| Largest natural one-step fall / smallest artificial | 41% / 85% | same | yes |
| Days with rain within an hour at nearest gauge | 5 of 11 | 5 of 11 | yes (gauge csv, sites csv) |
| Rain screen stations | "16" | 15 at zero rain, 16 at 1 mm tolerance | partly (see Findings 1) |
| Source checks, 24 stations | 24 percentages and Pass/Fail | same, MV243 89.5 Fail, MV184 112.6 Fail | yes (visits xlsx, register, certificates pdf, OP-04 s4) |
| Timeliness, 24 stations | 24 figures | same | yes (ingest log, BST for LoRa clock, F not received, T counted) |
| Gross beta, 39 filters | 39 figures 0.25 to 1.04 | same on integrated logged flow | yes (pump log, results xlsx issue 2) |

## Competing answers that survived
| Fork | Competing reading | Cells it moves | Shipped rule meant to close it |
|---|---|---|---|
| Gross beta volume | totaliser (2.5 m3 per 15 min regardless of flow), AS2 hour meter times set flow, or field-sheet volume, against the integral of logged flow | 38 of 39 filters, each 0.01 to 0.03 lower | none; no sentence says the measured flow governs |
| T intervals in timeliness | T not counted as received | MV184 99.5 to 99.4, MV243 99.6 to 99.5 (both near the .x5 line: 99.472 v 99.449, 99.562 v 99.540) | OP-04 s2 calls T "not monitoring data", yet also treats it as a value; open |
| CS-0583 return to KIT-2 | CS-0417 stays in KIT-2 after the 4 Sep return | 8 Sep MV171 98.4 v 95.9, 10 Sep MV226 99.1 v 96.5, 17 Sep MV149 101.2 v 98.6 (pass/fail unchanged) | register records only a return to the "source store" on 4 Sep; golden reading rests on the standing kit register |
| F counted as received | would move 11 stations by 0.1 to 1.5 points | judge rates it closed enough by OP-04 s2 and Schedule 2.3, not text-closed |

The main call has no surviving fork: SF3, SF4, SF15 (dates, midnight, BST) are not material, and every increase starts on the same date in both clocks.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 | yes |
| Formats | 3 or more | 4 (csv, xlsx, json, pdf) | yes |
| Large file | 25,000 rows or more | 317,592 rows (15.7 MB), plus a 4.7 MB ingest log | yes |
| Distractors named, none labelled by file name | 2 or more | metadata.json names the 2025 annual report and the filter gamma spectrometry; file names carry no label | yes |
| Distractors relevant, unused, ruled out | one that answers a graded quantity reproduces and a shipped fact rules it out | both rank nothing on origin (design note, Oracles); the real tempting surface read, rain gauges, is a data file not a declared distractor | pass with note: weak as wrong-basis distractors, relevant to weigh only loosely |
| Deliverables | 1 to 3, all in golden, no format family | 3 (docx, xlsx, svg), all present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | each | 24, 24 and 39 figures; unit and rounding stated in one closing sentence of the prompt | yes |
| Prompt shape, rubric 25 or more criteria | identifiable, 25 or more | shape "other"; 2 stations, 11 dates, 2 peaks, then 24, 24, 39 gradable figures | yes (rubric generated, not seen) |
| Prompt | one paragraph, question first, under 1,000 chars, no count the data hold | 883 chars, question first, no count | yes |
| Reads as real, not LLM generated | both | no authoring disclosure; incidental mess realistic | yes (goldens not re-judged for realism here) |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_strategy and gate_g decomposition_attribution, stump_class analytical, analyst_test the rain-at-nearest-gauge clearing, domain_test the lead-214 and bismuth-214 decay bound. These agree in substance (the surface read is the rain screen, the decisive step is the shape of each increase's end; no planted defect, decoy or hidden rule, `official_decoy` false). The thread did not name either declared distractor as the surface read, so neither is too load-bearing. No shipped artifact ranks the stations on origin wrongly. One discrepancy: the card, design note (Stump sentence, Three rules domain test, ladder R0) and FINAL_RECOMMENDATION all say "the procedure's" screen, but OP-04 (checked by pdftotext) and Schedule 2 contain no rain, natural or origin text. The default path is the author's constructed route, not a filed one.

Gate H: domain pass, layers pass, decisive_step analytical. Matches the card and the design note's Three rules.

## Stump power (Gate F)
Moderate to high on the whole, with one reservation for the main thread to weigh against the ladder. The decisive step is analytical (choose the discriminator on honest data), the rain, neighbour and time-of-day reads each file a wrong set, and five of the 11 true days carry light rain so a rain-led screen fails both ways. But a strong solver who plots each increase sees flat-topped plateaus ending in one step against smooth decays, and may land the call with no rain screen at all; the physics is textbook (the library's methods are routes a strong solver takes). If both top responses land the call, the pair reaches 60 only on the asks, which carry five or six independent traps (certificate issue date, the borrowed source, microsieverts and old codes, LoRa clock, totaliser against flow, reissued results). The three residual ask forks above are where a response could be marked wrong for a defensible reading, so they cut against the rubric's determinism as much as they add stump.

Pair with task210: same client domain (Physical & Environmental Sciences, environmental-monitoring-exceedance) and objective (anomaly-detection), drawn the same day (2026-11-04), back to back. The mechanisms differ (task210 delivered pump rate from wet-well fill and draw against a permit; task211 decay-bound origin of excursions), and the card carries a differentiation line. The concern is the Layer 1 furniture: both cards list a UTC historian beside a UK local-time log, outstation resends as exact duplicates, and pump or controller logs. task210 also already has two re-checks (pass2, pass3), so its design is not settled. I did not run `guard.py heart` or `surface` and I have no sight of the five promoted clone pairs, so I record the concern and make no ruling; the main thread should confirm those gates, and the clone-check, against task210 before ship.

## Findings, ranked
1. **Solution defect (FIX_NOW).** FINAL_RECOMMENDATION says "the procedure's rain screen would have notified 16 stations"; OP-04 has no rain screen. The judge counts 15 stations at zero rain and 16 at a 1 mm tolerance. Say "a rain screen" with the tolerance, or drop the clause. SOLUTION_STEPS 3 should name the 48-hour running median as the baseline (it already does) and add the KIT-2 default and that T intervals count as received values. The design note's Stump sentence, Three rules and ladder R0 carry the same "procedure's" wording and should be corrected to match.
2. **Gate B, the deciding reading.** No shipped file states how natural and artificial increases differ (OP-04, Schedule 2, the annual report and the spectrometry report are silent; the filters show no Cs-137 or I-131 above MDA). The thread passed it because the data separate the two populations (falls to 41 per cent against 85 per cent or more, 44 points apart, about four counting-noise widths). Weighed against the rule that a method no shipped file carries does not exist for the judge: the data's separation alone does force the reading for a solver who examines the shape of each increase's end, and the golden depends on no method named in any file. A portal judge could still call "an increase ends in one step" external knowledge of radon-progeny decay, because nothing the solver is shown says artificial increases end that way, and this is the likeliest ground for a determinism send-back. The smallest filed WHAT would be one sentence in agreement 2.2 defining the object, for example that an increase of artificial origin is one from a source people switch on and off and that ends when the source is stopped, while natural increases fade as the air clears. It names what the thing is, not the step-fall test or its threshold. Risk to weigh: it hands the decisive reading to every solver, which moves the call toward rule application, so the author may prefer to leave it unfiled and accept the Gate B risk.
3. **Gross beta volume (38 of 39 cells).** The data separate the candidates: the totaliser advances 2.5 m3 per 15 min on every RUN record whatever the measured flow (9.0 to 10.3 m3/h, falling as the filter loads), AS2's totaliser column is empty, and the field-sheet volume is hour meter times about 8 m3/h. A closure in the producing system's own record would carry it in plain words without stating a method: a header or note line in the pump controller export saying the totaliser counts running time at the set flow and does not record the measured flow, or an OP-04 s5 sentence that concentration is per cubic metre of air as the pump measured it. Either states a device, not a computation. A prompt-side convention pin ("air as the pump measured it") is the alternative.
4. **T intervals in timeliness (MV184, MV243).** A line in Schedule 2.3 or OP-04 s2 ("intervals sent in test mode are not counted as received"), or in the ingest log's own status legend, closes it in plain words. These two figures sit within 0.03 of a rounding line either way.
5. **CS-0583's return to KIT-2 (8, 10, 17 Sep checks).** One register row recording the date CS-0583 went back into KIT-2 closes it with no wording. Pass or fail is unaffected, but three graded percentages move.
6. **Distractors.** Both declared distractors rank nothing on origin, so they weigh little; acceptable for the gate, thin as designs.

## Next action for the author
Apply FIX_NOW: correct FINAL_RECOMMENDATION (drop or restate the "procedure's rain screen ... 16" clause), SOLUTION_STEPS 3 and 5 and 6, and the design note's "procedure's screen" wording; then decide whether to file the register row for CS-0583 (finding 5), the pump-log note (finding 3) and the T sentence (finding 4), which need a rebuild, two identical builds and one re-judge. Do not file the finding 2 sentence without deciding it moves the decisive step toward rule application.

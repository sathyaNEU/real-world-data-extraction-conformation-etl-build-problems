# determinism-check report, task460, 2026-10-15

Judged bundle: the fresh unzip at /tmp/determinism-check-task460-1792068956/target/ (the pre-rebuild pack). The thread's verdict is /tmp/determinism-check-task460-1792068956/verdict.md. The task folder's target.zip and submission.md were rebuilt afterwards for reader realism fixes. The only judged figure that moved is Quillbury's published non-baseload rate, 1.12 in the judged pack and 1.11 in the rebuilt pack (2,453.5 lb gives 1.113). submission.md already says 1.11. The judge did not see the rebuilt pack, so one re-confirmation is owed (see Next action).

## Verdict
DETERMINISTIC (no SOLUTION_WRONG against the judged bundle)
**Disposition:** FIX_NOW (optional, no model rerun; two data-dictionary pins, see Findings)
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The charter (3.2 and 3.3) defines avoided CO2 as the counterfactual change in the store's balancing-area generators' emissions, with interchange scheduled a day ahead and fixed. Read literally, that is a response of the area's generators in the hours the array generates. The thread estimated it as the slope of the hour-to-hour change in fossil CO2 on the change in net generation, by season and local standard hour, weighted by array output.
- Gorsefield 0.89 and Halvane 0.58 reproduce (gap 0.31).
- The other six reproduce at 0.39 to 0.41.
- They hold under every estimator variant the thread tried (quarterly, summer/winter, monthly, no seasons, demand regression, imputed hours dropped). All stay inside the same two-decimal bins.
- All five supplementary figure families reproduce for all eight stores.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Gorsefield avoided, t/MWh | 0.89 | 0.891 (0.889 to 0.891 across variants) | yes |
| Halvane | 0.58 | 0.579 | yes |
| Gap | 0.31 | 0.312 | yes |
| Tennaford, Brackwell, Quillbury, Kestrel Point, Faraview, Ostlemere | 0.41, 0.40, 0.39, 0.39, 0.39, 0.39 | 0.408, 0.400, 0.390, 0.389, 0.388, 0.388 | yes |
| Brackwell published average rate | 0.85 | 0.851 (1,876.8 lb) | yes |
| Quillbury non-baseload rate | 1.12 in the judged pack | 1.12 (2,467.5 lb) | yes; the rebuilt pack is 1.11, submission.md is updated, not re-judged |
| Metered use, MWh (Gorsefield, Halvane, Tennaford, Brackwell, Quillbury, Kestrel Point, Faraview, Ostlemere) | 2,589, 2,506, 2,468, 2,381, 2,368, 2,472, 1,984, 2,862 | same | yes |
| Share of use, % (same order) | 28.3, 27.1, 26.9, 26.5, 22.7, 27.5, 23.9, 30.2 | same | yes |
| Price, $/MWh used (same order) | 145, 142, 136, 155, 184, 226, 123, 169 | 145.26, 142.10, 135.92, 154.87, 184.02, 225.82, 123.11, 169.00 | yes |
| Hourly CSV rows | 70,080 | 8 stores x 8,760 hours | yes |
| Chart (monthly use basis) | not pinned | n/a | loosely gradable |

Each figure's source file and field is recorded in the thread's verdict.

## Competing answers that survived
No fork changes the main call. The forks below can move graded asks:
1. **Metered use source (asks 3, 4, 5, 24 figures).**
   - Ardley's "Energy - fixed price" kWh runs a constant 3.6 to 6.2 percent above the delivery utility's distribution kWh. Gorsefield would be 2,705 against 2,589.
   - The golden follows the word "metered" and the utility's distribution quantity. I found no shipped statement that the supplier quantity is loss-grossed: the invoice has no loss, wholesale or delivery-point text, and the Ardley label is silent.
   - The golden is the more natural reading, but it is not closed by a shipped sentence.
2. **Reissued invoices (Quillbury and Ostlemere).**
   - The golden takes the latest invoice per meter and cycle. Taking the first gives 2,398 and 2,828 MWh. Summing both gives 2,614 and 3,119.
   - "Latest supersedes" is stated nowhere. The manifest says credit memos are not included.
3. **Price including taxes.** "What we paid" is cash, so taxes are in (Gorsefield 145, against 137 pre-tax). Low risk.
4. **Average, not marginal.** An hour-matched average weights to Brackwell 0.825. The charter's counterfactual language rules it out. The charter never says "marginal" (low to moderate risk, and it is the intended estimand identification).

Closed forks: the estimator (SF8), the clock (SF9), KPLP/KSTP (SF10), the blended rate against fuel-specific rates, the 2024 rates, and the levels regression.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | csv, xlsx, pdf | yes |
| Large file | 25,000 or more rows | 70,080 rows in the hourly data and in the array model | yes |
| Distractors named in metadata.json | 2 or more, none labelled in a file name | edc_generation_emission_rates_2024.xlsx and ardley_power_content_label_2025.pdf; the names carry only the year and the supplier | yes |
| Distractor relevance | unused, weighable, rule-out-able, reproduces arithmetically | The 2024 rates give Gorsefield 0.93, a different two-decimal figure, and are ruled out by the charter's 2025 and the "data year 2025" notes. The Ardley kWh reproduces at 2,705 for Gorsefield, but nothing shipped says why it is not "metered" use. | partial, see Findings 1 |
| Deliverables | 1 to 3, all in the golden, no format family required | 2 (pdf and csv), both in the golden | yes |
| Asks | multi-dimensional, unit and rounding stated | 8-store tables of five figure families, each with unit and rounding in the prompt | yes |
| Prompt shape and rubric | identifiable shape, 25 or more criteria | prompt_shape 01 (ranked list under a cap of one); about 40 gradable items (8 x 4 figure families, call, first left out, gap, chart, CSV) | yes |
| Not LLM generated, goldens realistic | no tells | Not reviewed beyond the thread's note. The invoices are realistic (rebills, tiers, gas lines, two meters). The pack data are clean. | pass |
| Hygiene (thread) | | Minor temporal incoherence: the charter is dated 15 Sept 2026, but its 5.1 cites the "published 2025 rates", which the manifest dates 1 Oct 2026. Harmless to the answer. | minor |

## Gate G reconciliation
The thread's read and the design note (DESIGN_NOTE.md, Three rules and Ladder) and card match:
- **Mechanism:** the thread says method_or_model_selection, as does the note.
- **Stump class and decisive step:** the thread says analytical, as does the card's `stump_class: analytical`. The decisive step is the same in both: season-by-hour marginal rate weighted by array output.
- **Easy routes:** the thread's easy routes (Brackwell 0.85 average, Quillbury non-baseload, Tennaford one marginal rate fitted over all hours) equal the card's `analyst_test` and the note's R0 to R2 ladder.
- **Domain test:** the thread's swap test agrees with the card's `domain_test`.
- **Surface read:** the thread finds no surface-read rejection. The published rates are correct for another question and the work is a fitted model, which is consistent with the note's "each is a correct number for another question".
- **Declared distractors:** neither is the surface read carrying the task. The rates that carry the easy routes are in edc_generation_emission_rates_2025.xlsx, which is load-bearing for the fuel rates and is not a declared distractor. They are published inventory statistics and no artifact ranks the stores on the decision, so I do not raise Gate G. The thread's own borderline note: the shortcut is a lens swap, but the work is a fitted model.
- **Gate H:** `domain: pass`, `layers: pass`, `decisive_step: analytical`.
  - Layer 1 (mess): UTC end-of-hour against local-standard start-of-hour, the KPLP to KSTP rename, rebills, pro rata, tiers, two meters, and an electric vendor that also bills gas.
  - Layer 2 (rigour): hourly marginal emission factors.
- **Mismatches:** none. No send-back predictor.

## Stump power (Gate F)
Moderate on the main call. A strong model that reads the charter's counterfactual wording may reach the hourly margin. The Brackwell, Quillbury and Tennaford decoys, the fossil blended-rate shortcut and one-hour clock errors remain live ways to fail. The supplementary asks carry most of the difficulty (rebill supersession, pro rata, tiers, two-meter stores, the Halvane gas lines, KPLP, the right year's rates). The thread found the charter close to explicit about the counterfactual, which lowers how often the easy route is taken. No lever is required; this is a measure for the portal.

## Findings, ranked
1. **Metered-use source is not closed by a shipped sentence** (asks 3, 4, 5, 24 figures). The Ardley kWh is a constant 3.6 to 6.2 percent above the utility's. Nothing says it is supplier-level or loss-grossed. A pin in pilot_siting_data_dictionary.xlsx would close it: the delivery utility's distribution quantity is the meter reading and the supplier quantity is billed at the supply level. This is pack data only; the main call and the judged figures do not move.
2. **Reissued invoices:** "a reissued invoice for the same service period supersedes the earlier one" is not stated anywhere in the pack. Second pin in the dictionary.
3. **The chart's monthly use basis is not pinned** (loosely gradable).
4. **Charter "marginal" never named.** Intended estimand identification. Keep as is, do not file the HOW.
5. **Minor temporal incoherence** between the charter date and the rates release date (1 Oct 2026).
6. **Pack rebuilt after the judge ran.** Quillbury non-baseload is 1.11 in the rebuilt target.zip and submission.md, and 1.12 in the judged pack. The judge did not see the rebuilt pack.

## Next action for the author
Add the two data-dictionary pins from findings 1 and 2 to the generator and rebuild, then re-run the stage-3 gates. Do not file how the avoided rate is estimated. Because Quillbury's rate moved to 1.11 and the pack changed after the thread ran, confirm that the rebuilt pack's figures_check still passes. A single FIX_NOW re-judge is available if the author wants one on the rebuilt pack.

# Determinism verdict, task308 (pass 5, run 30805, on eb9d2db9)

- **Verdict:** DETERMINISTIC (main recommendation and asks 1-3 of the PDF). The workbook asks (A: incurred per policy, B: sums insured) were only partly reproduced, see Evidence.
- **Disposition:** FIX_NOW. Optional pins, no rerun: file in RC-07 that the 2027 repair panel is the 2025 panel (firm count unchanged), and pin the term and rewrite conventions for Ask B. The main call and the data stay byte-identical.
- **Why:** I rebuilt the occurrences and the layer values from the shipped files. Under the capacity-strain re-pricing the golden uses, Pennine is 0.09 (GBP 0.1m) and Severn Vale 0.02 (0.0). Pennine's four pre-2021 freezes, at 20.5 to 24.7m index-only, rise to 46 to 63m once their claims per firm roughly double at the 2027 book on the 2025 panel. The ordering held under every fit variant I ran. The literal RC-07 reading (index only) ends on Severn Vale, so the golden depends on an estimated adjustment that no document files by name. RC-07 points at it ("the index ... does not carry what else made a catastrophe's repairs cost what they did") and the claims data separates it, so it is forced analysis and not an unpinned choice.

## Evidence (recomputed)
| Item | Golden | Mine |
|---|---|---|
| Occurrences (first-loss-anchored windows, 72h/168h on date of loss) | stated | 70 to 73 across thresholds 12 to 25 per day, same layer values (-0.51/-0.83/-0.44/+0.02 index-only) |
| Claims per firm, Pennine pre-2021 freezes | 22.6 to 25.1, scaled 44.1 to 49.6 | 22.57, 23.81, 25.09, 24.16 scaled to 44.1, 47.7, 49.6, 46.4 (reproduced) |
| Occurrences of 150 or more claims | 64 | 64 (reproduced) |
| Hinge at 16.5, slope above it | 2.8 per cent | 2.81 per cent (reproduced) |
| Index only | Severn Vale leads | Severn Vale +0.02, Pennine -0.44, Coastal North -0.51, Fenland -0.83 |
| With surge fit | P 0.1, SV 0.0, CN -0.5, F -0.8 | P 0.09, SV 0.02, CN -0.49, F -0.77 |

- The reinstatement premium must use min(recovery, 15m) over 15m, as the quotation says (one reinstatement, at most the annual premium). Charging on the full 30m gives Severn Vale -0.26. That convention is stated in the quotation, so it is not a fork.
- Fit variants: minimum occurrence size 100/150/200, hinge none/10/14/16.5/20, weighted or not, with or without peril levels. Pennine is always 0.09 and Severn Vale 0.01 to 0.04, so the call and the one-decimal figures are stable. Coastal North sits at -0.48 to -0.54 and rounds to -0.5 throughout.
- **Surviving competing answer (the fork):** a solver who refuses to extrapolate claims per firm beyond the observed 22 to 25, or who grows the panel with the book, gets no uplift. The values are then Severn Vale 0.0, Pennine -0.4, Coastal North -0.5, Fenland -0.8, and the recommendation is Severn Vale. Any slope above about 1 per cent per claim per firm on the freeze extrapolation reproduces the golden, and the golden's 2.8 per cent clears that. Nothing in the files fixes the 2027 panel as the 2025 panel, though the panel grows only about 1 firm a year (Pennine 30 to 34), so panel growth barely moves the result. The margin of Pennine over Severn Vale is 0.07m, but the rounded figures (0.1 against 0.0) are not on a rounding line.
- **Ask B (sums insured 31 Dec 2025):** my implementation of step 7 gives Fenland 59,452.5, Pennine 73,471.5, Severn Vale 131,341.3 and Coastal North 71,641.0. The golden has 59,442.2, 73,441.1, 131,316.2 and 71,630.8. The gap is 10 to 30m on each region, so the shipped figures are not reproduced from my literal reading. The likely causes are the rewrite and reinstatement term identity and how mid-term adjustment rows pick the first listed sum insured. It needs a literal-rule check by the builder, or a pin of those conventions.
- **Ask A (incurred per policy):** I did not recompute the major-loss-unit join (cases grouped by policy, peril and latest date of loss, with the drop-out rule). Platform-only values (for example Fenland 2023: 104.74 against golden 117.89) differ as expected because the MLU claims are added. The golden is plausible but unverified here. It is a long rule-application chain, which the asks may be.
- Window placement ("the company may choose the date and time") does not move the answer. A best-window search and the first-loss anchor give identical layer values, and date of loss carries no time of day.

## Files/Hygiene
- Hygiene: PASS. 13 files across 6 formats (parquet, csv, xlsx, pdf, with nested sheets). The 483,625-row claims file satisfies the large-file gate. Documents are business-like. No authoring or benchmark language. Dates are coherent (extract date 31 Oct 2026, quotes 18 Nov 2026, plan 29 Oct 2026).
- Likely distractors: group_catastrophe_programme_2026.pdf, flood_resilience_survey_2024.csv, claims_operations_report_2025.pdf. The ops report's volume table does not match the claims parquet 2025 counts, so confirm it was meant as a distractor. No exclusion-level finding.
- Cross-batch check: no corpus access inside the allow-list, so not performed.

## Stump power
The trap is that an index-only carry-forward of recorded costs (Severn Vale, +0.02) ignores that Pennine's small repair panel (30 to 34 firms) made its freeze repairs cost more under strain. At 2027 volume the strain is roughly double, and the four freezes exhaust the layer. A capable analyst who cleans the data and applies RC-07 literally ends on Severn Vale, so the stump is strong. The cost is that the surge model is an estimate the analyst must choose.

## Stumping type
mechanism: forecasting / structural cost model (capacity-driven repair-cost elasticity); stumping_family: analytical (method with data-separated candidates); surface_read_dependency: no; sole_data_defect: no. The solver must estimate a cost response to repair capacity and re-price at the cover-year scale, which is a FINE-numbers modelling shape and not the rejection of a misleading reported figure. Gate G passes.

**Three rules (Gate H):** domain: pass; layers: pass; decisive_step: analytical. The field's own analysis is catastrophe-layer pricing, with loss-occurrence aggregation, exposure and cost re-basing, and a demand-surge / repair-capacity elasticity fitted on the claims. A swap to another field's nouns would not read the same. The easy route is to index-adjust and re-scale claims (the policy's literal recipe), with one loss occurrence per catastrophe. That gives Severn Vale at +0.0, which is wrong. Layer 1 mess: uncoded and late-notified claims, a Calder and Colne book, bordereaux, MLU case reports.

## Fix
- **Where:** input_files or prompt, minor.
- **What:** (1) Add one sentence to RC-07 section 3 that the cover year's repair panel is the 2025 panel. This pins a WHAT (population and scale), not the HOW. (2) Check Ask B against the literal step 7 and pin the term-identity and rewrite convention, or correct the golden if my reading is the intended one. (3) Recompute Ask A independently, since I did not.

# Verdict, task145 (fresh pass after redesign)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. Nothing needs repair for correctness. One watch-item (below) is an optional prompt or plan-note pin, not a blocker; if it is taken it requires no rerun of the data, only a re-read of the prompt.

**Why:** Every committed answer reproduced from the shipped files: 2 posts at Dorval, 1 at Calgary, 3 held. The three-post call rests on the 12 gateway-by-currency pass-through shares, which split cleanly: 0.96 to 1.00 in nine segments and 0.009 to 0.013 in three (Calgary USD, Mississauga CNY, Richmond CNY). Calgary's post survives every reasonable estimate of that share (it holds for any Calgary USD share below about 0.62, and also if only repeating consignments keep their CAD value), so the thin-margin test is clean. The main weakness is that no shipped sentence says forecasts should carry observed pass-through. The text alone (plan assumption 2 "goods as in the base", assumption 7 planning rates, CLR-OPS-11 2.1 and 2.2) is also satisfied by re-routing every foreign-currency shipment at the plan rates. That reading gives Dorval 2 and Calgary 0, with 4 held. The data refutes it for Calgary, so it is not an equally licensed alternative (see Evidence).

## Evidence (recomputed from target/)

| Item | Source | Reproduced |
|---|---|---|
| Base year 245,702 shipments, prior year 234,415, amended rows kept once (13 amended) | 8 highvalue_check files, old layout DD/MM/YYYY mapped to new | yes |
| Base formal rows per gateway 48,862 / 37,362 / 40,242 / 30,053 / 20,313 (YYZ/YUL/YVR/YYC/YWG) | equal formal_entries_released in gateway_activity_2024-10_2026-09.csv | yes |
| 73,696 repeat consignments (key gateway, importer, hs, currency; same invoice value or same CAD value; no shipment matches both) | highvalue_check | yes |
| Pass-through by segment: Calgary USD 117 of 13,286 = 0.009 (13,169 at same CAD value); YYZ CNY 0.011; YVR CNY 0.013; other nine 0.958 to 1.000; network 0.737; USD 0.719 | highvalue_check | yes |
| Routed formal counts 43,828 / 41,835 / 35,693 / 29,994 / 17,620 | share-weighted routing at plan rates against CAD 3,300, OGD always formal | yes (all five) |
| Re-route-all gives Calgary 23,332 | same | yes |
| Plan scale factors 1.0249 / 1.0330 / 1.0390 / 1.0403 / 1.0222 | network_plan_2027.xlsx over gateway_activity base totals | yes |
| Forecasts 3,743 / 3,601 / 3,091 / 2,600 / 1,501, which round to 3,750 / 3,600 / 3,100 / 2,600 / 1,500 | computed | yes |
| Placement 720 (YUL), 650 (YYC), 600 (YUL), then highest is YYZ at 535; loads 535 / 515 / 515 / 520 / 500 | BRK-STD-03 4.5 and Appendix A (posts 7/5/6/4/3) | yes |
| Overtime hours by desk and quarter (2,664 hours total); table in SUPPLEMENTARY_ANSWERS | ta_legacy and ta_export, MIGRATED lines dropped, desk by work date, call-backs at punch span | yes, all 20 cells match after rounding |
| Brandmoor net by desk and quarter (CAD 220,798 total); table in SUPPLEMENTARY_ANSWERS | ap_invoice_register, statement date month minus one, cost-centre scheme mapping, R1 re-issue and credit memo netted | yes, all 20 cells match |

Competing answers tested (main call):
- **Pass-through by segment (golden):** Dorval 2, Calgary 1, hold 3.
- **Re-route every foreign-currency shipment at the plan rates (literal rule execution):** Dorval 2, Calgary 0, hold 4. Calgary reaches 2,023 a month, 506 a post. The data contradicts the premise for Calgary: 99.1 per cent of its repeats held their CAD value while the rate moved.
- **Base-year formal rate carried unchanged:** 5 posts (YUL 643, YYC 651, YYZ 596, YVR 581, YWG 577), 1 held. The plan rates move, so this ignores a stated planning assumption.
- **One network share (0.737):** Dorval 2, hold 4 (YYC 544, YYZ 548 are under 560). This averages away the Calgary behaviour.
- **Repeaters keep CAD value, non-repeaters re-routed:** Calgary 2,512 a month, 628 a post, so the post is still placed. Same call as the golden.

Ask-level forks, each closed by the asking text or a shipped file:
- **Call-backs:** paid hours (min 3.00) against punch span. The prompt says "hours worked", and the data dictionary says HOURS is "the hours the line pays". The paid-hours reading flips most cells.
- **Desk:** desk on the work date (from the transfer table) against current roster desk or home cost centre. The roster desk flips cells (for example Dorval Q2 207 against 160).
- **Brandmoor:** the month lag comes only from the portal JSON, which shows every statement bills the prior month. The portal fee column is re-rated at the current schedule for statements before February 2026 and does not match the register, so the register, not the portal, is "charged". Fork risk: low.

## Files/Hygiene
PASS. 26 files; formats xlsx, csv, json, pdf (3), txt (2), docx; eight extracts of 6 to 8 MB, 480,130 rows in all. Distractors present and unused: gateway_activity_2021-01_2024-09.xlsx, network_plan_2026_issued_2025-09.xlsx, export_declarations_monthly, brandmoor_rate_schedule_2025.pdf. Timeline coherent (pulls 6 and 7 October 2026, covering through 30 September 2026). No authoring or benchmark disclosure found, and no leaked golden figures in the notes. Layout changes (old and new extract layouts, DD/MM against ISO dates, UTC against local release date, legacy and ERP cost-centre schemes, T&A migration overlap, re-issued statement) read as system artifacts. One hygiene note: the portal JSON fees disagree with the statements for pre-February 2026 statements. This looks like a realistic re-rating artifact and does not affect the answer, since the register is unambiguous.

## Stump power (Gate F)
Moderate to good. The easy routes are a clean-looking filed rule (re-route at plan rates) or carrying the base-year ratio, both of which a capable analyst could file, and both give a different post count (4 held, or 5 posts). Three further traps compound this: the call-back and desk-attribution asks, the statement-month lag, and the old and new extract layouts. The caveat is that nothing in the prompt cues the solver to test pass-through, so a model that never compares year-over-year repeats lands on the 4-held answer for a defensible-looking reason. That is the live stump, but it is also the source of the watch-item.

## Stumping type (Gate G)
`mechanism: method_or_model_selection (estimating FX pass-through), forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported number is wrong and no defect is planted. The difficulty is estimating how importers' prices respond to the plan rates and carrying that into a threshold-crossing count. On clean data the task would still stump, since the pass-through split is a property of the shipments, not a defect.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- **Domain:** forecasting formal entries at a value threshold under planned exchange rates for a brokerage staffing standard is customs and workforce-planning work. The swap test fails if "formal entries", "CAD 3,300" and "planning rate" are replaced by other nouns.
- **Layer 1:** extract layout change, DD/MM against ISO dates, UTC against local, legacy against ERP cost centres, T&A migration overlap, statement lag, re-issued statement.
- **Layer 2:** estimating FX pass-through from repeat consignments by gateway and invoice currency.
- **Decisive step:** a strong analyst who read every rule and cleaned the data correctly still gets it wrong by re-routing at the plan rates (Dorval 2, Calgary 0, 4 held) or by using one network share. Pass-through is the unit-of-behaviour choice, which counts as analysis.

## Fix
none required. Optional (location: prompt or plan note, estimand not method): the filed text stays silent on whether the forecast should reflect how importers price. A one-line pin of the WHAT would close the residual literal-reading fork, for example a clause in plan assumption 2 (shipment profile, lanes, customers and goods as in the base, "priced as in the base"). Do not file the pass-through share method itself, which would turn the decisive step into rule application. If the author keeps the text silent, the call remains forced by the data, but the literal-reading fork (4 held) is the one a strict reviewer could cite.

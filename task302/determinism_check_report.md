Determinism judge, stage 4 pass on target.zip 3b9ace95 (task302, run r3): one isolated thread holding only the shipped bundle and the submission's graded blocks. The shipped pack is the judged pack (target.zip 3b9ace95, rebuilt byte-identical at ship).

# Determinism verdict, task302 (run r3)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair needed and no rerun; two residual soft forks (below) are worth a prompt-side watch only if the portal shows them.

**Why:** The main call (infant formula, about NZD 60,000) is forced once "the category would have sold, less what it did sell" is read literally as a category-level counterfactual over the 12 months: only then do water's substitution (same-day sales on other water lines) and pet food's post-restock recovery come out of the loss, and formula is the one category with neither (its whole shelf empties at once, 246 store-days, 1,968 line-days). Every workbook figure and chart value reproduced from the shipped files. Gate A to E pass; the forks are residual and each is closed by evidence inside the files.

## Evidence (all recomputed from target/)
| Item | Result | Source |
|---|---|---|
| OOS line-days 2025-26 (opening on_hand_open = 0, trading days) | water 2,714; formula 1,968; pet food 2,042; GF 1,900: reproduced | stock_positions + store_trading_days |
| Formula OOS all on days all 8 lines out | 246 store-days x 8 = 1,968: reproduced | stock_positions |
| Till code to article mapping valid by date | 100% of POS codes map, 0 out-of-validity rows | till_item_codes, pos parquet |
| Main value, my own build (weekday mean +-4/8 weeks, excl. other-line-out days and 14 days after own restock; offset = units above expectation on other-out days and post-restock; halved; fy2026 price) | formula 57.8k (lost 119.5k less 3.9k, halved); water 11.6k; pet food 16.6k; GF 11.3k. Golden "about 60,000" rounds to the same NZD 10k (57.8k to 60k). | lines.csv shelf_price_fy2026 |
| Same loss with no netting (line-level) | water 109k, pet food 91k, formula 61k, GF 23k (water wins) | competing reading, see Fork 1 |
| Netting same-day substitution only (no post-restock recovery) | pet food 69.7k vs formula 59.7k (pet food wins) | competing reading, see Fork 2 |
| Post-restock profile | pet food units ~1.15-1.2x baseline for ~11 days after restock, then 1.0; water 1.25x day 0 then ~1.1 for 3 days; formula and GF ~1.0 | stock_positions + pos |
| Cereal trial (open stock = on_hand to 1 Feb 2026; from 2 Feb on_hand is closing: prev close + delivery = opening; closing identity holds on 99.5% of 8,640 post rows, opening identity on 98.7% of pre rows) | Feilding 99 to 26 (-73.7%); Levin 66 to 38 (-42.4%); Carterton 97 to 40 (-58.8%): reproduced | cereal_trial_stock |
| Same, naive on_hand==0 after go-live | 37/53/56, i.e. -62.6/-19.7/-42.3 (wrong; 41 sold-while-zero days show it is closing stock) | cereal_trial_stock |
| Deliveries after opening (6:30 to 31 Mar 2026, 7:00 from 1 Apr, from first-sale times) | North 339, South 169: reproduced (same result using each day's actual first sale) | dc_trailer_stops, store_trading_days |
| Same with stores.csv flat 07:00 | 305 / 151 (contradicted by sales at 06:31 for 9 months) | stores.csv |
| Pallets by month (appointment total counted once; the 166 two-dispatch-advice appointments carry identical pallet totals against different case counts) | water 188,185,262,205,223,249,247,221,178,259,221,200; pet food 277,224,228,290,214,240,209,176,258,198,193,207; GF 33,34,37,44,35,41,35,33,38,31,46,29: reproduced | goods_received + dock_appointments |
| Same, one total per dispatch advice | water 272,268,309,... (overcounts); naive row sum far higher | competing reading, see Fork 3 |
| Formula excluded from pallets | lines.csv supply = Supplier direct; formula absent from POs/GRNs | lines.csv |

## Forks (literal reading)
1. **Line-level vs category-level estimand (main call).** The planning note says "what [the category] would have sold ... less what it did sell", which is a category counterfactual; line-level lost sales (water 109k) is the easy route and gives water. Text licenses category netting; I rate it forced but it is the one place a good-faith analyst could disagree, and the method (how to net) is left open.
2. **Post-restock recovery (main call).** Omitting it leaves pet food at ~70k, above formula. Evidence for it is plain in the data (1.15-1.2x for ~11 days after each restock, restocks follow the OOS spell) and it is part of the 12-month category sales the note values, so forced; the window (7 to 21 days) does not change the ranking (net pet food stays under 25k).
3. **Pallets once per truck (workbook).** Data dictionary says only "pallets received". Forced by the file evidence (identical totals on both advices of every shared appointment, different cases), but undocumented; the alternative gives different monthly numbers.
4. **Store opening time (workbook).** stores.csv shows flat 07:00; tills show 06:30 first sales to 31 Mar 2026. Forced by sales before 07:00; alternative 305/151.
5. **Cereal on_hand semantics (workbook).** Undocumented switch, forced by 41 sold-while-zero rows and the stock identity.
Thin margin check: formula 57.8k to 60.6k across my variants, all round to 60k; nearest boundaries 55k and 65k. Formula leads the others by >40k under netting. No margin fragility.

## Files/Hygiene: PASS
16 files, formats csv (12), parquet, docx (2), xlsx. 25,000-row bar met (stock 683k, pos 609k). Business-realistic ids, mixed code types, exports with irregularities. Distractors: shelf_space_2026.xlsx, store_ordering_hours, purchase orders and EDI messages. No authoring/benchmark disclosure found in the two docx or xlsx. Temporal: note dated 16 Nov 2026, data to 30 Jun 2026, decision 25 Nov: coherent. No public-data contamination concern; no answer leakage found (the dictionary does not document the on_hand switch or pallet repetition). Not exclusion-level.

## Stump power (Gate F)
Strong models will plausibly fail: the easy route (rank by OOS line-days or by line-level lost sales) names bottled water (2,714 line-days, 109k); stopping at same-day substitution names pet food (~70k). Only category-level netting with deferred-demand recovery gives formula. Not too easy; the pack does not point to netting.

## Stumping type (Gate G)
mechanism: decomposition_attribution / statistical_rigor (category-level incremental sales, substitution and pull-forward), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no. Reported numbers (OOS counts, prices) are fine; difficulty is the estimand on honest data and survives clean data.

## Three rules (Gate H)
domain: pass, layers: pass (Layer 1: GTIN change over two pack changes, opening/closing on_hand switch, 6:30 to 7:00 opening, double-booked pallets; Layer 2: category-level incremental-sales estimation with substitution and demand pull-forward), decisive_step: analytical.
Field analysis: demand-loss estimation under stockouts, the standard retail lost-sales and substitution problem. Easy route taken after cleaning everything correctly: expected-minus-actual per out line, ranking water first (109k vs formula 61k).

## Fix: none
Optional (not required): none that changes what solvers see.

mechanism: decomposition_attribution; stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no; Gate H: domain pass / layers pass / decisive_step analytical.

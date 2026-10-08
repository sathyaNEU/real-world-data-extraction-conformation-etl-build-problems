# RC22 — Inflation accelerated from 3.0% to 3.7%: was it shelter, or last year's energy collapse dropping out?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Year-over-year growth acceleration in retail comparable sales, ad revenue or app engagement driven by easy or hard comparisons a year earlier (base effects) rather than by recent momentum |
| Domain | Macroeconomics / pricing strategy |
| Task shape | 03 · Bridge between two totals (12-month CPI inflation at month A → month B, bridged by component contributions, each split into recent monthly changes and base effects) |
| Core method | Exact contributions of components to a 12-month change in a chained Laspeyres-type index: link the 12-month span at the December weight update, using relative importances updated monthly by relative price change; combine the two links multiplicatively; contribution to acceleration = contribution at B − contribution at A; split each component's acceleration into months entering the window (recent) and months leaving it (base effect) |
| Analytical stump | Multiplying each component's 12-month change by the latest published relative importance gives contributions that do not add up to all-items inflation, because weights drift with relative prices and are reset each December. More importantly, acceleration in a 12-month rate is the difference between the month that enters the window and the month that drops out; a large energy price fall a year ago leaving the window raises inflation even if energy prices are flat now |
| Primary sources | U.S. BLS Consumer Price Index (CPI-U, not seasonally adjusted, component indexes) and BLS CPI relative importance tables (December) |

## 1. The real-world situation

A national retailer's pricing committee meets monthly to decide whether to accelerate price increases. The economist's slide said inflation
accelerated from 3.0% to 3.7% over six months "because shelter is re-accelerating", which supports aggressive pricing on home goods. A board member
pointed out that energy prices had collapsed a year earlier. The committee asked for an exact attribution before deciding.

## 2. The decision (one deterministic recommendation)

**The component to which the acceleration is attributed (largest contribution to the change in 12-month inflation from month A to month B), and
whether that contribution is mainly recent momentum or base effect (base share ≥ 50% means "base effect"), with the full component bridge.**

Rules (pricing-committee memo):

* Data: CPI-U NSA indexes for all items and the memo's 6-way partition: food, energy, shelter, core goods, medical care services, other core
  services (less shelter and medical); December relative importances from the BLS tables for each December spanned.
* Relative importance in month t within a weight year: RI_i(t) = RI_i(Dec) × [I_i(t) ÷ I_i(Dec)] ÷ [I_all(t) ÷ I_all(Dec)].
* Contribution of component i to the change from month s to month t within one weight year: RI_i(s) × [I_i(t) ÷ I_i(s) − 1] in index terms (the
  RI values sum to 100 across the partition).
* For a 12-month span crossing December, compute link 1 (s → Dec, old weights) and link 2 (Dec → t, new weights); the 12-month contribution =
  c1_i × (1 + g2) + c2_i, where g2 is the all-items change in link 2 and c are the link contributions as fractions.
* Acceleration contribution = 12-month contribution at B − at A.
* Recent vs base: for each component, recompute its 12-month contribution at B holding (i) only the monthly changes between A and B (entering
  months) and (ii) only the monthly changes between A − 12 and B − 12 (leaving months) at their actual values, with others as at A; report the shares
  of the acceleration contribution (normalised to sum to the component total).
* Attribute to the component with the largest acceleration contribution; label it "base effect" if the leaving-month share ≥ 50%.

## 3. Why capable analysts get it wrong

* Weight × 12-month change is the familiar shortcut.
* Acceleration is read as current momentum; the dropping-out month is invisible on a level chart.
* Weights are reset each December, so spans crossing December need linking.
* Shelter is a large, slow-moving component that dominates the level of inflation but not necessarily its change.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `cu.data.0.Current` | TXT (tab) | ~2M | BLS CPI flat files (download.bls.gov/pub/time.series/cu) | U.S. Government work (public domain) | Index levels |
| 2 | `cu.series` / `cu.item` | TXT | ~8k | BLS | Public domain | Series and item codes |
| 3 | `relative_importance_<Dec years>.xlsx` | XLSX | ~400 each | BLS CPI relative importance tables | Public domain | December weights |
| 4 | `cpi_handbook_of_methods.html` | HTML | — | BLS Handbook of Methods (CPI) | Public domain | Aggregation formulas |
| 5 | `pricing_committee_memo.pdf` | PDF | — | Task author | — | Rules in §2, months A and B, partition |
| 6 | `economist_slide.xlsx` | XLSX | — | Task author | — | The shortcut contributions |

## 5. Deterministic solution path

1. Extract NSA indexes for all items and the 6 components; December relative importances; verify the partition sums to 100.
2. Monthly-updated RI within each weight year.
3. Linked 12-month contributions at A and at B; check they sum to all-items inflation.
4. Acceleration contributions; recent vs base split; attribution and label.
5. Contrast with the economist's slide.

## 6. Wrong paths (method errors, not misreadings)

**A — latest RI × 12-month change.** Contributions do not sum to all-items inflation; ranking errors follow.

**B — level contributions instead of changes.** Shelter has the largest contribution to the level, so it "explains" the acceleration.

**C — no December linking.** Mixed weight years produce inconsistent contributions.

**D — seasonally adjusted components summed.** SA series are adjusted separately and are not additive.

## 7. Why the stump is analytical, not semantic

The partition, weights and formulas are specified. The trap is a growth-rate identity: acceleration equals entering minus leaving months, with
weights that drift.

## 8. Draft task prompt (prose)

> Our economist says inflation is re-accelerating because of shelter. Attribute the change in 12-month inflation between the two months in the
> pricing-committee memo to its components, including base effects, using the memo's exact method. Provide `acceleration_bridge.csv` (component:
> contributions at A and B, acceleration, recent and base shares), `acceleration_bridge.png`, and a one-page `pricing_committee_note.pdf`.

## 9. Deliverables

* `acceleration_bridge.csv` — six components with contributions, acceleration and splits.
* `acceleration_bridge.png` — waterfall from inflation at A to B by component, with base effects hatched.
* `pricing_committee_note.pdf` — attribution, label, and why the slide misleads.

## 10. Where 25+ rubric criteria come from

* Contributions at A and B for 6 components: 12.
* Closure checks at A and B: 2.
* Acceleration contributions: 6.
* Recent/base split for the top 2 components: 4.
* Attribution and label: 2.
* Slide contrast: 2+.

## 11. Golden-output checklist

* NSA indexes; December RIs per weight year; monthly RI update.
* Two-link combination across December.
* Acceleration as B − A; entering/leaving split.

## 12. Build notes (scope tuning)

* Choose A and B such that energy had a large decline in the months A − 12 to B − 12 and shelter decelerated slightly between A and B; confirm that
  energy's base effect is the largest acceleration contribution.

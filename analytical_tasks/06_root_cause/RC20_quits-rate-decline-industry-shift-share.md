# RC20 — The national quits rate fell from 3.0% to 2.3%: did people stop quitting everywhere, or did high-churn industries shrink?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Churn-rate changes in a portfolio of segments (subscription churn across plans, employee attrition across job families, app uninstall rates across markets) |
| Domain | Labour markets / workforce planning |
| Task shape | 03 · Bridge between two totals (total private quits rate, reference year → current year, bridged into within-industry rate changes, employment-mix changes and interaction, with the industry contributions listed) |
| Core method | Shift-share on not-seasonally-adjusted JOLTS levels averaged over the same 12 months: aggregate rate = Σ employment share × industry quits rate; within = Σ base share × Δ rate; mix = Σ Δ share × base rate; interaction; closure against the published aggregate; breadth test across industries |
| Analytical stump | Seasonally adjusted industry series are adjusted independently, so SA industry levels do not add up to the SA total and a bridge built on them does not close, leaving a residual that gets misread. Monthly snapshots also mix seasonal swings into the comparison. And a mix explanation is easy to assert but often wrong: the decomposition must be computed with base-period weights before deciding whether the decline is broad |
| Primary sources | U.S. BLS Job Openings and Labor Turnover Survey (JOLTS) — quits and employment levels by industry, seasonally adjusted and not seasonally adjusted |

## 1. The real-world situation

A large employer's HR leadership team had funded retention bonuses during the high-quit period. With the national quits rate down from 3.0% to
2.3%, finance proposed cutting the programme, arguing that "people have stopped quitting". HR argued the fall was mostly leisure and hospitality,
a high-churn sector whose share of employment had changed, and that quits in the company's professional-services and information industries were
still elevated. The committee wants a bridge.

## 2. The decision (one deterministic recommendation)

**Whether the retention programme is cut (cut if the within-industry component is ≥ 70% of the decline and at least 12 of the industries in the
memo's list have lower quits rates), with the bridge and industry contributions.**

Rules (workforce memo):

* Data: JOLTS not-seasonally-adjusted quits levels and employment levels for total private and the memo's list of 17 non-overlapping private
  industries (the most detailed level that sums to total private).
* Periods: 12-month averages for the reference year and current year (same calendar months).
* Industry rate r_i = mean quits level ÷ mean employment level; share w_i = mean employment level ÷ Σ employment.
* Aggregate rate R = Σ w_i r_i; closure check against total private NSA quits ÷ employment (report the difference, which arises only from the
  industry list and rounding).
* Within = Σ w_i,ref × Δr_i; mix = Σ Δw_i × r_i,ref; interaction = Σ Δw_i × Δr_i.
* Industry contribution = w_i,ref × Δr_i + Δw_i × r_i,ref + Δw_i × Δr_i.
* Breadth: count industries with r_i,cur < r_i,ref.

## 3. Why capable analysts get it wrong

* Published headline series are seasonally adjusted; using them for additive bridges breaks closure.
* The intuitive mix story (fewer hospitality workers) feels right without being computed.
* Single-month comparisons pick up seasonal and sampling noise.
* The decision depends on breadth as well as on size.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `jt.data.1.AllItems` | TXT (tab) | ~700k | BLS JOLTS flat files (download.bls.gov/pub/time.series/jt) | U.S. Government work (public domain) | All JOLTS series |
| 2 | `jt.series` | TXT | ~2k | BLS | Public domain | Series metadata (industry, element, SA flag) |
| 3 | `jt.industry` | TXT | ~30 | BLS | Public domain | Industry codes and hierarchy |
| 4 | `jolts_handbook_methods.html` | HTML | — | BLS Handbook of Methods | Public domain | Seasonal adjustment and estimation notes |
| 5 | `workforce_memo.pdf` | PDF | — | Task author | — | Rules in §2, industry list |
| 6 | `finance_cut_proposal.xlsx` | XLSX | — | Task author | — | Finance's SA headline comparison |

## 5. Deterministic solution path

1. Identify NSA quits and employment series for total private and the 17 industries; verify they partition total private.
2. Average levels over the two 12-month periods; compute rates and shares.
3. Shift-share components and industry contributions; closure check.
4. Breadth count; decision; contrast with finance's comparison and with an SA-based bridge.

## 6. Wrong paths (method errors, not misreadings)

**A — bridge on SA series.** Components do not sum to the SA total; the residual is misread as a mix or within effect.

**B — single-month comparison.** Seasonal and sampling noise; the decline is mis-sized.

**C — overlapping industry levels.** Supersectors and their components double-count employment.

**D — mean of industry rates.** Unweighted averaging ignores employment shares entirely.

## 7. Why the stump is analytical, not semantic

The industry list and formulas are given. The trap is additivity under independent seasonal adjustment and the temptation to assert a mix story
without computing it.

## 8. Draft task prompt (prose)

> Finance wants to cut our retention bonuses because quits have fallen nationally. Build the industry shift-share bridge in the workforce memo and
> tell me whether the fall is broad enough to justify the cut. Provide `quits_bridge.csv` (component and industry contributions),
> `quits_bridge_waterfall.png`, and a one-page `retention_programme_decision.pdf`.

## 9. Deliverables

* `quits_bridge.csv` — R_ref, within, mix, interaction, R_cur; plus each industry's contribution.
* `quits_bridge_waterfall.png` — waterfall by component, with industry contributions as a ranked bar inset.
* `retention_programme_decision.pdf` — decision, breadth count, and why the SA comparison misleads.

## 10. Where 25+ rubric criteria come from

* Series identification (NSA, partition check): 3.
* Rates and shares for the 17 industries (sampled 6 industries × 2 periods): 12.
* Components and closure: 5.
* Breadth count and decision: 2.
* Contrast with finance's figures: 2.
* Chart elements: 2+.

## 11. Golden-output checklist

* NSA levels; 12-month averages; partitioning industries.
* Rates as ratio of mean levels; base-period weights.
* Closure against total private NSA.
* Decision thresholds: 70% within and ≥ 12 industries lower.

## 12. Build notes (scope tuning)

* Choose a reference and current year in which the within component dominates but an SA-based bridge leaves a residual of ≥ 0.05 points; confirm the
  breadth count against the decision threshold before fixing the memo's 70% and 12-industry rules.

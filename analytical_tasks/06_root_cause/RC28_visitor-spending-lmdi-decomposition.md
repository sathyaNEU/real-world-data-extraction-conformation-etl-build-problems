# RC28 — Visitor spending up 6% while arrivals fell 3%: richer visitors, longer stays, a different market mix, or just prices?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Multiplicative revenue identities (revenue = users × sessions per user × revenue per session, by market; GMV = buyers × orders per buyer × basket value) where mix and price levels move together |
| Domain | Travel and tourism / destination marketing |
| Task shape | 03 · Bridge between two totals (annual visitor spending, reference → current, bridged by arrivals, market mix, length of stay, real daily spend and price level) |
| Core method | Spending = Σ_m arrivals × (arrivals_m ÷ arrivals) × days per visitor_m × real spend per visitor-day_m × price index; additive LMDI-I decomposition (logarithmic-mean weights) by factor across markets, giving exact closure with no residual; real spend uses the local CPI |
| Analytical stump | Additive percentage-change arithmetic on a multiplicative identity leaves an unexplained residual and depends on the order of factors. Market mix is a hidden factor: a rebound in a market with high daily spend but short stays raises spending per visitor without any market's visitors spending more. Nominal daily spend also includes local price inflation, which is not "higher-spending visitors" |
| Primary sources | Hawaiʻi Department of Business, Economic Development and Tourism (DBEDT) monthly visitor statistics by major market area; U.S. BLS CPI for Urban Hawaii |

## 1. The real-world situation

A state tourism authority reported record visitor spending despite fewer arrivals and credited its "high-value visitor" marketing strategy. The
legislature's budget committee, deciding whether to renew that strategy's funding, asked the auditor for an exact decomposition of the spending
change.

## 2. The decision (one deterministic recommendation)

**Whether the "high-value visitor" claim is supported (supported only if the real daily-spend effect is ≥ 50% of the nominal spending change), with
the five-factor LMDI bridge.**

Rules (audit memo):

* Data: DBEDT monthly visitor statistics, calendar reference and current years; markets: U.S. West, U.S. East, Japan, Canada, All Other; measures:
  visitor arrivals (air), visitor days, visitor expenditures ($).
* Annual values per market: sums of monthly arrivals, days and expenditures.
* Factors per market: A = total arrivals; S_m = arrivals_m ÷ A; L_m = days_m ÷ arrivals_m; D_m = (expenditures_m ÷ days_m) ÷ P; P = annual average
  CPI for Urban Hawaii (reference year = 1).
* Spending V = Σ_m A × S_m × L_m × D_m × P.
* LMDI-I: effect of factor X = Σ_m Lm(V_m,cur, V_m,ref) × ln(X_m,cur ÷ X_m,ref), with Lm(a, b) = (a − b) ÷ (ln a − ln b); for A and P the ratios are
  common to all markets.
* Report effects for arrivals, mix, length of stay, real daily spend, price; verify they sum to ΔV.
* Supported if real daily spend effect ÷ ΔV ≥ 50%.

## 3. Why capable analysts get it wrong

* "Spend per visitor rose" sounds like a behaviour change.
* Mix and stay length move spending per visitor without any spending behaviour change.
* Inflation in a tourist economy can be large and is invisible in nominal figures.
* Multiplicative identities need logarithmic or symmetric decompositions to close.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `dbedt_visitor_monthly_<years>.xlsx` | XLSX | ~15k (month × market × island × measure) | DBEDT Tourism Research (monthly visitor statistics) | Hawaiʻi State data, reuse with attribution (verify) | Arrivals, days, expenditures |
| 2 | `dbedt_visitor_definitions.pdf` | PDF | — | DBEDT | Same | Measure definitions and market areas |
| 3 | `cuura426sa0.csv` | CSV | ~100 | BLS CPI (Urban Hawaii, all items) | U.S. Government work (public domain) | Price index |
| 4 | `audit_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `authority_annual_report_excerpt.pdf` | PDF | — | Task author (summary of the authority's claim) | — | The high-value claim |
| 6 | `ang_2004_lmdi_citation.pdf` | PDF | — | Cite | Cite | LMDI method |

## 5. Deterministic solution path

1. Extract monthly measures by market; annualise; compute factors.
2. Compute V by market and total; reconcile with published totals.
3. LMDI effects; closure.
4. Decision; contrast with sequential percentage arithmetic and with the authority's claim.

## 6. Wrong paths (method errors, not misreadings)

**A — percentage changes added.** Leaves a residual; the order of factors changes the story.

**B — no market split.** Mix is folded into daily spend and stay length.

**C — nominal daily spend.** Inflation is credited to visitor quality.

**D — island-level double counting.** Visitors to several islands counted per island; state totals must be used.

## 7. Why the stump is analytical, not semantic

Factors and formulas are specified from published measures. The trap is a multiplicative identity with a hidden mix factor and a price level.

## 8. Draft task prompt (prose)

> The tourism authority says its high-value strategy drove record spending. Decompose the spending change with the audit memo's LMDI method and tell
> me whether the claim holds. Provide `spending_lmdi.csv` (factor: $ effect, share), `spending_bridge.png`, and a one-page `audit_finding.pdf`.

## 9. Deliverables

* `spending_lmdi.csv` — five factor effects with market detail.
* `spending_bridge.png` — waterfall by factor with market contributions as stacked segments.
* `audit_finding.pdf` — decision, bridge, and why per-visitor spending growth misleads.

## 10. Where 25+ rubric criteria come from

* Annual measures for 5 markets × 2 years × 3 measures (scored in groups): 6.
* Factors S, L, D per market: 6 (grouped).
* CPI ratio: 1.
* Five effects and closure: 6.
* Decision: 1.
* Contrasts (additive arithmetic, authority claim): 3.
* Chart elements and market detail: 3+.

## 11. Golden-output checklist

* State-level (not island-level) market totals.
* Real daily spend deflated by Urban Hawaii CPI.
* LMDI weights; exact closure.

## 12. Build notes (scope tuning)

* Choose years in which a high-daily-spend, short-stay market rebounded and local inflation exceeded 4%; confirm the real daily-spend effect is below
  50% of the change.

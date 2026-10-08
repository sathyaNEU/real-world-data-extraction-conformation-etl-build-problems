# RC01 — Why did online conversion fall? A traffic surge from one channel is not a broken checkout

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Conversion-drop investigations at e-commerce and app companies (channel mix shifts versus funnel breakage by device, browser or release) |
| Domain | E-commerce analytics |
| Task shape | 09 · Funnel or chain of stages (session → product view → add to cart → checkout → purchase; the stage and segment that explain the drop, and the team that owns it) |
| Core method | Stage-by-stage conditional rates by segment (channel × device); decompose the change in overall conversion into mix (share of sessions by segment) and within-segment rate changes per stage (sequential decomposition with the memo's ordering); identify the stage × segment with the largest rate-driven contribution |
| Analytical stump | Comparing overall stage conversion rates before and after attributes a mix shift (a surge of low-intent referral/social traffic) to the checkout. Only after removing mix does the true rate change show up — or not. Conversely, a real drop concentrated in one device can be masked by favourable mix elsewhere |
| Primary sources | Google Analytics 360 sample dataset for the Google Merchandise Store (BigQuery public dataset `google_analytics_sample.ga_sessions_*`) |

## 1. The real-world situation

An online merchandise store's conversion rate fell between two four-week periods. The product team suspected a checkout bug from a recent release
and was about to roll it back. The analytics lead noted that a marketing partnership had sent a surge of referral traffic in the later period.

## 2. The decision (one deterministic recommendation)

**The stage × segment that accounts for the largest share of the rate-driven conversion change (after mix), its contribution, and whether a rollback
of the checkout release is justified (only if the checkout→purchase rate fell within desktop direct/organic traffic).**

Rules (analytics memo):

* Data: ga_sessions tables for period A and period B (dates in memo).
* Segments: channelGrouping (Organic Search, Direct, Referral, Social, Paid Search, Affiliates, Display, Other) × device category (desktop, mobile,
  tablet).
* Stages from hits: product detail view, add to cart, checkout (checkout step 1), transaction (per the eCommerce action types).
* Conversion = sessions with a transaction ÷ sessions.
* Decomposition: Δ overall conversion = mix effect (Σ (share_B − share_A) × conv_A) + rate effect (Σ share_B × (conv_B − conv_A)); rate effect further
  split across stages by the product of conditional rates in stage order (memo's sequential method).
* Rollback rule above.

## 3. Why capable analysts get it wrong

* Overall funnel charts are the default diagnostic.
* Low-intent traffic lowers every stage's average conversion without any defect.
* Stage effects interact; a sequential decomposition with a fixed order is needed for determinism.
* Segments must be defined before looking (to avoid fishing).

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `ga_sessions_period_A.parquet` (export) | Parquet | ~70k sessions | BigQuery public dataset `bigquery-public-data.google_analytics_sample` | Google public dataset terms (sample data) | Sessions, hits, channel, device |
| 2 | `ga_sessions_period_B.parquet` | Parquet | ~80k sessions | Same | Same | Same |
| 3 | `ga360_bigquery_export_schema.html` | HTML | — | Google Analytics documentation | Public | Field definitions |
| 4 | `extraction_queries.sql` | SQL | — | Task author | — | Reproducible extraction |
| 5 | `analytics_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `product_team_funnel.xlsx` | XLSX | — | Task author | — | Overall funnel comparison |
| 7 | `release_notes.json` | JSON | — | Task author | — | Release timing (context) |

## 5. Deterministic solution path

1. Build session-level stage flags; segments; period labels.
2. Shares, conversion and stage rates per segment and period.
3. Mix and rate effects; sequential stage split; largest contribution.
4. Rollback rule; contrast with the overall funnel.

## 6. Wrong paths (method errors, not misreadings)

**A — overall funnel comparison.** Mix shift blamed on checkout.

**B — mix-only explanation without checking within-segment rates.** May miss a real device-specific drop.

**C — unordered stage attribution.** Non-deterministic splits.

**D — hit-level instead of session-level stages.** Inflated counts.

## 7. Why the stump is analytical, not semantic

Segments, stages and decomposition are specified. The trap is confusing composition change with performance change.

## 8. Draft task prompt (prose)

> Why did conversion fall, and should we roll back the checkout release? Decompose the change by funnel stage and channel × device as the analytics memo
> specifies. Provide `conversion_decomposition.csv` (segment × stage: shares, rates, mix and rate contributions), `funnel_waterfall.png`, and a one-page
> `conversion_rca.pdf`.

## 9. Deliverables

* `conversion_decomposition.csv`, `funnel_waterfall.png`, `conversion_rca.pdf`.

## 10. Where 25+ rubric criteria come from

* Overall Δ; mix and rate totals; contributions for 8 segment × stage cells; top cell; rollback call.

## 11. Golden-output checklist

* Stage flags; segments; decomposition formulas; ordering; rule.

## 12. Build notes (scope tuning)

* Choose periods in the sample date range where referral share jumps; confirm mix explains > 60% of the drop.

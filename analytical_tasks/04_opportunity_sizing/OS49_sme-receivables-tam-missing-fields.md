# OS49 — Invoice-finance market from company accounts: the smallest firms don't report the field you need

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | TAM built from records where a key field is missing for a systematic subset (micro-accounts without revenue, users without demographics, devices without telemetry) |
| Domain | SME lending / fintech |
| Task shape | 07 · Grid of cells (industry section × size band → trade receivables outstanding; the segment targeted for an invoice-finance product) |
| Core method | Parse filed accounts (iXBRL) for trade debtors; for filers without a debtors line (micro-entity abridged accounts), impute debtors from current assets using the debtors ÷ current-assets ratio of comparable small-company filers in the same industry and size band (ratio estimator); aggregate by segment; contrast with complete-case totals |
| Analytical stump | Summing debtors from accounts that report them silently drops micro-entities (the majority of companies), understating the market; scaling the complete-case total by company counts assumes micro firms hold receivables like larger small firms. Field missingness is driven by filing regime (size), so imputation must condition on size and industry |
| Primary sources | UK Companies House Accounts Data Product (daily/monthly iXBRL accounts bulk files); Companies House basic company data (SIC codes) |

## 1. The real-world situation

A fintech sizes the UK market for invoice finance by summing trade debtors in companies' filed accounts. The analyst used only accounts with a
trade-debtors tag and found a market dominated by medium-sized firms. The product targets micro and small firms, which mostly file abridged
micro-entity accounts without a debtors line.

## 2. The decision (one deterministic recommendation)

**The target segment (industry section × size band with the largest estimated receivables among micro and small companies), with the grid of
estimated receivables.**

Rules (strategy memo):

* Data: Companies House accounts bulk files for the 12 months in memo (latest accounts per company); basic company data for SIC codes.
* Size band by filing type/balance sheet total: micro (micro-entity accounts), small (small company accounts), medium/large excluded.
* Debtors: iXBRL tags for trade debtors (memo's taxonomy list); current assets tag.
* Imputation for micro filers lacking debtors: debtors = current assets × r(industry section), where r = Σ debtors ÷ Σ current assets among small
  filers in the same section with both tags and balance sheet total ≤ £1M (the most comparable group per memo).
* Segment totals = reported + imputed.
* Target = highest total among micro and small segments.
* Report complete-case totals for contrast.

## 3. Why capable analysts get it wrong

* Complete-case analysis is the default when a field is missing.
* Missingness is structural (filing regime), not random.
* Scaling by counts ignores that micro firms are smaller.
* The auxiliary variable (current assets) is reported by almost all filers.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–12 | `Accounts_Monthly_Data-<Month><Year>.zip` | iXBRL/HTML inside ZIP | ~200–300k accounts per month | Companies House Accounts Data Product | Open Government Licence v3 | Filed accounts |
| 13 | `BasicCompanyDataAsOneFile-<date>.csv` | CSV | ~5.5M | Companies House | OGL v3 | Company status, SIC codes |
| 14 | `uk_gaap_frs_taxonomy_tags.json` | JSON | ~50 | Task author (from FRC taxonomy) | OGL-derived | Tag lists |
| 15 | `sic_to_section.csv` | CSV | ~730 | ONS | OGL | Industry sections |
| 16 | `strategy_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 17 | `analyst_complete_case.xlsx` | XLSX | — | Task author | — | Naive sizing |
| 18 | `parsed_accounts.parquet` | Parquet | ~2.5M | Derived | OGL | Extracted values |

## 5. Deterministic solution path

1. Parse latest accounts per company; extract tags; classify size bands.
2. Compute ratios among small filers; impute micro debtors.
3. Segment totals; target; contrast.

## 6. Wrong paths (method errors, not misreadings)

**A — complete cases only.** Micro firms dropped.

**B — scaling by company counts.** Size mismatch.

**C — ratio from all filers including medium.** Not comparable.

**D — keeping older accounts for the same company.** Double counting.

## 7. Why the stump is analytical, not semantic

Tags, bands and the estimator are specified. The trap is non-random missingness in sizing.

## 8. Draft task prompt (prose)

> Which segment should our invoice-finance product target? Estimate trade receivables for micro and small companies from Companies House accounts,
> imputing where micro accounts omit debtors, as the strategy memo specifies. Provide `receivables_grid.csv` (section × band: companies, reported,
> imputed, total), `receivables_heatmap.png`, and a one-page `target_segment.pdf`.

## 9. Deliverables

* `receivables_grid.csv`, `receivables_heatmap.png`, `target_segment.pdf`.

## 10. Where 25+ rubric criteria come from

* ~10 sections × 2 bands totals = 20; ratios for 10 sections; target; contrast.

## 11. Golden-output checklist

* Latest accounts; tags; bands; ratio population; imputation; totals.

## 12. Build notes (scope tuning)

* Confirm micro-entity imputed totals change the target segment versus complete cases.

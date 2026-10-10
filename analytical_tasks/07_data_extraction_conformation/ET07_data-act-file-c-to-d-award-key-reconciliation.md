# ET07 — Federal spending C-to-D reconciliation: the contract key that is four columns, not one

| Field | Value |
|---|---|
| Domain | Federal financial management / DATA Act reporting / grants & contracts transparency |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 03 · Bridge between two totals (File C award obligations ↔ File D1 contract transactions) |
| Core technique | Composite natural-key construction (PIID + parent IDV PIID + agency codes); account-key fidelity (full TAS incl. allocation-transfer agency and DEFC); period alignment |
| Trap family (honest data) | Linking on PIID alone creates false links that net variances away; TAS collapsed to agency+main account |
| Primary sources | USAspending.gov custom account downloads (File A/B/C), award transaction downloads (File D1), DAIMS documentation |

## 1. The real-world project

An agency's Office of the CFO prepares its quarterly DATA Act certification. The Senior Accountable Official must
explain differences between **File C** (award-level obligations recorded in the financial system, by Treasury Account
Symbol) and **File D1** (contract actions reported to FPDS). A data engineer built the linkage on `piid`, because
"PIID is the contract number". Reported variances were small and certification went through. The Inspector General's
DATA Act audit sample found linked pairs that were two different contracts.

## 2. The business decision (one deterministic recommendation)

**Which sub-tier bureau must the SAO escalate for FY2024 Q2 — the bureau with the largest absolute unexplained
contract-obligation variance between File C and File D1 after correct linkage — and how large is it?**

Rules (certification procedures):

* Contract award key = `PIID` + `parent_award_id` (referenced IDV PIID; empty for definitive contracts/IDVs) + awarding
  agency code + parent award agency code — the same composition USAspending uses for its generated unique award key.
  Comparisons are case-insensitive with surrounding whitespace removed; no other normalization.
* File C side: sum `transaction_obligated_amount` for contract rows in the quarter's submission, grouped by award key and
  by full TAS (ATA, AID, BPOA, EPOA, availability type, main, sub) and disaster emergency fund code (DEFC).
* File D1 side: sum `federal_action_obligation` for actions with action date in the quarter, by award key.
* Variance categories (applied in order): (1) linked & equal; (2) linked, timing (D action date in quarter but C
  recorded in an adjacent quarter, matched across the ±1 quarter files); (3) unlinked in C; (4) unlinked in D; (5)
  linked residual.
* Unexplained variance = categories 3 + 4 + 5 in absolute dollars.

## 3. Why this gets overlooked in real projects

* PIID is printed on every contract and is unique *within an awarding office's definitive contracts*, but task and
  delivery orders are numbered within their parent IDV — order "0001" exists under thousands of IDVs.
* Joining on PIID alone usually finds *a* match, so unmatched rates look excellent; false links pair unrelated
  obligations whose differences partially cancel.
* TAS strings are long; engineers group on agency + main account and lose the allocation-transfer agency and sub-account,
  merging accounts owned by different bureaus.
* Since FY2020, DEFC splits the same TAS into several lines; dropping it duplicates rows on join.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–3 | `fileC_FY2024Q1.csv`, `fileC_FY2024Q2.csv`, `fileC_FY2024Q3.csv` (Account Breakdown by Award) | CSV | 100k–500k each | USAspending custom account download | U.S. Gov public domain | Award-level obligations by TAS/DEFC |
| 4 | `fileB_FY2024Q2.csv` (Program Activity & Object Class) | CSV | ~50k | USAspending | Public domain | Context: award vs non-award object classes |
| 5 | `fileA_FY2024Q2.csv` (Account Balances) | CSV | ~5k | USAspending | Public domain | TAS totals |
| 6–8 | `contracts_prime_transactions_FY2024Q1..Q3.csv` (D1) | CSV | 200k–1M each | USAspending award download | Public domain | Contract actions |
| 9 | `agency_codes.xlsx` (toptier/subtier, CGAC/FREC) | XLSX | ~1.5k | USAspending reference data | Public domain | Bureau mapping |
| 10 | `daims_v2_dictionary.xlsx` + `daims_validation_rules.xlsx` | XLSX | — | Treasury DAIMS | Public domain | Field semantics, C↔D validation rules |
| 11 | `tas_components_reference.pdf` (Treasury FAST Book extract) | PDF | — | Bureau of the Fiscal Service | Public domain | TAS composition |
| 12 | `certification_procedures.pdf` | PDF | — | Task author | — | Rules in §2 |
| 13 | `award_search_api_sample.json` | JSON | ~1k | USAspending API | Public domain | Spot-check of generated unique award keys |

## 5. Deterministic solution path

1. Restrict both sides to the agency; build the four-part award key on both sides.
2. Aggregate C by key (and keep TAS/DEFC detail for bureau attribution via the TAS owner/sub-tier mapping); aggregate D1
   by key.
3. Full outer join on key; classify each key into categories 1–5, using Q1/Q3 files to identify timing.
4. Attribute each key to a sub-tier bureau (awarding sub-tier on D; TAS-derived bureau on C-only keys).
5. Sum unexplained variance by bureau; rank; escalate the largest.
6. Re-run the join on PIID only to quantify false links and show how the ranking changes.

## 6. The traps

**Trap A — PIID-only join.** False links between same-numbered orders under different IDVs net variances; a different
bureau appears largest; "unlinked" counts look implausibly good.

**Trap B — two-part key without agency codes.** Same IDV PIID reused by different agencies' contracting offices links
across agencies.

**Trap C — collapsed TAS / dropped DEFC.** Bureau attribution of C-only keys moves to the wrong bureau; row duplication
inflates C totals.

**Trap D — no timing category.** Treats legitimate quarter-boundary timing as unexplained; inflates a bureau that
obligates heavily at quarter end.

## 7. Why the data is honest

Files C and D1 are the agency's and FPDS's official submissions as published. The composite award key is documented in
DAIMS and reflected in USAspending's own generated award IDs. Variances are real; the work is linking correctly.

## 8. Draft task prompt (prose)

> The SAO needs to know which bureau to escalate in our FY2024 Q2 DATA Act certification: the one with the largest
> unexplained contract-obligation variance between File C and File D1 under our certification procedures. Using the
> account and award downloads in the folder, link every contract award, classify the variance, and tell me the bureau and
> the amount. Deliver `c_to_d_bridge.xlsx` with a bureau summary (C total, D1 total, linked-equal, timing, unlinked-C,
> unlinked-D, residual, unexplained) and a key-level detail sheet, plus `c_to_d_waterfall.png` walking the agency's File
> C total to its File D1 total, one bar per category, with the escalated bureau's share highlighted. In the summary
> sheet's header note, state how many links a PIID-only join creates that do not exist under the full key and whether
> that join would have escalated a different bureau.

## 9. Deliverables

* `c_to_d_bridge.xlsx` (summary + detail), `c_to_d_waterfall.png`.

## 10. Where 25+ rubric criteria come from

* Per-bureau variance categories (≈6 bureaus × 4–5 categories); agency waterfall bars; escalated bureau and amount;
  false-link count; PIID-only escalation alternative.

## 11. Golden-output checklist

* Four-part key; full TAS + DEFC; timing via adjacent quarters; bureau ranking stated; bridge reconciles exactly.

## 12. Build notes (scope tuning)

* Choose an agency with heavy IDV/task-order use (many repeated order PIIDs) and at least two bureaus within 30% of each
  other in unexplained variance; confirm the PIID-only join flips the escalation.
* Copy the exact field names from the downloaded files into the procedures memo; USAspending column names evolve.

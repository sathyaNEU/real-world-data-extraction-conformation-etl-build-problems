# leak check, task485

**Verdict: REVIEW.** 14 files read, 36 golden figures and 5 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: manufacturer, architecture, remittances, supplies, reader, ingredient, nothing, sentence, attribution, family, accounts, service, adalimumab-kvrn, statement, register, policy, network, checks, saltiva, remittance, decisive, landed, completion, objective, empriva

## 1 file names (REVIEW 1)
- **REVIEW** `pharmacy_network_202610.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `clinical_review_2027_pdl.pdf`: golden figure 250 appears: ...25 mcg inhaler); Saltiva (fluticasone propionate 250 mcg/salmeterol 50 mcg inhaler) The three combinat...
- **REVIEW** `clinical_review_2027_pdl.pdf`: golden figure 100 appears: ...d. Long-acting insulins Glarvia (insulin glargine 100 units/mL pen); Deglutra (insulin degludec 100 uni...
- **REVIEW** `rebate_guarantee_reconciliation_fy2025.pdf`: golden figure 350 appears: ...SD) Jul-Sep 2024 8,829 627 782 528 3,241,314.00 3,350,588.42 0.00 Oct-Dec 2024 9,150 613 731 487 3,212,...
- **REVIEW** `clinical_review_2027_pdl.pdf`: carries 25 of 27 distinctive words of the committed call: 'Prefer Velantro (GLP-1 receptor agonists), Empriva (SGLT2 inhibitors), Glarvia (Long-acting insulins), Apiqor (Direct or'

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `clinical_review_2027_pdl.pdf`: 4 of 25 stump-paragraph terms appear (adalimumab-kvrn, policy, saltiva, empriva); read whether the document names the move
- **REVIEW** `pbm_agreement_exhibit_c.pdf`: 5 of 25 stump-paragraph terms appear (manufacturer, service, statement, network, remittance); read whether the document names the move
- **REVIEW** `pdl_2027_implementation_messages.pdf`: 3 of 25 stump-paragraph terms appear (nothing, statement, remittance); read whether the document names the move
- **REVIEW** `pdl_policy_eb-rx-04.pdf`: 7 of 25 stump-paragraph terms appear (manufacturer, remittances, supplies, ingredient, statement, policy); read whether the document names the move
- **REVIEW** `rebate_guarantee_reconciliation_fy2025.pdf`: 3 of 25 stump-paragraph terms appear (service, network, remittance); read whether the document names the move

## 5 announcements (REVIEW 1)
- **REVIEW** `prompt`: What should the Employees' Group Health Plan put on the preferred tier of its 2027 drug list in each brand class the Pharmacy and Therapeutics Committee is reviewing?

## 6 ranking artifacts (REVIEW 5)
- **REVIEW** `rebate_remittance_2025Q2.xlsx`: names 4 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `rebate_remittance_2025Q3.xlsx`: names 4 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `rebate_remittance_2025Q4.xlsx`: names 4 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `rebate_remittance_2026Q1.xlsx`: names 4 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `rebate_remittance_2026Q2.xlsx`: names 4 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 2 author vocabulary (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read (the isolated leak reader)

1. Decisive step: none stated; the nearest is policy EB-RX-04 3.2 (net cost per 30-day supply is the ingredient cost paid on the product's claims less the rebates the product's manufacturer paid the Plan on those claims, divided by the 30-day supplies dispensed), the estimand and not a step; no file says how a manufacturer-level rebate splits across its products.
2. Nothing ranks or scores the candidates (remittances by manufacturer and account only; the FY2025 reconciliation covers the guarantee, not the classes).
3. Nothing exists only to help the analyst (the pharmacy network export and the drug file are lookups the claims need).
4. Nothing reads as the answer (the only product-level figures are the clinical review's 30-day quantities).
5. Policy 3.1 and 3.2 read literally: per product, the ingredient cost on its non-reversed fiscal-year claims less the rebates its manufacturer paid on those claims, over the 30-day supplies dispensed, lowest in each class; 3.3 fixes the fiscal year as the latest with all four remittances received; which product's claims carry which share of a manufacturer's rebate is left to the analyst.
6. An analytical choice (attributing manufacturer-level rebates to individual products); nothing planted.
Sweep flags: the clinical review is harmless (compared products, packs and 30-day quantities; no preferred product, cost, rank or step); the remittance workbooks are harmless (manufacturers by account and line type, no product, no net cost, no per-product rebate); the pharmacy network text file is the organisation's own pipe-delimited export with a header and no prose; Exhibit C, the policy, the implementation messages and the FY2025 reconciliation are harmless (guarantee terms for the asks, the estimand and fiscal-year rule, scheduling chatter, a prior-year table showing no shortfall; none says how to split a manufacturer's rebate).
Realism: none generated (memo, contract and policy prose; remittance header blocks, summaries and prior-period lines; an account code change and a legacy cardholder id read as real-system mess); minor: the clinical review's comparability notes are slightly tidy but read as a pharmacist's memo.

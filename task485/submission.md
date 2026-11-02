## Tags

**Domain:** Healthcare Delivery & Health Economics, payment, claims and health plan analytics.
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Prefer Velantro (GLP-1 receptor agonists), Empriva (SGLT2 inhibitors), Glarvia (Long-acting insulins), Apiqor (Direct oral anticoagulants), Brezara (Inhaled corticosteroid and LABA combinations) and adalimumab-kvrn (Adalimumab products) on the 2027 preferred drug list.** Each has its class's lowest fiscal 2026 net cost per 30-day supply once every manufacturer's remittances are traced to the products that earned them: Velantro $510 against Liraquent $600, Glarvia $100 against Deglutra $170 and Brezara $200 against Vilaro $250. Not Liraquent, insulin glargine-qmrt or Saltiva, which lead their classes only when each manufacturer's remittances are spread over its products by ingredient cost, giving every product its manufacturer's average rebate.

## 2. Critical Components

Net cost per 30-day supply, fiscal 2026:

1. GLP-1 receptor agonists: Velantro **$510**, Liraquent **$600**, Dulmira **$620**
2. SGLT2 inhibitors: Empriva **$260**, Daplexa **$350**, Canivo **$370**
3. Long-acting insulins: Glarvia **$100**, Deglutra **$170**, insulin glargine-qmrt **$210**
4. Direct oral anticoagulants: Apiqor **$370**, Ravelta **$450**; Inhaled corticosteroid and LABA combinations: Brezara **$200**, Vilaro **$250**, Saltiva **$260**
5. Adalimumab products: adalimumab-kvrn **$1,190**, Advelis **$3,060**, Adalvane **$3,690**

## 3. Step-by-Step Solution

1. Conformed pbm_paid_claims_fy2026.csv: removed every paid claim that a reversal row names in reversal_of, read both NDC and date layouts, and mapped group codes 100, 200, 300 and 400 to the accounts' new codes.
2. Took each compared product's ingredient cost paid and its 30-day supplies (quantity over the 30-day quantity in clinical_review_2027_pdl.pdf) on its fiscal 2026 claims, per policy EB-RX-04.
3. Read the five rebate_remittance statements and assigned every current quarter and prior period line to its quarter of service and plan account, leaving out the lines for fiscal 2025 service.
4. For each manufacturer, fitted its fiscal 2026 remittances per account and quarter of service on the 30-day supplies of every product it supplies in the same account and quarter (least squares; the fit is exact to the cent), giving each product's rebate per 30-day supply and its fiscal 2026 rebates.
5. Divided each product's ingredient cost less its rebates by its 30-day supplies, giving the net costs in block 2.
6. Counted fiscal 2026 brand claims (compound claims out) by quarter of service and by the pharmacy's network on the date of service per Exhibit C, a claim carrying the retail dispensing fee as retail (the three hospital outpatient pharmacies that pharmacy_network_202610.txt lists as specialty were retail until 1 May 2026), priced them at Exhibit C's rates and set them against every remittance line for that quarter's service.Matched each claim before 1 January 2026 to member_roster_20261009.csv through the subscriber's legacy_cardholder_id and the member's birth date and gender, and counted the distinct members with a paid claim in each class under each account.
7. Preferred the product with the lowest net cost per 30-day supply in each class, per the policy.

## 4. Deliverable Answers

### pdl_2027_net_cost.xlsx

1. Net cost per 30-day supply, fiscal 2026, to the nearest ten dollars:
   - GLP-1 receptor agonists: Velantro $510, preferred
   - GLP-1 receptor agonists: Liraquent $600
   - GLP-1 receptor agonists: Dulmira $620
   - SGLT2 inhibitors: Empriva $260, preferred
   - SGLT2 inhibitors: Daplexa $350
   - SGLT2 inhibitors: Canivo $370
   - Long-acting insulins: Glarvia $100, preferred
   - Long-acting insulins: Deglutra $170
   - Long-acting insulins: insulin glargine-qmrt $210
   - Direct oral anticoagulants: Apiqor $370, preferred
   - Direct oral anticoagulants: Ravelta $450
   - Inhaled corticosteroid and LABA combinations: Brezara $200, preferred
   - Inhaled corticosteroid and LABA combinations: Vilaro $250
   - Inhaled corticosteroid and LABA combinations: Saltiva $260
   - Adalimumab products: adalimumab-kvrn $1,190, preferred
   - Adalimumab products: Advelis $3,060
   - Adalimumab products: Adalvane $3,690
2. Preferred product for 2027:
   - GLP-1 receptor agonists: Velantro
   - SGLT2 inhibitors: Empriva
   - Long-acting insulins: Glarvia
   - Direct oral anticoagulants: Apiqor
   - Inhaled corticosteroid and LABA combinations: Brezara
   - Adalimumab products: adalimumab-kvrn
3. Rebate guarantee by fiscal 2026 quarter (brand claims by channel, guarantee, rebates remitted for the quarter's claims, shortfall):
   - Jul-Sep 2025: retail under 84 days 9,484 claims, retail 84 days or more 654, mail order 839, specialty 572; guarantee $3,476,679; remitted $3,648,387; no shortfall
   - Oct-Dec 2025: retail under 84 days 9,570 claims, retail 84 days or more 659, mail order 792, specialty 535; guarantee $3,419,630; remitted $3,589,228; no shortfall
   - Jan-Mar 2026: retail under 84 days 9,653 claims, retail 84 days or more 685, mail order 818, specialty 466; guarantee $3,373,898; remitted $3,453,527; no shortfall
   - Apr-Jun 2026: retail under 84 days 9,573 claims, retail 84 days or more 652, mail order 798, specialty 610; guarantee $3,519,558; remitted $3,469,210; shortfall $50,348
4. Members with a paid claim in each reviewed class, by employer account:
   - GLP-1 receptor agonists: State Agencies 533, Higher Education 201, Local Government 203, Non-Medicare Retirees 151
   - SGLT2 inhibitors: State Agencies 386, Higher Education 147, Local Government 152, Non-Medicare Retirees 175
   - Long-acting insulins: State Agencies 208, Higher Education 71, Local Government 90, Non-Medicare Retirees 116
   - Direct oral anticoagulants: State Agencies 181, Higher Education 56, Local Government 78, Non-Medicare Retirees 159
   - Inhaled corticosteroid and LABA combinations: State Agencies 317, Higher Education 180, Local Government 129, Non-Medicare Retirees 93
   - Adalimumab products: State Agencies 74, Higher Education 35, Local Government 30, Non-Medicare Retirees 19

### pdl_2027_trustees.pptx

1. Slide 1 names the preferred product in each class with its net cost per 30-day supply and the next lowest product.
2. Slide 2 charts every compared product's net cost per 30-day supply by class, the preferred product's bar in green, adalimumab products on their own scale.

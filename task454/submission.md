## Tags

**Domain:** Survey Research & Official Statistics (census, register and administrative data quality: a state tourism commission's regional visitor spending built from a card scheme's de-identified point-of-sale research sample, each card's usual environment read from its own presence).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Fund Jabiru Coast, Lyrebird Peninsula, Spinifex Gorges, Tingle Ranges and Yallambee Valley in the 2027 round, each receiving $1,771,508: they are the five eligible regions with the highest 2026 visitor spending per resident, Yallambee Valley fifth at $4,150 and Pelican Coast first below the line at $3,205, $945 short.**
Not Gidgee Basin or Carisbrook Tablelands, which rank among the five only when every card is placed at its statement address: most of the spending there on cards billed elsewhere belongs to rostered mine workers, students, commuters and households that moved in, whose cards are in the region month after month, so it is not visitor spending ($2,657 and $2,547 per resident once it is taken out). Not Pelican Coast, $945 short of Yallambee Valley.

## 2. Critical Components

1. Every card-region pair in the 2026 research sample is either a trip, at most 3 months and 21 days in the region, or part of the holder's routine, 8 months or more and 59 days or more; the routine regions are the card's usual environment, whatever address its statements go to.
2. Yallambee Valley is fifth at **$4,150** per resident and Pelican Coast first below the line at **$3,205**, **$945** short.
3. Gidgee Basin and Carisbrook Tablelands carry **$2,657** and **$2,547** per resident, seventh and eighth.

## 3. Step-by-Step Solution

1. Joined the research sample's 148,555 card-region-month rows (12,201 cards) to the card register's selection weights by card_id, and laid Schedule 1 of rvif_2027_round_guidelines.pdf (each region's SA3s, the four shared SA2s at their shares) over erp_sa2_30jun2026_preliminary.csv for each eligible region's residents (section 4).
2. Read each card's usual environment from its own rows: a region the card is in for 8 months or more and on 59 days or more is part of it, and every other card-region pair is at most 3 months and 21 days, a trip; no pair falls between, so every threshold in the gap gives the same classes, and the statement SA2 is not read.
3. Raised each card's spending outside its usual environment by its selection weight, summed it by merchant region and calendar quarter, divided each region's 2026 total by its residents and ranked (section 4): Yallambee Valley fifth at $4,150, Pelican Coast sixth at $3,205.
4. Booked each 2026 transfer in ap_payments_rtip_2026.csv to the claims it paid: finance pays a council's approved claims in one Thursday transfer quoting the agreement of the first claim, so each transfer is split into the one combination of the council's earlier approved claims that sums to it (an acquitted agreement's retention travels with an open agreement's milestone); the 20 March transfers repeat the 19 March run and are dropped; claims approved on 29 and 30 December and those held had not been paid by 31 December 2026. What remained of each open agreement is its approved amount less what was paid, as the closure decision's third paragraph defines it: $3,852,430 across the regions.
5. Split each 2026 receipt in ar_receipts_rtip_2026.csv into what it returns: a receipt equal to a council's repeat returns that repeat, and a receipt equal to a repeat plus what an acquitted agreement left unspent (its paid amount less its final cost) returns both, only the second being unspent money; three councils had not returned their repeat by 31 December 2026. Unspent money returned in 2026, as the closure decision's fourth paragraph counts it: $709,970 across the regions.
6. The round's total is the 2027 appropriation of $12,000,000 plus $709,970 less $3,852,430, $8,857,540, as the guidelines' second section and the closure decision's fifth paragraph set it, shared equally: $1,771,508 each.
7. Fund Jabiru Coast, Lyrebird Peninsula, Spinifex Gorges, Tingle Ranges and Yallambee Valley.

## 4. Deliverable Answers

### regional_visitor_spend_2026.csv

1. Each eligible region's 2026 visitor spending by quarter and its 2026 total, each to the nearest thousand dollars, and its visitor spending per resident to the nearest dollar:
   - Jabiru Coast: Q1 $139,877,000, Q2 $122,831,000, Q3 $135,041,000, Q4 $123,129,000; the year $520,878,000; $10,149 per resident
   - Lyrebird Peninsula: Q1 $99,841,000, Q2 $104,262,000, Q3 $94,213,000, Q4 $104,719,000; the year $403,034,000; $5,894 per resident
   - Spinifex Gorges: Q1 $14,924,000, Q2 $12,933,000, Q3 $12,046,000, Q4 $11,295,000; the year $51,198,000; $5,197 per resident
   - Tingle Ranges: Q1 $26,613,000, Q2 $29,475,000, Q3 $29,699,000, Q4 $18,079,000; the year $103,866,000; $4,272 per resident
   - Yallambee Valley: Q1 $28,939,000, Q2 $33,132,000, Q3 $33,813,000, Q4 $31,861,000; the year $127,746,000; $4,150 per resident
   - Pelican Coast: Q1 $57,148,000, Q2 $54,518,000, Q3 $58,562,000, Q4 $63,851,000; the year $234,079,000; $3,205 per resident
   - Gidgee Basin: Q1 $15,704,000, Q2 $14,199,000, Q3 $12,875,000, Q4 $14,682,000; the year $57,460,000; $2,657 per resident
   - Carisbrook Tablelands: Q1 $27,216,000, Q2 $30,417,000, Q3 $31,180,000, Q4 $26,718,000; the year $115,532,000; $2,547 per resident
   - Lower Wollomby: Q1 $14,623,000, Q2 $12,051,000, Q3 $15,798,000, Q4 $16,494,000; the year $58,966,000; $1,521 per resident
   - Mulga Plains: Q1 $9,569,000, Q2 $11,142,000, Q3 $9,829,000, Q4 $8,261,000; the year $38,801,000; $1,387 per resident
   - Port Kelburn: Q1 $17,113,000, Q2 $19,882,000, Q3 $19,358,000, Q4 $15,878,000; the year $72,231,000; $1,167 per resident

### rvif_2027_round_paper.docx

1. Regions funded: Jabiru Coast, Lyrebird Peninsula, Spinifex Gorges, Tingle Ranges and Yallambee Valley.
2. First region below the line: Pelican Coast at $3,205 per resident, $945 short of Yallambee Valley at $4,150.
3. Horizontal bar chart of every eligible region's 2026 visitor spending per resident with the funding line marked between Yallambee Valley and Pelican Coast, the funded regions in blue (Figure 1).
4. Each funded region receives $1,771,508.
5. For each region, what remained at 31 December 2026 of the Regional Tourism Infrastructure Program's open agreements and the unspent money its councils returned in 2026 (nearest dollar):
   - Jabiru Coast: remaining $506,601; unspent money returned $76,015
   - Lyrebird Peninsula: remaining $170,544; unspent money returned $151,408
   - Yallambee Valley: remaining $430,427; unspent money returned $34,369
   - Spinifex Gorges: remaining $242,639; unspent money returned $35,438
   - Tingle Ranges: remaining $78,062; unspent money returned $120,613
   - Pelican Coast: remaining $586,137; unspent money returned $49,918
   - Gidgee Basin: remaining $136,751; unspent money returned $23,772
   - Carisbrook Tablelands: remaining $507,843; unspent money returned $65,920
   - Lower Wollomby: remaining $315,531; unspent money returned $78,703
   - Mulga Plains: remaining $593,995; unspent money returned $48,060
   - Port Kelburn: remaining $283,900; unspent money returned $25,754

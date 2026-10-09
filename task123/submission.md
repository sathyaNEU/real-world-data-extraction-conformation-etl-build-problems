# task123 · Steady Ground Fund, September 2026 stabilisation offers

## Tags

**Domain:** Nonprofit & Grant-making (grantee financial health: a community trust's stabilisation offers scored on its grantees' falls in income).
**Analytical objective:** Data Extraction & Conformation (ETL) (versioned quarterly grantee returns, dual-grant filings, a form revision, a charities register match and an offers schedule conformed into one screen that reproduces the bureau's published runs).

## 1. Final Recommendation

**Strike the September 2026 Steady Ground offers at 42.55 cents per dollar of fall: 9 offers totalling $559,969 of the $560,000 pot.**

The rate comes from the screen that gives back all 797 rows of Ledgerwood's six March runs, read with rule 4.1 against 31 March 2026, the census before this one. Not the screen that also scores the 14 grantees balancing at 31 March on twelve months to December 2025, which end before that census. Not the rate from the latest quarter built on management fourth quarters, which scores grantees whose annual return was not yet on the register and misses Ledgerwood's rows wherever a return had not reached the register by a March census. Not the rate from the latest versions in today's portal, which uses restatements accepted after a census. Not one row per grant return, which scores dual-grant organisations twice against rule 3.3. Not the filed financial years on the register, which match almost none of the published twelve-month figures.

## 2. Critical Components

1. The in-house screen gives back **797 of 797** published rows, every offer and all six rates of Ledgerwood's March runs
2. Twelve-month income must end on or after **31 March 2026** (rules 2 and 4.1), so the **14** grantees balancing at 31 March with no 2025-26 annual return on the register, whose twelve months stop at **December 2025**, are not scored, while the **17** balancing at 30 June are scored to **March 2026**
3. **132** grantees are scored and **9** fall by 10 per cent or more
4. The 9 offers total **$559,969**, leaving **$31** of the **$560,000** pot in the Fund

## 3. Step-by-Step Solution

1. Took each organisation's quarters from `portal_return_lines_2018q3_2026q2.csv` as held at each census (accepted versions by `accepted_at`, census day included), pooled across its grants in `grants_register_20261007.xlsx` (rule 3.3), year to date differenced into quarters.
2. Admitted a year's final quarter only as `total_gross_income` in `charities_register_returns_extract_20261007.csv` less the nine-month year to date, from its `date_received`, stepping both twelve-month windows back where the return was not yet received.
3. Replayed the six March censuses at each pack's pot (`SGF_screen_run_2021-03.xlsx` to `SGF_screen_run_2026-03.xlsx`): 797 of 797 rows, every offer and all six rates given back, as the cutover standard's clause 4 requires.
4. At 30 September 2026 the census before is 31 March 2026 (`SGF_round_rules_rev2026-06.pdf`, rules 2 and 4.1): the 17 grantees balancing at 30 June without a 2025-26 return are scored to March 2026, the 14 balancing at 31 March would stop at December 2025 and are not scored, nor are newer grantees without both periods (rule 3.2): 132 scored.
5. Applied the 10 per cent line (rule 4.3): 9 grantees are offered, and the first outside the line is Amberley Tenancy Advocacy Service at 6.4%.
6. Struck the highest rate to the hundredth of a cent whose rounded, floored and capped offers fit the $560,000 pot in `trustees_budget_minute_2026-27_extract.pdf` (rules 5.1 to 5.3): 42.55 cents, $559,969 offered, $31 left.
7. Split each fall over the same windows into government grants and contracts (QFR-24 `GOV_GRT`, QFR-16 `GOV_GRT` plus the memo `FEE_SVC_GOV`, `govt_grants_contracts` for a final quarter) and Trust money by the quarter it reached the grantee, the basis the QFR-24 memo `GRT_NGO_APT` ties to: paid lines of `trust_payment_run_2018-07_to_2026-09.csv` by `value_date`, plus the Steady Ground instalments in the grants register's Steady Ground offers sheet on rule 7's pay day, which are in no run and which rule 5.4 leaves in income.
8. Recommendation: offer the 9 grantees at 42.55 cents per dollar of fall.

## 4. Deliverable Answers

### steady_ground_sep2026_offers.docx

1. 42.55 cents per dollar of fall
2. Grantees offered, with the government money and the Trust's own money in the fall each offer is struck on, whole NZ$ (negative where that income rose):
   - Mayfield Kai Share Cooperative: offer $150,000, government money $258,337, Trust money -$19,966
   - Woolston Sports Education Trust: offer $109,687, government money $103,487, Trust money $36,866
   - Tai Tapu Kai Share Cooperative: offer $65,770, government money $94,431, Trust money -$71,516
   - Waikari After School Care Society: offer $59,426, government money $73,145, Trust money -$8,408
   - Papanui Neighbourhood Hub Trust: offer $51,797, government money $41,328, Trust money -$6,402
   - St Albans Newcomers Network: offer $41,503, government money $54,616, Trust money -$6,718
   - Sydenham Play Resource Library Society: offer $37,183, government money $34,351, Trust money $2,078
   - Shirley Kai Share Cooperative: offer $26,129, government money $28,381, Trust money -$4,300
   - Kaiapoi Newcomers Network: offer $18,474, government money $22,709, Trust money -$2,500
3. First grantee outside the line: Amberley Tenancy Advocacy Service, fall of 6.4%
4. 132 grantees scored
5. Published grantee rows given back exactly:
   - March 2021: 118
   - March 2022: 124
   - March 2023: 131
   - March 2024: 137
   - March 2025: 142
   - March 2026: 145

### steady_ground_sep2026_screen.csv

1. 132 rows, one per scored grantee, largest fall in dollars first, whole NZ$ and percentages to one decimal:
   - CC23552 Mayfield Kai Share Cooperative: twelve-month income $2,519,857, twelve months before $2,903,600, fall $383,743, 13.2%, offer $150,000, government part $258,337, Trust part -$19,966
   - CC20936 Woolston Sports Education Trust: twelve-month income $1,150,133, twelve months before $1,407,916, fall $257,783, 18.3%, offer $109,687, government part $103,487, Trust part $36,866
   - CC45658 Tai Tapu Kai Share Cooperative: twelve-month income $1,018,170, twelve months before $1,172,742, fall $154,572, 13.2%, offer $65,770, government part $94,431, Trust part -$71,516
   - CC45324 Waikari After School Care Society: twelve-month income $911,515, twelve months before $1,051,176, fall $139,661, 13.3%, offer $59,426, government part $73,145, Trust part -$8,408
   - CC34513 Papanui Neighbourhood Hub Trust: twelve-month income $743,031, twelve months before $864,764, fall $121,733, 14.1%, offer $51,797, government part $41,328, Trust part -$6,402
   - CC27360 St Albans Newcomers Network: twelve-month income $589,578, twelve months before $687,117, fall $97,539, 14.2%, offer $41,503, government part $54,616, Trust part -$6,718
   - CC58287 Diamond Harbour Whanau Support Services: twelve-month income $1,706,427, twelve months before $1,803,834, fall $97,407, 5.4%, offer $0, government part $5,849, Trust part -$8,100
   - CC30757 Sydenham Play Resource Library Society: twelve-month income $527,761, twelve months before $615,148, fall $87,387, 14.2%, offer $37,183, government part $34,351, Trust part $2,078
   - CC54322 Shirley Kai Share Cooperative: twelve-month income $394,008, twelve months before $455,415, fall $61,407, 13.5%, offer $26,129, government part $28,381, Trust part -$4,300
   - CC56509 Kaiapoi Newcomers Network: twelve-month income $275,267, twelve months before $318,683, fall $43,416, 13.6%, offer $18,474, government part $22,709, Trust part -$2,500
   - CC59225 Amberley Tenancy Advocacy Service: twelve-month income $493,685, twelve months before $527,413, fall $33,728, 6.4%, offer $0, government part $16,613, Trust part -$1,500
   - CC31839 Mount Somers Older Persons Club: twelve-month income $795,044, twelve months before $818,126, fall $23,082, 2.8%, offer $0, government part $5,382, Trust part $0
   - CC30956 Linwood Carer Respite Network: twelve-month income $846,136, twelve months before $859,000, fall $12,864, 1.5%, offer $0, government part -$5,509, Trust part $0
   - CC44521 Mairehau Arts Trust: twelve-month income $144,064, twelve months before $150,083, fall $6,019, 4.0%, offer $0, government part not reported (short form), Trust part -$900
   - CC34551 Hanmer Springs After School Care Society: twelve-month income $159,037, twelve months before $160,136, fall $1,099, 0.7%, offer $0, government part $1,979, Trust part $0
   - CC23638 Lincoln Surplus Kai Network: twelve-month income $312,231, twelve months before $313,145, fall $914, 0.3%, offer $0, government part -$6,150, Trust part -$900
   - CC44401 Rakaia Mental Wellbeing Collective: twelve-month income $337,073, twelve months before $337,331, fall $258, 0.1%, offer $0, government part -$2,023, Trust part -$600
   - CC48443 Beckenham Play Resource Library Society: twelve-month income $282,734, twelve months before $282,510, fall -$224, -0.1%, offer $0, government part not reported (short form), Trust part -$900
   - CC34798 Phillipstown Environmental Restoration Trust: twelve-month income $216,095, twelve months before $215,476, fall -$619, -0.3%, offer $0, government part -$5,002, Trust part -$900
   - CC39749 Mairehau Youth Collective: twelve-month income $231,164, twelve months before $230,435, fall -$729, -0.3%, offer $0, government part not reported (short form), Trust part -$900
   - CC37778 Opawa Village Hall Society: twelve-month income $385,051, twelve months before $383,971, fall -$1,080, -0.3%, offer $0, government part -$5,577, Trust part -$900
   - CC38629 Avonhead Kai Share Cooperative: twelve-month income $143,478, twelve months before $142,324, fall -$1,154, -0.8%, offer $0, government part -$534, Trust part -$300
   - CC41503 Papanui Environmental Restoration Trust: twelve-month income $382,192, twelve months before $380,633, fall -$1,559, -0.4%, offer $0, government part $6,989, Trust part -$900
   - CC37881 Rangiora Family Support Trust: twelve-month income $563,339, twelve months before $561,638, fall -$1,701, -0.3%, offer $0, government part -$13,663, Trust part $0
   - CC49235 Rakaia Community Rooms Trust: twelve-month income $451,848, twelve months before $450,121, fall -$1,727, -0.4%, offer $0, government part $636, Trust part -$1,800
   - CC51360 Diamond Harbour After School Care Society: twelve-month income $432,261, twelve months before $430,463, fall -$1,798, -0.4%, offer $0, government part -$589, Trust part -$600
   - CC20427 Temuka Surplus Kai Network: twelve-month income $1,670,866, twelve months before $1,668,831, fall -$2,035, -0.1%, offer $0, government part $15,701, Trust part -$900
   - CC28323 Mount Somers Village Hall Society: twelve-month income $187,080, twelve months before $184,872, fall -$2,208, -1.2%, offer $0, government part -$2,921, Trust part $0
   - CC32792 Hornby Mental Wellbeing Collective: twelve-month income $153,077, twelve months before $150,507, fall -$2,570, -1.7%, offer $0, government part $895, Trust part $0
   - CC26869 Linwood Community Gardens Society: twelve-month income $147,339, twelve months before $144,018, fall -$3,321, -2.3%, offer $0, government part not reported (short form), Trust part -$300
   - CC36807 Halswell Community Rooms Trust: twelve-month income $157,330, twelve months before $153,945, fall -$3,385, -2.2%, offer $0, government part not reported (short form), Trust part -$300
   - CC29723 Amberley Day Programme Trust: twelve-month income $391,485, twelve months before $387,581, fall -$3,904, -1.0%, offer $0, government part $4,674, Trust part $0
   - CC26245 Diamond Harbour Play Resource Library Society: twelve-month income $197,480, twelve months before $193,573, fall -$3,907, -2.0%, offer $0, government part not reported (short form), Trust part $0
   - CC49642 Ilam Older Persons Club: twelve-month income $515,008, twelve months before $511,035, fall -$3,973, -0.8%, offer $0, government part -$15,379, Trust part $32,566
   - CC48381 Darfield Men's Workshop Collective: twelve-month income $163,106, twelve months before $158,512, fall -$4,594, -2.9%, offer $0, government part $1,213, Trust part $0
   - CC40737 Hinds Learning Centre Trust: twelve-month income $150,364, twelve months before $145,261, fall -$5,103, -3.5%, offer $0, government part not reported (short form), Trust part -$900
   - CC20762 Tai Tapu Disability Recreation Society: twelve-month income $339,646, twelve months before $334,273, fall -$5,373, -1.6%, offer $0, government part not reported (short form), Trust part -$900
   - CC39009 Kaiapoi Community Rooms Trust: twelve-month income $368,011, twelve months before $362,582, fall -$5,429, -1.5%, offer $0, government part -$5,593, Trust part -$900
   - CC55531 Lyttelton Whanau Support Services: twelve-month income $182,601, twelve months before $176,947, fall -$5,654, -3.2%, offer $0, government part -$1,822, Trust part -$600
   - CC35249 Linwood Volunteer Exchange Trust: twelve-month income $202,872, twelve months before $196,611, fall -$6,261, -3.2%, offer $0, government part -$3,911, Trust part -$1,800
   - CC49384 Amberley Surplus Kai Network: twelve-month income $702,761, twelve months before $696,368, fall -$6,393, -0.9%, offer $0, government part $9,631, Trust part -$600
   - CC57177 Sydenham Heritage Society: twelve-month income $147,847, twelve months before $141,210, fall -$6,637, -4.7%, offer $0, government part -$3,812, Trust part -$900
   - CC30137 Springston Adult Literacy Project: twelve-month income $262,316, twelve months before $255,650, fall -$6,666, -2.6%, offer $0, government part not reported (short form), Trust part $0
   - CC37110 Woodend Hospital Transport Trust: twelve-month income $219,038, twelve months before $212,265, fall -$6,773, -3.2%, offer $0, government part -$13, Trust part -$300
   - CC46492 Rangiora Environmental Restoration Trust: twelve-month income $378,741, twelve months before $371,602, fall -$7,139, -1.9%, offer $0, government part $2,652, Trust part -$600
   - CC49906 Waimate Day Programme Trust: twelve-month income $149,879, twelve months before $142,489, fall -$7,390, -5.2%, offer $0, government part -$3,569, Trust part -$600
   - CC48543 Cust Surplus Kai Network: twelve-month income $424,854, twelve months before $417,440, fall -$7,414, -1.8%, offer $0, government part -$14,916, Trust part $0
   - CC22557 Waltham Parenting Network: twelve-month income $378,290, twelve months before $370,794, fall -$7,496, -2.0%, offer $0, government part -$5,254, Trust part $0
   - CC32163 Halswell Adult Literacy Project: twelve-month income $336,596, twelve months before $329,003, fall -$7,593, -2.3%, offer $0, government part -$2,963, Trust part $0
   - CC49741 Belfast Sports Education Trust: twelve-month income $470,748, twelve months before $462,829, fall -$7,919, -1.7%, offer $0, government part $1,913, Trust part $0
   - CC51093 Temuka Household Budgeting Trust: twelve-month income $194,846, twelve months before $186,845, fall -$8,001, -4.3%, offer $0, government part not reported (short form), Trust part $0
   - CC25820 Opawa Learning Centre Trust: twelve-month income $456,162, twelve months before $448,075, fall -$8,087, -1.8%, offer $0, government part -$2,645, Trust part -$600
   - CC36141 Addington Youth Collective: twelve-month income $328,071, twelve months before $319,815, fall -$8,256, -2.6%, offer $0, government part not reported (short form), Trust part -$900
   - CC40147 Amberley Music School Trust: twelve-month income $377,328, twelve months before $368,756, fall -$8,572, -2.3%, offer $0, government part -$7,057, Trust part $0
   - CC22266 Wigram Heritage Society: twelve-month income $306,799, twelve months before $297,876, fall -$8,923, -3.0%, offer $0, government part not reported (short form), Trust part -$300
   - CC58253 Mount Somers Sports Education Trust: twelve-month income $243,010, twelve months before $233,946, fall -$9,064, -3.9%, offer $0, government part -$11,945, Trust part $12,200
   - CC54735 Rolleston After School Care Society: twelve-month income $515,268, twelve months before $506,203, fall -$9,065, -1.8%, offer $0, government part -$3,990, Trust part -$900
   - CC58063 Mount Somers Te Reo Learning Trust: twelve-month income $373,025, twelve months before $363,835, fall -$9,190, -2.5%, offer $0, government part $365, Trust part -$900
   - CC31771 Mount Somers Parenting Network: twelve-month income $329,634, twelve months before $320,313, fall -$9,321, -2.9%, offer $0, government part not reported (short form), Trust part $0
   - CC28753 Mairehau Adult Literacy Project: twelve-month income $321,367, twelve months before $312,029, fall -$9,338, -3.0%, offer $0, government part not reported (short form), Trust part $0
   - CC34384 New Brighton Tenancy Advocacy Service: twelve-month income $319,139, twelve months before $309,482, fall -$9,657, -3.1%, offer $0, government part $973, Trust part $0
   - CC41812 Prebbleton Music School Trust: twelve-month income $439,143, twelve months before $429,276, fall -$9,867, -2.3%, offer $0, government part -$5,512, Trust part -$300
   - CC51555 Waikari Environmental Restoration Trust: twelve-month income $240,001, twelve months before $230,064, fall -$9,937, -4.3%, offer $0, government part not reported (short form), Trust part $0
   - CC46230 Ilam Parenting Network: twelve-month income $385,979, twelve months before $375,791, fall -$10,188, -2.7%, offer $0, government part -$4,324, Trust part $0
   - CC22217 Rangiora Carer Respite Network: twelve-month income $542,589, twelve months before $532,355, fall -$10,234, -1.9%, offer $0, government part -$14,616, Trust part $0
   - CC21428 Spreydon Parenting Network: twelve-month income $152,857, twelve months before $142,578, fall -$10,279, -7.2%, offer $0, government part not reported (short form), Trust part -$900
   - CC54654 Ilam Newcomers Network: twelve-month income $709,581, twelve months before $699,123, fall -$10,458, -1.5%, offer $0, government part -$18,021, Trust part $31,769
   - CC48564 Woodend Mental Wellbeing Collective: twelve-month income $153,537, twelve months before $142,801, fall -$10,736, -7.5%, offer $0, government part not reported (short form), Trust part -$300
   - CC59393 Aranui Day Programme Trust: twelve-month income $384,461, twelve months before $373,681, fall -$10,780, -2.9%, offer $0, government part -$12,968, Trust part $0
   - CC29117 Temuka Adult Literacy Project: twelve-month income $386,538, twelve months before $375,640, fall -$10,898, -2.9%, offer $0, government part -$3,201, Trust part -$300
   - CC46736 Hoon Hay Day Programme Trust: twelve-month income $998,980, twelve months before $988,045, fall -$10,935, -1.1%, offer $0, government part -$20,956, Trust part $50,301
   - CC36395 St Albans Neighbourhood Hub Trust: twelve-month income $711,118, twelve months before $699,889, fall -$11,229, -1.6%, offer $0, government part $389, Trust part -$3,000
   - CC35995 Burwood Household Budgeting Trust: twelve-month income $377,175, twelve months before $365,752, fall -$11,423, -3.1%, offer $0, government part -$8,117, Trust part $0
   - CC50679 Cheviot Family Support Trust: twelve-month income $377,256, twelve months before $365,824, fall -$11,432, -3.1%, offer $0, government part -$7,250, Trust part -$600
   - CC33844 Prebbleton Arts Trust: twelve-month income $536,638, twelve months before $525,118, fall -$11,520, -2.2%, offer $0, government part -$5,192, Trust part $0
   - CC48347 Lincoln Community Rooms Trust: twelve-month income $541,968, twelve months before $530,379, fall -$11,589, -2.2%, offer $0, government part -$16,271, Trust part $28,467
   - CC30060 Papanui Tenancy Advocacy Service: twelve-month income $338,023, twelve months before $325,400, fall -$12,623, -3.9%, offer $0, government part -$7,181, Trust part $0
   - CC52688 Mairehau Men's Workshop Collective: twelve-month income $386,492, twelve months before $373,768, fall -$12,724, -3.4%, offer $0, government part -$5,943, Trust part -$1,800
   - CC47128 Dunsandel Neighbourhood Hub Trust: twelve-month income $331,724, twelve months before $318,983, fall -$12,741, -4.0%, offer $0, government part not reported (short form), Trust part -$1,800
   - CC29258 Pegasus Learning Centre Trust: twelve-month income $463,380, twelve months before $450,245, fall -$13,135, -2.9%, offer $0, government part -$9,198, Trust part $0
   - CC42823 Riccarton Sports Education Trust: twelve-month income $225,888, twelve months before $212,450, fall -$13,438, -6.3%, offer $0, government part not reported (short form), Trust part $0
   - CC51077 Mairehau Mental Wellbeing Collective: twelve-month income $494,296, twelve months before $480,797, fall -$13,499, -2.8%, offer $0, government part -$1,532, Trust part -$900
   - CC56694 St Albans Heritage Society: twelve-month income $1,081,869, twelve months before $1,067,976, fall -$13,893, -1.3%, offer $0, government part -$13,711, Trust part -$1,800
   - CC35452 Cheviot Hospital Transport Trust: twelve-month income $161,980, twelve months before $147,666, fall -$14,314, -9.7%, offer $0, government part not reported (short form), Trust part $0
   - CC43375 Tai Tapu Neighbourhood Hub Trust: twelve-month income $335,405, twelve months before $320,371, fall -$15,034, -4.7%, offer $0, government part -$2,840, Trust part -$2,700
   - CC29528 Hororata Hospital Transport Trust: twelve-month income $380,819, twelve months before $365,734, fall -$15,085, -4.1%, offer $0, government part -$13,930, Trust part -$600
   - CC48969 Mairehau Disability Recreation Society: twelve-month income $246,653, twelve months before $231,189, fall -$15,464, -6.7%, offer $0, government part not reported (short form), Trust part -$600
   - CC33982 Ilam Carer Respite Network: twelve-month income $400,458, twelve months before $384,297, fall -$16,161, -4.2%, offer $0, government part -$5,411, Trust part $0
   - CC42762 New Brighton Te Reo Learning Trust: twelve-month income $301,345, twelve months before $284,018, fall -$17,327, -6.1%, offer $0, government part -$4,307, Trust part $0
   - CC55079 Hororata Community Gardens Society: twelve-month income $545,312, twelve months before $527,956, fall -$17,356, -3.3%, offer $0, government part -$13,617, Trust part -$300
   - CC45462 Oxford Community Transport Trust: twelve-month income $636,516, twelve months before $619,059, fall -$17,457, -2.8%, offer $0, government part $2,789, Trust part -$900
   - CC34953 New Brighton Music School Trust: twelve-month income $206,458, twelve months before $188,683, fall -$17,775, -9.4%, offer $0, government part not reported (short form), Trust part -$300
   - CC55936 Lincoln Sports Education Trust: twelve-month income $609,447, twelve months before $591,061, fall -$18,386, -3.1%, offer $0, government part -$5,890, Trust part $0
   - CC31570 Kaikoura Music School Trust: twelve-month income $248,271, twelve months before $229,842, fall -$18,429, -8.0%, offer $0, government part not reported (short form), Trust part -$1,800
   - CC44235 Waltham Mental Wellbeing Collective: twelve-month income $577,545, twelve months before $559,051, fall -$18,494, -3.3%, offer $0, government part -$12,410, Trust part -$1,200
   - CC32041 Waltham Te Reo Learning Trust: twelve-month income $666,190, twelve months before $647,314, fall -$18,876, -2.9%, offer $0, government part -$4,927, Trust part $0
   - CC53228 Addington Surplus Kai Network: twelve-month income $809,670, twelve months before $790,635, fall -$19,035, -2.4%, offer $0, government part -$12,887, Trust part -$6,600
   - CC55127 Tinwald Newcomers Network: twelve-month income $957,586, twelve months before $937,082, fall -$20,504, -2.2%, offer $0, government part -$15,342, Trust part -$1,500
   - CC28853 Amberley Parenting Network: twelve-month income $256,929, twelve months before $236,370, fall -$20,559, -8.7%, offer $0, government part not reported (short form), Trust part -$300
   - CC48848 Cashmere Disability Recreation Society: twelve-month income $718,002, twelve months before $696,970, fall -$21,032, -3.0%, offer $0, government part -$37,397, Trust part -$900
   - CC57084 Phillipstown After School Care Society: twelve-month income $365,122, twelve months before $343,723, fall -$21,399, -6.2%, offer $0, government part -$18,515, Trust part -$1,800
   - CC50038 St Albans Te Reo Learning Trust: twelve-month income $821,446, twelve months before $799,175, fall -$22,271, -2.8%, offer $0, government part $1,048, Trust part $0
   - CC21257 Geraldine Mental Wellbeing Collective: twelve-month income $233,454, twelve months before $210,470, fall -$22,984, -10.9%, offer $0, government part not reported (short form), Trust part -$900
   - CC22638 Waikari Older Persons Club: twelve-month income $560,392, twelve months before $536,250, fall -$24,142, -4.5%, offer $0, government part -$7,789, Trust part $0
   - CC57912 Governors Bay Environmental Restoration Trust: twelve-month income $456,397, twelve months before $431,340, fall -$25,057, -5.8%, offer $0, government part -$14,890, Trust part -$2,700
   - CC29457 Lyttelton Household Budgeting Trust: twelve-month income $393,559, twelve months before $368,196, fall -$25,363, -6.9%, offer $0, government part -$11,658, Trust part $0
   - CC54071 Shirley Mental Wellbeing Collective: twelve-month income $694,547, twelve months before $669,160, fall -$25,387, -3.8%, offer $0, government part -$2,523, Trust part -$4,500
   - CC22489 Governors Bay Community Rooms Trust: twelve-month income $981,807, twelve months before $955,841, fall -$25,966, -2.7%, offer $0, government part $5,297, Trust part -$3,000
   - CC38639 Lincoln Learning Centre Trust: twelve-month income $448,781, twelve months before $420,527, fall -$28,254, -6.7%, offer $0, government part -$5,958, Trust part -$2,700
   - CC22206 West Melton Volunteer Exchange Trust: twelve-month income $406,023, twelve months before $375,561, fall -$30,462, -8.1%, offer $0, government part -$16,536, Trust part $0
   - CC36961 Cheviot Village Hall Society: twelve-month income $847,992, twelve months before $817,005, fall -$30,987, -3.8%, offer $0, government part -$1,055, Trust part -$6,300
   - CC47907 Methven Parenting Network: twelve-month income $1,184,292, twelve months before $1,152,010, fall -$32,282, -2.8%, offer $0, government part -$21,973, Trust part $34,733
   - CC20441 Southbridge Adult Literacy Project: twelve-month income $517,220, twelve months before $482,952, fall -$34,268, -7.1%, offer $0, government part -$19,137, Trust part -$900
   - CC58501 Little River Community Rooms Trust: twelve-month income $2,143,408, twelve months before $2,107,479, fall -$35,929, -1.7%, offer $0, government part -$30,664, Trust part $124,938
   - CC24524 Heathcote Arts Trust: twelve-month income $432,241, twelve months before $396,120, fall -$36,121, -9.1%, offer $0, government part -$7,064, Trust part $0
   - CC56367 Kaikoura Carer Respite Network: twelve-month income $1,315,396, twelve months before $1,278,449, fall -$36,947, -2.9%, offer $0, government part -$11,064, Trust part -$3,300
   - CC32588 Heathcote Village Hall Society: twelve-month income $482,762, twelve months before $442,798, fall -$39,964, -9.0%, offer $0, government part -$22,961, Trust part -$600
   - CC23960 Diamond Harbour Kai Share Cooperative: twelve-month income $887,761, twelve months before $839,224, fall -$48,537, -5.8%, offer $0, government part -$31,367, Trust part $40,246
   - CC39881 Lincoln Neighbourhood Hub Trust: twelve-month income $1,406,284, twelve months before $1,357,250, fall -$49,034, -3.6%, offer $0, government part -$36,326, Trust part $61,034
   - CC52951 Mairehau Older Persons Club: twelve-month income $1,128,721, twelve months before $1,070,900, fall -$57,821, -5.4%, offer $0, government part -$23,679, Trust part $0
   - CC41252 Cashmere After School Care Society: twelve-month income $694,161, twelve months before $635,090, fall -$59,071, -9.3%, offer $0, government part -$5,638, Trust part -$25,724
   - CC55176 Hornby Newcomers Network: twelve-month income $530,482, twelve months before $461,379, fall -$69,103, -15.0%, offer $0, government part -$5,466, Trust part -$25,568
   - CC30148 Amberley Mental Wellbeing Collective: twelve-month income $938,833, twelve months before $864,661, fall -$74,172, -8.6%, offer $0, government part -$33,288, Trust part $0
   - CC54549 Waikari Mental Wellbeing Collective: twelve-month income $931,709, twelve months before $852,278, fall -$79,431, -9.3%, offer $0, government part -$2,717, Trust part -$21,103
   - CC58476 Rangiora Tenancy Advocacy Service: twelve-month income $656,855, twelve months before $575,752, fall -$81,103, -14.1%, offer $0, government part -$4,463, Trust part -$21,436
   - CC58347 Little River Hospital Transport Trust: twelve-month income $741,791, twelve months before $657,592, fall -$84,199, -12.8%, offer $0, government part -$10,695, Trust part -$39,234
   - CC27742 Beckenham After School Care Society: twelve-month income $758,227, twelve months before $660,499, fall -$97,728, -14.8%, offer $0, government part -$13,141, Trust part -$39,190
   - CC30897 Pegasus Kai Share Cooperative: twelve-month income $539,241, twelve months before $421,337, fall -$117,904, -28.0%, offer $0, government part -$16,445, Trust part -$37,744
   - CC44261 Kaikoura Community Transport Trust: twelve-month income $934,039, twelve months before $801,641, fall -$132,398, -16.5%, offer $0, government part -$18,326, Trust part -$30,651
   - CC28548 Spreydon Volunteer Exchange Trust: twelve-month income $2,154,191, twelve months before $2,015,471, fall -$138,720, -6.9%, offer $0, government part -$78,137, Trust part -$8,100
   - CC51237 Mayfield Te Reo Learning Trust: twelve-month income $966,178, twelve months before $786,725, fall -$179,453, -22.8%, offer $0, government part -$32,839, Trust part -$53,765
   - CC48115 Linwood Newcomers Network: twelve-month income $1,420,350, twelve months before $1,151,017, fall -$269,333, -23.4%, offer $0, government part -$64,364, Trust part -$76,775

### steady_ground_sep2026_offers.png

1. One bar per offer for the 9 grantees, largest first, each labelled with its amount
2. Floor drawn at $15,000 and cap drawn at $150,000, each labelled with its value
3. Title carries the rate, 42.55 cents per dollar of fall

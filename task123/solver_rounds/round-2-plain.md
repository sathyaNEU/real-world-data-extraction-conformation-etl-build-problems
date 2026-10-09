# solver round: round 2, plain

**Proxy score 80.2 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 38.2 of 58). Main call LANDED. 5 of 9 ask items cracked (80 per cent of tokens).

## Main call

golden: Strike the September 2026 Steady Ground offers at 42.55 cents per dollar of fall: 9 offers totalling $559,969 of the $560,000 pot.

solver: The trustees should sign 42.55 cents per dollar of fall for the September 2026 round. This puts nine offers totalling $559,969 against the $560,000 pot, leaving $31 in the Fund (at 42.56 the offers total $560,066). The rate comes from 132 scored grantees, screened as at the 30 September 2026 census with the method that gives back every row, offer and rate in all six Ledgerwood March packs.

tokens matched 4 of 7 (42.55, 9, 559,969, 560,000, Strike, September, Steady Ground)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| steady_ground_sep2026_offers.docx | 1 | 1 | 1 | 100% |
| steady_ground_sep2026_offers.docx | 2 | 30 | 38 | 79% |
| steady_ground_sep2026_offers.docx | 3 | 0 | 2 | 0% |
| steady_ground_sep2026_offers.docx | 4 | 1 | 1 | 100% |
| steady_ground_sep2026_offers.docx | 5 | 8 | 8 | 100% |
| steady_ground_sep2026_screen.csv | 1 | 119 | 853 | 14% |
| steady_ground_sep2026_offers.png | 1 | 0 | 1 | 0% |
| steady_ground_sep2026_offers.png | 2 | 3 | 3 | 100% |
| steady_ground_sep2026_offers.png | 3 | 2 | 2 | 100% |

## Solver's path

1. Read prompt.md, round rules (rule 4.1: twelve-month income runs for twelve months ending on or after the census before; rule 4.3: offer at 10% fall or more; rule 5: floor $15,000, cap $150,000, highest 2dp rate within pot; rule 5.4: each round scored afresh), budget minute (pot $560,000), cutover standard (in-house screen must give back every row, offer and rate of all six packs), field guide (only accepted versions count; a quarter's record is its own return; memo lines; QFR-16 to QFR-24 change).
2. Joined portal_return_lines to grants_register Grants on grant_ref to get charity_no. Per organisation and period: kept accepted versions only and took the one accepted most recently across all of the organisation's grants. This matters for CC56694 and CC59225, which file under two grants. Used the YTD column only, never PY.
3. Replay rule found by matching the packs. Twelve-month income = latest annual return on charities_register_returns_extract (charity_no trimmed and upper-cased; total_gross_income; date_received on or before the census) + YTD of the latest accepted Q1-Q3 return of the next financial year - YTD of the same quarter a year earlier. If there is no such quarter, it is the annual return itself. Twelve months before = the same construction one year back. Data is taken as at the census date, inclusive.
4. Scope = organisations with an Operating grant current at the census. Applied to the six March censuses, this gives back 118/124/131/137/142/145 rows exactly (income, before, fall $, fall %, offer) and the published rates and totals. A cutoff at the issue date breaks 2022 (CC51502) and 2023 (CC41503). Items dated on census day are needed in 2023, 2025 and 2026, so the cutoff is the census date itself.
5. September 2026 census, data as at 30 Sep 2026: 150 organisations in scope. 3 are not scored because their returns do not cover both periods (CC45991, CC37175, CC20394) and 1 has no register returns (CC29644). 14 March-year-end organisations had no FY2026 annual return on the register by 30 Sep. Their only window ends 31 Dec 2025, before the 31 Mar 2026 census, and repeats their March windows, so rules 4.1 and 5.4 exclude them. Result: 132 scored. CC58287's v2 June return (accepted 5 Oct) and six register returns received 1-7 Oct are left out.
6. Fall = before - income; fall % = fall / before. Nine grantees are at 10% or more. Searched 2dp rates: 42.55 gives $559,969 (Mayfield is capped at $150,000) and 42.56 gives $560,066, so the rate is 42.55 with $31 retained.
7. Government part: built the same way from government lines. Register govt_grants_contracts for the annual returns; quarterly YTD from GOV_GRT + FEE_SVC_GOV on QFR-16 and GOV_GRT on QFR-24 (this matches register govt on 100% of full-form year-end returns). Own (Trust) part: paid Trust payments (returned payments excluded, reissues counted) with value_date in each twelve-month window. The value-date basis matches every GRT_NGO_APT YTD memo line in the portal. Part of fall = before-window amount minus income-window amount.
8. Ordered the screen by dollar fall. The first grantee not offered is CC58287 Diamond Harbour Whanau Support Services at 5.4% ($97,407).

confidence: Medium-high. The replay matches all six packs exactly. The September answer depends on two choices the packs don't directly test: the 30 Sep census-date cutoff, and dropping the 14 stale-window grantees. Taking data as at 7 Oct instead gives 138 scored and 35.58c. Ignoring the window rule gives 146 scored and 17.76c.

notes: 'First grantee outside the line' is read in screen order (largest dollar fall first). Read by fall percentage, it would be Amberley Tenancy Advocacy Service (CC59225) at 6.4%. Short-form filers have no government line, so their government part cannot be determined and is left blank; no offered grantee is affected. The March government-cut framing does not change the rate.

### steady_ground_sep2026_offers.docx (solver's answers)
- Rate the September offers are struck at: 42.55 cents per dollar of fall (pot $560,000; 9 offers totalling $559,969; $31 stays in the Fund)
- Each grantee offered: offer, government part of the fall, Trust (own) part of the fall: Mayfield Kai Share Cooperative CC23552: offer $150,000 (capped; uncapped would be $163,283), fall $383,743, government $258,337, own -$6,600 | Woolston Sports Education Trust CC20936: offer $109,687, fall $257,783, government $103,487, own $0 | Tai Tapu Kai Share Cooperative CC45658: offer $65,770, fall $154,572, government $94,431, own -$20,700 | Waikari After School Care Society CC45324: offer $59,426, fall $139,661, government $73,145, own -$3,600 | Papanui Neighbourhood Hub Trust CC34513: offer $51,797, fall $121,733, government $41,328, own -$2,400 | St Albans Newcomers Network CC27360: o
- First grantee outside the line, with its fall as a percentage: Diamond Harbour Whanau Support Services (CC58287): fall $97,407, 5.4%. It ranks 7th by dollar fall but is under the 10% line, so it gets no offer.
- Number of grantees the screen scored: 132
- Published grantee rows the screen gives back exactly, per Ledgerwood March round: March 2021: 118 of 118; March 2022: 124 of 124; March 2023: 131 of 131; March 2024: 137 of 137; March 2025: 142 of 142; March 2026: 145 of 145. All six rates and offer totals also match: 29.77/$539,966, 38.40/$574,924, 33.83/$609,983, 26.54/$649,960, 30.81/$689,979, 20.16/$719,890.

### steady_ground_sep2026_screen.csv (solver's answers)
- Rows and order: 132 rows, one per scored grantee, largest dollar fall first
- Top rows (income / twelve months before / fall $ / fall % / offer / government part / own part): CC23552 2,519,857 / 2,903,600 / 383,743 / 13.2 / 150,000 / 258,337 / -6,600; CC20936 1,150,133 / 1,407,916 / 257,783 / 18.3 / 109,687 / 103,487 / 0; CC45658 1,018,170 / 1,172,742 / 154,572 / 13.2 / 65,770 / 94,431 / -20,700; CC45324 911,515 / 1,051,176 / 139,661 / 13.3 / 59,426 / 73,145 / -3,600; CC34513 743,031 / 864,764 / 121,733 / 14.1 / 51,797 / 41,328 / -2,400; CC27360 589,578 / 687,117 / 97,539 / 14.2 / 41,503 / 54,616 / -3,600; CC58287 1,706,427 / 1,803,834 / 97,407 / 5.4 / 0 / 5,849 / -8,100; CC30757 527,761 / 615,148 / 87,387 / 14.2 / 37,183 / 34,351 / 0; CC54322 394,008 / 455,415 / 6
- Offer column total: $559,969 across 9 non-zero offers; every other row is 0

### steady_ground_sep2026_offers.png (solver's answers)
- Title rate: 42.55 cents per dollar of fall
- Bars, largest first, labelled: Mayfield Kai Share Cooperative $150,000; Woolston Sports Education Trust $109,687; Tai Tapu Kai Share Cooperative $65,770; Waikari After School Care Society $59,426; Papanui Neighbourhood Hub Trust $51,797; St Albans Newcomers Network $41,503; Sydenham Play Resource Library Society $37,183; Shirley Kai Share Cooperative $26,129; Kaiapoi Newcomers Network $18,474
- Reference lines: Floor at $15,000 and cap at $150,000

# solver round: round 4, plain

**Proxy score 91.7 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 49.7 of 58). Main call LANDED. 7 of 9 ask items cracked (80 per cent of tokens).

## Main call

golden: Strike the September 2026 Steady Ground offers at 42.55 cents per dollar of fall: 9 offers totalling $559,969 of the $560,000 pot.

solver: Strike the September 2026 Steady Ground offers at 42.55 cents per dollar of fall. That gives 9 offers totalling $559,969 against the $560,000 pot ($31 stays in the Fund), out of 132 scored grantees, using data as at the 30 September 2026 census (42.56 would cost $560,066).

tokens matched 7 of 7 (42.55, 9, 559,969, 560,000, Strike, September, Steady Ground)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| steady_ground_sep2026_offers.docx | 1 | 1 | 1 | 100% |
| steady_ground_sep2026_offers.docx | 2 | 29 | 37 | 78% |
| steady_ground_sep2026_offers.docx | 3 | 2 | 2 | 100% |
| steady_ground_sep2026_offers.docx | 4 | 1 | 1 | 100% |
| steady_ground_sep2026_offers.docx | 5 | 7 | 8 | 88% |
| steady_ground_sep2026_screen.csv | 1 | 43 | 853 | 5% |
| steady_ground_sep2026_offers.png | 1 | 1 | 1 | 100% |
| steady_ground_sep2026_offers.png | 2 | 3 | 3 | 100% |
| steady_ground_sep2026_offers.png | 3 | 2 | 2 | 100% |

## Solver's path

1. Read the request, the round rules (10% threshold; offer = fall x rate, $15k floor, $150k cap; the highest 2-dp rate within the pot), the June budget minute (pot $560,000), the cutover standard (the in-house screen must reproduce all six Ledgerwood packs), the field guide, the form-change notice and the team thread.
2. Mapped portal returns to organisations through the grants register's grant_ref to charity_no. Used accepted versions only, taking each return's latest accepted version and, where an organisation filed under two grants, the later-accepted return for that quarter (this resolves CC59225's June 2026 conflict to the OG v2 return, $119,392 YTD).
3. Built twelve-month income from each quarter's own YTD by quarterly differencing across financial-year boundaries, which handles the June-to-March year-end changes. I did not use the PY column.
4. Replay: data as at the census date (versions accepted on or before the census). A financial-year total counts only if its annual return reached the Charities register by the census; otherwise the screen falls back to an earlier quarter. It takes the latest quarter on or after the previous census for which both twelve-month periods are covered. Scope is organisations holding a current operating grant at the census, from register dates and Term ended/Renewal variations. This reproduced every row of all six packs (122/128/135/141/146/149) and every rate.
5. Applied the same method to the 30 Sep 2026 census (previous census 31 Mar 2026; quarters Jun 2026 or Mar 2026): 153 in scope, 132 scored. This leaves out CC58287's v2 accepted on 5 Oct, which would otherwise put it over the line, and six annual returns received 1–7 Oct.
6. Searched rates at 0.01-cent steps: 42.55 gives $559,969 for 9 offers (Mayfield capped at $150,000) and 42.56 gives $560,066.
7. Split each offered fall. Government money is the change in government lines (QFR-16 GOV_GRT + FEE_SVC_GOV against QFR-24 GOV_GRT) plus the change in the central government co-funding paid with Trust instalments: the quarterly top-ups paid with the Jan, Apr and Jul 2025, Oct 2025 and Jan 2026 instalments, by value date. The Trust's own money is the change in paid Trust payments by value date (returned payments excluded, the reissues counted; this matches the GRT_NGO_APT memo line) less the co-funding.

confidence: High for the replay, the rate (42.55), the 9 offers, 132 scored and the first grantee outside the line (Amberley, 6.4%). Medium for the government/own split, because it depends on treating the co-funding paid through the Trust as government money and on value-date (cash) timing.

notes: If data accepted up to the 7 Oct extract were used instead of data as at the census, 138 would be scored and CC58287 would be offered, giving a rate of 35.58; the replay supports the census as-at convention. If co-funding were counted as Trust money, government parts would total $701,330 and own parts -$6,300.

### steady_ground_sep2026_offers.docx (solver's answers)
- Rate: 42.55 cents per dollar of fall
- Offers, largest first (offer; fall; fall %; government part of fall; Trust's own part of fall): Mayfield Kai Share Cooperative CC23552: $150,000 (capped); fall $383,743, 13.2%; government $261,784; own -$6,600 | Woolston Sports Education Trust CC20936: $109,687; fall $257,783, 18.3%; government $101,216; own $0 | Tai Tapu Kai Share Cooperative CC45658: $65,770; fall $154,572, 13.2%; government $97,042; own -$20,700 | Waikari After School Care Society CC45324: $59,426; fall $139,661, 13.3%; government $80,053; own -$3,600 | Papanui Neighbourhood Hub Trust CC34513: $51,797; fall $121,733, 14.1%; government $45,378; own -$2,400 | St Albans Newcomers Network CC27360: $41,503; fall $97,539, 1
- Totals: 9 offers, $559,969 offered, $31 left in the Fund; offered falls total $1,347,241, of which government money $733,730 (government lines $701,330 plus $32,400 of co-funding) and the Trust's own money -$38,700 (the Trust's own money went up)
- First grantee outside the line: Amberley Tenancy Advocacy Service (CC59225), fall $33,728 = 6.4%
- Grantees scored: 132 (153 in scope; 21 not scored because their returns, with a filed annual return, do not cover both periods as at 30 Sep 2026)
- Ledgerwood rows reproduced exactly per March round: 2021: 122 of 122; 2022: 128 of 128; 2023: 135 of 135; 2024: 141 of 141; 2025: 146 of 146; 2026: 149 of 149 (rates 29.77, 38.40, 33.83, 26.54, 30.81, 20.16 and totals offered also reproduced)

### steady_ground_sep2026_screen.csv (solver's answers)
- Rows and order: 132 rows, one per scored grantee, sorted by fall in dollars, largest first: CC23552, CC20936, CC45658, CC45324, CC34513, CC27360, CC30757, CC54322, CC56509 (the 9 offers), then CC59225 $33,728 (6.4%), CC58287 $28,861 (1.6%), CC31839 $23,082 (2.8%), CC30956 $12,864 (1.5%), ...
- Columns per row: Twelve-month income, the twelve months before, fall in $, fall % to 1 dp, offer (0 if no offer), government part of the fall, and the Trust's own part of the fall. Example: CC23552 has twelve-month income $2,519,857 (to Jun 2026) against $2,903,600, fall $383,743, 13.2%, offer $150,000, government $261,784, own -$6,600. CC20936 has $1,150,133 (to Mar 2026) against $1,407,916, fall $257,783, 18.3%, offer $109,687.
- Offers total: $559,969

### steady_ground_sep2026_offers.png (solver's answers)
- Bars: 9 bars, largest first, each labelled: $150,000, $109,687, $65,770, $59,426, $51,797, $41,503, $37,183, $26,129, $18,474
- Reference lines: Floor at $15,000 and cap at $150,000
- Title rate: 42.55 cents per dollar of fall

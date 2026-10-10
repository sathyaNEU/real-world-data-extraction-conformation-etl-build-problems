# solver round: round 3, plain

**Proxy score 86.0 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 44.0 of 58). Main call LANDED. 6 of 9 ask items cracked (80 per cent of tokens).

## Main call

golden: Strike the September 2026 Steady Ground offers at 42.55 cents per dollar of fall: 9 offers totalling $559,969 of the $560,000 pot.

solver: Strike the September 2026 Steady Ground offers at 42.55 cents per dollar of fall. That gives 9 offers totalling $559,969 against the $560,000 pot, with $31 left in the Fund. The 9 grantees are Mayfield Kai Share Cooperative $150,000 (cap), Woolston Sports Education Trust $109,687, Tai Tapu Kai Share Cooperative $65,770, Waikari After School Care Society $59,426, Papanui Neighbourhood Hub Trust $51,797, St Albans Newcomers Network $41,503, Sydenham Play Resource Library Society $37,183, Shirley Kai Share Cooperative $26,129 and Kaiapoi Newcomers Network $18,474. The screen scored 132 grantees using data as at the 30 September 2026 census, and it reproduces all six of Ledgerwood's March runs exactly.

tokens matched 7 of 7 (42.55, 9, 559,969, 560,000, Strike, September, Steady Ground)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| steady_ground_sep2026_offers.docx | 1 | 1 | 1 | 100% |
| steady_ground_sep2026_offers.docx | 2 | 28 | 37 | 76% |
| steady_ground_sep2026_offers.docx | 3 | 2 | 2 | 100% |
| steady_ground_sep2026_offers.docx | 4 | 1 | 1 | 100% |
| steady_ground_sep2026_offers.docx | 5 | 8 | 8 | 100% |
| steady_ground_sep2026_screen.csv | 1 | 54 | 853 | 6% |
| steady_ground_sep2026_offers.png | 1 | 0 | 1 | 0% |
| steady_ground_sep2026_offers.png | 2 | 3 | 3 | 100% |
| steady_ground_sep2026_offers.png | 3 | 2 | 2 | 100% |

## Solver's path

1. Read the request, round rules, cutoff standard, budget minute ($560,000 pot), field guide, extract record and team thread. Loaded the Ledgerwood packs for March 2021 to March 2026 (both the Screen and Round sheets).
2. Built an organisation-level quarterly record from portal_return_lines: accepted versions only, joined to grants_register Grants through grant_ref to get charity_no. Where an organisation holds both an operating and a project grant, its two returns for a quarter collapse to the latest accepted version. The total line is TOT_INC or TOT_REV.
3. Twelve-month income at quarter q = YTD(q) + the previous financial year's total + YTD from the same quarter a year earlier, each taken from that quarter's own return; the PY column is not used. Changed financial years are handled through short years (CC23995, CC29520, CC36026). 'Twelve months before' = the same calculation at q minus 4 quarters.
4. Rule found by replay: start from the last quarter before the census and step back a quarter at a time. A quarter qualifies only if the annual return for the financial year it relies on was received in charities_register_returns_extract (after normalising charity_no) on or before the census. Data is taken as at the census date (version accepted_at <= census). Ledgerwood demonstrably excluded data arriving after the census: the CC51502 v2 accepted on 12 Apr 2022 and the CC41503 register receipt on 18 Apr 2023. The rule also explains why the Dec-year-end organisations fall back to September and CC41503 and CC49235 fall back to March.
5. Scope is organisations holding an operating grant current at the census, counted once. Replay result: 121, 127, 134, 140, 145 and 148 rows reproduced exactly. All six rates (29.77, 38.40, 33.83, 26.54, 30.81, 20.16), every offer, and the Steady Ground offers sheet also match. The rate is the highest 2-decimal cents value where the offers (fall x rate, half-up to whole dollars, floor $15,000, cap $150,000, for falls of 10% or more) stay within the pot.
6. September 2026: census 30 Sep 2026, starting quarter Jun 2026. Rule 4.1 allows quarters no earlier than 31 Mar 2026 (the previous census), and data is as at 30 Sep 2026. In scope: 153. Not scored: 17 with no annual return for the needed year filed by 30 Sep, and 4 new grantees without prior-year returns. Scored: 132. Nine have a fall of 10% or more.
7. Rate search against the $560,000 pot: 42.55c gives $559,969 and 42.56c gives $560,066, so the rate is 42.55. The first grantee not offered is CC59225 Amberley Tenancy Advocacy Service at 6.4%.
8. Fall split. Government part = fall in government grants and contracts, with QFR-16 returns converted to the QFR-24 basis (GOV_GRT + FEE_SVC_GOV, from each quarter's own return), plus the fall in central government co-funding the Trust passed on. That co-funding is the Variations 'Government co-funding' amount divided by 12, in instalments for Oct 2024 to Mar 2026, counted by value date in trust_payment_run, paid rows only. Own part = fall in all Trust payments (which equal the GRT_NGO_APT memo) less the co-funding.

confidence: High for the replay method and the screen: all six March rounds reproduce exactly. Medium-high for the 42.55 rate, which depends on taking data as at the census date. Medium for how the fall is split into government money and the Trust's own money.

notes: Two choices decide the rate. The replay pins the data cutoff only to somewhere between the census and 12 days after it. If everything up to the 7 Oct extract is used instead, six register returns received 1–7 Oct and CC58287's v2 accepted 5 Oct get in: 138 scored, 10 offers, rate 35.58. If the screen may fall back to the Dec 2025 quarter, breaching rule 4.1: 149 scored, 14 offers, rate 17.76. The fall split is my reading of the request. Negative 'own' figures mean the Trust paid that grantee more in the later twelve months than in the earlier ones.

### steady_ground_sep2026_offers.docx (solver's answers)
- Rate the September offers are struck at: 42.55 cents per dollar of fall (9 offers, total offered $559,969, $31 left in the Fund from the $560,000 pot)
- Each offered grantee: offer, then the government money and our own money in its fall (whole NZD; a negative means that money went up): CC23552 Mayfield Kai Share Cooperative: offer $150,000 (cap), fall $383,743; government $259,239, our own -$6,600. CC20936 Woolston Sports Education Trust: offer $109,687, fall $257,783; government $100,513, our own $0. CC45658 Tai Tapu Kai Share Cooperative: offer $65,770, fall $154,572; government $98,216, our own -$20,700. CC45324 Waikari After School Care Society: offer $59,426, fall $139,661; government $76,381, our own -$3,600. CC34513 Papanui Neighbourhood Hub Trust: offer $51,797, fall $121,733; government $44,036, our own -$2,400. CC27360 St Albans Newcomers Network: offer $41,503, fa
- First grantee outside the line, with its fall as a percentage: Amberley Tenancy Advocacy Service (CC59225): fall $33,728, which is 6.4%
- Number of grantees the screen scored: 132 (153 organisations in scope; 17 had no annual return for the needed year filed with Charities Services by 30 Sep 2026; 4 had no prior-year returns)
- Published grantee rows the screen gives back exactly, for each of Ledgerwood's six March rounds: 2021: 121 of 121; 2022: 127 of 127; 2023: 134 of 134; 2024: 140 of 140; 2025: 145 of 145; 2026: 148 of 148. Every offer and every rate also matches (29.77, 38.40, 33.83, 26.54, 30.81, 20.16).

### steady_ground_sep2026_screen.csv (solver's answers)
- Rows and order: 132 rows, one per scored grantee, sorted by fall in dollars, largest first. The first ten are CC23552, CC20936, CC45658, CC45324, CC34513, CC27360, CC30757, CC54322, CC56509, then CC59225.
- Sample figures for the top rows (twelve-month income / twelve months before / fall $ / fall % / offer / government part / own part): CC23552: 2,519,857 / 2,903,600 / 383,743 / 13.2 / 150,000 / 259,239 / -6,600. CC20936 (twelve months to 31 Mar 2026): 1,150,133 / 1,407,916 / 257,783 / 18.3 / 109,687 / 100,513 / 0. CC45658: 1,018,170 / 1,172,742 / 154,572 / 13.2 / 65,770 / 98,216 / -20,700. CC59225: 493,685 / 527,413 / 33,728 / 6.4 / 0 / 16,613 / -1,500. CC58287: 1,774,973 / 1,803,834 / 28,861 / 1.6 / 0 / 9,623 / -8,100.
- Totals: Offers sum to $559,969 across 9 non-zero rows; the other 123 rows carry an offer of 0

### steady_ground_sep2026_offers.png (solver's answers)
- Title rate: 42.55 cents per dollar of fall
- Bars, largest first, with amount labels: Mayfield Kai Share Cooperative 150,000; Woolston Sports Education Trust 109,687; Tai Tapu Kai Share Cooperative 65,770; Waikari After School Care Society 59,426; Papanui Neighbourhood Hub Trust 51,797; St Albans Newcomers Network 41,503; Sydenham Play Resource Library Society 37,183; Shirley Kai Share Cooperative 26,129; Kaiapoi Newcomers Network 18,474
- Reference lines: Floor at $15,000 and cap at $150,000

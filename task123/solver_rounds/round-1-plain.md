# solver round: round 1, plain

**Proxy score 93.8 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 51.8 of 58). Main call LANDED. 8 of 9 ask items cracked (80 per cent of tokens).

## Main call

golden: Strike the September 2026 Steady Ground offers at 27.47 cents per dollar of fall: 14 offers totalling $819,939 of the $820,000 pot.

solver: Strike the September 2026 Steady Ground offers at 27.47 cents per dollar of fall. Rule 5.3 makes that the highest two-decimal rate that keeps the 14 offers inside the $820,000 pot: they total $819,939 and $61 stays in the Fund, while 27.48 would come to $820,178. The figures come from an in-house screen of 146 grantees at the 30 September 2026 census, built the way Ledgerwood built its screen, and that screen gives back all six March packs row for row.

tokens matched 7 of 7 (27.47, 14, 819,939, 820,000, Strike, September, Steady Ground)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| steady_ground_sep2026_offers.docx | 1 | 1 | 1 | 100% |
| steady_ground_sep2026_offers.docx | 2 | 58 | 58 | 100% |
| steady_ground_sep2026_offers.docx | 3 | 2 | 2 | 100% |
| steady_ground_sep2026_offers.docx | 4 | 1 | 1 | 100% |
| steady_ground_sep2026_offers.docx | 5 | 8 | 8 | 100% |
| steady_ground_sep2026_screen.csv | 1 | 43 | 953 | 5% |
| steady_ground_sep2026_offers.png | 1 | 1 | 1 | 100% |
| steady_ground_sep2026_offers.png | 2 | 3 | 3 | 100% |
| steady_ground_sep2026_offers.png | 3 | 2 | 2 | 100% |

## Solver's path

1. Read the round rules, budget minute (pot $820,000), cutover standard, field guide, portal form notice, grants thread and the six Ledgerwood packs (Screen and Round sheets).
2. Attached portal_return_lines to the grants register Grants sheet on grant_ref to get charity_no. Kept accepted versions only and took one return per organisation per quarter, so an organisation holding both an operating and a project grant is counted once. Its twelve-month total came from TOT_INC (QFR-16) or TOT_REV (QFR-24) YTD.
3. Reverse-engineered the Ledgerwood method. Data is taken as at the census day: a portal version counts only if accepted by the census date, and an annual return in the charities register counts only if date_received is on or before the census. Charity numbers are trimmed and upper-cased.
4. Twelve-month income at quarter Q is YTD(Q) plus the prior full financial year from the register annual return, less YTD(Q-4). When Q is the organisation's year end, the annual return total is used directly. Q is the latest quarter on or before the census at which both periods can be built; if the needed annual return has not been received, the screen steps back a quarter.
5. Scope is operating grants with start_date ≤ census ≤ end_date. A grantee whose fall is 10% or more is offered. Each offer is fall × rate, rounded and then held between $15,000 and $150,000. The rate is the highest two-decimal rate at which the offers fit inside the pot. This replay gives back all 118/124/131/137/142/145 published rows, every offer and all six rates exactly.
6. Sept 2026 census (2026-09-30, data as at that day): 150 organisations in scope and 146 scored. The quarters used were Jun-2026 for 115 grantees, Mar-2026 for 17 and Dec-2025 for 14 (where the FY2026 annual return was not received by 30 Sept). 14 grantees fell 10% or more. The rate is 27.47 and the offers total $819,939.
7. Split each fall into a government part and a Trust part over the same windows. Government money is GOV_GRT + FEE_SVC_GOV on QFR-16, GOV_GRC on QFR-24, and govt_grants_contracts in the register annual return. The Trust's own money is the paid lines in trust_payment_run, by value_date, over the 12 months to each window end; returned payments are excluded and reissues counted, which matches the QFR-24 GRT_NGO_APT memo exactly.

confidence: Medium-high for the rate and the offer list, because the method gives back all six Ledgerwood rounds exactly. Medium for the 'first grantee outside the line' answer, which depends on how the line is read, and for how the fall is split into government and Trust money.

notes: Taking data as at the census matters here. If the extract date (7 Oct) is used instead, a 5 Oct resubmission from Diamond Harbour Whanau (CC58287) puts it at 12.5% and offered, the Oct-received annual return for Heathcote (CC40435) moves it to another quarter, and the rate becomes 32.57. The March-cut 'relief' framing in the team thread does not affect the rules-based screen. Rule 5.4's previous Steady Ground instalments stay in reported income, as they did in Ledgerwood's replays. Steady Ground payments also count in the Trust's own money, which is why several own-money figures are negative.

### steady_ground_sep2026_offers.docx (solver's answers)
- Rate the September offers are struck at: 27.47 cents per dollar of fall (pot $820,000; 14 offers totalling $819,939; $61 retained)
- Each grantee offered: offer, government part of fall, Trust's own part of fall (whole NZD): Geraldine Carer Respite Network (CC50315): offer $150,000 (cap), fall $660,409, government $302,510, own -$10,800 | Heathcote Adult Literacy Project (CC40435): offer $106,458, fall $387,542, government $125,528, own $13,877 | Mayfield Kai Share Cooperative (CC23552): offer $105,414, fall $383,743, government $258,337, own -$19,966 | Woolston Sports Education Trust (CC20936): offer $70,813, fall $257,783, government $103,487, own $36,866 | Burwood Environmental Restoration Trust (CC47102): offer $68,195, fall $248,253, government $89,049, own $15,122 | Beckenham Carer Respite Network (CC42717):
- First grantee outside the line, with its fall as a percentage: Pegasus Community Transport Trust (CC28177), fall 7.7% ($58,635). This is the highest fall below the 10% line. Taken in fall-in-dollars order instead, the first grantee not offered is Diamond Harbour Whanau Support Services (CC58287) at 5.4%.
- Number of grantees scored: 146 (150 organisations in scope; 4 newer grantees lack two years of returns)
- Published rows the screen gives back exactly, per Ledgerwood March round: March 2021: 118 of 118; March 2022: 124 of 124; March 2023: 131 of 131; March 2024: 137 of 137; March 2025: 142 of 142; March 2026: 145 of 145. Each round's rate and offers also reproduce exactly (29.77, 38.40, 33.83, 26.54, 30.81, 20.16).

### steady_ground_sep2026_screen.csv (solver's answers)
- One row per scored grantee, largest fall in dollars first: 146 rows. The first row is Geraldine Carer Respite Network: twelve-month income $2,592,554, twelve months before $3,252,963, fall $660,409 / 20.3%, offer $150,000, government $302,510, own -$10,800. Next come Heathcote Adult Literacy Project at $387,542 / 22.1% and Mayfield Kai Share Cooperative at $383,743 / 13.2%. The last row is Linwood Newcomers Network: income $1,420,350, before $1,151,017, fall -$269,333 / -23.4%, offer 0. 14 rows carry an offer and 132 carry zero. For the 25 short-form grantees (QFR-16S/24S) the government part cannot be stated because those forms have no government lin

### steady_ground_sep2026_offers.png (solver's answers)
- Bars per offer, largest first, labelled; floor and cap lines; rate in title: 14 bars from $150,000 (Geraldine) down to $15,000 (Kaiapoi), labelled with their offers. Lines drawn across at the $15,000 floor and the $150,000 cap. Title shows 27.47 cents per dollar of fall.

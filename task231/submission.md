# task231 submission

## Tags

**Domain:** Survey Research & Official Statistics (nonresponse, calibration and measurement-error adjustment: the eligibility of a business panel's unresolved non-respondents).
**Analytical objective:** Data Quality Monitoring & Alerting (which regions of the September 2026 Business Conditions Survey round get further fieldwork at the main close).

## 1. Final Recommendation

**Put Capital and Harbour into the reminder-call extension, give Islands and Western Uplands the extra email reminder, and give the other eight regions neither.**

The 3,970 non-returners the business register does not show as closed are in scope at 84.7%, because 15.3% of the non-returners of rounds the register has caught up with (March 2017 to September 2022) had ceased trading by their round's frame date; on that base only Capital and Harbour fall under 55%, and Islands and Western Uplands are the only others under 58%. Not the register as it stands, which counts every one of them as trading and puts five regions under 55% (Capital, Harbour, Islands, Border and Western Uplands) and the other seven under 58%: the register records a closure only when it is notified, often a year or more after trading stops. Not the contact centre's resolved calls, nor the closure share of every earlier round (12.1%) or of the last two years (7.8%), which all still put Islands and Western Uplands under 55%: a call confirms a closure only when someone answers for the firm, and those rounds' closures are still reaching the register.

## 2. Critical Components

1. Firms returned by the 17:00 main close on 25 September: **4,610** of the **8,604** invited
2. Invited firms the register shows as ceased by 1 September: **24**; non-returners with no closure on the register: **3,970**
3. Non-returners of the settled rounds (March 2017 to September 2022) that had ceased trading by their round's frame date: **15.3%** (7,494 of 48,978)

## 3. Step-by-Step Solution

1. Counted each region's invited firms in bcs_invitations_2026_09.csv with a return in bcs_returns_2026_09.csv by 17:00 Brevland time on 25 September, each firm once (the fieldwork quality standard, section 4): 4,610 of 8,604 returned.
2. Joined the other invited firms to brevland_business_register_closures.csv on company number: 24 had ceased trading by 1 September and are out of scope under section 4 of the standard; 3,970 non-returners have no closure on the register.
3. The register's notes say a company appears only once its closure is registered, and the extract's registration dates run long after its cessation dates, so the 3,970 include firms that had already ceased; their share comes from earlier rounds the register has caught up with.
4. For the 23 rounds from March 2017 to September 2022 in bcs_round_outcomes_2017_2026.csv, took the firms with no return by the round's main close in BCS_round_calendar.xlsx, dropped those the register showed closed by that close, and linked the rest through bcs_panel_register.csv to the closure extract: 7,494 of 48,978, 15.3%, had ceased by the round's frame date.
5. Counted each region's own non-returners with no register closure (3,970 in all) in scope at 84.7% and divided its returns by its returns plus that count: Capital and Harbour come out under 55%, Islands and Western Uplands at 55% or more but under 58%, the other eight at 58% or more.
6. Set each region's alert level from the table in section 5 of the standard: red under 55%, amber from 55% to under 58%, green from 58%.
7. Recommendation: the extension for Capital and Harbour, the extra email for Islands and Western Uplands, neither for the other eight.

## 4. Deliverable Answers

### bcs_sep2026_extension.xlsx

1. The call: extension for Capital and Harbour; extra email for Islands and Western Uplands; neither for North Coast, Border, Northern Forests, South Coast, Eastern Lakes, Midlands, River Valley and Southern Plains.
2. Alert level by region:
   - Capital (R01): red, reminder-call extension
   - Harbour (R02): red, reminder-call extension
   - North Coast (R03): green, neither
   - Islands (R04): amber, extra email reminder
   - Border (R05): green, neither
   - Western Uplands (R06): amber, extra email reminder
   - Northern Forests (R07): green, neither
   - South Coast (R08): green, neither
   - Eastern Lakes (R09): green, neither
   - Midlands (R10): green, neither
   - River Valley (R11): green, neither
   - Southern Plains (R12): green, neither
3. September round so far, by region, firms the contact centre has reached and calls it has placed:
   - Capital: 454 firms reached, 1,359 calls placed
   - Harbour: 315 firms reached, 1,021 calls placed
   - North Coast: 224 firms reached, 684 calls placed
   - Islands: 174 firms reached, 538 calls placed
   - Border: 197 firms reached, 635 calls placed
   - Western Uplands: 229 firms reached, 652 calls placed
   - Northern Forests: 179 firms reached, 598 calls placed
   - South Coast: 292 firms reached, 919 calls placed
   - Eastern Lakes: 270 firms reached, 812 calls placed
   - Midlands: 310 firms reached, 942 calls placed
   - River Valley: 218 firms reached, 779 calls placed
   - Southern Plains: 242 firms reached, 743 calls placed
4. June 2026 round, by region, returns that reached us after the main close and their share of the region's June returns, one decimal:
   - Capital: 104 returns, 18.9%
   - Harbour: 75 returns, 17.0%
   - North Coast: 56 returns, 15.3%
   - Islands: 43 returns, 16.3%
   - Border: 44 returns, 12.3%
   - Western Uplands: 44 returns, 13.1%
   - Northern Forests: 43 returns, 12.8%
   - South Coast: 78 returns, 14.1%
   - Eastern Lakes: 79 returns, 16.4%
   - Midlands: 74 returns, 13.9%
   - River Valley: 51 returns, 10.5%
   - Southern Plains: 47 returns, 10.8%
5. March 2026 refreshment, by industry group, firms recruited and of them firms that have returned at least once:
   - A Agriculture, forestry and fishing: 34 recruited, 30 returned at least once
   - C Manufacturing: 112 recruited, 100 returned at least once
   - F Construction: 118 recruited, 102 returned at least once
   - G Wholesale and retail trade: 175 recruited, 148 returned at least once
   - H Transport and storage: 72 recruited, 64 returned at least once
   - I Accommodation and food: 81 recruited, 67 returned at least once
   - J Information and communication: 70 recruited, 60 returned at least once
   - M Professional and technical services: 139 recruited, 125 returned at least once
   - N Administrative and support services: 107 recruited, 99 returned at least once

### bcs_sep2026_response.pptx

1. One slide: a column for each region's response rate at the main close (non-returners with no register closure counted in scope at 84.7%), coloured by alert level, with dashed lines at 55% and 58%; title "Capital and Harbour go into the reminder-call extension; Islands and Western Uplands get the extra email".

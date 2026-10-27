## Tags

**Domain:** Quantitative Finance (market microstructure and execution cost: each venue's adverse move in the minute after a fill, read for single whole orders from a year of an asset manager's algorithmic fills).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**The board should keep Delvenne lit, Ardenwick mid, Thursgate mid and Quintrell SI off the platform's venue list and send the platform's orders to Wexcombe, Ardenwick lit, Delvenne Midpoint and Brindock SI.**
Read on the desk's 2026 fills with no desk trade in the same share in the following minute, the four meet an average adverse move of 2 (Delvenne lit), 3 (Ardenwick mid), 2 (Thursgate mid), 2 (Quintrell SI) basis points against the policy's 1.5. Not every 2026 fill averaged, which counts the same order's following child fills inside each fill's minute and passes Ardenwick mid and Thursgate mid; not the desk's 2026 single orders, which never used the midpoint books; not a short horizon, which stops before the move is made.

## 2. Critical Components

1. Delvenne MTF lit book's adverse move for the platform's orders is **2 basis points**.
2. Ardenwick MTF midpoint book's adverse move for the platform's orders is **3 basis points**.
3. Thursgate MTF midpoint book's adverse move for the platform's orders is **2 basis points**.
4. Quintrell Markets SI's adverse move for the platform's orders is **2 basis points**.

## 3. Step-by-Step Solution

1. Took the executions in hessenby_tca_executions_2026-01-02_to_2026-10-30.csv once each (one row per broker_exec_id), left out those ashlowe_execution_report_2026.csv and pemberwick_execution_report_2026.xlsx report as busted and the closing auction, and computed each fill's adverse move from mid_at_exec and mid_plus_60s as the adverse-move test in order_execution_policy_2025.pdf defines it: 171,750 fills.
2. Kept the fills after which no other desk execution in the same share, busted ones included, printed within 60 seconds, the platform's orders being sent whole and filled in one execution (wealth_dealing_plan_2027.pdf 4), with THGD and THGM as Thursgate's one book (venue_register_2026.xlsx): 69,118 fills.
3. Averaged each venue's adverse move over those fills and kept off the list every venue above 1.5 basis points: Delvenne lit, Ardenwick mid, Thursgate mid and Quintrell SI.
4. For the market orders, took each client order with a Gresmere note dated 1 January to 30 October 2026 (cancelled notes out, the new system's second issue of an end-of-June trade the old system had noted, same order, trade date, time and shares, out, an order's parts summed) at the dealing point its placed_at, a UTC time, gives under the plan's 15-minute cut-offs and the trading calendar, netted buys and sells in each share at each point, and divided each market order by the share's ADV, the consolidating line's shares before 18 May divided by ten (corporate_actions_2026.json), the order book carrying the new line's code on every order: mean sizes 0.169, 0.119 and 0.112 per cent.
5. For Gresmere's 2026 dealing, valued each effective note at shares times price_gbx, since the consideration column carries stamp duty on the old system's purchases and the client's net amount on the new system's notes, and took each trade month's purchases less its sales, January to October.
6. The board keeps Delvenne lit, Ardenwick mid, Thursgate mid and Quintrell SI off the list.

## 4. Deliverable Answers

### venue_list_board_paper_2027.pdf

1. Venues kept off the platform's list: Delvenne lit, Ardenwick mid, Thursgate mid and Quintrell SI.
2. Each venue's adverse move for the platform's orders, whole basis points:
   - Wexcombe Stock Exchange: 0, on the list
   - Ardenwick MTF lit book: 1, on the list
   - Delvenne MTF lit book: 2, kept off
   - Ardenwick MTF midpoint book: 3, kept off
   - Delvenne Midpoint: 1, on the list
   - Thursgate MTF midpoint book: 2, kept off
   - Brindock Securities SI: 0, on the list
   - Quintrell Markets SI: 2, kept off
3. Bar chart of the eight venues' adverse moves against the 1.5 basis point line, the four kept off in red.

### venue_review_2027.xlsx

4. Mean size of the platform's 2026 dealt orders as market orders under the 2027 dealing plan, per cent of the share's average daily volume, three decimals:
   - 09:30: 0.169
   - 12:00: 0.119
   - 14:30: 0.112
5. Value bought less value sold through Gresmere by trade month, £ million, two decimals:
   - January 2026: 4.72
   - February 2026: 4.40
   - March 2026: 5.05
   - April 2026: 3.71
   - May 2026: 4.31
   - June 2026: 3.13
   - July 2026: 4.65
   - August 2026: 4.23
   - September 2026: 3.18
   - October 2026: 3.87

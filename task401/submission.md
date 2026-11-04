## Tags

**Domain:** Psychology & Behavioral Science, mediation, moderation and process modelling (a charitable leisure trust's membership after its January and February 2026 changes, read through the members who stop coming before they cancel).  
**Analytical objective:** Root-Cause Analysis (which of the changes will cost the trust the most members over the 2026-27 membership year).

## 1. Final Recommendation

**Reverse the Rewards closure.** It will cost about 690 members over the 2026-27 membership year (2 February 2026 to 31 January 2027), 2.16 times the legacy terms letters at about 320, whose cancellations made February's spike. Not the letters: most of the members they prompted had stopped coming long before and would have cancelled within the year anyway. Not the daytime timetable (about 190), the shorter hours at Northgate and Westcroft (about -90) or the member care calls, which bring members back.

## 2. Critical Components

1. The closure: -101 cancellations against the same weeks of 2025 by 16 March, and **1,027** more Rewards holders with no visit in the 28 days to 16 March than a year earlier; last year **76.8 per cent** of holders in that position cancelled before the membership year ended, so the year's cost is about **690**.
2. The letters: **1,062** more legacy cancellations by 16 March than in the same weeks of 2025, but 1,091 fewer legacy members not visiting than a year earlier, who on last year's 68.3 per cent would have cancelled within the year: about **320**.
3. The rest: the timetable about 190, the hours cut about -90, and the care calls lower cancellations.

## 3. Step-by-Step Solution

1. Took each change's members from savings_programme_2025-26.docx: Rewards holders on 31 January 2026 (rewards_account_opened in membership_register_2026-03-16.csv), legacy tariffs (codes L-) on 2 February, weekday class bookings starting before 5pm from 13 October 2025 to 11 January 2026 (class_bookings_2024-10-07_to_2026-03-15.parquet), home centre Northgate or Westcroft; and the members in the same position 364 days earlier, the same weeks of 2025-26 (Schedule 4, 4.3).
2. Counted each membership once at its first request (Schedule 4, 4.1) in cancellation_requests_2024-01-01_to_2026-03-15.csv; for each change, the cancellations from its date to 16 March among its members not already leaving, less the same weeks of 2025 at that year's rate: closure -101, letters +1,062, timetable +66, hours +84.
3. From access_weekly_usage_2024-01-01_to_2026-03-15.parquet, members on the books with no visit in the 28 days before 16 March 2026 and before 17 March 2025, as a share of each change's members, the difference times its members now: closure +1,027, letters -1,091, timetable +222, hours -251.
4. Of last year's members of each change in that position on 17 March 2025, the share whose first request came before 2 February 2026, the end of that membership year: 76.8, 68.3, 54.8 and 70.2 per cent.
5. Each change's year is step 2 plus step 3 times step 4: the closure about 690, the letters about 320, the timetable about 190, the hours about -90; the closure is the largest.
6. Admissions: old till lines with a Family Swim read as its party from the price list's pay-as-you-go sheet; EPOS lines by transaction, a Swim and Gym ticket's two 4.70 lines one person; voids netted in both; EPOS refunds made inside a closure in pool_closures_2025-10-01_to_2026-03-15.csv kept, those swimmers were admitted; month of sale, site codes from the EPOS notice.
7. Fees: bureau A dated the working day after its processing date and re-presentations to their first month; bureau B by mandate (dd_mandates_2026-03-16.csv) over the household (paid_by_membership_no); a returned collection's fees counted when a later collection clears, including a bureau A collection refused twice and taken in December by bureau B; the administration charge out; each fee in the month its household's collection day falls in.

## 4. Deliverable Answers

### change_review.pdf

1. Change to reverse: the Rewards closure (1 February 2026), about 690 members over the 2026-27 membership year.
2. Why each of the others costs fewer: the legacy terms letters about 320 (cancellations brought forward from later in the year), the daytime timetable about 190, the shorter hours at Northgate and Westcroft about -90, the member care calls fewer cancellations.
3. Chart: one bar per change of its membership-year cost, split into the cancellations so far and the part still to come or already brought forward, the closure's largest.

### monthly_return.xlsx

1. Pay-as-you-go admissions, each person once, nearest 10:
   - October 2025: Northgate and Westcroft 4,130, other centres 14,570
   - November 2025: Northgate and Westcroft 3,910, other centres 13,850
   - December 2025: Northgate and Westcroft 3,180, other centres 10,830
   - January 2026: Northgate and Westcroft 4,520, other centres 16,400
   - February 2026: Northgate and Westcroft 3,310, other centres 13,660
2. Membership fees for the month they pay for, nearest GBP 100:
   - November 2025: legacy tariffs GBP 234,100, 2023 tariffs GBP 498,000
   - December 2025: legacy tariffs GBP 223,800, 2023 tariffs GBP 493,900
   - January 2026: legacy tariffs GBP 214,000, 2023 tariffs GBP 531,400
   - February 2026: legacy tariffs GBP 202,000, 2023 tariffs GBP 533,600

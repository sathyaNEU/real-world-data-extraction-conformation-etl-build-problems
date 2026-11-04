## Tags

**Domain:** Product Analytics, funnel and journey analysis (a Canadian subscription streaming service's free-trial conversion and the one programme its subscriber growth budget funds for the 2026-27 winter).  
**Analytical objective:** Root-Cause Analysis (which cause of the 2025-26 winter's fall in trial-to-paid conversion the funded programme fixes).

## 1. Final Recommendation

**Fund (C), the winter release slate.** Its cause cost about 2,100 of the 2025-26 winter's paid conversions, 1,900 more than the runner-up. Not (A) the first-month price hold (about 200): the fall holds in every segment and lands on the price date only because the autumn finales closed October the same week, and trialists with no season still to come converted almost as they did a year earlier. Not (B) first-charge recovery or (D) the paid acquisition mix (about 100 each).

## 2. Critical Components

1. The slate's cost, last winter's conversion less that of last winter's trialists with no season still to come, at this winter's trials (none of which had one): **2,100** paid conversions.
2. The price's cost, the rest of the fall less first-charge recovery and the channel mix: **200**.
3. First-charge recovery **100** and the paid acquisition mix **100**; the slate leads the price by **1,900**.

## 3. Step-by-Step Solution

1. Read trial_register.csv as one row per trial: the old platform's rows from 9 June 2025 carry Toronto time stamped Z, and its copies of web and phone sign-ups, which match a new-platform row field for field once re-timed, were dropped; trials counted by start date in Toronto time (conversion_standard_v3.pdf, section 2): 17,965 and 17,292 in the two winters.
2. Linked each trial to its first-charge attempts in charges_processor_a_2024-11_2025-09.csv and charges_processor_b_2025-09_2026-02.csv through the subscription it ended on (plan_changes.csv; section 4): conversion 51.7 per cent last winter and 37.1 per cent this winter, about 2,500 paid conversions at this winter's trials.
3. Set each trial's plays in trial_viewing_2024-11_2026-02.parquet (legacy numbers through account_crosswalk.csv and content_crosswalk.csv) against release_calendar.xlsx: last winter 70.2 per cent of trials had played a season whose last episode came out after their trial ended and paid at 56.9 per cent, against 39.4 per cent for the rest; this winter none had.
4. The slate: last winter's 51.7 per cent less 39.4 per cent, at this winter's trials: 2,100; first-charge recovery: declined first charges recovered fell from 72.0 to 52.5 per cent, on this winter's declined first charges: 100; the channel mix: last winter's channel shares at this winter's paid rate by channel: 100; the price takes the rest: 200.
5. Paid, trials started February to October 2025: a plan change made on the old platform before 9 June or in the apps before 14 October opened a subscription that no file links to its trial; each such first charge was matched to the trial without a charge whose end most closely precedes its first attempt, in the provinces its tax rate names: the shares in block 4.
6. Episodes, the same trials: the smart TV app's rows from 8 February to 27 October 2025 each cover an autoplay run, the episode named and the season's following episodes as far as the minutes reach on the calendar's runtimes; episodes counted once a trial (section 5) and averaged over every trial, including those that played nothing: the averages in block 4.
7. Ranked the four causes: the slate at 2,100 against 200 for the price takes the budget.

## 4. Deliverable Answers

### trial_conversion_review.xlsx

1. Share of each winter's November to January trials that played an episode: 94.3 per cent in 2024-25, 94.0 per cent in 2025-26.
2. Share still subscribed when the trial ended: 52.7 per cent and 38.4 per cent.
3. Share of their first charges collected: 98.0 per cent and 96.6 per cent.
4. Paid conversions each programme's cause cost this winter's trials, to the nearest hundred:
   - (A) First-month price hold: 200
   - (B) First-charge payment recovery: 100
   - (C) Winter release slate: 2,100
   - (D) Paid acquisition mix: 100
5. Programme to fund: (C) the winter release slate.
6. Runner-up: (A) the first-month price hold.
7. Gap: 1,900 paid conversions.
8. Trials started in each month of 2025, share that paid and average number of episodes played during the trial:
   - February: 50.9 per cent, 4.9 episodes
   - March: 51.2 per cent, 5.4 episodes
   - April: 54.0 per cent, 5.7 episodes
   - May: 52.4 per cent, 5.8 episodes
   - June: 52.2 per cent, 6.4 episodes
   - July: 53.9 per cent, 7.1 episodes
   - August: 54.9 per cent, 8.0 episodes
   - September: 54.1 per cent, 9.1 episodes
   - October: 49.9 per cent, 8.8 episodes

### winter_conversion_note.pdf

1. Waterfall from last winter's conversion rate at this winter's trials, 8,900 paid conversions, to this winter's 6,400, one bar per programme's cause: the slate 2,100, the price 200, first-charge recovery 100, the paid acquisition mix 100.

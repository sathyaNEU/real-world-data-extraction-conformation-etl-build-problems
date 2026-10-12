Example prompts
Pick one domain and one analytical objective, then shape it into the deliverable contract

Every task carries one domain and one Axis 1 analytical objective, chosen before you write a word of the prompt. Forecasting & Predictive Modeling is an objective, not an eighth domain: any accepted domain can carry it when the evidence pins the answer down, and we want more of those.

Step 1. Choose one domain
Six accepted domains. Pick the one whose decision-maker would actually own the call.

Domain

Product Analytics

Supply Chain & Logistics

Economics

Policy & Education

Demographic & Social Science

Nonprofit & Grant-making
The format every prompt now uses
Whatever objective you pick, the prompt is shaped the same way: a short stakeholder context, one committed recommendation ask, then a bullet list of 3 or more deliverables (no upper limit) with their file types, spanning the two format families assigned to you, and under each deliverable at least three specific asks.

One deterministic recommendation

Anchors the whole task. One committed call, one defensible answer.

3 or more deliverables, across the two assigned families
decision_memo.pdf
Text
Give me a one-page decision memo in decision_memo.pdf I can take to the review.

Open with the recommended option, name the strongest option it beats, and say in one sentence why the runner-up loses.
State the gap between them on the deciding metric in that metric's own unit (for example percentage points or dollars), to one decimal place, and cite the file and field the number came from.
Close with the one condition that would flip the recommendation, stated as a numeric threshold on that same metric, in its unit.
options_scan.xlsx
Data
Attach the full comparison in options_scan.xlsx so the team can audit it.

One row per option with its deciding-metric value in the metric's unit to one decimal place, and its rank as a whole number.
A final column naming the one change that would flip the recommendation.
A total row that reconciles to the figure cited in the memo, so the audit trail ties out.
margin_chart.png
Visual
Include margin_chart.png so the recommendation reads at a glance.

Plot the deciding metric by option in the metric's unit, with the recommended option and the runner-up labeled.
Order the bars from best to worst on that metric.
Mark the numeric threshold that would flip the recommendation.
Every deliverable is a natural request that names the file, and carries at least three asks: a supplementary question or a specific requirement about what the file must contain. The asks replace the old standalone supplementary-questions section.

Two worked examples in that format, on different objectives:

Anomaly detection and diagnostics
3 deliverables
Mobile checkout conversion fell 6 percent day over day on Tuesday, and the on-call PM has to decide tonight whether to page the payments team. The team ships continuously and traffic mix swings a lot between weekdays and weekends.

Tell me whether to escalate this drop to payments tonight or treat it as normal fluctuation.

checkout_conversion_triage.pdf
Text
Write up the escalate-or-hold call in checkout_conversion_triage.pdf so the on-call PM can act on it immediately.

State plainly whether Tuesday's 6 percent drop clears the bar to page payments tonight.
Explain how much of the day-over-day move, in percentage points to one decimal place, is attributable to the shifting weekday-to-weekend traffic mix versus a genuine funnel regression.
State the escalation threshold in percentage points and whether Tuesday's move exceeds it.
Name the single traffic segment driving the largest share of the genuine, mix-adjusted drop, and give that share in percentage points to one decimal place.
Name the funnel step where the genuine regression concentrates and its step-conversion change in percentage points to one decimal place.
conversion_by_day_and_segment.csv
Data
Give me the underlying numbers as conversion_by_day_and_segment.csv so the call can be sanity-checked.

Show daily conversion, as a percentage to one decimal place, for the recent window alongside the comparable prior baseline the decision rests on.
Break the numbers out by the traffic segments that changed mix, so the Tuesday gap can be traced to its source.
Include one row per day-segment with sessions as a whole-number count and conversion as a percentage to one decimal place.
conversion_triage_chart.png
Visual
Include conversion_triage_chart.png so the on-call PM can see the move at a glance.

Plot daily mobile checkout conversion, as a percentage to one decimal place, across the recent window with Tuesday marked.
Overlay a mix-adjusted conversion line so genuine regression is separable from mix shift.
Show the comparable prior baseline as a reference band, in conversion percent to one decimal place.
Forecasting
3 deliverables
A subscription app owes Finance one committed Q3 renewal-revenue number by Thursday, from three years of billing history.

Give a single committed Q3 renewal-revenue figure and say whether the current trend supports the board's growth target.

forecast.py
Code
Hand me a runnable forecast.py that reproduces the number from the shipped files.

Print the committed Q3 renewal-revenue figure in USD rounded to the nearest thousand, with its 80% interval in the same unit.
Print the holdout error for each of the last four quarters as MAPE in percent to one decimal place.
Print whether the current trend clears the board's growth target, as a yes or no with the gap in USD to the nearest thousand.
finance_note.docx
Text
Write the one-page finance_note.docx I can forward to the board.

State the Q3 figure in USD to the nearest thousand and whether it clears the board's growth target.
Name the single assumption that would move the number most, and by how much, in USD to the nearest thousand.
Close with the one trend condition that would put the target out of reach, stated as a numeric threshold in USD to the nearest thousand.
monthly_actuals.csv
Data
Include monthly_actuals.csv backing the estimate.

One row per month with actual and fitted renewal revenue in whole USD.
Flag the months excluded from training and give the reason.
A total row that reconciles fitted revenue to the committed Q3 figure.
The full contract, the kinds of asks, and the annotated walkthrough live on Writing the prompt.

Example prompts by objective
Browse the library for scenarios across every objective and domain. Each one is written in the current format: a stakeholder context, one recommendation, and 3 or more named deliverables (no upper limit) with their asks. Filter by objective or domain, or search for a scenario, and adapt the closest match.

Search these example prompts
For example: churn, forecast, allocate, hold
Filter by objective
All objectives
Descriptive & Distribution Analysis
Anomaly Detection & Diagnostics
Root-Cause Analysis
Experiment & Causal Analysis
Forecasting & Predictive Modeling
Data Extraction & Conformation (ETL / Pipeline Build)
Filter by domain
All domains
Product Analytics
Supply Chain & Logistics
Economics
Policy & Education
Nonprofit & Grant-making
Demographic & Social Science
60 prompts shown. Open an objective to read its prompts.


Descriptive & Distribution Analysis
The decision turns on how a population is composed or how a metric is distributed, not on why it moved.
10 prompts
Product Analytics
Our mobile note-taking app averages 14 sessions per user per week, but the growth team suspects that headline figure hides very different kinds of users. Alongside weekly session counts we have each active user's 30-day retention flag and whether they converted to premium, plus each usage tier's share of the base from last quarter so we can check whether the structure is stable.

Tell us whether to treat the active base as one population or design around distinct usage tiers, and which single tier to prioritize for investment.

report.pdf
Text
Give me a written recommendation in report.pdf that makes the one-population-vs-tiers call and defends it.

State whether weekly engagement is broadly shared or driven by distinct usage tiers, and how many tiers the data supports as a whole number
If tiers are warranted, give the share of the active base in each tier, as a percentage to one decimal place
Recommend which single tier to prioritize for investment, justified by its 30-day retention and premium-conversion rates rather than its size alone
Report the median weekly sessions for the largest tier and for the power-user tier, each in sessions to one decimal place
State the share of all weekly sessions delivered by the power-user tier, as a percentage to one decimal place
session_distribution.csv
Data
Hand me session_distribution.csv breaking down weekly sessions per user across the active base.

Include one row per weekly-session band with the count and percent of users in it, the count as a whole number and the percent to one decimal place
Report the overall median, mean, and p90 weekly session counts, each in sessions to one decimal place
Add a column assigning each band to a usage-tier label such as casual, regular, or power
Report the modal weekly-session band and the share of users it holds, as a percentage to one decimal place
Include a total row confirming the user counts sum to the active base, as a whole number
tier_economics.csv
Data
Add tier_economics.csv so the prioritization call rests on retention and value, not just tier size.

Give one row per usage tier
Report the 30-day retention rate for each tier, as a percentage to one decimal place
Report the premium-conversion rate for each tier, as a percentage to one decimal place
Include each tier's change in share of the active base versus last quarter, in percentage points to one decimal place
engagement_histogram.png
Visual
Include engagement_histogram.png showing how weekly sessions are spread across users.

Show how weekly sessions are spread across the active base as a histogram
Overlay the median and p90 as labeled vertical lines, each in sessions to one decimal place
Make any secondary bump in the high-session range clearly visible and annotate the tier boundaries in weekly sessions
Title the figure stating whether engagement is one population or distinct tiers and how many tiers the data supports
Product Analytics
Time-to-first-value, measured as minutes from signup to the first saved project, is the metric our onboarding team wants to move, evaluated on last quarter's new accounts. Each account also carries its 30-day retention outcome and its acquisition channel, so a proposed cutoff can be validated against whether fast activators actually retain and whether it holds across channels. We can also look at retention decile by decile, not just on either side of one line.

Decide where a defensible activate-versus-stall cutoff sits, whether it holds across channels, and whether to adopt it.

analysis.py
Code
Write analysis.py that builds the distribution and flags the activation cutoff you would adopt.

Build the time-to-first-value distribution by decile and print minutes-to-first-value at each decile, in minutes to one decimal place
Print the overall median time-to-first-value, in minutes to one decimal place
Mark which band boundary you would set as the activate-versus-stall cutoff, in minutes to the nearest whole minute
Print the number of new accounts analyzed from last quarter, as a whole number
Print the 30-day retention rate for accounts on each side of the chosen cutoff, each as a percentage to one decimal place
ttv_percentile_bands.csv
Data
Have analysis.py save ttv_percentile_bands.csv with the percentile-band table behind the call.

Include one row per decile with minutes-to-first-value at the boundary, in minutes to one decimal place
Include the count of accounts in each band as a whole number and the cumulative share activated at or before each decile, as a percentage to one decimal place
Add the 30-day retention rate within each decile, as a percentage to one decimal place
Include a total row confirming account counts sum to the base
channel_cutoff_check.csv
Data
Add channel_cutoff_check.csv so we can see whether the cutoff holds across acquisition channels.

Give one row per acquisition channel
Report each channel's median time-to-first-value, in minutes to one decimal place
Report the share of each channel's accounts on the fast side of the chosen cutoff, as a percentage to one decimal place
Flag any channel whose median falls on the stall side of the cutoff
onboarding_cutoff_note.pdf
Text
Add onboarding_cutoff_note.pdf summarizing the cutoff for the onboarding team.

State the cutoff in minutes and the share of new accounts on each side of it, the cutoff to the nearest whole minute and each share as a percentage to one decimal place
State whether fast activators retain better, citing the retention gap across the cutoff in percentage points to one decimal place
Note how much the cutoff moves in minutes to one decimal place if it is nudged to the neighboring decile boundary, as a robustness check
Recommend whether to adopt the cutoff and whether it holds across channels
activation_cutoff_deck.pptx
Visual
Build activation_cutoff_deck.pptx so the onboarding team can see the cutoff and the retention step behind it.

Plot minutes-to-first-value across the deciles as an annotated percentile chart and draw a labeled vertical cutoff line at the chosen boundary in whole minutes
Overlay the 30-day retention rate by decile as a second series on a secondary axis so the retention step across the cutoff is visible
Mark and label the overall median time-to-first-value line, in minutes to one decimal place
Include a small-multiple panel of the time-to-first-value distribution per acquisition channel, each panel annotated with that channel's share on the fast side, as a percentage to one decimal place
Close with a findings slide stating the recommended cutoff, the retention gap across it in percentage points to one decimal place, and whether to adopt it
Supply Chain & Logistics
Our regional warehouse ships thousands of SKUs and the ops director claims most of the storage cost comes from a minority of slow movers. We hold per-SKU annual picks, cubic storage footprint, unit holding cost, and the one-time slotting labor cost, so the case can weigh recurring cost, freed space, and payback rather than picks alone.

Recommend whether a tail-focused deslotting program is justified.

report.pdf
Text
Deliver report.pdf that settles whether the dead-stock tail is real and makes the deslotting call.

State whether a concentrated tail of dead stock is real or just perception, and how many SKUs sit in the slow-moving tail as a whole number
Quantify the share of SKUs and the share of annual storage cost in the slow-moving tail, each as a percentage to one decimal place
Recommend whether the tail-focused deslotting program is justified, with the payback period in months to one decimal place
State the projected annual storage-cost savings and the square footage freed, savings in USD to the nearest whole dollar and space to the nearest hundred square feet
inventory_turns.csv
Data
Attach inventory_turns.csv with the SKU-level turns behind the finding.

Report the turns distribution across SKUs with one row per turn band, turns as a ratio to two decimal places and the SKU count per band as a whole number
Add a column ranking SKUs by annual storage cost and list the top 10 cost-carrying slow movers, cost in USD to the nearest whole dollar
Flag the SKUs with zero or near-zero picks over the period
Include the cumulative share of storage cost against cumulative share of SKUs at each turn band, each as a percentage to one decimal place
deslotting_economics.csv
Data
Add deslotting_economics.csv laying out the cost and space case by action group.

Give one row per action group: keep, deslot-to-reserve, and liquidate
Report the SKU count, annual storage cost, and square footage for each group, counts as whole numbers, cost in USD to the nearest whole dollar, space to the nearest hundred square feet
Include the one-time slotting labor cost for the deslot and liquidate groups, in USD to the nearest whole dollar
Include a total row across all groups
slow_mover_deck.pptx
Visual
Put together slow_mover_deck.pptx to walk leadership through the case.

Show the SKU-count versus storage-cost split between fast and slow movers, with SKU counts as whole numbers and storage cost in USD to the nearest whole dollar
Include a slide plotting cumulative share of storage cost against cumulative share of SKUs, with the point where the slow-moving tail begins labeled
Include a slide sizing the space deslotting the tail would free, in square feet to the nearest hundred
Close with the projected annual storage-cost savings net of the one-time slotting cost and the payback period, savings in USD to the nearest whole dollar and payback in months to one decimal place
Supply Chain & Logistics
The procurement team splits spend across a large supplier roster and leadership wants to know how exposed we are if a few vendors fail. Each supplier record also carries its spend category, whether it is single-sourced with no qualified alternate, and its average lead time, so concentration can be judged by substitutability, not spend share alone.

Recommend whether the supplier base is concentrated for continuity-planning purposes, and which vendors are the true continuity risks.

report.pdf
Text
Deliver report.pdf that characterizes supplier spend concentration and makes the continuity-planning call.

State whether the roster is effectively a few critical partners plus a long fringe, and give the count of suppliers that are true continuity risks as a whole number
Quantify how much annual spend rides on the top handful of suppliers and the single largest supplier's individual share, each as a percentage of annual spend to one decimal place
Report the Herfindahl-Hirschman Index of supplier spend to the nearest whole number and state whether it crosses the concentration threshold
State how much of annual spend sits with single-sourced suppliers, as a percentage to one decimal place, and whether that changes the continuity call
supplier_spend_shares.csv
Data
Include supplier_spend_shares.csv ranking suppliers by their share of spend.

Include one row per supplier ranked by spend share, with cumulative spend share, as a percentage to one decimal place
Flag any supplier individually above a 10 percent share of annual spend
Add columns for the supplier's category and single-source flag
Include the count of suppliers needed to reach 80 percent of cumulative annual spend, as a whole number
category_exposure.csv
Data
Add category_exposure.csv so we can see where within-category dependence hides.

Give one row per spend category
Report each category's share of annual spend and its top supplier's within-category share, each as a percentage to one decimal place
Report each category's average supplier lead time in days to one decimal place
Flag categories where a single supplier holds more than half the category spend
supplier_exposure.html
Visual
Give me supplier_exposure.html so leadership can explore the concentration interactively.

Show spend share by supplier from largest to smallest, with the share axis in percent to one decimal place
Overlay a cumulative-share Pareto line on the bars with the 80 percent cumulative mark labeled
Highlight the single-sourced vendors whose loss would account for most of the spend
Include a findings panel stating whether the roster is concentrated, the Herfindahl-Hirschman Index value, and the count of true continuity-risk vendors
Economics
We have household net-worth microdata for a national survey wave and a policy client asking how wealth is distributed across the population. The extract also carries each household's income and age band, so the upper tail can be checked for whether it is a wealth phenomenon distinct from income and whether it concentrates in particular age bands.

Settle whether wealth concentration has a long upper tail worth separate policy treatment.

analysis.py
Code
Write analysis.py that produces the wealth distribution and the upper-tail figures.

Produce the wealth distribution by percentile and print net worth at each decile, in USD to the nearest whole dollar
Output the top-1 percent and top-10 percent shares of total wealth, each as a percentage to one decimal place
Report the Gini coefficient for net worth to three decimal places
Print the number of households in the extract as a whole number and the count with zero or negative net worth
wealth_percentiles.csv
Data
Have analysis.py write wealth_percentiles.csv with the percentile table.

Include one row per percentile with net worth at that percentile, in USD to the nearest whole dollar
Report the mean net worth within the top 1 percent against the overall median, each in USD to the nearest whole dollar
Include the ratio of the 99th-percentile net worth to the median, to one decimal place
Include a summary row with aggregate net worth across all households, in USD to the nearest whole dollar
wealth_by_age_income.csv
Data
Add wealth_by_age_income.csv so the client can see whether the tail tracks income and age.

Give one row per age band
Report each age band's share of total wealth and its median net worth, share as a percentage to one decimal place and median in USD to the nearest whole dollar
Report the correlation between income rank and wealth rank overall, to two decimal places, so the client can see how far wealth tracks income
Flag the age band that holds the largest share of the top-1-percent households
tail_findings.pdf
Text
Add tail_findings.pdf summarizing the shape for the policy client.

State how heavy the upper tail is relative to the bulk of households, and whether it is heavy enough to warrant separate treatment
State the top-1 percent share and the 99th-to-median ratio as the two headline tail figures, share to one decimal place and ratio to one decimal place
State whether the upper tail is concentrated in particular age bands or spread across them
Note whether wealth concentration exceeds income concentration, citing both Gini coefficients to three decimal places
wealth_distribution.html
Visual
Give me wealth_distribution.html so the policy client can explore the shape of the distribution.

Show net worth across percentiles as an annotated percentile chart, with the median and the 99th-percentile point marked and labeled in USD to the nearest whole dollar
Include a Lorenz-curve panel of net worth with the Gini coefficient shown in the caption to three decimal places
Include an ordered bar panel of each age band's share of total wealth from largest to smallest, with the age band holding the most top-1-percent households highlighted
Add a findings header stating whether the upper tail warrants separate policy treatment and the top-1 percent share to one decimal place
Let the user hover to read net worth at each decile, in USD to the nearest whole dollar
Economics
Monthly firm-level revenue data for the county's small businesses came in and the development office wants a picture of the size distribution. The dataset also includes each firm's employee count, industry sector, and whether it received prior county assistance, so the office can size outreach by revenue, weigh the jobs at stake, and target sectors rather than only describe the shape.

Recommend which characterization and outreach segmentation the office should use.

report.pdf
Text
Deliver report.pdf that characterizes firm sizes and recommends the outreach segmentation.

State whether firm sizes form a smooth heavy-tailed shape or distinct micro, small, and mid clusters, and how many clusters the data supports as a whole number
Recommend the segmentation the development office should use for outreach
Report the median and mean monthly firm revenue, each in USD to the nearest thousand
State the share of firms in the smallest cluster and the share of total county revenue held by the mid cluster, each as a percentage to one decimal place
State the share of total county employment held by the mid cluster, as a percentage to one decimal place, so the office can weigh jobs alongside revenue
firm_size_distribution.xlsx
Data
Attach firm_size_distribution.xlsx with the size breakdown behind the call.

Report firm counts across revenue bands with one row per band, counts as whole numbers
Show where any breaks between size clusters fall, in monthly revenue USD to the nearest thousand
Include the share of total county revenue held by each band, as a percentage to one decimal place
Include a total row confirming firm counts sum to the county total
cluster_profiles.csv
Data
Add cluster_profiles.csv profiling each size cluster for outreach.

Give one row per size cluster
Report each cluster's firm count, median monthly revenue, and median employee count, counts as whole numbers and revenue in USD to the nearest thousand
Report each cluster's share of total county employment, as a percentage to one decimal place
Report each cluster's share of firms that have never received prior county assistance, as a percentage to one decimal place
Name each cluster's most common industry sector
firm_size_clusters.png
Visual
Include firm_size_clusters.png showing the revenue distribution across firms.

Plot the revenue distribution across all firms on a log revenue axis and state the base used
Mark and label the cluster boundaries you would draw, in monthly revenue USD to the nearest thousand
Overlay the median and mean monthly revenue as labeled lines, each in USD to the nearest thousand
Annotate each cluster with its share of firms and its share of total county revenue, each as a percentage to one decimal place
Title the figure stating how many clusters the data supports and the recommended outreach segmentation
Policy & Education
A state agency gave us per-pupil spending figures across all its school districts and wants to know how unequal funding really is. The file also carries each district's enrollment and its share of low-income students, so equity can be judged enrollment-weighted, by how many pupils sit at the extremes, and against need.

Recommend how the agency should characterize funding equity in its annual report.

report.pdf
Text
Deliver report.pdf that characterizes the spending spread and recommends how to frame funding equity.

State whether the disparity is a smooth gradient or a few outlier districts pulling the tails, and how many districts are statistical outliers as a whole number
Recommend how to characterize funding equity in the annual report
Report the ratio of the 90th-percentile district's per-pupil spending to the 10th-percentile district's, to two decimal places
State the same ratio on an enrollment-weighted basis, to two decimal places, so it reflects pupils rather than districts, and note whether the two ratios tell the same story
Report the Gini coefficient of per-pupil spending across districts, to two decimal places
per_pupil_spending.csv
Data
Attach per_pupil_spending.csv with district-level dollars ranked out.

List one row per district with per-pupil dollars ranked high to low, in USD to the nearest whole dollar
Include each district's deviation from the statewide mean, in USD to the nearest whole dollar
Flag districts sitting far above or below the pack
Add each district's enrollment and low-income share, enrollment as a whole number and share as a percentage to one decimal place
equity_summary.csv
Data
Add equity_summary.csv so the report can show whether dollars track need.

Give one row per spending quartile of districts
Report each quartile's mean per-pupil spending and the number of pupils it covers, spending in USD to the nearest whole dollar and pupils as a whole number
Report each quartile's average low-income share, as a percentage to one decimal place
Report the correlation between per-pupil spending and low-income share across districts, to two decimal places
funding_spread.png
Visual
Include funding_spread.png showing the spread of per-pupil dollars across districts.

Show the spread of per-pupil dollars across all districts, with the dollar axis in USD to the nearest hundred
Overlay the statewide median and mean per-pupil lines, each labeled in USD to the nearest whole dollar
Mark and label the highest and lowest outlier districts, each in USD to the nearest whole dollar
Title the figure stating whether the disparity is a smooth gradient or outlier-driven and the 90-to-10 ratio to two decimal places
Policy & Education
Community college students accumulate credits at very different rates and the provost wants to understand momentum in the first year. The data links each student to their second-year persistence outcome and their entry status of part-time or full-time, so pace cohorts can be validated against who actually persists and split by entry status.

Determine whether first-year students cluster into recognizable pace cohorts, where the boundaries sit, and which cohort most needs intervention.

analysis.py
Code
Write analysis.py that builds the credit-accumulation distribution and draws the pace cohorts.

Build the first-year credit-accumulation distribution and print the count of students at each credit total, counts as whole numbers
Output the pace-cohort boundaries you would draw and the number of distinct cohorts the method selects, boundaries in credits to the nearest whole credit and the count as a whole number
Print the mean and median first-year credits, each to one decimal place
Print the number of students analyzed as a whole number
credit_accumulation.csv
Data
Save credit_accumulation.csv with the per-student credit totals and cohort labels.

Include a student_id column and each student's first-year credit total and assigned pace cohort, one row per student
Report the count and share of students in each pace cohort, counts as whole numbers and share as a percentage to one decimal place
Add each student's entry status and second-year persistence flag
Include a total row confirming student counts sum to the base
cohort_outcomes.csv
Data
Add cohort_outcomes.csv so the pace cohorts are validated against real outcomes.

Give one row per pace cohort
Report each cohort's second-year persistence rate, as a percentage to one decimal place
Report each cohort's split between part-time and full-time entrants, each as a percentage to one decimal place
Report the mean first-year credits for the fastest and slowest cohort, each in credits to the nearest whole credit
provost_momentum_brief.docx
Text
Add provost_momentum_brief.docx summarizing first-year momentum for the provost.

State how many distinct pace cohorts the data supports as a whole number and where the boundaries sit in credits
Give the share of students in the slowest-pace cohort and the modal first-year credit total, share as a percentage to one decimal place and the mode as a whole number
Recommend which cohort most needs intervention, justified by its persistence rate rather than its size
State the persistence gap between the fastest and slowest cohort, in percentage points to one decimal place
credit_pace_smallmultiples.png
Visual
Include credit_pace_smallmultiples.png showing the credit-accumulation distribution and the pace cohorts.

Plot the first-year credit-accumulation distribution across students with the credit axis in whole credits
Mark and label the pace-cohort boundaries as vertical lines, in credits to the nearest whole credit
Overlay the mean and median first-year credits as labeled lines, each to one decimal place
Add a small-multiple panel splitting the distribution by entry status, part-time and full-time, each panel annotated with that group's second-year persistence rate as a percentage to one decimal place
Title the figure stating the number of distinct pace cohorts and which cohort most needs intervention
Nonprofit & Grant-making
A community foundation gave us its full donation ledger for the year and the board wants to know how reliant it is on major gifts. The ledger also flags whether each donor is recurring or one-time and whether they gave last year, so dependence can be judged against renewal risk, not just this year's shares.

Recommend whether the foundation should characterize its funding as major-donor dependent and how exposed it is to lapse.

report.pdf
Text
Deliver report.pdf that describes the donation distribution and makes the major-donor-dependence call.

Quantify the share of total dollars from the largest donors versus the broad base, each as a percentage to one decimal place, and state whether funding is major-donor dependent
Report the share of total dollars from the top 10 donors and the number of donors who together give half of all dollars, share to one decimal place and count as a whole number
Report the Gini coefficient of gift dollars across donors, to two decimal places
State the dollars at risk if the top 5 donors lapsed and what share of total that is, dollars in USD to the nearest whole dollar and share as a percentage to one decimal place
donation_shares.csv
Data
Attach donation_shares.csv ranking donors by their share of dollars.

Include one row per donor with donor rank, gift dollars, and cumulative dollar share, dollars in USD to the nearest whole dollar and share as a percentage to one decimal place
Add each donor's recurring-or-one-time flag and whether they also gave last year
Flag donors individually above a 5 percent share of total dollars
Include a total row with total dollars raised, in USD to the nearest whole dollar
donor_retention.csv
Data
Add donor_retention.csv so the board can weigh dependence against renewal risk.

Give one row per donor tier: top 10, next tier, and broad base
Report each tier's share of total dollars and its year-over-year donor retention rate, each as a percentage to one decimal place
Report each tier's share of dollars coming from recurring donors, as a percentage to one decimal place
Report the count of donors in each tier as a whole number
gift_concentration.pptx
Visual
Put together gift_concentration.pptx to present the picture to the board.

Show the dollar split between the top donors and the broad base, in USD to the nearest whole dollar
Include a Pareto slide with cumulative dollar share against donor rank, with the 50 percent and 80 percent cumulative marks labeled
Include a slide on the lapse exposure if the largest donors did not renew, in USD to the nearest whole dollar
Close with a findings slide stating whether funding is major-donor dependent and the Gini coefficient of gift dollars to two decimal places
Demographic & Social Science
A city planner shared anonymized commute-time records from the latest travel survey and wants to know how the burden is spread across residents. Each record also carries the resident's primary commute mode of car, transit, or active travel and their home district, so the plan can see whether the extreme-commute tail is a mode problem and where it concentrates geographically.

Recommend which framing the transportation plan should adopt and where to focus.

report.pdf
Text
Deliver report.pdf that characterizes commute times and recommends the framing for the plan.

State whether the story is a heavy tail of extreme commuters or a broadly shifted middle, and what share of residents are extreme commuters as a percentage to one decimal place
Recommend which framing the transportation plan should adopt and which one district to focus on
Report the median and p95 one-way commute, each in minutes to one decimal place
State whether the extreme tail is concentrated in one commute mode, citing the median commute by mode in minutes to one decimal place
commute_minutes.csv
Data
Attach commute_minutes.csv with the one-way commute breakdown.

Report the share of residents in each commute-minute band, one row per band, as a percentage to one decimal place
Show the share with one-way commutes over 60 and over 90 minutes, each as a percentage to one decimal place
Report the mean and median one-way commute, each in minutes to one decimal place
Report the modal commute-minute band and the share it holds, as a percentage to one decimal place
Include a total row confirming the resident counts sum to the surveyed base
commute_by_mode_district.csv
Data
Add commute_by_mode_district.csv so the plan can see where and how the tail concentrates.

Give one row per home district
Report each district's median one-way commute and its share of residents commuting over 60 minutes, median in minutes to one decimal place and share as a percentage to one decimal place
Report each district's transit mode share, as a percentage to one decimal place
Flag the district with the heaviest extreme-commute tail
commute_distribution.html
Visual
Give me commute_distribution.html so the planning team can explore the spread.

Show the distribution of one-way commute minutes, with the minutes axis in whole minutes
Highlight the extreme-commuter tail and overlay the median and p95 as labeled lines, each in minutes to one decimal place
Add a small-multiple panel of the commute distribution per commute mode, each panel annotated with that mode's median in minutes to one decimal place
Let the user hover to read the count of residents in each commute-minute band, as a whole number

Anomaly Detection & Diagnostics
Something in the data looks wrong and the analyst must separate a real event from an artifact.
10 prompts
Product Analytics
Mobile checkout conversion fell 6 percent day over day on Tuesday, and the on-call PM must decide tonight whether to page the payments team. We ship continuously, traffic mix swings between weekdays and weekends and across device and OS, and we log funnel-step completion (cart, address, payment, confirmation), payment-gateway error rates per step, and revenue per completed checkout. Our runbook sets a mix-adjusted escalation threshold of 2.0 percentage points.

Tell me whether to escalate this drop to payments tonight or treat it as normal fluctuation.

checkout_conversion_triage.pdf
Text
Write up the escalate-or-hold call in checkout_conversion_triage.pdf so the on-call PM can act on it immediately.

State plainly whether Tuesday's drop clears the 2.0 percentage-point mix-adjusted bar to page payments tonight
Report how much of the day-over-day move, in percentage points to one decimal place, is the shifting weekday-to-weekend and device mix versus a genuine funnel regression
Name the funnel step (cart, address, payment, or confirmation) that accounts for the largest share of the genuine regression
Name the device and OS segment where the genuine regression is concentrated, and state its conversion drop in percentage points to one decimal place
Estimate the daily revenue at risk, in US dollars to the nearest hundred, if the genuine regression persists
conversion_by_day_and_segment.csv
Data
Give me the underlying numbers as conversion_by_day_and_segment.csv so I can sanity-check the call.

Include one row per day and traffic segment, with sessions as a whole-number count and conversion as a percentage to one decimal place
Show daily conversion for the recent window alongside the comparable prior baseline the decision rests on, in percent to one decimal place
Add a mix-adjusted conversion column holding segment composition at the prior-week mix, in percent to one decimal place
Include a new-versus-returning conversion split per day, in percent to one decimal place, so a mix effect from acquisition timing is separable from a returning-user regression
funnel_step_dropoff.csv
Data
Attach funnel_step_dropoff.csv so I can see which step actually moved.

One row per funnel step, with Tuesday's step completion rate and the prior baseline rate, each in percent to one decimal place
Include the payment-gateway error rate per step for Tuesday versus baseline, in percent to two decimal places, so a genuine payment fault is separable from a mix effect
Include the session count entering each step on Tuesday versus baseline as whole numbers, so a step's rate move is weighted by the volume behind it
Flag the single step with the largest adverse deviation from its baseline
conversion_triage_chart.png
Visual
Include conversion_triage_chart.png so the on-call PM can see the move at a glance.

Draw an annotated daily line of mobile checkout conversion across the recent window, y-axis in percent to one decimal place, with Tuesday's flagged point marked and labeled with its date and conversion value
Overlay the mix-adjusted conversion line as a second series so genuine regression is separable from mix shift, and shade the comparable prior baseline as a control band
Draw a labeled horizontal line at the 2.0 percentage-point escalation threshold below baseline, so it is visible whether Tuesday clears the bar
Add a per-segment small-multiple panel with one mini panel per device-and-OS segment showing that segment's conversion versus its baseline, ordered by size of drop so the concentrated segment stands out
Title the chart with the committed escalate-or-hold finding and annotate the single funnel step with the largest adverse deviation
Product Analytics
A weekly dashboard flagged 14 feature-usage metrics as statistically significant movers this week, and leadership wants the one that matters. We test a large number of metrics at once, each metric maps to a downstream KPI (retention, revenue, or support load) with a known impact weight, we retain daily readings within the week so a sustained move can be told from a one-day blip, and we track a per-metric action cost (the effort or spend to respond) and each metric's historical false-alarm rate.

Tell me which single flagged anomaly, if any, is worth acting on rather than routine variation.

feature_metric_review.docx
Text
Put the call in feature_metric_review.docx so I can bring one clear answer back to leadership.

Name the single metric worth acting on this week, or state clearly that none of the 14 clears the bar
Report the multiple-comparison-adjusted significance threshold used and how many of the 14 survive it, as a whole number
Among survivors, name the metric with the largest downstream business impact once each is weighted by its mapped KPI, and state that weighted impact
State whether the top metric's move is sustained across the week's daily readings or driven by a single day, giving the count of days it held outside its normal range
State the recommended action's expected net value after netting the metric's action cost against its weighted impact, so a high-impact but costly alert is separable from a cheap win
flagged_movers_ranked.xlsx
Data
Hand me flagged_movers_ranked.xlsx listing all 14 flagged metrics so I can see where the winner sits.

One row per metric, ranked by how credibly the move stands apart from routine week-to-week variation, measured in standard deviations to two decimal places, with whole-number ranks starting at 1
For each metric show this week's reading and its own recent range, in the metric's native unit to one decimal place, plus its adjusted p-value to three decimal places
Add the mapped KPI (retention, revenue, or support), the KPI-weighted business impact, and a flag for which metrics clear the corrected threshold
Add each metric's within-week persistence as a count of days sustained and its historical false-alarm rate in percent to one decimal place, so a chronically noisy metric is down-weighted
multiplicity_check.py
Code
Provide multiplicity_check.py that applies the multiple-testing correction behind the ranking.

Apply a family-wise or false-discovery correction across all 14 tests and print the corrected threshold to three decimal places
Print the count of metrics surviving correction as a whole number, and the single top surviving metric (or none) with its corrected significance to three decimal places
Print, for the top surviving metric, the persistence check result comparing the within-week daily trajectory against a single-day spike, along with the days-sustained count and its KPI-weighted impact
Print the expected net value for the top metric after subtracting its action cost, in the mapped-KPI unit
movers_impact_chart.pptx
Visual
Include movers_impact_chart.pptx so leadership sees separation, impact, and persistence together.

On a scatter slide plot all 14 metrics with statistical separation in standard deviations on one axis and KPI-weighted business impact on the other, points colored by mapped KPI, with the corrected-significance threshold drawn as a labeled line and the significant-and-high-impact quadrant shaded
On a small-multiples slide show one mini within-week daily-trajectory panel per surviving metric against its normal band, ordered by weighted impact, so sustained moves are separable from single-day spikes
Mark and label the single recommended metric on the scatter slide with its name, its separation in standard deviations, and its weighted impact
Add a findings slide stating the act-or-hold recommendation, the corrected threshold, the count surviving, and the recommended metric's net value after action cost
Title each slide with its finding stated in words
Supply Chain & Logistics
One regional distribution center's order-to-ship cycle time has jumped over the past nine days while the other centers look normal. Peak season is approaching, staffing was recently reshuffled on a known date with a known headcount change, and we capture stage-level timestamps (pick, pack, ship), daily order volume, and a 24-hour SLA target. Planning has a peak-volume forecast for the flagged DC.

Recommend whether we open an operational investigation now or keep monitoring.

dc_cycle_time_alert.docx
Text
Write it up in dc_cycle_time_alert.docx so operations leadership can decide before peak.

Recommend clearly whether this DC's nine-day rise warrants an investigation now or continued monitoring
Quantify the flagged DC's cycle-time increase over the nine days, in hours to one decimal place, and say whether it lines up with the staffing reshuffle date or precedes it
State whether rising order volume alone explains the increase, and name the process stage (pick, pack, or ship) contributing the most added hours
Report the flagged DC's on-time-shipment rate against the 24-hour SLA for the nine days versus its baseline, in percent to one decimal place, and the whole-number count of SLA-breach days
Report the projected cycle time at the forecast peak volume, in hours to one decimal place, and whether it breaches the 24-hour SLA
cycle_time_by_dc.csv
Data
Back it with cycle_time_by_dc.csv so I can see the flagged center against its peers.

One row per DC per day, with order-to-ship cycle time in hours to one decimal place and order volume as a whole-number count, over a comparable window
Include each center's normal cycle-time control range, in hours to one decimal place, so the size of this DC's deviation is unambiguous
Include each center's on-time-shipment rate against the 24-hour SLA over the window, in percent to one decimal place
Flag which days at the flagged DC exceed its normal upper range and total them as a whole-number count of breach days
stage_time_breakdown.csv
Data
Attach stage_time_breakdown.csv so the increase can be traced to a stage.

One row per stage (pick, pack, ship) with mean hours for the flagged nine days versus the prior baseline, each to one decimal place
Include the per-stage change in hours to one decimal place and rank the stages by contribution to the total increase
Add per-stage hours-per-order-volume so a demand-driven rise is separable from a productivity decline
dc_cycle_time_dashboard.html
Visual
Include dc_cycle_time_dashboard.html so leadership can see the flagged DC against peers and trace the cause.

In the main panel draw the flagged DC's daily order-to-ship cycle time across the window in hours to one decimal place, with each day breaching its normal upper control range marked and labeled with its date and value
Overlay peer centers as reference lines, shade the flagged DC's normal control band, mark the staffing-reshuffle date with a vertical line, and draw the 24-hour SLA line
Add a per-stage small-multiple panel (pick, pack, ship) each showing the flagged-window mean versus baseline, ordered by contribution to the increase
Add a per-DC small-multiple row ordered by deviation size so the flagged DC stands out against peers, and label the projected peak-volume cycle time
Add a findings panel stating the investigate-or-monitor recommendation, the nine-day increase in hours, the SLA-breach day count, and the projected peak cycle time
Supply Chain & Logistics
Freight cost per mile on our contracted lanes rose sharply this quarter and finance wants to renegotiate immediately. Fuel surcharges, lane mix, and seasonal capacity all move this number, we know shipped miles and spend per lane so a dollar savings estimate is possible, and carrier concentration varies by lane. We also hold a next-quarter capacity outlook.

Tell me whether the increase reflects a real rate shift or these confounders before finance reopens contracts.

freight_anomaly_check.py
Code
Write freight_anomaly_check.py that runs the analysis end to end and prints the recommendation.

Isolate whether the quarter's cost-per-mile rise is a genuine rate shift after accounting for fuel surcharges, lane mix, and seasonal capacity, and print a clear renegotiate-or-hold recommendation
Print the confounder-adjusted cost per mile in USD to the nearest cent and the share of the increase attributable to the genuine rate shift versus the confounders, as a percentage to one decimal place
Print the estimated annualized dollars at stake from the genuine rate portion, in US dollars to the nearest thousand, using shipped miles
lane_cost_breakdown.xlsx
Data
Have the script also export lane_cost_breakdown.xlsx so finance can see where the increase comes from.

One row per lane, with this quarter's cost per mile against the comparable prior period in USD per mile to the nearest cent, and the change split into fuel, mix, seasonal, and genuine-rate components
Rank lanes by contribution to the total cost-per-mile increase, as an integer rank starting at 1, and name the single lane driving the largest genuine rate increase
Include each lane's shipped miles as a whole-number count so the dollar weight behind each lane's move is visible
Include each lane's carrier concentration and flag the lanes where the genuine-rate portion exceeds the confounder portion, so a rate move tied to a single carrier is distinguishable from a market-wide shift
rate_decomposition_chart.png
Visual
Include rate_decomposition_chart.png showing how the increase breaks down.

Draw a waterfall from prior-period to this-quarter cost per mile with a labeled bar for each of fuel, lane mix, seasonal capacity, and genuine rate, in USD per mile to the nearest cent, and a reference line at the prior-period cost per mile
Make the genuine-rate portion visually distinct from the confounder portions
Add a lane-ranking bar panel ordering lanes by their contribution to the genuine-rate increase, with the single top lane labeled
Annotate the total change and the genuine-rate share as a percentage to one decimal place, and title the chart with the renegotiate-or-hold finding
freight_rate_memo.pdf
Text
Write freight_rate_memo.pdf so finance has the call in writing before reopening contracts.

State the renegotiate-or-hold recommendation and the confounder-adjusted cost-per-mile change, in USD per mile to the nearest cent
Name the single lane driving the largest genuine rate increase and its adjusted cost per mile, in USD per mile to the nearest cent
Give the next-quarter projected cost per mile if the genuine rate holds and the capacity outlook plays out, in USD per mile to the nearest cent
Economics
The latest monthly regional unemployment print for our metro jumped 0.4 points and a local reporter is asking if the labor market is turning. These figures are seasonally noisy and get revised. We hold the labor force and employment levels behind the rate, sector-level employment, comparable state and national rates, and the revision history for recent months.

Decide whether this move is a real deterioration worth flagging to the council or statistical noise.

unemployment_signal_memo.pdf
Text
Put your assessment in unemployment_signal_memo.pdf so I can respond to the council and the reporter.

Judge whether the 0.4-point jump is a real deterioration or falls within this series' normal seasonal and revision noise
State the seasonally aware baseline for this month as a rate in percent to one decimal place, and what it implies about the size of the move in percentage points to one decimal place against the typical month-to-month change
Say whether the rate rose because unemployment increased or because the labor force grew, using the levels behind the rate
Name the sector contributing the most to the change and whether the move is idiosyncratic to this metro versus the state and national rates
metro_unemployment_series.csv
Data
Include metro_unemployment_series.csv with the history behind the call so the numbers are auditable.

One row per month, with the metro's unadjusted and seasonally adjusted unemployment rate each in percent to one decimal place, positioned against comparable prior periods
Include the labor force and employment levels per month as whole-number counts, so a participation-driven move is separable from a job-loss move
Flag which recent values are still subject to revision and include the state and national rate for each month in percent to one decimal place
sector_employment_change.csv
Data
Attach sector_employment_change.csv so the change can be traced to sectors.

One row per sector, with the month-over-month employment change as a whole-number count and its contribution to the rate move in percentage points to one decimal place
Rank sectors by contribution to the change, as an integer rank starting at 1
Flag which sectors moved outside their own normal monthly range
unemployment_trend.pptx
Visual
Send me unemployment_trend.pptx showing the latest print against the series history for the council.

On a time-series slide plot the monthly unemployment rate over at least the last 5 years in percent to one decimal place, with the latest print marked and labeled with its month and value and the seasonally aware baseline for this month also marked
Shade the normal noise band around the trend in percentage points to one decimal place, and overlay the national rate as a reference line so an idiosyncratic metro move is visible
On a sector small-multiples slide show one mini panel per sector of its contribution to the rate move, ordered by contribution, with the top sector labeled
Add a findings slide stating the real-deterioration-or-noise call, the seasonally aware baseline, the move size versus the typical month-to-month change, and whether the move is participation-driven or job-loss-driven
Title each slide with its finding stated in words
Economics
Our tracked basket shows one category with an unusually large month-over-month price increase while headline inflation stayed tame. The head of research wants to know if this is early broad pass-through or an isolated blip. We hold each category's weight in the headline index, subcomponent detail within the flagged category, the full basket's monthly changes, and a record of prior pass-through episodes.

Recommend whether to escalate this category into the forecast narrative.

price_anomaly_assessment.pdf
Text
Deliver it in price_anomaly_assessment.pdf so the head of research can decide how to treat this category.

Recommend whether this category's jump should enter the forecast narrative as early pass-through or be treated as an isolated blip
State how many standard deviations the flagged month-over-month move sits from the category's own history, to one decimal place
Assess whether the move shows up in related categories or stands alone, and name the subcomponent within the category driving most of the increase
Report the flagged category's contribution to the headline this month, in percentage points to two decimal places, using its index weight
category_price_changes.xlsx
Data
Provide category_price_changes.xlsx so we can see this category next to the rest of the basket.

One row per basket category, with month-over-month price change in percent to one decimal place, the category's typical monthly movement in percentage points to one decimal place, and its index weight
Rank all categories by this month's move and include each category's contribution to the headline in percentage points to two decimal places
Flag the categories most correlated with the flagged one so early pass-through is separable from an isolated blip
category_subcomponents.csv
Data
Attach category_subcomponents.csv so the driver inside the category is visible.

One row per subcomponent of the flagged category, with month-over-month change in percent to one decimal place and its within-category weight
Rank subcomponents by contribution to the category's move, as an integer rank starting at 1
Flag whether the move is broad across subcomponents or concentrated in one
price_series_dashboard.html
Visual
Attach price_series_dashboard.html charting the flagged category against the basket.

In the main panel plot the flagged category's month-over-month change against the basket median over the trailing 24 months in percent to one decimal place, with the anomalous month marked and labeled with its date and value and the category's normal-range band shaded
Overlay the most correlated related category so co-movement or its absence is visible
Add a subcomponent small-multiple panel with one mini bar per subcomponent of the flagged category, ordered by contribution, with the top driver labeled
Add a category-ranking panel ordering all basket categories by this month's move with the flagged category highlighted and its headline contribution in percentage points to two decimal places annotated
Add a findings panel stating the escalate-to-narrative-or-blip recommendation, the standard-deviation distance from category history, and the broad-versus-isolated verdict
Policy & Education
A single high school posted a large single-year gain in math proficiency that is drawing praise and a possible board spotlight. Small schools swing a lot year to year and this cohort was small. We hold subject-level and student-subgroup proficiency, yearly cohort sizes, comparable similar-size peer schools, several prior years, the district average, and the school's student mobility rate.

Decide whether this gain is a real program effect worth publicizing and replicating or likely regression to the mean.

proficiency_gain_review.docx
Text
Write it up in proficiency_gain_review.docx so I can advise the board before they spotlight the school.

Decide whether the single-year math gain is a durable program effect worth replicating or likely regression to the mean
Report the single-year gain in percentage points to one decimal place against the school's own multi-year average, and whether it sits inside the typical year-to-year swing band for cohorts this size
Given the cohort size, state the margin around the gain in percentage points to one decimal place and whether the gain is statistically distinguishable from zero
Say whether the gain is broad across subgroups or concentrated in one, and whether elevated student mobility could account for it
school_proficiency_trends.csv
Data
Support it with school_proficiency_trends.csv so the school's swing can be seen against peers.

One row per school per year, with percent proficient to one decimal place and cohort size as a whole-number count, for the flagged school and comparable similar-size peers
Include each school's year-over-year change in percentage points to one decimal place so the flagged swing sits in context
Include the typical single-year swing band for cohorts this size, in percentage points to one decimal place
Include the district average percent proficient per year as a reference column, and the flagged school's rank among the peer set this year as a whole number starting at 1
subgroup_gain_breakdown.csv
Data
Attach subgroup_gain_breakdown.csv so the board can see whether the gain is broad.

One row per student subgroup, with the single-year proficiency change in percentage points to one decimal place and the subgroup's cohort size as a whole-number count
Rank subgroups by contribution to the school-wide gain, as an integer rank starting at 1
Flag which subgroup gains are within normal small-sample volatility versus outside it
proficiency_trend_plot.png
Visual
Include proficiency_trend_plot.png showing the school's swing versus peers.

Plot the school's percent proficient over the multi-year window against similar-size peer schools, axis in percent to one decimal place, with the headline single-year gain marked and labeled in percentage points to one decimal place
Shade the typical year-to-year swing band for small cohorts as a control band so the gain can be judged against normal volatility, and draw the district average as a reference line
Add a subgroup small-multiple panel with one mini bar per subgroup of its single-year change, ordered by contribution, flagging which subgroups are outside normal small-sample volatility
Annotate the margin around the gain given the cohort size, and title the chart with the durable-effect-or-regression-to-mean finding
Policy & Education
A new tip line for our permitting office logged a burst of complaints from one neighborhood over two weeks. Staff are split on whether service quality collapsed there or a single event or local campaign drove the reports. We hold complaint timestamps, complaint types, unique-complainant identifiers, and case resolution times, plus per-neighborhood baselines from the pre-burst period.

Recommend whether to open a formal service review for that area or treat it as a transient cluster.

complaint_cluster_memo.docx
Text
Put the call in complaint_cluster_memo.docx so I can decide whether to stand up a service review.

Recommend whether to open a formal service review for the neighborhood or treat the burst as a transient cluster
Report the flagged neighborhood's complaint count in the two-week window against its baseline count, each as a whole number, and how many standard deviations above baseline that is, to one decimal place
State whether the burst is a broad service decline or a concentrated single-issue spike, using the share from the top complaint type and the ratio of unique complainants to total complaints
Say whether resolution times in the flagged window actually worsened versus baseline, in hours to one decimal place, so a genuine service decline is separable from a reporting surge
complaint_log_by_area.csv
Data
Attach complaint_log_by_area.csv so the neighborhood's burst can be checked against the rest of the district.

One row per neighborhood per week, with complaint counts as whole numbers and the flagged two-week window isolated
Include each neighborhood's baseline weekly complaint count from the pre-burst period as a whole number, and rank neighborhoods by the size of their deviation this window
Include unique complainants per neighborhood-week as a whole number, so a coordinated campaign is separable from broad dissatisfaction
flagged_window_detail.csv
Data
Attach flagged_window_detail.csv breaking down the flagged burst.

One row per complaint type in the flagged window, with its count as a whole number and share of the window total in percent to one decimal place
Include mean resolution time per complaint type in hours to one decimal place against the pre-burst baseline
Flag the single complaint type that dominates the burst
complaint_trend_by_area.pptx
Visual
Add complaint_trend_by_area.pptx plotting the burst against the rest of the district.

On a time-series slide plot weekly complaint counts as whole numbers for the flagged neighborhood against the district over time, with the flagged two-week window shaded and each week above the neighborhood's baseline control band marked and labeled with its count
Shade the neighborhood's baseline control band and draw its baseline weekly count as a reference line
On a complaint-type small-multiples slide show one mini bar per complaint type in the flagged window, ordered by share, with the top type labeled, and overlay unique complainants against total complaints so a campaign signature is visible
On a ranking slide order neighborhoods by their deviation this window with the flagged one highlighted
Add a findings slide stating the open-review-or-transient call, the standard deviations above baseline, the top-type share, the unique-to-total ratio, and whether resolution times worsened
Demographic & Social Science
Our county's latest population estimate shows one age band shrinking far faster than the surrounding trend, and a planning committee wants to redraw service projections around it. Migration and estimation methodology both introduce swings here. We hold the components-of-change detail (births, deaths, net migration) behind the estimate, vintage and methodology flags on the series, the same age band's state-level trajectory, and the county's group-quarters population.

Determine whether this drop is a real demographic shift or an estimation artifact.

population_band_diagnosis.pdf
Text
Write the finding to population_band_diagnosis.pdf so the planning committee knows whether to build projections around it.

Determine whether the age band's steep decline is a real demographic shift or an estimation artifact
Report the flagged band's decline as a percentage to one decimal place against the surrounding-band trend over the same period
Using components of change, say whether net migration or natural change drives the drop, and whether a vintage or methodology change overlaps the decline
State whether the same age band declined at the state level, so a genuine cohort shift is separable from a county-specific estimation quirk
Report the flagged band's share of total county population at the start and end of the period, in percent to one decimal place, so the planning committee can size the service impact
age_band_estimates.csv
Data
Include age_band_estimates.csv so the flagged band can be traced against the others over time.

One row per age band per year, with population as a whole-number count and the flagged band's trajectory set against the surrounding bands
Include a year-over-year percent change column for each band to one decimal place, and the same-band state-level count per year as a whole number
Mark any vintage or methodology change in the estimate series that overlaps the flagged drop
components_of_change.csv
Data
Attach components_of_change.csv so the driver of the drop is auditable.

One row per year for the flagged band, with births, deaths, and net migration each as whole-number counts
Include net migration's share of the year's total change in percent to one decimal place, and flag the group-quarters portion so an institutional-population reclassification is separable from a real move
Rank the years by the size of the net migration swing, as an integer rank starting at 1
age_band_trajectory.html
Visual
Include age_band_trajectory.html contrasting the flagged band with its neighbors and tracing the driver.

In the main panel plot each age band's population across recent years as counts of people, with the flagged band highlighted, the same-band state trajectory overlaid, and any vintage or methodology change marked on the timeline with a vertical line
Shade the surrounding-band trend as a control band so the flagged band's departure is visible, and label the flagged band's deviation from the surrounding-band trend as a percentage to one decimal place
Add a components-of-change small-multiple panel with mini bars for births, deaths, and net migration by year for the flagged band, net-migration years ordered by swing size, with the group-quarters portion flagged
Add a per-band ranking panel ordering bands by year-over-year change with the flagged band highlighted
Add a findings panel stating the real-shift-or-artifact recommendation, the decline versus the surrounding trend, the migration-versus-natural driver, the state-level comparison, and the flagged band's share of county population at start and end
Nonprofit & Grant-making
Across our grantee portfolio, one program's reported cost per participant served came in far above the others this period, prompting a call to freeze its next disbursement. Program models, ramp-up phases, and reporting quirks vary widely across grantees. We hold each grantee's program model, months since launch, participants served, a fixed-versus-variable cost split, an outcomes measure (participants reaching the program goal), and several prior periods.

Tell me whether this grantee is a true outlier warranting review or explainable by these factors before we freeze funds.

grantee_cost_outlier.py
Code
Write grantee_cost_outlier.py that runs the evaluation and prints the recommendation.

Evaluate whether the grantee is a true cost-per-participant outlier or explainable by program model, ramp-up phase, and reporting differences, and print a clear freeze-or-continue recommendation
Print the flagged grantee's raw and ramp-and-model-adjusted cost per participant in USD to the nearest dollar, and how many standard deviations each sits from the peer mean, to one decimal place
Print the flagged grantee's cost per participant reaching the program goal in USD to the nearest dollar, so cost-effectiveness is judged alongside raw unit cost
Print the trend in the flagged grantee's adjusted cost per participant across prior periods, stating whether it is converging toward or diverging from the peer mean, and the projected next-period adjusted cost if the trend holds
portfolio_cost_comparison.csv
Data
Have it also write portfolio_cost_comparison.csv so the board can see where this grantee sits.

One row per grantee, with cost per participant in USD to the nearest dollar, program model, months since launch, and participants served as a whole-number count
Include a fixed-versus-variable cost split per grantee so a high startup cost during ramp is separable from a high ongoing unit cost
Rank grantees by ramp-and-model-adjusted cost per participant, as an integer rank starting at 1, and mark where the flagged grantee lands
Include each grantee's cost per participant reaching the program goal in USD to the nearest dollar and its share reaching the goal in percent to one decimal place, so cost-effectiveness is comparable across the portfolio
cost_vs_outcome_chart.png
Visual
Include cost_vs_outcome_chart.png so cost, results, and trend are seen together.

In panel A plot each grantee with cost per participant on one axis and share reaching the program goal on the other, in USD to the nearest dollar and percent to one decimal place, distinguishing ramp-up grantees from mature ones by marker, drawing the peer-mean cost as a labeled reference line, and marking and labeling the flagged grantee
In panel B draw a per-period small-multiple of the flagged grantee's adjusted cost per participant across prior periods with the peer control band shaded, so convergence toward or divergence from peers is visible
Order the grantees by adjusted cost per participant and annotate the flagged grantee's standard deviations from the peer mean
Title the chart with the freeze-or-continue finding and annotate the peer-mean line value and the flagged grantee's adjusted cost per participant
grantee_freeze_memo.pdf
Text
Summarize the decision in grantee_freeze_memo.pdf for the board.

State a freeze-or-continue verdict for the flagged grantee in one line
Report the flagged grantee's raw and adjusted cost per participant against the portfolio median, all in USD to the nearest dollar
Explain whether program model, ramp-up phase, or reporting differences account for the gap, and whether the trend across prior periods is converging toward peers
State the flagged grantee's cost per participant reaching the goal against the portfolio median in USD to the nearest dollar, so cost-effectiveness backs the call

Root-Cause Analysis
A metric moved and the task is to name the driver, with rival explanations ruled out on evidence.
10 prompts
Product Analytics
Average revenue per paying user fell 12 percent quarter over quarter and finance is asking whether we have a pricing problem. We have per-plan-tier paying-user counts and revenue for both quarters, retention and net revenue retention of the customer cohort present in both quarters, the quarterly downgrade rate of that existing cohort, the new-signup tier mix, and finance also needs a next-quarter forecast under two signup-mix scenarios. The answer decides whether the response is a pricing intervention or simply an artifact of who signed up.

Tell finance the one dominant driver of the ARPU decline: existing customers downgrading or churning at higher price points, or the arithmetic of a large new-user influx landing on the entry tier.

arpu_rootcause.docx
Text
Deliver arpu_rootcause.docx, the written analysis finance asked for.

Name the one dominant driver of the 12 percent ARPU decline and quantify its contribution in USD per paying user to the nearest cent
State plainly whether this is a pricing problem or a composition effect, and what finance should conclude for the forecast
Report net revenue retention for the cohort of customers present in both quarters, in percent to one decimal place, so it is clear whether the existing base is healthy independent of new-signup dilution
Give the ARPU for the existing-customer cohort alone in each quarter, in USD per paying user to the nearest cent
arpu_bridge.xlsx
Data
Attach arpu_bridge.xlsx, a bridge that walks last quarter's ARPU to this quarter's.

Decompose the ARPU change into contributions from existing-customer downgrades, high-tier churn, and new entry-tier signups, each in USD per paying user to the nearest cent
Show per-plan-tier paying-user counts (as whole numbers) for both quarters, one row per tier
Show per-plan-tier revenue (in USD, to the nearest dollar) for both quarters, one row per tier, so each bridge component is traceable
Include a total row reporting overall ARPU for each quarter, in USD per paying user to the nearest cent, so the bridge ties out
Report the share of new signups landing on the entry tier in each quarter, in percent to one decimal place
arpu_decomposition.pptx
Visual
Build arpu_decomposition.pptx, a short deck for the finance review.

On a waterfall slide, walk last quarter's ARPU to this quarter's with one labeled bar for each of the three drivers (existing-customer downgrades, high-tier churn, new entry-tier signups), the axis in USD per paying user to the nearest cent and each bar's contribution labeled to the nearest cent
On a driver-ranking slide, show a horizontal bar chart of the three drivers ordered by absolute USD contribution, largest at top, so the dominant driver is unmistakable
On a trend slide, plot the existing cohort's quarterly downgrade rate over the trailing periods with a reference line at the prior-quarter downgrade rate, annotating the most recent quarter's value in percent to one decimal place
Title the waterfall slide with the committed finding in words (pricing problem versus composition effect)
Close with a findings slide stating the recommendation and citing net revenue retention in percent to one decimal place as its support
arpu_forecast.py
Code
Include arpu_forecast.py projecting next quarter's ARPU under the current and normalized signup mix.

Print next quarter's projected ARPU in USD per paying user to the nearest cent, holding the new-signup mix at its current rate
Print the projected ARPU if the entry-tier signup surge normalizes to the prior-quarter mix, in USD per paying user to the nearest cent, so finance can see the composition effect's reversibility
Print the existing-cohort quarterly downgrade rate, in percent to one decimal place
Product Analytics
New-user activation slid from 41 percent to 33 percent over the last quarter, and the growth team is convinced the redesigned onboarding flow broke something. We have per-channel signup volume, mix share, activation, and week-1 retention of activated users, plus step-level funnel completion for comparable users across both periods. Leadership needs to know where to spend the next fix cycle before more signups leak out.

Tell us whether the activation decline is a real drop in step-completion for comparable users or a shift in the acquisition mix toward lower-intent channels, and name the single driver we should act on.

activation_driver.pdf
Text
Write up the finding in activation_driver.pdf, a short read for the growth lead.

Name the single primary driver behind the drop from 41 to 33 percent and state how much of the 8-percentage-point gap it accounts for, in percentage points rounded to one decimal place
Say explicitly whether the redesigned onboarding flow is exonerated or implicated, and what that means for the next fix cycle
Report the activation rate for a fixed comparable-user segment across both quarters, each in percent to one decimal place
State whether the shift toward lower-intent channels also lowered downstream week-1 retention of activated users, citing the retention gap between the two quarters in percentage points to one decimal place
channel_activation_breakdown.csv
Data
Hand over channel_activation_breakdown.csv showing activation by acquisition channel across the two quarters.

Show quarter-over-quarter signup volume (a count, as a whole number), mix share (percent, to one decimal place), and activation rate (percent, to one decimal place) per acquisition channel, one row per channel
Separate the portion of the overall decline attributable to channel mix from the portion attributable to within-channel completion changes, each in percentage points to one decimal place
Include a row for the blended total across all channels for each quarter, with volume as a whole-number count and activation rate in percent to one decimal place
Add the week-1 retention rate of activated users per channel, in percent to one decimal place
activation_diagnosis.png
Visual
Include activation_diagnosis.png, a single annotated figure the growth lead can read at a glance.

In a waterfall panel, split the 8-percentage-point activation drop into a channel-mix bar and a within-channel completion bar, each labeled in percentage points to one decimal place, summing to 8.0
In a driver-ranking panel, show per-channel contribution to the decline as horizontal bars ordered by magnitude, largest at top, so the single worst channel is obvious
In a step-funnel panel, chart completion at each onboarding step for last quarter versus the prior period holding channel constant, with the completion axis in percent to one decimal place and a reference line at the prior-period rate for the worst step
Annotate the single onboarding step with the largest step-level drop between the two periods, labeled in percentage points to one decimal place
Give the figure a caption stating the committed finding (acquisition mix versus onboarding flow) in words
activation_check.py
Code
Include activation_check.py that reconciles the mix and within-channel split.

Print the channel-mix and within-channel components of the 8-percentage-point decline, each in percentage points to one decimal place
Print the comparable-segment activation rate for each quarter, in percent to one decimal place
Print the number of the onboarding step with the largest comparable-user drop and its size in percentage points to one decimal place
Supply Chain & Logistics
Stockout incidents doubled across the retail replenishment program this quarter and the planning team wants to overhaul the demand forecast. We have per-incident forecast-versus-actual error, supplier lead times, reorder points, actual coverage days, unit lost-sales cost, and current safety-stock parameters, plus a weekly lead-time trend across the quarter, and the team wants a recommended reorder-point adjustment. Rebuilding the forecast is wasted effort if lead times, not forecast error, are driving the stockouts.

Name the dominant driver of the doubled stockouts: forecast error, or lengthening supplier lead times that outran the reorder points.

stockout_driver.docx
Text
Write stockout_driver.docx for the planning team.

Name the dominant driver of the stockout increase and quantify how much it accounts for, as a count of incidents to the nearest whole number
State whether a forecast overhaul is warranted or whether reorder points and lead times are the real issue
Report the split of stockout incidents between forecast error and lead-time lengthening, each as a whole-number count
Recommend the reorder-point adjustment, in days of coverage to one decimal place, needed to absorb the observed lead-time lengthening
stockout_attribution.csv
Data
Provide stockout_attribution.csv attributing each stockout incident to its cause.

For each stockout, show forecast-versus-actual error (in units, to the nearest whole unit) alongside the supplier lead time relative to the reorder point (in days, to the nearest whole day), one row per incident
Tally incidents (as whole-number counts) by whether forecast miss or lead-time lengthening was the binding cause
Include the reorder point and actual coverage days for each incident, in days to the nearest whole day
Add the lost-sales cost of each incident in USD to the nearest dollar, so incidents can be weighted by impact rather than counted equally
stockout_dashboard.html
Visual
Build stockout_dashboard.html, a standalone multi-panel dashboard for the planning review.

In a waterfall panel, decompose the rise in stockout incidents into a forecast-error contribution bar and a lead-time-lengthening contribution bar, each labeled as a whole-number incident count and summing to the total increase
In a driver-ranking panel, rank causes by their share of total lost-sales cost as horizontal bars ordered largest to smallest, each labeled in percent to one decimal place
In a trend panel, plot the weekly supplier lead-time trend against the lead time the reorder points assume, axis in days to the nearest whole day, with a reference line at the assumed coverage and the crossing week marked
Add a header findings panel stating the dominant driver and the recommended reorder-point adjustment in days of coverage to one decimal place
Annotate the count of days lead time exceeded reorder-point coverage over the quarter, as a whole number
reorder_point_fix.py
Code
Include reorder_point_fix.py recomputing reorder points under the new lead-time regime.

Print the recommended reorder point per SKU tier under the new lead-time regime, in units to the nearest whole unit
Print the count of stockouts that would have been prevented had the recommended reorder points been in place, as a whole number
Print the share of total lost-sales cost concentrated in the top decile of SKUs, in percent to one decimal place
Supply Chain & Logistics
The main distribution center's average pick rate per labor hour fell 18 percent after the peak-season ramp and the site lead blames new temporary staff. We have picks per hour by worker tenure, order-line size, travel distance per unit, a weekly temp-productivity trend across the ramp, and labor cost per unit picked. The remedy is very different if the real cause is order profile rather than worker throughput.

Give operations the one primary driver of the pick-rate drop: lower per-worker throughput, or a shift toward smaller, more scattered orders that require more travel per unit.

pickrate_analysis.pdf
Text
Deliver pickrate_analysis.pdf explaining the finding to the site lead.

Name the one primary driver of the 18 percent pick-rate drop and quantify its share of the decline, in percentage points to one decimal place
State whether the new temporary staff are actually the cause or whether order profile is doing the damage
Report the tenured-versus-temporary picks-per-hour gap after the ramp, in picks per hour to one decimal place
State whether the temporary-staff gap is closing week over week, citing the temp picks-per-hour change from their first to their most recent week, in picks per hour to one decimal place
pick_productivity_breakdown.xlsx
Data
Attach pick_productivity_breakdown.xlsx breaking pick rate down by worker tenure and order profile.

Report picks per labor hour (to one decimal place) for tenured versus temporary staff before and after the ramp, one row per tenure group per period
Show order-line size (average lines per order, to one decimal place) and pick-location spread (in meters traveled per unit, to one decimal place) over the same window so travel-per-unit can be compared against throughput
Give the mix-adjusted pick rate holding order profile at the pre-ramp mix, in picks per hour to one decimal place
Include the labor cost per unit picked, in USD to the nearest cent, for each period so the staffing impact is quantified
decompose_pickrate.py
Code
Include decompose_pickrate.py that splits the drop into a throughput effect and an order-profile effect.

Print the pick-rate decline split into worker-throughput and order-profile components, each in percentage points to one decimal place
Print the picks-per-hour figures by tenure group before and after the ramp, to one decimal place
Output the counterfactual pick rate had order profile stayed at the pre-ramp mix, in picks per hour to one decimal place
pickrate_decomposition.pptx
Visual
Build pickrate_decomposition.pptx, a short deck for the operations standup.

On a waterfall slide, split the 18 percent pick-rate drop into a worker-throughput bar and an order-profile bar, each labeled in percentage points to one decimal place and summing to the total decline
On a driver-ranking slide, rank the contributing factors (temp throughput, order-line size, travel per unit) as horizontal bars ordered by contribution, largest at top
On a trend slide, plot weekly picks per hour for tenured and temporary staff across the ramp, axis in picks per hour to one decimal place, with the ramp-start week marked and a reference line at the pre-ramp tenured rate, showing whether the temp line is converging
Overlay weekly average order-line size on a secondary axis of the trend slide so throughput and order profile can be read together
Close with a findings slide stating the recommendation and titling the deck with the committed driver in words
Economics
The metropolitan unemployment rate rose 1.4 points over two quarters while the national rate barely moved, and the local board wants to know what happened here. We have per-industry local employment change, the corresponding national industry trend, and each industry's share of metro employment. The policy response depends on whether local industries actually underperformed or the region is just concentrated in sectors contracting everywhere.

State the single primary driver of the metro unemployment increase: a local-competitive effect (local industries underperforming their national peers), or an industry-mix effect (heavy concentration in sectors contracting nationwide).

metro_unemployment.pdf
Text
Write metro_unemployment.pdf for the local board.

Name the single primary driver of the 1.4-point rise and quantify its contribution in percentage points to one decimal place
State whether the problem is a local-competitive effect or an industry-mix effect the region shares with the nation
Report the metro and national unemployment change over the two quarters, each in percentage points to one decimal place
State whether the local-competitive weakness is broad-based or concentrated, citing the number of industries needed to account for at least half the competitive effect, as a whole number
industry_shift_share.csv
Data
Attach industry_shift_share.csv splitting the change by industry into national, mix, and competitive components.

For each industry, show local employment change (in percent, to one decimal place) alongside the corresponding national trend (in percent, to one decimal place)
Report the three shift-share components per industry: national-growth, industry-mix, and local-competitive, each in percentage points to two decimal places
Include each industry's share of metro employment, as a percentage to one decimal place
Include a total row reconciling the three components to the 1.4-point metro rise, each in percentage points to one decimal place
shift_share_figure.png
Visual
Include shift_share_figure.png, a single annotated figure decomposing the metro unemployment rise.

In a waterfall panel, show the national-growth, industry-mix, and local-competitive components as three labeled bars summing to the 1.4-point rise, each in percentage points to one decimal place
In a driver-ranking panel, order industries by their contribution to the competitive effect as horizontal bars, largest at top, each labeled in percentage points to one decimal place
In a trend panel, plot the single largest contributing industry's local rate against its national peer trend over the two quarters, with a reference line at the national trend so the gap is visible
Annotate the single largest contributing industry with its competitive-effect contribution in percentage points to one decimal place
Give the figure a caption stating the committed driver (competitive versus mix) in words
shift_share.py
Code
Include shift_share.py computing the aggregate components and a robustness check.

Print the three aggregate shift-share components, each in percentage points to one decimal place, summing to the metro rise
Print the single industry with the largest local-competitive contribution and its value in percentage points to one decimal place
Print whether excluding that top industry flips the dominant driver from competitive to mix, as yes or no, with the recomputed components
Economics
A regional consumer price index accelerated from 2.1 to 3.6 percent year over year and the analysts disagree on whether it is broad-based. We have each item category's price change, its expenditure weight, its own prior-year trend, and a classification of categories as sticky or volatile. How the board characterizes the inflation, and whether it reads as persistent, depends on whether it is widespread or concentrated in a few heavily weighted items.

Name the one dominant driver of the CPI acceleration: genuine broad price increases across categories, or a small number of heavily weighted categories moving while the rest stayed flat.

cpi_rootcause.docx
Text
Deliver cpi_rootcause.docx explaining whether the acceleration is broad-based.

Name the one dominant driver of the move from 2.1 to 3.6 percent and quantify how much of the 1.5-percentage-point acceleration it explains, in percentage points to one decimal place
State whether inflation is broad-based or concentrated, and how the board should characterize it
Report the number of categories that together account for at least half the acceleration, as a whole number
State whether the acceleration is concentrated in volatile categories (likely transitory) or sticky categories (likely persistent), citing the sticky-category share of the acceleration in percentage points to one decimal place
category_contribution.xlsx
Data
Attach category_contribution.xlsx showing each item category's contribution to the headline change.

Show each category's price change (in percent, to one decimal place) and its expenditure-weighted contribution to the acceleration (in percentage points, to two decimal places), one row per category
Rank categories by contribution, as an integer rank starting at 1, so it is clear whether a few dominate or the rise is spread across many
Include each category's expenditure weight, as a percentage to one decimal place
Add a diffusion figure: the share of categories with price growth above their own prior-year trend, in percent to one decimal place
cpi_dashboard.html
Visual
Build cpi_dashboard.html, a standalone multi-panel dashboard for the board briefing.

In a waterfall panel, chart each category's weighted contribution as a step from the 2.1 percent prior rate to the 3.6 percent current rate, axis in percent to one decimal place, labeling the single largest step with its contribution in percentage points to two decimal places
In a driver-ranking panel, show categories as horizontal bars ordered by contribution, largest at top, so concentration versus breadth is obvious at a glance
In a trend panel, plot the top contributing category's price growth against its own prior-year trend with a reference line at that trend, annotating the current-year value in percent to one decimal place
Add a header findings panel stating whether the acceleration is broad-based or concentrated and the sticky-versus-volatile split in percentage points to one decimal place
Give the dashboard a title stating the committed driver in words
diffusion_check.py
Code
Include diffusion_check.py testing breadth and robustness of the acceleration.

Print the number of categories accounting for at least half the acceleration, as a whole number
Print the trimmed-mean acceleration excluding the top and bottom decile of category contributions, in percentage points to one decimal place, and whether it still reads as broad-based
Print the sticky-category versus volatile-category split of the acceleration, each in percentage points to one decimal place
Policy & Education
A district's four-year graduation rate fell from 88 to 81 percent and the superintendent is preparing to replace the instructional program. We have graduation rates matched on entry timing and prior enrollment, late-transfer counts by feeder program, subgroup breakouts, a multi-year late-transfer-share trend, and next year's incoming pipeline. Replacing instruction is misdirected if the decline traces to who is in the cohort rather than how comparable students fared.

Name the single main driver of the graduation decline: lower graduation among comparable students, or a change in cohort composition as feeder programs sent in more late transfers.

grad_rate_rootcause.pdf
Text
Write grad_rate_rootcause.pdf for the superintendent.

Name the single main driver of the drop from 88 to 81 percent and quantify its contribution in percentage points to one decimal place
State whether replacing the instructional program is justified or whether the decline is a composition effect
Report the composition-adjusted graduation rate for the later cohort, in percent to one decimal place
Report the graduation rate of late-transfer students versus continuously enrolled students in the later cohort, each in percent to one decimal place, so the size of the composition penalty is clear
cohort_composition.csv
Data
Attach cohort_composition.csv comparing cohort makeup and outcomes across the two years.

Show graduation rates (in percent, to one decimal place) for students matched on entry timing and prior enrollment across the two cohorts
Report the share of late transfers entering from feeder programs (in percent, to one decimal place) and their graduation rate (in percent, to one decimal place)
Include headcounts of matched and unmatched students per cohort, as whole numbers
Break out each cohort's graduation rate by subgroup, in percent to one decimal place, so any within-group decline can be located
grad_decomposition.pptx
Visual
Build grad_decomposition.pptx, a short deck for the board meeting.

On a waterfall slide, split the 7-point drop from 88 to 81 percent into a cohort-composition bar and a within-group performance bar, each labeled in percentage points to one decimal place and summing to 7.0
On a driver-ranking slide, rank feeder programs by their contribution to the composition effect as horizontal bars, largest at top, each labeled in percentage points to one decimal place
On a trend slide, plot the late-transfer share by cohort year with a reference line at the earlier cohort's share, annotating the later cohort's value in percent to one decimal place
Title the waterfall slide with the committed driver (composition versus performance) in words
Close with a findings slide stating the recommendation and whether replacing the instructional program is justified
grad_projection.py
Code
Include grad_projection.py decomposing the drop and projecting next year.

Print the composition and within-group components of the 7-point drop, each in percentage points to one decimal place
Print the projected graduation rate for next year's cohort given the incoming late-transfer share in the pipeline, in percent to one decimal place
Print the counterfactual later-cohort rate had the transfer mix matched the earlier cohort, in percent to one decimal place
Policy & Education
Enrollment in a state workforce-training subsidy fell 30 percent after a program-year boundary and the agency assumes outreach spending caused it. We have applicant volume, approval-eligibility rates, the income-threshold value before and after the boundary, the outreach-spend timeline, and take-up among the still-eligible. The corrective action differs entirely if a quiet eligibility tightening, not outreach, cut the qualifying population.

Name the dominant driver of the enrollment drop: reduced outreach, or a tightening of the income-eligibility threshold that removed a large slice of the previously qualifying population.

enrollment_rootcause.pdf
Text
Write enrollment_rootcause.pdf for the agency.

Name the dominant driver of the 30 percent enrollment decline and quantify its contribution in percentage points to one decimal place
State whether outreach spending or the eligibility-threshold change is responsible, and what the agency should fix
Report the enrollment change attributable to the eligibility tightening versus outreach, each in percentage points to one decimal place
Report whether take-up among still-eligible applicants held steady, citing the take-up rate before and after the boundary in percent to one decimal place
eligibility_impact.csv
Data
Attach eligibility_impact.csv showing applicants and eligibility outcomes across the program-year boundary.

Show application volume (a count, as a whole number) and approval-eligibility rates (in percent, to one decimal place) before and after the boundary
Estimate how many previously qualifying applicants the new income threshold excluded, as a count to the nearest whole applicant
Include the income-threshold value before and after the boundary, in USD to the nearest dollar
Report the still-eligible take-up rate before and after the boundary, in percent to one decimal place
enrollment_diagnosis.png
Visual
Include enrollment_diagnosis.png, a single annotated figure for the agency review.

In a waterfall panel, split the 30 percent enrollment decline into an eligibility-exclusion bar and a residual outreach-and-take-up bar, each labeled in percentage points to one decimal place and summing to 30.0
In a driver-ranking panel, rank the contributing factors (income-threshold exclusion, outreach reduction, take-up change) as horizontal bars ordered by contribution, largest at top
In a trend panel, plot outreach spend (left axis in USD to the nearest thousand) and enrollment (right axis as a whole-number count) on a shared timeline with the program-year boundary marked by a reference line, showing whether enrollment broke at the boundary or tracked spend
Annotate the percentage drop in enrollment at the boundary, to one decimal place
Give the figure a caption stating the committed driver (eligibility tightening versus outreach) in words
eligibility_recompute.py
Code
Include eligibility_recompute.py isolating the exclusion effect from the residual.

Print the enrollment change decomposed into the eligibility-exclusion effect and the residual outreach-and-take-up effect, each in percentage points to one decimal place
Print the count of applicants excluded solely by the new income threshold, as a whole number
Print the counterfactual enrollment had the income threshold been unchanged, as a count to the nearest whole number
Demographic & Social Science
A fast-growing county's annual population growth slowed from 2.3 to 0.6 percent and regional planners are debating whether people are leaving. We have births, deaths, and net migration by year, the median-age and crude-death-rate trend, and base population by year. Infrastructure and housing plans hinge on whether migration reversed or the resident population simply aged into negative natural increase.

Name the single primary driver of the growth slowdown: falling net in-migration, or the natural-increase component turning negative as the resident population aged.

county_growth.pdf
Text
Write county_growth.pdf for the regional planners.

Name the single primary driver of the slowdown from 2.3 to 0.6 percent and quantify its share in percentage points to one decimal place
State whether people are actually leaving or whether natural increase is the culprit
Report net migration and natural increase for the most recent year, each as a whole-number count of people
State whether natural increase turned negative and in which year, citing that year's births-minus-deaths as a whole-number count
components_of_change.csv
Data
Attach components_of_change.csv breaking annual growth into births, deaths, and net migration.

Show births, deaths, and net migration for each year (each as a count, to the nearest whole person) with their contribution to the growth rate (in percentage points, to one decimal place)
Separate the slowdown attributable to net migration from the slowdown attributable to natural increase, each in percentage points to one decimal place
Include total population at the start of each year, as a whole-number count of people
Report the crude death rate per year, in deaths per 1,000 residents to one decimal place, so the aging signal is visible
components_dashboard.html
Visual
Build components_dashboard.html, a standalone multi-panel dashboard for the planners.

In a waterfall panel, decompose the 1.7-point slowdown into a net-migration bar and a natural-increase bar, each labeled in percentage points to one decimal place and summing to the total slowdown
In a driver-ranking panel, rank the components of change (births, deaths, net migration) by their contribution to the slowdown as horizontal bars, largest at top
In a trend panel, plot net migration and natural increase by year with a zero reference line, marking the year natural increase turned negative and the year growth reached 0.6 percent
Add a header findings panel stating which component drove the slowdown and whether people are leaving
Give the dashboard a title stating the committed driver in words
growth_projection.py
Code
Include growth_projection.py decomposing the slowdown and projecting forward.

Print the migration and natural-increase components of the slowdown, each in percentage points to one decimal place
Print the projected growth rate three years out if the current natural-increase and migration trends continue, in percent to one decimal place
Print the counterfactual growth rate for the latest year had net migration held at its earliest-year level, in percent to one decimal place
Nonprofit & Grant-making
A national charity's year-over-year donor retention fell from 62 to 51 percent and the development director wants to invest in a re-engagement campaign. We have retention by donor acquisition cohort, donor counts, average gift value per cohort, revenue retained per cohort, and the size of last year's one-time event and emergency-appeal surge. That campaign is misaimed if the drop is really last year's one-time donors lapsing on schedule.

Name the single primary driver of the retention decline: higher lapse among established donors, or the prior year's surge of one-time event and emergency-appeal donors who were never likely to give again.

donor_retention.pdf
Text
Write donor_retention.pdf for the development director.

Name the single primary driver of the drop from 62 to 51 percent and quantify its contribution in percentage points to one decimal place
State whether a re-engagement campaign is warranted or whether the decline is an expected lapse of one-time donors
Report retention for established donors alone, in percent to one decimal place, with the one-time surge removed
Report revenue retention (dollars retained versus prior-year dollars) for established donors, in percent to one decimal place, so the decision weights donor value and not just headcount
retention_by_donor_type.csv
Data
Attach retention_by_donor_type.csv comparing retention across donor acquisition cohorts.

Show retention rates (in percent, to one decimal place) for established donors versus prior-year event and emergency-appeal acquirers
Report the size of the one-time donor surge (as a count of donors, to the nearest whole number) and its effect on the blended retention number (in percentage points, to one decimal place)
Include one row per acquisition cohort with prior-year donor count, retained count, and retention rate in percent to one decimal place
Add average gift value per cohort, in USD to the nearest dollar, so the value at stake per cohort is visible
retention_decomposition.pptx
Visual
Put together retention_decomposition.pptx for the board.

On a waterfall slide, split the 11-point drop from 62 to 51 percent into an established-donor-lapse bar and a one-time-donor-mix bar, each labeled in percentage points to one decimal place and summing to 11.0
On a driver-ranking slide, rank acquisition cohorts by their contribution to the retention decline as horizontal bars, largest at top, each labeled in percentage points to one decimal place
On a trend slide, plot the blended retention rate over the trailing years with a reference line at the pre-surge level, annotating the projected steady-state blended retention once the one-time surge cycles out in percent to one decimal place
Include a slide contrasting retention rates by donor type, in percent to one decimal place
Title the deck with the committed driver in words and close with a findings slide stating the recommendation and citing established-donor revenue retention in percent to one decimal place
retention_projection.py
Code
Include retention_projection.py decomposing the drop and projecting next year.

Print the established-lapse and one-time-mix components of the 11-point drop, each in percentage points to one decimal place
Print the projected blended retention next year assuming no re-acquisition surge, in percent to one decimal place
Print the established-donor count and the one-time-donor count for the prior year, each as a whole number

Experiment & Causal Analysis
The conclusion depends on a causal claim, from a designed test or from observational data with confounders.
10 prompts
Product Analytics
A two-week A/B test on a redesigned onboarding checklist shows a 4.1 percentage point lift in day-30 retention at p=0.03, but retention naturally decays across the first month and the treatment cohort skews toward users who signed up later in the test window. Signup-week cohorts, a user-segment split (brand-new versus reactivated users), and a pre-launch placebo week (before the checklist shipped, where the true effect is zero) are all available, and per-cohort sample sizes support a 95 percent confidence interval and a minimum-detectable-effect on the adjusted lift. The checklist adds about two seconds to first-session load and carries an engineering maintenance cost the team pegs at needing at least a 2.0 percentage point durable retention lift to justify. Leadership needs a ship-or-hold call before committing engineering to a full rollout.

Tell us whether to ship the redesigned onboarding checklist to all users.

ship_decision.pdf
Text
Write up your ship-or-hold call in ship_decision.pdf.

State the final ship or hold decision and the day-30 retention lift you expect at full rollout, in percentage points to one decimal place, after netting out the natural first-month decay and the later-signup mix, and report whether that cohort-adjusted lift stays statistically significant, giving the adjusted p-value to two decimal places and its 95 percent confidence interval in percentage points
Quantify how many of the raw 4.1 percentage points are confounding from later-signup skew and decay rather than a real treatment effect, to one decimal place
State the placebo-check result on the pre-launch week where the true effect is zero, and say whether it supports the design's validity
State whether the lift concentrates in brand-new users versus reactivated users, giving each segment's adjusted lift, and whether that changes the rollout call
Weigh the added first-session load time and the checklist's engineering maintenance cost against the retention gain, and give the net recommendation against the 2.0 percentage point bar
retention_by_cohort.csv
Data
Include retention_by_cohort.csv, day-30 retention broken out by signup-week cohort.

One row per signup-week cohort, with treatment and control day-30 retention as percentages to one decimal place
A column for the cohort-adjusted lift after treatment and control are put on equal footing for cohort composition, in percentage points to one decimal place
Treatment and control user counts per cohort, as whole numbers
Include a final summary row giving the blended unadjusted lift and the composition-adjusted lift side by side, both in percentage points to one decimal place
checklist_effect_panel.png
Visual
Attach checklist_effect_panel.png, a multi-panel effect-and-robustness figure.

Lead with an effect-size plot showing the cohort-adjusted day-30 retention lift as a point with its 95 percent confidence interval in percentage points, and draw a labeled vertical reference line at the 2.0 percentage point engineering-cost bar so it is visible whether the interval clears it
Add a parallel-trends panel plotting treatment and control day-30 retention across the signup-week cohorts, with the pre-launch placebo week marked and annotated to show its near-zero baseline gap
Add a per-segment small-multiple contrasting the adjusted lift for brand-new versus reactivated users, each drawn as a point with its confidence interval
Add a decomposition strip showing the raw 4.1 point lift, the confounding share removed, and the adjusted lift as bars ordered from largest to smallest
Title the figure with the ship-or-hold finding and the adjusted lift stated in words
adjustment_check.py
Code
Provide adjustment_check.py that runs the cohort adjustment, placebo, and significance test.

Print the cohort-adjusted lift and its p-value a manager can read without rerunning the script
Compute and print the placebo estimate on the pre-launch window, which should be near zero
Print the confounding share, raw lift minus adjusted lift, in percentage points to one decimal place
Print a ship or hold flag based on whether the adjusted lift is positive, significant, and clears the 2.0 percentage point engineering-cost threshold
Product Analytics
An in-app referral reward given to a random 50 percent of active users lifted referrals per user by 22 percent, but weekly treated referrals were already declining by the final week of the quarter. Weekly per-user referral data for both arms spans the full quarter, referrer segments (heavy versus occasional referrers) are tagged, downstream data shows whether referred users actually activate (referral quality), and the reward pays out about 8 dollars per referral. Weekly sample sizes support a confidence interval on the final-week lift and a projected steady-state lift from the fitted decay. Leadership wants to know whether the reward is a durable driver or a fading novelty spike before making it permanent.

Tell us whether to make the referral reward permanent.

referral_reward_call.docx
Text
Lay out your recommendation in referral_reward_call.docx.

Give a permanent-or-sunset recommendation with the steady-state referral lift you expect once novelty wears off, as a percentage to one decimal place, and report the final-week treated-versus-control lift as a percentage to one decimal place with its 95 percent confidence interval and whether it is still significantly above zero
State the weekly decay slope in referrals per user per week to two decimal places, and whether the decline is statistically distinguishable from flat
Assess referral quality by giving the activation rate of referred users for the treated arm versus organic referrals, each to one decimal place
Net the 8 dollar per-referral payout against the incremental referrals to state the cost per net-new activated user, and whether it clears the payback bar
Report whether the effect concentrates among heavy referrers or extends to occasional referrers, giving each segment's lift
referral_dashboard.html
Visual
Build referral_dashboard.html, a standalone multi-panel dashboard of the referral experiment.

Panel one: an effect-over-time chart of weekly referrals per user for treated versus control across the full quarter, with a fitted decay trend line through the treated series, the reward launch week shaded, and the week treated crosses back to the control level annotated
Panel two: an effect-size panel showing the final-week lift as a point with its 95 percent confidence interval and a labeled reference line at zero, plus the projected steady-state lift point beside it so the novelty-versus-durable gap is visible
Panel three: a small-multiple splitting the weekly trajectory for heavy versus occasional referrers, each as its own mini time series
Panel four: a referral-quality-and-cost panel comparing the activation rate of referred users for the treated arm versus organic referrals, and showing the 8 dollar payout netted to cost per net-new activated user against the payback bar
A headline findings banner stating the permanent-or-sunset call and the steady-state lift in words
weekly_referral_metrics.csv
Data
Attach weekly_referral_metrics.csv with the underlying weekly figures.

One row per week with referrals per user for treated and control, each to two decimal places
The weekly lift in percentage points to one decimal place for each week
Active-user counts per arm per week, as whole numbers
A column for cumulative incremental referrals to date, as whole numbers
The activation rate of referred users per arm per week, in percent to one decimal place
referral_decay_model.py
Code
Provide referral_decay_model.py fitting the decay and stating the call.

Fit a decay curve to the treated weekly series and print the estimated steady-state lift and the decay half-life in weeks
Print the final-week lift and its p-value
Print the cost per net-new activated user in USD to the nearest dollar
Print a permanent or sunset flag based on the steady-state lift clearing the payback bar
Supply Chain & Logistics
After moving a set of lanes to a new carrier, on-time delivery on those lanes rose from 88 to 93 percent while retained lanes held steady, but the switched lanes were disproportionately short-haul urban routes already trending upward beforehand. Lane-level monthly on-time data spans a pre-period and a post-period with haul-type and urban/rural flags, per-lane freight cost, transit time, and damage-claim rate, and the new carrier states a capacity ceiling that limits how many more lanes it can absorb. Lane counts support a confidence interval on the difference-in-differences estimate and a placebo difference-in-differences on a pre-switch window. Expansion is only justified if the trend-adjusted on-time gain is at least 2.0 percentage points with no increase in cost per lane.

Determine whether to keep the switched lanes on the new carrier and how far to expand the switch.

carrier_switch_analysis.py
Code
Deliver carrier_switch_analysis.py, the script that runs the comparison and states the recommendation.

Print the on-time effect of the switch net of the switched lanes' pre-existing upward trend, as a difference-in-differences versus retained lanes, in percentage points to one decimal place, with its 95 percent confidence interval
Print a switched-versus-retained on-time comparison for the pre and post periods a manager can read without rerunning anything
Print the placebo check applying the same difference-in-differences to a pre-switch window where no switch occurred, and confirm it is near zero
Print the counts of switched and retained lanes, each as a whole number
Print an expand flag based on the trend-adjusted gain clearing 2.0 percentage points with no cost increase
lane_ontime_summary.csv
Data
Also produce lane_ontime_summary.csv with the underlying lane-level figures.

One row per lane per period with on-time rate in percent to one decimal place, haul type, urban/rural flag, freight cost per lane, transit time, and damage rate
A pre-period and a post-period on-time-rate column per lane, each in percent to one decimal place
The trend-adjusted on-time improvement attributable to the new carrier, in percentage points to one decimal place
The trend-adjusted gain broken out by haul type, short-haul urban versus long-haul, so the heterogeneity is visible
The per-lane change in freight cost and damage rate after the switch
carrier_switch_readout.pptx
Visual
Prepare carrier_switch_readout.pptx, a leadership readout of the switch.

A parallel-trends slide plotting switched versus retained on-time across the pre and post monthly points, with the switch month marked, so pre-switch parallelism is visible
An effect-size slide showing the difference-in-differences on-time gain as a point with its 95 percent confidence interval and a labeled reference line at the 2.0 percentage point expansion bar
A robustness slide showing the placebo difference-in-differences on the pre-switch window near zero alongside the headline estimate
A heterogeneity slide with a small-multiple of the trend-adjusted gain by haul type, short-haul urban versus long-haul, ordered by gain
A findings slide stating the keep-and-expand call, how many additional lanes to switch under the capacity ceiling, and the cost and damage-rate second axis
carrier_switch_recommendation.pdf
Text
Write carrier_switch_recommendation.pdf so the manager can decide.

State whether to keep the switched lanes on the new carrier and how many additional lanes to switch given the capacity ceiling
Report the trend-adjusted on-time gain attributable to the switch, in percentage points to one decimal place
Explain why the raw 88 to 93 percent improvement overstates the carrier's effect, quantifying the trend's share
State whether the gain holds for long-haul lanes or is confined to short-haul urban, and what that implies for expansion scope
State the cost per lane change and whether expansion clears the cost-neutral bar
Supply Chain & Logistics
A supplier scorecard program for top-tier vendors coincided with a 30 percent year-over-year drop in defect rates, and procurement credits the scorecards. Because tier assignment is based on prior performance, the best vendors were already on an improving path, so regression to the mean may explain the gain. Per-vendor quarterly defect rates cover several pre-program quarters, tier assignment is recorded, a set of near-miss vendors just below the tier cutoff serves as a comparison, per-vendor purchase volume is available, and the program costs a known amount per vendor to administer against a known cost per defect. Vendor counts support a confidence interval on the difference-in-differences and a parallel pre-trend test. Expansion is only justified if the adjusted causal reduction is at least 5 percent with positive program ROI.

Tell us whether to expand the supplier scorecard program to more vendors.

scorecard_effect.docx
Text
Write it up in scorecard_effect.docx.

Give an expand-or-hold call stating the defect reduction genuinely caused by the scorecards versus what the top tier would have reached anyway, both as percentages to one decimal place
Give the counterfactual defect rate the top tier would have reached without the program, in percent to one decimal place
Assess whether regression to the mean among already-strong vendors explains the 30 percent drop, quantifying the reversion share
Report the program ROI, the administrative cost per vendor against the defect-cost savings from the adjusted reduction, and whether it is positive
State whether the effect differs between mid-tier and top-tier vendors and what that implies for who to expand to next
scorecard_effect_panel.png
Visual
Include scorecard_effect_panel.png, a multi-panel effect-and-robustness figure.

Lead with an effect-size plot of the difference-in-differences defect reduction as a point with its 95 percent confidence interval in percentage points, with a labeled reference line at the 5 percent expansion threshold
Add a parallel-trends panel of defect-rate paths for scorecard versus near-cutoff comparison vendors before and after launch, with the launch quarter marked and the pre-existing trend slope labeled in percentage points per quarter
Add a decomposition strip splitting the raw 30 percent drop into the regression-to-the-mean reversion share and the genuine program effect, drawn as ordered bars
Add a per-tier small-multiple contrasting the adjusted effect for mid-tier versus top-tier vendors, each as a point with its confidence interval
Title the figure with the expand-or-hold finding, the adjusted causal reduction, and whether ROI is positive stated in words
scorecard_did.py
Code
Provide scorecard_did.py estimating the program effect against the counterfactual.

Estimate the scorecard causal effect using a difference-in-differences against the near-cutoff comparison vendors, in percentage points to one decimal place, with its confidence interval
Print the regression-to-the-mean adjusted effect as a robustness cross-check
Print the counterfactual defect rate for scorecard vendors absent the program, in percent to one decimal place
Print the pre-trend test result confirming parallel pre-program paths
Print an expand or hold flag based on the adjusted effect clearing 5 percent with positive ROI
vendor_defect_panel.csv
Data
Attach vendor_defect_panel.csv with the vendor-quarter detail.

One row per vendor per quarter with defect rate in percent to one decimal place, tier, scorecard flag, and purchase volume
A pre-program and a post-program mean defect-rate column per vendor
The adjusted per-vendor effect for scorecard vendors, in percentage points to one decimal place
Vendor counts in the scorecard group and the comparison group, as whole numbers
Economics
A region raised its minimum wage while a neighboring region held flat, and low-wage employment grew 1.2 percent in the treated region versus 0.4 percent next door. The two regions had different pre-trends and were hit unevenly by a manufacturing boom, complicating the comparison. Monthly low-wage employment by region spans several pre and post years, a wage-threshold definition marks the low-wage segment, a high-wage employment series unaffected by the policy is available as a placebo, and hours-worked, average-wage, and sector (food service versus manufacturing) series let the employment call be checked on a second axis. The monthly series support a confidence interval on the difference-in-differences and a pre-trend test.

Decide whether the minimum wage increase caused a change in low-wage employment.

min_wage_effect.pdf
Text
Present your conclusion in min_wage_effect.pdf.

Give a clear verdict on whether the wage increase changed low-wage employment and in which direction, reporting the difference-in-differences estimate of the policy effect in percentage points to one decimal place with its 95 percent confidence interval
Assess whether the divergent pre-trends and the manufacturing boom account for the 1.2 versus 0.4 percent gap, quantifying the pre-trend contribution
Report the placebo difference-in-differences on high-wage employment unaffected by the policy, which should be near zero, and what it implies
Report the effect on hours worked and on the average low-wage wage as a second axis, so the employment call is not read in isolation
State whether the effect differs between the food-service and manufacturing sectors, giving each sector's estimate
employment_extract.py
Code
Include employment_extract.py, the script that assembles the employment series and runs the estimate.

Assemble low-wage employment by region and period aligned to the pre and post window, restricting to the low-wage segment via an explicit wage-threshold filter stated in the code
Pull the neighboring-region comparison series and the high-wage placebo series
Print the difference-in-differences estimate with its confidence interval and the pre-trend test statistic a reader can see without rerunning
Print the sector-split estimates for food service versus manufacturing
employment_panel.csv
Data
Output employment_panel.csv, the assembled two-region panel.

One row per region per period with low-wage employment as a headcount to the nearest whole number, a treatment flag, and a period flag marking pre or post
The treated-versus-comparison gap after the regions' pre-policy trajectories are lined up, in percentage points to one decimal place
Hours-worked and average-wage columns per region-period
The high-wage employment headcount per region-period for the placebo
employment_dashboard.html
Visual
Attach employment_dashboard.html, a standalone multi-panel dashboard of the wage-policy analysis.

Panel one: a parallel-trends line plotting low-wage employment paths for the treated and comparison regions with the policy date marked, so pre-policy parallelism or its absence is visible
Panel two: an effect-size panel showing the difference-in-differences estimate as a point with its 95 percent confidence interval and a labeled reference line at zero
Panel three: a placebo panel overlaying the high-wage employment difference-in-differences near zero to show it does not jump at the policy date
Panel four: a second-axis panel showing the hours-worked and average-wage effects, plus a small-multiple of the food-service versus manufacturing sector split
A headline findings banner stating the causal verdict and the difference-in-differences estimate in words
Economics
A cash transfer pilot enrolled households below a sharp income cutoff, and enrolled households now show higher consumption than those just above the line. Households near the threshold may have misreported income to qualify, which threatens the comparison right where it matters most. Household consumption and income (the running variable) are recorded in narrow bands on either side of the cutoff, covariates (household size, prior employment) allow a smoothness check, and program cost per household is known. Baseline poverty tertiles (bottom, middle, and top thirds of pre-transfer consumption) are tagged so the discontinuity can be estimated within each subgroup, and two child outcomes are tracked: school attendance and enrollment-persistence into the next grade. Band and subgroup counts support a 95 percent confidence interval on the discontinuity and on each subgroup and second-outcome estimate, a McCrary density test, and estimates under narrow, baseline, wide, and donut bandwidths.

Assess whether the cash transfers had a genuine causal effect on household consumption.

transfer_impact.pdf
Text
Record your decision in transfer_impact.pdf.

Give a verdict on whether the transfers raised consumption, focused on households near the eligibility cutoff, reporting the regression-discontinuity consumption effect at the cutoff in USD to the nearest whole dollar with its 95 percent confidence interval
Assess whether income misreporting or bunching around the threshold undermines the comparison, citing the McCrary density-test p-value to two decimal places, and separately state the covariate-smoothness result for household size and for prior employment across the cutoff
Report robustness by giving the estimate under the narrow, baseline, and wide bandwidths, and the donut estimate that drops households immediately at the threshold, and say whether the conclusion survives all four
Split the effect by baseline-poverty tertile, giving the consumption effect at the cutoff for the bottom, middle, and top tertile each in USD to the nearest whole dollar, and name which tertile gains most
Report the effect on child school attendance and on child school enrollment-persistence as two second outcomes, each in percentage points to one decimal place with its confidence interval, plus the program cost per household and the consumption gain per dollar transferred
rd_estimates.csv
Data
Provide rd_estimates.csv carrying the computed discontinuity results.

A bandwidth-robustness block with one row per bandwidth (narrow, baseline, wide, donut) giving the estimated consumption jump at the cutoff and its 95 percent confidence interval, in USD to the nearest whole dollar
One row per baseline-poverty tertile (bottom, middle, top) with that tertile's consumption effect at the cutoff and its 95 percent confidence interval in USD to the nearest whole dollar
The McCrary density-test statistic and p-value, and the covariate-smoothness p-values for household size and for prior employment, each to two decimal places
One row per second outcome (child school attendance, child school enrollment-persistence) with its effect in percentage points to one decimal place and its 95 percent confidence interval
A band-level block with one row per narrow income band giving mean consumption in USD to the nearest whole dollar, the household count as a whole number, and an eligible or ineligible flag, for bands just above and just below the cutoff
rd_consumption_panel.png
Visual
Include rd_consumption_panel.png, a multi-panel regression-discontinuity figure.

Lead with the RD scatter of mean consumption by income band on either side of the cutoff with a fitted line on each side, the size of the jump at the cutoff annotated with its confidence interval in USD to the nearest whole dollar, and the eligibility cutoff drawn as a labeled vertical line
Add a McCrary density panel showing a histogram of household density in the running variable with the density-test p-value annotated, to reveal any bunching just below the cutoff
Add a bandwidth-robustness small-multiple plotting the estimate under narrow, baseline, wide, and donut bandwidths as points with confidence intervals, ordered by bandwidth, with a labeled reference line at zero
Add a per-subgroup small-multiple contrasting the consumption effect at the cutoff for the bottom, middle, and top baseline-poverty tertile, each drawn as a point with its confidence interval
Title the figure with the causal verdict and the consumption effect at the cutoff stated in words, and add a second-outcome strip showing the child school attendance and enrollment-persistence effects each as a point with its confidence interval
rd_estimation.py
Code
Provide rd_estimation.py running the regression-discontinuity and robustness checks.

Estimate the regression-discontinuity consumption effect at the cutoff under the baseline bandwidth and print it with its 95 percent confidence interval a reader can see without rerunning
Run and print the McCrary density-test statistic and p-value for manipulation at the threshold, and print the covariate-smoothness p-values for household size and prior employment
Print the estimate under the narrow, wide, and donut bandwidths for robustness
Print the per-tertile consumption effect for the three baseline-poverty subgroups and the two second-outcome effects, child school attendance and enrollment-persistence
Print a causal verdict flag based on the estimate being significant, the density test passing, and the conclusion surviving the donut and narrow-bandwidth checks
Policy & Education
Free after-school tutoring at 15 schools produced math score gains 6 points above the district average, but participation was voluntary and the adopting schools had more engaged parents to begin with. Per-school pre and post math scores, a parental-engagement index, a comparison set of non-adopting schools, attendance as a second outcome, per-school program cost, and grade-band tags (elementary versus middle school) are all available. School counts support a confidence interval on the matched effect. The district will only expand if the matched gain is at least 3.0 points at an acceptable cost per point.

Decide whether to expand the after-school tutoring program district-wide.

tutoring_expansion.pdf
Text
Write your evaluation in tutoring_expansion.pdf.

Give an expand-or-hold call with the math gain attributable to tutoring rather than to more-engaged families, in test-score points to one decimal place with its 95 percent confidence interval, and quantify how many of the 6 points are explained by the parental-engagement gap
Assess whether the edge would hold at schools without that parental baseline
Report the effect on attendance as a second outcome, in percentage points to one decimal place
Report the cost per test-score point gained and whether it clears the district's bar
State whether the effect differs by grade band, elementary versus middle school, giving each estimate
tutoring_readout.pptx
Visual
Prepare tutoring_readout.pptx for the school board.

An effect-size slide showing the matched tutoring gain as a point with its 95 percent confidence interval in test-score points and a labeled reference line at the 3.0 point expansion bar, alongside the raw gain at tutoring versus matched comparison schools
A decomposition slide splitting the raw 6-point gap into the parental-engagement-explained share and the adjusted gain, drawn as ordered bars
A grade-band small-multiple slide contrasting the adjusted gain for elementary versus middle school, each as a point with its interval
A second-axis slide reporting the attendance effect and the cost per point against the district bar
A findings slide stating the expand-or-hold call and the adjusted gain in words
math_gains_by_school.xlsx
Data
Attach math_gains_by_school.xlsx with the school-level detail.

One row per school with pre and post math scores, the score change in test-score points to one decimal place, parental-engagement index, and a matched-comparison flag
The adjusted gain after schools are matched on baseline engagement, in test-score points to one decimal place
Rank tutoring schools by adjusted gain, as an integer rank starting at 1
The attendance change per school, in percentage points to one decimal place
The per-school program cost and cost per point
tutoring_match.py
Code
Provide tutoring_match.py that matches schools and states the call.

Match tutoring schools to comparison schools on baseline engagement and print the adjusted gain with its confidence interval
Print the raw 6-point gap and the engagement-explained share
Print the grade-band split estimates
Print an expand or hold flag based on the matched gain clearing 3.0 points with cost per point within the bar
Demographic & Social Science
A city expanded paid parental leave and fertility rates rose over the following two years relative to the prior trend, but several neighboring cities without the policy saw similar upticks tied to a broader economic recovery. A city-by-year panel covers several pre-policy years for the treated and comparison cities, with leave-uptake rate, female labor-force participation as a second outcome, a parity split (first births versus higher-order births), and program cost. The panel supports a confidence interval on the difference-in-differences, a pre-trend test, and a placebo on a pre-policy window. The question is whether the policy itself moved fertility.

Decide whether the paid-leave expansion had a causal effect on fertility.

leave_fertility.pdf
Text
Present your conclusion in leave_fertility.pdf.

Give a verdict on whether the leave expansion changed fertility once the region-wide recovery is netted out, reporting the difference-in-differences fertility effect in births per 1,000 women to one decimal place with its 95 percent confidence interval
Assess whether the neighboring-city upticks leave any effect attributable to the policy, quantifying the shared-recovery share
Report the placebo difference-in-differences on a pre-policy window, which should be near zero
Report the effect on female labor-force participation as a second axis, in percentage points to one decimal place, and the program cost per additional birth
State whether the effect concentrates in first births or higher-order births, giving each estimate
fertility_panel.csv
Data
Provide fertility_panel.csv, the city-by-year panel.

One row per city per year with the fertility rate in births per 1,000 women to one decimal place, a treatment flag, and a period flag for pre or post
The treated-minus-comparison change around the policy date, in births per 1,000 women to one decimal place
Leave-uptake rate and female labor-force participation columns per city-year
A parity-split column separating first births from higher-order births
fertility_dashboard.html
Visual
Attach fertility_dashboard.html, a standalone multi-panel dashboard of the paid-leave analysis.

Panel one: a parallel-trends line plotting fertility paths for the treated city versus comparison cities with the policy date marked, so pre-policy parallelism or its absence is visible, y-axis in births per 1,000 women
Panel two: an effect-size panel showing the difference-in-differences fertility effect as a point with its 95 percent confidence interval and a labeled reference line at zero, plus the placebo estimate point near zero beside it
Panel three: a parity small-multiple contrasting the effect for first births versus higher-order births, each as a point with its interval
Panel four: a second-axis panel showing the female labor-force participation effect and the program cost per additional birth
A headline findings banner stating the causal verdict and the difference-in-differences effect in words
leave_did.py
Code
Provide leave_did.py estimating the difference-in-differences.

Estimate the difference-in-differences fertility effect and print it with its confidence interval
Print the pre-trend and placebo test result
Print the parity-split estimates
Print a causal verdict flag based on the effect being significant with parallel pre-trends
Nonprofit & Grant-making
A foundation-funded job-training grant across 20 community organizations saw completers post employment rates 18 points higher than non-completers. Completion is voluntary and dropouts differ systematically from finishers, so the raw gap may overstate impact. Participant-level baseline traits, completion status, employment outcomes, and earnings are recorded, a comparable untreated group of eligible non-enrollees is available, organization id and per-participant program cost are tracked. Sample sizes support a confidence interval on the adjusted effect and a covariate-balance check. Renewal is only justified if the adjusted effect is at least 8 percentage points at an acceptable cost per placement.

Decide whether to renew the job-training grant on the basis of a real causal employment effect.

grant_renewal.docx
Text
Write the analysis in grant_renewal.docx.

Give a renew-or-not call with the employment gain genuinely caused by the program rather than by who completes it, in percentage points to one decimal place with its 95 percent confidence interval, reported against the raw 18-point completer gap side by side
Assess whether the completer-versus-dropout comparison overstates the effect, quantifying the selection share
Report the effect on earnings as a second outcome, in USD to the nearest whole dollar
Report the cost per employment placement and whether it clears the renewal bar
State whether the effect differs across the 20 organizations enough to renew selectively
employment_by_completion.xlsx
Data
Provide employment_by_completion.xlsx with the participant-level detail.

One row per participant with completion status, baseline traits, employment outcome, organization id, and program cost
Employment rates for completers, non-completers, and the comparable untreated group, each in percent to one decimal place
The adjusted employment effect, in percentage points to one decimal place, alongside the raw 18-point gap
The counts of completers, non-completers, and comparison-group members, each as a whole-number count
The per-organization adjusted effect
employment_effect_panel.png
Visual
Include employment_effect_panel.png, a multi-panel effect-and-robustness figure.

Lead with an effect-size plot showing employment rates for completers, non-completers, and the comparison group, plus the raw 18-point gap and the adjusted effect as labeled bars ordered from largest to smallest, with a labeled reference line at the 8 percentage point renewal bar
Add a covariate-balance panel plotting standardized mean differences of baseline traits before versus after adjustment to show the selection was closed
Add a per-organization small-multiple ranking the 20 organizations by adjusted effect, ordered from highest to lowest
Add a second-outcome panel showing the earnings effect in USD
Title the figure with the renew-or-not finding and the adjusted effect stated in words
grant_effect.py
Code
Provide grant_effect.py estimating the adjusted effect.

Estimate the adjusted employment effect against the comparable untreated group and print it with its confidence interval
Print the baseline-covariate balance before and after adjustment as standardized mean differences to two decimal places
Print the earnings second-outcome effect
Print a renew or not flag based on the adjusted effect clearing 8 percentage points with cost per placement within the bar
Nonprofit & Grant-making
A donor matching campaign emailed to a random half of lapsed donors saw the treated group give 9 percent more total dollars, but the match offer was only ever seen by donors who opened the email, so compliance is imperfect. Donor-level assignment, open and response status, dollars given, lapse-recency segment, a pre-campaign giving baseline, and the match payout cost are all available. Sample sizes support a confidence interval on the intent-to-treat effect and a treatment-on-the-treated estimate scaled by the open rate. We need the effect of running the campaign at full scale, not just among engaged openers.

Determine whether to run the donor-match campaign at full scale.

match_campaign_effect.py
Code
Deliver match_campaign_effect.py, the script that records the decision.

Print the intent-to-treat giving effect across all assigned donors, not just openers, in USD per donor to the nearest whole dollar, with its confidence interval
Print the treatment-on-the-treated opener effect and the open rate so the compliance gap is explicit
Print the net intent-to-treat effect after subtracting the match payout cost, in USD per donor
Print the counts of assigned, opened, and responded donors, each as a whole number
Print a run or hold flag based on the net intent-to-treat effect being positive
campaign_summary.csv
Data
Include campaign_summary.csv with the donor-level figures.

One row per donor with assignment, open status, response status, dollars given to the nearest whole dollar, and lapse-recency segment
Dollars given for treated versus control across the full assigned groups, in USD per donor to the nearest whole dollar
Distinguish the offered-the-match intent-to-treat effect from the opener-only effect, both in USD per donor to the nearest whole dollar
The open rate in the treated group, as a percentage to one decimal place
The per-segment intent-to-treat effect by lapse recency
match_campaign_decision.docx
Text
Write match_campaign_decision.docx with the recommendation in writing.

State whether to run the donor-match campaign at full scale
Report the intent-to-treat giving effect across all assigned donors, in USD per donor to the nearest whole dollar, with its confidence interval
Explain why the opener-only effect overstates what full-scale rollout would deliver
Report the net effect after match cost and the implied return per dollar of match budget
State whether the effect concentrates among recently lapsed versus long-lapsed donors, giving each segment's effect
match_campaign_readout.pptx
Visual
Prepare match_campaign_readout.pptx, a leadership readout contrasting the assigned effect with the opener-only effect.

An effect-size slide showing the intent-to-treat effect across all assigned donors as a point with its 95 percent confidence interval and a labeled reference line at zero, with the treatment-on-the-treated opener effect point beside it so the compliance gap is visible, dollars per donor to the nearest whole dollar
A compliance slide showing the open rate and how it scales the intent-to-treat effect up to the treatment-on-the-treated estimate
A per-segment small-multiple slide of the intent-to-treat effect by lapse-recency segment, ordered by effect
A cost slide showing the net intent-to-treat effect after the match payout and the implied return per dollar of match budget
A findings slide stating the run-or-hold call and the net intent-to-treat effect in words

Forecasting & Predictive Modeling
The decision depends on a future value or a predicted outcome that the supplied history can pin down.
10 prompts
Product Analytics
Support ticket volume for our SaaS platform spikes with every major release and the on-call staffing model keeps missing these bursts. We have three years of daily ticket counts split across three product lines (Core, Billing, Integrations), the release calendar tagged major versus minor, and per-ticket handle-time logs. Each on-call rotation clears about 220 tickets per day; a third rotation costs 42,000 dollars per month, while every day that demand breaches two-rotation capacity triggers roughly 3,100 dollars of overtime. Ops holds a service target that no more than five percent of days may exceed capacity. The decision is whether to add a third on-call rotation for next month.

Recommend whether to add the third on-call rotation, tied to whether forecast peak daily load and the count of capacity-breaching days violate the two-rotation capacity and the five-percent service target, and only after the model beats a naive seasonal baseline.

ticket_forecast.py
Code
Deliver the model as ticket_forecast.py.

Print the chosen model's backtest accuracy (MAPE) alongside a naive seasonal baseline, each as a percentage to one decimal place, so the improvement is visible
Use the release calendar as an input and print the average incremental daily tickets attributable to a major release versus a minor release, each as a whole number of tickets
Report the backtest window length in days, as a whole number, used to compute the reported accuracy
Print the forecast peak daily load and the number of days next month forecast to exceed two-rotation capacity, each as a whole number
Print the share of forecast peak-day volume carried by each of the three product lines, each as a percentage to one decimal place
daily_ticket_forecast.csv
Data
Output daily_ticket_forecast.csv covering next month.

One row per day for the next month with predicted ticket load and interval bounds, each as a whole number of tickets rounded to the nearest integer
Flag the days that coincide with a scheduled release and label each as major or minor
Include a boolean column marking days whose point forecast exceeds two-rotation capacity
Include a column giving the interval width, as a whole number of tickets, for each day
Break each day's total into Core, Billing, and Integrations columns that sum to the daily point forecast
staffing_recommendation.pdf
Text
Add staffing_recommendation.pdf stating the on-call decision.

Give a clear yes or no on adding the third rotation, tied to both the forecast peak load against two-rotation capacity and the breach-day count against the five-percent service target
Name the peak days next month that drive the staffing call
State the forecast peak daily load, the two-rotation capacity, and the count of capacity-breaching days, each as a whole number
Compare the monthly cost of a third rotation against the estimated overtime cost of the forecast breach days, each in USD rounded to the nearest thousand
staffing_forecast_deck.pptx
Visual
Add staffing_forecast_deck.pptx presenting the forecast to Ops leadership.

Lead with a fan chart slide plotting the point-forecast line, the interval band, and a trailing-actuals overlay for daily tickets, with the two-rotation capacity drawn as a labeled horizontal threshold line at its value
Annotate the single peak day and shade the run of capacity-breaching days; the slide title must state the add-or-hold call and the next-month horizon
Add a small-multiples slide with one panel per product line (Core, Billing, Integrations) showing that line's forecast path and its share of peak-day load
Close with a findings slide stating the recommendation, the forecast peak load, the breach-day count, and the third-rotation cost versus overtime comparison
Supply Chain & Logistics
A regional grocery distributor needs a reorder decision for its top forty SKUs over the next six weeks. Roughly a third have intermittent demand with many zero-demand days, while the rest are smooth and slightly trending. Each SKU carries a current on-hand position, a supplier lead time, a target service level of 95 percent that sets its safety stock, and a listed unit cost. Total purchase-order value is capped by an open-to-buy budget of 850,000 dollars. The forecast must drive both the per-SKU order quantity and whether the combined order fits the budget.

Produce the six-week demand forecast that drives the purchase order, net it against on-hand and safety stock to a reorder quantity per SKU, and state whether the total order value fits the open-to-buy budget, committing to an approach suited to the intermittent-plus-smooth mix.

reorder_forecast.pdf
Text
Write it up in reorder_forecast.pdf for the buyer.

State the total six-week reorder quantity across all forty SKUs as a whole number of units and its total value in USD rounded to the nearest thousand, and whether that value fits the open-to-buy budget
Explain how the intermittent-demand SKUs were treated differently from the smooth ones
Name the forecasting method chosen for the intermittent SKUs (for example Croston's method) and the method for the smooth SKUs
Name the three SKUs with the largest reorder value and the count of SKUs whose forecast demand exceeds current on-hand, each as a whole number
sku_demand_forecast.xlsx
Data
Attach sku_demand_forecast.xlsx with the per-SKU numbers.

One row per SKU with the six-week forecast quantity, a low-high range, the safety stock at the 95 percent service level, and the reorder quantity net of on-hand and safety stock, each as a whole number of units rounded to the nearest integer
Tag each SKU as intermittent or smooth and include its supplier lead time in days
Include the count of zero-demand days per SKU as a whole number so the buyer sees which numbers carry more uncertainty
Include the reorder value per SKU in USD and a total row summing forecast quantity, reorder quantity, and reorder value
forecast_build.py
Code
Provide forecast_build.py that generates the per-SKU six-week forecast.

Route intermittent SKUs to an intermittent-demand method and smooth SKUs to a trend method, and print which method each SKU used
Output the six-week total quantity per SKU, as a whole number of units rounded to the nearest integer
Print the total purchase-order quantity and total value across all forty SKUs, and a pass or fail against the open-to-buy budget
Print the backtest MAPE separately for the intermittent group and the smooth group, each as a percentage to one decimal place
reorder_dashboard.html
Visual
Add a standalone reorder_dashboard.html for the buyer's review meeting.

Top panel is a fan chart of aggregate weekly demand across the forty SKUs: point-forecast line, interval band, and a trailing eight-week actuals overlay, with a labeled horizontal line at the demand level the open-to-buy budget can fund
Add a small-multiples grid of the six largest-value SKUs, each panel showing its six-week forecast with its interval and a panel title naming the SKU and its method (intermittent or smooth)
Add an ordered horizontal bar panel of SKUs by reorder value, highlighting the three largest and drawing a marked line at the 850,000 dollar budget cap
Add a findings panel stating whether the order fits the budget, the total order value, and the count of SKUs whose forecast exceeds on-hand
Supply Chain & Logistics
A port terminal operator is weighing whether to lease extra yard space before peak season. Container throughput has clear weekly and annual seasonality, but the past eighteen months also carried a one-time surge from a competitor's outage that has now resolved. Throughput is handled across two berths with a fixed combined yard capacity; a lease adds a known block of slots at a known weekly cost, and every week throughput exceeds capacity incurs a demurrage penalty per over-capacity container. The go decision depends on both the size and the number of the forecast breach weeks.

Give a go or no-go on the lease, based on whether forecast peak weekly throughput exceeds current yard capacity, how many weeks breach it, and whether the lease cost is justified by the avoided demurrage.

yard_capacity_forecast.pdf
Text
Report in yard_capacity_forecast.pdf for the leasing decision.

State the go or no-go on the lease, tied to peak weekly throughput versus capacity and the count of breach weeks
Explain how the resolved competitor-outage surge was kept from inflating the peak forecast
Report the forecast peak weekly throughput and current capacity, each as a whole number of containers
Compare the season's lease cost against the demurrage that would be avoided across the breach weeks, each in USD rounded to the nearest thousand
weekly_throughput_forecast.csv
Data
Provide weekly_throughput_forecast.csv with the peak-season path.

One row per week through next peak season with forecast throughput and interval bounds, each as a whole number of containers rounded to the nearest integer
Include the current yard capacity as a reference field and a per-week over-capacity container count
Include a week-start date field, one per forecast week, so the series is ordered
Include a boolean breach flag per week where the point forecast exceeds capacity, and a per-berth split of the weekly forecast that sums to the total
yard_forecast.py
Code
Provide yard_forecast.py that reproduces the seasonal forecast.

Fit a seasonal model that isolates and removes the resolved competitor-outage surge, and print the backtest MAPE against a naive seasonal baseline, each as a percentage to one decimal place
Print the forecast peak weekly throughput and the count of breach weeks, each as a whole number
Print the season lease cost against the avoided demurrage, each in USD rounded to the nearest thousand
Print the forecast peak weekly throughput at each of the two berths, each as a whole number of containers
peak_vs_capacity.png
Visual
Add peak_vs_capacity.png showing the forecast against the capacity line.

Draw a fan chart of forecast weekly throughput with its point line, interval band, and a trailing-actuals overlay, and mark current capacity as a labeled horizontal line at its value, with the y-axis in containers scaled in increments rounded to the nearest thousand
Shade the weeks where the forecast crosses capacity and annotate the count of breach weeks and the single worst week's over-capacity container count, each as a whole number
Add a two-panel small-multiple beneath, one per berth, each showing that berth's forecast line and its share of peak-week load
Give the chart a title stating the go or no-go call and the peak-season horizon
Economics
A state treasury office must forecast next fiscal year's sales tax receipts to size the budget. Twelve years of monthly receipts show trend, seasonality, and a sharp recession dip and recovery. Recent nominal receipts have been lifted by inflation, and there is debate about how much of that is transitory. A companion CPI series lets receipts be deflated to real terms, and the budget must be sized on the persistent, not the transitory, component. The budget office holds a spending target it wants the central forecast to clear.

Deliver the annual sales-tax receipts forecast with a plausible low and high scenario, splitting the nominal figure into a real-growth component and an inflation component, and commit to the forecasting model behind it.

tax_receipts_forecast.pdf
Text
Write it to tax_receipts_forecast.pdf for the budget team.

State the annual receipts forecast in USD rounded to the nearest million, with a low and a high budget scenario on the same basis, and whether the central forecast clears the budget office's spending target
Split the year-over-year growth into a real-growth component and an inflation component, each in percent to one decimal place
Address whether recent inflation-driven receipts were treated as persistent or transitory and why
State the forecasting model used and the reason it was chosen over the alternatives
monthly_receipts_forecast.csv
Data
Attach monthly_receipts_forecast.csv rolling up to the annual figure.

One row per month of the fiscal year with the forecast and low-high scenario values in USD rounded to the nearest whole dollar, summing to the annual total
Include recent actual months so the forecast can be read against the recovery trend
Include both a nominal forecast and a real (deflated) forecast column per month, each in USD to the nearest whole dollar
Include a flag distinguishing recent actual rows from forecast rows
tax_receipts_forecast.py
Code
Include tax_receipts_forecast.py that reproduces the forecast from the receipts history.

Print a holdout accuracy figure (MAPE) on recent months versus a naive seasonal baseline, each as a percentage to one decimal place
Deflate nominal receipts to real terms and print the persistent-versus-transitory inflation adjustment applied, in percent to one decimal place
Print the annual nominal total and the annual real total, each in USD rounded to the nearest million
Run cleanly from the raw monthly receipts and CPI series to the saved annual and monthly forecast tables
receipts_forecast_deck.pptx
Visual
Add receipts_forecast_deck.pptx for the budget hearing.

Lead with a fan chart slide of monthly receipts: point-forecast line, interval band, and a recent-actuals overlay, with the prior fiscal year's monthly path drawn as a labeled reference line
Add a decomposition slide with stacked bars splitting year-over-year growth into a real-growth component and an inflation component, each labeled with its value in percent
Add a scenario slide showing the annual forecast under low, central, and high on a single axis, with the budget office's spending target drawn as a labeled horizontal line
Close with a findings slide stating the annual forecast, the real-versus-inflation split, and the model chosen
Economics
A commodities desk wants a next-quarter price forecast for regional wholesale electricity to decide whether to hedge. Prices are volatile, mean-reverting, and spike hard during heat waves, and simple trend models have badly overfit the spikes. The desk holds a hedge at a known strike price and pays a fixed premium per megawatt-hour to extend it; the hedge pays only in weeks the average price clears the strike. The call depends on how many weeks are forecast to clear the strike and by how much.

Produce the quarterly average price forecast with an honest range, give the hedge or no-hedge call based on the forecast weeks clearing the strike and the expected payoff against the premium, and commit to a defensible method.

electricity_price_forecast.docx
Text
Summarize in electricity_price_forecast.docx for the desk.

State the quarterly average price forecast in USD per megawatt-hour rounded to two decimal places, with a range on the same basis, and give a clear hedge or no-hedge call
Explain how the heat-wave spikes were handled so the forecast is not overfit to them
Report the backtest error (MAPE) of the chosen method versus a simple trend baseline, each as a percentage to one decimal place
State the count of weeks whose central forecast clears the strike price and the expected net payoff of the hedge against its premium, in USD rounded to the nearest thousand
price_scenarios.csv
Data
Attach price_scenarios.csv with the scenario detail.

Give the quarterly average price under central, low, and high scenarios, each in USD per megawatt-hour rounded to two decimal places
Include a weekly forecast path, in USD per megawatt-hour rounded to two decimal places, so the desk can see where spike risk concentrates within the quarter
Flag the weeks whose central forecast exceeds the current hedge strike price
Include a per-week amount by which the central forecast clears the strike, in USD per megawatt-hour, zero where it does not clear
forecast_model.py
Code
Include forecast_model.py, the model that produces the forecast and scenarios.

Fit a mean-reverting model and print the quarterly average central forecast, in USD per megawatt-hour to two decimal places
Print the backtest MAPE against a simple trend baseline, each as a percentage to one decimal place
Emit the low and high scenario quarterly averages from the forecast interval, in USD per megawatt-hour to two decimal places
Print the count of strike-clearing weeks and the expected hedge payoff net of premium, in USD to the nearest thousand
price_forecast_dashboard.html
Visual
Add a standalone price_forecast_dashboard.html for the trading review.

Top panel is a fan chart of the weekly price path: point-forecast line, interval band, and a recent-actuals overlay, with the hedge strike price drawn as a labeled horizontal reference line in USD per megawatt-hour
Shade the weeks whose central forecast clears the strike and annotate the count of clearing weeks and the single largest weekly clearance amount
Add a scenario panel with central, low, and high quarterly-average bars against the strike line
Add a findings panel stating the hedge or no-hedge call, the count of clearing weeks, the expected net payoff against the premium, and the backtest MAPE versus the trend baseline
Policy & Education
A school district must decide how many kindergarten classrooms to fund next year, which hinges on projected enrollment. We have fifteen years of enrollment by grade plus recent birth records for the catchment, and a new housing development just opened with no historical analog. Classrooms are funded in blocks with a fixed cap of 24 students each, so the count and its upper bound both drive how many rooms and teachers to fund. Each classroom costs a known amount to staff and equip, and the board holds a fixed classroom-funding budget the plan must fit.

Give next year's kindergarten enrollment count with a range, decompose it into the birth-cohort baseline and the new-development increment, commit to a cohort-survival method, and translate the count and its upper bound into a classroom count at 24 per room.

enrollment_forecast.pdf
Text
Write to enrollment_forecast.pdf for the funding decision.

State next year's kindergarten count as a whole number of students with a range on the same basis the board can fund classrooms against
Quantify how much the new housing development shifts the count, as a whole number of students, on top of the birth-cohort signal
Name the cohort-survival method used to carry the birth signal into kindergarten enrollment and report its holdout backtest accuracy (MAPE) against a naive baseline, each as a percentage to one decimal place
State how many classrooms to fund at 24 students per room under the central count and under the upper bound, each as a whole number, and whether the staffing-and-equipping cost at that classroom count fits the board's budget, in USD rounded to the nearest thousand
kindergarten_projection.csv
Data
Attach kindergarten_projection.csv with the projection detail.

Show the projected kindergarten count with low and high bounds, each as a whole number of students rounded to the nearest integer
Break out the birth-cohort-derived baseline separately from the development adjustment, each as a whole number of students, summing to the total
Show the birth-cohort survival ratio applied per year, to two decimal places
Include the implied classroom count at 24 per room for the central, low, and high figures
enrollment_projection.py
Code
Include enrollment_projection.py that reproduces the cohort-survival projection.

Apply the cohort-survival ratios to the birth records and print the survival ratio used per year, to two decimal places
Print a holdout backtest accuracy (MAPE) of the cohort-survival projection against a naive last-year-carried-forward baseline on recent years, each as a percentage to one decimal place
Print the central projected count with its low and high bounds, each as a whole number of students
Print the birth-cohort baseline and the new-development increment separately, each as a whole number, so their sum reconciles to the central count
Print the classrooms to fund at 24 per room under the central count and under the upper bound, and the total staffing-and-equipping cost at the recommended classroom count against the board's budget, in USD rounded to the nearest thousand
enrollment_projection_chart.png
Visual
Include enrollment_projection_chart.png showing the projection against history.

Plot fifteen years of historical kindergarten enrollment plus the next-year projection point, with a shaded low-high band on the projection, counts as whole numbers of students
Draw horizontal reference lines at multiples of 24 (the classroom-capacity blocks) so the classroom count is readable off the chart, and a labeled line at the number of classrooms the board's budget can fund
Mark the new-development adjustment as a separate labeled increment stacked on the birth-cohort baseline, in whole students
Give the chart a title stating the classrooms-to-fund call for next year and whether it fits the funding budget
Policy & Education
A community college wants to predict which incoming students are at risk of not returning for a second year so it can size its advising budget. We have six cohorts of enrollment, course, and financial-aid records, with a modest sample and real class imbalance. Advising can cover a fixed caseload, each advised student costs a known amount, and leadership wants the intervention cutoff set where it catches the most true non-returners without exceeding the advising budget.

Recommend the probability cutoff that flags students for intervention, backed by a per-student retention probability and validation that guards against overfitting, and confirm the resulting flagged caseload and cost fit the advising budget.

retention_model.py
Code
Deliver the model in retention_model.py.

Output a retention probability for each incoming student between 0 and 1 to two decimal places and apply the chosen intervention cutoff
Report validation performance on held-out cohorts (AUC) to two decimal places so the small-sample, imbalanced result is trustworthy
Print the chosen probability cutoff and the recall and precision at that cutoff, each to two decimal places
Print the flagged student count and the implied advising cost against the budget, as a whole number and in USD rounded to the nearest thousand
at_risk_students.csv
Data
Produce at_risk_students.csv listing flagged students.

One row per student with retention probability to two decimal places and a flag for whether they clear the intervention cutoff
Include the total flagged count as a whole number so advising can size its budget directly
Include each student's cohort identifier so advising can see the distribution across cohorts
Include the top three predictor features contributing to each flagged student's risk
retention_recommendation.pdf
Text
Add retention_recommendation.pdf stating the cutoff decision.

Recommend the probability cutoff to use, tied to the share of true non-returners captured and to the flagged caseload and cost fitting the advising budget
State the held-out AUC and the recall and precision at the chosen cutoff, each to two decimal places
State the flagged student count and the implied advising cost against the budget, as a whole number and in USD rounded to the nearest thousand
Name the top predictor features driving retention risk across the flagged students
risk_calibration.png
Visual
Include risk_calibration.png so advising can see how well the risk scores separate returners from non-returners.

Plot overlaid distributions of predicted retention probabilities for students who returned versus those who did not, with the chosen cutoff drawn as a labeled vertical line at its value between 0 and 1 to two decimal places
Add a second panel showing recall and flagged-caseload cost across candidate cutoffs, with a labeled horizontal line at the advising budget and the chosen operating point marked
Annotate the count of flagged students on each side of the cutoff, as whole numbers, and put the held-out AUC in the caption
Give the figure a title stating the recommended cutoff and the resulting caseload call
Policy & Education
A city transit authority is deciding whether to keep a fare-free pilot on three bus routes. We have two years of daily ridership before the pilot and eight months during it, and ridership is strongly seasonal with a post-pandemic recovery trend underneath. Forgone fare revenue is a known amount per rider, and the authority will continue only if the pilot's rider lift and its cost per incremental rider clear leadership's thresholds.

Recommend continue or end the pilot based on a forecast counterfactual of ridership without the pilot compared to observed, the resulting rider lift, and the cost per incremental rider against leadership's threshold.

fare_pilot_forecast.pdf
Text
Report in fare_pilot_forecast.pdf for the authority.

Give a clear continue-or-end recommendation grounded in the observed-versus-counterfactual gap and the cost per incremental rider
State the estimated ridership lift as a whole number of average daily riders, with a range on the same basis
Report the cumulative rider lift over the eight-month pilot window, as a whole number of riders
State the forgone fare revenue and the cost per incremental rider, in USD, against leadership's threshold
counterfactual_ridership.py
Code
Deliver counterfactual_ridership.py that builds the no-pilot baseline.

Produce the daily counterfactual ridership path over the pilot window with intervals, each as a whole number of riders rounded to the nearest integer
Report accuracy on the pre-pilot period (MAPE) as a percentage to one decimal place so the counterfactual baseline is credible
Report the total observed-minus-counterfactual difference over the pilot, as a whole number of riders
Print the cost per incremental rider, in USD to two decimal places, from forgone fares divided by the cumulative lift
ridership_comparison.csv
Data
Output ridership_comparison.csv pairing observed against counterfactual.

One row per day of the pilot with observed ridership, counterfactual forecast, and the difference, each as a whole number of riders rounded to the nearest integer
Include a running cumulative lift as a whole number of riders so the total pilot effect is legible
Include a date field, one row per pilot day, so the series is ordered
Include a per-day forgone-fare-revenue column in USD
pilot_impact_deck.pptx
Visual
Add pilot_impact_deck.pptx for the board vote.

Lead with a counterfactual slide plotting observed ridership against the counterfactual point-forecast line with its interval band and a pre-pilot actuals overlay, with the pilot-start date drawn as a labeled vertical line
Add a pre-pilot fit slide showing the model tracking actuals over the pre-pilot period, captioned with the pre-pilot MAPE
Add a cumulative-lift slide charting running lift across the pilot, with a labeled line marking leadership's cost-per-incremental-rider threshold
Close with a findings slide stating the continue-or-end call, the daily lift with its range, and the cost per incremental rider against the threshold
Demographic & Social Science
A metropolitan planning agency needs a ten-year population projection for a fast-changing suburb to justify a water infrastructure bond. Records give annual population, births, deaths, and net migration, and migration has swung sharply in the last four years with no clear steady state. The bond is sized on projected peak demand, so the projection must decompose the components and translate the terminal-year population into water demand at a known per-capita gallons-per-day rate. The utility holds a treatment-capacity ceiling in gallons per day that the projected demand must be tested against.

Deliver the ten-year population projection with a range under low, central, and high migration scenarios, decompose it into births, deaths, and net migration, commit to a projection method, and translate the terminal-year population into projected daily water demand.

population_projection.pdf
Text
Write population_projection.pdf to support the bond case.

State the ten-year population projection as a whole number of people rounded to the nearest hundred, with a range on the same basis wide enough to reflect the migration uncertainty
Explain how the volatile recent migration was handled and why the chosen method fits
State whether cohort-component or extrapolation was used and why
State the projected terminal-year daily water demand in gallons per day at the per-capita rate, under the central and high scenarios, and whether it breaches the utility's treatment-capacity ceiling
annual_population_projection.csv
Data
Attach annual_population_projection.csv with the yearly path.

One row per year for ten years with projected population and low-high bounds, each as a whole number of people rounded to the nearest integer
Break out the births, deaths, and net-migration components feeding each year's total, each as a whole number, reconciling to the year-over-year change
Include the assumed annual net-migration rate feeding each year, in percent to one decimal place
Include the implied daily water demand per year in gallons per day at the per-capita rate
population_projection.py
Code
Include population_projection.py that reproduces the projection.

Print the ten-year projected population under low, central, and high migration scenarios, each as a whole number of people to the nearest hundred
Print the net-migration assumption used in each scenario, as a whole number of people per year
Print the terminal-year daily water demand in gallons per day under each scenario
Run cleanly from the raw annual births, deaths, and migration history to the saved projection table
population_demand_dashboard.html
Visual
Add a standalone population_demand_dashboard.html for the bond hearing.

Top panel is a fan chart of the ten-year population projection under the central scenario: point line, low-high band, and a recent-actuals overlay of annual population
Add a decomposition panel with stacked bars per year showing the births, deaths, and net-migration contributions to each year's change
Add a small-multiples panel with one chart per migration scenario (low, central, high), each annotated with its terminal-year population and implied daily water demand, with the treatment-capacity ceiling drawn as a labeled horizontal line
Add a findings panel stating the terminal-year water demand under central and high against the capacity ceiling and the resulting bond-sizing call
Nonprofit & Grant-making
A grant-making foundation wants to project next year's total donation revenue to set its grant budget. Ten years of gift records show heavy December concentration, a handful of one-time major gifts that distort the trend, and steady growth in recurring small donors. The board follows a spend rule that budgets grants at a fixed share of the predictable recurring base only, treating volatile major gifts as upside, so the projection must separate the two streams and apply the rule.

Give the total donation-revenue projection with a range, separate the predictable recurring base from the volatile major-gift component, and state the grant budget the spend rule sets from the recurring base.

donation_forecast.docx
Text
Deliver donation_forecast.docx for the grant-budget decision.

State next year's total donation-revenue projection in USD rounded to the nearest thousand, with a range on the same basis
Break the projection into the predictable recurring base versus the volatile major-gift component, each in USD rounded to the nearest thousand, summing to the total
Name the method used to forecast the recurring base and how the volatile major gifts were handled separately
State the grant budget the spend rule sets as its fixed share of the recurring base, in USD rounded to the nearest thousand
revenue_projection.xlsx
Data
Attach revenue_projection.xlsx with the split-out build.

Give a monthly forecast in USD rounded to the nearest whole dollar that captures the December concentration, with interval bounds on the same basis
Show the recurring-base and major-gift streams as separate columns in USD that sum to the monthly total
Flag the historical one-time major gifts excluded from the base trend, each in USD to the nearest dollar
Include an annual total row and the spend-rule grant budget derived from the recurring-base annual total
donation_forecast.py
Code
Include donation_forecast.py that reproduces the split forecast.

Forecast the recurring base separately from the volatile major gifts and print the backtest MAPE on the recurring base versus a naive seasonal baseline, each as a percentage to one decimal place
Print the recurring-base annual total and the major-gift annual component separately, each in USD rounded to the nearest thousand
Print the total projection with its low-high range, in USD rounded to the nearest thousand
Print the spend-rule grant budget as the fixed share of the recurring-base annual total, in USD rounded to the nearest thousand
donation_forecast_chart.png
Visual
Include donation_forecast_chart.png showing the monthly projection.

Plot a fan chart of the monthly donation-revenue projection for next year with its point line, interval band, and a trailing-actuals overlay, in USD to the nearest thousand, with the December concentration visible
Show the recurring-base and major-gift components as separate stacked series that sum to the monthly total, and annotate the December peak month and the excluded one-time major gifts
Draw a labeled horizontal line at the spend-rule grant budget the recurring base supports
Give the chart a title stating the grant budget the spend rule sets for next year

Data Extraction & Conformation (ETL / Pipeline Build)
The work is to reconcile messy multi-source inputs into one analysis-ready, contract-conforming dataset.
10 prompts
Product Analytics
Marketing spend lands from four ad platforms, each with its own campaign naming, its own currency, and daily grains that sometimes double-count the last day of a month against a separate monthly export. Finance can't close Q2 until spend is reconciled into one daily USD table, and they also want the spend split by month and by platform, the size of the correction versus the naive sum they had been circulating, and any spend that can't be tied to an internal campaign.

Tell us our total conformed marketing spend for Q2 in USD from a single reconciled daily table.

spend_conform.py
Code
Please write spend_conform.py, which builds the reconciled daily spend table and prints the Q2 figures.

Converts every platform's spend to USD using the date-keyed FX rate table and maps each platform's campaign names to the internal campaign_id via the crosswalk
Drops the overlapping duplicate month-end rows where the daily feed and the separate monthly export cover the same day
Prints total conformed Q2 spend in USD to the nearest dollar, the same total broken out by calendar month and by platform, and names the single top campaign by conformed spend with its USD
Prints the naive uncorrected Q2 total, the naive-minus-conformed correction split into the FX-revaluation portion and the duplicate-removal portion, and the USD of spend that could not be mapped to an internal campaign_id
daily_spend_usd.csv
Data
Deliver daily_spend_usd.csv, the single conformed daily spend table in USD.

One row per campaign per day in USD with the internal campaign_id attached, and no duplicated last-day-of-month rows carried over from the monthly export
Carries the original platform, native currency, applied FX rate, and native-currency amount for each row
Includes an unmapped flag marking rows whose campaign name found no crosswalk match
Retains the source platform on each row so per-platform row counts reconcile back to each feed
spend_reconciliation_waterfall.png
Visual
Deliver spend_reconciliation_waterfall.png, a spend-reconciliation waterfall from the naive total to the conformed total.

Render a waterfall chart that starts at the naive uncorrected Q2 total in USD and ends at the conformed Q2 total, with one intermediate step bar for the duplicate-removal reduction and one for the FX-revaluation adjustment, each labeled with its USD
Add a labeled step bar for the unmapped spend that could not be tied to an internal campaign_id, sized to its USD
Draw a horizontal reference line at the naive circulated total with its USD value labeled so the size of the total correction is visible against it
Annotate the single largest adjustment step by name with its USD amount, and title the chart with the final conformed Q2 total in USD
spend_reconciliation_notes.docx
Text
Summarize the reconciliation in spend_reconciliation_notes.md for finance.

State the total conformed Q2 spend in USD and the naive-minus-conformed correction in USD, with the correction split into its FX and duplicate-removal portions
List the four platforms with each one's Q2 USD contribution and give the April, May, and June split in USD
Report the count of duplicate month-end rows dropped and the count of campaign names with no crosswalk match, each a whole number, plus the total unmapped spend in USD
Report the per-platform row counts feeding the table and the number of distinct internal campaign_ids after crosswalking, each a whole number
Product Analytics
We need one clean subscription-state table pulled from a Stripe events JSON stream and a legacy billing CSV that predates the migration, with a six-week overlap where the same subscription appears in both under different plan vocabularies and inconsistent money formats. The board wants a defensible active-subscriber number as of the cutover, the active recurring revenue behind it, and both broken out by plan so pricing can see where the base sits.

Tell us how many active paid subscriptions we had as of the cutover date, from one unified subscription table.

subscription_conform.py
Code
Please write subscription_conform.py, the pipeline that unifies the two systems and prints the cutover figures.

Unifies plan codes through the mapping file and converts all amounts to cents, including Stripe's mixed cents-and-dollar-string values
Deduplicates the six-week overlap by treating the Stripe record as authoritative over the legacy billing record
Prints the count of active paid subscriptions as of the cutover date and the active monthly recurring revenue in USD at cutover, plus both broken out by unified plan code
Prints the naive pre-dedup subscription count summing both systems alongside the conformed count so the overlap correction is visible, and the count of overlap-window subscriptions resolved to Stripe
conformed_subscriptions.csv
Data
Hand back conformed_subscriptions.csv, the single conformed subscription-state table.

One row per subscription with a unified plan code and amounts stored consistently in cents
Overlapping legacy rows suppressed in favor of the authoritative Stripe record
Includes a source column marking whether each surviving row came from Stripe or legacy billing and a status column for active versus not
Retains the original plan vocabulary and original amount string so each row traces back to its system
subscription_quality_dashboard.html
Visual
Deliver subscription_quality_dashboard.html, a standalone multi-panel data-quality dashboard for the cutover conform.

Include a dedup waterfall panel from the naive pre-dedup subscription count down to the conformed active count, with a labeled step for the overlap-window records resolved to Stripe
Include a before/after grouped bar panel of active subscriptions by unified plan code, one pair of bars per plan showing the pre-conform count beside the conformed count
Include a panel of active monthly recurring revenue by unified plan code with the plans ordered by conformed MRR descending, and a reference line at the total active MRR
Add a reconciliation callout stating the conformed active-subscriber count and the active MRR in USD at cutover, with a per-source line reconciling surviving Stripe versus legacy rows
cutover_reconciliation.docx
Text
Add cutover_reconciliation.md explaining the active-subscriber figure and how the overlap was handled.

State the count of active paid subscriptions at cutover and the active monthly recurring revenue in USD at cutover
Give the active count and the active recurring revenue broken out by unified plan code
Report the naive-minus-conformed count difference and the number of overlapping subscriptions resolved to Stripe, each a whole number, and list any plan codes that had no clean mapping
Report the count of legacy amount strings that required conversion to cents and the surviving row count per source, each a whole number
Supply Chain & Logistics
The same physical products show up across three supplier catalogs and our internal ERP item table under different vendor part numbers, inconsistent pack sizes, and non-standard UOM strings, and every item also carries a product category we want to keep. Procurement needs one clean item master to know what we actually carry, and because the catalogs are dirty in different ways they want the rows dropped by each cleaning rule broken out per source, the conformance rate within each product category, the size of the resolved count against the naive raw count, and the per-each price on every canonical product with the largest cross-vendor gaps to negotiate on. Procurement will only trust the master if at least 95 percent of ERP items resolve to a canonical product.

Tell us how many distinct products we truly carry after resolution, backed by one canonical SKU master.

sku_master_conform.py
Code
Please write sku_master_conform.py, which builds the canonical item master and prints the resolution figures.

Resolves duplicates to one row per product using the part-number crosswalk and normalizes all pricing to per-each USD from the mixed each / case-of-12 / case-of-24 pack sizes
Standardizes the non-standard UOM strings to a controlled UOM vocabulary via the mapping and, for each source catalog, records the rows dropped by each named cleaning rule (duplicate collapse by crosswalk, pack-size normalization failure, and unmapped UOM or part number)
Prints the distinct product count after resolution against the raw pre-resolution row count and the naive-minus-conformed reduction, and the count broken out by whether each product matched across one, two, or all three catalogs
Prints the conformance rate within each product category as the share of that category's raw rows that resolved cleanly, and the ERP-to-canonical match rate as a percent with an explicit pass or fail against the 95 percent trust gate
Prints the count of products whose per-each price differs across the catalogs they appear in and the single largest per-each price gap in USD as the negotiation target
sku_master.xlsx
Data
Hand back sku_master.xlsx, the conformed item master.

One row per canonical product with a normalized per-each USD price, a standardized UOM, and its product category
Retains the contributing vendor part numbers and each source catalog's original pack size and price so buyers can trace the resolution
Includes a source-count column giving how many catalogs each canonical product was matched from
Includes a price-dispersion column giving the max-minus-min per-each USD price across the matched catalogs for each product
Carries the product category on each row so the per-category conformance rates reconcile back to the master
sku_resolution_deck.pptx
Visual
Deliver sku_resolution_deck.pptx, a short deck walking procurement through the resolution.

A resolution slide with a waterfall from the raw pre-resolution row count down to the distinct product count, with one labeled step bar for each cleaning rule (duplicates collapsed by the crosswalk, pack-size normalization drops, and unmapped UOM or part-number drops), each sized to its dropped-row count
A per-source slide with grouped bars of the rows dropped by each cleaning rule for each of the three catalogs, so the dirtiest source is visible
A match-coverage slide with one bar each for products matched across all three catalogs, exactly two catalogs, and only one catalog, each labeled with its count
A per-category conformance slide ranking the product categories by their conformance rate, ordered descending, with a reference line at the 95 percent trust gate
A findings slide stating the distinct product count carried, whether the master clears the 95 percent gate, and the largest per-each price gap in USD as the committed recommendation
sku_resolution_summary.pdf
Text
Hand back sku_resolution_summary.pdf explaining the resolution.

State the distinct product count after resolution against the raw pre-resolution row count and the naive-minus-conformed reduction
Report how many products appeared in all three supplier catalogs, in exactly two, and in only one, each a whole number
Report the rows dropped by each cleaning rule for each source catalog and the ERP-to-canonical match rate against the 95 percent trust gate
Give the conformance rate within each product category and explain the pack-size normalization from each, case-of-12, and case-of-24 to per-each USD
State the count of products with a cross-catalog price gap and the largest single per-each gap in USD, plus any part numbers that found no crosswalk match
Supply Chain & Logistics
Delivery scan events arrive from two carrier feeds and one in-house driver app, all stamping times in the local terminal timezone with no offset recorded, and some parcels are scanned in more than one feed. Our service contract sets a 95 percent on-time target. Ops leadership wants a defensible on-time delivery number for the service review against that target, plus how late the late parcels actually run and a per-carrier breakdown so they know which carrier to escalate.

Tell us how many deliveries were on time against the promised dates, from one conformed scan table.

delivery_scan_conform.py
Code
Please write delivery_scan_conform.py, which conforms the scans and reports the on-time figures.

Normalizes every scan to UTC by joining to the terminal-to-timezone reference table
Keeps the earliest 'delivered' scan per parcel across the carrier feeds and driver app, then measures the delivered timestamp against the promised-date table
Prints the on-time delivery count and the on-time rate in percent to one decimal, plus both broken out by carrier
Prints the median lateness in hours across the late parcels and the count of parcels delivered more than 24 hours late
conformed_scans.csv
Data
Deliver conformed_scans.csv, the single conformed scan table.

One row per parcel scan in UTC with the source feed identified and duplicate delivered scans collapsed to the earliest per parcel
One row per parcel with promised date, actual delivered timestamp in UTC, the lateness in hours, and an on-time flag
Retains the terminal and resolved timezone offset used for each scan so times trace back to source
Flags parcels whose terminal had no resolvable timezone so they are visible and handled consistently in the rate denominator
delivery_conformance.png
Visual
Deliver delivery_conformance.png, an annotated conformance figure for the service review.

Render a per-carrier on-time rate panel as bars with each carrier's rate labeled to one decimal and a horizontal reference line at the 95 percent contractual target
Add a dedup waterfall panel from the raw scan count down to the conformed one-row-per-parcel count, with a labeled step for the duplicate delivered scans collapsed
Add a lateness panel showing the distribution of lateness in hours across late parcels with the median lateness marked by a labeled line
Title the figure with the defensible overall on-time rate to one decimal and annotate the worst-performing carrier by name
on_time_summary.pdf
Text
Deliver on_time_summary.pdf for the service review.

State the defensible on-time delivery count and the on-time rate in percent to one decimal against the 95 percent target
Give the on-time count and rate broken out by carrier and name the worst-performing carrier
Report the median lateness in hours for late parcels and the count delivered more than 24 hours late
Report how many duplicate delivered scans were collapsed and how many parcels lacked a resolvable timezone, each a whole number, and how those were handled
Economics
We're assembling a single quarterly panel of real GDP growth across 14 countries from an annual IMF WEO extract, a quarterly national-statistics CSV in local currency, and a Eurostat file already in euros. The research team can't publish comparisons until the series sit on one common basis, and they will only publish if at least 90 percent of the 14-country-by-quarter grid is populated. They need the per-source input row counts to reconcile against the conformed observation count, the completeness rate for each country and for each year, the count and share of imputed cells disaggregated from annual versus observed native-quarterly cells, and the share of series successfully placed on the common base before they trust any cross-country claim.

Tell us how many country-quarter observations we end up with in a single conformed real-GDP panel.

gdp_panel_conform.py
Code
Please write gdp_panel_conform.py, which builds the panel and prints the coverage figures.

Converts local-currency series to the common base using the supplied FX and deflator tables and standardizes country ids to ISO3 via the lookup, and records the units and currency conformance rate as the percent of series successfully placed on the common base
Reconciles annual-versus-quarterly grain by keeping native quarterly where available and disaggregating annual only where flagged
Prints the per-source input row counts for IMF, national statistics, and Eurostat and the reconciliation delta between the summed source rows and the conformed observation count
Prints the total country-quarter observation count, the countries covered, the quarters spanned, and the overall grid completeness rate as a percent against the full 14-country grid, with an explicit pass or fail against the 90 percent coverage gate
Prints the count and share of imputed cells disaggregated from annual versus observed native-quarterly cells and the count of empty country-quarter cells
gdp_panel.csv
Data
Hand back gdp_panel.csv, the conformed quarterly panel.

One row per country-quarter on the common base with ISO3 identifiers and real GDP growth in percent to one decimal
Flags whether each observation is native quarterly (observed) or disaggregated from annual (imputed)
Carries the source (IMF, national statistics, or Eurostat) for each observation so the per-source counts reconcile
Uses a consistent quarter key so the panel is uniquely keyed on country-quarter with no duplicate cells
Carries the applied FX rate and deflator basis on each converted row so the currency conformance is auditable
gdp_coverage_dashboard.html
Visual
Deliver gdp_coverage_dashboard.html, a standalone multi-panel coverage dashboard.

Include a per-country completeness panel with one bar per country showing that country's share of populated quarters as a percent, countries ordered by completeness ascending, with a reference line at the 90 percent coverage gate
Include a per-year completeness panel with one bar per year showing the share of the country grid populated that year, each labeled
Include a stacked bar panel of conformed observations by source with one labeled segment each for IMF, national statistics, and Eurostat, and a callout of the summed-source-minus-conformed reconciliation delta
Include an imputed-versus-observed panel showing the count and share of imputed cells disaggregated from annual beside observed native-quarterly cells, each labeled
Add a findings callout stating the total country-quarter observation count, the countries covered, the quarters spanned, whether the panel clears the 90 percent coverage gate, and the country with the fewest populated quarters
conform_note.docx
Text
Add conform_note.docx summarizing the conformed panel and the reconciliation choices.

State the total country-quarter observation count, the number of countries covered, and the quarters spanned, each a whole number
Report the overall grid completeness rate as a percent against the full 14-country grid and whether it clears the 90 percent coverage gate, and name the country with the fewest populated quarters with its completeness rate
Report the imputed-versus-observed cell split as counts and shares and the count of empty country-quarter cells
Report the per-source input row counts for IMF, national statistics, and Eurostat and the summed-source-minus-conformed reconciliation delta
Name the FX and deflator base used to put the series on a common basis and report the units and currency conformance rate as a percent, listing any series that could not be placed on the common base
Economics
Labor-market microdata arrives as three annual survey waves whose industry codes switch classification vintages, whose education is coded categorically in two waves and as years-of-schooling in the third, and whose weight columns are named inconsistently. The team needs one pooled file before any weighted estimate can be trusted, plus the estimate by industry, the gap between the weighted and unweighted totals, and how much reclassification the crosswalk introduced.

Tell us the weighted total employed count from one pooled, harmonized person-level table.

labor_panel_conform.py
Code
Please write labor_panel_conform.py, which pools the waves and prints the employment figures.

Harmonizes industry codes to the 2017 scheme via the crosswalk and conforms education to a single categorical scheme across all three waves
Unifies the differently named weight columns into one consistent weight field
Prints the weighted total employed count and the same total broken out by harmonized industry and by wave
Prints the unweighted employed count alongside the weighted one so the weighting effect is visible, and the count of records whose industry code changed under the 2017 crosswalk
labor_panel_pooled.csv
Data
Hand back labor_panel_pooled.csv, the pooled person-level table.

One row per person-wave with 2017 industry codes, a single education scheme, and a unified weight column
Retains a wave identifier and the original pre-crosswalk industry code so each record traces back to its survey year
Includes a flag marking records whose industry code required crosswalking to the 2017 scheme
Includes an employed flag so the weighted and unweighted totals compute directly from the table
labor_harmonization_deck.pptx
Visual
Deliver labor_harmonization_deck.pptx, a short deck presenting the harmonized estimate.

A slide with paired bars of the weighted versus unweighted employed total so the weighting effect is visible, with each total labeled
A slide with the weighted employed count by harmonized industry, industries ordered by weighted count descending
A reclassification slide with a bar for the count of records whose industry code changed under the 2017 crosswalk against the count that did not, each labeled
A findings slide stating the weighted total employed count as the committed figure and naming the largest industry by weighted employment
harmonization_notes.docx
Text
Add harmonization_notes.md documenting how the three waves were reconciled.

State the weighted total employed count and the unweighted total employed count
Give the weighted employed count broken out by harmonized industry and by wave
Report the count of records crosswalked to the 2017 industry scheme and any industry codes with no clean crosswalk, each a whole number
Explain how education was mapped to a single categorical scheme and name the reference scheme used for the unified weight
Policy & Education
Enrollment data lands from 40 schools in a mix of XLSX rosters, fixed-width SIS text exports, and Google Form CSVs, with grade levels written every which way, an English-learner flag coded differently per source, and students who transferred mid-year appearing more than once. The district office needs one clean headcount by grade before state reporting, plus the English-learner count and a clear view of how much duplication the transfers introduced.

Tell us the reconciled total headcount by grade from one conformed enrollment table.

enrollment_conform.py
Code
Please write enrollment_conform.py, which conforms the 40 schools' files and reports the reconciled figures.

Standardizes the varied grade labels (K, KG, Kindergarten, 1, 1st, and so on) through the mapping and harmonizes the differently coded English-learner flags into one yes/no field
Resolves mid-year transfers by keeping the latest active record per state student id
Prints the reconciled total headcount by grade and the district-wide total after reconciliation
Prints the naive pre-dedup headcount alongside the reconciled one so the transfer inflation is visible, and the reconciled English-learner count district-wide and by grade
enrollment_conformed.csv
Data
Deliver enrollment_conformed.csv, the single conformed enrollment table.

One active record per student keyed on state student id with a standardized grade label and a harmonized English-learner flag
Sending school and source format retained so each record traces back to its roster
Includes an active-record flag so only the retained record per student is counted
Retains the original grade label and original English-learner code so the standardization is auditable
headcount_reconciliation.png
Visual
Deliver headcount_reconciliation.png, an annotated headcount reconciliation figure for the district office.

Render a grouped bar chart of headcount by grade showing the naive pre-dedup count beside the reconciled count for each grade
Overlay the reconciled English-learner count by grade as a distinct series on the same grade axis
Add a labeled callout for the district-wide naive-minus-reconciled difference in students attributable to collapsed transfer duplicates
Title the chart with the reconciled district-wide total headcount and annotate the grade with the largest transfer-duplicate correction
headcount_by_grade.docx
Text
Add headcount_by_grade.md summarizing the reconciled headcount and what was cleaned up.

State the reconciled total headcount by grade and the district-wide total, each a whole number
Report the naive-minus-reconciled headcount difference and the count of duplicate transfer records collapsed, each a whole number
State the district-wide English-learner count and the English-learner count by grade
Report the per-source-format record counts feeding the table and any grade labels that could not be mapped
Policy & Education
We're building a clean per-pupil expenditure table from a state finance file at fund-and-object grain, a federal grants CSV at award grain, and a district crosswalk, complicated by inconsistent district name spellings and districts that merged mid-period so old and new codes both appear. A separate enrollment file gives each district-year's pupil count. Finance needs the statewide total to tie out to the audited control figure, the statewide per-pupil figure, and the federal-versus-state composition.

Tell us the reconciled statewide expenditure total, tied to the audited control, from one conformed district-year table.

ppe_conform.py
Code
Please write ppe_conform.py, which builds the district-year table and prints the reconciled figures.

Resolves districts to their current code via the merge-history table so merged districts collapse correctly, matching on cleaned district names where codes are missing
Rolls state finance at fund-and-object grain and federal grants at award grain up to district-year grain and joins the enrollment file for pupil counts
Prints the reconciled statewide expenditure total in USD, the delta against the audited control figure, and the statewide per-pupil expenditure in USD
Prints the federal-versus-state split of the statewide total in USD and the count of districts affected by mid-period merges
ppe_district_year.csv
Data
Deliver ppe_district_year.csv, the conformed per-pupil expenditure table.

One row per district-year on current district codes with expenditures combined across state finance and federal grant sources and the district's pupil count attached
Carries a per-pupil expenditure column and the federal and state expenditure components separately
Shows the reconciliation delta against the audited control total in USD
Includes a name-resolution flag showing which rows were remapped from old codes or matched by name
ppe_reconciliation_deck.pptx
Visual
Deliver ppe_reconciliation_deck.pptx, a short finance deck on the reconciliation.

A reconciliation slide with a waterfall from the summed source expenditure to the reconciled statewide total, with a labeled step for the delta against the audited control figure
A composition slide splitting the statewide total into its federal and state components with the federal share labeled as a percent to one decimal
A per-pupil slide ranking district-years by per-pupil expenditure in USD, ordered descending, with the highest and lowest district-year annotated by name
A findings slide stating the reconciled statewide total in USD tied to the audited control as the committed figure
reconciliation_memo.pdf
Text
Deliver reconciliation_memo.pdf for finance.

State the reconciled statewide expenditure total in USD and the delta against the audited control
State the statewide per-pupil expenditure in USD and name the highest and lowest per-pupil district-year
Report the federal-versus-state composition of the total in USD and the federal share as a percent to one decimal
Count the districts affected by mid-period merges and any district names that could not be resolved to a current code, each a whole number
Demographic & Social Science
We're merging census tract data from two decennial extracts and one ACS file, but tract boundaries changed between vintages, so older tracts have to be brought onto current geography with the supplied population-weighted crosswalk. The race and ethnicity category schemes differ across sources and the grains do not match. The team needs one tract-level table on current boundaries before any spatial analysis, along with the population composition and a clear count of how many tracts split or merged.

Tell us the total reconciled population from a single tract-level table on current boundaries.

tract_conform.py
Code
Please write tract_conform.py, which reads the sources and prints the reconciled figures.

Applies the crosswalk with population-weighted allocation factors to bring older tracts onto the current geography
Conforms the differing race and ethnicity category schemes into one harmonized scheme and aligns the differing table grains
Prints the total reconciled population on current boundaries and the count of current-boundary tracts
Prints the population broken out by harmonized race and ethnicity category and the count of older tracts that were split versus merged onto current geography
tracts_current_geography.csv
Data
Hand back tracts_current_geography.parquet, the single tract-level table on current boundaries.

One row per current-boundary tract with harmonized race and ethnicity categories
Population allocated onto current tracts via the weighted crosswalk as whole-person counts that sum to the reconciled total
Carries a current-boundary tract id so each row is uniquely keyed to current geography
Retains the contributing source (decennial vintage or ACS) so allocated counts trace back to their origin extract
tract_reconciliation_dashboard.html
Visual
Deliver tract_reconciliation_dashboard.html, a standalone multi-panel reconciliation dashboard.

Include a bar panel of reconciled population by harmonized race and ethnicity category, categories ordered by population descending, with the largest group's share labeled as a percent to one decimal
Include a panel showing the count of older tracts split versus merged onto current geography, each labeled
Include a per-source panel of allocated population by contributing source, one bar for each decennial vintage and one for ACS
Add a reconciliation callout stating the total reconciled population and the count of current-boundary tracts, confirming the allocated whole-person counts sum to the reconciled total
reconciliation_note.docx
Text
Add reconciliation_note.md summarizing the reconciled table and the harmonization choices.

State the total reconciled population and the count of current-boundary tracts, each a whole number
Give the population by harmonized race and ethnicity category and name the largest group with its share in percent to one decimal
Report how many older tracts were split and how many were merged onto current geography by the crosswalk, each a whole number
List the harmonized race and ethnicity categories the schemes mapped into and name the crosswalk vintage used
Nonprofit & Grant-making
We're building a unified donor table from a CRM export, an online-donations platform CSV, and an events spreadsheet, where the same donor appears under slightly different names, emails, and addresses and gift dates come in mixed formats and timezones. Development needs a clean total raised before the fiscal-year close, along with the unique donor count, a new-versus-returning split, per-source reconciliation, and the total by fund.

Tell us the reconciled total raised for the fiscal year from one conformed donor-gift table.

donor_conform.py
Code
Please write donor_conform.py, which conforms the three sources and prints the reconciled figures.

Performs entity resolution using the supplied match keys and dedup rules so one donor is not counted three times
Normalizes gift dates across the differing formats and timezones to a single date and standardizes fund designations through the mapping
Prints the reconciled fiscal-year total raised in USD, the count of unique resolved donors, and the average gift in USD
Prints the total raised reconciled back to CRM, platform, and events contributions and the new-versus-returning donor split by both donor count and dollars
donor_gifts_conformed.csv
Data
Deliver donor_gifts_conformed.csv, the single conformed donor-gift table.

One resolved donor identity per person with each gift on a single normalized date and a standardized fund designation
Retains which source system each gift came from so the total reconciles back to CRM, platform, and events
Includes a resolved donor id so gifts group to one identity per person, plus a first-gift flag marking donors new this fiscal year
Retains the original name, email, and source gift date so each merge is auditable
donor_reconciliation.png
Visual
Deliver donor_reconciliation.png, an annotated reconciliation figure for development.

Render a source-reconciliation panel with one bar for total raised by CRM, platform, and events that together sum to the reconciled fiscal-year total, with the total marked by a labeled reference line
Add a new-versus-returning panel showing the split in both donor count and dollars raised as paired bars, each labeled
Add a labeled callout for the count of duplicate donor identities merged by entity resolution and the resulting count of unique resolved donors
Add a bar panel of total raised by standardized fund designation, funds ordered by dollars descending, and title the figure with the reconciled fiscal-year total raised in USD
donor_reconciliation_note.docx
Text
Add donor_reconciliation_note.md summarizing the reconciled total and how it ties out.

State the reconciled fiscal-year total raised in USD and the count of unique resolved donors
Reconcile the total back to CRM, platform, and events contributions, each in USD
Report the new-versus-returning donor split in both donor count and dollars raised
Report how many duplicate donor identities were merged and the average gift in USD, and give the total raised by standardized fund designation
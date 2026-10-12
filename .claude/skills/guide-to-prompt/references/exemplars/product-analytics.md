# Exemplars: Product Analytics

> 8 accepted tasks in this domain, sorted by the current model's measured mean, lowest (hardest) first. Each is the client's own record. Index and the shared architecture: `index.md`.

## Set the 2027 team plan transcription allowance at 500 minutes per seat per month

**SaaS Usage Allowance Pricing**, Batch 14, Product Analytics, model mean **0.2** over 4 runs (0.27, 0.32, 0.32, 0.32).

### What makes it strong (the client's note)

The trap is the obvious series: chargeable minutes over the seats listed on the usage statement, with every Team workspace in, matches only 27 of the 36 published months (nine miss by 0.1 minute) and sets 575, which Standard section 7.2 bars however small the difference.
Only one series matches all 36 published months: billable seat-months (trial and paused days out, days on hold in, partial months prorated) with Team workspaces whose top-level account holds a pooled minutes agreement left out. Either correction alone matches 0 of 36.
The computation chain runs from seat-level status spells and workspace billing start dates, through account-hierarchy roll-ups to the pooled agreements, to monthly series, three-year seasonal indices, the FY2026 level and growth factor raised to 1.5, and the policy's round-up to the next 25-minute step.
Determinism pins: FY2026 level 389.9 minutes, growth factor 1.070398 over the published FY2025 mean of 364.3, March 2027 peak 483.8 (8.8 above the 475.0 step down), Product Operations peak 568.0 and a gap of 84.2 minutes.

### Stakeholder ask (the prompt, verbatim)

The Pricing Council meets in September to set the Team plan's included transcription allowance for 2027, and what I have to bring it is one number: the transcription minutes each Team seat should include per month in 2027. Three views have already reached me. Product Operations has worked up a figure of its own, our enterprise sales lead would price off the spring run rate, and FP&A wants the launch quarter left out of the forecast. The recommendation goes out under my name as Wrenfield's VP for pricing and packaging, and Pricing Analytics will check it step by step before the Council sees it.

The billing audit for FY2026 is still open, so none of those months has a published figure and we have to compute them ourselves from the raw extracts: the monthly usage statements, the seat status log, the workspace directory and account records, the enterprise agreements register, and the published KPI series for FY2023 to FY2025. The metrics standard, the packaging policy and Pricing Analytics' method note came across with them, and all three apply as written.

Pricing Analytics works from team_allowance_forecast_2027.xlsx, so build it on live formulas that let them trace any figure back to the extracts. For every month of FY2023 to FY2025 I want the series you forecast from beside the published figure, with the gap between the two, and FY2026 carried on the same series below. After that come the seasonal indices, the level and the growth factor as the method note defines them, the twelve monthly forecasts for 2027, and the policy's rule applied to those forecasts, showing the forecast values at which the allowance would go one step up or one step down. Take the sales lead's run-rate approach and FP&A's launch-quarter approach all the way through to the allowance each of them produces.

The Council gets team_allowance_council_paper.pdf. The first thing it should read is the allowance you recommend, the 2027 month and forecast figure that drive it, and the forecast figure at which it would change. Take on the strongest competing proposal: why it should not be adopted, and the gap in minutes between its peak forecast month and yours. Include a chart of the monthly series running from FY2023 to the end of the 2027 forecast, with the published figures marked on it. Say in plain terms whether your series matches every published monthly figure, and list any month where it does not. Close with the allowance the sales lead's approach and FP&A's approach would each produce, and why you are not using either.

### Deliverables

`team_allowance_forecast_2027.xlsx`, `team_allowance_council_paper.pdf` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A software company's Pricing Council must set the Team plan's included transcription allowance per seat per month for 2027. The FY2026 months are unpublished while a billing audit is open, so the analyst must rebuild the published KPI (average transcription minutes per Team seat) from raw usage statements, the seat status log, the workspace directory, the account hierarchy and the enterprise agreements register, under a metrics standard that bars any series missing a published figure. The series then feeds the method note's seasonal-index forecast and the packaging policy's 25-minute step rule. Three competing views must be answered: Product Operations' 575-minute figure, the sales lead's spring run rate and FP&A's launch-quarter exclusion. Deliverables are `team_allowance_forecast_2027.xlsx` (live formulas traceable to the extracts: the series beside the published figure with gaps, FY2026 below, indices, level, growth, twelve forecasts, the step triggers, and both alternative approaches carried to an allowance) and `team_allowance_council_paper.pdf` (opening on the recommendation, the driving month and the change triggers, rebutting the strongest rival with the peak gap, a series chart with published points, the match statement, and the two alternative allowances).)

`17 files, 13.4 MB`, `account_hierarchy.json`, `allowance_forecast_method_note_2027_cycle.docx`, `billing_platform_release_notes_2025-26.md`, `data_platform_extract_field_reference.txt`, `email_sadowski_allowance_run_rate.txt`, `enterprise_agreements_register.xlsx`, `fpa_note_launch_quarter.txt`, `growth_dashboard_transcription_export.xlsx`, `metrics_definitions_and_reproduction_standard_2024.pdf`, `product_ops_allowance_prep_note.docx`, `published_kpi_series_fy2023_fy2025.csv`, `seat_status_events.csv`, `team_plan_packaging_policy_may2025.docx`, `team_plan_price_card_nov2025.pdf`, `transcription_usage_by_seat_month.csv`, `workspace_billing_holds.csv`, `workspace_directory.csv`

### Final recommendation

Set the 2027 Team plan included transcription allowance at 500 minutes per seat per month: the peak 2027 forecast month is March 2027 at 483.8 minutes, and the allowance would move to 525 above 500.0 and to 475 at or below 475.0.

### Step-by-step solution

1. Fix the quantity: average transcription minutes per Team seat for each month of 2027, with the allowance set by Policy section 3.1 from the highest month, rounded up to the next 25-minute step.
2. Take FY2023 to FY2025 from the published KPI series and compute the twelve FY2026 months, unpublished while the audit is open, on a series that reproduces the published months.
3. Test the series. Chargeable minutes over statement-listed seats with every Team workspace matches 27 of 36 published months. Counting each seat by its billable days (trial and paused days out, hold days in, partial months prorated) and leaving out Team workspaces whose top-level account holds a pooled minutes agreement matches all 36.
4. Compute FY2026 on that series: a mean of 389.9 minutes per seat against the published FY2025 mean of 364.3, a growth factor of 1.070398.
5. Build seasonal indices from FY2024, FY2025 and FY2026 and forecast each 2027 month as index times the FY2026 level times growth to the power 1.5: January 447.5, February 423.7, March 483.8, April 446.6, May 458.3, June 434.1, July 398.1, August 368.2, September 433.9, October 469.2, November 441.5, December 376.6.
6. Apply the policy: the March 2027 peak of 483.8 sets 500; the allowance would go to 525 above 500.0 and to 475 at or below 475.0.
7. Carry the alternatives through: Product Operations' statement-seat series peaks at 568.0 and sets 575 (84.2 minutes above the recommended peak); the sales lead's April to June run rate on the recommended series peaks at 501.3 and sets 525; FP&A's launch-quarter exclusion peaks at 491.7 and sets 500.
8. Build the workbook with the extracts held in it and the series, forecast and readings on live formulas, and write the council paper opening on 500, March 2027 at 483.8 and the triggers.

### Key traps (what the model did)

- Built the KPI series on the face-value denominator (seats listed on the usage statement, all workspaces in), saw it match only 27 of 36 published months, and shipped it anyway; one run papered over the gap by pasting the published values into the forecast column.
- Kept enterprise pooled-agreement workspaces in the population because they are Team workspaces on the statement, never rolling the account hierarchy up to the agreements register.

### Justification

The metrics standard admits only a series that gives back every published month, and the method note and policy fix the forecast and the step once the series is chosen. Billable seat-months with pooled-agreement workspaces left out is the only reading that returns all 36 published months, and on it the March 2027 peak is 483.8 minutes, which rounds up to 500. Product Operations' 575 rests on a series that misses nine published months, so the standard rules it out. The sales lead's run rate and FP&A's launch-quarter exclusion each break an explicit method rule, so neither replaces the method's forecast.

## Flag shipping service level for om-1015 Follow up

**E-commerce Contribution Margin Diagnostics**, Batch 14, Product Analytics, model mean **0.41** over 4 runs (0.99, 0.26, 0.26, 0.25).

### What makes it strong (the client's note)

The trap is that the standard never writes the formula: any single exposure view (orders, units or net sales at one month's margin) replays the 40 closed actions but puts 44 to 55 closed values in the neutral band instead of 45, and only the construction that takes the highest of the six view sums reproduces every control. Some of those single views flag customer grouping on OM-1015 instead.
Conformance is checkable and tight: 40 of 40 closed actions, batch qualifying counts 8, 9, 8 and 7, batch D most-adverse counts 4 and 3, and exactly 45 closed dimension-case values inside the -2.00 to +2.00 pp neutral band.
Determinism pins: shipping service level -1.250005 pp, transaction type -0.427332 pp, customer grouping +2.893991 pp; shipping service level clears the -1.00 pp line by only 0.25 pp, so early rounding or a wrong basis flips the call.
The binding view differs by dimension (orders on the reference anchor for customer grouping and transaction type, net sales on the review anchor for shipping service level), which a solver must accept as the output of one construction rather than a dimension-specific rule.

### Stakeholder ask (the prompt, verbatim)

We’re closing OM-1015 on the Golf Shoes purchase flow and I need a call I can take into review. Review the supplied MDS-5 materials and tell me what, if anything, we should flag for follow up. If one of the rostered dimensions clears the action standard, name it. If none does, leave OM-1015 unassigned.

I need a short rca_recommendation.pdf. Put the call up front, then show the Golf Shoes contribution margin in the reference month and review month and how far it moved. Give me a small decision table with the signed review value for each of the three rostered dimensions. For the closed history, add a four-row batch check: for each archive batch A through D, report the dimension with the lowest aggregate signed review value across that batch’s ten closed reviews and the aggregate itself. Include the closed replay match count as well.

For the current case, I also want to see what is pushing the call without turning the memo into a dump of every cell. For the dimension you flag and the runner up, name the single largest adverse value-level contribution and the single largest offsetting contribution, with the percentage-point contribution for each.

The other file is rca_visuals.png. Keep it simple: one bar for each rostered dimension’s OM-1015 review value, the -1.00 pp action line, and the selected dimension and runner up easy to identify. Label the three bars with their values.

Keep full precision for anything that affects the decision; two decimals in the finished files is fine.

### Deliverables

`rca_recommendation.pdf`, `rca_visuals.png` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A product analytics lead is closing review OM-1015 on the Golf Shoes purchase flow and needs a call for review: flag one of three rostered dimensions (customer grouping, transaction type, shipping service level) if its MDS-5 review value is at or below -1.00 pp, or leave the case unassigned. The MDS-5 standard defines the metric, case population and action rule but not the review-value formula; the analyst must reconstruct a single parameter-free construction from DataCo monthly aggregates that reproduces all 40 closed actions and the coarse legacy QA controls, then apply it unrounded to OM-1015. Deliverables are `rca_recommendation.pdf` (call first, Golf Shoes contribution margin in 2016-10 and 2017-09 and the change, a three-row decision table, a four-row archive batch check with the lowest-aggregate dimension and value per batch, the closed replay match count, and the largest adverse and offsetting value-level contributions for the flagged dimension and runner up) and `rca_visuals.png` (three labeled bars with the -1.00 pp action line and the selected and runner-up dimensions marked).)

`15 files, 1.2 MB`, `00_source_provenance.txt`, `01_monthly_category_totals.csv`, `02_monthly_dimension_cells.csv`, `03_review_register.csv`, `04_dimension_roster.csv`, `05_closed_review_outcomes.csv`, `06_metric_dictionary.csv`, `07_review_standard.txt`, `08_source_dictionary.csv`, `09_reporting_rules.txt`, `10_review_scope.json`, `11_lineage.json`, `12_closed_review_notes.txt`, `13_archive_controls.json`, `99_file_manifest.json`

### Final recommendation

Flag shipping service level for OM-1015 follow up; it is the only rostered dimension at or below the -1.00 pp action standard (-1.25 pp), with transaction type (-0.43 pp) the runner up and customer grouping (+2.89 pp) not qualifying.

### Step-by-step solution

1. Reconcile the review register, dimension roster, closed outcomes, MDS-5 standard, archive controls, and reporting rules; confirm OM-1015 (Golf Shoes, 2016-10 to 2017-09) and the 40 closed reviews in batches A to D.
2. For each case and rostered dimension, keep every dimension value seen in either month, zero-filling missing months and setting zero-net-sales cell margins to zero.
3. For each exposure basis (orders, units, net sales), compute each value's share change between months and value it at the reference-month and at the review-month cell contribution margin, giving six candidate sums per dimension; take the highest unrounded sum as the review value.
4. Replay the closed history with that one construction: it matches 40 of 40 closed actions, the batch qualifying counts (8, 9, 8, 7), the batch D most-adverse counts, and the 45 neutral-band values.
5. Apply it to OM-1015: shipping service level -1.250005 pp, transaction type -0.427332 pp, customer grouping +2.893991 pp. Only shipping service level is at or below -1.00 pp.
6. Compute Golf Shoes contribution margin from monthly totals: 20.81% in 2016-10 and 10.87% in 2017-09, a -9.93 pp change.
7. Aggregate the closed review values by batch: lowest is A customer grouping +4.25 pp, B transaction type +14.57 pp, C transaction type +34.55 pp, D customer grouping +66.80 pp.
8. On the binding view, report value-level extremes: shipping service level Same Day -2.79 pp adverse and First Class +2.70 pp offsetting; transaction type TRANSFER -4.84 pp adverse and PAYMENT +2.40 pp offsetting. Build the memo and the three-bar chart.

### Key traps (what the model did)

- Recovered a review-value construction that replayed the 40 closed actions (claimed 40/40) but did not reproduce the coarser archive controls. The batch aggregates came out with the wrong sign and dimension (e.g. batch A -14.89 vs +4.25). Applied to OM-1015, this put customer grouping at -3.94pp, and that run flagged it. Stopped at the first construction that passed the action-level replay.

### Justification

MDS-5 leaves the review-value formula to be recovered from legacy evidence, and the closed actions plus the archive controls pin it to one construction: share change on each exposure basis valued at each month's cell margin, keeping the highest sum. That construction replays all 40 closed actions and every coarse count, including the 45 neutral-band values, so it is the conforming reading of the standard. Applied unrounded to OM-1015, it puts shipping service level at -1.25 pp, the only dimension past the -1.00 pp line, while transaction type at -0.43 pp falls short and customer grouping is favorable. The 9.93 pp margin drop in Golf Shoes is real, but only the shipping service level mix shift clears the action standard, driven by Same Day orders and partly offset by First Class.

## Staff the fy26 pod on county sheriffs, whose detention authorities lift the county seat market to 142,288

**Go-to-Market Vertical Selection**, Batch 14, Product Analytics, model mean **0.47** over 4 runs (0.44, 0.60, 0.52, 0.42).

### What makes it strong (the client's note)

Two traps stack. The workbook's 21.3% Campus growth comes from an unbalanced panel (same-store growth is under 5%), and the docket's officer-only universe makes State the only vertical that clears 25,000 (117,850 seats against County 23,788 and Campus 22,539).
The County win only appears after finding 700 county-type agencies with civilian staff and zero sworn officers (133,517 civilians in 2024), which the docket's "officer count above zero" filter removes.
The DT-03 Detention Operations closure looks like it kills those seats; the billing shows fourteen accounts carrying the same 959 seats from DT-03 to FS-01 at FY25Q3 and two new detention logos signing on FS-01 after 2025-07-01 for 141 seats.
Determinism pins: attach 0.300 (County), 1.133 (State), 1.320 (Campus) seats per officer on post-closure signings; 0.896 seats per civilian for the sixteen detention accounts (1,100 on 1,228); 132,289 uncovered detention civilians; County 142,288 against State 117,850, a 20.7% lead.

### Stakeholder ask (the prompt, verbatim)

I run product analytics at Shiftline, the workforce-operations platform law-enforcement agencies use to schedule and manage their personnel, licensed per active seat. Our FY26 plan funds exactly one new-vertical sales pod, and leadership locks the vertical this week: County Sheriffs, State Agencies, or Campus Safety. Recommend which vertical gets the pod, one committed call, no splits.

### Deliverables

`answer.md` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (Shiftline sells per-seat workforce scheduling to law-enforcement agencies, and its FY26 plan funds exactly one new-vertical sales pod. Leadership locks the vertical this week and must choose County Sheriffs, State Agencies, or Campus Safety, with one committed call and no splits. The pack holds an FBI UCR agency-year employee panel, the agency directory, the installed account book with quarterly billing lines, FY25 expansion signings, the product catalog, a GTM sizing workbook that ranks Campus first on officer growth, and a pod docket that sets the objective as FY26-27 serviceable seats at current list rates against a 25,000 net-new seat target. The analyst must replace the growth ranking with a seat sizing, audit the docket's officer-only target universe, recognize the county detention authorities it drops, test whether their seats survive the DT-03 closure, and commit the pod. The deliverable is the recommendation itself; no file is named.)

`16 files, 6.7 MB`, `agencies.csv`, `agency_types.csv`, `billing_line_items.csv`, `customer_accounts.csv`, `data_dictionary.json`, `employees_by_agency_year.csv`, `fbi_nibrs_user_manual_2021-1.pdf`, `fy25_expansion_cohort.csv`, `fy26_pod_docket.xlsx`, `gtm_sizing_workbook.xlsx`, `ops_review_thread.md`, `overview.xlsx`, `population_groups.csv`, `product_catalog.csv`, `states.csv`, `years.csv`

### Final recommendation

Staff the FY26 new-vertical sales pod on County Sheriffs, rejecting State Agencies and Campus Safety. Counting the county detention authorities, County holds 142,288 serviceable seats against 117,850 for State and 22,539 for Campus.

### Step-by-step solution

1. Inventory the pack: agency-year employee panel, agency directory, product catalog, installed accounts, billing lines, FY25 expansion signings, sizing workbook, pod docket, data dictionary, and the UCR manual.
2. Reproduce the sizing workbook. Campus ranks first on raw 2021 to 2024 officer growth (21.3%), but on a same-store basis it falls to under 5%, because most of the gain is agencies joining the panel.
3. Set growth aside. The docket's objective is FY26-27 serviceable seats at current list rates against a 25,000 net-new target.
4. Size each vertical on post-2025-07-01 signings (0.300, 1.133, and 1.320 seats per officer) applied to officers at agencies that are not already accounts: State 117,850, County 23,788, Campus 22,539. Only State clears 25,000 on this basis.
5. Rebuild the docket universe: every in-scope agency with 2024 sworn officers above zero (2,734 County, 761 State, 801 Campus). Check what that filter removes.
6. Find 700 county-type agencies reporting civilian staff and no sworn officers, holding 133,517 civilians in 2024. They are absent from every docket count.
7. Test whether they are sellable. Fourteen long-standing accounts billed DT-03 through FY25Q2 and the same 959 seats on FS-01 from FY25Q3. Two more signed on 2025-07-18 and 2025-09-16 and bill FS-01 at list, 141 seats on 154 civilians.
8. Take the detention attach: 1,100 seats on 1,228 civilians, 0.896 per civilian. Sheriff accounts carry no DT-03 at any date, so the sheriff 0.300 per officer is a patrol rate.
9. Apply 0.896 to the 132,289 uncovered detention civilians and add the sheriff patrol market: County 142,288 seats against State 117,850 and Campus 22,539, a County lead of 20.7%.
10. Commit the pod to County Sheriffs.

### Key traps (what the model did)

- Located the ~700 zero-sworn county detention authorities (133,517 civilians) but excluded them from the County market, keeping the docket's officer-count>0 universe, so State (~118k seats) beat County (~27k) and was recommended.
- Read the DT-03 Detention Operations SKU closure as making detention seats unsellable, without following the billing records showing accounts migrating seats intact to FS-01 and new detention logos signing on FS-01 after closure.

### Justification

Shiftline licenses a seat per scheduled person, so the pod should go where the current catalog reaches the most schedulable people. State leads only while the county market is defined as the docket's officer-only list, which by construction excludes every jail authority, since they report no sworn officers. Those 700 agencies employ 133,517 civilians who work rostered shifts. The DT-03 closure ended a module, not the business: existing detention accounts moved their seats intact to FS-01, and new detention logos have signed on FS-01 since the closure. Counting them at their observed 0.896 seats per civilian puts County at 142,288 seats, ahead of State by 20.7%. Campus misses the 25,000 target on every basis.

## Fund lc-12 Time-deposit rescue for the q1 lifecycle budget, not the win-back list

**Lifecycle Campaign Prioritization**, Batch 14, Marketing & Sales, model mean **0.5** over 4 runs (0.54, 0.58, 0.54, 0.55).

### What makes it strong (the client's note)

The trap is the win-back list: the CSV event parts alone stop covering most of the panel from July to October, so 221 members look dormant; with the JSONL archive unioned and confirmed by the device session log, only 15 went ninety days quiet and returned, 12 of them contactable, for 0.54 expected conversions.
A second collector, the web-tag-v2 export, mirrors time-deposit screens and relabels many as completions (94% completion against 56% in the primary log); counting it drops LC-12 to 3.00 and hands the call to LC-14.
Malformed rows must be recovered: 250 views named only in free-text notes, page paths in the token field, and 570 rows whose actor is a session token resolved through device_sessions_2018.tsv.
Determinism pins: LC-12 187 entered, 105 opened, 82 eligible, 71 contactable at 10.0% for 7.10; LC-14 189 contactable at 2.2% for 4.16 (a 70.8% lead for LC-12); LC-16 14 contactable at 18.0% for 2.52; LC-11 12 at 4.5% for 0.54.

### Stakeholder ask (the prompt, verbatim)

We lost a big chunk of monthly actives on the web app mid-year, and growth put together a win-back list from everyone who went quiet. Now they want the whole Q1 lifecycle budget pointed at that list and I've got to sign off or kill it by Thursday. So tell me straight, fund it or not, and why, no hedging.

Give me a one-page memo, decision_memo.pdf. Lead with whichever campaign you're recommending and the number that made the call, then back it up with whatever two or three numbers a skeptical VP would push back on first. Put a small bar chart on the page too, expected conversions for each campaign on the shortlist, so the gap is obvious at a glance.

### Deliverables

`decision_memo.pdf` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A bank's growth team wants the whole Q1 lifecycle budget pointed at a dormant win-back list built after a mid-year drop in web app actives, and the decision owner must fund it or kill it in favor of exactly one campaign from a closed four-campaign shortlist. The lifecycle brief fixes the audience rules for each campaign (any step of a flow counts, on any interface, and only currently subscribed, non-internal panel members are contactable) and defines expected incremental conversions as eligible contactable audience times the campaign's pilot response rate. The analyst works from web event logs delivered as CSV parts and a JSONL archive, a web-tag-v2 collector export, device sessions, CRM contacts and an identity crosswalk, internal accounts, a pilot readout, the shortlist roster, a growth Slack export and reference dimensions. The deliverable is `decision_memo.pdf`, a one-page memo that leads with the recommended campaign and its deciding number, gives two or three supporting numbers for a skeptical VP, and carries a bar chart of expected conversions for each shortlisted campaign.)

`18 files, 47.3 MB`, `campaign_pilot_readout.tsv`, `campaign_shortlist.csv`, `conversions_2018.csv`, `crm_contacts.csv`, `crm_identity_crosswalk.csv`, `device_sessions_2018.tsv`, `events_web_2018_archive_a.jsonl`, `events_web_2018_archive_b.jsonl`, `events_web_2018_archive_c.jsonl`, `events_web_2018_part01.csv`, `events_web_2018_part02.csv`, `events_web_2018_part03.csv`, `events_web_2018_part04.csv`, `events_web_2018_tagv2_export.jsonl`, `growth_slack_export.txt`, `internal_accounts.csv`, `lifecycle_brief.md`, `reference_dimensions.sqlite`

### Final recommendation

Fund LC-12 Time-Deposit Rescue as the single Q1 lifecycle campaign, at 7.10 expected incremental conversions (71 contactable members at a 10.0% pilot rate), and do not fund the LC-11 Dormant Win-Back list, which yields 0.54.

### Step-by-step solution

1. Union both event log deliveries (628,208 CSV rows and the 168,496-row JSONL archive) over the 381-member panel, and exclude the web-tag-v2 mirror export.
2. Recover malformed rows: map 250 note-only views through their notes, page paths through the page dimension, and 570 session-token actors through device_sessions_2018.tsv.
3. Size LC-11: 15 members went ninety or more days without activity and returned (not the 221 on the shortlist); 12 are contactable.
4. Size LC-12: 187 members reached a step of the time-deposit flow, 105 opened a deposit, 82 are eligible and 71 are contactable.
5. Size LC-14 on web and legacy loan-application screens: 189 contactable members who never submitted.
6. Size LC-16: 266 of 296 entrants completed a third-party transfer, leaving 14 contactable.
7. Apply contactability (current subscribed marketing record, bank-operated accounts excluded) and the Q4 2018 pilot readout rates: LC-12 10.0%, LC-14 2.2%, LC-16 18.0%, LC-11 4.5%.
8. Compute expected conversions: LC-12 7.10, LC-14 4.16, LC-16 2.52, LC-11 0.54.
9. Recommend LC-12 and write the one-page memo with the ranked table and the bar chart.

### Key traps (what the model did)

- Defused the headline decoy (killed the win-back list, LC-11 at 0.54) but mis-built the other campaign audiences. LC-12's contactable audience came out at 16-23 instead of 71, because malformed time-deposit rows (views only in free-text notes, paths in the token field, session-token actors) were not recovered and the tag-v2 mirror was not explicitly excluded. Runs then funded LC-16 (audience inflated to 52, 9.36 conv) or LC-14.

### Justification

The brief fixes the audiences, contactability and the conversion measure, so the decision is the ranking of expected conversions. Once the event log is read whole and the mirror collector is excluded, the win-back cohort shrinks from 221 to 15 members and finishes last, while LC-12 leads at 7.10 expected conversions against 4.16 for the runner-up LC-14. Funding the win-back list would spend the whole budget on a cohort that is largely an artifact of missing log coverage.

## Fix the approval-gated connection stall in three scoped parts and keep the listing, setup and enablement plan as they are

**SaaS Trial Activation**, Batch 14, Product Analytics, model mean **0.52** over 4 runs (0.49, 0.68, 0.48, 0.49).

### What makes it strong (the client's note)

The trap is composition: the blended rate falls only 7.7 points because the marketplace channel grew a segment that used to activate better, while like for like the fall is 16.4 points and sits entirely in approval-gated trials (52.7 to 8.9 percent).
The rival stories each have a surface case, and each is refuted by its own data: the guided setup holdout shows no difference, the sync defect is worth about 1.2 blended points and was already fixed, and marketplace trials activate no worse within segment.
The obvious remedy, restoring the legacy token connection, is cut down twice: the provider withdrew it for Forgeline Cloud (71.0 percent of the segment), and the organisation grant audit removes another 19.4 percent, leaving 9.7 percent restorable rather than the 29.0 percent the host list suggests.
The security standard opens the command-line token exception only where the provider withdrew the method, so the remaining 19.4 percent needs a third treatment, the measured organisation-credential outreach route.

### Stakeholder ask (the prompt, verbatim)

Subject: activation is down and I have four people telling me four different things. Our 14-day activation rate on new trial workspaces has been falling all year and it is the first thing the board asks about. Growth says the DevTools Hub listing is filling the funnel with trials that never activate and wants to pause it; Platform wants both of the summer platform releases rolled back; Onboarding says the guided setup redesign is the problem and wants it reverted; and Solutions wants to put every new trial through assisted onboarding, which means re-tasking the enablement team for the quarter. I have put everything we hold into the attached export: the product event history, the trials and organizations exports, the connection and support logs, the release history, our measurement and security standards, the marketplace agreement, the enablement plan and Growth's own read. Work it end to end and tell me what actually caused the fall and what it is worth, what we should do about it, and where the number lands by the end of December; and if the right answer is a shaped version of one of those four rather than any of them as pitched, say so plainly.

Please give me back two things. quill_activation_by_month.csv - one row per calendar month of 2027 with new trial workspaces, the number activated within 14 days, the rate as we report it today and the rate on a like-for-like basis, plus projected rows for October, November and December under the action you recommend and under doing nothing, and a total row for the quarter. quill_root_cause_memo.pdf - a short memo with one chart of the monthly rate on both bases, the cause and what it is worth in points, what you rule out and why, the action you recommend and exactly what it is scoped to, where the rate and the number of activated workspaces land in Q4 under it, the planning input the answer is most sensitive to, and what we should not lean on.

### Deliverables

`quill_activation_by_month.csv`, `quill_root_cause_memo.pdf` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (The head of a developer-documentation SaaS product is watching 14-day trial activation fall through 2027 while four teams push four fixes: pause the DevTools Hub marketplace listing, roll back the summer platform releases, revert the guided setup redesign, or put every trial through assisted onboarding. The analyst must clean the export (drop the re-sent supplementary batch, read only complete-window cohorts, exclude pilot and playbook cohorts), build the segment that actually broke by joining organisation app-approval policy to creator role, date the break to the Connect v3 release, size it on a like-for-like basis, refute each rival story with its own evidence, and then scope a remedy that the provider bulletin, the connector support matrix, the organisation grant audit and the security standard allow. The Q4 landing must be projected under the measurement standard's planning rules. Deliverables are `quill_activation_by_month.csv` (one row per 2027 cohort month with new trials, activated count, reported and like-for-like rates, then October to December under the recommended action and under doing nothing, plus a quarter total) and `quill_root_cause_memo.pdf` (a short memo with one chart of the monthly rate on both bases, the cause and its size in points, what is ruled out, the scoped action, the Q4 rate and activated count, the most sensitive planning input and what not to rely on).)

`19 files, 13.4 MB`, `SEC-2027-04_connection_security_standard.pdf`, `devtools_hub_listing_agreement.pdf`, `forgeline_platform_bulletin_2027-07.pdf`, `growth_readout_2027-09.docx`, `platform_incident_review_INC-2027-0533.pdf`, `quill_connector_support_matrix.xlsx`, `quill_data_dictionary.md`, `quill_enablement_capacity_plan_2027Q4.xlsx`, `quill_experiment_guided_setup_v4.json`, `quill_measurement_standard_2027H2.pdf`, `quill_organisations_2027.csv`, `quill_paid_conversion_2027.csv`, `quill_release_changelog_2027.md`, `quill_repo_connection_attempts_2027.csv`, `quill_support_tickets_2027Q3.csv`, `quill_sync_error_log_2027.csv`, `quill_weekly_activation_summary.xlsx`, `quill_workspace_events_2027.csv`, `quill_workspaces_2027.csv`

### Final recommendation

Fix the Connect v3 approval stall in three scoped parts: restore the legacy token connection for the 9.7 percent of approval-gated trials where it is still permitted, issue quill push service tokens to the 71.0 percent on Forgeline Cloud, and route the remaining 19.4 percent to organisation-credential outreach. Do not pause the DevTools Hub listing, revert guided setup v4 or re-task the enablement team; Q4 lands at 42.2 percent and 4,487 activated workspaces against 32.2 percent and 3,428 with no action.

### Step-by-step solution

1. Drop the 1,477 workspace rows and 4,202 event rows of supplementary batch EXP-20270930-B, which re-send primary records, leaving 24,870 trials and 91,030 events.
2. Apply QMS-2027-H2: activation is the first doc_published within 14 elapsed days; read cohorts created on or before 16 September; exclude the May assisted-onboarding pilot and the 300 August support-playbook trials from rates of record; use the fixed February to April and June to August windows.
3. Reproduce the headline (45.5 to 37.8 percent, 32.2 percent in September), then standardise on September's composition: 47.9 to 31.4 percent, a 16.4-point fall. Decompose into -2.7 points within segment, +1.1 composition and -6.0 interaction.
4. Define approval-gated trials by joining the organisation's app_approval_policy (restricted, any spelling) to a non-admin creator_role. The segment fell from 52.7 to 8.9 percent and grew from 6.8 to 37.6 percent of trials; every other trial moved from 44.9 to 46.3 percent.
5. Confirm the mechanism: from release 2027.5.2 on 18 May every approval-gated trial carries a pending_org_approval connection attempt, and none of the rest do.
6. Rule out the rivals: the guided setup holdout arms are 0.0 points apart; the sync defect cost about 1.2 blended points and was fixed on 4 August; marketplace trials run +1.0 and +4.1 points within segment; assisted onboarding lifts the gated segment by only 6.3 points; the listing cannot be paused before 6 April 2028, and pausing it would cut 1,406 activated workspaces.
7. Size the restore on both conditions: the code host still supports the method (29.0 percent of the segment) and the organisation grant is in force per the grant audit, leaving 9.7 percent.
8. Give the 71.0 percent on Forgeline Cloud a quill push service token under SEC-2027-04 clause 5.2(b), and send the 19.4 percent on supported hosts with revoked or lapsed grants to the organisation-credential outreach route.
9. Plan each part at its own measured rate (57.1, 33.3 and 32.4 percent) on September's composition and the 10,630-trial Q4 plan: 42.2 percent and 4,487 activated workspaces, against 32.2 percent and 3,428 with no action. Any two of the three parts land at 40.5 percent or below.
10. Run the ten-percent one-at-a-time sensitivity: the activation rate of trials outside the gated segment moves the projection most, by about 2.9 points.
11. Write the monthly CSV with actual, projected and total rows, and the memo with the two-basis chart, the ruled-out stories, the scoped action, the Q4 landing, the sensitivity and the sources not to rely on.

### Key traps (what the model did)

- Found the composition effect and the approval-gated cause, and correctly cut the legacy-token restore down, but recommended only two of three parts: the residual segment (revoked/lapsed org grants, 19.4%) was left with 'no treatment' or unallocated, so Q4 projection landed at 37.3-37.4% instead of 42.2%.

### Justification

The fall comes from one segment and one release. Approval-gated trials collapsed at Connect v3 while every other trial held steady, and the segment's growth through the marketplace channel turned a contained break into the headline decline. None of the four proposals reaches that mechanism as pitched. A plain rollback is not permitted for Forgeline Cloud and is blocked by revoked grants elsewhere, so the fix has to follow the three-way split that the provider bulletin, the grant audit and the security standard impose, with each part planned at the rate its own route has achieved. Done that way, it gains 1,059 activated workspaces in Q4 at no incremental cost and beats the best named alternative by 4.5 points. Pausing the listing raises the rate only by shrinking the denominator and is barred by contract.

## Merge the copied prospecting campaigns on 1 july instead of reverting the anvil bid change

**Paid User Acquisition**, Batch 14, Product Analytics, model mean **0.58** over 4 runs (0.71, 0.72, 0.55, 0.45).

### What makes it strong (the client's note)

The trap is the dated change everyone can see: Anvil iOS cost per thousand rose 9.8% across the 6 March bid switch, but campaigns that never switched rose 4.0% in the same weeks, so value bidding explains only 5.6% and reverting it leaves most of the rise in place.
The real driver only appears when campaigns are grouped by network, platform, age band and metro set rather than by name: 49 sets holding 99 live campaigns, carrying 17.1% of Anvil and Prism prospecting spend in January and 62.0% in May.
The cost of a live copy has to be priced from the account's own history: in the seven 2027 same-targeting merges in the change log, the surviving campaign's cost per thousand fell to 78.0% of its prior level on a 14-day window (a 28.1% premium; other defensible windows give 27.9% to 29.9%), while cross-age-band pauses and plain budget raises moved nothing.
The cost per new payer walk depends on a long chain of basis rules: invoiced spend net of credits and the Prism rebate with Corridor's fee included, Corridor impressions from invoice lines, MMP installs deduplicated by device and install time, first-ever payers checked against the archive and the 14-day refund window, and Denver account days throughout.

### Stakeholder ask (the prompt, verbatim)

Cost per new payer came in higher in May than in any month this year, and the board sees it again in July. The board note already has us reverting the Anvil bid change; I would rather make the change the numbers actually support, even if what they support is telling Noor that nothing in the accounts needs to change. I lead growth, so this one is mine, and it is one call: the single change we make to the paid accounts on 1 July.

Lucía loads it that morning from july_1_account_changes.csv, one row for every campaign the change touches, what happens to it, and its daily budget now and from the first, in whole dollars.

The case for it goes on one page for the June review, growth_review_june.html. Open on the change, then what is driving the rise and what May's cost per new payer would have come in at with the change already made, to the nearest ten dollars. For Anvil and for Prism separately, give the share of May's prospecting clicks that went through the campaigns it touches, to one decimal of a per cent. Marcus wants the walk from January's cost per new payer to May's: both months and every step to the cent. Under it, a chart of weekly cost per click from the first week of January, the campaigns the change touches against everything else, with the bid switch and the spring creative launch drawn in at their dates and the call in the title.

Two tables close the page. Finance sets Q3 network budgets off install cohorts, so for each install month from November to April, each network's prospecting installs, the new payers those installs produced, and the cost per new payer in whole dollars. And for the expansion shortlist, the ten launch groups with the fewest May prospecting installs per 100,000 adults aged 18 to 54, each with its May installs, its May new payers, its adults and that rate to one decimal.

### Deliverables

`july_1_account_changes.csv`, `growth_review_june.html` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A dating app's head of growth has watched cost per new payer climb from $128.85 in January to $168.90 in May, and the board note already commits to reverting the March Anvil value-bidding switch on 1 July. The analyst has to pick the single change to the paid ad accounts that the data supports, working from invoices, three networks' delivery reports, the campaign registry and geo lists, the change log, the MMP install export, store subscriptions, refunds, the pre-cutover billing archive, and Census metro population estimates, all under the growth KPI sheet's definitions. Two files are due: `july_1_account_changes.csv`, the load file listing every campaign the change touches with its action and its daily budget now and from 1 July in whole dollars, and `growth_review_june.html`, a one-page review that opens on the change, names the driver, gives May's cost per new payer with the change already made (to the nearest ten dollars), Anvil's and Prism's May prospecting click shares through the touched campaigns, the five-step January to May walk to the cent, a weekly cost per click chart with the bid switch and creative launch marked and the call in the title, a November to April install cohort table by network, and the ten launch groups with the fewest May prospecting installs per 100,000 adults aged 18 to 54.)

`26 files, 46.3 MB`, `CBSA-EST2023-AGESEX.pdf`, `account_devices.parquet`, `anvil_daily_performance.csv`, `ap_invoice_lines.csv`, `app_release_notes.md`, `board_growth_note_2028-05.pdf`, `campaign_change_log.csv`, `campaign_geo_targets.csv`, `campaign_registry.csv`, `cbsa-est2023-agesex.csv`, `corridor_daily_delivery.csv`, `creative_catalog.csv`, `data_dictionary.md`, `export_manifest.csv`, `growth_kpi_definitions.md`, `growth_sync_thread.md`, `growth_weekly_dashboard_2028-06-05.xlsx`, `metro_launch_schedule.csv`, `mmp_install_log.csv`, `network_settings.json`, `prism_daily_performance.csv`, `store_refunds.csv`, `store_subscriptions.csv`, `subscription_history_archive.parquet`, `tracking_links.csv`, `ua_account_runbook.md`

### Final recommendation

On 1 July, merge the copied prospecting campaigns on Anvil and Prism: pause the 50 campaigns that repeat another live campaign's network, platform, age band and metro set and move each budget to the longest-running campaign in its set (49 budget changes). Do not revert the Anvil bid change.

### Step-by-step solution

1. Build January and May on the KPI sheet's basis: invoiced prospecting spend (Anvil's 9 to 10 May delivery credit and Prism's volume rebate netted, Corridor's platform fee included, re-engagement excluded), network impressions and clicks with Corridor taken from its invoiced delivery lines, MMP installs counted once per device and install time, trials and first-ever payments from the store with the pre-cutover archive and the 14-day refund window applied, all on Denver account days and credited through the install of record. January is $222,400.62 over 1,726 new payers ($128.85); May is $342,870.59 over 2,030 ($168.90).
2. Walk the change one factor at a time in the KPI sheet's order: cost per thousand impressions +$24.16, impressions per click -$0.36, clicks per install +$0.47, installs per trial +$6.32, trials per new payer +$9.47. Impression prices carry most of the rise.
3. Test the bid switch: Anvil iOS prospecting cost per thousand rose 9.8% across 6 March, against 4.0% for campaigns that never switched, leaving 5.6% for value bidding.
4. Group every prospecting campaign by network, platform, age band and geo-list metro set. 49 sets hold two or three live campaigns, the copies launched from October with fresh creative. They carried 17.1% of Anvil and Prism prospecting spend in January and 62.0% in May.
5. Price a live copy from the change log: in seven 2027 pauses whose budget moved at the same timestamp to a campaign with identical targeting, the survivor's cost per thousand fell to 78.0% of its prior level on a 14-day window (a 28.1% premium; other defensible windows give 27.9% to 29.9%) with click-through unchanged. Three cross-age-band pauses and nine large budget raises moved nothing.
6. Check the rival readings: same-metro campaigns without a copy priced 7.3% higher in May than January against 29.8% for the copied ones; Spring 28 click-through decays on Winter 28's curve; the 3-day trial lowers conversion modestly (31.1% vs 33.5%) and shows only in the last walk step.
7. Apply the change to May: removing the premium on contested impressions with spend held puts May at $149.77, or $150 to the nearest ten dollars.
8. Write the load file (50 pauses naming their survivor, 49 survivors set to their set's summed daily budget) and the review page with the walk, the weekly cost per click chart (touched campaigns 42% above everything else by the week of 29 May), the cohort table and the expansion shortlist (Boston lowest at 5.6 per 100,000 adults).

### Key traps (what the model did)

- Rejected the bid-revert lure 4/4, but never priced the copy premium from the account's own natural experiments (the seven same-targeting merges in the change log), so the counterfactual came out $160 instead of $150 and the premium was missing or 37%.
- Under-scoped the copy sets: grouped only recent (Jan+) or 'fragmented launch' overlaps, giving 42-46 survivors / 84 rows instead of 49 sets / 99 campaigns, and wrote 'pause' without a zero budget.

### Justification

Cost per thousand impressions drives most of the January to May rise, and that price increase is concentrated in campaigns that share exact targeting with another live campaign on the same network. Their share of prospecting spend went from 17.1% to 62.0%, and the account's own 2027 merges show a copy adds 28% to the price of every impression. The bid switch explains only 5.6% on Anvil iOS once the trend in unswitched campaigns is netted out, and creative wear, the shorter trial and category inflation together explain little of the gap between copied and uncopied campaigns. Merging the copies is the one account change that removes the premium, and doing so would have put May at $150 per new payer instead of $168.90.

## Order 1,298 Top dog kits split 749 dog, 353 Cat, 196 Other

**Loyalty Program Operations**, Batch 14, Product Analytics, model mean **0.58** over 4 runs (0.62, 0.59, 0.58, 0.62).

### What makes it strong (the client's note)

The trap is the order basis: the paid read (subtotal less points credit) Finance used gives 1,148 kits, and reading the Hazel & Hound archive by account alone gives 1,143, because 970 storefront orders were credited by The Den to a member who checked out without signing in.
The computation chain runs from 24,646 active memberships (188 merged accounts folded into survivors) through two conformed order layers, two returns files (including 260 late-May storefront orders returned through Fetchwell), and a year-end link cut that keeps the January linking surge out.
Determinism pins: 1,298 Top Dog (1,048 app, 250 migration), 5,048 Pack Plus, 18,300 Pack, 194 members within $100 below the line, and a 749 / 353 / 196 split across two species vocabularies.
The closing block depends on ledger hygiene: W2027-38R replaces the REDEEM and PROMO entries of W2027-38 and MB-2's second transmission repeats its first, which gives 1,582 never-signed-in former Den members holding 7,396,935 points (a raw sum gives 1,640 and 9,951,112).

### Stakeholder ask (the prompt, verbatim)

Brightpack holds our kit pricing only through January, so the purchase order for Top Dog welcome kits must be placed on the 16th, five days before the determination run makes the result official. A wrong count either leaves boxes stranded in Brightpack's warehouse or forces us to air-freight make-goods in March. This is the first Pack Rewards determination since Hazel & Hound members were migrated. Finance budgeted the kit line using what members actually paid during the year, but I need the determination run to settle the order.

Give Brightpack one committed kit total, split across the three box builds: dog, cat, and other companion. Member, kit, and point counts are whole numbers unless a different rounding rule is stated.

Put the decision in pack_rewards_2028_determination_memo.docx. After the order total and box-build split, show the tier result from the determination: members landing in each of the three tiers, split by account origin,opened in the app versus created during the June migration,with a total that matches the membership population covered by the run. Also report the number of members finishing within $100 below the Top Dog threshold, which is the figure Maggie uses to size the order buffer.

Include a chart in the memo with grouped bars for member counts by tier and account origin, labeling every bar. Show the kit order by box build beside it, labeled by build, and use a title from which the VP can read the order directly.

Close the memo with the effect of the Hazel & Hound migration. Report Hazel & Hound sales from January 1 through the switchover, net of returns, to the nearest whole dollar. Then report how much of that total belongs to customers whose old Hazel & Hound account was linked to their membership by year-end, both to the nearest whole dollar and as a share of the total to one decimal place. For Priya's winback list, also report how many former Den members have never signed in and still hold at least 2,000 points, plus the total points they hold.

The determination run should produce pack_rewards_2027_member_year.csv, one row per membership covered by the determination, with membership number, account origin, qualifying activity for the year in dollars and cents, 2028 tier, and box build for each member receiving a kit.

### Deliverables

`pack_rewards_2028_determination_memo.docx`, `pack_rewards_2027_member_year.csv` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (Fetchwell's Pack Rewards program has to place its Top Dog welcome-kit purchase order with Brightpack on January 16, five days before the 2028 determination run, and this is the first determination since Hazel & Hound's Den members were migrated in June 2027. Finance budgeted the kit line on what members paid, but the program terms grade status on the merchandise subtotal of completed 2027 orders net of returns started by January 10, with Hazel & Hound purchases counted on the same measure. The analyst must conform the two order systems (dollars and UTC JSON against integer cents and Eastern time CSV), route Hazel & Hound accounts to surviving memberships through links as they stood at year-end and provisioned source references, credit storefront purchases The Den attributed by phone number at checkout, net both returns files, assign tiers and box builds from the profile of record, and report migration and winback figures from a ledger with a reissued batch and a duplicated transmission. The deliverables are `pack_rewards_2028_determination_memo.docx` (kit total and box-build split, tier counts by account origin with a total, the near-threshold buffer count, a labeled grouped-bar chart with the kit split beside it, and closing migration figures) and `pack_rewards_2027_member_year.csv` (one row per membership with origin, qualifying activity, tier, and box build).)

`21 files, 56.3 MB`, `data_dictionary.md`, `den_2026_determination_summary.csv`, `den_member_extract_20270601.csv`, `den_points_ledger_2026_2027.csv`, `den_program_overview.pdf`, `den_status_review_register_2027.xlsx`, `export_manifest.csv`, `fetchwell_members.csv`, `fetchwell_orders_2027.jsonl`, `fetchwell_returns_2027.csv`, `hh_orders_2026_2027.csv`, `hh_returns_2026_2027.csv`, `member_link_register.csv`, `migration_cutover_note.md`, `pack_points_ledger_2027.csv`, `pack_rewards_kpi_2027.csv`, `pack_rewards_program_terms.pdf`, `pack_team_thread_2028-01.md`, `pet_profiles_fetchwell.csv`, `pet_profiles_hh.csv`, `promo_campaign_catalog.csv`

### Final recommendation

Order 1,298 Top Dog welcome kits on the January 16 purchase order, split 749 dog, 353 cat, and 196 other companion builds.

### Step-by-step solution

1. Build the frame from the registry: 24,646 active memberships (17,943 opened in the app, 6,703 created at the June migration), with merged accounts carried by their surviving membership.
2. Route Hazel & Hound accounts to memberships through links dated on or before December 31, then through provisioned accounts' source references, keeping account ids as character keys.
3. Conform the two order systems: app JSON orders in dollars with UTC stamps and storefront orders in integer cents with Eastern stamps, dropping cancelled orders and leaving the SHIPPED orders from the final week, which belong to non-members, out of every member's year.
4. Join the Den ledger's BASE postings to the archive on the order reference to find storefront purchases credited to a member who checked out without signing in, and route each to that member's membership.
5. Compute qualifying activity: merchandise subtotal of completed 2027 orders on both stacks, minus merchandise refunds on returns initiated by January 10, 2028, from the Fetchwell file (which includes late-May storefront orders) and the storefront file. 1,298 members reach $2,400 and 5,048 land between $900 and $2,400.
6. Check the rival bases: the paid read gives 1,148 and the account-only archive read gives 1,143; neither matches the terms.
7. Count the buffer population: 194 members finish between $2,300.00 and $2,399.99.
8. Split the 1,298 by the primary pet on the profile of record (app first, imported Hazel & Hound otherwise, mapping both vocabularies): 749 dog, 353 cat, 196 other.
9. Compute the migration figures: storefront sales January 1 to June 1 net of both returns sources are $3,943,125; $630,900 (16.0%) belongs to accounts linked by December 31.
10. Build the winback list from the ledger of record (W2027-38R replacing W2027-38's REDEEM and PROMO entries, MB-2's second transmission dropped): 1,582 migration-created members whose last sign-in is still the provisioning stamp hold 7,396,935 points.
11. Write the memo and chart, and export the member-year CSV of 24,646 rows.

### Key traps (what the model did)

- Avoided Finance's paid-amount basis, but joined the Hazel & Hound / Den archive to members by account only. That missed 970 storefront orders The Den credited to members by phone number under one-off customer records, so 155 qualifying members were dropped: 1,143 kits instead of 1,298, with migration-origin Top Dog at 95 instead of 250.
- The same under-attribution also shifted the near-threshold buffer (210 vs 194).

### Justification

The terms grade status on the merchandise value of completed orders net of timely returns, not on what members paid, so Finance's paid basis undercounts by 150 members who covered part of their spend with points. The Den credited storefront purchases to members by phone number even when they never signed in, and those orders sit under one-off customer records, so an account-only read of the archive misses 155 qualifying members. Counting both stacks on the terms' measure with links as of year-end gives 1,298 Top Dog members, and the profile of record splits them 749 dog, 353 cat, and 196 other, which is the count Brightpack should build.

## Set the flow standard included allowance at 13,000 Billable runs, the only allowance that meets all three conditions

**Usage-Based Pricing Allowance Setting**, Batch 14, Product Analytics, model mean **0.58** over 4 runs (0.53, 0.88, 0.47, 0.53).

### What makes it strong (the client's note)

The trap is the slate itself: each of the seven candidates breaks one condition (5,000, 8,000 and 10,000 overrun February review hours; 12,000, 15,000, 20,000 and 30,000 fall short of the GBP 267,000 plan contribution), and the policy defines an allowance as any whole thousand, so the answer has to be found off the slate.
Annualised overage revenue is not monotone in the allowance because the rate card prices a block at GBP 12.00 at or below 12,500 included runs and GBP 17.00 above it, so neither the lowest nor the highest compliant allowance is the answer; the surviving region is about 12,600 to 13,400 runs and 13,000 is the only whole thousand in it.
Review capacity is two monthly resources, not one pool: February carries 238.0 reviewer hours and no accredited hours, March carries 593.0 with 423.6 accredited, so every Extended Review falls in March, and pooling the 831.0 hours would wrongly admit 9,000.
Two populations: the distribution runs over 1,750 Eligible Accounts, while the 9.5% bill-increase limit is a share of 2,575 Covered Accounts on the Announcement Date.

### Stakeholder ask (the prompt, verbatim)

Subject: where do we set the included allowance on Flow Standard, and who do we protect?

We are putting an included usage allowance on the Flow Standard plan from April and I have to take one number to the committee. The pricing team has fixed a slate of candidate allowances, three different cuts of the usage data give me three different answers, and whatever we land on has to sit inside what we have promised customers publicly and inside what support can physically get through before the change goes live. I have put everything the decision draws on into the attached export: the raw metering, the registers behind it, Commercial Finance's rollup, the policy and the commitment we published, the committee's minutes, the 2029 capacity plan, the rate card and an earlier working file.

Work it from the raw rows and tell me where to set the allowance and which accounts we protect, with the numbers behind both and what each candidate on the slate would cost us.

Please give me back two things. bracken_flow_allowance_distribution_2029.csv - the distribution of usage across the accounts the change applies to, deciles and the upper percentiles with a count at each, then the allowance you recommend with how many accounts and what share sit above it, each constraint and whether we clear it, then one block for each candidate allowance carrying the same figures, each marked as to whether it is the allowance you recommend. bracken_flow_allowance_decision_2029.png - one chart for the committee showing that distribution with every candidate marked and the constraint lines labeled, and the allowance you recommend and the share of accounts affected in the title.

### Deliverables

`bracken_flow_allowance_distribution_2029.csv`, `bracken_flow_allowance_decision_2029.png` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A SaaS company is putting an included usage allowance on its Flow Standard plan from April 2029 and the pricing lead must take one number to the pricing committee, along with which accounts are protected. The committee has modelled a slate of seven candidate allowances, and the choice has to stay inside the bill-increase limit the company has published, the grandfathering review capacity support can deliver before go-live, and the overage contribution in the FY2029 operating plan. Working from the raw daily usage ledger, account, subscription, workspace and addenda registers, Commercial Finance's rollup, the allowance policy, the published pricing commitment, the committee minutes, the 2029 capacity plan, the rate card and an earlier draft, the analyst must build the usage distribution on the policy's definitions, test each candidate against the three conditions, and set the allowance. Deliverables are `bracken_flow_allowance_distribution_2029.csv` (deciles and upper percentiles with counts, the recommended allowance with the accounts and share above it and each constraint, and one block per candidate) and `bracken_flow_allowance_decision_2029.png` (the distribution with every candidate and constraint line marked, and the recommendation and share affected in the title).)

`16 files, 10.8 MB`, `bracken_accounts_2028-12-31.csv`, `bracken_allowance_scenarios_draft_2028-11-20.json`, `bracken_committed_usage_addenda_2028-12-31.xlsx`, `bracken_customer_pricing_commitment_2028.pdf`, `bracken_data_dictionary.md`, `bracken_flow_included_allowance_policy_2029.pdf`, `bracken_flow_rate_card_2029.md`, `bracken_fy2029_operating_plan_extract.xlsx`, `bracken_monthly_usage_summary_2028.csv`, `bracken_platform_release_notes_2028.md`, `bracken_pricing_committee_minutes_2028-12-11.docx`, `bracken_subscription_changes_2029-01.csv`, `bracken_subscriptions_2028-12-31.csv`, `bracken_support_revops_capacity_plan_2029.xlsx`, `bracken_usage_ledger_daily_2028-10_2028-12.csv`, `bracken_workspace_register_2028-12-31.csv`

### Final recommendation

Set the Flow Standard Included Allowance at 13,000 Billable Runs per Billing Period, the only allowance that meets all three policy conditions; none of the seven Candidate Allowances does. At 13,000, 309 of the 1,750 Eligible Accounts sit above it: the 153 with Price Protection are grandfathered at their own Reference Usage and 156 (6.06% of 2,575 Covered Accounts) move to the rate card.

### Step-by-step solution

1. Normalise the plan, state, account type and run mode vocabularies, and confirm the ledger covers 1 October to 31 December 2028 in full.
2. Count Billable Runs (live runs that succeeded or failed), attribute them to accounts through the workspace register, and cut each account's series into Billing Periods on its anchor day; Reference Usage is the most recent Complete Billing Period.
3. Build the 1,750 Eligible Accounts: Flow Standard, in force, not trial, not internal, not under a Committed Usage Addendum in force on 1 April 2029 (545 of 591), with a Complete Billing Period.
4. Build the 2,575 Covered Accounts from the 2,480 in force at the Reference Date and the January changes effective on or before 15 January 2029.
5. Describe the distribution with linear-interpolation percentiles: median 3,395, P90 22,249, P95 36,751, P99 118,351.
6. Compute review capacity by month: February 238.0 hours (0.0 accredited), March 593.0 (423.6 accredited); Extended Reviews (3.5 hours, accounts at 40,000 runs or more) can only run in March.
7. Test the slate: 5,000, 8,000 and 10,000 put 465.0, 313.5 and 258.0 hours into February; 12,000, 15,000, 20,000 and 30,000 earn GBP 219,600, 227,256, 128,112 and 50,184 against GBP 267,000. None passes all three conditions.
8. Search every whole thousand: only 13,000 passes, at 6.06% against 9.5%, 190.5 of 238.0 February hours and 433.0 of 593.0 March hours, and GBP 281,520 against GBP 267,000.
9. Settle scope: 46 accounts with an Extended Review and an anchor day of 14 or earlier get their determination on 31 March, under 15 days' notice, so the allowance applies to them from May 2029; 7 of them lack Price Protection.
10. Confirm on both clause 6.1 alternative bases: 13,000 on the two-period mean (GBP 281,112) and on the greater of the two (GBP 304,164).

### Key traps (what the model did)

- Restricted the search to the seven slate allowances; when every candidate failed a condition, recommended the least-bad one (15,000) while its own CSV showed it failing the GBP 267,000 plan contribution.

### Justification

The policy sets the Included Allowance from among the allowances that satisfy all three conditions, and it defines an allowance as any whole thousand, not only the modelled candidates. Every candidate fails one condition, either because February's review hours cannot absorb the work or because overage revenue falls below the plan contribution. 13,000 sits just above the rate card's 12,500 band edge, where the higher block price lifts revenue to GBP 281,520 while the review load still fits each month, and it is the only whole thousand that clears all three conditions on every permitted basis.

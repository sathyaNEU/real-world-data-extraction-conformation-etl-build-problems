# Exemplars: Nonprofit & Grant-making

> 10 accepted tasks in this domain, sorted by the current model's measured mean, lowest (hardest) first. Each is the client's own record. Index and the shared architecture: `index.md`.

## Estimate 2,591,394 Applicant units eligible for the winter relief grant at 185 percent of the poverty guideline

**Means-Tested Grant Eligibility Estimation**, Batch 14, Nonprofit & Grant Making, model mean **0.17** over 4 runs (0.16, 0.18, 0.18, 0.18).

### What makes it strong (the client's note)

The trap is the unit: reading the housing file as one unit per household with household income gives 1,200,900 eligible households at 185 percent and 948,724 at 150 percent, and it reproduces one of the six November shares and none of the six November dollar allocations.
The applicant unit has to be built from the person records: the householder with spouse or partner and own children under 18, each subfamily its own unit, each other adult its own unit, with unit income the members' PINCP adjusted by ADJINC. That basis gives 8,349,629 units in 6,153,124 households and reproduces all six Paper 24/31 allocations to the dollar at 150 percent.
The guideline year is pinned to 2023 by the November paper and minutes; the 2024 and 2025 guidelines give 2,650,964 and 2,720,889 and would break the like-for-like comparison.
Determinism pins: 2,591,394 units at 185 percent; Connecticut 645,541 (24.9 percent), Maine 240,869 (9.3), Massachusetts 1,209,612 (46.7), New Hampshire 197,189 (7.6), Rhode Island 197,354 (7.6), Vermont 100,829 (3.9); tiers 2,003,305 / 328,190 / 121,163 / 138,736; full take-up cost 876,090,600; reach 0.55 percent gross and 0.52 percent net of the 6 percent fee.

### Stakeholder ask (the prompt, verbatim)

I am the research analyst at the Pellworth Foundation. The trustees meet on February 27 to decide whether the income limit for the Winter Relief Grant moves from 150 to 185 percent of the federal poverty guideline for the 2025-26 round, and Teresa has asked me for the estimate that goes in the board packet. The supplied files on the shared drive have the October extract of the Census Bureau's 2023 one-year microdata for the six states with its field list and the extract note, the Bureau's published state totals, the poverty guideline table, the partner guidelines, Nikhil's November budget paper, the November minutes and Teresa's message.

What I need first is the figure itself: the eligible population at 185 percent across the six states, one number that goes in the paper and that I will be asked to defend at the meeting. The rest supports it. Behind it I need the eligible population by state and by grant tier; the partner allocations that would follow on the same budget and the same formula, with the change for each partner against the November figures; and what share of the eligible population a budget of that size reaches at the current grant schedule. Three files: a workbook for finance with the tables, a short memo for the board packet that gives the figures and says how they were built, and a chart for the packet.

Shares to one decimal place and dollars whole, as in Nikhil's paper.

### Deliverables

`eligible_population_185_percent_paper_25-06.pdf`, `eligible_units_2025-26_estimate.xlsx`, `eligible_units_by_state.png` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A New England foundation's trustees will decide whether to raise the Winter Relief Grant income limit from 150 to 185 percent of the federal poverty guideline for the 2025-26 round. The research analyst must estimate the eligible population at 185 percent across six states from the Census Bureau's 2023 one-year PUMS person and housing files, using the extract note, field list, published state totals, guideline table, partner guidelines, the November budget paper (Paper 24/31) and minutes. The eligible population is then broken down by state and grant tier, the 4,800,000 budget is reallocated to the six partners on the November formula with the change against November, and the analyst reports the share of the eligible population the budget reaches at the current grant schedule. Deliverables are a finance workbook with the tables, a short memo for the board packet that gives the figures and how they were built, and a chart for the packet, with shares to one decimal and whole dollars.)

`20 files, 28.1 MB`, `Winter_Relief_Grant_185_percent_estimate_for_the_February_board.eml`, `acs_2023_1yr_state_totals.csv`, `hhs_poverty_guidelines_2023_2025.csv`, `psam_h09.csv`, `psam_h23.csv`, `psam_h25.csv`, `psam_h33.csv`, `psam_h44.csv`, `psam_h50.csv`, `psam_p09.csv`, `psam_p23.csv`, `psam_p25.csv`, `psam_p33.csv`, `psam_p44.csv`, `psam_p50.csv`, `pums_extract_field_list.csv`, `pums_extract_note.md`, `trustees_minutes_2024-11-21.pdf`, `trustees_paper_24-31_budget_and_allocations.pdf`, `winter_relief_grant_guidelines_2024-25.pdf`

### Final recommendation

At 185 percent of the 2023 poverty guideline the eligible population across the six states is 2,591,394 applicant units (against 2,194,741 at the current 150 percent, an increase of 396,653 or 18.1 percent); on the same 4,800,000 budget Massachusetts' allocation falls by 31,896 and the other five partners' allocations rise.

### Step-by-step solution

1. Load the six states' 2023 one-year PUMS person and housing files, keep occupied housing units and their persons, and exclude group quarters as the guidelines do; weighted, the extract holds 6,153,124 households.
2. Build applicant units from RELSHIPP, AGEP and SFN: the householder, spouse or partner and own children under 18 not in a subfamily as one unit, each subfamily as a unit, every other person aged 18 or over as a unit, and a child under 18 with no parent present in the householder's unit; 8,349,629 units.
3. Sum each unit's PINCP times ADJINC and test it, at or below the limit, against the 2023 guideline for the unit's size (14,580 plus 5,140 per additional member).
4. Check the basis at 150 percent: 2,194,741 eligible units give the six Paper 24/31 shares (24.9, 9.0, 47.3, 7.4, 7.5, 3.9 percent) and the six November allocations exactly. The household reading reproduces one share and no allocation.
5. At 185 percent, count 2,591,394 eligible units, 396,653 more (18.1 percent), and break them down by state and by grant tier (one member 2,003,305, two 328,190, three 121,163, four or more 138,736).
6. Allocate the 4,800,000 budget in proportion to each state's eligible count at 185 percent in whole dollars: Connecticut 1,195,726 (+2,905), Maine 446,158 (+13,608), Massachusetts 2,240,546 (-31,896), New Hampshire 365,250 (+10,067), Rhode Island 365,556 (+4,230), Vermont 186,764 (+1,086).
7. Compute reach at the current grant schedule: full take-up costs 876,090,600 at an average grant of 338, so the budget reaches 0.55 percent of the eligible population, or 0.52 percent net of the 6 percent partner fee.
8. Produce the workbook, the memo leading with 2,591,394 and how it was built, and the chart of eligible units by state at both limits.

### Key traps (what the model did)

- Counted eligibility at the housing-record grain (one occupied unit = one applicant unit, HINCP household income) and explicitly declined to build applicant units from person records, so the headline, tiers, 150% baseline and reach all came out on the wrong unit.
- Saw that its basis did not reproduce the November Paper 24/31 allocation and reported the non-reproduction as a caveat instead of treating it as proof the unit was wrong.

### Justification

The November allocation is the one published control, and only the person-built applicant unit tested against the 2023 guideline reproduces it to the dollar; the household reading, which looks natural from the housing file, misses five of six shares and every dollar amount. On the basis that returns November, 2,591,394 units are eligible at 185 percent. Because most of the added eligibility is adults living in someone else's home whose own income is below the limit, the share shifts away from Massachusetts, so its allocation falls while the other five partners gain. Even at the higher limit the budget reaches only about half a percent of those eligible.

## Return 134,225 Dollars to the threadgill endowment on the ending of the contribution agreement

**Restricted Contribution Settlement**, Batch 14, Nonprofit & Grant Making, model mean **0.19** over 4 runs (0.35, 0.32, 0.29, 0.32).

### What makes it strong (the client's note)

The trap is the totals comparison: awards paid from the fund account (3,615,333) exceed the contribution notified (3,510,000) in aggregate, which suggests nothing is owed, but that comparison cannot see sums that left the account without meeting an award.
No document says which of the 31 movements out to the general account are the fund's own money returning, so the attribution method has to be chosen against the closed Ellerby bequest, settled at 30,077 dollars on 11 March 2019. Only exact-amount pairing with pricing of an over-sized movement reproduces 30,077; netting returns 183,923, the balance 60,566, and unpriced pairing 39,523.
The computation chain: pair each movement out with an earlier movement in of the same amount (24 matches), take the 7 unmatched movements out as contribution leaving, and price the 7 September 2026 movement of 52,416 as 28,096 of recovered advance and 24,320 of contribution.
Determinism pins: sum returned 134,225 (3.8% of 3,510,000); applied 3,375,775; largest difference 24,320 in 2026, ahead of 23,871 in 2025; own-funds cost 239,558; 5,020 of 20,346 cleaned awards paid from the fund account.

### Stakeholder ask (the prompt, verbatim)

The Threadgill Endowment wrote to us in December ending the contribution agreement it has funded our hardship program under since 2020. Under the agreement we return so much of the contribution as has not been applied to its purpose. Nobody here has had to work that out before, because for seven years the arrangement simply ran, and the woman who set it up left in 2021 and took her spreadsheets with her. Their chair has written that they will take our figure as we put it. I would rather give them a number I can stand behind line by line than one I have rounded into a letter. The trustees take it on 19 March and they do not come back to these things.

I am the finance officer here and I have put the whole folder in front of you. The agreement and the notice. What the Endowment told us it was giving for each year. The fund account the program is paid out of, and the general account it sits beside. The claims, and the awards ledger, which changed system in 2022 and looks it. Then the statement of designated fund balances, the referral roll, the standard award by year, the published annual review, the returns we make to them each February, the Ellerby bequest account from the one before this, the office note on how we run the accounts, the Vandermeer quarterly files with their report, and whatever minutes the secretary marked up. That is everything the office holds and there is nothing behind it.

So: what do the trustees settle as the sum we return to the Threadgill Endowment. Whole dollars everywhere please, no cents, and any percentage to one decimal place.

Provide the reproducible analysis as threadgill_settlement.py, Python 3, standard library only, no arguments, reading the supplied files out of its working directory. I want it to print the sum returned, and that sum as a share of everything the Endowment notified us over the arrangement. Then a line for each year of the arrangement: what the Endowment notified us for that year, so much of it as was applied to its purpose, and the difference between the two. Put a line at the bottom for the arrangement as a whole with the totals of those three columns. The ledger will need cleaning before any of that is worth anything, so do that properly, and when you have, print one number off it: how many of the awards left were paid out of the fund account.

Then the covering page, settlement_note.pdf, one page, the way I would write to a counterparty and not a paper for a meeting. Open on the sum. Say which year the largest difference fell in and what that difference was. Then close it out by telling them what this arrangement has cost us out of our own funds over the seven years, off your own reconciliation rather than asserted.

Keep a chart in the note. I just need the two lines side by side, the contribution notified and so much of it as was applied, by year, both series named and every point labeled with its value, and the difference at each year marked above the axis with its figure. Label the axes, dollars and years, and title it with what it shows rather than what it contains.

### Deliverables

`threadgill_settlement.py`, `settlement_note.pdf` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A hardship fund must settle with the Threadgill Endowment, which has ended the contribution agreement that funded its standard awards from 2020 to 2026. Under the agreement the fund returns so much of the contribution as was not applied to its purpose, and the Endowment's trustees will accept the fund's figure as stated. The analyst works from the agreement and termination notice, the Endowment's notifications, the fund account and general account, the claims intake and a two-era awards ledger, the statement of fund balances, the annual review and returns, the closed Ellerby bequest account, office notes, minutes and a partner data share. The analyst must find the sum returned, its share of total notified, the year-by-year contribution applied, the cleaned-ledger count of awards paid from the fund account, and the arrangement's cost to the fund's own money. Deliverables are `threadgill_settlement.py` (Python 3, standard library only, no arguments, printing the sum, the share, a line per year and a totals line, and the award count) and `settlement_note.pdf` (a one-page letter to the Endowment opening on the sum, naming the year of the largest difference, closing on the own-funds cost, with a two-line chart of notified and applied contribution by year).)

`20 files, 5.0 MB`, `ohf_annual_returns_to_endowment.csv`, `ohf_annual_review_2026.xlsx`, `ohf_award_schedule.csv`, `ohf_awards_ledger_2018_2026.csv`, `ohf_claims_intake_2018_2026.csv`, `ohf_cofunding_agreement_2019.pdf`, `ohf_ellerby_account_2013_2018.csv`, `ohf_endowment_notifications.csv`, `ohf_file_notes.md`, `ohf_fund_balance_2026.pdf`, `ohf_general_account_2018_2026.csv`, `ohf_member_organizations.csv`, `ohf_office_procedures.md`, `ohf_scheme_handbook_2026.pdf`, `ohf_sources_and_licence.txt`, `ohf_termination_notice.pdf`, `ohf_threadgill_account_2020_2026.csv`, `ohf_trustees_minutes_extract.txt`, `vmt_data_share.csv`, `vmt_liaison_report_2027_02.pdf`

### Final recommendation

Return 134,225 dollars to the Threadgill Endowment, 3.8% of the 3,510,000 notified over 2020 to 2026; the largest yearly difference is 24,320 dollars in 2026, and the arrangement cost the fund 239,558 dollars of its own money.

### Step-by-step solution

1. Isolate the movements between the fund account and the general account: 29 movements in and 31 movements out over seven years, none labeled.
2. Score candidate attribution methods against the closed Ellerby arrangement, settled at 30,077 dollars. Only exact-amount pairing with pricing of a movement that exceeds an outstanding advance returns 30,077.
3. Run it on the Threadgill account in value-date order: 24 movements out match an earlier movement in of the same amount, and 7 movements out match nothing.
4. Price the 7 September 2026 movement of 52,416: the 12 August 2026 advance of 28,096 is the only outstanding advance it can contain, so 24,320 is contribution leaving.
5. Confirm the four remaining movements in (1,244,784 in total) are advances awaiting recovery under the instalment calendar, and that at each of the seven dates the Endowment money received to date exceeds the sum leaving.
6. Sum the seven amounts (11,753, 14,879, 17,987, 18,354, 23,061, 23,871 and 24,320) to 134,225, which is 3.8% of 3,510,000 notified.
7. Derive the applied series as notified less each year's amount: 238,247, 365,121, 432,013, 496,646, 576,939, 616,129 and 650,680, totalling 3,375,775. The largest difference is 24,320 in 2026.
8. Clean the awards ledger (1,114 exact repeats and 821 amendment rows removed) to 20,346 awards, 5,020 of them paid from the fund account.
9. Compute the own-funds cost as awards paid from the fund account, 3,615,333, less contribution applied, 3,375,775: 239,558.
10. Write the script and the one-page letter with the year table and the two-line chart.

### Key traps (what the model did)

- Settled the return from an aggregate or ad-hoc reconciliation (awards paid vs contribution notified, or arbitrary netting) instead of attributing individual outflows; two runs returned $0, others $2,421 and $706,139.
- Never used the settled Ellerby bequest as the method-selection control, so no run could distinguish netting / balance / pairing methods; downstream yearly differences and own-funds cost all drifted (105k to 7.85M).

### Justification

The agreement returns only the contribution not applied to standard awards, and the fund was free to move its own money in and out of the account. Separating those movements is the whole question, and the closed Ellerby arrangement, run the same way and already settled, shows which method the fund uses: pairing on exact amounts with the over-sized movement priced. That method reproduces the Ellerby settlement to the dollar and, on the Threadgill account, identifies one contribution outflow in each of the seven years totaling 134,225. The aggregate comparison of awards with contribution is correct about the fund's own subsidy of 239,558 but cannot detect these outflows.

## Budget on the halls and meeting places fund balance running out in 2029-30, With 7,283,135 Pounds not covered

**Capital Grant Drawdown Forecasting**, Batch 14, Nonprofit & Grant Making, model mean **0.34** over 4 runs (0.40, 0.40, 0.38, 0.40).

### What makes it strong (the client's note)

The trap is the stage schedule: every one of the 1,632 paid certificates falls on its scheduled date and the closed years reproduce from it, but it is stale for the 127 last-round awards with no certificate yet, whose schedules still run from acceptance although their case items arrived 7 to 17 months later. Forecasting from the schedule puts the crossing in 2028-29.
The guidance says the programme of works runs from commencement; the record shows commencement is the later of the certificate of insurance received and the contract administrator's appointment approved. Programme months from that date are constant by project type for all 1,632 certificates, while acceptance misses 82, the insurance certificate alone misses 26 and the appointment alone misses 56.
The computation chain: apply the three-month acceptance rule (763 of 960 offers live, excluding 269 certificates against lapsed offers), pay each stage at 95% with the retention released at final account, date every unpaid stage from commencement plus the programme months for its type, and sum by programme and financial year.
Determinism pins: 11,086,205; 17,455,255; 12,655,710; 7,660,805; 1,970,595; 204,565 by year; cumulative 41,197,170 at the close of 2028-29 and 48,857,975 at the close of 2029-30; six-year total 51,033,135; 7,283,135 not covered; closed years 2020-21 to 2025-26 reproduced to the pound.

### Stakeholder ask (the prompt, verbatim)

I need a six-year drawdown forecast for the Fund built from the case records, not rolled forward from last year's. Awards are paid out in stages as the works go, and the Committee publishes what the live awards are expected to draw in the coming year and the five after it, by program, against the balance the Fund holds. The Fund is closed to new applications, so everything that will be drawn is already on the register.

Give me the six years from 2026-27 by program and in total, in whole pounds. The Fund held 43,750,000 pounds at 31 March 2026. Tell me which year that balance runs out in and how much of the six years' drawings it doesn't cover. Also give me each program's six-year total.

Put it in drawdown_forecast.pdf, two pages, in the form the Committee publishes these in. Lead with the table, then the year the balance runs out and the amount not covered, and include one chart of the cumulative total with the balance drawn as a level and the crossing marked.

Also give me forecast.py, standard library only, no arguments, run from the supplied files. It should build the figures from the records rather than restate them and print the same table. The closed years are already published, so the same basis has to reproduce them to the pound. Say whether it does. Nothing rounded or estimated.

### Deliverables

`drawdown_forecast.pdf`, `forecast.py` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A grants committee runs a closed capital fund for community halls whose awards are drawn down in stages as works proceed. It needs a six-year drawdown forecast from 2026-27, by programme and in total, built from the case records rather than rolled forward, set against the 43,750,000 pounds the Fund held at 31 March 2026, with the year the balance runs out and the amount not covered. The analyst works from the award register, the stage schedule, the case items log, the certificate event log, the retention ledger, the published outturn for six closed years and the scheme guidance. Deliverables are `drawdown_forecast.pdf` (two pages leading with the table, then the exhaustion year and uncovered amount, and one cumulative chart with the balance as a level and the crossing marked) and `forecast.py` (standard library, no arguments, builds the figures from the records, prints the same table and says whether the closed years reproduce to the pound).)

`11 files, 1.2 MB`, `award_register.csv`, `case_items.csv`, `claims_log.csv`, `committee_note.pdf`, `data_dictionary.md`, `outturn_by_year.xlsx`, `programmes.csv`, `retention_ledger.csv`, `scheme_guidance.pdf`, `sources_and_licences.txt`, `stage_schedule.csv`

### Final recommendation

The Committee budgets on the 43,750,000 pound balance held at 31 March 2026 being exhausted in 2029-30, when cumulative drawings under live awards reach 48,857,975 pounds; 7,283,135 pounds of the six years' drawings (51,033,135) is not covered.

### Step-by-step solution

1. Apply the three-month acceptance rule to the register: 763 of 960 offers are live (48 with no acceptance and 149 accepted late lapse), and the 269 certificates logged against lapsed offers are excluded.
2. Model payment from the paid record: each certificate pays the stage less 5%, and the final account stage adds the retention held, confirmed against the 1,632 paid amounts and the retention ledger.
3. Test the schedule: every paid certificate falls on its scheduled date, but 127 last-round awards with no certificate have schedules that still run from acceptance.
4. Recover the programme months by project type measured from commencement, taken as the later of the certificate of insurance received and the appointment approved (equipment 3, 9, 13; refurbishment 4, 14, 20; extension 5, 11, 24, 29; new build 8, 14, 28, 36, 41; major works 9, 16, 28, 40, 48, 53). This reproduces all 1,632 paid certificates.
5. Date every unpaid stage of every live award from commencement plus its programme months and sum by programme and financial year: 11,086,205, 17,455,255, 12,655,710, 7,660,805, 1,970,595 and 204,565 for 2026-27 to 2031-32.
6. Report programme totals: 06.2 Community development 18,023,980; 08.1 Recreational and sporting services 18,629,370; 08.2 Cultural services 14,379,785; total 51,033,135.
7. Accumulate: 11,086,205, 28,541,460, 41,197,170, 48,857,975, 50,828,570 and 51,033,135, so the balance is exhausted in 2029-30 and 7,283,135 is not covered.
8. Backtest the same basis on 2020-21 to 2025-26: every closed year reproduces the published outturn by programme and in total to the pound. Write the PDF and the script.

### Key traps (what the model did)

- Dated every unpaid stage from the stage schedule's scheduled_date because that field reproduces all paid certificates and the closed years to the pound; never noticed that the backtest only covers awards whose schedules were already re-aligned, and that the 127 not-yet-drawing awards still run from acceptance.

### Justification

The stage schedule passes every backtest only because the office brings an award's schedule into line once it starts drawing; for the awards that have not yet drawn it still runs from acceptance. The guidance ties the programme to commencement, and the paid record identifies commencement as the later of the two case items, which reproduces every paid certificate where no rival dating does. Dating the unpaid stages that way pushes 20,368,300 pounds of drawings later and moves the year the balance runs out from 2028-29 to 2029-30, the year the Committee should budget on.

## Name education and learning in tessel, owned by farah okonkwo, as the source of the fy2025 average-grant fall

**Community Foundation Grants Reporting**, Batch 14, Nonprofit & Grant Making, model mean **0.36** over 4 runs (0.57, 0.13, 0.09, 0.68).

### What makes it strong (the client's note)

The trap is the counting basis. Treating each award decision as a grant, or keeping payees recorded under the Foundation's own EIN (46-3817205, its fiscally sponsored projects), reproduces at most 16 of the 24 published figures and moves the leaf to YF/DNM, EN/PLM or YF/HLV. Only combining decisions per grantee, programme and year and excluding those payees reproduces all 24.
The computation chain: drop rescinded awards, assign by fiscal year of award, aggregate decisions per grantee, exclude the Foundation's own EIN, check against the published series, then run FC-3 at programme level and again at county level inside Education and Learning, scaling county contributions by the programme's w-bar of 17.73 per cent.
Determinism pins: Foundation-wide change -$811.96 ($27,647.12 to $26,835.16); Education and Learning -$385.60 against Health and Wellbeing -$210.25 (margin $175.35); Tessel -$427.55 against Arlow -$1.86 (margin $425.69).
The binding constraint is G-7 5.1 and 5.2: the published years identify the basis, and the same test rules out the rapid-response exclusion, which reproduces only 21 of 24.

### Stakeholder ask (the prompt, verbatim)

Our average grant fell from FY2024 to FY2025 and the Finance Committee wants one panel named for it on November 18. Tell me which program and county it lands on, which panel lead owns it, and how much of the fall they account for.

Put the supporting analysis in average_grant_bridge_fy2025.xlsx. Set the compiled average beside the Network's published figure for every program and published year, with the gap between them. Give FY2024 and FY2025 by program with grants, share of grants and average grant, then each program's mix piece, rate piece and contribution to the change in the Foundation-wide average. Do the same for every county inside the program the drill enters. Take the explanations already put to the Board one at a time against the figure that settles each.

The Committee sees finance_committee_average_grant_fy2025.pptx, three or four slides. Bridge the FY2024 average grant to the FY2025 average, one step per program with mix and rate apart. Walk down to the leaf, showing the runner-up and the margin at each level and the contribution at which the call would change. Say which of the Board's explanations hold.

### Deliverables

`average_grant_bridge_fy2025.xlsx`, `finance_committee_average_grant_fy2025.pptx` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A community foundation's average grant fell from FY2024 to FY2025, and the Finance Committee wants one panel named for it at its November 18 meeting. The Network that used to compile the Average Grant Series has stopped, and Board Policy G-7 bars any compilation that does not reproduce all 24 published figures for FY2021 to FY2024. The analyst has to rebuild the Series basis from the raw award register, payment ledger and grantee directory, apply the FC-3 midpoint mix and rate decomposition to programmes and then to counties inside the leading programme, name the leaf and its panel lead, and test the three explanations Board members gave in the October minute. The deliverables are `average_grant_bridge_fy2025.xlsx` (published against compiled averages with gaps, both years by programme, both drill levels, and the explanations against their deciding figures) and `finance_committee_average_grant_fy2025.pptx` (three or four slides with a programme bridge, the drill to the leaf with runner-ups, margins and switching points, and a verdict on each explanation).)

`11 files, 1.9 MB`, `board_minutes_2025_10_14.pdf`, `network_letter_2025_07_22.txt`, `board_policy_g7_grants_data.pdf`, `finance_committee_standard_fc3.pdf`, `award_decisions_fy2021_fy2025.csv`, `disbursements_fy2021_fy2025.csv`, `grantee_directory.tsv`, `grants_office_note_extract.txt`, `average_grant_series_fy2021_fy2024.csv`, `grants_system_field_definitions.txt`, `programme_panels.json`

### Final recommendation

The FY2025 fall in the average grant comes from Education and Learning in Tessel, whose panel is led by Farah Okonkwo. Tessel contributes -$427.55 of the -$811.96 change (52.7 per cent).

### Step-by-step solution

1. Fix the measure from G-7 and FC-3: average grant by fiscal year of award, amount awarded, rescinded awards removed, cents rounded half up, explained with FC-3 midpoint mix and rate pieces, programmes first and counties second.
2. List the candidate drivers: six programmes, the six counties inside the programme the first level selects, and the three Board explanations (the rapid-response stream, Health's return from a one-off, and a fall spread across every panel).
3. Set the counting definition. A grant is one grantee's support under one programme in one fiscal year, with all its award decisions added together, and a payee recorded under the Foundation's own EIN is one of its own fiscally sponsored projects and is not a grant.
4. Confirm the definition against the published series: it reproduces all 24 figures for FY2021 to FY2024 to the cent. Counting per decision reproduces 16, and each half of the correction alone does no better. On this basis the average moves from $27,647.12 to $26,835.16, a fall of $811.96.
5. First level: Education and Learning contributes -$385.60 (mix $6.93, rate -$392.53), Health and Wellbeing -$210.25, Basic Needs -$151.90, and the other three between -$22.14 and -$20.23. The fall is a rate effect inside Education and Learning.
6. Second level inside Education and Learning: Tessel's average grant went from $38,834.24 to $29,027.17, carrying -$427.55 into the Foundation-wide change. Arlow is next at -$1.86, and the remaining counties net to a small rise.
7. Test the Board's explanations. Basic Needs, home of the rapid-response stream, is third at -$151.90, and leaving the stream out reproduces only 21 of the published figures. Health's return from its FY2024 high is second at -$210.25, real but $175.35 short of Education and Learning. The three smallest contributors add -$64.21 together, so the fall is not across the board.
8. Name the leaf: Education and Learning in Tessel, owned by panel lead Farah Okonkwo. The call changes if Education and Learning's contribution rises above -$210.25, or Tessel's above -$1.86.

### Key traps (what the model did)

- Counted each award decision as a grant (and/or kept the Foundation's own fiscally sponsored payees), which inflates the average-grant fall to -$2,576.58 and moves the drill leaf to Youth and Families / Dunmore (panel lead Ingrid Mireles).

### Justification

The answer depends on the counting basis, and G-7 makes the published years the test of that basis. Only per-grantee aggregation with the Foundation's own sponsored projects excluded reproduces all 24 published figures, and on that basis the FC-3 drill enters Education and Learning by a $175.35 margin and lands on Tessel by $425.69, with Tessel alone accounting for more than half of the fall. Each Board explanation fails against a specific figure: the rapid-response stream sits in the third-ranked programme and excluding it breaks the reproduction test, Health is the runner-up rather than the driver, and the three smallest programmes add only 7.9 per cent of the fall.

## Place eleven states on the fy2022 capacity watch, new jersey taking the largest reserve share

**Agricultural Research Grant Allocation**, Batch 14, Nonprofit & Grant Making, model mean **0.36** over 4 runs (0.44, 0.41, 0.39, 0.44).

### What makes it strong (the client's note)

The trap is the Index construction: AR-3.2 names it in words only, and the own-record term alone, a booked-year base or a per-row SBIR exclusion each produce plausible Indexes that do not match the filed register.
The register is the pin: support held per registered grantee (awards held in any part of the year, valued at obligations booked to date, SBIR listing 10.212 excluded on the base transaction), standardised against the state's own four prior cycles and against the fifty states, as 100 plus ten times the sum of the two terms, reproduces all 200 filed cells and the four filed Watch counts (5, 8, 6, 12). The closest variants reproduce 147 and 155 cells.
Neither office note changes the list: the Programme Office's FY2022 bookings basis reproduces no filed cell and would put Illinois on the Watch (its Index is 97.90), and the Grants Office's level per grantee for Hawaii is set aside by AR-3.6 (Hawaii's Index is 96.96).
Determinism pins: eleven states below 90; New Jersey 67.83 with USD 481,738 on a base of USD 61,991,256 across 15 grantees; Washington last on the Watch at 87.04 (USD 64,319); Maine first off at 90.51; fifty-state mean 103.39.

### Stakeholder ask (the prompt, verbatim)

The Trustees sit on the 6th and I have been handed the Watch page for the reserve. AR-3 is the rule we work to and it's in the supplied materials with the extract, the register, the calendar and the rest. The Chair has the Award page and I'm not touching that one.

What I need is the Capacity Watch for FY2022: which of the fifty states go on it, how many that is, and what each of them takes from this cycle's reserve. The Program Office and the Grants Office have both sent notes on the cycle and they don't agree with each other; they're in the supplied materials as received. I need to know whether either of them changes who is on the Watch, and no more than that.

The extract is the federal assistance file the way USAspending publishes it, one row per transaction with its booked year and its amount. The Secretariat pulled it on the 11th and has reconciled it, so work off that and the reference files rather than going back to the site.

(I'm travelling the Monday before the meeting, so in practice I need this by the 2nd.)

Three files back.

capacity_watch_memo.docx, the page the Trustees adopt.
Open with the states on the Watch for FY2022, how many there are, and each state's share of the reserve in whole dollars, largest share first.

Say whether either office's note changes who is on the Watch, and why. Inside the argument, not in an appendix.

Give the Index of the state taking the largest share, to two decimal places, and the support held and the grantee count behind its base for FY2022, as whole numbers.

capacity_watch_table.csv, the grid underneath the memo.
One row per state, all fifty, with the Capacity Index to two decimal places, the rank as a whole number lowest first, a column flagging the states on the Watch, and the reserve share in whole dollars, zero for a state not on the Watch.
rebuild_watch.py, because the Secretariat files the Index from this each cycle and I won't sign a page I can't rerun.
Rebuild the fifty-state table from the extract and the state reference alone.

Print two audit figures alongside it: how many states are on the Watch for FY2022, as a whole number, and the mean Index across the fifty states to two decimal places.

The list and the shares. Not two readings for me to pick between.

### Deliverables

`capacity_watch_memo.docx`, `capacity_watch_table.csv`, `rebuild_watch.py` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (An agricultural trust's Trustees must adopt the FY2022 Capacity Watch: which of the fifty states have a Capacity Index below 90 under allocation rule AR-3, how many there are, and what share of the USD 2,400,000 cycle reserve each receives, and whether either of two conflicting internal office notes changes the list. AR-3.2 describes the Index only in words and defers to the standing method, so it must be rebuilt from a USAspending extract of NIFA assistance transactions for FY2014 to FY2022 and a state reference file, with the Index register of filed values and the award record available as controls. Deliverables are `capacity_watch_memo.docx` (the Watch states, count and shares first, the ruling on the two notes inside the argument, and the largest-share state's Index, support held and grantee count), `capacity_watch_table.csv` (fifty rows with Index, rank, Watch flag and share) and `rebuild_watch.py` (a rebuild of the table that prints the Watch count and the fifty-state mean Index).)

`12 files, 6.5 MB`, `allocation_rule_ar3.docx`, `award_record.csv`, `capacity_index_register.xlsx`, `cycle_brief_2026.md`, `data_dictionary.json`, `extract_log.json`, `internal_assessments.md`, `nifa_assistance_transactions_fy2014_fy2022.csv`, `package_manifest.txt`, `program_reference.csv`, `state_reference.csv`, `trust_calendar.csv`

### Final recommendation

Place eleven states on the FY2022 Capacity Watch: New Jersey (USD 481,738 on an Index of 67.83), Kansas, South Dakota, New York, Colorado, Nevada, Rhode Island, Utah, West Virginia, Massachusetts and Washington; neither office's note changes the list.

### Step-by-step solution

1. Read AR-3: 3.2 names the Index and defers to the standing method, 3.4 excludes SBIR listing 10.212, 3.5 counts grantees by registration, 3.6 rules out the level, 3.9 sets the threshold at 90 and the sharing rule, and 3.1 limits the field to the fifty states.
2. Map transactions to states through state_reference.csv and drop awards whose base transaction is under 10.212.
3. Build each state's base by year: awards whose period of performance runs through any part of the fiscal year, valued at obligations booked through that year, over distinct registrations. Awards with no period of performance are held in no year.
4. Compute the Index as 100 plus ten times the sum of the own-record z-score (against the four preceding cycles, sample standard deviation) and the field z-score (against the fifty states in the year).
5. Replicate the register: all 200 filed cells for FY2018 to FY2021 and the four Watch counts reproduce.
6. Apply to FY2022: eleven states fall below 90, from New Jersey at 67.83 to Washington at 87.04; the fifty-state mean is 103.39.
7. Share the USD 2,400,000 reserve by each state's shortfall below 90 over the sum of the eleven shortfalls (110.45 Index points), rounded to the dollar: New Jersey 481,738, Kansas 322,245, South Dakota 305,079, New York 282,046, Colorado 276,831, Nevada 229,027, Rhode Island 160,145, Utah 116,034, West Virginia 83,006, Massachusetts 79,529, Washington 64,319.
8. Test the two office notes on the same construction: neither puts Illinois or Hawaii below 90, so neither changes the Watch.
9. Report New Jersey's base: USD 61,991,256 of support held across 15 registered grantees.

### Key traps (what the model did)

- Built the Capacity Index from a variant reading of the words-only AR-3.2 definition (booked-year base / own-record term only / per-row exclusion) without checking it against the filed register, giving 12-15 Watch states, NJ Index ~50 instead of 67.83 and a 50-state mean ~98-99 instead of 103.39.

### Justification

AR-3 defers the Index to the standing method, and the filed register is the record of that method. Only the two-term construction on support held reproduces every filed cell and Watch count, so the FY2022 Index values, the eleven-state list and the shares follow from it. The offices' notes rest on a booked-year basis and a level measure that the rule and the register both reject, so they leave the list unchanged.

## Retarget the sop 2025-07 Hours screen to systems at or above 5000 prior-year hours

**Public Library Development Grants**, Batch 14, Nonprofit & Grant Making, model mean **0.37** over 4 runs (0.17, 0.19, 0.17, 0.99).

### What makes it strong (the client's note)

The trap is taking the briefing's pooled +3.69 as the effect of the screen: the posted under-5000 rule would fund the 33 FY2023 openings whose visits per hour fell 3.41, while the 55 at or above 5000 rose 4.40.
Two decoys must be rejected: the briefing's under-18,000 row (+1.27) comes from a superseded 28 Aug draft, and SOP section 2 forbids a second cutoff, so the fix is to change the side of the posted 5000 cutoff, not its level. Refusing is barred because section 1 says the round is funded and a numeric screen must be posted.
The computation chain: unique fscs_key openings from outlet_annual.csv on structure codes 02 and 13, joined to ae_annual.csv at T-1 and T, negative missing codes dropped, sum(visits)/sum(hours) per group, and the split on prior-year hours.
Determinism pins: FY2023 at or above 5000 is 55 systems, 25.77 to 30.17 (+4.40) with 10 moving down; under 5000 is 33 systems, 24.22 to 20.81 (-3.41); the pooled 88 reproduce the briefing at 25.67 to 29.35 (+3.69).

### Stakeholder ask (the prompt, verbatim)

Hale is not reopening whether there is a new-outlet round. The grants are funded. SOP 2025-07 is the assignment rule for who enters that round: adopt it as posted, retarget it, or refuse it. Not a list of libraries, and not a pause of the cycle.

Okonkwo's briefing_fy2023.xlsx treats FY2023 new outlets as the treatment and reads the pooled visits-per-hour movement as the effect of opening. He will take that number into appropriations unless we can say whether that lift holds for the systems the hours screen would actually have assigned into the funded round.

The warehouse dump is the folder. ae_annual.csv and outlet_annual.csv are the returns.

screen_sop.txt is the assignment rule. I have not cleaned anything.

Give me screen_split.png, the one-slide exhibit Hale can put on the wall. Hours-weighted visits per public-service hour, on the new-outlet treatments the briefing used. Show the briefing's claimed effect, and next to it the same before/after movement for openings the screen we are taking to the packet would have assigned into the funded round and for openings it would not have. Units on the axis. Say what period it covers. Mark the briefing figure as the claimed effect, not as the identified effect under the assignment rule.

Then screen_replay.csv, because the board asked for that assignment rule replayed on the openings we already have: who would have been assigned into the funded round versus not, in each year the SOP says to score, not a second briefing.

One row per year the SOP says to score. For each of those years I want the openings the packet assignment would have funded and their visits-per-hour before, after, and change to 2 decimal places; how many of those assigned openings moved down; the openings it would not have funded and their before / after / change to 2 dp; and misses as the SOP defines them.

Put the briefing's pooled claimed effect on the same sheet as a reconciling row, labeled as the briefing, not as the identified effect.

Open the csv with the call: adopt, retarget, or refuse; the hours cutoff we are actually posting, as an integer; and whether assignment into the funded round is under that cutoff or at or above it.

### Deliverables

`screen_split.png`, `screen_replay.csv` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A library development board has funded a new-outlet grant round and must decide whether to adopt, retarget or refuse SOP 2025-07, the hours screen that assigns systems into that round (posted as prior-year public-service hours under 5000). A program analyst's FY2023 briefing reads the pooled +3.69 visits-per-hour movement of 88 new-outlet systems as the effect of opening, and a board member plans to take that figure to appropriations. The analyst must identify openings from outlet structure codes 02 and 13, compute hours-weighted visits per public-service hour from the administrative-entity return for the year before and the opening year, and split the openings on the 5000-hour cutoff for each year the SOP scores (FY2019, FY2022, FY2023, FY2024). They then count assigned openings that moved down and misses as the SOP defines them, and reconcile against the briefing. Deliverables are `screen_split.png` (a one-slide three-bar exhibit with the briefing marked as the claimed effect) and `screen_replay.csv` (call row first, one replay row per scored year, and a labeled briefing reconciling row).)

`14 files, 11.7 MB`, `ae_annual.csv`, `board_notes_20250912.txt`, `briefing_fy2023.xlsx`, `dim_outlet_type.csv`, `dim_region.csv`, `dim_state.csv`, `dim_structure.csv`, `extract_manifest.json`, `field_catalog.json`, `hours_collection_note.txt`, `outlet_annual.csv`, `screen_draft_20250828.txt`, `screen_sop.txt`, `warehouse_changelog.txt`

### Final recommendation

Retarget SOP 2025-07 so that systems with prior-year public-service hours at or above 5000 are assigned into the funded round, keeping the posted 5000 cutoff. Do not adopt the posted under-5000 rule, and do not refuse it.

### Step-by-step solution

1. Load ae_annual.csv and outlet_annual.csv, parse visits, service_hours and fiscal_year as numbers, pad structure_code to two digits and strip fscs_key. Exact duplicate outlet rows sit on structure code 00 and do not affect openings.
2. Read screen_sop.txt: the posted rule assigns systems under 5000 prior-year hours, openings are outlet structure codes 02 and 13, the scored years are FY2019, FY2022, FY2023 and FY2024, the replay governs over the briefing, and refusing or pausing is outside the packet.
3. Read the 28 Aug draft, the changelog and the field catalog: the under-18,000 draft is superseded, negative visits and hours are missing or closed codes, and fscs_key joins the two returns.
4. For each scored year T, take unique fscs_key openings and keep systems with positive visits and hours in both T-1 and T.
5. Compute hours-weighted visits per hour as sum of visits over sum of hours for each group, and the change as after minus before, to 2 decimals.
6. Split on prior-year hours at 5000. Count assigned systems whose own visits per hour fell, and count misses: systems on the priority side with positive prior-year visits and hours and no opening that year.
7. FY2023: 88 openings; at or above 5000, 55 systems, 25.77 to 30.17, +4.40, 10 moved down; under 5000, 33 systems, 24.22 to 20.81, -3.41; 1011 misses.
8. Confirm the briefing: the same 88 pooled give 25.67 to 29.35, +3.69. The under-18,000 row (70 systems, +1.27) belongs to the superseded draft.
9. Other years: FY2019 at or above 5000 -4.96 (41 systems, 29 down) vs under 5000 -13.79, 1144 misses; FY2022 +6.22 (40, 8 down) vs +1.97, 812 misses; FY2024 +0.82 (44, 20 down) vs -4.15, 1080 misses.
10. Make the call: retarget to at or above 5000. Write screen_replay.csv with the call row first and the briefing reconciling row, and draw screen_split.png with three FY2022 to FY2023 bars (briefing +3.69 marked as claimed, assigned +4.40, not assigned -3.41).

### Key traps (what the model did)

- Ran the replay and correctly found that the posted under-5000 screen funds the declining systems, but then chose the veto option (refuse) instead of the repair the rules allow (retarget to at-or-above 5000), and labelled the posted side as 'assigned' so every per-year figure is swapped.
- Misread the SOP's 'misses' definition, reporting ~7,700-8,000 per year instead of ~800-1,150.

### Justification

The briefing's +3.69 is a pooled movement across all 88 FY2023 openings, not the result of the posted assignment rule. Replaying SOP 2025-07 on the openings file shows that the systems it would fund, those under 5000 prior-year hours, saw visits per hour fall 3.41, while the openings at or above 5000 rose 4.40. In FY2019 and FY2024 the larger systems also beat the small ones, and in FY2022 both groups rose but the larger ones rose more. Under SOP section 5 the replay governs. Section 1 rules out refusing, and section 2 rules out adding or moving to a second cutoff such as the superseded 18,000 draft. The only call that matches the evidence and the SOP's limits is to keep the 5000 cutoff and assign at or above it.

## Certify the cottonwood match fund's program year 2023 match at $7,125,986.41, Inside the authorization

**Federal Grant Match Funding**, Batch 14, Nonprofit & Grant Making, model mean **0.38** over 4 runs (0.74, 0.32, 0.34, 0.34).

### What makes it strong (the client's note)

The trap is the unit of obligation: treating each award as one obligation, dated by its award period start, gives 74 awards, a $35,584,782.45 base and a $4,981,869.56 match below the floor, while the Terms define a covered obligation as a funded budget period, and the installment register shows budget periods the award dates miss.
Budget periods are not in any field: they are recovered by decomposing each award's monthly installment postings into runs and matching each run to the one federal action whose amount times 0.14 equals the run total to the cent.
Two other readings fail in opposite directions: every enrolled action as its own obligation pushes the match to $8,797,434.75, above the authorization; certifying each obligation at its opening action alone gives $5,807,686.12, under the floor.
The extract needs cleaning first: 750 repeated November rows and 4,493 zero-dollar actions drop out, and the dual-registered grantee's two UEIs must both be kept.

### Stakeholder ask (the prompt, verbatim)

Give me one number for the Cottonwood Match Fund's program year 2023, the match commitment I certify to the board in November, to the cent. Everything else here is there to back that figure up. It runs on the year's covered federal base at fourteen cents on every federal dollar, and I need to know whether it sits inside the January authorization or we go back to the board. Use the Match Fund Terms' definition of a covered obligation.

Put the figure in a short memo for the board, a word doc. Lead with that figure, then the base, the headroom against the authorization and the obligation count. Then give the ten largest obligations with grantee and agency, and a table of every USDA agency with its covered base, how many obligations it holds and the match. Put a chart under that table, one bar per agency, biggest first, the match written on each bar, and the certified base in the title.

Back it with a CSV, one row per obligation certified for the year, with the grantee, the award, the month its budget period opened, the month it closes, the federal dollars on it and the match on it. Sort it biggest federal amount first and put a total row at the bottom.

And send whatever you ran to build it so we can rerun it from the supplied files. It should print the base, the match, the obligation count and how many extract rows fell out as the repeated November pull and as zero-dollar actions.

### Deliverables

`certify_py2023.py`, `py2023_certification_memo.docx`, `py2023_covered_obligations.csv` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A foundation that matches federal USDA awards to its enrolled grantees at fourteen cents on the federal dollar must certify its program year 2023 match commitment to the board in November, to the cent, and say whether it sits inside the January authorization. From the USAspending FY2023 extract and its November re-pull, the award and grantee dimensions, the Fund's monthly installment register, the Match Fund Terms, the board resolution, the PY2022 restated schedule and a certification worksheet, the analyst must apply the Terms' definition of a covered obligation (a budget period, not an award) and certify the obligations whose budget period opened in the program year. Deliverables are a Word memo (match first, then base, headroom and obligation count, the ten largest obligations, a table of the seven USDA agencies and a bar chart under it with the base in the title), a CSV with one row per certified obligation sorted by federal amount with a total row, and the script that rebuilds the figures and prints the drop counts.)

`19 files, 8.1 MB`, `2_cfr_part_200_uniform_guidance_2023.pdf`, `board_resolution_2023-01.docx`, `data_dictionary.json`, `dim_assistance_type.csv`, `dim_award.csv`, `dim_cfda.csv`, `dim_recipient.csv`, `dim_state.csv`, `dim_subagency.csv`, `enrolled_grantees.csv`, `fact_transactions.csv`, `fact_transactions_repull_2023-11.csv`, `match_fund_terms_2021.docx`, `match_installment_register.csv`, `overview.xlsx`, `py2022_certified_schedule.xlsx`, `py2023_certification_worksheet.xlsx`, `sample_api_payload.json`, `usaspending_cohort_pull_fy2022.csv`

### Final recommendation

Certify the program year 2023 match commitment at $7,125,986.41, fourteen cents on the covered federal base of $50,899,902.82 across 117 covered obligations, inside the $7,950,000 authorization with $824,013.59 of headroom.

### Step-by-step solution

1. Read the Terms: a covered obligation is a funded budget period on an enrolled grantee's federal award, certified in the program year its budget period opens at the federal amount as of 30 September 2023; the match is 14% per obligation, rounded to the cent half-to-even and summed. Resolution 2023-01 authorizes up to $7,950,000 with an eighty percent floor of $6,360,000.
2. Collapse the October extract and the November re-pull on transaction_id (750 repeated rows), drop 4,493 zero-dollar actions, and keep the 39 enrolled grantees by UEI, including both UEIs of the dual-registered grantee.
3. Recover budget periods from the Fund's installment register: split each award's monthly postings into runs, and match each run to the action whose amount times 0.14 equals its total; actions sharing an award and close month form one obligation.
4. Certify the obligations whose budget period opened between October 2022 and September 2023: 117 obligations on 99 awards (18 awards carry two), summing to $50,899,902.82.
5. Compute the match per obligation: $7,125,986.41, leaving $824,013.59 of headroom against $7,950,000 and sitting above the $6,360,000 floor.
6. Roll up by agency: NRCS $19,450,927.98 on 42 (match $2,723,129.90), RUS $9,357,591.08 on 14, Forest Service $7,192,107.70 on 17, NIFA $5,735,199.62 on 14, APHIS $3,528,678.36 on 11, RBCS $3,392,782.86 on 12, AMS $2,242,615.22 on 7.
7. List the ten largest, led by Taylor's Grove Water Association at $2,449,037.99, and build the memo, chart, CSV and script.

### Key traps (what the model did)

- Certified at award grain: one obligation per award, dated by award period start (74-75 obligations), instead of the funded budget periods the Terms define. Budget periods exist only implicitly in the installment register (runs of postings matched to federal actions). The award-level base came out at $35-37M and the match fell below the floor, so the memo said the opposite of the floor criterion.
- Near-miss run: used the right population but still collapsed a multi-period award into one row (99 obligations instead of 117).

### Justification

The Terms make the budget period, not the award, the unit that is certified, and the Fund's own installment register shows exactly where each budget period opened and closed. Certifying the periods that opened in program year 2023 gives a $50,899,902.82 base and a $7,125,986.41 match. That sits $824,013.59 inside the January authorization and above the floor, so the board does not need a further authorization and no balance returns to the open-call pool.

## File the rapid response program extension on $272,018 Unexpended at june 30

**CDFI Award Compliance**, Batch 14, Nonprofit & Grant Making, model mean **0.39** over 4 runs (0.44, 0.31, 0.44, 0.42).

### What makes it strong (the client's note)

The first trap is treating the tracker's $1,501,048 of designated note amounts as expended; the agreement counts only disbursements, and the deduplicated ledger shows $1,157,089 posted through March 31 (tied out by the $782,771 interim report at December 31).
The second trap is timing: posting every remaining draw on its scheduled date gives a $150,651 residual, and a single 18 to 26 day lag gives $184,016. Single-family draws post 18 to 26 days after request (from the ledger), while commercial and multifamily draws post 40 to 50 days after request, an interval that only the SF-425 quarterly cells reveal.
Determinism pins: designated expenditure by June 30 of $1,277,031, coverable eligible closings of $51,000, residual of $272,018, and month-end totals of $1,184,089, $1,292,419, and $1,328,031. All 99 combinations of supported commercial and single-family lags return the same figures and the same per-loan split.
Eligibility screening is the binding constraint on the second piece: only TR-2021-31763, TR-2021-27819, and TR-2021-35265 qualify, because the three own-funded PPC-FA loans belong to the Persistent Poverty Counties objective and FA-funded or PPPLF-funded loans are barred by the other-Federal-award clause.

### Stakeholder ask (the prompt, verbatim)

I run compliance at Two Rivers Community Capital. Our Rapid Response Program award from the CDFI Fund reaches the end of its period of performance on June 30, and the assistance agreement says what counts as expended and what an extension request has to state. At the March close I need the one number that goes in that request: the part of the award that will still be unexpended on June 30 once the loans we have designated finish funding and once we have designated everything else eligible that has closed since the award started. Write me the memo for the credit committee, a Word document, with that residual in whole dollars up front and the two pieces under it, then each loan still funding in either group in the order they finish, what posts by June 30 and what lands after, the award dollars out the door at each month-end through June. Add the chart for the deck as a PNG: cumulative award dollars by month, the remaining months dashed, the eligible closings as their own band, the award drawn as a labeled line, and the residual marked at June 30.

### Deliverables

`rrp_award_position.png`, `rrp_extension_memo.docx` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (The compliance director at Two Rivers Community Capital, a CDFI, is preparing an extension request for its CDFI Fund Rapid Response Program award, whose period of performance ends June 30, 2022. At the March 31 close she needs the one figure the request must state: the part of the $1,600,049 award still unexpended on June 30 after the designated loans finish funding and after every other eligible closing since the award began is designated. The analyst must apply the assistance agreement's expenditure and designation rules, reconcile the cash ledger to the board tracker, project when each remaining construction draw will actually post by calibrating posting lags from the organization's own funding history and from the FA award's SF-425 filings, and identify which own-funded closings can still be designated. The deliverables are a Word memo for the credit committee (residual up front, its two pieces, each loan still funding in finish order with what posts by June 30 and what lands after, and month-end award dollars through June) and a PNG chart of cumulative award dollars with the remaining months dashed, eligible closings as a separate band, a labeled award line, and the residual marked at June 30.)

`15 files, 8.2 MB`, `CDFITLR_Guidance_February_2022.pdf`, `award_cash_ledger.csv`, `construction_draw_schedules.xlsx`, `county_reference.csv`, `data_dictionary.json`, `fa_award_sf425_quarterly_2020_2021.xlsx`, `finance_thread.md`, `loan_disbursement_procedures.docx`, `originations_register.csv`, `overview.xlsx`, `purpose_codes.csv`, `rrp_assistance_agreement_schedule.docx`, `rrp_deployment_tracker_2022q1.xlsx`, `rrp_interim_report_2021h2.xlsx`, `transaction_type_codes.csv`

### Final recommendation

File the Rapid Response Program extension on $272,018 still unexpended at June 30, 2022: of the $1,600,049 award, $1,277,031 will have gone out on the designated book and designating the eligible closings covers another $51,000.

### Step-by-step solution

1. Read Schedule 1 of the assistance agreement: award funds are expended only when disbursed to a borrower on a product designated to the award (prior own-fund disbursements count once designated); commitments and closings do not count; a transaction funded from another Federal award cannot be designated. The award is $1,600,049; the period runs July 1, 2021 to June 30, 2022.
2. Take the 31 RRP-FA designations in the period as the designated book ($1,501,048 of notes). Deduplicate the ledger's second extract pull and total RRP postings through March 31: $1,157,089. RRP postings through December 31 total $782,771, matching the interim report.
3. Find each open designated construction loan's scheduled draw requests that have no ledger posting yet.
4. Join the ledger to the draw schedules on loan and draw number for completed loans. Single-family construction and rehab progress draws post 18 to 26 days after request; closing advances post 0 to 2 days after the note.
5. Shift the request schedules of the FA-funded commercial and multifamily loans onto the eight SF-425 quarterly federal-share cells. Every shift from 40 to 50 days reproduces all eight cells; 39, 51, 18 to 26, 60, and 90 days do not.
6. Project remaining single-family draws at 18 to 26 days and remaining commercial draws at 40 to 50 days. Designated expenditure by June 30 is $1,277,031.
7. Identify eligible closings: own-funded loans closed in the period that are not PPC-FA and not funded from another Federal award, namely TR-2021-31763, TR-2021-27819, and TR-2021-35265, totaling $51,000, all disbursed by June 30.
8. Residual = $1,600,049 minus $1,277,031 minus $51,000 = $272,018, identical across all 99 lag combinations.
9. List the ten loans still funding in finish order (TR-2021-31763 in May; six commercial loans in July; three single-family loans in August) with what posts by June 30 and what lands after, and report month-end totals of $1,184,089 (April), $1,292,419 (May), and $1,328,031 (June).
10. Chart cumulative award dollars July 2021 through June 2022 with April to June dashed, eligible closings as a separate band, the award as a labeled line, and the residual marked at June 30.

### Key traps (what the model did)

- Projected June 30 cash by applying the single-family 18-26 day draw-to-post lag observed in the ledger to every remaining draw (3 runs), or by posting draws on their scheduled dates (1 run), so late-May commercial draws were counted as expended before June 30.
- All month-end totals (April $1,268k vs $1,184k, May $1,328k vs $1,292k) were shifted early by the same uniform-lag assumption.

### Justification

The extension request has to state what will actually be unexpended, and under the agreement that is a cash question, not a designation question. The tracker overstates deployment because open construction notes are counted at full note value, and the scheduled draw dates overstate June 30 cash because draws post only after inspection. The organization's own history shows that lag is 18 to 26 days for single-family projects, but commercial projects certified by an engineer of record take 40 to 50 days, which pushes the late-May commercial draws past June 30. With the three eligible own-funded closings designated, $272,018 remains, and that figure does not move anywhere inside the lag ranges the evidence supports.

## Project fy2026 massachusetts 501(C)(3) Revenue at usd 189.57 Billion using the benchmark-certified 5.184732% Growth rate

**Charitable Sector Revenue Outlook**, Batch 14, Nonprofit & Grant Making, model mean **0.42** over 3 runs (0.37, 0.47, 0.44).

### What makes it strong (the client's note)

The trap is the obvious extrapolation: compounding the continuing cohort's aggregate total revenue CAGR (5.333764%) gives USD 190.38 billion, but that construction reproduces none of the eight certified subsector rates and overstates the outlook by USD 0.81 billion.
The computation chain runs from 105,459 raw returns through 501(c)(3) filtering, the 365-day full-period rule, latest-filed and later-period-end tie breaks, a 7,838-organization continuing cohort, and a 4,719-organization panel with at least USD 100,000 of 2018 core operating revenue.
Determinism pins: the register's eight rates match only core operating revenue (contributions plus program service revenue) above the USD 100,000 threshold, which yields 5.184732% (USD 109.47 billion to USD 140.95 billion) and a FY2026 figure of USD 189,569,635,531.
The binding constraint is the base: the rate is measured on the continuing panel but applied to the full-sector 2023 total of USD 162,896,088,056 across 13,759 filers, not the continuing-cohort subtotal of USD 155.42 billion.

### Stakeholder ask (the prompt, verbatim)

The association's sector outlook goes to the board on Friday and I need help calculating the FY2026 figure, that is the combined total revenue for Massachusetts 501(c)(3) organizations, three years out from our 2023 reference year.

The scope file and the benchmark projections register lay out what the board has settled, including who counts as continuing, the reference window, and our certified subsector growth rates.

I will also need you to give me three files. First, ma_sector_outlook_fy2026.pdf for the board materials. Lead with the FY2026 figure and the growth rate behind it, how many organizations the rate is measured over, the annual revenue series from 2018 to 2023, the reconciliation against our benchmark register, and the comparison against the uncalibrated extrapolation. The next one is ma_sector_revenue_series.xlsx so the finance team can audit the calculations: the annual revenue series, every organization standing behind the growth rate with its revenue, and the benchmark register. And finally, ma_sector_revenue_series.png, a slide visual showing historical sector revenue and the forward projection to FY2026 alongside the certified subsector benchmarks.

### Deliverables

`ma_sector_outlook_fy2026.pdf`, `ma_sector_revenue_series.xlsx`, `ma_sector_revenue_series.png` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A Massachusetts nonprofit association needs the FY2026 combined total revenue figure for all Massachusetts 501(c)(3) organizations for a board sector outlook, three years out from a 2023 reference year. The scope file fixes the reference window (2018 to 2023), the return-of-record rules, the continuing-filer definition, and a certification standard: a growth construction is admissible only if it reproduces all eight certified subsector rates in the benchmark projections register to six decimal places. The analyst must resolve IRS Form 990 and 990-EZ filings to one full-year return of record per organization and year, build the 2018 to 2023 sector revenue series, find the construction that reproduces the register, measure its growth rate on the continuing panel, compound it three years from the full-sector 2023 base, and compare the result against the uncalibrated extrapolation. Deliverables are `ma_sector_outlook_fy2026.pdf` (board memo leading with the FY2026 figure and rate), `ma_sector_revenue_series.xlsx` (series, every panel organization with its revenue, and the register), and `ma_sector_revenue_series.png` (history, projection, and subsector benchmarks).)

`22 files, 45.0 MB`, `benchmark_projections_register.csv`, `exempt_organizations_master_ma.csv`, `file_manifest.csv`, `returns_financials_2017.csv`, `returns_financials_2018.csv`, `returns_financials_2019.csv`, `returns_financials_2020.csv`, `returns_financials_2021.csv`, `returns_financials_2022.csv`, `returns_financials_2023.csv`, `returns_financials_2024.csv`, `returns_header_2017.csv`, `returns_header_2018.csv`, `returns_header_2019.csv`, `returns_header_2020.csv`, `returns_header_2021.csv`, `returns_header_2022.csv`, `returns_header_2023.csv`, `returns_header_2024.csv`, `i990.pdf`, `i990ez.pdf`, `sector_outlook_scope.json`

### Final recommendation

Report FY2026 combined total revenue for Massachusetts 501(c)(3) organizations of USD 189,569,635,531: the full-sector 2023 base of USD 162,896,088,056 compounded three years at the benchmark-certified 5.184732% rate measured over 4,719 organizations.

### Step-by-step solution

1. Read the scope file and benchmark register: reference window 2018 to 2023, three-year horizon to FY2026, full-sector base, the uncalibrated comparison definition, and eight certified subsector rates.
2. Keep returns of organizations recorded as 501(c)(3) in the master file, drop tax periods under 365 days, keep the latest-filed return per tax period, and keep the later-ending period when two end in the same calendar year. Filers of record: 9,298 (2018), 9,985 (2019), 11,044 (2020), 12,552 (2021), 13,455 (2022), 13,759 (2023).
3. Sum Part I total revenue by period-end year: USD 121.44 billion (2018), 126.64 (2019), 131.00 (2020), 154.63 (2021), 165.46 (2022), and USD 162,896,088,056 (2023).
4. Form the continuing cohort of organizations with a return of record and reported total revenue in all six years: 7,838 organizations.
5. Test candidate constructions against the register. Only core operating revenue (Part I lines 8 plus 9) for continuing organizations with at least USD 100,000 of 2018 core revenue, aggregated over 2018 to 2023, reproduces all eight certified rates.
6. Apply that rule: 4,719 organizations qualify (3,119 fall below the threshold).
7. Compute the panel CAGR: core revenue grows from USD 109,472,649,402 to USD 140,951,324,918, a rate of 5.184732% a year.
8. Compute the uncalibrated comparison: the continuing cohort's total revenue CAGR of 5.333764% compounded from the full-sector base gives USD 190,376,556,658, USD 806.9 million above the certified figure, and fails all eight register rates.
9. Compound the full-sector 2023 base three years at 5.184732%: USD 189,569,635,531.
10. Deliver the board PDF, the audit workbook, and the slide chart.

### Key traps (what the model did)

- Correctly rejected the raw total-revenue CAGR but stopped at a near-miss calibrated construction (operational revenue over the 7,838 continuing cohort, no $100k 2018 floor), accepted residual differences against the certified subsector register, and reported 5.227%/5.267% and $189.80-190.01bn.

### Justification

The scope makes the register the admissibility test, so the growth rate has to come from the one construction that reproduces every certified subsector rate, and that construction is core operating revenue for the continuing panel above USD 100,000. The raw total revenue CAGR is easier to compute but fails every subsector check because it carries non-operating swings, and it would overstate the outlook by USD 0.81 billion. The scope also says the rate applies to the full sector's 2023 revenue across all filers of record, so the base is USD 162.90 billion rather than the USD 155.42 billion continuing-cohort subtotal. Together these give USD 189,569,635,531.

## Fund the 2027 cost relief pilot for housing in florida, the widest lowest-to-highest quintile burden gap

**Household Cost Burden Pilot Targeting**, Batch 14, Nonprofit & Grant Making, model mean **0.46** over 4 runs (0.44, 0.47, 0.94, 0.49).

### What makes it strong (the client's note)

The trap is the runner-up: Texas-Housing overtakes Florida-Housing on three plausible shortcuts, and each is closed by the official material. Omitting the ITBI files drops hierarchy leaves that exist only there (Personal insurance and pensions UCCs 800910 to 800940, finance charges 005420, 005520 and 005620) and gives Texas about 7.13 pp; a collection-year Interview window ignores the reference-month guidance and REF_YR and gives Texas about 12.58 pp; re-ranking quintiles within each state departs from the INC_RNKM rule in the CE guide and gives Texas about 11.25 pp.
The computation chain: read the integrated hierarchy (14 major categories, 645 leaves, 398 Interview and 247 Diary), select 283,524 MTBI, 18,052 ITBI and 102,416 Diary records for the four supported states, apply the hierarchy factor of 4 to UCCs 005420, 005520 and 005620, compute state-weighted calendar-year annual means by INC_RNKM quintile from 2022 reference months, convert Diary weekly means to annual, integrate, and take shares of the 14-category total.
Determinism pins: Florida-Housing 43.571087% (Q1) and 31.879581% (Q5), contrast 11.691506 pp; Texas-Housing 11.540349 pp; lead 0.151157 pp (1.309814% relative); Housing leads every state (New York 10.026094, California 8.826497); out-of-scope pick Florida-Healthcare 7.091393 pp; lowest-quintile-only keeps Florida-Housing at 43.571087%, with California-Housing second at 43.142046%.
The binding constraint is the lead of 0.15 pp, so the result holds only on the pinned method, and the brief must state limitations: state weights for four states only, no state-level replicate weights, independent Interview and Diary samples, thin cells (Florida Q5 Diary 102 consumer units) and 2022 evidence for a 2027 decision.

### Stakeholder ask (the prompt, verbatim)

The Community Cost Relief Foundation has funding for one state pilot in 2027. The program can be built around a major household spending category, but the board wants the choice grounded in where lower-income consumer units face the clearest disproportionate burden.

Using only the supplied official 2022 Consumer Expenditure materials, recommend the supported state and official major expenditure category where that category absorbs the widest additional share of total integrated annual mean consumer-unit expenditures in the lowest imputed-income quintile compared with the highest. Cover every supported state and every major expenditure category identified by the official integrated hierarchy.

The board also needs answers to four operating questions: How far does the recommendation lead the runner-up? Which category has the largest directional contrast within each supported state? If the recommended category were outside the foundation's program authority, which state-category pair among the remaining categories would receive the pilot? Would the recommendation change if the board prioritized the largest lowest-quintile category share instead of the contrast between the two ends of the distribution?

Deliver exactly these four items:

state_category_pilot_brief.pdf
Put the recommended state-category pair, its lead over the runner-up, and a short funding rationale on the opening page.
Show the selected pair and runner-up across all five imputed-income quintiles, with one clear distribution chart and one comparison chart covering the strongest pairs.
Answer all four operating questions, including the recommended-category-out-of-scope and lowest-quintile-only scenarios, and explain any change in recommendation.
Describe what the official materials contribute, document the evidence supporting the result, and state the limitations that matter for a 2027 pilot decision.
state_category_profile.csv
Provide one row for every supported state, official major expenditure category, and imputed-income quintile; do not omit categories or intermediate quintiles.
Carry the annual category mean, annual total mean, category share, and the identifiers needed to connect each row to the recommendation.
Include the supporting sample and represented-population diagnostics needed to judge thin or unstable cells.
Include concise provenance and reconciliation indicators so another analyst can trace each estimate to the supplied official material and detect incomplete coverage.
state_category_ranking.csv
Provide one row for every supported state-category pair and preserve the directional lowest-minus-highest contrast, including negative results.
Include the endpoint shares, complete overall ordering, selection status, runner-up status, and the recommendation's lead.
Report the leading category within each state and enough comparison detail to verify that the full state-category universe was considered.
Identify the state-category pair that would receive the pilot if the recommended category were out of scope, and clearly indicate whether the lowest-quintile-only scenario changes the recommended state-category pair.
reproduce_pilot.py
Use only the Python standard library and accept the supplied input directory (or a ZIP of it) as input.
Recreate both CSV deliverables and the PDF from the official source material without storing the recommendation or any result as a constant.
Validate the input inventory, coverage of supported states, complete official category universe, all five quintiles, key uniqueness, numeric integrity, and the reconciliations reported in the deliverables; stop with a useful error when a check fails.
Print a compact decision summary and validation summary, and produce deterministic outputs suitable for independent review.
The written brief should be concise and board-ready. Keep technical detail in the evidence tables and reproducibility checks rather than turning the brief into a methods manual.

### Deliverables

`state_category_pilot_brief.pdf`, `state_category_profile.csv`, `state_category_ranking.csv`, `reproduce_pilot.py` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A cost relief foundation can fund one state pilot in 2027 built around a major household spending category, and its board wants the state-category pair where that category takes the widest additional share of total spending in the lowest imputed-income quintile compared with the highest. Using only the official 2022 Consumer Expenditure Survey public-use files (Interview and Diary microdata, the research state weights, the integrated stub hierarchy and BLS documentation), the analyst must cover every supported state and every major category, name the pair, and answer four operating questions: the lead over the runner-up, the leading category in each state, the pick if the recommended category were out of scope, and whether a lowest-quintile-only rule would change the result. Deliverables are `state_category_pilot_brief.pdf` (a board brief with the recommendation and lead on the opening page, a five-quintile distribution chart and a strongest-pairs comparison chart), `state_category_profile.csv` (280 state, category and quintile rows with means, shares, sample and population diagnostics and provenance), `state_category_ranking.csv` (56 signed contrasts with ranks, flags and scenario results) and `reproduce_pilot.py` (a standard-library script that regenerates all three from the inputs with validation checks).)

`36 files, 269.4 MB`, `CE-HG-Integ-2022.txt`, `Interview__cawgt22.csv`, `Interview__flwgt22.csv`, `Interview__nywgt22.csv`, `Interview__txwgt22.csv`, `cawgt22.csv`, `ce-pumd-interview-diary-dictionary.xlsx`, `csxguide.pdf`, `expd221.csv`, `expd222.csv`, `expd223.csv`, `expd224.csv`, `flwgt22.csv`, `fmld221.csv`, `fmld222.csv`, `fmld223.csv`, `fmld224.csv`, `fmli221.csv`, `fmli222.csv`, `fmli223.csv`, `fmli224.csv`, `fmli231.csv`, `itbi221.csv`, `itbi222.csv`, `itbi223.csv`, `itbi224.csv`, `itbi231.csv`, `mtbi221.csv`, `mtbi222.csv`, `mtbi223.csv`, `mtbi224.csv`, `mtbi231.csv`, `nywgt22.csv`, `pumd_novice_guide.pdf`, `stateweights-documentation.pdf`, `txwgt22.csv`

### Final recommendation

Fund the 2027 pilot for Florida-Housing: Housing takes 43.57% of total integrated annual mean expenditures in Florida's lowest imputed-income quintile against 31.88% in the highest, an 11.69 percentage point contrast that leads runner-up Texas-Housing (11.54 pp) by 0.15 pp.

### Step-by-step solution

1. Validate the 36 official files (31 CSV, one TXT hierarchy, one XLSX dictionary, three PDFs) and take the supported states from the state-weight files: California, Florida, New York and Texas.
2. Read the integrated hierarchy: 14 major categories over 645 leaves, each tagged Interview or Diary, with a factor of 4 on UCCs 005420, 005520 and 005620.
3. Assemble the five Interview quarters (2022 Q1 to 2023 Q1), keep 2022 reference months from MTBI and ITBI, and link state weights: 283,524 MTBI and 18,052 ITBI records selected.
4. Assemble the four 2022 Diary quarters with state weights (102,416 records) and convert weekly means to annual.
5. Assign quintiles by INC_RNKM cut at 0.20 steps, compute state-weighted annual category means for every state, quintile and category, integrate Interview and Diary, and take shares of the 14-category total (280 profile rows, each state and quintile reconciling to 100%).
6. Compute the signed lowest-minus-highest contrast for all 56 pairs: Florida-Housing 11.691506 pp first, Texas-Housing 11.540349 pp second, a lead of 0.151157 pp; Personal insurance and pensions is negative in every state (-12.45 to -15.48 pp).
7. Answer the operating questions: Housing leads in every state; with Housing out of scope the pilot goes to Florida-Healthcare (7.091393 pp, New York-Healthcare second at 5.722090); on lowest-quintile share alone Florida-Housing stays first at 43.571087%.
8. Report the five-quintile profiles (Florida-Housing 43.57, 40.98, 39.29, 31.36, 31.88%; Texas-Housing 42.21, 35.81, 31.54, 31.56, 30.67%), the support counts and represented populations, and the limitations, in the brief, CSVs and script output.

### Key traps (what the model did)

- Used one of the plausible-but-wrong CE construction shortcuts (reference-period window / quintile assignment / leaf coverage) so the endpoint shares drifted (FL Q1 means below range, Texas contrast ~13.2 pp) and the 0.15 pp margin flipped to Texas-Housing; every run also overstated the lead (0.30 to 2.55 pp).

### Justification

The board's rule is the widest gap between the lowest and highest quintile in a category's share of total spending, computed on the official integrated hierarchy. Built the way the BLS materials specify, with every Interview leaf including those only in ITBI, calendar-year 2022 reference months and INC_RNKM quintiles, Florida-Housing has the widest gap of the 56 pairs and stays first under the lowest-quintile-only test. Its lead over Texas-Housing is small, so the brief presents the choice as descriptive prioritization with its limitations stated, not as proof that Florida's burden is statistically larger.

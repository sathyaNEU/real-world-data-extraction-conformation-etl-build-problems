# task173 submission

## Tags

**Domain:** Business & Operations Analytics, workforce and labour planning (a live tax-expert service's outsourced hours for the filing deadline).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Book 10,000 agent hours with Hillsborough Contact Services for the 2027 deadline fortnight.**
The fortnight's 47,169 new cases will bring 1.292 contacts a case, 60,949 in all, and the hours Hillsborough's agents need to carry what the bench cannot, with their own cases coming back at 33.0 per cent, come to 9,420, so the order is the next whole block. Not 7,000 hours from last season's 1.207 contacts a case, which a far more experienced bench produced. Not 9,000 from comeback rates by group with this year's classes at last season's average, which came from classes much longer on the queue than this year's four will be. Not 9,000 from booking Hillsborough's hours as capacity that opens no cases of its own.

## 2. Critical Components

1. Over the 2026 season a case came back **13.9%** of the time when a returning expert opened it and **33.0%** when a Hillsborough agent did; a follow-up came back **18.1%** whoever took it.
2. A class expert's cases come back about **41%** of the time in their first week on the queue, falling to about **20%** by the tenth.
3. The 2027 fortnight's cases bring **1.29** contacts each, about **61,000** in all, against **1.21** a case in the 2026 fortnight.

## 3. Step-by-Step Solution

1. Took the load, capacity and order rules from expert_capacity_planning_standard.docx: every contact on the cases opening 19 April to 2 May 2027, 67.32 handle hours an in-house expert, 0.85 a billed Hillsborough hour, whole blocks of 1,000 rounded up.
2. Took the bench from seasonal_expert_roster_2027.xlsx (150 confirmed English-queue experts) and training_calendar_2027.pdf (four classes of 60 going live 15 February, 1 March, 29 March and 12 April), and 47,169 new cases from the fortnight's days in demand_plan_2027.xlsx.
3. Linked each English-queue case in crm_expert_interactions_2026.csv from its opening interaction to its later ones and each handler to the roster: returning experts' cases came back 13.9% of the time, Hillsborough's 33.0%, a follow-up 18.1% whoever took it.
4. Fitted the class experts' comeback chance and handle time on their weeks on the queue, from 40.6% and 42.1 minutes in the first week to 19.5% and 32.2 minutes by the tenth, against 30.6 minutes for returning experts and 35.1 for Hillsborough's agents.
5. Back-tested the model on the old system's weekly reports (ticketing_agent_weekly_2021_2022.csv, ticketing_agent_weekly_2023_2025.csv, through seasonal_expert_history.csv): within 1.3% of each season's follow-ups per new ticket and 3.6% of each deadline fortnight's, where carrying the 2026 rate missed by up to 9.9% and 13.0%.
6. Read the four classes at their weeks in the 2027 fortnight: the bench carries 47,266 contacts at its handle hours.
7. Solved for the billed Hillsborough hours whose contacts, with the cases they open coming back at 33.0%, carry the rest of the load: 9,420 hours, 60,949 contacts in all at 1.292 a case.
8. Rounded up to the next block of 1,000: book 10,000 agent hours.

## 4. Deliverable Answers

### deadline_fortnight_plan_2027.xlsx

1. Booking with Hillsborough Contact Services for the 2027 deadline fortnight: 10,000 agent hours.
2. Billable hours our ACD records show for Hillsborough's agents, by day of the 2026 deadline fortnight (hours, one decimal):
   - 2026-04-20 (Monday): 299.2
   - 2026-04-21 (Tuesday): 209.8
   - 2026-04-22 (Wednesday): 202.6
   - 2026-04-23 (Thursday): 229.6
   - 2026-04-24 (Friday): 255.6
   - 2026-04-25 (Saturday): 209.1
   - 2026-04-26 (Sunday): 184.6
   - 2026-04-27 (Monday): 293.3
   - 2026-04-28 (Tuesday): 328.5
   - 2026-04-29 (Wednesday): 343.0
   - 2026-04-30 (Thursday): 393.9
   - 2026-05-01 (Friday): 117.1
   - 2026-05-02 (Saturday): 81.6
   - 2026-05-03 (Sunday): 68.0
3. Hours Hillsborough invoiced that the ACD records do not support, agent by agent, by invoice week (hours, one decimal):
   - Week of 2026-04-20 (Monday): 53.7
   - Week of 2026-04-27 (Monday), against the replacement invoice: 54.7
4. Average wait of the English-queue customers an expert answered, by day (whole seconds):
   - 2026-04-20 (Monday): 48
   - 2026-04-21 (Tuesday): 73
   - 2026-04-22 (Wednesday): 100
   - 2026-04-23 (Thursday): 105
   - 2026-04-24 (Friday): 85
   - 2026-04-25 (Saturday): 228
   - 2026-04-26 (Sunday): 224
   - 2026-04-27 (Monday): 127
   - 2026-04-28 (Tuesday): 173
   - 2026-04-29 (Wednesday): 129
   - 2026-04-30 (Thursday): 166
   - 2026-05-01 (Friday): 271
   - 2026-05-02 (Saturday): 44
   - 2026-05-03 (Sunday): 33
5. Share of answered customers answered within three minutes, by week (per cent, one decimal):
   - Week of 2026-04-20 (Monday): 78.8%
   - Week of 2026-04-27 (Monday): 74.5%

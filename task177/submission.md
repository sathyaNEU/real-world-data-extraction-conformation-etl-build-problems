## Tags

**Domain:** Psychology and behavioural science (decision-making and computational behavioural modelling).
**Analytical objective:** Forecasting and predictive modelling.

## 1. Final Recommendation

**Jobseekers on the register on 3 January 2027 will start 26 per cent of their own contacts between 1 March and 25 April 2027 in Ask Prairie Works.**
Not the 40 per cent one learning rate for every contact gives: overflow transfers, the record's only contacts a jobseeker did not choose, teach about a fifth as much as a chosen conversation, and the assistant-first weeks are made of such contacts. Not the 14 per cent of the last eight weeks of 2026, which ignores what the assistant-first weeks teach.

## 2. Critical Components

1. An overflow transfer moves a jobseeker's later choices **about a fifth** as far as a conversation they opened
2. During the assistant-first weeks those jobseekers start **18 per cent** of their own contacts in the assistant

## 3. Step-by-Step Solution

1. Built each jobseeker's contacts from contact_legs_2026.csv (claimant-line calls by the case number on the first leg, overflow transfers as the calls they came from with the voice session's end state) and assistant_sessions_2026.jsonl (app and web conversations through the accounts in contact_details_crosswalk.csv, a conversation's outcome its last session's end state): 413,866 contacts, 11,154 of them transfers.
2. Fitted by maximum likelihood a reinforcement-learning model of each jobseeker's choices (each channel's value starting at 0.5 and moved toward the outcome, 1 resolved or 0 not, of each contact that met it; the choice a logistic of the value gap with a lean and a pull to the last channel chosen) with a separate learning rate for transfers: the transfers' rate is about a fifth of the chosen rate, and the model fits the whole record more than 1,300 log-likelihood units better than one rate.
3. Took the jobseekers with a claim open on 3 January 2027 in claims_register_2026.csv, each from the end state of their own record.
4. Simulated 4 January to 25 April 2027 per assistant_first_rollout_plan.pdf: every call met by release 4.0 resolving 2,041 of 2,400 as in release4_acceptance_summary.pdf to 28 February (18 per cent of their own contacts started in the assistant), then the line back to advisers with the 2026 transfer share, check-ins every 14 days from each claim's opening and other contacts at the 2026 rate: 26 per cent of their own contacts in the window started in the assistant.
5. Counted the conversations in assistant_sessions_2026.jsonl once each, in the month their first session started, employer-widget times (written in UTC, as their hours and the employer line's calls a few minutes later show) moved to Manitoba time, with the employer accounts registered to Prairie Works Manitoba's own business number (812447093, on usage_tier_order_form_2027.pdf) and the accounts the vendor re-typed as staff on 14 September counted as our own use for the whole year, and the staff-console accounts registered to Riverlot's business number (724906318, its GST/HST number on vendor_invoices_2026.xlsx) left out as the vendor's own support desk: the monthly counts below.

## 4. Deliverable Answers

### assistant_share_forecast_mar_apr_2027.xlsx

1. Share of their own contacts jobseekers on the register on 3 January 2027 start in Ask Prairie Works, 1 March to 25 April 2027: 26 per cent
2. Employers' conversations with Ask Prairie Works, by month of 2026:
   - January: 945
   - February: 1,040
   - March: 1,555
   - April: 1,686
   - May: 1,850
   - June: 1,852
   - July: 1,660
   - August: 1,399
   - September: 1,838
   - October: 1,794
   - November: 1,799
   - December: 1,203
3. Our own staff and test accounts' conversations, by month of 2026:
   - January: 1,256
   - February: 1,148
   - March: 1,326
   - April: 1,171
   - May: 1,163
   - June: 1,217
   - July: 1,332
   - August: 1,161
   - September: 1,224
   - October: 1,208
   - November: 1,252
   - December: 1,244

### assistant_first_aftermath_note.docx

1. The forecast of 26 per cent with the reason it is below the one-rate figure of 40 per cent, the chart of the 2026 monthly share against both forecasts, and the inputs it rests on.

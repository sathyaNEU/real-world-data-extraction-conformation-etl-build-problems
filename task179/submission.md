## Tags

**Domain:** Epidemiology & Public Health, infectious disease transmission modeling (renewal-equation projection under a control scenario).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Plan the treatment centres for about 5,000 new cases (confirmed and probable, by onset) in weeks 49 to 52.**
Read against the time each source had to the 11 October cut-off, the transmission links give a 13-day serial interval and a reproduction number of 1.6 for weeks 36 to 41, so even with transmission halved from 2 November December still brings about 5,000 cases. Not 4,000, which the links taken as they stand give (11 days, 1.5): a link is entered only once its case has fallen ill, so the long intervals of September's and October's sources are missing from the extract.

## 2. Critical Components

1. Mean serial interval, right-truncated at 11 October: **13 days**
2. Reproduction number implied by the growth of onsets over weeks 36 to 41: **1.6**
3. New cases in weeks 49 to 52 under the central scenario: **5,000**

## 3. Step-by-Step Solution

1. From tvd_line_list_dunmarrow_2026-10-18.csv, kept Confirmed and Probable rows, counted a case notified twice under two numbers once by its sample_id, and built daily onsets to 11 October (complete to that date per the planning note).
2. From tvd_transmission_links_2026-10-18.csv, joined each Source person and Target person to those cases (a duplicate number mapped to the first) and kept the 2,449 pairs whose case fell ill by 11 October.
3. Fitted a discretised gamma serial interval by maximum likelihood with each pair conditioned on its interval being no longer than 11 October less its source's onset: mean 13 days (the same pairs read as complete give 11).
4. Fitted the log-linear growth of daily onsets over 31 August to 11 October (0.038 a day) and converted it through that interval to a reproduction number of 1.6, the central scenario's base in planning_note_phase3_2026-10-19.pdf.
5. Ran the renewal equation forward from 12 October on daily onsets with the reproduction number halved for every source with onset from 2 November, and summed 30 November to 27 December: 5,000 cases.
6. In contact_registry_dunmarrow_w36-w42.csv, grouped listings into people by district, household_code, initials, sex and age_years, then joined each PHD paper listing to the LMR tablet listing of the same source_case_number, household, initials and sex listed within a day of it with the age one to three years apart (the paper form's estimate); took the people whose first listing fell 7 to 27 September and counted a person completed when a listing of theirs ending on their last follow_up_end closed Follow-up completed (either team, per the planning note).
7. In tamberlow_field_lab_pcr_w36-w42.xlsx, kept Diagnostic rows, took each sample's final result (the re-run after Indeterminate), and added one hour to Result time (analyser), which runs on UTC (otherwise some results land less than the 92-minute cartridge run after reception, and positives fall on the day before the line list's lab_result_date); averaged collection to final result by ISO week of collection.
8. Plan for about 5,000 new cases in weeks 49 to 52.

## 4. Deliverable Answers

### tvd_projection_w49-w52.xlsx

1. New cases in weeks 49 to 52 under the central scenario: 5,000
2. Reproduction number the projection starts from: 1.6
3. Mean serial interval behind it: 13 days
4. Contacts first listed in weeks 37 to 39, different people and percentage who completed follow-up:
   - Tamberlow: 3,416 people, 73.4%
   - Quillmarsh: 2,154 people, 72.7%
   - Kettlebank North: 1,025 people, 65.1%
   - Brindlecourt: 491 people, 73.3%
5. Tamberlow field laboratory, diagnostic samples by week of collection, average hours from collection to final result and percentage resulted within 24 hours:
   - Week 38: 12.7 hours, 87.2%
   - Week 39: 12.9 hours, 85.7%
   - Week 40: 14.1 hours, 81.1%
   - Week 41: 14.8 hours, 80.2%

### tvd_projection_curve.svg

1. Bar chart of weekly cases by week of onset from week 30, observed to week 41 and projected to week 52, with the start of phase 3 (2 November, week 45) marked by a dashed line and weeks 49 to 52 shaded.

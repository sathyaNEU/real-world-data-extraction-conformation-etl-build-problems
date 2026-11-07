## Tags

**Domain:** Epidemiology and public health, disease surveillance and outbreak anomaly detection.
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**Take boundary main WM55081 (Ferndale to Kowhai Hills) out of service before the Kowhai Hills feed main renewal.**
Its water reached the confirmed cases at 189.5 per hundred thousand resident-days in the 1 to 12 days before onset, against 10.6 for the runner-up, Kowhai Hills Reservoir. Not Kowhai Hills Reservoir, which the supply zone register gives as the source of the two worst zones but which was not supplying them from 4 to 6 October, after heavy rain, when they drew Ferndale Road's water through the boundary main.

## 2. Critical Components

1. Confirmed cases among residents with onset from 1 September to 18 October 2027: **68**
2. Boundary main WM55081 reached **61** of them, at **189.5** per hundred thousand resident-days
3. Kowhai Hills Reservoir reached **62**, at **10.6** per hundred thousand resident-days

## 3. Step-by-Step Solution

1. Kept the confirmed cases among residents with onset from 1 September to 18 October 2027 in case_line_list_cryptosporidiosis_2027.xlsx (terms of reference sections 3 and 4) and placed each in its supply zone through its meshblock in meshblock_usually_resident_2023_by_supply_zone.csv: 68 cases.
2. Rebuilt each zone's supply for each day from valve_operations_2027-07-01_2027-10-18.csv read through network_model_export_2027-10-01.xlsx: a trunk main shut when one of its isolation valves was closed for most of the day, a boundary main open when its boundary valve was open for most of the day, each zone inlet traced over open mains back to its reservoir.
3. For each reservoir and boundary main, counted the cases whose zone received its water on any of the 1 to 12 days before onset and divided by the census residents of the zones it supplied, summed over 20 August to 17 October (section 4): boundary main WM55081 189.5 per hundred thousand resident-days on 61 cases, Kowhai Hills Reservoir 10.6 on 62.
4. Ranked the assets with five or more cases (section 4): boundary main WM55081 first, Kowhai Hills Reservoir the runner-up.
5. Applied the planned operations in kowhai_hills_feed_main_renewal_plan_revB.pdf to the network model: boundary main WM55081 would supply Kowhai Hills, 6,843 residents.
6. Ask 1: counted residents with a specimen in community_lab_faecal_parasites_2027-07-01_2027-10-18.csv by month of collection, one person per name and date of birth (joining a dormant and a live NHI), and joined each typing in reference_lab_cryptosporidium_typing_2027.xlsx to its community specimen through the accession inside the referrer reference, or name and date of birth, keeping residents.
7. Ask 2: counted contacts in crm_water_contacts_2027-07-01_2027-10-18.csv from properties the rating_connections_2027-10-18.parquet supply type shows as networked (reached by valuation reference or address), plus reports in website_water_quality_reports_2027.csv that never reached the CRM, a report keyed again by hand counted once at its website time, over the networked connections at 30 September.
8. Ask 3: took notification from afterhours_service_calls_2027.csv for requests imported from the after-hours service (same address, same night), attendance and completion from crew_job_times_2027.xlsx converted from UTC, or from the next planned maintenance work order on the request's street in work_orders_2027-07-01_2027-10-18.csv for requests done with planned works, and took medians by month of notification.

## 4. Deliverable Answers

### outbreak_source.xlsx

1. Asset to take out of service: boundary main WM55081 (Ferndale to Kowhai Hills), 189.5 per hundred thousand resident-days
2. Runner-up: Kowhai Hills Reservoir, 10.6 per hundred thousand resident-days
3. Reservoirs, confirmed cases and attack rate per hundred thousand resident-days:
   - Hillcrest Reservoir: 2 cases, 0.2
   - Ferndale Road Reservoir: 61 cases, 5.4
   - Riverbend Reservoir: 2 cases, 0.3
   - Kowhai Hills Reservoir: 62 cases, 10.6
   - Southgate Reservoir: 1 case, 0.1
   - Eastfield Reservoir: 1 case, 0.1
4. Residents drinking through it during the renewal: 6,843
5. Residents tested for Cryptosporidium:
   - July: 112
   - August: 117
   - September: 166
   - 1 to 17 October: 192
6. Residents typed since 1 July:
   - C. parvum: 28
   - C. hominis: 3
7. Complaints per 1,000 connections, July to September:
   - Clarity: 1.73
   - Taste: 0.85
   - Odour: 0.47
   - Pressure or flow: 0.66
   - Continuity of supply: 0.60
8. Median call-out times:
   - July: urgent attendance 37 minutes, urgent resolution 193 minutes, non-urgent attendance 20.3 hours, non-urgent resolution 37.0 hours
   - August: urgent attendance 38 minutes, urgent resolution 195 minutes, non-urgent attendance 27.7 hours, non-urgent resolution 42.7 hours
   - September: urgent attendance 43 minutes, urgent resolution 197 minutes, non-urgent attendance 27.6 hours, non-urgent resolution 40.5 hours

### incident_brief.docx

9. One page with the recommendation and a bar chart of confirmed cases among residents by onset date, 1 September to 18 October 2027.

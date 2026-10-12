# Exemplars: Supply Chain & Logistics

> 8 accepted tasks in this domain, sorted by the current model's measured mean, lowest (hardest) first. Each is the client's own record. Index and the shared architecture: `index.md`.

## Adopt the arrival-based 2026 cover schedule with gmr at 50,670 Minutes at p90

**Replenishment Cover Standards**, Batch 14, Supply Chain & Logistics, model mean **0.13** over 4 runs (0.21, 0.21, 0.00, 0.21).

### What makes it strong (the client's note)

The trap is the order book's natural grain: one observation per order line with every receipt kept returns only 19 of 24 published means and sets GMR p90 at 55,615 minutes, 4,945 minutes above the admissible schedule.
Two hidden definitions must both be recovered: one observation per goods receipt note, timed from the earliest order it carries, and exclusion of arrivals whose order was released inside a supplier performance plan period (found by comparing release dates against the register, with no flag column). Either correction alone reproduces fewer means than applying neither.
Determinism pins: the admissible compilation keeps 31,260 of 32,913 arrivals and returns all 24 published means exactly; GMR p50 33,665 and p90 50,670 minutes; network p50 8,110 and p90 30,470 minutes.
The binding constraint is RCS 2019 clause 6: a compilation that misses any published mean by even one minute cannot reach the board, so the reconciliation selects the definition rather than merely checking it.

### Stakeholder ask (the prompt, verbatim)

Set the 2026 cover schedule for the Halberth Members' Replenishment Network. I need the boundary for every commodity tier at both committed shares, one schedule, adopted as it stands. That is the call the March board takes.

None of the supporting analysis survived the move to the new platform, so the schedule has to be rebuilt from the order book and the goods-in records. What we still hold is what the Secretary published, the mean lead time for each tier in every receipt year on file, and the 2025 schedule the board adopted. RCS 2019 is in the folder with them.

cover_schedule_2026.csv is what the replenishment system loads. One row per tier per committed share, carrying the 2026 boundary in whole minutes, the cover days it implies, and how far it has moved against the 2025 schedule, per cent to one decimal. Add the network-wide boundary at each share.

cover_schedule_note_2026.pdf goes to the board, a page or two, and has to make that call defensible. Open with the schedule you are adopting and the compilation behind it, then the four published years of means beside what you compile, with the difference on each.

Show the closest reading that does not stand and where its schedule parts from yours, in minutes. I also need the tier moving furthest against the standing schedule and by how much, and the boundary at which its cover days would change. A chart of the lead-time distribution with both committed cut lines drawn on it goes in as well.

### Deliverables

`cover_schedule_2026.csv`, `cover_schedule_note_2026.pdf` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A members' replenishment network must put a single 2026 cover schedule to its March board after the platform migration lost every compilation program and parameter sheet. Under the RCS 2019 standard, a schedule may only reach the board if its compilation reproduces all 24 published mean lead times for 2021 to 2024 to the minute, but the standard never says what a "receipt" is or which receipts count. The analyst must rebuild the lead-time population from the order book and goods-in records, test the candidate definitions of the unit (order line versus depot arrival) and the population (with or without arrivals against orders released while a vendor was under a performance plan) against the published means, then take the 2025 boundaries at the p50 and p90 shares by the clause 4 rank rule. Deliverables are `cover_schedule_2026.csv` (one row per tier per share with the boundary in whole minutes, cover days, and per cent movement against the 2025 schedule, plus network-wide rows) and `cover_schedule_note_2026.pdf` (a one to two page board note with the schedule, the compilation basis, the published-versus-compiled means, the closest rejected reading and its GMR p90 divergence, the furthest-moving tier and its cover-day threshold, and a lead-time distribution chart with both cut lines).)

`14 files, 8.1 MB`, `adopted_cover_schedule.csv`, `board_minute_2026-02.pdf`, `commodity_tiers.csv`, `depot_register.csv`, `field_definitions.json`, `goods_receipt_orders.csv`, `goods_receipts.csv`, `order_book.csv`, `platform_migration_closure_note.txt`, `published_lead_time_means.csv`, `rcs_2019_replenishment_cover_standard.pdf`, `replenishment_desk_note.txt`, `supplier_performance_register.csv`, `vendor_register.csv`

### Final recommendation

Adopt the 2026 cover schedule compiled one observation per depot arrival with performance-plan arrivals excluded (for example GMR 33,665 minutes at p50 and 50,670 at p90; network 8,110 and 30,470), the only compilation that reproduces all 24 published means, and reject the order-line reading.

### Step-by-step solution

1. Fix what RCS 2019 pins: lead time in whole minutes from order release to receipt, counted in the year of receipt, boundaries at rank ceil(a x n / b) with no interpolation, rounded up to the next 5 minutes, cover days as the boundary divided by 1,440 rounded up.
2. Build the arrival population by joining goods_receipt_orders.csv to the order book and goods_receipts.csv; time each arrival from the release of the earliest order it carries.
3. Flag orders released on a date inside the vendor's plan_start to plan_end window on the supplier performance register (both ends inclusive) and drop the arrivals they sit on.
4. Recompute the 2021 to 2024 tier means on each candidate definition. Arrival grain with plan exclusion returns all 24 published means; order-line grain with every receipt kept returns 19; other combinations, including dropping expedited orders, return fewer.
5. Take the 2025 boundaries on the admissible population: AMB 3,135 / 4,495, CHL 4,700 / 6,750, FRZ 7,030 / 10,275, HHC 10,865 / 15,280, HBC 18,775 / 27,530, GMR 33,665 / 50,670, network 8,110 / 30,470 minutes (p50 / p90).
6. Derive cover days and movement against the 2025 schedule; GMR moves furthest at +11.1 per cent (33,665 against 30,300 at p50).
7. Compute the rejected order-line schedule; at GMR p90 it reads 55,615 minutes, 4,945 above the adopted boundary.
8. Note the GMR p90 cover-day threshold: 36 days up to and including 51,840 minutes, 37 above.
9. Write cover_schedule_2026.csv and the two-page board note with Table 1, the compilation basis, Annex A reconciliation, the alternative reading, the largest movement, and the distribution chart.

### Key traps (what the model did)

- Compiled the lead-time distribution at the order-line grain with every receipt kept, then adopted it (or fell back to the standing 2025 schedule) even though its own run-back reproduced only 19 of 24 published means.
- Treated the published-means reconciliation as a reported diagnostic rather than a binding gate: printed a 19/24 match and still adopted a schedule, in one case retreating to the prior-year schedule (0.0% movement everywhere).

### Justification

The standard defines how to cut a distribution but not which receipts make it up, and clause 6 makes the published means the test. Only one pairing of unit and population returns all 24 published means to the minute: one observation per depot arrival, timed from its first order, with arrivals against orders released under a supplier performance plan left out. The order-line reading the data layout invites misses five means, so a schedule built on it cannot go to the board, and it would overstate GMR p90 cover by 4,945 minutes. The adopted schedule follows mechanically from that population under clause 4, and GMR is the tier that moves most against the standing schedule.

## Certify the fy2027 rail crossing cycle at 23.8 Collisions prevented for standard apportionment

**Rail Grade Crossing Safety Programs**, Batch 14, Supply Chain & Logistics, model mean **0.17** over 4 runs (0.35, 0.27, 0.22, 0.29).

### What makes it strong (the client's note)

The trap is the factor table: fitting factors on improvement type alone gives 0.57, 0.47 and 0.29, reproduces ten of the fourteen certified district cells, misses D1 and D2 in both cycles with opposite signs, and composes the FY2027 slate to 28.5, which would be full apportionment.
The computation chain: count every reporting railroad's Form 57 reports at each crossing over the five-year window (N-6 to N-2), counting a same-event pair filed by two railroads once, divide by five, multiply by the maintained factor and by three, and sum to the cycle figure at one decimal.
Determinism pins: factors keyed on type and on whether a passenger-service railroad reports at the crossing (no: 0.65, 0.55, 0.35; yes: 0.45, 0.35, 0.20) reproduce all fourteen certified cells; FY2027 total 23.79, certified 23.8; districts D1 7.05, D3 7.05, D2 6.48, D5 1.32, D4 1.05, D6 0.84, D7 0.00; types T1 18.90, T2 2.16, T3 2.73; 16 of 20 crossings passenger-operated, 91 collisions in 2021 to 2025.
The binding constraint is the tier boundary in Worksheet B-2: 25.2 or more is full, 22.5 to below 25.2 is standard, so the factor table decides whether the cycle stays at full or drops one tier.

### Stakeholder ask (the prompt, verbatim)

I need the FY2027 cycle of the crossing improvement program certified before the Commission takes it up on the 12th of November. Use the program manual as it stands, it settles how a cycle gets certified and which apportionment tier follows from the figure, and don't re argue any of that. Give me one number, how many collisions the 20 approved projects are expected to prevent over the benefit period, one decimal, and the tier that puts the cycle in. The staff note has the slate and what the FY2025 cycle was certified at, nothing else in the program changed though.

Put it in a memo for the Commission, a word doc is fine. Lead with the certified figure and the tier, then the change against what was certified for FY2025 and which direction it moved. Then give each district's expected collisions prevented and the same by improvement type. Include one chart with one bar per district biggest first, the value written on each bar, last cycle's certified figure for that district next to it as a second series, and the certified total and the tier in the title.

Also give me the project schedule as an excel workbook, one row per approved project with the crossing, the district, the improvement type and the collisions it is expected to prevent over the period to two decimals, plus a total row.

### Deliverables

`rcip_fy2027_certification_memo.docx`, `rcip_fy2027_project_schedule.xlsx` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A state rail crossings safety branch must certify the FY2027 cycle of its Rail Crossing Improvement Program: the expected collisions prevented over the three-year benefit period, which sets the cycle's apportionment tier, and the change against the FY2025 certification. The analyst works from the program manual (Worksheet B-2), the FY2023 and FY2025 certifications of record with their district appendices, the three cycle project lists, a staff planning note, the FRA Form 57 grade-crossing incident extract with its railroad dimension and summaries, and the FRA reporting guide. The manual does not print the effectiveness factors in force, so the analyst must recover them from the certified district figures and apply them to the twenty approved FY2027 crossings. Deliverables are a Word certification memo that leads with the certified figure and tier, then the change against FY2025, district and improvement-type breakdowns and exactly one chart (FY2027 by district, largest first, values on the bars, FY2025 certified figures beside them, figure and tier in the title), and an Excel project schedule with one row per project and a total.)

`17 files, 11.6 MB`, `annual_railroad_summary.csv`, `crossing_summary.csv`, `data_dictionary.json`, `fra_form57_view_metadata.json`, `fra_guide_preparing_accident_incident_reports.pdf`, `incidents.csv`, `monthly_state_summary.csv`, `overview.xlsx`, `program_benefit_certifications.docx`, `railroads.csv`, `rcip_program_manual.docx`, `rcip_projects_fy2023.csv`, `rcip_projects_fy2025.csv`, `rcip_projects_fy2027.csv`, `staff_planning_note.docx`, `states_dim.csv`, `warning_device_summary.csv`

### Final recommendation

Certify the FY2027 cycle at 23.8 expected collisions prevented over the three-year benefit period, which receives the standard apportionment; this is 4.0 below the FY2025 certified 27.8 and one tier down from full apportionment.

### Step-by-step solution

1. Read Worksheet B-2: each project's expected collisions prevented is the crossing's Form 57 count by any reporting railroad over calendar years N-6 to N-2, divided by five, times the maintained effectiveness factor, times three. For FY2027 the window is 2021 to 2025. Tiers: 25.2 or more full, 22.5 to below 25.2 standard, below 22.5 supplemental review.
2. Take the FY2023 and FY2025 project lists of record (42 and 39 unique crossings, treating a later pull of the same project identifier as the same project), count reports over 2017 to 2021 and 2019 to 2023 with same-event pairs counted once, and set them against the fourteen certified appendix cells.
3. Fit the factors: type alone (0.57, 0.47, 0.29) misses D1 and D2 in both cycles; adding whether a passenger-service railroad reports at the crossing closes all fourteen cells with 0.65, 0.55, 0.35 at crossings without one and 0.45, 0.35, 0.20 at crossings with one.
4. Classify the twenty FY2027 crossings (16 passenger-operated, 4 freight only) and compose each project amount; the twenty amounts total 23.79, certified as 23.8.
5. Place 23.8 in the standard tier and compare with FY2025: 4.0 lower, down from full apportionment.
6. Report districts (D1 7.05, D3 7.05, D2 6.48, D5 1.32, D4 1.05, D6 0.84, D7 0.00) and types (T1 18.90, T2 2.16, T3 2.73).
7. Write the memo leading with 23.8 and the standard tier, then the change, the breakdowns, the district chart against the FY2025 certified figures, and the workings; build the twenty-row schedule with its 23.79 total.

### Key traps (what the model did)

- Fit the effectiveness factors on the obvious single key (improvement type) and accepted a table that reproduces only 10 of 14 certified district cells, then carried it forward; never searched for the second keying variable that closes the residual misses.

### Justification

The certifications of record are the only evidence of the factor values in force, and only the table keyed on improvement type and passenger operation reproduces every certified district figure. Carrying that table forward, as the manual and the staff planning note require, puts the FY2027 cycle at 23.8, inside the standard band. The type-only table would certify 28.5 and full apportionment, but it fails the certifications it claims to match, so it is not the table of record.

## Site the irap intermodal transload facility in pennsylvania, ahead of illinois on the reproduced rail access index

**Freight Rail Infrastructure Siting**, Batch 14, Supply Chain & Logistics, model mean **0.3** over 2 runs (0.18, 0.58).

### What makes it strong (the client's note)

The trap is the screening memo's first-order measure: the rail-involved share of all domestic Schedule C tonnage with no distance, sector, lane or cell restriction puts Oklahoma first at 41.36, but clause 3.1 rejects first-order shares and the measure does not reproduce Schedule D. Under the Index Oklahoma falls to 35.92.
The computation chain: read four 2017 quarterly extracts (791,437 records) and the 2022 extract (2,738,598 records) as text, scope to domestic producer shipments (mining 21 or manufacturing 31-33) of Schedule C commodities moving at least 250 great-circle miles, weight to short tons, keep origin-to-destination state lanes carrying at least 1,000,000 short tons, then keep state and commodity cells holding at least 50 sampled records, and take rail-involved tons over all counted tons.
Each survey year is read under its own coding (clause 3.2): rail-involved modes are 06, 15 and 17 in 2017 but 12, 22 and 24 in 2022, where 12 means pipeline in 2017.
Determinism pins: only this composition returns all nine Schedule D values (Minnesota 72.65 through Missouri 17.40); Pennsylvania 67.59, Illinois 56.99, gap 10.60; Pennsylvania counts 5,438,264 short tons, 3,675,907 rail-involved, to 5 destination states; Pennsylvania 2017 Index 66.19.

### Stakeholder ask (the prompt, verbatim)

The Inland Rail Access Program's Site Selection Committee meets Thursday and has funding for

exactly one intermodal transload facility this cycle. It goes to a single Candidate State under

IRAP-3 and the Committee wants that state named, not a shortlist and not a ranking with a

preference. The Program Office's cycle-3 screening memorandum and its records-migration archive

note are in the supplied materials for context.

Tell me which single Candidate State is selected under IRAP-3, and name the state it beats.

Hand me a runnable irap_site_selection.py that reproduces the selection from the shipped
files.

Print the selected state and its Rail Access Index on the 2022 survey, to two decimal
places.

Print the runner-up state, its Rail Access Index to two decimal places, and the gap between
the two in index points to two decimal places.

Print every Candidate State's Rail Access Index on the 2022 survey, to two decimal places,
ordered highest to lowest.

Print, for the selected state on the 2022 survey, the tonnage the Index counts that moved
with rail involvement and the total tonnage the Index counts, both in whole short tons.

Print the selected state's Rail Access Index on the 2017 survey, to two decimal places.

Print how many Candidate States have a higher Rail Access Index on the 2022 survey than on

the 2017 survey, as a whole number.

Print the Candidate State whose Rail Access Index rose the most between the two surveys,
and the rise in index points to two decimal places.

Print the single Candidate State and two-digit commodity combination with the largest
rail-involved tonnage the Index counts on the 2022 survey, naming both and giving the

tonnage in whole short tons.

Print the total tonnage the Index counts across all ten Candidate States on the 2022
survey, in whole short tons.

Print the number of destination states that the selected state's counted 2022 tonnage
moved to, as a whole number.

Print the domestic rail tonnage that FAF5 publishes for the selected state across the
Schedule C commodities in 2022, in thousand short tons to one decimal place.

Include state_rail_access_panel.csv so the Committee can audit the selection.
One row per Candidate State per Survey Year, carrying the total tonnage the Index counts
and the rail-involved part of it in whole short tons, and the Rail Access Index to two

decimal places.

Each row carries the state's name and its two-digit FIPS code.

Ordered by state name, then by Survey Year.

Include rail_access_index_chart.png so the selection reads at a glance.
Plot the 2022 Rail Access Index for every Candidate State as bars, ordered highest to
lowest.

Label the selected state and the runner-up with their Index values to two decimal places.

Draw a horizontal reference line at the selected state's Index and label it with that

value.

Annotate the chart with the number of Candidate States whose 2022 Index exceeds 50, as a
whole number.

Title the chart with the selected state.
Report every Index to two decimal places and every tonnage in whole short tons unless an ask

states otherwise, and keep the figures identical across all three files.

### Deliverables

`irap_site_selection.py`, `state_rail_access_panel.csv`, `rail_access_index_chart.png` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (An inland rail access program has funding for exactly one intermodal transload facility this cycle, and its Site Selection Standard (IRAP-3) awards it to the Candidate State with the highest Rail Access Index on the 2022 Commodity Flow Survey. The worksheet that defined the Index was lost in a records migration; only the nine completed cycle-2 Index values on the 2017 survey (Schedule D) survive, and the Standard says a treatment that does not return them is not the Index. The analyst must rebuild the treatment from the 2017 and 2022 shipment-level extracts and each year's documentation, apply it to the ten Candidate States, and name the selected state and the state it beats, setting aside a screening memo that points to Oklahoma. Deliverables are `irap_site_selection.py` (a runnable script that prints the selection, runner-up, gap, all ten 2022 Index values and a set of supplementary tonnage and comparison figures), `state_rail_access_panel.csv` (one row per Candidate State per survey year with FIPS, counted and rail-involved tonnage and the Index) and `rail_access_index_chart.png` (descending bars of the 2022 Index with the top two labeled, a reference line at the selected state's Index, a count of states above 50 and a title naming the selection).)

`15 files, 271.9 MB`, `CFS_area_to_FAF5_zone.xlsx`, `FAF5_metadata.xlsx`, `IRAP-3_site_selection_standard.pdf`, `PROVENANCE_MANIFEST.csv`, `cfs_2017_puf_industrial_extract_Q1.csv`, `cfs_2017_puf_industrial_extract_Q2.csv`, `cfs_2017_puf_industrial_extract_Q3.csv`, `cfs_2017_puf_industrial_extract_Q4.csv`, `cfs_2017_puf_users_guide.pdf`, `cfs_2022_pums_data_dictionary.xlsx`, `cfs_2022_pums_industrial_extract.csv`, `completed_scorecard_cycle2.csv`, `faf5_7_1_state_domestic_territory_extract.csv`, `records_migration_archive_note.md`, `site_screening_memo_cycle3.docx`

### Final recommendation

Select Pennsylvania under IRAP-3 with a 2022 Rail Access Index of 67.59; it beats the runner-up Illinois (56.99) by 10.60 index points.

### Step-by-step solution

1. Load the four 2017 quarterly extracts and the 2022 extract with every column as text so codes keep their leading zeros: 791,437 records for 2017 and 2,738,598 for 2022.
2. Scope the population: origin in a Candidate or Schedule D state, EXPORT_YN = N, SCTG in Schedule C or a group code lying wholly inside it (10-14 and 15-19 count), shipper in a producing sector (2022 SECTOR 21 or 31-33; 2017 NAICS mapped by its first two digits), and great-circle distance of at least 250 miles. Weight each record as SHIPMT_WGHT x WGT_FACTOR / 2000 short tons.
3. Reconstruct the Index treatment on the 2017 extracts by sweeping mode sets, commodity scope, weighting, distance, sector, lane and cell rules and their order. Only one composition returns all nine Schedule D values: keep state-to-state lanes with at least 1,000,000 short tons, then state and commodity cells with at least 50 sampled records.
4. Identify rail-involved tonnage under each year's coding: 2017 modes 06, 15 and 17; 2022 modes 12, 22 and 24.
5. Apply the treatment to the ten Candidate States on the 2022 extract: Pennsylvania 67.59, Illinois 56.99, Louisiana 52.08, Oklahoma 35.92, California 28.47, Texas 27.10, North Carolina 15.48, Kentucky 12.77, Florida 0.54, Arizona 0.00 (no counted tonnage).
6. Select Pennsylvania under clause 4.1; it beats Illinois by 10.60 index points, with no tie.
7. Report the supplementary figures: Pennsylvania 2017 Index 66.19; 4 Candidate States rose between surveys; the largest rise is Louisiana at 36.26 points; the largest rail-involved state and commodity cell is Texas SCTG 20 at 10,662,934 short tons; counted tonnage across the ten states is 153,232,592 short tons; and FAF5 publishes 13,588.9 thousand short tons of 2022 domestic rail tonnage for Pennsylvania across Schedule C.
8. Write the 20-row panel CSV ordered by state then year, and the chart with ten descending bars, Pennsylvania and Illinois labeled, a reference line at 67.59, an annotation that 3 of 10 states exceed 50, and a title naming Pennsylvania.

### Key traps (what the model did)

- Built the Rail Access Index from a partial or misordered composition of the scope rules (distance, sector, lane floor, cell floor, per-vintage mode codes) that does not return the nine Schedule D values, producing off-target indices; one run's composition flipped the winner to Illinois.

### Justification

IRAP-3 defines the Index as the treatment that returns the nine retained Schedule D values, and only one composition of the plausible rules does so. Under it Pennsylvania leads Illinois by 10.60 points on a counted population of 5,438,264 short tons, a margin that does not depend on rounding or a single record. The memo's Oklahoma pick rests on a first-order share that the Standard rejects and that misses every Schedule D value, and every partial reconstruction that favours Illinois also fails the Schedule D test, so none of them is the Index.

## Commit 221,709 Outbound units off recent_28D_Weekly_Avg for 2 to 8 december

**Outbound Warehouse Volume Planning**, Batch 14, Supply Chain & Logistics, model mean **0.44** over 4 runs (0.73, 0.46, 0.44, 0.25).

### What makes it strong (the client's note)

The trap is carrying forward PRIOR_YEAR_364D, the archived scorecard winner (WAPE 0.2838), which ranks last (0.2058) once the same convention is applied to the current 180-origin history; a second trap is multiplying the forecast by a coverage factor, which commits 237,097 instead of 221,709.
None of the scoring window, the outbound basis or the allowance form is stated: the 180-origin trailing window is pinned by reproducing the 0.251789 monitoring figure (all 285 admissible origins give 0.2641), the Quantity greater than zero basis by reproducing the archived scorecard, and the additive allowance by reproducing the 130,544 September booking.
The computation chain runs from removing 22,523 cross-sheet duplicate rows, through daily gross units and four profile forecasts per origin, to WAPE over 180 origins, then the 162nd sorted residual of the selected profile.
Determinism pins: RECENT_28D_WEEKLY_AVG WAPE 0.14160506, point forecast 179,587.5, additive allowance 42,121, coverage 163 of 180 weeks, commitment 221,709.

### Stakeholder ask (the prompt, verbatim)

I need the volume number from you by Friday morning, and just keep in mind that's when carrier capacity and the agency shift cover both go out for the week of December 2nd, and once they're in we're stuck with whatever we put down.

The planning folder is attached below for you. And I do want the number operations commits to from the 2nd through the 8th of December, which is also the number that will go in the booking. Please don't give me a central estimate. If it turns out that number is under, we have to do a ad hoc collections on the weekend, and I really don't want that.

Give me the call in outbound_volume_commitment_memo.pdf in no more than one page, and remember to put the committed number and the profile it came off right at the top so it's easy for me to see. Then tell me the reason of choosing that profile instead of the other ones. And also show me it would have held. This one bit me last time already. It looked fine when I signed it off, then the actual week time happened to come in way over and we have deal with that with no warnings. Give me one chart that will make the case quickest and don't just write me a methodology note, so I can read it in few minutes and forward it on.

Also let me know what you used in the folder and what you didn't use, and why. So I know what you ignored instead of finding it out later myself.

Make sure to put the supporting analysis in outbound_volume_workings.csv as well. It should include the candidate comparison and every single step from the files to find that committed number, so our planning can run the whole thing again without opening the PDF. Please give me just one number at the end, I don't want to see a range.

### Deliverables

`outbound_volume_commitment_memo.pdf`, `outbound_volume_workings.csv` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A UK online retailer's operations lead needs one committed gross outbound unit volume for 2 to 8 December 2011, the figure that goes into the carrier booking and the agency shift cover and cannot be changed once submitted. Under-commitment means weekend ad hoc collections, so the lead wants a service-level number rather than a central estimate. The planning folder holds two overlapping transaction extracts from the UCI Online Retail II workbook, a registry of four candidate forecast profiles, a planning standard that requires the best-scoring profile and nine-in-ten historical coverage, an archived June 2011 scorecard, a September 2011 monitoring entry and carrier booking, and external ONS retail context. The analyst must reconcile the extracts, recover the unstated scoring window, outbound basis and allowance form from the archival records, rank the profiles on the current scored history, size the minimum allowance that meets the coverage standard, and say which folder evidence was used or set aside. Deliverables are `outbound_volume_commitment_memo.pdf` (one page, committed number and profile at the top, one chart) and `outbound_volume_workings.csv` (the candidate comparison and every step to the commitment).)

`15 files, 36.3 MB`, `EXTERNAL_CONTEXT_SOURCE_NOTES.txt`, `PACKET_MANIFEST.json`, `READ_FIRST.txt`, `UCI_SOURCE_AND_FIELD_NOTES.txt`, `archived_scorecard_2011-06-04.csv`, `carrier_booking_log_2011-09-17.csv`, `external_retail_context_oct2011.csv`, `forecast_monitoring_log_2011-09-17.csv`, `forecast_profile_registry.json`, `invoice_status_reconciliation.csv`, `observed_operating_days.csv`, `source_sheet_coverage.csv`, `transactions_2009_2010.csv`, `transactions_2010_2011.csv`, `weekly_planning_standard.pdf`

### Final recommendation

Commit 221,709 gross outbound units for 2 to 8 December 2011, using RECENT_28D_WEEKLY_AVG as the governing profile (point forecast 179,587.5 plus a 42,121-unit additive allowance, covering 163 of 180 scored weeks). Do not carry forward the archived PRIOR_YEAR_364D selection.

### Step-by-step solution

1. Reconcile the two transaction extracts by removing the 22,523 rows duplicated across both worksheets for 1 to 9 December 2010, keeping legitimate within-sheet repeats.
2. Recover the outbound basis by reproducing the 2011-06-04 scorecard to eight decimals over its 180 origins (0.34325349, 0.36761787, 0.35177971, 0.28382681). Only Quantity greater than zero regardless of invoice prefix reproduces all four; dropping cancellation-prefixed rows breaks PRIOR_YEAR_364D because of the single positive row on invoice C496350.
3. Recover the scored-history length from the 2011-09-17 monitoring log: only a 180-origin trailing window ending 2011-09-09 reproduces PRIOR_YEAR_364D at 0.251789, while all 285 admissible origins give 0.26406412.
4. Recover the allowance form from the carrier booking log: at the 2011-09-17 origin SAME_WEEKDAYS_8W wins with a 104,158 point forecast, and the minimum additive allowance of 26,385.62 gives exactly the booked 130,544. The multiplicative equivalent (1.318924) gives 137,377 and does not.
5. Score the four profiles over the current scored history, the 180 origins from 2011-05-29 to 2011-11-24: RECENT_28D_WEEKLY_AVG 0.14160506, RECENT_7D_TOTAL 0.15834773, SAME_WEEKDAYS_8W 0.15931178, PRIOR_YEAR_364D 0.20578496. RECENT_28D_WEEKLY_AVG is the official profile.
6. Compute its point forecast for 2 to 8 December: one quarter of the 28 days to 1 December, 179,587.5 units.
7. Take the 162nd of 180 sorted residuals as the minimum additive allowance, 42,121 units; with a tie at rank 163 it covers 163 of 180 weeks (90.56 percent). The next smaller candidate, 41,794.50, covers 161 and fails.
8. Round 179,587.5 plus 42,121 up to 221,709 units and present it at the top of the one-page memo with one candidate comparison chart, the evidence used and set aside (the ONS context is sector value, not unit volume), and a CSV with every intermediate value.

### Key traps (what the model did)

- Picked the right profile but sized the service allowance on the wrong scoring window (all 361 origins instead of the trailing 180 the monitoring log pins), and in one run applied a multiplicative coverage factor instead of the additive allowance the carrier booking log pins.

### Justification

The planning standard makes the official profile whichever candidate scores best on the current scored history under the archived convention, and it sets the commitment by nine-in-ten historical coverage. Recovering that convention from the folder's own records fixes a 180-origin window, a Quantity greater than zero basis, and an additive allowance, each confirmed by reproducing a filed figure exactly. On that basis RECENT_28D_WEEKLY_AVG has the lowest WAPE, and the archived PRIOR_YEAR_364D winner now ranks last, so the earlier selection describes a window that closed six months ago. The 42,121-unit allowance is the smallest that meets the standard, giving 221,709 units that would have held in 163 of the 180 scored weeks.

## Select the allocation-treatment review package and preserve the ratified seq-b order

**Depot Replenishment Allocation**, Batch 14, Supply Chain & Logistics, model mean **0.46** over 4 runs (0.47, 0.53, 0.47, 0.50).

### What makes it strong (the client's note)

The trap is the default charter queue order (SEQ-A): it also reproduces all 660 settled scorecard values, so the replay alone cannot pick the treatment; only the dated, ratified OPN-2027-0105 row in the authority register resolves the active window to SEQ-B, and using SEQ-A as the baseline understates the shortfall by 584 requests.
Computation chain: conform 11,988 rows to 11,903 request IDs by earliest ingested_at, isolate 2,423 active requests worth $2,177,679, replay twelve settled cycles per depot with carry-forward of unreached requests, then simulate three active cycles under SEQ-B, SEQ-A, and a raised budget.
Determinism pins: SEQ-B baseline 1,871 new unfilled requests, SEQ-A counterfactual 1,287, movement 584; a $100,000 budget sensitivity leaves 1,488, a movement of 383.
The binding constraint on the reserve is the per-effective-cycle 55-request floor for February and March: Highland passes at 58 and 86, South fails February at 51 even though its two-month total looks competitive, and Central and Eastport are screened out by slot status and capacity.

### Stakeholder ask (the prompt, verbatim)

We'll be closing out the replenishment controls for January-March 2027 next week. I need one control package for the shortfall in the active window and the action it authorizes. Use only the packet to determine the treatment actually in force from January through March, and certify it on one active-window population. This sign-off cannot rely on a retroactive result or a result from one day. Please send one self-contained HTML file named replenishment_root_cause.html for the operations call. You can start with the executive recommendation and let the page carry one connected story: explain the shortfall's driver and the action, show the ratified baseline, then compare the isolated counterfactual and movement for the selected package with its closest competitor and cite the dated rule or record that rules the competitor out. Could you keep other explanations in a brief rejection view, and keep operational attribution separate from any claim that a physical depot caused the shortfall. Make the conformed and active counts and dollars traceable to dated sources, with source roles and units clear, and include the queue, budget context and evidence limits needed to understand the decision. Fold reserve sensitivity into the selected package by stating its effective-cycle conditions and whether they change the conclusion, do not make it a separate release recommendation. Please include a labeled visual comparison with the closest competitor and give the selected package one name and repeat that exact name in the recommendation, certification record, selected ledger row and visual title or caption. This is an internal exercise, not a forecast or live release instruction.

### Deliverables

`replenishment_root_cause.html` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A regional parcel network is closing out its January-March 2027 replenishment controls and needs one control package that explains the active-window fulfillment shortfall and the action it authorizes. Each of five depots gets a fixed $80,000 budget per monthly cycle, requests are filled only in full, and unreached requests stay open into later cycles. The analyst must conform 11,988 raw request rows to one row per request, determine from a dated authority register that the ratified order OPN-2027-0105 (SEQ-B, retained-open work before current-cycle intake) supersedes the default charter order for January through March, confirm that treatment against the settled scorecard, build the active-window baseline, and compare the isolated queue-order counterfactual with the closest competing explanation, funding capacity. The FLEX-2027-02 reserve must be folded in as a sensitivity under its per-effective-cycle gate rather than issued as a separate release. The deliverable is one self-contained HTML page, `replenishment_root_cause.html`, that opens with the recommendation, carries a certification record, a decision ledger, a brief rejection view, source roles and dates, and a labeled visual against the closest competitor, all using one repeated package name.)

`18 files, 2.0 MB`, `01_replenishment_request_export.csv`, `02_active_request_extract.tsv`, `03_depot_directory.xlsx`, `04_archived_allocation_scorecard.xlsx`, `05_supply_parameters.json`, `06_field_dictionary.json`, `07_cycle_calendar.csv`, `08_operations_correspondence.md`, `09_allocation_charter.docx`, `10_data_quality_log.csv`, `11_archive_reconciliation.csv`, `12_release_controls.csv`, `13_packet_manifest.csv`, `14_flex_reserve_authorization.csv`, `15_root_cause_review_protocol.md`, `16_queue_authority_register.csv`, `17_source_provenance.csv`, `19_network_operations_administration_note.md`

### Final recommendation

Select the allocation-treatment review package and preserve the ratified OPN-2027-0105 January-March 2027 order (SEQ-B). Under SEQ-B the active window leaves 1,871 new requests unfilled versus 1,287 under the default order, a 584-request movement that exceeds the 383-request movement from the nearest funding sensitivity.

### Step-by-step solution

1. Conform the request export by keeping the earliest-ingested row for each request_id: 11,988 raw rows become 11,903 conformed requests, of which 2,423 active requests total $2,177,679 and match the active extract.
2. Resolve the treatment in force from the queue authority register: OPN-2027-0105 is ratified, covers 2027-01-01 to 2027-03-31, and overrides the CHARTER-DEFAULT SEQ-A row with SEQ-B.
3. Replay the settled cycles under the charter rules (descending value, full-request fills, carry-forward of unreached requests); SEQ-B reproduces all 660 published scorecard values.
4. Run the active window under SEQ-B to get the certified baseline of 1,871 new unfilled requests.
5. Change only the queue order to SEQ-A: the count falls to 1,287, a movement of 584. Name the selected package "allocation-treatment review / preserve ratified SEQ-B".
6. Test the nearest rival, funding capacity: a $100,000 budget under SEQ-B leaves 1,488 unfilled, a movement of 383, smaller than the allocation movement, so funding stays a contributing sensitivity.
7. Screen FLEX-2027-02 as a sensitivity inside the selected package: effective February and March only, open slot, capacity at least 3.8, at least 55 removed in each cycle. Highland passes at 58 and 86, South fails February at 51, Central (closed), Eastport and North (capacity) are excluded. The reserve does not change the conclusion.
8. Publish replenishment_root_cause.html with the recommendation first, the certification record, decision ledger, rejection view, source roles and dates, evidence limits, and a labeled visual of 584 versus 383 carrying the package name.

### Key traps (what the model did)

- Correctly identified the ratified OPN-2027-0105 SEQ-B order as in force, then selected the actionable lever, a Highland FLEX reserve-release (funding) package, as the control package. It treated funding capacity as the driver and never ran the isolated SEQ-B vs SEQ-A counterfactual (1,871 vs 1,287, 584 movement) against the funding sensitivity (383).
- Attributed the 660/660 settled-replay reproduction to SEQ-A (or miscounted it as 60 cells) rather than noting that both orders reproduce, which is why the replay cannot discriminate.

### Justification

The settled replay cannot separate the two queue orders, because both reproduce every published value in the low-utilization history, so the decision rests on the dated authority register, where the ratified OPN-2027-0105 order puts retained-open requests first for January through March. Holding everything else fixed, that order accounts for a 584-request movement in new unfilled requests, more than the 383 recovered by raising the depot budget to $100,000, so allocation treatment is the supported operational driver and funding is a secondary sensitivity. The reserve screen confirms that only Highland clears the per-cycle floor and does not alter the driver finding. The result is an operational attribution from the supplied packet, not proof that any depot caused the shortfall.

## Award crossdock_Central_Epsilon to the midwest regional corridor, the highest corridor within sortation capacity

**Parcel Sortation Facility Allocation**, Batch 14, Supply Chain & Logistics, model mean **0.47** over 4 runs (0.51, 0.42, 0.51, 0.49).

### What makes it strong (the client's note)

The trap is the prompt's own framing: the Atlantic Coastal Corridor has the highest sustained volume (43,117 parcels/day), but the policy's feasibility clause, the VP memo, and the jam log (every overcapacity incident at 34,180 parcels/day or more) rule it out for this building.
The computation chain: drop 500 calibration scans and 300 non-dispatched records to reach 15,200 valid dispatches, take corridor shares, and scale to 110,000 parcels/day with whole-number rounding.
Determinism pins: MW-200 29,809 parcels/day (27.1%), SC-300 20,900 (19.0%), margin 8,909 parcels/day, required runner-up expansion 42.6%, AT-100 43,117 (39.2%), NW-400 11,441, GL-500 4,733.
The binding constraint is the facility sortation ceiling (34,180 parcels/day, the lowest OVERCAPACITY-coded volume in sorting_jam_incident_log.csv), which turns the volume leader into a disqualified corridor and makes Southern Plains, not Midwest, the runner-up.

### Stakeholder ask (the prompt, verbatim)

Morning, we have our steering review coming up this week for the Q4 lock-in on CROSSDOCK_CENTRAL_EPSILON, and operations has been arguing back and forth on which corridor should get the building. I need you to pull our Q3 dispatch telemetry, audit it against our network allocation policy, and settle this with hard numbers. Tell me which regional corridor has the highest sustained daily outbound volume and should actually take the facility.

Please put this into a one page PDF memo called parcel_allocation_memo.pdf. Start right off with the winning corridor and what its daily throughput rate looks like. In the breakdown, show who came in as the runner-up, the exact daily margin gap between first and second place, and the percentage volume expansion the runner-up would need to overtake the winner. Finish with an audited ranking table covering all five regional corridors with their volumes, daily rates, and overall workload share.

I also need one chart for the presentation deck saved as parcel_throughput_distribution.png. Make it a clean bar chart showing daily throughput across all five corridors plotted against the facility's physical capacity line. Highlight the winning corridor and label the daily rate directly on each bar so leadership can see the numbers clearly.

### Deliverables

`parcel_allocation_memo.pdf`, `parcel_throughput_distribution.png` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A retail logistics network must commission its automated cross-dock CROSSDOCK_CENTRAL_EPSILON for Q4 and award it to exactly one of five regional corridors. The steering review wants the decision settled from Q3 dispatch telemetry audited against the network allocation policy. The analyst must clean the 16,000-row dispatch manifest under the policy's exclusion rules, scale each corridor's share of valid dispatches to the 110,000 parcel/day network baseline, check the result against the facility's physical sortation limit documented in the engineering material and incident log, and name the winner, the runner-up, the daily margin, and the expansion the runner-up would need. Deliverables are `parcel_allocation_memo.pdf` (one page, opening on the winner and its daily rate, with the runner-up breakdown and a five-corridor ranking table of volumes, daily rates, and shares) and `parcel_throughput_distribution.png` (a bar chart of daily throughput for all five corridors against the facility's capacity line, winner highlighted, rates labeled on the bars).)

`10 files, 1.2 MB`, `facility_throughput_constraints.json`, `freight_carrier_agreements.csv`, `fulfillment_network_topology.html`, `network_allocation_policy.txt`, `package_dispatch_manifest_q3.csv`, `packaging_format_catalog.json`, `quarterly_corridor_benchmarks.xlsx`, `sorting_hardware_specifications.json`, `sorting_jam_incident_log.csv`, `vp_logistics_memorandum.txt`

### Final recommendation

Award CROSSDOCK_CENTRAL_EPSILON to the Midwest Regional Corridor (MW-200) at 29,809 parcels/day; the Atlantic Coastal Corridor (43,117 parcels/day) exceeds the facility's sortation capacity and is disqualified.

### Step-by-step solution

1. Filter the 16,000-row Q3 dispatch manifest per policy Section 2.1, removing 500 calibration scans and 300 records not DISPATCHED, leaving 15,200 valid outbound dispatches.
2. Group by corridor: AT-100 5,958 (39.2%), MW-200 4,119 (27.1%), SC-300 2,888 (19.0%), NW-400 1,581 (10.4%), GL-500 654 (4.3%).
3. Scale each share to the 110,000 parcel/day Q3 baseline and round: AT-100 43,117, MW-200 29,809, SC-300 20,900, NW-400 11,441, GL-500 4,733 parcels/day.
4. Apply policy Section 1.3 using the engineering material: the facility ceiling is 34,180 parcels/day, the lowest OVERCAPACITY-coded volume in sorting_jam_incident_log.csv; every logged overcapacity jam occurred at that volume or above.
5. Disqualify AT-100, which exceeds the ceiling by 8,937 parcels/day (26.1% over); it also exceeds the highest OVERCAPACITY jam volume (43,100).
6. Award the facility to MW-200, the highest corridor within capacity at 29,809 parcels/day.
7. Name SC-300 as runner-up at 20,900 parcels/day: a margin of 8,909 parcels/day, needing a 42.6% expansion to match MW-200.
8. Produce the one-page memo with the five-corridor ranking table and the bar chart with the capacity line, MW-200 highlighted, and rates labeled on each bar.

### Key traps (what the model did)

- Awarded the facility to the throughput leader as the prompt framed it, even after computing that it exceeds sortation capacity; treated the capacity breach as a waiver/mitigation item rather than disqualifying. One run derived a wrong capacity (84,706/day) and called AT-100 feasible.

### Justification

The policy's primary rule picks the highest sustained throughput, but it is bounded by the feasibility clause tying any award to the facility's certified mechanical parameters. The Atlantic corridor's 43,117 parcels/day sits well above the volumes at which the facility has repeatedly jammed, and the VP memo records that above-parameter routing caused the Q2 downtime. Awarding it to Atlantic would repeat that failure. Midwest is the largest corridor the building can actually handle, and Southern Plains trails it by 8,909 parcels/day, a 42.6% gap that leaves the call clear.

## Call the gulf loading year to june 2026 loading-constrained at a 20.3979% Congested share

**Port Grain Export Loading**, Batch 14, Supply Chain & Logistics, model mean **0.49** over 4 runs (0.45, 0.38, 0.88, 0.37).

### What makes it strong (the client's note)

The trap is the pre-read's method. It assigns weeks to months with the loading series' own month column, carries tonnage by vessels loaded, and reads the arrival footing on the same week's due figure. Each choice looks natural, and together they give 14.0989% and a not-constrained call while reproducing none of the lifted readings.
The computation chain filters bulk export tonnage to the three counted grain lines and the 14 Gulf ports over July 2025 to June 2026 (66,119,477 tonnes), takes the 53 weeks with a day in that year, and carries each month's tonnage into weeks by the days of the month each week covers. It then forms the waiting footing (in port over loaded) and the arrival footing (prior week's due over loaded).
Determinism pins: congested share 20.3979%, 10 of 53 weeks congested, 13,487,004 tonnes carried into congested weeks, with 9 weeks reaching the threshold on the waiting footing only, 11 on the arrival footing only and 23 on neither.
The binding constraint is validation. Set figures 1.0 and 1.5 come with no footing named, and only waiting at 1.0 with arrival at 1.5 reproduces all eight lifted readings (lk-81 to lk-88). Swapping them gives 5.1895%.

### Stakeholder ask (the prompt, verbatim)

The Gulf loading brief goes to the shipper council in two weeks. The pre-read says the year is clear, with a congested share of 14.0989% against the 19.0% threshold, but nobody on the desk can reproduce that figure. I need a call the council can verify.

Rebuild the calculation and determine whether the year through June 2026 was loading-constrained. Report the congested share to four decimal places. Before making the call, the method must reproduce every supplied lifted reading. If it cannot, identify the reading that remains unresolved and leave the brief without a constrained/not-constrained designation.

Use only the supplied materials. loading_terms.txt contains the governing terms, set_figures.csv contains the three fixed figures, and the lifted readings are the validation checks.

Return gulf_loading_rebuild.zip with three items. Include a Python rebuild script that regenerates the other two files and exits nonzero if the source files fail to load, the scope check fails, or any lifted reading does not reproduce. Include a one-page HTML brief with the call at the top and the week table in the format required by the carriage notes. Include one PNG showing the year week by week, with tonnage carried, both footings against their fixed figures, congested weeks marked, and the final share and call displayed.

The brief should explain how the year's tonnage and weeks were formed and how many of each there are; where the weeks fall on the two footings and which weeks reach the threshold on only one footing; whether the pre-read's 14.0989% differs from the rebuilt result and, if so, what the pre-read's own figures show about the source of the difference; and whether the scope checks and all lifted readings reconcile.

### Deliverables

`gulf_loading_rebuild.zip` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A grain logistics desk has to send a Gulf loading brief to the shipper council. The pre-read says the year through June 2026 was clear, at a 14.0989% congested share against a 19.0% threshold, but no one can reproduce that figure. The analyst works only from USDA port throughput and weekly loading-series extracts, a set of defined terms with no stated method, three unassigned set figures, three scope checks and eight lifted readings. They must rebuild the arithmetic so that every lifted reading reproduces, then decide whether the year was loading-constrained, report the share to four places, and account for the pre-read figure. The deliverable is `gulf_loading_rebuild.zip`, containing a Python rebuild script that regenerates the other two files and exits nonzero on a load, scope or reading failure, a one-page HTML brief with the call at the top and the week table in the carriage-notes column order, and a PNG of the year week by week showing tonnage, both footings against their set figures, congested weeks, and the share and call.)

`21 files, 6.2 MB`, `biodiesel_by_district.csv`, `calendar.csv`, `carriage_notes.txt`, `commodity_totals.csv`, `counted_lines.csv`, `field_guide.json`, `inventory.xlsx`, `lifted_readings.csv`, `loading_activity_weekly.csv`, `loading_terms.txt`, `pack_ledger.csv`, `port_totals.csv`, `pre_read_figure.txt`, `reading_runs.csv`, `readings_note.txt`, `rebuild_rules.txt`, `region_map.csv`, `scope_checks.csv`, `set_figures.csv`, `throughput_by_commodity.csv`, `throughput_by_shipment.csv`

### Final recommendation

The year through June 2026 was loading-constrained, with a congested share of 20.3979% against the 19.0 threshold. The pre-read's 14.0989% does not stand.

### Step-by-step solution

1. Read pack_ledger.csv for the closing month (June 2026). The year is July 2025 through June 2026.
2. Form the tonnage from throughput_by_commodity.csv: export, bulk, the three lines counted_lines.csv marks as grain, the 14 ports region_map.csv places in the Gulf. This gives 66,119,477 tonnes across 8 ports with tonnage, which passes scope checks q1, q2 and q3.
3. Define a week as the seven days ending on a Gulf loading-series date (Thursdays). Include every week with at least one day in the year: 53 weeks, from the week closing 3 July 2025 to the week closing 2 July 2026.
4. Carry each month's tonnage into weeks at one day's share of the month for each day the week covers. Eleven weeks draw from two months, and the weekly series sums to 66,119,477.
5. Compute the waiting footing as vessels in port over vessels loaded, and the arrival footing as the prior week's vessels due over the week's vessels loaded.
6. Assign set-a 1.0 to the waiting footing and set-b 1.5 to the arrival footing. A week is congested when both footings reach their figures: 10 weeks, with 9 waiting only, 11 arrival only and 23 neither.
7. Compute the share as tonnage carried into congested weeks over the year's tonnage: 13,487,004 of 66,119,477, or 20.3979%. This is above set-c 19.0, so the year is loading-constrained.
8. Recompute the eight lifted readings over their runs: lk-81 15.8951, lk-82 8.8295, lk-83 45.5893, lk-84 5.2914, lk-85 3,818,956, lk-86 10.4445, lk-87 22.5806, lk-88 5,165,911. All eight reproduce.
9. Reproduce the pre-read by using the series' month column (52 weeks), a carry by vessels loaded within the month, and the same-week due figure. The result is exactly 14.0989%, and it returns none of the readings.
10. Write the script, HTML brief and PNG from the same computed objects, with exit codes for load, scope and reading failures, and zip them as gulf_loading_rebuild.zip.

### Key traps (what the model did)

- Rebuilt the year with one of the pre-read's shortcuts still in place (arrival footing read on the same week's due figure) and an unsearched set-figure assignment; reproduced only 4 of 8 lifted readings, stopped searching, and used the prompt's escape hatch to withhold the call.

### Justification

The rebuild rules make the lifted readings the test of any method, and only one combination of week membership, carriage, footing construction and set-figure assignment reproduces all eight. That combination puts 10 of 53 weeks over both footings and 20.3979% of the year's tonnage in them, above the 19.0 line. The pre-read's 14.0989% comes from three individually plausible shortcuts that together fail every reading, so it gives the council no basis for calling the year clear.

## Release 48,300 Units to kestrel on premier tier, 16,100 A month

**Distributor Supply Allocation**, Batch 14, Supply Chain & Logistics, model mean **0.53** over 4 runs (0.80, 0.56, 0.49, 0.41).

### What makes it strong (the client's note)

The trap is the prompt's framing: December stock build and an emailed request to pull January orders forward invite netting out the build, which gives 102.9 percent, Priority tier and 44,100 units. Schedule E Section 2 counts shipments less returns to Halden and has no inventory adjustment, so the policy as written gives Premier.
The computation chain runs from 16,602 shipment lines, through removing 90 duplicate shipment-and-line rows, to Kestrel's Q4 sell-in of 48,915 units, attainment of 112.4 percent against a 43,500 target, the Premier 115 percent multiplier on a 42,000 base, and three equal releases.
Determinism pins: 48,300 units total, 16,100 per month, December sell-in 18,663 against sell-through 14,511, stock build 4,140 to 25,068, January sell-in 5,675 against sell-through 14,887.
The binding constraint is the written allocation policy, not the analyst's view of whether the order pull-forward was fair; last year's Q1 2025 allocation reproduces on the same shipment basis.

### Stakeholder ask (the prompt, verbatim)

Kestrel's Q1 allocation needs to be set under Schedule E before the January release is confirmed on the 20th. The package has the shipment lines, the distributor register and tier schedule, Kestrel's sell-through and inventory returns under Schedule C, last year's allocation, the Schedule E terms, and the account email export.

Kestrel came in above 110% for the first time, but almost all of the lift is December, their stock rose by about a third that month, and their January orders have mostly stopped. We're short this quarter with line two down, so units released to Kestrel can't go to distributors that are selling. They already hold about seven weeks of cover. I want the attainment checked before we release 15% over base. How many units do we release to Kestrel in Q1, and what's the monthly split?

Put it in a one-page PDF for the release meeting: the Q1 allocation, how it was derived, and whether the attainment holds. Also send the three-month schedule as a CSV with release month, release date, and units.

### Deliverables

`kestrel_q1_2026_release_schedule.csv`, `kestrel_q1_2026_supply_allocation.pdf` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (Halden Manufacturing is short on Q1 2026 supply because line two is down, and it must set Kestrel Distribution's Q1 allocation under Schedule E before the January release is confirmed on the 20th. Kestrel cleared 110 percent attainment for the first time, but most of the lift came in December, its stock rose by about a third that month, and January orders have mostly stopped, so the head of supply planning wants the attainment checked before releasing 15 percent over base. The analyst must deduplicate the shipment lines, compute Kestrel's Q4 sell-in and attainment on the Section 2 basis, map it to a tier and allocation, test whether the attainment holds against the sell-through, inventory and account correspondence, and set the monthly split. The deliverables are a one-page PDF for the release meeting with the Q1 allocation, how it was derived, and whether the attainment holds, plus a three-row CSV schedule with release month, release date and units.)

`12 files, 1.1 MB`, `account_email_export.csv`, `allocation_assessment_request.md`, `data_dictionary.json`, `distributor_inventory_monthly.csv`, `distributor_register.csv`, `distributor_sellthrough_monthly.csv`, `overview.xlsx`, `shipment_lines_2024_2026.csv`, `sku_price_list.csv`, `supply_allocation_policy_2026.md`, `supply_allocation_q1_2025_kestrel.xlsx`, `supply_allocation_tiers_2026.csv`

### Final recommendation

Release 48,300 units to Kestrel in Q1 2026 as 16,100 units in each of January, February and March. Kestrel's Q4 attainment of 112.4 percent on the Schedule E Section 2 basis earns the Premier tier at 115 percent of its 42,000-unit base.

### Step-by-step solution

1. Load shipment_lines_2024_2026.csv (16,602 rows), remove the 90 duplicate shipment and line rows, and filter to distributor DST-104 with ship dates from October to December 2025.
2. Read supply_allocation_policy_2026.md: Section 2 defines sell-in as units shipped in the quarter less returns to Halden, Section 3 sets attainment against the register target to one decimal, Section 4 sets allocation as tier percentage of base, and Section 5 sets three equal monthly releases.
3. Sum Kestrel's Q4 units to 48,915. No returns to Halden are recorded in the quarter.
4. From distributor_register.csv, take the Q4 2025 target of 43,500 and the Q1 2026 base allocation of 42,000. Attainment is 48,915 / 43,500 = 112.4 percent.
5. From supply_allocation_tiers_2026.csv, 112.4 percent falls in the Premier tier at 115 percent, giving 48,300 units released as 16,100 per month.
6. From the shipment lines, Kestrel's monthly sell-in was 14,692 in October, 15,560 in November, 18,663 in December and 5,675 in January.
7. From the sell-through and inventory returns, December sell-through was 14,511 and month-end stock rose from 20,928 to 25,068, a build of 4,140. January sell-through was 14,887, and Q4 sell-through was 44,468, or 0.91 of sell-in.
8. From account_email_export.csv, Kestrel asked on 24 November to bring its January standing orders into December to clear 110 percent, and Halden agreed to ship.
9. For context, 48,915 less 4,140 is 44,775, or 102.9 percent attainment, which is Priority tier at 105 percent and 44,100 units. This is not the Section 2 basis.
10. Confirm that supply_allocation_q1_2025_kestrel.xlsx used the same shipment basis (103.4 percent, Priority), and apply Schedule E as written for Q1 2026.

### Key traps (what the model did)

- Overrode the written allocation policy with an economic-substance adjustment. The runs netted out the December pull-forward or stock build, concluded the 112.4% attainment 'does not hold', and cut Kestrel to the Priority tier (44,100 units, 14,700/month). Schedule E Section 2 counts shipments less returns with no inventory adjustment, and last year was set on that basis.

### Justification

Schedule E sets the tier on Q4 sell-in, defined as units shipped in the quarter less returns to Halden. Section 6 leaves ordering timing to the distributor within its credit terms, and Halden scheduled and shipped the December orders as placed. The December build and the pull-forward request show that the 112.4 percent overstates Kestrel's underlying demand, and netting out the build would give Priority tier and 44,100 units. But the policy has no inventory adjustment, and last year's allocation was set on the same shipment basis. So the attainment holds as the policy is written, and Kestrel's allocation is 48,300 units. Whether Section 2 should reference sell-through or month-end stock in future quarters is a question for Schedule E, not for this allocation.

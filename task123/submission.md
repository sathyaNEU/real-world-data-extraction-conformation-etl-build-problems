## Tags

**Domain:** General Statistics & Data Science, data integration, record linkage and entity resolution.
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Rising mains A4, B2, C3 and C6 need re-phasing or a larger main before the 2027 chargers and cooktop conversions are connected.** With each apartment's demand on the phase its supply is wired to, their busiest phases reach 89% to 109% of rating against the 80% line. Not the balanced allocation, which spreads every single-phase apartment over three phases and puts no main over the line. Not the installer's rotation by apartment position, which leaves out A4 and C3 and adds A1. Not the expected busiest phase over random phasing, which adds A1.

## 2. Critical Components

1. Busiest-phase demand, existing and added, as a share of rating: A4 **109%**, B2 **94%**, C3 **97%**, C6 **89%**
2. Undesignated main nearest the line: B3 at **75%**

## 3. Step-by-Step Solution

1. Mapped each child NMI to its lot (QES_child_meter_register_20261031.xlsx), unit (OC1_register_extract_lots_20260930.xlsx) and rising main by tower and level (MSB_upgrade_2019_rising_main_schedule.pdf), and took each apartment's demand as twice its NEM12 kWh, every register, in the half-hours beginning 17:00 to 20:30 market time on 13 to 17 July 2026 (standard section 3).
2. Sorted each main's single-phase apartments into three groups by how their hourly voltages in QES_PQ_hourly_V_20260712T0000Z-20260720T0000Z.csv move together once the main's own average is taken out, since apartments on one phase sag together whenever any of them draws; the groups separate on every main.
3. Added each charger in OC1_2027_electrification_works_schedule.xlsx at 3.7 kW and each cooktop conversion at 1.4 kW to its apartment's phase, three-phase supplies split equally (sections 2 and 4).
4. Took each phase's highest summed half-hour plus its additions against 80% of the main's rating at 230 V (sections 1 and 5): A4 109%, B2 94%, C3 97%, C6 89% over the line, B3 nearest under at 75%.
5. July use: each meter's register movement between its midnight reads of 1 July and 1 August in QES_register_reads_2026-07.csv, general supply and controlled load together (section 7), through QES_meter_exchanges_2026.csv for the meters changed in July; where the midnight 1 August read is an estimate, the meter's own July intervals in the NEM12 file, since the actual read later that morning includes August's first hours.
6. Requests: one per car space in EV_charger_applications_2024-2026.xlsx, B2 and B3 numbers carried through basement_remarking_schedule_March2025.xlsx where written before the re-marking or where the written number is not one of the applicant's own spaces (by the unit written, or the lot an owner elsewhere gives) and the re-marked one is, on the main of the apartment the space belongs to (section 8); the visitor bays belong to no apartment.
7. Time outside the limits: each apartment's records in QES_PQ_events_2026-07.json joined into spans across its elements (a three-phase supply is outside while any phase is), a record counting only where the meter's own hourly maximum in QES_PQ_hourly_V_20260712T0000Z-20260720T0000Z.csv, in an hour it covers, is above 253 V, which leaves out the records the head-end re-sent ten hours after the excursion they repeat; clipped to 13 July 00:00 to 20 July 00:00 market time, over 168 hours an apartment (section 6).
8. A4, B2, C3 and C6 need works before connection; every other main stays under the 80% line.

## 4. Deliverable Answers

### riser_capacity_2027.xlsx

1. Rising mains needing works, busiest-phase share of rating in whole per cents:
   - A4: 109%
   - B2: 94%
   - C3: 97%
   - C6: 89%
2. Undesignated main nearest the line: B3 at 75%
3. Apartments' electricity use in July 2026, MWh to two decimals:
   - A1: 11.76
   - A2: 11.77
   - A3: 11.07
   - A4: 11.34
   - A5: 11.63
   - A6: 11.08
   - B1: 12.37
   - B2: 10.61
   - B3: 11.58
   - B4: 10.81
   - B5: 7.79
   - B6: 7.94
   - C1: 11.20
   - C2: 11.09
   - C3: 11.96
   - C4: 11.97
   - C5: 10.24
   - C6: 10.43
4. Charger requests lodged by the apartments' owners:
   - A1: 6
   - A2: 5
   - A3: 8
   - A4: 6
   - A5: 7
   - A6: 6
   - B1: 7
   - B2: 5
   - B3: 6
   - B4: 8
   - B5: 4
   - B6: 4
   - C1: 8
   - C2: 4
   - C3: 6
   - C4: 7
   - C5: 0
   - C6: 0
5. Share of the apartments' time in the week of 13 to 19 July outside 216 V to 253 V, per cent to two decimals:
   - A1: 1.50%
   - A2: 0.76%
   - A3: 1.61%
   - A4: 1.29%
   - A5: 1.48%
   - A6: 1.46%
   - B1: 1.02%
   - B2: 1.50%
   - B3: 1.30%
   - B4: 2.02%
   - B5: 2.21%
   - B6: 2.15%
   - C1: 1.06%
   - C2: 1.57%
   - C3: 1.32%
   - C4: 0.90%
   - C5: 2.27%
   - C6: 1.71%

### riser_phase_loading_2027.svg

1. One bar per rising main of its busiest-phase share of rating, the mains over the line in red with their shares, the 80% limit dashed across.

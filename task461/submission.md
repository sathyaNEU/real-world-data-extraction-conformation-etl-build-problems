## Tags

**Domain:** Physical & Environmental Sciences (emissions inventory: an office tower's base building Scope 2 intensity and its Scope 1 lines for a sustainability-linked loan).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Report to Corvane Bank plc that Pellow House's base building missed its 2026 target: 18.5 kg CO2e per square metre against 17.6, 0.9 kg over.**
The base building used 1,915 MWh in 2026: the import less the nine tenancy supplies, with the three comms rooms metered inside their occupiers' supplies counted once. Not every tenancy meter in the register subtracted, which takes those rooms out twice and files 15.9, inside the target; not every meter named a comms, server or equipment room left out, which leaves the roof licensee's own supply in the base building and files 19.8.

## 2. Critical Components

1. The base building used **1,915 MWh** of electricity in 2026 (import 3,477 MWh less tenancy supplies 1,562 MWh).
2. EM-102, EM-105 and EM-108 sit inside EM-101, EM-104 and EM-107: **268 MWh** that subtracting every listed meter takes out a second time.
3. Base building Scope 2 emissions are **396.5 t CO2e**, a KPI of **18.5 kg CO2e per m2**.

## 3. Step-by-Step Solution

1. Summed supplier_hh_import_1600004417286_2026.csv by settlement date into calendar months on the building's clock: the import was 3,477 MWh.
2. Read every tenancy meter in pellow_house_meter_register.xlsx from bms_energy_meter_registers_2026.csv at each month's local midnight (watt-hour registers divided by 1,000, EM-110 to its removal and EM-118 after it).
3. Compared the meters' half-hourly increments: EM-102, EM-105 and EM-108 never exceed EM-101, EM-104 and EM-107 and fell to zero exactly when those supplies were isolated in the June switchboard maintenance, so they sit inside them; EM-114 stayed live through every tenancy isolation and is a supply of its own.
4. Took the nine supplies (EM-101, EM-103, EM-104, EM-106, EM-107, EM-109, EM-110 with EM-118, EM-112, EM-114) from the import month by month, as corvane_rcf_schedule9_sustainability_kpis.pdf defines Base Building Electricity: 1,915 MWh for the year.
5. Applied parts 2 and 3 of the schedule: 0.20705 kg CO2e per kWh gives 396.5 t, over 21,460 square metres 18.5 kg CO2e per m2, 0.9 over the 17.6 target.
6. Gas oil: converted each dip in generator_tank_dips_2026.csv through generator_day_tank_calibration.xlsx, placed each week's burn on that week's runs in generator_controller_events_2026.csv to get the stock at each quarter's local midnight, and added gas_oil_delivery_dockets_2026.csv: litres by quarter below, at 2.6594 kg CO2e per litre.
7. Refrigerant: each chiller's additions in fgas_log_chillers_2026.csv less the kilograms calbrook_recovery_record_2026.xlsx recovered to cylinders on the same job: kilograms by chiller below, at a GWP of 1,430.

## 4. Deliverable Answers

### pellow_house_2026_kpi_report.xlsx

1. Base building electricity by month, MWh:
   - January: 158
   - February: 144
   - March: 156
   - April: 141
   - May: 150
   - June: 176
   - July: 190
   - August: 174
   - September: 166
   - October: 153
   - November: 152
   - December: 154
2. Base building electricity for 2026: 1,915 MWh.
3. Base building Scope 2 emissions: 396.5 t CO2e.
4. KPI: 18.5 kg CO2e per m2 against the 17.6 target: missed, by 0.9 kg.
5. Standby generator gas oil burned, litres and kg CO2e:
   - Q1: 570 litres, 1,516 kg CO2e
   - Q2: 317 litres, 843 kg CO2e
   - Q3: 318 litres, 846 kg CO2e
   - Q4: 448 litres, 1,191 kg CO2e
6. Refrigerant released, kg and kg CO2e:
   - CH-1: 10.8 kg, 15,444 kg CO2e
   - CH-2: 20.7 kg, 29,601 kg CO2e
   - CH-3: 14.8 kg, 21,164 kg CO2e
   - CH-4: 20.5 kg, 29,315 kg CO2e

### pellow_house_2026_kpi_letter.pdf

1. Result stated against the target: 18.5 kg CO2e per m2 against 17.6, missed by 0.9 kg, with the base building's 1,915 MWh and 396.5 t CO2e.
2. Chart: the base building's electricity in each month of 2026 as bars, each labelled in MWh.

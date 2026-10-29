## Tags

**Domain:** Energy Systems & Utilities (load forecasting).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Designate seven of Tallowbark Networks' sixteen zone substations for spring 2027: Gerrimbal, Kinnabar, Mundaree, Ondarra, Quorrabin, Tarravine and Wirrandel.**
Their forecast lowest demand between 10.00 am and 3.00 pm on the 2027 reference Sunday falls 0.6 to 1.1 MW below threshold once the solar soak is placed on the 23,257 controlled-load heaters whose meters switch on the network's signal. Not the four of the forecast that moves every heater into the window, which adds the 8,575 heaters on internal time switches that keep heating overnight and so clears Gerrimbal, Kinnabar and Quorrabin. Not the eleven of a forecast with no soak load, which leaves out the heaters the new signal times do move.

## 2. Critical Components

1. The reference day is Sunday 25 October 2026, network demand **-153.3 MW** at its lowest half-hour between 10.00 am and 3.00 pm.
2. The new switch-on signals reach **23,257** of the 31,832 controlled-load heaters (meters with an integral audio-frequency receiver); **8,575** are on meters with an internal time switch.
3. Forecast lowest demand at the designated substations: Gerrimbal **-13.1 MW** against -12.5 MW; Kinnabar **-15.1 MW** against -14.2 MW; Mundaree **-8.4 MW** against -7.3 MW; Ondarra **-6.7 MW** against -5.7 MW; Quorrabin **-10.6 MW** against -9.9 MW; Tarravine **-8.5 MW** against -7.6 MW; Wirrandel **-9.8 MW** against -9.0 MW.

## 3. Step-by-Step Solution

1. Converted zss_net_demand_spring2026.csv from UTC interval ends to local time (AEDT from 4 October 2026; TIBB is Tibbarin) and took the Sunday with the lowest network half-hour between 10.00 am and 3.00 pm (framework 2.2): 25 October 2026, -153.3 MW.
2. Subtracted each substation's forecast inverter capacity in solar_connections_outlook_2027.xlsx at that day's output per kW in rooftop_pv_monitoring_spring2026.json (framework 3.1a).
3. Took each heater's daily energy as its controlled-load register kWh (register named in approved_meter_models.xlsx) over the days read, all its meters, in cl_customer_reads_spring2026.csv (framework 3.2).
4. Read each heater's current meter in metering_installations_2026-12-11.csv against approved_meter_models.xlsx: 23,257 heaters have a contactor driven by an integral audio-frequency receiver and take network_notice_NN-2027-02.pdf's new signals; 8,575 run from an internal time switch and keep heating overnight.
5. Placed each reached heater at its element rating from its group's switch-on (load_control_register_2026-12-10.csv, the notice) until its daily energy was taken, summed by the metering register's zone substation, and took each substation's lowest half-hour: 7 below their framework section 4 thresholds.
6. Curtailment is the threshold less the forecast lowest demand; further capacity is the smallest, over the ten half-hours, of forecast demand less the threshold divided by output per kW.
7. For solar in service on 25 October 2026, chained der_applications_2026-12-08.xlsx through prior_application, took the latest application commissioned by that day, kept NMIs with a meter in service that day in the metering register and located them by it: 254.64 MW; the backstop share takes the commissioning of the first application carrying the inverter serial in service, on or after 1 July 2025 (framework 5.2): 32.50 MW.
8. Designated the 7 substations whose forecast lowest demand falls below threshold.

## 4. Deliverable Answers

### minimum_load_spring_2027.xlsx

1. Forecast lowest half-hour demand between 10.00 am and 3.00 pm on the reference Sunday, MW to one decimal:
   - Brindlemoor: -11.2 (threshold -12.6, clears)
   - Corrowie: -5.0 (threshold -7.7, clears)
   - Gerrimbal: -13.1 (threshold -12.5, designated)
   - Goonellan: -8.0 (threshold -11.0, clears)
   - Kellambie: -5.2 (threshold -7.7, clears)
   - Kinnabar: -15.1 (threshold -14.2, designated)
   - Mundaree: -8.4 (threshold -7.3, designated)
   - Ondarra: -6.7 (threshold -5.7, designated)
   - Orrinjal: -3.7 (threshold -5.6, clears)
   - Pelladrin: -4.8 (threshold -7.0, clears)
   - Quorrabin: -10.6 (threshold -9.9, designated)
   - Tarravine: -8.5 (threshold -7.6, designated)
   - Tibbarin: -7.3 (threshold -8.5, clears)
   - Wendimbra: -13.6 (threshold -15.5, clears)
   - Wirrandel: -9.8 (threshold -9.0, designated)
   - Wyndabar: -12.3 (threshold -14.2, clears)
2. Solar a designated substation would have to curtail at its lowest half-hour, MW to one decimal:
   - Gerrimbal: 0.6
   - Kinnabar: 0.9
   - Mundaree: 1.1
   - Ondarra: 1.0
   - Quorrabin: 0.7
   - Tarravine: 0.9
   - Wirrandel: 0.8
3. Further inverter capacity a cleared substation could take before any half-hour from 10.00 am to 3.00 pm fell below its threshold, MW to one decimal:
   - Brindlemoor: 1.9
   - Corrowie: 3.7
   - Goonellan: 4.0
   - Kellambie: 3.4
   - Orrinjal: 2.6
   - Pelladrin: 2.9
   - Tibbarin: 1.6
   - Wendimbra: 2.6
   - Wyndabar: 2.6
4. Rooftop solar inverter capacity in service behind each substation on 25 October 2026, and the part the emergency backstop can curtail, MW to two decimals:
   - Brindlemoor: 19.06 in service, 2.48 curtailable
   - Corrowie: 11.41 in service, 1.26 curtailable
   - Gerrimbal: 22.22 in service, 2.82 curtailable
   - Goonellan: 16.09 in service, 2.34 curtailable
   - Kellambie: 12.13 in service, 1.31 curtailable
   - Kinnabar: 23.57 in service, 3.02 curtailable
   - Mundaree: 15.66 in service, 1.86 curtailable
   - Ondarra: 12.71 in service, 1.42 curtailable
   - Orrinjal: 8.46 in service, 1.11 curtailable
   - Pelladrin: 8.99 in service, 1.06 curtailable
   - Quorrabin: 18.66 in service, 2.56 curtailable
   - Tarravine: 12.79 in service, 1.79 curtailable
   - Tibbarin: 13.28 in service, 1.74 curtailable
   - Wendimbra: 22.52 in service, 2.87 curtailable
   - Wirrandel: 15.99 in service, 2.21 curtailable
   - Wyndabar: 21.11 in service, 2.65 curtailable

### minimum_load_briefing_2027.docx

1. One-page briefing to the Minister recommending the 7 designations, with a bar chart of each substation's forecast lowest demand against its threshold, designated substations in amber.

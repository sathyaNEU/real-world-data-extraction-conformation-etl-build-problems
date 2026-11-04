# leak check, task461

**Verdict: REVIEW.** 13 files read, 35 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: tenancy, meters, register, occupier, inside, supply, golden, screen, supplies, another, emissions-inventory, import, sentence, registers, metered, decisive, second, location, hierarchy, architecture, system, parent, dockets, occupiers, premises

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `corvane_rcf_schedule9_sustainability_kpis.pdf`: \bdesign note\b|\bgenerator\b x1, a field term declared in metadata.json: ...pe 1 lines. 4.2 Gas oil: the litres burned by the Building's standby generator in each quarter, at 2.6594 kg CO2e per litre. 4.3 Refrigerant: the...

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `corvane_rcf_schedule9_sustainability_kpis.pdf`: carries 9 of 11 distinctive words of the committed call: "Report to Corvane Bank plc that Pellow House's base building missed its 2026 target: 18.5 kg CO2e per square metre again"

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `corvane_rcf_schedule9_sustainability_kpis.pdf`: 5 of 25 stump-paragraph terms appear (tenancy, occupier, supply, import, metered); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 describing content (REVIEW 1)
- **REVIEW** `corvane_rcf_schedule9_sustainability_kpis.pdf`: names 4 column(s) of the data files verbatim (MPAN, Refrigerant, litres, refrigerant): confirm it is the organisation's own record and not a note written for the analyst

## 1 file names (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), architecture 3, on a fresh copy of prompt.txt and target/ (target.zip sha256 686519e805067906d17f195fe3a964f49732590b216357a077303e06fc2ab2d5). Sweep 2 and 4 lines and the answer-figure line were ruled in the main thread.

# Reader answers (task461 v3)

1. Decisive step: no file announces it. Closest are the loan's own definitions: schedule9 1.4 "Base Building Electricity means the electricity imported to the Building through the revenue meter (MPAN 1600004417286) in the Measurement Period, less the electricity supplied in that period to the Tenancies as metered at each Tenancy's supply." This is a definition, not a hint.
2. Ranks or scores the candidates: none. The schedule gives only the target (2026: "17.6"); no file states a result or a verdict.
3. Exists only to help the analyst: none. The meter register and tenancy schedule are the nearest, see c.
4. Reads as the answer: none. Only the 2026 target 17.6 and the factors (0.20705, 2.6594, 1,430) appear, and they are standing loan terms.
5. Filed literal sentences: schedule9 1.4 (revenue-meter import less tenancy-supply electricity as metered at each Tenancy's supply, calendar year 2026 local time, 1.2); 1.5 "Net Lettable Area means 21,460 square metres" (denominator; EPC says 27,940 useful floor area, an unused distractor); 2.1 "Base Building Electricity multiplied by 0.20705 kg CO2e per kWh"; 2.2 "KPI means ... divided by Net Lettable Area"; 4.2 "the litres burned by the Building's standby generator in each quarter, at 2.6594 kg CO2e per litre"; 4.3 "the refrigerant released from each chiller in the Measurement Period ... 1,430 for R-134a". Literal result: population = import through MPAN 1600004417286 for 1 Jan to 31 Dec 2026 minus tenancy-metered supply at each tenant's supply; unit kg CO2e/m2 on 21,460 m2; Scope 1 by quarter (gas oil) and by chiller for the year (refrigerant). It does not say how burned litres or released kg are derived, nor how a removed/replaced tenancy meter is handled.
6. Decider: mostly following stated definitions and data handling (the tenancy-meter deduction across a meter swap EM-110 to EM-118, Wh versus kWh units, burned litres from dips/calibration/deliveries, released refrigerant from top-ups versus recharge). The main call (met or missed 17.6) turns on computing 1.4 correctly; nothing is flagged as a trap. Reading units and the meter changeover is a semantics/rule-following step. Deciding file: schedule9 Part 1.4 with pellow_house_meter_register.xlsx and the BMS export.

a. Harmless, because it holds only definitions, a target table, margin ratchet and reporting terms in an agreement voice; no passage states a 2026 result or hints how to treat any meter.
b. Harmless, because it is a dated facility agreement between Wexmoor Office Trust plc and Corvane Bank plc ("Executed as part of the Agreement"); it names MPAN and the quantities (litres, chiller, quarter) as contract language, not as a note to the analyst, and no column names are quoted as such.

c. Reads as the building's own meter register (CT ratio, installed dates, "Recharged to occupier", register units, "Register as at 05/01/2027"), kept for billing recharge and asset records. The only notes are "Removed 18/08/2026, replaced by EM-118" and "Replaces EM-110", which are ordinary asset-record entries. The "Recharged to occupier" Yes/No column and "Base building" occupier labels do separate tenancy from base meters, which points at the deduction step modestly, but that is what a recharge register does. Harmless.
d. Reads as an ordinary BMS export: half-hourly cumulative registers, mixed Wh/kWh units per point, EM-110 ending and EM-118 starting from 0.0 on 18/08/2026 (consistent with the register note), 368 distinct dates (31/12/2025 start). Nothing placed beyond what the register explains. Harmless.
e. Both ordinary. calbrook_recovery_record_2026.xlsx is authored by "Calbrook Cooling Services", with job numbers matching the F-gas log, cylinders and destination. generator_day_tank_calibration.xlsx is a dip-to-litres strapping table (Dip mm, Contents litres), a normal site record. Neither points at a step beyond giving the data. Minor note: the F-gas log dates (12/03) differ from the recovery record dates (10/03) for the same job, which reads like real paperwork drift.

Realism: none that clearly reads machine-made. Faint tells only: gas_oil_delivery_dockets_2026.csv has two consecutive dockets (550 and 650 litres) at the same time 11:20 on the same day to the same tank, which can look contrived; the authors of the xlsx files are all "Kate Harding" (metadata, a single person for tenant schedule, register and calibration across different organisations), and the BMS/hh files are very regular.

### Second read, after the FIX_NOW repair

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), on a fresh copy of prompt.txt and target/ (target.zip sha256 c50af2ddfe8280c1f401025d932b9a923c9fa1a80bd4d13b4331293c1a0e9c68), after the meter register's descriptions stopped sorting the meters and the prompt pinned Scope 2's rounding.

# Leak read, Pellow House pack

1. Decisive step stated? None as a step. Closest: Schedule 9 cl. 1.4 "Base Building Electricity means the electricity imported to the Building through the revenue meter (MPAN 1600004417286) in the Measurement Period, less the electricity supplied in that period to the Tenancies as metered at each Tenancy's supply." This is the loan's own definition; it does not say which meters are whole-supply and which are nested.
2. Ranks or scores candidates on the question: none. (The EPC gives an asset rating 63 / band C and a BER of 38.21, modelled not operational, and says so; it does not answer the 2026 question.)
3. File only to help the analyst: none. Every file reads as a counterparty record. Nearest: the meter register and tenancy schedule, but both are the building's own records.
4. Figure or name reading as the answer: none. Targets (2026: 17.6), factor 0.20705, NLA 21,460 are loan terms and inputs. The EPC floor area 27,940 m2 differs from NLA 21,460, which is context.
5. Literal-fixing sentences: cl. 1.4 above fixes the population as revenue-meter import minus electricity supplied to Tenancies "as metered at each Tenancy's supply", calendar year 1 Jan to 31 Dec in the Building's local time (cl. 1.2). Cl. 2.1 "Base Building Electricity multiplied by 0.20705 kg CO2e per kWh" and 2.2 "divided by Net Lettable Area" fix the unit as kg CO2e per m2 on 21,460 m2. Cl. 3 Target 2026 is 17.6 "not more than". Cl. 4.2 "the litres burned by the Building's standby generator in each quarter, at 2.6594 kg CO2e per litre" and 4.3 "the refrigerant released from each chiller in the Measurement Period, at a global warming potential of 1,430" fix the Scope 1 lines. Result: tenancy supply is measured per tenancy supply (not per meter), so the quantity depends on identifying each Tenancy's supply point from the data.
6. What decides the main answer: an analytical choice about the unit of analysis, i.e. "as metered at each Tenancy's supply" (cl. 1.4) against a register that lists 22 meters with some tenants holding several. Nothing says which are sub-meters of others; that has to be established from the interval data. Not a planted decoy, and the definition is stated. Partly a rule-application / reconstruction flavour once the nesting is found. Also needs the DST, Wh/kWh and replacement-meter (EM-110/EM-118) handling, which are mess.

## Flagged items
a. harmless, because Schedule 9 holds only definitions, targets and reporting terms; no passage states a 2026 KPI, an electricity total or a result.
b. harmless, because it names only the MPAN (also in the supplier file name/column) and reads as the parties' executed agreement ("Executed as part of the Agreement", dated, parties named, page footer). It does not use the BMS column names (Point, Units, Value) and carries no analyst-directed note.

## Specific files
c. Register and tenancy schedule read as the building's own records (Vantrell Controls register "as at 05/01/2027"; Wexmoor Office Trust schedule "at 31/12/2026"). Could a reader tell whole supply from nested part without interval data? Not directly, but there are circumstantial hints: several tenants have two meters in the same location with differing CT ratio ("EM-101 L2 east riser 300/5" and "EM-102 L2 east riser Whole current"; "EM-106 L7 east riser 200/5" and "EM-119 L7 east riser Whole current"; "EM-108 L9 east riser" and "EM-115 L9 east riser"; "EM-112" and "EM-117" both "L13 east riser"; EM-110/EM-116 for Mordaunt). A reader could guess that a CT-metered meter plus a whole-current one in the same riser means a part-inside-whole arrangement, but the register never says which is which, and the "Recharged to occupier" column is "Yes" for all. No column, note or description says "sub-meter" or "check meter". The only Notes are the EM-110/EM-118 replacement. Minor: tenancy schedule row "Lease (data room)" for Varnhold G.04 and Tamsett's two levels with EM-107/EM-108/EM-115 allow cross-reading tenancy to meters but not nesting. Weak hint only, not a leak.
d. BMS CSV reads as an ordinary export: 22 points, 30-minute cumulative registers, mixed kWh and Wh units per point (EM-103, EM-204 in Wh), one common 09:30 gap and a 01:30 gap on all meters (outage and spring clock change), duplicated timestamps in the autumn clock change, one counter decrease per meter (rollover or reset), EM-110 ending 18/08/2026 10:30 as EM-118 starts. All the gaps are common to every meter, consistent with a logger rather than something placed on one meter. Nothing reads as placed to be caught.
e. Yes. Tenancy schedule: author Kieran Warner, company Wexmoor Office Trust plc (landlord). Meter register: Company Vantrell Controls Ltd (BMS contractor), author blank, created 2016, modified 05/01/2027. Calbrook recovery: Calbrook Cooling Services. Tank chart: Brenlow Tanks Ltd, dated 2011. All plausible; the tank chart's Excel from a 2011 vendor is slightly odd but harmless.

## Realism
Minor tells only: calbrook_recovery_record_2026.xlsx uses plant refs PH-01..PH-04 and job dates (10/03, 16/06, 08/09, 03/11) that differ from fgas_log_chillers_2026.csv (CH-n, 12/03, 18/06, 10/09, 05/11), which reads as two systems with their own conventions and is plausible. Also generator_day_tank_calibration.xlsx is a clean monotonic chart with a sheet footer line, and the BMS date-format and the Calbrook sheet have no oddity. Otherwise none.

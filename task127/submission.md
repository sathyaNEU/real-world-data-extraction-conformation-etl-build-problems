# task127 · Minnesota Clean Heat Fund, 2027 heat-pump rebate slots across six co-operatives

## Tags

**Domain:** Nonprofit & Grant-making (giving strategy and program funding: a clean-heat fund splitting its programme year's rebate slots across the co-operatives it pays through).
**Analytical objective:** Opportunity Sizing & Decision Support (each co-operative's 2027 rebates sized from its eligible homes down to the installs its feeders can host and the meters its crew can set before the slots lapse).

## 1. Final Recommendation

**Place 1,170 of the 1,800 slots in 2027: North Shore 160, Valley 180, Lakes 240, Uplands 170, Riverbend 340, Pinewood 80, with 630 left unallocated.**

Riverbend takes the most, 100 slots ahead of Lakes. Not 1,800 shared on expected installs, which ignores that North Shore's and Valley's feeders take only 161 and 182 installs. Not the feeder-capped split with Lakes first, which assumes every meter is set before year-end when Lakes' and Uplands' crews set only 239 and 171. Not Uplands first on its count of qualifying homes, because most of them heat with the systems the pilot converted least often.

## 2. Critical Components

1. Pilot install rates by heating system replaced: **3 in 38** propane furnace (ducted), **1 in 32** electric resistance, **1 in 95** propane boiler (hydronic)
2. Installs the feeders can take in 2027: North Shore **161**, Valley **182**, Lakes **418**, Uplands **297**, Riverbend **342**, Pinewood **80**
3. Spare heat-pump meter sets a working day after standing work: Lakes **2.44**, Uplands **1.75**
4. Meters set by 31 December 2027: Lakes **239**, Uplands **171**, every feeder-capped install at the other four co-ops
5. Slots placed **1,170**, unallocated **630**

## 3. Step-by-Step Solution

1. Kept the `heat_survey_2025_households.csv` homes eligible under section 2 of `heat_pump_programme_rules_2027.pdf` (owner, single-family detached, income $35,000 to $149,999, heating PF, PB or ER), weighted, outside the six pilot neighbourhoods the same section excludes.
2. Divided `pilot_rebates_2026.xlsx` installs by heating system replaced by the eligible weighted homes of the six pilot neighbourhoods: 3 in 38, 1 in 32 and 1 in 95, which reproduce every pilot neighbourhood's installs, and applied them to each 2027 neighbourhood's eligible homes.
3. Joined neighbourhoods to feeders with `area_feeder_map.csv` and capped each feeder's expected installs at its `hosting_capacity_nov2026.xlsx` remaining kW over 5 kW a heat pump (section 3 of `cooperative_participation_terms.pdf`): 161, 182, 418, 297, 342 and 80.
4. In `field_orders_2025_2026.csv`, the two Monday-to-Thursday crews averaged 10.50 (Lakes) and 8.74 (Uplands) completed orders a working day from the first completion of the MXCH batch requested on 7 July 2025 up to, but not including, the day of its last completion, and 8.06 and 6.99 completed orders other than HPRM and that batch a working day from 12 December 2025 to the 10 December 2026 pull: 2.44 and 1.75 spare.
5. Raised each co-op's capped installs as meter orders on the 2027 dates of the pilot's install dates (same month and day, in the pilot's shares) and worked them day by day from the crew's next working day at the spare rate, skipping the holidays the crews kept in 2025 and 2026: Lakes sets 239 and Uplands 171 by 31 December, while the five-day crews, whose best 15 working days on record leave room for every order, set every meter.
6. Rounded each co-op's meter sets to the nearest ten under section 5 of the rules, whose sharing branch does not fire: 1,170 placed and 630 unallocated.
7. For the pilot audit, took each job's latest accepted invoice version (`finance_procedures.pdf` section 2) with a multi-zone system's repeated indoor-head lines counted once (`installer_price_guide_2026.pdf`) against the Schedule B rebate, and summed `rebate_payments_2026.csv` payments cleared by 30 November 2026 in Central time, leaving out those in `bank_returns_2026.json` (finance procedures sections 4 and 5).
8. Recommendation: place 1,170 slots, Riverbend 340 first, and hold 630.

## 4. Deliverable Answers

### slot_split_board_note_2027.docx

1. 2027 slots: North Shore 160, Valley 180, Lakes 240, Uplands 170, Riverbend 340, Pinewood 80
2. Unallocated: 630 of the 1,800 (1,170 placed)
3. Co-op taking the most slots: Riverbend, 340
4. Lead over the next: 100 slots ahead of Lakes

### coop_slot_split_2027.csv

1. One row per co-op plus a total row, whole dollars, rebate share to one decimal:
   - North Shore: 160 slots, average installed cost $16,962, rebate 23.6% of cost, $326,400 paid through 30 November 2026, covering 82 pilot installs
   - Valley: 180 slots, average installed cost $16,952, rebate 23.8%, $295,200 paid, covering 74 pilot installs
   - Lakes: 240 slots, average installed cost $14,786, rebate 29.7%, $143,800 paid, covering 32 pilot installs
   - Uplands: 170 slots, average installed cost $15,062, rebate 29.2%, $121,000 paid, covering 27 pilot installs
   - Riverbend: 340 slots, average installed cost $16,794, rebate 24.0%, $290,800 paid, covering 72 pilot installs
   - Pinewood: 80 slots, average installed cost $14,263, rebate 31.7%, $219,000 paid, covering 49 pilot installs
   - Total: 1,170 slots, matching the note; average installed cost $16,170, rebate 25.7%, $1,396,200 paid, covering 336 pilot installs

### coop_slots_2027.svg

1. A pair of bars per co-op, 2027 slots beside 2026 pilot installs, largest allocation first: Riverbend 340 and 92, Lakes 240 and 40, Valley 180 and 88, Uplands 170 and 32, North Shore 160 and 100, Pinewood 80 and 60
2. Unallocated slots as a bar of their own: 630
3. Every bar labelled with its value
4. Title with the total placed: "2027 rebate slots: 1,170 of 1,800 placed, Riverbend takes the most"

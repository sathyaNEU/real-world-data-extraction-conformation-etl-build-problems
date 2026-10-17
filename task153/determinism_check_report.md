# Verdict: task153 (Overton yard-island loads, Sep 14 to Nov 8 2026)

## Verdict
DETERMINISTIC. All committed answers reproduce from the shipped files. (No SOLUTION_WRONG: the solution blocks are accurate to within about 10 gallons on the yard draws, which no load count depends on; one wording nit is listed under Evidence.)

## Disposition
APPROVE. No repair needed and no model rerun. One optional one-clause pin on the saving is listed under Fix.

## Why
The main call (23 loads: Memphis 2, Jackson 5, Nashville 8, Cookeville 1, Knoxville 4, Blountville 3) is forced because the only physically grounded way to size what an island "will hand out" from the shipped files is per yard visit, capped by what each vehicle's tank can take. My independent rebuild gives the same six counts, and they survive every reasonable variant I tried (cap from 0% to 20% below tank, scaling 39 to 40 days or none, visits dated by enter or exit). The difficulty is the capture estimate, not a wording choice. The easy routes (card gallons, or uncapped burn between visits, both 29 loads) fail for an analytical reason. The 8,000-gallon whole-load floor and the adder arithmetic leave no second reading.

## Literal reading (done first)
The prompt gives no draw formula. Options where the text is silent, and what each gives:

| Silent point | Options | Loads |
|---|---|---|
| What counts as the island's draw | (a) card gallons of the yard's vehicles; (b) all fuel burned between yard visits, no tank limit; (c) between-visit burn limited to what the tank takes per visit | (a) 29, (b) 29, (c) 23 |
| Tank limit | none / full tank / tank less 10.2% / tank less 15% / tank less 20% | none 29; others all 23 |
| 8-week to 8-week scaling | 39 working days scaled to 40 / unscaled | 23 / 23 |
| Window edge (visit dated by enter or exit) | either | 23 / 23 |
| Opening tank dips (all within a few hundred gallons of the unpumpable heel) | ignored | no effect |
| Whole loads | floor per yard (prompt: "only the whole loads") | fixed by the text |
| Savings basis | adder difference on the same TriState average (offer: "the same average your three card programmes bill from"; Crossroads fee "part of the diesel price") | $17,408 |

Only option (c) is grounded in the files (geofence visits, model fuel tanks, FMS fills capped near 269 of 300), and every parameter choice inside (c) gives 23.

## Evidence (recomputed from the bundle)
| Value | Source | Reproduced |
|---|---|---|
| 157 active units, yards, tanks | fleet_units_2026-08.xlsx | yes |
| Device serials mapped to vehicles (6 swapped devices) | telematics_device_assignments.csv | yes, 0 unmapped rows |
| FMS 2025: 2,506 fills after removing resent rows; 48 fills over 225 gal, mean 269.29 (tank less 10.24%), all T680 | fms_island_transactions_2025.csv | yes |
| Yard draw, 29 Jun to 23 Aug, scaled by 40/39 (Memphis, Jackson, Nashville, Cookeville, Knoxville, Blountville) | geofence + vehicle_days + units | 21,303 / 44,697 / 69,403 / 12,900 / 37,576 / 27,845, against the golden 21,303 / 44,695 / 69,402 / 12,898 / 37,575 / 27,835 (within 10 gal) |
| Loads per yard | floor of draw/8,000 | 2 / 5 / 8 / 1 / 4 / 3 = 23 (reproduced) |
| Visit patterns (Nashville sleepers 2 visits a week, Blountville sleepers and Cookeville vans 1 a week) | geofence | yes: 16 visits per Nashville sleeper in 8 weeks; 88 Blountville sleeper visits (all capped); Cookeville vans 1 a week |
| Saving per load $800 / $640 / $864 | pricing schedules + offer; adders checked against the card files in every quarter (Riverbend +0.119 Memphis, Crossroads +0.084 Nashville, SMPM +0.127 Knoxville) | yes; 23 loads = $17,408 |
| Delta Riverbend gallons May / Jun / Jul | UTC to Central, credits netted to the month of the duplicate they reverse, DEF excluded | 33,472 / 36,732 / 37,170 yes |
| Keeble Crossroads gallons | 10 pm business-day rule, reversals netted to the original | 46,569 / 54,781 / 52,821 yes |
| Holston SMPM gallons | resent batch 0088202 (a verbatim repeat of 0088201's 144 details) removed, credits netted, 10 pm rule | 46,391 / 51,215 / 53,258 yes |
| Jackson Mar / Apr / May 2025 | BOL net gallons by delivery month; billed (product, freight, service, net of credit memos and rebills) less BOL gallons x rack in force at lift (6 pm posting rule) | 31,911 gal $891; 24,004 $811; 7,986 $254 yes |
| Knoxville Jun / Jul / Aug 2025 | same | 23,977 $446; 24,021 $542; 8,021 $191 yes |

Billed unit prices equal rack plus the contract adder on every load under the 6 pm rule, so the rack timing is confirmed by the files themselves.

Competing answers tried and rejected:
- 29 loads (card gallons or uncapped burn): ignores that Blountville sleepers burn 544 gal a loop against a 269-gal tankful, and that Cookeville vans burn about 80 gal a week against a 22-gal tank. Blountville would be 6 loads, Cookeville 3, Knoxville 5.
- Dropping the reserve entirely (cap = full tank): still 23.
- Unscaled eight weeks: still 23.

Minor notes (none moves a committed figure):
1. Solution step 3 says "each vehicle's fill is capped at its tank less 10.2%", but the T680 is the only model with fills at the cap. Two Sprinter fills (23.7 and 23.9 gal) exceed 89.8% of a 24.5-gal tank. Raising the Sprinter cap to 23.9 moves Cookeville from 12,900 to about 13,390, still 1 load. The count does not rest on the 10.2%.
2. Savings assume the card price and Overton's price sit on the same terminal average. The offer states this. About 7% of recent SMPM gallons (Kentucky sites) are priced off the Nashville terminal, which would add roughly $95 if someone priced the hypothetical gallons by site. This needs no fix, but it is the only soft spot in the $17,408.
3. The fob note ("fobs issued for those programmes still work at every island, and new units get a fob at delivery") does not say that Memphis, Nashville, Cookeville and Blountville vehicles hold fobs. The prompt and offer clearly treat all six islands as usable, so I read this as intended, but a hyper-literal reader has an open question here.
4. The figures quoted in the solution for the rejected routes (26 to 28 and 19 loads) are not committed answers; I did not reproduce them.

## Files/Hygiene
PASS. 22 input files; formats: csv (9), xlsx (4), pdf (6), txt (1), md (2). Largest tables: vehicle_days 79,042 rows, geofence 42,446, Crossroads 33,093, Riverbend 21,351. Layer 1 mess is authentic (device swaps with serial-named rows, UTC against local time, a 10 pm business day, 5-digit and spaced unit numbers, a fixed-width file with a resent batch, reversals carrying references, a 180-day geofence history). Dates are coherent: files pulled Aug 28, 2026; telematics through Aug 27; SMPM through Aug 23; offer Aug 26; commitment due Sep 4; Labor Day Sep 7 sits outside the window. The July 3 closure (39 working days) is visible in the telematics, though the notes do not list it as a company holiday. No authoring or benchmark language found (grep of all text and office metadata). Apparent unused distractors: overton_tank_wagon_prices_2026-08-24.pdf and ifta_returns_2025Q3-2026Q2.xlsx (I could not check metadata.json under the isolation rules). Real vs fictional public data: all fictional operational artifacts, no contamination. No exclusion-level finding. Cross-batch check: not possible under the isolation rules (no other task folder or report read); the stump mechanism (dwell and tank-limited yard capture) was not compared with any other build.

## Stump power
Good. Nothing in the prompt or documents explains the capture model. A strong model must rebuild yard visits from geofence events, keep the visits a vehicle actually makes at its own yard (Nashville's midweek reload, Blountville and Cookeville once a week), and limit each fill to the tank. The natural wrong answers are 29 (card gallons or uncapped burn), a 2025-island-share route, or a nights-at-the-yard route, any of which changes at least one yard count or the total. The asks add many independent chances to slip (UTC, 10 pm business day, credits, resent batch, rack posting time), so a response matching all 6 counts, the total and the saving is unlikely by luck. No model runs were supplied, so this is an estimate only.

## Stumping type
`mechanism: binding_constraint` (capture volume limited by yard dwell and tank size, with an opportunity-sizing flavour), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
The reported card gallons are correct; they answer a different question (the pool, not what an island can hand out), so the task is not a flip away from a wrong reported number. On perfectly clean data the same capture estimate still separates 23 from 29, so the clean-data test passes. This is not a banned scaffold.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Domain: fleet fuel procurement and yard fuelling economics; the deciding quantity is the volume a bulk site can actually capture from telematics dwell and tank limits, which would not read the same with hospitals or megawatt-hours swapped in.
- Layer 1 (mess): changed device serials, UTC against Central/Eastern time, the 10 pm business day, messy unit keys, credits and reversals, a resent SMPM batch, a holiday gap.
- Layer 2 (rigour): between-visit burn limited by what a tank can take per visit, judged against the FMS evidence of what drivers take.
- Easy route and its wrong answer: a strong analyst who cleans everything and reads every rule correctly can still take the pooled card gallons (or uncapped between-visit burn) as the island's reach, giving 29 loads and a saving of 29 x the account adders, instead of 23 and $17,408. The 10.2% reserve is recoverable from the 2025 fills but the counts do not depend on it, so no hidden rule decides the call.

## Fix
none. Optional, no rerun needed: the optional pin for the only soft spot is one clause in the prompt or the offer reading ("price both at the yard's own terminal average"); it is not required for determinism because the offer already says the averages are the same.
